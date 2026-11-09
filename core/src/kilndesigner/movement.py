"""How a kiln's brickwork moves as it heats: the expansion allowance to leave in each wall run and
over a sprung arch, where the joints go, and the IFB on a hot face that may shrink near its rating
(refractory-movement-and-mortar.md §1, the sixth research round).

- **Growth.** Fireclay brick grows 3/32 in per foot heated to 2400 °F, the allowance most makers
  recommend (Brosnan [M1]); Olsen gives 1/16–3/32 in per foot (p.51). No source read gives the
  curve below 2400 °F, so the growth is not scaled to a cooler firing: it is stated at 2400 °F,
  the safe side, and not worked out at all past it (ADR 0009).
- **Allowance.** Half the growth is enough; the joints take the rest (Bhatia [M2] p.29). Olsen's
  1/16 in per foot in a steel frame (p.52) is about that half.
- **Where.** In a steel frame, ¼ in fibre pads mortared to the brick ends at the corners, offset
  course to course (p.52, Fig. 2-31); in hard brick only the 9 in hot-face course (Fig. 2-30); an
  IFB wall in a flexible frame needs none up to 48 in (Fig. 2-32; the text says 5 ft, p.53). A
  free-standing chamber kiln has none: its walls act as one unit (p.52). Never in the masonry over
  an arch or near its springing (BIA TN 31, door-headers.md D3.1).

How far an arch rises as it grows in a held span is not worked out: the geometry (§1.2) is not
checked against a kiln or a published method.
"""

from __future__ import annotations

from kilndesigner.model import Kiln, SprungArch
from kilndesigner.sheet import Check, Sheet
from kilndesigner.units import Q_, si
from kilndesigner.working import Finding, Step

GROWTH_IN_PER_FT = 3 / 32
"""in per foot of run, heated to 2400 °F (Brosnan [M1]; Olsen p.51)."""
GROWTH_TO_F = 2400.0
"""°F: the temperature Brosnan's 3/32 in per foot is to."""
LEFT_OPEN = 0.5
"""Of the growth, the share to leave open: the joints take the rest (Bhatia [M2] p.29)."""
NO_JOINT_IN = 48.0
"""in: the longest IFB wall in a flexible frame that needs no joint (Olsen Fig. 2-32, p.52)."""
PAD_IN = 0.25
"""in: Olsen's fibre pad at a joint (p.52, Figs 2-31 and 2-32)."""

BROSNAN = (
    "Brosnan, 'Alumina-Silica Brick', in Schacht (ed.), Refractories Handbook: fireclay brick "
    "grows 3/32 in per ft heated to 2400 °F, the allowance most makers recommend; Olsen, The "
    "Kiln Book, 4th ed., p.51 (1/16–3/32 in per ft); refractory-movement-and-mortar.md §1.1 [M1]"
)
BHATIA = (
    "Bhatia, Overview of Refractory Materials, PDHonline M158, p.29: 'just one half of the "
    "theoretical expansion is sufficient', the joints taking the rest; Olsen p.52, 1/16 in per ft "
    "in a steel frame; refractory-movement-and-mortar.md §1.1 [M2]"
)
OLSEN_JOINTS = (
    "Olsen, The Kiln Book, 4th ed., p.52–53 (Figs 2-30, 2-31, 2-32): ¼ in fibre pads mortared to "
    "the brick ends at the corners, offset; in hard brick only the 9 in hot-face course; an IFB "
    "wall in a flexible frame needs none up to 48 in (Fig. 2-32; 5 ft by the text); free-standing "
    "chamber kilns use none; kiln-reference.md §2"
)
BIA_JOINTS = (
    "BIA Technical Note 31: 'Vertical expansion joints should not be placed in the masonry "
    "directly above a structural arch' or 'in close proximity to the springing'; door-headers.md "
    "D3.1 [H2]"
)
IFB_SHRINK = (
    "Brosnan, 'Alumina-Silica Brick': IFB 'for long-term exposures near the rated service "
    "temperature, shrinkage may occur sufficiently to allow joint opening', so use a higher duty "
    "rating than the process temperature alone needs; refractory-movement-and-mortar.md §1.1 [M1]"
)


