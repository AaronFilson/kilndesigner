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
zone gives them all its temperature; zones in series give each its own. A zone the model doesn't
have takes its path's alias (`Path.alias`: a chimney that isn't a zone of its own takes the last
chamber's gas), then its kind ("chamber 3" → "chamber").

**Parallel branches** (C1: several fireboxes, exit sets or chimneys, a chamber's side stoke holes
beside the front's path): a group of branches from one node to the next, each branch its elements
in order, the flow splitting so every branch has the same buoyancy less losses across it, the
junction's draft D; no branch carries flow backwards (one whose buoyancy is under D carries none,
said where it happens). Identical branches are one branch of ``branches`` (as before).

**Geometric bands**: where a length is a band (a chimney's height no source gives, a scaled width),
the path is built at each end and its most-air end carried beside it (`Path.alt`).
"""

from __future__ import annotations

import math
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from typing import Any, Literal

import numpy as np
from fluids.friction import friction_factor  # pyright: ignore[reportMissingTypeStubs]
from numpy.typing import NDArray

from kilndesigner.model import Kiln
from kilndesigner.numeric import find_root
from kilndesigner.thermal.air import air
from kilndesigner.v2.heat.gas import ATM, Products
from kilndesigner.v2.heat.sources import O2_IN_AIR
from kilndesigner.working import Step

type Vector = NDArray[np.float64]
type Kind = Literal["inlet", "grate", "duct", "fitting", "column", "parallel"]

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
TURBULENT_RE = 2300.0  # Lienhard eq. 7.41: the turbulent correlations from here (zone.py's)
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
    column's buoyancy from ``rise`` (up +). A parallel group (kind "parallel") holds its branches
    in ``parts``, each its elements in order (`balance` splits the flow among them)."""

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
    parts: tuple[tuple[Element, ...], ...] = ()

    def coefficient(self, most: bool) -> float:
        """The fitting's coefficient at the band's least-air end, or its most-air end."""
        return self.k_lo if most and self.k_lo is not None else self.k

    def by_re(self, most: bool) -> bool:
        """Whether the coefficient takes 6-7's Reynolds factor at this end of the band."""
        return self.re_dh > 0 and (self.re_lo or not most)


def _zones(els: Sequence[Element]) -> list[str]:
    out: list[str] = []
    for e in els:
        names = [z for b in e.parts for z in _zones(b)] if e.kind == "parallel" else [e.zone]
        for z in names:
            if z != "room" and z not in out:
                out.append(z)
    return out


def _open(e: Element, share: float) -> Element:
    """An element with its air intakes a ``share`` open (`Path.opened`)."""
    if e.kind == "parallel":
        return replace(e, parts=tuple(tuple(_open(x, share) for x in b) for b in e.parts))
    if not e.name.startswith(INTAKE):
        return e
    return replace(e, k=e.k / share**2, k_lo=None if e.k_lo is None else e.k_lo / share**2)


@dataclass(frozen=True)
class Path:
    """A gas path: its elements in order, the room's temperature and the air's pressure; drawn at
    its band's least-air end (rough walls, each fitting's higher coefficient), or its most-air end
    (``most``: a smooth wall, the lower). ``alias``: the zone each zone the model may not have
    takes its gas from; ``alt``: the most-air end's elements, where a length is a band;
    ``left_out``: what the path leaves out for want of a size, so its air is an upper bound."""

    elements: tuple[Element, ...]
    t_room: float
    pressure: float = ATM
    rough: float = ROUGH
    steps: tuple[Step, ...] = ()
    most_air: bool = False
    alias: tuple[tuple[str, str], ...] = ()
    alt: tuple[Element, ...] | None = None
    left_out: tuple[str, ...] = ()

    @property
    def room_density(self) -> float:
        return self.pressure * M_AIR / (R * self.t_room)

    @property
    def zones(self) -> tuple[str, ...]:
        """The gas zones its elements name, in the gas's order (not the room)."""
        return tuple(_zones(self.elements))

    def most(self) -> Path:
        """The path at its band's most-air end: a smooth wall, each fitting's lower coefficient,
        each length band at its most-air end."""
        els = self.alt if self.alt is not None else self.elements
        return replace(self, elements=els, rough=0.0, most_air=True, alt=None)

    def opened(self, share: float) -> Path:
        """The path with its air intakes a ``share`` open (the stoker's bricks): each intake's area
        × the share, so its coefficient on the full area ÷ share² (`Intakes`)."""
        if not 0 < share <= 1:
            raise ValueError("the intakes are open by a share of more than 0, at most 1")
        if share == 1:
            return self
        alt = None if self.alt is None else tuple(_open(e, share) for e in self.alt)
        return replace(self, elements=tuple(_open(e, share) for e in self.elements), alt=alt)


INTAKE = "air intakes"  # the name an intakes element starts with
# An opening in a wall or a bricked door into the firebox: an orifice, C 0.65–0.70
# (combustion-and-masonry.md §4.2 [S42]; Prahl & Emmons' 0.68 for windows, as COMPF2 takes it,
# grates-and-fuel-beds.md [G11]), K = 1/C² on its own area
ORIFICE_C = (0.65, 0.70)


@dataclass(frozen=True)
class Intakes:
    """A firebox set's air intakes, all its fireboxes together (m²), each a band (least, most):
    below the grate (the ash-pit mouths, primary air through the grate and the bed) and above it
    (the stoke holes and air holes, secondary air over the bed); where they come from
    (`firebox-air-intakes.md`; the dataset's `primary_air` and `secondary_air`)."""

    primary: tuple[float, float]
    secondary: tuple[float, float] = (0.0, 0.0)
    reference: str = ""

    def __post_init__(self) -> None:
        for lo, hi in (self.primary, self.secondary):
            if not 0 <= lo <= hi:
                raise ValueError("an intake's area band runs from its least to its most, ≥ 0")
        if self.primary[1] + self.secondary[1] <= 0:
            raise ValueError("a firebox needs an air intake")


def intakes(
    ins: Intakes, grate_area: float, grate_k: tuple[float, float] | None, branches: int
) -> Element:
    """The intakes as one inlet: the openings below the grate (a mouth flush in the wall, 3-1's
    0.50, then the grate's ζ on its own area, Idelchik 8-9) in parallel with those above it (an
    orifice, K = 1/C²), at one pressure drop, Σ A_i/√K_i; on the most primary area. Its band's
    least-air end the least areas at the higher coefficients, its most-air end the most at the
    lower."""
    ref_area = ins.primary[1] if ins.primary[1] > 0 else ins.secondary[1]

    def k_eq(primary: float, secondary: float, zeta: float, c: float) -> float:
        k_p = SHARP_ENTRANCE + (zeta * (primary / grate_area) ** 2 if grate_area > 0 else 0.0)
        flow = (primary / math.sqrt(k_p) if primary > 0 else 0.0) + secondary * c
        return (ref_area / flow) ** 2

    z_lo, z_hi = grate_k if grate_k is not None else (0.0, 0.0)
    least = k_eq(ins.primary[0], ins.secondary[0], z_hi, ORIFICE_C[0])
    most = k_eq(ins.primary[1], ins.secondary[1], z_lo, ORIFICE_C[1])
    note = (
        f"below the grate {ins.primary[0] / 0.0254**2:.0f}–{ins.primary[1] / 0.0254**2:.0f} in², "
        f"above it {ins.secondary[0] / 0.0254**2:.0f}–{ins.secondary[1] / 0.0254**2:.0f} in²: "
        f"K {least:.2f}–{most:.2f} on {ref_area / 0.0254**2:.0f} in²"
    )
    return Element(f"{INTAKE}, below and above the grate, in parallel", "inlet", "room",
                   ref_area / branches, branches, k=least, k_lo=most, note=note)  # fmt: skip


def k_re(re: float) -> float:
    """Idelchik's Reynolds factor for sharp elbows (diagram 6-7, Table 6-11): 45·λ_Re for
    3·10³ < Re < 4·10⁴, λ_Re = (1.8 lg Re − 1.64)⁻² the smooth pipe's (item 13), 1 from 4·10⁴;
    held at its 3·10³ value below (the diagram gives none: said)."""
    if re >= 4e4:
        return 1.0
    r = max(re, 3e3)
    return max(1.0, 45.0 * (1.8 * math.log10(r) - 1.64) ** -2)


def darcy(re: float, rel_rough: float, k1: float = 1.0) -> float:
    """Darcy's friction factor: Idelchik's k₁·64/Re below Re 2000 (diagram 2-1), Colebrook from
    Re 2300 (fluids' Clamond; Lienhard's start of the turbulent correlations, as `zone.py`'s), on
    the hydraulic diameter; between, straight from the one to the other (Derived: a bridge, so the
    pressure balance has no step there for the max fire's Newton iteration to fail on, C3a)."""
    if re < LAMINAR_RE:
        return k1 * 64.0 / max(re, 1e-3)
    if re < TURBULENT_RE:
        w = (re - LAMINAR_RE) / (TURBULENT_RE - LAMINAR_RE)
        return (1 - w) * k1 * 64.0 / LAMINAR_RE + w * float(
            friction_factor(TURBULENT_RE, rel_rough)
        )
    return float(friction_factor(re, rel_rough))


@dataclass(frozen=True)
class Draft:
    """The air the path draws, the gas it carries, and each element's buoyancy and loss (Pa); for
    each parallel group, the air through each of its branches (kg/s)."""

    air: float  # kg/s
    gas: float  # kg/s
    terms: tuple[tuple[str, float, float], ...]
    shares: tuple[tuple[str, tuple[float, ...]], ...] = ()


def zone_temperature(path: Path, zone: str, temps: Mapping[str, float]) -> float:
    """A zone's gas temperature (K): its own, else its alias's (`Path.alias`, followed on), else
    the kind of either ("chamber 3" → "chamber")."""
    alias = dict(path.alias)
    chain = [zone]
    while chain[-1] in alias and len(chain) < 8:
        chain.append(alias[chain[-1]])
    for z in (*chain, *(c.split(" ", 1)[0] for c in chain)):
        if z in temps:
            return temps[z]
    raise KeyError(f"no gas temperature for the path's {zone} zone")


class _Props:
    """ρ and μ of the fluid in each zone at the path's pressure, worked out once a balance."""

    def __init__(self, path: Path, temps: Mapping[str, float], prod: Products) -> None:
        self.path, self.temps, self.prod = path, temps, prod
        self.cache: dict[str, tuple[float, float]] = {
            "room": (path.room_density, air(path.t_room).viscosity)
        }

    def __call__(self, zone: str) -> tuple[float, float]:
        if zone not in self.cache:
            rho, mu, _, _ = self.prod.props(zone_temperature(self.path, zone, self.temps))
            self.cache[zone] = (rho * self.path.pressure / ATM, mu)
        return self.cache[zone]


def _term(
    path: Path, e: Element, m_air: float, m_gas: float, props: _Props, shares: list[Any]
) -> tuple[str, float, float]:
    """One element's (name, buoyancy, loss) at the path's air and gas flows (kg/s)."""
    if e.kind == "parallel":
        lift, loss = _split(path, e, m_air, m_gas, props, shares)
        return e.name, lift, loss
    rho, mu = props(e.zone)
    if e.kind == "column":
        return e.name, (path.room_density - rho) * G * e.rise, 0.0
    m = (m_air if e.zone == "room" else m_gas) / e.branches
    v = m / (rho * e.area)
    k = e.coefficient(path.most_air)
    if e.kind == "duct":
        re = rho * v * e.dh / mu
        k = darcy(re, path.rough / e.dh, e.k1) * e.length / e.dh
    elif e.by_re(path.most_air):
        k *= k_re(rho * v * e.re_dh / mu)
    return e.name, 0.0, k * rho * v * v / 2


def _branch(
    path: Path, els: Sequence[Element], m_air: float, m_gas: float, props: _Props
) -> tuple[float, float]:
    """A branch's buoyancy and loss (Pa) at its own air and gas flows."""
    lift = loss = 0.0
    for e in els:
        _, b, x = _term(path, e, m_air, m_gas, props, [])
        lift, loss = lift + b, loss + x
    return lift, loss


def _bracket(
    f: Callable[[float], float], c: float, width: float, cap: float = math.inf
) -> tuple[float, float]:
    """An interval round ``c`` where an increasing ``f`` changes sign, f(lo) ≤ 0 ≤ f(hi), widened
    by doubling steps; its top no further than ``cap``, where f ≥ 0."""
    lo, hi = c - width, min(c + width, cap)
    step = width
    while f(lo) > 0:
        lo, hi = lo - 2 * step, lo
        step *= 2
    step = width
    while hi < cap and f(hi) < 0:
        lo, hi = hi, min(hi + 2 * step, cap)
        step *= 2
    return lo, hi


def _quadratic(m: float, lifts: Sequence[float], r: Sequence[float]) -> float:
    """Where to start a junction's draft: D with Σ √((B_i − D)/R_i) = m, each branch's loss taken
    as R_i·m_i² (exact for losses in the velocity head alone), by bisection on arithmetic."""
    r = [max(x, 1e-300) for x in r]
    hi = max(lifts)
    lo = hi - max(1.0, abs(hi))
    while sum(math.sqrt(max(b - lo, 0.0) / x) for b, x in zip(lifts, r, strict=True)) < m:
        lo = hi - 2 * (hi - lo)
    for _ in range(60):
        mid = (lo + hi) / 2
        flow = sum(math.sqrt(max(b - mid, 0.0) / x) for b, x in zip(lifts, r, strict=True))
        lo, hi = (mid, hi) if flow > m else (lo, mid)
    return (lo + hi) / 2


def _split(
    path: Path, e: Element, m_air: float, m_gas: float, props: _Props, shares: list[Any]
) -> tuple[float, float]:
    """A parallel group at its air and gas flows: the junction's draft D that every branch with
    flow has across it, buoyancy less losses, the branches' flows summing to the group's (each
    carries the group's gas per kg of air). Returned as the flow-weighted buoyancy and that less
    D, so the group adds D to the path's balance; each branch's air goes into ``shares``. A
    branch whose buoyancy is under D carries nothing (no flow backwards); a branch with no loss
    at all (an opening left out for want of its size) holds D at its buoyancy and takes what the
    others don't."""
    lifts = [_branch(path, b, 0.0, 0.0, props)[0] for b in e.parts]
    top = max(lifts)
    if m_air <= 0:
        shares.append((e.name, tuple(0.0 for _ in e.parts)))
        return top, 0.0
    ratio = m_gas / m_air
    free = [i for i, b in enumerate(e.parts) if all(x.kind == "column" for x in b)]
    lossy = [i for i in range(len(e.parts)) if i not in free]
    cur = [m_air / max(len(lossy), 1)] * len(e.parts)  # each branch's last flow, to start from

    def loss(i: int, m: float) -> float:
        return _branch(path, e.parts[i], m, m * ratio, props)[1]

    def share(i: int, d: float) -> float:
        if lifts[i] <= d:
            return 0.0
        need = math.log(lifts[i] - d)

        def gap(u: float) -> float:  # on logs: a loss runs as a power of the flow, so near linear
            return math.log(max(loss(i, math.exp(u)), 1e-300)) - need

        cur[i] = math.exp(find_root(gap, *_bracket(gap, math.log(cur[i]), 0.05), xtol=1e-12))
        return cur[i]

    def excess(d: float) -> float:
        return sum(share(i, d) for i in lossy) - m_air

    held = max((lifts[i] for i in free), default=-math.inf)
    if free and excess(held) <= 0:
        d = held
        each = [0.0 if i in free else share(i, d) for i in range(len(e.parts))]
        each[free[0]] = m_air - sum(each)
    else:  # the branches with losses carry it all (a free branch's buoyancy is under D)
        hi = max(lifts[i] for i in lossy)
        d0 = _quadratic(m_air, [lifts[i] for i in lossy], [loss(i, cur[i]) / cur[i] ** 2
                                                            for i in lossy])  # fmt: skip
        lo, up = _bracket(lambda x: -excess(x), d0, max(0.05 * (hi - d0), 1e-9), hi)
        d = find_root(excess, lo, up, xtol=1e-10)
        each = [0.0 if i in free else share(i, d) for i in range(len(e.parts))]
    shares.append((e.name, tuple(each)))
    lift = sum(s * b for s, b in zip(each, lifts, strict=True)) / max(sum(each), 1e-300)
    return lift, lift - d


def balance(
    path: Path,
    m_air: float,
    temps: Mapping[str, float],
    prod: Products,
    gas_of: Callable[[float], float],
) -> Draft:
    """Each element's buoyancy and loss at an air flow (kg/s); ``gas_of`` gives the gas flow."""
    m_gas = gas_of(m_air)
    props = _Props(path, temps, prod)
    shares: list[Any] = []
    terms = tuple(_term(path, e, m_air, m_gas, props, shares) for e in path.elements)
    return Draft(m_air, m_gas, terms, tuple(shares))


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


def _upper(path: Path) -> str:
    """What the path leaves out for want of a size, as the table's working says it."""
    if not path.left_out:
        return ""
    return f"; an upper bound, too, for want of: {'; '.join(path.left_out)}"


TABLE_TEMPS = np.array([
    300, 350, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700,
    1800, 2000, 2200,
], dtype=float)  # fmt: skip


def table(
    path: Path,
    prod: Products,
    zones: Sequence[str] | None = None,
    fuel: float | None = None,
) -> Table:
    """The draft table: the air at each gas temperature, every hot zone at it (one zone: the
    standard three and every zone the path names), at the least-air end of the band and at its
    most-air end (`Path.most`)."""
    if zones is None:
        zones = ("firebox", "chamber", "chimney", *path.zones, *path.most().zones)
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
        note=f"{ROUGH_NOTE}; {FITTINGS_NOTE}; {LEFT_OUT}" + _upper(path),
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
    branches: int = 1,
) -> Element:
    """A flue turning up into its chimney, on the flue's velocity: with the chimney's depth along
    the flue at most twice the flue's height, 6-6 × k_Re; deeper, a band from Idelchik's own stack
    example, the sudden expansion (1 − F₀/F₁)² alone (Table 1-11, 4-1), to 6-6 held at b₁/b₀ 2.
    Several flues side by side into one chimney (``branches``): each its own turn, the expansion
    on the chimney's share each flue takes (its area over the flues' together)."""
    z = elbow(b1 / b0, across / b0)
    dh = hydraulic(across, b0)
    if b1 / b0 <= TURN_B[-1]:
        note = f"6-6 at b₁/b₀ {b1 / b0:.2f}, a₀/b₀ {across / b0:.2f}: ζ₁ {z:.2f}"
        return Element(name, "fitting", zone, a_flue, branches, k=z, re_dh=dh, note=note)
    sudden = (1 - min(a_flue * branches / a_stack, 1.0)) ** 2
    note = (
        f"a chimney {b1 / b0:.1f} × the flue's height deep: 6-6 held at b₁/b₀ 2, {z:.2f} × k_Re, "
        f"to the sudden expansion {sudden:.2f} (Idelchik's stack, Table 1-11)"
    )
    return Element(name, "fitting", zone, a_flue, branches, k=z, k_lo=sudden, re_dh=dh,
                   re_lo=False, note=note)  # fmt: skip


