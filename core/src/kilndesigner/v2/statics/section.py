"""A kiln's cross-section as rigid blocks cut from the engine's own solids, and its limit
analysis: what holds the walls, where the resultant falls in each bed joint, and the friction
each bed joint needs (ADR 0017, decision 7).

The section is a slice across the chamber at mid-depth, ``depth`` thick (12 in by default), so
every force is the slice's and is reported per metre run. Its blocks come from the engine's own
part solids (`geometry.lining_parts`, `geometry.part_solid`), cut by build123d
(`scratch/toolsets/whole-kiln/section2d.py`, method B, which agreed with blocks drawn from the
layout's numbers within 0.1 %):

- **the ground**: a fixed block under the walls (the floor and anything under it aren't modelled);
- **each wall**, every layer of it, cut into level courses of 2½ in (Olsen pp.19–20), evened to
  the springline;
- **each skewback**, as the engine lays it out on the wall's top;
- **the arch's ring**, cut into voussoirs by radial planes, one per 2½ in of extrados; the layers
  laid over the ring are its load (the design model's ``acting_ring``);
- **what holds the arch**: a frame (a fixed block against each skewback's back), a buttress (a
  fixed block against the whole outer face of each wall: earth, rock, concrete or more masonry,
  whose demand is computed, not trusted), or nothing.

A kiln on a slope is cut square to its floor: the weights in the section are g·cos(slope); the
share along the slope (g·sin) is carried along the vault and isn't in a cross-section.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import Any, Literal

import build123d as bd
import numpy as np

from kilndesigner.geometry import Part, lining_parts, part_solid
from kilndesigner.model import Kiln, SprungArch
from kilndesigner.units import Q_, si
from kilndesigner.v2.statics import sources
from kilndesigner.v2.statics.arch import sector
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
from kilndesigner.working import Step, show

MM = 1e-3  # the engine's solids are in millimetres
SLICE = si(Q_(12, "inch"), "m")
SUPPORT_THICKNESS = 51.0  # mm: the frame's or buttress's block behind the masonry (any size works)

type Support = Literal["frame", "buttress", "none"]
type State = Literal["cold", "hot"]

GROUND, FRAME, BUTTRESS, VOUSSOIR = "ground", "frame", "buttress", "voussoir"
SUPPORTS = (FRAME, BUTTRESS)

METHOD = (
    "rigid-block limit analysis, the static method: each block in equilibrium, N ≥ 0 and "
    "|T| ≤ μN at every joint (Heyman 1966; Livesley 1978; Ferris & Tin-Loi 2001; "
    "statics-software.md §11), solved by HiGHS"
)


class NotModelledError(Exception):
    """The section can't be built for this kiln yet: the reason says what is missing."""


def not_modelled(kiln: Kiln) -> str | None:
    """Why this kiln's cross-section isn't built, or None."""
    roof, c = kiln.roof, kiln.chamber
    if not isinstance(roof, SprungArch):
        return f"a cross-section across the width takes a sprung arch; this roof is {roof.type}"
    if c.shape != "box" or c.outline is not None:
        return "a sprung arch over a round or curved plan isn't cut into a section here"
    if roof.along or (c.chambers > 1 and not roof.tube):
        return "arches along the draft span the depth: their section runs along the kiln"
    if roof.crossing is not None:
        return "a crossing vault meets the arch in a groin: not a plane section"
    if roof.peak_at is not None:
        return "an offset-peak arch spans along the draft"
    if c.widths is not None:
        return "the chamber's width changes along its depth: one section doesn't stand for it"
    acting = kiln.lining.for_face("roof")[: roof.acting_ring]
    if len({layer.material for layer in acting}) > 1:
        return "a ring of bonded layers of different materials isn't cut into voussoirs yet"
    return None


@dataclass(frozen=True)
class CrossSection:
    """The blocks, the section the LP takes, what holds the arch, and how it was built."""

    blocks: tuple[Block, ...]
    section: Section
    support: Support
    slope: float  # radians
    springline: float  # m
    voussoirs: int
    courses: int
    steps: tuple[Step, ...]
    y_range: tuple[float, float] = (0.0, 0.0)  # m along the run: where the slice was taken


