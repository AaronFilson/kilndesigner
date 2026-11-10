"""The reference kilns' documented firings, as the heat model must let them stand (the user,
2026-11-10): "the kilns in the reference material all worked for the people that built them for
the purpose they were built for ... the model has to let them stand as working examples."

Each is an inequality on the kiln's own burners or fuel and its own draft
(`docs/engine-v2/problem-set.md` §2.2, §6; `thermal-combinations.md`, build order step 0). Where
the model says a working kiln can't reach its firing, the model or the design file's inputs are
at fault, never the kiln: such a test is marked with the missing piece, and nothing is fitted to
make it pass (ADR 0017, decision 4).

The book prints no heat failure, so the must-fail cases come from physics (Derived): a kiln whose
burners leave less heat in it at the cone than its lining's steady loss there can never reach the
cone, on any schedule.

Test inputs the book doesn't print (each also a question in `docs/planning/11-09-26.md` §I):
the setting's load and envelope; the cross-draft's lining and chamber are the design file's
assumptions (`reference_kilns.yaml`).
"""

from __future__ import annotations

import math
from pathlib import Path

import heat_cases
import pytest

from kilndesigner.combustion import available_heat_fraction
from kilndesigner.designfile import load_design
from kilndesigner.library import material, materials
from kilndesigner.shape import Arch
from kilndesigner.thermal.conductivity import Conductivity
from kilndesigner.thermal.surface import StillAirSurface
from kilndesigner.thermal.wall import Slab, solve_wall
from kilndesigner.units import Q_, si

ROOT = Path(__file__).resolve().parents[3]
OLSEN = ROOT / "examples" / "olsen"
HOUR = 3600.0
BTU_HR = si(Q_(1, "BTU/hr"), "W")
CONE_10 = 1285 + 273.15  # K, at 60 °C/h (cones.yaml); 1305 °C at 150 °C/h
CONE_10_FAST = 1305 + 273.15
# A quarter cord of the lightest wood in the source's table: 0.25 × 2,070 lb oven-dry (USU
# Extension, Wood Heating, Table 1; wood-fuel.md [W4]; Olsen p.143 "less than a quarter")
QUARTER_CORD_DRY_KG = 0.25 * si(Q_(2070, "lb"), "kg")


def _box_areas(kiln_path: Path, lining: float) -> tuple[float, float, float]:
    """The chamber's inside area (walls, floor, the arch and its end segments), the outside area
    of the box round it ``lining`` thick, and the outside height (m², m², m)."""
    k = load_design(kiln_path)
    w, d, h = (si(getattr(k.chamber, n), "m") for n in ("width", "depth", "height"))
    rise = si(k.roof.rise, "m")  # pyright: ignore[reportAttributeAccessIssue]
    arch = Arch(w, rise)
    inside = 2 * d * h + 2 * (w * h + arch.segment_area) + w * d + arch.arc_length * d
    wo, do, ho = w + 2 * lining, d + 2 * lining, h + rise + 2 * lining
    return inside, 2 * (wo * do + wo * ho + do * ho), ho


def _steady_loss(slabs: list[Slab], t_hot: float, kiln_path: Path) -> float:
    """The lining's steady loss with its hot face at ``t_hot`` (W): one wall of the chamber's
    inside area growing linearly to the outside box's (a test simplification of the six faces),
    still air at 70 °F outside (v1's `solve_wall`: k(T) integrated exactly, ASTM C680's way)."""
    t = sum(s.thickness for s in slabs)
    a_in, a_out, height = _box_areas(kiln_path, t)

    def area(x: float) -> float:
        return a_in + (a_out - a_in) * x / t

    air = si(Q_(70, "degF"), "K")
    surface = StillAirSurface("vertical", height, 0.9)
    return solve_wall(slabs, t_hot, air, surface, area=area).heat_flow


def _kept_at(t_flue: float, burners_btu_hr: float) -> float:
    """The most heat natural-gas burners can leave in a kiln with the flue gas at ``t_flue``:
    the input (HHV, the US rating's basis) × the available heat at λ = 1, the most any air ratio
    leaves (less air can't burn the fuel; more carries more heat away), Cantera's equilibrium
    (v1's `combustion.available_heat_fraction`)."""
    return burners_btu_hr * BTU_HR * available_heat_fraction(t_flue, 1.0, fuel="natural_gas")


CROSSDRAFT = OLSEN / "olsen-crossdraft-36.yaml"
PRINTED_INPUT = 6 * 36_000  # BTU/hr: six burners "rated at 36,000BTU/hr each" (p.226, the page)
DENSE = sorted(m.id for m in materials().values() if m.kind == "dense_firebrick")


