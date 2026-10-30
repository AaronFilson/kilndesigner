"""A firing, step by step: the walls heat through (finite volumes), the ware with them, and the
elements or burners supply what they can.

Each face of the chamber is a layered wall (:mod:`kilndesigner.thermal.transient`) whose hot face
is the chamber's temperature T_c. Each step of ``dt`` seconds:

1. the schedule asks for T_c* at the step's end (its ramp from where the kiln is, or its hold);
2. the heat that needs, D(T) = Σ faces' heat into the hot face + m·c·(T − T_c), is linear in T;
3. the heat that can be put in is the elements' power, or the burners' input times the available
   heat at the kiln's temperature (the flue gas leaves at it), times ``dt``;
4. T_c is T_c* if 0 ≤ D(T_c*) ≤ the heat available; the T where D is the heat available, if the
   schedule asks for more (the kiln falls behind); the T where D is zero if it asks to cool faster
   than the kiln cools by itself.

The hot face is taken at the chamber's temperature, as the steady heat loss does: no inside film,
no radiation exchange between faces, one temperature for the whole chamber and its ware.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from functools import cache
from typing import Literal

import numpy as np
from pydantic import BaseModel, ConfigDict

from kilndesigner.combustion import (
    OXIDATION_O2,
    PROPANE_HHV_BTU_PER_GAL,
    REDUCTION_AIR,
    Fuel,
    air_ratio_for_flue_oxygen,
    available_heat_fraction,
)
from kilndesigner.combustion import SOURCE as COMBUSTION_SOURCE
from kilndesigner.heatloss import EMISSIVITY, GROUND_SOURCE, SOIL_K, top_temperature
from kilndesigner.model import Kiln, Ramp
from kilndesigner.shape import chamber_shape
from kilndesigner.thermal.surface import FixedSurface, StillAirSurface, Surface
from kilndesigner.thermal.transient import HeatCapacity, Layer, StepResult, TransientWall
from kilndesigner.units import Q_, parse_quantity, si
from kilndesigner.working import Finding, Step, show

DT = 60.0  # s, one step
RECORD_EVERY = 5  # steps between the wall profiles kept for the heatmap
MAX_HOURS = 96.0  # a firing longer than this is stopped and reported
STALL_HOURS = 1.0  # power-limited with less than STALL_RISE over this long: the kiln has stalled
STALL_RISE = 1.0  # K
BTU_PER_KWH = 3412.14
REDUCTION_START_C = 900.0  # hybrid.REDUCTION_START: fire in oxidation to about 900 °C

# Ware and kiln furniture: fired clay, Lienhard Table A.2 (masonry-materials.md §1.1 [M1])
WARE_CP = 800.0  # J/(kg·K)
WARE_SOURCE = "Lienhard Table A.2, brick, fired clay, 24 °C; masonry-materials.md §1.1 [M1]"
METHOD = (
    "One-dimensional finite volumes through each face's layers, backward Euler with k(T), c_p(T) "
    "and the surface coefficient lagged a step; thermal/transient.py"
)
SCHEDULE_SOURCE = (
    "Orton's rates are the heating rate over the last 100 °C or so of the firing; "
    "electric-and-thermal.md §8 [S75]"
)

type Heat = Literal["electric", "gas"]


class SimulationError(ValueError):
    """A firing the engine can't simulate, with the reason."""


class FiringPoint(BaseModel):
    """The firing at one moment. Powers are averages over the step before it, in kW."""

    model_config = ConfigDict(frozen=True)

    time_h: float
    chamber_c: float
    setpoint_c: float
    heat_kw: float  # put into the kiln
    available_kw: float  # what the heat source could put in
    electric_kw: float  # drawn from the supply
    fuel_kw: float  # burned, at its higher heating value
    walls_kw: float  # into the walls' hot faces
    ware_kw: float
    shell_kw: float  # lost from the outside of the walls
    energy_kwh: float  # put into the kiln so far
    electricity_kwh: float
    fuel_kwh: float
    cost_usd: float | None
    hottest_shell_c: float


