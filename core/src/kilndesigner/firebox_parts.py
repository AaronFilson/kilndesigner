"""Fireboxes laid out in brick: their walls, floors and roofs, the inlet flues into the chamber,
the stoke holes and ash-pit mouths, and the grate bars (geometry.lining_parts).

Each firebox is the design's (fire.fireboxes): its inside ``width`` across its mouth, ``length``
from its mouth back, ``height`` from the grate (or its floor) up, and ``ash_pit`` from the grate
down. Its walls, floor and roof take the kiln's own layers, as the shells do (massing.py): the
walls' layers round its sides, the floor's under it, and the walls' layers laid flat over it. No
source here gives a firebox a lining of its own, so it is built as the kiln is.

- **Against a wall** (front, back, left or right): the firebox stands outside the kiln's wall,
  its grate at the chamber floor's level, its inside running ``length`` out from the wall. The
  wall between is cut by the inlet flues (``inlet`` × ``inlets``, spread across the firebox, at
  the foot of the wall), or, with none given, by the firebox's whole mouth.
- **Under the floor**: below the chamber's floor, which roofs it, along the middle of the run.
  The inlet flues go up through the floor at its far end, ``inlet``'s width across the firebox, as
  in Olsen's fast-fire kiln: "4½ in × the firebox width at the far end of each firebox" (The Kiln
  Book, 4th ed., p.141). With none given the floor is left solid, and said so.
- **Troughs, one to a chamber**: fireboxes against the front or back that don't fit side by side,
  one to each chamber in a row, are troughs sunk in each chamber's floor along its front, as in
  the Kyoto kilns' himae, "a 9 in (23 cm) trough along the front wall" (p.92); open to the
  chamber, lined below the floor with the floor's layers. In a row, a second firebox at the front
  or back feeds the next chamber the same way, as Olsen's second-chamber firebox does, sunk under
  that chamber's inlet flue (p.206).

Fireboxes side by side are spread evenly, or, where that leaves no room for their walls, packed
so each has its own walls, touching. A firebox whose height isn't given is drawn as tall as it is
wide, as the shells draw it.

The stoke hole (``stoke_hole``) is cut in the firebox's mouth wall, its foot at the grate, where
the fuel is thrown; Olsen puts "a 9 × 13 in stoke hole in each firebox door" (p.188). The ash pit's
mouth is left fully open below the grate, "the ash-pit entrance fully open" (p.188). Grate bars
are drawn ¾ in round, the least Olsen gives, "metal rods ¾–1 in in diameter" (p.199–200), the
grate's ``gap`` apart, running from the mouth back; with no gap given they aren't drawn.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Literal

from kilndesigner.model import Firebox, Kiln
from kilndesigner.shape import chamber_shape
from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_, si
from kilndesigner.working import Finding, length_text

if TYPE_CHECKING:
    from kilndesigner.geometry import Part
    from kilndesigner.hardware import Piece

IN = 25.4
BAR = 0.75 * IN  # Olsen's least grate bar (p.199–200)
GRATE_SOURCE = "Olsen, The Kiln Book, 4th ed., p.199–200 (grate bars ¾–1 in rods)"
FIREBOX_SOURCE = "Olsen, The Kiln Book, 4th ed., p.92, p.141, p.145, p.188"
EPS = 1.0  # mm: openings reach this far past the faces they cut

type Vec = tuple[float, float, float]
type Side = Literal["-x", "+x", "-y", "+y", "up"]
SIDE_FACE = {"-x": "left", "+x": "right", "-y": "front", "+y": "back"}
OPPOSITE: dict[str, Side] = {"-x": "+x", "+x": "-x", "-y": "+y", "+y": "-y"}


@dataclass(frozen=True)
class FireboxBox:
    """One firebox's inside, laid out level (mm): the ash pit included."""

    index: int  # from 1, over all the kiln's fireboxes
    box: Firebox
    lo: Vec
    hi: Vec
    grate_z: float
    kiln_side: Side  # the side of the inside the chamber is on: where the inlet flues go
    trough: bool = False
    chamber: int | None = None
    level: float = 0.0  # the chamber floor's height beside it

    @property
    def mouth(self) -> Side:
        """The side of the inside the firebox is fed from: across from the chamber, or the front
        end under the floor."""
        return "-y" if self.kiln_side == "up" else OPPOSITE[self.kiln_side]

    @property
    def along_y(self) -> bool:
        """Whether its length runs along y."""
        return self.kiln_side in ("-y", "+y", "up")


@dataclass(frozen=True)
class Opening:
    """A hole cut through the lining: a box, round about ``axis`` when ``round``."""

    name: str
    lo: Vec
    hi: Vec
    round: bool = False
    axis: int = 1


