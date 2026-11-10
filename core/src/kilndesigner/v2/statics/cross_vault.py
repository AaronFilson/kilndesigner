"""Crossing vaults (roof.crossing) on their walls, cold and hot: a two-way grid of rigid-block
slices cut through the groin solid, coupled where they cross.

The engine's crossing (`groin.py`) is two arched tubes at right angles over one chamber, each as
long as the other is wide: the roof over each point of the plan is the higher of the two vaults,
from the higher intrados to the higher extrados (`GroinLayer`), the groins where they meet, the
walls all round, each tube's end walls filled up to its arch. With crowns at different heights
(both of Olsen's crossings) the lower vault is two lunettes cut into the higher, the groins running
from the corners to the higher vault's side, a case no source read covers (`masonry-statics.md`
M4); cutting the solid itself covers it.

**The slices.** Vertical planes cut the solid both ways: one family across the width (along x,
square to the chamber's own tube) and one along the run (along y, square to the crossing's), each
slice a 2-D chain of voussoirs from wall face to wall face, carrying half its strip's weight and
half the layers' laid over the shell. A voussoir is the slice's section between the roof's intrados
and extrados; its joints are radial to the slice's own tube where that tube is the roof, plumb
where the other is (there the slice runs along the other's generators), none nearer a groin than
1.2 shell thicknesses (a voussoir spans the crease), a 2½ in course apart (Olsen pp.19–20). The
slices end in plumb joints at the walls' inside faces, against the caps filled up to the other
vault. The walls are buttressed, so they are held fixed and their demand computed.

**The coupling.** Where two slices cross they may pass any vertical force between them: the
orthogonal network of the cross diagram, "an orthogonal path to the diagonals and then via the
groins to the supports" (Maia Avelino, Iannuzzo, Van Mele & Block, SAHC 2020 §4.3,
`masonry-statics.md` [M3], section M4; Block & Ochsendorf's thrust networks, [M4]), here in block
form with the walls all round as the supports, the LP choosing how each crossing's load divides.
The two families' compressive stress fields add to one in equilibrium with the vault's weight, and
a sum of compressions is a compression (Derived): so an admissible state of the grid (no tension at
any joint, friction, and hot each family's joints at half the crushing stand-in, so that where the
two add they stay within it, Derived) is a state of the vault, and by the safe theorem it stands
(Heyman 1966). A lower bound: the shell's twisting and in-plane shear aren't counted.

Against fixed walls a flat slice carries load as a flat arch at great thrust, so the number is the
least peak push: the least, over the vault's states, of the largest push any slice puts on its walls
per metre (a min–max LP), what the buttress must give at its most loaded place.
"""

from __future__ import annotations

import bisect
import itertools
import math
from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy import sparse
from scipy.optimize import linprog

from kilndesigner.groin import Tube, tubes
from kilndesigner.model import Kiln, SprungArch
from kilndesigner.units import Q_, si
from kilndesigner.v2.statics import sources
from kilndesigner.v2.statics.blocks import G
from kilndesigner.v2.statics.rigid import Body, Joint, Problem, Section, assemble, force_on
from kilndesigner.v2.statics.section import METHOD, NotModelledError, State
from kilndesigner.working import Step, show

SLICES = 9
"""Slices each way: the Church kiln's least peak push changes 4 % from 5 to 9 and 0.3 % from 9 to
13 (test_statics_cross_vault.py)."""
CREASE = 1.2
"""Shell thicknesses kept clear of a groin by the joints either side of it."""
SAMPLES = 12
"""Points along each voussoir's intrados and extrados."""
END = "wall"

type Point = tuple[float, float]

CROSS = (
    "the cross diagram's orthogonal path (Maia Avelino et al., SAHC 2020 §4.3, masonry-statics.md "
    "[M3], M4) in block form: slices both ways, coupled where they cross"
)


@dataclass(frozen=True)
class Slice:
    """One slice: ``family`` 0 across the width (s = x, at y = ``at``) or 1 along the run (s = y,
    at x = ``at``), its strip ``width`` (m); each voussoir's outline in (s, z), its load (N, half
    its strip's weight with the layers over the shell) and the s that acts at, and the joints
    between them, each from its intrados point to its extrados point."""

    family: int
    at: float
    width: float
    voussoirs: tuple[tuple[Point, ...], ...]
    loads: tuple[tuple[float, float], ...]
    joints: tuple[tuple[Point, Point], ...]


