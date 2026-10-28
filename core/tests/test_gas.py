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
    assert ward_volume(pnw)[0] == pytest.approx(si(Q_(expected_in3, "in**3"), "m**3"))


def test_ward_column_by_cone() -> None:
    assert ward_column(Q_(1000, "degC")) == "6"  # above cone 06 (998 °C)
    assert ward_column(Q_(1285, "degC")) == "10"
    assert ward_column(Q_(1300, "degC")) is None


def _fired(pnw, **firing: object):  # type: ignore[no-untyped-def]
    kiln = pnw.model_copy(update={"firing": pnw.firing.model_copy(update=firing)})
    return design_gas(kiln)


def _past(gas) -> list[tuple[str, str]]:  # type: ignore[no-untyped-def]
    return [(f.level, f.message) for f in gas.findings if "stops at cone 10" in f.message]


def test_past_cone_10_is_a_warning_sized_from_cone_10(pnw) -> None:  # type: ignore[no-untyped-def]
    """Hotter than Ward's last column: warn, and size from the cone 10 figures."""
    gas = _fired(pnw, top_temperature=Q_(1300, "degC"))
    [(level, message)] = _past(gas)
    assert level == "warning"
    assert "(2372 °F)" in message
    assert gas.design_input_btu_hr == pytest.approx(design_gas(pnw).design_input_btu_hr)


def test_past_cone_10_by_the_cone_or_the_temperature(pnw) -> None:  # type: ignore[no-untyped-def]
    """The design's cone counts even when its temperature is given, and the other way round."""
    # Cone 11 with a cooler temperature: the cone is past cone 10, sized by the temperature
    [(level, message)] = _past(_fired(pnw, cone="11", top_temperature=Q_(2300, "degF")))
    assert level == "warning"
    assert "(cone 11)" in message
    # Both past it
    [(_, both)] = _past(_fired(pnw, cone="11", top_temperature=Q_(2400, "degF")))
    assert "(2400 °F and cone 11)" in both
    # Cone 10 fired fast is cone 10, though hotter than cone 10 at 60 °C/h
    assert _past(_fired(pnw, final_rate=150)) == []
    assert _past(design_gas(pnw)) == []


def test_pnw_burner_input(pnw) -> None:  # type: ignore[no-untyped-def]
    """9 in insulating brick at cone 10: 10,000–16,000 BTU/ft³/hr; fast firing uses 16,000."""
    assert wall_class(pnw) == "insulating_brick"
    gas = design_gas(pnw)
    volume_ft3 = 28 * 60 * (44 + 2.5) / 1728
    assert gas.design_input_btu_hr == pytest.approx(16_000 * volume_ft3)


def test_venturi_pressure_follows_the_ratings() -> None:
    models = gas_data()["venturi_burners"]["models"]
    spec = models["GACO MR100"]
    assert venturi_pressure(216_300, spec) == pytest.approx(10.0)
    # between table points, rating grows with √pressure
    p = venturi_pressure(184_565, spec)
    assert p is not None
    assert math.sqrt(p) == pytest.approx((math.sqrt(5) + math.sqrt(10)) / 2, rel=1e-3)
    assert venturi_pressure(400_000, spec) is None
    # Below 5 psi too: the 2 psi rating is on the same √pressure curve (§3.2, derived)
    assert venturi_pressure(96_600, spec) == pytest.approx(2.0)
    low = venturi_pressure(120_000, spec)
    assert low is not None
    assert 2 < low < 5
    # GACO's 11 in. w.c. rating is another orifice, so nothing below 2 psi is given
    assert venturi_pressure(50_000, spec) is None
    # A Ransome's ratings stay on the curve down to 11 in. w.c. (0.397 psi)
    b4 = models["Ransome B4"]
    assert venturi_pressure(55_300, b4) == pytest.approx(0.397)
    assert venturi_pressure(50_000, b4) is None


