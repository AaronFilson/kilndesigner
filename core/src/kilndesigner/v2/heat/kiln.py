"""A kiln's heat model from its design file: the fuel, the chamber the engine draws and its
openings, the rays through it with the setting in the way, the gas's grey gases, the walls from
the lining, and the draft (ADR 0017 H1–H13).

The load is required (ADR 0017 decision 11): no heat result without one. The design file says
what it can of it (`firing.ware`, `firing.setting`); the setting's envelope and emissivity it
doesn't, so they are the caller's, stated (`Load.reference`).
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

import numpy as np

from kilndesigner.library import material
from kilndesigner.model import Dome, Kiln, SprungArch
from kilndesigner.shape import FaceShape
from kilndesigner.thermal.surface import StillAirSurface
from kilndesigner.thermal.transient import HeatCapacity, Layer
from kilndesigner.units import si
from kilndesigner.v2.heat import air as air_mod
from kilndesigner.v2.heat import chamber as ch
from kilndesigner.v2.heat import draft as dr
from kilndesigner.v2.heat import gas, gasrad, rays
from kilndesigner.v2.heat import sources as src
from kilndesigner.v2.heat.ground import DRY, Ground, Soil, ground
from kilndesigner.v2.heat.walls import CellWall, Outside, face_sides, grown, linear_area
from kilndesigner.v2.heat.zone import (
    CONVECTION,
    CONVECTION_NOTE,
    ELEMENTS_NOTE,
    Elements,
    Face,
    Flow,
    Gas,
    Line,
    Opening,
    Setting,
    ZoneModel,
    fired_clay,
    line,
)
from kilndesigner.working import Step

NOMINAL = 1558.15  # K: the gas composition the grey gases are taken at (cone 10 at 60 °C/h)
WALL_FACES = ("left", "right", "front", "back", "floor", "roof")


class NotModelledError(ValueError):
    """What the heat model doesn't take yet, or what the design must say first."""


@dataclass(frozen=True)
class Load:
    """The setting: its mass (kg), its envelope in the chamber's frame (m) and its surface's
    emissivity, with where each comes from; ``gap`` the passages between its ware (m), an end of
    the stated band `sources.SETTING_GAP` (the wide end, the lower coefficient, unless given)."""

    mass: float
    lo: tuple[float, float, float]
    hi: tuple[float, float, float]
    emissivity: float
    reference: str
    gap: float = src.SETTING_GAP[1]


@dataclass(frozen=True)
class Wood:
    """Wood as fired: wet-basis moisture and net heating value per oven-dry kg (J/kg)."""

    moisture: float
    net_dry: float
    reference: str


def fuel_of(kiln: Kiln, wood: Wood | gas.Fuel | None) -> gas.Fuel:
    """The fuel a design burns: its burners' gas; or for a fire, the fuel given (each kiln's own,
    ADR 0017 decision 12: wood, coal or oil by its analysis, `gas.solid`), else the design's own
    wood (`site.wood`) on the surrogate's analysis."""
    heat = kiln.heat
    if heat.electric is not None and heat.gas is None and heat.fire is None:
        return gas.ELECTRIC  # elements as face sources (`elements_of`): the chamber holds air
    if heat.electric is not None:
        raise NotModelledError("elements beside burners or a fire (a hybrid) aren't modelled yet")
    if heat.gas is not None and heat.fire is None:
        f = heat.gas.fuel
        return gas.propane() if f == "propane" else gas.natural_gas()
    if heat.fire is not None and heat.gas is None:
        kind = heat.fire.fuel
        if isinstance(wood, gas.Fuel):
            if wood.kind != kind:
                raise NotModelledError(f"the design burns {kind}, the fuel given is {wood.kind}")
            return wood
        if kind != "wood":
            raise NotModelledError(
                f"{kind}: give the fuel's analysis, moisture and heating value (gas.solid, from "
                "kiln-fuels.md); the design file holds none"
            )
        if wood is None and kiln.site.wood is not None:
            w = kiln.site.wood
            wood = Wood(si(w.moisture, ""), si(w.heating_value, "J/kg"), "the design's site.wood")
        if wood is None:
            raise NotModelledError("the wood's moisture and heating value: the design gives none")
        return gas.wood(wood.moisture, wood.net_dry)
    raise NotModelledError("one kind of heat at a time: gas burners or a fire")


def rated_fuel(kiln: Kiln, fuel: gas.Fuel) -> float | None:
    """The burners' fuel at their rating (kg/s), the rating on the gas's higher heating value."""
    g = kiln.heat.gas
    if g is None or g.burners.rating is None or g.burners.count is None:
        return None
    return g.burners.count * si(g.burners.rating, "W") / fuel.hhv


