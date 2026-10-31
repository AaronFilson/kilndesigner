"""2D drawings for the plans: sections through the kiln, and brick course plans.

Drawings are made from the same lining parts as the 3D model (:func:`lining_parts`), cut by a
plane, so the plans and the model can't disagree. SVG is used for the PDF; DXF for CAD.
Model units are millimetres; dimensions are labelled in the design's units.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from typing import Literal
from xml.sax.saxutils import escape

import numpy as np

from kilndesigner.geometry import (
    COLOURS,
    Part,
    arch_outline,
    in_a_row,
    lining_parts,
    polygon_corners,
    polygon_reach,
)
from kilndesigner.masonry import IN, LayerPlan
from kilndesigner.model import CatenaryArch, Kiln
from kilndesigner.rings import CLOSER, FAMILIES, STRAIGHT
from kilndesigner.round_masonry import RingPlan
from kilndesigner.shape import CatenaryCurve
from kilndesigner.units import si

type Axis = Literal[0, 1, 2]


@dataclass(frozen=True)
class Rect:
    """A filled region: a rectangle, or the polygon ``points`` when given (an arch ring)."""

    x: float
    y: float
    w: float
    h: float
    fill: tuple[float, float, float]
    layer: str  # a part name or a label
    points: tuple[tuple[float, float], ...] = ()
    holes: tuple[tuple[tuple[float, float], ...], ...] = ()  # outlines cut out of ``points``


@dataclass(frozen=True)
class Dimension:
    x1: float
    y1: float
    x2: float
    y2: float
    offset: float  # how far the dimension line sits from the measured edge (mm, signed)
    text: str


@dataclass(frozen=True)
class Circle:
    x: float
    y: float
    r: float


@dataclass
class View:
    title: str
    rects: list[Rect]
    dims: list[Dimension]
    circles: list[Circle]

    def bounds(self) -> tuple[float, float, float, float]:
        xs = [r.x for r in self.rects] + [r.x + r.w for r in self.rects]
        ys = [r.y for r in self.rects] + [r.y + r.h for r in self.rects]
        return min(xs), min(ys), max(xs), max(ys)


def length_text(mm: float, us: bool) -> str:
    if us:
        inches = mm / IN
        return f"{inches:.3g} in" if inches < 24 else f"{inches:.4g} in"
    return f"{mm:.0f} mm"


def _arch_cut(p: Part, axis: Axis) -> Rect | None:
    """An arch ring or cap cut across (y = 0: its outline) or along (x = 0: a band)."""
    assert p.arch is not None
    fill = COLOURS.get(p.kind, (0.8, 0.8, 0.8))
    a = p.arch
    if axis == 1:
        points = tuple(arch_outline(p))
        xs, zs = [x for x, _ in points], [z for _, z in points]
        return Rect(min(xs), min(zs), max(xs) - min(xs), max(zs) - min(zs), fill, p.name, points)
    assert axis == 0, "arches are only cut across and along"
    bottom = p.lo[2] if p.cap else a.centre_z + a.radius
    top = a.centre_z + a.radius + a.thickness
    return Rect(p.lo[1], bottom, p.length_y, top - bottom, fill, p.name)


def _crossings(
    points: tuple[tuple[float, float], ...], along: Literal[0, 1], at: float
) -> list[tuple[float, float]]:
    """Where a line crosses a closed outline in the x–z plane, as spans of the other coordinate:
    ``along`` 0 is the line x = at (spans of z), 1 the line z = at (spans of x)."""
    hits: list[float] = []
    for p, q in zip(points, points[1:] + points[:1], strict=True):
        a, b = p[along], q[along]
        if (a <= at < b) or (b <= at < a):
            t = (at - a) / (b - a)
            hits.append(p[1 - along] + t * (q[1 - along] - p[1 - along]))
    hits.sort()
    return list(zip(hits[::2], hits[1::2], strict=False))


def _dome_cut(p: Part, axis: Axis, steps: int = 96) -> Rect | None:
    """A dome layer or a wall's top under it, cut through the centre line: across (y = 0, in the
    x–z plane) or along (x = 0, in the y–z plane), as an outline between its bottom and top."""
    assert p.dome is not None
    d, springline = p.dome, p.lo[2]
    lo, hi = p.lo[1 - axis], p.hi[1 - axis]  # across the cut: x for y = 0, y for x = 0
    if not p.lo[axis] - 1e-6 <= 0 <= p.hi[axis] + 1e-6:
        return None
    s = np.linspace(lo, hi, steps + 1)
    zero = np.zeros_like(s)
    x, y = (s, zero) if axis == 1 else (zero, s)
    top = d.heights(x, y, d.radius + d.thickness)
    inside = d.heights(x, y, d.radius)
    bottom = np.full_like(s, springline) if p.cap else np.maximum(inside, springline)
    keep = top > bottom + 1e-6
    assert keep.any(), "a dome layer always stands above its springline at the centre line"
    lower = [(float(a), float(b)) for a, b in zip(s[keep], bottom[keep], strict=True)]
    upper = [(float(a), float(b)) for a, b in zip(s[keep], top[keep], strict=True)]
    points = (*lower, *reversed(upper))
    us, vs = [a for a, _ in points], [b for _, b in points]
    fill = COLOURS.get(p.kind, (0.8, 0.8, 0.8))
    return Rect(min(us), min(vs), max(us) - min(us), max(vs) - min(vs), fill, p.name, points)


def _circle(r: float, steps: int = 96) -> tuple[tuple[float, float], ...]:
    return tuple(
        (r * math.cos(2 * math.pi * k / steps), r * math.sin(2 * math.pi * k / steps))
        for k in range(steps)
    )


type Outline = tuple[tuple[float, float], ...]


def _bounded(
    points: Outline, fill: tuple[float, float, float], name: str, holes: tuple[Outline, ...] = ()
) -> Rect:
    us, vs = [a for a, _ in points], [b for _, b in points]
    return Rect(min(us), min(vs), max(us) - min(us), max(vs) - min(vs), fill, name, points, holes)


def _revolved_cut(p: Part, axis: Axis, at: float) -> list[Rect]:
    """A part turned about the z axis, cut through the axis (x = 0 or y = 0: its outline and its
    mirror, joined where the outline runs along the axis) or across it (z = at: discs and rings,
    seen from above)."""
    assert p.revolve is not None
    fill = COLOURS.get(p.kind, (0.8, 0.8, 0.8))
    outline = p.revolve
    sides = p.sides

    def ring(r: float) -> Outline:
        return _circle(r) if sides is None else tuple(polygon_corners(sides, r))

    if axis == 2:
        rects: list[Rect] = []
        for a, b in _crossings(outline, 1, at):
            hole = (ring(a),) if a > 1e-6 else ()
            rects.append(_bounded(ring(b), fill, p.name, hole))
        return rects
    if abs(at) > 1e-6:
        return []  # sections are only drawn through the middle
    if sides is not None:
        # A polygon cut through its centre: r out to the corners, scaled to its reach along the cut
        reach = polygon_reach(sides, 0.0 if axis == 1 else math.pi / 2)
        outline = tuple((r * reach, z) for r, z in outline)
    n = len(outline)
    on_axis = [
        k for k in range(n) if abs(outline[k][0]) < 1e-6 and abs(outline[(k + 1) % n][0]) < 1e-6
    ]
    if on_axis:
        # Start just after the edge along the axis and end at it, then add the mirror image
        k = on_axis[0]
        half = outline[k + 1 :] + outline[: k + 1]
        joined = (*half, *((-r, z) for r, z in reversed(half)))
        return [_bounded(joined, fill, p.name)]
    mirror = tuple((-r, z) for r, z in reversed(outline))
    return [_bounded(outline, fill, p.name), _bounded(mirror, fill, p.name)]


def _plan_cut(p: Part, axis: Axis, at: float, steps: int = 96) -> list[Rect]:
    """A curved plan's layer (Part.plan) cut: seen from above at z = at, its outline less the
    inner one; or across (y = at) or along (x = at), each span of it between its bottom and top,
    a dome's sphere where it has one."""
    assert p.plan is not None
    fill = COLOURS.get(p.kind, (0.8, 0.8, 0.8))
    if axis == 2:
        if p.dome is not None or not p.lo[2] <= at <= p.hi[2]:
            return []
        return [_bounded(p.plan, fill, p.name, (p.inner,) if p.inner else ())]
    along: Literal[0, 1] = 0 if axis == 0 else 1
    ends = [e for a, b in _crossings(p.plan, along, at) for e in (a, b)]
    ends += [e for a, b in _crossings(p.inner or (), along, at) for e in (a, b)]
    ends.sort()
    rects: list[Rect] = []
    for a, b in zip(ends[::2], ends[1::2], strict=False):
        if p.dome is None:
            rects.append(Rect(a, p.lo[2], b - a, p.hi[2] - p.lo[2], fill, p.name))
            continue
        d, s = p.dome, np.linspace(a, b, steps + 1)
        x, y = (np.full_like(s, at), s) if axis == 0 else (s, np.full_like(s, at))
        top = d.heights(x, y, d.radius + d.thickness)
        floor = np.full_like(s, p.lo[2])
        bottom = floor if p.cap else np.maximum(d.heights(x, y, d.radius), floor)
        keep = top > bottom + 1e-6
        if not keep.any():
            continue
        lower = [(float(u), float(z)) for u, z in zip(s[keep], bottom[keep], strict=True)]
        upper = [(float(u), float(z)) for u, z in zip(s[keep], top[keep], strict=True)]
        rects.append(_bounded((*lower, *reversed(upper)), fill, p.name))
    return rects


