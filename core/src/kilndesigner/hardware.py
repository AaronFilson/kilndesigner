"""What turns a lining into a kiln: the steel, the door or car, ports, burners, chimney, spy holes.

Plain arithmetic, like :func:`kilndesigner.geometry.lining_parts`, so it can be tested without
OpenCascade. Sizes come from docs/research/kiln-hardware.md and electric-kiln-hardware.md, with
the section and source in each piece's detail. Where no source gives a size (car wheels, an
electric kiln's stand legs, a power burner's port), the piece is drawn only to show where it goes
and says so, or is left out with a finding.

Coordinates are inches here, as the sources give them, and millimetres on the way out, matching
the lining: x across the width, y from the front (negative) to the back, z up from the chamber
floor.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Literal

from kilndesigner.frame import CASE_T, FrameDesign, outside, skewback_top
from kilndesigner.gas import GasDesign
from kilndesigner.model import Kiln, SprungArch, WallFace
from kilndesigner.units import si
from kilndesigner.working import Finding

MM = 25.4
COURSE = 2.5  # in, a 2½ in brick course
BRICK = (9.0, 4.5, 2.5)  # in, a straight
CHIMNEY_BRICK = "hard-firebrick-kx99"

type Box = tuple[tuple[float, float, float], tuple[float, float, float]]


@dataclass(frozen=True)
class Cylinder:
    axis: Literal[0, 1, 2]
    centre: tuple[float, float, float]  # mm
    radius: float
    length: float


@dataclass(frozen=True)
class Piece:
    """A solid part: one or more boxes and cylinders fused, in mm."""

    name: str
    kind: str  # a colour key: a material kind, "steel" or "burner"
    title: str
    detail: str
    boxes: tuple[Box, ...] = ()
    cylinders: tuple[Cylinder, ...] = ()
    material: str | None = None

    @property
    def volume(self) -> float:
        """mm³: the boxes only (brick pieces have no cylinders)."""
        return sum(math.prod(h - lo for lo, h in zip(*b, strict=True)) for b in self.boxes)


@dataclass(frozen=True)
class Opening:
    """A hole cut through whatever it meets: a box, or a round hole along ``axis``."""

    name: str
    title: str
    box: Box
    round_axis: Literal[0, 1, 2] | None = None


@dataclass
class Hardware:
    pieces: list[Piece] = field(default_factory=list[Piece])
    openings: list[Opening] = field(default_factory=list[Opening])
    findings: list[Finding] = field(default_factory=list[Finding])
    chimney_bricks: int = 0


def _mm(b: tuple[tuple[float, float, float], tuple[float, float, float]]) -> Box:
    (x0, y0, z0), (x1, y1, z1) = b
    lo = (min(x0, x1) * MM, min(y0, y1) * MM, min(z0, z1) * MM)
    hi = (max(x0, x1) * MM, max(y0, y1) * MM, max(z0, z1) * MM)
    return lo, hi


class Faces:
    """Boxes placed on a wall's outside face: u along the face, z up, w outwards from it (in)."""

    def __init__(self, kiln: Kiln) -> None:
        o = outside(kiln)
        w, d = si(kiln.chamber.width, "in"), si(kiln.chamber.depth, "in")

        def t(face: str) -> float:
            layers = kiln.lining.for_face(face, door_face=kiln.door_face)  # type: ignore[arg-type]
            return sum(si(x.thickness, "in") for x in layers)

        self.thickness = {f: t(f) for f in ("left", "right", "front", "back")}
        self.x0, self.x1 = -w / 2 - self.thickness["left"], w / 2 + self.thickness["right"]
        self.y0, self.y1 = -d / 2 - self.thickness["front"], d / 2 + self.thickness["back"]
        self.bottom = -o.bottom
        self.inside = {"front": w, "back": w, "left": d, "right": d}

    def plane(self, face: WallFace) -> float:
        return {"front": self.y0, "back": self.y1, "left": self.x0, "right": self.x1}[face]

    def span(self, face: WallFace) -> tuple[float, float]:
        """The face's outside extent along u."""
        return (self.x0, self.x1) if face in ("front", "back") else (self.y0, self.y1)

    def box(
        self,
        face: WallFace,
        u: tuple[float, float],
        z: tuple[float, float],
        w: tuple[float, float],
    ) -> Box:
        sign = -1 if face in ("front", "left") else 1
        p = self.plane(face)
        n = (p + sign * w[0], p + sign * w[1])
        if face in ("front", "back"):
            return _mm(((u[0], n[0], z[0]), (u[1], n[1], z[1])))
        return _mm(((n[0], u[0], z[0]), (n[1], u[1], z[1])))

    def through(self, face: WallFace, u: tuple[float, float], z: tuple[float, float]) -> Box:
        """A box through the whole wall and anything on its face."""
        return self.box(face, u, z, (-self.thickness[face] - 1, 4))

    def point(self, face: WallFace, u: float, z: float, w: float) -> tuple[float, float, float]:
        lo, _ = self.box(face, (u, u), (z, z), (w, w))
        return lo[0], lo[1], lo[2]

    @staticmethod
    def normal_axis(face: WallFace) -> Literal[0, 1]:
        return 1 if face in ("front", "back") else 0


