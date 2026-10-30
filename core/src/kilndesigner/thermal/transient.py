"""Transient heat flow through a layered wall: one-dimensional finite volumes, implicit in time.

Each layer is cut into cells. A cell of volume V = A(x)·Δx stores heat ρ·c_p(T)·V per kelvin, and
passes heat to its neighbours through conductances G = A_face / (Δx₁/2k₁ + Δx₂/2k₂), so a layer
boundary is a series pair of half-cells, as in Patankar's harmonic mean. The hot face is held at
the chamber's temperature T_c through the first half-cell; the outside loses heat to still air
through the last half-cell and the surface coefficient h(T_s) of
:mod:`kilndesigner.thermal.surface`.

Backward Euler, with k, c_p and h taken at the start of each step (lagged), makes each step a
tridiagonal linear system. Because it is linear, the cell temperatures at the end of the step are
an affine function of T_c, u + v·T_c, and so is the heat that enters the hot face. The kiln can
then pick T_c for each step in closed form: the schedule's, or the one its heat can reach.

The discrete energy balance is exact: heat in at the hot face = heat stored + heat out at the
shell, step by step, to the round-off of the solve (the rows of the system sum to it).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray
from scipy.linalg import solve_banded

from kilndesigner.thermal.conductivity import Conductivity
from kilndesigner.thermal.surface import Surface
from kilndesigner.thermal.wall import AreaAtDepth, unit_area

type Vector = NDArray[np.float64]


@dataclass(frozen=True)
class HeatCapacity:
    """c_p(T) as points (kelvin, J/(kg·K)), linear between them and held at the end values."""

    temperatures: tuple[float, ...]
    values: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.temperatures) != len(self.values) or not self.temperatures:
            raise ValueError("specific heat needs matching, non-empty temperature and c_p lists")
        if any(b <= a for a, b in zip(self.temperatures, self.temperatures[1:], strict=False)):
            raise ValueError("specific heat temperatures must increase")
        if any(c <= 0 for c in self.values):
            raise ValueError("specific heat must be positive")

    @staticmethod
    def constant(c: float) -> HeatCapacity:
        return HeatCapacity((300.0,), (c,))

    def cp(self, t: Vector) -> Vector:
        return np.interp(t, self.temperatures, self.values)


@dataclass(frozen=True)
class Layer:
    name: str
    thickness: float  # m
    conductivity: Conductivity
    density: float  # kg/m³
    heat_capacity: HeatCapacity


@dataclass(frozen=True)
class StepResult:
    """One step's outcome for the T_c chosen."""

    chamber: float  # K
    heat_in: float  # J into the hot face over the step
    heat_out: float  # J out of the shell over the step
    stored: float  # J added to the wall over the step
    surface: float  # K, the outside face at the end of the step