class FaceProfile(BaseModel):
    """Where a face's cells sit, for the Parquet file and the heatmap."""

    model_config = ConfigDict(frozen=True)

    face: str
    depths_m: list[float]
    layers: list[str]
    inside_area_m2: float
    outside_area_m2: float


class FiringResult(BaseModel):
    """The summary of one simulated firing, with its working."""

    model_config = ConfigDict(frozen=True)

    name: str
    heat: str  # "electric", "gas", or "electric then gas at …"
    switch_over_c: float | None
    reached_c: float
    target_c: float
    duration_h: float
    duration: str
    held: bool
    completed: bool
    electricity_kwh: float
    fuel_kwh: float
    propane_gallons: float | None
    energy_kwh: float
    walls_kwh: float
    ware_kwh: float
    shell_kwh: float
    cost_usd: float | None
    cost: str | None
    points: list[FiringPoint]
    faces: list[FaceProfile]
    working: list[Step]
    findings: list[Finding]


@dataclass
class FiringRun:
    """A result with the walls' temperatures through time, for the Parquet file."""

    result: FiringResult
    times_h: list[float] = field(default_factory=list[float])
    profiles: list[list[list[float]]] = field(default_factory=list[list[list[float]]])
    """profiles[record][face] = cell temperatures, °C, hot face first."""


@cache
def _fraction(t_kiln_k: int, air_ratio: float, fuel: Fuel) -> float:
    """Available heat at a whole kelvin (cached: Cantera is slow, and 1 K is well within its
    accuracy here)."""
    return available_heat_fraction(float(t_kiln_k), air_ratio, fuel=fuel)


def default_schedule(kiln: Kiln) -> tuple[list[Ramp], Step]:
    """As fast as the heat allows to 100 °C below the top, then the cone's final rate."""
    top, _ = top_temperature(kiln)
    top_c = si(top, "degC")
    rate = kiln.firing.final_rate
    ramps = [
        Ramp(to=Q_(top_c - 100, "degC")),
        Ramp(to=Q_(top_c, "degC"), rate=Q_(rate, "delta_degC/hour")),
    ]
    step = Step(
        name="Firing schedule",
        value=f"full heat to {top_c - 100:.0f} °C, then {rate} °C/h to {top_c:.0f} °C",
        note="None given in the design: the cone's final rate over the last 100 °C.",
        reference=SCHEDULE_SOURCE,
    )
    return ramps, step


def _layers(kiln: Kiln, face: str) -> list[Layer]:
    from kilndesigner.castable import resolve_material

    layers: list[Layer] = []
    missing: list[str] = []
    for x in kiln.lining.for_face(face, door_face=kiln.door_face):  # pyright: ignore[reportArgumentType]
        m = resolve_material(kiln, x.material)
        if x.specific_heat is not None:
            cap = HeatCapacity.constant(si(x.specific_heat, "J/(kg*K)"))
        elif m.specific_heat is not None:
            cap = HeatCapacity(*m.specific_heat.to_points())
        else:
            missing.append(m.name)
            continue
        rho = si(parse_quantity(m.density), "kg/m**3")
        layers.append(Layer(m.id, si(x.thickness, "m"), m.k, rho, cap))
    if missing:
        raise SimulationError(
            f"no sourced specific heat for {', '.join(sorted(set(missing)))}: give the layer's "
            "specific_heat from the maker's sheet to simulate the firing"
        )
    return layers


@dataclass
class _Face:
    name: str
    wall: TransientWall