@dataclass(frozen=True)
class GrateBars:
    name: str
    title: str
    detail: str
    bars: int
    length: float  # each, mm
    axis: int  # 0 or 1: the way they run
    centres: tuple[Vec, ...]  # mm


@dataclass(frozen=True)
class Site:
    """Where the kiln's inside and walls are, to set fireboxes against (mm)."""

    width: float
    front: float  # the first chamber's inside front face, y
    back: float  # the last chamber's inside back face, y
    reach: dict[str, float]  # each wall's thickness
    floor_t: float
    height: float
    radius: float | None  # a round kiln's inside radius
    outer: float | None  # and its outside
    chambers: int
    fronts: tuple[float, ...]  # each chamber's inside front face
    floors: tuple[float, ...]  # each chamber's floor height

    @property
    def length(self) -> float:
        return self.back - self.front

    @property
    def middle(self) -> float:
        return (self.front + self.back) / 2

    def floor_at(self, y: float) -> float:
        k = 0
        for i, f in enumerate(self.fronts):
            if y >= f - 1e-6:
                k = i
        return self.floors[k]


def site(kiln: Kiln) -> Site:
    from kilndesigner.geometry import in_a_row, thicknesses

    c = kiln.chamber
    floor_t = sum(t for _, t in thicknesses(kiln, "floor"))
    walls = sum(si(x.thickness, "mm") for x in kiln.lining.walls)
    w, h = si(c.width, "mm"), si(c.height, "mm")
    if c.shape == "round":
        r = w / 2
        faces: tuple[str, ...] = ("left", "right", "front", "back")
        return Site(
            w, -r, r, dict.fromkeys(faces, walls), floor_t, h, r, r + walls, 1, (-r,), (0.0,)
        )
    reach: dict[str, float] = {
        f: sum(t for _, t in thicknesses(kiln, f)) for f in ("left", "right", "front", "back")
    }
    if in_a_row(kiln):
        from kilndesigner.run_parts import run_layout

        run = run_layout(kiln)
        n = run.chambers
        return Site(
            w, run.front(0), run.back(n - 1), reach, floor_t, h, None, None, n,
            tuple(run.front(i) for i in range(n)), tuple(run.floor(i) for i in range(n)),
        )  # fmt: skip
    d = si(c.depth, "mm")
    return Site(w, -d / 2, d / 2, reach, floor_t, h, None, None, 1, (-d / 2,), (0.0,))


def _outside(s: Site, face: str, u0: float, u1: float) -> float:
    """How far out from the kiln's centre line the wall's outside face is, behind a firebox from
    u0 to u1 along it (mm). A round wall's is taken where it reaches furthest, at the firebox's
    nearest point to the middle; the corners are filled to the curve."""
    if s.outer is not None:
        near = 0.0 if u0 <= 0 <= u1 else min(abs(u0), abs(u1))
        return math.sqrt(max(s.outer**2 - near**2, 0.0))
    if face == "front":
        return -s.front + s.reach["front"]
    if face == "back":
        return s.back + s.reach["back"]
    return s.width / 2 + s.reach[face]


GRATE_HEIGHT_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.199–200 and Fig. 8-2 (the grate at the vertical midpoint; "
    "12–18 in below and above on 30–100 ft³ kilns), p.188 (a 9–12 in rise from the grate to the "
    "chamber floor), p.179 (a 12–15 in step up)"
)


def grate_heights(fb: Firebox) -> tuple[float, float, float]:
    """A firebox's space above the grate, its ash pit below and the step up from the grate to
    the chamber floor (mm). With a grate, an ash pit left out is as deep as the space above,
    Olsen's grate at the vertical midpoint (p.199–200). A step left out is 0: the grate level with
    the chamber floor, the firebox open to the first chamber; the report gives Olsen's 9–12 in
    (p.188) as the other choice. Without a grate the fuel burns on the floor."""
    fh = si(fb.height, "mm") if fb.height is not None else si(fb.width, "mm")
    grate = fb.grate is not None
    ash = si(fb.ash_pit, "mm") if fb.ash_pit is not None else (fh if grate else 0.0)
    step = si(fb.step, "mm") if fb.step is not None else 0.0
    return fh, ash, step


