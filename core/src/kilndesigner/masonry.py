"""Masonry: how each lining layer is built, brick by brick, and what it takes.

Brick layers use the standard 9 × 4½ × 2½ in straight (electric-and-thermal.md §5, [S54]). How a
brick is laid depends on the layer's thickness:

- 2½ in: on edge (walls) or flat (floors and roofs);
- 4½ in: as stretchers, 9 in along the wall, 2½ in courses (walls) or on edge (floors and roofs);
- 9 in: as headers, 9 in through the wall, 4½ in along it.

Joints are staggered by starting every other course with a half brick. Pieces that don't fit a
whole brick are cut, and offcuts are reused where they're long enough (first-fit decreasing).
Joints are drawn dry, at the nominal brick size; mortar joints, if used, are not allowed for.

Fibre and board layers are counted by area, castables by volume and weight.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Literal

from pydantic import BaseModel, ConfigDict

from kilndesigner.geometry import Part, lining_parts
from kilndesigner.library import material
from kilndesigner.model import Kiln
from kilndesigner.units import Q_, parse_quantity, si
from kilndesigner.working import Finding

IN = 25.4  # mm
BRICK = (9 * IN, 4.5 * IN, 2.5 * IN)  # length, width, thickness (mm)
BRICK_SOURCE = "9 × 4½ × 2½ in straight; electric-and-thermal.md §5 [S54]"
KERF = IN / 8  # an assumption: a saw cut takes about ⅛ in
WASTE = 0.10  # an assumption: extra bought for breakage and mistakes, not from a source
TOL = 0.01  # mm

type Laying = Literal["stretcher", "on_edge", "header", "flat", "soldier"]
BRICK_KINDS = {"insulating_firebrick", "dense_firebrick"}
SHEET_KINDS = {"fibre_blanket", "fibre_board", "backup_insulation"}
CAST_KINDS = {"insulating_castable", "dense_castable"}


@dataclass(frozen=True)
class Piece:
    """One brick or cut piece in a course: where it starts along the run, and its size (mm)."""

    start: float
    length: float  # along the run
    height: float  # the course height it fills (less than full when ripped)
    full_length: float  # the brick's dimension along the run
    full_height: float  # the brick's dimension across the course

    @property
    def is_whole(self) -> bool:
        return (
            abs(self.length - self.full_length) < TOL and abs(self.height - self.full_height) < TOL
        )

    @property
    def is_ripped(self) -> bool:
        return abs(self.height - self.full_height) >= TOL


@dataclass(frozen=True)
class Course:
    index: int  # from the bottom (walls) or the front (floors and roofs), from 1
    offset: float  # mm from the start of the layer across courses
    pieces: tuple[Piece, ...]


@dataclass
class LayerPlan:
    part: Part
    laying: Laying
    run_length: float  # mm along each course
    span: float  # mm across all courses (wall height, or floor depth)
    courses: list[Course] = field(default_factory=list[Course])

    @property
    def pieces(self) -> list[Piece]:
        return [p for c in self.courses for p in c.pieces]


def _laying(thickness: float, horizontal: bool) -> tuple[Laying, float, float] | None:
    """How bricks are laid for a layer: (laying, unit along the run, course height)."""
    length, width, thick = BRICK
    if horizontal:
        options: dict[float, tuple[Laying, float, float]] = {
            thick: ("flat", length, width),
            width: ("on_edge", length, thick),
            length: ("soldier", width, thick),
        }
    else:
        options = {
            thick: ("on_edge", length, width),
            width: ("stretcher", length, thick),
            length: ("header", width, thick),
        }
    for size, laying in options.items():
        if abs(thickness - size) < TOL:
            return laying
    return None


def _run(length: float, unit: float, stagger: bool, height: float, full_h: float) -> list[Piece]:
    pieces: list[Piece] = []
    pos = 0.0
    if stagger:
        half = min(unit / 2, length)
        pieces.append(Piece(pos, half, height, unit, full_h))
        pos += half
    while pos + unit <= length + TOL:
        pieces.append(Piece(pos, unit, height, unit, full_h))
        pos += unit
    if length - pos > TOL:
        pieces.append(Piece(pos, length - pos, height, unit, full_h))
    return pieces


def _orient(part: Part) -> tuple[bool, float, float, float]:
    """(horizontal?, run length, span across courses, thickness) for a part's box (mm)."""
    dx, dy, dz = (b - a for a, b in zip(part.lo, part.hi, strict=True))
    face = part.wall
    if face in ("floor", "roof"):
        return True, dx, dy, dz
    if face in ("left", "right"):
        return False, dy, dz, dx
    return False, dx, dz, dy