def build_faces(kiln: Kiln) -> list[_Face]:
    t_air = si(kiln.site.ambient, "K")
    emissivity = EMISSIVITY[kiln.shell.finish]
    fire = kiln.heat.fire
    over_fire = fire is not None and any(fb.position == "under" for fb in fire.fireboxes)
    grounded = kiln.chamber.on_ground and not over_fire
    faces: list[_Face] = []
    for shape in chamber_shape(kiln).faces():
        if over_fire and shape.face == "floor":
            continue  # pragma: no cover - a fire kiln is refused before this
        layers = _layers(kiln, shape.face)
        thickness = sum(x.thickness for x in layers)
        surface: Surface
        if grounded and shape.face == "floor":
            d = math.sqrt(4 * shape.area_at(thickness) / math.pi)
            surface = FixedSurface(8 * SOIL_K / (math.pi * d))
        else:
            surface = StillAirSurface(
                shape.orientation, shape.characteristic_length(thickness), emissivity
            )
        wall = TransientWall(layers, surface, t_air, t_air, area=shape.area_at)
        faces.append(_Face(shape.face, wall))
    return faces


@dataclass(frozen=True)
class HeatSupply:
    """What the kiln has to heat with: element watts, and the burners' input in watts."""

    electric_w: float | None
    gas_w: float | None
    fuel: Fuel = "propane"
    reduction: bool = False
    switch_over_k: float | None = None  # a hybrid: elements below it, burners from it


def heat_supply(kiln: Kiln, switch_over_c: float | None = None) -> tuple[HeatSupply, list[Step]]:
    """The heat the design has, from the element and burner designs."""
    if kiln.heat.fire is not None:
        raise SimulationError("wood, coal and oil firings aren't simulated yet (plan milestone M7)")
    from kilndesigner.electric import design_elements
    from kilndesigner.gas import design_gas
    from kilndesigner.heatloss import heat_loss

    loss = heat_loss(kiln).total_watts
    steps: list[Step] = []
    electric_w = gas_w = None
    if kiln.heat.electric is not None:
        electric_w = design_elements(kiln, loss).installed_watts
        steps.append(Step(name="Element power", value=show(Q_(electric_w, "W"), "kW")))
    gas = kiln.heat.gas
    if gas is not None:
        gas_w = si(Q_(design_gas(kiln, loss).design_input_btu_hr, "BTU/hr"), "W")
        steps.append(
            Step(
                name="Burner input",
                value=f"{show(Q_(gas_w, 'W'), 'kW')} ({show(Q_(gas_w, 'W'), 'BTU/hr', 3)})",
                note="At its higher heating value; the kiln keeps the available heat of it.",
            )
        )
    switch: float | None = None
    if electric_w is not None and gas is not None:
        electric = kiln.heat.electric
        assert electric is not None
        if switch_over_c is not None:
            switch = switch_over_c + 273.15
        elif electric.off_above is not None:
            switch = si(electric.off_above, "K")
        else:
            switch = REDUCTION_START_C + 273.15
        steps.append(
            Step(
                name="Hand-over from elements to burners",
                value=show(Q_(switch, "K"), "degF" if kiln.units == "us" else "degC"),
                note=(
                    "as asked"
                    if switch_over_c is not None
                    else "the design's off_above"
                    if electric.off_above is not None
                    else "about where reduction starts (hybrid.REDUCTION_START)"
                ),
            )
        )
    return (
        HeatSupply(
            electric_w,
            gas_w,
            gas.fuel if gas is not None else "propane",
            bool(gas is not None and gas.reduction),
            switch,
        ),
        steps,
    )


def _source_at(supply: HeatSupply, t_k: float) -> Heat:
    if supply.gas_w is None:
        return "electric"
    if supply.electric_w is None:
        return "gas"
    assert supply.switch_over_k is not None
    return "electric" if t_k < supply.switch_over_k else "gas"


def _air_ratio(supply: HeatSupply, t_k: float) -> float:
    if supply.reduction and t_k >= REDUCTION_START_C + 273.15:
        return REDUCTION_AIR
    return air_ratio_for_flue_oxygen(OXIDATION_O2, supply.fuel)