def _cut(parts: list[Part], axis: Axis, at: float, u: Axis, v: Axis) -> list[Rect]:
    rects: list[Rect] = []
    for p in parts:
        fill = COLOURS.get(p.kind, (0.8, 0.8, 0.8))
        if p.plan is not None:
            rects += _plan_cut(p, axis, at)
            continue
        if p.revolve is not None:
            rects += _revolved_cut(p, axis, at)
            continue
        if p.dome is not None:
            if axis != 2 and abs(at) < 1e-6 and (rect := _dome_cut(p, axis)):
                rects.append(rect)
            continue  # a dome is all above the springline, so the plan misses it
        if p.profile is not None and p.across:
            # A (y, z) outline run along x: whole along the kiln (x = at), else crossed
            if axis == 0:
                if p.lo[0] - 1e-6 <= at <= p.hi[0] + 1e-6:
                    rects.append(_bounded(p.profile, fill, p.name))
                continue
            # Across (y = at: spans of z) or the plan (z = at: spans of y), both drawn from x
            for a, b in _crossings(p.profile, 0 if axis == 1 else 1, at):
                rects.append(Rect(p.lo[0], a, p.length_run, b - a, fill, p.name))
            continue
        if p.profile is not None and axis == 1:
            if p.lo[1] - 1e-6 <= at <= p.hi[1] + 1e-6:
                x0, z0, x1, z1 = p.lo[0], p.lo[2], p.hi[0], p.hi[2]
                rects.append(Rect(x0, z0, x1 - x0, z1 - z0, fill, p.name, p.profile))
            continue
        if p.profile is not None:
            # Along the kiln (x = at: spans of z, drawn y–z) or the plan (z = at: spans of x)
            for a, b in _crossings(p.profile, 0 if axis == 0 else 1, at):
                if axis == 0:
                    rects.append(Rect(p.lo[1], a, p.length_y, b - a, fill, p.name))
                else:
                    rects.append(Rect(a, p.lo[1], b - a, p.length_y, fill, p.name))
            continue
        if p.arch is not None:
            if p.lo[axis] - 1e-6 <= at <= p.hi[axis] + 1e-6 and (rect := _arch_cut(p, axis)):
                rects.append(rect)
            continue
        if p.lo[axis] - 1e-6 <= at <= p.hi[axis] + 1e-6:
            rects.append(
                Rect(
                    p.lo[u],
                    p.lo[v],
                    p.hi[u] - p.lo[u],
                    p.hi[v] - p.lo[v],
                    COLOURS.get(p.kind, (0.8, 0.8, 0.8)),
                    p.name,
                )
            )
    return rects


