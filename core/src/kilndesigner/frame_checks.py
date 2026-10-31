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


@dataclass(frozen=True)
class HotSteel:
    """The frame steel's temperature and AISC 360-16 Table A-4.2.1's factors at it, with the
    steel's room-temperature properties (steel-design.md §S2–S3)."""

    temperature: float  # °F, the bearing wall's outside face, steady at the top temperature
    ky: float  # Fy(T)/Fy, interpolated in the table
    ke: float  # E(T)/E, interpolated in the table
    fy: float  # psi, room temperature
    e: float  # psi, room temperature
    omega: float  # ASD safety factor for bending
    source: str  # AISC 360-16 §F1, §F10, App. 4
    where: str  # how the temperature was found


@dataclass(frozen=True)
class AngleSection:
    name: str
    leg: float  # in
    t: float  # in
    sx: float  # in³, geometric axis
    source: str


def _aisc_angle_moment(s: Sheet, a: AngleSection, hot: HotSteel) -> None:
    """AISC 360-16 §F10, an equal-leg angle bent about a geometric axis with no lateral-torsional
    restraint along its bay (L_b, a cell above), toe in compression, Cb = 1: the allowable
    moment M_a = M_n/Ω_b, with Fy and E reduced to the steel's temperature (Appendix 4)."""
    s.given("b", f"{a.name}'s leg", Q_(a.leg, "in"), source=a.source)
    s.given("t_a", f"{a.name}'s thickness", Q_(a.t, "in"), source=a.source)
    s.given(
        "S_x", f"{a.name}'s section modulus, geometric axis", Q_(a.sx, "in**3"), source=a.source
    )
    s.given("T_s", "the steel's temperature", Q_(hot.temperature, "degF"), "degF", source=hot.where)
    s.given("F_y0", "A36 yield stress, cold", Q_(hot.fy, "psi"), source=hot.source)
    s.given("E_0", "steel's modulus, cold", Q_(hot.e, "psi"), source=hot.source)
    s.given("k_y", "Fy(T)/Fy at T_s", hot.ky, source=f"{hot.source}: Table A-4.2.1, interpolated")
    s.given("k_E", "E(T)/E at T_s", hot.ke, source=f"{hot.source}: Table A-4.2.1, interpolated")
    s.let("F_y", "yield stress, hot", "k_y*F_y0", "psi")
    s.let("E", "modulus, hot", "k_E*E_0", "psi")
    s.let("M_y", "yield moment: 0.80 × the geometric one (F10)", "0.8*F_y*S_x", "lbf*in")
    s.let(
        "M_cr",
        "elastic lateral-torsional buckling moment, toe in compression (F10-5a)",
        "0.58*E*b^4*t_a/L_b^2*(sqrt(1 + 0.88*(L_b*t_a/b^2)^2) - 1)",
        "lbf*in",
        source=hot.source,
    )
    ratio = s.env["M_y"] / s.env["M_cr"]
    if ratio <= 1:
        s.let(
            "M_ltb",
            "lateral-torsional buckling strength (F10-2)",
            "min((1.92 - 1.17*sqrt(M_y/M_cr))*M_y, 1.5*M_y)",
            "lbf*in",
            source=hot.source,
        )
    else:
        s.let(
            "M_ltb",
            "lateral-torsional buckling strength (F10-3)",
            "(0.92 - 0.17*M_cr/M_y)*M_cr",
            "lbf*in",
            source=hot.source,
        )
    s.let("λ", "leg slenderness", "b/t_a")
    s.let("λ_p", "compact limit (Table B4.1b, case 12)", "0.54*sqrt(E/F_y)")
    s.let("λ_r", "noncompact limit", "0.91*sqrt(E/F_y)")
    s.let("S_c", "section modulus to the toe: 0.80 S_x (F10)", "0.8*S_x", "in**3")
    lam, lp, lr = s.env["λ"], s.env["λ_p"], s.env["λ_r"]
    if lam <= lp:
        s.let("M_lb", "leg local buckling: a compact leg, none (yielding governs)", "1.5*M_y",
              "lbf*in", source=hot.source)  # fmt: skip
    elif lam <= lr:
        s.let("M_lb", "leg local buckling, noncompact leg (F10-6)",
              "F_y*S_c*(2.43 - 1.72*λ*sqrt(F_y/E))", "lbf*in", source=hot.source)  # fmt: skip
    else:
        s.let("M_lb", "leg local buckling, slender leg (F10-7, F10-8)", "0.71*E/λ^2*S_c",
              "lbf*in", source=hot.source)  # fmt: skip
    s.let("M_n", "nominal moment: the least of F10-1, LTB and leg buckling",
          "min(1.5*M_y, M_ltb, M_lb)", "lbf*in", source=hot.source)  # fmt: skip
    s.given("Ω_b", "ASD safety factor for bending (F1)", hot.omega, source=hot.source)
    s.let("M_a", "allowable moment, hot", "M_n/Ω_b", "lbf*in", source=hot.source)


