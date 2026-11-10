"""Zones in series from the design (ADR 0017 H1): a row of chambers and a tube cut into segments
as gas zones of one enclosure (`chamber.py`: the engine's own cells, `massing.cells`, joined
through the flue holes in the walls between chambers, `run_parts.flue_rows`), each wall between
two chambers a wall with a face in each (`kiln.heat_model`); and a **staged firing**, each chamber
stoked in turn (problem set §2.4): the fuel burns in the stage's chamber, the air reaching it
through the chambers before (cooling their ware: the climbing kiln's heat recovery) and its gas
preheating the chambers after it. Each stage runs until its chamber's setting reaches its target,
and its time is reported: the Suzuki kiln's printed stage times (Olsen p.93: the firebox 15 h to
1000 °C, then 7 h each for chambers 1–3 and 5 h each for 4–7, 56 h to cone 8–9) become a test
once the stoking rate and the loads are known (part C).

What a stage burns is the caller's (a stoker's rate, or a schedule held by the chamber's setting):
the book prints no side-stoking rate, so a run states it.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field, replace

import numpy as np
from numpy.typing import NDArray

from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat.zone import ZoneModel
from kilndesigner.working import Step

type Vector = NDArray[np.float64]


@dataclass(frozen=True)
class Stage:
    """One stage: the chamber stoked (its setting's index, from 0), how the fuel burns there,
    the setting temperature (K) that ends it, and the longest it may run (s)."""

    chamber: int
    mode: fi.FixedInput | fi.Schedule
    target: float
    limit: float


@dataclass(frozen=True)
class Staged:
    """A staged firing: the stages joined into one record (times from the start), each stage's
    time (s; None where its chamber didn't reach its target in its limit)."""

    firing: fi.Firing
    times: tuple[float | None, ...]
    steps: tuple[Step, ...] = field(default=())


def stage_model(model: ZoneModel, chamber: int) -> ZoneModel:
    """The model with the fuel burning in a chamber's zone (the zone of its setting)."""
    if not 0 <= chamber < len(model.settings):
        raise fi.FiringError(f"no chamber {chamber + 1}: the model has {len(model.settings)}")
    return replace(model, burns=model.settings[chamber].zone)


def fire_stages(model: ZoneModel, stages: Sequence[Stage], sample: float = 600.0) -> Staged:
    """Fire the stages in turn from cold, each from where the last ended."""
    if not stages:
        raise fi.FiringError("a staged firing needs a stage")
    parts: list[fi.Firing] = []
    times: list[float | None] = []
    state: Vector | None = None
    offset = 0.0
    for st in stages:
        m = stage_model(model, st.chamber)
        f = fi.fire(m, st.mode, st.limit, stop_at=(st.chamber, st.target), sample=sample,
                    start=state)  # fmt: skip
        times.append(f.events.get((st.chamber, st.target)))
        parts.append(replace(f, times=f.times + offset))
        offset += float(f.times[-1])
        state = f.state
        if not f.completed:  # pragma: no cover - SUNDIALS' own failure, kept in the record
            break
    joined = _join(parts)
    return Staged(joined, tuple(times), (_working(model, stages, times, joined),))


def _join(parts: list[fi.Firing]) -> fi.Firing:
    """The stages' records as one, each stage's first sample its last's end."""
    first = parts[0]
    cut = [slice(None)] + [slice(1, None)] * (len(parts) - 1)
    cat = [np.concatenate([getattr(p, k)[c] for p, c in zip(parts, cut, strict=True)])
           for k in ("times", "t_gases", "t_settings", "fuel_rate", "air_share",
                     "air_share_smooth", "lam")]  # fmt: skip
    events: dict[tuple[int, float], float] = {}
    base = 0.0
    for p in parts:
        for key, when in p.events.items():
            events.setdefault(key, base + when)
        base = float(p.times[-1])
    last = parts[-1]
    return replace(first, times=cat[0], t_gases=cat[1], t_settings=cat[2], fuel_rate=cat[3],
                   air_share=cat[4], air_share_smooth=cat[5], lam=cat[6], energy=last.energy,
                   events=events, completed=all(p.completed for p in parts),
                   message=last.message, state=last.state, steps=last.steps)  # fmt: skip


def _working(
    model: ZoneModel, stages: Sequence[Stage], times: list[float | None], f: fi.Firing
) -> Step:
    e = f.energy
    each = ", ".join(
        f"chamber {s.chamber + 1} to {s.target - 273.15:.0f} °C: "
        + (f"{t / 3600:.2f} h" if t is not None else f"not in {s.limit / 3600:.0f} h")
        for s, t in zip(stages, times, strict=False)
    )
    ends = ", ".join(f"{model.settings[k].name} {f.t_settings[-1, k] - 273.15:.0f} °C"
                     for k in range(len(model.settings)))  # fmt: skip
    return Step(
        name="The stages",
        value=each,
        formula="each stage: the fuel burns in its chamber; the air reaches it through the "
        "chambers before, its gas warms those after; until its setting reaches its target",
        inputs={"fuel": f"{e['fuel kg']:.1f} kg", "the settings at the end": ends},
        reference="problem set §2.4; Olsen p.93 (the Suzuki kiln's stages)",
    )