def section_views(kiln: Kiln, element_rows: int = 0, coil_mm: float = 0.0) -> list[View]:
    """Three sections through the middle: front (x–z), side (y–z) and plan (x–y)."""
    from kilndesigner.bend import bent

    views = _section_views(kiln, element_rows, coil_mm)
    if bent(kiln):
        for view in views:
            view.title += ", the bend drawn straightened"
    return views


def _section_views(kiln: Kiln, element_rows: int, coil_mm: float) -> list[View]:
    us = kiln.units == "us"
    parts = lining_parts(kiln)
    if kiln.chamber.shape == "round":
        return _round_views(kiln, parts, us, element_rows, coil_mm)
    if in_a_row(kiln):
        return _run_views(kiln, parts, us)
    w, d, h = (si(getattr(kiln.chamber, n), "mm") for n in ("width", "depth", "height"))
    walls = kiln.heat.electric.walls if kiln.heat.electric else []
    rows = [h * (i + 0.5) / element_rows for i in range(element_rows)]

    front = View(
        "Section A–A: across the kiln, looking at the back", _cut(parts, 1, 0.0, 0, 2), [], []
    )
    side = View(
        "Section B–B: along the kiln, looking from the right", _cut(parts, 0, 0.0, 1, 2), [], []
    )
    plan = View("Section C–C: plan at mid-height", _cut(parts, 2, h / 2, 0, 1), [], [])

    # A catenary's inside width is its span at the floor; at mid-height it is narrower
    catenary = CatenaryCurve(w, h) if isinstance(kiln.roof, CatenaryArch) else None
    for view, inner_w in ((front, w), (side, d)):
        x0, y0, x1, y1 = view.bounds()
        across = (
            Dimension(
                -inner_w / 2, 0, inner_w / 2, 0, -0.12 * h,
                f"{length_text(inner_w, us)} inside, at the floor",
            )
            if catenary is not None and view is front
            else Dimension(
                -inner_w / 2, h, inner_w / 2, h, -0.35 * h, f"{length_text(inner_w, us)} inside"
            )
        )  # fmt: skip
        view.dims += [
            across,
            Dimension(x0, y0, x1, y0, 0.12 * h, f"{length_text(x1 - x0, us)} outside"),
            Dimension(
                -inner_w / 2, 0, -inner_w / 2, h, 0.3 * inner_w, f"{length_text(h, us)} inside"
            ),
            Dimension(x1, y0, x1, y1, 0.12 * (x1 - x0), f"{length_text(y1 - y0, us)} outside"),
        ]
    x0, y0, x1, y1 = plan.bounds()
    plan_w = w
    if catenary is not None:
        plan_w = 2 * catenary.a * math.acosh((catenary.height + catenary.a - h / 2) / catenary.a)
    plan.dims += [
        Dimension(
            -plan_w / 2, -d / 2, plan_w / 2, -d / 2, -0.3 * d, f"{length_text(plan_w, us)} inside"
        ),
        Dimension(x0, y0, x1, y0, 0.12 * d, f"{length_text(x1 - x0, us)} outside"),
        Dimension(x1, y0, x1, y1, 0.12 * (x1 - x0), f"{length_text(y1 - y0, us)} outside"),
    ]
    for z in rows:
        if "left" in walls:
            front.circles.append(Circle(-w / 2, z, coil_mm / 2))
        if "right" in walls:
            front.circles.append(Circle(w / 2, z, coil_mm / 2))
        if "back" in walls:
            side.circles.append(Circle(d / 2, z, coil_mm / 2))
        if "front" in walls:
            side.circles.append(Circle(-d / 2, z, coil_mm / 2))
    if any(p.tilt for p in parts):
        _on_the_slope(kiln, parts, (front, side, plan), us)
    return [front, side, plan]


