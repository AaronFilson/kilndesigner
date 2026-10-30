"""The electric checks as sheets (ADR 0013): the circuit, the breaker, the wire's temperature and
the elements, each written out as formulas a builder can follow, and change in the page.

:mod:`kilndesigner.electric` computes the same numbers its own way; each sheet must agree with
them (``Sheet.agrees``).
"""

from __future__ import annotations

from dataclasses import dataclass

from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_, Quantity

DESIGN = "the design"
NEC_CONTINUOUS = (
    "NEC 210.20(A) continuous loads at 125%, as applied by L&L; electric-and-thermal.md §3 [S25]"
)
THREE_PHASE = "P = √3·V·I on a three-phase line, V·I on one phase"
KANTHAL_DIAMETER = "Kanthal: d³ = 4·ρ_T·P² / (π²·U²·p); electric-and-thermal.md §1.6–1.7 [S13, S16]"
OLSEN_LOAD = (
    "Olsen (The Kiln Book, 4th ed., p.257) gives 6.4–9 W/in² for cone 10 kilns, about half "
    "Krueger's; which to design to is an open question"
)


def _phase(s: Sheet, phase: int) -> None:
    s.given("k_φ", "phase factor", 3**0.5 if phase == 3 else 1.0, source=THREE_PHASE)


def supply_power(
    voltage: float, breaker: float, phase: int, power: float, power_source: str
) -> Sheet:
    """The installed power against what the circuit can supply continuously."""
    s = Sheet("electric.supply", "Installed power against the circuit", reference=NEC_CONTINUOUS)
    s.given("V", "supply voltage", Q_(voltage, "V"), source=f"{DESIGN}: electric supply")
    s.given("I_b", "breaker rating", Q_(breaker, "A"), source=f"{DESIGN}: electric supply")
    s.given(
        "f_c",
        "share of the breaker a continuous load may draw",
        Q_(80, "percent"),
        "percent",
        source=NEC_CONTINUOUS,
    )
    _phase(s, phase)
    s.let("I_c", "continuous current limit", "f_c*I_b", "A", source=NEC_CONTINUOUS)
    s.let("P_s", "power the circuit can supply continuously", "k_φ*V*I_c", "kW")
    s.given("P", "installed power", Q_(power, "W"), "kW", source=power_source)
    s.require("P", "<=", "P_s")
    s.lever("P", Q_(0.1, "kW"), Q_(500, "kW"))
    return s


def breaker_size(
    voltage: float,
    phase: int,
    power: float,
    power_source: str,
    breaker: float,
    largest: float,
    source: str,
) -> Sheet:
    """NEC 422.11(E): the breaker no bigger than 20 A up to 13.3 A, else 150 % of the kiln's
    current or the next standard size up (240.6(A), a table)."""
    s = Sheet("electric.breaker", "The breaker against the kiln's current", reference=source)
    s.given("P", "installed power", Q_(power, "W"), "kW", source=power_source)
    s.given("V", "supply voltage", Q_(voltage, "V"), source=f"{DESIGN}: electric supply")
    _phase(s, phase)
    current = s.let("I", "the kiln's current", "P/(k_φ*V)", "A")
    if current <= 13.3:
        s.given(
            "I_max",
            "largest breaker for a kiln drawing 13.3 A or less",
            Q_(largest, "A"),
            source="NEC 422.11(E)(2); electric-and-thermal.md §3 [S23]",
        )
    else:
        s.given(
            "m",
            "most a breaker may be over the current",
            Q_(150, "percent"),
            "percent",
            source="NEC 422.11(E)(3); electric-and-thermal.md §3 [S23]",
        )
        s.let("I_150", "150 % of the kiln's current", "m*I", "A")
        s.given(
            "I_max",
            "largest breaker allowed: the first standard size at or above I_150",
            Q_(largest, "A"),
            source="NEC 240.6(A) standard sizes, a table; electric-and-thermal.md §3 [S79]",
        )
    s.given("I_b", "breaker rating", Q_(breaker, "A"), source=f"{DESIGN}: electric supply")
    s.require("I_b", "<=", "I_max")
    s.lever("I_b", Q_(15, "A"), Q_(600, "A"))
    return s


