"""The frame's checks as sheets (ADR 0013): an arch's statics, HarbisonWalker's rise and ring
rules, and the steel, each written out as formulas a builder can follow, and change in the page.

Every sheet starts from the design's own numbers (span, rise, each layer's density and thickness)
and works forward, so a sheet stands on its own: the hot thrust is the same chain of formulas in
the rod's sheet as in the angle's. :mod:`kilndesigner.frame` computes the same numbers its own way,
and each sheet must agree with them (``Sheet.agrees``).
"""

from __future__ import annotations

from dataclasses import dataclass

from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_

DESIGN = "the design"
HEYMAN = "Heyman, maximum thrust: hinges at the intrados at the crown, the extrados at the skewback"


@dataclass(frozen=True)
class Layer:
    """One layer of the roof, from the inside: its name, density (lb/ft³) and thickness (in)."""

    name: str
    density: float
    thickness: float


@dataclass(frozen=True)
class ArchInputs:
    span: float  # in, inside
    rise: float  # in
    layers: tuple[Layer, ...]
    ring: int  # how many layers, from the inside, are the ring


def _arch(s: Sheet, a: ArchInputs, *, weights: bool = False) -> None:
    """S, h, each layer, the ring T, the half-angle φ and the inside radius r."""
    s.given("S", "span, inside", Q_(a.span, "in"), source=f"{DESIGN}: the chamber's width")
    s.given("h", "rise", Q_(a.rise, "in"), source=f"{DESIGN}: the roof's rise")
    for i, x in enumerate(a.layers, 1):
        s.given(f"t_{i}", f"layer {i}, {x.name}", Q_(x.thickness, "in"), source=DESIGN)
        if weights:
            s.given(
                f"ρ_{i}",
                f"{x.name}, weight per cubic foot",
                Q_(x.density, "lbf/ft**3"),
                source="the material's data sheet",
            )
    s.let(
        "T",
        "the ring: its layers' thickness",
        " + ".join(f"t_{i}" for i in range(1, a.ring + 1)),
        "in",
    )
    s.let(
        "φ",
        "half the arch's angle",
        "2*atan(2*h/S)",
        "degree",
        source="a circular segment: tan(φ/2) = 2h/S",
    )
    s.let("r", "inside radius", "S/(2*sin(φ))", "in")


CAPPED = (
    "HarbisonWalker's largest printed heated-arch factor, used where its method gives no finite "
    "hot thrust (the ring too thick for its rise): the frame's give limits it instead, as in "
    "Olsen's light bolted frames (4th ed. p.139); arch-thrust-theory.md §8"
)


def _thrust(
    s: Sheet, n: int, thick: str = "t", capped: float | None = None, cold: bool = False
) -> None:
    """The arch's weight W, its cold thrust H_c, the heated factor f and the hot thrust H, from
    its ``n`` layers' thicknesses (``t_1``…, or a dome slice's ``τ_1``…) and the cells T, φ, r.
    ``capped``: the factor to use where HarbisonWalker's method has no finite answer."""
    below: list[str] = []
    for i in range(1, n + 1):
        inner = " + ".join(["r", *below])
        s.let(
            f"w_{i}",
            f"layer {i}'s weight per foot of arch",
            f"ρ_{i}*{thick}_{i}*2*φ*({inner} + {thick}_{i}/2)",
            "lbf/ft",
            source="density × thickness × the arc at mid-layer",
        )
        below.append(f"{thick}_{i}")
    s.let(
        "W",
        "the arch's weight per foot",
        " + ".join(f"w_{i}" for i in range(1, n + 1)),
        "lbf/ft",
        source="HarbisonWalker's W, exact form; kiln-hardware.md §4.6 [S20]",
    )
    s.let(
        "H_c",
        "thrust, cold",
        "W*(sin(φ) - (1 - cos(φ))/φ)/(2*(1 - cos(φ)))",
        "lbf/ft",
        source="three-hinged circular arch: moments about a springing",
    )
    if cold:
        return
    if capped is not None:
        s.given(
            "f", "hot thrust ÷ cold thrust: the most HarbisonWalker prints", capped, source=CAPPED
        )
        s.let("H", "thrust, hot", "f*H_c", "lbf/ft", source=CAPPED)
        return
    s.let("r_o", "radius of the ring's outside", "r + T", "in")
    s.let("r_m", "radius of the ring's middle", "r + T/2", "in")
    s.let(
        "x_bar",
        "half-ring's centroid, in from the crown",
        "2/3*(r_o^3 - r^3)/(r_o^2 - r^2)*(1 - cos(φ))/φ",
        "in",
    )
    s.let(
        "f",
        "hot thrust ÷ cold thrust",
        "((r_o*sin(φ) - x_bar)/(r - r_o*cos(φ)))/((r_m*sin(φ) - x_bar)/(r_m*(1 - cos(φ))))",
        source=HEYMAN,
    )
    s.let("H", "thrust, hot, in a rigid frame", "f*H_c", "lbf/ft", source=HEYMAN)