def build_hardware(kiln: Kiln, frame: FrameDesign, gas: GasDesign | None) -> Hardware:
    hw = Hardware()
    f = Faces(kiln)
    _frame(kiln, frame, f, hw)
    _door_or_car(kiln, frame, f, hw)
    if gas is not None:
        _burners(kiln, gas, f, hw)
        _flue_and_chimney(kiln, gas, f, hw)
    _spy_holes(kiln, f, hw, electric=gas is None)
    return hw


def _angle(
    name: str,
    corner: tuple[float, float],
    signs: tuple[int, int],
    z: tuple[float, float],
    leg: float,
    t: float,
) -> list[Box]:
    """An angle wrapping a vertical corner from outside: one leg on each face (in)."""
    (xc, yc), (sx, sy) = corner, signs
    del name
    leg_x = ((xc, yc - sy * (leg - t), z[0]), (xc + sx * t, yc + sy * t, z[1]))
    leg_y = ((xc - sx * (leg - t), yc, z[0]), (xc + sx * t, yc + sy * t, z[1]))
    return [_mm(leg_x), _mm(leg_y)]


def _frame(kiln: Kiln, frame: FrameDesign, f: Faces, hw: Hardware) -> None:
    leg, t = frame.angle_leg_in, frame.angle_t_in
    if frame.kind == "welded case":
        _case(kiln, f, hw)
        return
    arch = isinstance(kiln.roof, SprungArch)
    top = skewback_top(kiln) if arch else outside(kiln).wall_top
    source = frame.members[0].source or ""
    corners = [
        ((f.x0, f.y0), (-1, -1)),
        ((f.x1, f.y0), (1, -1)),
        ((f.x0, f.y1), (-1, 1)),
        ((f.x1, f.y1), (1, 1)),
    ]
    for i, (corner, signs) in enumerate(corners):
        hw.pieces.append(
            Piece(
                f"frame/post-{i + 1}",
                "steel",
                f"Corner post {i + 1} of 4",
                f"{frame.angle} angle, {top - f.bottom:.0f} in long; {source}",
                boxes=tuple(_angle("", corner, signs, (f.bottom, top + t), leg, t)),
            )
        )
    # Buttresses: on top of each side wall, vertical leg outside (Pitelka [S11])
    for side, x, s in (("left", f.x0, -1), ("right", f.x1, 1)):
        flat = ((x - s * (leg - t), f.y0 - t, top), (x + s * t, f.y1 + t, top + t))
        upright = ((x, f.y0 - t, top + t - leg), (x + s * t, f.y1 + t, top + t))
        title = "Buttress angle" if arch else "Roof angle"
        detail = (
            f"{frame.angle}, takes the arch's thrust at the skewback ({frame.thrust}); {source}"
            if arch and frame.thrust
            else f"{frame.angle}; {source}"
        )
        hw.pieces.append(
            Piece(
                f"frame/{side}-top",
                "steel",
                f"{title}, {side} side",
                detail,
                boxes=(_mm(flat), _mm(upright)),
            )
        )
    # Cross-members along the front and back, and the tie rods in front of them
    rod_r = frame.rod_d_in / 2
    for end, y, s in (("front", f.y0, -1), ("back", f.y1, 1)):
        bar = ((f.x0 - t, y, top - 2 + t), (f.x1 + t, y + s * 0.25, top + t))
        hw.pieces.append(
            Piece(
                f"frame/{end}-top",
                "steel",
                f"Top cross-member, {end}",
                f"¼ × 2 in flat bar; {source}",
                boxes=(_mm(bar),),
            )
        )
        if frame.rod:
            length = f.x1 - f.x0 + 2 * leg + 4
            centre = (0.0, (y + s * (t + rod_r + 0.1)) * MM, (top - 1 + t) * MM)
            hw.pieces.append(
                Piece(
                    f"frame/{end}-rod",
                    "steel",
                    f"Tie rod, {end}",
                    f"{frame.rod} threaded rod, {length:.0f} in long, ties the corner posts "
                    f"across the kiln; {frame.members[-1].source}",
                    cylinders=(Cylinder(0, centre, rod_r * MM, length * MM),),
                )
            )
    # The bottom ring of flat bar
    ring = [
        ((f.x0 - 0.25, f.y0, f.bottom), (f.x0, f.y1, f.bottom + 2)),
        ((f.x1, f.y0, f.bottom), (f.x1 + 0.25, f.y1, f.bottom + 2)),
        ((f.x0, f.y0 - 0.25, f.bottom), (f.x1, f.y0, f.bottom + 2)),
        ((f.x0, f.y1, f.bottom), (f.x1, f.y1 + 0.25, f.bottom + 2)),
    ]
    hw.pieces.append(
        Piece(
            "frame/bottom",
            "steel",
            "Bottom cross-members",
            f"¼ × 2 in flat bar on all four sides; {source}",
            boxes=tuple(_mm(b) for b in ring),
        )
    )


