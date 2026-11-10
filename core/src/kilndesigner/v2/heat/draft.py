"""The draft: a pressure balance round the gas path, burner or ash pit to chimney top (ADR 0017
H12): the buoyancy of each hot column against friction and fittings,

    Σ (ρ_room − ρ_gas)·g·Δz  =  Σ K·ρ·v²/2,

solved for the air the path draws. The friction is Darcy's on the passage's hydraulic diameter
(fluids' Clamond for Colebrook when turbulent; Idelchik's k₁·64/Re for a rectangle when laminar);
the fittings are Idelchik's 1966 rectangular forms (`fittings-and-kiln-convection.md` [D1], read
in the open AEC-tr-6630 translation): the sharp entrance 3-1, the sharp elbows 6-6 and 6-7 with
6-7's Reynolds factor, the bar grating 8-9 (8-4's thick grid), the free exit 11-1, and his own
stack example for a flue into a much larger chimney (Table 1-11, 4-1). Cantera's gas tables
(`gas.py`) take the gas's density and viscosity. What v2 writes is the path and the sum.

**The draft as a band** (ADR 0017 decision 4): where a source gives two values (an exit's 1.0 or
1.06, the grate's two cases), and brick's roughness, which no source gives (smooth to fluids'
'Rough concrete', 3.05 mm, the foot of Idelchik's "coarse" concrete, 3–9 mm), the path is drawn
at its least-air end and its most-air end (`Path.most`) is given beside it.

Stated, not sourced (each said in the working):
- Idelchik's tables hold from Re 10⁴–2·10⁵; a kiln's flues run at 3·10³–2·10⁴: the elbows take
  6-7's k_Re (45·λ_Re), held at its 3·10³ value below that; the grate and the openings are below
  their diagrams' Re (item 9: turbulent coefficients hardly change with Re above 10³);
- the fuel bed's and the setting's resistance have no source: left out, so the air is an upper
  bound (problem set §2.2).

Elements carry the zone whose gas fills them ("firebox", "chamber", "chimney"): one well-stirred
zone gives them all its temperature; zones in series give each its own.
"""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Literal

import numpy as np
from fluids.atmosphere import ATMOSPHERE_1976  # pyright: ignore[reportMissingTypeStubs]
from fluids.friction import friction_factor  # pyright: ignore[reportMissingTypeStubs]
from numpy.typing import NDArray

from kilndesigner.model import Kiln
from kilndesigner.numeric import find_root
from kilndesigner.thermal.air import air
from kilndesigner.units import si
from kilndesigner.v2.heat.gas import ATM, Products
from kilndesigner.v2.heat.sources import O2_IN_AIR
from kilndesigner.working import Step

type Vector = NDArray[np.float64]
type Kind = Literal["inlet", "grate", "duct", "fitting", "column"]

