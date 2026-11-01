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

from kilndesigner.groin import GroinLayer
from kilndesigner.model import (
    CatenaryArch,
    Dome,
    Face,
    FlatRoof,
    Kiln,
    OpenTop,
    SprungArch,
    arches_along,
)
from kilndesigner.outline import Revolved, shell_profile
from kilndesigner.rings import FLOOR_COURSE_IN, IN
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
    "earth": (0.55, 0.45, 0.33),
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
    "earth": "Clay, straw and earth",
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
    "earth",
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
    "wall": "Round wall",
    "walls": "Walls",
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
    centre_y: float = 0.0  # a chamber's in a row, along the run

    def heights(self, x: np.ndarray, y: np.ndarray, r: float) -> np.ndarray:
        """The sphere of radius ``r`` over (x, y); -inf where it doesn't reach."""
        y = y - self.centre_y
        under = r * r - x * x - y * y
        return np.where(under > 0, self.centre_z + np.sqrt(np.maximum(under, 0.0)), -np.inf)


type PlanPoints = tuple[tuple[float, float], ...]
"""A closed outline in plan, as points (mm)."""


def _shoelace(pts: tuple[tuple[float, float], ...]) -> float:
    nxt = pts[1:] + pts[:1]
    return abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, nxt, strict=True))) / 2


