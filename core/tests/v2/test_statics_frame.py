"""v2 statics: the steel frame in PyNite coupled to the arch (frame.py), checked against the hand
formulas and the probe (scratch/statics-combos/arch-frame/: frameflex.py, compat.py)."""

import math
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from kilndesigner.designfile import load_design
from kilndesigner.units import Q_, si
from kilndesigner.v2.statics import sources
from kilndesigner.v2.statics.frame import (
    Frame,
    TooHotError,
    angle,
    converge,
    couple,
    flexibility,
    for_kiln,
    hot_steel,
    kiln_coupling,
    rod,
)
from kilndesigner.v2.statics.section import analyse, cross_section

ROOT = Path(__file__).resolve().parents[3]
IN = 0.0254
LBFT = 4.4482216152605 / 0.3048
PSI = 6894.757293168361

# Olsen's fast-fire kiln: L2×2×3/16 angle bolted at the corners (p.139), ½-13 rods; the bay its
# 36 in outside depth, rods across 36 in + both legs, posts from under the 4½ in floor to the
# skewback's top, 39.97 in up (the engine's layout)
FAST_FIRE = Frame(angle("L2×2×3/16"), rod("1/2-13"), 36 * IN, 40 * IN, 44.47 * IN, 2, "p.139")


def test_pynite_meets_the_hand_formulas() -> None:
    """One slice over the whole bay, 1 N spread evenly on each side: the mean of a simple beam's
    deflection under a uniform load, wL⁴/120EI (w = 1/L), plus each post's half share over its
    stiffness, the rod's 2EA/L and the post's cantilever 3EI/h³ in parallel (Derived from the
    beam and bar formulas the probe checked)."""
    steel = hot_steel(70.0)
    f = FAST_FIRE
    e, i = steel.e, f.angle.ix
    k_post = 2 * e * f.rod.stress_area / f.rod_length + 3 * e * i / f.post_height**3
    hand = f.bay**3 / (120 * e * i) + 0.5 / k_post
    c = flexibility(f, np.array([0.0, f.bay]), steel)
    assert c[0, 0] == pytest.approx(hand, rel=1e-3)
    c4 = flexibility(f, np.linspace(0.0, f.bay, 5), steel)
    assert np.allclose(c4, c4.T)
    assert np.all(np.linalg.eigvalsh(c4) > 0)


def test_the_probes_frame_without_crushing() -> None:
    """The probe's 4 slices with the sliding cap of 580.45 lbf/ft (μ 0.50, no crushing): the end
    slices at the cap, the middle ones at 207.8 lbf/ft, the angle at 21.6 ksi."""
    r = couple(FAST_FIRE, 7.076 * LBFT, 580.45 * LBFT, 27 * IN, 0.005, 70.0, 4)
    assert r.h / LBFT == pytest.approx([580.45, 207.8, 207.8, 580.45], abs=0.1)
    assert r.angle_stress / PSI == pytest.approx(21611, rel=2e-3)
    assert r.states[0].startswith("most")
    assert r.states[1].startswith("between")
    assert r.kkt < 1e-9


def test_the_stand_in_cap_converges_along_the_bay() -> None:
    """With the C16 stand-in's cap (176 lbf/ft) every slice of the fast-fire arch reaches the cap
    with the steel cold, so the answer no longer depends on the slicing: the angle at 12.6 ksi
    (wL²/8 on Sx), under A36's 36 ksi, a hair over HarbisonWalker's 12 ksi for hot bindings."""
    cv = converge(FAST_FIRE, 7.080 * LBFT, 176.0 * LBFT, 27 * IN, 0.008, 70.0)
    assert cv.converged
    assert [n for n, _, _ in cv.history] == [4, 8]
    r = cv.result
    assert r.h / LBFT == pytest.approx(176.0)
    hand = 176.0 / 12 * 36**2 / 8 / 0.188  # psi: wL²/8 over Sx
    assert r.angle_stress / PSI == pytest.approx(hand, rel=1e-3)
    assert r.rod_force > 0
    names = [s.name for s in cv.steps]
    assert names[0] == "The frame"
    assert cv.steps[0].note == "p.139"
    assert "12 of" not in cv.steps[3].value


