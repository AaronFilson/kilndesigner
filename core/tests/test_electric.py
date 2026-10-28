"""Element design against Kanthal's worked example and the kiln makers' rules (ADR 0009)."""

import math
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from kilndesigner import load_design, parse_design
from kilndesigner.electric import design_elements, surface_load, wire_diameter, wire_length
from kilndesigner.heatloss import heat_loss
from kilndesigner.library import alloy, awg_diameter
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
    assert any("more than the circuit" in f.message for f in design.findings)


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
    in delta. The grooves are long enough for 8 AWG (3.264 mm, ASTM B258), which meets Kanthal's
    3 mm minimum for grooved elements, so there's no note about thin wire."""
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
    assert e.wiring == "3 string(s) of 3 in series, in delta: 1 string(s) across each pair of lines"
    assert 2.0 <= float(e.pitch.split("(")[1].split(" ")[0]) <= 4.0
    assert float(e.surface_load.split()[0]) <= 17.5
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


def test_too_little_power_for_the_loss_is_an_error() -> None:
    """2 kW can't hold a 7 ft³ kiln at cone 10, whose steady loss is several kW."""
    kiln = parse_design(FRONT.replace("alloy: kanthal-a1", "alloy: kanthal-a1\n    power: 2 kW"))
    loss = heat_loss(kiln).total_watts
    design = design_elements(kiln, loss)
    ratio = next(s for s in design.working if s.name.startswith("Installed power over"))
    assert ratio.value == f"{2000 / loss:.3g}"
    assert 2000 / loss < 1
    errors = [f.message for f in design.findings if f.level == "error"]
    assert errors == [
        "The installed power is no more than the heat loss at top temperature: the kiln can "
        "never reach it. Add power or insulation."
    ]


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


@pytest.mark.xfail(
    strict=True,
    reason=(
        "electric.py:291 labels ρ_T, worked in Ω·m, as Ω·mm²/m, so the step shows 1.511e-06 "
        "instead of 1.511 (the golden reports carry the same slip)"
    ),
)
def test_the_hot_resistivity_step_is_in_ohm_mm2_per_m() -> None:
    """A-1: ρ20 = 1.45 Ω·mm²/m (§1.1 [S1]); at 1322 °C, Ct = 1.04 + 0.01 × 22/100 (§1.2)."""
    design = design_elements(parse_design(FRONT.replace('cone: "10"', 'cone: "6"')))
    step = next(s for s in design.working if s.name == "Wire resistivity when hot")
    ct = 1.04 + 0.01 * 22 / 100
    assert float(step.value.split()[0]) == pytest.approx(1.45 * ct, abs=5e-4)


def test_current_at_high_supply_voltage_and_cold_wire_is_shown() -> None:
    """At +5 % (ANSI C84.1 Range A) the 48 A kiln draws 50.4 A hot (electrical-supply.md §1)."""
    root = Path(__file__).parents[2] / "examples"
    design = design_elements(load_design(root / "electric-front-loader.yaml"))
    note = next(f for f in design.findings if "Range A" in f.message)
    assert note.level == "info"
    assert "50.4 A" in note.message
