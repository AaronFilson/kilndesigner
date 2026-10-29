import itertools
import math
from pathlib import Path

import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from kilndesigner import Kiln, load_design, parse_design
from kilndesigner.bom import bill_of_materials, price_list
from kilndesigner.geometry import ArchShape, Part, lining_parts
from kilndesigner.library import materials
from kilndesigner.masonry import (
    BRICK_VOLUME,
    IN,
    KERF,
    TOL,
    ArchRing,
    Cut,
    arch_ring,
    brick_sizes,
    bricks_for_cuts,
    plan_layer,
    plan_layers,
    plan_masonry,
)
from kilndesigner.shape import Arch

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


def test_each_wall_of_brick_is_titled_by_where_it_is_in_the_layer() -> None:
    plans = plan_layers(wall(36, 10, thick_in=13.5))
    assert plans is not None
    jm26 = "Morgan Thermal Ceramics JM 26 insulating firebrick"
    assert [p.title() for p in plans] == [
        f"Left wall, layer 1 from the inside: {jm26}, wall of brick 1 of 2 from the inside",
        f"Left wall, layer 1 from the inside: {jm26}, wall of brick 2 of 2 from the inside",
    ]
    # One brick thick: no wall of brick to say
    [single] = plan_layers(wall(36, 10)) or []
    assert single.title() == f"Left wall, layer 1 from the inside: {jm26}"


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
    finding = next(f for f in findings if f.message.startswith("Left wall"))
    message = finding.message
    assert message.startswith(
        "Left wall, layer 1 from the inside is 6¾ in of Morgan Thermal Ceramics JM 26"
    )
    assert "missing from the brick count, the bill of materials and the price" in message
    assert message.endswith("Make it 5 in or 7 in thick.")
    # Its sheet: 6¾ in is ¼ in from 7 in (4½ + 2½), the nearer of the sums of whole bricks
    check = finding.check
    assert check is not None
    assert check.id == "masonry.thickness"
    assert check.requirements[0].margin.startswith("Δ = 0.25 in, ")
    assert check.solve == "Passes when T ≥ 6.961 in"  # within the planner's 1 mm of 7 in


@settings(max_examples=50, deadline=None)
@given(
    length=st.floats(min_value=3, max_value=120),
    height=st.floats(min_value=2.5, max_value=60),
)
def test_every_course_fills_its_run_exactly(length: float, height: float) -> None:
    plan = plan_layer(wall(length, height))
    assert plan is not None
    # exact to the planner's tolerance: a sliver thinner than TOL is never cut
    for course in plan.courses:
        assert sum(p.length for p in course.pieces) == pytest.approx(length * IN, abs=TOL)
        starts = [p.start for p in course.pieces]
        assert starts == sorted(starts)
    assert sum(c.pieces[0].height for c in plan.courses) == pytest.approx(height * IN, abs=TOL)


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


# Arch rings: straights and one tapered shape. Thin ends, in inches, from the 9-inch series
# (electric-and-thermal.md §5 [S54]): arches taper along their 4½ in depth, wedges along 9 in.
THIN_END = {
    "No. 1 arch": 2.125,
    "No. 2 arch": 1.75,
    "No. 3 arch": 1.0,
    "No. 1-X wedge": 2.25,
    "No. 1 wedge": 1.875,
    "No. 2 wedge": 1.5,
}


def arch_layer(span_in: float, rise_in: float, depth_in: float, length_in: float = 54) -> Part:
    """An arch layer ``depth_in`` deep on the inside of a sprung arch, as lining_parts makes it."""
    arch = Arch(span_in * IN, rise_in * IN)
    return Part(
        "roof/1-ifb-jm26",
        "ifb-jm26",
        "insulating_firebrick",
        (0.0, 0.0, 0.0),
        (span_in * IN, length_in * IN, rise_in * IN),
        arch=ArchShape(arch.radius, depth_in * IN, 0.0, arch.half_angle),
        face="roof",
    )


def test_a_60_degree_arch_is_turned_with_no_1_arches() -> None:
    """28 in span, 3¾ in rise, 4½ in deep, 54 in long.

    R = (14² + 3.75²) / (2 × 3.75) = 28.008 in and θ = asin(14 / R) = 0.5234 rad (30°). The outer
    arc is 2θ × 4½ = 4.711 in longer than the inner, and a No. 1 arch, 2½ in tapering to 2⅛,
    makes up ⅜ in of it: 12.56, so 13 a ring. Every brick is 2½ in across the outer arc,
    2θ(R + 4½) = 34.03 in: 13.6 bricks, so 14, and the 14th is a straight. (Rounded separately,
    the straights came out 2: one more than closes the ring, the review's bug.) Rings are a
    brick's 9 in long: 54 / 9 = 6.
    """
    ring = arch_ring(arch_layer(28, 3.75, 4.5))
    assert ring == ArchRing("No. 1 arch", shaped=13 * 6, straights=1 * 6, rings=6)
    assert ring is not None
    assert ring.describe() == "6 rings, each of 13 No. 1 arch bricks and 1 straight"


def test_a_tighter_arch_takes_a_steeper_taper() -> None:
    """A half circle 12 in across, 4½ in deep: θ = π/2, R = 6 in. The outer arc is 4.5π = 14.14
    in longer than the inner arc's 6π = 18.85 in. No. 1 arches (⅜ in each) would take 37.7
    bricks, 80 in of inside face; No. 2s (¾ in) 18.85 bricks, 33 in: both more than the inner
    arc. No. 3s (1½ in): 9.42 bricks, 9.42 in of it, and 3.77 straights fill the rest: 10 and 4.
    """
    ring = arch_ring(arch_layer(12, 6, 4.5))
    assert ring == ArchRing("No. 3 arch", shaped=10 * 6, straights=4 * 6, rings=6)


