"""Gas firing: burner input, the burners, the gas supply, the flue and the chimney.

- **Burner input** follows Olsen's Rule 1 (4th ed. p.226): about 10,000 BTU per cubic foot per
  hour at peak for an insulating-brick kiln, 16,000–19,000 for dense brick. Ward's table by wall
  and cone gives the range; at cone 10 its low end is Olsen's figure. The design's firing speed
  picks the low end (slow, the default) or the high end (fast, about 6–7 hours).
- **What must hold** is physical: the heat the burners leave in the kiln at the top temperature
  (their available heat, :mod:`kilndesigner.combustion`) must cover what the lining loses there.
  Fewer BTU than the rule of thumb fire more slowly, which is not a failure: Olsen fired a 36 ft³
  dense cross-draft on 6,000 BTU/ft³/hr in 12–15 hours (p.226).
- **Burners** come from the library, each at the pressure that gives its share, or are rated by
  the design for burners the library doesn't list.
- **The supply**: propane cylinders and tanks are checked against vaporization tables at the
  coldest air; a line (natural gas from the meter, or propane through regulators) gives a fixed
  pressure.
- **The flue** starts as large as the burner ports together (Olsen p.151), and larger in updrafts
  over 40 ft³ (p.173–174); it is then bricked down to tune the kiln.
- **The chimney**: gas under pressure drives the flow, so the chimney need only reach the top of
  the kiln or its frame, with a hood and stack above that (p.151). Its draft comes from the
  stack-effect equation.

Data: data/gas.yaml, from docs/research/combustion-and-masonry.md and kiln-reference.md.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from functools import cache
from importlib import resources
from typing import Any, Literal

import numpy as np
import yaml
from pydantic import BaseModel, ConfigDict

from kilndesigner.combustion import (
    OXIDATION_O2,
    PROPANE_HHV_BTU_PER_GAL,
    PROPANE_LB_PER_GAL,
    REDUCTION_AIR,
    air_ratio_for_flue_oxygen,
    available_heat_fraction,
)
from kilndesigner.combustion import SOURCE as COMBUSTION_SOURCE
from kilndesigner.cones import cone_temperature, hotter_than
from kilndesigner.gas_checks import (
    ALTITUDE,
    COOLING,
    LIQUID_COOLING_F,
    MOST_BURNERS,
    REGULATOR,
    TANK_TABLE_FILL,
    Demand,
    Draw,
    Pressure,
    Ratings,
    Supply,
    burner_capacity,
    burners,
    chimney_height,
    coldest_air,
    holds_top,
    pressure_ceiling,
    supply,
    unknown_burner,
    ward_range,
)
from kilndesigner.heatloss import top_temperature
from kilndesigner.model import (
    CatenaryArch,
    Cylinders,
    Dome,
    Gas,
    Kiln,
    Line,
    Port,
    SprungArch,
    Tank,
)
from kilndesigner.shape import chamber_shape
from kilndesigner.sheet import Check
from kilndesigner.units import Q_, Quantity, si
from kilndesigner.working import Finding, Step, show

PROPANE_BTU_PER_GAL = PROPANE_HHV_BTU_PER_GAL  # one propane data set (review G11)
STACK_C = 0.0342  # K/m, stack-effect equation [S42]
ATMOSPHERE = 101_325.0  # Pa
PA_PER_IN_WC = 249.09
CHIMNEY_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.151: with burners, the chimney as tall as the kiln or level "
    "with its top framework, then a ventilation hood and stack"
)
FLUE_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.151 (the exit flue as large as the burner ports, then "
    "restricted), p.173–174 (updrafts), p.236 (his three methods)"
)
OLSEN_INPUT = "Olsen, The Kiln Book, 4th ed., p.226 (Rule 1)"
DRAFT_SOURCE = "Stack effect, ΔP = 0.0342·a·h·(1/To − 1/Ti); combustion-and-masonry.md §4.2 [S42]"
ATMOSPHERE_SOURCE = (
    "NASA Glenn, Earth atmosphere model (troposphere): T = 15.04 − 0.00649·h °C, "
    "p = 101.29·((T + 273.1)/288.08)^5.256 kPa; combustion-and-masonry.md §4.3"
)
GAS_SAFETY = (
    "Gas piping, regulators, safety valves and the installation must be done or checked by a "
    "licensed gas fitter to your local code (NFPA 54 and 58 in the US)."
)
FLUE_PER_BTU = 7000.0  # BTU/hr per in² of exit flue, Olsen's third method (p.236)
FLUE_PER_FT3 = 2.5  # in² of exit flue per ft³, his second (p.236)
SLIGHTLY_UNDER = 0.9
"""An exit flue "slightly under" the inlets, as the Olsen 24 kit's 45 in² against its 50 in² of
burner ports (p.174)."""
BIG_UPDRAFT_FT3 = 40.0
"""Up to 40 ft³ an updraft's exit flue equals its inlets; larger ones need more (p.173–174)."""
BIG_UPDRAFT_EXTRA = 1.2  # "about 20 % more" from 50 ft³ (p.174)

type WallClass = Literal["hard_brick", "insulating_brick", "ceramic_fibre"]
WALL_WORDS = {
    "hard_brick": "9 in hard brick",
    "insulating_brick": "9 in insulating brick",
    "ceramic_fibre": "6 in ceramic fibre",
}
FUEL_WORDS = {"propane": "propane", "natural_gas": "natural gas"}


@cache
def gas_data() -> dict[str, Any]:
    text = resources.files("kilndesigner.data").joinpath("gas.yaml").read_text(encoding="utf-8")
    data: dict[str, Any] = yaml.safe_load(text)
    return data


def wall_class(kiln: Kiln) -> WallClass:
    """Ward's construction class from the walls' hot face."""
    from kilndesigner.castable import resolve_material

    kind = resolve_material(kiln, kiln.lining.walls[0].material).kind
    if kind in ("dense_firebrick", "dense_castable", "building_brick", "stone", "earth"):
        return "hard_brick"
    if kind in ("fibre_blanket", "fibre_board"):
        return "ceramic_fibre"
    return "insulating_brick"


def ward_volume(kiln: Kiln) -> tuple[float, str]:
    """Ward's chamber volume (m³) and how it was found: a sprung arch counts as ⅔ of its rise, a
    catenary as ⅔ of its base × height (§3.1, [S28]). Ward gives no formula for a dome, so its
    space is worked out exactly."""
    c = kiln.chamber
    w, d, h = si(c.width, "m"), si(c.length, "m"), si(c.height, "m")
    if c.shape == "round":
        return chamber_shape(kiln).volume, (
            "π/4 × D² × H, plus the space under the dome worked out exactly: Ward gives no "
            "formula for a round kiln"
        )
    if isinstance(kiln.roof, CatenaryArch):
        return d * (4 / 3 * h * w / 2), "L × (4/3 × H × ½ base), H to the crown"
    if isinstance(kiln.roof, Dome):
        return chamber_shape(kiln).volume, (
            "W × L × H, plus the space under the dome worked out exactly: Ward gives no formula "
            "for a dome"
        )
    if isinstance(kiln.roof, SprungArch):
        h += 2 / 3 * si(kiln.roof.rise, "m")
    return w * d * h, "W × L × H (a sprung arch adds ⅔ of its rise to H)"


def ward_column(top: Quantity) -> str | None:
    """The Ward column (cone 06, 6 or 10) that covers ``top``; None above cone 10."""
    t = si(top, "degC")
    for column in ("06", "6", "10"):
        if t <= si(cone_temperature(column), "degC") + 1e-6:
            return column
    return None


