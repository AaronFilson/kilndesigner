"""The section along a row of chambers: each chamber's arch spanning front to back along the
draft, the walls it springs from, and what holds the row's ends, as rigid blocks cut from the
engine's own solids, and their limit analysis (the LP of `rigid.py`).

Climbing, tandem and chamber kilns are laid out by `run_parts.py`: each chamber's arch springs from
the wall in front of it and the wall behind it, so the walls between chambers carry two arches,
which throw their thrust onto the common wall (Olsen, The Kiln Book, 4th ed., p.94–97). On a slope
each chamber's floor steps up, and the wall between two chambers rises from the lower floor to the
higher chamber's springline. One chamber under an arch along its depth (``roof.along``) is a row of
one.

The section is a slice square to x, across the kiln, ``depth`` thick (4 in: it passes between flues
9 in apart, Olsen's standard separator, p.96), taken nearest the middle where every wall it crosses
is whole from its foot to its top: between the flues and clear of the inlets and doors. Its blocks:

- **the floors**: fixed, the ground the walls stand on (on a slope, each chamber's own);
- **the walls across the run** (the end walls and the walls between chambers), each in level courses
  of 2½ in (Olsen pp.19–20), evened between its foot, the springlines it carries and its top;
- **the skewbacks**, as the engine lays them on the walls;
- **each chamber's ring**, cut into voussoirs by planes through its axis, one per 2½ in of
  extrados; the layers laid over the ring are its load (the design model's ``acting_ring``);
- **the ring's foot seated on the wall.** Where a chamber's arch ends against the next, taller
  wall between chambers, the engine's layout trims the ring at the wall's face (for its drawings
  and bill of materials), which leaves the foot against a vertical face with no bed under it. As
  built, the ring sits on the wall: Hotchkiss's arches were each "roped until the arch below was
  finished to buttress it" (p.55–56), the walls carrying them. So here the ring runs whole to its
  springing joint, into the wall up to the wall's top, and the wall's courses are cut round it;
- **what holds the ends**: a frame, a fixed block against each end skewback's back (or the end
  wall's top course where there is no skewback), the two ends tied by its rods to take the same
  force; or a buttress, a fixed block against each end wall's whole outer face: the firebox, the
  earth, the chimney or the bracing in front of and behind the row, whose demand is computed, not
  trusted (ADR 0017, decision 7).

The fireboxes' own walls stand in front of the row on their own floors and aren't cut: the front
end's buttress stands for them.
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import build123d as bd
import numpy as np

from kilndesigner.common_wall import COMMON_WALL_SOURCE
from kilndesigner.geometry import Part, in_a_row, lining_parts, part_solid
from kilndesigner.model import Kiln, SprungArch
from kilndesigner.run_parts import RunLayout, chamber_arch, run_layout
from kilndesigner.units import Q_, si
from kilndesigner.v2.statics import sources
from kilndesigner.v2.statics.blocks import Block, G, Load, contacts_pairwise
from kilndesigner.v2.statics.rigid import (
    Problem,
    Section,
    Solution,
    Status,
    assemble,
    force_on,
    section_from_blocks,
    solve,
)
from kilndesigner.v2.statics.section import (
    BUTTRESS,
    FRAME,
    METHOD,
    NotModelledError,
    State,
    Support,
    default_support,
)
from kilndesigner.v2.statics.solids import above, between, box, courses, fused, voussoirs
from kilndesigner.working import Step, show

MM = 1e-3  # the engine's solids are in millimetres
ROW_SLICE = si(Q_(4, "inch"), "m")
SUPPORT_THICKNESS = 51.0  # mm: the block behind the end masonry (any size works)

EARTH_DEPTH = 100.0  # mm below the lowest floor: how deep the ground under the floors is cut
HEADER_EVERY = 5
"""A wall's layers tied by a header course every fifth course: Olsen draws four stretcher courses
to one header (Fig 2-4, p.42) and counts bricks with "headers every fifth course" (p.295), the
fewest headers of his printed bonds (9 in walls "headers and stretchers alternating", p.41;
English bond, p.42–43); kiln-reference.md, Walls, bonds and openings."""

GROUND, EARTH, WALL, SKEWBACK, VOUSSOIR = "ground", "earth", "wall", "skewback", "voussoir"
ENDS = ("front", "back")


def not_modelled(kiln: Kiln) -> str | None:
    """Why this kiln's section along its row isn't built, or None."""
    roof, c = kiln.roof, kiln.chamber
    if not isinstance(roof, SprungArch):
        return f"the section along a row takes sprung arches; this roof is {roof.type}"
    if not in_a_row(kiln) or roof.tube:
        return "not a row of chambers under arches along the draft"
    if roof.crossing is not None:
        return "a crossing vault meets the arch in a groin: not a plane section"
    if c.shape != "box" or c.outline is not None or (c.bend is not None and si(c.bend, "degree")):
        return "a row of chambers on a straight box plan only"
    if roof.peak_at is not None:
        return "an offset-peak arch along the draft isn't cut into voussoirs yet"
    acting = kiln.lining.for_face("roof")[: roof.acting_ring]
    if len({layer.material for layer in acting}) > 1:
        return "a ring of bonded layers of different materials isn't cut into voussoirs yet"
    run = run_layout(kiln)
    if any(run.springline(i + 1) < run.springline(i) - 1.0 for i in range(run.chambers - 1)):
        return "a chamber springing lower than the one before it isn't laid out on its wall yet"
    return None


@dataclass(frozen=True)
class RowSection:
    """The blocks, the section the LP takes (its horizontal is y along the run, from ``origin``),
    what holds the ends, and how it was built."""

    blocks: tuple[Block, ...]
    section: Section
    support: Support
    x_range: tuple[float, float]  # m: where across the kiln the slice was taken
    origin: float  # m along the run: the section's x = 0
    chambers: int
    voussoirs: tuple[int, ...]  # each chamber's
    seated: tuple[int, ...]  # the chambers (from 1) whose back foot is seated in the wall
    steps: tuple[Step, ...]
    ring_material: str


@dataclass(frozen=True)
class _Ring:
    """One chamber's arch in the y–z plane (mm): its axis, its intrados radius and acting
    thickness, and the angles from the vertical to its front and back springings."""

    chamber: int  # from 0
    centre: tuple[float, float]  # (y, z)
    radius: float
    thickness: float
    front: float
    back: float


def _ring_of(kiln: Kiln, run: RunLayout, i: int, thickness: float) -> _Ring:
    arch = chamber_arch(kiln, run, i)
    if arch.drop:  # one chamber springing unevenly (roof.front_springline)
        centre_z = run.height + arch.rise - arch.radius
        return _Ring(i, (run.centre(0) + arch.offset, centre_z), arch.radius, thickness,
                     arch.front_angle, arch.back_angle)  # fmt: skip
    centre_z = run.springline(i) + arch.rise - arch.radius
    return _Ring(i, (run.centre(i), centre_z), arch.radius, thickness, arch.half_angle,
                 arch.half_angle)  # fmt: skip


def carved_from(name: str) -> str:
    """The part a carved piece was cut from: the engine names each piece of a box cut by holes
    after the box, with one more character ('-a', '-b', … and on past 'z': '-{', '-|', …)."""
    head, _, tail = name.rpartition("-")
    return head if head and len(tail) == 1 and tail >= "a" else name


def _is_wall(p: Part) -> bool:
    """A plain box of a wall across the run: not the floor, a roof or a profile."""
    plain = p.arch is None and p.profile is None and p.dome is None and p.revolve is None
    return plain and p.plan is None and p.groin is None and p.wall not in ("floor", "roof")


def clear_slice(parts: list[Part], d: float, width: float) -> tuple[float, float]:
    """Where across the kiln (x, mm) to take a ``d`` mm slice: the one nearest the middle through
    which every wall across the run is whole, one piece from its foot to its top."""
    groups: dict[str, list[Part]] = {}
    for p in parts:
        if _is_wall(p):
            groups.setdefault(carved_from(p.name), []).append(p)

    def clear(x0: float, x1: float) -> bool:
        for group in groups.values():
            hit = [p for p in group if p.lo[0] < x1 - 1e-6 and p.hi[0] > x0 + 1e-6]
            if not hit:
                continue
            if len(hit) != 1 or hit[0].lo[0] > x0 + 1e-6 or hit[0].hi[0] < x1 - 1e-6:
                return False
            if hit[0].lo[2] > min(q.lo[2] for q in group) + 0.5:
                return False
            if hit[0].hi[2] < max(q.hi[2] for q in group) - 0.5:
                return False
        return True

    half, step = width / 2, d / 4
    for k in range(int(half / step) + 1):
        for xc in (k * step, -k * step):
            if abs(xc) + d / 2 <= half + 1e-6 and clear(xc - d / 2, xc + d / 2):
                return xc - d / 2, xc + d / 2
    raise NotModelledError(
        "no slice along the run clears the openings in the walls across it (the flues, inlets "
        "and doors leave no pier as wide as the slice)"
    )


def _has_area(p: Part) -> bool:
    assert p.profile is not None
    pts, nxt = p.profile, p.profile[1:] + p.profile[:1]
    return abs(sum(y0 * z1 - y1 * z0 for (y0, z0), (y1, z1) in zip(pts, nxt, strict=True))) > 1.0


def _layer(p: Part) -> int:
    return int(p.name.split("/")[1].split("-")[0])


def _chamber(p: Part) -> int:
    """The chamber (from 0) a ring's part belongs to."""
    return int(p.name.rsplit("-chamber-", 1)[1]) - 1


