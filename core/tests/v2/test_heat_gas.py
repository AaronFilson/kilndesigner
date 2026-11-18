"""v2's gas tables (`heat/gas.py`): each fuel's equilibrium products, the heat a zone keeps when
its gas leaves at T, transport and the radiating composition. Checked against v1's Cantera
available heat, NIST's methane, FAO's wood formula and the review's wood tables."""

from __future__ import annotations

import fuel as own
import pytest
import reference as ref

from kilndesigner.combustion import available_heat
from kilndesigner.v2.heat import gas, sources

ROOM = 298.15
WOOD = gas.wood(0.12, 19e6)
U = 0.12 / 0.88  # water per kg dry wood
NET_AS_FIRED = 19e6 - 2.44e6 * U  # J per kg dry wood (FAO UBET eq. 3)


@pytest.mark.parametrize("fuel", ["propane", "natural_gas"])
@pytest.mark.parametrize("lam", [0.9, 1.0, 1.15, 1.5])
@pytest.mark.parametrize("t", [400.0, 873.15, 1273.15, 1558.15, 1904.0])
def test_gas_fuels_keep_v1s_available_heat(fuel: str, lam: float, t: float) -> None:
    """The same Cantera thermodynamics as v1's `combustion.available_heat`: the table's linear
    interpolation agrees to 1e-4 of the heat."""
    f = gas.propane() if fuel == "propane" else gas.natural_gas()
    p = gas.products(f, lam, ROOM)
    v1 = available_heat(t, lam, ROOM, fuel)  # pyright: ignore[reportArgumentType]
    assert p.released(t) == pytest.approx(v1, rel=1e-4)


def test_methanes_net_heat_is_nists_less_the_water() -> None:
    """NIST's ΔcH° 890.7 kJ/mol less two moles of water's evaporation at FAO's 2.44 MJ/kg:
    (890.7 − 2 × 2.44 × 18.015)/16.0425 = 50.04 MJ/kg."""
    p = gas.products(gas.natural_gas(), 1.0, ROOM)
    assert p.net_heat == pytest.approx((890.7e3 - 2 * 2.44e3 * 18.015) / 16.0425 * 1e3, rel=2e-3)
    assert p.net_heat / gas.natural_gas().hhv == pytest.approx(0.901, abs=0.002)


@pytest.mark.parametrize("lam", [1.0, 1.2, 2.0])
def test_woods_net_heat_is_faos_formula(lam: float) -> None:
    """H(w) per kg dry wood = H_dry − 2.44·u (FAO UBET eq. 3), whatever the air."""
    p = gas.products(WOOD, lam, ROOM)
    assert p.net_heat == pytest.approx(NET_AS_FIRED, rel=1e-4)


def test_woods_stoichiometric_air() -> None:
    """5.89 kg air per kg dry wood for the 50/6/44 surrogate (cantera-tespy-review.md §2)."""
    p = gas.products(WOOD, 1.0, ROOM)
    assert p.air == pytest.approx(5.89, abs=0.01)
    assert p.mass == pytest.approx(1 + U + 5.89, abs=0.01)


# cantera-tespy-review.md §2, the equilibrium column, % of the net heat as fired at 12 % moisture
FLUE_LOSS = {
    1.0: (7.2, 25.1, 39.8, 50.0, 60.6),
    1.2: (8.3, 29.0, 45.8, 57.5, 69.6),
    1.5: (10.0, 34.7, 54.8, 68.9, 83.3),
    2.0: (12.8, 44.3, 69.9, 87.7, 106.1),
    0.95: (None, None, 44.4, 54.3, 64.4),
    0.9: (None, None, 49.0, 58.6, 68.4),
    0.8: (None, None, 58.3, 67.2, 76.3),
}
FLUE_AT = (200, 600, 900, 1100, 1300)


@pytest.mark.parametrize("lam", sorted(FLUE_LOSS))
def test_woods_flue_loss_is_the_reviews_table(lam: float) -> None:
    """Loss = 1 − q(T)/H(w): the review's table (frozen and equilibrium within 0.3 points),
    reduction included, to its rounding."""
    p = gas.products(WOOD, lam, ROOM)
    for t, want in zip(FLUE_AT, FLUE_LOSS[lam], strict=True):
        if want is None:
            continue
        loss = 100 * (1 - p.released(t + 273.15) / NET_AS_FIRED)
        assert loss == pytest.approx(want, abs=0.1), (lam, t)


