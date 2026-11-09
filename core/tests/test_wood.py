"""Wood per firing, from the user's own heating value, moisture and firebox efficiency."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from kilndesigner import Kiln, load_design
from kilndesigner.model import WoodFuel
from kilndesigner.simulation import simulate
from kilndesigner.wood import WoodError, wood_per_firing

EXAMPLES = Path(__file__).parents[2] / "examples"
# Test inputs: Forest Research's oven-dry wood (19 GJ/t net) at its air-dry 20 % (wood-fuel.md),
# USU's white pine cord (2250 lb); the efficiency and price are a user's own, not data.
WOOD = {
    "heating_value": "19 MJ/kg",
    "moisture": "20 percent",
    "firebox_efficiency": "25 percent",
    "cord_weight": "2250 lb/cord",
    "price": "250 USD/cord",
}


def test_a_worked_example_by_hand() -> None:
    """100 kWh = 360 MJ into the kiln. H(w) = 19 × 0.8 − 2.44 × 0.2 = 14.712 MJ/kg, which is
    Forest Research's 14.7 GJ/t for logs at 20 %. m = 360 ÷ (0.25 × 14.712) = 97.879 kg as fired,
    78.303 kg oven-dry; a cord of 2250 lb is 1020.583 kg, so 0.076724 cord, at $250 $19.18."""
    w = wood_per_firing(360e6, WoodFuel.model_validate(WOOD))
    assert w.as_fired_kg == pytest.approx(97.879, abs=1e-3)
    assert w.oven_dry_kg == pytest.approx(78.303, abs=1e-3)
    assert w.cords == pytest.approx(0.076724, rel=1e-4)
    assert w.cost_usd == pytest.approx(19.181, abs=1e-3)
    assert w.working[0].value == "14.71 MJ/kg as fired"
    assert "FAO" in (w.working[0].reference or "")
    assert [s.name for s in w.working][-1] == "Cost of the wood"


def test_without_a_cord_weight_the_wood_is_by_weight_only() -> None:
    kept = {k: v for k, v in WOOD.items() if k not in ("cord_weight", "price")}
    wood = WoodFuel.model_validate(kept)
    w = wood_per_firing(360e6, wood, us=True)
    assert w.cords is None
    assert w.cost_usd is None
    assert "lb" in w.working[1].value


def test_a_cord_weight_without_a_price_gives_cords_but_no_cost() -> None:
    wood = WoodFuel.model_validate({k: v for k, v in WOOD.items() if k != "price"})
    w = wood_per_firing(360e6, wood)
    assert w.cords is not None
    assert w.cost_usd is None


def test_wood_too_wet_to_give_heat_is_refused() -> None:
    """At 89 %, 19 × 0.11 − 2.44 × 0.89 < 0: FAO's 'about 88 %' where wood gives nothing."""
    wood = WoodFuel.model_validate({**WOOD, "moisture": "89 percent"})
    with pytest.raises(WoodError, match="no heat"):
        wood_per_firing(360e6, wood)


@pytest.mark.parametrize(
    ("change", "message"),
    [
        ({"heating_value": "0 MJ/kg"}, "heating value"),
        ({"moisture": "100 percent"}, "moisture"),
        ({"firebox_efficiency": "0 percent"}, "efficiency"),
        ({"firebox_efficiency": "120 percent"}, "efficiency"),
        ({"cord_weight": "0 lb/cord"}, "cord weight"),
        ({"cord_weight": None}, "needs the cord_weight"),
        ({"heating_value": "19 kg"}, "heating value"),
    ],
)
def test_wood_values_are_checked(change: dict[str, object], message: str) -> None:
    with pytest.raises(ValidationError, match=message):
        WoodFuel.model_validate({**WOOD, **change})


def test_every_wood_value_is_the_users() -> None:
    for name in ("heating_value", "moisture", "firebox_efficiency"):
        with pytest.raises(ValidationError):
            WoodFuel.model_validate({k: v for k, v in WOOD.items() if k != name})


def _fast_fire(wood: dict[str, str] | None) -> Kiln:
    kiln = load_design(EXAMPLES / "olsen-32cuft-propane-wood-fastfire.yaml")
    doc = kiln.model_dump(by_alias=True, mode="json")
    doc["site"]["wood"] = wood
    return Kiln.model_validate(doc)


def test_the_gas_firing_of_a_wood_kiln_gives_its_wood() -> None:
    r = simulate(_fast_fire(WOOD), dt=300, record=False).result
    h_wet = 19 * 0.8 - 2.44 * 0.2
    assert r.wood_kg is not None
    assert r.wood_kg == pytest.approx(r.energy_kwh * 3.6 / (0.25 * h_wet), rel=1e-6)
    assert r.wood_oven_dry_kg == pytest.approx(r.wood_kg * 0.8)
    assert r.wood_cords is not None
    assert r.wood_cost_usd == pytest.approx(r.wood_cords * 250)
    assert any(s.name == "Cords per firing" for s in r.working)
    assert any("isn't simulated" in f.message for f in r.findings)


def test_a_wood_kiln_without_its_wood_says_what_it_needs() -> None:
    r = simulate(_fast_fire(None), dt=300, record=False).result
    assert r.wood_kg is None
    assert any("firebox_efficiency" in f.message for f in r.findings)


def test_wood_too_wet_is_said_in_the_firing() -> None:
    r = simulate(_fast_fire({**WOOD, "moisture": "95 percent"}), dt=300, record=False).result
    assert r.wood_kg is None
    assert any("no heat" in f.message for f in r.findings)
