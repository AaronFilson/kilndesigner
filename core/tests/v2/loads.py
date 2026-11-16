"""Each reference kiln's setting as a sourced band, as the heat model takes it (ADR 0017 decision
11: no heat result without a load; `docs/research/kiln-settings.md`).

**The mass** of each chamber's setting is the dataset's ``setting`` fact (its band, kg, the method's
arithmetic in its reason): the ware at a setting density of 60–260 kg per m³ of the chamber's
fired volume (the EU BREF's periodic and tunnel kilns firing whiteware, its "setting density" the
ware's mass over the kiln's whole fired volume, furniture left out; a kiln maker's test load, 100 lb
in a 10 ft³ kiln, 160, inside), plus the shelves: one layer (the setter shelf, p.172) to one each
6¾ in of the setting's height (Skutt's furniture kit: four layers of half shelves in its 27 in
kiln), each covering the setting's plan at 8–22 lb per 12 × 24 in shelf (Olsen pp.33–35: Advancer
to silicon carbide). Where the book prints the ware or the shelves, the band takes them.

**The envelope** is the stacking space the book's clearances leave in the chamber as v2 traces it:
the combustion space all round, 4½ in for floor burners and 2½–3 in burner tips (p.171, Fig
6-63's "4½" around"; 6 in, the band's other end, for a 4 in tip), 2½ in under the setter shelf
(p.172), and up to the springline in an updraft (the arch over the stacking collects the flue
gas, p.74), or in a cross- or downdraft to the roof at the setting's edges less the same space;
each kiln's printed clearances where the book gives them (`PRINTED`). On a curved wall (a round
chamber, an arch from the floor, a dome, a crossing) the plan and top are shrunk until the box,
its corners pushed out by the clearance, lies in the chamber's own solid (`Chamber.holds`).

**The emissivity**: fired clay measured at 0.52–0.54 (1073–1273 K; Jackson, Romero and Norris
1994 via Jones et al. [R6]) to fire brick, low alumina, 0.77 at 1273 K (Osborn 1985 via [R5]):
the band; fireclay brick's 0.75 at 980 °C (Sparrow and Cess via Lienhard Table 10.1) its nominal
(`radiation-exchange.md` §5.1).

Nothing here is fitted: each number is the sources', and each gap a stated band (ADR 0017 decision
4). The fast-fire's survey load (55 kg, `heat_cases.FAST_FIRE_LOAD`) stays its tests' input.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from functools import cache
from typing import Any, Literal

import numpy as np
import reference as ref

from kilndesigner.designfile import load_design
from kilndesigner.model import Kiln
from kilndesigner.units import Q_, si
from kilndesigner.v2.heat import chamber as ch
from kilndesigner.v2.heat import kiln as hk

IN = 0.0254
type End = Literal["least", "mid", "most"]

# --- the sources (kiln-settings.md) ---------------------------------------------------------------

# Ware over the chamber's fired volume (kg/m³): EU BREF Ceramic Manufacturing Industry (2007): the
# porcelain tunnel kilns' 60–70 (Table 2.18) to the electrical insulators' 100 m³ shuttle kiln,
# 260 (§2.3.8); sanitaryware's shuttle kilns 100 (Table 2.23), a porcelain shuttle kiln 0.91 t in
# 7.0 m³, 130 (Table 2.17, Derived); Paragon's test loads, about 100 lb in about 10 ft³, 160
# (Hohenshelt 2009)
WARE_DENSITY = (60.0, 260.0)
WARE_SOURCE = (
    "kiln-settings.md §2: EU BREF Ceramic Manufacturing Industry 2007, Tables 2.17, 2.18, 2.23 and "
    "§2.3.8 (setting density, the ware without furniture over the kiln's fired volume)"
)
# A 12 × 24 in shelf: Advancer 8 lb (Olsen p.35; makers list 8–9 lb) to silicon carbide, 1 in, 22 lb
# (p.33–35); mullite 20.5 lb and cordierite up to 21 lb between: as kg per m² of shelf
SHELF_SQ_IN = 12 * 24
SHELF_LB = (8.0, 22.0)
SHELF_1IN_LB = (20.5, 22.0)  # the 1 in shelves Olsen weighs: mullite to silicon carbide
SHELF_SOURCE = "Olsen pp.33–35 (kiln-settings.md §3): a 12 × 24 in shelf, Advancer 8 to SiC 22 lb"
LAYER_PITCH = 6.75 * IN  # Skutt KM-1027 furniture kit: 4 layers in its 27 in kiln (§3)
COMBUSTION_SPACE = (4.5 * IN, 6.0 * IN)  # p.171: 4½ in for 2½–3 in tips, 6 in for a 4 in tip
UNDER_SHELF = 2.5 * IN  # p.172: at least 2½ in between the setter shelf and the floor
EMISSIVITY = (0.52, 0.77)
EMISSIVITY_NOMINAL = 0.75
EMISSIVITY_SOURCE = (
    "radiation-exchange.md §5.1: fired clay 0.52–0.54 (Jackson et al. 1994) to low-alumina fire "
    "brick 0.77 at 1273 K (Osborn 1985); fireclay brick 0.75 at 980 °C (Sparrow and Cess) nominal"
)


def kg_per_m2(lb: float) -> float:
    """A 12 × 24 in shelf's weight as kg per m² of shelf."""
    return si(Q_(lb, "lb"), "kg") / si(Q_(SHELF_SQ_IN, "in**2"), "m**2")


