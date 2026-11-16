"""Electric elements as face sources (ADR 0017 H11; part C2): their power on the walls they line,
falling as the wire's resistance rises (Kanthal's Ct), the supply's current and the wire's surface
load; Olsen's worked element design W25 (pp.258–260; Table 9-6, p.257) reproduced on a test
chamber built from its printed size, and the electric car kiln on its design's power."""

from __future__ import annotations

from functools import cache
from typing import Any

import gas_cases as gc
import loads
import numpy as np
import pytest

from kilndesigner.model import Kiln
from kilndesigner.v2.heat import chamber as ch
from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat.zone import Balance

IN = 0.0254
FT = 12 * IN
HOUR = 3600.0
CONE_10 = 1285 + 273.15  # K, at 60 °C/h (cones.yaml)
W_IN2 = 1 / IN**2  # W/m² per W/in²
pytestmark = pytest.mark.geometry

# W25 (pp.258–260): "10½CF", cone 10, 240 V, 108 A, 26 kW in six element groups of 4333 W, each
# 154.2 ft of B&S 10 wire (0.102 in). TEST CHAMBER (no design file; its size isn't printed beyond
# the volume): a cube of 10½ ft³ (Principle 1, p.74), 26.3 in a side; the electric car kiln's 7 in
# wall, 4½ in K-26 (the 2600 °F IFB cone 10 elements need, p.246) over 2½ in K-23 (p.39, p.248), as
# its floor and its flat roof (small electric kilns' roofs are flat, pp.248–249); a hinged front
# door, the elements in all four walls, the door's too (method 2 counts four walls, p.256); a 150 A
# breaker, the next standard size over 125 % of 108 A (NEC, the engine's rule)
W25_SIDE = 10.5 ** (1 / 3) * FT
W25_WIRE = (0.102 * IN, 154.2 * FT, 6)


def w25_kiln(power: str | None = "26 kW", firing: dict[str, str] | None = None) -> Kiln:
    side = f"{W25_SIDE / IN:.2f} in"
    wall = [{"material": "ifb-k26", "thickness": "4.5 in"},
            {"material": "ifb-k23", "thickness": "2.5 in"}]  # fmt: skip
    electric: dict[str, Any] = {
        "supply": {"voltage": "240 V", "phase": 1, "breaker": "150 A"},
        "walls": ["left", "right", "back", "front"],
    }
    if power is not None:
        electric["power"] = power
    return Kiln.model_validate({
        "schema": 1, "name": "Olsen's W25 element design, a test chamber", "units": "us",
        "firing": firing or {"cone": "10"},
        "chamber": {"width": side, "depth": side, "height": side},
        "roof": {"type": "flat"},
        "loading": {"type": "door", "face": "front", "door": "hinged"},
        "lining": {"walls": wall, "floor": wall, "roof": wall},
        "heat": {"electric": electric},
    })  # fmt: skip


@cache
def w25_setting() -> tuple[loads.Envelope, loads.Mass]:
    """W25's setting by the loads' method (no dataset entry: an extra), on its test chamber."""
    k = w25_kiln()
    c = ch.cavity(k)
    env = loads.envelopes("w25", k, c)[0]
    return env, loads.mass("w25", c.volume, env)


@cache
def w25_model(end: loads.End = "mid", n_rays: int = 20_000) -> Any:
    env, m = w25_setting()
    kg = {"least": m.low, "mid": m.mid, "most": m.high}[end]
    load = hk.Load(kg, env.lo, env.hi, loads.EMISSIVITY_NOMINAL,
                   f"W25's setting by kiln-settings.md's method at its band's {end}")  # fmt: skip
    return hk.heat_model(w25_kiln(), load, 1.0, n_rays=n_rays, wire=W25_WIRE)


