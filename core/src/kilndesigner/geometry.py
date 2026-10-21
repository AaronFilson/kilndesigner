"""The kiln as a 3D model (build123d on OpenCascade), exported as STEP and glTF (ADR 0005).

Coordinates are millimetres, with the origin at the centre of the chamber floor: x across the
width, y from the front (negative) to the back, z up. Each layer of each face is its own named
solid, so the viewer can pick a part and show its working:

- the floor runs under the whole kiln;
- the walls stand on the floor and wrap the chamber layer by layer, like an onion: in each ring,
  the left and right walls run through and the back and front (door) fit between them;
- the roof sits on top of everything.

build123d is imported lazily: it loads OpenCascade, which takes seconds, and the calculations
don't need it.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from kilndesigner.model import Face, Kiln, SprungArch
from kilndesigner.shape import Arch
from kilndesigner.units import si

if TYPE_CHECKING:
    from build123d import Compound

    from kilndesigner.report import Report

# Display colours by material kind (RGB, 0–1)
COLOURS: dict[str, tuple[float, float, float]] = {
    "insulating_firebrick": (0.93, 0.89, 0.78),
    "dense_firebrick": (0.72, 0.45, 0.30),
    "fibre_blanket": (0.98, 0.98, 0.95),
    "fibre_board": (0.95, 0.95, 0.92),
    "insulating_castable": (0.80, 0.78, 0.74),
    "dense_castable": (0.62, 0.60, 0.58),
    "backup_insulation": (0.85, 0.85, 0.90),
    "element": (0.55, 0.55, 0.58),
}


@dataclass(frozen=True)
class ArchShape:
    """A circular arch running along y: its inner radius, thickness and centre, mm and radians.

    The arch spans the chamber between angles 90° ± ``half_angle`` about its centre, which sits
    on the kiln's centre line at height ``centre_z``.
    """

    radius: float
    thickness: float
    centre_z: float
    half_angle: float

    @property
    def segment_area(self) -> float:
        """The area between the inner circle and its chord at the springline (mm²)."""
        r, a = self.radius, self.half_angle
        return r * r * a - r * r * math.sin(a) * math.cos(a)


@dataclass(frozen=True)
class Part:
    """One layer of one face. A box unless ``arch`` is set; then an arch ring, or (with
    ``cap``) the segment of an end wall that fills the arch above the springline."""

    name: str
    material: str
    kind: str
    # an axis-aligned box, or the bounding box of an arch ring or cap: min and max corners, mm
    lo: tuple[float, float, float]
    hi: tuple[float, float, float]
    arch: ArchShape | None = None
    cap: bool = False
    face: Face | None = None  # the face it belongs to; the name says "door" for the door

    @property
    def wall(self) -> str:
        return self.face if self.face is not None else self.name.split("/")[0]

    @property
    def length_y(self) -> float:
        return self.hi[1] - self.lo[1]

    @property
    def volume(self) -> float:
        if self.arch is None:
            return (self.hi[0] - self.lo[0]) * (self.hi[1] - self.lo[1]) * (self.hi[2] - self.lo[2])
        if self.cap:
            return self.arch.segment_area * self.length_y
        r, t, a = self.arch.radius, self.arch.thickness, self.arch.half_angle
        return a * ((r + t) ** 2 - r**2) * self.length_y

    @property
    def thickness(self) -> float:
        """Through the layer, the way heat flows (mm)."""
        if self.arch is not None:
            return self.length_y if self.cap else self.arch.thickness
        dx, dy, dz = (b - a for a, b in zip(self.lo, self.hi, strict=True))
        face = self.wall
        if face in ("floor", "roof"):
            return dz
        if face in ("left", "right"):
            return dx
        return dy

    @property
    def area(self) -> float:
        """The layer's area across the heat flow, at its mid-thickness (mm²)."""
        return self.volume / self.thickness


class GeometryNotSupportedError(NotImplementedError):
    pass


def _thicknesses(kiln: Kiln, face: Face) -> list[tuple[str, float]]:
    layers = kiln.lining.for_face(face, door_face=kiln.door_face)
    return [(layer.material, si(layer.thickness, "mm")) for layer in layers]


