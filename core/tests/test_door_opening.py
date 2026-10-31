"""A door in part of a wall: the model's rules, the hole and the door laid in it, and what spans
it (door.py; door-openings.md, steel-design.md §S5)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from kilndesigner.designfile import load_design, parse_design
from kilndesigner.door import (
    cut_door,
    door_across,
    door_head,
    door_hole,
    door_holes,
    door_thrusts,
    model_door_holes,
)
from kilndesigner.frame import design_frame
from kilndesigner.geometry import lining_parts
from kilndesigner.hardware import build_hardware
from kilndesigner.model import Kiln
from kilndesigner.units import si

EXAMPLES = Path(__file__).parents[2] / "examples"


def _kiln(name: str, loading: dict[str, Any], **change: Any) -> Kiln:
    data = yaml.safe_load((EXAMPLES / name).read_text(encoding="utf-8"))
    data.setdefault("loading", {}).update(loading)
    for key, value in change.items():
        data[key] = value
    return parse_design(yaml.safe_dump(data, allow_unicode=True))


LINTEL = {"opening": {"width": "24 in", "height": "30 in", "head": "lintel", "across": "2 in"}}
ARCH = {"opening": {"width": "20 in", "height": "30 in"}}


def test_whole_wall_doors_are_unchanged() -> None:
    kiln = _kiln("gas-crossdraft.yaml", {})
    assert door_hole(kiln) is None
    assert door_head(kiln) is None
    assert model_door_holes(kiln) == []
    parts = lining_parts(kiln)
    assert cut_door(kiln, parts) == parts
    assert kiln.door_wall == kiln.door_face


def test_the_opening_is_cut_and_the_door_laid_in_it() -> None:
    whole = lining_parts(_kiln("gas-crossdraft.yaml", {}))
    kiln = _kiln("gas-crossdraft.yaml", LINTEL)
    assert kiln.door_wall is None
    parts = lining_parts(kiln)
    plugs = [p for p in parts if p.name.startswith("door/")]
    assert plugs
    # The door takes the bricks the hole took out: the lining's volume is the same
    assert sum(p.volume for p in parts) == pytest.approx(sum(p.volume for p in whole), rel=1e-9)
    hole = door_hole(kiln)
    assert hole is not None
    assert hole.radius == 0
    assert hole.hi[0] - hole.lo[0] == pytest.approx(24 * 25.4)
    assert (hole.lo[0] + hole.hi[0]) / 2 == pytest.approx(2 * 25.4)  # to the right, outside
    assert len(model_door_holes(kiln)) == 1


def test_the_lintel_is_sized_and_its_bearing_left_unchecked() -> None:
    kiln = _kiln("gas-crossdraft.yaml", LINTEL)
    head = door_head(kiln)
    assert head is not None
    assert head.lintel == "L4×4×1/4"
    assert head.length_in == 32
    note = next(f for f in head.findings if f.check is not None)
    assert note.check is not None
    assert note.check.id == "frame.door-lintel"
    assert "isn't checked" in note.message
    frame = design_frame(kiln)
    assert any(m.part == "door lintel" for m in frame.members)
    assert any(s.name == "Steel lintel over the door, hot" for s in frame.working)


def test_a_lintel_too_long_is_refused_with_its_sheet() -> None:
    wide = {"width": "120 in", "depth": "48 in", "height": "40 in"}
    kiln = _kiln(
        "gas-crossdraft.yaml",
        {"opening": {"width": "100 in", "height": "30 in", "head": "lintel"}},
        chamber=wide,
    )
    head = door_head(kiln)
    assert head is not None
    assert head.lintel is None
    refused = next(f for f in head.findings if f.level == "error")
    assert "wider than the 96 in" in refused.message
    assert refused.check is not None
    assert refused.check.id == "frame.door-lintel"


def test_an_arched_door_and_its_jambs_are_checked_by_heymans_statics() -> None:
    kiln = _kiln("gas-crossdraft.yaml", ARCH)
    head = door_head(kiln)
    assert head is not None
    assert head.lintel is None
    assert not [f for f in head.findings if f.level != "info"]
    assert any("holds its least thrust" in f.message for f in head.findings)
    step = next(s for s in head.working if s.name == "The door's arch and jambs")
    assert "Heyman" in (step.note or "")
    hole = door_hole(kiln)
    assert hole is not None
    assert hole.radius == pytest.approx(10 * 25.4)
    assert hole.hi[2] == pytest.approx(20 * 25.4)  # the jambs' top: the arch springs there
    assert len(model_door_holes(kiln)) == 2


def test_a_ring_too_thin_for_its_door_is_refused_with_its_sheet() -> None:
    # A 3 in ring over 26 in: 3/(13 + 1.5) ÷ 0.10743 = 1.93 times the thinnest, under Heyman's 2
    kiln = _kiln("gas-crossdraft.yaml", {"opening": {"width": "26 in", "height": "30 in"}})
    head = door_head(kiln)
    assert head is not None
    refused = next(f for f in head.findings if f.level == "error")
    assert refused.check is not None
    assert refused.check.id == "frame.door-arch"
    assert "1.9 times the thinnest" in refused.message


def test_the_arch_is_checked_for_sliding_at_its_springing(monkeypatch: pytest.MonkeyPatch) -> None:
    kiln = _kiln("gas-crossdraft.yaml", ARCH)
    head = door_head(kiln)
    assert head is not None
    step = next(s for s in head.working if s.name == "The door's arch and jambs")
    assert "needs friction" in step.value
    assert "of 0.6" in step.value
    assert "bonded into the jamb's end is counted" in (step.note or "")
    # With almost no friction it would slide (BIA's 0.60 swapped for 0.01)
    import kilndesigner.frame as frame

    monkeypatch.setattr(frame, "FRICTION", 0.01)
    head = door_head(kiln)
    assert head is not None
    slid = next(f for f in head.findings if f.level == "error")
    assert slid.check is not None
    assert slid.check.id == "frame.door-slide"
    assert "could slide there" in slid.message


def test_a_jamb_too_narrow_for_the_thrust_is_refused() -> None:
    # A 26 in door in a 28 in wall of 2½ in brick: each jamb is the inch beside it and the side
    # wall's 2½ in, and the 4½ in ring's thrust carries the resultant past it
    kx = "hard-firebrick-kx99"
    kiln = _kiln("gas-crossdraft.yaml", {"opening": {"width": "26 in", "height": "30 in"}},
                 lining={"walls": [{"material": kx, "thickness": "2.5 in"}],
                         "roof": [{"material": kx, "thickness": "4.5 in"}]})  # fmt: skip
    head = door_head(kiln)
    assert head is not None
    refused = next(f for f in head.findings if f.level == "error")
    assert refused.check is not None
    assert refused.check.id == "frame.door-jamb"
    assert "3.5 in jamb, outside it" in refused.message
    # A ring standing up past the wall's top doesn't fit
    tall = _kiln("gas-crossdraft.yaml", {"opening": {"width": "26 in", "height": "38 in"}},
                 lining={"walls": [{"material": kx, "thickness": "4.5 in"}],
                         "roof": [{"material": kx, "thickness": "9 in"}]})  # fmt: skip
    head = door_head(tall)
    assert head is not None
    assert any("doesn't fit under the wall's top" in f.message for f in head.findings)


def test_the_least_thrust_is_no_more_than_the_most_in_a_thick_ring() -> None:
    for t in (1.0, 4.5, 9.0):
        least, most = door_thrusts(10.0, 10.0 + t, 10.0 + t, 1.0, 0.0)
        assert 0 < least <= most
    # The roof's load on the wall's top adds to both
    loaded = door_thrusts(10.0, 14.5, 30.0, 1.0, 20.0)
    bare = door_thrusts(10.0, 14.5, 30.0, 1.0, 0.0)
    assert loaded[1] > bare[1]


def test_a_hinged_door_in_part_of_a_wall_hangs_round_the_opening() -> None:
    kiln = _kiln("gas-crossdraft.yaml", {**LINTEL, "door": "hinged"})
    hw = build_hardware(kiln, design_frame(kiln), None)
    frame = next(p for p in hw.pieces if p.name == "door/frame")
    xs = [b[0][0] for b in frame.boxes] + [b[1][0] for b in frame.boxes]
    assert min(xs) == pytest.approx(-10 * 25.4, abs=30)
    assert max(xs) == pytest.approx(14 * 25.4, abs=30)


def test_under_a_dome_the_lintel_carries_the_slices_edge() -> None:
    kiln = _kiln("dome-castable-kiln.yaml", {"opening": {"width": "20 in", "height": "24 in",
                                                         "head": "lintel"}})  # fmt: skip
    head = door_head(kiln)
    assert head is not None
    assert head.lintel is not None
    step = next(s for s in head.working if s.name == "Steel lintel over the door, hot")
    assert step.inputs["roof's edge"] != "0 lb/ft"


@pytest.mark.parametrize(
    ("loading", "words"),
    [
        ({**LINTEL, "type": "car"}, "car's door"),
        ({"opening": {"width": "24 in", "height": "8 in"}}, "semicircular head"),
        ({"opening": {"width": "60 in", "height": "30 in"}}, "doesn't fit"),
        ({"opening": {"width": "20 in", "height": "300 in"}}, "above the wall's inside top"),
        ({"opening": {"width": "0 in", "height": "30 in"}}, "more than 0"),
    ],
)
def test_openings_it_cannot_build_are_refused(loading: dict[str, Any], words: str) -> None:
    with pytest.raises(ValidationError, match=words):
        _kiln("gas-crossdraft.yaml", loading)


def test_a_door_lining_or_electric_kiln_is_refused() -> None:
    data = yaml.safe_load((EXAMPLES / "gas-crossdraft.yaml").read_text(encoding="utf-8"))
    data["lining"]["door"] = data["lining"]["walls"]
    data["loading"] = LINTEL
    text = yaml.safe_dump(data, allow_unicode=True)
    with pytest.raises(ValidationError, match=r"leave out lining\.door"):
        parse_design(text)
    with pytest.raises(ValidationError, match="electric kiln's door"):
        _kiln("electric-front-loader.yaml", LINTEL)


def test_a_hybrids_door_takes_burner_ports_through_its_bricks() -> None:
    # The author's kiln: a 24 × 40 in door in the front wall, eight burner ports in the door
    kiln = parse_design((EXAMPLES / "pnw-hybrid-crossdraft.yaml").read_text(encoding="utf-8"))
    assert kiln.loading.opening is not None
    assert kiln.heat.electric is not None
    assert [p for p in lining_parts(kiln) if p.name.startswith("door/")]
    from kilndesigner.gas import design_gas

    hw = build_hardware(kiln, design_frame(kiln), design_gas(kiln))
    assert not hw.refused
    burners = [p for p in hw.ports if p.kind == "burner"]
    assert len(burners) == 8
    hole = door_hole(kiln)
    assert hole is not None
    for p in burners:
        # Each port lies inside the door, so it is cut through the door's bricks
        assert p.wall == "front"
        assert hole.lo[0] / 25.4 <= p.across - p.width / 2
        assert p.across + p.width / 2 <= hole.hi[0] / 25.4
        assert p.up + p.height / 2 <= 40
    # Elements can't share the door's wall: their grooves run its whole length
    with pytest.raises(ValidationError, match="grooves run the whole front wall"):
        _kiln("pnw-hybrid-crossdraft.yaml", {},
              heat={**yaml.safe_load((EXAMPLES / "pnw-hybrid-crossdraft.yaml").read_text(
                  encoding="utf-8"))["heat"], "electric": {
                  "supply": {"voltage": "240 V", "breaker": "60 A"},
                  "alloy": "kanthal-apm", "walls": ["front"]}})  # fmt: skip


def test_climbing_kilns_take_doors_in_their_side_walls() -> None:
    door = {"width": "20 in", "height": "36 in"}
    side: dict[str, Any] = {"face": "left", "opening": door}
    kiln = _kiln("olsen/bidai.yaml", side)
    assert door_hole(kiln) is not None
    assert door_head(kiln) is not None
    with pytest.raises(ValidationError, match="under a springing"):
        _kiln("olsen/bidai.yaml", {"face": "front", "opening": door})
    with pytest.raises(ValidationError, match="one chamber"):
        _kiln("olsen/bidai.yaml", {**side, "opening": {**door, "across": "20 in"}})


def test_a_row_takes_a_door_into_each_chamber() -> None:
    kiln = _kiln("olsen/bidai.yaml", {})  # Fig 4-36: a 20 in door per chamber, one side wall
    holes = door_holes(kiln)
    assert len(holes) == 3
    # Each the same, at its chamber's front: 10.5 in towards the front of the chamber's middle
    from kilndesigner.run_parts import run_layout

    run = run_layout(kiln)
    for k, hole in enumerate(holes):
        middle = (run.front(k) + run.back(k)) / 2
        assert (hole.lo[1] + hole.hi[1]) / 2 == pytest.approx(middle - 10.5 * 25.4)
    names = {p.name.split("/")[1] for p in lining_parts(kiln) if p.name.startswith("door/")}
    assert names == {"1", "2", "3"}
    assert len(model_door_holes(kiln)) == 6  # a box and a half-round each
    head = door_head(kiln)
    assert head is not None
    assert any(s.name == "A door in each chamber" for s in head.working)
    assert door_across(kiln) == pytest.approx(-10.5)
    hw = build_hardware(kiln, design_frame(kiln), None)
    assert any("one into each chamber" in f.message for f in hw.findings)


@pytest.mark.parametrize(
    ("name", "loading", "words"),
    [
        ("gas-crossdraft.yaml",
         {"opening": {**ARCH["opening"], "each_chamber": True}}, "in a row"),
        ("olsen/bidai.yaml",
         {"opening": {"width": "20 in", "height": "36 in", "across": "15 in",
                      "each_chamber": True}},
         "of chamber 1"),
    ],
)  # fmt: skip
def test_a_door_in_each_chamber_must_be_a_rows_and_fit(
    name: str, loading: dict[str, Any], words: str
) -> None:
    with pytest.raises(ValidationError, match=words):
        _kiln(name, loading)


def test_a_round_kiln_door_breaks_its_ring() -> None:
    kiln = _kiln("olsen/breda-bottle.yaml", LINTEL)
    frame = design_frame(kiln)
    assert any("breaks the round wall's ring" in f.message for f in frame.findings)
    assert door_hole(kiln) is not None


def test_a_catenary_door_must_fit_under_its_curve() -> None:
    with pytest.raises(ValidationError, match="inside top"):
        _kiln("catenary-gas-kiln.yaml", {"opening": {"width": "30 in", "height": "40 in"}})
    kiln = _kiln("catenary-gas-kiln.yaml", ARCH)
    assert door_hole(kiln) is not None


def test_calimpongs_door_reaches_into_its_sail_domes_side() -> None:
    # Fig 4-140: a 33 × 37 in door in the side of walls 35 in tall, under a cast dome
    kiln = _kiln("olsen/conrad-teardrop.yaml", {})
    hole = door_hole(kiln)
    assert hole is not None
    assert (hole.lo[1] + hole.hi[1]) / 2 == pytest.approx(-6 * 25.4)  # 36 to 69 in of the 117
    head = door_head(kiln)
    assert head is not None
    assert not [f for f in head.findings if f.level != "info"]
    assert any(s.name == "The dome over the door's arch" for s in head.working)
    # Past the dome's curve over both jambs it is still refused
    with pytest.raises(ValidationError, match="inside top"):
        _kiln("olsen/conrad-teardrop.yaml",
              {"opening": {"width": "33 in", "height": "45 in", "across": "-6 in"}})  # fmt: skip


def test_a_door_in_a_tubes_side_is_refused_with_its_reason() -> None:
    # Tamba's doors rise through the springing of the tube's vault (Figs 4-11, 4-15)
    with pytest.raises(ValidationError, match="springing of its vault"):
        _kiln("olsen/tamba.yaml", {"face": "left", "opening": {"width": "24 in",
                                                              "height": "36 in"}})  # fmt: skip


def test_spy_holes_go_low_between_burners_up_the_door_sides_and_under_its_arched_head() -> None:
    """The author's door: burners in two columns at ±9 in leave the spy holes' column (3 in
    either side of the middle) clear, so the holes aren't pushed above them (the user: the spy
    holes go lower); the top hole stays a course under the arched head at its outer edge."""
    from kilndesigner.gas import design_gas

    kiln = load_design(Path(__file__).parents[2] / "examples" / "pnw-hybrid-crossdraft.yaml")
    hw = build_hardware(kiln, design_frame(kiln), design_gas(kiln))
    spies = sorted(p.up for p in hw.ports if p.kind == "spy")
    burners = [p.up for p in hw.ports if p.kind == "burner"]
    assert len(spies) == 3
    assert spies[0] < max(burners)  # not stacked above every burner
    door = kiln.loading.opening
    assert door is not None
    r = si(door.width, "in") / 2
    head = si(door.height, "in") - r + math.sqrt(r * r - (3 + 1.125) ** 2)
    assert spies[-1] + 1.25 <= head - 2.5 + 1e-6


CASTABLE = "pnw-hybrid-crossdraft-castable.yaml"


def _castable_door(**opening: Any) -> dict[str, Any]:
    door = {"width": "24 in", "height": "40 in", "sill": "0 in", "head": "arch", **opening}
    return {"opening": door}


def test_a_door_ring_of_its_own_under_a_cast_dome() -> None:
    """The castable PNW kiln: its dome's 2 in shell is too thin a ring for the 24 in door, so the
    door has a 4½ in brick ring arch of its own, laid first and the dome cast over it (Olsen's
    Kanayama and Höhr-Grenzhausen); the dome over it still counts its own shell."""
    kiln = load_design(EXAMPLES / CASTABLE)
    head = door_head(kiln)
    assert head is not None
    assert not [f for f in head.findings if f.level != "info"]
    step = next(s for s in head.working if s.name == "The door's arch and jambs")
    assert step.value.startswith("a 4.5 in ring over 24 in")
    shell = next(s for s in head.working if s.name == "The dome over the door's arch")
    assert "2 in higher" in shell.value  # the dome's shell, not the door's ring

    def depth_source(found: Any) -> str:
        assert found.check is not None
        return next(c.source or "" for c in found.check.cells if c.symbol == "d")

    # Left out, the ring is the roof's: the dome's 2 in shell, too thin for the door
    roofs = door_head(_kiln(CASTABLE, _castable_door()))
    assert roofs is not None
    refused = next(f for f in roofs.findings if f.level == "error")
    assert "thicken the roof's ring" in refused.message
    assert "in exactly the same way as" in depth_source(refused)
    thin = door_head(_kiln(CASTABLE, _castable_door(ring="2 in")))
    assert thin is not None
    refused = next(f for f in thin.findings if f.level == "error")
    assert "deepen the door's ring" in refused.message
    assert "Kanayama" in depth_source(refused)


@pytest.mark.parametrize(
    ("opening", "message"),
    [
        ({"head": "lintel", "ring": "4.5 in"}, "an arched head's"),
        ({"ring": "0 in"}, "more than 0 deep"),
    ],
)
def test_a_door_ring_is_an_arched_heads_and_has_depth(
    opening: dict[str, str], message: str
) -> None:
    with pytest.raises(ValidationError, match=message):
        _kiln(CASTABLE, _castable_door(**opening))
