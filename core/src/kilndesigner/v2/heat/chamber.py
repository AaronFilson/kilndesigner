"""The chamber the heat model radiates in, from the engine's own solids and layout (ADR 0017 H5):
the gas volume as `massing._cavity` draws each cell (the solid the 3-D model and the statics are
cut from), its faces named by where they are, and the design's openings carved from them.

Every shape the engine draws (B1):
- **a box chamber** under a sprung arch, a sail dome, a catenary (Ward's parabola), a flat roof or
  none; its end walls' segments over the springline counted with their walls;
- **a round chamber** (a cylinder: its "wall"), under a dome, a flat roof or open at the top;
- **chambers in a row** (`chamber.chambers`, of one size or of `chamber.sizes`, climbing or not):
  one gas zone each, joined through the flue holes in the walls between them
  (`run_parts.flue_rows`), the holes' sides named "flues" and built in that wall;
- **a tube as segments along its length** (a single chamber cut into ``segments`` gas zones, its
  walls split where they are cut), and a tunnel whose width changes (`chamber.widths`);
- **crossing gas paths** (`roof.crossing`: Fireworks, Church): the two tubes' insides as one, the
  groin where their vaults meet.

Each gas zone owns slabs of space along the run (`rays.Region`), cut at the middle of each wall
between chambers and at each segment's end, so a ray's path splits among the zones exactly. The
solid is split at the same planes, so no face straddles two zones; the cut faces are gas, not
surfaces. A run's slope and the climb of its chambers turn the whole solid without changing what
any face sees, so the rays are traced on the run laid out straight and level (massing's frame);
a bent run (`chamber.bend`) isn't (refused).

Names: with one gas zone, "floor", "left", "right", "front", "back", "roof" (the arch, dome or
vault), "wall" (a round chamber's), "open top"; with several, each with its zone's number
("floor 2"), and "flues 2" for the flue holes' sides in zone 2.

Frame: metres here, x across, y from the firing end to the flue end, z up from the first chamber's
floor; the first chamber centred on x = y = 0. A wall's "across" is to your right standing outside
and facing it, as the design file has it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from typing import Any, Literal

import numpy as np

from kilndesigner.model import Kiln, OpenTop
from kilndesigner.units import si
from kilndesigner.v2.heat.rays import Patch, Region, Zone, face_triangles

MM = 1e-3
COURSE = 2.5 * 0.0254  # a 2½ in course: the engine lays burner ports one course up
BIG = 1e3  # m: the regions reach this far, past any kiln
EPS = 0.5  # mm: a step into the gas from a face, to find its zone and its side

WALLS = ("left", "right", "front", "back")
type Point = tuple[float, float, float]


class NotModelledError(ValueError):
    """A chamber or opening the heat model doesn't take yet."""


@dataclass(frozen=True)
class GasZone:
    """A gas zone of the path: its name, what it is, and the slabs of space it owns (m)."""

    name: str
    kind: Literal["firebox", "chamber", "chimney"]
    regions: tuple[tuple[Point, Point], ...]
    volume: float  # m³, the solid's


@dataclass(frozen=True)
class Room:
    """A chamber's (or a segment's) inside: its box to the springline (m) and what rises over it,
    for its setting and its walls' sides."""

    lo: Point
    hi: Point
    rise: float


@dataclass(frozen=True)
class Chamber:
    """The inside: its surfaces, its openings, the first chamber's size (m), the gas volume (m³),
    and, for each surface, the wall it is built in and the gas zone it faces."""

    zones: tuple[Zone, ...]
    patches: tuple[Patch, ...]
    width: float
    depth: float
    height: float
    volume: float
    notes: tuple[str, ...] = ()
    gas: tuple[GasZone, ...] = ()
    built: dict[str, tuple[str, int]] = field(default_factory=dict[str, tuple[str, int]])
    rooms: tuple[Room, ...] = ()
    shape: Literal["box", "round", "crossing"] = "box"

    def regions(self) -> list[Region]:
        return [Region(k, lo, hi) for k, g in enumerate(self.gas) for lo, hi in g.regions]


# --- the solid ---------------------------------------------------------------------------------


