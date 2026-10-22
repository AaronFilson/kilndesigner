import json
from pathlib import Path

from typer.testing import CliRunner

from kilndesigner_cli.main import app

EXAMPLES = Path(__file__).parents[2] / "examples"
runner = CliRunner()


def test_check_accepts_a_valid_design() -> None:
    result = runner.invoke(app, ["check", str(EXAMPLES / "electric-front-loader.yaml")])
    assert result.exit_code == 0, result.output
    assert "is valid" in result.output


def test_check_rejects_an_invalid_design(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yaml"
    bad.write_text("name: x\n", encoding="utf-8")
    result = runner.invoke(app, ["check", str(bad)])
    assert result.exit_code == 2


def test_build_writes_the_report_without_a_model(tmp_path: Path) -> None:
    design = str(EXAMPLES / "electric-front-loader.yaml")
    result = runner.invoke(app, ["build", design, "--out", str(tmp_path), "--no-model"])
    assert result.exit_code == 0, result.output
    assert "Heat loss at top" in result.output
    report = json.loads((tmp_path / "report.json").read_text(encoding="utf-8"))
    assert report["electric"]["elements"]["count"] >= 3


def test_compare_shows_each_design() -> None:
    door = str(EXAMPLES / "pnw-hybrid-crossdraft.yaml")
    budget = str(EXAMPLES / "pnw-hybrid-crossdraft-budget.yaml")
    result = runner.invoke(app, ["compare", door, budget])
    assert result.exit_code == 0, result.output
    assert "pnw-hybrid-crossdraft-budget" in result.output
    assert "Burner input" in result.output
    assert "Materials (priced)" in result.output


def test_schema_is_json() -> None:
    result = runner.invoke(app, ["schema"])
    assert result.exit_code == 0
    assert json.loads(result.output)["title"] == "Kiln"
