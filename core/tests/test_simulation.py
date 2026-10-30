"""The firing simulation: whole kilns, schedules, refusals, costs and the Parquet files."""

from __future__ import annotations

from pathlib import Path

import pytest

from kilndesigner import Kiln, load_design
from kilndesigner.library import materials
from kilndesigner.model import Ramp
from kilndesigner.results import heatmap, read_summary, series, write_run
from kilndesigner.simulation import (
    SimulationError,
    default_schedule,
    simulate,
    switch_over_chart,
)
from kilndesigner.units import Q_

EXAMPLES = Path(__file__).parents[2] / "examples"
# A test input only, not engineering data: the castable roof needs some c_p to run the hybrid
TEST_CP = "1 kJ/(kg*K)"


def _example(name: str, **changes: object) -> Kiln:
    kiln = load_design(EXAMPLES / f"{name}.yaml")
    doc = kiln.model_dump(by_alias=True, mode="json")
    for path, value in changes.items():
        node = doc
        *parents, last = path.split(".")
        for key in parents:
            node = node[int(key)] if isinstance(node, list) else node[key]  # pyright: ignore
        node[last] = value  # pyright: ignore
    return Kiln.model_validate(doc)


def _hybrid(**changes: object) -> Kiln:
    return _example("pnw-hybrid-crossdraft", **{"lining.roof.0.specific_heat": TEST_CP, **changes})


@pytest.fixture(scope="module")
def electric() -> Kiln:
    return load_design(EXAMPLES / "electric-front-loader.yaml")


def test_an_electric_cone_10_firing(electric: Kiln) -> None:
    r = simulate(electric).result
    assert r.completed
    assert r.held
    assert r.reached_c == pytest.approx(1285, abs=0.5)  # cone 10 at 60 °C/h
    # Heat in = into the walls + into the ware, to the step's round-off
    assert r.energy_kwh == pytest.approx(r.walls_kwh + r.ware_kwh, rel=1e-9)
    assert r.electricity_kwh == pytest.approx(r.energy_kwh)
    assert r.cost_usd == pytest.approx(r.electricity_kwh * 0.12)
    assert r.fuel_kwh == 0
    assert r.propane_gallons is None
    # The heat goes mostly into the walls' storage; the shell loses a little through a firing
    assert 0 < r.shell_kwh < r.walls_kwh
    # Full heat to 1185 °C, then 60 °C/h: the last 100 °C take 1 h 40 min
    last = [p for p in r.points if p.setpoint_c > 1185.5]
    assert last[-1].time_h - last[0].time_h == pytest.approx(100 / 60, abs=0.05)
    assert 3 < r.duration_h < 12
    names = [s.name for s in r.working]
    assert "Firing schedule" in names
    assert "Cost of the firing" in names
    assert any("empty kiln" in f.message for f in r.findings)
    assert [f.face for f in r.faces] == ["left", "right", "back", "front", "floor", "roof"]


def test_ware_takes_heat_and_time(electric: Kiln) -> None:
    empty = simulate(electric, record=False).result
    loaded = simulate(_example("electric-front-loader", **{"firing.ware": "100 lb"})).result
    assert loaded.ware_kwh == pytest.approx(45.36 * 800 * (1285 - 21.1) / 3.6e6, rel=0.01)
    assert loaded.duration_h > empty.duration_h
    assert any(s.name == "Ware and furniture" for s in loaded.working)


def test_a_schedule_too_fast_for_the_elements_is_not_held(electric: Kiln) -> None:
    fast = [Ramp(to=Q_(1000, "degC"), rate=Q_(1000, "delta_degC/hour"))]
    r = simulate(electric, schedule=fast).result
    assert r.completed
    assert not r.held
    assert any("can't keep the schedule" in f.message for f in r.findings)


def test_holds_and_cooling(electric: Kiln) -> None:
    schedule = [
        Ramp(to=Q_(600, "degC"), rate=Q_(300, "delta_degC/hour"), hold=Q_(30, "minute")),
        Ramp(to=Q_(400, "degC"), rate=Q_(1000, "delta_degC/hour")),
        Ramp(to=Q_(450, "degC")),
    ]
    r = simulate(electric, schedule=schedule).result
    assert r.completed
    at_600 = [p for p in r.points if abs(p.chamber_c - 600) < 0.01]
    assert at_600[-1].time_h - at_600[0].time_h == pytest.approx(0.5, abs=0.05)
    # Cooling faster than the kiln cools itself: the power goes off and the kiln lags
    cooling = [p for p in r.points if p.setpoint_c < 599 and p.time_h < r.duration_h - 0.2]
    assert any(p.heat_kw == 0 and p.chamber_c > p.setpoint_c for p in cooling)
    assert r.reached_c == pytest.approx(600, abs=0.01)


