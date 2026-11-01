"""The steel that holds a kiln together: a frame for a sprung arch, or an electric kiln's case.

A catenary needs no frame over it, but its feet push out (its thrust is worked out, but what holds
the feet isn't sized). A sail dome over a door stands as arches spanning the walls either side, and
an angle along each, tied by rods, holds its thrust, checked hot by AISC 360-16 (steel-design.md).

A sprung arch pushes out on its skewbacks, and the frame must take that thrust: buttress angles
along the top of the side walls, held at their ends by corner posts tied across the kiln by
threaded rod (kiln-hardware.md §4.1). The thrust comes from HarbisonWalker's arch method
(§4.3 [S20]); the steel is checked against HarbisonWalker's 12,000 psi limit for bindings that may
run hot, with the angle's section modulus from AISC (§4.7). No source relates frame steel to arch
span, so the builders' published sizes (Pitelka [S11]) set the smallest angle, and the thrust check
can only make it bigger.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from functools import cache
from importlib import resources
from typing import Any

import numpy as np
import yaml
from pydantic import BaseModel, ConfigDict

from kilndesigner.frame_checks import (
    CAPPED,
    THRUST_THROUGH_STEEL,
    AngleSection,
    ArchInputs,
    CatenaryLayer,
    DomeInputs,
    HotSteel,
    Layer,
    Springs,
    buttress_bending,
    catenary_feet,
    checked_range,
    dome_buttress,
    dome_checked_range,
    dome_factor,
    dome_heated,
    dome_hot_line,
    dome_rise,
    dome_rod,
    dome_thickest,
    flat_friction,
    flat_ifb_top,
    flat_rods,
    flat_span,
    heated_factor_limit,
    hot_thrust_line,
    loose_ring,
    post_bending,
    rise_rule,
    rod_stress,
    skewback_on_wall,
    steel_heat,
    thrust_through_steel,
)
from kilndesigner.heatloss import top_temperature
from kilndesigner.model import CatenaryArch, Dome, FlatRoof, Kiln, SprungArch, arches_along
from kilndesigner.shape import Arch, CatenaryCurve, SailDome, chamber_shape
from kilndesigner.units import Q_, parse_quantity, si
from kilndesigner.working import Finding, Step

PITELKA = "Pitelka, sprung-arch frames; kiln-hardware.md §4.2 [S11]"
OLSEN_FRAME = (
    "Olsen, The Kiln Book, 4th ed., p.139 (the fast-fire kiln's bolted 2 × 2 × 3/16 in angle) and "
    "p.174 (an updraft 5 × 5 × 6 ft outside: corners 3 × 3 × ¼ in; smaller kilns 3/16 in)"
)
OLSEN_FRAME_FT3 = 5 * 5 * 6
"""ft³ outside: Olsen's updraft whose frame he sizes, 5 × 5 × 6 ft (p.174)."""
OLSEN_LEAST_RISE = 1.5  # in per foot of span (p.51)
OLSEN_RISE = (
    "Olsen, The Kiln Book, 4th ed., p.51: about 1½ in/ft at least, what a featheredge skewback "
    "gives; 3 in/ft 'generally' the most, but he has built 6 in/ft and there is 'no hard-and-fast "
    "rule'; p.296: 4–6 in/ft on chamber kilns of 4–8 ft span"
)
MERRILL = "Merrill flat-top kiln; kiln-hardware.md §4.2 [S16]"
CASE_SOURCE = (
    "L&L Easy-Load bulletin, 1/8 in welded steel case; electric-kiln-hardware.md §1.2 [S6]"
)
FLAT_BAR = "¼ × 2 in flat bar"


@cache
def steel_data() -> dict[str, Any]:
    text = resources.files("kilndesigner.data").joinpath("steel.yaml").read_text(encoding="utf-8")
    data: dict[str, Any] = yaml.safe_load(text)
    return data


@dataclass(frozen=True)
class Angle:
    name: str
    leg: float  # in
    t: float  # in
    w: float  # lb/ft
    sx: float  # in³, about a geometric axis
    sz: float  # in³, about the minor principal axis
    ix: float  # in⁴, about a geometric axis


def angles() -> list[Angle]:
    return [Angle(**s) for s in steel_data()["angles"]["shapes"]]


def angle(name: str) -> Angle:
    return next(a for a in angles() if a.name == name)


class Member(BaseModel):
    """A run of steel the frame needs: what it is, how many and how long."""

    model_config = ConfigDict(frozen=True)

    part: str
    steel: str
    count: int
    length_in: float
    source: str | None = None

    @property
    def total_ft(self) -> float:
        return self.count * self.length_in / 12


class FrameDesign(BaseModel):
    model_config = ConfigDict(frozen=True)

    kind: str  # "arch frame", "angle frame" or "welded case"
    angle: str | None  # the angle for posts and buttresses
    angle_leg_in: float
    angle_t_in: float
    rod: str | None
    rod_d_in: float
    thrust: str | None  # the design thrust, per foot of arch length
    members: list[Member]
    working: list[Step]
    findings: list[Finding]
    posts: int = 2
    """Posts along each side wall, the corners included, each pair tied across by a rod."""


@dataclass(frozen=True)
class Outside:
    """The lining's outside: its sizes and the wall thicknesses (in)."""

    width: float
    depth: float
    bottom: float  # below the chamber floor
    wall_top: float  # above the chamber floor: the springline, or the top of a flat roof
    left: float
    right: float


def outside(kiln: Kiln) -> Outside:
    def t(face: str) -> float:
        layers = kiln.lining.for_face(face, door_face=kiln.door_face)  # type: ignore[arg-type]
        return sum(si(x.thickness, "in") for x in layers)

    w, d, h = (si(getattr(kiln.chamber, n), "in") for n in ("width", "length", "height"))
    if isinstance(kiln.roof, CatenaryArch):
        # The arch is the side walls: as wide outside as its outer layer at the floor
        side = CatenaryCurve(w, h).half_width(t("roof")) - w / 2
        return Outside(
            width=w + 2 * side,
            depth=d + t("front") + t("back"),
            bottom=t("floor"),
            wall_top=h + t("roof"),
            left=side,
            right=side,
        )
    top = h if isinstance(kiln.roof, SprungArch | Dome) else h + t("roof")
    return Outside(
        width=w + t("left") + t("right"),
        depth=d + t("front") + t("back"),
        bottom=t("floor"),
        wall_top=top,
        left=t("left"),
        right=t("right"),
    )


def skewback_top(kiln: Kiln, *, whole_roof: bool = False) -> float:
    """Height of the skewback's top above the chamber floor (in): the solid ring's outer corner,
    where the buttress takes the thrust (review S5); insulation laid over the ring is only load.
    ``whole_roof``: the outer corner of every roof layer, the kiln's outside at the springing."""
    assert isinstance(kiln.roof, SprungArch)
    w = si(kiln.chamber.width, "in")
    arch = Arch(w, si(kiln.roof.rise, "in"))
    layers = kiln.lining.for_face("roof")
    roof = sum(si(x.thickness, "in") for x in (layers if whole_roof else layers[: kiln.roof.ring]))
    centre = si(kiln.chamber.height, "in") + arch.rise - arch.radius
    return centre + (arch.radius + roof) * math.cos(arch.half_angle)


LOOSE = ("fibre_blanket", "fibre_board", "backup_insulation")
"""Kinds of material that can't carry an arch's thrust: they're only ever its load."""


@dataclass(frozen=True)
class ArchLoad:
    """An arch's weight and its ring: the layers the design marks as the ring, from the inside;
    the rest are laid on the ring and are only load (HarbisonWalker's tables leave them out)."""

    weight: float  # lb per foot of arch length, every layer
    ring: float  # in, the ring's thickness
    ring_kinds: tuple[str, ...]
    loose: tuple[str, ...]  # ring layers that can't carry thrust, by name
    lines: tuple[str, ...]


def _arch_load(kiln: Kiln, arch: Arch) -> ArchLoad:
    """Every layer's density × thickness × mean arc, the exact form of HarbisonWalker's W
    (§4.6), and the ring's thickness."""
    from kilndesigner.castable import resolve_material

    assert isinstance(kiln.roof, SprungArch)
    weight, ring = 0.0, 0.0
    kinds: list[str] = []
    loose: list[str] = []
    lines: list[str] = []
    r = arch.radius
    for i, layer in enumerate(kiln.lining.for_face("roof")):
        m = resolve_material(kiln, layer.material)
        rho = si(parse_quantity(m.density), "lb/ft**3")
        t = si(layer.thickness, "in")
        mean_arc_ft = (r + t / 2) * 2 * arch.half_angle / 12
        wt = rho * (t / 12) * mean_arc_ft
        weight += wt
        if i < kiln.roof.ring:
            ring += t
            kinds.append(m.kind)
            if m.kind in LOOSE:
                loose.append(m.name)
        lines.append(f"{m.name}: {rho:.0f} lb/ft³ × {t:g} in × {mean_arc_ft:.2f} ft = {wt:.1f}")
        r += t
    return ArchLoad(weight, ring, tuple(kinds), tuple(loose), tuple(lines))


def _roof_layers(kiln: Kiln) -> tuple[Layer, ...]:
    """The roof's layers from the inside, as its sheets take them (frame_checks)."""
    from kilndesigner.castable import resolve_material

    return tuple(
        Layer(m.name, si(parse_quantity(m.density), "lb/ft**3"), si(x.thickness, "in"))
        for x in kiln.lining.for_face("roof")
        for m in [resolve_material(kiln, x.material)]
    )


def _arch_inputs(kiln: Kiln) -> ArchInputs:
    """The design's numbers an arch's sheets start from (frame_checks)."""
    assert isinstance(kiln.roof, SprungArch)
    span, rise = si(kiln.chamber.width, "in"), si(kiln.roof.rise, "in")
    return ArchInputs(span, rise, _roof_layers(kiln), kiln.roof.ring)


def ring_outside(kiln: Kiln) -> float:
    """How far out from the chamber's centre line the arch's ring reaches at the skewback (in):
    its outer corner."""
    assert isinstance(kiln.roof, SprungArch)
    arch = Arch(si(kiln.chamber.width, "in"), si(kiln.roof.rise, "in"))
    rings = kiln.lining.for_face("roof")[: kiln.roof.ring]
    return (arch.radius + sum(si(x.thickness, "in") for x in rings)) * math.sin(arch.half_angle)


def cold_thrust_factor(span: float, rise: float) -> float:
    """H / W for a circular arch, three-hinged, its weight spread evenly along the arc.

    Moments about a springing for half the arch: H·h = (W/2)·x̄, where x̄ is the horizontal
    distance from the springing to the half-arc's centroid, R·sin θ − R(1 − cos θ)/θ, and
    h = R(1 − cos θ), θ the half-angle. So H/W = (sin θ − (1 − cos θ)/θ) / (2(1 − cos θ)).
    It matches HarbisonWalker's table to ±0.6 %, its rounding (test_frame.py).
    """
    theta = 2 * math.atan(2 * rise / span)  # tan(θ/2) = 2h/S for a circular segment
    one_minus_cos = 1 - math.cos(theta)
    return (math.sin(theta) - one_minus_cos / theta) / (2 * one_minus_cos)


def _arch_moment(span: float, rise: float, thickness: float, hot: bool) -> float | None:
    """H × (weight per unit volume) for half an arch, with the thrust line at two contacts.

    Cold: both contacts at mid-thickness. Hot, the arch pressed between the steel: the
    intrados at the crown and the extrados at the skewback (Heyman's maximum thrust;
    arch-thrust-theory.md). Moments about the skewback contact P: H·(y_crown − y_P) =
    (W/2)·(x_P − x̄). None when the hot contacts can't make a lever: the thrust line leaves the
    brick.
    """
    phi = 2 * math.atan(2 * rise / span)
    r = span / 2 / math.sin(phi)
    outer = r + thickness
    half_area = (outer**2 - r**2) / 2 * phi
    x_bar = (2 / 3) * (outer**3 - r**3) / (outer**2 - r**2) * (1 - math.cos(phi)) / phi
    y_crown, r_p = (r, outer) if hot else (r + thickness / 2, r + thickness / 2)
    lever = y_crown - r_p * math.cos(phi)
    if lever <= 0:
        return None
    return half_area * (r_p * math.sin(phi) - x_bar) / lever


def heated_thrust_factor(span: float, rise: float, thickness: float) -> float | None:
    """Hot thrust of an arch free to rise, as a multiple of its cold thrust (statics).

    Reproduces all 73 printed cells of HarbisonWalker's table to 4 % (test_frame.py).
    """
    hot = _arch_moment(span, rise, thickness, hot=True)
    cold = _arch_moment(span, rise, thickness, hot=False)
    if hot is None or cold is None:
        return None
    return hot / cold


MAX_PRINTED_HEATED = 5.34  # the largest factor HarbisonWalker prints before "stress excessive"
ARCH_THEORY_SOURCE = (
    "statics with hinges at the arch faces (Heyman, maximum thrust); arch-thrust-theory.md "
    "[A1–A3], checked against HarbisonWalker's heated-arch table, kiln-hardware.md §4.3 [S20]"
)


NO_FRAME = "no frame"
"""A frame's kind when no steel is designed or drawn: a catenary, or a dome."""
CATENARY_SOURCE = "statics of a catenary, combustion-and-masonry.md §6.6 [S63] (derived)"


def _catenary_feet(kiln: Kiln) -> FrameDesign:
    """A catenary carries its own weight in compression, so it needs no frame over it; its feet
    push out, with the chain's horizontal tension turned round (combustion-and-masonry.md
    §6.6). Nothing sourced sizes what holds them, so nothing is drawn."""
    from kilndesigner.castable import resolve_material

    span_ft = si(kiln.chamber.width, "ft")
    curve = CatenaryCurve(span_ft, si(kiln.chamber.height, "ft"))
    # Each layer's weight over its own length, at its mid-thickness: the outer layers are longer
    # than the inside curve the statics run along
    total, cum, lines = 0.0, 0.0, []
    layers: list[CatenaryLayer] = []
    for layer in kiln.lining.for_face("roof"):
        m = resolve_material(kiln, layer.material)
        rho, t = si(parse_quantity(m.density), "lb/ft**3"), si(layer.thickness, "ft")
        length = curve.length(cum + t / 2)
        total += rho * t * length
        lines.append(
            f"{m.name}: {rho:.0f} lb/ft³ × {t * 12:g} in × {length:.2f} ft = "
            f"{rho * t * length:.1f} lb"
        )
        layers.append(CatenaryLayer(m.name, rho, t * 12, length))
        cum += t
    weight = total / curve.arc_length
    push = weight * curve.a
    bear = weight * curve.a * math.sinh(span_ft / 2 / curve.a)
    working = [
        Step(
            name="Catenary parameter",
            value=f"a = {curve.a * 12:.2f} in",
            formula="H = a (cosh(S / 2a) − 1), solved for a",
            inputs={"span S": f"{span_ft * 12:g} in", "height H": f"{curve.height * 12:g} in"},
            reference=CATENARY_SOURCE,
        ),
        Step(
            name="Arch weight per foot of its length, per foot of kiln",
            value=f"{weight:.1f} lb/ft²",
            formula=(
                "Σ density × thickness × length at mid-thickness, over the arch's layers, ÷ the "
                "inside curve's length"
            ),
            inputs={
                **{f"layer {i + 1}": s for i, s in enumerate(lines)},
                "inside curve": f"{curve.arc_length:.2f} ft",
            },
            reference=CATENARY_SOURCE,
        ),
        Step(
            name="Push out at each foot",
            value=f"{push:.0f} lb per foot of kiln",
            formula="H = w a: the hanging chain's horizontal tension, turned to thrust",
            reference=CATENARY_SOURCE,
            note="The cold arch carrying only itself; how heat changes it is not sourced.",
        ),
        Step(
            name="Weight on each foot",
            value=f"{bear:.0f} lb per foot of kiln",
            formula="V = w a sinh(S / 2a): half the arch",
            reference=CATENARY_SOURCE,
        ),
    ]
    feet = catenary_feet(span_ft * 12, curve.height * 12, curve.a * 12, layers, CATENARY_SOURCE)
    feet.agrees("H_a", Q_(curve.height, "ft"))
    feet.agrees("s", Q_(curve.arc_length, "ft"))
    feet.agrees("H", Q_(push, "lbf/ft"))
    feet.agrees("V", Q_(bear, "lbf/ft"))
    findings = [
        Finding.failed(
            feet.check(),
            message=(
                f"Each foot of the catenary pushes out with about {push:.0f} lb per foot of kiln, "
                "cold. No source sizes what holds it (a curb, ties or buttresses at the feet), "
                "so none is drawn: have it designed."
            ),
            reference="combustion-and-masonry.md §6.6",
        )
    ]
    return FrameDesign(
        kind=NO_FRAME, angle=None, angle_leg_in=0, angle_t_in=0, rod=None, rod_d_in=0,
        thrust=f"{push:.0f} lb per foot of kiln at each foot", members=[], working=working,
        findings=findings,
    )  # fmt: skip


