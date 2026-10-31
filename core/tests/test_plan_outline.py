"""A curved plan (chamber.outline): Calimpong's teardrop under its cast dome, against the book
(Olsen, The Kiln Book, 4th ed. Fig 4-140), and the shapes the engine refuses."""

import math
from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from kilndesigner import load_design
from kilndesigner.door import door_hole
from kilndesigner.drawings import section_views
from kilndesigner.form import form_of, plan_of
from kilndesigner.geometry import inside_top, lining_parts, part_solid
from kilndesigner.masonry import plan_masonry
from kilndesigner.model import Kiln
from kilndesigner.outline import offset
from kilndesigner.report import design_report
from kilndesigner.shape import chamber_shape
from kilndesigner.units import si

TEARDROP = Path(__file__).parents[2] / "examples" / "olsen" / "conrad-teardrop.yaml"
IN = 25.4


def data() -> dict[str, Any]:
    return yaml.safe_load(TEARDROP.read_text(encoding="utf-8"))


def oval_kiln() -> Kiln:
    d = data()
    outline = {"shape": "oval", "end_radius": "12 in"}
    d["chamber"].update(width="40 in", depth="60 in", outline=outline)
    d["roof"] = {"type": "flat"}
    d["loading"] = {"type": "door", "face": "front", "door": "bricked",
                    "opening": {"width": "12 in", "height": "20 in"}}  # fmt: skip
    del d["heat"]["fire"]["fireboxes"][0]["width"]
    d["heat"]["fire"]["fireboxes"][0]["width"] = "12 in"
    return Kiln.model_validate(d)


def test_calimpongs_teardrop_against_the_book() -> None:
    kiln = load_design(TEARDROP)
    assert si(kiln.chamber.depth, "in") == pytest.approx(9 * 12 + 9)  # 9'9" inside
    door = kiln.loading.opening
    assert door is not None
    assert (si(door.width, "in"), si(door.height, "in")) == (33, 37)
    plan = plan_of(kiln, "in")
    x0, x1, y0, y1 = plan.bounds
    assert (y1 - y0, x1 - x0) == pytest.approx((117, 51.5), abs=0.05)
    # Fitted to the printed widths (curved-kilns.md): within 3 % of their area, 4206 in²
    assert plan.area == pytest.approx(4206, rel=0.03)
    # The estimated crown, 45 in up, 53 in behind the front wall
    assert inside_top(kiln, "front", 0.0) / IN < 45
    report = design_report(kiln)
    assert [f for f in report.findings if f.level != "info"] == []
    assert report.chamber_volume == "106 ft³"


def test_the_shape_comes_from_the_form() -> None:
    kiln = load_design(TEARDROP)
    shape, form = chamber_shape(kiln), form_of(kiln)
    assert shape.volume == form.volume
    faces = {f.face: f for f in shape.faces()}
    assert faces["floor"].inside_area == pytest.approx(form.plan.area)
    grown = offset(form.plan, 0.1)
    assert faces["floor"].area_at(0.1) == pytest.approx(grown.area)
    walls = sum(faces[w].inside_area for w in ("left", "right", "front", "back"))
    # The walls to the springline, and their band up to the dome
    assert walls > form.plan.perimeter * form.height
    assert faces["roof"].area_at(0.1) > faces["roof"].inside_area > form.plan.area
    flat = chamber_shape(oval_kiln())
    by_face = {f.face: f for f in flat.faces()}
    assert by_face["roof"].inside_area == pytest.approx(by_face["floor"].inside_area)
    assert sum(f.inside_area for f in flat.faces() if f.orientation == "vertical") == pytest.approx(
        form_of(oval_kiln()).plan.perimeter * si(oval_kiln().chamber.height, "m")
    )


def test_the_lining_follows_the_plan() -> None:
    kiln = load_design(TEARDROP)
    parts = {p.name: p for p in lining_parts(kiln)}
    plan = plan_of(kiln, "mm")
    wall = parts["walls/1-ifb-k26"]
    t, h = 9 * IN, 35 * IN
    # A ring between the plan and the plan moved out 9 in, drawn in chords: within 0.1 %
    assert wall.volume == pytest.approx((offset(plan, t).area - plan.area) * h, rel=1e-3)
    assert wall.thickness == pytest.approx(t)
    floor = parts["floor/1-ifb-k26"]
    assert floor.volume == pytest.approx(offset(plan, t).area * t, rel=1e-3)
    dome, cap = parts["roof/1-kast-o-lite-26-li-plus"], parts["walls/1-ifb-k26-dome"]
    assert dome.thickness == pytest.approx(5.5 * IN)
    # The dome's shell is about its area over the plan times its thickness
    assert 0.8 < dome.volume / (offset(plan, t).area * 5.5 * IN) < 1.3
    assert cap.volume > 0
    assert parts["walls/1-ifb-k26"].title == "Walls, layer 1 from the inside"
    # Curved parts aren't cut by the door or fireboxes: one wall part, no door part
    assert not any(n.startswith("door/") for n in parts)
    # The door's hole reaches the curve's inside face, inside the chamber's width
    hole = door_hole(kiln)
    assert hole is not None
    assert hole.lo[0] < si(kiln.chamber.width, "mm") / 2 - IN
    masonry = plan_masonry(kiln).result
    assert any("plan's curve" in f.message for f in masonry.findings)