def lining_parts(kiln: Kiln) -> list[Part]:
    """The lining as boxes and arch rings: pure arithmetic, testable without OpenCascade."""
    from kilndesigner.library import material

    w, d, h = (si(getattr(kiln.chamber, n), "mm") for n in ("width", "depth", "height"))
    walls = ("left", "right", "back", "front")
    layers = {f: _thicknesses(kiln, f) for f in walls}
    t = {f: sum(x for _, x in layers[f]) for f in walls}
    x0, x1 = -w / 2 - t["left"], w / 2 + t["right"]
    y0, y1 = -d / 2 - t["front"], d / 2 + t["back"]
    parts: list[Part] = []

    def add(face: Face, i: int, mat: str, lo: tuple[float, ...], hi: tuple[float, ...]) -> None:
        name = f"{'door' if face == kiln.door_face else face}/{i + 1}-{mat}"
        kind = material(mat).kind
        parts.append(Part(name, mat, kind, (lo[0], lo[1], lo[2]), (hi[0], hi[1], hi[2]), face=face))

    def reach(face: str, i: int) -> float:
        """How far the face's layers 1..i reach out from the chamber (mm)."""
        return sum(x for _, x in layers[face][:i])

    cum = 0.0
    for i, (mat, th) in enumerate(_thicknesses(kiln, "floor")):
        add("floor", i, mat, (x0, y0, -cum - th), (x1, y1, -cum))
        cum += th
    # The walls wrap the chamber like an onion: each ring of layer i sits around ring i - 1.
    # The side walls' layer i runs the depth of ring i; the back and door fit between the side
    # walls' layer i - 1. So brick meets brick at the corners, and blanket meets blanket.
    for i in range(max(len(v) for v in layers.values())):
        left_in, left_out = reach("left", i), reach("left", i + 1)
        right_in, right_out = reach("right", i), reach("right", i + 1)
        front_in, front_out = reach("front", i), reach("front", i + 1)
        back_in, back_out = reach("back", i), reach("back", i + 1)
        ring_y = (-d / 2 - front_out, d / 2 + back_out)
        ring_x = (-w / 2 - left_in, w / 2 + right_in)
        if i < len(layers["left"]):
            mat = layers["left"][i][0]
            add("left", i, mat, (-w / 2 - left_out, ring_y[0], 0), (-w / 2 - left_in, ring_y[1], h))
        if i < len(layers["right"]):
            mat = layers["right"][i][0]
            add(
                "right", i, mat, (w / 2 + right_in, ring_y[0], 0), (w / 2 + right_out, ring_y[1], h)
            )
        if i < len(layers["back"]):
            mat = layers["back"][i][0]
            add("back", i, mat, (ring_x[0], d / 2 + back_in, 0), (ring_x[1], d / 2 + back_out, h))
        if i < len(layers["front"]):
            mat = layers["front"][i][0]
            add(
                "front",
                i,
                mat,
                (ring_x[0], -d / 2 - front_out, 0),
                (ring_x[1], -d / 2 - front_in, h),
            )
    cum = 0.0
    if isinstance(kiln.roof, SprungArch):
        arch = Arch(w, si(kiln.roof.rise, "mm"))
        centre_z = h + arch.rise - arch.radius
        # The end walls close the arch: each end-wall layer gets a cap above the springline.
        ends: tuple[tuple[Face, int], ...] = (("back", 1), ("front", -1))
        for face, sign in ends:
            reached = 0.0
            for i, (mat, th) in enumerate(layers[face]):
                ys = sorted((sign * (d / 2 + reached), sign * (d / 2 + reached + th)))
                shape = ArchShape(arch.radius, 0.0, centre_z, arch.half_angle)
                name = f"{'door' if face == kiln.door_face else face}/{i + 1}-{mat}-arch"
                parts.append(
                    Part(
                        name, mat, material(mat).kind,
                        (-w / 2, ys[0], h), (w / 2, ys[1], h + arch.rise),
                        arch=shape, cap=True, face=face,
                    )
                )  # fmt: skip
                reached += th
        for i, (mat, th) in enumerate(_thicknesses(kiln, "roof")):
            r_in = arch.radius + cum
            shape = ArchShape(r_in, th, centre_z, arch.half_angle)
            half_width = (r_in + th) * math.sin(arch.half_angle)
            lo = (-half_width, y0, h)
            hi = (half_width, y1, centre_z + r_in + th)
            parts.append(
                Part(
                    f"roof/{i + 1}-{mat}", mat, material(mat).kind, lo, hi, arch=shape, face="roof"
                )
            )
            cum += th
        return parts
    for i, (mat, th) in enumerate(_thicknesses(kiln, "roof")):
        add("roof", i, mat, (x0, y0, h + cum), (x1, y1, h + cum + th))
        cum += th
    return parts