def test_burners_are_listed_at_the_pressure_that_gives_their_share() -> None:
    """At 5 psi a burner gives its 5 psi rating, not the load: one below that rating runs at a
    lower pressure (the review's gas 4). Every option's pressure gives back its share."""
    gas = design_gas(load_design(EXAMPLES / "gas-crossdraft.yaml"))
    models = gas_data()["venturi_burners"]["models"]
    for o in gas.burner_options:
        each = float(o.each.split()[0].replace(",", ""))
        p = venturi_pressure(each, models[o.model])
        assert p is not None
        assert o.pressure == (f"{p:.1f} psi" if p >= 1 else f"{p * 27.7:.0f} in. w.c.")
    b5 = next(o for o in gas.burner_options if o.count == 2 and o.model == "Ransome B5")
    assert b5.pressure == "3.3 psi"  # 264,444 BTU/hr, under its 324,700 at 5 psi


def test_named_burners_too_big_at_their_lowest_pressure_are_checked_at_what_they_draw() -> None:
    """Eight GACO MR100s share 528,889 BTU/hr: 66,111 each, under the 96,600 an MR100 gives at
    2 psi, the lowest pressure on its high-pressure orifice. They draw 8 × 96,600 there, and
    the supply is checked against that (the review's gas 4)."""
    eight = "wall: front\n      model: GACO MR100\n      count: 8\n    supply"
    gas = design_gas(parse_design(GAS.replace("wall: front\n    supply", eight)))
    assert gas.burners is not None
    assert (gas.burners.count, gas.burners.pressure, gas.burners.each) == (
        8,
        "2.0 psi",
        "96,600 BTU/hr",
    )
    [warning] = [f.message for f in gas.findings if "lowest pressure its ratings" in f.message]
    assert "more than the 66,111 BTU/hr each this kiln needs" in warning
    assert "checked against the 772,800 BTU/hr the 8 burners draw there" in warning
    full_fire = next(s for s in gas.working if s.name == "Propane at full fire")
    assert full_fire.inputs == {"the burners draw": "772,800 BTU/hr"}
    assert gas.propane_at_full_fire == f"{772_800 / 91_502:.2f} gal/hr"
    # Four cylinders give 668,000 BTU/hr full at 20 °F: short of the draw, not of the input
    [error] = [f.message for f in gas.findings if f.level == "error"]
    assert "short of the 772,800 BTU/hr the burners need" in error
    # A slow firing wouldn't help: these burners can't turn down to it
    assert not [f for f in gas.findings if "slow firing" in f.message]


def test_when_no_burner_fits_a_finding_says_why() -> None:
    """A 56.7 ft³ (Ward's way) kiln of hard brick needs 20,000 BTU/ft³/hr, 1,133,333 BTU/hr; a
    tank at −20 °F holds 10.7 psig (NIST [S6]), leaving 0.7 psi, and eight Ransome B5s give under
    1 million there."""
    text = (
        GAS.replace("width: 28 in", "width: 48 in")
        .replace(
            "  walls:\n    - material: ifb-jm26", "  walls:\n    - material: hard-firebrick-kx99"
        )
        .replace(CYLINDERS, "type: tank\n      gallons: 1000")
        .replace("coldest_ambient: 20 degF", "coldest_ambient: -20 degF")
    )
    gas = design_gas(parse_design(text))
    assert gas.burners is None
    assert gas.burner_options == []
    assert (
        "No set of up to 8 venturi burners in the library delivers the 1,133,333 BTU/hr design "
        "input within 0.7 psi, the most this supply allows at -20 °F, so none is chosen."
    ) in [f.message for f in gas.findings if f.level == "error"]


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


GAS = (EXAMPLES / "gas-crossdraft.yaml").read_text(encoding="utf-8")
CYLINDERS = "type: cylinders\n      count: 4"


def test_a_kiln_without_burners_is_refused() -> None:
    with pytest.raises(ValueError, match="the kiln has no gas heat"):
        design_gas(load_design(EXAMPLES / "electric-front-loader.yaml"))


