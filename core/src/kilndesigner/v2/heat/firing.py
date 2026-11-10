"""A firing in time: the zones' DAE (`zone.py`) on SUNDIALS IDA (scikit-sundae), the settings'
temperatures as events, restarted at each break in a schedule (`thermal-software.md` §3.2–3.3:
IDA held to a piecewise-linear log failed on its kinks until stopped and restarted at them).

Modes (problem set §2.2), each the fuel's row:
- **max fire**: a stoked kiln as hard as its own draft lets it burn: the air the chimney draws with
  the damper open (`draft.py`, at each zone's temperature, through the fireboxes' intakes) burns
  the fuel at the products' λ; for coal, no more than the grates burn (`air.py`, the bed's most:
  the rest of the air passes as excess); a stoker's firing is anything slower, so a printed time
  is checked against this;
- **fixed input**: burners at a rating (or any fixed fuel rate);
- **a schedule** of temperatures held by a zone's gas (the first setting's, unless given), or by
  the first setting, the fuel what it takes. Its air (ADR 0017 decision 9): the stoker's, matched
  to the products' λ, the draft checked after for the most it draws; or the draft's own, all the
  air the chimney draws through the intakes a share open burning the fuel, so λ follows from the
  draft through the firing, above the products' λ with the intakes wide, below it (reduction)
  with them closed down.
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

from kilndesigner.v2.heat.air import COAL_BED_REFERENCE, MIXING_NOTE, REDUCTION, WOOD_BED_NOTE
from kilndesigner.v2.heat.gas import T_MAX, T_MIN
from kilndesigner.v2.heat.zone import FUEL_SCALE, Balance, Layout, State, ZoneModel
from kilndesigner.working import Step

type Vector = NDArray[np.float64]

SOURCES = (
    "SUNDIALS IDA (Hindmarsh et al., ACM TOMS 31, 2005; Gardner et al., ACM TOMS 48, 2022) through "
    "scikit-sundae 1.2; thermal-software.md §3"
)


START_TOL = 1e-3  # the algebraic rows at a start (kW, K, Pa/10): IDA refines from there
REDUCED = 0.999  # λ under this is reduction (λ 1 itself comes out to IDA's tolerance)


class FiringError(ValueError):
    """The firing can't be integrated as asked (a refusal with its reason, ADR 0009)."""


@dataclass(frozen=True)
class MaxFire:
    """As hard as the draft allows: the fuel the most air burns at the products' λ."""


@dataclass(frozen=True)
class FixedInput:
    """A fixed fuel rate (kg/s): burners at their rating, or a stoker's steady rate. ``air``: the
    products' own at their λ, or the draft's own through the intakes ``opened`` a share open (λ
    from the draft: below 1, reduction, when the stoker feeds more than the air burns)."""

    fuel: float
    air: Literal["stoker", "draft"] = "stoker"
    opened: float = 1.0

    def __post_init__(self) -> None:
        if not 0 < self.opened <= 1:
            raise FiringError("the intakes are open by a share of more than 0, at most 1")


