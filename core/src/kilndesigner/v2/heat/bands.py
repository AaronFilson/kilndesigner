"""Bands (ADR 0017 decisions 4 and 17): each uncertain input's band carried to the results, so a
printed figure can be tested inside v2's band.

**Corner runs.** The nominal run; each input at each end of its band with the rest nominal (its
swing, which also says which end raises each result); then, for each result, the two corners: every
input at the end that lowers it, and every input at the end that raises it. The result's band runs
from the least to the most of all those runs (the corners are its ends unless the result isn't
monotone in an input, which the swings would show). 2n + 1 runs and two more per result, each run
shared by every result it gives; a run repeated with the same inputs is run once. A result a run
can't give (a cone not reached) is +∞.

What the inputs are and how a run uses them is the caller's (`Input.ends`, the runner): v2's own
are listed where its models take them (the emissivity class and the grey gases, `kiln.py`; the
draft's band, `draft.Path.most`; the fuel's, `gas.solid`; the setting's passages, `sources`).
"""

from __future__ import annotations

import math
from collections.abc import Callable, Hashable, Mapping, Sequence
from dataclasses import dataclass, field

from kilndesigner.working import Step


@dataclass(frozen=True)
class Input:
    """An uncertain input: its band's two ends and its nominal value, as the runner takes them,
    and where the band comes from."""

    name: str
    ends: tuple[Hashable, Hashable]
    nominal: Hashable
    reference: str


@dataclass(frozen=True)
class Band:
    """A result's band: the nominal run's value, the least and the most of every run, and each
    input's swing (the result at its two ends, the rest nominal)."""

    result: str
    nominal: float
    low: float
    high: float
    swings: tuple[tuple[str, float, float], ...]
    steps: tuple[Step, ...] = field(default=())

    def holds(self, value: float) -> bool:
        """Whether a value lies inside the band."""
        return self.low <= value <= self.high


type Runner = Callable[[Mapping[str, Hashable]], Mapping[str, float | None]]


def corner_runs(run: Runner, inputs: Sequence[Input]) -> dict[str, Band]:
    """Each result's band over the inputs' bands (the module's corner runs)."""
    names = [i.name for i in inputs]
    if len(set(names)) != len(names):
        raise ValueError("each input once")
    done: dict[tuple[Hashable, ...], Mapping[str, float]] = {}

    def at(settings: Mapping[str, Hashable]) -> Mapping[str, float]:
        key = tuple(settings[n] for n in names)
        if key not in done:
            done[key] = {k: math.inf if v is None else float(v) for k, v in run(settings).items()}
        return done[key]

    base = {i.name: i.nominal for i in inputs}
    nominal = at(base)
    ends = {(i.name, k): at({**base, i.name: e}) for i in inputs for k, e in enumerate(i.ends)}
    bands: dict[str, Band] = {}
    for res, value in nominal.items():
        low_set = dict(base)
        high_set = dict(base)
        swings: list[tuple[str, float, float]] = []
        for i in inputs:
            a, b = ends[(i.name, 0)][res], ends[(i.name, 1)][res]
            swings.append((i.name, a, b))
            low_set[i.name], high_set[i.name] = (i.ends[0], i.ends[1]) if a <= b else i.ends[::-1]
        runs = [value, at(low_set)[res], at(high_set)[res]] + [x for _, a, b in swings
                                                             for x in (a, b)]  # fmt: skip
        band = Band(res, value, min(runs), max(runs), tuple(swings))
        bands[res] = Band(res, value, band.low, band.high, band.swings, (_step(band, inputs),))
    return bands


def _step(b: Band, inputs: Sequence[Input]) -> Step:
    """The band's working: its ends, and the inputs by how far each swings it."""
    order = sorted(b.swings, key=lambda s: -abs(s[2] - s[1]) if math.isfinite(s[2] - s[1]) else 0)
    return Step(
        name=f"The band: {b.result}",
        value=f"{b.low:.4g}–{b.high:.4g} (nominal {b.nominal:.4g})",
        formula="corner runs: each input at each end with the rest nominal, then every input at "
        "the end that lowers the result and at the end that raises it (ADR 0017 decision 17)",
        inputs={name: f"{lo:.4g} / {hi:.4g}" for name, lo, hi in order},
        reference="; ".join(f"{i.name}: {i.reference}" for i in inputs),
    )