def _case(kiln: Kiln, f: Faces, hw: Hardware) -> None:
    """An electric kiln's welded case, on a stand."""
    o = outside(kiln)
    t, top = CASE_T, o.wall_top
    source = "electric-kiln-hardware.md §1.2 [S6]"
    plates = {
        "left": ((f.x0 - t, f.y0, f.bottom), (f.x0, f.y1, top)),
        "right": ((f.x1, f.y0, f.bottom), (f.x1 + t, f.y1, top)),
        "back": ((f.x0 - t, f.y1, f.bottom), (f.x1 + t, f.y1 + t, top)),
        "top": ((f.x0 - t, f.y0, top), (f.x1 + t, f.y1 + t, top + t)),
        "bottom": ((f.x0 - t, f.y0, f.bottom - t), (f.x1 + t, f.y1 + t, f.bottom)),
    }
    for name, b in plates.items():
        if name == kiln.door_face:
            continue
        hw.pieces.append(
            Piece(
                f"case/{name}",
                "steel",
                f"Case, {name}",
                f"⅛ in welded steel plate; {source}",
                boxes=(_mm(b),),
            )
        )
    # The stand: 8 in, as the makers raise their kilns [S1] [S11]
    stand, leg = 8.0, 1.5
    legs = [
        ((x, y, f.bottom - t - stand), (x + sx * leg, y + sy * leg, f.bottom - t))
        for x, sx in ((f.x0, 1), (f.x1, -1))
        for y, sy in ((f.y0, 1), (f.y1 + t, -1))
    ]
    hw.pieces.append(
        Piece(
            "case/stand",
            "steel",
            "Stand",
            "Raises the kiln 8 in off the floor, so air can move under it; electric-kiln-"
            "hardware.md §1.3 [S1] [S11]. The legs' section is not sourced: drawn to show where "
            "they go.",
            boxes=tuple(_mm(b) for b in legs),
        )
    )


