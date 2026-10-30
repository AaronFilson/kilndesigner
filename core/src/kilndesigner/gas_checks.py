"""Gas firing's checks as sheets (ADR 0013): the burners against their published ratings, the
propane supply against the vaporization tables, the range of Ward's burner table, the kiln's size,
and a hybrid's elements against reduction.

Where the engine reads a table (Ward's BTU per ft³, a burner's ratings, a cylinder's or a tank's
vaporization, propane's vapour pressure), the sheet shows the two nearest rows as inputs and the
straight line between them as a formula, so the number can be followed back to the table and
moved along it. :mod:`kilndesigner.gas` computes the same numbers its own way; each sheet must
agree with them (``Sheet.agrees``).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

import numpy as np

from kilndesigner.sheet import Level, Sheet
from kilndesigner.units import Q_, Quantity

DESIGN = "the design"
LINEAR = "a straight line between the table's two nearest rows"
ROOT_P = (
    "on one orifice a venturi burner's output grows with √pressure: a straight line in √p "
    "between its two nearest published ratings; combustion-and-masonry.md §3.2 (derived)"
)
REGULATOR = (
    "RegO 597F series data sheet: capacity rated with the inlet 20 psig above the set pressure "
    "and delivery 20 % below it; combustion-and-masonry.md §2.8 [S89]"
)
LIQUID_COOLING_F = 20.0
"""How much colder than the air the liquid propane runs under continuous draw: the D × L × K
rule's basis (combustion-and-masonry.md §2.3 [S1], §2.8)."""
COOLING = "the liquid 20 °F under the air under draw; combustion-and-masonry.md §2.3 [S1], §2.8"
REGULATOR_INLET_PSI = 20.0  # RegO 597F: inlet 20 psig over the set pressure
REGULATOR_DROOP = 0.8  # RegO 597F: delivery 20 % below the set pressure at rated capacity
TANK_PSI = "to the 20 psi the burners' ratings go to; combustion-and-masonry.md §3.2"
TANK_TABLE_FILL = 73.3 / 90
"""The ⅓-full tank table is D × L × 90, the 50 %-full K; ⅓ full is K ≈ 73.3
(combustion-and-masonry.md §2.3, §2.8, derived)."""
ALTITUDE = (
    "Olsen, 4th ed. p.230–232: burner output × 0.9279 at 5000 ft, × 0.8579 at 10,000 ft, which "
    "√σ of the U.S. Standard Atmosphere reproduces to 0.2 % (derived)"
)
TOP_SOURCE = (
    "energy balance at the top temperature: the burners' available heat (Cantera, "
    "combustion.py) against the lining's steady loss (heatloss.py)"
)
MOST_BURNERS = 40
"""The most burners the engine will put on one kiln: Kaneko's 500 ft³ updraft has 32 (Olsen, 4th
ed. p.171–172)."""


def lookup(
    s: Sheet,
    y: str,
    meaning: str,
    x: str,
    table: tuple[list[float], list[float]],
    units: tuple[str, str],
    source: str,
) -> None:
    """The cell ``y`` read from a table at the cell ``x``, as the engine reads it (``np.interp``):
    held within the table's ends, then a straight line between the two nearest rows."""
    xs, ys = table
    x_unit, y_unit = units
    value = float(s.dims[x].to(x_unit).magnitude)
    arg = x
    if not xs[0] <= value <= xs[-1]:
        s.given(f"{x}_first", "the table's first row", Q_(xs[0], x_unit), source=source)
        s.given(f"{x}_last", "the table's last row", Q_(xs[-1], x_unit), source=source)
        s.let(f"{x}_c", "held within the table", f"min(max({x}, {x}_first), {x}_last)", x_unit)
        arg, value = f"{x}_c", min(max(value, xs[0]), xs[-1])
    i = min(max(int(np.searchsorted(xs, value, side="right")) - 1, 0), len(xs) - 2)
    for k, j in (("₁", i), ("₂", i + 1)):
        s.given(f"{x}{k}", "the table's row", Q_(xs[j], x_unit), source=source)
        s.given(f"{y}{k}", f"{meaning} in that row", Q_(ys[j], y_unit), source=source)
    s.let(y, meaning, f"{y}₁ + ({y}₂ - {y}₁)*({arg} - {x}₁)/({x}₂ - {x}₁)", y_unit, source=LINEAR)


