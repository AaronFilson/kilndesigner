"""The 3D model of a kiln whose bricks can't yet be laid out: runs that bend, and a catenary over
chambers in a row (geometry.not_drawn says which). Round kilns, chambers in a row and sloping
chambers are drawn part by part (geometry.py, run_parts.py), but take their ports and their
chimney and burners from here.

The lining is drawn as shells: the chamber's inside, offset outward by each layer's reach and
the inner offset taken away, so every layer wraps the whole kiln. The shell takes the walls'
layers everywhere, and the floor and roof are drawn with them (their own layers are calculated,
not drawn). Fireboxes are hollowed into the shell; ports are cut where the hardware layout puts
them (hardware.build_hardware), mapped onto the curved or longer walls. Nothing here is a rule
of thumb: every size is the design's or the engine's.

Coordinates are those of geometry.py: millimetres, x across, y from the firing end to the flue
end, z up from the first chamber's floor. The first chamber is centred on the origin, as the
hardware layout expects, and the others follow it in y.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Any, Literal

from kilndesigner.model import CatenaryArch, Dome, Firebox, Kiln, OpenTop, SprungArch
from kilndesigner.units import si

if TYPE_CHECKING:
    from kilndesigner.hardware import Hardware, PortSpot

MM = 25.4
type Point = tuple[float, float, float]


class MassingError(ValueError):
    """The shape can't be drawn: too tight a bend for the kiln's width, say."""


@dataclass(frozen=True)
class Run:
    """The kiln's inside, laid out: its chambers along the run and how the run bends and climbs."""

    round: bool
    width: float  # mm, inside (a round chamber's diameter)
    depth: float  # one chamber's depth
    height: float  # floor to springline (or crown, of a catenary)
    chambers: int
    between: float  # a wall between two chambers
    slope: float  # radians
    bend: float  # radians

    @property
    def length(self) -> float:
        """The run's inside length, firing end to flue end, walls between included (mm)."""
        return self.chambers * self.depth + (self.chambers - 1) * self.between

    def chamber_centre(self, i: int) -> float:
        """The y of chamber i's centre, before the run bends or climbs."""
        return i * (self.depth + self.between)

    @property
    def radius(self) -> float:
        """The bend's radius, to the run's centreline (mm); infinite when straight."""
        return self.length / self.bend if self.bend > 0 else math.inf


def run_of(kiln: Kiln) -> Run:
    c = kiln.chamber
    walls = kiln.lining.walls
    between = sum(si(x.thickness, "mm") for x in walls)
    return Run(
        round=c.shape == "round",
        width=si(c.width, "mm"),
        depth=si(c.depth, "mm"),
        height=si(c.height, "mm"),
        chambers=c.chambers,
        between=between,
        slope=math.radians(si(c.slope, "degree")) if c.slope is not None else 0.0,
        bend=math.radians(si(c.bend, "degree")) if c.bend is not None else 0.0,
    )


def place(run: Run, p: Point) -> Point:
    """Where a point laid out straight and level ends up once the run bends and climbs. The run
    bends from the first chamber's front face, about a vertical axis to its left, and climbs
    about the x axis through the front face's foot."""
    x, y, z = p
    front = -run.depth / 2
    s = y - front
    if run.bend > 0 and s > 0:
        rho = run.radius
        a = min(s, run.length) / rho
        beyond = max(0.0, s - run.length)
        cx, cy = -rho, front
        x, y = (
            cx + (rho + x) * math.cos(a) - beyond * math.sin(a),
            cy + (rho + x) * math.sin(a) + beyond * math.cos(a),
        )
    if run.slope > 0:
        dy = y - front
        y = front + dy * math.cos(run.slope) - z * math.sin(run.slope)
        z = dy * math.sin(run.slope) + z * math.cos(run.slope)
    return (x, y, z)


def turn_at(run: Run, y: float) -> float:
    """How far the run has turned (radians) at y, laid out straight."""
    if run.bend <= 0:
        return 0.0
    s = min(max(y + run.depth / 2, 0.0), run.length)
    return s / run.radius


