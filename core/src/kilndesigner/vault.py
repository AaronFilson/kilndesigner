"""Vaults whose section changes along the chamber: an arch spanning the chamber's depth, front to
back, so that the section across the width rises from the springline at the end walls to the crown
mid-way (Olsen's Bowen Mountain salt kiln, 4th ed. Fig 4-153, ``roof.along``; and each chamber of
a climbing kiln, p.94–95).

The section is given at stations along the depth, from the arch's circle, and the statics are
Heyman's, as the door arches' are (door.py): the ring against the thinnest arch of its half-angle
that holds a line of thrust, the hot line of thrust inside the ring, and each end wall, where the
arch springs, as a buttress holding the arch's thrust and half its weight (frame_checks).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from kilndesigner.frame_checks import (
    ArchInputs,
    Layer,
    hot_thrust_line,
    vault_end_wall,
    vault_end_wall_uneven,
    vault_ring,
)
from kilndesigner.model import Face, Kiln, SprungArch, arches_along
from kilndesigner.shape import Arch, along_arch
from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_, parse_quantity, si
from kilndesigner.working import Finding, Step

STATIONS = 8
"""Stations along one chamber's depth, end wall to end wall, at which its section is given."""
BOWEN = "Olsen, The Kiln Book, 4th ed., Fig 4-153 (Bowen Mountain), p.94–95 (climbing kilns)"
BRACING = (
    "Olsen, The Kiln Book, 4th ed., p.97: bracing a chamber kiln's firebox and front chamber 'is a "
    "must'; Fig 4-153 draws Bowen Mountain's 'BRACING' on the front wall at the springing"
)


def _layers(kiln: Kiln, face: Face) -> tuple[Layer, ...]:
    from kilndesigner.castable import resolve_material

    return tuple(
        Layer(m.name, si(parse_quantity(m.density), "lb/ft**3"), si(x.thickness, "in"))
        for x in kiln.lining.for_face(face)
        for m in [resolve_material(kiln, x.material)]
    )


UNEVEN = (
    "Olsen, The Kiln Book, 4th ed., Fig 4-153: Bowen Mountain's back springing printed 18 in, its "
    "front read about 16 in (2026-10-31); the circle through both springings, its crown the rise "
    "over the back's"
)
TRUNCATED = (
    "an arch springing unevenly is the level arch of its lower springing's angle, on the same "
    "circle, cut off at the higher springing: a line of thrust within the whole lies within the "
    "part, the cut face taking the force the line carries there (Heyman's safe theorem), so the "
    "larger angle is checked"
)
THINNER = (
    "the door's opening cuts into the vault's inside over the door: the vault still holds the "
    "concentric ring from the cut's top to its outside, which is checked; a line of thrust within "
    "that ring lies within the notched one (Heyman's safe theorem)"
)


def uneven_thrust(arch: Arch, weight: float) -> tuple[float, float, float]:
    """An arch springing unevenly, three-hinged at its springings and its crown, its weight per
    foot ``weight`` spread along the arc: its thrust H and each springing's vertical load,
    front and back. Each half's moments about the crown, with its centroid r(1 − cos φ)/φ in from
    it, and the two vertical loads summing to the weight:
    H = (W_f·ℓ_f/s_f + W_b·ℓ_b/s_b)/(f_f/s_f + f_b/s_b), V = (H·f + W·(s − ℓ))/s, with
    s = sin φ, f = 1 − cos φ, ℓ = sin φ − (1 − cos φ)/φ (all over r). Level, it is the level
    arch's H and W/2 each."""
    angles = (arch.front_angle, arch.back_angle)
    whole = sum(angles)
    halves = [(weight * p / whole, math.sin(p), 1 - math.cos(p), p) for p in angles]
    lever = [(w, s, f, s - f / p) for w, s, f, p in halves]
    h = sum(w * ell / s for w, s, _, ell in lever) / sum(f / s for _, s, f, _ in lever)
    front, back = ((h * f + w * (s - ell)) / s for w, s, f, ell in lever)
    return h, front, back


THRUST_LINE = (
    "a line of thrust through both springings at their own heights and the crown (Heyman's safe "
    "theorem: any such line within the masonry is in equilibrium; the hinges fix this one). With "
    "vertical loads only, H is the same all along the arch, so moments of the whole arch about "
    "the lower springing and of the higher half about the crown give it (standard statics; "
    "blocked-items.md §9)"
)


