"""The gas: each fuel's products at equilibrium at the air ratio λ, their enthalpy, transport and
radiating composition, tabulated against temperature (ADR 0017 H2–H4).

Cantera (GRI-Mech 3.0 thermodynamics and transport; ADR 0012) takes the chemistry. A gas fuel is
its Cantera species (natural gas as methane, as v1). **A solid or liquid fuel** (wood, coal, oil;
ADR 0017 decision 12, `kiln-fuels.md`) has no species: it is its ultimate analysis, C, H, O and N
per kg of dry fuel as atoms (CH_aO_bN_n per kmol of carbon), its ash and sulphur left out of the
gas (GRI-Mech holds no sulphur; S is at most 0.94 % of the coals, 0.3 % of the oil: its share of
the air, under 1 %, is left out and said), its enthalpy set by its sourced net heating value, its
water entering as liquid (FAO UBET eq. 3; EN ISO 18125's as-received form), so Cantera supplies
only the products (cantera-tespy-review.md §2). Wood without its own analysis is the 50/6/44 C/H/O
surrogate CH₁.₄₃O₀.₆₆, inside Stolarski 2022's quartiles (kiln-fuels.md §2.3). Below λ 1 the
equilibrium products carry CO and H₂, and the heat they hold is not released (H4); soot isn't
counted.

**Per kg of fuel**: of gas, or of dry fuel (its water comes with it). The heat a zone keeps
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
M_N = 14.007  # g/mol (IUPAC)
# The wood surrogate: C, H, O, N, S, ash as mass fractions of the dry fuel (Pettersen's 50/6/44)
SURROGATE = (0.50, 0.06, 0.44, 0.0, 0.0, 0.0)
# Net heating values (J per kg dry) the sources give for each kind, the range a fuel is checked in
NET_RANGE = {
    "wood": ((15e6, 23e6), "wood-fuel.md §1: 18.4–19.2 net; kiln-fuels.md: 17.0–19.9 by genus"),
    "coal": ((20e6, 30e6), "kiln-fuels.md §4: generic coal 27.9, Grade B 22–28 MJ/kg dry net"),
    "oil": ((40e6, 46e6), "kiln-fuels.md §3: #2 diesel 42.1–43.3 net, 45.4 gross"),
}
type Solid = Literal["wood", "coal", "oil"]


class RangeError(ValueError):
    """Outside the range the gas tables were made and checked for (ADR 0009)."""


@dataclass(frozen=True)
class Fuel:
    """A fuel: a gas by its Cantera species and higher heating value; or wood, coal or oil by its
    dry analysis (``composition``: C, H, O, N, S, ash as mass fractions of the dry fuel), its
    moisture (wet basis) and its net heating value per kg dry."""

    name: str
    kind: Literal["gas", "wood", "coal", "oil"]
    species: str = ""
    hhv: float = 0.0  # J/kg, gases: the basis of a burner's rating
    moisture: float = 0.0  # wet basis
    net_dry: float = 0.0  # J per kg dry fuel, net
    reference: str = ""
    composition: tuple[float, float, float, float, float, float] = SURROGATE

    @property
    def water_per_kg(self) -> float:
        """kg of water per kg of dry fuel: u = w/(1 − w)."""
        return self.moisture / (1 - self.moisture) if self.kind != "gas" else 0.0

    @property
    def gas_forming(self) -> float:
        """The share of the dry fuel that goes into the gas: all but its sulphur and ash."""
        return 1.0 - self.composition[4] - self.composition[5]


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


def solid(
    name: str,
    kind: Solid,
    composition: tuple[float, float, float, float, float, float],
    moisture: float,
    net_dry: float,
    reference: str,
) -> Fuel:
    """Wood, coal or oil by its dry analysis (C, H, O, N, S, ash as fractions of the dry fuel),
    its moisture (wet basis) and its net heating value (J per kg dry). The analysis's C, H, O, N
    and S are scaled to sum to 1 − ash, so bands' middles that don't (kiln-fuels.md §5) make a
    whole fuel; the scale is said in the name."""
    c, h, o, n, s, ash = composition
    if min(composition) < 0 or ash >= 1 or c <= 0:
        raise RangeError(f"{name}: an analysis needs carbon, no negative parts, ash under 100 %")
    if not 0.0 <= moisture <= 0.5:
        raise RangeError(
            f"{name} at {moisture:.0%} moisture: the formula is checked for 0–50 % wet basis "
            "(FAO UBET eq. 3)"
        )
    (lo, hi), why = NET_RANGE[kind]
    if not lo <= net_dry <= hi:
        raise RangeError(
            f"{name}: a net heating value of {net_dry / 1e6:.1f} MJ/kg dry is outside "
            f"{lo / 1e6:.0f}–{hi / 1e6:.0f} MJ/kg, the {kind} the sources give ({why})"
        )
    total = c + h + o + n + s
    k = (1 - ash) / total
    scaled = (c * k, h * k, o * k, n * k, s * k, ash)
    if abs(k - 1) > 1e-6:
        name = f"{name} (its analysis scaled ×{k:.3f} to sum to 100 %)"
    return Fuel(name, kind, moisture=moisture, net_dry=net_dry, reference=reference,
                composition=scaled)  # fmt: skip


def net_from_gross(gross_dry: float, hydrogen: float, oxygen: float, nitrogen: float) -> float:
    """The net heating value (J per kg dry) from the gross, EN ISO 18125's eq. as Alakangas 2016
    gives it ([F4] eq. 2.4, kiln-fuels.md): q_net,d = q_gr,d − 212.2·H − 0.8·(O + N) J/g, with H,
    O and N in % of the dry fuel (fractions here)."""
    return gross_dry - (212.2 * hydrogen * 100 + 0.8 * (oxygen + nitrogen) * 100) * 1e3


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
    air_enthalpy: Vector = field(default_factory=lambda: np.zeros(0))  # J per kg air

    def h_air(self, t: float) -> float:
        """The air's enthalpy (J/kg) at t, on GRI-Mech's formation basis: the stream through
        zones before the fire (staged firing)."""
        return float(np.interp(t, self.temps, self.air_enthalpy))

    @property
    def fuel_enthalpy(self) -> float:
        """The fuel's own enthalpy as it enters (J per kg fuel): the reactants less their air."""
        return self.reactants - self.air * self.h_air(self.t_air)

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