def test_a_9_inch_arch_is_turned_with_wedges_in_4_inch_rings() -> None:
    """The 60° arch above, 9 in deep: the outer arc is 2θ × 9 = 9.42 in longer. No. 1-X wedges
    (¼ in each) would take 37.7, 85 in of inside face against the 29.32 in arc. No. 1 wedges
    (⅝ in): 15.07, so 16; the outer arc, 38.74 in, takes 15.5 bricks, so the 16 wedges close it
    with no straight. Wedges lie 4½ in along the kiln: 54 / 4½ = 12 rings."""
    ring = arch_ring(arch_layer(28, 3.75, 9))
    assert ring == ArchRing("No. 1 wedge", shaped=16 * 12, straights=0, rings=12)


@pytest.mark.parametrize(
    ("span", "rise", "depth"),
    [(18, 2.4, 4.5), (28, 3.75, 4.5), (40, 5.4, 4.5), (36, 9, 4.5), (27, 4, 4.5), (54, 7.2, 9)],
)
def test_every_ring_counted_closes_its_arch(span: float, rise: float, depth: float) -> None:
    """Round the ring: the bricks' thin ends cover the inner arc, their 2½ in faces the outer."""
    part = arch_layer(span, rise, depth)
    ring = arch_ring(part)
    assert ring is not None
    assert part.arch is not None
    shaped, straights = ring.shaped // ring.rings, ring.straights // ring.rings
    inner = 2 * part.arch.half_angle * part.arch.radius / IN
    outer = inner + 2 * part.arch.half_angle * depth
    assert shaped * THIN_END[ring.shape] + straights * 2.5 >= inner
    assert (shaped + straights) * 2.5 >= outer


def test_an_arch_no_shape_turns_is_left_to_be_counted_by_volume() -> None:
    # A half circle 4 in across: even No. 3 arches (1½ in each) need 9.42 of them for the 14.1 in
    # the outer arc gains, and their 9.42 in of thin ends overrun the 6.28 in inner arc
    assert arch_ring(arch_layer(4, 2, 4.5)) is None
    # No arch or wedge is 2½ in deep, and a flat layer is no arch at all
    assert arch_ring(arch_layer(28, 3.75, 2.5)) is None
    assert arch_ring(wall(36, 10)) is None


def gas_crossdraft_with_a_brick_arch(thickness: str) -> Kiln:
    """The gas cross-draft (28 in span, 3¾ in rise, the roof 64 in long outside) with a JM 26
    arch of ``thickness`` under 2 in of blanket."""
    document = load_design(EXAMPLES / "gas-crossdraft.yaml").model_dump(mode="json", by_alias=True)
    roof = [
        {"material": "ifb-jm26", "thickness": thickness},
        {"material": "kaowool-blanket-8pcf", "thickness": "2 in"},
    ]
    return Kiln.model_validate({**document, "lining": {**document["lining"], "roof": roof}})


def test_a_brick_arch_is_bought_in_arch_bricks() -> None:
    """The 60° arch's rings: 13 No. 1 arches and 1 straight each (above). 64 in / 9 in is 7.1,
    so 8 rings: 104 arch bricks, and 115 with 10 % for breakage."""
    result = plan_masonry(gas_crossdraft_with_a_brick_arch("4.5 in")).result
    jm26 = "Morgan Thermal Ceramics JM 26 insulating firebrick"
    shaped = next(q for q in result.quantities if q.name == f"{jm26}, No. 1 arch")
    assert (shaped.amount, shaped.unit, shaped.kind) == (115, "bricks", "insulating_firebrick")
    assert shaped.detail == "104 in the arch plus 10% for breakage"
    arches = next(f for f in result.findings if f.message.startswith("Arch bricks"))
    assert (
        "Roof, layer 1 from the inside: 8 rings, each of 13 No. 1 arch bricks and 1 straight;"
        in arches.message
    )
    assert arches.reference == (
        "Arch and wedge shapes, 9-inch series; electric-and-thermal.md §5 [S54]"
    )

    # 9 in deep: wedges, 4½ in along the kiln, so 64 / 4.5 = 14.2: 15 rings of 16
    result = plan_masonry(gas_crossdraft_with_a_brick_arch("9 in")).result
    wedges = next(q for q in result.quantities if q.name == f"{jm26}, No. 1 wedge")
    assert wedges.amount == math.ceil(15 * 16 * 1.1)


def test_a_brick_arch_no_shape_fits_is_counted_by_volume() -> None:
    kiln = gas_crossdraft_with_a_brick_arch("2.5 in")
    result = plan_masonry(kiln).result
    assert not [q for q in result.quantities if "arch" in q.name or "wedge" in q.name]
    roof = next(p for p in lining_parts(kiln) if p.name == "roof/1-ifb-jm26")
    count = math.ceil(roof.volume / BRICK_VOLUME)
    arches = next(f.message for f in result.findings if f.message.startswith("Arch bricks"))
    assert f"Roof, layer 1 from the inside: about {count} bricks by volume;" in arches


@pytest.mark.parametrize(
    ("span", "straights"),
    [(45, 5), (36, 1)],
)
def test_the_arch_counts_match_pitelkas_published_arches(span: float, straights: int) -> None:
    """Pitelka's 4½ in arches at 2.3 in/ft: 45 in, "18 rows of #1 arch and 5 rows of
    straights"; 36 in, "18 rows of #1 arch plus one straight in theory" (kiln-hardware.md §4.4
    [S4] [S11])."""
    ring = arch_ring(arch_layer(span, 2.302 * span / 12, 4.5))
    assert ring is not None
    assert (ring.shape, ring.shaped // ring.rings, ring.straights // ring.rings) == (
        "No. 1 arch",
        18,
        straights,
    )