@dataclass(frozen=True)
class Schedule:
    """Temperatures (K) at times (s), held by the gas (of zone ``zone``, else the first setting's)
    or by the first setting, linear between. ``air``: the stoker's, at the products' λ, or the
    draft's own through the intakes ``opened`` a share open (λ from the draft)."""

    held: Literal["gas", "setting"]
    points: tuple[tuple[float, float], ...]
    zone: int | None = None
    air: Literal["stoker", "draft"] = "stoker"
    opened: float = 1.0

    def __post_init__(self) -> None:
        ts = [p[0] for p in self.points]
        if len(ts) < 2 or any(b <= a for a, b in itertools.pairwise(ts)):
            raise FiringError("a schedule needs two or more points at increasing times")
        if not 0 < self.opened <= 1:
            raise FiringError("the intakes are open by a share of more than 0, at most 1")

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
    """A firing's record: at each output time each zone's gas and each setting (K), the fuel
    rate (kg/s) and the air it needs over the most the draft draws; the energy over the firing
    (J); when each setting reached each target (s), keyed (setting, K). ``t_gas`` and
    ``t_setting`` are the first setting's and its zone's."""

    times: Vector
    t_gases: NDArray[np.float64]  # (n, zones)
    t_settings: NDArray[np.float64]  # (n, settings)
    fuel_rate: Vector
    air_share: Vector
    energy: dict[str, float]
    events: dict[tuple[int, float], float]
    completed: bool
    message: str
    gas: tuple[str, ...] = ()
    main: int = 0  # the first setting's zone
    steps: tuple[Step, ...] = field(default=())
    air_share_smooth: Vector = field(default_factory=lambda: np.zeros(0))
    state: Vector = field(default_factory=lambda: np.zeros(0))  # every unknown at the end
    lam: Vector = field(default_factory=lambda: np.zeros(0))  # λ at each output time
    bed_share: float = math.nan  # the most of the grates' most the fuel took (coal)

    @property
    def t_gas(self) -> Vector:
        return self.t_gases[:, self.main]

    @property
    def worst_air_share_smooth(self) -> float:
        """The air share at the draft band's most-air end: a smooth wall (`draft.ROUGH_NOTE`) and
        each fitting's lower coefficient (`draft.Path.most`)."""
        share = self.air_share_smooth[np.isfinite(self.air_share_smooth)]
        return float(share.max()) if len(share) else math.nan

    @property
    def t_setting(self) -> Vector:
        return self.t_settings[:, 0]

    def reached(self, target: float, setting: int = 0) -> float | None:
        """When a setting (the first, unless given) first reached ``target`` (K), or None."""
        if (setting, target) in self.events:
            return self.events[(setting, target)]
        col = self.t_settings[:, setting]
        above = np.flatnonzero(col >= target)
        if len(above) == 0:
            return None
        i = int(above[0])
        if i == 0:
            return float(self.times[0])
        t0, t1 = self.times[i - 1], self.times[i]
        s0, s1 = col[i - 1], col[i]
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
    """The mode's rows for one piece of time: the fuel's, and a setting it holds; and the air
    the stream carries, from the state, the gas's temperatures and the fuel (None: the
    products' own at their λ)."""

    fuel_row: Callable[[State, float], float]
    held: tuple[int, Callable[[State, float], float]] | None
    algebraic: list[int]
    air: Callable[[Vector, Vector, float], float | None] = field(
        default_factory=lambda: _stokers_air
    )


def _stokers_air(v: Vector, tg: Vector, f: float) -> float | None:
    """The stoker's air: the products' own at their λ (None)."""
    return None


def _drafts_air(
    mode: FixedInput | Schedule, model: ZoneModel, bal: Balance
) -> Callable[[Vector, Vector, float], float | None]:
    """The air a mode's stream carries: the stoker's, or the draft's own through the intakes as
    opened, at the gas's temperatures with the fuel burning (`Balance.drawn`)."""
    if mode.air == "stoker":
        return _stokers_air
    if model.path is None:
        raise FiringError("the draft's own air needs the kiln's draft, and its path isn't built")
    opened = model.path.opened(mode.opened)

    def drafts(v: Vector, tg: Vector, f: float) -> float | None:
        return bal.drawn(opened, tg, f)

    return drafts


def _rows(
    mode: Mode,
    model: ZoneModel,
    bal: Balance,
    y: Callable[[], Vector],
    now: Callable[[], tuple[float, float]],
) -> _Rows:
    """The mode's rows; ``now`` gives the time and the start of the piece being integrated."""
    lay = bal.lay
    alg = lay.algebraic
    if isinstance(mode, MaxFire):
        if lay.air < 0:
            raise FiringError("max fire needs the kiln's draft, and its path couldn't be built")
        per = model.products.air
        bed = model.bed if model.bed is not None else math.inf

        def fuel_max(s: State, cap: float) -> float:
            v = y()
            return (v[lay.fuel] - min(v[lay.air] / per, bed)) * FUEL_SCALE

        return _Rows(fuel_max, None, alg, lambda v, tg, f: float(v[lay.air]))
    air = _drafts_air(mode, model, bal)
    if isinstance(mode, FixedInput):
        fuel = mode.fuel
        return _Rows(lambda s, c: (y()[lay.fuel] - fuel) * FUEL_SCALE, None, alg, air)
    sched = mode
    if sched.held == "gas":
        zone = sched.zone if sched.zone is not None else model.setting.zone

        def gas_held(s: State, cap: float) -> float:
            return y()[lay.gases[zone]] - sched.at(*now())[0]

        return _Rows(gas_held, None, alg, air)

    def setting_rate(s: State, cap: float) -> float:
        return (cap * sched.at(*now())[1] - s.q_setting) / 1e3

    def setting_held(s: State, cap: float) -> float:
        return y()[lay.setting] - sched.at(*now())[0]

    return _Rows(setting_rate, (0, setting_held), [*alg, lay.setting], air)