def wire_rating(
    alloy: str,
    top: Quantity,
    above: Quantity,
    rating: Quantity,
    source: str,
    temp_unit: str,
) -> Sheet:
    """The wire, taken as hotter than the kiln by an assumed margin, against its rating in air."""
    s = Sheet("electric.wire-temperature", f"{alloy} against its rating in air", reference=source)
    s.given(
        "T_top",
        "the kiln's top temperature",
        top,
        temp_unit,
        source="the firing: its cone and final rate (Orton), or its top temperature",
    )
    s.given(
        "ΔT_w",
        "how much hotter the wire runs than the kiln (an assumption)",
        above,
        f"delta_{temp_unit}",
        source=(
            "Kanthal gives no figure for coils in grooves; its one example is 106 K for rod "
            "elements (electrical-supply.md §5)"
        ),
    )
    s.let("T_w", "the wire's temperature", "T_top + ΔT_w", temp_unit)
    s.given("T_max", f"{alloy}'s highest temperature in air", rating, temp_unit, source=source)
    s.require("T_w", "<=", "T_max", level="warning")
    s.lever("T_top", Q_(500, "degC"), Q_(1800, "degC"))
    return s


def grooves_past_cone_10(
    top: Quantity,
    grooved_max: Quantity,
    cone_10: Quantity,
    cone: str | None,
    past_by_cone: bool,
    temp_unit: str,
) -> Sheet:
    """Coils in grooves past cone 10: Kanthal's limit is lower still, but makers build cone 10
    kilns this way, so only past cone 10 (by temperature or by cone) is a warning."""
    kanthal = "Kanthal key data for elements, spiral in grooves; electric-and-thermal.md §1.6 [S14]"
    s = Sheet("electric.grooves", "Coils in grooves past cone 10", reference=kanthal)
    s.given(
        "T_top",
        "the kiln's top temperature",
        top,
        temp_unit,
        source="the firing: its cone and final rate (Orton), or its top temperature",
    )
    s.given(
        "T_K",
        "Kanthal's highest kiln temperature for coils in grooves",
        grooved_max,
        temp_unit,
        source=kanthal,
    )
    s.given(
        "T_10",
        "cone 10 at 150 °C/h: the hottest kiln makers build coils in grooves for",
        cone_10,
        temp_unit,
        source="Orton cone chart; cones.md",
    )
    if cone is not None:
        s.fact("cone", cone, source=f"{DESIGN}: firing")
    s.require("T_top", "<=", "T_10", level="warning")
    s.rule(
        "Kiln makers build coils in grooves up to cone 10, with shorter element life; past it, "
        "expect it shorter still.",
        holds=not past_by_cone,
        level="warning",
    )
    if not past_by_cone:  # past cone 10 by its name, no temperature passes
        s.lever("T_top", Q_(500, "degC"), Q_(1800, "degC"))
    return s


def surface_load(
    power_each: float, diameter: float, length: float, limit: Quantity, source: str
) -> Sheet:
    """The elements' surface load against Olsen's most for cone 10: above it they still work,
    but wear out sooner (4th ed. p.254–260)."""
    s = Sheet("electric.surface-load", "The elements' surface load", reference=source)
    s.given(
        "P_e",
        "power of each element",
        Q_(power_each, "W"),
        source="the installed power ÷ the elements",
    )
    s.given(
        "d",
        "the wire's diameter",
        Q_(diameter, "m"),
        "mm",
        source="the wire chosen: the coolest that fits the grooves (ASTM B258)",
    )
    s.given(
        "L",
        "wire in each element",
        Q_(length, "m"),
        "ft",
        source="working: Wire length per element",
    )
    s.let("p", "surface load", "P_e/(pi*d*L)", "W/in**2", source="watts ÷ the wire's surface")
    s.given("p_max", "Olsen's most for cone 10", limit, "W/in**2", source=source)
    s.require("p", "<=", "p_max", level="warning")
    s.lever("P_e", Q_(10, "W"), Q_(20, "kW"))
    return s


@dataclass(frozen=True)
class Arrangement:
    """One way of wiring the elements, and what the engine needs to try it."""

    rows: int  # elements
    series: int  # in series per string
    max_rows: int  # grooves the walls have room for
    grooves: int = 1  # grooves each element runs through


