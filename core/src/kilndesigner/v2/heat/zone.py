"""One well-stirred gas zone as a DAE (ADR 0017 H1; Hottel's well-stirred furnace as Latham 2008
pp. 24–26 restates it after Rhine & Tucker 1991): the gas, its surfaces, the walls behind them and
the setting, for SUNDIALS IDA.

**The gas** holds no heat of its own (quasi-steady; its residence time is about a second,
`thermal-software.md` §7.2) and leaves at its own temperature. Its balance, the fire inside it:

    F·q(T_g) = Σ_walls (Q_rad + Q_conv) + Q_setting + Q_openings,

F the fuel (kg/s), q(T_g) the heat each kg keeps when the products leave at T_g (`gas.py`).
**Each wall's hot face**: Q_rad + h·A·(T_g − T_hot) = the heat into its first cell (`walls.py`).
**The setting**, one lumped node: M·c_p(T)·dT/dt = Q_rad + h·A·(T_g − T). **Radiation**: the zone
method over the rays' exchange areas with the WSGG grey gases (`gasrad.py`).

**Openings** are black: a spy hole open to the room at the room's temperature (H13); an inlet flue
or a burner port is the fire seen through it, black at the gas's temperature, inside the fire's
control volume (its net radiation is the fuel's, not a loss); the exit flue at its wall's hot-face
temperature, its channel being that wall's brick (H13's chimney walls as their own zone wait for
zones in series; `thermal-combinations.md` §4.1).

**Convection inside**: no correlation for a kiln's setting is sourced (`thermal-software.md` §9):
ht's laminar flat plate (Baehr–Stephan) at the mean velocity across the chamber, over the setting's
length along the flow, the stated stand-in, the same coefficient on every surface.

The unknowns: [T_g, F, (T_hot, cells…, T_out) for each wall, T_setting, accumulators]. Which of
T_g, F and T_setting is held by the firing's mode is `firing.py`'s.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import ClassVar, Literal

import numpy as np
from ht.conv_external import (  # pyright: ignore[reportMissingTypeStubs]
    Nu_horizontal_plate_laminar_Baehr,
)
from numpy.typing import NDArray

from kilndesigner.thermal.transient import HeatCapacity
from kilndesigner.v2.heat import sources as src
from kilndesigner.v2.heat.draft import Table
from kilndesigner.v2.heat.gas import Products
from kilndesigner.v2.heat.gasrad import GasExchange
from kilndesigner.v2.heat.walls import CellWall
from kilndesigner.working import Step

type Vector = NDArray[np.float64]

CONVECTION_NOTE = (
    "no correlation for convection to a kiln's setting is sourced (thermal-software.md §9): ht's "
    "laminar flat plate (Baehr–Stephan) at the mean velocity across the chamber, over the "
    "setting's length along the flow, on every surface: a stated stand-in"
)


@dataclass(frozen=True)
class Line:
    """A hot-face emissivity line, ε = f·(a + 10⁻⁵·b·T), extrapolated past its measured range
    (the user's decision for refractories, radiation-exchange.md §5.5) and kept in 0.05–1."""

    name: str
    a: float
    b: float
    measured: tuple[float, float]
    reference: str
    factor: float = src.HEMISPHERICAL.value

    def __call__(self, t: Vector) -> Vector:
        return np.clip(self.factor * (self.a + 1e-5 * self.b * t), 0.05, 1.0)


def line(key: str) -> Line:
    a, b, measured, ref = src.EMISSIVITY_LINES[key]
    return Line(key, a, b, measured, f"{ref} (radiation-exchange.md §5)")


@dataclass(frozen=True)
class Setting:
    """The load: ware and furniture as one lumped node in its envelope (m, the chamber's frame)."""

    mass: float
    emissivity: float
    lo: tuple[float, float, float]
    hi: tuple[float, float, float]
    heat_capacity: HeatCapacity
    reference: str


def fired_clay() -> HeatCapacity:
    """v1's ware curve: 800 J/(kg·K) at 24 °C (Lienhard), then VDI's fireclay points."""
    from kilndesigner.library import material

    sh = material("firebrick-medium-duty-smithfield").specific_heat
    assert sh is not None
    ts, cs = sh.to_points()
    return HeatCapacity((src.FIRED_CLAY_AT, *ts), (src.FIRED_CLAY_CP.value, *cs))


@dataclass(frozen=True)
class Opening:
    """A black opening and what it shows: the room, the fire, or the flue's channel."""

    name: str
    kind: Literal["room", "flame", "flue"]
    wall: str = ""


@dataclass(frozen=True)
class Face:
    """A wall behind a surface of the exchange: its cells and its hot face's emissivity."""

    name: str
    wall: CellWall
    emissivity: Line


@dataclass(frozen=True)
class Flow:
    """Where the convection's velocity and length come from: the flow's cross-section (m²) and
    the setting's length along it (m)."""

    area: float
    length: float


@dataclass(frozen=True)
class ZoneModel:
    """Everything the DAE needs, in the exchange's surface order."""

    products: Products
    exchange: GasExchange
    names: tuple[str, ...]
    faces: tuple[Face, ...]
    setting: Setting
    openings: tuple[Opening, ...]
    flow: Flow
    t_room: float
    draft: Table | None = None
    steps: tuple[Step, ...] = field(default=())

    def __post_init__(self) -> None:
        named = {f.name for f in self.faces} | {o.name for o in self.openings} | {"setting"}
        if named != set(self.names):
            raise ValueError(f"every surface needs a wall, the setting or an opening: {named}")


@dataclass(frozen=True)
class Layout:
    """Where each unknown sits in the DAE's vector."""

    tg: int
    fuel: int
    walls: tuple[tuple[int, int, int], ...]  # (hot face, first cell, outer face) of each wall
    setting: int
    acc: int  # the first accumulator
    size: int

    ACC: ClassVar[tuple[str, ...]] = (
        "fuel kg", "fuel heat", "flue", "walls", "setting", "openings",
    )  # fmt: skip

    @property
    def algebraic(self) -> list[int]:
        out = [self.tg, self.fuel]
        for hot, _, out_face in self.walls:
            out += [hot, out_face]
        return out


def layout(model: ZoneModel) -> Layout:
    walls: list[tuple[int, int, int]] = []
    i = 2
    for f in model.faces:
        walls.append((i, i + 1, i + 1 + f.wall.cells))
        i += f.wall.cells + 2
    setting = i
    acc = setting + 1
    return Layout(0, 1, tuple(walls), setting, acc, acc + len(Layout.ACC))


@dataclass(frozen=True)
class State:
    """The heat flows at one instant (W), for the balance and the record."""

    q_walls: Vector
    q_setting: float
    q_openings: float
    released: float  # F·q(T_g)
    h: float


class Balance:
    """The zone's residual pieces, shared by every mode."""

    def __init__(self, model: ZoneModel) -> None:
        self.m = model
        self.lay = layout(model)
        names = model.names
        self.i_face = np.array([names.index(f.name) for f in model.faces])
        self.i_set = names.index("setting")
        self.room = np.array([names.index(o.name) for o in model.openings if o.kind == "room"],
                             dtype=int)  # fmt: skip
        self.flame = np.array([names.index(o.name) for o in model.openings if o.kind == "flame"],
                              dtype=int)  # fmt: skip
        self.flue = [(names.index(o.name), [f.name for f in model.faces].index(o.wall))
                     for o in model.openings if o.kind == "flue"]  # fmt: skip
        self.loss = np.concatenate([self.room, [i for i, _ in self.flue]]).astype(int)
        self.areas = model.exchange.areas
        self.eps_fixed = np.ones(len(names))
        self.eps_fixed[self.i_set] = model.setting.emissivity

    def convection(self, t_gas: float, fuel: float) -> float:
        """h (W/(m²·K)) from the laminar flat plate at the mean velocity."""
        p = self.m.products
        rho, mu, k, cp = p.props(min(max(t_gas, 300.0), 3000.0))
        v = max(fuel * p.mass, 1e-9) / (rho * self.m.flow.area)
        length = self.m.flow.length
        nu = float(Nu_horizontal_plate_laminar_Baehr(rho * v * length / mu, cp * mu / k))
        return nu * k / length

    def temps(self, y: Vector, t_gas: float) -> tuple[Vector, Vector]:
        """Every surface's temperature and emissivity."""
        lay, n = self.lay, len(self.m.names)
        t = np.empty(n)
        hot = np.array([y[h] for h, _, _ in lay.walls])
        t[self.i_face] = hot
        t[self.i_set] = y[lay.setting]
        t[self.room] = self.m.t_room
        t[self.flame] = t_gas
        for i, w in self.flue:
            t[i] = hot[w]
        eps = self.eps_fixed.copy()
        for k, f in enumerate(self.m.faces):
            eps[self.i_face[k]] = float(f.emissivity(np.array([hot[k]]))[0])
        return t, eps

    def state(self, y: Vector, t_gas: float, fuel: float) -> State:
        t, eps = self.temps(y, t_gas)
        q_rad = self.m.exchange.net(t_gas, t, eps)
        h = self.convection(t_gas, fuel)
        conv = h * self.areas * (t_gas - t)
        q_walls = (q_rad + conv)[self.i_face]
        q_set = float(q_rad[self.i_set] + conv[self.i_set])
        q_open = float(q_rad[self.loss].sum())
        return State(q_walls, q_set, q_open, fuel * self.m.products.released(t_gas), h)

    def fill(
        self,
        y: Vector,
        yp: Vector,
        res: Vector,
        t_gas: float,
        fuel: float,
        row0: Callable[[State, float], float],
        row1: Callable[[State, float], float],
        setting_row: Callable[[State, float], float] | None = None,
    ) -> State:
        """Every row: the walls and the accumulators here; rows 0 and 1, and the setting's when
        the mode holds it, from the mode, each given the state and the setting's heat capacity
        (J/K)."""
        lay, m = self.lay, self.m
        s = self.state(y, t_gas, fuel)
        for k, f in enumerate(m.faces):
            hot, c0, out = lay.walls[k]
            cells = y[c0:out]
            q = f.wall.flows(y[hot], cells, y[out])
            res[hot] = (s.q_walls[k] - q[0]) / 1e3
            res[c0:out] = f.wall.capacity(cells) * yp[c0:out] - (q[:-1] - q[1:])
            res[out] = q[-1] - f.wall.outer_loss(y[out])
        cap = m.setting.mass * float(m.setting.heat_capacity.cp(np.array([y[lay.setting]]))[0])
        if setting_row is None:
            res[lay.setting] = (cap * yp[lay.setting] - s.q_setting) / 1e3
        else:
            res[lay.setting] = setting_row(s, cap)
        res[lay.tg] = row0(s, cap)
        res[lay.fuel] = row1(s, cap)
        a = lay.acc
        net = m.products.net_heat
        res[a] = yp[a] - fuel
        res[a + 1] = yp[a + 1] - fuel * net / 1e6
        res[a + 2] = yp[a + 2] - (fuel * net - s.released) / 1e6
        res[a + 3] = yp[a + 3] - float(s.q_walls.sum()) / 1e6
        res[a + 4] = yp[a + 4] - s.q_setting / 1e6
        res[a + 5] = yp[a + 5] - s.q_openings / 1e6
        return s

    def sparsity(self) -> NDArray[np.int_]:
        """The Jacobian's pattern: each wall's cells tridiagonal with their faces; the gas, the
        fuel, every hot face and the setting coupled through the radiation; the accumulators on
        those."""
        lay = self.lay
        sp = np.zeros((lay.size, lay.size), dtype=int)
        hub = [lay.tg, lay.fuel, lay.setting, *(h for h, _, _ in lay.walls)]
        for r in hub:
            sp[r, hub] = 1
        for hot, c0, out in lay.walls:
            for j in range(hot, out + 1):
                sp[j, max(hot, j - 1) : min(out, j + 1) + 1] = 1
            sp[lay.tg, c0] = sp[lay.fuel, c0] = 1
        for a in range(lay.acc, lay.size):
            sp[a, a] = 1
            sp[a, hub] = 1
        return sp
