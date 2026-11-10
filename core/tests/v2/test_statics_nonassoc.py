"""v2 statics: non-associative friction by HiGHS's MILP (nonassoc.py), on the survey's cases
(statics-software.md §11, statics-combinations.md §3: test inputs, γ 20 kN/m³, μ 0.6, a 9 in wall
1.2 m high, the thrust 0.9 m up with 6 kN/m on the wall), and a kiln's walls (section.py)."""

import math
from dataclasses import replace
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from scipy.optimize import milp as real_milp

from kilndesigner.designfile import load_design
from kilndesigner.v2.statics import nonassoc
from kilndesigner.v2.statics.nonassoc import Mode, TooLargeError, collapse
from kilndesigner.v2.statics.rigid import Body, Joint, Problem, Section
from kilndesigner.v2.statics.section import analyse, cross_section, wall_capacity

ROOT = Path(__file__).resolve().parents[3]
GAMMA = 20000.0  # N/m³
B9 = 0.2286
HEIGHT, AT, V = 1.2, 0.9, 6000.0
LBFT = 4.4482216152605 / 0.3048


def block(name: str, x0: float, x1: float, z0: float, z1: float, loads: Any = ()) -> Body:
    return Body(name, GAMMA * (x1 - x0) * (z1 - z0), ((x0 + x1) / 2, (z0 + z1) / 2), loads=loads)


def case(buttress: bool, courses: int = 1) -> Problem:
    """A1 (one wall block) or C (a buttress block dry-laid against it); ``courses`` stacks the
    wall instead."""
    bodies = [Body("ground", 0.0, (0.0, -0.1), True, "ground")]
    joints: list[Joint] = []
    h = HEIGHT / courses
    for k in range(courses):
        loads = ((B9 / 2, AT, 0.0, -V),) if k == courses - 1 else ()
        bodies.append(block(f"wall {k}", 0.0, B9, k * h, (k + 1) * h, loads))
        joints.append(Joint(k, k + 1, ((0.0, k * h), (B9, k * h)), ((0.0, 1.0),) * 2, 1.0))
    top = courses
    if buttress:
        bodies.append(block("buttress", B9, 2 * B9, 0.0, HEIGHT))
        b = len(bodies) - 1
        joints.append(Joint(0, b, ((B9, 0.0), (2 * B9, 0.0)), ((0.0, 1.0),) * 2, 1.0))
        joints.append(Joint(1, b, ((B9, 0.0), (B9, HEIGHT)), ((1.0, 0.0),) * 2, 1.0))
    sec = Section(tuple(bodies), tuple(joints), 1.0)
    return Problem(sec, (0.6,) * len(joints), live=((top, 0.0, AT, 1.0, 0.0),))


def test_a_lone_wall_collapses_alike_either_way() -> None:
    """A1: one block, statically determinate: the LP and the MILP both 1.45877 kN/m, the base
    overturning about its toe, (V + W)·(b/2)/h_s."""
    c = collapse(case(False))
    hand = (V + GAMMA * B9 * HEIGHT) * (B9 / 2) / AT
    assert c.lp == pytest.approx(hand, rel=1e-6)
    assert c.least == pytest.approx(hand, rel=1e-6)
    assert c.proven
    assert c.modes == (Mode.OPEN, Mode.STICK)
    assert c.binaries == 6
    assert c.box_used < 1.0


