"""Chambers in a row, laid out in brick: climbing, tandem and tube kilns (geometry.lining_parts).

The chambers stand front to back along y, the first centred on the origin, each ``depth`` deep
with a wall between it and the next as thick as the side walls' layers, as the shells are drawn
(massing.run_of). On a slope the floors step up the ground: each chamber's floor stands a step
above the last, the pitch of a chamber and its wall times the tangent of the slope, as Olsen's
climbing kilns step 12–15 in from chamber to chamber (kiln-reference.md, Tube and climbing chamber
kilns, p.97). Every chamber's own parts are then level, so their bricks are laid in level courses.

- The floor runs under each chamber and the wall in front of the next one, at the chamber's level;
  on the level it runs the whole length.
- The side walls run through, past the end walls and the walls between chambers, which fit
  between them. On a slope each chamber has its own side walls, and a piece beside each wall
  between chambers that stands as tall as the wall.
- A wall between chambers stands on the lower chamber's floor and rises to the higher chamber's
  springline.
- Each chamber's sprung arch spans along the draft, front to back over its depth, as in Olsen's
  climbing kilns, whose arches throw their thrust onto the common wall (p.94–95), and runs across
  the kiln over the side walls; the side walls are capped up to it. Its skewbacks and fill stand on
  the walls in front of and behind it. Where two chambers share a wall, each chamber's arch and
  fill stop at the wall's middle on the level, or at the lower chamber's face of the wall on a
  slope, where the wall rises past the lower arch's springline.
- A tube's vault (``roof.tube``) spans the width instead and runs along the draft, chamber by
  chamber, as a single chamber's arch does; the end walls and the walls between chambers under it
  are filled up to it, and the side walls carry its skewbacks.
- A dome stands on each chamber's walls the same way, its walls filled up to it; a flat roof is
  laid over each chamber; an open top has nothing over the walls.
- Each wall between chambers has Olsen's standard flue holes, 4½ × 9 in with a 9 in separator,
  at the higher chamber's floor (p.96, p.45): ``flue_holes``.

A catenary over level chambers is one vault the whole run long (geometry._catenary_parts); over
chambers stepped up a slope it isn't laid out (geometry.not_drawn).
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any

from kilndesigner.geometry import SOLID_KINDS, ArchShape, DomeShape, Part, bulge_fill, thicknesses
from kilndesigner.model import Dome, FlatRoof, Kiln, SprungArch
from kilndesigner.shape import Arch, SailDome, along_arch
from kilndesigner.units import si

if TYPE_CHECKING:
    from kilndesigner.firebox_parts import Opening
    from kilndesigner.hardware import Hardware

type Outline = list[tuple[float, float]]

STEPS = 48  # points along an arch's curve


@dataclass(frozen=True)
class RunLayout:
    """Where the chambers stand, laid out straight (mm)."""

    width: float
    depth: float
    height: float  # floor to springline
    chambers: int
    between: float  # a wall between chambers
    step: float  # how far each chamber's floor stands above the last's

    @property
    def pitch(self) -> float:
        return self.depth + self.between

    def centre(self, i: int) -> float:
        return i * self.pitch

    def front(self, i: int) -> float:
        return self.centre(i) - self.depth / 2

    def back(self, i: int) -> float:
        return self.centre(i) + self.depth / 2

    def floor(self, i: int) -> float:
        return i * self.step

    @property
    def length(self) -> float:
        return self.chambers * self.depth + (self.chambers - 1) * self.between

    def step_at(self, y: float) -> float:
        """How high the floor stands at y along the run (mm)."""
        i = math.floor((y + self.depth / 2) / self.pitch)
        return self.floor(min(max(i, 0), self.chambers - 1))


def run_layout(kiln: Kiln) -> RunLayout:
    c = kiln.chamber
    between = sum(si(x.thickness, "mm") for x in kiln.lining.walls)
    depth = si(c.depth, "mm")
    slope = math.radians(si(c.slope, "degree")) if c.slope is not None else 0.0
    return RunLayout(
        width=si(c.width, "mm"),
        depth=depth,
        height=si(c.height, "mm"),
        chambers=c.chambers,
        between=between,
        step=(depth + between) * math.tan(slope),
    )


def _clip(points: Outline, lo: float, hi: float) -> Outline:
    """The outline cut to lo ≤ u ≤ hi, u its first coordinate (Sutherland–Hodgman)."""

    def half(pts: Outline, keep: Callable[[float], bool], edge: float) -> Outline:
        out: Outline = []
        for k, q in enumerate(pts):
            p = pts[k - 1]
            if keep(q[0]):
                if not keep(p[0]):
                    out.append(_meet(p, q, edge))
                out.append(q)
            elif keep(p[0]):
                out.append(_meet(p, q, edge))
        return out

    pts = half(points, lambda u: u >= lo - 1e-9, lo)
    return half(pts, lambda u: u <= hi + 1e-9, hi) if pts else pts


def _meet(p: tuple[float, float], q: tuple[float, float], u: float) -> tuple[float, float]:
    t = (u - p[0]) / (q[0] - p[0])
    return (u, p[1] + t * (q[1] - p[1]))


def _arc(c: float, centre_z: float, r: float, half_angle: float) -> Outline:
    """A circle's arc in the y–z plane about (c, centre_z), from the front springing to the back."""
    angles = [math.pi / 2 + half_angle - 2 * half_angle * k / STEPS for k in range(STEPS + 1)]
    return [(c - r * math.cos(t), centre_z + r * math.sin(t)) for t in angles]


