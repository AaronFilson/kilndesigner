"""Shapes as data: outlines of lines and arcs, a vault's sections at stations along a run, and
profiles turned about an axis (docs/planning/complex-curves.md, layer 1).

The named chamber and roof types (a box under a sprung arch, a dome, a round chamber) are
shorthands for these (form.py); a teardrop or an oval plan, a vault whose section changes along
its length or a bottle's revolved profile are the same data, made another way.

Plain floats in any one length unit, as in shape.py: a plan in x (across) and y (along), a
section in (across, up) from the springline, a revolved profile in (r, z). Outlines run
anticlockwise.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from itertools import pairwise

type Point = tuple[float, float]

TOUCH = 1e-9  # ends this close (relative to the outline's size) are taken as joined


@dataclass(frozen=True)
class Line:
    start: Point
    end: Point

    @property
    def length(self) -> float:
        return math.dist(self.start, self.end)

    def points(self, steps: int) -> list[Point]:
        """Its two ends: a straight line needs no more."""
        del steps
        return [self.start, self.end]

    def sweep_area(self) -> float:
        """½∫(x dy − y dx) along it: summed round a closed outline, its area (Green's theorem)."""
        (x0, y0), (x1, y1) = self.start, self.end
        return (x0 * y1 - x1 * y0) / 2

    def hit(self, origin: Point, u: Point) -> float | None:
        """How far along the ray from ``origin`` in the direction ``u`` (a unit vector) it meets
        this line, or None."""
        (ax, ay), (bx, by) = self.start, self.end
        dx, dy = bx - ax, by - ay
        det = u[0] * -dy - u[1] * -dx
        if abs(det) < 1e-15:
            return None
        ox, oy = ax - origin[0], ay - origin[1]
        t = (ox * -dy - oy * -dx) / det
        s = (u[0] * oy - u[1] * ox) / det
        return t if t > 0 and -1e-12 <= s <= 1 + 1e-12 else None


@dataclass(frozen=True)
class Arc:
    """A circular arc about ``centre``, from the angle ``start`` turning through ``sweep``
    (radians; positive anticlockwise)."""

    centre: Point
    radius: float
    start: float
    sweep: float

    def at(self, angle: float) -> Point:
        cx, cy = self.centre
        return (cx + self.radius * math.cos(angle), cy + self.radius * math.sin(angle))

    @property
    def first(self) -> Point:
        return self.at(self.start)

    @property
    def last(self) -> Point:
        return self.at(self.start + self.sweep)

    @property
    def length(self) -> float:
        return self.radius * abs(self.sweep)

    def points(self, steps: int) -> list[Point]:
        """``steps`` chords along it, ends included."""
        return [self.at(self.start + self.sweep * k / steps) for k in range(steps + 1)]

    def sweep_area(self) -> float:
        """½∫(x dy − y dx) along it, with x = cx + r cos t, y = cy + r sin t:
        ½[r²Δt + r·cx(sin t₁ − sin t₀) − r·cy(cos t₁ − cos t₀)]."""
        (cx, cy), r = self.centre, self.radius
        t0, t1 = self.start, self.start + self.sweep
        return (
            r * r * self.sweep
            + r * cx * (math.sin(t1) - math.sin(t0))
            - r * cy * (math.cos(t1) - math.cos(t0))
        ) / 2

    def hit(self, origin: Point, u: Point) -> float | None:
        """How far along the ray from ``origin`` in the direction ``u`` it meets this arc (the
        farther crossing of the circle that lies on the arc), or None."""
        ox, oy = origin[0] - self.centre[0], origin[1] - self.centre[1]
        b = ox * u[0] + oy * u[1]
        disc = b * b - (ox * ox + oy * oy - self.radius**2)
        if disc < 0:
            return None
        for t in (-b + math.sqrt(disc), -b - math.sqrt(disc)):
            if t > 0 and self._spans(math.atan2(oy + t * u[1], ox + t * u[0])):
                return t
        return None

    def _spans(self, angle: float) -> bool:
        lo = min(self.start, self.start + self.sweep)
        turned = (angle - lo) % (2 * math.pi)
        return turned <= abs(self.sweep) + 1e-12 or turned >= 2 * math.pi - 1e-12


@dataclass(frozen=True)
class Polyline:
    """A curve given as points, for one that isn't lines and arcs: a catenary."""

    vertices: tuple[Point, ...]

    @property
    def start(self) -> Point:
        return self.vertices[0]

    @property
    def end(self) -> Point:
        return self.vertices[-1]

    @property
    def length(self) -> float:
        return sum(math.dist(p, q) for p, q in pairwise(self.vertices))

    def points(self, steps: int) -> list[Point]:
        del steps
        return list(self.vertices)

    def sweep_area(self) -> float:
        return sum(Line(p, q).sweep_area() for p, q in pairwise(self.vertices))

    def hit(self, origin: Point, u: Point) -> float | None:
        hits = [Line(p, q).hit(origin, u) for p, q in pairwise(self.vertices)]
        found = [t for t in hits if t is not None]
        return max(found) if found else None


type Segment = Line | Arc | Polyline


def _ends(s: Segment) -> tuple[Point, Point]:
    if isinstance(s, Arc):
        return s.first, s.last
    return s.start, s.end


@dataclass(frozen=True)
class Outline:
    """A closed outline: segments end to end, anticlockwise, the last ending where the first
    starts."""

    segments: tuple[Segment, ...]

    def __post_init__(self) -> None:
        if not self.segments:
            raise ValueError("an outline needs at least one segment")
        ends = [_ends(s) for s in self.segments]
        size = max(math.hypot(*p) for e in ends for p in e) or 1.0
        for (_, end), (start, _) in zip(ends, ends[1:] + ends[:1], strict=True):
            if math.dist(end, start) > TOUCH * size:
                raise ValueError(f"the outline is open: a segment ends at {end}, the next "
                                 f"starts at {start}")  # fmt: skip
        if self.area <= 0:
            raise ValueError("the outline must run anticlockwise and enclose an area")

    @property
    def area(self) -> float:
        """∮ ½(x dy − y dx), exact for lines and arcs."""
        return sum(s.sweep_area() for s in self.segments)

    @property
    def perimeter(self) -> float:
        return sum(s.length for s in self.segments)

    def points(self, steps: int = 48) -> list[Point]:
        """The outline as a polygon, each arc in ``steps`` chords, no point repeated."""
        out: list[Point] = []
        for s in self.segments:
            out.extend(s.points(steps)[:-1])
        return out

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        """x₀, x₁, y₀, y₁ of the outline, arcs sampled finely."""
        xs, ys = zip(*self.points(720), strict=True)
        return min(xs), max(xs), min(ys), max(ys)

    def reach(self, angle: float, centre: Point = (0.0, 0.0)) -> float:
        """How far the outline lies from ``centre`` in the direction ``angle`` (radians from +x).
        For an outline that every ray from ``centre`` crosses once: a convex one, or a teardrop
        seen from inside its round end."""
        u = (math.cos(angle), math.sin(angle))
        hits = [s.hit(centre, u) for s in self.segments]
        found = [t for t in hits if t is not None]
        if not found:
            raise ValueError(f"the centre {centre} isn't inside the outline")
        return max(found)

    def sees_all(self, centre: Point = (0.0, 0.0)) -> bool:
        """Whether every point of the outline can be seen from ``centre`` along a ray inside it
        (the outline is star-shaped about it), so that ``reach`` is its distance every way: a
        convex outline from any point inside, a reverse curve only from where it doesn't hide
        what lies behind it."""
        for p in self.points(96):
            d = math.dist(p, centre)
            if d < 1e-12:
                continue
            # The ray towards a point of the outline always meets it there, so reach finds a hit
            far = self.reach(math.atan2(p[1] - centre[1], p[0] - centre[0]), centre)
            if far > d * (1 + 1e-6) + 1e-9 * self.perimeter:
                return False
        return True

    def farthest(self, centre: Point = (0.0, 0.0)) -> float:
        """The farthest the outline reaches from ``centre``: arcs at their farthest point."""
        far = 0.0
        for s in self.segments:
            pts = s.points(720) if isinstance(s, Arc) else s.points(0)
            far = max(far, *(math.dist(p, centre) for p in pts))
        return far


def rectangle(width: float, depth: float, centre: Point = (0.0, 0.0)) -> Outline:
    """``width`` across x, ``depth`` along y, centred on ``centre``."""
    cx, cy = centre
    x0, x1, y0, y1 = cx - width / 2, cx + width / 2, cy - depth / 2, cy + depth / 2
    c = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return Outline(tuple(Line(p, q) for p, q in zip(c, c[1:] + c[:1], strict=True)))


def circle(diameter: float, centre: Point = (0.0, 0.0)) -> Outline:
    return Outline((Arc(centre, diameter / 2, -math.pi / 2, 2 * math.pi),))


def regular_polygon(sides: int, apothem: float) -> Outline:
    """A regular polygon ``apothem`` from its centre to each flat, a flat facing the front (−y),
    as a faceted round kiln's wall (geometry.polygon_corners)."""
    r = apothem / math.cos(math.pi / sides)
    c = [
        (r * math.cos(-math.pi / 2 + (2 * k + 1) * math.pi / sides),
         r * math.sin(-math.pi / 2 + (2 * k + 1) * math.pi / sides))
        for k in range(sides)
    ]  # fmt: skip
    return Outline(tuple(Line(p, q) for p, q in zip(c, c[1:] + c[:1], strict=True)))


def oval(width: float, length: float, end_radius: float) -> Outline:
    """A four-centred oval, ``width`` across x and ``length`` along y, centred: round ends of
    ``end_radius`` on the long axis and flatter sides, each arc tangent to the next. The sides'
    radius follows from the three sizes (the usual construction of a four-centred oval)."""
    a, b, r = length / 2, width / 2, end_radius
    if not 0 < r < b <= a:
        raise ValueError("an oval needs 0 < end_radius < width/2 ≤ length/2")
    # The end arcs' centres at (0, ±(a − r)); the sides' at (∓(R − b), 0), R from tangency:
    # the centres R − r apart, so (R − b)² + (a − r)² = (R − r)²
    big = ((a - r) ** 2 + b * b - r * r) / (2 * (b - r))
    if big <= b:
        raise ValueError("the end radius is too large for an oval of these sizes")
    e, s = a - r, big - b
    turn = math.atan2(e, s)  # where each end arc meets a side arc, from the side's centre
    return Outline(
        (
            Arc((-s, 0.0), big, -turn, 2 * turn),  # the right side
            Arc((0.0, e), r, turn, math.pi - 2 * turn),  # the back end
            Arc((s, 0.0), big, math.pi - turn, 2 * turn),  # the left side
            Arc((0.0, -e), r, math.pi + turn, math.pi - 2 * turn),  # the front end
        )
    )


def teardrop(radius: float, length: float, side_radius: float | None = None) -> Outline:
    """A teardrop: a round end of ``radius`` centred on the origin, and two sides tangent to it
    meeting in a point ``length`` from the round end's far side, along +y. The sides are straight,
    or arcs of ``side_radius`` (each bulging outwards, tangent to the round end)."""
    nose = length - radius  # the point, from the round end's centre
    if nose <= radius:
        raise ValueError("a teardrop's length must be more than its round end's diameter")
    if side_radius is None:
        # A straight side from the point, tangent to the circle at the angle φ from +x
        phi = math.asin(radius / nose)
        right = (radius * math.cos(phi), radius * math.sin(phi))
        left = (-right[0], right[1])
        return Outline(
            (
                Line(right, (0.0, nose)),
                Line((0.0, nose), left),
                Arc((0.0, 0.0), radius, math.pi - phi, math.pi + 2 * phi),
            )
        )
    if side_radius <= radius:
        raise ValueError("the sides' radius must be more than the round end's")
    # A side's centre C at R_s − r from the origin (tangent inside) and R_s from the point
    cy = (nose * nose + radius * radius - 2 * side_radius * radius) / (2 * nose)
    off2 = (side_radius - radius) ** 2 - cy * cy
    if off2 <= 0:
        raise ValueError("the sides' radius is too small to reach the point")
    cx = math.sqrt(off2)
    # The right side's centre C is left of the axis, at (−cx, cy). It touches the round end at
    # −r·C/|C|, in the direction (cx, −cy) both from C and from the origin, and runs
    # anticlockwise from there up to the point; the left side is its mirror image
    t0 = math.atan2(-cy, cx)
    t1 = math.atan2(nose - cy, cx)
    return Outline(
        (
            Arc((-cx, cy), side_radius, t0, t1 - t0),
            Arc((cx, cy), side_radius, math.pi - t1, t1 - t0),
            Arc((0.0, 0.0), radius, math.pi - t0, math.pi + 2 * t0),
        )
    )


def _moved(s: Segment, dx: float, dy: float) -> Segment:
    if isinstance(s, Arc):
        return Arc((s.centre[0] + dx, s.centre[1] + dy), s.radius, s.start, s.sweep)
    if isinstance(s, Line):
        return Line((s.start[0] + dx, s.start[1] + dy), (s.end[0] + dx, s.end[1] + dy))
    return Polyline(tuple((x + dx, y + dy) for x, y in s.vertices))


def moved(outline: Outline, dx: float, dy: float) -> Outline:
    return Outline(tuple(_moved(s, dx, dy) for s in outline.segments))


def flat_teardrop(
    width: float, length: float, front_width: float | None = None, side_radius: float | None = None
) -> Outline:
    """A teardrop ``width`` across at its round end and ``length`` from its front to its point,
    along +y, centred on its length: the round end cut square by a flat front wall
    ``front_width`` wide (a firebox's wall, as Calimpong's), or whole when that is left out. The
    widest point then lies √(r² − (f/2)²) behind the front."""
    r = width / 2
    if front_width is None:
        whole = teardrop(r, length, side_radius)
        return moved(whole, 0.0, -length / 2 + r)
    if not 0 < front_width < width:
        raise ValueError("a teardrop's flat front must be narrower than its widest point")
    c = math.sqrt(r * r - (front_width / 2) ** 2)  # the front, behind the round end's centre
    whole = teardrop(r, length - c + r, side_radius)
    *sides, end = whole.segments
    assert isinstance(end, Arc)
    left, right = math.pi + math.asin(c / r), 2 * math.pi - math.asin(c / r)
    stop = end.start + end.sweep
    if not end.start < left < right < stop:
        raise ValueError("the teardrop's sides meet its round end in front of its flat front")
    cut = (
        Arc(end.centre, r, end.start, left - end.start),
        Line(end.at(left), end.at(right)),
        Arc(end.centre, r, right, stop - right),
    )
    return moved(Outline((*sides, *cut)), 0.0, -length / 2 + c)


def necked_teardrop(
    width: float,
    length: float,
    front_width: float,
    side_radius: float,
    neck_width: float,
    neck_length: float,
    neck_radius: float,
) -> Outline:
    """A teardrop with a flat front, as flat_teardrop, whose sides don't meet in a point but turn
    in a reverse (concave) curve into a straight, parallel-sided neck ``neck_width`` across and
    ``neck_length`` long, closed by a flat back wall: Calimpong's plan as the book draws it (Fig
    4-140, curved-kilns.md). Centred on its length, the front at −y.

    Each side is an arc of ``side_radius`` tangent inside the round end (its centre C at
    R_s − r from the round end's centre O), then an arc of ``neck_radius`` bending the other way,
    tangent outside the side's circle (|F − C| = R_s + ρ) and to the neck's straight side, which it
    meets where the neck begins. The side's centre is turned about O until both hold: one
    unknown, found by bisection, the side's circle growing towards the neck as it turns."""
    r, f, n = width / 2, front_width, neck_width / 2
    rs, rho = side_radius, neck_radius
    if not 0 < f < width:
        raise ValueError("a teardrop's flat front must be narrower than its widest point")
    if not 0 < neck_width < front_width or neck_length <= 0 or rho <= 0:
        raise ValueError("a neck must be narrower than the flat front, with a length and a radius")
    if rs <= r:
        raise ValueError("the sides' radius must be more than the round end's")
    c = math.sqrt(r * r - (f / 2) ** 2)  # the front, behind the round end's centre
    start = length - c - neck_length  # where the neck's straight sides begin, from O
    if start <= 0:
        raise ValueError("the neck is too long: it reaches the round end")
    fc = (n + rho, start)  # the reverse curve's centre, beside the neck's start

    def centre(psi: float) -> Point:
        """The right side's centre, R_s − r from O, ψ round from −x towards +y."""
        return (-(rs - r) * math.cos(psi), (rs - r) * math.sin(psi))

    def gap(psi: float) -> float:
        return math.dist(fc, centre(psi)) - (rs + rho)

    lo, hi = -math.pi / 2, math.pi / 2
    if not gap(lo) > 0 > gap(hi):
        raise ValueError("the sides and the neck's curve don't meet: change their radii")
    for _ in range(100):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if gap(mid) > 0 else (lo, mid)
    cc = centre((lo + hi) / 2)
    t0 = math.atan2(-cc[1], -cc[0])  # the side touches the round end, seen from C
    t1 = math.atan2(fc[1] - cc[1], fc[0] - cc[0])  # and the reverse curve
    a0 = math.atan2(cc[1] - fc[1], cc[0] - fc[0])  # the touching point, seen from F
    begin, stop = math.pi - t0, 2 * math.pi + t0
    low, high = math.pi + math.asin(c / r), 2 * math.pi - math.asin(c / r)
    meets = -math.pi / 2 < t0 < t1 < math.pi / 2 and -math.pi < a0 < -math.pi / 2
    if not meets or not begin < low < high < stop:
        raise ValueError("the sides and the neck's curve don't meet: change their radii")
    if t0 < 0:
        raise ValueError(
            "the sides would bulge wider than the round end: make their radius smaller or the "
            "neck's larger"
        )
    back = length - c
    side = Arc(cc, rs, t0, t1 - t0)
    turn = Arc(fc, rho, a0, -math.pi - a0)  # clockwise, round to −x: the neck's start
    right = (side, turn, Line((n, start), (n, back)))
    # The left half, mirrored: x → −x reverses each piece's direction
    left = (
        Line((-n, back), (-n, start)),
        Arc((-fc[0], fc[1]), rho, 0.0, turn.sweep),
        Arc((-cc[0], cc[1]), rs, math.pi - t1, t1 - t0),
    )
    # The round end, from the left side's touching point round the front to the right side's,
    # cut square by the front wall
    o = (0.0, 0.0)
    end = Arc(o, r, begin, stop - begin)
    cut = (
        Arc(o, r, begin, low - begin),
        Line(end.at(low), end.at(high)),
        Arc(o, r, high, stop - high),
    )
    return moved(Outline((*right, Line((n, back), (-n, back)), *left, *cut)), 0.0, -length / 2 + c)


def _normal(s: Line | Arc, end: bool) -> Point:
    """The outward normal of an anticlockwise outline's line or arc at its start or end."""
    if isinstance(s, Arc):
        a = s.start + (s.sweep if end else 0.0)
        sign = 1.0 if s.sweep > 0 else -1.0
        return (sign * math.cos(a), sign * math.sin(a))
    (x0, y0), (x1, y1) = s.start, s.end
    n = math.dist(s.start, s.end)
    return ((y1 - y0) / n, -(x1 - x0) / n)


def offset(outline: Outline, t: float) -> Outline:
    """A convex outline of lines and arcs moved out by ``t``: each line moved along its normal,
    each arc's radius grown, and an arc of radius ``t`` round each corner (the Minkowski sum with
    a disc, whose area is A + P·t + π·t², Steiner's formula). Tangent joins need no corner."""
    if t <= 0:
        return outline
    out: list[Segment] = []
    segs: list[Line | Arc] = []
    for s in outline.segments:
        if isinstance(s, Polyline):
            raise ValueError("a curve given as points isn't offset here")
        segs.append(s)
    for s, nxt in zip(segs, segs[1:] + segs[:1], strict=True):
        if isinstance(s, Arc):
            grow = t if s.sweep > 0 else -t
            if s.radius + grow <= 0:
                raise ValueError(
                    f"a reverse curve of {s.radius:g} radius is tighter than the {t:g} the outline "
                    "is moved out: it would close up"
                )
            out.append(Arc(s.centre, s.radius + grow, s.start, s.sweep))
        else:
            nx, ny = _normal(s, False)
            out.append(Line((s.start[0] + t * nx, s.start[1] + t * ny),
                            (s.end[0] + t * nx, s.end[1] + t * ny)))  # fmt: skip
        a, b = _normal(s, True), _normal(nxt, False)
        turn = math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1])
        if turn > 1e-9:
            corner = _ends(s)[1]
            out.append(Arc(corner, t, math.atan2(a[1], a[0]), turn))
    return Outline(tuple(out))


