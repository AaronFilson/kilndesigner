"""Gas firing: burner input, burner choice, the propane supply, and the chimney.

- **Burner input** comes from Ward Burner Systems' BTU per cubic foot per hour, by wall
  construction and cone. The high end of Ward's range gives about a 6–7 hour firing.
- **Burners** are chosen from Ward's published ratings by supply pressure.
- **The propane supply** is checked against cylinder and tank vaporization tables at the
  coldest air the kiln will be fired in. A cylinder can only boil off so much gas; as it cools
  and empties, the burners starve and the kiln stalls near the top.
- **The chimney** follows Olsen's and Ward's rule (3 × the inside height + ⅓ of the horizontal
  run), with the stack draft from the stack-effect equation.

Data: data/gas.yaml, from docs/research/combustion-and-masonry.md.
"""

from __future__ import annotations

import math
from functools import cache
from importlib import resources
from typing import Any, Literal

import numpy as np
import yaml
from pydantic import BaseModel, ConfigDict

from kilndesigner.cones import cone_temperature, hotter_than
from kilndesigner.heatloss import top_temperature
from kilndesigner.model import CatenaryArch, Cylinders, Dome, Gas, Kiln, SprungArch, Tank
from kilndesigner.shape import chamber_shape
from kilndesigner.units import Q_, Quantity, si
from kilndesigner.working import Finding, Step, show

PROPANE_BTU_PER_GAL = 91_502  # HHV at 60 °F [S1, S2]
PROPANE_LB_PER_GAL = 4.20  # [S1, S2]
STACK_C = 0.0342  # K/m, stack-effect equation [S42]
ATMOSPHERE = 101_325.0  # Pa
PA_PER_IN_WC = 249.09
CHIMNEY_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.80 (Principle 5), and Ward, 'Draft and Its Importance': "
    "3 × inside height + ⅓ of the horizontal run; olsen-kiln-book.md; "
    "combustion-and-masonry.md §4.1 [S32, S37]"
)
FLUE_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.236: 2.5 in² per ft³ (one of his three methods); "
    "olsen-kiln-book.md; combustion-and-masonry.md §4.1 [S38, S39]"
)
# The research covers US studio gas kilns of about 10 to 60 ft³ (kiln-hardware.md, its scope):
# past that the burner counts, flue and chimney aren't sourced
LARGEST_FT3 = 60.0
DRAFT_SOURCE = "Stack effect, ΔP = 0.0342·a·h·(1/To − 1/Ti); combustion-and-masonry.md §4.2 [S42]"
GAS_SAFETY = (
    "Gas piping, regulators, safety valves and the installation must be done or checked by a "
    "licensed gas fitter to your local code (NFPA 54 and 58 in the US)."
)

type WallClass = Literal["hard_brick", "insulating_brick", "ceramic_fibre"]
WALL_WORDS = {
    "hard_brick": "9 in hard brick",
    "insulating_brick": "9 in insulating brick",
    "ceramic_fibre": "6 in ceramic fibre",
}


@cache
def gas_data() -> dict[str, Any]:
    text = resources.files("kilndesigner.data").joinpath("gas.yaml").read_text(encoding="utf-8")
    data: dict[str, Any] = yaml.safe_load(text)
    return data


def wall_class(kiln: Kiln) -> WallClass:
    """Ward's construction class from the walls' hot face."""
    from kilndesigner.castable import resolve_material

    kind = resolve_material(kiln, kiln.lining.walls[0].material).kind
    if kind in ("dense_firebrick", "dense_castable"):
        return "hard_brick"
    if kind in ("fibre_blanket", "fibre_board"):
        return "ceramic_fibre"
    return "insulating_brick"


