import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import BaseModel, ValidationError

from kilndesigner.units import (
    Q_,
    Length,
    Temperature,
    UnitError,
    format_quantity,
    parse_quantity,
    si,
)


class Brick(BaseModel):
    """A model with quantity fields, as the design file has."""

    length: Length
    rated: Temperature


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


def test_a_field_reads_text_and_keeps_a_quantity_it_is_given() -> None:
    brick = Brick.model_validate({"length": "9 in", "rated": Q_(2300, "degF")})
    assert si(brick.length, "mm") == pytest.approx(228.6)
    assert si(brick.rated, "degF") == pytest.approx(2300)
    assert brick.model_dump(mode="json") == {"length": "9 in", "rated": "2300 °F"}


def test_a_field_refuses_a_quantity_of_the_wrong_kind() -> None:
    with pytest.raises(ValidationError, match="9 kilogram is not a length"):
        Brick.model_validate({"length": Q_(9, "kg"), "rated": "2300 degF"})


@pytest.mark.parametrize(
    ("value", "message"),
    [
        (9, "9 has no unit; write it as, for example, '9 in'"),
        (4.5, "4.5 has no unit"),
        ([9, "in"], r"\[9, 'in'\] is not a quantity"),
        (None, "None is not a quantity"),
    ],
)
def test_a_field_refuses_anything_but_a_quantity(value: object, message: str) -> None:
    with pytest.raises(ValidationError, match=message):
        Brick.model_validate({"length": value, "rated": "2300 degF"})


def test_the_json_schema_asks_for_text_with_a_unit() -> None:
    schema = Brick.model_json_schema()["properties"]
    assert schema["length"] == {
        "type": "string",
        "description": "A length with a unit, for example '9 in'",
        "examples": ["9 in"],
        "title": "Length",  # pydantic's, from the field name
    }
    assert schema["rated"]["description"] == "A temperature with a unit, for example '2345 degF'"


@given(
    st.floats(min_value=-1e6, max_value=1e6, allow_nan=False),
    st.sampled_from(["in", "mm", "ft", "degF", "degC", "kW", "BTU/hr", "A", "V", "USD/kWh"]),
)
def test_format_round_trips(magnitude: float, unit: str) -> None:
    quantity = Q_(magnitude, unit)
    again = parse_quantity(format_quantity(quantity))
    assert again.units == quantity.units
    assert again.magnitude == pytest.approx(magnitude, rel=1e-11, abs=1e-11)
