"""A 9 in round dome counted by Norton's methods (Refractories, 3rd ed., 1949, pp.730–732;
blocked-items.md §18 [K25]).

Two ways, beside the course-by-course laying of conical.py:

- **Norton's ring count**, in standard 9 × 4½ × 2½ in straights, No. 1 wedges and No. 1 keys: "Most
  domes are built up in 2½-in. rings with combinations of straights and keys alternated with
  4½-in. rings of straights and wedges ... mortar must be used to fill the joints." His formulas
  (Fig. 417) are partly garbled in the scan; read here as: the outer area A = 2π(r_m + ½t)·h_m,
  r_m and h_m the mid-surface's radius and rise; the 9 in equivalents A / (4½ × 2½); the first
  ring's 9 in equivalents, its outer circumference ÷ 4½; its No. 1 keys, (outer − inner
  circumference) ÷ (4½ − 4); the rings, the outer arc spring to spring ÷ 2½; the No. 1 wedge
  rings, (outer − inner arc) ÷ (2½ − 1⅞). The wedges are the whole's share of wedge rings, and the
  keys the rest's share of keys in the first ring. θ, the angle the dome subtends spring to
  spring, is what reproduces his worked example (r = 120 in, t = 9 in, 60°): 90 equivalents and
  58 keys in the first ring, 54 rings, 15 wedge rings, 1,230 in all. This reading gives 90, 56.5,
  54, 15 and 1,202; his split of the 1,230 (342 wedges, 585 keys, 303 straights) isn't reproduced
  closer than 7 %, the step between being lost in the scan.
- **Radial dome brick** (Table 155): "special shapes having a large end of 4½ by 2½ in. and a taper
  such that a projection of their corners will pass through the center of curvature". The small
  end is the large end × r/(r + t), which gives every row of Table 155 (4 to 40 ft inside radius)
  within 0.01 in (formula over table: the table is the test); the count is the outer surface ÷
  the 4½ × 2½ in large end. Refused outside the table's 4 to 40 ft.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from kilndesigner.working import Step

REF = "Norton, Refractories, 3rd ed. (1949), pp.730–732, Fig. 417 (blocked-items.md §18 [K25])"
TABLE_REF = "Norton, Refractories, 3rd ed. (1949), p.731, Table 155 (blocked-items.md §18 [K25])"
FACE, COURSE = 4.5, 2.5  # in: a 9 in straight's end, 4½ round the ring and 2½ up the meridian
KEY, WEDGE = 4.0, 1.875  # in: the No. 1 key's and No. 1 wedge's small ends (rings.py)
DEPTH = 9.0
TABLE_RANGE = (48.0, 480.0)  # in: Table 155, 4 to 40 ft inside radius


@dataclass(frozen=True)
class CountedDome:
    """A dome's brick by kind (name, count), the straights first; what to tell the builder."""

    counts: tuple[tuple[str, int], ...]
    text: str
    steps: tuple[Step, ...]


def _f(x: float) -> str:
    return f"{x:.4g} in"


def _half_angle(radius: float, rise: float) -> float:
    if not (0 < rise <= radius + 1e-9):
        raise ValueError("a spherical dome rises more than nothing and at most its radius")
    return math.acos(max(-1.0, (radius - rise) / radius))


@dataclass(frozen=True)
class NortonCount:
    """Norton's ring count of a 9 in dome; the raw (unrounded) figures and the counts."""

    total: float  # 9 in equivalents
    first_ring: float
    first_keys: float
    rings: float
    wedge_rings: float
    wedges: int
    keys: int
    straights: int


def norton_count(radius: float, rise: float, depth: float = DEPTH) -> NortonCount:
    """Norton's ring count of a dome of inside ``radius`` rising ``rise`` (in), ``depth`` thick.
    Raises ValueError where his method doesn't reach: a dome not 9 in thick, or one so tight that
    No. 1 keys alone can't turn its rings (more keys than bricks in a ring)."""
    if abs(depth - DEPTH) > 0.05:
        raise ValueError("Norton's ring count is for a 9 in dome of standard brick")
    alpha = _half_angle(radius, rise)
    theta = 2 * alpha
    outer, mid = radius + depth, radius + depth / 2
    total = 2 * math.pi * outer * mid * (1 - math.cos(alpha)) / (FACE * COURSE)
    first = 2 * math.pi * outer * math.sin(alpha) / FACE
    keys1 = 2 * math.pi * depth * math.sin(alpha) / (FACE - KEY)
    rings = outer * theta / COURSE
    wedge_rings = depth * theta / (COURSE - WEDGE)
    if keys1 > first:
        raise ValueError(
            f"a {radius:.3g} in radius is too tight for No. 1 keys alone: a ring would need "
            f"{keys1:.0f} keys among {first:.0f} bricks"
        )
    n = math.ceil(total - 1e-9)
    wedges = round(n * wedge_rings / rings)
    keys = round((n - wedges) * keys1 / first)
    return NortonCount(total, first, keys1, rings, wedge_rings, wedges, keys, n - wedges - keys)


