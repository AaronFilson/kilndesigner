"""Part C's tests for the gas and electric kilns (problem set §6; `11-10-26.md` §C, "C2 as built"),
each with v2's band (`bands.py`'s corner runs over the setting's band and λ) beside the book's
figure:

- **T1**, reaches its cone at the printed (or the design's) input: every corner of the band;
- **T2**, the time at a printed input: the kit 24's eight hours (p.139), W15's "about 8 h"
  (p.226); the 36 ft³ cross-draft's 12–15 h stays the open item (`test_heat_reference_firings`);
- **T5**, the evenness's ordering where the zone model can see it: Bowen Mountain's back fires cold
  (p.128), its chamber cut into two segments front to back.

λ is the operator's setting, 1.0–1.15: no gas kiln here has a draft path yet (part C1). The
electric kilns are in `test_heat_elements.py`. Kähler's salt kiln and Blakebrough's fibre kiln
print no burner input (their burners refused, `test_heat_burner_inputs.py`): their models build
(`test_heat_shapes.py`), their firings wait on an input. Nothing is fitted.
"""

from __future__ import annotations

import math
from dataclasses import replace
from functools import cache
from typing import Any

import gas_cases as gc
import heat_cases as hc
import loads
import pytest

from kilndesigner.v2.heat import chamber as ch
from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat import series, target

HOUR = 3600.0
pytestmark = [pytest.mark.slow, pytest.mark.geometry]

# The gas kilns whose burners the design names (count and model or rating) and that print or
# assume no draft: each must reach its cone at every corner of its band (T1)
T1 = (
    "olsen-kit-16", "olsen-kit-24", "kaneko-car", "updraft-test-1", "updraft-test-2",
    "updraft-test-3", "updraft-test-4", "bowen-mountain",
)  # fmt: skip


@pytest.mark.parametrize("kid", T1)
def test_t1_reaches_its_cone_on_its_burners(kid: str) -> None:
    """T1: on its burners at their supply's pressure (fixed input), the kiln reaches its cone at
    every corner of v2's band (the setting's least to most, λ 1.0–1.15); the band's working lists
    the inputs by their swing."""
    b = gc.band(kid)
    assert math.isfinite(b.high), f"{kid}: not reached at a corner, {b}"
    assert 0 < b.low <= b.nominal <= b.high
    assert b.steps[0].name.startswith("The band")
    swing = {name: hi - lo for name, lo, hi in b.swings}
    assert swing["the load"] > 0  # a heavier setting is slower
    assert swing["λ"] > 0  # more air carries more heat away


def test_t2_the_kit_24_fires_in_eight_hours() -> None:
    """T2: "Olsen 24 updraft gas kiln ... eight hours" (p.139; the cone isn't printed, cone 10 the
    design's). On its ten MR-750s at 8 in. w.c. (750,000 BTU/hr, p.222) cone 10 comes in 0.97–3.5 h
    across the band: inside eight hours at every corner, the time an operator's choice below the
    burners' full input. The input that takes eight hours, at the band's slowest corner (the
    heaviest setting, λ 1.15), is about half the burners' (Olsen calls most gas kilns overpowered,
    p.226)."""
    b = gc.band("olsen-kit-24")
    assert b.high < 8.0
    m = gc.at_end("olsen-kit-24", gc.model("olsen-kit-24", 1.15), "most")
    rate = gc.fuel_rate("olsen-kit-24", m)
    need = target.input_for(m, gc.cone("olsen-kit-24"), 8 * HOUR, rate / 2, most=16.0)
    assert need.fuel < 0.6 * rate