type Target = float | tuple[int, float]


def _mark(x: Target) -> tuple[int, float]:
    """A target as (setting, K): a bare temperature is the first setting's."""
    return (int(x[0]), float(x[1])) if isinstance(x, tuple) else (0, float(x))


def fire(
    model: ZoneModel,
    mode: Mode,
    t_end: float,
    targets: Sequence[Target] = (),
    stop_at: Target | None = None,
    sample: float = 60.0,
    rtol: float = 1e-5,
    start: Vector | None = None,
    max_steps: int = 50_000,
) -> Firing:
    """Fire the model from cold (or from ``start``, a firing's end state, the walls and settings
    as they were) for ``t_end`` (s), or until a setting reaches ``stop_at`` (K, or (setting, K));
    record when they reach each of ``targets``. ``max_steps``: IDA's budget for each piece of the
    schedule; spent, the firing stops there, not completed, and says so."""
    bal = Balance(model, air_row=isinstance(mode, MaxFire))
    lay = bal.lay
    if start is not None and (len(start) != lay.size or lay.air >= 0):
        raise FiringError("a firing carries on from one of the same model, not at max fire")
    room = model.t_room
    stop = _mark(stop_at) if stop_at is not None else None
    wanted: set[tuple[int, float]] = {_mark(x) for x in targets}
    if stop is not None:
        wanted.add(stop)
    marks: list[tuple[int, float]] = sorted(wanted)
    breaks = [0.0, t_end]
    if isinstance(mode, Schedule):
        breaks = sorted({0.0, t_end, *(p[0] for p in mode.points if 0 < p[0] < t_end)})
    y = np.full(lay.size, room)
    # A start the solver finds its way from: the fire's zone hot, the gas cooling along the path
    b = model.burns
    y[list(lay.gases)] = [600.0 if z < b else max(1800.0 - 300.0 * (z - b), 900.0)
                          for z in range(len(lay.gases))]  # fmt: skip
    y[lay.fuel] = mode.fuel if isinstance(mode, FixedInput) else 0.005
    if lay.air >= 0:
        y[lay.air] = 0.05
    y[lay.acc :] = 0.0
    if isinstance(mode, Schedule):
        if mode.held == "gas":
            zone = mode.zone if mode.zone is not None else model.setting.zone
            y[lay.gases[zone]] = mode.at(0.0)[0]
        else:
            y[lay.setting] = mode.at(0.0)[0]
    if start is not None:
        y = np.asarray(start, dtype=float).copy()
        y[lay.fuel] = mode.fuel if isinstance(mode, FixedInput) else y[lay.fuel]
    current: dict[str, Any] = {"y": y, "t": 0.0, "start": 0.0}
    rows = _rows(mode, model, bal, lambda: current["y"], lambda: (current["t"], current["start"]))

    def resfn(t: float, yy: Vector, yp: Vector, res: Vector) -> None:
        current["y"], current["t"] = yy, t
        tg = np.clip(yy[list(lay.gases)], T_MIN, T_MAX)
        fuel = float(yy[lay.fuel])
        bal.fill(yy, yp, res, tg, fuel, rows.fuel_row, rows.held, rows.air(yy, tg, fuel))

    times: list[Vector] = []
    ys: list[NDArray[np.float64]] = []
    events: dict[tuple[int, float], float] = {}
    message, completed = "", True
    sp = bal.sparsity()
    for t0, t1 in itertools.pairwise(breaks):
        current["start"] = t0
        y = _consistent(resfn, y, rows.algebraic, t0, lay.size)
        pending = [m for m in marks if m not in events]
        opts: dict[str, Any] = {
            "algebraic_idx": rows.algebraic, "calc_initcond": "yp0", "rtol": rtol,
            "atol": _atol(lay), "linsolver": "sparse", "sparsity": sp, "max_num_steps": max_steps,
        }  # fmt: skip
        if pending:
            where = [lay.settings[k] for k, _ in pending]
            opts.update(eventsfn=_events(pending, where, stop), num_events=len(pending))
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
        if stop is not None and stop in events:
            message = f"the setting reached {stop[1] - 273.15:.0f} °C"
            break
    t_all = np.concatenate(times)
    y_all = np.concatenate(ys)
    return _record(model, bal, mode, t_all, y_all, events, completed, message)