def default_support(kiln: Kiln) -> Support:
    """The design's: a buttressed arch (masonry, earth or a platform holds it in service) gets a
    buttress whose demand is computed; any other a frame."""
    roof = kiln.roof
    return BUTTRESS if isinstance(roof, SprungArch) and roof.buttressed else FRAME


def cross_section(
    kiln: Kiln,
    support: Support | None = None,
    depth: float = SLICE,
    course: float = sources.COURSE.value,
) -> CrossSection:
    """The section across the chamber at mid-depth, ``depth`` m thick; ``course`` m courses."""
    why = not_modelled(kiln)
    if why is not None:
        raise NotModelledError(why)
    roof = kiln.roof
    assert isinstance(roof, SprungArch)
    held: Support = support if support is not None else default_support(kiln)
    parts = [replace(p, tilt=0.0) for p in lining_parts(kiln)]  # cut square to the floor
    springline = si(kiln.chamber.height, "mm")
    y0, y1 = _clear_slice(kiln, parts, depth / MM, springline)
    parts = [p for p in parts if p.lo[1] < y1 and p.hi[1] > y0]
    n_courses = max(1, round(springline / (course / MM))) if springline > 0 else 0
    levels = [springline * k / n_courses for k in range(1, n_courses)]
    blocks: list[Block] = []
    x_out = 0.0
    for p in parts:
        side = p.name.split("/")[0]
        if side not in ("left", "right") or p.profile is not None or p.arch is not None:
            continue
        x_out = max(x_out, abs(p.lo[0]), abs(p.hi[0]))
        layer = p.name.split("/")[1].split("-")[0]
        for k, solid in enumerate(_courses(_sliced(p, y0, y1), levels)):
            blocks.append(_block(f"{side} wall, layer {layer}, piece {k + 1}", solid, p, side))
    skew_top = springline
    for p in parts:
        side = p.name.split("/")[0]
        if side in ("left", "right") and p.is_skewback and _has_area(p):
            for solid in _sliced(p, y0, y1):
                blocks.append(_block(f"{side} skewback", solid, p, side, tag=f"skewback {side}"))
            skew_top = max(skew_top, p.hi[2])
            x_out = max(x_out, abs(p.lo[0]), abs(p.hi[0]))
    rings = sorted(
        (p for p in parts if p.name.startswith("roof/") and p.arch is not None and not p.cap),
        key=lambda p: int(p.name.split("/")[1].split("-")[0]),
    )
    acting, over = rings[: roof.acting_ring], rings[roof.acting_ring :]
    ring_parts = acting
    arch = ring_parts[0].arch
    assert arch is not None
    r_in = arch.radius
    r_out = r_in + sum(p.arch.thickness for p in ring_parts if p.arch is not None)
    n_v = max(2, round(r_out * 2 * arch.half_angle / (course / MM)))
    a0 = math.pi / 2 - arch.half_angle
    theta = [a0 + 2 * arch.half_angle * i / n_v for i in range(n_v + 1)]
    ring = _fused([s for p in ring_parts for s in _sliced(p, y0, y1)])
    rho_ring = sources.density(ring_parts[0].material)
    for i, solid in enumerate(_voussoirs(ring, arch.centre_z, theta)):
        loads = _overburden(over, theta[i], theta[i + 1], depth)
        blocks.append(
            Block(f"voussoir {i + 1}", solid, rho_ring, MM, tag=VOUSSOIR,
                  material=ring_parts[0].material, loads=loads)
        )  # fmt: skip
    pad = 100.0
    x_out = max(x_out, r_out * math.sin(arch.half_angle))
    blocks.append(Block(GROUND, _box((-x_out - pad, y0, -pad), (x_out + pad, y1, 0.0)), 0.0, MM,
                        fixed=True, tag=GROUND))  # fmt: skip
    if skew_top <= 0.0:
        held = "none"  # the arch springs from the ground, which holds its feet by friction
    if held != "none":
        z_lo = springline if held == FRAME else 0.0
        if held == FRAME and skew_top - springline < 1.0:  # a level springing: no skewback
            z_lo = springline - course / MM  # the frame bears on the top course
        for sign in (-1.0, 1.0):
            xs = sorted((sign * x_out, sign * (x_out + SUPPORT_THICKNESS)))
            blocks.append(Block(f"{held} {'left' if sign < 0 else 'right'}",
                                _box((xs[0], y0, z_lo), (xs[1], y1, skew_top)), 0.0, MM,
                                fixed=True, tag=held))  # fmt: skip
    slope = si(kiln.chamber.slope, "radian") if kiln.chamber.slope is not None else 0.0
    sec = section_from_blocks(blocks, contacts_pairwise(blocks), depth)
    if slope:
        c = math.cos(slope)
        sec = Section(
            tuple(
                replace(b, weight=b.weight * c,
                        loads=tuple((x, z, fx * c, fz * c) for x, z, fx, fz in b.loads))
                for b in sec.bodies
            ),
            sec.joints,
            sec.depth,
        )  # fmt: skip
    steps = _built_steps(kiln, held, depth, course, n_courses, n_v, ring_parts, over, slope)
    where = (y0 + y1) / 2 * MM
    steps = (
        steps[0].model_copy(update={"inputs": {
            **steps[0].inputs, "slice's middle from mid-depth": show(Q_(where, "m"), "inch")}}),
        *steps[1:],
    )  # fmt: skip
    return CrossSection(tuple(blocks), sec, held, slope, springline * MM, n_v, n_courses, steps,
                        (y0 * MM, y1 * MM))  # fmt: skip