@dataclass(frozen=True)
class Demand:
    """What sets the design burner input: Ward's chamber volume and his BTU per ft³ per hour."""

    roof: Literal["flat", "sprung_arch", "catenary", "dome", "round"]  # round: a round chamber
    width: float  # in
    depth: float  # in, front to back: every chamber in a row
    height: float  # in: to the springline, or a catenary's crown
    rise: float  # in, a sprung arch's
    dome_ft3: float  # Ward's volume, ft³; a dome's or a round chamber's worked out exactly
    btu_per_ft3_hr: float
    what: str  # "9 in insulating brick, cone 10, the fast (high) end"
    source: str


def demand(s: Sheet, d: Demand) -> None:
    """V, Ward's volume, and D = b·V, the design burner input."""
    if d.roof in ("dome", "round"):
        s.given(
            "V",
            "chamber volume, Ward's way",
            Q_(d.dome_ft3, "ft**3"),
            source=f"worked out exactly: Ward gives no formula for a {d.roof} kiln",
        )
    else:
        s.given("W", "chamber width", Q_(d.width, "in"), source=DESIGN)
        s.given("L", "chamber depth", Q_(d.depth, "in"), source=DESIGN)
        to = "to the crown" if d.roof == "catenary" else "to the springline"
        s.given("H", f"chamber height, {to}", Q_(d.height, "in"), source=DESIGN)
        formula = {"flat": "W*L*H", "catenary": "L*4/3*H*W/2", "sprung_arch": "W*L*(H + 2/3*h_r)"}
        if d.roof == "sprung_arch":
            s.given("h_r", "the arch's rise", Q_(d.rise, "in"), source=DESIGN)
        s.let(
            "V",
            "chamber volume, Ward's way",
            formula[d.roof],
            "ft**3",
            source=f"{d.source}: a sprung arch adds ⅔ of its rise; a catenary is ⅔ of its "
            "base × height",
        )
    s.given(
        "b",
        f"Ward's burner input per ft³: {d.what}",
        Q_(d.btu_per_ft3_hr, "BTU/ft**3/hr"),
        source=f"{d.source} (table)",
    )
    s.let("D", "design burner input", "b*V", "BTU/hr")


def pressure_ceiling(vapour_psig: float) -> float:
    """The most pressure the burners are sure of from cylinders or a tank whose liquid has
    ``vapour_psig``: the regulator set 20 psi under it, no more than the ratings' 20 psi, and 20 %
    of droop at full flow (RegO 597F). Zero or less: the regulator can't work at all."""
    return REGULATOR_DROOP * min(20.0, vapour_psig - REGULATOR_INLET_PSI)


@dataclass(frozen=True)
class Pressure:
    """The most pressure the burners may run at from cylinders or a tank: the regulator set 20 psi
    under propane's vapour pressure with the liquid 20 °F under the coldest air, no more than
    20 psi, less 20 % droop (RegO 597F); on a line, the line's."""

    tank: bool
    air_f: float
    vapour: tuple[list[float], list[float]]  # °F, psig
    vapour_source: str
    line_psi: float | None = None  # a line's pressure, psi


def _pressure(s: Sheet, p: Pressure) -> None:
    if p.line_psi is not None:
        s.given(
            "p_max",
            "the line's pressure at the burners",
            Q_(p.line_psi, "psi"),
            "psi" if p.line_psi >= 1 else "inch_H2O",
            source=f"{DESIGN}: supply.pressure",
        )
        return
    s.given("t", "the coldest air it fires in", Q_(p.air_f, "degF"), source=DESIGN)
    s.given(
        "Δt_l",
        "the liquid's cooling under draw",
        Q_(LIQUID_COOLING_F, "delta_degF"),
        source=COOLING,
    )
    s.let("t_l", "the liquid's temperature", "t - Δt_l", "degF", source=COOLING)
    lookup(
        s,
        "p_v",
        "propane's vapour pressure (gauge)",
        "t_l",
        p.vapour,
        ("degF", "psi"),
        p.vapour_source,
    )
    s.given("p_top", "the highest pressure the ratings go to", Q_(20, "psi"), source=TANK_PSI)
    s.given(
        "p_reg",
        "the regulator's inlet over its set pressure",
        Q_(REGULATOR_INLET_PSI, "psi"),
        source=REGULATOR,
    )
    s.given("f_d", "delivery at full flow, as a share of set", REGULATOR_DROOP, source=REGULATOR)
    s.let(
        "p_max",
        "the most pressure the burners are sure of",
        "f_d*min(p_top, p_v - p_reg)",
        "psi",
        source=REGULATOR,
    )


