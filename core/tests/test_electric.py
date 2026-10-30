"""Element design against Kanthal's worked example and the kiln makers' rules (ADR 0009)."""

import math
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from kilndesigner import load_design, parse_design
from kilndesigner.electric import (
    design_elements,
    largest_breaker,
    surface_load,
    wire_diameter,
    wire_length,
)
from kilndesigner.heatloss import heat_loss
from kilndesigner.library import alloy, awg_diameter
from kilndesigner.sheet import Check, number
from kilndesigner.units import si
from kilndesigner.working import Finding

EXAMPLES = Path(__file__).parents[2] / "examples"


def test_kanthal_worked_example() -> None:
    """Kanthal 'Calculations of wire: examples' (electric-and-thermal.md §1.7, [S16]).

    20 kW at 220 V, Kanthal AF at 1200 °C (Ct 1.06), 4.0 W/cm². Kanthal: d ≈ 4.98 mm; with the
    standard 5.0 mm wire, 3.95 W/cm². Derived in the notes: L = 32.25 m.
    """
    af = alloy("kanthal-af")
    from kilndesigner.units import Q_

    ct = af.temperature_factor(Q_(1200, "degC"))
    assert ct == pytest.approx(1.06)
    rho_t = si(af.resistivity, "ohm*m") * ct
    d = wire_diameter(20_000, 220, 4.0e4, rho_t)
    assert d * 1000 == pytest.approx(4.978, abs=0.001)
    length = wire_length(20_000, 220, 5.0e-3, rho_t)
    assert length == pytest.approx(32.25, abs=0.01)
    assert surface_load(20_000, 5.0e-3, length) / 1e4 == pytest.approx(3.948, abs=0.001)


def test_olsens_worked_example() -> None:
    """Olsen's 10½ ft³ cone 10 kiln (*The Kiln Book*, 4th ed., p.258–260): 26 kW at 240 V in six
    groups of 4333 W; B&S 10 wire (0.102 in) at 0.083 Ω/ft cold, Ct 1.04: 154.2 ft a group, at
    7.4 W/in². He rounds the cold resistance to 12.8 Ω, and his load's denominator is a slip: the
    exact figures are 154.0 ft and 7.3 W/in²."""
    d = 0.102 * 0.0254
    rho_t = 0.083 / 0.3048 * 1.04 * math.pi * d**2 / 4  # Ω·m, hot
    length = wire_length(26_000 / 6, 240, d, rho_t)
    assert length / 0.3048 == pytest.approx(154.2, abs=0.3)
    assert surface_load(26_000 / 6, d, length) * 0.0254**2 == pytest.approx(7.3, abs=0.05)


@pytest.mark.parametrize(
    ("gauge", "mm"), [(8, 3.264), (10, 2.588), (12, 2.053), (13, 1.828), (14, 1.628), (20, 0.812)]
)
def test_awg_matches_the_published_table(gauge: int, mm: float) -> None:
    assert si(awg_diameter(gauge), "mm") == pytest.approx(mm, abs=0.001)


def test_ct_interpolates_between_rows() -> None:
    from kilndesigner.units import Q_

    a1 = alloy("kanthal-a1")
    assert a1.temperature_factor(Q_(1350, "degC")) == pytest.approx(1.045)
    assert a1.temperature_factor(Q_(20, "degC")) == 1.0


@pytest.fixture(scope="module")
def front_loader_design():
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    return kiln, design_elements(kiln, heat_loss(kiln).total_watts)


def test_a_48_amp_kiln_on_a_60_amp_breaker(front_loader_design) -> None:  # type: ignore[no-untyped-def]
    """L&L: 48 A × 1.25 = 60 A breaker (electric-and-thermal.md §3, [S25])."""
    _, design = front_loader_design
    assert design.continuous_current_limit == "48 A"
    assert design.installed_watts == pytest.approx(11_520)


