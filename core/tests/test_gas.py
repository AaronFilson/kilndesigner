"""Gas sizing, the propane supply and the chimney, against the cited tables (§2–§4)."""

import math
from pathlib import Path

import pytest

from kilndesigner import load_design, parse_design
from kilndesigner.gas import (
    design_gas,
    gas_data,
    venturi_pressure,
    wall_class,
    ward_column,
    ward_volume,
)
from kilndesigner.units import Q_, si

EXAMPLES = Path(__file__).parents[2] / "examples"
PNW = EXAMPLES / "pnw-hybrid-crossdraft.yaml"


@pytest.fixture(scope="module")
def pnw():  # type: ignore[no-untyped-def]
    return load_design(PNW)


def test_ward_volume_counts_two_thirds_of_the_arch(pnw) -> None:  # type: ignore[no-untyped-def]
    """Ward: sprung arch volume = W × L × (wall height + ⅔ rise) [S28]."""
    expected_in3 = 28 * 60 * (44 + 2 / 3 * 3.75)
    assert ward_volume(pnw) == pytest.approx(si(Q_(expected_in3, "in**3"), "m**3"))


def test_ward_column_by_cone() -> None:
    assert ward_column(Q_(1000, "degC")) == "6"  # above cone 06 (998 °C)
    assert ward_column(Q_(1285, "degC")) == "10"
    assert ward_column(Q_(1300, "degC")) is None


def test_pnw_burner_input(pnw) -> None:  # type: ignore[no-untyped-def]
    """9 in insulating brick at cone 10: 10,000–16,000 BTU/ft³/hr; fast firing uses 16,000."""
    assert wall_class(pnw) == "insulating_brick"
    gas = design_gas(pnw)
    volume_ft3 = 28 * 60 * (44 + 2.5) / 1728
    assert gas.design_input_btu_hr == pytest.approx(16_000 * volume_ft3)


def test_venturi_pressure_follows_the_ratings() -> None:
    spec = gas_data()["venturi_burners"]["models"]["GACO MR100"]
    assert venturi_pressure(216_300, spec["psi"], spec["btu_hr"]) == pytest.approx(10.0)
    # between table points, rating grows with √pressure
    p = venturi_pressure(184_565, spec["psi"], spec["btu_hr"])
    assert p is not None
    assert math.sqrt(p) == pytest.approx((math.sqrt(5) + math.sqrt(10)) / 2, rel=1e-3)
    assert venturi_pressure(400_000, spec["psi"], spec["btu_hr"]) is None
    # the in. w.c. and 2 psi entries may be another orifice, so nothing below 5 psi is given
    assert venturi_pressure(10_000, spec["psi"], spec["btu_hr"]) == pytest.approx(5.0)


def test_draft_is_figured_at_the_sites_air_not_the_coldest_day(pnw) -> None:  # type: ignore[no-untyped-def]
    """Warm air gives the least draft (structure-and-draft.md §4)."""
    warm = parse_design(
        (EXAMPLES / "pnw-hybrid-crossdraft.yaml").read_text(encoding="utf-8")
    ).model_copy(deep=True)
    base = design_gas(pnw).draft
    hotter = warm.model_copy(
        update={"site": warm.site.model_copy(update={"ambient": Q_(100, "degF")})}
    )
    assert design_gas(hotter).draft[0] < base[0]


def test_four_cylinders_at_20f_match_the_research_check(pnw) -> None:  # type: ignore[no-untyped-def]
    """combustion-and-masonry.md §10: 668,000 full, 376,000 half, 173,200 conservative."""
    gas = design_gas(pnw)
    capacities = [s.capacity_btu_hr for s in gas.supply]
    assert capacities == pytest.approx([668_000, 376_000, 173_200])
    assert not any(s.meets_demand for s in gas.supply)
    assert any(f.level == "error" and "stall" in f.message for f in gas.findings)


def test_chosen_burners_cover_the_input(pnw) -> None:  # type: ignore[no-untyped-def]
    gas = design_gas(pnw)
    assert gas.burners is not None
    each = float(gas.burners.each.split()[0].replace(",", ""))
    assert each * gas.burners.count == pytest.approx(gas.design_input_btu_hr, rel=1e-6)
    assert float(gas.burners.pressure.split()[0]) <= 10


def test_chimney_follows_the_rule(pnw) -> None:  # type: ignore[no-untyped-def]
    """3 × (44 + 3.75) in + ⅓ × (60 in chamber + 8 in flue wall + 9 in to the chimney)."""
    gas = design_gas(pnw)
    expected = 3 * 47.75 + (60 + 8 + 9) / 3
    assert gas.chimney_height is not None
    assert f"({expected:.0f} in)" in gas.chimney_height


def test_stack_draft_matches_the_research_example() -> None:
    """§4.2: a 12 ft stack, 20 °F outside, 1000 °F flue gas: about 0.128 in. w.c."""
    from kilndesigner.gas import ATMOSPHERE, PA_PER_IN_WC, STACK_C

    dp = STACK_C * ATMOSPHERE * 3.6576 * (1 / 266.48 - 1 / 810.93)
    assert dp / PA_PER_IN_WC == pytest.approx(0.128, abs=0.002)


def test_a_tank_keeps_up_with_a_slow_firing() -> None:
    kiln = load_design(EXAMPLES / "pnw-hybrid-crossdraft-budget.yaml")
    gas = design_gas(kiln)
    assert all(s.meets_demand for s in gas.supply)


def test_power_burners_need_electricity() -> None:
    text = PNW.read_text(encoding="utf-8").replace("type: venturi", "type: power")
    gas = design_gas(parse_design(text))
    assert gas.burners is not None
    assert gas.burners.model.startswith("Ward MB")
    assert any("power cut" in f.message for f in gas.findings)
