"""Radiation between the chamber's faces by Monte Carlo rays, with the setting in the way (ADR
0017 H5): trimesh's ray queries on Embree (embreex) against the faces the engine's own solids give,
so any chamber the engine draws and any obstruction in it are traced, partial shadows included
(`thermal-software.md` §5.1; `thermal-combinations.md` §2.3).

From each zone, points uniform by area and cosine-weighted directions into the gas; each ray's
first hit is tallied, and its length kept, as 200 quantiles a pair (`thermal-combinations.md` §3
#1), so a grey gas of any absorption coefficient k needs no new rays: the direct exchange areas
are (Hottel's zone method, one gas zone; Monnaemang 2015 eqs. 3.11–3.14):

    s_i s_j(k) = A_i · mean[e^(−k s) · 1(hit j)],   g s_i(k) = A_i · mean[1 − e^(−k s)].

Monte Carlo factors sum to 1 by row but aren't reciprocal; broken closure can put a wall's flux off
by over a factor of 2 (Clarksean & Solbrig 1993), so both are enforced to round-off by Larsen &
Howell's least-change smoothing (J. Heat Transfer 108, 1986, as Monnaemang 2015 §3.2.3 eqs.
3.33–3.44 restates it), x′_ij = x_ij + w_ij(λ_i + λ_j), with each pair's weight its tally's variance
(Loehrke et al. 1995's idea, via Frangi 2025 §3.5): the most accurate of five closures tried
(`thermal-software.md` §5.2).

Openings (flues, spy holes, inlet flues) are rectangles carved out of a flat face: rays leave them
uniformly and a hit inside one is the opening's.
"""

from __future__ import annotations

import math
import time
from collections.abc import Sequence
from dataclasses import dataclass, field, replace
from typing import Any

import numpy as np
import trimesh  # pyright: ignore[reportMissingTypeStubs]
from numpy.typing import NDArray

from kilndesigner.thermal.radiation import Enclosure
from kilndesigner.working import Step

type Vector = NDArray[np.float64]
type Matrix = NDArray[np.float64]

CHUNK = 100_000  # rays in flight: the memory the trace takes
QUANTILES = np.linspace(0.0025, 0.9975, 200)
# Embree works in float32: an origin moved less than its spacing (6e-8 at 0.5 m) is lost and the
# ray hits its own triangle (seen in the survey: half the rays), so 1e-6 m
OFFSET = 1e-6
LOST_LIMIT = 1e-4  # rays escaping a closed chamber, as a share: more is a leak in the mesh
SOURCES = (
    "trimesh 5.2 + embreex 4.4 (Embree); Hottel's zone method as Monnaemang 2015 eqs. 3.11–3.14 "
    "restates it; Larsen & Howell 1986's smoothing (Monnaemang §3.2.3), variance weights "
    "(Loehrke et al. 1995 via Frangi 2025 §3.5)"
)


class GeometryError(ValueError):
    """The scene isn't a closed chamber the rays can trace, or an opening isn't on its face."""


@dataclass(frozen=True)
class Zone:
    """A named set of triangles (m), each wound so its normal points into the gas."""

    name: str
    triangles: NDArray[np.float64]  # (n, 3, 3)


@dataclass(frozen=True)
class Patch:
    """An opening: a rectangle on a flat zone's plane, centre ± half[0]·u ± half[1]·v, with the
    zone's normal into the gas; carved out of that zone."""

    name: str
    face: str
    centre: tuple[float, float, float]
    u: tuple[float, float, float]
    v: tuple[float, float, float]
    half: tuple[float, float]

    @property
    def area(self) -> float:
        return 4 * self.half[0] * self.half[1]

    @property
    def normal(self) -> Vector:
        n = np.cross(np.asarray(self.u), np.asarray(self.v))
        return n / np.linalg.norm(n)

    def inside(self, p: Matrix, tol: float = 1e-6) -> NDArray[np.bool_]:
        d = p - np.asarray(self.centre)
        return (
            (np.abs(d @ np.asarray(self.u)) <= self.half[0])
            & (np.abs(d @ np.asarray(self.v)) <= self.half[1])
            & (np.abs(d @ self.normal) <= tol)
        )


def _geometry(tris: Matrix) -> tuple[Vector, Matrix]:
    e1, e2 = tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]
    cr = np.cross(e1, e2)
    area = 0.5 * np.linalg.norm(cr, axis=1)
    return area, cr / (2 * area[:, None])


