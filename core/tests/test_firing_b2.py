"""The firing fields of B2 (docs/planning/11-09-26.md): fireboxes on the diagonals, an under-floor
firebox's mouth and inlets, Roman and sloped firebox roofs, the stoke hole's sill, coal pits,
floor burners by side and end, burners firing into a firebox, and spy and stoke holes placed one
by one."""

import math
from pathlib import Path
from typing import Any

import pytest
from pydantic import ValidationError

from kilndesigner.designfile import load_design
from kilndesigner.firebox_parts import (
    firebox_boxes,
    firebox_findings,
    gas_burner_pieces,
    openings,
    roof_fill_parts,
)
from kilndesigner.firing_holes import floor_burner_xy
from kilndesigner.geometry import lining_parts
from kilndesigner.hardware import Faces, Hardware, build_hardware
from kilndesigner.masonry import plan_masonry
from kilndesigner.model import Burners, Kiln
from kilndesigner.report import design_report
from kilndesigner.units import Q_

ROOT = Path(__file__).parents[2]
TEMPLATES = ROOT / "core" / "src" / "kilndesigner" / "data" / "templates"
EXAMPLES = ROOT / "examples" / "olsen"
IN = 25.4


def _data(name: str) -> dict[str, Any]:
    return load_design(TEMPLATES / f"{name}.yaml").model_dump(mode="json", by_alias=True)


def _fast_fire(**firebox: Any) -> Kiln:
    data = _data("wood-fast-fire")
    for fb in data["heat"]["fire"]["fireboxes"]:
        fb.update(firebox)
    return Kiln.model_validate(data)


def _groundhog(**firebox: Any) -> Kiln:
    data = _data("groundhog")
    data["heat"]["fire"]["fireboxes"][0].update(firebox)
    return Kiln.model_validate(data)


def _hardware(kiln: Kiln) -> Hardware:
    report = design_report(kiln)
    return build_hardware(kiln, report.frame, report.gas, report.fire)


# --- Fireboxes on the diagonals -----------------------------------------------------------------


def test_a_round_kilns_diagonal_fireboxes_stand_on_its_45_degree_lines() -> None:
    kiln = load_design(EXAMPLES / "singh-coal.yaml")
    boxes = firebox_boxes(kiln)
    assert [b.box.position for b in boxes] == ["front-left", "front-right", "back-left",
                                               "back-right"]  # fmt: skip
    r = kiln.chamber.width.to("mm").magnitude / 2
    for b in boxes:
        middle = (b.lo[0] + b.hi[0]) / 2
        assert abs(middle) == pytest.approx(r * math.sqrt(0.5))
        assert (middle < 0) == b.box.position.endswith("left")
        assert (b.kiln_side == "+y") == b.box.position.startswith("front")
    message = firebox_findings(kiln)[0].message
    assert "on the front-left diagonal, drawn against the front wall" in message
    assert "a coal pit outside its mouth, 24 in across and 48 in out, its depth not" in message
    names = [p.name for p in lining_parts(kiln)]
    assert len(names) == len(set(names))


def test_a_box_kilns_diagonal_firebox_goes_into_its_corner() -> None:
    kiln = _groundhog(position="back-right")
    (b,) = firebox_boxes(kiln)
    half = kiln.chamber.width.to("mm").magnitude / 2
    assert b.hi[0] == pytest.approx(half)  # its side flush with the side wall's inside
    assert b.kiln_side == "-y"
    assert any(o.name == "firebox-1/mouth" or o.name.endswith("/inlet") for o in openings(kiln))


def test_a_diagonal_firebox_stands_alone() -> None:
    with pytest.raises(ValidationError, match="stands alone at its corner"):
        _groundhog(position="front-left", count=2)


# --- An under-floor firebox's mouth and inlets --------------------------------------------------


def test_an_under_floor_firebox_fed_from_the_back_has_its_inlet_at_the_front() -> None:
    front = _fast_fire()
    back = _fast_fire(mouth="back")
    a, b = firebox_boxes(front)[0], firebox_boxes(back)[0]
    assert (a.mouth, b.mouth) == ("-y", "+y")
    inlet_a = next(o for o in openings(front) if o.name == "firebox-1/inlet")
    inlet_b = next(o for o in openings(back) if o.name == "firebox-1/inlet")
    assert inlet_a.hi[1] == pytest.approx(a.hi[1])
    assert inlet_b.lo[1] == pytest.approx(b.lo[1])
    assert "fed from the back of the run" in firebox_findings(back)[0].message