def interpolate(x: float, xs: list[float], ys: list[float]) -> float:
    return float(np.interp(x, xs, ys))


# ---- The air at the site ----------------------------------------------------------------------


def _atmosphere(elevation_m: float) -> tuple[float, float]:
    """NASA Glenn's troposphere: air temperature (°C) and pressure (kPa) at an elevation (m)."""
    t = 15.04 - 0.00649 * elevation_m
    return t, 101.29 * ((t + 273.1) / 288.08) ** 5.256


def air_pressure(elevation_m: float) -> float:
    """The standard atmosphere's pressure at an elevation, Pa, scaled so sea level is 101,325."""
    return ATMOSPHERE * _atmosphere(elevation_m)[1] / _atmosphere(0.0)[1]


def altitude_factor(elevation_m: float) -> float:
    """A burner's output at an elevation as a share of sea level: √σ, σ the air's density over sea
    level's. Through an orifice at a set gauge pressure the gas flows as √(Δp/ρ), and each cubic
    foot carries heat as ρ, so the heat goes as √ρ (derived; it reproduces Olsen's 0.9279 at
    5000 ft and 0.8579 at 10,000 ft, p.230–232, to 0.2 %)."""

    def density(h: float) -> float:
        t, p = _atmosphere(h)
        return p / (0.2869 * (t + 273.1))

    return math.sqrt(density(elevation_m) / density(0.0))


# ---- Burner ratings ---------------------------------------------------------------------------


def _on_one_orifice(spec: dict[str, Any]) -> tuple[list[float], list[float]]:
    """A venturi burner's published pressures (psi) and ratings (BTU/hr) from its
    ``curve_from_psi`` up: the ones on the same √pressure curve, so the same orifice
    (combustion-and-masonry.md §3.2)."""
    kept = [
        (p, r) for p, r in zip(spec["psi"], spec["btu_hr"], strict=True)
        if p >= spec["curve_from_psi"]
    ]  # fmt: skip
    return [p for p, _ in kept], [r for _, r in kept]


def venturi_pressure(btu: float, spec: dict[str, Any]) -> float | None:
    """Supply pressure (psi) at which a venturi burner gives ``btu``, read from its ratings.

    Between published pressures on one orifice, output rises with √pressure, so √pressure is
    interpolated. Outside them nothing is published: None.
    """
    psi, ratings = _on_one_orifice(spec)
    if not ratings[0] <= btu <= ratings[-1]:
        return None
    root = interpolate(btu, ratings, [math.sqrt(p) for p in psi])
    return root**2


NATURAL_GAS_LOW_PSI = 11 / 27.68
"""Low pressure, 11 in. w.c. or less (Olsen p.215): where the natural-gas ratings, at 8 in. w.c.,
can be carried by √pressure through the same orifice (p.216)."""


def line_rating(spec: dict[str, Any], fuel: str, psi: float) -> float | None:
    """A venturi burner's rating (BTU/hr, sea level) on a line held at ``psi``, or None if no
    published rating covers that gas at that pressure."""
    if fuel == "natural_gas":
        ng = spec.get("natural_gas")
        if ng is None or psi > NATURAL_GAS_LOW_PSI * (1 + 1e-9):
            return None
        return float(ng["btu_hr"]) * math.sqrt(psi * 27.68 / ng["in_wc"])
    pressures, ratings = _on_one_orifice(spec)
    if pressures[0] <= psi <= pressures[-1]:
        roots = [math.sqrt(p) for p in pressures]
        return interpolate(math.sqrt(psi), roots, ratings)
    for p, r in zip(spec["psi"], spec["btu_hr"], strict=True):  # a published low-pressure orifice
        if abs(p - psi) <= 0.01 * p:
            return float(r)
    return None


def _pressure_text(psi: float) -> str:
    return f"{psi:.1f} psi" if psi >= 1 else f"{psi * 27.7:.0f} in. w.c."


class BurnerOption(BaseModel):
    model_config = ConfigDict(frozen=True)

    model: str
    type: Literal["venturi", "power"]
    count: int
    pressure: str
    each: str
    total_cost: float


class SupplyCase(BaseModel):
    model_config = ConfigDict(frozen=True)

    case: str
    capacity: str
    capacity_btu_hr: float
    meets_demand: bool
    source: str


class GasDesign(BaseModel):
    model_config = ConfigDict(frozen=True)

    fuel: str
    construction: str
    ward_volume: str
    demand_range: str
    design_input: str
    design_input_btu_hr: float
    full_fire_btu_hr: float
    """What the burners put in at full fire: the design input, or their own when they differ."""
    propane_at_full_fire: str
    """The gas at full fire: gallons of propane, or cubic feet of natural gas, an hour."""
    burners: BurnerOption | None
    burner_options: list[BurnerOption]
    supply_temperature: str
    supply: list[SupplyCase]
    tank_suggestion: str | None
    chimney_height: str | None
    chimney_height_in: float | None
    flue_area: str
    flue_area_in2: float
    inlet_area_in2: float | None
    """The burner ports together, when their size is known."""
    draft: list[str]
    working: list[Step]
    findings: list[Finding]


@dataclass(frozen=True)
class Supplying:
    """How the burners are fed: the most pressure they may run at, and whether it is a line's."""

    max_psi: float
    line: bool
    altitude: float


def named_model(kind: Literal["venturi", "power"], named: str) -> str | None:
    """The library's name for the burner a design names: 'MR100' or 'Ward MB400' will do."""
    for name in gas_data()[f"{kind}_burners"]["models"]:
        if (name if kind == "venturi" else f"Ward {name}").endswith(named):
            return str(name)
    return None


def _each_at(
    spec: dict[str, Any], kind: str, share: float, how: Supplying, fuel: str
) -> tuple[float, float] | None:
    """The pressure (psi) a library burner runs at to carry ``share`` BTU/hr at the site, and what
    it then gives there; None if it can't. On a line the pressure is the line's, and the burner
    gives its rating there."""
    if kind == "power":
        rating = float(spec["btu_hr"]) * how.altitude
        return (11 / 27.68, share) if share <= rating else None
    if how.line:
        r = line_rating(spec, fuel, how.max_psi)
        return None if r is None else (how.max_psi, r * how.altitude)
    p = venturi_pressure(share / how.altitude, spec)
    if p is None or p > how.max_psi:
        return None
    return p, share


def _burner_options(
    demand: float,
    kind: Literal["venturi", "power"],
    how: Supplying,
    fuel: str,
    only: str | None = None,
) -> list[BurnerOption]:
    """The sets of up to MOST_BURNERS burners that carry ``demand``, fewest first: every venturi
    model at the pressure that gives its share (or, on a line, its rating there), the smallest
    power burner that does (or only ``only``)."""
    data = gas_data()
    models = {
        name: spec
        for name, spec in data[f"{kind}_burners"]["models"].items()
        if only is None or name == only
    }
    options: list[BurnerOption] = []
    for count in range(1, MOST_BURNERS + 1):
        share = demand / count
        for name, spec in models.items():
            set_at = _each_at(spec, kind, share, how, fuel)
            if set_at is None:
                continue
            p, each = set_at
            if how.line and kind == "venturi" and count * each < demand * (1 - 1e-9):
                continue  # on a line each gives its rating: too few to carry the input
            if how.line and kind == "venturi" and (count - 1) * each >= demand * (1 - 1e-9):
                continue  # one fewer would do
            options.append(
                BurnerOption(
                    model=name if kind == "venturi" else f"Ward {name}", type=kind, count=count,
                    pressure=_pressure_text(p), each=f"{each:,.0f} BTU/hr",
                    total_cost=count * spec["price"],
                )
            )  # fmt: skip
            if kind == "power":
                break
    options.sort(key=lambda o: (o.count, o.total_cost))
    return options