def thrust_line_thrust(arch: Arch, weight: float) -> tuple[float, float, float]:
    """The same arch as uneven_thrust's, worked the second way (THRUST_LINE): moments of the
    whole arch about the front (lower) springing, the back springing ``arch.drop`` above it, and
    of the back half about the crown. Over r, the front springing at (−s_f, −f_f) from the crown,
    the back at (s_b, −f_b), each half's weight W·φ/(φ_f + φ_b) at c = (1 − cos φ)/φ from it:
    V_b·(s_f + s_b) + H·δ = W_f·(s_f − c_f) + W_b·(s_f + c_b), δ = drop/r;
    V_b·s_b = H·f_b + W_b·c_b. Returns H, V_f, V_b."""
    pf, pb = arch.front_angle, arch.back_angle
    wf, wb = (weight * p / (pf + pb) for p in (pf, pb))
    sf, sb = math.sin(pf), math.sin(pb)
    fb = 1 - math.cos(pb)
    cf, cb = ((1 - math.cos(p)) / p for p in (pf, pb))
    delta = arch.drop / arch.radius
    about = wf * (sf - cf) + wb * (sf + cb)  # the loads' moment about the front springing
    h = (sb * about / (sf + sb) - wb * cb) / (fb + sb * delta / (sf + sb))
    back = (h * fb + wb * cb) / sb
    return h, weight - back, back


def along_inputs(kiln: Kiln, cut: float = 0.0) -> ArchInputs:
    """The arch along the chamber's depth, as the frame's sheets take an arch (in). Springing
    unevenly, the level arch on the same circle at the larger angle (TRUNCATED); with ``cut``, the
    thinner ring left over a door cut that far into its inside (THINNER)."""
    assert isinstance(kiln.roof, SprungArch)
    assert arches_along(kiln)
    layers = _layers(kiln, "roof")
    arch = along_arch(kiln, "in")
    if not arch.drop and not cut:
        return ArchInputs(arch.span, arch.rise, layers, kiln.roof.ring)
    phi = max(arch.front_angle, arch.back_angle)
    r = arch.radius + cut
    if cut:
        left, out = cut, []
        for i, x in enumerate(layers):
            take = min(left, x.thickness) if i < kiln.roof.ring else 0.0
            out.append(Layer(x.name, x.density, x.thickness - take))
            left -= take
        layers = tuple(out)
    return ArchInputs(2 * r * math.sin(phi), r * (1 - math.cos(phi)), layers, kiln.roof.ring)


def stations(kiln: Kiln) -> list[tuple[float, float]]:
    """The chamber's inside height (in) at stations along one chamber's depth, from its front end
    wall (in): the arch's circle over the springlines."""
    arch = along_arch(kiln, "in")
    h = si(kiln.chamber.height, "in")
    out: list[tuple[float, float]] = []
    for k in range(STATIONS + 1):
        y = arch.span * k / STATIONS
        out.append((y, h + arch.height(y - arch.span / 2)))
    return out


