"""v2's target times (`heat/target.py`): the time at a steady input, and the input for a time,
found by Brent's method around whole firings, on W15's IFB kiln (test inputs, `heat_cases.py`)."""

from __future__ import annotations

from typing import Any

import heat_cases as hc
import pytest

from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat import target as tg

pytestmark = [pytest.mark.slow, pytest.mark.geometry]
HOUR = 3600.0


@pytest.fixture(scope="module")
def w15() -> tuple[Any, float]:
    k = hc._crossdraft(hc.FLUE | hc.IFB)  # pyright: ignore[reportPrivateUsage]
    m = hk.heat_model(k, hc.CROSSDRAFT_LOAD, 1.15, n_rays=20_000)
    return m, hc._burners(k, m)  # pyright: ignore[reportPrivateUsage]


def test_more_input_is_sooner(w15: tuple[Any, float]) -> None:
    m, rated = w15
    slow = tg.time_at(m, rated, hc.CONE_10, 12 * HOUR)
    fast = tg.time_at(m, 1.5 * rated, hc.CONE_10, 12 * HOUR)
    assert slow is not None
    assert fast is not None
    assert fast < slow
    assert tg.time_at(m, 0.2 * rated, hc.CONE_10, 4 * HOUR) is None


def test_the_input_for_a_time_gives_that_time(w15: tuple[Any, float]) -> None:
    """The input for cone 10 in 6 h, fired again, takes 6 h (to the solve's tolerance)."""
    m, rated = w15
    r = tg.input_for(m, hc.CONE_10, 6 * HOUR, rated)
    assert r.fuel < rated  # W15's ten burners do it in about 4.4 h
    t = tg.time_at(m, r.fuel, hc.CONE_10, 12 * HOUR)
    assert t is not None
    assert t == pytest.approx(6 * HOUR, rel=0.005)
    assert r.steps[0].name == "The input for the time"
    assert r.firings >= 3


def test_targets_out_of_reach_are_refused(w15: tuple[Any, float]) -> None:
    m, rated = w15
    with pytest.raises(tg.TargetError, match="isn't reached"):
        tg.input_for(m, hc.CONE_10, 0.5 * HOUR, rated, most=2.0)
    with pytest.raises(tg.TargetError, match="is reached in under"):
        tg.input_for(m, hc.CONE_10, 11 * HOUR, rated, most=1.5)