def run_parts(kiln: Kiln) -> list[Part]:
    """The lining of chambers in a row, part by part."""
    from kilndesigner.castable import resolve_material

    run = run_layout(kiln)
    w, h, n, t = run.width, run.height, run.chambers, run.between
    stepped = run.step > 1e-6
    faces = ("left", "right", "front", "back")
    layers = {f: thicknesses(kiln, f) for f in faces}
    walls = [(x.material, si(x.thickness, "mm")) for x in kiln.lining.walls]
    reach = {f: sum(th for _, th in layers[f]) for f in faces}
    x0, x1 = -w / 2 - reach["left"], w / 2 + reach["right"]
    y0, y1 = run.front(0) - reach["front"], run.back(n - 1) + reach["back"]
    parts: list[Part] = []

    def kind(mat: str) -> str:
        return resolve_material(kiln, mat).kind

    def named(face: str) -> str:
        return "door" if face == kiln.door_wall else face

    def box(name: str, mat: str, face: str, lo: Any, hi: Any, chamber: int | None) -> Part:
        return Part(name, mat, kind(mat), lo, hi, face=face, chamber=chamber)  # type: ignore[arg-type]

    def suffix(i: int) -> str:
        return f"-chamber-{i + 1}"

    # Each chamber's stretch of the run: from the far face of the wall in front of it (the outside
    # of the front wall, for the first) to the far face of the wall behind it
    def stretch(i: int) -> tuple[float, float]:
        start = y0 if i == 0 else run.back(i - 1) + t
        return start, (y1 if i == n - 1 else run.back(i) + t)

    # Where a chamber's roof stops, front and back
    def clip(i: int) -> tuple[float, float]:
        front = y0 if i == 0 else run.back(i - 1) + (0.0 if stepped else t / 2)
        back = y1 if i == n - 1 else run.back(i) + (0.0 if stepped else t / 2)
        return front, back

    # One chamber's arch springing lower at the front (roof.front_springline): the front wall
    # stands to its own springline, the side walls to the lower one, capped up to the arch
    roof = kiln.roof
    drop = (
        along_arch(kiln, "mm").drop
        if isinstance(roof, SprungArch) and roof.front_springline is not None
        else 0.0
    )
    low = h - max(drop, 0.0)
    floor = thicknesses(kiln, "floor")
    spans = [(i, *stretch(i)) for i in range(n)] if stepped else [(None, y0, y1)]
    for i, a, b in spans:
        z = run.floor(i or 0)
        cum = 0.0
        for k, (mat, th) in enumerate(floor):
            name = f"floor/{k + 1}-{mat}" + (suffix(i) if i is not None else "")
            parts.append(box(name, mat, "floor", (x0, a, z - cum - th), (x1, b, z - cum),
                             None if i is None else i + 1))  # fmt: skip
            cum += th

    # Each wall part, and the chamber whose springline tops it (None: every chamber's, on the level)
    walls_up: list[tuple[Part, int | None]] = []
    for side, sign in (("left", -1), ("right", 1)):
        reached = 0.0
        for k, (mat, th) in enumerate(layers[side]):
            xs = sorted((sign * (w / 2 + reached), sign * (w / 2 + reached + th)))
            base = f"{named(side)}/{k + 1}-{mat}"
            if not stepped:
                p = box(base, mat, side, (xs[0], y0, 0.0), (xs[1], y1, low), None)
                parts.append(p)
                walls_up.append((p, None))
            else:
                for i in range(n):
                    a, b = stretch(i)
                    z = run.floor(i)
                    end = b if i == n - 1 else run.back(i)
                    p = box(base + suffix(i), mat, side, (xs[0], a, z), (xs[1], end, z + h), i + 1)
                    parts.append(p)
                    walls_up.append((p, i))
                    if i < n - 1:
                        top = run.floor(i + 1) + h
                        p = box(f"{base}{suffix(i)}-by-wall", mat, side, (xs[0], end, z),
                                (xs[1], b, top), i + 1)  # fmt: skip
                        parts.append(p)
                        walls_up.append((p, i + 1))
            reached += th

    # The end walls, and the walls between chambers, between the side walls
    ends: list[tuple[str, int, float, int, list[tuple[str, float]], float]] = [
        ("front", -1, run.front(0), 0, layers["front"], h - drop),
        ("back", 1, run.back(n - 1), n - 1, layers["back"], run.floor(n - 1) + h),
    ]
    for face, sign, at, i, stack, top in ends:
        reached = 0.0
        for k, (mat, th) in enumerate(stack):
            ys = sorted((at + sign * reached, at + sign * (reached + th)))
            name = f"{named(face)}/{k + 1}-{mat}"
            p = box(name, mat, face, (-w / 2, ys[0], run.floor(i)), (w / 2, ys[1], top),
                    i + 1 if stepped else None)  # fmt: skip
            parts.append(p)
            walls_up.append((p, i if stepped else None))
            reached += th
    for i in range(n - 1):
        reached = 0.0
        for k, (mat, th) in enumerate(walls):
            y = run.back(i) + reached
            top = run.floor(i + 1) + h
            p = box(f"division/{k + 1}-{mat}{suffix(i)}", mat, "back", (-w / 2, y, run.floor(i)),
                    (w / 2, y + th, top), i + 1)  # fmt: skip
            parts.append(p)
            walls_up.append((p, i + 1 if stepped else None))
            reached += th

    rings = thicknesses(kiln, "roof")
    for i in range(n):
        lo, hi = clip(i)
        springline = run.floor(i) + h
        if isinstance(roof, FlatRoof):
            cum = 0.0
            for k, (mat, th) in enumerate(rings):
                parts.append(box(f"roof/{k + 1}-{mat}{suffix(i)}", mat, "roof",
                                 (x0, lo, springline + cum), (x1, hi, springline + cum + th),
                                 i + 1))  # fmt: skip
                cum += th
        elif isinstance(roof, SprungArch) and roof.tube:
            parts += _tube(kiln, run, i, (lo, hi), rings, walls_up, layers)
        elif isinstance(roof, SprungArch):
            parts += _arch(kiln, run, i, (lo, hi), (x0, x1), rings, walls_up, layers, walls)
        elif isinstance(roof, Dome):
            parts += _dome(kiln, run, i, (lo, hi), (x0, x1), rings, walls_up)
    return parts