def along_statics(kiln: Kiln) -> tuple[list[Step], list[Finding]]:
    """The section at stations, and Heyman's statics of the arch along the depth and its end
    walls: the working and the findings."""
    from kilndesigner.frame import steel_data

    whole = along_arch(kiln, "in")
    into = door_in_vault(kiln)
    cut = into.cut if into is not None else 0.0
    a = along_inputs(kiln, cut)
    arch = Arch(a.span, a.rise)
    working: list[Step] = []
    findings: list[Finding] = []
    sections = stations(kiln)
    h = si(kiln.chamber.height, "in")
    inputs = {
        "span S, the chamber's depth": f"{whole.span:g} in",
        "rise ρ": f"{whole.rise:g} in",
        "springline h": f"{h:g} in" + (" at the back" if whole.drop else ""),
    }
    if whole.drop:
        inputs["springline at the front"] = f"{h - whole.drop:g} in"
    working.append(
        Step(
            name="The chamber's section along its depth",
            value=", ".join(f"{z:.1f} in at {y:g} in" for y, z in sections),
            formula=(
                "z(y) = h + ρ − R + √(R² − (y − y_c)²), the circle through (0, h − δ) and (S, h) "
                f"with its top h + ρ: R = {whole.radius:.2f} in, "
                f"y_c = {whole.span / 2 + whole.offset:.2f} in"
                if whole.drop
                else "z(y) = h + ρ − R + √(R² − (y − S/2)²), R = (S²/4 + ρ²)/2ρ"
            ),
            inputs=inputs,
            reference=BOWEN + (f"; {UNEVEN}" if whole.drop else ""),
            note=(
                "The arch spans front to back, so the section across the width is a rectangle as "
                "tall as the arch at that station; the side walls are filled up to it."
            ),
        )
    )
    minimum = steel_data()["arch_minimum_thickness"]
    phi = math.degrees(arch.half_angle)
    eta = float(np.interp(phi, minimum["half_angle_deg"], minimum["eta"]))
    ring = vault_ring(a, eta, minimum["safety"], minimum["source"])
    t = sum(x.thickness for x in a.layers[: a.ring])
    k = t / (arch.radius + t / 2) / eta
    ring.agrees("k", k)
    line = hot_thrust_line(a)
    ends = _end_walls(kiln, whole)
    x_r, e, x_3 = (ends[0][1].env[n] / 0.0254 for n in ("x_R", "e", "x_3"))
    walls = (
        "; ".join(
            f"on the {face} wall the resultant {s.env['x_R'] / 0.0254:.1f} in into its "
            f"{s.env['e'] / 0.0254:g} in base (middle third to {s.env['x_3'] / 0.0254:.1f} in)"
            for face, s in ends
        )
        if whole.drop
        else f"on each end wall the cold thrust carries the resultant {x_r:.1f} in into its "
        f"{e:g} in base (middle third to {x_3:.1f} in)"
    )
    notes = [
        "Geometry and loads alone, so no range of T/S limits it. The end wall is taken standing "
        "on its own, the fill over the skewback left out: the steadier case is spare. The hot "
        "thrust, the arch pressed between braced walls, is the frame's."
    ]
    if whole.drop:
        notes.append(f"The ring: {TRUNCATED}.")
    if cut:
        notes.append(f"The door: {THINNER}, {cut:.2f} in.")
    working.append(
        Step(
            name="The arch along the depth: Heyman's statics",
            value=(
                f"a {t:.4g} in ring over {whole.span:g} in, {k:.1f} times the thinnest that stands "
                f"(half-angle {phi:.1f}°); {walls}"
            ),
            formula=(
                "k = T/(r + T/2) ÷ η(φ) ≥ 2; x_R = (N·x_p + G·e/2 + H_c·y_p)/(N + G) ≤ e, "
                + (
                    "N each springing's share, H_c the uneven three-hinged arch's"
                    if whole.drop
                    else "N = W/2"
                )
                + ", G the wall under the springline"
            ),
            reference="; ".join(
                f"{x}" for x in [ring.reference, *dict.fromkeys(s.reference for _, s in ends)]
            ),
            note=" ".join(notes),
        )
    )
    for sheet, message in (
        (ring, f"The arch's {t:g} in ring is {k:.1f} times the thinnest that holds a line of "
         f"thrust at its half-angle, less than Heyman's {minimum['safety']}: thicken the ring or "
         "raise the arch."),
        (line, "The arch's hot line of thrust leaves its ring at the skewback: the ring is too "
         "thick for its rise; raise the arch or thin the ring."),
    ):  # fmt: skip
        if (check := sheet.check()).status != "pass":
            findings.append(Finding.failed(check, message=message))
    for face, end in ends:
        which = f"The {face} wall" if whole.drop else "Each end wall"
        findings.append(_end_finding(end, which))
    return working, findings


