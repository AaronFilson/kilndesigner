"""The printed fuel of a reference kiln as heat, with the sources and the spread of each input.

Engine v2's validation (ADR 0017) compares the heat a model puts into a kiln with the
heat in the fuel the book says the kiln burned. These conversions are the book's side of that
comparison. Every number is sourced in ``docs/research/``; where none is, the fuel isn't converted
and the reason is returned instead.
"""

from __future__ import annotations

from dataclasses import dataclass

from kilndesigner.units import Q_, si

MJ_PER_KWH = 3.6

# Net calorific value of oven-dry wood, MJ/kg: FAO UBET (2004) Table 10, spruce 18.8, beech 18.4,
# poplar 18.5, willow 18.4, softwood bark 19.2; Forest Research's generic 19 (wood-fuel.md §1)
WOOD_NET_DRY_MJ_KG = (18.4, 19.2)
WOOD_NET_SOURCE = "FAO UBET 2004 Table 10; Forest Research (wood-fuel.md §1 [W2], [W3])"
# Air-dried wood holds 12–20 % water, wet basis (FAO UBET §5.1.2; wood-fuel.md §2)
AIR_DRY_MOISTURE = (0.12, 0.20)
EVAPORATION_MJ_KG = 2.44  # FAO UBET eq. 3 (wood-fuel.md §2)
# Oven-dry weight of a cord, lb: USU Extension "Wood Heating" Table 1 (wood-fuel.md §1 [W4]),
# Engelmann spruce 2,070 to white oak 4,200: "wood of any kind"
CORD_DRY_LB_ANY = (2070.0, 4200.0)
CORD_DRY_LB_PINE = (2250.0, 2610.0)  # white, ponderosa and lodgepole pine (the same table)
CORD_SOURCE = "USU Extension, Wood Heating, Table 1 (wood-fuel.md §1 [W4])"
# #2 diesel, 132,000–140,000 BTU/gal (Olsen, 4th ed. p.209)
DIESEL_BTU_GAL = (132_000.0, 140_000.0)
DIESEL_SOURCE = "Olsen, The Kiln Book, 4th ed., p.209"
# Wood pottery kilns measured: 12.4–21.6 % (Adubah 2026, 19 Ghanaian kilns) and 18.07 %
# (Jongpluempiti et al. 2015); the starting range for a cone-10 wood kiln 15–30 %
# (firebox-efficiency.md §2, §6)
WOOD_ETA_MEASURED = (0.124, 0.216)
WOOD_ETA_RANGE = (0.15, 0.30)
WOOD_ETA_SOURCE = "firebox-efficiency.md §2, §6 ([P1] Adubah 2026; [P2] Jongpluempiti 2015)"


@dataclass(frozen=True)
class FuelHeat:
    """A printed fuel as net heat, lowest to highest, in kWh, and how it was worked out."""

    low_kwh: float
    high_kwh: float
    how: str
    sources: tuple[str, ...]


def net_mj_per_kg_dry(moisture: float, dry_mj_kg: float) -> float:
    """Net heat per kg of oven-dry wood burnt at a wet-basis ``moisture``: H(w) ÷ (1 − w), with
    H(w) = H_dry·(1 − w) − 2.44·w (FAO UBET eq. 3)."""
    return dry_mj_kg - EVAPORATION_MJ_KG * moisture / (1 - moisture)


def net_mj_per_kg_as_fired(moisture: float, dry_mj_kg: float) -> float:
    """Net heat per kg of wood as fired: H(w) = H_dry·(1 − w) − 2.44·w (FAO UBET eq. 3)."""
    return dry_mj_kg * (1 - moisture) - EVAPORATION_MJ_KG * moisture


def wood_cords(cords: float, kind: str = "") -> FuelHeat:
    """Cords of air-dried wood as net heat: the cord's oven-dry weight (by species where the table
    has it) × the net heat per dry kg at 12–20 % moisture."""
    pine = "pine" in kind.lower()
    lb = CORD_DRY_LB_PINE if pine else CORD_DRY_LB_ANY
    kg = (si(Q_(lb[0], "lb"), "kg"), si(Q_(lb[1], "lb"), "kg"))
    low = cords * kg[0] * net_mj_per_kg_dry(AIR_DRY_MOISTURE[1], WOOD_NET_DRY_MJ_KG[0])
    high = cords * kg[1] * net_mj_per_kg_dry(AIR_DRY_MOISTURE[0], WOOD_NET_DRY_MJ_KG[1])
    return FuelHeat(
        low / MJ_PER_KWH,
        high / MJ_PER_KWH,
        f"{cords:g} cord × {lb[0]:,.0f}–{lb[1]:,.0f} lb oven-dry "
        f"({'pine' if pine else 'any species'}) × net heat per dry kg at 12–20 % moisture",
        (CORD_SOURCE, WOOD_NET_SOURCE),
    )


def wood_mass(kg: float) -> FuelHeat:
    """A weight of wood as fired (taken as air-dried, 12–20 % water) as net heat."""
    low = kg * net_mj_per_kg_as_fired(AIR_DRY_MOISTURE[1], WOOD_NET_DRY_MJ_KG[0])
    high = kg * net_mj_per_kg_as_fired(AIR_DRY_MOISTURE[0], WOOD_NET_DRY_MJ_KG[1])
    return FuelHeat(
        low / MJ_PER_KWH,
        high / MJ_PER_KWH,
        f"{kg:,.0f} kg as fired, taken as air-dried (12–20 % water)",
        (WOOD_NET_SOURCE,),
    )


def diesel(gallons: float) -> FuelHeat:
    """US gallons of #2 diesel at the book's 132,000–140,000 BTU/gal."""
    btu = (gallons * DIESEL_BTU_GAL[0], gallons * DIESEL_BTU_GAL[1])
    return FuelHeat(
        si(Q_(btu[0], "BTU"), "kWh"),
        si(Q_(btu[1], "BTU"), "kWh"),
        f"{gallons:g} gal × 132,000–140,000 BTU/gal",
        (DIESEL_SOURCE,),
    )


def fuel_heat(value: float, unit: str, fuel: str, kind: str = "") -> FuelHeat | str:
    """A printed amount of fuel as net heat, or the reason it can't be converted."""
    if fuel.startswith("wood"):
        if unit == "cord":
            return wood_cords(value, kind)
        if unit in {"ton", "tonne", "lb", "kg"}:
            return wood_mass(si(Q_(value, unit), "kg"))
        return (
            f"no sourced weight for a {unit} of wood (only cords and weights convert); "
            "left out (ADR 0009)"
        )
    if fuel.startswith("oil") and unit in {"gallon", "gal"}:
        return diesel(value)
    if fuel.startswith("coal"):
        return "no heating value for coal is sourced in docs/research; left out"
    return f"no sourced conversion for {fuel} in {unit}"