def dome_buttress(
    dm: DomeInputs,
    at: float,
    bay: float,
    a: AngleSection,
    hot: HotSteel,
    limit: float,
    stress_source: str,
) -> Sheet:
    """The angle along the top of each wall the dome's slices bear on, bending between posts
    under the most thrust any slice gives, hot: AISC 360-16 F10 with the steel's properties at
    its temperature, and HarbisonWalker's 12,000 psi for bindings that may run hot."""
    s = Sheet(
        "frame.dome-buttress",
        f"Buttress angle along the dome's bearing walls, {a.name}, hot",
        reference=f"{hot.source}; {stress_source}; steel-design.md §S4",
    )
    _slice(s, dm, at, weights=True)
    _thrust(s, len(dm.layers), "τ")
    s.given(
        "ℓ",
        "the bay: the buttress between posts",
        Q_(bay, "in"),
        source=f"{DESIGN}: the bearing wall's outside length, and the posts along it",
    )
    s.let(
        "M",
        "bending moment, a simple beam between posts, the peak thrust all along",
        "H*ℓ^2/8",
        "lbf*in",
        source="statics; the slices' peak thrust taken over the whole bay (cautious)",
    )
    # F10's Lb is the bay
    s.let("L_b", "unbraced length, AISC L_b", "ℓ", "in")
    _aisc_angle_moment(s, a, hot)
    s.require("M", "<=", "M_a")
    s.let("σ_b", "bending stress", "M/S_x", "psi")
    s.given("σ_allow", "allowed in steel that may run hot", Q_(limit, "psi"), source=stress_source)
    s.require("σ_b", "<=", "σ_allow")
    s.lever("S_x", Q_(0.05, "in**3"), Q_(10, "in**3"))
    return s


def dome_rod(
    dm: DomeInputs,
    at: float,
    bay: float,
    share: float,
    rod: tuple[str, float],
    limit: float,
    sources: tuple[str, str],
) -> Sheet:
    name, area = rod
    rods, stress = sources
    s = Sheet(
        "frame.dome-rod",
        f"Ties across the dome's bearing walls, {name} rod, hot",
        reference=f"{rods}; {stress}; domes-over-doors.md §D4.1 step 4",
    )
    _slice(s, dm, at, weights=True)
    _thrust(s, len(dm.layers), "τ")
    s.given("ℓ", "the bay between posts", Q_(bay, "in"), source=DESIGN)
    s.given(
        "m",
        "the bays the busiest rod ties",
        share,
        source="statics: ½ for the corner posts alone (the door's head and the back)",
    )
    s.let("P", "load on the busiest rod, hot", "H*ℓ*m", "lbf")
    s.given("A_s", f"{name} rod's tensile stress area", Q_(area, "in**2"), source=rods)
    s.let("σ", "stress in each rod", "P/A_s", "psi")
    s.given("σ_allow", "allowed in steel that may run hot", Q_(limit, "psi"), source=stress)
    s.require("σ", "<=", "σ_allow")
    s.lever("A_s", Q_(0.01, "in**2"), Q_(2, "in**2"))
    return s


@dataclass(frozen=True)
class LintelInputs:
    """A steel lintel over a door in part of a wall (steel-design.md §S5): the opening, the wall's
    layers over it, and the roof's edge load on it."""

    clear: float  # in, the opening's width
    bearing: float  # in, at each end
    above: float  # in, the wall over the opening, at its highest
    layers: tuple[Layer, ...]  # the wall's
    edge: float  # lb/ft, the roof's vertical load on the wall over the opening
    edge_source: str
    longest: float  # in, the longest span checked
    longest_source: str


