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

import itertools
import math
from dataclasses import dataclass, replace

import numpy as np

from kilndesigner.firebox_parts import (
    EPS,
    Opening,
    _plain,  # pyright: ignore[reportPrivateUsage]
    carve,
    site,
)
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


def _alongs(kiln: Kiln) -> list[tuple[float, float]]:
    """Each door's edges along its wall, in the kiln's own x (front, back) or y (sides), mm: one,
    or one per chamber of a row (``each_chamber``), ``across`` from each chamber's middle."""
    door = kiln.loading.opening
    assert door is not None
    face = kiln.loading.face
    across = si(door.across, "mm")
    u = across if face in ("front", "right") else -across  # to the right, seen from outside
    half = si(door.width, "mm") / 2
    if door.each_chamber:
        from kilndesigner.run_parts import run_layout

        run = run_layout(kiln)
        middles = [(run.front(k) + run.back(k)) / 2 for k in range(run.chambers)]
        return [(m + u - half, m + u + half) for m in middles]
    if face in ("left", "right"):
        u += site(kiln).middle
    return [(u - half, u + half)]


def door_across(kiln: Kiln) -> float:
    """The (first) door's centre along its wall (in), as a port's ``across`` measures it: from
    the wall's middle, or along a row's side wall from the first chamber's middle."""
    door = kiln.loading.opening
    assert door is not None
    face = kiln.loading.face
    if face in ("front", "back"):
        return si(door.across, "in")
    u0, u1 = _alongs(kiln)[0]
    return (1.0 if face == "right" else -1.0) * (u0 + u1) / 2 / IN


def door_holes(kiln: Kiln) -> list[DoorHole]:
    """The doors' openings through their wall: none when the whole wall is the door."""
    if kiln.loading.opening is None:
        return []
    return [_hole(kiln, u0, u1) for u0, u1 in _alongs(kiln)]


def door_hole(kiln: Kiln) -> DoorHole | None:
    """The (first) door's opening through its wall, or None when the whole wall is the door."""
    holes = door_holes(kiln)
    return holes[0] if holes else None


def _hole(kiln: Kiln, u0: float, u1: float) -> DoorHole:
    from kilndesigner.firebox_parts import (
        _inside_face,  # pyright: ignore[reportPrivateUsage]
        _outside,  # pyright: ignore[reportPrivateUsage]
    )

    door = kiln.loading.opening
    assert door is not None
    face = kiln.loading.face
    s = site(kiln)
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
    if kiln.chamber.outline is not None:
        inner = sign * _curve_inside(kiln, face, rel)
    a = (min(outer, inner) - EPS, max(outer, inner) + EPS)
    if face in ("front", "back"):
        return DoorHole(face, (u0, a[0], zs[0]), (u1, a[1], zs[1]), radius)
    return DoorHole(face, (a[0], u0, zs[0]), (a[1], u1, zs[1]), radius)


def _curve_inside(kiln: Kiln, face: WallFace, rel: tuple[float, float]) -> float:
    """A curved plan's inside face behind a door from rel[0] to rel[1] along its wall (mm, from
    the middle): where the curve comes nearest the middle across the door, so the hole reaches
    the inside everywhere, as a round wall's does."""
    from kilndesigner.form import plan_of

    plan = plan_of(kiln, "mm")
    angle = {"front": -math.pi / 2, "back": math.pi / 2, "left": math.pi, "right": 0.0}[face]
    side = face in ("left", "right")
    reaches: list[float] = []
    for k in range(17):
        u = rel[0] + (rel[1] - rel[0]) * k / 16
        try:
            reaches.append(plan.reach(angle, (0.0, u) if side else (u, 0.0)))
        except ValueError:
            reaches.append(0.0)
    return min(reaches)