G = 9.80665
R = 8314.462618  # J/(kmol·K)
M_AIR = O2_IN_AIR.value * 31.998 + (1 - O2_IN_AIR.value) * 28.014  # kg/kmol, N2 for the rest
ROUGH = 3.05e-3  # m: fluids' 'Rough concrete'
ROUGH_NOTE = (
    "brick's roughness: no source (fluids' tables have none, nor Idelchik's Table 2-1, whose "
    "coarse concrete is 3–9 mm); a band from a smooth wall to fluids' 'Rough concrete', 3.05 mm, "
    "the draft taken at its rough end"
)
IDELCHIK = (
    "Idel'chik, Handbook of Hydraulic Resistance (AEC-tr-6630, 1966), as read in "
    "fittings-and-kiln-convection.md [D1]"
)
FITTINGS_NOTE = (
    "the fittings Idelchik's rectangular forms (3-1, 6-6, 6-7, 8-4, 8-9, 11-1; Table 1-11): his "
    "tables hold from Re 10⁴–2·10⁵, a kiln's flues run at 3·10³–2·10⁴, so the elbows take 6-7's "
    "k_Re = 45·λ_Re (held at its 3·10³ value below), and the grate and openings are taken below "
    "their diagrams' Re (his item 9); each two-valued coefficient a band, the least-air end used"
)
LEFT_OUT = (
    "the fuel bed's and the setting's resistance have no source: left out, so the air is an "
    "upper bound (problem set §2.2)"
)
SHARP_ENTRANCE = 0.5  # 3-1: an entrance flush in a wall, any edge
EXIT = (1.0, 1.06)  # 11-1: a free exit, uniform, and a developed (m = 7) profile
LAMINAR_RE = 2000.0  # Idelchik §2: laminar below Re 2000
# Diagram 2-1: laminar friction in a rectangle, λ = k₁·64/Re, k₁ against a₀/b₀ (short ÷ long)
K1_RATIO = (0.0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0)
K1 = (1.50, 1.34, 1.20, 1.02, 0.94, 0.90, 0.89)
# Diagram 6-6: a sharp elbow into a narrower or wider passage, ζ₁ on the inlet's velocity, by
# b₁/b₀ (the exit's side in the plane of the turn over the inlet's) and by a₀/b₀ (the side normal
# to the turn over the inlet's side in it), read as b₀/a₀ 4 (a₀/b₀ 0.25), 1, 0.25 (4) and 0 (∞)
TURN_B = (0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 2.0)
TURN_A = (0.0, 0.25, 1.0, 4.0)  # b₀/a₀
TURN = (
    (1.50, 1.04, 0.79, 0.69, 0.63, 0.60, 0.55),  # a₀/b₀ ∞
    (1.46, 1.10, 0.90, 0.81, 0.76, 0.72, 0.66),  # 4.0
    (1.70, 1.36, 1.15, 1.02, 0.95, 0.90, 0.84),  # 1.0
    (1.76, 1.43, 1.24, 1.14, 1.09, 1.06, 1.06),  # 0.25
)
# Diagram 8-4: the thick grid's τ against l/d_h; 8-9's round bars (Table 8-2, shape 7)
TAU_L = (0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.4, 2.0, 3.0)
TAU = (1.35, 1.22, 1.10, 0.84, 0.42, 0.24, 0.10, 0.02, 0.0)
GRID_FRICTION = 0.02  # 8-4 tabulated at λ = 0.02
ROUND_BETA = (1.73, 0.74)  # β₁ (case a) and β₂ (case b) for round bars


def hydraulic(width: float, height: float) -> float:
    return 2 * width * height / (width + height)


@dataclass(frozen=True)
class Element:
    """One piece of the path. ``area`` is the flow area of one branch, the velocity's; ``zone``
    the gas filling it ("room" for the cold air). A duct's friction comes from its length and
    hydraulic diameter (``k1`` Idelchik's laminar factor for its shape), a fitting's from ``k``
    (the least-air end of its band; ``k_lo`` the most-air end, the same unless two sources' values
    differ), times 6-7's Reynolds factor on the passage of diameter ``re_dh`` where it is given; a
    column's buoyancy from ``rise`` (up +)."""

    name: str
    kind: Kind
    zone: str
    area: float = 0.0
    branches: int = 1
    k: float = 0.0
    length: float = 0.0
    dh: float = 0.0
    rise: float = 0.0
    note: str = ""
    k_lo: float | None = None
    k1: float = 1.0
    re_dh: float = 0.0
    re_lo: bool = True  # the most-air end takes the Reynolds factor too
    sides: tuple[float, float] | None = None  # a rectangular duct's

    def coefficient(self, most: bool) -> float:
        """The fitting's coefficient at the band's least-air end, or its most-air end."""
        return self.k_lo if most and self.k_lo is not None else self.k

    def by_re(self, most: bool) -> bool:
        """Whether the coefficient takes 6-7's Reynolds factor at this end of the band."""
        return self.re_dh > 0 and (self.re_lo or not most)


@dataclass(frozen=True)
class Path:
    """A gas path: its elements in order, the room's temperature and the air's pressure; drawn at
    its band's least-air end (rough walls, each fitting's higher coefficient), or its most-air end
    (``most``: a smooth wall, the lower)."""

    elements: tuple[Element, ...]
    t_room: float
    pressure: float = ATM
    rough: float = ROUGH
    steps: tuple[Step, ...] = ()
    most_air: bool = False

    @property
    def room_density(self) -> float:
        return self.pressure * M_AIR / (R * self.t_room)

    def most(self) -> Path:
        """The path at its band's most-air end: a smooth wall, each fitting's lower coefficient."""
        return Path(self.elements, self.t_room, self.pressure, 0.0, self.steps, True)