def _directions(nrm: Matrix, rng: np.random.Generator) -> Matrix:
    """Cosine-weighted directions about each normal (Malley's method)."""
    m = len(nrm)
    helper = np.where(np.abs(nrm[:, [0]]) < 0.9, [[1.0, 0.0, 0.0]], [[0.0, 1.0, 0.0]])
    t1 = np.cross(nrm, helper)
    t1 /= np.linalg.norm(t1, axis=1)[:, None]
    t2 = np.cross(nrm, t1)
    u1, u2 = rng.random(m), rng.random(m)
    r, ph = np.sqrt(u1), 2 * np.pi * u2
    return (
        (r * np.cos(ph))[:, None] * t1
        + (r * np.sin(ph))[:, None] * t2
        + np.sqrt(1 - u1)[:, None] * nrm
    )


@dataclass(frozen=True)
class Rays:
    """The trace: each zone's area, the rays from it, how many first hit each zone, and each
    pair's path-length quantiles (m)."""

    names: tuple[str, ...]
    areas: Vector
    emitted: Vector
    counts: Matrix
    lengths: NDArray[np.float64]  # (n, n, Q)
    volume: float
    lost: int
    seconds: float
    steps: tuple[Step, ...] = field(default=())

    def index(self, name: str) -> int:
        return self.names.index(name)

    @property
    def raw(self) -> Matrix:
        """F_ij as tallied: the share of i's rays that first hit j."""
        return self.counts / self.emitted[:, None]

    def exchange(self, k: float) -> tuple[Matrix, Vector]:
        """The direct exchange areas for a grey gas of absorption coefficient k (1/m): s_i s_j
        (symmetric) and g s_i, closed so every surface's row sums to its area exactly.

        Each pair has two estimates, from i's rays and from j's; they are combined by their
        variances (Loehrke et al. 1995's reciprocity weighting, via Frangi 2025 §3.5.4), so a
        small opening's precise estimate isn't spoiled by a large face's few hits on it. Where
        only one direction saw the pair, the other's zero takes one hit's variance; a pair neither
        saw stays zero. Then Larsen & Howell's closure, weighted by the combined variance."""
        a, n = self.areas, self.emitted
        f = self.raw
        m1 = np.exp(-k * self.lengths).mean(axis=2)
        m2 = np.exp(-2 * k * self.lengths).mean(axis=2)
        x = a[:, None] * f * m1
        per_ray = np.maximum(f * m2 - (f * m1) ** 2, 0.0)
        seen = (self.counts > 0) | (self.counts.T > 0)
        np.fill_diagonal(seen, np.diag(self.counts) > 0)
        floor = np.where(seen & (self.counts == 0), 1.0 / n[:, None], 0.0)
        var = (a**2)[:, None] * np.maximum(per_ray, floor) / n[:, None]
        both = var + var.T
        safe = np.where(both > 0, both, 1.0)
        sym = np.where(both > 0, (x * var.T + x.T * var) / safe, 0.5 * (x + x.T))
        w = np.where(both > 0, var * var.T / safe, 0.0)
        g = a - x.sum(axis=1)
        m1t, m2t = (f * m1).sum(axis=1), (f * m2).sum(axis=1)
        var_g = a**2 * np.maximum(m2t - m1t**2, 0.0) / n
        return smooth(a, sym, w, g, var_g)

    def view(self) -> Enclosure:
        """The closed view factors as the engine's grey enclosure takes them."""
        ss, _ = self.exchange(0.0)
        return Enclosure(self.names, tuple(float(v) for v in self.areas), ss / self.areas[:, None])


def smooth(
    area: Vector, x: Matrix, w: Matrix, g: Vector | None = None, wg: Vector | None = None
) -> tuple[Matrix, Vector]:
    """Larsen & Howell's least change: x′ = x + w∘(λ_i + λ_j), g′ = g + w_g∘λ, with
    (diag(W1 + w_g) + W)λ = A − x1 − g, so x′ stays symmetric and every row of [x′ g′] sums to its
    area. Zero weights keep their entries; a negative entry left by the correction is refused."""
    g = np.zeros(len(area)) if g is None else g
    wg = np.zeros(len(area)) if wg is None else wg
    r = np.diag(w.sum(axis=1) + wg) + w
    lam = np.linalg.lstsq(r, area - x.sum(axis=1) - g, rcond=None)[0]
    x2 = x + w * (lam[:, None] + lam[None, :])
    g2 = g + wg * lam
    if x2.min() < -1e-12 * area.max() or g2.min() < -1e-12 * area.max():
        raise GeometryError("the closure drove an exchange area negative: too few rays")
    return np.maximum(x2, 0.0), np.maximum(g2, 0.0)


