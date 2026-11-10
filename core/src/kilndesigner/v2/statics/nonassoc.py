"""Non-associative friction: the least collapse load of a course-level model, as a mixed-integer
linear program on HiGHS (`scipy.optimize.milp`).

The linear program in `rigid.py` treats friction as associative: a joint that slides also opens.
Real masonry joints slide without opening, and where sliding governs an indeterminate assembly
the true collapse load can be lower than the LP's (`docs/research/statics-combinations.md` §3:
a buttress dry-laid against a wall collapses at 2.245 kN/m against the LP's 2.939).

The non-associative collapse load is the least load factor λ at which a statically admissible
force field and a mechanism exist together, each joint point in one mode (Ferris and Tin-Loi
2001, Int. J. Mech. Sci. 43, 209–224, Eq. 10, a program with complementarity constraints; read):

- open:      N = T = 0, δn ≥ 0, δt free;
- sticking:  |T| ≤ μN, δn = 0, δt = 0;
- sliding +: T = −μN, δn = 0, δt ≥ 0;   sliding −: T = +μN, δn = 0, δt ≤ 0.

δ is the relative velocity of block b over block a at the point (the transpose of the
equilibrium matrix applied to the blocks' velocities, by virtual work); the mechanism is
normalised by the live load's work, 1. Three binaries a point choose its mode (none set:
sticking), with big-M bounds: N's by LP bound tightening over the admissible fields with
0 ≤ λ ≤ λ_LP, the velocities' by a box on the blocks' velocities, reported if it binds. HiGHS's
branch and cut proves the least value for models of tens of blocks; the mode pattern found is
then solved again as two plain LPs (statics with the modes' force equalities, kinematics with
their velocity signs), which removes the big-M round-off. The probe
(`scratch/statics-combos/friction/nonassoc_milp.py`) checked case C by brute force over all
4,096 mode patterns.

For brick-level models the search may not finish: the best collapse state found is then an upper
bound on the least, and HiGHS's dual bound a lower one; both are reported.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Any

import numpy as np
import numpy.typing as npt
from scipy import sparse
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

from kilndesigner.v2.statics.rigid import Problem, Status, assemble, solve

type FloatArray = npt.NDArray[np.float64]

MAX_BINARIES = 600
"""Above this, a model isn't course-level: refused (case C2's 288 binaries took 300 s to find a
state and didn't prove it least in 1,163 s; statics-combinations.md §3)."""


class Mode(Enum):
    OPEN = "open"
    STICK = "sticking"
    SLIDE_PLUS = "sliding +"
    SLIDE_MINUS = "sliding −"


@dataclass(frozen=True)
class Collapse:
    """The least non-associative collapse load factor against the LP's, with the mechanism.

    ``least`` is proven when ``proven``; otherwise ``least`` is the best collapse state found (an
    upper bound) and ``bound`` HiGHS's dual bound (a lower one)."""

    lp: float
    least: float
    bound: float
    proven: bool
    modes: tuple[Mode, ...]
    velocities: FloatArray | None
    forces: FloatArray | None
    box_used: float  # the largest block velocity over the box: 1 means the box binds
    binaries: int
    message: str


class TooLargeError(ValueError):
    """The model has more binaries than a course-level model: the least isn't searched."""