@dataclass(frozen=True)
class Ratings:
    """A burner's published ratings: a venturi's on one orifice by pressure (psi), or one rating
    (``btu_hr[0]``): a power burner's, or a burner's at a line's fixed pressure (``rated``)."""

    model: str
    kind: Literal["venturi", "power", "rated"]
    psi: tuple[float, ...]
    btu_hr: tuple[float, ...]
    source: str
    altitude: float = 1.0  # output at the site's elevation, as a share of sea level


def burner_capacity(r: Ratings, max_psi: float) -> float:
    """What one burner gives at the most pressure allowed, at the site, as the sheet works it
    out."""
    if r.kind != "venturi":
        return r.btu_hr[0] * r.altitude
    roots = [math.sqrt(p) for p in r.psi]
    return float(np.interp(math.sqrt(max_psi), roots, r.btu_hr)) * r.altitude


def burners(d: Demand, count: int, why: str, r: Ratings, p: Pressure, low: Level) -> Sheet:
    """The burners' share of the input against what one gives: no more than its rating at the
    most pressure allowed, and (a venturi) no less than its lowest published rating."""
    s = Sheet("gas.burners", f"{count} × {r.model} against the design input", reference=r.source)
    demand(s, d)
    s.given("n", "burners", count, source=why)
    s.let("q", "each burner's share", "D/n", "BTU/hr")
    sea = "r_sea" if r.altitude != 1 else "r_cap"
    if r.kind != "venturi":
        what = (
            f"one {r.model}'s rating, at 11 in. w.c."
            if r.kind == "power"
            else f"one {r.model}'s rating at the line's pressure"
        )
        s.given(sea, what, Q_(r.btu_hr[0], "BTU/hr"), source=r.source)
        if r.altitude != 1:
            _altitude(s, r.altitude)
            s.let("r_cap", "one burner at the site", "r_sea*f_alt", "BTU/hr", source=ALTITUDE)
    else:
        _pressure(s, p)
        s.given(
            "p_0",
            "the lowest pressure published on this orifice",
            Q_(r.psi[0], "psi"),
            source=r.source,
        )
        s.given("r_0", "its rating there", Q_(r.btu_hr[0], "BTU/hr"), source=r.source)
        at = min(float(s.dims["p_max"].to("psi").magnitude), r.psi[-1])
        i = min(max(int(np.searchsorted(r.psi, at, side="right")) - 1, 0), len(r.psi) - 2)
        lo = ("p_0", "r_0")
        if i > 0:
            s.given("p₁", "a published pressure", Q_(r.psi[i], "psi"), source=r.source)
            s.given("r₁", "its rating", Q_(r.btu_hr[i], "BTU/hr"), source=r.source)
            lo = ("p₁", "r₁")
        s.given("p₂", "the next published pressure", Q_(r.psi[i + 1], "psi"), source=r.source)
        s.given("r₂", "its rating", Q_(r.btu_hr[i + 1], "BTU/hr"), source=r.source)
        (pl, rl) = lo
        s.let(
            sea,
            "one burner at the most pressure allowed",
            f"{rl} + (r₂ - {rl})*(sqrt(min(p_max, p₂)) - sqrt({pl}))/(sqrt(p₂) - sqrt({pl}))",
            "BTU/hr",
            source=ROOT_P,
        )
        s.require("p_0", "<=", "p_max")
        low_cell = "r_0"
        if r.altitude != 1:
            _altitude(s, r.altitude)
            s.let("r_cap", "one burner at the site", "r_sea*f_alt", "BTU/hr", source=ALTITUDE)
            s.let("r_low", "its lowest rating, at the site", "r_0*f_alt", "BTU/hr", source=ALTITUDE)
            low_cell = "r_low"
        s.require("q", ">=", low_cell, level=low)
    s.require("q", "<=", "r_cap")
    # The counts that pass lie between D/r_cap and D/r_0: solve within that window, as the one
    # change the solver looks for lies at its nearer end
    total, cap = s.env["D"], s.env["r_cap"]
    fewest = total / cap if cap > 0 else math.inf
    most = total / (s.env["r_0"] * r.altitude) if r.kind == "venturi" else float(MOST_BURNERS)
    if fewest <= min(most, MOST_BURNERS) and most >= 1:
        s.lever("n", max(fewest, 1), min(most, MOST_BURNERS), step=1)
    else:
        s.lever("n", 1, MOST_BURNERS, step=1)
    return s


