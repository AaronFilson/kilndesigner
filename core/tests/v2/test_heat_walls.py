"""v2's walls as cells (`heat/walls.py`) on SUNDIALS IDA: against the semi-infinite solid (erf),
Incropera §5.5's plane wall with convection (the series solution), v1's `TransientWall` and, held
long, v1's steady `solve_wall` (k(T) integrated exactly, as ASTM C680)."""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np
import pytest
from numpy.typing import NDArray
from scipy.special import erfc
from sksundae.ida import IDA  # pyright: ignore[reportMissingTypeStubs]

from kilndesigner.library import material
from kilndesigner.numeric import find_root
from kilndesigner.thermal.conductivity import Conductivity
from kilndesigner.thermal.surface import StillAirSurface
from kilndesigner.thermal.transient import HeatCapacity, Layer, TransientWall
from kilndesigner.thermal.wall import Slab, solve_wall
from kilndesigner.units import parse_quantity, si
from kilndesigner.v2.heat import walls as wl

type Vector = NDArray[np.float64]
ROOM = 294.26
IN = 0.0254


def _run(
    wall: wl.CellWall,
    t_end: float,
    t0: float,
    hot: Callable[[float], float] | None = None,
    film: tuple[float, float] | None = None,
) -> tuple[float, Vector, float]:
    """Integrate one wall to t_end from a uniform t0: the hot face held to hot(t), or behind a
    film (h, T∞). Returns T_hot, the cells and T_out at the end."""
    n = wall.cells

    def res(t: float, y: Vector, yp: Vector, r: Vector) -> None:
        th, c, to = y[0], y[1 : n + 1], y[n + 1]
        q = wall.flows(th, c, to)
        if film is None:
            assert hot is not None
            r[0] = th - hot(t)
        else:
            r[0] = (film[0] * wall.area_in * (film[1] - th) - q[0]) / 1e3
        r[1 : n + 1] = wall.capacity(c) * yp[1 : n + 1] - (q[:-1] - q[1:])
        r[n + 1] = q[-1] - wall.outer_loss(to)

    y0 = np.full(n + 2, t0)
    if hot is not None:
        y0[0] = hot(0.0)
    solver = IDA(res, algebraic_idx=[0, n + 1], calc_initcond="yp0", rtol=1e-7, atol=1e-6,
                 linsolver="band", lband=1, uband=1, max_num_steps=100_000)  # fmt: skip
    sol = solver.solve(np.array([0.0, t_end]), y0, np.zeros(n + 2))
    assert sol.success, sol.message
    y = sol.y[-1]
    return float(y[0]), y[1 : n + 1], float(y[n + 1])


def _slab(k: float, rho: float, c: float, thickness: float) -> Layer:
    return Layer("test", thickness, Conductivity.constant(k), rho, HeatCapacity.constant(c))


ADIABATIC = wl.Outside("adiabatic")


def test_a_thick_wall_heated_by_a_step_is_the_semi_infinite_solid() -> None:
    """A step of ΔT on the face of a solid deep enough: T = T_i + ΔT erfc(x/2√(αt)), and the
    heat taken in, 2kΔT√(t/(πα)) per m² (Carslaw & Jaeger; Holman eq. 4-8, 4-12)."""
    k, rho, c, dt_ = 1.0, 2000.0, 1000.0, 1000.0
    alpha = k / (rho * c)
    wall = wl.CellWall("deep", (_slab(k, rho, c, 0.5),), lambda x: 1.0, ADIABATIC)
    t = 7200.0
    _, cells, _ = _run(wall, t, 300.0, hot=lambda s: 1300.0)
    x = np.cumsum(wall.dx) - wall.dx / 2
    exact = 300 + dt_ * erfc(x / (2 * math.sqrt(alpha * t)))
    assert np.abs(cells - exact).max() < 0.01 * dt_
    taken = wall.stored(cells, 300.0)
    assert taken == pytest.approx(2 * k * dt_ * math.sqrt(t / (math.pi * alpha)), rel=0.01)


def _incropera(bi: float, fo: float, xs: Vector, terms: int = 60) -> Vector:
    """θ* = Σ C_n e^(−ζ_n² Fo) cos(ζ_n x*), ζ_n tan ζ_n = Bi, C_n = 4 sin ζ_n/(2ζ_n + sin 2ζ_n)
    (Incropera & DeWitt §5.5.1, eqs. 5.39a–c), x* from the adiabatic mid-plane."""
    out = np.zeros_like(xs)

    def eigen(v: float) -> float:
        return v * math.tan(v) - bi

    for n in range(terms):
        lo, hi = n * math.pi + 1e-12, n * math.pi + math.pi / 2 - 1e-12
        z = find_root(eigen, lo, hi)
        cn = 4 * math.sin(z) / (2 * z + math.sin(2 * z))
        out += cn * math.exp(-z * z * fo) * np.cos(z * xs)
    return out


