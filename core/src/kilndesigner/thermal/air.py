"""Properties of air at 1 atm, from the Neutrium table (electric-and-thermal.md §6.3, [S63]).

Linear interpolation between the table's rows, 250 K to 1000 K. The table is Holman's (Heat
Transfer, Table A-5) rather than Incropera's Table A.4, as the science review of 2026-10-28 found:
its 300 K density is Holman's 1.177 kg/m³, not Incropera's 1.161. The two differ by under 2 % in
the surface coefficient.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass

import numpy as np

_T = np.array([250, 300, 400, 500, 600, 700, 800, 900, 1000], dtype=float)
_RHO = np.array([1.413, 1.177, 0.883, 0.706, 0.589, 0.504, 0.441, 0.392, 0.353])
_CP = np.array([1003, 1005, 1013, 1029, 1051, 1075, 1099, 1120, 1141], dtype=float)
_K = np.array([0.0223, 0.0261, 0.0331, 0.0395, 0.0456, 0.0513, 0.0569, 0.0625, 0.0672])
_MU = np.array([1.610, 1.850, 2.290, 2.680, 3.030, 3.350, 3.640, 3.920, 4.180]) * 1e-5

T_MIN, T_MAX = float(_T[0]), float(_T[-1])


@dataclass(frozen=True)
class Air:
    temperature: float  # K
    density: float  # kg/m³
    specific_heat: float  # J/(kg·K)
    conductivity: float  # W/(m·K)
    viscosity: float  # Pa·s

    @property
    def kinematic_viscosity(self) -> float:
        return self.viscosity / self.density

    @property
    def diffusivity(self) -> float:
        return self.conductivity / (self.density * self.specific_heat)

    @property
    def prandtl(self) -> float:
        return self.specific_heat * self.viscosity / self.conductivity


_TL: list[float] = _T.tolist()
_COLUMNS: list[list[float]] = [_RHO.tolist(), _CP.tolist(), _K.tolist(), _MU.tolist()]


def air(temperature: float) -> Air:
    """Air at ``temperature`` (K), which must lie within the table.

    Linear between rows, with numpy.interp's arithmetic (the same values) without its overhead:
    the firing simulation asks for air several times a step."""
    if not T_MIN <= temperature <= T_MAX:
        raise ValueError(f"air properties are tabulated from {T_MIN} K to {T_MAX} K")
    j = bisect_right(_TL, temperature) - 1
    if j >= len(_TL) - 1 or _TL[j] == temperature:
        values = [col[j] for col in _COLUMNS]
    else:
        x0, x1 = _TL[j], _TL[j + 1]
        values = [(c[j + 1] - c[j]) / (x1 - x0) * (temperature - x0) + c[j] for c in _COLUMNS]
    return Air(temperature, *values)
