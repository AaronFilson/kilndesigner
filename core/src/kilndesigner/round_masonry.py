"""Masonry for a round chamber: its wall as rings of tapered brick, its floor and flat roof as
discs of straights cut to the circle, its dome counted by volume.

- The wall, ring by ring from the inside out (rings.py): a 9 in ring of key bricks laid flat in
  2½ in courses, a 4½ in ring of arch bricks on end in 9 in courses (Olsen, p.45; circle bricks,
  which he prefers for 4½ in, aren't sized in docs/research). Each course is the same ring; the
  top course is ripped to the wall's height. A wall that isn't whole 9 and 4½ in rings is
  reported, as a straight wall that isn't whole bricks is.
- The floor runs under the whole kiln, out to the wall's outside, as the box kiln's does; a flat
  roof sits on the wall. Each is laid in rows of straights, as a box kiln's floor is (masonry.py),
  the rows' ends cut to the circle.
- A dome over a round chamber is a sphere through the springline circle (shape.RoundDome); its
  layers are counted by volume, as the box kiln's dome is: no standard shape turns a dome.

Coordinates in mm; the chamber's axis is z.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict

from kilndesigner.castable import resolve_material
from kilndesigner.library import material
from kilndesigner.masonry import (
    BRICK_KINDS,
    BRICK_SOURCE,
    BRICK_VOLUME,
    BULK_KINDS,
    SHEET_KINDS,
    TOL,
    Cut,
    Masonry,
    MasonryPlan,
    brick_sizes,
    buildable_near,
    buy_quantities,
    layings,
    run_pieces,
)
from kilndesigner.materials_checks import SUMS, whole_bricks
from kilndesigner.model import Dome, FlatRoof, Kiln
from kilndesigner.rings import FAMILIES, IN, SOURCE, RingError, ring, ring_series, wall_rings
from kilndesigner.shape import RoundDome
from kilndesigner.units import si
from kilndesigner.working import Finding, length_text

RINGS = "whole 9 and 4½ in rings: a·9 + b·4½ in (Olsen, The Kiln Book, 4th ed., p.45)"


def _disc_rows(radius: float, thickness: float) -> list[Cut] | None:
    """A disc of brick ``thickness`` thick, laid in rows of straights across it: the pieces that
    aren't whole, and how many are (as Cuts with full size; whole ones have no cut). None if
    whole bricks don't make the thickness."""
    sizes = brick_sizes(thickness)
    if sizes is None:
        return None
    pieces: list[Cut] = []
    for size in sizes:
        laying = next(v for k, v in layings(True).items() if abs(k - size) < 1.0)
        _, unit, width = laying
        rows = math.ceil(2 * radius / width - TOL / width)
        for i in range(rows):
            y0 = -radius + i * width
            y1 = min(y0 + width, radius)
            near = 0.0 if y0 <= 0 <= y1 else min(abs(y0), abs(y1))
            chord = 2 * math.sqrt(max(radius * radius - near * near, 0.0))
            for p in run_pieces(chord, unit, stagger=i % 2 == 1, height=y1 - y0, full_h=width):
                pieces.append(Cut(p.length, p.height, p.full_length, p.full_height))
    return pieces


def _cap_volume(rho: float, below: float) -> float:
    """A sphere of radius rho, its centre ``below`` the springline: its volume above it."""
    h = rho - below
    return math.pi * h * h * (3 * rho - h) / 3 if h > 0 else 0.0


