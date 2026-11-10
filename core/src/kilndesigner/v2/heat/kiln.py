"""A kiln's heat model from its design file: the fuel, the chamber the engine draws and its
openings, the rays through it with the setting in the way, the gas's grey gases, the walls from
the lining, and the draft (ADR 0017 H1–H13).

The load is required (ADR 0017 decision 11): no heat result without one. The design file says
what it can of it (`firing.ware`, `firing.setting`); the setting's envelope and emissivity it
doesn't, so they are the caller's, stated (`Load.reference`).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

import numpy as np

from kilndesigner.library import material
from kilndesigner.model import Dome, Kiln, SprungArch
from kilndesigner.thermal.surface import StillAirSurface
from kilndesigner.thermal.transient import HeatCapacity, Layer
from kilndesigner.units import si
from kilndesigner.v2.heat import chamber as ch
from kilndesigner.v2.heat import draft as dr
from kilndesigner.v2.heat import gas, gasrad, rays
from kilndesigner.v2.heat import sources as src
from kilndesigner.v2.heat.ground import DRY, Ground, Soil, ground
from kilndesigner.v2.heat.walls import CellWall, Outside, face_sides, grown, linear_area
from kilndesigner.v2.heat.zone import (
    CONVECTION_NOTE,
    Face,
    Flow,
    Gas,
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
    emissivity, with where each comes from."""

    mass: float
    lo: tuple[float, float, float]
    hi: tuple[float, float, float]
    emissivity: float
    reference: str


@dataclass(frozen=True)
class Wood:
    """Wood as fired: wet-basis moisture and net heating value per oven-dry kg (J/kg)."""

    moisture: float
    net_dry: float
    reference: str


def fuel_of(kiln: Kiln, wood: Wood | None) -> gas.Fuel:
    heat = kiln.heat
    if heat.electric is not None and heat.gas is None and heat.fire is None:
        raise NotModelledError("elements as face sources are build order step 10, not built yet")
    if heat.gas is not None and heat.fire is None:
        f = heat.gas.fuel
        return gas.propane() if f == "propane" else gas.natural_gas()
    if heat.fire is not None and heat.gas is None:
        if heat.fire.fuel != "wood":
            raise NotModelledError(
                f"{heat.fire.fuel}: no composition or heating value is sourced (problem set §7)"
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
    if m.specific_heat is None:
        if x.specific_heat is None:
            raise NotModelledError(f"{x.material}: no specific heat sourced or given")
        cp = HeatCapacity.constant(si(x.specific_heat, "J/(kg*K)"))
    else:
        ts, cs = m.specific_heat.to_points()
        if m.kind == "dense_firebrick" and ts[0] > src.FIRED_CLAY_AT:
            ts, cs = (src.FIRED_CLAY_AT, *ts), (src.FIRED_CLAY_CP.value, *cs)
        cp = HeatCapacity(tuple(ts), tuple(cs))
    return Layer(x.material, si(x.thickness, "m"), m.k, rho, cp)


def _emissivity(material_id: str) -> str:
    kind = material(material_id).kind
    if kind == "insulating_firebrick":
        return "ifb-mpk125"
    if kind == "dense_firebrick":
        return "dense-medium"
    raise NotModelledError(f"{material_id}: no hot-face emissivity sourced for {kind}")


def _layers(kiln: Kiln, built: str, door: str | None) -> tuple[Layer, ...]:
    """The layers a surface's wall is built of: the lining's face, the walls between chambers
    (`common_wall.between_layers`), a firebox's own lining, the engine's chimney (one 4½ in layer
    of hard brick, `hardware.CHIMNEY_BRICK`)."""
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

        return (_layer(DesignLayer(material=CHIMNEY_BRICK, thickness=Q_(4.5, "in"))),)
    face = "walls" if built == "walls" else built
    return tuple(_layer(x) for x in kiln.lining.for_face(face, door_face=door))  # pyright: ignore[reportArgumentType]


def _grey(
    prod: gas.Products, wsgg: Literal["bordbar2014", "dorigon2013", "transparent"]
) -> tuple[gasrad.WSGG | None, float, float]:
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
    wood: Wood | None = None,
    wsgg: Literal["bordbar2014", "dorigon2013", "transparent"] = "bordbar2014",
    n_rays: int = 100_000,
    seed: int = 20261110,
    grate_bar: float | None = None,
    ground_soil: Soil = DRY,
    path: bool = False,
    segments: int = 1,
) -> ZoneModel:
    """The kiln's zone model at an air ratio λ, with its load (one per chamber zone, front to
    back). With ``path`` the fireboxes and the chimney are gas zones of their own, with their own
    brick (H13): the fuel burns in the firebox, the floor over it a wall between the two zones,
    the chimney's walls taking heat from the leaving gas; without, the one chamber is the zone the
    fire burns in, as built first. A floor on the ground (``chamber.on_ground`` or a foundation,
    as v1 reads it) loses into the soil (`ground.py`)."""
    fuel = fuel_of(kiln, wood)
    t_room = si(kiln.site.ambient, "K")
    prod = gas.products(fuel, air_ratio, t_room)
    c = ch.chamber(kiln, segments=segments, path=path)
    if c.shape != "box":
        raise NotModelledError(
            f"a {c.shape} chamber is traced (chamber.py) but its walls' outside areas aren't "
            "worked out yet: box chambers only"
        )
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
    faces, soil, notes = _faces(kiln, c, traced, ground_soil, path, t_room)
    notes = [*c.notes, *notes]
    fire_zone = kinds.index("firebox") if "firebox" in kinds else rooms[0]
    openings = _openings(c, rooms[0])
    gases = _gases(kiln, c, loads, rooms)
    table, draft_path = None, None
    try:
        draft_path = dr.kiln_path(kiln, grate_bar=grate_bar)
        table = dr.table(draft_path, prod, fuel=rated_fuel(kiln, fuel))
    except dr.NotModelledError as e:
        notes.append(f"the draft isn't worked out: {e}")
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
            inputs={f.name: f.emissivity.reference for f in faces[:1]},
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
        Step(name="Convection inside", value="the laminar flat plate", note=CONVECTION_NOTE),
        *(table.steps if table is not None else ()),
        Step(name="Said about the model", value="; ".join(notes) if notes else "nothing"),
    )  # fmt: skip
    return ZoneModel(
        prod, exchange, traced.names, tuple(faces), tuple(settings), tuple(openings), gases,
        t_room, table, steps, soil, draft_path, path_zones, fire_zone,
    )  # fmt: skip


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
        fits = np.all(hi > lo) and np.all(lo >= room.lo) and np.all(hi <= room.hi)
        if not fits:
            raise NotModelledError(
                "the setting's envelope must lie inside its chamber, under its springline"
            )
        name = "setting" if len(loads) == 1 else f"setting {j + 1}"
        boxes.append(rays.box_zone(name, x.lo, x.hi))
        settings.append(Setting(x.mass, x.emissivity, x.lo, x.hi, fired_clay(), x.reference,
                                name, k))  # fmt: skip
    return settings, boxes