def _altitude(s: Sheet, factor: float) -> None:
    s.given(
        "f_alt",
        "a burner's output at the site's elevation, as a share of sea level",
        factor,
        source=f"{ALTITUDE}: √σ, σ the standard atmosphere's air density over sea level's",
    )


def holds_top(
    loss_w: float,
    top: Quantity,
    eta: float,
    eta_source: str,
    count: int,
    each_btu_hr: float,
    each_source: str,
    temp_unit: str,
) -> Sheet:
    """The burners at full fire against the heat the kiln loses at its top temperature: only the
    heat that doesn't leave up the flue (the available heat) counts. Below this the kiln can never
    reach the top, whatever the firing time."""
    s = Sheet("gas.top", "The burners can hold the top temperature", reference=TOP_SOURCE)
    s.given("T_top", "the top temperature", top, temp_unit, source="the design: the firing")
    s.given(
        "Q",
        "heat lost through the lining, held at T_top",
        Q_(loss_w, "W"),
        "BTU/hr",
        source="working: Total heat loss at top temperature (the wall solve, iterated)",
    )
    s.given("n", "burners", count, source=DESIGN)
    s.given(
        "r", "each burner at full fire, at the site", Q_(each_btu_hr, "BTU/hr"), source=each_source
    )
    s.let("P", "the burners' input at full fire", "n*r", "BTU/hr")
    s.given(
        "η",
        "available heat: the share of the gas's heat left in the kiln, the flue gas leaving at "
        "T_top",
        eta,
        source=eta_source,
    )
    s.let("P_k", "heat the burners leave in the kiln", "η*P", "BTU/hr")
    s.require("P_k", ">=", "Q")
    s.lever("n", 1, 4 * MOST_BURNERS, step=1)
    return s


def unknown_burner(model: str, kind: str, known: list[str], source: str) -> Sheet:
    s = Sheet("gas.burner-model", "The burner the design names", reference=source)
    s.fact("the design's burner", f"{model} ({kind})", source=DESIGN)
    s.fact(f"{kind} burners with published ratings", ", ".join(known), source=source)
    s.rule("The burners must be ones whose ratings the library has.", holds=False)
    return s


@dataclass(frozen=True)
class Draw:
    """What the burners draw at full fire: the design input, or more when each is too big for
    its share even at its lowest published pressure."""

    count: int | None = None  # set when they draw more than the input
    each: float = 0.0  # BTU/hr, each at its lowest published pressure
    source: str = ""


def _draw(s: Sheet, d: Demand, draw: Draw) -> None:
    demand(s, d)
    if draw.count is None:
        s.let("P", "what the burners draw at full fire", "D", "BTU/hr")
        return
    s.given("n_b", "burners", draw.count, source=DESIGN)
    s.given(
        "r_0", "each, at its lowest published pressure", Q_(draw.each, "BTU/hr"), source=draw.source
    )
    s.let("P", "what the burners draw at full fire", "n_b*r_0", "BTU/hr")


@dataclass(frozen=True)
class Supply:
    """A propane supply read from a vaporization table at the coldest air."""

    case: str  # "4 × 100 lb cylinders, full"
    cylinders: int | None  # None for a tank
    air_f: float
    table: tuple[list[float], list[float]]  # °F, BTU/hr for one cylinder or the tank
    source: str
    by_liquid: bool = False  # the table is by the liquid's temperature, not the air's
    fill: float = 1.0  # the table scaled to the fill it's labelled with (the ⅓-full tank table)


def supply(id: str, d: Demand, draw: Draw, sup: Supply, level: Level) -> Sheet:
    s = Sheet(id, f"Propane supply: {sup.case}", reference=sup.source)
    _draw(s, d, draw)
    s.given("t", "the coldest air it fires in", Q_(sup.air_f, "degF"), source=DESIGN)
    at = "t"
    if sup.by_liquid:
        s.given(
            "Δt_l",
            "the liquid's cooling under draw",
            Q_(LIQUID_COOLING_F, "delta_degF"),
            source=COOLING,
        )
        s.let("t_l", "the liquid's temperature, which the table is read by", "t - Δt_l", "degF")
        at = "t_l"
    one = "one cylinder" if sup.cylinders is not None else "the tank"
    if sup.fill != 1.0:
        lookup(s, "c_50", "the table's figure (D × L × 90)", at, sup.table, ("degF", "BTU/hr"),
               sup.source)  # fmt: skip
        s.given(
            "f_fill",
            "K at ⅓ full over the table's K of 90",
            sup.fill,
            source="combustion-and-masonry.md §2.3, §2.8: K 73.3 at ⅓ full (derived)",
        )
        s.let("c", f"what {one} vaporizes", "c_50*f_fill", "BTU/hr")
    else:
        lookup(s, "c", f"what {one} vaporizes", at, sup.table, ("degF", "BTU/hr"), sup.source)
    if sup.cylinders is None:
        s.let("C", "what the supply gives", "c", "BTU/hr")
    else:
        s.given("n", "cylinders, joined in parallel", sup.cylinders, source=DESIGN)
        s.let(
            "C",
            "what the supply gives",
            "n*c",
            "BTU/hr",
            source="cylinders in parallel add (combustion-and-masonry.md §2.6, inferred)",
        )
        s.lever("n", 1, 40, step=1)
    s.require("C", ">=", "P", level=level)
    return s