def test_co_at_equilibrium_in_reduction() -> None:
    """x_CO at 1300 °C: 1.4 % at λ 0.95, 2.8 % at 0.9, 5.9 % at 0.8 (the review's table)."""
    for lam, x in ((0.95, 0.014), (0.9, 0.028), (0.8, 0.059)):
        p = gas.products(WOOD, lam, ROOM)
        co = float(p.x_co[abs(p.temps - 1573.15).argmin()])
        assert co == pytest.approx(x, abs=0.0006)


# cantera-tespy-review.md §7: propane products at λ 1.15, Cantera's mixture-averaged transport
TRANSPORT = {
    200: (0.731, 2.40e-5, 0.0377, 1119.0),
    600: (0.396, 3.75e-5, 0.0655, 1238.0),
    1000: (0.272, 4.87e-5, 0.0919, 1333.0),
    1300: (0.220, 5.62e-5, 0.1104, 1383.0),
}


@pytest.mark.parametrize("t", sorted(TRANSPORT))
def test_propane_flue_gas_transport(t: int) -> None:
    p = gas.products(gas.propane(), 1.15, ROOM)
    got = p.props(t + 273.15)
    for g, w in zip(got, TRANSPORT[t], strict=True):
        assert g == pytest.approx(w, rel=6e-3)


def test_methanes_radiating_composition() -> None:
    """CH4 + 2(O2 + 3.773 N2) → CO2 + 2 H2O + 7.55 N2: MR 2, p_w + p_c = 3/10.55 atm."""
    p = gas.products(gas.natural_gas(), 1.0, ROOM)
    pwc, mr = p.radiating(1000.0)
    assert mr == pytest.approx(2.0, rel=1e-3)
    assert pwc == pytest.approx(3 / (3 + 2 * sources.N2_PER_O2), rel=2e-3)


def test_refusals() -> None:
    with pytest.raises(gas.RangeError, match=r"below 0\.8"):
        gas.products(gas.propane(), 0.7, ROOM)
    p = gas.products(gas.propane(), 1.0, ROOM)
    p.check(1600.0)
    with pytest.raises(gas.RangeError, match="tables span"):
        p.check(3100.0)
    with pytest.raises(gas.RangeError, match="moisture"):
        gas.wood(0.6, 19e6)
    with pytest.raises(gas.RangeError, match="not wood"):
        gas.wood(0.12, 30e6)


# --- coal and oil, and each kiln's own fuel (ADR 0017 decision 12; kiln-fuels.md) ------------

DIESEL = gas.solid("#2 diesel", "oil", (0.8645, 0.1335, 0.0, 0.0, 0.002, 0.0), 0.0, 42.7e6, "test")
COAL = gas.solid("generic coal", "coal", (0.715, 0.045, 0.11, 0.013, 0.0047, 0.14), 0.10, 27.9e6,
                 "test")  # fmt: skip


def test_oils_stoichiometric_air() -> None:
    """C 86.45 %, H 13.35 %: (0.8645/12.011 + 0.1335/4.032) kmol O2 a kg, × 137.7 kg of air a
    kmol O2 = 14.47 kg; no water, so the net heat is the heating value (the S left out)."""
    p = gas.products(DIESEL, 1.0, ROOM)
    assert DIESEL.name == "#2 diesel"  # its analysis sums to 100 %: not scaled
    o2 = 0.8645 / 12.011 + 0.1335 / (4 * 1.008)
    assert p.air == pytest.approx(o2 * (31.998 + sources.N2_PER_O2 * 28.014), rel=2e-3)
    assert p.net_heat == pytest.approx(42.7e6, rel=1e-4)
    assert p.mass == pytest.approx(1 - 0.002 + p.air, rel=1e-9)


