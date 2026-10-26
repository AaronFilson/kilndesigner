"""Castables the builder mixes: conservation, the conductivity law against published bricks,
the first firing's chemistry, and refusals outside what's been checked (ADR 0009)."""

from __future__ import annotations

import math
from collections.abc import Sequence
from pathlib import Path

import pytest
from hypothesis import given
from hypothesis import strategies as st

from kilndesigner import load_design
from kilndesigner.castable import (
    GLUCAN_MOLAR_MASS,
    CastableError,
    analyse_mix,
    conductivity_law,
    mix_material,
)
from kilndesigner.model import CastableMix, Kiln
from kilndesigner.report import design_report
from kilndesigner.units import Q_, parse_quantity, si

EXAMPLES = Path(__file__).parents[2] / "examples"
KILN = load_design(EXAMPLES / "diy-castable-test-kiln.yaml")


def _mix(
    parts: Sequence[tuple[str, float]], water: float, foam: float | None = None, **kw: object
) -> CastableMix:
    return CastableMix.model_validate(
        {
            "id": "test",
            "name": "test",
            "ingredients": [{"ingredient": i, "mass": f"{m} lb", **kw} for i, m in parts],
            "water": f"{water} lb",
            "foam": foam,
        }
    )


BACKUP = [
    ("mulcoa-70", 15),
    ("greenstripe", 25),
    ("kyanite", 5),
    ("dextrin", 5),
    ("newsprint", 0.25),
]


def test_mass_and_volume_are_conserved() -> None:
    a = analyse_mix(KILN, _mix(BACKUP, 14.5, foam=60))
    wet = si(parse_quantity(a.wet_density), "kg/m**3")
    assert wet * a.cast_volume_m3 == pytest.approx(a.dry_mass_kg + a.water_kg, rel=1e-3)
    # With 60 % air the cast volume is 2.5 × what the solids and water fill on their own
    solids_and_water = (
        sum(si(parse_quantity(b.volume), "m**3") for b in a.batch) + a.water_kg / 1000
    )
    assert a.cast_volume_m3 == pytest.approx(solids_and_water / 0.4, rel=1e-3)
    dried = si(parse_quantity(a.dried_density), "kg/m**3")
    assert wet > dried > a.fired_density_kg_m3  # water, then LOI and organics, leave


def test_foam_is_what_makes_the_notes_backup_light() -> None:
    # The notes call this a "K16 type" at about 30 lb/ft³. With no foam it fires near 77.
    no_foam = analyse_mix(KILN, _mix(BACKUP, 14.5))
    assert si(Q_(no_foam.fired_density_kg_m3, "kg/m**3"), "lb/ft**3") == pytest.approx(77, abs=2)
    foamed = analyse_mix(KILN, _mix(BACKUP, 14.5, foam=60))
    assert si(Q_(foamed.fired_density_kg_m3, "kg/m**3"), "lb/ft**3") == pytest.approx(31, abs=1)


def test_the_conductivity_law_reproduces_the_published_bricks() -> None:
    law = conductivity_law()
    assert law.bricks == 9
    assert law.rms < 0.10
    # Each brick predicted from the other eight: the error the results quote
    assert law.worst < 0.25
    # K-26, 657 kg/m³: 0.26 W/(m·K) at 815 °C on Morgan's 2025 sheet
    assert law.k(657, 815 + 273.15) == pytest.approx(0.26, rel=0.15)


@given(st.floats(480, 1250), st.floats(480, 1250), st.floats(533, 1643))
def test_a_denser_mix_conducts_more(rho1: float, rho2: float, t: float) -> None:
    law = conductivity_law()
    lo, hi = sorted((rho1, rho2))
    assert law.k(lo, t) <= law.k(hi, t)


def test_a_mix_outside_the_checked_densities_is_refused() -> None:
    hot_face_no_foam = [("mulcoa-70", 26), ("greenstripe", 15), ("kyanite", 4), ("dextrin", 5)]
    with pytest.raises(CastableError, match="480 to 1250 kg/m³"):
        analyse_mix(KILN, _mix(hot_face_no_foam, 12))


def test_an_ingredient_without_a_sourced_density_must_be_given_one() -> None:
    with pytest.raises(CastableError, match="no density is sourced for Expanded perlite"):
        analyse_mix(KILN, _mix([("mulcoa-70", 40), ("perlite", 1)], 8))
    given_one = CastableMix.model_validate(
        {
            "id": "test",
            "name": "test",
            "ingredients": [
                {"ingredient": "mulcoa-70", "mass": "40 lb"},
                {"ingredient": "perlite", "mass": "1 lb", "density": "2.3 g/cm**3"},
            ],
            "water": "8 lb",
            "foam": 50,
        }
    )
    assert analyse_mix(KILN, given_one).batch[1].source.endswith("density given in the mix")
    secar = analyse_mix(KILN, _mix([("mulcoa-70", 40), ("secar-71", 5)], 5, foam=50))
    assert secar.sets == "cement"