def _layer(x: object) -> Layer:
    """A lining layer as v1's transient wall takes it: the library's k(T), density and c_p(T);
    a dense firebrick's c_p from fired clay's 800 J/(kg·K) at 24 °C (Lienhard) up to its VDI points,
    as v1's ware curve; an IFB's single point held (the library's rule)."""
    from kilndesigner.model import Layer as DesignLayer
    from kilndesigner.units import parse_quantity

    assert isinstance(x, DesignLayer)
    m = material(x.material)
    rho = si(parse_quantity(m.density), "kg/m**3")
    if m.specific_heat is None and x.specific_heat is not None:
        cp = HeatCapacity.constant(si(x.specific_heat, "J/(kg*K)"))
    elif m.specific_heat is None and m.kind in ("insulating_castable", "dense_castable"):
        cls = material(src.CASTABLE_CP_FROM).specific_heat  # castables.md §14.3's class value
        assert cls is not None
        ts, cs = cls.to_points()
        cp = HeatCapacity(tuple(ts), tuple(cs))
    elif m.specific_heat is None:
        raise NotModelledError(f"{x.material}: no specific heat sourced or given")
    else:
        ts, cs = m.specific_heat.to_points()
        if m.kind == "dense_firebrick" and ts[0] > src.FIRED_CLAY_AT:
            ts, cs = (src.FIRED_CLAY_AT, *ts), (src.FIRED_CLAY_CP.value, *cs)
        cp = HeatCapacity(tuple(ts), tuple(cs))
    return Layer(x.material, si(x.thickness, "m"), m.k, rho, cp)


type Emissivity = Literal["nominal", "low", "high"]
# The emissivity class as a band (ADR 0017 decision 17): each brick's measured lines, the lower and
# the higher at kiln temperatures (radiation-exchange.md §5: MPK 140 under MPK 125, Osborn's
# medium-alumina fire brick under his low-alumina), and the hemispherical share of the normal
# value, 0.95–1.0 (Jones et al. [R6] Fig. 6)
EMISSIVITY_CLASS: dict[str, tuple[dict[str, str], float]] = {
    "nominal": ({"insulating_firebrick": "ifb-mpk125", "dense_firebrick": "dense-medium",
                 "fibre_blanket": "fibre-normal", "insulating_castable": "ifb-mpk125",
                 "dense_castable": "dense-medium", "stone": "dense-medium",
                 "building_brick": "dense-medium"}, src.HEMISPHERICAL.value),
    "low": ({"insulating_firebrick": "ifb-mpk140", "dense_firebrick": "dense-medium",
             "fibre_blanket": "fibre-parallel", "insulating_castable": "ifb-mpk140",
             "dense_castable": "dense-medium", "stone": "dense-medium",
             "building_brick": "dense-medium"}, 0.95),
    "high": ({"insulating_firebrick": "ifb-mpk125", "dense_firebrick": "dense-low",
              "fibre_blanket": "fibre-normal", "insulating_castable": "dense-low",
              "dense_castable": "dense-low", "stone": "dense-low",
              "building_brick": "dense-low"}, 1.0),
}  # fmt: skip
# Stone (granite) and building brick have no hot-face emissivity in any source read
# (radiation-exchange.md §4): carried as the dense fire brick's band, the nearest measured silicate
# ceramics, said in the working (`_class_notes`)
# A fibre blanket's hot face: a folded module shows its fibres end on, the normal-fibre line its
# nominal; a laid blanket's lie parallel, the band's low end (radiation-exchange.md §5.3)


CASTABLES = ("insulating_castable", "dense_castable")
FIBRE_NOTE = (
    "a fibre blanket's hot face takes Fletcher and Williams' fibre board lines (radiation-"
    "exchange.md §5.3): fibres normal to the face (a folded module's) nominal, parallel (a laid "
    "blanket's) the band's low end"
)


def _class_notes(faces: Sequence[Face]) -> list[str]:
    """What the walls take from a class rather than their own material: a castable's specific
    heat and hot-face emissivity, a fibre blanket's emissivity."""
    layers = [x.name for f in faces for x in f.wall.layers]
    hot = {material(f.wall.layers[0].name).kind for f in faces}
    out: list[str] = []
    if any(material(x).specific_heat is None and material(x).kind in CASTABLES for x in layers):
        out.append(src.CASTABLE_CP_NOTE)
    if hot & set(CASTABLES):
        out.append(src.CASTABLE_EMISSIVITY_NOTE)
    if "fibre_blanket" in hot:
        out.append(FIBRE_NOTE)
    if hot & {"stone", "building_brick"}:
        out.append(
            "stone or building brick at the hot face: no hot emissivity measured "
            "(radiation-exchange.md §4), carried as the dense fire brick's band"
        )
    return out


def _emissivity(material_id: str, cls: Emissivity = "nominal") -> Line:
    """A brick's hot-face emissivity line in an emissivity class (`EMISSIVITY_CLASS`)."""
    kind = material(material_id).kind
    keys, factor = EMISSIVITY_CLASS[cls]
    if kind not in keys:
        raise NotModelledError(f"{material_id}: no hot-face emissivity sourced for {kind}")
    return line(keys[kind], factor)