def _on_the_slope(kiln: Kiln, parts: list[Part], views: tuple[View, View, View], us: bool) -> None:
    """A single chamber on a slope: the section along it drawn up the slope, the section across
    it and the plan square to the floor, as the bricks are laid."""
    front, side, plan = views
    tilt = {p.name: p for p in parts}
    turned: list[Rect] = []
    for r in side.rects:
        p = tilt[r.layer]
        x1, y1 = r.x + r.w, r.y + r.h
        corners = r.points or ((r.x, r.y), (x1, r.y), (x1, y1), (r.x, y1))
        turned.append(_bounded(tuple(p.tilted(u, v) for u, v in corners), r.fill, r.layer))
    side.rects = turned
    slope = si(kiln.chamber.slope, "degree") if kiln.chamber.slope is not None else 0.0
    side.title = f"Section B–B: along the kiln, up its {slope:.3g}° slope, looking from the right"
    front.title = "Section A–A: across the kiln, square to its sloping floor, looking at the back"
    plan.title = "Section C–C: plan at mid-height, laid out along the slope"
    x0, y0, x1, y1 = side.bounds()
    h = y1 - y0
    side.dims = [
        Dimension(x0, y0, x1, y0, 0.12 * h, f"{length_text(x1 - x0, us)} outside, level"),
        Dimension(x1, y0, x1, y1, 0.06 * (x1 - x0), f"{length_text(h, us)} outside, rise included"),
    ]
    side.circles = []


def _round_views(
    kiln: Kiln, parts: list[Part], us: bool, element_rows: int = 0, coil_mm: float = 0.0
) -> list[View]:
    """A round chamber is the same through its axis whichever way it's cut: one section through
    the axis, and the plan at mid-height. The element grooves are cut in the section where the
    elements' quarters of the ring cross it (geometry.round_groove)."""
    from kilndesigner.geometry import hot_face_reach

    d, h = si(kiln.chamber.width, "mm"), si(kiln.chamber.height, "mm")
    section = View("Section A–A: through the axis, looking at the back", _cut(parts, 1, 0.0, 0, 2),
                   [], [])  # fmt: skip
    plan = View("Section C–C: plan at mid-height", _cut(parts, 2, h / 2, 0, 1), [], [])
    x0, y0, x1, y1 = section.bounds()
    section.dims += [
        Dimension(-d / 2, 0, d / 2, 0, -0.12 * h, f"{length_text(d, us)} across inside"),
        Dimension(x0, y0, x1, y0, 0.12 * h, f"{length_text(x1 - x0, us)} outside"),
        Dimension(-d / 2, 0, -d / 2, h, 0.3 * d, f"{length_text(h, us)} inside"),
        Dimension(x1, y0, x1, y1, 0.12 * (x1 - x0), f"{length_text(y1 - y0, us)} outside"),
    ]
    x0, y0, x1, _ = plan.bounds()
    plan.dims += [
        Dimension(-d / 2, 0, d / 2, 0, 0.0, f"{length_text(d, us)} across inside"),
        Dimension(x0, y0, x1, y0, 0.12 * d, f"{length_text(x1 - x0, us)} across outside"),
    ]
    walls = kiln.heat.electric.walls if kiln.heat.electric else []
    x = hot_face_reach(kiln, 0.0)  # the hot face where the cut crosses it
    for i in range(element_rows):
        z = h * (i + 0.5) / element_rows
        for wall, sign in (("left", -1), ("right", 1)):
            if wall in walls:
                section.circles.append(Circle(sign * x, z, coil_mm / 2))
    return [section, plan]


