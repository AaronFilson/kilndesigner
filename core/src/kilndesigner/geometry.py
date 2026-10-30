"""The kiln as a 3D model (build123d on OpenCascade), exported as STEP and glTF (ADR 0005).

Coordinates are millimetres, with the origin at the centre of the chamber floor: x across the
width, y from the front (negative) to the back, z up. Each layer of each face is its own named
solid, so the viewer can pick a part and show its working:

- the floor runs under the whole kiln;
- the walls stand on the floor and wrap the chamber layer by layer, like an onion: in each ring,
  the left and right walls run through and the back and front (door) fit between them;
- the roof sits on top of everything.

A catenary arch has no side walls: it stands on the floor, and the end walls close it inside its
ends. A dome rests on all four walls, whose tops are filled up to it.

build123d is imported lazily: it loads OpenCascade, which takes seconds, and the calculations
don't need it.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import numpy as np

from kilndesigner.model import CatenaryArch, Dome, Face, Kiln, SprungArch
from kilndesigner.shape import Arch, CatenaryCurve, SailDome
from kilndesigner.units import si
from kilndesigner.working import length_text

if TYPE_CHECKING:
    from build123d import Compound

    from kilndesigner.hardware import Hardware, Opening, Piece
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
    "building_brick": (0.66, 0.31, 0.23),
    "stone": (0.58, 0.57, 0.54),
    "element": (0.55, 0.55, 0.58),
    "steel": (0.30, 0.32, 0.36),
    "burner": (0.72, 0.55, 0.28),
}
KIND_NAMES = {
    "insulating_firebrick": "Insulating firebrick",
    "dense_firebrick": "Hard firebrick",
    "fibre_blanket": "Ceramic fibre blanket",
    "fibre_board": "Ceramic fibre board",
    "insulating_castable": "Insulating castable",
    "dense_castable": "Dense castable",
    "backup_insulation": "Backup insulation",
    "building_brick": "Building brick",
    "stone": "Stone",
    "element": "Elements",
    "steel": "Steel",
    "burner": "Burners",
}
# Materials an arch can spring from: brick, castable and stone, not fibre
SOLID_KINDS = {
    "insulating_firebrick",
    "dense_firebrick",
    "insulating_castable",
    "dense_castable",
    "building_brick",
    "stone",
}
FACE_NAMES = {
    "left": "Left wall",
    "right": "Right wall",
    "back": "Back wall",
    "front": "Front wall",
    "door": "Door",
    "floor": "Floor",
    "roof": "Roof",
    "arch": "Catenary arch",
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
class DomeShape:
    """A layer of a dome: the part of a spherical shell, centred on the kiln's centre line at
    height ``centre_z``, that lies over the part's plan and above the springline (mm). A wall's
    cap under the dome has no thickness: it fills up to the sphere."""

    radius: float
    thickness: float
    centre_z: float

    def heights(self, x: np.ndarray, y: np.ndarray, r: float) -> np.ndarray:
        """The sphere of radius ``r`` over (x, y); -inf where it doesn't reach."""
        under = r * r - x * x - y * y
        return np.where(under > 0, self.centre_z + np.sqrt(np.maximum(under, 0.0)), -np.inf)


