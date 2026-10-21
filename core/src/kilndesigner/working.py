"""The working behind a result: each step's formula, inputs, value and reference.

The plans print the working, so a builder or an inspector can check every number.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from kilndesigner.units import Quantity, format_quantity


class Step(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    value: str
    formula: str | None = None
    inputs: dict[str, str] = Field(default_factory=dict)
    reference: str | None = None
    note: str | None = None


class Finding(BaseModel):
    """Something the builder must know: a limit exceeded, an assumption, a safety note."""

    model_config = ConfigDict(frozen=True)

    level: Literal["info", "warning", "error"]
    message: str
    reference: str | None = None


def show(value: Quantity | float | str, unit: str | None = None, digits: int = 4) -> str:
    """Format a value for the working, optionally converted to ``unit``."""
    if isinstance(value, str):
        return value
    if isinstance(value, float | int):
        return f"{value:.{digits}g}"
    if unit is not None:
        value = value.to(unit)
    return f"{value.magnitude:.{digits}g} {value.units:~P}"


__all__ = ["Finding", "Step", "format_quantity", "show"]
