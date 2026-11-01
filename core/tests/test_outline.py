"""Shapes as data (outline.py) and the forms the named types stand for (form.py): every example's
form gives the chamber shape.chamber_shape gives, so the named types are shorthands for it."""

import math
from pathlib import Path

import pytest

from kilndesigner import load_design
from kilndesigner.form import form_of
from kilndesigner.outline import (
    Arc,
    Line,
    Outline,
    Polyline,
    Revolved,
    Run,
    SphereDome,
    Station,
    arch_section,
    circle,
    curve_section,
    flat_teardrop,
    half_width,
    moved,
    necked_teardrop,
    offset,
    oval,
    prism,
    rectangle,
    regular_polygon,
    shell_profile,
    teardrop,
)
from kilndesigner.shape import Arch, RoundDome, SailDome, chamber_shape

EXAMPLES = Path(__file__).parents[2] / "examples"
DESIGNS = sorted(EXAMPLES.glob("*.yaml")) + sorted((EXAMPLES / "olsen").glob("*.yaml"))


# Kilns whose form differs from shape.chamber_shape, and why (none: Bidai's and Kyoto's arches,
# more than semicircles, turn past the vertical in both)
DIFFERS: dict[str, str] = dict.fromkeys(
    ("church-skaelskor", "fireworks-edmonton"),
    "crossing vaults: the form is the chamber's own tube; groin.py has the two tubes' union",
)


@pytest.mark.parametrize("path", DESIGNS, ids=lambda p: p.stem)
def test_every_example_has_the_same_chamber_as_a_form(path: Path) -> None:
    kiln = load_design(path)
    form, shape = form_of(kiln), chamber_shape(kiln)
    floor = next(f for f in shape.faces() if f.face == "floor")
    assert form.plan.area == pytest.approx(floor.inside_area, rel=1e-12)
    assert form.open_top == shape.open_top
    # SailDome's volume is summed on a 400 × 400 grid; the form's in polar form
    same = form.volume == pytest.approx(shape.volume, rel=2e-4)
    assert same != (path.stem in DIFFERS), DIFFERS.get(path.stem, "the volumes differ")


def test_an_arch_more_than_a_semicircle() -> None:
    # A semicircle and a little more: its segment is more than half the circle
    section = arch_section(1.0, 0.6)
    radius = (0.25 + 0.36) / 1.2
    assert section.area > math.pi * radius**2 / 2
    assert section.reach(0.0, (0.0, 0.01)) > 0.5  # wider than its span above the springline
    arch = Arch(1.0, 0.6)
    assert arch.half_angle > math.pi / 2
    assert arch.segment_area == pytest.approx(section.area)
    assert arch.half_width == pytest.approx(radius)
    assert arch.arc_length == pytest.approx(2 * radius * (math.pi - math.asin(0.5 / radius)))


def test_a_semicircular_arch() -> None:
    arch = Arch(1.0, 0.5)
    assert arch.radius == pytest.approx(0.5)
    assert arch.half_angle == pytest.approx(math.pi / 2)
    assert arch.segment_area == pytest.approx(math.pi * 0.25 / 2)
    assert arch.half_width == pytest.approx(0.5)
    assert arch.segment_area == pytest.approx(arch_section(1.0, 0.5).area)


@pytest.mark.parametrize("name", ["bidai", "kyoto-climbing"])
def test_kilns_with_arches_over_a_semicircle(name: str) -> None:
    kiln = load_design(EXAMPLES / "olsen" / f"{name}.yaml")
    shape = chamber_shape(kiln)
    assert shape.arch is not None
    assert shape.arch.half_angle > math.pi / 2
    assert shape.volume == pytest.approx(form_of(kiln).volume, rel=1e-9)


def test_lines_and_arcs_make_exact_areas() -> None:
    assert rectangle(2, 3, (5, -1)).area == pytest.approx(6)
    assert rectangle(2, 3).perimeter == pytest.approx(10)
    assert circle(2).area == pytest.approx(math.pi)
    assert circle(2).perimeter == pytest.approx(2 * math.pi)
    hexagon = regular_polygon(6, 1)
    assert hexagon.area == pytest.approx(6 * math.tan(math.pi / 6))
    assert rectangle(2, 4).bounds == pytest.approx((-1, 1, -2, 2))


