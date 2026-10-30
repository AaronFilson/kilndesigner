"""The finite-volume wall against analytical solutions, and its energy balance (ADR 0009)."""

from __future__ import annotations

import math

import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from kilndesigner.thermal.conductivity import Conductivity
from kilndesigner.thermal.surface import FixedSurface, StillAirSurface
from kilndesigner.thermal.transient import HeatCapacity, Layer, TransientWall
from kilndesigner.thermal.wall import Slab, solve_wall


def _march(wall: TransientWall, t_c: float, seconds: float, dt: float) -> tuple[float, ...]:
    """Hold the hot face at ``t_c``; return the totals heat in, stored, out."""
    heat_in = stored = out = 0.0
    for _ in range(round(seconds / dt)):
        o = wall.prepare(dt)(t_c)
        wall.commit(t_c, o.surface)
        heat_in, stored, out = heat_in + o.heat_in, stored + o.stored, out + o.heat_out
    return heat_in, stored, out


def test_semi_infinite_solid_matches_the_erf_solution() -> None:
    """A thick slab whose face steps to T_s: T = T_s + (T_i − T_s)·erf(x / 2√(αt)) (Holman eq.
    4-8, thermal-properties.md §8.3 [T45]). Within 1 % of the 1000 K step: backward Euler's first
    steps after a sudden jump are the main error."""
    k, rho, c = 1.0, 2000.0, 1000.0
    alpha = k / (rho * c)
    layer = Layer("slab", 0.5, Conductivity.constant(k), rho, HeatCapacity.constant(c))
    wall = TransientWall([layer], FixedSurface(0.0), 300.0, 300.0, max_cell=0.001)
    seconds = 3600.0
    heat_in, _, _ = _march(wall, 1300.0, seconds, 5.0)
    for x, t in zip(wall.centres, wall.temperatures, strict=True):
        if x > 0.15:
            break
        exact = 1300.0 + (300.0 - 1300.0) * math.erf(x / (2 * math.sqrt(alpha * seconds)))
        assert t == pytest.approx(exact, abs=10.0)
    # And the heat taken: Q/A = 2k(T_s − T_i)√(t/πα) (the integral of Holman eq. 4-12)
    exact_q = 2 * k * 1000.0 * math.sqrt(seconds / (math.pi * alpha))
    assert heat_in == pytest.approx(exact_q, rel=0.01)


def test_a_long_firing_settles_to_the_steady_wall() -> None:
    """Held long enough, the transient wall carries the steady solver's heat flow (C680-style,
    with k(T) and the still-air surface), so the two models agree where they overlap."""
    k_ifb = Conductivity((673.15, 1273.15), (0.25, 0.33))
    k_fibre = Conductivity((533.15, 1255.15), (0.063, 0.264))
    layers = [
        Layer("ifb", 0.114, k_ifb, 800.0, HeatCapacity.constant(1210.0)),
        Layer("fibre", 0.025, k_fibre, 128.0, HeatCapacity.constant(1130.0)),
    ]
    surface = StillAirSurface("vertical", 0.6, 0.79)
    wall = TransientWall(layers, surface, 294.0, 294.0)
    dt = 600.0
    _march(wall, 1500.0, 400 * 3600.0, dt)
    o = wall.prepare(dt)(1500.0)
    steady = solve_wall(
        [Slab(x.name, x.thickness, x.conductivity) for x in layers], 1500.0, 294.0, surface
    )
    assert o.heat_out / dt == pytest.approx(steady.heat_flow, rel=0.02)
    assert o.surface == pytest.approx(steady.surface, abs=2.0)


@settings(max_examples=40, deadline=None)
@given(
    layers=st.lists(
        st.tuples(
            st.floats(0.01, 0.15),  # thickness
            st.floats(0.03, 2.0),  # k at 300 K
            st.floats(0.0, 2.0),  # k's rise to 1600 K
            st.floats(100.0, 2500.0),  # ρ
            st.floats(500.0, 1300.0),  # c_p
        ),
        min_size=1,
        max_size=3,
    ),
    temps=st.lists(st.floats(300.0, 1600.0), min_size=1, max_size=12),
    dt=st.floats(10.0, 1200.0),
    h=st.floats(0.0, 30.0),
)
def test_energy_is_conserved(
    layers: list[tuple[float, float, float, float, float]],
    temps: list[float],
    dt: float,
    h: float,
) -> None:
    """Every step: heat in at the hot face = heat stored + heat out at the shell."""
    wall = TransientWall(
        [
            Layer(
                f"l{i}",
                t,
                Conductivity((300.0, 1600.0), (k, k + rise)),
                rho,
                HeatCapacity((300.0, 1600.0), (c, 1.2 * c)),
            )
            for i, (t, k, rise, rho, c) in enumerate(layers)
        ],
        FixedSurface(h),
        290.0,
        290.0,
        area=lambda x: (0.5 + 2 * x) ** 2,
    )
    for t_c in temps:
        prepared = wall.prepare(dt)
        a, b = wall.heat_in_line(dt)
        o = prepared(t_c)
        assert a + b * t_c == pytest.approx(o.heat_in, rel=1e-9, abs=1e-6)
        scale = max(abs(o.heat_in), abs(o.stored), abs(o.heat_out), 1.0)
        assert abs(o.heat_in - o.stored - o.heat_out) <= 1e-8 * scale
        wall.commit(t_c, o.surface)


def test_heat_capacity_holds_its_end_values() -> None:
    c = HeatCapacity((673.15, 873.15), (956.0, 997.0))
    assert list(c.cp(np.array([300.0, 773.15, 2000.0]))) == pytest.approx([956.0, 976.5, 997.0])


@pytest.mark.parametrize(
    ("temps", "values", "message"),
    [
        ((), (), "matching"),
        ((300.0, 300.0), (1.0, 2.0), "increase"),
        ((300.0,), (0.0,), "positive"),
    ],
)
def test_heat_capacity_refuses_bad_data(
    temps: tuple[float, ...], values: tuple[float, ...], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        HeatCapacity(temps, values)


def test_a_wall_needs_layers_of_some_thickness() -> None:
    with pytest.raises(ValueError, match="at least one layer"):
        TransientWall([], FixedSurface(1.0), 300.0, 300.0)
    bad = Layer("x", 0.0, Conductivity.constant(1.0), 1.0, HeatCapacity.constant(1.0))
    with pytest.raises(ValueError, match="thicker than zero"):
        TransientWall([bad], FixedSurface(1.0), 300.0, 300.0)


def test_stored_energy_and_areas() -> None:
    layer = Layer("x", 0.1, Conductivity.constant(1.0), 1000.0, HeatCapacity.constant(1000.0))
    wall = TransientWall([layer], FixedSurface(5.0), 300.0, 400.0, area=lambda x: 1 + x)
    assert wall.thickness == pytest.approx(0.1)
    assert wall.inside_area == 1.0
    assert wall.outside_area == pytest.approx(1.1)
    # ρ·c·V·ΔT, V = ∫(1 + x)dx over 0.1 m = 0.105 m³
    assert wall.stored_energy(300.0) == pytest.approx(1000 * 1000 * 0.105 * 100, rel=1e-6)
