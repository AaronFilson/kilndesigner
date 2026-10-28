"""Catenary arches and domes: their shape, their parts, their heat loss, what holds them, their
ports and their drawings (combustion-and-masonry.md §6.6–6.7)."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pytest

from kilndesigner import load_design
from kilndesigner.drawings import section_views
from kilndesigner.frame import NO_FRAME, design_frame
from kilndesigner.gas import ward_volume
from kilndesigner.geometry import build_model, inside_top, lining_parts
from kilndesigner.hardware import build_hardware, layout
from kilndesigner.library import material
from kilndesigner.model import Kiln
from kilndesigner.report import design_report
from kilndesigner.shape import CatenaryCurve, SailDome, chamber_shape
from kilndesigner.units import parse_quantity, si

EXAMPLES = Path(__file__).parents[2] / "examples"
IN = 25.4


def _catenary() -> Kiln:
    return load_design(EXAMPLES / "catenary-gas-kiln.yaml")


def _dome() -> Kiln:
    return load_design(EXAMPLES / "dome-castable-kiln.yaml")


def _changed(kiln: Kiln, **changes: object) -> Kiln:
    return Kiln.model_validate({**kiln.model_dump(mode="json", by_alias=True), **changes})


def _area(points: list[tuple[float, float]]) -> float:
    """The area inside a closed outline (the shoelace formula)."""
    pairs = zip(points, points[1:] + points[:1], strict=True)
    return abs(sum(x0 * z1 - x1 * z0 for (x0, z0), (x1, z1) in pairs)) / 2


# The curves


def test_a_catenary_meets_the_floor_at_its_span_and_peaks_at_its_height() -> None:
    curve = CatenaryCurve(40, 48)
    assert curve.z(20) == pytest.approx(0, abs=1e-9)
    assert curve.z(-20) == pytest.approx(0, abs=1e-9)
    assert curve.z(0) == pytest.approx(48)
    # Its length and area, in closed form, agree with the curve drawn as points
    assert curve.length(0.0) == pytest.approx(curve.arc_length, rel=1e-5)
    assert _area(curve.offset(0.0, 2000)) == pytest.approx(curve.area, rel=1e-5)


def test_a_catenary_moved_out_stays_that_far_from_the_inside() -> None:
    curve = CatenaryCurve(40, 48)
    for x, z in curve.offset(4.5, 40)[1:-1]:
        nearest = min(math.dist((x, z), p) for p in curve.offset(0.0, 4000))
        assert nearest == pytest.approx(4.5, abs=0.01)
    # A ring's area is its thickness times its length halfway through
    ring = curve.offset(0.0, 2000) + list(reversed(curve.offset(4.5, 2000)))
    assert _area(ring) == pytest.approx(4.5 * curve.length(2.25), rel=1e-3)


def test_a_flat_catenary_meets_the_floor_and_its_layers_stay_parallel() -> None:
    """40 wide and only 5 high. With a at the half span, 20 (cosh 1 − 1) = 10.9 high, so a is
    longer than the half span; and the curve meets the floor at a slant, so a layer on it reaches
    the floor further out than its thickness past the foot."""
    curve = CatenaryCurve(40, 5)
    assert curve.a > 20
    assert curve.z(20) == pytest.approx(0, abs=1e-9)
    assert curve.z(-20) == pytest.approx(0, abs=1e-9)
    assert curve.z(0) == pytest.approx(5)
    assert _area(curve.offset(0.0, 2000)) == pytest.approx(curve.area, rel=1e-5)
    # The inside curve, carried on under the floor past its feet
    xs = np.linspace(-40, 40, 80001)
    inside = np.column_stack([xs, curve.z(0) + curve.a - curve.a * np.cosh(xs / curve.a)])

    def distance(point: tuple[float, float]) -> float:
        return float(np.min(np.hypot(inside[:, 0] - point[0], inside[:, 1] - point[1])))

    layer = curve.offset(4.5, 40)
    for point in layer[1:-1]:
        assert distance(point) == pytest.approx(4.5, abs=1e-3)
    half = curve.half_width(4.5)
    assert half > 20 + 4.5
    assert layer[0] == pytest.approx((-half, 0))
    assert layer[-1] == pytest.approx((half, 0))
    assert distance((half, 0.0)) == pytest.approx(4.5, abs=1e-3)


def test_a_sail_dome_passes_through_the_four_corners() -> None:
    dome = SailDome(28, 48, 6)
    corner = math.hypot(14, 24)
    assert dome.centre + math.sqrt(dome.radius**2 - corner**2) == pytest.approx(0, abs=1e-9)
    assert dome.centre + dome.radius == pytest.approx(6)
    # Over a tiny rise it is nearly flat: its area is the plan's, its volume about half a
    # paraboloid's over the plan
    flat = SailDome(28, 48, 0.01)
    assert flat.area() == pytest.approx(28 * 48, rel=1e-3)
    assert dome.area() > 28 * 48


# The lining's parts


def test_a_catenary_has_no_side_walls_and_its_rings_stand_on_the_floor() -> None:
    kiln = _catenary()
    parts = lining_parts(kiln)
    assert not any(p.wall in ("left", "right") for p in parts)
    rings = [p for p in parts if p.name.startswith("arch/")]
    assert [p.ring for p in rings] == pytest.approx([4.5 * IN, 2 * IN])
    assert all(p.profile is not None and p.lo[2] == 0 for p in rings)
    outline = rings[0].profile
    assert outline is not None
    inside = outline[: len(outline) // 2]  # the inside curve, then the outside back
    assert inside[0] == pytest.approx((-20 * IN, 0))  # the inside meets the floor at the span
    assert max(z for _, z in inside) == pytest.approx(48 * IN)  # and reaches the crown
    assert max(z for _, z in outline) == pytest.approx(52.5 * IN)
    # The rings run from the back wall's outside to the door's; the end walls close the arch
    assert rings[0].lo[1] == pytest.approx(-(18 + 9) * IN)
    assert rings[0].hi[1] == pytest.approx((18 + 9) * IN)
    ends = [p for p in parts if p.wall in ("front", "back")]
    assert {p.name.split("/")[0] for p in ends} == {"door", "back"}
    assert all(p.thickness == pytest.approx(4.5 * IN) for p in ends)
    # The floor runs under the arch's feet
    floor = next(p for p in parts if p.name.startswith("floor/1"))
    assert floor.hi[0] == pytest.approx(rings[-1].hi[0])


def test_a_catenarys_parts_fill_the_lining_exactly() -> None:
    kiln = _catenary()
    parts = lining_parts(kiln)
    curve = CatenaryCurve(40 * IN, 48 * IN)
    length = (36 + 18) * IN
    total = 6.5 * IN
    outer_area = _area(curve.offset(total, 2000))
    floor = 2 * curve.half_width(total) * length * 7 * IN
    end_walls = curve.area * 18 * IN
    rings = (outer_area - curve.area) * length
    assert sum(p.volume for p in parts) == pytest.approx(floor + end_walls + rings, rel=1e-3)


def test_a_dome_caps_every_wall_and_covers_the_whole_kiln() -> None:
    kiln = _dome()
    parts = lining_parts(kiln)
    caps = [p for p in parts if p.cap]
    assert {p.wall for p in caps} == {"left", "right", "front", "back"}
    assert all(p.dome is not None and p.lo[2] == pytest.approx(36 * IN) for p in caps)
    roof = [p for p in parts if p.name.startswith("roof/")]
    assert [p.thickness for p in roof] == pytest.approx([3 * IN, 2 * IN])
    walls = [p for p in parts if p.wall in ("left", "right") and p.dome is None]
    x0 = min(p.lo[0] for p in walls)
    assert roof[0].lo[0] == pytest.approx(x0)  # out to the walls' outside
    assert roof[0].hi[2] == pytest.approx((36 + 8 + 3) * IN)  # the crown, plus the layer


def test_a_domes_parts_fill_the_lining_exactly() -> None:
    kiln = _dome()
    parts = lining_parts(kiln)
    dome = SailDome(30 * IN, 36 * IN, 8 * IN)
    out_w, out_d = (30 + 16) * IN, (36 + 16) * IN
    shell = 5 * IN
    # Everything outside the chamber, up to the outer sphere: a box to the springline, and the
    # sphere moved out by the dome's thickness above it, over the whole kiln
    n = 800
    x, y = np.meshgrid(
        (np.arange(n) + 0.5) / n * out_w - out_w / 2, (np.arange(n) + 0.5) / n * out_d - out_d / 2
    )
    top = dome.centre + np.sqrt(np.maximum((dome.radius + shell) ** 2 - x * x - y * y, 0.0))
    above = float(np.sum(np.maximum(top, 0.0))) * out_w * out_d / n / n
    envelope = out_w * out_d * (36 + 7) * IN + above
    chamber = 30 * IN * 36 * IN * 36 * IN + dome.volume
    assert sum(p.volume for p in parts) == pytest.approx(envelope - chamber, rel=2e-3)


def test_a_steep_dome_caps_only_the_wall_layers_under_its_sphere() -> None:
    """A 23 in rise over 30 × 36 in: the sphere's radius is (549 + 23²) / (2 × 23) = 23.43 in,
    549 in² being the half-diagonal squared. On walls of three 4½ in layers, the third starts
    15 + 9 = 24 in out from the middle at the sides and 18 + 9 = 27 in at the ends: past the
    sphere, so there's nothing above it to fill. The first two layers are under it."""
    four_and_a_half = [
        {"material": m, "thickness": "4.5 in"} for m in ("ifb-jm26", "ifb-k23", "ifb-k23")
    ]
    lining = {**_dome().lining.model_dump(mode="json"), "walls": four_and_a_half}
    kiln = _changed(_dome(), roof={"type": "dome", "rise": "23 in"}, lining=lining)
    dome = SailDome(30 * IN, 36 * IN, 23 * IN)
    assert dome.radius == pytest.approx((549 + 23**2) / (2 * 23) * IN)
    parts = lining_parts(kiln)
    caps = {(p.wall, p.name.split("/")[1].split("-")[0]) for p in parts if p.cap}
    assert caps == {(w, n) for w in ("left", "right", "back", "front") for n in ("1", "2")}
    # The parts still fill the lining exactly: everything outside the chamber, up to the outer
    # sphere (the roof's 5 in moved out), over the whole kiln
    out_w, out_d = (30 + 27) * IN, (36 + 27) * IN
    n = 800
    x, y = np.meshgrid(
        (np.arange(n) + 0.5) / n * out_w - out_w / 2, (np.arange(n) + 0.5) / n * out_d - out_d / 2
    )
    top = dome.centre + np.sqrt(np.maximum((dome.radius + 5 * IN) ** 2 - x * x - y * y, 0.0))
    above = float(np.sum(np.maximum(top, 0.0))) * out_w * out_d / n / n
    envelope = out_w * out_d * (36 + 7) * IN + above
    chamber = 30 * IN * 36 * IN * 36 * IN + dome.volume
    assert sum(p.volume for p in parts) == pytest.approx(envelope - chamber, rel=2e-3)


