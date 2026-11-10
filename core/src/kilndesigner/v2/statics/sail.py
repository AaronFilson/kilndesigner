"""A dome over a square, oblong or curved plan (a sail dome) on its walls, by Heyman's slicing,
cold and hot.

The engine's dome over a box or a curved plan (`outline.SphereDome`; `geometry._dome_parts`,
`run_parts._dome`) is the sphere through the plan's farthest point from its crown, ``rise`` above
the springline there; the walls' tops are filled up to its inside (their caps) and the dome's shell
is laid over the whole plan. So the dome rests on all its walls, along curves that rise from the
springline where the plan reaches farthest to their highest over each wall's middle: it needs no
force pattern to its corners, its walls carry it all round.

**Slicing.** Vertical planes square to the plan's width cut the shell into strips, each an arch
across the width from wall to wall: "the central surface ... divided into a series of independent
parallel arches" (Intrigila, Nodargi & Bisegna, SAHC 2020 §1, on Heyman's technique for domes and
cross vaults; `masonry-statics.md` [M7]). By the safe theorem a state in which every strip stands
on its own, the strips pressing nothing on each other, is a state of the whole dome: "if a thrust
surface is found that lies within one lune, then stability is satisfied for the 'original
undivided structure'" (Heyman 1977 p.109, via Lau 2006 p.35). A lower bound: the dome may stand
where a strip alone can't.

A vertical plane cuts a spherical shell in a ring of uniform thickness, between circles of radius
√(R² − v²) and √((R + T)² − v²) about the sphere's centre, v the plane's distance from it (Derived).
Each strip is that ring between its walls' inner faces, springing where the sphere meets them (on
the caps), on its two walls in 2½ in courses, the layers over the shell its load (the design's
``acting_ring``); the walls are held by a buttress against their whole outer faces, the dome
kilns' walls all being buttressed (the frame's angles run along straight walls only, so a dome is
held by masonry in the design file), its demand computed. Every strip is solved by the LP of
`rigid.py`; the strips nearest the walls' middles and the farthest points decide.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from kilndesigner.form import crown_of, plan_of
from kilndesigner.model import Dome, Kiln
from kilndesigner.outline import Outline, SphereDome, half_width, rectangle
from kilndesigner.units import Q_, si
from kilndesigner.v2.statics import sources
from kilndesigner.v2.statics.arch import VOUSSOIR, ArchRing, Overburden, on_walls
from kilndesigner.v2.statics.rigid import Problem, Section, Status, assemble, force_on, solve
from kilndesigner.v2.statics.section import BUTTRESS, METHOD, NotModelledError, State
from kilndesigner.working import Step, show

STRIPS = 16
"""Strips across each dome: a strip at the middle of each sixteenth of its run, and one at each
end, by the walls' inside faces."""

SLICING = (
    "Heyman's slicing: the shell cut into independent parallel arches (Intrigila, Nodargi & "
    "Bisegna, SAHC 2020 §1, masonry-statics.md [M7]); the whole stands if each slice does "
    "(Heyman 1977 p.109, via Lau 2006 p.35)"
)


@dataclass(frozen=True)
class SphereShell:
    """One dome: its plan, the sphere's centre (plan x, y and height, m), its inside radius, the
    springline, the shell's acting thickness and the layers over it (thickness, density)."""

    plan: Outline
    centre: tuple[float, float, float]
    radius: float
    springline: float
    thickness: float
    over: tuple[tuple[float, float], ...]


def not_modelled(kiln: Kiln) -> str | None:
    """Why this kiln's dome isn't sliced here, or None."""
    roof, c = kiln.roof, kiln.chamber
    if not isinstance(roof, Dome):
        return f"a sail dome is a dome; this roof is {roof.type}"
    if c.shape == "round":
        return "a dome over a round plan is a dome of revolution (dome.py)"
    if len({layer.material for layer in kiln.lining.walls}) > 1:
        return "walls of several materials under a sail dome aren't built"
    acting = kiln.lining.for_face("roof")[: roof.acting_ring]
    if len({layer.material for layer in acting}) > 1:
        return "a shell of bonded layers of different materials isn't sliced yet"
    return None


