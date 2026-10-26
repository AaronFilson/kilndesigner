"""Orton cones as temperatures, by the heating rate over the end of the firing.

Cones 022 to 14 are self-supporting cones. Above 14 Orton makes only large and PCE cones, and
their equivalents are published at fewer heating rates, so a cone may have no value at a rate:
asking for it is refused with the rates that are tabulated (ADR 0009).
"""

from __future__ import annotations

from functools import cache
from importlib import resources
from typing import Any

import yaml

from kilndesigner.units import Q_, Quantity

CONE_SOURCE = "Orton cone charts; cones.md and electric-and-thermal.md §8"


@cache
def _table() -> tuple[tuple[int, ...], dict[str, tuple[int | None, ...]]]:
    text = resources.files("kilndesigner.data").joinpath("cones.yaml").read_text(encoding="utf-8")
    data: Any = yaml.safe_load(text)
    rates = tuple(int(r) for r in data["rates_c_per_hour"])
    cones = {
        str(k): tuple(None if v is None else int(v) for v in vs) for k, vs in data["cones"].items()
    }
    return rates, cones


def normalise(cone: str) -> str:
    """Accept '10', '06', '05½' or '5 1/2'-style input; return the table's key."""
    return cone.strip().replace("½", ".5").replace(" 1/2", ".5")


def cone_names() -> tuple[str, ...]:
    """The cones in the table, coolest first."""
    return tuple(_table()[1])


def cone_rates(cone: str) -> tuple[int, ...]:
    """The heating rates (°C/h) at which a cone's temperature is tabulated."""
    rates, cones = _table()
    key = normalise(cone)
    if key not in cones:
        names = cone_names()
        raise ValueError(f"cone {cone!r} is not in the Orton table ({names[0]} to {names[-1]})")
    return tuple(r for r, v in zip(rates, cones[key], strict=True) if v is not None)


def cone_temperature(cone: str, rate_c_per_hour: int = 60) -> Quantity:
    rates, cones = _table()
    available = cone_rates(cone)
    if rate_c_per_hour not in rates:
        raise ValueError(f"cone temperatures are tabulated at {rates} °C/h")
    if rate_c_per_hour not in available:
        shown = ", ".join(f"{r} °C/h" for r in available)
        raise ValueError(
            f"Orton publishes cone {cone} only at {shown}; set the firing's final_rate to match"
        )
    value = cones[normalise(cone)][rates.index(rate_c_per_hour)]
    assert value is not None
    return Q_(value, "degC")
