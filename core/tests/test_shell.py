"""Chambers and shell (shell.py): no door, a hung door, a cone for each chamber, chambers of
different sizes, a back wall of its own, a width changing along the run, and offset-peak arches."""

import math
from pathlib import Path

import pytest
from pydantic import ValidationError

from kilndesigner.designfile import parse_design
from kilndesigner.drawings import section_views
from kilndesigner.frame import cold_thrust_factor, design_frame
from kilndesigner.geometry import lining_parts, not_drawn, write_model
from kilndesigner.hardware import build_hardware
from kilndesigner.heatloss import heat_loss
from kilndesigner.massing import cells, run_of
from kilndesigner.report import design_report
from kilndesigner.run_parts import run_layout
from kilndesigner.shape import Arch, chamber_shape
from kilndesigner.shell import (
    PeakArch,
    Taper,
    chamber_temperatures,
    door_weight,
    sizes_of,
    width_at,
    widths_of,
)
from kilndesigner.units import si

OLSEN = Path(__file__).parents[2] / "examples" / "olsen"


def _text(name: str) -> str:
    return (OLSEN / f"{name}.yaml").read_text(encoding="utf-8")


def _edit(name: str, *changes: tuple[str, str]) -> str:
    text = _text(name)
    for old, new in changes:
        assert old in text, old
        text = text.replace(old, new, 1)
    return text


# --- A back wall of its own -------------------------------------------------------------------


def test_the_back_wall_takes_its_own_layers() -> None:
    kato = parse_design(_text("kato-coal"))
    assert [si(x.thickness, "in") for x in kato.lining.for_face("back")] == [10]
    assert [si(x.thickness, "in") for x in kato.lining.for_face("left")] == [18]
    # A door in the back wall takes lining.door first
    assert kato.lining.for_face("back", door_face="back")[0] is kato.lining.door[0]  # type: ignore[index]
    back = [p for p in lining_parts(kato) if p.name.startswith("back/1-") and not p.cap]
    assert back
    assert {round(p.length_y, 6) for p in back} == {254.0}
    thick = parse_design(
        _edit("kato-coal", ('thickness: 10 in # "10"" by', "thickness: 18 in # by"))
    )
    assert heat_loss(kato).total_watts > heat_loss(thick).total_watts


# --- No door ----------------------------------------------------------------------------------


def test_a_kiln_set_over_its_walls_has_no_door() -> None:
    singh = parse_design(_text("singh-lowfire"))
    assert singh.door_wall is None
    assert singh.door_kind is None
    hw = build_hardware(singh, design_frame(singh), None, None)
    assert any("has no door" in f.message for f in hw.findings)
    assert not any(p.face == "front" and "door" in p.name for p in lining_parts(singh))


def test_no_door_is_for_an_open_top_without_a_door() -> None:
    with pytest.raises(ValidationError, match="open-topped"):
        parse_design(_edit("singh-lowfire", ("type: open # shards", "type: flat # shards")))
    with pytest.raises(ValidationError, match="has no door"):
        parse_design(_edit("singh-lowfire", ("type: top #", "door: bricked\n  type: top #")))


# --- A door hung on its own frame -------------------------------------------------------------


def test_a_hung_doors_weight_is_checked_against_its_trolleys() -> None:
    kaneko = parse_design(_text("kaneko-car"))
    assert kaneko.door_kind is None
    weight, area, lines = door_weight(kaneko)
    # The front wall, out to the side walls' outside, to the springline, and the arch's segment
    seg = Arch(96, 14).segment_area
    assert area == pytest.approx(((96 + 14) * 96 + seg) / 144)
    assert len(lines) == 2
    assert weight > 0
    frame = design_frame(kaneko)
    assert any(s.name.startswith("The hung door") for s in frame.working)
    assert [f.level for f in frame.findings if "trolleys" in f.message] == ["info"]
    light = parse_design(_edit("kaneko-car", ("trolley_rating: 1000 lb", "trolley_rating: 100 lb")))
    assert [f.level for f in design_frame(light).findings if "trolleys" in f.message] == ["warning"]
    report = design_report(kaneko)
    assert report.bom is not None
    assert any(line.item.startswith("Door trolleys") for line in report.bom.lines)