def _inside(pts: tuple[tuple[float, float], ...], x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Which of the points (x, y) lie inside the polygon: the even–odd rule, a ray along +x."""
    out = np.zeros(x.shape, dtype=bool)
    for (xa, ya), (xb, yb) in zip(pts, pts[1:] + pts[:1], strict=True):
        if ya == yb:
            continue
        crosses = (ya > y) != (yb > y)
        at = xa + (y - ya) * (xb - xa) / (yb - ya)
        out ^= crosses & (x < at)
    return out


def polygon_fraction(sides: int) -> float:
    """A regular polygon's area over its circumscribed circle's: N·sin(2π/N)/(2π)."""
    return sides * math.sin(2 * math.pi / sides) / (2 * math.pi)


def polygon_reach(sides: int, angle: float) -> float:
    """How far a regular polygon, corners at radius 1 and a flat facing the front (−y), reaches
    from its centre in the direction ``angle`` (radians from +x): cos(π/N) / cos(θ − φ), φ the
    nearest flat's outward normal."""
    step = 2 * math.pi / sides
    k = round((angle + math.pi / 2) / step)
    return math.cos(math.pi / sides) / math.cos(angle - (-math.pi / 2 + k * step))


def polygon_corners(sides: int, radius: float) -> list[tuple[float, float]]:
    """A regular polygon's corners, ``radius`` out, a flat facing the front (−y), anticlockwise."""
    return [
        (
            radius * math.cos(-math.pi / 2 + (2 * k + 1) * math.pi / sides),
            radius * math.sin(-math.pi / 2 + (2 * k + 1) * math.pi / sides),
        )
        for k in range(sides)
    ]


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
    # An outline in the r–z plane (r ≥ 0, mm), turned about the z axis: a round wall's layer, a
    # disc of floor or roof, a layer of a round dome. ``ring`` is then its thickness.
    revolve: tuple[tuple[float, float], ...] | None = None
    # With ``revolve``: a faceted round kiln's regular polygon of this many sides, a flat at the
    # front, rather than a circle; the outline's r is then out to the polygon's corners
    sides: int | None = None
    # A ``profile`` in the y–z plane, (y, z) pairs, run along x: an arch spanning along the
    # draft, its skewbacks, and the side walls' caps closing it (chambers in a row)
    across: bool = False
    chamber: int | None = None  # which chamber in a row it belongs to, from 1
    # A single chamber on a slope is laid out level, then tilted up the slope (radians) about the
    # x axis through the foot of its front face, at y = ``pivot``: its courses follow the floor
    tilt: float = 0.0
    pivot: float = 0.0
    # A curved plan's layer (chamber.outline): an outline in plan (x, y, mm, anticlockwise),
    # less ``inner`` for a wall's ring, from lo z to hi z; with ``dome``, up to the dome's sphere
    # (a wall's cap) or between its spheres (a layer of the dome) over it. ``ring`` is then its
    # thickness.
    plan: tuple[tuple[float, float], ...] | None = None
    inner: tuple[tuple[float, float], ...] | None = None
    # Crossing vaults' layer above the springline (roof.crossing, groin.py): a ring of both
    # vaults with the groin cut out, or an end wall's cap; lo–hi its plan. ``ring`` its thickness
    groin: GroinLayer | None = None

    def tilted(self, y: float, z: float) -> tuple[float, float]:
        """Where a point (y, z) of the part, laid out level, stands on the slope."""
        if not self.tilt:
            return y, z
        dy, c, s = y - self.pivot, math.cos(self.tilt), math.sin(self.tilt)
        return self.pivot + dy * c - z * s, dy * s + z * c

    @property
    def wall(self) -> str:
        return self.face if self.face is not None else self.name.split("/")[0]

    @property
    def is_skewback(self) -> bool:
        return self.name.split("/", 1)[1].startswith("skewback")

    @property
    def title(self) -> str:
        """Where the part is, in words: 'Left wall, layer 2 from the inside'."""
        where, rest = self.name.split("/", 1)
        face = FACE_NAMES.get(where, where)
        of = f" of chamber {self.chamber}" if self.chamber is not None else ""
        if where.startswith("firebox-"):
            wall = FACE_NAMES[self.face or "floor"].lower()
            number = rest.split("-", 1)[0]
            return f"Firebox {where.split('-', 1)[1]}, {wall}, layer {number} from the inside"
        if self.chamber is not None and (where == "division" or "-by-wall" in rest):
            between = f"the wall between chambers {self.chamber} and {self.chamber + 1}"
            face = f"Wall between chambers {self.chamber} and {self.chamber + 1}"
            if where != "division":
                face = f"{FACE_NAMES.get(where, where)} beside {between}"
            of = ""
        if rest.startswith("skewback"):
            return f"{face}{of}, the skewback and fill on top"
        number = rest.split("-", 1)[0]
        above = ", above the springline" if self.cap else ""
        return f"{face}{of}, layer {number} from the inside{above}"

    @property
    def length_y(self) -> float:
        return self.hi[1] - self.lo[1]

    @property
    def length_run(self) -> float:
        """How far a profile or arch runs: along y, or along x when ``across``."""
        return self.hi[0] - self.lo[0] if self.across else self.length_y

    @property
    def volume(self) -> float:
        if self.groin is not None:
            return self.groin.volume(self.lo, self.hi)
        if self.revolve is not None:
            # A polygon through the corners has N·sin(2π/N)/(2π) of the circle's area, at every r
            scale = 1.0 if self.sides is None else polygon_fraction(self.sides)
            return Revolved(self.revolve).volume * scale
        if self.plan is not None:
            return self._plan_volume(self.plan)
        if self.profile is not None:
            pts, nxt = self.profile, self.profile[1:] + self.profile[:1]
            area = abs(sum(x0 * z1 - x1 * z0 for (x0, z0), (x1, z1) in zip(pts, nxt, strict=True)))
            return area / 2 * self.length_run  # the shoelace formula, times the length
        if self.dome is not None:
            return self._dome_volume(self.dome)
        if self.arch is None:
            return (self.hi[0] - self.lo[0]) * (self.hi[1] - self.lo[1]) * (self.hi[2] - self.lo[2])
        if self.cap:
            return self.arch.segment_area * self.length_run
        r, t, a = self.arch.radius, self.arch.thickness, self.arch.half_angle
        return a * ((r + t) ** 2 - r**2) * self.length_run

    def _plan_volume(self, plan: tuple[tuple[float, float], ...], n: int = 400) -> float:
        """A prism on the plan (less ``inner``): its area by the shoelace formula times its
        height. Under or within a dome: the dome's heights over the plan, summed on a fine grid
        (the midpoint rule), as _dome_volume's."""
        if self.dome is None:
            area = _shoelace(plan) - (_shoelace(self.inner) if self.inner else 0.0)
            return area * (self.hi[2] - self.lo[2])
        (x0, y0, springline), (x1, y1, _) = self.lo, self.hi
        xs = x0 + (np.arange(n) + 0.5) / n * (x1 - x0)
        ys = y0 + (np.arange(n) + 0.5) / n * (y1 - y0)
        x, y = np.meshgrid(xs, ys)
        inside = _inside(plan, x, y)
        if self.inner:
            inside &= ~_inside(self.inner, x, y)
        d = self.dome
        top = d.heights(x, y, d.radius + d.thickness)
        bottom = springline if self.cap else np.maximum(d.heights(x, y, d.radius), springline)
        cell = (x1 - x0) * (y1 - y0) / n / n
        return float(np.sum(np.where(inside, np.maximum(top - bottom, 0.0), 0.0)) * cell)

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
    if c.bend is not None and si(c.bend, "degree") > 0:
        from kilndesigner.massing import MassingError, check_bend, run_of

        try:
            check_bend(run_of(kiln))
        except MassingError as e:
            return str(e)
    if c.chambers > 1 and isinstance(kiln.roof, CatenaryArch) and slope_of(kiln) > 0:
        return (
            "a catenary over chambers stepped up a slope is calculated and drawn, but not laid out "
            "in brick or priced: no source here says how one chamber's catenary meets the next's "
            "at a step"
        )
    return None


def in_a_row(kiln: Kiln) -> bool:
    """Chambers in a row, laid out by run_parts.py; and one chamber under an arch along its depth
    (roof.along), laid out as a row of one."""
    return kiln.chamber.chambers > 1 or arches_along(kiln)


def on_a_stand(kiln: Kiln) -> bool:
    """A single level box: its frame, door and element grooves are drawn (hardware.py). Round
    kilns, chambers in a row and kilns on a slope take only their chimney and burners."""
    from kilndesigner.bend import bent

    return (
        kiln.chamber.shape != "round"
        and not in_a_row(kiln)
        and not slope_of(kiln)
        and not bent(kiln)
    )


def _thicknesses(kiln: Kiln, face: Face) -> list[tuple[str, float]]:
    layers = kiln.lining.for_face(face, door_face=kiln.door_face)
    return [(layer.material, si(layer.thickness, "mm")) for layer in layers]


def thicknesses(kiln: Kiln, face: Face) -> list[tuple[str, float]]:
    """Each layer of a face, inside first: (material, thickness in mm)."""
    return _thicknesses(kiln, face)


def lining_parts(kiln: Kiln) -> list[Part]:
    """The lining as boxes and arch rings: pure arithmetic, testable without OpenCascade. A single
    chamber on a slope is laid out level, each part then tilted up the slope (Part.tilt)."""
    from dataclasses import replace

    if (why := not_drawn(kiln)) is not None:
        raise GeometryNotSupportedError(why)
    from kilndesigner.firebox_parts import carve, firebox_parts, openings

    parts = _level_parts(kiln)
    if kiln.loading.opening is not None:
        from kilndesigner.door import cut_door

        parts = cut_door(kiln, parts)
    holes = openings(kiln)
    if in_a_row(kiln):
        from kilndesigner.run_parts import flue_holes

        holes += flue_holes(kiln)
    if holes or kiln.heat.fire is not None:
        # A trough's cut takes the floor out under it; its own floor is laid in the cut
        walls = [h for h in holes if not h.name.endswith("/trough")]
        parts = carve(parts, holes) + carve(firebox_parts(kiln), walls)
    tilt = slope_of(kiln) if not in_a_row(kiln) else 0.0
    if not tilt:
        return parts
    pivot = -si(kiln.chamber.depth, "mm") / 2
    return [replace(p, tilt=tilt, pivot=pivot) for p in parts]


def slope_of(kiln: Kiln) -> float:
    """The floor's slope (radians), 0 when level."""
    s = kiln.chamber.slope
    return math.radians(si(s, "degree")) if s is not None else 0.0


def _level_parts(kiln: Kiln) -> list[Part]:
    from kilndesigner.castable import resolve_material

    if kiln.chamber.shape == "round":
        return _round_parts(kiln)
    if kiln.chamber.outline is not None:
        return _outline_parts(kiln)
    if isinstance(kiln.roof, SprungArch) and kiln.roof.crossing is not None:
        from kilndesigner.crossing import crossing_parts

        return crossing_parts(kiln)
    if in_a_row(kiln) and isinstance(kiln.roof, CatenaryArch):
        return _catenary_parts(kiln)
    if in_a_row(kiln):
        from kilndesigner.run_parts import run_parts

        return run_parts(kiln)
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
        name = f"{'door' if face == kiln.door_wall else face}/{i + 1}-{mat}"
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
                name = f"{'door' if face == kiln.door_wall else face}/{i + 1}-{mat}-arch"
                parts.append(
                    Part(
                        name, mat, resolve_material(kiln, mat).kind,
                        (-arch.half_width, ys[0], h), (arch.half_width, ys[1], h + arch.rise),
                        arch=shape, cap=True, face=face,
                    )
                )  # fmt: skip
                reached += th
        for i, (mat, th) in enumerate(_thicknesses(kiln, "roof")):
            r_in = arch.radius + cum
            shape = ArchShape(r_in, th, centre_z, arch.half_angle)
            # Past a semicircle the ring is widest at its centre's height, and its outer corner at
            # each springing turns down below the springline
            half_width = (r_in + th) * (
                1.0 if arch.half_angle > math.pi / 2 else math.sin(arch.half_angle)
            )
            lo = (-half_width, y0, min(h, centre_z + (r_in + th) * math.cos(arch.half_angle)))
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
    if isinstance(kiln.roof, OpenTop):
        return parts  # the setting is covered for each firing: nothing built over the walls
    for i, (mat, th) in enumerate(_thicknesses(kiln, "roof")):
        add("roof", i, mat, (x0, y0, h + cum), (x1, y1, h + cum + th))
        cum += th
    return parts


def _catenary_parts(kiln: Kiln) -> list[Part]:
    """A catenary arch from the floor (combustion-and-masonry.md §6.6): the floor under it all,
    the arch's rings standing on the floor and running from the outside of the back wall to the
    outside of the front, and the end walls closing it inside its ends. Each ring is the inside
    curve moved out by the layers inside it. Chambers in a row on the level stand under one
    catenary the whole run long, the walls between them closing it as the end walls do, as a
    tube's vault does (run_parts._tube)."""
    from kilndesigner.castable import resolve_material

    w, h = si(kiln.chamber.width, "mm"), si(kiln.chamber.height, "mm")
    first, last = -si(kiln.chamber.depth, "mm") / 2, si(kiln.chamber.depth, "mm") / 2
    between: list[tuple[int, float]] = []  # each wall between chambers: its chamber, its near face
    if in_a_row(kiln):
        from kilndesigner.run_parts import run_layout

        run = run_layout(kiln)
        first, last = run.front(0), run.back(run.chambers - 1)
        between = [(i + 1, run.back(i)) for i in range(run.chambers - 1)]
    curve = CatenaryCurve(w, h)
    rings = _thicknesses(kiln, "roof")
    ends = {f: _thicknesses(kiln, f) for f in ("front", "back")}
    y0 = first - sum(t for _, t in ends["front"])
    y1 = last + sum(t for _, t in ends["back"])
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
        at = last if face == "back" else first
        for i, (mat, th) in enumerate(ends[face]):
            ys = sorted((at + sign * reached, at + sign * (reached + th)))
            name = f"{'door' if face == kiln.door_wall else face}/{i + 1}-{mat}"
            lo, hi = (-w / 2, ys[0], 0.0), (w / 2, ys[1], h)
            parts.append(Part(name, mat, kind(mat), lo, hi, face=face, profile=inside))
            reached += th
    for chamber, y in between:
        for i, (mat, th) in enumerate(
            (x.material, si(x.thickness, "mm")) for x in kiln.lining.walls
        ):
            parts.append(
                Part(
                    f"division/{i + 1}-{mat}-chamber-{chamber}", mat, kind(mat), (-w / 2, y, 0.0),
                    (w / 2, y + th, h), face="back", profile=inside, chamber=chamber,
                )
            )  # fmt: skip
            y += th
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


def _round_parts(kiln: Kiln) -> list[Part]:
    """A round chamber (round_masonry.py): the floor as discs under the whole kiln, out to the
    wall's outside; the wall as rings, one per layer, from the floor to the springline; and a flat
    roof as discs on the wall, or a dome as layers of a sphere through the springline circle
    (shape.RoundDome) above the springline, or nothing for an open top. Each is an outline in the
    r–z plane turned about the chamber's axis. A faceted wall (shape.facets) is a regular
    polygon instead, its flats the bricks' faces, and the floor and lid slabs are the polygon out
    to the wall's outside corners, as round_masonry lays them; r is then out to the corners."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.shape import facets

    radius, h = si(kiln.chamber.width, "mm") / 2, si(kiln.chamber.height, "mm")
    walls = [(x.material, si(x.thickness, "mm")) for x in kiln.lining.walls]
    sides = facets(kiln)
    # Out to the corners for a faceted wall: each layer's apothem over cos(π/N)
    corner = 1.0
    if sides is not None:
        from kilndesigner.rings import inside_apothem

        corner = 1 / math.cos(math.pi / sides)
        radius = inside_apothem(2 * radius, sides)
    outside = (radius + sum(t for _, t in walls)) * corner
    parts: list[Part] = []

    def add(name: str, mat: str, outline: list[tuple[float, float]], th: float, face: Face | None):
        reach = max(r for r, _ in outline)
        zs = [z for _, z in outline]
        parts.append(
            Part(
                name, mat, resolve_material(kiln, mat).kind, (-reach, -reach, min(zs)),
                (reach, reach, max(zs)), face=face, ring=th, revolve=tuple(outline),
                sides=sides if flat else None,
            )
        )  # fmt: skip

    flat = True
    cum = 0.0
    # A floor inside the walls (Paragon's) is the inside outline, in the wall's lowest course,
    # the wall running a course below the inside floor; else it runs under the walls (Skutt's)
    inside = kiln.chamber.floor_inside
    floor_reach = radius * corner if inside else outside
    foot = -FLOOR_COURSE_IN * IN if inside else 0.0
    for i, (mat, th) in enumerate(_thicknesses(kiln, "floor")):
        z0, z1 = -cum - th, -cum
        add(f"floor/{i + 1}-{mat}", mat,
            [(0.0, z0), (floor_reach, z0), (floor_reach, z1), (0.0, z1)], th, "floor")  # fmt: skip
        cum += th
    r = radius
    for i, (mat, th) in enumerate(walls):
        r0, r1 = r * corner, (r + th) * corner
        add(f"wall/{i + 1}-{mat}", mat, [(r0, foot), (r1, foot), (r1, h), (r0, h)], th, None)
        r += th
    roof = kiln.roof
    cum = 0.0
    if isinstance(roof, Dome):
        flat = False  # a dome is a sphere's; facets() is for electric kilns, with flat lids
        from kilndesigner.shape import RoundDome

        dome = RoundDome(si(kiln.chamber.width, "mm"), si(roof.rise, "mm"))
        below = dome.radius - dome.rise  # the sphere's centre under the springline
        centre = h - below
        rho = dome.radius
        for i, (mat, th) in enumerate(_thicknesses(kiln, "roof")):
            add(f"roof/{i + 1}-{mat}", mat, shell_profile(rho, rho + th, centre, h), th, "roof")
            rho += th
    elif isinstance(roof, FlatRoof):
        for i, (mat, th) in enumerate(_thicknesses(kiln, "roof")):
            z0, z1 = h + cum, h + cum + th
            add(f"roof/{i + 1}-{mat}", mat, [(0.0, z0), (outside, z0), (outside, z1), (0.0, z1)],
                th, "roof")  # fmt: skip
            cum += th
    return parts


def _outline_parts(kiln: Kiln) -> list[Part]:
    """A curved plan (chamber.outline, form.py): the floor under the whole kiln, out to the
    walls' outside; each wall layer a ring on the plan moved out by the layers inside it
    (outline.offset), from the floor to the springline, its top filled up to a dome's sphere; and
    the dome's layers (or a flat roof's slabs) over the whole kiln, as on a box (_dome_parts)."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.form import crown_of, plan_of
    from kilndesigner.outline import SphereDome, offset

    plan, h = plan_of(kiln, "mm"), si(kiln.chamber.height, "mm")
    walls = _thicknesses(kiln, "left")
    out_t = sum(t for _, t in walls)

    def pts(t: float) -> tuple[tuple[float, float], ...]:
        return tuple(offset(plan, t).points(48))

    outside = pts(out_t)
    parts: list[Part] = []

    def add(name: str, mat: str, th: float, z: tuple[float, float], plan_: PlanPoints,
            inner: PlanPoints | None = None, **more: Any) -> None:  # fmt: skip
        px, py = [x for x, _ in plan_], [y for _, y in plan_]
        parts.append(
            Part(
                name, mat, resolve_material(kiln, mat).kind, (min(px), min(py), z[0]),
                (max(px), max(py), z[1]), ring=th, plan=plan_, inner=inner, **more,
            )
        )  # fmt: skip

    cum = 0.0
    for i, (mat, th) in enumerate(_thicknesses(kiln, "floor")):
        add(f"floor/{i + 1}-{mat}", mat, th, (-cum - th, -cum), outside, face="floor")
        cum += th
    roof = kiln.roof
    dome: DomeShape | None = None
    crown = crown_of(kiln, "mm")
    if isinstance(roof, Dome):
        sphere = SphereDome(plan, si(roof.rise, "mm"), crown)
        dome = DomeShape(sphere.radius, 0.0, h + sphere.rise - sphere.radius, crown[1])
    reach = 0.0
    for i, (mat, th) in enumerate(walls):
        ring, inner = pts(reach + th), pts(reach)
        add(f"walls/{i + 1}-{mat}", mat, th, (0.0, h), ring, inner)
        if dome is not None:
            top = dome.centre_z + dome.radius
            add(f"walls/{i + 1}-{mat}-dome", mat, th, (h, top), ring, inner, cap=True, dome=dome)
        reach += th
    cum = 0.0
    for i, (mat, th) in enumerate(_thicknesses(kiln, "roof")):
        if dome is None:
            add(f"roof/{i + 1}-{mat}", mat, th, (h + cum, h + cum + th), outside, face="roof")
        else:
            shell = DomeShape(dome.radius + cum, th, dome.centre_z, dome.centre_y)
            top = dome.centre_z + dome.radius + cum + th
            add(f"roof/{i + 1}-{mat}", mat, th, (h, top), outside, face="roof", dome=shell)
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
    if kiln.chamber.shape == "round":
        return h  # the round wall stands to the springline all the way round
    if kiln.chamber.outline is not None:
        return _outline_top(kiln, face, u, h)
    if isinstance(kiln.roof, CatenaryArch):
        return CatenaryCurve(w, h).z(u) if end and abs(u) < w / 2 else 0.0
    if isinstance(kiln.roof, SprungArch) and arches_along(kiln):
        # Each chamber's arch spans its depth along the draft (run_parts.py): it meets the side
        # walls, the first chamber's centred on u = 0, and the end walls stand to the springline
        # (u along y); springing unevenly, the front wall stands to its own springline
        from kilndesigner.shape import along_arch

        arch = along_arch(kiln, "mm")
        if face == "front":
            return h - arch.drop
        if end or abs(u) >= d / 2:
            return h if u > 0 or end else h - arch.drop
        return h + arch.height(u)
    if isinstance(kiln.roof, SprungArch) and end:
        arch = Arch(w, si(kiln.roof.rise, "mm"))
        if abs(u) < arch.half_width:  # past a semicircle, the arch is wider than the span
            return max(h, h + arch.rise - arch.radius + math.sqrt(arch.radius**2 - u**2))
    if isinstance(kiln.roof, Dome) and abs(u) < (w if end else d) / 2:
        dome = SailDome(w, d, si(kiln.roof.rise, "mm"))
        off = d / 2 if end else w / 2  # the wall's distance from the centre line
        return h + max(0.0, dome.centre + math.sqrt(dome.radius**2 - off**2 - u**2))
    return h