def loose_ring(what: str, materials: list[str], source: str) -> Sheet:
    s = Sheet("frame.ring-material", f"What the {what}'s ring is made of", reference=source)
    for m in materials:
        s.fact("in the ring", m, source=DESIGN)
    s.rule(f"A {what}'s ring carries the thrust, so it must be brick or castable.", holds=False)
    return s


def rise_rule(a: ArchInputs, low: float, source: str) -> Sheet:
    """The arch's rise against Olsen's least: about 1½ in per foot of span, what a featheredge
    skewback gives; less "can result in structural difficulty". He sets no most (4th ed. p.51)."""
    s = Sheet("frame.rise", "The arch's rise for its span", reference=source)
    s.given("S", "span, inside", Q_(a.span, "in"), source=f"{DESIGN}: the chamber's width")
    s.given("h", "rise", Q_(a.rise, "in"), source=f"{DESIGN}: the roof's rise")
    s.let("d", "rise per foot of span", "h/S", "in/ft")
    s.given("d_min", "least rise for a sprung arch", Q_(low, "in/ft"), "in/ft", source=source)
    s.require("d", ">=", "d_min", level="warning")
    s.lever("h", Q_(0.1, "in"), Q_(a.span / 2, "in"))
    return s


def skewback_on_wall(a: ArchInputs, wall: float) -> Sheet:
    s = Sheet("frame.skewback", "The skewback stands on the side wall")
    _arch(s, a)
    s.given("t_w", "the thinner side wall", Q_(wall, "in"), source=f"{DESIGN}: the walls' layers")
    s.let("x_c", "the ring's outer corner, out from the centre line", "(r + T)*sin(φ)", "in")
    s.let("x_w", "the side wall's outside, out from the centre line", "S/2 + t_w", "in")
    s.require("x_c", "<=", "x_w")
    s.lever("t_w", Q_(1, "in"), Q_(60, "in"))
    return s


THRUST_THROUGH_STEEL = (
    'HarbisonWalker: "When the skewback is carried on a channel or angle, the line of thrust '
    'should pass through, or slightly above, the corner of the supporting steel"; '
    "kiln-hardware.md §4.1 [S20]"
)


