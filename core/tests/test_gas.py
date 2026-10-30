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


def test_the_burner_sheet_reads_a_line_a_rating_and_the_altitude() -> None:
    """A burner rated by the design (Olsen's Eclipse TR-80, 214,200 BTU/hr, p.224) gives √σ of it
    at altitude (0.928 at 5000 ft, p.230); a venturi on a line runs at the line's pressure, shown in
    in. w.c. under a pound."""
    from kilndesigner.gas_checks import Demand, Pressure, Ratings, burners

    d = Demand("flat", 36, 36, 36, 0.0, 0.0, 10_000, "insulating brick", "Olsen p.226")
    line = Pressure(tank=False, air_f=70, vapour=([], []), vapour_source="", line_psi=8 / 27.68)
    rated = Ratings("Eclipse TR-80", "rated", (), (214_200,), "Olsen p.224", altitude=0.928)
    s = burners(d, 2, "the design", rated, line, "warning")
    assert s.env["f_alt"] == pytest.approx(0.928)
    assert s.env["r_cap"] == pytest.approx(si(Q_(214_200 * 0.928, "BTU/hr"), "W"))
    venturi = Ratings("a venturi", "venturi", (1, 4, 9), (50_000, 100_000, 150_000), "test", 0.928)

    def p_max_unit(p: Pressure) -> str:
        sheet = burners(d, 2, "the design", venturi, p, "warning")
        assert sheet.env["r_low"] == pytest.approx(si(Q_(50_000 * 0.928, "BTU/hr"), "W"))
        return next(c.unit for c in sheet.check().cells if c.symbol == "p_max")

    assert p_max_unit(line) == "inch_H2O"  # 8 in. w.c. on the line
    high = Pressure(tank=False, air_f=70, vapour=([], []), vapour_source="", line_psi=2.0)
    assert p_max_unit(high) == "psi"


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
    [check] = [f.check for f in gas.findings if "stops at cone 10" in f.message]
    assert check is not None
    assert check.requirements[0].margin == "T_top = 1,300 °C, 15 °C over T_10 = 1,285 °C"
    assert check.rule_holds  # cone 10 itself is in Ward's table
    # Given only a temperature, the sheet says how hot Ward's table goes
    alone = pnw.model_copy(
        update={
            "firing": pnw.firing.model_copy(
                update={"cone": None, "top_temperature": Q_(1300, "degC")}
            )
        }
    )
    [only] = [f.check for f in design_gas(alone).findings if "stops at cone 10" in f.message]
    assert only is not None
    assert only.solve == "Passes when T_top ≤ 1,285 °C"
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
    """9 in insulating brick at cone 10: 10,000–16,000 BTU/ft³/hr (Ward). A slow firing, the
    default, takes 10,000, Olsen's Rule 1 (p.226); a fast one 16,000."""
    assert wall_class(pnw) == "insulating_brick"
    volume_ft3 = 28 * 60 * (44 + 2.5) / 1728
    assert design_gas(pnw).design_input_btu_hr == pytest.approx(10_000 * volume_ft3)
    fast = pnw.model_copy(
        update={
            "heat": pnw.heat.model_copy(
                update={"gas": pnw.heat.gas.model_copy(update={"firing_speed": "fast"})}
            )
        }
    )
    assert design_gas(fast).design_input_btu_hr == pytest.approx(16_000 * volume_ft3)
    step = next(s for s in design_gas(pnw).working if s.name == "Burner input per cubic foot")
    assert step.inputs["Olsen's Rule 1"] == "7,000–10,000 BTU/ft³/hr"


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
    assert b5.each == "165,278 BTU/hr"  # under its 205,400 at 2 psi
    assert b5.pressure == "1.3 psi"


