"""Crossing vaults laid out, drawn and checked (roof.crossing; groin.py has the geometry).

The lining: the floor under both tubes and the walls to the springline as boxes, each layer the
union of the two tubes grown less the union grown to the layer before, split into boxes so the
course plans and the fireboxes' holes work as on any box kiln; above the springline, each roof
layer of both vaults as one part, the groin cut out of it, and the end walls' caps closing each
tube's ends up to its arch.

The statics: each vault as the engine checks a sprung arch on its walls (Heyman's thinnest ring,
the hot line of thrust, Olsen's least rise, the thrust the buttress holds). The groin's ribs are
not checked: no source recorded in docs/research gives a groin vault's statics (Heyman's chapter
"The masonry vault", The Stone Skeleton, is not read: blocked-items.md [K19]).
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any, Literal

import numpy as np

from kilndesigner.groin import CrossingShape, GroinLayer, Tube, tubes
from kilndesigner.model import Face, Kiln, SprungArch
from kilndesigner.units import Q_, si
from kilndesigner.working import Finding, Step

if TYPE_CHECKING:
    from kilndesigner.geometry import Part
    from kilndesigner.shape import FaceShape

FIG_7 = (
    "Olsen, The Kiln Book, 4th ed., Ch. 7, p.178–183: Fig 7-1, a groundhog crossing an anagama, "
    "their vaults meeting in a groin (a concept, its sizes the designer's: the user, 2026-10-31); "
    "Fig 7-2, the fire zone where they cross"
)
GROIN_UNCHECKED = (
    "The groin, where the two vaults meet over the fire zone, isn't checked: its ribs gather both "
    "vaults' weight and thrust along the diagonals onto the crossing's four corners (Maia Avelino "
    "et al., SAHC 2020, §4.3: in a 10 × 7.5 m cross vault on its corners the forces accumulate "
    "along the diagonals, the corners' total thrust 67.5–96.7 % of the weight; masonry-statics.md "
    "§M4). That is one worked example, its result depending on the force pattern chosen, not a "
    "rule; Heyman's slicing (webs onto the diagonals, the diagonals as arches to the corners) is "
    "the safe method, read in summary only, so it isn't applied here. Each vault is checked as "
    "an arch on its walls, as a barrel "
    "vault; where the other tube crosses it, its walls are open and the groin carries it, so "
    "buttress the crossing's corners well, as Olsen buttresses these kilns with dirt, rocks and "
    "concrete (Kanayama, p.186). No source sizes that buttress, so it isn't sized here."
)


def crossed(kiln: Kiln) -> bool:
    """Crossing vaults (roof.crossing)."""
    return isinstance(kiln.roof, SprungArch) and kiln.roof.crossing is not None


def crossing_shape(kiln: Kiln) -> CrossingShape:
    """The chamber, in metres, for its volume and heat loss."""
    return CrossingShape(tubes(kiln, "m"))


def crossing_faces(shape: CrossingShape) -> list[FaceShape]:
    """The faces the lining covers: the front and back walls, the chamber's own tube's ends, as a
    box's under an arch (the arch's segment over them); the left and right, every other wall,
    half the plan's perimeter less the ends each, with the crossing tube's end segment; the floor
    under both tubes; and the vaults, less where each lies inside the other."""
    from kilndesigner.shape import FaceShape

    chamber, crossing = shape.tubes
    h, w = chamber.springline, chamber.span

    def sides(t: float) -> float:
        return (shape.perimeter(t) - 2 * (w + 2 * t)) / 2 * (h + 2 * t) + crossing.segment_area

    def ends(t: float) -> float:
        return (w + 2 * t) * (h + 2 * t) + chamber.segment_area

    length = chamber.run[1] - chamber.run[0]
    side = (shape.perimeter() - 2 * w) / 2
    out = [FaceShape(f, "vertical", sides(0.0), side, h, grows=sides) for f in ("left", "right")]
    out += [FaceShape(f, "vertical", ends(0.0), w, h, grows=ends) for f in ("back", "front")]
    out.append(FaceShape("floor", "facing_down", shape.floor(), w, length, grows=shape.floor))
    out.append(FaceShape("roof", "facing_up", shape.vaults(), w, length, grows=shape.vaults))
    return out


# --- The lining's parts -------------------------------------------------------------------------

type Box = tuple[tuple[float, float, float], tuple[float, float, float]]


def _minus(box: Box, cut: Box) -> list[Box]:
    """The box less ``cut``: the slabs either side of it, axis by axis (x first, so the side
    walls run through and the ends fit between them, as on a box kiln)."""
    (a, b), (lo, hi) = box, cut
    if any(hi[i] <= a[i] + 1e-6 or lo[i] >= b[i] - 1e-6 for i in range(3)):
        return [box]
    pieces: list[Box] = []
    cur_lo, cur_hi = list(a), list(b)
    for i in range(3):
        if lo[i] > cur_lo[i] + 1e-6:
            q_hi = list(cur_hi)
            q_hi[i] = lo[i]
            pieces.append(((cur_lo[0], cur_lo[1], cur_lo[2]), (q_hi[0], q_hi[1], q_hi[2])))
            cur_lo[i] = lo[i]
        if hi[i] < cur_hi[i] - 1e-6:
            q_lo = list(cur_lo)
            q_lo[i] = hi[i]
            pieces.append(((q_lo[0], q_lo[1], q_lo[2]), (cur_hi[0], cur_hi[1], cur_hi[2])))
            cur_hi[i] = hi[i]
    return pieces


def _minus_all(boxes: list[Box], cuts: list[Box]) -> list[Box]:
    for cut in cuts:
        boxes = [q for b in boxes for q in _minus(b, cut)]
    return boxes


def _plan(tube: Tube, t: float, z: tuple[float, float]) -> Box:
    """The tube's plan grown by t each way, from z[0] to z[1]."""
    c0, c1 = tube.centre - tube.span / 2 - t, tube.centre + tube.span / 2 + t
    a, b = tube.run[0] - t, tube.run[1] + t
    if tube.axis == 1:
        return (c0, a, z[0]), (c1, b, z[1])
    return (a, c0, z[0]), (b, c1, z[1])