def entrance(name: str, zone: str, area: float, branches: int = 1) -> Element:
    """Gas entering a passage flush in the wall of a larger space: 3-1's 0.50."""
    return Element(name, "fitting", zone, area, branches, k=SHARP_ENTRANCE)


def outlet(name: str, zone: str, area: float, branches: int = 1) -> Element:
    """A jet leaving a passage into a large space, its velocity head lost: 11-1's 1.0 for a
    uniform jet to 1.06 for a developed (m = 7) profile."""
    return Element(name, "fitting", zone, area, branches, k=EXIT[1], k_lo=EXIT[0])


def column(name: str, zone: str, rise: float) -> Element:
    return Element(name, "column", zone, rise=rise)


def contraction(name: str, zone: str, a0: float, a1: float, branches: int = 1) -> Element:
    """Gas passing from a passage of area ``a1`` into a narrower one of ``a0`` (each branch's),
    its inlet in the end wall with a blunt edge: Idelchik's 3-9, ζ = 0.5(1 − F₀/F₁) on the narrow
    passage's velocity (Re > 10⁴); from a large space it is 3-1's 0.50 (`entrance`)."""
    f = min(a0 / a1, 1.0) if a1 > 0 else 0.0
    k = SHARP_ENTRANCE * (1 - f)
    return Element(name, "fitting", zone, a0, branches, k=k, note=f"3-9 at F₀/F₁ {f:.2f}: {k:.2f}")


