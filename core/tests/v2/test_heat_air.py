"""λ through a firing (`heat/air.py`): the stream after the fire at any λ, against Cantera's own
equilibrium, and the fuel bed's most."""

from __future__ import annotations

import math

import pytest

from kilndesigner.v2.heat import air, gas

ROOM = 294.26
WOOD = gas.wood(0.185, 18.46e6)
P1 = gas.products(WOOD, 1.0, ROOM)


@pytest.mark.parametrize(
    ("lam", "t", "within"),
    [(1.3, 1500.0, 0.0015), (2.0, 1500.0, 0.0015), (1.3, 1000.0, 1e-4), (3.0, 1900.0, 0.009)],
)
def test_excess_air_mixed_in_unreacted_is_cantera_s_equilibrium(
    lam: float, t: float, within: float
) -> None:
    """The heat a zone keeps per kg of fuel, the λ 1 products with the excess air mixed in,
    against Cantera's products at the leaner λ: within 0.15 % of the net heat at 1500 K to λ 2,
    0.9 % at 1900 K and λ 3 (the dissociation a leaner gas suppresses)."""
    leaner = gas.products(WOOD, lam, ROOM)
    a = lam * P1.air
    into = P1.fuel_enthalpy + a * P1.h_air(ROOM)
    kept = into - air.burnt(P1, 1.0, a, t).flow
    assert kept == pytest.approx(leaner.released(t), abs=within * P1.net_heat)
    assert air.burnt(P1, 1.0, a, t).lam == pytest.approx(lam)


def test_reduction_takes_the_streams_own_products() -> None:
    """At a table's λ, its products exactly; between two, linear; below 0.8, held there."""
    p9 = gas.products(WOOD, 0.9, ROOM)
    b = air.burnt(P1, 2.0, 2.0 * 0.9 * P1.air, 1500.0)
    assert b.flow == pytest.approx(2.0 * p9.mass * p9.h(1500.0), rel=1e-12)
    assert not b.held
    p85 = gas.products(WOOD, 0.85, ROOM)
    mid = air.burnt(P1, 1.0, 0.875 * P1.air, 1500.0).flow
    want = 0.5 * (p85.mass * p85.h(1500.0) + p9.mass * p9.h(1500.0))
    assert mid == pytest.approx(want, rel=1e-12)
    p8 = gas.products(WOOD, 0.8, ROOM)
    low = air.burnt(P1, 1.0, 0.5 * P1.air, 1500.0)
    assert low.held
    assert low.lam == pytest.approx(0.5)
    assert low.flow == pytest.approx(p8.mass * p8.h(1500.0), rel=1e-12)
    lean = gas.products(WOOD, 1.15, ROOM)  # a model at λ 1.15: down to 1.0 by the tables
    near = air.burnt(lean, 1.0, 1.0 * lean.air / 1.15, 1500.0)
    assert near.flow == pytest.approx(P1.mass * P1.h(1500.0), rel=1e-12)


def test_no_fuel_is_air_alone() -> None:
    """With no fuel the stream is its air; through no fuel it stays linear (a solver's iterate
    may pass below zero with the air at the products' λ)."""
    b = air.burnt(P1, 0.0, 0.05, 900.0)
    assert math.isinf(b.lam)
    assert b.flow == pytest.approx(0.05 * P1.h_air(900.0))
    neg = air.burnt(P1, -1e-4, -1e-4 * P1.air, 900.0)
    assert neg.flow == pytest.approx(-1e-4 * P1.mass * P1.h(900.0))


def test_the_coal_beds_most() -> None:
    """85–200 kg/(m²·h) as fired on Singh's four 4 ft² grates, 1.49 m², less the coal's water."""
    coal = gas.solid("c", "coal", (0.715, 0.045, 0.11, 0.013, 0.0047, 0.14), 0.10, 27.9e6, "")
    most = air.bed_most(coal, 1.486, air.COAL_BED[1])
    assert most == pytest.approx(200 / 3600 * 1.486 * 0.9)
    assert air.COAL_BED[0] * 3600 == pytest.approx(85.0)
