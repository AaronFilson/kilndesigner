"""A sprung arch's steel frame in PyNite, coupled to the arch's limit analysis: the hot thrust
along the bay and the steel's stress at its temperature.

**The frame** (the engine's arch frame; `scratch/statics-combos/arch-frame/frameflex.py`): a
buttress angle along the top of each side wall behind the skewbacks, bolted to posts of the same
angle fixed at their feet; a tie rod across between each pair of posts at the buttress's level,
axial only. The angle bends about its geometric axis (the leg held by the wall it sits on). E at
the steel's temperature by AISC 360-16 Appendix 4 Table A-4.2.1 (kE; the table ends at 1,400 °F,
past which no stiffness is sourced and the coupling refuses).

**The coupling** (`compat.py` of the same probe; `statics-combinations.md` §2): the arch is cut
along the kiln into slices, each a rigid no-tension ring whose push on the frame lies between the
section's least (cold: the frame snug, the arch settled to its least thrust) and most (hot: the
cap from the hot friction and the crushing stand-in). Heating grows each slice's span by ε, so with
the frame where it was each side wants g = C·P_min + ε·S/2 − (the rods' own growth)/2 further out.
The frame moves u = C·P (C its flexibility at the slices, by unit loads in PyNite):

    minimise ½·PᵀCP − gᵀP  over  b·H_min ≤ P ≤ b·H_max,

a bounded convex program solved exactly as bounded least squares on C's Cholesky factor
(SciPy's ``lsq_linear``). Its optimality conditions say which slices the frame holds (between the
bounds: the frame takes the whole growth), which hinge or crush (at H_max: the crown rises and
takes the rest), and which spread (at H_min). The thrust is then known along the bay, and PyNite
gives the angle's moment and the rods' pull under it.

Rigid brick absorbs nothing: every inch of growth the frame doesn't take goes into a mechanism.
Elastic shortening, creep and joint closure of the brick would lower the thrust; their data are
not found (`arch-thrust-theory.md` §6). The crushing stand-in caps a slice, so the answer
converges as the slices are refined (`converge`).
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from functools import cache
from importlib import resources
from typing import Any

import numpy as np
import numpy.typing as npt
import yaml
from scipy.optimize import lsq_linear

from kilndesigner.model import Kiln
from kilndesigner.units import Q_, si
from kilndesigner.v2.statics import sources
from kilndesigner.v2.statics.section import CrossSection, SectionResult
from kilndesigner.working import Step, show

type FloatArray = npt.NDArray[np.float64]

ALPHA_STEEL = 11.7e-6
"""A36 and low-carbon steel, 1/K at room temperature (thermal-properties.md §2.2: 3 sources)."""
NU = 0.3
"""Steel's Poisson's ratio, from memory: it only sets G, which the symmetric push doesn't load."""
GRID = si(Q_(0.5, "inch"), "m")  # the buttress's nodes along the bay


@cache
def _steel() -> dict[str, Any]:
    text = resources.files("kilndesigner.data").joinpath("steel.yaml").read_text(encoding="utf-8")
    data: dict[str, Any] = yaml.safe_load(text)
    return data


@dataclass(frozen=True)
class AngleSection:
    """An equal-leg angle, SI (m, m², m³, m⁴): AISC Shapes Database v16.0 via steel.yaml. Its
    area and torsion constant are the thin-walled sums t(2b − t) and (2b − t)t³/3 (Derived; the
    symmetric push loads neither)."""

    name: str
    leg: float
    t: float
    sx: float
    sz: float
    ix: float

    @property
    def area(self) -> float:
        return self.t * (2 * self.leg - self.t)

    @property
    def j(self) -> float:
        return (2 * self.leg - self.t) * self.t**3 / 3


@dataclass(frozen=True)
class RodSize:
    """A threaded rod: its diameter and tensile stress area (m, m²), steel.yaml (Fastenal)."""

    name: str
    d: float
    stress_area: float


def angle(name: str) -> AngleSection:
    inch = si(Q_(1, "inch"), "m")
    for s in _steel()["angles"]["shapes"]:
        if s["name"] == name:
            return AngleSection(
                name, s["leg"] * inch, s["t"] * inch, s["sx"] * inch**3, s["sz"] * inch**3,
                s["ix"] * inch**4,
            )  # fmt: skip
    raise KeyError(f"no angle {name!r} in steel.yaml")


