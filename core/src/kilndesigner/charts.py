"""Simple line charts as SVG, for the plans: no plotting library, deterministic output."""

from __future__ import annotations

import math
from dataclasses import dataclass
from xml.sax.saxutils import escape

PALETTE = ("#1a4f8b", "#c0611b", "#7a7a7a", "#2e7d32")


@dataclass(frozen=True)
class Series:
    label: str
    points: list[tuple[float, float]]
    dashed: bool = False


@dataclass(frozen=True)
class Marker:
    x: float
    label: str


def _ticks(lo: float, hi: float, count: int = 5) -> list[float]:
    """Round tick values (1, 2, 2.5 or 5 × a power of ten) covering lo..hi."""
    raw = (hi - lo) / count
    magnitude = 10 ** math.floor(math.log10(raw))
    step = next(m * magnitude for m in (1, 2, 2.5, 5, 10) if m * magnitude >= raw)
    first = (lo // step) * step
    out: list[float] = []
    t = first
    while t <= hi + 1e-9:
        if t >= lo - 1e-9:
            out.append(round(t, 10))
        t += step
    return out


def line_chart(
    series: list[Series],
    *,
    x_label: str,
    y_label: str,
    markers: list[Marker] | None = None,
    y_format: str = "{:g}",
    width: float = 640,
    height: float = 300,
) -> str:
    left, right, top, bottom = 64.0, 16.0, 16.0, 46.0
    xs = [x for s in series for x, _ in s.points]
    ys = [y for s in series for _, y in s.points]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(0.0, min(ys)), max(ys) * 1.08
    pw, ph = width - left - right, height - top - bottom

    def px(x: float) -> float:
        return left + (x - x0) / (x1 - x0) * pw

    def py(y: float) -> float:
        return top + ph - (y - y0) / (y1 - y0) * ph

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'font-family="sans-serif" font-size="11">',
        f'<rect x="{left}" y="{top}" width="{pw}" height="{ph}" fill="none" stroke="#999"/>',
    ]
    for t in _ticks(y0, y1):
        out.append(
            f'<line x1="{left}" x2="{left + pw}" y1="{py(t):.1f}" y2="{py(t):.1f}" stroke="#e3e3e3"/>'
        )
        out.append(
            f'<text x="{left - 6}" y="{py(t) + 4:.1f}" text-anchor="end" fill="#444">'
            f"{escape(y_format.format(t))}</text>"
        )
    for t in _ticks(x0, x1, 6):
        out.append(
            f'<text x="{px(t):.1f}" y="{top + ph + 16}" text-anchor="middle" fill="#444">{t:g}</text>'
        )
    if y0 < 0 < y1:
        out.append(
            f'<line x1="{left}" x2="{left + pw}" y1="{py(0):.1f}" y2="{py(0):.1f}" stroke="#555"/>'
        )
    for m in markers or []:
        out.append(
            f'<line x1="{px(m.x):.1f}" x2="{px(m.x):.1f}" y1="{top}" y2="{top + ph}" '
            'stroke="#2e7d32" stroke-dasharray="4 3"/>'
        )
        out.append(
            f'<text x="{px(m.x) + 4:.1f}" y="{top + 12}" fill="#2e7d32">{escape(m.label)}</text>'
        )
    for i, s in enumerate(series):
        colour = PALETTE[i % len(PALETTE)]
        path = " ".join(f"{px(x):.1f},{py(y):.1f}" for x, y in s.points)
        dash = ' stroke-dasharray="6 4"' if s.dashed else ""
        out.append(
            f'<polyline points="{path}" fill="none" stroke="{colour}" stroke-width="2"{dash}/>'
        )
        ly = top + 14 + 15 * i
        out.append(
            f'<line x1="{left + 10}" x2="{left + 30}" y1="{ly + 14}" y2="{ly + 14}" stroke="{colour}" stroke-width="2"{dash}/>'
        )
        out.append(f'<text x="{left + 36}" y="{ly + 18}" fill="#222">{escape(s.label)}</text>')
    out.append(
        f'<text x="{left + pw / 2}" y="{height - 8}" text-anchor="middle" fill="#222">{escape(x_label)}</text>'
    )
    out.append(
        f'<text transform="rotate(-90)" x="{-(top + ph / 2)}" y="16" text-anchor="middle" '
        f'fill="#222">{escape(y_label)}</text>'
    )
    out.append("</svg>")
    return "\n".join(out)
