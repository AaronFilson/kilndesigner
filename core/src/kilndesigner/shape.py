"""The chamber's faces and their areas, as plain geometry (no CAD).

Areas grow with depth into the lining. For a face of inside size a × b, the area at depth x is
taken as (a + 2x)(b + 2x): each face spreads into the corners as the lining thickens. This is the
usual approximation for rectangular furnaces; it double-counts a little at the edges and corners,
which errs on the side of more heat loss. A sprung arch's area grows with its radius instead, a
catenary's with the length of its curve moved out, and a dome's with its sphere.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import cached_property
from itertools import pairwise

import numpy as np
from scipy.optimize import brentq

from kilndesigner.model import CatenaryArch, Dome, Face, Kiln, SprungArch
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


def _float(value: object) -> float:
    return float(value)  # pyright: ignore[reportArgumentType]  # SciPy's root, a float


@dataclass(frozen=True)
class CatenaryCurve:
    """A catenary arch springing from the floor, ``span`` wide there and ``height`` high at the
    crown, inside: z = height + a − a·cosh(x / a), with a found from the span and height
    (combustion-and-masonry.md §6.6). Any one length unit."""

    span: float
    height: float

    @cached_property
    def a(self) -> float:
        half, h = self.span / 2, self.height

        def gap(a: float) -> float:
            return a * (math.cosh(half / a) - 1) - h

        lo, hi = half / 700, half  # cosh(700) is near the largest a float holds
        while gap(hi) > 0:
            hi *= 2
        return _float(brentq(gap, lo, hi, xtol=1e-12 * half))

    def z(self, x: float) -> float:
        return self.height + self.a - self.a * math.cosh(x / self.a)

    @property
    def arc_length(self) -> float:
        return 2 * self.a * math.sinh(self.span / 2 / self.a)

    @property
    def area(self) -> float:
        """The area between the arch and the floor."""
        a = self.a
        return self.span * (self.height + a) - 2 * a * a * math.sinh(self.span / 2 / a)

    def _foot(self, depth: float) -> float:
        """Where along the inside curve (its x) the curve moved out by ``depth`` meets the floor."""
        if depth <= 0:
            return self.span / 2

        def above(t: float) -> float:
            return self.z(t) + depth / math.cosh(t / self.a)

        hi = self.span / 2 + depth
        while above(hi) > 0:
            hi += depth
        return _float(brentq(above, self.span / 2, hi))

    def offset(self, depth: float, steps: int = 64) -> list[tuple[float, float]]:
        """The inside curve moved out by ``depth`` along its normal, from foot to foot, ending on
        the floor at both. Its points are evenly spaced along the curve."""
        a, foot = self.a, self._foot(depth)
        s1 = a * math.sinh(foot / a)
        points: list[tuple[float, float]] = []
        for i in range(steps + 1):
            s = -s1 + 2 * s1 * i / steps  # along the inside curve, from the left foot
            t = a * math.asinh(s / a)
            x = t + depth * math.tanh(t / a)
            z = self.z(t) + depth / math.cosh(t / a)
            points.append((x, 0.0 if i in (0, steps) else max(0.0, z)))
        return points

    def half_width(self, depth: float) -> float:
        """Half the width of the curve moved out by ``depth``, at the floor."""
        foot = self._foot(depth)
        return foot + depth * math.tanh(foot / self.a)

    def length(self, depth: float) -> float:
        """The length of the curve moved out by ``depth``, foot to foot."""
        points = self.offset(depth, 400)
        return sum(math.dist(p, q) for p, q in pairwise(points))


def _grid(width: float, depth: float, n: int = 400) -> tuple[np.ndarray, np.ndarray, float]:
    """Midpoints of an n × n grid over a ``width`` × ``depth`` rectangle, centred, and each cell's
    area: for integrating over the chamber's plan."""
    xs = (np.arange(n) + 0.5) / n * width - width / 2
    ys = (np.arange(n) + 0.5) / n * depth - depth / 2
    x, y = np.meshgrid(xs, ys)
    return x, y, width * depth / n / n


