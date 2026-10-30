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
    box = parse_design(SOURCE.replace("  shape: round\n", ""))
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
    domed = parse_design(SOURCE.replace("type: flat", "type: dome\n  rise: 6 in"))
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
