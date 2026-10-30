"""One Pint registry for the whole engine, and the quantity types the design file uses (ADR 0004).

Every physical value in a design is a quantity with a unit, written as text: ``"9 in"``,
``"2345 degF"``, ``"240 V"``, ``"0.12 USD/kWh"``. A bare number is rejected, because a bare
number in a kiln design is a unit mistake waiting to happen.

The solvers work in SI on plain floats; :func:`si` is the one place units are stripped.
"""

from __future__ import annotations

import re
from typing import Annotated, Any

import pint
from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

ureg = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)
ureg.define("USD = [currency] = $")
ureg.define("pcf = pound / foot ** 3")
Q_ = ureg.Quantity  # pyright: ignore[reportInvalidTypeForm]  # Pint's registry-bound class

Quantity = pint.Quantity

_NUMBER_AND_UNIT = re.compile(r"^\s*([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)\s*(.*?)\s*$")


class UnitError(ValueError):
    """A value has no unit, an unknown unit, or the wrong kind of unit."""


def parse_quantity(text: str, dimension: str | None = None) -> Quantity:
    """Parse ``"<number> <unit>"`` into a quantity, checking its dimension if one is given.

    The number and the unit are parsed separately, so offset temperatures such as
    ``"2345 degF"`` work (Pint refuses to multiply a number by an offset unit).
    """
    match = _NUMBER_AND_UNIT.match(text)
    if match is None:
        raise UnitError(f"{text!r} is not a number followed by a unit")
    number, unit = match.groups()
    if not unit:
        raise UnitError(f"{text!r} has no unit; write it as, for example, '{number} in'")
    try:
        units = ureg.parse_units(unit)
    except (pint.UndefinedUnitError, pint.DefinitionSyntaxError, AttributeError, TypeError) as e:
        raise UnitError(f"{unit!r} in {text!r} is not a unit Kilndesigner knows") from e
    quantity = Q_(float(number), units)
    if dimension is not None and not quantity.check(dimension):
        raise UnitError(f"{text!r} is not a {_DIMENSION_NAMES.get(dimension, dimension)}")
    return quantity


def format_quantity(quantity: Quantity) -> str:
    """Write a quantity back as text that :func:`parse_quantity` reads unchanged."""
    return f"{quantity.magnitude:.12g} {quantity.units:~}"


def si(quantity: Quantity, unit: str) -> float:
    """The magnitude of ``quantity`` in ``unit``, as a plain float for the solvers."""
    return float(quantity.to(unit).magnitude)


_DIMENSION_NAMES = {
    "[length]": "length",
    "[length] ** 2": "area",
    "[length] ** 3": "volume",
    "[temperature]": "temperature",
    "[mass]": "mass",
    "[power]": "power",
    "[current]": "current",
    "[electric_potential]": "voltage",
    "[pressure]": "pressure",
    "[currency] / [energy]": "price per unit of energy",
    "[currency] / [volume]": "price per unit of volume",
    "[currency] / [mass]": "price per unit of mass",
    "[currency]": "amount of money",
    "[mass] / [length] ** 3": "density",
    "[mass] / [time] ** 2": "spring rate (force per length)",
    "[]": "angle",
    "[length] ** 3 / [time]": "flow (volume per time)",
    "[temperature] / [time]": "heating rate (temperature per time)",
    "[time]": "time",
    "[length] ** 2 / [time] ** 2 / [temperature]": "specific heat",
}


class QuantityField:
    """Pydantic metadata for a quantity of one dimension, read from and written as text."""

    def __init__(self, dimension: str, example: str) -> None:
        self.dimension = dimension
        self.example = example

    def validate(self, value: Any) -> Quantity:
        if isinstance(value, pint.Quantity):
            if not value.check(self.dimension):
                raise UnitError(f"{value} is not a {_DIMENSION_NAMES[self.dimension]}")
            return value
        if isinstance(value, str):
            return parse_quantity(value, self.dimension)
        if isinstance(value, int | float):
            raise UnitError(f"{value} has no unit; write it as, for example, '{self.example}'")
        raise UnitError(f"{value!r} is not a quantity")

    def __get_pydantic_core_schema__(
        self, source: type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(
            self.validate,
            serialization=core_schema.plain_serializer_function_ser_schema(format_quantity),
        )

    def __get_pydantic_json_schema__(
        self, schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        name = _DIMENSION_NAMES[self.dimension]
        return {
            "type": "string",
            "description": f"A {name} with a unit, for example '{self.example}'",
            "examples": [self.example],
        }


Length = Annotated[pint.Quantity, QuantityField("[length]", "9 in")]
Temperature = Annotated[pint.Quantity, QuantityField("[temperature]", "2345 degF")]
Power = Annotated[pint.Quantity, QuantityField("[power]", "11.5 kW")]
Current = Annotated[pint.Quantity, QuantityField("[current]", "48 A")]
Voltage = Annotated[pint.Quantity, QuantityField("[electric_potential]", "240 V")]
Pressure = Annotated[pint.Quantity, QuantityField("[pressure]", "11 inch_H2O")]
EnergyPrice = Annotated[pint.Quantity, QuantityField("[currency] / [energy]", "0.12 USD/kWh")]
VolumePrice = Annotated[pint.Quantity, QuantityField("[currency] / [volume]", "3.50 USD/gallon")]
Money = Annotated[pint.Quantity, QuantityField("[currency]", "5000 USD")]
Mass = Annotated[pint.Quantity, QuantityField("[mass]", "50 lb")]
Density = Annotated[pint.Quantity, QuantityField("[mass] / [length] ** 3", "2.6 g/cm**3")]
MassPrice = Annotated[pint.Quantity, QuantityField("[currency] / [mass]", "1.02 USD/lb")]
SpringRate = Annotated[pint.Quantity, QuantityField("[mass] / [time] ** 2", "283 lbf/in")]
Angle = Annotated[pint.Quantity, QuantityField("[]", "20 degree")]
Flow = Annotated[pint.Quantity, QuantityField("[length] ** 3 / [time]", "2 gallon/hour")]
Rate = Annotated[pint.Quantity, QuantityField("[temperature] / [time]", "200 delta_degF/hour")]
Duration = Annotated[pint.Quantity, QuantityField("[time]", "30 minute")]
SpecificHeat = Annotated[
    pint.Quantity, QuantityField("[length] ** 2 / [time] ** 2 / [temperature]", "1.0 kJ/(kg*K)")
]
