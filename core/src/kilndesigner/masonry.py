"""Masonry: how each lining layer is built, brick by brick, and what it takes.

Brick layers use the standard 9 × 4½ × 2½ in straight (electric-and-thermal.md §5, [S54]). A
brick is 2½, 4½ or 9 in through, depending on how it's laid:

- 2½ in: on edge (walls) or flat (floors and roofs);
- 4½ in: as stretchers, 9 in along the wall, 2½ in courses (walls) or on edge (floors and roofs);
- 9 in: as headers, 9 in through the wall, 4½ in along it.

A thicker layer is built of several walls of brick side by side, the fewest that add up to its
thickness: 13½ in is 9 in of headers and 4½ in of stretchers, 7 in is 4½ + 2½. A thickness no
mix of 2½, 4½ and 9 in makes can't be laid from whole bricks, and is reported.

Joints are staggered by starting every other course with a half brick. Pieces that don't fit a
whole brick are cut, and offcuts are reused where they're long enough (first-fit decreasing).
Joints are drawn dry, at the nominal brick size; mortar joints, if used, are not allowed for.

Fibre and board layers are counted by area, castables by volume and weight.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass, field, replace
from typing import Literal

from pydantic import BaseModel, ConfigDict

from kilndesigner.castable import resolve_material
from kilndesigner.geometry import Part, lining_parts
from kilndesigner.library import material
from kilndesigner.materials_checks import whole_bricks
from kilndesigner.model import CatenaryArch, Kiln, SprungArch
from kilndesigner.shape import Arch
from kilndesigner.units import Q_, parse_quantity, si
from kilndesigner.working import Finding, length_text

IN = 25.4  # mm
BRICK = (9 * IN, 4.5 * IN, 2.5 * IN)  # length, width, thickness (mm)
BRICK_SOURCE = "9 × 4½ × 2½ in straight; electric-and-thermal.md §5 [S54]"
KERF = IN / 8  # an assumption: a saw cut takes about ⅛ in
WASTE = 0.10  # an assumption: extra bought for breakage and mistakes, not from a source
TOL = 0.01  # mm
# A layer within 1 mm of a brick size is that size, so a metric design can say 114 mm for 4½ in.
THICKNESS_TOL = 1.0  # mm

type Laying = Literal["stretcher", "on_edge", "header", "flat", "soldier"]
BRICK_KINDS = {"insulating_firebrick", "dense_firebrick", "building_brick"}
SHEET_KINDS = {"fibre_blanket", "fibre_board", "backup_insulation"}
CAST_KINDS = {"insulating_castable", "dense_castable"}
BULK_KINDS = CAST_KINDS | {"stone"}  # counted by weight from their volume


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
    within: tuple[int, int] = (1, 1)  # this wall of brick, of how many side by side in the layer

    @property
    def pieces(self) -> list[Piece]:
        return [p for c in self.courses for p in c.pieces]

    def title(self) -> str:
        """'Left wall, layer 2 from the inside: K-23 …, the inner of 2 walls of brick'."""
        title = f"{layer_name(self.part)}: {material(self.part.material).name}"
        k, n = self.within
        if n > 1:
            title += f", wall of brick {k} of {n} from the inside"
        return title


LAYING_NAMES: dict[Laying, str] = {
    "stretcher": "bricks laid flat along the wall",
    "on_edge": "bricks on edge",
    "header": "bricks laid through the wall",
    "flat": "bricks laid flat",
    "soldier": "bricks standing on end",
}


def layer_name(part: Part) -> str:
    """Where a lining layer is, in words: 'Left wall, layer 2 from the inside'."""
    return part.title


def _layings(horizontal: bool) -> dict[float, tuple[Laying, float, float]]:
    """For each brick size through a layer: (laying, unit along the run, course height)."""
    length, width, thick = BRICK
    if horizontal:
        return {
            thick: ("flat", length, width),
            width: ("on_edge", length, thick),
            length: ("soldier", width, thick),
        }
    return {
        thick: ("on_edge", length, width),
        width: ("stretcher", length, thick),
        length: ("header", width, thick),
    }


def _laying(thickness: float, horizontal: bool) -> tuple[Laying, float, float] | None:
    """How bricks are laid for one wall of brick: (laying, unit along the run, course height)."""
    for size, laying in _layings(horizontal).items():
        if abs(thickness - size) < THICKNESS_TOL:
            return laying
    return None


def brick_sizes(thickness: float) -> list[float] | None:
    """The walls of brick, side by side, that make up a layer's thickness (mm), largest first:
    the fewest that add up. None if no mix of 2½, 4½ and 9 in does."""
    big, mid, small = sorted(BRICK, reverse=True)  # 9, 4½, 2½ in
    mixes = [
        (a, b, c)
        for a in range(int(thickness // big) + 2)
        for b in range(int(thickness // mid) + 2)
        for c in range(int(thickness // small) + 2)
        if a + b + c and abs(a * big + b * mid + c * small - thickness) < THICKNESS_TOL
    ]
    if not mixes:
        return None
    a, b, c = min(mixes, key=lambda n: (sum(n), -n[0], -n[1]))  # fewest, then the biggest bricks
    return [big] * a + [mid] * b + [small] * c


def buildable_near(thickness: float) -> tuple[float | None, float]:
    """The nearest thicknesses (mm) whole bricks can make, below and above ``thickness``."""
    sizes = sorted(BRICK, reverse=True)
    top = thickness + sizes[0]
    sums = {
        a * sizes[0] + b * sizes[1] + c * sizes[2]
        for a in range(int(top // sizes[0]) + 1)
        for b in range(int(top // sizes[1]) + 1)
        for c in range(int(top // sizes[2]) + 1)
    } - {0.0}
    below = [s for s in sums if s < thickness]
    return (max(below) if below else None), min(s for s in sums if s > thickness)


def _split(part: Part, sizes: list[float]) -> list[Part]:
    """The part as walls of brick side by side, from the hot face out, scaled to fill it."""
    axis, hot_at_hi = {
        "floor": (2, True),
        "roof": (2, False),
        "left": (0, True),
        "right": (0, False),
        "back": (1, False),
        "front": (1, True),
    }[part.wall]
    scale = part.thickness / sum(sizes)
    pieces: list[Part] = []
    edge = part.hi[axis] if hot_at_hi else part.lo[axis]
    for size in sizes:
        step = size * scale
        lo, hi = list(part.lo), list(part.hi)
        if hot_at_hi:
            lo[axis], hi[axis] = edge - step, edge
            edge -= step
        else:
            lo[axis], hi[axis] = edge, edge + step
            edge += step
        pieces.append(replace(part, lo=(lo[0], lo[1], lo[2]), hi=(hi[0], hi[1], hi[2])))
    return pieces


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
    """The courses of one wall of brick: a part one brick thick, else None."""
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


def plan_layers(part: Part) -> list[LayerPlan] | None:
    """A brick layer as walls of brick side by side, from the inside out; None if whole bricks
    can't make its thickness."""
    sizes = brick_sizes(part.thickness)
    if sizes is None:
        return None
    plans: list[LayerPlan] = []
    for k, piece in enumerate(_split(part, sizes)):
        plan = plan_layer(piece)
        if plan is None:  # every piece is one brick thick, so this can't happen
            raise AssertionError(f"{part.name}: no laying for {piece.thickness:.1f} mm")
        plan.within = (k + 1, len(sizes))
        plans.append(plan)
    return plans