DOME_SOURCE = (
    "Heyman's half dome sliced into parallel arches, the safe theorem; domes-over-doors.md §D3–D4 "
    "[D3] [D4] (derived)"
)


@dataclass(frozen=True)
class DomeSlice:
    """One arch of a dome sliced parallel to its door wall, ``at`` in from the middle (in)."""

    at: float
    thickness: float  # the ring's, in the slice's plane (in)
    half_angle: float  # radians
    rise: float  # the slice's own rise above its springings (in)
    factor: float  # thickness over the thinnest that stands, cold (Heyman)
    thickest: float  # HarbisonWalker's limit for the slice's rise (in)
    weight: float  # lb per inch of the walls it spans, every layer
    span: float = 0.0  # in: the symmetric arch's span (a curved plan's; the chamber's otherwise)


CURVED_SLICE_SOURCE = (
    "the engine's own cautious rule over a curved plan: each slice taken as the symmetric arch on "
    "its farther springing, the larger span, half-angle and weight (derived from the sliced dome, "
    "domes-over-doors.md §D4)"
)


def _curved_chords(kiln: Kiln, count: int) -> tuple[float, list[tuple[float, float]]]:
    """A dome over a curved plan (chamber.outline), sliced parallel to the door wall: the
    sphere's inside radius (in), and for each slice its distance from the sphere's centre and
    the farther of its two springings along it, from the centre's line (in). Slices with no
    chord, past the plan's edge, are left out."""
    from kilndesigner.form import crown_of, plan_of
    from kilndesigner.outline import SphereDome

    assert isinstance(kiln.roof, Dome)
    plan, crown = plan_of(kiln, "in"), crown_of(kiln, "in")
    radius = SphereDome(plan, si(kiln.roof.rise, "in"), crown).radius
    pts = plan.points(96)
    across = kiln.door_face in ("front", "back")  # slices across the kiln, at y = constant
    k, u = (1, 0) if across else (0, 1)  # the coordinate fixing the slice, the one along it
    lo, hi = min(p[k] for p in pts), max(p[k] for p in pts)
    out: list[tuple[float, float]] = []
    for i in range(count):
        at = lo + (hi - lo) * i / (count - 1)
        cuts = []
        for p, q in itertools.pairwise([*pts, pts[0]]):
            if (p[k] - at) * (q[k] - at) <= 0 and p[k] != q[k]:
                s = (at - p[k]) / (q[k] - p[k])
                cuts.append(p[u] + s * (q[u] - p[u]) - crown[u])
        if len(cuts) >= 2 and max(cuts) - min(cuts) > 1e-6:
            out.append((at - crown[k], max(abs(c) for c in cuts)))
    return radius, out


def dome_slices(kiln: Kiln, rise: float | None = None, count: int = 21) -> list[DomeSlice]:
    """The dome as arches parallel to the door wall, spanning the two walls either side, from the
    middle out to the end wall (the dome is symmetric). ``rise`` (in) overrides the design's.
    Over a curved plan the slices run across the whole plan, each taken as the symmetric arch on
    its farther springing (CURVED_SLICE_SOURCE)."""
    from kilndesigner.castable import resolve_material

    assert isinstance(kiln.roof, Dome)
    w, d = si(kiln.chamber.width, "in"), si(kiln.chamber.depth, "in")
    span, length = (w, d) if kiln.door_face in ("front", "back") else (d, w)
    dome = SailDome(w, d, si(kiln.roof.rise, "in") if rise is None else rise)
    radius = dome.radius
    cuts = [(length / 2 * i / (count - 1), span / 2) for i in range(count)]
    if kiln.chamber.outline is not None:
        assert rise is None, "a curved plan's dome has the design's rise"
        radius, cuts = _curved_chords(kiln, count)
    layers = [
        (si(parse_quantity(resolve_material(kiln, x.material).density), "lb/ft**3") / 1728,
         si(x.thickness, "in"))
        for x in kiln.lining.for_face("roof")
    ]  # fmt: skip
    ring = sum(t for _, t in layers[: kiln.roof.ring])
    table = steel_data()["arch_minimum_thickness"]
    slices: list[DomeSlice] = []
    for y, half in cuts:
        span = 2 * half
        inside = math.sqrt(radius**2 - y**2)
        alpha = math.asin(min(1.0, span / 2 / inside))
        own_rise = inside * (1 - math.cos(alpha))
        thickness = math.sqrt((radius + ring) ** 2 - y**2) - inside
        eta = float(np.interp(math.degrees(alpha), table["half_angle_deg"], table["eta"]))
        weight, r = 0.0, radius
        for density, t in layers:  # each layer's slice: its thickness × centre radius × arc
            lo, hi = math.sqrt(r**2 - y**2), math.sqrt((r + t) ** 2 - y**2)
            weight += density * (hi - lo) * (lo + hi) / 2 * 2 * alpha
            r += t
        slices.append(
            DomeSlice(
                y, thickness, alpha, own_rise, thickness / (inside + thickness / 2) / eta,
                (own_rise - span / 48) / math.cos(alpha), weight, span,
            )
        )  # fmt: skip
    return slices


def _curved_dome_thrust(kiln: Kiln) -> tuple[str | None, list[Step]]:
    """A dome over a curved plan, sliced parallel to the door wall (dome_slices): each slice's
    thrust on the walls it springs from, cold and hot, per foot of wall; the most of them. None
    when a slice's hot line of thrust leaves it."""
    slices = dome_slices(kiln)
    worst: tuple[float, float, DomeSlice] | None = None
    for s in slices:
        factor = heated_thrust_factor(s.span, s.rise, s.thickness)
        if factor is None:
            return None, [
                Step(
                    name="Thrust the masonry holds",
                    value=(
                        f"not worked out: hot, the slice {s.at:.1f} in from the crown would push "
                        "its line of thrust out of the ring"
                    ),
                    reference=f"{CURVED_SLICE_SOURCE}; {ARCH_THEORY_SOURCE}",
                )
            ]
        cold = cold_thrust_factor(s.span, s.rise) * s.weight * 12
        hot = min(factor, MAX_PRINTED_HEATED) * cold
        if worst is None or hot > worst[1]:
            worst = (cold, hot, s)
    assert worst is not None
    cold, hot, s = worst
    thrust = f"{hot:.0f} lb per foot of wall, hot ({cold:.0f} cold)"
    return thrust, [
        Step(
            name="Thrust the masonry holds",
            value=thrust,
            formula=(
                "the dome over the curved plan in slices parallel to the door wall, each a "
                "circular arch of radius √(R² − y²) on its farther springing: H = W·(sin α − "
                "(1 − cos α)/α) / (2(1 − cos α)), W its weight; hot, × the heated factor (at most "
                f"{MAX_PRINTED_HEATED:g}, the largest HarbisonWalker prints)"
            ),
            inputs={
                "slices": f"{len(slices)}",
                "the most": (
                    f"{s.at:.1f} in from the crown: {s.span:.1f} in span, rising {s.rise:.2f} "
                    f"in, {s.thickness:.2f} in thick"
                ),
            },
            reference=f"{CURVED_SLICE_SOURCE}; {DOME_SOURCE}; {ARCH_THEORY_SOURCE}; {CAPPED}",
            note=(
                "The slices near the walls are short and flat and rest on the walls' tops cast "
                "up to the dome; the slicing is one way the dome can stand (Heyman's safe "
                "theorem), not the only one."
            ),
        )
    ]


def _dome_frame(kiln: Kiln) -> FrameDesign:
    """A sail dome with a door: it stands as arches parallel to the door wall, spanning the two
    walls either side, if every one stands (domes-over-doors.md §D4, §D7). Its thrust on those
    walls is worked out; no source sizes the steel for it yet."""
    from kilndesigner.castable import resolve_material

    assert isinstance(kiln.roof, Dome)
    assert kiln.chamber.outline is None, "a curved plan's dome is held by masonry (model.py)"
    data = steel_data()
    rule, minimum = data["rise_per_foot"], data["arch_minimum_thickness"]
    working: list[Step] = []
    findings: list[Finding] = []
    door = kiln.door_face
    w, d = si(kiln.chamber.width, "in"), si(kiln.chamber.depth, "in")
    span, length = (w, d) if door in ("front", "back") else (d, w)
    walls = "the left and right walls" if door in ("front", "back") else "the front and back walls"
    rings = kiln.lining.for_face("roof")[: kiln.roof.ring]
    kinds = [resolve_material(kiln, x.material) for x in rings]
    if loose := [m.name for m in kinds if m.kind in LOOSE]:
        findings.append(
            Finding.failed(
                loose_ring("dome", loose, DOME_SOURCE).check(),
                message=(
                    f"The dome's ring includes {' and '.join(loose)}, which can't carry a dome: "
                    "the ring must be brick or castable. Set the roof's ring to the layers that "
                    "are."
                ),
            )
        )
        return _unframed(working, findings)
    slices = dome_slices(kiln)
    middle, end = slices[0], slices[-1]
    dm = DomeInputs(span, length, si(kiln.roof.rise, "in"), _roof_layers(kiln), kiln.roof.ring)

    def where(s: DomeSlice) -> str:
        if s is middle:
            return "in the middle"
        return "at the end walls" if s is end else f"{s.at:.1f} in from the middle"

    def describe(s: DomeSlice) -> str:
        return (
            f"{s.thickness:.2f} in thick, {math.degrees(s.half_angle):.1f}° each side, rising "
            f"{s.rise:.2f} in ({12 * s.rise / span:.2f} in/ft); factor {s.factor:.0f}; "
            f"HarbisonWalker allows {s.thickest:.2f} in"
        )

    working.append(
        Step(
            name="Dome, as arches parallel to the door wall",
            value=f"{len(slices)} slices spanning {walls}, {span:g} in apart",
            inputs={"in the middle": describe(middle), "at the end wall": describe(end)},
            formula=(
                "each slice a circular arch: ρ = √(R² − y²), sin α = ½S/ρ, its own rise "
                "ρ(1 − cos α); factor = (t/r) ÷ the thinnest t/r that stands; HarbisonWalker: "
                "t ≤ (h − S/48) ÷ cos α"
            ),
            reference=f"{DOME_SOURCE}; {minimum['source']}; {data['arch_constants']['source']}",
            note=(
                "Applying HarbisonWalker's rules for sprung arches to a dome's slices is an "
                "assumption (domes-over-doors.md §D8). The door wall and the wall opposite carry "
                "nothing."
            ),
        )
    )
    weak = min(slices, key=lambda s: s.factor)
    eta = float(np.interp(math.degrees(weak.half_angle), minimum["half_angle_deg"], minimum["eta"]))
    standing = dome_factor(dm, weak.at, eta, minimum["safety"], minimum["source"])
    standing.agrees("T", Q_(weak.thickness, "in"))
    standing.agrees("φ", weak.half_angle)
    standing.agrees("k", weak.factor)
    if (check := standing.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"Over a door in the {door} wall the dome stands as arches spanning {walls}, "
                    f"and the slice {where(weak)} is only {weak.factor:.1f} "
                    "times as thick as the thinnest that stands, under Heyman's "
                    f"{minimum['safety']}. "
                    "Thicken the dome."
                ),
                reference=DOME_SOURCE,
            )
        )
    worst = max(slices, key=lambda s: s.thickness - s.thickest)
    fitting = dome_thickest(dm, worst.at, data["arch_constants"]["source"])
    fitting.agrees("h_s", Q_(worst.rise, "in"))
    fitting.agrees("T_max", Q_(worst.thickest, "in"))
    if (check := fitting.check()).status != "pass":
        # The least rise at which every slice passes, if any below the half-diagonal does
        corner = math.hypot(w, d) / 2
        lo, hi = si(kiln.roof.rise, "in"), corner * 0.999
        passes = all(s.thickness <= s.thickest for s in dome_slices(kiln, rise=hi))
        if passes:
            for _ in range(40):
                mid = (lo + hi) / 2
                ok = all(s.thickness <= s.thickest for s in dome_slices(kiln, rise=mid))
                lo, hi = (lo, mid) if ok else (mid, hi)
        change = f"Raise the dome to at least {hi:.1f} in" if passes else "Raise or thin the dome"
        other = "a side wall" if door in ("front", "back") else "the front or back wall"
        if length > span:  # the slices span the shorter way: turned, they'd rise more
            change += (
                f", or put the door in {other}, so the slices span the longer way and rise more"
            )
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"Over a door in the {door} wall the dome stands as arches spanning {walls}, "
                    f"and they're too thick for their own rise: {worst.thickness:.2f} in "
                    f"{where(worst)}, where HarbisonWalker allows "
                    f"{max(worst.thickest, 0):.2f} in, so the line of thrust would drop out of "
                    f"the dome when it heats. {change}."
                ),
                reference=f"{DOME_SOURCE}; {data['arch_constants']['source']}",
            )
        )
    low, high = rule["general"]
    for m in kinds:
        a, b = rule.get(m.kind, rule["general"])
        low, high = max(low, a), min(high, b)
    steep = [s for s in slices if not low - 1e-9 <= 12 * s.rise / span <= high + 1e-9]
    s = (steep or slices)[0]
    rising = dome_rise(dm, s.at, low, high, rule["source"])
    rising.agrees("h_s", Q_(s.rise, "in"))
    if (check := rising.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"The dome's slices over the door rise {12 * s.rise / span:.2f} in per foot "
                    f"of span {where(s)}; HarbisonWalker gives {low:g}–{high:g} "
                    "in/ft for a roof arch of this ring."
                ),
            )
        )
    # The thrust on the walls the slices span, cold and heated (the heated factor as for a
    # sprung arch, free to rise)
    factors = [heated_thrust_factor(span, s.rise, s.thickness) for s in slices]
    leaving = next((s for s, f in zip(slices, factors, strict=True) if f is None), None)
    if leaving is not None:
        findings.append(
            Finding.failed(
                dome_hot_line(dm, leaving.at).check(),
                message=(
                    f"Hot, the dome's slice {where(leaving)} would push its "
                    "thrust line out of the ring: it is too thick for its rise. Raise the dome "
                    "or thin it."
                ),
                reference=ARCH_THEORY_SOURCE,
            )
        )
        return _unframed(working, findings)
    hot: list[tuple[float, float]] = []
    for s, factor in zip(slices, factors, strict=True):
        assert factor is not None
        cold = cold_thrust_factor(span, s.rise) * s.weight
        hot.append((cold * 12, factor * cold * 12))  # lb per foot of wall
    steps = length / 2 / (len(slices) - 1)
    total = 2 * sum(
        (a + b) / 2 * steps / 12 for (_, a), (_, b) in itertools.pairwise(hot)
    )  # lb along each wall, hot
    peak_cold, peak_hot = max(c for c, _ in hot), max(h for _, h in hot)
    working.append(
        Step(
            name=f"Thrust on {walls}",
            value=(
                f"up to {peak_hot:.0f} lb per foot hot ({peak_cold:.0f} cold); {total:.0f} lb "
                "along each wall"
            ),
            formula=(
                "H = W·(sin α − (1 − cos α)/α) / (2(1 − cos α)) for each slice, W its weight; "
                "× the heated factor"
            ),
            reference=f"{DOME_SOURCE}; {ARCH_THEORY_SOURCE}",
            note="Each layer of the roof counts as weight; only the ring as thickness.",
        )
    )
    # Each check on the slice that decides it: the most heated factor, the thickest, the most thrust
    pushing = max(zip(slices, factors, strict=True), key=lambda p: p[1] or 0.0)
    heating = dome_heated(dm, pushing[0].at, MAX_PRINTED_HEATED, ARCH_THEORY_SOURCE)
    heating.agrees("f", pushing[1] or 0.0)
    if (check := heating.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"Hot, the dome's slices push {pushing[1] or 0.0:.1f} times their cold "
                    f"thrust, more than the {MAX_PRINTED_HEATED:g} times HarbisonWalker prints "
                    "before it marks the stress excessive. A higher dome pushes less."
                ),
            )
        )
    thickest = max(slices, key=lambda s: s.thickness)
    s_over_t = 100 * thickest.thickness / span
    tabled = dome_checked_range(
        dm, thickest.at, data["heated_factor"]["t_over_s"][-1], ARCH_THEORY_SOURCE
    )
    tabled.agrees("T", Q_(thickest.thickness, "in"))
    if (check := tabled.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"The dome's slices reach T/S {s_over_t:.1f} %, past the 10 % of "
                    "HarbisonWalker's heated-arch table, so their hot thrust is worked out from "
                    "statics past what's been checked."
                ),
            )
        )
    peak = slices[max(range(len(hot)), key=lambda i: hot[i][1])]
    return _dome_steel(kiln, dm, peak.at, peak_hot, total, walls, working, findings)


