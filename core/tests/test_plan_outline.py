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
from kilndesigner.outline import half_width, offset
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
    # Fitted to the printed widths (curved-kilns.md): 6 % under their area, 4206 in², the round
    # end putting the widest point further forward than the book draws it
    assert plan.area == pytest.approx(4206, rel=0.07)
    # The book's neck: 16 in a foot before it, then 12 in straight for its last 19 in
    assert 2 * half_width(plan, 86 - 117 / 2) == pytest.approx(16, abs=1)
    for y in (99, 110, 116.9):
        assert 2 * half_width(plan, y - 117 / 2) == pytest.approx(12)
    # The estimated crown, 45 in up, 53 in behind the front wall
    assert inside_top(kiln, "front", 0.0) / IN < 45
    report = design_report(kiln)
    assert [f for f in report.findings if f.level != "info"] == []
    assert report.chamber_volume == "97.4 ft³"  # 106 ft³ before the neck (2026-10-31)


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


def test_necks_it_refuses() -> None:
    d = data()
    del d["chamber"]["outline"]["neck_radius"]
    with pytest.raises(ValidationError, match="neck takes neck_width"):
        Kiln.model_validate(d)
    d = data()
    d["chamber"]["outline"] = {"shape": "oval", "end_radius": "12 in", "neck_width": "6 in"}
    with pytest.raises(ValidationError, match="end_radius only"):
        Kiln.model_validate(d)
    d = data()
    d["lining"]["walls"][0]["thickness"] = "40 in"
    with pytest.raises(ValidationError, match="walls can't follow"):
        Kiln.model_validate(d)
    d = data()
    d["roof"]["crown_at"] = "105 in"  # in the neck, where the reverse curves hide the walls
    d["roof"]["rise"] = "5 in"
    with pytest.raises(ValidationError, match="see the whole plan"):
        Kiln.model_validate(d)


def test_courses_round_the_curve() -> None:
    from kilndesigner.curve_masonry import curve_rings

    kiln = load_design(TEARDROP)
    rings = curve_rings(kiln, 0.0, 9.0)
    assert rings is not None
    assert [r.reach for r in rings] == [0.0, 4.5]
    inner = {r.kind: r for r in rings[0].runs}
    # The 39 in front: four whole straights and a 3 in closer
    fronts = [r for r in rings[0].runs if r.kind == "straight" and r.length == pytest.approx(39)]
    assert (fronts[0].whole, fronts[0].closer) == (4, pytest.approx(3))
    # The round end, radius 25¾ in: 9 in chords each turn 2·asin(4.5/25.75)
    theta = 2 * math.asin(4.5 / 25.75)
    convex = [r for r in rings[0].runs if r.kind == "convex"]
    assert max(r.joint for r in convex) == pytest.approx(2 * 4.5 * math.sin(theta / 2))
    assert inner["concave"].cut > 0
    assert not any(r.kind == "corner" for r in rings[0].runs)
    assert sum(r.kind == "corner" for r in rings[1].runs) == 4  # round the square corners
    assert curve_rings(kiln, 0.0, 7.0) is None  # not whole 4½ in rings
    masonry = plan_masonry(kiln).result
    found = next(f for f in masonry.findings if f.message.startswith("Courses round the curve"))
    assert "14 courses" in found.message
    assert "cut to the angle" in found.message


def test_the_door_head_as_drawn() -> None:
    from kilndesigner.door import door_head

    kiln = load_design(TEARDROP)
    head = door_head(kiln)
    assert head is not None
    assert "rounded to 1 in" in head.working[0].value
    assert any("isn't checked" in f.message for f in head.findings)
    hole = door_hole(kiln)
    assert hole is not None
    assert (hole.radius, hole.corner) == (0.0, IN)
    assert hole.hi[2] == pytest.approx(36 * IN)  # the box stops a corner's radius under the head
    d = data()
    d["loading"]["opening"].update(head="flat")
    del d["loading"]["opening"]["corner"]
    square = Kiln.model_validate(d)
    assert "flat, square" in (door_head(square) or head).working[0].value
    assert door_hole(square).hi[2] == pytest.approx(37 * IN)  # type: ignore[union-attr]
    for change_, why in (({"head": "arch"}, "corner is a flat head's"),
                         ({"corner": "20 in"}, "less than half")):  # fmt: skip
        d = data()
        d["loading"]["opening"].update(change_)
        with pytest.raises(ValidationError, match=why):
            Kiln.model_validate(d)
    d = data()
    d["loading"]["opening"].update(ring="4.5 in")
    with pytest.raises(ValidationError, match="or a flat head"):
        Kiln.model_validate(d)


@pytest.mark.geometry
def test_the_flat_heads_hole_in_the_model() -> None:
    from kilndesigner.door import model_door_holes

    holes = model_door_holes(load_design(TEARDROP))
    assert len(holes) == 4  # the box, the band between the corners, and a round in each
    band = holes[1]
    assert band[1][2] - band[0][2] == pytest.approx(IN)


def test_the_dome_sliced_over_the_curve() -> None:
    from kilndesigner.frame import design_frame as frame_design
    from kilndesigner.frame import dome_slices

    kiln = load_design(TEARDROP)
    slices = dome_slices(kiln)
    # Planes parallel to the right wall, across the 51½ in, each spanning front to back
    assert all(abs(s.at) <= 51.5 / 2 for s in slices)
    middle = min(slices, key=lambda s: abs(s.at))
    # Its farther springing: the back wall, 64 in behind the crown (53 in from the front of 117)
    assert middle.span == pytest.approx(2 * 64, abs=1)
    assert len({round(s.span) for s in slices}) > 2  # the chords change across the curve
    frame = frame_design(kiln)
    assert frame.thrust is not None
    assert "per foot of wall" in frame.thrust
    d = data()
    d["roof"]["buttressed"] = False
    with pytest.raises(ValidationError, match="held by masonry"):
        Kiln.model_validate(d)
    # A door in the back wall: the slices run across the kiln, either side of the crown
    d = data()
    d["loading"] = {"type": "door", "face": "back", "door": "bricked"}
    across = dome_slices(Kiln.model_validate(d))
    assert min(s.at for s in across) < 0 < max(s.at for s in across)
    assert max(s.span for s in across) <= 51.5 + 1e-6


def test_a_dome_crowned_in_the_middle_by_default() -> None:
    d = data()
    del d["roof"]["crown_at"]
    kiln = Kiln.model_validate(d)
    form = form_of(kiln)
    assert form.domes[0].centre == (0.0, 0.0)
    assert math.isfinite(chamber_shape(kiln).volume)