def cut_door(kiln: Kiln, parts: list[Part]) -> list[Part]:
    """The door's wall with the opening cut from its plain boxes, and the door laid in the hole in
    the wall's own layers, named ``door/…``. Curved walls (a round wall, a catenary's end) keep
    their volume and are cut in the model only, as the fireboxes' holes are; their door isn't a
    separate part."""
    holes = door_holes(kiln)
    if not holes:
        return parts
    plugs: list[Part] = []
    for k, hole in enumerate(holes):
        out: list[Part] = []
        for p in parts:
            if p.wall != hole.face or not _plain(p):
                out.append(p)
                continue
            lo = tuple(max(a, b) for a, b in zip(p.lo, hole.lo, strict=True))
            hi = tuple(min(a, b) for a, b in zip(p.hi, hole.hi, strict=True))
            if all(b - a > 1e-6 for a, b in zip(lo, hi, strict=True)):
                rest = p.name.split("/", 1)[1]
                # One door keeps its plain name; a door per chamber is numbered by chamber
                name = f"door/{rest}" if len(holes) == 1 else f"door/{k + 1}/{rest}"
                plugs.append(replace(p, name=name, lo=(lo[0], lo[1], lo[2]),
                                     hi=(hi[0], hi[1], hi[2])))  # fmt: skip
            out += carve([p], [hole.opening])
        parts = out
    return parts + plugs


def model_door_holes(kiln: Kiln) -> list[tuple[tuple[float, ...], tuple[float, ...], object]]:
    """The door's opening as solids, to cut the model's walls: the box to the jambs' top, and an
    arched head's half-round over it."""
    from kilndesigner.geometry import _box, _cylinder  # pyright: ignore[reportPrivateUsage]

    out: list[tuple[tuple[float, ...], tuple[float, ...], object]] = []
    for hole in door_holes(kiln):
        out.append((hole.lo, hole.hi, _box(hole.lo, hole.hi)))
        if hole.radius <= 0:
            continue
        axis = 1 if hole.face in ("front", "back") else 0
        centre = tuple((a + b) / 2 for a, b in zip(hole.lo, hole.hi, strict=True))
        centre = (centre[0], centre[1], hole.hi[2])
        length = hole.hi[axis] - hole.lo[axis]
        lo = tuple(c - hole.radius if i != axis else hole.lo[i] for i, c in enumerate(centre))
        hi = tuple(c + hole.radius if i != axis else hole.hi[i] for i, c in enumerate(centre))
        out.append((lo, hi, _cylinder(axis, centre, hole.radius, length)))  # type: ignore[arg-type]
    return out


# ---- What spans the door -----------------------------------------------------------------------


def _wall_above(kiln: Kiln, *, crown: bool = False) -> float:
    """How much wall stands over the (first) door, at its highest, or with ``crown`` over its
    middle (in): the wall's inside top over the opening less the door's top."""
    door = kiln.loading.opening
    assert door is not None
    face = kiln.loading.face
    u0, u1 = _alongs(kiln)[0]
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
    if crown:
        samples = [(u0 + u1) / 2]
    elif u0 < 0 < u1:
        samples.append(0.0)
    top = max(inside_top(kiln, face, u) for u in samples) / IN
    return max(top - si(door.sill, "in") - si(door.height, "in"), 0.0)


