"""Gas combustion: how much of the fuel's heat stays in the kiln.

The gases leave a kiln at about the kiln's temperature, carrying heat up the chimney. What is
left, the *available heat*, is the fuel's heating value minus the heat in the flue gas. It falls
steeply as the kiln gets hotter, and that is why a gas kiln uses most of its fuel near the top.

The thermodynamics come from Cantera with the GRI-Mech 3.0 mechanism (NASA polynomial data for
every species, including dissociation at kiln temperatures). Reactants start at the air
temperature; products are taken at equilibrium at the flue temperature. Natural gas is taken as
methane, its main part.

Heating values and air composition: combustion-and-masonry.md §1.1.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import Any, Literal

type Fuel = Literal["propane", "natural_gas"]

# One propane data set, [S1, S2] (combustion-and-masonry.md §1.1): 21,548 BTU/lb (× 2.326 kJ/kg
# per BTU/lb = 50.12 MJ/kg), 91,502 BTU/gal and 4.20 lb/gal, all at 60 °F. GREET's 50.152 is its
# LPG row, not propane's (review G11).
PROPANE_HHV_MJ_PER_KG = 21_548 * 2.326e-3
PROPANE_HHV_BTU_PER_GAL = 91_502  # at 60 °F [S1, S2]
PROPANE_LB_PER_GAL = 4.20  # at 60 °F [S1, S2]
METHANE_HHV_MJ_PER_KG = 890.7 / 16.0425  # NIST: ΔcH° −890.7 kJ/mol, M 16.0425 g/mol [S87]
O2_IN_AIR = 0.2095  # by volume; gives 23.86 ft³ air per ft³ propane [S1]
N2_PER_O2 = (1 - O2_IN_AIR) / O2_IN_AIR
OXIDATION_O2 = 0.03  # oxidation means more than 3% excess oxygen (Frenzel) [S69]
REDUCTION_AIR = 0.9  # a moderate reduction, λ = 0.9 (combustion-and-masonry.md §8, derived)
SOURCE = (
    "Cantera 3.2, GRI-Mech 3.0 thermodynamics; propane HHV 21,548 BTU/lb (50.12 MJ/kg) and "
    "91,502 BTU/gal [S1, S2]; natural gas as methane, HHV 55.52 MJ/kg (NIST); "
    "combustion-and-masonry.md §1.1"
)


@dataclass(frozen=True)
class Gas:
    """A fuel gas: its species in GRI-Mech, its carbon and hydrogen atoms, and its higher heating
    value."""

    species: str
    carbon: int
    hydrogen: int
    hhv_mj_per_kg: float

    @property
    def oxygen(self) -> float:
        """Moles of O2 to burn one mole of the gas: C + H/4."""
        return self.carbon + self.hydrogen / 4


GASES: dict[Fuel, Gas] = {
    "propane": Gas("C3H8", 3, 8, PROPANE_HHV_MJ_PER_KG),
    "natural_gas": Gas("CH4", 1, 4, METHANE_HHV_MJ_PER_KG),
}


def air_ratio_for_flue_oxygen(o2_dry: float, fuel: Fuel = "propane") -> float:
    """λ (air supplied ÷ air needed) that leaves ``o2_dry`` oxygen in the dry flue gas.

    CₐHᵦ + λs(O2 + n N2) → a CO2 + (b/2) H2O + (λ − 1)s O2 + λsn N2, with s = a + b/4. The dry
    flue gas holds a + (λ − 1)s + λsn moles, of which (λ − 1)s are oxygen, so
    λ = (s(1 − o) + o·a) / (s(1 − o − n·o)).
    """
    g, n = GASES[fuel], N2_PER_O2
    s = g.oxygen
    return (s * (1 - o2_dry) + o2_dry * g.carbon) / (s * (1 - o2_dry - n * o2_dry))


@cache
def _mechanism() -> Any:
    import cantera as ct  # pyright: ignore[reportMissingTypeStubs]

    return ct.Solution("gri30.yaml")


def _reactants(air_ratio: float, t_air: float, fuel: Fuel) -> tuple[Any, float, float]:
    gas, species = _mechanism(), GASES[fuel].species
    gas.TP = t_air, 101_325.0
    gas.set_equivalence_ratio(1.0 / air_ratio, species, f"O2:1.0, N2:{N2_PER_O2}")
    return gas, float(gas.enthalpy_mass), float(gas.Y[gas.species_index(species)])


def available_heat(
    t_flue: float, air_ratio: float = 1.0, t_air: float = 298.15, fuel: Fuel = "propane"
) -> float:
    """Heat kept in the kiln per kg of fuel (J/kg), with the flue gas leaving at ``t_flue`` K."""
    gas, h_reactants, fuel_fraction = _reactants(air_ratio, t_air, fuel)
    gas.TP = t_flue, 101_325.0
    gas.equilibrate("TP")
    return (h_reactants - float(gas.enthalpy_mass)) / fuel_fraction


def available_heat_fraction(
    t_flue: float, air_ratio: float = 1.0, t_air: float = 298.15, fuel: Fuel = "propane"
) -> float:
    """Available heat as a fraction of the higher heating value."""
    hhv = GASES[fuel].hhv_mj_per_kg * 1e6
    return available_heat(t_flue, air_ratio, t_air, fuel) / hhv


def adiabatic_flame_temperature(
    air_ratio: float = 1.0, t_air: float = 298.15, fuel: Fuel = "propane"
) -> float:
    gas, _, _ = _reactants(air_ratio, t_air, fuel)
    gas.equilibrate("HP")
    return float(gas.T)