def _supply_cases(gas: Gas, demand: float, t_f: float) -> tuple[list[SupplyCase], float]:
    data = gas_data()
    cases: list[SupplyCase] = []
    supply = gas.supply
    t = min(max(t_f, 0.0), 70.0)
    if isinstance(supply, Cylinders):
        opt = data["cylinder_100lb_optimistic"]
        con = data["cylinder_100lb_conservative"]
        n = supply.count
        liquid = min(max(t_f - LIQUID_COOLING_F, 0.0), 70.0)  # the table is by liquid temperature
        for label, lb in (("full", 100), ("half full", 50)):
            each = interpolate(liquid, opt["temps_f"], opt["rows"][lb])
            cases.append(
                SupplyCase(
                    case=f"{n} × 100 lb cylinders, {label}",
                    capacity=f"{n * each:,.0f} BTU/hr ({each:,.0f} each)",
                    capacity_btu_hr=n * each, meets_demand=n * each >= demand,
                    source=f"{opt['source']}, read at the liquid's temperature ({COOLING})",
                )
            )  # fmt: skip
        each = interpolate(min(t, 60.0), con["temps_f"], con["btu_hr"])
        cases.append(
            SupplyCase(
                case=f"{n} × 100 lb cylinders, ¼ full, keeping 10 psi",
                capacity=f"{n * each:,.0f} BTU/hr ({each:,.0f} each)",
                capacity_btu_hr=n * each, meets_demand=n * each >= demand,
                source=con["source"],
            )
        )  # fmt: skip
        return cases, n * 100 / PROPANE_LB_PER_GAL
    assert isinstance(supply, Tank)
    table = data["tanks_one_third_full"]
    cap = interpolate(t, table["temps_f"], table["gallons"][supply.gallons]) * TANK_TABLE_FILL
    cases.append(
        SupplyCase(
            case=f"{supply.gallons} gal tank, ⅓ full",
            capacity=f"{cap:,.0f} BTU/hr",
            capacity_btu_hr=cap, meets_demand=cap >= demand,
            source=f"{table['source']}, × 73.3/90 for ⅓ full (§2.3, §2.8)",
        )
    )  # fmt: skip
    return cases, supply.gallons / 3


def _supply(gas: Gas, t_f: float, conservative: bool) -> Supply:
    """The supply case a sheet checks: full cylinders or the tank ⅓ full, or the cylinders' own
    conservative case (¼ full, keeping 10 psi)."""
    data = gas_data()
    if isinstance(gas.supply, Cylinders):
        n = gas.supply.count
        if conservative:
            con = data["cylinder_100lb_conservative"]
            return Supply(
                f"{n} × 100 lb cylinders, ¼ full, keeping 10 psi",
                n,
                t_f,
                (con["temps_f"], con["btu_hr"]),
                con["source"],
            )
        opt = data["cylinder_100lb_optimistic"]
        return Supply(
            f"{n} × 100 lb cylinders, full",
            n,
            t_f,
            (opt["temps_f"], opt["rows"][100]),
            opt["source"],
            by_liquid=True,
        )
    assert isinstance(gas.supply, Tank)
    table = data["tanks_one_third_full"]
    return Supply(
        f"{gas.supply.gallons} gal tank, ⅓ full",
        None,
        t_f,
        (table["temps_f"], table["gallons"][gas.supply.gallons]),
        table["source"],
        fill=TANK_TABLE_FILL,
    )


def _demand(kiln: Kiln, per_ft3: float, volume_ft3: float, what: str, source: str) -> Demand:
    """The design's numbers the input's sheets start from: Ward's volume and the figure used."""
    c, roof = kiln.chamber, kiln.roof
    kind = (
        "round"
        if c.shape == "round"
        else "catenary"
        if isinstance(roof, CatenaryArch)
        else "dome"
        if isinstance(roof, Dome)
        else "sprung_arch"
        if isinstance(roof, SprungArch)
        else "flat"
    )
    rise = si(roof.rise, "in") if isinstance(roof, SprungArch) else 0.0
    return Demand(
        kind,
        si(c.width, "in"),
        si(c.length, "in"),
        si(c.height, "in"),
        rise,
        volume_ft3,
        per_ft3,
        what,
        source,
    )


def tank_suggestion(demand: float, t_f: float) -> str | None:
    table = gas_data()["tanks_one_third_full"]
    t = min(max(t_f, 0.0), 70.0)
    for gallons, row in table["gallons"].items():
        cap = interpolate(t, table["temps_f"], row) * TANK_TABLE_FILL
        if cap >= demand:
            return (
                f"A {gallons} gal tank, kept at least ⅓ full, supplies "
                f"{cap:,.0f} BTU/hr at {t_f:.0f} °F"
            )
    return None


def _oversized(
    gas: Gas, demand: float, how: Supplying, only: str | None
) -> tuple[BurnerOption, float] | None:
    """The burners the design names (``only``, the library's name for them), when each is bigger
    than its share of the load even at the lowest pressure its ratings are published for on one
    orifice: at that pressure, and what they draw there. None if the design doesn't name both a
    venturi model and a count, or the burners are on a line (they run at the line's pressure)."""
    asked = gas.burners
    count = asked.wanted
    spec = gas_data()["venturi_burners"]["models"].get(only or "")
    if asked.type != "venturi" or only is None or spec is None or count is None or how.line:
        return None
    psi, ratings = _on_one_orifice(spec)
    low = ratings[0] * how.altitude
    if demand / count >= low or psi[0] > how.max_psi:
        return None
    option = BurnerOption(
        model=only,
        type="venturi",
        count=count,
        pressure=_pressure_text(psi[0]),
        each=f"{low:,.0f} BTU/hr",
        total_cost=count * spec["price"],
    )
    return option, count * low


def _ratings(
    kind: Literal["venturi", "power"], name: str, how: Supplying, fuel: str
) -> Ratings | None:
    data = gas_data()[f"{kind}_burners"]
    spec = data["models"][name]
    if kind == "power":
        return Ratings(
            f"Ward {name}", kind, (), (float(spec["btu_hr"]),), data["source"], how.altitude
        )
    if how.line:
        r = line_rating(spec, fuel, how.max_psi)
        if r is None:
            return None
        source = data["natural_gas_source"] if fuel == "natural_gas" else data["source"]
        return Ratings(name, "rated", (how.max_psi,), (r,), source, how.altitude)
    psi, btu = _on_one_orifice(spec)
    return Ratings(
        name, kind, tuple(psi), tuple(float(b) for b in btu), data["source"], how.altitude
    )


def _pressure(gas: Gas, how: Supplying, t_f: float) -> Pressure:
    vapour = gas_data()["vapour_pressure"]
    return Pressure(
        tank=isinstance(gas.supply, Tank), air_f=t_f,
        vapour=(vapour["temps_f"], vapour["psig"]), vapour_source=vapour["source"],
        line_psi=how.max_psi if how.line else None,
    )  # fmt: skip