def firebox_boxes(kiln: Kiln) -> list[FireboxBox]:
    """Every firebox's inside, where it stands."""
    fire = kiln.heat.fire
    if fire is None:
        return []
    s = site(kiln)
    walls = sum(si(x.thickness, "mm") for x in kiln.lining.walls)
    out: list[FireboxBox] = []
    j = 0
    ends = 0  # fireboxes at the ends of a row so far: the later ones feed the later chambers
    for fb in fire.fireboxes:
        fw, fl = si(fb.width, "mm"), si(fb.length, "mm")
        fh, ash, step = grate_heights(fb)
        n, face = fb.count, fb.position
        first = 0
        troughs = n * fw > s.width + 1e-6 and 1 < n <= s.chambers
        if s.chambers > 1 and face in ("front", "back"):
            first, ends = ends, ends + (n if troughs else 1)
        if face in ("front", "back") and (troughs or 0 < first < s.chambers):
            half = min(fl, s.width) / 2
            for i in range(first, min(first + n, s.chambers)):
                j += 1
                y, z = s.fronts[i], s.floors[i]
                lo, hi = (-half, y, z - fh - ash), (half, y + fw, z)
                out.append(FireboxBox(j, fb, lo, hi, z - fh, "up", True, i + 1, z))
            continue
        across = s.width if face in ("front", "back", "under") else s.length
        pitch = max(across / n, fw + 2 * walls)
        for i in range(n):
            j += 1
            c = pitch * (i - (n - 1) / 2)
            u0, u1 = c - fw / 2, c + fw / 2
            if face == "under":
                long = min(fl, s.length)
                level = s.floors[0]
                top = level - s.floor_t
                lo = (u0, s.middle - long / 2, top - fh - ash)
                hi = (u1, s.middle + long / 2, top)
                out.append(FireboxBox(j, fb, lo, hi, top - fh, "up", level=level))
                continue
            if face in ("front", "back"):
                y_out = _outside(s, face, u0, u1)
                level = s.floors[0] if face == "front" else s.floors[-1]
                g = level - step
                if face == "front":
                    lo, hi = (u0, -y_out - fl, g - ash), (u1, -y_out, g + fh)
                    side: Side = "+y"
                else:
                    lo, hi = (u0, y_out, g - ash), (u1, y_out + fl, g + fh)
                    side = "-y"
            else:
                y0, y1 = s.middle + u0, s.middle + u1
                level = s.floor_at(s.middle + c)
                g = level - step
                x_out = _outside(s, face, u0, u1)
                if face == "left":
                    lo, hi = (-x_out - fl, y0, g - ash), (-x_out, y1, g + fh)
                    side = "+x"
                else:
                    lo, hi = (x_out, y0, g - ash), (x_out + fl, y1, g + fh)
                    side = "-x"
            out.append(FireboxBox(j, fb, lo, hi, g, side, level=level))
    return out


# --- Parts --------------------------------------------------------------------------------------


def _layers(kiln: Kiln) -> tuple[list[tuple[str, float]], list[tuple[str, float]]]:
    from kilndesigner.geometry import thicknesses

    walls = [(x.material, si(x.thickness, "mm")) for x in kiln.lining.walls]
    return walls, thicknesses(kiln, "floor")