def test_named_burners_too_big_at_their_lowest_pressure_are_checked_at_what_they_draw() -> None:
    """Eight GACO MR100s share 330,556 BTU/hr: 41,319 each, under the 96,600 an MR100 gives at
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
    [big] = [f for f in gas.findings if "lowest pressure its ratings" in f.message]
    warning = big.message
    assert "more than the 41,319 BTU/hr each this kiln needs" in warning
    assert "checked against the 772,800 BTU/hr the 8 burners draw there" in warning
    # Its sheet: the share against the 2 psi rating, and the count that would run within it
    check = big.check
    assert check is not None
    assert (check.id, check.title, check.status) == (
        "gas.burners",
        "8 × GACO MR100 against the design input",
        "warning",
    )
    assert [r.holds for r in check.requirements] == [True, False, True]  # p_0, r_0, r_cap
    assert check.solve == "Passes when n ≤ 3"  # 330,556 ÷ 96,600 = 3.42
    full_fire = next(s for s in gas.working if s.name == "Propane at full fire")
    assert full_fire.inputs == {"the burners draw": "772,800 BTU/hr"}
    assert gas.propane_at_full_fire == f"{772_800 / 91_502:.2f} gal/hr"
    assert gas.full_fire_btu_hr == pytest.approx(772_800)
    # Four cylinders give 668,000 BTU/hr full at 20 °F: short of the draw, not of the input
    [error] = [f.message for f in gas.findings if f.level == "error"]
    assert "short of the 772,800 BTU/hr the burners draw" in error


def test_when_no_burner_fits_a_finding_says_why() -> None:
    """Natural gas at 2 psi: the library rates its burners for natural gas only at low pressure
    (Olsen p.215: 11 in. w.c. or less), so none can be chosen; the design must rate its own."""
    text = GAS.replace(CYLINDERS, "type: line\n      pressure: 2 psi").replace(
        "  gas:\n", "  gas:\n    fuel: natural_gas\n"
    )
    gas = design_gas(parse_design(text))
    assert gas.burners is None
    assert gas.burner_options == []
    [none] = [f for f in gas.findings if f.message.startswith("No set of up to 40")]
    assert none.message == (
        "No set of up to 40 venturi burners in the library delivers the 330,556 BTU/hr design "
        "input on natural gas within 2.0 psi, so none is chosen. Give the burners and their "
        "rating."
    )
    assert none.check is not None
    assert none.check.rule == "The burners must be ones whose ratings the library has."
    # Rated by the design, they fire
    rated = text.replace(
        "wall: front\n    supply",
        "wall: front\n      count: 4\n      rating: 90000 BTU/hr\n    supply",
    )
    fired = design_gas(parse_design(rated))
    assert fired.full_fire_btu_hr == pytest.approx(360_000)
    assert not [f for f in fired.findings if f.level == "error"]


def test_the_vaporization_tables_start_at_0f() -> None:
    """Colder than the tables: a tank at −20 °F can't be checked."""
    text = GAS.replace(CYLINDERS, "type: tank\n      gallons: 1000").replace(
        "coldest_ambient: 20 degF", "coldest_ambient: -20 degF"
    )
    gas = design_gas(parse_design(text))
    [cold] = [f for f in gas.findings if f.message.startswith("The vaporization tables")]
    assert cold.check is not None
    # 0 °F, give or take the part-in-a-billion slack on ≥ (printed in powers of ten near 0)
    assert cold.check.solve is not None
    assert cold.check.solve.startswith("Passes when t ≥ ")


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


def _fast(kiln):  # type: ignore[no-untyped-def]
    gas = kiln.heat.gas.model_copy(update={"firing_speed": "fast"})
    return kiln.model_copy(update={"heat": kiln.heat.model_copy(update={"gas": gas})})


def test_four_cylinders_at_20f_are_read_by_the_liquids_temperature(pnw) -> None:  # type: ignore[no-untyped-def]
    """The 100 lb table is by the liquid's temperature, which runs 20 °F under the air under draw
    (combustion-and-masonry.md §2.3, §2.8; review G5): at 20 °F air it is read at 0 °F, 113,000
    each full and 64,000 half full, not the 20 °F row's 167,000. The conservative ¼-full case
    stays by air, 43,300. Against a fast firing's 16,000 BTU/ft³/hr."""
    gas = design_gas(_fast(pnw))
    capacities = [s.capacity_btu_hr for s in gas.supply]
    assert capacities == pytest.approx([4 * 113_000, 4 * 64_000, 4 * 43_300])
    assert not any(s.meets_demand for s in gas.supply)
    [stall] = [f for f in gas.findings if f.level == "error" and "stall" in f.message]
    check = stall.check
    assert check is not None
    assert check.id == "gas.supply-full"
    cells = {c.symbol: c for c in check.cells}
    assert cells["t_l"].formula == "t − Δt_l"
    assert check.requirements[0].margin == "C = 452,000 Btu/h, 62.49 % of P = 723,333 Btu/h"
    assert check.solve == "Passes when n ≥ 7"  # 723,333 ÷ 113,000 cylinders


