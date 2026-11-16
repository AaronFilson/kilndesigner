"""A row fired in stages, each on its own draft (`heat/series.py`, C3b): the front firebox's stage
on the front's path, then each chamber's on its side holes beside the front's path or alone with
the fire mouth shut (`paths.Inputs.stage`); max fire, a ramp held to a time, a fixed rate or a
schedule; the state carried from stage to stage. On Olsen's two-chamber kiln (p.206) with its
setting at its band's middle (`loads.py`); the wood a test input."""

from __future__ import annotations

from dataclasses import replace
from functools import cache
from typing import Literal

import loads
import numpy as np
import path_inputs as pi
import pytest

from kilndesigner.v2.heat import draft as dr
from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat import series as se
from kilndesigner.v2.heat.zone import Balance, ZoneModel

pytestmark = [pytest.mark.slow, pytest.mark.geometry]
KID = "olsen-two-chamber"
HOUR = 3600.0
WOOD = hk.Wood(0.12, 19e6, "TEST INPUT: FAO's air-dried 12 %, Forest Research's 19 MJ/kg")
RED = 1000 + 273.15  # the Kyoto kilns' side stoking begins at about 1000 °C (Olsen p.93, p.86)
CONE_11 = 1294 + 273.15


@cache
def _model() -> ZoneModel:
    k = loads.design(KID)
    return hk.heat_model(k, loads.loads(KID, "mid"), 1.0, WOOD, n_rays=4_000, path=True,
                         path_inputs=pi.inputs(KID))  # fmt: skip


@cache
def _path(stage: int, front_open: bool = True) -> dr.Path:
    return dr.kiln_path(loads.design(KID), inputs=pi.inputs(KID, stage=stage,
                                                            front_open=front_open))  # fmt: skip


def _front(limit: float = 30 * HOUR) -> se.Stage:
    """The front firebox's stage: its zone burns, on the front's own path, to 1000 °C."""
    m = _model()
    return se.Stage(0, fi.MaxFire(), RED, limit, m.path, m.burns, True, "the front")


def test_each_stage_at_max_fire_on_its_own_draft() -> None:
    """The front firebox brings chamber 1 to 1000 °C, then each chamber is side-stoked to cone 11
    as hard as its own path draws: each stage's fuel is the air it draws at λ 1, burnt in its own
    zone; the stages' times and fuels add up to the joined record's, whose balance closes."""
    m = _model()
    assert [g.name for g in m.gas] == ["firebox", "chamber 1", "chamber 2"]
    stages = [_front(), *(se.Stage(j, fi.MaxFire(), CONE_11, 30 * HOUR, _path(j)) for j in (0, 1))]
    s = se.fire_stages(m, stages, sample=1800.0)
    assert all(t is not None and t > 0 for t in s.times)
    assert s.total == pytest.approx(sum(t for t in s.times if t is not None))
    f = s.firing
    assert f.reached(CONE_11, 1) == pytest.approx(s.total, rel=1e-6)
    assert sum(s.fuel) == pytest.approx(f.fuel_kg, rel=1e-9)
    assert all(w > 0 for w in s.fuel)
    assert np.allclose(f.lam, 1.0, atol=1e-3)  # max fire: all the air burns the fuel at λ 1
    e = f.energy
    closure = e["fuel heat"] - e["flue"] - e["walls"] - e["setting"] - e["openings"]
    assert abs(closure) < 1e-6 * e["fuel heat"]
    parts = [p for p in s.parts if p is not None]
    assert [p.gas for p in parts] == [f.gas] * 3
    assert "max fire on its draft" in s.steps[0].value
    assert "the fire mouth open" in (s.steps[0].note or "")
    assert se.stage_model(m, 1).burns == 2
    assert se.stage_model(m, 1, _path(1)).path is _path(1)