def test_elements_meet_the_rules(front_loader_design) -> None:  # type: ignore[no-untyped-def]
    _, design = front_loader_design
    e = design.elements
    assert e is not None
    assert float(e.surface_load.split()[0]) <= 17.5
    ratio = float(e.pitch.split("(")[1].split(" ")[0])
    assert 2.0 <= ratio <= 4.0
    assert not [f for f in design.findings if f.level == "error"]


def test_power_per_volume_is_like_commercial_kilns(front_loader_design) -> None:  # type: ignore[no-untyped-def]
    """7 cu ft cone 10 kilns from L&L and Skutt: about 1650–1720 W/ft³ (§7)."""
    _, design = front_loader_design
    per_volume = float(design.power_per_volume.split()[0])
    assert 1500 < per_volume < 1900


def test_too_much_power_is_an_error() -> None:
    text = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    kiln = parse_design(text.replace("alloy: kanthal-a1", "alloy: kanthal-a1\n    power: 20 kW"))
    design = design_elements(kiln)
    [error] = [f for f in design.findings if "more than the circuit" in f.message]
    # Its sheet: P_s = f_c·I_b·V = 0.8 × 60 A × 240 V, against the 20 kW asked for
    assert error.check is not None
    assert error.check.requirements[0].margin == "P = 20 kW, 173.6 % of P_s = 11.52 kW"
    assert error.check.solve == "Passes when P ≤ 11.52 kW"


def test_no_wire_that_fits_shows_the_nearest_arrangement() -> None:
    """20 kW in the front loader's three walls: the nearest is three elements of three grooves
    each. At Krueger's 17.5 W/in², the most any source uses, the thinnest wire is 2.598 mm,
    between 10 AWG (2.588 mm) and 9 AWG (2.906 mm); in 9 AWG the coil's pitch is under 2 wire
    diameters, since pitch ÷ d goes as 1/d². Longer grooves would let it fit."""
    kiln = parse_design(FRONT.replace("alloy: kanthal-a1", "alloy: kanthal-a1\n    power: 20 kW"))
    [error] = [
        f for f in design_elements(kiln).findings if f.check and f.check.id == "electric.no-wire"
    ]
    assert error.message.startswith("No standard wire gauge gives elements that fit")
    check = error.check
    assert check is not None
    cells = {c.symbol: c for c in check.cells}
    assert cells["c_g"].formula == "c·(d/d_g)²"
    assert [r.margin for r in check.requirements] == [
        "d = 2.598 mm, 79.58 % of d_max = 3.264 mm",
        "c_g = 1.929, 96.46 % of c_min = 2",
    ]
    assert cells["G"].meaning == "groove for each element: round its walls, 3 rows"
    assert check.solve == "Passes when G ≥ 209.9 in"


def _front_loader_fired(firing: str) -> list[tuple[str, str]]:
    text = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    kiln = parse_design(text.replace('  cone: "10"', firing))
    return [(f.level, f.message) for f in design_elements(kiln).findings]


def test_past_the_wire_rating_and_past_cone_10_are_warnings() -> None:
    """Hot wire wears out faster: a warning, as is a kiln past cone 10 by cone or temperature."""
    hot = _front_loader_fired('  cone: "10"\n  top_temperature: 2400 °F')
    assert [lv for lv, m in hot if "is rated to" in m] == ["warning"]
    assert any("wear out faster" in m for _, m in hot)
    grooves = "highest kiln temperature"
    assert [lv for lv, m in hot if grooves in m] == ["warning"]
    # Cone 11 at 60 °C/h is cooler than cone 10 fired fast, but it is past cone 10
    eleven = _front_loader_fired('  cone: "11"')
    assert [lv for lv, m in eleven if grooves in m] == ["warning"]
    ten = _front_loader_fired('  cone: "10"')
    assert [lv for lv, m in ten if grooves in m] == ["info"]
    assert not [m for lv, m in hot + eleven + ten if lv == "error"]


