"""v2's zone and firing on IDA (`heat/zone.py`, `heat/firing.py`, `heat/kiln.py`): the energy
balance closes, IDA converges, each mode runs, and what isn't modelled is refused with its reason.
The reference kilns' own firings are in `test_heat_reference_firings.py`."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

import fuel as kiln_fuel
import heat_cases as hc
import numpy as np
import pytest
import yaml

from kilndesigner.designfile import load_design
from kilndesigner.library import Material, material
from kilndesigner.model import Kiln
from kilndesigner.model import Layer as DesignLayer
from kilndesigner.units import Q_
from kilndesigner.v2.heat import air as air_mod
from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import gas
from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat.zone import ACC, Balance, ZoneModel

OLSEN = Path(__file__).resolve().parents[3] / "examples" / "olsen"
IN = 0.0254
pytestmark = [pytest.mark.slow, pytest.mark.geometry]


def _design(name: str, change: dict[str, Any]) -> Kiln:
    data = yaml.safe_load((OLSEN / f"{name}.yaml").read_text(encoding="utf-8"))
    for key, value in change.items():
        node = data
        *parents, last = key.split(".")
        for p in parents:
            node = node.setdefault(p, {})
        node[last] = value
    return Kiln.model_validate(data)


def test_the_energy_balance_closes() -> None:
    """Over the p.309 log: the fuel's net heat = flue + walls + setting + openings, to
    round-off, every instant integrated (the gas row is the balance)."""
    f = hc.fast_fire_log()
    e = f.energy
    closure = e["fuel heat"] - e["flue"] - e["walls"] - e["setting"] - e["openings"]
    assert abs(closure) < 1e-9 * e["fuel heat"]
    assert e["fuel heat"] == pytest.approx(f.fuel_kg * hc.fast_fire_model().products.net_heat)
    assert any(s.name == "Where the fuel's heat went" for s in f.steps)


def test_ida_converges_in_its_tolerance() -> None:
    """Max fire at rtol 1e-5 and 1e-7: cone 10 within 0.2 %."""
    m = hc.fast_fire_model()
    a = fi.fire(m, fi.MaxFire(), 2 * 3600.0, (), hc.CONE_10)
    b = fi.fire(m, fi.MaxFire(), 2 * 3600.0, (), hc.CONE_10, rtol=1e-7)
    ta, tb = a.reached(hc.CONE_10), b.reached(hc.CONE_10)
    assert ta is not None
    assert tb is not None
    assert ta == pytest.approx(tb, rel=2e-3)


def test_the_gas_held_to_the_log() -> None:
    """The log's temperatures held by the gas instead (the thermocouple read between gas and
    setting): the setting lags the gas and ends short of it."""
    pts = tuple((mi * 60.0, c + 273.15) for mi, c in hc.LOG)
    f = fi.fire(hc.fast_fire_model(), fi.Schedule("gas", pts), hc.LOG[-1][0] * 60.0)
    assert f.completed
    assert f.t_gas[-1] == pytest.approx(1285 + 273.15, abs=1e-3)
    assert f.t_setting[-1] < f.t_gas[-1]
    assert f.worst_air_share < 1.0


def test_a_schedule_at_its_breaks() -> None:
    s = fi.Schedule("gas", ((0.0, 300.0), (100.0, 400.0), (300.0, 400.0)))
    assert s.at(50.0) == pytest.approx((350.0, 1.0))
    assert s.at(100.0) == pytest.approx((400.0, 1.0))
    assert s.at(100.0, start=100.0) == pytest.approx((400.0, 0.0))
    assert s.at(500.0) == (400.0, 0.0)
    with pytest.raises(fi.FiringError, match="two or more points"):
        fi.Schedule("gas", ((0.0, 300.0),))
    with pytest.raises(fi.FiringError, match="increasing"):
        fi.Schedule("gas", ((0.0, 300.0), (0.0, 400.0)))


def test_when_the_setting_reached_a_temperature() -> None:
    f = hc.fast_fire_log()
    assert f.reached(hc.CONE_10) == pytest.approx(245 * 60.0, rel=1e-6)  # the log's 9:00
    t = f.reached(900 + 273.15)
    assert t is not None
    assert 95 * 60 - 60 < t < 95 * 60 + 60  # the log's 900 °C at 6:30
    assert f.reached(250.0) == 0.0
    assert f.reached(2000.0) is None


def test_a_target_reached_to_round_off_is_reached() -> None:
    """A setting held to a schedule reaches a break's temperature only to round-off, and IDA
    gives no event where its root is zero as the next piece starts: the first sample within the
    temperatures' tolerance counts, not the one after it."""
    t = np.array([0.0, 60.0, 120.0, 180.0])
    s = np.array([[300.0], [1500.0], [1558.15 - 1e-7], [1558.15]])
    f = fi.Firing(t, s, s, np.zeros(4), np.zeros(4), {}, {}, True, "")
    assert f.reached(1558.15) == pytest.approx(120.0)
    assert f.reached(1529.075) == pytest.approx(90.0, rel=1e-6)  # halfway, interpolated
    assert f.reached(1600.0) is None


