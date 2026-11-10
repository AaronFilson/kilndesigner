"""The draft: a pressure balance round the gas path, burner or ash pit to chimney top (ADR 0017
H12): the buoyancy of each hot column against friction and fittings,

    Σ (ρ_room − ρ_gas)·g·Δz  =  Σ K·ρ·v²/2,

solved for the air the path draws. fluids takes the friction (Clamond's Colebrook, 64/Re laminar)
and the fittings (Idelchik's sharp entrance, Rennels' contractions, expansions and mitred turns,
Blevins' round-bar grate); Cantera's gas tables (`gas.py`) take the gas's density and viscosity
(`tool-triples.md` §2; `thermal-software.md` §8). What v2 writes is the path and the sum.

Stated, not sourced (each said in the working):
- fluids' fittings are for round pipes; a brick flue's is taken through its area-equivalent
  diameter until Idelchik's rectangular forms are read (`thermal-software.md` §8, *pending*);
- no source gives brick's roughness: a band from a smooth wall to fluids' 'Rough concrete',
  3.05 mm; the draft is drawn at its rough end (the least air), the smooth end given beside it;
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
from fluids.filters import round_edge_grill  # pyright: ignore[reportMissingTypeStubs]
from fluids.fittings import (  # pyright: ignore[reportMissingTypeStubs]
    bend_miter,
    contraction_sharp,
    diffuser_sharp,
    entrance_sharp,
    exit_normal,
)
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
    "brick's roughness: no source (fluids' tables have none); a band from a smooth wall to "
    "fluids' 'Rough concrete', 3.05 mm, the draft taken at its rough end"
)
ROUND_FITTINGS = (
    "fluids' fittings are for round pipes: a rectangular brick passage is taken through its "
    "area-equivalent diameter until Idelchik's rectangular forms are read"
)
LEFT_OUT = (
    "the fuel bed's and the setting's resistance have no source: left out, so the air is an "
    "upper bound (problem set §2.2)"
)


def eq_diameter(area: float) -> float:
    """The diameter of the circle of the same area."""
    return math.sqrt(4 * area / math.pi)


def hydraulic(width: float, height: float) -> float:
    return 2 * width * height / (width + height)


@dataclass(frozen=True)
class Element:
    """One piece of the path. ``area`` is the flow area of one branch, the velocity's; ``zone``
    the gas filling it ("room" for the cold air). A duct's friction comes from its length and
    hydraulic diameter, a fitting's from ``k``, a column's buoyancy from ``rise`` (up +)."""

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


@dataclass(frozen=True)
class Path:
    """A gas path: its elements in order, the room's temperature and the air's pressure."""

    elements: tuple[Element, ...]
    t_room: float
    pressure: float = ATM
    rough: float = ROUGH
    steps: tuple[Step, ...] = ()

    @property
    def room_density(self) -> float:
        return self.pressure * M_AIR / (R * self.t_room)


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
        k = e.k
        if e.kind == "duct":
            re = rho * v * e.dh / mu
            k = friction_factor(max(re, 1e-3), path.rough / e.dh) * e.length / e.dh
        terms.append((e.name, 0.0, k * rho * v * v / 2))
    return Draft(m_air, m_gas, tuple(terms))


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
    rough end of the band and at a smooth wall."""
    rough, smooth = [], []
    smooth_path = Path(path.elements, path.t_room, path.pressure, 0.0, path.steps)
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
        inputs={"smooth wall at 1300 °C": f"{s[i]:.4f} kg/s", "λ": f"{prod.air_ratio:.3f}"},
        reference="fluids 1.3 (Clamond's Colebrook; Idelchik, Rennels, Blevins); Cantera's gas; "
        "tool-triples.md §2",
        note=f"{ROUGH_NOTE}; {ROUND_FITTINGS}; {LEFT_OUT}",
    )
    return Table(TABLE_TEMPS.copy(), r, s, (*path.steps, step))


# --- the parts a path is built from --------------------------------------------------------------