def bulge_fill(
    r_out: float, centre_z: float, h: float, outer: float, steps: int = 16
) -> list[tuple[float, float]]:
    """The fill beside an arch more than a semicircle (its centre above the springline ``h``):
    from the ring's outside at the springline up to its widest, at ``centre_z``, out to the wall's
    outer face at ``outer``; empty where the ring reaches past that face at the springline."""
    foot = math.sqrt(r_out**2 - (h - centre_z) ** 2)
    if foot >= outer:
        return []
    outline: list[tuple[float, float]] = []
    for i in range(steps + 1):
        z = h + (centre_z - h) * i / steps
        point = (min(outer, math.sqrt(r_out**2 - (z - centre_z) ** 2)), z)
        if not outline or outline[-1] != point:
            outline.append(point)
    if outline[-1][0] < outer:
        outline.append((outer, centre_z))
    return [*outline, (outer, h)]


def _outline_top(kiln: Kiln, face: Face, u: float, h: float) -> float:
    """A curved plan's wall top at ``u`` along the face (mm): where the dome's sphere meets the
    wall, at the outline's point there. A side wall's u is along y from the middle, the curve's
    half-width across; the front's along x, at the front's straight; the back is the plan's far
    end, standing to the springline."""
    from kilndesigner.form import crown_of, plan_of
    from kilndesigner.outline import SphereDome, half_width

    roof = kiln.roof
    if not isinstance(roof, Dome) or face == "back":
        return h
    plan = plan_of(kiln, "mm")
    if face in ("left", "right"):
        x, y = half_width(plan, u), u
    else:
        y = plan.bounds[2] + 1e-6
        if abs(u) >= half_width(plan, y):
            return h
        x = u
    crown = crown_of(kiln, "mm")
    dome = SphereDome(plan, si(roof.rise, "mm"), crown)
    under = dome.radius**2 - x * x - (y - crown[1]) ** 2
    return h + max(0.0, dome.rise - dome.radius + math.sqrt(max(under, 0.0)))


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
        if a > math.pi / 2:
            # Past a semicircle the arch springs from the wall's top, its radius there turned
            # below the level, and bulges out above it: the fill is what lies between the ring's
            # outside and the wall's outer face, from the springline up to the ring's widest
            outline = bulge_fill(r_out, centre_z, h, outer)
            if not outline:
                continue  # the ring bulges past the wall's outer face: nothing to fill
        elif top[0] <= outer:
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