def test_max_fire_needs_a_draft() -> None:
    k = hc._crossdraft(hc.FLUE)  # pyright: ignore[reportPrivateUsage]
    m = hk.heat_model(k, hc.CROSSDRAFT_LOAD, 1.0, n_rays=5_000)
    assert m.draft is None
    with pytest.raises(fi.FiringError, match="max fire needs"):
        fi.fire(m, fi.MaxFire(), 3600.0)
    f = fi.fire(m, fi.FixedInput(0.0012), 1800.0)
    assert np.isnan(f.worst_air_share)
    share = next(s for s in f.steps if s.name == "Air needed over the most the draft draws")
    assert "isn't built" in share.value
    assert "the burners'" in f.steps[-1].inputs["how"]


def test_an_impossible_start_is_refused() -> None:
    m = hc.fast_fire_model()
    with pytest.raises(fi.FiringError, match="no consistent start"):
        fi.fire(m, fi.Schedule("setting", ((0.0, 3500.0), (60.0, 3500.0))), 60.0)


def test_a_gas_past_the_tables_is_refused() -> None:
    m = hc.fast_fire_model()
    bal = Balance(m)
    lay = bal.lay
    y = np.full((2, lay.size), 300.0)
    y[:, lay.tg] = 3200.0
    with pytest.raises(fi.FiringError, match="past the gas tables"):
        fi._record(m, bal, fi.MaxFire(), np.array([0.0, 1.0]), y, {}, True, "")  # pyright: ignore[reportPrivateUsage]
    y[:, lay.tg] = 200.0
    with pytest.raises(fi.FiringError, match="below the gas tables"):
        fi._record(m, bal, fi.MaxFire(), np.array([0.0, 1.0]), y, {}, True, "")  # pyright: ignore[reportPrivateUsage]


def test_other_grey_gases() -> None:
    k = load_design(OLSEN / "fast-fire.yaml")
    for wsgg, name in (("dorigon2013", "Dorigon"), ("transparent", "transparent")):
        m = hk.heat_model(k, hc.FAST_FIRE_LOAD, 1.0, hc.WOOD, wsgg=wsgg, n_rays=5_000)  # pyright: ignore[reportArgumentType]
        step = next(s for s in m.steps if s.name == "Gas radiation")
        assert name in step.value


