"""The walls as method-of-lines cells (ADR 0017 H8): v1's `TransientWall` physics (ADR 0015) as
rates for a DAE, with nothing lagged, so the firing integrator iterates k(T) and c_p(T) with
everything else (`thermal-software.md` §3.3, §4.1).

Each layer is cut into cells of at most 5 mm (at least four). A cell of volume A(x)·Δx stores
ρ·c_p(T)·V per kelvin and passes heat through conductances G = A_face/(Δx₁/2k₁ + Δx₂/2k₂), a layer
boundary being a series pair of half-cells (Patankar's harmonic mean), as `TransientWall`. The hot
face and the outer face are unknowns of their own (algebraic): heat reaches the first cell through
its half-cell, and leaves the last to the outside through its half-cell and then:
- still air: v1's `StillAirSurface` (Churchill–Chu, Lloyd–Moran, Jaffer; radiation to the room),
  h at the face's own temperature;
- adiabatic: nothing leaves (a floor over a firebox when the firebox isn't a zone, said so);
- a ground coupled to the face (`ground.py`), which takes the flow the face gives it.

    C_i dT_i/dt = q_i − q_{i+1},   q_0 = G_hot (T_hot − T_1),   q_n = G_out (T_n − T_out).

The area grows with depth as the caller's A(x) gives it (a box face's outside rectangle grown by
its thickness on each edge tiles the outer box).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Literal

import numpy as np
from numpy.typing import NDArray

from kilndesigner.thermal.surface import Surface
from kilndesigner.thermal.transient import Layer

type Vector = NDArray[np.float64]
type Kind = Literal["air", "adiabatic", "ground"]


@dataclass(frozen=True)
class Outside:
    """What the wall's outer face loses to."""

    kind: Kind
    surface: Surface | None = None
    t_ambient: float = 294.15


def linear_area(a_in: float, a_out: float, thickness: float) -> Callable[[float], float]:
    """A(x) from the inside area to the outside one, linear in depth."""

    def area(x: float) -> float:
        return a_in + (a_out - a_in) * x / thickness

    return area


@dataclass(frozen=True)
class CellWall:
    """A layered wall as cells, hot face first; its outside's kind."""

    name: str
    layers: tuple[Layer, ...]
    area: Callable[[float], float]
    outside: Outside
    max_cell: float = 0.005
    min_cells: int = 4
    dx: Vector = field(init=False)
    owner: NDArray[np.int_] = field(init=False)
    face_area: Vector = field(init=False)
    volume: Vector = field(init=False)

    def __post_init__(self) -> None:
        if not self.layers:
            raise ValueError("a wall needs at least one layer")
        widths: list[float] = []
        owner: list[int] = []
        for i, layer in enumerate(self.layers):
            if layer.thickness <= 0:
                raise ValueError("a layer must be thicker than zero")
            n = max(self.min_cells, int(np.ceil(layer.thickness / self.max_cell - 1e-9)))
            widths += [layer.thickness / n] * n
            owner += [i] * n
        dx = np.array(widths)
        edges = np.concatenate(([0.0], np.cumsum(dx)))
        centres = 0.5 * (edges[:-1] + edges[1:])
        object.__setattr__(self, "dx", dx)
        object.__setattr__(self, "owner", np.array(owner))
        object.__setattr__(self, "face_area", np.array([self.area(float(x)) for x in edges]))
        object.__setattr__(self, "volume", np.array([self.area(float(x)) for x in centres]) * dx)

    @property
    def cells(self) -> int:
        return len(self.dx)

    @property
    def thickness(self) -> float:
        return float(self.dx.sum())

    @property
    def area_in(self) -> float:
        return float(self.face_area[0])

    @property
    def area_out(self) -> float:
        return float(self.face_area[-1])

    def k(self, t: Vector) -> Vector:
        out = np.empty_like(t)
        for i, layer in enumerate(self.layers):
            m = self.owner == i
            out[m] = layer.conductivity.k_many(t[m])
        return out

    def capacity(self, t: Vector) -> Vector:
        """ρ·c_p(T)·V of each cell, J/K."""
        out = np.empty_like(t)
        for i, layer in enumerate(self.layers):
            m = self.owner == i
            out[m] = layer.density * layer.heat_capacity.cp(t[m]) * self.volume[m]
        return out

    def flows(self, t_hot: float, cells: Vector, t_out: float) -> Vector:
        """Heat (W) through each face, inwards to outwards: q_0 into the hot face's cell, … q_n
        out of the last."""
        k = self.k(cells)
        half = self.dx / (2 * k)
        q = np.empty(len(cells) + 1)
        q[0] = self.face_area[0] / half[0] * (t_hot - cells[0])
        q[1:-1] = self.face_area[1:-1] / (half[:-1] + half[1:]) * (cells[:-1] - cells[1:])
        q[-1] = self.face_area[-1] / half[-1] * (cells[-1] - t_out)
        return q

    def outer_loss(self, t_out: float) -> float:
        """What the outer face gives the outside (W); a ground's flow is the caller's."""
        o = self.outside
        if o.kind == "air":
            assert o.surface is not None
            h = o.surface.coefficient(t_out, o.t_ambient)
            return h * self.area_out * (t_out - o.t_ambient)
        return 0.0

    def stored(self, cells: Vector, t0: float) -> float:
        """Heat held above a uniform t0 (J), c_p integrated exactly cell by cell."""
        total = 0.0
        for i, layer in enumerate(self.layers):
            m = self.owner == i
            cp = layer.heat_capacity
            h = np.array([cp.enthalpy(float(t)) - cp.enthalpy(t0) for t in cells[m]])
            total += float(np.sum(layer.density * self.volume[m] * h))
        return total


def grown(a_in: float, sides: tuple[float, float], thickness: float) -> float:
    """A face's outside area: its inside area grown as its bounding rectangle (sides, m) grows by
    the thickness on each edge. A box's six rectangles so grown tile the outer box exactly; an
    arch's crown keeps its curvature's share (Derived)."""
    a, b = sides
    return a_in * (a + 2 * thickness) * (b + 2 * thickness) / (a * b)


def face_sides(
    face: str, width: float, depth: float, height: float, rise: float
) -> tuple[float, float]:
    """The bounding rectangle of a box chamber's face: the side walls to the springline, the end
    walls to the crown, the floor and roof the plan."""
    if face in ("left", "right"):
        return depth, height
    if face in ("front", "back"):
        return width, height + rise
    return width, depth


def layers_total(layers: Sequence[Layer]) -> float:
    return sum(x.thickness for x in layers)