@dataclass(frozen=True)
class Cell:
    """A piece of the inside, laid out straight and level: a box (with its roof) or a cylinder,
    centred at ``y`` and ``length`` long; its roof's arch spans across x, or along y (``along``)."""

    kind: Literal["box", "round", "pit"]
    y: float
    length: float
    x: float = 0.0
    width: float = 0.0
    z0: float = 0.0
    z1: float = 0.0
    along: bool = False


def cells(kiln: Kiln, run: Run) -> list[Cell]:
    """The inside as cells: one per chamber (or eight along a bent single chamber), and one per
    firebox."""
    out: list[Cell] = []
    if run.round:
        out.append(Cell("round", 0.0, run.width, width=run.width, z1=run.height))
    else:
        many = run.chambers > 1
        if many:
            for i in range(run.chambers):
                out.append(
                    Cell("box", run.chamber_centre(i), run.depth, width=run.width, z1=run.height,
                         along=True)
                )  # fmt: skip
        else:
            pieces = 8 if run.bend > 0 else 1
            step = run.depth / pieces
            for i in range(pieces):
                y = -run.depth / 2 + step * (i + 0.5)
                out.append(Cell("box", y, step, width=run.width, z1=run.height))
    fire = kiln.heat.fire
    for box in fire.fireboxes if fire is not None else []:
        out += _firebox_cells(kiln, run, box)
    return out


def _firebox_cells(kiln: Kiln, run: Run, box: Firebox) -> list[Cell]:
    """Each firebox of this size, against its wall and spread evenly along it. Fireboxes that
    don't fit side by side, one to a chamber in a row, are troughs along each chamber's front, as
    in the Kyoto kilns' himae (Olsen, 4th ed. p.92). A firebox whose height isn't given is drawn as
    tall as it is wide, and said so in its title."""
    fw, fl = si(box.width, "mm"), si(box.length, "mm")
    fh = si(box.height, "mm") if box.height is not None else fw
    n = box.count
    out: list[Cell] = []
    face = box.position
    across = run.width if face in ("front", "back", "under") else run.length
    if face in ("front", "back") and n * fw > across + 1e-6 and 1 < n <= run.chambers:
        for i in range(n):
            y = run.chamber_centre(i) - run.depth / 2 + fw / 2
            out.append(Cell("pit", y, fw, width=min(fl, run.width), z0=-fh, z1=0.0))
        return out
    centres = [across * ((i + 0.5) / n - 0.5) for i in range(n)]
    back = run.chamber_centre(run.chambers - 1) + run.depth / 2
    front = -run.depth / 2
    for c in centres:
        if face == "front":
            out.append(Cell("pit", front - fl / 2, fl + 2, x=c, width=fw, z0=0.0, z1=fh))
        elif face == "back":
            out.append(Cell("pit", back + fl / 2, fl + 2, x=c, width=fw, z0=0.0, z1=fh))
        elif face == "under":
            # Under the floor, below the floor's shell, along the run
            low = -run.between
            out.append(Cell("pit", (back + front) / 2, min(fl, run.length), x=c, width=fw,
                            z0=low - fh, z1=low))  # fmt: skip
        else:
            sign = -1 if face == "left" else 1
            # Against a side wall: its length runs out along x
            x = sign * (run.width / 2 + fl / 2)
            y = front + run.length / 2 + c
            out.append(Cell("pit", y, fw, x=x, width=fl + 2, z0=0.0, z1=fh))
    return out


def _roof_top(kiln: Kiln, run: Run) -> float:
    """How far above the springline the inside rises at its crown (mm)."""
    roof = kiln.roof
    if isinstance(roof, SprungArch | Dome):
        return si(roof.rise, "mm")
    return 0.0


# --- Solids (build123d, imported lazily) ------------------------------------------------------


