"""Round kilns drawn and planned: lining parts turned about the axis, sections, course plans for
each ring, floor and roof, plans and a model."""

import json
import math
from pathlib import Path

import pytest

from kilndesigner.designfile import load_design, parse_design
from kilndesigner.drawings import ring_plan_svg, section_views, view_svg
from kilndesigner.geometry import lining_parts, not_drawn, write_model
from kilndesigner.masonry import plan_masonry
from kilndesigner.model import Kiln
from kilndesigner.plans import build_plans
from kilndesigner.report import design_report
from kilndesigner.round_masonry import RingPlan, cap_volume
from kilndesigner.shape import RoundDome

ROOT = Path(__file__).parents[2]
TEMPLATES = ROOT / "core" / "src" / "kilndesigner" / "data" / "templates"
ROUND = sorted(
    p
    for p in [*(ROOT / "examples").rglob("*.yaml"), *TEMPLATES.glob("*.yaml")]
    if "shape: round" in p.read_text(encoding="utf-8")
)
IN = 25.4

SMALL = """\
schema: 1
name: Round test kiln
units: us
firing: {cone: "6"}
chamber: {shape: round, width: 60 in, depth: 60 in, height: 36 in}
roof: {type: dome, rise: 15 in}
lining:
  walls:
    - {material: ifb-jm26, thickness: 4.5 in}
    - {material: firebrick-medium-duty-smithfield, thickness: 9 in}
  floor:
    - {material: firebrick-medium-duty-smithfield, thickness: 4.5 in}
  roof:
    - {material: firebrick-medium-duty-smithfield, thickness: 4.5 in}
heat:
  fire:
    fuel: wood
    fireboxes:
      - {position: under, width: 18 in, length: 30 in}
draft: {type: up}
"""


def _small(roof: str | None = None) -> Kiln:
    text = SMALL if roof is None else SMALL.replace("roof: {type: dome, rise: 15 in}", roof)
    return parse_design(text)


def test_the_round_examples_are_found() -> None:
    names = {p.stem for p in ROUND}
    assert {"breda-bottle", "kenzan-muffle", "ninodaguia", "singh-coal", "round-open-top"} <= names


def test_a_round_kiln_is_drawn() -> None:
    for path in ROUND:
        assert not_drawn(load_design(path)) is None, path


def test_round_parts_are_rings_discs_and_dome_layers_of_the_right_volume() -> None:
    kiln = _small()
    parts = {p.name: p for p in lining_parts(kiln)}
    r, h = 30 * IN, 36 * IN
    wall1, wall2 = parts["wall/1-ifb-jm26"], parts["wall/2-firebrick-medium-duty-smithfield"]
    assert wall1.volume == pytest.approx(math.pi * ((r + 4.5 * IN) ** 2 - r**2) * h)
    assert wall2.thickness == pytest.approx(9 * IN)
    assert wall1.title == "Round wall, layer 1 from the inside"
    # The wall's area at mid-thickness, as round_masonry counts sheet
    assert wall1.area == pytest.approx(2 * math.pi * (r + 2.25 * IN) * h)
    outside = r + 13.5 * IN
    floor = parts["floor/1-firebrick-medium-duty-smithfield"]
    assert floor.volume == pytest.approx(math.pi * outside**2 * 4.5 * IN)
    assert floor.hi[2] == 0.0
    dome = RoundDome(2 * r, 15 * IN)
    below = dome.radius - dome.rise
    expected = cap_volume(dome.radius + 4.5 * IN, below) - cap_volume(dome.radius, below)
    roof = parts["roof/1-firebrick-medium-duty-smithfield"]
    assert roof.volume == pytest.approx(expected, rel=2e-3)
    assert roof.lo[2] == pytest.approx(h)


def test_a_flat_roof_is_a_disc_on_the_wall_and_an_open_top_has_none() -> None:
    flat = {p.name: p for p in lining_parts(_small("roof: {type: flat}"))}
    roof = flat["roof/1-firebrick-medium-duty-smithfield"]
    assert roof.lo[2] == pytest.approx(36 * IN)
    assert roof.hi[0] == pytest.approx(30 * IN + 13.5 * IN)
    open_ = lining_parts(_small("roof: {type: open}"))
    assert not [p for p in open_ if p.wall == "roof"]


