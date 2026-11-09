"""Wood per firing, from the heat a firing puts into the kiln and the user's own wood.

Every input is the user's (``site.wood``): the net heating value of the oven-dry wood, its
moisture on the wet basis and the firebox's efficiency. None has a default, since wood varies by
species, moisture and stacking, and no source gives a kiln firebox's efficiency
(docs/research/wood-fuel.md).

1. The net heating value at the wood's moisture (FAO, Unified Bioenergy Terminology, 2004, §5.1.2,
   eq. 3): H(w) = H(dry)·(1 − w) − 2.44 MJ/kg·w, the 2.44 MJ/kg being the water's evaporation.
2. The wood as fired: m = Q ÷ (η·H(w)), Q the heat into the kiln's walls and ware.
3. Its oven-dry part m·(1 − w); over the oven-dry weight of a cord, the cords; times the price of a
   cord, the cost.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from kilndesigner.model import WoodFuel
from kilndesigner.units import Q_, format_quantity, si
from kilndesigner.working import Step

EVAPORATION_MJ_PER_KG = 2.44
MOISTURE_SOURCE = (
    "FAO, Unified Bioenergy Terminology (UBET), 2004, §5.1.2 eq. 3: H(w) = H(dry)·(1 − w) − 2.44·w "
    "MJ/kg; wood-fuel.md §2"
)
CORD_SOURCE = (
    "A standard cord, 4 × 4 × 8 ft = 128 ft³ stacked (MU Extension G5450); wood-fuel.md §1"
)
SOURCE = "docs/research/wood-fuel.md"


class WoodError(ValueError):
    """Wood the engine can't work out a firing for, with the reason."""


class WoodEstimate(BaseModel):
    """The wood one firing burns, with its working."""

    model_config = ConfigDict(frozen=True)

    as_fired_kg: float
    oven_dry_kg: float
    cords: float | None
    cost_usd: float | None
    working: list[Step]


def wood_per_firing(heat_j: float, wood: WoodFuel, *, us: bool = False) -> WoodEstimate:
    """The wood that puts ``heat_j`` joules into the kiln, by the user's own values."""
    h_dry = si(wood.heating_value, "MJ/kg")
    w = si(wood.moisture, "")
    eta = si(wood.firebox_efficiency, "")
    h_wet = h_dry * (1 - w) - EVAPORATION_MJ_PER_KG * w
    if h_wet <= 0:
        raise WoodError(
            f"wood at {w:.0%} moisture gives no heat: evaporating its water takes all of its "
            f"{h_dry:g} MJ/kg ({MOISTURE_SOURCE})"
        )
    heat_mj = heat_j / 1e6
    wet_kg = heat_mj / (eta * h_wet)
    dry_kg = wet_kg * (1 - w)
    mass_unit = "lb" if us else "kg"
    steps = [
        Step(
            name="Wood's net heating value at its moisture",
            value=f"{h_wet:.2f} MJ/kg as fired",
            formula="H(w) = H(dry)·(1 − w) − 2.44 MJ/kg·w",
            inputs={
                "H(dry), yours": format_quantity(wood.heating_value),
                "w, wet basis, yours": f"{w:.0%}",
            },
            reference=MOISTURE_SOURCE,
        ),
        Step(
            name="Wood per firing",
            value=f"{_mass(wet_kg, mass_unit)} as fired ({_mass(dry_kg, mass_unit)} oven-dry)",
            formula="m = Q ÷ (η·H(w)); oven-dry m·(1 − w)",
            inputs={
                "Q, heat into the kiln": f"{heat_mj / 3.6:.1f} kWh",
                "η, firebox efficiency, yours": f"{eta:.0%}",
            },
            note=(
                "Q is the simulated heat into the walls and ware; the firebox efficiency stands "
                "for everything else, chiefly the flue gas."
            ),
            reference=SOURCE,
        ),
    ]
    cords = cost = None
    if wood.cord_weight is not None:
        cord_kg = si(wood.cord_weight * Q_(1, "cord"), "kg")
        cords = dry_kg / cord_kg
        steps.append(
            Step(
                name="Cords per firing",
                value=f"{cords:.2f} cord",
                formula="oven-dry wood ÷ oven-dry weight of a cord",
                inputs={"a cord, yours": format_quantity(wood.cord_weight)},
                reference=CORD_SOURCE,
            )
        )
        if wood.price is not None:
            per_cord = si(wood.price * Q_(1, "cord"), "USD")
            cost = cords * per_cord
            steps.append(
                Step(
                    name="Cost of the wood",
                    value=f"${cost:,.2f}",
                    formula="cords × price of a cord",
                    inputs={"price, yours": f"${per_cord:,.2f}/cord"},
                )
            )
    return WoodEstimate(
        as_fired_kg=wet_kg, oven_dry_kg=dry_kg, cords=cords, cost_usd=cost, working=steps
    )


def _mass(kg: float, unit: str) -> str:
    return f"{si(Q_(kg, 'kg'), unit):,.0f} {unit}"


__all__ = ["WoodError", "WoodEstimate", "wood_per_firing"]