@dataclass(frozen=True)
class Part:
    """One layer of one face. A box unless ``arch`` is set; then an arch ring, or (with
    ``cap``) the segment of an end wall that fills the arch above the springline. With
    ``profile``, an outline in the x–z plane run along y: the skewback and fill on a wall top,
    a catenary's ring (``ring``, its thickness), or an end wall closing a catenary. With
    ``dome``, a layer of a dome, or (with ``cap``) a wall's top filled up to it."""

    name: str
    material: str
    kind: str
    # an axis-aligned box, or the bounding box of an arch ring, cap or profile: corners, mm
    lo: tuple[float, float, float]
    hi: tuple[float, float, float]
    arch: ArchShape | None = None
    cap: bool = False
    face: Face | None = None  # the face it belongs to; the name says "door" for the door
    profile: tuple[tuple[float, float], ...] | None = None
    ring: float | None = None
    dome: DomeShape | None = None

    @property
    def wall(self) -> str:
        return self.face if self.face is not None else self.name.split("/")[0]

    @property
    def title(self) -> str:
        """Where the part is, in words: 'Left wall, layer 2 from the inside'."""
        where, rest = self.name.split("/", 1)
        face = FACE_NAMES.get(where, where)
        if rest.startswith("skewback"):
            return f"{face}, the skewback and fill on top"
        number = rest.split("-", 1)[0]
        above = ", above the springline" if self.cap else ""
        return f"{face}, layer {number} from the inside{above}"

    @property
    def length_y(self) -> float:
        return self.hi[1] - self.lo[1]

    @property
    def volume(self) -> float:
        if self.profile is not None:
            pts, nxt = self.profile, self.profile[1:] + self.profile[:1]
            area = abs(sum(x0 * z1 - x1 * z0 for (x0, z0), (x1, z1) in zip(pts, nxt, strict=True)))
            return area / 2 * self.length_y  # the shoelace formula, times the length
        if self.dome is not None:
            return self._dome_volume(self.dome)
        if self.arch is None:
            return (self.hi[0] - self.lo[0]) * (self.hi[1] - self.lo[1]) * (self.hi[2] - self.lo[2])
        if self.cap:
            return self.arch.segment_area * self.length_y
        r, t, a = self.arch.radius, self.arch.thickness, self.arch.half_angle
        return a * ((r + t) ** 2 - r**2) * self.length_y

    def _dome_volume(self, d: DomeShape, n: int = 500) -> float:
        """Between the springline (or the shell's inside) and the sphere, over the part's plan,
        summed on a fine grid (the midpoint rule)."""
        (x0, y0, springline), (x1, y1, _) = self.lo, self.hi
        xs = x0 + (np.arange(n) + 0.5) / n * (x1 - x0)
        ys = y0 + (np.arange(n) + 0.5) / n * (y1 - y0)
        x, y = np.meshgrid(xs, ys)
        top = d.heights(x, y, d.radius + d.thickness)
        bottom = (
            np.full_like(x, springline)
            if self.cap
            else np.maximum(d.heights(x, y, d.radius), springline)
        )
        cell = (x1 - x0) * (y1 - y0) / n / n
        return float(np.sum(np.maximum(top - bottom, 0.0)) * cell)

    @property
    def thickness(self) -> float:
        """Through the layer, the way heat flows (mm)."""
        if self.ring is not None:
            return self.ring
        if self.dome is not None:
            if not self.cap:
                return self.dome.thickness
            return self.length_y if self.wall in ("front", "back") else self.hi[0] - self.lo[0]
        if self.profile is not None:
            return self.length_y if self.wall in ("front", "back") else self.hi[0] - self.lo[0]
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


def not_drawn(kiln: Kiln) -> str | None:
    """Why the lining can't be laid out in brick, planned or priced for this kiln yet, or None.
    The calculations (heat loss, firing, chimney, roof) still run, and the 3D model is drawn as
    shells (massing.py)."""
    c = kiln.chamber
    if c.shape == "round":
        return (
            "round chambers are calculated, counted in brick and priced, and drawn as shells, but "
            "not yet drawn brick by brick or given plans"
        )
    if kiln.roof.type == "open":
        return "an open top is calculated and drawn, but not yet laid out in brick or priced"
    if c.chambers > 1:
        return (
            "chambers in a row are calculated as one long chamber and drawn, but not yet laid out "
            "in brick or priced"
        )
    if c.slope is not None and si(c.slope, "degree") > 0:
        return "a sloping floor is calculated and drawn, but not yet laid out in brick or priced"
    if c.bend is not None and si(c.bend, "degree") > 0:
        return "a bent run is calculated and drawn, but not yet laid out in brick or priced"
    return None


def _thicknesses(kiln: Kiln, face: Face) -> list[tuple[str, float]]:
    layers = kiln.lining.for_face(face, door_face=kiln.door_face)
    return [(layer.material, si(layer.thickness, "mm")) for layer in layers]