def collapse(
    p: Problem, box: float = 10.0, time_limit: float = 120.0, gap: float = 1e-9
) -> Collapse:
    """The least load factor at which the problem's live load collapses it, with non-associative
    friction. ``p`` must have a live load; a joint with μ = ∞ can't slide."""
    if not p.live:
        raise ValueError("a collapse load needs a live load to factor")
    asm = assemble(p)
    nv = len(asm.points)
    if 3 * nv > MAX_BINARIES:
        raise TooLargeError(
            f"{3 * nv} binaries: more than a course-level model's {MAX_BINARIES}; the least "
            "non-associative load isn't searched (the LP's stands as an upper bound)"
        )
    lp_sol = solve(p, _lam(asm.nvar), -1)
    if lp_sol.status is not Status.OPTIMAL:
        raise ValueError(f"the associative LP has no finite collapse load: {lp_sol.status.value}")
    lam_lp = lp_sol.value
    lam_hi = lam_lp * (1 + 1e-7) + 1e-9
    m_n = _n_bounds(p, lam_hi) * (1 + 1e-6) + 1e-6
    a = asm.a_eq.toarray()
    nb = a.shape[0] // 3
    mus = np.array([p.mu[j] for j, *_ in asm.points])
    slides = ~np.isinf(mus)
    mu0 = np.where(slides, mus, 0.0)
    m_s = 2.0 * mu0 * m_n
    m_v = np.array([2.0 * box * (1.0 + abs(x) + abs(z)) for _, x, z, _, _ in asm.points])
    # variables: f (2nv), λ, U (3nb), δ (2nv), o, p, m (nv each)
    i_lam = 2 * nv
    i_u = i_lam + 1
    i_d = i_u + 3 * nb
    i_o = i_d + 2 * nv
    i_p, i_m = i_o + nv, i_o + 2 * nv
    n = i_m + nv
    rows: list[int] = []
    cols: list[int] = []
    vals: list[float] = []
    lo: list[float] = []
    hi: list[float] = []

    def add(entries: list[tuple[int, float]], a_lo: float, a_hi: float) -> None:
        r = len(lo)
        for c, v in entries:
            rows.append(r)
            cols.append(c)
            vals.append(v)
        lo.append(a_lo)
        hi.append(a_hi)

    for i in range(3 * nb):  # equilibrium
        ent = [(j, a[i, j]) for j in range(2 * nv) if a[i, j] != 0.0]
        if a[i, -1] != 0.0:
            ent.append((i_lam, a[i, -1]))
        add(ent, float(asm.b_eq[i]), float(asm.b_eq[i]))
    for v in range(nv):  # Coulomb
        if slides[v]:
            add([(2 * v + 1, 1.0), (2 * v, -mu0[v])], -np.inf, 0.0)
            add([(2 * v + 1, -1.0), (2 * v, -mu0[v])], -np.inf, 0.0)
    for j in range(2 * nv):  # kinematics, by virtual work: δ_j = Σ_i A[i, j] U_i
        ent = [(i_d + j, 1.0)] + [(i_u + i, -a[i, j]) for i in range(3 * nb) if a[i, j] != 0.0]
        add(ent, 0.0, 0.0)
    add([(i_u + i, a[i, -1]) for i in range(3 * nb) if a[i, -1] != 0.0], 1.0, 1.0)
    for v in range(nv):  # each point's mode
        nn, tt, dn, dt = 2 * v, 2 * v + 1, i_d + 2 * v, i_d + 2 * v + 1
        o, pp, mm = i_o + v, i_p + v, i_m + v
        add([(nn, 1.0), (o, m_n[v])], -np.inf, m_n[v])  # open: N = 0
        add([(dn, 1.0), (o, -m_v[v])], -np.inf, 0.0)  # closed unless open: δn = 0
        add([(dt, 1.0), (o, -m_v[v]), (pp, -m_v[v])], -np.inf, 0.0)
        add([(dt, -1.0), (o, -m_v[v]), (mm, -m_v[v])], -np.inf, 0.0)
        if slides[v]:
            add([(tt, 1.0), (nn, mu0[v]), (pp, m_s[v])], -np.inf, m_s[v])  # T = −μN sliding +
            add([(nn, mu0[v]), (tt, -1.0), (mm, m_s[v])], -np.inf, m_s[v])  # T = +μN sliding −
        add([(o, 1.0), (pp, 1.0), (mm, 1.0)], -np.inf, 1.0)
    lb, ub = np.zeros(n), np.zeros(n)
    lb[i_o:], ub[i_o:] = 0.0, 1.0
    for v in range(nv):
        lb[2 * v], ub[2 * v] = 0.0, m_n[v]
        tb = mu0[v] * m_n[v] if slides[v] else np.inf
        lb[2 * v + 1], ub[2 * v + 1] = -tb, tb
        lb[i_d + 2 * v], ub[i_d + 2 * v] = 0.0, m_v[v]
        lb[i_d + 2 * v + 1], ub[i_d + 2 * v + 1] = -m_v[v], m_v[v]
        if not slides[v]:
            ub[i_p + v] = ub[i_m + v] = 0.0
    lb[i_lam], ub[i_lam] = 0.0, lam_hi
    lb[i_u:i_d], ub[i_u:i_d] = -box, box
    integrality = np.zeros(n)
    integrality[i_o:] = 1
    cost = np.zeros(n)
    cost[i_lam] = 1.0
    bounds: Any = Bounds  # SciPy's stubs type its bounds as floats; arrays are what it takes
    constraint: Any = LinearConstraint
    res: Any = milp(
        cost,
        integrality=integrality,
        bounds=bounds(lb, ub),
        constraints=constraint(
            sparse.csr_array((vals, (rows, cols)), shape=(len(lo), n)), np.array(lo), np.array(hi)
        ),
        options={"time_limit": time_limit, "mip_rel_gap": gap},
    )
    if res.x is None:
        return Collapse(lam_lp, lam_lp, float(getattr(res, "mip_dual_bound", 0.0) or 0.0), False,
                        (), None, None, math.nan, 3 * nv, str(res.message))  # fmt: skip
    x = np.asarray(res.x, dtype=np.float64)
    modes = tuple(
        Mode.OPEN if x[i_o + v] > 0.5
        else Mode.SLIDE_PLUS if x[i_p + v] > 0.5
        else Mode.SLIDE_MINUS if x[i_m + v] > 0.5
        else Mode.STICK
        for v in range(nv)
    )  # fmt: skip
    found = float(x[i_lam])
    forces, velocities = x[:i_lam], x[i_u:i_d]
    polished = _polish(p, asm.a_eq.toarray(), asm.b_eq, modes, lam_hi)
    if polished is not None:
        found, forces, velocities = polished
    proven = int(res.status) == 0
    bound = found if proven else float(getattr(res, "mip_dual_bound", 0.0) or 0.0)
    return Collapse(lam_lp, found, bound, proven, modes, velocities, forces,
                    float(np.max(np.abs(x[i_u:i_d])) / box), 3 * nv, str(res.message))  # fmt: skip


