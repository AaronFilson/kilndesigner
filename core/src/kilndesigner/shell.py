"""Chambers and shell: what the design can say about a kiln's chambers and walls beyond one box
of one size (docs/planning/11-09-26.md, B3).

- No door: a kiln set over its walls, open-topped (loading.type "top").
- A door hung on its own frame from trolleys (loading.hung): its weight against their rating.
- A cone for each chamber in a row (firing.chamber_cones): the heat loss, chamber by chamber.
- Chambers of different sizes in a row (chamber.sizes).
- A back wall built thicker or thinner than the sides (lining.back, through Lining.for_face).
- A plan whose width changes along the run: a tunnel's sections, a groundhog tapering to its
  chimney (chamber.widths).
- Double-radius, offset-peak arches along the draft (roof.peak_at), by the line of thrust.

Each is checked here for the range that has been worked out, and refused with the reason
outside it (ADR 0009).
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING

from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_, Quantity, si
from kilndesigner.working import Finding, Step, show

if TYPE_CHECKING:
    from kilndesigner.bom import BomLine
    from kilndesigner.frame import FrameDesign
    from kilndesigner.model import Face, Kiln
    from kilndesigner.run_parts import RunLayout
    from kilndesigner.shape import Arch, ChamberShape, FaceShape


# --- The design's limits ----------------------------------------------------------------------


def check_shell(kiln: Kiln) -> None:
    """Refuse what the B3 fields can't build, with the reason."""
    _check_top(kiln)
    _check_hung(kiln)
    _check_cones(kiln)
    _check_sizes(kiln)
    _check_widths(kiln)
    _check_peak(kiln)


def _check_top(kiln: Kiln) -> None:
    from kilndesigner.model import OpenTop

    loading = kiln.loading
    if loading.type != "top":
        return
    if not isinstance(kiln.roof, OpenTop):
        raise ValueError(
            "a kiln with no door is set over its walls, so it is laid out only open-topped "
            "(roof: open), as Singh's low-fire kiln is (Olsen Fig 6-11): give it a door, a car or "
            "a lid, or an open top"
        )
    if loading.opening is not None or loading.door is not None or kiln.lining.door is not None:
        raise ValueError(
            "a kiln set over its walls has no door: leave out loading.opening, loading.door and "
            "lining.door"
        )


def _check_hung(kiln: Kiln) -> None:
    loading = kiln.loading
    if loading.hung is None:
        return
    if loading.type not in ("door", "car"):
        raise ValueError("a hung door closes a wall: it is for a door or a car, not a lid or none")
    if loading.door is not None:
        raise ValueError(
            "a door hung on its own frame is neither bricked up nor hinged: leave out loading.door"
        )


def _check_cones(kiln: Kiln) -> None:
    from kilndesigner import cones
    from kilndesigner.heatloss import top_temperature

    given = kiln.firing.chamber_cones
    if given is None:
        return
    n = kiln.chamber.chambers
    if n < 2 or len(given) != n:
        raise ValueError(
            f"give a cone for each of the {n} chambers in a row, front to back, not {len(given)}"
        )
    top = si(top_temperature(kiln)[0], "degC")
    for i, cone in enumerate(given):
        if cone is None:
            continue
        t = si(cones.cone_temperature(cone, kiln.firing.final_rate), "degC")
        if t > top + 1e-6:
            raise ValueError(
                f"chamber {i + 1}'s cone {cone}, {t:g} °C, is hotter than the firing's top, "
                f"{top:g} °C: the firing's cone or top temperature is the hottest chamber's"
            )


def _check_sizes(kiln: Kiln) -> None:
    from kilndesigner.model import Dome, FlatRoof, OpenTop, SprungArch

    c, roof = kiln.chamber, kiln.roof
    if c.sizes is None:
        return
    if c.shape != "box" or c.outline is not None or c.bend is not None or c.widths is not None:
        raise ValueError(
            "chambers of different sizes are laid out as straight box chambers in a row: leave "
            "out the shape, outline, bend and widths"
        )
    arch_along = isinstance(roof, SprungArch) and not roof.tube and roof.crossing is None
    if not (isinstance(roof, FlatRoof | OpenTop | Dome) or arch_along):
        raise ValueError(
            "chambers of different sizes take each its own arch along the draft, its own dome, "
            "or a flat roof: a tube's vault or a catenary over chambers of different heights "
            "isn't described here"
        )
    if isinstance(roof, SprungArch | Dome) and not roof.buttressed:
        raise ValueError(
            "chambers of different sizes are held by masonry here (roof.buttressed: true), as "
            "climbing kilns' arches throw their thrust onto the common walls (Olsen p.94–95): "
            "the bracing statics of end walls under arches of different sizes aren't worked out"
        )
    if isinstance(roof, SprungArch) and roof.front_springline is not None:
        raise ValueError("chambers of different sizes spring level: leave out front_springline")
    if kiln.heat.electric is not None:
        raise ValueError(
            "elements are laid out along a run of one size: fire chambers of different sizes "
            "with gas or fuel"
        )
    width = si(c.width, "in")
    for i, (depth, _, rise) in enumerate(sizes_of(kiln, "in")):
        if isinstance(roof, SprungArch) and not 0 < rise <= depth / 2:
            raise ValueError(
                f"chamber {i + 1}'s arch, along its {depth:g} in depth, must rise more than 0 and "
                f"at most half that, {depth / 2:g} in"
            )
        if isinstance(roof, Dome) and not 0 < rise < math.hypot(width, depth) / 2:
            raise ValueError(
                f"chamber {i + 1}'s dome must rise less than half its diagonal, "
                f"{math.hypot(width, depth) / 2:.1f} in"
            )


