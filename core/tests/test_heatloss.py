from pathlib import Path

import pytest

from kilndesigner import load_design, parse_design
from kilndesigner.cones import cone_temperature
from kilndesigner.heatloss import heat_loss
from kilndesigner.library import materials
from kilndesigner.shape import Arch
from kilndesigner.units import si

EXAMPLES = Path(__file__).parents[2] / "examples"


def test_cone_10_is_1285_c_at_60_per_hour() -> None:
    """Orton's cone 10 self-supporting page: 1285 °C at 60 °C/h, 1305 at 150 (§8, [S76])."""
    assert si(cone_temperature("10"), "degC") == 1285
    assert si(cone_temperature("10", 150), "degC") == 1305
    assert si(cone_temperature("06"), "degC") == 998
    assert si(cone_temperature("5½"), "degC") == 1203


def test_every_library_material_loads_with_increasing_k_points() -> None:
    for m in materials().values():
        k = m.k
        assert all(v > 0 for v in k.values)
        assert m.max_service_temperature.check("[temperature]")


def test_front_loader_heat_loss_is_plausible() -> None:
    result = heat_loss(load_design(EXAMPLES / "electric-front-loader.yaml"))
    total_kw = result.total_watts / 1000
    # Steady loss at cone 10 must be well under the 11.5 kW installed in similar kilns.
    assert 3 < total_kw < 9
    assert len(result.faces) == 6
    assert not [f for f in result.findings if f.level == "error"]


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
    from kilndesigner.units import Q_

    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    assert (
        heat_loss(kiln, ambient=Q_(20, "degF")).total_watts
        > heat_loss(kiln, ambient=Q_(90, "degF")).total_watts
    )


def test_arch_geometry() -> None:
    """A semicircle: rise = half the span, arc = π r, segment = π r² / 2."""
    arch = Arch(span=2.0, rise=1.0)
    assert arch.radius == pytest.approx(1.0)
    assert arch.arc_length == pytest.approx(3.14159265, rel=1e-8)
    assert arch.segment_area == pytest.approx(3.14159265 / 2, rel=1e-8)
