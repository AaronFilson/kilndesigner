"""Air at 1 atm against the Neutrium table (electric-and-thermal.md §6.3, [S63])."""

import numpy as np
import pytest

from kilndesigner.thermal.air import T_MAX, T_MIN, air


def test_the_table_spans_250_to_1000_k() -> None:
    assert (T_MIN, T_MAX) == (250.0, 1000.0)


def test_air_on_a_table_row_is_that_row() -> None:
    a = air(1000.0)
    assert (a.density, a.specific_heat, a.conductivity, a.viscosity) == pytest.approx(
        (0.353, 1141, 0.0672, 4.180e-5)
    )


def test_air_between_rows_is_interpolated_linearly() -> None:
    """350 K is halfway between the 300 K and 400 K rows."""
    a = air(350.0)
    assert a.temperature == 350.0
    assert a.density == pytest.approx((1.177 + 0.883) / 2)
    assert a.specific_heat == pytest.approx((1005 + 1013) / 2)
    assert a.conductivity == pytest.approx((0.0261 + 0.0331) / 2)
    assert a.viscosity == pytest.approx((1.850e-5 + 2.290e-5) / 2)


def test_derived_properties_at_300_k() -> None:
    """ν = μ/ρ, α = k/(ρ·cp), Pr = cp·μ/k, from the 300 K row."""
    a = air(300.0)
    assert a.kinematic_viscosity == pytest.approx(1.850e-5 / 1.177)
    assert a.diffusivity == pytest.approx(0.0261 / (1.177 * 1005))
    assert a.prandtl == pytest.approx(a.kinematic_viscosity / a.diffusivity)


def test_air_is_numpy_interp_to_the_bit() -> None:
    """The quick interpolation gives numpy.interp's values exactly, on rows and between them."""
    from kilndesigner.thermal import air as table

    for t in [*np.linspace(250.0, 1000.0, 301), 300.0, 777.7, 1000.0]:
        a = air(float(t))
        assert (a.density, a.specific_heat, a.conductivity, a.viscosity) == tuple(
            float(np.interp(t, table._T, col))  # pyright: ignore[reportPrivateUsage]
            for col in (table._RHO, table._CP, table._K, table._MU)  # pyright: ignore[reportPrivateUsage]
        )


@pytest.mark.parametrize("temperature", [249.9, 1000.1, 1500.0])
def test_air_outside_the_table_is_refused(temperature: float) -> None:
    """ADR 0009: no extrapolation past the table."""
    with pytest.raises(ValueError, match=r"tabulated from 250\.0 K to 1000\.0 K"):
        air(temperature)
