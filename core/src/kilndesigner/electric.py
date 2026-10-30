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

from kilndesigner import electric_checks as sheets
from kilndesigner.cones import cone_temperature, hotter_than
from kilndesigner.heatloss import top_temperature
from kilndesigner.library import Alloy, alloy, awg_diameter
from kilndesigner.model import Electric, Kiln
from kilndesigner.shape import chamber_shape
from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_, Quantity, parse_quantity, si
from kilndesigner.working import Finding, Step, show

CONTINUOUS_FRACTION = 0.8
CONTINUOUS_SOURCE = (
    "NEC 210.20(A) continuous loads at 125%, as applied by L&L; electric-and-thermal.md §3 [S25]"
)
# NEC 240.6(A), fuses and inverse-time breakers, to 600 A (electric-and-thermal.md §3 [S79])
STANDARD_BREAKERS = (
    15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 125, 150, 175, 200, 225, 250, 300,
    350, 400, 450, 500, 600,
)  # fmt: skip
BREAKER_MAX_SOURCE = (
    "NEC 422.11(E), a single non-motor appliance, as reported; standard sizes 240.6(A); "
    "electric-and-thermal.md §3 [S23, S79]"
)
# Olsen: normal electric kilns run 5–9 W/in² of wire surface, and a cone 10 kiln is designed at
# 6.4–9 (4th ed. p.254, p.257); Kanthal's chart for A-1 as he prints it gives about 6.6–9.6 near
# cone 10 (p.253). Krueger's 17.5 W/in² for hobby kilns (electric-and-thermal.md §1.6 [S15]) is
# above every point on that chart.
KILN_SURFACE_LOAD = Q_(9, "W/in**2")
SURFACE_LOAD_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.254 and p.257: 5–9 W/in² for normal electric kilns, 6.4–9 "
    "for cone 10; Kanthal's A-1 chart, p.253"
)
# The most any source runs coils in grooves at: Krueger's hobby kilns, A-1 at about 2300 °F. Above
# Olsen's 9 the elements wear out faster (he goes to thinner wire when a coil won't fit, p.260);
# above this the engine has no source at all.
MOST_SURFACE_LOAD = Q_(17.5, "W/in**2")
MOST_LOAD_SOURCE = "Krueger Pottery, A-1 coils in grooves; electric-and-thermal.md §1.6 [S15]"
COIL_RATIO = (5.0, 6.0)  # outside coil diameter / wire diameter, coils in grooves
# Coil pitch / wire diameter: at least 2 d for a spiral in grooves (Kanthal key data [S14]); no
# more than 4 d, the top of Kanthal's general 2–4 d (§1.6 [S13]), since no groove rule gives one
PITCH_RATIO = (2.0, 4.0)
PITCH_TEXT = (
    "at least 2 d in grooves (Kanthal key data [S14]), at most 4 d (Kanthal, general [S13])"
)
COIL_SOURCE = "Kanthal, element in grooves; electric-and-thermal.md §1.6 [S13, S14]"
# Kanthal key data for a spiral in grooves [S14]: wire 2.0–5.0 mm; wall loading at most 35 kW/m²
# at 1000 °C (no figure is given for hotter furnaces, where it can only be lower)
GROOVE_WIRE = (Q_(2.0, "mm"), Q_(5.0, "mm"))
WALL_LOADING = Q_(35, "kW/m**2")
KEY_DATA = "Kanthal key data, spiral in grooves; electric-and-thermal.md §1.6 [S14]"
# Krueger's 17.5 W/in² is for Kanthal A-1 in kilns rated about 2300 °F (§1.6 [S15])
KRUEGER_ALLOY, KRUEGER_TOP = "kanthal-a1", Q_(2300, "degF")
GROOVED_MAX_FURNACE = Q_(1250, "degC")  # Kanthal key data, spiral in grooves [S14]
CONE_10_FAST = cone_temperature("10", 150)  # the hottest that studio kiln makers build for
KANTHAL_MIN_WIRE = Q_(3, "mm")  # Kanthal minimum for grooved elements, for long life [S9, S13]
# An assumption: the wire runs hotter than the kiln. Ct changes by under 1% across 100 °C at
# kiln temperatures (§1.2), so the exact margin barely matters for resistance. Kanthal's one
# published example is 106 K above a 1000 °C furnace for AF rod-over-bend at 3.98 W/cm²
# (electrical-supply.md §5); no figure exists for coils in grooves.
WIRE_ABOVE_KILN = Q_(100, "delta_degC")
COURSE_HEIGHT = Q_(2.5, "in")  # one groove per brick course at most (§5: 9 × 4½ × 2½ in)
# A faceted round wall of 2½ or 3 in brick is laid in 4½ in courses (Skutt KM-1227-3, L&L
# e23T-3; electric-kiln-survey.md), so one groove per 4½ in at most. No maker's groove pitch was
# found; the engine keeps the one-per-course rule, not a spacing of its own.
ROUND_COURSE_HEIGHT = Q_(4.5, "in")
ROUND_SOURCE = (
    "a faceted ring, one brick per facet per course, 4½ in courses (electric-kiln-survey.md, "
    "Skutt KM-1227-3, L&L e23T-3)"
)
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


