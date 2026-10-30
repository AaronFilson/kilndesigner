"""Masonry for a round chamber: its wall as rings of tapered brick, its floor and flat roof as
discs of straights cut to the circle, its dome counted by volume.

- The wall, ring by ring from the inside out (rings.py): a 9 in ring of key bricks laid flat in
  2½ in courses (Olsen, p.45); a 4½ in ring as the design's ``chamber.rings`` says, straights
  with mortar-filled wedge joints, straights cut to the angle, straights with featheredges, or
  arch bricks (rings.py). Each course is the same ring; the
  top course is ripped to the wall's height. A wall that isn't whole 9 and 4½ in rings is
  reported, as a straight wall that isn't whole bricks is.
- The floor runs under the whole kiln, out to the wall's outside, as the box kiln's does; a flat
  roof sits on the wall. Each is laid in rows of straights, as a box kiln's floor is (masonry.py),
  the rows' ends cut to the circle.
- A dome over a round chamber is a sphere through the springline circle (shape.RoundDome); its
  layers are counted by volume, as the box kiln's dome is: no standard shape turns a dome.

Coordinates in mm; the chamber's axis is z.
"""

from __future__ import annotations

import math
from collections import Counter, defaultdict
from dataclasses import dataclass, replace

from kilndesigner.castable import resolve_material
from kilndesigner.firebox_parts import firebox_findings
from kilndesigner.geometry import Part, lining_parts
from kilndesigner.library import material
from kilndesigner.masonry import (
    BRICK_KINDS,
    BRICK_SOURCE,
    BRICK_VOLUME,
    BULK_KINDS,
    SHEET_KINDS,
    TOL,
    Course,
    Cut,
    LayerPlan,
    Masonry,
    MasonryPlan,
    _not_buildable,  # pyright: ignore[reportPrivateUsage]
    brick_sizes,
    buildable_near,
    buy_quantities,
    layings,
    plan_layers,
    port_findings,
    run_pieces,
)
from kilndesigner.materials_checks import SUMS, whole_bricks
from kilndesigner.model import Dome, FlatRoof, Kiln
from kilndesigner.rings import (
    CUT_SLACK,
    FAMILIES,
    FEATHEREDGE_SOURCE,
    IN,
    MORTAR_SOURCE,
    SOURCE,
    Ring,
    RingError,
    Series,
    cut_bricks,
    cut_diameter,
    ring,
    ring_method,
    ring_series,
    wall_rings,
)
from kilndesigner.shape import RoundDome
from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_, si
from kilndesigner.working import Finding, length_text

RINGS = "whole 9 and 4½ in rings: a·9 + b·4½ in (Olsen, The Kiln Book, 4th ed., p.45)"

RING_WORDS: dict[str, str] = {
    "key": "key bricks laid flat, 9 in through the wall, in 2½ in courses",
    "arch": (
        "arch bricks standing on end, 4½ in through the wall, in 9 in courses (possible but not "
        "recommended, Olsen p.45)"
    ),
    "featheredge": (
        "straights standing on end with featheredges among them, 4½ in through the wall, in "
        "9 in courses"
    ),
    "mortar": (
        "straights laid flat, 4½ in through the wall, in 2½ in courses, their inside faces on the "
        "curve and the wedge-shaped joints behind filled with mortar (Olsen p.45, Fig. 2-13)"
    ),
    "cut": (
        "straights laid flat, 4½ in through the wall, in 2½ in courses, each cut at both ends to "
        "the angle so the ring closes tight"
    ),
    "cut2.5": (
        "2½ in straights on their 4½ in face, 2½ in through the wall, in 4½ in courses, each cut "
        "at both ends to the angle so the ring closes tight, as electric kilns are built"
    ),
    "cut3": (
        "3 in straights on their 4½ in face, 3 in through the wall, in 4½ in courses, each cut "
        "at both ends to the angle so the ring closes tight, as electric kilns are built"
    ),
}