def _clear_slice(kiln: Kiln, parts: list[Part], d: float, springline: float) -> tuple[float, float]:
    """Where along the run (y, mm) to take a ``d`` mm slice: the one nearest mid-depth through
    which every side-wall layer runs whole from the floor to the springline, and every layer of
    the roof whole, clear of the openings cut in them (a firebox's mouth, a flue)."""
    half = si(kiln.chamber.length, "mm") / 2
    groups: dict[str, list[Part]] = {}
    for p in parts:
        side = p.name.split("/")[0]
        layer = p.name.split("/")[1].split("-")[0]
        if side in ("left", "right") and p.profile is None and p.arch is None:
            groups.setdefault(f"{side} {layer}", []).append(p)
        elif side == "roof" and p.arch is not None and not p.cap:
            groups.setdefault(f"roof {layer}", []).append(p)

    def clear(y0: float, y1: float) -> bool:
        for key, group in groups.items():
            hit = [p for p in group if p.lo[1] < y1 - 1e-6 and p.hi[1] > y0 + 1e-6]
            if len(hit) != 1 or hit[0].lo[1] > y0 + 1e-6 or hit[0].hi[1] < y1 - 1e-6:
                return False
            if key.startswith(("left", "right")) and (
                hit[0].lo[2] > 0.5 or hit[0].hi[2] < springline - 0.5
            ):
                return False
        return True

    step = d / 4
    for k in range(int(half / step) + 1):
        for yc in (k * step, -k * step):
            if abs(yc) + d / 2 <= half + 1e-6 and clear(yc - d / 2, yc + d / 2):
                return yc - d / 2, yc + d / 2
    raise NotModelledError(
        "no slice across the chamber clears the openings in its side walls and roof"
    )


def _has_area(p: Part) -> bool:
    assert p.profile is not None
    pts, nxt = p.profile, p.profile[1:] + p.profile[:1]
    return abs(sum(x0 * z1 - x1 * z0 for (x0, z0), (x1, z1) in zip(pts, nxt, strict=True))) > 1.0


def _sliced(p: Part, y0: float, y1: float) -> list[Any]:
    """The part's solid between y0 and y1 (mm), as solids (none for a wall with no height)."""
    solid = part_solid(p)
    if solid is None:
        return []
    # XZ's normal is −y: BOTTOM keeps y > y0, TOP keeps y < y1
    keep = solid.split(bd.Plane.XZ.offset(-y0), keep=bd.Keep.BOTTOM)
    keep = None if keep is None else keep.split(bd.Plane.XZ.offset(-y1), keep=bd.Keep.TOP)
    return [] if keep is None else list(keep.solids())


def _split(solid: Any, plane: Any) -> list[Any]:
    return [s for piece in solid.split(plane, keep=bd.Keep.BOTH) if piece is not None
            for s in piece.solids()]  # fmt: skip


