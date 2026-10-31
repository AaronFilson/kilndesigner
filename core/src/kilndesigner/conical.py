"""Conical (tatami) bricks: round, tapered bricks laid end-on, the narrow end at the hot face.

The Tamba tube kilns and the Kyoto climbing kilns arch their chambers and fireboxes with hand-made
bricks "made by being rolled in a Tatami mat" (Olsen, *The Kiln Book*, 4th ed., p.85, Fig. 4-6;
p.97, p.200). No source gives their size: they are custom, so the builder gives the length and
the two end diameters (the user, 2026-10-31).

Pure geometry, derived here (no rule of thumb):

- A ring of n bricks round a circle of inside radius r, each brick's axis radial: the narrow ends
  lie on r, the wide ends on r + L. Neighbours touch where the end circles meet, so the angle
  each brick takes is the larger of d / r (narrow ends) and D / (r + L) (wide ends).
- Both touch at once at the brick's own radius, r₀ = L·d / (D − d): there the ring closes with no
  joint. Larger, the wide ends touch and the narrow ends open a wedge joint of fireclay on the hot
  face; smaller, the narrow ends touch and the wide ends open outside.
- A dome course is the same ring on the sphere's radius; the courses step up the meridian by the
  same angle, so a dome of radius r₀ is close-packed both ways.
- A vault (a tube or chamber arch) curves one way only: along it the rows step by the wide end, D,
  and the narrow ends stand D − d apart on the hot face.

The engine shows the joints and leaves the call to the builder: no source gives a largest hot-face
joint for fireclay-set tatami bricks (Olsen p.94: "thick fireclay joints").
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from kilndesigner.model import ConicalBrick
from kilndesigner.units import si
from kilndesigner.working import Step

REF = "Olsen, The Kiln Book, 4th ed., p.85, Fig. 4-6; geometry derived in conical.py"


@dataclass(frozen=True)
class Brick:
    """A conical brick, inches: its length and its wide and narrow end diameters."""

    length: float
    wide: float
    narrow: float

    def __post_init__(self) -> None:
        if not (self.length > 0 and self.wide > self.narrow > 0):
            raise ValueError(
                "a conical brick has a length and a wide end wider than its narrow end"
            )

    @classmethod
    def of(cls, spec: ConicalBrick) -> Brick:
        """The design's brick, in inches."""
        return cls(si(spec.length, "in"), si(spec.wide, "in"), si(spec.narrow, "in"))

    @property
    def own_radius(self) -> float:
        """The inside radius (in) its ring closes on with no joint: L·d / (D − d)."""
        return self.length * self.narrow / (self.wide - self.narrow)


@dataclass(frozen=True)
class Course:
    """One ring of conical bricks round an inside radius, inches and radians."""

    brick: Brick
    radius: float  # inside, at the narrow ends
    angle: float  # each brick's share of the circle
    inside_joint: float  # between narrow ends, on the hot face
    outside_joint: float  # between wide ends

    def bricks(self, sweep: float) -> int:
        """Bricks to lay round ``sweep`` radians, the last one trimmed or the joints opened."""
        return math.ceil(sweep / self.angle - 1e-9)


def course(radius: float, brick: Brick) -> Course:
    """The ring of ``brick`` round an inside radius (in), its joints where the ends don't touch."""
    if radius <= 0:
        raise ValueError("a course needs a positive inside radius")
    outer = radius + brick.length
    angle = max(brick.narrow / radius, brick.wide / outer)
    return Course(brick, radius, angle, radius * angle - brick.narrow, outer * angle - brick.wide)


@dataclass(frozen=True)
class Vault:
    """A circular-segment arch of conical bricks along a run, inches."""

    span: float
    rise: float
    run: float
    radius: float
    sweep: float  # radians of arc
    course: Course
    per_row: int
    rows: int
    steps: tuple[Step, ...]

    @property
    def total(self) -> int:
        return self.per_row * self.rows

    @property
    def hot_face_brick(self) -> float:
        """The part of the hot face that is brick end, not fireclay: π d² / 4 per cell."""
        b = self.course.brick
        cell = (self.radius * self.course.angle) * b.wide
        return math.pi * b.narrow**2 / 4 / cell


def segment_radius(span: float, rise: float) -> tuple[float, float]:
    """The radius and the swept angle of a circular arch of this span and rise (rise ≤ span/2)."""
    if not (0 < rise <= span / 2 + 1e-9):
        raise ValueError("a circular arch rises more than nothing and at most half its span")
    radius = (span**2 / 4 + rise**2) / (2 * rise)
    return radius, 2 * math.asin(min(1.0, span / 2 / radius))


def vault(span: float, rise: float, run: float, brick: Brick) -> Vault:
    """The conical bricks for an arch of ``span`` and ``rise`` over a ``run`` of kiln (in)."""
    radius, sweep = segment_radius(span, rise)
    c = course(radius, brick)
    per_row = c.bricks(sweep)
    rows = math.ceil(run / brick.wide - 1e-9)

    def f(x: float) -> str:
        return f"{x:.3g} in"

    steps = (
        Step(
            name="Arch radius",
            formula="r = (S²/4 + h²) / 2h",
            inputs={"S": f(span), "h": f(rise)},
            value=f(radius),
            reference="circle geometry",
        ),
        Step(
            name="The brick's own radius",
            formula="r₀ = L·d / (D − d)",
            inputs={"L": f(brick.length), "D": f(brick.wide), "d": f(brick.narrow)},
            value=f(brick.own_radius),
            reference=REF,
            note="its ring closes with no joint here",
        ),
        Step(
            name="Each brick's angle",
            formula="θ = max(d / r, D / (r + L))",
            inputs={"r": f(radius)},
            value=f"{math.degrees(c.angle):.3g}°",
            reference=REF,
        ),
        Step(
            name="Hot-face joint between narrow ends",
            formula="r·θ − d",
            value=f(c.inside_joint),
            reference=REF,
            note="fireclay; no source gives a largest joint (Olsen p.94: thick fireclay joints)",
        ),
        Step(
            name="Bricks per row",
            formula="⌈φ / θ⌉, φ = 2·asin(S / 2r)",
            inputs={"φ": f"{math.degrees(sweep):.3g}°"},
            value=str(per_row),
            reference=REF,
        ),
        Step(
            name="Rows along the run",
            formula="⌈run / D⌉",
            inputs={"run": f(run)},
            value=str(rows),
            reference=REF,
            note="wide ends touching; the narrow ends stand D − d apart on the hot face",
        ),
    )
    return Vault(span, rise, run, radius, sweep, c, per_row, rows, steps)


def dome(radius: float, rise: float, brick: Brick) -> list[tuple[float, int]]:
    """A spherical dome of inside ``radius`` rising ``rise`` (in): each course's height of its
    narrow ends above the springing and its bricks, from the springing up to the crown, which a
    plug closes. Each course steps up the meridian by its brick's angle."""
    if not (0 < rise <= radius + 1e-9):
        raise ValueError("a spherical dome rises more than nothing and at most its radius")
    c = course(radius, brick)
    start = math.asin(max(0.0, (radius - rise) / radius))  # springing, up from the equator
    out: list[tuple[float, int]] = []
    lat = start + c.angle / 2
    while lat < math.pi / 2 - c.angle / 2 + 1e-9:
        # The course's circle is cos(lat) of the sphere's; each brick takes r·θ of it
        out.append(
            (
                radius * (math.sin(lat) - math.sin(start)),
                math.ceil(2 * math.pi * math.cos(lat) / c.angle - 1e-9),
            )
        )
        lat += c.angle
    return out
