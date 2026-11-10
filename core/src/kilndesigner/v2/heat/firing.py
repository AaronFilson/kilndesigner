"""A firing in time: the zone's DAE (`zone.py`) on SUNDIALS IDA (scikit-sundae), the setting's
temperatures as events, restarted at each break in a schedule (`thermal-software.md` §3.2–3.3:
IDA held to a piecewise-linear log failed on its kinks until stopped and restarted at them).

Modes (problem set §2.2):
- **max fire**: a stoked kiln as hard as its own draft lets it burn: the air the chimney draws with
  the damper open (`draft.py`) burns the fuel at the products' λ; a stoker's firing is anything
  slower, so a printed time is checked against this;
- **fixed input**: burners at a rating (or any fixed fuel rate);
- **a schedule** of temperatures held by the gas, or by the setting, the fuel what it takes.
Each mode fixes which of the gas temperature, the fuel and the setting is solved for.
"""

from __future__ import annotations

import itertools
import math
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field, replace
from typing import Any, Literal

import numpy as np
from numpy.typing import NDArray
from scipy.optimize import root
from sksundae.ida import IDA  # pyright: ignore[reportMissingTypeStubs]

from kilndesigner.v2.heat.gas import T_MAX, T_MIN
from kilndesigner.v2.heat.zone import Balance, Layout, State, ZoneModel
from kilndesigner.working import Step

type Vector = NDArray[np.float64]

SOURCES = (
    "SUNDIALS IDA (Hindmarsh et al., ACM TOMS 31, 2005; Gardner et al., ACM TOMS 48, 2022) through "
    "scikit-sundae 1.2; thermal-software.md §3"
)


class FiringError(ValueError):
    """The firing can't be integrated as asked (a refusal with its reason, ADR 0009)."""


@dataclass(frozen=True)
class MaxFire:
    """As hard as the draft allows: the fuel the most air burns at the products' λ."""


@dataclass(frozen=True)
class FixedInput:
    """A fixed fuel rate (kg/s): burners at their rating."""

    fuel: float


@dataclass(frozen=True)
class Schedule:
    """Temperatures (K) at times (s), held by the gas or by the setting, linear between."""

    held: Literal["gas", "setting"]
    points: tuple[tuple[float, float], ...]

    def __post_init__(self) -> None:
        ts = [p[0] for p in self.points]
        if len(ts) < 2 or any(b <= a for a, b in itertools.pairwise(ts)):
            raise FiringError("a schedule needs two or more points at increasing times")

    def at(self, t: float, start: float = -math.inf) -> tuple[float, float]:
        """The scheduled temperature and its rate (K/s) at t, on the first piece that ends after
        ``start`` (a segment's start: at a break the next piece's rate, not the last's)."""
        for (t0, v0), (t1, v1) in itertools.pairwise(self.points):
            if t1 > start + 1e-9 and (t <= t1 + 1e-9 or start >= t0 - 1e-9):
                rate = (v1 - v0) / (t1 - t0)
                return v0 + rate * (min(max(t, t0), t1) - t0), rate
        return self.points[-1][1], 0.0


type Mode = MaxFire | FixedInput | Schedule


@dataclass(frozen=True)
class Firing:
    """A firing's record: at each output time the gas, the setting, the fuel rate (kg/s) and the
    air it needs over the most the draft draws; the energy over the firing (J); when the setting
    reached each target (s)."""

    times: Vector
    t_gas: Vector
    t_setting: Vector
    fuel_rate: Vector
    air_share: Vector
    energy: dict[str, float]
    events: dict[float, float]
    completed: bool
    message: str
    steps: tuple[Step, ...] = field(default=())

    def reached(self, target: float) -> float | None:
        """When the setting first reached ``target`` (K), or None."""
        if target in self.events:
            return self.events[target]
        above = np.flatnonzero(self.t_setting >= target)
        if len(above) == 0:
            return None
        i = int(above[0])
        if i == 0:
            return float(self.times[0])
        t0, t1 = self.times[i - 1], self.times[i]
        s0, s1 = self.t_setting[i - 1], self.t_setting[i]
        return float(t0 + (t1 - t0) * (target - s0) / (s1 - s0))

    @property
    def fuel_kg(self) -> float:
        return self.energy["fuel kg"]

    @property
    def worst_air_share(self) -> float:
        share = self.air_share[np.isfinite(self.air_share)]
        return float(share.max()) if len(share) else math.nan


@dataclass
class _Rows:
    """The mode's rows for one piece of time."""

    row0: Callable[[State, float], float]
    row1: Callable[[State, float], float]
    setting_row: Callable[[State, float], float] | None
    algebraic: list[int]


def _gas_balance(s: State) -> float:
    return (s.released - float(s.q_walls.sum()) - s.q_setting - s.q_openings) / 1e3