def test_wall_tops_under_the_dome() -> None:
    kiln = load_design(TEARDROP)
    h = 35 * IN
    assert inside_top(kiln, "back", 0.0) == h  # the point: the springline
    assert inside_top(kiln, "front", 40 * IN) == h  # past the flat front
    assert inside_top(kiln, "front", 0.0) > h
    assert inside_top(kiln, "right", 0.0) > inside_top(kiln, "front", 0.0)
    flat = oval_kiln()
    assert inside_top(flat, "left", 0.0) == si(flat.chamber.height, "mm")


def test_sections_of_a_curved_plan() -> None:
    front, side, plan = section_views(load_design(TEARDROP))
    names = {r.layer for r in plan.rects}
    assert "walls/1-ifb-k26" in names
    walls = [r for r in front.rects if r.layer == "walls/1-ifb-k26"]
    assert len(walls) == 2  # either side
    assert any(r.layer == "roof/1-kast-o-lite-26-li-plus" and r.points for r in side.rects)
    flat = section_views(oval_kiln())
    assert any(r.layer.startswith("roof/") for r in flat[0].rects)
    assert not any(r.layer.startswith("roof/") for r in flat[2].rects)


@pytest.mark.geometry
def test_the_solids_hold_the_parts_volumes() -> None:
    kiln = load_design(TEARDROP)
    for p in lining_parts(kiln):
        if p.plan is None:
            continue
        solid = part_solid(p)
        assert solid is not None
        assert solid.volume == pytest.approx(p.volume, rel=0.01), p.name
    for p in lining_parts(oval_kiln()):
        if p.plan is not None and p.name.startswith("roof/"):
            solid = part_solid(p)
            assert solid is not None
            assert solid.volume == pytest.approx(p.volume, rel=1e-3)


def change(**chamber: Any) -> dict[str, Any]:
    d = data()
    d["chamber"].update(chamber)
    return d


@pytest.mark.parametrize(
    ("design", "why"),
    [
        (change(shape="round", depth="51.5 in"), "one level, straight chamber"),
        (change(chambers=2), "one level, straight chamber"),
        (change(outline={"shape": "teardrop", "front_width": "60 in"}), "can't be drawn"),
        (change(outline={"shape": "teardrop", "side_radius": "100 in"}), "larger than"),
        (change(outline={"shape": "oval"}), "end_radius only"),
        (change(outline={"shape": "teardrop", "end_radius": "5 in"}), "not end_radius"),
    ],
)
def test_plans_it_refuses(design: dict[str, Any], why: str) -> None:
    with pytest.raises(ValidationError, match=why):
        Kiln.model_validate(design)


def test_roofs_and_heat_it_refuses() -> None:
    d = data()
    d["roof"] = {"type": "sprung_arch", "rise": "8 in"}
    d["loading"] = {"type": "door", "face": "front"}
    with pytest.raises(ValidationError, match="arch or vault over a teardrop"):
        Kiln.model_validate(d)
    d = data()
    d["roof"]["crown_at"] = "200 in"
    with pytest.raises(ValidationError, match="stand over the plan"):
        Kiln.model_validate(d)
    d = data()
    d["roof"]["rise"] = "80 in"
    with pytest.raises(ValidationError, match="farthest reach"):
        Kiln.model_validate(d)
    d = data()
    del d["chamber"]["outline"]
    with pytest.raises(ValidationError, match="crown_at is for a curved plan"):
        Kiln.model_validate(d)
    d = data()
    d["heat"] = {"electric": {"supply": {"voltage": "240 V", "breaker": "50 A"}}}
    d["draft"] = None
    d["loading"] = {"type": "door", "face": "front"}
    with pytest.raises(ValidationError, match="elements are laid out along straight walls"):
        Kiln.model_validate(d)


def test_a_dome_crowned_in_the_middle_by_default() -> None:
    d = data()
    del d["roof"]["crown_at"]
    kiln = Kiln.model_validate(d)
    form = form_of(kiln)
    assert form.domes[0].centre == (0.0, 0.0)
    assert math.isfinite(chamber_shape(kiln).volume)
