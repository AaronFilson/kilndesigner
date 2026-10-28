"""The hardware: frame, door or car, ports, burners, chimney and spy holes, placed on the kiln."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import cast

import pytest

from kilndesigner import load_design, parse_design
from kilndesigner.geometry import lining_parts
from kilndesigner.hardware import MM, Hardware, build_hardware, layout
from kilndesigner.model import Face, Kiln
from kilndesigner.report import Report, design_report
from kilndesigner.working import Finding

EXAMPLES = Path(__file__).parents[2] / "examples"


def _hardware(name: str) -> tuple[Hardware, tuple[Kiln, Report]]:
    kiln = load_design(EXAMPLES / name)
    report = design_report(kiln)
    return build_hardware(kiln, report.frame, report.gas), (kiln, report)


@pytest.mark.parametrize("name", sorted(p.name for p in EXAMPLES.glob("*.yaml")))
def test_every_piece_and_opening_is_a_real_solid(name: str) -> None:
    hw, _ = _hardware(name)
    for piece in hw.pieces:
        assert piece.boxes or piece.cylinders, piece.name
        for lo, hi in piece.boxes:
            assert all(h > lo_ for lo_, h in zip(lo, hi, strict=True)), piece.name
        for c in piece.cylinders:
            assert c.radius > 0, piece.name
            assert c.length > 0, piece.name
    for opening in hw.openings:
        lo, hi = opening.box
        assert all(h > lo_ for lo_, h in zip(lo, hi, strict=True)), opening.name
    assert len({p.name for p in hw.pieces}) == len(hw.pieces)


def test_the_gas_kiln_has_its_burners_flue_chimney_and_spy_holes() -> None:
    hw, (_, report) = _hardware("pnw-hybrid-crossdraft.yaml")
    gas = report.gas
    assert gas is not None
    assert gas.burners is not None
    assert gas.chimney_height is not None
    names = {o.name for o in hw.openings}
    assert {f"port/burner-{i + 1}" for i in range(gas.burners.count)} <= names
    assert {"port/flue", "port/damper", "port/spy-1", "port/spy-2", "port/spy-3"} <= names
    assert len([p for p in hw.pieces if p.name.startswith("burner/")]) == gas.burners.count
    # The chimney's inside is at least the flue's area (Rhodes) and it reaches the height found
    stack = next(p for p in hw.pieces if p.name == "chimney/stack")
    top = max(hi[2] for _, hi in stack.boxes) / MM
    assert top == pytest.approx(float(gas.chimney_height.split("(")[1].split()[0]))
    xs = sorted({v for lo, hi in stack.boxes for v in (lo[0], hi[0])})
    ys = sorted({v for lo, hi in stack.boxes for v in (lo[1], hi[1])})
    inside = (xs[-2] - xs[1]) * (ys[-2] - ys[1]) / MM**2
    assert inside >= float(gas.flue_area.split()[0])
    assert hw.chimney_bricks > 0


def test_ports_go_through_their_walls() -> None:
    hw, (kiln, _) = _hardware("pnw-hybrid-crossdraft.yaml")
    parts = lining_parts(kiln)
    for opening in hw.openings:
        if opening.name in ("port/chimney-inlet", "port/damper"):
            continue
        lo, hi = opening.box
        hit = [
            p for p in parts
            if all(p.lo[i] < hi[i] and p.hi[i] > lo[i] for i in range(3))
        ]  # fmt: skip
        assert hit, f"{opening.name} cuts nothing"
        # Through every layer of the wall it's in
        faces = {p.face for p in hit}
        assert len(faces) == 1, opening.name
        face = faces.pop()
        assert face is not None
        layers = kiln.lining.for_face(cast("Face", face), door_face=kiln.door_face)
        assert len(hit) >= len(layers), opening.name


def test_the_electric_kiln_has_a_case_a_hinged_door_and_peepholes() -> None:
    hw, _ = _hardware("electric-front-loader.yaml")
    names = {p.name for p in hw.pieces}
    assert {"case/left", "case/right", "case/back", "case/stand", "door/case"} <= names
    assert {"door/hinge-1", "door/hinge-2", "door/latch-1", "door/latch-2"} <= names
    assert not any(n.startswith(("frame/", "burner/", "chimney/")) for n in names)
    holes = [o for o in hw.openings if o.name.startswith("port/spy")]
    assert len(holes) == 3
    for o in holes:  # 1 in round holes
        lo, hi = o.box
        assert o.round_axis is not None
        across = [hi[i] - lo[i] for i in range(3) if i != o.round_axis]
        assert min(across) == pytest.approx(25.4)


def test_a_dense_hinged_door_asks_for_its_hardware_to_be_checked() -> None:
    """Pitelka's hinged door is one layer of IFB [S13]: a heavier door is a warning, not a rule."""
    text = (EXAMPLES / "gas-crossdraft.yaml").read_text(encoding="utf-8")
    hinged = text.replace("face: right", "face: right\n  door: hinged")

    def door_findings(source: str) -> list[Finding]:
        kiln = parse_design(source)
        report = design_report(kiln)
        hw = build_hardware(kiln, report.frame, report.gas)
        return [f for f in hw.findings if "hinged door is lined" in f.message]

    assert door_findings(hinged) == []
    [finding] = door_findings(
        hinged.replace("material: ifb-jm26", "material: hard-firebrick-kx99", 1)
    )
    assert finding.level == "warning"
    assert "HarbisonWalker KX-99 super-duty firebrick" in finding.message
    assert "never" not in finding.message


