"""Zones in series (ADR 0017 H1): well-stirred gas zones along the gas path, the gas leaving each
at that zone's temperature into the next (Hottel's well-stirred furnace zone by zone, as Latham
2008 restates it). The fuel burns in the first zone; zone k keeps what the gas gives up between
the zones' temperatures, F·[q(T_k) − q(T_{k−1})].

Each zone is a `zone.ZoneModel` with its own walls, setting and rays. Between two zones the
flues are black openings, each seeing the other zone's gas (as an inlet flue sees the fire): the
radiation between zones through them isn't the zone method's gas-to-gas exchange (that needs the
rays to start in the gas volumes, not written; `thermal-combinations.md` §5), so what one zone
sends through a link and the next receives needn't match; the mismatch is in the working.

Modes: a fixed input, or a schedule held by the first zone's gas or setting. A row's draft (the
chimney after the last zone) isn't built: the air isn't checked.
"""

from __future__ import annotations

import itertools
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from typing import Any

import numpy as np
from numpy.typing import NDArray
from sksundae.ida import IDA  # pyright: ignore[reportMissingTypeStubs]

from kilndesigner.v2.heat.firing import (
    FiringError,
    FixedInput,
    Schedule,
    _atol,  # pyright: ignore[reportPrivateUsage]
    _consistent,  # pyright: ignore[reportPrivateUsage]
    _gas_balance,  # pyright: ignore[reportPrivateUsage]
)
from kilndesigner.v2.heat.zone import Balance, Layout, State, ZoneModel
from kilndesigner.working import Step

type Vector = NDArray[np.float64]


@dataclass(frozen=True)
class SeriesFiring:
    """Each zone's gas and setting at each output time (K), the fuel rate, the totals (J) and
    when each zone's setting reached each target (s)."""

    times: Vector
    t_gas: NDArray[np.float64]  # (n, zones)
    t_setting: NDArray[np.float64]
    fuel_rate: Vector
    energy: dict[str, float]
    events: dict[tuple[int, float], float]
    steps: tuple[Step, ...] = field(default=())

    def reached(self, zone: int, target: float) -> float | None:
        if (zone, target) in self.events:
            return self.events[(zone, target)]
        return None


def fire_series(
    zones: Sequence[ZoneModel],
    mode: FixedInput | Schedule,
    t_end: float,
    targets: Sequence[tuple[int, float]] = (),
    stop_at: tuple[int, float] | None = None,
    sample: float = 60.0,
    rtol: float = 1e-5,
) -> SeriesFiring:
    """Fire zones in series from cold; ``targets`` and ``stop_at`` are (zone, setting K)."""
    if len({(z.products.fuel, z.products.air_ratio, z.products.t_air) for z in zones}) != 1:
        raise FiringError("zones in series burn one fuel at one air ratio")
    bals = [Balance(z) for z in zones]
    lays = [b.lay for b in bals]
    off = [0, *itertools.accumulate(lay.size for lay in lays)]
    size = off[-1]
    tg = [o + lay.tg for o, lay in zip(off, lays, strict=False)]
    fuel_i = off[0] + lays[0].fuel
    held = isinstance(mode, Schedule) and mode.held == "setting"
    room = zones[0].t_room
    y = np.full(size, room)
    for o, lay in zip(off, lays, strict=False):
        y[o + lay.tg] = 1500.0
        y[o + lay.fuel] = mode.fuel if isinstance(mode, FixedInput) else 0.001
        y[o + lay.acc : o + lay.size] = 0.0
    if isinstance(mode, Schedule):
        y[off[0] + (lays[0].setting if held else lays[0].tg)] = mode.at(0.0)[0]
    now: dict[str, float] = {"t": 0.0, "start": 0.0}

    def resfn(t: float, yy: Vector, yp: Vector, res: Vector) -> None:
        now["t"] = t
        temps = {k: min(max(float(yy[i]), 250.0), 3000.0) for k, i in enumerate(tg)}
        fuel = float(yy[fuel_i])
        for k, (b, lay, o) in enumerate(zip(bals, lays, off, strict=False)):
            b.others = temps
            b.upstream = temps[k - 1] if k > 0 else None
            yk, ypk, rk = yy[o : o + lay.size], yp[o : o + lay.size], res[o : o + lay.size]
            row0, row1, srow = _rows(k, mode, yk, lay, fuel, now)
            b.fill(yk, ypk, rk, temps[k], fuel, row0, row1, srow)

    alg = [o + i for o, lay in zip(off, lays, strict=False) for i in lay.algebraic]
    if held:
        alg.append(off[0] + lays[0].setting)
    sp = np.zeros((size, size), dtype=int)
    for b, lay, o in zip(bals, lays, off, strict=False):
        sp[o : o + lay.size, o : o + lay.size] = b.sparsity()
        hub = [o + lay.tg, o + lay.fuel, o + lay.setting, *(o + h for h, _, _ in lay.walls)]
        for r in [*hub, *range(o + lay.acc, o + lay.size)]:
            sp[r, tg] = 1
            sp[r, fuel_i] = 1
    breaks = [0.0, t_end]
    if isinstance(mode, Schedule):
        breaks = sorted({0.0, t_end, *(p[0] for p in mode.points if 0 < p[0] < t_end)})
    wanted: set[tuple[int, float]] = {(int(z), float(m)) for z, m in targets}
    if stop_at is not None:
        wanted.add((int(stop_at[0]), float(stop_at[1])))
    marks: list[tuple[int, float]] = sorted(wanted)
    atol = np.concatenate([_atol(lay) for lay in lays])
    times: list[Vector] = []
    ys: list[NDArray[np.float64]] = []
    events: dict[tuple[int, float], float] = {}
    for t0, t1 in itertools.pairwise(breaks):
        now["start"] = t0
        y = _consistent(resfn, y, alg, t0, size)
        pending = [m for m in marks if m not in events]
        opts: dict[str, Any] = {
            "algebraic_idx": alg, "calc_initcond": "yp0", "rtol": rtol, "atol": atol,
            "linsolver": "sparse", "sparsity": sp, "max_num_steps": 50_000,
        }  # fmt: skip
        if pending:
            where = [off[z] + lays[z].setting for z, _ in pending]
            opts.update(eventsfn=_events(pending, where, stop_at), num_events=len(pending))
        span = np.unique(np.concatenate([np.arange(t0, t1, sample), [t1]]))
        sol = IDA(resfn, **opts).solve(span, y, np.zeros(size))
        first = 0 if not times else 1
        times.append(np.asarray(sol.t, dtype=float)[first:])
        ys.append(np.asarray(sol.y, dtype=float)[first:])
        if sol.i_events is not None:
            flags, when = np.atleast_2d(sol.i_events), np.atleast_1d(sol.t_events)
            for idx, te in zip(flags, when, strict=False):
                for j in np.flatnonzero(np.asarray(idx) != 0):
                    events.setdefault(pending[int(j)], float(te))
        y = np.asarray(sol.y[-1], dtype=float).copy()
        if not sol.success:  # pragma: no cover - SUNDIALS' own failure
            raise FiringError(f"IDA stopped at {float(sol.t[-1]) / 3600:.2f} h: {sol.message}")
        if stop_at is not None and stop_at in events:
            break
    t_all, y_all = np.concatenate(times), np.concatenate(ys)
    return _record(zones, lays, off, t_all, y_all, events)