def allowance_sheet(id: str, title: str, run_in: float, top_f: float) -> Sheet:
    """The growth of a run of brickwork ``run_in`` long, hot, and the allowance to leave open."""
    s = Sheet(id, title, reference=f"{BROSNAN}; {BHATIA}")
    s.given("L", "the run, outside", Q_(run_in, "in"), "in", source="the design's outside sizes")
    s.given("g", "growth per foot, to 2400 °F", Q_(GROWTH_IN_PER_FT, "in/ft"), "in/ft",
            source=BROSNAN)  # fmt: skip
    s.let("ΔL", "the run's growth, hot", "L*g", "in")
    s.given("f", "the share to leave open", LEFT_OPEN, source=BHATIA)
    s.let("a", "the allowance to leave open", "f*ΔL", "in")
    s.given("T", "the kiln's top temperature", Q_(top_f, "degF"), "degF",
            source="the design's firing")  # fmt: skip
    s.given("T_g", "the temperature the growth is to", Q_(GROWTH_TO_F, "degF"), "degF",
            source=BROSNAN)  # fmt: skip
    s.require("T", "<=", "T_g", level="warning")
    return s


def _runs(kiln: Kiln) -> list[tuple[str, str, float, tuple[str, ...]]]:
    """Each straight run of brick wall: its id, its name, its outside length (in), its faces."""
    from kilndesigner.frame import outside

    o = outside(kiln)
    return [
        ("across", "front and back walls", o.width, ("front", "back")),
        ("along", "side walls", o.depth, ("left", "right")),
    ]


