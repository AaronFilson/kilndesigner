"""Slow firings: the user's long firing time on the design's own heat, the sources beside it."""

from __future__ import annotations

from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.model import Ramp
from kilndesigner.simulation import LONGEST_FIRING_H, SimulationError, paced_hours, simulate
from kilndesigner.slow import SOURCED, slow_firing, slow_schedule
from kilndesigner.target import solve_target
from kilndesigner.units import Q_

ROOT = Path(__file__).parents[2]
ELECTRIC = ROOT / "examples" / "electric-front-loader.yaml"
GAS = ROOT / "examples" / "gas-crossdraft.yaml"


def test_paced_hours_counts_paced_ramps_and_holds() -> None:
    ramps = [
        Ramp(to=Q_(600, "degC")),  # full heat: nothing
        Ramp(to=Q_(1200, "degC"), rate=Q_(100, "delta_degC/hour"), hold=Q_(2, "hour")),
        Ramp(to=Q_(1000, "degC"), rate=Q_(50, "delta_degC/hour")),
    ]
    assert paced_hours(ramps, 293.15) == pytest.approx(6 + 2 + 4)


def test_a_schedule_longer_than_any_sourced_firing_is_refused() -> None:
    kiln = load_design(ELECTRIC)
    days = [Ramp(to=Q_(1200, "degC"), rate=Q_(4, "delta_degC/hour"))]  # about 295 h
    with pytest.raises(SimulationError, match="Bizen"):
        simulate(kiln, schedule=days, record=False)
    with pytest.raises(SimulationError, match="longer than any sourced firing"):
        slow_firing(kiln, LONGEST_FIRING_H + 1)
    with pytest.raises(SimulationError, match="longer than any sourced firing"):
        solve_target(load_design(GAS), LONGEST_FIRING_H + 1)


@pytest.mark.parametrize(
    ("hours", "soak", "why"),
    [(0, 0, "more than zero"), (10, 10, "the soak"), (10, -1, "the soak")],
)
def test_a_firing_time_or_soak_that_makes_no_sense_is_refused(
    hours: float, soak: float, why: str
) -> None:
    with pytest.raises(SimulationError, match=why):
        slow_firing(load_design(ELECTRIC), hours, soak)


def test_the_schedule_is_a_constant_rise_then_the_soak() -> None:
    kiln = load_design(ELECTRIC)
    [ramp], top, rate = slow_schedule(kiln, 50, 10)
    room = kiln.site.ambient.to("degC").magnitude
    assert rate == pytest.approx((top - room) / 40)
    assert ramp.hold is not None
    assert ramp.hold.to("hour").magnitude == pytest.approx(10)
    [plain], _, _ = slow_schedule(kiln, 50)
    assert plain.hold is None


def test_a_wood_kiln_gets_the_sources_only() -> None:
    kiln = load_design(ROOT / "core/src/kilndesigner/data/templates/anagama.yaml")
    s = slow_firing(kiln, 120)
    assert s.firing is None
    assert s.sources == list(SOURCED)
    assert "aren't simulated" in s.findings[0].message
    assert any("Bizen" in x.kiln and "p.99" in x.reference for x in s.sources)


@pytest.mark.slow
def test_a_slow_electric_firing_reports_where_the_heat_goes() -> None:
    s = slow_firing(load_design(ELECTRIC), 48, 6)
    assert s.firing is not None
    assert s.quickest is not None
    assert s.firing.completed
    assert s.firing.duration_h == pytest.approx(48, abs=0.1)
    # The shell's loss grows with the time: the slow firing loses far more than the quick one
    assert s.firing.shell_kwh > 5 * s.quickest.shell_kwh
    assert s.shell_share is not None
    assert s.walls_share is not None
    assert s.ware_share is not None
    assert s.shell_share + s.walls_share + s.ware_share > 1  # the walls' heat includes the shell's
    assert not [f for f in s.findings if f.level == "warning"]
    assert any("p.99" in (x.reference or "") for x in s.findings)
    names = [w.name for w in s.working]
    assert "Where the heat goes" in names


@pytest.mark.slow
def test_a_kiln_that_cant_reach_the_top_is_warned(monkeypatch: pytest.MonkeyPatch) -> None:
    kiln = load_design(ELECTRIC)
    real = simulate

    def short_of_top(*args: object, **kw: object):
        run = real(*args, **kw)  # pyright: ignore[reportArgumentType]
        if kw.get("schedule") is not None:
            run.result = run.result.model_copy(update={"completed": False, "reached_c": 900.0})
        return run

    monkeypatch.setattr("kilndesigner.slow.simulate", short_of_top)
    s = slow_firing(kiln, 12)
    [warning] = [f for f in s.findings if f.level == "warning"]
    assert "doesn't reach the top" in warning.message

    def behind(*args: object, **kw: object):
        run = real(*args, **kw)  # pyright: ignore[reportArgumentType]
        if kw.get("schedule") is not None:
            run.result = run.result.model_copy(update={"held": False})
        return run

    monkeypatch.setattr("kilndesigner.slow.simulate", behind)
    s = slow_firing(kiln, 12)
    assert any("can't keep this pace" in f.message for f in s.findings)