@dataclass(frozen=True)
class _Layout:
    """The run laid out straight (mm): each chamber's span along y and its springline and rise,
    the walls between them (y spans), and where the gas zones are cut."""

    width: float
    chambers: tuple[tuple[float, float, float, float], ...]  # (front, back, springline, rise)
    walls: tuple[tuple[float, float], ...]
    cuts: tuple[float, ...]
    round: bool = False


def _layout(kiln: Kiln, run: Any, segments: int) -> _Layout:
    from kilndesigner.massing import _roof_top  # pyright: ignore[reportPrivateUsage]

    rows = []
    for i in range(run.chambers):
        c, d = run.chamber_centre(i), run.depth_of(i)
        h, rise = (run.sizes[i][1], run.sizes[i][2]) if run.sizes else (run.height, None)
        rows.append((c - d / 2, c + d / 2, h, rise if rise is not None else _roof_top(kiln, run)))
    walls = tuple((rows[i][1], rows[i + 1][0]) for i in range(len(rows) - 1))
    if run.chambers > 1:
        cuts = tuple((a + b) / 2 for a, b in walls)
    else:
        front, back = rows[0][0], rows[0][1]
        cuts = tuple(front + (back - front) * k / segments for k in range(1, segments))
    return _Layout(run.width, tuple(rows), walls, cuts, run.round)


def _tube_solid(t: Any) -> Any:
    """One of a crossing's two tubes (mm): its box to the springline and its vault over it."""
    from build123d import Box, Cylinder, Pos

    from kilndesigner.massing import _axis  # pyright: ignore[reportPrivateUsage]

    lo, hi = t.run
    length, mid = hi - lo, (lo + hi) / 2
    h, span = t.springline, t.span
    if t.axis == 1:  # along y, its span across x
        body = Pos(t.centre, mid, h / 2) * Box(span, length, h)
        vault = Pos(t.centre, mid, t.centre_z) * Cylinder(t.radius, length).rotate(_axis("x"), 90)
        above = Pos(t.centre, mid, h + t.rise / 2) * Box(span, length, t.rise)
    else:  # along x, its span across y
        body = Pos(mid, t.centre, h / 2) * Box(length, span, h)
        vault = Pos(mid, t.centre, t.centre_z) * Cylinder(t.radius, length).rotate(_axis("y"), 90)
        above = Pos(mid, t.centre, h + t.rise / 2) * Box(length, span, t.rise)
    return body + (vault & above)


def _solid(kiln: Kiln, run: Any, lay: _Layout) -> tuple[Any, str]:
    """The gas volume (mm): the chambers' cells, the flue holes between them, or a crossing's two
    tubes; and the shape."""
    from build123d import Box, Pos

    from kilndesigner.crossing import crossed
    from kilndesigner.groin import tubes
    from kilndesigner.massing import (
        _cavity,  # pyright: ignore[reportPrivateUsage]
        _roof_top,  # pyright: ignore[reportPrivateUsage]
        cells,
    )

    if crossed(kiln):
        a, b = tubes(kiln, "mm")
        return _tube_solid(a) + _tube_solid(b), "crossing"
    parts = []
    for c in cells(kiln, run):
        if c.kind == "pit":
            continue
        if c.kind == "box" and run.height <= 0 and c.rise is None:
            # An arch springing from the floor: massing draws it as a cell of its own size
            c = replace(c, rise=_roof_top(kiln, run))
        parts.append(Pos(0, c.y, 0) * _cavity(kiln, run, c, 0.0))
    if run.chambers > 1:
        from kilndesigner.run_parts import flue_rows

        for row in flue_rows(kiln):
            y0, y1 = lay.walls[row.chamber - 1]
            span = row.count * row.pitch - (row.pitch - row.width)
            tall = row.top - row.bottom
            for k in range(row.count):
                x = -span / 2 + k * row.pitch + row.width / 2
                parts.append(Pos(x, (y0 + y1) / 2, tall / 2) * Box(row.width, y1 - y0, tall))
    solid = parts[0]
    for p in parts[1:]:
        solid = solid + p
    return solid, "round" if lay.round else "box"


def _pieces(solid: Any, cuts: tuple[float, ...]) -> list[Any]:
    """The solid split at each cut (a plane square to y)."""
    from build123d import Keep, Plane

    pieces = [solid]
    for y in cuts:
        plane = Plane(origin=(0, y, 0), z_dir=(0, 1, 0))
        pieces = [s for p in pieces for s in p.split(plane, keep=Keep.ALL)]
    return pieces