def _courses(solids: list[Any], levels: list[float]) -> list[Any]:
    """Each solid cut at the level planes, lowest first."""
    out: list[Any] = []
    rest = solids
    for z in levels:
        above: list[Any] = []
        for piece in (x for s in rest for x in _split(s, bd.Plane.XY.offset(z))):
            (out if z > piece.center(bd.CenterOf.MASS).Z else above).append(piece)
        rest = above
    return out + rest


def _fused(solids: list[Any]) -> Any:
    whole = solids[0]
    for s in solids[1:]:
        whole = whole.fuse(s)
    return whole


def _voussoirs(ring: Any, centre_z: float, theta: list[float]) -> list[Any]:
    """The ring cut by radial planes through the arch's axis at each inner angle, from the right
    springing to the left."""
    out: list[Any] = []
    rest = ring
    for a in theta[1:-1]:
        normal = np.array([-math.sin(a), 0.0, math.cos(a)])
        plane = bd.Plane(origin=(0.0, 0.0, centre_z), z_dir=tuple(normal.tolist()))
        before: list[Any] = []
        after: list[Any] = []
        for piece in _split(rest, plane):
            c = piece.center(bd.CenterOf.MASS)
            side = float(normal @ np.array([c.X, 0.0, c.Z - centre_z]))
            (before if side < 0 else after).append(piece)
        out.append(_fused(before))
        rest = _fused(after)
    out.append(rest)
    return out


def _overburden(over: list[Part], t0: float, t1: float, depth: float) -> tuple[Load, ...]:
    """The layers laid over the ring above one voussoir, as loads at their centroids."""
    loads: list[Load] = []
    for p in over:
        a = p.arch
        assert a is not None
        w, x, z = sector(
            a.radius * MM, (a.radius + a.thickness) * MM, t0, t1,
            sources.density(p.material) * G * depth,
        )  # fmt: skip
        loads.append(Load((x, 0.0, a.centre_z * MM + z), (0.0, 0.0, -w)))
    return tuple(loads)


def _block(name: str, solid: Any, p: Part, side: str, tag: str | None = None) -> Block:
    return Block(name, solid, sources.density(p.material), MM, tag=tag or f"wall {side}",
                 material=p.material)  # fmt: skip


def _box(lo: tuple[float, float, float], hi: tuple[float, float, float]) -> Any:
    sx, sy, sz = (b - a for a, b in zip(lo, hi, strict=True))
    cx, cy, cz = ((a + b) / 2 for a, b in zip(lo, hi, strict=True))
    return (bd.Pos(cx, cy, cz) * bd.Box(sx, sy, sz)).solid()


def _built_steps(
    kiln: Kiln,
    held: Support,
    depth: float,
    course: float,
    n_courses: int,
    n_v: int,
    ring: list[Part],
    over: list[Part],
    slope: float,
) -> tuple[Step, ...]:
    materials = sorted({p.material for p in [*ring, *over]} | {
        layer.material for layer in kiln.lining.walls})  # fmt: skip
    steps = [
        Step(
            name="Cross-section through the kiln",
            value=f"{n_courses} courses a wall, {n_v} voussoirs, held by: {held}",
            formula="the engine's part solids cut by build123d: level planes for courses, radial "
            "planes for voussoirs; contacts by the pairwise planar method",
            inputs={
                "slice": show(Q_(depth, "m"), "inch"),
                "course": show(Q_(course, "m"), "inch"),
                "ring": ", ".join(p.material for p in ring),
                "laid over the ring (load)": ", ".join(p.material for p in over) or "none",
            },
            reference=sources.COURSE.reference,
            note=sources.COURSE.note,
        ),
        Step(
            name="Densities",
            value=", ".join(f"{m} {sources.density(m):.0f} kg/m³" for m in materials),
            reference="; ".join(sources.density_reference(m) for m in materials),
        ),
    ]
    if slope:
        steps.append(
            Step(
                name="Slope",
                value=f"weights × cos {math.degrees(slope):.1f}° = {math.cos(slope):.4f}",
                formula="the section is cut square to the floor: g·cos(slope) acts in it",
                note="the share along the slope, g·sin(slope), is carried along the vault and "
                "isn't in this section",
            )
        )
    return tuple(steps)


