"""λ through a firing (ADR 0017 decision 9, H11): the air the draft draws through the fireboxes'
intakes against the fuel the stoker burns, and the fuel bed's most.

**The stream after the fire at any λ.** The zone model carries the products at one λ (`gas.py`,
per kg of fuel). With more air than that, the stream is those products with the excess air mixed
in unreacted; Cantera's own equilibrium at the leaner λ releases within 0.15 % of the net heat
of this at 1500 K for λ up to 2, and within 0.9 % at 1900 K up to λ 3 (Derived:
`test_heat_air.py` checks it), the gap the dissociation a leaner gas suppresses. With less air
(reduction), the products at the stream's own λ, between Cantera's tables at λ 0.8, 0.85, 0.9,
0.95 and 1, their CO and H₂ holding heat that isn't released (H4); below 0.8, past the range
checked, the products are held at 0.8 and the firing says so (`gas.LAMBDA_MIN`).

**The fuel bed.** Coal on a hand-fired grate burns 85–200 kg/(m²·h) as fired at the drafts of
natural-draft kilns and boilers (`grates-and-fuel-beds.md`: Norsker's 85–145 in potters' kilns,
Gebhardt's Table 29 to 200 at 0.5 in of draft); the stoker can't burn more on the grate whatever
the air. No source gives a burning rate for wood logs on a hand-fired grate: wood is limited by
the draft's air alone (said).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from kilndesigner.v2.heat import gas

REDUCTION = (0.8, 0.85, 0.9, 0.95, 1.0)  # λ: the tables below 1
COAL_BED = (85.0 / 3600, 200.0 / 3600)  # kg/(m²·s) as fired (grates-and-fuel-beds.md)
COAL_BED_REFERENCE = (
    "grates-and-fuel-beds.md: coal on hand-fired grates 85–145 kg/(m²·h) in potters' kilns "
    "(Norsker 1987 §2.3.4), to 200 at 0.5 in of draft (Gebhardt 1917 Table 29)"
)
WOOD_BED_NOTE = (
    "no source gives a burning rate for wood logs on a hand-fired grate "
    "(grates-and-fuel-beds.md): the wood is limited by the draft's air alone"
)
MIXING_NOTE = (
    "λ above the products' own: the excess air mixed in unreacted (within 0.15 % of the net heat "
    "of Cantera's equilibrium at 1500 K to λ 2); below it, Cantera's products at the stream's own "
    "λ, held at 0.8, the least checked"
)


@dataclass(frozen=True)
class Burnt:
    """The enthalpy flow (W) the burning zone's stream carries out at its temperature, and the
    stream's λ (held at 0.8 below it, said by ``held``)."""

    flow: float
    lam: float
    held: bool = False


def burnt(p: gas.Products, fuel: float, air: float, t: float) -> Burnt:
    """The stream of ``fuel`` (kg/s, dry) burnt with ``air`` (kg/s) leaving at ``t`` (K). With
    no air short of the products' λ the flow is linear in both (so a solver's iterate may pass
    through no fuel at all)."""
    excess = air - fuel * p.air
    if excess >= 0 or fuel <= 0:
        lam = p.air_ratio * air / (fuel * p.air) if fuel > 0 else math.inf
        return Burnt(fuel * p.mass * p.h(t) + excess * p.h_air(t), lam)
    lam = p.air_ratio * air / (fuel * p.air)
    held = lam < REDUCTION[0]
    at = max(lam, REDUCTION[0])
    grid = [x for x in REDUCTION if x < p.air_ratio] + [p.air_ratio]
    i = int(np.searchsorted(grid, at, side="right")) - 1
    i = min(max(i, 0), len(grid) - 2)
    lo, hi = grid[i], grid[i + 1]
    p_lo = gas.products(p.fuel, lo, p.t_air)
    w = (at - lo) / (hi - lo)
    h = (1 - w) * p_lo.mass * p_lo.h(t) + w * _table(p, hi).mass * _table(p, hi).h(t)
    return Burnt(fuel * h, lam, held)


def _table(p: gas.Products, lam: float) -> gas.Products:
    return p if math.isclose(lam, p.air_ratio) else gas.products(p.fuel, lam, p.t_air)


def bed_most(fuel: gas.Fuel, grate_area: float, rate: float) -> float:
    """The most dry fuel (kg/s) the grates burn at a bed rate (kg/(m²·s) as fired)."""
    return rate * grate_area * (1 - fuel.moisture)