def test_an_arch_section_is_the_segment_above_the_springline() -> None:
    section = arch_section(1.2, 0.3)
    assert section.area == pytest.approx(Arch(1.2, 0.3).segment_area)
    assert section.farthest() == pytest.approx(0.6)  # the springings
    assert section.reach(math.pi / 2, (0.0, 0.01)) == pytest.approx(0.29)  # the crown


def test_an_oval_is_four_tangent_arcs() -> None:
    o = oval(2.0, 3.0, 0.6)
    x0, x1, y0, y1 = o.bounds
    assert (x1 - x0, y1 - y0) == pytest.approx((2.0, 3.0), abs=1e-4)
    assert o.reach(0) == pytest.approx(1.0)
    assert o.reach(math.pi / 2) == pytest.approx(1.5)
    # The exact area agrees with the polygon through many points on it
    pts = o.points(4000)
    nxt = pts[1:] + pts[:1]
    shoelace = sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(pts, nxt, strict=True)) / 2
    assert o.area == pytest.approx(shoelace, rel=1e-6)
    for bad in ((2.0, 3.0, 1.0), (3.0, 2.0, 0.5), (2.0, 3.0, 0.0)):
        with pytest.raises(ValueError, match="oval"):
            oval(*bad)
    with pytest.raises(ValueError, match="too large"):
        oval(2.0, 2.0, 0.5)


def test_a_teardrop_with_straight_sides() -> None:
    t = teardrop(1.0, 4.0)
    x0, x1, y0, y1 = t.bounds
    assert (x0, x1, y0, y1) == pytest.approx((-1, 1, -1, 3), abs=1e-4)
    # The circle and the kite of the two tangents: πr² less the circle's slice the kite covers
    phi = math.asin(1 / 3)
    kite = 1 * math.sqrt(9 - 1)  # two right triangles, legs r and √(d² − r²)
    assert t.area == pytest.approx(math.pi - (math.pi - 2 * phi) / 2 + kite)
    assert t.reach(math.pi / 2) == pytest.approx(3.0)
    assert t.reach(-math.pi / 2) == pytest.approx(1.0)
    with pytest.raises(ValueError, match="length"):
        teardrop(1.0, 2.0)


def test_a_teardrop_with_curved_sides() -> None:
    straight, curved = teardrop(1.0, 4.0), teardrop(1.0, 4.0, side_radius=6.0)
    assert curved.reach(math.pi / 2) == pytest.approx(3.0)
    assert curved.area > straight.area  # the sides bulge out
    # Very large side arcs come close to the straight sides
    assert teardrop(1.0, 4.0, 1e5).area == pytest.approx(straight.area, rel=1e-4)
    with pytest.raises(ValueError, match="more than"):
        teardrop(1.0, 4.0, 0.5)
    with pytest.raises(ValueError, match="too small"):
        teardrop(1.0, 4.0, 1.5)


def test_a_teardrop_with_a_flat_front() -> None:
    whole = flat_teardrop(2.0, 5.0)  # round all round, centred on its length
    assert whole.bounds == pytest.approx((-1, 1, -2.5, 2.5), abs=1e-4)
    assert whole.area == pytest.approx(teardrop(1.0, 5.0).area)
    cut = flat_teardrop(2.0, 5.0, 1.2, 8.0)
    _, _, y0, y1 = cut.bounds
    assert (y0, y1) == pytest.approx((-2.5, 2.5), abs=1e-6)
    assert half_width(cut, -2.5 + 1e-9) == pytest.approx(0.6)  # the flat front
    assert half_width(cut, -2.5 + 0.8) >= 1.0  # at the round end's centre, or the sides' bulge
    assert half_width(cut, 9.0) == 0.0
    # The cut takes off the circle's segment beyond the chord, 0.8 from its centre
    seg = math.acos(0.8) - 0.8 * 0.6
    assert cut.area == pytest.approx(teardrop(1.0, 5.2, 8.0).area - seg)
    with pytest.raises(ValueError, match="narrower"):
        flat_teardrop(2.0, 5.0, 2.0)
    # Tight sides touch the round end below where a wide front would cut it
    with pytest.raises(ValueError, match="in front of"):
        flat_teardrop(2.0, 2.1, 1.6, 1.3)


