from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from kilndesigner import load_design, parse_design
from kilndesigner.bom import bill_of_materials, price_list
from kilndesigner.geometry import Part
from kilndesigner.library import materials
from kilndesigner.masonry import IN, KERF, Cut, bricks_for_cuts, plan_layer, plan_masonry

EXAMPLES = Path(__file__).parents[2] / "examples"


def wall(length_in: float, height_in: float, thick_in: float = 4.5) -> Part:
    return Part(
        "left/1-ifb-jm26",
        "ifb-jm26",
        "insulating_firebrick",
        (0.0, 0.0, 0.0),
        (thick_in * IN, length_in * IN, height_in * IN),
    )


def test_a_wall_of_whole_bricks() -> None:
    """36 in × 5 in of stretchers: two courses of four bricks, the second staggered."""
    plan = plan_layer(wall(36, 5))
    assert plan is not None
    assert plan.laying == "stretcher"
    assert [len(c.pieces) for c in plan.courses] == [4, 5]
    assert all(p.is_whole for p in plan.courses[0].pieces)
    # the staggered course starts and ends with half bricks
    second = plan.courses[1].pieces
    assert second[0].length == pytest.approx(4.5 * IN)
    assert second[-1].length == pytest.approx(4.5 * IN)


def test_the_top_course_is_ripped_to_fit() -> None:
    plan = plan_layer(wall(18, 6))
    assert plan is not None
    top = plan.courses[-1]
    assert all(p.is_ripped for p in top.pieces)
    assert top.pieces[0].height == pytest.approx(1 * IN)


def test_thickness_chooses_the_laying() -> None:
    assert plan_layer(wall(18, 9, thick_in=2.5)).laying == "on_edge"  # type: ignore[union-attr]
    assert plan_layer(wall(18, 9, thick_in=9)).laying == "header"  # type: ignore[union-attr]
    assert plan_layer(wall(18, 9, thick_in=3.7)) is None


@settings(max_examples=50, deadline=None)
@given(
    length=st.floats(min_value=3, max_value=120),
    height=st.floats(min_value=2.5, max_value=60),
)
def test_every_course_fills_its_run_exactly(length: float, height: float) -> None:
    plan = plan_layer(wall(length, height))
    assert plan is not None
    for course in plan.courses:
        assert sum(p.length for p in course.pieces) == pytest.approx(length * IN)
        starts = [p.start for p in course.pieces]
        assert starts == sorted(starts)
    assert sum(c.pieces[0].height for c in plan.courses) == pytest.approx(height * IN)


def test_offcuts_are_reused() -> None:
    full = 9 * IN
    # two 4 in pieces fit in one brick (with a saw cut between them); a 6 in piece needs its own
    cuts = [Cut(4 * IN, 2.5 * IN, full, 2.5 * IN)] * 2 + [Cut(6 * IN, 2.5 * IN, full, 2.5 * IN)]
    assert bricks_for_cuts(cuts) == 2
    # 4.5 + 4.5 doesn't fit once the kerf is taken
    halves = [Cut(4.5 * IN, 2.5 * IN, full, 2.5 * IN)] * 2
    assert KERF > 0
    assert bricks_for_cuts(halves) == 2


def test_front_loader_quantities() -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    result = plan_masonry(kiln).result
    by_material = {q.material: q for q in result.quantities}
    assert set(by_material) == {"ifb-jm26", "ifb-k23", "kaowool-blanket-8pcf"}
    jm26 = by_material["ifb-jm26"]
    # Each brick is 101.25 in³; the JM 26 lining is about 22,000 in³, so 220+ bricks plus 10%.
    assert 230 < jm26.amount < 330
    assert by_material["kaowool-blanket-8pcf"].unit == "ft²"


def test_brick_count_covers_the_volume() -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    masonry = plan_masonry(kiln)
    brick_volume = 9 * 4.5 * 2.5 * IN**3
    for mid in ("ifb-jm26", "ifb-k23"):
        lining = sum(layer.part.volume for layer in masonry.layers if layer.part.material == mid)
        bought = next(q.amount for q in masonry.result.quantities if q.material == mid)
        assert bought * brick_volume >= lining


def test_every_price_names_a_library_entry() -> None:
    known = set(materials()) | {"kanthal-a1"}
    assert {item.material for item in price_list().items} <= known


def test_bom_totals_and_budget() -> None:
    text = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    kiln = parse_design(text + "  materials_budget: 1000 USD\n")
    bom = bill_of_materials(kiln, plan_masonry(kiln).result, None)
    assert bom.total == pytest.approx(sum(line.cost or 0 for line in bom.lines))
    assert any("over the $1,000 budget" in f.message for f in bom.findings)
