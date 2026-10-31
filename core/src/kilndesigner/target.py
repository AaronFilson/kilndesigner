"""A target firing time: the burner input that fires the kiln in it, and what that input needs.

1. **The input**: the firing simulation (:mod:`kilndesigner.simulation`) is run with trial burner
   inputs, bisected (on a log scale) to the least that finishes the schedule in the target time.
   In a hybrid the burners are lit from the start (or the design's ``gas.on_from``) and the
   elements stay on to the top, through reduction: the author's choice for fast firings, with the
   sourced cost to the elements' life given as a finding.
   The load is the design's own (its setting or ware).
2. **The burners**: the design's count, the library's burners at that count by the existing sizing
   rules (:func:`kilndesigner.gas.design_gas` with the input found), with the ports and the flue
   1 : 1 (Olsen p.151) and the chimney as for any gas kiln.
3. **The supply**, as a table of options to pick from: the 100 lb cylinders (full, and ¼ full
   keeping 10 psi) that carry the draw at the coldest air, the air the design's cylinders need,
   and each tank with the least fill it must be kept at, from the vaporization tables in
   data/gas.yaml.
4. **What limits it**: the schedule's paced segments (the cone's final rate), the most the library's
   burners give at the count and the pressure the supply allows, and the design's own supply. When
   the target can't be met the fastest firing within those limits is simulated and given.
5. **The ware**: no source sets a maximum heating rate for ware (hybrid-firing.md §5), so the
   heating rate is reported against the fastest sourced schedules, not refused.
"""

from __future__ import annotations

import math

from pydantic import BaseModel, ConfigDict

from kilndesigner.combustion import PROPANE_HHV_BTU_PER_GAL, PROPANE_LB_PER_GAL
from kilndesigner.gas import design_gas, gas_data, interpolate, tank_suggestion
from kilndesigner.gas_checks import COOLING, LIQUID_COOLING_F
from kilndesigner.heatloss import heat_loss, top_temperature
from kilndesigner.model import Cylinders, Kiln, Line
from kilndesigner.simulation import DT, MAX_HOURS, FiringResult, SimulationError, simulate
from kilndesigner.units import Q_, si
from kilndesigner.working import Finding, Step, show

W_PER_BTU_HR = si(Q_(1, "BTU/hr"), "W")
TOLERANCE = 0.01  # the input is found to 1 %
ELEMENTS_PAST_TOP_C = 100.0  # the hand-over set above the top: the elements never switch off
UNLIMITED_W = 1e9  # a trial input big enough that only the schedule's pace limits the firing
WARE_SOURCE = (
    "hybrid-firing.md §5: no source sets a maximum heating rate for ware; the fastest sourced "
    "glaze schedule is Bartlett's Fast Glaze, 316 °C/h (570 °F/h) to 1083 °C [H2]; Digitalfire, "
    "'up to 500F/hr should be fine' for thin, even bisque [H5]"
)
FASTEST_SOURCED_C_PER_H = 316.0  # Bartlett Fast Glaze, hybrid-firing.md §5.2 [H2]
ELEMENTS_SOURCE = (
    "hybrid-firing.md §1.2: Skutt, reducing 'will clobber their useful life' [H1]; reduction from "
    "about 900 °C [S66]"
)


TANK_K = {10: 45.0, 20: 60.0, 30: 70.0, 40: 80.0, 50: 90.0, 60: 100.0}
"""K of the D × L × K rule by percent full (combustion-and-masonry.md §2.3 [S1, S2]); the ⅓-full
table (§2.4) is read as the 50 % K, 90, as TANK_TABLE_FILL does."""


class SupplyOption(BaseModel):
    """One way to supply the propane for the firing: a row of the options table."""

    model_config = ConfigDict(frozen=True)

    option: str
    works: bool
    needs: str
    cost: str | None  # per firing: the propane and electricity, the same whatever holds the gas
    source: str


def _lowest_air_for(each: float, temps: list[float], caps: list[float]) -> float | None:
    """The lowest temperature in a table at which one vessel gives ``each`` BTU/hr; None past it."""
    if each > caps[-1]:
        return None
    return interpolate(each, caps, temps) if each > caps[0] else temps[0]