def _zone_of(lay: _Layout, y: float) -> int:
    return sum(1 for c in lay.cuts if y > c)


def _namer(lay: _Layout, many: bool) -> Any:
    """Name a face of a piece (mm): skip the cuts' faces; find its zone and the way it faces from
    a point a step into the gas. Gives the name, a point on the face and its normal into the gas."""

    def name(piece: Any, face: Any) -> tuple[str, Any, Any] | None:
        planar = face.geom_type.name == "PLANE"
        p = face.center() if planar else face.position_at(0.5, 0.5)
        n = face.normal_at(p)
        inward = -n if piece.is_inside(p - n * EPS) else n
        x, y = p.X, p.Y
        if planar and abs(n.Y) > 0.999 and any(abs(y - c) < 1e-3 for c in lay.cuts):
            return None  # a cut: gas on both sides
        k = _zone_of(lay, y + inward.Y * EPS)
        tag = f" {k + 1}" if many else ""
        if any(a + 1e-3 < y < b - 1e-3 for a, b in lay.walls):
            return f"flues{tag}", p, inward
        if not planar:
            return (f"wall{tag}" if abs(inward.Z) < 1e-6 else f"roof{tag}"), p, inward
        if inward.Z > 0.999:
            return f"floor{tag}", p, inward
        if abs(inward.Y) > 0.999:
            front, back = _span(lay, k, many)
            if abs(y - front) < 1e-3 and inward.Y > 0:
                return f"front{tag}", p, inward
            if abs(y - back) < 1e-3 and inward.Y < 0:
                return f"back{tag}", p, inward
            return (f"left{tag}" if x < 0 else f"right{tag}"), p, inward  # a step in a width
        if abs(inward.X) > 0.999:
            return (f"left{tag}" if inward.X > 0 else f"right{tag}"), p, inward
        return f"roof{tag}", p, inward

    return name


def _oriented(face: Any, piece: Any) -> Any:
    """A face's triangles (m), wound so their normals point into the gas. OCCT's tessellation
    follows the face's own orientation, which a fused and split solid doesn't always keep, so the
    face's largest triangle decides for the whole face: a point 2 mm off it along its normal must
    be in the gas (the tessellation's deflection is 0.5 mm)."""
    from build123d import Vector

    t = face_triangles([face])
    if len(t) == 0:
        return t
    cr = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])
    k = int(np.argmax(np.linalg.norm(cr, axis=1)))
    nrm = cr[k] / np.linalg.norm(cr[k])
    probe = t[k].mean(axis=0) / MM + 2.0 * nrm
    if not piece.is_inside(Vector(*(float(v) for v in probe))):
        t = t[:, [0, 2, 1]]
    return t


def _span(lay: _Layout, k: int, many: bool) -> tuple[float, float]:
    """Zone k's end walls along y (mm): its chamber's, or the tube's ends."""
    rows = list(lay.chambers)
    row = rows[k] if len(rows) > 1 else rows[0]
    return row[0], row[1]


def _regions(lay: _Layout, n: int) -> list[tuple[tuple[Point, Point], ...]]:
    edges = [-BIG, *(c * MM for c in lay.cuts), BIG]
    return [(((-BIG, edges[k], -BIG), (BIG, edges[k + 1], BIG)),) for k in range(n)]


def _rooms(lay: _Layout, n: int, kiln: Kiln) -> tuple[Room, ...]:
    w = lay.width * MM
    rows = list(lay.chambers)
    if len(rows) > 1:
        return tuple(Room((-w / 2, f * MM, 0.0), (w / 2, b * MM, h * MM), r * MM)
                     for f, b, h, r in rows)  # fmt: skip
    f, b, h, r = rows[0]
    if isinstance(kiln.roof, OpenTop):
        r = 0.0
    ends = [f, *lay.cuts, b]
    return tuple(Room((-w / 2, ends[k] * MM, 0.0), (w / 2, ends[k + 1] * MM, h * MM), r * MM)
                 for k in range(n))  # fmt: skip