def thrust_through_steel(a: ArchInputs, wall: float, leg: float, t: float) -> Sheet:
    """The line of thrust from the ring's outer corner at the skewback, carried out through the
    skewback and wall at the slope of the springing's reaction (W/2 down, H_c out), against the
    buttress angle whose corner sits at the ring's outer corner's height on the wall's outside
    (review S5). Cold thrust: the steepest line, the worst case."""
    s = Sheet("frame.thrust-steel", "The line of thrust meets the buttress angle",
              reference=THRUST_THROUGH_STEEL)  # fmt: skip
    _arch(s, a, weights=True)
    _thrust(s, len(a.layers), cold=True)
    s.given("t_w", "the thicker side wall", Q_(wall, "in"), source=f"{DESIGN}: the walls' layers")
    s.let("x_c", "the ring's outer corner, out from the centre line", "(r + T)*sin(φ)", "in")
    s.let("x_w", "the side wall's outside, out from the centre line", "S/2 + t_w", "in")
    s.let(
        "δ",
        "how far the line drops from the ring's corner to the wall's outside",
        "W/(2*H_c)*(x_w - x_c)",
        "in",
        source="the reaction at a springing: W/2 down and H_c out",
    )
    s.given("L", "the angle's upright leg", Q_(leg, "in"), source="the angle chosen")
    s.given("t_a", "the angle's thickness", Q_(t, "in"), source="the angle chosen")
    s.let("δ_max", "the upright leg below the angle's corner", "L - t_a", "in")
    s.require("δ", "<=", "δ_max", level="warning")
    s.lever("t_w", Q_(0.5, "in"), Q_(60, "in"))
    return s


def hot_thrust_line(a: ArchInputs) -> Sheet:
    s = Sheet("frame.hot-line", "The hot line of thrust stays in the ring", reference=HEYMAN)
    _arch(s, a)
    _hot_line(s)
    s.lever("h", Q_(0.1, "in"), Q_(a.span / 2, "in"))
    return s


def heated_factor_limit(a: ArchInputs, f_max: float, source: str) -> Sheet:
    s = Sheet(
        "frame.heated-factor", "Hot thrust against what HarbisonWalker prints", reference=source
    )
    _arch(s, a, weights=True)
    _thrust(s, len(a.layers))
    s.given("f_max", "the largest factor HarbisonWalker prints", f_max, source=source)
    s.require("f", "<=", "f_max", level="warning")
    _hot_line(s)
    s.lever("h", Q_(0.1, "in"), Q_(a.span / 2, "in"))
    return s


def _hot_line(s: Sheet) -> None:
    """The hot line of thrust inside the ring: past it the factor f has no meaning (its lever
    turns negative), so a sheet that solves on the rise must hold to it too."""
    s.let(
        "y_P",
        "height of the skewback's hinge, from the centre",
        "(r + T)*cos(φ)",
        "in",
        source=HEYMAN,
    )
    s.require("y_P", "<", "r")


def checked_range(
    a: ArchInputs, ts: tuple[float, float], d: tuple[float, float], source: str
) -> Sheet:
    s = Sheet(
        "frame.checked-range",
        "The arch inside the range the statics were checked over",
        reference=source,
    )
    _arch(s, a)
    s.let("TS", "ring thickness ÷ span", "T/S", "percent")
    s.let("d", "rise per foot of span", "h/S", "in/ft")
    s.given(
        "TS_min", "thinnest in the checked table", Q_(ts[0], "percent"), "percent", source=source
    )
    s.given(
        "TS_max", "thickest in the checked table", Q_(ts[1], "percent"), "percent", source=source
    )
    s.given("d_min", "flattest in the checked table", Q_(d[0], "in/ft"), "in/ft", source=source)
    s.given("d_max", "steepest in the checked table", Q_(d[1], "in/ft"), "in/ft", source=source)
    for left, op, right in (
        ("TS", ">=", "TS_min"),
        ("TS", "<=", "TS_max"),
        ("d", ">=", "d_min"),
        ("d", "<=", "d_max"),
    ):
        s.require(left, op, right, level="warning")  # pyright: ignore[reportArgumentType]
    # The rise can't bring a ring too thick for its span back into the table: its first layer can
    if s.env["TS_min"] <= s.env["TS"] <= s.env["TS_max"]:
        s.lever("h", Q_(0.1, "in"), Q_(a.span / 2, "in"))
    else:
        s.lever("t_1", Q_(0.1, "in"), Q_(a.span / 4, "in"))
    return s