def _supply_options(
    draw: float,
    t_f: float,
    n_full: int,
    n_quarter: int,
    n_now: int | None,
    cost: str | None,
) -> tuple[list[SupplyOption], list[Step]]:
    """Every supply that carries ``draw`` at ``t_f`` °F of air, for the user to pick from."""
    data = gas_data()
    opt, con = data["cylinder_100lb_optimistic"], data["cylinder_100lb_conservative"]
    table = data["tanks_one_third_full"]
    rows: list[SupplyOption] = [
        SupplyOption(
            option="100 lb cylinders, full",
            works=True,
            needs=f"{n_full} cylinders at {t_f:.0f} °F",
            cost=cost,
            source=f"{opt['source']} ({COOLING})",
        ),
        SupplyOption(
            option="100 lb cylinders, down to ¼ full keeping 10 psi",
            works=True,
            needs=f"{n_quarter} cylinders at {t_f:.0f} °F",
            cost=cost,
            source=con["source"],
        ),
    ]
    if n_now is not None:
        each = draw / n_now
        full_air = _lowest_air_for(each, opt["temps_f"], opt["rows"][100])
        low_air = _lowest_air_for(each, con["temps_f"], con["btu_hr"])
        for label, air, top, src in (
            ("full", full_air, opt["temps_f"][-1], opt["source"]),
            ("¼ full", low_air, con["temps_f"][-1], con["source"]),
        ):
            air_text = (
                f"air at {air + (LIQUID_COOLING_F if label == 'full' else 0.0):.0f} °F or warmer"
                if air is not None
                else f"no temperature in the table (to {top:.0f} °F"
                + (" of liquid" if label == "full" else "")
                + ")"
            )
            rows.append(
                SupplyOption(
                    option=f"The design's {n_now} cylinders, {label}",
                    works=air is not None
                    and air + (LIQUID_COOLING_F if label == "full" else 0.0) <= t_f + 1e-9,
                    needs=air_text,
                    cost=cost,
                    source=src,
                )
            )
    t = min(max(t_f, 0.0), 70.0)
    fills, ks = list(TANK_K), list(TANK_K.values())
    for gallons, row in table["gallons"].items():
        at_90 = interpolate(t, table["temps_f"], row)
        k = 90.0 * draw / at_90
        works = k <= ks[-1]
        fill = interpolate(k, ks, [float(f) for f in fills]) if works else None
        rows.append(
            SupplyOption(
                option=f"{gallons} gal tank",
                works=works,
                needs=(
                    f"kept at least {max(fill or 0.0, fills[0]):.0f} % full at {t_f:.0f} °F"
                    if works
                    else f"too small even 60 % full at {t_f:.0f} °F ({at_90 * ks[-1] / 90:,.0f} "
                    "BTU/hr)"
                ),
                cost=cost,
                source=(
                    f"{table['source']}, scaled by K ÷ 90 for the fill (combustion-and-masonry.md "
                    "§2.3, derived)"
                ),
            )
        )
    step = Step(
        name="Propane supply options",
        value=f"{sum(r.works for r in rows)} of {len(rows)} work",
        inputs={"draw": f"{draw:,.0f} BTU/hr", "coldest air": f"{t_f:.0f} °F"},
        note=(
            "Each costs the same per firing: the propane burned is the same whatever holds it. "
            "A tank's fill is interpolated between the D × L × K rule's rows (derived)."
        ),
        reference="combustion-and-masonry.md §2.1–2.4",
    )
    return rows, [step]


class TargetFiring(BaseModel):
    """What a target firing time needs, and what limits it."""

    model_config = ConfigDict(frozen=True)

    target_h: float
    met: bool
    shortest_h: float  # the schedule's paced segments alone, with unlimited heat
    input_btu_hr: float  # needed for the target (or, unmet, what the target would need)
    input_per_ft3_btu_hr: float
    duration_h: float  # the firing at the input used: the target's, or the fastest within limits
    limits: list[str]
    burners: str | None
    burner_each_btu_hr: float | None
    burners_most_btu_hr: float | None  # the library's most at the design's count
    propane_gal_hr: float | None
    cylinders_full: int | None  # 100 lb cylinders needed at the coldest air, full
    cylinders_quarter: int | None  # and ¼ full keeping 10 psi
    tank: str | None
    supply_meets: bool | None  # the design's own supply carries the draw
    propane_gallons: float | None
    electricity_kwh: float
    elements_share: float  # of the heat put in
    cost_usd: float | None
    cost: str | None
    flue_area_in2: float
    inlet_area_in2: float | None
    chimney_height: str | None
    draft: list[str]
    peak_rate_c_per_h: float
    supply_options: list[SupplyOption]
    working: list[Step]
    findings: list[Finding]


