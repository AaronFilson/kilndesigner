"""Element design for electric kilns: wire, length, coil and circuits.

The method is Kanthal's (electric-and-thermal.md §1.6, §1.7):
- the hot resistance from the power and voltage: R_T = U²/P;
- the wire diameter from the surface load p allowed: d³ = 4·ρ20·Ct·P² / (π²·U²·p);
- the length from the chosen standard wire: L = R_T·q / (ρ20·Ct), q = πd²/4;
- the coil from the groove rules: outside diameter 5–6 d, pitch 2–4 d.

The circuit follows the NEC continuous-load rule as kiln makers apply it: the kiln may draw at
most 80% of the breaker's rating (the breaker is 125% of the load) (§3, L&L [S25]).
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict

from kilndesigner.cones import cone_temperature
from kilndesigner.heatloss import top_temperature
from kilndesigner.library import Alloy, alloy, awg_diameter
from kilndesigner.model import Electric, Kiln
from kilndesigner.shape import chamber_shape
from kilndesigner.units import Q_, Quantity, parse_quantity, si
from kilndesigner.working import Finding, Step, show

CONTINUOUS_FRACTION = 0.8
CONTINUOUS_SOURCE = (
    "NEC 210.20(A) continuous loads at 125%, as applied by L&L; electric-and-thermal.md §3 [S25]"
)
# Krueger Pottery: about 17.5 W/in² for Kanthal A-1 coils in brick grooves, kilns rated about
# 2300 °F (electric-and-thermal.md §1.6, [S15]).
KILN_SURFACE_LOAD = Q_(17.5, "W/in**2")
SURFACE_LOAD_SOURCE = "Krueger Pottery, A-1 coils in grooves; electric-and-thermal.md §1.6 [S15]"
COIL_RATIO = (5.0, 6.0)  # outside coil diameter / wire diameter, coils in grooves
PITCH_RATIO = (2.0, 4.0)  # coil pitch / wire diameter
COIL_SOURCE = "Kanthal, element in grooves; electric-and-thermal.md §1.6 [S13, S14]"
GROOVED_MAX_FURNACE = Q_(1250, "degC")  # Kanthal key data, spiral in grooves [S14]
CONE_10_FAST = cone_temperature("10", 150)  # the hottest that studio kiln makers build for
KANTHAL_MIN_WIRE = Q_(3, "mm")  # Kanthal minimum for grooved elements, for long life [S9, S13]
# An assumption: the wire runs hotter than the kiln. Ct changes by under 1% across 100 °C at
# kiln temperatures (§1.2), so the exact margin barely matters for resistance. Kanthal's one
# published example is 106 K above a 1000 °C furnace for AF rod-over-bend at 3.98 W/cm²
# (electrical-supply.md §5); no figure exists for coils in grooves.
WIRE_ABOVE_KILN = Q_(100, "delta_degC")
COURSE_HEIGHT = Q_(2.5, "in")  # one groove per brick course at most (§5: 9 × 4½ × 2½ in)
GAUGES = range(8, 21)


def wire_diameter(power: float, voltage: float, surface_load: float, rho_t: float) -> float:
    """Kanthal's wire diameter (m) for a power (W), voltage (V), load (W/m²), ρ_T (Ω·m)."""
    return (4 * rho_t * power**2 / (math.pi**2 * voltage**2 * surface_load)) ** (1 / 3)


def wire_length(power: float, voltage: float, diameter: float, rho_t: float) -> float:
    """Length (m) of wire of ``diameter`` (m) that draws ``power`` at ``voltage``."""
    area = math.pi * diameter**2 / 4
    return voltage**2 / power * area / rho_t


def surface_load(power: float, diameter: float, length: float) -> float:
    """W/m² of wire surface."""
    return power / (math.pi * diameter * length)


@dataclass(frozen=True)
class Candidate:
    rows: int
    series: int
    gauge: int
    diameter: float  # m
    length: float  # m, per element
    load: float  # W/m²
    coil_outside: float  # m
    turns: float
    pitch: float  # m

    @property
    def pitch_ratio(self) -> float:
        return self.pitch / self.diameter


class ElementResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    count: int
    wiring: str
    gauge: str
    wire_diameter: str
    length_each: str
    cold_resistance_each: str
    hot_resistance_each: str
    power_each: str
    current_each: str
    surface_load: str
    coil_outside_diameter: str
    coil_outside_diameter_mm: float
    turns_each: str
    close_wound_length_each: str
    stretched_length_each: str
    pitch: str
    groove_rows: int
    groove_length_each: str
    wire_mass_total: str