def _cavity(kiln: Kiln, run: Run, cell: Cell, r: float) -> Any:
    """The cell's inside grown outward by r (mm), laid out straight and level at the origin."""
    from build123d import Box, Cylinder, Pos, Sphere

    roof = kiln.roof
    open_top = isinstance(roof, OpenTop)
    if cell.kind == "pit":
        z0, z1 = cell.z0 - r, cell.z1 + r
        return Pos(cell.x, 0, (z0 + z1) / 2) * Box(cell.width + 2 * r, cell.length, z1 - z0)
    if cell.kind == "round":
        # A round chamber takes a dome, a flat roof or none (model.py)
        radius = run.width / 2
        top = run.height if open_top else run.height + r
        body = Pos(0, 0, (top - r) / 2) * Cylinder(radius + r, top + r)
        if isinstance(roof, Dome):
            body = body + _cap(radius + r, _roof_top(kiln, run) + r, run.height)
        return body
    w, length = run.width, cell.length
    top = run.height if open_top else run.height + r
    body = Pos(0, 0, (top - r) / 2) * Box(w + 2 * r, length, top + r)
    if isinstance(roof, CatenaryArch):
        return _parabola(w / 2 + r, run.height + r, length, -r)
    if isinstance(roof, SprungArch):
        span = run.depth if cell.along else w
        rise = _roof_top(kiln, run)
        radius = (span**2 / 4 + rise**2) / (2 * rise)
        centre = run.height + rise - radius
        vault = Cylinder(radius + r, (w + 2 * r) if cell.along else length)
        turned = (
            Pos(0, 0, centre) * vault.rotate(_axis("y"), 90)
            if cell.along
            else Pos(0, 0, centre) * vault.rotate(_axis("x"), 90)
        )
        above = Pos(0, 0, run.height + (rise + r) / 2) * Box(w + 2 * r, length, rise + r)
        return body + (turned & above)
    if isinstance(roof, Dome):
        half_diagonal = math.hypot(w, length) / 2
        rise = _roof_top(kiln, run)
        radius = (half_diagonal**2 + rise**2) / (2 * rise)
        centre = run.height + rise - radius
        above = Pos(0, 0, run.height + (rise + r) / 2) * Box(w + 2 * r, length, rise + r)
        return body + ((Pos(0, 0, centre) * Sphere(radius + r)) & above)
    return body


def _axis(name: str) -> Any:
    from build123d import Axis

    return {"x": Axis.X, "y": Axis.Y}[name]


def _cap(base_radius: float, rise: float, z0: float) -> Any:
    """A sphere's cap on a circle of ``base_radius`` at height z0, rising ``rise``."""
    from build123d import Box, Pos, Sphere

    radius = (base_radius**2 + rise**2) / (2 * rise)
    centre = z0 + rise - radius
    keep = Pos(0, 0, z0 + rise / 2) * Box(2 * base_radius, 2 * base_radius, rise)
    return (Pos(0, 0, centre) * Sphere(radius)) & keep


def _parabola(half: float, height: float, length: float, z0: float) -> Any:
    """A parabolic tunnel, Ward's stand-in for a catenary (combustion-and-masonry.md [S28])."""
    from build123d import Plane, Polyline, Pos, extrude, make_face

    steps = 24
    pts = [(half * (2 * i / steps - 1), z0 + height * (1 - (2 * i / steps - 1) ** 2))
           for i in range(steps + 1)]  # fmt: skip
    outline = Polyline(*pts, close=True)
    face = Plane.XZ * make_face(outline)
    return Pos(0, length / 2, 0) * extrude(face, length)


def _located(run: Run, cell: Cell, solid: Any) -> Any:
    """Put a cell's solid where it goes: along the run, turned with the bend, tilted with the
    slope."""
    from build123d import Axis, Pos

    x, y, _ = place(replace(run, slope=0.0), (0.0, cell.y, 0.0))
    turn = turn_at(run, cell.y)
    if turn:
        solid = solid.rotate(Axis.Z, math.degrees(turn))
    solid = Pos(x, y, 0) * solid
    if run.slope > 0:
        front = Axis((0, -run.depth / 2, 0), (1, 0, 0))
        solid = solid.rotate(front, math.degrees(run.slope))
    return solid


