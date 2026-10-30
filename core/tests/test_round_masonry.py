"""A round chamber's masonry: rings of tapered brick, discs of straights, a dome by volume."""

from __future__ import annotations

from pathlib import Path

import pytest

from kilndesigner.designfile import load_design, parse_design
from kilndesigner.masonry import plan_masonry
from kilndesigner.report import design_report
from kilndesigner.rings import IN, cut_diameter, nominal_diameter

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
    assert "a round wall is laid in rings of 9 in key bricks and 4½ in rings" in bad.message
    assert "Make it 4½ in or 9 in thick" in bad.message


@pytest.mark.parametrize("path", ROUND, ids=lambda p: p.stem)
def test_every_round_example_is_priced(path: Path) -> None:
    report = design_report(load_design(path))
    assert report.masonry is not None
    assert report.bom is not None
    assert not any("No masonry plan" in f.message for f in report.findings)


@pytest.mark.parametrize("method", ["mortar", "cut", "featheredge", "arch"])
def test_each_way_of_turning_a_4_and_a_half_inch_ring_is_counted(method: str) -> None:
    text = _kiln().replace("thickness: 9 in}]", "thickness: 4.5 in}]")
    kiln = parse_design(text)
    kiln = kiln.model_copy(update={"chamber": kiln.chamber.model_copy(update={"rings": method})})
    plan = plan_masonry(kiln)
    [inner] = plan.rings
    assert inner.series == method
    assert f"This one: {method}." in " ".join(f.message for f in plan.result.findings)
    assert plan.result.quantities


def _cut_ring_warnings(diameter: str) -> list[str]:
    text = _kiln().replace("thickness: 9 in}]", "thickness: 4.5 in}]")
    text = text.replace("width: 60 in, depth: 60 in", f"width: {diameter}, depth: {diameter}")
    kiln = parse_design(text)
    kiln = kiln.model_copy(update={"chamber": kiln.chamber.model_copy(update={"rings": "cut"})})
    return [f.message for f in plan_masonry(kiln).result.findings
            if f.check is not None and f.check.id == "masonry.cut-ring"]  # fmt: skip


def test_a_cut_ring_in_whole_bricks_is_not_warned() -> None:
    """24 full bricks round a 4½ in ring make cut_diameter(24) across inside (the mean of flats
    and corners); 60 in is 24.12 bricks, 1.1 in off round the ring, more than 1/16 in."""
    assert _cut_ring_warnings(f"{cut_diameter(24) / IN:.4f} in") == []
    assert len(_cut_ring_warnings("60 in")) == 1


def test_a_cut_ring_not_in_whole_bricks_is_warned_with_the_sizes_that_are() -> None:
    """58 in inside takes 23.44 bricks: laid as 23 and a closer, with the sizes 23 and 24
    whole bricks make."""
    [w] = _cut_ring_warnings("58 in")
    assert "23.44 full 9 in bricks" in w
    assert "the fewest, 23, and a closer" in w
    assert "(23 bricks)" in w
    assert "(24 bricks)" in w


def test_a_3_inch_electric_wall_is_one_ring_of_12_full_bricks() -> None:
    """A KM-1227-3: 12 sides of 3 in brick, 9 in faces outside, 4½ in courses. Its 36 in wall
    is 8 courses, the top ripped to 4½ in; no closer and no warning at the 12-brick diameter."""
    d = f"{nominal_diameter(12, 3 * IN) / IN:.4f} in"
    text = _kiln().replace("thickness: 9 in}]", "thickness: 3 in}]")
    text = text.replace("width: 60 in, depth: 60 in", f"width: {d}, depth: {d}")
    kiln = parse_design(text)
    kiln = kiln.model_copy(update={"chamber": kiln.chamber.model_copy(update={"rings": "cut"})})
    plan = plan_masonry(kiln)
    [wall] = plan.rings
    assert wall.series == "cut3"
    assert dict(wall.ring.counts) == {"straight cut to the angle": 12}
    assert wall.courses == 8
    assert "as electric kilns are built" in wall.description(True)
    assert not [
        f for f in plan.result.findings if f.check is not None and f.check.id == "masonry.cut-ring"
    ]
