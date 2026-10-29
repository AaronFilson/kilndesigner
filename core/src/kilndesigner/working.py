"""The working behind a result: each step's formula, inputs, value and reference.

The plans print the working, so a builder or an inspector can check every number.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from kilndesigner.sheet import Check
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
    """Something the builder must know: a limit exceeded, an assumption, a safety note. A warning
    or an error carries the check that raised it: its formulas, inputs and sources (ADR 0013)."""

    model_config = ConfigDict(frozen=True)

    level: Literal["info", "warning", "error"]
    message: str
    reference: str | None = None
    check: Check | None = None

    @model_validator(mode="after")
    def _raised_by_its_check(self) -> Finding:
        if self.level != "info" and (self.check is None or self.check.status != self.level):
            raise ValueError(
                f"a {self.level} is raised by a check that fails at that level, with its formulas "
                f"and inputs (ADR 0013): {self.message!r}"
            )
        return self

    @classmethod
    def failed(cls, check: Check, message: str, reference: str | None = None) -> Finding:
        """The finding a failed check raises, at the check's level."""
        if check.status == "pass":
            raise ValueError(f"{check.id} passed: there is nothing to report")
        return cls(
            level=check.status, message=message, reference=reference or check.reference, check=check
        )


def show(value: Quantity | float | str, unit: str | None = None, digits: int = 4) -> str:
    """Format a value for the working, optionally converted to ``unit``."""
    if isinstance(value, str):
        return value
    if isinstance(value, float | int):
        return f"{value:.{digits}g}"
    if unit is not None:
        value = value.to(unit)
    return f"{value.magnitude:.{digits}g} {value.units:~P}"


IN = 25.4  # mm
FRACTIONS = {1: "⅛", 2: "¼", 3: "⅜", 4: "½", 5: "⅝", 6: "¾", 7: "⅞"}


def length_text(mm: float, us: bool) -> str:
    """A thickness as a builder writes it: '13½ in', '6¾ in', or '343 mm'."""
    if not us:
        return f"{mm:.0f} mm"
    eighths = round(mm / IN * 8)
    if abs(eighths / 8 - mm / IN) > 0.01:
        return f"{mm / IN:.3g} in"
    whole, part = divmod(eighths, 8)
    return f"{whole or ''}{FRACTIONS[part]} in" if part else f"{whole} in"


__all__ = ["Finding", "Step", "format_quantity", "length_text", "show"]