def test_w25s_elements_as_printed() -> None:
    """The model's elements carry W25's printed design: 26 kW at 240 V draws 108 A; its wire,
    six groups of 154.2 ft of 0.102 in, runs at 7.3 W/in² (printed 7.4 with a slip in its
    denominator: 582 for about 593, kiln-reference.md); the four walls take a quarter each; cold
    the wire draws Ct's 1.04 more (Rh 13.3 Ω, Rc 12.8 Ω printed)."""
    m = w25_model(n_rays=2_000)
    el = m.elements
    assert el is not None
    assert el.power == pytest.approx(26_000)
    assert el.current == pytest.approx(108.3, abs=0.1)
    assert el.surface_load is not None
    assert el.surface_load / W_IN2 == pytest.approx(7.31, abs=0.01)
    assert sorted(m.faces[k].name for k, _ in el.faces) == ["back", "front", "left", "right"]
    assert [s for _, s in el.faces] == pytest.approx([0.25] * 4)
    assert el.most(293.15) == pytest.approx(26_000 * 1.04)
    step = next(s for s in m.steps if s.name == "The elements")
    assert "7.31 W/in²" in step.inputs["surface load"]
    radiation = next(s for s in m.steps if s.name == "Gas radiation")
    assert "a transparent gas" in radiation.value  # air: no CO₂ or H₂O


def test_the_elements_heat_the_walls_and_the_balance_closes() -> None:
    """At a fixed power the elements' heat enters their walls' hot faces: the energy balance closes
    (power in = walls + setting + openings; no flue, no stream), the lined walls hotter than the
    unlined floor."""
    m = w25_model(n_rays=2_000)
    f = fi.fire(m, fi.FixedInput(20_000.0), 2 * HOUR)
    e = f.energy
    assert e["fuel heat"] == pytest.approx(20_000.0 * 2 * HOUR, rel=1e-6)
    closure = e["fuel heat"] - e["flue"] - e["walls"] - e["setting"] - e["openings"]
    assert abs(closure) < 1e-6 * e["fuel heat"]
    assert e["flue"] == pytest.approx(0.0, abs=1e-6 * e["fuel heat"])
    lay = Balance(m).lay
    names = [x.name for x in m.faces]
    hot = {n: f.state[lay.walls[k][0]] for k, n in enumerate(names)}
    assert hot["left"] > hot["floor"]
    assert np.isnan(f.lam).all()
    assert f.steps[-1].name == "The elements"


def test_what_the_design_leaves_to_the_elements() -> None:
    """With no power given, the circuit's continuous limit, 80 % of its 150 A breaker at 240 V
    (NEC 210.20(A), v1's rule); a design's own top temperature is the wire's design point; a wall
    the traced faces don't hold is refused."""
    m = w25_model(n_rays=2_000)
    areas = dict(zip(m.names, m.exchange.areas, strict=True))
    el = hk.elements_of(w25_kiln(power=None), m.faces, areas, None)
    assert el.power == pytest.approx(0.8 * 150 * 240)
    assert el.surface_load is None
    hot = hk.elements_of(w25_kiln(firing={"top_temperature": "1200 degC"}), m.faces, areas, None)
    assert hot.design == pytest.approx(1473.15)
    with pytest.raises(hk.NotModelledError, match="aren't among the faces"):
        hk.elements_of(w25_kiln(), (), areas, None)


@pytest.mark.slow
def test_w25_reaches_cone_10_on_its_elements() -> None:
    """T1: W25 on its 26 kW, the elements full on, reaches cone 10 at both ends of its setting's
    band (the book prints no time: the time is v2's, beside its design's cone)."""
    times = []
    for end in ("least", "most"):
        m = w25_model(end)
        f = fi.fire(m, fi.MaxFire(), 24 * HOUR, (), CONE_10)
        t = f.reached(CONE_10)
        assert t is not None
        times.append(t / HOUR)
    assert times[0] < times[1]


@pytest.mark.slow
def test_the_electric_car_kiln_reaches_cone_10() -> None:
    """T1: the 45 in electric car kiln on its design's 51.9 kW (5 W/in² of its two sides, p.256:
    assumed), the elements full on, reaches cone 10 at every corner of its load's band; the book
    prints no time (problem set §2.6)."""
    b = gc.band("electric-car-45")
    assert np.isfinite(b.high)
    assert b.low < b.high