def _rows(
    mode: Mode,
    model: ZoneModel,
    lay: Layout,
    y: Callable[[], Vector],
    now: Callable[[], tuple[float, float]],
) -> _Rows:
    """The mode's rows; ``now`` gives the time and the start of the piece being integrated."""
    alg = lay.algebraic
    if isinstance(mode, MaxFire):
        draft = model.draft
        if draft is None:
            raise FiringError("max fire needs the kiln's draft, and its path couldn't be built")
        per = model.products.air

        def fuel_max(s: State, cap: float) -> float:
            v = y()
            return v[lay.fuel] - draft.at(v[lay.tg]) / per

        return _Rows(lambda s, c: _gas_balance(s), fuel_max, None, alg)
    if isinstance(mode, FixedInput):
        fuel = mode.fuel
        return _Rows(lambda s, c: _gas_balance(s), lambda s, c: y()[lay.fuel] - fuel, None, alg)
    sched = mode
    if sched.held == "gas":

        def gas_held(s: State, cap: float) -> float:
            return y()[lay.tg] - sched.at(*now())[0]

        return _Rows(gas_held, lambda s, c: _gas_balance(s), None, alg)

    def setting_rate(s: State, cap: float) -> float:
        return (cap * sched.at(*now())[1] - s.q_setting) / 1e3

    def setting_held(s: State, cap: float) -> float:
        return y()[lay.setting] - sched.at(*now())[0]

    return _Rows(setting_rate, lambda s, c: _gas_balance(s), setting_held, [*alg, lay.setting])


def fire(
    model: ZoneModel,
    mode: Mode,
    t_end: float,
    targets: Sequence[float] = (),
    stop_at: float | None = None,
    sample: float = 60.0,
    rtol: float = 1e-5,
) -> Firing:
    """Fire the model from cold to ``t_end`` (s), or until the setting reaches ``stop_at`` (K);
    record when it reaches each of ``targets``."""
    bal = Balance(model)
    lay = bal.lay
    room = model.t_room
    wanted: set[float] = {float(x) for x in targets}
    if stop_at is not None:
        wanted.add(float(stop_at))
    marks: list[float] = sorted(wanted)
    breaks = [0.0, t_end]
    if isinstance(mode, Schedule):
        breaks = sorted({0.0, t_end, *(p[0] for p in mode.points if 0 < p[0] < t_end)})
    y = np.full(lay.size, room)
    y[lay.tg] = 1500.0
    y[lay.fuel] = mode.fuel if isinstance(mode, FixedInput) else 0.001
    y[lay.acc :] = 0.0
    if isinstance(mode, Schedule):
        y[lay.tg if mode.held == "gas" else lay.setting] = mode.at(0.0)[0]
    current: dict[str, Any] = {"y": y, "t": 0.0, "start": 0.0}
    rows = _rows(mode, model, lay, lambda: current["y"], lambda: (current["t"], current["start"]))

    def resfn(t: float, yy: Vector, yp: Vector, res: Vector) -> None:
        current["y"], current["t"] = yy, t
        tg = min(max(float(yy[lay.tg]), T_MIN), T_MAX)
        bal.fill(yy, yp, res, tg, float(yy[lay.fuel]), rows.row0, rows.row1, rows.setting_row)

    times: list[Vector] = []
    ys: list[NDArray[np.float64]] = []
    events: dict[float, float] = {}
    message, completed = "", True
    sp = bal.sparsity()
    for t0, t1 in itertools.pairwise(breaks):
        current["start"] = t0
        y = _consistent(resfn, y, rows.algebraic, t0, lay.size)
        pending = [m for m in marks if m not in events]
        opts: dict[str, Any] = {
            "algebraic_idx": rows.algebraic, "calc_initcond": "yp0", "rtol": rtol,
            "atol": _atol(lay), "linsolver": "sparse", "sparsity": sp, "max_num_steps": 50_000,
        }  # fmt: skip
        if pending:
            opts.update(eventsfn=_events(pending, lay.setting, stop_at), num_events=len(pending))
        span = np.unique(np.concatenate([np.arange(t0, t1, sample), [t1]]))
        sol = IDA(resfn, **opts).solve(span, y, np.zeros(lay.size))
        first = 0 if not times else 1  # the break's sample is the last piece's end
        times.append(np.asarray(sol.t, dtype=float)[first:])
        ys.append(np.asarray(sol.y, dtype=float)[first:])
        if sol.i_events is not None:
            flags, when = np.atleast_2d(sol.i_events), np.atleast_1d(sol.t_events)
            for idx, te in zip(flags, when, strict=False):
                for k in np.flatnonzero(np.asarray(idx) != 0):
                    events.setdefault(pending[int(k)], float(te))
        y = np.asarray(sol.y[-1], dtype=float).copy()
        if not sol.success:  # pragma: no cover - SUNDIALS' own failure, kept in the record
            message, completed = str(sol.message), False
            break
        if stop_at is not None and stop_at in events:
            message = f"the setting reached {stop_at - 273.15:.0f} °C"
            break
    t_all = np.concatenate(times)
    y_all = np.concatenate(ys)
    return _record(model, bal, mode, t_all, y_all, events, completed, message)


