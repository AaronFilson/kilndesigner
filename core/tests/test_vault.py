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
from kilndesigner.frame import design_frame
from kilndesigner.geometry import in_a_row, inside_top
from kilndesigner.model import Kiln, arches_along
from kilndesigner.shape import chamber_shape
from kilndesigner.units import Q_, si
from kilndesigner.vault import along_statics, stations

BOWEN = Path(__file__).parents[2] / "examples" / "olsen" / "bowen-mountain.yaml"


def _bowen(**change: Any) -> Kiln:
    data = yaml.safe_load(BOWEN.read_text(encoding="utf-8"))
    for key, value in change.items():
        if isinstance(value, dict) and isinstance(data.get(key), dict):
            data[key].update(value)  # pyright: ignore[reportUnknownMemberType]
        else:
            data[key] = value
    return parse_design(yaml.safe_dump(data, allow_unicode=True))


def test_bowen_mountains_vault_is_described_as_built() -> None:
    # Fig 4-153: 5 ft long, 3 ft wide, 18 in at the back wall, 36 in to the crown
    kiln = load_design(BOWEN)
    assert arches_along(kiln)
    assert in_a_row(kiln)
    sections = stations(kiln)
    assert sections[0] == pytest.approx((0.0, 18.0))
    assert sections[-1] == pytest.approx((60.0, 18.0))
    assert max(z for _, z in sections) == pytest.approx(36.0)
    assert sections[len(sections) // 2] == pytest.approx((30.0, 36.0))
    # The side wall rises to the arch: 36 in mid-way, the end walls stand to the springline
    assert inside_top(kiln, "right", 0.0) / 25.4 == pytest.approx(36.0)
    assert inside_top(kiln, "front", 0.0) / 25.4 == pytest.approx(18.0)


def test_bowen_mountains_volume_is_the_box_and_the_arch_along_it() -> None:
    kiln = load_design(BOWEN)
    s, h = 60.0, 18.0  # span and rise, in
    r = (s * s / 4 + h * h) / (2 * h)
    theta = math.atan2(s / 2, r - h)
    segment = r * r * theta - s / 2 * (r - h)
    expected = (60 * 18 + segment) * 36 / 1728  # ft³
    ft3 = si(Q_(1, "ft**3"), "m**3")
    assert chamber_shape(kiln).volume / ft3 == pytest.approx(expected, rel=1e-6)


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
    # The side door reaches up to the arch over both its jambs, not past it
    with pytest.raises(ValidationError, match="inside top"):
        _bowen(loading={"opening": {"width": "24 in", "height": "34 in"}})