def lining_parts(kiln: Kiln) -> list[Part]:
    """The lining as boxes and arch rings: pure arithmetic, testable without OpenCascade."""
    from kilndesigner.castable import resolve_material

    if (why := not_drawn(kiln)) is not None:
        raise GeometryNotSupportedError(why)
    if isinstance(kiln.roof, CatenaryArch):
        return _catenary_parts(kiln)
    w, d, h = (si(getattr(kiln.chamber, n), "mm") for n in ("width", "depth", "height"))
    walls = ("left", "right", "back", "front")
    layers = {f: _thicknesses(kiln, f) for f in walls}
    t = {f: sum(x for _, x in layers[f]) for f in walls}
    x0, x1 = -w / 2 - t["left"], w / 2 + t["right"]
    y0, y1 = -d / 2 - t["front"], d / 2 + t["back"]
    parts: list[Part] = []

    def add(face: Face, i: int, mat: str, lo: tuple[float, ...], hi: tuple[float, ...]) -> None:
        name = f"{'door' if face == kiln.door_face else face}/{i + 1}-{mat}"
        kind = resolve_material(kiln, mat).kind
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
                        name, mat, resolve_material(kiln, mat).kind,
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
                    f"roof/{i + 1}-{mat}",
                    mat,
                    resolve_material(kiln, mat).kind,
                    lo,
                    hi,
                    arch=shape,
                    face="roof",
                )
            )
            cum += th
        parts += _skewbacks(kiln, arch, centre_z, cum, (y0, y1), layers)
        return parts
    if isinstance(kiln.roof, Dome):
        return parts + _dome_parts(kiln, parts, (x0, x1, y0, y1))
    for i, (mat, th) in enumerate(_thicknesses(kiln, "roof")):
        add("roof", i, mat, (x0, y0, h + cum), (x1, y1, h + cum + th))
        cum += th
    return parts


def _catenary_parts(kiln: Kiln) -> list[Part]:
    """A catenary arch from the floor (combustion-and-masonry.md §6.6): the floor under it all,
    the arch's rings standing on the floor and running from the outside of the back wall to the
    outside of the front, and the end walls closing it inside its ends. Each ring is the inside
    curve moved out by the layers inside it."""
    from kilndesigner.castable import resolve_material

    w, d, h = (si(getattr(kiln.chamber, n), "mm") for n in ("width", "depth", "height"))
    curve = CatenaryCurve(w, h)
    rings = _thicknesses(kiln, "roof")
    ends = {f: _thicknesses(kiln, f) for f in ("front", "back")}
    y0 = -d / 2 - sum(t for _, t in ends["front"])
    y1 = d / 2 + sum(t for _, t in ends["back"])
    reach = curve.half_width(sum(t for _, t in rings))
    parts: list[Part] = []

    def kind(mat: str) -> str:
        return resolve_material(kiln, mat).kind

    cum = 0.0
    for i, (mat, th) in enumerate(_thicknesses(kiln, "floor")):
        lo, hi = (-reach, y0, -cum - th), (reach, y1, -cum)
        parts.append(Part(f"floor/{i + 1}-{mat}", mat, kind(mat), lo, hi, face="floor"))
        cum += th
    inside = tuple(curve.offset(0.0))
    sides: tuple[tuple[Face, int], ...] = (("back", 1), ("front", -1))
    for face, sign in sides:
        reached = 0.0
        for i, (mat, th) in enumerate(ends[face]):
            ys = sorted((sign * (d / 2 + reached), sign * (d / 2 + reached + th)))
            name = f"{'door' if face == kiln.door_face else face}/{i + 1}-{mat}"
            lo, hi = (-w / 2, ys[0], 0.0), (w / 2, ys[1], h)
            parts.append(Part(name, mat, kind(mat), lo, hi, face=face, profile=inside))
            reached += th
    cum = 0.0
    for i, (mat, th) in enumerate(rings):
        outline = (*curve.offset(cum), *reversed(curve.offset(cum + th)))
        half = curve.half_width(cum + th)
        parts.append(
            Part(
                f"arch/{i + 1}-{mat}", mat, kind(mat), (-half, y0, 0.0), (half, y1, h + cum + th),
                face="roof", profile=outline, ring=th,
            )
        )  # fmt: skip
        cum += th
    return parts


