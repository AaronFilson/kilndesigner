"""A corbelled vault or corbel arch: each course of the two walls stepped in over the opening
until what is left is narrow enough for one brick laid across it as a lintel.

The sources (curved-kilns.md, "Corbel overhang per course"):

- TMS 402's prescriptive corbel limits, as the Brick Industry Association's *Corbels* brief
  (August 2025, p.2–3) gives them: each course projects no more than the smaller of half the
  unit's nominal height and a third of the unit's or wythe's nominal thickness, and the whole
  corbel no more than half the wall's thickness (multi-wythe composite solid masonry). These are
  for non-loadbearing building masonry at ambient temperature: their use for a kiln's refractory
  at heat is an assumption, stated in the working.
- Rhodes, *Kilns* (1968), p.101–102: one brick as a lintel bridges an opening up to 6 in; a corbel
  arch is "not practical for openings more than about 18 inches across".
- Olsen, *The Kiln Book*, 4th ed., p.49: "Use the corbel arch to span up to 61cm (24in.)"; small
  kilns roofed with corbels are "not a good practice".

Spans past Olsen's 24 in are refused: no source gives a corbel past it. Past Rhodes's 18 in the
layout is given with a warning.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from kilndesigner.sheet import Check, Sheet
from kilndesigner.units import Q_, Quantity, si
from kilndesigner.working import Finding, Step

TMS = (
    "TMS 402 prescriptive corbels, per Brick Industry Association, Corbels (Brick Brief, Aug 2025) "
    "p.2–3, https://www.gobrick.com/media/file/BB%20Corbels_082025.pdf; curved-kilns.md"
)
RHODES = "Rhodes, Kilns (1968) p.101–102; door-headers.md [H10]"
OLSEN = "Olsen, The Kiln Book, 4th ed., p.49; curved-kilns.md"
LINTEL_IN = 6.0  # Rhodes: one brick bridges holes up to six inches across
OLSEN_IN = 24.0  # Olsen p.49: the corbel arch spans up to 24 in
RHODES_IN = 18.0  # Rhodes: not practical past about 18 in
AMBIENT = (
    "TMS 402's limits are for non-loadbearing building masonry at room temperature; no source "
    "gives a corbel limit for refractory at heat, so they are used here as they stand"
)


class CorbelRefusedError(ValueError):
    """A corbel the sources don't reach, with the reason."""


@dataclass(frozen=True)
class Corbel:
    """A corbel laid out over a clear span (in): ``courses`` stepped in from each side by ``step``
    each, leaving ``gap`` for the lintel brick."""

    span: float
    course: float
    wall: float
    step: float
    courses: int

    @property
    def projection(self) -> float:
        """Each side's whole projection (in)."""
        return self.courses * self.step

    @property
    def gap(self) -> float:
        """What the lintel brick bridges at the top (in)."""
        return self.span - 2 * self.projection

    @property
    def rise(self) -> float:
        """From the springing to the lintel's underside (in): the stepped courses."""
        return self.courses * self.course

    def section(self) -> list[tuple[float, float]]:
        """The inside outline across the opening, from the left springing to the right (in, x
        across from the left wall's face, z up from the springing): the steps, then the lintel."""
        left: list[tuple[float, float]] = [(0.0, 0.0)]
        for k in range(1, self.courses + 1):
            z = (k - 1) * self.course
            left += [(left[-1][0], z), ((k) * self.step, z)]
        left.append((self.projection, self.rise))
        left = [p for i, p in enumerate(left) if i == 0 or p != left[i - 1]]
        right = [(self.span - x, z) for x, z in reversed(left)]
        return left + right

    def sheet(self) -> Sheet:
        s = Sheet("corbel", "Corbel over the opening", reference=f"{TMS}; {RHODES}; {OLSEN}")
        s.given("S", "the clear span at the springing", Q_(self.span, "in"), source="the design")
        s.given("S_max", "the widest corbel arch", Q_(OLSEN_IN, "in"), source=OLSEN)
        s.require("S", "<=", "S_max")
        s.given("h", "the unit's nominal height, a course", Q_(self.course, "in"),
                source="the design")  # fmt: skip
        s.given("d", "the wall's nominal thickness (the wythe)", Q_(self.wall, "in"),
                source="the design")  # fmt: skip
        s.given("p", "each course's projection", Q_(self.step, "in"), source="the design")
        s.let("p_max", "the most one course may project", "min(h/2, d/3)", "in", source=TMS)
        s.require("p", "<=", "p_max")
        s.given("n", "courses stepped in on each side", float(self.courses))
        s.let("P", "each side's whole projection", "n*p", "in")
        s.let("P_max", "the most the whole corbel may project", "d/2", "in", source=TMS)
        s.require("P", "<=", "P_max")
        s.let("g", "left at the top for the lintel brick", "S - 2*P", "in")
        s.given("g_max", "the widest opening one brick bridges", Q_(LINTEL_IN, "in"),
                source=RHODES)  # fmt: skip
        s.require("g", "<=", "g_max")
        s.lever("p", Q_(0.125, "in"), Q_(4.5, "in"))
        return s

    def check(self) -> Check:
        return self.sheet().check()


