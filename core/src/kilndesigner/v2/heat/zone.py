"""Well-stirred gas zones as a DAE (ADR 0017 H1; Hottel's well-stirred furnace as Latham 2008
pp. 24–26 restates it after Rhine & Tucker 1991, zone by zone along the gas path): the gas, its
surfaces, the walls behind them and the settings, for SUNDIALS IDA.

**The gas** of each zone holds no heat of its own (quasi-steady; its residence time is about a
second, `thermal-software.md` §7.2) and leaves at its own temperature into the next zone. The
stream through zone z is air before the zone the fuel burns in (``burns``) and the products from
it on; per kg of fuel, entering at the room's temperature:

    F·[H_in,z − H_out,z] = −Q_rad,z − Q_fire,z + Σ_(surfaces of z) h_z·A·(T_z − T_s),

H the stream's enthalpy (`gas.py`: m·h_products(T), or the air's m_air·h_air(T)), the fuel's own
enthalpy entering the burning zone; Q_rad,z the zone's net radiative gain (`gasrad.ZonesExchange`);
Q_fire,z the net radiation into the black surfaces that show its fire (a grate, an inlet flue or a
burner port, inside the fire's control volume: their exchange is the fuel's, not a loss). With one
zone burning its fuel this is F·q(T_g) = Σ walls + setting + openings, as before.

**Each wall's hot face**: Q_rad + h·A·(T_g − T_hot) = the heat into its first cell (`walls.py`); a
wall between two zones (a floor over a firebox) has a second surface, its outer face, balanced the
same way against its own zone. **Each setting**, a lumped node in its zone: M·c_p(T)·dT/dt = Q_rad
+ h·A·(T_g − T). **Radiation**: the zone method over the rays' exchange areas with the WSGG grey
gases (`gasrad.py`). **The draft** (a design with its chimney): the air it draws, damper open, is
an unknown of its own, its row the pressure balance round the path at the zones' temperatures
(`draft.py`); a stoked kiln at max fire burns the fuel that air carries.

**Openings** are black: a spy hole or the chimney's top open to the room at the room's temperature
(H13); the fire's surfaces at their zone's gas temperature; an exit flue left as an opening (the
chimney not a zone) at its wall's hot-face temperature.

**Convection inside** (`fittings-and-kiln-convection.md` §2, "For the engine"; no measured
coefficient inside a kiln exists): each zone as flow in a duct on its section's hydraulic diameter
at the mean velocity, the larger of Baehr–Stephan's developing laminar flow and Gnielinski's
turbulent correlation (Lienhard eq. 7.41; ht), with Churchill–Chu's natural convection (Lienhard
eq. 8.13b) as each surface's floor; the setting at its passages' laminar parallel-plate value
(Lienhard Table 7.4) on a stated band of gaps.

The unknowns: [T_g of each zone, F, (the draft's air), (T_hot, cells…, T_out) for each wall, the
soil, T of each setting, accumulators]. Which of them the firing's mode holds is `firing.py`'s.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Literal

import numpy as np
from fluids.friction import Clamond  # pyright: ignore[reportMissingTypeStubs]
from ht.conv_internal import (  # pyright: ignore[reportMissingTypeStubs]
    laminar_entry_Baehr_Stephan,
    turbulent_Gnielinski,
)
from numpy.typing import NDArray

from kilndesigner.thermal.transient import HeatCapacity
from kilndesigner.v2.heat import sources as src
from kilndesigner.v2.heat.draft import Path, Table, pressure
from kilndesigner.v2.heat.gas import Products
from kilndesigner.v2.heat.gasrad import GasExchange, ZonesExchange
from kilndesigner.v2.heat.ground import Ground
from kilndesigner.v2.heat.walls import CellWall
from kilndesigner.working import Step

type Vector = NDArray[np.float64]

CONVECTION = (
    "each zone flow in a duct on its section's hydraulic diameter; Churchill–Chu the floor; the "
    "setting its passages' laminar value"
)
CONVECTION_NOTE = (
    "fittings-and-kiln-convection.md §2 (no measured coefficient inside a kiln exists): each zone "
    "as flow in a duct on its section's hydraulic diameter at the mean velocity, the larger of "
    "Baehr–Stephan's developing laminar flow over the zone's length and Gnielinski's turbulent "
    "correlation (Lienhard eq. 7.41, ±20 % on D_h; ht 1.2), the gas the hotter so no property "
    "correction (eq. 7.45, n = 0); Churchill–Chu's natural convection on a vertical wall of the "
    "zone's height (eq. 8.13b), at the film temperature, as each surface's floor (floors and roofs "
    "taken as walls); the setting at its passages' fully developed laminar value between plates, "
    "Nu 7.541 (Table 7.4), or Gnielinski's when turbulent, on gaps of a stated band (no source "
    "gives a kiln setting's passages) at the zone's mean velocity, over its envelope's area"
)
AIR_SCALE = 10.0  # Pa: the draft's row
FUEL_SCALE = 1e3
DUCT_RE_MIN = 10.0  # the duct correlation's least Reynolds number (a still chimney: no matter)
G = 9.80665
PLATES_NU = 7.541  # Lienhard Table 7.4: parallel plates, fully developed laminar, T_w fixed
TURBULENT_RE = 2300.0  # Gnielinski's range starts here (Lienhard eq. 7.41)


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
    """A load: ware and furniture as one lumped node in its envelope (m, the chamber's frame), in
    gas zone ``zone``, its surface ``name``; ``gap`` the passages between its ware (m, a stated
    band's end, `sources.SETTING_GAP`)."""

    mass: float
    emissivity: float
    lo: tuple[float, float, float]
    hi: tuple[float, float, float]
    heat_capacity: HeatCapacity
    reference: str
    name: str = "setting"
    zone: int = 0
    gap: float = src.SETTING_GAP[1]


def fired_clay() -> HeatCapacity:
    """v1's ware curve: 800 J/(kg·K) at 24 °C (Lienhard), then VDI's fireclay points."""
    from kilndesigner.library import material

    sh = material("firebrick-medium-duty-smithfield").specific_heat
    assert sh is not None
    ts, cs = sh.to_points()
    return HeatCapacity((src.FIRED_CLAY_AT, *ts), (src.FIRED_CLAY_CP.value, *cs))


@dataclass(frozen=True)
class Opening:
    """A black opening and what it shows: the room, the fire of gas zone ``zone``, or the exit
    flue's channel (its wall's hot face)."""

    name: str
    kind: Literal["room", "flame", "flue"]
    wall: str = ""
    zone: int = 0


@dataclass(frozen=True)
class Face:
    """A wall behind a surface: its cells, its hot face's emissivity and the gas zone it faces;
    a wall between two zones names its outer face's surface (``back``), zone and emissivity."""

    name: str
    wall: CellWall
    emissivity: Line
    zone: int = 0
    back: str = ""
    back_zone: int = 0
    back_emissivity: Line | None = None


@dataclass(frozen=True)
class Flow:
    """Where a zone's convection comes from: the flow's cross-section (m²), the length along it
    (m), the section's hydraulic diameter (m), and its walls' height (m, natural convection's)."""

    area: float
    length: float
    duct: float
    height: float


@dataclass(frozen=True)
class Gas:
    """A well-stirred gas zone of the path: its name and its convection's flow."""

    name: str
    flow: Flow


@dataclass(frozen=True)
class ZoneModel:
    """Everything the DAE needs, in the exchange's surface order; the gas zones in the gas's
    order along the path, the fuel burning in zone ``burns``."""

    products: Products
    exchange: GasExchange | ZonesExchange
    names: tuple[str, ...]
    faces: tuple[Face, ...]
    settings: tuple[Setting, ...]
    openings: tuple[Opening, ...]
    gas: tuple[Gas, ...]
    t_room: float
    draft: Table | None = None
    steps: tuple[Step, ...] = field(default=())
    ground: Ground | None = None
    path: Path | None = None
    path_zones: tuple[tuple[str, int], ...] = ()
    burns: int = 0

    def __post_init__(self) -> None:
        if not self.settings:
            raise ValueError("no heat result without a load (ADR 0017 decision 11)")
        named = (
            {f.name for f in self.faces} | {f.back for f in self.faces if f.back}
            | {o.name for o in self.openings} | {s.name for s in self.settings}
        )  # fmt: skip
        if named != set(self.names):
            raise ValueError(f"every surface needs a wall, a setting or an opening: {named}")
        on_soil = [f.name for f in self.faces if f.wall.outside.kind == "ground"]
        if len(on_soil) != (self.ground is not None):
            raise ValueError("a ground needs one wall on it, and a wall on the ground its ground")

    @property
    def setting(self) -> Setting:
        return self.settings[0]

    @property
    def flow(self) -> Flow:
        return self.gas[0].flow


@dataclass(frozen=True)
class Layout:
    """Where each unknown sits in the DAE's vector."""

    gases: tuple[int, ...]
    fuel: int
    air: int  # the draft's air, or -1
    walls: tuple[tuple[int, int, int], ...]  # (hot face, first cell, outer face) of each wall
    settings: tuple[int, ...]
    acc: int  # the first accumulator
    size: int
    acc_names: tuple[str, ...]
    grounded: int = -1  # the wall on the ground, or -1
    soil: tuple[int, int] = (0, 0)  # the ground's free nodes: first, count

    @property
    def tg(self) -> int:
        return self.gases[0]

    @property
    def setting(self) -> int:
        return self.settings[0]

    @property
    def algebraic(self) -> list[int]:
        """The algebraic unknowns: a grounded wall's outer face has the disc's soil as its
        capacity, so it is differential."""
        out = [*self.gases, self.fuel] + ([self.air] if self.air >= 0 else [])
        for k, (hot, _, out_face) in enumerate(self.walls):
            out += [hot] if k == self.grounded else [hot, out_face]
        return out


ACC = ("fuel kg", "fuel heat", "flue", "walls", "setting", "openings")


def layout(model: ZoneModel, air_row: bool = False) -> Layout:
    """The unknowns' places; the draft's air an unknown of its own at max fire (``air_row``)."""
    g = len(model.gas)
    gases = tuple(range(g))
    fuel = g
    i = g + 1
    air = -1
    if air_row and model.path is not None:
        air, i = i, i + 1
    walls: list[tuple[int, int, int]] = []
    for f in model.faces:
        walls.append((i, i + 1, i + 1 + f.wall.cells))
        i += f.wall.cells + 2
    grounded, soil = -1, (0, 0)
    if model.ground is not None:
        grounded = next(k for k, f in enumerate(model.faces) if f.wall.outside.kind == "ground")
        soil = (i, len(model.ground.free))
        i += soil[1]
    settings = tuple(range(i, i + len(model.settings)))
    acc = i + len(model.settings)
    names = ACC + (tuple(f"walls: {z.name}" for z in model.gas) if g > 1 else ())
    return Layout(gases, fuel, air, tuple(walls), settings, acc, acc + len(names), names,
                  grounded, soil)  # fmt: skip


def duct_h(rho: float, mu: float, k: float, cp: float, v: float, d: float, length: float) -> float:
    """Flow in a duct of hydraulic diameter ``d`` (W/(m²·K)): the larger of Baehr–Stephan's
    developing laminar flow over ``length`` and Gnielinski's turbulent correlation (Lienhard eq.
    7.41, from Re 1000 so the larger doesn't jump at transition; ht 1.2)."""
    re = max(rho * v * d / mu, DUCT_RE_MIN)
    pr = cp * mu / k
    laminar = float(laminar_entry_Baehr_Stephan(re, pr, length, d))
    fd = float(Clamond(max(re, TURBULENT_RE), 0.0))
    turbulent = float(turbulent_Gnielinski(re, pr, fd)) if re > 1000.0 else 0.0
    return max(laminar, turbulent) * k / d


def natural_h(p: Products, t_gas: Vector, t_wall: Vector, tall: Vector) -> Vector:
    """Churchill–Chu's natural convection on a vertical wall ``tall`` high (Lienhard eq. 8.13b,
    all Ra; ht's `Nu_vertical_plate_Churchill`), the gas's properties at the film temperature,
    β = 1/T_film (an ideal gas), W/(m²·K)."""
    film = np.clip((t_gas + t_wall) / 2, 300.0, 3000.0)
    rho = np.interp(film, p.temps, p.density)
    mu = np.interp(film, p.temps, p.viscosity)
    k = np.interp(film, p.temps, p.conductivity)
    cp = np.interp(film, p.temps, p.cp)
    pr = cp * mu / k
    ra = G * np.abs(t_gas - t_wall) / film * tall**3 * (rho / mu) ** 2 * pr
    nu = (0.825 + 0.387 * ra ** (1 / 6) / (1 + (0.492 / pr) ** (9 / 16)) ** (8 / 27)) ** 2
    return nu * k / tall


def passage_h(rho: float, mu: float, k: float, cp: float, v: float, d: float) -> float:
    """A setting's passages, gaps between ware of hydraulic diameter ``d`` = 2 × the gap: fully
    developed laminar flow between plates, Nu 7.541 (Lienhard Table 7.4, T_w fixed), or
    Gnielinski's when the flow is turbulent (W/(m²·K))."""
    re = rho * v * d / mu
    nu = PLATES_NU
    if re > TURBULENT_RE:
        fd = float(Clamond(re, 0.0))
        nu = max(nu, float(turbulent_Gnielinski(re, cp * mu / k, fd)))
    return nu * k / d


@dataclass(frozen=True)
class State:
    """The heat flows at one instant (W), for the balances and the record: into each wall's hot
    face and outer face (a wall between zones), each setting, the openings that lose to the room;
    each zone's released heat, each surface's convection coefficient and each zone's gas's
    radiative gain."""

    q_walls: Vector
    q_backs: Vector
    q_settings: Vector
    q_openings: float
    released: Vector
    h: Vector
    out: Vector  # what each zone's gas gives up

    @property
    def q_setting(self) -> float:
        return float(self.q_settings[0])


class Balance:
    """The zones' residual pieces, shared by every mode; the draft's air an unknown at max fire
    (``air_row``): below about 300 K the products are denser than the room's air and the draft
    reverses, and a duct's friction factor jumps at transition, which a Newton iteration doesn't
    cross well, so the other modes find the draft's air after the firing, by bisection."""

    def __init__(self, model: ZoneModel, air_row: bool = False) -> None:
        self.m = model
        self.lay = layout(model, air_row)
        names = model.names
        g = len(model.gas)
        self.g = g
        self.i_face = np.array([names.index(f.name) for f in model.faces], dtype=int)
        self.back = [(k, names.index(f.back)) for k, f in enumerate(model.faces) if f.back]
        self.i_set = np.array([names.index(s.name) for s in model.settings], dtype=int)
        self.room = np.array([names.index(o.name) for o in model.openings if o.kind == "room"],
                             dtype=int)  # fmt: skip
        self.flame = [(names.index(o.name), o.zone) for o in model.openings if o.kind == "flame"]
        faces = [f.name for f in model.faces]
        self.flue = [(names.index(o.name), faces.index(o.wall))
                     for o in model.openings if o.kind == "flue"]  # fmt: skip
        self.loss = np.concatenate([self.room, [i for i, _ in self.flue]]).astype(int)
        self.areas = model.exchange.areas
        self.eps_fixed = np.ones(len(names))
        for s, i in zip(model.settings, self.i_set, strict=True):
            self.eps_fixed[i] = s.emissivity
        # The zone each surface's convection comes from (-1: none, an opening)
        self.zone_of = np.full(len(names), -1, dtype=int)
        for f, i in zip(model.faces, self.i_face, strict=True):
            self.zone_of[i] = f.zone
        for k, i in self.back:
            self.zone_of[i] = model.faces[k].back_zone
        for s, i in zip(model.settings, self.i_set, strict=True):
            self.zone_of[i] = s.zone
        self.convects = self.zone_of >= 0
        self.conv = np.flatnonzero(self.convects)
        self.tall = np.array([model.gas[z].flow.height for z in self.zone_of[self.conv]])
        self.path_zone = dict(model.path_zones)
        self.stoked = model.products.fuel.kind == "wood"

    def convection(self, t_gas: Vector, fuel: float, t: Vector) -> Vector:
        """h (W/(m²·K)) on each surface (0 on an opening): its zone's duct flow, at least
        Churchill–Chu's natural convection on it; a setting at least its passages' value."""
        p = self.m.products
        m_gas = max(fuel * p.mass, 1e-9)
        forced, speed = np.empty(self.g), np.empty(self.g)
        for z, gz in enumerate(self.m.gas):
            rho, mu, k, cp = p.props(min(max(float(t_gas[z]), 300.0), 3000.0))
            speed[z] = m_gas / (rho * gz.flow.area)
            forced[z] = duct_h(rho, mu, k, cp, speed[z], gz.flow.duct, gz.flow.length)
        c = self.conv
        zones = self.zone_of[c]
        h = np.zeros(len(t))
        h[c] = np.maximum(forced[zones], natural_h(p, t_gas[zones], t[c], self.tall))
        for s, i in zip(self.m.settings, self.i_set, strict=True):
            rho, mu, k, cp = p.props(min(max(float(t_gas[s.zone]), 300.0), 3000.0))
            h[i] = max(h[i], passage_h(rho, mu, k, cp, float(speed[s.zone]), 2 * s.gap))
        return h

    def temps(self, y: Vector, t_gas: Vector) -> tuple[Vector, Vector]:
        """Every surface's temperature and emissivity."""
        lay, n = self.lay, len(self.m.names)
        t = np.empty(n)
        hot = np.array([y[h] for h, _, _ in lay.walls])
        t[self.i_face] = hot
        for k, i in self.back:
            t[i] = y[lay.walls[k][2]]
        t[self.i_set] = y[list(lay.settings)]
        t[self.room] = self.m.t_room
        for i, z in self.flame:
            t[i] = t_gas[z]
        for i, w in self.flue:
            t[i] = hot[w]
        eps = self.eps_fixed.copy()
        for k, f in enumerate(self.m.faces):
            eps[self.i_face[k]] = float(f.emissivity(np.array([hot[k]]))[0])
        for k, i in self.back:
            face = self.m.faces[k]
            line_ = face.back_emissivity or face.emissivity
            eps[i] = float(line_(np.array([t[i]]))[0])
        return t, eps

    def radiation(self, t_gas: Vector, t: Vector, eps: Vector) -> tuple[Vector, Vector]:
        ex = self.m.exchange
        if isinstance(ex, ZonesExchange):
            return ex.net(t_gas, t, eps)
        q = ex.net(float(t_gas[0]), t, eps)
        return q, np.array([-float(q.sum())])

    def released(self, t_gas: Vector, fuel: float) -> Vector:
        """F·[H_in − H_out] in each zone: air before the burning zone, the products from it."""
        p, b = self.m.products, self.m.burns
        h_out = np.array([p.air * p.h_air(float(t)) if z < b else p.mass * p.h(float(t))
                          for z, t in enumerate(t_gas)])  # fmt: skip
        h_in = np.concatenate([[p.air * p.h_air(p.t_air)], h_out[:-1]])
        h_in[b] += p.fuel_enthalpy
        return fuel * (h_in - h_out)

    def state(self, y: Vector, t_gas: Vector, fuel: float) -> State:
        t, eps = self.temps(y, t_gas)
        q_rad, q_gas = self.radiation(t_gas, t, eps)
        h = self.convection(t_gas, fuel, t)
        z = self.zone_of
        conv = np.where(self.convects, h * self.areas * (t_gas[z] - t), 0.0)
        into = q_rad + conv
        out = -q_gas + np.bincount(z[self.convects], conv[self.convects], minlength=self.g)
        for i, k in self.flame:
            out[k] -= q_rad[i]
        q_backs = np.zeros(len(self.m.faces))
        for k, i in self.back:
            q_backs[k] = into[i]
        return State(
            into[self.i_face], q_backs, into[self.i_set], float(q_rad[self.loss].sum()),
            self.released(t_gas, fuel), h, out,
        )  # fmt: skip

    def draft_residual(self, t_gas: Vector, fuel: float, m_air: float) -> float:
        """The pressure balance round the path at the zones' temperatures (Pa): buoyancy less
        losses, the air ``m_air`` drawn; each element's zone a gas zone (the first if unnamed)."""
        path = self.m.path
        assert path is not None
        temps = {name: float(t_gas[self.path_zone.get(name, 0)])
                 for name in ("firebox", "chamber", "chimney", *self.path_zone)}  # fmt: skip
        return pressure(path, m_air, temps, self.m.products, None if self.stoked else fuel)

    def fill(
        self,
        y: Vector,
        yp: Vector,
        res: Vector,
        t_gas: Vector,
        fuel: float,
        fuel_row: Callable[[State, float], float],
        held: tuple[int, Callable[[State, float], float]] | None = None,
    ) -> State:
        """Every row: each zone's gas, the walls, the settings and the accumulators here; the
        fuel's from the mode, given the state and the first setting's heat capacity (J/K); a
        setting the mode holds, (index, its row)."""
        lay, m = self.lay, self.m
        s = self.state(y, t_gas, fuel)
        res[list(lay.gases)] = (s.released - s.out) / 1e3
        for k, f in enumerate(m.faces):
            hot, c0, out = lay.walls[k]
            cells = y[c0:out]
            q = f.wall.flows(y[hot], cells, y[out])
            res[hot] = (s.q_walls[k] - q[0]) / 1e3
            res[c0:out] = f.wall.capacity(cells) * yp[c0:out] - (q[:-1] - q[1:])
            if f.back:
                res[out] = (q[-1] + s.q_backs[k]) / 1e3
            elif k == lay.grounded:
                g = m.ground
                assert g is not None
                u0, n = lay.soil
                u, up = y[u0 : u0 + n], yp[u0 : u0 + n]
                res[out] = q[-1] - g.into(u, y[out], m.t_room, yp[out])
                res[u0 : u0 + n] = g.rows(u, up, y[out], m.t_room)
            else:
                res[out] = q[-1] - f.wall.outer_loss(y[out])
        caps = np.array([st.mass * float(st.heat_capacity.cp(np.array([y[i]]))[0])
                         for st, i in zip(m.settings, lay.settings, strict=True)])  # fmt: skip
        for j, i in enumerate(lay.settings):
            res[i] = (caps[j] * yp[i] - s.q_settings[j]) / 1e3
        if held is not None:
            res[lay.settings[held[0]]] = held[1](s, float(caps[held[0]]))
        res[lay.fuel] = fuel_row(s, float(caps[0]))
        if lay.air >= 0:
            res[lay.air] = self.draft_residual(t_gas, fuel, float(y[lay.air])) / AIR_SCALE
        a = lay.acc
        net = m.products.net_heat
        walls = s.q_walls.sum() + s.q_backs.sum()
        res[a] = yp[a] - fuel
        res[a + 1] = yp[a + 1] - fuel * net / 1e6
        res[a + 2] = yp[a + 2] - (fuel * net - float(s.released.sum())) / 1e6
        res[a + 3] = yp[a + 3] - float(walls) / 1e6
        res[a + 4] = yp[a + 4] - float(s.q_settings.sum()) / 1e6
        res[a + 5] = yp[a + 5] - s.q_openings / 1e6
        if self.g > 1:
            by_zone = np.bincount([f.zone for f in m.faces], s.q_walls, minlength=self.g)
            by_zone += np.bincount([f.back_zone for f in m.faces], s.q_backs, minlength=self.g)
            res[a + 6 : a + 6 + self.g] = yp[a + 6 : a + 6 + self.g] - by_zone / 1e6
        return s

    def sparsity(self) -> NDArray[np.int_]:
        """The Jacobian's pattern: each wall's cells tridiagonal with their faces; the gases, the
        fuel, the air, every face and every setting coupled through the radiation; the
        accumulators on those."""
        lay = self.lay
        sp = np.zeros((lay.size, lay.size), dtype=int)
        hub = [*lay.gases, lay.fuel, *lay.settings, *(h for h, _, _ in lay.walls)]
        hub += [lay.walls[k][2] for k, _ in self.back]
        if lay.air >= 0:
            hub.append(lay.air)
        for r in hub:
            sp[r, hub] = 1
        for hot, c0, out in lay.walls:
            for j in range(hot, out + 1):
                sp[j, max(hot, j - 1) : min(out, j + 1) + 1] = 1
            sp[list(lay.gases), c0] = 1
            sp[lay.fuel, c0] = 1
        for a in range(lay.acc, lay.size):
            sp[a, a] = 1
            sp[a, hub] = 1
        g = self.m.ground
        if g is not None:
            u0 = lay.soil[0]
            out = lay.walls[lay.grounded][2]
            kff = g.stiffness[g.free][:, g.free]
            rows, cols = kff.nonzero()
            sp[u0 + rows, u0 + cols] = 1
            near = np.flatnonzero(np.asarray(abs(g.stiffness[g.free][:, g.disc]).sum(axis=1)))
            sp[u0 + near, out] = 1
            sp[out, u0 + near] = 1
        return sp