def row_section(
    kiln: Kiln,
    support: Support | None = None,
    depth: float = ROW_SLICE,
    course: float = sources.COURSE.value,
) -> RowSection:
    """The section along the row, ``depth`` m thick, in ``course`` m courses."""
    why = not_modelled(kiln)
    if why is not None:
        raise NotModelledError(why)
    roof = kiln.roof
    assert isinstance(roof, SprungArch)
    held: Support = support if support is not None else default_support(kiln)
    run = run_layout(kiln)
    parts = [p for p in lining_parts(kiln) if not p.name.startswith("firebox-")]
    x0, x1 = clear_slice(parts, depth / MM, run.width)
    parts = [p for p in parts if p.lo[0] < x1 - 1e-6 and p.hi[0] > x0 + 1e-6]
    stepped = run.step > 1e-6 or run.stepped

    def cut(p: Part) -> list[Any]:
        solid = part_solid(p)
        return [] if solid is None else between(solid, 0, x0, x1)

    rings_by: dict[int, list[Part]] = {}
    for p in parts:
        if p.wall == "roof" and p.profile is not None:
            rings_by.setdefault(_chamber(p), []).append(p)
    acting_t = sum(si(x.thickness, "mm") for x in kiln.lining.for_face("roof")[: roof.acting_ring])
    rho_ring = sources.density(kiln.lining.for_face("roof")[0].material)
    ring_mat = kiln.lining.for_face("roof")[0].material

    # Each chamber's ring; where it ends against the taller wall behind it, its foot a springer
    # coursed into that wall
    blocks: list[Block] = []
    seats: dict[int, _Seat] = {}  # by chamber, from 0
    n_vs: list[int] = []
    for i in sorted(rings_by):
        layers = sorted(rings_by[i], key=_layer)
        acting = [p for p in layers if _layer(p) <= roof.acting_ring]
        over = [p for p in layers if _layer(p) > roof.acting_ring]
        ring = _ring_of(kiln, run, i, acting_t)
        whole = fused([s for p in acting for s in cut(p)])
        if max(ring.front, ring.back) > math.pi / 2:  # past a semicircle: its feet laid level
            whole = fused(above(whole, run.springline(i)))
        start = math.pi / 2 - ring.back  # the back springing, as an angle from +y
        top = max(run.springline(i), run.springline(i + 1)) if i + 1 < run.chambers else 0.0
        trimmed = abs(max(p.hi[1] for p in acting) - run.back(i)) < 0.5
        if stepped and i + 1 < run.chambers and top > run.springline(i) + 1.0 and trimmed:
            seat = _springer(ring, whole, run.back(i), top, run.springline(i))
            seats[i] = seat
            whole, start = seat.rest, seat.angle
        hi = math.pi / 2 + ring.front
        r_out = ring.radius + ring.thickness
        n = max(2, round(r_out * (hi - start) / (course / MM)))
        angles = [start + (hi - start) * k / n for k in range(n + 1)]
        pieces = voussoirs(whole, 1, ring.centre, angles)
        loads = _overburden(over, cut, ring, angles)
        pieces.reverse()  # front to back
        n_vs.append(len(pieces))
        for k, solid in enumerate(pieces):
            where = _interval(ring, angles, solid)
            blocks.append(Block(f"chamber {i + 1} voussoir {k + 1}", solid, rho_ring, MM,
                                tag=VOUSSOIR, material=ring_mat,
                                loads=loads.get(where, ())))  # fmt: skip

    # The walls across the run in courses, their layers tied by header courses; a springer's
    # courses bonded into the wall's face
    walls: dict[str, list[Part]] = {}
    for p in parts:
        if _is_wall(p):
            walls.setdefault(_wall_of(p.name), []).append(p)
    for wall, layers in walls.items():
        layers.sort(key=lambda q: q.lo[1])
        lo_z, hi_z = layers[0].lo[2], layers[0].hi[2]
        keys = [s.springline for i, s in seats.items()
                if layers[0].lo[1] > run.back(i) - 1.0
                and layers[-1].hi[1] < run.back(i) + run.between + 1.0
                and lo_z + 1.0 < s.springline < hi_z - 1.0]  # fmt: skip
        levels = _levels(lo_z, hi_z, keys, course / MM)
        pieces = {id(p): courses(cut(p), levels) for p in layers}
        springers = [s.springer for i, s in seats.items()
                     if any(abs(p.lo[1] - run.back(i)) < 1.0 for p in layers)]  # fmt: skip
        spr = courses(springers, levels) if springers else []
        tied = len(layers) > 1 and all(abs(p.lo[2] - lo_z) < 1.0 and abs(p.hi[2] - hi_z) < 1.0
                                       for p in layers)  # fmt: skip
        for k in range(max(len(v) for v in pieces.values())):
            course_k = [(p, pieces[id(p)][k]) for p in layers if k < len(pieces[id(p)])]
            extra = [(s, ring_mat) for s in spr if _same_course(s, course_k[0][1])]
            if tied and k % HEADER_EVERY == HEADER_EVERY - 1:  # a header course
                blocks.append(_bonded(f"{wall} wall, course {k + 1}, headers",
                                      [(s, p.material) for p, s in course_k] + extra))  # fmt: skip
                continue
            for p, solid in course_k:
                mine = extra if p is layers[0] else []
                blocks.append(_bonded(f"{p.name}, course {k + 1}", [(solid, p.material), *mine]))
    for p in parts:
        if p.profile is not None and p.wall != "roof" and p.is_skewback and _has_area(p):
            for solid in cut(p):
                blocks.append(Block(p.name, solid, sources.density(p.material), MM, tag=SKEWBACK,
                                    material=p.material))  # fmt: skip
    floors = [p for p in parts if p.wall == "floor" and _is_floor(p)]
    datum = min(p.lo[2] for p in floors) - EARTH_DEPTH
    for p in floors:
        for solid in cut(p):
            blocks.append(Block(p.name, solid, 0.0, MM, fixed=True, tag=GROUND))
        lowest = not any(q.hi[2] < p.lo[2] + 1.0 and q.lo[1] < p.hi[1] - 1.0
                         and q.hi[1] > p.lo[1] + 1.0 for q in floors if q is not p)  # fmt: skip
        if stepped and lowest:  # the hillside under a chamber's floor
            earth = box((x0, p.lo[1], datum), (x1, p.hi[1], p.lo[2]))
            blocks.append(Block(f"earth under {p.name}", earth, 0.0, MM, fixed=True, tag=EARTH))

    # What holds the ends
    masonry = [b for b in blocks if not b.fixed]
    y_front = min(float(b.lo[1]) for b in masonry)
    y_back = max(float(b.hi[1]) for b in masonry)
    for end, y_face, sign in (("front", y_front, -1.0), ("back", y_back, 1.0)):
        at_end = [b for b in masonry if abs((b.lo[1] if sign < 0 else b.hi[1]) - y_face) < 1.0]
        z_top = max(float(b.hi[2]) for b in at_end)
        if held == BUTTRESS:
            z_lo = min(float(b.lo[2]) for b in at_end)
        else:
            skew = [b for b in at_end if b.tag == SKEWBACK]
            z_lo = (min(float(b.lo[2]) for b in skew) if skew
                    else max(float(b.lo[2]) for b in at_end if b.tag == WALL))  # fmt: skip
        ys = sorted((y_face, y_face + sign * SUPPORT_THICKNESS))
        blocks.append(Block(f"{held} {end}", box((x0, ys[0], z_lo), (x1, ys[1], z_top)), 0.0, MM,
                            fixed=True, tag=f"{held} {end}"))  # fmt: skip

    origin = (y_front + y_back) / 2 * MM
    sec = section_from_blocks(blocks, contacts_pairwise(blocks), (x1 - x0) * MM, axis=1,
                              origin=origin)  # fmt: skip
    seated = tuple(i + 1 for i in sorted(seats))
    steps = _built_steps(kiln, roof.acting_ring, held, (x0 * MM, x1 * MM), course, n_vs,
                         list(seated))  # fmt: skip
    return RowSection(tuple(blocks), sec, held, (x0 * MM, x1 * MM), origin, run.chambers,
                      tuple(n_vs), seated, steps, ring_mat)  # fmt: skip