def _dome_parts(
    kiln: Kiln, walls: list[Part], plan: tuple[float, float, float, float]
) -> list[Part]:
    """A dome on the walls (combustion-and-masonry.md §6.7): each wall's top filled up to the
    sphere, and the dome's layers over the whole kiln, the first resting on that fill."""
    from kilndesigner.castable import resolve_material

    assert isinstance(kiln.roof, Dome)
    w, d, h = (si(getattr(kiln.chamber, n), "mm") for n in ("width", "depth", "height"))
    dome = SailDome(w, d, si(kiln.roof.rise, "mm"))
    centre, r = h + dome.centre, dome.radius
    parts: list[Part] = []
    for wall in walls:
        if wall.face not in ("left", "right", "front", "back"):
            continue
        # The dome stands highest over the point of the wall's plan nearest the centre line
        near_x = min(max(0.0, wall.lo[0]), wall.hi[0])
        near_y = min(max(0.0, wall.lo[1]), wall.hi[1])
        if r * r <= near_x**2 + near_y**2:
            continue
        top = centre + math.sqrt(r * r - near_x**2 - near_y**2)
        if top <= h + 1e-6:
            continue
        parts.append(
            Part(
                f"{wall.name}-dome", wall.material, wall.kind, (wall.lo[0], wall.lo[1], h),
                (wall.hi[0], wall.hi[1], top), cap=True, face=wall.face,
                dome=DomeShape(r, 0.0, centre),
            )
        )  # fmt: skip
    x0, x1, y0, y1 = plan
    cum = 0.0
    for i, (mat, th) in enumerate(_thicknesses(kiln, "roof")):
        parts.append(
            Part(
                f"roof/{i + 1}-{mat}", mat, resolve_material(kiln, mat).kind, (x0, y0, h),
                (x1, y1, centre + r + cum + th), face="roof", dome=DomeShape(r + cum, th, centre),
            )
        )  # fmt: skip
        cum += th
    return parts


def inside_top(kiln: Kiln, face: Face, u: float) -> float:
    """How high a wall's inside face reaches at ``u`` along it (mm, from the floor): the
    springline, or the curve where an arch or dome meets it. A catenary has no side walls."""
    w, d, h = (si(getattr(kiln.chamber, n), "mm") for n in ("width", "depth", "height"))
    end = face in ("front", "back")
    if isinstance(kiln.roof, CatenaryArch):
        return CatenaryCurve(w, h).z(u) if end and abs(u) < w / 2 else 0.0
    if isinstance(kiln.roof, SprungArch) and end and abs(u) < w / 2:
        arch = Arch(w, si(kiln.roof.rise, "mm"))
        return h + arch.rise - arch.radius + math.sqrt(arch.radius**2 - u**2)
    if isinstance(kiln.roof, Dome) and abs(u) < (w if end else d) / 2:
        dome = SailDome(w, d, si(kiln.roof.rise, "mm"))
        off = d / 2 if end else w / 2  # the wall's distance from the centre line
        return h + max(0.0, dome.centre + math.sqrt(dome.radius**2 - off**2 - u**2))
    return h


def _skewbacks(
    kiln: Kiln,
    arch: Arch,
    centre_z: float,
    roof_thickness: float,
    ys: tuple[float, float],
    layers: Mapping[str, list[tuple[str, float]]],
) -> list[Part]:
    """The skewback and fill on each side wall: what the arch springs from, out to the wall's
    outer face. Its inner face lies along the arch's radius at the springline, so it takes the
    arch's thrust square on (combustion-and-masonry.md §6.5). It's built of the wall's main
    (thickest) brick or castable and runs the kiln's full length."""
    from kilndesigner.castable import resolve_material

    w, h = si(kiln.chamber.width, "mm"), si(kiln.chamber.height, "mm")
    r_out = arch.radius + roof_thickness
    a = arch.half_angle
    parts: list[Part] = []
    sides: tuple[tuple[Face, int], ...] = (("left", -1), ("right", 1))
    for side, sign in sides:
        wall = layers[side]
        solid = [layer for layer in wall if resolve_material(kiln, layer[0]).kind in SOLID_KINDS]
        if not solid:
            continue  # nothing to spring an arch from
        outer = w / 2 + sum(t for _, t in wall)
        top = (r_out * math.sin(a), centre_z + r_out * math.cos(a))  # the arch's outer corner
        if top[0] <= outer:
            outline = [(w / 2, h), top, (outer, top[1]), (outer, h)]
        else:  # the arch reaches past the wall: the fill ends where the radius leaves it
            r = outer / math.sin(a)
            outline = [(w / 2, h), (outer, centre_z + r * math.cos(a)), (outer, h)]
        profile = tuple((sign * x, z) for x, z in outline)
        mat = max(solid, key=lambda layer: layer[1])[0]
        xs, zs = [x for x, _ in profile], [z for _, z in profile]
        parts.append(
            Part(
                f"{side}/skewback-{mat}",
                mat,
                resolve_material(kiln, mat).kind,
                (min(xs), ys[0], min(zs)),
                (max(xs), ys[1], max(zs)),
                face=side,
                profile=profile,
            )
        )
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
    outline = part.profile if part.profile is not None else arch_outline(part)
    solid: Any = extrude(Plane.XZ * Polygon(*outline, align=None), amount=part.length_y)
    return Pos(0, part.lo[1] - solid.bounding_box().min.Y, 0) * solid