def _lined(
    kiln: Kiln,
    tag: str,
    lo: Vec,
    hi: Vec,
    open_side: Side | None,
    roof: bool,
    chamber: int | None,
    floor_: bool = True,
) -> list[Part]:
    """A box's walls, floor (unless not ``floor_``) and (with ``roof``) roof round the inside
    lo–hi, the walls' layers wrapped like the kiln's own (geometry._level_parts): the walls across
    x run through, those across y fit between them. ``open_side`` is left unbuilt: the kiln's
    wall is there."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.geometry import Part

    walls, floor = _layers(kiln)
    parts: list[Part] = []
    built = {side: side != open_side for side in ("-x", "+x", "-y", "+y")}
    total = sum(t for _, t in walls)

    def out(side: str, r: float) -> float:
        return r if built[side] else 0.0

    def add(name: str, mat: str, face: str, a: Vec, b: Vec) -> None:
        if any(q - p < 1e-6 for p, q in zip(a, b, strict=True)):
            return
        kind = resolve_material(kiln, mat).kind
        parts.append(Part(f"{tag}/{name}", mat, kind, a, b, face=face, chamber=chamber))  # type: ignore[arg-type]

    (x0, y0, z0), (x1, y1, z1) = lo, hi
    r = 0.0
    for k, (mat, th) in enumerate(walls):
        rr = r + th
        if built["-x"]:
            add(f"{k + 1}-{mat}-left", mat, "left", (x0 - rr, y0 - out("-y", rr), z0),
                (x0 - r, y1 + out("+y", rr), z1))  # fmt: skip
        if built["+x"]:
            add(f"{k + 1}-{mat}-right", mat, "right", (x1 + r, y0 - out("-y", rr), z0),
                (x1 + rr, y1 + out("+y", rr), z1))  # fmt: skip
        if built["-y"]:
            add(f"{k + 1}-{mat}-front", mat, "front", (x0 - out("-x", r), y0 - rr, z0),
                (x1 + out("+x", r), y0 - r, z1))  # fmt: skip
        if built["+y"]:
            add(f"{k + 1}-{mat}-back", mat, "back", (x0 - out("-x", r), y1 + r, z0),
                (x1 + out("+x", r), y1 + rr, z1))  # fmt: skip
        r = rr
    xs = (x0 - out("-x", total), x1 + out("+x", total))
    ys = (y0 - out("-y", total), y1 + out("+y", total))
    cum = 0.0
    for k, (mat, th) in enumerate(floor if floor_ else []):
        add(f"{k + 1}-{mat}-floor", mat, "floor", (xs[0], ys[0], z0 - cum - th),
            (xs[1], ys[1], z0 - cum))  # fmt: skip
        cum += th
    if roof:
        cum = 0.0
        for k, (mat, th) in enumerate(walls):
            add(f"{k + 1}-{mat}-roof", mat, "roof", (xs[0], ys[0], z1 + cum),
                (xs[1], ys[1], z1 + cum + th))  # fmt: skip
            cum += th
    return parts


def _trough_floor(kiln: Kiln, tag: str, b: FireboxBox) -> list[Part]:
    """The floor's layers under a trough shallower than the floor, in the floor's cut."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.geometry import Part

    out: list[Part] = []
    cum = 0.0
    for k, (mat, th) in enumerate(_layers(kiln)[1]):
        z = b.lo[2] - cum
        out.append(
            Part(f"{tag}/{k + 1}-{mat}-floor", mat, resolve_material(kiln, mat).kind,
                 (b.lo[0], b.lo[1], z - th), (b.hi[0], b.hi[1], z), face="floor",
                 chamber=b.chamber)
        )  # fmt: skip
        cum += th
    return out


def firebox_parts(kiln: Kiln) -> list[Part]:
    """Every firebox's walls, floor and roof, as boxes."""
    s = site(kiln)
    parts: list[Part] = []
    for b in firebox_boxes(kiln):
        tag = f"firebox-{b.index}"
        if b.trough:
            bottom = b.level - s.floor_t
            if b.lo[2] < bottom - 1e-6:
                parts += _lined(kiln, tag, b.lo, (b.hi[0], b.hi[1], bottom), None, False,
                                b.chamber)  # fmt: skip
            else:
                # Shallower than the floor: the floor's layers under it, in the cut
                parts += _trough_floor(kiln, tag, b)
            continue
        if b.kiln_side == "up":
            parts += _lined(kiln, tag, b.lo, b.hi, None, False, b.chamber)
            continue
        # Below the kiln's floor the kiln has no wall, so the firebox builds its own there
        cut = b.level - s.floor_t
        if b.lo[2] < cut - 1e-6:
            parts += _lined(kiln, f"{tag}/pit", b.lo, (b.hi[0], b.hi[1], cut), None, False,
                            b.chamber)  # fmt: skip
            parts += _lined(kiln, tag, (b.lo[0], b.lo[1], cut), b.hi, b.kiln_side, True,
                            b.chamber, floor_=False)  # fmt: skip
        else:
            parts += _lined(kiln, tag, b.lo, b.hi, b.kiln_side, True, b.chamber)
    return parts


# --- Openings -----------------------------------------------------------------------------------


def _spread(u0: float, u1: float, width: float, k: int) -> list[tuple[float, float]]:
    """``k`` holes ``width`` wide, spread evenly across u0–u1, each in its own share of it; one
    hole the whole way across if they don't fit side by side."""
    if k * width >= u1 - u0 - 1e-6:
        return [(u0, u1)]
    share = (u1 - u0) / k
    return [(u0 + share * (i + 0.5) - width / 2, u0 + share * (i + 0.5) + width / 2)
            for i in range(k)]  # fmt: skip


def inlets_fit(b: FireboxBox) -> bool:
    """Whether a firebox's inlet flues fit side by side across it."""
    fb = b.box
    if fb.inlet is None:
        return True
    w = fb.inlet.size_in()[0] * IN
    u0, u1 = (b.lo[0], b.hi[0]) if b.along_y else (b.lo[1], b.hi[1])
    return fb.inlets * w < u1 - u0 - 1e-6