def _built(kiln: Kiln, name: str, chambers: int) -> str:
    """The lining face a surface is built in: the walls between chambers ("between") take their
    flue holes' sides too."""
    face, _, k = name.partition(" ")
    if face == "flues":
        return "between"
    if chambers > 1 and k:
        i = int(k)
        if (face == "front" and i > 1) or (face == "back" and i < chambers):
            return "between"
    if face == "wall":
        return "walls"
    return face


def cavity(kiln: Kiln, segments: int = 1) -> Chamber:
    """The gas volume's surfaces, gas zones and rooms from the engine's own solid; no openings."""
    from kilndesigner.massing import run_of

    if segments < 1:
        raise NotModelledError("a tube is cut into one segment or more")
    run = run_of(kiln)
    if run.bend > 0:
        raise NotModelledError(
            "a bent run (chamber.bend) isn't traced: its cells turn against each other"
        )
    if segments > 1 and (run.chambers > 1 or run.round):
        raise NotModelledError("segments cut a single box chamber; chambers in a row are zones")
    lay = _layout(kiln, run, segments)
    solid, shape = _solid(kiln, run, lay)
    if shape == "crossing":
        lay = _Layout(lay.width, lay.chambers, (), ())
    n = len(lay.cuts) + 1
    many = n > 1
    namer = _namer(lay, many)
    groups: dict[str, list[Any]] = {}
    pieces = _pieces(solid, lay.cuts)
    volumes = np.zeros(n)
    for piece in pieces:
        c = piece.center()
        volumes[_zone_of(lay, c.Y)] += float(piece.volume) * MM**3
        for face in piece.faces():
            named = namer(piece, face)
            if named is not None:
                groups.setdefault(named[0], []).append(_oriented(face, piece))
    zones = [Zone(nm, np.concatenate(groups[nm])) for nm in sorted(groups, key=_order)]
    if isinstance(kiln.roof, OpenTop):
        zones = [Zone(z.name.replace("roof", "open top"), z.triangles) for z in zones]
    gas = tuple(
        GasZone(f"chamber {k + 1}" if many else "chamber", "chamber", reg, float(volumes[k]))
        for k, reg in enumerate(_regions(lay, n))
    )
    built = {z.name: (_built(kiln, z.name, run.chambers), _zone_index(z.name, many)) for z in zones}
    f0, b0, h0, _ = lay.chambers[0]
    if shape == "crossing":
        c = kiln.chamber
        f0, b0, h0 = -si(c.depth, "mm") / 2, si(c.depth, "mm") / 2, si(c.height, "mm")
    return Chamber(
        tuple(zones), (), lay.width * MM, (b0 - f0) * MM, h0 * MM, float(volumes.sum()), (),
        gas, built, _rooms(lay, n, kiln), shape,  # type: ignore[arg-type]
    )  # fmt: skip


def _zone_index(name: str, many: bool) -> int:
    return int(name.rsplit(" ", 1)[1]) - 1 if many else 0


ORDER = ("left", "right", "front", "back", "floor", "roof", "wall", "flues")


def _order(name: str) -> tuple[int, int]:
    face, _, k = name.partition(" ")
    return (int(k) if k.isdigit() else 0, ORDER.index(face) if face in ORDER else len(ORDER))


# --- openings ----------------------------------------------------------------------------------


def wall_patch(
    name: str,
    wall: str,
    size: tuple[float, float],
    across: float,
    up: float,
    dims: Any,
    face: str | None = None,
    y0: float = 0.0,
) -> Patch:
    """A rectangle (width, height, m) on a wall, its centre ``across`` to the right seen from
    outside and ``up`` from the floor; u × v points into the gas. ``dims`` (width, depth, height)
    of the chamber whose wall it is, centred along y at ``y0``; ``face`` its surface's name."""
    w, h = size
    width, depth, _ = dims
    face = face or wall
    flat, tall = (w / 2, h / 2), (h / 2, w / 2)
    if wall == "front":
        return Patch(name, face, (across, y0 - depth / 2, up), (0, 0, 1), (1, 0, 0), tall)
    if wall == "back":
        return Patch(name, face, (-across, y0 + depth / 2, up), (1, 0, 0), (0, 0, 1), flat)
    if wall == "left":
        return Patch(name, face, (-width / 2, y0 - across, up), (0, 1, 0), (0, 0, 1), flat)
    if wall == "right":
        return Patch(name, face, (width / 2, y0 + across, up), (0, 0, 1), (0, 1, 0), tall)
    raise NotModelledError(f"an opening in the {wall} isn't placed yet")