@dataclass(frozen=True)
class Springs:
    rate: float  # lbf/in, each spring
    growth: float  # in per foot of span, hot
    growth_source: str
    spring_source: str


def _rod_load(s: Sheet, a: ArchInputs, bay: float, share: float, springs: Springs | None) -> None:
    """P, the busiest rod's load, hot: its share of the thrust along a bay between posts (half the
    kiln's length for each of two rods at the corner posts; a whole bay for a rod at a post
    between), or with springs the preload plus the spring's push as the arch grows, no more than
    the rigid frame's."""
    s.given(
        "L",
        "the bay: the buttress's length between posts",
        Q_(bay, "in"),
        source=f"{DESIGN}: the kiln's outside depth, and the posts along its sides",
    )
    s.given(
        "m",
        "the bays the busiest rod ties",
        share,
        source="statics: half a bay each side of a post; ½ for the corner posts alone",
    )
    if springs is None:
        s.let("P", "load on the busiest rod, hot", "H*L*m", "lbf")
        return
    s.let("P_rigid", "each rod's load, hot, in a rigid frame", "H*L*m", "lbf")
    s.let("P_c", "each spring's preload: the cold thrust", "H_c*L*m", "lbf")
    s.given("k", "each spring's rate", Q_(springs.rate, "lbf/in"), source=f"{DESIGN}: spring_rate")
    s.given(
        "g",
        "the arch's growth, hot, per foot of span",
        Q_(springs.growth, "in/ft"),
        "in/ft",
        source=springs.growth_source,
    )
    s.let("ΔS", "the span's growth, hot", "S*g", "in", source=springs.growth_source)
    s.let(
        "P",
        "load on the busiest rod, hot",
        "min(P_c + k*ΔS/2, P_rigid)",
        "lbf",
        source=springs.spring_source,
    )


def rod_stress(
    a: ArchInputs,
    bay: float,
    share: float,
    rod: str,
    area: float,
    limit: float,
    springs: Springs | None,
    sources: tuple[str, str],
    capped: float | None = None,
) -> Sheet:
    rods, stress = sources
    s = Sheet("frame.rod", f"Tie rods, {rod}, hot", reference=f"{rods}; {stress}")
    _arch(s, a, weights=True)
    _thrust(s, len(a.layers), capped=capped)
    _rod_load(s, a, bay, share, springs)
    s.given("A_s", f"{rod} rod's tensile stress area", Q_(area, "in**2"), source=rods)
    s.let("σ", "stress in each rod", "P/A_s", "psi")
    s.given("σ_allow", "allowed in steel that may run hot", Q_(limit, "psi"), source=stress)
    s.require("σ", "<=", "σ_allow")
    s.lever("A_s", Q_(0.01, "in**2"), Q_(2, "in**2"))
    return s


def buttress_bending(
    a: ArchInputs,
    bay: float,
    share: float,
    angle: str,
    sx: float,
    limit: float,
    springs: Springs | None,
    sources: tuple[str, str],
    capped: float | None = None,
) -> Sheet:
    shapes, stress = sources
    s = Sheet(
        "frame.buttress", f"Buttress angle, {angle}, in bending", reference=f"{shapes}; {stress}"
    )
    _arch(s, a, weights=True)
    _thrust(s, len(a.layers), capped=capped)
    _rod_load(s, a, bay, share, springs)
    s.let("w", "the thrust along the buttress", "P/(m*L)", "lbf/ft")
    s.let("M", "bending moment, a simple beam between the posts", "w*L^2/8", "lbf*in")
    s.given("S_x", f"{angle}'s section modulus", Q_(sx, "in**3"), source=shapes)
    s.let("σ_b", "bending stress", "M/S_x", "psi")
    s.given("σ_allow", "allowed in steel that may run hot", Q_(limit, "psi"), source=stress)
    s.require("σ_b", "<=", "σ_allow")
    s.lever("L", Q_(6, "in"), Q_(240, "in"))
    return s


# ---- A sail dome, as arches parallel to its door wall (domes-over-doors.md §D4) ----------------

