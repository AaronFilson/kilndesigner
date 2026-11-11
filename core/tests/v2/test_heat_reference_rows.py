"""Part C3b: the rows, the climbing and multi-chamber reference kilns fired in stages on their own
draft (`row_cases.py`: each stage on its own path, max fire or held to the book's time), each
printed heat figure against v2's band (ADR 0017 decision 17; `docs/planning/11-10-26.md`, "C3b as
built", the results table).

The owner's rule (2026-11-10): the reference kilns all worked as built, and the model has to let
them stand. A figure inside v2's band stands; one outside is an open item (a strict xfail), traced
to its inputs or the missing physics, its question in the plan doc. Nothing is fitted.

**Stoked times are inequalities** (problem set §2.2, §6): max fire is the fastest a stage's draft
lets it go, so a printed time stands where v2's max fire is no slower somewhere in its band (the
band's least), and a printed fuel stands where it is no less than v2's least.
"""

from __future__ import annotations

import math

import numpy as np
import pytest
import row_cases as rc

from kilndesigner.cones import cone_temperature
from kilndesigner.units import si

pytestmark = [pytest.mark.slow, pytest.mark.geometry]
HOUR = 3600.0


def _stands(kid: str, result: str, book: float) -> None:
    """A printed time (or fuel) inside v2's band of max fire: no faster than its least."""
    b = rc.band(kid)[result]
    assert b.low <= book, f"{kid}: {result} {b.low:.3g}–{b.high:.3g} (nominal {b.nominal:.3g})"


# --- T1: every row reaches its cones in stages, on its own draft ---------------------------------


@pytest.mark.parametrize("kid", rc.ROWS)
def test_each_chamber_reaches_its_cone_in_stages_on_its_own_draft(kid: str) -> None:
    """T1 (problem set §6): the front's stage and then each chamber's, each as hard as its own
    path draws, bring every chamber to its cone somewhere in v2's band. Kitade on Olsen's Rule 6
    chimney (C1's question 8, built here as the other C3 agent builds it) only at the draft's
    most-air end: at the band's middle its setting levels off near 1170 °C."""
    assert math.isfinite(rc.band(kid)[rc.FIRING].low)


# --- Suzuki's cooperative kiln (p.93) ----------------------------------------------------------

SUZUKI = rc.PLANS["suzuki-kyoto"]


@pytest.mark.parametrize("phase", SUZUKI.phases, ids=lambda p: p.name)
def test_suzuki_each_stage_inside_its_printed_time(phase: rc.Phase) -> None:
    """p.93: the firebox 15 h to 1000 °C, then 7 h each for chambers 1–3 and 5 h each for 4–7: no
    stage of v2's max fire is slower somewhere in its band."""
    assert phase.book is not None
    _stands("suzuki-kyoto", f"{phase.name} (h)", phase.book)


def test_suzuki_fires_inside_56_h() -> None:
    """p.93: "approximately 56 hours to fire a chamber kiln of seven chambers"."""
    _stands("suzuki-kyoto", rc.FIRING, 56.0)


@pytest.mark.parametrize("chamber", range(7))
def test_suzuki_each_chamber_reaches_its_printed_cone(chamber: int) -> None:
    """Fig 4-35: cone 10 in chambers 1 and 2, 8–9 in 3 to 6 (9 taken, the hotter, as the design),
    bisque cone 1 in chamber 7: each reached in its stage (the band's nominal run)."""
    s = rc.run("suzuki-kyoto", rc.NOMINAL)  # called as the band calls it: its cached run
    assert s is not None
    peak = float(s.firing.t_settings[:, chamber].max())
    assert peak >= rc.cones("suzuki-kyoto")[chamber] - 1e-3


def test_suzuki_the_kiln_reaches_cone_8_to_9() -> None:
    """p.93's text: the kiln to cone 8–9: every chamber but the bisque one at least cone 8."""
    s = rc.run("suzuki-kyoto", rc.NOMINAL)  # called as the band calls it: its cached run
    assert s is not None
    cone_8 = si(cone_temperature("8", 60), "K")
    assert np.all(s.firing.t_settings[:, :6].max(axis=0) >= cone_8)


def test_suzuki_the_cone_falls_along_the_kiln() -> None:
    """T5, Fig 4-35's evenness: "each chamber is side-stoked to its own temperature", the cone
    falling along the kiln: no chamber driven past its own by the stages before it (its peak
    under the next cone up), so the peaks fall as the printed cones do."""
    s = rc.run("suzuki-kyoto", rc.NOMINAL)  # called as the band calls it: its cached run
    assert s is not None
    peaks = s.firing.t_settings.max(axis=0)
    nxt = [si(cone_temperature(c, 60), "K") for c in ("11", "11", "10", "10", "10", "10", "2")]
    assert np.all(peaks < np.array(nxt))
    assert np.all(np.diff(peaks) <= 1e-3)


def test_suzuki_burns_its_bundles_in_chambers_1_to_3() -> None:
    """T3, p.93: about 75 bundles a side for each of chambers 1–3 over their 7 h, 450 in all
    (derived), at a bundle's stated band (the dataset's `fuel_unit_mass`: packed as a cord is
    stacked, an assumption): no less than v2 needs held to the printed stage times at the stoker's
    λ 1, the least air (the book fires them in reduction, λ under 1: more wood for the heat), even
    at the light end of a bundle's band."""
    lo, _ = rc.bundle("suzuki-kyoto")
    b = rc.held_band("suzuki-kyoto")[rc.SIDE_FUEL]
    assert b.low <= 450 * lo / 1e3


