import json
import math
from pathlib import Path
from typing import Any

import pytest

from kilndesigner.report import _unique_checks  # pyright: ignore[reportPrivateUsage]
from kilndesigner.sheet import (
    Check,
    ExpressionError,
    Sheet,
    SheetMismatchError,
    evaluate,
    excel,
    number,
    parse,
    requirement_text,
    shown,
)
from kilndesigner.units import Q_
from kilndesigner.working import Finding

CORPUS = Path(__file__).parent / "expressions.json"
corpus: dict[str, Any] = json.loads(CORPUS.read_text(encoding="utf-8"))


def _float(v: float | str) -> float:
    return float(v)  # "NaN", "Infinity" and "-Infinity" read as float() reads them


@pytest.mark.parametrize("case", corpus["expressions"], ids=lambda c: c["expr"])
def test_the_shared_expressions(case: dict[str, Any]) -> None:
    got = evaluate(parse(case["expr"]), case.get("env", {}))
    want = _float(case["value"])
    if math.isnan(want):
        assert math.isnan(got)
    else:
        assert got == pytest.approx(want, rel=1e-12)


@pytest.mark.parametrize("case", corpus["errors"], ids=lambda c: c["expr"])
def test_the_shared_errors(case: dict[str, Any]) -> None:
    with pytest.raises(ExpressionError):
        evaluate(parse(case["expr"]), case.get("env", {}))


@pytest.mark.parametrize("case", corpus["numbers"], ids=lambda c: str(c["x"]))
def test_the_shared_numbers(case: dict[str, Any]) -> None:
    assert number(_float(case["x"])) == case["text"]


@pytest.mark.parametrize(
    ("expr", "text"),
    [
        ("pi/4*d^2", "π/4·d²"),
        ("sqrt(a^2 + b^2)", "√(a² + b²)"),
        ("sqrt(x)", "√x"),
        ("P_c + k*ΔS/2", "P_c + k·ΔS/2"),
        ("a - (b - c)", "a − (b − c)"),
        ("a - b + c", "a − b + c"),
        ("a/(b*c)", "a/(b·c)"),
        ("(a + b)/c", "(a + b)/c"),
        ("-(a + b)", "−(a + b)"),
        ("-a^2", "−a²"),
        ("(-a)^2", "(−a)²"),
        ("x^(n + 1)", "x^(n + 1)"),
        ("x^n", "x^n"),
        ("x^0.5", "x^0.5"),
        ("abs(a - b)", "|a − b|"),
        ("min(a, b*2)", "min(a, b·2)"),
        ("a*(b*c)", "a·b·c"),
        ("a*(b/c)", "a·b/c"),
        ("a/(b/c)", "a/(b/c)"),
        ("a - (b + c)", "a − (b + c)"),
    ],
)
def test_a_formula_reads_as_a_builder_writes_it(expr: str, text: str) -> None:
    assert shown(parse(expr)) == text


def test_a_formula_goes_into_a_spreadsheet_fully_bracketed() -> None:
    ref = {"a": "C2", "b": "C3"}
    assert excel(parse("-a^2 + pi*b"), ref) == "((-(C2^2))+(PI()*C3))"
    assert excel(parse("atan2(a, b)"), ref) == "ATAN2(C3,C2)"
    assert excel(parse("ln(a) + log10(b) + sqrt(min(a, b))"), ref) == (
        "((LN(C2)+LOG10(C3))+SQRT(MIN(C2,C3)))"
    )


def rod(load_lbf: float) -> Sheet:
    s = Sheet("test.rod", "Tie rod stress, hot", reference="a test")
    s.given("P", "load on each rod, hot", Q_(load_lbf, "lbf"), source="working step")
    s.given("d", "rod root diameter", Q_(0.4001, "in"), source="ASME B1.1")
    s.let("A", "root area", "pi/4*d^2", "in**2")
    s.let("σ", "stress", "P/A", "psi")
    s.given("σ_allow", "allowable stress", Q_(12000, "psi"), source="AISC")
    s.require("σ", "<=", "σ_allow")
    s.lever("d", Q_(0.1, "in"), Q_(2, "in"))
    return s


def test_a_passing_check_says_how_far_the_lever_can_go() -> None:
    c = rod(224).check()
    assert c.status == "pass"
    assert c.cells[2].formula == "π/4·d²"
    assert c.cells[2].label == "in²"
    assert c.requirements[0].margin == "σ = 1,782 psi, 14.85 % of σ_allow = 12,000 psi"
    assert c.solve == "Passes while d ≥ 0.1542 in"  # σ = σ_allow at d = √(4P/(π σ_allow))