def test_a_cold_day_that_passed_now_stalls(pnw) -> None:  # type: ignore[no-untyped-def]
    """Review fix 4: the PNW kiln on four cylinders at 20 °F, slow firing (452,083 BTU/hr), passed
    against the 20 °F row (4 × 167,000 = 668,000). Read at the liquid's 0 °F it gets 452,000 and
    stalls; the regulator leaves the burners 2.96 psi (0.8 × (23.7 − 20))."""
    gas = design_gas(pnw)
    step = next(s for s in gas.working if s.name == "Propane pressure available")
    assert step.inputs["burners limited to"] == "2.96 psi"
    [stall] = [f for f in gas.findings if f.level == "error"]
    assert "stall" in stall.message


def test_the_pressure_ceiling_leaves_room_for_the_regulator() -> None:
    """RegO 597F: inlet 20 psig over set, delivery 20 % under set at capacity [S89]; no more than
    the ratings' 20 psi."""
    from kilndesigner.gas_checks import pressure_ceiling

    assert pressure_ceiling(23.7) == pytest.approx(0.8 * 3.7)
    assert pressure_ceiling(110.2) == pytest.approx(16.0)
    assert pressure_ceiling(16.7) < 0


def test_chosen_burners_cover_the_input(pnw) -> None:  # type: ignore[no-untyped-def]
    gas = design_gas(pnw)
    assert gas.burners is not None
    each = float(gas.burners.each.split()[0].replace(",", ""))
    assert each * gas.burners.count == pytest.approx(gas.design_input_btu_hr, rel=1e-5)
    step = next(s for s in gas.working if s.name == "Propane pressure available")
    limit = float(step.inputs["burners limited to"].split()[0])
    assert float(gas.burners.pressure.split()[0]) <= limit


def test_a_gas_kiln_chimney_reaches_the_kiln_top(pnw) -> None:  # type: ignore[no-untyped-def]
    """Gas under pressure drives the flow: the chimney need only reach the kiln's top, with a
    hood and stack above (Olsen p.151). PNW: 44 in to the springline, a 3.75 in rise and 5 in of
    roof."""
    gas = design_gas(pnw)
    assert gas.chimney_height_in == pytest.approx(44 + 3.75 + 5)
    assert gas.chimney_height == "4.4 ft (53 in) above the chamber floor"
    assert not [f for f in gas.findings if f.check and f.check.id == "gas.chimney"]
    # A chimney built lower than the kiln's top is a warning
    low = PNW.read_text(encoding="utf-8").replace(
        "  flue_wall: back\n", "  flue_wall: back\n  chimney:\n    height: 40 in\n"
    )
    [short] = [
        f for f in design_gas(parse_design(low)).findings if f.check and f.check.id == "gas.chimney"
    ]
    assert short.level == "warning"
    assert "12.8 in below the top of the kiln" in short.message


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
    assert gas.design_input_btu_hr == pytest.approx(4000 * volume_ft3)  # slow: the low end
    step = next(s for s in gas.working if s.name == "Burner input per cubic foot")
    assert step.inputs == {"construction": "6 in ceramic fibre", "cone column": "06"}


def test_a_hard_brick_kiln_takes_wards_hard_brick_column() -> None:
    """A hot face of super-duty hard firebrick: Ward gives 16,000–20,000 BTU/ft³/hr for 9 in hard
    brick at cone 10 [S28]; a slow firing takes the low end, Olsen's 16,000 (p.226)."""
    hot_face = "  walls:\n    - material: ifb-jm26"
    assert hot_face in GAS
    kiln = parse_design(GAS.replace(hot_face, "  walls:\n    - material: hard-firebrick-kx99"))
    assert wall_class(kiln) == "hard_brick"
    gas = design_gas(kiln)
    volume_ft3 = 28 * 48 * (40 + 2 / 3 * 3.75) / 1728
    assert gas.construction == "9 in hard brick"
    assert gas.design_input_btu_hr == pytest.approx(16_000 * volume_ft3)
    assert gas.demand_range == f"{16_000 * volume_ft3:,.0f}–{20_000 * volume_ft3:,.0f} BTU/hr"
    step = next(s for s in gas.working if s.name == "Burner input per cubic foot")
    assert step.inputs["Olsen's Rule 1"] == "16,000–19,000 BTU/ft³/hr"