def _main_solid(kiln: Kiln, stack: list[tuple[str, float]]) -> str | None:
    from kilndesigner.castable import resolve_material

    solid = [x for x in stack if resolve_material(kiln, x[0]).kind in SOLID_KINDS]
    return max(solid, key=lambda x: x[1])[0] if solid else None


def _arch(
    kiln: Kiln,
    run: RunLayout,
    i: int,
    ends: tuple[float, float],
    xs: tuple[float, float],
    rings: list[tuple[str, float]],
    walls_up: list[tuple[Part, int | None]],
    layers: dict[str, list[tuple[str, float]]],
    walls: list[tuple[str, float]],
) -> list[Part]:
    """Chamber i's arch along the draft: its rings, the side walls' caps, its skewbacks."""
    from kilndesigner.castable import resolve_material

    assert isinstance(kiln.roof, SprungArch)
    arch = along_arch(kiln, "mm")
    if arch.drop:
        return _uneven_arch(kiln, run, arch, ends, xs, rings, walls_up, layers)
    springline = run.floor(i) + run.height
    centre_z = springline + arch.rise - arch.radius
    c = run.centre(i)
    a = arch.half_angle
    lo, hi = ends
    tag = f"-chamber-{i + 1}"
    parts: list[Part] = []

    def kind(mat: str) -> str:
        return resolve_material(kiln, mat).kind

    def part(name: str, mat: str, face: str, outline: Outline, x: tuple[float, float],
             **extra: Any) -> Part:  # fmt: skip
        ys, zs = [p[0] for p in outline], [p[1] for p in outline]
        return Part(
            name, mat, kind(mat), (x[0], min(ys), min(zs)), (x[1], max(ys), max(zs)),
            face=face, profile=tuple(outline), across=True, chamber=i + 1,  # type: ignore[arg-type]
            **extra,
        )  # fmt: skip

    cum = 0.0
    for k, (mat, th) in enumerate(rings):
        r = arch.radius + cum
        outline = [*_arc(c, centre_z, r, a), *reversed(_arc(c, centre_z, r + th, a))]
        clipped = _clip(outline, lo, hi)
        # A ring whole between where the roof stops keeps its arch, to be counted in shapes
        reach = (r + th) * (1.0 if a > math.pi / 2 else math.sin(a))  # widest past a semicircle
        whole = c - reach >= lo - 1e-6 and c + reach <= hi + 1e-6
        shape = ArchShape(r, th, centre_z, a) if whole else None
        parts.append(
            part(f"roof/{k + 1}-{mat}{tag}", mat, "roof", clipped, xs, ring=th, arch=shape)
        )
        cum += th
    # The side walls closing the arch: each layer filled up to the arch's inside
    inside = _arc(c, centre_z, arch.radius, a)
    for p, owner in walls_up:
        if p.wall not in ("left", "right") or not _tops(p, owner, i, run):
            continue
        if p.hi[1] <= c - run.depth / 2 + 1e-6 or p.lo[1] >= c + run.depth / 2 - 1e-6:
            continue  # beside a wall between chambers, not under this arch
        name = p.name.rsplit("-chamber-", 1)[0] if "-chamber-" in p.name else p.name
        cap = part(f"{name}{tag}-arch", p.material, p.wall, inside, (p.lo[0], p.hi[0]), cap=True)
        parts.append(replace(cap, chamber=p.chamber or i + 1))
    # The skewbacks, along the arch's radius at the springline, out to where the roof stops
    r_out = arch.radius + cum
    for face, sign, end in (("front", -1, lo), ("back", 1, hi)):
        outer = abs(end - c)
        if outer <= run.depth / 2 + 1e-6:
            continue  # the wall rises past the springline: the arch stops against it
        first, last = i == 0, i == run.chambers - 1
        stack = (layers["front"] if first else walls) if face == "front" else (
            layers["back"] if last else walls
        )  # fmt: skip
        mat = _main_solid(kiln, stack)
        if mat is None:
            continue  # nothing to spring an arch from
        top = (r_out * math.sin(a), centre_z + r_out * math.cos(a))
        if a > math.pi / 2:  # past a semicircle: the fill beside the ring's bulge
            half = bulge_fill(r_out, centre_z, springline, outer)
            if not half:
                continue  # the ring bulges past where the roof stops
        elif top[0] <= outer:
            half = [(run.depth / 2, springline), top, (outer, top[1]), (outer, springline)]
        else:
            r = outer / math.sin(a)
            half = [(run.depth / 2, springline), (outer, centre_z + r * math.cos(a)),
                    (outer, springline)]  # fmt: skip
        outline = [(c + sign * u, z) for u, z in half]
        parts.append(part(f"{face}/skewback-{mat}{tag}", mat, face, outline, xs))
    return parts