def openings(kiln: Kiln) -> list[Opening]:
    """The holes the fireboxes need: inlet flues (or the open mouth) into the chamber, troughs
    sunk in the floor, stoke holes and ash-pit mouths."""
    s = site(kiln)
    walls = sum(si(x.thickness, "mm") for x in kiln.lining.walls)
    out: list[Opening] = []
    for b in firebox_boxes(kiln):
        tag = f"firebox-{b.index}"
        fb = b.box
        (x0, y0, z0), (x1, y1, z1) = b.lo, b.hi
        if b.trough:
            # Through the floor's whole depth: the trough is lined below it
            bottom = min(z0, b.level - s.floor_t)
            out.append(Opening(f"{tag}/trough", (x0, y0, bottom), (x1, y1, b.level + EPS)))
            continue
        if b.kiln_side == "up":
            if fb.inlet is not None:
                iw, ih = fb.inlet.size_in()
                iw, ih = iw * IN, ih * IN
                zs = (z1 - EPS, z1 + s.floor_t + EPS)
                for a0, a1 in _spread(x0, x1, iw, fb.inlets):
                    out.append(Opening(f"{tag}/inlet", (a0, y1 - ih, zs[0]), (a1, y1, zs[1]),
                                       fb.inlet.round and a1 - a0 < iw + 1e-6, 2))  # fmt: skip
        else:
            # Through the kiln's wall, from the firebox's face to the chamber's inside
            kiln_side = b.kiln_side
            axis = 1 if b.along_y else 0
            if axis == 1:
                near = y1 if kiln_side == "+y" else y0
            else:
                near = x1 if kiln_side == "+x" else x0
            u0, u1 = (x0, x1) if axis == 1 else (y0 - s.middle, y1 - s.middle)
            inner = _inside_face(s, kiln_side, near, (u0, u1))
            a, z = (min(near, inner) - EPS, max(near, inner) + EPS), b.level
            u0, u1 = (x0, x1) if axis == 1 else (y0, y1)
            # No wider than the chamber's inside behind it
            lim = (s.width / 2) if axis == 1 else None
            lo_u, hi_u = (max(u0, -lim), min(u1, lim)) if lim is not None else (u0, u1)
            if fb.inlet is not None:
                iw, ih = fb.inlet.size_in()
                iw, ih = iw * IN, ih * IN
                for a0, a1 in _spread(lo_u, hi_u, iw, fb.inlets):
                    round_ = fb.inlet.round and a1 - a0 < iw + 1e-6
                    out.append(_through(f"{tag}/inlet", axis, a, (a0, a1), (z, z + ih), round_))
            else:
                lo_u, hi_u, height = _mouth(kiln, s, kiln_side, (lo_u, hi_u), z1 - z)
                if height > 1e-6 and hi_u - lo_u > 1e-6:
                    out.append(_through(f"{tag}/mouth", axis, a, (lo_u, hi_u), (z, z + height),
                                        False))  # fmt: skip
        # The mouth wall: its stoke hole, and the ash pit's open mouth
        mouth = b.mouth
        axis = 0 if mouth in ("-x", "+x") else 1
        face = {"-x": x0, "+x": x1, "-y": y0, "+y": y1}[mouth]
        outward = face - walls if mouth.startswith("-") else face + walls
        a = (min(face, outward) - EPS, max(face, outward) + EPS)
        u0, u1 = (y0, y1) if axis == 0 else (x0, x1)
        if fb.stoke_hole is not None:
            sw, sh = fb.stoke_hole.size_in()
            sw, sh = sw * IN, sh * IN
            c = (u0 + u1) / 2
            zs = (b.grate_z, min(b.grate_z + sh, z1))
            hole = _through(f"{tag}/stoke-hole", axis, a, (c - sw / 2, c + sw / 2), zs, False)
            out.append(replace(hole, round=fb.stoke_hole.round))
        if fb.grate is not None and b.grate_z - z0 > 1e-6:
            out.append(_through(f"{tag}/ash-pit", axis, a, (u0, u1), (z0, b.grate_z), False))
    return out


def _mouth(
    kiln: Kiln, s: Site, kiln_side: str, u: tuple[float, float], tall: float
) -> tuple[float, float, float]:
    """The largest rectangle, no taller than the firebox, that fits the chamber's inside where the
    firebox's mouth opens through the wall: under the arch or dome that meets an end wall of a
    single chamber, or up to the springline (u0, u1, height; mm)."""
    from kilndesigner.geometry import in_a_row, inside_top

    if s.radius is not None or in_a_row(kiln) or kiln_side in ("+x", "-x"):
        return u[0], u[1], min(tall, s.height)
    face = "front" if kiln_side == "+y" else "back"
    sign = 1 if face == "front" else -1  # across, seen from outside: x for the front, -x behind

    def top(x: float) -> float:
        return inside_top(kiln, face, sign * x)

    best = (u[0], u[1], 0.0)
    xs = [u[0] + (u[1] - u[0]) * k / 64 for k in range(65)]
    for h in sorted({min(tall, top(x)) for x in xs}):
        if h <= 0:
            continue
        inside = [x for x in xs if top(x) >= h - 1e-6]
        a, b = min(inside), max(inside)
        if (b - a) * h > (best[1] - best[0]) * best[2]:
            best = (a, b, h)
    return best