def _checks(firing: str) -> dict[str, Check]:
    kiln = parse_design(FRONT.replace('  cone: "10"', firing))
    return {f.check.id: f.check for f in design_elements(kiln).findings if f.check}


def test_the_wire_and_groove_sheets_say_how_hot_is_too_hot() -> None:
    """A-1 is rated to 1400 °C (2552 °F) in air; the wire is taken 100 °C (180 °F) above the
    kiln, so the kiln may reach 2372 °F. Past cone 10 by temperature, cone 10 at 150 °C/h
    (2381 °F) is where it passes again; past it by its cone (11), no temperature does."""
    hot = _checks('  cone: "10"\n  top_temperature: 2400 °F')
    wire = hot["electric.wire-temperature"]
    assert wire.requirements[0].margin == "T_w = 2,580 °F, 28 °F over T_max = 2,552 °F"
    assert wire.solve == "Passes when T_top ≤ 2,372 °F"
    assert hot["electric.grooves"].solve == "Passes when T_top ≤ 2,381 °F"
    eleven = _checks('  cone: "11"')["electric.grooves"]
    assert (eleven.status, eleven.rule_holds, eleven.lever) == ("warning", False, None)
    assert eleven.cells[3].text == "11"


def test_three_phase_uses_root_three() -> None:
    text = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    kiln = parse_design(text.replace("phase: 1", "phase: 3").replace("60 A", "40 A"))
    design = design_elements(kiln)
    assert design.installed_watts == pytest.approx(math.sqrt(3) * 240 * 32)
    assert design.elements is not None
    assert design.elements.count % 3 == 0


@settings(max_examples=30, deadline=None)
@given(
    power=st.floats(min_value=200, max_value=5000),
    voltage=st.floats(min_value=60, max_value=480),
    load=st.floats(min_value=1e4, max_value=4e4),
)
def test_the_chosen_diameter_meets_the_load_exactly(
    power: float, voltage: float, load: float
) -> None:
    rho_t = 1.45e-6 * 1.04
    d = wire_diameter(power, voltage, load, rho_t)
    length = wire_length(power, voltage, d, rho_t)
    assert surface_load(power, d, length) == pytest.approx(load, rel=1e-9)
    # a thicker wire at the same power and voltage is longer and runs at a lower load
    longer = wire_length(power, voltage, d * 1.1, rho_t)
    assert longer > length
    assert surface_load(power, d * 1.1, longer) < load


FRONT = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
ELEMENT_WALLS = "walls: [left, right, back]"


def _thin_wire(findings: list[Finding]) -> list[str]:
    return [f.message for f in findings if "Kanthal recommends wire of 3 mm" in f.message]


def test_a_kiln_without_elements_is_refused() -> None:
    with pytest.raises(ValueError, match="the kiln has no electric heat"):
        design_elements(load_design(EXAMPLES / "gas-crossdraft.yaml"))


def test_a_set_number_of_elements_is_kept() -> None:
    """With elements: 9 the tool wires the nine it is given, and when it can't use 3 mm wire it
    looks at every count to say whether any could."""
    kiln = parse_design(FRONT.replace(ELEMENT_WALLS, f"{ELEMENT_WALLS}\n    elements: 9"))
    design = design_elements(kiln)
    e = design.elements
    assert e is not None
    assert e.count == 9
    assert e.groove_rows == 9
    assert float(e.surface_load.split()[0]) <= 17.5
    [thin] = _thin_wire(design.findings)
    assert thin.startswith(
        f"For the 9 elements the design asks for, the tool chose {e.gauge} wire ("
    )
    # The only wall without elements is the door, so there's no room to add more grooves
    assert "No number of elements in the left, right and back walls fits wire that thick" in thin
    assert thin.endswith("Expect to replace these elements sooner.")