@dataclass(frozen=True)
class _Seat:
    """A ring's foot coursed into the wall it ends against: the springer, the ring below the
    radial joint that meets the wall's face at the extrados (or at the wall's top, if lower), the
    rest of the ring above that joint, the joint's angle from +y, and the ring's springline."""

    springer: Any
    rest: Any
    angle: float
    springline: float


def _springer(ring: _Ring, whole: Any, face: float, top: float, springline: float) -> _Seat:
    """The tas-de-charge: "the lower courses … laid in horizontal courses and bonded into the
    wall, forming a solid mass" (Encyclopædia Britannica, 11th ed., 1911, vol. 26 p.437, "Tas-de-
    Charge"); "the beds of these courses are not radial as those of the average voussoirs, but
    horizontal" (Fehér 2021, Periodica Polytechnica Architecture 52(1), 21–31)."""
    cy, cz = ring.centre
    u = face - cy
    z_e = cz + math.sqrt(max((ring.radius + ring.thickness) ** 2 - u * u, 0.0))
    angle = math.atan2(min(z_e, top) - cz, u)
    springer, rest = voussoirs(whole, 1, ring.centre, [0.0, angle, math.pi])
    return _Seat(springer, rest, angle, springline)


def _same_course(piece: Any, course_solid: Any) -> bool:
    bb, z = course_solid.bounding_box(), piece.center(bd.CenterOf.MASS).Z
    return bool(bb.min.Z - 1e-6 < z < bb.max.Z + 1e-6)