def _inside_face(s: Site, kiln_side: str, near: float, u: tuple[float, float]) -> float:
    """The chamber's inside face behind a firebox's face at ``near``: a round wall's where it
    comes nearest the middle across the firebox, so the hole reaches the inside everywhere."""
    if s.radius is not None:
        far = min(max(abs(u[0]), abs(u[1])), 0.99 * s.radius)
        return math.copysign(math.sqrt(s.radius**2 - far**2), near)
    if kiln_side == "+y":
        return s.front
    if kiln_side == "-y":
        return s.back
    return -s.width / 2 if kiln_side == "+x" else s.width / 2


def _through(
    name: str, axis: int, along: tuple[float, float], u: tuple[float, float],
    z: tuple[float, float], round_: bool,
) -> Opening:  # fmt: skip
    if axis == 1:
        return Opening(name, (u[0], along[0], z[0]), (u[1], along[1], z[1]), round_, 1)
    return Opening(name, (along[0], u[0], z[0]), (along[1], u[1], z[1]), round_, 0)


# --- Carving boxes ------------------------------------------------------------------------------


def _plain(p: Part) -> bool:
    return (
        p.arch is None and p.profile is None and p.dome is None and p.revolve is None
        and p.plan is None and p.groin is None
    )  # fmt: skip


def carve(parts: list[Part], holes: list[Opening]) -> list[Part]:
    """The parts with each hole taken out of the plain boxes it passes through: a box less a box
    is up to six boxes, named after the box with a letter. Curved parts keep their volume and are
    cut in the model only."""
    out: list[Part] = []
    for p in parts:
        pieces = [p]
        if _plain(p):
            for h in holes:
                pieces = [q for piece in pieces for q in _minus(piece, h.lo, h.hi)]
        if len(pieces) == 1:
            out.append(replace(pieces[0], name=p.name))
            continue
        out += [replace(q, name=f"{p.name}-{chr(ord('a') + k)}") for k, q in enumerate(pieces)]
    return out


def _minus(p: Part, lo: Vec, hi: Vec) -> list[Part]:
    """The box less the box lo–hi: the slabs either side of it, axis by axis."""
    a, b = p.lo, p.hi
    if any(hi[i] <= a[i] + 1e-6 or lo[i] >= b[i] - 1e-6 for i in range(3)):
        return [p]
    pieces: list[Part] = []
    cur_lo, cur_hi = list(a), list(b)
    for i in range(3):
        if lo[i] > cur_lo[i] + 1e-6:
            q_hi = list(cur_hi)
            q_hi[i] = lo[i]
            pieces.append(replace(p, lo=(cur_lo[0], cur_lo[1], cur_lo[2]),
                                  hi=(q_hi[0], q_hi[1], q_hi[2])))  # fmt: skip
            cur_lo[i] = lo[i]
        if hi[i] < cur_hi[i] - 1e-6:
            q_lo = list(cur_lo)
            q_lo[i] = hi[i]
            pieces.append(replace(p, lo=(q_lo[0], q_lo[1], q_lo[2]),
                                  hi=(cur_hi[0], cur_hi[1], cur_hi[2])))  # fmt: skip
            cur_hi[i] = hi[i]
    return pieces


# --- Grates -------------------------------------------------------------------------------------