def test_a_hung_door_in_part_of_a_wall_weighs_the_opening() -> None:
    kato = parse_design(
        _edit(
            "kato-coal",
            ("  door: bricked\n", "  hung:\n    trolleys: 1\n    trolley_rating: 500 lb\n"
             "  opening:\n    width: 20 in\n    height: 30 in\n"),
            ("  door:\n    - material: firebrick-medium-duty-smithfield\n      thickness: 10 in "
             "# \"10\"\" at the door end (Fig 5-4)\n", ""),
        )
    )  # fmt: skip
    from kilndesigner.castable import resolve_material
    from kilndesigner.units import parse_quantity

    weight, area, _ = door_weight(kato)
    assert area == pytest.approx(600 / 144)
    density = parse_quantity(resolve_material(kato, kato.lining.walls[0].material).density)
    assert weight == pytest.approx(si(density, "lb/ft**3") * 18 / 12 * 600 / 144)
    hw = build_hardware(kato, design_frame(kato), None, None)
    assert any("hung on its own frame" in f.message for f in hw.findings)


def test_a_hung_door_closes_a_wall_and_has_no_hinges() -> None:
    with pytest.raises(ValidationError, match="neither bricked up nor hinged"):
        parse_design(
            _edit(
                "kaneko-car", ("  face: front\n  hung:", "  door: hinged\n  face: front\n  hung:")
            )
        )
    with pytest.raises(ValidationError, match="closes a wall"):
        parse_design(
            _edit(
                "singh-lowfire",
                ("type: top #", "hung: {trolleys: 1, trolley_rating: 9 lb}\n  type: top #"),
            )
        )
    with pytest.raises(ValidationError, match="more than 0"):
        parse_design(_edit("kaneko-car", ("trolley_rating: 1000 lb", "trolley_rating: 0 lb")))


# --- A cone for each chamber ------------------------------------------------------------------


def test_each_chamber_loses_heat_at_its_own_cone() -> None:
    suzuki = parse_design(_text("suzuki-kyoto"))
    temps = chamber_temperatures(suzuki)
    assert temps[0] == temps[1] == max(temps)
    assert temps[-1] == min(temps)
    hot = parse_design(
        _edit("suzuki-kyoto", ('  chamber_cones: ["10", "10", "9", "9", "9", "9", "1"]', ""))
    )
    each, top = heat_loss(suzuki), heat_loss(hot)
    assert each.total_watts < top.total_watts
    step = next(s for s in each.working if s.name.startswith("Heat loss, each chamber"))
    assert len(step.inputs) == 7
    # Each chamber the same size: the loss is the mean of the run's at each temperature
    ones = [heat_loss(hot, inside=si_k(t)).total_watts for t in temps]
    assert each.total_watts == pytest.approx(sum(ones) / 7)
    # None takes the firing's top
    some = parse_design(
        _edit("suzuki-kyoto", ('"9", "9", "9", "9", "1"]', '"9", "9", "9", "9", null]'))
    )
    assert chamber_temperatures(some)[-1] == temps[0]


def si_k(t: float):
    from kilndesigner.units import Q_

    return Q_(t, "K")


def test_a_cone_for_each_chamber_is_one_a_chamber_and_no_hotter_than_the_top() -> None:
    with pytest.raises(ValidationError, match="each of the 7 chambers"):
        parse_design(_edit("suzuki-kyoto", ('"9", "1"]', '"1"]')))
    with pytest.raises(ValidationError, match="hotter than the firing's top"):
        parse_design(_edit("suzuki-kyoto", ('["10", "10", "9"', '["11", "10", "9"')))
    with pytest.raises(ValidationError, match="not in the Orton table"):
        parse_design(_edit("suzuki-kyoto", ('["10", "10", "9"', '["10", "10", "99"')))


# --- Chambers of different sizes --------------------------------------------------------------


def test_chambers_of_different_sizes_take_their_own_volume() -> None:
    bidai = parse_design(_text("bidai"))
    assert sizes_of(bidai, "in") == [(42, 38, 21), (46, 42, 23), (36, 41, 18)]
    assert si(bidai.chamber.length, "in") == 124
    expected = sum(73 * (d * h + math.pi * r * r / 2) for d, h, r in sizes_of(bidai, "in"))
    assert chamber_shape(bidai).volume == pytest.approx(expected * 0.0254**3, rel=1e-9)
    run = run_layout(bidai)
    assert run.front(0) == pytest.approx(-21 * 25.4)
    assert run.back(2) - run.front(0) == pytest.approx((124 + 2 * 9.5) * 25.4)
    assert run.springline(1) == pytest.approx(run.floor(1) + 42 * 25.4)
    assert run.stepped
    # Each chamber's arch is its own: three arches, each over its own depth
    roofs = [p for p in lining_parts(bidai) if p.name.startswith("roof/")]
    assert {p.chamber for p in roofs} == {1, 2, 3}
    frame = design_frame(bidai)
    assert [s.name for s in frame.working if s.name.startswith("Thrust")] == [
        f"Thrust the masonry holds, chamber {i}'s arch" for i in (1, 2, 3)
    ]
    *_, plan = section_views(bidai)
    assert "each chamber" in plan.title