@dataclass
class _Controller:
    """Walks the schedule: each ramp from where the kiln is, then its hold."""

    ramps: Sequence[Ramp]
    index: int = 0
    held_for: float = 0.0  # s into the current hold
    holding: bool = False

    @property
    def done(self) -> bool:
        return self.index >= len(self.ramps)

    def target(self, t_c: float, dt: float) -> tuple[float, bool]:
        """T_c* for the step's end, and whether the schedule sets a pace (False: full heat)."""
        ramp = self.ramps[self.index]
        to = si(ramp.to, "K")
        if self.holding:
            return to, True
        if ramp.rate is None:
            return to, False
        step = si(ramp.rate, "K/s") * dt
        return (min(t_c + step, to) if to >= t_c else max(t_c - step, to)), True

    def advance(self, t_start: float, t_c: float, dt: float) -> None:
        ramp = self.ramps[self.index]
        to = si(ramp.to, "K")
        if self.holding:
            self.held_for += dt
            if self.held_for >= si(ramp.hold, "s") - 1e-9:  # pyright: ignore[reportArgumentType]
                self.index, self.holding, self.held_for = self.index + 1, False, 0.0
            return
        heating = to >= t_start
        if (heating and t_c >= to - 1e-6) or (not heating and t_c <= to + 1e-6):
            if ramp.hold is not None and si(ramp.hold, "s") > 0:
                self.holding = True
            else:
                self.index += 1