def plan_layer(part: Part) -> LayerPlan | None:
    horizontal, run, span, thickness = _orient(part)
    laying = _laying(thickness, horizontal)
    if laying is None:
        return None
    kind, unit, course_h = laying
    plan = LayerPlan(part, kind, run, span)
    n = math.ceil(span / course_h - TOL / course_h)
    for i in range(n):
        offset = i * course_h
        height = min(course_h, span - offset)
        pieces = _run(run, unit, stagger=i % 2 == 1, height=height, full_h=course_h)
        plan.courses.append(Course(i + 1, offset, tuple(pieces)))
    return plan


BRICK_VOLUME = BRICK[0] * BRICK[1] * BRICK[2]
ARCH_SOURCE = "Arch and wedge shapes, 9-inch series; electric-and-thermal.md §5 [S54]"
# Arch bricks taper across the 2½ in face along their 4½ in depth (for 4½ in rings); wedges taper
# along their 9 in length (for 9 in rings). Thin end, in inches (electric-and-thermal.md §5).
ARCHES = {"No. 1 arch": 2.125, "No. 2 arch": 1.75, "No. 3 arch": 1.0}
WEDGES = {"No. 1-X wedge": 2.25, "No. 1 wedge": 1.875, "No. 2 wedge": 1.5}


@dataclass(frozen=True)
class ArchRing:
    """One arch layer turned from straights and one tapered shape."""

    shape: str
    shaped: int
    straights: int
    rings: int  # rings along the kiln, one brick deep each

    def describe(self) -> str:
        return (
            f"{self.rings} rings, each of {self.shaped // self.rings} {self.shape} bricks and "
            f"{self.straights // self.rings} straights"
        )


def arch_ring(part: Part) -> ArchRing | None:
    """The standard arch-brick count: enough tapered bricks to turn the ring's curve.

    Around a ring of radial depth L, the outer arc is longer than the inner by 2θ·L; each tapered
    brick makes up (2½ in − its thin end) of that. The rest of the inner arc is straights.
    """
    if part.arch is None:
        return None
    a = part.arch
    depth = a.thickness
    if abs(depth - BRICK[1]) < TOL:
        tapers, along = ARCHES, BRICK[0]  # bricks 4½ in deep, 9 in along the kiln
    elif abs(depth - BRICK[0]) < TOL:
        tapers, along = WEDGES, BRICK[1]  # bricks 9 in deep, 4½ in along the kiln
    else:
        return None
    gain = 2 * a.half_angle * depth  # outer arc minus inner arc, mm
    inner_arc = 2 * a.half_angle * a.radius
    for shape, thin_in in tapers.items():
        thin = thin_in * IN
        n_shaped = gain / (BRICK[2] - thin)
        n_straight = (inner_arc - n_shaped * thin) / BRICK[2]
        if n_straight >= -0.5:  # the gentlest taper that can turn the curve
            rings = math.ceil(part.length_y / along - TOL / along)
            per_ring_shaped = math.ceil(n_shaped)
            per_ring_straight = max(0, math.ceil(n_straight))
            return ArchRing(shape, per_ring_shaped * rings, per_ring_straight * rings, rings)
    return None


@dataclass(frozen=True)
class Cut:
    length: float  # mm
    height: float  # mm across the course; less than the brick's when ripped
    full_length: float
    full_height: float

    def describe(self, us: bool) -> str:
        def size(mm: float) -> str:
            return f"{mm / IN:.3g} in" if us else f"{mm:.0f} mm"

        parts: list[str] = []
        if abs(self.length - self.full_length) >= TOL:
            parts.append(f"cut to {size(self.length)} long")
        if abs(self.height - self.full_height) >= TOL:
            parts.append(f"ripped to {size(self.height)}")
        return ", ".join(parts)