def _not_buildable(part: Part, us: bool) -> Finding:
    thick = length_text(part.thickness, us)
    below, above = buildable_near(part.thickness)
    choices = " or ".join(length_text(t, us) for t in (below, above) if t is not None)
    name = f"{layer_name(part)}, {material(part.material).name}"
    sheet = whole_bricks(name, part.thickness, below, above, THICKNESS_TOL, us, BRICK_SOURCE)
    nearest = min(abs(t - part.thickness) for t in (below, above) if t is not None)
    sheet.agrees("Δ", Q_(nearest, "mm"))
    return Finding.failed(
        sheet.check(),
        message=(
            f"{layer_name(part)} is {thick} of {material(part.material).name}. Whole "
            "9 × 4½ × 2½ in bricks make layers 2½, 4½ or 9 in thick, or any sum of those (7 in is "
            f"4½ + 2½, 13½ in is 9 + 4½), but not {thick}. So this layer has no course plan, and "
            "its bricks are missing from the brick count, the bill of materials and the price. "
            f"Make it {choices} thick."
        ),
        reference=BRICK_SOURCE,
    )


def _side_by_side(built: list[tuple[Part, list[LayerPlan]]], us: bool) -> Finding:
    layers = [
        f"{layer_name(part)} ({length_text(part.thickness, us)}): "
        + ", then ".join(
            f"{length_text(p.part.thickness, us)} of {LAYING_NAMES[p.laying]}" for p in plans
        )
        for part, plans in built
    ]
    return Finding(
        level="info",
        message=(
            "Layers thicker than one brick are built as walls of brick side by side, from the "
            "inside out. " + "; ".join(layers) + "."
        ),
        reference=BRICK_SOURCE,
    )


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
        rings = f"{self.rings} ring{'' if self.rings == 1 else 's'}"
        straights = self.straights // self.rings
        return (
            f"{rings}, each of {self.shaped // self.rings} {self.shape} bricks and {straights} "
            f"straight{'' if straights == 1 else 's'}"
        )