# A clay flue liner's wall (clay-flue-liners.md): a fireclay body (ASTM C315's liners are fire clay
# or shale, its tables unread), taken as the library's fireclay brick, Alsey Smithfield, 5/8 in:
# Rumford's standard 8½ × 8½ in flue weighs 36 lb a 2 ft piece, 26.8 kg/m, which at Smithfield's
# 2,086 kg/m³ is 19.9 in² of wall, t = (8.5 − √(8.5² − 19.9))/2 = 0.63 in (Derived)
FLUE_LINER = ("firebrick-medium-duty-smithfield", 0.63)  # (material, in)
FLUE_LINER_NOTE = (
    "the chimney's walls clay flue liners (clay-flue-liners.md): a fireclay body, the library's "
    "Smithfield brick, 0.63 in thick (Rumford's 36 lb per 2 ft of standard 8½ × 8½ in flue at "
    "its 2,086 kg/m³: Derived), standing in the room's still air"
)


def flue_liner() -> tuple[object, ...]:
    """A chimney of clay flue liners, as the design's layers (`FLUE_LINER`)."""
    from kilndesigner.model import Layer as DesignLayer
    from kilndesigner.units import Q_

    return (DesignLayer(material=FLUE_LINER[0], thickness=Q_(FLUE_LINER[1], "in")),)


def _layers(
    kiln: Kiln, built: str, door: str | None, chimney: Sequence[object] | None = None
) -> tuple[Layer, ...]:
    """The layers a surface's wall is built of: the lining's face, the walls between chambers
    (`common_wall.between_layers`), a firebox's own lining, the chimney's own walls where given
    (a design's `Layer`s, hot face first: clay flue liners, `FLUE_LINER`), else the engine's (one
    4½ in layer of hard brick, `hardware.CHIMNEY_BRICK`)."""
    from kilndesigner.model import Layer as DesignLayer
    from kilndesigner.units import Q_

    if built == "between":
        from kilndesigner.common_wall import between_layers

        return tuple(_layer(DesignLayer(material=m, thickness=Q_(t, "mm")))
                     for m, t in between_layers(kiln))  # fmt: skip
    if built == "firebox":
        fire = kiln.heat.fire
        own = next((b.lining for b in fire.fireboxes if b.lining), None) if fire else None
        return tuple(_layer(x) for x in (own or kiln.lining.walls))
    if built == "chimney":
        from kilndesigner.hardware import CHIMNEY_BRICK

        if chimney:
            return tuple(_layer(x) for x in chimney)
        return (_layer(DesignLayer(material=CHIMNEY_BRICK, thickness=Q_(4.5, "in"))),)
    face = "walls" if built == "walls" else built
    return tuple(_layer(x) for x in kiln.lining.for_face(face, door_face=door))  # pyright: ignore[reportArgumentType]


def _grey(
    prod: gas.Products, wsgg: Literal["bordbar2014", "dorigon2013", "transparent"]
) -> tuple[gasrad.WSGG | None, float, float]:
    if prod.fuel is gas.ELECTRIC:  # air: no CO₂ or H₂O to radiate
        return None, 0.0, math.nan
    pwc, mr = prod.radiating(NOMINAL)
    if wsgg == "bordbar2014":
        return gasrad.bordbar2014(min(max(mr, 0.01), 4.0)), pwc, mr
    if wsgg == "dorigon2013":
        return gasrad.dorigon2013(mr), pwc, mr
    return None, pwc, mr