def _tube(
    kiln: Kiln,
    run: RunLayout,
    i: int,
    ends: tuple[float, float],
    rings: list[tuple[str, float]],
    walls_up: list[tuple[Part, int | None]],
    layers: dict[str, list[tuple[str, float]]],
) -> list[Part]:
    """Chamber i's stretch of a tube's vault: the arch spans the width and runs along the draft,
    as a single chamber's does (geometry._level_parts), from where chamber i's roof starts to where
    it stops. The end walls and the walls between chambers under it are filled up to it, and the
    side walls carry its skewbacks."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.geometry import _skewbacks  # pyright: ignore[reportPrivateUsage]

    assert isinstance(kiln.roof, SprungArch)
    w = run.width
    arch = Arch(w, si(kiln.roof.rise, "mm"))
    springline = run.floor(i) + run.height
    centre_z = springline + arch.rise - arch.radius
    lo, hi = ends
    tag = f"-chamber-{i + 1}"
    parts: list[Part] = []

    def kind(mat: str) -> str:
        return resolve_material(kiln, mat).kind

    # The walls across the run whose tops are this chamber's springline, under its stretch
    for p, owner in walls_up:
        if p.wall not in ("front", "back") or not _tops(p, owner, i, run):
            continue
        mid = (p.lo[1] + p.hi[1]) / 2
        last = i == run.chambers - 1
        if mid < lo - 1e-6 or (mid >= hi - 1e-6 and not last):
            continue  # under the next chamber's stretch, where a shared wall is counted once
        shape = ArchShape(arch.radius, 0.0, centre_z, arch.half_angle)
        name = p.name.rsplit("-chamber-", 1)[0] if "-chamber-" in p.name else p.name
        parts.append(
            Part(
                f"{name}{tag}-arch", p.material, p.kind, (-arch.half_width, p.lo[1], springline),
                (arch.half_width, p.hi[1], springline + arch.rise), arch=shape, cap=True,
                face=p.face, chamber=p.chamber or i + 1,
            )
        )  # fmt: skip
    cum = 0.0
    for k, (mat, th) in enumerate(rings):
        r_in = arch.radius + cum
        half = (r_in + th) * (1.0 if arch.half_angle > math.pi / 2 else math.sin(arch.half_angle))
        low = min(springline, centre_z + (r_in + th) * math.cos(arch.half_angle))
        parts.append(
            Part(
                f"roof/{k + 1}-{mat}{tag}", mat, kind(mat), (-half, lo, low),
                (half, hi, centre_z + r_in + th), face="roof", chamber=i + 1,
                arch=ArchShape(r_in, th, centre_z, arch.half_angle),
            )
        )  # fmt: skip
        cum += th
    # The skewbacks, laid out at the floor and raised to this chamber's springline
    rise = run.floor(i)
    level = _skewbacks(kiln, arch, centre_z - rise, cum, (lo, hi), layers)
    for p in level:
        assert p.profile is not None
        parts.append(
            replace(
                p, name=f"{p.name}{tag}", chamber=i + 1,
                lo=(p.lo[0], p.lo[1], p.lo[2] + rise), hi=(p.hi[0], p.hi[1], p.hi[2] + rise),
                profile=tuple((x, z + rise) for x, z in p.profile),
            )
        )  # fmt: skip
    return parts


def _uneven_arc(c: float, centre_z: float, r: float, arch: Arch) -> Outline:
    """An arch's arc springing unevenly, in the y–z plane, from the front springing to the back:
    about its centre ``arch.offset`` behind the chamber's middle ``c``."""
    f, b = arch.front_angle, arch.back_angle
    angles = [-f + (f + b) * k / STEPS for k in range(STEPS + 1)]
    return [(c + arch.offset + r * math.sin(t), centre_z + r * math.cos(t)) for t in angles]