def test_a_plane_wall_with_convection_is_incroperas_series() -> None:
    """Half a symmetric plane wall, L 0.1 m, k 1, ρc 2×10⁶ (α 5×10⁻⁷), h 20 (Bi 2), from 300 K
    in a 1300 K fluid, at Fo 0.5 (10,000 s): the cells and the face against the series."""
    k, rho, c, length, h = 1.0, 2000.0, 1000.0, 0.1, 20.0
    wall = wl.CellWall("slab", (_slab(k, rho, c, length),), lambda x: 1.0, ADIABATIC,
                       max_cell=0.0025)  # fmt: skip
    t = 0.5 * length**2 * rho * c / k
    th, cells, to = _run(wall, t, 300.0, film=(h, 1300.0))
    x = np.cumsum(wall.dx) - wall.dx / 2
    theta = _incropera(h * length / k, 0.5, 1 - x / length)
    assert np.abs((cells - 1300.0) / (300.0 - 1300.0) - theta).max() < 0.003
    face = _incropera(h * length / k, 0.5, np.array([1.0, 0.0]))
    assert (th - 1300.0) / (300.0 - 1300.0) == pytest.approx(face[0], abs=0.003)
    assert (to - 1300.0) / (300.0 - 1300.0) == pytest.approx(face[1], abs=0.003)


def _material_layer(mid: str, thickness: float) -> Layer:
    m = material(mid)
    assert m.specific_heat is not None
    temps, cps = m.specific_heat.to_points()
    if temps[0] > 300:  # held at its first value down to 24 °C, as the library says: v1's 800
        temps, cps = (297.15, *temps), (800.0, *cps)
    return Layer(mid, thickness, m.k, si(parse_quantity(m.density), "kg/m**3"),
                 HeatCapacity(tuple(temps), tuple(cps)))  # fmt: skip


LINING = (
    _material_layer("firebrick-medium-duty-smithfield", 4.5 * IN),
    _material_layer("ifb-k23", 4.5 * IN),
)
AIR = wl.Outside("air", StillAirSurface("vertical", 1.2, 0.9), ROOM)


def test_cells_agree_with_v1s_transient_wall() -> None:
    """A two-layer lining (4½ in medium-duty over 4½ in K-23, still air outside) with its hot face
    ramped 294 → 1558 K in 10 h: v2's cells on IDA against v1's backward Euler at 10 s steps
    (lagged properties, first order): the same within their discretisation."""
    area = wl.linear_area(1.0, 1.6, 9 * IN)
    wall = wl.CellWall("lining", LINING, area, AIR)
    t_end = 10 * 3600.0

    def ramp(t: float) -> float:
        return ROOM + (1558.0 - ROOM) * min(t / t_end, 1.0)

    _, cells, to = _run(wall, t_end, ROOM, hot=ramp)
    tw = TransientWall(list(LINING), AIR.surface, ROOM, ROOM, area=area)  # pyright: ignore[reportArgumentType]
    dt, t = 10.0, 0.0
    while t < t_end - 1e-9:
        step = tw.prepare(dt)
        t += dt
        r = step(ramp(t))
        tw.commit(ramp(t), r.surface)
    assert np.abs(cells - tw.temperatures).max() < 1.0
    assert to == pytest.approx(tw.t_surface, abs=0.5)


def test_held_long_the_cells_reach_the_steady_loss() -> None:
    """Held at 1558 K for 2,000 h the lining is steady: its loss is v1's `solve_wall`, k(T)
    integrated exactly across each layer (ASTM C680's way), within the cells' discretisation."""
    area = wl.linear_area(1.0, 1.6, 9 * IN)
    wall = wl.CellWall("lining", LINING, area, AIR)
    th, cells, to = _run(wall, 2000 * 3600.0, ROOM, hot=lambda s: 1558.0)
    slabs = [Slab(x.name, x.thickness, x.conductivity) for x in LINING]
    steady = solve_wall(slabs, 1558.0, ROOM, AIR.surface, area=area)  # pyright: ignore[reportArgumentType]
    assert wall.outer_loss(to) == pytest.approx(steady.heat_flow, rel=0.01)
    assert wall.flows(th, cells, to)[0] == pytest.approx(steady.heat_flow, rel=0.01)
    assert to == pytest.approx(steady.surface, abs=1.0)


def test_the_wall_records() -> None:
    wall = wl.CellWall("lining", LINING, wl.linear_area(1.0, 1.6, 9 * IN), ADIABATIC)
    assert wall.cells == 46  # 4½ in in 5 mm cells: 23 a layer
    assert wall.thickness == pytest.approx(9 * IN)
    assert (wall.area_in, wall.area_out) == pytest.approx((1.0, 1.6))
    assert wall.outer_loss(900.0) == 0.0
    assert wall.stored(np.full(46, 300.0), 300.0) == 0.0
    assert wl.layers_total(LINING) == pytest.approx(9 * IN)
    with pytest.raises(ValueError, match="at least one layer"):
        wl.CellWall("none", (), lambda x: 1.0, ADIABATIC)
    with pytest.raises(ValueError, match="thicker than zero"):
        wl.CellWall("thin", (_slab(1, 1, 1, 0.0),), lambda x: 1.0, ADIABATIC)


def test_a_boxs_grown_faces_tile_the_outer_box() -> None:
    """Each face's rectangle grown by the lining on each edge: six of them make the outer box."""
    w, d, h, t = 0.7, 0.9, 1.1, 0.23
    faces = ("left", "right", "front", "back", "floor", "roof")
    sides = [wl.face_sides(f, w, d, h, 0.0) for f in faces]
    total = sum(wl.grown(math.prod(s), s, t) for s in sides)
    wo, do, ho = w + 2 * t, d + 2 * t, h + 2 * t
    assert total == pytest.approx(2 * (wo * do + wo * ho + do * ho))
    assert wl.face_sides("front", w, d, h, 0.1) == (w, h + 0.1)