def test_an_outline_moved_out() -> None:
    # A rectangle moved out by t: its corners rounded, Steiner's A + P·t + π·t²
    r = rectangle(2.0, 1.0)
    assert offset(r, 0.0) is r
    assert offset(r, 0.25).area == pytest.approx(2 + 6 * 0.25 + math.pi * 0.0625)
    assert offset(r, 0.25).perimeter == pytest.approx(6 + 2 * math.pi * 0.25)
    drop = flat_teardrop(1.0, 3.0, 0.6, 5.0)
    grown = offset(drop, 0.1)
    assert grown.area == pytest.approx(drop.area + drop.perimeter * 0.1 + math.pi * 0.01)
    assert offset(oval(2.0, 3.0, 0.6), 0.5).bounds == pytest.approx((-1.5, 1.5, -2, 2), abs=1e-4)
    with pytest.raises(ValueError, match="points"):
        offset(curve_section([(1.0, 0.0), (0.0, 1.0), (-1.0, 0.0)]), 0.1)
    # An arc turning clockwise (a hollow in the outline) shrinks as the outline grows
    notch = Outline(
        (
            Line((-2.0, -1.0), (2.0, -1.0)),
            Line((2.0, -1.0), (2.0, 1.0)),
            Arc((0.0, 2.0), math.sqrt(5), -math.atan2(1, 2), -(math.pi - 2 * math.atan2(1, 2))),
            Line((-2.0, 1.0), (-2.0, -1.0)),
        )
    )
    grown_notch = offset(notch, 0.1)
    arc = next(s for s in grown_notch.segments if isinstance(s, Arc) and s.radius > 1)
    assert arc.radius == pytest.approx(math.sqrt(5) - 0.1)
    assert moved(circle(1.0), 1.0, 2.0).bounds == pytest.approx((0.5, 1.5, 1.5, 2.5), abs=1e-4)
    poly = moved(Outline((Polyline(((0, 0), (1, 0), (0, 1))), Line((0, 1), (0, 0)))), 1, 1)
    assert poly.area == pytest.approx(0.5)


def test_an_outline_is_closed_anticlockwise_and_not_empty() -> None:
    with pytest.raises(ValueError, match="at least one"):
        Outline(())
    with pytest.raises(ValueError, match="open"):
        Outline((Line((0, 0), (1, 0)), Line((1, 0), (1, 1))))
    square = [(0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0)]  # clockwise
    with pytest.raises(ValueError, match="anticlockwise"):
        Outline(tuple(Line(p, q) for p, q in zip(square, square[1:] + square[:1], strict=True)))


def test_reach_needs_the_centre_inside() -> None:
    with pytest.raises(ValueError, match="inside"):
        rectangle(1, 1).reach(0.0, centre=(5.0, 5.0))
    # A ray along a side's line meets neither it nor (from outside) the arc
    assert Line((0, 0), (1, 0)).hit((0, 0), (1, 0)) is None
    assert Arc((0, 0), 1, 0, 1).hit((5, 5), (1, 0)) is None
    assert Polyline(((2, -1), (2, 1))).hit((0, 0), (0, 1)) is None


def test_a_curve_section_and_its_points() -> None:
    section = curve_section([(1.0, 0.0), (0.0, 1.0), (-1.0, 0.0)])
    assert section.area == pytest.approx(1.0)
    assert section.perimeter == pytest.approx(2 + 2 * math.sqrt(2))
    assert len(section.points()) == 3


def test_a_run_lofts_between_stations() -> None:
    small, big = arch_section(1.0, 0.25), arch_section(1.5, 0.4)
    run = Run((Station(0, small), Station(2, big), Station(3, big)))
    assert run.length == 3
    assert run.volume == pytest.approx((small.area + big.area) + big.area)
    assert prism(small, 4.0).volume == pytest.approx(4 * small.area)
    with pytest.raises(ValueError, match="two or more"):
        Run((Station(0, small),))
    with pytest.raises(ValueError, match="in order"):
        Run((Station(1, small), Station(0, small)))


