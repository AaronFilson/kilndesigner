"""v2's convection inside a kiln (`heat/zone.py`, `fittings-and-kiln-convection.md` §2): flow in a
duct on each zone's hydraulic diameter, Churchill–Chu's natural convection as each surface's floor,
the setting's passages' laminar value between plates."""

from __future__ import annotations

import numpy as np
import pytest
from ht.conv_free_immersed import (  # pyright: ignore[reportMissingTypeStubs]
    Nu_vertical_plate_Churchill,
)
from ht.conv_internal import turbulent_Gnielinski  # pyright: ignore[reportMissingTypeStubs]

from kilndesigner.v2.heat import gas
from kilndesigner.v2.heat import sources as src
from kilndesigner.v2.heat.zone import PLATES_NU, duct_h, natural_h, passage_h

ROOM = 294.26
WOOD = gas.products(gas.wood(0.12, 19e6), 1.0, ROOM)


def test_natural_convection_is_churchill_and_chus() -> None:
    """Lienhard eq. 8.13b at the film temperature, as ht's own function gives it."""
    tg, tw, tall = np.array([1500.0, 600.0]), np.array([1400.0, 400.0]), np.array([0.9, 4.0])
    h = natural_h(WOOD, tg, tw, tall)
    for i in range(2):
        film = (tg[i] + tw[i]) / 2
        rho, mu, k, cp = WOOD.props(film)
        gr = 9.80665 * abs(tg[i] - tw[i]) / film * tall[i] ** 3 * (rho / mu) ** 2
        want = float(Nu_vertical_plate_Churchill(cp * mu / k, gr)) * k / tall[i]
        assert h[i] == pytest.approx(want, rel=1e-9)
    assert natural_h(WOOD, tg, tg, tall) == pytest.approx(0.825**2 * np.array(
        [WOOD.props(1500.0)[2] / 0.9, WOOD.props(600.0)[2] / 4.0]), rel=1e-9)  # fmt: skip


def test_a_settings_passages_laminar_and_turbulent() -> None:
    """Nu 7.541 between plates when laminar (Table 7.4), Gnielinski's when turbulent."""
    rho, mu, k, cp = WOOD.props(1500.0)
    assert passage_h(rho, mu, k, cp, 0.5, 0.1) == pytest.approx(PLATES_NU * k / 0.1)
    rho, mu, k, cp = WOOD.props(300.0)
    fast = passage_h(rho, mu, k, cp, 5.0, 0.1)
    re = rho * 5.0 * 0.1 / mu
    assert re > 2300
    assert fast > PLATES_NU * k / 0.1
    assert fast == pytest.approx(
        float(turbulent_Gnielinski(re, cp * mu / k, 0.3164 * re**-0.25)) * k / 0.1, rel=0.05
    )
    assert src.SETTING_GAP == (0.025, 0.100)


def test_flow_in_a_duct_takes_the_larger_form() -> None:
    """Laminar entry at low Re, Gnielinski's turbulent value well past transition."""
    rho, mu, k, cp = WOOD.props(1200.0)
    slow = duct_h(rho, mu, k, cp, 0.05, 0.2, 4.0)
    assert slow > 3.657 * k / 0.2  # the developing laminar value is above the developed one
    fast = duct_h(rho, mu, k, cp, 30.0, 0.2, 4.0)
    re = rho * 30.0 * 0.2 / mu
    assert re > 1e4
    assert fast == pytest.approx(
        float(turbulent_Gnielinski(re, cp * mu / k, (1.82 * np.log10(re) - 1.64) ** -2)) * k / 0.2,
        rel=0.03,
    )
