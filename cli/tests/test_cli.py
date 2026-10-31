import importlib
import io
import json
import sys
from pathlib import Path

import pytest
from typer.testing import CliRunner

import kilndesigner_cli.main
from kilndesigner import Kiln, load_design
from kilndesigner.build import BuildResult, build_design
from kilndesigner.report import design_report
from kilndesigner_cli.main import COMPARED, app, comparison_rows, summary

EXAMPLES = Path(__file__).parents[2] / "examples"
ELECTRIC = EXAMPLES / "electric-front-loader.yaml"
GAS = EXAMPLES / "gas-crossdraft.yaml"
runner = CliRunner()


def _design(tmp_path: Path, old: str, new: str) -> Path:
    """The electric example with one thing changed, written to a file."""
    text = ELECTRIC.read_text(encoding="utf-8")
    assert old in text
    path = tmp_path / "changed.yaml"
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return path


def _starts(header: str) -> list[int]:
    """Where each column of ``compare``'s table starts: where its design's name does."""
    starts: list[int] = []
    for name in header.split():
        starts.append(header.index(name, starts[-1] + 1 if starts else 0))
    return starts


def _table(output: str) -> dict[str, list[str]]:
    """The cells of each row of ``compare``'s table, by the row's label."""
    header, *lines = output.splitlines()
    starts = _starts(header)
    bounds = list(zip(starts, [*starts[1:], None], strict=True))
    return {line[: starts[0]].strip(): [line[a:b].strip() for a, b in bounds] for line in lines}


def test_check_accepts_a_valid_design() -> None:
    result = runner.invoke(app, ["check", str(ELECTRIC)])
    assert result.exit_code == 0, result.output
    assert "is valid" in result.output


def test_check_rejects_an_invalid_design(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("name: x\n", encoding="utf-8")
    result = runner.invoke(app, ["check", str(bad)])
    assert result.exit_code == 2


def test_build_writes_the_report_without_a_model(tmp_path: Path) -> None:
    result = runner.invoke(app, ["build", str(ELECTRIC), "--out", str(tmp_path), "--no-model"])
    assert result.exit_code == 0, result.output
    assert "Heat loss at top" in result.output
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    elements = report["electric"]["elements"]
    assert elements["count"] >= 1
    assert elements["groove_rows"] >= 3  # each element may run through several grooves


def test_compare_shows_each_design() -> None:
    door = str(EXAMPLES / "pnw-hybrid-crossdraft.yaml")
    budget = str(EXAMPLES / "pnw-hybrid-crossdraft-budget.yaml")
    castable = str(EXAMPLES / "pnw-hybrid-crossdraft-castable.yaml")
    result = runner.invoke(app, ["compare", door, budget, castable])
    assert result.exit_code == 0, result.output
    assert "pnw-hybrid-crossdraft-budget" in result.output
    assert "pnw-hybrid-crossdraft-castable" in result.output
    assert "Burner input" in result.output
    assert "Materials (priced)" in result.output


def test_compare_keeps_long_cells_apart_and_its_rows_in_one_order() -> None:
    """Columns were as wide as the longest design name, so "$2,750 + unpriced items" ran into the
    next column; and the rows came in the order of the first design given (the review's bugs)."""
    one = runner.invoke(app, ["compare", str(ELECTRIC), str(GAS)])
    other = runner.invoke(app, ["compare", str(GAS), str(ELECTRIC)])
    assert one.exit_code == other.exit_code == 0
    for result in (one, other):
        header, *lines = result.stdout.splitlines()
        for line in lines:
            # Every cell ends at least two spaces before the next column starts
            assert all(line[s - 2 : s] == "  " for s in _starts(header)[1:]), line
    labels = [list(_table(r.stdout)) for r in (one, other)]
    assert labels[0] == labels[1]
    assert labels[0] == [label for label in COMPARED if label in labels[0]]
    table = _table(one.stdout)
    assert table["Materials (priced)"][0].endswith("+ unpriced items")
    assert table["Materials (priced)"][1].startswith("$")


def test_a_castable_that_cant_be_worked_out_is_refused_without_a_traceback(tmp_path: Path) -> None:
    """A CastableError reached the user as a traceback (the review's materials 14)."""
    text = (EXAMPLES / "diy-castable-test-kiln.yaml").read_text(encoding="utf-8")
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        text.replace("ingredient: kyanite", "ingredient: unobtainium", 1), encoding="utf-8"
    )
    for command in (
        ["compare", str(ELECTRIC), str(bad)],
        ["build", str(bad), "--no-model", "--no-plans", "--out", str(tmp_path / "out")],
    ):
        result = runner.invoke(app, command)
        assert result.exit_code == 2, result.output
        assert "no ingredient 'unobtainium'; the library has:" in result.stderr
        assert result.exception is None or isinstance(result.exception, SystemExit)


def test_schema_is_json() -> None:
    result = runner.invoke(app, ["schema"])
    assert result.exit_code == 0
    assert json.loads(result.output)["title"] == "Kiln"


