"""Brick courses round a curved plan (chamber.outline): each wall layer as rings of straights
laid flat as stretchers, 9 in along the wall, 4½ in through, 2½ in courses, as Calimpong's walls
are (Olsen, The Kiln Book, 4th ed., Figs 4-143, 4-144: IFB walls in stretcher courses, the side
walls double).

Each ring follows the plan moved out to its inside face (outline.offset), piece by piece:

- a straight wall: whole straights, and a closer cut to what is left;
- a convex arc (the round end, the bulging sides): straights with their inside faces on the
  curve and wedge-shaped joints behind filled with mortar, as Olsen draws a curved wall (p.45,
  Fig. 2-13; rings.py, "mortar"). Each brick's inside face is a 9 in chord of the arc, turning
  θ = 2·asin(4½/R); n = ⌊sweep/θ⌋ whole bricks and a closer to the chord left; the widest
  joint, at the outside, is 2·d·sin(θ/2);
- a concave arc (the reverse curve into a neck): laid that way the joints would open on the hot
  face, so the straights are cut to the angle, each end θ/2 off square, θ the angle a 9 in chord
  of the inside face turns (rings.py, "cut": straights cut to the angle, the norm in electric
  kilns, the user, 2026-10-30). Applying the cut method to a concave curve is the engine's own
  reading: no source lays a concave wall;
- a corner of the plan moved out (outline.offset rounds it): bricks lapped at the corner and cut
  to fit, counted as its length in straights, rounded up.

A layer that isn't a whole number of 4½ in rings is left counted by volume, as before.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from kilndesigner.model import Kiln
from kilndesigner.outline import Arc, Line, Outline, offset
from kilndesigner.rings import MORTAR_SOURCE

IN = 25.4  # mm
STRAIGHT = 9.0  # in, along the wall
THROUGH = 4.5  # in, through the wall
COURSE = 2.5  # in, a course's height
CUT_SOURCE = (
    "straights cut to the angle (the user, a kiln builder, 2026-10-30; rings.py), applied to a "
    "concave curve by the engine"
)
SOURCE = (
    f"{MORTAR_SOURCE}; {CUT_SOURCE}; Olsen Figs 4-143, 4-144 (Calimpong's IFB walls in "
    "stretcher courses, the side walls double)"
)


@dataclass(frozen=True)
class Run:
    """One piece of a ring round the plan, per course."""

    kind: str  # "straight", "convex", "concave", "corner"
    length: float  # in, along the ring's inside face
    whole: int
    closer: float  # in, the closer's inside face (0 for none)
    joint: float = 0.0  # in, the widest mortar joint at the outside (convex)
    cut: float = 0.0  # degrees off square at each end (concave)

    @property
    def bricks(self) -> int:
        return self.whole + (1 if self.closer > 1e-6 else 0)


@dataclass(frozen=True)
class CurveRing:
    """A ring of stretchers round the plan: its inside face moved out ``reach`` from the
    chamber's, and its pieces."""

    reach: float  # in
    runs: tuple[Run, ...]

    @property
    def bricks(self) -> int:
        return sum(r.bricks for r in self.runs)


def _straight_run(length: float) -> Run:
    n = math.floor(length / STRAIGHT + 1e-9)
    return Run("straight", length, n, length - n * STRAIGHT)


def _arc_run(a: Arc, corner: bool) -> Run:
    length = a.length
    if corner or a.radius <= STRAIGHT / 2:
        return Run("corner", length, math.ceil(length / STRAIGHT - 1e-9), 0.0)
    theta = 2 * math.asin(min(1.0, STRAIGHT / 2 / a.radius))
    sweep = abs(a.sweep)
    n = math.floor(sweep / theta + 1e-9)
    rest = sweep - n * theta
    closer = 2 * a.radius * math.sin(rest / 2) if rest > 1e-9 else 0.0
    if a.sweep > 0:
        return Run("convex", length, n, closer, joint=2 * THROUGH * math.sin(theta / 2))
    return Run("concave", length, n, closer, cut=math.degrees(theta / 2))


def ring_runs(inside: Outline, reach: float) -> tuple[Run, ...]:
    """A ring's pieces along its inside face, in inches, the plan moved out ``reach``: the arcs
    outline.offset adds at the plan's corners, of radius ``reach``, are laid as corners."""
    runs: list[Run] = []
    for s in inside.segments:
        if isinstance(s, Line):
            runs.append(_straight_run(s.length))
        elif isinstance(s, Arc):
            runs.append(_arc_run(s, reach > 0 and abs(s.radius - reach) < 1e-6))
    return tuple(runs)


def curve_rings(kiln: Kiln, inner: float, thickness: float) -> list[CurveRing] | None:
    """The 4½ in stretcher rings of a curved plan's wall layer from ``inner`` to ``inner +
    thickness`` out from the chamber's inside (in); None when the layer isn't whole rings."""
    from kilndesigner.form import plan_of

    count = round(thickness / THROUGH)
    if count < 1 or abs(thickness - count * THROUGH) > 1 / 25.4:
        return None
    plan = plan_of(kiln, "in")
    rings: list[CurveRing] = []
    for j in range(count):
        reach = inner + j * THROUGH
        rings.append(CurveRing(reach, ring_runs(offset(plan, reach), reach)))
    return rings


WORDS = (
    ("straight", "on straight walls"),
    ("convex", "round the convex curves, mortar in the wedge joints"),
    ("concave", "round the reverse curves, cut to the angle"),
    ("corner", "lapped and cut at corners"),
)


def describe(rings: list[CurveRing], courses: int) -> str:
    """'ring 1 (inside): 41 bricks a course: …'."""
    parts: list[str] = []
    for i, ring in enumerate(rings, 1):
        bits: list[str] = []
        for kind, word in WORDS:
            runs = [r for r in ring.runs if r.kind == kind]
            if not runs:
                continue
            n = sum(r.bricks for r in runs)
            text = f"{n} {word}"
            if kind == "convex":
                text += f" (joints to {max(r.joint for r in runs):.2f} in at the outside)"
            if kind == "concave":
                text += f" ({max(r.cut for r in runs):.1f}° off square at each end)"
            bits.append(text)
        parts.append(f"ring {i} from the inside, {ring.bricks} bricks a course: " + ", ".join(bits))
    return f"{courses} courses of 2½ in; " + "; ".join(parts)


def courses(height_in: float) -> int:
    """Courses of stretchers to the wall's height, the top one ripped to fit."""
    return math.ceil(height_in / COURSE - 1e-9)


__all__ = ["SOURCE", "CurveRing", "Run", "courses", "curve_rings", "describe", "ring_runs"]