def _size(port: Any) -> tuple[float, float, bool]:
    w, h = port.size_in()
    if port.round:  # a round hole as the square of its area (said in the working)
        side = math.sqrt(math.pi / 4) * w
        return side * 0.0254, side * 0.0254, True
    return w * 0.0254, h * 0.0254, False


def _on(c: Chamber, k: int | None) -> tuple[tuple[float, float, float], float]:
    """Chamber k's (from 0) size and middle along y (m); None: the whole run, whose walls a
    tube's segments share."""
    if not c.rooms:
        return (c.width, c.depth, c.height), 0.0
    rooms = c.rooms if k is None else (c.rooms[k],)
    lo, hi = min(r.lo[1] for r in rooms), max(r.hi[1] for r in rooms)
    return (c.width, hi - lo, rooms[0].hi[2]), (lo + hi) / 2


def _placed(c: Chamber, wall: str, p: Patch) -> Patch:
    """The opening on the surface of the gas zone its centre is in."""
    if len(c.gas) <= 1:
        return p
    y = p.centre[1]
    k = next(i for i, g in enumerate(c.gas) for lo, hi in g.regions if lo[1] <= y <= hi[1])
    return replace(p, face=f"{wall} {k + 1}")


def _flat(c: Chamber, wall: str) -> bool:
    """Whether a wall is flat for openings: a round chamber's isn't."""
    return c.shape != "round" or wall == "floor"


def openings(kiln: Kiln, c: Chamber | tuple[float, float, float]) -> tuple[list[Patch], list[str]]:
    """The design's openings as patches, and what was said about them."""
    if not isinstance(c, Chamber):  # a single box's (width, depth, height)
        c = Chamber((), (), *c, 0.0)
    out: list[Patch] = []
    notes: list[str] = []
    draft = kiln.draft
    rows = kiln.chamber.chambers > 1
    if draft is not None and draft.flue_port is not None and draft.type != "up":
        w, h, rnd = _size(draft.flue_port)
        across = si(draft.flue_across, "m") if draft.flue_across is not None else 0.0
        if _flat(c, draft.flue_wall):
            dims, y0 = _on(c, len(c.rooms) - 1 if rows else None)
            p = wall_patch("exit flue", draft.flue_wall, (w, h), across, h / 2, dims, y0=y0)
            out.append(_placed(c, draft.flue_wall, p))
            if rnd:
                notes.append("the round exit flue taken as the square of its area")
        else:
            notes.append("the exit flue in a round wall: not carved yet, left out")
    elif draft is not None and draft.exits is not None:
        out += _exits(kiln, c, rows, notes)
    if kiln.heat.fire is not None:
        out += _inlets(kiln, c, rows, notes)
    gas = kiln.heat.gas
    if gas is not None and gas.burners.count is not None and gas.burners.wall != "floor":
        from kilndesigner.firebox_parts import burner_port_in

        size = burner_port_in(kiln)
        wall = gas.burners.wall
        if size is None:
            notes.append("the burner ports' size isn't given: their openings are left out")
        elif not _flat(c, wall):
            notes.append("burner ports in a round wall: not carved yet, left out")
        else:
            pw, ph = size[0] * 0.0254, size[1] * 0.0254
            if size[2]:
                pw = ph = math.sqrt(math.pi / 4) * pw
            up = si(gas.burners.up, "m") if gas.burners.up is not None else COURSE + ph / 2
            dims, y0 = _on(c, 0 if rows else None)
            length = dims[1] if wall in ("left", "right") else dims[0]
            n = gas.burners.count
            for i in range(n):
                across = length * ((i + 0.5) / n - 0.5)
                p = wall_patch(f"burner port {i + 1}", wall, (pw, ph), across, up, dims, y0=y0)
                out.append(_placed(c, wall, p))
            notes.append("burner ports spread evenly along their wall, as the engine lays them")
    spies = kiln.spy_holes.holes if kiln.spy_holes is not None else None
    for i, hole in enumerate(spies or []):
        if hole.wall == "roof" or not _flat(c, hole.wall):
            notes.append(f"spy hole {i + 1} is in the roof or a round wall: not carved yet")
            continue
        w, h, _ = _size(hole.port)
        up = si(hole.up, "m") if hole.up is not None else h / 2
        across = si(hole.across, "m")
        dims, y0 = _on(c, min(hole.chamber - 1, len(c.rooms) - 1) if rows else None)
        p = wall_patch(f"spy hole {i + 1}", hole.wall, (w, h), across, up, dims, y0=y0)
        out.append(_placed(c, hole.wall, p))
    return _settled(c, out, notes), notes