def largest_breaker(amps: float) -> float:
    """The biggest breaker (A) NEC 422.11(E) allows for a kiln drawing ``amps``, with no rating
    marked on it: 20 A up to 13.3 A; above that, 150 % of the current, or the next standard size
    up when 150 % isn't one."""
    if amps <= 13.3:
        return 20.0
    limit = 1.5 * amps
    # A hair of tolerance, so that 150 % of 16.666… A is the standard 25 A and not 30 A
    return next((s for s in STANDARD_BREAKERS if s >= limit * (1 - 1e-9)), limit)


@dataclass(frozen=True)
class Candidate:
    rows: int  # elements
    series: int
    gauge: int
    diameter: float  # m
    length: float  # m, per element
    load: float  # W/m²
    coil_outside: float  # m
    turns: float
    pitch: float  # m
    grooves: int = 1
    """Groove rows each element runs through, round its walls: Olsen's elements run several
    (4th ed. p.259–260: about 22 ft of stretched coil each)."""

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
    if kiln.chamber.shape == "round":
        # Round the facets of each quarter of the ring the elements are in, along the hot face
        return chamber_shape(kiln).perimeter() / 4 * len(set(electric.walls))
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
        for grooves in range(1, max_rows // rows + 1):
            run = groove * grooves  # each element's coil, stretched along its grooves
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
                        outside, turns, run / turns, grooves,
                    )  # fmt: skip
                    if candidate.pitch_ratio < PITCH_RATIO[0]:
                        break  # too long for its grooves, and thicker wire is longer still
                    if candidate.pitch_ratio <= PITCH_RATIO[1]:
                        found.append(candidate)
    return found