def simulate(
    kiln: Kiln,
    *,
    schedule: Sequence[Ramp] | None = None,
    switch_over_c: float | None = None,
    dt: float = DT,
    record: bool = True,
) -> FiringRun:
    """Fire the kiln along its schedule (or ``schedule``) from the room's temperature."""
    us = kiln.units == "us"
    unit = "degF" if us else "degC"
    working: list[Step] = []
    findings: list[Finding] = []
    if schedule is None and kiln.firing.schedule is not None:
        schedule = kiln.firing.schedule
        working.append(
            Step(
                name="Firing schedule",
                value=f"{len(schedule)} segments, as given in the design",
            )
        )
    elif schedule is None:
        schedule, step = default_schedule(kiln)
        working.append(step)
    supply, supply_steps = heat_supply(kiln, switch_over_c)
    working += supply_steps
    faces = build_faces(kiln)
    t_air = si(kiln.site.ambient, "K")
    ware_kg = si(kiln.firing.ware, "kg") if kiln.firing.ware is not None else 0.0
    ware_cap = ware_kg * WARE_CP
    e_price = (
        si(kiln.site.electricity_price, "USD/kWh")
        if kiln.site.electricity_price is not None
        else None
    )
    p_price = (
        si(kiln.site.propane_price, "USD/gallon") if kiln.site.propane_price is not None else None
    )
    priced = (supply.electric_w is None or e_price is not None) and (
        supply.gas_w is None or (supply.fuel == "propane" and p_price is not None)
    )
    target_k = max(si(r.to, "K") for r in schedule)

    ctl = _Controller(schedule)
    t_c, time = t_air, 0.0
    totals = dict.fromkeys(("energy", "electricity", "fuel", "walls", "ware", "shell", "cost"), 0.0)
    held = True
    stalled = False
    behind_at: float | None = None
    points: list[FiringPoint] = []
    run = FiringRun(result=None)  # pyright: ignore[reportArgumentType]  # filled in below
    stall_window: list[tuple[float, float]] = []

    def keep(step: int, setpoint: float, kw: dict[str, float], shell_max: float) -> None:
        to_kwh = 1 / 3.6e6
        points.append(
            FiringPoint(
                time_h=time / 3600,
                chamber_c=t_c - 273.15,
                setpoint_c=setpoint - 273.15,
                heat_kw=kw["heat"],
                available_kw=kw["available"],
                electric_kw=kw["electric"],
                fuel_kw=kw["fuel"],
                walls_kw=kw["walls"],
                ware_kw=kw["ware"],
                shell_kw=kw["shell"],
                energy_kwh=totals["energy"] * to_kwh,
                electricity_kwh=totals["electricity"] * to_kwh,
                fuel_kwh=totals["fuel"] * to_kwh,
                cost_usd=totals["cost"] if priced else None,
                hottest_shell_c=shell_max - 273.15,
            )
        )
        if record and step % RECORD_EVERY == 0:
            run.times_h.append(time / 3600)
            run.profiles.append([list(f.wall.temperatures - 273.15) for f in faces])

    zero: dict[str, float] = dict.fromkeys(
        ("heat", "available", "electric", "fuel", "walls", "ware", "shell"), 0.0
    )
    keep(0, t_c, zero, t_air)
    step = 0
    while not ctl.done:
        if time >= MAX_HOURS * 3600:
            findings.append(
                Finding(
                    level="info",
                    message=(
                        f"The firing was stopped at {MAX_HOURS:g} hours, before the schedule's end."
                    ),
                )
            )
            break
        step += 1
        t_start = t_c
        target, paced = ctl.target(t_c, dt)
        results = [f.wall.prepare(dt) for f in faces]
        lines = [f.wall.heat_in_line(dt) for f in faces]
        a = sum(x[0] for x in lines) - ware_cap * t_c
        b = sum(x[1] for x in lines) + ware_cap
        source = _source_at(supply, t_c)
        if source == "electric":
            assert supply.electric_w is not None
            fraction, available_w = 1.0, supply.electric_w
        else:
            assert supply.gas_w is not None
            fraction = _fraction(round(t_c), _air_ratio(supply, t_c), supply.fuel)
            available_w = supply.gas_w * max(fraction, 0.0)
        e_max = available_w * dt
        need = a + b * target
        limited = False
        if need > e_max:
            t_new, limited = (e_max - a) / b, True
        elif need < 0:
            t_new = -a / b
        else:
            t_new = target
        heat = a + b * t_new
        outcomes: list[StepResult] = [r(t_new) for r in results]
        for f, o in zip(faces, outcomes, strict=True):
            f.wall.commit(t_new, o.surface)
        walls = sum(o.heat_in for o in outcomes)
        shell = sum(o.heat_out for o in outcomes)
        ware = ware_cap * (t_new - t_c)
        t_c = t_new
        time += dt
        electric_j = heat if source == "electric" else 0.0
        fuel_j = heat / fraction if source == "gas" and heat > 0 else 0.0
        totals["energy"] += heat
        totals["electricity"] += electric_j
        totals["fuel"] += fuel_j
        totals["walls"] += walls
        totals["ware"] += ware
        totals["shell"] += shell
        if priced:
            totals["cost"] += electric_j / 3.6e6 * (e_price or 0.0) + (
                fuel_j / 3.6e6 * BTU_PER_KWH / PROPANE_HHV_BTU_PER_GAL * (p_price or 0.0)
            )
        if paced and limited and target - t_new > 0.5:
            held = False
            behind_at = behind_at if behind_at is not None else t_start
        kw = {
            "heat": heat / dt / 1000,
            "available": available_w / 1000,
            "electric": electric_j / dt / 1000,
            "fuel": fuel_j / dt / 1000,
            "walls": walls / dt / 1000,
            "ware": ware / dt / 1000,
            "shell": shell / dt / 1000,
        }
        keep(step, target, kw, max(o.surface for o in outcomes))
        ctl.advance(t_start, t_c, dt)
        # A kiln at full heat that no longer warms has stalled
        stall_window.append((time, t_c))
        while stall_window[0][0] < time - STALL_HOURS * 3600:
            stall_window.pop(0)
        if (
            limited
            and time - stall_window[0][0] >= STALL_HOURS * 3600 - 1.5 * dt
            and t_c - stall_window[0][1] < STALL_RISE
            and target > t_c + STALL_RISE
        ):
            if source == "electric" and supply.gas_w is not None:
                # A hybrid's elements have stalled short of the hand-over: light the burners
                supply = replace(supply, switch_over_k=t_c)
                stall_window.clear()
                findings.append(
                    Finding(
                        level="info",
                        message=(
                            f"The elements stall at {show(Q_(t_c, 'K'), unit)}, short of the "
                            "hand-over, so the burners take over there."
                        ),
                    )
                )
                continue
            stalled = True
            break

    completed = ctl.done
    duration = time / 3600
    to_kwh = 1 / 3.6e6
    if stalled:
        findings.append(
            Finding(
                level="info",
                message=(
                    f"The kiln stalls at {show(Q_(t_c, 'K'), unit)}: at full heat its walls and "
                    "shell take all the heat it has, so it can't reach "
                    f"{show(Q_(target_k, 'K'), unit)}."
                ),
            )
        )
    if not held and behind_at is not None:
        findings.append(
            Finding(
                level="info",
                message=(
                    "The heat can't keep the schedule from about "
                    f"{show(Q_(behind_at, 'K'), unit)}: the kiln falls behind the asked rate, "
                    "and the firing takes longer."
                ),
            )
        )
    gallons = (
        totals["fuel"] * to_kwh * BTU_PER_KWH / PROPANE_HHV_BTU_PER_GAL
        if supply.gas_w is not None and supply.fuel == "propane"
        else None
    )
    cost = totals["cost"] if priced else None
    heat_name = (
        "electric"
        if supply.gas_w is None
        else "gas"
        if supply.electric_w is None
        else f"electric, then gas from {show(Q_(supply.switch_over_k or 0.0, 'K'), unit, 4)}"
    )
    working += [
        Step(
            name="Method",
            value=f"{len(faces)} faces, a {dt:g} s step",
            note=(
                "The hot face is held at the chamber's temperature; the outside loses heat as in "
                "the steady heat loss (or into the ground)."
            ),
            reference=METHOD,
        ),
        Step(
            name="Firing time",
            value=f"{duration:.2f} h",
            note="to the schedule's end" if completed else "stopped before the schedule's end",
        ),
        Step(
            name="Heat put into the kiln",
            value=show(Q_(totals["energy"], "J"), "kWh"),
            formula="Σ heat per step = walls + ware",
            inputs={
                "into the walls": show(Q_(totals["walls"], "J"), "kWh"),
                "into the ware": show(Q_(totals["ware"], "J"), "kWh"),
                "of which lost from the shell": show(Q_(totals["shell"], "J"), "kWh"),
            },
        ),
    ]
    if ware_kg:
        working.append(
            Step(
                name="Ware and furniture",
                value=show(kiln.firing.ware, "lb" if us else "kg"),  # pyright: ignore[reportArgumentType]
                inputs={"specific heat": f"{WARE_CP:g} J/(kg·K)"},
                reference=WARE_SOURCE,
                note="Lumped at the chamber's temperature; fired clay's room-temperature c_p.",
            )
        )
    else:
        findings.append(
            Finding(
                level="info",
                message=(
                    "No ware is given (firing.ware), so the simulation heats an empty kiln; ware "
                    "and shelves take more heat and time."
                ),
            )
        )
    if supply.electric_w is not None:
        working.append(
            Step(name="Electricity used", value=show(Q_(totals["electricity"], "J"), "kWh"))
        )
    if supply.gas_w is not None:
        working.append(
            Step(
                name="Fuel burned",
                value=show(Q_(totals["fuel"], "J"), "kWh")
                + (f" ({gallons:.1f} gal of propane)" if gallons is not None else ""),
                formula="Σ heat put in by the burners ÷ available heat at the kiln's temperature",
                inputs={"propane": "91,502 BTU/gal"} if gallons is not None else {},
                reference=COMBUSTION_SOURCE,
            )
        )
    cost_text = None
    if cost is not None:
        cost_text = f"${cost:,.2f}"
        working.append(
            Step(
                name="Cost of the firing",
                value=cost_text,
                formula="kWh × electricity price + gallons × propane price",
                inputs={
                    k: v
                    for k, v in (
                        ("electricity", f"${e_price:.3f}/kWh" if e_price is not None else None),
                        ("propane", f"${p_price:.2f}/gal" if p_price is not None else None),
                    )
                    if v is not None
                },
            )
        )
    else:
        findings.append(
            Finding(
                level="info",
                message=(
                    "The firing's cost isn't given: it needs the site's electricity_price"
                    + (
                        " and propane_price"
                        if supply.gas_w is not None and supply.fuel == "propane"
                        else ""
                    )
                    + (
                        "; natural gas has no price in the design"
                        if supply.gas_w is not None and supply.fuel == "natural_gas"
                        else ""
                    )
                    + "."
                ),
            )
        )
    findings += _data_findings(kiln, faces)
    findings.append(
        Finding(
            level="info",
            message=(
                "The simulation holds the walls' hot faces at the chamber's temperature and treats "
                "the chamber and its ware as one temperature; flue losses are counted through the "
                "burners' available heat, but not air leaks or the door's seal."
            ),
            reference=GROUND_SOURCE if kiln.chamber.on_ground else None,
        )
    )
    run.result = FiringResult(
        name=kiln.name,
        heat=heat_name,
        switch_over_c=(supply.switch_over_k - 273.15) if supply.switch_over_k else None,
        reached_c=max(p.chamber_c for p in points),
        target_c=target_k - 273.15,
        duration_h=duration,
        duration=f"{int(duration)} h {round((duration % 1) * 60):02d} min",
        held=held,
        completed=completed,
        electricity_kwh=totals["electricity"] * to_kwh,
        fuel_kwh=totals["fuel"] * to_kwh,
        propane_gallons=gallons,
        energy_kwh=totals["energy"] * to_kwh,
        walls_kwh=totals["walls"] * to_kwh,
        ware_kwh=totals["ware"] * to_kwh,
        shell_kwh=totals["shell"] * to_kwh,
        cost_usd=cost,
        cost=cost_text,
        points=points,
        faces=[
            FaceProfile(
                face=f.name,
                depths_m=[float(x) for x in f.wall.centres],
                layers=[f.wall.layers[i].name for i in f.wall.owner],
                inside_area_m2=f.wall.inside_area,
                outside_area_m2=f.wall.outside_area,
            )
            for f in faces
        ],
        working=working,
        findings=findings,
    )
    return run


