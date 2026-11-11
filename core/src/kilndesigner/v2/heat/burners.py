"""The heat input of venturi burners (ADR 0017 H11, decision 13): what a burner delivers at its
supply pressure, from the published ratings the engine's library holds (`data/gas.yaml`;
`combustion-and-masonry.md` §3.2 [S27]; Olsen p.222's MR-750 and MR-100 on natural gas).

Through one orifice a burner's output rises with √pressure (Olsen p.216): on a published curve the
ratings between its pressures are interpolated in √pressure, and a rating given with its pressure
carries to another by √(p/p_rated). That carry is refused where no source covers it: natural gas
above low pressure, 11 in. w.c. (Olsen p.215), and a library burner off its published range.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import cache
from importlib import resources
from typing import Any

import numpy as np
import yaml

from kilndesigner.units import si
from kilndesigner.working import Step

IN_WC_PER_PSI = 27.68  # in. w.c. per psi (water at 4 °C; the engine's gas module's)
LOW_PRESSURE_PSI = 11 / IN_WC_PER_PSI  # Olsen p.215: low pressure, 11 in. w.c. or less
SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.216 (output ∝ √pressure through one orifice), p.215 (low "
    "pressure, 11 in. w.c.), p.222 (MR-750, MR-100); Ward and GACO ratings, "
    "combustion-and-masonry.md §3.2 [S27]"
)


class BurnerError(ValueError):
    """A pressure or burner the published ratings don't cover (ADR 0009)."""


@dataclass(frozen=True)
class Curve:
    """A venturi burner's published propane ratings on one orifice: psi and BTU/hr."""

    model: str
    psi: tuple[float, ...]
    btu_hr: tuple[float, ...]
    natural_gas: tuple[float, float] | None  # (in. w.c., BTU/hr) when published

    def at(self, psi: float) -> float:
        """BTU/hr at a propane pressure within the curve, √pressure interpolated."""
        if not self.psi[0] <= psi <= self.psi[-1]:
            raise BurnerError(
                f"{self.model}: {psi:.2f} psi is outside its published {self.psi[0]:g}–"
                f"{self.psi[-1]:g} psi"
            )
        roots = np.sqrt(np.array(self.psi))
        return float(np.interp(math.sqrt(psi), roots, np.array(self.btu_hr)))

    def pressure_for(self, btu_hr: float) -> float:
        """The propane pressure (psi) that gives ``btu_hr``, within the curve."""
        if not self.btu_hr[0] <= btu_hr <= self.btu_hr[-1]:
            raise BurnerError(
                f"{self.model}: {btu_hr:,.0f} BTU/hr is outside its published "
                f"{self.btu_hr[0]:,.0f}–{self.btu_hr[-1]:,.0f}"
            )
        roots = np.sqrt(np.array(self.psi))
        return float(np.interp(btu_hr, np.array(self.btu_hr), roots)) ** 2


@cache
def _library() -> dict[str, Any]:
    text = resources.files("kilndesigner.data").joinpath("gas.yaml").read_text(encoding="utf-8")
    data: Any = yaml.safe_load(text)
    return data["venturi_burners"]["models"]


def curve(model: str) -> Curve:
    """A library burner's curve, from its lowest pressure on the √pressure curve up."""
    spec = _library().get(model)
    if spec is None:
        raise BurnerError(
            f"no published ratings for {model!r}; the library has {sorted(_library())}"
        )
    kept = [(p, r) for p, r in zip(spec["psi"], spec["btu_hr"], strict=True)
            if p >= spec["curve_from_psi"]]  # fmt: skip
    ng = spec.get("natural_gas")
    return Curve(
        model,
        tuple(float(p) for p, _ in kept),
        tuple(float(r) for _, r in kept),
        (float(ng["in_wc"]), float(ng["btu_hr"])) if ng else None,
    )


def carried(rating: float, rated_psi: float, psi: float, fuel: str) -> float:
    """A rating given at ``rated_psi`` carried to ``psi`` through the same orifice, by
    √(p/p_rated) (Olsen p.216); natural gas only within low pressure (p.215)."""
    if fuel == "natural_gas" and max(rated_psi, psi) > LOW_PRESSURE_PSI * (1 + 1e-9):
        raise BurnerError(
            f"natural gas at {max(rated_psi, psi) * IN_WC_PER_PSI:.0f} in. w.c.: the √pressure "
            "carry is cited for low pressure only, 11 in. w.c. or less (Olsen p.215–216)"
        )
    return rating * math.sqrt(psi / rated_psi)


@dataclass(frozen=True)
class Input:
    """What a design's burners give at their supply pressure (BTU/hr): each and all of them, and
    how it was read."""

    count: int
    each: float
    how: str
    steps: tuple[Step, ...] = ()

    @property
    def total(self) -> float:
        return self.count * self.each