def rod(name: str) -> RodSize:
    inch = si(Q_(1, "inch"), "m")
    for s in _steel()["rods"]["sizes"]:
        if s["name"] == name:
            return RodSize(name, s["d"] * inch, s["stress_area"] * inch**2)
    raise KeyError(f"no rod {name!r} in steel.yaml")


@dataclass(frozen=True)
class HotSteel:
    """A36 at a temperature: AISC 360-16 Table A-4.2.1's ky = Fy(T)/Fy and kE = E(T)/E, linear
    between rows (steel-design.md §S3), and E, Fy themselves (Pa)."""

    temperature_f: float
    ky: float
    ke: float
    e: float
    fy: float


class TooHotError(ValueError):
    """Past 1,400 °F Table A-4.2.1's kE column ends: no sourced stiffness."""


def hot_steel(temperature_f: float) -> HotSteel:
    hs = _steel()["hot_steel"]
    if temperature_f > hs["ke_deg_f"][-1]:
        raise TooHotError(
            f"{temperature_f:.0f} °F: AISC Table A-4.2.1's E(T) ends at {hs['ke_deg_f'][-1]} °F"
        )
    ky = float(np.interp(temperature_f, hs["ky_deg_f"], hs["ky"]))
    ke = float(np.interp(temperature_f, hs["ke_deg_f"], hs["ke"]))
    psi = si(Q_(1, "psi"), "Pa")
    return HotSteel(temperature_f, ky, ke, hs["e_psi"] * psi * ke, hs["fy_psi"] * psi * ky)


@dataclass(frozen=True)
class Frame:
    """The arch's frame: the buttress angle along each side (the posts of the same angle), the
    rods, the bay between end posts along a side, the rods' stretched length between nuts, the
    posts' height from their feet to the buttress (m), and how many posts a side (the corners
    included, evenly spaced, each pair tied by a rod)."""

    angle: AngleSection
    rod: RodSize
    bay: float
    rod_length: float
    post_height: float
    posts: int = 2
    source: str = ""

    def __post_init__(self) -> None:
        if self.posts < 2:
            raise ValueError("a frame has a post at each end of each side")

    @property
    def stations(self) -> FloatArray:
        return np.linspace(0.0, self.bay, self.posts)


def _grid(frame: Frame, edges: FloatArray) -> FloatArray:
    """The buttress's nodes: the slices' edges and the posts (a post within a quarter grid step
    of an edge snapped onto it), each interval between them split evenly about every half inch.
    No member much shorter than its neighbours: PyNite's stability check calls that singular."""
    marks = [float(e) for e in edges]
    for s in frame.stations:
        if min(abs(s - m) for m in marks) > GRID / 4:
            marks.append(float(s))
    marks.sort()
    out: list[float] = [marks[0]]
    for a, b in itertools.pairwise(marks):
        k = max(1, round((b - a) / GRID))
        out += [a + (b - a) * i / k for i in range(1, k + 1)]
    return np.array(out)


def build(frame: Frame, edges: FloatArray, steel: HotSteel) -> tuple[Any, FloatArray]:
    """The frame in PyNite: x across (the left buttress at 0, the right at the rods' length),
    y up, z along the bay."""
    from Pynite import FEModel3D

    m: Any = FEModel3D()
    m.add_material("A36", steel.e, steel.e / (2 * (1 + NU)), NU, 0.0)
    a = frame.angle
    m.add_section("angle", a.area, a.ix, a.ix, a.j)
    r = frame.rod
    m.add_section("rod", r.stress_area, math.pi * r.d**4 / 64, math.pi * r.d**4 / 64,
                  math.pi * r.d**4 / 32)  # fmt: skip
    z = _grid(frame, edges)
    posts = {int(np.argmin(np.abs(z - s))) for s in frame.stations}
    y = frame.post_height
    for side, x in (("L", 0.0), ("R", frame.rod_length)):
        for i, zi in enumerate(z):
            m.add_node(f"{side}{i}", x, y, float(zi))
        for i in range(len(z) - 1):
            m.add_member(f"B{side}{i}", f"{side}{i}", f"{side}{i + 1}", "A36", "angle")
        m.def_releases(f"B{side}0", Ryi=True, Rzi=True)  # bolted to the end posts: pinned
        m.def_releases(f"B{side}{len(z) - 2}", Ryj=True, Rzj=True)
        for k in sorted(posts):
            base = f"{side}base{k}"
            m.add_node(base, x, 0.0, float(z[k]))
            m.add_member(f"P{side}{k}", base, f"{side}{k}", "A36", "angle")
            m.def_support(base, True, True, True, True, True, True)
    for k in sorted(posts):
        m.add_member(f"rod{k}", f"L{k}", f"R{k}", "A36", "rod")
        m.def_releases(f"rod{k}", Rxi=True, Ryi=True, Rzi=True, Ryj=True, Rzj=True)
    return m, z


