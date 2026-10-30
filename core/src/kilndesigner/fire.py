"""Wood, coal and oil firing: the fireboxes, and the chimney that draws them.

A fire in a firebox has no gas pressure behind it: the chimney does the work (natural draft),
unless a blower drives an oil burner (forced draft). So the chimney and the fireboxes are sized
together, by Olsen's rules (*The Kiln Book*, 4th ed.):

- **Chimney height**: Rule 5, 3 ft per ft of downward pull plus 1 ft per 3 ft of horizontal pull
  (p.80), is the most; the early Far-East proportions, a chimney twice the chamber's height, the
  least (p.130, Fig. 5-2). His groundhogs' 5–10 ft chimneys on 29–48 in chambers sit between them
  (p.112). A fast-fire kiln's pull counts its firebox (p.140). A climbing kiln's slope draws, and
  Rule 5 doesn't cover it: its chimney reaches at least the line through its chamber tops (p.81);
  the Bizen kiln's is about 3 × its total rise (p.101). Forced draft needs about a quarter less
  (p.79, p.130); above about 4000 ft, 30 % more (p.81, p.140).
- **Chimney section**: a wood kiln's grate about 7 × the chimney's section (10 × in his first rule,
  4 × in groundhogs; p.76–77); the exit flues a little smaller than the chimney where they enter it
  (p.78).
- **Coal**: 1 ft² of grate per 6–8 ft² of floor (p.206). **Oil**: 1 ft² of combustion area per
  5 ft² of floor (p.213); 132,000 BTU per gallon of #2 diesel (p.214).

The chimney is a tuning part: Olsen builds it to be raised, lowered and dampered (p.81). So the
rules here warn only past the edge of what he states and builds.
"""

from __future__ import annotations

import math

from pydantic import BaseModel, ConfigDict

from kilndesigner.fire_checks import (
    AUXILIARY_AIR,
    CLIMBING,
    COAL,
    GRATE,
    OIL,
    RULE_5,
    Pull,
    chimney_height,
    floor_ratio,
    grate_ratio,
)
from kilndesigner.heatloss import top_temperature
from kilndesigner.model import Dome, Firebox, Kiln, Port, Section, SprungArch
from kilndesigner.units import Q_, Quantity, si
from kilndesigner.working import Finding, Step, show

OIL_BTU_PER_GAL = 132_000  # #2 diesel at 100 psi (Olsen p.214)
GRATE_TO_CHIMNEY = 7.0  # what Olsen now uses (p.77)
GRATE_RANGE = (4.0, 10.0)  # groundhogs (p.77) to his first rule (p.76)
FLUE_INTO_CHIMNEY = 0.75  # the exit flues' entry into the chimney: 3 bricks into 4 (p.78)
COAL_FLOOR_PER_GRATE = 8.0  # the most floor per ft² of coal grate (p.76, p.206)
OIL_FLOOR_PER_AREA = 5.0  # floor per ft² of oil combustion area (p.213)
HIGH_FT = 4000.0  # above about this, chimney and flues grow (p.81, p.140)
STACK_C = 0.0342  # K/m, stack-effect equation [S42]
PA_PER_IN_WC = 249.09
DRAFT_SOURCE = "Stack effect, ΔP = 0.0342·a·h·(1/To − 1/Ti); combustion-and-masonry.md §4.2 [S42]"
FUEL_WORDS = {"wood": "wood", "coal": "coal", "oil": "oil"}


class FireDesign(BaseModel):
    model_config = ConfigDict(frozen=True)

    fuel: str
    fireboxes: list[str]
    grate_area: str | None
    grate_area_in2: float | None
    chimney_height: str | None
    chimney_height_in: float | None
    chimney_range: str | None
    chimney_area_in2: float
    flue_area: str
    flue_area_in2: float
    inlet_area_in2: float | None
    full_fire_btu_hr: float
    """An oil kiln's burners at full fire; 0 for wood and coal, whose rate is the stoker's."""
    draft: list[str]
    working: list[Step]
    findings: list[Finding]


