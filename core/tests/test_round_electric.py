"""Round electric kilns: a faceted ring of 3 in brick, its grooves, slabs and bands."""

from __future__ import annotations

import math
from pathlib import Path

import pytest

from kilndesigner.designfile import load_design, parse_design
from kilndesigner.electric import design_elements
from kilndesigner.frame import design_frame
from kilndesigner.masonry import plan_masonry
from kilndesigner.rings import IN, inside_apothem
from kilndesigner.shape import chamber_shape, facets

EXAMPLE = Path(__file__).parents[2] / "examples" / "round-electric.yaml"
SOURCE = EXAMPLE.read_text(encoding="utf-8")
LID = "loading:\n  type: lid\n"


def kiln(**swap: str):  # type: ignore[no-untyped-def]
    text = SOURCE
    for old, new in swap.items():
        text = text.replace(old.replace("_", " "), new)
    return parse_design(text)


def test_twelve_facets_and_the_polygons_areas() -> None:
    k = kiln()
    assert facets(k) == 12
    s = chamber_shape(k)
    d = 28.075 * IN / 1000
    a = inside_apothem(d, 12)
    # Flats and corners average the diameter; the flats are 2·a·tan(π/12) each
    assert a * (1 + 1 / math.cos(math.pi / 12)) == pytest.approx(d)
    assert s.perimeter() == pytest.approx(24 * a * math.tan(math.pi / 12))
    assert s.volume == pytest.approx(12 * a * a * math.tan(math.pi / 12) * 27 * IN / 1000)
    walls = sum(f.inside_area for f in s.faces() if f.orientation == "vertical")
    assert walls == pytest.approx(s.perimeter() * 27 * IN / 1000)
    # Between the inscribed and circumscribed circles
    assert 2 * math.pi * a < s.perimeter() < 2 * math.pi * a / math.cos(math.pi / 12)


def test_a_wall_that_isnt_whole_bricks_is_a_circle() -> None:
    k = kiln(**{"28.075 in": "30 in"})
    assert facets(k) is None
    assert chamber_shape(k).perimeter() == pytest.approx(math.pi * 30 * IN / 1000)
    step = next(s for s in design_elements(k).working if s.name.startswith("Groove round"))
    assert "round the circle" in (step.note or "")


def test_only_a_brick_ring_cut_to_the_angle_has_facets() -> None:
    blanket = parse_design(SOURCE.replace("ifb-k23", "kaowool-blanket-8pcf", 1))
    assert facets(blanket) is None
    k = kiln()
    mortar = k.model_copy(update={"chamber": k.chamber.model_copy(update={"rings": "mortar"})})
    assert facets(mortar) is None
    box = parse_design(SOURCE.replace("  shape: round\n", "").replace(LID, ""))
    assert facets(box) is None
    thick = parse_design(SOURCE.replace("thickness: 3 in", "thickness: 5 in", 1))
    assert facets(thick) is None


def test_elements_in_grooves_round_the_facets() -> None:
    k = kiln()
    e = design_elements(k)
    assert e.elements is not None
    assert not [f for f in e.findings if f.level == "error"]
    step = next(s for s in e.working if s.name.startswith("Groove round"))
    assert step.inputs["N, facets"] == "12"
    assert step.inputs["courses"] == "6"
    assert "No source gives a groove pitch" in (step.note or "")
    loading = next(s for s in e.working if s.name == "Wall loading")
    assert "left, right, back, front" in loading.inputs["element walls"]


def test_a_shallow_ring_has_too_few_grooves_for_the_power() -> None:
    e = design_elements(kiln(**{"height: 27 in": "height: 9 in"}))
    assert e.elements is None
    assert any(f.level == "error" and "No standard wire gauge" in f.message for f in e.findings)


def test_slabs_of_3_in_brick_out_to_the_corners() -> None:
    plan = plan_masonry(kiln())
    floors = [p for p in plan.layers if p.part.name.startswith("floor/")]
    assert len(floors) == 1
    a = inside_apothem(28.075 * IN, 12)
    corner = (a + 3 * IN) / math.cos(math.pi / 12)
    assert floors[0].circle == pytest.approx(corner)
    text = " ".join(f.message for f in plan.result.findings)
    assert "Floor, layer 1" in text
    assert "Roof, layer 1" in text