def half_width(outline: Outline, y: float) -> float:
    """Half the outline's width at ``y``, about x = 0 (a convex plan symmetric about its long
    axis); 0 beyond its ends."""
    try:
        return outline.reach(0.0, (0.0, y))
    except ValueError:
        return 0.0


@dataclass(frozen=True)
class Station:
    """A vault's section at ``at`` along its run: a closed outline in (across, up), up from the
    springline, the space under the crown."""

    at: float
    section: Outline


@dataclass(frozen=True)
class Run:
    """A vault along a straight run: its sections at stations, lofted between them. ``axis`` is
    the plan direction it runs in, ``offset`` where its centre line lies across that (plan
    coordinates); the stations' ``at`` are along the axis."""

    stations: tuple[Station, ...]
    axis: tuple[float, float] = (0.0, 1.0)
    offset: float = 0.0

    def __post_init__(self) -> None:
        ats = [s.at for s in self.stations]
        if len(ats) < 2 or any(b <= a for a, b in pairwise(ats)):
            raise ValueError("a run needs two or more stations, in order along it")

    @property
    def length(self) -> float:
        return self.stations[-1].at - self.stations[0].at

    @property
    def volume(self) -> float:
        """The sections' areas, trapezoidal between stations: exact where the section stays the
        same, the mean of the ends' areas where it changes (a ruled loft between similar
        sections is near that)."""
        return sum(
            (a.section.area + b.section.area) / 2 * (b.at - a.at)
            for a, b in pairwise(self.stations)
        )