def _face(box: Box, chamber: Tube) -> Face:
    """Which wall a box of wall is part of: the chamber's ends are the front and back walls;
    every other wall is the left or right, by its side of the middle."""
    (x0, y0, _), (x1, y1, _) = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    if abs(cx) <= chamber.span / 2 and cy < chamber.run[0]:
        return "front"
    if abs(cx) <= chamber.span / 2 and cy > chamber.run[1]:
        return "back"
    return "left" if cx < 0 else "right"


def crossing_parts(kiln: Kiln) -> list[Part]:
    """The lining of crossing vaults, in mm (geometry.Part)."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.geometry import Part

    chamber, crossing = tubes(kiln, "mm")
    h = chamber.springline
    parts: list[Part] = []

    def kind(mat: str) -> str:
        return resolve_material(kiln, mat).kind

    def named(face: Face) -> str:
        return "door" if face == kiln.door_wall else face

    walls = [(x.material, si(x.thickness, "mm")) for x in kiln.lining.walls]
    out = sum(t for _, t in walls)
    cum = 0.0
    for i, (mat, th) in enumerate((x.material, si(x.thickness, "mm"))
                                  for x in kiln.lining.for_face("floor")):  # fmt: skip
        z = (-cum - th, -cum)
        own = _plan(chamber, out, z)
        boxes = [own, *_minus(_plan(crossing, out, z), own)]
        for k, (lo, hi) in enumerate(boxes):
            parts.append(Part(f"floor/{i + 1}-{mat}" + (f"-p{k}" if k else ""), mat, kind(mat),
                              lo, hi, face="floor"))  # fmt: skip
        cum += th
    reached = 0.0
    for i, (mat, th) in enumerate(walls):
        z = (0.0, h)
        inner = [_plan(t, reached, z) for t in (chamber, crossing)]
        own = _plan(chamber, reached + th, z)
        a = _minus_all([own], inner)
        b = _minus_all([_plan(crossing, reached + th, z)], [*inner, own])
        seen: dict[str, int] = {}
        for lo, hi in a + b:
            face = _face((lo, hi), chamber)
            name = f"{named(face)}/{i + 1}-{mat}"
            k = seen[name] = seen.get(name, 0) + 1
            parts.append(Part(name + (f"-p{k - 1}" if k > 1 else ""), mat, kind(mat), lo, hi,
                              face=face))  # fmt: skip
        reached += th
    roof = [(x.material, si(x.thickness, "mm")) for x in kiln.lining.for_face("roof")]
    shell = sum(t for _, t in roof)
    both = (chamber, crossing)
    # The end walls' caps, closing each tube's ends above the springline up to its arch
    ends: list[tuple[int, Face, int]] = [(0, "front", -1), (0, "back", 1), (1, "left", -1),
                                          (1, "right", 1)]  # fmt: skip
    for which, face, sign in ends:
        tube = both[which]
        reached = 0.0
        for i, (mat, th) in enumerate(_layers(kiln, face)):
            edge = tube.run[1] if sign > 0 else tube.run[0]
            along = sorted((edge + sign * reached, edge + sign * (reached + th)))
            c0, c1 = tube.centre - tube.span / 2, tube.centre + tube.span / 2
            top = h + tube.rise
            lo, hi = ((c0, along[0], h), (c1, along[1], top)) if tube.axis == 1 else (
                (along[0], c0, h), (along[1], c1, top))  # fmt: skip
            layer = GroinLayer(both, 0.0, 0.0, cap=which, shell=shell)
            parts.append(Part(f"{named(face)}/{i + 1}-{mat}-arch", mat, kind(mat), lo, hi,
                              cap=True, face=face, ring=th, groin=layer))  # fmt: skip
            reached += th
    cum = 0.0
    for i, (mat, th) in enumerate(roof):
        layer = GroinLayer(both, cum, cum + th)
        lo, hi = _roof_box(both, cum + th)
        parts.append(Part(f"roof/{i + 1}-{mat}", mat, kind(mat), lo, hi, face="roof", ring=th,
                          groin=layer))  # fmt: skip
        cum += th
    return parts


def _layers(kiln: Kiln, face: Face) -> list[tuple[str, float]]:
    return [(x.material, si(x.thickness, "mm")) for x in kiln.lining.for_face(face)]


def _roof_box(both: tuple[Tube, Tube], out: float) -> Box:
    """The plan and height a roof layer reaching ``out`` from the inside can fill."""
    xs: list[float] = []
    ys: list[float] = []
    for t in both:
        reach = t.foot(out)
        across = (t.centre - reach, t.centre + reach)
        along = (t.run[0] - t.ends, t.run[1] + t.ends)
        xs += across if t.axis == 1 else along
        ys += along if t.axis == 1 else across
    top = max(t.centre_z + t.radius + out for t in both)
    return (min(xs), min(ys), both[0].springline), (max(xs), max(ys), top)


def groin_cut(part: Part, axis: Literal[0, 1], at: float) -> list[tuple[tuple[float, float], ...]]:
    """The part cut through x = at (axis 0) or y = at (axis 1), as outlines; none if the plane
    misses it."""
    assert part.groin is not None
    if not part.lo[axis] - 1e-6 <= at <= part.hi[axis] + 1e-6:
        return []
    other = 1 - axis
    return part.groin.cut(axis, at, part.lo[other], part.hi[other])


def groin_solid(part: Part) -> Any:
    """The part's solid, by the same subtraction its volume sums: a ring layer, both tubes'
    rings less the union grown to the layer inside; a cap, its band up to its tube's arch less
    the other tube's vault and all inside it."""
    from build123d import Box as Block
    from build123d import Pos

    layer = part.groin
    assert layer is not None
    lo, hi = part.lo, part.hi
    big = 1e5

    def above(t: Tube) -> Any:
        return Pos(0, 0, t.springline + big / 2) * Block(big, big, big)

    def vault(t: Tube, depth: float, *, over_ends: bool) -> Any:
        from kilndesigner.geometry import _cylinder  # pyright: ignore[reportPrivateUsage]

        grow = t.ends if over_ends else 0.0
        a, b = t.run[0] - grow, t.run[1] + grow
        mid = (a + b) / 2
        centre = (t.centre, mid, t.centre_z) if t.axis == 1 else (mid, t.centre, t.centre_z)
        return _cylinder(t.axis, centre, t.radius + depth, b - a) & above(t)

    if layer.cap is not None:
        own, other = layer.tubes[layer.cap], layer.tubes[1 - layer.cap]
        from kilndesigner.geometry import _box  # pyright: ignore[reportPrivateUsage]

        band = _box(lo, hi)
        return (band & vault(own, 0.0, over_ends=True)) - vault(other, layer.shell, over_ends=True)
    rings = [
        vault(t, layer.outer, over_ends=True) - vault(t, layer.inner, over_ends=True)
        for t in layer.tubes
    ]
    solid = rings[0] + rings[1]
    for t in layer.tubes:
        solid = solid - vault(t, layer.inner, over_ends=False)
    return solid