@dataclass(frozen=True)
class SailDome:
    """A sphere through the four top corners of a ``width`` × ``depth`` chamber, ``rise`` above
    them at its centre (combustion-and-masonry.md §6.7). Heights are from the springline."""

    width: float
    depth: float
    rise: float

    @property
    def radius(self) -> float:
        corner2 = (self.width**2 + self.depth**2) / 4
        return (corner2 + self.rise**2) / (2 * self.rise)

    @property
    def centre(self) -> float:
        """The sphere's centre, below the springline (negative)."""
        return self.rise - self.radius

    def segment(self, across: float, along: float) -> float:
        """The area of a wall's inside face above the springline: the circle where the sphere
        meets the wall, ``across`` from the centre, over the wall's ``along`` length."""
        r = math.sqrt(self.radius**2 - across**2)
        half = along / 2
        return r * r * math.asin(half / r) - half * math.sqrt(r * r - half * half)

    @property
    def volume(self) -> float:
        """The space under the dome, above the springline."""
        x, y, cell = _grid(self.width, self.depth)
        z = self.centre + np.sqrt(self.radius**2 - x * x - y * y)
        return float(np.sum(np.maximum(z, 0.0)) * cell)

    def area(self, depth: float = 0.0) -> float:
        """The sphere moved out by ``depth`` over the chamber's plan grown by ``depth`` each side,
        above the springline."""
        r = self.radius + depth
        x, y, cell = _grid(self.width + 2 * depth, self.depth + 2 * depth)
        under = np.maximum(r * r - x * x - y * y, 1e-12)
        above = self.centre + np.sqrt(under) >= 0
        return float(np.sum(np.where(above, r / np.sqrt(under), 0.0)) * cell)


@dataclass(frozen=True)
class FaceShape:
    face: Face
    orientation: Orientation
    inside_area: float  # m²
    a: float  # m, the face's two inside sizes (for flat faces)
    b: float
    arch: Arch | None = None
    grows: Callable[[float], float] | None = field(default=None, compare=False)
    """The area at a depth into the lining, for a curved face that isn't a circular arch."""

    def area_at(self, depth: float) -> float:
        if self.grows is not None:
            return self.grows(depth)
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
    catenary: CatenaryCurve | None = None
    dome: SailDome | None = None

    @property
    def volume(self) -> float:
        if self.catenary is not None:
            return self.catenary.area * self.depth
        if self.dome is not None:
            return self.width * self.depth * self.height + self.dome.volume
        segment = self.arch.segment_area if self.arch else 0.0
        return (self.width * self.height + segment) * self.depth

    def faces(self) -> list[FaceShape]:
        w, d, h = self.width, self.depth, self.height
        if self.catenary is not None:
            return self._catenary_faces(self.catenary)
        floor = FaceShape("floor", "facing_down", w * d, w, d)
        if self.dome is not None:
            dome = self.dome
            sides, ends = dome.segment(w / 2, d), dome.segment(d / 2, w)
            return [
                FaceShape("left", "vertical", d * h + sides, d, h),
                FaceShape("right", "vertical", d * h + sides, d, h),
                FaceShape("back", "vertical", w * h + ends, w, h),
                FaceShape("front", "vertical", w * h + ends, w, h),
                floor,
                FaceShape("roof", "facing_up", dome.area(), w, d, grows=dome.area),
            ]
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
            floor,
            roof,
        ]

    def _catenary_faces(self, arch: CatenaryCurve) -> list[FaceShape]:
        """A catenary has no side walls: the arch runs from the floor over the top. Its outside
        is mostly upright, so it loses heat as a vertical wall as tall as the arch."""
        w, d, h = self.width, self.depth, self.height

        def grows(depth: float) -> float:
            return arch.length(depth) * (d + 2 * depth)

        return [
            FaceShape("back", "vertical", arch.area, w, h),
            FaceShape("front", "vertical", arch.area, w, h),
            FaceShape("floor", "facing_down", w * d, w, d),
            FaceShape("roof", "vertical", arch.arc_length * d, arch.arc_length, h, grows=grows),
        ]


def chamber_shape(kiln: Kiln) -> ChamberShape:
    c = kiln.chamber
    w, d, h = si(c.width, "m"), si(c.depth, "m"), si(c.height, "m")
    if isinstance(kiln.roof, SprungArch):
        return ChamberShape(w, d, h, Arch(w, si(kiln.roof.rise, "m")))
    if isinstance(kiln.roof, CatenaryArch):
        return ChamberShape(w, d, h, None, catenary=CatenaryCurve(w, h))
    if isinstance(kiln.roof, Dome):
        return ChamberShape(w, d, h, None, dome=SailDome(w, d, si(kiln.roof.rise, "m")))
    return ChamberShape(w, d, h, None)
