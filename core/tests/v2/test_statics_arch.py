"""v2 statics: the rigid-block LP (rigid.py) on a circular arch ring (arch.py), against published
least thicknesses (engine-v2-negative-cases.md §1, N1) and the closed forms of
arch-thrust-theory.md §3."""

import math
from dataclasses import replace

import numpy as np
import pytest

from kilndesigner.v2.statics.arch import (
    ArchRing,
    Overburden,
    least_thickness,
    stands,
    thrust,
)
from kilndesigner.v2.statics.rigid import (
    Body,
    Joint,
    Problem,
    Section,
    Status,
    assemble,
    force_on,
    geometric_factor,
    solve,
)

IN = 0.0254
LBFT = 4.4482216152605 / 0.3048  # N/m in a lb/ft
K23 = 32.0 * 16.018463373960138  # kg/m³: 32.0 pcf (materials.yaml ifb-k23, 513 kg/m³)


def closed_form(ring: ArchRing, r_p: float, y_c: float) -> float:
    """arch-thrust-theory.md §3: H = M_P / (y_c − y_P), per metre run."""
    r, t, phi = ring.radius, ring.thickness, ring.half_angle
    w = ring.density * 9.80665
    m_p = w * (
        r_p * math.sin(phi) * phi * t * (r + t / 2)
        - ((r + t) ** 3 - r**3) * (1 - math.cos(phi)) / 3
    )
    return m_p / (y_c - r_p * math.cos(phi))


def test_n1_a_semicircle_needs_its_least_thickness() -> None:
    """Couplet–Heyman: 0.1075 of the centre line's radius (Milankovitch, as Maia Avelino et al.
    2020 quote it). 160 voussoirs give 0.10746; N1's 3 in ring on meaders-david's 60 in
    half-circle (t/r 0.095) can't stand, 0.11 and 0.22 can."""
    t = least_thickness(1.0, math.pi / 2, 2000.0, 0.6, voussoirs=160)
    assert t == pytest.approx(0.1075, abs=2e-4)
    assert not stands(ArchRing.semicircle(1.0, 0.095, 2000.0, voussoirs=160), 0.6)
    assert stands(ArchRing.semicircle(1.0, 0.11, 2000.0, voussoirs=160), 0.6)
    assert stands(ArchRing.semicircle(1.0, 0.22, 2000.0, voussoirs=160), 0.6)
    assert 0.11 / t == pytest.approx(1.02, abs=0.01)
    assert 0.22 / t == pytest.approx(2.05, abs=0.01)


def test_friction_too_low_and_nothing_stands() -> None:
    """At μ 0.3 the springing joint slides at any thickness up to 0.6 R (statics-software.md §11:
    none up to 0.30); at μ 0.5 the least thickness is unchanged."""
    assert math.isnan(least_thickness(1.0, math.pi / 2, 2000.0, 0.3, voussoirs=40))
    assert least_thickness(1.0, math.pi / 2, 2000.0, 0.5, voussoirs=40) == pytest.approx(
        least_thickness(1.0, math.pi / 2, 2000.0, 0.6, voussoirs=40)
    )


def test_least_and_most_thrust_meet_the_closed_forms() -> None:
    """HarbisonWalker's cell d = 1.608 in/ft, T/S 7 % (4½ in K-23 on 64.3 in): the LP's least and
    most thrust are the closed forms with the hinges at the faces; the heated factor 2.02 (HW
    prints 1.98, within the derivation's 4 %)."""
    span = 4.5 / 0.07 * IN
    ring = ArchRing.from_span_rise(span, 1.608 * span / 12 / IN * IN, 4.5 * IN, K23, voussoirs=80)
    r, t = ring.radius, ring.thickness
    least, most = thrust(ring, 0.6, 1), thrust(ring, 0.6, -1)
    assert least.value == pytest.approx(closed_form(ring, r, r + t), rel=1e-9)
    assert most.value == pytest.approx(closed_form(ring, r + t, r), rel=1e-9)
    cold = closed_form(ring, r + t / 2, r + t / 2)
    assert most.value / cold == pytest.approx(2.02, abs=0.005)
    assert not ring.straight_line_fits