def test_inlets_spread_over_the_floor_run_down_the_middle() -> None:
    kiln = _fast_fire(inlets_at="spread", inlets=3, inlet={"width": "4.5 in", "height": "4.5 in"})
    b = firebox_boxes(kiln)[0]
    inlets = [o for o in openings(kiln) if o.name == "firebox-1/inlet"]
    assert len(inlets) == 3
    share = (b.hi[1] - b.lo[1]) / 3
    for i, o in enumerate(inlets):
        assert (o.lo[1] + o.hi[1]) / 2 == pytest.approx(b.lo[1] + share * (i + 0.5))
        assert (o.lo[0] + o.hi[0]) / 2 == pytest.approx((b.lo[0] + b.hi[0]) / 2)
    assert "3 inlet flues spread evenly along it" in firebox_findings(kiln)[0].message


def test_round_inlets_spread_over_the_floor_stay_round() -> None:
    kiln = _fast_fire(inlets_at="spread", inlets=2, inlet={"diameter": "3 in"})
    assert all(o.round for o in openings(kiln) if o.name.endswith("/inlet"))


@pytest.mark.parametrize(
    ("change", "match"),
    [
        ({"mouth": "back"}, "for a firebox under the floor"),
        ({"inlets_at": "spread"}, "for a firebox under the floor"),
    ],
)
def test_mouth_and_inlets_at_are_for_under_floor_fireboxes(
    change: dict[str, str], match: str
) -> None:
    with pytest.raises(ValidationError, match=match):
        _groundhog(**change)


def test_spread_inlets_need_their_size() -> None:
    with pytest.raises(ValidationError, match="need their size"):
        _fast_fire(inlets_at="spread", inlet=None)


# --- Roman and sloped roofs ---------------------------------------------------------------------


def test_a_roman_firebox_roof_fills_the_haunches_over_a_semicircle() -> None:
    kiln = load_design(EXAMPLES / "phoenix-nh.yaml")
    (b,) = firebox_boxes(kiln)
    parts = roof_fill_parts(kiln, b)
    assert len(parts) == 2
    w = b.hi[0] - b.lo[0]
    r, run = w / 2, b.hi[1] - b.lo[1]
    exact = (w * r - math.pi * r * r / 2) * run
    assert sum(p.volume for p in parts) == pytest.approx(exact, rel=0.01)
    assert all(p.name in [q.name for q in lining_parts(kiln)] for p in parts)
    message = firebox_findings(kiln)[0].message
    assert "roofed with a Roman (semicircular) arch" in message
    arches = [f.message for f in plan_masonry(kiln).result.findings if "Arch bricks" in f.message]
    assert "Firebox 1, roof, layer 1 from the inside: about" in arches[0]


def test_a_roman_roof_on_a_wall_firebox_runs_the_other_way() -> None:
    data = _data("coal")
    data["heat"]["fire"]["fireboxes"][0].update(roof="roman", height="40 in")
    kiln = Kiln.model_validate(data)
    b = firebox_boxes(kiln)[0]
    assert not b.along_y
    parts = roof_fill_parts(kiln, b)
    assert parts
    assert all(p.across for p in parts)


def test_a_roman_roof_too_wide_for_its_height_is_drawn_flat() -> None:
    kiln = load_design(EXAMPLES / "phoenix-wright.yaml")
    (b,) = firebox_boxes(kiln)
    assert roof_fill_parts(kiln, b) == []
    assert "its roman roof refused and drawn flat" in firebox_findings(kiln)[0].message


def test_a_sloped_roof_is_a_wedge_deepest_at_the_mouth() -> None:
    kiln = _groundhog(roof="sloped", roof_slope="10 degree")
    (b,) = firebox_boxes(kiln)
    (wedge,) = roof_fill_parts(kiln, b)
    run = b.hi[1] - b.lo[1]
    drop = run * math.tan(math.radians(10))
    assert wedge.volume == pytest.approx(0.5 * run * drop * (b.hi[0] - b.lo[0]))
    assert wedge.across
    # Deepest at the mouth: the front firebox's outer end, y0
    deepest = min(z for _, z in wedge.profile or ())
    assert [y for y, z in wedge.profile or () if z == deepest] == [pytest.approx(b.lo[1])]
    assert "sloping up 10° from the mouth" in firebox_findings(kiln)[0].message