def design_input(kiln: Any) -> Input:
    """The design's burners at its supply's pressure (ADR 0017 decision 13): a rating the design
    gives is each burner's input at that pressure (model.Burners.rating); a library burner on
    natural gas is its published rating at 8 in. w.c. carried by √(p/p_rated) within low pressure
    (Olsen p.215–216); on propane its published curve at the pressure (2–20 psi, one orifice),
    or its own published low-pressure rating at 11 in. w.c. (another orifice). Refused where no
    source gives it: no rating and no library burner, or no pressure (a tank or cylinders)."""
    g = kiln.heat.gas
    if g is None:
        raise BurnerError("the design has no gas burners")
    b = g.burners
    count = b.wanted
    if count is None:
        raise BurnerError("the design doesn't say how many burners")
    if b.rating is not None:
        each = si_btu(b.rating)
        how = f"the design's rating, {each:,.0f} BTU/hr each at its supply's pressure"
        return Input(count, each, how, (_step(count, each, how),))
    if b.model is None:
        raise BurnerError("no burner rating and no library burner: its input isn't sourced")
    if getattr(g.supply, "pressure", None) is None:
        raise BurnerError("the supply (a tank or cylinders) gives no pressure at the burners")
    psi = si(g.supply.pressure, "psi")
    c = curve(b.model)
    if g.fuel == "natural_gas":
        if c.natural_gas is None:
            raise BurnerError(f"{b.model}: no natural-gas rating published")
        in_wc, rating = c.natural_gas
        each = carried(rating, in_wc / IN_WC_PER_PSI, psi, "natural_gas")
        how = (f"{b.model}: {rating:,.0f} BTU/hr at {in_wc:g} in. w.c. on natural gas (Olsen "
               f"p.222), × √({psi * IN_WC_PER_PSI:.1f}/{in_wc:g})")  # fmt: skip
        return Input(count, each, how, (working(count, rating, in_wc / IN_WC_PER_PSI, psi,
                                                "natural_gas"),))  # fmt: skip
    spec = _library()[b.model]
    low = [(p, r) for p, r in zip(spec["psi"], spec["btu_hr"], strict=True)
           if p < spec["curve_from_psi"] and abs(p - psi) <= 0.01 * p]  # fmt: skip
    if low:
        each = float(low[0][1])
        how = (
            f"{b.model}: its published {each:,.0f} BTU/hr at {psi * IN_WC_PER_PSI:.0f} in. "
            "w.c. on propane (its low-pressure orifice, combustion-and-masonry.md §3.2)"
        )
    else:
        each = c.at(psi)
        how = f"{b.model}: {each:,.0f} BTU/hr at {psi:.2f} psi on its published propane curve"
    return Input(count, each, how, (_step(count, each, how),))


def si_btu(q: Any) -> float:
    """A power as BTU/hr."""
    return si(q, "BTU/hr")


def _step(count: int, each: float, how: str) -> Step:
    return Step(
        name="The burners' input",
        value=f"{count} × {each:,.0f} BTU/hr = {count * each:,.0f} BTU/hr",
        inputs={"each": how},
        reference=SOURCE,
    )


# --- Olsen's orifice equation (p.216) and Ward's tables (pp.230–233) ------------------------------

# Q = 1658.5·K·A·√(ΔP/d) ft³/hr (A in², ΔP in. w.c., d the gas's specific gravity), K 0.80 for
# good atmospheric orifices (p.216); BTU/hr = Q × the gas's heating value. Ward's tables are this
# with K 0.80 on natural gas at 1000 BTU/ft³, SG 0.64 (1.655×10⁶·A·√P), and on propane at 2,500
# BTU/ft³, SG 1.52 (2.683×10⁶·A·√P); Table 8-7 the same on propane and butane (2,500 at SG 1.53,
# 3,175 at SG 2.00); Fig 8-39 natural gas at 1,100 BTU/ft³, SG 0.65 (kiln-reference.md, Orifices)
ORIFICE_K = 0.80
GASES: dict[str, tuple[float, float, str]] = {
    "natural_gas": (1000.0, 0.64, "Ward's tables (Table 8-11, p.230)"),
    "natural_gas_1100": (1100.0, 0.65, "Fig 8-39 (p.217), Olsen's natural-gas chart"),
    "propane": (2500.0, 1.53, "Table 8-7 (pp.218–219)"),
    "butane": (3175.0, 2.00, "Table 8-7 (pp.218–219)"),
}
# Number drills (in): ASME B94.11M's standard sizes; Ward's orifice function for #38, 10,711.16 =
# 1.324×10⁶ × its area (Table 8-12, p.231), gives 0.1015 in (burner-inputs.md §2, Derived)
DRILL_IN = {18: 0.1695, 32: 0.1160, 34: 0.1110, 38: 0.1015, 45: 0.0820, 46: 0.0810, 50: 0.0700}
ORIFICE_SOURCE = (
    "Olsen p.216 (the orifice equation, K 0.80), Table 8-7 and Fig 8-39, Ward's Tables 8-11 to "
    "8-14 (pp.230–233); kiln-reference.md, Orifices; number drills ASME B94.11M"
)


def orifice(drill: int, in_wc: float, gas: str) -> float:
    """A number drill's orifice at ``in_wc`` (in. w.c.) on ``gas`` (BTU/hr): Olsen's orifice
    equation at K 0.80 (p.216). Low pressure only, where the gas doesn't compress (§3.4)."""
    if drill not in DRILL_IN:
        raise BurnerError(f"no size for a #{drill} drill here; the table has {sorted(DRILL_IN)}")
    if in_wc > 28.0:
        raise BurnerError(
            f"{in_wc:.0f} in. w.c.: the orifice equation is for low pressure (combustion-and-"
            "masonry.md §3.4: the gas compresses and chokes at psi pressures)"
        )
    hv, sg, _ = GASES[gas]
    area = math.pi * DRILL_IN[drill] ** 2 / 4
    return 1658.5 * ORIFICE_K * area * math.sqrt(in_wc / sg) * hv


def working(count: int, rating: float, rated_psi: float, psi: float, fuel: str) -> Step:
    each = carried(rating, rated_psi, psi, fuel)
    return Step(
        name="The burners' input",
        value=f"{count} × {each:,.0f} BTU/hr = {count * each:,.0f} BTU/hr",
        formula="Q = Q_rated·√(p/p_rated), one orifice",
        inputs={
            "rating": f"{rating:,.0f} BTU/hr at {rated_psi * IN_WC_PER_PSI:.1f} in. w.c.",
            "supply": f"{psi * IN_WC_PER_PSI:.1f} in. w.c. ({psi:.2f} psi)",
        },
        reference=SOURCE,
    )