def test_what_the_heat_model_refuses(monkeypatch: pytest.MonkeyPatch) -> None:
    ff = load_design(OLSEN / "fast-fire.yaml")
    with pytest.raises(hk.NotModelledError, match="the wood's moisture"):
        hk.fuel_of(ff, None)
    own = {"heating_value": "19 MJ/kg", "moisture": "12 percent",
           "firebox_efficiency": "25 percent"}  # fmt: skip
    wooded = _design("fast-fire", {"site.wood": own})
    assert hk.fuel_of(wooded, None).moisture == pytest.approx(0.12)
    singh = load_design(OLSEN / "singh-coal.yaml")
    with pytest.raises(hk.NotModelledError, match="give the fuel's analysis"):
        hk.fuel_of(singh, None)
    coal = kiln_fuel.own_fuels("singh-coal")[0]
    assert hk.fuel_of(singh, coal) is coal  # each kiln's own fuel (ADR 0017 decision 12)
    with pytest.raises(hk.NotModelledError, match="the design burns wood"):
        hk.fuel_of(ff, coal)
    electric = load_design(OLSEN / "electric-car-45.yaml")
    assert hk.fuel_of(electric, None) is gas.ELECTRIC  # its elements as face sources (C2)
    both = {"fuel": "natural_gas", "burners": {"rating": "36000 BTU/hr", "count": 2},
            "supply": {"type": "line", "pressure": "8 inch_H2O"}}  # fmt: skip
    with pytest.raises(hk.NotModelledError, match="one kind of heat"):
        hk.fuel_of(_design("fast-fire", {"heat.gas": both}), None)
    hybrid = _design("electric-car-45", {"heat.gas": both})
    with pytest.raises(hk.NotModelledError, match="hybrid"):
        hk.fuel_of(hybrid, None)
    propane = _design("olsen-crossdraft-36", {"heat.gas.fuel": "propane"})
    assert hk.fuel_of(propane, None).name == "propane"
    outside = replace(hc.FAST_FIRE_LOAD, hi=(9 * IN, 12.5 * IN, 40 * IN))
    with pytest.raises(hk.NotModelledError, match="inside its chamber"):
        hk.heat_model(ff, outside, 1.0, hc.WOOD, n_rays=1_000)
    with pytest.raises(hk.NotModelledError, match="no hot-face emissivity"):
        hk._emissivity("calcium-silicate-promasil-1100")  # pyright: ignore[reportPrivateUsage]
    # Every library material has a c_p now (a castable the class value, C2): a board without one
    board = DesignLayer(material="calcium-silicate-promasil-1100", thickness=Q_(2, "in"))

    def no_cp(mid: str) -> Material:
        return material(mid).model_copy(update={"specific_heat": None})

    monkeypatch.setattr(hk, "material", no_cp)
    with pytest.raises(hk.NotModelledError, match="no specific heat"):
        hk._layer(board)  # pyright: ignore[reportPrivateUsage]
    given = board.model_copy(update={"specific_heat": Q_(1.0, "kJ/(kg*K)")})
    assert hk._layer(given).heat_capacity.cp(np.array([800.0]))[0] == pytest.approx(1000.0)  # pyright: ignore[reportPrivateUsage]
    monkeypatch.undo()
    no_rating = _design("olsen-crossdraft-36", {"heat.gas.burners.rating": None})
    assert hk.rated_fuel(no_rating, hk.fuel_of(no_rating, None)) is None
    round_ = load_design(OLSEN / "kenzan-muffle.yaml")  # a round chamber is taken (C2), but the
    with pytest.raises(hk.NotModelledError, match="inside its chamber"):  # fast-fire's box pokes
        hk.heat_model(round_, hc.FAST_FIRE_LOAD, 1.0, hc.WOOD, n_rays=1_000)  # out of it


def test_the_whole_path_closes_and_cools_along_it() -> None:
    """The fast-fire as firebox, chamber and chimney (H13): the fuel burns in the firebox; each
    zone's gas cooler than the last's; the balance closes to round-off and the walls' share is
    the zones' shares summed; the floor between firebox and chamber takes heat from both sides,
    its underside hotter than its top while the fire is on."""
    m = hc.fast_fire_model()
    assert [g.name for g in m.gas] == ["firebox", "chamber", "chimney"]
    assert m.burns == 0
    f = fi.fire(m, fi.MaxFire(), 3 * 3600.0, (), hc.CONE_10)
    assert f.completed
    late = f.times > 600.0
    assert np.all(f.t_gases[late, 0] > f.t_gases[late, 1])
    assert np.all(f.t_gases[late, 1] > f.t_gases[late, 2])
    e = f.energy
    closure = e["fuel heat"] - e["flue"] - e["walls"] - e["setting"] - e["openings"]
    assert abs(closure) < 1e-9 * e["fuel heat"]
    zones = sum(e[f"walls: {g}"] for g in ("firebox", "chamber", "chimney"))
    assert zones == pytest.approx(e["walls"], rel=1e-9)
    floor = next(x for x in m.faces if x.name == "floor")
    assert floor.back == "firebox roof"
    assert floor.back_zone == 0
    assert "firebox walls" in {x.name for x in m.faces}
    assert any(o.kind == "flame" and o.zone == 0 for o in m.openings)  # the grate
    assert any(s.name == "The gas zones" for s in m.steps)


@pytest.mark.parametrize("held", ["gas", "setting"])
def test_a_schedule_held_on_the_whole_path(held: str) -> None:
    pts = ((0.0, 294.26), (1800.0, 900.0), (3600.0, 1100.0))
    m = hc.fast_fire_model()
    f = fi.fire(m, fi.Schedule(held, pts), 3600.0)  # pyright: ignore[reportArgumentType]
    assert f.completed
    col = f.t_gas if held == "gas" else f.t_setting
    assert col[-1] == pytest.approx(1100.0, abs=0.01)
    assert f.worst_air_share_smooth <= f.worst_air_share