def _grow(kiln: Kiln, run: Run, cell: Cell, r: float) -> Any:
    """A cell's cavity grown by r, lengthened so neighbours' shells close round a bend."""
    grow = 0.0
    if run.bend > 0 and cell.kind == "box":
        step = cell.length / run.radius
        grow = 2 * (run.width / 2 + r) * math.tan(step / 2) + 1.0
    long = replace(cell, length=cell.length + grow + 2 * r)
    return _located(run, cell, _cavity(kiln, run, long, r))


def _union(solids: list[Any]) -> Any:
    shape = solids[0]
    for s in solids[1:]:
        shape = shape + s
    return shape


def shell_layers(kiln: Kiln) -> list[tuple[str, str, Any]]:
    """Each layer of the walls as a solid shell round the whole inside: (name, material, solid)."""
    run = run_of(kiln)
    check_bend(run)
    inside = cells(kiln, run)
    layers = [(x.material, si(x.thickness, "mm")) for x in kiln.lining.walls]
    out: list[tuple[str, str, Any]] = []
    reach = 0.0
    hollow = _union([_grow(kiln, run, c, 0.0) for c in inside])
    for i, (material, thickness) in enumerate(layers):
        outer = _union([_grow(kiln, run, c, reach + thickness) for c in inside])
        out.append((f"shell/{i + 1}-{material}", material, outer - hollow))
        hollow = outer
        reach += thickness
    return out


def check_bend(run: Run) -> None:
    if run.bend > 0 and run.radius <= run.width / 2 + run.between:
        raise MassingError(
            f"a {math.degrees(run.bend):.0f}° bend over a {run.length / MM:.0f} in run turns "
            f"tighter than the kiln is wide; make the bend smaller or the run longer"
        )


# --- Ports --------------------------------------------------------------------------------------


def port_axis(kiln: Kiln, run: Run, spot: PortSpot) -> tuple[Point, Point]:
    """The port's centre on the inside face and the point a wall's thickness outside it, laid
    out straight and level (mm). On a round kiln, ``across`` is along the curve."""
    t = run.between
    up = spot.up * MM
    across = spot.across * MM
    face = spot.wall
    if run.round:
        radius = run.width / 2
        base = {"front": -math.pi / 2, "right": 0.0, "back": math.pi / 2, "left": math.pi}[face]
        # To the right, facing the wall from outside, is anticlockwise seen from above
        a = base + across / radius
        inner = (radius * math.cos(a), radius * math.sin(a), up)
        outer = ((radius + t + 50) * math.cos(a), (radius + t + 50) * math.sin(a), up)
        return inner, outer
    half_w = run.width / 2
    front = -run.depth / 2
    back = run.chamber_centre(run.chambers - 1) + run.depth / 2
    if face == "front":
        return (across, front, up), (across, front - t - 50, up)
    if face == "back":
        return (-across, back, up), (-across, back + t + 50, up)
    if face == "left":
        return (-half_w, -across, up), (-half_w - t - 50, -across, up)
    return (half_w, across, up), (half_w + t + 50, across, up)


def port_solid(kiln: Kiln, run: Run, spot: PortSpot) -> Any:
    """A hole through the shell for the port: a cylinder, or a box, along its axis."""
    from build123d import Box, Cylinder, Plane, Vector

    inner, outer = (place(run, p) for p in port_axis(kiln, run, spot))
    a, b = Vector(*inner), Vector(*outer)
    start = a - (b - a).normalized() * 30
    axis = b - start
    centre = start + axis * 0.5
    if spot.round:
        hole: Any = Cylinder(spot.width * MM / 2, axis.length)
    else:
        # The port's width runs level along the wall, its height up the wall
        hole = Box(spot.width * MM, spot.height * MM, axis.length)
    z = axis.normalized()
    level = Vector(0, 0, 1).cross(z)
    return Plane(origin=centre, x_dir=level.normalized(), z_dir=z) * hole


# --- The model -----------------------------------------------------------------------------------