def _burner_check(
    gas: Gas,
    need: Demand,
    demand: float,
    how: Supplying,
    t_f: float,
    only: str | None,
    oversized: bool,
) -> Check:
    """The sheet of the set that comes closest to carrying the input: the named burner, or else the
    library's nearest, at the named count, or else the fewest whose top rating covers it."""
    kind, wanted = gas.burners.type, gas.burners.wanted
    best: tuple[float, Ratings, int] | None = None
    for name in gas_data()[f"{kind}_burners"]["models"]:
        if only is not None and name != only:
            continue
        r = _ratings(kind, name, how, gas.fuel)
        if r is None:
            continue
        reach = kind != "venturi" or how.max_psi >= r.psi[0]
        cap = burner_capacity(r, how.max_psi) if reach else 0.0
        most = MOST_BURNERS
        n = wanted or (min(max(math.ceil(demand / cap - 1e-9), 1), most) if cap > 0 else most)
        q = demand / n
        short = (max(q / cap - 1, 0) if cap > 0 else math.inf) + (
            max(r.btu_hr[0] * r.altitude / q - 1, 0) if r.kind == "venturi" else 0
        )
        if best is None or short < best[0]:
            best = (short, r, n)
    if best is None:  # no library burner is rated for this gas at this pressure
        known = list(gas_data()[f"{kind}_burners"]["models"])
        return unknown_burner(
            gas.burners.model or "a library burner",
            kind,
            known,
            gas_data()[f"{kind}_burners"]["source"],
        ).check()
    _, r, n = best
    why = (
        "the design"
        if wanted
        else f"the fewest {r.model}s whose rating at the most pressure covers the input, up to "
        f"{MOST_BURNERS}"
    )
    sheet = burners(need, n, why, r, _pressure(gas, how, t_f), "warning" if oversized else "error")
    sheet.agrees("D", Q_(demand, "BTU/hr"))
    sheet.agrees("q", Q_(demand / n, "BTU/hr"))
    if r.kind == "venturi":
        sheet.agrees("p_max", Q_(how.max_psi, "psi"))
        if how.max_psi >= r.psi[0]:
            sheet.agrees("r_cap", Q_(burner_capacity(r, how.max_psi), "BTU/hr"))
    return sheet.check()


@dataclass(frozen=True)
class Burning:
    """The burners as fired: the set, each burner's input at full fire at the site, how many, and
    where that figure comes from."""

    chosen: BurnerOption | None
    count: int
    each: float  # BTU/hr, at full fire, at the site
    source: str
    options: list[BurnerOption]

    @property
    def draw(self) -> float:
        return self.count * self.each


def _supplying(gas: Gas, t_f: float, altitude: float, working: list[Step]) -> Supplying:
    """The most pressure the burners may run at: a line's own; or, on cylinders or a tank, the
    regulator set 20 psi under propane's vapour pressure with the liquid 20 °F under the coldest
    air, no more than 20 psi, less 20 % droop at full flow (RegO 597F)."""
    if isinstance(gas.supply, Line):
        psi = si(gas.supply.pressure, "psi")
        working.append(
            Step(
                name=f"{FUEL_WORDS[gas.fuel].capitalize()} pressure at the burners",
                value=_pressure_text(psi),
                inputs={"from": "the line (supply.pressure)"},
            )
        )
        return Supplying(psi, True, altitude)
    vapour = gas_data()["vapour_pressure"]
    liquid = t_f - LIQUID_COOLING_F
    tank_psig = interpolate(liquid, vapour["temps_f"], vapour["psig"])
    max_psi = pressure_ceiling(tank_psig)
    working.append(
        Step(
            name="Propane pressure available",
            value=f"{tank_psig:.0f} psig in the cylinder or tank, the liquid at {liquid:.0f} °F",
            formula="0.8 × min(20 psi, p_v − 20 psi)",
            inputs={
                "coldest air": f"{t_f:.0f} °F",
                "liquid under draw": f"{LIQUID_COOLING_F:.0f} °F colder",
                "burners limited to": f"{max_psi:.3g} psi",
            },
            reference=f"{vapour['source']}; {COOLING}; {REGULATOR}",
            note=(
                "The regulator needs its inlet 20 psi over its setting, and at full flow delivers "
                "20 % under it; the burners' ratings go to 20 psi."
            ),
        )
    )
    return Supplying(max_psi, False, altitude)


def _choose_burners(
    gas: Gas,
    need: Demand,
    demand: float,
    how: Supplying,
    t_f: float,
    working: list[Step],
    findings: list[Finding],
) -> Burning:
    """The burners and what each puts in at full fire. A design that names its burners fires on
    them, at the design input if they can give it, or at all they can give if not: fewer BTU than
    the rule of thumb is a slower firing, and the energy check (gas.top) says whether the kiln
    gets to the top at all."""
    data = gas_data()
    asked = gas.burners
    kind = asked.type
    wanted = asked.wanted
    fuel = FUEL_WORDS[gas.fuel]
    if asked.rating is not None:
        assert wanted is not None
        each = si(asked.rating, "BTU/hr") * how.altitude
        working.append(
            Step(
                name="Burners",
                value=f"{wanted} × {each:,.0f} BTU/hr",
                inputs={
                    "each, as rated": show(asked.rating, "BTU/hr"),
                    **({"× elevation": f"{how.altitude:.4f}"} if how.altitude != 1 else {}),
                },
                reference="the design: burners.rating",
            )
        )
        _short_of_the_rule(wanted * each, demand, need, findings)
        return Burning(None, wanted, each, "the design: burners.rating", [])
    options = _burner_options(demand, kind, how, gas.fuel)
    only = named_model(kind, asked.model) if asked.model else None
    source = data[f"{kind}_burners"]["source"]
    if asked.model and only is None:
        known = list(data[f"{kind}_burners"]["models"])
        findings.append(
            Finding.failed(
                unknown_burner(asked.model, kind, known, source).check(),
                message=(
                    f"{asked.model} isn't a {kind} burner whose ratings the library has: choose "
                    f"one of {', '.join(known)}, give the burners' rating instead, or leave the "
                    "model out."
                ),
            )
        )
        return Burning(None, wanted or 1, demand / (wanted or 1), source, options)
    if asked.model or wanted:
        named = _burner_options(demand, kind, how, gas.fuel, only) if only else options
        matching = [o for o in named if wanted is None or o.count == wanted]
        if matching:
            chosen = matching[0]
            return _burning(chosen, _each(chosen, demand, how, gas), demand, how, working, options)
        big = _oversized(gas, demand, how, only)
        if big is not None:
            chosen, draw = big
            findings.append(
                Finding.failed(
                    _burner_check(gas, need, demand, how, t_f, only, oversized=True),
                    message=(
                        f"Each {chosen.model} gives {chosen.each} at {chosen.pressure}, the lowest "
                        "pressure its ratings are published for on one orifice, and that is more "
                        f"than the {demand / chosen.count:,.0f} BTU/hr each this kiln needs. Its "
                        "output lower down isn't published, so the supply is checked against the "
                        f"{draw:,.0f} BTU/hr the {chosen.count} burners draw there. Fewer or "
                        "smaller burners would run within their ratings."
                    ),
                    reference=f"{source}; the curve, §3.2 (derived)",
                )
            )
            return _burning(chosen, draw / chosen.count, demand, how, working, options)
        # Named burners short of the rule of thumb: they fire at all they can give
        full = _at_full(gas, only, wanted, how)
        if full is not None:
            chosen, each = full
            _short_of_the_rule(chosen.count * each, demand, need, findings)
            return _burning(chosen, each, demand, how, working, options)
        findings.append(
            Finding.failed(
                _burner_check(gas, need, demand, how, t_f, only, oversized=False),
                message=(
                    f"The burners chosen aren't rated for {fuel} at "
                    f"{_pressure_text(how.max_psi)}. Choose others, or give their rating."
                ),
            )
        )
        return Burning(None, wanted or 1, 0.0, source, options)
    if options:
        chosen = options[0]
        # Review G10: the fewest burners is the engine's pick, not a source's; Olsen's builds use
        # several. Said, not imposed: no source gives a rule for the count.
        findings.append(
            Finding(
                level="info",
                message=(
                    f"The tool chose the fewest burners that carry the input ({chosen.count} × "
                    f"{chosen.model}). Olsen's builds use several: a 20 ft³ cross-draft on four, "
                    "a 36 ft³ cross-draft on six and an IFB updraft that size on at least ten "
                    "(p.226–228). No source gives a rule for the count; set burners.count to "
                    "spread the heat over more."
                ),
                reference="Olsen, The Kiln Book, 4th ed., p.226–228; kiln-reference.md",
            )
        )
        return _burning(chosen, _each(chosen, demand, how, gas), demand, how, working, options)
    findings.append(
        Finding.failed(
            _burner_check(gas, need, demand, how, t_f, None, oversized=False),
            message=(
                f"No set of up to {MOST_BURNERS} {kind} burners in the library delivers the "
                f"{demand:,.0f} BTU/hr design input on {fuel} within "
                f"{_pressure_text(how.max_psi)}, so none is chosen. Give the burners and their "
                "rating."
            ),
        )
    )
    return Burning(None, 0, 0.0, source, [])