def not_modelled(kiln: Kiln) -> str | None:
    """Why this kiln's crossing vault isn't sliced here, or None."""
    roof, c = kiln.roof, kiln.chamber
    if not isinstance(roof, SprungArch) or roof.crossing is None:
        return "not a crossing vault"
    x = roof.crossing
    if x.at is not None and abs(si(x.at, "m") - si(c.depth, "m") / 2) > 1e-6:
        return "a crossing off the chamber's middle isn't sliced yet"
    if abs(si(x.length, "m") - si(c.width, "m")) > 1e-6:
        return "a crossing tube with arms past the chamber's walls isn't sliced yet"
    if abs(si(x.span, "m") - si(c.depth, "m")) > 1e-6:
        return "a crossing tube narrower or wider than the chamber isn't sliced yet"
    if not roof.buttressed:
        return "a crossing vault held by a frame isn't modelled: no frame holds the caps"
    acting = kiln.lining.for_face("roof")[: roof.acting_ring]
    if len({layer.material for layer in acting}) > 1:
        return "a shell of bonded layers of different materials isn't sliced yet"
    return None


def _area(pts: tuple[Point, ...]) -> tuple[float, float]:
    """A simple polygon's area and its centroid's s (the shoelace formula)."""
    a = cx = 0.0
    for (x0, z0), (x1, z1) in itertools.pairwise((*pts, pts[0])):
        c = x0 * z1 - x1 * z0
        a += c
        cx += (x0 + x1) * c
    return abs(a) / 2, cx / (3 * a)


def _circle(tube: Tube, u: float, out: float) -> float:
    """The tube's circle ``out`` from its inside, ``u`` across from its centreline: its height, or
    -inf where it doesn't reach."""
    under = (tube.radius + out) ** 2 - u * u
    return tube.centre_z + math.sqrt(under) if under > 0 else -math.inf


@dataclass(frozen=True)
class _Vaults:
    main: Tube
    cross: Tube
    shell: float  # m, the acting ring
    over: tuple[tuple[float, float], ...]  # the layers over it: (thickness m, density kg/m³)
    density: float

    @property
    def crown(self) -> float:
        """The higher crown's extrados: nothing of the roof is above it."""
        return max(t.springline + t.rise for t in (self.main, self.cross)) + self.shell

    def top(self, x: float, y: float, out: float = 0.0) -> float:
        """The higher of the two circles ``out`` from the insides, over (x, y)."""
        return max(_circle(self.main, x - self.main.centre, out),
                   _circle(self.cross, y - self.cross.centre, out))  # fmt: skip

    def own(self, family: int, x: float, y: float) -> bool:
        """Whether the slice's own tube is the roof over (x, y)."""
        zm = _circle(self.main, x - self.main.centre, 0.0)
        zc = _circle(self.cross, y - self.cross.centre, 0.0)
        return zm >= zc if family == 0 else zc > zm


def _cut(v: _Vaults, family: int, at: float, width: float) -> Slice:
    tube = v.main if family == 0 else v.cross
    h, t = v.main.springline, v.shell

    def point(s: float) -> Point:
        return (s, at) if family == 0 else (at, s)

    def lower(s: float) -> float:
        return max(v.top(*point(s)), h)

    def upper(s: float, out: float = t) -> float:
        return v.top(*point(s), out)

    def joint(s: float) -> tuple[Point, Point]:
        z0 = lower(s)
        if not v.own(family, *point(s)):
            return (s, z0), (s, upper(s))  # along the other tube's generators: plumb
        dx, dz = s - tube.centre, z0 - tube.centre_z
        n = math.hypot(dx, dz)
        dx, dz = dx / n, dz / n
        lo, hi = 0.0, (v.crown - z0) / dz  # the radius is above the whole roof there
        for _ in range(60):  # where it leaves the shell
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if z0 + mid * dz < upper(s + mid * dx) else (lo, mid)
        return (s, z0), (s + hi * dx, z0 + hi * dz)

    a, b = tube.centre - tube.span / 2, tube.centre + tube.span / 2
    grid = np.linspace(a, b, 2001)
    owns = [v.own(family, *point(float(s))) for s in grid]
    creases = [float(grid[i] + grid[i + 1]) / 2 for i in range(len(grid) - 1)
               if owns[i] != owns[i + 1]]  # fmt: skip
    m = max(2, round((b - a) / sources.COURSE.value))
    stations = [a + (b - a) * j / m for j in range(m + 1)]
    keep = [a, *(s for s in stations[1:-1] if all(abs(s - c) > CREASE * t for c in creases)), b]
    joints = tuple(joint(s) for s in keep)
    outlines: list[tuple[Point, ...]] = []
    loads: list[tuple[float, float]] = []
    for (lo_a, up_a), (lo_b, up_b) in itertools.pairwise(joints):
        below = [(float(s), lower(float(s))) for s in np.linspace(lo_a[0], lo_b[0], SAMPLES)]
        above = [(float(s), upper(float(s))) for s in np.linspace(up_b[0], up_a[0], SAMPLES)]
        outline = (*below, up_b, *above[1:-1], up_a)
        outlines.append(outline)
        area, cs = _area(outline)
        parts = [(v.density * area, cs)]
        rim = t
        for thick, density in v.over:  # the layers laid over the shell: its load
            ss = np.linspace(up_a[0], up_b[0], SAMPLES)
            layer = (*((float(s), upper(float(s), rim)) for s in ss),
                     *((float(s), upper(float(s), rim + thick)) for s in ss[::-1]))  # fmt: skip
            area, cs = _area(layer)
            parts.append((density * area, cs))
            rim += thick
        mass = sum(p for p, _ in parts)
        loads.append((mass * G * width / 2, sum(p * s for p, s in parts) / mass))
    return Slice(family, at, width, tuple(outlines), tuple(loads), joints)


