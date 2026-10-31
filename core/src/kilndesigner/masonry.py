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
from typing import TYPE_CHECKING, Literal

from pydantic import BaseModel, ConfigDict

from kilndesigner import conical
from kilndesigner.allowance import allowance
from kilndesigner.bend import bent, developed
from kilndesigner.bend import note as bend_note
from kilndesigner.castable import resolve_material
from kilndesigner.firebox_parts import firebox_findings
from kilndesigner.geometry import Part, in_a_row, lining_parts
from kilndesigner.library import material
from kilndesigner.materials_checks import whole_bricks
from kilndesigner.model import CatenaryArch, Kiln, SprungArch
from kilndesigner.shape import Arch
from kilndesigner.units import Q_, parse_quantity, si
from kilndesigner.working import Finding, Step, length_text, show

if TYPE_CHECKING:
    from kilndesigner.round_masonry import RingPlan

IN = 25.4  # mm
BRICK = (9 * IN, 4.5 * IN, 2.5 * IN)  # length, width, thickness (mm)
BRICK_SOURCE = "9 × 4½ × 2½ in straight; electric-and-thermal.md §5 [S54]"
KERF = IN / 8  # an assumption: a saw cut takes about ⅛ in
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
    # A round kiln's floor or roof: the circle its rows are cut to, centred on the layer (mm)
    circle: float | None = None

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


def layings(horizontal: bool) -> dict[float, tuple[Laying, float, float]]:
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
    for size, laying in layings(horizontal).items():
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


def run_pieces(
    length: float, unit: float, stagger: bool, height: float, full_h: float
) -> list[Piece]:
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
        pieces = run_pieces(run, unit, stagger=i % 2 == 1, height=height, full_h=course_h)
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
        assert plan is not None, "every piece is one brick thick, so it can always be laid"
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
# Gentlest first. The No. 1-X wedge is A.P. Green's (Firebrick Shapes, p.96), used only with
# lining.shapes 'apg': Olsen's tables turn arches with the simpler No. 1 and No. 2 (p.303–305).
ARCHES = {"No. 1 arch": 2.125, "No. 2 arch": 1.75, "No. 3 arch": 1.0}
WEDGES = {"No. 1 wedge": 1.875, "No. 2 wedge": 1.5}
APG_WEDGES = {"No. 1-X wedge": 2.25, **WEDGES}


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


def arch_ring(part: Part, *, apg: bool = False) -> ArchRing | None:
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
        tapers = APG_WEDGES if apg else WEDGES
        along = BRICK[1]  # bricks 9 in deep, 4½ in along the kiln
    else:
        return None
    gain = 2 * a.half_angle * depth  # outer arc minus inner arc, mm
    inner_arc = 2 * a.half_angle * a.radius
    for shape, thin_in in tapers.items():
        thin = thin_in * IN
        n_shaped = gain / (BRICK[2] - thin)
        n_straight = (inner_arc - n_shaped * thin) / BRICK[2]
        if n_straight >= -0.5:  # the gentlest taper that can turn the curve
            rings = math.ceil(part.length_run / along - TOL / along)
            per_ring_shaped = math.ceil(n_shaped - 1e-9)
            per_ring = math.ceil((inner_arc + gain) / BRICK[2] - 1e-9)
            per_ring_straight = max(0, per_ring - per_ring_shaped)
            return ArchRing(shape, per_ring_shaped * rings, per_ring_straight * rings, rings)
    return None


CONICAL = "conical (tatami) brick"