def coldest_air(air_f: float, first_f: float, source: str) -> Sheet:
    s = Sheet(
        "gas.coldest-air", "The coldest air against the vaporization tables", reference=source
    )
    s.given("t", "the coldest air it fires in", Q_(air_f, "degF"), source=DESIGN)
    s.given("t_first", "the tables' coldest row", Q_(first_f, "degF"), source=source)
    s.require("t", ">=", "t_first")
    s.lever("t", Q_(-60, "degF"), Q_(120, "degF"))
    return s


def chimney_height(least: float, built: float, given: bool, source: str) -> Sheet:
    """A gas kiln's chimney against the least Olsen takes it to: the kiln's top (in)."""
    s = Sheet("gas.chimney", "The chimney reaches the top of the kiln", reference=source)
    s.given(
        "H_k",
        "the kiln's top, outside, above the chamber floor",
        Q_(least, "in"),
        source="the design: the chamber, the roof's rise and the roof's layers",
    )
    s.given(
        "H",
        "the chimney's top above the chamber floor",
        Q_(built, "in"),
        source=f"{DESIGN}: draft.chimney.height" if given else "the engine: the kiln's top",
    )
    s.require("H", ">=", "H_k", level="warning")
    s.lever("H", Q_(1, "in"), Q_(max(4 * least, 120), "in"))
    return s


def ward_range(
    top: Quantity, given: bool, cone: str | None, past_cone: bool, cone_10: Quantity, source: str
) -> Sheet:
    """Ward's table has columns for cones 06, 6 and 10: a design hotter than cone 10, by its
    temperature or its cone, is sized from the cone 10 column."""
    s = Sheet("gas.ward-range", "The firing against Ward's burner table", reference=source)
    s.given(
        "T_top",
        "the design's top temperature",
        top,
        source=DESIGN if given else "Orton, the design's cone at its final rate",
    )
    s.given(
        "T_10",
        "cone 10, Ward's hottest column (Orton, 60 °C/h)",
        cone_10,
        source="Orton cone charts; cones.md",
    )
    if given:
        s.require("T_top", "<=", "T_10", level="warning")
    if cone is not None:
        s.fact("the design's cone", cone, source=DESIGN)
        s.rule(
            "Ward's table has columns for cones 06, 6 and 10 only.",
            holds=not past_cone,
            level="warning",
        )
    if given and cone is None:
        s.lever("T_top", Q_(500, "degC"), Q_(1500, "degC"))
    return s


def elements_in_reduction(
    off: Quantity, start: Quantity, wire: str, wire_max: Quantity, sources: tuple[str, str]
) -> Sheet:
    """A hybrid fired in reduction: the elements off before reduction starts."""
    reduction, wire_source = sources
    s = Sheet("hybrid.reduction", "The elements off before reduction", reference=reduction)
    s.fact("the firing", "reduction", source=DESIGN)
    s.given("T_off", "the elements switch off at", off, source=f"{DESIGN}: off_above")
    s.given("T_red", "reduction starts about", start, source=reduction)
    s.given("T_wire", f"{wire} in CO- and H₂-rich gas, at most", wire_max, source=wire_source)
    s.require("T_off", "<=", "T_red", level="warning")
    s.lever("T_off", Q_(300, "degC"), Q_(1400, "degC"))
    return s


__all__ = [
    "ALTITUDE",
    "MOST_BURNERS",
    "Demand",
    "Draw",
    "Pressure",
    "Ratings",
    "Supply",
    "burner_capacity",
    "burners",
    "chimney_height",
    "coldest_air",
    "demand",
    "elements_in_reduction",
    "holds_top",
    "lookup",
    "supply",
    "ward_range",
]
