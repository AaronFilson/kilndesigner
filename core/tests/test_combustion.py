"""Combustion against published propane data (combustion-and-masonry.md §1.1)."""

import pytest

from kilndesigner.combustion import (
    PROPANE_HHV_MJ_PER_KG,
    adiabatic_flame_temperature,
    air_ratio_for_flue_oxygen,
    available_heat,
    available_heat_fraction,
)


def test_adiabatic_flame_temperature_in_air() -> None:
    """Published maximum flame temperature of propane in air: 3,595 °F [S1]."""
    t_f = (adiabatic_flame_temperature() - 273.15) * 9 / 5 + 32
    assert t_f == pytest.approx(3595, rel=0.02)


def test_heat_released_at_room_temperature_is_the_lower_heating_value() -> None:
    """Products cooled to 25 °C with the water as vapour release the LHV: 46.607 MJ/kg [S5]."""
    assert available_heat(298.15) / 1e6 == pytest.approx(46.607, rel=0.01)
    assert available_heat_fraction(298.15) == pytest.approx(
        46.607 / PROPANE_HHV_MJ_PER_KG, rel=0.01
    )


def test_no_heat_is_available_at_the_flame_temperature() -> None:
    assert available_heat_fraction(adiabatic_flame_temperature()) == pytest.approx(0.0, abs=1e-6)


def test_available_heat_falls_as_the_kiln_gets_hotter() -> None:
    temps = [500.0, 900.0, 1300.0, 1558.0]
    fractions = [available_heat_fraction(t, 1.15) for t in temps]
    assert fractions == sorted(fractions, reverse=True)
    # At cone 10 with 15% excess air, roughly half the fuel's heat goes up the chimney.
    assert 0.3 < fractions[-1] < 0.6


def test_excess_air_costs_heat_and_so_does_reduction() -> None:
    t = 1400.0
    assert available_heat_fraction(t, 1.3) < available_heat_fraction(t, 1.0)
    assert available_heat_fraction(t, 0.9) < available_heat_fraction(t, 1.0)


def test_air_ratio_for_three_percent_oxygen() -> None:
    """C3H8 + 5λ(O2 + 3.773 N2): 3% dry O2 needs about 15% excess air."""
    assert air_ratio_for_flue_oxygen(0.0) == pytest.approx(1.0)
    assert air_ratio_for_flue_oxygen(0.03) == pytest.approx(1.153, abs=0.002)
