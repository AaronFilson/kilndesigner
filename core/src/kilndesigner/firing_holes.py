"""Holes and burners the design places for firing (B2 in docs/planning/11-09-26.md): spy holes of
their own size in any chamber, in a wall or up through the roof's arch or dome; stoke holes into
the chambers themselves; and floor burners laid out by side and end, down the middle of the
floor, or set in from the corners.

Coordinates are inches, as hardware.py's, and millimetres on the way out: x across the width, y
from the front (negative) to the back, z up from the first chamber's floor.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from kilndesigner.gas import kiln_top_in
from kilndesigner.model import Burners, Kiln, PlacedHole
from kilndesigner.units import si
from kilndesigner.working import Finding

if TYPE_CHECKING:
    from kilndesigner.hardware import Faces, Hardware

MM = 25.4
FLOOR_BURNERS_SOURCE = "Olsen, The Kiln Book, 4th ed., p.171–174"
SPY_SOURCE = "Olsen, The Kiln Book, 4th ed., p.94 (Fig 4-36), p.141"
STOKE_SOURCE = "Olsen, The Kiln Book, 4th ed., Figs 4-7, 4-10, 4-46, 4-96"


def _chamber_y(kiln: Kiln, chamber: int) -> tuple[float, float]:
    """A chamber's middle along the run, and its floor's height (in), the first chamber's middle
    at y = 0 as the hardware lays a single chamber."""
    from kilndesigner.geometry import in_a_row

    if not in_a_row(kiln):
        return 0.0, 0.0
    from kilndesigner.run_parts import run_layout

    run = run_layout(kiln)
    k = chamber - 1
    return (run.front(k) + run.back(k)) / 2 / MM, run.floor(k) / MM


def place_holes(
    kiln: Kiln,
    f: Faces,
    hw: Hardware,
    holes: list[PlacedHole],
    kind: Literal["spy", "stoke"],
    first: int,
) -> int:
    """Cut each hole the design places: in a wall, through the hardware's port check where the
    kiln is one chamber, or on its chamber's stretch of the wall in a row; through the roof,
    straight up from the springline through whatever is over it. Returns how many were cut."""
    from kilndesigner.geometry import in_a_row
    from kilndesigner.hardware import Opening, PortSpot, _mm  # pyright: ignore[reportPrivateUsage]

    word = "Spy hole" if kind == "spy" else "Stoke hole"
    cut = 0
    for i, h in enumerate(holes):
        n = first + i
        w, ht = h.port.size_in()
        across = si(h.across, "in")
        if h.wall == "roof":
            y0, floor = _chamber_y(kiln, h.chamber)
            y = y0 + si(h.along, "in")
            z0 = si(kiln.chamber.height, "in") + floor
            z1 = kiln_top_in(kiln) + floor + 4
            box = _mm(((across - w / 2, y - ht / 2, z0), (across + w / 2, y + ht / 2, z1)))
            hw.openings.append(
                Opening(f"port/{kind}-roof-{n}", f"{word} {n}, through the roof", box,
                        2 if h.port.round else None)
            )  # fmt: skip
            cut += 1
            continue
        up = si(h.up, "in") if h.up is not None else 0.0
        spot = PortSpot(f"port/{kind}-{n}", f"{word} {n}", "spy", h.wall, across, up, w, ht,
                        h.port.round)  # fmt: skip
        if not in_a_row(kiln):
            cut += f.place(kiln, hw, spot)
            continue
        # In a row: on the chamber's own stretch of a side wall, from its middle; the front and
        # back walls are the first and last chambers'
        y0, _ = _chamber_y(kiln, h.chamber)
        if h.wall in ("left", "right"):
            y = y0 + (across if h.wall == "right" else -across)
            spot = PortSpot(spot.name, spot.title, "spy", h.wall,
                            y if h.wall == "right" else -y, up, w, ht, h.port.round)  # fmt: skip
        hw.ports.append(spot)
        cut += 1
    return cut


def placed_hole_findings(kiln: Kiln, spy: int, stoke: int) -> list[Finding]:
    """What the placed spy and stoke holes are, and what isn't worked out for them."""
    out: list[Finding] = []
    extra = (kiln.spy_holes.holes if kiln.spy_holes else None) or []
    if extra:
        sizes = sorted({_size(h) for h in extra})
        roof = sum(h.wall == "roof" for h in extra)
        out.append(Finding(level="info", reference=SPY_SOURCE, message=(
            f"{spy} of the {len(extra)} spy holes the design places are cut ({', '.join(sizes)})"
            + (f", {roof} up through the roof, straight up from the springline" if roof else "")
            + ". Each is placed as given; none is checked against the setting or the shelf "
            "posts.")))  # fmt: skip
    holes = kiln.stoke_holes or []
    if holes:
        sizes = sorted({_size(h) for h in holes})
        message = (
            f"{stoke} of the {len(holes)} stoke holes into the chambers are cut "
            f"({', '.join(sizes)}). Each is bricked up between stokings, as side-stoked kilns' "
            "are; the plugs aren't counted, and the wood they take isn't worked out."
        )
        out.append(Finding(level="info", reference=STOKE_SOURCE, message=message))
    return out