HOT_STEEL_WHERE = (
    "the engine's heat-loss solve: the bearing walls' outside face, steady at the top temperature "
    "(heatloss.py; electric-and-thermal.md §6)"
)


def hot_steel(kiln: Kiln, faces: tuple[str, ...]) -> HotSteel:
    """The frame steel's temperature, the hottest outside face of ``faces`` from the engine's
    own wall solve, and AISC Table A-4.2.1's factors at it (linear between rows)."""
    from kilndesigner.heatloss import heat_loss

    data = steel_data()["hot_steel"]
    loss = heat_loss(kiln)
    kelvin = max(f.layers[-1].cold_side_k for f in loss.faces if f.face in faces)
    t = kelvin * 9 / 5 - 459.67
    return HotSteel(
        temperature=t,
        ky=float(np.interp(t, data["ky_deg_f"], data["ky"])),
        ke=float(np.interp(t, data["ke_deg_f"], data["ke"])),
        fy=float(data["fy_psi"]),
        e=float(data["e_psi"]),
        omega=float(data["omega_b"]),
        source=data["source"],
        where=HOT_STEEL_WHERE,
    )


def angle_allowable(a: Angle, bay: float, hot: HotSteel) -> float:
    """AISC 360-16 §F10 allowable moment (lb·in) of an equal-leg angle about a geometric axis, no
    lateral-torsional restraint over ``bay`` (in), toe in compression, Cb = 1, at ``hot``'s
    temperature: the same chain as frame_checks._aisc_angle_moment (steel-design.md §S4)."""
    fy, e = hot.ky * hot.fy, hot.ke * hot.e
    my = 0.8 * fy * a.sx
    root_term = math.sqrt(1 + 0.88 * (bay * a.t / a.leg**2) ** 2) - 1
    mcr = 0.58 * e * a.leg**4 * a.t / bay**2 * root_term
    if my <= mcr:
        ltb = min((1.92 - 1.17 * math.sqrt(my / mcr)) * my, 1.5 * my)
    else:
        ltb = (0.92 - 0.17 * mcr / my) * mcr
    lam, root = a.leg / a.t, math.sqrt(e / fy)
    sc = 0.8 * a.sx
    if lam <= 0.54 * root:
        leg = 1.5 * my
    elif lam <= 0.91 * root:
        leg = fy * sc * (2.43 - 1.72 * lam / root)
    else:
        leg = 0.71 * e / lam**2 * sc
    return min(1.5 * my, ltb, leg) / hot.omega


DOME_STEEL_SOURCE = "steel-design.md §S4–S5 (derived from AISC 360-16 and the sliced dome)"


def _dome_steel(
    kiln: Kiln,
    dm: DomeInputs,
    at: float,
    peak_hot: float,
    total: float,
    walls: str,
    working: list[Step],
    findings: list[Finding],
) -> FrameDesign:
    """Steel for a sail dome over a whole-wall door: an angle along the top of each wall the
    slices bear on, bending between posts under the slices' peak hot thrust; corner (and, if
    needed, side) posts tied across by rods, the end pair across the door's head and the back
    wall; a ring of the same angle round the springline (steel-design.md §S5)."""
    data = steel_data()
    limit = float(data["binding_stress_psi"])
    o = outside(kiln)
    across = kiln.door_face in ("front", "back")
    bearing = ("left", "right") if across else ("front", "back")
    along = o.depth if across else o.width
    hot = hot_steel(kiln, bearing)
    hs = data["hot_steel"]
    heat = steel_heat(hot, hs["ke_deg_f"][-1], hs["service_deg_f"], hs["service_source"])
    working.append(
        Step(
            name="Frame steel's temperature",
            value=f"{hot.temperature:.0f} °F: Fy × {hot.ky:.2f}, E × {hot.ke:.2f}",
            formula="the bearing walls' outside face; AISC Table A-4.2.1 interpolated",
            reference=f"{HOT_STEEL_WHERE}; {hot.source}",
        )
    )
    if (check := heat.check()).status == "error":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"The dome's buttress steel would run at {hot.temperature:.0f} °F on the "
                    f"outside of {walls}, past the {hs['ke_deg_f'][-1]} °F where AISC's table of "
                    "hot steel's stiffness ends: nothing sourced sizes steel that hot. Insulate "
                    "the walls more, so their outside runs cooler."
                ),
            )
        )
        return _unframed(working, findings)
    if check.status == "warning":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"The dome's buttress steel would run at {hot.temperature:.0f} °F, above the "
                    f"{hs['service_deg_f']} °F Giles keeps carbon steel to in continuous service; "
                    "AISC's reduced strength used here is for fire, a short event. More insulation "
                    "would keep it cooler."
                ),
            )
        )
    # The smallest angle, as for an arch frame (Olsen p.139, p.174)
    from kilndesigner.gas import kiln_top_in

    outside_ft3 = o.width * o.depth * (o.bottom + kiln_top_in(kiln)) / 1728
    floor = angle("L3×3×1/4") if outside_ft3 >= OLSEN_FRAME_FT3 else angle("L2×2×3/16")
    w = peak_hot / 12  # lb per in
    rods = data["rods"]["sizes"][1:]
    posts = _posts_per_side(along, w, floor, limit, rods) if across else 2
    bay = along / (posts - 1)
    share = 0.5 if posts == 2 else 1.0
    moment = w * bay**2 / 8
    fits = [
        a for a in angles()
        if a.leg >= floor.leg and a.t >= floor.t and moment / a.sx <= limit
        and moment <= angle_allowable(a, bay, hot)
    ]  # fmt: skip
    chosen = fits[0] if fits else max(angles(), key=lambda a: a.sx)
    section = AngleSection(chosen.name, chosen.leg, chosen.t, chosen.sx, data["angles"]["source"])
    bending = dome_buttress(dm, at, bay, section, hot, limit, data["binding_stress_source"])
    bending.agrees("H", Q_(peak_hot, "lbf/ft"))
    bending.agrees("M", Q_(moment, "lbf*in"))
    bending.agrees("M_a", Q_(angle_allowable(chosen, bay, hot), "lbf*in"))
    allowed = angle_allowable(chosen, bay, hot)
    working.append(
        Step(
            name="Buttress angle along the bearing walls, hot",
            value=(
                f"{chosen.name}: M = {moment:,.0f} lb·in against AISC's {allowed:,.0f} lb·in "
                f"allowable at {hot.temperature:.0f} °F; {moment / chosen.sx:,.0f} psi"
            ),
            formula=(
                "M = H ℓ²/8 (the peak thrust all along a bay); M_a = M_n/Ω_b, M_n the least of "
                "1.5M_y, lateral-torsional buckling (F10-2/3, M_cr from F10-5a) and leg local "
                "buckling (F10-6/7), Fy and E reduced to the steel's temperature; and M/S_x ≤ "
                "12,000 psi"
            ),
            inputs={"H": f"{peak_hot:.0f} lb/ft", "bay ℓ": f"{bay:.1f} in", "posts": str(posts)},
            reference=f"{hot.source}; {data['binding_stress_source']}; {DOME_STEEL_SOURCE}",
            note=(
                "Unbraced along the bay, toe in compression: the cautious case of F10; masonry "
                "against the angle would brace it."
            ),
        )
    )
    if (check := bending.check()).status != "pass" or not fits:
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"No listed angle up to {chosen.name} carries the dome's {peak_hot:.0f} lb "
                    f"per foot of hot thrust over {bay:.0f} in between posts at "
                    f"{hot.temperature:.0f} °F. "
                    + ("Raise the dome or lighten it." if across else
                       "Put the door in the front or back wall, so posts can go along the sides.")
                ),
            )
        )  # fmt: skip
    per_rod = w * bay * share
    rod = rods[-1]
    for size in rods:
        if per_rod / size["stress_area"] <= limit:
            rod = size
            break
    tied = dome_rod(dm, at, bay, share, (rod["name"], rod["stress_area"]), limit,
                    (data["rods"]["source"], data["binding_stress_source"]))  # fmt: skip
    tied.agrees("P", Q_(per_rod, "lbf"))
    if (check := tied.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"No rod up to {rod['name']} carries the dome's thrust: the busiest takes "
                    f"{per_rod:,.0f} lb."
                ),
            )
        )
    working.append(
        Step(
            name="Tie rods across the bearing walls",
            value=f"{rod['name']}: {per_rod:,.0f} lb, {per_rod / rod['stress_area']:,.0f} psi",
            formula="H × bay × share ÷ tensile stress area",
            inputs={"along each wall, hot": f"{total:.0f} lb"},
            reference=f"{data['rods']['source']}; {data['binding_stress_source']}; {DOME_SOURCE}",
            note=(
                "The end pair runs across the door's head and across the back wall. Under the "
                "sliced dome nothing bears on the door wall, so the angle across the door's head "
                "is a tie and a frame member, not a lintel."
            ),
        )
    )
    leg = chosen.leg
    members = [
        Member(part="corner posts" if posts == 2 else "posts, at the corners and along the sides",
               steel=chosen.name, count=2 * posts, length_in=o.bottom + o.wall_top,
               source=DOME_STEEL_SOURCE),
        Member(part="buttresses along the dome's bearing walls", steel=chosen.name, count=2,
               length_in=along + 2 * leg, source=DOME_STEEL_SOURCE),
        Member(part="ring angles across the door's head and the back", steel=chosen.name,
               count=2, length_in=(o.width if across else o.depth) + 2 * leg,
               source=DOME_STEEL_SOURCE),
        *_ring_of(FLAT_BAR, "bottom cross-members", o, leg, PITELKA),
        Member(part="tie rods", steel=f"{rod['name']} threaded rod", count=posts,
               length_in=(o.width if across else o.depth) + 2 * leg + 4,
               source=f"length: {MERRILL}"),
    ]  # fmt: skip
    if fits and bending.check().status == "pass":
        findings.append(
            Finding(
                level="info",
                message=(
                    f"The dome needs a frame: {chosen.name} angle along the tops of {walls} and "
                    f"round the springline, {2 * posts} posts, and {posts} {rod['name']} tie rods "
                    f"({per_rod:,.0f} lb on the busiest), the steel at about "
                    f"{hot.temperature:.0f} °F. Fit it before the form comes out."
                ),
                reference=DOME_STEEL_SOURCE,
                check=bending.check(),
            )
        )
    if tied.check().status == "pass":
        findings.append(
            Finding(
                level="info",
                message=(
                    f"The end pair of {rod['name']} rods ties across the door's head and the back "
                    f"wall, {per_rod:,.0f} lb on the busiest, hot."
                ),
                reference=DOME_STEEL_SOURCE,
                check=tied.check(),
            )
        )
    return FrameDesign(
        kind="dome frame", angle=chosen.name, angle_leg_in=chosen.leg, angle_t_in=chosen.t,
        rod=rod["name"], rod_d_in=rod["d"], thrust=f"{peak_hot:.0f} lb per foot on {walls}, hot",
        members=members, working=working, findings=findings, posts=posts,
    )  # fmt: skip


MASONRY_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.53 (Fig. 2-35B: a battered wall carries an arch's thrust "
    "without steel), p.97 (bracing a chamber kiln's firebox and front chamber 'is a must'), p.186 "
    "(walls buttressed with earth, rocks and concrete under a cast dome)"
)


def _held_by_masonry(kiln: Kiln) -> FrameDesign:
    """A roof whose thrust the design gives to masonry or earth: no steel is sized. A sprung
    arch's thrust is worked out, so the builder knows what the buttress holds."""
    working: list[Step] = []
    thrust: str | None = None
    roof = kiln.roof
    if isinstance(roof, SprungArch) and kiln.chamber.shape == "box":
        # Chambers in a row: each arch spans its chamber's depth, along the draft (run_parts.py)
        along = arches_along(kiln)
        span = si(kiln.chamber.depth if along else kiln.chamber.width, "in")
        from kilndesigner.shape import along_arch

        arch = along_arch(kiln, "in") if along else Arch(span, si(roof.rise, "in"))
        load = _arch_load(kiln, arch)
        cold = cold_thrust_factor(span, arch.rise) * load.weight
        heated = heated_thrust_factor(span, arch.rise, load.ring)
        if arch.drop:  # springing unevenly: no heated factor printed, so the largest is taken
            cold, step = uneven_cold(arch, load.weight)
            heated = None
            working.append(step)
        hot = (heated if heated is not None else MAX_PRINTED_HEATED) * cold
        hot = min(hot, MAX_PRINTED_HEATED * cold)
        thrust = f"{hot:.0f} lb per foot of arch, hot ({cold:.0f} cold)"
        working.append(
            Step(
                name="Thrust the masonry holds",
                value=thrust,
                formula="H = W·(sin θ − (1 − cos θ)/θ) / (2(1 − cos θ)); hot, × the heated factor",
                reference=f"{ARCH_THEORY_SOURCE}; {CAPPED}",
            )
        )
    if isinstance(roof, Dome) and kiln.chamber.outline is not None:
        thrust, steps = _curved_dome_thrust(kiln)
        working += steps
    findings = [
        Finding(
            level="info",
            message=(
                "The roof's thrust is carried by the kiln's masonry (thick or battered walls, "
                "buttresses, or earth), as the design says, so no steel frame is sized. Olsen: a "
                "battered wall can carry an arch without steel; brace a chamber kiln's firebox "
                "and front chamber."
            ),
            reference=MASONRY_SOURCE,
        )
    ]
    return FrameDesign(
        kind=NO_FRAME, angle=None, angle_leg_in=0, angle_t_in=0, rod=None, rod_d_in=0,
        thrust=thrust, members=[], working=working, findings=findings,
    )  # fmt: skip


