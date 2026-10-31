"""Corbels: TMS 402's projection limits (via BIA), Rhodes's 6 in lintel and 18 in, Olsen's 24 in."""

from __future__ import annotations

import pytest

from kilndesigner.corbel import Corbel, CorbelRefusedError, corbel, corbel_working
from kilndesigner.units import Q_


def test_a_9_in_flue_in_a_9_in_wall() -> None:
    # Dry-laid 2½ in courses: each may step min(1.25, 3) = 1.25 in; 9 in closes to 6 in in 2.
    c = corbel(Q_(9, "in"), Q_(2.5, "in"), Q_(9, "in"))
    assert c.step == pytest.approx(1.25)
    assert c.courses == 2
    assert c.gap == pytest.approx(4.0)
    assert c.rise == pytest.approx(5.0)
    assert c.check().status == "pass"
    working, findings = corbel_working(c)
    assert "2 course(s)" in working[0].value
    assert findings == []


def test_pitelka_s_flue_is_within_the_limits() -> None:
    # Pitelka (door-headers.md [H12]): 9 in flue, the third course 2 in out each side.
    c = Corbel(9.0, 2.5, 9.0, 2 / 3, 3)
    assert c.projection == pytest.approx(2.0)
    assert c.check().status == "pass"


def test_the_whole_corbel_is_limited_to_half_the_wall() -> None:
    # 18 in in a 9 in wall: 6 in a side to leave 6 in, past d/2 = 4.5 in.
    c = corbel(Q_(18, "in"), Q_(2.5, "in"), Q_(9, "in"))
    assert c.check().status == "error"
    _, findings = corbel_working(c)
    assert findings[0].level == "error"


def test_past_rhodes_is_flagged_and_past_olsen_refused() -> None:
    c = corbel(Q_(20, "in"), Q_(2.5, "in"), Q_(31.5, "in"))
    assert c.check().status == "pass"
    _, findings = corbel_working(c)
    assert [f.level for f in findings] == ["info"]
    with pytest.raises(CorbelRefusedError, match="24 in"):
        corbel(Q_(25, "in"), Q_(2.5, "in"), Q_(9, "in"))


def test_too_big_a_step_fails() -> None:
    c = corbel(Q_(9, "in"), Q_(2.5, "in"), Q_(9, "in"), step=Q_(2, "in"))
    assert c.check().status == "error"


def test_refusals() -> None:
    with pytest.raises(CorbelRefusedError):
        corbel(Q_(0, "in"), Q_(2.5, "in"), Q_(9, "in"))
    with pytest.raises(CorbelRefusedError):
        corbel(Q_(9, "in"), Q_(2.5, "in"), Q_(9, "in"), step=Q_(0, "in"))


def test_section_steps() -> None:
    c = corbel(Q_(9, "in"), Q_(2.5, "in"), Q_(9, "in"))
    pts = c.section()
    assert pts[0] == (0.0, 0.0)
    assert pts[-1] == (9.0, 0.0)
    assert (2.5, 5.0) in pts
    assert (6.5, 5.0) in pts
    narrow = corbel(Q_(5, "in"), Q_(2.5, "in"), Q_(9, "in"))
    assert narrow.courses == 0
    assert narrow.section() == [(0.0, 0.0), (5.0, 0.0)]