def expansion(name: str, zone: str, a0: float, a2: float, branches: int = 1) -> Element:
    """Gas leaving a passage of area ``a0`` (each branch's) into a wider one of ``a2``: Idelchik's
    4-1, the sudden expansion ζ = (1 − F₀/F₂)² on the narrow passage's velocity (Re > 3.5·10³);
    into a large space it is the free exit (`outlet`)."""
    f = min(a0 / a2, 1.0) if a2 > 0 else 0.0
    k = (1 - f) ** 2
    return Element(name, "fitting", zone, a0, branches, k=k, note=f"4-1 at F₀/F₂ {f:.2f}: {k:.2f}")


def gaps(
    name: str,
    zone: str,
    count: int,
    width: float,
    height: float,
    thickness: float,
    approach: float,
) -> tuple[Element, Element]:
    """A wall with through-gaps, ``count`` holes ``width`` × ``height`` through a wall
    ``thickness`` thick across a passage of ``approach`` area (a bag wall, the flue holes between
    two chambers): Idelchik's 8-4, ζ = [(0.5 + τ√(1 − f))(1 − f) + (1 − f)² + λl/d_h]/f² on the
    approach velocity, f the holes' share of the section, τ by l/d_h. On the holes' own velocity
    that is ζ·f²; its friction term is the holes' own (`duct`, Darcy at their Re), so the jet's
    part is returned with the friction's duct beside it. The diagram is for Re ≥ 10⁵ (its low-Re
    form not transcribed): below its Re, said (item 9)."""
    area = count * width * height
    f = min(area / approach, 1.0)
    l_dh = thickness / hydraulic(width, height)
    tau = grid_tau(l_dh)
    k = (0.5 + tau * math.sqrt(1 - f)) * (1 - f) + (1 - f) ** 2
    note = f"8-4 at f {f:.2f}, l/d_h {l_dh:.2f} (τ {tau:.2f}): ζ {k:.2f} on the holes' velocity"
    jet = Element(name, "fitting", zone, width * height, count, k=k, note=note)
    return jet, duct(f"{name}, through the wall", zone, width, height, thickness, count)