ROW_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.94–95 (the arches throw their thrust onto the common wall), "
    "p.97 (bracing a chamber kiln's firebox and front chamber 'is a must')"
)


def uneven_cold(arch: Arch, weight: float) -> tuple[float, Step]:
    """An arch springing unevenly (in, lb per foot): its cold thrust by a line of thrust through
    both springings at their own heights (vault.THRUST_LINE), with its working, shown beside the
    halves' moments about the crown it replaces. Hot stays × HarbisonWalker's largest factor."""
    from kilndesigner.vault import THRUST_LINE, UNEVEN, thrust_line_thrust, uneven_thrust

    before, *_ = uneven_thrust(arch, weight)
    cold, front, back = thrust_line_thrust(arch, weight)
    return cold, Step(
        name="The uneven arch's cold thrust, by a line of thrust through both springings",
        value=f"H = {cold:.1f} lb per foot of arch (each half about the crown: {before:.1f}); "
        f"V = {front:.1f} lb at the front, {back:.1f} lb at the back",
        formula=(
            "V_b·(s_f + s_b) + H·δ = W_f·(s_f − c_f) + W_b·(s_f + c_b) (the whole arch about the "
            "front springing); V_b·s_b = H·f_b + W_b·c_b (the back half about the crown); "
            "s = sin φ, f = 1 − cos φ, c = (1 − cos φ)/φ, δ = drop/r, all over r"
        ),
        inputs={
            "W, the arch's weight": f"{weight:.1f} lb per foot",
            "φ_f, φ_b": f"{math.degrees(arch.front_angle):.2f}°, "
            f"{math.degrees(arch.back_angle):.2f}°",
            "r": f"{arch.radius:.2f} in",
            "drop δ·r, the front springing below the back's": f"{arch.drop:g} in",
        },
        reference=f"{THRUST_LINE}; {ARCH_THEORY_SOURCE}; {UNEVEN}",
        note=(
            "The two ways are the same statics written differently and agree; this one takes the "
            "springings at their own heights directly. Hot, HarbisonWalker's largest printed "
            "factor is kept: no heated factor for unequal springings is sourced "
            "(blocked-items.md §9), and the largest is the safe side."
        ),
    )


def _row_arches(kiln: Kiln) -> FrameDesign:
    """Chambers in a row, each under an arch spanning its depth along the draft (run_parts.py).
    Each wall between chambers takes the thrust of the arches either side, which push against
    each other (Olsen p.94–95); the front and back walls take one arch's thrust each, across the
    kiln's width, and want bracing (p.97). No source here sizes that bracing, so the thrust is
    worked out and no steel is sized."""
    assert isinstance(kiln.roof, SprungArch)
    from kilndesigner.shape import along_arch
    from kilndesigner.vault import UNEVEN

    depth, width = si(kiln.chamber.depth, "in"), si(kiln.chamber.width, "in")
    arch = along_arch(kiln, "in")
    load = _arch_load(kiln, arch)
    checks: list[Step] = []
    if arch.drop:
        # Springing unevenly: no heated factor is printed for it, so HarbisonWalker's largest
        cold, step = uneven_cold(arch, load.weight)
        checks.append(step)
        heated = None
    else:
        cold = cold_thrust_factor(depth, arch.rise) * load.weight
        heated = heated_thrust_factor(depth, arch.rise, load.ring)
    hot = min((heated if heated is not None else MAX_PRINTED_HEATED) * cold,
              MAX_PRINTED_HEATED * cold)  # fmt: skip
    whole = hot * width / 12
    thrust = (
        f"{hot:.0f} lb per foot of arch, hot ({cold:.0f} cold): {whole:,.0f} lb on each end wall"
    )
    inputs = {"span": f"{depth:g} in", "rise": f"{arch.rise:g} in", "width": f"{width:g} in"}
    if arch.drop:
        inputs["front springline below the back's"] = f"{arch.drop:g} in"
    working = [
        *checks,
        Step(
            name="Thrust on each end wall",
            value=thrust,
            formula=(
                "H, cold, by the line of thrust through both springings (above); hot, × "
                "HarbisonWalker's largest factor; × the kiln's width"
                if arch.drop
                else "H = W·(sin θ − (1 − cos θ)/θ) / (2(1 − cos θ)) per foot, hot, × the kiln's "
                "width; the arch spans one chamber's depth"
            ),
            inputs=inputs,
            reference=f"{ARCH_THEORY_SOURCE}; {CAPPED}; {ROW_SOURCE}"
            + (f"; {UNEVEN}" if arch.drop else ""),
            note=(
                "The arch springs at different heights, outside HarbisonWalker's heated-arch "
                "method (a level arch's), so its largest printed factor is taken: the cautious "
                "side."
                if arch.drop
                else None
            ),
        ),
    ]
    between = (
        "The walls between chambers take the arches either side, which push against each other "
        "(Olsen p.94–95); the "
        if kiln.chamber.chambers > 1
        else "The "
    )
    findings = [
        Finding(
            level="info",
            message=(
                f"{'Each chamber' if kiln.chamber.chambers > 1 else 'The chamber'}'s arch spans "
                "its depth, along the draft, so its thrust falls on the walls before and behind "
                f"it, not on the side walls. {between}front and back walls each take one arch's "
                f"thrust, {whole:,.0f} lb hot across the kiln's width. Brace them: Olsen calls "
                "bracing a chamber kiln's firebox and front chamber 'a must' (p.97). No source "
                "here sizes that bracing, so no steel frame is sized; or hold the ends with "
                "masonry (roof.buttressed)."
            ),
            reference=ROW_SOURCE,
        )
    ]
    from kilndesigner.vault import along_statics

    steps, found = along_statics(kiln)
    working += steps
    findings += found
    return FrameDesign(
        kind=NO_FRAME, angle=None, angle_leg_in=0, angle_t_in=0, rod=None, rod_d_in=0,
        thrust=thrust, members=[], working=working, findings=findings,
    )  # fmt: skip


ALONG_FRAME = (
    "the sprung-arch frame turned to the arch's span: corner angles on the end walls, buttress "
    "angles across them at the springing, tie rods running the chamber's depth over the arch "
    "(kiln-hardware.md §4.1–4.2 [S11] [S20]); Bowen Mountain's corner angles and bars over the "
    "arch, read by the user from the construction photos (olsen-kilns.md, 2026-10-31)"
)
MULTI_RING = (
    "the roof's ring layers taken as one ring, their thicknesses summed, as the engine takes any "
    "ring of several layers (frame_checks: T = t_1 + t_2 + …); no source here checks whether "
    "rings laid one on another without bond act as one"
)


BUILDING_FRAME = (
    "the designer's reading: the steel holds the arch while it is built and the mortar sets, the "
    "mortared masonry and the platform it is built into in service (roof.building_frame; Bowen "
    "Mountain, the user, 2026-10-31). No source in docs/research quantifies the restraint mortar "
    "or a platform gives an end wall"
)


def _building_frame(kiln: Kiln) -> FrameDesign:
    """A sprung arch the masonry holds in service, its steel used while building only
    (``roof.building_frame``): the frame is sized as the in-service one would be, the cautious
    side for a cold arch on its form, and listed; the in-service working is the masonry's, its
    walls' statics reported as they stand."""
    assert isinstance(kiln.roof, SprungArch)
    roof = kiln.roof.model_copy(update={"buttressed": False, "building_frame": False})
    framed = kiln.model_copy(update={"roof": roof})
    steel = _along_frame(framed, building=True) if roof.along else _design_frame(framed)
    service = _held_by_masonry(kiln)
    findings = [
        f
        if not f.message.startswith("Weld the frame")
        else f.model_copy(
            update={
                "message": (
                    "Weld the frame and fit it before the arch form comes out: it holds the arch "
                    "while it is built and the mortar sets. In service the design takes the "
                    "mortared masonry and its platform as holding the arch, and no check here "
                    "counts on the steel."
                )
            }
        )
        for f in steel.findings
    ]
    findings.append(
        Finding(
            level="info",
            message=(
                "The frame is for building: it is sized for the arch's hot thrust, the cautious "
                "side for a cold arch on its form, so it would also carry the arch fired if left "
                "on. In service the roof is taken as buttressed by the mortared masonry and the "
                "platform it is built into, the designer's reason; no source here quantifies "
                "that restraint, so it is the design's judgment, not a check."
            ),
            reference=BUILDING_FRAME,
        )
    )
    members = [m.model_copy(update={"part": f"{m.part}, for building"}) for m in steel.members]
    return steel.model_copy(
        update={
            "members": members,
            "working": [*steel.working, *service.working],
            "findings": findings,
        }
    )