def test_a_car_kiln_has_a_car() -> None:
    hw, _ = _hardware("pnw-hybrid-crossdraft-car.yaml")
    names = {p.name for p in hw.pieces}
    assert {"car/frame", "car/wheels", "car/rails"} <= names
    assert any("not sized" in f.message for f in hw.findings)


def _example(name: str, **changes: object) -> tuple[Hardware, Kiln, Report]:
    """An example, with parts of its design replaced: ``heat__gas__burners={...}`` replaces
    heat.gas.burners, and so on along the path."""
    document = load_design(EXAMPLES / name).model_dump(mode="json", by_alias=True)
    for path, value in changes.items():
        *parents, last = path.split("__")
        target = document
        for key in parents:
            target = target.setdefault(key, {})
        target[last] = value
    kiln = Kiln.model_validate(document)
    report = design_report(kiln)
    return build_hardware(kiln, report.frame, report.gas), kiln, report


def _gas(**changes: object) -> tuple[Hardware, Kiln, Report]:
    """The gas cross-draft (28 × 48 × 40 in inside, 8 in walls), changed."""
    return _example("gas-crossdraft.yaml", **changes)


def _electric(**changes: object) -> tuple[Hardware, Kiln, Report]:
    """The electric front-loader (22½ × 22½ × 24 in inside, 5½ in walls), changed."""
    return _example("electric-front-loader.yaml", **changes)


def _spots(hw: Hardware, kind: str) -> list[tuple[str, float, float, float, float]]:
    return [(p.wall, p.across, p.up, p.width, p.height) for p in hw.ports if p.kind == kind]


def _errors(hw: Hardware) -> list[str]:
    return [f.message for f in hw.findings if f.level == "error"]


def test_burners_go_where_they_are_placed_and_number_one_a_place() -> None:
    places = [
        {"wall": "front", "across": "-6 in", "up": "6 in"},
        {"wall": "left", "across": "10 in", "up": "5 in"},
        {"wall": "left", "across": "-10 in", "up": "5 in"},
    ]
    hw, _, report = _gas(heat__gas__burners={"model": "Ransome B4", "places": places})
    assert report.gas is not None
    assert report.gas.burners is not None
    assert report.gas.burners.count == 3
    assert [s[:3] for s in _spots(hw, "burner")] == [
        ("front", -6, 6),
        ("left", 10, 5),
        ("left", -10, 5),
    ]
    assert not _errors(hw)
    # A port on the left wall is cut through it, centred where it was placed: across is to the
    # right as you face the wall from outside, which on the left wall is towards the front.
    port = next(o for o in hw.openings if o.name == "port/burner-2")
    (x0, y0, z0), (x1, y1, z1) = port.box
    assert x0 < -(14 + 8) * MM  # through the 8 in left wall,
    assert x1 == pytest.approx(-13 * MM)  # from an inch inside it
    assert (y0 + y1) / 2 == pytest.approx(-10 * MM)
    assert (z0 + z1) / 2 == pytest.approx(5 * MM)
    burner = next(p for p in hw.pieces if p.name == "burner/2")
    assert burner.cylinders[0].axis == 0  # fires across the kiln