def _events(pending: list[tuple[int, float]], where: list[int], stop: Any) -> Any:
    """IDA's events: each setting rising through its targets, the stop target terminal."""

    def eventsfn(t: float, yy: Vector, yp: Vector, ev: Vector) -> None:
        for i, ((_, m), w) in enumerate(zip(pending, where, strict=True)):
            ev[i] = yy[w] - m

    fn: Any = eventsfn
    fn.terminal = [p == stop for p in pending]
    fn.direction = [1] * len(pending)
    return fn


def _atol(lay: Layout) -> Vector:
    atol = np.full(lay.size, 1e-3)
    atol[lay.fuel] = 1e-8
    if lay.air >= 0:
        atol[lay.air] = 1e-6
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
    if np.abs(part(sol.x)).max() > START_TOL:
        sol = root(part, y[alg], method="lm")  # Levenberg–Marquardt, slower and surer
    if np.abs(part(sol.x)).max() > START_TOL:  # a least-squares minimum isn't a start
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
    events: dict[tuple[int, float], float],
    completed: bool,
    message: str,
) -> Firing:
    lay = bal.lay
    tg, fuel, ts = y[:, list(lay.gases)], y[:, lay.fuel], y[:, list(lay.settings)]
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
    smooth = np.full(len(t), math.nan)
    p = model.products
    lam = np.full(len(t), p.air_ratio)
    if lay.air >= 0:
        share = fuel * p.air / np.maximum(y[:, lay.air], 1e-12)
        lam = p.air_ratio / np.maximum(share, 1e-12)
    elif model.path is not None:
        share, smooth = _shares(model, bal, t, tg, fuel)
        if isinstance(mode, Schedule | FixedInput) and mode.air == "draft":
            lam = _drawn_lam(model, bal, mode, t, tg, fuel)
    else:
        share = np.full(len(t), math.nan)
    bed = float(fuel.max() / model.bed) if model.bed is not None else math.nan
    acc = y[-1, lay.acc :]
    pairs = zip(lay.acc_names, acc, strict=True)
    energy = {name: float(v) * (1.0 if i == 0 else 1e6) for i, (name, v) in enumerate(pairs)}
    names = tuple(g.name for g in model.gas)
    firing = Firing(t, tg, ts, fuel, share, energy, events, completed, message, names,
                    model.setting.zone, air_share_smooth=smooth, state=y[-1].copy(), lam=lam,
                    bed_share=bed)  # fmt: skip
    return replace(firing, steps=(*model.steps, *_working(model, mode, firing)))


def _drawn_lam(
    model: ZoneModel, bal: Balance, mode: Schedule | FixedInput, t: Vector,
    tg: NDArray[np.float64], fuel: Vector,
) -> Vector:  # fmt: skip
    """λ through a firing on the draft's own air: the air drawn through the intakes as opened,
    at SHARE_POINTS times (linear between), over what the fuel burnt at λ 1 needs."""
    assert model.path is not None
    opened = model.path.opened(mode.opened)
    p = model.products
    pick = np.unique(np.linspace(0, len(t) - 1, min(len(t), SHARE_POINTS)).astype(int))
    lam = [p.air_ratio * bal.drawn(opened, tg[i], float(fuel[i])) / max(float(fuel[i]) * p.air,
                                                                       1e-12)
           for i in pick]  # fmt: skip
    return np.interp(t, t[pick], np.array(lam))


SHARE_POINTS = 60  # the draft's air found at this many times, the share between them linear


