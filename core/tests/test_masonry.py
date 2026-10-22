import itertools
from pathlib import Path

import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from kilndesigner import Kiln, load_design, parse_design
from kilndesigner.bom import bill_of_materials, price_list
from kilndesigner.geometry import Part
from kilndesigner.library import materials
from kilndesigner.masonry import (
    IN,
    KERF,
    Cut,
    brick_sizes,
    bricks_for_cuts,
    plan_layer,
    plan_layers,
    plan_masonry,
)

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


@pytest.mark.parametrize(
    ("inches", "walls"),
    [
        (2.5, [2.5]),
        (9, [9]),
        (13.5, [9, 4.5]),
        (7, [4.5, 2.5]),
        (5, [2.5, 2.5]),
        (18, [9, 9]),
        (6.75, None),
        (3.7, None),
    ],
)
def test_a_layer_is_the_fewest_walls_of_brick_that_add_up(
    inches: float, walls: list[float] | None
) -> None:
    found = brick_sizes(inches * IN)
    assert ([round(s / IN, 3) for s in found] if found else None) == walls


def test_a_metric_thickness_within_a_millimetre_is_a_brick_size() -> None:
    assert brick_sizes(114) == [4.5 * IN]  # 4½ in is 114.3 mm


def test_a_thick_layer_is_headers_beside_stretchers() -> None:
    plans = plan_layers(wall(36, 10, thick_in=13.5))
    assert plans is not None
    assert [(p.laying, round(p.part.thickness / IN, 3)) for p in plans] == [
        ("header", 9),
        ("stretcher", 4.5),
    ]
    assert [p.within for p in plans] == [(1, 2), (2, 2)]
    # The left wall's inside face is its high x: the headers are on the inside
    assert plans[0].part.hi[0] == pytest.approx(13.5 * IN)
    assert plans[1].part.lo[0] == pytest.approx(0)


@settings(max_examples=30, deadline=None)
@given(nine=st.integers(0, 2), four=st.integers(0, 2), two=st.integers(0, 2))
def test_walls_of_brick_fill_the_layer_without_gaps(nine: int, four: int, two: int) -> None:
    assume(nine + four + two)
    thick = 9 * nine + 4.5 * four + 2.5 * two
    plans = plan_layers(wall(27, 10, thick_in=thick))
    assert plans is not None
    assert sum(p.part.thickness for p in plans) == pytest.approx(thick * IN)
    for inner, outer in itertools.pairwise(p.part for p in plans):
        assert outer.hi[0] == pytest.approx(inner.lo[0])


def front_loader_with_walls(thickness: str) -> Kiln:
    text = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    first = "    - material: ifb-jm26\n      thickness: 4.5 in"
    assert first in text
    return parse_design(
        text.replace(first, f"    - material: ifb-jm26\n      thickness: {thickness}", 1)
    )


def test_a_thick_wall_is_counted_and_explained() -> None:
    masonry = plan_masonry(front_loader_with_walls("13.5 in"))
    messages = [f.message for f in masonry.result.findings]
    assert not any("missing from the brick count" in m for m in messages)
    side = next(m for m in messages if m.startswith("Layers thicker than one brick"))
    assert "Left wall, layer 1 from the inside (13½ in): 9 in of bricks laid through" in side
    assert "then 4½ in of bricks laid flat along the wall" in side
    brick_volume = 9 * 4.5 * 2.5 * IN**3
    lining = sum(p.part.volume for p in masonry.layers if p.part.material == "ifb-jm26")
    bought = next(q.amount for q in masonry.result.quantities if q.material == "ifb-jm26")
    assert bought * brick_volume >= lining


def test_a_layer_whole_bricks_cant_make_says_where_why_and_what_to_do() -> None:
    findings = plan_masonry(front_loader_with_walls("6.75 in")).result.findings
    message = next(f.message for f in findings if f.message.startswith("Left wall"))
    assert message.startswith(
        "Left wall, layer 1 from the inside is 6¾ in of Morgan Thermal Ceramics JM 26"
    )
    assert "missing from the brick count, the bill of materials and the price" in message
    assert message.endswith("Make it 5 in or 7 in thick.")


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