# --- each kiln's printed setting (kiln-settings.md §4) --------------------------------------------


@dataclass(frozen=True)
class Printed:
    """What the book prints of a kiln's setting: its plan (in, the chamber's frame, front to back
    along y from the chamber's middle), its bottom (in up), the clearance at the sides, front and
    top (in), the ware (kg), its shelves' weights (lb a 12 × 24 in shelf), and where."""

    page: str
    plan: tuple[tuple[float, float], tuple[float, float]] | None = None
    bottom: float | None = None
    side: float | None = None
    front: float | None = None
    top: float | None = None
    ware: tuple[float, float] | None = None
    shelves: tuple[float, float] | None = None
    no_shelves: bool = False
    to_springline: bool = False


PRINTED: dict[str, Printed] = {
    # 4½ in clear each side and in front, 1 in at the back, on the bag walls' two rowlock rows; its
    # 12 × 24 × 1 in shelves (p.139, p.142, Figs 5-35, 5-43)
    "fast-fire": Printed(
        "p.139, p.142", plan=((-9.0, -9.0), (9.0, 12.5)), bottom=9.0, shelves=SHELF_1IN_LB
    ),
    # 16 ft³ of stacking, 24 × 24 in between the dashed lines (3 in a side, 6 in at each end), to
    # the arch line (p.136, Figs 5-17, 5-18)
    "kahler-salt": Printed("p.136", plan=((-12.0, -12.0), (12.0, 12.0)), to_springline=True),
    # two 24 × 24 in shelves, a 9 in burner channel along each side (p.148, Fig 5-70)
    "blakebrough-tasmania": Printed("p.148", plan=((-12.0, -24.0), (12.0, 24.0))),
    # a 9 in combustion width round the floor (p.172)
    "kaneko-car": Printed("p.172", side=9.0),
    # saggars about 12 in clear round them, stacked to within 6–8 in of the dome (p.135)
    "singh-coal": Printed("p.135", side=12.0, top=7.0),
    # 1 ft from the top of the setting to the crown (p.131, Fig 5-4)
    "kato-coal": Printed("p.131", top=12.0),
    # 6 in between the top setter and the roof (pp.102–103)
    "fujiwara-bizen": Printed("pp.102–103", top=6.0),
    # at least 9 in between the setting and the front wall (p.93, p.205)
    "kyoto-climbing": Printed("p.93, p.205", front=9.0),
    # 20 short tons of bricks and tiles a cycle, 18 t printed beside (p.160): no furniture printed
    "falcone-pompeii": Printed("p.160", ware=(18_000.0, 18_144.0), no_shelves=True),
    # pots 13–24 in tall set without shelves, levelled on saggar setters (pp.85–86)
    "tamba": Printed("pp.85–86", no_shelves=True),
}
UPDRAFT = ("up",)  # an updraft's setting stops at the springline (p.74)


# --- the envelope ---------------------------------------------------------------------------------


