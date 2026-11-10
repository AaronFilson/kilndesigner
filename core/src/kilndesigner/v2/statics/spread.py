"""An arch on spreading supports: how far its supports can move apart before it collapses (N5).

As the supports spread the arch can't stay whole. It opens into a mechanism of three hinges, its
minimum-thrust state's (Heyman's arch on spreading supports): the crown's at the extrados and one
each side at the intrados, at the haunch, or at the springing for a flat arch. "Small movements of
the supports cause the formation of a three-hinged arch"; the voussoirs move as rigid bodies, "the
only admissible state of deformation of the element is the rotation around one of its edge"; and as
the arch deforms its intrados hinge can move (Coccia, Di Carlo & Rinaldi 2015, Int. J. Adv. Struct.
Eng. 7:307–320, read; on Ochsendorf 2002, ch. 5, and 2006, Struct. Eng. 84(2):29–36, as they report
them).

**The moved arch** (Derived). With its lower hinge at joint k and each support moved out u, the
blocks below each lower hinge move out with their support, and those above it turn about it so that
the crown's hinge stays on the arch's axis and the crown drops:

    with d = C − H, the crown's hinge from the lower one in the right half, the upper blocks turn
    by θ, where d_z·sin θ − |d_x|·(1 − cos θ) = u,

which has a root while u < |d| − |d_x|, where the three hinges line up. The opened joints touch only
at their hinges; every other joint is whole. Whether the moved arch stands is the LP of `rigid.py`
on its moved blocks: Ochsendorf's static method in the deformed configuration.

**The path.** The supports move out step by step. The hinge starts where the unmoved arch's least
thrust touches the intrados; where the arch moved about it has no admissible state, the hinge moves
to the next joint toward the crown or the springing if the arch moved about that one has (a hinge
"admissible" in the moved geometry, as Coccia et al. relocate theirs). The collapse spread is the
last spread with an admissible state, the last step halved until it is under ``tol`` of the
thickness. Checked against Ochsendorf's test arch as Coccia et al. give it (a semicircle of 16
voussoirs, 50 mm thick on a 220 mm mean radius, t/R 0.23: collapse measured at a 15.4 % increase of
the span, 16.9 % by Ochsendorf's static method, 32.24 mm and 16.53 % by their kinematic one) and
against their Eq. 18 for many voussoirs (`test_statics_spread.py`).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from kilndesigner.model import Kiln, SprungArch, arches_along
from kilndesigner.run_parts import chamber_arch, run_layout
from kilndesigner.shape import Arch
from kilndesigner.units import si
from kilndesigner.v2.statics import sources
from kilndesigner.v2.statics.arch import SUPPORT, ArchRing, Overburden
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

type Point = tuple[float, float]

STEPS = 200
"""Steps of the supports' movement to a thickness: collapse comes at 0.03–0.9 of the thickness on
a semicircle (Coccia et al. 2015 Eq. 18), so 6–180 steps before the last is halved."""


def _turn(v: Point, theta: float) -> Point:
    c, s = math.cos(theta), math.sin(theta)
    return (c * v[0] - s * v[1], s * v[0] + c * v[1])


def rotation(h: Point, c: Point, u: float) -> float | None:
    """The upper blocks' turn θ (radians, anticlockwise in the right half) when each support has
    moved out ``u`` m, the lower hinge at ``h`` and the crown's at ``c``; None once the hinges line
    up."""
    dx, dz = c[0] - h[0], c[1] - h[1]
    if u >= math.hypot(dx, dz) - abs(dx):
        return None
    lo, hi = 0.0, math.atan2(dz, abs(dx))  # the left side rises from −u to |d| − |d_x| − u
    for _ in range(80):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if dz * math.sin(mid) - abs(dx) * (1 - math.cos(mid)) < u else (lo, mid)
    return (lo + hi) / 2


def moved(ring: ArchRing, lower: int, u: float) -> Section | None:
    """The ring's section with each support moved out ``u`` m, the lower hinges at joint ``lower``
    (``ArchRing.section()``'s numbering, 0 the right springing) and its mirror, the crown's at the
    middle joint; None once the hinges line up."""
    n = ring.voussoirs
    if n % 2:
        raise ValueError("an arch on spreading supports is cut into an even number of voussoirs")
    crown = n // 2
    if not 0 <= lower < crown:
        raise ValueError("the lower hinge is a joint between the springing and the crown")
    sec = ring.section()
    h = sec.joints[lower].points[0]  # the intrados point
    theta = rotation(h, sec.joints[crown].points[1], u)  # the crown's extrados point
    if theta is None:
        return None

    def motion(body: int) -> tuple[float, Point, float]:
        """(turn, about, shift) of a body: the right half's below the hinge shift with their
        support, above it turn about the hinge; the left half's the mirror."""
        if body == n or (body < crown and body < lower):
            return 0.0, (0.0, 0.0), u
        if body < crown:
            return theta, h, u
        if body == n + 1 or body >= n - lower:
            return 0.0, (0.0, 0.0), -u
        return -theta, (-h[0], h[1]), -u

    def place(p: Point, m: tuple[float, Point, float]) -> Point:
        turn, (ax, az), shift = m
        x, z = _turn((p[0] - ax, p[1] - az), turn)
        return (ax + x + shift, az + z)

    bodies: list[Body] = []
    for i, b in enumerate(sec.bodies):
        m = motion(i)
        loads = tuple((*place((x, z), m), *_turn((fx, fz), m[0])) for x, z, fx, fz in b.loads)
        bodies.append(Body(b.name, b.weight, place(b.centroid, m), b.fixed, b.tag, b.material,
                           loads))  # fmt: skip
    joints: list[Joint] = []
    for k, j in enumerate(sec.joints):
        ma, mb = motion(j.a), motion(j.b)
        if ma == mb:
            joints.append(Joint(j.a, j.b, tuple(place(p, mb) for p in j.points),
                                tuple(_turn(v, mb[0]) for v in j.normals), j.depth))  # fmt: skip
            continue
        # an opened joint touches at its hinge alone (the crown's at the extrados), its normal
        # halfway between its two faces'
        point = place(j.points[1 if k == crown else 0], mb)
        normal = _turn(j.normals[0], (ma[0] + mb[0]) / 2)
        joints.append(Joint(j.a, j.b, (point,), (normal,), j.depth, planar=False))
    return Section(tuple(bodies), tuple(joints), sec.depth)


def stands(ring: ArchRing, lower: int, u: float, mu: float = 0.6) -> bool:
    """Whether the ring moved ``u`` m a side about its hinges at ``lower`` has an admissible
    state."""
    sec = moved(ring, lower, u)
    if sec is None:
        return False
    return solve(Problem(sec, (mu,) * len(sec.joints))).status is Status.OPTIMAL


SLIDING = (
    "a joint of the ring's least-thrust state is at its friction limit: sliding governs, and the "
    "three-hinge mechanism, the blocks only turning, doesn't follow"
)


def first_hinge(ring: ArchRing, mu: float = 0.6) -> int:
    """Where the unmoved ring's least-thrust state touches the intrados, in the right half: the
    touching joint nearest the crown. Refused where a joint of that state slides."""
    sec = ring.section()
    p = Problem(sec, (mu,) * len(sec.joints))
    sol = solve(p, force_on(assemble(p), sec, SUPPORT, 0, outward=True), 1)
    if sol.status is not Status.OPTIMAL:
        raise ValueError("the ring has no admissible state unmoved")
    crown = ring.voussoirs // 2
    touching = [k for k in range(crown) if sol.joints[k].e <= -0.5 + 1e-6]
    if not touching or any(s.t_over_n >= mu - 1e-6 for s in sol.joints):
        raise ValueError(SLIDING)
    return max(touching)


@dataclass(frozen=True)
class Collapse:
    """The spread at collapse: each support's movement (m), the span's increase over the inside
    span, and the lower hinge's joint first and at the end."""

    u: float
    increase: float
    first: int
    last: int


def collapse(ring: ArchRing, mu: float = 0.6, tol: float = 1e-3) -> Collapse:
    """Move the supports out step by step until no hinge leaves the arch an admissible state; the
    last step halved until it is under ``tol`` of the ring's thickness."""
    k = first = first_hinge(ring, mu)
    crown = ring.voussoirs // 2
    u, du = 0.0, ring.thickness / STEPS
    while True:
        nxt = next((c for c in (k, k + 1) if c < crown and stands(ring, c, u + du, mu)), None)
        if nxt is not None:
            k, u = nxt, u + du
            continue
        if du <= tol * ring.thickness:
            break
        du /= 2
    return Collapse(u, 2 * u / ring.span, first, k)


# ------------------------------------------------------------------------------------ a kiln


def kiln_rings(kiln: Kiln) -> list[tuple[str, ArchRing]]:
    """A kiln's arch rings from its design file, as v2's sections take them: the acting ring's
    layers, the layers over it as load; one voussoir to each 2½ in of extrados (Olsen pp.19–20),
    evened, the half angle at most a semicircle's (past one, laid level on its walls). An arch
    across the width (at its widest station), or each chamber's of a row along the draft (one of
    each size). Refused, with the reason: not a sprung arch, a crossing, an offset peak or uneven
    springings (not symmetrical)."""
    roof, c = kiln.roof, kiln.chamber
    if not isinstance(roof, SprungArch):
        raise ValueError(f"spreading supports are worked for sprung arches, not a {roof.type}")
    if roof.crossing is not None or roof.peak_at is not None or roof.front_springline is not None:
        raise ValueError(
            "a crossing, an offset peak or uneven springings: the arch isn't symmetrical, and the "
            "spreading is worked for a symmetrical one"
        )
    layers = kiln.lining.for_face("roof")
    t = sum(si(x.thickness, "m") for x in layers[: roof.acting_ring])
    rho = sources.density(layers[0].material)
    over = tuple(Overburden(si(x.thickness, "m"), sources.density(x.material))
                 for x in layers[roof.acting_ring :])  # fmt: skip
    spans: list[tuple[str, float, float]] = []
    if arches_along(kiln):
        run = run_layout(kiln)
        for i in range(run.chambers):
            a = chamber_arch(kiln, run, i)
            if all(abs(a.span / 1000 - s) > 1e-6 or abs(a.rise / 1000 - r) > 1e-6
                   for _, s, r in spans):  # fmt: skip
                spans.append((f"chamber {i + 1}", a.span / 1000, a.rise / 1000))
    else:
        width = si(c.width, "m")
        if c.widths is not None:
            width = max(si(w.width, "m") for w in c.widths)
        spans.append(("across", width, si(roof.rise, "m") * width / si(c.width, "m")))
    out: list[tuple[str, ArchRing]] = []
    for label, span, rise in spans:
        arch = Arch(span, rise)
        phi = min(arch.half_angle, math.pi / 2)
        n = max(4, 2 * round((arch.radius + t) * phi / sources.COURSE.value))
        out.append((label, ArchRing(arch.radius, t, phi, rho, 1.0, n, over)))
    return out
