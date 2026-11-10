"""Gas radiation (ADR 0017 H6): the products' CO₂ and H₂O as a weighted sum of grey gases inside
Hottel's zone method, one well-stirred gas zone, every surface grey and diffuse.

**The grey gases.** A published weighted-sum-of-grey-gases (WSGG) set: grey gas j absorbs with
k_j = κ_j·(p_H₂O + p_CO₂) and carries the share a_j(T) of a blackbody's emission at T; the clear
gas the rest, 1 − Σ a_j (`thermal-software.md` §6):
- **Bordbar, Węcel & Hyppänen 2014**, Combust. Flame 161:2435, a HITEMP-2010 line-by-line fit in
  the molar ratio MR = x_H₂O/x_CO₂ (0.01–4), 300–2400 K; its 168 coefficients as NIST's Fire
  Dynamics Simulator codes them (`Source/radi.f90`, lines 3222–3271, commit f6cc57b; NIST's notice:
  not subject to US copyright, use allowed with NIST acknowledged) and as BYU's RadLib (MIT) does,
  the two agreeing to 1e-7. The adopted set.
- **Dorigon, Galarça & França 2013**, IJHMT 64:863, a HITEMP-2010 fit at MR 1 and 2, 400–2500 K,
  read in the ENCIT 2012 paper 118, Tables 1–2: the second set for the band (the two differ by up
  to 13 %; both are within about ±10 %, 19 % at 600 K, of Alberti's line-by-line tables).
Outside a set's temperature range its weights are held at the range's ends (FDS does the same;
said in the working): a surface below 300 K emits under 0.2 % of what it does at 1000 K.

**The exchange** (Monnaemang 2015 eqs. 3.11–3.14, after Hottel & Sarofim 1967 and Modest 2013):
for each grey gas, with the direct exchange areas s s and g s from the rays (`rays.py`),

    [diag(A) − diag(1 − ε)·s s] J = A ε E_s + (1 − ε) g s E_g,
    q_i = ε_i (Σ_j s s_ij J_j + g s_i E_g − A_i E_s,i),

E_s = a_j(T_s)σT_s⁴, E_g = a_j(T_g)σT_g⁴; summed over the grey gases and the clear one. The gas
loses what the surfaces gain, Σ q_i, the enclosure being closed. Soot isn't counted (no kiln
flame's soot fraction is in any source read; ADR 0017 leaves soot radiation out).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

import numpy as np
from numpy.typing import NDArray

from kilndesigner.thermal.surface import STEFAN_BOLTZMANN as SIGMA

type Vector = NDArray[np.float64]
type Matrix = NDArray[np.float64]

# Bordbar 2014 as FDS radi.f90 lines 3222–3271 code it: C[j][k][l] for grey gas j, power k of
# T/1200 K, power l of MR; d[j][l]: κ_j = Σ_l d_jl MR^l in 1/(atm·m)
BORDBAR_C = (
    ((0.7412956, -0.5244441, 0.5822860, -0.2096994, 0.0242031),
     (-0.9412652, 0.2799577, -0.7672319, 0.3204027, -0.0391017),
     (0.8531866, 0.0823075, 0.5289430, -0.2468463, 0.0310940),
     (-0.3342806, 0.1474987, -0.4160689, 0.1697627, -0.0204066),
     (0.0431436, -0.0688622, 0.1109773, -0.0420861, 0.0049188)),
    ((0.1552073, -0.4862117, 0.3668088, -0.1055508, 0.0105857),
     (0.6755648, 1.4092710, -1.3834490, 0.4575210, -0.0501976),
     (-1.1253940, -0.5913199, 0.9085441, -0.3334201, 0.0384236),
     (0.6040543, -0.0553385, -0.1733014, 0.0791608, -0.0098934),
     (-0.1105453, 0.0464663, -0.0016129, -0.0035398, 0.0006121)),
    ((0.2550242, 0.3805403, -0.4249709, 0.1429446, -0.0157408),
     (-0.6065428, 0.3494024, 0.1853509, -0.1013694, 0.0130244),
     (0.8123855, -1.1020090, 0.4046178, -0.0811822, 0.0062981),
     (-0.4532290, 0.6784475, -0.3432603, 0.0883088, -0.0084152),
     (0.0869309, -0.1306996, 0.0741446, -0.0202929, 0.0020110)),
    ((-0.0345199, 0.2656726, -0.1225365, 0.0300151, -0.0028205),
     (0.4112046, -0.5728350, 0.2924490, -0.0798076, 0.0079966),
     (-0.5055995, 0.4579559, -0.2616436, 0.0764841, -0.0079084),
     (0.2317509, -0.1656759, 0.1052608, -0.0321935, 0.0033870),
     (-0.0375491, 0.0229520, -0.0160047, 0.0050463, -0.0005364)),
)  # fmt: skip
BORDBAR_D = (
    (0.0340429, 0.0652305, -0.0463685, 0.0138684, -0.0014450),
    (0.3509457, 0.7465138, -0.5293090, 0.1594423, -0.0166326),
    (4.5707400, 2.1680670, -1.4989010, 0.4917165, -0.0542999),
    (109.81690, -50.923590, 23.432360, -5.1638920, 0.4393889),
)  # fmt: skip
BORDBAR_REF = (
    "Bordbar, Węcel & Hyppänen, Combust. Flame 161 (2014) 2435–2445 (HITEMP-2010 LBL), as NIST "
    "FDS Source/radi.f90 lines 3222–3271 (commit f6cc57b; NIST: not subject to US copyright) and "
    "BYU RadLib rad_wsgg.cc (MIT) code it (thermal-software.md §6.1)"
)
# Dorigon et al. 2013, ENCIT 2012 paper 118 Tables 1–2: κ_j (1/(atm·m)); a_j = Σ_k b_jk T^k, T in K
DORIGON = {
    1.0: (
        (0.187, 1.723, 12.484, 144.938),
        ((7.197e-02, 8.724e-04, -9.690e-07, 4.651e-10, -7.917e-14),
         (1.107e-01, 3.397e-04, -2.467e-07, 4.647e-11, -1.039e-15),
         (2.091e-01, -6.423e-05, -3.200e-08, 1.718e-11, -2.105e-15),
         (7.092e-02, 6.586e-05, -1.278e-07, 5.577e-11, -7.709e-15)),
    ),
    2.0: (
        (0.192, 1.719, 11.370, 111.016),
        ((5.617e-02, 7.844e-04, -8.563e-07, 4.246e-10, -7.440e-14),
         (1.426e-01, 1.795e-04, -1.077e-08, -6.971e-11, 1.774e-14),
         (1.362e-01, 2.574e-04, -3.711e-07, 1.575e-10, -2.267e-14),
         (1.222e-01, -2.327e-05, -7.492e-08, 4.275e-11, -6.608e-15)),
    ),
}  # fmt: skip
DORIGON_REF = (
    "Dorigon, Galarça & França, ENCIT 2012 paper 118, Tables 1–2 (the IJHMT 64 (2013) 863 set; "
    "HITEMP-2010 LBL), read in thermal-software.md §6.1"
)


class RangeError(ValueError):
    """A gas composition outside the range a set was fitted for (ADR 0009)."""


@dataclass(frozen=True)
class WSGG:
    """A WSGG set at one molar ratio: κ_j (1/(atm·m)) and a_j(T) = Σ_k c_jk (T/T_ref)^k."""

    name: str
    reference: str
    kappa: Vector
    coef: Matrix  # (J, K)
    t_ref: float
    t_range: tuple[float, float]
    mr: float
    note: str = ""

    def weights(self, t: float | Vector) -> Vector:
        """a_j at each temperature (K): shape (J,) for a scalar, (n, J) for n temperatures;
        held at the set's range ends outside it."""
        tt = np.clip(np.asarray(t, dtype=float), *self.t_range) / self.t_ref
        return (tt[..., None] ** np.arange(self.coef.shape[1])) @ self.coef.T

    def emissivity(self, t: float, pl: float) -> float:
        """A homogeneous path's total emissivity, Σ a_j(T)(1 − e^(−κ_j pL)), pL in atm·m."""
        return float(np.sum(self.weights(t) * (1 - np.exp(-self.kappa * pl))))


