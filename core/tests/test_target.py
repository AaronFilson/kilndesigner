"""Elements and burners together, and the burners solved for a target firing time."""

from __future__ import annotations

from pathlib import Path

import pytest

from kilndesigner import Kiln, load_design
from kilndesigner.report import design_report
from kilndesigner.simulation import SimulationError, simulate
from kilndesigner.target import solve_target
from kilndesigner.units import Q_

EXAMPLES = Path(__file__).parents[2] / "examples"
DT = 120.0  # a coarser step keeps these quick; the method is the same


def _example(changes: dict[str, object] | None = None) -> Kiln:
    kiln = load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml")
    doc = kiln.model_dump(by_alias=True, mode="json")
    for path, value in (changes or {}).items():
        node = doc
        *parents, last = path.split(".")
        for key in parents:
            node = node[key]  # pyright: ignore
        node[last] = value  # pyright: ignore
    return Kiln.model_validate(doc)


@pytest.mark.slow
def test_burners_lit_at_the_hand_over_is_the_hand_over() -> None:
    kiln = _example()
    plain = simulate(kiln, dt=DT, record=False).result
    same = simulate(_example({"heat.gas.on_from": "1650 degF"}), dt=DT, record=False).result
    assert same.duration_h == plain.duration_h
    assert same.cost_usd == plain.cost_usd
    assert same.gas_from_c is None
    assert plain.heat.startswith("electric, then gas")


def test_both_together_fire_faster() -> None:
    plain = simulate(_example(), dt=DT, record=False).result
    both = simulate(_example(), gas_from_c=20.0, dt=DT, record=False).result
    assert both.completed
    assert both.duration_h < plain.duration_h / 3
    assert both.electricity_kwh > 0
    assert both.fuel_kwh > 0
    assert both.gas_from_c == pytest.approx(20.0)
    assert "with gas from" in both.heat
    assert any(s.name == "Burners lit, the elements still on" for s in both.working)
    assert not any("into reduction" in f.message for f in both.findings)
    # From the design: the same firing
    design = simulate(_example({"heat.gas.on_from": "68 degF"}), dt=DT, record=False).result
    assert design.duration_h == both.duration_h


def test_elements_on_into_reduction_are_flagged() -> None:
    r = simulate(_example(), switch_over_c=1100.0, gas_from_c=500.0, dt=DT, record=False).result
    assert any("into reduction" in f.message for f in r.findings)


def test_stalled_elements_light_the_burners_early() -> None:
    kiln = _example({"heat.electric.power": "1 kW"})
    r = simulate(kiln, switch_over_c=1000.0, gas_from_c=800.0, dt=DT, record=False).result
    assert r.completed
    assert r.gas_from_c is not None
    assert r.gas_from_c < 800.0
    assert any("stall" in f.message for f in r.findings)


def test_a_stall_before_the_burners_are_lit_lights_them_not_hands_over() -> None:
    """Run together, the burners are lit at the stall and the elements stay on: not a hand-over."""
    kiln = _example({"heat.electric.power": "1 kW"})
    both = simulate(kiln, switch_over_c=1000.0, gas_from_c=800.0, dt=DT, record=False).result
    [stall] = [f for f in both.findings if "stall" in f.message]
    assert "the burners are lit there and the elements stay on" in stall.message
    assert "take over" not in stall.message
    alone = simulate(kiln, switch_over_c=800.0, dt=DT, record=False).result
    [stall] = [f for f in alone.findings if "stall" in f.message]
    assert "short of the hand-over, so the burners take over there" in stall.message


@pytest.mark.slow
def test_a_6_hour_target() -> None:
    t = solve_target(_example(), 6.0, dt=DT)
    assert t.met
    assert not t.limits
    assert t.duration_h <= 6.0
    assert t.input_btu_hr > 452_000  # more than the rule of thumb's
    assert t.burners is not None
    assert t.burners.startswith("8 ×")
    assert t.cylinders_full is not None
    assert t.cylinders_quarter is not None
    assert t.cylinders_quarter > t.cylinders_full
    assert t.supply_meets
    assert 0 < t.elements_share < 0.5
    assert t.cost_usd is not None
    assert t.cost_usd > 0
    assert t.peak_rate_c_per_h > 316
    assert any("faster than any sourced schedule" in f.message for f in t.findings)
    assert any(s.name == "Burner input for the target" for s in t.working)
    assert any("into reduction" in f.message for f in t.findings)  # elements on to the top
    options = {o.option: o for o in t.supply_options}
    assert options["1000 gal tank"].works
    assert "% full" in options["1000 gal tank"].needs
    assert not options["120 gal tank"].works
    assert "11 cylinders, full" in " ".join(options)
    assert all(o.cost == t.cost for o in t.supply_options)
    # A 12 h firing needs less
    slow = solve_target(_example(), 12.0, dt=DT)
    assert slow.input_btu_hr < t.input_btu_hr


def test_a_slow_target_below_the_first_guess() -> None:
    t = solve_target(_example(), 20.0, dt=DT)
    assert t.met
    assert t.input_btu_hr < 452_000
    # The elements are on to the top: the top check counts them with the burners
    assert any(s.name == "Burners and elements against the heat lost at the top" for s in t.working)
    assert not any("sized to fire the kiln on their own" in f.message for f in t.findings)


def test_the_supply_limits_a_fast_target() -> None:
    t = solve_target(_example({"heat.gas.supply.count": 1}), 4.0, dt=DT)
    assert not t.met
    assert any("supply" in x for x in t.limits)
    assert t.duration_h > 4.0
    assert t.supply_meets is False
    assert any("can't be met" in f.message for f in t.findings)
    assert any("more than the" in f.message for f in t.findings)  # burns more than it holds


def test_the_burners_limit_a_fast_target() -> None:
    kiln = _example({"heat.gas.burners.count": 1, "heat.gas.burners.places": None})
    t = solve_target(kiln, 3.0, dt=DT)
    assert not t.met
    assert any("burners" in x for x in t.limits)


def test_a_target_faster_than_the_schedule_is_refused() -> None:
    with pytest.raises(SimulationError, match="the schedule alone"):
        solve_target(_example(), 1.0, dt=DT)
    with pytest.raises(SimulationError, match="more than zero"):
        solve_target(_example(), 0.0, dt=DT)
    with pytest.raises(SimulationError, match="target_time"):
        solve_target(_example(), dt=DT)
    with pytest.raises(SimulationError, match="has none"):
        solve_target(load_design(EXAMPLES / "electric-front-loader.yaml"), 6.0)


@pytest.mark.slow
def test_the_report_solves_the_design_target() -> None:
    report = design_report(_example({"firing.target_time": "8 hour"}))
    assert report.target is not None
    assert report.target.met
    electric = load_design(EXAMPLES / "electric-front-loader.yaml")
    electric = electric.model_copy(
        update={"firing": electric.firing.model_copy(update={"target_time": Q_(6, "hour")})}
    )
    report = design_report(electric)
    assert report.target is None
    assert any("target firing time isn't worked out" in f.message for f in report.findings)