def test_a_count_and_places_must_agree() -> None:
    with pytest.raises(ValueError, match="a place for each of the 2 burners"):
        _gas(heat__gas__burners={"count": 2, "places": [{"wall": "front", "up": "6 in"}]})


def test_burner_ports_can_be_raised_and_sized() -> None:
    hw, _, _ = _gas(heat__gas__burners={"up": "10 in", "port": {"diameter": "5 in"}})
    assert [s[2:] for s in _spots(hw, "burner")] == [(10, 5, 5), (10, 5, 5)]
    assert not [f for f in hw.findings if f.level != "info" and "port" in f.message]
    # A Ransome B4's head is 3¾ in: a 4 in port is under Ward's inch, a 3 in one too small
    hw, _, _ = _gas(heat__gas__burners={"port": {"diameter": "4 in"}})
    assert any(f.level == "warning" and "Ward's inch" in f.message for f in hw.findings)
    hw, _, _ = _gas(heat__gas__burners={"port": {"width": "3 in", "height": "6 in"}})
    assert any("won't sit within a port 3 in across" in m for m in _errors(hw))


def test_a_port_that_doesnt_fit_its_wall_is_refused_and_not_cut() -> None:
    places = [
        {"wall": "front", "across": "12 in", "up": "6 in"},  # 28 in wide: 12 + 2⅜ is past 14
        {"wall": "front", "across": "-3 in", "up": "2 in"},  # its bottom is below the floor
        {"wall": "front", "across": "0 in", "up": "45 in"},  # above the arch at the front
    ]
    hw, _, _ = _gas(heat__gas__burners={"places": places})
    errors = _errors(hw)
    assert len(errors) == 3
    assert "past the side of the front wall" in errors[0]
    assert "below the floor" in errors[1]
    assert "above the top of the front wall's inside" in errors[2]
    assert not any(o.name.startswith("port/burner") for o in hw.openings)
    assert not any(p.name.startswith("burner/") for p in hw.pieces)


def test_ports_that_overlap_are_refused() -> None:
    places = [
        {"wall": "front", "across": "-7 in", "up": "6 in"},
        {"wall": "back", "across": "0 in", "up": "6 in"},
    ]
    hw, _, _ = _gas(heat__gas__burners={"places": places})
    # The burners are cut first, then the flue, which would cut through burner port 2
    assert [m for m in _errors(hw) if "overlaps" in m] == [
        "Flue port (11.25 × 7.5 in, 0 in across and 3.75 in up the back wall) overlaps burner "
        "port 2, so it isn't cut. Move it or make it smaller."
    ]
    assert [o.name for o in hw.openings if o.name == "port/flue"] == []
    assert not any(p.name.startswith("chimney/") for p in hw.pieces)


def test_spy_holes_can_be_counted_sized_and_placed() -> None:
    hw, _, _ = _gas(spy_holes={"count": 5, "port": {"diameter": "2 in"}})
    spots = _spots(hw, "spy")
    assert len(spots) == 5
    assert {s[0] for s in spots} == {"right"}  # the door
    assert [s[3:] for s in spots] == [(2, 2)] * 5
    assert [s[2] for s in spots] == sorted(s[2] for s in spots)  # from the bottom up
    assert any("5 spy holes, 2 in round" in f.message for f in hw.findings)

    places = [{"wall": "back", "across": "8 in", "up": "30 in"}]
    hw, _, _ = _gas(spy_holes={"places": places})
    assert _spots(hw, "spy") == [("back", 8, 30, 2.25, 2.5)]

    hw, _, _ = _gas(spy_holes={"count": 0})
    assert _spots(hw, "spy") == []
    assert any("No spy holes" in f.message for f in hw.findings)


def test_the_flue_can_be_sized_and_moved_and_the_chimney_follows() -> None:
    hw, _, _ = _gas(draft={"type": "cross", "flue_port": {"width": "9 in", "height": "10 in"},
                           "flue_across": "4 in"})  # fmt: skip
    assert _spots(hw, "flue") == [("back", 4, 5, 9, 10)]
    stack = next(p for p in hw.pieces if p.name == "chimney/stack")
    xs = [v for lo, hi in stack.boxes for v in (lo[0], hi[0])]
    # On the back wall, to the right facing it from outside is towards -x
    assert (min(xs) + max(xs)) / 2 == pytest.approx(-4 * MM)
    assert not any("flue port is" in f.message for f in hw.findings)  # 90 in², over the 83
    hw, _, _ = _gas(draft={"type": "cross", "flue_port": {"width": "6 in", "height": "7.5 in"}})
    assert any(
        f.level == "warning" and "The flue port is 45 in², under the 83 in²" in f.message
        for f in hw.findings
    )


