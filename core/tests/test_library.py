"""The reference library: materials and alloys from their cited data files."""

import pytest

from kilndesigner.library import (
    UnknownEntryError,
    alloy,
    alloys,
    material,
    materials,
)
from kilndesigner.units import Q_, si


def test_a_data_sheet_in_us_units_is_converted_to_si() -> None:
    """K-23 (materials.yaml, Morgan K series [S31]): 0.90 BTU·in/(hr·ft²·°F) at 500 °F."""
    # 1 BTU·in/(hr·ft²·°F) in W/(m·K): 1055.056 J × 0.0254 m / (3600 s × 0.09290304 m² × 5/9 K)
    btu_in = 1055.056 * 0.0254 / (3600 * 0.09290304 * 5 / 9)
    assert f"{btu_in:.6f}" == "0.144228"
    k = material("ifb-k23").k
    assert k.temperatures[0] == pytest.approx((500 - 32) * 5 / 9 + 273.15)
    assert k.values[0] == pytest.approx(0.90 * btu_in, rel=1e-4)


def test_a_materials_limit_is_a_temperature() -> None:
    """K-23: the lower of its two sheets' classifications, 2300 °F."""
    limit = material("ifb-k23").max_service_temperature
    assert limit is not None
    assert si(limit, "degF") == pytest.approx(2300)


def test_an_alloys_resistivity_is_in_ohm_mm2_per_m() -> None:
    """Kanthal A-1: 1.45 Ω·mm²/m at 20 °C, 7.10 g/cm³, 1400 °C in air (§1.1 [S1])."""
    a1 = alloy("kanthal-a1")
    assert a1.resistivity.magnitude == pytest.approx(1.45)
    assert si(a1.resistivity, "ohm*m") == pytest.approx(1.45e-6)
    assert si(a1.max_air_temperature, "degC") == pytest.approx(1400)


def test_ct_is_held_at_the_ends_of_its_table() -> None:
    """Kanthal D's Ct (§1.2 [S4]): 1.00 at 20 °C, 1.08 from 1200 °C to the table's 1300 °C."""
    d = alloy("kanthal-d")
    assert d.temperature_factor(Q_(0, "degC")) == 1.00
    assert d.temperature_factor(Q_(1250, "degC")) == pytest.approx(1.08)
    assert d.temperature_factor(Q_(1350, "degC")) == 1.08
    # Nikrothal 80's Ct falls from 1.05 at 500 °C to 1.04 at 600 °C (§1.2 [S5])
    assert alloy("nikrothal-80").temperature_factor(Q_(550, "degC")) == pytest.approx(1.045)


def test_an_unknown_material_names_the_ones_there_are() -> None:
    with pytest.raises(UnknownEntryError) as missing:
        material("ifb-k28")
    known = ", ".join(sorted(materials()))
    assert str(missing.value) == f"no material 'ifb-k28'; the library has: {known}"
    assert isinstance(missing.value, KeyError)
    assert "ifb-jm26" in known


def test_an_unknown_alloy_names_the_ones_there_are() -> None:
    with pytest.raises(UnknownEntryError) as missing:
        alloy("kanthal-a")
    assert str(missing.value) == (
        "no alloy 'kanthal-a'; the library has: kanthal-a1, kanthal-af, kanthal-apm, kanthal-d, "
        "nikrothal-80"
    )
    assert len(alloys()) == 5