def _door_or_car(kiln: Kiln, frame: FrameDesign, f: Faces, hw: Hardware) -> None:
    face = kiln.door_face
    assert face not in ("floor", "roof")
    o = outside(kiln)
    top = skewback_top(kiln) if isinstance(kiln.roof, SprungArch) else o.wall_top
    u0, u1 = f.span(face)
    if kiln.loading.type == "car":
        _car(kiln, frame, f, hw)
        return
    if kiln.door_kind == "bricked":
        hw.findings.append(
            Finding(
                level="info",
                message=(
                    f"The {face} wall is the door: bricked up, dry, for each firing. Lay the "
                    "inner and outer courses together, staggered, with a header course "
                    "two-thirds of the way up."
                ),
                reference="kiln-hardware.md §6.1 [S4]",
            )
        )
        return
    electric = frame.kind == "welded case"
    if electric:
        plate = f.box(face, (u0, u1), (f.bottom, top), (0, CASE_T))
        hw.pieces.append(
            Piece(
                "door/case",
                "steel",
                "Door case",
                "⅛ in steel; the door hangs on its hinges and is clamped shut. electric-kiln-"
                "hardware.md §2 [S6]",
                boxes=(plate,),
            )
        )
        depth = CASE_T
        pin_d, pin_len, out = 0.75, (top - f.bottom) * 0.8, 1.0
        pin_source = "a ¾ in steel hinge rod (Paragon Dragon), electric-kiln-hardware.md §2.1 [S18]"
    else:
        leg, t = 4.0, 0.25  # ¼ × 4 × 4 angle at any kiln size (Pitelka [S13])
        z0, z1 = f.bottom, top
        sides = [
            f.box(face, (u0, u0 + leg), (z0, z1), (0, t)),
            f.box(face, (u1 - leg, u1), (z0, z1), (0, t)),
            f.box(face, (u0, u1), (z0, z0 + leg), (0, t)),
            f.box(face, (u0, u1), (z1 - leg, z1), (0, t)),
        ]
        hw.pieces.append(
            Piece(
                "door/frame",
                "steel",
                "Door frame",
                "¼ × 4 × 4 in angle, mitred and welded like a picture frame; the IFB door is "
                "clamped in it. kiln-hardware.md §6.2 [S13]",
                boxes=tuple(sides),
            )
        )
        depth = t
        pin_d, pin_len, out = 0.75, 10.0, 2.5
        pin_source = (
            "two 10 in lengths of ¾ in shaft, 2½ in out from the brick face, "
            "kiln-hardware.md §6.2 [S13]"
        )
        from kilndesigner.castable import resolve_material

        kinds = {
            resolve_material(kiln, layer.material).kind
            for layer in kiln.lining.for_face(face, door_face=face)
        }
        if kinds & {"dense_firebrick", "dense_castable"}:
            hw.findings.append(
                Finding(
                    level="warning",
                    message="A hinged door should never be built from hard brick.",
                    reference="kiln-hardware.md §6.2 [S13]",
                )
            )
    height = top - f.bottom
    for i, frac in enumerate((0.25, 0.75)):
        z = f.bottom + frac * height
        hinge = f.point(face, u0, z, depth + out)
        hw.pieces.append(
            Piece(
                f"door/hinge-{i + 1}",
                "steel",
                f"Door hinge {i + 1} of 2",
                pin_source,
                cylinders=(Cylinder(2, hinge, pin_d / 2 * MM, min(pin_len, height / 2.5) * MM),),
            )
        )
        latch = f.point(face, u1 - 1.5, z, depth + 0.125)
        hw.pieces.append(
            Piece(
                f"door/latch-{i + 1}",
                "steel",
                f"Door latch {i + 1} of 2",
                "An eccentric latch: a 2 in disc on a ¾ in shaft, with a 10 in lever; kiln-"
                "hardware.md §6.2 [S13]"
                if not electric
                else "A clamp holds the door shut (L&L: DE-STA-CO clamps); size not sourced, drawn "
                "to "
                "show where it goes. electric-kiln-hardware.md §2.2 [S2]",
                cylinders=(Cylinder(Faces.normal_axis(face), latch, 1.0 * MM, 0.25 * MM),),
            )
        )