class ElectricDesign(BaseModel):
    model_config = ConfigDict(frozen=True)

    alloy: str
    supply: str
    continuous_current_limit: str
    installed_power: str
    installed_watts: float
    line_current: str
    elements: ElementResult | None
    power_per_volume: str
    working: list[Step]
    findings: list[Finding]


def _groove_length(kiln: Kiln, electric: Electric) -> float:
    lengths = {
        "left": si(kiln.chamber.depth, "m"),
        "right": si(kiln.chamber.depth, "m"),
        "back": si(kiln.chamber.width, "m"),
        "front": si(kiln.chamber.width, "m"),
    }
    return sum(lengths[w] for w in electric.walls)


def _candidates(
    *,
    power: float,
    voltage: float,
    phases: Literal[1, 3],
    groove: float,
    max_rows: int,
    rho_t: float,
    max_load: float,
    fixed_count: int | None,
) -> list[Candidate]:
    found: list[Candidate] = []
    for rows in range(1, max_rows + 1):
        if fixed_count is not None and rows != fixed_count:
            continue
        if phases == 3 and rows % 3:
            continue
        per_leg = rows // 3 if phases == 3 else rows
        for series in range(1, per_leg + 1):
            if per_leg % series:
                continue
            p_e, v_e = power / rows, voltage / series
            d_min = wire_diameter(p_e, v_e, max_load, rho_t)
            for gauge in reversed(GAUGES):  # from the thinnest
                d = si(awg_diameter(gauge), "m")
                if d < d_min:
                    continue  # over the surface-load limit
                length = wire_length(p_e, v_e, d, rho_t)
                outside = sum(COIL_RATIO) / 2 * d
                turns = length / (math.pi * (outside - d))
                candidate = Candidate(
                    rows, series, gauge, d, length, surface_load(p_e, d, length),
                    outside, turns, groove / turns,
                )  # fmt: skip
                if candidate.pitch_ratio < PITCH_RATIO[0]:
                    break  # the coil is too long for the groove, and thicker wire is longer still
                if candidate.pitch_ratio <= PITCH_RATIO[1]:
                    found.append(candidate)
    return found


def choose(candidates: list[Candidate]) -> Candidate:
    """The fewest elements, since each is a groove to cut and a pair of terminals to wire; then
    the thickest wire that fits them, since thicker wire lasts longer (Kanthal [S9]); then the
    lowest surface load, which also lasts longer (Krueger [S15]); then the pitch nearest the
    middle of its range."""
    middle = sum(PITCH_RATIO) / 2
    return min(
        candidates,
        key=lambda c: (c.rows, -c.diameter, c.load, abs(c.pitch_ratio - middle)),
    )


def _thin_wire(
    best: Candidate, everything: list[Candidate], electric: Electric, door: str
) -> Finding:
    """Why the wire is under Kanthal's 3 mm, and what would allow thicker wire."""
    wire = f"{best.gauge} AWG wire ({show(Q_(best.diameter, 'm'), 'mm', 3)})"
    if electric.elements is None:
        chose = (
            f"The tool chose {best.rows} elements of {wire}: the fewest elements that work, each "
            "with the thickest wire whose coil fits its groove."
        )
    else:
        chose = (
            f"For the {best.rows} elements the design asks for, the tool chose {wire}, the "
            "thickest whose coil fits each groove."
        )
    thick = [c for c in everything if c.diameter >= si(KANTHAL_MIN_WIRE, "m")]
    if thick:
        alt = choose(thick)
        then = (
            f"{alt.rows} elements would take {alt.gauge} AWG "
            f"({show(Q_(alt.diameter, 'm'), 'mm', 3)}); set elements: {alt.rows} in the "
            "design's electric heat to use them."
        )
    else:
        free = [w for w in ("left", "right", "back", "front") if w not in electric.walls]
        room = any(w != door for w in free)
        then = (
            f"No number of elements in {_walls(electric.walls)} fits wire that thick, because "
            "its coils would be longer than the grooves. "
            + ("Elements in more walls would make room; otherwise, expect " if room else "Expect ")
            + "to replace these elements sooner."
        )
    return Finding(
        level="info",
        message=(
            f"{chose} Kanthal recommends wire of 3 mm or more for the longest life in grooves. "
            f"{then}"
        ),
        reference="electric-and-thermal.md §1.6 [S9, S13]",
    )