def grooves_drawn(kiln: Kiln) -> bool:
    """Whether the model draws the element grooves: in a box on a stand, or round a round kiln's
    wall; not yet along chambers in a row or up a slope."""
    return on_a_stand(kiln) or (kiln.chamber.shape == "round" and kiln.chamber.slope is None)


QUARTERS = {"front": -90.0, "left": 180.0, "back": 90.0, "right": 0.0}
"""The middle of each quarter of a round kiln's ring, degrees from +x (electric._groove_length
gives the elements a quarter of the ring for each wall named)."""


def hot_face_reach(kiln: Kiln, angle: float) -> float:
    """How far a round kiln's hot face is from its axis (mm) in the direction ``angle`` (radians
    from +x): the radius, or for a faceted wall, out to the polygon (rings.inside_apothem)."""
    from kilndesigner.shape import facets

    radius = si(kiln.chamber.width, "mm") / 2
    sides = facets(kiln)
    if sides is None:
        return radius
    from kilndesigner.rings import inside_apothem

    corner = inside_apothem(2 * radius, sides) / math.cos(math.pi / sides)
    return corner * polygon_reach(sides, angle)


def round_groove(kiln: Kiln, walls: list[str], z: float) -> list[tuple[float, float, float]]:
    """One groove round a round kiln's hot face at height ``z`` (mm): round the facets of each
    quarter of the ring the elements are in (electric._groove_length), front, left, back, right,
    the coil bending at each corner; a circle's when the wall isn't faceted."""
    from kilndesigner.shape import facets

    sides = facets(kiln)
    steps = 12  # a quarter of a circle drawn in this many chords
    points: list[tuple[float, float, float]] = []
    for wall in [w for w in ("front", "left", "back", "right") if w in walls]:
        mid = math.radians(QUARTERS[wall])
        start, end = mid + math.pi / 4, mid - math.pi / 4  # clockwise, as the box's run goes
        angles = [start + (end - start) * k / steps for k in range(steps + 1)]
        if sides is not None:
            # The quarter's ends, and every corner between them
            corners = [
                end + (-math.pi / 2 + (2 * k + 1) * math.pi / sides - end) % (2 * math.pi)
                for k in range(sides)
            ]
            inside = sorted((a for a in corners if end + 1e-9 < a < start - 1e-9), reverse=True)
            angles = [start, *inside, end]
        for a in angles:
            reach = hot_face_reach(kiln, a)
            p = (reach * math.cos(a), reach * math.sin(a), z)
            if not points or math.dist(points[-1], p) > 1e-6:
                points.append(p)
    return points