def _outward(m: Any, z: FloatArray, combo: str) -> FloatArray:
    left = np.array([-m.nodes[f"L{i}"].DX[combo] for i in range(len(z))])
    right = np.array([m.nodes[f"R{i}"].DX[combo] for i in range(len(z))])
    return 0.5 * (left + right)


def _mean(z: FloatArray, u: FloatArray, a: float, b: float) -> float:
    k = (z >= a - 1e-9) & (z <= b + 1e-9)
    return float(np.trapezoid(u[k], z[k]) / (b - a))


def _load(m: Any, z: FloatArray, a: float, b: float, w: float, case: str) -> None:
    """``w`` N/m outward on both buttresses over [a, b]."""
    for i in range(len(z) - 1):
        if z[i] >= a - 1e-9 and z[i + 1] <= b + 1e-9:
            m.add_member_dist_load(f"BL{i}", "FX", -w, -w, case=case)
            m.add_member_dist_load(f"BR{i}", "FX", w, w, case=case)


def flexibility(frame: Frame, edges: FloatArray, steel: HotSteel) -> FloatArray:
    """C (m/N): the outward move of the buttresses averaged over slice i when slice j pushes with
    1 N in all, spread evenly over it, on both sides at once (work-conjugate to P_j = H_j b_j)."""
    m, z = build(frame, edges, steel)
    n = len(edges) - 1
    for j in range(n):
        _load(m, z, float(edges[j]), float(edges[j + 1]), 1.0 / (edges[j + 1] - edges[j]), f"S{j}")
        m.add_load_combo(f"C{j}", {f"S{j}": 1.0})
    m.analyze_linear(check_statics=False)
    c = np.zeros((n, n))
    for j in range(n):
        u = _outward(m, z, f"C{j}")
        for i in range(n):
            c[i, j] = _mean(z, u, float(edges[i]), float(edges[i + 1]))
    return 0.5 * (c + c.T)


@dataclass(frozen=True)
class Coupled:
    """The arch and the frame together at one slicing: each slice's push (N/m), what it does,
    the frame's response, and the steel's stress (Pa) at its temperature."""

    edges: FloatArray
    h: FloatArray  # N/m, each slice
    states: tuple[str, ...]
    kkt: float  # the largest violation of the optimality conditions, a share of the growth
    moment: float  # N·m, the buttress angle's largest
    angle_stress: float  # Pa, moment / Sx
    rod_force: float  # N, the busiest rod
    rod_stress: float  # Pa, on its tensile stress area
    steel: HotSteel
    growth: float  # m a side, the arch's less the rods' own