@dataclass
class TransientWall:
    """A layered wall's temperatures through time. ``area`` is A(depth) as in the steady solver."""

    layers: Sequence[Layer]
    surface: Surface
    t_ambient: float
    t_initial: float
    area: AreaAtDepth = unit_area
    max_cell: float = 0.005  # m
    min_cells: int = 4
    temperatures: Vector = field(init=False)
    t_surface: float = field(init=False)

    def __post_init__(self) -> None:
        if not self.layers:
            raise ValueError("a wall needs at least one layer")
        widths: list[float] = []
        owner: list[int] = []
        for i, layer in enumerate(self.layers):
            if layer.thickness <= 0:
                raise ValueError("a layer must be thicker than zero")
            n = max(self.min_cells, int(np.ceil(layer.thickness / self.max_cell)))
            widths += [layer.thickness / n] * n
            owner += [i] * n
        self.dx = np.array(widths)
        self.owner = np.array(owner)
        edges = np.concatenate(([0.0], np.cumsum(self.dx)))
        self.edges = edges
        self.centres = 0.5 * (edges[:-1] + edges[1:])
        self.face_area = np.array([self.area(float(x)) for x in edges])
        self.volume = np.array([self.area(float(x)) for x in self.centres]) * self.dx
        self.temperatures = np.full(len(self.dx), self.t_initial, dtype=np.float64)
        self.t_surface = self.t_initial

    @property
    def thickness(self) -> float:
        return float(self.edges[-1])

    @property
    def outside_area(self) -> float:
        return float(self.face_area[-1])

    @property
    def inside_area(self) -> float:
        return float(self.face_area[0])

    def _k(self, t: Vector) -> Vector:
        out = np.empty_like(t)
        for i, layer in enumerate(self.layers):
            mask = self.owner == i
            out[mask] = [layer.conductivity.k(float(x)) for x in t[mask]]
        return out

    def _capacity(self, t: Vector) -> Vector:
        """ρ·c_p·V of each cell, J/K."""
        out = np.empty_like(t)
        for i, layer in enumerate(self.layers):
            mask = self.owner == i
            out[mask] = layer.density * layer.heat_capacity.cp(t[mask]) * self.volume[mask]
        return out

    def stored_energy(self, reference: float) -> float:
        """Heat held above ``reference`` K, with c_p at each cell's temperature (J); a rough
        figure for reports, not the balance the step keeps (that uses lagged c_p)."""
        return float(np.sum(self._capacity(self.temperatures) * (self.temperatures - reference)))

    def _surface_temperature(self, t_last: float, r_half: float) -> tuple[float, float]:
        """The outside face's temperature and h, for the last cell at ``t_last``: the series of
        the half-cell and the surface film, with h at the face's own temperature (fixed point)."""
        ts, h, a = self.t_surface, 0.0, self.outside_area
        for _ in range(4):
            h = self.surface.coefficient(ts, self.t_ambient)
            if h <= 0:  # no film: the face is the last cell's half-cell away from nothing
                return t_last, 0.0
            film = 1.0 / (h * a)
            ts = self.t_ambient + (t_last - self.t_ambient) * film / (r_half + film)
        return ts, h

    def prepare(self, dt: float) -> Callable[[float], StepResult]:
        """Set up one implicit step of ``dt`` seconds; return a function from T_c to its result.

        Call :meth:`commit` with the chosen result's T_c to advance."""
        t_old = self.temperatures
        k = self._k(t_old)
        cap = self._capacity(t_old)
        half = self.dx / (2 * k)  # m²·K/W per unit area, each cell's half
        g_inner = self.face_area[1:-1] / (half[:-1] + half[1:])
        g_hot = self.face_area[0] / half[0]
        r_half_out = half[-1] / self.face_area[-1]
        _, h = self._surface_temperature(float(t_old[-1]), r_half_out)
        g_out = 0.0 if h <= 0 else 1.0 / (r_half_out + 1.0 / (h * self.outside_area))

        n = len(t_old)
        diag = cap / dt
        diag[:-1] += g_inner
        diag[1:] += g_inner
        diag[0] += g_hot
        diag[-1] += g_out
        bands = np.zeros((3, n))
        bands[0, 1:] = -g_inner
        bands[1] = diag
        bands[2, :-1] = -g_inner
        rhs0 = cap / dt * t_old
        rhs0[-1] += g_out * self.t_ambient
        rhs1 = np.zeros(n)
        rhs1[0] = g_hot
        solved = solve_banded((1, 1), bands, np.column_stack((rhs0, rhs1)))
        u, v = solved[:, 0], solved[:, 1]
        self._pending = (u, v, cap, g_hot, g_out, r_half_out)

        def result(t_c: float) -> StepResult:
            t_new = u + v * t_c
            heat_in = g_hot * (t_c - t_new[0]) * dt
            heat_out = g_out * (t_new[-1] - self.t_ambient) * dt
            stored = float(np.sum(cap * (t_new - t_old)))
            # The face sits between the last cell and the air, in proportion to the resistances
            ts = self.t_ambient + (t_new[-1] - self.t_ambient) * (1.0 - g_out * r_half_out)
            return StepResult(t_c, float(heat_in), float(heat_out), stored, float(ts))

        return result

    def heat_in_line(self, dt: float) -> tuple[float, float]:
        """Heat into the hot face over the prepared step as a + b·T_c (J): (a, b)."""
        u, v, _, g_hot, _, _ = self._pending
        return -g_hot * u[0] * dt, g_hot * (1.0 - v[0]) * dt

    def commit(self, t_c: float, surface: float) -> None:
        u, v, *_ = self._pending
        self.temperatures = u + v * t_c
        self.t_surface = surface
