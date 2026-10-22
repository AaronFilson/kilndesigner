"""Temperature-dependent thermal conductivity, and its integral (the Kirchhoff transform).

For steady 1D conduction with k(T), the heat flow through a layer is exact when written with
the integral of k:  Q · ∫dx/A(x) = ∫k(T) dT  between the layer's two faces. So the solver never
needs a "mean k"; it integrates the data sheet's k(T) directly.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass

from kilndesigner.numeric import find_root

# k never drops below this when extrapolated past a data sheet's last point (W/(m·K)).
_K_FLOOR = 1e-3


@dataclass(frozen=True)
class Conductivity:
    """k(T) as points (kelvin, W/(m·K)), linear between them and extrapolated beyond."""

    temperatures: tuple[float, ...]
    values: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.temperatures) != len(self.values) or not self.temperatures:
            raise ValueError("conductivity needs matching, non-empty temperature and k lists")
        if any(b <= a for a, b in zip(self.temperatures, self.temperatures[1:], strict=False)):
            raise ValueError("conductivity temperatures must increase")
        if any(k <= 0 for k in self.values):
            raise ValueError("conductivity must be positive")

    @staticmethod
    def constant(k: float) -> Conductivity:
        return Conductivity((300.0,), (k,))

    def _segment(self, t: float) -> tuple[float, float]:
        """Slope and intercept of the linear piece that applies at temperature ``t``."""
        ts, ks = self.temperatures, self.values
        if len(ts) == 1:
            return 0.0, ks[0]
        i = 0
        while i < len(ts) - 2 and t > ts[i + 1]:
            i += 1
        slope = (ks[i + 1] - ks[i]) / (ts[i + 1] - ts[i])
        return slope, ks[i] - slope * ts[i]

    def k(self, t: float) -> float:
        slope, intercept = self._segment(t)
        return max(slope * t + intercept, _K_FLOOR)

    def integral(self, t0: float, t1: float) -> float:
        """∫ k dT from t0 to t1 (W/m), exact for the piecewise-linear k."""
        if t1 < t0:
            return -self.integral(t1, t0)
        breaks = sorted({t0, t1, *(t for t in self.temperatures[1:-1] if t0 < t < t1)})
        total = 0.0
        for a, b in itertools.pairwise(breaks):
            # k is linear on [a, b] (apart from the floor, which only matters far off the data)
            total += 0.5 * (self.k(a) + self.k(b)) * (b - a)
        return total

    def upper_temperature(self, t0: float, target: float) -> float:
        """The temperature t1 with ∫ k dT from t0 to t1 equal to ``target`` (W/m)."""
        if target == 0:
            return t0
        k0 = self.k(t0)
        guess = t0 + target / k0
        lo, hi = (t0, max(guess, t0 + 1.0)) if target > 0 else (min(guess, t0 - 1.0), t0)

        def f(t: float) -> float:
            return self.integral(t0, t) - target

        while f(hi) < 0:
            hi += 2 * (hi - lo)
        while f(lo) > 0:
            lo -= 2 * (hi - lo)
        return find_root(f, lo, hi, xtol=1e-9)