def trace(
    zones: Sequence[Zone],
    patches: Sequence[Patch] = (),
    rays: int = 100_000,
    seed: int = 20261110,
    volume: float | None = None,
    closed: bool = True,
) -> Rays:
    """Trace ``rays`` from every zone and opening. ``volume``, the gas's (m³), is the closed form
    when known; otherwise Cauchy's mean chord, 4V = Σ A_i·mean chord_i (Lienhard Table 10.4's
    L₀ = 4V/A), from the same rays. A chamber must be ``closed``: rays escaping it are refused as
    a leak in the mesh; in an open scene they go to the surroundings, untallied."""
    rng = np.random.default_rng(seed)
    t0 = time.perf_counter()
    tris = np.concatenate([z.triangles for z in zones])
    owner = np.concatenate([np.full(len(z.triangles), i) for i, z in enumerate(zones)])
    area_t, nrm_t = _geometry(tris)
    if np.any(area_t <= 0):
        raise GeometryError("a triangle has no area")
    mesh: Any = trimesh.Trimesh(
        tris.reshape(-1, 3), np.arange(len(tris) * 3).reshape(-1, 3), process=False
    )
    names = tuple([z.name for z in zones] + [p.name for p in patches])
    nz, n = len(zones), len(names)
    by_face: dict[int, list[tuple[int, Patch]]] = {}
    for j, p in enumerate(patches):
        if p.face not in names[:nz]:
            raise GeometryError(f"opening {p.name} is on {p.face!r}, not a zone")
        by_face.setdefault(names.index(p.face), []).append((nz + j, p))
    areas = np.zeros(n)
    for i in range(nz):
        areas[i] = area_t[owner == i].sum() - sum(p.area for _, p in by_face.get(i, []))
    for j, p in enumerate(patches):
        areas[nz + j] = p.area
        _check_on_face(p, tris[owner == names.index(p.face)])
    counts = np.zeros((n, n))
    lengths = np.zeros((n, n, len(QUANTILES)))
    lost = 0
    chord = np.zeros(n)
    for i in range(n):
        dist_by: list[list[Vector]] = [[] for _ in range(n)]
        done = 0
        while done < rays:
            m = min(CHUNK, rays - done)
            if i < nz:
                o, d = _emit_zone(tris, area_t, nrm_t, owner, i, by_face.get(i, []), m, rng)
            else:
                o, d = _emit_patch(patches[i - nz], m, rng)
            tri, ray, loc = mesh.ray.intersects_id(o, d, multiple_hits=False, return_locations=True)
            tri, ray = np.asarray(tri, dtype=int), np.asarray(ray, dtype=int)
            loc = np.asarray(loc, dtype=float)
            s = np.linalg.norm(loc - o[ray], axis=1)
            hit = owner[tri].copy()
            for face, items in by_face.items():
                on = hit == face
                for j, p in items:
                    sel = on & p.inside(loc)
                    hit[sel] = j
            lost += m - len(ray)
            chord[i] += s.sum()
            for j in range(n):
                sel = hit == j
                if sel.any():
                    dist_by[j].append(s[sel])
                    counts[i, j] += sel.sum()
            done += m
        for j in range(n):
            if dist_by[j]:
                lengths[i, j] = np.quantile(np.concatenate(dist_by[j]), QUANTILES)
    if closed and lost > LOST_LIMIT * rays * n:
        raise GeometryError(f"{lost} rays escaped the chamber: it isn't closed")
    emitted = np.full(n, float(rays))
    vol = volume if volume is not None else float((areas * chord / emitted).sum() / 4)
    seconds = time.perf_counter() - t0
    out = Rays(names, areas, emitted, counts, lengths, vol, lost, seconds)
    return replace(out, steps=(_working(out, len(tris)),))


def _check_on_face(p: Patch, face_tris: Matrix) -> None:
    """Each corner of the opening must lie on one of its face's triangles."""
    c, u, v = (np.asarray(x) for x in (p.centre, p.u, p.v))
    for su, sv in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        q = c + su * p.half[0] * u * (1 - 1e-9) + sv * p.half[1] * v * (1 - 1e-9)
        if not _on_triangles(q, face_tris):
            raise GeometryError(f"opening {p.name} isn't wholly on its face {p.face}")


def _on_triangles(q: Vector, tris: Matrix, tol: float = 1e-6) -> bool:
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    n = np.cross(b - a, c - a)
    nn = np.linalg.norm(n, axis=1)
    near = np.abs(((q - a) * n).sum(axis=1)) / nn <= tol
    v0, v1, v2 = c - a, b - a, q - a
    d00, d01, d11 = (v0 * v0).sum(1), (v0 * v1).sum(1), (v1 * v1).sum(1)
    d02, d12 = (v0 * v2).sum(1), (v1 * v2).sum(1)
    den = d00 * d11 - d01 * d01
    s = (d11 * d02 - d01 * d12) / den
    t = (d00 * d12 - d01 * d02) / den
    inside = (s >= -tol) & (t >= -tol) & (s + t <= 1 + tol)
    return bool(np.any(near & inside))