# The chamber, heat loss and burners


def test_a_catenary_has_four_faces_and_wards_volume() -> None:
    kiln = _catenary()
    shape = chamber_shape(kiln)
    assert [f.face for f in shape.faces()] == ["back", "front", "floor", "roof"]
    curve = CatenaryCurve(si(kiln.chamber.width, "m"), si(kiln.chamber.height, "m"))
    assert shape.volume == pytest.approx(curve.area * si(kiln.chamber.depth, "m"))
    roof = shape.faces()[-1]
    assert roof.orientation == "vertical"
    assert roof.area_at(0.0) == pytest.approx(curve.length(0) * si(kiln.chamber.depth, "m"))
    assert roof.area_at(0.1) > roof.area_at(0.0)
    volume, formula = ward_volume(kiln)
    assert volume == pytest.approx(
        si(kiln.chamber.depth, "m") * 4 / 3 * si(kiln.chamber.height, "m")
        * si(kiln.chamber.width, "m") / 2
    )  # fmt: skip
    assert "4/3" in formula
    report = design_report(kiln)
    assert len(report.heat_loss.faces) == 4
    assert any("upright wall" in f.message for f in report.findings)


def test_a_domes_walls_rise_under_it_and_its_volume_counts_it() -> None:
    kiln = _dome()
    shape = chamber_shape(kiln)
    faces = {f.face: f for f in shape.faces()}
    w, d, h = (si(getattr(kiln.chamber, n), "m") for n in ("width", "depth", "height"))
    assert faces["left"].inside_area > d * h
    assert faces["front"].inside_area > w * h
    assert shape.volume == pytest.approx(w * d * h + SailDome(w, d, 8 * IN / 1000).volume)
    _, formula = ward_volume(kiln)
    assert "Ward gives no formula for a dome" in formula
    gas = design_report(kiln).gas
    assert gas is not None
    assert gas.chimney_height is not None
    assert "(" in gas.chimney_height  # the rise counts in the inside height