def test_one_zone_is_the_model_as_first_built() -> None:
    """The chamber alone as the zone the fire burns in (``path`` False): the max fire reaches
    cone 10 far sooner than the whole path does, as the model did before the fireboxes and
    chimney were zones (0.395 h on fluids' round-pipe fittings, the flat plate and wood at 12 %;
    0.41 h on Idelchik's and the duct forms; 0.48 h on the kiln's own wood at its bands'
    middles, 18.5 %, B4)."""
    m = hc.fast_fire_model(path=False)
    assert len(m.gas) == 1
    f = fi.fire(m, fi.MaxFire(), 3600.0, (), hc.CONE_10)
    t = f.reached(hc.CONE_10)
    assert t is not None
    assert t == pytest.approx(0.48 * 3600, rel=0.02)


# --- λ from the intakes and the draft (ADR 0017 decision 9; B4 step 4) -------------------------


def test_the_log_on_the_drafts_own_air() -> None:
    """p.309's log with all the air the chimney draws through the intakes (open) burning the
    wood: λ follows from the draft, above 1 throughout (the open kiln carries its log in
    oxidation), and the wood is more than the stoker's λ 1 needs, its excess air heated."""
    f = hc.fast_fire_log("draft")
    assert f.completed
    assert 1.0 < f.lam.min() < 1.3
    assert f.lam.max() > 3.0  # holding at cone 10 the wood is small and the draft strong
    assert f.fuel_kg > 1.4 * hc.fast_fire_log().fuel_kg
    step = f.steps[-1]
    assert step.name == "λ through the firing"
    assert "intakes 100% open" in step.inputs["how"]
    assert "no source gives a burning rate for wood" in (step.note or "")


def test_stoking_faster_than_the_air_burns_is_reduction() -> None:
    """From the log's state at 1016 °C, wood fed faster than the draft's air burns: λ under 1
    (reduction, the CO and H₂ unburnt), and past 0.8, the least checked, held there and said."""
    split = 125 * 60.0
    first = tuple(p for p in hc.LOG_POINTS if p[0] <= split)
    m = hc.fast_fire_model()
    a = fi.fire(m, fi.Schedule("setting", first, air="draft"), split)
    rich = fi.fire(m, fi.FixedInput(0.016, air="draft"), 1800.0, start=a.state)
    assert 0.8 < rich.lam.min() <= rich.lam.max() < 0.95
    assert "reduction" in rich.steps[-1].value
    richer = fi.fire(m, fi.FixedInput(0.02, air="draft"), 1800.0, start=a.state)
    assert richer.lam.min() < 0.8
    assert "held there" in richer.steps[-1].value
    gain = richer.t_setting[-1] - rich.t_setting[-1]
    assert gain < 0.25 * (rich.t_setting[-1] - a.t_setting[-1])  # more wood, little more heat


def test_coal_burns_no_more_than_its_grates_take() -> None:
    """The fast-fire on Kato's coal (a test of the bed's limit: the kiln burns wood): at the
    hand-fired grates' least, 85 kg/(m²·h), the max fire burns no more than the grates take, the
    rest of the draft's air passing as excess (λ above 1)."""
    k = _design("fast-fire", {"heat.fire.fuel": "coal"})
    coal = kiln_fuel.own_fuels("kato-coal")[0]
    rate = air_mod.COAL_BED[0]
    m = hk.heat_model(k, hc.FAST_FIRE_LOAD, 1.0, coal, n_rays=5_000, grate_bar=0.75 * IN,
                      path=True, bed_rate=rate)  # fmt: skip
    assert m.bed is not None
    assert m.bed == pytest.approx(rate * 2 * 12 * 24 * IN**2 * 0.9)
    f = fi.fire(m, fi.MaxFire(), 1800.0)
    assert f.fuel_rate.max() <= m.bed * (1 + 1e-6)
    assert f.bed_share == pytest.approx(1.0, abs=1e-3)
    assert f.lam.max() > 1.2
    assert "the grates'" in f.steps[-1].inputs["how"]
    assert any("burn at most 85 kg" in (s.value or "") for s in m.steps)
    no_rate = hk.heat_model(k, hc.FAST_FIRE_LOAD, 1.0, coal, n_rays=2_000, path=True)
    assert no_rate.bed is None
    assert any("the bed's burning rate not given" in (s.value or "") for s in no_rate.steps)


