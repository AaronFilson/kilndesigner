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
from collections.abc import Callable
from dataclasses import dataclass

from kilndesigner.model import ConicalBrick
from kilndesigner.units import Quantity, si
from kilndesigner.working import Step

REF = "Olsen, The Kiln Book, 4th ed., p.85, Fig. 4-6; geometry derived in conical.py"

# Fig. 4-6's brick, measured on the page image at 400 dpi (2026-10-31): 625 px long, its wide end
# 260 px and its narrow end 175 px across, the taper real, as drawn (the user). Its spiral groove
# runs at about 57° to the axis (scaled from the figure: 140 px across for 90 px along), so its
# path is the run along the axis ÷ cos 57°.
FIG_4_6 = {"length/wide": 625 / 260, "wide/narrow": 260 / 175}
GROOVE_PATH = 1 / math.cos(math.atan2(140, 90))  # path per unit of axial run
# The user's estimates (2026-10-31): a ¾ in bore and a ¾ in half-round groove, each running ¾ of
# the way from the wide end
BORE, GROOVE, REACH = 0.75, 0.75, 0.75


@dataclass(frozen=True)
class Brick:
    """A conical brick, inches: its length and its wide and narrow end diameters."""

    length: float
    wide: float
    narrow: float
    bore: float = 0.0  # the hole along the axis, ¾ of the way in from the wide end
    groove: float = 0.0  # the half-round spiral groove's width, ¾ of the way down

    def __post_init__(self) -> None:
        if not (self.length > 0 and self.wide > self.narrow > 0):
            raise ValueError(
                "a conical brick has a length and a wide end wider than its narrow end"
            )
        if not 0 <= self.bore < self.narrow:
            raise ValueError("a conical brick's bore is narrower than its narrow end")
        if not 0 <= self.groove < self.narrow:
            raise ValueError("a conical brick's groove is narrower than its narrow end")

    @classmethod
    def of(cls, spec: ConicalBrick) -> Brick:
        """The design's brick, in inches."""
        length = si(spec.length, "in")
        if spec.proportions == "fig-4-6":
            return cls.fig_4_6(length)

        def opt(q: Quantity | None) -> float:
            return 0.0 if q is None else si(q, "in")

        return cls(
            length, si(spec.wide, "in"), si(spec.narrow, "in"), opt(spec.bore), opt(spec.groove)
        )

    @classmethod
    def fig_4_6(cls, length: float) -> Brick:
        """Olsen's drawn brick (p.85, Fig. 4-6) at this length: its ends scaled from the figure
        (FIG_4_6), the taper real, as drawn; the user's ¾ in bore and groove."""
        wide = length / FIG_4_6["length/wide"]
        return cls(length, wide, wide / FIG_4_6["wide/narrow"], BORE, GROOVE)

    @property
    def volume(self) -> float:
        """Its fired clay, in³: the frustum π·L·(D² + D·d + d²) / 12, less the bore π·b²·¾L / 4
        and the half-round groove π·g²/8 along its spiral, ¾L ÷ cos 57°."""
        d2 = self.wide**2 + self.wide * self.narrow + self.narrow**2
        run = REACH * self.length
        bore = math.pi * self.bore**2 / 4 * run
        groove = math.pi * self.groove**2 / 8 * run * GROOVE_PATH
        return math.pi * self.length * d2 / 12 - bore - groove

    def narrow_for(self, radius: float) -> float:
        """The narrow end (in) that would close a ring of this inside radius with no joint, the
        length and the wide end kept: d = D·r / (r + L)."""
        return self.wide * radius / (radius + self.length)

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
    laid = lay_conical_dome(radius, rise, brick)
    return [(c.height, c.bricks) for c in laid.courses]


STRAIGHTS_REF = (
    "Olsen, The Kiln Book, 4th ed., p.51 (a dome is part of one sphere; standard bricks laid in "
    "header or stretcher courses, each pitched to the dome's radius by Hendo's gauge, Fig. 2-28A) "
    "and p.45 (straights round a curve, their inside faces touching, the wedge joints behind "
    "filled with mortar, Fig. 2-13); geometry derived in conical.py"
)