def test_chambers_of_different_sizes_on_the_level_under_domes() -> None:
    holly = parse_design(_text("hollyweird"))
    shape = chamber_shape(holly)
    assert si(holly.chamber.length, "ft") == pytest.approx(20)
    assert {f.face for f in shape.faces()} == {"left", "right", "back", "front", "floor", "roof"}
    roof = next(f for f in shape.faces() if f.face == "roof")
    assert roof.area_at(0.1) > roof.inside_area
    massing = cells(holly, run_of(holly))
    assert [round(c.length / 25.4) for c in massing if c.kind == "box"] == [96, 144]
    flat = parse_design(_edit("hollyweird", ("  type: dome\n  rise: 12.6 in\n  buttressed: true\n",
                                              "  type: flat\n")))  # fmt: skip
    assert chamber_shape(flat).volume == pytest.approx(55 * 240 * 35.4 * 0.0254**3)


def test_chambers_of_different_sizes_are_refused_outside_their_range() -> None:
    cases = {
        "a size for each": (
            "    - depth: 36 in\n      height: 41 in\n      rise: 18 in # 59 in to the crown\n",
            "",
        ),
        "held by masonry": ("  buttressed: true # thrust", "  buttressed: false # thrust"),
        "at most half": ("      rise: 18 in", "      rise: 19 in"),
        "a tube's vault": ("  rise: 21 in # chamber 1's", "  rise: 21 in\n  tube: true #"),
    }
    for match, change in cases.items():
        with pytest.raises(ValidationError, match=match):
            parse_design(_edit("bidai", change))
    with pytest.raises(ValidationError, match="more than 0"):
        parse_design(_edit("bidai", ("    - depth: 42 in\n", "    - depth: 0 in\n")))
    with pytest.raises(ValidationError, match="less than half its diagonal"):
        parse_design(
            _edit("hollyweird", ("    - depth: 8 ft\n", "    - depth: 8 ft\n      rise: 99 in\n"))
        )
    for bad in ("height: -1 in", "rise: -1 in"):
        with pytest.raises(ValidationError, match="more than 0"):
            parse_design(
                _edit("hollyweird", ("    - depth: 8 ft\n", f"    - depth: 8 ft\n      {bad}\n"))
            )


# --- A width changing along the run -----------------------------------------------------------


def test_a_plan_tapering_to_the_chimney() -> None:
    hog = parse_design(_text("ellington-new-hog"))
    assert widths_of(hog, "in") == [(0, 120), (120, 120), (216, 48)]
    taper = Taper(tuple(widths_of(hog, "in")))
    assert taper.area == pytest.approx(120 * 120 + 96 * 84)
    assert taper.widest == 120
    assert taper.front == 120
    assert taper.back == 48
    assert width_at(list(taper.stations), 168) == pytest.approx(84)
    assert width_at(list(taper.stations), -1) == 120
    assert width_at(list(taper.stations), 999) == 48
    # The arch keeps its shape: its segment scales as the width squared
    seg = Arch(120, 43).segment_area / 120**2
    assert chamber_shape(hog).volume == pytest.approx(seg * taper.square * 0.0254**3)
    assert "width changes" in (not_drawn(hog) or "")
    frame = design_frame(hog)
    assert frame.working[0].name == "The widest section"


def test_a_tunnel_whose_width_changes_is_framed_at_its_widest() -> None:
    kannofen = parse_design(_text("kannofen"))
    frame = design_frame(kannofen)
    assert frame.working[0].name == "The widest section"
    assert "1.07" not in frame.working[0].value  # inches
    assert frame.members
    massing = [c for c in cells(kannofen, run_of(kannofen)) if c.kind == "box"]
    assert len(massing) == 16
    assert max(c.width for c in massing) > min(c.width for c in massing)
    flat = parse_design(
        _edit("kannofen", ("  type: sprung_arch\n  rise: 0.26 m\n", "  type: flat\n"))
    )
    assert chamber_shape(flat).volume == pytest.approx(
        Taper(tuple(widths_of(flat, "m"))).area * 1.365
    )


