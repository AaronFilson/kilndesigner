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
    castable_reports,
    conductivity_law,
    mix_material,
)
from kilndesigner.heatloss import HeatLoss, heat_loss
from kilndesigner.model import CastableMix, Kiln
from kilndesigner.report import design_report
from kilndesigner.units import Q_, parse_quantity, si

EXAMPLES = Path(__file__).parents[2] / "examples"
KILN = load_design(EXAMPLES / "diy-castable-test-kiln.yaml")
FRONT_LOADER = load_design(EXAMPLES / "electric-front-loader.yaml")
LB = 0.45359237  # kg
# A cement-bonded foamed mix: nothing in it burns, converts or inverts
FOAMED: dict[str, object] = {
    "id": "foamed-mulcoa",
    "name": "Foamed Mulcoa and Secar 71",
    "ingredients": [
        {"ingredient": "mulcoa-70", "mass": "40 lb", "price": "1.00 USD/lb"},
        {"ingredient": "secar-71", "mass": "5 lb"},
    ],
    "water": "5 lb",
    "foam": 50,
}
# A burnout mix, unfoamed: the corn starch leaves the pores
STARCH: dict[str, object] = {
    "id": "starch-mix",
    "name": "Molochite, Secar 71 and corn starch",
    "ingredients": [
        {"ingredient": "molochite", "mass": "20 lb"},
        {"ingredient": "secar-71", "mass": "5 lb"},
        {"ingredient": "cornstarch", "mass": "10 lb"},
    ],
    "water": "10 lb",
}


def _layer(material: str, thickness: str) -> dict[str, str]:
    return {"material": material, "thickness": thickness}


def _front_loader_with(
    castables: list[dict[str, object]],
    walls: list[dict[str, str]],
    roof: list[dict[str, str]] | None = None,
) -> Kiln:
    """The cone 10 front-loader (11.52 kW) with castables in its lining."""
    data = FRONT_LOADER.model_dump(mode="json", by_alias=True)
    data["castables"] = castables
    data["lining"] = {**data["lining"], "walls": walls, "roof": roof or data["lining"]["roof"]}
    return Kiln.model_validate(data)


def _fahrenheit(kelvin: float) -> str:
    return f"{(kelvin - 273.15) * 1.8 + 32:.0f} °F"


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


def test_an_unknown_ingredient_is_refused() -> None:
    with pytest.raises(
        CastableError, match="test: no ingredient 'grog'; the library has: ciment-fondu, cornstarch"
    ):
        analyse_mix(KILN, _mix([("mulcoa-70", 40), ("grog", 5)], 5, foam=50))


def test_a_measured_fired_density_replaces_the_estimate() -> None:
    measured = CastableMix.model_validate(
        {
            "id": "test",
            "name": "test",
            "ingredients": [{"ingredient": i, "mass": f"{m} lb"} for i, m in BACKUP],
            "water": "14.5 lb",
            "foam": 60,
            "measured": {"fired_density": "35 lb/ft**3", "linear_shrinkage": 1.5},
        }
    )
    a = analyse_mix(KILN, measured)
    assert a.fired_density_kg_m3 == pytest.approx(si(Q_(35, "lb/ft**3"), "kg/m**3"))
    step = next(s for s in a.working if s.name == "Fired density")
    assert step.formula == "measured on test pieces"
    assert step.inputs == {"linear shrinkage": "1.5 %"}
    estimated = analyse_mix(KILN, _mix(BACKUP, 14.5, foam=60))
    guess = next(s for s in estimated.working if s.name == "Fired density")
    assert guess.inputs == {"linear shrinkage": "0.0 % (assumed)"}
    # The estimate is about 31 lb/ft³; the denser measured piece conducts more
    assert estimated.fired_density_kg_m3 < a.fired_density_kg_m3
    law = conductivity_law()
    assert law.k(a.fired_density_kg_m3, 1000) > law.k(estimated.fired_density_kg_m3, 1000)