type Row = Callable[[State, float], float]


def _rows(
    k: int, mode: FixedInput | Schedule, yk: Vector, lay: Layout, fuel: float, now: dict[str, float]
) -> tuple[Row, Row, Row | None]:
    """Zone k's mode rows: the first zone's as a single zone's; the others solve their gas and
    take the first zone's fuel."""

    def balance(s: State, cap: float) -> float:
        return _gas_balance(s)

    def pinned(s: State, cap: float) -> float:
        return float(yk[lay.fuel]) - (
            mode.fuel if isinstance(mode, FixedInput) and k == 0 else fuel
        )

    if k > 0 or isinstance(mode, FixedInput):
        return balance, pinned, None
    sched = mode

    def held_gas(s: State, cap: float) -> float:
        return float(yk[lay.tg]) - sched.at(now["t"], now["start"])[0]

    if sched.held == "gas":
        return held_gas, balance, None

    def rate(s: State, cap: float) -> float:
        return (cap * sched.at(now["t"], now["start"])[1] - s.q_setting) / 1e3

    def held_setting(s: State, cap: float) -> float:
        return float(yk[lay.setting]) - sched.at(now["t"], now["start"])[0]

    return rate, balance, held_setting


def _events(pending: list[tuple[int, float]], where: list[int], stop: Any) -> Any:
    def eventsfn(t: float, yy: Vector, yp: Vector, ev: Vector) -> None:
        for i, ((_, m), w) in enumerate(zip(pending, where, strict=True)):
            ev[i] = yy[w] - m

    fn: Any = eventsfn
    fn.terminal = [p == stop for p in pending]
    fn.direction = [1] * len(pending)
    return fn


def _record(
    zones: Sequence[ZoneModel],
    lays: list[Layout],
    off: list[int],
    t: Vector,
    y: NDArray[np.float64],
    events: dict[tuple[int, float], float],
) -> SeriesFiring:
    tg = np.column_stack([y[:, o + lay.tg] for o, lay in zip(off, lays, strict=False)])
    ts = np.column_stack([y[:, o + lay.setting] for o, lay in zip(off, lays, strict=False)])
    fuel = y[:, off[0] + lays[0].fuel]
    acc = [
        dict(zip(Layout.ACC, y[-1, o + lay.acc : o + lay.size], strict=True))
        for o, lay in zip(off, lays, strict=False)
    ]
    n = len(zones)
    heat = float(acc[0]["fuel heat"]) * 1e6
    flue = (sum(float(a["flue"]) for a in acc) - (n - 1) * float(acc[0]["fuel heat"])) * 1e6
    links = sum(float(a["openings"]) for a in acc) * 1e6
    energy = {
        "fuel kg": float(acc[0]["fuel kg"]),
        "fuel heat": heat,
        "flue": flue,
        "walls": sum(float(a["walls"]) for a in acc) * 1e6,
        "setting": sum(float(a["setting"]) for a in acc) * 1e6,
        "openings": links,
    }
    closure = heat - flue - energy["walls"] - energy["setting"] - energy["openings"]
    step = Step(
        name="Zones in series",
        value=", ".join(
            f"zone {k + 1}: gas at most {tg[:, k].max() - 273.15:.0f} °C, setting "
            f"{ts[-1, k] - 273.15:.0f} °C at the end"
            for k in range(n)
        ),
        inputs={
            "fuel": f"{energy['fuel kg']:.2f} kg",
            "unaccounted": f"{closure / 1e6:.2e} MJ",
            "openings and links": f"{energy['openings'] / max(heat, 1.0):.1%} of the fuel's heat",
        },
        note="the links between zones are black at the neighbour's gas temperature: what one "
        "zone sends through them and the next receives needn't match (the gas-to-gas zone "
        "exchange isn't written); the mismatch is inside 'openings and links'",
    )
    return SeriesFiring(t, tg, ts, fuel, energy, events, (step,))