@pytest.mark.parametrize("chamber", range(3))
def test_suzuki_burns_75_bundles_a_side_in_each_of_chambers_1_to_3(chamber: int) -> None:
    """T3, p.93: "approximately 75 bundles per side and seven hours" for each reduction chamber:
    150 bundles each, no less than v2's held run burns in that chamber's 7 h at the stoker's λ 1,
    even at the light end of a bundle's band."""
    lo, _ = rc.bundle("suzuki-kyoto")
    s = rc.run("suzuki-kyoto", rc.NOMINAL, True)
    assert s is not None
    assert s.fuel[1 + chamber] <= 150 * lo


def test_suzukis_stoking_rate_reduces() -> None:
    """p.93: from the fourth hour one bundle every 3–4 minutes from each side "to give a reducing
    atmosphere": 30–40 bundles an hour, even at the light end of a bundle's band more than the most
    v2's draft burns at λ 1 in chambers 1–3 (max fire) at any corner of its band, so the fire is
    short of air, as the book says."""
    lo, _ = rc.bundle("suzuki-kyoto")
    b = rc.band("suzuki-kyoto")[rc.RATE]
    assert 30 * lo > b.high


# --- Tamba (pp.86–87) ----------------------------------------------------------------------------


def test_tamba_preheats_inside_36_h() -> None:
    """pp.86–87: the dogi stoked alone about 36 h, the first stoke holes to about 1000 °C."""
    _stands("tamba", "the dogi, to 1000 °C (h)", 36.0)


def test_tamba_side_stokes_inside_14_to_18_h() -> None:
    """pp.86–87: 14–18 h of side stoking, every chamber to its cone (10, assumed)."""
    _stands("tamba", rc.SIDES, 18.0)


def test_tamba_fires_inside_50_to_54_h() -> None:
    """pp.86–87 (derived): about 36 h of firebox and 14–18 h of side stoking."""
    _stands("tamba", rc.FIRING, 54.0)


def test_tamba_burns_its_bundles_side_stoking() -> None:
    """T3, pp.86–87: about 200 bundles (15 × 15 × 30 in) side stoking, at a bundle's stated band
    (the dataset's): no less than v2 needs held to the book's 36 h preheat and its 14–18 h of side
    stoking (16 h, shared evenly among the seven chambers) at the stoker's λ 1, even at the light
    end of a bundle's band."""
    lo, _ = rc.bundle("tamba")
    b = rc.held_band("tamba")[rc.SIDE_FUEL]
    assert b.low <= 200 * lo / 1e3


# --- Fujiwara's Bizen kiln (pp.99–105) -----------------------------------------------------------


def test_fujiwara_stokes_its_chambers_inside_12_h() -> None:
    """pp.103–104: after 6½ days of the dogi, 12 h stoking the chambers: v2's dogi at max fire
    those 6½ days, then chamber 1 and the kedo side-stoked to their cones."""
    _stands("fujiwara-bizen", rc.SIDES, 12.0)


def test_fujiwara_fires_in_seven_days() -> None:
    """p.99: "exactly seven days": 6½ days of the dogi and the chambers' stoking."""
    _stands("fujiwara-bizen", rc.FIRING, 7 * 24.0)


def test_fujiwaras_side_holes_need_the_fire_mouth_open() -> None:
    """C1's question 3: with the fire mouth shut the 5 in takiguchi alone can't bring the chambers
    to their cones (the band's other end), so the book's 12 h matches the fire mouth open."""
    shut = rc.run("fujiwara-bizen", rc.Corner(front_open=False))
    assert shut is not None
    assert shut.times[1:] == (None, None)


# --- Olsen's Hollyweird tube (pp.116–117) --------------------------------------------------------


def test_hollyweird_holds_its_front_chamber_35_to_40_h_in_60() -> None:
    """p.117: the front chamber held at cone 11-plus 35–40 h of a normal 60 h firing: it reaches
    cone 11 by 60 − 35 = 25 h."""
    _stands("hollyweird", "the front chamber (h)", 25.0)


def test_hollyweird_holds_its_back_chamber_10_to_15_h_in_60() -> None:
    """p.117: the back chamber held at cone 11-plus 10–15 h: it reaches cone 11 by 50 h."""
    _stands("hollyweird", rc.FIRING, 50.0)


# --- Tobe (p.90) -------------------------------------------------------------------------------


def test_tobe_burns_no_less_than_its_max_fire() -> None:
    """p.90: "required 40 tons of wood to fire" (the whole kiln, decision 15; short or metric
    isn't said: the short ton, the less), as fired: no less than v2's max fire burns (the fastest
    firing its draft allows, at λ 1, each chamber to cone 10), as fired at each corner's moisture,
    somewhere in its band."""
    _stands("tobe", rc.WET, 40 * rc.SHORT_TON / 1e3)


# --- the book's side ---------------------------------------------------------------------------


@pytest.mark.parametrize("kid", sorted(rc.BUNDLES))
def test_a_bundle_weighs_as_its_volume_packed_as_a_cord(kid: str) -> None:
    """The dataset's bundle band is the cord arithmetic (USU's oven-dry cord over 128 ft³ × the
    printed bundle's gross volume), to its rounding."""
    volume, pine = rc.BUNDLES[kid]
    assert rc.bundle(kid) == pytest.approx(rc.bundle_kg(volume, pine), abs=0.06)