def test_a_big_kiln_is_sized_not_refused() -> None:
    """Olsen's rules cover kilns to 500 ft³ (Kaneko's car kiln, p.170–172), so a big kiln is
    sized: it used to be refused past 60 ft³, crash past about 130 ft³ (no chimney size held the
    flue) and lose its burners past 8 (the review's gas 7). 72 × 90 in by 40 in plus the arch:
    about 160 ft³, on power burners and a 1000 gal tank."""
    from kilndesigner.report import design_report

    text = (
        GAS.replace("width: 28 in", "width: 72 in")
        .replace("depth: 48 in", "depth: 90 in")
        .replace("type: venturi", "type: power")
        .replace(CYLINDERS, "type: tank\n      gallons: 1000")
    )
    report = design_report(parse_design(text))
    assert report.gas is not None
    assert report.gas.burners is not None
    assert report.gas.chimney_height is not None
    assert not [f for f in report.errors if "bigger than" in f.message]


def test_a_kiln_too_big_for_the_library_checks_its_supply_against_the_input() -> None:
    """With no set of library burners big enough, none is chosen and nothing is drawn: the propane
    supply is checked against the design input, as its sheet says (P = D), not against nothing
    (that raised SheetMismatchError)."""
    text = (
        GAS.replace("width: 28 in", "width: 200 in")
        .replace("depth: 48 in", "depth: 300 in")
        .replace("height: 40 in", "height: 120 in")
    )
    assert text.count("200 in") == 1
    assert text.count("300 in") == 1
    gas = design_gas(parse_design(text))
    assert gas.burners is None
    assert gas.full_fire_btu_hr == 0
    assert gas.supply
    assert not gas.supply[0].meets_demand
    short = next(f for f in gas.findings if f.check and f.check.id == "gas.supply-full")
    assert f"{gas.design_input_btu_hr:,.0f} BTU/hr" in short.message


def test_a_big_kiln_needs_more_than_one_power_burner() -> None:
    """48 × 48 in by 40 in plus the arch: 57 ft³ × 16,000 (fast) = 906,667 BTU/hr, past the
    biggest Ward power burner, the MB700's 795,000 [S22]. Two MB400s at 475,000 each carry it."""
    text = (
        GAS.replace("width: 28 in", "width: 48 in")
        .replace("type: venturi", "type: power")
        .replace("reduction: true", "reduction: true\n    firing_speed: fast")
    )
    gas = design_gas(parse_design(text))
    demand = 16_000 * 48 * 48 * (40 + 2 / 3 * 3.75) / 1728
    assert gas.design_input_btu_hr == pytest.approx(demand)
    assert all(o.count >= 2 for o in gas.burner_options)
    assert gas.burners is not None
    assert (gas.burners.count, gas.burners.model) == (2, "Ward MB400")
    assert gas.burners.total_cost == pytest.approx(2 * 1229)


def test_firing_below_the_vaporization_tables_is_an_error() -> None:
    """The cylinder table starts at 0 °F of liquid, 20 °F of air (§2.1, §2.8); the vapour-pressure
    table at −20 °F (NIST [S6]), which the liquid at −30 °F is held to: 10.7 psig, under the
    regulator's 20 psi margin, so nothing is left for the burners."""
    text = GAS.replace("coldest_ambient: 20 degF", "coldest_ambient: -10 degF")
    gas = design_gas(parse_design(text))
    errors = [f.message for f in gas.findings if f.level == "error"]
    assert any(m.startswith("The vaporization tables start at 20 °F of air") for m in errors)
    step = next(s for s in gas.working if s.name == "Propane pressure available")
    assert step.value == "11 psig in the cylinder or tank, the liquid at -30 °F"
    assert step.inputs["burners limited to"] == "-7.44 psi"


def test_one_cylinder_cant_keep_up_even_with_a_slow_firing() -> None:
    """One 100 lb cylinder at 20 °F air, its liquid at 0 °F, gives 113,000 BTU/hr full [S3]: short
    of the slow input (10,000 BTU/ft³/hr for 9 in insulating brick at cone 10 [S28])."""
    gas = design_gas(parse_design(GAS.replace(CYLINDERS, "type: cylinders\n      count: 1")))
    volume_ft3 = 28 * 48 * (40 + 2 / 3 * 3.75) / 1728
    assert 10_000 * volume_ft3 > 113_000
    errors = [f.message for f in gas.findings if f.level == "error"]
    assert any(e.startswith("Even full, the propane supply gives only 113,000 BTU/hr") for e in errors)
    assert not [f for f in gas.findings if "slow firing" in f.message]
    assert not [f for f in gas.findings if "joined in parallel" in f.message]


def _loss(text: str) -> float:
    from kilndesigner.heatloss import heat_loss

    return heat_loss(parse_design(text)).total_watts