def test_three_phase_in_four_walls_takes_wire_over_3_mm() -> None:
    """208 V three-phase on a 60 A breaker, elements in all four walls: √3 × 208 × 48 = 17.3 kW,
    in delta. Three elements of three grooves each, as Olsen runs his (p.259–260), take 8 AWG
    (3.264 mm, ASTM B258) at 8.78 W/in², under his 9 for cone 10, and meet Kanthal's 3 mm
    minimum for grooved elements, so there's no note about thin wire."""
    text = (
        FRONT.replace("phase: 1", "phase: 3")
        .replace("240 V", "208 V")
        .replace(ELEMENT_WALLS, "walls: [left, right, back, front]")
    )
    design = design_elements(parse_design(text))
    assert design.installed_watts == pytest.approx(math.sqrt(3) * 208 * 48)
    e = design.elements
    assert e is not None
    assert e.gauge == "8 AWG"
    assert e.wire_diameter == "0.129 in"
    assert e.wiring == (
        "3 in parallel, each across the full voltage, in delta: 1 string(s) across each pair of "
        "lines"
    )
    assert (e.count, e.groove_rows, e.surface_load) == (3, 9, "8.78 W/in²")
    assert 2.0 <= float(e.pitch.split("(")[1].split(" ")[0]) <= 4.0
    assert _thin_wire(design.findings) == []
    assert design.supply == "208 V, 3-phase, 60 A breaker"


def test_elements_in_one_wall_that_cant_take_thick_wire() -> None:
    """A 30 A circuit with elements in the left wall only: no count fits 3 mm wire there, and
    the back wall is free, so more walls are suggested."""
    text = FRONT.replace(ELEMENT_WALLS, "walls: [left]").replace("60 A", "30 A")
    design = design_elements(parse_design(text))
    assert design.continuous_current_limit == "24 A"
    [thin] = _thin_wire(design.findings)
    assert "No number of elements in the left wall fits wire that thick" in thin
    assert "Elements in more walls would make room; otherwise, expect to replace" in thin


def test_the_wall_loading_is_worked_and_checked_against_kanthal() -> None:
    """Kanthal key data, spiral in grooves: at most 35 kW/m² of wall at 1000 °C [S14] (review
    E5). The front-loader's 11.52 kW over its three element walls is well under; one wall with a
    30 A circuit's power over half the area is checked the same way."""
    design = design_elements(parse_design(FRONT))
    step = next(s for s in design.working if s.name == "Wall loading")
    kiln = parse_design(FRONT)
    c = kiln.chamber
    w, d, h = si(c.width, "m"), si(c.length, "m"), si(c.height, "m")
    area = 2 * d * h + w * h  # left, right, back
    assert step.value == f"{design.installed_watts / area / 1000:.3g} kW/m²"
    assert step.inputs["Kanthal's most, in grooves at 1000 °C"] == "35 kW/m²"
    assert not [f for f in design.findings if f.check and f.check.id == "electric.wall-loading"]


def test_a_wall_loaded_past_kanthals_figure_is_a_warning() -> None:
    from kilndesigner.electric_checks import wall_loading
    from kilndesigner.units import Q_

    check = wall_loading(20_000, 0.5, Q_(35, "kW/m**2"), "Kanthal").check()
    assert check.status == "warning"
    assert check.requirements[0].margin == "w = 40 kW/m², 114.3 % of w_max = 35 kW/m²"


def test_wire_under_kanthals_groove_range_is_a_warning() -> None:
    """Kanthal gives 2.0–5.0 mm for coils in grooves [S14] (review E4); 0.81 mm (20 AWG) is
    outside it."""
    from kilndesigner.electric_checks import groove_wire
    from kilndesigner.units import Q_

    check = groove_wire(si(awg_diameter(20), "m"), Q_(2.0, "mm"), "Kanthal").check()
    assert check.status == "warning"
    assert check.solve == "Passes when d ≥ 2 mm"
    assert groove_wire(2.1e-3, Q_(2.0, "mm"), "Kanthal").check().status == "pass"