def test_bands_are_listed_not_sized() -> None:
    f = design_frame(kiln())
    (band,) = f.findings
    assert "3 round the wall" in band.message
    assert "round the lid" in band.message
    assert "aren't sized" in band.message
    domed = parse_design(SOURCE.replace("type: flat", "type: dome\n  rise: 6 in").replace(LID, ""))
    assert "round the lid" not in design_frame(domed).findings[0].message


def test_an_electric_lid_and_floor_are_polygons_of_whole_bricks_banded() -> None:
    """The lid and floor slab follow the kiln's 12 sides, as many whole bricks as fit and the
    edge bricks cut to the profile, each in a steel band; only the lid's band is hinged (the
    user, electric-kiln-survey.md)."""
    kiln = load_design(Path(__file__).parents[2] / "examples" / "round-electric.yaml")
    text = " ".join(f.message for f in plan_masonry(kiln).result.findings)
    assert "Floor, layer 1 from the inside: a 12-sided slab of mortared straights" in text
    assert "cut to the kiln's profile, a steel band round it, not hinged" in text
    assert "a steel band round it carrying the lid's hinge" in text


def test_a_top_loader_loads_under_its_lid() -> None:
    """The lid is the flat roof, hinged on its band; the walls are all wall (no door)."""
    k = kiln()
    assert k.loading.type == "lid"
    assert k.door_wall is None
    assert k.door_kind == "hinged"
    front = parse_design(SOURCE.replace(LID, ""))
    assert front.door_wall == "front"  # a design without the lid keeps its front door


GAS = "heat:\n  gas:\n    supply:\n      type: cylinders\n      count: 4\nsite:"


@pytest.mark.parametrize(
    "text",
    [
        SOURCE.replace("  shape: round\n", ""),  # a box
        SOURCE.replace("type: flat", "type: dome\n  rise: 6 in"),  # no flat lid
        SOURCE[: SOURCE.index("heat:")] + GAS + SOURCE.split("site:", 1)[1],  # gas
    ],
)
def test_a_lid_only_on_a_round_electric_kiln_with_a_flat_roof(text: str) -> None:
    with pytest.raises(ValueError, match="a lid is laid out only on a round electric kiln"):
        parse_design(text)


def test_a_lid_takes_no_door_in_its_walls() -> None:
    roof = "  roof:\n    - material: ifb-k23\n      thickness: 3 in\n"
    door = "  door:\n    - material: ifb-k23\n      thickness: 3 in\n"
    with pytest.raises(ValueError, match=r"leave out loading\.opening and lining\.door"):
        parse_design(SOURCE.replace(roof, roof + door))


def test_the_lids_hardware_and_peepholes_in_the_wall() -> None:
    from kilndesigner.hardware import build_hardware

    k = kiln()
    hw = build_hardware(k, design_frame(k), None)
    text = " ".join(f.message for f in hw.findings)
    assert "loads from the top" in text
    assert "hinge" in text
    assert "handle" in text
    assert "aren't sized" in text
    assert "through the wall, as the kiln has no door" in text
    assert not [p for p in hw.pieces if p.name.startswith("door/")]
    spies = sorted((p for p in hw.ports if p.kind == "spy"), key=lambda p: p.up)
    # One in the middle of each 9 in section, between its two courses' grooves
    assert [p.up for p in spies] == pytest.approx([4.5, 13.5, 22.5])
    assert {p.wall for p in spies} == {"front"}


def test_peephole_heights() -> None:
    from kilndesigner.hardware import lid_peephole_heights

    assert lid_peephole_heights(27, 3) == pytest.approx([4.5, 13.5, 22.5])
    assert lid_peephole_heights(27, 1) == pytest.approx([13.5])
    assert lid_peephole_heights(22.5, 3) == pytest.approx([4.5, 13.5, 20.25])  # a short top
    assert lid_peephole_heights(9, 2) == pytest.approx([3, 6])  # more than sections: even
    assert lid_peephole_heights(27, 0) == []


def test_peepholes_placed_by_hand_on_a_top_loader() -> None:
    from kilndesigner.hardware import build_hardware

    placed = (
        SOURCE + "spy_holes:\n  places:\n    - wall: back\n      across: 0 in\n      up: 10 in\n"
    )
    k = parse_design(placed)
    hw = build_hardware(k, design_frame(k), None)
    assert any("where the design places them" in f.message for f in hw.findings)
    square = parse_design(SOURCE + "spy_holes:\n  port:\n    width: 1 in\n    height: 2 in\n")
    hw = build_hardware(square, design_frame(square), None)
    assert any("1 × 2 in, through the wall" in f.message for f in hw.findings)


