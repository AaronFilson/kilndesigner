"""The masonry's and the bill of materials' checks as sheets (ADR 0013): a brick layer's thickness
in whole bricks, and the priced materials against the budget."""

from __future__ import annotations

from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_

SUMS = "whole 9, 4½ and 2½ in bricks side by side: a·9 + b·4½ + c·2½ in"


def whole_bricks(
    layer: str,
    thickness_mm: float,
    below_mm: float | None,
    above_mm: float,
    tolerance_mm: float,
    us: bool,
    source: str,
    sums: str = SUMS,
) -> Sheet:
    """A brick layer's thickness against the nearest thicknesses whole bricks make (``sums``
    says which: straight walls, or a round wall's rings)."""
    unit = "in" if us else "mm"
    s = Sheet("masonry.thickness", f"{layer} in whole bricks", reference=source)
    s.given("T", f"{layer}'s thickness", Q_(thickness_mm, "mm"), unit=unit, source="the design")
    if below_mm is not None:
        s.given(
            "T_below",
            "the next thickness whole bricks make, below",
            Q_(below_mm, "mm"),
            unit=unit,
            source=sums,
        )
    s.given(
        "T_above",
        "the next thickness whole bricks make, above",
        Q_(above_mm, "mm"),
        unit=unit,
        source=SUMS,
    )
    nearest = "abs(T_above - T)" if below_mm is None else "min(abs(T - T_below), abs(T_above - T))"
    s.let("Δ", "how far it is from one whole bricks make", nearest, unit)
    s.given(
        "Δ_max",
        "close enough to lay as whole bricks",
        Q_(tolerance_mm, "mm"),
        unit=unit,
        source="the course planner's tolerance",
    )
    s.require("Δ", "<", "Δ_max", level="warning")
    lo = below_mm if below_mm is not None else 0.001
    s.lever("T", Q_(lo, "mm"), Q_(above_mm, "mm"))
    return s


def within_budget(lines: list[tuple[str, float, str | None]], budget: float) -> Sheet:
    """Each priced line's cost (USD), their sum, and the design's budget."""
    s = Sheet("bom.budget", "The priced materials against the budget")
    for i, (item, cost, source) in enumerate(lines, 1):
        s.given(f"c_{i}", item, Q_(cost, "USD"), source=source)
    terms = " + ".join(f"c_{i}" for i in range(1, len(lines) + 1)) or "0*B"
    s.given("B", "the budget", Q_(budget, "USD"), source="the design: site.materials_budget")
    s.let("C", "the priced materials", terms, "USD")
    s.require("C", "<=", "B", level="warning")
    total = sum(cost for _, cost, _ in lines)
    s.lever("B", Q_(0, "USD"), Q_(2 * max(total, budget, 1.0), "USD"))
    return s


__all__ = ["whole_bricks", "within_budget"]