def test_the_emissivity_classes_and_a_bed_without_grates() -> None:
    """The class's ends (MPK 140 under MPK 125, medium-alumina fire brick under low, × 0.95–1.0
    hemispherical); a coal bed's rate with no grate to act on is said and left out."""
    t = np.array([1500.0])
    low, high = (hk._emissivity("ifb-k23", c)(t)[0] for c in ("low", "high"))  # pyright: ignore[reportPrivateUsage, reportArgumentType]
    assert low < high
    dense = hk._emissivity("firebrick-medium-duty-smithfield", "high")  # pyright: ignore[reportPrivateUsage]
    assert dense.name == "dense-low"
    assert dense.factor == 1.0
    coal = kiln_fuel.own_fuels("kato-coal")[0]
    bare = _design("fast-fire", {"heat.fire.fuel": "coal"})
    fb = bare.heat.fire.fireboxes[0]  # pyright: ignore[reportOptionalMemberAccess]
    bare.heat.fire.fireboxes[0] = fb.model_copy(update={"grate": None})  # pyright: ignore[reportOptionalMemberAccess]
    notes: list[str] = []
    assert hk._bed(bare, coal, air_mod.COAL_BED[1], notes) is None  # pyright: ignore[reportPrivateUsage]
    assert "no grate given" in notes[0]


def test_the_drafts_own_air_needs_a_draft() -> None:
    k = hc._crossdraft(hc.FLUE)  # pyright: ignore[reportPrivateUsage]
    m = hk.heat_model(k, hc.CROSSDRAFT_LOAD, 1.0, n_rays=2_000)
    with pytest.raises(fi.FiringError, match="draft's own air needs"):
        fi.fire(m, fi.FixedInput(0.001, air="draft"), 600.0)
    with pytest.raises(fi.FiringError, match="a share of more than 0"):
        fi.FixedInput(0.001, air="draft", opened=0.0)
    with pytest.raises(fi.FiringError, match="a share of more than 0"):
        fi.Schedule("gas", ((0.0, 300.0), (60.0, 400.0)), opened=1.5)


def test_a_chimney_of_clay_flue_liners() -> None:
    """Olsen's fast-fire chimney "made from chimney flues" (Fig 5-37): its walls a fireclay body
    0.63 in thick (clay-flue-liners.md, Derived from Rumford's weights), an eighth of the mass of
    the engine's 4½ in of hard brick, said in the working."""
    k = load_design(OLSEN / "fast-fire.yaml")
    m = hk.heat_model(k, hc.FAST_FIRE_LOAD, 1.0, hc.WOOD, n_rays=2_000, path=True,
                      chimney=hk.flue_liner())  # fmt: skip
    walls = next(f for f in m.faces if f.name == "chimney walls").wall.layers
    assert [x.name for x in walls] == ["firebrick-medium-duty-smithfield"]
    assert walls[0].thickness == pytest.approx(0.63 * IN)
    said = next(s for s in m.steps if s.name == "Said about the model").value
    assert "clay flue liners" in said
    other = hk.heat_model(k, hc.FAST_FIRE_LOAD, 1.0, hc.WOOD, n_rays=2_000, path=True,
                          chimney=hk.flue_liner() * 2)  # fmt: skip
    assert (
        "the chimney's walls: given"
        in next(s for s in other.steps if s.name == "Said about the model").value
    )


def test_a_round_chimney_as_a_zone_is_a_round_duct() -> None:
    """The chimney zone's convection takes a round chimney's own area and diameter."""
    k = _design("fast-fire", {"draft.chimney.inside": {"diameter": "10 in"}})
    m = hk.heat_model(k, hc.FAST_FIRE_LOAD, 1.0, hc.WOOD, n_rays=2_000, path=True)
    chimney = next(g for g in m.gas if g.name == "chimney")
    assert chimney.flow.area == pytest.approx(np.pi * (10 * IN) ** 2 / 4)
    assert chimney.flow.duct == pytest.approx(10 * IN)


def test_a_model_names_every_surface() -> None:
    m = hc.fast_fire_model()
    with pytest.raises(ValueError, match="every surface"):
        ZoneModel(m.products, m.exchange, (*m.names, "ghost"), m.faces, m.settings, m.openings,
                  m.gas, m.t_room)  # fmt: skip
    with pytest.raises(ValueError, match="without a load"):
        ZoneModel(m.products, m.exchange, m.names, m.faces, (), m.openings, m.gas, m.t_room)
    assert ACC[0] == "fuel kg"
    assert m.flow is m.gas[0].flow