# --- a path from a design file -------------------------------------------------------------------


class NotModelledError(ValueError):
    """The design doesn't give what the path needs, or v2 doesn't build this path yet."""


def kiln_path(
    kiln: Kiln,
    *,
    grate_bar: float | None = None,
    rough: float = ROUGH,
    intake: Intakes | None = None,
    inputs: Any = None,
    segments: int = 1,
) -> Path:
    """The gas path of a design as built, from its air intakes to its chimney's top (C1:
    `paths.py`, which holds the forms). ``grate_bar``: the grate's bar thickness (m), which the
    design file doesn't carry (the fast-fire's ¾ in rod is printed, Olsen p.204); without it the
    grate's loss is left out and said so. ``intake``: the fireboxes' air intakes (ADR 0017
    decision 9; the design file holds none: the dataset's areas); without them, the design's
    openings. ``inputs``: what else the design file can't say (`paths.Inputs`), the dataset's;
    the two above fill its fields where it leaves them out. ``segments``: a single chamber cut
    into that many zones along its length, as the heat model cuts it. Refused, naming the input,
    where nothing bounds a piece of the path."""
    from kilndesigner.v2.heat import paths

    given = inputs if isinstance(inputs, paths.Inputs) else paths.Inputs()
    if given.grate_bar is None and grate_bar is not None:
        given = replace(given, grate_bar=grate_bar)
    if given.intake is None and intake is not None:
        given = replace(given, intake=intake)
    return paths.kiln_path(kiln, given, rough=rough, segments=segments)