BIA_LINTEL = "BIA Technical Note 31B (1987); door-headers.md §D1 [H1]"
LINTEL_BEARING = "TMS 402-16 §5.2.1.3, at least 4 in; door-headers.md §D1.5 [H6]"


def door_lintel(
    li: LintelInputs, a: AngleSection, ix: float, hot: HotSteel, limit: float, stress_source: str
) -> Sheet:
    """A steel angle over a door in part of a wall, carrying everything above the opening with no
    arching (BIA TN 31B) and the roof's edge on it, checked hot by AISC 360-16 F10 as the dome's
    buttress is; its deflection by BIA's L/600 and 0.3 in, × 1.56 for an angle free to twist (AISC
    Commentary F10). The bearing of its ends on refractory brick is not checked: no allowable
    stress is found (door-openings.md)."""
    s = Sheet(
        "frame.door-lintel",
        f"Steel lintel over the door, {a.name}, hot",
        reference=f"{BIA_LINTEL}; {hot.source}; steel-design.md §S5",
    )
    s.given("L_c", "the opening's width", Q_(li.clear, "in"), source=f"{DESIGN}: the door")
    s.given("L_max", "the widest opening a steel angle lintel spans", Q_(li.longest, "in"),
            source=li.longest_source)  # fmt: skip
    s.require("L_c", "<=", "L_max")
    s.given("b_e", "bearing at each end", Q_(li.bearing, "in"), source=LINTEL_BEARING)
    s.let("L", "span, centre to centre of the bearings", "L_c + b_e", "in", source=BIA_LINTEL)
    s.given("h_a", "the wall over the opening, at its highest", Q_(li.above, "in"),
            source=f"{DESIGN}: the wall's inside top less the door's top")  # fmt: skip
    for i, x in enumerate(li.layers, 1):
        s.given(f"t_{i}", f"layer {i}, {x.name}", Q_(x.thickness, "in"), source=DESIGN)
        s.given(f"ρ_{i}", f"{x.name}, weight per cubic foot", Q_(x.density, "lbf/ft**3"),
                source="the material's data sheet")  # fmt: skip
    total = " + ".join(f"ρ_{i}*t_{i}" for i in range(1, len(li.layers) + 1))
    s.let("w_m", "the wall over the opening, all of it, per foot", f"({total})*h_a", "lbf/ft",
          source=f"{BIA_LINTEL}: with no arching, the full weight above the opening")  # fmt: skip
    s.given("V", "the roof's edge load on the wall over the opening", Q_(li.edge, "lbf/ft"),
            source=li.edge_source)  # fmt: skip
    s.let("w", "load on the lintel", "w_m + V", "lbf/ft")
    s.let("M", "bending moment, a simple beam", "w*L^2/8", "lbf*in", source=BIA_LINTEL)
    s.let("L_b", "unbraced length, AISC L_b: the span", "L", "in")
    _aisc_angle_moment(s, a, hot)
    s.require("M", "<=", "M_a")
    s.let("σ_b", "bending stress", "M/S_x", "psi")
    s.given("σ_allow", "allowed in steel that may run hot", Q_(limit, "psi"), source=stress_source)
    s.require("σ_b", "<=", "σ_allow")
    s.given("I_x", f"{a.name}'s moment of inertia, geometric axis", Q_(ix, "in**4"),
            source=a.source)  # fmt: skip
    s.let("Δ", "deflection, hot, the angle free to twist", "1.56*5*w*L^4/(384*E*I_x)", "in",
          source=f"{BIA_LINTEL}: 5wL⁴/384EI; AISC 360-16 Commentary F10, × 1.56")  # fmt: skip
    s.let("Δ_600", "BIA's limit: the clear span over 600", "L_c/600", "in", source=BIA_LINTEL)
    s.given("Δ_max", "BIA's limit, at most", Q_(0.3, "in"), source=BIA_LINTEL)
    s.require("Δ", "<=", "Δ_600")
    s.require("Δ", "<=", "Δ_max")
    s.let("R", "each end's reaction on the brick", "w*L/2", "lbf",
          source="statics; its bearing stress is not checked: no allowable stress for refractory "
          "brick is found (door-openings.md)")  # fmt: skip
    s.lever("S_x", Q_(0.05, "in**3"), Q_(10, "in**3"))
    return s


# ---- An arched door head and its jambs (Heyman; door.py) ---------------------------------------