def test_the_coil_pitch_cites_the_groove_rule() -> None:
    """Review E10: in grooves Kanthal's key data give a pitch of at least 2 d [S14]; the 4 d top
    is Kanthal's general range [S13]."""
    design = design_elements(parse_design(FRONT))
    coil = next(s for s in design.working if s.name == "Coil")
    assert coil.inputs["pitch range"].startswith("at least 2 d in grooves (Kanthal key data")


def test_krueger_load_outside_its_alloy_or_temperature_is_noted() -> None:
    """Review E5: Krueger's 17.5 W/in² is for A-1 at about 2300 °F; held to it at cone 10 the
    elements get a note saying no source covers that load there."""
    design = design_elements(parse_design(FRONT))
    noted = [f for f in design.findings if "held only to Krueger's 17.5" in f.message]
    loaded = [f for f in design.findings if f.check and f.check.id == "electric.surface-load"]
    assert bool(noted) == bool(loaded)


def test_too_little_power_for_the_loss_is_an_error() -> None:
    """2 kW can't hold a 7 ft³ kiln at cone 10, whose steady loss is several kW. (On a 20 A
    breaker: 2 kW draws 8.3 A, too little for the example's 60 A.)"""
    kiln = parse_design(_with_power("2 kW", breaker="20 A"))
    loss = heat_loss(kiln).total_watts
    design = design_elements(kiln, loss)
    ratio = next(s for s in design.working if s.name.startswith("Installed power over"))
    assert ratio.value == f"{2000 / loss:.3g}"
    assert 2000 / loss < 1
    errors = [f for f in design.findings if f.level == "error"]
    assert [f.message for f in errors] == [
        "The installed power is no more than the heat loss at top temperature: the kiln can "
        "never reach it. Add power or insulation."
    ]
    check = errors[0].check
    assert check is not None
    assert check.solve == f"Passes when P ≥ {number(loss / 1000)} kW"


def test_a_cone_6_kiln_is_inside_kanthals_limits() -> None:
    """Cone 6 is 1222 °C at 60 °C/h, under Kanthal's 1250 °C for coils in grooves [S14]; the wire,
    taken 100 °C hotter, is under A-1's 1400 °C in air [S1]. Ct at 1322 °C lies between the
    table's 1.04 at 1300 °C and 1.05 at 1400 °C (§1.2)."""
    design = design_elements(parse_design(FRONT.replace('cone: "10"', 'cone: "6"')))
    assert not [f for f in design.findings if "highest kiln temperature" in f.message]
    assert not [f for f in design.findings if "is rated to" in f.message]
    step = next(s for s in design.working if s.name == "Wire resistivity when hot")
    assert step.inputs["wire temperature"] == "2412 °F"
    assert step.inputs["Ct"] == "1.04"
    assert step.inputs["ρ20"] == "1.45 mm²⋅Ω/m"


def test_the_hot_resistivity_step_is_in_ohm_mm2_per_m() -> None:
    """A-1: ρ20 = 1.45 Ω·mm²/m (§1.1 [S1]); at 1322 °C, Ct = 1.04 + 0.01 × 22/100 (§1.2)."""
    design = design_elements(parse_design(FRONT.replace('cone: "10"', 'cone: "6"')))
    step = next(s for s in design.working if s.name == "Wire resistivity when hot")
    ct = 1.04 + 0.01 * 22 / 100
    assert float(step.value.split()[0]) == pytest.approx(1.45 * ct, abs=5e-4)