def test_coal_burns_to_its_heating_value_less_its_water() -> None:
    """Per kg dry coal: the net 27.9 MJ less the 0.111 kg of water's evaporation; the ash stays
    in the bed (its 14 % isn't in the gas); the analysis scaled to sum to 100 % is said."""
    p = gas.products(COAL, 1.2, ROOM)
    u = 0.10 / 0.90
    assert p.net_heat == pytest.approx(27.9e6 - 2.44e6 * u, rel=1e-4)
    assert p.mass == pytest.approx(COAL.gas_forming + u + p.air, rel=1e-9)
    assert sum(COAL.composition) == pytest.approx(1.0)
    assert "scaled" in COAL.name
    assert "ash stays in the bed" in (p.steps[0].note or "")
    assert gas.net_from_gross(20e6, 0.06, 0.40, 0.004) == pytest.approx(
        20e6 - (212.2 * 6 + 0.8 * 40.4) * 1e3
    )


def test_solid_fuels_outside_their_sources_are_refused() -> None:
    with pytest.raises(gas.RangeError, match="coal the sources give"):
        gas.solid("c", "coal", COAL.composition, 0.1, 35e6, "")
    with pytest.raises(gas.RangeError, match="moisture"):
        gas.solid("c", "coal", COAL.composition, 0.6, 27e6, "")
    with pytest.raises(gas.RangeError, match="needs carbon"):
        gas.solid("c", "coal", (0.0, 0.1, 0.1, 0.0, 0.0, 0.1), 0.1, 27e6, "")


FUEL_KILNS = sorted(
    kid
    for kid, k in ref.load()["kilns"].items()
    if any(f.get("what") == "fuel_species" for f in k.get("heat") or [])
)


def test_every_fuel_kiln_has_its_own_fuel() -> None:
    """The 37 kilns that burn wood, coal or oil (the dataset, research A1; 38 with Olsen's
    unbuilt two-chamber design, out of the set since 2026-11-17)."""
    assert len(FUEL_KILNS) == 37
    kinds = {f.kind for kid in FUEL_KILNS for f in own.own_fuels(kid)}
    assert kinds == {"wood", "coal", "oil"}
    assert [f.kind for f in own.own_fuels("blakebrough-sturt")] == ["wood", "oil"]


@pytest.mark.slow
@pytest.mark.parametrize("kid", FUEL_KILNS)
def test_each_kilns_own_fuel_burns_to_its_heating_value(kid: str) -> None:
    """Each fuel at its bands' least, middle and most: the products' net heat is its heating
    value less its water's evaporation (FAO UBET eq. 3)."""
    for end in ("least", "mid", "most"):
        for f in own.own_fuels(kid, end):  # pyright: ignore[reportArgumentType]
            p = gas.products(f, 1.2, ROOM)
            assert p.net_heat == pytest.approx(f.net_dry - 2.44e6 * f.water_per_kg, rel=2e-4)


def test_singh_s_grade_b_coal_is_netted_from_its_gross() -> None:
    """Grade B's 23.0–26.8 MJ/kg gross (equilibrated) with 2–6 % moisture (assumed) and the
    generic analysis's middles (H 4.55 %, O + N 12.15 %): 23.0/0.94 − 0.975 = 23.49 to
    26.8/0.98 − 0.975 = 26.37 MJ/kg net dry (EN ISO 18125)."""
    least, most = own.own_fuels("singh-coal", "least")[0], own.own_fuels("singh-coal", "most")[0]
    assert least.moisture == pytest.approx(0.06)
    assert most.moisture == pytest.approx(0.02)
    step = (212.2 * 4.55 + 0.8 * 12.15) * 1e3
    assert least.net_dry == pytest.approx(23.0e6 / 0.94 - step, rel=1e-6)
    assert most.net_dry == pytest.approx(26.8e6 / 0.98 - step, rel=1e-6)
    assert least.composition[5] == pytest.approx(0.2175 - 0.06, abs=1e-3)


def test_the_working_names_the_fuel_and_its_sources() -> None:
    steps = gas.products(WOOD, 1.0, ROOM).steps
    assert [s.name for s in steps] == [
        "The fuel",
        "Air and products per kg of fuel",
        "Heat kept per kg of fuel",
    ]
    assert "Pettersen" in (steps[0].reference or "")
    assert "read at the page" in (steps[0].note or "")
    gas_steps = gas.products(gas.natural_gas(), 1.0, ROOM).steps
    assert "CH4" in gas_steps[0].value
    assert gas_steps[0].note is None
