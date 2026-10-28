"""How results and their working are written for the plans."""

import pytest

from kilndesigner.units import Q_
from kilndesigner.working import Finding, Step, length_text, show


def test_text_is_shown_as_it_is() -> None:
    assert show("as given in the design") == "as given in the design"


def test_numbers_are_shown_to_four_figures_by_default() -> None:
    assert show(1234.567) == "1235"
    assert show(0.0123456) == "0.01235"
    assert show(1.04567, digits=3) == "1.05"
    assert show(48) == "48"


def test_quantities_are_shown_with_their_unit_converted_if_asked() -> None:
    """Cone 10 at 60 °C/h is 1285 °C, 2345 °F (electric-and-thermal.md §8)."""
    assert show(Q_(1285, "degC")) == "1285 °C"
    assert show(Q_(1285, "degC"), "degF") == "2345 °F"
    assert show(Q_(11_520, "W"), "kW") == "11.52 kW"
    assert show(Q_(17.5, "W/in**2"), "W/cm**2", 3) == "2.71 W/cm²"


@pytest.mark.parametrize(
    ("mm", "text"),
    [
        (228.6, "9 in"),  # a brick's length
        (114.3, "4½ in"),  # its width
        (342.9, "13½ in"),  # a brick and a half
        (171.45, "6¾ in"),
        (12.7, "½ in"),  # no whole inches
        (3.175, "⅛ in"),
        (10.0, "0.394 in"),  # not near an eighth
    ],
)
def test_us_lengths_are_written_in_eighths_where_they_fall_on_one(mm: float, text: str) -> None:
    assert length_text(mm, us=True) == text


def test_metric_lengths_are_whole_millimetres() -> None:
    assert length_text(342.9, us=False) == "343 mm"
    assert length_text(114.3, us=False) == "114 mm"


def test_steps_and_findings_carry_their_references() -> None:
    step = Step(name="Top temperature", value="1285 °C", reference="Orton")
    assert step.inputs == {}
    assert step.formula is None
    finding = Finding(level="warning", message="hot", reference="electric-and-thermal.md §1.6")
    assert finding.reference == "electric-and-thermal.md §1.6"
    with pytest.raises(ValueError, match="frozen"):
        step.name = "other"  # pyright: ignore[reportAttributeAccessIssue]
    with pytest.raises(ValueError, match="level"):
        Finding.model_validate({"level": "fatal", "message": "x"})