def _size(h: PlacedHole) -> str:
    w, ht = h.port.size_in()
    return f"{w:g} in round" if h.port.round else f"{w:g} × {ht:g} in"


def floor_burner_xy(
    asked: Burners, w: float, d: float, count: int, inset: float
) -> tuple[list[tuple[float, float]], str] | None:
    """Floor burners laid out by the design's per_side, per_end, centre and corner_offset (in,
    the chamber's centre at 0): each side's and end's burners along their wall in the combustion
    space ``inset`` in from it, set in ``corner_offset`` from the inside corners or each in the
    middle of an even share; the centre ones down the middle of the floor, each in the middle of
    an even share of its depth. None: the hardware's even loop round the edge. With a centre count
    and no per_side, the rest go round the loop."""
    if asked.per_side is None and asked.centre is None:
        return None
    a, b = w - 2 * inset, d - 2 * inset
    centre = asked.centre or 0
    off = si(asked.corner_offset, "in") if asked.corner_offset is not None else None

    def along(length: float, k: int) -> list[float]:
        if k == 0:
            return []
        if off is None:
            run = length - 2 * inset
            return [-run / 2 + (i + 0.5) * run / k for i in range(k)]
        if k == 1:
            return [0.0]
        start, end = -length / 2 + off, length / 2 - off
        return [start + i * (end - start) / (k - 1) for i in range(k)]

    pts: list[tuple[float, float]] = []
    if asked.per_side is not None and asked.per_end is not None:
        for x in (-a / 2, a / 2):
            pts += [(x, y) for y in along(d, asked.per_side)]
        for y in (-b / 2, b / 2):
            pts += [(x, y) for x in along(w, asked.per_end)]
        edge = (f"{asked.per_side} along each side and {asked.per_end} along each end, "
                f"{inset:g} in in from the walls")  # fmt: skip
    else:
        edge = f"{count - centre} round the edge, {inset:g} in in from the walls"
        loop = 2 * (a + b)
        k = count - centre
        for i in range(k):
            s = (i + 0.5) * loop / k
            if s < a:
                pts.append((-a / 2 + s, -b / 2))
            elif s < a + b:
                pts.append((a / 2, -b / 2 + (s - a)))
            elif s < 2 * a + b:
                pts.append((a / 2 - (s - a - b), b / 2))
            else:
                pts.append((-a / 2, b / 2 - (s - 2 * a - b)))
    pts += [(0.0, -b / 2 + (i + 0.5) * b / centre) for i in range(centre)]
    corner = f", the nearest {off:g} in from each corner" if off is not None else ""
    middle = f", and {centre} up through the middle of the floor" if centre else ""
    return pts, f"{edge}{corner}{middle}"


__all__ = ["floor_burner_xy", "place_holes", "placed_hole_findings"]