# --------------------------------------------------------------------------------------------
# the analysis


@dataclass(frozen=True)
class BedJoint:
    """A bed joint of one wall (all its layers together): its height above the floor (m), the
    normal force (N/m), where the resultant falls (from the joint's middle, as a share of its
    width, + outward), and the friction it needs, |T|/N."""

    side: str
    height: float
    n: float
    e: float
    t_over_n: float
    width: float


@dataclass(frozen=True)
class SectionResult:
    """One state of the section: the force on what holds it (per side, N/m: the least, and for a
    hot frame the most), the bed joints at the least-force state, and the working."""

    state: State
    stands: bool
    least: float  # N/m a side: the least the support must give (0 for none)
    most: float  # N/m a side: the most it can be made to take (math.inf if unbounded)
    beds: tuple[BedJoint, ...]
    least_solution: Solution
    steps: tuple[Step, ...]


def conditions(xs: CrossSection, state: State, support_friction: bool = False) -> Problem:
    """The section's problem in a state: μ cold or hot at the masonry's joints; at the support's
    joints 0, or with ``support_friction`` the masonry's own (the band's two ends); hot, the
    crushing stand-in at every joint of a material that has one."""
    sec = xs.section
    mu = sources.MU_COLD.value if state == "cold" else sources.MU_HOT.value
    mus: list[float] = []
    crush: list[float | None] = []
    for j in sec.joints:
        a, b = sec.bodies[j.a], sec.bodies[j.b]
        at_support = a.tag in SUPPORTS or b.tag in SUPPORTS
        mus.append(mu if (not at_support or support_friction) else 0.0)
        stresses = [
            s.value
            for m in (a.material, b.material)
            if m is not None and (s := sources.crushing(m)) is not None
        ]
        crush.append(min(stresses) if state == "hot" and stresses else None)
    return Problem(sec, tuple(mus), tuple(crush) if state == "hot" else ())


def analyse(xs: CrossSection, state: State, support_friction: bool = False) -> SectionResult:
    """The least force the support must give (cold: the frame lets the arch settle to its least
    thrust; a buttress gives no more than it must), and for a frame the most the arch can push
    on it (hot: the cap of the frame's load), with each wall's bed joints at the least."""
    p = conditions(xs, state, support_friction)
    sec, depth = xs.section, xs.section.depth
    if xs.support == "none":
        sol = solve(p)
        least = 0.0 if sol.status is Status.OPTIMAL else math.nan
        most = least
    else:
        cost = force_on(assemble(p), sec, xs.support, 0, outward=True)
        sol = solve(p, cost, 1)
        least = sol.value / 2 / depth if sol.status is Status.OPTIMAL else math.nan
        top = solve(p, cost, -1)
        most = top.value / 2 / depth if top.status is Status.OPTIMAL else top.value
    stands = sol.status is Status.OPTIMAL
    beds = bed_joints(xs, sol) if stands else ()
    steps = _analysis_steps(xs, state, support_friction, stands, least, most, beds)
    return SectionResult(state, stands, least, most, beds, sol, steps)


def bed_joints(xs: CrossSection, sol: Solution) -> tuple[BedJoint, ...]:
    """Each wall's level joints, every layer of the wall together, from the floor up to the
    skewback's bed."""
    sec, x = xs.section, sol.x
    assert x is not None
    groups: dict[tuple[str, float], list[int]] = {}
    for j, jt in enumerate(sec.joints):
        nz = jt.normals[0][1]
        if abs(nz) < 0.99:
            continue
        upper = sec.bodies[jt.b] if nz > 0 else sec.bodies[jt.a]  # the normal points a into b
        if not upper.tag.startswith(("wall ", "skewback ")):
            continue
        side = upper.tag.split()[-1]
        groups.setdefault((side, round(jt.points[0][1], 6)), []).append(j)
    out: list[BedJoint] = []
    asm = sol.assembly
    for (side, z), js in sorted(groups.items()):
        n = t = m = 0.0
        xs_all: list[float] = []
        for j in js:
            k0 = asm.first[j]
            for k in range(k0, k0 + len(sec.joints[j].points)):
                _, px, _, _, _ = asm.points[k]
                n += float(x[2 * k])
                t += float(x[2 * k + 1])
                m += float(x[2 * k]) * px
                xs_all.append(px)
        lo, hi = min(xs_all), max(xs_all)
        width = hi - lo
        e = ((m / n) - (lo + hi) / 2) / width if n > 0 else math.nan
        outward = -1.0 if side == "left" else 1.0
        out.append(BedJoint(side, z, n / sec.depth, e * outward,
                            abs(t) / n if n > 0 else math.nan, width))  # fmt: skip
    return tuple(out)


