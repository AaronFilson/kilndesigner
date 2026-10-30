"""A door in part of a wall: the model's rules, the hole and the door laid in it, and what spans
it (door.py; door-openings.md, steel-design.md §S5)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from kilndesigner.designfile import parse_design
from kilndesigner.door import cut_door, door_head, door_hole, model_door_holes
from kilndesigner.frame import design_frame
from kilndesigner.geometry import lining_parts
from kilndesigner.hardware import build_hardware
from kilndesigner.model import Kiln

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


def test_an_arched_door_is_laid_out_not_checked() -> None:
    kiln = _kiln("gas-crossdraft.yaml", ARCH)
    head = door_head(kiln)
    assert head is not None
    assert head.lintel is None
    assert any("aren't checked" in f.message for f in head.findings)
    hole = door_hole(kiln)
    assert hole is not None
    assert hole.radius == pytest.approx(10 * 25.4)
    assert hole.hi[2] == pytest.approx(20 * 25.4)  # the jambs' top: the arch springs there
    assert len(model_door_holes(kiln)) == 2


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


def test_climbing_kilns_take_doors_in_their_side_walls() -> None:
    door = {"width": "20 in", "height": "36 in"}
    side: dict[str, Any] = {"face": "left", "opening": door}
    kiln = _kiln("olsen/bidai.yaml", side)
    assert door_hole(kiln) is not None
    assert door_head(kiln) is not None
    with pytest.raises(ValidationError, match="under a springing"):
        _kiln("olsen/bidai.yaml", {"opening": {"width": "20 in", "height": "36 in"}})
    with pytest.raises(ValidationError, match="one chamber"):
        _kiln("olsen/bidai.yaml", {**side, "opening": {**door, "across": "20 in"}})


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
