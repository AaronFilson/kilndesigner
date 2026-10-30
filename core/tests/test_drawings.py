"""Section drawings and their SVG and DXF: what each roof shape looks like when it is cut.

Expected sizes come from the example design files and the shapes' definitions, worked out here.
"""

import math
from pathlib import Path
from xml.etree import ElementTree

import pytest

from kilndesigner import load_design, parse_design
from kilndesigner.drawings import (
    Dimension,
    Rect,
    View,
    length_text,
    section_views,
    view_svg,
    write_dxf,
)
from kilndesigner.model import Kiln

EXAMPLES = Path(__file__).parents[2] / "examples"
SVG = "{http://www.w3.org/2000/svg}"
IN = 25.4


def _load(name: str) -> Kiln:
    return load_design(EXAMPLES / f"{name}.yaml")


def _variant(name: str, *changes: tuple[str, str]) -> Kiln:
    text = (EXAMPLES / f"{name}.yaml").read_text(encoding="utf-8")
    for old, new in changes:
        assert old in text
        text = text.replace(old, new)
    return parse_design(text)


def _rect(view: View, layer: str) -> Rect:
    (rect,) = [r for r in view.rects if r.layer == layer]
    return rect


def _parts(view: View) -> set[str]:
    return {r.layer for r in view.rects}


@pytest.fixture(scope="module")
def sprung() -> list[View]:
    # 28 in wide, 48 in deep, 40 in to the springline, a 3.75 in rise; 3 in of castable then
    # 2 in of blanket over the arch; walls 4.5 + 2.5 + 1 in
    return section_views(_load("gas-crossdraft"))


@pytest.fixture(scope="module")
def catenary() -> list[View]:
    # 40 in span at the floor, 48 in to the crown, 36 in deep; end walls 4.5 + 4.5 in; the arch
    # 4.5 in of brick then 2 in of blanket
    return section_views(_load("catenary-gas-kiln"))


@pytest.fixture(scope="module")
def dome() -> list[View]:
    # 30 in wide, 36 in deep, 36 in to the springline, an 8 in rise; walls 4.5 + 2.5 + 1 in;
    # 3 in of castable then 2 in of blanket over the dome
    kiln = _load("dome-castable-kiln")
    roof = {**kiln.roof.model_dump(mode="json"), "rise": "8 in"}  # the example rises 9 in
    return section_views(
        Kiln.model_validate({**kiln.model_dump(mode="json", by_alias=True), "roof": roof})
    )


def test_lengths_are_labelled_in_the_designs_units() -> None:
    assert length_text(10.125 * IN, us=True) == "10.1 in"  # three figures under 2 ft
    assert length_text(24 * IN, us=True) == "24 in"
    assert length_text(30.25 * IN, us=True) == "30.25 in"  # four figures from 2 ft up
    assert length_text(571.6, us=False) == "572 mm"


def test_a_box_kiln_is_dimensioned_inside_and_out() -> None:
    front, side, plan = section_views(_load("electric-front-loader"))
    # 22.5 in square and 24 in high inside; 5.5 in walls, a 7 in floor and a 5.5 in roof
    assert [d.text for d in front.dims] == [
        "22.5 in inside",
        "33.5 in outside",
        "24 in inside",
        "36.5 in outside",
    ]
    assert [d.text for d in side.dims] == [d.text for d in front.dims]
    assert [d.text for d in plan.dims] == ["22.5 in inside", "33.5 in outside", "33.5 in outside"]


def test_a_metric_design_is_dimensioned_in_millimetres() -> None:
    kiln = _variant(
        "electric-front-loader",
        ("units: us", "units: metric"),
        ("width: 22.5 in", "width: 600 mm"),
        ("depth: 22.5 in", "depth: 600 mm"),
        ("height: 24 in", "height: 610 mm"),
    )
    front = section_views(kiln)[0]
    # 4.5 in of brick and 1 in of blanket each side: 600 + 2 × 139.7 = 879.4 mm
    assert [d.text for d in front.dims][:3] == [
        "600 mm inside",
        "879 mm outside",
        "610 mm inside",
    ]


