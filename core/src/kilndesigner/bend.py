"""A run that bends in plan (chamber.bend), laid out in brick.

The lining is laid out straight (geometry.lining_parts) and bent as the shells are (massing.place):
the run's centreline turns left on a circular arc from the first chamber's front face, through
the bend, over the run's inside length; what stands before the front face stays straight, and
what stands past the run's end carries on along its last tangent.

- **Model**: each part's section across the run (x–z) is swept round the bend's centre where it
  lies in the bend, and carried straight before and after it, so the walls curve as they're built.
  A part whose section changes along the run (an arch along the draft, a dome, a firebox's
  pieces) is moved whole, to where its middle lies.
- **Masonry**: a layer on the inside of the bend is shorter than the centreline, one on the
  outside longer: by Pappus's theorem a section swept round a centre sweeps its centroid's path,
  so each layer is counted at the length its middle runs, (ρ + x)·θ in the bend, ρ the
  centreline's radius and x the layer's offset from it, as model.Chamber.bend says.
- **Plans**: drawn straightened, as the bricks are counted, and said so.
"""

from __future__ import annotations

import math
from dataclasses import replace
from typing import TYPE_CHECKING, Any

from kilndesigner.model import Kiln
from kilndesigner.units import si

if TYPE_CHECKING:
    from kilndesigner.geometry import Part
    from kilndesigner.massing import Run


def bent(kiln: Kiln) -> bool:
    c = kiln.chamber
    return c.bend is not None and si(c.bend, "degree") > 0


def _section_centre(part: Part) -> float:
    """The x of the centroid of a part's section across the run."""
    if part.arch is not None:
        return 0.0  # an arch's ring or cap is symmetric about the centre line
    if part.profile is not None and not part.across:
        pts = part.profile
        area = cx = 0.0
        for (x0, z0), (x1, z1) in zip(pts, (*pts[1:], pts[0]), strict=True):
            cross = x0 * z1 - x1 * z0
            area += cross
            cx += (x0 + x1) * cross
        return cx / (3 * area) if abs(area) > 1e-9 else (part.lo[0] + part.hi[0]) / 2
    return (part.lo[0] + part.hi[0]) / 2


def developed(kiln: Kiln, parts: list[Part]) -> list[Part]:
    """The parts of a bent run as they're counted: each part that runs along the run, its length
    in the bend scaled to its centroid's path, (ρ + x)/ρ."""
    if not bent(kiln):
        return parts
    from kilndesigner.massing import run_of

    run = run_of(kiln)
    front, back = -run.depth / 2, -run.depth / 2 + run.length
    out: list[Part] = []
    for p in parts:
        if p.across or p.dome is not None or p.revolve is not None:
            out.append(p)
            continue
        inside = max(0.0, min(p.hi[1], back) - max(p.lo[1], front))
        grown = inside * _section_centre(p) / run.radius
        out.append(replace(p, hi=(p.hi[0], p.hi[1] + grown, p.hi[2])))
    return out


def _axis(run: Run) -> Any:
    from build123d import Axis

    return Axis((-run.radius, -run.depth / 2, 0), (0, 0, 1))


def _sweep(section: list[tuple[float, float]], y0: float, y1: float, run: Run) -> Any:
    """A section (x, z) carried from y0 to y1 along the bent run."""
    from build123d import Plane, Polygon, Pos, extrude, revolve

    front = -run.depth / 2
    back = front + run.length
    pieces: list[Any] = []

    def straight(a: float, b: float) -> Any:
        solid: Any = extrude(Plane.XZ * Polygon(*section, align=None), amount=b - a)
        return Pos(0, a - solid.bounding_box().min.Y, 0) * solid

    if y0 < front - 1e-6:
        pieces.append(straight(y0, min(y1, front)))
    a, b = max(y0, front), min(y1, back)
    if b - a > 1e-6:
        face: Any = Pos(0, front, 0) * (Plane.XZ * Polygon(*section, align=None))
        swept: Any = revolve(face, _axis(run), math.degrees((b - a) / run.radius))
        pieces.append(swept.rotate(_axis(run), math.degrees((a - front) / run.radius)))
    if y1 > back + 1e-6:
        beyond = straight(max(y0, back), y1)
        beyond = Pos(0, front - back, 0) * beyond
        pieces.append(beyond.rotate(_axis(run), math.degrees(run.length / run.radius)))
    solid = pieces[0]
    for p in pieces[1:]:
        solid = solid + p
    return solid


def moved(solid: Any, y: float, run: Run) -> Any:
    """A solid laid out straight, moved whole to where its middle ``y`` lies on the bent run."""
    from build123d import Pos

    s = y + run.depth / 2  # along the run from its front face
    if s <= 0:
        return solid
    along = min(s, run.length)
    # Back along the run by what the bend turns, then round the bend's centre (massing.place)
    return (Pos(0, -along, 0) * solid).rotate(_axis(run), math.degrees(along / run.radius))


def bent_solid(part: Part, run: Run) -> Any | None:
    """The part's solid on the bent run."""
    from kilndesigner.geometry import _level_solid, arch_outline  # pyright: ignore[reportPrivateUsage]

    if part.across or part.dome is not None or part.revolve is not None:
        solid = _level_solid(part)
        return None if solid is None else moved(solid, (part.lo[1] + part.hi[1]) / 2, run)
    if part.arch is not None:
        section = arch_outline(part)
    elif part.profile is not None:
        section = list(part.profile)
    else:
        if any(b - a < 1e-6 for a, b in zip(part.lo, part.hi, strict=True)):
            return None
        (x0, _, z0), (x1, _, z1) = part.lo, part.hi
        section = [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]
    return _sweep(section, part.lo[1], part.hi[1], run)


def bent_box(lo: tuple[float, float, float], hi: tuple[float, float, float], run: Run) -> Any:
    """A box laid out straight (a hole), on the bent run."""
    section = [(lo[0], lo[2]), (hi[0], lo[2]), (hi[0], hi[2]), (lo[0], hi[2])]
    return _sweep(section, lo[1], hi[1], run)


def note(kiln: Kiln) -> str:
    """What the masonry and plans say of a bent run."""
    from kilndesigner.massing import run_of
    from kilndesigner.working import length_text

    run = run_of(kiln)
    us = kiln.units == "us"
    return (
        f"The run bends {math.degrees(run.bend):.3g}° to the left over its "
        f"{length_text(run.length, us)} inside, its centreline on a "
        f"{length_text(run.radius, us)} radius. The plans draw it straightened; each layer along "
        "the run is counted at the length its middle runs round the bend, (radius + offset) × "
        "angle (Pappus's theorem), so the walls on the inside of the bend take fewer bricks and "
        "those outside more. Straight bricks in a curved wall open their joints on the outside of "
        "the curve; no source here sizes tapered bricks for a wall's bend."
    )
