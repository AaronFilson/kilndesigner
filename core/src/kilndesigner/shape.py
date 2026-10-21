"""The chamber's faces and their areas, as plain geometry (no CAD).

Areas grow with depth into the lining. For a face of inside size a × b, the area at depth x is
taken as (a + 2x)(b + 2x): each face spreads into the corners as the lining thickens. This is the
usual approximation for rectangular furnaces; it double-counts a little at the edges and corners,
which errs on the side of more heat loss. A sprung arch's area grows with its radius instead.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from kilndesigner.model import Face, Kiln, SprungArch
from kilndesigner.thermal.surface import Orientation
from kilndesigner.units import si


@dataclass(frozen=True)
class Arch:
    """A circular arch of span ``span`` and rise ``rise`` (m)."""

    span: float
    rise: float

    @property
    def radius(self) -> float:
        return (self.span**2 / 4 + self.rise**2) / (2 * self.rise)

    @property
    def half_angle(self) -> float:
        return math.asin(self.span / (2 * self.radius))

    @property
    def arc_length(self) -> float:
        return 2 * self.radius * self.half_angle

    @property
    def segment_area(self) -> float:
        """The area between the arch and its springline (m²)."""
        r, theta = self.radius, self.half_angle
        return r * r * theta - (self.span / 2) * (r - self.rise)


@dataclass(frozen=True)
class FaceShape:
    face: Face
    orientation: Orientation
    inside_area: float  # m²
    a: float  # m, the face's two inside sizes (for flat faces)
    b: float
    arch: Arch | None = None

    def area_at(self, depth: float) -> float:
        if self.arch is not None:
            return 2 * (self.arch.radius + depth) * self.arch.half_angle * (self.b + 2 * depth)
        extra = self.inside_area - self.a * self.b  # an arch segment on an end wall
        return (self.a + 2 * depth) * (self.b + 2 * depth) + extra

    def characteristic_length(self, depth: float) -> float:
        """Height for a vertical face; area over perimeter for a horizontal one."""
        a, b = self.a + 2 * depth, self.b + 2 * depth
        if self.orientation == "vertical":
            return b
        if self.arch is not None:
            a = 2 * (self.arch.radius + depth) * self.arch.half_angle
        return (a * b) / (2 * (a + b))


@dataclass(frozen=True)
class ChamberShape:
    width: float
    depth: float
    height: float
    arch: Arch | None

    @property
    def volume(self) -> float:
        segment = self.arch.segment_area if self.arch else 0.0
        return (self.width * self.height + segment) * self.depth

    def faces(self) -> list[FaceShape]:
        w, d, h = self.width, self.depth, self.height
        segment = self.arch.segment_area if self.arch else 0.0
        roof = (
            FaceShape("roof", "facing_up", self.arch.arc_length * d, w, d, self.arch)
            if self.arch
            else FaceShape("roof", "facing_up", w * d, w, d)
        )
        # For vertical faces, ``b`` is the height (the convection length).
        return [
            FaceShape("left", "vertical", d * h, d, h),
            FaceShape("right", "vertical", d * h, d, h),
            FaceShape("back", "vertical", w * h + segment, w, h),
            FaceShape("front", "vertical", w * h + segment, w, h),
            FaceShape("floor", "facing_down", w * d, w, d),
            roof,
        ]


def chamber_shape(kiln: Kiln) -> ChamberShape:
    c = kiln.chamber
    arch = None
    if isinstance(kiln.roof, SprungArch):
        arch = Arch(si(c.width, "m"), si(kiln.roof.rise, "m"))
    return ChamberShape(si(c.width, "m"), si(c.depth, "m"), si(c.height, "m"), arch)
