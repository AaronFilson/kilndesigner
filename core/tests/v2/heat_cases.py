"""The reference kilns' firings as heat-model runs, for the reference-firing tests.

Each case is a kiln's design file plus what the book doesn't print and the model needs, each a
stated test input (not engineering data) with its question in `docs/planning/11-09-26.md` §I: the
setting's load and envelope above all (ADR 0017 decision 11: no heat result without a load).

Filled in with the firing model (build order step 6); until then each case says so.
"""

from __future__ import annotations

from typing import Protocol


class Outcome(Protocol):
    """What a reference-firing test reads from a run."""

    @property
    def completed(self) -> bool: ...

    @property
    def worst_air_share(self) -> float: ...

    @property
    def fuel_kg(self) -> float: ...

    def reached(self, t_setting: float) -> float | None: ...


def _not_built() -> Outcome:
    raise NotImplementedError("the firing model (build order step 6) isn't built yet")


def fast_fire_max() -> Outcome:
    return _not_built()


def fast_fire_log() -> Outcome:
    return _not_built()


def w15_ifb() -> Outcome:
    return _not_built()


def crossdraft_36() -> Outcome:
    return _not_built()