def shells(kiln: Kiln) -> list[SphereShell]:
    """Each dome of the kiln (one a chamber in a row), in metres."""
    roof = kiln.roof
    assert isinstance(roof, Dome)
    layers = kiln.lining.for_face("roof")
    acting = sum(si(x.thickness, "m") for x in layers[: roof.acting_ring])
    over = tuple((si(x.thickness, "m"), sources.density(x.material))
                 for x in layers[roof.acting_ring :])  # fmt: skip
    c = kiln.chamber
    if c.outline is not None:
        plan = plan_of(kiln, "m")
        crown = crown_of(kiln, "m")
        dome = SphereDome(plan, si(roof.rise, "m"), crown)
        h = si(c.height, "m")
        centre = (crown[0], crown[1], h + dome.rise - dome.radius)
        return [SphereShell(plan, centre, dome.radius, h, acting, over)]
    from kilndesigner.run_parts import run_layout

    run = run_layout(kiln)
    out: list[SphereShell] = []
    for i in range(c.chambers):
        rise = run.sizes[i][2] if run.sizes else si(roof.rise, "mm")
        at = run.centre(i) * 1e-3
        plan = rectangle(run.width * 1e-3, run.depth_of(i) * 1e-3, (0.0, at))
        dome = SphereDome(plan, rise * 1e-3, (0.0, at))
        springline = run.springline(i) * 1e-3
        out.append(SphereShell(plan, (0.0, at, springline + dome.rise - dome.radius),
                               dome.radius, springline, acting, over))  # fmt: skip
    return out


@dataclass(frozen=True)
class Strip:
    """A strip of a dome at ``at`` along its run (m): its ring, where it springs (m above the
    floor) and the section on its walls."""

    at: float
    ring: ArchRing
    springing: float
    section: Section


def strips(kiln: Kiln, shell: SphereShell, n: int = STRIPS) -> list[Strip]:
    """The dome's strips across its width, a metre deep each (forces per metre of wall)."""
    wall = sum(si(x.thickness, "m") for x in kiln.lining.walls)
    rho_wall = sources.density(kiln.lining.walls[0].material)
    rho = sources.density(kiln.lining.for_face("roof")[0].material)
    _, _, y0, y1 = shell.plan.bounds
    eps = 1e-4 * (y1 - y0)
    ats = [y0 + eps, *(y0 + (y1 - y0) * (k + 0.5) / n for k in range(n)), y1 - eps]
    _, cy, cz = shell.centre
    r, t = shell.radius, shell.thickness
    out: list[Strip] = []
    for at in ats:
        v = at - cy
        hw = half_width(shell.plan, at)
        r_in = math.sqrt(max(r * r - v * v, 0.0))
        if hw <= 1e-6 or hw >= r_in:
            continue  # the plan's tip, or the sphere not over the plan's width there
        r_out = math.sqrt((r + t) ** 2 - v * v)
        over: list[Overburden] = []
        rim = r + t
        for thick, density in shell.over:
            outer = math.sqrt((rim + thick) ** 2 - v * v)
            over.append(Overburden(outer - math.sqrt(rim * rim - v * v), density))
            rim += thick
        phi = math.asin(hw / r_in)
        ring = ArchRing(r_in, r_out - r_in, phi, rho, 1.0, 40, tuple(over))
        springing = cz + math.sqrt(r_in * r_in - hw * hw)
        courses = max(1, round(springing / sources.COURSE.value))
        sec = on_walls(ring, wall, springing, rho_wall, courses, BUTTRESS)
        out.append(Strip(at, ring, springing, sec))
    return out