def _each(option: BurnerOption, demand: float, how: Supplying, gas: Gas) -> float:
    """What each burner of a library set puts in at full fire, exactly: its share of the input,
    or on a line its rating at the line's pressure."""
    if not how.line or option.type == "power":
        return demand / option.count
    spec = gas_data()["venturi_burners"]["models"][option.model]
    rating = line_rating(spec, gas.fuel, how.max_psi)
    assert rating is not None  # the option was listed because it has one
    return rating * how.altitude


def _at_full(
    gas: Gas, only: str | None, wanted: int | None, how: Supplying
) -> tuple[BurnerOption, float] | None:
    """The named model, or the library's biggest at the named count, at the most pressure allowed:
    what it gives there at the site. None if nothing is rated for the gas and pressure."""
    kind = gas.burners.type
    best: tuple[BurnerOption, float] | None = None
    for name, spec in gas_data()[f"{kind}_burners"]["models"].items():
        if only is not None and name != only:
            continue
        r = _ratings(kind, name, how, gas.fuel)
        if r is None or (r.kind == "venturi" and how.max_psi < r.psi[0]):
            continue
        each = burner_capacity(r, how.max_psi)
        count = wanted or 1
        option = BurnerOption(
            model=name if kind == "venturi" else f"Ward {name}", type=kind, count=count,
            pressure=_pressure_text(how.max_psi if kind == "venturi" else 11 / 27.68),
            each=f"{each:,.0f} BTU/hr", total_cost=count * spec["price"],
        )  # fmt: skip
        if best is None or each > best[1]:
            best = (option, each)
    return best


def _short_of_the_rule(full: float, demand: float, need: Demand, findings: list[Finding]) -> None:
    if full >= demand * (1 - 1e-9):
        return
    findings.append(
        Finding(
            level="info",
            message=(
                f"The burners give {full:,.0f} BTU/hr at full fire, "
                f"{full / need.dome_ft3:,.0f} "
                f"BTU per ft³ an hour, under the {demand:,.0f} BTU/hr of the rule of thumb "
                f"({need.btu_per_ft3_hr:,.0f} BTU/ft³/hr). That fires more slowly, not worse: "
                "Olsen fired a 36 ft³ dense cross-draft on 6,000 BTU/ft³/hr to cone 10 in 12–15 "
                "hours. The energy check (the burners against the heat loss at the top) says "
                "whether they reach the top at all."
            ),
            reference=f"{OLSEN_INPUT}, p.226",
        )
    )


def _burning(
    chosen: BurnerOption,
    each: float,
    demand: float,
    how: Supplying,
    working: list[Step],
    options: list[BurnerOption],
) -> Burning:
    data = gas_data()
    working.append(
        Step(
            name="Burners",
            value=f"{chosen.count} × {chosen.model} at {chosen.pressure}",
            inputs={
                "each": f"{each:,.0f} BTU/hr",
                "cost": f"${chosen.total_cost:,.2f}",
                **({"× elevation": f"{how.altitude:.4f}"} if how.altitude != 1 else {}),
            },
            reference=data[f"{chosen.type}_burners"]["source"],
            note=(
                None
                if chosen.type != "venturi"
                else "On a line each burner gives its rating at the line's pressure."
                if how.line
                else "The pressure at which each gives its share, read from its published "
                "ratings: between them, output rises with √pressure (§3.2, derived)."
                if chosen.count * each <= demand * (1 + 1e-9)
                else "The lowest pressure its ratings are published for on one orifice; each "
                "gives more than its share there (§3.2, derived)."
            ),
        )
    )
    return Burning(chosen, chosen.count, each, data[f"{chosen.type}_burners"]["source"], options)


# ---- Ports, flue and chimney ------------------------------------------------------------------

# Burner ports by model: ("round", diameter) or ("rect", width, height), in inches, and the
# burner's body (diameter, length) where a source gives it.
BURNER_PORTS: dict[str, tuple[tuple[str, float, float], tuple[float, float] | None, str]] = {
    "GACO MR750": (
        ("round", 3.5, 3.5),
        (2.5, 8.0),
        "Ward's port, an inch wider than the 2.5 in head; the same as Robinson's 3½ in "
        "hole for MR-750s (kiln-hardware.md §1.1 [S1] [S30] [S6], derived)",
    ),
    "GACO MR100": (
        ("rect", 4.5, 5.0),
        None,
        "4½ × 5 in, half a brick by two courses, as Pitelka built for MR-100s "
        "(kiln-hardware.md §1.1 [S4] [S5]). The burner's size is not sourced.",
    ),
}
RANSOME = {
    "Ransome B1": (8.5, 1.875),
    "Ransome B2": (10.5, 2.75),
    "Ransome B3": (12.0, 3.25),
    "Ransome B4": (17.0, 3.75),
    "Ransome B5": (21.0, 5.0),
}
for _model, (_length, _end) in RANSOME.items():
    BURNER_PORTS[_model] = (
        ("round", _end + 1, _end + 1),
        (_end, _length),
        f"Ward's port, an inch wider than the burner's {_end:g} in larger end, taken as the head; "
        "the catalogue doesn't say which end is the head (kiln-hardware.md §1.1, §1.2 [S1] [S9], "
        "derived)",
    )


def burner_port(gas: Gas, chosen: BurnerOption | None) -> Port | None:
    """The size of each burner's port: the design's, or the one its model's sources give."""
    if gas.burners.port is not None:
        return gas.burners.port
    spec = BURNER_PORTS.get(chosen.model) if chosen is not None else None
    if spec is None:
        return None
    shape, w, h = spec[0]
    return (
        Port(diameter=Q_(w, "in"))
        if shape == "round"
        else Port(width=Q_(w, "in"), height=Q_(h, "in"))
    )


def port_area_in2(port: Port) -> float:
    w, h = port.size_in()
    return math.pi * w * w / 4 if port.round else w * h