DOME_SPHERE = "a sphere through the chamber's four top corners; combustion-and-masonry.md §6.7"


@dataclass(frozen=True)
class DomeInputs:
    span: float  # in: the slices' span, between the walls either side of the door
    length: float  # in: along those walls
    rise: float  # in: the dome's rise at its centre
    layers: tuple[Layer, ...]
    ring: int


def _slice(
    s: Sheet, dm: DomeInputs, at: float, *, layers: bool = True, weights: bool = False
) -> None:
    """One slice, ``at`` in from the middle: the sphere's R, the slice's inside radius r, its
    half-angle φ and, with ``layers``, each layer's thickness in the slice's plane (τ) and the
    ring's (T)."""
    s.given(
        "S",
        "the slices' span: the walls either side of the door",
        Q_(dm.span, "in"),
        source=f"{DESIGN}: the chamber and the door's wall",
    )
    s.given(
        "L",
        "the length of the walls the slices span",
        Q_(dm.length, "in"),
        source=f"{DESIGN}: the chamber",
    )
    s.given("h", "the dome's rise at its centre", Q_(dm.rise, "in"), source=f"{DESIGN}: the roof")
    s.given(
        "y",
        "this slice, in from the middle",
        Q_(at, "in"),
        source="the slice that decides the check, of 21 from the middle to the end wall",
    )
    s.let("R", "the dome's inside radius", "((S^2 + L^2)/4 + h^2)/(2*h)", "in", source=DOME_SPHERE)
    s.let("r", "the slice's inside radius", "sqrt(R^2 - y^2)", "in")
    s.let(
        "φ",
        "half the slice's angle",
        "asin(S/(2*r))",
        "degree",
        source="a circular arch of radius r over the span S",
    )
    if not layers:
        return
    outside = "R"
    for i, x in enumerate(dm.layers, 1):
        s.given(f"t_{i}", f"layer {i}, {x.name}", Q_(x.thickness, "in"), source=DESIGN)
        if weights:
            s.given(
                f"ρ_{i}",
                f"{x.name}, weight per cubic foot",
                Q_(x.density, "lbf/ft**3"),
                source="the material's data sheet",
            )
    for i in range(1, len(dm.layers) + 1):
        inner = "r" if i == 1 else f"sqrt(({outside})^2 - y^2)"
        outside = f"{outside} + t_{i}"
        s.let(
            f"τ_{i}",
            f"layer {i}, thick in the slice's plane",
            f"sqrt(({outside})^2 - y^2) - {inner}",
            "in",
            source="the shell cut by the slice's plane",
        )
    s.let(
        "T",
        "the ring, thick in the slice's plane",
        " + ".join(f"τ_{i}" for i in range(1, dm.ring + 1)),
        "in",
    )


def _dome_reach(dm: DomeInputs) -> float:
    """The highest rise to solve over: just under a hemisphere through the corners."""
    return 0.999 * (dm.span**2 + dm.length**2) ** 0.5 / 2


def dome_factor(dm: DomeInputs, at: float, eta: float, safety: float, source: str) -> Sheet:
    s = Sheet(
        "frame.dome-factor",
        "The dome's slice against the thinnest arch that stands",
        reference=source,
    )
    _slice(s, dm, at)
    s.given(
        "η",
        "the thinnest ring that stands, as t/r, at this half-angle",
        eta,
        source=f"{source}: Heyman's table by half-angle, interpolated at φ",
    )
    s.let(
        "k",
        "how many times the thinnest that stands",
        "T/(r + T/2)/η",
        source="Heyman's geometric factor of safety",
    )
    s.given("k_min", "Heyman's factor of safety", safety, source=source)
    s.require("k", ">=", "k_min")
    s.lever("t_1", Q_(0.1, "in"), Q_(24, "in"))
    return s