def no_wire_fits(
    power: float,
    power_source: str,
    voltage: float,
    a: Arrangement,
    rho20: Quantity,
    ct: float,
    alloy_source: str,
    max_load: Quantity,
    load_source: str,
    thickest: Quantity,
    next_gauge: Quantity | None,
    coil_ratio: float,
    pitch_min: float,
    coil_source: str,
    groove: float,
) -> Sheet:
    """The thinnest wire the surface load allows, and its coil in the groove; then the first
    standard gauge at or above it (``next_gauge``, None if there is none). Its coil is too long
    for the groove (pitch under 2 d), or no gauge is thick enough. The wire's length goes as d²
    at a set power and voltage, so the pitch ÷ d goes as 1/d²: thicker wire is worse still."""
    s = Sheet("electric.no-wire", "A wire for the elements", reference=KANTHAL_DIAMETER)
    s.given("P", "installed power", Q_(power, "W"), "kW", source=power_source)
    s.given("V", "supply voltage", Q_(voltage, "V"), source=f"{DESIGN}: electric supply")
    s.given(
        "n",
        "elements",
        float(a.rows),
        source=f"{DESIGN}'s, or the count that comes nearest to fitting; walls take {a.max_rows}",
    )
    s.given("s", "elements in series in each string", float(a.series), source="the wiring")
    s.let("P_e", "power of each element", "P/n", "W")
    s.let("U_e", "voltage across each element", "V/s", "V")
    s.given("ρ_20", "the wire's resistivity at 20 °C", rho20, "ohm*mm**2/m", source=alloy_source)
    s.given(
        "C_t", "its resistivity factor hot", ct, source=f"{alloy_source}: a table, interpolated"
    )
    s.let("ρ_T", "resistivity hot", "ρ_20*C_t", "ohm*mm**2/m")
    s.given("p", "surface load allowed", max_load, "W/in**2", source=f"{load_source}. {OLSEN_LOAD}")
    s.let(
        "d",
        "thinnest wire that surface load allows",
        "(4*ρ_T*P_e^2/(pi^2*U_e^2*p))^(1/3)",
        "mm",
        source=KANTHAL_DIAMETER,
    )
    s.given(
        "d_max",
        "thickest standard gauge the tool uses (8 AWG)",
        thickest,
        "mm",
        source="ASTM B258, a table",
    )
    s.let(
        "L",
        "wire in each element, at that diameter",
        "U_e^2/P_e*(pi*d^2/4)/ρ_T",
        "m",
        source="L = R_T·q / ρ_T, R_T = U²/P",
    )
    s.given("r_D", "coil outside diameter ÷ wire", coil_ratio, source=coil_source)
    s.let("N", "turns in each coil", "L/(pi*(r_D - 1)*d)")
    s.given(
        "G",
        "groove for each element: round its walls"
        + (f", {a.grooves} rows" if a.grooves > 1 else ""),
        Q_(groove, "m"),
        "in",
        source=f"{DESIGN}: the element walls",
    )
    s.let("c", "coil pitch ÷ wire, stretched along the groove", "G/(N*d)")
    s.given("c_min", "closest pitch for coils in grooves", pitch_min, source=coil_source)
    s.require("d", "<=", "d_max")
    if next_gauge is None:
        s.require("c", ">=", "c_min")
    else:
        s.given(
            "d_g",
            "the first standard gauge at or above d",
            next_gauge,
            "mm",
            source="ASTM B258, a table",
        )
        s.let(
            "c_g",
            "its coil pitch ÷ wire",
            "c*(d/d_g)^2",
            source="L goes as d², so pitch ÷ d goes as 1/d²",
        )
        s.require("c_g", ">=", "c_min")
    s.lever("G", Q_(0.1, "m"), Q_(50, "m"))
    return s


def power_over_loss(power: float, power_source: str, loss: float) -> Sheet:
    """The elements must put in more than the kiln loses at its top temperature."""
    s = Sheet("electric.power-over-loss", "Installed power against the heat loss at the top")
    s.given(
        "Q",
        "steady heat loss at the top temperature",
        Q_(loss, "W"),
        "kW",
        source="working: Total heat loss at top temperature (the wall solve, iterated)",
    )
    s.given("P", "installed power", Q_(power, "W"), "kW", source=power_source)
    s.require("P", ">", "Q")
    s.lever("P", Q_(0.1, "kW"), Q_(500, "kW"))
    return s


__all__ = [
    "Arrangement",
    "breaker_size",
    "grooves_past_cone_10",
    "no_wire_fits",
    "power_over_loss",
    "supply_power",
    "wire_rating",
]
