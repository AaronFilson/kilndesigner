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