def element_runs(kiln: Kiln, rows: int, coil_diameter_mm: float) -> list[ElementRun]:
    """Element coils centred on the inside face of the element walls, one per row."""
    electric = kiln.heat.electric
    if electric is None or rows == 0:
        return []
    w, d, h = (si(getattr(kiln.chamber, n), "mm") for n in ("width", "depth", "height"))
    if kiln.chamber.shape == "round":
        return [
            ElementRun(
                f"element/{row + 1}", coil_diameter_mm,
                tuple(round_groove(kiln, list(electric.walls), h * (row + 0.5) / rows)),
            )
            for row in range(rows)
        ]  # fmt: skip
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

    if part.across:
        # A (y, z) outline in the y–z plane, extruded along x from the part's x
        assert part.profile is not None
        across: Any = extrude(Plane.YZ * Polygon(*part.profile, align=None), amount=part.length_run)
        return Pos(part.lo[0] - across.bounding_box().min.X, 0, 0) * across
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
    solid: Any = plan & (Pos(0, d.centre_y, d.centre_z) * Sphere(d.radius + d.thickness))
    if not part.cap:
        solid = solid - Pos(0, d.centre_y, d.centre_z) * Sphere(d.radius)
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


def _revolved_solid(part: Part) -> Any:
    """A round wall's layer, a disc or a dome's layer: its r–z outline turned about the z axis."""
    from build123d import Axis, Plane, Polyline, make_face, revolve

    assert part.revolve is not None
    if part.sides is not None:
        return _polygon_solid(part)
    face: Any = Plane.XZ * make_face(Polyline(*part.revolve, close=True))
    return revolve(face, Axis.Z)