def arch_ring(part: Part) -> ArchRing | None:
    """The standard arch-brick count: enough tapered bricks to turn the ring's curve.

    Around a ring of radial depth L, the outer arc is longer than the inner by 2θ·L; each tapered
    brick makes up (2½ in − its thin end) of that. Every brick is 2½ in across the outer arc, so
    the ring takes the outer arc ÷ 2½ in bricks, rounded up once: the rest are straights.
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
            per_ring_shaped = math.ceil(n_shaped - 1e-9)
            per_ring = math.ceil((inner_arc + gain) / BRICK[2] - 1e-9)
            per_ring_straight = max(0, per_ring - per_ring_shaped)
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
    side_by_side: list[tuple[Part, list[LayerPlan]]] = []
    under_skewbacks: list[Laying] = []  # how the side walls' brick is laid, under a sprung arch
    for part in lining_parts(kiln):
        m = resolve_material(kiln, part.material)
        if part.profile is not None or part.dome is not None:
            # A skewback and the fill beside a sprung arch; a catenary's ring or an end wall
            # closing it; a dome's layer or a wall's top under it. No standard shapes turn these
            # curves, so brick is counted by volume.
            skewback = part.profile is not None and part.wall in ("left", "right")
            if m.kind in BRICK_KINDS:
                count = math.ceil(part.volume / BRICK_VOLUME)
                whole[m.id] += count
                cut = "the arch's angle" if skewback else "the curve"
                bricks = "brick" if count == 1 else "bricks"
                arch_lines.append(
                    f"{layer_name(part)}: about {count} {bricks} by volume, cut to {cut}"
                )
            elif m.kind in BULK_KINDS:
                cast_volume[m.id] += part.volume
            elif m.kind in SHEET_KINDS:
                sheet_area[m.id] += part.area
                sheet_area_thickness[m.id] += part.volume
                if not part.cap:
                    sheet_thickness.setdefault(m.id, set()).add(round(part.thickness, 2))
            continue
        if m.kind in BRICK_KINDS and part.arch is not None:
            if part.cap:
                count = math.ceil(part.volume / BRICK_VOLUME)
                whole[m.id] += count
                arch_lines.append(
                    f"{layer_name(part)}: about {count} bricks by volume, cut to the arch's curve"
                )
                continue
            ring = arch_ring(part)
            if ring is None:
                count = math.ceil(part.volume / BRICK_VOLUME)
                whole[m.id] += count
                arch_lines.append(f"{layer_name(part)}: about {count} bricks by volume")
            else:
                shapes[(m.id, ring.shape)] += ring.shaped
                whole[m.id] += ring.straights
                arch_lines.append(f"{layer_name(part)}: {ring.describe()}")
            continue
        if m.kind in BRICK_KINDS:
            plans = plan_layers(part)
            if plans is None:
                findings.append(_not_buildable(part, us))
                continue
            if len(plans) > 1:
                side_by_side.append((part, plans))
            if isinstance(kiln.roof, SprungArch) and part.wall in ("left", "right"):
                under_skewbacks.extend(plan.laying for plan in plans)
            layers.extend(plans)
            for piece in (p for plan in plans for p in plan.pieces):
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
        elif m.kind in BULK_KINDS:
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
    if side_by_side:
        findings.append(_side_by_side(side_by_side, us))
    if arch_lines:
        findings.append(
            Finding(
                level="info",
                message="Arch bricks: " + "; ".join(arch_lines) + ".",
                reference=ARCH_SOURCE,
            )
        )
    if isinstance(kiln.roof, SprungArch):
        arch = Arch(si(kiln.chamber.width, "in"), si(kiln.roof.rise, "in"))
        skew = 90 - math.degrees(arch.half_angle)
        findings.append(
            Finding(
                level="info",
                message=(
                    "The skewbacks and the fill beside the arch are drawn along the arch's radius "
                    "at the springline and counted by volume. The skewback's face must match the "
                    f"arch: {skew:.0f}° to the horizontal here, 90° less half the arch's central "
                    "angle (HarbisonWalker's 60° skews suit a 60° arch, its 48° skews one at "
                    "2.302 in/ft). The steel that takes the arch's thrust is in the frame."
                ),
                reference="kiln-hardware.md §5.2 [S20]",
            )
        )
        if "stretcher" in under_skewbacks:
            findings.append(
                Finding(
                    level="info",
                    message=(
                        'HarbisonWalker, for industrial furnaces: "A stretcher course should never '
                        'be used immediately below the skewback." Brick in these side walls is '
                        "laid as stretchers, as in Olsen's insulating-brick kilns, whose "
                        "featheredge skewbacks sit on a stretcher hot face (p.176, p.140). Where "
                        "you can, lay the course under each skewback as headers."
                    ),
                    reference="kiln-hardware.md §4.1 [S20]; Olsen, The Kiln Book, 4th ed., p.176",
                )
            )
    if any(kiln.castable(mid) is None for mid in cast_volume):
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
        if kiln.castable(mid) is not None:
            continue  # your own mix: counted by batches and ingredients (castable.py)
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
                    if m.kind in CAST_KINDS
                    else f"{si(volume, 'ft**3' if us else 'm**3'):.3g} {'ft³' if us else 'm³'} "
                    f"laid, at its density, plus {WASTE:.0%}"
                ),
                priced_amount=si(mass, "lb") * (1 + WASTE),
            )
        )
    if layers:
        corners = (
            ""
            if isinstance(kiln.roof, CatenaryArch)  # it has no side walls
            else " At the corners the side walls run through and the back and door fit between "
            "them, layer by layer."
        )
        findings.append(
            Finding(
                level="info",
                message=(
                    "Brick counts assume dry joints at the nominal 9 × 4½ × 2½ in size, a ⅛ in saw "
                    f"cut, and {WASTE:.0%} extra for breakage.{corners}"
                ),
                reference=BRICK_SOURCE,
            )
        )
    return MasonryPlan(layers, Masonry(quantities=quantities, cut_list=cut_list, findings=findings))
