"""Openings: exit flues of any count and layout, flues between chambers, dampers and passive air,
several chimneys or one through the crown, vent holes, salt ports and vapour holes."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from kilndesigner.build import design_document
from kilndesigner.designfile import load_design
from kilndesigner.fire import design_fire
from kilndesigner.hardware import MM, Hardware, build_hardware, floor_and_roof_holes
from kilndesigner.masonry import plan_masonry
from kilndesigner.model import Holes, Kiln
from kilndesigner.openings import grid_places, wall_places
from kilndesigner.report import design_report
from kilndesigner.run_parts import flue_holes, flue_rows

ROOT = Path(__file__).parents[2]
EXAMPLES = ROOT / "examples"
TEMPLATES = ROOT / "core" / "src" / "kilndesigner" / "data" / "templates"
SQUARE_6 = {"width": "6 in", "height": "6 in"}


def _template(name: str) -> Kiln:
    return load_design(TEMPLATES / f"{name}.yaml")


def _with(kiln: Kiln, **changes: Any) -> Kiln:
    """The kiln with its draft's fields (or, for openings, the kiln's) changed, validated anew."""
    doc: dict[str, Any] = dict(design_document(kiln))
    openings = changes.pop("openings", None)
    if changes:
        doc["draft"] = {**doc["draft"], **changes}
    if openings is not None:
        doc["openings"] = openings
    return Kiln.model_validate(doc)


def _hardware(kiln: Kiln) -> Hardware:
    report = design_report(kiln)
    return build_hardware(kiln, report.frame, report.gas, report.fire)


def _round_trip(kiln: Kiln) -> None:
    assert Kiln.model_validate(design_document(kiln)) == kiln


# ---- Schema --------------------------------------------------------------------------------


def test_every_new_field_round_trips() -> None:
    kiln = _with(
        _template("wood-fast-fire"),
        flue_port=None,
        exits=[
            {"through": "floor", "count": 4, "port": SQUARE_6},
            {"through": "back", "port": {"diameter": "4 in"}, "places": [{"across": "3 in"}]},
        ],
        connection={"width": "9 in", "height": "7.5 in"},
        chimneys=2,
        damper={"port": {"width": "12 in", "height": "2.5 in"}, "up": "30 in"},
        passive_air={"width": "2.5 in", "height": "4 in"},
        between={"count": 3, "port": {"width": "9 in", "height": "12 in"}},
        openings={
            "vents": [{"through": "roof", "count": 2, "port": {"diameter": "2 in"}}],
            "salt_ports": [
                {"through": "left", "port": {"width": "2.5 in", "height": "2.5 in"},
                 "places": [{"across": "0 in", "up": "20 in"}]}
            ],
            "vapour_holes": [{"through": "roof", "port": {"diameter": "1 in"}}],
        },
    )  # fmt: skip
    _round_trip(kiln)
    assert kiln.draft is not None
    assert kiln.draft.chimneys == 2
    assert kiln.openings is not None
    assert [k for k, _ in kiln.openings.all()] == ["vent", "salt port", "vapour hole"]
    _round_trip(_with(_template("gas-crossdraft"), damper={"kind": "top"}, chimney_through="crown"))


def test_the_defaults_change_nothing() -> None:
    kiln = _template("wood-fast-fire")
    assert kiln.draft is not None
    assert kiln.draft.exits is None
    assert kiln.draft.chimneys == 1
    assert kiln.draft.chimney_through == "beside"
    assert kiln.draft.damper is None
    assert kiln.draft.passive_air is None
    assert kiln.draft.between is None
    assert kiln.openings is None
    doc: dict[str, Any] = dict(design_document(kiln))
    assert "exits" not in doc["draft"]


@pytest.mark.parametrize(
    ("changes", "says"),
    [
        ({"exits": [{"through": "back", "port": SQUARE_6}]}, "not both"),
        ({"flue_port": None, "chimneys": 2, "chimney_through": "crown"}, "one chimney"),
        ({"damper": {"kind": "top", "up": "3 ft"}}, "no slot"),
        (
            {"flue_port": None,
             "exits": [{"through": "back", "count": 2, "port": SQUARE_6, "places": [{}]}]},
            "a place for each",
        ),
        (
            {"flue_port": None,
             "exits": [{"through": "back", "port": SQUARE_6, "places": [{"along": "3 in"}]}]},
            "no along",
        ),
        (
            {"flue_port": None,
             "exits": [{"through": "floor", "port": SQUARE_6, "places": [{"up": "3 in"}]}]},
            "no up",
        ),
    ],
)  # fmt: skip
def test_a_hole_that_cant_be_built_is_refused(changes: dict[str, Any], says: str) -> None:
    with pytest.raises(ValidationError, match=says):
        _with(_template("wood-fast-fire"), **changes)


def test_holes_spread_evenly_when_not_placed() -> None:
    row = Holes.model_validate({"through": "back", "count": 4, "port": SQUARE_6})
    assert wall_places(row, 40) == [(-15, 3), (-5, 3), (5, 3), (15, 3)]
    grid = Holes.model_validate({"through": "floor", "count": 4, "port": SQUARE_6})
    assert grid_places(grid, 40, 40) == [(-10, -10), (10, -10), (-10, 10), (10, 10)]
    three = Holes.model_validate({"through": "roof", "count": 3, "port": SQUARE_6})
    assert grid_places(three, 40, 40) == [(-10, -10), (10, -10), (0, 10)]  # the last row centred
    assert three.total_in2() == 108


# ---- The flue area the rules use: the stated flues added up --------------------------------


def test_a_wood_kilns_flue_area_is_its_exit_flues_added_up() -> None:
    kiln = load_design(EXAMPLES / "olsen" / "singh-coal.yaml")
    fire = design_fire(kiln)
    assert fire.flue_area_in2 == pytest.approx(12 * 36)
    step = next(s for s in fire.working if s.name == "Exit flues as built, together")
    assert step.value == "432 in²"
    assert step.inputs["exit flues"] == "12 × 6 × 6 in (36.0 in²) in the floor"


def test_a_gas_kilns_exit_flues_are_checked_together_against_olsens_one_to_one() -> None:
    kiln = load_design(EXAMPLES / "olsen" / "kahler-salt.yaml")
    report = design_report(kiln)
    assert report.gas is not None
    step = next(s for s in report.gas.working if s.name == "Exit flues as built, together")
    assert step.value == "122 in²"  # 3 × 4½ × 9 in
    assert "1 : 1" in step.inputs["Olsen's starting size"]
    # Too small together: the check's working adds them up
    small = _with(
        kiln, exits=[{"through": "floor", "count": 2, "port": {"width": "2 in", "height": "2 in"}}]
    )
    hw = _hardware(small)
    found = next(f for f in hw.findings if f.check is not None and f.check.id == "hardware.flue")
    assert "exit flues together are 8 in²" in found.message
    assert found.check is not None
    assert any("n_1*a_1" in str(x) for x in found.check.model_dump().values())


def test_several_chimneys_as_built_add_up_for_the_grate() -> None:
    kiln = _template("wood-fast-fire")
    one = design_fire(kiln)
    two = design_fire(_with(kiln, chimneys=2))
    assert two.chimney_area_in2 == pytest.approx(2 * one.chimney_area_in2)
    assert any(s.name == "Chimneys' section together" for s in two.working)


# ---- Drawn: the 3D model's openings and pieces, and the brick count ------------------------


def test_floor_exit_flues_are_cut_through_the_floor() -> None:
    kiln = load_design(EXAMPLES / "olsen" / "singh-coal.yaml")
    hw = _hardware(kiln)
    exits = [o for o in hw.openings if o.name.startswith("port/exit-1-")]
    assert len(exits) == 12
    for o in exits:
        (x0, y0, _), (x1, y1, z1) = o.box
        assert (x1 - x0) / MM == pytest.approx(6)
        assert (y1 - y0) / MM == pytest.approx(6)
        assert z1 / MM == pytest.approx(1)  # through the floor, not into the chamber
        r = max(abs(x0), abs(x1)) ** 2 + max(abs(y0), abs(y1)) ** 2
        assert r**0.5 / MM < 42  # inside the round chamber
    assert "port/flue" not in {o.name for o in hw.openings}
    assert len(floor_and_roof_holes(hw)) >= 12
    duct = next(p for p in hw.pieces if p.name == "chimney/duct")
    assert "24 × 16 in inside" in duct.detail  # the connection to the chimney


def test_wall_exit_flues_are_placed_as_ports() -> None:
    kiln = load_design(EXAMPLES / "olsen" / "meaders-cheever.yaml")
    hw = _hardware(kiln)
    flues = [p for p in hw.ports if p.kind == "opening"]
    assert len(flues) == 6
    assert {(p.wall, p.width, p.height) for p in flues} == {("back", 5, 9)}
    assert not hw.refused


def test_a_wall_hole_that_doesnt_fit_is_refused_with_its_reason() -> None:
    kiln = _with(
        _template("wood-fast-fire"),
        flue_port=None,
        exits=[{"through": "back", "port": SQUARE_6, "places": [{"across": "200 in"}]}],
    )
    hw = _hardware(kiln)
    assert [p.name for p in hw.refused] == ["port/exit-1-1"]
    assert any(f.level == "error" and "Exit flue 1.1" in f.message for f in hw.findings)


def test_two_chimneys_stand_along_the_flue_wall_with_a_damper_on_each_top() -> None:
    kiln = load_design(EXAMPLES / "olsen" / "bae-gilgama.yaml")
    hw = _hardware(kiln)
    stacks = [p for p in hw.pieces if p.name.startswith("chimney/stack")]
    assert [p.name for p in stacks] == ["chimney/stack-1", "chimney/stack-2"]
    centres = [sum(lo[0] + hi[0] for lo, hi in p.boxes) / (2 * len(p.boxes)) / MM for p in stacks]
    assert centres == pytest.approx([12, -12], abs=0.5)  # spread along the 48 in back wall
    assert not any(o.name.startswith("port/damper") for o in hw.openings)
    assert any("slab laid over the chimney's top" in f.message for f in hw.findings)
    assert len([p for p in hw.ports if p.kind == "opening"]) == 2


def test_a_damper_slot_and_a_passive_air_hole_where_the_design_puts_them() -> None:
    kiln = load_design(EXAMPLES / "olsen" / "conrad-teardrop.yaml")
    hw = _hardware(kiln)
    slot = next(o for o in hw.openings if o.name == "port/damper")
    assert slot.box[0][2] / MM == pytest.approx(73)
    air = next(o for o in hw.openings if o.name == "port/passive-air")
    (_, _, z0), (_, _, z1) = air.box
    assert (z0 / MM, z1 / MM) == pytest.approx((0, 4))
    assert any("passive air hole, 2.5 × 4 in" in f.message for f in hw.findings)
    sized = _hardware(_with(kiln, damper={"port": {"width": "15 in", "height": "3 in"}}))
    assert any("15 in wide and 3 in high" in f.message for f in sized.findings)


def test_a_chimney_through_the_crown() -> None:
    kiln = load_design(EXAMPLES / "olsen" / "kahler-salt.yaml")
    hw = _hardware(kiln)
    stack = next(p for p in hw.pieces if p.name == "chimney/stack")
    assert stack.title == "Chimney through the crown"
    top = max(hi[2] for _, hi in stack.boxes) / MM
    assert top == pytest.approx(132)  # 11 ft
    flue = next(o for o in hw.openings if o.name == "port/flue")
    (x0, y0, _), (x1, y1, _) = flue.box
    assert ((x1 - x0) / MM, (y1 - y0) / MM) == pytest.approx((9, 7))
    assert hw.chimney_bricks > 0
    assert not any(p.name == "chimney/duct" for p in hw.pieces)


def test_vents_salt_ports_and_vapour_holes_are_cut() -> None:
    kiln = _with(
        _template("wood-fast-fire"),
        openings={
            "vents": [{"through": "roof", "count": 4, "port": {"diameter": "2 in"}}],
            "salt_ports": [{"through": "left", "count": 2, "port": {"width": "2.5 in",
                                                                     "height": "2.5 in"}}],
            "vapour_holes": [{"through": "roof", "port": {"diameter": "1 in"}}],
        },
    )  # fmt: skip
    hw = _hardware(kiln)
    names = {o.name for o in hw.openings}
    assert {f"port/vent-1-{k}" for k in range(1, 5)} <= names
    assert {"port/salt-1-1", "port/salt-1-2", "port/vapour-1-1"} <= names
    vent = next(o for o in hw.openings if o.name == "port/vent-1-1")
    assert vent.round_axis == 2
    assert {p.wall for p in hw.ports if p.name.startswith("port/salt-")} == {"left"}
    assert any("4 vents in the roof" in f.message for f in hw.findings)
    roof = [h for h in floor_and_roof_holes(hw) if h.lo[2] > 0]
    assert len(roof) >= 5


def test_an_updrafts_roof_exits_replace_its_one_flue() -> None:
    kiln = _template("gas-updraft")
    hw = _hardware(_with(kiln, flue_port=None, exits=[{"through": "roof", "count": 4,
                                                       "port": SQUARE_6}]))  # fmt: skip
    names = {o.name for o in hw.openings}
    assert "port/flue" not in names
    assert {f"port/exit-1-{k}" for k in range(1, 5)} <= names


# ---- Flues between chambers ----------------------------------------------------------------


def test_flues_between_chambers_by_count_and_size() -> None:
    kiln = _template("climbing")
    sized = _with(kiln, between={"count": 3, "port": {"width": "9 in", "height": "12 in"}})
    rows = flue_rows(sized)
    assert len(rows) == len(flue_rows(kiln))
    assert {r.count for r in rows} == {3}
    holes = [h for h in flue_holes(sized) if h.name.startswith("flue-1-")]
    assert len(holes) == 3
    assert {round((h.hi[0] - h.lo[0]) / MM, 6) for h in holes} == {9}
    width = kiln.chamber.width.to("inch").magnitude
    centres = [(h.lo[0] + h.hi[0]) / 2 / MM for h in holes]
    assert centres == pytest.approx([-width / 3, 0, width / 3])
    notes = " ".join(f.message for f in plan_masonry(sized).result.findings)
    assert "3 flue holes 9 in wide and 12 in tall" in notes