@dataclass(frozen=True)
class DoorArchInputs:
    """A semicircular ring arch over a door in part of a wall, on brick jambs."""

    span: float  # in, the door's width
    ring: float  # in, the ring's depth, radially
    layers: tuple[Layer, ...]  # the wall's, through its thickness
    above: float  # in, the wall over the springline at the door's crown
    edge: float  # lb/ft, the roof's vertical load on the wall over the door
    edge_source: str
    ring_source: str
    springing: float  # in, the springline over the jambs' base
    jamb: float  # in, the narrower jamb, along the wall, to the next opening or the wall's end
    jamb_source: str
    least: float  # lbf, the minimum thrust: a line of thrust from the crown's top
    most: float  # lbf, the maximum thrust: a line of thrust from the crown's soffit
    cross: float = 0.0  # in, the cross wall bonded into the jamb's far end (0: none, a door)
    cross_q: float = 0.0  # psi, that wall's weight per square inch of its face
    # in, the wall counted over the springline on the jamb, where it isn't Z (a head in a vault's
    # edge, whose jamb's wall drops under the springline along it: 0)
    over_jamb: float | None = None


ARCH_STATICS = (
    "Heyman's safe theorem: masonry stands if a line of thrust in equilibrium with its loads lies "
    "within it, the line found need not be the actual one; domes-over-doors.md §D3, "
    "arch-thrust-theory.md §2"
)
MINIMUM_THRUST = (
    "the minimum thrust, the line of thrust from the crown's extrados touching the intrados: 'an "
    "arch on spreading supports will act in a state of minimum thrust' (Heyman, The Stone "
    "Skeleton; arch-thrust-theory.md §2 [A1], [A3]), the least it pushes on its neighbours "
    "(domes-over-doors.md §D3 [D7])"
)
NO_TENSION = (
    "the resultant in the base's middle third: no tension at the joint (domes-over-doors.md §D3 "
    "[D7]; door-headers.md §D3.2, BIA TN 31A); a statics criterion, not an allowable stress"
)


BONDED = (
    "a design rule, not a sourced one (door-headers.md §D9): 'resistance to horizontal thrust ... "
    "is provided by the adjacent mass of masonry' (BIA TN 31A §D3.5), and a cross wall bonded "
    "into the jamb's end is part of it; only a length of it equal to the jamb wall's thickness "
    "is counted, its weight at the cross wall's middle, so the rest of the return is spare"
)


def _door_arch(s: Sheet, da: DoorArchInputs, *, loads: bool = True) -> None:
    """The arch's size, and with ``loads`` the wall's weight on half of it, its least thrust H and
    where the line of thrust crosses the springing, x_p in from the door's edge."""
    s.given("S", "the door's width", Q_(da.span, "in"), source=f"{DESIGN}: the door")
    s.given("d", "the ring's depth", Q_(da.ring, "in"), source=da.ring_source)
    s.let("r", "the arch's inside radius: a semicircle", "S/2", "in")
    s.let("R_o", "the ring's outside radius", "r + d", "in")
    if not loads:
        return
    for i, x in enumerate(da.layers, 1):
        s.given(f"t_{i}", f"layer {i}, {x.name}", Q_(x.thickness, "in"), source=DESIGN)
        s.given(f"ρ_{i}", f"{x.name}, weight per cubic foot", Q_(x.density, "lbf/ft**3"),
                source="the material's data sheet")  # fmt: skip
    n = len(da.layers)
    s.let("b", "the wall's thickness", " + ".join(f"t_{i}" for i in range(1, n + 1)), "in")
    s.let("q", "the wall's weight per square inch of its face",
          " + ".join(f"ρ_{i}*t_{i}" for i in range(1, n + 1)), "psi")  # fmt: skip
    s.given("Z", "the wall over the springline at the door's crown", Q_(da.above, "in"),
            source=f"{DESIGN}: the wall's inside top over the door's middle")  # fmt: skip
    s.given("V", "the roof's vertical load on the wall over the door", Q_(da.edge, "lbf/ft"),
            source=da.edge_source)  # fmt: skip
    s.let("W_r", "half the ring's weight", "q*pi/4*(R_o^2 - r^2)", "lbf",
          source="a quarter annulus")  # fmt: skip
    s.let("x_r", "its centroid, out from the door's middle",
          "4*(R_o^3 - r^3)/(3*pi*(R_o^2 - r^2))", "in", source="a quarter annulus")  # fmt: skip
    s.let("W_s", "the wall over half the ring, all of it", "q*(R_o*Z - pi*R_o^2/4)", "lbf",
          source="the whole wall above the soffit taken to bear on the arch, 'certainly on the "
          "safe side' (BIA TN 31A; door-headers.md §D3.6)")  # fmt: skip
    s.let("x_s", "its centroid, out from the door's middle",
          "(R_o^2*Z/2 - R_o^3/3)/(R_o*Z - pi*R_o^2/4)", "in",
          source="a rectangle R_o by Z less a quarter disc")  # fmt: skip
    s.let("W_v", "the roof's load over half the ring", "V*R_o", "lbf")
    s.let("N", "each springing's vertical load", "W_r + W_s + W_v", "lbf")
    s.given("H", "thrust: the least the arch pushes on each jamb", Q_(da.least, "lbf"),
            source=f"{MINIMUM_THRUST}; the engine's search over radial joints every ½° "
            "(door.py: door_thrusts)")  # fmt: skip
    s.let("x_p", "where the line of thrust crosses the springing, in from the door's edge",
          "(H*R_o + W_r*x_r + W_s*x_s + W_v*R_o/2)/N - r", "in",
          source="moments of half the arch about the crown's top")  # fmt: skip


