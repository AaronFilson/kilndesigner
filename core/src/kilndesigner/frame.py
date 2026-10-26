"""The steel that holds a kiln together: a frame for a sprung arch, or an electric kiln's case.

A sprung arch pushes out on its skewbacks, and the frame must take that thrust: buttress angles
along the top of the side walls, held at their ends by corner posts tied across the kiln by
threaded rod (kiln-hardware.md §4.1). The thrust comes from HarbisonWalker's arch method
(§4.3 [S20]); the steel is checked against HarbisonWalker's 12,000 psi limit for bindings that may
run hot, with the angle's section modulus from AISC (§4.7). No source relates frame steel to arch
span, so the builders' published sizes (Pitelka [S11]) set the smallest angle, and the thrust check
can only make it bigger.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import cache
from importlib import resources
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict

from kilndesigner.model import Kiln, SprungArch
from kilndesigner.shape import Arch, chamber_shape
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
    sx: float  # in³


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
    top = h if isinstance(kiln.roof, SprungArch) else h + t("roof")
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


def _arch_weight(kiln: Kiln, arch: Arch) -> tuple[float, float, list[str]]:
    """The arch's weight per foot of length (lb/ft) and its load-bearing thickness (in): every
    layer's density × thickness × mean arc, the exact form of HarbisonWalker's W (§4.6)."""
    from kilndesigner.castable import resolve_material

    weight = 0.0
    solid = 0.0
    lines: list[str] = []
    r = arch.radius
    for layer in kiln.lining.for_face("roof"):
        m = resolve_material(kiln, layer.material)
        rho = si(parse_quantity(m.density), "lb/ft**3")
        t = si(layer.thickness, "in")
        mean_arc_ft = (r + t / 2) * 2 * arch.half_angle / 12
        wt = rho * (t / 12) * mean_arc_ft
        weight += wt
        if m.kind not in ("fibre_blanket", "fibre_board", "backup_insulation"):
            solid += t
        lines.append(f"{m.name}: {rho:.0f} lb/ft³ × {t:g} in × {mean_arc_ft:.2f} ft = {wt:.1f}")
        r += t
    return weight, solid, lines


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


def design_frame(kiln: Kiln) -> FrameDesign:
    o = outside(kiln)
    volume_ft3 = chamber_shape(kiln).volume / si(parse_quantity("1 ft**3"), "m**3")
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
    weight, solid_t, lines = _arch_weight(kiln, arch)
    working.append(
        Step(
            name="Arch weight per foot of length",
            value=f"{weight:.1f} lb/ft",
            formula="Σ density × thickness × mean arc, over the roof's layers",
            inputs={f"layer {i + 1}": s for i, s in enumerate(lines)},
            reference="HarbisonWalker W, exact form; kiln-hardware.md §4.6 [S20]",
            note="Includes insulation laid on the arch, which HarbisonWalker's tables leave out.",
        )
    )
    consts = data["arch_constants"]
    heated_table = data["heated_factor"]
    thrust: float | None = None
    t_over_s = 100 * solid_t / span_in
    if not 0 < arch.rise < span_in / 2:
        findings.append(
            Finding(
                level="error",
                message=(
                    f"The arch's rise of {arch.rise:.2f} in must be above 0 and below half the "
                    f"{span_in:.1f} in span for a segmental arch, so the frame can't be checked."
                ),
                reference=consts["source"],
            )
        )
    else:
        h_factor = cold_thrust_factor(span_in, arch.rise)
        cold = h_factor * weight
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
        thrust = cold
        heated = heated_thrust_factor(span_in, arch.rise, solid_t)
        if heated is None or heated > MAX_PRINTED_HEATED:
            findings.append(
                Finding(
                    level="error",
                    message=(
                        "Hot, this arch's thrust line would "
                        + (
                            "leave the brick: it is too thick for its rise"
                            if heated is None
                            else f"push {heated:.1f} times its cold thrust"
                        )
                        + f" (T/S {t_over_s:.1f} %, {d:.2f} in/ft). HarbisonWalker marks the "
                        f"stress excessive past about {MAX_PRINTED_HEATED:g} times. Raise the arch."
                    ),
                    reference=ARCH_THEORY_SOURCE,
                )
            )
        else:
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
            in_table = (
                heated_table["t_over_s"][0] <= t_over_s <= heated_table["t_over_s"][-1]
                and consts["d"][0] <= d <= consts["d"][-1]
            )
            if not in_table:
                findings.append(
                    Finding(
                        level="info",
                        message=(
                            f"The heated thrust is worked out from statics. HarbisonWalker's "
                            f"table, which it matches to 4 %, covers T/S 4–10 % and 1–3 in/ft; "
                            f"this arch, at {t_over_s:.1f} % and {d:.2f} in/ft, is outside it."
                        ),
                        reference=ARCH_THEORY_SOURCE,
                    )
                )

    chosen = floor
    rod = data["rods"]["sizes"][1]  # ½-13, what builders use [S7] [S17]
    if thrust is not None:
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
                    f"{data['binding_stress_source']}; AISC Sx, kiln-hardware.md §4.7.1 [S28]"
                ),
                note="A cautious first check, derived in kiln-hardware.md §4.5; not a sourced "
                "design rule.",
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
        Member(
            part="bottom cross-members, all four sides",
            steel=FLAT_BAR,
            count=4,
            length_in=o.width + o.depth + 4 * leg,
            source=PITELKA,
        ),
        Member(
            part="tie rods",
            steel=f"{rod['name']} threaded rod",
            count=2,
            length_in=o.width + 2 * leg + 4,
            source=f"length: {MERRILL}",
        ),
    ]
    if not any(f.level == "error" for f in findings) and thrust is not None:
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
        thrust=None if thrust is None else f"{thrust:.0f} lb per foot of arch",
        members=members,
        working=working,
        findings=findings,
    )


def _flat_frame(kiln: Kiln, o: Outside) -> FrameDesign:
    """A gas kiln with a flat roof: angle round the roof, rods across (Merrill's flat-top)."""
    a = angle("L2×2×3/16")
    members = [
        Member(
            part="corner posts",
            steel=a.name,
            count=4,
            length_in=o.bottom + o.wall_top,
            source=MERRILL,
        ),
        Member(
            part="roof angle, all four sides",
            steel=a.name,
            count=4,
            length_in=o.width + o.depth + 4 * a.leg,
            source=MERRILL,
        ),
        Member(
            part="tie rods",
            steel="3/8-16 threaded rod",
            count=2,
            length_in=o.width + 2 * a.leg + 4,
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
        thrust=None,
        members=members,
        working=[Step(name="Frame", value=f"{a.name} with 3/8 in rods", reference=MERRILL)],
        findings=[],
    )


CASE_T = 0.125  # in, L&L's welded case [S6]


def _case(kiln: Kiln, o: Outside) -> FrameDesign:
    """An electric kiln in a welded steel case, as the makers build them."""
    plates = [
        Member(
            part="side and back plates",
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
    return FrameDesign(
        kind="welded case",
        angle=None,
        angle_leg_in=0,
        angle_t_in=CASE_T,
        rod=None,
        rod_d_in=0,
        thrust=None,
        members=plates,
        working=[Step(name="Case", value="welded ⅛ in steel", reference=CASE_SOURCE)],
        findings=[],
    )