def test_a_sphere_dome_over_a_rectangle_or_circle() -> None:
    assert SphereDome(rectangle(1.2, 0.9), 0.25).volume == pytest.approx(
        SailDome(1.2, 0.9, 0.25).volume, rel=1e-4
    )
    assert SphereDome(circle(1.5), 0.3).volume == pytest.approx(RoundDome(1.5, 0.3).volume)
    assert SphereDome(circle(1.5), 0.3).radius == pytest.approx(RoundDome(1.5, 0.3).radius)
    # Over a teardrop, from the round end's centre: springing at the point, the farthest reach
    drop = SphereDome(teardrop(1.0, 4.0), 0.5)
    assert drop.radius == pytest.approx((9 + 0.25) / 1.0)
    assert 0 < drop.volume < teardrop(1.0, 4.0).area * 0.5


def _shoelace(points: list[tuple[float, float]]) -> float:
    nxt = points[1:] + points[:1]
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(points, nxt, strict=True)) / 2


def test_a_teardrop_with_a_neck() -> None:
    # Calimpong's: 51½ in, 117 in long, a 39 in front, a 12 in neck 19 in long
    drop = necked_teardrop(51.5, 117, 39, 145, 12, 19, 32)
    x0, x1, y0, y1 = drop.bounds
    assert (x1 - x0, y1 - y0) == pytest.approx((51.5, 117), abs=1e-3)
    assert drop.area == pytest.approx(_shoelace(drop.points(4000)), rel=1e-5)
    # Every join is tangent but the four square corners (front and back)
    for y in (40.0, 45.0, 58.4):
        assert 2 * half_width(drop, y) == pytest.approx(12)
    widths = [2 * half_width(drop, -58.5 + k) for k in range(1, 117)]
    assert max(widths) == pytest.approx(51.5, abs=0.01)
    # The reverse curves bend the other way: arcs turning clockwise
    assert sum(1 for s in drop.segments if isinstance(s, Arc) and s.sweep < 0) == 2
    # Moved out, the reverse curves tighten and the Steiner area still holds
    grown = offset(drop, 9)
    assert grown.area == pytest.approx(drop.area + drop.perimeter * 9 + math.pi * 81, rel=1e-9)
    assert grown.area == pytest.approx(_shoelace(grown.points(4000)), rel=1e-5)
    with pytest.raises(ValueError, match="close up"):
        offset(drop, 40)
    # From the round end it sees the whole outline; from inside the neck the curves hide some
    assert drop.sees_all((0.0, -5.5))
    assert not drop.sees_all((0.0, 50.0))
    assert not drop.sees_all((0.0, 80.0))  # outside it
    # From a point of the outline itself (that point skipped): a rectangle's corner sees it all
    assert rectangle(2.0, 1.0).sees_all((-1.0, -0.5))


@pytest.mark.parametrize(
    ("sizes", "why"),
    [
        ((51.5, 117, 60, 145, 12, 19, 32), "narrower than its widest"),
        ((51.5, 117, 39, 145, 40, 19, 32), "narrower than the flat front"),
        ((51.5, 117, 39, 20, 12, 19, 32), "more than the round end's"),
        ((51.5, 117, 39, 145, 12, 110, 32), "too long"),
        ((51.5, 117, 39, 95, 12, 19, 36), "bulge wider"),
        ((51.5, 117, 39, 145, 12, 19, 400), "don't meet"),
        ((51.5, 60, 39, 145, 12, 19, 3), "don't meet|in front of"),
    ],
)
def test_necks_it_refuses(sizes: tuple[float, ...], why: str) -> None:
    with pytest.raises(ValueError, match=why):
        necked_teardrop(*sizes)


def test_a_revolved_shell() -> None:
    # A whole hemisphere shell, radii 1 to 2, centred on the springline: (2/3)π(2³ − 1³)
    shell = Revolved(tuple(shell_profile(1.0, 2.0, 0.0, 0.0, steps=2000)))
    assert shell.volume == pytest.approx(2 / 3 * math.pi * 7, rel=1e-5)