def test_the_mix_takes_the_lowest_sourced_service_limit() -> None:
    a = analyse_mix(KILN, _mix([("mulcoa-70", 40), ("ciment-fondu", 5)], 5, foam=50))
    assert a.service_limit is not None
    assert si(parse_quantity(a.service_limit), "degC") == pytest.approx(1271, abs=1)
    unknown = analyse_mix(KILN, _mix(BACKUP, 14.5, foam=60))
    assert unknown.service_limit is None
    assert any("no source gives a service limit" in f.message for f in unknown.findings)


def test_the_kyanite_growth_bound_follows_from_its_densities() -> None:
    report = design_report(KILN)
    hot = next(c for c in report.castables if c.mix.id == "diy-hot-face")
    step = next(s for s in hot.first_firing if s.name == "Kyanite's growth, at most")
    a = hot.mix
    kyanite_volume = 4 * 0.45359237 / 3610
    expected = kyanite_volume / a.cast_volume_m3 * (3.61 / 3.03 - 1) / 3
    assert float(step.value.split()[0]) == pytest.approx(100 * expected, abs=0.01)


def test_burnout_chemistry() -> None:
    # (C6H10O5)n + 6n O2 → 6n CO2 + 5n H2O, per kg of glucan
    mol = 1 / GLUCAN_MOLAR_MASS
    assert 6 * mol * 0.032 == pytest.approx(1.184, abs=0.001)  # kg of oxygen
    assert 6 * mol * 0.04401 == pytest.approx(1.629, abs=0.001)  # kg of CO2
    assert 5 * mol * 0.018015 == pytest.approx(0.556, abs=0.001)  # kg of water
    report = design_report(KILN)
    backup = next(c for c in report.castables if c.mix.id == "diy-backup")
    burn = next(s for s in backup.first_firing if s.name == "Organics to burn out")
    organic_lb = float(burn.value.split()[0].replace(",", ""))
    heat_kwh = float(burn.value.split("releasing ")[1].split()[0].replace(",", ""))
    # 4.15–4.16 kcal/g
    assert heat_kwh * 3.6e6 / (organic_lb * 0.45359237) == pytest.approx(4.155 * 4184e3, rel=0.01)


def test_the_kyanite_in_the_backup_never_converts() -> None:
    report = design_report(KILN)
    backup = next(c for c in report.castables if c.mix.id == "diy-backup")
    assert all(any("never expands" in n for n in layer.notes) for layer in backup.layers)
    hot = next(c for c in report.castables if c.mix.id == "diy-hot-face")
    assert all(any("starts to convert" in n for n in layer.notes) for layer in hot.layers)


def test_the_dryout_holds_half_an_hour_per_inch_and_refuses_thick_layers() -> None:
    report = design_report(KILN)
    backup = next(c for c in report.castables if c.mix.id == "diy-backup")
    assert [s.hold for s in backup.schedule[:3]] == ["4.5 h"] * 3  # the 9 in walls
    thick = Kiln.model_validate(
        {**KILN.model_dump(mode="json", by_alias=True),
         "lining": {"walls": [{"material": "diy-hot-face", "thickness": "2 in"},
                              {"material": "diy-backup", "thickness": "10 in"}]}}
    )  # fmt: skip
    backup = next(c for c in design_report(thick).castables if c.mix.id == "diy-backup")
    assert not backup.schedule
    assert any(f.level == "error" and "up to 9 in" in f.message for f in backup.findings)


def test_batches_cover_the_layers_that_use_the_mix() -> None:
    report = design_report(KILN)
    for c in report.castables:
        placed = si(parse_quantity(c.placed), "m**3")
        assert c.batches * c.mix.cast_volume_m3 >= placed * 1.1 - 1e-9
        assert (c.batches - 1) * c.mix.cast_volume_m3 < placed * 1.1


def test_a_mix_is_a_lining_material() -> None:
    mix = KILN.castable("diy-backup")
    assert mix is not None
    m = mix_material(KILN, mix)
    assert m.max_service is None
    assert m.k.k(1000 + 273.15) == pytest.approx(
        conductivity_law().k(analyse_mix(KILN, mix).fired_density_kg_m3, 1273.15)
    )
    assert math.isfinite(si(parse_quantity(m.density), "kg/m**3"))


def test_one_kiln_dries_on_one_schedule_set_by_its_thickest_layer() -> None:
    """HarbisonWalker: the thickest section sets the schedule (castables-minerals.md §5)."""
    report = design_report(load_design(EXAMPLES / "diy-castable-test-kiln.yaml"))
    hours = {c.schedule_hours for c in report.castables if c.layers}
    assert len(hours) == 1
    assert any("castable in layers" in f.message for c in report.castables for f in c.findings)


def test_free_quartz_in_a_fireclay_is_noted() -> None:
    """Greenstripe is 10–20 % quartz by its SDS, though its role is clay."""
    report = design_report(load_design(EXAMPLES / "diy-castable-test-kiln.yaml"))
    notes = [n for c in report.castables for layer in c.layers for n in layer.notes]
    assert any("free quartz in Greenstripe" in n for n in notes)