def grates(kiln: Kiln) -> list[GrateBars]:
    """Each grate's bars: ¾ in round, the grate's gap apart, from the mouth back."""
    us = kiln.units == "us"
    out: list[GrateBars] = []
    for b in firebox_boxes(kiln):
        g = b.box.grate
        if g is None or g.gap is None or b.trough:
            continue
        gw, gl, gap = si(g.width, "mm"), si(g.length, "mm"), si(g.gap, "mm")
        (x0, y0, _), (x1, y1, _) = b.lo, b.hi
        along = 1 if b.along_y else 0
        span = (x1 - x0) if along == 1 else (y1 - y0)
        gw = min(gw, span)
        long = min(gl, (y1 - y0) if along == 1 else (x1 - x0))
        n = max(1, math.floor((gw + gap) / (BAR + gap) + 1e-9))
        width = n * BAR + (n - 1) * gap
        mouth = b.mouth
        start = {"-y": y0, "+y": y1, "-x": x0, "+x": x1}[mouth]
        mid_run = start + long / 2 if mouth.startswith("-") else start - long / 2
        mid_u = ((x0 + x1) / 2) if along == 1 else ((y0 + y1) / 2)
        z = b.grate_z - BAR / 2
        centres: list[Vec] = []
        for i in range(n):
            u = mid_u - width / 2 + BAR / 2 + i * (BAR + gap)
            centres.append((u, mid_run, z) if along == 1 else (mid_run, u, z))
        out.append(
            GrateBars(
                f"firebox-{b.index}/grate", f"Firebox {b.index}, grate",
                f"{n} bars of ¾ in round steel, {length_text(long, us)} long, "
                f"{length_text(gap, us)} apart (Olsen p.199–200: rods ¾–1 in)",
                n, long, along, tuple(centres),
            )
        )  # fmt: skip
    return out


def grate_pieces(kiln: Kiln) -> list[Piece]:
    """The grate bars as hardware pieces, for the model."""
    from kilndesigner.hardware import Cylinder, Piece

    out: list[Piece] = []
    for g in grates(kiln):
        axis: Literal[0, 1] = 1 if g.axis == 1 else 0
        cyl = tuple(Cylinder(axis, c, BAR / 2, g.length) for c in g.centres)
        out.append(Piece(g.name, "steel", g.title, g.detail, cylinders=cyl))
    return out


def firebox_findings(kiln: Kiln) -> list[Finding]:
    """How the fireboxes are built, and what is left out."""
    boxes = firebox_boxes(kiln)
    if not boxes:
        return []
    us = kiln.units == "us"
    notes: list[str] = []
    for b in boxes:
        fb = b.box
        where = (
            f"a trough sunk in chamber {b.chamber}'s floor along its front"
            if b.trough
            else "under the floor"
            if b.kiln_side == "up"
            else f"against the {fb.position} wall"
        )
        bits = [f"Firebox {b.index}, {where}"]
        if fb.height is None:
            bits.append(f"drawn {length_text(si(fb.width, 'mm'), us)} tall, as wide as it is, as "
                        "its height isn't given")  # fmt: skip
        if b.kiln_side == "up" and not b.trough and fb.inlet is None:
            bits.append("no inlet flue size is given, so the floor over it is left solid: give "
                        "the firebox an inlet")  # fmt: skip
        if not inlets_fit(b):
            bits.append(f"its {fb.inlets} inlet flues don't fit side by side across it, so one "
                        "opening its whole width is cut")  # fmt: skip
        if fb.grate is not None and fb.grate.gap is None:
            bits.append("its grate's bar spacing isn't given, so no bars are drawn or listed")
        if fb.grate is not None:
            ash = grate_heights(fb)[1]
            said = []
            if fb.ash_pit is None:
                said.append(f"its ash pit {length_text(ash, us)} deep, as deep as the space "
                            "above the grate (Olsen's grate at the vertical midpoint, "
                            "p.199–200)")  # fmt: skip
            if fb.step is None and b.kiln_side != "up":
                said.append("its grate level with the chamber floor, as no step is given")
            if said:
                bits.append("drawn with " + " and ".join(said))
        notes.append(", ".join(bits))
    message = (
        "Fireboxes are built of the kiln's own layers, the walls' round their sides and over "
        "their roofs, the floor's under them; no source here gives a firebox its own lining. "
        "Against a wall, the grate sits its step below the chamber floor, so smouldering coals "
        "fall into the front stacking (p.188), and the inlet flues are cut at the floor's level "
        "in the wall between; below the kiln's floor the firebox has walls of its own. Stoke "
        "holes are cut with their foot at the grate (p.188), and ash pits are left open at the "
        "mouth (p.188). The flat roofs are drawn of the walls' layers: span them with an arch, "
        "bricks or kiln shelves as Olsen does (p.145). " + "; ".join(notes) + "."
    )
    return [Finding(level="info", message=message, reference=FIREBOX_SOURCE),
            *grate_findings(kiln, boxes)]  # fmt: skip