def _peak_rate(r: FiringResult) -> float:
    """The fastest rise over any hour of the firing, °C/h."""
    pts = r.points
    best, j = 0.0, 0
    for p in pts:
        while pts[j].time_h < p.time_h - 1.0:
            j += 1
        span = p.time_h - pts[j].time_h
        if span >= 1.0 - 1e-6:
            best = max(best, (p.chamber_c - pts[j].chamber_c) / span)
    return best


def _cylinders(draw: float, t_f: float) -> tuple[int, int, list[Step]]:
    data = gas_data()
    opt, con = data["cylinder_100lb_optimistic"], data["cylinder_100lb_conservative"]
    liquid = min(max(t_f - LIQUID_COOLING_F, 0.0), 70.0)
    full = interpolate(liquid, opt["temps_f"], opt["rows"][100])
    quarter = interpolate(min(max(t_f, 0.0), 60.0), con["temps_f"], con["btu_hr"])
    n_full, n_quarter = math.ceil(draw / full - 1e-9), math.ceil(draw / quarter - 1e-9)
    steps = [
        Step(
            name="100 lb cylinders for the draw, full",
            value=str(n_full),
            formula="⌈draw ÷ each cylinder's vaporization⌉",
            inputs={"draw": f"{draw:,.0f} BTU/hr", "each": f"{full:,.0f} BTU/hr"},
            reference=f"{opt['source']}, read at the liquid's temperature ({COOLING})",
        ),
        Step(
            name="100 lb cylinders for the draw, ¼ full keeping 10 psi",
            value=str(n_quarter),
            formula="⌈draw ÷ each cylinder's vaporization⌉",
            inputs={"draw": f"{draw:,.0f} BTU/hr", "each": f"{quarter:,.0f} BTU/hr"},
            reference=con["source"],
            note="Cylinders in parallel are taken to add their capacities (an inference, §2.6).",
        ),
    ]
    return n_full, n_quarter, steps


def _without_named_burners(kiln: Kiln) -> Kiln:
    return _with_burner(kiln, None)


def _with_burner(kiln: Kiln, model: str | None) -> Kiln:
    """The kiln with its burners' model replaced (None: the library chooses), its count kept."""
    gas = kiln.heat.gas
    assert gas is not None
    burners = gas.burners.model_copy(update={"model": model, "rating": None})
    return kiln.model_copy(
        update={
            "heat": kiln.heat.model_copy(
                update={"gas": gas.model_copy(update={"burners": burners})}
            )
        }
    )


