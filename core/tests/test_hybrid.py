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


PNW_TEXT = PNW.read_text(encoding="utf-8")


def test_a_hybrid_needs_elements_and_burners() -> None:
    with pytest.raises(ValueError, match="a hybrid needs both elements and burners"):
        analyse_hybrid(load_design(EXAMPLES / "gas-crossdraft.yaml"), 11_520)


def test_a_hybrid_needs_both_prices() -> None:
    kiln = parse_design(PNW_TEXT.replace("  electricity_price: 0.12 USD/kWh\n", ""))
    with pytest.raises(ValueError, match="give the site's electricity_price and propane_price"):
        analyse_hybrid(kiln, 11_520)


def test_elements_that_can_hold_the_top_temperature_have_no_ceiling_below_it() -> None:
    kiln = load_design(PNW)
    loss_at_top = heat_loss(kiln).total_watts
    analysis = analyse_hybrid(kiln, loss_at_top + 1000)
    assert analysis.electric_ceiling == (
        "the top temperature (2345 °F); the elements could fire it alone"
    )
    assert analysis.electric_ceiling_c == pytest.approx(1285)  # cone 10 at 60 °C/h
    assert analysis.switch_over_reason == "as set in the design"


def test_oxidation_firing_with_no_set_switch_hands_over_at_the_ceiling() -> None:
    """With no reduction and no off_above, the only limit is the electric ceiling. At $0.12/kWh
    and $3.50/gal electricity is the cheaper useful heat everywhere, and the analysis says so."""
    text = PNW_TEXT.replace("reduction: true", "reduction: false").replace(
        "    off_above: 1650 degF\n", ""
    )
    analysis = analyse_hybrid(parse_design(text), 11_520)
    assert analysis.switch_over == analysis.electric_ceiling
    assert analysis.switch_over_reason == "the elements can't raise the kiln any further above it"
    assert all(p.propane_reducing_per_kwh is None for p in analysis.points)
    assert all(p.propane_per_kwh > p.electric_per_kwh for p in analysis.points)
    assert analysis.cost_crossover is None
    cheaper = next(s for s in analysis.working if s.name == "Cheaper heat")
    assert cheaper.value == "electricity, at every temperature in the firing"
    switch = next(s for s in analysis.working if s.name == "Switch-over")
    assert switch.reference is None  # no reduction, so the reduction source doesn't apply
    advice = "electricity is the cheaper heat at every temperature"
    assert any(advice in f.message for f in analysis.findings)


def test_elements_left_on_into_reduction_are_a_warning() -> None:
    """Reduction from about 900 °C (1652 °F) [S66]; Kanthal allows A-1 and APM only 1050 °C
    (1922 °F) in CO- and H₂-rich gas [S9]. Elements set to stay on to 1900 °F hand over at the
    start of reduction instead, with a warning."""
    text = PNW_TEXT.replace("off_above: 1650 degF", "off_above: 1900 degF")
    analysis = analyse_hybrid(parse_design(text), 11_520)
    assert analysis.switch_over_c == pytest.approx(900)
    assert analysis.switch_over == "1652 °F"
    assert analysis.switch_over_reason == "reduction starts about here and attacks the elements"
    [warning] = [f for f in analysis.findings if f.level == "warning"]
    assert warning.message.startswith("The elements stay on to 1900 °F, past the start of")
    assert "Kanthal allows A-1 and APM only 1922 °F" in warning.message


def test_dear_electricity_makes_propane_the_cheaper_heat_throughout() -> None:
    """At $0.40/kWh, propane at $3.50/gal is cheaper per useful kWh even at the top: there is no
    crossover, and the hand-over stays where the design sets it."""
    text = PNW_TEXT.replace("0.12 USD/kWh", "0.40 USD/kWh")
    analysis = analyse_hybrid(parse_design(text), 11_520)
    assert analysis.cost_crossover is None
    assert all(p.electric_per_kwh == pytest.approx(0.40) for p in analysis.points)
    assert all(p.propane_per_kwh < 0.40 for p in analysis.points)
    assert analysis.switch_over_reason == "as set in the design"


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
