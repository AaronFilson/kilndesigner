import re
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
    # Kast-O-Lite 26 has no specific heat in the library (Kast-O-Lite 30 has a class value)
    text = (EXAMPLES / "pnw-hybrid-crossdraft.yaml").read_text(encoding="utf-8")
    design = tmp_path / "kol26.yaml"
    design.write_text(
        text.replace("kast-o-lite-30-li-plus", "kast-o-lite-26-li-plus"), encoding="utf-8"
    )
    result = runner.invoke(app, ["simulate", str(design), "--out", str(tmp_path / "out")])
    assert result.exit_code == 2
    assert "specific_heat" in result.output


def test_simulate_a_hybrid_with_its_chart(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    text = (EXAMPLES / "pnw-hybrid-crossdraft.yaml").read_text(encoding="utf-8")
    # A test input only, not engineering data: the castable roof needs some c_p to run
    text = text.replace(
        "kast-o-lite-30-li-plus\n      thickness: 3 in\n",
        "kast-o-lite-30-li-plus\n      thickness: 3 in\n      specific_heat: 1 kJ/(kg*K)\n",
    )
    # Empty: with a full setting the elements climb so slowly the chart's late hand-overs run out
    # of hours before they stall
    text = re.sub(r"\n  setting:\n(    [^\n]*\n)+", "\n", text)
    assert "setting:" not in text
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
    # The chart's working and findings are printed, and a hand-over past the stall is marked
    assert "Cheapest hand-over:" in result.output
    assert "elements stall; burners from" in result.output
    assert "[info] The elements stall at about" in result.output
    assert (out / "switchover.json").is_file()


def test_simulate_solves_a_target_time(tmp_path: Path) -> None:
    design = str(EXAMPLES / "pnw-hybrid-crossdraft.yaml")
    result = runner.invoke(app, ["simulate", design, "--target", "6h", "--out", str(tmp_path)])
    assert result.exit_code == 0, result.output
    assert "a 6 h firing" in result.output
    assert "Propane supply options (pick one):" in result.output
    assert "1000 gal tank" in result.output
    assert (tmp_path / "target.json").is_file()
    worded = runner.invoke(
        app, ["simulate", design, "--target", "0.5 hour", "--out", str(tmp_path)]
    )
    assert worded.exit_code == 2
    assert "the schedule alone" in worded.output