# --- The statics --------------------------------------------------------------------------------


def crossing_statics(kiln: Kiln) -> tuple[list[Step], list[Finding]]:
    """Each vault checked as the engine checks a sprung arch on its walls, and the groin said not
    to be checked, with the reason: the working and the findings."""
    from kilndesigner.frame import (
        ARCH_THEORY_SOURCE,
        MAX_PRINTED_HEATED,
        OLSEN_LEAST_RISE,
        OLSEN_RISE,
        _arch_load,  # pyright: ignore[reportPrivateUsage]
        _roof_layers,  # pyright: ignore[reportPrivateUsage]
        cold_thrust_factor,
        heated_thrust_factor,
        steel_data,
    )
    from kilndesigner.frame_checks import (
        CAPPED,
        ArchInputs,
        hot_thrust_line,
        rise_rule,
        vault_ring,
    )
    from kilndesigner.shape import Arch

    roof = kiln.roof
    assert isinstance(roof, SprungArch)
    assert roof.crossing is not None
    minimum = steel_data()["arch_minimum_thickness"]
    layers = _roof_layers(kiln)
    working: list[Step] = []
    findings: list[Finding] = []
    vaults = (
        ("the chamber's vault (the anagama's, front to back)", kiln.chamber.width, roof.rise),
        ("the crossing vault (the groundhog's, side to side)", roof.crossing.span,
         roof.crossing.rise),
    )  # fmt: skip
    for name, span_q, rise_q in vaults:
        span, rise = si(span_q, "in"), si(rise_q, "in")
        arch = Arch(span, rise)
        load = _arch_load(kiln, arch)
        cold = cold_thrust_factor(span, rise) * load.weight
        heated = heated_thrust_factor(span, rise, load.ring)
        hot = min((heated if heated is not None else MAX_PRINTED_HEATED) * cold,
                  MAX_PRINTED_HEATED * cold)  # fmt: skip
        a = ArchInputs(span, rise, layers, roof.ring)
        phi = math.degrees(arch.half_angle)
        eta = float(np.interp(phi, minimum["half_angle_deg"], minimum["eta"]))
        ring = vault_ring(a, eta, minimum["safety"], minimum["source"])
        t = load.ring
        k = t / (arch.radius + t / 2) / eta
        ring.agrees("k", k)
        line = hot_thrust_line(a)
        rising = rise_rule(a, OLSEN_LEAST_RISE, OLSEN_RISE)
        rising.agrees("d", rise / span)
        working.append(
            Step(
                name=f"{name[0].upper()}{name[1:]}: Heyman's statics and its thrust",
                value=(
                    f"a {t:g} in ring over {span:g} in, rising {rise:g} in "
                    f"({12 * rise / span:.2f} in/ft): {k:.1f} times the thinnest that stands "
                    f"(half-angle {phi:.1f}°); {load.weight:.0f} lb per foot of vault, thrust "
                    f"{hot:.0f} lb/ft hot ({cold:.0f} cold), held by the buttress"
                ),
                formula=(
                    "k = T/(r + T/2) ÷ η(φ) ≥ 2; H = W·(sin θ − (1 − cos θ)/θ) / (2(1 − cos θ)); "
                    "hot, × the heated factor"
                ),
                inputs={"span": f"{span:g} in", "rise": f"{rise:g} in", "ring": f"{t:g} in"},
                reference=f"{ring.reference}; {ARCH_THEORY_SOURCE}; {CAPPED}; {FIG_7}",
                note=(
                    "Checked as a barrel vault on its walls, as the engine checks any sprung arch. "
                    "Within the crossing the other vault cuts it; the groin isn't checked."
                ),
            )
        )
        for sheet, message in (
            (ring, f"In {name}, the {t:g} in ring is {k:.1f} times the thinnest that holds a line "
             f"of thrust at its half-angle, less than Heyman's {minimum['safety']}: thicken the "
             "ring or raise the vault."),
            (line, f"In {name}, the hot line of thrust leaves the ring at the skewback: the ring "
             "is too thick for its rise; raise the vault or thin the ring."),
            (rising, f"{name[0].upper()}{name[1:]} rises {12 * rise / span:.2f} in per foot of "
             "span, less than Olsen's 1½ in/ft: less 'can result in structural difficulty'."),
        ):  # fmt: skip
            if (check := sheet.check()).status != "pass":
                findings.append(Finding.failed(check, message=message))
    findings.append(Finding(level="info", message=GROIN_UNCHECKED, reference=FIG_7))
    return working, findings