def test_a_sloped_roof_on_a_side_firebox_runs_along_x() -> None:
    data = _data("coal")
    data["heat"]["fire"]["fireboxes"][0].update(roof="sloped", roof_slope="5 degree")
    kiln = Kiln.model_validate(data)
    (wedge, *_) = roof_fill_parts(kiln, firebox_boxes(kiln)[0])
    assert not wedge.across


def test_a_slope_too_steep_for_the_firebox_is_drawn_flat() -> None:
    kiln = _groundhog(roof="sloped", roof_slope="55 degree")
    assert roof_fill_parts(kiln, firebox_boxes(kiln)[0]) == []
    assert "its sloped roof refused and drawn flat" in firebox_findings(kiln)[0].message


@pytest.mark.parametrize(
    ("change", "match"),
    [
        ({"roof": "sloped"}, "takes its roof_slope"),
        ({"roof_slope": "10 degree"}, "takes its roof_slope"),
        ({"roof": "sloped", "roof_slope": "20 percent"}, "as an angle"),
        ({"roof": "sloped", "roof_slope": "70 degree"}, "under 60 degrees"),
    ],
)
def test_a_sloped_roof_needs_a_slope_it_can_have(change: dict[str, str], match: str) -> None:
    with pytest.raises(ValidationError, match=match):
        _groundhog(**change)


def test_an_under_floor_firebox_has_no_roof_to_slope() -> None:
    with pytest.raises(ValidationError, match="no roof of its own to slope"):
        _fast_fire(roof="sloped", roof_slope="10 degree")


# --- The stoke hole's sill and the coal pit ------------------------------------------------------


def test_a_sill_raises_the_stoke_holes_foot_above_the_grate() -> None:
    kiln = load_design(EXAMPLES / "miravet.yaml")
    (b,) = firebox_boxes(kiln)
    hole = next(o for o in openings(kiln) if o.name == "firebox-1/stoke-hole")
    assert hole.lo[2] == pytest.approx(b.grate_z + 36 * IN)
    message = firebox_findings(kiln)[0].message
    assert "its stoke hole's sill 36 in above the firebox floor" in message


def test_a_sill_above_the_firebox_cuts_no_stoke_hole() -> None:
    kiln = _groundhog(sill="200 in", stoke_hole={"width": "9 in", "height": "9 in"})
    assert not [o for o in openings(kiln) if o.name.endswith("/stoke-hole")]


@pytest.mark.parametrize(
    ("change", "match"),
    [
        ({"sill": "10 in", "stoke_hole": None}, "give the stoke_hole"),
        ({"sill": "-1 in", "stoke_hole": {"width": "9 in", "height": "9 in"}}, "below the grate"),
    ],
)
def test_a_sill_is_a_stoke_holes(change: dict[str, Any], match: str) -> None:
    with pytest.raises(ValidationError, match=match):
        _groundhog(**change)


def test_a_coal_pit_is_dug_outside_a_wall_fireboxs_mouth() -> None:
    kiln = _groundhog(coal_pit={"width": "24 in", "length": "48 in", "depth": "30 in"})
    assert "48 in out, 30 in deep, dug, not built" in firebox_findings(kiln)[0].message
    with pytest.raises(ValidationError, match="dug outside a firebox's mouth in a wall"):
        _fast_fire(coal_pit={"width": "24 in", "length": "48 in"})
    with pytest.raises(ValidationError, match="more than zero"):
        _groundhog(coal_pit={"width": "0 in", "length": "48 in"})


# --- Floor burners by side and end ---------------------------------------------------------------


def _updraft(**burners: Any) -> Kiln:
    data = _data("gas-updraft")
    data["heat"]["gas"]["burners"].update(burners)
    return Kiln.model_validate(data)


def _floor_ports(kiln: Kiln) -> list[tuple[float, float]]:
    hw = _hardware(kiln)
    return [
        ((o.box[0][0] + o.box[1][0]) / 2 / IN, (o.box[0][1] + o.box[1][1]) / 2 / IN)
        for o in hw.openings
        if o.name.startswith("port/burner-")
    ]