def _run_views(kiln: Kiln, parts: list[Part], us: bool) -> list[View]:
    """Chambers in a row: across the first chamber, along the whole run (its steps up the slope
    and every chamber's arch), and the plan of each chamber at its own mid-height."""
    from kilndesigner.run_parts import run_layout

    run = run_layout(kiln)
    w, d, h, n = run.width, run.depth, run.height, run.chambers
    front = View("Section A–A: across the first chamber, looking at the back",
                 _cut(parts, 1, 0.0, 0, 2), [], [])  # fmt: skip
    side = View("Section B–B: along the kiln, looking from the right", _cut(parts, 0, 0.0, 1, 2),
                [], [])  # fmt: skip
    if run.step > 1e-6:
        rects: list[Rect] = []
        for i in range(n):
            mine = [p for p in parts if p.chamber == i + 1]
            rects += _cut(mine, 2, run.floor(i) + h / 2, 0, 1)
        plan = View("Section C–C: plan of each chamber at its mid-height", rects, [], [])
    else:
        plan = View("Section C–C: plan at mid-height", _cut(parts, 2, h / 2, 0, 1), [], [])
    x0, y0, x1, y1 = front.bounds()
    front.dims += [
        Dimension(-w / 2, h, w / 2, h, -0.35 * h, f"{length_text(w, us)} inside"),
        Dimension(x0, y0, x1, y0, 0.12 * h, f"{length_text(x1 - x0, us)} outside"),
        Dimension(-w / 2, 0, -w / 2, h, 0.3 * w, f"{length_text(h, us)} inside"),
        Dimension(x1, y0, x1, y1, 0.12 * (x1 - x0), f"{length_text(y1 - y0, us)} outside"),
    ]
    x0, y0, x1, y1 = side.bounds()
    side.dims += [
        Dimension(-d / 2, 0, d / 2, 0, 0.7 * h, f"{length_text(d, us)} inside, each chamber"),
        Dimension(x0, y0, x1, y0, 0.25 * h, f"{length_text(x1 - x0, us)} outside"),
        Dimension(-d / 2, 0, -d / 2, h, -0.6 * d, f"{length_text(h, us)} to the springline"),
        Dimension(x1, y0, x1, y1, 0.04 * (x1 - x0), f"{length_text(y1 - y0, us)} outside"),
    ]
    x0, y0, x1, y1 = plan.bounds()
    start = -d / 2
    plan.dims += [
        Dimension(-w / 2, start, w / 2, start, -0.3 * d, f"{length_text(w, us)} inside"),
        Dimension(x0, y0, x1, y0, 0.12 * d, f"{length_text(x1 - x0, us)} outside"),
        Dimension(x1, y0, x1, y1, 0.12 * (x1 - x0), f"{length_text(y1 - y0, us)} outside"),
    ]
    return [front, side, plan]


