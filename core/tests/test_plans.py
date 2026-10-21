from pathlib import Path
from xml.etree import ElementTree

import pytest

from kilndesigner import load_design
from kilndesigner.drawings import course_plan_svg, section_views, view_svg
from kilndesigner.masonry import plan_masonry
from kilndesigner.plans import build_plans
from kilndesigner.report import design_report

EXAMPLES = Path(__file__).parents[2] / "examples"


@pytest.fixture(scope="module")
def kiln():  # type: ignore[no-untyped-def]
    return load_design(EXAMPLES / "electric-front-loader.yaml")


def test_sections_cut_the_right_parts(kiln) -> None:  # type: ignore[no-untyped-def]
    front, side, plan = section_views(kiln, element_rows=9, coil_mm=10)
    front_parts = {r.layer.split("/")[0] for r in front.rects}
    assert front_parts == {"floor", "left", "right", "roof"}
    side_parts = {r.layer.split("/")[0] for r in side.rects}
    assert side_parts == {"floor", "back", "door", "roof"}
    assert {r.layer.split("/")[0] for r in plan.rects} == {"left", "right", "back", "door"}
    # elements on the left and right walls show in section A–A; on the back wall in B–B
    assert len(front.circles) == 18
    assert len(side.circles) == 9


def test_svgs_are_well_formed(kiln) -> None:  # type: ignore[no-untyped-def]
    for view in section_views(kiln):
        ElementTree.fromstring(view_svg(view))
    for layer in plan_masonry(kiln).layers:
        root = ElementTree.fromstring(course_plan_svg(layer, us=True))
        rects = root.findall(".//{http://www.w3.org/2000/svg}rect")
        assert len(rects) == len(layer.pieces)


def test_plans_compile_and_are_deterministic(kiln, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    report = design_report(kiln)
    first = build_plans(kiln, report, dxf_path=tmp_path / "a.dxf")
    second = build_plans(kiln, report)
    assert first.pdf.startswith(b"%PDF")
    assert first.pdf == second.pdf
    assert (tmp_path / "a.dxf").read_text(encoding="utf-8").startswith("  0\nSECTION")


def test_dxf_has_a_layer_per_part(kiln, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    from ezdxf.filemanagement import readfile  # pyright: ignore[reportMissingTypeStubs]

    build_plans(kiln, design_report(kiln), dxf_path=tmp_path / "s.dxf")
    doc = readfile(tmp_path / "s.dxf")
    names = {layer.dxf.name for layer in doc.layers}
    assert "left_1-ifb-jm26" in names
    assert "dimensions" in names
