"""A kiln's heat model from its design file: the fuel, the chamber the engine draws and its
openings, the rays through it with the setting in the way, the gas's grey gases, the walls from
the lining, and the draft (ADR 0017 H1–H13).

The load is required (ADR 0017 decision 11): no heat result without one. The design file says
what it can of it (`firing.ware`, `firing.setting`); the setting's envelope and emissivity it
doesn't, so they are the caller's, stated (`Load.reference`).
"""

from __future__ import annotations

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


def heat_model(
    kiln: Kiln,
    load: Load,
    air_ratio: float,
    wood: Wood | None = None,
    wsgg: Literal["bordbar2014", "dorigon2013", "transparent"] = "bordbar2014",
    n_rays: int = 100_000,
    seed: int = 20261110,
    grate_bar: float | None = None,
    ground_soil: Soil = DRY,
) -> ZoneModel:
    """The kiln's zone model at an air ratio λ, with its load. A floor on the ground (the design's
    ``chamber.on_ground`` or a foundation, as v1 reads it) loses into the soil (`ground.py`)."""
    fuel = fuel_of(kiln, wood)
    t_room = si(kiln.site.ambient, "K")
    prod = gas.products(fuel, air_ratio, t_room)
    c = ch.chamber(kiln)
    roof = kiln.roof
    rise = si(roof.rise, "m") if isinstance(roof, SprungArch | Dome) else 0.0
    lo, hi = np.asarray(load.lo), np.asarray(load.hi)
    inside = np.array([c.width / 2, c.depth / 2, c.height])
    fits = np.all(hi > lo) and np.all(lo >= [-inside[0], -inside[1], 0.0])
    if not (fits and np.all(hi <= inside)):
        raise NotModelledError(
            "the setting's envelope must lie inside the chamber, under its springline"
        )
    box = rays.box_zone("setting", load.lo, load.hi)
    vol = c.volume - rays.box_volume(load.lo, load.hi)
    traced = rays.trace([*c.zones, box], c.patches, rays=n_rays, seed=seed, volume=vol)
    pwc, mr = prod.radiating(NOMINAL)
    grey = None
    if wsgg == "bordbar2014":
        grey = gasrad.bordbar2014(min(max(mr, 0.01), 4.0))
    elif wsgg == "dorigon2013":
        grey = gasrad.dorigon2013(mr)
    exchange = gasrad.exchange_for(traced, grey, pwc)
    door = kiln.loading.face if kiln.loading.type in ("door", "car") else None
    shell = src.SHELL_EMISSIVITY[kiln.shell.finish]
    fire = kiln.heat.fire
    under = fire is not None and any(b.position == "under" for b in fire.fireboxes)
    on_ground = (kiln.chamber.on_ground or kiln.chamber.foundation is not None) and not under
    faces: list[Face] = []
    notes: list[str] = list(c.notes)
    soil: Ground | None = None
    for name in traced.names:
        if name not in WALL_FACES:
            continue
        layers = tuple(_layer(x) for x in kiln.lining.for_face(name, door_face=door))  # pyright: ignore[reportArgumentType]
        t = sum(x.thickness for x in layers)
        a_in = float(traced.areas[traced.index(name)])
        sides = face_sides(name, c.width, c.depth, c.height, rise)
        a_out = grown(a_in, sides, t)
        if name == "floor" and under:
            outside = Outside("adiabatic", None, t_room)
            notes.append(
                "the floor over the fireboxes: its underside adiabatic (the fireboxes aren't "
                "zones yet)"
            )
        elif name == "floor" and on_ground:
            outside = Outside("ground", None, t_room)
            soil = ground(a_out, ground_soil)
            notes.append(
                f"the floor on the ground: {soil.soil.reference}, the floor as the disc of its "
                f"{a_out:.2f} m² ({soil.nodes} nodes), the soil round it adiabatic, the far sides "
                "at the room's temperature"
            )
        else:
            o = sides[0] + 2 * t, sides[1] + 2 * t
            if name == "roof":
                surf = StillAirSurface("facing_up", o[0] * o[1] / (2 * (o[0] + o[1])), shell)
            elif name == "floor":
                surf = StillAirSurface("facing_down", min(o) / 2, shell)
            else:
                surf = StillAirSurface("vertical", o[1], shell)
            outside = Outside("air", surf, t_room)
        wall = CellWall(name, layers, linear_area(a_in, a_out, t), outside)
        faces.append(Face(name, wall, line(_emissivity(layers[0].name))))
    openings: list[Opening] = []
    for p in c.patches:
        if p.name == "exit flue":
            assert kiln.draft is not None
            openings.append(Opening(p.name, "flue", kiln.draft.flue_wall))
        elif p.name.startswith(("inlet flue", "burner port")):
            openings.append(Opening(p.name, "flame"))
        else:
            openings.append(Opening(p.name, "room"))
    setting = Setting(load.mass, load.emissivity, load.lo, load.hi, fired_clay(), load.reference)
    across = kiln.draft is not None and kiln.draft.type == "cross"
    if across:
        flow = Flow(c.width * c.height, float(hi[1] - lo[1]))
    else:
        flow = Flow(c.width * c.depth, float(hi[2] - lo[2]))
    table = None
    try:
        path = dr.kiln_path(kiln, grate_bar=grate_bar)
        table = dr.table(path, prod, fuel=rated_fuel(kiln, fuel))
    except dr.NotModelledError as e:
        notes.append(f"the draft isn't worked out: {e}")
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
            value="; ".join(f"{f.name}: " + " + ".join(f"{x.thickness * 1e3:.0f} mm {x.name}"
                                                        for x in f.wall.layers) for f in faces),
            inputs={f.name: f.emissivity.reference for f in faces[:1]},
            note="hot-face emissivity lines extrapolated past their measured range (the user's "
            "decision, radiation-exchange.md §5.5)",
        ),
        Step(
            name="The setting",
            value=f"{load.mass:.0f} kg, ε {load.emissivity:.2f}, in "
            f"{np.round(lo, 3).tolist()}–{np.round(hi, 3).tolist()} m",
            reference=src.FIRED_CLAY_CP.reference,
            note=load.reference,
        ),
        Step(name="Convection inside", value="the laminar flat plate", note=CONVECTION_NOTE),
        *(table.steps if table is not None else ()),
        Step(name="Said about the model", value="; ".join(notes) if notes else "nothing"),
    )  # fmt: skip
    return ZoneModel(
        prod, exchange, traced.names, tuple(faces), setting, tuple(openings), flow, t_room,
        table, steps, soil,
    )  # fmt: skip