@dataclass(frozen=True)
class Envelope:
    """A chamber zone's setting space (m), its plan's area (m²) and height (m), and how found."""

    lo: tuple[float, float, float]
    hi: tuple[float, float, float]
    how: str

    @property
    def plan(self) -> float:
        return (self.hi[0] - self.lo[0]) * (self.hi[1] - self.lo[1])

    @property
    def height(self) -> float:
        return self.hi[2] - self.lo[2]


MARGIN = 1e-3  # m: a pushed point stops this short of the wall, off the traced surface
LEVEL_TOL = 0.01  # m: a roof this little over the springline is flat there (a flat roof, a top)
SCALES = tuple(1.0 - 0.05 * k for k in range(15))  # the plan's scales tried, 1 down to 0.3
MIN_HEIGHT = 2.0 * IN  # a setting at least a 2 in pot high
CUT_GAP = 0.5 * IN  # a segment's setting stops this short of a cut between gas zones


def _roof(c: ch.Chamber) -> Any:
    """The chambers' traced faces as one mesh for vertical rays (trimesh on Embree, as rays.py)."""
    import trimesh  # pyright: ignore[reportMissingTypeStubs]

    tris = np.concatenate([z.triangles for z in c.zones])
    mesh: Any = trimesh.Trimesh(tris.reshape(-1, 3), np.arange(len(tris) * 3).reshape(-1, 3),
                                process=False)  # fmt: skip
    e1, e2 = tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]
    return mesh, np.cross(e1, e2)[:, 2]


def heights(c: ch.Chamber, xy: np.ndarray, z0: float, mesh: Any = None) -> np.ndarray:
    """The roof over each plan point (m) from ``z0`` up: the first face a vertical ray meets, if
    it faces down into the gas (the point is inside the chamber); −∞ for a point outside it."""
    mesh, nz = mesh if mesh is not None else _roof(c)
    o = np.column_stack([xy, np.full(len(xy), z0)])
    d = np.tile((0.0, 0.0, 1.0), (len(xy), 1))
    tri, ray, loc = mesh.ray.intersects_id(o, d, multiple_hits=False, return_locations=True)
    out = np.full(len(xy), -np.inf)
    for t, r, p in zip(np.asarray(tri, dtype=int), np.asarray(ray, dtype=int),
                       np.asarray(loc, dtype=float), strict=True):  # fmt: skip
        if nz[t] < 0:  # wound into the gas: a face over the point, seen from inside
            out[r] = p[2]
    return out


def _probe(mx: float, my: float, ax: float, ay: float, push: float) -> np.ndarray:
    """A plan's corners and edges' middles, each pushed out from its middle by ``push`` (less the
    margin): radially at the corners, square to the edges at their middles."""
    pts = []
    for sx in (-1.0, 0.0, 1.0):
        for sy in (-1.0, 0.0, 1.0):
            if sx == sy == 0.0:
                continue
            v = np.array([sx * ax, sy * ay])
            n = np.array([sx, sy]) / math.hypot(sx, sy)
            pts.append((mx, my) + v + max(push - MARGIN, 0.0) * n)
    return np.array(pts)