def test_the_fire_mouth_shut_passes_no_stream_through_the_front() -> None:
    """With the fire mouth shut (C1's question 3, the band's other end) the stoked chamber's air
    comes through its side holes alone: no stream through the zones before it, whose gas is
    still (their settings' convection Churchill–Chu's alone, no flow in their passages)."""
    m = _model()
    shut = se.stage_model(m, 1, _path(1, False), front_open=False)
    assert (shut.burns, shut.enters) == (2, 2)
    tg = np.array([900.0, 1200.0, 1400.0])
    released = Balance(shut).released(tg, 0.01)
    assert released[:2] == pytest.approx([0.0, 0.0])
    assert released[2] > 0
    temps = np.full(len(m.names), 800.0)
    i = m.names.index("setting 1")
    tight = tuple(replace(x, gap=0.005) for x in m.settings)  # its passages' value the larger
    h_open = Balance(replace(se.stage_model(m, 1), settings=tight)).convection(tg, 0.01, temps)
    h_shut = Balance(replace(shut, settings=tight)).convection(tg, 0.01, temps)
    assert h_shut[i] < 0.5 * h_open[i]
    assert h_shut[m.names.index("setting 2")] == pytest.approx(h_open[m.names.index("setting 2")])
    stages = [_front(), se.Stage(1, fi.MaxFire(), CONE_11, 2 * HOUR, _path(1, False),
                                 front_open=False)]  # fmt: skip
    s = se.fire_stages(m, stages, sample=1800.0)
    assert "the fire mouth shut" in s.steps[0].value


def test_a_stage_held_to_the_books_time_on_either_air() -> None:
    """A ramp: the stoked chamber's setting held to a straight line from where the front's stage
    left it to cone 11 in 3 h, the fuel what that takes; with all the air its draft draws (λ from
    the draft) it burns more than with the stoker's (λ at the products')."""
    m = _model()
    fuel: list[float] = []
    airs: tuple[Literal["stoker", "draft"], ...] = ("stoker", "draft")
    for air in airs:
        ramp = se.Stage(1, se.Ramp(3 * HOUR, air), CONE_11, 0.0, _path(1))
        s = se.fire_stages(m, [_front(), ramp], sample=1800.0)
        assert s.times[1] == pytest.approx(3 * HOUR, rel=1e-3)
        assert f"held to a 3.0 h ramp, the {'stoker' if air == 'stoker' else 'draft'}" in (
            s.steps[0].value
        )
        fuel.append(s.fuel[1])
    assert fuel[1] > fuel[0]


def test_stages_on_a_fixed_rate_and_a_schedule_carry_the_state_across_layouts() -> None:
    """Max fire's draft air is an unknown of its own: a fixed rate or a schedule after it carries
    on without it, and max fire after them takes it again from what the path draws."""
    m = _model()
    stages = [
        _front(),
        se.Stage(0, fi.FixedInput(0.01), CONE_11, 0.5 * HOUR, _path(0)),
        se.Stage(1, fi.MaxFire(), CONE_11, 30 * HOUR, _path(1)),
    ]
    s = se.fire_stages(m, stages, sample=1800.0)
    assert s.times[1] is None  # 36 kg/h doesn't bring it to cone 11 in half an hour
    assert s.times[2] is not None
    assert s.total is None
    assert "36 kg/h" in s.steps[0].value
    assert "not in 0.5 h" in s.steps[0].value
    held = fi.Schedule("gas", ((0.0, 1300.0), (0.5 * HOUR, 1350.0)), zone=2)
    t = se.fire_stages(m, [_front(), se.Stage(1, held, CONE_11, 0.5 * HOUR, _path(1))],
                       sample=1800.0)  # fmt: skip
    assert "a schedule" in t.steps[0].value


def test_a_chamber_already_at_its_target_takes_no_time() -> None:
    """Preheated past its target by the stages before, a chamber's stage takes no time and no
    fuel; a firing whose every stage is so is refused."""
    m = _model()
    s = se.fire_stages(m, [_front(), se.Stage(0, fi.MaxFire(), 500.0, HOUR, _path(0))],
                       sample=1800.0)  # fmt: skip
    assert s.times[1] == 0.0
    assert s.fuel[1] == 0.0
    assert s.parts[1] is None
    with pytest.raises(fi.FiringError, match="every stage's chamber was at its target"):
        se.fire_stages(m, [se.Stage(0, fi.FixedInput(0.01), 200.0, HOUR)])


def test_what_the_stages_refuse() -> None:
    m = _model()
    with pytest.raises(fi.FiringError, match="no gas zone 6"):
        se.stage_model(m, 0, burns=5)
    with pytest.raises(fi.FiringError, match="no setting 5 to hold"):
        fi.fire(m, fi.Schedule("setting", ((0.0, 300.0), (60.0, 310.0)), setting=4), 60.0)
    pathless = replace(m, path=None)
    stages = [se.Stage(0, fi.FixedInput(0.01), RED, 600.0), se.Stage(1, fi.MaxFire(), RED, 600.0)]
    with pytest.raises(fi.FiringError, match="max fire needs the kiln's draft"):
        se.fire_stages(pathless, stages, sample=300.0)