def _polygon_solid(part: Part) -> Any:
    """A faceted round kiln's wall layer or slab: its rectangle in the r–z plane (r out to the
    corners) made a regular polygon, or a polygon ring, and extruded up."""
    from build123d import Plane, Polygon, extrude

    assert part.revolve is not None
    assert part.sides is not None
    rs, zs = [r for r, _ in part.revolve], [z for _, z in part.revolve]
    r0, r1, z0, z1 = min(rs), max(rs), min(zs), max(zs)
    plane = Plane.XY.offset(z0)
    outer: Any = plane * Polygon(*polygon_corners(part.sides, r1), align=None)
    if r0 > 1e-6:
        outer -= plane * Polygon(*polygon_corners(part.sides, r0), align=None)
    return extrude(outer, z1 - z0)


def part_solid(part: Part) -> Any | None:
    """The solid of one lining part, whatever its shape, tilted up its slope; None for a wall with
    no height (an arch springing from the floor, as in a groundhog)."""
    solid = _level_solid(part)
    if solid is None or not part.tilt:
        return solid
    from build123d import Axis

    return solid.rotate(Axis((0, part.pivot, 0), (1, 0, 0)), math.degrees(part.tilt))


def _plan_solid(part: Part) -> Any:
    """A curved plan's layer: its outline (less the inner one) extruded from lo z to hi z, cut
    to the dome's sphere (a wall's cap) or to the shell between its spheres."""
    from build123d import Plane, Polygon, Pos, Sphere, extrude

    assert part.plan is not None
    plane = Plane.XY.offset(part.lo[2])
    face: Any = plane * Polygon(*part.plan, align=None)
    if part.inner is not None:
        face -= plane * Polygon(*part.inner, align=None)
    d = part.dome
    solid: Any = extrude(face, part.hi[2] - part.lo[2] + (1.0 if d is not None else 0.0))
    if d is None:
        return solid
    solid &= Pos(0, d.centre_y, d.centre_z) * Sphere(d.radius + d.thickness)
    if not part.cap:
        solid -= Pos(0, d.centre_y, d.centre_z) * Sphere(d.radius)
    return solid


