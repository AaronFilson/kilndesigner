from pathlib import Path
from xml.etree import ElementTree

import pytest

from kilndesigner import load_design, parse_design
from kilndesigner.charts import Marker, Series, line_chart
from kilndesigner.heatloss import heat_loss
from kilndesigner.hybrid import analyse_hybrid, propane_cost_per_kwh
from kilndesigner.units import Q_

EXAMPLES = Path(__file__).parents[2] / "examples"
PNW = EXAMPLES / "pnw-hybrid-crossdraft.yaml"


@pytest.fixture(scope="module")
def analysis():  # type: ignore[no-untyped-def]
    return analyse_hybrid(load_design(PNW), 11_520)


def test_the_electric_ceiling_is_where_loss_meets_power(analysis) -> None:  # type: ignore[no-untyped-def]
    loss = heat_loss(load_design(PNW), inside=Q_(analysis.electric_ceiling_c, "degC")).total_watts
    assert loss == pytest.approx(11_520, rel=0.01)


def test_propane_costs_more_per_useful_kwh_as_the_kiln_heats(analysis) -> None:  # type: ignore[no-untyped-def]
    costs = [p.propane_per_kwh for p in analysis.points]
    assert costs == sorted(costs)
    # at $3.50/gal and 26.8 kWh/gal, propane can't beat $0.13/kWh even with no flue loss
    assert all(c > 3.50 / (91_502 / 3412.14) for c in costs)


def test_reducing_costs_more_than_oxidising(analysis) -> None:  # type: ignore[no-untyped-def]
    for p in analysis.points:
        if p.propane_reducing_per_kwh is not None:
            assert p.propane_reducing_per_kwh > p.propane_per_kwh


def test_switch_over_is_the_lowest_limit(analysis) -> None:  # type: ignore[no-untyped-def]
    # off_above 1650 °F (898.9 °C) is just below the 900 °C start of reduction
    assert analysis.switch_over_c == pytest.approx(898.9, abs=0.1)
    assert analysis.switch_over_reason == "as set in the design"
    assert analysis.switch_over_c < analysis.electric_ceiling_c


def test_cheap_propane_moves_the_crossover() -> None:
    text = PNW.read_text(encoding="utf-8").replace("3.50 USD/gallon", "1.20 USD/gallon")
    analysis = analyse_hybrid(parse_design(text), 11_520)
    assert analysis.cost_crossover is not None
    # cheap propane wins at low temperature, electricity at high: the switch doesn't move, but
    # the analysis says the early elements are there for control rather than cost
    assert analysis.switch_over_reason == "as set in the design"
    assert any("for control" in f.message for f in analysis.findings)


def test_propane_cost_per_kwh_units() -> None:
    # 26.82 kWh/gal of HHV; at 25 °C and λ 1 about 93% of it is available
    assert propane_cost_per_kwh(2.682, 298.15, 1.0) == pytest.approx(0.1 / 0.929, rel=0.01)


def test_line_chart_is_valid_svg() -> None:
    svg = line_chart(
        [Series("a", [(0, 0), (1, 2)]), Series("b", [(0, 1), (1, 1)], dashed=True)],
        x_label="x",
        y_label="y",
        markers=[Marker(0.5, "half")],
    )
    root = ElementTree.fromstring(svg)
    assert len(root.findall(".//{http://www.w3.org/2000/svg}polyline")) == 2
