"""v2's zones in series from the design (`heat/series.py`, B3): chambers in a row and a tube cut
into segments as gas zones of one enclosure, the walls between chambers with a face in each, and
a staged firing with each chamber's stage time. The loads and the stoking rates are test inputs:
the book prints neither for these kilns."""

from __future__ import annotations

from functools import cache
from pathlib import Path

import numpy as np
import pytest

from kilndesigner.designfile import load_design
from kilndesigner.v2.heat import chamber as ch
from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat import series as se
from kilndesigner.v2.heat.zone import ZoneModel

pytestmark = [pytest.mark.slow, pytest.mark.geometry]
OLSEN = Path(__file__).resolve().parents[3] / "examples" / "olsen"
HOUR = 3600.0
WOOD = hk.Wood(0.12, 19e6, "TEST INPUT: FAO's air-dried 12 %, Forest Research's 19 MJ/kg")
CONE_10 = 1285 + 273.15


def _loads(c: ch.Chamber) -> list[hk.Load]:
    """TEST INPUT: each room's envelope 0.1 m in from its walls and floor, to 0.9 of its height,
    at 360 kg per m³ (the fast-fire's test setting, 55 kg in 0.152 m³)."""
    out = []
    for r in c.rooms:
        lo = (r.lo[0] + 0.1, r.lo[1] + 0.1, 0.1)
        hi = (r.hi[0] - 0.1, r.hi[1] - 0.1, 0.9 * r.hi[2])
        vol = float(np.prod(np.subtract(hi, lo)))
        out.append(hk.Load(360.0 * vol, lo, hi, 0.8, "TEST INPUT: 360 kg/m³ of envelope"))
    return out


@cache
def _model(name: str, segments: int = 1) -> ZoneModel:
    k = load_design(OLSEN / f"{name}.yaml")
    return hk.heat_model(k, _loads(ch.cavity(k, segments=segments)), 1.2, WOOD, n_rays=10_000,
                         segments=segments)  # fmt: skip


def test_two_chambers_in_a_row_fired_in_stages() -> None:
    """Olsen's two-chamber kiln: each chamber a zone, the wall between them a wall with a face in
    each; stoked in turn at a test rate, the first chamber's gas preheats the second, whose stage
    is the shorter; the stages' records join, the balance closing over both."""
    m = _model("olsen-two-chamber")
    between = next(f for f in m.faces if f.back)
    assert (between.name, between.back, between.zone, between.back_zone) == (
        "back 1", "front 2", 0, 1,
    )  # fmt: skip
    rate = 60.0 / 3600
    stages = [se.Stage(i, fi.FixedInput(rate), CONE_10, 30 * HOUR) for i in (0, 1)]
    s = se.fire_stages(m, stages, sample=1800.0)
    first, second = s.times
    assert first is not None
    assert second is not None
    assert second < first
    f = s.firing
    assert f.reached(CONE_10, 0) == pytest.approx(first, rel=1e-6)
    assert f.reached(CONE_10, 1) == pytest.approx(first + second, rel=1e-6)
    assert np.all(np.diff(f.times) > 0)
    e = f.energy
    closure = e["fuel heat"] - e["flue"] - e["walls"] - e["setting"] - e["openings"]
    assert abs(closure) < 1e-9 * e["fuel heat"]
    assert e["fuel kg"] == pytest.approx(rate * f.times[-1], rel=1e-6)
    assert s.steps[0].name == "The stages"
    assert se.stage_model(m, 1).burns == 1


def test_a_tube_in_segments_cools_along_its_length() -> None:
    """The anagama in a hole as a tube of four segments, the fire at its front: each segment's
    gas and setting cooler than the one before."""
    m = _model("anagama-hole", segments=4)
    assert len(m.gas) == 4
    f = fi.fire(m, fi.FixedInput(40.0 / 3600), 6 * HOUR, sample=1800.0)
    assert np.all(np.diff(f.t_gases[-1]) < 0)
    assert np.all(np.diff(f.t_settings[-1]) < 0)


def test_a_stage_short_of_its_target_and_a_zone_held() -> None:
    """A stage whose chamber doesn't reach its target in its limit has no time; a schedule held
    by another zone's gas holds that zone's."""
    m = _model("olsen-two-chamber")
    s = se.fire_stages(m, [se.Stage(0, fi.FixedInput(0.001), CONE_10, 600.0)], sample=300.0)
    assert s.times == (None,)
    assert "not in" in s.steps[0].value
    pts = ((0.0, 294.26), (1800.0, 700.0))
    f = fi.fire(m, fi.Schedule("gas", pts, zone=1), 1800.0, sample=300.0)
    assert f.t_gases[-1, 1] == pytest.approx(700.0, abs=0.01)


def test_what_a_staged_firing_refuses() -> None:
    m = _model("olsen-two-chamber")
    with pytest.raises(fi.FiringError, match="no chamber 3"):
        se.stage_model(m, 2)
    with pytest.raises(fi.FiringError, match="needs a stage"):
        se.fire_stages(m, [])
    with pytest.raises(fi.FiringError, match="carries on"):
        fi.fire(m, fi.FixedInput(0.01), 60.0, start=np.zeros(3))
    with pytest.raises(hk.NotModelledError, match="one load for each"):
        hk.heat_model(load_design(OLSEN / "olsen-two-chamber.yaml"), _loads(
            ch.cavity(load_design(OLSEN / "olsen-two-chamber.yaml")))[:1], 1.2, WOOD,
            n_rays=1_000)  # fmt: skip