def test_elements_are_drawn_on_the_walls_that_carry_them() -> None:
    kiln = _load("electric-front-loader")  # elements in the left, right and back walls
    front, side, _ = section_views(kiln, element_rows=2, coil_mm=12)
    half = 22.5 * IN / 2
    rows = [24 * IN / 4, 24 * IN * 3 / 4]  # the middle of each half of the 24 in height
    # A row on the left wall's inside face, then the right's, at each height
    assert [c.x for c in front.circles] == pytest.approx([-half, half, -half, half])
    assert [c.y for c in front.circles] == pytest.approx([rows[0], rows[0], rows[1], rows[1]])
    # The back wall's inside face, half the depth back
    assert [c.x for c in side.circles] == pytest.approx([half, half])
    assert [c.y for c in side.circles] == pytest.approx(rows)
    assert {c.r for c in front.circles + side.circles} == {6.0}


def test_elements_in_the_front_wall_show_in_the_side_section_only() -> None:
    kiln = _variant(
        "electric-front-loader",
        ("walls: [left, right, back]", "walls: [front]"),
        ("face: front", "face: right"),
    )
    front, side, _ = section_views(kiln, element_rows=3, coil_mm=10)
    assert front.circles == []
    # The front wall's inside face, half the depth forward, at the middle of each third
    assert [c.x for c in side.circles] == pytest.approx([-22.5 * IN / 2] * 3)
    assert [c.y for c in side.circles] == pytest.approx([24 * IN * k / 6 for k in (1, 3, 5)])


def test_a_sprung_arch_across_the_kiln_is_its_ring(sprung: list[View]) -> None:
    front = sprung[0]
    ring = _rect(front, "roof/1-kast-o-lite-30-li-plus")
    assert ring.points
    # The hot face springs from the walls' inside faces at the springline and rises 3.75 in;
    # the ring is 3 in thick at the crown.
    springline, crown = 40 * IN, 43.75 * IN
    for x, z in [(-14 * IN, springline), (14 * IN, springline), (0, crown), (0, crown + 3 * IN)]:
        assert any(math.isclose(px, x, abs_tol=1e-6) and math.isclose(pz, z, abs_tol=1e-6)
                   for px, pz in ring.points), (x, z)  # fmt: skip
    assert ring.y == pytest.approx(springline)
    assert ring.y + ring.h == pytest.approx(crown + 3 * IN)
    # The skewbacks under the arch's feet, drawn as their outlines, from the springline
    skewback = _rect(front, "left/skewback-ifb-jm26")
    assert skewback.points[0] == pytest.approx((-14 * IN, springline))
    assert _rect(front, "right/skewback-ifb-jm26").points[0] == pytest.approx((14 * IN, springline))
    # The end walls' caps are 24 in or more from the cut: not in it
    assert not [p for p in _parts(front) if p.endswith("-arch")]


def test_a_sprung_arch_along_the_kiln_is_a_band_over_the_end_caps(sprung: list[View]) -> None:
    side = sprung[1]
    ring = _rect(side, "roof/1-kast-o-lite-30-li-plus")
    assert ring.points == ()
    # The crown: 3 in of castable from 43.75 in up, the kiln's whole length (48 in inside and
    # 8 in of wall at each end)
    assert (ring.y, ring.h) == pytest.approx((43.75 * IN, 3 * IN))
    assert (ring.x, ring.w) == pytest.approx((-32 * IN, 64 * IN))
    # The back wall's first layer, 4.5 in thick, closes the arch from the springline to the crown
    cap = _rect(side, "back/1-ifb-jm26-arch")
    assert (cap.x, cap.w) == pytest.approx((24 * IN, 4.5 * IN))
    assert (cap.y, cap.h) == pytest.approx((40 * IN, 3.75 * IN))
    # The skewbacks lie along the side walls, away from the middle
    assert not [p for p in _parts(side) if "skewback" in p]


def test_the_plan_of_an_arched_kiln_is_cut_below_the_arch(sprung: list[View]) -> None:
    plan = sprung[2]
    assert {p.split("/")[0] for p in _parts(plan)} == {"left", "right", "door", "back"}
    assert not [p for p in _parts(plan) if "skewback" in p or p.endswith("-arch")]