def test_a_width_changing_along_the_run_is_refused_outside_its_range() -> None:
    cases = {
        "from the front wall": ("    - at: 0 m\n", "    - at: 0.1 m\n"),
        "in order": ("    - at: 3.0 m\n", "    - at: 1.0 m\n"),
        "more than 0": ("      width: 1.04 m\n", "      width: 0 m\n"),
        "one straight box": ("  depth: 4.5 m\n", "  depth: 4.5 m\n  chambers: 2\n"),
        "sprung arch across": ("  rise: 0.26 m\n", "  rise: 0.26 m\n  along: true\n"),
    }
    for match, change in cases.items():
        with pytest.raises(ValidationError, match=match):
            parse_design(_edit("kannofen", change))


# --- Arches of two radii ----------------------------------------------------------------------


def test_a_peak_mid_span_is_the_circular_arch() -> None:
    peak, circle = PeakArch(42, 15, 0.5), Arch(42, 15)
    assert peak.front_radius == pytest.approx(circle.radius)
    assert peak.arc_length == pytest.approx(circle.arc_length)
    assert peak.segment_area == pytest.approx(circle.segment_area)
    h, front, back = peak.thrust(100.0)
    assert h == pytest.approx(cold_thrust_factor(42, 15) * 100)
    assert front == pytest.approx(50)
    assert back == pytest.approx(50)
    assert peak.height(21) == pytest.approx(15)
    assert peak.height(0) == pytest.approx(0, abs=1e-9)


def test_an_offset_peak_moves_the_load_to_the_longer_half() -> None:
    peak = PeakArch(42, 15, 0.6)
    assert peak.front_radius > peak.back_radius
    h, front, back = peak.thrust(100.0)
    assert front + back == pytest.approx(100)
    # The whole arch about the back springing, the springings level so H has no moment there:
    # V_f·S = Σ W·(S − x), each half's weight at its centroid, r(1 − cos φ)/φ from the peak
    (rf, pf, af), (rb, pb, _ab) = peak.halves()
    wf = 100 * rf * pf / peak.arc_length
    xf, xb = af - rf * (1 - math.cos(pf)) / pf, af + rb * (1 - math.cos(pb)) / pb
    assert front == pytest.approx((wf * (42 - xf) + (100 - wf) * (42 - xb)) / 42)
    assert h > 0
    # A line of thrust through the hinges lies inside a thick ring
    assert peak.line_gap(9) < peak.line_gap(3)


def _peaked(share: str, ring: str = "9 in # as the Bidai kiln's arch") -> str:
    return _edit(
        "kyoto-climbing",
        ("  buttressed: true #", f"  peak_at: {share}\n  buttressed: true #"),
        ("9 in # as the Bidai kiln's arch", ring),
        ("  rise: 20.7 in", "  rise: 15 in"),
    )


def test_an_offset_peak_arch_is_held_by_masonry_by_its_line_of_thrust() -> None:
    kiln = parse_design(_peaked("55 percent"))
    frame = design_frame(kiln)
    steps = [s for s in frame.working if s.name.startswith("Thrust the masonry holds")]
    assert len(steps) == 10
    assert "line of thrust" in steps[0].value
    assert "two radii" in (not_drawn(kiln) or "")
    shape = chamber_shape(kiln)
    level = chamber_shape(parse_design(_edit("kyoto-climbing", ("rise: 20.7 in", "rise: 15 in"))))
    assert shape.volume == pytest.approx(level.volume, rel=0.02)
    assert shape.volume != level.volume
    thin = parse_design(_peaked("55 percent", "2 in"))
    assert any(f.level == "warning" for f in design_frame(thin).findings)


def test_an_offset_peak_is_refused_outside_its_range() -> None:
    with pytest.raises(ValidationError, match="within its span"):
        parse_design(_peaked("100 percent"))
    with pytest.raises(ValidationError, match="quarter circle"):
        parse_design(_peaked("90 percent"))
    with pytest.raises(ValidationError, match="held by masonry"):
        parse_design(_peaked("55 percent").replace("  buttressed: true #", "  buttressed: false #"))
    with pytest.raises(ValidationError, match="arches along the draft"):
        parse_design(_edit("kaneko-car", ("  rise: 14 in", "  rise: 14 in\n  peak_at: 55 percent\n"
                                          "  buttressed: true")))  # fmt: skip