def _along_frame(kiln: Kiln, *, building: bool = False) -> FrameDesign:
    """One chamber's arch along its depth (``roof.along``) held by steel: the sprung-arch frame
    turned to the arch's span. The end walls take the thrust, so the buttress angles lie across
    them at the springing between corner posts (and posts between, where the steel needs them),
    and the tie rods run the chamber's depth over the arch. The thrust per foot of the kiln's
    width is the arch's: springing unevenly, the uneven three-hinged arch's, × HarbisonWalker's
    largest heated factor, as no heated factor is printed for it."""
    assert isinstance(kiln.roof, SprungArch)
    from kilndesigner.frame_checks import GivenCold
    from kilndesigner.shape import along_arch
    from kilndesigner.vault import THRUST_LINE, UNEVEN, along_inputs, along_statics

    o = outside(kiln)
    data = steel_data()
    limit = float(data["binding_stress_psi"])
    whole = along_arch(kiln, "in")
    a = along_inputs(kiln)
    load = _arch_load(kiln, whole)
    working: list[Step] = []
    findings: list[Finding] = []
    if load.loose:
        findings.append(
            Finding.failed(
                loose_ring("arch", list(load.loose), data["rise_per_foot"]["source"]).check(),
                message=(
                    f"The arch's ring includes {' and '.join(load.loose)}, which can't carry an "
                    "arch's thrust: the ring must be brick or castable. Set the roof's ring to the "
                    "layers that are."
                ),
            )
        )
        return _unframed(working, findings)
    h = si(kiln.chamber.height, "in")
    roof_t = sum(si(x.thickness, "in") for x in kiln.lining.for_face("roof"))
    centre = h + whole.rise - whole.radius
    skewback = max(
        centre + (whole.radius + load.ring) * math.cos(p)
        for p in (whole.front_angle, whole.back_angle)
    )
    crown = h + whole.rise + roof_t  # the roof's outside at the crown, where the rods run over
    outside_ft3 = o.width * o.depth * (o.bottom + crown) / 1728
    big = outside_ft3 >= OLSEN_FRAME_FT3
    floor = angle("L3×3×1/4") if big else angle("L2×2×3/16")
    working.append(
        Step(
            name="Smallest frame angle",
            value=floor.name,
            inputs={"outside, to the roof's crown": f"{outside_ft3:.0f} ft³"},
            reference=OLSEN_FRAME,
            note=(
                "Olsen's corner posts for a 5 × 5 × 6 ft kiln, 'larger (stronger), but not smaller'"
                if big
                else "Olsen's bolted fast-fire frame; smaller kilns can use 3/16 in angle"
            ),
        )
    )
    rings = kiln.lining.for_face("roof")[: kiln.roof.ring]
    working.append(
        Step(
            name="Arch ring",
            value=f"{load.ring:g} in"
            + (f", {len(rings)} rings laid one on another" if len(rings) > 1 else ""),
            inputs={
                f"ring {i + 1}": f"{si(x.thickness, 'in'):g} in {x.material}"
                for i, x in enumerate(rings)
            },
            reference=MULTI_RING if len(rings) > 1 else None,
            note="The layers laid over the ring are its load, not part of it.",
        )
    )
    given: GivenCold | None = None
    capped: float | None = MAX_PRINTED_HEATED
    factor = MAX_PRINTED_HEATED
    if whole.drop:
        cold, step = uneven_cold(whole, load.weight)
        working.append(step)
        given = GivenCold(
            cold, f"a line of thrust through both springings (vault.py); {THRUST_LINE}; {UNEVEN}"
        )
        why = (
            "The arch springs at different heights, outside HarbisonWalker's heated-arch method "
            "(a level arch's), so its largest printed factor is taken: the cautious side."
        )
    else:
        cold = cold_thrust_factor(a.span, a.rise) * load.weight
        heated = heated_thrust_factor(a.span, a.rise, load.ring)
        cos_half = math.cos(whole.half_angle)
        thickest = (a.rise - a.span / 48) / cos_half if cos_half > 1e-9 else math.inf
        if (
            heated is not None
            and load.ring <= thickest + 1e-9
            and heated <= MAX_PRINTED_HEATED + 1e-9
            and hot_thrust_line(a).check().status == "pass"
        ):
            capped, factor = None, heated
            why = f"Heyman's maximum thrust, the arch pressed between the steel: × {heated:.2f}."
        else:
            why = (
                "The ring is too thick for its rise for HarbisonWalker's heated-arch method, so "
                "its largest printed factor is taken."
            )
    hot = cold * factor
    width = o.width
    working.append(
        Step(
            name="Thrust on each end wall",
            value=(
                f"{hot:.0f} lb per foot of the kiln's width, hot ({cold:.0f} cold): "
                f"{hot * si(kiln.chamber.width, 'in') / 12:,.0f} lb across the chamber"
            ),
            formula=(
                "H, cold, by the line of thrust through both springings (above); hot, × "
                "HarbisonWalker's largest factor"
                if whole.drop
                else "H = W·(sin θ − (1 − cos θ)/θ) / (2(1 − cos θ)); hot, × the heated factor"
            ),
            inputs={"W, the arch's weight per foot": f"{load.weight:.1f} lb/ft",
                    "span, the chamber's depth": f"{whole.span:g} in"},
            reference=f"{ARCH_THEORY_SOURCE}; {CAPPED}" + (f"; {UNEVEN}" if whole.drop else ""),
            note=why,
        )
    )  # fmt: skip
    rods = data["rods"]["sizes"][1:]  # ½-13 and up, as the sprung-arch frame
    posts = _posts_per_side(width, hot / 12, floor, limit, rods)
    bay = width / (posts - 1)
    share = 0.5 if posts == 2 else 1.0
    moment = (hot / 12) * bay**2 / 8
    per_rod = hot * (bay / 12) * share
    # The posts: pinned at the foot on the platform (or tied by the bottom ring), held at the rods
    # over the crown, the buttress's end load between
    above = si(kiln.roof.rods_above_crown, "in") if kiln.roof.rods_above_crown is not None else 0.0
    span_post = o.bottom + crown + above
    up = o.bottom + skewback
    post_moment = per_rod * up * (span_post - up) / span_post
    steel = hot_steel(kiln, ("front", "back"))
    hs = data["hot_steel"]
    heat = steel_heat(steel, hs["ke_deg_f"][-1], hs["service_deg_f"], hs["service_source"])
    if (check := heat.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"The frame's posts would run at {steel.temperature:.0f} °F on the end walls' "
                    "outside, past where AISC's hot-steel table or Giles's continuous service "
                    "reaches: their bending check is past what's been checked. Insulate the end "
                    "walls more."
                ),
            )
        )
    fits = [
        x for x in angles()
        if x.sx >= moment / limit and x.leg >= floor.leg and x.t >= floor.t
        and post_moment / x.sx <= limit and post_moment <= angle_allowable(x, span_post, steel)
    ]  # fmt: skip
    biggest = max(angles(), key=lambda x: x.sx)
    chosen = fits[0] if fits else biggest
    bending = buttress_bending(
        a, bay, share, chosen.name, chosen.sx, limit, None,
        (data["angles"]["source"], data["binding_stress_source"]), capped, given,
    )  # fmt: skip
    bending.agrees("M", Q_(moment, "lbf*in"))
    if (check := bending.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"No angle up to {biggest.name} carries the arch's thrust across the end wall "
                    f"over {bay:.0f} in between posts, the shortest bay the engine sets "
                    f"({MIN_BAY:g} in or more). Lighten the arch, or hold the end walls with "
                    "masonry (buttressed)."
                ),
            )
        )
    working.append(
        Step(
            name=(
                "Posts on each end wall"
                if posts == 2
                else f"Posts on each end wall: {posts}, {bay:.1f} in apart"
            ),
            value=f"{posts} each end, the corners included",
            formula="the fewest posts for which a listed angle and rod carry the thrust between",
            reference="kiln-hardware.md §4.1–4.2 [S20] [S34] (derived)",
        )
    )
    working.append(
        Step(
            name="Buttress angle across each end wall, bending",
            value=f"needs Sx ≥ {moment / limit:.3f} in³; {chosen.name} has {chosen.sx:.3f} in³",
            formula="M = wL²/8, Sx = M ÷ 12,000 psi (a simple beam between the posts)",
            inputs={"w": f"{hot / 12:.2f} lb/in", "L": f"{bay:.1f} in",
                    "M": f"{moment:,.0f} lb·in"},
            reference=f"{data['binding_stress_source']}; AISC Sx, kiln-hardware.md §4.7.1 [S28]",
            note="A cautious first check, derived in kiln-hardware.md §4.5; not a sourced rule.",
        )
    )  # fmt: skip
    rod = rods[-1]
    for size in rods:
        if per_rod / size["stress_area"] <= limit:
            rod = size
            break
    tied = rod_stress(
        a, bay, share, rod["name"], rod["stress_area"], limit, None,
        (data["rods"]["source"], data["binding_stress_source"]), capped, given,
    )  # fmt: skip
    tied.agrees("P", Q_(per_rod, "lbf"))
    if (check := tied.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"No rod up to {rod['name']} carries the arch's thrust: the busiest takes "
                    f"{per_rod:,.0f} lb, {per_rod / rod['stress_area']:,.0f} psi, hot."
                ),
                reference=f"{data['rods']['source']}; {data['binding_stress_source']}",
            )
        )
    working.append(
        Step(
            name=f"Tie rods along the chamber's depth, over the arch, {posts}",
            value=f"{rod['name']}: {per_rod / rod['stress_area']:,.0f} psi",
            formula="thrust × the bay the busiest rod ties ÷ tensile stress area",
            inputs={"load on the busiest rod": f"{per_rod:,.0f} lb",
                    "stress area": f"{rod['stress_area']} in²"},
            reference=f"{data['rods']['source']}; {data['binding_stress_source']}",
        )
    )  # fmt: skip
    # The rods run over the arch, above the buttress: each post carries the buttress's end
    # load up to its rod as a beam pinned at its foot, checked as the dome's buttress (AISC F10)
    section = AngleSection(chosen.name, chosen.leg, chosen.t, chosen.sx, data["angles"]["source"])
    posted = post_bending(
        per_rod, up, span_post, section, steel, limit,
        ("the busiest rod's load (above)", data["binding_stress_source"]),
    )  # fmt: skip
    posted.agrees("M", Q_(post_moment, "lbf*in"))
    posted.agrees("M_a", Q_(angle_allowable(chosen, span_post, steel), "lbf*in"))
    if (check := posted.check()).status != "pass":
        # The highest rods the chosen angle carries: P·a·(L − a)/L ≤ M_lim, so
        # L ≤ P·a²/(P·a − M_lim) when P·a > M_lim
        m_lim = min(limit * chosen.sx, angle_allowable(chosen, span_post, steel))
        highest = (
            per_rod * up**2 / (per_rod * up - m_lim) - o.bottom - crown
            if per_rod * up > m_lim
            else math.inf
        )
        lower = (
            f"run the rods at most {highest:.1f} in over the crown"
            if highest >= 0
            else "run the rods at the buttress's height"
        )
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"The posts bend {post_moment:,.0f} lb·in between their feet and the rods "
                    f"{span_post:.0f} in up: {post_moment / chosen.sx:,.0f} psi in "
                    f"{chosen.name}, the heaviest listed angle, against AISC's "
                    f"{angle_allowable(chosen, span_post, steel):,.0f} lb·in hot and "
                    f"HarbisonWalker's {limit:,.0f} psi for steel that may run hot. With it, "
                    f"{lower}, or add posts between the corners."
                ),
            )
        )
    on_platform = kiln.chamber.foundation is not None
    shear = per_rod * (span_post - up) / span_post
    working.append(
        Step(
            name="Posts between the foot and the rod, in bending",
            value=(
                f"{post_moment:,.0f} lb·in against AISC's "
                f"{angle_allowable(chosen, span_post, steel):,.0f} lb·in allowable at "
                f"{steel.temperature:.0f} °F; {post_moment / chosen.sx:,.0f} psi in {chosen.name}"
            ),
            formula=(
                "M = P·a·(L − a)/L, a point load on a beam pinned at both ends; M_a = M_n/Ω_b by "
                "AISC 360-16 F10, unbraced over L, Fy and E at the steel's temperature; and "
                "M/S_x ≤ 12,000 psi"
            ),
            inputs={"P, the busiest post's load": f"{per_rod:,.0f} lb",
                    "a, the buttress above the post's foot": f"{up:.1f} in",
                    "L, the foot to the rod": f"{span_post:.1f} in",
                    "rods above the roof's crown": f"{above:g} in"},
            reference=f"statics of a simple beam (derived); {steel.source}; "
            f"{data['binding_stress_source']}; {DOME_STEEL_SOURCE}",
            note=(
                "The foot is taken pinned, the safe side: no source here gives the fixity of a "
                "post anchored in or bolted to a platform. "
                + ("" if kiln.roof.rods_above_crown is not None else
                   "The rods' height isn't given, so they're taken at the roof's crown. ")
                + "Rods at the buttress's height would take the post's bending away."
            ),
        )
    )  # fmt: skip
    if on_platform:
        working.append(
            Step(
                name="Each post's foot on the platform",
                value=f"{shear:,.0f} lb outward, hot; no uplift from the thrust",
                formula="V_f = P·(L − a)/L, the lower reaction of the pinned post",
                inputs={"P": f"{per_rod:,.0f} lb", "a": f"{up:.1f} in", "L": f"{span_post:.1f} in"},
                reference="statics of a simple beam (derived)",
                note=(
                    "The thrust is level, so it lifts no foot; the steel's own weight bears down. "
                    "The rest of P, P·a/L, goes to the rod, which is sized for the whole P (the "
                    "safe side). The anchors aren't sized: no method for anchors in concrete "
                    "(ACI 318 ch. 17) is in docs/research, so a builder sizes them for this shear."
                ),
            )
        )  # fmt: skip
        findings.append(
            Finding(
                level="info",
                message=(
                    f"The posts' feet stand in or are bolted to the platform, taken as pinned: "
                    f"each must carry {shear:,.0f} lb outward, hot, with no uplift from the arch. "
                    "Size the anchors for it: no anchor method is sourced here."
                ),
                reference="statics of a simple beam (derived); the user, 2026-10-31",
            )
        )
    statics, found = along_statics(kiln, framed="building" if building else True)
    working += statics
    findings += found
    leg = chosen.leg
    members = [
        Member(part="corner posts" if posts == 2 else "posts on the end walls, corners included",
               steel=chosen.name, count=2 * posts, length_in=span_post, source=ALONG_FRAME),
        Member(part="buttresses across the end walls at the springing", steel=chosen.name,
               count=2, length_in=o.width + 2 * leg, source=ALONG_FRAME),
        *([] if on_platform else _ring_of(FLAT_BAR, "bottom cross-members", o, leg, PITELKA)),
        Member(part="tie rods along the depth, over the arch", steel=f"{rod['name']} threaded rod",
               count=posts, length_in=o.depth + 2 * leg + 4, source=f"length: {MERRILL}"),
    ]  # fmt: skip
    if not any(f.level == "error" for f in findings):
        findings.append(
            Finding(
                level="info",
                message=(
                    "Weld the frame and fit it before the arch form comes out: the steel is what "
                    "holds the arch up."
                ),
                reference="kiln-hardware.md §4.1–4.2 [S11] [S21]",
            )
        )
    return FrameDesign(
        kind="arch frame", angle=chosen.name, angle_leg_in=chosen.leg, angle_t_in=chosen.t,
        rod=rod["name"], rod_d_in=rod["d"], thrust=f"{hot:.0f} lb per foot of the kiln's width",
        members=members, working=working, findings=findings, posts=posts,
    )  # fmt: skip


def _round_frame(kiln: Kiln) -> FrameDesign:
    """A round kiln: its wall is a ring, which holds any dome on it; makers band it with iron (the
    Breda bottle kiln, Olsen p.167; Sèvres, p.168–169). The band isn't sized here."""
    findings = [
        Finding(
            level="info",
            message=(
                "A round kiln's wall is a ring that holds any dome on it, and builders band it "
                "with iron (Olsen's Breda bottle kiln, p.167): no band is sized here."
            ),
            reference="Olsen, The Kiln Book, 4th ed., p.167–169",
        )
    ]
    working: list[Step] = []
    thrust = None
    if kiln.heat.electric is not None:
        findings = [_electric_bands(kiln)]
    elif isinstance(kiln.roof, Dome):
        ring = round_dome_ring(kiln)
        if ring is None:
            findings.append(
                Finding(
                    level="info",
                    message=(
                        "The dome rises more than half the chamber's width, past a hemisphere: "
                        "its thrust isn't worked out (membrane theory here is checked to a "
                        "hemisphere only)."
                    ),
                    reference=MEMBRANE,
                )
            )
        else:
            working, thrust = ring.steps, ring.thrust
            findings.append(ring.finding())
    return FrameDesign(
        kind=NO_FRAME, angle=None, angle_leg_in=0, angle_t_in=0, rod=None, rod_d_in=0,
        thrust=thrust, members=[], working=working, findings=findings,
    )  # fmt: skip


MEMBRANE = (
    "Timoshenko, Theory of Plates and Shells, §106, eq. (257), membrane forces of a spherical "
    "dome under its own weight; the edge ring's force H = a₀·N_α·cos α₀ (domes-over-doors.md §D1)"
)
NO_TENSION = 51.83
"""Degrees from the crown past which the membrane state has hoop tension (Timoshenko, 51°50′;
Lau's no-tension solutions reach α ≤ 51.8°, domes-over-doors.md §D1)."""


@dataclass(frozen=True)
class DomeRing:
    """A round dome's membrane forces at its springing, imperial: the meridian thrust (lb per ft
    of the springing circle), its outward part, the ring tension the wall or a band holds (lb),
    and the hoop force in the shell there (lb per ft; positive is tension)."""

    alpha: float  # degrees, the springing from the crown
    meridian: float
    per_foot: float
    ring: float
    hoop: float
    steps: list[Step]
    cracked: LuneThrust | None = None

    @property
    def thrust(self) -> str:
        """The push the frame reports: past 51.8°, the cracked dome's least push if Lau's range
        covers it, else the membrane push."""
        c = self.cracked
        if c is not None and c.per_foot is not None:
            return f"at least {c.per_foot:.0f} lb per foot of the wall's top (cracked into lunes)"
        return f"{self.per_foot:.0f} lb per foot of the wall's top"

    def finding(self) -> Finding:
        text = (
            f"The dome pushes out {self.per_foot:,.0f} lb per foot round the wall's top; the "
            f"wall's ring, or an iron band round it, holds that as {self.ring:,.0f} lb of ring "
            "tension (membrane theory, the dome's own weight). No band is sized: no source here "
            "gives an allowable for a hot kiln's band."
        )
        c = self.cracked
        if c is None:
            return Finding(level="info", message=text, reference=MEMBRANE)
        text += (
            f" The dome springs {self.alpha:.1f}° from its crown, past the {NO_TENSION}° "
            f"where the membrane state turns to hoop tension ({self.hoop:,.0f} lb per foot "
            "at the springing), which mortared brick doesn't carry: it cracks along its "
            "meridians and stands as lunes."
        )
        if c.per_foot is None or c.ring is None or c.h_over_w is None:
            text += (
                f" Its t/R of {c.t_over_r:.3f} is outside {LAU_T_R[0]}–{LAU_T_R[1]}, where "
                "Lau's lune statics are checked, so the cracked dome's push isn't worked out; "
                "the membrane numbers above aren't a design value for it."
            )
            return Finding(level="info", message=text, reference=f"{MEMBRANE}; {LAU}")
        text += (
            f" Cracked so, it pushes at least {c.per_foot:,.0f} lb per foot, a ring tension of "
            f"at least {c.ring:,.0f} lb (Lau's lune statics: H/W = {c.h_over_w:.3f} of a "
            "lune's weight; the membrane push above leans on hoop tension). That is a least "
            "value: a dome pushed in by its wall can thrust "
            "many times more (430 % of its weight for a hemisphere, SAHC 2020)."
        )
        if c.t_over_r < LAU_THIN:
            text += (
                f" At t/R = {c.t_over_r:.3f} it is thinner than the {LAU_THIN} Lau finds a "
                "hemisphere needs with no hoop force between its lunes (0.041 with them); a "
                "shallower dome needs less (his Fig. 3.13), but the equations alone don't show "
                "it stands (p.59)."
            )
        return Finding(level="info", message=text, reference=f"{MEMBRANE}; {LAU}")


def membrane(a: float, q: float, alpha: float) -> tuple[float, float, float, float]:
    """A spherical cap's membrane forces at its edge (Timoshenko §106), in any consistent units:
    radius a, weight q per unit area, the edge α radians from the crown. The meridian
    compression N_α = aq/(1 + cos α), its outward part N_α·cos α, the ring force a·sin α ×
    that, and the hoop force aq(1/(1 + cos α) − cos α), tension when positive."""
    meridian = a * q / (1 + math.cos(alpha))
    out = meridian * math.cos(alpha)
    return (
        meridian,
        out,
        a * math.sin(alpha) * out,
        a * q * (1 / (1 + math.cos(alpha)) - math.cos(alpha)),
    )


