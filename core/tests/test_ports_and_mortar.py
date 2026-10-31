"""Floor burner ports and a roof flue taken out of the brick count; a mortar ring's wedge-joint
mortar on the bill of materials."""

from __future__ import annotations

import math
from pathlib import Path

from kilndesigner.designfile import load_design, parse_design
from kilndesigner.geometry import Part
from kilndesigner.masonry import Hole, plan_layer, plan_masonry, port_findings, punch
from kilndesigner.report import design_report
from kilndesigner.round_masonry import WEDGE_MORTAR, wedge_mortar

ROOT = Path(__file__).parents[2]
IN = 25.4
ROUND = """
schema: 1
name: Round test kiln
units: %s
firing: {cone: "6"}
chamber: {shape: round, width: 60 in, depth: 60 in, height: 36 in}
roof: {type: flat}
lining:
  walls: [{material: firebrick-medium-duty-smithfield, thickness: 4.5 in}]
heat:
  fire:
    fuel: wood
    fireboxes: [{position: under, width: 24 in, length: 48 in, height: 24 in}]
draft: {type: up}
"""


def _floor(width: float = 36 * IN, depth: float = 27 * IN) -> Part:
    """A floor of bricks laid flat, 2½ in thick."""
    return Part("floor/1-x", "x", "insulating_firebrick", (0, 0, -2.5 * IN), (width, depth, 0))


def test_a_brick_wholly_inside_a_hole_is_taken_out() -> None:
    plan = plan_layer(_floor())
    assert plan is not None
    before = len(plan.pieces)
    # 9 × 4½ in bricks in rows from the front: an 18 × 9 in hole at the corner holds 4 of them
    hole = Hole((-1, -1, -10 * IN), (18 * IN + 0.5, 9 * IN + 0.5, 1))
    # Two whole bricks in the first row; the second starts with a half brick, then a whole one
    assert punch(plan, [hole]) == 4
    assert len(plan.pieces) == before - 4


def test_a_hole_missing_the_layer_takes_nothing() -> None:
    plan = plan_layer(_floor())
    assert plan is not None
    above = Hole((0, 0, 100.0), (500.0, 500.0, 200.0))
    assert punch(plan, [above]) == 0


def test_a_round_hole_takes_only_bricks_inside_its_circle() -> None:
    hole = Hole((0, 0, 0), (100.0, 100.0, 10.0), round=True)
    assert hole.holds(30, 70, 30, 70)
    assert not hole.holds(0, 100, 0, 100)  # the box's corners are outside the circle
    part = Part("floor/1-x", "x", "k", (0, 0, 0), (200.0, 200.0, 10.0))
    assert math.isclose(hole.through(part), math.pi / 4 * 100 * 100 * 10)


def test_a_flat_roof_flue_comes_out_of_the_count() -> None:
    kiln = load_design(ROOT / "examples" / "electric-front-loader.yaml")
    top = max(p.part.hi[2] for p in plan_masonry(kiln).layers if p.part.wall == "roof")
    flue = Hole((-6 * IN, -6 * IN, 0.0), (6 * IN, 6 * IN, top + 1))

    def bricks(holes: list[Hole]) -> int:
        return sum(int(q.amount) for q in plan_masonry(kiln, holes).result.quantities
                   if q.unit == "bricks")  # fmt: skip

    assert bricks([flue]) < bricks([])


def test_the_note_says_how_the_holes_are_counted() -> None:
    kiln = load_design(ROOT / "core/src/kilndesigner/data/templates/gas-updraft.yaml")
    report = design_report(kiln)
    [note] = [f for f in report.findings if "cut in the 3D model" in f.message]
    assert "taken out of the count" in note.message
    part = _floor()
    [placed] = port_findings(kiln, True, [(part, 2)], ["Floor, layer 2"], {"Roof, layer 1"})
    assert "2 from floor" in placed.message
    assert "Floor, layer 2: counted less the holes' volume" in placed.message
    assert "The flue goes through the curved roof (Roof, layer 1)" in placed.message


def test_a_mortar_ring_puts_its_mortar_on_the_bill() -> None:
    text = ROUND % "us"
    plan = plan_masonry(parse_design(text))
    [mortar] = [q for q in plan.result.quantities if q.material == WEDGE_MORTAR]
    assert mortar.unit == "ft³"
    assert mortar.amount > 0
    assert "by volume only" in mortar.detail
    [step] = [s for s in plan.result.working if s.name == "Mortar in the rings' wedge joints"]
    assert "p.295" in (step.note or "")
    report = design_report(parse_design(text))
    assert report.bom is not None
    [line] = [x for x in report.bom.lines if "wedge joints" in x.item]
    assert line.cost is None


def test_a_metric_mortar_ring_is_in_litres_and_none_without_mortar_rings() -> None:
    plan = plan_masonry(parse_design(ROUND % "metric"))
    assert wedge_mortar(plan.rings, 914.4, us=False) is not None
    [mortar] = [q for q in plan.result.quantities if q.material == WEDGE_MORTAR]
    assert mortar.unit == "L"
    assert wedge_mortar([], 914.4, us=True) is None