def corbel(
    span: Quantity, course: Quantity, wall: Quantity, step: Quantity | None = None
) -> Corbel:
    """Lay out a corbel over ``span``: each course stepped in by ``step`` (by default the most
    TMS 402 allows, min(h/2, d/3)), as few courses as leave a gap one brick bridges (6 in, Rhodes).
    Refused past Olsen's 24 in, or where even the most each course and the whole corbel may project
    can't close the span to 6 in."""
    s, h, d = si(span, "in"), si(course, "in"), si(wall, "in")
    if min(s, h, d) <= 0:
        raise CorbelRefusedError("a corbel needs a span, a course height and a wall thickness")
    if s > OLSEN_IN:
        raise CorbelRefusedError(
            f"a corbel over {s:g} in is past the {OLSEN_IN:g} in Olsen gives for a corbel arch "
            f"(p.49), and no source gives one wider: use a sprung arch ({OLSEN})"
        )
    most = min(h / 2, d / 3)
    p = most if step is None else si(step, "in")
    if p <= 0:
        raise CorbelRefusedError("each course must step in by something")
    n = max(0, math.ceil((s - LINTEL_IN) / (2 * p) - 1e-9))
    return Corbel(s, h, d, p, n)


def corbel_working(c: Corbel) -> tuple[list[Step], list[Finding]]:
    """The corbel's layout and its checks, with the findings they raise."""
    check = c.check()
    findings: list[Finding] = []
    working = [
        Step(
            name="Corbel: courses stepped in",
            value=(
                f"{c.courses} course(s) a side, {c.step:.3g} in each, "
                f"{c.projection:.3g} in in all; a lintel brick over the {c.gap:.3g} in left, "
                f"{c.rise:.3g} in above the springing"
            ),
            formula="n = ⌈(S − g_max)/2p⌉, p ≤ min(h/2, d/3), n·p ≤ d/2, g = S − 2n·p ≤ 6 in",
            inputs={
                "span S": f"{c.span:g} in",
                "course h": f"{c.course:g} in",
                "wall d": f"{c.wall:g} in",
            },
            reference=f"{TMS}; {RHODES}",
            note=AMBIENT,
        )
    ]
    if check.status != "pass":
        findings.append(
            Finding.failed(
                check,
                "The corbel steps past what TMS 402 allows a course or the whole corbel, or leaves "
                "more than one brick bridges: thicken the wall, step less, or turn an arch.",
            )
        )
    if c.span > RHODES_IN:
        findings.append(
            Finding(
                level="info",
                message=(
                    f"A corbel over {c.span:g} in: Rhodes finds corbels impractical past about "
                    f"{RHODES_IN:g} in, Olsen allows {OLSEN_IN:g} in and calls corbelled kiln "
                    "roofs poor practice (structural instability, an uneven surface, erosion)."
                ),
                reference=f"{RHODES}; {OLSEN}",
            )
        )
    return working, findings


__all__ = ["Corbel", "CorbelRefusedError", "corbel", "corbel_working"]