def _uneven_arch(
    kiln: Kiln,
    run: RunLayout,
    arch: Arch,
    ends: tuple[float, float],
    xs: tuple[float, float],
    rings: list[tuple[str, float]],
    walls_up: list[tuple[Part, int | None]],
    layers: dict[str, list[tuple[str, float]]],
) -> list[Part]:
    """One chamber's arch along its depth springing at different heights at its ends
    (roof.front_springline, Bowen Mountain, Fig 4-153): its rings, the side walls' caps up to it
    from the lower springline, and a skewback on each end wall at its own springline."""
    from kilndesigner.castable import resolve_material

    back = run.height  # the back's springline; the front's is ``drop`` lower
    front = back - arch.drop
    low = min(front, back)
    centre_z = back + arch.rise - arch.radius
    c, half = run.centre(0), run.depth / 2
    lo, hi = ends
    parts: list[Part] = []

    def part(name: str, mat: str, face: str, outline: Outline, x: tuple[float, float],
             **extra: Any) -> Part:  # fmt: skip
        ys, zs = [p[0] for p in outline], [p[1] for p in outline]
        return Part(
            name, mat, resolve_material(kiln, mat).kind, (x[0], min(ys), min(zs)),
            (x[1], max(ys), max(zs)), face=face, profile=tuple(outline), across=True,  # type: ignore[arg-type]
            chamber=1, **extra,
        )  # fmt: skip

    cum = 0.0
    for k, (mat, th) in enumerate(rings):
        r = arch.radius + cum
        outline = [*_uneven_arc(c, centre_z, r, arch), *reversed(_uneven_arc(c, centre_z, r + th,
                                                                           arch))]  # fmt: skip
        clipped = _clip(outline, lo, hi)
        ys = [p[0] for p in outline]
        whole = min(ys) >= lo - 1e-6 and max(ys) <= hi + 1e-6
        shape = ArchShape(r, th, centre_z, arch.half_angle) if whole else None
        parts.append(part(f"roof/{k + 1}-{mat}-chamber-1", mat, "roof", clipped, xs, ring=th,
                          arch=shape))  # fmt: skip
        cum += th
    # The side walls closing the arch, from the lower springline up to its inside
    inside = _uneven_arc(c, centre_z, arch.radius, arch)
    if back > low + 1e-6:
        inside.append((c + half, low))
    if front > low + 1e-6:
        inside.append((c - half, low))
    for p, _ in walls_up:
        if p.wall not in ("left", "right"):
            continue
        cap = part(f"{p.name}-chamber-1-arch", p.material, p.wall, inside, (p.lo[0], p.hi[0]),
                   cap=True)  # fmt: skip
        parts.append(cap)
    # A skewback on each end wall at its own springline, along the arch's radius there
    r_out = arch.radius + cum
    for face, sign, end, angle, springline in (
        ("front", -1, lo, arch.front_angle, front),
        ("back", 1, hi, arch.back_angle, back),
    ):
        outer = abs(end - c)
        mat = _main_solid(kiln, layers[face])
        if outer <= half + 1e-6 or mat is None:
            continue
        u_c = sign * arch.offset  # the centre, out towards this end from the middle
        corner = (u_c + r_out * math.sin(angle), centre_z + r_out * math.cos(angle))
        if corner[0] <= outer:
            local = [(half, springline), corner, (outer, corner[1]), (outer, springline)]
        else:
            rho = (outer - u_c) / math.sin(angle)
            local = [(half, springline), (outer, centre_z + rho * math.cos(angle)),
                     (outer, springline)]  # fmt: skip
        outline = [(c + sign * u, z) for u, z in local]
        parts.append(part(f"{face}/skewback-{mat}-chamber-1", mat, face, outline, xs))
    return parts