def couple(
    frame: Frame,
    h_min: float,
    h_max: float,
    span: float,
    strain: float,
    steel_temperature_f: float = 70.0,
    slices: int = 4,
    start: float | None = None,
) -> Coupled:
    """The hot thrust along the bay: each of ``slices`` slices between ``h_min`` and ``h_max``
    (N/m a side; h_max may be math.inf), the arch's span ``span`` (m) grown by ``strain``, the
    steel at ``steel_temperature_f`` (its rods' own growth given back). ``start``: the cold push
    the frame was snugged at (N/m; default h_min)."""
    steel = hot_steel(steel_temperature_f)
    edges = np.linspace(0.0, frame.bay, slices + 1)
    b = np.diff(edges)
    c = flexibility(frame, edges, steel)
    lo = b * h_min
    hi = b * h_max if math.isfinite(h_max) else np.full(slices, np.inf)
    relief = ALPHA_STEEL * si(Q_(steel_temperature_f - 70.0, "delta_degF"), "K")
    relief *= frame.rod_length / 2
    growth = strain * span / 2 - relief
    g = c @ (b * (h_min if start is None else start)) + growth
    lc = np.linalg.cholesky(c)
    res: Any = lsq_linear(lc.T, np.linalg.solve(lc, g), bounds=(lo, hi), method="bvls",
                          tol=1e-15, max_iter=100_000)  # fmt: skip
    p = np.asarray(res.x, dtype=np.float64)
    r = c @ p - g
    tol = 1e-8 * max(float(np.max(np.abs(p))), 1.0)
    at_lo = np.abs(p - lo) <= tol
    at_hi = np.isfinite(hi) & (np.abs(p - np.where(np.isfinite(hi), hi, 0.0)) <= tol)
    free = ~at_lo & ~at_hi
    worst = max(
        float(np.max(np.maximum(-r[at_lo], 0.0), initial=0.0)),
        float(np.max(np.maximum(r[at_hi], 0.0), initial=0.0)),
        float(np.max(np.abs(r[free]), initial=0.0)),
    )
    states = tuple(
        "least: spreads" if a else "most: hinges or crushes" if h else "between: the frame takes it"
        for a, h in zip(at_lo, at_hi, strict=True)
    )
    moment, rod_force = _steel_response(frame, edges, p, steel)
    scale = max(abs(growth), 1e-12)
    return Coupled(
        edges, p / b, states, worst / scale, moment, moment / frame.angle.sx, rod_force,
        rod_force / frame.rod.stress_area, steel, growth,
    )  # fmt: skip


def _steel_response(
    frame: Frame, edges: FloatArray, p: FloatArray, steel: HotSteel
) -> tuple[float, float]:
    """PyNite under the solved pushes: the buttress angle's largest moment and the busiest rod."""
    m, z = build(frame, edges, steel)
    for j in range(len(p)):
        a, b = float(edges[j]), float(edges[j + 1])
        _load(m, z, a, b, float(p[j]) / (b - a), "H")
    m.add_load_combo("H", {"H": 1.0})
    m.analyze_linear(check_statics=False)
    moment = 0.0
    for name, member in m.members.items():
        if str(name).startswith("B"):
            for axis in ("My", "Mz"):
                moment = max(moment, abs(member.max_moment(axis, "H")),
                             abs(member.min_moment(axis, "H")))  # fmt: skip
    pull = max(abs(mm.max_axial("H")) for n, mm in m.members.items() if str(n).startswith("rod"))
    return float(moment), float(pull)


@dataclass(frozen=True)
class Converged:
    """The coupling refined until the busiest slice's push and the angle's stress move less than
    ``tol`` from one slicing to the next."""

    result: Coupled
    history: tuple[tuple[int, float, float], ...]  # (slices, the largest push N/m, stress Pa)
    converged: bool
    steps: tuple[Step, ...]


def converge(
    frame: Frame,
    h_min: float,
    h_max: float,
    span: float,
    strain: float,
    steel_temperature_f: float = 70.0,
    slicings: tuple[int, ...] = (4, 8, 16, 32),
    tol: float = 0.01,
    start: float | None = None,
) -> Converged:
    history: list[tuple[int, float, float]] = []
    result: Coupled | None = None
    done = False
    for n in slicings:
        result = couple(frame, h_min, h_max, span, strain, steel_temperature_f, n, start)
        history.append((n, float(np.max(result.h)), result.angle_stress))
        if len(history) > 1:
            (_, h0, s0), (_, h1, s1) = history[-2], history[-1]
            if abs(h1 - h0) <= tol * max(abs(h1), 1e-9) and abs(s1 - s0) <= tol * max(s1, 1e-9):
                done = True
                break
    assert result is not None
    return Converged(result, tuple(history), done, _steps(frame, result, history, done, strain))


def for_kiln(
    kiln: Kiln, xs: CrossSection, angle_name: str, rod_name: str, posts: int = 2, source: str = ""
) -> Frame:
    """The frame round a kiln's lining: the bay its outside depth (posts at the corners), the
    rods across its outside width and both angles' legs, the posts from under the floor to the
    skewback's top (the engine's arch frame, `frame.py` of v1, kiln-hardware.md §4)."""
    lining = kiln.lining

    def thick(face: str) -> float:
        layers = lining.for_face(face, door_face=kiln.door_face)  # type: ignore[arg-type]
        return sum(si(x.thickness, "m") for x in layers)

    a = angle(angle_name)
    width = si(kiln.chamber.width, "m") + thick("left") + thick("right")
    depth = si(kiln.chamber.length, "m") + thick("front") + thick("back")
    return Frame(a, rod(rod_name), depth, width + 2 * a.leg, thick("floor") + xs.skewback_top,
                 posts, source)  # fmt: skip