def dome_thickest(dm: DomeInputs, at: float, source: str) -> Sheet:
    s = Sheet("frame.dome-thickness", "The dome's slice thickness for its rise", reference=source)
    _slice(s, dm, at)
    s.let("h_s", "the slice's own rise", "r*(1 - cos(φ))", "in")
    s.let(
        "T_max",
        "thickest ring the slice's rise allows",
        "(h_s - S/48)/cos(φ)",
        "in",
        source="HarbisonWalker: the line of thrust no lower than ¼ in per foot of span",
    )
    s.require("T", "<=", "T_max")
    s.lever("h", Q_(0.5, "in"), Q_(_dome_reach(dm), "in"))
    return s


def dome_rise(dm: DomeInputs, at: float, low: float, high: float, source: str) -> Sheet:
    s = Sheet("frame.dome-rise", "The dome's slice: its rise for its span", reference=source)
    _slice(s, dm, at, layers=False)
    s.let("h_s", "the slice's own rise", "r*(1 - cos(φ))", "in")
    s.let("d", "rise per foot of span", "h_s/S", "in/ft")
    s.given(
        "d_min", "least rise for a roof arch of this ring", Q_(low, "in/ft"), "in/ft", source=source
    )
    s.given(
        "d_max", "most rise for a roof arch of this ring", Q_(high, "in/ft"), "in/ft", source=source
    )
    s.require("d", ">=", "d_min")
    s.require("d", "<=", "d_max")
    s.lever("h", Q_(0.5, "in"), Q_(_dome_reach(dm), "in"))
    return s


def dome_hot_line(dm: DomeInputs, at: float) -> Sheet:
    s = Sheet(
        "frame.dome-hot-line", "The dome's hot line of thrust stays in the slice", reference=HEYMAN
    )
    _slice(s, dm, at)
    _hot_line(s)
    s.lever("h", Q_(0.5, "in"), Q_(_dome_reach(dm), "in"))
    return s


def dome_heated(dm: DomeInputs, at: float, f_max: float, source: str) -> Sheet:
    s = Sheet(
        "frame.dome-heated-factor",
        "The dome's hot thrust against what HarbisonWalker prints",
        reference=source,
    )
    _slice(s, dm, at, weights=True)
    _thrust(s, len(dm.layers), "τ")
    s.given("f_max", "the largest factor HarbisonWalker prints", f_max, source=source)
    s.require("f", "<=", "f_max", level="warning")
    _hot_line(s)
    s.lever("h", Q_(0.5, "in"), Q_(_dome_reach(dm), "in"))
    return s


def dome_checked_range(dm: DomeInputs, at: float, ts_max: float, source: str) -> Sheet:
    s = Sheet(
        "frame.dome-checked-range",
        "The dome's slices inside the table the statics were checked against",
        reference=source,
    )
    _slice(s, dm, at)
    s.let("TS", "ring thickness ÷ span", "T/S", "percent")
    s.given(
        "TS_max", "thickest in the checked table", Q_(ts_max, "percent"), "percent", source=source
    )
    s.require("TS", "<=", "TS_max", level="warning")
    s.lever("t_1", Q_(0.1, "in"), Q_(24, "in"))
    return s


def dome_steel(dm: DomeInputs, at: float, along: float, source: str) -> Sheet:
    s = Sheet("frame.dome-steel", "What the dome's steel must hold", reference=source)
    _slice(s, dm, at, weights=True)
    _thrust(s, len(dm.layers), "τ")
    s.given(
        "F",
        "the hot thrust along each wall",
        Q_(along, "lbf"),
        source="each slice's H, summed along the wall over the 21 slices (trapezoid rule)",
    )
    s.let(
        "F_tie", "each tie: one across the door's head, one across the wall opposite", "F/2", "lbf"
    )
    s.rule(
        "No source sizes the steel for a dome: have it designed for H and F_tie.",
        holds=False,
        level="warning",
    )
    return s


# ---- A catenary's feet --------------------------------------------------------------------------