def bordbar2014(mr: float) -> WSGG:
    if not 0.01 <= mr <= 4.0:
        raise RangeError(f"MR {mr:.3g} is outside Bordbar 2014's 0.01–4")
    d = np.asarray(BORDBAR_D)
    c = np.asarray(BORDBAR_C)
    powers = mr ** np.arange(d.shape[1])
    return WSGG("Bordbar 2014", BORDBAR_REF, d @ powers, c @ powers, 1200.0, (300.0, 2400.0), mr)


def dorigon2013(mr: float) -> WSGG:
    """Dorigon's set at MR 1 or 2, whichever is nearer (the gap is said)."""
    if not 0.5 <= mr <= 4.0:
        raise RangeError(f"MR {mr:.3g}: Dorigon 2013 is fitted at MR 1 and 2 only")
    at = 1.0 if mr < 1.5 else 2.0
    kappa, b = DORIGON[at]
    note = "" if abs(mr - at) < 0.02 else f"the products' MR {mr:.2f} taken at the set's {at:g}"
    return WSGG(
        f"Dorigon 2013 (MR {at:g})", DORIGON_REF, np.asarray(kappa), np.asarray(b), 1.0,
        (400.0, 2500.0), at, note,
    )  # fmt: skip


@dataclass(frozen=True)
class GasExchange:
    """One gas zone's radiation: the surfaces' areas and, per grey gas (the clear gas first), the
    direct exchange areas, with the set and the absorbing partial pressure (atm) they were made
    for. ``wsgg`` None: a transparent gas (radiation between faces only)."""

    areas: Vector
    deas: tuple[tuple[Matrix, Vector], ...]
    wsgg: WSGG | None
    pwc: float

    def surface_weights(self, t: Vector) -> Matrix:
        """(n, J + 1): each surface's emission shares, the clear gas first."""
        if self.wsgg is None:
            return np.ones((len(t), 1))
        a = self.wsgg.weights(t)
        return np.column_stack([1.0 - a.sum(axis=1), a])

    def gas_weights(self, t_gas: float) -> Vector:
        if self.wsgg is None:
            return np.zeros(1)
        a = self.wsgg.weights(t_gas)
        return np.concatenate([[0.0], a])

    def net(self, t_gas: float, temps: Vector, eps: Vector) -> Vector:
        """Net radiation into each surface (W): the zone method summed over the grey gases. The
        gas loses their sum."""
        a = self.areas
        ws, wg = self.surface_weights(temps), self.gas_weights(t_gas)
        bs, bg = SIGMA * temps**4, SIGMA * t_gas**4
        q = np.zeros(len(a))
        for m, (ss, gs) in enumerate(self.deas):
            es, eg = ws[:, m] * bs, wg[m] * bg
            lhs = np.diag(a) - (1 - eps)[:, None] * ss
            j = np.linalg.solve(lhs, a * eps * es + (1 - eps) * gs * eg)
            q += eps * (ss @ j + gs * eg - a * es)
        return q


class Traced(Protocol):
    """A trace that gives the direct exchange areas for a grey gas, as `rays.Rays` does."""

    @property
    def areas(self) -> Vector: ...

    def exchange(self, k: float) -> tuple[Matrix, Vector]: ...


def exchange_for(traced: Traced, wsgg: WSGG | None, pwc: float) -> GasExchange:
    """The direct exchange areas for each grey gas from a trace: the clear gas at k = 0, grey gas
    j at k_j = κ_j·(p_H₂O + p_CO₂) (1/m, with pwc in atm)."""
    ks: Sequence[float] = [0.0] if wsgg is None else [0.0, *(float(k) * pwc for k in wsgg.kappa)]
    return GasExchange(traced.areas, tuple(traced.exchange(k) for k in ks), wsgg, pwc)
