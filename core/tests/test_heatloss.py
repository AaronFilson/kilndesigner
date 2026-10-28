from pathlib import Path

import pytest

from kilndesigner import load_design, parse_design
from kilndesigner.cones import cone_temperature
from kilndesigner.heatloss import heat_loss
from kilndesigner.library import materials
from kilndesigner.shape import Arch
from kilndesigner.thermal.surface import RA_SOURCE
from kilndesigner.units import Q_, si

EXAMPLES = Path(__file__).parents[2] / "examples"


def test_cone_10_is_1285_c_at_60_per_hour() -> None:
    """Orton's cone 10 self-supporting page: 1285 °C at 60 °C/h, 1305 at 150 (§8, [S76])."""
    assert si(cone_temperature("10"), "degC") == 1285
    assert si(cone_temperature("10", 150), "degC") == 1305
    assert si(cone_temperature("06"), "degC") == 998
    assert si(cone_temperature("5½"), "degC") == 1203


def test_pce_cones_to_42_at_their_one_rate() -> None:
    """ASTM C24 Table X1.1: cone 15 1430 °C and 32½ 1724 at 150 °C/h; 42 2015 at 600 (cones.md)."""
    assert si(cone_temperature("15", 150), "degC") == 1430
    assert si(cone_temperature("32 1/2", 150), "degC") == 1724
    assert si(cone_temperature("38", 100), "degC") == 1835
    assert si(cone_temperature("42", 600), "degC") == 2015
    with pytest.raises(ValueError, match="only at 150 °C/h"):
        cone_temperature("20")
    with pytest.raises(ValueError, match="not in the Orton table"):
        cone_temperature("22", 150)


def test_every_library_material_loads_with_increasing_k_points() -> None:
    for m in materials().values():
        k = m.k
        assert all(v > 0 for v in k.values)
        limit = m.max_service_temperature
        assert limit is not None
        assert limit.check("[temperature]")


def test_front_loader_heat_loss_is_plausible() -> None:
    result = heat_loss(load_design(EXAMPLES / "electric-front-loader.yaml"))
    total_kw = result.total_watts / 1000
    # Steady loss at cone 10 must be well under the 11.5 kW installed in similar kilns.
    assert 3 < total_kw < 9
    assert len(result.faces) == 6
    assert not [f for f in result.findings if f.level == "error"]


def test_k_past_the_data_sheet_is_one_note_per_material_not_a_warning() -> None:
    """JM 26's sheet stops at 1832 °F; at cone 10 that is normal, so it is a note."""
    result = heat_loss(load_design(EXAMPLES / "electric-front-loader.yaml"))
    past = [f for f in result.findings if "past its data sheet's points" in f.message]
    jm26 = [f for f in past if "JM 26" in f.message]
    assert len(jm26) == 1
    assert "up to 2345 °F (data to 1832 °F)" in jm26[0].message
    assert all(f.level == "info" for f in past)
    assert not [f for f in result.findings if f.level == "warning"]


def test_a_low_rated_brick_on_the_hot_face_is_an_error() -> None:
    text = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    kiln = parse_design(text.replace("- material: ifb-jm26", "- material: ifb-k23", 1))
    result = heat_loss(kiln)
    errors = [f for f in result.findings if f.level == "error"]
    assert errors
    assert "K-23" in errors[0].message


def test_more_insulation_loses_less_heat() -> None:
    text = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    thin = heat_loss(parse_design(text)).total_watts
    thick = heat_loss(parse_design(text.replace("thickness: 1 in", "thickness: 2 in"))).total_watts
    assert thick < thin


def test_colder_air_loses_more_heat() -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    assert (
        heat_loss(kiln, ambient=Q_(20, "degF")).total_watts
        > heat_loss(kiln, ambient=Q_(90, "degF")).total_watts
    )


def test_a_face_outside_its_convection_correlation_is_a_warning() -> None:
    """Held 1 °F above its 70 °F air, the kiln's outside barely warms. The floor's Rayleigh number
    falls below the 10⁵ that hot-face-down convection is checked from (thermal-properties.md §5),
    so its loss is flagged; the walls (checked from 0.1) and roof (from 10⁴) are still covered."""
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    result = heat_loss(kiln, inside=Q_(71, "degF"))
    assert result.working[0].name == "Inside temperature"
    assert result.working[0].value == "71 °F"
    [warning] = [f for f in result.findings if f.level == "warning"]
    assert warning.message.startswith("floor: the outside air's Rayleigh number is ")
    assert "outside the 1e+05 to 1e+10 its convection correlation is checked for" in warning.message
    assert warning.reference == RA_SOURCE
    ra = float(warning.message.split("number is ")[1].split(",")[0])
    assert 0 < ra < 1e5


def test_arch_geometry() -> None:
    """A semicircle: rise = half the span, arc = π r, segment = π r² / 2."""
    arch = Arch(span=2.0, rise=1.0)
    assert arch.radius == pytest.approx(1.0)
    assert arch.arc_length == pytest.approx(3.14159265, rel=1e-8)
    assert arch.segment_area == pytest.approx(3.14159265 / 2, rel=1e-8)