def test_a_dry_laid_buttress_collapses_below_the_lp() -> None:
    """C: the LP gives 2.93941 kN/m; the least non-associative collapse is 2.24546 (−23.6 %),
    both blocks rocking on their toes and the joint between them sliding (statics-combinations.md
    §3; the hand form P = W₂(b/2)/(h − μb), H = ((W₁ + V)b/2 + Ph)/h_s)."""
    c = collapse(case(True))
    w = GAMMA * B9 * HEIGHT
    p = w * (B9 / 2) / (HEIGHT - 0.6 * B9)
    assert c.lp / 1000 == pytest.approx(2.93941, abs=1e-5)
    assert c.least == pytest.approx(((w + V) * B9 / 2 + p * HEIGHT) / AT, rel=1e-6)
    assert c.least / 1000 == pytest.approx(2.24546, abs=1e-5)
    assert c.proven
    assert c.modes[-2:] == (Mode.SLIDE_PLUS, Mode.SLIDE_PLUS)  # the interface slides
    assert c.velocities is not None
    assert c.forces is not None
    keyed = collapse(replace(case(True), mu=(math.inf, math.inf, 0.6)))  # the beds can't slide
    assert keyed.least <= keyed.lp
    assert keyed.least >= c.least - 1e-6


def test_what_the_milp_wont_take() -> None:
    plain = case(False)
    with pytest.raises(ValueError, match="live load"):
        collapse(Problem(plain.section, plain.mu))
    with pytest.raises(TooLargeError, match="course-level"):
        collapse(case(False, courses=101))
    down = Problem(plain.section, plain.mu, live=((1, B9 / 2, HEIGHT, 0.0, -1.0),))
    with pytest.raises(ValueError, match="no finite collapse"):
        collapse(down)


def test_when_highs_doesnt_finish(monkeypatch: pytest.MonkeyPatch) -> None:
    """No state in the time: the LP's load stands as the upper bound; a state not proven least
    is reported with HiGHS's dual bound; a mode pattern the plain LPs can't redo keeps the
    MILP's own values."""

    def unfinished(*args: Any, **kwargs: Any) -> Any:
        res = real_milp(*args, **kwargs)
        return SimpleNamespace(x=res.x, status=1, message="time limit", mip_dual_bound=2000.0)

    def nothing(*args: Any, **kwargs: Any) -> Any:
        return SimpleNamespace(x=None, status=1, message="time limit", mip_dual_bound=None)

    def no_lp(*args: Any, **kwargs: Any) -> Any:
        return SimpleNamespace(status=2, x=None)

    monkeypatch.setattr(nonassoc, "milp", unfinished)
    c = collapse(case(True))
    assert not c.proven
    assert c.bound == 2000.0
    assert c.least / 1000 == pytest.approx(2.24546, abs=1e-5)
    monkeypatch.setattr(nonassoc, "milp", nothing)
    none = collapse(case(True))
    assert none.least == none.lp
    assert none.modes == ()
    assert not none.proven
    monkeypatch.setattr(nonassoc, "milp", real_milp)
    monkeypatch.setattr(nonassoc, "linprog", no_lp)
    raw = collapse(case(True))
    assert raw.least / 1000 == pytest.approx(2.24546, abs=1e-3)


@pytest.mark.geometry
def test_a_kilns_wall_alone_under_the_arch() -> None:
    """The fast-fire kiln's right wall at the least-frame state: the arch pushes 11.6 lbf/ft; the
    wall alone takes 4.3 (one column of courses: the LP and the MILP agree), so the frame must
    give 7.3; the section's joint optimum is 7.08. meaders-david's arch springs from the ground:
    no wall."""
    olsen = ROOT / "examples" / "olsen"
    xs = cross_section(load_design(olsen / "fast-fire.yaml"))
    w = wall_capacity(xs, analyse(xs, "cold"), "right")
    assert w is not None
    assert w.push / LBFT == pytest.approx(11.6, abs=0.1)
    assert w.lp / LBFT == pytest.approx(4.3, abs=0.1)
    assert w.least == pytest.approx(w.lp, rel=1e-6)
    assert w.proven
    assert w.support_needed / LBFT == pytest.approx(7.3, abs=0.1)
    assert w.steps[0].note is None
    hot = wall_capacity(xs, analyse(xs, "hot"), "left")
    assert hot is not None
    assert hot.steps[0].note is not None
    md = cross_section(load_design(olsen / "meaders-david.yaml"))
    assert wall_capacity(md, analyse(md, "cold"), "right") is None