def _hex(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{round(c * 255):02x}" for c in rgb)


def text_size(view: View) -> float:
    """The dimension text's height for a view (mm, in the view's own units): a twentieth of the
    view's longer side for a squarish view, as before; for a long one, a twentieth of three times
    its shorter side, so the text stays in scale with the section it labels, but never under 1.5 %
    of the longer side, so it still reads when the page fits the whole length."""
    x0, y0, x1, y1 = view.bounds()
    long, short = max(x1 - x0, y1 - y0), min(x1 - x0, y1 - y0)
    return max(0.05 * min(long, 3 * short), 0.015 * long)


def view_svg(view: View, font: float | None = None) -> str:
    """An SVG of a view, y up, with a margin for the dimensions."""
    x0, y0, x1, y1 = view.bounds()
    size = max(x1 - x0, y1 - y0)
    font = font or text_size(view)
    # Room for every dimension line and its text, and a margin round it all
    for dim in view.dims:
        if abs(dim.y2 - dim.y1) < 1e-9:
            line = dim.y1 - dim.offset
            y0, y1 = min(y0, line - 1.5 * font), max(y1, line + 1.5 * font)
        else:
            line = dim.x1 + dim.offset
            x0, x1 = min(x0, line - 1.5 * font), max(x1, line + 1.5 * font)
    margin = max(2 * font, 0.05 * size)
    vx, vy = x0 - margin, -(y1 + margin)
    vw, vh = (x1 - x0) + 2 * margin, (y1 - y0) + 2 * margin
    stroke = size * 0.002
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}">',
        f'<g stroke="#222" stroke-width="{stroke:.2f}">',
    ]
    for r in view.rects:
        title = f"<title>{escape(r.layer)}</title>"
        if r.holes:
            path = " ".join(
                "M " + " L ".join(f"{x:.2f},{-y:.2f}" for x, y in ring) + " Z"
                for ring in (r.points, *r.holes)
            )
            out.append(f'<path d="{path}" fill-rule="evenodd" fill="{_hex(r.fill)}">{title}</path>')
            continue
        if r.points:
            pts = " ".join(f"{x:.2f},{-y:.2f}" for x, y in r.points)
            out.append(f'<polygon points="{pts}" fill="{_hex(r.fill)}">{title}</polygon>')
            continue
        out.append(
            f'<rect x="{r.x:.2f}" y="{-(r.y + r.h):.2f}" width="{r.w:.2f}" height="{r.h:.2f}" '
            f'fill="{_hex(r.fill)}">{title}</rect>'
        )
    for c in view.circles:
        out.append(
            f'<circle cx="{c.x:.2f}" cy="{-c.y:.2f}" r="{c.r:.2f}" fill="#8c8c94" '
            f'stroke-width="{stroke / 2:.2f}"/>'
        )
    out.append("</g>")
    out.append(f'<g stroke="#1a4f8b" stroke-width="{stroke:.2f}" fill="#1a4f8b">')
    for dim in view.dims:
        out.extend(_dimension_svg(dim, font, stroke))
    out.append("</g></svg>")
    return "\n".join(out)


def _dimension_svg(dim: Dimension, font: float, stroke: float) -> list[str]:
    horizontal = abs(dim.y2 - dim.y1) < 1e-9
    tick = font * 0.4
    if horizontal:
        y = dim.y1 - dim.offset
        lines = [
            (dim.x1, dim.y1, dim.x1, y),
            (dim.x2, dim.y2, dim.x2, y),
            (dim.x1, y, dim.x2, y),
            (dim.x1 - tick, y - tick, dim.x1 + tick, y + tick),
            (dim.x2 - tick, y - tick, dim.x2 + tick, y + tick),
        ]
        tx, ty, rot = (dim.x1 + dim.x2) / 2, y + font * 0.4, 0
    else:
        x = dim.x1 + dim.offset
        lines = [
            (dim.x1, dim.y1, x, dim.y1),
            (dim.x2, dim.y2, x, dim.y2),
            (x, dim.y1, x, dim.y2),
            (x - tick, dim.y1 - tick, x + tick, dim.y1 + tick),
            (x - tick, dim.y2 - tick, x + tick, dim.y2 + tick),
        ]
        tx, ty, rot = x - font * 0.4, (dim.y1 + dim.y2) / 2, -90
    out = [f'<line x1="{a:.2f}" y1="{-b:.2f}" x2="{c:.2f}" y2="{-e:.2f}"/>' for a, b, c, e in lines]
    out.append(
        f'<text x="{tx:.2f}" y="{-ty:.2f}" font-size="{font:.2f}" text-anchor="middle" '
        f'stroke="none" font-family="sans-serif" '
        f'transform="rotate({rot} {tx:.2f} {-ty:.2f})">{escape(dim.text)}</text>'
    )
    return out


def course_plan_svg(plan: LayerPlan, us: bool) -> str:
    """Every brick and cut piece of one layer, course by course, as seen from inside the kiln."""
    run, span = plan.run_length, plan.span
    size = max(run, span)
    font = size * 0.03
    stroke = size * 0.0015
    margin = size * 0.08
    vx, vy, vw, vh = -margin, -(span + margin * 0.5), run + margin * 1.5, span + margin
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}">',
        f'<g stroke="#222" stroke-width="{stroke:.2f}">',
    ]
    base = _hex(COLOURS.get(plan.part.kind, (0.85, 0.85, 0.85)))
    for course in plan.courses:
        for piece in course.pieces:
            fill = base if piece.is_whole else "#e8a65d"
            out.append(
                f'<rect x="{piece.start:.2f}" y="{-(course.offset + piece.height):.2f}" '
                f'width="{piece.length:.2f}" height="{piece.height:.2f}" fill="{fill}"/>'
            )
    out.append("</g>")
    if plan.circle is not None:  # a round kiln's floor or roof: the line its rows are cut to
        c = plan.circle
        out.append(
            f'<circle cx="{run / 2:.2f}" cy="{-span / 2:.2f}" r="{c:.2f}" fill="none" '
            f'stroke="#1a4f8b" stroke-width="{stroke * 2:.2f}" '
            f'stroke-dasharray="{size * 0.01:.2f}"/>'
        )
    for course in plan.courses:
        y = course.offset + course.pieces[0].height / 2 if course.pieces else course.offset
        out.append(
            f'<text x="{-font * 0.5:.2f}" y="{-y + font * 0.35:.2f}" font-size="{font:.2f}" '
            f'text-anchor="end" font-family="sans-serif" fill="#444">{course.index}</text>'
        )
    out.append("</svg>")
    return "\n".join(out)