def test_burners_that_cant_hold_the_top_are_an_error() -> None:
    """One Ransome B1 gives 30,700 BTU/hr at 10 psi [S27]: at cone 10 only about a third of that
    stays in the kiln, far short of what the lining loses there. The energy check fails."""
    one_b1 = "wall: front\n      model: Ransome B1\n      count: 1\n    supply"
    text = GAS.replace("wall: front\n    supply", one_b1)
    gas = design_gas(parse_design(text), _loss(text))
    assert gas.burners is not None
    # Under the 30,700 it gives at 10 psi [S27]: at 20 °F the regulator leaves it 2.96 psi
    assert 0 < gas.full_fire_btu_hr < 30_700
    [top] = [f for f in gas.findings if f.check and f.check.id == "gas.top"]
    assert top.level == "error"
    assert "The kiln can't reach its top temperature" in top.message
    assert top.check is not None
    assert top.check.solve is not None
    assert top.check.solve.startswith("Passes when n ≥ ")


def test_named_burners_under_the_rule_fire_more_slowly() -> None:
    """One Ransome B4 gives 286,600 BTU/hr at 10 psi [S27], under the 330,556 of the rule: a
    slower firing, as Olsen's 36 ft³ kiln on 6,000 BTU/ft³/hr (p.226), and a note, not an error.
    It holds the top: about a third of it beats the lining's loss."""
    text = GAS.replace(
        "wall: front\n    supply", "wall: front\n      model: B4\n      count: 1\n    supply"
    )
    gas = design_gas(parse_design(text), _loss(text))
    assert not [f for f in gas.findings if f.level == "error"]
    [slow] = [f for f in gas.findings if "fires more slowly" in f.message]
    assert slow.level == "info"
    # Its 10 psi rating is 286,600 [S27]; at 20 °F the regulator leaves 2.96 psi, and the √p
    # curve between its published ratings gives less
    assert 0 < gas.full_fire_btu_hr < 286_600


def test_a_named_power_burner_bigger_than_needed_is_used() -> None:
    """One MB700 (795,000 BTU/hr) carries 528,889, though a smaller one would; it used to be
    refused because only the smallest that fits was listed."""
    text = GAS.replace("type: venturi", "type: power").replace(
        "wall: front\n    supply", "wall: front\n      model: MB700\n      count: 1\n    supply"
    )
    gas = design_gas(parse_design(text))
    assert gas.burners is not None
    assert (gas.burners.model, gas.burners.count) == ("Ward MB700", 1)
    assert not [f for f in gas.findings if f.level == "error" and "burners" in f.message]


def test_a_power_burner_under_the_rule_fires_at_its_rating() -> None:
    """One MB200, 270,000 BTU/hr [S22], under the rule's 330,556: it fires at its rating."""
    text = GAS.replace("type: venturi", "type: power").replace(
        "wall: front\n    supply",
        "wall: front\n      model: Ward MB200\n      count: 1\n    supply",
    )
    gas = design_gas(parse_design(text))
    assert gas.burners is not None
    assert (gas.burners.model, gas.burners.each) == ("Ward MB200", "270,000 BTU/hr")
    assert any("fires more slowly" in f.message for f in gas.findings)


def test_a_burner_the_library_doesnt_have_is_an_error() -> None:
    text = GAS.replace("wall: front\n    supply", "wall: front\n      model: Acme 9\n    supply")
    gas = design_gas(parse_design(text))
    assert gas.burners is None
    [error] = [f for f in gas.findings if "Acme 9" in f.message]
    assert error.message.startswith("Acme 9 isn't a venturi burner whose ratings the library has")
    assert error.check is not None
    assert error.check.rule == "The burners must be ones whose ratings the library has."


def test_the_conservative_supply_case_is_a_warning() -> None:
    """Four cylinders at 20 °F: 668,000 full covers 330,556, but ¼ full, keeping 10 psi, they
    give 4 × 43,300 [S10, S11]."""
    gas = design_gas(load_design(EXAMPLES / "gas-crossdraft.yaml"))
    [low] = [f for f in gas.findings if "conservative case" in f.message]
    assert low.level == "warning"
    assert low.check is not None
    assert low.check.id == "gas.supply-low"
    assert low.check.solve == "Passes when n ≥ 8"  # 330,556 ÷ 43,300 = 7.63