def _tops(p: Part, owner: int | None, i: int, run: RunLayout) -> bool:
    """Whether the wall part's top is chamber i's springline."""
    return abs(p.hi[2] - (run.floor(i) + run.height)) < 1e-6 and owner in (None, i)


def _dome(
    kiln: Kiln,
    run: RunLayout,
    i: int,
    ends: tuple[float, float],
    xs: tuple[float, float],
    rings: list[tuple[str, float]],
    walls_up: list[tuple[Part, int | None]],
) -> list[Part]:
    """Chamber i's dome: the walls under it filled up to it, and its layers over the chamber."""
    from kilndesigner.castable import resolve_material

    assert isinstance(kiln.roof, Dome)
    dome = SailDome(run.width, run.depth, si(kiln.roof.rise, "mm"))
    springline = run.floor(i) + run.height
    centre, r, c = springline + dome.centre, dome.radius, run.centre(i)
    lo, hi = ends
    tag = f"-chamber-{i + 1}"
    parts: list[Part] = []
    for p, owner in walls_up:
        if not _tops(p, owner, i, run):
            continue
        a, b = max(p.lo[1], lo), min(p.hi[1], hi)
        if b - a < 1e-6:
            continue
        near_x = min(max(0.0, p.lo[0]), p.hi[0])
        near_y = min(max(c, a), b) - c
        if r * r <= near_x**2 + near_y**2:
            continue
        top = centre + math.sqrt(r * r - near_x**2 - near_y**2)
        if top <= springline + 1e-6:
            continue
        name = p.name.rsplit("-chamber-", 1)[0] if "-chamber-" in p.name else p.name
        parts.append(
            Part(
                f"{name}{tag}-dome", p.material, p.kind, (p.lo[0], a, springline),
                (p.hi[0], b, top), cap=True, face=p.face, chamber=p.chamber or i + 1,
                dome=DomeShape(r, 0.0, centre, c),
            )
        )  # fmt: skip
    cum = 0.0
    for k, (mat, th) in enumerate(rings):
        parts.append(
            Part(
                f"roof/{k + 1}-{mat}{tag}", mat, resolve_material(kiln, mat).kind,
                (xs[0], lo, springline), (xs[1], hi, centre + r + cum + th), face="roof",
                chamber=i + 1, dome=DomeShape(r + cum, th, centre, c),
            )
        )  # fmt: skip
        cum += th
    return parts