def _car(kiln: Kiln, frame: FrameDesign, f: Faces, hw: Hardware) -> None:
    """A car: a steel frame under the deck, wheels, and rails out through the car's end."""
    leg, t = max(frame.angle_leg_in, 2.0), max(frame.angle_t_in, 0.1875)
    zb = f.bottom
    ring = [
        ((f.x0, f.y0, zb - leg), (f.x0 + t, f.y1, zb)),
        ((f.x1 - t, f.y0, zb - leg), (f.x1, f.y1, zb)),
        ((f.x0, f.y0, zb - leg), (f.x1, f.y0 + t, zb)),
        ((f.x0, f.y1 - t, zb - leg), (f.x1, f.y1, zb)),
        ((f.x0, f.y0, zb - t), (f.x1, f.y1, zb)),
    ]
    hw.pieces.append(
        Piece(
            "car/frame",
            "steel",
            "Car frame",
            "A welded steel frame carrying the deck (the floor's layers) and the car's end wall; "
            "kiln-hardware.md §6.3 [S35]. No source gives its steel size: drawn in the frame's "
            "angle to show where it goes.",
            boxes=tuple(_mm(b) for b in ring),
        )
    )
    wheel_r = 3.0
    rail_x = (f.x0 + 4, f.x1 - 4)
    wheels: list[Cylinder] = []
    for x in rail_x:
        for y in (f.y0 + 6, f.y1 - 6):
            wheels.append(
                Cylinder(0, (x * MM, y * MM, (zb - leg - wheel_r) * MM), wheel_r * MM, 1.5 * MM)
            )
    hw.pieces.append(
        Piece(
            "car/wheels",
            "steel",
            "Car wheels",
            "Grooved wheels running on the rails (forum, kiln-hardware.md §6.3 [S24]). No source "
            "gives a studio car's wheel size: drawn to show where they go.",
            cylinders=tuple(wheels),
        )
    )
    face = kiln.door_face
    rail_z = zb - leg - 2 * wheel_r
    run = f.y1 - f.y0
    ys = {"front": (f.y0 - run, f.y1), "back": (f.y0, f.y1 + run)}.get(face, (f.y0, f.y1))
    rails = [_mm(((x - 0.75, ys[0], rail_z - 1.5), (x + 0.75, ys[1], rail_z))) for x in rail_x]
    if face in ("left", "right"):
        hw.findings.append(
            Finding(
                level="info",
                message=(
                    "The car is drawn rolling out of the front or back; a car through a side wall "
                    "is "
                    "drawn with its rails under the kiln only."
                ),
            )
        )
    hw.pieces.append(
        Piece(
            "car/rails",
            "steel",
            "Rails",
            "Two 1½ in angles, apex up, long enough for the car to roll clear of the kiln "
            "(forum and hobby builds, kiln-hardware.md §6.3 [S24] [S25], secondary).",
            boxes=tuple(rails),
        )
    )
    hw.findings.append(
        Finding(
            level="info",
            message=(
                "No source gives a studio car kiln's wheel size, rail size or seal dimensions. The "
                "car "
                "is drawn to show its parts, not sized: size the wheels and rails for the car's "
                "weight."
            ),
            reference="kiln-hardware.md §6.3",
        )
    )


# Burner ports by model: ("round", diameter) or ("rect", width, height), in inches, and the
# burner's body (diameter, length) where a source gives it.
PORTS: dict[str, tuple[tuple[str, float, float], tuple[float, float] | None, str]] = {
    "GACO MR750": (
        ("round", 3.5, 3.5),
        (2.5, 8.0),
        "Ward's port, an inch wider than the 2.5 in head; the same as Robinson's 3½ in "
        "hole for MR-750s (kiln-hardware.md §1.1 [S1] [S30] [S6], derived)",
    ),
    "GACO MR100": (
        ("rect", 4.5, 5.0),
        None,
        "4½ × 5 in, half a brick by two courses, as Pitelka built for MR-100s "
        "(kiln-hardware.md §1.1 [S4] [S5]). The burner's size is not sourced.",
    ),
}
RANSOME = {
    "Ransome B1": (8.5, 1.875),
    "Ransome B2": (10.5, 2.75),
    "Ransome B3": (12.0, 3.25),
    "Ransome B4": (17.0, 3.75),
    "Ransome B5": (21.0, 5.0),
}
for _model, (_length, _end) in RANSOME.items():
    PORTS[_model] = (
        ("round", _end + 1, _end + 1),
        (_end, _length),
        f"Ward's port, an inch wider than the burner's {_end:g} in larger end, taken as the head; "
        "the catalogue doesn't say which end is the head (kiln-hardware.md §1.1, §1.2 [S1] [S9], "
        "derived)",
    )