def test_hot_rods_give_the_growth_back() -> None:
    """At 600 °F the rods' own growth, α·ΔT·L/2 = 0.069 in a side, beats the arch's 0.5 %
    (0.068 in): every slice spreads to the least push. At 0.8 % part of the bay holds."""
    lo = 7.080 * LBFT
    r = couple(FAST_FIRE, lo, 176.0 * LBFT, 27 * IN, 0.005, 600.0, 8)
    assert r.h == pytest.approx(lo)
    assert all(s.startswith("least") for s in r.states)
    assert r.growth < 0
    part = converge(FAST_FIRE, lo, 176.0 * LBFT, 27 * IN, 0.008, 600.0)
    assert {s.split(":")[0] for s in part.result.states} >= {"least", "most"}
    assert r.steel.ke == pytest.approx(0.78)


def test_a_post_mid_bay_holds_the_middle() -> None:
    """A third post a side mid-bay, tied across: the buttress is continuous over it, so the angle
    works less than on two posts, the slicing converging all the same."""
    three = Frame(FAST_FIRE.angle, FAST_FIRE.rod, FAST_FIRE.bay, FAST_FIRE.rod_length,
                  FAST_FIRE.post_height, 3)  # fmt: skip
    two = couple(FAST_FIRE, 7.08 * LBFT, 176.0 * LBFT, 27 * IN, 0.008, 70.0, 5)
    held = couple(three, 7.08 * LBFT, 176.0 * LBFT, 27 * IN, 0.008, 70.0, 5)  # post mid-slice
    assert held.angle_stress < two.angle_stress


def test_rigid_brick_loads_the_ends() -> None:
    """No cap (rigid brick, no crushing): the stiff ends of the bay take the growth, more than the
    middle; finer slices load the end strips harder (the probe's divergence)."""
    four = couple(FAST_FIRE, 7.08 * LBFT, math.inf, 27 * IN, 0.005, 70.0, 4)
    assert four.h[0] > four.h[1]
    one = converge(FAST_FIRE, 7.08 * LBFT, math.inf, 27 * IN, 0.005, 70.0, slicings=(4,))
    assert not one.converged
    assert one.steps[3].note == "not converged in the slicings tried"


def test_hot_steel_and_the_tables() -> None:
    hs = hot_steel(1000.0)
    assert (hs.ky, hs.ke) == pytest.approx((0.66, 0.49))
    assert hs.fy / PSI == pytest.approx(36000 * 0.66)
    assert hot_steel(70.0).e / PSI == pytest.approx(29e6)
    with pytest.raises(TooHotError, match="1400"):
        hot_steel(1500.0)
    with pytest.raises(KeyError, match="no angle"):
        angle("L1×1×1/8")
    with pytest.raises(KeyError, match="no rod"):
        rod("1-8")
    with pytest.raises(ValueError, match="post at each end"):
        Frame(angle("L2×2×1/4"), rod("1/2-13"), 1.0, 1.0, 1.0, 1)
    a = angle("L2×2×3/16")
    assert a.area == pytest.approx(0.1875 * (4 - 0.1875) * IN**2)
    assert a.j > 0
    assert sources.growth("ifb-k26") == (0.005, 0.008, sources.IFB_GROWTH)
    dense = sources.growth("firebrick-medium-duty-smithfield")
    assert dense is not None
    assert dense[1] == pytest.approx(3 / 32 / 12)
    assert sources.growth("kast-o-lite-26-li-plus") is None


@pytest.mark.geometry
def test_the_fast_fire_kilns_frame_from_its_section() -> None:
    """for_kiln lays the frame out round the engine's lining; kiln_coupling takes the section's
    cold least and hot most and the ring's growth: the angle near 12.6 ksi at the cap."""
    kiln = load_design(ROOT / "examples" / "olsen" / "fast-fire.yaml")
    xs = cross_section(kiln)
    frame = for_kiln(kiln, xs, "L2×2×3/16", "1/2-13", source="Olsen p.139")
    assert frame.bay == pytest.approx(36 * IN)
    assert frame.rod_length == pytest.approx(40 * IN)
    assert frame.post_height == pytest.approx(4.5 * IN + xs.skewback_top)
    cold, hot = analyse(xs, "cold"), analyse(xs, "hot")
    cv = kiln_coupling(kiln, xs, cold, hot, frame)
    assert cv.converged
    assert si(Q_(cv.result.angle_stress, "Pa"), "psi") == pytest.approx(12636, rel=0.01)
    low = kiln_coupling(kiln, xs, cold, hot, frame, cautious=False)
    assert low.result.angle_stress <= cv.result.angle_stress
    no_growth = replace(xs, ring_material="kast-o-lite-26-li-plus")
    with pytest.raises(ValueError, match="no sourced expansion"):
        kiln_coupling(kiln, no_growth, cold, hot, frame)
