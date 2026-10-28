"""The steel that holds a kiln together: a frame for a sprung arch, or an electric kiln's case.

A catenary needs no frame over it, but its feet push out (its thrust is worked out, but what holds
the feet isn't sized); a dome's thrust has no source, so no steel is designed for it.

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

from kilndesigner.heatloss import top_temperature
from kilndesigner.model import CatenaryArch, Dome, Kiln, SprungArch
from kilndesigner.shape import Arch, CatenaryCurve, SailDome, chamber_shape
from kilndesigner.units import parse_quantity, si
from kilndesigner.working import Finding, Step

PITELKA = "Pitelka, sprung-arch frames; kiln-hardware.md §4.2 [S11]"
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

    w, d, h = (si(getattr(kiln.chamber, n), "in") for n in ("width", "depth", "height"))
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


def skewback_top(kiln: Kiln) -> float:
    """Height of the skewback's top above the chamber floor (in): the arch's outer corner."""
    assert isinstance(kiln.roof, SprungArch)
    w = si(kiln.chamber.width, "in")
    arch = Arch(w, si(kiln.roof.rise, "in"))
    roof = sum(si(x.thickness, "in") for x in kiln.lining.for_face("roof"))
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
    for layer in kiln.lining.for_face("roof"):
        m = resolve_material(kiln, layer.material)
        rho, t = si(parse_quantity(m.density), "lb/ft**3"), si(layer.thickness, "ft")
        length = curve.length(cum + t / 2)
        total += rho * t * length
        lines.append(
            f"{m.name}: {rho:.0f} lb/ft³ × {t * 12:g} in × {length:.2f} ft = "
            f"{rho * t * length:.1f} lb"
        )
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
    findings = [
        Finding(
            level="warning",
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


def dome_slices(kiln: Kiln, rise: float | None = None, count: int = 21) -> list[DomeSlice]:
    """The dome as arches parallel to the door wall, spanning the two walls either side, from the
    middle out to the end wall (the dome is symmetric). ``rise`` (in) overrides the design's."""
    from kilndesigner.castable import resolve_material

    assert isinstance(kiln.roof, Dome)
    w, d = si(kiln.chamber.width, "in"), si(kiln.chamber.depth, "in")
    span, length = (w, d) if kiln.door_face in ("front", "back") else (d, w)
    dome = SailDome(w, d, si(kiln.roof.rise, "in") if rise is None else rise)
    layers = [
        (si(parse_quantity(resolve_material(kiln, x.material).density), "lb/ft**3") / 1728,
         si(x.thickness, "in"))
        for x in kiln.lining.for_face("roof")
    ]  # fmt: skip
    ring = sum(t for _, t in layers[: kiln.roof.ring])
    table = steel_data()["arch_minimum_thickness"]
    slices: list[DomeSlice] = []
    for i in range(count):
        y = length / 2 * i / (count - 1)
        inside = math.sqrt(dome.radius**2 - y**2)
        alpha = math.asin(min(1.0, span / 2 / inside))
        own_rise = inside * (1 - math.cos(alpha))
        thickness = math.sqrt((dome.radius + ring) ** 2 - y**2) - inside
        eta = float(np.interp(math.degrees(alpha), table["half_angle_deg"], table["eta"]))
        weight, r = 0.0, dome.radius
        for density, t in layers:  # each layer's slice: its thickness × centre radius × arc
            lo, hi = math.sqrt(r**2 - y**2), math.sqrt((r + t) ** 2 - y**2)
            weight += density * (hi - lo) * (lo + hi) / 2 * 2 * alpha
            r += t
        slices.append(
            DomeSlice(
                y, thickness, alpha, own_rise, thickness / (inside + thickness / 2) / eta,
                (own_rise - span / 48) / math.cos(alpha), weight,
            )
        )  # fmt: skip
    return slices