def bricks_for_cuts(cuts: list[Cut]) -> int:
    """Whole bricks needed for the cut pieces, reusing offcuts along the brick's length.

    First-fit decreasing on length, for pieces of the same height; ripped pieces each start a
    brick of their own (their offcut is a sliver along the length).
    """
    bins: dict[tuple[float, float], list[float]] = {}
    count = 0
    for cut in sorted(cuts, key=lambda c: -c.length):
        key = (round(cut.height, 2), round(cut.full_length, 2))
        if cut.height < cut.full_height - TOL:
            count += 1
            continue
        spaces = bins.setdefault(key, [])
        for i, space in enumerate(spaces):
            if space >= cut.length - TOL:
                spaces[i] = space - cut.length - KERF
                break
        else:
            spaces.append(cut.full_length - cut.length - KERF)
            count += 1
    return count


class CutLine(BaseModel):
    model_config = ConfigDict(frozen=True)

    material: str
    cut: str
    count: int


class Quantity(BaseModel):
    model_config = ConfigDict(frozen=True)

    material: str
    name: str
    kind: str
    amount: float
    unit: str
    detail: str
    # For pricing, in US units whatever the display: bricks, ft²·in of sheet, or lb of castable
    priced_amount: float


class Masonry(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    quantities: list[Quantity]
    cut_list: list[CutLine]
    findings: list[Finding]


@dataclass
class MasonryPlan:
    layers: list[LayerPlan]
    result: Masonry


def plan_masonry(kiln: Kiln) -> MasonryPlan:
    us = kiln.units == "us"
    findings: list[Finding] = []
    layers: list[LayerPlan] = []
    whole: Counter[str] = Counter()
    shapes: Counter[tuple[str, str]] = Counter()
    cuts: dict[str, list[Cut]] = {}
    sheet_area: defaultdict[str, float] = defaultdict(float)
    sheet_area_thickness: defaultdict[str, float] = defaultdict(float)
    sheet_thickness: dict[str, set[float]] = {}
    cast_volume: defaultdict[str, float] = defaultdict(float)

    arch_lines: list[str] = []
    for part in lining_parts(kiln):
        m = material(part.material)
        if m.kind in BRICK_KINDS and part.arch is not None:
            if part.cap:
                count = math.ceil(part.volume / BRICK_VOLUME)
                whole[m.id] += count
                arch_lines.append(
                    f"{part.name}: about {count} bricks by volume, cut to the arch's curve"
                )
                continue
            ring = arch_ring(part)
            if ring is None:
                count = math.ceil(part.volume / BRICK_VOLUME)
                whole[m.id] += count
                arch_lines.append(f"{part.name}: about {count} bricks by volume")
            else:
                shapes[(m.id, ring.shape)] += ring.shaped
                whole[m.id] += ring.straights
                arch_lines.append(f"{part.name}: {ring.describe()}")
            continue
        if m.kind in BRICK_KINDS:
            plan = plan_layer(part)
            if plan is None:
                findings.append(
                    Finding(
                        level="warning",
                        message=(
                            f"{part.name}: brick layers must be 2½, 4½ or 9 in thick to be laid "
                            "from standard straights; this layer isn't counted."
                        ),
                        reference=BRICK_SOURCE,
                    )
                )
                continue
            layers.append(plan)
            for piece in plan.pieces:
                if piece.is_whole:
                    whole[m.id] += 1
                else:
                    cuts.setdefault(m.id, []).append(
                        Cut(piece.length, piece.height, piece.full_length, piece.full_height)
                    )
        elif m.kind in SHEET_KINDS:
            sheet_area[m.id] += part.area
            sheet_area_thickness[m.id] += part.volume
            if not part.cap:
                sheet_thickness.setdefault(m.id, set()).add(round(part.thickness, 2))
        elif m.kind in CAST_KINDS:
            cast_volume[m.id] += part.volume

    quantities: list[Quantity] = []
    cut_list: list[CutLine] = []
    for mid in sorted(set(whole) | set(cuts)):
        m = material(mid)
        from_cuts = bricks_for_cuts(cuts.get(mid, []))
        exact = whole[mid] + from_cuts
        buy = math.ceil(exact * (1 + WASTE))
        quantities.append(
            Quantity(
                material=mid,
                name=m.name,
                kind=m.kind,
                amount=buy,
                unit="bricks",
                detail=(
                    f"{whole[mid]} whole, {from_cuts} cut into {len(cuts.get(mid, []))} pieces; "
                    f"{exact} in the kiln plus {WASTE:.0%} for breakage"
                ),
                priced_amount=buy,
            )
        )
        counts = Counter(c.describe(us) for c in cuts.get(mid, []))
        cut_list.extend(
            CutLine(material=mid, cut=desc, count=n) for desc, n in sorted(counts.items())
        )
    for (mid, shape), count in sorted(shapes.items()):
        m = material(mid)
        buy = math.ceil(count * (1 + WASTE))
        quantities.append(
            Quantity(
                material=mid,
                name=f"{m.name}, {shape}",
                kind=m.kind,
                amount=buy,
                unit="bricks",
                detail=f"{count} in the arch plus {WASTE:.0%} for breakage",
                priced_amount=buy,
            )
        )
    if arch_lines:
        findings.append(
            Finding(
                level="info",
                message="Arch bricks: " + "; ".join(arch_lines) + ".",
                reference=ARCH_SOURCE,
            )
        )
    if any(p.arch is not None and not p.cap for p in lining_parts(kiln)):
        findings.append(
            Finding(
                level="warning",
                message=(
                    "The arch's skewbacks, the fill over the wall tops beside the arch, and the "
                    "steel that takes the arch's thrust are not drawn or counted yet. A 60° "
                    "skewback is the usual choice."
                ),
                reference="combustion-and-masonry.md §6.5 [S61, S62]",
            )
        )
    if cast_volume:
        findings.append(
            Finding(
                level="info",
                message=(
                    "Castable: cure 16–24 h above 60 °F kept damp, never let it freeze, and dry it "
                    "out slowly before the first firing (for Mizzou: 75 °F/h with a ½ h hold per "
                    "inch at 250, 500 and 1000 °F). Follow the maker's sheet for your castable."
                ),
                reference="combustion-and-masonry.md §6.2 [S54, S56]",
            )
        )
    for mid, area_mm2 in sorted(sheet_area.items()):
        m = material(mid)
        area = Q_(area_mm2, "mm**2")
        thick = ", ".join(
            f"{t / IN:.3g} in" if us else f"{t:.0f} mm" for t in sorted(sheet_thickness[mid])
        )
        quantities.append(
            Quantity(
                material=mid,
                name=m.name,
                kind=m.kind,
                amount=round(si(area, "ft**2" if us else "m**2") * (1 + WASTE), 1),
                unit="ft²" if us else "m²",
                detail=f"{thick} thick; area plus {WASTE:.0%} for trimming",
                priced_amount=si(Q_(sheet_area_thickness[mid], "mm**3"), "ft**2*in") * (1 + WASTE),
            )
        )
    for mid, volume_mm3 in sorted(cast_volume.items()):
        m = material(mid)
        volume = Q_(volume_mm3, "mm**3")
        mass = volume * parse_quantity(m.density)
        quantities.append(
            Quantity(
                material=mid,
                name=m.name,
                kind=m.kind,
                amount=round(si(mass, "lb" if us else "kg") * (1 + WASTE), 0),
                unit="lb" if us else "kg",
                detail=(
                    f"{si(volume, 'ft**3' if us else 'm**3'):.3g} {'ft³' if us else 'm³'} placed, "
                    f"at the dried density, plus {WASTE:.0%}"
                ),
                priced_amount=si(mass, "lb") * (1 + WASTE),
            )
        )
    if layers:
        findings.append(
            Finding(
                level="info",
                message=(
                    "Brick counts assume dry joints at the nominal 9 × 4½ × 2½ in size, a ⅛ in saw "
                    f"cut, and {WASTE:.0%} extra for breakage. At the corners the side walls run "
                    "through and the back and door fit between them, layer by layer."
                ),
                reference=BRICK_SOURCE,
            )
        )
    if any(p.part.name.startswith("roof/") for p in layers):
        findings.append(
            Finding(
                level="warning",
                message=(
                    "A flat brick roof can't support itself. It needs a support this tool doesn't "
                    "design yet, such as a steel frame with hangers or a sprung arch."
                ),
            )
        )
    return MasonryPlan(layers, Masonry(quantities=quantities, cut_list=cut_list, findings=findings))
