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


def test_current_at_high_supply_voltage_and_cold_wire_is_shown() -> None:
    """At +5 % (ANSI C84.1 Range A) the 48 A kiln draws 50.4 A hot (electrical-supply.md §1)."""
    root = Path(__file__).parents[2] / "examples"
    design = design_elements(load_design(root / "electric-front-loader.yaml"))
    note = next(f for f in design.findings if "Range A" in f.message)
    assert note.level == "info"
    assert "50.4 A" in note.message
