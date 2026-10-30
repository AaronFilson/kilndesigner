from pathlib import Path

import pytest
from typer.testing import CliRunner

from kilndesigner_cli.main import app

EXAMPLES = Path(__file__).parents[2] / "examples"
runner = CliRunner()


def test_simulate_writes_parquet(tmp_path: Path) -> None:
    result = runner.invoke(
        app, ["simulate", str(EXAMPLES / "electric-front-loader.yaml"), "--out", str(tmp_path)]
    )
    assert result.exit_code == 0, result.output
    assert "Firing time:" in result.output
    assert "Schedule kept:    yes" in result.output
    assert "Cost:             $" in result.output
    assert (tmp_path / "walls.parquet").is_file()
    assert (tmp_path / "series.parquet").is_file()


def test_simulate_refuses_a_castable_without_specific_heat(tmp_path: Path) -> None:
    result = runner.invoke(
        app, ["simulate", str(EXAMPLES / "pnw-hybrid-crossdraft.yaml"), "--out", str(tmp_path)]
    )
    assert result.exit_code == 2
    assert "specific_heat" in result.output


def test_simulate_a_hybrid_with_its_chart(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    text = (EXAMPLES / "pnw-hybrid-crossdraft.yaml").read_text(encoding="utf-8")
    # A test input only, not engineering data: the castable roof needs some c_p to run
    text = text.replace(
        "kast-o-lite-30-li-plus\n      thickness: 3 in\n",
        "kast-o-lite-30-li-plus\n      thickness: 3 in\n      specific_heat: 1 kJ/(kg*K)\n",
    )
    design = tmp_path / "hybrid.yaml"
    design.write_text(text, encoding="utf-8")
    monkeypatch.setattr("kilndesigner.simulation.DT", 900.0)
    import kilndesigner.simulation as sim

    original = sim.switch_over_chart
    monkeypatch.setattr(
        "kilndesigner_cli.main.switch_over_chart",
        lambda kiln: original(kiln, step_f=900, dt=900.0),  # pyright: ignore[reportUnknownLambdaType]
    )
    out = tmp_path / "out"
    result = runner.invoke(
        app,
        ["simulate", str(design), "--out", str(out), "--switch-over", "1200 degF", "--chart"],
    )
    assert result.exit_code == 0, result.output
    assert "Fuel burned:" in result.output
    assert "gal propane" in result.output
    assert "Hand-over" in result.output
    assert (out / "switchover.json").is_file()