SHAPE_TONES = ("#9a6fb0", "#5f8fc4", "#5ba88a", "#d1a23f")
"""Tapered shapes in a ring plan, tightest first; straights take the material's colour."""

WEDGE_JOINTS = "wedge joints, filled with mortar"
MORTAR_TONE = "#b8b2a7"


def _mortar_course(
    plan: RingPlan, order: list[str], cx: float, shift: float, tone: dict[str, str]
) -> list[str]:
    """One course of a mortar ring as it is laid (rings.straight_ring; Olsen p.45, Fig. 2-13):
    each straight, or the closer, a rectangle whose inside face is a chord of the inside circle,
    and between each two the wedge-shaped joint that opens behind them, drawn as its triangle.
    ``shift`` turns the course by that part of a straight's angle."""
    r, d = plan.inside_radius, plan.depth

    def chord(shape: str) -> float:  # the angle a brick's inside face turns
        length = plan.ring.length if shape == CLOSER and plan.ring.length else STRAIGHT * IN
        return 2 * math.asin(length / (2 * r))

    def at(radius: float, angle: float) -> tuple[float, float]:
        return radius * math.cos(angle), radius * math.sin(angle)

    def svg(pts: list[tuple[float, float]], fill: str) -> str:
        points = " ".join(f"{cx + x:.2f},{-y:.2f}" for x, y in pts)
        return f'<polygon points="{points}" fill="{fill}"/>'

    bricks: list[tuple[tuple[float, float], ...]] = []
    out: list[str] = []
    b0 = shift * chord(FAMILIES["mortar"].straight)
    for shape in order:
        b1 = b0 + chord(shape)
        mid = (b0 + b1) / 2
        nx, ny = math.cos(mid), math.sin(mid)  # the chord's outward normal
        p0, p1 = at(r, b0), at(r, b1)
        q0, q1 = (p0[0] + d * nx, p0[1] + d * ny), (p1[0] + d * nx, p1[1] + d * ny)
        bricks.append((p0, p1, q1, q0))
        out.append(svg([p0, p1, q1, q0], tone[shape]))
        b0 = b1
    for (_, p1, q1, _), (_, _, _, q0) in itertools.pairwise([*bricks, bricks[0]]):
        out.append(svg([p1, q1, q0], tone[WEDGE_JOINTS]))
    return out


