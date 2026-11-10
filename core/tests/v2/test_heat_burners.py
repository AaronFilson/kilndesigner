"""v2's burners (`heat/burners.py`): a venturi burner's output at its supply pressure, √pressure
through one orifice (Olsen p.216), against the library's published ratings."""

from __future__ import annotations

import math

import pytest

from kilndesigner.v2.heat import burners as bu


@pytest.mark.parametrize("model", ["Ransome B1", "Ransome B3", "Ransome B5", "GACO MR750"])
def test_published_ratings_rise_with_root_pressure(model: str) -> None:
    """Each published rating on the curve is its lowest one carried by √(p/p₀), within 5 % (the
    carry reads low by up to 4.7 % on Ransome's B1): the √pressure rule holds on the makers' own
    figures to that."""
    c = bu.curve(model)
    for p, r in zip(c.psi, c.btu_hr, strict=True):
        assert bu.carried(c.btu_hr[0], c.psi[0], p, "propane") == pytest.approx(r, rel=0.05)


def test_a_curve_both_ways() -> None:
    c = bu.curve("GACO MR100")
    assert c.psi[0] == 2.0  # its 11 in. w.c. rating is another orifice (curve_from_psi)
    assert c.at(5.0) == pytest.approx(152_830)
    q = c.at(7.0)
    assert c.pressure_for(q) == pytest.approx(7.0, rel=1e-9)
    assert c.natural_gas == (8.0, 100_000.0)
    with pytest.raises(bu.BurnerError, match="outside its published"):
        c.at(30.0)
    with pytest.raises(bu.BurnerError, match="outside its published"):
        c.pressure_for(10_000.0)
    with pytest.raises(bu.BurnerError, match="no published ratings"):
        bu.curve("Acme X")


def test_the_crossdraft_question() -> None:
    """A burner rated near 36,000 BTU/hr at 11 in. w.c. on propane (Ransome B3's 34,200) gives
    77,500 at 2 psi on its published curve: 2.2 × its low-pressure rating, about what the model
    needs from the 36 ft³ cross-draft's six for cone 10 in 15 h (§I); on natural gas the carry
    stops at 11 in. w.c., 1.17 × an 8 in. w.c. rating."""
    b3 = bu.curve("Ransome B3")
    assert b3.at(2.0) / b3.at(0.397) == pytest.approx(2.27, abs=0.01)
    low = bu.carried(36_000, 8 / bu.IN_WC_PER_PSI, bu.LOW_PRESSURE_PSI, "natural_gas")
    assert low / 36_000 == pytest.approx(math.sqrt(11 / 8))
    with pytest.raises(bu.BurnerError, match="low pressure only"):
        bu.carried(36_000, 8 / bu.IN_WC_PER_PSI, 1.0, "natural_gas")
    step = bu.working(6, 36_000, 8 / bu.IN_WC_PER_PSI, bu.LOW_PRESSURE_PSI, "natural_gas")
    assert step.value.startswith("6 × 42,214 BTU/hr")
