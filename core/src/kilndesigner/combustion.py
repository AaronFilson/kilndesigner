"""Propane combustion: how much of the fuel's heat stays in the kiln.

The gases leave a kiln at about the kiln's temperature, carrying heat up the chimney. What is
left, the *available heat*, is the fuel's heating value minus the heat in the flue gas. It falls
steeply as the kiln gets hotter, and that is why a gas kiln uses most of its fuel near the top.

The thermodynamics come from Cantera with the GRI-Mech 3.0 mechanism (NASA polynomial data for
every species, including dissociation at kiln temperatures). Reactants start at the air
temperature; products are taken at equilibrium at the flue temperature.

Heating values and air composition: combustion-and-masonry.md §1.1.
"""

from __future__ import annotations

from functools import cache
from typing import Any

PROPANE_HHV_MJ_PER_KG = 50.152  # GREET [S5]
PROPANE_HHV_BTU_PER_GAL = 91_502  # at 60 °F [S1, S2]
PROPANE_LB_PER_GAL = 4.20  # at 60 °F [S1, S2]
O2_IN_AIR = 0.2095  # by volume; gives 23.86 ft³ air per ft³ propane [S1]
N2_PER_O2 = (1 - O2_IN_AIR) / O2_IN_AIR
SOURCE = (
    "Cantera 3.2, GRI-Mech 3.0 thermodynamics; propane HHV 50.152 MJ/kg (GREET) and "
    "91,502 BTU/gal; combustion-and-masonry.md §1.1"
)


def air_ratio_for_flue_oxygen(o2_dry: float) -> float:
    """λ (air supplied ÷ air needed) that leaves ``o2_dry`` oxygen in the dry flue gas.

    C3H8 + 5λ(O2 + n N2) → 3 CO2 + 4 H2O + 5(λ − 1) O2 + 5λn N2, so the dry flue gas holds
    3 + 5(λ − 1) + 5λn moles, of which 5(λ − 1) are oxygen.
    """
    n = N2_PER_O2
    return (5 - 2 * o2_dry) / (5 - o2_dry * (5 + 5 * n))


@cache
def _gas() -> Any:
    import cantera as ct  # pyright: ignore[reportMissingTypeStubs]

    return ct.Solution("gri30.yaml")


def _reactants(air_ratio: float, t_air: float) -> tuple[Any, float, float]:
    gas = _gas()
    gas.TP = t_air, 101_325.0
    gas.set_equivalence_ratio(1.0 / air_ratio, "C3H8", f"O2:1.0, N2:{N2_PER_O2}")
    return gas, float(gas.enthalpy_mass), float(gas.Y[gas.species_index("C3H8")])


def available_heat(t_flue: float, air_ratio: float = 1.0, t_air: float = 298.15) -> float:
    """Heat kept in the kiln per kg of propane (J/kg), with the flue gas leaving at ``t_flue`` K."""
    gas, h_reactants, fuel_fraction = _reactants(air_ratio, t_air)
    gas.TP = t_flue, 101_325.0
    gas.equilibrate("TP")
    return (h_reactants - float(gas.enthalpy_mass)) / fuel_fraction


def available_heat_fraction(t_flue: float, air_ratio: float = 1.0, t_air: float = 298.15) -> float:
    """Available heat as a fraction of the higher heating value."""
    return available_heat(t_flue, air_ratio, t_air) / (PROPANE_HHV_MJ_PER_KG * 1e6)


def adiabatic_flame_temperature(air_ratio: float = 1.0, t_air: float = 298.15) -> float:
    gas, _, _ = _reactants(air_ratio, t_air)
    gas.equilibrate("HP")
    return float(gas.T)