def _level_solid(part: Part) -> Any | None:
    if part.groin is not None:
        from kilndesigner.crossing import groin_solid

        return groin_solid(part)
    if part.plan is not None:
        return _plan_solid(part)
    if part.revolve is not None:
        return _revolved_solid(part)
    if part.dome is not None:
        return _dome_solid(part)
    if part.arch is not None or part.profile is not None:
        return _arch_solid(part)
    if any(b - a < 1e-6 for a, b in zip(part.lo, part.hi, strict=True)):
        return None
    return _box(part.lo, part.hi)


type Hole = tuple[tuple[float, float, float], tuple[float, float, float], Any]
"""A hole to cut through the lining: its bounding box's corners (mm) and its solid."""


def _overlaps(solid: Any, lo: tuple[float, ...], hi: tuple[float, ...]) -> bool:
    bb = solid.bounding_box()
    return (
        hi[0] > bb.min.X and lo[0] < bb.max.X and hi[1] > bb.min.Y and lo[1] < bb.max.Y
        and hi[2] > bb.min.Z and lo[2] < bb.max.Z
    )  # fmt: skip


def _cut(solid: Any, holes: list[Hole]) -> Any:
    for lo, hi, hole in holes:
        if _overlaps(solid, lo, hi):
            solid = solid - hole
    return solid


def _holes(kiln: Kiln, hardware: Hardware | None) -> list[Hole]:
    """The ports and openings through the lining: a box kiln's openings from the hardware layout;
    a round kiln's ports mapped round its curve, as the shells' are (massing.port_solid)."""
    if hardware is None:
        return []
    if on_a_stand(kiln):
        return [(*o.box, _opening_solid(o)) for o in hardware.openings]
    # Burner ports up through the floor and an updraft's flue through the roof stand where the
    # hardware puts them over the first chamber's floor; the walls' ports follow the run
    h = si(kiln.chamber.height, "mm")
    holes: list[Hole] = [
        _placed_hole(kiln, *o.box, _opening_solid(o))
        for o in hardware.openings
        if o.box[1][2] <= 30.0 or o.box[0][2] >= h - 30.0
    ]
    if in_a_row(kiln):
        from kilndesigner.run_parts import run_holes

        return holes + run_holes(kiln, hardware)
    from kilndesigner.massing import port_solid, run_of

    run = run_of(kiln)
    for spot in hardware.ports:
        hole = port_solid(kiln, run, spot)
        bb = hole.bounding_box()
        holes.append(((bb.min.X, bb.min.Y, bb.min.Z), (bb.max.X, bb.max.Y, bb.max.Z), hole))
    return holes


def _tilted_solid(kiln: Kiln, solid: Any) -> Any:
    """A solid laid out level, tilted up a single chamber's slope as its parts are."""
    tilt = slope_of(kiln) if not in_a_row(kiln) else 0.0
    if not tilt:
        return solid
    from build123d import Axis

    pivot = -si(kiln.chamber.depth, "mm") / 2
    return solid.rotate(Axis((0, pivot, 0), (1, 0, 0)), math.degrees(tilt))


def _placed_hole(
    kiln: Kiln, lo: tuple[float, float, float], hi: tuple[float, float, float], solid: Any
) -> Hole:
    """A hole laid out straight and level, put where the lining is: round a bend, swept as the
    walls are, and up a single chamber's slope."""
    from kilndesigner.bend import bent, bent_box
    from kilndesigner.massing import run_of

    if bent(kiln):
        solid = bent_box(lo, hi, run_of(kiln))
    solid = _tilted_solid(kiln, solid)
    bb = solid.bounding_box()
    return ((bb.min.X, bb.min.Y, bb.min.Z), (bb.max.X, bb.max.Y, bb.max.Z), solid)


def _placed_part(kiln: Kiln, part: Part) -> Any | None:
    """A lining part's solid, round a bend when the run bends."""
    from kilndesigner.bend import bent, bent_solid
    from kilndesigner.massing import run_of

    if not bent(kiln):
        return part_solid(part)
    solid = bent_solid(part, run_of(kiln))
    if solid is None or not part.tilt:
        return solid
    from build123d import Axis

    return solid.rotate(Axis((0, part.pivot, 0), (1, 0, 0)), math.degrees(part.tilt))