@dataclass(frozen=True)
class DomeCourse:
    """One horizontal course of a dome, inches: the height of its hot face's middle above the
    springing, the ring's inside diameter there, and its bricks."""

    height: float
    across: float
    bricks: int


@dataclass(frozen=True)
class DomeLaying:
    """A dome laid course by course from the springing to the crown, its plug's opening left."""

    courses: tuple[DomeCourse, ...]
    crown: float  # in, across the opening above the top course, closed by a plug
    steps: tuple[Step, ...]

    @property
    def total(self) -> int:
        return sum(c.bricks for c in self.courses)


type Fraction = Callable[[float], float]
"""The part (0 to 1) of a course's ring, of this inside radius in inches about the dome's axis,
that lies over the kiln's plan: 1 everywhere over a round kiln; less over a rectangle, whose
walls cut a sail dome's low courses into arcs."""


def _whole(_: float) -> float:
    return 1.0


def lay_dome(
    radius: float,
    rise: float,
    along: float,
    up: float,
    *,
    what: str,
    reference: str,
    fraction: Fraction = _whole,
    joint: tuple[str, str, float] | None = None,
) -> DomeLaying:
    """A spherical dome of inside ``radius`` rising ``rise`` above its springing (in), laid in
    horizontal courses: each brick takes ``along`` radians of the sphere round its course and
    each course ``up`` radians up the meridian, measured from the sphere's centre (each brick
    on a radius of the dome, as Hendo's gauge sets it, Olsen p.51). A course at latitude λ is a
    ring of inside radius r·cos λ, so it takes 2π·cos λ / along bricks, times the part of it
    over the plan. Courses run from the springing up while a whole course fits; the opening
    above is the crown's plug. ``joint`` is a note on the joints: its name, formula and size."""
    if not (0 < rise <= radius + 1e-9):
        raise ValueError("a spherical dome rises more than nothing and at most its radius")
    start = math.asin(max(0.0, (radius - rise) / radius))  # springing, up from the equator
    courses: list[DomeCourse] = []
    lat = start + up / 2
    while lat < math.pi / 2 - up / 2 + 1e-9:
        ring = radius * math.cos(lat)
        n = math.ceil(2 * math.pi * math.cos(lat) * fraction(ring) / along - 1e-9)
        if n > 0:
            courses.append(DomeCourse(radius * (math.sin(lat) - math.sin(start)), 2 * ring, n))
        lat += up
    crown = 2 * radius * math.cos(lat - up / 2)

    def f(x: float) -> str:
        return f"{x:.3g} in"

    span = (
        f", from {courses[0].bricks} round the lowest to {courses[-1].bricks} at the top"
        if courses
        else ""
    )
    steps = [
        Step(
            name=f"{what}: the dome's sphere",
            formula="springing at λ₀ = asin((r − h) / r) above the sphere's equator",
            inputs={"r": f(radius), "h": f(rise)},
            value=f"λ₀ = {math.degrees(start):.3g}°",
            reference="sphere geometry",
        ),
        Step(
            name=f"{what}: each brick's angle round and up",
            formula="round its course and up the meridian, from the sphere's centre",
            inputs={"round": f"{math.degrees(along):.3g}°"},
            value=f"{math.degrees(up):.3g}° a course",
            reference=reference,
        ),
        Step(
            name=f"{what}: courses",
            formula="from λ₀ up a course angle at a time while a whole course fits; "
            "n = ⌈2π·cos λ·p / round⌉",
            inputs={
                "p": "the part of each ring over the plan"
                if fraction is not _whole
                else "1, a round kiln",
            },
            value=f"{len(courses)} courses, {sum(c.bricks for c in courses)} bricks{span}",
            reference=reference,
        ),
        Step(
            name=f"{what}: the crown's opening",
            formula="2r·cos λ, λ at the top course's upper edge",
            value=f(crown),
            reference=reference,
            note="closed by a plug or keystone, as beehive crowns are (curved-kilns.md, NPS)",
        ),
    ]
    if joint is not None:
        steps.append(Step(name=f"{what}: {joint[0]}", formula=joint[1], value=f(joint[2]),
                          reference=reference,
                          note="no source gives a largest joint"))  # fmt: skip
    return DomeLaying(tuple(courses), crown, tuple(steps))