@pytest.mark.geometry
def test_shells_draw_sizes_tapers_and_peaks(tmp_path: Path) -> None:
    flat = _edit("kannofen", ("  type: sprung_arch\n  rise: 0.26 m\n", "  type: flat\n"))
    for text in (_text("ellington-new-hog"), _peaked("55 percent"), flat):
        kiln = parse_design(text)
        written = write_model(kiln, design_report(kiln), tmp_path)
        assert written["gltf"].stat().st_size > 0


# --- The ranges refused -----------------------------------------------------------------------

BIDAI_REFUSED = {
    "straight box chambers": ("  chambers: 3\n", "  chambers: 3\n  bend: 10 degree\n"),
    "front_springline": (
        "  rise: 21 in # chamber 1's",
        "  rise: 21 in\n  front_springline: 30 in #",
    ),
}
FLAT = ("  type: sprung_arch\n  rise: 0.26 m\n", "  type: flat\n")
KANNOFEN_REFUSED = {
    "straight walls": [
        ("heat:\n", "heat:\n  electric:\n    supply: {voltage: 240 V, breaker: 50 A}\n")
    ],
    "a side wall": [
        FLAT,
        ("  face: back\n", "  face: left\n  opening: {width: 0.3 m, height: 0.5 m}\n"),
    ],
}


@pytest.mark.parametrize(("match", "change"), BIDAI_REFUSED.items())
def test_sizes_refused(match: str, change: tuple[str, str]) -> None:
    with pytest.raises(ValidationError, match=match):
        parse_design(_edit("bidai", change))


@pytest.mark.parametrize(("match", "change"), KANNOFEN_REFUSED.items())
def test_widths_refused(match: str, change: list[tuple[str, str]]) -> None:
    with pytest.raises(ValidationError, match=match):
        parse_design(_edit("kannofen", *change))


def test_sizes_under_a_catenary_or_with_elements_are_refused() -> None:
    catenary = _edit("hollyweird", ("  type: dome\n  rise: 12.6 in\n", "  type: catenary_arch\n"))
    with pytest.raises(ValidationError, match="catenary"):
        parse_design(catenary)
    kit = (OLSEN.parent / "electric-front-loader.yaml").read_text(encoding="utf-8")
    assert "  depth:" in kit
    sized = kit.replace(
        "  depth:", "  chambers: 2\n  sizes: [{depth: 10 in}, {depth: 12 in}]\n  depth:", 1
    )
    with pytest.raises(ValidationError, match="fire chambers of different sizes"):
        parse_design(sized)
    taper = kit.replace(
        "  depth:", "  widths: [{at: 0 in, width: 10 in}, {at: 18 in, width: 12 in}]\n  depth:", 1
    )
    with pytest.raises(ValidationError):
        parse_design(taper)


def test_shell_leaves_other_kilns_alone() -> None:
    from kilndesigner.shell import shell_frame, shell_not_drawn

    kyoto = parse_design(_text("kyoto-climbing"))
    assert shell_frame(kyoto) is None
    assert shell_not_drawn(kyoto) is None
    assert widths_of(kyoto, "in") == [(0, 63), (41.33, 63)]
    flat_sized = parse_design(
        _edit(
            "hollyweird", ("  type: dome\n  rise: 12.6 in\n  buttressed: true\n", "  type: flat\n")
        )
    )
    assert sizes_of(flat_sized, "in")[0][2] == 0


def test_a_hung_door_in_a_side_wall_weighs_the_wall() -> None:
    kiln = parse_design(
        _edit("kaneko-car", ("  type: sprung_arch\n  rise: 14 in", "  type: flat\n"),
              ("  type: car\n  face: front\n", "  type: car\n  face: left\n"))
    )  # fmt: skip
    _, area, _ = door_weight(kiln)
    assert area == pytest.approx(108 * 96 / 144)
    front = parse_design(
        _edit("kaneko-car", ("  type: sprung_arch\n  rise: 14 in", "  type: flat\n"))
    )
    assert door_weight(front)[1] == pytest.approx((96 + 14) * 96 / 144)
