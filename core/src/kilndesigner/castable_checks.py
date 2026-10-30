"""The castables' checks as sheets (ADR 0013): the dry-out schedule's reach, the heat the organics
give off as they burn out, a mix with no service limit, and castable cast in layers.

:mod:`kilndesigner.castable` decides its findings from these.
"""

from __future__ import annotations

from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_, Quantity


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
    mixes: list[tuple[str, float, float, float]],
    window_c: tuple[float, float],
    ramp_f_per_h: float,
    need_w: float,
    installed_w: float | None,
    sources: tuple[str, str, str],
) -> Sheet:
    """Every mix's organics, where they get hot enough to burn, spread over the climb through
    the burnout window, against the heat the kiln needs to hold that climb.

    ``mixes`` is (name, heat per batch J, volume that reaches the window m³, batch volume m³).
    ``need_w`` is the kiln's steady loss with the inside at the window's top; the heat stored in
    the lining while it climbs is left out, so the check errs towards a runaway warning.
    """
    heat_source, window_source, ramp_source = sources
    s = Sheet("castable.burnout", "The organics' heat as they burn out", reference=heat_source)
    terms: list[str] = []
    for i, (name, heat_per_batch_j, placed_m3, batch_m3) in enumerate(mixes, 1):
        s.given(
            f"Q_b{i}",
            f"{name}: the organics' heat in one batch",
            Q_(heat_per_batch_j, "J"),
            unit="kWh",
            source=f"{heat_source}: each organic's mass × its heat of combustion",
        )
        s.given(
            f"V_{i}",
            f"{name}: castable that gets above the window's start",
            Q_(placed_m3, "m**3"),
            unit="ft**3",
            source="the lining's castable layers, the part of each above T_lo",
        )
        s.given(
            f"V_b{i}",
            f"{name}: what one batch casts",
            Q_(batch_m3, "m**3"),
            unit="ft**3",
            source="the mix: its ingredients' volumes",
        )
        terms.append(f"Q_b{i}*V_{i}/V_b{i}")
    s.let("Q", "heat the organics give off, every mix", " + ".join(terms), "kWh")
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
        "the heat the kiln needs at the window's top: its steady loss there",
        Q_(need_w, "W"),
        unit="kW",
        source="the heat-loss solve with the inside at T_hi (conduction; the lining's stored "
        "heat left out, which errs towards a warning)",
    )
    if installed_w is not None:
        s.fact(
            "the kiln's installed heat (elements, or else burners)",
            f"{installed_w / 1000:.3g} kW",
            source="the design",
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


def no_shrinkage(name: str) -> Sheet:
    """A mix with no measured firing shrinkage or fired density: both are estimated with none,
    so density and conductivity come out as lower bounds (review M3)."""
    s = Sheet(
        "castable.shrinkage", f"{name}: firing shrinkage", reference="castables.md §11a (derived)"
    )
    s.fact("linear shrinkage on firing", "not measured; taken as 0 %", source="the design")
    s.rule(
        "Firing shrinkage makes a mix denser and more conductive (5 % linear shrinkage is about "
        "16 % denser); with none measured, the fired density and k are lower bounds, the unsafe "
        "side for heat loss. Measure test pieces.",
        holds=False,
        level="warning",
    )
    return s


def fired_too_cool(name: str, fired_to: Quantity, top: Quantity) -> Sheet:
    """Test pieces fired below the kiln's top temperature don't show its full shrinkage (M10)."""
    s = Sheet(
        "castable.test-firing", f"{name}: the test pieces' firing", reference="the design"
    )
    s.given("T_test", "the test pieces' firing", fired_to, "degF", source="the design: measured")
    s.given("T_top", "the kiln's top temperature", top, "degF", source="the design: the firing")
    s.require("T_test", ">=", "T_top", level="warning")
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
        "the thickest single layer",
        Q_(schedule_in, "in"),
        source=source,
    )
    s.rule(
        "The only sourced dry-out schedule covers a single layer of 9 in or less; HarbisonWalker "
        "evaluates a lining of several components case by case, so none is given for layers "
        "cast together (refused, ADR 0009).",
        holds=False,
        level="warning",
    )
    return s


__all__ = [
    "burnout_heat",
    "cast_in_layers",
    "dryout_reach",
    "fired_too_cool",
    "no_service_limit",
    "no_shrinkage",
]
