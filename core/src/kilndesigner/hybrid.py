"""Hybrid kilns: when to hand over from the elements to the burners.

Two things decide it:

1. **What each kWh of heat costs, by kiln temperature.** An element puts all of its energy into
   the kiln. A burner loses whatever leaves up the chimney, and that loss grows with the kiln's
   temperature (:mod:`kilndesigner.combustion`). So propane's cost per useful kWh rises through
   the firing while electricity's stays flat.
2. **What the elements can still do.** Their power is fixed; the kiln's heat loss rises with
   temperature. Where the loss reaches the element power, the elements alone can't raise the
   kiln any further: the *electric ceiling*. Well before it, they heat slowly.

And one limit: reduction attacks the elements' protective oxide, so they should be off before
reduction starts (about 900 °C; Kanthal allows A-1 and APM 1050 °C in CO- and H₂-rich gas).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from kilndesigner.combustion import (
    PROPANE_HHV_BTU_PER_GAL,
    air_ratio_for_flue_oxygen,
    available_heat_fraction,
)
from kilndesigner.combustion import (
    SOURCE as COMBUSTION_SOURCE,
)
from kilndesigner.heatloss import heat_loss, top_temperature
from kilndesigner.library import alloy
from kilndesigner.model import Kiln
from kilndesigner.numeric import find_root
from kilndesigner.units import Q_, Quantity, si
from kilndesigner.working import Finding, Step, show

BTU_PER_KWH = 3412.14
REDUCTION_START = Q_(900, "degC")
REDUCTION_SOURCE = (
    "Fire in oxidation to about 900 °C before reducing (Finkelnburg, Ceramics Monthly 2022); "
    "combustion-and-masonry.md §8 [S66]"
)
OXIDATION_O2 = 0.03  # oxidation means more than 3% excess oxygen (Frenzel) [S69]
REDUCTION_AIR = 0.9  # a moderate reduction, λ = 0.9 (combustion-and-masonry.md §8, derived)


class CostPoint(BaseModel):
    model_config = ConfigDict(frozen=True)

    temperature_f: float
    temperature_c: float
    electric_per_kwh: float
    propane_per_kwh: float
    propane_reducing_per_kwh: float | None
    element_surplus_kw: float


class HybridAnalysis(BaseModel):
    model_config = ConfigDict(frozen=True)

    element_power: str
    electric_ceiling: str
    electric_ceiling_c: float
    cost_crossover: str | None
    switch_over: str
    switch_over_c: float
    switch_over_reason: str
    points: list[CostPoint]
    working: list[Step]
    findings: list[Finding]


def propane_cost_per_kwh(price_per_gal: float, t_flue_k: float, air_ratio: float) -> float:
    """Dollars per kWh that stays in the kiln, with the flue gas at ``t_flue_k``."""
    kwh_per_gal = PROPANE_HHV_BTU_PER_GAL / BTU_PER_KWH
    return price_per_gal / (kwh_per_gal * available_heat_fraction(t_flue_k, air_ratio))


def analyse_hybrid(kiln: Kiln, element_watts: float) -> HybridAnalysis:
    electric, gas = kiln.heat.electric, kiln.heat.gas
    if electric is None or gas is None:
        raise ValueError("a hybrid needs both elements and burners")
    site = kiln.site
    if site.electricity_price is None or site.propane_price is None:
        raise ValueError("give the site's electricity_price and propane_price")
    us = kiln.units == "us"
    unit = "degF" if us else "degC"
    e_price = si(site.electricity_price, "USD/kWh")
    p_price = si(site.propane_price, "USD/gallon")
    top, _ = top_temperature(kiln)
    t_air = si(site.ambient, "K")
    lam = air_ratio_for_flue_oxygen(OXIDATION_O2)
    working: list[Step] = []
    findings: list[Finding] = []

    def loss_watts(t_k: float) -> float:
        return heat_loss(kiln, inside=Q_(t_k, "K")).total_watts

    # The electric ceiling: where the steady loss equals the element power.
    t_top = si(top, "K")
    lo = t_air + 60.0
    if loss_watts(t_top) <= element_watts:
        ceiling = t_top
        ceiling_text = f"the top temperature ({show(top, unit)}); the elements could fire it alone"
    else:
        ceiling = find_root(lambda t: loss_watts(t) - element_watts, lo, t_top, xtol=0.5)
        ceiling_text = show(Q_(ceiling, "K"), unit, 4)
    working.append(
        Step(
            name="Electric ceiling",
            value=ceiling_text,
            formula="the inside temperature where the steady heat loss equals the element power",
            inputs={"element power": show(Q_(element_watts, "W"), "kW")},
            note=(
                "The steady loss ignores the heat going into the ware and walls, so the elements "
                "slow down well before this; it is an upper bound."
            ),
        )
    )

    # Cost per useful kWh, by temperature.
    points: list[CostPoint] = []
    t_f = 300.0
    top_f = si(top, "degF")
    crossover: float | None = None
    previous: tuple[float, float] | None = None
    while t_f <= top_f + 1e-6:
        t_k = si(Q_(t_f, "degF"), "K")
        gas_cost = propane_cost_per_kwh(p_price, t_k, lam)
        reducing = (
            propane_cost_per_kwh(p_price, t_k, REDUCTION_AIR)
            if gas.reduction and t_k >= si(REDUCTION_START, "K") - 1e-6
            else None
        )
        points.append(
            CostPoint(
                temperature_f=t_f,
                temperature_c=si(Q_(t_f, "degF"), "degC"),
                electric_per_kwh=e_price,
                propane_per_kwh=gas_cost,
                propane_reducing_per_kwh=reducing,
                element_surplus_kw=(element_watts - loss_watts(t_k)) / 1000,
            )
        )
        diff = gas_cost - e_price
        if previous is not None and crossover is None and (previous[1] < 0) != (diff < 0):
            crossover = previous[0] + (t_f - previous[0]) * previous[1] / (previous[1] - diff)
        previous = (t_f, diff)
        t_f += 100.0
    first = points[0]
    working.append(
        Step(
            name="Propane, cost per useful kWh",
            value=(
                f"${first.propane_per_kwh:.3f} at {first.temperature_f:.0f} °F rising to "
                f"${points[-1].propane_per_kwh:.3f} at {points[-1].temperature_f:.0f} °F"
            ),
            formula="price per gallon ÷ (26.8 kWh per gallon × available heat)",
            inputs={
                "propane": f"${p_price:.2f}/gal",
                "air": f"{OXIDATION_O2:.0%} oxygen in the flue (λ = {lam:.2f})",
                "flue gas": "leaves at the kiln's temperature",
            },
            reference=COMBUSTION_SOURCE,
        )
    )
    working.append(
        Step(
            name="Electricity, cost per useful kWh",
            value=f"${e_price:.3f} at every temperature",
            note="An element puts all of its energy into the kiln.",
        )
    )
    cross_text = None
    if crossover is not None:
        cross_text = show(Q_(crossover, "degF"), unit, 4)
        working.append(
            Step(
                name="Where propane and electricity cost the same per useful kWh",
                value=cross_text,
            )
        )
    else:
        # No crossover: one heat is cheaper from the first temperature to the top
        cheaper = "electricity" if first.propane_per_kwh > e_price else "propane"
        working.append(
            Step(name="Cheaper heat", value=f"{cheaper}, at every temperature in the firing")
        )

    # The switch-over.
    candidates: list[tuple[float, str]] = [
        (ceiling, "the elements can't raise the kiln any further above it")
    ]
    if gas.reduction:
        candidates.append(
            (si(REDUCTION_START, "K"), "reduction starts about here and attacks the elements")
        )
    if electric.off_above is not None:
        candidates.append((si(electric.off_above, "K"), "as set in the design"))
    switch, reason = min(candidates)
    if crossover is not None and first.propane_per_kwh < e_price:
        # Propane's cost per useful kWh rises with temperature, so cheap propane wins early and
        # electricity late: the opposite of a hybrid's order. Say so; don't move the switch.
        findings.append(
            Finding(
                level="info",
                message=(
                    f"Below {cross_text}, propane is the cheaper heat per useful kWh at these "
                    "prices; above it, electricity is. Running the elements early pays for "
                    "control (a slow, even, programmable start), not for cost."
                ),
                reference=COMBUSTION_SOURCE,
            )
        )
    working.append(
        Step(
            name="Switch-over",
            value=show(Q_(switch, "K"), unit, 4),
            note=f"The lowest of the limits: {reason}.",
            reference=REDUCTION_SOURCE if gas.reduction else None,
        )
    )
    on_past = electric.off_above is not None and si(electric.off_above, "K") > si(
        REDUCTION_START, "K"
    )
    if gas.reduction and on_past:
        assert electric.off_above is not None
        wire = alloy(electric.alloy)
        findings.append(
            Finding(
                level="warning",
                message=(
                    f"The elements stay on to {show(electric.off_above, unit)}, past the start of "
                    "reduction. Reduction attacks the alumina layer that protects the wire; "
                    f"Kanthal allows {wire.name} only {show(wire.max_reducing_temperature, unit)} "
                    "in CO- and H₂-rich gas."
                ),
                reference="electric-and-thermal.md §1.4, §1.5 [S9]",
            )
        )
    if first.propane_per_kwh > e_price:
        findings.append(
            Finding(
                level="info",
                message=(
                    f"At ${e_price:.2f}/kWh and ${p_price:.2f}/gal, electricity is the cheaper "
                    "heat at every temperature, so run the elements as long as they can keep the "
                    "schedule, and add the burners alongside them rather than instead of them."
                ),
                reference=COMBUSTION_SOURCE,
            )
        )
    elif crossover is None:
        findings.append(
            Finding(
                level="info",
                message=(
                    f"At ${e_price:.2f}/kWh and ${p_price:.2f}/gal, propane is the cheaper heat at "
                    "every temperature, so the elements save nothing on fuel at any stage of the "
                    "firing."
                ),
                reference=COMBUSTION_SOURCE,
            )
        )
    findings.append(
        Finding(
            level="info",
            message=(
                "Cost per firing needs a firing schedule and the heat stored in the walls and "
                "ware; that comes with the firing simulation (plan milestone M6)."
            ),
        )
    )
    return HybridAnalysis(
        element_power=show(Q_(element_watts, "W"), "kW"),
        electric_ceiling=ceiling_text,
        electric_ceiling_c=si(Q_(ceiling, "K"), "degC"),
        cost_crossover=cross_text,
        switch_over=show(Q_(switch, "K"), unit, 4),
        switch_over_c=si(Q_(switch, "K"), "degC"),
        switch_over_reason=reason,
        points=points,
        working=working,
        findings=findings,
    )


__all__ = ["HybridAnalysis", "Quantity", "analyse_hybrid", "propane_cost_per_kwh"]