def grate_sheets(kiln: Kiln, b: FireboxBox) -> list[Sheet]:
    """The one thing a grate firebox against a wall must do whatever it is fired for: rise above
    the chamber floor, so its flame has a way in. Its heights otherwise are the builder's choice
    and are reported, not judged (grate_findings)."""
    if b.kiln_side == "up" or b.trough:
        return []
    fh, _, step = grate_heights(b.box)
    given = "the design: the firebox"
    s = Sheet(f"firebox.reaches-floor.{b.index}",
              f"Firebox {b.index} rises above the chamber floor",
              reference=FIREBOX_SOURCE)  # fmt: skip
    s.given("a", "space above the grate", Q_(fh, "mm").to("in"), "in", source=given)
    s.given("e", "grate to chamber floor", Q_(step, "mm").to("in"), "in", source=given)
    s.require("a", ">", "e")
    s.lever("a", Q_(1, "in"), Q_(60, "in"))
    return [s]


def grate_findings(kiln: Kiln, boxes: list[FireboxBox]) -> list[Finding]:
    """Each grate firebox's heights, with what Olsen gives for each way of firing. A wood or coal
    firebox is built for the effect wanted, so these are options to weigh, not limits: the most
    heat from a high grate with the most air under it (his fast-fire kilns), an even burn from the
    grate at the midpoint, or ash carried up round the ware for ash glazing and flashing, the
    firebox part of the first chamber (the user, a kiln builder, 2026-10-30)."""
    us = kiln.units == "us"
    ft3 = chamber_shape(kiln).volume / si(Q_(1, "ft**3"), "m**3")
    out: list[Finding] = []
    for b in boxes:
        if b.box.grate is None:
            continue
        fh, ash, step = grate_heights(b.box)
        for sheet in grate_sheets(kiln, b):
            if (check := sheet.check()).status != "pass":
                out.append(Finding.failed(check, (
                    f"Firebox {b.index} is {length_text(fh, us)} tall above its grate, which is "
                    f"{length_text(step, us)} below the chamber floor, so it doesn't reach the "
                    "floor and its flame has no way into the chamber: make it taller or the step "
                    "less.")))  # fmt: skip
        share = ash / (ash + fh) if ash + fh > 0 else 0.0
        where = (
            f", the grate {length_text(step, us)} below the chamber floor"
            if b.kiln_side != "up" and not b.trough
            else ""
        )
        band = (
            f" This kiln is {ft3:.0f} ft³, inside the 30–100 ft³ for which Olsen gives 12–18 in "
            "below the grate and the same above (p.199)."
            if 30 <= ft3 <= 100
            else f" This kiln is {ft3:.0f} ft³; Olsen's 12–18 in below and above is for "
            "30–100 ft³ kilns (p.199), and the shortest he gives is 12½ in with the grate at "
            "6–7 in, on a 12–16 ft³ fast-fire kiln."
        )
        out.append(Finding(level="info", reference=GRATE_HEIGHT_SOURCE, message=(
            f"Firebox {b.index}: {length_text(fh, us)} above the grate and an ash pit "
            f"{length_text(ash, us)} below it ({share:.0%} of its height below the grate){where}. "
            "How high to set the grate depends on the firing wanted. Olsen sets it at the "
            "vertical midpoint (Fig. 8-2, p.199–200; the Breda kiln's equal volumes above and "
            "below, p.167); for the most heat his fast-fire kilns put more than half below, for "
            "the most air under the coals (p.140, p.204); a grate set too low chokes the coals "
            "(p.199). A 9–12 in rise from the grate to the chamber floor drops smouldering coals "
            "into the front stacking (p.188), and Fig. 7-3 steps up 12–15 in (p.179). Kilns "
            "fired for ash glazing and flashing make the firebox part of the first chamber, so "
            "the ash rides up round the pots: a step of 0 in, the default." + band
        )))  # fmt: skip
    return out


def model_holes(kiln: Kiln) -> list[tuple[Vec, Vec, object]]:
    """The fireboxes' openings as solids, to cut the model's curved parts."""
    from kilndesigner.geometry import _box, _cylinder  # pyright: ignore[reportPrivateUsage]

    out: list[tuple[Vec, Vec, object]] = []
    for o in openings(kiln):
        if any(q - p < 1e-6 for p, q in zip(o.lo, o.hi, strict=True)):
            continue
        if o.round:
            centre = tuple((p + q) / 2 for p, q in zip(o.lo, o.hi, strict=True))
            across = [o.hi[i] - o.lo[i] for i in range(3) if i != o.axis]
            solid = _cylinder(o.axis, centre, min(across) / 2, o.hi[o.axis] - o.lo[o.axis])  # type: ignore[arg-type]
        else:
            solid = _box(o.lo, o.hi)
        out.append((o.lo, o.hi, solid))
    return out


__all__ = [
    "FireboxBox",
    "GrateBars",
    "carve",
    "firebox_boxes",
    "firebox_findings",
    "firebox_parts",
    "grate_pieces",
    "grates",
    "model_holes",
    "openings",
]
