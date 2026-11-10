"""The ground under a grounded floor (ADR 0017 H9): transient conduction in the soil, 2-D
axisymmetric, by scikit-fem (`thermal-software.md` §4.2): the floor as the disc of its own area on
the soil's surface, held at the floor's outer face's temperature; the soil round the disc
adiabatic (Incropera Table 4.1 case 10's assumption); the far sides held at the room's temperature.

The r-weighted forms of the heat equation on P1 triangles over a graded r–z mesh, the mass lumped
(row sums: each node's own soil, so the disc's soil is the floor's outer face's capacity and no
rate couples two nodes). As DAE rows, with u the free nodes and T_d the disc's temperature:

    2π (M_u u′ + K_uu u + K_ud T_d + K_uf T_far) = 0,
    Q_ground = 2π Σ_disc (K T + M T′)   (the heat the floor gives the soil).

The soil: dry mineral soil, k 1.0 W/(m·K), ρ 1500 kg/m³, c 1840 J/(kg·K) (Lienhard Table A.2, via
`thermal-properties.md` §8.2), as v1 takes it (soil under a hot floor dries out); damp clay or silt,
1.5 W/(m·K) (DIN EN 12524 via ht), the other end of the band. k(T) of hot soil isn't sourced.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from numpy.typing import NDArray
from skfem import (  # pyright: ignore[reportMissingTypeStubs]
    Basis,
    BilinearForm,
    ElementTriP1,
    MeshTri,
    asm,
)
from skfem.helpers import dot  # pyright: ignore[reportMissingTypeStubs]

type Vector = NDArray[np.float64]

SOURCE = (
    "scikit-fem 12 (P1, axisymmetric r-weighted forms; thermal-software.md §4.2); Incropera "
    "Table 4.1 case 10 (a disc on an adiabatic half-space, S = 2D) and the semi-infinite solid as "
    "its limits (thermal-properties.md §8)"
)


@dataclass(frozen=True)
class Soil:
    k: float
    rho: float
    c: float
    reference: str


DRY = Soil(
    1.0, 1500.0, 1840.0, "Lienhard Table A.2, soil (mineral), dry (thermal-properties.md §8.2)"
)
DAMP = Soil(1.5, 1500.0, 2085.0, "DIN EN 12524 clay or silt, via ht (thermal-properties.md §8.2)")


def graded(x0: float, x1: float, h0: float, ratio: float) -> Vector:
    """Points from x0 to x1, the first step h0, each next ``ratio`` longer."""
    pts = [x0]
    h = h0
    while pts[-1] + h < x1 - 1e-12:
        pts.append(pts[-1] + h)
        h *= ratio
    pts.append(x1)
    return np.array(pts)


@dataclass(frozen=True)
class Ground:
    """The soil's matrices (r-weighted, without the 2π), its nodes split into the disc's, the far
    sides' and the free ones."""

    radius: float
    soil: Soil
    stiffness: Any  # scipy CSR, (N, N)
    mass: Vector  # the lumped mass, (N,)
    disc: NDArray[np.int_]
    far: NDArray[np.int_]
    free: NDArray[np.int_]
    extent: float
    notes: tuple[str, ...] = field(default=())

    @property
    def nodes(self) -> int:
        return len(self.mass)

    @property
    def disc_capacity(self) -> float:
        """The disc's own soil's heat capacity (J/K): the floor's outer face's."""
        return 2 * math.pi * float(self.mass[self.disc].sum())

    def rows(self, u: Vector, up: Vector, t_disc: float, t_far: float) -> Vector:
        """The free nodes' residuals (W)."""
        k = self.stiffness
        full = np.empty(self.nodes)
        full[self.free] = u
        full[self.disc] = t_disc
        full[self.far] = t_far
        return 2 * math.pi * (self.mass[self.free] * up + (k @ full)[self.free])

    def into(self, u: Vector, t_disc: float, t_far: float, rate: float) -> float:
        """The heat the disc gives the soil (W), its own soil warming at ``rate`` (K/s)."""
        full = np.empty(self.nodes)
        full[self.free] = u
        full[self.disc] = t_disc
        full[self.far] = t_far
        return 2 * math.pi * float((self.stiffness @ full)[self.disc].sum()) + (
            self.disc_capacity * rate
        )