def _shares(model: ZoneModel, bal: Balance, t: Vector, tg: NDArray[np.float64],
            fuel: Vector) -> tuple[Vector, Vector]:  # fmt: skip
    """The air each instant's fuel needs over the most the draft draws at the zones'
    temperatures, damper open (`draft.draw`, by bisection), at up to SHARE_POINTS times: at the
    draft band's least-air end (rough brick, the fittings' higher coefficients) and its most-air
    end (`draft.Path.most`)."""
    from kilndesigner.v2.heat.draft import draw

    path = model.path
    assert path is not None
    smooth = path.most()
    p = model.products
    pick = np.unique(np.linspace(0, len(t) - 1, min(len(t), SHARE_POINTS)).astype(int))
    out: list[list[float]] = [[], []]
    for i in pick:
        temps = {name: float(tg[i, bal.path_zone.get(name, 0)])
                 for name in ("firebox", "chamber", "chimney", *bal.path_zone)}  # fmt: skip
        burnt = None if bal.stoked else float(fuel[i])
        for k, pth in enumerate((path, smooth)):
            most = draw(pth, temps, p, burnt).air
            out[k].append(float(fuel[i]) * p.air / max(most, 1e-12))
    rough_share, smooth_share = (np.interp(t, t[pick], np.array(v)) for v in out)
    return rough_share, smooth_share


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
        (f"setting {s + 1} " if len(model.settings) > 1 else "")
        + f"{k - 273.15:.0f} °C at {v / 3600:.2f} h"
        for (s, k), v in sorted(f.events.items())
    )
    shares = ", ".join(
        f"{k} {100 * e[k] / fuel_heat:.0f} %" for k in ("flue", "walls", "setting", "openings")
    )
    zones = [k for k in e if k.startswith("walls: ")]
    if zones:
        shares += (
            " (the walls: "
            + ", ".join(f"{k[7:]} {100 * e[k] / fuel_heat:.0f} %" for k in zones)
            + ")"
        )
    closure = e["fuel heat"] - e["flue"] - e["walls"] - e["setting"] - e["openings"]
    hottest = ", ".join(f"{g} {f.t_gases[:, z].max() - 273.15:.0f} °C" for z, g in enumerate(f.gas))
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
            formula="F·[H_in − H_out] = Q_rad + Q_fire + Σ h·A·ΔT in each zone, each instant; "
            "integrated: net heat in = flue + walls + setting + openings",
            inputs={
                "net heat in": f"{e['fuel heat'] / 1e6:.1f} MJ",
                "unaccounted": f"{closure / 1e6:.2e} MJ",
            },
        ),
        Step(
            name="Air needed over the most the draft draws",
            value=f"at most {f.worst_air_share:.2f}"
            if model.path is not None
            else "not worked out: the kiln's draft path isn't built",
        ),
        _lam_step(model, mode, f),
    )


def _lam_step(model: ZoneModel, mode: Mode, f: Firing) -> Step:
    """λ through the firing (ADR 0017 decision 9), how it was set, and the fuel bed's share."""
    lam = f.lam[np.isfinite(f.lam)]
    low, high = (float(lam.min()), float(lam.max())) if len(lam) else (math.nan, math.nan)
    value = f"{low:.2f}–{high:.2f}"
    if low < REDUCED:
        below = f.times[f.lam < REDUCED]
        value += f"; reduction (λ < 1) from {below[0] / 3600:.2f} to {below[-1] / 3600:.2f} h"
    if low < REDUCTION[0]:
        value += f"; below {REDUCTION[0]}, the least checked: the products held there"
    if isinstance(mode, MaxFire):
        how = "max fire: the draft's air burns the fuel at the products' λ"
        if model.bed is not None:
            how += (
                f", no more than the grates' {model.bed * 3600:.0f} kg/h dry (at most "
                f"{f.bed_share:.2f} of it), the rest of the air in excess"
            )
    elif mode.air == "draft":
        how = f"the draft's own air through the intakes {mode.opened:.0%} open burns the fuel " + (
            "the schedule takes" if isinstance(mode, Schedule) else "fed at a fixed rate"
        )
    else:
        how = "the stoker's (or the burners'), at the products' λ"
    note = MIXING_NOTE if model.products.fuel.kind != "gas" else None
    if model.products.fuel.kind == "wood":
        note = f"{MIXING_NOTE}; {WOOD_BED_NOTE}"
    elif model.products.fuel.kind == "coal":
        note = f"{MIXING_NOTE}; {COAL_BED_REFERENCE}"
    return Step(name="λ through the firing", value=value, inputs={"how": how}, note=note)
