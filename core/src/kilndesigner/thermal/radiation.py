"""Radiation between the faces of a chamber: view factors and grey-body exchange.

View factors (radiation-exchange.md §1):
- identical, parallel, directly opposed rectangles: Howell's catalogue C-11, Lienhard Table 10.3
  case 1;
- two rectangles sharing an edge at 90°: Howell C-14, Lienhard Table 10.3 case 2;
- coaxial parallel discs: Lienhard Table 10.3 case 3;
- view-factor algebra: summation (Lienhard eq. 10.12), reciprocity (eq. 10.15), and a concave
  face over an opening sees what the opening sees (Lienhard Examples 10.1 and 10.3).

Exchange (radiation-exchange.md §2): diffuse, grey, opaque faces, each at one temperature, with a
transparent gas between them; the radiosities solve Lienhard eq. 10.42,
B_i = (1 − ε_i) Σ_j F_ij B_j + ε_i σ T_i⁴, and q_i = B_i − Σ_j F_ij B_j. Gas radiation (CO₂ and
H₂O in a fuel-fired kiln) is left out: radiation-exchange.md §4.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from kilndesigner.thermal.surface import STEFAN_BOLTZMANN

type Matrix = NDArray[np.float64]

# Reciprocity and summation hold to this, or the view factors are refused
CLOSURE_TOLERANCE = 1e-9

BOX_FACES = ("left", "right", "back", "front", "floor", "roof")


def parallel_rectangles(a: float, b: float, c: float) -> float:
    """F from one a × b rectangle to an identical one directly opposite, c apart.

    Howell C-11; Lienhard Table 10.3 case 1: X = a/c, Y = b/c,
    F = 2/(πXY)·{ln[(1+X²)(1+Y²)/(1+X²+Y²)]^½ + X√(1+Y²)·atan(X/√(1+Y²))
                 + Y√(1+X²)·atan(Y/√(1+X²)) − X·atan X − Y·atan Y}.
    """
    if a <= 0 or b <= 0 or c <= 0:
        raise ValueError("parallel rectangles need positive sizes and spacing")
    x, y = a / c, b / c
    x2, y2 = x * x, y * y
    sx, sy = math.sqrt(1 + x2), math.sqrt(1 + y2)
    bracket = (
        0.5 * math.log((1 + x2) * (1 + y2) / (1 + x2 + y2))
        + x * sy * math.atan(x / sy)
        + y * sx * math.atan(y / sx)
        - x * math.atan(x)
        - y * math.atan(y)
    )
    return 2 / (math.pi * x * y) * bracket


def perpendicular_rectangles(w: float, h: float, length: float) -> float:
    """F from a w × l rectangle to an h × l one sharing its l edge at 90°.

    Howell C-14; Lienhard Table 10.3 case 2: H = h/l, W = w/l,
    F = 1/(πW)·{W·atan(1/W) + H·atan(1/H) − √(H²+W²)·atan(1/√(H²+W²))
                + ¼ ln([(1+W²)(1+H²)/(1+W²+H²)]
                       · [W²(1+W²+H²)/((1+W²)(W²+H²))]^(W²)
                       · [H²(1+H²+W²)/((1+H²)(H²+W²))]^(H²))}.
    """
    if w <= 0 or h <= 0 or length <= 0:
        raise ValueError("perpendicular rectangles need positive sizes")
    big_w, big_h = w / length, h / length
    w2, h2 = big_w * big_w, big_h * big_h
    r = math.sqrt(w2 + h2)
    log_term = (
        math.log((1 + w2) * (1 + h2) / (1 + w2 + h2))
        + w2 * math.log(w2 * (1 + w2 + h2) / ((1 + w2) * (w2 + h2)))
        + h2 * math.log(h2 * (1 + h2 + w2) / ((1 + h2) * (h2 + w2)))
    )
    return (
        1
        / (math.pi * big_w)
        * (
            big_w * math.atan(1 / big_w)
            + big_h * math.atan(1 / big_h)
            - r * math.atan(1 / r)
            + 0.25 * log_term
        )
    )


def coaxial_discs(r1: float, r2: float, h: float) -> float:
    """F from a disc of radius r1 to a parallel coaxial disc of radius r2, h apart.

    Lienhard Table 10.3 case 3: R1 = r1/h, R2 = r2/h, X = 1 + (1 + R2²)/R1²,
    F = ½[X − √(X² − 4(R2/R1)²)].
    """
    if r1 <= 0 or r2 <= 0 or h <= 0:
        raise ValueError("coaxial discs need positive radii and spacing")
    big_r1, big_r2 = r1 / h, r2 / h
    x = 1 + (1 + big_r2 * big_r2) / (big_r1 * big_r1)
    return 0.5 * (x - math.sqrt(x * x - 4 * (big_r2 / big_r1) ** 2))


@dataclass(frozen=True)
class Enclosure:
    """Named faces, their areas (m²) and the view factors F[i][j] from face i to face j."""

    names: tuple[str, ...]
    areas: tuple[float, ...]
    view: Matrix

    def __post_init__(self) -> None:
        n = len(self.names)
        if len(self.areas) != n or self.view.shape != (n, n):
            raise ValueError("an enclosure needs one area and one row of view factors per face")
        check_closure(self.areas, self.view)

    def factor(self, a: str, b: str) -> float:
        return float(self.view[self.names.index(a), self.names.index(b)])


def check_closure(areas: Sequence[float], view: Matrix) -> None:
    """Refuse view factors that break summation (each row sums to 1, Lienhard eq. 10.12) or
    reciprocity (A_i F_ij = A_j F_ji, eq. 10.15), or that fall outside 0–1."""
    a = np.asarray(areas, dtype=float)
    if np.any(view < -CLOSURE_TOLERANCE) or np.any(view > 1 + CLOSURE_TOLERANCE):
        raise ValueError("a view factor lies outside 0–1")
    rows = view.sum(axis=1)
    if np.any(np.abs(rows - 1) > CLOSURE_TOLERANCE):
        raise ValueError(f"view factors don't sum to 1 from each face: {rows}")
    flow = a[:, None] * view
    if np.any(np.abs(flow - flow.T) > CLOSURE_TOLERANCE * max(float(a.max()), 1.0)):
        raise ValueError("view factors break reciprocity, A_i F_ij = A_j F_ji")


def box(width: float, depth: float, height: float) -> Enclosure:
    """The six inside faces of a rectangular chamber, as ``BOX_FACES``: left and right are
    depth × height (across the width), back and front width × height (across the depth), floor
    and roof width × depth (across the height). Every factor is from C-11 or C-14; a face sees
    none of itself."""
    w, d, h = width, depth, height
    sizes = {
        "left": (d, h),
        "right": (d, h),
        "back": (w, h),
        "front": (w, h),
        "floor": (w, d),
        "roof": (w, d),
    }
    opposite = {"left": "right", "right": "left", "back": "front", "front": "back"}
    opposite |= {"floor": "roof", "roof": "floor"}
    gap = {"left": w, "right": w, "back": d, "front": d, "floor": h, "roof": h}
    # The edge each pair of adjoining faces shares
    axis = {"left": "x", "right": "x", "back": "y", "front": "y", "floor": "z", "roof": "z"}
    extent = {"x": w, "y": d, "z": h}
    n = len(BOX_FACES)
    view = np.zeros((n, n))
    for i, a in enumerate(BOX_FACES):
        for j, b in enumerate(BOX_FACES):
            if a == b:
                continue
            if opposite[a] == b:
                p, q = sizes[a]
                view[i, j] = parallel_rectangles(p, q, gap[a])
                continue
            # Adjoining: the shared edge runs along the axis neither face is normal to
            (common,) = {"x", "y", "z"} - {axis[a], axis[b]}
            length = extent[common]
            view[i, j] = perpendicular_rectangles(extent[axis[b]], extent[axis[a]], length)
    areas = tuple(sizes[f][0] * sizes[f][1] for f in BOX_FACES)
    return Enclosure(BOX_FACES, areas, view)


def covered(enclosure: Enclosure, face: str, area: float) -> Enclosure:
    """Replace a flat face by a concave one of ``area`` spanning the same opening (an arch or a
    dome over the springline). Everything leaving the cover towards the rest passes through the
    opening, so F_cover→j = (A_open/A_cover)·F_open→j and the cover sees itself with
    1 − A_open/A_cover (Lienhard Examples 10.1, 10.3; reciprocity, eq. 10.15). Exact for
    radiosity uniform over the cover."""
    k = enclosure.names.index(face)
    opening = enclosure.areas[k]
    if area < opening * (1 - CLOSURE_TOLERANCE):
        raise ValueError("a concave cover can't be smaller than the opening it spans")
    ratio = opening / area
    view = enclosure.view.copy()
    view[k, :] *= ratio
    view[k, k] = 1 - ratio
    areas = tuple(area if i == k else a for i, a in enumerate(enclosure.areas))
    return Enclosure(enclosure.names, areas, view)


@dataclass(frozen=True)
class Exchange:
    """The radiosities B (W/m²) and the net flux q (W/m², leaving) and power Q (W) of each face."""

    radiosity: NDArray[np.float64]
    flux: NDArray[np.float64]
    power: NDArray[np.float64]


def exchange(
    enclosure: Enclosure,
    emissivity: Sequence[float],
    temperature: Sequence[float | None],
    flux: Sequence[float | None] | None = None,
) -> Exchange:
    """Solve the grey enclosure. Each face has a temperature (K) or, where the temperature is
    None, a net flux leaving it (W/m²; 0 for a face that only re-radiates, Lienhard's insulated
    "refractory surface"). Rows: B_i − (1 − ε_i) Σ_j F_ij B_j = ε_i σT_i⁴ for a known
    temperature (eq. 10.42), B_i − Σ_j F_ij B_j = q_i for a known flux (eqs. 10.39, 10.41)."""
    n = len(enclosure.names)
    eps = np.asarray(emissivity, dtype=float)
    if eps.shape != (n,) or np.any(eps <= 0) or np.any(eps > 1):
        raise ValueError("each face needs an emissivity above 0 and up to 1")
    given = [None] * n if flux is None else list(flux)
    if len(temperature) != n or len(given) != n:
        raise ValueError("each face needs a temperature or a flux")
    f = enclosure.view
    m = np.eye(n)
    rhs = np.zeros(n)
    for i, t in enumerate(temperature):
        if t is not None:
            m[i] -= (1 - eps[i]) * f[i]
            rhs[i] = eps[i] * STEFAN_BOLTZMANN * t**4
        else:
            q = given[i]
            if q is None:
                raise ValueError(f"face {enclosure.names[i]} has neither a temperature nor a flux")
            m[i] -= f[i]
            rhs[i] = q
    if all(t is None for t in temperature):
        raise ValueError("at least one face needs a temperature")
    b = np.linalg.solve(m, rhs)
    q_net = b - f @ b
    return Exchange(b, q_net, q_net * np.asarray(enclosure.areas))


def surface_temperature(ex: Exchange, emissivity: float, i: int) -> float:
    """A face's temperature from its radiosity and net flux: σT⁴ = B + q(1 − ε)/ε (eq. 10.39)."""
    e_b = ex.radiosity[i] + ex.flux[i] * (1 - emissivity) / emissivity
    return float((e_b / STEFAN_BOLTZMANN) ** 0.25)