def kiln_top_in(kiln: Kiln) -> float:
    """The outside top of the kiln above the chamber floor (in): the crown of its roof, outside.
    An open top's is the top of its walls."""
    layers = [] if kiln.roof.type == "open" else kiln.lining.for_face("roof")
    roof = sum(si(x.thickness, "in") for x in layers)
    top = si(kiln.chamber.height, "in") + roof
    if isinstance(kiln.roof, SprungArch | Dome):
        top += si(kiln.roof.rise, "in")
    return top


def starting_flue(
    inlet: float | None, draw: float, volume_ft3: float, updraft: bool
) -> tuple[float, str]:
    """Olsen's starting size for the exit flue (in²) and how it was found: the burner ports
    together (p.151), more in an updraft over 40 ft³ (p.173–174); without the ports' size, his
    third method, 1 in² per 7000 BTU/hr (p.236)."""
    if inlet is not None:
        if updraft and volume_ft3 > BIG_UPDRAFT_FT3:
            return BIG_UPDRAFT_EXTRA * inlet, (
                "1.2 × the burner ports together: an updraft over 40 ft³ needs about 20 % more "
                "exit than inlet (p.174)"
            )
        return inlet, "the burner ports together, 1 : 1 (p.151, p.173)"
    return draw / FLUE_PER_BTU, "1 in² per 7000 BTU/hr of burner input (p.236, his third method)"


def _draft_lines(
    kiln: Kiln, height_in: float, top: Quantity, working: list[Step], temp_unit: str
) -> list[str]:
    """The stack draft at the chimney's base, with warm air (the least draft: codes give no summer
    design figure, structure-and-draft.md §4)."""
    to = si(kiln.site.ambient, "K")
    a = air_pressure(si(kiln.site.elevation, "m") if kiln.site.elevation is not None else 0.0)
    lines: list[str] = []
    for label, flue in (
        ("flue gas at 1000 °F", Q_(1000, "degF")),
        ("flue gas at top temperature", top),
    ):
        dp = STACK_C * a * si(Q_(height_in, "in"), "m") * (1 / to - 1 / si(flue, "K"))
        line = f"{dp / PA_PER_IN_WC:.3f} in. w.c. ({dp:.0f} Pa) with {label}"
        lines.append(line)
        working.append(
            Step(
                name="Draft at the chimney's base",
                value=line,
                inputs={
                    "outside air": show(kiln.site.ambient, temp_unit),
                    "air pressure": f"{a / 1000:.1f} kPa",
                },
                reference=DRAFT_SOURCE if kiln.site.elevation is None else (
                    f"{DRAFT_SOURCE}; {ATMOSPHERE_SOURCE}"
                ),
            )
        )  # fmt: skip
    return lines


