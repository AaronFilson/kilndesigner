"""The bearing under a kiln's walls on the platform they stand on (``chamber.foundation``).

Each wall's weight per foot, from the platform to its top, with the roof's share where the roof
springs from it, spread over the wall's thickness: the mean pressure under it. It is set against
the platform's compressive strength as a ratio, not passed or failed: no allowable bearing stress
for concrete under a kiln is sourced in docs/research (refractory-bearing.md §B4 finds none for
refractory either), so the ratio is shown with the strength's own source.
"""

from __future__ import annotations

from kilndesigner.model import Face, Kiln, SprungArch, arches_along
from kilndesigner.units import parse_quantity, si
from kilndesigner.working import Finding, Step

BEARING = (
    "statics: the wall's weight and the roof's share over its base; refractory-bearing.md §B4 (no "
    "allowable bearing stress sourced)"
)


def _wall(kiln: Kiln, face: Face) -> tuple[float, float]:
    """A wall's Σ density × thickness (lb/ft³ × in) and its thickness (in)."""
    from kilndesigner.castable import resolve_material

    layers = kiln.lining.for_face(face)
    rho_t = sum(
        si(parse_quantity(resolve_material(kiln, x.material).density), "lb/ft**3")
        * si(x.thickness, "in")
        for x in layers
    )
    return rho_t, sum(si(x.thickness, "in") for x in layers)


def platform_bearing(kiln: Kiln) -> tuple[list[Step], list[Finding]]:
    """The mean pressure under each wall on the platform, and its ratio to the platform's
    strength. Worked out for a box kiln under a sprung arch; refused otherwise."""
    found = kiln.chamber.foundation
    if found is None:
        return [], []
    strength = si(found.compressive_strength, "psi")
    roof = kiln.roof
    if (
        not isinstance(roof, SprungArch)
        or kiln.chamber.shape != "box"
        or roof.tube
        or (kiln.chamber.chambers > 1)
    ):
        return [], [
            Finding(
                level="info",
                message=(
                    f"The kiln stands on {found.material} ({strength:,.0f} psi, "
                    f"{found.strength_source}); the bearing under its walls is worked out for "
                    "one box chamber under a sprung arch only, so it isn't here."
                ),
                reference=BEARING,
            )
        ]
    from kilndesigner.frame import _arch_load, outside  # pyright: ignore[reportPrivateUsage]
    from kilndesigner.shape import Arch, along_arch
    from kilndesigner.vault import uneven_thrust

    o = outside(kiln)
    h = si(kiln.chamber.height, "in")
    roof_t = sum(si(x.thickness, "in") for x in kiln.lining.for_face("roof"))
    crown = h + si(roof.rise, "in") + roof_t
    if arches_along(kiln):
        arch = along_arch(kiln, "in")
        _, front, back = uneven_thrust(arch, _arch_load(kiln, arch).weight)
        tops: dict[Face, tuple[float, float]] = {
            "front": (h - arch.drop, front), "back": (h, back),
            "left": (crown, 0.0), "right": (crown, 0.0),
        }  # fmt: skip
    else:
        arch = Arch(si(kiln.chamber.width, "in"), si(roof.rise, "in"))
        half = _arch_load(kiln, arch).weight / 2
        tops = {"left": (h, half), "right": (h, half), "front": (crown, 0.0), "back": (crown, 0.0)}
    rows: dict[str, str] = {}
    worst = (0.0, "")
    for face, (top, share) in tops.items():
        rho_t, t = _wall(kiln, face)
        weight = rho_t * (o.bottom + top) / 144 + share  # lb per foot of wall
        q = weight / (12 * t)
        rows[f"{face} wall"] = f"{weight:,.0f} lb/ft over {t:g} in = {q:.1f} psi" + (
            f", the roof's {share:.0f} lb/ft in it" if share else ""
        )
        worst = max(worst, (q, face))
    q, face = worst
    step = Step(
        name=f"Bearing under the walls on the {found.material}",
        value=f"{q:.1f} psi under the {face} wall, {q / strength:.2%} of {strength:,.0f} psi",
        formula=(
            "q = (Σ ρ·t × (d_f + z_top)/144 + N)/(12·t), lb per foot over the wall's base; d_f the "
            "floor's depth, z_top the wall's top, N the roof's share where it springs"
        ),
        inputs=rows,
        reference=BEARING,
        note=(
            "Mean pressure, the wall taken down through the floor's depth to the platform, the "
            "masonry above a springline outside the ring and any lean of the resultant left out; "
            "a wall filled up to a vault is taken to the roof's crown, the most it reaches. The "
            f"strength is {found.strength_source}."
        ),
    )
    finding = Finding(
        level="info",
        message=(
            f"The walls bear at most {q:.1f} psi on the {found.material} (the {face} wall), "
            f"{q / strength:.2%} of its {strength:,.0f} psi ({found.strength_source}). Shown, not "
            "checked: no allowable bearing stress for it is sourced. Its heat loss isn't worked "
            "out either: no thermal conductivity for it is sourced, so the floor's loss is "
            "worked out as before, without the platform."
        ),
        reference=BEARING,
    )
    return [step], [finding]


__all__ = ["platform_bearing"]