@pytest.mark.parametrize("brick", DENSE)
def test_must_fail_the_crossdraft_in_bare_dense_brick_never_reaches_cone_10(brick: str) -> None:
    """Olsen's 36 ft³ cross-draft on its printed burners, lined with 9 in of bare dense brick (the
    book's "dense brick" with no backing): with any dense firebrick in the library, the steady
    loss at cone 10 is over twice what the burners can leave there, so no schedule reaches cone
    10. The design file's backing is the engine's inference from this (reference_kilns.yaml)."""
    nine = [Slab(brick, si(Q_(9, "in"), "m"), material(brick).k)]
    loss = _steady_loss(nine, CONE_10, CROSSDRAFT)
    kept = _kept_at(CONE_10, PRINTED_INPUT)
    assert kept < 0.5 * loss, f"{brick}: kept {kept / 1e3:.1f} kW, steady loss {loss / 1e3:.1f} kW"


def test_the_crossdraft_as_designed_passes_the_steady_check_at_cone_10() -> None:
    """The design file's lining (4½ in medium-duty over 4½ in K-23, assumed) leaves a positive
    margin at cone 10 at λ = 1: a necessary condition only. Whether it gets there in 12–15 h is
    the transient question (test below)."""
    designed = [
        Slab("md", si(Q_(4.5, "in"), "m"), material("firebrick-medium-duty-smithfield").k),
        Slab("k23", si(Q_(4.5, "in"), "m"), material("ifb-k23").k),
    ]
    loss = _steady_loss(designed, CONE_10, CROSSDRAFT)
    kept = _kept_at(CONE_10, PRINTED_INPUT)
    assert kept > loss


def test_the_must_fail_check_is_not_trivially_true() -> None:
    """The same arithmetic on a lining of near-zero conductivity passes: the check fails the
    bare dense brick for its conductivity, not for the burners' size."""
    still = [Slab("ideal", si(Q_(9, "in"), "m"), Conductivity.constant(0.01))]
    assert _kept_at(CONE_10, PRINTED_INPUT) > _steady_loss(still, CONE_10, CROSSDRAFT)


# --- the documented firings, on the whole model (build order step 6) ----------------------------


@pytest.mark.slow
@pytest.mark.geometry
def test_fast_fire_reaches_cone_10_inside_3_5_h_on_its_own_draft() -> None:
    """Olsen p.139: cone 10 in 3½ h. A stoked kiln's time is the stoker's choice within what its
    draft lets it burn (problem set §2.2): the draft-limited fire (the air the chimney draws with
    the damper open, wood burnt at λ 1) must reach cone 10 sooner."""
    t = heat_cases.fast_fire_max().reached(CONE_10_FAST)
    assert t is not None
    assert t < 3.5 * HOUR


@pytest.mark.slow
@pytest.mark.geometry
def test_the_fast_fire_stands_with_four_times_the_load() -> None:
    """The load is a test input (the book prints none): with four times it, 220 kg, the
    draft-limited fire still reaches cone 10 inside 3½ h, so the verdict doesn't hang on it."""
    t = heat_cases.fast_fire_max(heavier=4.0).reached(CONE_10_FAST)
    assert t is not None
    assert t < 3.5 * HOUR


@pytest.mark.slow
@pytest.mark.geometry
def test_fast_fire_follows_its_p309_log_within_its_drafts_air() -> None:
    """Olsen p.309's logged firing (4 h 50 min, cone 10 down at 9:00): with the setting held to
    the log's temperatures, the wood it takes never needs more air than the draft draws."""
    result = heat_cases.fast_fire_log()
    assert result.completed
    assert result.worst_air_share <= 1.0


@pytest.mark.slow
@pytest.mark.geometry
def test_fast_fire_burns_under_a_quarter_cord() -> None:
    """Olsen p.143: "less than a quarter of a cord" for a 3½ to 4-hour firing; the logged firing
    held to its temperatures must burn less than a quarter cord of the lightest wood."""
    result = heat_cases.fast_fire_log()
    assert result.fuel_kg < QUARTER_CORD_DRY_KG


@pytest.mark.slow
@pytest.mark.geometry
def test_w15_ifb_updraft_fires_easily_in_about_8_h_on_ten_burners() -> None:
    """Olsen p.226: a 36 ft³ IFB updraft "will have a minimum of 10 such burners and will probably
    fire easily in eight hours": a general statement, not a built kiln (no design file)."""
    result = heat_cases.w15_ifb()
    t = result.reached(CONE_10)
    assert t is not None
    assert t < 8 * HOUR


@pytest.mark.xfail(
    strict=True,
    reason="open item: the design file's inputs (lining backing, burners' delivered input, chamber,"
    " cone) aren't printed; docs/planning/11-09-26.md §I",
)
@pytest.mark.slow
@pytest.mark.geometry
def test_crossdraft_36_reaches_cone_10_in_12_to_15_h_on_six_burners() -> None:
    """Olsen p.226: "fired ... on six small venturi air-mixer burners (rated at 36,000BTU/hr
    each) in about 12 to 15 hours". The cone isn't printed (cone 10 is the design file's)."""
    result = heat_cases.crossdraft_36()
    t = result.reached(CONE_10)
    assert t is not None
    assert t <= 15 * HOUR


def test_a_quarter_cord_is_the_lightest_tables_wood() -> None:
    assert pytest.approx(234.7, abs=0.1) == QUARTER_CORD_DRY_KG
    assert math.isclose(CONE_10 - 273.15, 1285)