def _dome_solid(part: Part) -> Any:
    """A dome layer: the shell between two spheres, over the part's plan, above the springline.
    A wall's cap: its plan, from the springline up to the sphere."""
    from build123d import Pos, Sphere

    assert part.dome is not None
    d = part.dome
    plan = _box(part.lo, (part.hi[0], part.hi[1], part.hi[2] + 1))
    solid: Any = plan & (Pos(0, 0, d.centre_z) * Sphere(d.radius + d.thickness))
    if not part.cap:
        solid = solid - Pos(0, 0, d.centre_z) * Sphere(d.radius)
    return solid


def _box(lo: tuple[float, ...], hi: tuple[float, ...]) -> Any:
    from build123d import Box, Pos

    sx, sy, sz = (b - a for a, b in zip(lo, hi, strict=True))
    cx, cy, cz = ((a + b) / 2 for a, b in zip(lo, hi, strict=True))
    return Pos(cx, cy, cz) * Box(sx, sy, sz)


def _cylinder(axis: int, centre: tuple[float, float, float], radius: float, length: float) -> Any:
    from build123d import Cylinder, Pos, Rot

    turn = {0: Rot(0, 90, 0), 1: Rot(90, 0, 0), 2: Rot(0, 0, 0)}[axis]
    return Pos(*centre) * turn * Cylinder(radius, length)


def _opening_solid(o: Opening) -> Any:
    lo, hi = o.box
    if o.round_axis is None:
        return _box(lo, hi)
    centre = ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2)
    across = [hi[i] - lo[i] for i in range(3) if i != o.round_axis]
    return _cylinder(o.round_axis, centre, min(across) / 2, hi[o.round_axis] - lo[o.round_axis])


def piece_solid(p: Piece) -> Any:
    from build123d import Compound

    solids = [_box(lo, hi) for lo, hi in p.boxes]
    solids += [_cylinder(c.axis, c.centre, c.radius, c.length) for c in p.cylinders]
    return solids[0] if len(solids) == 1 else Compound(children=solids)


def _overlaps(solid: Any, lo: tuple[float, ...], hi: tuple[float, ...]) -> bool:
    bb = solid.bounding_box()
    return (
        hi[0] > bb.min.X and lo[0] < bb.max.X and hi[1] > bb.min.Y and lo[1] < bb.max.Y
        and hi[2] > bb.min.Z and lo[2] < bb.max.Z
    )  # fmt: skip


def _cut(solid: Any, holes: list[tuple[Opening, Any]]) -> Any:
    for opening, hole in holes:
        if _overlaps(solid, *opening.box):
            solid = solid - hole
    return solid


def build_model(
    kiln: Kiln, elements: list[ElementRun] | None = None, hardware: Hardware | None = None
) -> Compound:
    from build123d import Circle, Color, Compound, Plane, Polyline, Transition, sweep

    holes = [(o, _opening_solid(o)) for o in (hardware.openings if hardware else [])]
    children: list[Any] = []
    for part in lining_parts(kiln):
        boxed = part.arch is None and part.profile is None and part.dome is None
        if boxed and any(b - a < 1e-6 for a, b in zip(part.lo, part.hi, strict=True)):
            continue  # a wall with no height: an arch springing from the floor (a groundhog)
        solid: Any = (
            _box(part.lo, part.hi)
            if boxed
            else _dome_solid(part)
            if part.dome is not None
            else _arch_solid(part)
        )
        solid = _cut(solid, holes)
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
    for piece in hardware.pieces if hardware else []:
        solid = piece_solid(piece)
        if piece.kind != "burner" and not piece.name.startswith("frame/"):
            solid = _cut(solid, holes)
        solid.label = piece.name
        solid.color = Color(*COLOURS.get(piece.kind, (0.8, 0.8, 0.8)))
        children.append(solid)
    model = Compound(children=children)
    model.label = kiln.name
    return model


def colour(kind: str) -> str:
    r, g, b = COLOURS.get(kind, (0.8, 0.8, 0.8))
    return f"#{round(r * 255):02x}{round(g * 255):02x}{round(b * 255):02x}"