def _port_in2(port: Port) -> float:
    w, h = port.size_in()
    return math.pi * w * w / 4 if port.round else w * h


def _describe(fb: Firebox) -> str:
    where = "under the floor" if fb.position == "under" else f"at the {fb.position} wall"
    size = f"{si(fb.width, 'in'):g} × {si(fb.length, 'in'):g} in"
    grate = (
        f", a {si(fb.grate.width, 'in'):g} × {si(fb.grate.length, 'in'):g} in grate"
        if fb.grate is not None
        else ", fired on its floor"
    )
    return f"{fb.count} × {size} {where}{grate}"


def _brick_section(area: float) -> tuple[float, float]:
    """The smallest chimney section of whole half-bricks (4½ in steps), no more than 2 : 1, that
    gives ``area`` in²; Olsen rounds up to brick sizes (p.77)."""
    sizes = [4.5 * n for n in range(1, 2 + math.ceil(math.sqrt(max(area, 1)) / 4.5) * 2)]
    return min(
        ((p, q) for p in sizes for q in sizes if p <= q <= 2 * p and p * q >= area),
        key=lambda pq: (pq[0] * pq[1], pq[1]),
    )


def _along_the_flow(inside: Section, flue_wall: str) -> float:
    """A chimney's inside size the way the gases cross it: front to back (its depth) behind a
    front or back flue wall, side to side (its width) beside a left or right one (in)."""
    if inside.diameter is not None:
        return si(inside.diameter, "in")
    assert inside.width is not None
    assert inside.depth is not None
    return si(inside.depth if flue_wall in ("front", "back") else inside.width, "in")


def inside_height(kiln: Kiln) -> float:
    """From the chamber floor to the top inside (in): the crown of an arch or dome."""
    h = si(kiln.chamber.height, "in")
    if isinstance(kiln.roof, SprungArch | Dome):
        h += si(kiln.roof.rise, "in")
    return h


def pull(kiln: Kiln, fireboxes: list[Firebox], forced: bool, chimney: float = 0.0) -> Pull:
    """The pull a natural-draft chimney's height comes from (Olsen p.80, p.140, p.81). The
    horizontal pull runs through the chamber, the flue wall, the run and the chimney's own width
    (``chimney``, in), as in Olsen's example: 5 + 1 + 1 ft (p.80, Fig. 3-14)."""
    c = kiln.chamber
    draft = kiln.draft
    down = inside_height(kiln)
    under = [
        si(fb.height, "in") + (si(fb.ash_pit, "in") if fb.ash_pit is not None else 0.0)
        for fb in fireboxes
        if fb.position == "under" and fb.height is not None
    ]
    if under:  # a fast-fire kiln pulls down through its fireboxes too (p.140)
        down += max(under)
    wall = draft.flue_wall if draft is not None else "back"
    along = si(c.length, "in") if wall in ("front", "back") else si(c.width, "in")
    flue_wall = sum(si(x.thickness, "in") for x in kiln.lining.for_face(wall))
    run = si(draft.run_to_chimney, "in") if draft is not None else 0.0
    across = along + flue_wall + run + chimney
    slope = si(c.slope, "radian") if c.slope is not None else 0.0
    rise = math.tan(slope) * (si(c.length, "in") + flue_wall + run)
    high = kiln.site.elevation is not None and si(kiln.site.elevation, "ft") >= HIGH_FT
    return Pull(down if rise == 0 else inside_height(kiln), across, rise, forced, high)


def _draft(kiln: Kiln, height_in: float, top: Quantity, working: list[Step]) -> list[str]:
    from kilndesigner.gas import air_pressure

    to = si(kiln.site.ambient, "K")
    a = air_pressure(si(kiln.site.elevation, "m") if kiln.site.elevation is not None else 0.0)
    lines: list[str] = []
    temp_unit = "degF" if kiln.units == "us" else "degC"
    for label, flue in (("flue gas at 1000 °F", Q_(1000, "degF")), ("flue gas at top", top)):
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
                reference=DRAFT_SOURCE,
            )
        )
    return lines


