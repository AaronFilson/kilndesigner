"""The reference kilns' dataset (``reference_kilns.yaml``): every Olsen design is in it, every
fact carries its source and status, and the conversions the v1 baseline uses are right."""

from typing import Any

import fuel
import pytest
import reference as ref

OLSEN = ref.ROOT / "examples" / "olsen"


@pytest.fixture(scope="module")
def data() -> dict[str, Any]:
    return ref.load()


def test_every_olsen_kiln_is_in_the_dataset(data: dict[str, Any]) -> None:
    assert set(data["kilns"]) == {p.stem for p in OLSEN.glob("*.yaml")}
    for kid, k in data["kilns"].items():
        assert k["design"] == f"examples/olsen/{kid}.yaml"
        assert k["doc"] == f"docs/kilns/olsen/{kid}.md"


def test_every_fact_has_its_source_and_status(data: dict[str, Any]) -> None:
    assert ref.problems(data) == []


def test_a_fact_without_its_source_is_caught() -> None:
    def kiln(*heat: dict[str, Any]) -> dict[str, Any]:
        return {
            "kilns": {
                "x": {
                    "name": "x",
                    "design": "examples/olsen/fast-fire.yaml",
                    "doc": "docs/kilns/olsen/fast-fire.md",
                    "fuel": "wood",
                    "draft": "down",
                    "heat": list(heat),
                }
            }
        }

    def found(*heat: dict[str, Any]) -> str:
        return "; ".join(ref.problems(kiln(*heat)))

    ok = {"what": "firing_time", "value": 3.5, "unit": "hour", "status": "printed", "page": "p.139"}
    assert found(ok) == ""
    assert "no page" in found(ok | {"page": None})
    assert "isn't 'p.N'" in found(ok | {"page": "page 139"})
    assert "needs its reason" in found(ok | {"status": "assumed", "page": None})
    assert "needs its spread" in found(ok | {"status": "scaled", "figure": "Fig 5-35"})
    assert "needs its figure" in found(ok | {"status": "drawing"})
    assert "needs its unit" in found(ok | {"unit": None})
    assert "Pint registry" in found(ok | {"unit": "fortnights of wood"})
    assert "vocabulary" in found(ok | {"what": "firing_speed"})
    assert "runs backwards" in found(ok | {"value": [4, 3]})
    assert "can't have a bound" in found(ok | {"value": [3, 4], "bound": "<"})
    log = {"what": "schedule", "value": [["5:00", 190]], "unit": "degC", "status": "printed"}
    assert found(log | {"page": "p.309"}) == ""
    assert "isn't ['H:MM'" in found(log | {"page": "p.309", "value": [["five", 190]]})
    assert "doesn't exist" in "; ".join(
        ref.problems({"kilns": {"y": kiln()["kilns"]["x"] | {"design": "nope.yaml"}}})
    )


def test_firings_pair_a_time_with_the_fuel_of_the_same_firing() -> None:
    k: dict[str, Any] = {
        "heat": [
            {"what": "firing_time", "value": 3.5, "unit": "hour", "status": "printed"},
            {"what": "fuel_per_firing", "value": 0.25, "unit": "cord", "status": "printed"},
            {
                "what": "firing_time",
                "value": 1.9,
                "unit": "hour",
                "status": "printed",
                "firing": "altitude",
            },
            {"what": "firing_time", "value": 9, "unit": "hour", "status": "assumed"},
        ]
    }
    by = {f.label: f for f in ref.firings(k)}
    assert set(by) == {"", "altitude"}
    assert [t["value"] for t in by[""].times] == [3.5]
    assert len(by[""].fuels) == 1
    assert by["altitude"].fuels == []


def test_burner_input_is_the_total_or_count_times_each_rating() -> None:
    def rating(btu: float, page: str) -> dict[str, Any]:
        return {"what": "burner_rating", "value": btu, "unit": "BTU/hr", "status": "printed",
                "page": page}  # fmt: skip

    six = {"what": "burner_count", "value": 6, "status": "printed", "page": "p.226"}
    assert ref.burner_inputs({"heat": [six, rating(36000, "p.226")]}) == [
        (216_000, "6 burners (p.226) × 36,000 BTU/hr (p.226)")
    ]
    two = ref.burner_inputs({"heat": [six, rating(75000, "p.222"), rating(54000, "p.220")]})
    assert [x for x, _ in two] == [450_000, 324_000]
    total = {"what": "burner_input", "value": 924000, "unit": "BTU/hr", "status": "printed",
             "page": "p.214"}  # fmt: skip
    got = ref.burner_inputs({"heat": [six, rating(36000, "p.226"), total]})
    assert [x for x, _ in got] == [pytest.approx(924_000)]
    assert ref.burner_inputs({"heat": [rating(36000, "p.226")]}) == []
    several = {"what": "firing_time", "value": "several days", "status": "printed", "page": "p.1"}
    assert ref.firings({"heat": [several]}) == []


def test_a_quarter_cord_as_heat() -> None:
    """0.25 cord × 2,070–4,200 lb oven-dry × (18.4 − 2.44·0.2/0.8) to (19.2 − 2.44·0.12/0.88)
    MJ per dry kg (FAO UBET eq. 3), by hand: 1,160.0 and 2,496.1 kWh."""
    h = fuel.wood_cords(0.25)
    assert h.low_kwh == pytest.approx(1159.98, rel=1e-4)
    assert h.high_kwh == pytest.approx(2496.10, rel=1e-4)
    pine = fuel.wood_cords(0.25, "pine (Pinus)")
    assert pine.low_kwh > h.low_kwh
    assert pine.high_kwh < h.high_kwh


def test_the_moisture_formula_meets_forest_researchs_logs() -> None:
    """Forest Research: log wood at 20 % moisture, 14.7 GJ/t (wood-fuel.md §2)."""
    assert fuel.net_mj_per_kg_as_fired(0.20, 19.0) == pytest.approx(14.71, abs=0.01)


def test_wood_by_weight_diesel_and_what_isnt_converted() -> None:
    w = fuel.wood_mass(1000.0)
    assert w.low_kwh == pytest.approx(14232 / 3.6, rel=1e-4)
    assert w.high_kwh == pytest.approx(16603.2 / 3.6, rel=1e-4)
    d = fuel.fuel_heat(60, "gallon", "oil")
    assert not isinstance(d, str)
    assert d.low_kwh == pytest.approx(60 * 132_000 / 3412.14, rel=1e-3)
    tons = fuel.fuel_heat(2, "ton", "wood")
    assert not isinstance(tons, str)
    assert tons.low_kwh == pytest.approx(fuel.wood_mass(2 * 907.18474).low_kwh)
    assert "coal" in str(fuel.fuel_heat(10, "shovel", "coal"))
    assert "no sourced weight" in str(fuel.fuel_heat(200, "bundle", "wood"))
    assert "no sourced conversion" in str(fuel.fuel_heat(1, "therm", "gas"))
