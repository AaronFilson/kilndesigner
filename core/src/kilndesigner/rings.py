"""Bricks to turn a circle: one ring of a round wall, or of an arch, from tapered shapes.

Every brick in a ring shows its thick end, T, on the outside circle and its thin end, t, on the
inside; a straight has t = T. A ring of inside diameter D and radial depth L takes

    N = π (D + 2L) / T          bricks round the outside, and
    Σ nᵢ tᵢ = π D               round the inside.

Two neighbouring shapes, a tighter one (t₁) and a gentler one (t₂), share the ring:

    n₂ = (π D − N t₁) / (t₂ − t₁),   n₁ = N − n₂.

The pair is the tightest two whose n₁ and n₂ both come out at zero or more; beyond the gentlest
taper, the gentlest is mixed with straights. The book doesn't say how it rounds N; its tables
round a fraction of a brick of 0.097 or less down (A-4 at 3'6", 0.088; A-6 at 6'0", 0.097) and
one of 0.106 or more up (A-4 at 7", 0.106). So N is rounded down within 0.1 of a brick and up
otherwise: derived from the tables, not stated by them. The gentler shape's count is rounded to
the nearest brick, and the tighter one makes up N. This reproduces Olsen's tables A-4 to A-7
(arch bricks and wedges, 2½ and 3 in series) to within a brick of each shape and exactly in
total (The Kiln Book, 4th ed. p.303–305; kiln-reference.md, "Tables A-4 to A-7"), which the
tests keep.

Shapes, 2½ in series (kiln-reference.md, "Brick sizes and shapes", p.21, p.298–302):

- arch bricks, 9 × 4½ × (2½ → t), taper along the 4½ in: a ring 4½ in deep;
- wedges, 9 × 4½ × (2½ → t), taper along the 9 in: a ring 9 in deep;
- keys, 9 × (4½ → t) × 2½, taper along the 9 in: a ring 9 in deep, the 4½ in face outside.

Olsen's bricks for curved walls (p.45): 4½ in, circle bricks (arch bricks possible but not
recommended); 9 in, key bricks, or circle and key bricks. His appendix has no circle-brick table,
and round face brick is little used (the user, a kiln builder, 2026-10-30), so a 4½ in ring is
turned one of four ways, the builder's choice:

- **mortar**: straights laid flat as stretchers, 9 in round the ring, 4½ in through, 2½ in
  courses, their inside faces on the curve and the wedge-shaped joints behind filled with mortar,
  as Olsen draws a curved wall (Fig. 2-13, p.45). Each brick's inside face is a 9 in chord of the
  inside circle, turning θ = 2·asin(L/D); n = ⌊2π/θ⌋ whole bricks and one closer cut to the
  chord 2·r·sin(φ/2) of the angle φ = 2π − nθ left. Two bricks meeting at their inside corners
  open a joint 2·d·sin(α/2) wide at the outside, α the angle between them; the joints' mortar is
  Σ ½·d²·sin α per course height.
- **cut**: straights laid as above, each cut at both ends to the angle θ_o/2 off square so the
  ring closes with no wedge joints, the norm in electric kilns (the user). θ_o is the angle a
  9 in chord of the outside circle turns: the bricks keep their full 9 in outside face, and an
  electric kiln is sized to a whole number of them, 6, 8, 10, 12 bricks round (the user). A
  diameter that isn't takes ⌊2π/θ_o⌋ full bricks and a closer cut to what is left, and is
  warned of, with the diameters whole bricks give.
- **featheredge**: straights on end with featheredges among them, 9 × 4½ × (2½ → ⅛) in
  (HarbisonWalker's 2½ in series, kiln-hardware.md §5.1 [S20]), laid as arch bricks are: the
  same tapered ring above, with the featheredge the one taper (the user names the method).
- **arch**: arch bricks on end, Olsen's fallback.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, replace
from typing import Literal

IN = 25.4  # mm
SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.21, p.45, p.303–305 (kiln-reference.md, Brick sizes and "
    "shapes; Walls, bonds and openings; Tables A-4 to A-7)"
)

DOWN = 0.1  # of a brick: rounded down below this (derived from tables A-4 and A-6, above)

type Series = Literal[
    "arch", "wedge", "key", "arch3", "wedge3", "featheredge", "mortar", "cut", "cut2.5", "cut3"
]
type Method = Literal["mortar", "cut", "featheredge", "arch"]
STRAIGHT = 9.0  # in, a straight's length
FEATHEREDGE_SOURCE = (
    "HarbisonWalker featheredge, 9 × 4½ × (2½ − ⅛) in (kiln-hardware.md §5.1 [S20]); straights "
    "with featheredges, and straights cut to the angle, the norm in electric kilns (the user, a "
    "kiln builder, 2026-10-30)"
)
MORTAR_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.45, Fig. 2-13: straights on the curve, their joints opening "
    "toward the outside"
)


@dataclass(frozen=True)
class Taper:
    name: str
    thin: float  # in, the thin end, on the inside of the ring


@dataclass(frozen=True)
class Family:
    thick: float  # in, each brick's face on the outside of the ring
    depth: float  # in, through the ring
    height: float  # in, the course height in a wall (the brick's third dimension)
    tapers: tuple[Taper, ...]  # tightest first
    straight: str


FAMILIES: dict[Series, Family] = {
    # Arch bricks in a wall stand on end: 4½ in through, 2½ in round the ring, 9 in high
    "arch": Family(
        2.5, 4.5, 9.0,
        (Taper("No. 3 arch", 1.0), Taper("No. 2 arch", 1.75), Taper("No. 1 arch", 2.125)),
        "straight",
    ),
    "wedge": Family(
        2.5, 9.0, 4.5,
        (Taper("No. 2 wedge", 1.5), Taper("No. 1 wedge", 1.875)),
        "straight",
    ),
    # Keys lie flat: 9 in through, 4½ in round the outside, 2½ in courses
    "key": Family(
        4.5, 9.0, 2.5,
        (Taper("No. 4 key", 2.25), Taper("No. 3 key", 3.0), Taper("No. 2 key", 3.5),
         Taper("No. 1 key", 4.0)),
        "straight laid through the wall",
    ),
    # 3 in series (9 × 4½ × 3 in), tables A-5 and A-7. The book's shape page for this series is
    # cut off or faint (p.22), so the thin ends are derived from the tables' single-shape rows:
    # A-5 at 1'6", 29 No.3 arch round π × 18 in → 1.95 ≈ 2 in; at 3'9", 57 No.2 round π × 45 in
    # → 2.48 ≈ 2½ in; at 6'0", 28 No.2 and 57 No.1 round π × 72 in → 2.74 ≈ 2¾ in. A-7 at 3'0",
    # 57 No.3 wedges round π × 36 in → 1.98 ≈ 2 in; at 4'6", 38 + 38 → No.2 2.46 ≈ 2½ in. These
    # agree with the faint "No.2 (3–2½)" on p.22 and the (3–2) No.3 arch there.
    "arch3": Family(
        3.0, 4.5, 9.0,
        (Taper("No. 3 arch, 3 in series", 2.0), Taper("No. 2 arch, 3 in series", 2.5),
         Taper("No. 1 arch, 3 in series", 2.75)),
        "3 in straight",
    ),
    "wedge3": Family(
        3.0, 9.0, 4.5,
        (Taper("No. 3 wedge, 3 in series", 2.0), Taper("No. 2 wedge, 3 in series", 2.5)),
        "3 in straight",
    ),
    # On end as arch bricks are: 4½ in through, 2½ in round the outside, 9 in courses
    "featheredge": Family(2.5, 4.5, 9.0, (Taper("featheredge", 0.125),), "straight"),
    # Straights laid flat as stretchers: 9 in round the ring, 4½ in through, 2½ in courses
    "mortar": Family(9.0, 4.5, 2.5, (), "straight laid flat"),
    "cut": Family(9.0, 4.5, 2.5, (), "straight cut to the angle"),
    # Electric kilns' walls: 2½ or 3 in brick through, laid flat on the 4½ in face, 9 in round
    # the outside, 4½ in courses (Skutt KM-1227-3, L&L e23T-3; electric-kiln-survey.md)
    "cut2.5": Family(9.0, 2.5, 4.5, (), "straight cut to the angle"),
    "cut3": Family(9.0, 3.0, 4.5, (), "straight cut to the angle"),
}  # fmt: skip
CLOSER = "closer, a straight cut short"


class RingError(ValueError):
    """The circle is tighter than the tightest shape turns on its own."""


@dataclass(frozen=True)
class Ring:
    series: Series
    inside_diameter: float  # mm
    counts: tuple[tuple[str, int], ...]  # shape and how many, tightest first
    # Straight rings (mortar, cut), mm and degrees
    length: float | None = None  # the closer's face: mortar, inside; cut, outside
    joint: float | None = None  # mortar: the widest joint at the outside
    mortar: float | None = None  # mortar: the wedge joints' mortar per mm of course height, mm²
    angle: float | None = None  # cut: each end cut off square by this

    @property
    def total(self) -> int:
        return sum(n for _, n in self.counts)

    def describe(self) -> str:
        return ", ".join(f"{n} {name}" for name, n in self.counts if n)


def ring(inside_diameter_mm: float, series: Series) -> Ring:
    """The bricks for one ring of the given inside diameter (mm)."""
    if series in ("mortar", "cut", "cut2.5", "cut3"):
        method = "mortar" if series == "mortar" else "cut"
        return replace(
            straight_ring(inside_diameter_mm, method, FAMILIES[series].depth * IN), series=series
        )
    f = FAMILIES[series]
    d = inside_diameter_mm / IN
    exact = math.pi * (d + 2 * f.depth) / f.thick
    inner = math.pi * d
    total = math.ceil(exact - DOWN)
    shapes = [*f.tapers, Taper(f.straight, f.thick)]
    tightest = shapes[0]
    if inner < exact * tightest.thin - 1e-6:
        raise RingError(
            f"a {d:.3g} in circle is tighter than {tightest.name} bricks turn on their own "
            f"(their {f.depth:g} in ring is at least "
            f"{2 * f.depth * tightest.thin / (f.thick - tightest.thin):.3g} in across inside)"
        )
    for tight, gentle in itertools.pairwise(shapes):
        n_gentle = (inner - exact * tight.thin) / (gentle.thin - tight.thin)
        if n_gentle <= exact + 1e-6:
            g = min(total, round(n_gentle))
            return Ring(series, inside_diameter_mm, ((tight.name, total - g), (gentle.name, g)))
    raise AssertionError("the straights' pair always fits: they make up any larger circle")


CUT_SLACK = 1 / 16  # in round the outside: a ring this near whole bricks is laid whole (the user)


def cut_count(n: float) -> tuple[int, bool]:
    """The full bricks a cut ring lays for ``n`` round its outside, and whether that's whole: the
    nearest whole number when it is within 1/16 in of it round the ring, else the fewest, n
    rounded down, with a closer (the user, a kiln builder, 2026-10-30: whole bricks, or the
    fewest and a closer when a size is needed; 1/16 in for near enough, dry-laid)."""
    near = round(n)
    if abs(n - near) * STRAIGHT <= CUT_SLACK and near >= 3:
        return near, True
    return math.floor(n), False


def nominal_diameter(bricks: float, depth_mm: float) -> float:
    """A cut ring's inside diameter as makers quote it (mm): the mean of its inside flat-to-flat
    and corner-to-corner widths, for ``bricks`` full 9 in faces round the outside and walls
    ``depth_mm`` thick. The outside apothem is 4½ / tan(π/N), the inside one that less the wall.
    Skutt's KM-1227-3 sheet, 12 sides of 3 in brick, prints 28.00 in; this gives 28.07 in
    (electric-kiln-survey.md, derived)."""
    half = math.pi / bricks
    inner = STRAIGHT * IN / 2 / math.tan(half) - depth_mm
    return inner * (1 + 1 / math.cos(half))


def inside_apothem(inside_diameter_mm: float, sides: float) -> float:
    """A cut ring's inside apothem (mm), the centre to the middle of a flat, from its diameter as
    makers quote it, the mean of flats and corners: D = a·(1 + 1/cos(π/N))."""
    return inside_diameter_mm / (1 + 1 / math.cos(math.pi / sides))


def cut_facets(inside_diameter_mm: float, depth_mm: float) -> int | None:
    """The facets of a cut ring of whole bricks round, or None when it takes a closer."""
    n, whole = cut_count(cut_bricks(inside_diameter_mm, depth_mm))
    return n if whole else None


def cut_bricks(inside_diameter_mm: float, depth_mm: float = 4.5 * IN) -> float:
    """How many full 9 in straights, cut to the angle, turn a ring of this inside diameter (as
    makers quote it, nominal_diameter) and depth: N solved from nominal_diameter(N) = D, by
    bisection (it grows with N). Electric kilns are built to a whole number of them, 6, 8, 10,
    12 bricks round (the user, a kiln builder, 2026-10-30)."""
    lo, hi = 3.0, 400.0
    if nominal_diameter(lo, depth_mm) >= inside_diameter_mm:
        return lo
    for _ in range(80):
        mid = (lo + hi) / 2
        if nominal_diameter(mid, depth_mm) < inside_diameter_mm:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def cut_diameter(bricks: int, depth_mm: float = 4.5 * IN) -> float:
    """The inside diameter (mm) that ``bricks`` full straights cut to the angle turn exactly."""
    return nominal_diameter(bricks, depth_mm)


def straight_ring(inside_diameter_mm: float, method: Literal["mortar", "cut"],
                  depth_mm: float | None = None) -> Ring:  # fmt: skip
    """A ring of straights laid flat: with wedge joints of mortar, or cut to the angle."""
    f = FAMILIES[method]
    r, d, length = inside_diameter_mm / 2, f.depth * IN, STRAIGHT * IN
    if method == "cut":
        d = depth_mm if depth_mm is not None else d
        exact = cut_bricks(inside_diameter_mm, d)
        n, whole = cut_count(exact)
        # Each end of a brick in an N-sided ring is cut 180/N degrees off square; a closer takes
        # the part of a brick left over, along the outside
        closer = None if whole else (exact - n) * length
        counts = ((f.straight, n),) + (((CLOSER, 1),) if closer is not None else ())
        return Ring(
            method, inside_diameter_mm, counts, length=closer, angle=180 / (n if whole else exact)
        )
    if length > 2 * r:
        raise RingError(
            f"a {inside_diameter_mm / IN:.3g} in circle is narrower than a 9 in straight, so "
            "straights can't follow it: cut them to the angle, or use featheredges"
        )
    theta = 2 * math.asin(length / (2 * r))
    n = math.floor(2 * math.pi / theta + 1e-9)
    rest = 2 * math.pi - n * theta
    if rest < 1e-6:
        angles, closer = [theta] * n, None
    else:
        # The closer's two joints each turn half its angle and half a whole brick's
        angles, closer = [theta] * (n - 1) + [(theta + rest) / 2] * 2, 2 * r * math.sin(rest / 2)
    counts = ((f.straight, n),) + (((CLOSER, 1),) if closer is not None else ())
    return Ring(
        method, inside_diameter_mm, counts, length=closer,
        joint=max(2 * d * math.sin(a / 2) for a in angles),
        mortar=sum(0.5 * d * d * math.sin(a) for a in angles),
    )  # fmt: skip


def ring_series(depth_mm: float, method: Method = "arch") -> Series | None:
    """The shapes for a round wall ring this deep (p.45): 9 in, keys; 4½ in, as ``method`` says.
    None for any other depth."""
    if abs(depth_mm - 9 * IN) < 1.0:
        return "key"
    if abs(depth_mm - 4.5 * IN) < 1.0:
        return method
    if method == "cut":
        for series in ("cut2.5", "cut3"):
            if abs(depth_mm - FAMILIES[series].depth * IN) < 1.0:
                return series
    return None


def ring_method(kiln_rings: Method | None, electric: bool) -> Method:
    """The 4½ in ring's method: the design's, or cut for an electric kiln and mortar otherwise."""
    if kiln_rings is not None:
        return kiln_rings
    return "cut" if electric else "mortar"


def wall_rings(thickness_mm: float, method: Method = "arch") -> list[float] | None:
    """A round wall as rings of 9 and 4½ in, from the inside out, the 4½ in ring (if any) on the
    hot face; or, cut to the angle, one ring of 2½ or 3 in brick, as electric kilns are. None if
    those don't make the thickness."""
    if method == "cut" and any(abs(thickness_mm - t * IN) < 1.0 for t in (2.5, 3.0)):
        return [thickness_mm]
    halves = thickness_mm / (4.5 * IN)
    n = round(halves)
    if n < 1 or abs(halves - n) * 4.5 * IN >= 1.0:
        return None
    nines, half = divmod(n, 2)
    return [4.5 * IN] * half + [9 * IN] * nines