def _per_metre(v: float) -> str:
    """A force per metre run, with its lbf/ft; 'unbounded', or 'none' when no state exists."""
    fixed = {math.inf: "unbounded"}
    text = "none" if math.isnan(v) else f"{v:.4g} N/m ({si(Q_(v, 'N/m'), 'lbf/ft'):.4g} lbf/ft)"
    return fixed.get(v, text)


def _analysis_steps(
    xs: CrossSection,
    state: State,
    support_friction: bool,
    stands: bool,
    least: float,
    most: float,
    beds: tuple[BedJoint, ...],
) -> tuple[Step, ...]:
    mu = sources.MU_COLD if state == "cold" else sources.MU_HOT
    steps = list(xs.steps)
    steps.append(Step(name=f"Friction at the masonry's joints ({state})", value=f"μ = {mu.value}",
                      reference=mu.reference, note=mu.note))  # fmt: skip
    if xs.support != "none":
        steps.append(Step(
            name=f"Friction at the {xs.support}'s contact",
            value=f"μ = {mu.value if support_friction else 0.0}",
            note=sources.MU_SUPPORT_NOTE,
        ))  # fmt: skip
    if state == "hot":
        stand_ins = sorted(
            {(m, s) for b in xs.section.bodies if b.material is not None
             for m, s in [(b.material, sources.crushing(b.material))] if s is not None},
            key=lambda ms: ms[0],
        )  # fmt: skip
        for m, s in stand_ins:
            steps.append(Step(
                name=f"Hot crushing stand-in, {m}",
                value=show(Q_(s.value, "Pa"), "psi"),
                formula="the resultant leaves room for a uniform stress block at this stress "
                "inside the joint: each end's force ≥ N²/(2σbd), N ≤ σbd (16 inscribed chords)",
                reference=s.reference,
                note=s.note,
            ))  # fmt: skip
    if xs.support == "none":
        steps.append(Step(
            name="An admissible state, the masonry standing on the ground alone",
            value="found" if stands else "none: the section can't stand without support",
            formula=METHOD,
        ))  # fmt: skip
    else:
        steps.append(Step(
            name=f"Least force on the {xs.support}, a side ({state})",
            value=_per_metre(least),
            formula=f"minimise the outward force on the {xs.support} over every admissible state "
            "(Heyman's minimum thrust: supports that give let the arch settle)",
            reference=METHOD,
        ))  # fmt: skip
        steps.append(Step(
            name=f"Most force on the {xs.support}, a side ({state})",
            value=_per_metre(most),
            formula=f"maximise the outward force on the {xs.support}: the most the masonry can "
            "push before a joint slides, crushes or a hinge pattern runs out",
            reference=METHOD,
            note="unbounded: rigid brick that doesn't crush takes any push"
            if math.isinf(most) else None,
        ))  # fmt: skip
    if beds:
        worst = max(beds, key=lambda b: b.e)
        grip = max(beds, key=lambda b: b.t_over_n)
        steps.append(Step(
            name="Bed joints (decision 7), at the least force",
            value=f"resultant farthest out {worst.e:+.3f} of the width ({worst.side} wall, "
            f"{show(Q_(worst.height, 'm'), 'inch')} up); most friction needed T/N "
            f"{grip.t_over_n:.3f} ({grip.side}, {show(Q_(grip.height, 'm'), 'inch')} up)",
            formula="e = (Σ N·x / Σ N − middle) / width, + outward; T/N against μ",
        ))  # fmt: skip
    return tuple(steps)