def _wall_of(name: str) -> str:
    """Which wall across the run a wall part is a layer of: its face, and the chamber whose wall
    it is for a wall between chambers."""
    face = name.split("/", 1)[0]
    if "-chamber-" in name:
        return f"{face} {name.rsplit('-chamber-', 1)[1].split('-')[0]}"
    return face


def _bonded(name: str, pieces: list[tuple[Any, str]]) -> Block:
    """Pieces of masonry bonded into one block (a header course through a wall's layers, a
    springer's course in the wall's face): their weights summed, at their centroid; its crushing
    stand-in the weakest of their materials'."""
    solid, material = pieces[0]
    if len(pieces) == 1:
        return Block(name, solid, sources.density(material), MM, tag=WALL, material=material)
    masses = [sources.density(m) * float(s.volume) for s, m in pieces]
    volume = sum(float(s.volume) for s, _ in pieces)
    crush = {m: c.value if (c := sources.crushing(m)) is not None else math.inf
             for _, m in pieces}  # fmt: skip
    blk = Block(name, fused([s for s, _ in pieces]), sum(masses) / volume, MM, tag=WALL,
                material=min(crush, key=lambda m: crush[m]))  # fmt: skip
    centres = [s.center(bd.CenterOf.MASS) for s, _ in pieces]
    blk.centroid = np.array([sum(m * c.X for m, c in zip(masses, centres, strict=True)),
                             sum(m * c.Y for m, c in zip(masses, centres, strict=True)),
                             sum(m * c.Z for m, c in zip(masses, centres, strict=True))]) / sum(
        masses) * MM  # fmt: skip
    return blk