def solve_target(kiln: Kiln, target_h: float | None = None, *, dt: float = DT) -> TargetFiring:
    """The burner input, burners, supply and cost to fire ``kiln`` in ``target_h`` hours (or its
    ``firing.target_time``)."""
    gas = kiln.heat.gas
    if gas is None:
        raise SimulationError("a target firing time is solved for the burners: the kiln has none")
    if target_h is None:
        if kiln.firing.target_time is None:
            raise SimulationError("give a target firing time (firing.target_time)")
        target_h = si(kiln.firing.target_time, "hour")
    if target_h <= 0:
        raise SimulationError("the target firing time must be more than zero")
    us = kiln.units == "us"
    unit = "degF" if us else "degC"
    hybrid = kiln.heat.electric is not None
    lit_c: float | None = None
    if hybrid:
        lit_c = (
            si(gas.on_from, "degC") if gas.on_from is not None else si(kiln.site.ambient, "degC")
        )
    cap_h = max(3 * target_h, target_h + 12)
    working: list[Step] = []
    findings: list[Finding] = []
    # The elements stay on to the top, through reduction (the author's choice, 2026-10-30)
    off_c: float | None = None
    if hybrid:
        top, _ = top_temperature(kiln)
        off_c = si(top, "degC") + ELEMENTS_PAST_TOP_C
        working.append(
            Step(
                name="Elements and burners together",
                value=f"the burners lit from {show(Q_(lit_c or 0.0, 'degC'), unit)}, the elements "
                "on to the top",
                note=(
                    "The author's choice for a target firing time: both heat for the whole "
                    "firing, through reduction, at the cost of the elements' life."
                ),
                reference=ELEMENTS_SOURCE,
            )
        )

    def fire(watts: float, hours: float = cap_h) -> FiringResult:
        return simulate(
            kiln,
            switch_over_c=off_c,
            gas_from_c=lit_c,
            burner_w=watts,
            max_hours=hours,
            dt=dt,
            record=False,
        ).result

    def done_in(r: FiringResult) -> float:
        return r.duration_h if r.completed else math.inf

    shortest = fire(UNLIMITED_W).duration_h
    working.append(
        Step(
            name="Shortest firing the schedule allows",
            value=f"{shortest:.2f} h",
            formula="the schedule's paced segments, with unlimited heat",
            note="The cone's final rate over the last 100 °C sets most of it.",
        )
    )
    loss = heat_loss(kiln).total_watts
    plain = _without_named_burners(kiln)
    rule = design_gas(kiln, loss)
    if target_h < shortest - 1e-6:
        raise SimulationError(
            f"the schedule alone takes {shortest:.2f} h (its paced segments, such as the cone's "
            f"final rate), longer than the {target_h:g} h asked: no burner input fires it faster"
        )

    # Bisect the input: the duration falls as the input rises
    hi = si(Q_(rule.design_input_btu_hr, "BTU/hr"), "W")
    lo = 0.0
    tries = 0
    while done_in(fire(hi)) > target_h:
        lo, hi = hi, hi * 2
        tries += 1
        if hi > UNLIMITED_W:  # pragma: no cover - the shortest firing was checked above
            raise SimulationError("no burner input fires the schedule in the target time")
    if lo == 0.0:
        lo = hi / 2
        while lo > 1.0 and done_in(fire(lo)) <= target_h:
            hi, lo = lo, lo / 2
            tries += 1
    while hi / lo > 1 + TOLERANCE:
        mid = math.sqrt(lo * hi)
        tries += 1
        if done_in(fire(mid)) <= target_h:
            hi = mid
        else:
            lo = mid
    need_w = hi
    need = need_w / W_PER_BTU_HR
    at_target = fire(need_w)
    volume_ft3 = float(rule.ward_volume.split()[0])
    working.append(
        Step(
            name="Burner input for the target",
            value=f"{need:,.0f} BTU/hr ({need / volume_ft3:,.0f} BTU/ft³/hr)",
            formula="the least input whose simulated firing ends within the target, bisected",
            inputs={
                "target": f"{target_h:g} h",
                "simulated firings": str(tries + 3),
                "to within": f"{TOLERANCE:.0%}",
                **(
                    {"burners lit from": show(Q_(lit_c, "degC"), unit)} if lit_c is not None else {}
                ),
                "rule of thumb, for comparison": rule.design_input,
            },
            reference="simulation.py (ADR 0015)",
        )
    )

    # The burners at the design's count, from the library, and the most they give
    design = design_gas(plain, loss, need)
    most = design_gas(plain, loss, UNLIMITED_W / W_PER_BTU_HR).full_fire_btu_hr
    if design.full_fire_btu_hr > need * (1 + TOLERANCE) and gas.burners.type == "venturi":
        # No library burner turns down to its share: the one whose lowest published rating is
        # least, run there (gas.py's oversized burners)
        count = gas.burners.wanted or 1
        lows = {
            name: spec["btu_hr"][spec["psi"].index(min(p for p in spec["psi"]
                                                       if p >= spec["curve_from_psi"]))]
            for name, spec in gas_data()["venturi_burners"]["models"].items()
        }  # fmt: skip
        big_enough = [n for n in lows if lows[n] * count >= need] or list(lows)
        smallest = min(big_enough, key=lambda n: lows[n])
        design = design_gas(_with_burner(kiln, smallest), loss, need)
        findings.append(
            Finding(
                level="info",
                message=(
                    f"No library burner is rated for the {need / count:,.0f} BTU/hr each of "
                    f"{count} burners this firing needs at the pressure the supply allows: "
                    f"{count} × {smallest} draw {design.full_fire_btu_hr:,.0f} BTU/hr at their "
                    "lowest, so the supply is sized for that. Fire them turned down below their "
                    "published range, or light fewer of them."
                ),
                reference=gas_data()["venturi_burners"]["source"],
            )
        )
    limits: list[str] = []
    cap = need
    if most < need * (1 - 1e-6):
        cap = min(cap, most)
        limits.append(
            f"the burners: the library's biggest at the design's count give {most:,.0f} BTU/hr "
            f"at the pressure the supply allows, short of the {need:,.0f} BTU/hr needed"
        )
    supply_meets: bool | None = None
    if not isinstance(gas.supply, Line) and design.supply:
        own = design.supply[0].capacity_btu_hr
        supply_meets = own >= min(need, most) * (1 - 1e-9)
        if own < need * (1 - 1e-6):
            cap = min(cap, own)
            limits.append(
                f"the design's supply: {design.supply[0].case} vaporize {own:,.0f} BTU/hr at the "
                f"coldest air, short of the {need:,.0f} BTU/hr needed (more cylinders or a tank "
                "would lift it)"
            )
    met = cap >= need * (1 - 1e-6)
    used = at_target if met else fire(si(Q_(cap, "BTU/hr"), "W"), MAX_HOURS)
    if not met:
        findings.append(
            Finding(
                level="info",
                message=(
                    f"The {target_h:g} h target can't be met: "
                    + "; ".join(limits)
                    + f". The fastest firing within them, on {cap:,.0f} BTU/hr, takes "
                    f"{used.duration_h:.1f} h"
                    + ("" if used.completed else " and doesn't finish the schedule")
                    + "."
                ),
                reference="simulation.py (ADR 0015); gas.py",
            )
        )

    # The supply the draw needs at the coldest air
    t_cold = (
        kiln.site.coldest_ambient if kiln.site.coldest_ambient is not None else kiln.site.ambient
    )
    t_f = si(t_cold, "degF")
    draw = design.full_fire_btu_hr
    n_full = n_quarter = None
    tank: str | None = None
    gal_hr: float | None = None
    options: list[SupplyOption] = []
    if gas.fuel == "propane" and not isinstance(gas.supply, Line):
        n_full, n_quarter, steps = _cylinders(draw, t_f)
        working += steps
        tank = tank_suggestion(draw, t_f)
        n_now = gas.supply.count if isinstance(gas.supply, Cylinders) else None
        options, steps = _supply_options(draw, t_f, n_full, n_quarter, n_now, used.cost)
        working += steps
        gal_hr = draw / PROPANE_HHV_BTU_PER_GAL
        on_hand = (
            gas.supply.count * 100 / PROPANE_LB_PER_GAL
            if isinstance(gas.supply, Cylinders)
            else gas.supply.gallons / 3
        )
        burnt = used.propane_gallons or 0.0
        if burnt > on_hand:
            findings.append(
                Finding(
                    level="info",
                    message=(
                        f"The firing burns {burnt:.0f} gal of propane, more than the "
                        f"{on_hand:.0f} gal the design's supply holds."
                    ),
                )
            )
    elif gas.fuel == "propane":
        gal_hr = draw / PROPANE_HHV_BTU_PER_GAL

    # The ware: how fast it is heated
    peak = _peak_rate(used)
    working.append(
        Step(
            name="Fastest heating over an hour",
            value=f"{peak:.0f} °C/h ({peak * 1.8:.0f} °F/h)",
            reference=WARE_SOURCE,
        )
    )
    if peak > FASTEST_SOURCED_C_PER_H:
        findings.append(
            Finding(
                level="info",
                message=(
                    f"The ware heats at up to {peak:.0f} °C/h ({peak * 1.8:.0f} °F/h), faster than "
                    f"any sourced schedule ({FASTEST_SOURCED_C_PER_H:.0f} °C/h, Bartlett's Fast "
                    "Glaze). No source sets a limit, so it isn't refused; thick or uneven ware and "
                    "the quartz inversion at 573 °C are where it would crack."
                ),
                reference=WARE_SOURCE,
            )
        )
    share = used.electricity_kwh / used.energy_kwh if used.energy_kwh > 0 else 0.0
    if hybrid:
        working.append(
            Step(
                name="The elements' share of the heat",
                value=f"{share:.0%} ({used.electricity_kwh:,.0f} kWh)",
                note="On for the whole firing, through reduction.",
                reference=ELEMENTS_SOURCE,
            )
        )
    working += design.working
    findings += [f for f in used.findings if "into reduction" in f.message]
    findings += [f for f in design.findings if f.level != "info" or "target" in f.message]
    return TargetFiring(
        target_h=target_h,
        met=met,
        shortest_h=shortest,
        input_btu_hr=need,
        input_per_ft3_btu_hr=need / volume_ft3,
        duration_h=used.duration_h,
        limits=limits,
        burners=(
            f"{design.burners.count} × {design.burners.model} at {design.burners.pressure}"
            if design.burners is not None
            else None
        ),
        burner_each_btu_hr=(draw / design.burners.count if design.burners is not None else None),
        burners_most_btu_hr=most,
        propane_gal_hr=gal_hr,
        cylinders_full=n_full,
        cylinders_quarter=n_quarter,
        tank=tank,
        supply_meets=supply_meets,
        propane_gallons=used.propane_gallons,
        electricity_kwh=used.electricity_kwh,
        elements_share=share,
        cost_usd=used.cost_usd,
        cost=used.cost,
        flue_area_in2=design.flue_area_in2,
        inlet_area_in2=design.inlet_area_in2,
        chimney_height=design.chimney_height,
        draft=design.draft,
        peak_rate_c_per_h=peak,
        supply_options=options,
        working=working,
        findings=findings,
    )