def prism(section: Outline, length: float, **where: float | tuple[float, float]) -> Run:
    """A vault of one section all along: two stations, ``length`` apart, centred on 0."""
    return Run((Station(-length / 2, section), Station(length / 2, section)), **where)  # pyright: ignore[reportArgumentType]


def arch_section(span: float, rise: float) -> Outline:
    """A circular arch's crown over its springline, as a section: the arc and its chord. One
    rising more than half its span is more than a semicircle, turning past the vertical at each
    springing."""
    radius = (span**2 / 4 + rise**2) / (2 * rise)
    half = math.asin(min(1.0, span / (2 * radius)))
    if rise > span / 2:
        half = math.pi - half
    centre = (0.0, rise - radius)
    arc = Arc(centre, radius, math.pi / 2 - half, 2 * half)
    return Outline((arc, Line(arc.last, arc.first)))


def curve_section(points: Sequence[Point]) -> Outline:
    """A crown given as points from the right springing over to the left (a catenary's), closed
    by the chord between them."""
    curve = Polyline(tuple(points))
    return Outline((curve, Line(curve.end, curve.start)))


@dataclass(frozen=True)
class SphereDome:
    """A dome over a plan outline: the sphere, centred over ``centre``, through the outline's
    farthest point, ``rise`` above the springline there (a sail dome over a rectangle, a cap over
    a circle). Over a teardrop or an oval it springs from the farthest point and stands above the
    springline elsewhere, as Olsen's cast domes do over their walls."""

    over: Outline
    rise: float
    centre: Point = (0.0, 0.0)

    @property
    def radius(self) -> float:
        base = self.over.farthest(self.centre)
        return (base * base + self.rise**2) / (2 * self.rise)

    @property
    def volume(self) -> float:
        """The space under the sphere over the outline, above the springline: in polar form
        ∫ [c·ρ²/2 + (R³ − (R² − ρ²)^{3/2})/3] dθ, c the sphere's centre's height (below the
        springline, negative) and ρ(θ) the outline's reach. The outline lies inside the
        springline circle, so the sphere stands above it everywhere."""
        r = self.radius
        c = self.rise - r
        n = 4096
        total = 0.0
        for k in range(n):
            rho = self.over.reach((k + 0.5) / n * 2 * math.pi, self.centre)
            total += c * rho * rho / 2 + (r**3 - max(r * r - rho * rho, 0.0) ** 1.5) / 3
        return total * 2 * math.pi / n


