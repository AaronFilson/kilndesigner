"""Every reference kiln's own draft path (C1, `docs/planning/11-10-26.md`): the gas path of a
design as built, from the air intakes to the chimney's top, as Idelchik's elements in series and
parallel groups (`draft.py`), each piece where the engine lays it out (`firebox_parts`,
`run_parts`, `openings`, `massing`).

The forms, each said in the path's working:

- **The heat source.** Stoked fireboxes under the floor, their inlet flues up through it (the
  fast-fire's, as first built); against a wall or on a diagonal, through their inlet flues or
  their whole mouth in that wall (`firebox_parts.openings`), the fire's column from the grate to
  the passage's middle; troughs sunk in a chamber's floor, the chamber's own fire, their air
  through its side stoke holes; gas burners' ports through a wall, at given places, up through
  the floor (an updraft's) or into a firebox of their own; an oil drip's ports. Several firebox
  sets are parallel branches joined in the chamber they feed.
- **The chambers.** One, its climb a column (on a slope, turned as `massing.place` turns the run);
  one cut into segments, each its own zone, the gas crossing each cut at the tube's mid-height (an
  assumption, said); chambers in a row in series through the flue holes in the walls between them
  (Idelchik 8-4, a wall with through-gaps), each chamber's climb a column on `run_parts`' stepped
  floors. Fired in stages (`series.py`), the stoked chamber's side stoke holes are a second inlet
  beside the front's path, the two joined in that chamber.
- **The exits.** One flue port; sets of exit flues through a wall, the floor or the roof
  (`draft.exits`, where the engine cuts them), several sets in parallel; an open top; none given:
  p.78's rule, inlet = exit = chimney section, an assumption with its page.
- **The chimney.** Beside the kiln (the run, the turn up, its column, its friction, its top; a
  tapered one narrowing from the kiln's top, p.80), through the crown, several side by side, none
  over an updraft, whose chamber is its stack (p.80), or a bottle over its dome (Breda). One the
  design doesn't give is read in this order: the dataset's printed, scaled or drawn sizes (the
  caller's `Inputs`), then p.78's section, then a stated band for a height no source gives, from
  the book's own rules (least: twice the downward pull, p.130, Fig 5-2, or a climbing kiln's line
  through its chamber tops, p.81; most: Rule 5, p.80, or 3 × a climbing kiln's rise, p.101).

What the design file can't say comes in as builder inputs (`Inputs`), filled by the caller from
the dataset (`core/tests/v2/reference_kilns.yaml`). A size no source gives is left out and said,
so the path's air is an upper bound (`Path.left_out`); where nothing bounds a piece of the path,
it is refused, naming the input.

Frame: metres, z up from the first chamber's floor, as the engine lays the kiln out.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, replace
from functools import cached_property
from typing import Any

from fluids.atmosphere import ATMOSPHERE_1976  # pyright: ignore[reportMissingTypeStubs]

from kilndesigner.model import CatenaryArch, Dome, FlatRoof, Kiln, OpenTop, Port, SprungArch
from kilndesigner.units import si
from kilndesigner.v2.heat import draft as dr
from kilndesigner.v2.heat.draft import Element, NotModelledError
from kilndesigner.v2.heat.gas import ATM
from kilndesigner.working import Step

IN, MM = 0.0254, 1e-3
SIDES = {"up": "under", "+y": "front", "-y": "back", "+x": "left", "-x": "right"}
P78 = "Olsen p.78 (natural draft: inlet flue area = exit flue area = chimney section)"
P78_GAS = "Olsen p.78 (pressurized gas: inlet area = exit area, 'a safe rule of thumb')"
P174 = "Olsen pp.173–174 (an updraft over about 40 ft³: about 20 % less inlet than exit)"
P80 = "Olsen p.80, Principle 4 (tapering can begin once the chimney passes the top of the arch)"
HEIGHT_RULES = (
    "Olsen p.130, Fig 5-2 (the least: twice the downward pull) and p.80, Rule 5 (the most: 3 ft "
    "per ft of downward pull + 1 ft per 3 ft of horizontal pull)"
)
CLIMBING_RULES = (
    "Olsen p.81, Principle 8 (the least: the line through the chamber tops) and p.101 (the most: "
    "the Bizen kiln's, about 3 × the kiln's total rise)"
)
MID_HEIGHT = (
    "the gas taken across each cut between a tube's segments at the tube's mid-height (half the "
    "crown's height): an assumption, the well-stirred zones say nothing of where it crosses"
)
RULE_6 = (
    "Olsen pp.79–80, Rule 6 (the chimney ¼ to ⅕ of the chamber's diameter, seldom under 9 × 9 in "
    "at the base in natural draft)"
)
RULE_6_NOTE = (
    "rests on Rule 6 seeding p.78 where nothing on the path is sized: a stated band, the owner's "
    "question 8 (C1, 11-10-26.md), open"
)
MIN_CHIMNEY = 9 * 0.0254  # m: "seldom under 9 x 9in" (p.80)
TAPER_STEPS = 8  # a tapered chimney's friction summed over this many slices


@dataclass(frozen=True)
class Band:
    """A length (m) the design doesn't give, as a band from its least-air end to its most-air
    end (the smaller and the larger: a taller chimney or a wider passage draws more), and where
    it comes from."""

    lo: float
    hi: float
    source: str

    def __post_init__(self) -> None:
        if not 0 < self.lo <= self.hi:
            raise ValueError("a band runs from its least to its most, more than zero")

    def end(self, most: bool) -> float:
        return self.hi if most else self.lo


@dataclass(frozen=True)
class Flues:
    """Openings the design doesn't give (or gives otherwise), each size a band (m): ``count`` of
    them, each ``width`` across and ``height`` tall, round of diameter ``width`` when ``round``.
    One left out is p.78's: the count with both sizes given (as many as the area takes), else a
    size, the area over the count (one where it isn't given) and the other size. Or their whole
    ``area`` alone (each square): an open top's way out past what stands in it."""

    width: Band | None = None
    count: int | None = None
    height: Band | None = None
    round: bool = False
    source: str = ""
    area: Band | None = None

    def __post_init__(self) -> None:
        if self.width is None and self.height is None and self.area is None:
            raise ValueError("give a set of flues its width, its height or its area")


@dataclass(frozen=True)
class Stack:
    """A chimney as the dataset gives it, in place of the design's or where it gives none: its
    height from the first chamber's floor and its inside section, each a band (m; a round one's
    ``width`` its diameter), its top's section (m) where it tapers, its own exit flues, and how
    many of it stand side by side."""

    height: Band | None = None
    width: Band | None = None
    depth: Band | None = None
    round: bool = False
    top: tuple[float, float] | None = None
    exits: Flues | None = None
    count: int | None = None
    source: str = ""


@dataclass(frozen=True)
class Inputs:
    """What the path needs that the design file can't say, from the dataset (the caller's):

    - ``grate_bar``: the grate's bar thickness (m);
    - ``intake``: the air intakes (`draft.Intakes`), all the fireboxes' together, or one for each
      firebox entry in the design's order (None: that entry's design openings);
    - ``stack``: the chimney as the dataset gives it (`Stack`);
    - ``exits``, ``inlets``, ``between``: exit flues, each firebox's inlet flues, the flues between
      chambers, where the design gives none or the dataset prints them otherwise (`Flues`);
    - ``connection``: the flue from the kiln into the chimney, (width, height) bands;
    - ``stage``: a row fired in stages, the chamber stoked (from 0, as `series.Stage`), its side
      stoke holes an inlet beside the front's path (closed with ``front_open`` False);
    - ``one_per_chamber``: a firebox entry with as many as the row has chambers laid one to a
      chamber, the book's troughs (the owner's question 3), not side by side at the front;
    - ``updraft``: the dataset's draft where the design has none (the oil-drip kiln's);
    - ``stackless``: the dataset prints no stack (Tamba's end chamber, "open chimney holes and no
      stack", p.88): the last chamber's exits open to the room through its roof;
    - ``rule6``: where nothing on the path is sized, seed p.78 with Olsen's Rule 6, the chimney's
      side ⅕ to ¼ of the chamber's width and at least 9 in (pp.79–80), a band (the owner's question
      8, C1: open, so it is asked for, and every path on it says so).
    """

    grate_bar: float | None = None
    intake: dr.Intakes | tuple[dr.Intakes | None, ...] | None = None
    stack: Stack | None = None
    exits: Flues | None = None
    inlets: Flues | None = None
    between: Flues | None = None
    connection: tuple[Band, Band] | None = None
    stage: int | None = None
    front_open: bool = True
    one_per_chamber: bool = False
    updraft: bool = False
    stackless: bool = False
    rule6: bool = False


def kiln_path(
    kiln: Kiln, inputs: Inputs | None = None, *, rough: float = dr.ROUGH, segments: int = 1
) -> dr.Path:
    """The gas path of a design (module docstring), drawn at its bands' least-air end, the most-air
    end's elements beside it where a length is a band (`Path.alt`)."""
    given = inputs or Inputs()
    laid = _Laid(kiln)
    least = _Build(kiln, given, segments, False, laid).path(rough)
    most = _Build(kiln, given, segments, True, laid).path(rough)
    alt = None if most.elements == least.elements else most.elements
    return replace(least, alt=alt)


class _Laid:
    """The engine's layout of the fireboxes and their openings, worked out once a path."""

    def __init__(self, kiln: Kiln) -> None:
        self.kiln = kiln

    @cached_property
    def boxes(self) -> list[Any]:
        from kilndesigner.firebox_parts import firebox_boxes

        return firebox_boxes(self.kiln)

    @cached_property
    def all_holes(self) -> list[Any]:
        """Every opening the fireboxes need, as `firebox_parts.openings` cuts them."""
        from kilndesigner.firebox_parts import openings

        return list(openings(self.kiln))

    @cached_property
    def holes(self) -> dict[str, Any]:
        """The first opening of each name (a firebox's inlet flues share one)."""
        out: dict[str, Any] = {}
        for o in self.all_holes:
            out.setdefault(o.name, o)
        return out

    def passage(self, b: Any) -> bool:
        """Whether the engine's layout gives a firebox a way into the chamber: an inlet flue or
        its mouth of some size."""
        names = (f"firebox-{b.index}/inlet", f"firebox-{b.index}/mouth")
        return any(
            o.name in names and all(h - lo > 1e-6 for lo, h in zip(o.lo, o.hi, strict=True))
            for o in self.all_holes
        )


# --- helpers -------------------------------------------------------------------------------------


def _thickness(kiln: Kiln, face: str) -> float:
    return sum(si(x.thickness, "m") for x in kiln.lining.for_face(face))  # pyright: ignore[reportArgumentType]


def _area(w: float, h: float, rnd: bool) -> float:
    return math.pi * w * w / 4 if rnd else w * h


def _port(p: Port) -> tuple[float, float, bool]:
    w, h = p.size_in()
    return w * IN, h * IN, p.round


def chimney_zone(kiln: Kiln) -> bool:
    """Whether the heat model builds the chimney as a gas zone of its own: as `chamber._stack`
    does, a chimney beside the kiln with its section given, fed by one flue port in the back or
    front wall. Otherwise the chimney's gas is the last chamber's (`Path.alias`)."""
    d = kiln.draft
    return (
        d is not None
        and d.chimney is not None
        and d.chimney.inside is not None
        and d.flue_port is not None
        and d.type != "up"
        and d.chimney_through == "beside"
        and d.chimneys == 1
        and d.exits is None
        and d.flue_wall in ("back", "front")
    )


def _merged(els: list[Element]) -> list[Element]:
    """Columns of one zone next to each other as one, under the later's name (it says where the
    gas goes); columns of no height left out."""
    out: list[Element] = []
    for e in els:
        if out and e.kind == "column" and out[-1].kind == "column" and out[-1].zone == e.zone:
            out[-1] = replace(e, rise=out[-1].rise + e.rise)
        else:
            out.append(e)
        if out[-1].kind == "column" and abs(out[-1].rise) < 1e-12:
            out.pop()
    return out


def _group(name: str, branches: Sequence[Sequence[Element]]) -> list[Element]:
    """Branches in parallel, joined where they meet: one branch is just its elements."""
    kept = [_merged(list(b)) for b in branches]
    if len(kept) == 1:
        return kept[0]
    return [Element(name, "parallel", "", parts=tuple(tuple(b) for b in kept))]


@dataclass
class _Feed:
    """A way in: its elements from the room to where it enters ``node`` at height ``z`` (m)."""

    name: str
    els: list[Element]
    node: int
    z: float


@dataclass
class _Exit:
    """A set of identical exit flues: through a wall, the floor or the roof (or the open top),
    each ``w`` × ``h`` (m; round of diameter ``w``), their middles at ``z`` (m), through a face
    ``thick`` thick, ``along`` the mean distance of floor holes from the flue wall (m)."""

    name: str
    count: int
    w: float
    h: float
    rnd: bool
    through: str
    z: float
    thick: float
    along: float = 0.0

    @property
    def area(self) -> float:
        return _area(self.w, self.h, self.rnd)


class _Build:
    """One end of the path's bands (``most``: each length band at its most-air end)."""

    def __init__(self, kiln: Kiln, inputs: Inputs, segments: int, most: bool, laid: _Laid) -> None:
        from kilndesigner.firebox_parts import site

        self.kiln, self.inputs, self.most, self.laid = kiln, inputs, most, laid
        self.notes: list[str] = []
        self.left: list[str] = []
        c = kiln.chamber
        self.n = c.chambers
        if segments < 1:
            raise NotModelledError("a tube is cut into one segment or more")
        if segments > 1 and (self.n > 1 or c.shape == "round"):
            raise NotModelledError("segments cut a single box chamber; chambers in a row are zones")
        self.segments = segments
        self.nodes = self.n if self.n > 1 else segments
        draft = kiln.draft
        self.updraft = draft.type == "up" if draft is not None else inputs.updraft
        self.site = site(kiln)
        self.slope = math.radians(si(c.slope, "degree")) if c.slope is not None else 0.0
        self.depth = si(c.depth, "m")
        self.width = si(c.width, "m")
        self.height = si(c.height, "m")
        self.rise = si(kiln.roof.rise, "m") if isinstance(kiln.roof, SprungArch | Dome) else 0.0
        self.stack_zone = "chimney" if chimney_zone(kiln) else "stack"
        self.run: Any = None
        if self.n > 1:
            from kilndesigner.run_parts import run_layout

            self.run = run_layout(kiln)

    # --- the frame ---------------------------------------------------------------------------

    def zone(self, k: int) -> str:
        return f"chamber {k + 1}" if self.nodes > 1 else "chamber"

    def floor(self, k: int) -> float:
        """Node k's reference height: its floor's (m), a segment's where it starts."""
        if self.run is not None:
            return float(self.run.floor(k)) * MM
        return k * self.depth / self.nodes * math.sin(self.slope)

    def z_at(self, y: float, z: float) -> float:
        """A point laid out level (m: y along the run, z up from its chamber's floor) where the
        kiln stands: a single chamber turned up its slope (`massing.place`), a row's chambers
        stepped (`run_parts`), so a row's points are already at their height."""
        if self.run is not None:
            return z
        from kilndesigner.massing import place, run_of

        return place(run_of(self.kiln), (0.0, y / MM, z / MM))[2] * MM

    # --- the path ----------------------------------------------------------------------------

    def path(self, rough: float) -> dr.Path:
        heat = self.kiln.heat
        if heat.electric is not None and heat.gas is None and heat.fire is None:
            raise NotModelledError("an electric kiln draws no air for its heat: no draft path")
        if heat.gas is not None and heat.fire is not None:
            raise NotModelledError("v2's draft takes one kind of heat: fireboxes or gas burners")
        t_room = si(self.kiln.site.ambient, "K")
        pressure = ATM
        if self.kiln.site.elevation is not None:
            z_site = si(self.kiln.site.elevation, "m")
            pressure = float(ATMOSPHERE_1976(z_site).P)
            self.notes.append(
                f"{z_site:.0f} m up: {pressure:.0f} Pa (US Standard Atmosphere 1976, fluids)"
            )
        els = self.series()
        els += self.leave()
        els = _merged(els)
        flat = list(_flatten(els))
        odd = [e.name for e in flat if e.sides is not None
               and not 0.5 <= e.sides[0] / e.sides[1] <= 2.0]  # fmt: skip
        if odd:
            self.notes.append(
                "turbulent friction as a circle's on D_h for "
                + ", ".join(dict.fromkeys(odd))
                + ": past Idelchik's 0.5–2 side ratio for that (item 17), none other read"
            )
        if self.left:
            self.notes.append("left out for want of a size, so the air is an upper bound: "
                              + "; ".join(self.left))  # fmt: skip
        step = Step(
            name="The gas path",
            value=_describe(els),
            inputs={e.name: f"Δz {e.rise:.3f} m" for e in flat if e.kind == "column"}
            | {e.name: e.note for e in flat if e.note},
            reference=f"the design file; the fittings from {dr.IDELCHIK}; friction fluids 1.3",
            note="; ".join([*dict.fromkeys(self.notes), dr.FITTINGS_NOTE]),
        )
        alias: tuple[tuple[str, str], ...] = ()
        if self.stack_zone == "stack":
            alias = (("stack", self.zone(self.nodes - 1)),)
        return dr.Path(tuple(els), t_room, pressure, rough, (step,), alias=alias,
                       left_out=tuple(dict.fromkeys(self.left)))  # fmt: skip

    def series(self) -> list[Element]:
        """The way in and the chambers in series, to the last node's floor."""
        stage = self.inputs.stage
        if stage is not None and not 0 <= stage < self.nodes:
            raise NotModelledError(f"no chamber {stage + 1} to stoke: the kiln has {self.nodes}")
        front = self.feeds() if stage is None or self.inputs.front_open else []
        if not front:
            self.notes.append("the front's intakes closed for the stage")
        assert front or stage is not None  # every heat source has a way in at the front
        els = self.join(front, 0) if front else []
        for k in range(self.nodes):
            if stage == k:
                side = self.side(k)
                to_floor = column_to(self.zone(k), self.floor(k) - side.z)
                if front:
                    els = _group(f"chamber {k + 1}'s side stoke holes beside the front's path",
                                 [els, [*side.els, to_floor]])  # fmt: skip
                else:
                    els = [*side.els, to_floor]
            if k < self.nodes - 1 and (front or (stage is not None and k >= stage)):
                els += self.passage(k)
        return els

    def join(self, feeds: list[_Feed], node: int) -> list[Element]:
        """Feeds into one node, each brought to its floor; several in parallel."""
        zone, floor = self.zone(node), self.floor(node)
        branches = [[*f.els, column_to(zone, floor - f.z)] for f in feeds]
        return _group("the fireboxes, side by side", branches)

    # --- the ways in -------------------------------------------------------------------------

    def feeds(self) -> list[_Feed]:
        heat = self.kiln.heat
        if heat.gas is not None:
            return self.burners()
        fire = heat.fire
        assert fire is not None
        boxes = self.laid.boxes
        intakes = self.inputs.intake
        total = sum(fb.count for fb in fire.fireboxes)
        if total > fire.fireboxes[0].count and isinstance(intakes, dr.Intakes):
            self.notes.append("the intakes shared among the fireboxes by their count")
        out: list[_Feed] = []
        for j, fb in enumerate(fire.fireboxes):
            mine = [b for b in boxes if b.box is fb]
            ins: dr.Intakes | None = None
            if isinstance(intakes, tuple):
                ins = intakes[j] if j < len(intakes) else None
            elif intakes is not None:
                share = fb.count / total
                ins = dr.Intakes(
                    (intakes.primary[0] * share, intakes.primary[1] * share),
                    (intakes.secondary[0] * share, intakes.secondary[1] * share),
                    intakes.reference,
                )
            if self.inputs.one_per_chamber and fb.count == self.n > 1:
                self.notes.append(
                    f"{fb.count} fireboxes laid one to each chamber as the book draws them (the "
                    "owner's question 3), each its chamber's own trough, not side by side at the "
                    "front as the engine lays them"
                )
                out.append(self.trough(0))
            elif mine[0].trough:
                # Troughs sunk in the chambers' floors: the first chamber's is the front's fire;
                # a later chamber's burns in its stage, its air through that chamber's sides
                if any(b.chamber == 1 for b in mine):
                    out.append(self.trough(0))
            elif mine[0].kiln_side == "up":
                out.append(self.under(fb, len(mine), ins))
            else:
                out.append(self.wall(fb, mine, ins))
        return out

    def fire_zone(self, side: str) -> str:
        """A firebox's gas zone as `chamber._plan` names it: "firebox", or by its side when the
        fireboxes stand on more than one."""
        sides = {SIDES[b.kiln_side] for b in self.laid.boxes if not b.trough}
        return "firebox" if len(sides) <= 1 else f"firebox {side}"

    def intake_els(
        self, ins: dr.Intakes | None, fb: Any, n: int, design: tuple[float, float], zone: str
    ) -> list[Element]:
        """The fireboxes' air intakes: the dataset's (`Intakes`), else the design's ash-pit mouth
        and stoke hole (``design``: their areas, all n together), else left out and said."""
        g = fb.grate
        barred = g is not None and g.gap is not None and self.inputs.grate_bar is not None
        g_area = si(g.width, "m") * si(g.length, "m") * n if g is not None else 0.0
        k_g = None
        if barred:
            assert g is not None
            assert g.gap is not None
            assert self.inputs.grate_bar is not None
            k_g = dr.bar_grate(si(g.gap, "m"), self.inputs.grate_bar)
        elif g is not None:
            self.notes.append("the grate's loss left out: its bars' size isn't given")
        self.notes.append("the fuel bed's resistance: no source, left out")
        if ins is not None:
            self.notes.append(f"the air intakes: {ins.reference}")
            return [dr.intakes(ins, g_area, k_g, n)]
        below, above = design
        if below + above > 0:
            made = dr.Intakes((below, below), (above, above), "the design's")
            self.notes.append(
                "the air intakes: the design's ash-pit mouth and stoke hole, fully open (the "
                "dataset gives none)"
            )
            return [dr.intakes(made, g_area, k_g, n)]
        self.left.append(f"the air intakes of the {zone} (no size given)")
        return []

    def under(self, fb: Any, n: int, ins: dr.Intakes | None) -> _Feed:
        """Fireboxes under the floor: the ash-pit mouth (or the intakes), the grate, the firebox's
        column and run, the turn up into the inlet flues and through the floor (the fast-fire's,
        p.141), or the floor's holes the dataset gives, or none (left out, said)."""
        kiln = self.kiln
        zone = self.fire_zone("under")
        t_floor = _thickness(kiln, "floor")
        fw = si(fb.width, "m")
        fh = si(fb.height, "m") if fb.height is not None else fw
        pit = si(fb.ash_pit, "m") if fb.ash_pit is not None else fh
        els: list[Element] = []
        g = fb.grate
        barred = g is not None and g.gap is not None and self.inputs.grate_bar is not None
        g_area = si(g.width, "m") * si(g.length, "m") * n if g is not None else 0.0
        if ins is not None:
            k_g = None
            if barred:
                assert g is not None
                assert g.gap is not None
                assert self.inputs.grate_bar is not None
                k_g = dr.bar_grate(si(g.gap, "m"), self.inputs.grate_bar)
            els.append(dr.intakes(ins, g_area, k_g, n))
            self.notes.append(f"the air intakes: {ins.reference}")
        elif g is None:
            # Fired on its floor: its mouth, the stoke hole the design gives, else its open end
            if fb.stoke_hole is not None:
                sw, sh, srnd = _port(fb.stoke_hole)
                els.append(dr.inlet("the firebox's mouth (its stoke hole)", _area(sw, sh, srnd), n))
                self.notes.append("the air intakes: the design's firebox mouth, fully open")
            else:
                els.append(dr.inlet("the firebox's open end (its width by its height)", fw * fh,
                                    n))  # fmt: skip
                self.notes.append("the air intakes: the firebox's open end (no mouth given)")
        else:
            els.append(dr.inlet("ash-pit mouth (the firebox's width by the ash pit's depth)",
                                fw * pit, n))  # fmt: skip
            self.notes.append(
                "the air intakes: the design's ash-pit mouths alone (no others given)"
            )
            if barred:
                assert g is not None
                assert g.gap is not None
                assert self.inputs.grate_bar is not None
                els.append(dr.grate("grate, round bars (Idelchik 8-9)", si(g.width, "m"),
                                    si(g.length, "m"), si(g.gap, "m"), self.inputs.grate_bar,
                                    n))  # fmt: skip
        if g is not None and not barred:
            self.notes.append("the grate's loss left out: its bars' size isn't given")
        self.notes.append("the fuel bed's resistance: no source, left out")
        els.append(dr.column("firebox and inlet flue, grate to the chamber floor", zone,
                             t_floor + fh))  # fmt: skip
        run = si(g.length, "m") / 2 if g is not None else si(fb.length, "m") / 2
        els.append(dr.duct("firebox, the gas's run off the grate (half its length)", zone, fw, fh,
                           run, n))  # fmt: skip
        if fb.inlet is not None:
            iw, ih, rnd = _port(fb.inlet)
            ia = _area(iw, ih, rnd)
            k = n * fb.inlets
            share = fw / fb.inlets  # each inlet's share of the channel's width
            els.append(dr.turn("into the inlet flue, a sharp turn up", zone, share, fh, ia / share,
                               k))  # fmt: skip
            if abs(iw - share) > 1e-3:
                self.notes.append(
                    "an inlet flue narrower or wider than its share of the channel: 6-6 taken on "
                    "its area over that share (6-6 keeps the side normal to the turn)"
                )
            els.append(dr.duct("inlet flue, through the floor", zone, iw, ih, t_floor, k, rnd=rnd))
            els.append(dr.outlet("inlet flue into the chamber", zone, ia, k))
        else:
            holes = self.given_inlets()
            if holes is None:
                self.left.append("the floor's holes over the firebox (not sized)")
            else:
                count, w, h, rnd = holes
                a = _area(w, h, rnd)
                els.append(dr.contraction("into the floor's holes", zone, a,
                                          fw * si(fb.length, "m") * n / count, count))  # fmt: skip
                els.append(dr.duct("the floor's holes, through the floor", zone, w, h, t_floor,
                                   count, rnd=rnd))  # fmt: skip
                els.append(dr.outlet("the floor's holes into the chamber", zone, a, count))
        return _Feed("under the floor", els, 0, self.z_at(0.0, 0.0))

    def wall(self, fb: Any, boxes: list[Any], ins: dr.Intakes | None) -> _Feed:
        """Fireboxes against a wall (or on a diagonal, drawn against the front or back): the
        intakes in their mouth wall, the fire's column from the grate to the middle of their
        passage into the chamber, the run off the grate, the contraction into the inlet flues (or
        the whole mouth, as the engine cuts it), through the wall and out into the chamber."""
        joined = [b for b in boxes if self.laid.passage(b)]
        if joined and len(joined) < len(boxes) and fb.inlet is None and self.inputs.inlets is None:
            self.notes.append(
                f"{len(boxes) - len(joined)} of the {len(boxes)} fireboxes stand past the "
                "chamber's width as the engine lays them, with no way into it: left out"
            )
            boxes = joined
        b = boxes[0]
        n = len(boxes)
        side = SIDES[b.kiln_side]
        zone = self.fire_zone(side)
        holes = self.laid.holes
        tag = f"firebox-{b.index}"
        fw = si(fb.width, "m")
        fh, ash, _ = (x * MM for x in _grate_heights(fb))
        g = b.grate_z * MM
        # The design's openings in the mouth wall: the ash pit's open mouth below the grate and
        # the stoke hole above it
        below = fw * ash * n if fb.grate is not None else 0.0
        stoke = holes.get(f"{tag}/stoke-hole")
        above = 0.0
        if stoke is not None:
            sw, sh, srnd = _port(fb.stoke_hole)
            above = _area(sw, sh, srnd) * n
        els: list[Element] = []
        if b.gas:
            els += self.gas_ports_into(b, n)
        else:
            els += self.intake_els(ins, fb, n, (below, above), zone)
        face = {"front": "front", "back": "back", "left": "left", "right": "right"}[side]
        t_wall = _thickness(self.kiln, face)
        gi = self.given_inlets()
        if gi is not None:  # the dataset's, over the design's (whose count may be the default)
            k, iw, ih, rnd = gi
            k = max(1, round(k / n))
            z_mid = b.level * MM + ih / 2
            what = "inlet flues"
        elif fb.inlet is not None:
            iw, ih, rnd = _port(fb.inlet)
            k = fb.inlets
            z_mid = b.level * MM + ih / 2
            what = "inlet flues"
            given = self.kiln_inlet_note(b, fb)
            if given:
                self.notes.append(given)
        else:
            mouth = holes.get(f"{tag}/mouth")
            if mouth is not None:
                lo, hi = mouth.lo, mouth.hi
                axis = mouth.axis
                across = (hi[0] - lo[0]) if axis == 1 else (hi[1] - lo[1])
                iw, ih, rnd, k = across * MM, (hi[2] - lo[2]) * MM, False, 1
                z_mid = (lo[2] + hi[2]) / 2 * MM
                what = "mouth"
                self.notes.append(
                    f"the {zone}'s whole mouth into the chamber, as the engine cuts it "
                    f"({iw / IN:.1f} × {ih / IN:.1f} in): no inlet flues given"
                )
            else:
                raise NotModelledError(
                    f"the {zone} has no way into the chamber: the engine's layout leaves no mouth "
                    "(the firebox below the floor) and the design gives no inlet flues"
                )
        a = _area(iw, ih, rnd)
        h_sec = max(fh, z_mid + ih / 2 - g)  # the space reaches its passage
        if h_sec > fh + 1e-9:
            self.notes.append(
                f"the {zone}'s space taken as reaching its passage, {h_sec / IN:.1f} in above the "
                f"fire (the design's {fh / IN:.1f} in doesn't)"
            )
        g0 = fb.grate
        run = si(g0.length, "m") / 2 if g0 is not None else si(fb.length, "m") / 2
        # Where the fire and the passage stand: the fire over the grate's middle, the passage at
        # the chamber's inside face (a side firebox's along its middle)
        y_fire: float = (b.lo[1] + b.hi[1]) / 2 * MM
        faces = {"front": self.site.front * MM, "back": self.site.back * MM}
        y_pass = faces.get(side, y_fire)
        z_fire, z_pass = self.z_at(y_fire, g), self.z_at(y_pass, z_mid)
        els.append(dr.column(f"{zone}, the fire to its {what}' middle", zone, z_pass - z_fire))
        els.append(dr.duct(f"{zone}, the gas's run off the grate (half its length)", zone, fw,
                           h_sec, run, n))  # fmt: skip
        els.append(dr.contraction(f"into the {zone}'s {what}", zone, a, fw * h_sec / k, k * n))
        els.append(dr.duct(f"{zone}'s {what}, through the {face} wall", zone, iw, ih, t_wall,
                           k * n, rnd=rnd))  # fmt: skip
        els.append(dr.outlet(f"{zone}'s {what} into the chamber", zone, a, k * n))
        return _Feed(f"the {zone}", els, 0, z_pass)

    def kiln_inlet_note(self, b: Any, fb: Any) -> str:
        """Where the engine's layout merges a firebox's inlet flues into one slot (more than fit
        side by side), the path keeps the design's count and size: said."""
        from kilndesigner.firebox_parts import inlets_fit

        if inlets_fit(b):
            return ""
        return (
            f"{fb.inlets} inlet flues of the design's size, though the engine's layout cuts them "
            "as one slot (they don't fit side by side)"
        )

    def given_inlets(self, cap: float = math.inf) -> tuple[int, float, float, bool] | None:
        """Inlet flues the dataset gives (`Inputs.inlets`), what it leaves out by p.78, against
        the exits' or the chimney's area; None if not given."""
        f = self.inputs.inlets
        if f is None:
            return None
        return self.flues(f, "inlet flues", cap)

    def flues(self, f: Flues, what: str, cap: float = math.inf) -> tuple[int, float, float, bool]:
        """A set of flues from the dataset at this end of their bands, what it leaves out by p.78
        (the area of the path's anchor, `anchor`): the count with both sizes given, else the
        missing size over the count (one where it isn't given); ``cap`` the most a height may be
        (m), its firebox's."""
        if f.area is not None:
            count = f.count or 1
            side = math.sqrt(f.area.end(self.most) / count)
            self.notes.append(f"the {what}: {f.area.lo / IN**2:.0f}–{f.area.hi / IN**2:.0f} in² "
                              f"({f.source})")  # fmt: skip
            return count, side, side, False
        w = f.width.end(self.most) if f.width is not None else None
        h = f.height.end(self.most) if f.height is not None else None
        if w is not None and (f.round or h is not None) and f.count is not None:
            h = w if f.round or h is None else h
            size = f"{w / IN:.1f} in round" if f.round else f"{w / IN:.1f} × {h / IN:.1f} in"
            self.notes.append(f"the {what}: {f.count} × {size} ({f.source})")
            return f.count, w, h, f.round
        area, anchor = self.anchor(skip=what)
        rule = f"{P78} on {anchor}, {area / IN**2:.0f} in²"
        if w is not None and (f.round or h is not None):
            h = w if f.round or h is None else h
            count = max(1, round(area / _area(w, h, f.round)))
            self.notes.append(
                f"the {what}: {count} of {w / IN:.1f} × {h / IN:.1f} in ({f.source}), as many as "
                f"{rule} takes"
            )
            return count, w, h, f.round
        count = f.count or 1
        if w is None:
            assert h is not None
            w = area / count / h
            self.notes.append(f"the {what}: {count} × {h / IN:.1f} in tall ({f.source}), "
                              f"{w / IN:.1f} in wide by {rule}")  # fmt: skip
            return count, w, h, False
        h = min(area / count / w, cap)
        self.notes.append(f"the {what}: {count} × {w / IN:.1f} in wide ({f.source}), "
                          f"{h / IN:.1f} in tall by {rule}")  # fmt: skip
        return count, w, h, False

    def trough(self, k: int) -> _Feed:
        """A chamber's own trough (himae): the fire burns in the chamber's zone, its air through
        the chamber's side stoke holes (`side`)."""
        feed = self.side(k)
        self.notes.append(f"chamber {k + 1}'s fire in its trough, the chamber's own zone")
        return feed

    def side(self, k: int) -> _Feed:
        """Chamber k's side stoke holes (the design's `stoke_holes`), each an opening in its side
        wall at its height, all open; none given: left out and said."""
        holes = [h for h in (self.kiln.stoke_holes or []) if h.chamber == k + 1]
        if not holes:
            self.left.append(f"chamber {k + 1}'s side stoke holes (not sized)")
            return _Feed(f"chamber {k + 1}'s side", [], k, self.floor(k))
        groups: dict[tuple[float, float, bool, float, float], int] = {}
        for h in holes:
            w, ht, rnd = _port(h.port)
            up = si(h.up, "m") if h.up is not None else ht / 2
            key = (w, ht, rnd, up, _thickness(self.kiln, h.wall))
            groups[key] = groups.get(key, 0) + 1
        branches: list[list[Element]] = []
        for (w, ht, rnd, up, t), count in groups.items():
            a = _area(w, ht, rnd)
            name = f"{dr.INTAKE}, chamber {k + 1}'s side stoke holes"
            z = self.floor(k) + up
            branches.append([
                Element(name, "inlet", "room", a, count, k=dr.SHARP_ENTRANCE,
                        note=f"{count} × {w / IN:.1f} in{' round' if rnd else ''}, the design's"),
                dr.duct(f"chamber {k + 1}'s side stoke holes, through the wall", "room", w, ht, t,
                        count, rnd=rnd),
                dr.outlet(f"chamber {k + 1}'s side stoke holes into it", "room", a, count),
                column_to(self.zone(k), self.floor(k) - z),
            ])  # fmt: skip
        self.notes.append(f"chamber {k + 1}'s side stoke holes open (the design's), its intakes")
        return _Feed(f"chamber {k + 1}'s side", _group("the side stoke holes", branches), k,
                     self.floor(k))  # fmt: skip

    def burners(self) -> list[_Feed]:
        """Gas burners: room air round them through their ports (the venturi's own pumping isn't
        modelled), in a wall at their height, at given places, or up through the floor."""
        from kilndesigner.firebox_parts import burner_port_in

        g = self.kiln.heat.gas
        assert g is not None
        boxes = [b for b in self.laid.boxes if b.gas]
        if boxes:
            return [self.wall(boxes[0].box, boxes, None)]
        size = burner_port_in(self.kiln)
        count = g.burners.wanted
        if size is None or count is None:
            raise NotModelledError("the burners' port size or count isn't given")
        pw, ph, rnd = size[0] * IN, size[1] * IN, size[2]
        pa = _area(pw, ph, rnd)
        self.notes.append(
            "all the air taken as drawn through the burner ports by the draft: the venturi's own "
            "pumping isn't modelled (no source), and the burner tube in the port is ignored"
        )
        b = g.burners
        if b.wall == "floor" and b.places is None:
            t = _thickness(self.kiln, "floor")
            els = [
                dr.inlet("burner ports, room air round the burners", pa, count),
                dr.duct("burner ports, up through the floor", "room", pw, ph, t, count, rnd=rnd),
                dr.outlet("burner ports into the chamber", "room", pa, count),
            ]
            return [_Feed("the burner ports in the floor", els, 0, 0.0)]
        spots: dict[tuple[float, float], int] = {}
        if b.places is not None:
            for p in b.places:
                key = (_thickness(self.kiln, p.wall), si(p.up, "m"))
                spots[key] = spots.get(key, 0) + 1
        else:
            up = si(b.up, "m") if b.up is not None else 0.0635 + ph / 2  # a 2½ in course up
            for wall, share in zip(b.spread_over, b.shares(count), strict=True):
                key = (_thickness(self.kiln, wall), up)
                spots[key] = spots.get(key, 0) + share
        out: list[_Feed] = []
        for (t, up), c in spots.items():
            els = [
                dr.inlet("burner ports, room air round the burners", pa, c),
                dr.duct("burner ports, through the wall", "room", pw, ph, t, c, rnd=rnd),
                dr.outlet("burner ports into the chamber", "room", pa, c),
            ]
            out.append(_Feed("the burner ports", els, 0, up))
        return out

    def gas_ports_into(self, b: Any, n: int) -> list[Element]:
        """Burners firing into their own firebox (Bowen's): room air round them through its mouth
        wall's ports."""
        from kilndesigner.firebox_parts import _layers, burner_port_in  # pyright: ignore[reportPrivateUsage]

        ports = [o for o in self.laid.all_holes if o.name.startswith(f"firebox-{b.index}/burner")]
        size = burner_port_in(self.kiln)
        if not ports or size is None:
            raise NotModelledError("the gas firebox's burner ports aren't laid out (their size)")
        pw, ph, rnd = size[0] * IN, size[1] * IN, size[2]
        pa = _area(pw, ph, rnd)
        t = sum(th for _, th in _layers(self.kiln, b.box)[0]) * MM
        c = len(ports)
        self.notes.append(
            "the burners fire into their firebox through its mouth wall: all the air taken as "
            "drawn through their ports by the draft (the venturi's pumping isn't modelled)"
        )
        return [
            dr.inlet("burner ports, room air round the burners", pa, c),
            dr.duct("burner ports, through the firebox's mouth wall", "room", pw, ph, t, c,
                    rnd=rnd),
            dr.outlet("burner ports into the firebox", "room", pa, c),
        ]  # fmt: skip

    # --- between the nodes -------------------------------------------------------------------

    def passage(self, k: int) -> list[Element]:
        """From node k into node k + 1: a row's flue holes through the wall between (8-4), or a
        segment's cut at the tube's mid-height."""
        zone, nxt = self.zone(k), self.zone(k + 1)
        if self.run is None:
            y = (k + 1) * self.depth / self.nodes
            z_cut = self.z_at(y - self.depth / 2, (self.height + self.rise) / 2)
            self.notes.append(MID_HEIGHT)
            return [column_to(zone, z_cut - self.floor(k)),
                    column_to(nxt, self.floor(k + 1) - z_cut)]  # fmt: skip
        from kilndesigner.run_parts import flue_rows

        row = next((r for r in flue_rows(self.kiln) if r.chamber == k + 1), None)
        f = self.inputs.between
        if f is not None:
            count, w, h, _ = self.flues(f, "flues between the chambers")
            bottom = float(self.run.floor(k + 1)) * MM
            top = bottom + h
        elif row is not None:
            count, w = row.count, row.width * MM
            bottom, top = row.bottom * MM, row.top * MM
            h = top - bottom
            given = self.kiln.draft is not None and self.kiln.draft.between is not None
            if not given:
                self.notes.append(
                    "the flues between the chambers Olsen's standard 4½ × 9 in, 9 in apart, as "
                    "many as fit (p.96, p.45), as the engine lays them: the design gives none"
                )
        else:
            raise NotModelledError(f"no flues through the wall after chamber {k + 1}")
        z = (bottom + top) / 2
        approach = self.width * float(self.run.height_of(k)) * MM
        jet, rub = dr.gaps(f"the flues from chamber {k + 1} into chamber {k + 2} (Idelchik 8-4)",
                           zone, count, w, h, float(self.run.between) * MM, approach)  # fmt: skip
        return [column_to(zone, z - self.floor(k)), jet, rub, column_to(nxt, self.floor(k + 1) - z)]

    # --- the way out -------------------------------------------------------------------------

    def leave(self) -> list[Element]:
        """From the last node: its exit flues and the chimney, or straight to the room (an
        updraft, whose chamber is its stack)."""
        last = self.nodes - 1
        exits = self.exits()
        stack = self.stack_given()
        if stack is None:
            zone = self.zone(last)
            branches = [
                [*self.out_of(e, last), dr.outlet(f"{e.name} into the room", zone, e.area, e.count)]
                for e in exits
            ]
            if self.inputs.stackless:
                self.notes.append(
                    "no stack (the dataset's): the last chamber's exits open to the room through "
                    "its roof, at its crown (an assumption: where they are isn't printed)"
                )
            else:
                self.notes.append(
                    "an updraft: its chamber is its stack, its exits open to the room (Olsen p.80: "
                    "updraft kilns have no chimneys)"
                )
            return _group("the exit flues, side by side", branches)
        return self.chimney(exits, stack, last)

    def out_of(self, e: _Exit, k: int) -> list[Element]:
        """A set of exit flues from node k's floor: the chamber's column up (or down) to them, the
        sharp entrance, the passage through their face (a floor's or roof's a column too)."""
        zone = self.zone(k)
        name = (
            f"{zone}, inlet to the exit flue's middle"  # the one flue first built, as it was named
            if e.name == "exit flue"
            else f"{zone}, inlet to {e.name}"
        )
        els = [dr.column(name, zone, e.z - self.floor(k))]
        if e.through == "top":
            return els
        els.append(dr.entrance(f"{e.name}, sharp entrance", zone, e.area, e.count))
        where = {"floor": "the floor", "roof": "the roof"}.get(e.through, "the flue wall")
        els.append(dr.duct(f"{e.name}, through {where}", zone, e.w, e.h, e.thick, e.count,
                           rnd=e.rnd))  # fmt: skip
        if e.through in ("floor", "roof"):
            els.append(column_to(zone, -e.thick if e.through == "floor" else e.thick))
        return els

    def exits(self) -> list[_Exit]:
        """The exit flues: the design's flue port or sets of exits, the dataset's, an open top,
        or p.78's area as one opening."""
        kiln = self.kiln
        d = kiln.draft
        last = self.nodes - 1
        wall = d.flue_wall if d is not None else "back"
        if isinstance(kiln.roof, OpenTop):
            if self.inputs.exits is not None:  # past what stands in it (Kenzan's muffle)
                count, w, h, _ = self.flues(self.inputs.exits, "open top's way out")
                side = math.sqrt(count * w * h)
            else:
                a = (math.pi * self.width**2 / 4 if kiln.chamber.shape == "round"
                     else self.width * self.depth)  # fmt: skip
                side = math.sqrt(a)
                self.notes.append("the open top the exit, its area the chamber's plan; what "
                                  "covers the setting there has no source: left out")  # fmt: skip
                self.left.append("whatever covers the open top's setting (not sized)")
            return [_Exit("the open top", 1, side, side, False, "top",
                          self.top_z(last), 0.0)]  # fmt: skip
        if d is not None and d.flue_port is not None:
            w, h, rnd = _port(d.flue_port)
            if self.updraft:
                z = self.roof_z(0.0, 0.0, last)
                return [_Exit("exit flue", 1, w, h, rnd, "roof", z, _thickness(kiln, "roof"))]
            z = self.wall_z(wall, h / 2, last)
            return [_Exit("exit flue", 1, w, h, rnd, wall, z, _thickness(kiln, wall))]
        if d is not None and d.exits is not None:
            return [self.exit_set(s, h, last) for s, h in enumerate(d.exits, 1)]
        f = self.inputs.exits
        up = self.updraft or self.inputs.stackless  # out through the roof, at its crown
        through = "roof" if up else wall
        face = _thickness(kiln, "roof" if up else wall)
        if f is not None:
            count, w, h, rnd = self.flues(f, "exit flues")
            z = self.roof_z(0.0, 0.0, last) if up else self.wall_z(wall, h / 2, last)
            return [_Exit("exit flues", count, w, h, rnd, through, z, face)]
        area, anchor = self.anchor(skip="exit flues")
        side = math.sqrt(area)
        rule = P78_GAS if self.kiln.heat.gas is not None else P78
        if self.updraft and self.kiln.heat.gas is not None:
            band = self.updraft_band(area)
            side = math.sqrt(band.end(self.most))
            self.notes.append(f"the exit flue in the crown, square, {band.lo / IN**2:.0f}–"
                              f"{band.hi / IN**2:.0f} in² ({band.source})")  # fmt: skip
        else:
            self.notes.append(f"the exit flue: {area / IN**2:.0f} in², square, by {rule} on "
                              f"{anchor}: the design gives none")  # fmt: skip
        z = self.roof_z(0.0, 0.0, last) if up else self.wall_z(wall, side / 2, last)
        return [_Exit("exit flue", 1, side, side, False, through, z, face)]

    def updraft_band(self, inlet: float) -> Band:
        """A gas updraft's exit in its crown: p.78's inlet = exit to the kits' 20 % more (pp.173–
        174), the two the band's ends: whether "about 40 ft³" is the stacking space or the
        chamber isn't said, and the reference updrafts straddle it either way."""
        return Band(inlet, 1.2 * inlet, f"{P78_GAS} to {P174}")

    def exit_set(self, s: int, h: Any, k: int) -> _Exit:
        """A set of the design's exit flues (`draft.exits`), where the engine cuts them: its
        holes' middles' mean height (they share one, but for holes over a curved roof)."""
        from kilndesigner.openings import grid_places, wall_places

        w, ht, rnd = _port(h.port)
        name = f"exit flues {s}" if len(self.kiln.draft.exits or []) > 1 else "exit flues"  # pyright: ignore[reportOptionalMemberAccess]
        if h.through in ("floor", "roof"):
            span, deep = self.width, self.depth
            if self.kiln.chamber.shape == "round":
                span = deep = self.width / math.sqrt(2)
            places = grid_places(h, span / IN, deep / IN)
            if h.through == "floor":
                along = sum(self.depth / 2 - y * IN for _, y in places) / len(places)
                return _Exit(name, h.wanted, w, ht, rnd, "floor", self.floor(k),
                             _thickness(self.kiln, "floor"), along)  # fmt: skip
            zs = [self.roof_z(x * IN, y * IN, k) for x, y in places]
            if max(zs) - min(zs) > 0.01:
                self.notes.append(f"{name}: over the curved roof, at their mean height")
            return _Exit(name, h.wanted, w, ht, rnd, "roof", sum(zs) / len(zs),
                         _thickness(self.kiln, "roof"))  # fmt: skip
        inside = (self.depth if h.through in ("left", "right") else self.width) / IN
        ups = [up * IN for _, up in wall_places(h, inside)]
        z = self.wall_z(h.through, sum(ups) / len(ups), k)
        return _Exit(name, h.wanted, w, ht, rnd, h.through, z, _thickness(self.kiln, h.through))

    def wall_z(self, wall: str, up: float, k: int) -> float:
        """A point ``up`` above node k's floor in a wall: the back's at the run's end on a slope."""
        if self.run is not None:
            return self.floor(k) + up
        y = {"back": self.depth / 2, "front": -self.depth / 2}.get(wall, 0.0)
        return self.z_at(y, up)

    def top_z(self, k: int) -> float:
        return self.floor(k) + self.height

    def roof_z(self, x: float, y: float, k: int) -> float:
        """The roof's inside height over (x, y) (m, from the chamber's middle): the springline,
        and an arch's, a dome's or a catenary's rise over it there."""
        from kilndesigner.model import arches_along
        from kilndesigner.shape import Arch, CatenaryCurve, RoundDome, SailDome

        roof = self.kiln.roof
        h = self.height
        if isinstance(roof, CatenaryArch):
            return self.floor(k) + CatenaryCurve(self.width, h).z(x)
        if isinstance(roof, SprungArch):
            along = arches_along(self.kiln)
            arch = Arch(self.depth if along else self.width, si(roof.rise, "m"))
            u = y if along else x
            return self.floor(k) + h + arch.height(min(abs(u), arch.span / 2))
        if isinstance(roof, Dome):
            r = si(roof.rise, "m")
            if self.kiln.chamber.shape == "round":
                d = RoundDome(self.width, r)
                rho = min(math.hypot(x, y), self.width / 2)
                return self.floor(k) + h + r - d.radius + math.sqrt(d.radius**2 - rho**2)
            s = SailDome(self.width, self.depth, r)
            return self.floor(k) + h + s.centre + math.sqrt(max(s.radius**2 - x * x - y * y, 0.0))
        assert isinstance(roof, FlatRoof | OpenTop)
        return self.floor(k) + h

    def anchor(self, skip: str = "") -> tuple[float, str]:
        """The area p.78's rule carries along the path (m²) and what it is: the exit flues given,
        the chimney's section given, the inlet flues, the flues between chambers, the burners' or
        drip ports; refused if the path gives none."""
        kiln = self.kiln
        d = kiln.draft
        if skip != "exit flues" and d is not None:
            area = d.exit_area_in2()
            if area is not None:
                return area * IN**2, "the exit flues"
        st = self.inputs.stack
        if st is not None and st.width is not None and (st.depth is not None or st.round):
            w = st.width.end(self.most)
            a = math.pi * w * w / 4 if st.round else w * st.depth.end(self.most)  # pyright: ignore[reportOptionalMemberAccess]
            return a, "the chimney's section (the dataset's)"
        if d is not None and d.chimney is not None and d.chimney.inside is not None:
            return d.chimney.inside.area_in2() * IN**2, "the chimney's section"
        fire = kiln.heat.fire
        if fire is not None:
            total = sum(fb.count * fb.inlets * _area(*_port(fb.inlet))
                        for fb in fire.fireboxes if fb.inlet is not None)  # fmt: skip
            if total > 0 and skip != "inlet flues":
                return total, "the inlet flues"
            if fire.fuel == "oil" and isinstance(self.inputs.intake, dr.Intakes):
                ins = self.inputs.intake
                return ins.primary[1] + ins.secondary[1], "the drip ports (the oil's inlets)"
        from kilndesigner.firebox_parts import burner_port_in
        from kilndesigner.run_parts import flue_rows

        rows = flue_rows(kiln) if self.n > 1 else []
        if rows and skip != "flues between the chambers":
            r = rows[0]
            return r.count * r.width * (r.top - r.bottom) * MM**2, "the flues between chambers"
        g = kiln.heat.gas
        size = burner_port_in(kiln) if g is not None else None
        if g is not None and size is not None and g.burners.wanted is not None:
            return g.burners.wanted * _area(size[0] * IN, size[1] * IN, size[2]), "the burner ports"
        if self.inputs.rule6:
            return self.rule6()
        need = f"the {skip}" if skip else "the chimney's section"
        raise NotModelledError(
            f"{need}: not given, and p.78's rule (inlet = exit = chimney section) has nothing to "
            "size them by: no inlet, exit or between flues, burner ports or chimney section is "
            "given in the design or the dataset"
        )

    def rule6(self) -> tuple[float, str]:
        """Olsen's Rule 6 (pp.79–80) as p.78's anchor: the chimney's side ⅕ of the chamber's
        width at the band's least-air end, ¼ at its most, neither under 9 in ("seldom under 9 x
        9in"); its area the kiln's whole chimney section, shared among its chimneys. Said, with
        the owner's question it rests on."""
        lo, hi = max(self.width / 5, MIN_CHIMNEY), max(self.width / 4, MIN_CHIMNEY)
        side = hi if self.most else lo
        self.notes.append(
            f"the chimney's section by {RULE_6} on the chamber's {self.width / IN:.0f} in width, "
            f"{lo / IN:.1f}–{hi / IN:.1f} in square: it {RULE_6_NOTE}"
        )
        return side * side, f"Rule 6's chimney section ({RULE_6})"

    # --- the chimney -------------------------------------------------------------------------

    def stack_given(self) -> dict[str, Any] | None:
        """The chimney: the dataset's (`Inputs.stack`) over the design's, each size at this end
        of its band; its section by p.78 and its height by the book's rules where neither gives
        one; None for an updraft without one."""
        d = self.kiln.draft
        st = self.inputs.stack
        built = d.chimney if d is not None else None
        if self.inputs.stackless or (built is None and st is None and self.updraft):
            return None
        spec: dict[str, Any] = {"count": d.chimneys if d is not None else 1, "top": None}
        if st is not None and st.count is not None:
            spec["count"] = st.count
        # the height, from the first chamber's floor
        if st is not None and st.height is not None:
            spec["height"] = st.height.end(self.most)
            lo, hi = st.height.lo / 0.3048, st.height.hi / 0.3048
            self.notes.append(f"the chimney {lo:.1f}–{hi:.1f} ft tall ({st.height.source})")
        elif built is not None:
            spec["height"] = si(built.height, "m")
        else:
            band = self.height_band()
            spec["height"] = band.end(self.most)
            self.notes.append(
                f"the chimney's height: none given, the band {band.lo / 0.3048:.1f}–"
                f"{band.hi / 0.3048:.1f} ft from {band.source}"
            )
        # the section
        if st is not None and st.width is not None and (st.depth is not None or st.round):
            w = st.width.end(self.most)
            spec["round"] = st.round
            spec["w"], spec["d"] = (w, w) if st.round else (w, st.depth.end(self.most))  # pyright: ignore[reportOptionalMemberAccess]
            spec["top"] = st.top
            self.notes.append(f"the chimney's section the dataset's ({st.source})")
        elif built is not None and built.inside is not None:
            ins = built.inside
            if ins.diameter is not None:
                spec["round"], spec["w"] = True, si(ins.diameter, "m")
                spec["d"] = spec["w"]
            else:
                assert ins.width is not None
                assert ins.depth is not None
                spec["round"], spec["w"], spec["d"] = False, si(ins.width, "m"), si(ins.depth, "m")
            if built.top is not None:
                t = built.top
                spec["top"] = (
                    (si(t.diameter, "m"),) * 2 if t.diameter is not None
                    else (si(t.width, "m"), si(t.depth, "m"))  # pyright: ignore[reportArgumentType]
                )  # fmt: skip
        else:
            area, anchor = self.anchor()
            each = area / spec["count"]
            if st is not None and st.round:
                dia = math.sqrt(4 * each / math.pi)
                spec["round"], spec["w"], spec["d"] = True, dia, dia
                shape = f"round ({st.source})"
            else:
                side = math.sqrt(each)
                spec["round"], spec["w"], spec["d"] = False, side, side
                shape = "square (its shape not given)"
            self.notes.append(f"the chimney's section {area / IN**2:.0f} in², {shape}, by {P78} "
                              f"on {anchor}: none given")  # fmt: skip
        return spec

    def height_band(self) -> Band:
        """A chimney's height no source gives, from the book's rules (v1's `fire.pull` holds the
        same): a climbing kiln's least the line through its chamber tops (p.81), its most 3 × its
        total rise (p.101); else the least twice the downward pull (p.130, Fig 5-2), the most Rule
        5, 3 × the downward pull + ⅓ × the horizontal pull (p.80). From the first chamber's
        floor."""
        kiln = self.kiln
        d = kiln.draft
        down = self.height + self.rise
        wall = d.flue_wall if d is not None else "back"
        length = float(self.run.length) * MM if self.run is not None else self.depth
        along = length if wall in ("front", "back") else self.width
        t_wall = _thickness(kiln, wall)
        run = si(d.run_to_chimney, "m") if d is not None else 0.0
        rise = math.tan(self.slope) * (length + t_wall + run)
        if rise > 0:
            least = rise + down
            return Band(least, max(3 * rise, least), CLIMBING_RULES)
        fire = kiln.heat.fire
        under = [si(fb.height, "m") + (si(fb.ash_pit, "m") if fb.ash_pit is not None else 0.0)
                 for fb in (fire.fireboxes if fire else []) if fb.position == "under"
                 and fb.height is not None]  # fmt: skip
        if under:
            down += max(under)
        across = along + t_wall + run
        return Band(2 * down, max(3 * down + across / 3, 2 * down), HEIGHT_RULES)

    def chimney(self, exits: list[_Exit], spec: dict[str, Any], k: int) -> list[Element]:
        """The exits into the chimney beside the kiln (or through its crown), the chimney's
        column, its friction and its top; floor exits through the channels under the floor."""
        kiln = self.kiln
        d = kiln.draft
        zone = self.stack_zone
        n = int(spec["count"])
        cw, cd, rnd = float(spec["w"]), float(spec["d"]), bool(spec["round"])
        side = math.sqrt(math.pi / 4)
        ca = _area(cw, cd, rnd)
        top = float(spec["height"])
        run = si(d.run_to_chimney, "m") if d is not None else 0.0
        conn = self.connection()
        branches: list[list[Element]] = []
        bases: list[float] = []
        for e in exits:
            els = self.out_of(e, k)
            if e.through == "top":
                raise NotModelledError("an open top under a chimney isn't a kiln the book draws")
            if self.updraft and e.through == "roof":
                # Into a chimney over the crown (Breda's bottle): the gas goes on up
                els.append(dr.expansion(f"{e.name} into the chimney", zone, e.area,
                                        ca * n / e.count, e.count))  # fmt: skip
                base = e.z + e.thick
            elif e.through == "floor":
                els.append(dr.outlet(f"{e.name} into the channels under the floor", zone, e.area,
                                     e.count))  # fmt: skip
                base = self.floor(k) - e.thick
                wall = d.flue_wall if d is not None else "back"
                t_wall = _thickness(kiln, wall)
                if conn is not None:
                    w, h = conn
                    els.append(dr.duct("the channels and connection to the chimney", zone, w, h,
                                       e.along + t_wall + run))  # fmt: skip
                    els.append(dr.turn_up("turn up into the chimney", zone, w, h,
                                          cd * (side if rnd else 1), w * h, ca * n))  # fmt: skip
                    base -= h / 2
                else:
                    self.left.append("the channels under the floor (not sized)")
            else:
                if conn is not None:
                    w, h = conn
                    els.append(dr.expansion(f"{e.name} into the connection", zone, e.area,
                                            w * h / e.count, e.count))  # fmt: skip
                    if run > 0:
                        els.append(dr.duct("the connection to the chimney", zone, w, h, run))
                    els.append(dr.turn_up("turn up into the chimney", zone, w, h,
                                          cd * (side if rnd else 1), w * h, ca * n))  # fmt: skip
                else:
                    if run > 0:
                        els.append(dr.duct("the run to the chimney", zone, e.w, e.h, run, e.count,
                                           rnd=e.rnd))  # fmt: skip
                    fa, fb0 = (e.w * side, e.h * side) if e.rnd else (e.w, e.h)
                    els.append(dr.turn_up("turn up into the chimney", zone, fa, fb0,
                                          cd * (side if rnd else 1), e.area, ca * n / e.count,
                                          e.count))  # fmt: skip
                base = e.z
            bases.append(base)
            branches.append(els)
        if d is not None and d.chimney_through == "crown":
            self.notes.append("the chimney through the crown: its flue taken from the exits' "
                              "level straight up to its top, at the chimney's section")  # fmt: skip
        base = min(bases)  # each set's gas brought to the chimney's foot, then up it together
        for els, b in zip(branches, bases, strict=True):
            els.append(column_to(zone, base - b))
        out = _group("the exit flues, side by side", branches)
        out.append(dr.column("chimney", zone, top - base))
        out += self.stack_friction(zone, cw, cd, rnd, spec["top"], top - base, base, n)
        ta = _area(*spec["top"], rnd) if spec["top"] is not None else ca  # pyright: ignore[reportCallIssue]
        out.append(dr.outlet("chimney top", zone, ta, n))
        if n > 1:
            self.notes.append(f"{n} chimneys side by side, the flow shared evenly")
        return out

    def stack_friction(
        self,
        zone: str,
        cw: float,
        cd: float,
        rnd: bool,
        top: tuple[float, float] | None,
        tall: float,
        base: float,
        n: int,
    ) -> list[Element]:
        """The chimney's friction: straight, or straight to the kiln's top and tapering from there
        to its top's section in slices (p.80); the taper's own contraction left out (a gradual
        one, said)."""
        if top is None:
            return [dr.duct("chimney", zone, cw, cd, tall, n, rnd=rnd)]
        from kilndesigner.gas import kiln_top_in

        start = min(max(kiln_top_in(self.kiln) * IN - base, 0.0), tall)
        els = [dr.duct("chimney, straight to the kiln's top", zone, cw, cd, start, n, rnd=rnd)]
        rest = tall - start
        for i in range(TAPER_STEPS):
            f = (i + 0.5) / TAPER_STEPS
            w = cw + (top[0] - cw) * f
            dd = cd + (top[1] - cd) * f
            els.append(dr.duct(f"chimney, tapering ({i + 1} of {TAPER_STEPS})", zone, w, dd,
                               rest / TAPER_STEPS, n, rnd=rnd))  # fmt: skip
        self.notes.append(
            f"the chimney tapering from the kiln's top to its top ({P80}): its friction in "
            "slices, the gradual contraction's own loss left out"
        )
        return els

    def connection(self) -> tuple[float, float] | None:
        """The flue from the kiln into the chimney: the dataset's, else the design's, as a
        rectangle (a round one as the square of its area)."""
        given = self.inputs.connection
        if given is not None:
            return given[0].end(self.most), given[1].end(self.most)
        d = self.kiln.draft
        if d is None or d.connection is None:
            return None
        w, h, rnd = _port(d.connection)
        if rnd:
            s = math.sqrt(math.pi / 4) * w
            return s, s
        return w, h


def column_to(zone: str, rise: float) -> Element:
    return dr.column(f"{zone}, its climb", zone, rise)


def _grate_heights(fb: Any) -> tuple[float, float, float]:
    from kilndesigner.firebox_parts import grate_heights

    return grate_heights(fb)


def _flatten(els: Sequence[Element]) -> Any:
    for e in els:
        if e.kind == "parallel":
            for b in e.parts:
                yield from _flatten(b)
        else:
            yield e


def _describe(els: Sequence[Element]) -> str:
    out: list[str] = []
    for e in els:
        if e.kind == "column":
            continue
        if e.kind == "parallel":
            out.append("[" + " | ".join(_describe(b) for b in e.parts) + "]")
        else:
            out.append(e.name)
    return " → ".join(out)
