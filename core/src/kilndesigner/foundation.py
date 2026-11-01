"""The concrete platform a kiln stands on (``chamber.foundation``): the bearing under its walls,
and its top face's temperature.

Each wall's weight per foot, from the platform to its top, with the roof's share where the roof
springs from it, spread over the wall's thickness: the mean pressure under it. It is checked
against AISC 360-16 §J8's allowable bearing on concrete, 0.85 f′c over Ω_c = 2.31 on the full
area (the same as ACI 318, AISC's commentary says), with f′c reduced for the top face's heat by
EN 1992-1-2 Table 3.1 where the platform's thickness lets the heat be worked out. The top face is
checked against ACI 349's long-term limit for concrete, 150 °F (concrete-foundations.md).
"""

from __future__ import annotations

import numpy as np

from kilndesigner.model import Face, Kiln, SprungArch, arches_along
from kilndesigner.sheet import Sheet
from kilndesigner.thermal.conductivity import Conductivity
from kilndesigner.units import Q_, parse_quantity, si
from kilndesigner.working import Finding, Step

BEARING = (
    "statics: the wall's weight and the roof's share over its base; AISC 360-16 §J8 (J8-1, "
    "Ω_c = 2.31), as ACI 318; concrete-foundations.md §C3"
)
OMEGA_C = 2.31
"""AISC 360-16 §J8: the ASD safety factor for bearing on concrete."""
CONCRETE_K_SOURCE = (
    "EN 1992-1-2:2004 §3.3.3, the lower limit of normal-weight concrete's conductivity; "
    "blocked-items.md §20 [K31]"
)
_THETA_C = (20, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200)
CONCRETE_K = Conductivity(
    tuple(t + 273.15 for t in _THETA_C),
    tuple(1.36 - 0.136 * (t / 100) + 0.0057 * (t / 100) ** 2 for t in _THETA_C),
)
"""EN 1992-1-2's lower limit, sampled every 100 °C (linear between; the quadratic's chords differ
from it by under 0.002 W/(m·K))."""
STRENGTH_HOT = (1.00, 1.00, 0.95, 0.85, 0.75, 0.60, 0.45, 0.30, 0.15, 0.08, 0.04, 0.01, 0.00)
"""EN 1992-1-2 Table 3.1, f_c,θ/f_ck for siliceous aggregate, the lower of its two rows, at
_THETA_C."""
STRENGTH_HOT_SOURCE = (
    "EN 1992-1-2:2004 Table 3.1, siliceous aggregate (the lower row); blocked-items.md §20 [K31]"
)
ACI_349_F = 150.0
ACI_349_LOCAL_F = 200.0
ACI_349 = (
    "ACI 349-97 §A.4, as quoted in NRC ML15075A347: 150 °F, 200 °F in local areas, long term; "
    "blocked-items.md §20 [K32]"
)


def platform_top(kiln: Kiln) -> float | None:
    """The platform's top face at the top temperature (K), the floor's outside in the engine's
    heat-loss solve; None without the platform's thickness, or over fireboxes."""
    found = kiln.chamber.foundation
    if found is None or found.thickness is None:
        return None
    from kilndesigner.heatloss import heat_loss

    floor = next((f for f in heat_loss(kiln).faces if f.face == "floor"), None)
    return None if floor is None else floor.layers[-1].cold_side_k


def top_face_check(top_k: float, material: str) -> Sheet:
    """The platform's top face against ACI 349's long-term limit for concrete."""
    s = Sheet(
        "foundation.top-temperature",
        f"The {material} platform's top face, long term",
        reference=ACI_349,
    )
    s.given(
        "T_top", "the top face at the top temperature", Q_(top_k, "K"), "degF",
        source="the engine's heat-loss solve: the floor's outside (heatloss.py)",
    )  # fmt: skip
    s.given("T_max", "ACI 349's long-term limit, general areas", Q_(ACI_349_F, "degF"), "degF",
            source=ACI_349)  # fmt: skip
    s.require("T_top", "<=", "T_max", level="warning")
    s.lever("T_top", Q_(300, "K"), Q_(600, "K"))
    return s


def bearing_check(q: float, strength: float, k_hot: float, wall: str, sources: str) -> Sheet:
    """The mean pressure under a wall against AISC 360-16 J8-1's allowable bearing, ASD."""
    s = Sheet("foundation.bearing", f"Bearing under the {wall} wall on the platform", BEARING)
    s.given("q", "mean pressure under the wall", Q_(q, "psi"), source="statics (above)")
    s.given("f_c", "the platform's compressive strength f′c", Q_(strength, "psi"), source=sources)
    s.given("k_c", "f_c,θ/f_ck at the top face", k_hot, source=STRENGTH_HOT_SOURCE)
    s.given("Ω_c", "ASD safety factor, bearing on concrete", OMEGA_C, source="AISC 360-16 §J8")
    s.let("q_a", "allowable bearing, the full area (J8-1)", "0.85*k_c*f_c/Ω_c", "psi",
          source="AISC 360-16 §J8, as ACI 318")  # fmt: skip
    s.require("q", "<=", "q_a")
    s.lever("f_c", Q_(500, "psi"), Q_(10000, "psi"))
    return s


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