def ground(floor_area: float, soil: Soil = DRY, extent: float = 8.0, fine: float = 0.01) -> Ground:
    """The soil under a floor of ``floor_area`` (m²), as the disc of that area: a graded mesh
    ``extent`` deep and wide, its first cells ``fine`` (m) at the disc's edge and the surface."""
    a = math.sqrt(floor_area / math.pi)
    if extent < 4 * a:
        raise ValueError("the soil's extent must be at least four of the disc's radii")
    r = np.unique(np.concatenate([
        graded(0.0, a, max(a / 6, fine), 1.0),
        a + graded(0.0, extent - a, fine, 1.3)[1:],
    ]))  # fmt: skip
    z = -graded(0.0, extent, fine / 2, 1.3)[::-1]
    mesh: Any = MeshTri.init_tensor(r, z)
    basis: Any = Basis(mesh, ElementTriP1())

    @BilinearForm
    def stiff(u: Any, v: Any, w: Any) -> Any:
        return soil.k * dot(u.grad, v.grad) * w.x[0]

    @BilinearForm
    def mass(u: Any, v: Any, w: Any) -> Any:
        return soil.rho * soil.c * u * v * w.x[0]

    def on_disc(x: Any) -> Any:
        return np.isclose(x[1], 0.0) & (x[0] <= a + 1e-9)

    def on_far(x: Any) -> Any:
        return np.isclose(x[0], extent) | np.isclose(x[1], -extent)

    kmat = asm(stiff, basis).tocsr()
    lumped = np.asarray(asm(mass, basis).sum(axis=1)).ravel()
    disc = np.unique(basis.get_dofs(mesh.facets_satisfying(on_disc)).all())
    far = np.unique(basis.get_dofs(on_far).all())
    fixed = np.union1d(disc, far)
    free = np.setdiff1d(np.arange(basis.N), fixed)
    return Ground(a, soil, kmat, lumped, disc, far, free, extent)


def steady(g: Ground) -> float:
    """The soil's conductance at steady state, Q/ΔT (W/K), the far sides held."""
    k = g.stiffness
    u = np.zeros(g.nodes)
    u[g.disc] = 1.0
    kff = sp.csc_matrix(k[g.free][:, g.free])
    solved: Any = spla.spsolve(kff, -(k[g.free][:, g.disc] @ np.ones(len(g.disc))))
    u[g.free] = np.asarray(solved)
    return 2 * math.pi * float((k @ u)[g.disc].sum())


def step_response(g: Ground, times: list[float]) -> list[float]:
    """Q/ΔT (W/K) at each time after the disc steps by 1 K (backward Euler, steps growing 25 %
    from 5 s): the check against the slab and disc limits."""
    k = g.stiffness
    m = g.mass
    u = np.zeros(g.nodes)
    u[g.disc] = 1.0
    prev = np.zeros(g.nodes)
    t, dt = 0.0, 5.0
    out: list[float] = []
    todo = sorted(times)
    while todo:
        dt = min(dt, todo[0] - t)
        a = sp.diags(m / dt) + k
        aff = sp.csc_matrix(a[g.free][:, g.free])
        rhs = (m / dt * prev)[g.free] - a[g.free][:, g.disc] @ np.ones(len(g.disc))
        solved: Any = spla.spsolve(aff, rhs)
        u[g.free] = np.asarray(solved)
        q = 2 * math.pi * float((m / dt * (u - prev) + k @ u)[g.disc].sum())
        prev = u.copy()
        t += dt
        if abs(t - todo[0]) < 1e-6:
            out.append(q)
            todo.pop(0)
        dt = min(dt * 1.25, 1800.0)
    return out
