"""v2's gas radiation (`heat/gasrad.py`): the published WSGG sets and the zone method's exchange,
checked against Lienhard's Example 10.11, each other, `radiation.exchange` with a transparent gas,
and the zone method's own energy balance."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pytest
from numpy.typing import NDArray

from kilndesigner.thermal.radiation import box, exchange
from kilndesigner.thermal.surface import STEFAN_BOLTZMANN as SIGMA
from kilndesigner.v2.heat import gasrad as gr

type Vector = NDArray[np.float64]


def test_lienhards_example_10_11() -> None:
    """CO₂ at 0.2 atm in N₂, L₀ 40 cm, 1200 °C: ε_g = 0.085 read off Alberti's chart (Lienhard
    §10.5, radiation-exchange.md §6). Bordbar's set at its lowest MR, 0.01 (nearly pure CO₂), is
    within its stated accuracy against line by line."""
    w = gr.bordbar2014(0.01)
    eps = w.emissivity(1473.15, 0.2 * 1.01 * 0.40)
    assert eps == pytest.approx(0.085, rel=0.12)


@pytest.mark.parametrize("mr", [1.0, 2.0])
def test_the_two_sets_are_within_their_band(mr: float) -> None:
    """Bordbar 2014 reads 0 to +13 % over Dorigon 2013 at MR 1 and 2, L 0.1–3 m, 600–1600 K
    (thermal-software.md §6.2): the band v2 carries."""
    b, d = gr.bordbar2014(mr), gr.dorigon2013(mr)
    for t in (600.0, 1000.0, 1300.0, 1600.0):
        for length in (0.1, 0.5, 1.0, 3.0):
            pl = 0.28 * length
            ratio = b.emissivity(t, pl) / d.emissivity(t, pl)
            assert -0.01 < ratio - 1 < 0.15, (mr, t, length, ratio)


@pytest.mark.parametrize("make", [gr.bordbar2014, gr.dorigon2013])
@pytest.mark.parametrize("mr", [0.9, 1.0, 4 / 3, 2.0])
def test_weights_are_shares(make: object, mr: float) -> None:
    """Each grey gas's weight is positive and they sum below 1 over 400–2400 K (the clear gas
    keeps the rest)."""
    w = make(mr)  # pyright: ignore[reportCallIssue]
    a = w.weights(np.linspace(400, 2400, 41))
    assert a.min() > 0
    assert a.sum(axis=1).max() < 1


def test_weights_are_held_at_the_ranges_ends() -> None:
    w = gr.bordbar2014(1.0)
    assert np.allclose(w.weights(250.0), w.weights(300.0))
    assert np.allclose(w.weights(3000.0), w.weights(2400.0))


def test_refusals_and_the_nearest_dorigon_set() -> None:
    with pytest.raises(gr.RangeError, match=r"0\.01–4"):
        gr.bordbar2014(5.0)
    with pytest.raises(gr.RangeError, match="MR 1 and 2"):
        gr.dorigon2013(0.3)
    assert gr.dorigon2013(0.9).mr == 1.0
    assert "taken at the set's 1" in gr.dorigon2013(0.9).note
    assert gr.dorigon2013(1.6).mr == 2.0
    assert gr.dorigon2013(2.0).note == ""


@dataclass(frozen=True)
class Exact:
    """A transparent box's exact factors (Howell C-11, C-14) standing in for a trace."""

    areas: Vector
    f: NDArray[np.float64]

    def exchange(self, k: float) -> tuple[NDArray[np.float64], Vector]:
        assert k == 0.0
        return self.areas[:, None] * self.f, np.zeros(len(self.areas))


def test_a_transparent_gas_is_radiation_py() -> None:
    """With no gas radiation the zone method is Lienhard eq. 10.42: `radiation.exchange`."""
    enc = box(0.7, 0.9, 1.1)
    areas = np.asarray(enc.areas)
    gx = gr.exchange_for(Exact(areas, enc.view), None, 0.0)
    temps = np.array([900.0, 950.0, 1000.0, 1100.0, 800.0, 1200.0])
    eps = np.array([0.6, 0.6, 0.7, 0.5, 0.8, 0.6])
    q = gx.net(1500.0, temps, eps)
    want = exchange(enc, list(eps), list(temps)).power
    assert np.allclose(q, -want, rtol=1e-12, atol=1e-6)
    assert q.sum() == pytest.approx(0.0, abs=1e-6)


@dataclass(frozen=True)
class Grey:
    """A cube's exact transparent factors with a hand-made grey-gas split: a share of each pair
    and a gas column, closed (rows sum to the areas)."""

    areas: Vector
    f: NDArray[np.float64]

    def exchange(self, k: float) -> tuple[NDArray[np.float64], Vector]:
        tau = np.exp(-k * 0.6)  # one path length for every pair (a test construction)
        ss = self.areas[:, None] * self.f * tau
        return ss, self.areas - ss.sum(axis=1)


def test_black_isothermal_walls_exchange_only_with_the_gas() -> None:
    """Black walls at one temperature: q = Σ_j g s_j (a_j(T_g)σT_g⁴ − a_j(T_w)σT_w⁴)."""
    enc = box(1.0, 1.0, 1.0)
    w = gr.bordbar2014(2.0)
    gx = gr.exchange_for(Grey(np.asarray(enc.areas), enc.view), w, 0.28)
    tw, tg = 1100.0, 1500.0
    q = gx.net(tg, np.full(6, tw), np.ones(6))
    aw, ag = gx.surface_weights(np.array([tw]))[0], gx.gas_weights(tg)
    gs = np.array([g for _, g in gx.deas])  # (J + 1, n)
    want = (gs * (ag * SIGMA * tg**4 - aw * SIGMA * tw**4)[:, None]).sum(axis=0)
    assert np.allclose(q, want, rtol=1e-12)
    assert len(gx.deas) == 5


def test_the_gas_loses_what_the_surfaces_gain() -> None:
    """Grey walls at different temperatures: the gas's own balance, Σ_j Σ_i g s_ij (E_g,j −
    J_ij), equals the surfaces' net gain, so the closed enclosure conserves energy."""
    enc = box(0.8, 1.0, 1.2)
    w = gr.bordbar2014(1.0)
    gx = gr.exchange_for(Grey(np.asarray(enc.areas), enc.view), w, 0.3)
    temps = np.array([900.0, 950.0, 1000.0, 1100.0, 800.0, 1200.0])
    eps = np.array([0.6, 0.6, 0.7, 0.5, 0.8, 0.6])
    tg = 1400.0
    q = gx.net(tg, temps, eps)
    a = gx.areas
    ws, wg = gx.surface_weights(temps), gx.gas_weights(tg)
    loss = 0.0
    for m, (ss, gs) in enumerate(gx.deas):
        es, eg = ws[:, m] * SIGMA * temps**4, wg[m] * SIGMA * tg**4
        lhs = np.diag(a) - (1 - eps)[:, None] * ss
        j = np.linalg.solve(lhs, a * eps * es + (1 - eps) * gs * eg)
        loss += float((gs * (eg - j)).sum())
    assert q.sum() == pytest.approx(loss, rel=1e-10)
    assert q.sum() > 0
