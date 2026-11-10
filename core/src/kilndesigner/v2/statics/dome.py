"""A dome of revolution as rigid ring blocks, per radian of azimuth, with hoop compression: least
thickness, the thrust at the springing, and a round kiln's dome on its wall.

**The model** (Derived here; the same LP as `rigid.py`). A spherical shell between the inner
radius R and R + T, from its crown to the springing colatitude ψ_s, is cut by conical joints
through the sphere's centre into rings. Per radian of azimuth each ring is a wedge whose weight is
ρg·(r_o³ − r_i³)/3·(cos ψ₀ − cos ψ₁), at the wedge's centroid (exact integrals over the annular
sector, weighted by the distance from the axis). Its forces lie in the meridian plane:

- **the conical joints** above and below, N ≥ 0 and |T| ≤ μN at the joint's two ends, so the
  resultant may sit anywhere across the joint, and the springing's too (a springing that moves);
- **hoop compression**: the wedge's two meridian faces, pushed by the neighbouring wedges, give
  a net push away from the axis, F ≥ 0 per radian, acting anywhere between the ring's lowest and
  highest point (a horizontal force's moment depends only on its height). Hoop tension, the
  push toward the axis, is not allowed: no tension (Heyman's assumption). As a joint: a fixed
  body, the normal +x, no friction.
- **lunes** (no hoop force at all, the dome cracked along its meridians): no hoop joints, and the
  opposite lune's push at the crown, across the axis, between the crown's intrados and extrados.

Checked: a hemisphere with hoop forces needs t/R 0.0428 of its mid-surface radius (Heyman 0.042;
Nodargi and Bisegna's refined 0.04284; domes-over-doors.md §D1). The lunes give the same: hoop
compression is never active at the limit, the binding zone being low, where hoops would be in
tension (the thrust-network probe found the same, `tool-triples.md` §4). Lau's 0.069 for lunes
(Lau 2006 p.54) is not reproduced: an open question (`engine-v2-negative-cases.md` §7).

A round kiln's dome bears on its round wall: wall courses per radian (their weight ρg times the
annulus's area moment), a skewback ring cut on the dome's springing cone, hoops in the wall too,
and optionally a steel band: a push toward the axis at its height (the band's tension per radian).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from kilndesigner.model import Dome as DomeRoof
from kilndesigner.model import Kiln
from kilndesigner.units import Q_, si
from kilndesigner.v2.statics import sources
from kilndesigner.v2.statics.blocks import G
from kilndesigner.v2.statics.rigid import (
    Body,
    Joint,
    Problem,
    Section,
    Status,
    assemble,
    force_on,
    solve,
)
from kilndesigner.v2.statics.section import NotModelledError
from kilndesigner.working import Step, show

RING, HOOP, GROUND, BAND, WALL = "ring", "hoop", "ground", "band", "wall"


@dataclass(frozen=True)
class DomeShell:
    """A spherical shell of revolution: inner radius, thickness (m), springing colatitude ψ_s
    (radians from the crown), density (kg/m³), and how many rings it is cut into."""

    radius: float
    thickness: float
    springing: float
    density: float
    rings: int = 60

    def __post_init__(self) -> None:
        if not (self.radius > 0 and self.thickness > 0 and self.density >= 0):
            raise ValueError("a dome needs a positive radius and thickness")
        if not 0 < self.springing <= math.pi / 2:
            raise ValueError("a dome's springing is between its crown and its equator")
        if self.rings < 2:
            raise ValueError("a dome is cut into at least two rings")

    @classmethod
    def from_span_rise(
        cls, span: float, rise: float, thickness: float, density: float, rings: int = 60
    ) -> DomeShell:
        """A spherical cap by its inside diameter and rise (m): R = (D²/4 + h²)/(2h)."""
        if not 0 < rise <= span / 2:
            raise ValueError("a spherical dome's rise is above 0 and at most its radius")
        radius = (span**2 / 4 + rise**2) / (2 * rise)
        return cls(radius, thickness, math.asin(span / 2 / radius), density, rings)

    @classmethod
    def hemisphere(
        cls, mid_radius: float, thickness: float, density: float, rings: int = 60
    ) -> DomeShell:
        return cls(mid_radius - thickness / 2, thickness, math.pi / 2, density, rings)

    @property
    def weight(self) -> float:
        """N per radian of azimuth."""
        r, t = self.radius, self.thickness
        return self.density * G * ((r + t) ** 3 - r**3) / 3 * (1 - math.cos(self.springing))


def _shell_wedge(
    r0: float, r1: float, p0: float, p1: float, unit: float
) -> tuple[float, float, float]:
    """A spherical shell's band between radii r0, r1 and colatitudes p0, p1, turned one radian:
    its weight and centroid (x from the axis, z from the sphere's centre)."""
    w = unit * (r1**3 - r0**3) / 3 * (math.cos(p0) - math.cos(p1))
    mx = unit * (r1**4 - r0**4) / 4 * ((p1 - p0) / 2 - (math.sin(2 * p1) - math.sin(2 * p0)) / 4)
    mz = unit * (r1**4 - r0**4) / 4 * (math.sin(p1) ** 2 - math.sin(p0) ** 2) / 2
    return w, mx / w, mz / w


def _rings(shell: DomeShell, zc: float, overburden: list[tuple[float, float]]) -> list[Body]:
    ri, ro = shell.radius, shell.radius + shell.thickness
    n = shell.rings
    out: list[Body] = []
    for k in range(n):
        p0, p1 = shell.springing * k / n, shell.springing * (k + 1) / n
        w, x, z = _shell_wedge(ri, ro, p0, p1, shell.density * G)
        loads: list[tuple[float, float, float, float]] = []
        inner = ro
        for thick, rho in overburden:  # layers laid over the shell: its load
            wl, xl, zl = _shell_wedge(inner, inner + thick, p0, p1, rho * G)
            loads.append((xl, zc + zl, 0.0, -wl))
            inner += thick
        out.append(Body(f"ring {k + 1}", w, (x, zc + z), False, RING, None, tuple(loads)))
    return out


def _wedge(poly: list[tuple[float, float]], unit: float) -> tuple[float, float, float]:
    """A polygon in the meridian plane turned through one radian: its weight (unit × ∫x dA) and
    centroid (∫x² dA, ∫xz dA over ∫x dA), by Green's theorem (Derived)."""
    a1 = a2 = a3 = 0.0
    for (x0, z0), (x1, z1) in zip(poly, poly[1:] + poly[:1], strict=True):
        c = x0 * z1 - x1 * z0
        a1 += (x0 + x1) * c
        a2 += (x0 * x0 + x0 * x1 + x1 * x1) * c
        a3 += (x0 * z1 + 2 * x0 * z0 + 2 * x1 * z1 + x1 * z0) * c
    first, second, cross = a1 / 6, a2 / 12, a3 / 24
    if first < 0:
        first, second, cross = -first, -second, -cross
    return unit * first, second / first, cross / first


def section(
    shell: DomeShell,
    hoops: bool = True,
    wall: tuple[float, float, float, int] | None = None,
    band: float | None = None,
    overburden: list[tuple[float, float]] | None = None,
) -> Section:
    """The dome per radian of azimuth, its springing on fixed ground, or with ``wall`` (its
    thickness m, height m, density kg/m³, courses) on a round wall standing on the ground: a
    skewback ring on the wall's top cut on the springing cone. ``band``: a steel band's height
    (m) on the wall or skewback, pushing toward the axis. Rings first (crown down), then the
    skewback and courses, then the fixed bodies."""
    ri, ro, ps = shell.radius, shell.radius + shell.thickness, shell.springing
    height = 0.0 if wall is None else wall[1]
    zc = height - ri * math.cos(ps)  # the springing's intrados on the wall's inner top edge
    bodies = _rings(shell, zc, overburden or [])
    n = shell.rings
    joints: list[Joint] = []
    for k in range(1, n):
        p = ps * k / n
        c, s = math.cos(p), math.sin(p)
        pts = ((ri * s, zc + ri * c), (ro * s, zc + ro * c))
        joints.append(Joint(k - 1, k, pts, ((c, -s), (c, -s)), 1.0))
    c, s = math.cos(ps), math.sin(ps)
    springing_pts = ((ri * s, zc + ri * c), (ro * s, zc + ro * c))
    springing_n = ((c, -s), (c, -s))  # from the lowest ring down into what it springs from
    hoop_bodies: list[tuple[int, float, float]] = []  # (body, z low, z high) for hoop joints
    for k in range(n):
        p0, p1 = ps * k / n, ps * (k + 1) / n
        hoop_bodies.append((k, zc + ri * math.cos(p1), zc + ro * math.cos(p0)))
    if wall is None:
        holder = len(bodies)
        bodies.append(Body("ground", 0.0, (ri * s, zc + ri * c - 0.1), True, GROUND))
        joints.append(Joint(n - 1, holder, springing_pts, springing_n, 1.0))
    else:
        thick, h, rho, courses = wall
        unit = rho * G
        x_in, x_out = ri * s, ri * s + thick
        x_e, z_e = ro * s, zc + ro * c
        skewed = ps < math.pi / 2 - 1e-9 and z_e > h + 1e-9
        first = len(bodies)
        top = h
        if skewed:
            poly = [(x_in, h), (x_e, z_e), (x_out, z_e), (x_out, h)]
            w, cx, cz = _wedge(poly, unit)
            bodies.append(Body("skewback", w, (cx, cz), False, "skewback"))
            hoop_bodies.append((first, h, z_e))
            top = z_e
        dz = h / courses
        course0 = len(bodies)
        for k in range(courses):
            w, cx, cz = _wedge([(x_in, k * dz), (x_out, k * dz), (x_out, (k + 1) * dz),
                                (x_in, (k + 1) * dz)], unit)  # fmt: skip
            bodies.append(Body(f"wall, course {k + 1}", w, (cx, cz), False, WALL))
            hoop_bodies.append((course0 + k, k * dz, (k + 1) * dz))
        holder = first if skewed else course0 + courses - 1
        joints.append(Joint(n - 1, holder, springing_pts, springing_n, 1.0))
        ground = len(bodies)
        bodies.append(Body("ground", 0.0, (x_in, -0.1), True, GROUND))
        joints.append(Joint(ground, course0, ((x_in, 0.0), (x_out, 0.0)), ((0.0, 1.0),) * 2, 1.0))
        for k in range(1, courses + (1 if skewed else 0)):
            above = course0 + k if k < courses else first
            z = k * dz
            joints.append(Joint(course0 + k - 1, above, ((x_in, z), (x_out, z)),
                                ((0.0, 1.0),) * 2, 1.0))  # fmt: skip
        if band is not None:
            banded = first if skewed and band >= h else course0 + min(int(band / dz), courses - 1)
            bodies.append(Body("band", 0.0, (x_out + 0.1, band), True, BAND))
            joints.append(Joint(len(bodies) - 1, banded, ((x_out, min(band, top)),),
                                ((-1.0, 0.0),), 1.0, planar=False))  # fmt: skip
    axis = len(bodies)
    bodies.append(Body("axis", 0.0, (-0.1, zc), True, HOOP))
    if hoops:  # compression in the hoops pushes each wedge away from the axis
        for body, z_lo, z_hi in hoop_bodies:  # not planar: no crushing rows, never shrunk
            x = bodies[body].centroid[0]
            joints.append(Joint(axis, body, ((x, z_lo), (x, z_hi)), ((1.0, 0.0),) * 2, 1.0,
                                planar=False))  # fmt: skip
    else:  # lunes: the opposite lune pushes at the crown, across the axis
        joints.append(Joint(axis, 0, ((0.0, zc + ri), (0.0, zc + ro)), ((1.0, 0.0),) * 2, 1.0))
    return Section(tuple(bodies), tuple(joints), 1.0)


def problem(sec: Section, mu: float) -> Problem:
    """μ at the masonry's joints; none at the hoops' and the band's (they push square)."""
    mus = tuple(
        0.0 if {sec.bodies[j.a].tag, sec.bodies[j.b].tag} & {HOOP, BAND} else mu for j in sec.joints
    )
    return Problem(sec, mus)


def stands(shell: DomeShell, mu: float, hoops: bool = True) -> bool:
    return solve(problem(section(shell, hoops), mu)).status is Status.OPTIMAL


def least_thickness(
    mid_radius: float, springing: float, density: float, mu: float, hoops: bool = True,
    rings: int = 60, tol: float = 1e-5,
) -> float:  # fmt: skip
    """The least thickness (m) of a spherical dome of this mid-surface and springing under its
    own weight, its thickness scaled about the mid-surface; math.nan if none up to 0.4 R stands."""

    def ok(t: float) -> bool:
        return stands(DomeShell(mid_radius - t / 2, t, springing, density, rings), mu, hoops)

    lo, hi = 1e-4 * mid_radius, 0.4 * mid_radius
    if not ok(hi):
        return math.nan
    while hi - lo > tol * mid_radius:
        mid = (lo + hi) / 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi


def springing_thrust(shell: DomeShell, mu: float, sense: int = 1, hoops: bool = True) -> float:
    """The horizontal push at the springing per radian of azimuth (N): the least (``sense`` 1,
    supports that give) or the most (−1); math.nan if the dome can't stand. Per metre of the
    springing's circumference, divide by its radius (Lau 2006 Eq. 3.1)."""
    sec = section(shell, hoops)
    p = problem(sec, mu)
    sol = solve(p, force_on(assemble(p), sec, GROUND, 0), sense)
    return sol.value if sol.status is Status.OPTIMAL else math.nan


# --------------------------------------------------------------------------------- a round kiln


def kiln_not_modelled(kiln: Kiln) -> str | None:
    """Why a kiln's dome isn't built as a dome of revolution, or None."""
    roof = kiln.roof
    if not isinstance(roof, DomeRoof):
        return f"not a dome: {roof.type}"
    if kiln.chamber.shape != "round":
        return (
            "a dome over a square or curved plan (a sail dome) isn't a dome of revolution: its "
            "thrust network, which force pattern carries it to the corners, isn't built"
        )
    if len({layer.material for layer in kiln.lining.walls}) > 1:
        return "a round wall of several materials isn't built"
    return None


@dataclass(frozen=True)
class DomeResult:
    """A round kiln's dome on its wall, in one state: whether it stands with hoop compression and
    as lunes, the least push at its springing per metre of circumference (on fixed ground), and
    the working."""

    state: str
    stands: bool
    stands_as_lunes: bool
    thrust: float  # N/m of the springing's circumference
    steps: tuple[Step, ...]


def kiln_dome(kiln: Kiln, state: str = "cold", rings: int = 40) -> DomeResult:
    """A round kiln's spherical dome on its round wall, both from the design file: the acting
    ring's layers the shell, the layers over it its load, the wall's courses 2½ in."""
    why = kiln_not_modelled(kiln)
    if why is not None:
        raise NotModelledError(why)
    roof = kiln.roof
    assert isinstance(roof, DomeRoof)
    layers = kiln.lining.for_face("roof")
    acting, over = layers[: roof.acting_ring], layers[roof.acting_ring :]
    t = sum(si(x.thickness, "m") for x in acting)
    rho = sources.density(acting[0].material)
    span, rise = si(kiln.chamber.width, "m"), si(roof.rise, "m")
    shell = DomeShell.from_span_rise(span, rise, t, rho, rings)
    loads = [(si(x.thickness, "m"), sources.density(x.material)) for x in over]
    wall_t = sum(si(x.thickness, "m") for x in kiln.lining.walls)
    wall_rho = sources.density(kiln.lining.walls[0].material)
    height = si(kiln.chamber.height, "m")
    courses = max(1, round(height / sources.COURSE.value))
    mu = sources.MU_COLD if state == "cold" else sources.MU_HOT
    sec = section(shell, True, (wall_t, height, wall_rho, courses), overburden=loads)
    ok = solve(problem(sec, mu.value)).status is Status.OPTIMAL
    lunes = section(shell, False, (wall_t, height, wall_rho, courses), overburden=loads)
    ok_lunes = solve(problem(lunes, mu.value)).status is Status.OPTIMAL
    ground = section(shell, True, overburden=loads)
    p = problem(ground, mu.value)
    least = solve(p, force_on(assemble(p), ground, GROUND, 0), 1)
    r_s = shell.radius * math.sin(shell.springing)
    thrust = least.value / r_s if least.status is Status.OPTIMAL else math.nan
    hot_note = mu.note
    if state == "hot":
        hot_note = f"{mu.note}; the crushing stand-in isn't applied to the dome's joints yet"
    steps = (
        Step(
            name="The dome as rings of revolution",
            value=f"inner radius {show(Q_(shell.radius, 'm'), 'inch')}, springing "
            f"{math.degrees(shell.springing):.1f}° from the crown, {rings} rings; on a "
            f"{show(Q_(wall_t, 'm'), 'inch')} round wall {show(Q_(height, 'm'), 'inch')} high",
            formula="R = (D²/4 + h²)/(2h); per radian of azimuth, conical joints, hoop "
            "compression pushing each ring out, no hoop tension",
            reference="Heyman's hemisphere 0.042, Nodargi & Bisegna 0.04284 (domes-over-doors.md "
            "§D1): reproduced, 0.0428",
        ),
        Step(
            name=f"Friction ({state})",
            value=f"μ = {mu.value}",
            reference=mu.reference,
            note=hot_note,
        ),
        Step(
            name="An admissible state on the wall",
            value=("found" if ok else "none")
            + "; as lunes (no hoop force): "
            + ("found" if ok_lunes else "none"),
            reference="the LP of rigid.py (statics-software.md §11)",
        ),
        Step(
            name="The least push at the springing, a metre of its circumference",
            value=f"{thrust:.4g} N/m ({si(Q_(thrust, 'N/m'), 'lbf/ft'):.4g} lbf/ft)",
            formula="h = H/r_s, H the least horizontal push per radian on fixed supports "
            "(Lau 2006 Eq. 3.1)",
        ),
    )
    return DomeResult(state, ok, ok_lunes, thrust, steps)