def test_floor_burners_by_side_and_end() -> None:
    kiln = load_design(EXAMPLES / "kaneko-car.yaml")
    ports = _floor_ports(kiln)
    assert len(ports) == 32
    w = kiln.chamber.width.to("in").magnitude
    sides = [p for p in ports if abs(abs(p[0]) - (w / 2 - 2.5)) < 1e-6]
    assert len(sides) == 20
    hw = _hardware(kiln)
    assert any("10 along each side and 6 along each end" in f.message for f in hw.findings)


def test_floor_burners_set_in_from_the_corners() -> None:
    kiln = _updraft(count=None, per_side=3, per_end=2, corner_offset="9 in")
    ports = _floor_ports(kiln)
    assert len(ports) == 10
    d = kiln.chamber.depth.to("in").magnitude
    left = sorted(y for x, y in ports if x < -10)
    assert left[0] == pytest.approx(-d / 2 + 9)
    assert left[-1] == pytest.approx(d / 2 - 9)
    assert left[1] == pytest.approx(0.0)


def test_a_centre_pair_fires_up_the_middle_the_rest_round_the_edge() -> None:
    kiln = load_design(EXAMPLES / "olsen-kit-24.yaml")
    ports = _floor_ports(kiln)
    middle = [p for p in ports if abs(p[0]) < 1e-6 and abs(p[1]) < 10]
    assert len(middle) == 2
    assert len(ports) == 10


def test_floor_burner_layout_left_out_is_the_even_loop() -> None:
    assert floor_burner_xy(Burners(wall="floor", count=4), 30, 30, 4, 2.25) is None
    asked = Burners(wall="floor", per_side=1, per_end=0, corner_offset=Q_(5, "in"))
    one = floor_burner_xy(asked, 30, 30, 2, 2.25)
    assert one is not None
    assert one[0] == [(-12.75, 0.0), (12.75, 0.0)]


@pytest.mark.parametrize(
    ("burners", "match"),
    [
        ({"per_side": 2}, "together"),
        ({"per_side": 2, "per_end": 2, "count": 9}, "not the count's 9"),
        ({"centre": 13}, "more burners in the middle"),
        ({"wall": "front", "per_side": 1, "per_end": 1}, "give wall: floor"),
        ({"corner_offset": "0 in", "per_side": 3, "per_end": 3}, "more than zero"),
    ],
)
def test_floor_burner_layouts_it_refuses(burners: dict[str, Any], match: str) -> None:
    with pytest.raises(ValidationError, match=match):
        _updraft(**burners)


def test_a_corner_offset_needs_sides_and_room() -> None:
    with pytest.raises(ValidationError, match="give per_side"):
        _updraft(corner_offset="6 in", centre=2)
    with pytest.raises(ValidationError, match="less than half the shorter"):
        _updraft(count=None, per_side=2, per_end=2, corner_offset="20 in")


def test_the_burner_count_follows_from_sides_and_ends() -> None:
    assert Burners(wall="floor", per_side=10, per_end=6).wanted == 32
    assert Burners(wall="floor", per_side=1, per_end=1, centre=2).wanted == 6


# --- Gas burners firing into a firebox ------------------------------------------------------------


def _gas_firebox(**firebox: Any) -> Kiln:
    data = _data("gas-crossdraft")
    data["heat"]["gas"]["burners"].update(count=2, model="GACO MR750")
    data["heat"]["gas"]["firebox"] = {
        "position": "front", "width": "24 in", "length": "18 in", "height": "12 in",
        "inlet": {"width": "9 in", "height": "4.5 in"}, "inlets": 2, **firebox,
    }  # fmt: skip
    return Kiln.model_validate(data)