# What holds them


def test_a_catenarys_feet_push_out_with_the_chains_tension() -> None:
    kiln = _catenary()
    frame = design_frame(kiln)
    assert frame.kind == NO_FRAME
    assert frame.members == []
    curve = CatenaryCurve(40 / 12, 48 / 12)
    # JM 26 at its library density, 4.5 in, and 8 pcf blanket, 2 in
    rho = si(parse_quantity(material("ifb-jm26").density), "lb/ft**3")
    w = rho * 4.5 / 12 + 8 * 2 / 12
    assert frame.thrust == f"{w * curve.a:.0f} lb per foot of kiln at each foot"
    assert any(f.level == "warning" and "pushes out" in f.message for f in frame.findings)
    hw = build_hardware(kiln, frame, design_report(kiln).gas)
    assert not any(p.name.startswith("frame/") for p in hw.pieces)


def test_no_frame_is_designed_for_a_dome() -> None:
    frame = design_frame(_dome())
    assert frame.kind == NO_FRAME
    assert any("no source gives how hard" in f.message for f in frame.findings)


# What is refused


def test_a_catenary_is_refused_side_walls_and_elements() -> None:
    kiln = _catenary()
    with pytest.raises(ValueError, match="can't go in the left wall"):
        _changed(kiln, loading={"type": "door", "face": "left"})
    with pytest.raises(ValueError, match="can't go in the right wall"):
        _changed(kiln, draft={"type": "cross", "flue_wall": "right"})
    electric = {"supply": {"voltage": "240 V", "breaker": "60 A"}, "walls": ["back"]}
    heat = {**kiln.heat.model_dump(mode="json"), "electric": electric}
    with pytest.raises(ValueError, match="elements in a catenary kiln"):
        _changed(kiln, heat=heat)