def test_a_mix_denser_than_its_solids_is_refused() -> None:
    """40 lb of Mulcoa 70 (2.88 g/cm³, no LOI) is 6.30 L of solid; with 4 lb (1.81 L) of water it
    casts 8.11 L. A measured 20 % linear shrinkage would leave 0.8³ of that, 4.15 L: less than
    the solid alone, so the measurements can't both be right."""
    mix = CastableMix.model_validate(
        {
            "id": "test",
            "name": "test",
            "ingredients": [{"ingredient": "mulcoa-70", "mass": "40 lb"}],
            "water": "4 lb",
            "measured": {"linear_shrinkage": 20},
        }
    )
    solid, water = 40 * LB / 2880, 4 * LB / 1000
    assert (solid + water) * 0.8**3 < solid
    with pytest.raises(CastableError, match="test: the fired mix would be denser than its solids"):
        analyse_mix(KILN, mix)


@pytest.fixture(scope="module")
def foamed_kiln() -> tuple[Kiln, HeatLoss]:
    """Foamed castable behind 4½ in of JM 26 in the walls; the starch mix is listed but unused."""
    kiln = _front_loader_with(
        [FOAMED, STARCH], walls=[_layer("ifb-jm26", "4.5 in"), _layer("foamed-mulcoa", "2 in")]
    )
    return kiln, heat_loss(kiln)


def test_a_mix_with_nothing_that_changes_in_the_wall(foamed_kiln: tuple[Kiln, HeatLoss]) -> None:
    kiln, loss = foamed_kiln
    mix = kiln.castable("foamed-mulcoa")
    assert mix is not None
    cast = analyse_mix(kiln, mix).cast_volume_m3
    report, _ = castable_reports(kiln, loss, 11_520, {"foamed-mulcoa": 2 * cast})
    # Two batches' worth placed, with 10 % for waste, is three batches
    assert report.batches == 3
    assert [(t.amount, t.cost) for t in report.totals] == [("120 lb", 120.0), ("15 lb", None)]
    # No organics, kyanite or quartz: each layer gets its thickness and temperatures
    assert [use.face for use in report.layers] == ["left", "right", "back", "front"]
    for use in report.layers:
        layer = next(f.layers[1] for f in loss.faces if f.face == use.face)
        hot, cold = _fahrenheit(layer.hot_side_k), _fahrenheit(layer.cold_side_k)
        assert use.notes == [f"2 in, from {hot} to {cold}."]
    # The first firing drives off water only: 2 batches × 5 lb, at 2256.4 kJ/kg
    assert [s.name for s in report.first_firing] == [
        "Water to drive off",
        "Steam pressure if water is trapped",
    ]
    boil_kwh = 10 * LB * 2256.4e3 / 3.6e6
    assert report.first_firing[0].value == f"10 lb; {boil_kwh:.3g} kWh to boil it"
    assert report.first_firing[0].note == (
        "Some water stays bound in the cement until it is heated further."
    )
    # Mizzou's dry-out [S41]: 75 °F/h from 70 °F, with ½ h per inch held at 250, 500 and 1000 °F,
    # then on to 2345 °F
    assert [s.hold for s in report.schedule] == ["1.0 h", "1.0 h", "1.0 h", None]
    assert report.schedule_hours == pytest.approx((2345 - 70) / 75 + 3 * 1.0)
    foam = "Fold in foam until the mix is 50 % of the cast volume air"
    assert any(s.startswith(foam) for s in report.steps)
    assert any(s.startswith("Cure it 16–24 h above 60 °F") for s in report.steps)


def test_a_mix_the_lining_doesnt_use(foamed_kiln: tuple[Kiln, HeatLoss]) -> None:
    kiln, loss = foamed_kiln
    _, unused = castable_reports(kiln, loss, 11_520, {})
    assert unused.mix.id == "starch-mix"
    assert (unused.placed, unused.batches, unused.layers) == ("none", 0, [])
    assert all(t.amount_lb == 0 for t in unused.totals)
    assert unused.first_firing == []
    assert (unused.schedule, unused.schedule_hours) == ([], None)
    assert "Molochite, Secar 71 and corn starch is not used in the lining." in [
        f.message for f in unused.findings
    ]