def round_dome_ring(kiln: Kiln) -> DomeRing | None:
    """The membrane forces at a round dome's springing (Timoshenko §106): a spherical cap of
    radius a, springing α₀ from its crown, weighing q per unit of its surface. N_α = −aq/(1 +
    cos α₀) along the meridian, its outward part N_α·cos α₀ per unit of the springing circle,
    the ring force a₀·N_α·cos α₀ with a₀ = a·sin α₀, and the hoop force aq(1/(1 + cos α₀) −
    cos α₀). a is the mid-surface's radius; q is Σ density × thickness of the roof's layers."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.shape import RoundDome

    assert isinstance(kiln.roof, Dome)
    dome = RoundDome(si(kiln.chamber.width, "ft"), si(kiln.roof.rise, "ft"))
    layers = [
        (si(parse_quantity(resolve_material(kiln, x.material).density), "lb/ft**3"),
         si(x.thickness, "ft"))
        for x in kiln.lining.for_face("roof")
    ]  # fmt: skip
    q = sum(rho * t for rho, t in layers)
    a = dome.radius + sum(t for _, t in layers) / 2
    if dome.rise > dome.diameter / 2 + 1e-9:
        return None  # past a hemisphere: the dome leans in over the wall, not checked here
    alpha = math.asin(min(1.0, dome.diameter / 2 / dome.radius))
    meridian, per_foot, ring, hoop = membrane(a, q, alpha)
    thick = sum(t for _, t in layers)
    cracked = lune_thrust(a, thick, q / thick, alpha) if alpha > math.radians(NO_TENSION) else None
    steps = [
        Step(
            name="Dome: weight per square foot of shell",
            formula="q = Σ density × thickness, over the roof's layers",
            inputs={
                f"layer {i + 1}": f"{rho:.0f} lb/ft³ × {t * 12:.3g} in"
                for i, (rho, t) in enumerate(layers)
            },
            value=f"{q:.1f} lb/ft²",
            reference=MEMBRANE,
        ),
        Step(
            name="Dome: its sphere and springing",
            formula="R = (r_b² + h²) / 2h; a = R + T/2; α₀ = asin(r_b / R)",
            inputs={
                "r_b": f"{dome.diameter / 2 * 12:.3g} in",
                "h": f"{dome.rise * 12:.3g} in",
            },
            value=f"a = {a * 12:.3g} in, α₀ = {math.degrees(alpha):.1f}°",
            reference="sphere geometry",
        ),
        Step(
            name="Dome: meridian thrust at the springing",
            formula="N_α = a·q / (1 + cos α₀), compression",
            value=f"{meridian:,.0f} lb/ft",
            reference=MEMBRANE,
        ),
        Step(
            name="Dome: outward push on the wall's top",
            formula="N_α·cos α₀",
            value=f"{per_foot:,.0f} lb/ft",
            reference=MEMBRANE,
        ),
        Step(
            name="Dome: ring tension at the springing",
            formula="H = a₀·N_α·cos α₀, a₀ = a·sin α₀",
            value=f"{ring:,.0f} lb",
            reference=MEMBRANE,
            note="held by the wall's ring of brick or an iron band round it (Olsen p.167)",
        ),
        Step(
            name="Dome: hoop force in the shell at the springing",
            formula="N_θ = a·q·(1/(1 + cos α₀) − cos α₀), tension when positive",
            value=f"{hoop:,.0f} lb/ft",
            reference=MEMBRANE,
            note=f"tension past α₀ = {NO_TENSION}°",
        ),
    ]
    if cracked is not None:
        steps += cracked.steps
    return DomeRing(math.degrees(alpha), meridian, per_foot, ring, hoop, steps, cracked)


LAU = (
    "W. W. Lau, Equilibrium Analysis of Masonry Domes, S.M. thesis, MIT, 2006 "
    "(masonry-statics.md §M3, checked on the page images)"
)
LAU_SAHC = (
    "Maia Avelino, Iannuzzo, Van Mele & Block, SAHC 2020, §4.2: hemisphere t/R = 0.10, "
    "(T/W)min 19.8 %, (T/W)max 430 % (masonry-statics.md §M3)"
)
LAU_T_R = (0.03, 0.20)
"""t/R (whole thickness over the median radius) over which Lau compares Eq. 3.6 with his thrust
lines (Fig. 3.17, p.59); outside it the lune check refuses (ADR 0009)."""
LAU_THIN = 0.069
"""Lau's least t/R for a hemisphere with no hoop force between the lunes (p.54); 0.041 with
them (p.55)."""


@dataclass(frozen=True)
class LuneThrust:
    """A cracked dome's least push, from Lau's lune statics (Eq. 3.6), imperial: H/W for one
    lune, the push per foot of the base circle (Eq. 3.1), the ring tension it makes, and the
    whole dome's weight. None of the numbers when t/R is outside Lau's checked range."""

    t_over_r: float
    h_over_w: float | None
    per_foot: float | None
    ring: float | None
    weight: float
    steps: list[Step]


def lune_thrust(a: float, thick: float, rho: float, alpha: float) -> LuneThrust:
    """Lau's (2006) least horizontal thrust of a spherical dome cracked into lunes, δ = 0, any
    consistent units (a the median radius, thick the whole thickness, rho the weight per unit
    volume, alpha radians from the crown).

    Eq. 3.6 (p.58): H = W·(a sin α − x_cg) / ((a + t) cos δ − a cos α), t half the thickness, for
    a pin at the middle of the lune's foot and a roller at the crown's extrados. W from Eq. 2.5
    (p.36) with δ = 0; x_cg is the lune's centroid as θ → 0, 3(r⁴ − r′⁴)/(8(r³ − r′³)) ·
    (2α − sin 2α)/(2(1 − cos α)), derived by integrating over the shell (printed Eq. 2.6 has
    (β − γ) sin γ in its denominator, which would make a hemisphere's centroid negative; with
    δ = 0 the term drops, as in Eq. 2.5). Per length of the base, Eq. 3.1: h = H/(aθ sin α),
    and H/θ = (H/W)·W_dome/2π."""
    t_r = thick / a
    r, r_in = a + thick / 2, a - thick / 2
    weight = 2 * math.pi * rho * (r**3 - r_in**3) / 3 * (1 - math.cos(alpha))
    steps = [
        Step(
            name="Dome cracked into lunes: thickness over radius",
            formula="t/R = T / a",
            inputs={"T": f"{thick * 12:.3g} in", "a": f"{a * 12:.4g} in"},
            value=f"{t_r:.3f}",
            reference=LAU,
            note=(
                f"Lau's lune statics are compared with his thrust lines for t/R "
                f"{LAU_T_R[0]}–{LAU_T_R[1]} (Fig. 3.17, p.59)"
            ),
        ),
        Step(
            name="Dome cracked into lunes: whole dome's weight",
            formula="W_dome = 2π·ρ·(r³ − r′³)/3·(1 − cos α), r = a + T/2, r′ = a − T/2",
            inputs={"ρ": f"{rho:.0f} lb/ft³", "α": f"{math.degrees(alpha):.1f}°"},
            value=f"{weight:,.0f} lb",
            reference=f"{LAU}, Eq. 2.5 (p.36), θ = 2π, δ = 0",
        ),
    ]
    if not LAU_T_R[0] <= t_r <= LAU_T_R[1]:
        return LuneThrust(t_r, None, None, None, weight, steps)
    k = 3 * (r**4 - r_in**4) / (8 * (r**3 - r_in**3))
    x_cg = k * (2 * alpha - math.sin(2 * alpha)) / (2 * (1 - math.cos(alpha)))
    t = thick / 2
    h_w = (a * math.sin(alpha) - x_cg) / ((a + t) - a * math.cos(alpha))
    per_foot = h_w * weight / (2 * math.pi * a * math.sin(alpha))
    ring = per_foot * a * math.sin(alpha)
    steps += [
        Step(
            name="Dome cracked into lunes: a lune's centroid from the axis",
            formula="x_cg = 3(r⁴ − r′⁴)/(8(r³ − r′³)) · (2α − sin 2α)/(2(1 − cos α))",
            value=f"{x_cg * 12:.4g} in",
            reference=f"{LAU}, Eq. 2.6 (p.36), θ → 0, δ = 0, derived by integration",
        ),
        Step(
            name="Dome cracked into lunes: least thrust over a lune's weight",
            formula="H/W = (a sin α − x_cg) / ((a + t) − a cos α), t = T/2",
            value=f"{h_w:.3f}",
            reference=f"{LAU}, Eq. 3.6 (p.58)",
            note=(
                "within about 5 % of Lau's thrust-line minimum for α near 90°, which is up to "
                "20 % lower below α = 40° (p.59)"
            ),
        ),
    ]
    if alpha >= math.pi / 3:
        fit = -0.583 * alpha + 1.123
        steps.append(
            Step(
                name="Dome cracked into lunes: Lau's linear fit, a cross-check",
                formula="H/W = −0.583·α + 1.123, α in radians, α ≥ π/3, within 20 %",
                value=f"{fit:.3f}",
                reference=f"{LAU}, Eq. 3.2 (p.56)",
            )
        )
    steps += [
        Step(
            name="Dome cracked into lunes: least push per foot of the base",
            formula="h = H/(aθ sin α) = (H/W)·W_dome / (2π·a·sin α)",
            value=f"at least {per_foot:,.0f} lb/ft",
            reference=f"{LAU}, Eq. 3.1 (p.56); {LAU_SAHC}",
            note="a least value: pushed in, a dome can thrust many times more (SAHC 2020)",
        ),
        Step(
            name="Dome cracked into lunes: least ring tension at the base",
            formula="h·a·sin α",
            value=f"at least {ring:,.0f} lb",
            reference=f"{LAU}; {MEMBRANE}",
        ),
    ]
    return LuneThrust(t_r, h_w, per_foot, ring, weight, steps)


SECTION_IN = 9.0
"""A round electric kiln's section: two 4½ in courses (L&L e23T-3, "Three 9" high sections";
electric-kiln-survey.md, verified)."""
BANDS_SOURCE = (
    "electric-kiln-survey.md: L&L e23T-3, 9 in sections; Skutt's lid, slab and body bands, the "
    "bricks held by the band's tension, not cement (kiln parts listings, snippets)"
)


def _electric_bands(kiln: Kiln) -> Finding:
    """A round electric kiln's steel bands, listed but not sized: one round each section, the
    floor slab and the lid. No source gives a band's width, thickness or tension."""
    from kilndesigner.rings import wall_height

    inside = kiln.chamber.floor_inside
    height = wall_height(si(kiln.chamber.height, "in"), inside)
    sections = math.ceil(height / SECTION_IN - 1e-6)
    lid = "the lid" if isinstance(kiln.roof, FlatRoof) else None
    slab = "the floor slab" + (", inside the wall's lowest course" if inside else "")
    parts = [f"{sections} round the wall, one round each {SECTION_IN:g} in section",
             f"one round {slab}"] + ([f"one round {lid}"] if lid else [])  # fmt: skip
    return Finding(
        level="info",
        message=(
            "A round electric kiln's bricks are held by steel bands, not mortar: "
            + "; ".join(parts)
            + ". Their width, thickness and tension aren't sized: no source found gives them, so "
            "take them from the maker of the bands or a kiln of the same size."
        ),
        reference=BANDS_SOURCE,
    )


def round_door_bands(kiln: Kiln) -> Finding:
    """A round kiln's bands where a door breaks its wall: each band at the door's height stops at
    the jambs, and those above run over its head; listed, not sized (no source sizes a band)."""
    door = kiln.loading.opening
    assert door is not None, "only a door in part of the wall breaks the bands"
    sill = si(door.sill, "in")
    top = sill + si(door.height, "in")
    dome = isinstance(kiln.roof, Dome)
    return Finding(
        level="info",
        message=(
            f"The door breaks the round wall's ring and the iron bands round it, from {sill:g} "
            f"to {top:g} in up: a band there can't run round in one piece, so it ends at the "
            "jambs, and the bands above run over the door's head"
            + (
                ", which can't hold the dome's thrust as a ring: the band over the door carries "
                "it across"
                if dome
                else ""
            )
            + ". No source sizes a band or says how its ends are held at a jamb, so they aren't "
            "sized."
        ),
        reference="steel-design.md §S5; Olsen, The Kiln Book, 4th ed., p.167–169 (iron bands)",
    )


def design_frame(kiln: Kiln) -> FrameDesign:
    """The frame, and for a door in part of a wall, what spans the door (door.py)."""
    from kilndesigner.door import door_head
    from kilndesigner.foundation import platform_bearing

    frame = _design_frame(kiln)
    if isinstance(kiln.roof, SprungArch) and kiln.roof.crossing is not None:
        from kilndesigner.crossing import crossing_note, crossing_statics

        steps, found = crossing_statics(kiln)
        frame = frame.model_copy(update={
            "working": [*frame.working, *steps],
            "findings": [*frame.findings, *found, crossing_note(kiln)],
        })  # fmt: skip
    bearing, under = platform_bearing(kiln)
    if bearing or under:
        frame = frame.model_copy(
            update={"working": [*frame.working, *bearing], "findings": [*frame.findings, *under]}
        )
    head = door_head(kiln)
    if head is None:
        return frame
    members = list(frame.members)
    if head.lintel is not None:
        members.append(
            Member(part="door lintel", steel=head.lintel, count=1, length_in=head.length_in,
                   source="steel-design.md §S5; door-openings.md")
        )  # fmt: skip
    findings = [*frame.findings, *head.findings]
    if kiln.chamber.shape == "round":
        findings.append(round_door_bands(kiln))
    return frame.model_copy(
        update={
            "members": members, "working": [*frame.working, *head.working], "findings": findings,
        }
    )  # fmt: skip