def _end_finding(end: Sheet, which: str) -> Finding:
    x_r, e, x_3 = (end.env[n] / 0.0254 for n in ("x_R", "e", "x_3"))
    check = end.check()
    holds = check.status == "pass"
    return Finding(
            level="info",
            message=(
                f"{which}, standing on its own, "
                + (
                    f"holds the arch's cold thrust: the resultant meets its {e:g} in base "
                    f"{x_r:.1f} in in from the inside, within its middle third. Brace it for the "
                    "hot thrust all the same"
                    if holds
                    else f"can't hold the arch's cold thrust: the resultant would meet its base "
                    f"{x_r:.1f} in in from the inside, "
                    + ("past the wall" if x_r > e else f"past its middle third, {x_3:.1f} in")
                    + ". The bracing at the springing carries it, so it is needed, not optional"
                )
                + ": Olsen braces a chamber kiln's front, and Bowen Mountain's drawing shows it. "
                "No source sizes that bracing, so it isn't sized here."
            ),
            reference=f"{end.reference}; {BRACING}",
            check=check,
        )  # fmt: skip


INTO_VAULT = (
    "a door in a side wall under an arch along the chamber's depth, its head rising into the "
    "vault's edge: the door's ring is the masonry round its head up to the vault's outside, the "
    "side wall's fill and the vault's ring together, laid as the vault's (Olsen lays a door's ring "
    "arch 'in exactly the same way as' the chamber's, door-headers.md §D4; Tamba's doors are "
    "turned in the vault's own brickwork, Figs 4-11, 4-15). Bowen Mountain's door is 36 in tall "
    "under a vault meeting the side wall 33.8 in up at its jambs (Fig 4-153, read by the user, "
    "2026-10-31)"
)
SUPERPOSED = (
    "Heyman's safe theorem, the static theorem of limit analysis: two states of thrust each in "
    "equilibrium with its own loads and each within the masonry add to one within it, compression "
    "plus compression; so the vault, its ring checked whole (less any cut), carries itself to its "
    "end walls, and the door's ring carries the fill over the door. The vault's ring over the door "
    "is counted in both: the safe side for the door's ring"
)


@dataclass(frozen=True)
class DoorInVault:
    """A door in a side wall under one chamber's arch along its depth whose arched head, with its
    ring, rises into the vault (in): how far the opening cuts into the vault's inside, the least
    depth of masonry round the head up to the vault's outside (the door's ring, at most the ring
    asked for), the springing, and the jambs: how far each runs along the wall, from the door's
    edge, before the wall's top drops under the springing."""

    cut: float
    ring: float
    springing: float
    radius: float
    jambs: tuple[float, float]
    jamb_tops: tuple[float, float]
    vault_ring: float


def door_in_vault(kiln: Kiln) -> DoorInVault | None:
    """The door's head in the vault's edge (INTO_VAULT), or None when the door and its ring stand
    under the vault, or it isn't such a door."""
    door, roof = kiln.loading.opening, kiln.roof
    if (
        door is None
        or door.head != "arch"
        or not isinstance(roof, SprungArch)
        or not roof.along
        or kiln.loading.face not in ("left", "right")
    ):
        return None
    arch = along_arch(kiln, "in")
    h = si(kiln.chamber.height, "in")
    roof_ring = sum(si(x.thickness, "in") for x in kiln.lining.for_face("roof")[: roof.ring])
    ring = si(door.ring, "in") if door.ring is not None else roof_ring
    r = si(door.width, "in") / 2
    across = si(door.across, "in")
    u_d = across if kiln.loading.face == "right" else -across  # along y, from the middle
    springing = si(door.sill, "in") + si(door.height, "in") - r
    centre_z = h + arch.rise - arch.radius

    def inside(u: float) -> float:
        if abs(u) >= arch.span / 2:  # past the arch's ends: the end walls' springlines
            return h - max(arch.drop, 0.0)
        return h + arch.height(u)

    def outside(u: float) -> float:
        v = (arch.radius + roof_ring) ** 2 - (u - arch.offset) ** 2
        return centre_z + math.sqrt(v) if v > 0 else math.inf

    angles = [float(t) for t in np.radians(np.linspace(-90.0, 90.0, 181))]
    reaches = any(
        springing + (r + ring) * math.cos(t) > inside(u_d + (r + ring) * math.sin(t)) + 1e-9
        for t in angles
    )
    if not reaches:
        return None
    cut = max(0.0, *(springing + r * math.cos(t) - inside(u_d + r * math.sin(t)) for t in angles))
    depth = ring
    for t in angles:
        s, c = math.sin(t), math.cos(t)
        for k in range(1, 201):  # out along the radius, 1/200 of the ring at a time
            rho = r + ring * k / 200
            if springing + rho * c > outside(u_d + rho * s):
                depth = min(depth, rho - r - ring / 200)
                break
    half = arch.span / 2
    lean = springing - centre_z
    reach = math.sqrt(max(arch.radius**2 - lean**2, 0.0)) if lean < arch.radius else 0.0
    edges = (u_d - r, u_d + r)
    # The wall's top drops under the springing where the arch does, or at the end wall
    stops = (max(arch.offset - reach, -half), min(arch.offset + reach, half))
    jambs = (edges[0] - stops[0], stops[1] - edges[1])
    return DoorInVault(
        cut=cut,
        ring=depth,
        springing=springing,
        radius=r,
        jambs=(max(jambs[0], 0.0), max(jambs[1], 0.0)),
        jamb_tops=(inside(edges[0]), inside(edges[1])),
        vault_ring=roof_ring,
    )


