"""Vaults whose section changes along the chamber: one chamber's arch spanning its depth (Olsen's
Bowen Mountain salt kiln, Fig 4-153; roof.along), its section at stations and its statics
(vault.py, Heyman's, as door arches')."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pytest
import yaml
from pydantic import ValidationError

from kilndesigner.designfile import load_design, parse_design
from kilndesigner.frame import cold_thrust_factor, design_frame
from kilndesigner.geometry import in_a_row, inside_top, lining_parts
from kilndesigner.model import Kiln, arches_along
from kilndesigner.shape import Arch, along_arch, chamber_shape
from kilndesigner.units import Q_, si
from kilndesigner.vault import (
    along_inputs,
    along_statics,
    door_in_vault,
    stations,
    thrust_line_thrust,
    uneven_thrust,
)

BOWEN = Path(__file__).parents[2] / "examples" / "olsen" / "bowen-mountain.yaml"


def _bowen(**change: Any) -> Kiln:
    data = yaml.safe_load(BOWEN.read_text(encoding="utf-8"))
    for key, value in change.items():
        if isinstance(value, dict) and isinstance(data.get(key), dict):
            data[key].update(value)  # pyright: ignore[reportUnknownMemberType]
        else:
            data[key] = value
    return parse_design(yaml.safe_dump(data, allow_unicode=True))


LEVEL = {"rise": "18 in", "front_springline": None}


def test_bowen_mountains_vault_is_described_as_built() -> None:
    # Fig 4-153: 5 ft long, 3 ft wide, 18 in at the back wall, about 16 in at the front, 36 in to
    # the crown
    kiln = load_design(BOWEN)
    assert arches_along(kiln)
    assert in_a_row(kiln)
    sections = stations(kiln)
    assert sections[0] == pytest.approx((0.0, 16.0))
    assert sections[-1] == pytest.approx((60.0, 18.0))
    # The crown, 36 in up, stands a little behind the middle
    arch = along_arch(kiln, "in")
    assert arch.offset > 0
    assert 18 + arch.height(arch.offset) == pytest.approx(36.0)
    # The side wall rises to the arch, the end walls stand to their own springlines
    assert inside_top(kiln, "right", arch.offset * 25.4) / 25.4 == pytest.approx(36.0)
    assert inside_top(kiln, "front", 0.0) / 25.4 == pytest.approx(16.0)
    assert inside_top(kiln, "back", 0.0) / 25.4 == pytest.approx(18.0)


def test_a_level_vault_is_the_box_and_the_arch_along_it() -> None:
    kiln = _bowen(roof=LEVEL)
    sections = stations(kiln)
    assert sections[0] == pytest.approx((0.0, 18.0))
    assert sections[len(sections) // 2] == pytest.approx((30.0, 36.0))
    s, h = 60.0, 18.0  # span and rise, in
    r = (s * s / 4 + h * h) / (2 * h)
    theta = math.atan2(s / 2, r - h)
    segment = r * r * theta - s / 2 * (r - h)
    expected = (60 * 18 + segment) * 36 / 1728  # ft³
    ft3 = si(Q_(1, "ft**3"), "m**3")
    assert chamber_shape(kiln).volume / ft3 == pytest.approx(expected, rel=1e-6)


def test_an_uneven_arch_is_the_circle_through_both_springings() -> None:
    arch = Arch(60.0, 18.0, 2.0)
    r = arch.radius
    # Both springings and the crown lie on the circle
    assert arch.height(-30.0) == pytest.approx(-2.0)
    assert arch.height(30.0) == pytest.approx(0.0, abs=1e-9)
    assert arch.height(arch.offset) == pytest.approx(18.0)
    assert r * math.sin(arch.front_angle) + r * math.sin(arch.back_angle) == pytest.approx(60.0)
    # The area under the back's springline, by the arc's own integral
    n = 20000
    du = 60.0 / n
    area = sum(arch.height(-30.0 + (i + 0.5) * du) for i in range(n)) * du
    assert arch.segment_area == pytest.approx(area, rel=1e-6)
    assert arch.arc_length == pytest.approx(r * (arch.front_angle + arch.back_angle))
    # Level, it is the level arch
    level = Arch(60.0, 18.0)
    assert Arch(60.0, 18.0, 0.0).radius == level.radius
    assert level.front_angle == level.back_angle == level.half_angle
    # A springing higher at the front is the mirror image
    mirror = Arch(60.0, 20.0, -2.0)
    assert mirror.radius == pytest.approx(r)
    assert mirror.front_angle == pytest.approx(arch.back_angle)


def test_bowen_mountains_volume_is_the_box_and_the_uneven_arch_over_it() -> None:
    kiln = load_design(BOWEN)
    arch = along_arch(kiln, "in")
    expected = (60 * 18 + arch.segment_area) * 36 / 1728  # ft³
    ft3 = si(Q_(1, "ft**3"), "m**3")
    assert chamber_shape(kiln).volume / ft3 == pytest.approx(expected, rel=1e-6)
    assert expected < 38.5  # the level vault's, 18 in at both ends


def test_the_uneven_arch_is_laid_out_from_each_springline() -> None:
    kiln = load_design(BOWEN)
    parts = {p.name: p for p in lining_parts(kiln)}
    assert parts["front/1-ifb-jm28"].hi[2] == pytest.approx(16 * 25.4)
    assert parts["back/1-ifb-jm28"].hi[2] == pytest.approx(18 * 25.4)
    assert parts["left/1-ifb-jm28"].hi[2] == pytest.approx(16 * 25.4)
    assert parts["front/skewback-ifb-jm28-chamber-1"].lo[2] == pytest.approx(16 * 25.4)
    assert parts["back/skewback-ifb-jm28-chamber-1"].lo[2] == pytest.approx(18 * 25.4)
    ring = parts["roof/1-ifb-jm28-chamber-1"]
    assert ring.arch is not None
    assert ring.hi[2] == pytest.approx((36 + 9) * 25.4, abs=0.5)
    cap = parts["right/1-ifb-jm28-chamber-1-arch"]
    assert cap.profile is not None
    assert min(z for _, z in cap.profile) == pytest.approx(16 * 25.4)


def test_a_thrust_line_through_both_springings_agrees_with_the_halves() -> None:
    kiln = load_design(BOWEN)
    arch = along_arch(kiln, "in")
    assert arch.drop == pytest.approx(2.0)
    for a in (arch, Arch(arch.span, arch.rise, -3.0), Arch(60.0, 18.0, 4.0)):
        h, front, back = thrust_line_thrust(a, 100.0)
        assert (h, front, back) == pytest.approx(uneven_thrust(a, 100.0))
        assert front + back == pytest.approx(100.0)
    # by hand, Arch(60, 18, 4): the back half about the crown holds with that H
    a = Arch(60.0, 18.0, 4.0)
    h, _, back = thrust_line_thrust(a, 100.0)
    pb = a.back_angle
    wb = 100.0 * pb / (a.front_angle + pb)
    fb = 1 - math.cos(pb)
    assert back * math.sin(pb) == pytest.approx(h * fb + wb * fb / pb)
    frame = design_frame(kiln)
    [step] = [s for s in frame.working if s.name.startswith("The uneven arch's cold thrust")]
    assert "each half about the crown" in step.value
    assert "largest printed factor is kept" in (step.note or "")


def test_the_uneven_arch_springs_each_end_wall_on_its_own_share() -> None:
    kiln = load_design(BOWEN)
    working, findings = along_statics(kiln)
    walls = [f for f in findings if f.check and f.check.id.startswith("frame.vault-end-wall")]
    assert [f.message.split(",")[0] for f in walls] == ["The front wall", "The back wall"]
    arch = along_arch(kiln, "in")
    _, front, back = uneven_thrust(arch, 100.0)
    assert front + back == pytest.approx(100.0)
    assert front > back  # the front half, turning the larger angle, is the heavier
    level = Arch(60.0, 18.0)
    h0, f0, b0 = uneven_thrust(level, 100.0)
    assert f0 == pytest.approx(50.0)
    assert b0 == pytest.approx(50.0)
    assert h0 == pytest.approx(cold_thrust_factor(60.0, 18.0) * 100.0)
    statics = next(s for s in working if s.name.startswith("The arch along the depth"))
    assert "on the front wall" in statics.value
    assert statics.note is not None
    assert "cut off at the higher springing" in statics.note
    frame = design_frame(kiln)
    thrust = next(s for s in frame.working if s.name == "Thrust on each end wall")
    assert thrust.note is not None
    assert "largest printed factor" in thrust.note
    with pytest.raises(ValidationError, match="past a quarter circle"):
        _bowen(roof={"front_springline": "2 in", "rise": "30 in"})
    with pytest.raises(ValidationError, match="below its crown"):
        _bowen(roof={"front_springline": "40 in"})
    with pytest.raises(ValidationError, match="more than 0"):
        _bowen(roof={"front_springline": "0 in"})
    with pytest.raises(ValidationError, match="front_springline is for one chamber"):
        _bowen(roof={"front_springline": "16 in", "along": False}, loading={"face": "front"})


def test_bowen_mountains_door_rises_into_the_vault() -> None:
    kiln = load_design(BOWEN)
    into = door_in_vault(kiln)
    assert into is not None
    assert into.springing == pytest.approx(24.0)
    # The vault meets the side wall about 33.8 in up at the jambs; the head's crown just reaches
    # the vault's inside, and its ring the vault's outside
    assert min(into.jamb_tops) == pytest.approx(33.6, abs=0.1)
    assert into.cut < 0.1
    assert 8.9 < into.ring <= 9.0
    frame = design_frame(kiln)
    assert any(s.name == "The door's head in the vault's edge" for s in frame.working)
    door = [f for f in frame.findings if "The door is arched" in f.message]
    assert door
    assert "times the thinnest" in door[0].message
    assert not [f for f in frame.findings if f.level == "error"]
    statics = next(s for s in frame.working if s.name.startswith("The arch along the depth"))
    assert statics.note is not None
    assert "The door:" in statics.note


def test_a_door_into_the_vault_is_refused_where_nothing_covers_it() -> None:
    # A flat head into the vault: no lintel statics under a vault's edge
    with pytest.raises(ValidationError, match="laid out arched"):
        _bowen(loading={"opening": {"width": "24 in", "height": "34 in", "head": "flat"}})
    # Jambs rising past the vault's inside
    with pytest.raises(ValidationError, match="jambs"):
        _bowen(loading={"opening": {"width": "24 in", "height": "46 in"}})
    # A head cutting through the vault's ring
    with pytest.raises(ValidationError, match="cut through"):
        _bowen(loading={"opening": {"width": "40 in", "height": "46 in"}})
    # Under the vault, the door's ring keeps clear of it: no head in the vault
    assert door_in_vault(_bowen(loading={"opening": {"width": "24 in", "height": "26 in"}})) is None


def test_a_door_cut_into_the_vault_checks_the_thinner_ring() -> None:
    kiln = _bowen(roof=LEVEL, loading={"opening": {"width": "20 in", "height": "37 in"}})
    into = door_in_vault(kiln)
    assert into is not None
    assert into.cut > 0.5
    thinner = along_inputs(kiln, into.cut)
    whole = along_inputs(kiln)
    assert thinner.layers[0].thickness == pytest.approx(9.0 - into.cut)
    assert thinner.rise > whole.rise  # the ring's inside moved out by the cut
    _, findings = along_statics(kiln)
    assert not [f for f in findings if f.level == "error"]


def test_bowen_mountains_arch_stands_and_needs_its_bracing() -> None:
    kiln = load_design(BOWEN)
    working, findings = along_statics(kiln)
    assert not [f for f in findings if f.level != "info"]
    statics = next(s for s in working if s.name.startswith("The arch along the depth"))
    assert "times the thinnest that stands" in statics.value
    end = next(f for f in findings if f.check and f.check.id.startswith("frame.vault-end-wall"))
    # The 9 in end wall alone can't hold even the cold thrust: the drawn bracing carries it
    assert end.check is not None
    assert end.check.status == "error"
    assert "needed, not optional" in end.message
    frame = design_frame(kiln)
    assert frame.members == []
    assert any(s.name == "The chamber's section along its depth" for s in frame.working)


def test_a_thick_end_wall_holds_the_arch_alone() -> None:
    wall = {"material": "ifb-jm28", "thickness": "9 in"}
    kiln = _bowen(lining={"walls": [wall, wall, wall]})
    _, findings = along_statics(kiln)
    end = next(f for f in findings if f.check and f.check.id.startswith("frame.vault-end-wall"))
    assert end.check is not None
    assert end.check.status == "pass"
    assert "holds the arch's cold thrust" in end.message


def test_a_ring_too_thin_for_its_arch_is_an_error() -> None:
    thin = {"material": "ifb-jm28", "thickness": "1 in"}
    wall = {"material": "ifb-jm28", "thickness": "9 in"}
    kiln = _bowen(lining={"walls": [wall], "roof": [thin, wall]})
    _, findings = along_statics(kiln)
    errors = [f for f in findings if f.level == "error"]
    assert errors
    assert errors[0].check is not None
    assert errors[0].check.id.startswith("frame.vault-ring")


def test_one_chambers_arch_along_is_validated() -> None:
    with pytest.raises(ValidationError, match="at most half its span, the chamber's depth"):
        _bowen(roof={"rise": "31 in"})
    with pytest.raises(ValidationError, match="leave out along, or tube"):
        _bowen(roof={"tube": True})
    with pytest.raises(ValidationError, match="along the draft already"):
        _bowen(chamber={"chambers": 2})
    # A lintel's door reaches up to the arch over both its jambs, not past it
    with pytest.raises(ValidationError, match="inside top"):
        _bowen(loading={"opening": {"width": "24 in", "height": "34 in", "head": "lintel"}})