@pytest.fixture(scope="module")
def starch_kiln() -> tuple[Kiln, HeatLoss, float]:
    """The burnout mix behind JM 26 in the walls, and behind JM 26 and 2 in of blanket in the
    roof; with the cast volume of one batch."""
    kiln = _front_loader_with(
        [STARCH],
        walls=[_layer("ifb-jm26", "4.5 in"), _layer("starch-mix", "2 in")],
        roof=[
            _layer("ifb-jm26", "4.5 in"),
            _layer("kaowool-blanket-8pcf", "2 in"),
            _layer("starch-mix", "1 in"),
        ],
    )
    mix = kiln.castable("starch-mix")
    assert mix is not None
    return kiln, heat_loss(kiln), analyse_mix(kiln, mix).cast_volume_m3


def test_organics_that_never_reach_240_c_never_burn_out(
    starch_kiln: tuple[Kiln, HeatLoss, float],
) -> None:
    """Organics burn from about 240 °C (464 °F) [S54]: behind 2 in of blanket the roof's layer
    stays below it, while the walls' layer, behind brick alone, passes it."""
    kiln, loss, cast = starch_kiln
    [report] = castable_reports(kiln, loss, 11_520, {"starch-mix": 5 * cast})
    roof = next(f for f in loss.faces if f.face == "roof").layers[2]
    assert roof.hot_side_k < 240 + 273.15
    [roof_use] = [use for use in report.layers if use.face == "roof"]
    assert roof_use.notes == [
        "The whole layer stays below 464 °F: the organics never burn out, and the binder stays "
        "as it dried (castables.md §7 [S54] (excerpt))."
    ]
    wall = next(f for f in loss.faces if f.face == "left").layers[1]
    assert wall.hot_side_k > 240 + 273.15
    [left_use] = [use for use in report.layers if use.face == "left"]
    assert left_use.notes[0].startswith("The organics are gone from the hottest")


def test_burning_out_more_than_the_kilns_own_heat_is_a_warning(
    starch_kiln: tuple[Kiln, HeatLoss, float],
) -> None:
    """Five batches hold 50 lb of corn starch at 4.16 kcal/g [S51]: 395 MJ. Spread over the climb
    from 464 to 1022 °F at 75 °F/h (7.44 h), that is 14.7 kW, 1.3 times the kiln's 11.52 kW."""
    kiln, loss, cast = starch_kiln
    [report] = castable_reports(kiln, loss, 11_520, {"starch-mix": 5 * cast})
    heat = 5 * 10 * LB * 4.16 * 4184e3
    window_h = (550 - 240) * 1.8 / 75
    rate = heat / (window_h * 3600)
    assert f"{rate / 1000:.3g}" == "14.7"
    step = next(s for s in report.first_firing if s.name == "Burnout heat, spread over the window")
    assert step.value == f"{rate / 1000:.3g} kW for about {window_h:.1f} h"
    assert step.inputs["the kiln's own heat"] == f"11.5 kW ({rate / 11_520:.1f}×)"
    [warning] = [f for f in report.findings if "can run away" in f.message]
    assert warning.level == "warning"
    assert f"about 14.7 kW through the burnout window, {rate / 11_520:.1f} times" in warning.message
    # Unfoamed, so the check on each batch is the weight of a level US quart (0.946353 L)
    volume = (20 / 2700 + 5 / 2940 + 10 / 1500 + 10 / 1000) * LB  # m³ per batch
    quart_lb = 45 * LB / volume * 0.946353e-3 / LB
    assert any(f"a level US quart weighs {quart_lb:.3g} lb" in s for s in report.steps)


def test_without_the_kilns_heat_the_burnout_isnt_compared(
    starch_kiln: tuple[Kiln, HeatLoss, float],
) -> None:
    kiln, loss, cast = starch_kiln
    [report] = castable_reports(kiln, loss, None, {"starch-mix": 5 * cast})
    step = next(s for s in report.first_firing if s.name == "Burnout heat, spread over the window")
    assert "the kiln's own heat" not in step.inputs
    assert not [f for f in report.findings if "can run away" in f.message]
    assert any("burn out as smoke" in f.message for f in report.findings)