def _lam(nvar: int) -> FloatArray:
    c = np.zeros(nvar)
    c[-1] = 1.0
    return c


def _n_bounds(p: Problem, lam_hi: float) -> FloatArray:
    """Each point's largest normal force over the statically admissible fields, 0 ≤ λ ≤ λ_LP."""
    asm = assemble(p)
    out = np.empty(len(asm.points))
    for v in range(len(asm.points)):
        c = np.zeros(asm.nvar)
        c[2 * v] = 1.0
        sol = solve(p, c, -1, live_bounds=(0.0, lam_hi))
        out[v] = sol.value
    return out


def _polish(
    p: Problem, a: FloatArray, b: FloatArray, modes: tuple[Mode, ...], lam_hi: float
) -> tuple[float, FloatArray, FloatArray] | None:
    """The mode pattern as two exact LPs: the least λ with the modes' force equalities, and a
    mechanism with their velocity signs. None if either fails (the MILP's own values stand)."""
    asm = assemble(p)
    nv = len(asm.points)
    bounds: list[tuple[float | None, float | None]] = [(0.0, None), (None, None)] * nv
    bounds.append((0.0, lam_hi))
    eq_rows: list[FloatArray] = []
    for v, md in enumerate(modes):
        if md is Mode.OPEN:
            bounds[2 * v] = (0.0, 0.0)
        elif md in (Mode.SLIDE_PLUS, Mode.SLIDE_MINUS):
            r = np.zeros(asm.nvar)
            r[2 * v + 1] = 1.0
            mu = p.mu[asm.points[v][0]]
            r[2 * v] = mu if md is Mode.SLIDE_PLUS else -mu  # T + μN = 0, or T − μN = 0
            eq_rows.append(r)
    a_eq = np.vstack([a, *eq_rows]) if eq_rows else a
    b_eq = np.concatenate([b, np.zeros(len(eq_rows))])
    statics: Any = linprog(_lam(asm.nvar), A_ub=asm.a_ub if asm.b_ub.size else None,
                           b_ub=asm.b_ub if asm.b_ub.size else None, A_eq=a_eq, b_eq=b_eq,
                           bounds=bounds, method="highs")  # fmt: skip
    k = a[:, :-1].T  # δ = K U
    e_lam = a[:, -1]
    ub_rows: list[FloatArray] = []
    eq_k: list[FloatArray] = [e_lam]
    eq_b = [1.0]
    for v, md in enumerate(modes):
        kn, kt = k[2 * v], k[2 * v + 1]
        if md is Mode.OPEN:
            ub_rows.append(-kn)
            continue
        eq_k.append(kn)
        eq_b.append(0.0)
        if md is Mode.STICK:
            eq_k.append(kt)
            eq_b.append(0.0)
        else:
            ub_rows.append(-kt if md is Mode.SLIDE_PLUS else kt)
    kinematics: Any = linprog(np.zeros(a.shape[0]),
                              A_ub=np.array(ub_rows) if ub_rows else None,
                              b_ub=np.zeros(len(ub_rows)) if ub_rows else None,
                              A_eq=np.array(eq_k), b_eq=np.array(eq_b), bounds=(None, None),
                              method="highs")  # fmt: skip
    if int(statics.status) != 0 or int(kinematics.status) != 0:
        return None
    x = np.asarray(statics.x, dtype=np.float64)
    return float(x[-1]), x[:-1], np.asarray(kinematics.x, dtype=np.float64)