def _settled(c: Chamber, patches: list[Patch], notes: list[str]) -> list[Patch]:
    """Each opening slid onto its face where the engine's layout puts it past the face's edge (a
    tapering width, an arch's end segment), its size kept; one with no flat face to go on, or
    larger than its face, left out. Said in the notes."""
    if not c.zones:
        return patches
    faces = {z.name: z.triangles for z in c.zones}
    out: list[Patch] = []
    for p in patches:
        tris = faces.get(p.face)
        moved = _slid(p, tris) if tris is not None else None
        if moved is None:
            notes.append(f"{p.name}: not on a flat {p.face} at its size: left out")
            continue
        shift = float(np.linalg.norm(np.subtract(moved.centre, p.centre)))
        if shift > 1e-6:
            notes.append(f"{p.name}: moved {shift * 1e3:.0f} mm onto its face, its size kept")
        out.append(moved)
    return out


def _slid(p: Patch, tris: Any) -> Patch | None:
    """The opening moved the least to lie inside the extent of its face's triangles in its own
    plane, then checked corner by corner; None if it can't."""
    from kilndesigner.v2.heat.rays import (
        _on_triangles,  # pyright: ignore[reportPrivateUsage]
    )

    c, u, v, n = (np.asarray(x, dtype=float) for x in (p.centre, p.u, p.v, p.normal))
    pts = tris.reshape(-1, 3)
    near = np.abs((pts - c) @ n) < 1e-6
    if not near.any():
        return None
    du, dv = (pts[near] - c) @ u, (pts[near] - c) @ v
    a, b = p.half
    su = min(max(0.0, du.min() + a), du.max() - a)
    sv = min(max(0.0, dv.min() + b), dv.max() - b)
    if du.max() - du.min() < 2 * a - 1e-9 or dv.max() - dv.min() < 2 * b - 1e-9:
        return None
    moved = replace(p, centre=tuple(float(x) for x in c + su * u + sv * v))  # type: ignore[arg-type]
    mc = np.asarray(moved.centre)
    for s1, s2 in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        q = mc + s1 * a * u * (1 - 1e-9) + s2 * b * v * (1 - 1e-9)
        if not _on_triangles(q, tris):
            return None
    return moved


def _exits(kiln: Kiln, c: Chamber, rows: bool, notes: list[str]) -> list[Patch]:
    """`draft.exits`: each set of holes where the engine cuts them (`openings.wall_places`,
    `grid_places`): spread along a wall at its foot, or in a grid over the floor or a flat roof,
    or as placed; in a row, in the last chamber (the flue end)."""
    from kilndesigner.openings import grid_places, wall_places

    assert kiln.draft is not None
    assert kiln.draft.exits is not None
    out: list[Patch] = []
    last = len(c.rooms) - 1 if rows else None
    for s, h in enumerate(kiln.draft.exits, 1):
        w, ht, _ = _size(h.port)
        if h.through in ("floor", "roof"):
            flat_roof = c.shape != "crossing" and not _arched(kiln)
            if h.through == "roof" and (not flat_roof or c.shape == "round"):
                notes.append(f"exit flues {s} in a curved roof: not carved yet, left out")
                continue
            dims, y0 = _on(c, last)
            span = dims[0] / math.sqrt(2) if c.shape == "round" else dims[0]
            deep = dims[0] / math.sqrt(2) if c.shape == "round" else dims[1]
            z = 0.0 if h.through == "floor" else dims[2]
            u, v = ((1, 0, 0), (0, 1, 0)) if h.through == "floor" else ((0, 1, 0), (1, 0, 0))
            for k, (x, y) in enumerate(grid_places(h, span / 0.0254, deep / 0.0254), 1):
                centre = (x * 0.0254, y0 + y * 0.0254, z)
                half = (w / 2, ht / 2) if h.through == "floor" else (ht / 2, w / 2)
                p = Patch(f"exit flue {s}.{k}", h.through, centre, u, v, half)
                out.append(_placed(c, h.through, p))
            continue
        wall = h.through
        if not _flat(c, wall):
            notes.append(f"exit flues {s} in a round wall: not carved yet, left out")
            continue
        dims, y0 = _on(c, (last if wall == "back" else 0) if rows else None)
        inside = (dims[1] if wall in ("left", "right") else dims[0]) / 0.0254
        for k, (across, up) in enumerate(wall_places(h, inside), 1):
            p = wall_patch(f"exit flue {s}.{k}", wall, (w, ht), across * 0.0254, up * 0.0254,
                           dims, y0=y0)  # fmt: skip
            out.append(_placed(c, wall, p))
    return out