def test_the_layout_has_every_wall_and_every_port_asked_for() -> None:
    places = [
        {"wall": "front", "across": "-7 in", "up": "6 in"},
        {"wall": "front", "across": "13 in", "up": "6 in"},  # past the side: refused
    ]
    hw, kiln, _ = _gas(heat__gas__burners={"places": places})
    shown = json.loads(json.dumps(layout(kiln, hw)))
    assert set(shown["walls"]) == {"front", "back", "left", "right"}
    front = shown["walls"]["front"]
    assert front["half_width"] == pytest.approx(14 * MM)
    assert front["origin"] == pytest.approx([0, -(24 + 8) * MM, 0])  # the outside face
    # The front closes the arch: its inside reaches the crown in the middle, the springline at
    # the sides
    tops = dict(front["top"])
    assert tops[0] == pytest.approx((40 + 3.75) * MM)
    assert tops[-14 * MM] == pytest.approx(40 * MM)
    assert shown["walls"]["left"]["top"][12][1] == pytest.approx(40 * MM)
    burners = [p for p in shown["ports"] if p["kind"] == "burner"]
    assert [(p["name"], p["cut"]) for p in burners] == [
        ("port/burner-1", True),
        ("port/burner-2", False),
    ]
    assert burners[0]["across"] == pytest.approx(-7 * MM)
    assert {p["kind"] for p in shown["ports"]} == {"burner", "flue", "spy"}


def test_a_port_is_a_diameter_or_a_width_and_height() -> None:
    with pytest.raises(ValueError, match="not both"):
        _gas(spy_holes={"port": {"diameter": "2 in", "width": "2 in"}})
    with pytest.raises(ValueError, match="both a width and a height"):
        _gas(spy_holes={"port": {"width": "2 in"}})
    with pytest.raises(ValueError, match="more than zero"):
        _gas(spy_holes={"port": {"diameter": "0 in"}})


def test_a_power_burner_with_no_sourced_port_is_not_drawn() -> None:
    kiln = load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml")
    assert kiln.heat.gas is not None
    gas = kiln.heat.gas.model_copy(
        update={"burners": kiln.heat.gas.burners.model_copy(update={"type": "power"})}
    )
    kiln = kiln.model_copy(update={"heat": kiln.heat.model_copy(update={"gas": gas})})
    report = design_report(kiln)
    hw = build_hardware(kiln, report.frame, report.gas)
    assert not any(o.name.startswith("port/burner") for o in hw.openings)
    assert any("port size" in f.message for f in hw.findings)
    assert math.isfinite(hw.chimney_bricks)


def test_burners_with_no_sourced_port_size_are_cut_to_the_size_given() -> None:
    hw, _, report = _gas(
        heat__gas__burners={"model": "GACO MR100", "port": {"width": "5 in", "height": "5 in"}}
    )
    assert report.gas is not None
    assert report.gas.burners is not None
    assert report.gas.burners.model == "GACO MR100"
    assert [s[3:] for s in _spots(hw, "burner")] == [(5, 5)] * report.gas.burners.count
    assert any(
        f.level == "info"
        and f.message == "The burner ports are the size given; no source gives one for GACO MR100."
        for f in hw.findings
    )
    # No source gives an MR100's body either, so no burner is drawn in its port
    assert not any(p.name.startswith("burner/") for p in hw.pieces)


def test_burners_that_cant_fire_the_kiln_get_no_ports() -> None:
    """One GACO MR750 can't deliver the cross-draft's design input within 10 psi."""
    hw, _, report = _gas(heat__gas__burners={"model": "GACO MR750", "count": 1})
    assert report.gas is not None
    assert report.gas.burners is None
    assert any("The burners chosen can't deliver" in f.message for f in report.gas.findings)
    assert _spots(hw, "burner") == []
    assert not any(p.name.startswith("burner/") for p in hw.pieces)
    assert not any("bag wall" in f.message for f in hw.findings)
    assert len(_spots(hw, "flue")) == 1  # the rest of the kiln is still drawn


