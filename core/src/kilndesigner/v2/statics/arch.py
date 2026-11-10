"""A circular arch of voussoirs on two supports: its least and most thrust, and its least
thickness.

The ring is the annulus between the intrados radius R and R + T, between the angles 90° ± φ about
its centre, cut by radial joints into voussoirs. Each voussoir is the exact annular sector, its
weight ρ·g·d·Δθ·((R + T)² − R²)/2 at its centroid 2/3 · ((R + T)³ − R³)/((R + T)² − R²) ·
sin(Δθ/2)/(Δθ/2) from the centre (Derived). The springing joints are radial: a skewback cut on
the arch's radius (HarbisonWalker's geometry, `docs/research/kiln-hardware.md` §4.3); a
semicircle's are level. Layers laid over the ring are its load (the engine's ``acting_ring``).

Each support is a fixed body. The least horizontal thrust on the supports is Heyman's
minimum-thrust state, an arch on spreading supports; the most is the maximum-thrust state, an
arch whose supports close on it, as a heated arch in a frame that holds its span
(`docs/research/arch-thrust-theory.md` §2). Where a straight line fits inside the ring from
skewback to skewback, R ≤ (R + T)·cos φ, rigid brick gives no maximum (§8): crushing at the
hinges then sets it (`crushing.py`).

The least thickness is the thickness below which no thrust line fits under the arch's own weight
(the Couplet–Heyman problem): 0.1075 of the centre line's radius for a semicircle with radial
joints (Milankovitch's value as Maia Avelino et al. 2020 quote it, `engine-v2-negative-cases.md`
§1), 0.10748 with true centroids.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from kilndesigner.v2.statics.blocks import G
from kilndesigner.v2.statics.rigid import (
    Body,
    Joint,
    Problem,
    Section,
    Solution,
    Status,
    assemble,
    force_on,
    solve,
)

SUPPORT = "support"
VOUSSOIR = "voussoir"


@dataclass(frozen=True)
class Overburden:
    """A layer laid over the ring: carried as load, not as part of the ring."""

    thickness: float  # m
    density: float  # kg/m³


@dataclass(frozen=True)
class ArchRing:
    """A circular ring of voussoirs: intrados radius, thickness (m), half the central angle φ
    (radians), density (kg/m³), the slice's depth (m) and the number of voussoirs."""

    radius: float
    thickness: float
    half_angle: float
    density: float
    depth: float = 1.0
    voussoirs: int = 40
    overburden: tuple[Overburden, ...] = ()

    def __post_init__(self) -> None:
        if not (self.radius > 0 and self.thickness > 0 and self.density >= 0 and self.depth > 0):
            raise ValueError("an arch ring needs a positive radius, thickness and depth")
        if not 0 < self.half_angle <= math.pi / 2:
            raise ValueError("an arch ring's half angle is between 0 and 90°")
        if self.voussoirs < 2:
            raise ValueError("an arch ring has at least two voussoirs")

    @classmethod
    def from_span_rise(
        cls,
        span: float,
        rise: float,
        thickness: float,
        density: float,
        depth: float = 1.0,
        voussoirs: int = 40,
        overburden: tuple[Overburden, ...] = (),
    ) -> ArchRing:
        """A segmental arch by its inside span and rise (m): R = S²/(8h) + h/2 and
        tan(φ/2) = 2h/S (kiln-hardware.md §4.3, formulas 1 and 5)."""
        if not 0 < rise <= span / 2:
            raise ValueError("a circular arch's rise is above 0 and at most half its span")
        radius = span**2 / (8 * rise) + rise / 2
        return cls(
            radius, thickness, 2 * math.atan(2 * rise / span), density, depth, voussoirs,
            overburden,
        )  # fmt: skip

    @classmethod
    def semicircle(
        cls, centre_radius: float, thickness: float, density: float, depth: float = 1.0,
        voussoirs: int = 40,
    ) -> ArchRing:  # fmt: skip
        """A half circle by its centre line's radius and its thickness (m)."""
        return cls(centre_radius - thickness / 2, thickness, math.pi / 2, density, depth, voussoirs)

    @property
    def span(self) -> float:
        """Inside span, m."""
        return 2 * self.radius * math.sin(self.half_angle)

    @property
    def rise(self) -> float:
        """Inside rise, m."""
        return self.radius * (1 - math.cos(self.half_angle))

    @property
    def straight_line_fits(self) -> bool:
        """R ≤ (R + T)·cos φ: no maximum-thrust state in rigid brick (arch-thrust-theory.md §8)."""
        return self.radius <= (self.radius + self.thickness) * math.cos(self.half_angle)

    @property
    def weight(self) -> float:
        """The ring's own weight over the slice, N."""
        r, t = self.radius, self.thickness
        return self.density * G * self.depth * self.half_angle * ((r + t) ** 2 - r**2)

    def section(self, centre_z: float = 0.0) -> Section:
        """Voussoirs 0 … n−1 from the right springing to the left, then the two supports."""
        r, ro, n = self.radius, self.radius + self.thickness, self.voussoirs
        a0 = math.pi / 2 - self.half_angle
        theta = a0 + 2 * self.half_angle * np.arange(n + 1) / n
        bodies: list[Body] = []
        for i in range(n):
            bodies.append(self._voussoir(i, float(theta[i]), float(theta[i + 1]), centre_z))
        bodies.append(Body("support R", 0.0, (ro, centre_z), True, SUPPORT))
        bodies.append(Body("support L", 0.0, (-ro, centre_z), True, SUPPORT))
        joints: list[Joint] = []
        for k in range(n + 1):
            th = float(theta[k])
            c, s = math.cos(th), math.sin(th)
            pts = ((r * c, centre_z + r * s), (ro * c, centre_z + ro * s))
            normal = (-s, c)  # the way θ grows: from the voussoir before into the one after
            a = n if k == 0 else k - 1  # the right support, or the voussoir before
            b = n + 1 if k == n else k  # the left support, or the voussoir after
            joints.append(Joint(a, b, pts, (normal, normal), self.depth))
        return Section(tuple(bodies), tuple(joints), self.depth)

    def _voussoir(self, i: int, t0: float, t1: float, centre_z: float) -> Body:
        r, ro = self.radius, self.radius + self.thickness
        weight, cx, cz = _sector(r, ro, t0, t1, self.density * G * self.depth)
        loads: list[tuple[float, float, float, float]] = []
        inner = ro
        for layer in self.overburden:
            w, x, z = _sector(
                inner, inner + layer.thickness, t0, t1, layer.density * G * self.depth
            )
            loads.append((x, centre_z + z, 0.0, -w))
            inner += layer.thickness
        return Body(f"voussoir {i + 1}", weight, (cx, centre_z + cz), False, VOUSSOIR, None,
                    tuple(loads))  # fmt: skip