def test_compare_shows_a_dash_where_a_design_has_no_such_number() -> None:
    result = runner.invoke(app, ["compare", str(ELECTRIC), str(GAS)])
    assert result.exit_code == 0, result.output
    assert result.stdout.splitlines()[0].split() == ["electric-front-loader", "gas-crossdraft"]
    table = _table(result.stdout)
    electric_power, gas_power = table["Installed power"]
    assert electric_power.endswith(" kW")
    assert gas_power == "—"
    electric_burners, gas_burners = table["Burner input"]
    assert electric_burners == "—"
    assert gas_burners.endswith(" BTU/hr")
    assert table["Propane supply keeps up"][0] == "—"
    assert "Switch to burners at" not in table  # neither is a hybrid
    assert set(table) >= {"Chamber volume", "Heat loss at top", "Errors / warnings"}


def test_compare_refuses_a_design_naming_a_material_the_library_lacks(tmp_path: Path) -> None:
    bad = _design(tmp_path, "material: ifb-k23", "material: unobtainium")
    result = runner.invoke(app, ["compare", str(ELECTRIC), str(bad)])
    assert result.exit_code == 2
    assert result.stderr.startswith(f"{bad}: no material 'unobtainium'; the library has: ")
    assert result.stdout == ""  # no half-made table


def test_build_refuses_a_design_naming_an_alloy_the_library_lacks(tmp_path: Path) -> None:
    bad = _design(tmp_path, "alloy: kanthal-a1", "alloy: unobtainium")
    out = tmp_path / "out"
    result = runner.invoke(app, ["build", str(bad), "--out", str(out), "--no-model", "--no-plans"])
    assert result.exit_code == 2
    assert result.stderr.startswith(f"{bad}: no alloy 'unobtainium'; the library has: ")
    assert not out.exists()


def test_build_of_a_gas_kiln_shows_no_electric_lines(tmp_path: Path) -> None:
    result = runner.invoke(
        app, ["build", str(GAS), "--out", str(tmp_path), "--no-model", "--no-plans"]
    )
    assert result.exit_code == 0, result.output
    lines = result.stdout.splitlines()
    assert lines[0] == "Gas cross-draft, cone 10"
    assert lines[3].startswith("  Heat loss at top: ")
    assert lines[4].startswith("  Materials:        $")  # straight on from the heat loss
    assert "Installed power" not in result.stdout
    # No model, plans or drawings; the workbook of the warnings' sheets
    assert lines[-1] == f"Wrote {tmp_path / 'report.json'}, {tmp_path / 'checks.xlsx'}"
    assert json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))["electric"] is None


def test_build_exits_1_when_the_design_has_errors(tmp_path: Path) -> None:
    # One element can't carry the circuit's power in any standard wire: no elements are chosen.
    walls = "    walls: [left, right, back]\n"
    design = _design(tmp_path, walls, walls + "    elements: 1\n")
    out = tmp_path / "out"
    result = runner.invoke(
        app, ["build", str(design), "--out", str(out), "--no-model", "--no-plans"]
    )
    assert result.exit_code == 1
    assert "  Installed power:  " in result.stdout
    assert "Elements:" not in result.stdout
    assert "  [E1 error] No standard wire gauge gives elements that fit" in result.stdout
    assert (out / "report.json").is_file()  # the report is still written, to see why


def test_build_prints_what_it_could_not_make_on_stderr(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def build_without_a_model(kiln: Kiln, out: Path, *, model: bool, plans: bool) -> BuildResult:
        result = build_design(kiln, out, model=False, plans=plans)
        result.notes.append("No 3D model: this shape has no model yet")
        return result

    monkeypatch.setattr(kilndesigner_cli.main, "build_design", build_without_a_model)
    result = runner.invoke(app, ["build", str(ELECTRIC), "--out", str(tmp_path), "--no-plans"])
    assert result.exit_code == 0, result.output
    assert result.stderr == "No 3D model: this shape has no model yet\n"
    assert "No 3D model" not in result.stdout
    assert result.stdout.splitlines()[0] == "Electric front-loader, cone 10"


def test_without_a_bill_of_materials_no_materials_line_is_shown() -> None:
    # The engine always plans the masonry today, so a report without a bill is made by hand.
    report = design_report(load_design(ELECTRIC))
    assert report.bom is not None
    assert report.electric is not None
    without = report.model_copy(update={"bom": None})
    assert "  Materials:        $" in summary(report)
    assert "Materials:" not in summary(without)
    assert "Materials (priced)" in comparison_rows(report)
    assert "Materials (priced)" not in comparison_rows(without)
    assert comparison_rows(without)["Installed power"] == report.electric.installed_power


def test_importing_the_cli_switches_the_console_to_utf8(monkeypatch: pytest.MonkeyPatch) -> None:
    # A Windows console defaults to a code page with no Ω; a captured stream can't be switched.
    console = io.BytesIO()
    stdout = io.TextIOWrapper(console, encoding="cp1252", newline="\n")  # the same on Windows
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stderr", io.StringIO())
    importlib.reload(kilndesigner_cli.main)
    assert stdout.encoding == "utf-8"
    stdout.write("12.3 Ω\n")
    stdout.flush()
    assert console.getvalue() == "12.3 Ω\n".encode()
