"""v2's zone and firing on IDA (`heat/zone.py`, `heat/firing.py`, `heat/kiln.py`): the energy
balance closes, IDA converges, each mode runs, and what isn't modelled is refused with its reason.
The reference kilns' own firings are in `test_heat_reference_firings.py`."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

import heat_cases as hc
import numpy as np
import pytest
import yaml

from kilndesigner.designfile import load_design
from kilndesigner.model import Kiln
from kilndesigner.model import Layer as DesignLayer
from kilndesigner.units import Q_
from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat.zone import Balance, Layout, ZoneModel

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
    assert f.steps[-2].name == "Where the fuel's heat went"


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


def test_max_fire_needs_a_draft() -> None:
    k = hc._crossdraft(hc.FLUE)  # pyright: ignore[reportPrivateUsage]
    m = hk.heat_model(k, hc.CROSSDRAFT_LOAD, 1.0, n_rays=5_000)
    assert m.draft is None
    with pytest.raises(fi.FiringError, match="max fire needs"):
        fi.fire(m, fi.MaxFire(), 3600.0)
    f = fi.fire(m, fi.FixedInput(0.0012), 1800.0)
    assert np.isnan(f.worst_air_share)
    assert "isn't built" in f.steps[-1].value


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


def test_what_the_heat_model_refuses() -> None:
    ff = load_design(OLSEN / "fast-fire.yaml")
    with pytest.raises(hk.NotModelledError, match="the wood's moisture"):
        hk.fuel_of(ff, None)
    own = {"heating_value": "19 MJ/kg", "moisture": "12 percent",
           "firebox_efficiency": "25 percent"}  # fmt: skip
    wooded = _design("fast-fire", {"site.wood": own})
    assert hk.fuel_of(wooded, None).moisture == pytest.approx(0.12)
    with pytest.raises(hk.NotModelledError, match="no composition"):
        hk.fuel_of(load_design(OLSEN / "singh-coal.yaml"), None)
    with pytest.raises(hk.NotModelledError, match="elements"):
        hk.fuel_of(load_design(OLSEN / "electric-car-45.yaml"), None)
    both = {"fuel": "natural_gas", "burners": {"rating": "36000 BTU/hr", "count": 2},
            "supply": {"type": "line", "pressure": "8 inch_H2O"}}  # fmt: skip
    with pytest.raises(hk.NotModelledError, match="one kind of heat"):
        hk.fuel_of(_design("fast-fire", {"heat.gas": both}), None)
    propane = _design("olsen-crossdraft-36", {"heat.gas.fuel": "propane"})
    assert hk.fuel_of(propane, None).name == "propane"
    outside = replace(hc.FAST_FIRE_LOAD, hi=(9 * IN, 12.5 * IN, 40 * IN))
    with pytest.raises(hk.NotModelledError, match="inside the chamber"):
        hk.heat_model(ff, outside, 1.0, hc.WOOD, n_rays=1_000)
    with pytest.raises(hk.NotModelledError, match="no hot-face emissivity"):
        hk._emissivity("kaowool-blanket-8pcf")  # pyright: ignore[reportPrivateUsage]
    cast = DesignLayer(material="kast-o-lite-26-li-plus", thickness=Q_(2, "in"))
    with pytest.raises(hk.NotModelledError, match="no specific heat"):
        hk._layer(cast)  # pyright: ignore[reportPrivateUsage]
    given = cast.model_copy(update={"specific_heat": Q_(1.0, "kJ/(kg*K)")})
    assert hk._layer(given).heat_capacity.cp(np.array([800.0]))[0] == pytest.approx(1000.0)  # pyright: ignore[reportPrivateUsage]
    no_rating = _design("olsen-crossdraft-36", {"heat.gas.burners.rating": None})
    assert hk.rated_fuel(no_rating, hk.fuel_of(no_rating, None)) is None


def test_a_model_names_every_surface() -> None:
    m = hc.fast_fire_model()
    with pytest.raises(ValueError, match="every surface"):
        ZoneModel(m.products, m.exchange, (*m.names, "ghost"), m.faces, m.setting, m.openings,
                  m.flow, m.t_room)  # fmt: skip
    assert Layout.ACC[0] == "fuel kg"