def _sector(
    r0: float, r1: float, t0: float, t1: float, unit_weight: float
) -> tuple[float, float, float]:
    """An annular sector's weight (unit weight × area) and centroid (x, z) about its centre."""
    d = t1 - t0
    area = d * (r1**2 - r0**2) / 2
    rc = (2.0 / 3.0) * (r1**3 - r0**3) / (r1**2 - r0**2) * math.sin(d / 2) / (d / 2)
    mid = (t0 + t1) / 2
    return unit_weight * area, rc * math.cos(mid), rc * math.sin(mid)


@dataclass(frozen=True)
class Thrust:
    """The horizontal thrust on each support, per metre run of the arch (N/m), at the least
    (Heyman's minimum-thrust state) or the most, and the solution behind it."""

    value: float  # N/m; math.inf when unbounded, math.nan when no state exists
    status: Status
    solution: Solution


def thrust(ring: ArchRing, mu: float, sense: int, crush: float | None = None) -> Thrust:
    """``sense`` 1: the least thrust; −1: the most. ``mu``: friction at every joint; ``crush``:
    a crushing stress (Pa) at every joint, or None."""
    sec = ring.section()
    n = len(sec.joints)
    p = Problem(sec, (mu,) * n, (crush,) * n if crush is not None else ())
    cost = force_on(assemble(p), sec, SUPPORT, 0, outward=True)
    sol = solve(p, cost, sense)
    # both supports are summed in the cost: half is one support's, per metre run
    value = sol.value / 2 / ring.depth if sol.status is Status.OPTIMAL else sol.value
    return Thrust(value, sol.status, sol)


def stands(ring: ArchRing, mu: float) -> bool:
    """Whether any thrust line fits: an admissible state exists."""
    sec = ring.section()
    return solve(Problem(sec, (mu,) * len(sec.joints))).status is Status.OPTIMAL


def least_thickness(
    centre_radius: float,
    half_angle: float,
    density: float,
    mu: float,
    voussoirs: int = 160,
    tol: float = 1e-6,
) -> float:
    """The least thickness (m) of a circular arch of this centre line under its own weight, by
    bisection: the arch's thickness scales about the centre line, its weight with it. Returns
    math.nan if no thickness up to 0.6 of the radius stands (sliding governs: μ too low)."""

    def ok(t: float) -> bool:
        ring = ArchRing(centre_radius - t / 2, t, half_angle, density, 1.0, voussoirs)
        return stands(ring, mu)

    lo, hi = 1e-4 * centre_radius, 0.6 * centre_radius
    if not ok(hi):
        return math.nan
    while hi - lo > tol * centre_radius:
        mid = (lo + hi) / 2
        if ok(mid):
            hi = mid
        else:
            lo = mid
    return hi