def _sharp() -> float:
    """A sharp-edged entrance, Idelchik's K 0.5 (fluids `entrance_sharp`)."""
    return float(entrance_sharp(method="Idelchik"))


def inlet(name: str, area: float, branches: int = 1) -> Element:
    """Room air entering through a sharp-edged opening (Idelchik's K 0.5, via fluids)."""
    return Element(name, "inlet", "room", area, branches, k=_sharp())


def grate(
    name: str, width: float, length: float, gap: float, bar: float, branches: int = 1
) -> Element:
    """A grate of round bars: Blevins' round-edged grill at the open fraction gap/(gap + bar), on
    the approach velocity over the grate's whole area (fluids `round_edge_grill`)."""
    alpha = gap / (gap + bar)
    k = float(round_edge_grill(alpha))
    return Element(name, "grate", "room", width * length, branches, k=k,
                   note=f"open fraction {alpha:.2f}, K {k:.2f}")  # fmt: skip


def duct(
    name: str,
    zone: str,
    width: float,
    height: float,
    length: float,
    branches: int = 1,
    rnd: bool = False,
) -> Element:
    """A passage's friction (Darcy f·L/D_h, fluids' Colebrook): a rectangle, or round of
    diameter ``width`` when ``rnd``."""
    if rnd:
        return Element(name, "duct", zone, math.pi * width**2 / 4, branches, length=length,
                       dh=width)  # fmt: skip
    return Element(name, "duct", zone, width * height, branches, length=length,
                   dh=hydraulic(width, height))  # fmt: skip


def contraction_turn(
    name: str, zone: str, a_from: float, a_to: float, branches: int = 1
) -> Element:
    """Into a smaller passage round a 90° corner: Rennels' sharp contraction plus a 90° mitre,
    on the smaller passage's velocity."""
    k = float(contraction_sharp(eq_diameter(a_from), eq_diameter(a_to))) + float(bend_miter(90))
    return Element(name, "fitting", zone, a_to, branches, k=k, note=f"K {k:.2f}")


def turn_expansion(name: str, zone: str, a_from: float, a_to: float) -> Element:
    """Round a 90° corner into a larger passage (a flue into its chimney): a mitre plus Rennels'
    sharp expansion, on the smaller passage's velocity."""
    k = float(bend_miter(90)) + float(diffuser_sharp(eq_diameter(a_from), eq_diameter(a_to)))
    return Element(name, "fitting", zone, a_from, k=k, note=f"K {k:.2f}")


def entrance(name: str, zone: str, area: float, branches: int = 1) -> Element:
    """Gas entering a passage from a larger space through sharp edges (Idelchik, K 0.5)."""
    return Element(name, "fitting", zone, area, branches, k=_sharp())


def outlet(name: str, zone: str, area: float, branches: int = 1) -> Element:
    """A jet leaving a passage into a large space: its velocity head lost (K 1)."""
    return Element(name, "fitting", zone, area, branches, k=float(exit_normal()))


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
            els.append(grate("grate, round bars (Blevins)", gw, gl, si(fb.grate.gap, "m"),
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
        els.append(contraction_turn("into the inlet flue", "firebox", fw * fh / fb.inlets, ia, k))
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
    els.append(turn_expansion("turn up into the chimney, and its expansion", "chimney", ea, ca))
    height = si(chim.height, "m") - z_exit
    els.append(column("chimney", "chimney", height))
    els.append(duct("chimney", "chimney", cw, cd, height, rnd=rnd))
    els.append(outlet("chimney top", "chimney", ca))
    steps = (
        Step(
            name="The gas path",
            value=" → ".join(e.name for e in els if e.kind != "column"),
            inputs={e.name: f"Δz {e.rise:.3f} m" for e in els if e.kind == "column"},
            reference="the design file; the parts' losses from fluids 1.3",
            note="; ".join([*notes, ROUND_FITTINGS]),
        ),
    )
    return Path(tuple(els), t_room, pressure, rough, steps)