def plan_round_masonry(kiln: Kiln) -> MasonryPlan:
    us = kiln.units == "us"
    c = kiln.chamber
    inside = si(c.width, "mm") / 2
    height = si(c.height, "mm")
    findings: list[Finding] = []
    whole: Counter[str] = Counter()
    shapes: Counter[tuple[str, str]] = Counter()
    cuts: dict[str, list[Cut]] = {}
    sheet_area: defaultdict[str, float] = defaultdict(float)
    sheet_area_thickness: defaultdict[str, float] = defaultdict(float)
    sheet_thickness: dict[str, set[float]] = {}
    cast_volume: defaultdict[str, float] = defaultdict(float)
    lines: list[str] = []

    def sheet(mid: str, area: float, thickness: float) -> None:
        sheet_area[mid] += area
        sheet_area_thickness[mid] += area * thickness
        sheet_thickness.setdefault(mid, set()).add(round(thickness, 2))

    def unbuildable(where: str, mid: str, thickness: float, rings: bool) -> None:
        name = f"{where}, {material(mid).name}"
        step = 4.5 * IN
        below: float | None
        if rings:
            below = math.floor(thickness / step) * step or None
            above = (math.floor(thickness / step) + 1) * step
        else:
            below, above = buildable_near(thickness)
        source, sums = (SOURCE, RINGS) if rings else (BRICK_SOURCE, SUMS)
        sheet_ = whole_bricks(name, thickness, below, above, 1.0, us, source, sums)
        choices = " or ".join(length_text(t, us) for t in (below, above) if t is not None)
        what = (
            "a round wall is laid in rings of 9 in key bricks and 4½ in arch bricks (Olsen, p.45)"
            if rings
            else "whole 9 × 4½ × 2½ in bricks make layers 2½, 4½ or 9 in thick, or sums of those"
        )
        findings.append(
            Finding.failed(
                sheet_.check(),
                message=(
                    f"{where} is {length_text(thickness, us)} of {material(mid).name}, but {what}. "
                    "So its bricks are missing from the brick count, the bill of materials and "
                    f"the price. Make it {choices} thick."
                ),
                reference=source,
            )
        )

    def _wall_ring(mid: str, r: float, depth: float) -> str:
        """Count one ring of the wall, ``r`` its inside radius; say what it is."""
        series = ring_series(depth)
        assert series is not None, "wall_rings gives 9 and 4½ in rings only"
        family = FAMILIES[series]
        course = family.height * IN
        courses = math.ceil(height / course - TOL / course)
        try:
            one = ring(2 * r, series)
        except RingError as e:
            findings.append(Finding(level="warning", message=f"Round wall: {e}.", reference=SOURCE))
            return ""
        top = height - (courses - 1) * course
        ripped = abs(top - course) >= TOL
        for name, n in one.counts:
            if name != family.straight:
                shapes[(mid, name)] += n * courses  # the top course's are cut down from whole
            elif ripped:
                whole[mid] += n * (courses - 1)
                # Keys lie flat and are ripped to the top course; arch bricks stand on end and
                # are cut short
                cut = (
                    Cut(9 * IN, top, 9 * IN, course)
                    if series == "key"
                    else Cut(top, 2.5 * IN, 9 * IN, 2.5 * IN)
                )
                cuts.setdefault(mid, []).extend([cut] * n)
            else:
                whole[mid] += n * courses
        text = f"{length_text(depth, us)} ring of {courses} courses of {one.describe()}"
        if ripped:
            text += f", the top course ripped to {length_text(top, us)}"
        return text

    # The wall, ring by ring
    r = inside
    for i, layer in enumerate(kiln.lining.walls):
        m = resolve_material(kiln, layer.material)
        th = si(layer.thickness, "mm")
        where = f"Round wall, layer {i + 1} from the inside"
        if m.kind in BRICK_KINDS:
            depths = wall_rings(th)
            if depths is None:
                unbuildable(where, m.id, th, rings=True)
            else:
                parts = [_wall_ring(m.id, r + sum(depths[:k]), d) for k, d in enumerate(depths)]
                lines.append(f"{where}: " + "; then ".join(p for p in parts if p))
        elif m.kind in SHEET_KINDS:
            sheet(m.id, 2 * math.pi * (r + th / 2) * height, th)
        elif m.kind in BULK_KINDS:
            cast_volume[m.id] += math.pi * ((r + th) ** 2 - r * r) * height
        r += th
    outside = inside + sum(si(x.thickness, "mm") for x in kiln.lining.walls)

    def disc(face: str, radius: float) -> None:
        for i, layer in enumerate(kiln.lining.for_face(face)):  # type: ignore[arg-type]
            m = resolve_material(kiln, layer.material)
            th = si(layer.thickness, "mm")
            where = f"{face.capitalize()}, layer {i + 1} from the inside"
            area = math.pi * radius * radius
            if m.kind in BRICK_KINDS:
                pieces = _disc_rows(radius, th)
                if pieces is None:
                    unbuildable(where, m.id, th, rings=False)
                    continue
                n_whole = 0
                for p in pieces:
                    if abs(p.length - p.full_length) < TOL and abs(p.height - p.full_height) < TOL:
                        n_whole += 1
                    else:
                        cuts.setdefault(m.id, []).append(p)
                whole[m.id] += n_whole
                lines.append(
                    f"{where}: rows of straights across a {length_text(2 * radius, us)} circle, "
                    f"{n_whole} whole and {len(pieces) - n_whole} cut to the circle"
                )
            elif m.kind in SHEET_KINDS:
                sheet(m.id, area, th)
            elif m.kind in BULK_KINDS:
                cast_volume[m.id] += area * th

    disc("floor", outside)
    roof = kiln.roof
    if isinstance(roof, FlatRoof):
        disc("roof", outside)
    elif isinstance(roof, Dome):
        dome = RoundDome(2 * inside, si(roof.rise, "mm"))
        below = dome.radius - dome.rise  # the sphere's centre under the springline
        rho = dome.radius
        for i, layer in enumerate(kiln.lining.for_face("roof")):
            m = resolve_material(kiln, layer.material)
            th = si(layer.thickness, "mm")
            volume = _cap_volume(rho + th, below) - _cap_volume(rho, below)
            if m.kind in BRICK_KINDS:
                count = math.ceil(volume / BRICK_VOLUME)
                whole[m.id] += count
                lines.append(
                    f"Dome, layer {i + 1} from the inside: about {count} bricks by volume, cut to "
                    "the curve"
                )
            elif m.kind in SHEET_KINDS:
                sheet(m.id, volume / th, th)
            elif m.kind in BULK_KINDS:
                cast_volume[m.id] += volume
            rho += th
    if lines:
        findings.append(
            Finding(
                level="info",
                message=(
                    "Round kiln: " + "; ".join(lines) + ". Rings follow Olsen's circle tables; "
                    "he prefers circle bricks for a 4½ in ring, whose sizes aren't in our "
                    "sources, so arch bricks on end are counted. Stagger the joints course to "
                    "course as in a straight wall (p.45). Brick counts assume dry joints at the "
                    "nominal size; the breakage allowances are those of a box kiln (allowance.py)."
                ),
                reference=f"{SOURCE}; {BRICK_SOURCE}",
            )
        )
    quantities, cut_list, working = buy_quantities(
        kiln, whole, shapes, cuts, sheet_area, sheet_area_thickness, sheet_thickness, cast_volume,
        shapes_in="the round wall",
    )  # fmt: skip
    result = Masonry(quantities=quantities, cut_list=cut_list, findings=findings, working=working)
    return MasonryPlan([], result)