def _data_findings(kiln: Kiln, faces: Sequence[_Face]) -> list[Finding]:
    from kilndesigner.castable import resolve_material

    out: list[Finding] = []
    sources: dict[str, str] = {}
    given: set[str] = set()
    for face in faces:
        for x in kiln.lining.for_face(face.name, door_face=kiln.door_face):  # pyright: ignore[reportArgumentType]
            m = resolve_material(kiln, x.material)
            if x.specific_heat is not None:
                given.add(m.name)
            elif m.specific_heat is not None:
                sources[m.name] = f"{m.specific_heat.source} ({m.specific_heat.status})"
    if sources:
        out.append(
            Finding(
                level="info",
                message=(
                    "Specific heats come from one source each, most of them generic or a class "
                    "value rather than the maker's sheet, and are held at their end values outside "
                    "their temperatures: "
                    + "; ".join(f"{k}: {v}" for k, v in sorted(sources.items()))
                ),
            )
        )
    if given:
        out.append(
            Finding(
                level="info",
                message="Specific heat as given in the design for: " + ", ".join(sorted(given)),
            )
        )
    return out


class SwitchPoint(BaseModel):
    model_config = ConfigDict(frozen=True)

    switch_over_c: float
    switch_over_f: float
    duration_h: float
    cost_usd: float
    electricity_kwh: float
    propane_gallons: float
    held: bool
    completed: bool
    # Where the burners really took over: lower than asked when the elements stalled first
    handed_over_c: float | None = None
    elements_stalled: bool = False


