"""The gas: each fuel's products at equilibrium at the air ratio λ, their enthalpy, transport and
radiating composition, tabulated against temperature (ADR 0017 H2–H4).

Cantera (GRI-Mech 3.0 thermodynamics and transport; ADR 0012) takes the chemistry. A gas fuel is
its Cantera species (natural gas as methane, as v1). Wood has no species: it is the 50/6/44 C/H/O
surrogate CH₁.₄₃O₀.₆₆ (Pettersen 1984, via firebox-efficiency.md §4), its enthalpy set by its
sourced net heating value, its water entering as liquid (FAO UBET eq. 3), so Cantera supplies only
the products (cantera-tespy-review.md §2). Below λ 1 the equilibrium products carry CO and H₂, and
the heat they hold is not released (H4); soot isn't counted.

**Per kg of fuel**: of gas, or of oven-dry wood (its water comes with it). The heat a zone keeps
when its gas leaves at T is

    q(T) = H_reactants − m_products · h_products(T)     (J per kg fuel)

with H_reactants the fuel and air as they enter (air at the room's temperature, wood at 25 °C) and
h_products the equilibrium mixture's enthalpy at T, 1 atm (both on GRI-Mech's formation basis).
With λ ≥ 1 and T at 25 °C it is the fuel's net heating value: for gas Cantera's, for wood the
source's less the water's evaporation (FAO eq. 3).

The tables span 250–3000 K, inside the NASA polynomials' 200–3500 K (Cantera's transport fits
start at 300 K, so the room's air below it is extrapolated); a temperature outside is refused
(ADR 0009), as is λ below 0.8 (the lowest checked: cantera-tespy-review.md §2; richer
flames make soot, which gas-phase equilibrium doesn't).
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from functools import cache
from typing import Any, Literal

import numpy as np
from numpy.typing import NDArray

from kilndesigner.v2.heat import sources as src
from kilndesigner.working import Step

type Vector = NDArray[np.float64]

# K: the tables. From 250 K so an unfired kiln's gas, the room's air, is in them: the NASA
# polynomials hold from 200 K; Cantera's transport fits start at 300 K and are extrapolated below
# (only the first minutes' convection uses them)
T_MIN, T_MAX = 250.0, 3000.0
T_STEP = 10.0
LAMBDA_MIN = 0.8
T_REF = 298.15
ATM = 101_325.0
M_H2O, M_O2, M_N2 = 18.015, 31.998, 28.014  # kg/kmol


class RangeError(ValueError):
    """Outside the range the gas tables were made and checked for (ADR 0009)."""


@dataclass(frozen=True)
class Fuel:
    """A fuel: a gas by its Cantera species and higher heating value, or wood as the surrogate
    with its moisture (wet basis) and net heating value (oven-dry)."""

    name: str
    kind: Literal["gas", "wood"]
    species: str = ""
    hhv: float = 0.0  # J/kg, gases: the basis of a burner's rating
    moisture: float = 0.0  # wood, wet basis
    net_dry: float = 0.0  # J per kg oven-dry wood, net
    reference: str = ""

    @property
    def water_per_kg(self) -> float:
        """kg of water per kg of fuel: wood's u = w/(1 − w), dry basis."""
        return self.moisture / (1 - self.moisture) if self.kind == "wood" else 0.0


def propane() -> Fuel:
    p = src.PROPANE_HHV
    return Fuel("propane", "gas", "C3H8", p.value, reference=p.reference)


def natural_gas() -> Fuel:
    m = src.METHANE_HHV
    why = f"{m.reference}; {m.note}"
    return Fuel("natural gas (methane)", "gas", "CH4", m.value, reference=why)


def wood(moisture: float, net_dry: float) -> Fuel:
    """Wood at a wet-basis ``moisture``, with its net heating value per oven-dry kg (J/kg)."""
    if not 0.0 <= moisture <= 0.5:
        raise RangeError(
            f"wood at {moisture:.0%} moisture: the formula is checked for 0–50 % wet basis; "
            "air-dried wood holds 12–20 % (FAO UBET §5.1.2)"
        )
    lo, hi = 15e6, 23e6
    if not lo <= net_dry <= hi:
        raise RangeError(
            f"a net heating value of {net_dry / 1e6:.1f} MJ/kg oven-dry is outside 15–23 MJ/kg: "
            "not wood as the sources give it (wood-fuel.md §1: 18.4–19.2 net, 20.0–21.1 "
            "'available')"
        )
    return Fuel(
        "wood",
        "wood",
        moisture=moisture,
        net_dry=net_dry,
        reference=f"{src.WOOD_CHO.reference}; {src.EVAPORATION.reference}",
    )