def choose(candidates: list[Candidate]) -> Candidate:
    """The fewest elements, since each is a pair of terminals to wire; then the thickest wire
    that fits them, since thicker wire lasts longer (Kanthal [S9]); then the lowest surface load,
    which also lasts longer (Olsen p.254); then the pitch nearest the middle of its range; then
    the fewest grooves."""
    middle = sum(PITCH_RATIO) / 2
    return min(
        candidates,
        key=lambda c: (c.rows, -c.diameter, c.load, abs(c.pitch_ratio - middle), c.grooves),
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


def _no_wire_sheet(
    electric: Electric,
    wire: Alloy,
    power: float,
    power_source: str,
    voltage: float,
    groove: float,
    max_rows: int,
    rho_t: float,
    ct: float,
) -> Sheet:
    """The sheet behind "no wire fits": the arrangement of elements that comes nearest to fitting,
    with the thinnest wire the surface load allows and its coil stretched along the groove.
    Thicker wire is longer, so if that coil is too long, every thicker one is too."""
    max_load = si(MOST_SURFACE_LOAD, "W/m**2")
    sizes = sorted(si(awg_diameter(g), "m") for g in GAUGES)
    coil = sum(COIL_RATIO) / 2
    best: tuple[float, sheets.Arrangement, float, float | None] | None = None
    for rows in range(1, max_rows + 1):
        if electric.elements is not None and rows != electric.elements:
            continue
        if electric.supply.phase == 3 and rows % 3:
            continue
        per_leg = rows // 3 if electric.supply.phase == 3 else rows
        for grooves in range(1, max_rows // rows + 1):
            for series in (s for s in range(1, per_leg + 1) if per_leg % s == 0):
                p_e, v_e = power / rows, voltage / series
                d = wire_diameter(p_e, v_e, max_load, rho_t)
                turns = wire_length(p_e, v_e, d, rho_t) / (math.pi * (coil - 1) * d)
                pitch = groove * grooves / turns / d
                gauge = next((g for g in sizes if g >= d), None)
                fit = pitch if gauge is None else pitch * (d / gauge) ** 2
                score = min(fit / PITCH_RATIO[0], sizes[-1] / d)
                if best is None or score > best[0]:
                    arrangement = sheets.Arrangement(rows, series, max_rows, grooves)
                    best = (score, arrangement, d, gauge)
    a = best[1] if best else sheets.Arrangement(electric.elements or 1, 1, max_rows)
    gauge = best[3] if best else None
    s = sheets.no_wire_fits(
        power, power_source, voltage, a, wire.resistivity, ct, wire.source, MOST_SURFACE_LOAD,
        MOST_LOAD_SOURCE, awg_diameter(min(GAUGES)),
        None if gauge is None else Q_(gauge, "m"), coil, PITCH_RATIO[0], COIL_SOURCE,
        groove * a.grooves,
    )  # fmt: skip
    if best is None:
        s.rule(
            f"The walls have room for {max_rows} grooves, one per brick course; the elements must "
            "fit them, in threes on a three-phase supply.",
            holds=False,
        )
    else:
        s.agrees("d", best[2])
        if s.check().status == "pass":
            s.rule(
                "A standard gauge from 8 to 20 AWG must lie between the thinnest wire the surface "
                "load allows and the thickest whose coil fits the groove at 2–4 wire diameters; "
                "none does.",
                holds=False,
            )
    return s


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
    power_source = (
        "the design: electric power"
        if electric.power is not None
        else "the circuit's continuous limit (the design leaves the power out)"
    )
    supplying = sheets.supply_power(voltage, breaker, supply.phase, power, power_source)
    supplying.agrees("P_s", supply_power)
    if (check := supplying.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"{show(Q_(power, 'W'), 'kW')} is more than the circuit can supply "
                    f"continuously ({show(Q_(supply_power, 'W'), 'kW')}). Use a bigger circuit or "
                    f"install less power."
                ),
            )
        )
    line_current = power / (root3 * voltage)
    largest = largest_breaker(line_current)
    working.append(
        Step(
            name="Largest breaker allowed",
            value=show(Q_(largest, "A")),
            formula=(
                "20 A up to 13.3 A; above that, 150 % of the kiln's current, or the next "
                "standard size up"
            ),
            inputs={"kiln's current": show(Q_(line_current, "A"), digits=3)},
            reference=BREAKER_MAX_SOURCE,
        )
    )
    sizing = sheets.breaker_size(
        voltage, supply.phase, power, power_source, breaker, largest, BREAKER_MAX_SOURCE
    )
    sizing.agrees("I", line_current)
    if (check := sizing.check()).status != "pass":
        draws = show(Q_(line_current, "A"), digits=3)
        least = show(Q_(line_current / CONTINUOUS_FRACTION, "A"), digits=3)
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"A {show(supply.breaker)} breaker is too big for a kiln that draws {draws}: "
                    "it wouldn't protect the kiln's own wiring, terminal block and cord. NEC "
                    f"422.11(E) allows at most {show(Q_(largest, 'A'))} here, and the breaker must "
                    f"still be at least 125 % of the current, {least}. Use a smaller breaker, or "
                    "install more power."
                ),
                reference=BREAKER_MAX_SOURCE,
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
            value=show(Q_(rho_t, "ohm*m"), "ohm*mm**2/m"),
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
    shape = chamber_shape(kiln)
    is_round = kiln.chamber.shape == "round"
    course = ROUND_COURSE_HEIGHT if is_round else COURSE_HEIGHT
    max_rows = int(si(kiln.chamber.height, "m") / si(course, "m") + 1e-9)
    if is_round:
        working.append(
            _round_grooves_step(
                electric, shape.sides, groove, max_rows, us, kiln.chamber.floor_inside
            )
        )
    max_load = si(MOST_SURFACE_LOAD, "W/m**2")
    preferred = si(KILN_SURFACE_LOAD, "W/m**2")
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
        nearest = _no_wire_sheet(
            electric, wire, power, power_source, voltage, groove, max_rows, rho_t, ct
        )
        findings.append(
            Finding.failed(
                nearest.check(),
                message=(
                    "No standard wire gauge gives elements that fit the grooves with a coil pitch "
                    "of 2–4 wire diameters under the surface-load limit. Change the element walls, "
                    "the number of elements, or the power."
                ),
                reference=COIL_SOURCE,
            )
        )
    else:
        # Olsen's load where anything fits it; else the lowest that fits (he goes to thinner wire
        # when a coil won't fit, p.260), with a warning: the elements wear out sooner
        within = [c for c in candidates if c.load <= preferred * (1 + 1e-9)]
        best = (
            choose(within)
            if within
            else min(candidates, key=lambda c: (c.load, c.rows, -c.diameter))
        )
        elements = _element_result(best, wire, voltage, power, groove, us, supply.phase)
        if not within:
            loading = sheets.surface_load(
                power / best.rows, best.diameter, best.length, KILN_SURFACE_LOAD,
                SURFACE_LOAD_SOURCE,
            )  # fmt: skip
            loading.agrees("p", best.load)
            findings.append(
                Finding.failed(
                    loading.check(),
                    message=(
                        f"No wire that fits the grooves runs at Olsen's 9 W/in² or less: the "
                        f"coolest is {show(Q_(best.load, 'W/m**2'), 'W/in**2', 3)}. The elements "
                        "will wear out sooner. Elements in more walls, or less power, would bring "
                        "it down."
                    ),
                )
            )
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
        # The limit the chosen wire was held to: Olsen's, or Krueger's when nothing fits his
        limit = (preferred, SURFACE_LOAD_SOURCE) if within else (max_load, MOST_LOAD_SOURCE)
        working.extend(_element_steps(best, p_e, v_e, rho_t, limit, us))
        if not within and (
            electric.alloy != KRUEGER_ALLOY or si(top, "degF") > si(KRUEGER_TOP, "degF") + 1e-6
        ):
            findings.append(
                Finding(
                    level="info",
                    message=(
                        f"The elements run above Olsen's 9 W/in², held only to Krueger's 17.5, "
                        f"which is for Kanthal A-1 in kilns rated about 2300 °F. This kiln is "
                        f"{electric.alloy} to {show(top, temp_unit)}: no source covers that load "
                        "there, so expect the elements to wear faster than Krueger's."
                    ),
                    reference=MOST_LOAD_SOURCE,
                )
            )
        thin = sheets.groove_wire(best.diameter, GROOVE_WIRE[0], KEY_DATA).check()
        if thin.status != "pass":
            findings.append(
                Finding.failed(
                    thin,
                    message=(
                        f"The wire is {show(Q_(best.diameter, 'm'), 'mm', 3)}, under the 2.0–5.0 "
                        "mm Kanthal gives for coils in grooves: outside the range the maker "
                        "has checked. Thinner wire sags and burns through sooner."
                    ),
                    reference=KEY_DATA,
                )
            )
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
            findings.append(_thin_wire(best, everything, electric, kiln.door_wall or ""))

    # Wall loading: the power over the inside area of the walls that carry elements
    c = kiln.chamber
    w, d, h = si(c.width, "m"), si(c.length, "m"), si(c.height, "m")
    side = {"left": d * h, "right": d * h, "back": w * h, "front": w * h}
    if is_round:  # quarters of the ring, flats and corners
        side = {f.face: f.inside_area for f in shape.faces() if f.orientation == "vertical"}
    wall_area = sum(side.get(wall, 0.0) for wall in electric.walls)
    if wall_area > 0:
        loading = power / wall_area
        working.append(
            Step(
                name="Wall loading",
                value=show(Q_(loading, "W/m**2"), "kW/m**2", 3),
                formula="installed power ÷ inside area of the element walls",
                inputs={
                    "element walls": ", ".join(electric.walls),
                    "their area": show(Q_(wall_area, "m**2"), "ft**2" if us else "m**2", 3),
                    "Kanthal's most, in grooves at 1000 °C": show(WALL_LOADING),
                },
                reference=KEY_DATA,
                note="Kanthal gives no figure above 1000 °C, where it can only be lower; and the "
                "floor and roof carry no elements here.",
            )
        )
        walls = sheets.wall_loading(power, wall_area, WALL_LOADING, KEY_DATA)
        walls.agrees("w", Q_(loading, "W/m**2"))
        if (check := walls.check()).status != "pass":
            findings.append(
                Finding.failed(
                    check,
                    message=(
                        f"The element walls carry {show(Q_(loading, 'W/m**2'), 'kW/m**2', 3)}, "
                        f"over Kanthal's {show(WALL_LOADING)} for coils in grooves at 1000 °C "
                        "(less hotter). Put elements in more walls, or install less power."
                    ),
                    reference=KEY_DATA,
                )
            )

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
        if kiln.heat.gas is None:
            enough = sheets.power_over_loss(power, power_source, heat_loss_watts)
            if (check := enough.check()).status != "pass":
                findings.append(
                    Finding.failed(
                        check,
                        message=(
                            "The installed power is no more than the heat loss at top "
                            "temperature: the kiln can never reach it. Add power or insulation."
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


def _round_grooves_step(
    electric: Electric,
    sides: int | None,
    groove: float,
    rows: int,
    us: bool,
    floor_inside: bool = False,
) -> Step:
    """The grooves of a round kiln: round the facets, one per course above the floor."""
    inputs = {
        "element walls (quarters of the ring)": ", ".join(electric.walls),
        "courses": str(rows),
        "course height": show(ROUND_COURSE_HEIGHT),
    }
    if floor_inside:
        # The floor slab fills the wall's lowest course, so it has no groove (FLOOR_INSIDE_SOURCE)
        inputs["the wall's lowest course"] = "holds the floor slab, no groove"
    if sides is None:
        formula = "π·D/4 per quarter"
        note = (
            "The wall isn't one ring of whole bricks cut to the angle, so the groove is taken "
            "round the circle."
        )
    else:
        formula = "2·N·a·tan(π/N)/4 per quarter, a = D/(1 + 1/cos(π/N))"
        inputs["N, facets"] = str(sides)
        note = (
            "Each groove runs round the flats of its course, the coil bending at each corner. No "
            "source gives a groove pitch, a groove depth, or how tight a coil may bend at a "
            "facet's corner: one groove per course is the engine's limit, from the bricks' size."
        )
    return Step(
        name="Groove round the ring, per element course",
        value=show(Q_(groove, "m"), "ft" if us else "m"),
        formula=formula,
        inputs=inputs,
        reference=ROUND_SOURCE,
        note=note,
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
    # The wire still works past its rating; it wears out faster, so a warning
    rating = sheets.wire_rating(
        wire.name, top, WIRE_ABOVE_KILN, wire.max_air_temperature, wire.source, temp_unit
    )
    rating.agrees("T_w", wire_temp)
    if (check := rating.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"{wire.name} is rated to {show(wire.max_air_temperature, temp_unit)} in air; "
                    f"elements here would run near {show(wire_temp, temp_unit)}, so expect them to "
                    f"wear out faster. The wire is taken as {show(WIRE_ABOVE_KILN)} above the "
                    "kiln, an assumption: Kanthal gives no figure for coils in grooves."
                ),
            )
        )
    if si(top, "K") > si(GROOVED_MAX_FURNACE, "K"):
        # Usual practice up to cone 10, so a note there; past cone 10, by the design's
        # temperature or its cone, it is a warning, and its sheet says why
        cone = kiln.firing.cone
        grooves = sheets.grooves_past_cone_10(
            top,
            GROOVED_MAX_FURNACE,
            CONE_10_FAST,
            cone,
            cone is not None and hotter_than(cone, "10"),
            temp_unit,
        )
        message = (
            f"Kanthal lists {show(GROOVED_MAX_FURNACE, temp_unit)} as the highest kiln "
            f"temperature for coils in grooves; this kiln reaches {show(top, temp_unit)}. "
            "Kiln makers build cone 10 kilns this way, with shorter element life."
        )
        reference = "Kanthal key data for elements; electric-and-thermal.md §1.6 [S14]"
        if (check := grooves.check()).status != "pass":
            findings.append(Finding.failed(check, message=message, reference=reference))
        else:
            findings.append(Finding(level="info", message=message, reference=reference))


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
        stretched_length_each=show(Q_(groove * c.grooves, "m"), short),
        pitch=f"{show(Q_(c.pitch, 'm'), short, 3)} ({c.pitch_ratio:.2f} × wire diameter)",
        groove_rows=c.rows * c.grooves,
        groove_length_each=show(Q_(groove * c.grooves, "m"), short),
        wire_mass_total=show(Q_(mass, "kg"), "lb" if us else "kg", 3),
    )


def _element_steps(
    c: Candidate,
    p_e: float,
    v_e: float,
    rho_t: float,
    limit: tuple[float, str],
    us: bool,
) -> list[Step]:
    max_load, limit_source = limit
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
            reference=limit_source,
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
            inputs={
                "U, each element": show(Q_(v_e, "V"), digits=4),
                "P, each element": show(Q_(p_e, "W"), "W", 4),
                "d": show(Q_(c.diameter, "m"), "mm", 3),
            },
            reference="Kanthal element design: R = U²/P, L = R·q/ρ_T; electric-and-thermal.md "
            "§1.6 [S13]",
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
            inputs={"D/d": f"{sum(COIL_RATIO) / 2:g}", "pitch range": PITCH_TEXT},
            reference=COIL_SOURCE,
        ),
    ]