class SwitchOverChart(BaseModel):
    """A hybrid's firing time and cost against where it hands over from elements to burners."""

    model_config = ConfigDict(frozen=True)

    points: list[SwitchPoint]
    cheapest_c: float
    fastest_c: float
    working: list[Step]
    findings: list[Finding]


def switch_over_chart(kiln: Kiln, *, step_f: float = 200.0, dt: float = DT) -> SwitchOverChart:
    """Simulate the firing with the hand-over at each ``step_f`` °F from 400 °F to the top."""
    if kiln.heat.electric is None or kiln.heat.gas is None:
        raise SimulationError("the switch-over chart is for a kiln with elements and burners")
    gas = kiln.heat.gas
    if gas.fuel != "propane":
        raise SimulationError("the switch-over chart is worked out for propane only")
    if kiln.site.electricity_price is None or kiln.site.propane_price is None:
        raise SimulationError("give the site's electricity_price and propane_price")
    top, _ = top_temperature(kiln)
    top_f = si(top, "degF")
    temps_f = list(np.arange(400.0, top_f, step_f))
    points: list[SwitchPoint] = []
    for t_f in temps_f:
        t_c = (t_f - 32) / 1.8
        r = simulate(kiln, switch_over_c=t_c, dt=dt, record=False).result
        points.append(
            SwitchPoint(
                switch_over_c=t_c,
                switch_over_f=t_f,
                duration_h=r.duration_h,
                cost_usd=r.cost_usd or 0.0,
                electricity_kwh=r.electricity_kwh,
                propane_gallons=r.propane_gallons or 0.0,
                held=r.held,
                completed=r.completed,
                handed_over_c=r.switch_over_c,
                elements_stalled=r.switch_over_c is not None and r.switch_over_c < t_c - 0.5,
            )
        )
    done = [p for p in points if p.completed] or points
    cheapest = min(done, key=lambda p: p.cost_usd)
    fastest = min(done, key=lambda p: p.duration_h)
    unit = "degF" if kiln.units == "us" else "degC"
    working = [
        Step(
            name="Switch-over chart",
            value=f"{len(points)} firings, the hand-over every {step_f:g} °F",
            note="Each is the full transient firing with the elements off from the hand-over.",
            reference=METHOD,
        ),
        Step(
            name="Cheapest hand-over",
            value=f"{show(Q_(cheapest.switch_over_c, 'degC'), unit)}: ${cheapest.cost_usd:,.2f}, "
            f"{cheapest.duration_h:.1f} h",
        ),
        Step(
            name="Fastest hand-over",
            value=f"{show(Q_(fastest.switch_over_c, 'degC'), unit)}: {fastest.duration_h:.1f} h, "
            f"${fastest.cost_usd:,.2f}",
        ),
    ]
    findings: list[Finding] = []
    stalled = [p for p in points if p.elements_stalled and p.handed_over_c is not None]
    if stalled:
        at = show(Q_(min(p.handed_over_c or 0.0 for p in stalled), "degC"), unit)
        findings.append(
            Finding(
                level="info",
                message=(
                    f"The elements stall at about {at}, so a hand-over set above that happens at "
                    "the stall: those points are the same firing."
                ),
            )
        )
    if any(not p.completed for p in points):
        findings.append(
            Finding(
                level="info",
                message=(
                    "Some hand-overs never finish the firing: the elements stall before reaching "
                    "them. Those points are left out of the cheapest and fastest."
                ),
            )
        )
    if gas.reduction:
        findings.append(
            Finding(
                level="info",
                message=(
                    "Hand-overs above about 900 °C leave the elements on into reduction, which "
                    "attacks their oxide layer."
                ),
                reference=COMBUSTION_SOURCE,
            )
        )
    return SwitchOverChart(
        points=points,
        cheapest_c=cheapest.switch_over_c,
        fastest_c=fastest.switch_over_c,
        working=working,
        findings=findings,
    )