@dataclass(frozen=True)
class ElementRun:
    """One element's groove: a coil of ``diameter`` along ``path`` (mm points)."""

    name: str
    diameter: float
    path: tuple[tuple[float, float, float], ...]


def element_runs(kiln: Kiln, rows: int, coil_diameter_mm: float) -> list[ElementRun]:
    """Element coils centred on the inside face of the element walls, one per row."""
    electric = kiln.heat.electric
    if electric is None or rows == 0:
        return []
    w, d, h = (si(getattr(kiln.chamber, n), "mm") for n in ("width", "depth", "height"))
    corners = {
        "front": ((w / 2, -d / 2), (-w / 2, -d / 2)),
        "left": ((-w / 2, -d / 2), (-w / 2, d / 2)),
        "back": ((-w / 2, d / 2), (w / 2, d / 2)),
        "right": ((w / 2, d / 2), (w / 2, -d / 2)),
    }
    order = [wall for wall in ("front", "left", "back", "right") if wall in electric.walls]
    runs: list[ElementRun] = []
    for row in range(rows):
        z = h * (row + 0.5) / rows
        points: list[tuple[float, float, float]] = []
        for wall in order:
            for x, y in corners[wall]:
                if not points or points[-1][:2] != (x, y):
                    points.append((x, y, z))
        runs.append(ElementRun(f"element/{row + 1}", coil_diameter_mm, tuple(points)))
    return runs


def arch_outline(part: Part, steps: int = 48) -> list[tuple[float, float]]:
    """The arch ring or cap as a closed outline in the x–z plane (mm)."""
    assert part.arch is not None
    a = part.arch
    angles = [math.pi / 2 + a.half_angle - 2 * a.half_angle * i / steps for i in range(steps + 1)]
    inner = [(a.radius * math.cos(t), a.centre_z + a.radius * math.sin(t)) for t in angles]
    if part.cap:
        return inner  # the chord closes it
    r_out = a.radius + a.thickness
    outer = [(r_out * math.cos(t), a.centre_z + r_out * math.sin(t)) for t in reversed(angles)]
    return inner + outer


def _arch_solid(part: Part) -> Any:
    from build123d import Plane, Polygon, Pos, extrude

    # Extrude the outline from the x–z plane, then move it so it starts at the part's y.
    solid: Any = extrude(Plane.XZ * Polygon(*arch_outline(part), align=None), amount=part.length_y)
    return Pos(0, part.lo[1] - solid.bounding_box().min.Y, 0) * solid


def build_model(kiln: Kiln, elements: list[ElementRun] | None = None) -> Compound:
    from build123d import (
        Box,
        Circle,
        Color,
        Compound,
        Plane,
        Polyline,
        Pos,
        Transition,
        sweep,
    )

    children: list[Any] = []
    for part in lining_parts(kiln):
        sx, sy, sz = (b - a for a, b in zip(part.lo, part.hi, strict=True))
        cx, cy, cz = ((a + b) / 2 for a, b in zip(part.lo, part.hi, strict=True))
        solid: Any = Pos(cx, cy, cz) * Box(sx, sy, sz) if part.arch is None else _arch_solid(part)
        solid.label = part.name
        solid.color = Color(*COLOURS.get(part.kind, (0.8, 0.8, 0.8)))
        children.append(solid)
    for run in elements or []:
        path = Polyline(*run.path)
        start, tangent = path.position_at(0), path.tangent_at(0)
        profile = Plane(origin=start, z_dir=tangent) * Circle(run.diameter / 2)
        coil: Any = sweep(profile, path=path, transition=Transition.RIGHT)
        coil.label = run.name
        coil.color = Color(*COLOURS["element"])
        children.append(coil)
    model = Compound(children=children)
    model.label = kiln.name
    return model


def write_model(kiln: Kiln, report: Report, out_dir: Path) -> dict[str, Path]:
    """Build the kiln with its elements (if any) and export it."""
    runs: list[ElementRun] = []
    if report.electric is not None and report.electric.elements is not None:
        el = report.electric.elements
        runs = element_runs(kiln, el.count, el.coil_outside_diameter_mm)
    return export_model(build_model(kiln, runs), out_dir)


def export_model(model: Compound, out_dir: Path, stem: str = "kiln") -> dict[str, Path]:
    from build123d import export_gltf, export_step

    out_dir.mkdir(parents=True, exist_ok=True)
    step, glb = out_dir / f"{stem}.step", out_dir / f"{stem}.glb"
    export_step(model, str(step))
    export_gltf(model, str(glb), binary=True)
    return {"step": step, "gltf": glb}
