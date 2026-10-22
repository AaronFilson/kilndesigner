"""Heat loss from the kiln's outside surface to still air: natural convection plus radiation.

Correlations (electric-and-thermal.md §6.2):
- vertical plate: Churchill and Chu (1975), all Ra;
- horizontal plate, hot side up: Lloyd and Moran, Nu = 0.54 Ra^¼ (10⁴–10⁷), 0.15 Ra^⅓ (10⁷–10¹¹);
- horizontal plate, hot side down: Nu = 0.27 Ra^¼ (10⁵–10¹¹);
with air properties at the film temperature and L = A/P for horizontal plates.
Radiation to surroundings at the air temperature: h_r = εσ(Ts² + T∞²)(Ts + T∞).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol

from kilndesigner.thermal.air import air

STEFAN_BOLTZMANN = 5.670374e-8  # W/(m²·K⁴)
GRAVITY = 9.80665  # m/s²

type Orientation = Literal["vertical", "facing_up", "facing_down"]


class Surface(Protocol):
    def coefficient(self, t_surface: float, t_ambient: float) -> float:
        """The combined surface coefficient h (W/(m²·K)) at these temperatures (K)."""
        ...


@dataclass(frozen=True)
class FixedSurface:
    """A surface with a given coefficient, as in textbook examples."""

    h: float

    def coefficient(self, t_surface: float, t_ambient: float) -> float:
        return self.h


def rayleigh(t_surface: float, t_ambient: float, length: float) -> tuple[float, float]:
    """Rayleigh and Prandtl numbers for still air, properties at the film temperature."""
    film = air(0.5 * (t_surface + t_ambient))
    beta = 1.0 / film.temperature
    ra = (
        GRAVITY
        * beta
        * abs(t_surface - t_ambient)
        * length**3
        / (film.kinematic_viscosity * film.diffusivity)
    )
    return ra, film.prandtl


def nusselt(orientation: Orientation, ra: float, pr: float) -> float:
    match orientation:
        case "vertical":
            return (0.825 + 0.387 * ra ** (1 / 6) / (1 + (0.492 / pr) ** (9 / 16)) ** (8 / 27)) ** 2
        case "facing_up":
            return 0.54 * ra**0.25 if ra < 1e7 else 0.15 * ra ** (1 / 3)
        case "facing_down":
            return 0.27 * ra**0.25


def convection_coefficient(
    orientation: Orientation, length: float, t_surface: float, t_ambient: float
) -> float:
    if t_surface == t_ambient:
        return 0.0
    ra, pr = rayleigh(t_surface, t_ambient, length)
    film = air(0.5 * (t_surface + t_ambient))
    return nusselt(orientation, ra, pr) * film.conductivity / length


def radiation_coefficient(emissivity: float, t_surface: float, t_ambient: float) -> float:
    return emissivity * STEFAN_BOLTZMANN * (t_surface**2 + t_ambient**2) * (t_surface + t_ambient)


@dataclass(frozen=True)
class StillAirSurface:
    """An outside face of the kiln in still air.

    ``length`` is the height for a vertical face, or area/perimeter for a horizontal one.
    """

    orientation: Orientation
    length: float
    emissivity: float

    def coefficient(self, t_surface: float, t_ambient: float) -> float:
        return convection_coefficient(
            self.orientation, self.length, t_surface, t_ambient
        ) + radiation_coefficient(self.emissivity, t_surface, t_ambient)
