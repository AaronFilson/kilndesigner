"""v2's zones in series (`heat/series.py`): two chambers in a row, the gas leaving the first at its
temperature into the second; one zone alone is `firing.fire`'s zone; the balance closes."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import heat_cases as hc
import numpy as np
import pytest

from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat import series as se
from kilndesigner.v2.heat.zone import Opening, ZoneModel

pytestmark = [pytest.mark.slow, pytest.mark.geometry]
HOUR = 3600.0
# The second chamber's door to the first: the 9 × 4½ in flue at the foot of its front wall
HOLE = {"spy_holes": {"holes": [{"port": {"width": "9 in", "height": "4.5 in"},
                                 "wall": "front", "up": "2.25 in"}]}}  # fmt: skip


def _relink(m: ZoneModel, swap: dict[str, Opening]) -> ZoneModel:
    return replace(m, openings=tuple(swap.get(o.name, o) for o in m.openings))


@pytest.fixture(scope="module")
def pair() -> tuple[ZoneModel, ZoneModel, float]:
    """Two of W15's IFB cubes in a row (test inputs, `heat_cases.py`): the burners in the first,
    its exit flue into the second, the second's own flue out."""
    k1 = hc._crossdraft(hc.FLUE | hc.IFB)  # pyright: ignore[reportPrivateUsage]
    k2 = hc._crossdraft(hc.FLUE | hc.IFB | HOLE)  # pyright: ignore[reportPrivateUsage]
    m1 = hk.heat_model(k1, hc.CROSSDRAFT_LOAD, 1.15, n_rays=20_000)
    m2 = hk.heat_model(k2, hc.CROSSDRAFT_LOAD, 1.15, n_rays=20_000)
    first = _relink(m1, {"exit flue": Opening("exit flue", "zone", zone=1)})
    second = _relink(m2, {"spy hole 1": Opening("spy hole 1", "zone", zone=0)})
    return first, second, hc._burners(k1, m1)  # pyright: ignore[reportPrivateUsage]


def test_one_zone_alone_is_the_single_zone(pair: tuple[Any, Any, float]) -> None:
    m = hk.heat_model(hc._crossdraft(hc.FLUE | hc.IFB), hc.CROSSDRAFT_LOAD, 1.15, n_rays=20_000)  # pyright: ignore[reportPrivateUsage]
    fuel = pair[2]
    one = se.fire_series([m], fi.FixedInput(fuel), 2 * HOUR)
    alone = fi.fire(m, fi.FixedInput(fuel), 2 * HOUR)
    assert one.t_setting[-1, 0] == pytest.approx(alone.t_setting[-1], abs=0.05)
    assert one.t_gas[-1, 0] == pytest.approx(alone.t_gas[-1], abs=0.05)
    assert one.energy["flue"] == pytest.approx(alone.energy["flue"], rel=1e-4)


def test_two_chambers_in_a_row(pair: tuple[Any, Any, float]) -> None:
    """The second chamber's gas is cooler than the first's and its setting lags; the fuel's heat
    is the flue, the walls, the settings and the openings and links, to round-off."""
    first, second, fuel = pair
    f = se.fire_series([first, second], fi.FixedInput(fuel), 6 * HOUR, targets=((0, 1173.15),))
    assert np.all(f.t_gas[10:, 0] > f.t_gas[10:, 1])
    assert f.t_setting[-1, 0] > f.t_setting[-1, 1] + 50
    e = f.energy
    closure = e["fuel heat"] - e["flue"] - e["walls"] - e["setting"] - e["openings"]
    assert abs(closure) < 1e-6 * e["fuel heat"]
    assert e["flue"] > 0
    t900 = f.reached(0, 1173.15)
    assert t900 is not None
    assert t900 < 6 * HOUR
    assert f.reached(1, 1173.15) is None
    assert f.steps[0].name == "Zones in series"


def test_a_schedule_held_in_the_first_zone(pair: tuple[Any, Any, float]) -> None:
    first, second, _ = pair
    pts = ((0.0, 294.26), (HOUR, 900.0), (2 * HOUR, 1100.0))
    for held in ("gas", "setting"):
        f = se.fire_series([first, second], fi.Schedule(held, pts), 2 * HOUR,  # pyright: ignore[reportArgumentType]
                           stop_at=(0, 2000.0))  # fmt: skip
        col = f.t_gas if held == "gas" else f.t_setting
        assert col[-1, 0] == pytest.approx(1100.0, abs=0.01)
        assert f.fuel_rate[-1] > 0


def test_one_fuel_for_the_row(pair: tuple[Any, Any, float]) -> None:
    first, second, fuel = pair
    other = hk.heat_model(hc._crossdraft(hc.FLUE | hc.IFB), hc.CROSSDRAFT_LOAD, 1.0, n_rays=5_000)  # pyright: ignore[reportPrivateUsage]
    with pytest.raises(fi.FiringError, match="one fuel"):
        se.fire_series([first, other], fi.FixedInput(fuel), HOUR)
    f = se.fire_series([first, second], fi.FixedInput(fuel), 12 * HOUR, stop_at=(0, 1000.0))
    assert f.reached(0, 1000.0) is not None
    assert f.times[-1] < 12 * HOUR