@dataclass(frozen=True)
class CatenaryLayer:
    name: str
    density: float  # lb/ft³
    thickness: float  # in
    length: float  # ft: the curve moved out to the layer's middle, foot to foot


def catenary_feet(
    span: float, height: float, a: float, layers: list[CatenaryLayer], source: str
) -> Sheet:
    s = Sheet("frame.catenary-feet", "What holds the catenary's feet", reference=source)
    s.given("S", "span at the floor, inside", Q_(span, "in"), source=f"{DESIGN}: the chamber")
    s.given("H_k", "height at the crown, inside", Q_(height, "in"), source=f"{DESIGN}: the chamber")
    s.given(
        "a", "the catenary's parameter", Q_(a, "in"), source="solved from H_k = a(cosh(S/2a) − 1)"
    )
    s.let(
        "H_a",
        "the crown's height that a gives: H_k again",
        "a*((exp(S/(2*a)) + exp(-S/(2*a)))/2 - 1)",
        "in",
        source=source,
    )
    s.let(
        "s",
        "the inside curve's length",
        "a*(exp(S/(2*a)) - exp(-S/(2*a)))",
        "ft",
        source="2a·sinh(S/2a)",
    )
    for i, x in enumerate(layers, 1):
        s.given(f"t_{i}", f"layer {i}, {x.name}", Q_(x.thickness, "in"), source=DESIGN)
        s.given(
            f"ρ_{i}",
            f"{x.name}, weight per cubic foot",
            Q_(x.density, "lbf/ft**3"),
            source="the material's data sheet",
        )
        s.given(
            f"ℓ_{i}",
            f"layer {i}'s length at its middle",
            Q_(x.length, "ft"),
            source="the curve moved out to mid-layer, measured foot to foot",
        )
    total = " + ".join(f"ρ_{i}*t_{i}*ℓ_{i}" for i in range(1, len(layers) + 1))
    s.let(
        "w",
        "the arch's weight per foot of curve, per foot of kiln",
        f"({total})/s",
        "lbf/ft**2",
        source=source,
    )
    s.let(
        "H",
        "each foot's push, per foot of kiln",
        "w*a",
        "lbf/ft",
        source="the hanging chain's horizontal tension, turned to thrust",
    )
    s.let("V", "the weight on each foot, per foot of kiln", "w*s/2", "lbf/ft")
    s.rule(
        "No source sizes what holds a catenary's feet (a curb, ties or buttresses): have it "
        "designed for H.",
        holds=False,
        level="warning",
    )
    return s


# ---- A flat roof as a jack arch (flat-roofs.md §2, §4) ------------------------------------------


def _flat(s: Sheet, span: float, layers: tuple[Layer, ...], *, weights: bool) -> None:
    s.given(
        "S",
        "the roof's span between the walls either side of the door",
        Q_(span, "in"),
        source=f"{DESIGN}: the chamber and the door's wall",
    )
    for i, x in enumerate(layers, 1):
        s.given(f"t_{i}", f"layer {i}, {x.name}", Q_(x.thickness, "in"), source=DESIGN)
        if weights:
            s.given(
                f"ρ_{i}",
                f"{x.name}, weight per cubic foot",
                Q_(x.density, "lbf/ft**3"),
                source="the material's data sheet",
            )
    if weights:
        s.let(
            "q",
            "the roof's weight per square foot, every layer",
            " + ".join(f"ρ_{i}*t_{i}" for i in range(1, len(layers) + 1)),
            "lbf/ft**2",
        )
        s.let(
            "H",
            "the squeeze the roof needs, per foot of roof, cold",
            "3*q*S^2/(8*t_1)",
            "lbf/ft",
            source="BIA's jack arch, H = 3WS/8d with W = q·S and d = t_1: the thrust line in the "
            "middle third",
        )