def _vaults(kiln: Kiln) -> _Vaults:
    roof = kiln.roof
    assert isinstance(roof, SprungArch)
    main, cross = tubes(kiln, "m")
    layers = kiln.lining.for_face("roof")
    shell = sum(si(x.thickness, "m") for x in layers[: roof.acting_ring])
    over = tuple((si(x.thickness, "m"), sources.density(x.material))
                 for x in layers[roof.acting_ring :])  # fmt: skip
    return _Vaults(main, cross, shell, over, sources.density(layers[0].material))


def slices(kiln: Kiln, n: int = SLICES) -> list[Slice]:
    """The vault's slices, ``n`` each way, in metres: across the width (each at a y), then along
    the run (each at an x), at the middles of their strips."""
    v = _vaults(kiln)
    out: list[Slice] = []
    for family, other in ((0, v.cross), (1, v.main)):  # the strips run across the other tube
        width = other.span / n
        for k in range(n):
            out.append(_cut(v, family, other.centre - other.span / 2 + (k + 0.5) * width, width))
    return out


def _problem(kiln: Kiln, sl: Slice, state: State, analogy: bool) -> Problem:
    shell = kiln.lining.for_face("roof")[0].material
    bodies = [Body(f"voussoir {k + 1} of the slice at {sl.at:.3f} m", w, (s, 0.0), material=shell)
              for k, (w, s) in enumerate(sl.loads)]  # fmt: skip
    (first, _), (last, _) = sl.joints[0], sl.joints[-1]
    bodies.append(Body("the wall at the low end", 0.0, (first[0] - 0.1, first[1]), True, END))
    bodies.append(Body("the wall at the high end", 0.0, (last[0] + 0.1, last[1]), True, END))
    nv = len(sl.voussoirs)
    joints: list[Joint] = []
    for j, (lo, up) in enumerate(sl.joints):
        ln = math.hypot(up[0] - lo[0], up[1] - lo[1])
        normal = ((up[1] - lo[1]) / ln, (lo[0] - up[0]) / ln)  # to its right going up: on +s
        joints.append(Joint(nv if j == 0 else j - 1, nv + 1 if j == nv else j, (lo, up),
                            (normal, normal), sl.width))  # fmt: skip
    mu = (sources.MU_COLD if state == "cold" else sources.MU_HOT).value
    stand_in = sources.crushing(shell)
    crush: tuple[float | None, ...] = ()
    if state == "hot" and stand_in is not None and (analogy or not sources.by_analogy(shell)):
        crush = (stand_in.value / 2,) * len(joints)  # half each family's
    return Problem(Section(tuple(bodies), tuple(joints), sl.width), (mu,) * len(joints), crush)


def _holding(sl: Slice, s: float) -> int:
    """The voussoir of the slice over s along it."""
    k = bisect.bisect_right([lo[0] for lo, _ in sl.joints], s) - 1
    return min(max(k, 0), len(sl.voussoirs) - 1)