def conditions(kiln: Kiln, sec: Section, state: State, analogy: bool = True) -> Problem:
    """μ cold or hot at the masonry's joints, 0 where it meets the buttress (unsourced, the band's
    low end); hot, the crushing stand-in of the shell's and the walls' materials."""
    mu = sources.MU_COLD.value if state == "cold" else sources.MU_HOT.value
    shell_mat = kiln.lining.for_face("roof")[0].material
    wall_mat = kiln.lining.walls[0].material

    def stand_in(tag: str) -> float | None:
        m = shell_mat if tag == VOUSSOIR else wall_mat if tag.startswith(("wall", "skew")) else None
        if m is None or (not analogy and sources.by_analogy(m)):
            return None
        s = sources.crushing(m)
        return None if s is None else s.value

    mus: list[float] = []
    crush: list[float | None] = []
    for j in sec.joints:
        tags = (sec.bodies[j.a].tag, sec.bodies[j.b].tag)
        mus.append(0.0 if BUTTRESS in tags else mu)
        limits = [s for s in (stand_in(tag) for tag in tags) if s is not None]
        crush.append(min(limits) if limits and state == "hot" else None)
    return Problem(sec, tuple(mus), tuple(crush) if state == "hot" else ())


@dataclass(frozen=True)
class SailResult:
    """One state of a kiln's domes: whether every strip stands, the largest least push on the
    walls' buttress (N per metre of wall), whether a hot verdict rests on a stand-in by analogy,
    and the working."""

    state: State
    stands: bool
    least: float
    analogy: bool
    steps: tuple[Step, ...]


def analyse(kiln: Kiln, state: State) -> SailResult:
    why = not_modelled(kiln)
    if why is not None:
        raise NotModelledError(why)
    stands, rescued, least, count = True, True, 0.0, 0
    worst_at = math.nan
    for shell in shells(kiln):
        for s in strips(kiln, shell):
            count += 1
            p = conditions(kiln, s.section, state)
            cost = force_on(assemble(p), s.section, BUTTRESS, 0, outward=True)
            sol = solve(p, cost, 1)
            if sol.status is not Status.OPTIMAL:
                stands = False
                decided = conditions(kiln, s.section, state, analogy=False)
                rescued = (
                    rescued
                    and decided.crush != p.crush
                    and (solve(decided).status is Status.OPTIMAL)
                )
                continue
            if sol.value / 2 > least:
                least, worst_at = sol.value / 2, s.at
    analogy = not stands and rescued
    steps = _steps(kiln, state, count, stands, least, worst_at, analogy)
    return SailResult(state, stands, least if stands else math.nan, analogy, steps)


def _steps(
    kiln: Kiln, state: State, count: int, stands: bool, least: float, at: float, analogy: bool
) -> tuple[Step, ...]:
    roof = kiln.roof
    assert isinstance(roof, Dome)
    mu = sources.MU_COLD if state == "cold" else sources.MU_HOT
    lbft = si(Q_(least, "N/m"), "lbf/ft")
    steps = [
        Step(
            name=f"The dome in strips ({state})",
            value=f"{count} strips across the width, each a ring on its two walls: "
            + ("every one stands" if stands else "a strip has no admissible state"),
            formula="each strip the ring between √(R² − v²) and √((R + T)² − v²) about the "
            "sphere's centre, springing where the sphere meets the walls' inside faces; on its "
            "walls in 2½ in courses, a buttress against their outer faces",
            inputs={"rise": show(roof.rise, "inch"), "μ": f"{mu.value}"},
            reference=f"{SLICING}; {METHOD}",
            note=mu.note,
        ),
    ]
    if stands:
        steps.append(Step(
            name=f"The most any strip needs of the walls' buttress ({state})",
            value=f"{least:.4g} N/m ({lbft:.4g} lbf/ft) of wall, the strip "
            f"{show(Q_(at, 'm'), 'inch')} along the run",
            formula="minimise the outward force on the buttress for each strip (Heyman's minimum "
            "thrust); the largest of them",
            reference=METHOD,
        ))  # fmt: skip
    if analogy:
        steps.append(Step(
            name="The hot verdict rests on a stand-in by analogy",
            value="no admissible state with dense firebrick's 25 psi crushing stand-in, one "
            "without it: not given (ADR 0009)",
            reference=sources.C16_DENSE.reference,
            note=sources.C16_DENSE.note,
        ))  # fmt: skip
    return tuple(steps)
