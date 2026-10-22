"""Orton cones as temperatures (self-supporting cones, by final heating rate)."""

from __future__ import annotations

from functools import cache
from importlib import resources
from typing import Any

import yaml

from kilndesigner.units import Q_, Quantity

CONE_SOURCE = "Orton cone chart (2016), self-supporting cones; electric-and-thermal.md §8 [S75]"


@cache
def _table() -> tuple[tuple[int, ...], dict[str, tuple[int, ...]]]:
    text = resources.files("kilndesigner.data").joinpath("cones.yaml").read_text(encoding="utf-8")
    data: Any = yaml.safe_load(text)
    rates = tuple(int(r) for r in data["rates_c_per_hour"])
    cones = {str(k): tuple(int(v) for v in vs) for k, vs in data["cones"].items()}
    return rates, cones


def normalise(cone: str) -> str:
    """Accept '10', '06', '05½' or '5 1/2'-style input; return the table's key."""
    return cone.strip().replace("½", ".5").replace(" 1/2", ".5")


def cone_temperature(cone: str, rate_c_per_hour: int = 60) -> Quantity:
    rates, cones = _table()
    key = normalise(cone)
    if key not in cones:
        raise ValueError(f"cone {cone!r} is not in the Orton table (022 to 14)")
    if rate_c_per_hour not in rates:
        raise ValueError(f"cone temperatures are tabulated at {rates} °C/h")
    return Q_(cones[key][rates.index(rate_c_per_hour)], "degC")