def door_arch_ring(da: DoorArchInputs, eta: float, safety: float, source: str) -> Sheet:
    """The ring against the thinnest semicircle that holds a line of thrust (Couplet–Heyman),
    with Heyman's geometric factor of safety; and, under the wall's load, the least thrust no more
    than the most, so a line of thrust fits in the ring. Geometry: no range of T/S limits it."""
    s = Sheet("frame.door-arch", "The door's arch: a line of thrust fits in its ring",
              reference=f"{ARCH_STATICS}; {source}")  # fmt: skip
    _door_arch(s, da)
    s.require("Z", ">=", "R_o")
    s.given("η", "the thinnest semicircle that stands, as t/r", eta,
            source=f"{source}: Heyman's table at a half-angle of 90°")  # fmt: skip
    s.let("k", "how many times the thinnest that stands", "d/(r + d/2)/η",
          source="Heyman's geometric factor of safety, under its own weight")  # fmt: skip
    s.given("k_min", "Heyman's factor of safety", safety, source=source)
    s.require("k", ">=", "k_min")
    s.given("H_max", "the most the arch can push: the line from the crown's soffit",
            Q_(da.most, "lbf"),
            source="Heyman's maximum thrust, hinges at the intrados at the crown and the extrados "
            "lower down (arch-thrust-theory.md §2 [A2]); the engine's search")  # fmt: skip
    s.require("H", "<=", "H_max")
    s.lever("d", Q_(0.5, "in"), Q_(24, "in"))
    return s


def _jamb_base(s: Sheet, da: DoorArchInputs) -> None:
    s.given("h_s", "the springline over the jamb's base", Q_(da.springing, "in"),
            source=f"{DESIGN}: the door's sill and height, less its radius")  # fmt: skip
    s.given("e", "the jamb's width along the wall", Q_(da.jamb, "in"), source=da.jamb_source)
    s.let("G_1", "the jamb under the springline", "q*e*h_s", "lbf")
    over = "Z"
    if da.over_jamb is not None:
        over = "Z_j"
        s.given("Z_j", "the wall counted over the springline on the jamb", Q_(da.over_jamb, "in"),
                source=f"{DESIGN}: the wall drops under the springline along the jamb, so none "
                "is counted")  # fmt: skip
    s.let("G_2", "the wall over the springline on the jamb, beside the ring",
          f"q*max(e - d, 0*d)*{over}", "lbf")  # fmt: skip
    s.given("b_c", "the cross wall bonded into the jamb's far end, its thickness",
            Q_(da.cross, "in"), source=f"{DESIGN}: the wall at the corner; 0 where the jamb "
            "ends at another door")  # fmt: skip
    s.given("q_c", "the cross wall's weight per square inch of its face", Q_(da.cross_q, "psi"),
            source="its lining's layers and densities")  # fmt: skip
    s.let("G_3", "the cross wall bonded in: one wall's thickness b of it, the jamb's full height",
          "q_c*b*(h_s + Z)", "lbf",
          source=BONDED)  # fmt: skip
    s.let("ΣV", "the vertical load on the jamb's base", "N + G_1 + G_2 + G_3", "lbf")
    s.let("x_R", "where the resultant meets the base, in from the door's edge",
          "(N*x_p + G_1*e/2 + G_2*(d + e)/2 + G_3*(e - b_c/2) + H*h_s)/ΣV", "in",
          source="moments about the door's edge at the base: the thrust carries the resultant "
          "away from the door")  # fmt: skip


