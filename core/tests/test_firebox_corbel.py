"""A firebox roofed with a corbel (corbel.py): its courses drawn, worked and checked, and refused
where the sources or the design don't reach."""

from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from kilndesigner.corbel import TMS
from kilndesigner.designfile import load_design
from kilndesigner.fire import design_fire
from kilndesigner.firebox_parts import (
    brick_wall_in,
    corbel_refusal,
    firebox_boxes,
    firebox_corbel,
    firebox_findings,
)
from kilndesigner.geometry import lining_parts
from kilndesigner.model import Kiln

ROOT = Path(__file__).parents[2]
EXAMPLE = ROOT / "examples" / "corbel-firebox-crossdraft.yaml"
TEMPLATES = ROOT / "core" / "src" / "kilndesigner" / "data" / "templates"
IN = 25.4


def _doc() -> dict[str, Any]:
    return yaml.safe_load(EXAMPLE.read_text(encoding="utf-8"))


def _kiln(**firebox: Any) -> Kiln:
    doc = _doc()
    doc["heat"]["fire"]["fireboxes"][0].update(firebox)
    return Kiln.model_validate(doc)


def _corbels(kiln: Kiln) -> list[Any]:
    return [p for p in lining_parts(kiln) if "/corbel-" in p.name]


def test_the_example_corbels_its_firebox_in_three_courses() -> None:
    kiln = load_design(EXAMPLE)
    assert brick_wall_in(kiln) == pytest.approx(9.0)
    c = firebox_corbel(kiln, kiln.heat.fire.fireboxes[0])  # type: ignore[union-attr]
    assert c is not None
    # 13½ in closed by 1¼ in steps (min(2½/2, 9/3)) to 6 in: three courses, 7½ in of rise
    assert (c.courses, c.step, c.gap, c.rise) == (3, 1.25, 6.0, 7.5)
    assert c.check().status == "pass"
    (box,) = firebox_boxes(kiln)
    parts = _corbels(kiln)
    assert len(parts) == 6
    top = [p for p in parts if "corbel-3" in p.name]
    # The top course projects three steps from each side wall, its top at the firebox's roof
    for p in top:
        assert p.hi[1] - p.lo[1] == pytest.approx(3.75 * IN)
        assert p.hi[2] == pytest.approx(box.hi[2])
        assert p.face == "roof"
    bottom = [p for p in parts if "corbel-1" in p.name]
    assert all(p.lo[2] == pytest.approx(box.hi[2] - 7.5 * IN) for p in bottom)
    assert corbel_refusal(kiln, box) is None


def test_the_report_carries_the_corbels_working() -> None:
    fire = design_fire(load_design(EXAMPLE))
    (step,) = [s for s in fire.working if "Corbel" in s.name]
    assert "3 course(s) a side" in step.value
    assert step.reference is not None
    assert TMS in step.reference
    assert "combustion-and-masonry.md §5" in step.reference
    assert not [f for f in fire.findings if f.check is not None and f.check.id == "corbel"]


def test_a_front_firebox_corbels_across_x() -> None:
    kiln = _kiln(position="front", width="12 in")
    parts = _corbels(kiln)
    assert parts
    assert all(p.hi[0] - p.lo[0] < 12 * IN / 2 for p in parts)


def test_a_wall_too_thin_fails_the_tms_check() -> None:
    doc = _doc()
    doc["lining"]["walls"] = doc["lining"]["walls"][:1]  # 4½ in alone
    kiln = Kiln.model_validate(doc)
    fire = design_fire(kiln)
    failed = [f for f in fire.findings if f.check is not None and f.check.id == "corbel"]
    assert failed
    assert failed[0].level in ("warning", "error")


def test_a_wide_corbel_is_noted_past_rhodes() -> None:
    fire = design_fire(_kiln(width="20 in", height="30 in"))
    assert any("Rhodes finds corbels impractical" in f.message for f in fire.findings)


def test_a_corbel_too_tall_for_its_firebox_is_drawn_flat_and_said() -> None:
    kiln = _kiln(height="7 in")
    assert not _corbels(kiln)
    (box,) = firebox_boxes(kiln)
    refused = corbel_refusal(kiln, box)
    assert refused is not None
    assert "make it taller" in refused
    assert any("corbel roof refused" in f.message for f in firebox_findings(kiln))


def test_a_corbel_needs_brick_walls() -> None:
    doc = _doc()
    doc["lining"]["walls"] = [{"material": "kast-o-lite-30-li-plus", "thickness": "9 in"}]
    kiln = Kiln.model_validate(doc)
    assert brick_wall_in(kiln) == 0
    assert firebox_corbel(kiln, kiln.heat.fire.fireboxes[0]) is None  # type: ignore[union-attr]
    assert not _corbels(kiln)
    (box,) = firebox_boxes(kiln)
    assert "isn't brick" in (corbel_refusal(kiln, box) or "")


def test_a_trough_has_no_roof_to_corbel() -> None:
    doc = yaml.safe_load((TEMPLATES / "climbing.yaml").read_text(encoding="utf-8"))
    for fb in doc["heat"]["fire"]["fireboxes"]:
        fb["roof"] = "corbel"
    kiln = Kiln.model_validate(doc)
    boxes = [b for b in firebox_boxes(kiln) if b.trough]
    assert boxes
    assert "trough" in (corbel_refusal(kiln, boxes[0]) or "")
    assert not _corbels(kiln)


def test_a_flat_roof_has_no_corbel() -> None:
    kiln = _kiln(roof="flat")
    (box,) = firebox_boxes(kiln)
    assert corbel_refusal(kiln, box) is None
    assert firebox_corbel(kiln, box.box) is None
    assert not _corbels(kiln)


@pytest.mark.parametrize(
    ("change", "says"),
    [
        ({"position": "under"}, "roofed by the chamber's floor"),
        ({"width": "25 in", "inlet": None}, "past the 24 in"),
        ({"roof": "flat", "corbel_step": "1 in"}, "corbel_step is for a corbel roof"),
        ({"corbel_step": "0 in"}, "must step in by something"),
    ],
)
def test_the_design_file_refuses_what_no_source_reaches(change: dict[str, Any], says: str) -> None:
    with pytest.raises(ValidationError, match=says):
        _kiln(**change)


def test_a_given_step_is_used() -> None:
    kiln = _kiln(corbel_step="1 in")
    c = firebox_corbel(kiln, kiln.heat.fire.fireboxes[0])  # type: ignore[union-attr]
    assert c is not None
    assert c.step == 1.0
    assert c.courses == 4
