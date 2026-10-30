"""Steady heat flow through a layered wall, in the manner of ASTM C680.

Layers are in series. Each layer's k(T) is integrated exactly (the Kirchhoff transform), and the
area may grow with depth, as it does through the wall of a box kiln. The outside surface
temperature is found by iteration, because the surface coefficient depends on it:

1. guess the surface temperature Ts;
2. the surface sets the heat flow: Q = A_out · h(Ts) · (Ts − T∞);
3. march inwards through each layer: ∫k dT across the layer = Q · ∫dx/A(x);
4. compare the hot-face temperature this gives with the one wanted, and adjust Ts.

The hot-face temperature rises monotonically with Ts, so a bracketing root-finder converges.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from kilndesigner.numeric import find_root, integrate
from kilndesigner.thermal.air import T_MAX as AIR_T_MAX
from kilndesigner.thermal.conductivity import Conductivity
from kilndesigner.thermal.surface import Surface

type AreaAtDepth = Callable[[float], float]


def unit_area(depth: float) -> float:
    return 1.0


@dataclass(frozen=True)
class Slab:
    name: str
    thickness: float  # m
    conductivity: Conductivity


@dataclass(frozen=True)
class WallResult:
    heat_flow: float  # W (or W/m² for a unit-area wall)
    hot_face: float  # K, the lining's inside face
    interfaces: tuple[float, ...]  # K, between layers, hot side first
    surface: float  # K, the outside face
    surface_coefficient: float  # W/(m²·K) at the solution
    outside_area: float  # m²

    @property
    def temperatures(self) -> tuple[float, ...]:
        """Every face from the hot face out: hot face, each interface, outside surface."""
        return (self.hot_face, *self.interfaces, self.surface)


def _depth_integrals(slabs: Sequence[Slab], area: AreaAtDepth) -> list[float]:
    """∫dx/A(x) across each slab (1/m)."""
    out: list[float] = []
    depth = 0.0

    def inverse_area(x: float) -> float:
        return 1.0 / area(x)

    for slab in slabs:
        out.append(integrate(inverse_area, depth, depth + slab.thickness))
        depth += slab.thickness
    return out


def solve_wall(
    slabs: Sequence[Slab],
    t_inside: float,
    t_ambient: float,
    surface: Surface,
    *,
    area: AreaAtDepth = unit_area,
    inside_coefficient: float | None = None,
) -> WallResult:
    """Steady heat flow through ``slabs`` from ``t_inside`` to still air at ``t_ambient`` (K).

    With ``inside_coefficient`` set, ``t_inside`` is the gas temperature and a film sits on the
    hot face (textbook furnace walls); without it, ``t_inside`` is the hot-face temperature.
    """
    if not slabs:
        raise ValueError("a wall needs at least one layer")
    if t_inside <= t_ambient:
        raise ValueError("the inside must be hotter than the air outside")
    total = sum(s.thickness for s in slabs)
    a_in, a_out = area(0.0), area(total)
    resistances = _depth_integrals(slabs, area)

    def march(t_surface: float) -> tuple[float, float, list[float], float]:
        h = surface.coefficient(t_surface, t_ambient)
        q = a_out * h * (t_surface - t_ambient)
        temps = [t_surface]
        for slab, r in zip(reversed(slabs), reversed(resistances), strict=True):
            temps.append(slab.conductivity.upper_temperature(temps[-1], q * r))
        temps.reverse()
        hot_face = temps[0]
        gas = hot_face + q / (a_in * inside_coefficient) if inside_coefficient else hot_face
        return gas, q, temps, h

    def mismatch(t_surface: float) -> float:
        return march(t_surface)[0] - t_inside

    # The surface film can't be hotter than the air table goes (ADR 0009: refuse, don't guess).
    hottest = min(t_inside, 2 * AIR_T_MAX - t_ambient)
    if mismatch(hottest) < 0:
        raise ValueError(
            f"the outside surface would run above {hottest - 273.15:.0f} °C, past the air "
            "properties the surface model is checked for; insulate the wall more"
        )
    _, q, temps, h = march(find_root(mismatch, t_ambient + 1e-9, hottest))
    return WallResult(
        heat_flow=q,
        hot_face=temps[0],
        interfaces=tuple(temps[1:-1]),
        surface=temps[-1],
        surface_coefficient=h,
        outside_area=a_out,
    )