def _bricks(kiln: Kiln, faces: tuple[str, ...]) -> tuple[bool, bool]:
    """Whether the faces have a brick layer, and whether every brick in them is IFB."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.masonry import BRICK_KINDS

    kinds = [
        resolve_material(kiln, x.material).kind
        for face in faces
        for x in kiln.lining.for_face(face, door_face=kiln.door_face)  # type: ignore[arg-type]
    ]
    bricks = [k for k in kinds if k in BRICK_KINDS]
    return bool(bricks), bool(bricks) and all(k == "insulating_firebrick" for k in bricks)


def _arched(kiln: Kiln) -> bool:
    """Whether the kiln has an arch over its walls: a sprung roof, or an arched door head."""
    opening = kiln.loading.opening
    return isinstance(kiln.roof, SprungArch) or (opening is not None and opening.head == "arch")


def expansion(kiln: Kiln, frame_kind: str) -> tuple[list[Step], list[Finding]]:
    """The expansion allowance of a box kiln's brick wall runs and its sprung arch, as working and
    info findings (refractory-movement-and-mortar.md §4.1). Round kilns and catenaries aren't
    covered: no source here places joints in a ring or along a catenary."""
    from kilndesigner.frame import NO_FRAME
    from kilndesigner.heatloss import top_temperature

    if kiln.chamber.shape != "box" or kiln.roof.type == "catenary_arch":
        return [], []
    top_f = si(top_temperature(kiln)[0], "degF")
    framed = frame_kind != NO_FRAME
    steps: list[Step] = []
    findings: list[Finding] = []
    for key, name, run, faces in _runs(kiln):
        brick, ifb = _bricks(kiln, faces)
        if not brick:
            continue
        sheet = allowance_sheet(f"movement.{key}", f"Expansion allowance, the {name}", run, top_f)
        findings.append(_run_finding(kiln, name, run, top_f, framed, ifb, sheet.check()))
        if top_f <= GROWTH_TO_F:
            grow, allow = sheet.env["ΔL"] / 0.0254, sheet.env["a"] / 0.0254
            steps.append(
                Step(
                    name=f"Expansion allowance, the {name}",
                    value=f"grows {grow:.3f} in hot; leave {allow:.3f} in open",
                    formula="ΔL = L × 3/32 in per ft (to 2400 °F); a = ½ ΔL",
                    inputs={"L, outside": f"{run:.1f} in", "top temperature": f"{top_f:.0f} °F"},
                    reference=f"{BROSNAN}; {BHATIA}",
                    note=(
                        "The growth is to 2400 °F; no source read gives it below, so it isn't "
                        "scaled down to a cooler firing (the safe side)."
                    ),
                )
            )
    if isinstance(kiln.roof, SprungArch) and top_f <= GROWTH_TO_F:
        steps.append(_arch_step(kiln))
    return steps, findings


def _arch_step(kiln: Kiln) -> Step:
    from kilndesigner.model import arches_along

    assert isinstance(kiln.roof, SprungArch)
    span = si(kiln.chamber.depth if arches_along(kiln) else kiln.chamber.width, "in")
    grow = span / 12 * GROWTH_IN_PER_FT
    return Step(
        name="Expansion allowance, the arch's span",
        value=f"grows {grow:.3f} in hot; {LEFT_OPEN * grow:.3f} in of it for the frame to give",
        formula="ΔS = S × 3/32 in per ft (to 2400 °F); a = ½ ΔS",
        inputs={"S, the span": f"{span:g} in"},
        reference=f"{BROSNAN}; {BHATIA}; {BIA_JOINTS}",
        note=(
            "No expansion joint in the masonry over the arch or near its springing (BIA). How far "
            "the arch rises as it grows in a held span isn't worked out: no published method or "
            "measurement was found (refractory-movement-and-mortar.md §1.2)."
        ),
    )


def _run_finding(
    kiln: Kiln, name: str, run: float, top_f: float, framed: bool, ifb: bool, check: Check
) -> Finding:
    if top_f > GROWTH_TO_F:
        return Finding(
            level="info",
            message=(
                f"The {name}' growth hot isn't worked out: the kiln fires to {top_f:.0f} °F, past "
                f"the {GROWTH_TO_F:.0f} °F the sourced 3/32 in per foot is to. Leave the frame "
                "room to give, as Olsen does (p.52)."
            ),
            reference=BROSNAN,
            check=check,
        )
    grow = run / 12 * GROWTH_IN_PER_FT
    allow = LEFT_OPEN * grow
    text = (
        f"The {name}, {run:.1f} in outside, grow about {grow:.2f} in hot (3/32 in per foot, to "
        f"2400 °F): leave about {allow:.2f} in of it open, half the growth, the joints taking the "
        "rest (Bhatia; Olsen's 1/16 in per foot in a frame). "
    )
    if not framed:
        text += (
            "Free-standing, as this kiln is, Olsen's chamber kilns have no expansion joints: the "
            "walls act as one unit (p.52)."
        )
    elif ifb and run <= NO_JOINT_IN:
        text += (
            f"An IFB wall up to {NO_JOINT_IN:g} in in a flexible frame, built not too tight, needs "
            "no joint (Olsen p.52–53); the frame takes it."
        )
    else:
        text += (
            "Olsen puts it at the corners as ¼ in fibre pads mortared to the brick ends, "
            "offset course to course, not straight through"
            + ("" if ifb else "; in hard brick only the 9 in hot-face course needs it")
            + (
                f"; past {NO_JOINT_IN:g} in he joints IFB walls too (p.52–53)."
                if run > NO_JOINT_IN
                else " (p.52–53)."
            )
        )
    if _arched(kiln):
        text += " No joint in the masonry over an arch or near its springing (BIA)."
    refs = [BROSNAN, BHATIA] + ([] if not framed else [OLSEN_JOINTS])
    refs += [BIA_JOINTS] if _arched(kiln) else []
    return Finding(level="info", message=text, reference="; ".join(refs), check=check)


def ifb_notes(kiln: Kiln) -> list[Step]:
    """Each IFB on a hot face, with its rating beside the kiln's top temperature: Brosnan warns it
    may shrink and open its joints in long service near its rating. No source says how near, so
    the margin is shown, not judged."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.heatloss import top_temperature

    top_f = si(top_temperature(kiln)[0], "degF")
    seen: dict[str, list[str]] = {}
    for face in ("floor", "left", "right", "front", "back", "roof"):
        layers = kiln.lining.for_face(face, door_face=kiln.door_face)  # type: ignore[arg-type]
        if not layers:
            continue
        m = resolve_material(kiln, layers[0].material)
        if m.kind == "insulating_firebrick" and m.max_service_temperature is not None:
            seen.setdefault(m.id, []).append(face)
    steps: list[Step] = []
    for mid, faces in seen.items():
        m = resolve_material(kiln, mid)
        assert m.max_service_temperature is not None
        rating = si(m.max_service_temperature, "degF")
        steps.append(
            Step(
                name=f"IFB near its rating: {m.name}",
                value=f"rated {rating:.0f} °F; the kiln fires to {top_f:.0f} °F, "
                f"{rating - top_f:.0f} °F below",
                inputs={"hot face of": ", ".join(faces)},
                reference=f"{IFB_SHRINK}; rating: {m.source}",
                note=(
                    "Long service near its rating can shrink IFB enough to open its joints; no "
                    "source says how near, so the margin is shown, not judged."
                ),
            )
        )
    return steps