def crossing_note(kiln: Kiln) -> Finding:
    """What the plans and the bill take as the crossing's layout."""
    chamber, crossing = tubes(kiln, "in")
    arms = (crossing.run[1] - crossing.run[0] - chamber.span) / 2
    shape = crossing_shape(kiln)
    ft3 = shape.volume() / si(Q_(1, "ft**3"), "m**3")
    return Finding(
        level="info",
        message=(
            f"Two vaults cross over the fire zone: the chamber's, {chamber.span:g} in wide, "
            f"rising {chamber.rise:g} in to {chamber.springline + chamber.rise:g} in, front to "
            f"back; the crossing's, {crossing.span:g} in wide, rising {crossing.rise:g} in to "
            f"{crossing.springline + crossing.rise:g} in, side to side"
            + (f", its arms {arms:g} in out past the side walls" if arms > 1e-6 else "")
            + f". Both spring from the walls' tops, {chamber.springline:g} in up. Inside, "
            f"{ft3:.1f} ft³. Each layer of the vaults is laid out as both tubes' rings less "
            "everything inside the layer before, so the groin, where they meet, is cut on site "
            "to the other vault's curve: no standard shape turns it, and its brick is counted by "
            "volume."
        ),
        reference=FIG_7,
    )


__all__ = [
    "crossed",
    "crossing_faces",
    "crossing_note",
    "crossing_parts",
    "crossing_shape",
    "crossing_statics",
    "groin_cut",
    "groin_solid",
]