def design_fire(kiln: Kiln) -> FireDesign:
    fire = kiln.heat.fire
    if fire is None:
        raise ValueError("the kiln has no fireboxes")
    findings: list[Finding] = []
    working: list[Step] = []
    fuel = FUEL_WORDS[fire.fuel]
    top, _ = top_temperature(kiln)

    # The fireboxes
    boxes = [_describe(fb) for fb in fire.fireboxes]
    grates = [fb for fb in fire.fireboxes if fb.grate is not None]
    grate_in2 = (
        sum(
            fb.count * si(fb.grate.width, "in") * si(fb.grate.length, "in")
            for fb in grates
            if fb.grate is not None
        )
        if grates
        else None
    )
    floor_in2 = sum(fb.count * si(fb.width, "in") * si(fb.length, "in") for fb in fire.fireboxes)
    inlets = [fb for fb in fire.fireboxes if fb.inlet is not None]
    inlet_in2 = (
        sum(fb.count * fb.inlets * _port_in2(fb.inlet) for fb in inlets if fb.inlet is not None)
        if len(inlets) == len(fire.fireboxes)
        else None
    )
    working.append(
        Step(
            name="Fireboxes",
            value="; ".join(boxes),
            inputs={
                "floor, all fireboxes": f"{floor_in2:,.0f} in²",
                **({"grate, all fireboxes": f"{grate_in2:,.0f} in²"} if grate_in2 else {}),
                **({"inlet flues into the chamber": f"{inlet_in2:,.0f} in²"} if inlet_in2 else {}),
            },
        )
    )
    full_fire = 0.0
    if fire.fuel == "oil" and fire.oil_burners is not None and fire.oil_rate is not None:
        gph = si(fire.oil_rate, "gallon/hour")
        full_fire = fire.oil_burners * gph * OIL_BTU_PER_GAL
        working.append(
            Step(
                name="Oil at full fire",
                value=f"{full_fire:,.0f} BTU/hr",
                formula="burners × gallons an hour × 132,000 BTU/gal",
                inputs={"burners": str(fire.oil_burners), "each": f"{gph:g} gal/hr"},
                reference="Olsen, The Kiln Book, 4th ed., p.214 (#2 diesel at 100 psi)",
            )
        )

    # The chimney's section: as built, or Olsen's 7 : 1 from the grate (or the firebox floor)
    draft = kiln.draft
    built = draft.chimney if draft is not None else None
    feed = grate_in2 if grate_in2 is not None else floor_in2
    if built is not None and built.inside is not None:
        chimney_in2 = built.inside.area_in2()
        section_note = "as built"
        chimney_along = _along_the_flow(built.inside, draft.flue_wall if draft else "back")
    else:
        a, b = _brick_section(feed / GRATE_TO_CHIMNEY)
        chimney_in2 = a * b
        section_note = f"{a:g} × {b:g} in: the {'grate' if grate_in2 else 'firebox floor'} ÷ 7"
        chimney_along = a
    working.append(
        Step(
            name="Chimney's section at the base",
            value=f"{chimney_in2:,.0f} in²",
            inputs={"how": section_note},
            reference=GRATE,
        )
    )
    flue_in2 = (
        _port_in2(draft.flue_port)
        if draft is not None and draft.flue_port is not None
        else FLUE_INTO_CHIMNEY * chimney_in2
    )

    # Fuel by fuel: wood's grate against the chimney, coal's grate or oil's area against the floor
    floor = si(kiln.chamber.width, "in") * si(kiln.chamber.length, "in")
    if kiln.chamber.shape == "round":
        floor = math.pi / 4 * si(kiln.chamber.width, "in") ** 2
    # The grate's ratio is for draft kilns (p.77, Fig. 3-8): an updraft's chimney, such as a
    # bottle kiln's hood over its whole dome, isn't the throat the fire draws through
    pulled = draft is not None and draft.type != "up"
    if fire.fuel == "wood" and pulled and built is not None and built.inside is not None:
        what = "the grate, all fireboxes" if grate_in2 else "the firebox floor, all fireboxes"
        sheet = grate_ratio(feed, chimney_in2, what, GRATE_RANGE)
        if (check := sheet.check()).status != "pass":
            ratio = feed / chimney_in2
            findings.append(
                Finding.failed(
                    check,
                    message=(
                        f"The {'grate' if grate_in2 else 'firebox floor'} is {ratio:.1f} times the "
                        "chimney's section, outside the 4–10 times Olsen's wood kilns span (about "
                        "7 now, 4 in groundhogs). The chimney may pull too hard or too little for "
                        "the fire."
                    ),
                )
            )
    elif fire.fuel == "coal":
        sheet = floor_ratio(
            grate_in2 or floor_in2, floor, "grate", COAL_FLOOR_PER_GRATE, COAL, "fire.coal-grate"
        )
        if (check := sheet.check()).status != "pass":
            findings.append(
                Finding.failed(
                    check,
                    message=(
                        "The coal grates are under 1 ft² per 8 ft² of floor, the least Olsen gives "
                        "(1 per 6–8)."
                    ),
                )
            )
    elif fire.fuel == "oil":
        sheet = floor_ratio(
            floor_in2, floor, "combustion area", OIL_FLOOR_PER_AREA, OIL, "fire.oil-area"
        )
        if (check := sheet.check()).status != "pass":
            findings.append(
                Finding.failed(
                    check,
                    message=(
                        "The oil fireboxes give under 1 ft² of combustion area per 5 ft² of floor, "
                        "Olsen's figure."
                    ),
                )
            )

    # The chimney's height
    chimney_text: str | None = None
    chimney_in: float | None = None
    span_text: str | None = None
    lines: list[str] = []
    if draft is not None and draft.type in ("cross", "down"):
        p = pull(kiln, fire.fireboxes, fire.forced, chimney_along)
        allow = (0.75 if p.forced else 1) * (1.3 if p.high else 1)
        if p.rise > 0:
            # A climbing kiln's slope draws, and Rule 5 doesn't cover it (p.81): at least the line
            # through the chamber tops; Fujiwara's Bizen chimney, about 3 × the rise (p.101)
            least = (p.rise + p.down) * allow
            most = max(3 * p.rise * allow, least)
            proposed = least
        else:
            least = 2 * p.down * allow  # p.130, Fig. 5-2
            most = (3 * p.down + p.across / 3) * allow  # Rule 5, p.80
            proposed = most
        chimney_in = si(built.height, "in") if built is not None else proposed
        chimney_text = f"{chimney_in / 12:.1f} ft ({chimney_in:.0f} in) above the chamber floor"
        span_text = f"{least / 12:.1f}–{most / 12:.1f} ft"
        working.append(
            Step(
                name="Chimney height",
                value=chimney_text,
                formula=(
                    "least: the line through the chamber tops (p.81); most: 3 × the total rise "
                    "(p.101)"
                    if p.rise > 0
                    else "least 2 × downward pull (p.130, Fig. 5-2); most 3 × downward pull + ⅓ "
                    "× horizontal pull (Rule 5, p.80)"
                ),
                inputs={
                    "downward pull": f"{p.down:.1f} in",
                    "horizontal pull": f"{p.across:.1f} in",
                    **({"total rise": f"{p.rise:.1f} in"} if p.rise > 0 else {}),
                    "range": span_text,
                    **({"forced draft": "× 0.75"} if p.forced else {}),
                    **({"altitude": "× 1.3"} if p.high else {}),
                },
                reference=RULE_5,
                note=(
                    "Build it to be tuned: add or take off brick, and damper it. 'If the chimney "
                    "seems too tall, it probably is' (p.80). The height is measured from the "
                    "chamber floor. Sources disagree on horizontal pull: Olsen and Ward add ⅓ ft "
                    "of chimney per foot, Rhodes 2 ft (kiln-hardware.md, conflict on horizontal "
                    "pull); Olsen's is used, as ADR 0014 takes his built kilns as the reference."
                ),
            )
        )
        # Wood beside gas: the gas may let the chimney be cut down, but then the wood needs an
        # auxiliary air source (Olsen p.79)
        with_gas = kiln.heat.gas is not None and fire.fuel == "wood"
        sheet = chimney_height(p, chimney_in, built is not None, with_gas)
        sheet.agrees("H_min", Q_(least, "in"))
        if (check := sheet.check()).status != "pass":
            findings.append(
                Finding.failed(
                    check,
                    message=(
                        f"This kiln burns wood with its gas, and its chimney, "
                        f"{chimney_in / 12:.1f} ft, is under the {least / 12:.1f} ft the wood "
                        "needs to draw its own air. Olsen: 'If a combination of wood is also to "
                        "be used, then you must provide an auxillary air source' (p.79). Give "
                        f"the wood a blower (fire.forced), or build the chimney to "
                        f"{least / 12:.1f} ft."
                        if with_gas and not fire.forced
                        else f"The chimney is {chimney_in / 12:.1f} ft, under the "
                        f"{least / 12:.1f} ft Olsen's rules give as the least for this kiln: it "
                        "may not draw the fire hard enough to reach the top."
                    ),
                )
            )
        elif chimney_in > most * (1 + 1e-9):
            rule = "3 × the kiln's rise" if p.rise > 0 else "Rule 5"
            findings.append(
                Finding(
                    level="info",
                    message=(
                        f"The chimney, {chimney_in / 12:.1f} ft, is taller than the "
                        f"{most / 12:.1f} ft Olsen's rules give as the most ({rule}): too tall a "
                        "chimney pulls heat out and fires unevenly (p.80–81). Damper it, or take "
                        "some off."
                    ),
                    reference=CLIMBING if p.rise > 0 else RULE_5,
                )
            )
        if with_gas and not fire.forced and check.status == "pass":
            findings.append(
                Finding(
                    level="info",
                    message=(
                        "This kiln burns wood with its gas, so its chimney is sized to draw the "
                        "wood. With gas under pressure it could be at least 25 % shorter, but "
                        "then the wood needs an auxiliary air source, a blower (p.79)."
                    ),
                    reference=AUXILIARY_AIR,
                )
            )
        lines = _draft(kiln, chimney_in, top, working)
    elif draft is not None and draft.type == "up":
        findings.append(
            Finding(
                level="info",
                message=(
                    "An updraft's gases rise straight through the setting to the flues in its "
                    "roof: Olsen's Rule 5 is for kilns that pull down or across, so no chimney "
                    "height is worked out here."
                ),
                reference=RULE_5,
            )
        )
    findings.append(
        Finding(
            level="info",
            message=(
                "Fireboxes are laid out in brick in the masonry, plans and 3D model; their "
                f"{fuel} use per firing waits for the client's kiln (plan milestone M7)."
            ),
        )
    )
    return FireDesign(
        fuel=fuel,
        fireboxes=boxes,
        grate_area=f"{grate_in2:,.0f} in²" if grate_in2 is not None else None,
        grate_area_in2=grate_in2,
        chimney_height=chimney_text,
        chimney_height_in=chimney_in,
        chimney_range=span_text,
        chimney_area_in2=chimney_in2,
        flue_area=f"{flue_in2:.0f} in²",
        flue_area_in2=flue_in2,
        inlet_area_in2=inlet_in2,
        full_fire_btu_hr=full_fire,
        draft=lines,
        working=working,
        findings=findings,
    )


__all__ = ["FireDesign", "design_fire", "inside_height", "pull"]