def _grid(kiln: Kiln, sls: list[Slice], state: State, analogy: bool) -> tuple[bool, float]:
    """The grid's LP: every slice's equilibrium and joints, a vertical force passed at each
    crossing, and t ≥ each slice's push per metre of wall, t least: (a state exists, t in N/m)."""
    probs = [_problem(kiln, sl, state, analogy) for sl in sls]
    asms = [assemble(p) for p in probs]
    cols = [0, *itertools.accumulate(a.nvar for a in asms)]
    rows = [0, *itertools.accumulate(len(a.b_eq) for a in asms)]
    across = [k for k, sl in enumerate(sls) if sl.family == 0]
    along = [k for k, sl in enumerate(sls) if sl.family == 1]
    r: list[int] = []
    c: list[int] = []
    v: list[float] = []
    for k, (i, j) in enumerate(itertools.product(across, along)):
        x, y = sls[j].at, sls[i].at  # where they cross
        ri, rj = rows[i] + 3 * _holding(sls[i], x), rows[j] + 3 * _holding(sls[j], y)
        r += [ri + 1, ri + 2, rj + 1, rj + 2]  # up on the slice across, down on the one along
        c += [k] * 4
        v += [1.0, x, -1.0, -y]
    nc = len(across) * len(along)
    extra = nc + 1  # the couplings, then t
    eq: Any = sparse.block_diag([a.a_eq for a in asms], format="csr")
    couple = sparse.csr_array((v, (r, c)), shape=(rows[-1], extra))
    a_eq: Any = sparse.hstack([eq, couple], format="csr")
    pr: list[int] = []
    pc: list[int] = []
    pv: list[float] = []
    for k, (sl, p, a) in enumerate(zip(sls, probs, asms, strict=True)):
        push = force_on(a, p.section, END, 0, outward=True) / sl.width / 2
        for col in np.flatnonzero(push):
            pr.append(k)
            pc.append(cols[k] + int(col))
            pv.append(float(push[col]))
        pr.append(k)
        pc.append(cols[-1] + nc)
        pv.append(-1.0)
    ub: Any = sparse.block_diag([a.a_ub for a in asms], format="csr")
    peak = sparse.csr_array((pv, (pr, pc)), shape=(len(sls), cols[-1] + extra))
    a_ub: Any = sparse.vstack(
        [sparse.hstack([ub, sparse.csr_array((ub.shape[0], extra))]), peak], format="csr"
    )
    b_ub = np.concatenate([*(a.b_ub for a in asms), np.zeros(len(sls))])
    b_eq = np.concatenate([a.b_eq for a in asms])
    bounds: list[tuple[float | None, float | None]] = [
        bound for a in asms for bound in [(0.0, None), (None, None)] * len(a.points)
    ]
    bounds += [(None, None)] * nc + [(0.0, None)]
    cost = np.zeros(cols[-1] + extra)
    cost[-1] = 1.0
    res: Any = linprog(cost, A_ub=a_ub, b_ub=b_ub, A_eq=a_eq, b_eq=b_eq, bounds=bounds,
                       method="highs")  # fmt: skip
    ok = int(res.status) == 0
    return ok, float(res.x[-1]) if ok else math.nan


@dataclass(frozen=True)
class CrossResult:
    """One state of a crossing vault: whether the grid has an admissible state, the least peak
    push on the walls (N per metre of wall), whether a hot verdict rests on a stand-in by analogy,
    and the working."""

    state: State
    stands: bool
    peak: float
    analogy: bool
    steps: tuple[Step, ...]


def analyse(kiln: Kiln, state: State, n: int = SLICES) -> CrossResult:
    why = not_modelled(kiln)
    if why is not None:
        raise NotModelledError(why)
    sls = slices(kiln, n)
    stands, peak = _grid(kiln, sls, state, analogy=True)
    shell = kiln.lining.for_face("roof")[0].material
    analogy = (not stands and state == "hot" and sources.by_analogy(shell)
               and _grid(kiln, sls, state, analogy=False)[0])  # fmt: skip
    return CrossResult(
        state, stands, peak, analogy, _steps(kiln, state, sls, stands, peak, analogy)
    )


def _steps(
    kiln: Kiln, state: State, sls: list[Slice], stands: bool, peak: float, analogy: bool
) -> tuple[Step, ...]:
    roof = kiln.roof
    assert isinstance(roof, SprungArch)
    assert roof.crossing is not None
    mu = sources.MU_COLD if state == "cold" else sources.MU_HOT
    n = len(sls) // 2
    steps = [
        Step(
            name=f"The crossing vault in slices both ways ({state})",
            value=f"{n} slices each way, {sum(len(s.voussoirs) for s in sls)} voussoirs, coupled "
            f"at {n * n} crossings: " + ("an admissible state" if stands else "none"),
            formula="each slice the groin solid's section between the higher intrados and "
            "extrados; joints radial to its own tube, plumb across the other's; each family half "
            "its strip's weight, any vertical force passed where two slices cross",
            inputs={
                "rises": f"{show(roof.rise, 'inch')}, {show(roof.crossing.rise, 'inch')}",
                "μ": f"{mu.value}",
            },
            reference=f"{CROSS}; {METHOD}",
            note=mu.note,
        )
    ]
    if stands:
        steps.append(Step(
            name=f"The least peak push on the walls ({state})",
            value=f"{peak:.4g} N/m ({si(Q_(peak, 'N/m'), 'lbf/ft'):.4g} lbf/ft) of wall",
            formula="minimise t, every slice's push on its walls per metre at most t: what the "
            "buttress must give at its most loaded place",
            reference=METHOD,
        ))  # fmt: skip
    if analogy:
        steps.append(Step(
            name="The hot verdict rests on a stand-in by analogy",
            value="no admissible state with dense firebrick's 25 psi crushing stand-in, one "
            "without it: not given (ADR 0009)",
            reference=sources.C16_DENSE.reference,
            note=sources.C16_DENSE.note,
        ))  # fmt: skip
    return tuple(steps)
