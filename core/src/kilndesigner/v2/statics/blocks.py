"""Rigid blocks and the faces where they touch, from build123d solids.

A block is a solid made by build123d on OpenCascade: a course of a wall cut from the engine's own
part solid, an arch's voussoir, a skewback. OpenCascade's mass properties give its volume and
centroid; its weight is its material's density × g × volume.

The contacts between blocks are found two ways (`docs/research/tool-triples.md` §1, from the probe
`scratch/toolsets/whole-kiln/blocks_occ.py`):

- **Pairwise**, for planar faces, the default: bounding boxes filter the pairs of blocks; two
  planar faces with opposite normals lying on one plane, within ``tol``, are intersected by a
  Boolean common. The second face is moved onto the first one's plane first, so a gap or an overlap
  up to ``tol`` still counts. It found every contact of the probe's cases to the printed digits.
- **General Fuse** (OpenCascade's ``BOPAlgo_Builder`` with glue): every face two solids share,
  curved ones included. It is the only way to find curved contacts; a gap needs its fuzzy value,
  and an overlap of 1e-4 in turned into a sliver in the probe, so it is used for curved contacts.

A contact carries its polygon's corners (planar) or points sampled over its face (curved), each
with the normal from block ``a`` into block ``b``. The solids are in the caller's model unit (the
engine builds in millimetres) and ``unit`` gives metres per model unit: everything a block or a
contact reports is SI (metres, m², m³, kg/m³, newtons).

A planar contact's corners bound where its resultant can act. The corners of a non-convex contact
would let it act outside the contact; the engine's cuts (courses, voussoirs) make convex ones.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from importlib import import_module
from typing import Any

import build123d as bd
import numpy as np
import numpy.typing as npt

type FloatArray = npt.NDArray[np.float64]

G = 9.80665
"""Standard gravity, m/s² (exact by definition, 3rd CGPM, 1901)."""

_OPPOSITE = 1e-7  # 1 + n_a · n_b below this: the faces' normals are opposite (about 0.03°)


@dataclass(frozen=True)
class Load:
    """A force on a block besides its own weight: ``force`` (N) acting at ``point`` (m)."""

    point: tuple[float, float, float]
    force: tuple[float, float, float]


@dataclass(frozen=True, eq=False)
class PlaneFace:
    """One planar face of a block: its outward normal, its plane's offset (normal · x) and its
    bounding box, in model units."""

    normal: FloatArray
    offset: float
    face: Any
    lo: FloatArray
    hi: FloatArray


@dataclass(eq=False)
class Block:
    """A rigid block: a solid, its material's density (kg/m³) and how it is held.

    ``fixed`` blocks (the ground, a frame, a support) have no equilibrium of their own. ``unit``
    is metres per model unit of the solid (0.001 for the engine's millimetres)."""

    name: str
    solid: Any
    density: float = 0.0
    unit: float = 1.0
    fixed: bool = False
    tag: str = ""
    material: str | None = None
    loads: tuple[Load, ...] = ()
    volume: float = field(init=False)  # m³
    centroid: FloatArray = field(init=False)  # m
    lo: FloatArray = field(init=False)  # bounding box, model units
    hi: FloatArray = field(init=False)
    planes: list[PlaneFace] = field(init=False)
    curved: int = field(init=False)  # how many of its faces aren't planes

    def __post_init__(self) -> None:
        s = self.solid
        self.volume = float(s.volume) * self.unit**3
        c = s.center(bd.CenterOf.MASS)
        self.centroid = np.array([c.X, c.Y, c.Z], dtype=np.float64) * self.unit
        bb = s.bounding_box()
        self.lo = np.array([bb.min.X, bb.min.Y, bb.min.Z], dtype=np.float64)
        self.hi = np.array([bb.max.X, bb.max.Y, bb.max.Z], dtype=np.float64)
        self.planes = []
        self.curved = 0
        for f in s.faces():
            if f.geom_type != bd.GeomType.PLANE:
                self.curved += 1
                continue
            n = f.normal_at()
            normal = np.array([n.X, n.Y, n.Z], dtype=np.float64)
            p = f.center(bd.CenterOf.MASS)
            fb = f.bounding_box()
            self.planes.append(
                PlaneFace(
                    normal,
                    float(normal @ np.array([p.X, p.Y, p.Z], dtype=np.float64)),
                    f,
                    np.array([fb.min.X, fb.min.Y, fb.min.Z], dtype=np.float64),
                    np.array([fb.max.X, fb.max.Y, fb.max.Z], dtype=np.float64),
                )
            )

    @property
    def weight(self) -> float:
        """N: density × g × volume."""
        return self.density * G * self.volume


@dataclass(frozen=True, eq=False)
class Contact:
    """Where blocks ``a`` and ``b`` touch: the contact's points (m), the normal at each from ``a``
    into ``b``, its area (m²), and whether it is planar."""

    a: int
    b: int
    points: FloatArray  # (k, 3)
    normals: FloatArray  # (k, 3), unit
    area: float
    planar: bool


def _shared_unit(blocks: Sequence[Block]) -> float:
    unit = blocks[0].unit
    if any(b.unit != unit for b in blocks):
        raise ValueError("the blocks of one model must share a model unit")
    return unit


def contacts_pairwise(
    blocks: Sequence[Block], tol: float = 2.5e-5, min_area: float = 1e-8
) -> list[Contact]:
    """Every planar contact between the blocks: faces with opposite normals on one plane, the gap
    or overlap between them at most ``tol`` (m), the common area at least ``min_area`` (m²).
    Two fixed blocks are never paired."""
    if not blocks:
        return []
    unit = _shared_unit(blocks)
    t = tol / unit
    lo = np.array([b.lo for b in blocks]) - t
    hi = np.array([b.hi for b in blocks]) + t
    out: list[Contact] = []
    for i in range(len(blocks)):
        near = np.nonzero(np.all((lo[i + 1 :] <= hi[i]) & (hi[i + 1 :] >= lo[i]), axis=1))[0]
        for j in (int(k) + i + 1 for k in near):
            if blocks[i].fixed and blocks[j].fixed:
                continue
            for fa in blocks[i].planes:
                for fb in blocks[j].planes:
                    if float(fa.normal @ fb.normal) > -1.0 + _OPPOSITE:
                        continue
                    gap = -fb.offset - fa.offset  # b's plane lies at n_a · x = -offset_b
                    if abs(gap) > t:
                        continue
                    if np.any(fa.lo - t > fb.hi) or np.any(fb.lo - t > fa.hi):
                        continue
                    moved = fb.face if gap == 0.0 else bd.Pos(*(-gap * fa.normal)) * fb.face
                    common = fa.face & moved
                    if common is None:
                        continue
                    out += _planar(common, i, j, fa.normal, unit, min_area)
    return out


def _planar(
    shape: Any, a: int, b: int, normal: FloatArray, unit: float, min_area: float
) -> list[Contact]:
    out: list[Contact] = []
    for f in shape.faces():
        area = float(f.area) * unit**2
        if area < min_area:
            continue
        pts = np.array([(v.X, v.Y, v.Z) for v in f.vertices()], dtype=np.float64) * unit
        out.append(Contact(a, b, pts, np.tile(normal, (len(pts), 1)), area, True))
    return out


def contacts_fuse(
    blocks: Sequence[Block], fuzzy: float = 0.0, min_area: float = 1e-8, samples: int = 9
) -> list[Contact]:
    """Every face two blocks share, by OpenCascade's General Fuse with glue: planar and curved.
    A curved face is sampled at ``samples`` points along each of its parameters' directions,
    its normal at each oriented out of block ``a``. ``fuzzy`` (m) lets the fuse close a gap."""
    # OpenCascade's Python bindings (OCP) ship no stubs for these names: modules typed as such
    bop = import_module("OCP.BOPAlgo")
    maps = import_module("OCP.collections")
    top_abs = import_module("OCP.TopAbs")
    top_exp = import_module("OCP.TopExp")

    if not blocks:
        return []
    unit = _shared_unit(blocks)
    gf = bop.BOPAlgo_Builder()
    for blk in blocks:
        gf.AddArgument(blk.solid.wrapped)
    gf.SetGlue(bop.BOPAlgo_GlueShift)
    if fuzzy:
        gf.SetFuzzyValue(fuzzy / unit)
    gf.SetRunParallel(False)
    gf.Perform()
    if gf.HasErrors():  # pragma: no cover - OpenCascade's own failure
        raise RuntimeError("OpenCascade's General Fuse failed on these blocks")
    images: list[tuple[Any, int]] = []
    for i, blk in enumerate(blocks):
        mods = gf.Modified(blk.solid.wrapped)
        if mods.Size() == 0:
            images.append((blk.solid.wrapped, i))
        else:
            images += [(mods.First(), i), (mods.Last(), i)]
    fmap = maps.IndexedDataMap_TopoDS_Shape_List_TopoDS_Shape_TopTools_ShapeMapHasher()
    top_exp.TopExp.MapShapesAndAncestors_s(
        gf.Shape(), top_abs.TopAbs_FACE, top_abs.TopAbs_SOLID, fmap
    )

    def owner(s: Any) -> int:
        for img, i in images:
            if img.IsSame(s):
                return i
        raise KeyError("a solid of the fuse wasn't traced to a block")  # pragma: no cover

    out: list[Contact] = []
    for k in range(1, fmap.Extent() + 1):
        anc = fmap.FindFromIndex(k)
        if anc.Size() != 2:
            continue
        a, b = owner(anc.First()), owner(anc.Last())
        if a == b or (blocks[a].fixed and blocks[b].fixed):
            continue
        a, b = min(a, b), max(a, b)
        f = bd.Face(fmap.FindKey(k))
        area = float(f.area) * unit**2
        if area < min_area:
            continue
        if f.geom_type == bd.GeomType.PLANE:
            n = f.normal_at()
            normal = _outward(blocks[a], f, np.array([n.X, n.Y, n.Z], dtype=np.float64))
            out += _planar(f, a, b, normal, unit, 0.0)
            continue
        pts: list[FloatArray] = []
        normals: list[FloatArray] = []
        for u in np.linspace(0.0, 1.0, samples):
            for v in np.linspace(0.0, 1.0, samples):
                p = f.position_at(float(u), float(v))
                n = f.normal_at(float(u), float(v))
                pts.append(np.array([p.X, p.Y, p.Z], dtype=np.float64))
                normals.append(np.array([n.X, n.Y, n.Z], dtype=np.float64))
        normal_a = [_outward(blocks[a], f, n, p) for p, n in zip(pts, normals, strict=True)]
        out.append(Contact(a, b, np.array(pts) * unit, np.array(normal_a), area, False))
    return out


def _outward(block: Block, face: Any, n: FloatArray, at: FloatArray | None = None) -> FloatArray:
    """``n``, turned if need be to point out of ``block`` at ``at`` (the face's centre if None)."""
    if at is None:
        c = face.center(bd.CenterOf.MASS)
        at = np.array([c.X, c.Y, c.Z], dtype=np.float64)
    size = float(np.max(block.hi - block.lo))
    probe = at + 1e-4 * size * n
    inside = bool(block.solid.is_inside(bd.Vector(*probe.tolist())))
    return -n if inside else n