def k_re(re: float) -> float:
    """Idelchik's Reynolds factor for sharp elbows (diagram 6-7, Table 6-11): 45·λ_Re for
    3·10³ < Re < 4·10⁴, λ_Re = (1.8 lg Re − 1.64)⁻² the smooth pipe's (item 13), 1 from 4·10⁴;
    held at its 3·10³ value below (the diagram gives none: said)."""
    if re >= 4e4:
        return 1.0
    r = max(re, 3e3)
    return max(1.0, 45.0 * (1.8 * math.log10(r) - 1.64) ** -2)


def darcy(re: float, rel_rough: float, k1: float = 1.0) -> float:
    """Darcy's friction factor: Idelchik's k₁·64/Re below Re 2000 (diagram 2-1), Colebrook above
    (fluids' Clamond), on the hydraulic diameter."""
    if re < LAMINAR_RE:
        return k1 * 64.0 / max(re, 1e-3)
    return float(friction_factor(re, rel_rough))


@dataclass(frozen=True)
class Draft:
    """The air the path draws, the gas it carries, and each element's buoyancy and loss (Pa)."""

    air: float  # kg/s
    gas: float  # kg/s
    terms: tuple[tuple[str, float, float], ...]


def _state(path: Path, zone: str, temps: Mapping[str, float], prod: Products) -> tuple[float, ...]:
    """ρ and μ of the fluid in a zone, at the path's pressure."""
    if zone == "room":
        return path.room_density, air(path.t_room).viscosity
    rho, mu, _, _ = prod.props(temps[zone])
    return rho * path.pressure / ATM, mu


def balance(
    path: Path,
    m_air: float,
    temps: Mapping[str, float],
    prod: Products,
    gas_of: Callable[[float], float],
) -> Draft:
    """Each element's buoyancy and loss at an air flow (kg/s); ``gas_of`` gives the gas flow."""
    m_gas = gas_of(m_air)
    rho_room = path.room_density
    terms: list[tuple[str, float, float]] = []
    for e in path.elements:
        rho, mu = _state(path, e.zone, temps, prod)
        m = (m_air if e.zone == "room" else m_gas) / e.branches
        if e.kind == "column":
            terms.append((e.name, (rho_room - rho) * G * e.rise, 0.0))
            continue
        v = m / (rho * e.area)
        k = e.coefficient(path.most_air)
        if e.kind == "duct":
            re = rho * v * e.dh / mu
            k = darcy(re, path.rough / e.dh, e.k1) * e.length / e.dh
        elif e.by_re(path.most_air):
            k *= k_re(rho * v * e.re_dh / mu)
        terms.append((e.name, 0.0, k * rho * v * v / 2))
    return Draft(m_air, m_gas, tuple(terms))


def pressure(
    path: Path,
    m_air: float,
    temps: Mapping[str, float],
    prod: Products,
    fuel: float | None = None,
) -> float:
    """The path's buoyancy less its losses (Pa) at an air flow (kg/s): zero at the air it draws,
    damper open. Stoked (``fuel`` None) the gas is air × products ÷ air; burners add their fuel."""

    def gas_of(m: float) -> float:
        return m * prod.mass / prod.air if fuel is None else m + fuel

    d = balance(path, abs(m_air), temps, prod, gas_of)
    lift = sum(b for _, b, _ in d.terms)
    loss = sum(x for _, _, x in d.terms)
    return lift - math.copysign(loss, m_air)  # a flow pushed backwards is pushed back


def draw(
    path: Path,
    temps: Mapping[str, float],
    prod: Products,
    fuel: float | None = None,
) -> Draft:
    """The air the path draws with its hot zones at ``temps`` (K), the damper open. Stoked
    (``fuel`` None): the fuel burns at the products' λ, so the gas is air × products ÷ air.
    Fixed fuel (kg/s): the gas is the air plus the fuel. No net buoyancy: no flow."""

    def gas_of(m_air: float) -> float:
        if fuel is None:
            return m_air * prod.mass / prod.air
        return m_air + fuel

    def residual(m_air: float) -> float:
        d = balance(path, m_air, temps, prod, gas_of)
        return sum(b for _, b, _ in d.terms) - sum(loss for _, _, loss in d.terms)

    if residual(0.0) <= 0:
        return balance(path, 0.0, temps, prod, gas_of)
    hi = 0.01
    while residual(hi) > 0:
        hi *= 2
    m = find_root(residual, 0.0, hi, xtol=1e-12)
    return balance(path, m, temps, prod, gas_of)