def _catenary_half_width(span: float, crown: float, z: float) -> float:
    """Half the inside width at height ``z`` of z(x) = crown + a − a·cosh(x / a) with ``span``
    at the floor: ``a`` by bisection, then x = a·acosh((crown + a − z) / a)."""
    lo, hi = span / 100, span * 100
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid * (math.cosh(span / 2 / mid) - 1) > crown:
            lo = mid  # too tight a curve: a is larger
        else:
            hi = mid
    a = (lo + hi) / 2
    return a * math.acosh((crown + a - z) / a)


def test_a_catenary_across_the_kiln_is_its_rings(catenary: list[View]) -> None:
    front = catenary[0]
    # The end walls sit 18 in or more from the middle, so the cut shows the arch and floor
    assert _parts(front) == {
        "arch/1-ifb-jm26",
        "arch/2-kaowool-blanket-8pcf",
        "floor/1-hard-firebrick-kx99",
        "floor/2-ifb-k23",
    }
    ring = _rect(front, "arch/1-ifb-jm26")
    assert ring.points
    assert ring.y == 0
    assert ring.y + ring.h == pytest.approx((48 + 4.5) * IN)
    assert max(z for _, z in ring.points) == pytest.approx((48 + 4.5) * IN)
    assert front.dims[0].text == "40 in inside, at the floor"
    assert (front.dims[0].y1, front.dims[0].y2) == (0, 0)


def test_a_catenary_along_the_kiln_shows_the_end_walls_to_the_crown(
    catenary: list[View],
) -> None:
    side = catenary[1]
    back = _rect(side, "back/1-ifb-jm26")
    assert (back.x, back.w) == pytest.approx((18 * IN, 4.5 * IN))
    assert (back.y, back.h) == pytest.approx((0, 48 * IN), abs=1e-6)
    crown = _rect(side, "arch/1-ifb-jm26")
    assert (crown.y, crown.h) == pytest.approx((48 * IN, 4.5 * IN))
    # The arch runs over the end walls: 36 in plus 9 in at each end
    assert (crown.x, crown.w) == pytest.approx((-27 * IN, 54 * IN))


def test_a_catenarys_plan_cuts_both_legs_and_is_narrower_than_the_floor(
    catenary: list[View],
) -> None:
    plan = catenary[2]
    legs = sorted((r for r in plan.rects if r.layer == "arch/1-ifb-jm26"), key=lambda r: r.x)
    assert len(legs) == 2
    assert legs[0].x + legs[0].w < 0 < legs[1].x
    assert legs[0].x == pytest.approx(-(legs[1].x + legs[1].w))
    inside = 2 * _catenary_half_width(40 * IN, 48 * IN, 24 * IN)
    assert inside < 40 * IN
    dim = plan.dims[0]
    assert dim.x2 - dim.x1 == pytest.approx(inside, rel=1e-6)
    assert dim.text == f"{length_text(inside, us=True)} inside"
    # The end wall's cut, made from its outline, agrees with the curve
    back = _rect(plan, "back/1-ifb-jm26")
    assert back.w == pytest.approx(inside, rel=2e-3)
    assert legs[0].x + legs[0].w == pytest.approx(-inside / 2, rel=2e-3)


def test_a_dome_across_the_kiln(dome: list[View]) -> None:
    front = dome[0]
    # A sphere through the top corners (15 in, 18 in) and 8 in above them at the centre:
    # r = (15² + 18² + 8²) / (2 × 8) = 38.3125 in, its centre 8 - r = -30.3125 in below the
    # springline at 36 in.
    r, centre = (15**2 + 18**2 + 8**2) / 16, 8 - (15**2 + 18**2 + 8**2) / 16
    roof = _rect(front, "roof/1-kast-o-lite-30-li-plus")
    assert any(
        math.isclose(x, 0, abs_tol=1e-6) and math.isclose(z, 44 * IN) for x, z in roof.points
    )
    assert max(z for _, z in roof.points) == pytest.approx(47 * IN)
    assert max(z for _, z in _rect(front, "roof/2-kaowool-blanket-8pcf").points) == (
        pytest.approx(49 * IN)
    )
    # The left wall's top fills up to the sphere: highest at its inside face, 15 in out
    cap = _rect(front, "left/1-ifb-jm26-dome")
    top = 36 + centre + math.sqrt(r * r - 15**2)
    assert max(z for _, z in cap.points) == pytest.approx(top * IN)
    assert min(z for _, z in cap.points) == pytest.approx(36 * IN)
    # The front and back walls, and their tops, are 18 in or more from the cut
    assert not [p for p in _parts(front) if p.startswith(("door/", "back/"))]