FLUE_WIDTH = 4.5 * 25.4  # Olsen's standard flue between chambers, 4½ × 9 in (p.96)
FLUE_HEIGHT = 9 * 25.4
FLUE_PIER = 9 * 25.4  # a 9 in flue separator (p.45)
FLUE_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.96 (standard 4½ × 9 in flues at 9 in), p.45 (a 9 in flue "
    "separator; flue holes on a header course)"
)


@dataclass(frozen=True)
class FlueRow:
    """The flue holes through the wall between chambers ``chamber`` and the next (mm)."""

    chamber: int  # from 1
    count: int
    bottom: float
    top: float


def flue_rows(kiln: Kiln) -> list[FlueRow]:
    """Olsen's standard flues through each wall between chambers: 4½ in wide and 9 in tall, as
    many as fit across the chamber with a 9 in separator between each, their foot at the higher
    chamber's floor, so the gases pass along the floor into it (p.96, p.45). Each stops at the
    lower chamber's springline."""
    run = run_layout(kiln)
    n = max(1, math.floor((run.width + FLUE_PIER) / (FLUE_WIDTH + FLUE_PIER) + 1e-9))
    rows: list[FlueRow] = []
    for i in range(run.chambers - 1):
        bottom = run.floor(i + 1)
        top = min(bottom + FLUE_HEIGHT, run.floor(i) + run.height)
        if top - bottom > 1e-6:
            rows.append(FlueRow(i + 1, n, bottom, top))
    return rows


def flue_holes(kiln: Kiln) -> list[Opening]:
    """The flue holes, to cut from the walls between chambers."""
    from kilndesigner.firebox_parts import Opening

    run = run_layout(kiln)
    out: list[Opening] = []
    for row in flue_rows(kiln):
        i = row.chamber - 1
        span = row.count * FLUE_WIDTH + (row.count - 1) * FLUE_PIER
        y0, y1 = run.back(i) - 1.0, run.back(i) + run.between + 1.0
        for k in range(row.count):
            x = -span / 2 + k * (FLUE_WIDTH + FLUE_PIER)
            out.append(
                Opening(f"flue-{row.chamber}-{k + 1}", (x, y0, row.bottom),
                        (x + FLUE_WIDTH, y1, row.top))
            )  # fmt: skip
    return out


def run_holes(kiln: Kiln, hardware: Hardware | None) -> list[tuple[Any, Any, Any]]:
    """The ports through the lining, where the shells put them on a level run, raised with the
    floor they stand on."""
    from dataclasses import replace

    from build123d import Pos

    from kilndesigner.massing import port_solid, run_of

    if hardware is None:
        return []
    run = replace(run_of(kiln), slope=0.0)
    layout = run_layout(kiln)
    holes: list[tuple[Any, Any, Any]] = []
    for spot in hardware.ports:
        hole = port_solid(kiln, run, spot)
        hole = Pos(0, 0, layout.step_at(hole.bounding_box().center().Y)) * hole
        bb = hole.bounding_box()
        holes.append(((bb.min.X, bb.min.Y, bb.min.Z), (bb.max.X, bb.max.Y, bb.max.Z), hole))
    return holes


def run_pieces(kiln: Kiln, hardware: Hardware | None) -> list[Any]:
    """The chimney and burners, where the shells put them on a level run, raised with the floor
    they stand by."""
    from dataclasses import replace

    from build123d import Pos

    from kilndesigner.massing import moved_pieces, run_of

    layout = run_layout(kiln)
    out: list[Any] = []
    for solid in moved_pieces(kiln, replace(run_of(kiln), slope=0.0), hardware):
        label, colour = solid.label, solid.color
        moved = Pos(0, 0, layout.step_at(solid.bounding_box().center().Y)) * solid
        moved.label, moved.color = label, colour
        out.append(moved)
    return out
