"""The printed fuel of a reference kiln as heat, with the sources and the spread of each input.

Engine v2's validation (ADR 0017) compares the heat a model puts into a kiln with the
heat in the fuel the book says the kiln burned. These conversions are the book's side of that
comparison. Every number is sourced in ``docs/research/``; where none is, the fuel isn't converted
and the reason is returned instead.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from typing import Any, Literal

import reference as ref

from kilndesigner.units import Q_, si
from kilndesigner.v2.heat import gas

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
        return (
            "a coal's heating value is each kiln's (kiln-fuels.md §4), and a shovel's weight the "
            "owner's question (Taylor's 21 lb the only open figure): not converted here"
        )
    return f"no sourced conversion for {fuel} in {unit}"


# --- each kiln's own fuel for the heat model (ADR 0017 decision 12; kiln-fuels.md §5) ---------

# Which end of each band a fuel is built at: the least heat per kg as fired (the wettest, the
# lowest heating value), the bands' middles, or the most. The analysis is always at its middles.
type End = Literal["least", "mid", "most"]
# Singh's Grade B steam coal (kiln-fuels.md §4): its heating value is gross on the equilibrated
# basis, its ash and moisture together 19.6–23.9 % (UHV = 8900 − 138·(A + M), [F7] p.14); its
# moisture alone isn't printed: India's Barakar coals hold under 2 to 6 % ([F7] p.9), carried by
# analogy (an assumption, said)
GRADE_B_MOISTURE = (0.02, 0.06)
GRADE_B_ASH_AND_MOISTURE = (0.196, 0.239)
ANALYSIS = ("fuel_carbon", "fuel_hydrogen", "fuel_oxygen", "fuel_nitrogen", "fuel_sulphur",
            "fuel_ash")  # fmt: skip


def _band(f: dict[str, Any] | None, unit: str) -> tuple[float, float]:
    """A fuel fact as (low, high) in ``unit``; an upper bound ("<=") runs from zero; none is 0."""
    if f is None:
        return 0.0, 0.0
    lo, hi = ref.span(f, unit)
    return (0.0, hi) if f.get("bound") in ("<", "<=") else (lo, hi)


def _pick(band: tuple[float, float], end: End, wet: bool = False) -> float:
    """A band's end: ``least`` heat is its low end, or its high end for the moisture."""
    lo, hi = band
    if end == "mid":
        return (lo + hi) / 2
    return hi if (end == "least") == wet else lo


@cache
def _kilns() -> dict[str, Any]:
    """The dataset's kilns, read once."""
    return ref.load()["kilns"]


def own_intakes(kid: str) -> tuple[tuple[float, float], tuple[float, float]] | None:
    """A kiln's air intakes from the dataset (firebox-air-intakes.md §3), m², all its fireboxes
    together: below the grate and above it, each (least, most); None where neither is given (the
    dataset's gap); a side not given is closed (the least air, said by the caller)."""
    kiln = _kilns()[kid]
    below = ref.facts(kiln, "flow", "primary_air")
    above = ref.facts(kiln, "flow", "secondary_air")
    if not below and not above:
        return None

    def area(fs: list[dict[str, Any]]) -> tuple[float, float]:
        return ref.span(fs[0], "m**2") if fs else (0.0, 0.0)

    return area(below), area(above)


def own_fuels(kid: str, end: End = "mid") -> list[gas.Fuel]:
    """A reference kiln's fuels, from the dataset's facts (each `fuel_species` starts one: the
    Sturt kiln burns wood and drips oil), as the heat model takes them."""
    kiln = _kilns()[kid]
    groups: list[dict[str, dict[str, Any]]] = []
    for f in kiln.get("heat") or []:
        what = str(f.get("what"))
        if what == "fuel_species":
            groups.append({what: f})
        elif what.startswith("fuel_") and what not in ("fuel_kind", "fuel_rate") and groups:
            groups[-1][what] = f
    return [_fuel(kid, g, end) for g in groups if "fuel_heating_value" in g]


def _fuel(kid: str, g: dict[str, dict[str, Any]], end: End) -> gas.Fuel:
    species = str(g["fuel_species"]["value"])
    kind: gas.Solid = "oil" if "diesel" in species else "coal" if "coal" in species else "wood"
    parts = [(lo + hi) / 2 for lo, hi in (_band(g.get(a), "") for a in ANALYSIS)]
    net = _band(g["fuel_heating_value"], "J/kg")
    moisture = _pick(_band(g.get("fuel_moisture"), ""), end, wet=True)
    how = f"{kid}'s own fuel from the dataset (kiln-fuels.md §5), at the bands' {end}"
    if kid == "singh-coal":
        moisture = _pick(GRADE_B_MOISTURE, end, wet=True)
        parts[5] = sum(GRADE_B_ASH_AND_MOISTURE) / 2 - moisture
        gross_dry = _pick(net, end) / (1 - moisture)
        value = gas.net_from_gross(gross_dry, parts[1], parts[2], parts[3])
        how += "; Grade B's gross (equilibrated) to net dry by EN ISO 18125, its moisture assumed"
    else:
        value = _pick(net, end)
    c, h, o, n, s, ash = parts
    return gas.solid(species, kind, (c, h, o, n, s, ash), moisture, value, how)