def _faces(
    kiln: Kiln, c: ch.Chamber, traced: rays.Rays, ground_soil: Soil, path: bool, t_room: float
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
    for name in traced.names:
        if name not in c.built or name == "firebox roof":
            continue
        built, zone = c.built[name]
        face, _, tag = name.rpartition(" ")
        if not tag.isdigit():
            face, tag = name, ""
        if built in ("grate", "open") or (built == "between" and face == "front"):
            continue  # an opening, or the back of a wall between chambers
        layers = _layers(kiln, built, door)
        t = sum(x.thickness for x in layers)
        a_in = area[name]
        back, back_zone, back_line = "", 0, None
        if face in WALL_FACES:
            room = c.rooms[rooms.index(zone)] if c.rooms and zone in rooms else None
            w, d, h = ((room.hi[0] - room.lo[0], room.hi[1] - room.lo[1], room.hi[2] - room.lo[2])
                       if room else (c.width, c.depth, c.height))  # fmt: skip
            a_out = grown(a_in, face_sides(face, w, d, h, rise), t)
        else:
            a_out = a_in * _duct_growth(kiln, c, built, t)
        if built == "between" and face == "back":
            back = f"front {int(tag) + 1}"
            back_zone = c.built[back][1]
            a_out = area[back]
            back_line = line(_emissivity(layers[-1].name))
            outside = Outside("adiabatic", None, t_room)
        elif built == "between":
            outside = Outside("adiabatic", None, t_room)  # the flue holes' sides, in that wall
        elif face == "floor" and under and zoned:
            back, back_zone = "firebox roof", c.built["firebox roof"][1]
            a_out = area["firebox roof"]
            back_line = line(_emissivity(layers[-1].name))
            outside = Outside("adiabatic", None, t_room)
        elif face == "floor" and under:
            outside = Outside("adiabatic", None, t_room)
            notes.append(
                "the floor over the fireboxes: its underside adiabatic (the fireboxes aren't "
                "zones in this model)"
            )
        elif face == "floor" and on_ground:
            outside = Outside("ground", None, t_room)
            soil = ground(a_out, ground_soil)
            notes.append(
                f"the floor on the ground: {soil.soil.reference}, the floor as the disc of its "
                f"{a_out:.2f} m² ({soil.nodes} nodes), the soil round it adiabatic, the far sides "
                "at the room's temperature"
            )
        elif name in ("inlet flues", "exit flue"):
            outside = Outside("adiabatic", None, t_room)
            notes.append(f"the {name}' sides: their brick's far side adiabatic (a channel "
                         "through a wall stores heat, its loss is the wall's)")  # fmt: skip
        else:
            outside = Outside("air", _surface(kiln, c, face, built, t, shell, rise), t_room)
        wall = CellWall(name, layers, linear_area(a_in, a_out, t), outside)
        faces.append(Face(name, wall, line(_emissivity(layers[0].name)), zone, back, back_zone,
                          back_line))  # fmt: skip
    return faces, soil, notes


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
    """Each zone's convection's flow: across a chamber (cross-draft: its width × height, the
    setting's length along y; else its plan, the setting's height), along a firebox's channels,
    up the chimney as a duct."""
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
            if across:
                out.append(Gas(g.name, Flow(w * h, x.hi[1] - x.lo[1])))
            else:
                out.append(Gas(g.name, Flow(w * d, x.hi[2] - x.lo[2])))
        elif g.kind == "firebox":
            fire = kiln.heat.fire
            assert fire is not None
            fb = fire.fireboxes[0]
            fw, fl = si(fb.width, "m"), si(fb.length, "m")
            fh = si(fb.height, "m") if fb.height is not None else fw
            out.append(Gas(g.name, Flow(fw * fh * sum(b.count for b in fire.fireboxes), fl)))
        else:
            assert kiln.draft is not None
            assert kiln.draft.chimney is not None
            inside = kiln.draft.chimney.inside
            assert inside is not None
            across = inside.width if inside.width is not None else inside.diameter
            assert across is not None
            a = si(across, "m")
            b = si(inside.depth, "m") if inside.depth is not None else a
            out.append(Gas(g.name, Flow(a * b, si(kiln.draft.chimney.height, "m"),
                                        2 * a * b / (a + b))))  # fmt: skip
    return tuple(out)