def design_gas(
    kiln: Kiln,
    loss_watts: float | None = None,
    input_btu_hr: float | None = None,
    *,
    elements_on_top_w: float | None = None,
) -> GasDesign:
    """The burners, supply, flue and chimney of a gas kiln. With ``loss_watts``, the kiln's steady
    heat loss at its top temperature, the burners are also checked against it. ``input_btu_hr``
    replaces the rule-of-thumb input: the one the target-time solver found.
    ``elements_on_top_w`` is a hybrid's element power when the elements stay on to the top (the
    solver's firing): the top check counts it with the burners'. Without it a hybrid's burners are
    checked alone, as the elements hand over below the top."""
    gas = kiln.heat.gas
    if gas is None:
        raise ValueError("the kiln has no gas heat")
    data = gas_data()
    findings: list[Finding] = []
    working: list[Step] = []
    us = kiln.units == "us"
    temp_unit = "degF" if us else "degC"
    fuel = FUEL_WORDS[gas.fuel]

    top, _ = top_temperature(kiln)
    construction = wall_class(kiln)
    column = ward_column(top)
    volume_m3, volume_formula = ward_volume(kiln)
    volume_ft3 = volume_m3 / si(Q_(1, "ft**3"), "m**3")
    ward = data["ward_btu_per_ft3_hr"]
    # Past cone 10 by the design's temperature or by its cone, whichever it gives. Kilns are fired
    # past it, so a warning; the burners are sized from the column the temperature reaches.
    firing = kiln.firing
    past: list[str] = []
    if firing.top_temperature is not None and column is None:
        past.append(show(top, temp_unit))
    if firing.cone is not None and hotter_than(firing.cone, "10"):
        past.append(f"cone {firing.cone}")
    column = column or "10"
    in_range = ward_range(
        top,
        firing.top_temperature is not None,
        firing.cone,
        firing.cone is not None and hotter_than(firing.cone, "10"),
        cone_temperature("10"),
        ward["source"],
    ).check()
    if in_range.status != "pass":
        findings.append(
            Finding.failed(
                in_range,
                message=(
                    "Ward's burner table stops at cone 10, and this design goes past it "
                    f"({' and '.join(past)}): the burners are sized from the cone {column} "
                    "column and may be short of heat at the top."
                ),
            )
        )
    low, high = ward["walls"][construction][ward["columns"].index(column)]
    fast = gas.firing_speed == "fast"
    per_ft3 = high if fast else low
    demand = per_ft3 * volume_ft3
    need = _demand(
        kiln,
        per_ft3,
        volume_ft3,
        f"{WALL_WORDS[construction]}, cone {column}, the {'fast (high)' if fast else 'slow (low)'} "
        "end",
        ward["source"],
    )
    olsen = data["olsen_btu_per_ft3_hr"].get(construction)
    working += [
        Step(
            name="Chamber volume, Ward's way",
            value=f"{volume_ft3:.1f} ft³",
            formula=volume_formula,
            reference=ward["source"],
        ),
        Step(
            name="Burner input per cubic foot",
            value=f"{low:,}–{high:,} BTU/ft³/hr",
            inputs={
                "construction": WALL_WORDS[construction],
                "this kiln's walls": " + ".join(
                    f"{show(layer.thickness, 'in' if us else 'mm')} {layer.material}"
                    for layer in kiln.lining.walls
                ),
                "cone column": column,
                **(
                    {"Olsen's Rule 1": f"{olsen[0]:,}–{olsen[1]:,} BTU/ft³/hr"}
                    if olsen is not None
                    else {}
                ),
            },
            reference=f"{ward['source']}; {data['olsen_btu_per_ft3_hr']['source']}",
            note=(
                "Olsen's Rule 1 is the low end of Ward's range at cone 10. He calls most gas kilns "
                "overpowered: a 36 ft³ IFB updraft on 10,000 BTU/ft³/hr fires in about 8 hours. "
                "Ward's high end gives about 6–7 hours. The table's column is chosen by the hot "
                "face and assumes its construction; a thinner or thicker wall is checked by the "
                "energy balance at the top temperature (gas.top), from this kiln's own heat loss."
            ),
        ),
        Step(
            name="Design burner input",
            value=f"{demand:,.0f} BTU/hr ({show(Q_(demand, 'BTU/hr'), 'kW')})",
            formula=f"{'high' if fast else 'low'} end × volume",
            inputs={"firing speed": gas.firing_speed},
        ),
    ]
    if input_btu_hr is not None:
        demand = input_btu_hr
        need = replace(
            need,
            btu_per_ft3_hr=demand / volume_ft3,
            what="the input the firing simulation found for the target firing time",
            source="the firing simulation (simulation.py, ADR 0015)",
        )
        working.append(
            Step(
                name="Burner input for the target firing time",
                value=f"{demand:,.0f} BTU/hr ({demand / volume_ft3:,.0f} BTU/ft³/hr)",
                note="Found with the firing simulation, in place of the rule of thumb above.",
                reference="simulation.py (ADR 0015); target.py",
            )
        )
    if kiln.heat.electric is not None and elements_on_top_w is None:
        findings.append(
            Finding(
                level="info",
                message=(
                    "The burners are sized to fire the kiln on their own, because the elements "
                    "are switched off before the top of the firing."
                ),
            )
        )

    t_cold = (
        kiln.site.coldest_ambient if kiln.site.coldest_ambient is not None else kiln.site.ambient
    )
    t_f = si(t_cold, "degF")
    on_line = isinstance(gas.supply, Line)
    if not on_line:
        tables = (
            f"{data['cylinder_100lb_optimistic']['source']}; "
            f"{data['tanks_one_third_full']['source']}"
        )
        # The cylinder table is by the liquid's temperature, 20 °F under the air under draw
        first = data["cylinder_100lb_optimistic"]["temps_f"][0] + (
            LIQUID_COOLING_F if isinstance(gas.supply, Cylinders) else 0.0
        )
        cold = coldest_air(t_f, first, f"{tables}; {COOLING}").check()
        if cold.status != "pass":
            findings.append(
                Finding.failed(
                    cold,
                    message=(
                        f"The vaporization tables start at {first:.0f} °F of air (the cylinder "
                        "table at 0 °F of liquid, which runs 20 °F under the air); colder firing "
                        "can't be checked."
                    ),
                )
            )

    elevation = si(kiln.site.elevation, "m") if kiln.site.elevation is not None else 0.0
    altitude = altitude_factor(elevation)
    if kiln.site.elevation is not None:
        working.append(
            Step(
                name="Burner output at the site's elevation",
                value=f"× {altitude:.4f}",
                formula="√σ, σ the air's density at the site over sea level's",
                inputs={"elevation": show(kiln.site.elevation, "ft" if us else "m")},
                reference=f"{ALTITUDE}; {ATMOSPHERE_SOURCE}",
            )
        )

    # The burners, and what they draw: the supply must keep up with that
    how = _supplying(gas, t_f, altitude, working)
    burning = _choose_burners(gas, need, demand, how, t_f, working, findings)
    chosen, draw = burning.chosen, burning.draw
    if gas.fuel == "propane":
        gal_hr = draw / PROPANE_BTU_PER_GAL
        at_full = f"{gal_hr:.2f} gal/hr"
        working.append(
            Step(
                name="Propane at full fire",
                value=f"{gal_hr:.2f} gal/hr ({gal_hr * PROPANE_LB_PER_GAL:.1f} lb/hr)",
                formula="BTU/hr ÷ 91,502 BTU/gal",
                inputs={} if draw == demand else {"the burners draw": f"{draw:,.0f} BTU/hr"},
                reference="combustion-and-masonry.md §1.1 [S1, S2]",
            )
        )
    else:
        cfh = draw / data["natural_gas"]["btu_per_ft3"]
        at_full = f"{cfh:,.0f} ft³/hr"
        working.append(
            Step(
                name="Natural gas at full fire",
                value=f"{cfh:,.0f} ft³/hr",
                formula="BTU/hr ÷ 1000 BTU/ft³",
                inputs={} if draw == demand else {"the burners draw": f"{draw:,.0f} BTU/hr"},
                reference=data["natural_gas"]["source"],
                note=(
                    "Check the meter and the line can pass it: Olsen's 20 ft³ kiln needed "
                    "182 ft³/hr against a house meter's 175 (p.228)."
                ),
            )
        )

    # The burners against the heat the kiln loses at the top: the one limit that is physical
    if loss_watts is not None and burning.count > 0 and burning.each > 0:
        lam = REDUCTION_AIR if gas.reduction else air_ratio_for_flue_oxygen(OXIDATION_O2, gas.fuel)
        eta = available_heat_fraction(si(top, "K"), lam, si(kiln.site.ambient, "K"), gas.fuel)
        air = (
            f"λ = {lam:.2f}, a moderate reduction"
            if gas.reduction
            else f"λ = {lam:.2f}, {OXIDATION_O2:.0%} oxygen in the flue"
        )
        working.append(
            Step(
                name="Available heat at the top temperature",
                value=f"{eta:.3f}",
                formula="(HHV − heat in the flue gas at T_top) ÷ HHV",
                inputs={"fuel": fuel, "air": air, "flue gas": show(top, temp_unit)},
                reference=COMBUSTION_SOURCE,
            )
        )
        sheet = holds_top(
            loss_watts, top, eta, f"{COMBUSTION_SOURCE}: {fuel}, {air}", burning.count,
            burning.each, burning.source, temp_unit, elements_on_top_w,
        )  # fmt: skip
        sheet.agrees("P", Q_(draw, "BTU/hr"))
        check = sheet.check()
        kept = eta * draw
        lost = si(Q_(loss_watts, "W"), "BTU/hr")
        elements = (
            si(Q_(elements_on_top_w, "W"), "BTU/hr") if elements_on_top_w is not None else None
        )
        working.append(
            Step(
                name="Burners against the heat lost at the top"
                if elements is None
                else "Burners and elements against the heat lost at the top",
                value=(
                    f"{kept:,.0f} BTU/hr kept against {lost:,.0f} BTU/hr lost"
                    if elements is None
                    else f"{kept:,.0f} + {elements:,.0f} BTU/hr kept against {lost:,.0f} BTU/hr "
                    "lost"
                ),
                formula="η × burner input at full fire ≥ steady heat loss"
                if elements is None
                else "η × burner input at full fire + element power ≥ steady heat loss",
                reference=sheet.reference,
            )
        )
        if check.status != "pass":
            findings.append(
                Finding.failed(
                    check,
                    message=(
                        f"At full fire the burners leave {kept:,.0f} BTU/hr in the kiln at "
                        f"{show(top, temp_unit)} (only {eta:.0%} of their {draw:,.0f} BTU/hr: the "
                        "rest leaves with the flue gas)"
                        + (
                            ""
                            if elements is None
                            else f", and the elements on to the top add {elements:,.0f} BTU/hr"
                        )
                        + f", less than the {lost:,.0f} BTU/hr the lining loses there. "
                        "The kiln can't reach its top temperature. Add burners or insulation."
                    ),
                )
            )

    # The supply
    cases: list[SupplyCase] = []
    tank: str | None = None
    if on_line:
        assert isinstance(gas.supply, Line)
        working.append(
            Step(
                name=f"Supply: a {fuel} line",
                value=_pressure_text(si(gas.supply.pressure, "psi")),
                note="A line's capacity is the meter's and the pipe's; nothing is vaporized.",
            )
        )
    else:
        # With no burners chosen there is no draw: the supply is checked against the design input
        load = draw if burning.count > 0 else demand
        cases, liquid_gal = _supply_cases(gas, load, t_f)
        _check_supply(gas, need, burning, demand, cases, t_f, t_cold, temp_unit, working, findings)
        hours = liquid_gal / (draw / PROPANE_BTU_PER_GAL) if draw > 0 else math.inf
        working.append(
            Step(
                name="Propane on hand",
                value=f"{liquid_gal:.0f} gal: {hours:.1f} hours at full fire",
                formula=(
                    "cylinders × 100 lb ÷ 4.20 lb/gal"
                    if isinstance(gas.supply, Cylinders)
                    else "⅓ of the tank"
                ),
            )
        )  # fmt: skip
        tank = tank_suggestion(draw, t_f)

    if gas.burners.type == "power":
        findings.append(
            Finding(
                level="info",
                message="Power burners need electricity: a power cut stops the firing.",
                reference="combustion-and-masonry.md §3.3 [S26]",
            )
        )

    # The flue
    chamber_ft3 = chamber_shape(kiln).volume / si(Q_(1, "ft**3"), "m**3")
    port = burner_port(gas, chosen)
    inlet = port_area_in2(port) * burning.count if port is not None and burning.count else None
    updraft = kiln.draft is not None and kiln.draft.type == "up"
    flue_in2, how_flue = starting_flue(inlet, draw, chamber_ft3, updraft)
    working.append(
        Step(
            name="Exit flue, to start",
            value=f"{flue_in2:.0f} in²",
            formula=how_flue,
            inputs={
                **({"burner ports together": f"{inlet:.0f} in²"} if inlet is not None else {}),
                "Olsen's other methods": (
                    f"{FLUE_PER_FT3 * chamber_ft3:.0f} in² (2½ in² per ft³), "
                    f"{draw / FLUE_PER_BTU:.0f} in² (1 in² per 7000 BTU/hr)"
                ),
            },
            reference=FLUE_SOURCE,
            note=(
                "Build it this size and brick it down to tune the kiln: it is much easier to "
                "restrict than to enlarge (p.151, p.236). Size the damper to close it fully."
            ),
        )
    )

    # The chimney: gas under pressure needs it only to the top of the kiln, then a hood and stack
    chimney: str | None = None
    chimney_in: float | None = None
    draft: list[str] = []
    if kiln.draft is not None and kiln.draft.type in ("cross", "down"):
        least = kiln_top_in(kiln)
        built = kiln.draft.chimney
        chimney_in = si(built.height, "in") if built is not None else least
        chimney = f"{chimney_in / 12:.1f} ft ({chimney_in:.0f} in) above the chamber floor"
        working.append(
            Step(
                name="Chimney height",
                value=chimney,
                formula="at least the kiln's top, outside; a hood and stack take the gases on",
                inputs={
                    "the kiln's top": f"{least:.1f} in",
                    **({"as built": f"{chimney_in:.1f} in"} if built is not None else {}),
                },
                reference=CHIMNEY_SOURCE,
                note=(
                    "With burners under gas pressure (or a blower) the gas drives the flow; the "
                    "chimney and stack only need to carry the gases out above where people are."
                    + (
                        " The kiln burns a fire too, and the chimney must draw it: the one drawn "
                        "is the fire's (Olsen p.79)."
                        if kiln.heat.fire is not None
                        else ""
                    )
                ),
            )
        )
        sheet = chimney_height(least, chimney_in, built is not None, CHIMNEY_SOURCE)
        if (check := sheet.check()).status != "pass":
            findings.append(
                Finding.failed(
                    check,
                    message=(
                        f"The chimney stops {least - chimney_in:.1f} in below the top of the "
                        "kiln. With gas burners Olsen takes it at least to the kiln's top or its "
                        "frame, with a hood and stack above, so the gases don't spill out where "
                        "people work."
                    ),
                )
            )
        draft = _draft_lines(kiln, chimney_in, top, working, temp_unit)
    findings.append(
        Finding(
            level="info",
            message=(
                "Above the kiln a ventilation hood and stack carry the flue gases out of the "
                "building, above where people are (Olsen p.151)."
            ),
            reference=CHIMNEY_SOURCE,
        )
    )
    findings.append(Finding(level="info", message=GAS_SAFETY))
    return GasDesign(
        fuel=fuel,
        construction=WALL_WORDS[construction],
        ward_volume=f"{volume_ft3:.1f} ft³",
        demand_range=f"{low * volume_ft3:,.0f}–{high * volume_ft3:,.0f} BTU/hr",
        design_input=f"{demand:,.0f} BTU/hr",
        design_input_btu_hr=demand,
        full_fire_btu_hr=draw,
        propane_at_full_fire=at_full,
        burners=chosen,
        burner_options=burning.options[:8],
        supply_temperature=show(t_cold, temp_unit),
        supply=cases,
        tank_suggestion=tank,
        chimney_height=chimney,
        chimney_height_in=chimney_in,
        flue_area=f"{flue_in2:.0f} in²",
        flue_area_in2=flue_in2,
        inlet_area_in2=inlet,
        draft=draft,
        working=working,
        findings=findings,
    )


