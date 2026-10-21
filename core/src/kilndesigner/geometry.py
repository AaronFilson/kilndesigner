"""The kiln as a 3D model (build123d on OpenCascade), exported as STEP and glTF (ADR 0005).

Coordinates are millimetres, with the origin at the centre of the chamber floor: x across the
width, y from the front (negative) to the back, z up. Each layer of each face is its own named
solid, so the viewer can pick a part and show its working:

- the floor runs under the whole kiln;
- the left and right walls stand on the floor and run the full outside depth, closing the corners;
- the back and front (door) walls fit between the left and right walls;
- the roof sits on top of everything.

build123d is imported lazily: it loads OpenCascade, which takes seconds, and the calculations
don't need it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from kilndesigner.model import Face, FlatRoof, Kiln
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
class Part:
    name: str
    material: str
    kind: str
    # an axis-aligned box: min and max corners, mm
    lo: tuple[float, float, float]
    hi: tuple[float, float, float]

    @property
    def volume(self) -> float:
        return (self.hi[0] - self.lo[0]) * (self.hi[1] - self.lo[1]) * (self.hi[2] - self.lo[2])


class GeometryNotSupportedError(NotImplementedError):
    pass


def _thicknesses(kiln: Kiln, face: Face) -> list[tuple[str, float]]:
    layers = kiln.lining.for_face(face, door_face=kiln.door_face)
    return [(layer.material, si(layer.thickness, "mm")) for layer in layers]


def lining_parts(kiln: Kiln) -> list[Part]:
    """The lining as boxes: pure arithmetic, testable without OpenCascade."""
    from kilndesigner.library import material

    if not isinstance(kiln.roof, FlatRoof):
        raise GeometryNotSupportedError("3D models of arched roofs come with the masonry module")
    w, d, h = (si(getattr(kiln.chamber, n), "mm") for n in ("width", "depth", "height"))
    t = {f: sum(x for _, x in _thicknesses(kiln, f)) for f in ("left", "right", "back", "front")}
    x0, x1 = -w / 2 - t["left"], w / 2 + t["right"]
    y0, y1 = -d / 2 - t["front"], d / 2 + t["back"]
    parts: list[Part] = []

    def add(face: str, i: int, mat: str, lo: tuple[float, ...], hi: tuple[float, ...]) -> None:
        name = f"{'door' if face == kiln.door_face else face}/{i + 1}-{mat}"
        kind = material(mat).kind
        parts.append(Part(name, mat, kind, (lo[0], lo[1], lo[2]), (hi[0], hi[1], hi[2])))

    cum = 0.0
    for i, (mat, th) in enumerate(_thicknesses(kiln, "floor")):
        add("floor", i, mat, (x0, y0, -cum - th), (x1, y1, -cum))
        cum += th
    cum = 0.0
    for i, (mat, th) in enumerate(_thicknesses(kiln, "left")):
        add("left", i, mat, (-w / 2 - cum - th, y0, 0), (-w / 2 - cum, y1, h))
        cum += th
    cum = 0.0
    for i, (mat, th) in enumerate(_thicknesses(kiln, "right")):
        add("right", i, mat, (w / 2 + cum, y0, 0), (w / 2 + cum + th, y1, h))
        cum += th
    cum = 0.0
    for i, (mat, th) in enumerate(_thicknesses(kiln, "back")):
        add("back", i, mat, (-w / 2, d / 2 + cum, 0), (w / 2, d / 2 + cum + th, h))
        cum += th
    cum = 0.0
    for i, (mat, th) in enumerate(_thicknesses(kiln, "front")):
        add("front", i, mat, (-w / 2, -d / 2 - cum - th, 0), (w / 2, -d / 2 - cum, h))
        cum += th
    cum = 0.0
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
        solid: Any = Pos(cx, cy, cz) * Box(sx, sy, sz)
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
