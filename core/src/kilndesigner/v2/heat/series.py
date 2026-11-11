"""Zones in series from the design (ADR 0017 H1): a row of chambers and a tube cut into segments
as gas zones of one enclosure (`chamber.py`: the engine's own cells, `massing.cells`, joined
through the flue holes in the walls between chambers, `run_parts.flue_rows`), each wall between
two chambers a wall with a face in each (`kiln.heat_model`); and a **staged firing**, each chamber
stoked in turn (problem set §2.4): the fuel burns in the stage's chamber, the air reaching it
through the chambers before (cooling their ware: the climbing kiln's heat recovery) and its gas
preheating the chambers after it. Each stage runs until its chamber's setting reaches its target,
and its time is reported: the Suzuki kiln's printed stage times (Olsen p.93: the firebox 15 h to
1000 °C, then 7 h each for chambers 1–3 and 5 h each for 4–7, 56 h to cone 8–9) are tested so
(part C3b, `docs/planning/11-10-26.md`).

**Each stage on its own draft** (ADR 0017 decision 9; C3b): a stage carries its own gas path
(`paths.Inputs.stage`: the front's way in for the stage the front firebox fires; the stoked
chamber's side stoke holes beside the front's path, or alone with the fire mouth shut, C1's
question 3, carried as the band's two ends) and the zone its fuel burns in. Its fuel:

- **max fire**, as hard as that path's draft lets it burn (all the air it draws at the products'
  λ, the draft's air an unknown of the stage's DAE): a stoker's stage is anything slower, so a
  printed stage time is checked against this one (problem set §2.2);
- **a ramp**: the stoked chamber's setting held to a straight line from where it stands to its
  target over a time (the book's stage time), the fuel whatever that takes, with the stoker's air
  (λ at the products') or all the air the stage's draft draws (λ from the draft): the fuel
  against the heat (T3) at the book's own pace;
- a fixed rate or a schedule, as `firing.py` takes them.

With the fire mouth shut no stream passes the zones before the stoked one (`ZoneModel.enters`):
its air comes through its side holes alone. With it open all the stream passes the front's zones,
though the draft may split it between the front's path and the side holes (`draft.Draft.shares`):
the two ends bound the stoker's practice, which the book doesn't print (said in the working).

A stage whose chamber the stages before have already brought to its target takes no time (its
fuel none). Each stage carries on from the last's state: walls, settings and the energy so far.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from typing import Literal

import numpy as np
from numpy.typing import NDArray

from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat.draft import Path
from kilndesigner.v2.heat.zone import Balance, Layout, ZoneModel, layout
from kilndesigner.working import Step

type Vector = NDArray[np.float64]

AIR_START = 0.05  # kg/s: the draft's air where it draws none to start from (as `firing.fire`)


@dataclass(frozen=True)
class Ramp:
    """The stoked chamber's setting held to a straight line from where the stage finds it to the
    stage's target over ``time`` (s); the air the stoker's (at the products' λ) or the draft's
    own through the intakes ``opened`` a share open (λ from the draft)."""

    time: float
    air: Literal["stoker", "draft"] = "stoker"
    opened: float = 1.0


type StageMode = fi.MaxFire | fi.FixedInput | fi.Schedule | Ramp


@dataclass(frozen=True)
class Stage:
    """One stage: the chamber whose setting ends it (its index, from 0), how the fuel burns, the
    setting temperature (K) that ends it, and the longest it may run (s); the stage's own draft
    path (None: the model's), the gas zone its fuel burns in (None: the chamber's own; the
    firebox's for the stage the front fire takes), whether the fire mouth is open (the stream
    through the front's zones) and its name."""

    chamber: int
    mode: StageMode
    target: float
    limit: float
    path: Path | None = None
    burns: int | None = None
    front_open: bool = True
    name: str = ""


@dataclass(frozen=True)
class Staged:
    """A staged firing: the stages joined into one record (times from the start), each stage's
    time (s; None where its chamber didn't reach its target in its limit, 0 where the stages
    before had brought it there), its fuel (kg, dry) and its own record (None where skipped)."""

    firing: fi.Firing
    times: tuple[float | None, ...]
    steps: tuple[Step, ...] = field(default=())
    fuel: tuple[float, ...] = ()
    parts: tuple[fi.Firing | None, ...] = ()

    @property
    def total(self) -> float | None:
        """The stages' times together (s), None if any stage fell short."""
        return None if None in self.times else float(sum(t or 0.0 for t in self.times))


def stage_model(
    model: ZoneModel,
    chamber: int,
    path: Path | None = None,
    burns: int | None = None,
    front_open: bool = True,
) -> ZoneModel:
    """The model with the fuel burning in a chamber's zone (the zone of its setting) or in
    ``burns``, on the stage's draft ``path``; with the fire mouth shut the stream enters at that
    zone."""
    if not 0 <= chamber < len(model.settings):
        raise fi.FiringError(f"no chamber {chamber + 1}: the model has {len(model.settings)}")
    zone = model.settings[chamber].zone if burns is None else burns
    if not 0 <= zone < len(model.gas):
        raise fi.FiringError(f"no gas zone {zone + 1} to burn in: the model has {len(model.gas)}")
    return replace(model, burns=zone, path=model.path if path is None else path,
                   enters=0 if front_open else zone)  # fmt: skip


def _carried(m: ZoneModel, state: Vector, had_air: bool, air_row: bool) -> Vector:
    """The last stage's end state in this stage's layout: at max fire the draft's air is an
    unknown of its own, right after the fuel (`zone.layout`)."""
    g = len(m.gas)
    if had_air == air_row:
        return state
    if had_air:
        return np.delete(state, g + 1)
    return np.insert(state, g + 1, AIR_START)  # a guess: `_lit` sets it


def _lit(m: ZoneModel, lay: Layout, y: Vector | None) -> Vector:
    """Max fire's start (``y``, else the cold kiln's), its fire lit: the gas from the burning zone
    on at least `firing.fire`'s guess (1800 K, 300 K less a zone after, at least 900 K) and the air
    and fuel what the stage's path draws so. The algebraic unknowns are only guesses, solved again
    at the start (`firing._consistent`); from these they grow to the hot branch of max fire's
    consistent states. A kiln's draft also balances with almost no fire, the fire out (Fujiwara's
    dogi from cold at its driest wood found that one, 0.003 kg/s): max fire is the most the draft
    draws."""
    if y is None:
        y = np.full(lay.size, m.t_room)
        y[lay.acc :] = 0.0
    else:
        y = y.copy()
    g, b = len(m.gas), m.burns
    lit = np.array([max(1800.0 - 300.0 * (z - b), 900.0) if z >= b else 0.0 for z in range(g)])
    y[:g] = np.maximum(y[:g], lit)
    assert m.path is not None  # the air is a row only where the path is built (`zone.layout`)
    drawn = Balance(m).drawn(m.path, y[:g], 0.0)
    y[lay.air] = max(drawn, AIR_START)
    y[lay.fuel] = y[lay.air] / m.products.air
    return y


def _mode(st: Stage, start: float) -> tuple[fi.Mode, float]:
    """The stage's firing mode and limit (s): a ramp as the schedule it is, from ``start`` (K)."""
    if not isinstance(st.mode, Ramp):
        return st.mode, st.limit
    r = st.mode
    sched = fi.Schedule("setting", ((0.0, start), (r.time, st.target)), air=r.air,
                        opened=r.opened, setting=st.chamber)  # fmt: skip
    return sched, r.time


def fire_stages(
    model: ZoneModel, stages: Sequence[Stage], sample: float = 600.0, rtol: float = 1e-5
) -> Staged:
    """Fire the stages in turn from cold, each from where the last ended (``rtol`` IDA's)."""
    if not stages:
        raise fi.FiringError("a staged firing needs a stage")
    parts: list[fi.Firing] = []
    each: list[fi.Firing | None] = []
    times: list[float | None] = []
    fuel: list[float] = []
    state: Vector | None = None
    had_air = False
    offset, burnt = 0.0, 0.0
    for st in stages:
        m = stage_model(model, st.chamber, st.path, st.burns, st.front_open)
        air_row = isinstance(st.mode, fi.MaxFire) and m.path is not None  # else refused there
        start = None if state is None else _carried(m, state, had_air, air_row)
        lay = layout(m, air_row)
        if air_row:
            start = _lit(m, lay, start)
        t_now = m.t_room if start is None else float(start[lay.settings[st.chamber]])
        if t_now >= st.target - fi.REACHED_TOL:  # brought there by the stages before
            times.append(0.0)
            fuel.append(0.0)
            each.append(None)
            continue
        mode, limit = _mode(st, t_now)
        f = fi.fire(m, mode, limit, stop_at=(st.chamber, st.target), sample=sample, rtol=rtol,
                    start=start)  # fmt: skip
        times.append(f.reached(st.target, st.chamber))
        fuel.append(f.fuel_kg - burnt)
        burnt = f.fuel_kg
        each.append(f)
        parts.append(replace(f, times=f.times + offset))
        offset += float(f.times[-1])
        state, had_air = f.state, air_row
        if not f.completed:  # pragma: no cover - SUNDIALS' own failure, kept in the record
            break
    if not parts:
        raise fi.FiringError("every stage's chamber was at its target before it began")
    joined = _join(parts)
    step = _working(model, stages, times, fuel, joined)
    return Staged(joined, tuple(times), (step,), tuple(fuel), tuple(each))


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


def _how(st: Stage) -> str:
    """A stage's fuel and air, in words."""
    mode = st.mode
    if isinstance(mode, fi.MaxFire):
        what = "max fire on its draft"
    elif isinstance(mode, Ramp):
        air = "the stoker's air" if mode.air == "stoker" else "the draft's own air"
        what = f"held to a {mode.time / 3600:.1f} h ramp, {air}"
    elif isinstance(mode, fi.FixedInput):
        what = f"{mode.fuel * 3600:.0f} kg/h"
    else:
        what = "a schedule"
    return what + ("" if st.front_open else ", the fire mouth shut")


def _working(
    model: ZoneModel,
    stages: Sequence[Stage],
    times: list[float | None],
    fuel: list[float],
    f: fi.Firing,
) -> Step:
    e = f.energy
    each = "; ".join(
        f"{s.name or f'chamber {s.chamber + 1}'} to {s.target - 273.15:.0f} °C ({_how(s)}): "
        + (f"{t / 3600:.2f} h, {w:.0f} kg" if t is not None else f"not in {s.limit / 3600:g} h")
        for s, t, w in zip(stages, times, fuel, strict=False)
    )
    ends = ", ".join(f"{model.settings[k].name} {f.t_settings[-1, k] - 273.15:.0f} °C"
                     for k in range(len(model.settings)))  # fmt: skip
    peaks = ", ".join(f"{model.settings[k].name} {f.t_settings[:, k].max() - 273.15:.0f} °C"
                      for k in range(len(model.settings)))  # fmt: skip
    lam = f.lam[np.isfinite(f.lam)]
    return Step(
        name="The stages",
        value=each,
        formula="each stage: the fuel burns in its chamber (or the front's firebox); the air "
        "reaches it through its own path (the front's, its side holes, or both), cooling the "
        "chambers it passes; its gas warms those after; until its setting reaches its target",
        inputs={
            "fuel": f"{e['fuel kg']:.1f} kg",
            "the settings at the end": ends,
            "the settings at their hottest": peaks,
            "λ": f"{lam.min():.2f}–{lam.max():.2f}" if len(lam) else "not worked out",
        },
        reference="problem set §2.4; Olsen p.93 (the Suzuki kiln's stages)",
        note="the fire mouth open: all the stream through the front's zones, though the draft may "
        "split it with the side holes; shut: none through them (the band's two ends, C1's "
        "question 3)"
        if any(s.path is not None for s in stages)
        else None,
    )