def _is_floor(p: Part) -> bool:
    return p.arch is None and p.profile is None and p.dome is None


def _levels(bottom: float, top: float, keys: list[float], course: float) -> list[float]:
    """Level joints from a wall's foot to its top, at each key level, the courses evened between."""
    marks = [bottom, *sorted(keys), top]
    out: list[float] = []
    for a, b in itertools.pairwise(marks):
        n = max(1, round((b - a) / course))
        out += [a + (b - a) * k / n for k in range(1, n)]
        if b < top:
            out.append(b)
    return out


def _interval(ring: _Ring, angles: list[float], solid: Any) -> int:
    """Which of the joints' intervals the solid's centroid lies in, about the ring's axis."""
    c = solid.center(bd.CenterOf.MASS)
    a = math.atan2(c.Z - ring.centre[1], c.Y - ring.centre[0])
    return min(range(len(angles) - 1), key=lambda j: abs((angles[j] + angles[j + 1]) / 2 - a))


def _overburden(
    over: list[Part], cut: Callable[[Part], list[Any]], ring: _Ring, angles: list[float]
) -> dict[int, tuple[Load, ...]]:
    """The layers laid over a ring, as loads on its voussoirs, keyed by the joints' interval: each
    layer cut by the same planes, each piece's weight at its centroid on the voussoir under it."""
    out: dict[int, list[Load]] = {}
    for p in over:
        rho = sources.density(p.material)
        for solid in cut(p):
            for piece in voussoirs(solid, 1, ring.centre, angles):
                c = piece.center(bd.CenterOf.MASS)
                w = rho * G * float(piece.volume) * MM**3
                load = Load((c.X * MM, c.Y * MM, c.Z * MM), (0.0, 0.0, -w))
                out.setdefault(_interval(ring, angles, piece), []).append(load)
    return {k: tuple(v) for k, v in out.items()}