def _roof_edge(kiln: Kiln) -> tuple[float, str]:
    """The roof's vertical load on the wall over the door (lb/ft) and where it comes from."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.vault import TAMBA, through_springing, vault_on_door

    if through_springing(kiln):
        down, _ = vault_on_door(kiln)
        return down, (
            "half the tube vault's weight per foot, all its layers: with the wall under it cut "
            f"away, its foot over the door stands on the door's ring (statics; {TAMBA})"
        )
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
    if door.each_chamber:
        out.working.append(
            Step(
                name="A door in each chamber",
                value=f"{len(_alongs(kiln))} doors, one into each chamber, alike",
                reference="Olsen Figs 4-36, 4-45; door-openings.md",
                note="The chambers are alike, so the first door's head stands for them all.",
            )
        )
    if door.head == "arch":
        _arch_head(kiln, w, out)
        return out
    _lintel(kiln, w, above, out)
    return out


# ---- An arched head and its jambs --------------------------------------------------------------

RING_SOURCE = (
    "the roof's ring: Olsen lays the door's ring arch 'in exactly the same way as' the chamber's, "
    "and Rhodes 'in the same way as the main arch is built' (door-headers.md §D4)"
)


def door_thrusts(r: float, outer: float, top: float, q: float, edge: float) -> tuple[float, float]:
    """The least and most thrust (lbf) of a semicircular ring, inside radius ``r`` and outside
    ``outer`` (in), under its own weight and the wall over it to ``top`` above the springline,
    ``q`` lbf per square inch of the wall's face, and ``edge`` lbf per inch along the wall's top.

    Heyman's limits (arch-thrust-theory.md §2): the least is a line of thrust from the crown's
    extrados that touches the intrados at the worst radial joint; the most, one from the crown's
    intrados that touches the extrados. Half the arch is cut into a grid; at each radial joint
    the load on it is the ring nearer the crown and the wall standing on that stretch of the
    ring, cut by a plumb line from the joint's extrados (a wall's head joints are upright).
    H = the loads' moment about the joint's touching point over the height from it to the
    crown's line."""
    step = outer / 240
    xs = np.arange(step / 2, outer, step)
    ys = np.arange(step / 2, top, step)
    x, y = (a.ravel() for a in np.meshgrid(xs, ys))
    keep = x * x + y * y >= r * r  # the ring and the wall over it, not the opening
    x, y = x[keep], y[keep]
    w = np.full(x.shape, q * step * step)
    x = np.concatenate([x, xs])  # the roof's load along the wall's top
    y = np.concatenate([y, np.full(xs.shape, top)])
    w = np.concatenate([w, np.full(xs.shape, edge * step)])
    angle = np.arctan2(x, y)
    ring = x * x + y * y <= outer * outer
    least, most = 0.0, math.inf
    for theta in np.radians(np.arange(0.5, 90.01, 0.5)):
        near = np.where(ring, angle < theta, x < outer * math.sin(theta))
        load, moment = w[near].sum(), (w[near] * x[near]).sum()
        s, c = math.sin(theta), math.cos(theta)
        least = max(least, (load * r * s - moment) / (outer - r * c))
        if outer * c < r:
            most = min(most, (load * outer * s - moment) / (r - outer * c))
    return least, most


OWN_RING_SOURCE = (
    "the design's door ring: under a cast dome Olsen lays the door's brick ring arch first and "
    "casts the shell over it (Kanayama Figs 7-17, 7-25; Höhr-Grenzhausen Figs 4-135, 4-137), "
    "and lays 'another ring arch, resting on top of the door arch' (door-headers.md [H11])"
)


def _ring_depth(kiln: Kiln) -> float | None:
    """The door arch's ring depth (in): the design's own, else the roof's ring when the roof is
    an arch or dome."""
    door = kiln.loading.opening
    if door is not None and door.ring is not None:
        return si(door.ring, "in")
    ring = getattr(kiln.roof, "ring", None)
    if ring is None or kiln.roof.type not in ("sprung_arch", "catenary_arch", "dome"):
        return None
    return sum(si(x.thickness, "in") for x in kiln.lining.for_face("roof")[:ring])


def _jamb(kiln: Kiln) -> tuple[float, str, WallFace | None]:
    """The narrowest jamb (in): from a door's edge along the wall's outside to the next door or
    the wall's outside end; and the cross wall bonded into its far end when that end is the
    wall's corner (None between two doors)."""
    s = site(kiln)
    face = kiln.loading.face
    sides: tuple[WallFace, WallFace]
    if face in ("front", "back"):
        sides = ("left", "right")
        ends = (-s.width / 2 - s.reach["left"], s.width / 2 + s.reach["right"])
    else:
        sides = ("front", "back")
        ends = (s.front - s.reach["front"], s.back + s.reach["back"])
    doors = sorted(_alongs(kiln))
    gaps = [doors[0][0] - ends[0], ends[1] - doors[-1][1]]
    gaps += [b[0] - a[1] for a, b in itertools.pairwise(doors)]
    narrow = min(range(len(gaps)), key=gaps.__getitem__)
    corner = sides[narrow] if narrow < 2 else None
    return (
        gaps[narrow] / IN,
        f"{DESIGN_WORD}: from the door's edge along the wall's outside to "
        + ("the next door or " if len(doors) > 1 else "")
        + "the wall's outside end, the narrower side",
        corner,
    )


DESIGN_WORD = "the design"