def _solid_moles(fuel: Fuel, lam: float) -> tuple[dict[str, float], float, float, float, float]:
    """The mixture per kmol of carbon (Cantera species: the fuel as C, H, O and N atoms, its
    water, the air), the kg of dry fuel per kmol C, the stoichiometric O2, the water and the
    fuel's N atoms, all per kmol C."""
    c, h, o, n, _, _ = fuel.composition
    kmol_c = c / src.M_C  # kmol C per kg dry fuel
    a, b, nn = h / src.M_H / kmol_c, o / src.M_O / kmol_c, n / M_N / kmol_c
    m_dry = 1.0 / kmol_c  # kg dry fuel per kmol C
    water = fuel.water_per_kg * m_dry / M_H2O
    s = 1 + a / 4 - b / 2
    x = {"C": 1.0, "H": a, "O": b, "N": nn, "H2O": water, "O2": lam * s,
         "N2": lam * s * src.N2_PER_O2}  # fmt: skip
    return x, m_dry, s, water, nn


def _reactants_solid(fuel: Fuel, lam: float, t_air: float) -> tuple[dict[str, float], float, float]:
    """A solid or liquid fuel's mixture, its reactants' enthalpy (J per kg dry fuel) and air
    (kg/kg dry fuel).

    The fuel's enthalpy from its net heating value: CH_aO_bN_n + s O2 → CO2 + a/2 H2O(g) + n/2 N2
    releases H_net per kg dry at 25 °C; its water enters as liquid, 2.44 MJ/kg below the vapour
    (FAO)."""
    x, m_dry, s, water, nn = _solid_moles(fuel, lam)
    a = x["H"]
    h_co2, h_h2o, h_o2, h_n2 = (_species_h(n, T_REF) for n in ("CO2", "H2O", "O2", "N2"))
    h_fuel = fuel.net_dry * m_dry + h_co2 + a / 2 * h_h2o + nn / 2 * h_n2 - s * h_o2  # per kmol C
    h_liquid = h_h2o - src.EVAPORATION.value * M_H2O
    o2 = lam * s
    h_air = o2 * (_species_h("O2", t_air) + src.N2_PER_O2 * _species_h("N2", t_air))
    air = o2 * (M_O2 + src.N2_PER_O2 * M_N2) / m_dry
    return x, (h_fuel + water * h_liquid + h_air) / m_dry, air


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
        xw, reactants, air = _reactants_solid(fuel, air_ratio, t_air)
        g.TPX = T_REF, ATM, xw
        x0 = g.X.copy()
        mass = fuel.gas_forming + fuel.water_per_kg + air
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
    air_h = []
    for t in temps:  # the air as it is, unreacted
        g.TPX = float(t), ATM, f"O2:1.0, N2:{src.N2_PER_O2}"
        air_h.append(float(g.enthalpy_mass))
    p = Products(
        fuel, air_ratio, t_air, air, mass, reactants, temps, arr["h"], arr["rho"], arr["mu"],
        arr["k"], arr["cp"], arr["w"], arr["c"], arr["co"], air_enthalpy=np.array(air_h),
    )  # fmt: skip
    return replace(p, steps=_working(p))