def _built_steps(
    kiln: Kiln,
    acting_ring: int,
    held: Support,
    x_range: tuple[float, float],
    course: float,
    n_vs: list[int],
    seated: list[int],
) -> tuple[Step, ...]:
    roof = kiln.lining.for_face("roof")
    materials = sorted({layer.material for layer in [*roof, *kiln.lining.walls]})
    seat_note = (
        f"chambers {', '.join(str(i) for i in seated)}: where each ring ends against the taller "
        "wall behind it (the engine's layout trims it at the wall's face), its foot below the "
        "joint that meets the wall's face is a springer laid in the wall's level courses and "
        "bonded to them (a tas-de-charge, masonry-statics.md M8)"
        if seated
        else "none"
    )
    return (
        Step(
            name="Section along the row",
            value=f"{kiln.chamber.chambers} chamber(s), {', '.join(str(n) for n in n_vs)} "
            f"voussoirs; held at the ends by: {held}",
            formula="the engine's part solids cut by build123d in a slice square to x: level "
            "planes for courses, planes through each arch's axis for voussoirs; contacts by the "
            "pairwise planar method",
            inputs={
                "slice across the kiln": f"{show(Q_(x_range[0], 'm'), 'inch')} to "
                f"{show(Q_(x_range[1], 'm'), 'inch')}",
                "course": show(Q_(course, "m"), "inch"),
                "ring": ", ".join(x.material for x in roof[:acting_ring]),
                "ring feet on a springer": seat_note,
                "a wall's layers": "tied by a header course every fifth course (Olsen p.41–42, "
                "p.295)",
                "the walls between chambers": f"{COMMON_WALL_SOURCE} (common_wall.py), unless the "
                "design gives them (lining.between)",
            },
            reference=sources.COURSE.reference,
            note="the fireboxes' own walls aren't in the section: the front end's support stands "
            "for them; on a slope the ground under each chamber's floor is fixed, as the floors "
            "are",
        ),
        Step(
            name="Densities",
            value=", ".join(f"{m} {sources.density(m):.0f} kg/m³" for m in materials),
            reference="; ".join(sources.density_reference(m) for m in materials),
        ),
    )