def conical_layer(part: Part, brick: conical.Brick | None) -> tuple[int, str] | None:
    """A sprung arch's or a dome's layer as deep as the builder's conical brick is long: its
    bricks and how they lie (conical.py). Arches by the ring and the rows along the run; domes by
    the layer's area over each brick's square of it at mid-depth."""
    if brick is None or part.cap or part.is_skewback:
        return None
    if abs(part.thickness - brick.length * IN) >= TOL:
        return None
    if part.arch is not None:
        a = part.arch
        c = conical.course(a.radius / IN, brick)
        per_row = c.bricks(2 * a.half_angle)
        rows = math.ceil(part.length_run / (brick.wide * IN) - 1e-9)
        return per_row * rows, (
            f"{rows} rows of {per_row} conical bricks, wide ends touching, "
            f"{c.inside_joint:.2g} in fireclay between the narrow ends"
        )
    if part.dome is not None:
        c = conical.course(part.dome.radius / IN, brick)
        mid = (part.dome.radius / IN + brick.length / 2) * c.angle
        count = math.ceil(part.area / IN**2 / mid**2 - 1e-9)
        return count, (
            f"about {count} conical bricks in courses, "
            f"{c.inside_joint:.2g} in fireclay between the narrow ends"
        )
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
    working: list[Step] = []


@dataclass
class MasonryPlan:
    layers: list[LayerPlan]
    result: Masonry
    rings: list[RingPlan] = field(default_factory=list["RingPlan"])  # a round wall's rings

    def course_plans(self) -> list[LayerPlan | RingPlan]:
        """Every layer with a course plan, floor first, then the walls, then the roof."""
        if not self.rings:
            return list(self.layers)
        own = [p for p in self.layers if not p.part.name.startswith("firebox-")]
        fireboxes = [p for p in self.layers if p.part.name.startswith("firebox-")]
        floor = [p for p in own if p.part.wall == "floor"]
        rest = [p for p in own if p.part.wall != "floor"]
        return [*floor, *self.rings, *rest, *fireboxes]