def _design_frame(kiln: Kiln) -> FrameDesign:
    o = outside(kiln)
    volume_ft3 = chamber_shape(kiln).volume / si(parse_quantity("1 ft**3"), "m**3")
    if kiln.roof.type == "open":
        return _unframed([], [])  # no roof, so no thrust to hold
    if kiln.chamber.shape == "round":
        return _round_frame(kiln)
    if isinstance(kiln.roof, SprungArch) and kiln.roof.building_frame:
        return _building_frame(kiln)
    if getattr(kiln.roof, "buttressed", False):
        return _held_by_masonry(kiln)
    if arches_along(kiln):
        one = isinstance(kiln.roof, SprungArch) and kiln.roof.along
        return _along_frame(kiln) if one else _row_arches(kiln)
    if isinstance(kiln.roof, CatenaryArch):
        return _catenary_feet(kiln)
    if isinstance(kiln.roof, Dome):
        return _dome_frame(kiln)
    if not isinstance(kiln.roof, SprungArch):
        if kiln.heat.gas is None and kiln.heat.fire is None:
            return _case(kiln, o)
        return _flat_frame(kiln, o)
    working: list[Step] = []
    findings: list[Finding] = []
    data = steel_data()
    limit = float(data["binding_stress_psi"])

    # The smallest angle, from the builders who published theirs: Olsen's (p.139, p.174), and
    # Pitelka's for a hinged door
    outside_ft3 = o.width * o.depth * (o.bottom + skewback_top(kiln, whole_roof=True)) / 1728
    if kiln.door_kind == "hinged":
        floor = angle("L3×3×1/4") if volume_ft3 <= 24 else angle("L4×4×1/4")
        why = f"hinged door, {volume_ft3:.0f} ft³ ({'≤' if volume_ft3 <= 24 else '>'} 24 ft³)"
        floor_source = PITELKA
    elif outside_ft3 >= OLSEN_FRAME_FT3:
        floor, why, floor_source = (
            angle("L3×3×1/4"),
            (
                f"{outside_ft3:.0f} ft³ outside: Olsen's corner posts for a 5 × 5 × 6 ft kiln, "
                "'larger (stronger), but not smaller'"
            ),
            OLSEN_FRAME,
        )
    else:
        floor, why, floor_source = (
            angle("L2×2×3/16"),
            (
                f"{outside_ft3:.0f} ft³ outside: Olsen's bolted fast-fire frame; smaller kilns can "
                "use 3/16 in angle"
            ),
            OLSEN_FRAME,
        )
    working.append(
        Step(
            name="Smallest frame angle",
            value=floor.name,
            inputs={"because": why},
            reference=floor_source,
        )
    )

    span_in = si(kiln.chamber.width, "in")
    arch = Arch(span_in, si(kiln.roof.rise, "in"))
    d = arch.rise / (span_in / 12)
    load = _arch_load(kiln, arch)
    working.append(
        Step(
            name="Arch weight per foot of length",
            value=f"{load.weight:.1f} lb/ft",
            formula="Σ density × thickness × mean arc, over the roof's layers",
            inputs={f"layer {i + 1}": s for i, s in enumerate(load.lines)},
            reference="HarbisonWalker W, exact form; kiln-hardware.md §4.6 [S20]",
            note="Includes insulation laid on the arch, which HarbisonWalker's tables leave out.",
        )
    )
    consts = data["arch_constants"]
    heated_table = data["heated_factor"]
    rule = data["rise_per_foot"]
    t_over_s = 100 * load.ring / span_in
    arch_in = _arch_inputs(kiln)
    if load.loose:
        findings.append(
            Finding.failed(
                loose_ring("arch", list(load.loose), rule["source"]).check(),
                message=(
                    f"The arch's ring includes {' and '.join(load.loose)}, which can't carry an "
                    "arch's thrust: the ring must be brick or castable. Set the roof's ring to the "
                    "layers that are."
                ),
            )
        )
        return _unframed(working, findings)
    working.append(
        Step(
            name="Arch ring",
            value=f"{load.ring:g} in, T/S {t_over_s:.1f} %",
            inputs={"layers from the inside": str(kiln.roof.ring)},
            note="The layers laid over the ring are its load, not part of it.",
        )
    )
    # Olsen's least rise, about 1½ in/ft, what a featheredge skewback gives; he sets no most
    # (p.51: he has built 6 in/ft; p.296: 4–6 in/ft on chamber kilns)
    rising = rise_rule(arch_in, OLSEN_LEAST_RISE, OLSEN_RISE)
    rising.agrees("d", d / 12)
    if (check := rising.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"The arch rises {d:.2f} in per foot of span, less than Olsen's 1½ in/ft, what "
                    "a featheredge skewback gives: less 'can result in structural difficulty'. "
                    f"On this span that is a rise of {OLSEN_LEAST_RISE * span_in / 12:.2f} in."
                ),
            )
        )
    # HarbisonWalker's heated-arch method works while the hot thrust line can hinge inside the
    # ring: T ≤ (h − S/48) ÷ cos ½θ, the line rising at least ¼ in per foot of span
    cos_half = math.cos(arch.half_angle)
    # A half circle springs straight up from its skewbacks, so its ring can be any thickness
    thickest = (arch.rise - span_in / 48) / cos_half if cos_half > 1e-9 else math.inf
    working.append(
        Step(
            name="Thickest ring for HarbisonWalker's heated-arch method",
            value=f"{thickest:.2f} in" if math.isfinite(thickest) else "any: a half circle",
            formula="T ≤ (h − S/48) ÷ cos ½θ",
            inputs={
                "h": f"{arch.rise:.2f} in",
                "S": f"{span_in:g} in",
                "½θ": f"{math.degrees(arch.half_angle):.1f}°",
            },
            reference=consts["source"],
        )
    )
    # The skewback needs the wall under it: the ring's outer corner must be within the side walls
    corner, wall = ring_outside(kiln), span_in / 2 + min(o.left, o.right)
    standing = skewback_on_wall(arch_in, min(o.left, o.right))
    standing.agrees("x_c", Q_(corner, "in"))
    standing.agrees("x_w", Q_(wall, "in"))
    if (check := standing.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"The arch's ring reaches {corner - wall:.2f} in past the outside of the side "
                    "walls at the skewback, so the skewback has no wall to stand on. Thicken the "
                    "side walls or thin the ring."
                ),
            )
        )
    h_factor = cold_thrust_factor(span_in, arch.rise)
    cold = h_factor * load.weight
    working.append(
        Step(
            name="Cold horizontal thrust",
            value=f"{cold:.1f} lb per foot of arch",
            formula="H = W·(sin θ − (1 − cos θ)/θ) / (2(1 − cos θ)), θ = 2·atan(2h/S)",
            inputs={"rise per foot of span, d": f"{d:.3f} in/ft", "H / W": f"{h_factor:.3f}"},
            reference=(
                f"statics of a three-hinged circular arch; checked against {consts['source']}"
            ),
        )
    )
    heated = heated_thrust_factor(span_in, arch.rise, load.ring)
    statics = (
        heated is not None
        and load.ring <= thickest + 1e-9
        and heated <= MAX_PRINTED_HEATED + 1e-9
        and hot_thrust_line(arch_in).check().status == "pass"
    )
    capped: float | None = None
    if statics:
        assert heated is not None
        thrust = heated * cold
        working.append(
            Step(
                name="Thrust of the heated arch, free to rise",
                value=f"{thrust:.1f} lb per foot of arch",
                formula=(
                    "hinges at the intrados at the crown and the extrados at the skewbacks: "
                    "Hmax = M_P / (y_crown − y_P); factor = Hmax / H with both at mid-thickness"
                ),
                inputs={"T/S": f"{t_over_s:.1f} %", "factor": f"{heated:.2f}"},
                reference=ARCH_THEORY_SOURCE,
            )
        )
        table = checked_range(
            arch_in,
            (heated_table["t_over_s"][0], heated_table["t_over_s"][-1]),
            (consts["d"][0], consts["d"][-1]),
            ARCH_THEORY_SOURCE,
        ).check()
        if table.status != "pass":
            findings.append(
                Finding(
                    level="info",
                    message=(
                        "The heated thrust is worked out from statics. HarbisonWalker's table, "
                        f"which it matches to 4 %, covers T/S 4–10 % and 1–3 in/ft; this arch, at "
                        f"{t_over_s:.1f} % and {d:.2f} in/ft, is past it, where the same statics "
                        "carry on."
                    ),
                    reference=ARCH_THEORY_SOURCE,
                )
            )
    else:
        capped = MAX_PRINTED_HEATED
        thrust = capped * cold
        working.append(
            Step(
                name="Thrust of the heated arch",
                value=f"{thrust:.1f} lb per foot of arch",
                formula="H = 5.34 × H_c, the most HarbisonWalker tabulates",
                inputs={"T/S": f"{t_over_s:.1f} %", "the thickest ring its method takes": (
                    f"{max(thickest, 0):.2f} in" if math.isfinite(thickest) else "any"
                )},
                reference=CAPPED,
            )
        )  # fmt: skip
        findings.append(
            Finding(
                level="info",
                message=(
                    f"This arch's {load.ring:g} in ring is too thick for its rise for "
                    "HarbisonWalker's heated-arch method, which has no finite hot thrust for it "
                    "in a rigid frame and marks such arches 'stress excessive'. Olsen builds "
                    "arches like it, No. 1 arches of 4½ in insulating brick at 1½ in/ft, in light "
                    "frames that give (his fast-fire kiln's is 2 × 2 × 3/16 in angle, bolted), so "
                    "the frame's give limits the thrust. The steel is sized for "
                    f"{MAX_PRINTED_HEATED:g} × the cold thrust, the most HarbisonWalker "
                    "tabulates. Leave the frame its expansion allowance (Olsen p.52)."
                ),
                reference=CAPPED,
            )
        )
    rigid = thrust
    if kiln.roof.ties == "springs":
        thrust = _sprung_ties(kiln, span_in, cold, rigid, o, working, findings)
    if statics:
        heating = heated_factor_limit(arch_in, MAX_PRINTED_HEATED, ARCH_THEORY_SOURCE)
        heating.agrees("W", Q_(load.weight, "lbf/ft"))
        heating.agrees("H_c", Q_(cold, "lbf/ft"))
        heating.agrees("f", heated or 0.0)

    chosen = floor
    rods = data["rods"]["sizes"][1:]  # ½-13 and up: ½ in is what builders use [S7] [S17]
    rod = rods[0]
    # Posts along each side, the corners included: the fewest that let a listed angle and rod
    # carry the thrust, as builders add buckstays along a large kiln's sides (kiln-hardware.md
    # §4.1–4.2). With springs on the rods, only the corner posts are worked out.
    posts = 2
    if kiln.roof.ties == "rigid":
        posts = _posts_per_side(o.depth, thrust / 12, floor, limit, rods)
    bay = o.depth / (posts - 1)  # the buttress spans between posts
    share = 0.5 if posts == 2 else 1.0  # the busiest rod's bays: one at a post between
    moment = (thrust / 12) * bay**2 / 8
    needed = moment / limit
    fits = [a for a in angles() if a.sx >= needed and a.leg >= floor.leg and a.t >= floor.t]
    springs = None
    if kiln.roof.ties == "springs":
        assert kiln.roof.spring_rate is not None
        k = si(kiln.roof.spring_rate, "lbf/in")
        springs = Springs(k, GROWTH_IN_PER_FT, GROWTH_SOURCE, SPRING_SOURCE)
    biggest = max(angles(), key=lambda a: a.sx)
    bending = buttress_bending(
        arch_in, bay, share, (fits[0] if fits else biggest).name,
        (fits[0] if fits else biggest).sx, limit, springs,
        (data["angles"]["source"], data["binding_stress_source"]), capped,
    )  # fmt: skip
    bending.agrees("M", Q_(moment, "lbf*in"))
    if (check := bending.check()).status != "pass" or not fits:
        closer = (
            "Lighten the arch, or hold it with masonry (buttressed)"
            if kiln.roof.ties == "rigid"
            else "Tie the rods rigid, so posts can go along the side walls"
        )
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"No angle up to {biggest.name} carries the arch's thrust over {bay:.0f} in "
                    f"between posts, the shortest bay the engine sets ({MIN_BAY:g} in or more). "
                    f"{closer}."
                ),
            )
        )
    else:
        chosen = fits[0]
    if posts > 2:
        working.append(
            Step(
                name="Posts along the side walls",
                value=f"{posts} each side, {bay:.1f} in apart",
                formula=(
                    "the fewest posts for which a listed angle (M = wL²/8) and rod (P = wL) carry "
                    "the thrust between them"
                ),
                reference="kiln-hardware.md §4.1–4.2 [S20] [S34] (derived)",
                note=(
                    "Large kilns are braced by buckstays along their sides, tied across by rods "
                    "(HarbisonWalker; Rhodes). No source gives their spacing: this is the widest "
                    "the steel allows."
                ),
            )
        )
    working.append(
        Step(
            name="Buttress angle, bending",
            value=f"needs Sx ≥ {needed:.3f} in³; {chosen.name} has {chosen.sx:.3f} in³",
            formula="M = wL²/8, Sx = M ÷ 12,000 psi (a simple beam between the posts)",
            inputs={
                "w": f"{thrust / 12:.2f} lb/in",
                "L": f"{bay:.1f} in",
                "M": f"{moment:,.0f} lb·in",
            },
            reference=(
                f"{data['binding_stress_source']}; AISC Sx and Sz, kiln-hardware.md §4.7.1 [S28]"
            ),
            note=(
                "A cautious first check, derived in kiln-hardware.md §4.5; not a sourced design "
                "rule. Sx is about a geometric axis, bending parallel to a leg. An angle free to "
                f"twist bends about its principal axis instead, where its Sz is {chosen.sz:.3f} "
                f"in³: {moment / chosen.sz:,.0f} psi. Which applies depends on how the brickwork "
                "holds the angle, which no source here says."
            ),
        )
    )
    per_rod = thrust * (bay / 12) * share  # the busiest rod
    for size in rods:
        rod = size
        if per_rod / size["stress_area"] <= limit:
            break
    tied = rod_stress(
        arch_in, bay, share, rod["name"], rod["stress_area"], limit, springs,
        (data["rods"]["source"], data["binding_stress_source"]), capped,
    )  # fmt: skip
    tied.agrees("P", Q_(per_rod, "lbf"))
    if (check := tied.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"No rod up to {rod['name']} carries the arch's thrust: the busiest of the "
                    f"{posts} rods takes {per_rod:,.0f} lb, {per_rod / rod['stress_area']:,.0f} "
                    "psi, hot."
                ),
                reference=f"{data['rods']['source']}; {data['binding_stress_source']}",
            )
        )
    working.append(
        Step(
            name=(
                "Tie rods, one at the front and one at the back"
                if posts == 2
                else f"Tie rods, one at each of the {posts} pairs of posts"
            ),
            value=f"{rod['name']}: {per_rod / rod['stress_area']:,.0f} psi",
            formula=(
                "thrust × length ÷ 2 rods ÷ tensile stress area"
                if posts == 2
                else "thrust × the bay between posts ÷ tensile stress area, at a post between"
            ),
            inputs={
                "load on the busiest rod": f"{per_rod:,.0f} lb",
                "stress area": f"{rod['stress_area']} in²",
            },
            reference=f"{data['rods']['source']}; {data['binding_stress_source']}",
            note="½ in is the smallest used here, because builders use it (kiln-hardware.md "
            "§4.2 [S7] [S17]).",
        )
    )

    top = skewback_top(kiln)
    leg = chosen.leg
    # HarbisonWalker: the line of thrust through, or slightly above, the steel's corner (S5).
    # A note, not a warning: Olsen's built kilns (Kahler's salt kiln, his three-chamber kiln)
    # stand with it lower, and ADR 0014 takes them as the reference.
    sheet = thrust_through_steel(arch_in, max(o.left, o.right), chosen.leg, chosen.t)
    if sheet.check().status != "pass":
        drop, most = sheet.env["δ"] / 0.0254, sheet.env["δ_max"] / 0.0254
        findings.append(
            Finding(
                level="info",
                message=(
                    f"The cold line of thrust drops {drop:.2f} in from the ring's corner to the "
                    f"side wall's outside, past the {chosen.name} buttress's {most:.2f} in of "
                    "upright leg: HarbisonWalker, for industrial furnaces, wants it through or "
                    "just above the steel's corner. Olsen's built kilns stand with it lower, so "
                    "this is a note; a longer-legged angle, thinner walls at the skewback or more "
                    "rise would bring it up."
                ),
                reference=THRUST_THROUGH_STEEL,
            )
        )
    members = [
        Member(
            part="corner posts" if posts == 2 else "posts, at the corners and along the sides",
            steel=chosen.name,
            count=2 * posts,
            length_in=o.bottom + top,
            source=PITELKA,
        ),
        Member(
            part="buttresses behind the skewbacks",
            steel=chosen.name,
            count=2,
            length_in=o.depth + 2 * leg,
            source=PITELKA,
        ),
        Member(
            part="top cross-members, front and back",
            steel=chosen.name if kiln.door_kind == "hinged" else FLAT_BAR,
            count=2,
            length_in=o.width + 2 * leg,
            source=PITELKA,
        ),
        *_ring_of(FLAT_BAR, "bottom cross-members", o, leg, PITELKA),
        Member(
            part="tie rods",
            steel=f"{rod['name']} threaded rod",
            count=posts,
            length_in=o.width + 2 * leg + 4,
            source=f"length: {MERRILL}",
        ),
    ]
    if not any(f.level == "error" for f in findings):
        findings.append(
            Finding(
                level="info",
                message=(
                    "Weld the frame and fit it before the arch form comes out: the steel is what "
                    "holds the arch up."
                ),
                reference="kiln-hardware.md §4.1–4.2 [S11] [S21]",
            )
        )
    return FrameDesign(
        kind="arch frame",
        angle=chosen.name,
        angle_leg_in=chosen.leg,
        angle_t_in=chosen.t,
        rod=rod["name"],
        rod_d_in=rod["d"],
        thrust=f"{thrust:.0f} lb per foot of arch",
        members=members,
        working=working,
        findings=findings,
        posts=posts,
    )


MIN_BAY = 18.0
"""in: posts no closer than two brick lengths. No source gives a buckstay spacing; past this the
arch is too heavy for a frame of listed angle and rod, and wants lightening or masonry."""