def test_a_domes_plan_and_side(dome: list[View]) -> None:
    side, plan = dome[1], dome[2]
    assert {"door/1-ifb-jm26-dome", "back/1-ifb-jm26-dome"} <= _parts(side)
    assert _rect(side, "roof/1-kast-o-lite-30-li-plus").points
    # The dome is all above the springline; the plan is cut at mid-height
    assert not [p for p in _parts(plan) if p.startswith("roof/") or p.endswith("-dome")]


def test_the_svg_draws_rings_as_polygons_and_boxes_as_rects(sprung: list[View]) -> None:
    front = sprung[0]
    root = ElementTree.fromstring(view_svg(front, font=20))
    polygons = list(root.iter(f"{SVG}polygon"))
    rects = list(root.iter(f"{SVG}rect"))
    assert [p.findtext(f"{SVG}title") for p in polygons] == [
        r.layer for r in front.rects if r.points
    ]
    assert [p.findtext(f"{SVG}title") for p in rects] == [
        r.layer for r in front.rects if not r.points
    ]
    ring = next(r for r in front.rects if r.points)
    first = polygons[0].get("points", "").split()
    assert len(first) == len(ring.points)
    # y is flipped: SVG's y runs down
    x, y = ring.points[0]
    assert first[0] == f"{x:.2f},{-y:.2f}"
    labels = [t.text for t in root.iter(f"{SVG}text")]
    assert labels == [d.text for d in front.dims]
    assert {t.get("font-size") for t in root.iter(f"{SVG}text")} == {"20.00"}


def test_dimension_text_is_sized_to_each_view() -> None:
    from kilndesigner.drawings import text_size

    # A squarish view keeps a twentieth of its longer side
    square = View("square", [Rect(0, 0, 1000, 900, (0, 0, 0), "a")], [], [])
    assert text_size(square) == pytest.approx(50.0)
    # A long run's section along it: in scale with its height, never under 1.5 % of its length
    long = View("long", [Rect(0, 0, 12000, 2000, (0, 0, 0), "a")], [], [])
    assert text_size(long) == pytest.approx(0.05 * 3 * 2000)
    assert text_size(long) < 0.05 * 12000
    thin = View("thin", [Rect(0, 0, 36000, 200, (0, 0, 0), "a")], [], [])
    assert text_size(thin) == pytest.approx(0.015 * 36000)
    # The view box holds every dimension line and its text
    long.dims.append(Dimension(0, 0, 12000, 0, 900.0, "12000 mm"))
    root = ElementTree.fromstring(view_svg(long))
    _, vy, _, vh = (float(v) for v in root.get("viewBox", "").split())
    assert -vy - vh <= -900 - 1.5 * text_size(long)


def test_the_dxf_keeps_the_arch_outline(sprung: list[View], tmp_path: Path) -> None:
    from ezdxf.entities.lwpolyline import LWPolyline  # pyright: ignore[reportMissingTypeStubs]
    from ezdxf.filemanagement import readfile  # pyright: ignore[reportMissingTypeStubs]

    write_dxf(sprung, str(tmp_path / "arch.dxf"), us=True)
    doc = readfile(tmp_path / "arch.dxf")
    rings = [
        len(e)
        for e in doc.modelspace().query("LWPOLYLINE")
        if isinstance(e, LWPolyline) and e.dxf.layer == "roof_1-kast-o-lite-30-li-plus"
    ]
    # Across the kiln: the ring's inner and outer arcs, 49 points each; along it: a band
    expected = len(_rect(sprung[0], "roof/1-kast-o-lite-30-li-plus").points)
    assert sorted(rings) == [4, expected]
    assert expected == 98
    titles = [e.dxf.text for e in doc.modelspace().query("TEXT") if e.dxf.layer == "titles"]
    assert titles == [v.title for v in sprung]