def _events(pending: list[float], setting: int, stop_at: float | None) -> Any:
    """IDA's events: the setting rising through each target, the stop target terminal."""

    def eventsfn(t: float, yy: Vector, yp: Vector, ev: Vector) -> None:
        for i, m in enumerate(pending):
            ev[i] = yy[setting] - m

    fn: Any = eventsfn
    fn.terminal = [stop_at is not None and m == stop_at for m in pending]
    fn.direction = [1] * len(pending)
    return fn


def _atol(lay: Layout) -> Vector:
    atol = np.full(lay.size, 1e-3)
    atol[lay.fuel] = 1e-8
    atol[lay.acc :] = 1e-6
    return atol


def _consistent(
    resfn: Callable[[float, Vector, Vector, Vector], None],
    y: Vector,
    alg: list[int],
    t: float,
    size: int,
) -> Vector:
    """The algebraic unknowns solved with everything else held (IDA then finds y′)."""
    res = np.zeros(size)
    yp = np.zeros(size)

    def part(x: Vector) -> Vector:
        yy = y.copy()
        yy[alg] = x
        resfn(t, yy, yp, res)
        return res[alg].copy()

    sol = root(part, y[alg], method="hybr")
    if not sol.success and np.abs(part(sol.x)).max() > 1e-6:
        raise FiringError(f"no consistent start at {t / 3600:.2f} h: {sol.message}")
    out = y.copy()
    out[alg] = sol.x
    return out


def _record(
    model: ZoneModel,
    bal: Balance,
    mode: Mode,
    t: Vector,
    y: NDArray[np.float64],
    events: dict[float, float],
    completed: bool,
    message: str,
) -> Firing:
    lay = bal.lay
    tg, fuel, ts = y[:, lay.tg], y[:, lay.fuel], y[:, lay.setting]
    if tg.max() > T_MAX:
        raise FiringError(
            f"the gas reached {tg.max() - 273.15:.0f} °C, past the gas tables' "
            f"{T_MAX - 273.15:.0f} °C (GRI-Mech's range)"
        )
    if tg.min() < T_MIN:
        raise FiringError(
            f"the gas fell to {tg.min() - 273.15:.0f} °C, below the gas tables' "
            f"{T_MIN - 273.15:.0f} °C"
        )
    if model.draft is not None:
        share = fuel * model.products.air / np.array([max(model.draft.at(x), 1e-12) for x in tg])
    else:
        share = np.full(len(t), math.nan)
    acc = y[-1, lay.acc :]
    pairs = zip(Layout.ACC, acc, strict=True)
    energy = {name: float(v) * (1.0 if i == 0 else 1e6) for i, (name, v) in enumerate(pairs)}
    firing = Firing(t, tg, ts, fuel, share, energy, events, completed, message)
    return replace(firing, steps=(*model.steps, *_working(model, mode, firing)))


def _working(model: ZoneModel, mode: Mode, f: Firing) -> tuple[Step, ...]:
    e = f.energy
    fuel_heat = e["fuel heat"] or 1.0
    what = {
        MaxFire: "as hard as the draft allows (the damper open), the fuel at the products' λ",
        FixedInput: "a fixed fuel rate",
        Schedule: "held to a schedule",
    }[type(mode)]
    if isinstance(mode, Schedule):
        what += f" by the {mode.held}"
    reached = ", ".join(
        f"{k - 273.15:.0f} °C at {v / 3600:.2f} h" for k, v in sorted(f.events.items())
    )
    shares = ", ".join(
        f"{k} {100 * e[k] / fuel_heat:.0f} %" for k in ("flue", "walls", "setting", "openings")
    )
    closure = e["fuel heat"] - e["flue"] - e["walls"] - e["setting"] - e["openings"]
    hottest = f"{f.t_gas.max() - 273.15:.0f} °C"
    return (
        Step(
            name="The firing",
            value=f"{f.times[-1] / 3600:.2f} h, {what}; "
            + (f"the setting reached {reached}" if reached else "no target reached"),
            inputs={"fuel": f"{e['fuel kg']:.2f} kg", "gas, hottest": hottest},
            reference=SOURCES,
            note=f.message or None,
        ),
        Step(
            name="Where the fuel's heat went",
            value=shares,
            formula="F·q(T_g) = Σ walls + setting + openings, each instant; integrated",
            inputs={
                "net heat in": f"{e['fuel heat'] / 1e6:.1f} MJ",
                "unaccounted": f"{closure / 1e6:.2e} MJ",
            },
        ),
        Step(
            name="Air needed over the most the draft draws",
            value=f"at most {f.worst_air_share:.2f}"
            if model.draft is not None
            else "not worked out: the kiln's draft path isn't built",
        ),
    )