@dataclass(frozen=True)
class Table:
    """The most air the path draws (damper open) against one gas temperature in every zone."""

    temps: Vector
    air: Vector
    smooth: Vector
    steps: tuple[Step, ...] = field(default=())

    def at(self, t: float) -> float:
        return float(np.interp(t, self.temps, self.air))


TABLE_TEMPS = np.array([
    300, 350, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700,
    1800, 2000, 2200,
], dtype=float)  # fmt: skip


def table(
    path: Path,
    prod: Products,
    zones: Sequence[str] = ("firebox", "chamber", "chimney"),
    fuel: float | None = None,
) -> Table:
    """The draft table: the air at each gas temperature, every hot zone at it (one zone), at the
    least-air end of the band and at its most-air end (`Path.most`)."""
    rough, smooth = [], []
    smooth_path = path.most()
    for t in TABLE_TEMPS:
        temps = dict.fromkeys(zones, float(t))
        rough.append(draw(path, temps, prod, fuel).air)
        smooth.append(draw(smooth_path, temps, prod, fuel).air)
    r, s = np.array(rough), np.array(smooth)
    i = int(np.argmin(abs(TABLE_TEMPS - 1573.15)))
    step = Step(
        name="The most air the draft draws, damper open",
        value=", ".join(
            f"{TABLE_TEMPS[j] - 273.15:.0f} °C: {r[j]:.4f} kg/s" for j in (1, 4, i, len(r) - 1)
        ),
        formula="Σ (ρ_room − ρ_gas)·g·Δz = Σ K·ρ·v²/2, solved for the air",
        inputs={
            "the band's most-air end at 1300 °C": f"{s[i]:.4f} kg/s",
            "λ": f"{prod.air_ratio:.3f}",
        },
        reference=f"{IDELCHIK}; fluids 1.3 (Clamond's Colebrook); Cantera's gas",
        note=f"{ROUGH_NOTE}; {FITTINGS_NOTE}; {LEFT_OUT}",
    )
    return Table(TABLE_TEMPS.copy(), r, s, (*path.steps, step))


# --- the parts a path is built from --------------------------------------------------------------


def inlet(name: str, area: float, branches: int = 1) -> Element:
    """Room air entering through an opening flush in a wall: Idelchik's 3-1, 0.50 for any edge."""
    return Element(name, "inlet", "room", area, branches, k=SHARP_ENTRANCE)


def grid_tau(l_dh: float) -> float:
    """Diagram 8-4's τ, the thick grid's jet factor, against the passage's depth over its d_h."""
    return float(np.interp(l_dh, TAU_L, TAU))


def bar_grate(gap: float, bar: float) -> tuple[float, float]:
    """A grate of round bars, Idelchik's 8-9 at θ 90°, ζ on the approach velocity over the grate's
    whole area: case (b), any depth, β₂·ζ′ with ζ′ 8-4's thick grid [(0.5 + τ√(1 − f))(1 − f) +
    (1 − f)² + λ·l/d_h]/f² (f = gap/(gap + bar), l the bar's depth, its diameter, d_h = 2·gap, a
    slot's), and case (a), β₁·(S₁/a₀ − 1)^(4/3), drawn for bars five times as deep as thick: the
    two as a band (lower, higher)."""
    f = gap / (gap + bar)
    l_dh = bar / (2 * gap)
    tau = grid_tau(l_dh)
    zeta = ((0.5 + tau * math.sqrt(1 - f)) * (1 - f) + (1 - f) ** 2 + GRID_FRICTION * l_dh) / f**2
    b = ROUND_BETA[1] * zeta
    a = ROUND_BETA[0] * ((gap + bar) / gap - 1) ** (4 / 3)
    return min(a, b), max(a, b)


def grate(
    name: str, width: float, length: float, gap: float, bar: float, branches: int = 1
) -> Element:
    """A grate of round bars (Idelchik 8-9, `bar_grate`), on the approach velocity over the
    grate's whole area; the band's higher case drawn, the lower beside it."""
    lo, hi = bar_grate(gap, bar)
    return Element(name, "grate", "room", width * length, branches, k=hi, k_lo=lo,
                   note=f"open fraction {gap / (gap + bar):.2f}, ζ {lo:.2f}–{hi:.2f}")  # fmt: skip


def laminar_k1(width: float, height: float) -> float:
    """Diagram 2-1's k₁ for a rectangle's laminar friction, by its short side over its long."""
    return float(np.interp(min(width, height) / max(width, height), K1_RATIO, K1))