def envelopes(kid: str, kiln: Kiln, c: ch.Chamber, wide: bool = True) -> list[Envelope]:
    """Each chamber zone's setting space (front to back): the room inset by the combustion space
    (4½ in, or 6 in with ``wide`` False: p.171), from 2½ in up (p.172) to the springline in an
    updraft (p.74) or else the roof at its edges less the same space, each kiln's printed
    clearances first. On a curved wall or under a low arch the plan is narrowed, across, along or
    both, to the largest box whose edges, pushed out by the clearances, stay under the roof."""
    p = PRINTED.get(kid, Printed(""))
    space = COMBUSTION_SPACE[0 if wide else 1]
    side = p.side * IN if p.side is not None else space
    front = p.front * IN if p.front is not None else side
    top_gap = p.top * IN if p.top is not None else space
    up = kiln.draft is None or kiln.draft.type in UPDRAFT
    out: list[Envelope] = []
    rooms = c.rooms or (ch.Room((-c.width / 2, -c.depth / 2, 0.0),
                                (c.width / 2, c.depth / 2, c.height), 0.0),)  # fmt: skip
    mesh = _roof(c)
    # A tube cut into segments: its setting runs on through the cuts, each part stopping half an
    # inch short of a cut so the boxes don't touch (the end walls keep the combustion space)
    segmented = kiln.chamber.chambers == 1 and len(rooms) > 1
    for j, r in enumerate(rooms):
        z0 = r.lo[2] + (p.bottom * IN if p.bottom is not None else UNDER_SHELF)
        if p.plan is not None and len(rooms) == 1:
            (x0, y0), (x1, y1) = p.plan
            mid_y = (r.lo[1] + r.hi[1]) / 2
            lo = [x0 * IN, mid_y + y0 * IN]
            hi = [x1 * IN, mid_y + y1 * IN]
            push, scales = 0.0, ((1.0, 1.0),)
            how = f"printed ({p.page})"
        else:
            first, last = j == 0, j == len(rooms) - 1
            at_lo = front if first else (CUT_GAP if segmented else side)
            at_hi = CUT_GAP if segmented and not last else side
            lo = [r.lo[0] + side, r.lo[1] + at_lo]
            hi = [r.hi[0] - side, r.hi[1] - at_hi]
            push = side
            scales = tuple({(a, b) for s in SCALES for a, b in ((s, 1.0), (1.0, s), (s, s))})
            how = (f"the room less {side / IN:g} in a side" + (f", {front / IN:g} in at the front"
                   if first and front != side else "") + " (p.171" + (f"; {p.page}" if p.page
                   else "") + ")")  # fmt: skip
        mx, my = (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2
        ax, ay = (hi[0] - lo[0]) / 2, (hi[1] - lo[1]) / 2
        spring = r.hi[2]
        level = (p.to_springline or up) and spring > z0 + MIN_HEIGHT
        best: tuple[float, float, float, float, bool] | None = None  # (volume, sx, sy, top, flat)
        for sx, sy in sorted(scales, reverse=True):
            flat = False
            roof = heights(c, _probe(mx, my, sx * ax, sy * ay, push), z0 + MARGIN, mesh).min()
            if not math.isfinite(roof):
                continue  # a point outside the chamber's plan
            if level:  # to the springline under an arch or a dome; under a flat roof or an open
                # top at the springline, the clearance below it
                over = heights(c, _probe(mx, my, sx * ax, sy * ay, 0.0), z0 + MARGIN, mesh).min()
                flat = over <= spring + LEVEL_TOL
                top = min(roof, spring) - top_gap if flat else spring
            else:
                top = roof - top_gap
            vol = 4 * sx * ax * sy * ay * (top - z0)
            if top - z0 >= MIN_HEIGHT and (best is None or vol > best[0] * (1 + 1e-9)):
                best = (vol, sx, sy, top, flat)
        if best is None:
            raise ValueError(f"{kid}: no setting fits chamber {j + 1} with the clearances")
        _, sx, sy, z1, flat = best
        if (sx, sy) != (1.0, 1.0):
            how += f", its plan × {sx:.2f} across and × {sy:.2f} along to fit the roof"
        if level and flat:
            how += f", to {top_gap / IN:g} in under the flat roof or open top at the springline"
        elif level:
            how += ", to the springline" + (f" ({p.page})" if p.to_springline else " (p.74)")
        else:
            how += f", up to the roof less {top_gap / IN:g} in"
        out.append(Envelope((mx - sx * ax, my - sy * ay, z0), (mx + sx * ax, my + sy * ay, z1),
                            how))  # fmt: skip
    return out


# --- the mass -------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Mass:
    """A chamber zone's setting mass band (kg): the ware's and the shelves' ends, and how."""

    ware: tuple[float, float]
    shelves: tuple[float, float]
    how: str
    layers: tuple[int, int] = (1, 1)

    @property
    def low(self) -> float:
        return self.ware[0] + self.shelves[0]

    @property
    def high(self) -> float:
        return self.ware[1] + self.shelves[1]

    @property
    def mid(self) -> float:
        return (self.low + self.high) / 2


def mass(kid: str, volume: float, env: Envelope) -> Mass:
    """The setting's mass band for a chamber zone of ``volume`` (m³) and its envelope: the ware's
    setting density over the volume (or the printed ware), and one to height ÷ 6¾ in layers of
    shelves over the plan at 8–22 lb a 12 × 24 in shelf (or the printed shelves')."""
    p = PRINTED.get(kid, Printed(""))
    ware = p.ware if p.ware is not None else (WARE_DENSITY[0] * volume, WARE_DENSITY[1] * volume)
    most = max(1, math.floor(env.height / LAYER_PITCH + 1e-9))
    lb = p.shelves if p.shelves is not None else SHELF_LB
    shelves = (0.0, 0.0) if p.no_shelves else (
        env.plan * kg_per_m2(lb[0]), most * env.plan * kg_per_m2(lb[1]))  # fmt: skip
    how = (
        (f"the ware printed, {ware[0]:,.0f}–{ware[1]:,.0f} kg ({p.page})" if p.ware is not None
         else f"the ware {WARE_DENSITY[0]:g}–{WARE_DENSITY[1]:g} kg/m³ × {volume:.3f} m³")
        + ("; no shelves" + (f" ({p.page})" if p.no_shelves else "")
           if p.no_shelves else
           f"; 1–{most} layers of shelves over {env.plan:.3f} m² at {lb[0]:g}–{lb[1]:g} lb a "
           "12 × 24 in shelf")
    )  # fmt: skip
    return Mass(ware, shelves, how, (1, most))


# --- the dataset's bands and the loads ------------------------------------------------------------


@cache
def _kilns() -> dict[str, Any]:
    return ref.load()["kilns"]


def dataset_bands(kid: str) -> list[tuple[float, float]]:
    """The dataset's setting mass bands (kg), one per chamber zone, front to back."""
    facts = [f for f in ref.facts(_kilns()[kid], "heat", "setting") if ref.numeric(f)]
    return [ref.span(f, "kg") for f in facts]


@dataclass(frozen=True)
class Setting:
    """A kiln's setting: each chamber zone's envelope and mass band, and the dataset's bands."""

    kid: str
    envelopes: tuple[Envelope, ...]
    masses: tuple[Mass, ...]
    volumes: tuple[float, ...]
    dataset: tuple[tuple[float, float], ...] = field(default=())


@cache
def design(kid: str) -> Kiln:
    return load_design(ref.ROOT / str(_kilns()[kid]["design"]))


@cache
def traced(kid: str, segments: int = 1) -> ch.Chamber:
    """The kiln's chambers as v2 traces them (no openings, no path): rooms, volumes, the solid."""
    return ch.cavity(design(kid), segments)


@cache
def setting(kid: str, segments: int = 1, wide: bool = True) -> Setting:
    """A reference kiln's setting band, worked out from its chambers as v2 traces them."""
    c = traced(kid, segments)
    vols = tuple(g.volume for g in c.gas if g.kind == "chamber")
    envs = tuple(envelopes(kid, design(kid), c, wide))
    masses = tuple(mass(kid, v, e) for v, e in zip(vols, envs, strict=True))
    return Setting(kid, envs, masses, vols, tuple(dataset_bands(kid)) if segments == 1 else ())


def loads(kid: str, end: End = "mid", segments: int = 1, emissivity: float | None = None,
          wide: bool = True) -> list[hk.Load]:  # fmt: skip
    """The kiln's loads, one per chamber zone, at the mass band's ``end`` (the dataset's band; a
    tube cut into segments shares its one band by the segments' volumes)."""
    s = setting(kid, segments, wide)
    bands = list(s.dataset) or [(m.low, m.high) for m in s.masses]
    whole = dataset_bands(kid)
    if segments > 1 and len(whole) == 1:
        total = sum(s.volumes)
        bands = [(whole[0][0] * v / total, whole[0][1] * v / total) for v in s.volumes]
    eps = EMISSIVITY_NOMINAL if emissivity is None else emissivity
    out: list[hk.Load] = []
    for (low, high), env, m in zip(bands, s.envelopes, s.masses, strict=True):
        kg = {"least": low, "mid": (low + high) / 2, "most": high}[end]
        out.append(hk.Load(
            kg, env.lo, env.hi, eps,
            f"{kid}'s setting at its band's {end}, {low:,.0f}–{high:,.0f} kg (kiln-settings.md: "
            f"{m.how}); the envelope {env.how}; ε {eps:.2f} ({EMISSIVITY_SOURCE})",
        ))  # fmt: skip
    return out
