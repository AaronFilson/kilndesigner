"""Small typed wrappers around SciPy's numerics."""

from __future__ import annotations

from collections.abc import Callable
from typing import cast

from scipy.integrate import quad
from scipy.optimize import brentq


def find_root(f: Callable[[float], float], lo: float, hi: float, xtol: float = 1e-10) -> float:
    """The root of ``f`` between ``lo`` and ``hi``, where ``f`` changes sign (Brent's method)."""
    return float(cast("float", brentq(f, lo, hi, xtol=xtol)))


def integrate(f: Callable[[float], float], a: float, b: float) -> float:
    """∫ f from ``a`` to ``b`` (adaptive quadrature)."""
    value = cast("tuple[float, float]", quad(f, a, b))[0]
    return float(value)
