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
the nearest brick, and the tighter one makes up N. This reproduces Olsen's tables A-4 (arch
bricks) and A-6 (wedges) to within a brick of each shape and exactly in total (The Kiln Book, 4th
ed. p.303–305; kiln-reference.md, "Tables A-4 to A-7"), which the tests keep.

Shapes, 2½ in series (kiln-reference.md, "Brick sizes and shapes", p.21, p.298–302):

- arch bricks, 9 × 4½ × (2½ → t), taper along the 4½ in: a ring 4½ in deep;
- wedges, 9 × 4½ × (2½ → t), taper along the 9 in: a ring 9 in deep;
- keys, 9 × (4½ → t) × 2½, taper along the 9 in: a ring 9 in deep, the 4½ in face outside.

Olsen's bricks for curved walls (p.45): 4½ in, circle bricks (arch bricks possible but not
recommended); 9 in, key bricks, or circle and key bricks. Circle bricks' sizes are in his appendix
but not transcribed into docs/research, so they aren't offered here.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Literal

IN = 25.4  # mm
SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.21, p.45, p.303–305 (kiln-reference.md, Brick sizes and "
    "shapes; Walls, bonds and openings; Tables A-4 to A-7)"
)

DOWN = 0.1  # of a brick: rounded down below this (derived from tables A-4 and A-6, above)

type Series = Literal["arch", "wedge", "key"]


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
}  # fmt: skip


class RingError(ValueError):
    """The circle is tighter than the tightest shape turns on its own."""


@dataclass(frozen=True)
class Ring:
    series: Series
    inside_diameter: float  # mm
    counts: tuple[tuple[str, int], ...]  # shape and how many, tightest first

    @property
    def total(self) -> int:
        return sum(n for _, n in self.counts)

    def describe(self) -> str:
        return ", ".join(f"{n} {name}" for name, n in self.counts if n)


def ring(inside_diameter_mm: float, series: Series) -> Ring:
    """The bricks for one ring of the given inside diameter (mm)."""
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


def ring_series(depth_mm: float) -> Series | None:
    """The shapes Olsen gives for a round wall ring this deep (p.45): 9 in, keys; 4½ in, arch
    bricks (as circle bricks' sizes aren't transcribed). None for any other depth."""
    if abs(depth_mm - 9 * IN) < 1.0:
        return "key"
    if abs(depth_mm - 4.5 * IN) < 1.0:
        return "arch"
    return None


def wall_rings(thickness_mm: float) -> list[float] | None:
    """A round wall as rings of 9 and 4½ in, from the inside out, the 4½ in ring (if any) on the
    hot face; None if 9s and 4½s don't make the thickness."""
    halves = thickness_mm / (4.5 * IN)
    n = round(halves)
    if n < 1 or abs(halves - n) * 4.5 * IN >= 1.0:
        return None
    nines, half = divmod(n, 2)
    return [4.5 * IN] * half + [9 * IN] * nines