def door_jamb(da: DoorArchInputs) -> Sheet:
    """The jamb as a buttress: the arch's least thrust and its load, with the jamb's own weight,
    the wall over it and a cross wall bonded into its far end, give a resultant at the jamb's base
    that must lie within it (the safe theorem), and in its middle third for no tension."""
    s = Sheet("frame.door-jamb", "The door's jamb holds the arch's thrust",
              reference=f"{ARCH_STATICS}; {MINIMUM_THRUST}; {NO_TENSION}")  # fmt: skip
    _door_arch(s, da)
    _jamb_base(s, da)
    s.require("x_R", "<=", "e")
    s.let("x_0", "the door's edge", "0*e", "in")
    s.require("x_R", ">=", "x_0")
    s.let("x_3", "the far edge of the base's middle third", "2*e/3", "in", source=NO_TENSION)
    s.require("x_R", "<=", "x_3", level="warning")
    s.lever("e", Q_(2, "in"), Q_(240, "in"))
    return s


def door_slide(da: DoorArchInputs, mu: float, source: str) -> Sheet:
    """Sliding at the springing: the arch's least thrust over its vertical load there must not
    pass the friction between brick units (BIA: stable if the resultant's angle to the joint's
    normal is under the angle of friction). The jamb's base carries more weight for the same
    thrust, so the springing's level joint governs."""
    s = Sheet("frame.door-slide", "The door's arch doesn't slide at its springing",
              reference=f"{source}; {MINIMUM_THRUST}")  # fmt: skip
    _door_arch(s, da)
    s.let("μ_need", "the friction the springing's level joint needs", "H/N",
          source="the resultant's angle to the joint's normal: tan⁻¹(H/N)")  # fmt: skip
    s.given("μ", "friction between brick masonry units", mu, source=source)
    s.require("μ_need", "<=", "μ")
    return s


def steel_heat(hot: HotSteel, table_top: float, service: float, service_source: str) -> Sheet:
    """The frame steel's temperature against the sourced range: AISC's table of E(T) ends at
    1,400 °F (past it nothing sourced gives the steel's stiffness: refuse), and Giles keeps carbon
    steel at or under 600 °F in continuous service (AISC's table is for fire, a short event)."""
    s = Sheet(
        "frame.steel-heat",
        "The frame steel's temperature against its sourced range",
        reference=f"{hot.source}; {service_source}; steel-design.md §S3",
    )
    s.given("T_s", "the steel's temperature", Q_(hot.temperature, "degF"), "degF", source=hot.where)
    s.given("T_table", "hottest in AISC Table A-4.2.1's E(T) column", Q_(table_top, "degF"), "degF",
            source=hot.source)  # fmt: skip
    s.given("T_service", "hottest for carbon steel held hot (Giles)", Q_(service, "degF"), "degF",
            source=service_source)  # fmt: skip
    s.require("T_s", "<=", "T_table")
    s.require("T_s", "<=", "T_service", level="warning")
    return s


# ---- An arch along the chamber's depth, on its end walls (vault.py) ----------------------------


def vault_ring(a: ArchInputs, eta: float, safety: float, source: str) -> Sheet:
    """A roof arch's ring against the thinnest circular arch of its half-angle that holds a line
    of thrust under its own weight (Couplet–Heyman), with Heyman's geometric factor of safety:
    geometry alone, so no range of T/S limits it (as the door arch's and the dome slice's)."""
    s = Sheet("frame.vault-ring", "The arch's ring holds a line of thrust",
              reference=f"{ARCH_STATICS}; {source}")  # fmt: skip
    _arch(s, a)
    s.given("η", "the thinnest ring that stands, as t/r, at this half-angle", eta,
            source=f"{source}: Heyman's table by half-angle, interpolated at φ")  # fmt: skip
    s.let("k", "how many times the thinnest that stands", "T/(r + T/2)/η",
          source="Heyman's geometric factor of safety")  # fmt: skip
    s.given("k_min", "Heyman's factor of safety", safety, source=source)
    s.require("k", ">=", "k_min")
    s.lever("t_1", Q_(0.5, "in"), Q_(24, "in"))
    return s