def test_burners_fire_into_a_firebox_through_its_mouth_wall() -> None:
    kiln = _gas_firebox()
    (b,) = firebox_boxes(kiln)
    assert b.gas
    ports = [o for o in openings(kiln) if "/burner-port-" in o.name]
    assert len(ports) == 2
    assert all(o.round for o in ports)
    assert all(o.hi[1] > b.lo[1] - 1 and o.lo[1] < b.lo[1] for o in ports)  # the mouth wall
    hw = _hardware(kiln)
    burners = [p for p in hw.pieces if p.name.startswith("burner/")]
    assert len(burners) == 2
    assert all(p.cylinders[0].centre[1] < b.lo[1] for p in burners)  # outside the mouth
    assert not [o for o in hw.openings if o.name.startswith("port/burner-")]
    assert "the burners' firebox" in firebox_findings(kiln)[0].message
    assert any(p.name.startswith("firebox-1/") for p in lining_parts(kiln))


def test_burners_that_dont_fit_across_the_mouth_arent_cut() -> None:
    kiln = _gas_firebox(width="6 in")
    assert not [o for o in openings(kiln) if "/burner-port-" in o.name]
    assert "burner ports aren't cut" in firebox_findings(kiln)[0].message


def test_burners_above_a_low_firebox_arent_cut() -> None:
    data = _gas_firebox().model_dump(mode="json", by_alias=True)
    data["heat"]["gas"]["burners"]["up"] = "30 in"
    assert not [o for o in openings(Kiln.model_validate(data)) if "/burner-port-" in o.name]


def test_burners_with_an_unknown_port_have_no_pieces_or_holes() -> None:
    data = _gas_firebox().model_dump(mode="json", by_alias=True)
    data["heat"]["gas"]["burners"]["model"] = "Ward 1"
    kiln = Kiln.model_validate(data)
    assert not [o for o in openings(kiln) if "/burner-port-" in o.name]
    assert gas_burner_pieces(kiln, None, "") == []


def test_a_burner_port_given_sets_the_firebox_ports() -> None:
    data = _gas_firebox().model_dump(mode="json", by_alias=True)
    data["heat"]["gas"]["burners"]["port"] = {"width": "4.5 in", "height": "5 in"}
    ports = [o for o in openings(Kiln.model_validate(data)) if "/burner-port-" in o.name]
    assert ports
    assert not any(o.round for o in ports)
    assert ports[0].hi[2] - ports[0].lo[2] == pytest.approx(5 * IN)


@pytest.mark.parametrize(
    ("burners", "firebox", "match"),
    [
        ({"walls": ["left", "right"]}, {}, "go in its mouth wall"),
        ({}, {"count": 2}, "one firebox with no grate"),
        ({"count": None}, {}, "give their count"),
    ],
)
def test_a_gas_firebox_it_refuses(
    burners: dict[str, Any], firebox: dict[str, Any], match: str
) -> None:
    data = _gas_firebox().model_dump(mode="json", by_alias=True)
    data["heat"]["gas"]["burners"].update(burners)
    if "walls" in burners:
        data["heat"]["gas"]["burners"].pop("wall", None)
    data["heat"]["gas"]["firebox"].update(firebox)
    with pytest.raises(ValidationError, match=match):
        Kiln.model_validate(data)


# --- Spy holes and stoke holes placed one by one -------------------------------------------------


def test_a_spy_hole_of_its_own_size_is_cut_beside_the_defaults() -> None:
    kiln = load_design(EXAMPLES / "fast-fire.yaml")
    hw = _hardware(kiln)
    spies = [p for p in hw.ports if p.kind == "spy"]
    assert len(spies) == 4
    assert (spies[-1].width, spies[-1].height) == (2.5, 2.5)
    assert any("1 of the 1 spy holes the design places are cut" in f.message for f in hw.findings)
    assert any(f.message.startswith("Three spy holes") for f in hw.findings)


def test_a_spy_hole_up_through_the_roof() -> None:
    data = _data("gas-crossdraft")
    data["spy_holes"] = {"holes": [{"port": {"diameter": "2 in"}, "wall": "roof",
                                    "along": "6 in"}]}  # fmt: skip
    kiln = Kiln.model_validate(data)
    hw = _hardware(kiln)
    (hole,) = [o for o in hw.openings if o.name == "port/spy-roof-4"]
    assert hole.round_axis == 2
    assert (hole.box[0][1] + hole.box[1][1]) / 2 == pytest.approx(6 * IN)
    assert hole.box[0][2] == pytest.approx(kiln.chamber.height.to("mm").magnitude)
    assert any("up through the roof" in f.message for f in hw.findings)


