"""The design report: what it gathers from each calculation, and how it reports findings."""

from pathlib import Path

import pytest

from kilndesigner import load_design, parse_design
from kilndesigner.geometry import GeometryNotSupportedError, lining_parts
from kilndesigner.model import Kiln
from kilndesigner.report import ENGINE_VERSION, design_report

EXAMPLES = Path(__file__).parents[2] / "examples"
FT3_IN_MM3 = 304.8**3  # 1 ft = 304.8 mm exactly


def _variant(name: str, *changes: tuple[str, str]) -> Kiln:
    text = (EXAMPLES / f"{name}.yaml").read_text(encoding="utf-8")
    for old, new in changes:
        assert old in text
        text = text.replace(old, new)
    return parse_design(text)


def test_the_chamber_volume_is_in_the_designs_units() -> None:
    us = design_report(load_design(EXAMPLES / "electric-front-loader.yaml"))
    # 22.5 × 22.5 × 24 in = 12,150 in³ = 7.03 ft³
    assert us.chamber_volume == "7.03 ft³"
    assert us.engine_version == ENGINE_VERSION
    assert us.name == "Electric front-loader, cone 10"
    metric = design_report(
        _variant(
            "electric-front-loader",
            ("units: us", "units: metric"),
            ("width: 22.5 in", "width: 600 mm"),
            ("depth: 22.5 in", "depth: 600 mm"),
            ("height: 24 in", "height: 610 mm"),
        )
    )
    # 0.6 × 0.6 × 0.61 m = 0.2196 m³, to three figures
    assert metric.chamber_volume == "0.22 m³"


def test_a_hybrid_without_both_prices_is_not_costed() -> None:
    kiln = _variant("pnw-hybrid-crossdraft", ("  propane_price: 3.50 USD/gallon\n", ""))
    report = design_report(kiln)
    assert report.electric is not None
    assert report.gas is not None
    assert report.hybrid is None
    asks = [f for f in report.findings if "electricity_price and propane_price" in f.message]
    assert [f.level for f in asks] == ["info"]


def test_castables_are_measured_from_the_lining() -> None:
    kiln = load_design(EXAMPLES / "diy-castable-test-kiln.yaml")
    report = design_report(kiln)
    assert [c.mix.name for c in report.castables] == [m.name for m in kiln.castables or []]
    for c, mix in zip(report.castables, kiln.castables or [], strict=True):
        # Every part of the lining cast from this mix, added up
        volume = sum(p.volume for p in lining_parts(kiln) if p.material == mix.id) / FT3_IN_MM3
        assert volume > 0
        number, unit = c.placed.split()
        assert unit == "ft³"
        assert float(number) == pytest.approx(volume, rel=5e-3)  # shown to three figures
        # and what each mix found is in the report's findings
        assert {(f.level, f.message) for f in c.findings} <= {
            (f.level, f.message) for f in report.findings
        }


def test_findings_are_listed_once_each_errors_first() -> None:
    # One small burner can't hold this kiln at the top, and four cylinders can't keep up on a
    # cold day (20 °F: the liquid at 0 °F, the regulator still working)
    kiln = _variant(
        "gas-crossdraft",
        ("      wall: front\n", "      wall: front\n      model: Ransome B1\n      count: 1\n"),
        ("type: cylinders\n      count: 4", "type: cylinders\n      count: 1"),
    )
    report = design_report(kiln)
    levels = [f.level for f in report.findings]
    assert levels == sorted(levels, key=["error", "warning", "info"].index)
    keys = [(f.level, f.message) for f in report.findings]
    assert len(keys) == len(set(keys))
    assert report.errors == [f for f in report.findings if f.level == "error"]
    assert any("can't reach its top temperature" in f.message for f in report.errors)


def test_a_shape_without_a_masonry_plan_still_gets_a_report(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def no_plan(kiln: Kiln) -> object:
        raise GeometryNotSupportedError("no brick plan for this roof yet")

    monkeypatch.setattr("kilndesigner.report.plan_masonry", no_plan)
    report = design_report(load_design(EXAMPLES / "electric-front-loader.yaml"))
    assert report.masonry is None
    assert report.bom is None
    assert report.heat_loss.total  # the rest is still calculated
    assert report.electric is not None
    notes = [f for f in report.findings if f.message.startswith("No masonry plan")]
    assert [(f.level, f.message) for f in notes] == [
        ("info", "No masonry plan or bill of materials: no brick plan for this roof yet")
    ]