def heat_model(
    kiln: Kiln,
    load: Load | Sequence[Load],
    air_ratio: float,
    wood: Wood | gas.Fuel | None = None,
    wsgg: Literal["bordbar2014", "dorigon2013", "transparent"] = "bordbar2014",
    n_rays: int = 100_000,
    seed: int = 20261110,
    grate_bar: float | None = None,
    ground_soil: Soil = DRY,
    path: bool = False,
    segments: int = 1,
    intake: dr.Intakes | None = None,
    bed_rate: float | None = None,
    emissivity: Emissivity = "nominal",
    chimney: Sequence[object] | None = None,
    path_inputs: object = None,
    wire: tuple[float, float, int] | None = None,
) -> ZoneModel:
    """The kiln's zone model at an air ratio λ, with its load (one per chamber zone, front to
    back). With ``path`` the fireboxes and the chimney are gas zones of their own, with their own
    brick (H13): the fuel burns in the firebox, the floor over it a wall between the two zones,
    the chimney's walls taking heat from the leaving gas; without, the one chamber is the zone the
    fire burns in, as built first. A floor on the ground (``chamber.on_ground`` or a foundation,
    as v1 reads it) loses into the soil (`ground.py`). ``intake``: the fireboxes' air intakes for
    the draft (`draft.Intakes`); ``bed_rate``: a coal bed's burning rate on its grates (kg/(m²·s)
    as fired, `air.COAL_BED`), the most the stoker can burn; ``emissivity``: the class's band end
    (`EMISSIVITY_CLASS`); ``chimney``: the chimney's own walls, hot face first, where the book says
    how it is built (`flue_liner()` for clay flue liners; the design file can't say);
    ``path_inputs``: what else the draft path needs that the design file can't say, the
    dataset's (`paths.Inputs`); ``wire``: an electric kiln's element wire (diameter m, length m
    of each, the count), for its surface load, where the book prints it.

    Every chamber shape `chamber.py` traces is taken: a round chamber's or a crossing's walls grow
    to their outsides as the engine's own shape grows them (`shape.chamber_shape`). An electric
    kiln's elements are face sources on the walls they line (`elements_of`), its gas still air."""
    fuel = fuel_of(kiln, wood)
    t_room = si(kiln.site.ambient, "K")
    electric = fuel is gas.ELECTRIC
    prod = gas.still_air(t_room) if electric else gas.products(fuel, air_ratio, t_room)
    if electric:
        wsgg = "transparent"
    c = ch.chamber(kiln, segments=segments, path=path)
    loads = [load] if isinstance(load, Load) else list(load)
    kinds = [g.kind for g in c.gas]
    rooms = [k for k, g in enumerate(c.gas) if g.kind == "chamber"]
    if len(loads) != len(rooms):
        raise NotModelledError(
            f"one load for each chamber zone: {len(rooms)} zones, {len(loads)} loads"
        )
    settings, boxes = _settings(c, loads, rooms)
    many = len(c.gas) > 1
    grey, pwc, mr = _grey(prod, wsgg)
    ks = gasrad.grey_ks(grey, pwc)
    vol = c.volume - sum(rays.box_volume(x.lo, x.hi) for x in loads)
    traced = rays.trace(
        [*c.zones, *boxes], c.patches, rays=n_rays, seed=seed, volume=vol,
        regions=c.regions() if many else (), gas=[g.name for g in c.gas] if many else (), ks=ks,
    )  # fmt: skip
    exchange: gasrad.GasExchange | gasrad.ZonesExchange = (
        gasrad.exchange_zones(traced, grey, pwc) if many else gasrad.exchange_for(traced, grey, pwc)
    )
    faces, soil, notes = _faces(kiln, c, traced, ground_soil, path, t_room, emissivity, chimney)
    notes = [*c.notes, *notes, *_class_notes(faces)]
    if chimney and any(g.kind == "chimney" for g in c.gas):
        liner = tuple(chimney) == flue_liner()
        notes.append(FLUE_LINER_NOTE if liner else "the chimney's walls: given")
    fire_zone = kinds.index("firebox") if "firebox" in kinds else rooms[0]
    openings = _openings(c, rooms[0])
    gases = _gases(kiln, c, loads, rooms)
    table, draft_path = None, None
    try:
        draft_path = dr.kiln_path(kiln, grate_bar=grate_bar, intake=intake, inputs=path_inputs,
                                  segments=segments)  # fmt: skip
        table = dr.table(draft_path, prod, fuel=rated_fuel(kiln, fuel))
    except dr.NotModelledError as e:
        notes.append(f"the draft isn't worked out: {e}")
    bed = _bed(kiln, fuel, bed_rate, notes)
    elements = elements_of(kiln, faces, dict(zip(traced.names, traced.areas, strict=True)), wire,
                           c.shape) if electric else None  # fmt: skip
    path_zones = tuple((g.name, k) for k, g in enumerate(c.gas)) if many else ()
    steps = (
        *prod.steps,
        *traced.steps,
        Step(
            name="Gas radiation",
            value=f"{grey.name if grey is not None else 'a transparent gas'}; p_H2O + p_CO2 "
            f"{pwc:.3f} atm, MR {mr:.2f}, the products at {NOMINAL - 273.15:.0f} °C",
            reference=grey.reference if grey is not None else None,
            note=(grey.note or None) if grey is not None else "gas radiation left out by request",
        ),
        Step(
            name="The walls",
            value="; ".join(f"{f.name}" + (f" | {f.back}" if f.back else "") + ": "
                            + " + ".join(f"{x.thickness * 1e3:.0f} mm {x.name}"
                                         for x in f.wall.layers) for f in faces),
            inputs={f.name: f.emissivity.reference for f in faces[:1]}
            | {"the emissivity class": f"{emissivity}: {EMISSIVITY_CLASS[emissivity][0]}, × "
               f"{EMISSIVITY_CLASS[emissivity][1]:.2f} hemispherical"},
            note="hot-face emissivity lines extrapolated past their measured range (the user's "
            "decision, radiation-exchange.md §5.5); a wall between two zones (|) has a face in "
            "each",
        ),
        Step(
            name="The setting",
            value="; ".join(f"{x.mass:.0f} kg, ε {x.emissivity:.2f}, in "
                            f"{np.round(x.lo, 3).tolist()}–{np.round(x.hi, 3).tolist()} m"
                            for x in loads),
            reference=src.FIRED_CLAY_CP.reference,
            note=loads[0].reference,
        ),
        Step(name="The gas zones", value=", ".join(f"{g.name} {g.volume * 1e3:.0f} L"
                                                   for g in c.gas),
             note=f"the fuel burns in the {c.gas[fire_zone].name}" if many else None),
        Step(
            name="Convection inside",
            value=CONVECTION,
            inputs={"the setting's passages": ", ".join(f"{x.gap * 1e3:.0f} mm" for x in loads)},
            reference="Lienhard, A Heat Transfer Textbook 6th ed. (2024) eqs. 7.41, 8.13b, Table "
            "7.4; ht 1.2",
            note=f"{CONVECTION_NOTE}; {src.SETTING_GAP_NOTE}",
        ),
        *(table.steps if table is not None else ()),
        *((_elements_working(elements, faces),) if elements is not None else ()),
        Step(name="Said about the model", value="; ".join(notes) if notes else "nothing"),
    )  # fmt: skip
    return ZoneModel(
        prod, exchange, traced.names, tuple(faces), tuple(settings), tuple(openings), gases,
        t_room, table, steps, soil, draft_path, path_zones, fire_zone, bed, elements,
    )  # fmt: skip