def duct(
    name: str,
    zone: str,
    width: float,
    height: float,
    length: float,
    branches: int = 1,
    rnd: bool = False,
) -> Element:
    """A passage's friction (Darcy f·L/D_h, `darcy`): a rectangle, or round of diameter
    ``width`` when ``rnd``."""
    if rnd:
        return Element(name, "duct", zone, math.pi * width**2 / 4, branches, length=length,
                       dh=width)  # fmt: skip
    return Element(name, "duct", zone, width * height, branches, length=length,
                   dh=hydraulic(width, height), k1=laminar_k1(width, height),
                   sides=(width, height))  # fmt: skip


def elbow(b1_b0: float, a0_b0: float) -> float:
    """Idelchik's 6-6, a sharp 90° elbow of rectangular section into a narrower or wider passage:
    ζ₁ on the inlet's velocity, bilinear in b₁/b₀ and b₀/a₀ over the diagram's grid, held at its
    edges (0.6–2.0; a₀/b₀ 0.25–∞)."""
    b = min(max(b1_b0, TURN_B[0]), TURN_B[-1])
    x = min(max(1.0 / a0_b0, TURN_A[0]), TURN_A[-1])
    rows = [float(np.interp(b, TURN_B, r)) for r in TURN]
    return float(np.interp(x, TURN_A, rows))


def turn(
    name: str,
    zone: str,
    across: float,
    b0: float,
    b1: float,
    branches: int = 1,
) -> Element:
    """A sharp 90° turn from a passage ``across`` × ``b0`` (``b0`` its side in the plane of the
    turn) into one whose side in that plane is ``b1``, the same across: 6-6 × k_Re on the inlet's
    velocity (a firebox's channel turning up into its inlet flue)."""
    z = elbow(b1 / b0, across / b0)
    held = not TURN_B[0] <= b1 / b0 <= TURN_B[-1]
    note = f"6-6 at b₁/b₀ {b1 / b0:.2f}, a₀/b₀ {across / b0:.2f}: ζ₁ {z:.2f}" + (
        " (held at the diagram's edge)" if held else ""
    )
    return Element(name, "fitting", zone, across * b0, branches, k=z, re_dh=hydraulic(across, b0),
                   note=note)  # fmt: skip


def turn_up(
    name: str,
    zone: str,
    across: float,
    b0: float,
    b1: float,
    a_flue: float,
    a_stack: float,
) -> Element:
    """A flue turning up into its chimney, on the flue's velocity: with the chimney's depth along
    the flue at most twice the flue's height, 6-6 × k_Re; deeper, a band from Idelchik's own stack
    example, the sudden expansion (1 − F₀/F₁)² alone (Table 1-11, 4-1), to 6-6 held at b₁/b₀ 2."""
    z = elbow(b1 / b0, across / b0)
    dh = hydraulic(across, b0)
    if b1 / b0 <= TURN_B[-1]:
        note = f"6-6 at b₁/b₀ {b1 / b0:.2f}, a₀/b₀ {across / b0:.2f}: ζ₁ {z:.2f}"
        return Element(name, "fitting", zone, a_flue, k=z, re_dh=dh, note=note)
    expansion = (1 - a_flue / a_stack) ** 2
    note = (
        f"a chimney {b1 / b0:.1f} × the flue's height deep: 6-6 held at b₁/b₀ 2, {z:.2f} × k_Re, "
        f"to the sudden expansion {expansion:.2f} (Idelchik's stack, Table 1-11)"
    )
    return Element(name, "fitting", zone, a_flue, k=z, k_lo=expansion, re_dh=dh, re_lo=False,
                   note=note)  # fmt: skip


def entrance(name: str, zone: str, area: float, branches: int = 1) -> Element:
    """Gas entering a passage flush in the wall of a larger space: 3-1's 0.50."""
    return Element(name, "fitting", zone, area, branches, k=SHARP_ENTRANCE)


def outlet(name: str, zone: str, area: float, branches: int = 1) -> Element:
    """A jet leaving a passage into a large space, its velocity head lost: 11-1's 1.0 for a
    uniform jet to 1.06 for a developed (m = 7) profile."""
    return Element(name, "fitting", zone, area, branches, k=EXIT[1], k_lo=EXIT[0])


def column(name: str, zone: str, rise: float) -> Element:
    return Element(name, "column", zone, rise=rise)


# --- a path from a design file -------------------------------------------------------------------