@pytest.mark.parametrize(
    ("amps", "largest"),
    [
        (12.5, 20),  # 13.3 A or less: 20 A (NEC 422.11(E)(2))
        (13.3, 20),
        (13.4, 25),  # 150 % is 20.1 A; the next standard size up is 25 A
        (4000 / 240, 25),  # 150 % is 25 A to the last bit of floating point: 25 A is standard
        (30, 45),  # 45 A is a standard size
        (36, 60),  # 54 A isn't: the next one up is 60 A
        (48, 80),  # L&L's 48 A kiln: 72 A, so 80 A
    ],
)
def test_the_largest_breaker_follows_nec_422_11_e(amps: float, largest: float) -> None:
    """Electric-and-thermal.md §3: 20 A up to 13.3 A, then 150 % with the next standard size
    up (240.6(A) [S79]) permitted [S23]."""
    assert largest_breaker(amps) == largest


def _with_power(power: str, breaker: str = "60 A", voltage: str = "240 V") -> str:
    return (
        FRONT.replace("alloy: kanthal-a1", f"alloy: kanthal-a1\n    power: {power}")
        .replace("breaker: 60 A", f"breaker: {breaker}")
        .replace("voltage: 240 V", f"voltage: {voltage}")
    )


def test_a_breaker_too_big_for_the_kiln_is_an_error() -> None:
    """The review's case: 4 kW at 240 V draws 16.7 A, so at most 25 A, not 60 A."""
    design = design_elements(parse_design(_with_power("4 kW")))
    step = next(s for s in design.working if s.name == "Largest breaker allowed")
    assert step.value == "25 A"
    assert step.inputs == {"kiln's current": "16.7 A"}
    errors = [f for f in design.findings if f.level == "error"]
    assert [f.message for f in errors] == [
        "A 60 A breaker is too big for a kiln that draws 16.7 A: it wouldn't protect the "
        "kiln's own wiring, terminal block and cord. NEC 422.11(E) allows at most 25 A here, "
        "and the breaker must still be at least 125 % of the current, 20.8 A. Use a smaller "
        "breaker, or install more power."
    ]
    assert errors[0].reference is not None
    assert "422.11(E)" in errors[0].reference
    # Its sheet: I = P/V, 150 % of it is 25 A, a standard size, against the 60 A breaker
    check = errors[0].check
    assert check is not None
    assert [c.symbol for c in check.cells] == ["P", "V", "k_φ", "I", "m", "I_150", "I_max", "I_b"]
    assert check.requirements[0].margin == "I_b = 60 A, 240 % of I_max = 25 A"
    assert check.solve == "Passes when I_b ≤ 25 A"


@pytest.mark.parametrize(
    ("power", "breaker", "voltage", "too_big"),
    [
        ("8.64 kW", "60 A", "240 V", False),  # 36 A: 150 % is 54 A, so up to 60 A
        ("8.64 kW", "70 A", "240 V", True),
        ("1.5 kW", "20 A", "120 V", False),  # 12.5 A: up to 20 A
        ("1.5 kW", "25 A", "120 V", True),
    ],
)
def test_the_breaker_check_allows_the_rule_and_no_more(
    power: str, breaker: str, voltage: str, too_big: bool
) -> None:
    design = design_elements(parse_design(_with_power(power, breaker, voltage)))
    assert any("is too big for a kiln" in f.message for f in design.findings) is too_big


def test_a_circuit_sized_kiln_is_never_on_too_big_a_breaker(front_loader_design) -> None:  # type: ignore[no-untyped-def]
    """With the power left out the kiln draws 80 % of the breaker, under the 150 % limit."""
    _, design = front_loader_design
    step = next(s for s in design.working if s.name == "Largest breaker allowed")
    assert step.value == "80 A"
    assert not [f for f in design.findings if "is too big for a kiln" in f.message]


def test_current_at_high_supply_voltage_and_cold_wire_is_shown() -> None:
    """At +5 % (ANSI C84.1 Range A) the 48 A kiln draws 50.4 A hot (electrical-supply.md §1)."""
    root = Path(__file__).parents[2] / "examples"
    design = design_elements(load_design(root / "electric-front-loader.yaml"))
    note = next(f for f in design.findings if "Range A" in f.message)
    assert note.level == "info"
    assert "50.4 A" in note.message