def elements_of(
    kiln: Kiln,
    faces: Sequence[Face],
    areas: dict[str, float],
    wire: tuple[float, float, int] | None,
    shape: str = "box",
) -> Elements:
    """The design's elements as face sources: the walls they line (a round chamber's one wall),
    each its share of the power by area; the power the design gives, else the circuit's
    continuous limit, 80 % of the breaker (v1's electric.CONTINUOUS_FRACTION, NEC 210.20(A)); at
    the firing's top temperature (its cone at its final rate), Kanthal's Ct (the library's
    alloy)."""
    from kilndesigner.cones import cone_temperature
    from kilndesigner.electric import CONTINUOUS_FRACTION
    from kilndesigner.library import alloy

    el = kiln.heat.electric
    assert el is not None
    walls = {"wall"} if shape == "round" else set(el.walls)
    lined = [k for k, f in enumerate(faces) if f.name.split(" ")[0] in walls]
    if not lined:
        raise NotModelledError(f"the elements' walls {sorted(walls)} aren't among the faces traced")
    total = sum(areas[faces[k].name] for k in lined)
    shares = tuple((k, areas[faces[k].name] / total) for k in lined)
    supply = el.supply
    volts, phases = si(supply.voltage, "V"), supply.phase
    if el.power is not None:
        power = si(el.power, "W")
    else:
        power = (3**0.5 if phases == 3 else 1.0) * volts * CONTINUOUS_FRACTION * si(
            supply.breaker, "A")  # fmt: skip
    f = kiln.firing
    top = (si(f.top_temperature, "K") if f.top_temperature is not None
           else si(cone_temperature(str(f.cone), f.final_rate), "K"))  # fmt: skip
    a = alloy(el.alloy)
    ct = tuple((t + 273.15, c) for t, c in a.ct)
    return Elements(shares, power, top, ct, volts, phases, wire,
                    f"{a.name}: {a.source}; the power the design's")  # fmt: skip


def _elements_working(el: Elements, faces: Sequence[Face]) -> Step:
    load = el.surface_load
    return Step(
        name="The elements",
        value=", ".join(f"{faces[k].name} {share:.0%}" for k, share in el.faces)
        + f" of {el.power / 1e3:.2f} kW",
        formula="P(T) = P_design·Ct(T_design)/Ct(T); I = P/V (√3·V on three phases); surface "
        "load P/(n·π·d·L)",
        inputs={
            "supply": f"{el.voltage:.0f} V, {el.phases} phase, {el.current:.1f} A",
            "cold": f"{el.most(293.15) / 1e3:.2f} kW",
            "surface load": f"{load * 0.0254**2:.2f} W/in²" if load is not None else "no wire",
        },
        reference=el.reference,
        note=ELEMENTS_NOTE,
    )


def _bed(kiln: Kiln, fuel: gas.Fuel, rate: float | None, notes: list[str]) -> float | None:
    """The most dry fuel the grates burn (kg/s): a coal bed's rate on the grates' area; wood's
    has no source (the draft's air alone)."""
    fire = kiln.heat.fire
    if fire is None or fuel.kind == "gas":
        return None
    if fuel.kind == "wood":
        notes.append(air_mod.WOOD_BED_NOTE)
        return None
    if rate is None:
        notes.append(f"{fuel.kind}: the bed's burning rate not given, the draft's air alone")
        return None
    area = sum(si(b.grate.width, "m") * si(b.grate.length, "m") * b.count
               for b in fire.fireboxes if b.grate is not None)  # fmt: skip
    if area <= 0:
        notes.append("no grate given: the bed's rate has no area to act on, the air alone")
        return None
    most = air_mod.bed_most(fuel, area, rate)
    notes.append(f"the grates, {area:.2f} m², burn at most {rate * 3600:.0f} kg/(m²·h) as fired "
                 f"({air_mod.COAL_BED_REFERENCE})")  # fmt: skip
    return most


