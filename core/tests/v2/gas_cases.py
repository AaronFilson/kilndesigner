"""Part C2's gas and electric kilns as heat-model runs (`docs/planning/11-10-26.md` §C, "C2 as
built"): each kiln's own setting band (`loads.py`), its burners at its supply's pressure
(`burners.design_input`) or its elements as face sources, and v2's band over the inputs no source
fixes (`bands.py`'s corner runs).

**λ is the operator's setting.** No gas kiln here has a draft path yet (part C1), so the air its
venturi burners and ports take isn't worked out: λ runs from 1.0, the most heat any air ratio
leaves, to 1.15, 3 % O₂, v1's oxidising air ratio (the W15 test's), and the band carries both.

Nothing here is fitted: each input is the book's, the dataset's (each with its source) or a stated
band's end.
"""

from __future__ import annotations

from collections.abc import Hashable, Mapping
from dataclasses import replace
from functools import cache
from typing import Any

import loads

from kilndesigner.cones import cone_temperature
from kilndesigner.units import Q_, si
from kilndesigner.v2.heat import bands
from kilndesigner.v2.heat import burners as bu
from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import kiln as hk

HOUR = 3600.0
BTU_HR = si(Q_(1, "BTU/hr"), "W")
BAND_RAYS = 20_000
LAMBDA = (1.0, 1.15)
LAMBDA_SOURCE = (
    "the operator's (no draft path yet, part C1): λ 1, the most heat any air ratio leaves, to "
    "1.15, 3 % O₂, v1's oxidising air ratio (the W15 test's)"
)
LOAD_SOURCE = "kiln-settings.md: the kiln's setting band (the dataset's `setting` facts)"
TIME = "time to its cone (h)"
INPUTS = (
    bands.Input("the load", ("least", "most"), "mid", LOAD_SOURCE),
    bands.Input("λ", LAMBDA, LAMBDA[0], LAMBDA_SOURCE),
)


def cone(kid: str) -> float:
    """The design's target (K): its cone at its final rate, or its top temperature."""
    f = loads.design(kid).firing
    if f.top_temperature is not None:
        return si(f.top_temperature, "K")
    return si(cone_temperature(str(f.cone), f.final_rate), "K")


@cache
def model(kid: str, lam: float = 1.0, segments: int = 1, n_rays: int = BAND_RAYS) -> Any:
    """The kiln's zone model at λ, its load at its band's middle (the corner runs set the mass)."""
    k = loads.design(kid)
    return hk.heat_model(k, loads.loads(kid, "mid", segments), lam, n_rays=n_rays,
                         segments=segments)  # fmt: skip


def burners(kid: str) -> bu.Input:
    """The design's burners at its supply's pressure (ADR 0017 decision 13)."""
    return bu.design_input(loads.design(kid))


def fuel_rate(kid: str, m: Any) -> float:
    """The burners' input as fuel (kg/s), the rating on the gas's higher heating value."""
    return burners(kid).total * BTU_HR / m.products.fuel.hhv


def at_end(kid: str, m: Any, end: loads.End, segments: int = 1) -> Any:
    """The model with each setting's mass at its band's end."""
    masses = [x.mass for x in loads.loads(kid, end, segments)]
    return replace(m, settings=tuple(replace(s, mass=w) for s, w in
                                     zip(m.settings, masses, strict=True)))  # fmt: skip


@cache
def time_to_cone(kid: str, end: loads.End = "mid", lam: float = 1.0, hours: float = 48.0,
                 n_rays: int = BAND_RAYS) -> float | None:  # fmt: skip
    """Hours to the design's cone with the burners at their supply's pressure (fixed input), or
    the elements full on; None if not reached in ``hours``."""
    m = at_end(kid, model(kid, lam, 1, n_rays), end)
    target = cone(kid)
    mode: fi.Mode = (fi.MaxFire() if m.elements is not None
                     else fi.FixedInput(fuel_rate(kid, m)))  # fmt: skip
    t = fi.fire(m, mode, hours * HOUR, (), target, sample=600.0).reached(target)
    return None if t is None else t / HOUR


def run(kid: str, s: Mapping[str, Hashable]) -> dict[str, float | None]:
    """One band run: the time to the cone at the band's corner ``s``."""
    lam = float(s["λ"]) if "λ" in s else 1.0  # pyright: ignore[reportArgumentType]
    return {TIME: time_to_cone(kid, s["the load"], lam)}  # pyright: ignore[reportArgumentType]


@cache
def band(kid: str) -> bands.Band:
    """v2's band for the time to the cone over the load's and λ's ends (an electric kiln's over
    the load's alone: no combustion air)."""
    electric = loads.design(kid).heat.electric is not None
    inputs = INPUTS[:1] if electric else INPUTS
    return bands.corner_runs(lambda s: run(kid, s), inputs)[TIME]