def _burners(kiln: Kiln, gas: GasDesign, f: Faces, hw: Hardware) -> None:
    b = gas.burners
    if b is None or kiln.heat.gas is None:
        return
    face = kiln.heat.gas.burners.wall
    model = b.model.removeprefix("Ward ")
    spec = PORTS.get(b.model)
    if spec is None:
        hw.findings.append(
            Finding(
                level="warning",
                message=(
                    f"No source gives the port size for {b.model} burners, so the ports aren't "
                    "drawn. "
                    "Ask the burner's maker."
                ),
                reference="kiln-hardware.md §1.4",
            )
        )
        return
    (shape, pw, ph), body, why = spec
    span = f.inside[face]
    for i in range(b.count):
        u = -span / 2 + (i + 0.5) * span / b.count
        z0 = COURSE  # one course above the floor (Pitelka [S4])
        box = f.through(face, (u - pw / 2, u + pw / 2), (z0, z0 + ph))
        axis = Faces.normal_axis(face)
        hw.openings.append(
            Opening(
                f"port/burner-{i + 1}",
                f"Burner port {i + 1}",
                box,
                axis if shape == "round" else None,
            )
        )
        if body is not None:
            dia, length = body
            # ½ in back from the outside of the port (Ward [S1])
            centre = f.point(face, u, z0 + ph / 2, 0.5 + length / 2)
            hw.pieces.append(
                Piece(
                    f"burner/{i + 1}",
                    "burner",
                    f"Burner {i + 1} of {b.count}",
                    f"{model} at {b.pressure}, {b.each}. Port: {why}. Set ½ in back from the "
                    "port (kiln-hardware.md §1.1 [S1]).",
                    cylinders=(Cylinder(axis, centre, dia / 2 * MM, length * MM),),
                )
            )
    hw.findings.append(
        Finding(
            level="info",
            message=(
                "Side-mounted burners need a bag wall so the flames don't hit the ware: hard "
                "brick, "
                "first course solid in front of the burners."
            ),
            reference="kiln-hardware.md §1.3 [S4]",
        )
    )


def _flue_and_chimney(kiln: Kiln, gas: GasDesign, f: Faces, hw: Hardware) -> None:
    area = float(gas.flue_area.split()[0])
    draft = kiln.draft
    if draft is None or draft.type == "up":
        # A flue port in the roof's centre (Pitelka's updrafts [S11]); no chimney is drawn.
        side = math.sqrt(area)
        roof_top = 1e4
        box = _mm(
            (
                (-side / 2, -side / 2, si(kiln.chamber.height, "in") - 1),
                (side / 2, side / 2, roof_top),
            )
        )
        hw.openings.append(Opening("port/flue", "Flue port", box))
        return
    face = draft.flue_wall
    span = f.inside[face]
    courses = 3
    while area / (courses * COURSE) > span - 2 and courses < 8:
        courses += 1
    fh = courses * COURSE
    fw = math.ceil(area / fh * 4) / 4
    hw.openings.append(
        Opening("port/flue", "Flue port", f.through(face, (-fw / 2, fw / 2), (0, fh)))
    )
    if gas.chimney_height is None:
        return
    # The chimney: inside at least the flue's area (Rhodes [S34]), whole half-bricks, hard brick
    # 4½ in thick (Pitelka [S4]), its base `run_to_chimney` out from the flue wall.
    sizes = [4.5 * n for n in range(1, 5)]
    a, b = min(
        ((p, q) for p in sizes for q in sizes if p <= q <= 2 * p and p * q >= area),
        key=lambda pq: (pq[0] * pq[1], pq[1]),
    )
    across, along = b, a  # across the flue wall, and outwards from it
    wall = 4.5
    run = si(draft.run_to_chimney, "in")
    height = float(gas.chimney_height.split("(")[1].split()[0])  # "14.1 ft (169 in) above ..."
    z0, z1 = f.bottom, height
    c0 = run  # the chimney's outside face nearest the kiln, w out from the flue wall
    walls = [
        ("near", (-across / 2 - wall, across / 2 + wall), (c0, c0 + wall)),
        (
            "far",
            (-across / 2 - wall, across / 2 + wall),
            (c0 + wall + along, c0 + 2 * wall + along),
        ),
        ("side-1", (-across / 2 - wall, -across / 2), (c0 + wall, c0 + wall + along)),
        ("side-2", (across / 2, across / 2 + wall), (c0 + wall, c0 + wall + along)),
    ]
    volume = 0.0
    boxes: list[Box] = []
    for _, u, w in walls:
        boxes.append(f.box(face, u, (z0, z1), w))
        volume += (u[1] - u[0]) * (z1 - z0) * (w[1] - w[0])
    title_size = f"{across:g} × {along:g} in inside"
    hw.pieces.append(
        Piece(
            "chimney/stack",
            "dense_firebrick",
            "Chimney",
            f"{title_size}, {height / 12:.1f} ft above the chamber floor, one 4½ in layer of hard "
            "brick laid in fireclay mortar (kiln-hardware.md §3.2 [S4]); inside at least the "
            f"flue's {area:.0f} in² (Rhodes, §3.1 [S34]). Height: {gas.chimney_height}.",
            boxes=tuple(boxes),
            material=CHIMNEY_BRICK,
        )
    )
    if run > 0:
        duct = [
            f.box(face, (-fw / 2 - wall, fw / 2 + wall), (f.bottom, 0), (0, c0 + wall)),
            f.box(face, (-fw / 2 - wall, -fw / 2), (0, fh), (0, c0 + wall)),
            f.box(face, (fw / 2, fw / 2 + wall), (0, fh), (0, c0 + wall)),
            f.box(face, (-fw / 2 - wall, fw / 2 + wall), (fh, fh + wall), (0, c0 + wall)),
        ]
        for lo, hi in duct:
            volume += math.prod(h - lo_ for lo_, h in zip(lo, hi, strict=True)) / MM**3
        hw.pieces.append(
            Piece(
                "chimney/duct",
                "dense_firebrick",
                "Flue duct to the chimney",
                f"{fw:g} × {fh:g} in inside, hard brick, from the flue port to the chimney.",
                boxes=tuple(duct),
                material=CHIMNEY_BRICK,
            )
        )
    hw.openings.append(
        Opening(
            "port/chimney-inlet",
            "Chimney inlet",
            f.box(face, (-fw / 2, fw / 2), (0, fh), (c0 - 1, c0 + wall + 1)),
        )
    )
    # The damper slot: about a foot above the flue, a course high, 3 in wider than the inside
    zd = fh + 12
    hw.openings.append(
        Opening(
            "port/damper",
            "Damper slot",
            f.box(
                face,
                (-across / 2 - 1.5, across / 2 + 1.5),
                (zd, zd + COURSE),
                (c0 + wall + along - 1, c0 + 2 * wall + along + 1),
            ),
        )
    )
    hw.findings.append(
        Finding(
            level="info",
            message=(
                f"Damper: a kiln shelf in a slot {across + 3:g} in wide and one course high, about "
                "a "
                "foot above the top of the flue. Brace the chimney with angle at its corners and "
                "tie it "
                "to the kiln frame."
            ),
            reference="kiln-hardware.md §3.2–3.3 [S4]",
        )
    )
    hw.chimney_bricks = math.ceil(volume / math.prod(BRICK) * 1.05)