def test_a_failing_check_says_what_would_pass() -> None:
    s = rod(3000)
    c = s.check()
    assert c.status == "error"
    assert not c.requirements[0].holds
    assert c.solve == "Passes when d ≥ 0.5642 in"
    assert requirement_text(c.requirements[0]) == "σ ≤ σ_allow"
    f = Finding.failed(c, "The rods are overstressed.")
    assert (f.level, f.reference, f.check) == ("error", "a test", c)


def test_a_passing_check_raises_no_finding() -> None:
    with pytest.raises(ValueError, match="nothing to report"):
        Finding.failed(rod(224).check(), "nothing")


def test_temperatures_compare_by_difference_not_ratio() -> None:
    s = Sheet("test.face", "Hot face against the brick's rating")
    s.given("T_face", "hot face", Q_(2350, "degF"))
    s.given("T_max", "rating", Q_(2300, "degF"), source="ASTM C155")
    s.require("T_face", "<=", "T_max", level="warning")
    s.lever("T_face", Q_(1000, "degF"), Q_(3000, "degF"))
    c = s.check()
    assert c.status == "warning"
    assert c.requirements[0].margin == "T_face = 2,350 °F, 50 °F over T_max = 2,300 °F"
    assert c.solve == "Passes when T_face ≤ 2,300 °F"


def test_a_rule_that_isnt_a_formula() -> None:
    s = Sheet("test.ring", "What a dome's ring is made of")
    s.fact("ring", "ceramic fiber blanket", source="the design")
    s.rule("A dome's ring must be brick or castable.", holds=False)
    c = s.check()
    assert (c.status, c.solve, c.cells[0].text) == ("error", None, "ceramic fiber blanket")


def test_a_lever_with_no_change_in_its_range() -> None:
    s = rod(224)
    s.lever("d", Q_(0.3, "in"), Q_(2, "in"))
    assert s.check().solve == "Passes for any d from 0.3 in to 2 in"
    s = rod(3000)
    s.lever("d", Q_(0.1, "in"), Q_(0.5, "in"))
    assert s.check().solve == "Doesn't pass for any d from 0.1 in to 0.5 in"


def test_a_value_on_its_limit_passes_whichever_way_the_float_fell() -> None:
    s = Sheet("test.edge", "On the limit")
    s.given("a", "value", 0.1 + 0.2)  # 0.30000000000000004
    s.given("b", "limit", 0.3)
    assert s.require("a", "<=", "b")
    assert s.require("b", ">=", "a")
    assert not s.require("a", "<", "b")  # strict: no slack
    s.given("inf", "no limit", math.inf)
    assert not s.require("inf", "<=", "a")


def test_the_worst_failing_requirement_sets_the_level() -> None:
    s = Sheet("test.two", "Two limits")
    s.given("x", "value", 5.0)
    s.given("soft", "warning limit", 4.0)
    s.given("hard", "error limit", 6.0)
    s.require("x", "<", "soft", level="warning")
    assert s.require("x", ">", "hard", level="error") is False
    assert s.check().status == "error"


def test_units_that_dont_match_are_caught() -> None:
    s = Sheet("test.units", "Units")
    s.given("P", "force", Q_(1, "lbf"))
    s.given("d", "length", Q_(1, "in"))
    with pytest.raises(ExpressionError, match="comes out in"):
        s.let("σ", "stress", "P/d", "psi")
    with pytest.raises(ExpressionError, match="can't add"):
        s.let("x", "nonsense", "P + d", "lbf")
    with pytest.raises(ExpressionError, match="no unit"):
        s.let("y", "nonsense", "sin(d)")
    with pytest.raises(ExpressionError, match="no unit"):
        s.let("z", "nonsense", "d^d", "in")
    with pytest.raises(ExpressionError, match="different units"):
        s.let("w", "nonsense", "max(P, d)", "lbf")
    with pytest.raises(ExpressionError, match="different units"):
        s.require("P", "<=", "d")
    assert s.let("r", "a ratio", "atan2(d, d)") == pytest.approx(math.pi / 4)
    assert s.let("m", "abs and min", "abs(-d) + min(d, d)", "in") == pytest.approx(0.0508)
    assert s.let("n", "minus", "-(P - P)", "lbf") == 0


def test_a_sheet_reads_only_cells_above_and_names_them_once() -> None:
    s = Sheet("test.names", "Names")
    s.given("a", "one", 1.0)
    with pytest.raises(ExpressionError, match="not cells above"):
        s.let("b", "two", "a + c")
    for bad in ("a", "2a", "sqrt", "pi", ""):
        with pytest.raises(ExpressionError, match=r"a cell|already"):
            s.given(bad, "bad", 1.0)
    with pytest.raises(ExpressionError, match="not a cell"):
        s.require("a", "<", "zz")
    s.let("b", "two", "a*2")
    with pytest.raises(ExpressionError, match="must be an input"):
        s.lever("b", 0.0, 1.0)


