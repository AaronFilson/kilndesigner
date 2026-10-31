"""A slow firing: the kiln fired over a long time the user chooses, for ware that needs it.

Firing speed is the user's choice (the author, 30 October 2026): nothing here limits or warns on
the rate. The engine fires the design's own heat (elements, burners or both) along a paced
schedule, a constant rise from the room to the top in the chosen time less the soak, then the
soak at the top, and reports what that firing takes: its heat, where the heat goes (the walls'
store, the ware, the shell's loss), its fuel or electricity and cost, beside the same kiln's
quickest firing. A kiln whose heat can't reach the top at all is a physical fault and is warned.

What the sources say about slow firings is given beside it, each as reported, as options to
compare (slow-firing.md): Bizen's seven days, La Borne's tunnel kilns, Tamba's tube kilns,
Kaneko's car kiln of several days, Kato's thick-walled coal kiln, anagamas' cords of wood.

Wood, coal and oil kilns aren't simulated (milestone M7, no wood combustion source yet), so for
them only the sources are given. A schedule longer than the longest sourced firing is refused
(simulation.LONGEST_FIRING_H).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from kilndesigner.heatloss import top_temperature
from kilndesigner.model import Kiln, Ramp
from kilndesigner.sheet import Sheet
from kilndesigner.simulation import (
    LONGEST_FIRING_H,
    LONGEST_FIRING_SOURCE,
    FiringResult,
    SimulationError,
    simulate,
)
from kilndesigner.units import Q_, si
from kilndesigner.working import Finding, Step, show

OLSEN = "Olsen, The Kiln Book, 4th ed."
BIZEN_AIM = (
    '"maximum efficiency of wood consumption over a seven-day firing period with minimum stoking '
    'and draft" and "minimum loss of heat during gradual temperature increase"'
)


class SourcedFiring(BaseModel):
    """One slow firing as a source reports it: no engine number, an option to compare."""

    model_config = ConfigDict(frozen=True)

    kiln: str
    fuel: str
    time: str
    used: str | None = None  # fuel per firing, as reported
    notes: str | None = None
    reference: str


SOURCED: tuple[SourcedFiring, ...] = (
    SourcedFiring(
        kiln="Kei Fujiwara's Bizen kiln (climbing cross-draft)",
        fuel="wood",
        time="seven days: 2½ days stoking the fire-mouth air duct, 4 days the fire mouth, 12 h the "
        "chambers; the top at 6½ days, then a soaking fire; cooled closed over about three days",
        notes="designed for " + BIZEN_AIM + "; Bizen clays bloat, blister, crack and sag if fired "
        "too rapidly; walls 10–13 in, tight, no expansion joints",
        reference=f"{OLSEN}, p.99, pp.100, 103–105",
    ),
    SourcedFiring(
        kiln="La Borne tunnel kilns, 1766–2825 ft³",
        fuel="wood",
        time="2½–3 days' preheating, up to four days of petit feu with split logs, about one day "
        "of grand feu with branches and twigs: about 7–8 days (derived)",
        reference=f"{OLSEN}, p.110–111",
    ),
    SourcedFiring(
        kiln="Tamba tube kilns, 120–150 ft long",
        fuel="wood",
        time="the firebox about 36 h, to about 1000 °C at the first stoke holes; then side "
        "stoking, 14 (?) to 18 h",
        used="about 200 bundles of kindling, 15 × 15 × 30 in, side stoking",
        reference=f"{OLSEN}, pp.86–87",
    ),
    SourcedFiring(
        kiln="Suzuki cooperative climbing kiln, Kyoto, seven chambers",
        fuel="wood bundles",
        time="about 56 h to cone 8–9; the firebox 15 h to 1000 °C",
        used="about 75 bundles a side in each of chambers 1–3",
        reference=f"{OLSEN}, p.93",
    ),
    SourcedFiring(
        kiln="Olsen's Hollyweird tube (anagama type)",
        fuel="wood",
        time='a "normal" firing 60 h, held at cone 11-plus 35–40 h in the front chamber, '
        "10–15 h in the back",
        reference=f"{OLSEN}, p.117",
    ),
    SourcedFiring(
        kiln="Mr Kato's coal downdraft, about 250 ft³",
        fuel="coal",
        time="over 50 h to 2372 °F, cooled three days or more",
        notes="slow because of the very thick walls and only two fireboxes",
        reference=f"{OLSEN}, p.131",
    ),
    SourcedFiring(
        kiln="Jun Kaneko's car kiln, 8 × 9 × 8 ft",
        fuel="gas, 32 atmospheric burners",
        time='"fired extremely slowly, allowing for a long soaking rise in temperature over '
        'several days, depending upon the size of the pieces being fired"',
        reference=f"{OLSEN}, p.172",
    ),
    SourcedFiring(
        kiln="Tobe climbing kiln, largest chamber 25 × 10 × 10 ft",
        fuel="wood",
        time="not given",
        used='"40 tons of wood to fire" (the chamber or the whole kiln: unclear)',
        reference=f"{OLSEN}, p.90",
    ),
    SourcedFiring(
        kiln="Anagamas (University of Montevallo; Buck Creek; a forum report)",
        fuel="wood",
        time="4–5 days where given",
        used="14 cords a firing; 10 cords over 4 days; about 6 cords over 5 days (1 cord about "
        "128 ft³, 2,000–3,000 lb)",
        reference="combustion-and-masonry.md §5.3 [S49]",
    ),
    SourcedFiring(
        kiln="A small conventional wood kiln",
        fuel="wood",
        time="24–48 h",
        used='"a cord or more"',
        reference="combustion-and-masonry.md §5.3 [S48] (a patent's background)",
    ),
)


class SlowFiring(BaseModel):
    """A firing over the time the user chose, and the sources' slow firings beside it."""

    model_config = ConfigDict(frozen=True)

    hours: float
    soak_h: float
    top_c: float
    rate_c_per_h: float
    firing: FiringResult | None  # None for a kiln the engine can't simulate (wood, coal, oil)
    quickest: FiringResult | None  # the design's own (or default) schedule, for comparison
    walls_share: float | None
    ware_share: float | None
    shell_share: float | None
    sources: list[SourcedFiring]
    working: list[Step]
    findings: list[Finding]