# --------------------------------------------------------------------------------------------
# the analysis


def _support(tag: str) -> bool:
    return tag.startswith((FRAME, BUTTRESS, EARTH))


def conditions(
    rs: RowSection, state: State, support_friction: bool = False, analogy: bool = True
) -> Problem:
    """μ cold or hot at the masonry's joints; where masonry meets the ends' supports or the
    earth 0, or with ``support_friction`` the masonry's own (no coefficient is sourced for brick
    on steel or earth); hot, the crushing stand-in at every joint of a material that has one
    (without ``analogy``, only the stand-ins decided, not those carried over by analogy)."""
    sec = rs.section
    mu = sources.MU_COLD.value if state == "cold" else sources.MU_HOT.value
    mus: list[float] = []
    crush: list[float | None] = []
    for j in sec.joints:
        a, b = sec.bodies[j.a], sec.bodies[j.b]
        at_support = _support(a.tag) or _support(b.tag)
        mus.append(mu if (not at_support or support_friction) else 0.0)
        stresses = [
            s.value
            for m in (a.material, b.material)
            if m is not None
            and (s := sources.crushing(m)) is not None
            and (analogy or not sources.by_analogy(m))
        ]
        crush.append(min(stresses) if state == "hot" and stresses else None)
    return Problem(sec, tuple(mus), tuple(crush) if state == "hot" else ())


@dataclass(frozen=True)
class RowResult:
    """One state of the row: whether it stands, the least force each end's support must give
    (N/m run across the kiln) and, hot, the most it can be made to take, with the working."""

    state: State
    stands: bool
    least: dict[str, float]
    most: dict[str, float]
    solution: Solution
    steps: tuple[Step, ...]
    analogy: bool = False
    """Hot, no admissible state with the crushing stand-ins, but one without those carried over by
    analogy: the verdict rests on them alone."""


