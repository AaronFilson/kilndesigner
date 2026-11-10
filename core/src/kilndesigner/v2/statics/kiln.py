"""A kiln's statics in v2: every part of it the engine can cut and solve, cold and hot, and for
what it can't yet, the missing piece said plainly (ADR 0009) rather than a verdict on the kiln.

v2 flags nothing (ADR 0017, decision 3): the result is whether an admissible state exists in each
state, the forces on what holds the kiln, and the working. The reference kilns all stood and
worked for their builders (the user, 2026-11-10): where v2 says one can't stand, the model is
missing physics, and `missing` names it.

- **Sprung arches across the width**: the cross-section cut from the engine's solids
  (`section.py`), at each printed station where the width changes.
- **Arches along the draft**, a row of chambers or one chamber under an arch along its depth: the
  section along the row (`row.py`).
- **Catenary arches**: the ring along the engine's catenary on fixed feet (`arch.catenary_ring`).
- **Round domes on round walls**: rings of revolution with hoop compression (`dome.py`).
- **No roof**: free-standing walls under their own weight.
- Refused, each with its reason: crossing vaults, domes over square or curved plans, and fibre
  roofs hung in steel.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from kilndesigner.model import CatenaryArch, Dome, FlatRoof, Kiln, OpenTop, SprungArch
from kilndesigner.units import Q_, si
from kilndesigner.v2.statics import sources
from kilndesigner.v2.statics.arch import SUPPORT, catenary_ring
from kilndesigner.v2.statics.dome import kiln_dome, kiln_not_modelled
from kilndesigner.v2.statics.rigid import Problem, Status, assemble, force_on, solve
from kilndesigner.v2.statics.row import analyse as analyse_row
from kilndesigner.v2.statics.row import row_section
from kilndesigner.v2.statics.section import NotModelledError, analyse, cross_section, stations
from kilndesigner.working import Step

STATES = ("cold", "hot")


@dataclass(frozen=True)
class KilnStatics:
    """Whether the kiln stands in each state (None: not modelled), the numbers that matter
    (N/m, per metre run or of circumference), what is missing, and the working."""

    kind: str
    stands: dict[str, bool | None]
    numbers: dict[str, float] = field(default_factory=dict[str, float])
    missing: str | None = None
    steps: tuple[Step, ...] = ()

    @property
    def all_stand(self) -> bool | None:
        """True when every state stands, False when one doesn't, None when not modelled."""
        if any(v is None for v in self.stands.values()):
            return None
        return all(bool(v) for v in self.stands.values())


def statics(kiln: Kiln) -> KilnStatics:
    roof = kiln.roof
    if isinstance(roof, OpenTop):
        return _open(kiln)
    if isinstance(roof, FlatRoof):
        return _refused(
            "flat roof",
            "a flat roof here is fibre hung in a steel frame or a slab: not masonry the limit "
            "analysis takes; fibre anchoring is left out of v2 (ADR 0017)",
        )
    if isinstance(roof, CatenaryArch):
        return _catenary(kiln)
    if isinstance(roof, Dome):
        why = kiln_not_modelled(kiln)
        if why is not None:
            return _refused("dome", why)
        results = {s: kiln_dome(kiln, s) for s in STATES}
        return KilnStatics(
            "dome of revolution",
            {s: r.stands for s, r in results.items()},
            {f"springing push, {s}": r.thrust for s, r in results.items()},
            steps=tuple(step for r in results.values() for step in r.steps),
        )
    assert isinstance(roof, SprungArch)
    if roof.crossing is not None:
        return _refused(
            "crossing vault",
            "two vaults crossing in a groin carry their load to the corners in three dimensions: "
            "a force pattern (cross or fan; SAHC 2020 §4.3) or 3-D blocks are needed, not built",
        )
    if roof.along or (kiln.chamber.chambers > 1 and not roof.tube):
        return _row(kiln)
    try:
        return _cross_sections(kiln)
    except NotModelledError as e:
        return _refused("sprung arch", str(e))


def _refused(kind: str, why: str) -> KilnStatics:
    return KilnStatics(kind, dict.fromkeys(STATES), missing=why,
                       steps=(Step(name="Not modelled", value=why),))  # fmt: skip


ROW = "arches along the draft"
ANALOGY = (
    "dense brick's hot crushing: with the 25 psi stand-in carried over from IFB by analogy (a "
    "question for the user) there is no admissible state hot, without it one; real hot crushing "
    "and creep data, and the shell's temperature through its thickness, are to decide it"
)