def build_massing(kiln: Kiln, hardware: Hardware | None) -> Any:
    """The kiln's shells, fireboxes and ports, and the hardware that sits clear of the bricks:
    its burners and chimney, moved with the flue end."""
    from build123d import Color, Compound

    from kilndesigner.castable import resolve_material
    from kilndesigner.geometry import COLOURS

    run = run_of(kiln)
    holes = [port_solid(kiln, run, s) for s in (hardware.ports if hardware else [])]
    children: list[Any] = []
    for name, material, solid in shell_layers(kiln):
        for hole in holes:
            solid = solid - hole
        solid.label = name
        solid.color = Color(*COLOURS.get(resolve_material(kiln, material).kind, (0.8, 0.8, 0.8)))
        children.append(solid)
    for piece in moved_pieces(kiln, run, hardware):
        children.append(piece)
    model = Compound(children=children)
    model.label = kiln.name
    return model


def moved_pieces(kiln: Kiln, run: Run, hardware: Hardware | None) -> list[Any]:
    """The chimney, its duct and the burners, moved from the first chamber's walls to where the
    run puts them. The frame and door are drawn for a box on a stand, so they're left out."""
    from build123d import Axis, Color, Pos

    from kilndesigner.geometry import COLOURS, piece_solid

    out: list[Any] = []
    if hardware is None:
        return out
    shift = run.chamber_centre(run.chambers - 1)
    for piece in hardware.pieces:
        if not piece.name.startswith(("chimney/", "burner/")):
            continue
        solid = piece_solid(piece)
        bb = solid.bounding_box()
        foot = (bb.center().X, bb.center().Y, bb.min.Z)
        if run.round:
            moved = foot
        else:
            at_back = foot[1] > run.depth / 2
            local = (foot[0], foot[1] + (shift if at_back else 0.0), foot[2])
            moved = place(run, local)
            turn = turn_at(run, local[1]) if at_back else 0.0
            if turn:
                solid = solid.rotate(Axis((foot[0], foot[1], 0), (0, 0, 1)), math.degrees(turn))
        solid = Pos(moved[0] - foot[0], moved[1] - foot[1], moved[2] - foot[2]) * solid
        solid.label = piece.name
        solid.color = Color(*COLOURS.get(piece.kind, (0.8, 0.8, 0.8)))
        out.append(solid)
    return out


def massing_index(kiln: Kiln, hardware: Hardware | None) -> dict[str, dict[str, str]]:
    """What each part of the massing model is, for the viewer."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.geometry import KIND_NAMES, colour
    from kilndesigner.working import length_text

    us = kiln.units == "us"
    index: dict[str, dict[str, str]] = {}
    for i, layer in enumerate(kiln.lining.walls):
        m = resolve_material(kiln, layer.material)
        index[f"shell/{i + 1}-{layer.material}"] = {
            "title": f"Lining, layer {i + 1}",
            "detail": (
                f"{m.name}, {length_text(si(layer.thickness, 'mm'), us)} thick: the walls' "
                "layers, drawn round the whole kiln, the floor and roof too"
            ),
            "kind": KIND_NAMES.get(m.kind, m.kind),
            "colour": colour(m.kind),
        }
    for piece in hardware.pieces if hardware else []:
        if piece.name.startswith(("chimney/", "burner/")):
            index[piece.name] = {
                "title": piece.title,
                "detail": piece.detail,
                "kind": KIND_NAMES.get(piece.kind, piece.kind),
                "colour": colour(piece.kind),
            }
    return index


def massing_layout(kiln: Kiln, hardware: Hardware) -> dict[str, object]:
    """The hardware layout, with what the viewer needs to put ports on curved and longer walls: a
    round chamber's inside radius, and the run's chambers, slope and bend."""
    from kilndesigner.hardware import layout

    run = run_of(kiln)
    out = layout(kiln, hardware)
    out["run"] = {
        "round": run.round,
        "radius": run.width / 2 if run.round else None,
        "chambers": run.chambers,
        "depth": run.depth,
        "chamber_pitch": run.depth + run.between,
        "slope": math.degrees(run.slope),
        "bend": math.degrees(run.bend),
        "length": run.length,
    }
    return out
