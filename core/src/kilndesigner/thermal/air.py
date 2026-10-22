"""Properties of air at 1 atm, from the Neutrium table (electric-and-thermal.md §6.3, [S63]).

Linear interpolation between the table's rows, 250 K to 1000 K. The table matches the values
commonly quoted from Incropera Table A.4.
"""

from __future__ import annotations

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


def air(temperature: float) -> Air:
    """Air at ``temperature`` (K), which must lie within the table."""
    if not T_MIN <= temperature <= T_MAX:
        raise ValueError(f"air properties are tabulated from {T_MIN} K to {T_MAX} K")
    return Air(
        temperature,
        float(np.interp(temperature, _T, _RHO)),
        float(np.interp(temperature, _T, _CP)),
        float(np.interp(temperature, _T, _K)),
        float(np.interp(temperature, _T, _MU)),
    )