def flat_friction(span: float, layers: tuple[Layer, ...], mu: float, source: str) -> Sheet:
    s = Sheet(
        "frame.flat-friction", "The flat roof holds at its ends by friction", reference=source
    )
    _flat(s, span, layers, weights=False)
    s.let("μ_need", "the friction its ends need: 4d ÷ 3S, d = t_1", "4*t_1/(3*S)", source=source)
    s.given(
        "μ",
        "friction between brick masonry units",
        mu,
        source=f"{source} (none is sourced for insulating firebrick)",
    )
    s.require("μ_need", "<=", "μ")
    s.lever("t_1", Q_(0.5, "in"), Q_(24, "in"))
    return s


def flat_span(span: float, checked: float, longest: float) -> Sheet:
    s = Sheet(
        "frame.flat-span",
        "The flat roof's span against the sourced flat roofs",
        reference="flat-roofs.md §4.1, §4.3, §4.5",
    )
    s.given(
        "S",
        "the roof's span between the walls either side of the door",
        Q_(span, "in"),
        source=f"{DESIGN}: the chamber and the door's wall",
    )
    s.given(
        "S_checked",
        "the longest one-way flat roof in the sources: Merrill's",
        Q_(checked, "in"),
        source="flat-roofs.md §4.3 [F9]",
    )
    s.given(
        "S_longest",
        "about the longest flat brick roof, on four walls",
        Q_(longest, "in"),
        source="L&L's lids and Nils Lou's roof; flat-roofs.md §4.1, §4.3 (derived)",
    )
    s.require("S", "<=", "S_longest")
    s.require("S", "<=", "S_checked", level="warning")
    s.lever("S", Q_(6, "in"), Q_(120, "in"))
    return s


def flat_ifb_top(material: str, top_f: float, limit_f: float, source: str) -> Sheet:
    s = Sheet(
        "frame.flat-ifb-top", "A flat insulating-firebrick roof's top temperature", reference=source
    )
    s.fact("the roof's slab", material, source=DESIGN)
    s.given(
        "T_top",
        "the firing's top temperature",
        Q_(top_f, "degF"),
        source=f"{DESIGN}: the firing (its cone, or top_temperature)",
    )
    s.given("T_max", "the hottest BNZ keeps a flat IFB roof to", Q_(limit_f, "degF"), source=source)
    s.require("T_top", "<=", "T_max", level="warning")
    return s


def flat_rods(
    span: float,
    layers: tuple[Layer, ...],
    row: float,
    rod: tuple[str, float],
    limit: float,
    sources: tuple[str, str, str],
) -> Sheet:
    name, area = rod
    roof, rods, stress = sources
    s = Sheet("frame.flat-rod", f"Rods across the flat roof, {name}", reference=f"{rods}; {stress}")
    _flat(s, span, layers, weights=True)
    s.given("b", "the roof each rod squeezes: one row of brick", Q_(row, "in"), source=rods)
    s.let("P", "load on each rod, cold", "H*b", "lbf", source=roof)
    s.given("A_s", f"{name} rod's tensile stress area", Q_(area, "in**2"), source=stress)
    s.let("σ", "stress in each rod", "P/A_s", "psi")
    s.given("σ_allow", "allowed in steel that may run hot", Q_(limit, "psi"), source=stress)
    s.require("σ", "<=", "σ_allow")
    s.lever("A_s", Q_(0.01, "in**2"), Q_(2, "in**2"))
    return s


__all__ = [
    "ArchInputs",
    "CatenaryLayer",
    "DomeInputs",
    "Layer",
    "Springs",
    "buttress_bending",
    "catenary_feet",
    "checked_range",
    "dome_checked_range",
    "dome_factor",
    "dome_heated",
    "dome_hot_line",
    "dome_rise",
    "dome_steel",
    "dome_thickest",
    "flat_friction",
    "flat_ifb_top",
    "flat_rods",
    "flat_span",
    "heated_factor_limit",
    "hot_thrust_line",
    "loose_ring",
    "rise_rule",
    "rod_stress",
    "skewback_on_wall",
    "thrust_through_steel",
]