def norton_dome(radius: float, rise: float, depth: float, what: str = "Dome") -> CountedDome:
    """Norton's ring count of a 9 in dome, as the builder's counts and the working."""
    c = norton_count(radius, rise, depth)
    alpha = _half_angle(radius, rise)
    steps = (
        Step(
            name=f"{what}: Norton's dome, its angle",
            formula="θ = 2·acos((r − h) / r), spring to spring",
            inputs={"r": _f(radius), "h": _f(rise)},
            value=f"{math.degrees(2 * alpha):.3g}°",
            reference=REF,
            note="the reading of θ that reproduces Norton's worked example (r 120 in, 60°)",
        ),
        Step(
            name=f"{what}: Norton's 9 in equivalents",
            formula="A / (4½ × 2½), A = 2π(r_m + ½t)·h_m, h_m = r_m(1 − cos ½θ)",
            inputs={"t": _f(depth), "r_m": _f(radius + depth / 2)},
            value=f"{c.total:,.0f}",
            reference=REF,
            note="his worked example: 1,230; this reading of his formula gives 1,202",
        ),
        Step(
            name=f"{what}: Norton's first ring",
            formula="2π(r + t)·sin ½θ / 4½; No. 1 keys 2π·t·sin ½θ / (4½ − 4)",
            value=f"{c.first_ring:.0f} 9 in equivalents, {c.first_keys:.0f} No. 1 keys",
            reference=REF,
            note="his worked example: 90 and 58",
        ),
        Step(
            name=f"{what}: Norton's rings",
            formula="(r + t)·θ / 2½; No. 1 wedge rings t·θ / (2½ − 1⅞)",
            value=f"{c.rings:.0f} rings, {c.wedge_rings:.0f} of No. 1 wedges",
            reference=REF,
            note="his worked example: 54 and 15",
        ),
        Step(
            name=f"{what}: Norton's count",
            formula="wedges = N·(wedge rings / rings); keys = (N − wedges)·(keys / bricks in the "
            "first ring); straights the rest",
            value=f"{c.straights} straights, {c.wedges} No. 1 wedges, {c.keys} No. 1 keys",
            reference=REF,
            note="his worked example: 303, 342 and 585; the split's step is lost in the scan "
            "and this reading differs by up to 7 %",
        ),
    )
    text = (
        f"Norton's ring count, 2½ in rings of straights and No. 1 keys alternated with rings of "
        f"straights and No. 1 wedges, mortar filling the joints: {c.straights} straights, "
        f"{c.wedges} No. 1 wedges and {c.keys} No. 1 keys, about {round(c.rings)} rings, each "
        "self-supporting (Norton p.732)"
    )
    counts = (("straight", c.straights), ("No. 1 wedge", c.wedges), ("No. 1 key", c.keys))
    return CountedDome(counts, text, steps)


def radial_small_end(radius: float, depth: float = DEPTH) -> tuple[float, float]:
    """The radial dome brick's small end (in), round its ring and up the meridian: the 4½ × 2½
    in large end × r / (r + t), its corners projecting to the dome's centre."""
    k = radius / (radius + depth)
    return FACE * k, COURSE * k


def radial_dome(radius: float, rise: float, depth: float, what: str = "Dome") -> CountedDome:
    """A 9 in dome of Norton's radial dome brick (Table 155). Raises ValueError outside the
    table's 4 to 40 ft inside radius, or for a dome not 9 in thick."""
    if abs(depth - DEPTH) > 0.05:
        raise ValueError("Norton's radial dome brick is for a 9 in dome")
    lo, hi = TABLE_RANGE
    if not lo - 1e-6 <= radius <= hi + 1e-6:
        raise ValueError(f"a {radius / 12:.3g} ft inside radius is outside Table 155's 4 to 40 ft")
    alpha = _half_angle(radius, rise)
    outer = radius + depth
    area = 2 * math.pi * outer * outer * (1 - math.cos(alpha))
    n = math.ceil(area / (FACE * COURSE) - 1e-9)
    w, t = radial_small_end(radius, depth)
    shape = f"radial dome brick, {w:.2f} × {t:.2f} in small end"
    steps = (
        Step(
            name=f"{what}: radial dome brick's small end",
            formula="4½ × 2½ in × r / (r + t)",
            inputs={"r": _f(radius), "t": _f(depth)},
            value=f"{w:.2f} × {t:.2f} in",
            reference=TABLE_REF,
            note="the corners project to the dome's centre; gives Table 155's rows within 0.01 in",
        ),
        Step(
            name=f"{what}: radial dome brick",
            formula="n = 2π(r + t)²(1 − cos ½θ) / (4½ × 2½)",
            value=str(n),
            reference=TABLE_REF,
            note="near the crown even these won't fit unless hand cut (Norton p.731)",
        ),
    )
    text = (
        f"{n} radial dome brick, 9 in long, 4½ × 2½ in at the large end and {w:.2f} × {t:.2f} in "
        "at the small (Norton's Table 155: or insulating firebrick ground to it), strictly radial "
        "joints; near the crown they're hand cut"
    )
    return CountedDome(((shape, n),), text, steps)
