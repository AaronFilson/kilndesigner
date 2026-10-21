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


def test_schema_is_json() -> None:
    result = runner.invoke(app, ["schema"])
    assert result.exit_code == 0
    assert json.loads(result.output)["title"] == "Kiln"
