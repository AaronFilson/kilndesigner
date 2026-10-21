import pytest
from hypothesis import given
from hypothesis import strategies as st

from kilndesigner.units import Q_, UnitError, format_quantity, parse_quantity, si


@pytest.mark.parametrize(
    ("text", "unit", "expected"),
    [
        ("9 in", "mm", 228.6),
        ("4.5in", "in", 4.5),
        ("1 ft", "in", 12.0),
        ("240 V", "V", 240.0),
        ("48 A", "A", 48.0),
        ("11.5 kW", "W", 11_500.0),
        ("100000 BTU/hr", "W", 29_307.1),
        ("1e3 W", "kW", 1.0),
        ("0.12 USD/kWh", "USD/kWh", 0.12),
        ("8 pcf", "kg/m**3", 128.15),
    ],
)
def test_parses_number_and_unit(text: str, unit: str, expected: float) -> None:
    assert si(parse_quantity(text), unit) == pytest.approx(expected, rel=1e-4)


def test_offset_temperatures_parse() -> None:
    assert si(parse_quantity("2345 degF"), "degC") == pytest.approx(1285.0, abs=0.01)
    assert si(parse_quantity("1285 degC"), "K") == pytest.approx(1558.15)


@pytest.mark.parametrize("text", ["9", "", "in", "nine in"])
def test_rejects_text_without_number_and_unit(text: str) -> None:
    with pytest.raises(UnitError):
        parse_quantity(text)


def test_rejects_unknown_units() -> None:
    with pytest.raises(UnitError, match="not a unit"):
        parse_quantity("9 bricks")


def test_rejects_wrong_dimension() -> None:
    with pytest.raises(UnitError, match="not a length"):
        parse_quantity("9 kg", "[length]")


@given(
    st.floats(min_value=-1e6, max_value=1e6, allow_nan=False),
    st.sampled_from(["in", "mm", "ft", "degF", "degC", "kW", "BTU/hr", "A", "V", "USD/kWh"]),
)
def test_format_round_trips(magnitude: float, unit: str) -> None:
    quantity = Q_(magnitude, unit)
    again = parse_quantity(format_quantity(quantity))
    assert again.units == quantity.units
    assert again.magnitude == pytest.approx(magnitude, rel=1e-11, abs=1e-11)