def test_the_fast_fire_arch_has_no_most_thrust_in_rigid_brick() -> None:
    """Olsen's fast-fire arch (27 in span, 1½ in/ft, 4½ in K-23; pp.139–140): R = 28.69 ≤
    (R + T)·cos φ = 29.29 in, so a straight line fits and rigid brick gives no maximum; its least
    thrust is the probe's 11.661 lb/ft (archlp.py at 32.0 pcf)."""
    ring = ArchRing.from_span_rise(27 * IN, 3.375 * IN, 4.5 * IN, K23, voussoirs=320)
    assert ring.straight_line_fits
    assert ring.span == pytest.approx(27 * IN)
    assert ring.rise == pytest.approx(3.375 * IN)
    least = thrust(ring, 0.6, 1)
    assert least.value / LBFT == pytest.approx(11.6612, abs=1e-4)
    hinge = least.solution.joints
    assert hinge[0].e == pytest.approx(-0.5)  # the springing hinges at the intrados
    assert hinge[160].e == pytest.approx(0.5)  # the crown at the extrados
    most = thrust(ring, 0.6, -1)
    assert most.status is Status.UNBOUNDED
    assert most.value == math.inf


def test_load_on_the_ring_and_the_vertical_reaction() -> None:
    ring = ArchRing.from_span_rise(36 * IN, 6.906 * IN, 4.5 * IN, K23, voussoirs=40)
    layer = Overburden(2.5 * IN, K23)
    loaded = replace(ring, overburden=(layer,))
    sec = loaded.section()
    p = Problem(sec, (0.6,) * len(sec.joints))
    down = solve(p, force_on(assemble(p), sec, "support", 1))
    over = (
        layer.density
        * 9.80665
        * 2
        * ring.half_angle
        * (
            (ring.radius + ring.thickness + layer.thickness) ** 2
            - (ring.radius + ring.thickness) ** 2
        )
        / 2
    )
    assert -down.value == pytest.approx(ring.weight + over)
    assert thrust(loaded, 0.6, 1).value > thrust(ring, 0.6, 1).value
    assert replace(loaded, overburden=(Overburden(0.01, 0.0),)).section().bodies[3].loads[0][3] == 0


def test_crushing_caps_the_most_thrust() -> None:
    """With a crushing stress at every joint, the fast-fire arch's most thrust is finite: the
    crown's stress block sits on the intrados, the springings' on the extrados, each just fitting.

    A flat thrust line, the arch's weight neglected, would give σd·2[(R + T)cos φ − R]/(1 +
    cos²φ) = 80 lb/ft at 10 psi (compat.py's cap, Derived). The weight sags the line 0.7 in from
    crown to springing, as much as the ring's 0.6 in of room, so the true cap is about twice that:
    170 lb/ft. It doesn't depend on the voussoirs' count."""
    sigma = 10 * 6894.757  # 10 psi
    ring = ArchRing.from_span_rise(27 * IN, 3.375 * IN, 4.5 * IN, K23, voussoirs=40)
    r, t, c = ring.radius, ring.thickness, math.cos(ring.half_angle)
    flat = 2 * sigma * ((r + t) * c - r) / (1 + c * c)
    most = thrust(ring, 0.6, -1, crush=sigma)
    assert most.status is Status.OPTIMAL
    assert flat / LBFT == pytest.approx(80.37, abs=0.01)
    assert most.value / LBFT == pytest.approx(170.3, abs=0.1)
    joints = most.solution.joints
    for s in (joints[0], joints[20], joints[-1]):  # springings and crown: blocks just fit
        block = s.n / (sigma * ring.depth * t)
        assert 0.5 - abs(s.e) == pytest.approx(block / 2, abs=2e-3)
    assert joints[20].e < 0 < joints[0].e  # crown at the intrados, springing at the extrados
    coarse = ArchRing.from_span_rise(27 * IN, 3.375 * IN, 4.5 * IN, K23, voussoirs=4)
    assert thrust(coarse, 0.6, -1, crush=sigma).value == pytest.approx(most.value, rel=1e-6)
    stronger = thrust(ring, 0.6, -1, crush=2 * sigma)
    assert most.value < stronger.value < 2 * most.value


def test_heymans_geometric_factor_of_safety() -> None:
    """Shrinking every joint about its middle until no thrust line fits: about t/t_least for a
    semicircle (the weight stays the arch's own), 0 if it doesn't stand as built."""
    ring = ArchRing.semicircle(1.0, 0.2, 2000.0, voussoirs=40)
    sec = ring.section()
    gfs = geometric_factor(Problem(sec, (0.6,) * len(sec.joints)))
    assert 1.5 < gfs < 0.2 / 0.1075
    thin = ArchRing.semicircle(1.0, 0.09, 2000.0, voussoirs=40).section()
    assert geometric_factor(Problem(thin, (0.6,) * len(thin.joints))) == 0.0
    free = Section(sec.bodies, sec.joints, sec.depth)
    assert geometric_factor(Problem(free, (math.inf,) * len(sec.joints)), hi=1.2) == 1.2


