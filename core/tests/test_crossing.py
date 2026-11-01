"""Crossing vaults (roof.crossing): two arched tubes at right angles meeting in a groin, Olsen's
multi-directional kilns (The Kiln Book, 4th ed., Ch. 7, Figs 7-1, 7-2): the geometry against the
Steinmetz solid, the lining, the drawings, the brick counts and each vault's statics."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import pytest
import yaml
from pydantic import ValidationError

from kilndesigner.crossing import crossed, crossing_note, crossing_statics
from kilndesigner.designfile import load_design, parse_design
from kilndesigner.drawings import section_views
from kilndesigner.frame import design_frame
from kilndesigner.geometry import lining_parts, part_solid
from kilndesigner.groin import CrossingShape, GroinLayer, Tube, tubes
from kilndesigner.masonry import plan_masonry
from kilndesigner.model import Kiln
from kilndesigner.report import design_report
from kilndesigner.shape import chamber_shape
from kilndesigner.units import Q_, si

OLSEN = Path(__file__).parents[2] / "examples" / "olsen"
FIREWORKS = OLSEN / "fireworks-edmonton.yaml"
FT3 = si(Q_(1, "ft**3"), "m**3")


def _fireworks(**change: Any) -> Kiln:
    data = yaml.safe_load(FIREWORKS.read_text(encoding="utf-8"))
    for key, value in change.items():
        if isinstance(value, dict) and isinstance(data.get(key), dict):
            data[key].update(value)  # pyright: ignore[reportUnknownMemberType]
        else:
            data[key] = value
    return parse_design(yaml.safe_dump(data, allow_unicode=True))


def _crossing(**change: Any) -> dict[str, Any]:
    out: dict[str, Any] = {"span": "9 ft", "rise": "36 in", "length": "9 ft"}
    out.update(change)
    return out


def _roof(**change: Any) -> dict[str, Any]:
    out: dict[str, Any] = {"type": "sprung_arch", "rise": "24 in", "buttressed": True,
                           "crossing": _crossing()}  # fmt: skip
    out.update(change)
    return out


ARMS = _roof(crossing=_crossing(length="15 ft", at="60 in", span="7 ft", rise="30 in"))
FRONT_ONLY = {
    "fuel": "wood",
    "fireboxes": [{"position": "front", "width": "36 in", "length": "42 in"}],
}


def test_fireworks_is_two_vaults_crossing_at_the_users_heights() -> None:
    kiln = load_design(FIREWORKS)
    assert crossed(kiln)
    chamber, crossing = tubes(kiln, "in")
    # The user's starting heights (2026-10-31): the anagama about 5 ft, the groundhog about 6 ft
    assert chamber.springline + chamber.rise == pytest.approx(60.0)
    assert crossing.springline + crossing.rise == pytest.approx(72.0)
    assert chamber.span == crossing.span == pytest.approx(108.0)  # the 9 ft fire zone
    report = design_report(kiln)
    assert report.errors == []
    messages = " ".join(f.message for f in report.findings)
    assert "The groin, where the two vaults meet over the fire zone, isn't checked" in messages
    assert "Two vaults cross over the fire zone" in messages


def test_a_semicircular_groin_is_the_steinmetz_solid() -> None:
    # Two half-cylinders of radius r over a 2r square: each πr³, their common part half the
    # bicylinder, 8r³/3; each vault's surface 2πr², 4r² of it inside the other
    r, h = 1.0, 0.5
    a = Tube(1, 2 * r, r, h, 0.0, (-r, r), 0.2)
    b = Tube(0, 2 * r, r, h, 0.0, (-r, r), 0.2)
    shape = CrossingShape((a, b))
    assert shape.floor() == pytest.approx(4 * r * r)
    assert shape.perimeter() == pytest.approx(8 * r)
    assert shape.volume(n=1200) == pytest.approx(4 * r * r * h + 2 * math.pi - 8 / 3, rel=2e-4)
    assert shape.vaults() == pytest.approx(4 * math.pi - 8, rel=1e-3)
    # Grown, the floor and walls grow as a box's, the vaults as their circles
    assert shape.floor(0.1) == pytest.approx(2.2**2)
    assert shape.vaults(0.1) > shape.vaults()


def test_the_plan_of_a_crossing_with_arms_is_a_cross() -> None:
    a = Tube(1, 2.0, 1.0, 1.0, 0.0, (-3.0, 3.0), 0.0)
    b = Tube(0, 1.0, 0.5, 1.0, 0.5, (-4.0, 4.0), 0.0)
    shape = CrossingShape((a, b))
    assert shape.floor() == pytest.approx(2 * 6 + 8 * 1 - 2 * 1)
    assert shape.perimeter() == pytest.approx(2 * (6 + 8))


def test_its_faces_and_volume_feed_the_heat_loss() -> None:
    kiln = load_design(FIREWORKS)
    shape = chamber_shape(kiln)
    assert shape.crossing is not None
    faces = {f.face: f for f in shape.faces()}
    assert set(faces) == {"left", "right", "front", "back", "floor", "roof"}
    w, h = 108 * 0.0254, 36 * 0.0254
    assert faces["floor"].inside_area == pytest.approx(w * w)
    # No arms: the side walls are the chamber's, with the crossing's arch over each
    one = CrossingShape(tubes(kiln, "m")).tubes[1].segment_area
    assert faces["left"].inside_area == pytest.approx(w * h + one)
    assert faces["roof"].area_at(0.1) > faces["roof"].inside_area
    assert shape.volume / FT3 == pytest.approx(430.7, abs=0.5)


def test_the_lining_is_the_union_grown_and_the_solids_agree() -> None:
    kiln = _fireworks(roof=ARMS, heat={"fire": FRONT_ONLY})
    parts = lining_parts(kiln)
    names = [p.name for p in parts]
    assert len(names) == len(set(names))
    groin = [p for p in parts if p.groin is not None]
    assert {p.name for p in groin} >= {"roof/1-kast-o-lite-26-li-plus", "left/1-ifb-k26-arch"}
    # The arms' walls run out past the chamber's side walls
    walls = [p for p in parts if p.groin is None and p.face in ("left", "right")]
    assert max(p.hi[0] for p in walls) == pytest.approx((90 + 9) * 25.4)
    note = crossing_note(kiln).message
    assert "arms 36 in out past the side walls" in note


@pytest.mark.geometry
def test_each_layer_of_the_vaults_matches_its_solid() -> None:
    kiln = _fireworks(roof=ARMS, heat={"fire": FRONT_ONLY})
    for p in lining_parts(kiln):
        if p.groin is None:
            continue
        solid = part_solid(p)
        assert solid is not None
        assert solid.volume == pytest.approx(p.volume, rel=5e-3), p.name


def test_the_sections_cut_the_vaults() -> None:
    kiln = _fireworks(roof=ARMS, heat={"fire": FRONT_ONLY})
    front, side, plan = section_views(kiln)
    assert any(r.layer.startswith("roof/") for r in front.rects)
    assert any(r.layer.startswith("roof/") for r in side.rects)
    assert not any(r.layer.startswith("roof/") for r in plan.rects)
    layer = next(p for p in lining_parts(kiln) if p.name.startswith("roof/"))
    assert layer.groin is not None
    from kilndesigner.crossing import groin_cut

    assert groin_cut(layer, 0, 1e6) == []


def test_a_brick_vault_is_counted_with_its_groin_cut_on_site() -> None:
    kiln = _fireworks(lining={"roof": [{"material": "ifb-k26", "thickness": "4.5 in"}]})
    masonry = plan_masonry(kiln).result
    text = " ".join(f.message for f in masonry.findings)
    assert "the groin cut on site" in text
    assert "the end cut to the other vault on site" in text


def test_each_vault_is_checked_as_a_sprung_arch() -> None:
    steps, findings = crossing_statics(load_design(FIREWORKS))
    assert len(steps) == 2
    assert "2.7 times the thinnest" in steps[1].value
    assert [f.level for f in findings] == ["info"]
    # A semicircle over 9 ft in a 6 in ring is too thin; a flat crossing rises too little
    _, found = crossing_statics(_fireworks(roof=_roof(crossing=_crossing(rise="54 in"))))
    assert any("thinnest" in f.message and f.level == "error" for f in found)
    thick = {"walls": [{"material": "ifb-k26", "thickness": "9 in"}] * 2}
    flat = _fireworks(roof=_roof(crossing=_crossing(rise="10 in")), lining=thick)
    _, found = crossing_statics(flat)
    assert any("Olsen's 1½ in/ft" in f.message for f in found)
    frame = design_frame(load_design(FIREWORKS))
    assert any("Heyman's statics" in s.name for s in frame.working)


GAS = {"burners": {"type": "venturi", "wall": "front"}, "supply": {"type": "cylinders", "count": 4}}
FLUE_RIGHT = {"type": "cross", "flue_wall": "right"}
SPY_LEFT = {"places": [{"wall": "left", "up": "12 in"}]}
THIN_WALLS = {"walls": [{"material": "ifb-k26", "thickness": "2.5 in"}]}


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"chamber": {"chambers": 2}}, "one level, straight box chamber"),
        ({"roof": _roof(along=True)}, "leave out tube, along"),
        ({"roof": _roof(buttressed=False)}, "held by masonry"),
        ({"heat": {"gas": GAS}}, "fired with fuel"),
        ({"lining": {"door": [{"material": "ifb-k26", "thickness": "9 in"}]}}, "door"),
        ({"roof": _roof(crossing=_crossing(rise="60 in"))}, "at most half its span"),
        ({"roof": _roof(crossing=_crossing(at="20 in"))}, "within the chamber's"),
        ({"roof": _roof(crossing=_crossing(length="8 ft"))}, "at least the chamber's width"),
        ({"roof": ARMS}, "a firebox can't go in the left wall"),
        ({"roof": ARMS, "heat": {"fire": FRONT_ONLY}, "draft": FLUE_RIGHT}, "the flue can't go"),
        ({"roof": ARMS, "heat": {"fire": FRONT_ONLY}, "spy_holes": SPY_LEFT}, "a spy hole"),
        ({"lining": THIN_WALLS}, "must stand on its walls"),
    ],
)
def test_what_the_engine_refuses(change: dict[str, Any], message: str) -> None:
    with pytest.raises(ValidationError, match=message):
        _fireworks(**change)


def test_a_cap_is_the_wall_under_its_arch_less_the_other_vault() -> None:
    a = Tube(1, 2.0, 1.0, 0.0, 0.0, (-1.0, 1.0), 0.2)
    b = Tube(0, 2.0, 0.5, 0.0, 0.0, (-1.0, 1.0), 0.2)
    cap = GroinLayer((a, b), 0.0, 0.0, cap=0, shell=0.1)
    # The front wall's cap: the chamber's semicircle, less the crossing's lower vault and ring
    lo, hi = (-1.0, -1.2, 0.0), (1.0, -1.0, 1.0)
    whole = math.pi / 2 * 0.2
    assert 0 < cap.volume(lo, hi) < whole
    bottom, top = cap.intervals(np.array([0.0]), np.array([-1.1]))[0]
    assert top[0] == pytest.approx(1.0, abs=1e-3)
    assert bottom[0] > 0.0