def test_a_fibre_kiln_at_cone_06_takes_wards_fibre_column() -> None:
    """A flat-roofed fibre kiln fired to cone 06, as for raku: Ward gives 4,000–6,000 BTU/ft³/hr
    for 6 in of ceramic fibre at cone 06 [S28]. Flat roof: the volume is W × L × H."""
    text = (
        GAS.replace('cone: "10"', 'cone: "06"')
        .replace("type: sprung_arch\n  rise: 3.75 in # a 60° arch: 0.134 × the span", "type: flat")
        .replace(
            "  walls:\n    - material: ifb-jm26\n      thickness: 4.5 in\n"
            "    - material: ifb-k23\n      thickness: 2.5 in\n"
            "    - material: kaowool-blanket-8pcf\n      thickness: 1 in",
            "  walls:\n    - material: kaowool-blanket-8pcf\n      thickness: 6 in",
        )
    )
    kiln = parse_design(text)
    assert wall_class(kiln) == "ceramic_fibre"
    volume_ft3 = 28 * 48 * 40 / 1728
    assert ward_volume(kiln)[0] == pytest.approx(si(Q_(volume_ft3, "ft**3"), "m**3"))
    gas = design_gas(kiln)
    assert gas.construction == "6 in ceramic fibre"
    assert gas.demand_range == f"{4000 * volume_ft3:,.0f}–{6000 * volume_ft3:,.0f} BTU/hr"
    assert gas.design_input_btu_hr == pytest.approx(6000 * volume_ft3)
    step = next(s for s in gas.working if s.name == "Burner input per cubic foot")
    assert step.inputs == {"construction": "6 in ceramic fibre", "cone column": "06"}


def test_a_hard_brick_kiln_takes_wards_hard_brick_column() -> None:
    """A hot face of super-duty hard firebrick: Ward gives 16,000–20,000 BTU/ft³/hr for 9 in hard
    brick at cone 10 [S28]; a fast firing takes the high end."""
    hot_face = "  walls:\n    - material: ifb-jm26"
    assert hot_face in GAS
    kiln = parse_design(GAS.replace(hot_face, "  walls:\n    - material: hard-firebrick-kx99"))
    assert wall_class(kiln) == "hard_brick"
    gas = design_gas(kiln)
    volume_ft3 = 28 * 48 * (40 + 2 / 3 * 3.75) / 1728
    assert gas.construction == "9 in hard brick"
    assert gas.design_input_btu_hr == pytest.approx(20_000 * volume_ft3)
    assert gas.demand_range == f"{16_000 * volume_ft3:,.0f}–{20_000 * volume_ft3:,.0f} BTU/hr"


def test_a_kiln_past_the_sourced_sizes_is_refused_its_burners_and_chimney() -> None:
    """48 × 60 in by 40 in plus a 3.75 in arch: 71.5 ft³, past the research's studio kilns of up
    to about 60 ft³. It used to crash past about 130 ft³ (no chimney size held the flue) and
    lose its burners past 8 (the review's gas 7). A 1000 gal tank ⅓ full gives 1,031,230 BTU/hr
    at 20 °F [S13], short of the 1,133,333 the kiln would need."""
    text = (
        GAS.replace("width: 28 in", "width: 48 in")
        .replace("depth: 48 in", "depth: 60 in")
        .replace("type: venturi", "type: power")
        .replace(CYLINDERS, "type: tank\n      gallons: 1000")
    )
    kiln = parse_design(text)
    gas = design_gas(kiln)
    demand = 16_000 * 48 * 60 * (40 + 2 / 3 * 3.75) / 1728
    assert gas.design_input_btu_hr == pytest.approx(demand)
    assert (gas.burners, gas.burner_options, gas.chimney_height) == (None, [], None)
    errors = [f.message for f in gas.findings if f.level == "error"]
    assert "At 71 ft³ this kiln is bigger than the sources here cover" in errors[0]
    assert gas.tank_suggestion is None
    assert [s.capacity_btu_hr for s in gas.supply] == pytest.approx([1_031_230])
    # Far past it, the whole report is refused, not crashed
    huge = text.replace("width: 48 in", "width: 72 in").replace("depth: 60 in", "depth: 90 in")
    from kilndesigner.report import design_report

    assert any(
        "bigger than the sources here cover" in f.message
        for f in design_report(parse_design(huge)).errors
    )


