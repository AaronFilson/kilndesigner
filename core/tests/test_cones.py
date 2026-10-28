"""Orton cones as temperatures (cones.yaml; electric-and-thermal.md §8, cones.md)."""

import pytest

from kilndesigner.cones import (
    CONE_SOURCE,
    cone_names,
    cone_rates,
    cone_temperature,
    hotter_than,
    normalise,
)
from kilndesigner.units import si


@pytest.mark.parametrize(
    ("written", "key"),
    [("10", "10"), (" 06 ", "06"), ("5½", "5.5"), ("05½", "05.5"), ("32 1/2", "32.5")],
)
def test_cones_are_written_the_way_potters_write_them(written: str, key: str) -> None:
    assert normalise(written) == key


def test_the_table_runs_from_cone_022_to_42_coolest_first() -> None:
    names = cone_names()
    assert (names[0], names[-1]) == ("022", "42")
    assert names.index("06") < names.index("6") < names.index("10") < names.index("11")


def test_self_supporting_cones_are_tabulated_at_60_and_150_per_hour() -> None:
    """Orton's chart gives cones 022–14 at 60 and 150 °C/h; PCE cones have one rate each."""
    assert cone_rates("10") == (60, 150)
    assert cone_rates("5½") == (60, 150)
    assert cone_rates("15") == (150,)
    assert cone_rates("38") == (100,)
    assert cone_rates("42") == (600,)


def test_cone_6_by_its_rate() -> None:
    """Orton: cone 6 is 1222 °C at 60 °C/h and 1243 °C at 150 °C/h."""
    assert si(cone_temperature("6"), "degC") == 1222
    assert si(cone_temperature("6", 150), "degC") == 1243
    assert "Orton" in CONE_SOURCE


def test_a_rate_the_chart_does_not_have_is_refused() -> None:
    with pytest.raises(ValueError, match=r"tabulated at \(60, 150, 100, 600\) °C/h"):
        cone_temperature("10", 120)


def test_a_rate_the_cone_is_not_published_at_names_the_ones_it_is() -> None:
    with pytest.raises(ValueError, match="cone 39 only at 600 °C/h; set the firing's final_rate"):
        cone_temperature("39", 150)


def test_hotter_than_follows_ortons_order_not_the_number() -> None:
    """Cone 06 is cooler than cone 6, and cone 11 comes after cone 10 at any rate."""
    assert hotter_than("11", "10")
    assert not hotter_than("06", "6")
    assert not hotter_than("10", "10")
    assert hotter_than("5½", "5")


def test_an_unknown_cone_is_refused() -> None:
    with pytest.raises(ValueError, match="cone '43' is not in the Orton table"):
        hotter_than("43", "10")
    with pytest.raises(ValueError, match=r"\(022 to 42\)"):
        cone_rates("021½")
