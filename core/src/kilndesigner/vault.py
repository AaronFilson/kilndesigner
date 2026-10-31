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

import numpy as np

from kilndesigner.frame_checks import (
    ArchInputs,
    Layer,
    hot_thrust_line,
    vault_end_wall,
    vault_ring,
)
from kilndesigner.model import Face, Kiln, SprungArch, arches_along
from kilndesigner.shape import Arch
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


def along_inputs(kiln: Kiln) -> ArchInputs:
    """The arch along the chamber's depth, as the frame's sheets take an arch (in)."""
    assert isinstance(kiln.roof, SprungArch)
    assert arches_along(kiln)
    span, rise = si(kiln.chamber.depth, "in"), si(kiln.roof.rise, "in")
    return ArchInputs(span, rise, _layers(kiln, "roof"), kiln.roof.ring)


def stations(kiln: Kiln) -> list[tuple[float, float]]:
    """The chamber's inside height (in) at stations along one chamber's depth, from its front end
    wall (in): the arch's circle over the springline."""
    a = along_inputs(kiln)
    arch = Arch(a.span, a.rise)
    h = si(kiln.chamber.height, "in")
    centre = h + arch.rise - arch.radius
    out: list[tuple[float, float]] = []
    for k in range(STATIONS + 1):
        y = a.span * k / STATIONS
        u = y - a.span / 2
        out.append((y, centre + math.sqrt(arch.radius**2 - u * u)))
    return out


def along_statics(kiln: Kiln) -> tuple[list[Step], list[Finding]]:
    """The section at stations, and Heyman's statics of the arch along the depth and its end
    walls: the working and the findings."""
    from kilndesigner.frame import steel_data

    a = along_inputs(kiln)
    arch = Arch(a.span, a.rise)
    working: list[Step] = []
    findings: list[Finding] = []
    sections = stations(kiln)
    working.append(
        Step(
            name="The chamber's section along its depth",
            value=", ".join(f"{z:.1f} in at {y:g} in" for y, z in sections),
            formula="z(y) = h + ρ − R + √(R² − (y − S/2)²), R = (S²/4 + ρ²)/2ρ",
            inputs={
                "span S, the chamber's depth": f"{a.span:g} in",
                "rise ρ": f"{a.rise:g} in",
                "springline h": f"{si(kiln.chamber.height, 'in'):g} in",
            },
            reference=BOWEN,
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
    end = _end_wall(kiln, a)
    x_r, e, x_3 = (end.env[n] / 0.0254 for n in ("x_R", "e", "x_3"))
    working.append(
        Step(
            name="The arch along the depth: Heyman's statics",
            value=(
                f"a {t:g} in ring over {a.span:g} in, {k:.1f} times the thinnest that stands "
                f"(half-angle {phi:.1f}°); on each end wall the cold thrust carries the resultant "
                f"{x_r:.1f} in into its {e:g} in base (middle third to {x_3:.1f} in)"
            ),
            formula=(
                "k = T/(r + T/2) ÷ η(φ) ≥ 2; x_R = (N·x_p + G·e/2 + H_c·y_p)/(N + G) ≤ e, "
                "N = W/2, G the wall under the springline"
            ),
            reference=f"{ring.reference}; {end.reference}",
            note=(
                "Geometry and loads alone, so no range of T/S limits it. The end wall is taken "
                "standing on its own, the fill over the skewback left out: the steadier case is "
                "spare. The hot thrust, the arch pressed between braced walls, is the frame's."
            ),
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
    check = end.check()
    holds = check.status == "pass"
    findings.append(
        Finding(
            level="info",
            message=(
                "Each end wall, standing on its own, "
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
        )
    )
    return working, findings


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


def _end_wall(kiln: Kiln, a: ArchInputs) -> Sheet:
    """The end wall's sheet: the thinner of the front and back walls, its numbers checked against
    the engine's own arch (shape.Arch)."""
    ends: tuple[Face, Face] = ("front", "back")
    walls = [_layers(kiln, f) for f in ends]
    thinner = min(walls, key=lambda w: sum(x.thickness for x in w))
    sheet = vault_end_wall(a, thinner, si(kiln.chamber.height, "in"))
    arch = Arch(a.span, a.rise)
    sheet.agrees("r", Q_(arch.radius, "in"))
    return sheet


__all__ = ["along_inputs", "along_statics", "stations", "through_springing", "vault_on_door"]