def ward_volume(kiln: Kiln) -> tuple[float, str]:
    """Ward's chamber volume (m³) and how it was found: a sprung arch counts as ⅔ of its rise, a
    catenary as ⅔ of its base × height (§3.1, [S28]). Ward gives no formula for a dome, so its
    space is worked out exactly."""
    c = kiln.chamber
    w, d, h = si(c.width, "m"), si(c.depth, "m"), si(c.height, "m")
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

    construction: str
    ward_volume: str
    demand_range: str
    design_input: str
    design_input_btu_hr: float
    propane_at_full_fire: str
    burners: BurnerOption | None
    burner_options: list[BurnerOption]
    supply_temperature: str
    supply: list[SupplyCase]
    tank_suggestion: str | None
    chimney_height: str | None
    flue_area: str
    draft: list[str]
    working: list[Step]
    findings: list[Finding]


def _burner_options(
    demand: float, kind: Literal["venturi", "power"], max_psi: float
) -> list[BurnerOption]:
    data = gas_data()
    options: list[BurnerOption] = []
    for count in range(1, 9):
        each = demand / count
        if kind == "venturi":
            for name, spec in data["venturi_burners"]["models"].items():
                # A burner too big for the load at its lowest published pressure isn't listed:
                # at the pressures given it would put in more than the load
                p = venturi_pressure(each, spec)
                if p is None or p > max_psi:
                    continue
                options.append(
                    BurnerOption(
                        model=name, type="venturi", count=count, pressure=_pressure_text(p),
                        each=f"{each:,.0f} BTU/hr", total_cost=count * spec["price"],
                    )
                )  # fmt: skip
        else:
            for name, spec in data["power_burners"]["models"].items():
                if each <= spec["btu_hr"]:
                    options.append(
                        BurnerOption(
                            model=f"Ward {name}", type="power", count=count,
                            pressure="11 in. w.c.", each=f"{each:,.0f} BTU/hr",
                            total_cost=count * spec["price"],
                        )
                    )  # fmt: skip
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
        for label, lb in (("full", 100), ("half full", 50)):
            each = interpolate(t, opt["temps_f"], opt["rows"][lb])
            cases.append(
                SupplyCase(
                    case=f"{n} × 100 lb cylinders, {label}",
                    capacity=f"{n * each:,.0f} BTU/hr ({each:,.0f} each)",
                    capacity_btu_hr=n * each, meets_demand=n * each >= demand,
                    source=opt["source"],
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
        liquid_gal = n * 100 / PROPANE_LB_PER_GAL
    else:
        assert isinstance(supply, Tank)
        table = data["tanks_one_third_full"]
        cap = interpolate(t, table["temps_f"], table["gallons"][supply.gallons])
        cases.append(
            SupplyCase(
                case=f"{supply.gallons} gal tank, ⅓ full",
                capacity=f"{cap:,.0f} BTU/hr",
                capacity_btu_hr=cap, meets_demand=cap >= demand, source=table["source"],
            )
        )  # fmt: skip
        liquid_gal = supply.gallons / 3
    return cases, liquid_gal


def _tank_suggestion(demand: float, t_f: float) -> str | None:
    table = gas_data()["tanks_one_third_full"]
    t = min(max(t_f, 0.0), 70.0)
    for gallons, row in table["gallons"].items():
        if interpolate(t, table["temps_f"], row) >= demand:
            return (
                f"A {gallons} gal tank, kept at least ⅓ full, supplies "
                f"{interpolate(t, table['temps_f'], row):,.0f} BTU/hr at {t_f:.0f} °F"
            )
    return None


def _oversized(gas: Gas, demand: float, max_psi: float) -> tuple[BurnerOption, float] | None:
    """The burners the design names, when each is bigger than its share of the load even at the
    lowest pressure its ratings are published for on one orifice: at that pressure, and what
    they draw there. None if the design doesn't name both a venturi model and a count."""
    asked = gas.burners
    count = asked.wanted
    spec = gas_data()["venturi_burners"]["models"].get(asked.model or "")
    if asked.type != "venturi" or spec is None or count is None:
        return None
    psi, ratings = _on_one_orifice(spec)
    if demand / count >= ratings[0] or psi[0] > max_psi:
        return None
    option = BurnerOption(
        model=asked.model or "", type="venturi", count=count, pressure=_pressure_text(psi[0]),
        each=f"{ratings[0]:,.0f} BTU/hr", total_cost=count * spec["price"],
    )  # fmt: skip
    return option, count * ratings[0]


def _choose_burners(
    gas: Gas, demand: float, t_f: float, working: list[Step], findings: list[Finding]
) -> tuple[BurnerOption | None, float, list[BurnerOption]]:
    """The burners, what they draw (BTU/hr), and the other sets that would do."""
    data = gas_data()
    vapour = data["vapour_pressure"]
    tank_psig = interpolate(t_f, vapour["temps_f"], vapour["psig"])
    max_psi = 10.0 if isinstance(gas.supply, Cylinders) else min(20.0, tank_psig - 10.0)
    working.append(
        Step(
            name="Propane pressure available",
            value=f"{tank_psig:.0f} psig in the cylinder or tank at {t_f:.0f} °F",
            inputs={"burners limited to": f"{max_psi:.3g} psi"},
            reference=vapour["source"],
            note=(
                "With cylinders, burners are kept to 10 psi or less so the regulator still works "
                "when the cylinders are cold and low."
            ),
        )
    )
    options = _burner_options(demand, gas.burners.type, max_psi)
    chosen: BurnerOption | None = None
    draw = demand
    wanted = gas.burners.wanted
    source = data["venturi_burners"]["source"]
    if gas.burners.model or wanted:
        matching = [
            o
            for o in options
            if (gas.burners.model is None or o.model.endswith(gas.burners.model))
            and (wanted is None or o.count == wanted)
        ]
        chosen = matching[0] if matching else None
        big = _oversized(gas, demand, max_psi) if chosen is None else None
        if big is not None:
            chosen, draw = big
            findings.append(
                Finding(
                    level="warning",
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
        elif chosen is None:
            findings.append(
                Finding(
                    level="error",
                    message=(
                        "The burners chosen can't deliver the design input within "
                        f"{max_psi:.3g} psi. Choose more or bigger burners."
                    ),
                )
            )
    elif options:
        chosen = options[0]
    else:
        findings.append(
            Finding(
                level="error",
                message=(
                    f"No set of up to 8 {gas.burners.type} burners in the library delivers the "
                    f"{demand:,.0f} BTU/hr design input within {max_psi:.3g} psi, the most this "
                    f"supply allows at {t_f:.0f} °F, so none is chosen."
                ),
                reference=data[f"{gas.burners.type}_burners"]["source"],
            )
        )
    if chosen is not None:
        working.append(
            Step(
                name="Burners",
                value=f"{chosen.count} × {chosen.model} at {chosen.pressure}",
                inputs={"each": chosen.each, "cost": f"${chosen.total_cost:,.2f}"},
                reference=data[f"{chosen.type}_burners"]["source"],
                note=(
                    None
                    if chosen.type != "venturi"
                    else "The pressure at which each gives its share, read from its published "
                    "ratings: between them, output rises with √pressure (§3.2, derived)."
                    if draw == demand
                    else "The lowest pressure its ratings are published for on one orifice; each "
                    "gives more than its share there (§3.2, derived)."
                ),
            )
        )
    return chosen, draw, options


def design_gas(kiln: Kiln) -> GasDesign:
    gas = kiln.heat.gas
    if gas is None:
        raise ValueError("the kiln has no gas heat")
    data = gas_data()
    findings: list[Finding] = []
    working: list[Step] = []
    us = kiln.units == "us"
    temp_unit = "degF" if us else "degC"

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
    if past:
        findings.append(
            Finding(
                level="warning",
                message=(
                    "Ward's burner table stops at cone 10, and this design goes past it "
                    f"({' and '.join(past)}): the burners are sized from the cone {column} "
                    "column and may be short of heat at the top."
                ),
                reference=ward["source"],
            )
        )
    low, high = ward["walls"][construction][ward["columns"].index(column)]
    demand = (high if gas.firing_speed == "fast" else low) * volume_ft3
    other = (low if gas.firing_speed == "fast" else high) * volume_ft3
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
            inputs={"construction": WALL_WORDS[construction], "cone column": column},
            reference=ward["source"],
            note="The high end gives about a 6–7 hour firing, the low end 14–18 hours.",
        ),
        Step(
            name="Design burner input",
            value=f"{demand:,.0f} BTU/hr ({show(Q_(demand, 'BTU/hr'), 'kW')})",
            formula=f"{'high' if gas.firing_speed == 'fast' else 'low'} end × volume",
            inputs={"firing speed": gas.firing_speed},
        ),
    ]
    if kiln.heat.electric is not None:
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
    if t_f < 0:
        findings.append(
            Finding(
                level="error",
                message="The vaporization tables start at 0 °F; colder firing can't be checked.",
            )
        )

    # The burners, and what they draw: the supply must keep up with that
    chamber_ft3 = chamber_shape(kiln).volume / si(Q_(1, "ft**3"), "m**3")
    too_big = chamber_ft3 > LARGEST_FT3
    if too_big:
        findings.append(
            Finding(
                level="error",
                message=(
                    f"At {chamber_ft3:.0f} ft³ this kiln is bigger than the sources here cover, "
                    f"studio gas kilns of up to about {LARGEST_FT3:.0f} ft³, so its burners and "
                    "chimney aren't sized."
                ),
                reference="kiln-hardware.md, its scope",
            )
        )
        chosen, draw, options = None, demand, []
    else:
        chosen, draw, options = _choose_burners(gas, demand, t_f, working, findings)
    gal_hr = draw / PROPANE_BTU_PER_GAL
    working.append(
        Step(
            name="Propane at full fire",
            value=f"{gal_hr:.2f} gal/hr ({gal_hr * PROPANE_LB_PER_GAL:.1f} lb/hr)",
            formula="BTU/hr ÷ 91,502 BTU/gal",
            inputs={} if draw == demand else {"the burners draw": f"{draw:,.0f} BTU/hr"},
            reference="combustion-and-masonry.md §1.1 [S1, S2]",
        )
    )

    # The supply
    cases, liquid_gal = _supply_cases(gas, draw, t_f)
    for case in cases:
        working.append(
            Step(
                name=f"Supply: {case.case}",
                value=case.capacity,
                inputs={"air temperature": show(t_cold, temp_unit)},
                reference=case.source,
                note="meets the design input" if case.meets_demand else "short of the design input",
            )
        )
    worst = cases[-1]
    if not cases[0].meets_demand:
        findings.append(
            Finding(
                level="error",
                message=(
                    f"Even full, the propane supply gives only {cases[0].capacity} at "
                    f"{show(t_cold, temp_unit)}, short of the {draw:,.0f} BTU/hr the burners "
                    "need. The kiln would stall before the top."
                ),
                reference=cases[0].source,
            )
        )
        # Only when the burners can turn down to a slow firing's input
        if gas.firing_speed == "fast" and cases[0].capacity_btu_hr >= other and draw == demand:
            findings.append(
                Finding(
                    level="info",
                    message=(
                        f"Full, this supply could keep up with a slow firing ({other:,.0f} "
                        "BTU/hr, about 14–18 hours) at this temperature. Set firing_speed: slow "
                        "to size for it."
                    ),
                    reference=ward["source"],
                )
            )
    elif not worst.meets_demand:
        need = "design input" if draw == demand else "the burners draw"
        findings.append(
            Finding(
                level="warning",
                message=(
                    f"The propane supply meets the {draw:,.0f} BTU/hr {need} when full "
                    f"but not in the conservative case ({worst.case}: {worst.capacity}) at "
                    f"{show(t_cold, temp_unit)}. Expect the kiln to slow near the top as the "
                    "cylinders cool and empty. Use more cylinders or a tank."
                ),
                reference=worst.source,
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
    hours = liquid_gal / gal_hr
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
    tank = _tank_suggestion(draw, t_f)

    if gas.burners.type == "power":
        findings.append(
            Finding(
                level="info",
                message="Power burners need electricity: a power cut stops the firing.",
                reference="combustion-and-masonry.md §3.3 [S26]",
            )
        )

    # The chimney and flue
    shape = chamber_shape(kiln)
    flue_in2 = 2.5 * shape.volume / si(Q_(1, "ft**3"), "m**3")
    working.append(
        Step(
            name="Exit flue area",
            value=f"{flue_in2:.0f} in²",
            formula="2.5 in² per ft³ of chamber",
            reference=FLUE_SOURCE,
            note=(
                "Ward's alternative: the same area as all the burner ports together. Size the "
                "damper to close it fully."
            ),
        )
    )
    chimney: str | None = None
    draft: list[str] = []
    if kiln.draft is not None and kiln.draft.type in ("cross", "down") and not too_big:
        inside_h = si(kiln.chamber.height, "in")  # a catenary's height is to its crown already
        if isinstance(kiln.roof, SprungArch | Dome):
            inside_h += si(kiln.roof.rise, "in")
        along = (
            si(kiln.chamber.depth, "in")
            if kiln.draft.flue_wall in ("front", "back")
            else si(kiln.chamber.width, "in")
        )
        flue_wall = sum(si(x.thickness, "in") for x in kiln.lining.for_face(kiln.draft.flue_wall))
        run = along + flue_wall + si(kiln.draft.run_to_chimney, "in")
        height_in = 3 * inside_h + run / 3
        chimney = f"{height_in / 12:.1f} ft ({height_in:.0f} in) above the chamber floor"
        working.append(
            Step(
                name="Chimney height",
                value=chimney,
                formula="3 × inside height + ⅓ × horizontal run",
                inputs={
                    "inside height": f"{inside_h:.1f} in",
                    "horizontal run": f"{run:.1f} in (chamber, flue wall and run to the chimney)",
                },
                reference=CHIMNEY_SOURCE,
                note=(
                    "With power burners the chimney only needs to clear the building."
                    if gas.burners.type == "power"
                    else None
                ),
            )
        )
        # Warm air gives the least draft, so use the site's air, not the coldest day (codes
        # give no summer design figure: structure-and-draft.md §4).
        to = si(kiln.site.ambient, "K")
        for label, flue in (
            ("flue gas at 1000 °F", Q_(1000, "degF")),
            ("flue gas at top temperature", top),
        ):
            dp = STACK_C * ATMOSPHERE * si(Q_(height_in, "in"), "m") * (1 / to - 1 / si(flue, "K"))
            line = f"{dp / PA_PER_IN_WC:.3f} in. w.c. ({dp:.0f} Pa) with {label}"
            draft.append(line)
            working.append(
                Step(
                    name="Draft at the chimney's base",
                    value=line,
                    inputs={"outside air": show(kiln.site.ambient, temp_unit)},
                    reference=DRAFT_SOURCE,
                )
            )  # fmt: skip
    findings.append(Finding(level="info", message=GAS_SAFETY))
    return GasDesign(
        construction=WALL_WORDS[construction],
        ward_volume=f"{volume_ft3:.1f} ft³",
        demand_range=f"{low * volume_ft3:,.0f}–{high * volume_ft3:,.0f} BTU/hr",
        design_input=f"{demand:,.0f} BTU/hr",
        design_input_btu_hr=demand,
        propane_at_full_fire=f"{gal_hr:.2f} gal/hr",
        burners=chosen,
        burner_options=options[:8],
        supply_temperature=show(t_cold, temp_unit),
        supply=cases,
        tank_suggestion=tank,
        chimney_height=chimney,
        flue_area=f"{flue_in2:.0f} in²",
        draft=draft,
        working=working,
        findings=findings,
    )