def analyse(rs: RowSection, state: State, support_friction: bool = False) -> RowResult:
    """The least force the ends' supports must give together, each end's share of it, and hot the
    most the row can push on them, per metre across the kiln."""
    p = conditions(rs, state, support_friction)
    sec, depth = rs.section, rs.section.depth
    asm = assemble(p)
    ends = {end: force_on(asm, sec, f"{rs.support} {end}", 0, outward=True) for end in ENDS}
    cost = ends["front"] + ends["back"]
    sol = solve(p, cost, 1)
    stands = sol.status is Status.OPTIMAL
    analogy = False
    if state == "hot" and not stands:
        decided = conditions(rs, state, support_friction, analogy=False)
        analogy = decided.crush != p.crush and solve(decided).status is Status.OPTIMAL
    least = {end: (float(c @ sol.x) / depth if sol.x is not None else math.nan)
             for end, c in ends.items()}  # fmt: skip
    most: dict[str, float] = {}
    if state == "hot":
        top = solve(p, cost, -1)
        most = {end: (float(c @ top.x) / depth if top.x is not None else top.value)
                for end, c in ends.items()}  # fmt: skip
    steps = _analysis_steps(rs, state, support_friction, stands, least, most, analogy)
    return RowResult(state, stands, least, most, sol, steps, analogy)


def _per_metre(v: float) -> str:
    fixed = {math.inf: "unbounded"}
    text = "none" if math.isnan(v) else f"{v:.4g} N/m ({si(Q_(v, 'N/m'), 'lbf/ft'):.4g} lbf/ft)"
    return fixed.get(v, text)


def _analysis_steps(
    rs: RowSection,
    state: State,
    support_friction: bool,
    stands: bool,
    least: dict[str, float],
    most: dict[str, float],
    analogy: bool,
) -> tuple[Step, ...]:
    mu = sources.MU_COLD if state == "cold" else sources.MU_HOT
    steps = list(rs.steps)
    steps.append(Step(name=f"Friction at the masonry's joints ({state})", value=f"μ = {mu.value}",
                      reference=mu.reference, note=mu.note))  # fmt: skip
    steps.append(Step(name=f"Friction at the {rs.support}'s contact",
                      value=f"μ = {mu.value if support_friction else 0.0}",
                      note=sources.MU_SUPPORT_NOTE))  # fmt: skip
    if state == "hot":
        mats = sorted({b.material for b in rs.section.bodies if b.material is not None})
        for m in mats:
            s = sources.crushing(m)
            if s is not None:
                steps.append(Step(name=f"Hot crushing stand-in, {m}",
                                  value=show(Q_(s.value, "Pa"), "psi"),
                                  reference=s.reference, note=s.note))  # fmt: skip
    steps.append(Step(
        name=f"Least force on the {rs.support} at the ends ({state})",
        value="; ".join(f"{end} {_per_metre(v)}" for end, v in least.items()) if stands
        else "none: no admissible state",
        formula=f"minimise the outward force on the ends' {rs.support}, both ends together, over "
        "every admissible state (Heyman's minimum thrust: supports that give let the arches "
        "settle); each end's share of it",
        reference=METHOD,
    ))  # fmt: skip
    if analogy:
        steps.append(Step(
            name="The hot verdict rests on a stand-in by analogy",
            value="no admissible state with dense firebrick's 25 psi crushing stand-in at every "
            "joint, one without it: not given (ADR 0009)",
            reference=sources.C16_DENSE.reference,
            note="the stand-in is carried over from the user's IFB decision by analogy, a question "
            "for the user; real hot crushing and creep data (refractory-bearing.md gap 11) and the "
            "ring's temperature through its thickness (the heat model) are to decide it",
        ))  # fmt: skip
    if most:
        steps.append(Step(
            name=f"Most force on the {rs.support} at the ends (hot)",
            value="; ".join(f"{end} {_per_metre(v)}" for end, v in most.items()),
            formula="maximise the outward force on the ends: the most the row can push before a "
            "joint slides, crushes or a hinge pattern runs out",
            reference=METHOD,
        ))  # fmt: skip
    return tuple(steps)
