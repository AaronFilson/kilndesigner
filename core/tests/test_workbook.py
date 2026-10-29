"""The workbook's live formulas, evaluated by an independent spreadsheet engine (the ``formulas``
package), give the sheet's values, and keep giving them when an input is changed."""

import warnings
from pathlib import Path
from typing import Any

import pytest

from kilndesigner.sheet import Check, Sheet, values
from kilndesigner.units import Q_
from kilndesigner.workbook import checks_workbook

with warnings.catch_warnings():
    warnings.simplefilter("ignore", SyntaxWarning)  # the formulas package's own `is 1.0`
    import formulas  # pyright: ignore[reportMissingTypeStubs]


def rod(load_lbf: float) -> Check:
    s = Sheet("test.rod", "Tie rod stress, hot")
    s.given("P", "load on each rod, hot", Q_(load_lbf, "lbf"))
    s.given("d", "rod root diameter", Q_(0.4001, "in"))
    s.let("A", "root area", "pi/4*d^2", "in**2")
    s.let("σ", "stress", "P/A", "psi")
    s.given("σ_allow", "allowable stress", Q_(12000, "psi"))
    s.require("σ", "<=", "σ_allow")
    s.lever("d", Q_(0.1, "in"), Q_(2, "in"))
    return s.check().model_copy(update={"label": "E1"})


def face() -> Check:
    s = Sheet("test.face", "Hot face against the rating")
    s.given("T_face", "hot face", Q_(2350, "degF"))
    s.given("T_max", "rating", Q_(2300, "degF"))
    s.let("ΔT", "over the rating", "T_face - T_max", "delta_degF")
    s.let("x", "powers and functions", "sqrt(abs(ΔT/T_max))^3 + max(ΔT, -ΔT)/ΔT + atan2(1, 1)")
    s.require("T_face", "<=", "T_max", level="warning")
    s.fact("brick", "K-23")
    s.rule("The brick must be rated for the hot face.", holds=False, level="warning")
    return s.check().model_copy(update={"label": "W1"})


class Book:
    """A workbook, calculated from its formulas, read by worksheet and cell."""

    def __init__(self, path: Path) -> None:
        self.model: Any = formulas.ExcelModel().loads(str(path)).finish()
        self.solution: dict[str, Any] = self.model.calculate()

    def key(self, sheet: str, cell: str) -> str:
        want = f"]{sheet.upper()}'!{cell}"
        return next(k for k in self.solution if k.endswith(want))

    def __call__(self, sheet: str, cell: str) -> Any:
        return self.solution[self.key(sheet, cell)].value[0][0]

    def change(self, sheet: str, cell: str, value: float) -> None:
        self.solution = self.model.calculate(inputs={self.key(sheet, cell): value})


ROD, FACE = "E1 Tie rod stress, hot", "W1 Hot face against the rating"


@pytest.fixture
def book(tmp_path: Path) -> Book:
    path = tmp_path / "checks.xlsx"
    path.write_bytes(checks_workbook([rod(3000), face()]))
    return Book(path)


def test_the_formulas_reproduce_the_sheet(book: Book) -> None:
    for i, c in enumerate(rod(3000).cells):
        assert c.value is not None
        assert book(ROD, f"G{6 + i}") == pytest.approx(c.value, rel=1e-9)
        assert book(ROD, f"C{6 + i}") == pytest.approx(c.value * c.scale + c.offset, rel=1e-9)
    assert not book(ROD, "B13")  # σ ≤ σ_allow fails
    assert book(ROD, "C13") == pytest.approx(1.98844, rel=1e-5)
    assert book(ROD, "B15") == "error"
    assert book("Checks", "C2") == "error"


def test_an_edited_input_recomputes_like_the_page(book: Book) -> None:
    book.change(ROD, "C7", 0.6)  # d, in inches: past the 0.5642 in the solve gave
    want = values(rod(3000).cells, {"d": 0.6 * 0.0254})
    assert book(ROD, "G9") == pytest.approx(want["σ"], rel=1e-9)
    assert book(ROD, "B15") == "pass"


def test_temperatures_and_rules(book: Book) -> None:
    by = {c.symbol: c for c in face().cells}
    assert book(FACE, "C8") == pytest.approx(50, rel=1e-9)  # ΔT in °F
    assert book(FACE, "G9") == pytest.approx(by["x"].value, rel=1e-9)
    assert book(FACE, "C10") == "K-23"
    assert book(FACE, "B16") == "warning"  # the rule fails at warning level
    book.change(FACE, "C6", 2200)  # T_face under the rating: the rule still fails
    assert book(FACE, "B16") == "warning"