ELECTRIC = Fuel("electricity (the elements' heat; the chamber's gas is air)", "gas")


@cache
def still_air(t_air: float) -> Products:
    """An electric kiln's chamber gas: air, no fuel and no stream through it (the elements heat
    the faces they line; a vent's flow isn't modelled). Its tables are air's (Cantera, as the
    products' are), its CO₂ and H₂O nil: a transparent gas. Per unit of "fuel", the elements'
    joule: no air, no products, one joule net."""
    g = _gas()
    temps = np.arange(T_MIN - T_STEP, T_MAX + T_STEP / 2, T_STEP)
    cols: dict[str, list[float]] = {k: [] for k in ("h", "rho", "mu", "k", "cp")}
    for t in temps:
        g.TPX = float(t), ATM, f"O2:1.0, N2:{src.N2_PER_O2}"
        cols["h"].append(float(g.enthalpy_mass))
        cols["rho"].append(float(g.density))
        cols["mu"].append(float(g.viscosity))
        cols["k"].append(float(g.thermal_conductivity))
        cols["cp"].append(float(g.cp_mass))
    arr = {k: np.array(v) for k, v in cols.items()}
    nil = np.zeros(len(temps))
    steps = (
        Step(name="The gas", value="air, its tables Cantera's (GRI-Mech 3.0 thermodynamics and "
             "transport); no fuel burns and no stream passes", reference=src.GRI30,
             note="an electric kiln's vent flow isn't modelled: its air is still"),
    )  # fmt: skip
    return Products(
        ELECTRIC, 1.0, t_air, 0.0, 0.0, 1.0, temps, arr["h"], arr["rho"], arr["mu"], arr["k"],
        arr["cp"], nil, nil, nil, steps, arr["h"],
    )  # fmt: skip


def _working(p: Products) -> tuple[Step, ...]:
    f = p.fuel
    if f.kind == "gas":
        what = f"{f.name}: Cantera species {f.species}, HHV {f.hhv / 1e6:.2f} MJ/kg"
        note = None
    else:
        c, h, o, n, s, ash = (100 * v for v in f.composition)
        what = (
            f"{f.name}: C {c:.1f}, H {h:.2f}, O {o:.1f}, N {n:.2f}, S {s:.2f}, ash {ash:.2f} % "
            f"dry; {f.moisture:.0%} moisture (wet basis), {f.net_dry / 1e6:.2f} MJ/kg net dry"
        )
        surrogate = f"{src.WOOD_CHO.note}; " if f.composition == SURROGATE else ""
        note = (
            f"{surrogate}the ash stays in the bed and the sulphur is left out of the gas "
            "(GRI-Mech has no sulphur; its air under 1 %)"
        )
    hot = p.released(1558.15)
    return (
        Step(name="The fuel", value=what, reference=f.reference, note=note),
        Step(
            name="Air and products per kg of fuel",
            value=f"{p.air:.3f} kg air, {p.mass:.3f} kg products",
            formula="λ × stoichiometric air; products = the fuel's gas-forming part (and its "
            "water) + air",
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