def test_the_sheet_must_reproduce_the_engines_number() -> None:
    s = rod(224)
    s.agrees("σ", Q_(1781.7, "psi"), rel=1e-3)
    with pytest.raises(SheetMismatchError, match="the engine"):
        s.agrees("σ", 1.0)


def test_a_check_that_fires_twice_gets_two_ids() -> None:
    c = rod(3000).check()
    findings = [
        Finding.failed(c, "one"),
        Finding.failed(c, "two"),
        Finding(level="info", message="x"),
    ]
    ids = [(f.check.id, f.check.label) for f in _unique_checks(findings) if f.check]
    assert ids == [("test.rod", "E1"), ("test.rod-2", "E2")]


def coldest_air() -> Sheet:
    s = Sheet("test.cold", "Coldest air")
    s.given("t", "coldest air", Q_(-10, "degF"))
    s.given("t_min", "coldest the table covers", Q_(0, "degF"))
    s.require("t", ">=", "t_min")
    s.lever("t", Q_(-40, "degF"), Q_(100, "degF"))
    return s


def test_a_limit_of_zero_solves_to_zero_not_the_slack() -> None:
    assert coldest_air().check().solve == "Passes when t ≥ 0 °F"


def cylinders(p_max: float = 1_000_000, window: tuple[float, float] = (1, 40)) -> Sheet:
    s = Sheet("test.cylinders", "Cylinders against the burners")
    s.given("n", "cylinders", 4)
    s.given("c", "what one gives", Q_(167_000, "BTU/hr"))
    s.let("C", "what they give", "n*c", "BTU/hr")
    s.given("P", "what the burners need", Q_(723_333, "BTU/hr"))
    s.given("P_max", "the most the regulator passes", Q_(p_max, "BTU/hr"))
    s.require("C", ">=", "P")
    s.require("C", "<=", "P_max")
    s.lever("n", *window, step=1)
    return s


def test_a_count_solves_to_a_whole_number_that_passes() -> None:
    assert cylinders().check().solve == "Passes when n ≥ 5"  # 723,333 ÷ 167,000 = 4.331
    # Capped at 800,000: between 4.331 and 4.79 cylinders it would pass, but no whole number does
    no_whole = cylinders(800_000, (4, 4.6)).check().solve
    assert no_whole == "No whole n passes (it would at n ≥ 4.331)"


def budget() -> Sheet:
    s = Sheet("test.budget", "Budget")
    s.given("C", "the priced materials", Q_(12_561, "USD"))
    s.given("B", "the budget", Q_(5_000, "USD"))
    s.require("C", "<=", "B", level="warning")
    s.lever("B", Q_(0, "USD"), Q_(30_000, "USD"))
    return s


def test_money_is_written_with_its_sign_first() -> None:
    c = budget().check()
    assert c.requirements[0].margin == "C = $12,561, 251.2 % of B = $5,000"
    assert c.solve == "Passes when B ≥ $12,561"


def test_an_angle_shows_in_degrees() -> None:
    s = Sheet("test.angle", "Angle")
    s.given("θ", "an angle", Q_(30, "degree"))
    assert s.check().cells[0].label == "°"


def golden_checks() -> list[Check]:
    s = Sheet("test.face", "Hot face against the brick's rating")
    s.given("T_face", "hot face", Q_(2350, "degF"))
    s.given("T_max", "rating", Q_(2300, "degF"))
    s.require("T_face", "<=", "T_max", level="warning")
    s.lever("T_face", Q_(1000, "degF"), Q_(3000, "degF"))
    ring = Sheet("test.ring", "What a dome's ring is made of")
    ring.fact("ring", "ceramic fiber blanket")
    ring.rule("A dome's ring must be brick or castable.", holds=False)
    far = rod(224)
    far.lever("d", Q_(0.3, "in"), Q_(2, "in"))
    return [
        rod(224).check(),
        rod(3000).check(),
        s.check(),
        ring.check(),
        far.check(),
        coldest_air().check(),
        cylinders().check(),
        cylinders(800_000, (4, 4.6)).check(),
        budget().check(),
    ]


def test_the_shared_checks(update_golden: bool) -> None:
    """The page recomputes these checks' status, margins and solve text and must match."""
    made = [c.model_dump(mode="json") for c in golden_checks()]
    if update_golden:
        corpus["checks"] = made
        text = json.dumps(corpus, ensure_ascii=False, indent=2) + "\n"
        CORPUS.write_text(text, encoding="utf-8", newline="\n")
    assert corpus["checks"] == made
