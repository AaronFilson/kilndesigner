"""The castables' checks as sheets (ADR 0013): the dry-out schedule's reach, the heat the organics
give off as they burn out, a mix with no service limit, and castable cast in layers.

:mod:`kilndesigner.castable` decides its findings from these.
"""

from __future__ import annotations

from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_


def dryout_reach(thickest_in: float, max_in: float, source: str) -> Sheet:
    title = "The dry-out schedule against the thickest castable"
    s = Sheet("castable.dryout", title, reference=source)
    s.given(
        "t",
        "the thickest castable layer in the lining",
        Q_(thickest_in, "in"),
        source="the design: its castable layers",
    )
    s.given(
        "t_max", "the thickest layer the sourced schedule covers", Q_(max_in, "in"), source=source
    )
    s.require("t", "<=", "t_max")
    s.lever("t", Q_(0.5, "in"), Q_(2 * max_in, "in"))
    return s


def burnout_heat(
    name: str,
    heat_per_batch_j: float,
    placed_m3: float,
    batch_m3: float,
    window_c: tuple[float, float],
    ramp_f_per_h: float,
    kiln_w: float,
    sources: tuple[str, str, str],
) -> Sheet:
    """The organics' heat spread over the climb through their burnout window, against the
    kiln's own heat."""
    heat_source, window_source, ramp_source = sources
    s = Sheet(
        "castable.burnout", f"{name}: the organics' heat as they burn out", reference=heat_source
    )
    s.given(
        "Q_b",
        "the organics' heat in one batch",
        Q_(heat_per_batch_j, "J"),
        unit="kWh",
        source=f"{heat_source}: each organic's mass × its heat of combustion",
    )
    s.given(
        "V",
        "castable placed in the lining",
        Q_(placed_m3, "m**3"),
        unit="ft**3",
        source="the lining's castable layers",
    )
    s.given(
        "V_b",
        "what one batch casts",
        Q_(batch_m3, "m**3"),
        unit="ft**3",
        source="the mix: its ingredients' volumes",
    )
    s.let("n", "batches in the lining", "V/V_b")
    s.let("Q", "heat the organics give off", "Q_b*n", "kWh")
    s.given(
        "T_lo",
        "the organics start to burn",
        Q_(window_c[0], "degC"),
        unit="degF",
        source=window_source,
    )
    s.given(
        "T_hi", "the organics are gone", Q_(window_c[1], "degC"), unit="degF", source=window_source
    )
    s.given("r", "the schedule's climb", Q_(ramp_f_per_h, "delta_degF/hour"), source=ramp_source)
    s.let("t_w", "time to climb through the window", "(T_hi - T_lo)/r", "hour")
    s.let("P_b", "the organics' heat, spread over that time", "Q/t_w", "kW")
    s.given(
        "P_k",
        "the kiln's own heat: its elements, or else its burners",
        Q_(kiln_w, "W"),
        unit="kW",
        source="the elements' installed power, or the burners' input",
    )
    s.require("P_b", "<=", "P_k", level="warning")
    s.lever("r", Q_(1, "delta_degF/hour"), Q_(1000, "delta_degF/hour"))
    return s


def no_service_limit(name: str, ingredients: list[str], top_f: float, source: str) -> Sheet:
    s = Sheet("castable.service-limit", f"{name}: how hot it may run", reference=source)
    for i in ingredients:
        s.fact("ingredient, no service limit sourced", i, source="castables.md, ingredients.yaml")
    s.given(
        "T_top",
        "the kiln's top temperature",
        Q_(top_f, "degF"),
        source="the design's cone or top temperature",
    )
    s.rule(
        "A castable needs a sourced service limit above the kiln's top temperature before it "
        "can be trusted at the hot face; none of this mix's ingredients has one.",
        holds=False,
        level="warning",
    )
    return s


def cast_in_layers(face: str, layers_in: list[float], schedule_in: float, source: str) -> Sheet:
    s = Sheet("castable.layers", f"Castable cast in layers in the {face} wall", reference=source)
    for i, t in enumerate(layers_in, 1):
        s.given(f"t_{i}", f"castable layer {i}", Q_(t, "in"), source="the design: the lining")
    s.let(
        "t_all",
        "castable in the wall, all its layers",
        " + ".join(f"t_{i}" for i in range(1, len(layers_in) + 1)),
        "in",
    )
    s.given(
        "t_s",
        "the thickest single layer, which sets the schedule",
        Q_(schedule_in, "in"),
        source=source,
    )
    s.rule(
        "The schedule is set by the thickest single layer, as HarbisonWalker does; no maker "
        "gives holds for layers cast wet together, so each must dry before the next is cast.",
        holds=False,
        level="warning",
    )
    return s


__all__ = ["burnout_heat", "cast_in_layers", "dryout_reach", "no_service_limit"]