@cache
def _gas() -> Any:
    import cantera as ct  # pyright: ignore[reportMissingTypeStubs]

    g = ct.Solution("gri30.yaml")
    g.transport_model = "mixture-averaged"
    return g


def _species_h(name: str, t: float) -> float:
    """A species' molar enthalpy (J/kmol) on GRI-Mech's formation basis."""
    return float(_gas().species(name).thermo.h(t))


@dataclass(frozen=True)
class Products:
    """A fuel's products at λ, at equilibrium at each temperature of the table."""

    fuel: Fuel
    air_ratio: float
    t_air: float
    air: float  # kg air per kg fuel
    mass: float  # kg products per kg fuel
    reactants: float  # J per kg fuel, as they enter
    temps: Vector
    enthalpy: Vector  # J per kg products
    density: Vector
    viscosity: Vector
    conductivity: Vector
    cp: Vector
    x_h2o: Vector
    x_co2: Vector
    x_co: Vector
    steps: tuple[Step, ...] = field(default=())

    def check(self, t: float) -> None:
        if not T_MIN <= t <= T_MAX:
            raise RangeError(
                f"gas at {t - 273.15:.0f} °C: the tables span {T_MIN - 273.15:.0f}–"
                f"{T_MAX - 273.15:.0f} °C (GRI-Mech's NASA polynomials 200–3500 K; transport "
                "fitted from 300 K)"
            )

    def h(self, t: float) -> float:
        """The products' enthalpy (J/kg) at t, the table's linear interpolation."""
        return float(np.interp(t, self.temps, self.enthalpy))

    def released(self, t: float) -> float:
        """Heat kept per kg fuel when the products leave at t (J/kg)."""
        return self.reactants - self.mass * self.h(t)

    @property
    def net_heat(self) -> float:
        """The fuel's net heat per kg with the products at 25 °C and complete combustion
        (λ ≥ 1): its net heating value as fired, the air entering at t_air."""
        return self.reactants - self.mass * float(np.interp(T_REF, self.temps, self.enthalpy))

    def props(self, t: float) -> tuple[float, float, float, float]:
        """ρ (kg/m³), μ (Pa·s), k (W/(m·K)), c_p (J/(kg·K)) of the products at t, 1 atm."""
        return (
            float(np.interp(t, self.temps, self.density)),
            float(np.interp(t, self.temps, self.viscosity)),
            float(np.interp(t, self.temps, self.conductivity)),
            float(np.interp(t, self.temps, self.cp)),
        )

    def radiating(self, t: float) -> tuple[float, float]:
        """p_H2O + p_CO2 (atm, at 1 atm total) and the molar ratio MR = x_H2O / x_CO2 at t."""
        xw = float(np.interp(t, self.temps, self.x_h2o))
        xc = float(np.interp(t, self.temps, self.x_co2))
        return xw + xc, xw / xc


def _wood_moles(fuel: Fuel, lam: float) -> tuple[dict[str, float], float, float, float]:
    """The mixture per kmol of carbon (Cantera species), its mass, the stoichiometric O2 and the
    water, all per kmol C."""
    a, b = src.WOOD_H_PER_C, src.WOOD_O_PER_C
    m_wood = src.M_C + a * src.M_H + b * src.M_O  # kg per kmol C
    water = fuel.water_per_kg * m_wood / M_H2O
    s = 1 + a / 4 - b / 2
    x = {"C": 1.0, "H": a, "O": b, "H2O": water, "O2": lam * s, "N2": lam * s * src.N2_PER_O2}
    return x, m_wood, s, water


def _reactants_wood(fuel: Fuel, lam: float, t_air: float) -> tuple[dict[str, float], float, float]:
    """Wood's mixture, its reactants' enthalpy (J per kg dry wood) and air (kg/kg dry wood).

    The wood's enthalpy from its net heating value: CH_aO_b + s O2 → CO2 + a/2 H2O(g) releases
    H_net·M per kmol C at 25 °C; its water enters as liquid, 2.44 MJ/kg below the vapour (FAO)."""
    x, m_wood, s, water = _wood_moles(fuel, lam)
    a = src.WOOD_H_PER_C
    h_co2, h_h2o, h_o2 = (_species_h(n, T_REF) for n in ("CO2", "H2O", "O2"))
    h_wood = fuel.net_dry * m_wood + h_co2 + a / 2 * h_h2o - s * h_o2  # J per kmol C
    h_liquid = h_h2o - src.EVAPORATION.value * M_H2O
    o2 = lam * s
    h_air = o2 * (_species_h("O2", t_air) + src.N2_PER_O2 * _species_h("N2", t_air))
    air = o2 * (M_O2 + src.N2_PER_O2 * M_N2) / m_wood
    return x, (h_wood + water * h_liquid + h_air) / m_wood, air