def _walls(walls: Sequence[str]) -> str:
    """'the left wall', 'the left and back walls', 'the left, right and back walls'."""
    if len(walls) == 1:
        return f"the {walls[0]} wall"
    return f"the {', '.join(walls[:-1])} and {walls[-1]} walls"


def design_elements(kiln: Kiln, heat_loss_watts: float | None = None) -> ElectricDesign:
    electric = kiln.heat.electric
    if electric is None:
        raise ValueError("the kiln has no electric heat")
    wire = alloy(electric.alloy)
    us = kiln.units == "us"
    temp_unit = "degF" if us else "degC"
    findings: list[Finding] = []
    working: list[Step] = []

    supply = electric.supply
    voltage, breaker = si(supply.voltage, "V"), si(supply.breaker, "A")
    limit_current = CONTINUOUS_FRACTION * breaker
    root3 = math.sqrt(3) if supply.phase == 3 else 1.0
    supply_power = root3 * voltage * limit_current
    working.append(
        Step(
            name="Continuous current limit",
            value=show(Q_(limit_current, "A")),
            formula="0.8 × breaker rating (the breaker is 125% of a continuous load)",
            inputs={"breaker": show(supply.breaker)},
            reference=CONTINUOUS_SOURCE,
        )
    )
    working.append(
        Step(
            name="Power the circuit can supply",
            value=show(Q_(supply_power, "W"), "kW"),
            formula="P = V·I" if supply.phase == 1 else "P = √3·V·I (three-phase)",
            inputs={"voltage": show(supply.voltage), "current": show(Q_(limit_current, "A"))},
        )
    )
    power = si(electric.power, "W") if electric.power is not None else supply_power
    if power > supply_power * (1 + 1e-9):
        findings.append(
            Finding(
                level="error",
                message=(
                    f"{show(Q_(power, 'W'), 'kW')} is more than the circuit can supply "
                    f"continuously ({show(Q_(supply_power, 'W'), 'kW')}). Use a bigger circuit or "
                    f"install less power."
                ),
                reference=CONTINUOUS_SOURCE,
            )
        )

    top, _ = top_temperature(kiln)
    wire_temp = top + WIRE_ABOVE_KILN
    ct = wire.temperature_factor(wire_temp)
    rho20 = si(wire.resistivity, "ohm*m")
    rho_t = rho20 * ct
    working.append(
        Step(
            name="Wire resistivity when hot",
            value=show(Q_(rho_t, "ohm*mm**2/m"), "ohm*mm**2/m"),
            formula="ρ_T = ρ20 · Ct",
            inputs={
                "ρ20": show(wire.resistivity),
                "wire temperature": show(wire_temp, temp_unit),
                "Ct": show(ct, digits=3),
            },
            reference=wire.source,
            note="The wire is assumed to run 100 °C above the kiln; Ct changes little there.",
        )
    )
    _check_temperatures(kiln, wire, top, wire_temp, findings, temp_unit)

    groove = _groove_length(kiln, electric)
    max_rows = int(si(kiln.chamber.height, "m") // si(COURSE_HEIGHT, "m"))
    max_load = si(KILN_SURFACE_LOAD, "W/m**2")
    candidates = _candidates(
        power=power,
        voltage=voltage,
        phases=supply.phase,
        groove=groove,
        max_rows=max_rows,
        rho_t=rho_t,
        max_load=max_load,
        fixed_count=electric.elements,
    )
    elements: ElementResult | None = None
    if not candidates:
        findings.append(
            Finding(
                level="error",
                message=(
                    "No standard wire gauge gives elements that fit the grooves with a coil pitch "
                    "of 2–4 wire diameters under the surface-load limit. Change the element walls, "
                    "the number of elements, or the power."
                ),
                reference=COIL_SOURCE,
            )
        )
    else:
        best = choose(candidates)
        elements = _element_result(best, wire, voltage, power, groove, us, supply.phase)
        # Current follows V/R: +5 % at the top of ANSI C84.1 Range A, more again while the wire
        # is cold (R falls by Ct). Makers design at the 80 % limit too (Skutt KM1027: 48 A on 60 A;
        # electrical-supply.md §1–3), so this is a note.
        hot_amps = power / (root3 * voltage)
        ct = wire.temperature_factor(wire_temp)
        findings.append(
            Finding(
                level="info",
                message=(
                    f"The elements draw {hot_amps:.1f} A hot at {show(supply.voltage)}. At +5 % "
                    f"supply voltage (ANSI C84.1 Range A) that is {1.05 * hot_amps:.1f} A, and "
                    f"{1.05 * hot_amps * ct:.1f} A while the wire is cold, against the "
                    f"{limit_current:.0f} A continuous limit. Kiln makers rate kilns the same way."
                ),
                reference="electrical-supply.md §1 [E1–E3], §3",
            )
        )
        p_e, v_e = power / best.rows, voltage / best.series
        working.extend(_element_steps(best, p_e, v_e, rho_t, max_load, us))
        if best.diameter < si(KANTHAL_MIN_WIRE, "m"):
            everything = candidates
            if electric.elements is not None:
                everything = _candidates(
                    power=power,
                    voltage=voltage,
                    phases=supply.phase,
                    groove=groove,
                    max_rows=max_rows,
                    rho_t=rho_t,
                    max_load=max_load,
                    fixed_count=None,
                )
            findings.append(_thin_wire(best, everything, electric, kiln.door_face))

    line_current = power / (root3 * voltage)
    volume = _chamber_volume(kiln)
    per_volume = Q_(power / volume, "W/m**3")
    working.append(
        Step(
            name="Installed power per unit of chamber volume",
            value=show(per_volume, "W/ft**3" if us else "kW/m**3"),
            note=(
                "For comparison, 7 cu ft cone 10 kilns from L&L and Skutt have about "
                "1650–1720 W/ft³ (electric-and-thermal.md §7 [S73, S74])."
            ),
        )
    )
    if heat_loss_watts:
        ratio = power / heat_loss_watts
        working.append(
            Step(
                name="Installed power over steady loss at top temperature",
                value=show(ratio, digits=3),
                formula="P_installed / Q_loss",
                note="Power above the loss is what heats the ware and walls near the top.",
            )
        )
        if ratio <= 1.0 and kiln.heat.gas is None:
            findings.append(
                Finding(
                    level="error",
                    message=(
                        "The installed power is no more than the heat loss at top temperature: "
                        "the kiln can never reach it. Add power or insulation."
                    ),
                )
            )
        elif ratio <= 1.0:
            findings.append(
                Finding(
                    level="info",
                    message=(
                        "The elements alone can't hold the top temperature; in this hybrid the "
                        "burners take over before then."
                    ),
                )
            )
    findings.append(
        Finding(
            level="info",
            message=(
                "Electrical work must follow your local code and be checked by a licensed "
                "electrician. These results are engineering guidance, not an approved design."
            ),
        )
    )
    return ElectricDesign(
        alloy=wire.name,
        supply=f"{show(supply.voltage)}, {supply.phase}-phase, {show(supply.breaker)} breaker",
        continuous_current_limit=show(Q_(limit_current, "A")),
        installed_power=show(Q_(power, "W"), "kW"),
        installed_watts=power,
        line_current=show(Q_(line_current, "A")),
        elements=elements,
        power_per_volume=show(per_volume, "W/ft**3" if us else "kW/m**3"),
        working=working,
        findings=findings,
    )


def _chamber_volume(kiln: Kiln) -> float:
    return chamber_shape(kiln).volume


def _check_temperatures(
    kiln: Kiln,
    wire: Alloy,
    top: Quantity,
    wire_temp: Quantity,
    findings: list[Finding],
    temp_unit: str,
) -> None:
    if si(wire_temp, "K") > si(wire.max_air_temperature, "K"):
        findings.append(
            Finding(
                level="error",
                message=(
                    f"{wire.name} is rated to {show(wire.max_air_temperature, temp_unit)} in air; "
                    f"elements here would run near {show(wire_temp, temp_unit)}. The wire is taken "
                    f"as {show(WIRE_ABOVE_KILN)} above the kiln, an assumption: Kanthal gives no "
                    "figure for coils in grooves."
                ),
                reference=wire.source,
            )
        )
    if si(top, "K") > si(GROOVED_MAX_FURNACE, "K"):
        findings.append(
            Finding(
                # Usual practice up to cone 10, so a note there; past cone 10 it is a warning.
                level="info" if si(top, "K") <= si(CONE_10_FAST, "K") + 1e-6 else "warning",
                message=(
                    f"Kanthal lists {show(GROOVED_MAX_FURNACE, temp_unit)} as the highest furnace "
                    f"temperature for coils in grooves; this kiln reaches {show(top, temp_unit)}. "
                    "Kiln makers build cone 10 kilns this way, with shorter element life."
                ),
                reference="Kanthal key data for elements; electric-and-thermal.md §1.6 [S14]",
            )
        )


def _element_result(
    c: Candidate,
    wire: Alloy,
    voltage: float,
    power: float,
    groove: float,
    us: bool,
    phase: int = 1,
) -> ElementResult:
    p_e, v_e = power / c.rows, voltage / c.series
    rho20 = si(wire.resistivity, "ohm*m")
    area = math.pi * c.diameter**2 / 4
    r_cold = rho20 * c.length / area
    r_hot = v_e**2 / p_e
    mass = c.rows * c.length * area * si(parse_quantity(wire.density), "kg/m**3")
    long_, short = ("ft", "in") if us else ("m", "mm")
    strings = c.rows // c.series
    wiring = (
        f"{strings} string(s) of {c.series} in series"
        if c.series > 1
        else f"{c.rows} in parallel, each across the full voltage"
    )
    if phase == 3:
        # v_e = line voltage / series: only true in delta (electrical-supply.md §4).
        wiring += f", in delta: {strings // 3} string(s) across each pair of lines"
    return ElementResult(
        count=c.rows,
        wiring=wiring,
        gauge=f"{c.gauge} AWG",
        wire_diameter=show(Q_(c.diameter, "m"), short, 3),
        length_each=show(Q_(c.length, "m"), long_),
        cold_resistance_each=show(Q_(r_cold, "ohm")),
        hot_resistance_each=show(Q_(r_hot, "ohm")),
        power_each=show(Q_(p_e, "W"), "W"),
        current_each=show(Q_(v_e / r_hot, "A")),
        surface_load=show(Q_(c.load, "W/m**2"), "W/in**2" if us else "W/cm**2", 3),
        coil_outside_diameter=show(Q_(c.coil_outside, "m"), short, 3),
        coil_outside_diameter_mm=c.coil_outside * 1000,
        turns_each=show(c.turns, digits=4),
        close_wound_length_each=show(Q_(c.turns * c.diameter, "m"), short),
        stretched_length_each=show(Q_(groove, "m"), short),
        pitch=f"{show(Q_(c.pitch, 'm'), short, 3)} ({c.pitch_ratio:.2f} × wire diameter)",
        groove_rows=c.rows,
        groove_length_each=show(Q_(groove, "m"), short),
        wire_mass_total=show(Q_(mass, "kg"), "lb" if us else "kg", 3),
    )


def _element_steps(
    c: Candidate, p_e: float, v_e: float, rho_t: float, max_load: float, us: bool
) -> list[Step]:
    load_unit = "W/in**2" if us else "W/cm**2"
    short = "in" if us else "mm"
    d_min = wire_diameter(p_e, v_e, max_load, rho_t)
    return [
        Step(
            name="Power and voltage per element",
            value=f"{show(Q_(p_e, 'W'), 'W')} at {show(Q_(v_e, 'V'))}",
            inputs={"elements": str(c.rows), "in series per string": str(c.series)},
        ),
        Step(
            name="Smallest wire for the surface-load limit",
            value=show(Q_(d_min, "m"), "mm", 3),
            formula="d³ = 4·ρ_T·P² / (π²·U²·p)",
            inputs={"p (limit)": show(Q_(max_load, "W/m**2"), load_unit, 3)},
            reference=SURFACE_LOAD_SOURCE,
        ),
        Step(
            name="Wire chosen",
            value=f"{c.gauge} AWG, {show(Q_(c.diameter, 'm'), 'mm', 3)}",
            note=(
                "The fewest elements that work, then the thickest standard gauge (ASTM B258) for "
                "them: at or above the smallest diameter, with a coil that fits the groove at a "
                "pitch of 2–4 wire diameters. Thicker wire lasts longer (Kanthal)."
            ),
            reference="electric-and-thermal.md §1.6 [S9, S13]",
        ),
        Step(
            name="Wire length per element",
            value=show(Q_(c.length, "m"), "ft" if us else "m"),
            formula="L = U²/P · (πd²/4) / ρ_T",
        ),
        Step(
            name="Surface load",
            value=show(Q_(c.load, "W/m**2"), load_unit, 3),
            formula="p = P / (π·d·L)",
            reference=SURFACE_LOAD_SOURCE,
        ),
        Step(
            name="Coil",
            value=(
                f"{c.turns:.0f} turns, {show(Q_(c.coil_outside, 'm'), short, 3)} outside, "
                f"pitch {c.pitch_ratio:.2f} d"
            ),
            formula="turns = L / (π·(D − d)); pitch = groove length / turns",
            inputs={"D/d": f"{sum(COIL_RATIO) / 2:g}", "pitch range": "2–4 d"},
            reference=COIL_SOURCE,
        ),
    ]