def test_a_tank_colder_than_its_vapour_table_is_held_at_the_table() -> None:
    """At −30 °F the vapour-pressure table (from −20 °F) is read at its first row, as the engine
    reads it; the sheet shows the hold. Four GACO MR100s can't run at the 0.7 psi left: their
    high-pressure orifice starts at 2 psi."""
    text = (
        GAS.replace(CYLINDERS, "type: tank\n      gallons: 1000")
        .replace("coldest_ambient: 20 degF", "coldest_ambient: -30 degF")
        .replace(
            "wall: front\n    supply", "wall: front\n      model: MR100\n      count: 4\n    supply"
        )
    )
    gas = design_gas(parse_design(text))
    [none] = [f for f in gas.findings if f.message.startswith("The burners chosen aren't rated")]
    assert none.check is not None
    cells = {c.symbol: c for c in none.check.cells}
    assert cells["t_l_c"].formula == "min(max(t_l, t_l_first), t_l_last)"


def test_an_up_draft_has_no_chimney() -> None:
    """An updraft's flue is in its roof, with a hood over it; no chimney is worked out."""
    gas = design_gas(parse_design(GAS.replace("type: cross", "type: up")))
    assert gas.chimney_height is None
    assert gas.draft == []
    names = [s.name for s in gas.working]
    assert "Exit flue, to start" in names
    assert "Chimney height" not in names
    assert "Draft at the chimney's base" not in names


def test_power_burners_need_electricity() -> None:
    text = PNW.read_text(encoding="utf-8").replace("type: venturi", "type: power")
    gas = design_gas(parse_design(text))
    assert gas.burners is not None
    assert gas.burners.model.startswith("Ward MB")
    assert any("power cut" in f.message for f in gas.findings)


def test_the_altitude_factor_reproduces_olsens_table() -> None:
    """Olsen p.230–232: burners give 0.9279 of their output at 5000 ft and 0.8579 at 10,000 ft.
    √σ of NASA's standard atmosphere gives both to 0.2 %."""
    from kilndesigner.gas import altitude_factor

    assert altitude_factor(0.0) == pytest.approx(1.0)
    assert altitude_factor(1524.0) == pytest.approx(0.9279, rel=0.002)
    assert altitude_factor(3048.0) == pytest.approx(0.8579, rel=0.002)


def test_burners_at_altitude_give_less() -> None:
    """At 5000 ft a burner set gives about 7 % less, so the same input needs more pressure."""
    high = GAS.replace(
        "propane_price: 3.50 USD/gallon", "propane_price: 3.50 USD/gallon\n  elevation: 5000 ft"
    )
    gas = design_gas(parse_design(high))
    step = next(s for s in gas.working if s.name == "Burner output at the site's elevation")
    assert step.value == "× 0.9284"


def test_the_flue_starts_at_the_burner_ports() -> None:
    """Olsen: the exit flue as large as the burner ports together, then restricted (p.151); an
    updraft over 40 ft³ about 20 % more (p.174: his 100 ft³ kit, 100 in² of inlets, 120–140 in²
    out); without the ports' size, 1 in² per 7000 BTU/hr (p.236)."""
    from kilndesigner.gas import starting_flue

    assert starting_flue(50.0, 240_000, 24.0, updraft=True)[0] == pytest.approx(50.0)
    assert starting_flue(100.0, 1e6, 100.0, updraft=True)[0] == pytest.approx(120.0)
    assert starting_flue(100.0, 1e6, 100.0, updraft=False)[0] == pytest.approx(100.0)
    assert starting_flue(None, 700_000, 50.0, updraft=False)[0] == pytest.approx(100.0)


def test_natural_gas_ratings_follow_the_square_root_of_pressure() -> None:
    """Olsen p.222: an MR100 gives 100,000 BTU/hr on natural gas at 8 in. w.c.; through the same
    orifice, output goes as √pressure (p.216). Over 11 in. w.c. (low pressure, p.215) the library
    has no natural-gas rating."""
    from kilndesigner.gas import line_rating

    spec = gas_data()["venturi_burners"]["models"]["GACO MR100"]
    assert line_rating(spec, "natural_gas", 8 / 27.68) == pytest.approx(100_000)
    assert line_rating(spec, "natural_gas", 2 / 27.68) == pytest.approx(50_000)
    assert line_rating(spec, "natural_gas", 1.0) is None
    assert (
        line_rating(gas_data()["venturi_burners"]["models"]["Ransome B1"], "natural_gas", 0.3)
        is None
    )
    # Propane on a line: on the curve, or a published low-pressure orifice
    assert line_rating(spec, "propane", 10.0) == pytest.approx(216_300)
    assert line_rating(spec, "propane", 0.397) == pytest.approx(94_000)
    assert line_rating(spec, "propane", 0.6) is None