def test_a_flat_roofed_gas_kiln_is_framed_in_roof_angle_and_rods() -> None:
    """Merrill's flat-top frame (frame.py): L2×2×3/16 round the top of the walls, 45 in up (40 in
    inside and the 5 in roof), and ⅜ in rods 44 + 2 × 2 + 4 = 52 in long across it."""
    hw, _, report = _gas(roof={"type": "flat"})
    assert report.frame.kind == "angle frame"
    pieces = {p.name: p for p in hw.pieces}
    left = pieces["frame/left-top"]
    assert left.title == "Roof angle, left side"
    assert left.detail == "L2×2×3/16; Merrill flat-top kiln; kiln-hardware.md §4.2 [S16]"
    assert max(hi[2] for _, hi in left.boxes) == pytest.approx((45 + 0.1875) * MM)
    for i in range(4):
        post = pieces[f"frame/post-{i + 1}"]
        assert min(lo[2] for lo, _ in post.boxes) == pytest.approx(-7 * MM)  # under the floor
        assert max(hi[2] for _, hi in post.boxes) == pytest.approx((45 + 0.1875) * MM)
    for end in ("front", "back"):
        [rod] = pieces[f"frame/{end}-rod"].cylinders
        assert (rod.axis, rod.radius, rod.length) == pytest.approx((0, 0.1875 * MM, 52 * MM))


def test_the_chimneys_bricks_are_its_volume_in_straights() -> None:
    """The stack and the duct to it, in 9 × 4½ × 2½ in straights, with the 5 % for cuts the bill
    of materials gives."""
    straight = 9 * 4.5 * 2.5 * MM**3
    hw, _, _ = _gas()
    pieces = {p.name: p for p in hw.pieces}
    volume = pieces["chimney/stack"].volume + pieces["chimney/duct"].volume
    assert hw.chimney_bricks == math.ceil(volume / straight * 1.05)

    # Built against the flue wall: no duct, and the stack's near wall on the wall's outside
    hw, _, _ = _gas(draft={"type": "cross", "flue_wall": "back", "run_to_chimney": "0 in"})
    pieces = {p.name: p for p in hw.pieces}
    assert "chimney/duct" not in pieces
    stack = pieces["chimney/stack"]
    assert min(lo[1] for lo, _ in stack.boxes) == pytest.approx((24 + 8) * MM)
    assert hw.chimney_bricks == math.ceil(stack.volume / straight * 1.05)


@pytest.mark.parametrize("draft", [{"type": "up"}, None], ids=["up-draft", "no draft"])
def test_an_up_draft_flue_is_a_square_in_the_roof_with_no_chimney(
    draft: dict[str, str] | None,
) -> None:
    hw, _, report = _gas(draft=draft)
    assert report.gas is not None
    assert report.gas.chimney_height is None
    [flue] = [o for o in hw.openings if o.name == "port/flue"]
    (x0, y0, z0), (x1, y1, _) = flue.box
    side = math.sqrt(float(report.gas.flue_area.split()[0])) * MM  # Ward's area, square
    assert (x1 - x0, y1 - y0) == pytest.approx((side, side))
    assert ((x0 + x1) / 2, (y0 + y1) / 2) == pytest.approx((0, 0), abs=1e-9)  # mid-roof
    assert z0 == pytest.approx((40 - 1) * MM)  # from an inch below the springline, up
    assert flue.round_axis is None
    assert _spots(hw, "flue") == []  # not a port in a wall, to show or move
    assert not any(p.name.startswith("chimney/") for p in hw.pieces)
    assert hw.chimney_bricks == 0


def test_an_up_draft_flue_can_be_round_and_is_checked_against_wards_area() -> None:
    hw, _, _ = _gas(draft={"type": "up", "flue_port": {"diameter": "10 in"}})
    [flue] = [o for o in hw.openings if o.name == "port/flue"]
    (x0, y0, _), (x1, y1, _) = flue.box
    assert (flue.round_axis, x1 - x0, y1 - y0) == pytest.approx((2, 10 * MM, 10 * MM))
    # π × 5² = 78.5 in², under the 2.5 in² per ft³ of the 33 ft³ chamber
    assert any(
        f.level == "warning" and "The flue port is 79 in², under the 83 in²" in f.message
        for f in hw.findings
    )