def test_a_design_schedule_is_used() -> None:
    kiln = _example(
        "electric-front-loader",
        **{"firing.schedule": [{"to": "500 degC", "rate": "200 delta_degC/hour"}]},
    )
    r = simulate(kiln, record=False).result
    assert r.working[0].value == "1 segments, as given in the design"
    assert r.duration_h == pytest.approx(480 / 200, abs=0.05)


@pytest.mark.parametrize(
    ("ramp", "message"),
    [
        ({"to": "500 degC", "rate": "0 delta_degC/hour"}, "more than zero"),
        ({"to": "500 degC", "hold": "-1 hour"}, "negative"),
        ({"to": "500 degC", "rate": "5 hour"}, "heating rate"),
    ],
)
def test_ramps_are_checked(ramp: dict[str, str], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        Ramp.model_validate(ramp)


def test_a_rate_in_degrees_per_hour_reads_as_a_difference() -> None:
    r = Ramp.model_validate({"to": "1000 degF", "rate": "108 delta_degF/hour"})
    assert r.rate is not None
    assert r.rate.to("K/hour").magnitude == pytest.approx(60)


def test_the_default_schedule(electric: Kiln) -> None:
    ramps, step = default_schedule(electric)
    assert ramps[0].rate is None
    assert ramps[1].rate == Q_(60, "delta_degC/hour")
    assert "60 °C/h" in step.value
    assert step.reference


def test_a_kiln_that_stalls() -> None:
    weak = _example("electric-front-loader", **{"heat.electric.power": "2 kW"})
    r = simulate(weak, dt=300, record=False).result
    assert not r.completed
    assert r.reached_c < 1285
    assert any("stalls" in f.message for f in r.findings)


def test_a_firing_that_runs_too_long(electric: Kiln, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("kilndesigner.simulation.MAX_HOURS", 0.5)
    r = simulate(electric, record=False).result
    assert not r.completed
    assert any("stopped at 0.5 hours" in f.message for f in r.findings)


def test_a_castable_without_a_sourced_specific_heat_is_refused() -> None:
    kiln = load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml")
    with pytest.raises(SimulationError, match="Kast-O-Lite 30 LI Plus"):
        simulate(kiln)


def test_wood_firing_waits_for_m7() -> None:
    kiln = load_design(
        EXAMPLES
        / "olsen"
        / next(
            iter(
                sorted(
                    p.name
                    for p in (EXAMPLES / "olsen").glob("*.yaml")
                    if "fire:" in p.read_text(encoding="utf-8")
                )
            )
        )
    )
    with pytest.raises(SimulationError, match="M7"):
        simulate(kiln)


def test_the_hybrid_hands_over_and_costs_both_fuels() -> None:
    r = simulate(_hybrid(), dt=300, record=False).result
    assert r.completed
    assert r.switch_over_c == pytest.approx((1650 - 32) / 1.8)
    assert r.electricity_kwh > 0
    assert r.fuel_kwh > 0
    assert r.propane_gallons == pytest.approx(r.fuel_kwh * 3412.14 / 91502)
    assert r.propane_gallons is not None
    assert r.cost_usd == pytest.approx(r.electricity_kwh * 0.12 + r.propane_gallons * 3.50)
    # Burning fuel only counts the available heat: more is burned than is kept
    gas_points = [p for p in r.points if p.fuel_kw > 0]
    assert all(p.fuel_kw > p.heat_kw for p in gas_points)
    assert "then gas" in r.heat
    assert any("as given in the design" in f.message for f in r.findings)


def test_a_hybrid_hands_over_where_its_elements_stall() -> None:
    r = simulate(_hybrid(), switch_over_c=1250, dt=300, record=False).result
    assert r.completed
    assert r.switch_over_c is not None
    assert r.switch_over_c < 1250
    assert any("burners take over" in f.message for f in r.findings)


def test_a_hybrid_without_off_above_hands_over_at_reduction() -> None:
    kiln = _hybrid(**{"heat.electric.off_above": None})
    r = simulate(kiln, dt=600, record=False).result
    assert r.switch_over_c == pytest.approx(900)


def test_gas_without_prices_has_no_cost() -> None:
    kiln = _example(
        "gas-crossdraft",
        **{"lining.roof.0.specific_heat": TEST_CP, "site.propane_price": None},
    )
    r = simulate(kiln, dt=600, record=False).result
    assert r.cost is None
    assert r.cost_usd is None
    assert r.heat == "gas"
    assert any("propane_price" in f.message for f in r.findings)


def test_natural_gas_has_no_price() -> None:
    kiln = _example(
        "gas-crossdraft",
        **{
            "lining.roof.0.specific_heat": TEST_CP,
            "heat.gas.fuel": "natural_gas",
            "heat.gas.supply": {"type": "line", "pressure": "7 inch_H2O"},
            "heat.gas.burners": {
                "type": "venturi",
                "wall": "front",
                "count": 2,
                "rating": "100000 BTU/hr",
            },
        },
    )
    r = simulate(kiln, dt=600, record=False).result
    assert r.propane_gallons is None
    assert any("natural gas has no price" in f.message for f in r.findings)


def test_the_switch_over_chart() -> None:
    chart = switch_over_chart(_hybrid(), step_f=700, dt=600)
    assert [p.switch_over_f for p in chart.points] == [400, 1100, 1800]
    # Later hand-overs run the elements longer: more electricity, less propane
    kwh = [p.electricity_kwh for p in chart.points]
    gal = [p.propane_gallons for p in chart.points]
    assert kwh == sorted(kwh)
    assert gal == sorted(gal, reverse=True)
    assert chart.fastest_c == pytest.approx((400 - 32) / 1.8)
    assert chart.cheapest_c in [p.switch_over_c for p in chart.points]
    assert any("reduction" in f.message for f in chart.findings)


def test_the_switch_over_chart_marks_stalls(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("kilndesigner.simulation.MAX_HOURS", 20.0)
    chart = switch_over_chart(_hybrid(), step_f=1700, dt=600)
    assert [p.completed for p in chart.points] == [True, False]
    assert any("never finish" in f.message for f in chart.findings)


@pytest.mark.parametrize(
    ("kiln", "message"),
    [
        ("electric-front-loader", "elements and burners"),
        ("natural", "propane only"),
        ("noprice", "electricity_price"),
    ],
)
def test_the_switch_over_chart_refuses(kiln: str, message: str) -> None:
    k = (
        _hybrid(
            **{
                "heat.gas.fuel": "natural_gas",
                "heat.gas.supply": {"type": "line", "pressure": "7 inch_H2O"},
            }
        )
        if kiln == "natural"
        else _hybrid(**{"site.propane_price": None})
        if kiln == "noprice"
        else load_design(EXAMPLES / f"{kiln}.yaml")
    )
    with pytest.raises(SimulationError, match=message):
        switch_over_chart(k)


def test_ground_floor_and_given_specific_heat() -> None:
    kiln = _example(
        "electric-front-loader",
        **{
            "chamber.on_ground": True,
            "lining.walls.0.specific_heat": "1.2 kJ/(kg*K)",
            "site.electricity_price": None,
        },
    )
    r = simulate(kiln, dt=600, record=False).result
    assert r.completed
    assert r.cost is None
    assert any("as given in the design" in f.message for f in r.findings)


def test_every_library_material_with_a_specific_heat_cites_it() -> None:
    with_cp = [m for m in materials().values() if m.specific_heat is not None]
    assert len(with_cp) >= 10
    for m in with_cp:
        assert m.specific_heat is not None
        assert ".md" in m.specific_heat.source
    # None for the castables: no source gives one (thermal-properties.md §1, Not found)
    assert materials()["kast-o-lite-30-li-plus"].specific_heat is None


def test_results_round_trip_through_parquet(electric: Kiln, tmp_path: Path) -> None:
    run = simulate(electric)
    written = write_run(run, tmp_path, run_id="front-loader")
    assert {p.name for p in written} == {"firing.json", "series.parquet", "walls.parquet"}
    assert read_summary(tmp_path) == run.result
    points = series(tmp_path, max_points=50)
    assert len(points) <= 51
    assert points[0] == run.result.points[0]
    assert points[-1] == run.result.points[-1]
    full = series(tmp_path, max_points=100_000)
    assert full == run.result.points
    hm = heatmap(tmp_path, max_times=20)
    assert hm.walls == [f.face for f in run.result.faces]
    assert len(hm.times_h) <= 21
    assert hm.times_h[-1] == run.times_h[-1]
    assert len(hm.temperatures[0]) == 6
    assert len(hm.temperatures[-1][0]) == len(run.result.faces[0].depths_m)
    # The hot face leads the cold one at the end of the firing
    assert hm.temperatures[-1][0][0] > hm.temperatures[-1][0][-1]
    assert hm.min_c == pytest.approx(21.1, abs=0.1)
    assert hm.max_c > 1200
    assert hm.layers[0][0] == "ifb-jm26"