def _posts_per_side(
    depth: float, w: float, floor: Angle, limit: float, rods: list[dict[str, Any]]
) -> int:
    """The fewest posts along each side wall, corners included, for which an angle no smaller than
    ``floor`` carries the thrust ``w`` (lb per in) between posts as a simple beam, and a listed rod
    ties the busiest pair: half the kiln's length at the corners alone, a whole bay at a post
    between. Bays stop shrinking at ``MIN_BAY``."""
    n = 2
    while True:
        bay = depth / (n - 1)
        share = 0.5 if n == 2 else 1.0
        bent = any(
            a.sx >= w * bay**2 / 8 / limit and a.leg >= floor.leg and a.t >= floor.t
            for a in angles()
        )
        tied = any(w * bay * share / r["stress_area"] <= limit for r in rods)
        if (bent and tied) or depth / n < MIN_BAY:
            return n
        n += 1


GROWTH_IN_PER_FT = 3 / 32  # the most brickwork grows hot: Olsen 4th ed. p.51 (1/16–3/32 in/ft)
GROWTH_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.51: 1/16–3/32 in per ft (0.5–0.8 %), with IFB's 0.5–0.7 % "
    "reversible expansion (thermal-properties.md §2)"
)
SPRING_SOURCE = (
    "a spring's force grows by its rate × its travel; the rods' share capped at the rigid frame's "
    "hot thrust (arch-springs.md, arch-thrust-theory.md)"
)


def _sprung_ties(
    kiln: Kiln,
    span_in: float,
    cold: float,
    rigid: float,
    o: Outside,
    working: list[Step],
    findings: list[Finding],
) -> float:
    """The hot thrust (lb per ft) when each tie rod ends in a compression spring.

    The springs are set to carry the cold thrust; as the arch grows by ΔS across its span,
    each end gives ΔS/2 and its spring pushes back k·ΔS/2 more. The thrust can't pass what a
    rigid frame would see (Heyman's maximum), so it's the smaller of the two.
    """
    assert isinstance(kiln.roof, SprungArch)
    assert kiln.roof.spring_rate is not None
    k = si(kiln.roof.spring_rate, "lbf/in")
    growth = span_in / 12 * GROWTH_IN_PER_FT
    feet = o.depth / 12
    cold_rod = cold * feet / 2
    hot_rod = min(cold_rod + k * growth / 2, rigid * feet / 2)
    working.append(
        Step(
            name="Growth of the arch's span, hot",
            value=f"{growth:.3f} in",
            formula="ΔS = span in ft × 3/32 in",
            inputs={"span": f"{span_in:.1f} in"},
            reference=GROWTH_SOURCE,
        )
    )
    working.append(
        Step(
            name="Tie rod load with springs, hot",
            value=f"{hot_rod:,.0f} lb per rod (rigid: {rigid * feet / 2:,.0f} lb)",
            formula="P = P_cold + k·ΔS/2, no more than the rigid frame's",
            inputs={
                "P_cold, the spring's preload": f"{cold_rod:,.0f} lb",
                "k, each spring": f"{k:,.0f} lbf/in",
                "each spring's travel, hot": f"{growth / 2:.3f} in",
                "set length: compress each spring by": f"{cold_rod / k:.2f} in, cold",
            },
            reference=SPRING_SOURCE,
        )
    )
    findings.append(
        Finding(
            level="info",
            message=(
                f"Set each spring {cold_rod / k:.2f} in shorter than free, cold; hot it takes "
                f"{growth / 2:.3f} in more, so pick one whose solid height leaves that room. "
                "Keep the springs outside the insulation and steel: music wire is good to about "
                "250 °F."
            ),
            reference="arch-springs.md (spring temperature limits)",
        )
    )
    return hot_rod * 2 / feet


def _ring_of(steel: str, part: str, o: Outside, leg: float, source: str) -> list[Member]:
    """Members once round the kiln's outside: two across the front and back, two along the
    sides, each long enough to lap the corners by a leg."""
    return [
        Member(part=f"{part}, front and back", steel=steel, count=2, length_in=o.width + 2 * leg,
               source=source),
        Member(part=f"{part}, sides", steel=steel, count=2, length_in=o.depth + 2 * leg,
               source=source),
    ]  # fmt: skip


def _unframed(working: list[Step], findings: list[Finding]) -> FrameDesign:
    """An arch whose thrust can't be worked out: no steel is shown, and the findings say why."""
    return FrameDesign(
        kind=NO_FRAME, angle=None, angle_leg_in=0, angle_t_in=0, rod=None, rod_d_in=0,
        thrust=None, members=[], working=working, findings=findings,
    )  # fmt: skip


FLAT_SOURCE = "BIA Technical Note 31A, jack arches; flat-roofs.md §2 [F2]"
FLAT_CHECKED_IN = 36.0
"""The longest one-way flat roof in the sources: Merrill's rows, squeezed by rods (§4.3 [F9])."""
FLAT_LONGEST_IN = 45.0
"""About the longest flat brick roof in the sources, on four walls: L&L's lids and Nils Lou's
roof (flat-roofs.md §4.1, §4.3, derived)."""
FLAT_IFB_TOP_F = 2450.0
"""BNZ: suspended flat IFB roofs no hotter than 1345 °C, 2450 °F (flat-roofs.md §4.4 [F15])."""
FRICTION = 0.60
"""BIA's friction between brick masonry units (§2.2 [F2]); for IFB none is sourced."""
ROW_IN = 4.5  # a row of roof brick, as Merrill's: bricks on end, 4½ in across the row (§4.3)


def _flat_roof(kiln: Kiln, working: list[Step], findings: list[Finding]) -> float | None:
    """A flat roof over a whole-wall door spans one way, between the walls either side of the
    door, as a jack arch squeezed by its frame (flat-roofs.md §2, §4). Returns its thrust, lb per
    inch of roof, or None for a fibre roof."""
    from kilndesigner.castable import resolve_material

    door = kiln.door_face
    w, d = si(kiln.chamber.width, "in"), si(kiln.chamber.depth, "in")
    span, length = (w, d) if door in ("front", "back") else (d, w)
    walls = "the left and right walls" if door in ("front", "back") else "the front and back walls"
    layers = kiln.lining.for_face("roof")
    slab = resolve_material(kiln, layers[0].material)
    depth = si(layers[0].thickness, "in")
    if slab.kind in LOOSE:
        findings.append(
            Finding(
                level="info",
                message=(
                    "A fibre roof can't span as a flat arch: it hangs from its frame, which isn't "
                    "designed here."
                ),
            )
        )
        return None
    load = sum(
        si(parse_quantity(resolve_material(kiln, x.material).density), "lb/ft**3")
        / 1728
        * si(x.thickness, "in")
        for x in layers
    )  # lb per square inch of roof, every layer
    thrust = 3 * load * span**2 / (8 * depth)  # lb per inch: H = 3WS/8d, W = load × S
    working.append(
        Step(
            name="Flat roof, as a jack arch",
            value=(
                f"spans {span:g} in between {walls}; the frame must squeeze it with "
                f"{thrust * 12:.0f} lb per foot, {thrust * length:.0f} lb in all, cold"
            ),
            formula="H = 3WS / 8d, the thrust line in the middle third; fm = 2H / bd",
            inputs={
                "S": f"{span:g} in",
                "d": f"{depth:g} in of {slab.name}",
                "W": f"{load * 144:.1f} lb per ft² of roof, every layer, × S",
                "fm": f"{2 * thrust / depth:.1f} psi",
            },
            reference=FLAT_SOURCE,
            note=(
                "BIA's method is for cold brick masonry between abutments that don't move; heat "
                "and the clamp's own squeeze aren't in it (flat-roofs.md §2.5)."
            ),
        )
    )
    roof = _roof_layers(kiln)
    holding = flat_friction(span, roof, FRICTION, FLAT_SOURCE)
    holding.agrees("μ_need", 4 * depth / (3 * span))
    if (check := holding.check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"The flat roof is {depth:g} in deep over {span:g} in: too deep for its span "
                    "to hold at its ends by friction. BIA's jack arches need the span more than "
                    f"about 2.2 times the depth, at the friction of {FRICTION:g} it gives for "
                    "brick (none is sourced for insulating firebrick). Make it thinner or use an "
                    "arch."
                ),
            )
        )
    reach = flat_span(span, FLAT_CHECKED_IN, FLAT_LONGEST_IN).check()
    if reach.status == "error":
        findings.append(
            Finding.failed(
                reach,
                message=(
                    f"A flat roof over {span:g} in is longer than any flat brick roof in the "
                    f"sources, about {FLAT_LONGEST_IN:g} in. Use an arch or a dome."
                ),
                reference="flat-roofs.md §4.5",
            )
        )
    elif reach.status == "warning":
        findings.append(
            Finding.failed(
                reach,
                message=(
                    f"The flat roof spans {span:g} in, past the longest one-way flat roof in the "
                    f"sources, Merrill's {FLAT_CHECKED_IN:g} in; flat lids of about "
                    f"{FLAT_LONGEST_IN:g} in rest on all four walls, and makers move to fibre "
                    "there."
                ),
                reference="flat-roofs.md §4.1, §4.3",
            )
        )
    top = si(top_temperature(kiln)[0], "degF")
    if slab.kind == "insulating_firebrick":
        hottest = flat_ifb_top(slab.name, top, FLAT_IFB_TOP_F, "flat-roofs.md §4.4 [F15]")
        if (check := hottest.check()).status != "pass":
            findings.append(
                Finding.failed(
                    check,
                    message=(
                        f"BNZ keeps flat insulating-firebrick roofs to {FLAT_IFB_TOP_F:g} °F, "
                        f"where IFB still holds together; this kiln reaches {top:.0f} °F. It says "
                        "to use a sprung arch above that."
                    ),
                )
            )
    findings.append(
        Finding(
            level="info",
            message=(
                f"The flat roof stays up only while it's squeezed across its {span:g} in span: "
                "tighten its band or rods after the first firing and every few firings after, as "
                "the makers say, because the brick shrinks and works loose. No maker document read "
                "shows a front-loader with a flat brick roof (L&L and Bailey arch theirs)."
            ),
            reference="flat-roofs.md §3.2, §4.2",
        )
    )
    return thrust


def _flat_frame(kiln: Kiln, o: Outside) -> FrameDesign:
    """A gas kiln with a flat roof: angle round the roof, and Merrill's rod through each row of
    roof brick, squeezing it across its span (kiln-hardware.md §4.2 [S16])."""
    a = angle("L2×2×3/16")
    working: list[Step] = [
        Step(name="Frame", value=f"{a.name} with 3/8 in rods", reference=MERRILL)
    ]
    findings: list[Finding] = []
    thrust = _flat_roof(kiln, working, findings)
    members = [
        Member(
            part="corner posts",
            steel=a.name,
            count=4,
            length_in=o.bottom + o.wall_top,
            source=MERRILL,
        ),
        *_ring_of(a.name, "roof angle", o, a.leg, MERRILL),
        _roof_rods(kiln, o, thrust, a.leg, working, findings, MERRILL),
    ]
    return FrameDesign(
        kind="angle frame",
        angle=a.name,
        angle_leg_in=a.leg,
        angle_t_in=a.t,
        rod="3/8-16",
        rod_d_in=0.375,
        thrust=None if thrust is None else f"{thrust * 12:.0f} lb per foot of roof, cold",
        members=members,
        working=working,
        findings=findings,
    )


def _roof_rods(
    kiln: Kiln,
    o: Outside,
    thrust: float | None,
    leg: float,
    working: list[Step],
    findings: list[Finding],
    source: str,
) -> Member:
    """A 3/8 in rod through each row of roof brick, across its span, squeezing it (Merrill; Olsen's
    electric flat roof, 4th ed. p.248–249): the rods, and their check."""
    across = kiln.door_face in ("front", "back")
    length = o.depth if across else o.width
    rows = max(2, math.ceil(length / ROW_IN - 1e-9))
    rod = steel_data()["rods"]["sizes"][0]  # Merrill's 3/8 in
    if thrust is not None:
        per_rod = thrust * ROW_IN
        stress = per_rod / rod["stress_area"]
        working.append(
            Step(
                name="Rods across the roof, one every 4½ in",
                value=f"{rows} rods: {per_rod:.0f} lb each, {stress:,.0f} psi",
                formula=(
                    "the roof's thrust × 4½ in, a row of brick, ÷ the rod's tensile stress area"
                ),
                reference=f"{source}; {steel_data()['binding_stress_source']}",
            )
        )
        data = steel_data()
        squeezing = flat_rods(
            si(kiln.chamber.width if across else kiln.chamber.depth, "in"),
            _roof_layers(kiln),
            ROW_IN,
            (rod["name"], rod["stress_area"]),
            float(data["binding_stress_psi"]),
            (FLAT_SOURCE, source, f"{data['rods']['source']}; {data['binding_stress_source']}"),
        )
        squeezing.agrees("H", Q_(thrust, "lbf/in"))
        squeezing.agrees("P", Q_(per_rod, "lbf"))
        if (check := squeezing.check()).status != "pass":
            findings.append(
                Finding.failed(
                    check,
                    message=(
                        f"A 3/8 in rod every 4½ in across the roof would carry {stress:,.0f} psi, "
                        "past HarbisonWalker's 12,000 psi for hot steel. Use a thinner or lighter "
                        "roof, or an arch."
                    ),
                    reference=data["binding_stress_source"],
                )
            )
    return Member(
        part="rods across the roof, one every 4½ in",
        steel="3/8-16 threaded rod",
        count=rows,
        length_in=(o.width if across else o.depth) + 2 * leg + 4,
        source=source,
    )


CASE_T = 0.125  # in, L&L's welded case [S6]
OLSEN_ELECTRIC_ROOF = (
    "Olsen, The Kiln Book, 4th ed., p.248–249: a flat roof needs an angle-iron frame, 'a basic "
    "requirement', with rows of brick held by tie bolts through them"
)


def _case(kiln: Kiln, o: Outside) -> FrameDesign:
    """An electric kiln in a welded steel case, as the makers build them: a plate on each wall but
    the door's. A flat brick roof sits in an angle-iron frame with a tie bolt through each row of
    its brick (Olsen p.248–249)."""
    walls = [w for w in ("left", "right", "back", "front") if w != kiln.door_face]
    plates = [
        Member(
            part=f"{', '.join(walls[:-1])} and {walls[-1]} plates",
            steel="⅛ in steel plate",
            count=3,
            length_in=o.bottom + o.wall_top,
            source=CASE_SOURCE,
        ),
        Member(
            part="top and bottom plates",
            steel="⅛ in steel plate",
            count=2,
            length_in=o.depth,
            source=CASE_SOURCE,
        ),
    ]
    working = [Step(name="Case", value="welded ⅛ in steel", reference=CASE_SOURCE)]
    findings: list[Finding] = []
    thrust = _flat_roof(kiln, working, findings)
    if thrust is not None:
        a = angle("L2×2×3/16")  # Olsen gives no size: Merrill's flat-top angle
        plates += [
            *_ring_of(a.name, "roof angle", o, a.leg, f"{OLSEN_ELECTRIC_ROOF}; size: {MERRILL}"),
            _roof_rods(kiln, o, thrust, a.leg, working, findings, OLSEN_ELECTRIC_ROOF),
        ]
    return FrameDesign(
        kind="welded case",
        angle=None,
        angle_leg_in=0,
        angle_t_in=CASE_T,
        rod=None if thrust is None else "3/8-16",
        rod_d_in=0 if thrust is None else 0.375,
        thrust=None if thrust is None else f"{thrust * 12:.0f} lb per foot of roof, cold",
        members=plates,
        working=working,
        findings=findings,
    )