def lay_conical_dome(
    radius: float, rise: float, brick: Brick, fraction: Fraction = _whole, what: str = "Dome"
) -> DomeLaying:
    """A dome of conical bricks, their narrow ends on the inside sphere: each brick's angle
    θ = max(d / r, D / (r + L)) both round its course and up the meridian."""
    c = course(radius, brick)
    joint = ("hot-face joint between narrow ends", "r·θ − d", c.inside_joint)
    laid = lay_dome(radius, rise, c.angle, c.angle, what=what, reference=REF, fraction=fraction,
                    joint=joint)  # fmt: skip
    return DomeLaying(laid.courses, laid.crown, laid.steps + dome_fit(radius, brick, laid, what))


def dome_fit(radius: float, brick: Brick, laid: DomeLaying, what: str) -> tuple[Step, ...]:
    """The check of a conical brick against its dome: the radius it closes on with no joint, the
    narrow end this dome's radius wants, which ends touch, and the clay laid. Shown, not judged:
    no source gives a largest fireclay joint (Olsen p.94)."""

    def f(x: float) -> str:
        return f"{x:.3g} in"

    own, wants = brick.own_radius, brick.narrow_for(radius)
    if abs(radius - own) < 1e-6:
        touch = "both ends touch: the dome is close-packed"
    elif radius > own:
        touch = "the wide ends touch; the narrow ends open fireclay joints on the hot face"
    else:
        touch = "the narrow ends touch; the wide ends open joints outside"
    return (
        Step(
            name=f"{what}: the brick's own radius",
            formula="r₀ = L·d / (D − d)",
            inputs={"L": f(brick.length), "D": f(brick.wide), "d": f(brick.narrow)},
            value=f(own),
            reference=REF,
            note="a dome of this inside radius closes with no joint both round and up",
        ),
        Step(
            name=f"{what}: the taper this dome wants",
            formula="d = D·r / (r + L), the length and the wide end kept",
            inputs={"r": f(radius)},
            value=f"{f(wants)} narrow end, against the brick's {f(brick.narrow)}",
            reference=REF,
            note=touch,
        ),
        Step(
            name=f"{what}: clay in the bricks",
            formula="n · (π·L·(D² + D·d + d²) / 12 − π·b²·¾L / 4 − π·g²/8 · ¾L / cos 57°)",
            inputs={"n": str(laid.total), "b": f(brick.bore), "g": f(brick.groove)},
            value=f"{laid.total * brick.volume / 1728:.3g} ft³",
            reference=REF + "; bore and groove the user's estimates, the groove's 57° scaled",
            note="the bore and groove taken out"
            if brick.bore or brick.groove
            else "solid: no bore or groove given",
        ),
    )


def lay_straights_dome(
    radius: float,
    rise: float,
    depth: float,
    fraction: Fraction = _whole,
    what: str = "Dome",
) -> DomeLaying | None:
    """A dome of 9 × 4½ × 2½ in straights (Olsen p.51): 9 in deep in header courses, each brick's
    4½ in end on the hot face; 4½ in deep in stretcher courses, its 9 in side on the hot face.
    Either way 2½ in up the meridian, the inside faces touching and the joints opening behind
    as in a curved wall (p.45). None for any other depth."""
    if abs(depth - 9) < 0.05:
        face, kind = 4.5, "header"
    elif abs(depth - 4.5) < 0.05:
        face, kind = 9.0, "stretcher"
    else:
        return None
    along, up = face / radius, 2.5 / radius
    joint = (
        f"{kind} courses: the joint behind, between the bricks' outer ends",
        "(r + t)·w / r − w",
        (radius + depth) * face / radius - face,
    )
    return lay_dome(radius, rise, along, up, what=what, reference=STRAIGHTS_REF,
                    fraction=fraction, joint=joint)  # fmt: skip


def rectangle(half_width: float, half_depth: float) -> Fraction:
    """The part of a ring centred on a rectangle's centre that lies over it (inches), sampled
    round the ring finely enough for a course count."""

    def part(ring: float) -> float:
        n = 720
        inside = 0
        for k in range(n):
            t = (k + 0.5) / n * 2 * math.pi
            if abs(ring * math.cos(t)) <= half_width and abs(ring * math.sin(t)) <= half_depth:
                inside += 1
        return inside / n

    return part