def test_a_big_kiln_needs_more_than_one_power_burner() -> None:
    """48 × 48 in by 40 in plus the arch: 57 ft³ × 16,000 = 906,667 BTU/hr, past the biggest
    Ward power burner, the MB700's 795,000 [S22]. Two MB400s at 475,000 each carry it."""
    text = GAS.replace("width: 28 in", "width: 48 in").replace("type: venturi", "type: power")
    gas = design_gas(parse_design(text))
    demand = 16_000 * 48 * 48 * (40 + 2 / 3 * 3.75) / 1728
    assert gas.design_input_btu_hr == pytest.approx(demand)
    assert all(o.count >= 2 for o in gas.burner_options)
    assert gas.burners is not None
    assert (gas.burners.count, gas.burners.model) == (2, "Ward MB400")
    assert gas.burners.total_cost == pytest.approx(2 * 1229)


def test_firing_below_the_vaporization_tables_is_an_error() -> None:
    """The cylinder and tank tables start at 0 °F (§2.1–2.4); propane's vapour pressure at
    −10 °F is 16.7 psig (NIST [S6])."""
    text = GAS.replace("coldest_ambient: 20 degF", "coldest_ambient: -10 degF")
    gas = design_gas(parse_design(text))
    errors = [f.message for f in gas.findings if f.level == "error"]
    assert "The vaporization tables start at 0 °F; colder firing can't be checked." in errors
    step = next(s for s in gas.working if s.name == "Propane pressure available")
    assert step.value == "17 psig in the cylinder or tank at -10 °F"
    assert step.inputs == {"burners limited to": "10 psi"}


def test_one_cylinder_cant_keep_up_even_with_a_slow_firing() -> None:
    """One 100 lb cylinder at 20 °F gives 167,000 BTU/hr full [S3]: short of the fast input and
    of the slow one (10,000 BTU/ft³/hr for 9 in insulating brick at cone 10 [S28])."""
    gas = design_gas(parse_design(GAS.replace(CYLINDERS, "type: cylinders\n      count: 1")))
    volume_ft3 = 28 * 48 * (40 + 2 / 3 * 3.75) / 1728
    assert 10_000 * volume_ft3 > 167_000
    [error] = [f.message for f in gas.findings if f.level == "error"]
    assert error.startswith("Even full, the propane supply gives only 167,000 BTU/hr")
    assert not [f for f in gas.findings if "slow firing" in f.message]
    assert not [f for f in gas.findings if "joined in parallel" in f.message]


def test_burners_that_cant_deliver_the_input_are_an_error() -> None:
    """One Ransome B1 gives 30,700 BTU/hr at 10 psi [S27], far short of 528,889."""
    one_b1 = "wall: front\n      model: Ransome B1\n      count: 1\n    supply"
    text = GAS.replace("wall: front\n    supply", one_b1)
    gas = design_gas(parse_design(text))
    assert gas.burners is None
    assert (
        "The burners chosen can't deliver the design input within 10 psi. Choose more or bigger "
        "burners."
    ) in [f.message for f in gas.findings if f.level == "error"]
    assert not [s for s in gas.working if s.name == "Burners"]


def test_an_up_draft_has_no_chimney_rule() -> None:
    """Olsen's and Ward's chimney rule is for cross- and down-draft kilns; an up-draft gets the
    exit flue area only."""
    gas = design_gas(parse_design(GAS.replace("type: cross", "type: up")))
    assert gas.chimney_height is None
    assert gas.draft == []
    names = [s.name for s in gas.working]
    assert "Exit flue area" in names
    assert "Chimney height" not in names
    assert "Draft at the chimney's base" not in names


def test_power_burners_need_electricity() -> None:
    text = PNW.read_text(encoding="utf-8").replace("type: venturi", "type: power")
    gas = design_gas(parse_design(text))
    assert gas.burners is not None
    assert gas.burners.model.startswith("Ward MB")
    assert any("power cut" in f.message for f in gas.findings)