END_WALL = (
    "the end wall as a buttress, per foot of its width: the arch's thrust and half its weight at "
    "the springing, with the wall's own weight under it, give a resultant at the wall's base that "
    "must lie within it (Heyman's safe theorem), and in its middle third for no tension"
)


def vault_end_wall(a: ArchInputs, wall: tuple[Layer, ...], springing: float) -> Sheet:
    """An arch spanning the chamber's depth springs from the front and back walls: each must hold
    half its weight and its thrust, cold (hinges at mid-ring, the three-hinged arch's H), as a
    buttress standing on its own, per foot of the wall's width. The line of thrust crosses the
    springing at the ring's middle; the fill over the skewback, which would steady the wall, is
    left out."""
    s = Sheet("frame.vault-end-wall", "The end wall alone holds the arch's thrust, cold",
              reference=f"{ARCH_STATICS}; {NO_TENSION}")  # fmt: skip
    _arch(s, a, weights=True)
    _thrust(s, len(a.layers), cold=True)
    for i, x in enumerate(wall, 1):
        s.given(f"e_{i}", f"end wall layer {i}, {x.name}", Q_(x.thickness, "in"), source=DESIGN)
        s.given(f"γ_{i}", f"{x.name}, weight per cubic foot", Q_(x.density, "lbf/ft**3"),
                source="the material's data sheet")  # fmt: skip
    n = len(wall)
    s.let("e", "the end wall's thickness", " + ".join(f"e_{i}" for i in range(1, n + 1)), "in")
    s.given("h_s", "the springline over the floor", Q_(springing, "in"),
            source=f"{DESIGN}: the chamber's height")  # fmt: skip
    weight = " + ".join(f"γ_{i}*e_{i}" for i in range(1, n + 1))
    s.let("G", "the end wall's weight under the springline, per foot", f"({weight})*h_s", "lbf/ft")
    s.let("N", "half the arch's weight, on the springing", "W/2", "lbf/ft")
    s.let("x_p", "where the line of thrust crosses the springing, in from the wall's inside face",
          "(r + T/2)*sin(φ) - S/2", "in", source="the ring's middle at the skewback")  # fmt: skip
    s.let("y_p", "its height over the floor", "h_s + T/2*cos(φ)", "in")
    s.let("x_R", "where the resultant meets the wall's base, in from its inside face",
          "(N*x_p + G*e/2 + H_c*y_p)/(N + G)", "in",
          source="moments about the base's inside edge: the thrust carries it outward")  # fmt: skip
    s.require("x_R", "<=", "e")
    s.let("x_3", "the far edge of the base's middle third", "2*e/3", "in", source=NO_TENSION)
    s.require("x_R", "<=", "x_3", level="warning")
    return s


UNEVEN_STATICS = (
    "a three-hinged circular arch, hinges at each springing and the crown, its halves unequal: "
    "moments of each half about the crown, and the vertical loads summing to its weight (statics, "
    "as the level arch's H_c)"
)


