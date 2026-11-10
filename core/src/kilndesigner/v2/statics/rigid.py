"""Rigid-block limit analysis of a section: the static (lower-bound) linear program, on HiGHS.

A section is a slice through the masonry, a set of blocks in the x–z plane (x across, z up) with
the joints between them. Each free block is in equilibrium under its weight, its loads and the
forces at its joints: three equations a block. At each point of a joint there is a normal force
N ≥ 0 (no tension across a joint, Heyman's first assumption) and a shear T with |T| ≤ μN
(Coulomb friction, no cohesion). A planar joint carries its forces at its two ends, so its
resultant can act anywhere across the joint and nowhere outside it. This is the static method of
rigid-block limit analysis (Livesley 1978, from memory; the associative problem of Ferris and
Tin-Loi 2001, Int. J. Mech. Sci. 43, 209–224, read; `docs/research/statics-software.md` §11, where
the formulation reproduced the analytic least thickness of a semicircle).

Any force field this program finds is in equilibrium and violates no joint's conditions, so by
the safe theorem the section stands (Heyman 1966). Two caveats carried into every result:

- **Associative friction.** The program lets a sliding joint open too. Where sliding governs an
  indeterminate assembly, the true collapse load can be lower (statics-combinations.md §3, case C:
  −23.6 %); `nonassoc.py` gives the least non-associative value for course-level models.
- **Crushing** is unlimited unless a joint has a crushing stress: then its resultant must leave
  room for a uniform stress block of that stress inside the joint (`crushing.py`, the hot stand-in).

Units: SI floats throughout (N, m, Pa). A section's forces are the slice's; divide by its depth for
forces per metre run.
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any

import numpy as np
import numpy.typing as npt
from scipy import sparse
from scipy.optimize import linprog

from kilndesigner.v2.statics.blocks import Block, Contact

type FloatArray = npt.NDArray[np.float64]

CRUSH_PIECES = 16
"""Chords inscribed in the crushing parabola (an inner approximation, on the safe side: the end
force it asks for is at most 1/(4·16²) = 0.1 % of the joint's crushing load above the exact one)."""


@dataclass(frozen=True)
class Body:
    """A block in the section: its weight (N), the x–z centroid it acts at (m), how it is held,
    and any loads besides its weight, as (x, z, Fx, Fz) in m and N."""

    name: str
    weight: float
    centroid: tuple[float, float]
    fixed: bool = False
    tag: str = ""
    material: str | None = None
    loads: tuple[tuple[float, float, float, float], ...] = ()


@dataclass(frozen=True)
class Joint:
    """A contact in the section between bodies ``a`` and ``b``: its points (x, z, m), the unit
    normal at each from ``a`` into ``b``, and its depth across the section (m). A planar joint has
    two points, its ends."""

    a: int
    b: int
    points: tuple[tuple[float, float], ...]
    normals: tuple[tuple[float, float], ...]
    depth: float
    planar: bool = True

    @property
    def length(self) -> float:
        """m, end to end in the section (a curved joint: along its points)."""
        p = np.array(self.points)
        return float(np.sum(np.hypot(*np.diff(p, axis=0).T)))

    @property
    def middle(self) -> tuple[float, float]:
        p = np.array(self.points)
        return float(p[:, 0].mean()), float(p[:, 1].mean())


@dataclass(frozen=True)
class Section:
    """Bodies and joints in the x–z plane, a slice ``depth`` m thick."""

    bodies: tuple[Body, ...]
    joints: tuple[Joint, ...]
    depth: float

    def tagged(self, tag: str) -> list[int]:
        return [i for i, b in enumerate(self.bodies) if b.tag == tag]

    def without(self, tags: set[str]) -> Section:
        """The section with the bodies of these tags, and their joints, taken out."""
        keep = [i for i, b in enumerate(self.bodies) if b.tag not in tags]
        new = {old: k for k, old in enumerate(keep)}
        joints = tuple(
            replace(j, a=new[j.a], b=new[j.b]) for j in self.joints if j.a in new and j.b in new
        )
        return Section(tuple(self.bodies[i] for i in keep), joints, self.depth)


def section_from_blocks(
    blocks: Sequence[Block], contacts: Sequence[Contact], depth: float | None = None
) -> Section:
    """A section from blocks that are prisms along y and their contacts: each contact with its
    normals in the x–z plane becomes a joint; a planar one keeps the two ends of its polygon, a
    curved one its sampled points in order along it. ``depth`` (m) defaults to the blocks' extent
    along y."""
    bodies = tuple(
        Body(
            b.name,
            b.weight,
            (float(b.centroid[0]), float(b.centroid[2])),
            b.fixed,
            b.tag,
            b.material,
            tuple((ld.point[0], ld.point[2], ld.force[0], ld.force[2]) for ld in b.loads),
        )
        for b in blocks
    )
    if depth is None:
        lo = min(float(b.lo[1]) for b in blocks) * blocks[0].unit
        hi = max(float(b.hi[1]) for b in blocks) * blocks[0].unit
        depth = hi - lo
    joints: list[Joint] = []
    for c in contacts:
        n2 = c.normals[:, [0, 2]]
        if np.any(np.abs(c.normals[:, 1]) > 1e-6):
            continue  # a face across the slice
        pts = c.points[:, [0, 2]]
        if c.planar:
            n = n2[0] / float(np.linalg.norm(n2[0]))
            t = np.array([-n[1], n[0]])
            s = pts @ t
            ends = (pts[int(np.argmin(s))], pts[int(np.argmax(s))])
            length = float(np.max(s) - np.min(s))  # > 0: a face with area, its normal in-plane
            joints.append(
                Joint(
                    c.a,
                    c.b,
                    tuple((float(p[0]), float(p[1])) for p in ends),
                    ((float(n[0]), float(n[1])),) * 2,
                    c.area / length,
                )
            )
            continue
        # a curved contact: its distinct points in the section, in order along it
        keyed: dict[tuple[float, float], FloatArray] = {}
        for p, n in zip(pts, n2, strict=True):
            keyed.setdefault((round(float(p[0]), 9), round(float(p[1]), 9)), n)
        order = _along(np.array(list(keyed)))
        ps = [list(keyed)[k] for k in order]
        ns = [keyed[p] / float(np.linalg.norm(keyed[p])) for p in ps]
        joint = Joint(
            c.a,
            c.b,
            tuple(ps),
            tuple((float(n[0]), float(n[1])) for n in ns),
            1.0,
            planar=False,
        )
        joints.append(replace(joint, depth=c.area / joint.length))
    return Section(bodies, tuple(joints), depth)


def _along(p: FloatArray) -> list[int]:
    """Indices of points ordered along the curve they lie on: start at one end (the point
    farthest from the centroid) and walk to the nearest unvisited point."""
    rest = list(range(len(p)))
    k = max(rest, key=lambda i: float(np.linalg.norm(p[i] - p.mean(axis=0))))
    order = [k]
    rest.remove(k)
    while rest:
        k = min(rest, key=lambda i: float(np.linalg.norm(p[i] - p[order[-1]])))
        order.append(k)
        rest.remove(k)
    return order


class Status(Enum):
    """What HiGHS reports: a state was found, none exists, or the objective has no bound."""

    OPTIMAL = "optimal"
    INFEASIBLE = "infeasible"
    UNBOUNDED = "unbounded"
    FAILED = "failed"


@dataclass(frozen=True)
class Problem:
    """A section and the conditions at its joints.

    - ``mu``: each joint's friction coefficient (``math.inf``: it can't slide).
    - ``crush``: each joint's crushing stress, Pa, or None (unlimited compression).
    - ``live``: loads multiplied by the load factor λ, as (body, x, z, Fx, Fz).
    - ``shrink``: each planar joint's width divided by this about its middle, the search behind
      Heyman's geometric factor of safety (1: the joints as built).
    """

    section: Section
    mu: tuple[float, ...]
    crush: tuple[float | None, ...] = ()
    live: tuple[tuple[int, float, float, float, float], ...] = ()
    shrink: float = 1.0

    def __post_init__(self) -> None:
        n = len(self.section.joints)
        if len(self.mu) != n:
            raise ValueError(f"a friction coefficient for each of the {n} joints")
        if self.crush and len(self.crush) != n:
            raise ValueError(f"a crushing stress (or None) for each of the {n} joints")
        if self.shrink < 1.0:
            raise ValueError("the joints can only be shrunk (shrink ≥ 1)")


@dataclass(frozen=True)
class Assembly:
    """The linear program's matrices: x = [N₀, T₀, N₁, T₁, …, λ?]."""

    a_eq: sparse.csr_array
    b_eq: FloatArray
    a_ub: sparse.csr_array
    b_ub: FloatArray
    points: list[tuple[int, float, float, float, float]]  # (joint, x, z, nx, nz)
    first: list[int]  # each joint's first point
    nvar: int
    has_live: bool


def assemble(p: Problem) -> Assembly:
    sec = p.section
    free = {i: k for k, i in enumerate(i for i, b in enumerate(sec.bodies) if not b.fixed)}
    points: list[tuple[int, float, float, float, float]] = []
    first: list[int] = []
    for j, jt in enumerate(sec.joints):
        first.append(len(points))
        pts = _shrunk(jt, p.shrink)
        for (x, z), (nx, nz) in zip(pts, jt.normals, strict=True):
            points.append((j, x, z, nx, nz))
    has_live = bool(p.live)
    nvar = 2 * len(points) + (1 if has_live else 0)
    rows: list[int] = []
    cols: list[int] = []
    vals: list[float] = []

    def add(body: int, col: int, x: float, z: float, fx: float, fz: float) -> None:
        r = 3 * free[body]
        rows.extend((r, r + 1, r + 2))
        cols.extend((col, col, col))
        vals.extend((fx, fz, x * fz - z * fx))

    for k, (j, x, z, nx, nz) in enumerate(points):
        jt = sec.joints[j]
        for col, (dx, dz) in ((2 * k, (nx, nz)), (2 * k + 1, (-nz, nx))):
            if jt.b in free:
                add(jt.b, col, x, z, dx, dz)  # on b: along the normal from a into b
            if jt.a in free:
                add(jt.a, col, x, z, -dx, -dz)
    b_eq = np.zeros(3 * len(free))
    for i, r in free.items():
        body = sec.bodies[i]
        cx, _ = body.centroid
        b_eq[3 * r + 1] += body.weight  # A x + (0, −W, −x W) = 0
        b_eq[3 * r + 2] += cx * body.weight
        for x, z, fx, fz in body.loads:
            b_eq[3 * r] -= fx
            b_eq[3 * r + 1] -= fz
            b_eq[3 * r + 2] -= x * fz - z * fx
    if has_live:
        for body, x, z, fx, fz in p.live:
            if body in free:
                add(body, nvar - 1, x, z, fx, fz)
    a_eq = sparse.csr_array((vals, (rows, cols)), shape=(3 * len(free), nvar))

    urows: list[int] = []
    ucols: list[int] = []
    uvals: list[float] = []
    ub: list[float] = []

    def row(entries: list[tuple[int, float]], bound: float) -> None:
        r = len(ub)
        for c, v in entries:
            urows.append(r)
            ucols.append(c)
            uvals.append(v)
        ub.append(bound)

    for k, (j, *_) in enumerate(points):
        mu = p.mu[j]
        if math.isinf(mu):
            continue
        row([(2 * k + 1, 1.0), (2 * k, -mu)], 0.0)  # T − μN ≤ 0
        row([(2 * k + 1, -1.0), (2 * k, -mu)], 0.0)  # −T − μN ≤ 0
    for j, sigma in enumerate(p.crush):
        jt = sec.joints[j]
        if sigma is None or not jt.planar:
            continue
        k1, k2 = first[j], first[j] + 1
        b = jt.length / p.shrink
        n_max = sigma * b * jt.depth  # the whole joint at the crushing stress
        c = 2.0 * n_max  # 2σbd: an end's force must be at least N²/(2σbd)
        row([(2 * k1, 1.0), (2 * k2, 1.0)], n_max)
        breaks = [float(x) for x in np.linspace(0.0, n_max, CRUSH_PIECES + 1)]
        for lo, hi in itertools.pairwise(breaks):
            slope = (lo + hi) / c
            for end in (k1, k2):  # each end's force ≥ the chord under N²/(2σbd)
                row([(2 * k1, slope), (2 * k2, slope), (2 * end, -1.0)], lo * hi / c)
    a_ub = sparse.csr_array((uvals, (urows, ucols)), shape=(len(ub), nvar))
    return Assembly(a_eq, b_eq, a_ub, np.array(ub), points, first, nvar, has_live)


def _shrunk(jt: Joint, shrink: float) -> tuple[tuple[float, float], ...]:
    if shrink == 1.0 or not jt.planar:
        return jt.points
    (x0, z0), (x1, z1) = jt.points
    mx, mz = (x0 + x1) / 2, (z0 + z1) / 2
    return (
        (mx + (x0 - mx) / shrink, mz + (z0 - mz) / shrink),
        (mx + (x1 - mx) / shrink, mz + (z1 - mz) / shrink),
    )


@dataclass(frozen=True)
class JointState:
    """One joint in a solution: the normal and shear forces on ``b`` (N, the slice's), where the
    resultant acts across the joint (``e``: from its middle, as a share of its width, −½ to ½;
    + toward the joint's second point), and the friction it uses, |T|/N."""

    joint: int
    a: str
    b: str
    n: float
    t: float
    e: float
    t_over_n: float
    mu: float


@dataclass(frozen=True)
class Solution:
    status: Status
    value: float  # the objective, as asked (math.inf or math.nan when there is none)
    x: FloatArray | None
    assembly: Assembly
    problem: Problem
    message: str
    joints: list[JointState] = field(default_factory=list[JointState])

    @property
    def load_factor(self) -> float | None:
        if self.x is None or not self.assembly.has_live:
            return None
        return float(self.x[-1])


def solve(
    p: Problem,
    cost: FloatArray | None = None,
    sense: int = 1,
    live_bounds: tuple[float, float] | None = None,
) -> Solution:
    """Minimise (``sense`` 1) or maximise (−1) ``cost`` · x over the admissible states; with no
    cost, find any admissible state. ``live_bounds`` bounds the load factor (default λ ≥ 0)."""
    asm = assemble(p)
    if asm.nvar == 0:  # no joints: only weightless, unloaded bodies are in equilibrium
        ok = not np.any(asm.b_eq)
        status = Status.OPTIMAL if ok else Status.INFEASIBLE
        return Solution(status, 0.0 if ok else math.nan, np.zeros(0) if ok else None, asm, p,
                        "no joints")  # fmt: skip
    c = np.zeros(asm.nvar) if cost is None else sense * np.asarray(cost, dtype=np.float64)
    bounds: list[tuple[float | None, float | None]] = [(0.0, None), (None, None)] * len(asm.points)
    if asm.has_live:
        bounds.append(live_bounds if live_bounds is not None else (0.0, None))
    res: Any = linprog(
        c,
        A_ub=asm.a_ub if asm.b_ub.size else None,
        b_ub=asm.b_ub if asm.b_ub.size else None,
        A_eq=asm.a_eq,
        b_eq=asm.b_eq,
        bounds=bounds,
        method="highs",
    )
    status = {0: Status.OPTIMAL, 2: Status.INFEASIBLE, 3: Status.UNBOUNDED}.get(
        int(res.status), Status.FAILED
    )
    if status is not Status.OPTIMAL:
        value = math.inf if status is Status.UNBOUNDED else math.nan
        return Solution(status, value, None, asm, p, str(res.message))
    x = np.asarray(res.x, dtype=np.float64)
    return Solution(status, sense * float(res.fun), x, asm, p, str(res.message), states(p, asm, x))


def states(p: Problem, asm: Assembly, x: FloatArray) -> list[JointState]:
    sec = p.section
    out: list[JointState] = []
    for j, jt in enumerate(sec.joints):
        k0 = asm.first[j]
        ks = range(k0, k0 + len(jt.points))
        n = float(sum(x[2 * k] for k in ks))
        t = float(sum(x[2 * k + 1] for k in ks))
        e = math.nan
        if jt.planar and n > 0:
            n2 = float(x[2 * (k0 + 1)])
            e = (n2 / n - 0.5) / p.shrink  # the resultant's place across the as-built joint
        out.append(
            JointState(
                j,
                sec.bodies[jt.a].name,
                sec.bodies[jt.b].name,
                n,
                t,
                e,
                abs(t) / n if n > 0 else math.nan,
                p.mu[j],
            )
        )
    return out


def force_on(
    asm: Assembly, section: Section, tag: str, axis: int, outward: bool = False
) -> FloatArray:
    """A cost vector: the total force the joints exert on the bodies tagged ``tag``, its x
    (``axis`` 0) or z (1) component. ``outward``: each body's x component signed away from x = 0
    (a support on the right pushed to +x, one on the left to −x, both count positive)."""
    c = np.zeros(asm.nvar)
    for k, (j, _, _, nx, nz) in enumerate(asm.points):
        jt = section.joints[j]
        for body, sgn in ((jt.b, 1.0), (jt.a, -1.0)):
            if section.bodies[body].tag != tag:
                continue
            side = 1.0
            if outward:
                side = 1.0 if section.bodies[body].centroid[0] >= 0 else -1.0
            dn = (nx, nz)[axis]
            dt = (-nz, nx)[axis]
            c[2 * k] += sgn * dn * side
            c[2 * k + 1] += sgn * dt * side
    return c


def geometric_factor(p: Problem, lo: float = 1.0, hi: float = 64.0, tol: float = 1e-4) -> float:
    """Heyman's geometric factor of safety: the most the joints can be shrunk about their middles
    with an admissible state still found (1 if none is found as built: then 0 is returned)."""
    if solve(p).status is not Status.OPTIMAL:
        return 0.0
    if solve(replace(p, shrink=hi)).status is Status.OPTIMAL:
        return hi
    while hi / lo > 1 + tol:
        mid = math.sqrt(lo * hi)
        if solve(replace(p, shrink=mid)).status is Status.OPTIMAL:
            lo = mid
        else:
            hi = mid
    return lo
