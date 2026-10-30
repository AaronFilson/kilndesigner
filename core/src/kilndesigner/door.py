"""A door in part of a wall (model.DoorOpening): the hole it cuts, the door laid in it, and what
spans it.

Olsen's kilns span such a door with a semicircular brick arch on brick jambs (Figs 4-11, 4-15,
5-42, 7-18) or frame a rectangular opening in angle iron (Fig 6-69); door-openings.md. A steel
lintel is sized by steel-design.md §S5: it carries everything over the opening with no arching
(BIA TN 31B) and the roof's edge on it, checked hot by AISC 360-16 F10 as the dome's buttress
angle is. Its ends' bearing on refractory brick has no sourced allowable stress, so it is reported
and left unchecked. A door arch isn't sized: HarbisonWalker's arch method, which the engine's arch
checks use, covers roof arches with T/S 4–10 %, and a door arch's hot thrust isn't found
(door-headers.md §D3.7, §D8).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace

from kilndesigner.firebox_parts import EPS, Opening, carve, site
from kilndesigner.geometry import Part, inside_top
from kilndesigner.model import Dome, Kiln, WallFace
from kilndesigner.units import Q_, parse_quantity, si
from kilndesigner.working import Finding, Step

IN = 25.4
DOOR_SOURCE = "door-openings.md (Olsen, The Kiln Book, 4th ed., Figs 4-11, 4-15, 5-42, 6-69, 7-18)"
BEARING_IN = 4.0  # TMS 402-16 §5.2.1.3: at least 4 in in the direction of the span (§D1.5)
LONGEST_IN = 96.0  # BIA: codes permit steel angle lintels for openings up to 8 ft (§D1.5)
LONGEST_SOURCE = "BIA TN 31B: steel angle lintels for openings up to 8 ft; door-headers.md §D1.5"
BIA_LEG_IN = 3.5  # BIA: a horizontal leg of at least 3½ in, ¼ in thick, for 4 in brick (§D1.5)
BIA_T_IN = 0.25


@dataclass(frozen=True)
class DoorHole:
    """Where the door's opening is, laid out level (mm): the box from the sill to the jambs' top
    (an arched head's springing), and the arch's radius over it (0 for a lintel)."""

    face: WallFace
    lo: tuple[float, float, float]
    hi: tuple[float, float, float]
    radius: float

    @property
    def opening(self) -> Opening:
        return Opening(f"door/{self.face}", self.lo, self.hi)


def _along(kiln: Kiln) -> tuple[float, float]:
    """The door's edges along its wall, in the kiln's own x (front, back) or y (sides), mm."""
    door = kiln.loading.opening
    assert door is not None
    face = kiln.loading.face
    across = si(door.across, "mm")
    u = across if face in ("front", "right") else -across  # to the right, seen from outside
    if face in ("left", "right"):
        u += site(kiln).middle
    half = si(door.width, "mm") / 2
    return u - half, u + half


def door_hole(kiln: Kiln) -> DoorHole | None:
    """The door's opening through its wall, or None when the whole wall is the door."""
    from kilndesigner.firebox_parts import (
        _inside_face,  # pyright: ignore[reportPrivateUsage]
        _outside,  # pyright: ignore[reportPrivateUsage]
    )

    door = kiln.loading.opening
    if door is None:
        return None
    face = kiln.loading.face
    s = site(kiln)
    u0, u1 = _along(kiln)
    w, h = si(door.width, "mm"), si(door.height, "mm")
    radius = w / 2 if door.head == "arch" else 0.0
    if face == "front":
        z = s.floors[0]
    elif face == "back":
        z = s.floors[-1]
    else:
        z = s.floor_at((u0 + u1) / 2)
    zs = (z + si(door.sill, "mm"), z + si(door.sill, "mm") + h - radius)
    rel = (u0, u1) if face in ("front", "back") else (u0 - s.middle, u1 - s.middle)
    side = {"front": "+y", "back": "-y", "left": "+x", "right": "-x"}[face]
    sign = -1.0 if face in ("front", "left") else 1.0
    outer = sign * _outside(s, face, *rel)
    inner = _inside_face(s, side, sign, rel)
    a = (min(outer, inner) - EPS, max(outer, inner) + EPS)
    if face in ("front", "back"):
        return DoorHole(face, (u0, a[0], zs[0]), (u1, a[1], zs[1]), radius)
    return DoorHole(face, (a[0], u0, zs[0]), (a[1], u1, zs[1]), radius)


def cut_door(kiln: Kiln, parts: list[Part]) -> list[Part]:
    """The door's wall with the opening cut from its plain boxes, and the door laid in the hole in
    the wall's own layers, named ``door/…``. Curved walls (a round wall, a catenary's end) keep
    their volume and are cut in the model only, as the fireboxes' holes are; their door isn't a
    separate part."""
    hole = door_hole(kiln)
    if hole is None:
        return parts
    plugs: list[Part] = []
    out: list[Part] = []
    for p in parts:
        plain = p.arch is None and p.profile is None and p.dome is None and p.revolve is None
        if p.wall != hole.face or not plain:
            out.append(p)
            continue
        lo = tuple(max(a, b) for a, b in zip(p.lo, hole.lo, strict=True))
        hi = tuple(min(a, b) for a, b in zip(p.hi, hole.hi, strict=True))
        if all(b - a > 1e-6 for a, b in zip(lo, hi, strict=True)):
            rest = p.name.split("/", 1)[1]
            plugs.append(replace(p, name=f"door/{rest}", lo=(lo[0], lo[1], lo[2]),
                                 hi=(hi[0], hi[1], hi[2])))  # fmt: skip
        out += carve([p], [hole.opening])
    return out + plugs


def model_door_holes(kiln: Kiln) -> list[tuple[tuple[float, ...], tuple[float, ...], object]]:
    """The door's opening as solids, to cut the model's walls: the box to the jambs' top, and an
    arched head's half-round over it."""
    from kilndesigner.geometry import _box, _cylinder  # pyright: ignore[reportPrivateUsage]

    hole = door_hole(kiln)
    if hole is None:
        return []
    out: list[tuple[tuple[float, ...], tuple[float, ...], object]] = [
        (hole.lo, hole.hi, _box(hole.lo, hole.hi))
    ]
    if hole.radius > 0:
        axis = 1 if hole.face in ("front", "back") else 0
        centre = tuple((a + b) / 2 for a, b in zip(hole.lo, hole.hi, strict=True))
        centre = (centre[0], centre[1], hole.hi[2])
        length = hole.hi[axis] - hole.lo[axis]
        lo = tuple(c - hole.radius if i != axis else hole.lo[i] for i, c in enumerate(centre))
        hi = tuple(c + hole.radius if i != axis else hole.hi[i] for i, c in enumerate(centre))
        out.append((lo, hi, _cylinder(axis, centre, hole.radius, length)))  # type: ignore[arg-type]
    return out


# ---- What spans the door -----------------------------------------------------------------------


def _wall_above(kiln: Kiln) -> float:
    """How much wall stands over the door, at its highest (in): the wall's inside top over the
    opening less the door's top."""
    door = kiln.loading.opening
    assert door is not None
    face = kiln.loading.face
    u0, u1 = _along(kiln)
    if face in ("left", "right"):
        # Along the side wall, from the middle of the chamber the door opens into
        middle = site(kiln).middle
        if kiln.chamber.chambers > 1:
            from kilndesigner.run_parts import run_layout

            run = run_layout(kiln)
            k = next(i for i in range(run.chambers) if run.front(i) <= (u0 + u1) / 2 <= run.back(i))
            middle = (run.front(k) + run.back(k)) / 2
        u0, u1 = u0 - middle, u1 - middle
    samples = [u0 + (u1 - u0) * k / 16 for k in range(17)]
    if u0 < 0 < u1:
        samples.append(0.0)
    top = max(inside_top(kiln, face, u) for u in samples) / IN
    return max(top - si(door.sill, "in") - si(door.height, "in"), 0.0)


def _roof_edge(kiln: Kiln) -> tuple[float, str]:
    """The roof's vertical load on the wall over the door (lb/ft) and where it comes from."""
    from kilndesigner.castable import resolve_material

    if isinstance(kiln.roof, Dome) and kiln.chamber.shape != "round":
        from kilndesigner.frame import dome_slices

        heaviest = max(s.weight for s in dome_slices(kiln))
        return heaviest / 2 * 12, (
            "the dome's heaviest slice, half its weight on each wall it spans (domes-over-doors.md "
            "§D4.1): the sliced dome puts nothing on the door wall, so this is the cautious case "
            "steel-design.md §S5 asks for"
        )
    if kiln.chamber.shape == "round" and kiln.roof.type != "open":
        from kilndesigner.geometry import lining_parts

        weight = sum(
            p.volume / IN**3 / 1728
            * si(parse_quantity(resolve_material(kiln, p.material).density), "lb/ft**3")
            for p in lining_parts(kiln) if p.wall == "roof"
        )  # fmt: skip
        walls = sum(si(x.thickness, "in") for x in kiln.lining.walls)
        perimeter = math.pi * (si(kiln.chamber.width, "in") + walls) / 12  # ft, mid-wall
        return weight / perimeter, (
            "the roof's weight spread evenly round the round wall's middle (statics, the roof "
            "being round; door-headers.md §D7)"
        )
    return 0.0, (
        "none: the roof spans between the walls either side of the door, or stands on its own "
        "(door-headers.md §D7)"
    )


@dataclass
class DoorHead:
    working: list[Step]
    findings: list[Finding]
    lintel: str | None = None  # the angle
    length_in: float = 0.0


def door_head(kiln: Kiln) -> DoorHead | None:
    """What spans a door in part of a wall: a steel lintel sized and checked, or an arch laid out
    but not checked. None when the whole wall is the door."""
    door = kiln.loading.opening
    if door is None:
        return None
    face = kiln.loading.face
    w, h = si(door.width, "in"), si(door.height, "in")
    above = _wall_above(kiln)
    out = DoorHead([], [])
    out.working.append(
        Step(
            name="Door in part of the wall",
            value=(
                f"{w:g} × {h:g} in in the {face} wall, {above:.1f} in of wall over it, its head "
                f"{'a semicircular arch' if door.head == 'arch' else 'a steel lintel'}"
            ),
            reference=DOOR_SOURCE,
        )
    )
    if door.head == "arch":
        out.findings.append(
            Finding(
                level="info",
                message=(
                    f"The door is arched, as Olsen's built kilns' are: brick jambs, and a "
                    f"semicircular ring arch {w:g} in across laid on a form (Tamba Figs 4-11, "
                    "4-15; Kanayama Figs 7-17, 7-18; Kecskemét's swing door, Fig 5-42). The arch "
                    "and jambs aren't checked: the engine's arch method (HarbisonWalker's) covers "
                    "roof arches of T/S 4–10 %, and no source gives a door arch's hot thrust. "
                    "Rhodes: its thrust is slight beside the main arch's and the walls' mass "
                    "buttresses it."
                ),
                reference=f"{DOOR_SOURCE}; door-headers.md §D3.7, §D4, §D8",
            )
        )
        return out
    _lintel(kiln, w, above, out)
    return out


def _lintel(kiln: Kiln, clear: float, above: float, out: DoorHead) -> None:
    from kilndesigner.castable import resolve_material
    from kilndesigner.frame import angle_allowable, angles, hot_steel, steel_data
    from kilndesigner.frame_checks import (
        AngleSection,
        Layer,
        LintelInputs,
        door_lintel,
        steel_heat,
    )

    face = kiln.loading.face
    data = steel_data()
    hs = data["hot_steel"]
    limit = float(data["binding_stress_psi"])
    hot = hot_steel(kiln, (face,))
    heat = steel_heat(hot, hs["ke_deg_f"][-1], hs["service_deg_f"], hs["service_source"])
    out.working.append(
        Step(
            name="Lintel's temperature",
            value=f"{hot.temperature:.0f} °F: Fy × {hot.ky:.2f}, E × {hot.ke:.2f}",
            formula="the door wall's outside face; AISC Table A-4.2.1 interpolated",
            reference=f"{hot.where}; {hot.source}",
            note=(
                "Taken at the wall's outside face, as the frame's steel is (steel-design.md §S3). "
                "Steel reaching into the hot inner layers would run hotter, past every limit "
                "(door-headers.md §D7, example 2); how the inner layers over the opening sit on "
                "the lintel is the builder's detail, not checked."
            ),
        )
    )
    if (check := heat.check()).status == "error":
        out.findings.append(
            Finding.failed(
                check,
                message=(
                    f"The door's lintel would run at {hot.temperature:.0f} °F, past the "
                    f"{hs['ke_deg_f'][-1]} °F where AISC's table of hot steel's stiffness ends: "
                    "nothing sourced sizes it. Arch the door instead, or insulate the wall more."
                ),
            )
        )
        return
    if check.status == "warning":
        out.findings.append(
            Finding.failed(
                check,
                message=(
                    f"The door's lintel would run at {hot.temperature:.0f} °F, above the "
                    f"{hs['service_deg_f']} °F Giles keeps carbon steel to in continuous service; "
                    "AISC's reduced strength used here is for fire, a short event."
                ),
            )
        )
    layers = tuple(
        Layer(m.name, si(parse_quantity(m.density), "lb/ft**3"), si(x.thickness, "in"))
        for x in kiln.lining.for_face(face)
        for m in [resolve_material(kiln, x.material)]
    )
    edge, edge_source = _roof_edge(kiln)
    li = LintelInputs(clear, BEARING_IN, above, layers, edge, edge_source, LONGEST_IN,
                      LONGEST_SOURCE)  # fmt: skip
    span = clear + BEARING_IN
    load = sum(x.density * x.thickness for x in layers) / 12 * above / 12 + edge  # lb/ft
    moment = load / 12 * span**2 / 8  # lb·in
    e = hot.ke * hot.e

    def deflection(ix: float) -> float:
        return 1.56 * 5 * load / 12 * span**4 / (384 * e * ix)

    allowed = min(clear / 600, 0.3)
    smallest = [a for a in angles() if a.leg >= BIA_LEG_IN and a.t >= BIA_T_IN]
    fits = [
        a for a in smallest
        if moment <= angle_allowable(a, span, hot) and moment / a.sx <= limit
        and deflection(a.ix) <= allowed
    ]  # fmt: skip
    chosen = fits[0] if fits else smallest[-1]
    section = AngleSection(chosen.name, chosen.leg, chosen.t, chosen.sx, data["angles"]["source"])
    sheet = door_lintel(li, section, chosen.ix, hot, limit, data["binding_stress_source"])
    sheet.agrees("w", Q_(load, "lbf/ft"))
    sheet.agrees("M", Q_(moment, "lbf*in"))
    sheet.agrees("M_a", Q_(angle_allowable(chosen, span, hot), "lbf*in"))
    sheet.agrees("Δ", Q_(deflection(chosen.ix), "in"))
    reaction = load * span / 12 / 2
    out.working.append(
        Step(
            name="Steel lintel over the door, hot",
            value=(
                f"{chosen.name}: w = {load:.0f} lb/ft, M = {moment:,.0f} lb·in against AISC's "
                f"{angle_allowable(chosen, span, hot):,.0f} lb·in; deflects "
                f"{deflection(chosen.ix):.3f} in against {allowed:.3f} in; each end "
                f"{reaction:,.0f} lb on the brick"
            ),
            formula=(
                "w = Σρt × the wall over the opening + the roof's edge; M = wL²/8, L the clear "
                "span + 4 in; M_a by AISC F10 hot (as the dome's buttress); Δ = 1.56·5wL⁴/384EI ≤ "
                "L/600 and 0.3 in; σ = M/S_x ≤ 12,000 psi"
            ),
            inputs={
                "the wall over it": f"{above:.1f} in",
                "roof's edge": f"{edge:.0f} lb/ft",
                "span L": f"{span:g} in",
            },
            reference=f"{sheet.reference}; {LONGEST_SOURCE}",
            note=(
                "No arching is counted (BIA, with no shoring): the steel carries everything over "
                "the opening. Unbraced, toe in compression: F10's cautious case. The bearing "
                "stress of each end on refractory brick is NOT checked: no allowable stress is "
                "found (door-openings.md). BIA's least angle, a 3½ in leg ¼ in thick, sets the "
                "smallest."
            ),
        )
    )
    if (check := sheet.check()).status != "pass" or not fits:
        out.findings.append(
            Finding.failed(
                check,
                message=(
                    f"No listed angle up to {chosen.name} carries the {load:.0f} lb/ft over the "
                    f"{clear:g} in door at {hot.temperature:.0f} °F"
                    + (f", and the door is wider than the {LONGEST_IN:g} in a steel lintel is "
                       "checked to" if clear > LONGEST_IN else "")
                    + ". Arch the door instead, as Olsen's built kilns do, or make it narrower."
                ),
            )
        )  # fmt: skip
        return
    walls = sum(x.thickness for x in layers)
    out.lintel, out.length_in = chosen.name, clear + 2 * BEARING_IN
    out.findings.append(
        Finding(
            level="info",
            message=(
                f"The door's lintel: {chosen.name}, {clear + 2 * BEARING_IN:g} in long, 4 in "
                f"bearing each end, about {hot.temperature:.0f} °F. Each end puts "
                f"{reaction:,.0f} lb on the brick; that bearing isn't checked, as no allowable "
                "stress for refractory brick is found."
                + (f" The wall is {walls:g} in thick: BIA puts an angle under each wythe of a "
                   "solid wall, so more than one is likely; how many isn't sized here."
                   if walls > chosen.leg else "")
            ),
            reference=f"{sheet.reference}; door-openings.md",
            check=check,
        )
    )  # fmt: skip


__all__ = ["DoorHead", "DoorHole", "cut_door", "door_head", "door_hole", "model_door_holes"]
