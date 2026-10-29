"""The heat-loss checks as sheets (ADR 0013): a material against its service limit, and the
outside air's Rayleigh number against the range its convection correlation was checked over.

The wall's temperatures come from an iterated solve (:mod:`kilndesigner.thermal.wall`), so they
enter as inputs naming the working step; editing one recomputes what follows from it, not the
wall.
"""

from __future__ import annotations

from kilndesigner.sheet import Sheet
from kilndesigner.thermal.air import Air
from kilndesigner.thermal.surface import GRAVITY, RA_SOURCE
from kilndesigner.units import Q_, Quantity

AIR_SOURCE = (
    "Holman Table A-5 at the film temperature, interpolated: a table (thermal/air.py; "
    "electric-and-thermal.md §6.3 [S63])"
)


def service_temperature(
    face: str,
    material: str,
    layer: int,
    hot: Quantity,
    limit: Quantity,
    source: str,
    temp_unit: str,
) -> Sheet:
    """A layer's hot side against the most its maker allows. ``layer`` counts from 0 inside: the
    first layer's hot side is the kiln's own top temperature, the builder's to choose."""
    s = Sheet(
        f"heatloss.service.{face}.{layer + 1}",
        f"{face}: {material} against its rating",
        reference=source,
    )
    where = (
        "the kiln's top temperature: this layer is the hot face"
        if layer == 0
        else f"working: Heat loss, {face} (the wall solve, iterated): layer {layer + 1}'s hot side"
    )
    s.given("T_hot", f"{material}'s hot side", hot, temp_unit, source=where)
    s.given("T_max", f"{material}'s service limit", limit, temp_unit, source=source)
    # Past its class a brick shrinks and wears faster, but stands: Olsen's cone 10 fast-fire kiln
    # is 2300 °F brick (4th ed. p.140), so a warning
    s.require("T_hot", "<=", "T_max", level="warning")
    if layer == 0:
        s.lever("T_hot", Q_(200, "degC"), Q_(2000, "degC"))
    return s


def rayleigh_range(
    face: str,
    surface: float,
    ambient: float,
    length: float,
    film: Air,
    checked: tuple[float, float],
    temp_unit: str,
    length_unit: str,
) -> Sheet:
    """Ra = g·β·ΔT·L³ / (ν·α), with air at the film temperature, against the range the face's
    convection correlation was checked over (thermal-properties.md §5)."""
    s = Sheet(
        f"heatloss.rayleigh.{face}",
        f"{face}: the outside air's Rayleigh number",
        reference=RA_SOURCE,
    )
    s.given(
        "T_s",
        f"{face}'s outside surface",
        Q_(surface, "K"),
        temp_unit,
        source=f"working: Heat loss, {face} (the wall solve, iterated)",
    )
    s.given("T_a", "air around the kiln", Q_(ambient, "K"), temp_unit, source="the design: site")
    s.given(
        "L",
        "the face's length for convection: its height, or area ÷ perimeter if flat",
        Q_(length, "m"),
        length_unit,
        source="the chamber's shape and the lining's thickness",
    )
    s.given("g", "gravity", Q_(GRAVITY, "m/s**2"), source="standard gravity")
    s.let("T_f", "film temperature", "(T_s + T_a)/2", temp_unit)
    s.given("ρ", "air's density at T_f", Q_(film.density, "kg/m**3"), source=AIR_SOURCE)
    s.given("μ", "air's viscosity at T_f", Q_(film.viscosity, "Pa*s"), source=AIR_SOURCE)
    s.given("k_a", "air's conductivity at T_f", Q_(film.conductivity, "W/(m*K)"), source=AIR_SOURCE)
    s.given(
        "c_p", "air's specific heat at T_f", Q_(film.specific_heat, "J/(kg*K)"), source=AIR_SOURCE
    )
    s.let("β", "air's expansion coefficient, an ideal gas", "1/T_f", "1/K")
    s.let("ν", "kinematic viscosity", "μ/ρ", "m**2/s")
    s.let("α", "thermal diffusivity", "k_a/(ρ*c_p)", "m**2/s")
    s.let("Ra", "Rayleigh number", "g*β*abs(T_s - T_a)*L^3/(ν*α)", source=RA_SOURCE)
    lo, hi = checked
    s.given("Ra_min", "lowest Ra the correlation was checked at", lo, source=RA_SOURCE)
    s.given("Ra_max", "highest Ra the correlation was checked at", hi, source=RA_SOURCE)
    s.require("Ra", ">=", "Ra_min", level="warning")
    s.require("Ra", "<=", "Ra_max", level="warning")
    s.lever("L", Q_(0.01, "m"), Q_(10, "m"))
    return s


__all__ = ["rayleigh_range", "service_temperature"]
