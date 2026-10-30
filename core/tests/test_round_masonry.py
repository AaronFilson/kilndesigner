"""A round chamber's masonry: rings of tapered brick, discs of straights, a dome by volume."""

from __future__ import annotations

from pathlib import Path

import pytest

from kilndesigner.designfile import load_design, parse_design
from kilndesigner.masonry import plan_masonry
from kilndesigner.report import design_report

EXAMPLES = Path(__file__).parents[2] / "examples"
ROUND = sorted(
    p for p in EXAMPLES.rglob("*.yaml") if "shape: round" in p.read_text(encoding="utf-8")
)

KILN = """
schema: 1
name: Round test kiln
units: us
firing: {cone: "6"}
chamber: {shape: round, width: 60 in, depth: 60 in, height: 36 in}
roof: {type: flat}
lining:
  walls: [{material: %s, thickness: 9 in}]
heat:
  fire:
    fuel: wood
    fireboxes: [{position: under, width: 24 in, length: 48 in, height: 24 in}]
draft: {type: up}
"""


def _kiln(material: str = "firebrick-medium-duty-smithfield") -> str:
    return KILN % material


def test_a_9_inch_round_wall_is_courses_of_key_rings() -> None:
    """60 in across: 55 keys a ring (test_rings), 36 in ÷ 2½ in = 14.4, so 15 courses, the top
    one ripped to 1 in."""
    plan = plan_masonry(parse_design(_kiln()))
    q = {x.name: x for x in plan.result.quantities}
    no3 = next(x for n, x in q.items() if n.endswith("No. 3 key"))
    no2 = next(x for n, x in q.items() if n.endswith("No. 2 key"))
    assert no3.detail.startswith("75 in the round wall")  # 5 a ring × 15 courses
    assert no2.detail.startswith("750 in the round wall")
    [info] = [f for f in plan.result.findings if f.message.startswith("Round kiln")]
    assert "9 in ring of 15 courses of 5 No. 3 key, 50 No. 2 key" in info.message
    assert "the top course ripped to 1 in" in info.message


def test_a_round_floor_is_rows_cut_to_the_circle() -> None:
    plan = plan_masonry(parse_design(_kiln()))
    [info] = [f for f in plan.result.findings if f.message.startswith("Round kiln")]
    assert "Floor, layer 1 from the inside: rows of straights across a 78 in circle" in info.message
    assert any("cut to" in c.cut for c in plan.result.cut_list)


def test_a_round_wall_not_in_whole_rings_is_reported() -> None:
    text = _kiln().replace("thickness: 9 in}]", "thickness: 7 in}]")
    plan = plan_masonry(parse_design(text))
    [bad] = [f for f in plan.result.findings if f.check is not None]
    assert "a round wall is laid in rings of 9 in key bricks and 4½ in arch bricks" in bad.message
    assert "Make it 4½ in or 9 in thick" in bad.message


@pytest.mark.parametrize("path", ROUND, ids=lambda p: p.stem)
def test_every_round_example_is_priced(path: Path) -> None:
    report = design_report(load_design(path))
    assert report.masonry is not None
    assert report.bom is not None
    assert not any("No masonry plan" in f.message for f in report.findings)