def kiln_coupling(
    kiln: Kiln,
    xs: CrossSection,
    cold: SectionResult,
    hot: SectionResult,
    frame: Frame,
    steel_temperature_f: float = 70.0,
    cautious: bool = True,
) -> Converged:
    """The hot thrust along a framed kiln's bay: between the cold section's least push on the
    frame (the arch settled) and the hot section's most (the cap), the ring's growth the high end
    of its material's band (``cautious``) or the low."""
    band = sources.growth(xs.ring_material)
    if band is None:
        raise ValueError(f"no sourced expansion for {xs.ring_material}: the growth isn't known")
    low, high, _ = band
    span = si(kiln.chamber.width, "m")
    return converge(frame, max(cold.least, hot.least), hot.most, span,
                    high if cautious else low, steel_temperature_f, start=cold.least)  # fmt: skip


def _steps(
    frame: Frame,
    r: Coupled,
    history: list[tuple[int, float, float]],
    done: bool,
    strain: float,
) -> tuple[Step, ...]:
    hs = _steel()["hot_steel"]
    binding = si(Q_(_steel()["binding_stress_psi"], "psi"), "Pa")
    held = sum(s.startswith("between") for s in r.states)
    capped = sum(s.startswith("most") for s in r.states)
    return (
        Step(
            name="The frame",
            value=f"{frame.angle.name} buttresses and {frame.posts} posts a side, "
            f"{frame.rod.name} rods; bay {show(Q_(frame.bay, 'm'), 'inch')}",
            inputs={
                "rods' length": show(Q_(frame.rod_length, "m"), "inch"),
                "posts' height": show(Q_(frame.post_height, "m"), "inch"),
            },
            reference="AISC Shapes Database v16.0 and Fastenal's thread table (steel.yaml); "
            "PyNite 3.2.1",
            note=frame.source or None,
        ),
        Step(
            name="Steel at its temperature",
            value=f"{r.steel.temperature_f:.0f} °F: E × {r.steel.ke:.2f}, Fy × {r.steel.ky:.2f}",
            reference=hs["source"],
        ),
        Step(
            name="The arch's growth a side, less the rods' own",
            value=show(Q_(r.growth, "m"), "inch"),
            formula="ε·S/2 − α_steel·ΔT·L_rod/2",
            inputs={"ε": f"{strain:.4f}", "α_steel": f"{ALPHA_STEEL:.3g} /K"},
            reference="thermal-properties.md §2.1–2.2; refractory-movement-and-mortar.md §1.1",
        ),
        Step(
            name="The hot push along the bay",
            value=f"{min(r.h):.4g} to {max(r.h):.4g} N/m ("
            f"{si(Q_(min(r.h), 'N/m'), 'lbf/ft'):.4g} to "
            f"{si(Q_(max(r.h), 'N/m'), 'lbf/ft'):.4g} lbf/ft); {held} of {len(r.h)} slices held by "
            f"the frame, {capped} at the cap",
            formula="minimise ½PᵀCP − gᵀP over b·H_min ≤ P ≤ b·H_max (bounded least squares)",
            inputs={
                "slicings": ", ".join(f"{n}: {h:.4g} N/m" for n, h, _ in history),
                "optimality": f"{r.kkt:.1e} of the growth",
            },
            reference="statics-combinations.md §2 (the arch–frame pair)",
            note=None if done else "not converged in the slicings tried",
        ),
        Step(
            name="The buttress angle",
            value=f"M {r.moment:.4g} N·m; {show(Q_(r.angle_stress, 'Pa'), 'psi')} on Sx, against "
            f"Fy(T) {show(Q_(r.steel.fy, 'Pa'), 'psi')} and the binding limit "
            f"{show(Q_(binding, 'Pa'), 'psi')}",
            reference=f"{hs['source']}; {_steel()['binding_stress_source']}",
        ),
        Step(
            name="The busiest rod",
            value=f"{r.rod_force:.4g} N ({si(Q_(r.rod_force, 'N'), 'lbf'):.4g} lbf); "
            f"{show(Q_(r.rod_stress, 'Pa'), 'psi')} on its stress area",
            reference=_steel()["binding_stress_source"],
        ),
    )