@dataclass
class RingPlan:
    """One ring of a round wall, the same in every course: which shapes, how many, in order."""

    part: Part  # the wall's layer it's in
    within: tuple[int, int]  # this ring, of how many in the layer, from the inside
    inside_radius: float  # mm
    depth: float  # mm, through the wall
    series: Series
    ring: Ring
    courses: int
    course_height: float  # mm
    top: float  # mm, the top course's height; less than course_height when ripped

    @property
    def ripped(self) -> bool:
        return abs(self.top - self.course_height) >= TOL

    def title(self) -> str:
        title = f"{self.part.title}: {material(self.part.material).name}"
        k, n = self.within
        if n > 1:
            title += f", ring {k} of {n} from the inside"
        return title

    def description(self, us: bool) -> str:
        text = (
            f"{self.courses} courses of {RING_WORDS[self.series]}, each course "
            f"{self.ring.describe()} round a circle {length_text(2 * self.inside_radius, us)} "
            "across inside"
        )
        text += straight_ring_text(self.ring, us)
        if self.ripped:
            text += f"; the top course ripped to {length_text(self.top, us)}"
        return text + "."

    def order(self) -> list[str]:
        """The shapes round the ring, each spread evenly among the others."""
        keyed = [((j + 0.5) / n, name) for name, n in self.ring.counts for j in range(n)]
        return [name for _, name in sorted(keyed)]


def straight_ring_text(r: Ring, us: bool) -> str:
    """What a ring of straights needs beyond its count: the closer, the joints, the cuts."""
    out = ""
    if r.series == "mortar":
        if r.length is not None:
            out += f", the closer cut to {length_text(r.length, us)}"
        assert r.joint is not None
        assert r.mortar is not None
        per_ft = r.mortar * 12 * IN / IN**3  # in³ for each foot of wall height
        out += (
            f"; the joints open to {length_text(r.joint, us)} at the outside, about "
            f"{per_ft:.0f} in³ of mortar in them for each foot of wall height (no source sets a "
            "widest joint)"
        )
    elif r.series in ("cut", "cut2.5", "cut3"):
        assert r.angle is not None
        out += f", each cut at both ends {r.angle:.1f}° off square, its 9 in outside face whole"
        if r.length is not None:
            out += f"; the closer cut to {length_text(r.length, us)} along its outside face"
    return out


def cut_ring_sheet(inside_diameter: float, depth: float) -> Sheet:
    """Whether full 9 in straights cut to the angle turn this ring exactly (mm in): the ring of
    the nearest whole number of bricks that has this inside diameter (the mean of its flats and
    corners, as makers quote it), and how far its faces miss 9 in, all round."""
    whole = max(round(cut_bricks(inside_diameter, depth)), 3)
    s = Sheet("masonry.cut-ring", "Full bricks turn the ring", reference=FEATHEREDGE_SOURCE)
    s.given("D", "inside diameter, the mean of flats and corners",
            Q_(inside_diameter, "mm").to("in"), "in", source="the design: the chamber")  # fmt: skip
    s.given("t", "the wall, through", Q_(depth, "mm").to("in"), "in", source="the walls' layers")
    s.given("L", "a straight's outside face", Q_(9, "in"), "in", source="a 9 in straight")
    s.given("N", "the nearest whole number of bricks round", float(whole),
            source="solved from D, rounded")  # fmt: skip
    s.let("a_i", "inside apothem", "D/(1 + 1/cos(pi/N))", "in")
    s.let("F", "each brick's outside face, for this D", "2*(a_i + t)*tan(pi/N)", "in")
    s.let("g", "the ring's miss round the outside", "N*abs(F - L)", "in")
    s.given("g_max", "near enough", Q_(CUT_SLACK, "in"), "in",
            source="the user, a kiln builder: 1/16 in, dry-laid; mortared joints take "
            "more")  # fmt: skip
    s.require("g", "<=", "g_max", level="warning")
    s.lever("D", Q_(cut_diameter(max(whole - 1, 3), depth), "mm").to("in"),
            Q_(cut_diameter(whole + 1, depth), "mm").to("in"))  # fmt: skip
    return s