def _settings(
    c: ch.Chamber, loads: list[Load], rooms: list[int]
) -> tuple[list[Setting], list[rays.Zone]]:
    """Each load in its chamber zone's room, under its springline, as a setting and its box."""
    settings: list[Setting] = []
    boxes: list[rays.Zone] = []
    whole = ch.Room((-c.width / 2, -c.depth / 2, 0.0), (c.width / 2, c.depth / 2, c.height), 0.0)
    for j, (x, k) in enumerate(zip(loads, rooms, strict=True)):
        room = c.rooms[j] if c.rooms else whole
        lo, hi = np.asarray(x.lo), np.asarray(x.hi)
        # in the chamber's own gas (an arch's or a dome's included), over its own room
        fits = c.holds(x.lo, x.hi) and room.lo[1] <= (lo[1] + hi[1]) / 2 <= room.hi[1]
        if not (np.all(hi > lo) and fits):
            raise NotModelledError(
                "the setting's envelope must lie inside its chamber, in its gas (a box's corners, "
                "edges and faces inside the traced solid)"
            )
        name = "setting" if len(loads) == 1 else f"setting {j + 1}"
        boxes.append(rays.box_zone(name, x.lo, x.hi))
        settings.append(Setting(x.mass, x.emissivity, x.lo, x.hi, fired_clay(), x.reference,
                                name, k, x.gap))  # fmt: skip
    return settings, boxes


def _faces(
    kiln: Kiln,
    c: ch.Chamber,
    traced: rays.Rays,
    ground_soil: Soil,
    path: bool,
    t_room: float,
    cls: Emissivity = "nominal",
    chimney: Sequence[object] | None = None,
) -> tuple[list[Face], Ground | None, list[str]]:
    """The walls behind the surfaces: each its layers, its area growing to its outside, and what
    its outer face loses to; the floor over fireboxes that are zones a wall between the two."""
    roof = kiln.roof
    rise = si(roof.rise, "m") if isinstance(roof, SprungArch | Dome) else 0.0
    door = kiln.loading.face if kiln.loading.type in ("door", "car") else None
    shell = src.SHELL_EMISSIVITY[kiln.shell.finish]
    fire = kiln.heat.fire
    under = fire is not None and any(b.position == "under" for b in fire.fireboxes)
    on_ground = (kiln.chamber.on_ground or kiln.chamber.foundation is not None) and not under
    zoned = "firebox roof" in traced.names
    faces: list[Face] = []
    notes: list[str] = []
    soil: Ground | None = None
    area = {n: float(a) for n, a in zip(traced.names, traced.areas, strict=True)}
    rooms = [k for k, g in enumerate(c.gas) if g.kind == "chamber"]
    if len(rooms) > 1 and on_ground:
        on_ground = False
        notes.append("the chambers' floors on the ground: one ground a model so far, so their "
                     "undersides are taken as adiabatic (the soil stores and loses little "
                     "over a firing behind a thick floor, 11-09-26.md §I step 7)")  # fmt: skip
    shaped = _shaped_faces(kiln) if c.shape != "box" else {}
    if shaped:
        notes.append(SHAPED_NOTE)
    for name in traced.names:
        if name not in c.built or (name == "firebox roof" and under):  # the floor's underside
            continue
        built, zone = c.built[name]
        face, _, tag = name.rpartition(" ")
        if not tag.isdigit():
            face, tag = name, ""
        if built in ("grate", "open") or (built == "between" and face == "front"):
            continue  # an opening, or the back of a wall between chambers
        layers = _layers(kiln, built, door, chimney)
        t = sum(x.thickness for x in layers)
        a_in = area[name]
        back, back_zone, back_line = "", 0, None
        if face in shaped:
            a_out = a_in * _grows(shaped[face], t)
        elif face in WALL_FACES:
            room = c.rooms[rooms.index(zone)] if c.rooms and zone in rooms else None
            w, d, h = ((room.hi[0] - room.lo[0], room.hi[1] - room.lo[1], room.hi[2] - room.lo[2])
                       if room else (c.width, c.depth, c.height))  # fmt: skip
            sides = face_sides(face, w, d, h, rise)
            if min(sides) <= 0:  # no wall under an arch from the floor: the face's own rectangle
                sides = _own_sides(c, name)
            a_out = grown(a_in, sides, t)
        else:
            a_out = a_in * _duct_growth(kiln, c, built, t)
        if built == "between" and face == "back":
            back = f"front {int(tag) + 1}"
            back_zone = c.built[back][1]
            a_out = area[back]
            back_line = _emissivity(layers[-1].name, cls)
            outside = Outside("adiabatic", None, t_room)
        elif built == "between":
            outside = Outside("adiabatic", None, t_room)  # the flue holes' sides, in that wall
        elif face == "floor" and under and zoned:
            back, back_zone = "firebox roof", c.built["firebox roof"][1]
            a_out = area["firebox roof"]
            back_line = _emissivity(layers[-1].name, cls)
            outside = Outside("adiabatic", None, t_room)
        elif face == "floor" and under:
            outside = Outside("adiabatic", None, t_room)
            notes.append(
                "the floor over the fireboxes: its underside adiabatic (the fireboxes aren't "
                "zones in this model)"
            )
        elif face == "floor" and on_ground:
            outside = Outside("ground", None, t_room)
            # the far sides 8 m off (step 7), or four of the disc's radii under a bigger floor
            # (La Borne's, 27 × 11 ft), as far as the mesh's own rule asks
            soil = ground(a_out, ground_soil, max(8.0, 4.0 * math.sqrt(a_out / math.pi)))
            notes.append(
                f"the floor on the ground: {soil.soil.reference}, the floor as the disc of its "
                f"{a_out:.2f} m² ({soil.nodes} nodes), the soil round it adiabatic, the far sides "
                "at the room's temperature"
            )
        elif name in ("inlet flues", "exit flue"):
            outside = Outside("adiabatic", None, t_room)
            notes.append(f"the {name}' sides: their brick's far side adiabatic (a channel "
                         "through a wall stores heat, its loss is the wall's)")  # fmt: skip
        elif face in shaped:
            f0 = shaped[face][0]
            surface = StillAirSurface(f0.orientation, f0.characteristic_length(t), shell)
            outside = Outside("air", surface, t_room)
        else:
            outside = Outside("air", _surface(kiln, c, face, built, t, shell, rise), t_room)
        wall = CellWall(name, layers, linear_area(a_in, a_out, t), outside)
        faces.append(Face(name, wall, _emissivity(layers[0].name, cls), zone, back, back_zone,
                          back_line))  # fmt: skip
    return faces, soil, notes