def _arched(kiln: Kiln) -> bool:
    from kilndesigner.model import CatenaryArch, Dome, SprungArch

    return isinstance(kiln.roof, SprungArch | Dome | CatenaryArch)


def _inlets(kiln: Kiln, c: Chamber, rows: bool, notes: list[str]) -> list[Patch]:
    """The fireboxes' inlet flues into the chamber, the fire seen through them: up through the
    floor (under-floor fireboxes) or through a wall (fireboxes against it), at the engine's
    layout (`firebox_parts.openings`), kept on their face at their size."""
    from kilndesigner.firebox_parts import openings as fire_openings

    out: list[Patch] = []
    holes = [o for o in fire_openings(kiln) if o.name.endswith("/inlet")]
    for k, o in enumerate(holes):
        name = f"inlet flue {k + 1}"
        (x0, y0, z0), (x1, y1, z1) = (tuple(v * MM for v in o.lo), tuple(v * MM for v in o.hi))
        if o.axis == 2:  # up through the floor
            half = ((x1 - x0) / 2, (y1 - y0) / 2)
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            mx = min(max(cx, -c.width / 2 + half[0]), c.width / 2 - half[0])
            my = min(max(cy, -c.depth / 2 + half[1]), c.depth / 2 - half[1])
            if max(abs(mx - cx), abs(my - cy)) > 1e-6:
                notes.append(
                    f"{name}: the engine's layout puts it {abs(mx - cx) * 1e3:.0f} × "
                    f"{abs(my - cy) * 1e3:.0f} mm off the floor (under a wall); moved onto the "
                    "floor at its size"
                )
            p = Patch(name, "floor", (mx, my, 0.0), (1, 0, 0), (0, 1, 0), half)
            out.append(_placed(c, "floor", p))
            continue
        if c.shape == "round":
            notes.append(f"{name} through a round wall: not carved yet, left out")
            continue
        if o.axis == 1:  # through the front or back wall
            middle = (c.rooms[0].lo[1] + c.rooms[-1].hi[1]) / 2 if c.rooms else 0.0
            wall = "front" if (y0 + y1) / 2 < middle else "back"
            size = (min(x1 - x0, c.width), z1 - z0)
            across = (x0 + x1) / 2 if wall == "front" else -(x0 + x1) / 2
            across = min(max(across, -(c.width - size[0]) / 2), (c.width - size[0]) / 2)
        else:
            wall = "left" if (x0 + x1) / 2 < 0 else "right"
            size = (y1 - y0, z1 - z0)
            across = (y0 + y1) / 2
        dims, mid = _on(c, (0 if wall == "front" else len(c.rooms) - 1) if rows else None)
        if wall in ("left", "right"):
            across = mid - across if wall == "left" else across - mid
        up = min((z0 + z1) / 2, dims[2] - size[1] / 2)
        out.append(_placed(c, wall, wall_patch(name, wall, size, across, up, dims, y0=mid)))
    return out


def chamber(kiln: Kiln, segments: int = 1) -> Chamber:
    """The inside with its openings; a single chamber cut into ``segments`` along its length."""
    c = cavity(kiln, segments)
    patches, notes = openings(kiln, c)
    return replace(c, patches=tuple(patches), notes=tuple(notes))