def test_a_problem_needs_its_conditions() -> None:
    sec = ArchRing.semicircle(1.0, 0.2, 2000.0, voussoirs=4).section()
    with pytest.raises(ValueError, match="friction coefficient for each"):
        Problem(sec, (0.6,))
    with pytest.raises(ValueError, match="crushing stress"):
        Problem(sec, (0.6,) * 5, (None,))
    with pytest.raises(ValueError, match="shrunk"):
        Problem(sec, (0.6,) * 5, shrink=0.5)
    with pytest.raises(ValueError, match="rise"):
        ArchRing.from_span_rise(1.0, 0.6, 0.1, 2000.0)
    with pytest.raises(ValueError, match="half angle"):
        ArchRing(1.0, 0.1, 2.0, 2000.0)
    with pytest.raises(ValueError, match="positive"):
        ArchRing(1.0, -0.1, 1.0, 2000.0)
    with pytest.raises(ValueError, match="two voussoirs"):
        ArchRing(1.0, 0.1, 1.0, 2000.0, voussoirs=1)


def test_a_live_load_factor() -> None:
    """A semicircle (t/R 0.2) under a point load at its crown, λ × its own weight: the load
    factor is finite and grows with the thickness."""

    def factor(t: float) -> float:
        ring = ArchRing.semicircle(1.0, t, 2000.0, voussoirs=40)
        sec = ring.section()
        crown = 20  # the voussoir right of the crown joint
        live = ((crown, 0.0, 1.0, 0.0, -ring.weight),)
        p = Problem(sec, (0.6,) * len(sec.joints), live=live)
        sol = solve(p, _lam(p), -1)
        assert sol.load_factor is not None
        return sol.load_factor

    assert 0 < factor(0.15) < factor(0.25)


def _lam(p: Problem) -> np.ndarray:
    c = np.zeros(assemble(p).nvar)
    c[-1] = 1.0
    return c


def test_a_joint_measures_itself() -> None:
    j = Joint(0, 1, ((0.0, 0.0), (0.3, 0.4)), ((1.0, 0.0), (1.0, 0.0)), 1.0)
    assert j.length == pytest.approx(0.5)
    assert j.middle == pytest.approx((0.15, 0.2))


def test_a_section_by_hand() -> None:
    """A 1 m block of 1 kN on fixed ground, by a planar joint and a curved one (three points,
    no crushing rows: the stand-in applies to planar joints only); a live load on the ground
    is nothing to the ground."""
    ground = Body("ground", 0.0, (0.0, -0.5), fixed=True, tag="ground")
    block = Body("block", 1000.0, (0.0, 0.5), tag="block", loads=((0.5, 1.0, 0.0, -100.0),))
    flat = Joint(0, 1, ((-0.5, 0.0), (0.5, 0.0)), ((0.0, 1.0), (0.0, 1.0)), 1.0)
    bowl = Joint(
        0, 1, ((-0.5, 0.1), (0.0, 0.0), (0.5, 0.1)), ((0.2, 0.98), (0.0, 1.0), (-0.2, 0.98)), 1.0,
        planar=False,
    )  # fmt: skip
    sec = Section((ground, block), (flat, bowl), 1.0)
    assert sec.tagged("block") == [1]
    p = Problem(sec, (0.6, 0.6), (1e5, 1e5), live=((0, 0.0, 0.0, 1.0, 0.0),))
    asm = assemble(p)
    assert asm.b_ub.size == 2 * 5 + 1 + 2 * 16  # friction at 5 points; one joint's crushing
    sol = solve(p)
    assert sol.status is Status.OPTIMAL
    assert sol.load_factor is not None
    plain = solve(Problem(sec, (0.6, 0.6)))
    assert plain.load_factor is None
    assert math.isnan(plain.joints[1].e)  # no place across a curved joint
    up = solve(
        Problem(sec, (0.6, 0.6)), force_on(assemble(Problem(sec, (0.6, 0.6))), sec, "block", 1)
    )
    assert up.value == pytest.approx(1100.0)
    no = solve(Problem(Section((ground, block), (), 1.0), ()))
    assert no.status is Status.INFEASIBLE
    assert math.isnan(no.value)
    assert no.joints == []
    alone = solve(Problem(Section((ground,), (), 1.0), ()))
    assert alone.status is Status.OPTIMAL
