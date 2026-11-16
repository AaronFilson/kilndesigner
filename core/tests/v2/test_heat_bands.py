"""Bands by corner runs (`heat/bands.py`): on functions whose bands are known."""

from __future__ import annotations

import math
from collections.abc import Hashable, Mapping

import pytest

from kilndesigner.v2.heat import bands

INPUTS = (
    bands.Input("x", (0.0, 1.0), 0.5, "test"),
    bands.Input("y", (2.0, 0.0), 1.0, "test"),
    bands.Input("z", (0.0, 1.0), 0.5, "test"),
)


def test_a_linear_result_spans_its_corners() -> None:
    """r = x + 2y − z over x, z ∈ [0, 1], y ∈ [0, 2]: the band is −1 to 5, its corners; s = −r
    the same reversed; each input's swing at its two ends; repeated settings run once."""
    calls: list[tuple[float, ...]] = []

    def run(s: Mapping[str, Hashable]) -> dict[str, float | None]:
        x, y, z = (float(s[k]) for k in "xyz")  # pyright: ignore[reportArgumentType]
        calls.append((x, y, z))
        return {"r": x + 2 * y - z, "s": -(x + 2 * y - z)}

    got = bands.corner_runs(run, INPUTS)
    r, s = got["r"], got["s"]
    assert (r.low, r.nominal, r.high) == pytest.approx((-1.0, 2.0, 5.0))
    assert (s.low, s.high) == pytest.approx((-5.0, 1.0))
    assert {n: (a, b) for n, a, b in r.swings}["y"] == pytest.approx((4.0, 0.0))
    assert len(calls) == len(set(calls)) == 1 + 6 + 2  # s's corners are r's
    assert r.holds(4.9)
    assert not r.holds(5.1)
    step = r.steps[0]
    assert step.name == "The band: r"
    assert next(iter(step.inputs)) == "y"  # the input that swings it most first


def test_a_result_not_given_is_infinite() -> None:
    def run(s: Mapping[str, Hashable]) -> dict[str, float | None]:
        return {"t": None if float(s["x"]) > 0.9 else 1.0}  # pyright: ignore[reportArgumentType]

    t = bands.corner_runs(run, INPUTS[:1])["t"]
    assert t.low == 1.0
    assert math.isinf(t.high)
    both = bands.corner_runs(run, INPUTS[:2])["t"]  # x's infinite swing sorts first, over y's
    assert next(iter(both.steps[0].inputs)) == "x"
    with pytest.raises(ValueError, match="each input once"):
        bands.corner_runs(run, (INPUTS[0], INPUTS[0]))