def slow_schedule(kiln: Kiln, hours: float, soak_h: float = 0.0) -> tuple[list[Ramp], float, float]:
    """A constant rise from the room to the top in ``hours − soak_h``, then the soak there: the
    schedule, the top (°C) and the rate (°C/h)."""
    top = si(top_temperature(kiln)[0], "degC")
    room = si(kiln.site.ambient, "degC")
    rate = (top - room) / (hours - soak_h)
    ramps = [
        Ramp(
            to=Q_(top, "degC"),
            rate=Q_(rate, "delta_degC/hour"),
            hold=Q_(soak_h, "hour") if soak_h > 0 else None,
        )
    ]
    return ramps, top, rate


def slow_firing(kiln: Kiln, hours: float, soak_h: float = 0.0) -> SlowFiring:
    """Fire ``kiln`` to its top over ``hours``, the last ``soak_h`` of them held at the top."""
    if hours <= 0:
        raise SimulationError("the firing time must be more than zero")
    if soak_h < 0 or soak_h >= hours:
        raise SimulationError("the soak must be at least zero and shorter than the firing")
    if hours > LONGEST_FIRING_H + 1e-9:
        raise SimulationError(
            f"{hours:g} h is longer than any sourced firing: the longest is Bizen's, seven days "
            f"and about three days' cooling, {LONGEST_FIRING_H:g} h ({LONGEST_FIRING_SOURCE})"
        )
    unit = "degF" if kiln.units == "us" else "degC"
    ramps, top, rate = slow_schedule(kiln, hours, soak_h)
    working = [
        Step(
            name="Slow firing schedule",
            value=(
                f"{show(Q_(rate, 'delta_degC/hour'), 'delta_' + unit + '/hour', 3)} from the room "
                f"to {show(Q_(top, 'degC'), unit)}"
                + (f", then {soak_h:g} h at the top" if soak_h else "")
            ),
            formula="rate = (T_top − T_room) / (t − t_soak)",
            inputs={
                "t": f"{hours:g} h",
                "t_soak": f"{soak_h:g} h",
                "T_top": show(Q_(top, "degC"), unit),
                "T_room": show(kiln.site.ambient, unit),
            },
            note=(
                "The user's choice of time; a constant rise is the simplest schedule. Give "
                "firing.schedule for a shaped one (preheat, holds). The top is the cone's at the "
                "design's final rate; Orton's tables bend a cone at a lower temperature when it "
                "is fired slower, so a long firing may need less."
            ),
            reference="the author, 30 October 2026: firing speed is the user's choice",
        )
    ]
    findings: list[Finding] = []
    sources = list(SOURCED)
    fire = kiln.heat.fire
    if fire is not None and fire.purpose == "heat":
        findings.append(
            Finding(
                level="info",
                message=(
                    "Wood, coal and oil firings aren't simulated yet (milestone M7: no wood "
                    "combustion source), so this kiln's slow firing isn't worked out. The sources' "
                    "slow firings and the wood they burnt are given to compare."
                ),
                reference="slow-firing.md",
            )
        )
        return SlowFiring(
            hours=hours, soak_h=soak_h, top_c=top, rate_c_per_h=rate, firing=None,
            quickest=None, walls_share=None, ware_share=None, shell_share=None,
            sources=sources, working=working, findings=findings,
        )  # fmt: skip
    slow = simulate(kiln, schedule=ramps, record=False).result
    quick = simulate(kiln, record=False).result
    energy = slow.energy_kwh
    walls = slow.walls_kwh / energy if energy > 0 else None
    ware = slow.ware_kwh / energy if energy > 0 else None
    shell = slow.shell_kwh / energy if energy > 0 else None
    working.append(
        Step(
            name="Where the heat goes",
            value=(
                f"{slow.energy_kwh:,.0f} kWh put in over {slow.duration_h:.1f} h, against "
                f"{quick.energy_kwh:,.0f} kWh in {quick.duration_h:.1f} h on the quickest schedule"
            ),
            formula="heat put in = into the walls + into the ware; of it, lost from the shell",
            inputs={
                "into the walls": f"{slow.walls_kwh:,.0f} kWh (quickest {quick.walls_kwh:,.0f})",
                "into the ware": f"{slow.ware_kwh:,.0f} kWh (quickest {quick.ware_kwh:,.0f})",
                "lost from the shell": f"{slow.shell_kwh:,.0f} kWh "
                f"(quickest {quick.shell_kwh:,.0f})",
            },
            reference="simulation.py (ADR 0015)",
            note=(
                "The walls' heat is their store plus what passes through them to the shell; the "
                "shell's loss grows with the time, the walls' store and the ware's don't."
            ),
        )
    )
    if slow.cost is not None and quick.cost is not None:
        working.append(
            Step(name="Cost of the firing", value=f"{slow.cost} (quickest {quick.cost})")
        )
    if shell is not None:
        findings.append(
            Finding(
                level="info",
                message=(
                    f"Over {slow.duration_h:.0f} h the shell loses {shell:.0%} of the heat put "
                    f"in ({slow.shell_kwh:,.0f} kWh, against {quick.shell_kwh:,.0f} kWh on the "
                    f"quickest schedule, {quick.duration_h:.1f} h). In a long firing the shell's "
                    "loss is what grows: more insulation outside cuts it, and the walls' store is "
                    f"paid once. Olsen's Bizen kiln is built for {BIZEN_AIM} (p.99)."
                ),
                reference=f"{OLSEN}, p.99; simulation.py",
            )
        )
    if not slow.completed:
        sheet = Sheet(
            "firing.reaches-top", "The kiln's heat reaches the top", reference="simulation.py"
        )
        sheet.given("T_r", "the hottest the simulated firing reaches",
                    Q_(slow.reached_c, "degC"), unit, source="simulation.py")  # fmt: skip
        sheet.given("T_top", "the top: the cone's temperature at the final rate",
                    Q_(top, "degC"), unit, source="the design: firing.cone")  # fmt: skip
        sheet.require("T_r", ">=", "T_top", level="warning")
        findings.append(
            Finding.failed(
                sheet.check(),
                message=(
                    f"The kiln doesn't reach the top on its own heat: it gets to "
                    f"{show(Q_(slow.reached_c, 'degC'), unit)} of "
                    f"{show(Q_(top, 'degC'), unit)}. More heat or more insulation is needed "
                    "whatever the firing time."
                ),
            )
        )
    elif not slow.held:
        findings.append(
            Finding(
                level="info",
                message=(
                    "The heat can't keep this pace all the way, so the firing takes "
                    f"{slow.duration_h:.1f} h, not {hours:g} h."
                ),
            )
        )
    findings += [f for f in slow.findings if f.level != "info"]
    return SlowFiring(
        hours=hours,
        soak_h=soak_h,
        top_c=top,
        rate_c_per_h=rate,
        firing=slow,
        quickest=quick,
        walls_share=walls,
        ware_share=ware,
        shell_share=shell,
        sources=sources,
        working=working,
        findings=findings,
    )


__all__ = ["SOURCED", "SlowFiring", "SourcedFiring", "slow_firing", "slow_schedule"]