def _spy_holes(kiln: Kiln, f: Faces, hw: Hardware, *, electric: bool) -> None:
    face = kiln.door_face
    assert face not in ("floor", "roof")
    h = si(kiln.chamber.height, "in")
    axis = Faces.normal_axis(face)
    if electric:
        # 1 in, full diameter through the brick, three per kiln (L&L Easy-Load [S3] [S6])
        for i, frac in enumerate((0.25, 0.5, 0.75)):
            z = h * frac
            hw.openings.append(
                Opening(
                    f"port/spy-{i + 1}",
                    f"Peephole {i + 1}",
                    f.through(face, (-0.5, 0.5), (z - 0.5, z + 0.5)),
                    axis,
                )
            )
        hw.findings.append(
            Finding(
                level="info",
                message=(
                    "Three 1 in peepholes are cut through the door. Their heights are not sourced; "
                    "they "
                    "are spaced evenly."
                ),
                reference="electric-kiln-hardware.md §4 [S3] [S6]",
            )
        )
        return
    # The top hole about level with the bottom of the arch [S4], or a foot below a flat roof [S13]
    top = h - COURSE if isinstance(kiln.roof, SprungArch) else h - 12
    bottom = min(8.0, top / 3)
    for i, (z, u) in enumerate(((bottom, -3.0), ((bottom + top) / 2, -3.0), (top, 3.0))):
        hw.openings.append(
            Opening(
                f"port/spy-{i + 1}",
                f"Spy hole {i + 1}",
                f.through(face, (u - 1.125, u + 1.125), (z, z + COURSE)),
            )
        )
    hw.findings.append(
        Finding(
            level="info",
            message=(
                "Three spy holes, 2¼ × 2½ in (a quarter brick), in the door: about 8 in above the "
                "floor, midway and near the top, a few inches off centre so they miss the shelf "
                "posts. "
                "Cone packs in the top and bottom, draw rings in the middle."
            ),
            reference="kiln-hardware.md §2 [S4] [S13]",
        )
    )