SHAPED_NOTE = (
    "the walls' outside areas and outer surfaces from the engine's own chamber shape "
    "(shape.chamber_shape, v1's heat loss): a round chamber's wall and floor as the outline moved "
    "out by each face's thickness, its dome the sphere moved out over the wall's outside circle; "
    "a crossing's walls, floor and vaults as crossing.crossing_faces grows them"
)


def _shaped_faces(kiln: Kiln) -> dict[str, list[FaceShape]]:
    """A round or crossing chamber's faces as the engine's shape grows them through the lining
    (`shape.chamber_shape`), keyed by v2's names: a round chamber's wall is v1's four quarters,
    its roof the dome's cap or the flat lid; a crossing's names are the same in both."""
    from kilndesigner.shape import chamber_shape

    shape = chamber_shape(kiln)
    out: dict[str, list[FaceShape]] = {}
    for f in shape.faces():
        name = "wall" if shape.round and f.face in ("left", "right", "back", "front") else f.face
        out.setdefault(name, []).append(f)
    return out


def _own_sides(c: ch.Chamber, name: str) -> tuple[float, float]:
    """A traced face's own bounding rectangle in its plane (m): its extent along the two axes it
    lies across (the steps of a tapering arch from the floor, Ellington's, have no room's wall
    height to take)."""
    tris = next(z.triangles for z in c.zones if z.name == name).reshape(-1, 3)
    span = tris.max(axis=0) - tris.min(axis=0)
    a, b = sorted(span)[1:]
    return float(a), float(b)


def _grows(faces: list[FaceShape], t: float) -> float:
    """A face's outside area over its inside area, ``t`` (m) out through its lining."""
    return sum(f.area_at(t) for f in faces) / sum(f.inside_area for f in faces)


def _duct_growth(kiln: Kiln, c: ch.Chamber, built: str, t: float) -> float:
    """A firebox's or a chimney's walls round their box: the outside perimeter over the inside's
    (Derived: each wall's outside grows by the thickness on each edge, as a box chamber's)."""
    if built == "chimney" and kiln.draft is not None and kiln.draft.chimney is not None:
        inside = kiln.draft.chimney.inside
        assert inside is not None  # the chimney zone is built only from its given section
        across = inside.width if inside.width is not None else inside.diameter
        along = inside.depth if inside.depth is not None else inside.diameter
        assert across is not None
        assert along is not None
        a, b = si(across, "m"), si(along, "m")
        return (a + b + 4 * t) / (a + b)  # a round one's circumference grows as (d + 2t)/d
    fire = kiln.heat.fire
    if built == "firebox" and fire is not None:
        fb = fire.fireboxes[0]
        a, b = si(fb.width, "m"), si(fb.length, "m")
        return (a + b + 4 * t) / (a + b)
    return 1.0


