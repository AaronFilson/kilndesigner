"""Kilns other than a single box or round chamber, laid out in brick: open tops on boxes, chambers
in a row (stepped up a slope or level), single chambers on a slope."""

from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.geometry import lining_parts, not_drawn, write_model
from kilndesigner.masonry import plan_masonry
from kilndesigner.model import Kiln
from kilndesigner.plans import build_plans
from kilndesigner.report import design_report

ROOT = Path(__file__).parents[2]
EXAMPLES = ROOT / "examples"
TEMPLATES = ROOT / "core" / "src" / "kilndesigner" / "data" / "templates"


def _with(path: Path, **chamber: object) -> Kiln:
    kiln = load_design(path)
    document = kiln.model_dump(mode="json", by_alias=True)
    roof = chamber.pop("roof", None)
    if roof is not None:
        document["roof"] = roof
    document["chamber"].update(chamber)
    return Kiln.model_validate(document)


def open_box() -> Kiln:
    """Ninodaguia's open-topped wood kiln, built square, its walls whole bricks thick."""
    kiln = _with(EXAMPLES / "olsen" / "ninodaguia.yaml", shape="box")
    document = kiln.model_dump(mode="json", by_alias=True)
    document["lining"]["walls"][0]["thickness"] = "13.5 inch"
    return Kiln.model_validate(document)


def test_an_open_box_is_laid_out_with_no_roof() -> None:
    kiln = open_box()
    assert not_drawn(kiln) is None
    parts = lining_parts(kiln)
    assert parts
    assert not [p for p in parts if p.wall == "roof"]
    masonry = plan_masonry(kiln)
    assert masonry.layers
    assert not [p for p in masonry.layers if p.part.wall == "roof"]
    report = design_report(kiln)
    assert report.bom is not None
    assert any("bricks" in line.needed for line in report.bom.lines)


def test_an_open_box_has_plans(tmp_path: Path) -> None:
    kiln = open_box()
    plans = build_plans(kiln, design_report(kiln), dxf_path=tmp_path / "s.dxf")
    assert plans.pdf.startswith(b"%PDF")
    assert (tmp_path / "s.dxf").exists()


@pytest.mark.geometry
def test_an_open_box_has_a_model(tmp_path: Path) -> None:
    kiln = open_box()
    written = write_model(kiln, design_report(kiln), tmp_path)
    assert written["gltf"].stat().st_size > 1000