def _check_widths(kiln: Kiln) -> None:
    from kilndesigner.model import FlatRoof, OpenTop, SprungArch

    c, roof = kiln.chamber, kiln.roof
    if c.widths is None:
        return
    if c.shape != "box" or c.chambers > 1 or c.outline is not None or c.bend is not None:
        raise ValueError(
            "a width changing along the run is laid out for one straight box chamber: leave out "
            "its shape, chambers, outline and bend"
        )
    across = isinstance(roof, SprungArch) and not (roof.along or roof.tube or roof.crossing)
    if not (across or isinstance(roof, FlatRoof | OpenTop)):
        raise ValueError(
            "a chamber whose width changes takes a sprung arch across its width, a flat roof or "
            "an open top: a catenary, a dome or an arch along the draft over a changing width "
            "isn't described here"
        )
    if kiln.heat.electric is not None:
        raise ValueError("elements are laid out along straight walls: fire it with gas or fuel")
    if kiln.loading.opening is not None and kiln.loading.face in ("left", "right"):
        raise ValueError("a door in a side wall that runs on the slant isn't laid out: use an end")
    stations = widths_of(kiln, "in")
    depth = si(c.depth, "in")
    ats = [a for a, _ in stations]
    if abs(ats[0]) > 1e-6 or abs(ats[-1] - depth) > 1e-6:
        raise ValueError(
            f"the widths run from the front wall (at 0) to the back (at the depth, {depth:g} in)"
        )
    if any(b <= a for a, b in itertools.pairwise(ats)):
        raise ValueError("give the widths' stations in order, front to back, each further on")
    if any(w <= 0 for _, w in stations):
        raise ValueError("each width must be more than 0")


def _check_peak(kiln: Kiln) -> None:
    from kilndesigner.model import SprungArch, arches_along

    roof = kiln.roof
    if not isinstance(roof, SprungArch) or roof.peak_at is None:
        return
    share = si(roof.peak_at, "")
    if not 0 < share < 1:
        raise ValueError("an arch's peak stands within its span: more than 0 % and under 100 %")
    if not arches_along(kiln) or roof.front_springline is not None:
        raise ValueError(
            "an offset peak is laid out for arches along the draft springing level, as the Kyoto "
            "kilns' are (chambers in a row, or roof.along): leave out front_springline"
        )
    if not roof.buttressed or roof.building_frame:
        raise ValueError(
            "an offset-peak arch is held by masonry here (roof.buttressed: true, no "
            "building_frame), as the climbing kilns' arches are (Olsen p.95): no steel is sized "
            "for an arch of two radii"
        )
    for i, (depth, _, rise) in enumerate(sizes_of(kiln, "in")):
        arch = PeakArch(depth, rise, share)
        if min(arch.front_run, arch.back_run) < rise - 1e-9:
            raise ValueError(
                f"chamber {i + 1}'s peak, {share * 100:g} % along its {depth:g} in span, leaves a "
                f"half running {min(arch.front_run, arch.back_run):.1f} in, less than the "
                f"{rise:g} in rise: that half would turn past a quarter circle and lean in at its "
                "springing. Bring the peak nearer the middle, or lower the arch"
            )


# --- A door hung on its own frame ---------------------------------------------------------------

HUNG = (
    "Olsen, The Kiln Book, 4th ed., Fig 6-64 (Kaneko's door, hung from an overhead I-beam on two "
    "half-ton trolleys, with spring latches); the door's weight is its layers' density × thickness "
    "× its area, statics"
)