class NotModelledError(ValueError):
    """The design doesn't give what the path needs, or v2 doesn't build this path yet."""


def _thickness(kiln: Kiln, face: str) -> float:
    return sum(si(x.thickness, "m") for x in kiln.lining.for_face(face))  # pyright: ignore[reportArgumentType]


def _port_area(w: float, h: float, rnd: bool) -> float:
    return math.pi * w * w / 4 if rnd else w * h


def kiln_path(kiln: Kiln, *, grate_bar: float | None = None, rough: float = ROUGH) -> Path:
    """The gas path of a design: under-floor stoked fireboxes or gas burners' ports, the chamber,
    the exit flue and the chimney, as the design gives them (z from the chamber's floor).

    ``grate_bar``: the grate's bar thickness (m), which the design file doesn't carry (the
    fast-fire's ¾ in rod is printed, Olsen p.204); without it the grate's loss is left out and
    said so. Refused: a design with no chimney or exit flue given (the engine's rule-sized
    defaults are v1's and aren't a kiln's own draft), and paths v2 doesn't build yet."""
    draft = kiln.draft
    if draft is None or draft.chimney is None:
        raise NotModelledError(
            "the design gives no chimney, so its draft can't be worked out (the engine's "
            "rule-sized chimney isn't the kiln's own)"
        )
    if draft.flue_port is None or draft.exits is not None or draft.chimneys != 1:
        raise NotModelledError(
            "v2's draft takes one exit flue (draft.flue_port) into one chimney; several exits "
            "or chimneys aren't built yet"
        )
    if draft.chimney_through != "beside" or draft.type == "up":
        raise NotModelledError("a chimney through the crown or over an up-draft isn't built yet")
    t_room = si(kiln.site.ambient, "K")
    pressure = ATM
    notes: list[str] = []
    if kiln.site.elevation is not None:
        z_site = si(kiln.site.elevation, "m")
        pressure = float(ATMOSPHERE_1976(z_site).P)
        notes.append(f"{z_site:.0f} m up: {pressure:.0f} Pa (US Standard Atmosphere 1976, fluids)")
    els: list[Element] = []
    fire, gas_heat = kiln.heat.fire, kiln.heat.gas
    if fire is not None and gas_heat is None:
        boxes = fire.fireboxes
        if len(boxes) != 1 or boxes[0].position != "under" or boxes[0].inlet is None:
            raise NotModelledError(
                "v2's draft takes one set of fireboxes under the floor with their inlet flues; "
                "fireboxes against a wall aren't built yet"
            )
        fb = boxes[0]
        assert fb.inlet is not None
        n = fb.count
        t_floor = _thickness(kiln, "floor")
        fw = si(fb.width, "m")
        fh = si(fb.height, "m") if fb.height is not None else fw
        pit = si(fb.ash_pit, "m") if fb.ash_pit is not None else fh
        els.append(inlet("ash-pit mouth (the firebox's width by the ash pit's depth)", fw * pit, n))
        if fb.grate is not None and fb.grate.gap is not None and grate_bar is not None:
            gw, gl = si(fb.grate.width, "m"), si(fb.grate.length, "m")
            els.append(grate("grate, round bars (Idelchik 8-9)", gw, gl, si(fb.grate.gap, "m"),
                             grate_bar, n))  # fmt: skip
        else:
            notes.append("the grate's loss left out: its bars' size isn't given")
        notes.append("the fuel bed's resistance: no source, left out")
        els.append(column("firebox and inlet flue, grate to the chamber floor", "firebox",
                          t_floor + fh))  # fmt: skip
        run = si(fb.grate.length, "m") / 2 if fb.grate is not None else si(fb.length, "m") / 2
        els.append(duct("firebox, the gas's run off the grate (half its length)", "firebox",
                        fw, fh, run, n))  # fmt: skip
        iw, ih = fb.inlet.size_in()
        ia = _port_area(iw * 0.0254, ih * 0.0254, fb.inlet.round)
        k = n * fb.inlets
        share = fw / fb.inlets  # each inlet's share of the channel's width
        els.append(turn("into the inlet flue, a sharp turn up", "firebox", share, fh, ia / share,
                        k))  # fmt: skip
        if abs(iw * 0.0254 - share) > 1e-3:
            notes.append(
                "an inlet flue narrower or wider than its share of the channel: 6-6 taken on its "
                "area over that share (6-6 keeps the side normal to the turn)"
            )
        els.append(duct("inlet flue, through the floor", "firebox", iw * 0.0254, ih * 0.0254,
                        t_floor, k, rnd=fb.inlet.round))  # fmt: skip
        els.append(outlet("inlet flue into the chamber", "firebox", ia, k))
        z_in = 0.0
    elif gas_heat is not None and fire is None:
        from kilndesigner.firebox_parts import burner_port_in

        size = burner_port_in(kiln)
        count = gas_heat.burners.count
        if size is None or count is None or gas_heat.burners.wall == "floor":
            raise NotModelledError(
                "the burners' port size or count isn't given, or they fire up through the "
                "floor (not built yet)"
            )
        pw, ph = size[0] * 0.0254, size[1] * 0.0254
        pa = _port_area(pw, ph, size[2])
        wall = _thickness(kiln, gas_heat.burners.wall)
        els.append(inlet("burner ports, room air round the burners", pa, count))
        els.append(duct("burner ports, through the wall", "room", pw, ph, wall, count,
                        rnd=size[2]))  # fmt: skip
        els.append(outlet("burner ports into the chamber", "room", pa, count))
        notes.append(
            "all the air taken as drawn through the burner ports by the draft: the venturi's own "
            "pumping isn't modelled (no source), and the burner tube in the port is ignored"
        )
        z_in = (
            si(gas_heat.burners.up, "m")
            if gas_heat.burners.up is not None
            else (
                0.0635 + ph / 2  # a 2½ in course up, as the engine lays the ports (Pitelka [S4])
            )
        )
    else:
        raise NotModelledError("v2's draft takes one kind of heat: fireboxes or gas burners")
    ew, eh = (x * 0.0254 for x in draft.flue_port.size_in())
    ea = _port_area(ew, eh, draft.flue_port.round)
    z_exit = eh / 2  # at the foot of the flue wall, as the engine lays it
    els.append(column("chamber, inlet to the exit flue's middle", "chamber", z_exit - z_in))
    els.append(entrance("exit flue, sharp entrance", "chamber", ea))
    els.append(duct("exit flue, through the flue wall", "chamber", ew, eh,
                    _thickness(kiln, draft.flue_wall), rnd=draft.flue_port.round))  # fmt: skip
    chim = draft.chimney
    if chim.inside is None:
        raise NotModelledError("the chimney's inside section isn't given")
    rnd = chim.inside.diameter is not None
    if chim.inside.diameter is not None:
        cw = cd = si(chim.inside.diameter, "m")
        ca = math.pi * cw * cw / 4
    else:
        assert chim.inside.width is not None
        assert chim.inside.depth is not None
        cw, cd = si(chim.inside.width, "m"), si(chim.inside.depth, "m")
        ca = cw * cd
    run = si(draft.run_to_chimney, "m")
    if run > 0:
        els.append(duct("the run to the chimney", "chimney", ew, eh, run,
                        rnd=draft.flue_port.round))  # fmt: skip
    # A round flue or chimney as the square of its area (Idelchik item 12: as circular)
    side = math.sqrt(math.pi / 4)
    fa, fb0 = (ew * side, eh * side) if draft.flue_port.round else (ew, eh)
    els.append(turn_up("turn up into the chimney", "chimney", fa, fb0, cd * (side if rnd else 1),
                       ea, ca))  # fmt: skip
    height = si(chim.height, "m") - z_exit
    els.append(column("chimney", "chimney", height))
    els.append(duct("chimney", "chimney", cw, cd, height, rnd=rnd))
    els.append(outlet("chimney top", "chimney", ca))
    odd = [e.name for e in els if e.sides is not None
           and not 0.5 <= e.sides[0] / e.sides[1] <= 2.0]  # fmt: skip
    if odd:
        notes.append(
            "turbulent friction as a circle's on D_h for "
            + ", ".join(odd)
            + ": past Idelchik's 0.5–2 side ratio for that (item 17), none other read"
        )
    steps = (
        Step(
            name="The gas path",
            value=" → ".join(e.name for e in els if e.kind != "column"),
            inputs={e.name: f"Δz {e.rise:.3f} m" for e in els if e.kind == "column"}
            | {e.name: e.note for e in els if e.note},
            reference=f"the design file; the fittings from {IDELCHIK}; friction fluids 1.3",
            note="; ".join([*notes, FITTINGS_NOTE]),
        ),
    )
    return Path(tuple(els), t_room, pressure, rough, steps)
