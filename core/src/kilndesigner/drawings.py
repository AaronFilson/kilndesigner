"""2D drawings for the plans: sections through the kiln, and brick course plans.

Drawings are made from the same lining parts as the 3D model (:func:`lining_parts`), cut by a
plane, so the plans and the model can't disagree. SVG is used for the PDF; DXF for CAD.
Model units are millimetres; dimensions are labelled in the design's units.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal
from xml.sax.saxutils import escape

import numpy as np

from kilndesigner.geometry import COLOURS, Part, arch_outline, lining_parts
from kilndesigner.masonry import IN, LayerPlan
from kilndesigner.model import CatenaryArch, Kiln
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
    if axis == 0:
        bottom = p.lo[2] if p.cap else a.centre_z + a.radius
        top = a.centre_z + a.radius + a.thickness
        return Rect(p.lo[1], bottom, p.length_y, top - bottom, fill, p.name)
    return None


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
    top = d.heights(s, zero, d.radius + d.thickness)
    inside = d.heights(s, zero, d.radius)
    bottom = np.full_like(s, springline) if p.cap else np.maximum(inside, springline)
    keep = top > bottom + 1e-6
    if not keep.any():
        return None
    lower = [(float(a), float(b)) for a, b in zip(s[keep], bottom[keep], strict=True)]
    upper = [(float(a), float(b)) for a, b in zip(s[keep], top[keep], strict=True)]
    points = (*lower, *reversed(upper))
    us, vs = [a for a, _ in points], [b for _, b in points]
    fill = COLOURS.get(p.kind, (0.8, 0.8, 0.8))
    return Rect(min(us), min(vs), max(us) - min(us), max(vs) - min(vs), fill, p.name, points)


def _cut(parts: list[Part], axis: Axis, at: float, u: Axis, v: Axis) -> list[Rect]:
    rects: list[Rect] = []
    for p in parts:
        fill = COLOURS.get(p.kind, (0.8, 0.8, 0.8))
        if p.dome is not None:
            if axis != 2 and abs(at) < 1e-6 and (rect := _dome_cut(p, axis)):
                rects.append(rect)
            continue  # a dome is all above the springline, so the plan misses it
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
    us = kiln.units == "us"
    parts = lining_parts(kiln)
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
    return [front, side, plan]


def _hex(rgb: tuple[float, float, float]) -> str:
    return "#" + "".join(f"{round(c * 255):02x}" for c in rgb)


def view_svg(view: View, font: float | None = None) -> str:
    """An SVG of a view, y up, with a margin for the dimensions."""
    x0, y0, x1, y1 = view.bounds()
    size = max(x1 - x0, y1 - y0)
    font = font or size * 0.05
    margin = size * 0.25
    vx, vy = x0 - margin, -(y1 + margin)
    vw, vh = (x1 - x0) + 2 * margin, (y1 - y0) + 2 * margin
    stroke = size * 0.002
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.2f} {vy:.2f} {vw:.2f} {vh:.2f}">',
        f'<g stroke="#222" stroke-width="{stroke:.2f}">',
    ]
    for r in view.rects:
        title = f"<title>{escape(r.layer)}</title>"
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
    for course in plan.courses:
        y = course.offset + course.pieces[0].height / 2 if course.pieces else course.offset
        out.append(
            f'<text x="{-font * 0.5:.2f}" y="{-y + font * 0.35:.2f}" font-size="{font:.2f}" '
            f'text-anchor="end" font-family="sans-serif" fill="#444">{course.index}</text>'
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
        dx = offset - x0
        for r in view.rects:
            layer = r.layer.replace("/", "_")
            if layer not in doc.layers:
                doc.layers.add(layer)
            pts = list(r.points) or [
                (r.x, r.y), (r.x + r.w, r.y), (r.x + r.w, r.y + r.h), (r.x, r.y + r.h)
            ]  # fmt: skip
            msp.add_lwpolyline(
                [(x + dx, y) for x, y in pts], close=True, dxfattribs={"layer": layer}
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
                dxfattribs={"layer": "dimensions"},
            ).render()
        msp.add_text(
            view.title, height=(x1 - x0) * 0.03, dxfattribs={"layer": "titles"}
        ).set_placement((offset, y0 - (x1 - x0) * 0.3))
        offset += (x1 - x0) * 1.6
    doc.saveas(path)