TAMBA = (
    "Olsen, The Kiln Book, 4th ed., Figs 4-11, 4-14, 4-15 (p.86–87): Tamba's doors rise through "
    "the springing of the tube's vault, its own brickwork turned as an arch over each, with a "
    "'SUPPORTING WALL IN FRONT OF ALL DOORS'; door-openings.md"
)


def through_springing(kiln: Kiln) -> bool:
    """A door in part of a tube's side wall: it rises through the springing of the tube's vault,
    which is turned as an arch over it (Tamba, Figs 4-11, 4-15)."""
    roof = kiln.roof
    return (
        isinstance(roof, SprungArch)
        and roof.tube
        and kiln.loading.opening is not None
        and kiln.loading.face in ("left", "right")
    )


def vault_on_door(kiln: Kiln) -> tuple[float, float]:
    """What the tube's vault puts on a door through its springing, per foot along the tube
    (lb/ft): half its weight, down on the door's arch, and its thrust, cold (the three-hinged
    arch's H), out against the masonry beside the door. Statics of the vault's section: with the
    wall under it cut away, its foot over the door stands on the door's ring."""
    from kilndesigner.frame import _arch_load, cold_thrust_factor  # pyright: ignore[reportPrivateUsage]

    span, rise = si(kiln.chamber.width, "in"), si(kiln.roof.rise, "in")  # pyright: ignore[reportAttributeAccessIssue]
    load = _arch_load(kiln, Arch(span, rise))
    return load.weight / 2, cold_thrust_factor(span, rise) * load.weight


def _end_walls(kiln: Kiln, whole: Arch) -> list[tuple[Face, Sheet]]:
    """The end walls' sheets, their numbers checked against the engine's own arch (shape.Arch):
    level, the thinner of the front and back walls; springing unevenly, each wall at its own
    springline, under its own share of the arch."""
    ends: tuple[Face, Face] = ("front", "back")
    h = si(kiln.chamber.height, "in")
    if not whole.drop:
        a = along_inputs(kiln)
        walls = [_layers(kiln, f) for f in ends]
        thinner = min(walls, key=lambda w: sum(x.thickness for x in w))
        sheet = vault_end_wall(a, thinner, h)
        sheet.agrees("r", Q_(Arch(a.span, a.rise).radius, "in"))
        return [("front", sheet)]
    assert isinstance(kiln.roof, SprungArch)
    from kilndesigner.frame import _arch_load  # pyright: ignore[reportPrivateUsage]

    thrust, *down = uneven_thrust(whole, _arch_load(kiln, whole).weight)
    out: list[tuple[Face, Sheet]] = []
    for face, springing, v in zip(ends, (h - whole.drop, h), down, strict=True):
        sheet = vault_end_wall_uneven(
            whole.radius, math.degrees(whole.front_angle), math.degrees(whole.back_angle),
            _layers(kiln, "roof"), kiln.roof.ring, _layers(kiln, face), springing, face,
            f"the engine's circle through both springings (vault.py); {UNEVEN}",
        )  # fmt: skip
        sheet.agrees("H_c", Q_(thrust, "lbf/ft"))
        sheet.agrees("N", Q_(v, "lbf/ft"))
        out.append((face, sheet))
    return out


__all__ = ["along_inputs", "along_statics", "stations", "through_springing", "vault_on_door"]