@cache
def products(fuel: Fuel, air_ratio: float, t_air: float) -> Products:
    """The fuel's products at λ = ``air_ratio`` with air at ``t_air`` (K), tabulated 300–3000 K."""
    if air_ratio < LAMBDA_MIN:
        raise RangeError(
            f"λ {air_ratio:.2f}: below {LAMBDA_MIN}, the lowest checked; a richer flame makes "
            "soot, which gas-phase equilibrium doesn't count (cantera-tespy-review.md §2)"
        )
    g = _gas()
    if fuel.kind == "gas":
        g.TP = t_air, ATM
        g.set_equivalence_ratio(1.0 / air_ratio, fuel.species, f"O2:1.0, N2:{src.N2_PER_O2}")
        y_fuel = float(g.Y[g.species_index(fuel.species)])
        x0: Any = g.X.copy()
        reactants = float(g.enthalpy_mass) / y_fuel
        mass = 1.0 / y_fuel
        air = mass - 1.0
    else:
        xw, reactants, air = _reactants_wood(fuel, air_ratio, t_air)
        g.TPX = T_REF, ATM, xw
        x0 = g.X.copy()
        mass = 1.0 + fuel.water_per_kg + air
    # From 290 K so 25 °C interpolates (the polynomials hold from 200 K); refused below T_MIN
    temps = np.arange(T_MIN - T_STEP, T_MAX + T_STEP / 2, T_STEP)
    cols: dict[str, list[float]] = {k: [] for k in ("h", "rho", "mu", "k", "cp", "w", "c", "co")}
    iw, ic, ico = (g.species_index(n) for n in ("H2O", "CO2", "CO"))
    for t in temps:
        g.TPX = float(t), ATM, x0
        g.equilibrate("TP")
        cols["h"].append(float(g.enthalpy_mass))
        cols["rho"].append(float(g.density))
        cols["mu"].append(float(g.viscosity))
        cols["k"].append(float(g.thermal_conductivity))
        cols["cp"].append(float(g.cp_mass))
        cols["w"].append(float(g.X[iw]))
        cols["c"].append(float(g.X[ic]))
        cols["co"].append(float(g.X[ico]))
    arr = {k: np.array(v) for k, v in cols.items()}
    p = Products(
        fuel, air_ratio, t_air, air, mass, reactants, temps, arr["h"], arr["rho"], arr["mu"],
        arr["k"], arr["cp"], arr["w"], arr["c"], arr["co"],
    )  # fmt: skip
    return replace(p, steps=_working(p))


def _working(p: Products) -> tuple[Step, ...]:
    f = p.fuel
    what = (
        f"{f.name}: Cantera species {f.species}, HHV {f.hhv / 1e6:.2f} MJ/kg"
        if f.kind == "gas"
        else f"wood CH{src.WOOD_H_PER_C:.3f}O{src.WOOD_O_PER_C:.3f}, {f.moisture:.0%} moisture "
        f"(wet basis), {f.net_dry / 1e6:.2f} MJ/kg net oven-dry"
    )
    hot = p.released(1558.15)
    return (
        Step(
            name="The fuel",
            value=what,
            reference=f.reference,
            note=None if f.kind == "gas" else src.WOOD_CHO.note,
        ),
        Step(
            name="Air and products per kg of fuel",
            value=f"{p.air:.3f} kg air, {p.mass:.3f} kg products",
            formula="λ × stoichiometric air; products = fuel (and its water) + air",
            inputs={"λ": f"{p.air_ratio:.3f}", "air at": f"{p.t_air - 273.15:.1f} °C"},
            reference=src.O2_IN_AIR.reference,
        ),
        Step(
            name="Heat kept per kg of fuel",
            value=f"{p.net_heat / 1e6:.3f} MJ/kg with the gas leaving at 25 °C; "
            f"{hot / 1e6:.3f} MJ/kg at 1285 °C",
            formula="q(T) = H_reactants − m_products·h_products,eq(T)",
            reference=src.GRI30,
            note="equilibrium products; below λ 1 the CO and H2 at equilibrium hold heat that "
            "isn't released (ADR 0017 H4); soot not counted",
        ),
    )