def _emit_zone(
    tris: Matrix,
    area_t: Vector,
    nrm_t: Matrix,
    owner: NDArray[np.int_],
    i: int,
    holes: Sequence[tuple[int, Patch]],
    m: int,
    rng: np.random.Generator,
) -> tuple[Matrix, Matrix]:
    """m points uniform by area on zone i outside its openings (rejection), and their rays."""
    idx = np.flatnonzero(owner == i)
    p_tri = area_t[idx] / area_t[idx].sum()
    pts: list[Matrix] = []
    nrms: list[Matrix] = []
    have = 0
    while have < m:
        pick = rng.choice(idx, size=m, p=p_tri)
        v = tris[pick]
        r1, r2 = rng.random(m), rng.random(m)
        s = np.sqrt(r1)
        q = (1 - s)[:, None] * v[:, 0] + (s * (1 - r2))[:, None] * v[:, 1]
        q += (s * r2)[:, None] * v[:, 2]
        keep = np.ones(m, dtype=bool)
        for _, p in holes:
            keep &= ~p.inside(q)
        pts.append(q[keep])
        nrms.append(nrm_t[pick][keep])
        have += int(keep.sum())
    q, nn = np.concatenate(pts)[:m], np.concatenate(nrms)[:m]
    return q + OFFSET * nn, _directions(nn, rng)


def _emit_patch(p: Patch, m: int, rng: np.random.Generator) -> tuple[Matrix, Matrix]:
    c, u, v = (np.asarray(x) for x in (p.centre, p.u, p.v))
    a = (2 * rng.random(m) - 1) * p.half[0]
    b = (2 * rng.random(m) - 1) * p.half[1]
    q = c + a[:, None] * u + b[:, None] * v
    nn = np.tile(p.normal, (m, 1))
    return q + OFFSET * nn, _directions(nn, rng)


def _working(r: Rays, triangles: int) -> Step:
    f = r.raw
    s = r.areas[:, None] * f
    recip = float(np.abs(s - s.T).max() / r.areas.max())
    return Step(
        name="Radiation between faces: Monte Carlo rays",
        value=f"{int(r.emitted[0]):,} rays from each of {len(r.names)} zones, {triangles} "
        f"triangles, {r.seconds:.1f} s; raw reciprocity off by {recip:.1e} of the largest area, "
        "closed to round-off",
        inputs={nm: f"{a:.4f} m²" for nm, a in zip(r.names, r.areas, strict=True)},
        formula="s_i s_j(k) = A_i·mean[e^(−ks)·1(hit j)]; g s_i(k) = A_i·mean[1 − e^(−ks)]; "
        "x′ = x + w∘(λ_i + λ_j), w the tally's variance",
        reference=SOURCES,
        note=f"{r.lost} rays escaped; gas volume {r.volume:.4f} m³",
    )


# --- zones from the engine's own solids ----------------------------------------------------------


def solid_zones(solid: Any, classify: Any, tol: float = 0.5, scale: float = 1e-3) -> list[Zone]:
    """The faces of a build123d solid (the gas volume) as named zones: OCCT's triangulation of
    each face (``tol`` its linear deflection in the solid's units), flipped so the normals point
    into the gas (a solid's faces point out), scaled to metres. ``classify`` names each face, or
    returns None to leave it out."""
    groups: dict[str, list[Matrix]] = {}
    for face in solid.faces():
        name = classify(face)
        if name is None:
            continue
        verts, idx = face.tessellate(tol, 0.2)
        v = np.array([[p.X, p.Y, p.Z] for p in verts], dtype=np.float64) * scale
        t = np.array([v[[a, c, b]] for a, b, c in idx])
        groups.setdefault(name, []).append(t)
    out: list[Zone] = []
    for name, ts in groups.items():
        t = np.concatenate(ts)
        area, _ = _geometry(t)
        out.append(Zone(name, t[area > 1e-14]))
    return out


def box_zone(name: str, lo: Sequence[float], hi: Sequence[float]) -> Zone:
    """A closed box in the gas (the setting's envelope): its twelve triangles, normals outward,
    into the gas around it."""
    b: Any = trimesh.creation.box(bounds=[list(lo), list(hi)])
    return Zone(name, np.asarray(b.triangles, dtype=np.float64))


def box_volume(lo: Sequence[float], hi: Sequence[float]) -> float:
    return math.prod(h - lo_ for lo_, h in zip(lo, hi, strict=True))