def build_model(
    kiln: Kiln, elements: list[ElementRun] | None = None, hardware: Hardware | None = None
) -> Compound:
    from build123d import Circle, Color, Compound, Plane, Polyline, Transition, sweep

    holes = _holes(kiln, hardware)
    grates: list[Any] = []
    if kiln.heat.fire is not None:
        from kilndesigner.firebox_parts import grate_pieces, model_holes

        holes += [_placed_hole(kiln, lo, hi, solid) for lo, hi, solid in model_holes(kiln)]
        grates = grate_pieces(kiln)
    if in_a_row(kiln):
        # The flue holes between chambers, for the walls that aren't boxes (a catenary's)
        from kilndesigner.run_parts import flue_holes

        holes += [_placed_hole(kiln, o.lo, o.hi, _box(o.lo, o.hi)) for o in flue_holes(kiln)]
    # A door in part of a wall: its opening cuts the walls (the curved ones too), not the door
    from kilndesigner.door import model_door_holes

    doorway = [_placed_hole(kiln, lo, hi, solid) for lo, hi, solid in model_door_holes(kiln)]  # type: ignore[arg-type]
    children: list[Any] = []
    for part in lining_parts(kiln):
        solid = _placed_part(kiln, part)
        if solid is None:
            continue
        solid = _cut(solid, holes if part.name.startswith("door/") else holes + doorway)
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
    if in_a_row(kiln):
        # The frame and door are drawn for a box on a stand, so they're left out, as on a round
        # kiln; the chimney and burners stand where the run puts them
        from kilndesigner.run_parts import run_pieces

        children += run_pieces(kiln, hardware)
        hardware = None
    elif not on_a_stand(kiln):
        # The frame and door are drawn for a level box on a stand; the chimney and burners stand
        # clear of the bricks, where the shells' model puts them, up the slope or round the bend
        from kilndesigner.massing import moved_pieces, run_of

        children += moved_pieces(kiln, run_of(kiln), hardware)
        hardware = None
    from kilndesigner.bend import bent, moved
    from kilndesigner.massing import run_of

    for piece in grates:
        solid = piece_solid(piece)
        if bent(kiln):
            solid = moved(solid, solid.bounding_box().center().Y, run_of(kiln))
        solid = _tilted_solid(kiln, solid)
        solid.label = piece.name
        solid.color = Color(*COLOURS[piece.kind])
        children.append(solid)
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
        if not p.is_skewback and not p.cap:
            detail += f", {length_text(p.thickness, us)} thick"
        index[p.name] = entry(p.title, detail, p.kind)
    if kiln.heat.fire is not None:
        from kilndesigner.firebox_parts import grates

        for g in grates(kiln):
            index[g.name] = entry(g.title, g.detail, "steel")
    electric = report.electric
    if grooves_drawn(kiln) and electric is not None and electric.elements is not None:
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
        if not on_a_stand(kiln) and not piece.name.startswith(("chimney/", "burner/")):
            continue  # not drawn on a round kiln (build_model)
        index[piece.name] = entry(piece.title, piece.detail, piece.kind)
    return index


def write_model(kiln: Kiln, report: Report, out_dir: Path) -> dict[str, Path]:
    """Build the kiln with its elements, frame, door, ports and chimney, export it, and write
    what each part is and where its ports are."""
    from kilndesigner.hardware import build_hardware, layout

    if not_drawn(kiln) is not None:
        return _write_massing(kiln, report, out_dir)
    runs: list[ElementRun] = []
    # Element grooves along chambers in a row or up a slope aren't laid out yet
    round_ = not on_a_stand(kiln)
    if grooves_drawn(kiln) and report.electric is not None and report.electric.elements is not None:
        el = report.electric.elements
        runs = element_runs(kiln, el.groove_rows, el.coil_outside_diameter_mm)
    hardware = build_hardware(kiln, report.frame, report.gas, report.fire)
    written = export_model(build_model(kiln, runs, hardware), out_dir)
    parts = out_dir / "parts.json"
    index = part_index(kiln, report, hardware)
    parts.write_text(json.dumps(index, ensure_ascii=False, indent=2), "utf-8")
    places = out_dir / LAYOUT
    where = brick_layout(kiln, hardware) if round_ else layout(kiln, hardware)
    places.write_text(json.dumps(where, ensure_ascii=False, indent=2), "utf-8")
    return {**written, "parts": parts, "layout": places}


def brick_layout(kiln: Kiln, hardware: Hardware) -> dict[str, object]:
    """The layout of a kiln laid out in brick that isn't a level box on a stand: with the radius,
    for ports on a round wall, or the run's chambers, slope and bend (massing.massing_layout).
    Chambers in a row stand level, each floor ``step`` mm above the last (run_parts.py), rather
    than tilted up the slope as the shells are, so the viewer raises a port with its chamber's
    floor."""
    from kilndesigner.massing import massing_layout

    where = massing_layout(kiln, hardware)
    if in_a_row(kiln):
        from kilndesigner.run_parts import run_layout

        run = where["run"]
        assert isinstance(run, dict)
        run["step"] = run_layout(kiln).step  # pyright: ignore[reportUnknownMemberType]
    return where


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