def test_stoke_holes_in_each_chamber_of_a_row() -> None:
    data = _data("wood-two-chamber")
    port = {"width": "4.5 in", "height": "4.5 in"}
    data["stoke_holes"] = [
        *({"port": port, "wall": "left", "up": "12 in", "chamber": c} for c in (1, 2)),
        {"port": port, "wall": "roof", "chamber": 2},
    ]
    kiln = Kiln.model_validate(data)
    hw = _hardware(kiln)
    stokes = [p for p in hw.ports if p.name.startswith("port/stoke-")]
    assert len(stokes) == 2
    assert stokes[0].across != stokes[1].across
    assert [o for o in hw.openings if o.name == "port/stoke-roof-3"]
    assert any("3 of the 3 stoke holes" in f.message for f in hw.findings)


def test_a_stoke_hole_in_a_door() -> None:
    data = _data("groundhog")
    data["stoke_holes"] = [{"port": {"width": "9 in", "height": "9 in"}, "wall": "front",
                            "up": "10 in", "across": "12 in"}]  # fmt: skip
    hw = _hardware(Kiln.model_validate(data))
    assert [p for p in hw.ports if p.name == "port/stoke-1"]


@pytest.mark.parametrize(
    ("hole", "match"),
    [
        ({"wall": "roof", "up": "3 in"}, "no height up a wall"),
        ({"wall": "left"}, "needs its height"),
        ({"wall": "left", "up": "3 in", "along": "2 in"}, "along places a hole"),
        ({"wall": "left", "up": "3 in", "chamber": 3}, "the kiln has 1"),
        ({"wall": "roof", "across": "100 in"}, "reaches past its chamber"),
    ],
)
def test_holes_it_refuses(hole: dict[str, Any], match: str) -> None:
    data = _data("gas-crossdraft")
    data["stoke_holes"] = [{"port": {"diameter": "2 in"}, **hole}]
    with pytest.raises(ValidationError, match=match):
        Kiln.model_validate(data)


def test_holes_it_refuses_in_a_row() -> None:
    data = _data("wood-two-chamber")
    data["spy_holes"] = {"holes": [{"port": {"diameter": "2 in"}, "wall": "front", "up": "5 in",
                                    "chamber": 2}]}  # fmt: skip
    with pytest.raises(ValidationError, match="the front wall is chamber 1's"):
        Kiln.model_validate(data)
    data["spy_holes"] = {"holes": [{"port": {"diameter": "2 in"}, "wall": "left", "up": "5 in",
                                    "across": "500 in"}]}  # fmt: skip
    with pytest.raises(ValidationError, match="reaches past the chamber's"):
        Kiln.model_validate(data)


def test_holes_need_a_box_chamber_and_a_roof() -> None:
    round_ = load_design(EXAMPLES / "singh-coal.yaml").model_dump(mode="json", by_alias=True)
    round_["stoke_holes"] = [{"port": {"diameter": "2 in"}, "wall": "left", "up": "5 in"}]
    with pytest.raises(ValidationError, match="box chamber's straight walls"):
        Kiln.model_validate(round_)
    open_ = load_design(TEMPLATES / "round-open-top.yaml").model_dump(mode="json", by_alias=True)
    open_["stoke_holes"] = [{"port": {"diameter": "2 in"}, "wall": "roof"}]
    with pytest.raises(ValidationError, match="open top has no roof"):
        Kiln.model_validate(open_)


def test_a_catenary_takes_no_holes_in_its_sides() -> None:
    data = _data("catenary-gas")
    data["stoke_holes"] = [{"port": {"diameter": "2 in"}, "wall": "left", "up": "5 in"}]
    with pytest.raises(ValidationError, match="a stoke hole can't go in the left"):
        Kiln.model_validate(data)


def test_a_spy_hole_that_doesnt_fit_is_refused_by_the_port_check() -> None:
    data = _data("gas-crossdraft")
    data["spy_holes"] = {"holes": [{"port": {"diameter": "2 in"}, "wall": "back",
                                    "up": "-5 in"}]}  # fmt: skip
    kiln = Kiln.model_validate(data)
    hw = _hardware(kiln)
    assert any("0 of the 1 spy holes" in f.message for f in hw.findings)
    assert hw.refused
    assert isinstance(Faces(kiln).plane("back"), float)