def _arch_head(kiln: Kiln, w: float, out: DoorHead) -> None:
    from kilndesigner.castable import resolve_material
    from kilndesigner.frame import FRICTION, steel_data
    from kilndesigner.frame_checks import (
        DoorArchInputs,
        Layer,
        door_arch_ring,
        door_jamb,
        door_slide,
    )

    door = kiln.loading.opening
    assert door is not None
    face = kiln.loading.face
    figures = (
        "as Olsen's built kilns' are: brick jambs and a semicircular ring arch laid on a form "
        "(Tamba Figs 4-11, 4-15; Kanayama Figs 7-17, 7-18; Kecskemét, Fig 5-42)"
    )
    ring = _ring_depth(kiln)
    if ring is None or kiln.chamber.shape == "round":
        why = (
            "the round wall's ring and its band take the thrust, not a jamb"
            if kiln.chamber.shape == "round"
            else "the roof has no ring to lay the door's arch like, and no source gives a door "
            "arch's ring depth"
        )
        out.findings.append(
            Finding(
                level="info",
                message=f"The door is arched, {figures}. Its arch and jambs aren't checked: {why}.",
                reference=f"{DOOR_SOURCE}; door-headers.md §D4, §D8",
            )
        )
        return
    layers = tuple(
        Layer(m.name, si(parse_quantity(m.density), "lb/ft**3"), si(x.thickness, "in"))
        for x in kiln.lining.for_face(face)
        for m in [resolve_material(kiln, x.material)]
    )
    edge, edge_source = _roof_edge(kiln)
    r = w / 2
    springing = si(door.sill, "in") + si(door.height, "in") - r
    above = _wall_above(kiln, crown=True) + r
    if isinstance(kiln.roof, Dome):
        # A dome stands on the door's wall: its shell is cast over the door's arch, laid first
        # (Olsen Figs 4-135, 4-137, Höhr-Grenzhausen), so the masonry over the ring runs on into
        # the shell; its weight is counted twice, as wall here and as the roof's edge, the safe
        # side for the ring's thrust
        shell = sum(si(x.thickness, "in") for x in kiln.lining.for_face("roof")[: kiln.roof.ring])
        above += shell
        out.working.append(
            Step(
                name="The dome over the door's arch",
                value=f"the wall over the door taken {shell:g} in higher, the dome's shell",
                reference=(
                    "Olsen Figs 4-135, 4-137 (p.123): the entry door's arch is laid, then the "
                    "dome cast over it; door-openings.md"
                ),
                note=(
                    "The shell's weight is counted as wall over the ring and again as the "
                    "roof's edge on it: the safe side for the ring's thrust."
                ),
            )
        )
    from kilndesigner.vault import TAMBA, through_springing, vault_on_door

    if through_springing(kiln):
        # The vault's own brickwork is turned as an arch over the door (Fig 4-11): the ring over
        # the door's crown is the vault's, and the vault's foot stands on it (the roof's edge)
        above = max(above, r) + ring
        down, out_thrust = vault_on_door(kiln)
        out.working.append(
            Step(
                name="The door through the vault's springing",
                value=(
                    f"its ring the vault's own, {ring:g} in over the door's crown; the vault puts "
                    f"{down:.0f} lb/ft down on it and pushes {out_thrust:.0f} lb/ft out, "
                    f"{out_thrust * w / 12:.0f} lb over the door's {w:g} in"
                ),
                formula="V = W/2, H = W·(sin θ − (1 − cos θ)/θ)/(2(1 − cos θ)), per foot of tube",
                reference=f"{TAMBA}; {ARCH_REFERENCE}",
                note=(
                    "With the wall under it cut away, the vault's foot over the door has nothing "
                    "to push against: its outward thrust goes along the tube into the brickwork "
                    "beside the door and the supporting wall in front of it (Fig 4-15), which the "
                    "design buttresses (roof.buttressed); that buttress isn't sized. The door's "
                    "ring is checked under the vault's weight as the roof's edge on it."
                ),
            )
        )
    jamb, jamb_source, corner = _jamb(kiln)
    q = sum(x.density * x.thickness for x in layers) / 1728  # lb per square inch of face
    cross = cross_q = 0.0
    if corner is not None:
        for x in kiln.lining.for_face(corner):
            m = resolve_material(kiln, x.material)
            t = si(x.thickness, "in")
            cross += t
            cross_q += si(parse_quantity(m.density), "lb/ft**3") * t / 1728
    least, most = door_thrusts(r, r + ring, max(above, r + ring), q, edge / 12)
    ring_source = RING_SOURCE if door.ring is None else OWN_RING_SOURCE
    da = DoorArchInputs(w, ring, layers, above, edge, edge_source, ring_source, springing, jamb,
                        jamb_source, least, most, cross, cross_q)  # fmt: skip
    minimum = steel_data()["arch_minimum_thickness"]
    eta = float(np.interp(90.0, minimum["half_angle_deg"], minimum["eta"]))
    standing = door_arch_ring(da, eta, minimum["safety"], minimum["source"])
    k = ring / (r + ring / 2) / eta
    standing.agrees("k", k)
    holding = door_jamb(da)
    sliding = door_slide(da, FRICTION, SLIDE_SOURCE)
    x_r, x_3 = (holding.env[n] / 0.0254 for n in ("x_R", "x_3"))
    mu_need = sliding.env["μ_need"]
    out.working.append(
        Step(
            name="The door's arch and jambs",
            value=(
                f"a {ring:g} in ring over {w:g} in, {k:.1f} times the thinnest that stands; "
                f"its thrust {least:.0f} lb at least, {most:.0f} lb at most; on the {jamb:.1f} in "
                f"jamb the resultant {x_r:.1f} in in from the door's edge (its middle third to "
                f"{x_3:.1f} in); at the springing it needs friction {mu_need:.2f} of "
                f"{FRICTION:g}"
            ),
            formula=(
                "k = d/(r + d/2) ÷ η(90°) ≥ 2; H_min ≤ H_max, each the loads' moment about the "
                "touching point over its height to the crown's line; "
                "x_R = (N·x_p + G₁·e/2 + G₂·(d + e)/2 + G₃·(e − b_c/2) + H_min·h_s)/ΣV ≤ e; "
                "H_min/N ≤ μ"
            ),
            inputs={
                "ring depth": f"{ring:g} in",
                "wall over the springline": f"{above:.1f} in",
                "roof's edge": f"{edge:.0f} lb/ft",
                "springline": f"{springing:g} in",
            },
            reference=f"{holding.reference}; {minimum['source']}",
            note=(
                "HarbisonWalker's arch method covers roof arches of T/S 4–10 %, and this door "
                f"arch's ring is {ring / w:.0%} of its span: so the statics here are Heyman's, "
                "from the geometry and the loads alone, which need no range. A jamb that gives "
                "a little lets the arch settle to its least thrust, so that is what it must hold "
                "(Heyman). A hot arch held rigidly would push towards the most; a door arch's hot "
                "thrust is not sourced (door-headers.md §D8). The whole wall over the arch is "
                "taken to bear on it, BIA's safe side. Sliding uses BIA's friction between brick "
                f"masonry units, {FRICTION:g}: for clay brick, none is sourced for insulating "
                "firebrick or refractory joints (refractory-bearing.md §B4.1). "
                + (
                    f"The {corner} wall bonded into the jamb's end is counted for a length of the "
                    "jamb wall's thickness only (a design rule, door-headers.md §D9). "
                    if corner
                    else "The jamb ends at another door: no cross wall is counted. "
                )
                + "A partition wall bonded in between doors isn't counted."
            ),
        )
    )
    failed = False
    for sheet in (standing, holding, sliding):
        if (check := sheet.check()).status != "pass":
            failed = True
            out.findings.append(
                Finding.failed(
                    check,
                    message=(
                        f"The door's {ring:g} in ring, {r + ring:g} in to its outside, doesn't "
                        f"fit under the wall's top, {above:.1f} in over the springline: lower "
                        "the door or narrow it."
                        if sheet is standing and above < r + ring
                        else f"The door's {ring:g} in ring is {k:.1f} times the thinnest "
                        f"semicircle that stands (Heyman's {minimum['safety']}), and under the "
                        f"wall over it its least thrust is {least:.0f} lb, its most {most:.0f} "
                        + (
                            "lb: thicken the roof's ring or narrow the door."
                            if door.ring is None
                            else "lb: deepen the door's ring or narrow the door."
                        )
                        if sheet is standing
                        else f"The door arch's least thrust, {least:.0f} lb, over its "
                        f"{sliding.env['N'] / 4.4482216:.0f} lb load at the springing needs "
                        f"friction {mu_need:.2f}, more than the {FRICTION:g} BIA gives for brick: "
                        "it could slide there. Load the arch more or narrow the door."
                        if sheet is sliding
                        else f"The door arch's thrust carries the resultant {x_r:.1f} in into "
                        f"the {jamb:.1f} in jamb, "
                        + (
                            "outside it"
                            if x_r > jamb
                            else "past its edge at the door: the ring overhangs the jamb"
                            if x_r < 0
                            else f"past its middle third, {x_3:.1f} in"
                        )
                        + ". Widen the jamb or narrow the door."
                    ),
                )
            )
    out.findings.append(
        Finding(
            level="info",
            message=(
                f"The door is arched, {figures}."
                + (
                    ""
                    if failed
                    else f" Its {ring:g} in ring is {k:.1f} times the thinnest that holds a line "
                    f"of thrust, and the {jamb:.1f} in jamb holds its least thrust, "
                    f"{least:.0f} lb, its resultant {x_r:.1f} in in from the door (Heyman's "
                    "statics)."
                )
            ),
            reference=f"{DOOR_SOURCE}; {ARCH_REFERENCE}",
        )
    )
    env = holding.env
    b, n, total = env["b"], env["N"], env["ΣV"]
    seat = min(env["x_p"], env["d"] - env["x_p"])
    toe = min(env["x_R"], env["e"] - env["x_R"])
    psi = 6894.757
    springing_psi = 2 * n / (3 * b * seat) / psi if seat > 0 else math.inf
    toe_psi = 2 * total / (3 * b * toe) / psi if toe > 0 else math.inf
    out.working.append(
        Step(
            name="Bearing stress under the door's arch",
            value=f"{springing_psi:.1f} psi at the springing, {toe_psi:.1f} psi at the jamb's toe",
            formula="σ = 2N/(3·b·a), a the resultant's distance to the nearer edge",
            reference=BEARING_SOURCE,
            note=BEARING_NOTE,
        )
    )