def _check_supply(
    gas: Gas,
    need: Demand,
    burning: Burning,
    demand: float,
    cases: list[SupplyCase],
    t_f: float,
    t_cold: Quantity,
    temp_unit: str,
    working: list[Step],
    findings: list[Finding],
) -> None:
    """Propane cylinders or a tank against what the burners draw, at the coldest air; with no
    burners chosen, against the design input (the sheet's P = D)."""
    draw = burning.draw if burning.count > 0 else demand
    for case in cases:
        working.append(
            Step(
                name=f"Supply: {case.case}",
                value=case.capacity,
                inputs={"air temperature": show(t_cold, temp_unit)},
                reference=case.source,
                note="meets the burners' draw"
                if case.meets_demand
                else "short of the burners' draw",
            )
        )
    worst = cases[-1]
    used = (
        Draw()
        if abs(draw - demand) <= 1e-9 * demand or burning.count == 0
        else Draw(burning.count, burning.each, burning.source)
    )
    full = supply("gas.supply-full", need, used, _supply(gas, t_f, conservative=False), "error")
    full.agrees("P", Q_(draw, "BTU/hr"))
    full.agrees("C", Q_(cases[0].capacity_btu_hr, "BTU/hr"))
    if (check := full.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"Even full, the propane supply gives only {cases[0].capacity} at "
                    f"{show(t_cold, temp_unit)}, short of the {draw:,.0f} BTU/hr the burners "
                    "draw. The kiln would stall before the top."
                ),
            )
        )
        if gas.firing_speed == "fast" and gas.burners.rating is None:
            findings.append(
                Finding(
                    level="info",
                    message=(
                        "Set firing_speed: slow to size the burners by Olsen's Rule 1, the low end "
                        "of Ward's range: they draw less, and the kiln fires more slowly."
                    ),
                    reference=OLSEN_INPUT,
                )
            )
    elif isinstance(gas.supply, Cylinders):  # a tank has no case below ⅓ full
        quarter = supply(
            "gas.supply-low", need, used, _supply(gas, t_f, conservative=True), "warning"
        )
        quarter.agrees("C", Q_(worst.capacity_btu_hr, "BTU/hr"))
        if (check := quarter.check()).status != "pass":
            findings.append(
                Finding.failed(
                    check,
                    message=(
                        f"The propane supply meets the {draw:,.0f} BTU/hr the burners draw when "
                        f"full but not in the conservative case ({worst.case}: {worst.capacity}) "
                        f"at {show(t_cold, temp_unit)}. Expect the kiln to slow near the top as "
                        "the cylinders cool and empty. Use more cylinders or a tank."
                    ),
                )
            )
    if isinstance(gas.supply, Cylinders) and gas.supply.count > 1:
        findings.append(
            Finding(
                level="info",
                message=(
                    "Cylinders joined in parallel are assumed to add their capacities. That is a "
                    "reasonable inference at the same temperature and fill, but no source states "
                    "it. Never warm a cylinder with a flame or heater."
                ),
                reference="combustion-and-masonry.md §2.6 [S23, S24]",
            )
        )