def ring_plan_svg(plan: RingPlan, us: bool) -> str:
    """One ring of a round wall seen from above: every brick of an odd course and of an even one,
    which starts half a brick round so that the joints don't line up; a cut ring's courses are
    stacked in line, so it shows one. A tapered or cut brick's thick end is on the outside circle
    and its thin end on the inside, laid in turn round the ring; a mortar ring's straights are
    drawn square, their inside faces on the curve, with the wedge joints open between them."""
    r_in, r_out = plan.inside_radius, plan.inside_radius + plan.depth
    family = FAMILIES[plan.series]
    thin = {t.name: t.thin * IN for t in family.tapers} | {family.straight: family.thick * IN}
    tapers = [t.name for t in family.tapers]
    if plan.ring.length is not None and plan.series in ("mortar", "cut", "cut2.5", "cut3"):
        # The closer: a straight cut short, its inside face the chord it closes
        thin[CLOSER] = plan.ring.length
        tapers.append(CLOSER)
    tone = {name: SHAPE_TONES[k % len(SHAPE_TONES)] for k, name in enumerate(tapers)}
    tone[family.straight] = _hex(COLOURS.get(plan.part.kind, (0.85, 0.85, 0.85)))
    order = plan.order()
    inner_total = sum(thin[s] for s in order)
    gap = r_out * 0.35  # between the two plans
    size = 4 * r_out + gap
    font = size * 0.02
    stroke = size * 0.0008
    legend = [(name, f"{n} {name}") for name, n in plan.ring.counts if n]
    if plan.series == "mortar":  # the joints open behind the straights, drawn as they are
        tone[WEDGE_JOINTS] = MORTAR_TONE
        legend.append((WEDGE_JOINTS, WEDGE_JOINTS))
    vx, vy = -r_out - font, -(r_out + font * 3)
    vw, vh = size + 2 * font, 2 * r_out + font * (7 + 1.6 * len(legend))
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}">',
        f'<g stroke="#222" stroke-width="{stroke:.2f}">',
    ]
    # Cut rings stack course on course, facets in line, for a smooth wall (the user: in small
    # kilns, electric especially, smooth walls matter more than staggered joints)
    staggered = (("Odd courses", 0.0), ("Even courses", 0.5))
    courses = (("Every course", 0.0),) if plan.series.startswith("cut") else staggered
    mortared = plan.series == "mortar"
    for k, (label, shift) in enumerate(courses):
        cx = k * (2 * r_out + gap)
        if mortared:
            out += _mortar_course(plan, order, cx, shift, tone)
        step = 2 * math.pi / len(order)  # round the outside, every brick shows its thick end
        inner = 0.0
        for j, shape in enumerate([] if mortared else order):
            a0, a1 = (j + shift) * step, (j + 1 + shift) * step
            b0 = (inner + shift * thin[order[0]]) / inner_total * 2 * math.pi
            inner += thin[shape]
            b1 = (inner + shift * thin[order[0]]) / inner_total * 2 * math.pi
            pts = [
                (r_out * math.cos(a0), r_out * math.sin(a0)),
                (r_out * math.cos(a1), r_out * math.sin(a1)),
                (r_in * math.cos(b1), r_in * math.sin(b1)),
                (r_in * math.cos(b0), r_in * math.sin(b0)),
            ]
            points = " ".join(f"{cx + x:.2f},{-y:.2f}" for x, y in pts)
            out.append(f'<polygon points="{points}" fill="{tone[shape]}"/>')
        out.append(
            f'<text x="{cx:.2f}" y="{-(r_out + font):.2f}" font-size="{font:.2f}" '
            f'text-anchor="middle" stroke="none" font-family="sans-serif" fill="#444">'
            f"{label}</text>"
        )
    out.append("</g>")
    y = r_out + font * 2.5
    for name, text in legend:
        out.append(
            f'<rect x="{-r_out:.2f}" y="{y - font * 0.8:.2f}" width="{font:.2f}" '
            f'height="{font:.2f}" fill="{tone[name]}" stroke="#222" stroke-width="{stroke:.2f}"/>'
        )
        out.append(
            f'<text x="{-r_out + font * 1.5:.2f}" y="{y:.2f}" font-size="{font:.2f}" '
            f'font-family="sans-serif" fill="#444">{escape(text)}</text>'
        )
        y += font * 1.6
    out.append(
        f'<text x="{-r_out:.2f}" y="{y:.2f}" font-size="{font:.2f}" font-family="sans-serif" '
        f'fill="#444">{escape(length_text(2 * r_in, us))} across inside, '
        f"{escape(length_text(plan.depth, us))} through</text>"
    )
    out.append("</svg>")
    return "\n".join(out)


def write_dxf(views: list[View], path: str, us: bool) -> None:
    """The sections side by side in one DXF, one CAD layer per lining part, in millimetres."""
    from ezdxf.filemanagement import new  # pyright: ignore[reportMissingTypeStubs]

    doc = new(units=4)  # 4 = millimetres
    for name in ("dimensions", "elements", "titles"):
        doc.layers.add(name)
    msp = doc.modelspace()
    offset = 0.0
    for view in views:
        x0, y0, x1, _ = view.bounds()
        text = text_size(view)
        dx = offset - x0
        for r in view.rects:
            layer = r.layer.replace("/", "_")
            if layer not in doc.layers:
                doc.layers.add(layer)
            pts = list(r.points) or [
                (r.x, r.y), (r.x + r.w, r.y), (r.x + r.w, r.y + r.h), (r.x, r.y + r.h)
            ]  # fmt: skip
            for outline in (pts, *r.holes):
                msp.add_lwpolyline(
                    [(x + dx, y) for x, y in outline], close=True, dxfattribs={"layer": layer}
                )
        for c in view.circles:
            msp.add_circle((c.x + dx, c.y), c.r, dxfattribs={"layer": "elements"})
        for dim in view.dims:
            horizontal = abs(dim.y2 - dim.y1) < 1e-9
            base = (
                ((dim.x1 + dim.x2) / 2 + dx, dim.y1 - dim.offset)
                if horizontal
                else (dim.x1 + dim.offset + dx, (dim.y1 + dim.y2) / 2)
            )
            msp.add_linear_dim(
                base=base,
                p1=(dim.x1 + dx, dim.y1),
                p2=(dim.x2 + dx, dim.y2),
                angle=0 if horizontal else 90,
                text=dim.text,
                override={"dimtxt": text, "dimasz": text * 0.6},
                dxfattribs={"layer": "dimensions"},
            ).render()
        msp.add_text(view.title, height=text, dxfattribs={"layer": "titles"}).set_placement(
            (offset, y0 - 6 * text)
        )
        offset += (x1 - x0) * 1.6
    doc.saveas(path)