def _disc_rows(radius: float, thickness: float, part: Part) -> list[LayerPlan] | None:
    """A disc of brick ``thickness`` thick, laid in rows of straights across it, the rows' ends
    cut to the circle: one plan for each wall of brick in the layer, from the inside out. None if
    whole bricks don't make the thickness."""
    sizes = brick_sizes(thickness)
    if sizes is None:
        return None
    plans: list[LayerPlan] = []
    for k, size in enumerate(sizes):
        kind, unit, width = next(v for s, v in layings(True).items() if abs(s - size) < 1.0)
        plan = LayerPlan(part, kind, 2 * radius, 2 * radius, within=(k + 1, len(sizes)),
                         circle=radius)  # fmt: skip
        rows = math.ceil(2 * radius / width - TOL / width)
        for i in range(rows):
            y0 = -radius + i * width
            y1 = min(y0 + width, radius)
            near = 0.0 if y0 <= 0 <= y1 else min(abs(y0), abs(y1))
            chord = 2 * math.sqrt(max(radius * radius - near * near, 0.0))
            start = radius - chord / 2  # the row centred on the circle
            pieces = run_pieces(chord, unit, stagger=i % 2 == 1, height=y1 - y0, full_h=width)
            plan.courses.append(
                Course(i + 1, y0 + radius, tuple(replace(p, start=p.start + start) for p in pieces))
            )
        plans.append(plan)
    return plans


def cap_volume(rho: float, below: float) -> float:
    """A sphere of radius rho, its centre ``below`` the springline: its volume above it."""
    h = rho - below
    return math.pi * h * h * (3 * rho - h) / 3 if h > 0 else 0.0