def _top_face(kiln: Kiln, material: str) -> tuple[float | None, float, list[Step], list[Finding]]:
    """The platform's top face at the top temperature, checked against ACI 349, and EN
    1992-1-2's strength ratio there; for any kiln on a platform of given thickness."""
    top = platform_top(kiln)
    k_hot = 1.0
    steps: list[Step] = []
    findings: list[Finding] = []
    if top is not None:
        k_hot = float(np.interp(top - 273.15, _THETA_C, STRENGTH_HOT))
        sheet = top_face_check(top, material)
        top_f = top * 9 / 5 - 459.67
        steps.append(
            Step(
                name=f"The {material} platform's top face",
                value=f"{top_f:.0f} °F at the top temperature; f_c,θ/f_ck {k_hot:.2f}",
                formula="the floor's outside face in the heat-loss solve, the platform under it",
                reference=f"{ACI_349}; {STRENGTH_HOT_SOURCE}",
                note=(
                    f"ACI 349 allows {ACI_349_F:g} °F long term, {ACI_349_LOCAL_F:g} °F in local "
                    "areas; EN 1992-1-2's strength table is for fires heating at 2–50 K/min, so "
                    "for a slab held hot firing after firing it is shown, not certified."
                ),
            )
        )
        check = sheet.check()
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"The platform's top face would reach {top_f:.0f} °F at the top temperature, "
                    f"above the {ACI_349_F:g} °F ACI 349 allows concrete long term "
                    f"({ACI_349_LOCAL_F:g} °F in local areas). Insulate the floor more."
                ),
            )
            if check.status != "pass"
            else Finding(
                level="info",
                message=(
                    f"The platform's top face reaches {top_f:.0f} °F at the top temperature, "
                    f"within the {ACI_349_F:g} °F ACI 349 allows concrete long term."
                ),
                reference=ACI_349,
                check=check,
            )
        )
    return top, k_hot, steps, findings


def platform_bearing(kiln: Kiln) -> tuple[list[Step], list[Finding]]:
    """The mean pressure under each wall on the platform, and its ratio to the platform's
    strength. Worked out for a box kiln under a sprung arch; refused otherwise, though the
    platform's top face is still worked out and checked where its thickness is given."""
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
        _, _, steps, findings = _top_face(kiln, found.material)
        return steps, [
            Finding(
                level="info",
                message=(
                    f"The kiln stands on {found.material} ({strength:,.0f} psi, "
                    f"{found.strength_source}); the bearing under its walls is worked out for "
                    "one box chamber under a sprung arch only, so it isn't here."
                ),
                reference=BEARING,
            ),
            *findings,
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
    top, k_hot, steps, findings = _top_face(kiln, found.material)
    allowed = 0.85 * k_hot * strength / OMEGA_C
    bearing = bearing_check(q, strength, k_hot, face, found.strength_source)
    bearing.agrees("q_a", Q_(allowed, "psi"))
    step = Step(
        name=f"Bearing under the walls on the {found.material}",
        value=(
            f"{q:.1f} psi under the {face} wall against {allowed:,.0f} psi allowed "
            f"(0.85 f′c/2.31, f′c {strength:,.0f} psi)"
        ),
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
            + (
                ""
                if top is not None
                else " The platform's top face's heat isn't worked out (its thickness isn't "
                "given, or the floor stands over fireboxes), so f′c is taken unreduced."
            )
        ),
    )
    check = bearing.check()
    findings.insert(
        0,
        Finding.failed(
            check,
            message=(
                f"The {face} wall bears {q:.1f} psi on the {found.material}, more than the "
                f"{allowed:,.0f} psi AISC 360-16 §J8 allows on {strength:,.0f} psi concrete "
                f"({found.strength_source}). Use a stronger mix or spread the wall's footing."
            ),
        )
        if check.status != "pass"
        else Finding(
            level="info",
            message=(
                f"The walls bear at most {q:.1f} psi on the {found.material} (the {face} wall), "
                f"within the {allowed:,.0f} psi AISC 360-16 §J8 allows on {strength:,.0f} psi "
                f"concrete ({found.strength_source})."
                + (
                    ""
                    if top is not None
                    else " Give the platform's thickness to have the floor's loss through it and "
                    "its top face's temperature worked out."
                )
            ),
            reference=BEARING,
            check=check,
        ),
    )
    return [*steps, step], findings


__all__ = ["platform_bearing"]
