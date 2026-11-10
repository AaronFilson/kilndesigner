"""The sourced values v2's heat model uses, each with its reference in `docs/research/`.

Nothing here is fitted to a reference kiln (ADR 0017, decision 4). A value with no source is not
here: the caller gives it, and the working says it was given.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Sourced:
    """A value (SI) with where it comes from, and a note when it is flagged."""

    value: float
    reference: str
    note: str | None = None


# --- air -----------------------------------------------------------------------------------------

O2_IN_AIR = Sourced(
    0.2095,
    "combustion-and-masonry.md §1.1 [S1]: 20.95 % O2 by volume (v1's combustion.O2_IN_AIR)",
    "argon and the rest are counted as nitrogen",
)
N2_PER_O2 = (1 - O2_IN_AIR.value) / O2_IN_AIR.value

# --- wood ----------------------------------------------------------------------------------------

# Dry wood about 50 % C, 6 % H, 44 % O by mass: CH(a)O(b) per mole of carbon
WOOD_CHO = Sourced(
    0.0,
    "Pettersen, 'The chemical composition of wood', in Rowell (ed.), The Chemistry of Solid Wood, "
    "ACS Adv. Chem. 207, 1984, as quoted in firebox-efficiency.md §4 and cantera-tespy-review.md "
    "§2: about 50 % C, 6 % H, 44 % O by mass",
    "the chapter hasn't been read at the page; ash and nitrogen left out",
)
M_C, M_H, M_O = 12.011, 1.008, 15.999  # g/mol (IUPAC standard atomic weights)
WOOD_H_PER_C = (6.0 / M_H) / (50.0 / M_C)  # 1.430
WOOD_O_PER_C = (44.0 / M_O) / (50.0 / M_C)  # 0.661
WOOD_NET_DRY = Sourced(
    19e6,
    "Forest Research, 'Typical calorific values of fuels': wood, solid, oven dry, net 19 GJ/t "
    "(wood-fuel.md §1 [W2]); FAO UBET 2004 Table 10 gives 18.4–19.2 MJ/kg for five woods [W3]",
)
WOOD_NET_DRY_BAND = (18.4e6, 19.2e6)
EVAPORATION = Sourced(
    2.44e6,
    "FAO UBET 2004 eq. 3: H(w) = H(dry)(1 − w) − 2.44 w MJ/kg, 'the evaporation energy of water' "
    "(wood-fuel.md §2 [W3])",
)
AIR_DRY_MOISTURE = Sourced(
    0.12,
    "FAO UBET §5.1.2: air-dried wood holds 12–20 % water, wet basis (wood-fuel.md §2 [W3])",
)
AIR_DRY_MOISTURE_BAND = (0.12, 0.20)

# --- gas fuels -----------------------------------------------------------------------------------

PROPANE_HHV = Sourced(
    21_548 * 2.326e3,
    "21,548 BTU/lb (50.12 MJ/kg) at 60 °F [S1, S2] (combustion-and-masonry.md §1.1; v1's "
    "combustion.PROPANE_HHV_MJ_PER_KG)",
)
METHANE_HHV = Sourced(
    890.7e3 / 16.0425 * 1e3,
    "NIST: ΔcH° −890.7 kJ/mol, M 16.0425 g/mol [S87] (v1's combustion.METHANE_HHV_MJ_PER_KG)",
    "natural gas taken as methane, its main part, as v1 does",
)
RATING_BASIS = (
    "a burner's BTU/hr rating is taken on the gas's higher heating value, the basis of Olsen's "
    "1,100 and 2,550 BTU/ft³ for natural gas and propane (p.227, Rule 4; kiln-reference.md)"
)

# --- solids --------------------------------------------------------------------------------------

FIRED_CLAY_CP = Sourced(
    800.0,
    "Lienhard Table A.2, brick, fired clay, at 24 °C (masonry-materials.md §1.1 [M1]); then VDI "
    "Heat Atlas fireclay c_p from 400 °C (§2.3 [M2]): v1's ware curve (heat review #1)",
)
FIRED_CLAY_AT = 24.0 + 273.15
SHELL_EMISSIVITY = {"painted": 0.95, "oxidised_steel": 0.79, "rolled_steel_sheet": 0.6}
SHELL_REFERENCE = "CIBSE Guide C Table C3.7; electric-and-thermal.md §4.7 [S52] (v1's heatloss)"

# Hot-face emissivity lines ε₀ = a + 10⁻⁵·b·T (T in K), radiation-exchange.md §5, and the
# hemispherical share of the normal value for insulators, 0.95–1.0 (Jones et al. [R6] Fig. 6)
EMISSIVITY_LINES = {
    # Osborn 1985 via IFRF CF148 [R5] and Jones et al. [R6]: fire brick, 673–1673 K
    "dense-medium": (0.84, -20.0, (673.0, 1673.0), "Osborn 1985: fire brick, medium Al2O3"),
    "dense-low": (0.90, -10.0, (673.0, 1673.0), "Osborn 1985: fire brick, low Al2O3"),
    # Hampartsoumian 1990 via Jones et al. [R6] Table A2: Morgan MPK lightweight refractories
    "ifb-mpk125": (0.53, 8.0, (1063.0, 1350.0), "Hampartsoumian 1990: MPK 125"),
    "ifb-mpk140": (0.21, 25.3, (1073.0, 1350.0), "Hampartsoumian 1990: MPK 140"),
}
HEMISPHERICAL = Sourced(
    0.95,
    "Jones, Mason & Williams 2019 [R6] Fig. 6: an insulator's hemispherical emissivity is 0.95–1.0 "
    "of its normal value; CIBSE's 0.95 for smooth non-metals (thermal-properties.md §7)",
    "the band's low end",
)

# --- the gas tables ------------------------------------------------------------------------------

GRI30 = (
    "Cantera 3.2, GRI-Mech 3.0 thermodynamics and transport (ADR 0012; Smith, Golden, Frenklach "
    "et al. 1999): NASA polynomials 200–3500 K; mixture-averaged transport, checked against "
    "Holman's air within 3.5 % to 1000 K (cantera-tespy-review.md §7)"
)