def _dome_frame(kiln: Kiln) -> FrameDesign:
    """A sail dome with a door: it stands as arches parallel to the door wall, spanning the two
    walls either side, if every one stands (domes-over-doors.md §D4, §D7). Its thrust on those
    walls is worked out; no source sizes the steel for it yet."""
    from kilndesigner.castable import resolve_material

    assert isinstance(kiln.roof, Dome)
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
            Finding(
                level="error",
                message=(
                    f"The dome's ring includes {' and '.join(loose)}, which can't carry a dome: "
                    "the ring must be brick or castable. Set the roof's ring to the layers that "
                    "are."
                ),
                reference=DOME_SOURCE,
            )
        )
        return _unframed(working, findings)
    slices = dome_slices(kiln)
    middle, end = slices[0], slices[-1]

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
    if weak.factor < minimum["safety"]:
        findings.append(
            Finding(
                level="error",
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
    too_thick = [s for s in slices if s.thickness > s.thickest + 1e-9]
    if too_thick:
        worst = max(too_thick, key=lambda s: s.thickness - s.thickest)
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
            Finding(
                level="error",
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
    if steep:
        s = steep[0]
        findings.append(
            Finding(
                level="error",
                message=(
                    f"The dome's slices over the door rise {12 * s.rise / span:.2f} in per foot "
                    f"of span {where(s)}; HarbisonWalker gives {low:g}–{high:g} "
                    "in/ft for a roof arch of this ring."
                ),
                reference=rule["source"],
            )
        )
    # The thrust on the walls the slices span, cold and heated (the heated factor as for a
    # sprung arch, free to rise)
    hot: list[tuple[float, float]] = []
    for s in slices:
        cold = cold_thrust_factor(span, s.rise) * s.weight
        factor = heated_thrust_factor(span, s.rise, s.thickness)
        if factor is None:
            findings.append(
                Finding(
                    level="error",
                    message=(
                        f"Hot, the dome's slice {where(s)} would push its "
                        "thrust line out of the ring: it is too thick for its rise. Raise the dome "
                        "or thin it."
                    ),
                    reference=ARCH_THEORY_SOURCE,
                )
            )
            return _unframed(working, findings)
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
    s_over_t = max(100 * s.thickness / span for s in slices)
    if peak_hot > MAX_PRINTED_HEATED * peak_cold:
        findings.append(
            Finding(
                level="warning",
                message=(
                    f"Hot, the dome's slices push {peak_hot / peak_cold:.1f} times their cold "
                    f"thrust, more than the {MAX_PRINTED_HEATED:g} times HarbisonWalker prints "
                    "before it marks the stress excessive. A higher dome pushes less."
                ),
                reference=ARCH_THEORY_SOURCE,
            )
        )
    if s_over_t > data["heated_factor"]["t_over_s"][-1]:
        findings.append(
            Finding(
                level="warning",
                message=(
                    f"The dome's slices reach T/S {s_over_t:.1f} %, past the 10 % of "
                    "HarbisonWalker's "
                    "heated-arch table, so their hot thrust is worked out from statics past what's "
                    "been checked."
                ),
                reference=ARCH_THEORY_SOURCE,
            )
        )
    findings.append(
        Finding(
            level="warning",
            message=(
                f"The dome pushes out on {walls} with up to {peak_hot:.0f} lb per foot hot, "
                f"{total:.0f} lb along each, and a tie across the door's head and one across the "
                f"wall opposite take {total / 2:.0f} lb each. No source sizes the steel for a "
                "dome, so none is drawn: have it designed for these."
            ),
            reference=DOME_SOURCE,
        )
    )
    return FrameDesign(
        kind=NO_FRAME, angle=None, angle_leg_in=0, angle_t_in=0, rod=None, rod_d_in=0,
        thrust=f"{peak_hot:.0f} lb per foot on {walls}, hot", members=[], working=working,
        findings=findings,
    )  # fmt: skip


def design_frame(kiln: Kiln) -> FrameDesign:
    o = outside(kiln)
    volume_ft3 = chamber_shape(kiln).volume / si(parse_quantity("1 ft**3"), "m**3")
    if isinstance(kiln.roof, CatenaryArch):
        return _catenary_feet(kiln)
    if isinstance(kiln.roof, Dome):
        return _dome_frame(kiln)
    if not isinstance(kiln.roof, SprungArch):
        if kiln.heat.gas is None:
            return _case(kiln, o)
        return _flat_frame(kiln, o)
    working: list[Step] = []
    findings: list[Finding] = []
    data = steel_data()
    limit = float(data["binding_stress_psi"])

    # The smallest angle, from the builders who published theirs
    if kiln.door_kind == "hinged":
        floor = angle("L3×3×1/4") if volume_ft3 <= 24 else angle("L4×4×1/4")
        why = f"hinged door, {volume_ft3:.0f} ft³ ({'≤' if volume_ft3 <= 24 else '>'} 24 ft³)"
    else:
        floor, why = angle("L3×3×3/16"), '"generally adequate" for a studio sprung arch'
    working.append(
        Step(
            name="Smallest frame angle",
            value=floor.name,
            inputs={"because": why},
            reference=PITELKA,
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
    if load.loose:
        findings.append(
            Finding(
                level="error",
                message=(
                    f"The arch's ring includes {' and '.join(load.loose)}, which can't carry an "
                    "arch's thrust: the ring must be brick or castable. Set the roof's ring to the "
                    "layers that are."
                ),
                reference=rule["source"],
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
    # HarbisonWalker's rise for a roof arch, by its brick; the strictest of the ring's
    low, high = rule["general"]
    for kind in load.ring_kinds:
        lo, hi = rule.get(kind, rule["general"])
        low, high = max(low, lo), min(high, hi)
    if not low - 1e-9 <= d <= high + 1e-9:
        findings.append(
            Finding(
                level="error",
                message=(
                    f"The arch rises {d:.2f} in per foot of span. HarbisonWalker gives {low:g}–"
                    f"{high:g} in/ft for a roof arch of this ring: a rise of "
                    f"{low * span_in / 12:.2f}–{high * span_in / 12:.2f} in on this span."
                ),
                reference=rule["source"],
            )
        )
    # HarbisonWalker's thickest ring: ¼ in per foot of span is the lowest the line of thrust may
    # rise, so T ≤ (h − S/48) ÷ cos ½θ
    thickest = (arch.rise - span_in / 48) / math.cos(arch.half_angle)
    working.append(
        Step(
            name="Thickest ring for the rise",
            value=f"{thickest:.2f} in",
            formula="T ≤ (h − S/48) ÷ cos ½θ",
            inputs={
                "h": f"{arch.rise:.2f} in",
                "S": f"{span_in:g} in",
                "½θ": f"{math.degrees(arch.half_angle):.1f}°",
            },
            reference=consts["source"],
        )
    )
    if load.ring > thickest + 1e-9:
        findings.append(
            Finding(
                level="error",
                message=(
                    f"The arch's {load.ring:g} in ring is thicker than HarbisonWalker allows for "
                    f"its rise, {max(thickest, 0):.2f} in: the line of thrust would drop too low. "
                    "Raise the arch or thin the ring."
                ),
                reference=consts["source"],
            )
        )
    # The skewback needs the wall under it: the ring's outer corner must be within the side walls
    corner, wall = ring_outside(kiln), span_in / 2 + min(o.left, o.right)
    if corner > wall + 1e-6:
        findings.append(
            Finding(
                level="error",
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
    if heated is None:
        findings.append(
            Finding(
                level="error",
                message=(
                    "Hot, this arch's thrust line would leave the ring: it is too thick for its "
                    f"rise (T/S {t_over_s:.1f} %, {d:.2f} in/ft), so no steel can be sized for it. "
                    "Raise the arch or thin the ring."
                ),
                reference=ARCH_THEORY_SOURCE,
            )
        )
        return _unframed(working, findings)
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
    rigid = thrust
    if kiln.roof.ties == "springs":
        thrust = _sprung_ties(kiln, span_in, cold, rigid, o, working, findings)
    in_table = (
        heated_table["t_over_s"][0] <= t_over_s <= heated_table["t_over_s"][-1]
        and consts["d"][0] <= d <= consts["d"][-1]
    )
    if thrust < rigid - 1e-9:
        pass  # the springs set the hot thrust, not the rigid frame's statics
    elif heated > MAX_PRINTED_HEATED:
        # Only a guard: HarbisonWalker's own rise and thickness rules are the limits
        findings.append(
            Finding(
                level="warning",
                message=(
                    f"Hot, this arch pushes {heated:.1f} times its cold thrust, more than the "
                    f"{MAX_PRINTED_HEATED:g} times HarbisonWalker prints before it marks the "
                    "stress "
                    "excessive. The steel is sized for it; a higher arch pushes less."
                ),
                reference=ARCH_THEORY_SOURCE,
            )
        )
    elif not in_table:
        findings.append(
            Finding(
                level="warning",
                message=(
                    f"The heated thrust is worked out from statics. HarbisonWalker's table, which "
                    f"it matches to 4 %, covers T/S 4–10 % and 1–3 in/ft; this arch, at "
                    f"{t_over_s:.1f} % and {d:.2f} in/ft, is outside it, so the steel is sized "
                    "past what's been checked."
                ),
                reference=ARCH_THEORY_SOURCE,
            )
        )

    chosen = floor
    rod = data["rods"]["sizes"][1]  # ½-13, what builders use [S7] [S17]
    length = o.depth  # the buttress spans between the corner posts
    moment = (thrust / 12) * length**2 / 8
    needed = moment / limit
    fits = [a for a in angles() if a.sx >= needed and a.leg >= floor.leg and a.t >= floor.t]
    if not fits:
        findings.append(
            Finding(
                level="error",
                message=(
                    f"No angle up to L4×4×3/8 carries the arch's thrust over {length:.0f} in "
                    "between the corner posts. Add posts along the side walls."
                ),
                reference=data["angles"]["source"],
            )
        )
    else:
        chosen = fits[0]
    working.append(
        Step(
            name="Buttress angle, bending",
            value=f"needs Sx ≥ {needed:.3f} in³; {chosen.name} has {chosen.sx:.3f} in³",
            formula="M = wL²/8, Sx = M ÷ 12,000 psi (a simple beam between the corner posts)",
            inputs={
                "w": f"{thrust / 12:.2f} lb/in",
                "L": f"{length:.1f} in",
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
    per_rod = thrust * (o.depth / 12) / 2
    for size in data["rods"]["sizes"][1:]:
        rod = size
        if per_rod / size["stress_area"] <= limit:
            break
    else:
        findings.append(
            Finding(level="error", message="No rod up to ¾ in carries the arch's thrust.")
        )
    working.append(
        Step(
            name="Tie rods, one at the front and one at the back",
            value=f"{rod['name']}: {per_rod / rod['stress_area']:,.0f} psi",
            formula="thrust × length ÷ 2 rods ÷ tensile stress area",
            inputs={
                "load per rod": f"{per_rod:,.0f} lb",
                "stress area": f"{rod['stress_area']} in²",
            },
            reference=f"{data['rods']['source']}; {data['binding_stress_source']}",
            note="½ in is the smallest used here, because builders use it (kiln-hardware.md "
            "§4.2 [S7] [S17]).",
        )
    )

    top = skewback_top(kiln)
    leg = chosen.leg
    members = [
        Member(
            part="corner posts",
            steel=chosen.name,
            count=4,
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
            count=2,
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
    )


GROWTH_IN_PER_FT = 3 / 32  # the most brickwork grows hot: Olsen 4th ed. p.51 (1/16–3/32 in/ft)
GROWTH_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.51: 1/16–3/32 in per ft (0.5–0.8 %), with IFB's 0.5–0.7 % "
    "reversible expansion (thermal-properties.md §2); olsen-kiln-book.md"
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
    assert isinstance(kiln.roof, SprungArch) and kiln.roof.spring_rate is not None
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
    if 4 * depth / (3 * span) > FRICTION:
        findings.append(
            Finding(
                level="error",
                message=(
                    f"The flat roof is {depth:g} in deep over {span:g} in: too deep for its span "
                    "to "
                    "hold at its ends by friction. BIA's jack arches need the span more than about "
                    f"2.2 times the depth, at the friction of {FRICTION:g} it gives for brick "
                    "(none "
                    "is sourced for insulating firebrick). Make it thinner or use an arch."
                ),
                reference=FLAT_SOURCE,
            )
        )
    if span > FLAT_LONGEST_IN:
        findings.append(
            Finding(
                level="error",
                message=(
                    f"A flat roof over {span:g} in is longer than any flat brick roof in the "
                    "sources, "
                    f"about {FLAT_LONGEST_IN:g} in. Use an arch or a dome."
                ),
                reference="flat-roofs.md §4.5",
            )
        )
    elif span > FLAT_CHECKED_IN:
        findings.append(
            Finding(
                level="warning",
                message=(
                    f"The flat roof spans {span:g} in, past the longest one-way flat roof in the "
                    f"sources, Merrill's {FLAT_CHECKED_IN:g} in; flat lids of about "
                    f"{FLAT_LONGEST_IN:g} "
                    "in rest on all four walls, and makers move to fibre there."
                ),
                reference="flat-roofs.md §4.1, §4.3",
            )
        )
    top = si(top_temperature(kiln)[0], "degF")
    if slab.kind == "insulating_firebrick" and top > FLAT_IFB_TOP_F:
        findings.append(
            Finding(
                level="warning",
                message=(
                    f"BNZ keeps flat insulating-firebrick roofs to {FLAT_IFB_TOP_F:g} °F, where "
                    f"IFB still holds together; this kiln reaches {top:.0f} °F. It says to use a "
                    "sprung arch above that."
                ),
                reference="flat-roofs.md §4.4 [F15]",
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
                    "the roof's thrust × 4½ in, a row of Merrill's brick, ÷ the rod's tensile "
                    "stress area"
                ),
                reference=f"{MERRILL}; {steel_data()['binding_stress_source']}",
            )
        )
        if stress > float(steel_data()["binding_stress_psi"]):
            findings.append(
                Finding(
                    level="error",
                    message=(
                        f"A 3/8 in rod every 4½ in across the roof would carry {stress:,.0f} psi, "
                        "past HarbisonWalker's 12,000 psi for hot steel. Use a thinner or lighter "
                        "roof, or an arch."
                    ),
                    reference=steel_data()["binding_stress_source"],
                )
            )
    members = [
        Member(
            part="corner posts",
            steel=a.name,
            count=4,
            length_in=o.bottom + o.wall_top,
            source=MERRILL,
        ),
        *_ring_of(a.name, "roof angle", o, a.leg, MERRILL),
        Member(
            part="rods across the roof, one every 4½ in",
            steel="3/8-16 threaded rod",
            count=rows,
            length_in=(o.width if across else o.depth) + 2 * a.leg + 4,
            source=MERRILL,
        ),
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


CASE_T = 0.125  # in, L&L's welded case [S6]


def _case(kiln: Kiln, o: Outside) -> FrameDesign:
    """An electric kiln in a welded steel case, as the makers build them: a plate on each wall but
    the door's."""
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
        findings.append(
            Finding(
                level="warning",
                message=(
                    f"The case, or a band round the roof, must squeeze it across its span with "
                    f"about {thrust * 12:.0f} lb per foot, cold. No source gives a band's size or "
                    "tension for a kiln roof, so none is drawn: have it designed."
                ),
                reference="flat-roofs.md §3",
            )
        )
    return FrameDesign(
        kind="welded case",
        angle=None,
        angle_leg_in=0,
        angle_t_in=CASE_T,
        rod=None,
        rod_d_in=0,
        thrust=None if thrust is None else f"{thrust * 12:.0f} lb per foot of roof, cold",
        members=plates,
        working=working,
        findings=findings,
    )