@dataclass(frozen=True)
class Revolved:
    """A closed outline in the r–z plane (r ≥ 0) turned about the z axis: a round wall's layer,
    a dome's shell, a bottle's chimney."""

    profile: tuple[Point, ...]

    @property
    def volume(self) -> float:
        """Pappus: 2π × the outline's area × its centroid's radius, by the shoelace sums."""
        pts, nxt = self.profile, self.profile[1:] + self.profile[:1]
        moment = sum(
            (r0 + r1) * (r0 * z1 - r1 * z0) for (r0, z0), (r1, z1) in zip(pts, nxt, strict=True)
        )
        return math.pi * abs(moment) / 3


def shell_profile(
    inner: float, outer: float, centre: float, springline: float, steps: int = 48
) -> list[Point]:
    """The part of a spherical shell (radii ``inner`` to ``outer``, centred on the axis at height
    ``centre``) above the springline, in the r–z plane: up the inside from the springline to the
    crown, down the outside, and back along the springline."""

    def arc(rho: float, rising: bool) -> list[Point]:
        end = math.acos(max(-1.0, min(1.0, (springline - centre) / rho)))  # from the vertical
        angles = [end * (1 - k / steps) for k in range(steps + 1)]
        pts = [(rho * math.sin(a), centre + rho * math.cos(a)) for a in angles]
        return pts if rising else pts[::-1]

    return [*arc(inner, True), *arc(outer, False)]