def part_index(
    kiln: Kiln, report: Report, hardware: Hardware | None = None
) -> dict[str, dict[str, str]]:
    """What each named part of the model is, for the viewer: a title, a line of detail, and what
    it's made of (``kind``, with its ``colour`` in the model, for the legend)."""
    from kilndesigner.castable import resolve_material

    us = kiln.units == "us"
    index: dict[str, dict[str, str]] = {}

    def entry(title: str, detail: str, kind: str) -> dict[str, str]:
        return {"title": title, "detail": detail, "kind": KIND_NAMES.get(kind, kind),
                "colour": colour(kind)}  # fmt: skip

    for p in lining_parts(kiln):
        detail = resolve_material(kiln, p.material).name
        skewback = p.profile is not None and p.wall in ("left", "right")
        if not skewback and not p.cap:
            detail += f", {length_text(p.thickness, us)} thick"
        index[p.name] = entry(p.title, detail, p.kind)
    electric = report.electric
    if electric is not None and electric.elements is not None:
        el = electric.elements
        # The model draws one coil a groove; an element may run several grooves, in turn
        per = max(1, el.groove_rows // max(1, el.count))
        for row in range(max(el.groove_rows, el.count)):
            i, groove = divmod(row, per)
            index[f"element/{row + 1}"] = entry(
                f"Element {min(i, el.count - 1) + 1} of {el.count}"
                + (f", groove {groove + 1} of {per}" if per > 1 else ""),
                f"{el.gauge} {electric.alloy}, {el.length_each} of wire, {el.power_each}",
                "element",
            )
    for piece in hardware.pieces if hardware else []:
        index[piece.name] = entry(piece.title, piece.detail, piece.kind)
    return index


def write_model(kiln: Kiln, report: Report, out_dir: Path) -> dict[str, Path]:
    """Build the kiln with its elements, frame, door, ports and chimney, export it, and write
    what each part is and where its ports are."""
    from kilndesigner.hardware import build_hardware, layout

    if not_drawn(kiln) is not None:
        return _write_massing(kiln, report, out_dir)
    runs: list[ElementRun] = []
    if report.electric is not None and report.electric.elements is not None:
        el = report.electric.elements
        runs = element_runs(kiln, el.groove_rows, el.coil_outside_diameter_mm)
    hardware = build_hardware(kiln, report.frame, report.gas, report.fire)
    written = export_model(build_model(kiln, runs, hardware), out_dir)
    parts = out_dir / "parts.json"
    index = part_index(kiln, report, hardware)
    parts.write_text(json.dumps(index, ensure_ascii=False, indent=2), "utf-8")
    places = out_dir / LAYOUT
    places.write_text(json.dumps(layout(kiln, hardware), ensure_ascii=False, indent=2), "utf-8")
    return {**written, "parts": parts, "layout": places}


def _write_massing(kiln: Kiln, report: Report, out_dir: Path) -> dict[str, Path]:
    """The model of a kiln whose bricks aren't laid out yet: its lining as shells."""
    from kilndesigner.hardware import build_hardware
    from kilndesigner.massing import MassingError, build_massing, massing_index, massing_layout

    hardware = build_hardware(kiln, report.frame, report.gas, report.fire)
    try:
        model = build_massing(kiln, hardware)
    except MassingError as e:
        raise GeometryNotSupportedError(str(e)) from e
    written = export_model(model, out_dir)
    parts = out_dir / "parts.json"
    parts.write_text(
        json.dumps(massing_index(kiln, hardware), ensure_ascii=False, indent=2), "utf-8"
    )
    places = out_dir / LAYOUT
    places.write_text(
        json.dumps(massing_layout(kiln, hardware), ensure_ascii=False, indent=2), "utf-8"
    )
    return {**written, "parts": parts, "layout": places}


LAYOUT = "layout.json"
"""The file in a build with each wall's frame and each port's place (hardware.layout)."""


def export_model(model: Compound, out_dir: Path, stem: str = "kiln") -> dict[str, Path]:
    from build123d import export_gltf, export_step

    out_dir.mkdir(parents=True, exist_ok=True)
    step, glb = out_dir / f"{stem}.step", out_dir / f"{stem}.glb"
    export_step(model, str(step))
    export_gltf(model, str(glb), binary=True)
    return {"step": step, "gltf": glb}