def test_the_model_is_the_polygon_with_its_grooves() -> None:
    """The wall, floor and lid are the 12-sided polygon the masonry lays (its slabs out to the
    wall's outside corners), and the grooves run round the facets, one per course."""
    from kilndesigner.geometry import element_runs, hot_face_reach, lining_parts, polygon_fraction

    k = kiln()
    a = inside_apothem(28.075 * IN, 12)
    corner = (a + 3 * IN) / math.cos(math.pi / 12)
    parts = {p.name.split("/")[0]: p for p in lining_parts(k)}
    for name in ("floor", "wall", "roof"):
        assert parts[name].sides == 12
        assert max(r for r, _ in parts[name].revolve or ()) == pytest.approx(corner)
    floor = parts["floor"]
    assert floor.volume == pytest.approx(polygon_fraction(12) * math.pi * corner**2 * 3 * IN)
    wall = parts["wall"]
    ring = polygon_fraction(12) * math.pi * (corner**2 - (a / math.cos(math.pi / 12)) ** 2)
    assert wall.volume == pytest.approx(ring * 27 * IN)
    assert hot_face_reach(k, -math.pi / 2) == pytest.approx(a)  # a flat at the front
    assert hot_face_reach(k, -math.pi / 2 + math.pi / 12) == pytest.approx(
        a / math.cos(math.pi / 12)
    )
    runs = element_runs(k, 6, 10.0)
    assert len(runs) == 6
    assert [r.path[0][2] for r in runs] == pytest.approx([(i + 0.5) * 4.5 * IN for i in range(6)])
    path = runs[0].path
    # Every corner of the ring once, and the quarters' ends, closed round
    assert path[0] == pytest.approx(path[-1])
    assert len(path) == 13  # the quarters' ends, at ±45° and ±135°, fall on corners
    for x, y, _ in path:
        assert a - 1e-6 <= math.hypot(x, y) <= a / math.cos(math.pi / 12) + 1e-6


def test_grooves_in_some_quarters_and_round_a_circle() -> None:
    from kilndesigner.geometry import element_runs

    two = kiln(**{"walls: [left, right, back, front]": "walls: [left, right]"})
    (run,) = element_runs(two, 1, 10.0)
    assert all(abs(x) >= abs(y) - 1e-6 for x, y, _ in run.path)  # only the side quarters
    circle = kiln(**{"28.075 in": "30 in"})
    (run,) = element_runs(circle, 1, 10.0)
    r = 15 * IN
    assert all(math.hypot(x, y) == pytest.approx(r) for x, y, _ in run.path)
    assert len(run.path) == 4 * 12 + 1


def test_a_door_breaks_a_round_kilns_bands() -> None:
    """Where a round kiln has a door, its bands can't run round there: listed, not sized."""
    import yaml

    data = yaml.safe_load((EXAMPLE.parent / "olsen" / "breda-bottle.yaml").read_text("utf-8"))
    data["loading"] = {"opening": {"width": "24 in", "height": "30 in", "head": "lintel"}}
    domed = parse_design(yaml.safe_dump(data, allow_unicode=True))
    (band,) = [f for f in design_frame(domed).findings if "breaks the round wall" in f.message]
    assert "from 0 to 30 in up" in band.message
    assert "carries it across" in band.message
    assert "aren't sized" in band.message
    data["roof"] = {"type": "flat"}
    flat = parse_design(yaml.safe_dump(data, allow_unicode=True))
    (band,) = [f for f in design_frame(flat).findings if "breaks the round wall" in f.message]
    assert "carries it across" not in band.message


def test_the_section_cuts_the_grooves() -> None:
    from kilndesigner.drawings import section_views

    k = kiln()
    section, plan = section_views(k, element_rows=6, coil_mm=12)
    a = inside_apothem(28.075 * IN, 12)
    assert len(section.circles) == 12
    assert {round(abs(c.x), 6) for c in section.circles} == {round(a, 6)}
    _, _, x1, _ = section.bounds()
    assert x1 == pytest.approx(a + 3 * IN)  # a flat faces +x: the section is flat to flat
    xs = [x for r in plan.rects for x, _ in r.points]
    assert max(xs) == pytest.approx(a + 3 * IN)
    assert len(plan.rects[0].points) == 12