def vault_end_wall_uneven(
    r: float,
    front: float,
    back: float,
    layers: tuple[Layer, ...],
    ring: int,
    wall: tuple[Layer, ...],
    springing: float,
    end: str,
    source: str,
) -> Sheet:
    """An arch along the chamber's depth springing at different heights at its ends: one end
    wall, as vault_end_wall's, holding the arch's cold thrust and that end's share of its weight.
    The circle's inside radius r and each springing's angle from the crown, φ_f and φ_b, are the
    engine's (the circle through both springings, its crown the rise over the back's)."""
    s = Sheet(f"frame.vault-end-wall-{end}", f"The {end} wall alone holds the arch's thrust, cold",
              reference=f"{ARCH_STATICS}; {NO_TENSION}; {UNEVEN_STATICS}")  # fmt: skip
    s.given("r", "inside radius", Q_(r, "in"), source=source)
    s.given("φ_f", "the front springing's angle from the crown", Q_(front, "degree"), "degree",
            source=source)  # fmt: skip
    s.given("φ_b", "the back springing's angle from the crown", Q_(back, "degree"), "degree",
            source=source)  # fmt: skip
    for i, x in enumerate(layers, 1):
        s.given(f"t_{i}", f"layer {i}, {x.name}", Q_(x.thickness, "in"), source=DESIGN)
        s.given(f"ρ_{i}", f"{x.name}, weight per cubic foot", Q_(x.density, "lbf/ft**3"),
                source="the material's data sheet")  # fmt: skip
    s.let("T", "the ring: its layers' thickness",
          " + ".join(f"t_{i}" for i in range(1, ring + 1)), "in")  # fmt: skip
    below: list[str] = []
    for i in range(1, len(layers) + 1):
        inner = " + ".join(["r", *below])
        s.let(f"w_{i}", f"layer {i}'s weight per foot of arch",
              f"ρ_{i}*t_{i}*(φ_f + φ_b)*({inner} + t_{i}/2)", "lbf/ft",
              source="density × thickness × the arc at mid-layer")  # fmt: skip
        below.append(f"t_{i}")
    total = " + ".join(f"w_{i}" for i in range(1, len(layers) + 1))
    s.let("W", "the arch's weight per foot", total, "lbf/ft",
          source="HarbisonWalker's W, exact form; kiln-hardware.md §4.6 [S20]")  # fmt: skip
    for e in ("f", "b"):
        s.let(f"W_{e}", f"the {'front' if e == 'f' else 'back'} half's weight",
              f"W*φ_{e}/(φ_f + φ_b)", "lbf/ft")  # fmt: skip
        s.let(f"ℓ_{e}", "its centroid's lever about its springing, over r",
              f"sin(φ_{e}) - (1 - cos(φ_{e}))/φ_{e}",
              source="an arc's centroid, r(1 − cos φ)/φ in from the crown")  # fmt: skip
    s.let("H_c", "thrust, cold",
          "(W_f*ℓ_f/sin(φ_f) + W_b*ℓ_b/sin(φ_b))/((1 - cos(φ_f))/sin(φ_f) + "
          "(1 - cos(φ_b))/sin(φ_b))", "lbf/ft", source=UNEVEN_STATICS)  # fmt: skip
    e = "f" if end == "front" else "b"
    s.let("N", f"the {end} springing's vertical load",
          f"(H_c*(1 - cos(φ_{e})) + W_{e}*(sin(φ_{e}) - ℓ_{e}))/sin(φ_{e})", "lbf/ft",
          source=UNEVEN_STATICS)  # fmt: skip
    for i, x in enumerate(wall, 1):
        s.given(f"e_{i}", f"end wall layer {i}, {x.name}", Q_(x.thickness, "in"), source=DESIGN)
        s.given(f"γ_{i}", f"{x.name}, weight per cubic foot", Q_(x.density, "lbf/ft**3"),
                source="the material's data sheet")  # fmt: skip
    n = len(wall)
    s.let("e", "the end wall's thickness", " + ".join(f"e_{i}" for i in range(1, n + 1)), "in")
    s.given("h_s", "the springline over the floor", Q_(springing, "in"),
            source=f"{DESIGN}: the {end} wall's springline")  # fmt: skip
    weight = " + ".join(f"γ_{i}*e_{i}" for i in range(1, n + 1))
    s.let("G", "the end wall's weight under the springline, per foot", f"({weight})*h_s", "lbf/ft")
    s.let("x_p", "where the line of thrust crosses the springing, in from the wall's inside face",
          f"T/2*sin(φ_{e})", "in", source="the ring's middle at the skewback")  # fmt: skip
    s.let("y_p", "its height over the floor", f"h_s + T/2*cos(φ_{e})", "in")
    s.let("x_R", "where the resultant meets the wall's base, in from its inside face",
          "(N*x_p + G*e/2 + H_c*y_p)/(N + G)", "in",
          source="moments about the base's inside edge: the thrust carries it outward")  # fmt: skip
    s.require("x_R", "<=", "e")
    s.let("x_3", "the far edge of the base's middle third", "2*e/3", "in", source=NO_TENSION)
    s.require("x_R", "<=", "x_3", level="warning")
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
    "AngleSection",
    "ArchInputs",
    "CatenaryLayer",
    "DomeInputs",
    "HotSteel",
    "Layer",
    "Springs",
    "buttress_bending",
    "catenary_feet",
    "checked_range",
    "dome_buttress",
    "dome_checked_range",
    "dome_factor",
    "dome_heated",
    "dome_hot_line",
    "dome_rise",
    "dome_rod",
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
    "steel_heat",
    "thrust_through_steel",
]