def plan_round_masonry(kiln: Kiln) -> MasonryPlan:
    us = kiln.units == "us"
    c = kiln.chamber
    inside = si(c.width, "mm") / 2
    height = si(c.height, "mm")
    method = ring_method(c.rings, kiln.heat.electric is not None)
    findings: list[Finding] = []
    whole: Counter[str] = Counter()
    shapes: Counter[tuple[str, str]] = Counter()
    cuts: dict[str, list[Cut]] = {}
    sheet_area: defaultdict[str, float] = defaultdict(float)
    sheet_area_thickness: defaultdict[str, float] = defaultdict(float)
    sheet_thickness: dict[str, set[float]] = {}
    cast_volume: defaultdict[str, float] = defaultdict(float)
    lines: list[str] = []
    parts = {p.name: p for p in lining_parts(kiln)}
    layers: list[LayerPlan] = []
    ring_plans: list[RingPlan] = []

    def sheet(mid: str, area: float, thickness: float) -> None:
        sheet_area[mid] += area
        sheet_area_thickness[mid] += area * thickness
        sheet_thickness.setdefault(mid, set()).add(round(thickness, 2))

    def unbuildable(where: str, mid: str, thickness: float, rings: bool) -> None:
        name = f"{where}, {material(mid).name}"
        step = 4.5 * IN
        below: float | None
        if rings:
            below = math.floor(thickness / step) * step or None
            above = (math.floor(thickness / step) + 1) * step
        else:
            below, above = buildable_near(thickness)
        source, sums = (SOURCE, RINGS) if rings else (BRICK_SOURCE, SUMS)
        sheet_ = whole_bricks(name, thickness, below, above, 1.0, us, source, sums)
        choices = " or ".join(length_text(t, us) for t in (below, above) if t is not None)
        what = (
            "a round wall is laid in rings of 9 in key bricks and 4½ in rings (Olsen, p.45)"
            if rings
            else "whole 9 × 4½ × 2½ in bricks make layers 2½, 4½ or 9 in thick, or sums of those"
        )
        findings.append(
            Finding.failed(
                sheet_.check(),
                message=(
                    f"{where} is {length_text(thickness, us)} of {material(mid).name}, but {what}. "
                    "So its bricks are missing from the brick count, the bill of materials and "
                    f"the price. Make it {choices} thick."
                ),
                reference=source,
            )
        )

    def _wall_ring(mid: str, r: float, depth: float, part: Part, within: tuple[int, int]) -> str:
        """Count one ring of the wall, ``r`` its inside radius; plan it; say what it is."""
        series = ring_series(depth, method)
        assert series is not None, "wall_rings gives 9 and 4½ in rings only"
        family = FAMILIES[series]
        course = family.height * IN
        courses = math.ceil(height / course - TOL / course)
        try:
            one = ring(2 * r, series)
        except RingError as e:
            findings.append(Finding(level="warning", message=f"Round wall: {e}.", reference=SOURCE))
            return ""
        top = height - (courses - 1) * course
        ripped = abs(top - course) >= TOL
        ring_plans.append(RingPlan(part, within, r, depth, series, one, courses, course, top))
        is_cut = series in ("cut", "cut2.5", "cut3")
        if is_cut and (check := cut_ring_sheet(2 * r, depth).check()).status != "pass":
            n = math.floor(cut_bricks(2 * r, depth))
            near = " or ".join(
                f"{length_text(cut_diameter(k, depth), us)} ({k} bricks)"
                for k in (n, n + 1)
                if k >= 3
            )
            findings.append(Finding.failed(check, (
                f"Round wall: a {length_text(2 * r, us)} ring of straights cut to the angle "
                f"takes {cut_bricks(2 * r, depth):.2f} full 9 in bricks round, more than 1/16 in "
                f"from whole bricks, so it is laid with the fewest, {n}, and a closer cut to "
                f"{length_text(one.length or 0.0, us)}: allowed, but not usual. Cut rings are "
                "built in whole bricks, as electric kilns are sized 6, 8, 10, 12 bricks round: "
                f"for no closer make this ring {near} across inside.")))  # fmt: skip
        if series == "mortar" or is_cut:
            full = 9 * IN
            heights = [course] * (courses - 1) + [top]
            for name, n in one.counts:
                long = full if name == family.straight else one.length
                assert long is not None
                for h in heights:
                    if abs(long - full) < TOL and abs(h - course) < TOL:
                        whole[mid] += n
                    else:
                        cuts.setdefault(mid, []).extend([Cut(long, h, full, course)] * n)
            text = f"{length_text(depth, us)} ring of {courses} courses of {one.describe()}"
            text += straight_ring_text(one, us)
            if ripped:
                text += f", the top course ripped to {length_text(top, us)}"
            return text
        for name, n in one.counts:
            if name != family.straight:
                shapes[(mid, name)] += n * courses  # the top course's are cut down from whole
            elif ripped:
                whole[mid] += n * (courses - 1)
                # Keys lie flat and are ripped to the top course; arch bricks stand on end and
                # are cut short
                cut = (
                    Cut(9 * IN, top, 9 * IN, course)
                    if series == "key"
                    else Cut(top, 2.5 * IN, 9 * IN, 2.5 * IN)
                )
                cuts.setdefault(mid, []).extend([cut] * n)
            else:
                whole[mid] += n * courses
        text = f"{length_text(depth, us)} ring of {courses} courses of {one.describe()}"
        if ripped:
            text += f", the top course ripped to {length_text(top, us)}"
        return text

    # The wall, ring by ring
    r = inside
    for i, layer in enumerate(kiln.lining.walls):
        m = resolve_material(kiln, layer.material)
        th = si(layer.thickness, "mm")
        where = f"Round wall, layer {i + 1} from the inside"
        if m.kind in BRICK_KINDS:
            depths = wall_rings(th, method)
            if depths is None:
                unbuildable(where, m.id, th, rings=True)
            else:
                part = parts[f"wall/{i + 1}-{layer.material}"]
                said = [
                    _wall_ring(m.id, r + sum(depths[:k]), d, part, (k + 1, len(depths)))
                    for k, d in enumerate(depths)
                ]
                lines.append(f"{where}: " + "; then ".join(s for s in said if s))
        elif m.kind in SHEET_KINDS:
            sheet(m.id, 2 * math.pi * (r + th / 2) * height, th)
        elif m.kind in BULK_KINDS:
            cast_volume[m.id] += math.pi * ((r + th) ** 2 - r * r) * height
        r += th
    outside = inside + sum(si(x.thickness, "mm") for x in kiln.lining.walls)

    def disc(face: str, radius: float) -> None:
        for i, layer in enumerate(kiln.lining.for_face(face)):  # type: ignore[arg-type]
            m = resolve_material(kiln, layer.material)
            th = si(layer.thickness, "mm")
            where = f"{face.capitalize()}, layer {i + 1} from the inside"
            area = math.pi * radius * radius
            if m.kind in BRICK_KINDS:
                plans = _disc_rows(radius, th, parts[f"{face}/{i + 1}-{layer.material}"])
                if plans is None:
                    unbuildable(where, m.id, th, rings=False)
                    continue
                layers.extend(plans)
                pieces = [p for plan in plans for p in plan.pieces]
                n_whole = 0
                for p in pieces:
                    if abs(p.length - p.full_length) < TOL and abs(p.height - p.full_height) < TOL:
                        n_whole += 1
                    else:
                        cuts.setdefault(m.id, []).append(
                            Cut(p.length, p.height, p.full_length, p.full_height)
                        )
                whole[m.id] += n_whole
                lines.append(
                    f"{where}: rows of straights across a {length_text(2 * radius, us)} circle, "
                    f"{n_whole} whole and {len(pieces) - n_whole} cut to the circle"
                )
            elif m.kind in SHEET_KINDS:
                sheet(m.id, area, th)
            elif m.kind in BULK_KINDS:
                cast_volume[m.id] += area * th

    disc("floor", outside)
    roof = kiln.roof
    if isinstance(roof, FlatRoof):
        disc("roof", outside)
    elif isinstance(roof, Dome):
        dome = RoundDome(2 * inside, si(roof.rise, "mm"))
        below = dome.radius - dome.rise  # the sphere's centre under the springline
        rho = dome.radius
        for i, layer in enumerate(kiln.lining.for_face("roof")):
            m = resolve_material(kiln, layer.material)
            th = si(layer.thickness, "mm")
            volume = cap_volume(rho + th, below) - cap_volume(rho, below)
            if m.kind in BRICK_KINDS:
                count = math.ceil(volume / BRICK_VOLUME)
                whole[m.id] += count
                lines.append(
                    f"Dome, layer {i + 1} from the inside: about {count} bricks by volume, cut to "
                    "the curve"
                )
            elif m.kind in SHEET_KINDS:
                sheet(m.id, volume / th, th)
            elif m.kind in BULK_KINDS:
                cast_volume[m.id] += volume
            rho += th
    if lines:
        findings.append(
            Finding(
                level="info",
                message=(
                    "Round kiln: " + "; ".join(lines) + ". Tapered rings follow Olsen's circle "
                    "tables. A 4½ in ring is the builder's choice (the design's chamber.rings): "
                    "straights with mortar-filled wedge joints, as Olsen draws a curved wall "
                    "(Fig. 2-13, p.45); straights cut to the angle, the norm in electric kilns; "
                    "straights with featheredges; or arch bricks, possible but not recommended "
                    f"(p.45). This one: {method}. "
                    + (
                        "Cut rings are stacked course on course, their facets in line: in small "
                        "kilns, electric especially, a smooth wall matters more than staggered "
                        "joints (the user, a kiln builder). "
                        if method == "cut"
                        else "Stagger the joints course to course as in a straight wall (p.45). "
                    )
                    + "Brick counts assume dry joints at the nominal size, "
                    "but for the wedge joints said; the breakage allowances are those of a box "
                    "kiln (allowance.py)."
                ),
                reference=f"{SOURCE}; {MORTAR_SOURCE}; {FEATHEREDGE_SOURCE}; {BRICK_SOURCE}",
            )
        )
    # The fireboxes: boxes of the kiln's layers, laid as a box kiln's are
    for part in (p for p in parts.values() if p.name.startswith("firebox-")):
        m = resolve_material(kiln, part.material)
        if m.kind in BRICK_KINDS:
            plans = plan_layers(part)
            if plans is None:
                findings.append(_not_buildable(part, us))
                continue
            layers.extend(plans)
            for p in (p for plan in plans for p in plan.pieces):
                if p.is_whole:
                    whole[m.id] += 1
                else:
                    cuts.setdefault(m.id, []).append(
                        Cut(p.length, p.height, p.full_length, p.full_height)
                    )
        elif m.kind in SHEET_KINDS:
            sheet(m.id, part.area, part.thickness)
        elif m.kind in BULK_KINDS:
            cast_volume[m.id] += part.volume
    findings += firebox_findings(kiln) + port_findings(kiln)
    quantities, cut_list, working = buy_quantities(
        kiln, whole, shapes, cuts, sheet_area, sheet_area_thickness, sheet_thickness, cast_volume,
        shapes_in="the round wall",
    )  # fmt: skip
    result = Masonry(quantities=quantities, cut_list=cut_list, findings=findings, working=working)
    return MasonryPlan(layers, result, ring_plans)
