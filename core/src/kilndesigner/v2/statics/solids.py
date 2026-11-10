"""Cutting the engine's solids into rigid blocks with build123d: boxes, the part of a solid between
two planes, level courses and radial voussoirs. Everything here is in the solids' own model unit
(the engine's millimetres); `blocks.Block` turns a solid into SI.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Any

import build123d as bd

type Vec3 = tuple[float, float, float]


def box(lo: Vec3, hi: Vec3) -> Any:
    """The axis-aligned box between two corners."""
    sx, sy, sz = (b - a for a, b in zip(lo, hi, strict=True))
    cx, cy, cz = ((a + b) / 2 for a, b in zip(lo, hi, strict=True))
    return (bd.Pos(cx, cy, cz) * bd.Box(sx, sy, sz)).solid()


def split(solid: Any, plane: Any) -> list[Any]:
    """The solid's pieces either side of the plane."""
    return [s for piece in solid.split(plane, keep=bd.Keep.BOTH) if piece is not None
            for s in piece.solids()]  # fmt: skip


def fused(solids: Sequence[Any]) -> Any:
    """The solids fused into one."""
    whole = solids[0]
    for s in solids[1:]:
        whole = whole.fuse(s)
    return whole


def between(solid: Any, axis: int, lo: float, hi: float) -> list[Any]:
    """The solid's pieces between the planes ``lo`` and ``hi`` square to ``axis`` (0 x, 1 y)."""
    if axis == 0:  # YZ's normal is +x: TOP keeps x > lo, BOTTOM keeps x < hi
        keep = solid.split(bd.Plane.YZ.offset(lo), keep=bd.Keep.TOP)
        keep = None if keep is None else keep.split(bd.Plane.YZ.offset(hi), keep=bd.Keep.BOTTOM)
    else:  # XZ's normal is −y: BOTTOM keeps y > lo, TOP keeps y < hi
        keep = solid.split(bd.Plane.XZ.offset(-lo), keep=bd.Keep.BOTTOM)
        keep = None if keep is None else keep.split(bd.Plane.XZ.offset(-hi), keep=bd.Keep.TOP)
    return [] if keep is None else list(keep.solids())


def above(solid: Any, z: float) -> list[Any]:
    """The solid's pieces above the level z."""
    keep = solid.split(bd.Plane.XY.offset(z), keep=bd.Keep.TOP)
    return [] if keep is None else list(keep.solids())


def courses(solids: Sequence[Any], levels: Sequence[float]) -> list[Any]:
    """Each solid cut at the level planes (z), lowest piece first."""
    out: list[Any] = []
    rest = list(solids)
    for z in levels:
        above: list[Any] = []
        for piece in (x for s in rest for x in split(s, bd.Plane.XY.offset(z))):
            (out if z > piece.center(bd.CenterOf.MASS).Z else above).append(piece)
        rest = above
    return out + rest


def voussoirs(
    ring: Any, across: int, centre: tuple[float, float], angles: Sequence[float]
) -> list[Any]:
    """The ring cut into voussoirs by planes through its axis at each inner angle. The ring runs
    along the axis square to its plane; ``across`` is its plane's horizontal (0 x, 1 y), ``centre``
    the axis's place in that plane (across, z), and each angle is measured in the plane from the
    +across direction towards +z, the list rising: the first voussoir lies between the first two
    angles. A plane that misses what is left of the ring makes no voussoir."""
    u0, zc = centre
    out: list[Any] = []
    rest = ring
    for a in angles[1:-1]:
        normal = [0.0, 0.0, math.cos(a)]
        normal[across] = -math.sin(a)
        origin = [0.0, 0.0, zc]
        origin[across] = u0
        plane = bd.Plane(origin=(origin[0], origin[1], origin[2]),
                         z_dir=(normal[0], normal[1], normal[2]))  # fmt: skip
        before: list[Any] = []
        after: list[Any] = []
        for piece in split(rest, plane):
            c = piece.center(bd.CenterOf.MASS)
            p = (c.X, c.Y, c.Z)
            side = normal[across] * (p[across] - u0) + normal[2] * (p[2] - zc)
            (before if side < 0 else after).append(piece)
        if before:
            out.append(fused(before))
        if not after:
            return out
        rest = fused(after)
    out.append(rest)
    return out