def _surface(
    kiln: Kiln, c: ch.Chamber, face: str, built: str, t: float, shell: float, rise: float
) -> StillAirSurface:
    """The still air outside a wall: v1's surfaces at the wall's own size."""
    if built == "chimney" and kiln.draft is not None and kiln.draft.chimney is not None:
        return StillAirSurface("vertical", si(kiln.draft.chimney.height, "m"), shell)
    if built == "firebox":
        fire = kiln.heat.fire
        assert fire is not None
        fb = fire.fireboxes[0]
        tall = si(fb.height, "m") if fb.height is not None else si(fb.width, "m")
        return StillAirSurface("vertical", tall, shell)
    sides = face_sides(face, c.width, c.depth, c.height, rise)
    o = sides[0] + 2 * t, sides[1] + 2 * t
    if face == "roof":
        return StillAirSurface("facing_up", o[0] * o[1] / (2 * (o[0] + o[1])), shell)
    if face == "floor":
        return StillAirSurface("facing_down", min(o) / 2, shell)
    return StillAirSurface("vertical", o[1], shell)


def _openings(c: ch.Chamber, first: int) -> list[Opening]:
    """The openings: the patches carved from the faces, and the zones' own: a grate (the fire),
    the chimney's top and an open top (the room)."""
    out: list[Opening] = []
    for p in c.patches:
        if p.name.startswith("exit flue"):
            out.append(Opening(p.name, "flue", p.face))
        elif p.name.startswith(("inlet flue", "burner port")):
            out.append(Opening(p.name, "flame", zone=first))
        else:
            out.append(Opening(p.name, "room"))
    for z in c.zones:
        built, zone = c.built[z.name]
        if built == "grate":
            out.append(Opening(z.name, "flame", zone=zone))
        elif built == "open":
            out.append(Opening(z.name, "room"))
    return out


def _gases(kiln: Kiln, c: ch.Chamber, loads: list[Load], rooms: list[int]) -> tuple[Gas, ...]:
    """Each zone's convection's flow, as a duct: across a chamber (cross-draft: its width ×
    height, along the setting's length; else its plan, down the setting's height), along a
    firebox's channels, up the chimney; each section's hydraulic diameter, 2ab/(a + b)."""
    across = kiln.draft is not None and kiln.draft.type == "cross"
    out: list[Gas] = []
    for k, g in enumerate(c.gas):
        if g.kind == "chamber":
            j = rooms.index(k)
            x = loads[j]
            room = c.rooms[j] if c.rooms else None
            w = room.hi[0] - room.lo[0] if room else c.width
            d = room.hi[1] - room.lo[1] if room else c.depth
            h = room.hi[2] - room.lo[2] if room else c.height
            if c.shape == "round":  # up or down a cylinder, its plan a disc
                out.append(Gas(g.name, Flow(math.pi * w * w / 4, x.hi[2] - x.lo[2], w, h)))
            elif c.shape == "crossing":  # up the crossing's plan, the two tubes' union
                from kilndesigner.crossing import crossing_shape

                cs = crossing_shape(kiln)
                plan = cs.floor()
                out.append(Gas(g.name, Flow(plan, x.hi[2] - x.lo[2], 4 * plan / cs.perimeter(),
                                            h)))  # fmt: skip
            elif across:
                out.append(Gas(g.name, Flow(w * h, x.hi[1] - x.lo[1], hydraulic(w, h), h)))
            else:
                out.append(Gas(g.name, Flow(w * d, x.hi[2] - x.lo[2], hydraulic(w, d), h)))
        elif g.kind == "firebox":
            fire = kiln.heat.fire
            assert fire is not None
            fb = fire.fireboxes[0]
            fw, fl = si(fb.width, "m"), si(fb.length, "m")
            fh = si(fb.height, "m") if fb.height is not None else fw
            n = sum(b.count for b in fire.fireboxes)
            out.append(Gas(g.name, Flow(fw * fh * n, fl, hydraulic(fw, fh), fh)))
        else:
            assert kiln.draft is not None
            assert kiln.draft.chimney is not None
            inside = kiln.draft.chimney.inside
            assert inside is not None
            tall = si(kiln.draft.chimney.height, "m")
            if inside.diameter is not None:
                dia = si(inside.diameter, "m")
                out.append(Gas(g.name, Flow(math.pi * dia * dia / 4, tall, dia, tall)))
                continue
            assert inside.width is not None
            assert inside.depth is not None
            a, b = si(inside.width, "m"), si(inside.depth, "m")
            out.append(Gas(g.name, Flow(a * b, tall, hydraulic(a, b), tall)))
    return tuple(out)


def hydraulic(a: float, b: float) -> float:
    """A rectangle's hydraulic diameter, 4A/P (Lienhard §7.5)."""
    return 2 * a * b / (a + b)