ARCH_REFERENCE = "arch-thrust-theory.md; domes-over-doors.md §D3; door-headers.md §D3, §D9"
SLIDE_SOURCE = (
    "BIA TN 31A: 'the coefficient of friction between the units composing a brick or tile masonry "
    "arch is at least 0.60', stable against sliding if the resultant's angle to the joint's normal "
    "is under the angle of friction (door-headers.md §D3.3; refractory-bearing.md §B4.1)"
)
BEARING_SOURCE = "refractory-bearing.md"
BEARING_NOTE = (
    "Reported, not checked: no maker, standard or handbook found gives an allowable bearing "
    "stress or a factor of safety for refractory brick or castable, cold or hot (one search "
    "extract, unread, gives a factor of 2 on the crushing strength at temperature for refractory-"
    "lined vessels: refractory-bearing.md §B4); ASTM C133 says "
    "cold crushing strength is not a measure of performance hot, and the ASTM C16 load (25 psi) "
    "is a test condition, not a limit (refractory-bearing.md). Compare it with the brick's cold "
    "crushing strength and hot-load data there."
)


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
                f"{reaction:,.0f} lb on the brick, "
                f"{reaction / (BEARING_IN * chosen.leg):.0f} psi over {BEARING_IN:g} in by its "
                f"{chosen.leg:g} in leg; that bearing isn't checked, as no allowable stress "
                "for refractory brick is published (refractory-bearing.md)."
                + (f" The wall is {walls:g} in thick: BIA puts an angle under each wythe of a "
                   "solid wall, so more than one is likely; how many isn't sized here."
                   if walls > chosen.leg else "")
            ),
            reference=f"{sheet.reference}; door-openings.md",
            check=check,
        )
    )  # fmt: skip


__all__ = ["DoorHead", "DoorHole", "cut_door", "door_head", "door_hole", "model_door_holes"]