def test_the_sections_cut_through_the_axis_and_across_it() -> None:
    section, plan = section_views(_small())
    walls = [r for r in section.rects if r.layer.startswith("wall/")]
    assert len(walls) == 4  # each ring, on both sides of the axis
    floor = [r for r in section.rects if r.layer.startswith("floor/")]
    assert len(floor) == 1  # one piece, joined across the axis
    assert floor[0].w == pytest.approx(2 * (30 + 13.5) * IN)
    rings = [r for r in plan.rects if r.layer.startswith("wall/")]
    assert len(rings) == 2
    assert all(len(r.holes) == 1 for r in rings)
    assert rings[0].w == pytest.approx(2 * 34.5 * IN, rel=1e-3)
    svg = view_svg(plan)
    assert 'fill-rule="evenodd"' in svg
    assert any("across inside" in d.text for d in plan.dims)


def test_each_ring_has_a_plan_of_its_bricks() -> None:
    masonry = plan_masonry(_small())
    rings = masonry.rings
    assert [r.series for r in rings] == ["arch", "key"]
    arch, key = rings
    assert arch.courses == 4  # 36 in of 9 in courses
    assert not arch.ripped
    assert key.courses == math.ceil(36 / 2.5)
    assert key.ripped
    assert key.top == pytest.approx(36 * IN - 14 * 2.5 * IN)
    assert len(key.order()) == key.ring.total
    assert "arch bricks standing on end" in arch.description(True)
    assert "circle bricks" in arch.description(True)
    assert "key bricks laid flat" in key.description(True)
    svg = ring_plan_svg(key, True)
    assert svg.count("<polygon") == 2 * key.ring.total
    assert "Even courses" in svg
    # Floor first, then the wall's rings, then the roof (a dome: counted by volume, no plan)
    order = [p for p in masonry.course_plans() if not p.part.name.startswith("firebox-")]
    assert order[0].part.wall == "floor"
    assert all(isinstance(p, RingPlan) for p in order[1:])
    # The fireboxes' walls come last
    assert all(p.part.name.startswith("firebox-") for p in masonry.course_plans()[len(order) :])


def test_a_round_floor_is_laid_in_rows_cut_to_the_circle() -> None:
    masonry = plan_masonry(_small("roof: {type: flat}"))
    floor, roof = [p for p in masonry.layers if not p.part.name.startswith("firebox-")]
    radius = (30 + 13.5) * IN
    assert floor.circle == pytest.approx(radius)
    assert floor.span == pytest.approx(2 * radius)
    for course in floor.courses:
        for piece in course.pieces:
            assert piece.start >= -0.01
            assert piece.start + piece.length <= 2 * radius + 0.01
    assert roof.part.wall == "roof"


@pytest.mark.parametrize("path", ROUND, ids=lambda p: p.stem)
def test_every_round_example_builds_plans(path: Path, tmp_path: Path) -> None:
    kiln = load_design(path)
    plans = build_plans(kiln, design_report(kiln), dxf_path=tmp_path / "s.dxf")
    assert plans.pdf.startswith(b"%PDF")
    assert (tmp_path / "s.dxf").stat().st_size > 1000
    kinds = [d.kind for d in plans.drawings]
    assert kinds.count("section") == 2
    assert kinds.count("course plan") == len(plans.masonry.course_plans())
    # What it takes is counted, or a layer whole bricks can't make is reported (Kenzan's 4 in)
    failed = [f for f in plans.masonry.result.findings if f.check is not None]
    assert plans.bom.lines or failed


@pytest.mark.geometry
@pytest.mark.parametrize("path", ROUND, ids=lambda p: p.stem)
def test_every_round_example_builds_a_model_of_its_layers(path: Path, tmp_path: Path) -> None:
    kiln = load_design(path)
    written = write_model(kiln, design_report(kiln), tmp_path)
    assert written["gltf"].stat().st_size > 1000
    parts = json.loads(written["parts"].read_text(encoding="utf-8"))
    assert any(name.startswith("wall/") for name in parts)
    assert any(name.startswith("floor/") for name in parts)
    assert all(not name.startswith("shell/") for name in parts)
    layout = json.loads(written["layout"].read_text(encoding="utf-8"))
    assert layout["run"]["round"] is True