# W15 (p.226): "an updraught kiln of 36cu. ft using insulation bricks will have a minimum of 10
# such burners and will probably fire easily in eight hours": the cross-draft's cube with IFB and
# ten 36,000 BTU/hr burners (heat_cases.w15_ifb's chamber, a stand-in: no design file), its setting
# by kiln-settings.md's method on that chamber (an extra: no dataset entry)
@cache
def _w15_setting() -> tuple[Any, loads.Envelope, loads.Mass]:
    k = hc._crossdraft(hc.FLUE | hc.IFB)  # pyright: ignore[reportPrivateUsage]
    c = ch.cavity(k)
    env = loads.envelopes("w15", k, c)[0]
    return k, env, loads.mass("w15", c.volume, env)


@cache
def _w15_model(lam: float) -> Any:
    k, env, mass = _w15_setting()
    load = hk.Load(mass.mid, env.lo, env.hi, loads.EMISSIVITY_NOMINAL,
                   "W15's setting by kiln-settings.md's method, its stand-in chamber")  # fmt: skip
    return hk.heat_model(k, load, lam, n_rays=gc.BAND_RAYS)


@cache
def _w15(end: loads.End, lam: float) -> float | None:
    """Hours to cone 10 on W15's ten burners at its setting band's end and λ."""
    k, _, mass = _w15_setting()
    kg = {"least": mass.low, "mid": mass.mid, "most": mass.high}[end]
    m = _w15_model(lam)
    m = replace(m, settings=(replace(m.settings[0], mass=kg),))
    f = fi.fire(m, fi.FixedInput(hk.rated_fuel(k, m.products.fuel) or 0.0), 24 * HOUR, (),
                hc.CONE_10)  # fmt: skip
    t = f.reached(hc.CONE_10)
    return None if t is None else t / HOUR


def test_t2_w15_fires_easily_in_about_eight_hours() -> None:
    """T2: W15 on its ten burners (360,000 BTU/hr, p.226) reaches cone 10 inside about eight hours
    at every corner of its band (the setting's least to most by the method, λ 1.0–1.15)."""
    times = [_w15(end, lam) for end in ("least", "most") for lam in gc.LAMBDA]
    assert all(t is not None for t in times)
    assert max(t for t in times if t is not None) < 8.0


def test_t1_the_three_chamber_kiln_reaches_cone_10_in_every_chamber() -> None:
    """T1: Olsen's three-chamber climbing kiln on its six Eclipse TR-80s at 10 in. w.c.
    (1,285,200 BTU/hr at peak, p.224), fired in stages, each chamber in turn on all six as a
    climbing kiln is (the book doesn't say where the six fire; the design lays them in the front
    wall): every chamber reaches cone 10 at both ends of its band, each later chamber faster for
    the heat the earlier ones' gas left in it."""
    for end in ("least", "most"):
        m = gc.at_end("olsen-three-chamber", gc.model("olsen-three-chamber"), end)
        rate = gc.fuel_rate("olsen-three-chamber", m)
        cone = gc.cone("olsen-three-chamber")
        stages = [series.Stage(k, fi.FixedInput(rate), cone, 24 * HOUR) for k in range(3)]
        times = series.fire_stages(m, stages).times
        assert all(t is not None for t in times)
        first, *later = (t for t in times if t is not None)
        assert all(t < first for t in later)


def test_t5_bowen_mountains_back_fires_cold() -> None:
    """T5: "the back usually fires cold" (p.128). Bowen Mountain's chamber cut into two segments
    front to back, its eight MR-750s firing in at the front: when the front's setting reaches
    cone 10 the back's is colder, its gas too (the ordering, not the size: the book prints none)."""
    m = gc.at_end("bowen-mountain", gc.model("bowen-mountain", 1.0, 2), "mid", 2)
    cone = gc.cone("bowen-mountain")
    f = fi.fire(m, fi.FixedInput(gc.fuel_rate("bowen-mountain", m)), 24 * HOUR, (),
                (0, cone))  # fmt: skip
    assert f.reached(cone, 0) is not None
    assert f.t_settings[-1, 1] < f.t_settings[-1, 0] - 10.0
    assert f.t_gases[-1, 1] < f.t_gases[-1, 0]
