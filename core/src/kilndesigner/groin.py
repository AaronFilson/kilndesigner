"""Two arched tubes crossing at right angles, their vaults meeting in a groin (roof.crossing):
Olsen's multi-directional kilns, an anagama-style tube crossed by a groundhog-style one over a
shared fire zone (The Kiln Book, 4th ed., Ch. 7, p.178–183, Figs 7-1, 7-2).

Plain geometry, in any one length unit: each tube is a box to the springline under a circular
arch, and the chamber is the union of the two. The lining is that union grown layer by layer
(the union of each tube grown, a Minkowski sum distributing over a union), so each layer of the
vaults is the two tubes' rings less everything inside the layer before, and the groin, where the
vaults meet, falls out of the subtraction: it is cut on site, as no standard shape turns it.
Volumes are summed on a grid over the plan, column by column: within each tube's run its layer is
an interval of height, so a column's share is the length of a union of intervals.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import cache
from typing import Literal

import numpy as np

from kilndesigner.model import Kiln, SprungArch
from kilndesigner.units import si

type Floats = np.ndarray
"""An array of floats, any shape."""


@dataclass(frozen=True)
class Tube:
    """One arched tube: ``axis`` 1 runs along y (the chamber's own, front to back), 0 along x
    (the crossing). ``centre`` is its centreline's place across (x for axis 1, y for axis 0),
    ``run`` its inside from end wall to end wall along its axis, ``ends`` its end walls'
    thickness, all layers."""

    axis: Literal[0, 1]
    span: float
    rise: float
    springline: float
    centre: float
    run: tuple[float, float]
    ends: float

    @property
    def radius(self) -> float:
        return (self.span**2 / 4 + self.rise**2) / (2 * self.rise)

    @property
    def centre_z(self) -> float:
        """The circle's centre, at or below the springline."""
        return self.springline + self.rise - self.radius

    @property
    def half_angle(self) -> float:
        return math.atan2(self.span / 2, self.radius - self.rise)

    @property
    def segment_area(self) -> float:
        """The area between the arch and its springline."""
        r = self.radius
        return r * r * self.half_angle - (self.span / 2) * (r - self.rise)

    def foot(self, depth: float) -> float:
        """How far from the middle the circle ``depth`` out meets the springline."""
        return math.sqrt(max((self.radius + depth) ** 2 - (self.radius - self.rise) ** 2, 0.0))

    def coords(self, x: Floats, y: Floats) -> tuple[Floats, Floats]:
        """(across, along) for points (x, y)."""
        if self.axis == 1:
            return x - self.centre, y
        return y - self.centre, x

    def top(self, x: Floats, y: Floats, depth: float, *, over_ends: bool) -> Floats:
        """The circle ``depth`` out over each point, where it stands above the springline within
        the run (and over its end walls, with ``over_ends``); -inf elsewhere."""
        u, v = self.coords(x, y)
        lo, hi = self.run
        grow = self.ends if over_ends else 0.0
        r = self.radius + depth
        under = r * r - u * u
        z = self.centre_z + np.sqrt(np.maximum(under, 0.0))
        inside = (v >= lo - grow) & (v <= hi + grow) & (under > 0) & (z > self.springline)
        return np.where(inside, z, -np.inf)


def tubes(kiln: Kiln, unit: str) -> tuple[Tube, Tube]:
    """The chamber's tube and the crossing tube, in ``unit``, from the middle of the chamber's
    floor: x across the width, y from the front (negative) to the back."""
    roof = kiln.roof
    assert isinstance(roof, SprungArch)
    assert roof.crossing is not None
    x, c = roof.crossing, kiln.chamber
    w, d, h = si(c.width, unit), si(c.depth, unit), si(c.height, unit)
    at = si(x.at, unit) if x.at is not None else d / 2
    walls = sum(si(t.thickness, unit) for t in kiln.lining.walls)
    front = sum(si(t.thickness, unit) for t in kiln.lining.for_face("front"))
    back = sum(si(t.thickness, unit) for t in kiln.lining.for_face("back"))
    length = si(x.length, unit)
    chamber = Tube(1, w, si(roof.rise, unit), h, 0.0, (-d / 2, d / 2), max(front, back))
    crossing = Tube(0, si(x.span, unit), si(x.rise, unit), h, at - d / 2,
                    (-length / 2, length / 2), walls)  # fmt: skip
    return chamber, crossing


def _union_length(a: tuple[Floats, Floats], b: tuple[Floats, Floats]) -> Floats:
    """The length of the union of the intervals a and b, each (lo, hi), empty where hi ≤ lo."""
    la = np.maximum(a[1] - a[0], 0.0)
    lb = np.maximum(b[1] - b[0], 0.0)
    both = np.maximum(np.minimum(a[1], b[1]) - np.maximum(a[0], b[0]), 0.0)
    both = np.where((la > 0) & (lb > 0), both, 0.0)
    return la + lb - both


@dataclass(frozen=True)
class GroinLayer:
    """A layer of crossing vaults above the springline. A ring (``cap`` None): both tubes'
    rings from ``inner`` to ``outer`` out, over their runs and end walls, less everything inside
    ``inner`` (the union grown to it). A cap (``cap`` the tube's index): the wall closing that
    tube's end above the springline, up to its arch, less the other tube's vault and all inside
    it (``shell`` out, the roof's whole thickness); the part's plan gives the band."""

    tubes: tuple[Tube, Tube]
    inner: float
    outer: float
    cap: int | None = None
    shell: float = 0.0

    def intervals(self, x: Floats, y: Floats) -> list[tuple[Floats, Floats]]:
        """Each tube's share of the layer over the points, as (bottom, top); empty where top ≤
        bottom. Their union is the layer."""
        if self.cap is not None:
            own, other = self.tubes[self.cap], self.tubes[1 - self.cap]
            top = own.top(x, y, 0.0, over_ends=True)
            low = np.maximum(other.top(x, y, self.shell, over_ends=True), own.springline)
            return [(low, top)]
        cut = np.maximum(*(t.top(x, y, self.inner, over_ends=False) for t in self.tubes))
        out: list[tuple[Floats, Floats]] = []
        for t in self.tubes:
            top = t.top(x, y, self.outer, over_ends=True)
            low = np.maximum(t.top(x, y, self.inner, over_ends=True), t.springline)
            out.append((np.maximum(low, cut), top))
        return out

    def volume(self, lo: tuple[float, ...], hi: tuple[float, ...], n: int = 600) -> float:
        """Summed column by column on an n × n grid over the plan lo–hi (the midpoint rule)."""
        return _volume(self, tuple(lo), tuple(hi), n)

    def _volume(self, lo: tuple[float, ...], hi: tuple[float, ...], n: int) -> float:
        xs = lo[0] + (np.arange(n) + 0.5) / n * (hi[0] - lo[0])
        ys = lo[1] + (np.arange(n) + 0.5) / n * (hi[1] - lo[1])
        x, y = np.meshgrid(xs, ys)
        parts = self.intervals(x, y)
        tall = (
            np.maximum(parts[0][1] - parts[0][0], 0.0)
            if len(parts) == 1
            else _union_length(parts[0], parts[1])
        )
        tall = np.where(np.isfinite(tall), tall, 0.0)
        return float(np.sum(tall)) * (hi[0] - lo[0]) * (hi[1] - lo[1]) / n / n

    def cut(
        self, axis: Literal[0, 1], at: float, lo: float, hi: float, steps: int = 192
    ) -> list[tuple[tuple[float, float], ...]]:
        """The layer cut by the plane x = ``at`` (axis 0, outlines in y–z) or y = ``at`` (axis 1,
        in x–z), from ``lo`` to ``hi`` along the cut: each tube's share as closed outlines, one
        per run of the cut where it has height."""
        s = np.linspace(lo, hi, steps + 1)
        line = np.full_like(s, at)
        x, y = (line, s) if axis == 0 else (s, line)
        outlines: list[tuple[tuple[float, float], ...]] = []
        for bottom, top in self.intervals(x, y):
            keep = np.isfinite(top) & (top > bottom + 1e-6)
            k = 0
            while k < len(s):
                if not keep[k]:
                    k += 1
                    continue
                j = k
                while j + 1 < len(s) and keep[j + 1]:
                    j += 1
                if j > k:
                    lower = [(float(s[i]), float(bottom[i])) for i in range(k, j + 1)]
                    upper = [(float(s[i]), float(top[i])) for i in range(j, k - 1, -1)]
                    outlines.append((*lower, *upper))
                k = j + 1
        return outlines


@cache
def _volume(layer: GroinLayer, lo: tuple[float, ...], hi: tuple[float, ...], n: int) -> float:
    """A layer's volume, worked out once: the lining's parts are asked for it many times."""
    return layer._volume(lo, hi, n)  # pyright: ignore[reportPrivateUsage]


# --- The chamber, for its heat loss and volume ------------------------------------------------


@dataclass(frozen=True)
class CrossingShape:
    """The chamber of crossing vaults, its faces growing with depth into the lining as the union
    of the two tubes grown (any one unit): the floor and walls as a box's do, (a + 2t)(b + 2t),
    the vaults' surface as each tube's circle moved out, less where it lies inside the other."""

    tubes: tuple[Tube, Tube]

    def _rects(self, t: float) -> tuple[tuple[float, float, float, float], ...]:
        out: list[tuple[float, float, float, float]] = []
        for tube in self.tubes:
            a, b = tube.run[0] - t, tube.run[1] + t
            c0, c1 = tube.centre - tube.span / 2 - t, tube.centre + tube.span / 2 + t
            out.append((c0, c1, a, b) if tube.axis == 1 else (a, b, c0, c1))
        return tuple(out)

    def floor(self, t: float = 0.0) -> float:
        """The plan's area, t out: the two rectangles less their overlap."""
        (ax0, ax1, ay0, ay1), (gx0, gx1, gy0, gy1) = self._rects(t)
        over = max(0.0, min(ax1, gx1) - max(ax0, gx0)) * max(0.0, min(ay1, gy1) - max(ay0, gy0))
        return (ax1 - ax0) * (ay1 - ay0) + (gx1 - gx0) * (gy1 - gy0) - over

    def perimeter(self, t: float = 0.0) -> float:
        """The plan's perimeter, t out: the two rectangles' less their overlap's, as the
        crossing's edges cross (each tube runs through the other's width)."""
        (ax0, ax1, ay0, ay1), (gx0, gx1, gy0, gy1) = self._rects(t)
        ox, oy = min(ax1, gx1) - max(ax0, gx0), min(ay1, gy1) - max(ay0, gy0)
        return 2 * ((ax1 - ax0) + (ay1 - ay0) + (gx1 - gx0) + (gy1 - gy0) - ox - oy)

    def vaults(self, t: float = 0.0, n: int = 2000) -> float:
        """The vaults' surface, t out: each tube's circle moved out, over its run grown by t,
        where it isn't inside the other tube grown by t, (R + t) dφ dv. At each angle φ about the
        circle's centre the point stands at a fixed height and a fixed place along the other tube,
        so the stretch of the run inside the other is |v − c_o| < √(R_o² − (z − z_o)²): summed
        over φ, its length known exactly, so the area changes smoothly with t."""
        total = 0.0
        for k, tube in enumerate(self.tubes):
            other = self.tubes[1 - k]
            r, ro = tube.radius + t, other.radius + t
            phi0 = math.acos(min(1.0, (tube.springline - tube.centre_z) / r))
            lo, hi = tube.run[0] - t, tube.run[1] + t
            # The angles at which the point stands along the other tube's run, grown by t
            sines = [(other.run[0] - t - tube.centre) / r, (other.run[1] + t - tube.centre) / r]
            a, b = (max(-phi0, math.asin(min(max(s, -1.0), 1.0))) for s in sines)
            b = min(b, phi0)
            total += (hi - lo) * r * 2 * phi0
            if b <= a:
                continue
            phi = a + (np.arange(n) + 0.5) / n * (b - a)
            z = tube.centre_z + r * np.cos(phi)
            rise = np.maximum(z - other.centre_z, 0.0)
            half = np.sqrt(np.maximum(ro * ro - rise * rise, 0.0))
            over = np.minimum(hi, other.centre + half) - np.maximum(lo, other.centre - half)
            total -= float(np.sum(np.maximum(over, 0.0))) * r * (b - a) / n
        return total

    def volume(self, n: int = 600) -> float:
        """The space inside: the plan's area to the springline, and under the higher of the two
        vaults above it, summed on a grid."""
        return _chamber_volume(self, n)

    def _volume(self, n: int) -> float:
        chamber, crossing = self.tubes
        (ax0, ax1, ay0, ay1), (gx0, gx1, gy0, gy1) = self._rects(0.0)
        x0, x1, y0, y1 = min(ax0, gx0), max(ax1, gx1), min(ay0, gy0), max(ay1, gy1)
        xs = x0 + (np.arange(n) + 0.5) / n * (x1 - x0)
        ys = y0 + (np.arange(n) + 0.5) / n * (y1 - y0)
        x, y = np.meshgrid(xs, ys)
        z = np.maximum(*(t.top(x, y, 0.0, over_ends=False) for t in self.tubes))
        above = np.where(np.isfinite(z), z - chamber.springline, 0.0)
        cell = (x1 - x0) * (y1 - y0) / n / n
        return self.floor() * crossing.springline + float(np.sum(above)) * cell


@cache
def _chamber_volume(shape: CrossingShape, n: int) -> float:
    return shape._volume(n)  # pyright: ignore[reportPrivateUsage]


__all__ = ["CrossingShape", "GroinLayer", "Tube", "tubes"]