def door_weight(kiln: Kiln) -> tuple[float, float, list[str]]:
    """The door's weight (lb), its area (ft²) and each layer's line: a whole wall, out to the
    side walls' outside and up to the springline (an arch's segment over it, at an end), or the
    opening, laid in the wall's layers."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.model import SprungArch
    from kilndesigner.shape import Arch
    from kilndesigner.units import parse_quantity

    face, c = kiln.door_face, kiln.chamber
    opening = kiln.loading.opening
    assert face not in ("floor", "roof")
    if opening is not None:
        area = si(opening.width, "in") * si(opening.height, "in")
        layers = kiln.lining.for_face(face)
    else:
        layers = kiln.lining.for_face(face, door_face=face)
        h = si(c.height, "in")
        if face in ("front", "back"):
            sides = sum(si(x.thickness, "in") for x in kiln.lining.for_face("left"))
            sides += sum(si(x.thickness, "in") for x in kiln.lining.for_face("right"))
            width = si(c.width, "in")
            area = (width + sides) * h
            roof = kiln.roof
            if isinstance(roof, SprungArch) and not roof.along and c.chambers == 1:
                area += Arch(width, si(roof.rise, "in")).segment_area
        else:
            area = si(c.length, "in") * h
    weight, lines = 0.0, []
    for x in layers:
        m = resolve_material(kiln, x.material)
        rho, t = si(parse_quantity(m.density), "lb/ft**3"), si(x.thickness, "in")
        w = rho * t / 12 * area / 144
        weight += w
        lines.append(f"{m.name}: {rho:.0f} lb/ft³ × {t:g} in × {area / 144:.2f} ft² = {w:.0f} lb")
    return weight, area / 144, lines


def door_hardware(kiln: Kiln, findings: list[Finding]) -> bool:
    """What hardware.py says of a kiln with no door, or a hung door; True when nothing else is
    to be drawn for the door (a car's deck still is)."""
    loading = kiln.loading
    if loading.type == "top":
        findings.append(
            Finding(
                level="info",
                message=(
                    "The kiln has no door: it is set over its walls and covered for each firing, "
                    "as Singh's low-fire kiln is (Olsen, 4th ed. Fig 6-11). Its walls are all wall."
                ),
                reference="Olsen, The Kiln Book, 4th ed., p.155–156, Figs 6-11 to 6-13",
            )
        )
        return True
    if loading.hung is None:
        return False
    findings.append(
        Finding(
            level="info",
            message=(
                f"The {kiln.door_face} wall is a door hung on its own frame from an overhead beam "
                f"on {loading.hung.trolleys} trolleys, rolled aside to load, as Kaneko's is "
                "(Olsen, 4th ed. Fig 6-64): no hinges. Its frame, latches and beam are the "
                "builder's: no source here sizes them."
            ),
            reference=HUNG,
        )
    )
    return loading.type != "car"


def hung_door_line(kiln: Kiln) -> BomLine | None:
    """The hung door's trolleys, for the bill of materials: listed, not priced."""
    from kilndesigner.bom import BomLine

    hung = kiln.loading.hung
    if hung is None:
        return None
    rating = si(hung.trolley_rating, "lb")
    return BomLine(
        item=f"Door trolleys, rated {rating:,.0f} lb each, and the overhead beam they run on",
        needed=f"{hung.trolleys} trolleys; the beam as the builder sizes it",
        buy=f"{hung.trolleys} trolleys",
        unit_price=None,
        cost=None,
        priced_as=None,
        source=HUNG,
    )


def hung_door_statics(kiln: Kiln) -> tuple[list[Step], list[Finding]]:
    """A hung door's weight against its trolleys' rated load (loading.hung)."""
    hung = kiln.loading.hung
    if hung is None:
        return [], []
    weight, area, lines = door_weight(kiln)
    rated = hung.trolleys * si(hung.trolley_rating, "lb")
    step = Step(
        name="The hung door's weight on its trolleys",
        value=f"{weight:,.0f} lb on {hung.trolleys} trolleys rated {rated:,.0f} lb in all",
        formula="W = Σ ρ·t·A over the door's layers; W ≤ n·R",
        inputs={
            **{f"layer {i + 1}": s for i, s in enumerate(lines)},
            "door's area A": f"{area:.2f} ft²",
            "trolleys n × rating R": f"{hung.trolleys} × {si(hung.trolley_rating, 'lb'):g} lb",
        },
        reference=HUNG,
        note=(
            "The door's own masonry only: its steel frame and the latches add to it, and are the "
            "builder's. The beam it runs on isn't sized: no span or section is printed for it."
        ),
    )
    sheet = Sheet("frame.hung_door", "The hung door's weight on its trolleys", reference=HUNG)
    sheet.given("W", "the door's masonry", Q_(weight, "lb"), source="working: the door's layers")
    sheet.given("n", "trolleys", hung.trolleys, source="the design: loading.hung.trolleys")
    sheet.given("R", "each trolley's rated load", Q_(si(hung.trolley_rating, "lb"), "lb"),
                source="the design: loading.hung.trolley_rating")  # fmt: skip
    sheet.let("C", "the trolleys' rated load", "n*R", "lb")
    sheet.require("W", "<=", "C", level="warning")
    sheet.agrees("C", Q_(rated, "lb"))
    if (check := sheet.check()).status != "pass":
        finding = Finding.failed(
            check,
            message=(
                f"The hung door weighs about {weight:,.0f} lb, more than its {hung.trolleys} "
                f"trolleys' {rated:,.0f} lb rated load: use more or larger trolleys, or a lighter "
                "door."
            ),
        )
    else:
        finding = Finding(
            level="info",
            message=(
                f"The door hangs from an overhead beam on {hung.trolleys} trolleys, rated "
                f"{rated:,.0f} lb in all; its masonry weighs about {weight:,.0f} lb. Its frame, "
                "latches and the beam aren't sized: no source here gives them."
            ),
            reference=HUNG,
        )
    return [step], [finding]


# --- A cone for each chamber --------------------------------------------------------------------

CHAMBER_CONES = (
    "the design's cone for each chamber (firing.chamber_cones), as Olsen prints Suzuki's, chamber "
    "by chamber (4th ed. Fig 4-35); Orton cone charts, cones.md"
)


def chamber_temperatures(kiln: Kiln) -> list[float]:
    """Each chamber's top temperature, K, front to back: its own cone, or the firing's top."""
    from kilndesigner import cones
    from kilndesigner.heatloss import top_temperature

    top = si(top_temperature(kiln)[0], "K")
    given = kiln.firing.chamber_cones or [None] * kiln.chamber.chambers
    return [
        top if c is None else si(cones.cone_temperature(c, kiln.firing.final_rate), "K")
        for c in given
    ]


def chamber_cones_loss(kiln: Kiln, at_top: float, air: Quantity) -> tuple[float, Step]:
    """The kiln's loss with each chamber at its own cone: the whole run's loss at each chamber's
    temperature, times that chamber's share of the run's length, summed. The faces of a run are
    its side walls, floor and roof along the run, and its end walls; the share takes the end
    walls with the chambers beside them along the run, which errs a little to the hot side for
    the coolest end chamber, the safe side."""
    from kilndesigner.heatloss import heat_loss

    temps = chamber_temperatures(kiln)
    depths = [d for d, _, _ in sizes_of(kiln, "m")]
    run = sum(depths)
    top = max(temps)
    at: dict[float, float] = {top: at_top}
    for t in temps:
        if t not in at:
            at[t] = heat_loss(kiln, ambient=air, inside=Q_(t, "K")).total_watts
    total = sum(d / run * at[t] for d, t in zip(depths, temps, strict=True))
    unit = "degF" if kiln.units == "us" else "degC"
    lines = {
        f"chamber {i + 1}": (
            f"{show(Q_(t, 'K'), unit)}, {d / run * 100:.1f} % of the run: "
            f"{show(Q_(d / run * at[t], 'W'), 'kW')}"
        )
        for i, (d, t) in enumerate(zip(depths, temps, strict=True))
    }
    return total, Step(
        name="Heat loss, each chamber at its own cone",
        value=show(Q_(total, "W"), "kW"),
        formula="Q = Σ (d_k / Σd)·Q_run(T_k): each chamber's share of the run at its own top",
        inputs=lines,
        reference=CHAMBER_CONES,
        note=(
            "The faces and their temperatures listed are the whole run held at the hottest "
            "chamber's top; the total takes each chamber at its own. Heat passing between the "
            "chambers through the walls between them isn't counted, as for one top temperature."
        ),
    )


# --- Sizes along a row --------------------------------------------------------------------------


def sizes_of(kiln: Kiln, unit: str) -> list[tuple[float, float, float]]:
    """Each chamber's depth, springline height and roof rise (0 for a roof without one), front to
    back, in ``unit``: from chamber.sizes, or the chamber's own size for each."""
    from kilndesigner.model import Dome, SprungArch

    c, roof = kiln.chamber, kiln.roof
    rise = si(roof.rise, unit) if isinstance(roof, SprungArch | Dome) else 0.0
    height = si(c.height, unit)
    if c.sizes is None:
        return [(si(c.depth, unit), height, rise)] * c.chambers
    return [
        (
            si(s.depth, unit),
            si(s.height, unit) if s.height is not None else height,
            si(s.rise, unit) if s.rise is not None and rise else rise,
        )
        for s in c.sizes
    ]


def shell_not_drawn(kiln: Kiln) -> str | None:
    """Why this kiln's bricks can't be laid out yet (geometry.not_drawn), for the B3 fields."""
    from kilndesigner.model import SprungArch

    if kiln.chamber.widths is not None:
        return (
            "a chamber whose width changes along its run is calculated and drawn as shells, but "
            "its bricks aren't laid out or priced: the courses of a wall on the slant and the "
            "rings of an arch whose span changes aren't described here"
        )
    roof = kiln.roof
    if isinstance(roof, SprungArch) and roof.peak_at is not None:
        return (
            "an offset-peak arch is calculated and drawn as shells, but its bricks aren't laid "
            "out or priced: no source here gives the arch bricks for an arch of two radii"
        )
    return None


def sizes_note(kiln: Kiln, run: RunLayout, us: bool) -> str:
    """What masonry.py says of chambers of different sizes: each one's size, and its floor."""
    from kilndesigner.working import length_text

    def size(i: int) -> str:
        return (
            f"chamber {i + 1} {length_text(run.depth_of(i), us)} deep, its springline "
            f"{length_text(run.height_of(i), us)} up"
            + (f", its floor {length_text(run.floor(i), us)} above the first's" if i else "")
        )

    return (
        "Each chamber is its own size (chamber.sizes): "
        + "; ".join(size(i) for i in range(run.chambers))
        + ". The floors climb the slope between the chambers' centres, and each wall between "
        "chambers rises to the higher springline of the two beside it. Each chamber is built "
        "level, in level courses. "
    )


def sized(kiln: Kiln) -> bool:
    """Chambers in a row whose sizes differ (chamber.sizes)."""
    return kiln.chamber.sizes is not None


# --- Widths along the run -----------------------------------------------------------------------


def widths_of(kiln: Kiln, unit: str) -> list[tuple[float, float]]:
    """The stations along the chamber, (from the front wall, width), in ``unit``; the chamber's
    width at both ends when no widths are given."""
    c = kiln.chamber
    if c.widths is None:
        return [(0.0, si(c.width, unit)), (si(c.depth, unit), si(c.width, unit))]
    return [(si(s.at, unit), si(s.width, unit)) for s in c.widths]


def width_at(stations: list[tuple[float, float]], y: float) -> float:
    """The width at ``y`` from the front wall: straight between stations."""
    if y <= stations[0][0]:
        return stations[0][1]
    for (a, wa), (b, wb) in itertools.pairwise(stations):
        if y <= b:
            return wa + (wb - wa) * (y - a) / (b - a)
    return stations[-1][1]


@dataclass(frozen=True)
class Taper:
    """A plan whose width changes straight between stations (chamber.widths): the integrals the
    areas and volume need, in one unit. A sprung arch over it keeps its shape, its radius and
    segment scaling with the width and its angle the same (``ratio`` the rise over the span, 0
    without one)."""

    stations: tuple[tuple[float, float], ...]

    @property
    def depth(self) -> float:
        return self.stations[-1][0] - self.stations[0][0]

    def _pieces(self) -> list[tuple[float, float, float]]:
        return [(b - a, wa, wb) for (a, wa), (b, wb) in zip(self.stations, self.stations[1:],
                                                             strict=False)]  # fmt: skip

    @property
    def area(self) -> float:
        """The plan's area, ∫w dy: each piece a trapezoid."""
        return sum(length * (wa + wb) / 2 for length, wa, wb in self._pieces())

    @property
    def square(self) -> float:
        """∫w² dy, for a section growing as the width squared: L(a² + ab + b²)/3 a piece."""
        return sum(length * (wa * wa + wa * wb + wb * wb) / 3 for length, wa, wb in self._pieces())

    @property
    def side(self) -> float:
        """One side wall's length along its slant: Σ √(L² + ((b − a)/2)²)."""
        return sum(math.hypot(length, (wb - wa) / 2) for length, wa, wb in self._pieces())

    @property
    def widest(self) -> float:
        return max(w for _, w in self.stations)

    @property
    def front(self) -> float:
        return self.stations[0][1]

    @property
    def back(self) -> float:
        return self.stations[-1][1]


# --- The chamber's faces and volume --------------------------------------------------------------


def shell_shape(kiln: Kiln) -> ChamberShape:
    """The chamber's shape (shape.ChamberShape, m) for chambers of different sizes, a width
    changing along the run, or an offset-peak arch: its volume and faces worked out here, each
    face growing through the lining as shape.py's do."""
    from kilndesigner.model import OpenTop
    from kilndesigner.shape import ChamberShape

    c = kiln.chamber
    w, h = si(c.width, "m"), si(c.height, "m")
    volume, faces = _taper_faces(kiln) if c.widths is not None else _row_faces(kiln)
    return ChamberShape(
        w, si(c.length, "m"), h, None, open_top=isinstance(kiln.roof, OpenTop),
        chambers=c.chambers, given=(volume, tuple(faces)),
    )  # fmt: skip


def _row_faces(kiln: Kiln) -> tuple[float, list[FaceShape]]:
    """Chambers in a row, each its own size and its own arch along the draft, dome or flat roof:
    the side walls the sum of each chamber's, capped up to its arch or dome; the end walls the
    first's and the last's; the walls between losing no heat outside, as shape._row_faces. Where
    two chambers' springlines differ, the wall between rises to the higher, and the step between
    their roofs isn't counted."""
    from kilndesigner.model import Dome, SprungArch
    from kilndesigner.shape import Arch, FaceShape, SailDome

    roof = kiln.roof
    w = si(kiln.chamber.width, "m")
    rows = sizes_of(kiln, "m")
    n = len(rows)
    total = sum(d for d, _, _ in rows)
    tallest = max(h for _, h, _ in rows)
    share = si(roof.peak_at, "") if isinstance(roof, SprungArch) and roof.peak_at else None
    arches: list[Arch | PeakArch] = []
    domes: list[SailDome] = []
    if isinstance(roof, SprungArch):
        arches = [PeakArch(d, r, share) if share is not None else Arch(d, r) for d, _, r in rows]
    elif isinstance(roof, Dome):
        domes = [SailDome(w, d, r) for d, _, r in rows]
    if arches:
        segs = [a.segment_area for a in arches]
    elif domes:
        segs = [m.segment(w / 2, d) for m, (d, _, _) in zip(domes, rows, strict=True)]
    else:
        segs = [0.0] * n

    def sides(t: float) -> float:
        pieces = zip(rows, segs, strict=True)
        return sum((d + 2 * t / n) * (h + 2 * t) + s for (d, h, _), s in pieces)

    def end(k: int) -> float:
        d, h, _ = rows[k]
        return w * h + (domes[k].segment(d / 2, w) if domes else 0.0)

    first, last = rows[0][1], rows[-1][1]
    faces = [
        FaceShape("left", "vertical", sides(0.0), total, tallest, grows=sides),
        FaceShape("right", "vertical", sides(0.0), total, tallest, grows=sides),
        FaceShape("back", "vertical", end(n - 1), w, last),
        FaceShape("front", "vertical", end(0), w, first),
        FaceShape("floor", "facing_down", w * total, w, total),
    ]
    volume = sum(w * d * h for d, h, _ in rows)
    if arches:

        def vaults(t: float) -> float:
            return sum(_grown(a, t) for a in arches) * (w + 2 * t)

        arc = sum(a.arc_length for a in arches)
        faces.append(FaceShape("roof", "facing_up", vaults(0.0), arc, w, grows=vaults))
        volume += w * sum(segs)
    elif domes:

        def caps(t: float) -> float:
            return sum(m.area(t) for m in domes)

        faces.append(FaceShape("roof", "facing_up", caps(0.0), w, total, grows=caps))
        volume += sum(m.volume for m in domes)
    else:
        faces.append(FaceShape("roof", "facing_up", w * total, w, total))
    return volume, faces


def _grown(arch: Arch | PeakArch, t: float) -> float:
    """An arch's length t out from its inside."""
    if isinstance(arch, PeakArch):
        return arch.grown(t)
    return 2 * (arch.radius + t) * arch.half_angle


def _taper_faces(kiln: Kiln) -> tuple[float, list[FaceShape]]:
    """One chamber whose width changes straight between stations (chamber.widths): its side walls
    along their slant, its end walls each its own width, its floor the plan, and a sprung arch
    over it keeping its shape, its radius and segment scaling with the width (rise ∝ width). Each
    face grows through the lining as a box's does: an outline moved out by t gains P·t + 4t²."""
    from kilndesigner.model import SprungArch
    from kilndesigner.shape import Arch, FaceShape

    roof = kiln.roof
    taper = Taper(tuple(widths_of(kiln, "m")))
    width, h, depth = si(kiln.chamber.width, "m"), si(kiln.chamber.height, "m"), taper.depth
    arch = Arch(width, si(roof.rise, "m")) if isinstance(roof, SprungArch) else None
    seg0 = arch.segment_area / width**2 if arch is not None else 0.0
    perimeter = 2 * taper.side + taper.front + taper.back

    def plan(t: float) -> float:
        return taper.area + perimeter * t + 4 * t * t

    def side(t: float) -> float:
        return (taper.side + 2 * t) * (h + 2 * t)

    faces = [
        FaceShape("left", "vertical", side(0.0), taper.side, h, grows=side),
        FaceShape("right", "vertical", side(0.0), taper.side, h, grows=side),
        FaceShape("back", "vertical", taper.back * h + seg0 * taper.back**2, taper.back, h),
        FaceShape("front", "vertical", taper.front * h + seg0 * taper.front**2, taper.front, h),
        FaceShape("floor", "facing_down", taper.area, width, depth, grows=plan),
    ]
    if arch is not None:
        phi, scale = arch.half_angle, arch.radius / width

        def vault(t: float) -> float:
            return 2 * phi * (scale * taper.area + t * depth) * (depth + 2 * t) / depth

        faces.append(FaceShape("roof", "facing_up", vault(0.0), width, depth, grows=vault))
    else:
        faces.append(FaceShape("roof", "facing_up", taper.area, width, depth, grows=plan))
    return h * taper.area + seg0 * taper.square, faces


# --- Statics ----------------------------------------------------------------------------------

WIDEST = (
    "the steel sized for the widest section: the arch keeps its shape along the run, so its "
    "thrust per foot grows with its span, and the widest section's is the most anywhere"
)
PEAK = (
    "a line of thrust through both springings and the peak, three-hinged (vault.THRUST_LINE's, "
    "each half its own circle); Heyman's safe theorem and geometric factor of safety, the ring "
    "twice the thinnest that holds a line (arch-thrust-theory.md); the arch's two radii as "
    "Olsen draws the Kyoto kilns' (4th ed. p.91–92, p.95)"
)


def shell_frame(kiln: Kiln) -> FrameDesign | None:
    """The frame for a width changing along the run (sized at its widest), or the masonry's
    statics for arches along the draft of different sizes or with an offset peak; None for any
    other kiln."""
    from kilndesigner.model import SprungArch

    c, roof = kiln.chamber, kiln.roof
    if c.widths is not None:
        return _widest_frame(kiln)
    if isinstance(roof, SprungArch) and (c.sizes is not None or roof.peak_at is not None):
        return _arches_held(kiln)
    return None


def _widest_frame(kiln: Kiln) -> FrameDesign:
    from kilndesigner.frame import _design_frame  # pyright: ignore[reportPrivateUsage]
    from kilndesigner.model import SprungArch

    c, roof = kiln.chamber, kiln.roof
    widest = Taper(tuple(widths_of(kiln, "in"))).widest
    scale = widest / si(c.width, "in")
    chamber = c.model_copy(update={"width": Q_(widest, "in"), "widths": None})
    update: dict[str, object] = {"chamber": chamber}
    if isinstance(roof, SprungArch):
        update["roof"] = roof.model_copy(update={"rise": Q_(si(roof.rise, "in") * scale, "in")})
    frame = _design_frame(kiln.model_copy(update=update))
    step = Step(
        name="The widest section",
        value=f"{widest:.4g} in wide"
        + (
            f", the arch rising {si(roof.rise, 'in') * scale:.1f} in"
            if isinstance(roof, SprungArch)
            else ""
        ),
        formula="ρ(w) = ρ₀·w / w₀: the arch keeps its shape at every station",
        inputs={
            "stations": ", ".join(f"{w:.4g} in at {a:.4g} in" for a, w in widths_of(kiln, "in"))
        },
        reference=WIDEST,
        note="The frame's members run the chamber's whole length, sized for this section.",
    )
    return frame.model_copy(update={"working": [step, *frame.working]})


def _roof_weight(kiln: Kiln, arch: Arch | PeakArch) -> tuple[float, float]:
    """The arch's weight per foot along its run (lb/ft), every layer, each at its mid-depth's
    length, as frame._arch_load; and the ring's thickness (in)."""
    from kilndesigner.castable import resolve_material
    from kilndesigner.model import SprungArch
    from kilndesigner.units import parse_quantity

    assert isinstance(kiln.roof, SprungArch)
    weight, ring, cum = 0.0, 0.0, 0.0
    for i, layer in enumerate(kiln.lining.for_face("roof")):
        m = resolve_material(kiln, layer.material)
        rho, t = si(parse_quantity(m.density), "lb/ft**3"), si(layer.thickness, "in")
        weight += rho * t / 12 * _grown(arch, cum + t / 2) / 12
        if i < kiln.roof.acting_ring:
            ring += t
        cum += t
    return weight, ring


def _arches_held(kiln: Kiln) -> FrameDesign:
    """Arches along the draft held by masonry (buttressed), each chamber's its own size or with
    its peak set back: each one's cold thrust by a line of thrust through its springings and
    crown, hot × HarbisonWalker's heated factor (a level circular arch's) or, for two radii, his
    largest; and an offset-peak arch's ring against Heyman's factor of 2."""
    from kilndesigner.frame import (
        ARCH_THEORY_SOURCE,
        MASONRY_SOURCE,
        MAX_PRINTED_HEATED,
        NO_FRAME,
        FrameDesign,
        cold_thrust_factor,
        heated_thrust_factor,
    )
    from kilndesigner.model import SprungArch
    from kilndesigner.shape import Arch
    from kilndesigner.vault import _layers as _wall  # pyright: ignore[reportPrivateUsage]
    from kilndesigner.vault import wall_slide

    roof = kiln.roof
    assert isinstance(roof, SprungArch)
    share = si(roof.peak_at, "") if roof.peak_at is not None else None
    working: list[Step] = []
    findings: list[Finding] = []
    hottest = 0.0
    sizes = sizes_of(kiln, "in")
    for i, (depth, _, rise) in enumerate(sizes):
        name = f"chamber {i + 1}'s arch" if kiln.chamber.chambers > 1 else "the arch"
        if share is None:
            arch: Arch | PeakArch = Arch(depth, rise)
            weight, ring = _roof_weight(kiln, arch)
            cold = cold_thrust_factor(depth, rise) * weight
            front = back = weight / 2
            factor = heated_thrust_factor(depth, rise, ring)
            hot = min((factor if factor is not None else MAX_PRINTED_HEATED) * cold,
                      MAX_PRINTED_HEATED * cold)  # fmt: skip
            formula = "H = W·(sin θ − (1 − cos θ)/θ) / (2(1 − cos θ)); hot, × the heated factor"
            reference = ARCH_THEORY_SOURCE
            extra = ""
        else:
            peak = PeakArch(depth, rise, share)
            weight, ring = _roof_weight(kiln, peak)
            cold, front, back = peak.thrust(weight)
            hot = MAX_PRINTED_HEATED * cold
            formula = (
                "H = (W − W_f·c_f/a_f − W_b·c_b/a_b) / (ρ(1/a_f + 1/a_b)), each half about the "
                "peak; hot, × HarbisonWalker's largest factor"
            )
            reference = f"{PEAK}; {ARCH_THEORY_SOURCE}"
            gap = peak.line_gap(ring)
            extra = (
                f"; V {front:.0f} lb at the front, {back:.0f} lb at the back; the line of thrust "
                f"strays {gap * 100:.0f} % of the {ring:g} in ring from its middle"
            )
            sheet = Sheet("frame.peak_line", f"{name.capitalize()}'s line of thrust", PEAK)
            sheet.given("g", "how far the line strays from the ring's middle, over the ring", gap,
                        source="working: the line through the springings and the peak")  # fmt: skip
            sheet.given("q", "within the ring's middle half: a factor of safety of 2", 0.25,
                        source=PEAK)  # fmt: skip
            sheet.require("g", "<=", "q", level="warning")
            if (check := sheet.check()).status != "pass":
                findings.append(
                    Finding.failed(
                        check,
                        message=(
                            f"{name.capitalize()}'s line of thrust, through its springings and its "
                            f"peak, strays {gap * 100:.0f} % of its {ring:g} in ring from the "
                            "ring's middle: "
                            + (
                                "it leaves the ring, so the arch as drawn has no line of thrust "
                                "this way. "
                                if gap > 0.5
                                else "more than the quarter that Heyman's factor of safety of 2 "
                                "allows. "
                            )
                            + "Thicken the ring, or bring the peak nearer the middle."
                        ),
                    )
                )
        hottest = max(hottest, hot)
        working.append(
            Step(
                name=f"Thrust the masonry holds, {name}",
                value=f"{hot:.0f} lb per foot of arch, hot ({cold:.0f} cold){extra}",
                formula=formula,
                inputs={
                    "span, the chamber's depth": f"{depth:g} in",
                    "rise": f"{rise:g} in",
                    "W, the arch's weight": f"{weight:.1f} lb per foot",
                    **({"peak, from the front springing": f"{share * 100:g} %"} if share else {}),
                },
                reference=reference,
                note=(
                    "No heated factor is printed for an arch of two radii, so HarbisonWalker's "
                    "largest is taken: the cautious side."
                    if share is not None
                    else None
                ),
            )
        )
        # The kiln's front and back walls stand alone under the end arches' springings (the
        # walls between chambers have an arch on each side); sliding there (review part 2, #3)
        ends: list[tuple[Face, float]] = []
        if i == 0:
            ends.append(("front", front))
        if i == len(sizes) - 1:
            ends.append(("back", back))
        for face, load in ends:
            step, slid = wall_slide(
                kiln, cold, load, _wall(kiln, face), face,
                f"The {face} wall under {name}",
                thrust_source=f"{reference}: {name}'s cold H and its springing's load",
                sheet_id=f"frame.end-wall-slide-{face}",
            )  # fmt: skip
            working.append(step)
            findings += slid
    findings.append(
        Finding(
            level="info",
            message=(
                "The roof's thrust is carried by the kiln's masonry (thick or battered walls, "
                "buttresses, or earth), as the design says, so no steel frame is sized: up to "
                f"{hottest:.0f} lb per foot of arch, hot. Olsen: brace a chamber kiln's firebox "
                "and front chamber."
            ),
            reference=MASONRY_SOURCE,
        )
    )
    return FrameDesign(
        kind=NO_FRAME, angle=None, angle_leg_in=0, angle_t_in=0, rod=None, rod_d_in=0,
        thrust=f"{hottest:.0f} lb per foot of arch, hot", members=[], working=working,
        findings=findings,
    )  # fmt: skip


# --- Arches of two radii --------------------------------------------------------------------


@dataclass(frozen=True)
class PeakArch:
    """An arch of span ``span`` and rise ``rise`` whose peak stands ``share`` of the span from the
    front springing (roof.peak_at): two circular arcs, each through its springing and level at
    the peak, so the two meet smoothly there. Each half is a circle's arc from its top: its run
    a = r sin φ and its rise ρ = r(1 − cos φ), so r = (a² + ρ²)/2ρ. Any one length unit."""

    span: float
    rise: float
    share: float

    @property
    def front_run(self) -> float:
        return self.span * self.share

    @property
    def back_run(self) -> float:
        return self.span * (1 - self.share)

    def _radius(self, run: float) -> float:
        return (run * run + self.rise * self.rise) / (2 * self.rise)

    @cached_property
    def front_radius(self) -> float:
        return self._radius(self.front_run)

    @cached_property
    def back_radius(self) -> float:
        return self._radius(self.back_run)

    @property
    def front_angle(self) -> float:
        return math.atan2(self.front_run, self.front_radius - self.rise)

    @property
    def back_angle(self) -> float:
        return math.atan2(self.back_run, self.back_radius - self.rise)

    def halves(self) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        """Each half's (radius, angle, run), front then back."""
        return (
            (self.front_radius, self.front_angle, self.front_run),
            (self.back_radius, self.back_angle, self.back_run),
        )

    @property
    def arc_length(self) -> float:
        return sum(r * phi for r, phi, _ in self.halves())

    @property
    def segment_area(self) -> float:
        """The area between the arch and its springline: each half's quarter-segment, the
        sector less the triangle under it, r²φ/2 − a(r − ρ)/2."""
        return sum(r * r * phi / 2 - a * (r - self.rise) / 2 for r, phi, a in self.halves())

    def height(self, u: float) -> float:
        """The inside's height over the springline at ``u`` from the front springing."""
        a = self.front_run
        r, run = (self.front_radius, a - u) if u <= a else (self.back_radius, u - a)
        return self.rise - r + math.sqrt(max(r * r - run * run, 0.0))

    def grown(self, t: float) -> float:
        """The arc's length ``t`` out from the inside, along each half's radius."""
        return sum((r + t) * phi for r, phi, _ in self.halves())

    def thrust(self, weight: float) -> tuple[float, float, float]:
        """The cold thrust H and each springing's vertical load (front, back), its weight
        ``weight`` spread evenly along the arc: a line of thrust through both springings and the
        peak, three-hinged, as vault.THRUST_LINE's. Each half about the peak: V·a = H·ρ + W_h·c,
        c = r(1 − cos φ)/φ the half's centroid in from the peak; and V_f + V_b = W. So
        H = (W − W_f·c_f/a_f − W_b·c_b/a_b) / (ρ(1/a_f + 1/a_b))."""
        total = self.arc_length
        parts = [(weight * r * phi / total, r * (1 - math.cos(phi)) / phi, a)
                 for r, phi, a in self.halves()]  # fmt: skip
        h = (weight - sum(w * c / a for w, c, a in parts)) / (
            self.rise * sum(1 / a for _, _, a in parts)
        )
        front, back = ((h * self.rise + w * c) / a for w, c, a in parts)
        return h, front, back

    def mid_line(self, ring: float, n: int = 200) -> list[tuple[float, float, float, float]]:
        """The ring's mid-line, ``ring``/2 out from the inside, front springing to back: points
        (u along from the front springing, z over the springline, the line's slope angle, the
        share of the arch's length each stands for)."""
        mid = ring / 2
        total = self.arc_length
        pts: list[tuple[float, float, float, float]] = []
        peak = self.front_run
        for which, (r, phi, _) in enumerate(self.halves()):
            for k in range(n):
                ang = phi * (k + 0.5) / n  # from the peak out towards the springing
                du = (r + mid) * math.sin(ang)
                z = self.rise - r + (r + mid) * math.cos(ang)
                # Both halves are measured from the peak, front_run along from the front springing
                u = peak - du if which == 0 else peak + du
                pts.append((u, z, ang, r * phi / n / total))
        return sorted(pts)

    def line_gap(self, ring: float, n: int = 200) -> float:
        """How far a line of thrust strays from the ring's middle, at its worst, square to the
        ring, as a share of the ring: the line three-hinged at the mid-line's two springings and
        its peak, the arch's own weight spread along it (any weight: the line's shape doesn't
        depend on it). At a point u along, the line stands at z = z_A + [(u − u_A)·V_A −
        Σ(u − u_j)·w_j]/H, the loads w_j to its front; H and V_A from the moments about the peak
        of the front half and about the back springing of the whole. Heyman's safe theorem: a
        line within the ring holds; within its middle half (a share of ¼ or less), the ring is at
        least twice the thinnest that holds it, his geometric factor of safety of 2."""
        pts = self.mid_line(ring, n)
        mid = ring / 2
        ends = [(0.0 - mid * math.sin(self.front_angle), -mid * (1 - math.cos(self.front_angle))),
                (self.span + mid * math.sin(self.back_angle),
                 -mid * (1 - math.cos(self.back_angle)))]  # fmt: skip
        (ua, za), (ub, zb) = ends
        uc, zc = self.front_run, self.rise + mid
        left = [(u, w) for u, _, _, w in pts if u < uc]
        # About the peak, the front half: (u_A − u_C)V_A − (z_A − z_C)H = Σ_left (u_j − u_C)w_j
        # About the back springing, the whole: (u_A − u_B)V_A − (z_A − z_B)H = Σ (u_j − u_B)w_j
        a1, b1, c1 = ua - uc, -(za - zc), sum((u - uc) * w for u, w in left)
        a2, b2, c2 = ua - ub, -(za - zb), sum((u - ub) * w for u, _, _, w in pts)
        det = a1 * b2 - a2 * b1
        v_a, h = (c1 * b2 - c2 * b1) / det, (a1 * c2 - a2 * c1) / det
        worst, before, before_x = 0.0, 0.0, 0.0
        for u, z, ang, w in pts:
            line = za + ((u - ua) * v_a - (before * u - before_x)) / h
            worst = max(worst, abs(line - z) * math.cos(ang))
            before += w
            before_x += w * u
        return worst / ring


__all__ = [
    "PeakArch",
    "Taper",
    "check_shell",
    "sized",
    "sizes_of",
    "width_at",
    "widths_of",
]
