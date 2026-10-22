"""Steady wall solver against published worked examples (ADR 0009).

Sources: docs/research/electric-and-thermal.md §6.4.
"""

import itertools

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from kilndesigner.thermal.conductivity import Conductivity
from kilndesigner.thermal.surface import FixedSurface, StillAirSurface
from kilndesigner.thermal.wall import Slab, solve_wall

C = 273.15


def slab(name: str, thickness: float, k: float) -> Slab:
    return Slab(name, thickness, Conductivity.constant(k))


def test_furnace_wall_with_film_coefficients() -> None:
    """Test A: FOSSEE Basic Mechanical Engineering, Example 6.11 [S64].

    Fire brick 0.2 m (k 4.0) and common brick 0.2 m (k 0.65); gas at 1400 °C with h = 34;
    air at 50 °C with h = 19. Published: 3.07 kW/m², hot face 1309.705 °C, interface 1156.204 °C.
    """
    result = solve_wall(
        [slab("fire brick", 0.2, 4.0), slab("common brick", 0.2, 0.65)],
        1400 + C,
        50 + C,
        FixedSurface(19.0),
        inside_coefficient=34.0,
    )
    assert result.heat_flow == pytest.approx(3070, rel=1e-3)
    assert result.hot_face - C == pytest.approx(1309.705, abs=0.05)
    assert result.interfaces[0] - C == pytest.approx(1156.204, abs=0.05)


def test_furnace_wall_in_kilojoules_per_hour() -> None:
    """Test B: same source, Example 6.5 [S64]. k and h given in kJ/h units (÷ 3.6 for W).

    Published: 5916.3 kJ/(h·m²), inner surface 1625.88 °C, outer surface 171.72 °C.
    """
    result = solve_wall(
        [slab("brick", 0.225, 4.984 / 3.6), slab("insulating brick", 0.125, 0.623 / 3.6)],
        1650 + C,
        27 + C,
        FixedSurface(40.88 / 3.6),
        inside_coefficient=245.28 / 3.6,
    )
    assert result.heat_flow * 3.6 == pytest.approx(5916.3, rel=1e-3)
    assert result.hot_face - C == pytest.approx(1625.88, abs=0.1)
    assert result.surface - C == pytest.approx(171.72, abs=0.1)


def test_three_layers_between_fixed_faces() -> None:
    """Test C: CSJM University CHE S204 ch. 2 [S65]; faces at 870 °C and 40 °C.

    The source's resistances give 837.0 W/m², interfaces 685.9 °C and 162.8 °C.
    A very large outside coefficient pins the outside face to the air temperature.
    """
    result = solve_wall(
        [slab("fire brick", 0.22, 1.0), slab("insulating", 0.075, 0.12), slab("red", 0.11, 0.75)],
        870 + C,
        40 + C,
        FixedSurface(1e9),
    )
    assert result.heat_flow == pytest.approx(837.0, rel=1e-3)
    assert [t - C for t in result.interfaces] == pytest.approx([685.9, 162.8], abs=0.1)


def test_temperature_dependent_k_matches_the_exact_integral() -> None:
    """k = a + bT through one slab: Q·L = a(T1 − T2) + b/2 (T1² − T2²) exactly."""
    k = Conductivity((300.0, 1500.0), (0.1, 0.4))
    result = solve_wall([Slab("ifb", 0.1, k)], 1500.0, 300.0, FixedSurface(1e9))
    a = 0.1 - 300 * (0.3 / 1200)
    b = 0.3 / 1200
    expected = (a * (1500 - 300) + b / 2 * (1500**2 - 300**2)) / 0.1
    assert result.heat_flow == pytest.approx(expected, rel=1e-6)


def test_growing_area_reduces_flux_density_like_a_cylinder() -> None:
    """Area growing linearly with depth: ∫dx/A matches the closed form ln(A2/A1)/(dA/dx)."""
    a0, growth, thick = 1.0, 4.0, 0.1
    result = solve_wall(
        [slab("layer", thick, 1.0)],
        1000.0,
        300.0,
        FixedSurface(1e9),
        area=lambda x: a0 + growth * x,
    )
    import math

    resistance = math.log((a0 + growth * thick) / a0) / growth
    assert result.heat_flow == pytest.approx(700.0 / resistance, rel=1e-6)


ifb = st.floats(min_value=0.02, max_value=0.3)


@settings(max_examples=40, deadline=None)
@given(inner=ifb, outer=ifb, extra=st.floats(min_value=0.001, max_value=0.1))
def test_thicker_insulation_never_loses_more_heat(inner: float, outer: float, extra: float) -> None:
    k_ifb = Conductivity((600.0, 1300.0), (0.25, 0.33))
    k_fibre = Conductivity((533.0, 1255.0), (0.063, 0.264))
    shell = StillAirSurface("vertical", 1.0, 0.9)

    def loss(fibre: float) -> float:
        return solve_wall(
            [Slab("ifb", inner, k_ifb), Slab("fibre", fibre, k_fibre)], 1558.0, 294.0, shell
        ).heat_flow

    assert loss(outer + extra) < loss(outer)


@settings(max_examples=40, deadline=None)
@given(t_hot=st.floats(min_value=500, max_value=1600))
def test_temperatures_fall_through_the_wall(t_hot: float) -> None:
    result = solve_wall(
        [slab("a", 0.1, 0.3), slab("b", 0.05, 0.1)],
        t_hot,
        294.0,
        StillAirSurface("facing_up", 0.5, 0.8),
    )
    temps = result.temperatures
    assert all(a > b for a, b in itertools.pairwise(temps))
    assert result.surface > 294.0