def test_a_flue_too_wide_for_a_narrow_wall_is_made_taller() -> None:
    """A kiln 12 in wide with its flue in the back wall: three 2½ in courses would make the flue
    wider than the 10 in the wall leaves, so it goes up a course at a time until it fits."""
    hw, _, report = _gas(
        chamber={"width": "12 in", "depth": "100 in", "height": "48 in"},
        heat__gas__burners={"wall": "left"},
    )
    assert report.gas is not None
    area = float(report.gas.flue_area.split()[0])
    courses = next(n for n in range(3, 9) if area / (2.5 * n) <= 12 - 2)
    assert courses > 3
    [(wall, across, up, width, height)] = _spots(hw, "flue")
    assert (wall, across) == ("back", 0)
    assert height == pytest.approx(courses * 2.5)
    assert up == pytest.approx(height / 2)  # at the foot of the wall
    assert width == pytest.approx(math.ceil(area / height * 4) / 4)  # to the next ¼ in
    assert width * height >= area
    assert not _errors(hw)


def test_a_car_rolls_out_of_its_end_on_rails_a_kiln_long() -> None:
    """Outside, the cross-draft runs from y = −32 to 32 in (48 in inside, 8 in walls)."""
    hw, _, _ = _gas(loading={"type": "car", "face": "front"})
    rails = next(p for p in hw.pieces if p.name == "car/rails")
    assert len(rails.boxes) == 2
    for lo, hi in rails.boxes:  # out of the front, as far again as the kiln is long
        assert (lo[1], hi[1]) == pytest.approx((-(32 + 64) * MM, 32 * MM))
    side_wall = "a car through a side wall is drawn with its rails under the kiln only"
    assert not any(side_wall in f.message for f in hw.findings)

    hw, _, _ = _gas(loading={"type": "car", "face": "right"})
    rails = next(p for p in hw.pieces if p.name == "car/rails")
    for lo, hi in rails.boxes:
        assert (lo[1], hi[1]) == pytest.approx((-32 * MM, 32 * MM))
    assert any(side_wall in f.message for f in hw.findings)


def test_an_electric_kilns_door_in_a_side_wall_takes_that_side_of_the_case() -> None:
    hw, _, _ = _electric(loading={"face": "left"}, heat__electric__walls=["right", "back"])
    names = {p.name for p in hw.pieces}
    assert "case/left" not in names
    assert {"case/right", "case/back", "case/top", "case/bottom", "door/case"} <= names
    # The door's ⅛ in plate is on the outside of the left wall, 11¼ + 5½ in from the middle
    [(lo, hi)] = next(p for p in hw.pieces if p.name == "door/case").boxes
    assert (lo[0], hi[0]) == pytest.approx((-(16.75 + 0.125) * MM, -16.75 * MM))
    assert {o.name for o in hw.openings} == {"port/spy-1", "port/spy-2", "port/spy-3"}
    assert {s[0] for s in _spots(hw, "spy")} == {"left"}


def test_electric_peepholes_say_how_many_where_and_what_size() -> None:
    reference = "electric-kiln-hardware.md §4 [S3] [S6]"

    def note(hw: Hardware) -> Finding:
        return next(f for f in hw.findings if "peephole" in f.message)

    hw, _, _ = _electric(spy_holes={"count": 2})
    assert _spots(hw, "spy") == [("front", 0, 8, 1, 1), ("front", 0, 16, 1, 1)]  # 24 in, thirds
    assert note(hw).message == "2 peepholes, 1 in round, in the door, spaced evenly."
    assert note(hw).reference == reference

    hw, _, _ = _electric(spy_holes={"places": [{"wall": "back", "up": "12 in"}]})
    assert _spots(hw, "spy") == [("back", 0, 12, 1, 1)]
    assert note(hw).message == "1 peephole, 1 in round, where the design places them."

    hw, _, _ = _electric(spy_holes={"count": 1, "port": {"width": "1 in", "height": "2 in"}})
    assert _spots(hw, "spy") == [("front", 0, 12, 1, 2)]
    assert note(hw).message == "1 peephole, 1 × 2 in, in the door, spaced evenly."