def test_a_dome_that_would_bulge_past_its_walls_is_refused() -> None:
    with pytest.raises(ValueError, match=r"less than half the chamber's diagonal, 23\.4 in"):
        _changed(_dome(), roof={"type": "dome", "rise": "24 in"})


# Ports


def test_ports_fit_under_the_curves() -> None:
    kiln = _catenary()
    # The end wall is the catenary's shape; there are no side walls to put a port in
    assert inside_top(kiln, "front", 0) == pytest.approx(48 * IN)
    assert inside_top(kiln, "front", 19 * IN) < 10 * IN
    assert inside_top(kiln, "left", 0) == 0
    report = design_report(kiln)
    hw = build_hardware(kiln, report.frame, report.gas)
    assert {p.name for p in hw.ports if p.kind == "burner"} == {"port/burner-1", "port/burner-2"}
    shown = layout(kiln, hw)
    assert shown["walls"]["left"]["top"][12][1] == 0  # type: ignore[index]
    high = _changed(
        kiln,
        heat={
            **kiln.heat.model_dump(mode="json"),
            "gas": {
                **kiln.heat.gas.model_dump(mode="json"),  # type: ignore[union-attr]
                "burners": {"places": [{"wall": "front", "across": "17 in", "up": "12 in"}]},
            },
        },
    )
    report = design_report(high)
    hw = build_hardware(high, report.frame, report.gas)
    assert any("goes above the top of the front wall's inside" in f.message for f in hw.findings)

    dome = _dome()
    assert inside_top(dome, "left", 0) > 36 * IN  # every wall rises under a dome
    assert inside_top(dome, "front", 0) > 36 * IN
    assert inside_top(dome, "front", 15 * IN) == pytest.approx(36 * IN, abs=0.5)


# Drawings


def test_the_sections_cut_through_the_curves() -> None:
    front, side, plan = section_views(_catenary())
    rings = [r for r in front.rects if r.layer.startswith("arch/")]
    assert len(rings) == 2
    assert all(r.points for r in rings)  # drawn as the curve
    # Along the kiln, the arch is cut at its crown; across it at mid-height, at both legs
    crown = [r for r in side.rects if r.layer.startswith("arch/1")]
    assert len(crown) == 1
    assert crown[0].y == pytest.approx(48 * IN, abs=1)
    assert len([r for r in plan.rects if r.layer.startswith("arch/1")]) == 2
    assert any("at the floor" in dim.text for dim in front.dims)

    front, side, _ = section_views(_dome())
    shells = [r for r in front.rects if r.layer.startswith("roof/")]
    assert len(shells) == 2
    assert shells[0].y + shells[0].h == pytest.approx((36 + 8 + 3) * IN, abs=2)
    assert any(r.layer.endswith("-dome") for r in side.rects)  # the end walls' tops


@pytest.mark.geometry
@pytest.mark.parametrize("load", [_catenary, _dome], ids=["catenary", "dome"])
def test_the_solids_match_their_parts(load) -> None:  # type: ignore[no-untyped-def]
    kiln = load()
    parts = lining_parts(kiln)
    model = build_model(kiln)
    for part, solid in zip(parts, model.children, strict=True):
        assert solid.volume == pytest.approx(part.volume, rel=3e-3), part.name