def _row(kiln: Kiln) -> KilnStatics:
    """The section along a row of chambers, cold and hot; a hot verdict that rests only on a
    crushing stand-in carried over by analogy isn't given, the missing data said instead."""
    try:
        rs = row_section(kiln)
    except NotModelledError as e:
        return _refused(ROW, str(e))
    stands: dict[str, bool | None] = {}
    numbers: dict[str, float] = {}
    steps: list[Step] = []
    missing: str | None = None
    for state in STATES:
        r = analyse_row(rs, state)
        stands[state] = None if r.analogy else r.stands
        missing = ANALOGY if r.analogy else missing
        for end, v in r.least.items():
            numbers[f"least on the {rs.support} at the {end}, {state}"] = v
        for end, v in r.most.items():
            numbers[f"most on the {rs.support} at the {end}, hot"] = v
        steps += list(r.steps[len(rs.steps) :]) if steps else list(r.steps)
    return KilnStatics(ROW, stands, numbers, missing, tuple(steps))


def _cross_sections(kiln: Kiln) -> KilnStatics:
    stands: dict[str, bool | None] = {}
    numbers: dict[str, float] = {}
    steps: list[Step] = []
    sts = stations(kiln)
    for at, station in sts:
        xs = cross_section(station)
        where = f" at {at:.2f} m" if len(sts) > 1 else ""
        for state in STATES:
            r = analyse(xs, state)
            stands[state] = bool(stands.get(state, True)) and r.stands
            if xs.support != "none":
                numbers[f"least on the {xs.support}{where}, {state}"] = r.least
                if state == "hot":
                    numbers[f"most on the {xs.support}{where}, hot"] = r.most
            steps += list(r.steps[len(xs.steps) :]) if steps else list(r.steps)
    return KilnStatics("cross-section", stands, numbers, steps=tuple(steps))


def _catenary(kiln: Kiln) -> KilnStatics:
    layers = kiln.lining.for_face("roof")
    ring = layers[0]
    t = si(ring.thickness, "m")
    rho = sources.density(ring.material)
    span, height = si(kiln.chamber.width, "m"), si(kiln.chamber.height, "m")
    sec = catenary_ring(span, height, t, rho, 1.0, 40)
    stands: dict[str, bool | None] = {}
    numbers: dict[str, float] = {}
    for state in STATES:
        mu = (sources.MU_COLD if state == "cold" else sources.MU_HOT).value
        crush = sources.crushing(ring.material) if state == "hot" else None
        n = len(sec.joints)
        p = Problem(sec, (mu,) * n, (crush.value,) * n if crush is not None else ())
        sol = solve(p, force_on(assemble(p), sec, SUPPORT, 0, outward=True), 1)
        stands[state] = sol.status is Status.OPTIMAL
        numbers[f"least push at the feet, {state}"] = (
            sol.value / 2 if sol.status is Status.OPTIMAL else math.nan
        )
    steps = (
        Step(
            name="The catenary ring",
            value=f"{span:.3f} m wide at the floor, {height:.3f} m to the crown, "
            f"{ring.material} {t:.4f} m thick, 40 voussoirs on fixed feet",
            formula="z = h + a − a·cosh(x/a) (shape.CatenaryCurve); joints normal to the curve",
            reference="combustion-and-masonry.md §6.6; the LP of rigid.py",
            note="the layers over the ring left out (none on the reference kiln)"
            if len(layers) == 1 else "the layers over the ring left out",
        ),
        Step(
            name="An admissible state, cold and hot",
            value=", ".join(f"{s}: {'found' if v else 'none'}" for s, v in stands.items()),
            inputs={k: f"{v:.4g} N/m ({si(Q_(v, 'N/m'), 'lbf/ft'):.4g} lbf/ft)"
                    for k, v in numbers.items()},
        ),
    )  # fmt: skip
    return KilnStatics("catenary arch", stands, numbers, steps=steps)


def _open(kiln: Kiln) -> KilnStatics:
    """No roof: the walls stand on the ground under their own weight, every bed joint's
    resultant at its middle (a wall of level courses, nothing pushing it)."""
    walls = kiln.lining.walls
    height = si(kiln.chamber.height, "m")
    weight = sum(sources.density(x.material) * si(x.thickness, "m") for x in walls) * 9.80665
    steps = (
        Step(
            name="No roof: the walls under their own weight",
            value=f"the base bed joint carries {weight * height:.4g} N a metre of wall at its "
            "middle; nothing pushes the walls, so every bed joint's resultant is at its middle",
            formula="N = Σ ρ g t h; e = 0",
            note="what covers the setting each firing (shards, broken ware) is a load not modelled",
        ),
    )
    return KilnStatics("no roof", dict.fromkeys(STATES, True), {"base load": weight * height},
                       steps=steps)  # fmt: skip