def plan_masonry(kiln: Kiln) -> MasonryPlan:
    if kiln.chamber.shape == "round":
        from kilndesigner.round_masonry import plan_round_masonry

        return plan_round_masonry(kiln)
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
    row = in_a_row(kiln)
    along = row and not (isinstance(kiln.roof, SprungArch) and kiln.roof.tube)
    tatami = None if kiln.lining.conical is None else conical.Brick.of(kiln.lining.conical)
    for part in developed(kiln, lining_parts(kiln)):
        m = resolve_material(kiln, part.material)
        laid = conical_layer(part, tatami) if m.kind in BRICK_KINDS else None
        if laid is not None:
            shapes[(m.id, CONICAL)] += laid[0]
            arch_lines.append(f"{layer_name(part)}: {laid[1]}")
            continue
        if part.across and part.arch is not None and m.kind in BRICK_KINDS:
            # An arch along the draft that stops short of its neighbour: in standard shapes
            ring = arch_ring(part, apg=kiln.lining.shapes == "apg")
            if ring is not None:
                shapes[(m.id, ring.shape)] += ring.shaped
                whole[m.id] += ring.straights
                arch_lines.append(f"{layer_name(part)}: {ring.describe()}")
                continue
        if part.profile is not None or part.dome is not None or part.plan is not None:
            # A skewback and the fill beside a sprung arch; a catenary's ring or an end wall
            # closing it; a dome's layer or a wall's top under it; a curved plan's wall, floor or
            # roof. No standard shapes turn these curves, so brick is counted by volume.
            skewback = part.is_skewback
            if m.kind in BRICK_KINDS:
                count = math.ceil(part.volume / BRICK_VOLUME)
                whole[m.id] += count
                cut = "the arch's angle" if skewback else "the curve"
                if part.plan is not None and part.dome is None:
                    cut = "the plan's curve where it needs it"
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
            ring = arch_ring(part, apg=kiln.lining.shapes == "apg")
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
            springs = ("front", "back") if along else ("left", "right")
            if isinstance(kiln.roof, SprungArch) and part.wall in springs:
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

    quantities, cut_list, working = buy_quantities(
        kiln, whole, shapes, cuts, sheet_area, sheet_area_thickness, sheet_thickness, cast_volume
    )
    brick = allowance(kiln, "brick")
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
        span = kiln.chamber.depth if along else kiln.chamber.width
        arch = Arch(si(span, "in"), si(kiln.roof.rise, "in"))
        skew = 90 - math.degrees(arch.half_angle)
        skewback = (
            "The skewbacks and the fill beside the arch are drawn along the arch's radius at the "
            "springline and counted by volume. The skewback's face must match the arch: "
            f"{skew:.0f}° to the horizontal here, 90° less half the arch's central angle "
            "(HarbisonWalker's 60° skews suit a 60° arch, its 48° skews one at 2.302 in/ft). "
            if skew >= 0.5
            else "The arch rises half its span or more: a semicircle or past one, its radius at "
            "each springing level or turned below it, so it springs from the wall's top with no "
            "skewback, and the fill beside its bulge, up to its widest, is counted by volume "
            "(HarbisonWalker's skewbacks are for arches under a semicircle). "
        )
        findings.append(
            Finding(
                level="info",
                message=(
                    skewback
                    + (
                        "The arch's thrust is held by the kiln's masonry, as the design says."
                        if kiln.roof.buttressed
                        else "The end walls take the arches' thrust; no steel for them is sized "
                        "(the frame's findings)."
                        if along
                        else "The steel that takes the arch's thrust is in the frame."
                    )
                ),
                reference="kiln-hardware.md §5.2 [S20]",
            )
        )
        if "stretcher" in under_skewbacks:
            these = "the walls the arches spring from" if along else "these side walls"
            findings.append(
                Finding(
                    level="info",
                    message=(
                        'HarbisonWalker, for industrial furnaces: "A stretcher course should never '
                        f'be used immediately below the skewback." Brick in {these} is '
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
    if layers:
        corners = (
            ""
            if isinstance(kiln.roof, CatenaryArch)  # it has no side walls
            else " The side walls run through, past the end walls and the walls between "
            "chambers, which fit between them."
            if row
            else " At the corners the side walls run through and the back and door fit between "
            "them, layer by layer."
        )
        findings.append(
            Finding(
                level="info",
                message=(
                    "Brick counts assume dry joints at the nominal 9 × 4½ × 2½ in size, a ⅛ in saw "
                    f"cut, and {brick.text} extra for breakage. Each cut piece already takes its "
                    "own brick in the count. The size is sourced; the saw cut is an assumption no "
                    "source gives, so adjust it to your saw. "
                    + (
                        "The allowance is the design's own."
                        if brick.from_design
                        else 'The allowance is the masonry estimators\' "at least 5 percent" '
                        "(BIA): set allowances.brick in the design from your own experience."
                    )
                    + corners
                ),
                reference=f"{BRICK_SOURCE}; kerf assumed; {brick.reference}",
            )
        )
    findings += firebox_findings(kiln) + port_findings(kiln)
    if bent(kiln):
        findings.append(Finding(level="info", message=bend_note(kiln), reference="bend.py"))
    if row:
        findings.append(_row_note(kiln, us))
    elif kiln.chamber.slope is not None and si(kiln.chamber.slope, "degree") > 0:
        slope = si(kiln.chamber.slope, "degree")
        findings.append(
            Finding(
                level="info",
                message=(
                    f"The kiln is laid out along its {slope:.3g}° slope: the floor, walls and "
                    "roof are built square to the sloping floor, every course following it, so "
                    "the course plans are those of a level kiln of the same size. This is how "
                    "the plans draw it; no source here sets how a sloping kiln's courses run, so "
                    "level courses stepped up the slope are as good a choice, with more cutting "
                    "at the top of each wall."
                ),
            )
        )
    return MasonryPlan(
        layers,
        Masonry(quantities=quantities, cut_list=cut_list, findings=findings, working=working),
    )


def port_findings(kiln: Kiln) -> list[Finding]:
    """What the brick count leaves in for the holes the burners and an updraft's flue need: they
    are placed with the burners (hardware.py), after the masonry is counted."""
    gas = kiln.heat.gas
    through: list[str] = []
    if gas is not None and gas.burners.wall == "floor":
        through.append("the burner ports up through the floor")
    burnt = gas is not None or kiln.heat.fire is not None
    if burnt and (kiln.draft is None or kiln.draft.type == "up"):
        through.append("the flue through the roof")
    if not through:
        return []
    return [
        Finding(
            level="info",
            message=(
                " and ".join(through).capitalize()
                + (" are" if len(through) > 1 or "ports" in through[0] else " is")
                + " cut in the 3D model where the burners "
                "and flue are placed; the brick count leaves those bricks in, to be cut on site, "
                "as the side walls' ports are."
            ),
        )
    ]


def _row_note(kiln: Kiln, us: bool) -> Finding:
    """How chambers in a row are laid out (run_parts.py), and what isn't."""
    from kilndesigner.run_parts import run_layout

    run = run_layout(kiln)
    n = run.chambers
    if n == 1:
        return Finding(
            level="info",
            message=(
                "The chamber's arch spans along the draft, over its depth, springing from the "
                "front and back walls, and the side walls are filled up to it, as in Olsen's "
                "Bowen Mountain salt kiln (Fig 4-153): its section across the width rises from "
                "the springline at the end walls to the crown mid-way. The side walls above the "
                "springline are cut to the arch's curve and counted by volume."
            ),
            reference="run_parts.py; Olsen, The Kiln Book, 4th ed., Fig 4-153, p.127",
        )
    text = (
        f"The {n} chambers stand in a row, each wall between them "
        f"{length_text(run.between, us)} thick, as thick as the side walls. "
    )
    reference = "run_parts.py; Olsen, The Kiln Book, 4th ed."
    if run.step > 1e-6:
        slope = si(kiln.chamber.slope, "degree") if kiln.chamber.slope is not None else 0.0
        text += (
            f"Each floor steps {length_text(run.step, us)} above the last: the pitch of a "
            f"chamber and its wall, {length_text(run.pitch, us)}, times tan {slope:.3g}°, as "
            "Olsen's climbing kilns step 12–15 in from chamber to chamber (p.97). Each chamber "
            "is built level, in level courses. "
        )
        reference += ", p.97"
    if isinstance(kiln.roof, SprungArch) and kiln.roof.tube:
        text += (
            "The chambers stand in one tube: its arch spans the width and runs the whole length, "
            "as a tube kiln's, 'an anagama extended' (p.85), its thrust on the side walls; the end "
            "walls and the walls between chambers are filled up to it. "
        )
        reference += ", p.85"
    elif isinstance(kiln.roof, SprungArch):
        text += (
            "Each chamber's arch spans along the draft, over its depth, and throws its thrust "
            "onto the walls before and behind it, as in Olsen's climbing kilns (p.94–95). Where "
            "an arch meets its neighbour over the wall they share, it is cut there and counted by "
            "volume. "
        )
        reference += ", p.94–95; kiln-reference.md, Tube and climbing chamber kilns"
    from kilndesigner.run_parts import FLUE_HEIGHT, flue_rows

    rows = flue_rows(kiln)
    if rows:
        n = rows[0].count
        short = [r.chamber for r in rows if r.top - r.bottom < FLUE_HEIGHT - 1e-6]
        text += (
            f"Each wall between chambers has {n} flue {'hole' if n == 1 else 'holes'} 4½ in "
            "wide and 9 in tall at the higher chamber's floor, 9 in apart: Olsen's standard "
            '4½ × 9 in flues for the Kyoto climbing kilns, "at 9 in" read as a 9 in separator '
            "(p.96, p.45); the book doesn't say which way the 4½ in runs, so it is taken across. "
            "They are cut from the brick count. "
        )
        if short:
            text += (
                "The flues out of chambers " + ", ".join(str(c) for c in short) + " stop at the "
                "lower chamber's springline, under 9 in tall. "
            )
        text += (
            "Lay them on a header course with the header over each one laid so it can be knocked "
            "out if the flue proves too small, and size them against your firing: Olsen errs on "
            "flues too large (p.45)."
        )
    else:
        text += "No flue hole fits under the springlines, so the walls between are counted solid."
    return Finding(level="info", message=text, reference=reference + ", p.45, p.96")


def buy_quantities(
    kiln: Kiln,
    whole: Counter[str],
    shapes: Counter[tuple[str, str]],
    cuts: dict[str, list[Cut]],
    sheet_area: dict[str, float],
    sheet_area_thickness: dict[str, float],
    sheet_thickness: dict[str, set[float]],
    cast_volume: dict[str, float],
    shapes_in: str = "the arch",
) -> tuple[list[Quantity], list[CutLine], list[Step]]:
    """What to buy: whole bricks and cuts, shapes (laid in ``shapes_in``), sheet by area,
    castable by weight."""
    us = kiln.units == "us"
    quantities: list[Quantity] = []
    cut_list: list[CutLine] = []
    working: list[Step] = []
    brick, shaped = allowance(kiln, "brick"), allowance(kiln, "shaped")
    sheet, cast = allowance(kiln, "sheet"), allowance(kiln, "castable")
    if whole or cuts:
        working.append(brick.step())
    if shapes:
        working.append(shaped.step())
    if sheet_area:
        working.append(sheet.step())
    if any(kiln.castable(mid) is None for mid in cast_volume):
        working.append(cast.step())
    for mid in sorted(set(whole) | set(cuts)):
        m = material(mid)
        from_cuts = bricks_for_cuts(cuts.get(mid, []))
        exact = whole[mid] + from_cuts
        buy = brick.buy(exact)
        quantities.append(
            Quantity(
                material=mid,
                name=m.name,
                kind=m.kind,
                amount=buy,
                unit="bricks",
                detail=(
                    f"{whole[mid]} whole, {from_cuts} cut into {len(cuts.get(mid, []))} pieces; "
                    f"{exact} in the kiln plus {brick.text} for breakage"
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
        buy = shaped.buy(count)
        quantities.append(
            Quantity(
                material=mid,
                name=f"{m.name}, {shape}",
                kind=m.kind,
                amount=buy,
                unit="bricks",
                detail=f"{count} in {shapes_in} plus {shaped.text} for breakage",
                priced_amount=buy,
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
                amount=round(si(area, "ft**2" if us else "m**2") * (1 + sheet.share), 1),
                unit="ft²" if us else "m²",
                detail=(
                    f"{thick} thick; area plus {sheet.text} for trimming"
                    if sheet.share
                    else f"{thick} thick; the area, with nothing added for trimming"
                ),
                priced_amount=si(Q_(sheet_area_thickness[mid], "mm**3"), "ft**2*in")
                * (1 + sheet.share),
            )
        )
    for mid, volume_mm3 in sorted(cast_volume.items()):
        if kiln.castable(mid) is not None:
            continue  # your own mix: counted by batches and ingredients (castable.py)
        m = material(mid)
        volume = Q_(volume_mm3, "mm**3")
        # A castable is bought by its maker's "material required" where the sheet gives one
        # (review M8); else at its dried density
        required = m.material_required if m.kind in CAST_KINDS else None
        mass = volume * parse_quantity(required or m.density)
        basis = (
            f"at the maker's {show(parse_quantity(required), 'lb/ft**3' if us else 'kg/m**3')} "
            "required to place it"
            if required
            else "at the dried density"
        )
        quantities.append(
            Quantity(
                material=mid,
                name=m.name,
                kind=m.kind,
                amount=round(si(mass, "lb" if us else "kg") * (1 + cast.share), 0),
                unit="lb" if us else "kg",
                detail=(
                    f"{si(volume, 'ft**3' if us else 'm**3'):.3g} {'ft³' if us else 'm³'} placed, "
                    f"{basis}, plus {cast.text}"
                    if m.kind in CAST_KINDS
                    else f"{si(volume, 'ft**3' if us else 'm**3'):.3g} {'ft³' if us else 'm³'} "
                    f"laid, at its density, plus {cast.text}"
                ),
                priced_amount=si(mass, "lb") * (1 + cast.share),
            )
        )
    return quantities, cut_list, working
