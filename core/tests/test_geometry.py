import itertools
import json
import math
from pathlib import Path

import pytest

from kilndesigner import load_design, parse_design
from kilndesigner.geometry import (
    LAYOUT,
    Part,
    build_model,
    element_runs,
    export_model,
    lining_parts,
    part_index,
    write_model,
)
from kilndesigner.hardware import build_hardware, layout
from kilndesigner.model import Kiln
from kilndesigner.report import design_report

EXAMPLES = Path(__file__).parents[2] / "examples"
IN = 25.4
JM26 = "Morgan Thermal Ceramics JM 26 insulating firebrick"


def _changed(name: str, **changes: object) -> Kiln:
    """An example with parts of its design replaced: ``lining__door=[...]`` sets lining.door."""
    document = load_design(EXAMPLES / name).model_dump(mode="json", by_alias=True)
    for path, value in changes.items():
        *parents, last = path.split("__")
        target = document
        for key in parents:
            target = target.setdefault(key, {})
        target[last] = value
    return Kiln.model_validate(document)


def _overlap(
    a: tuple[tuple[float, ...], tuple[float, ...]], b: tuple[tuple[float, ...], tuple[float, ...]]
) -> float:
    """The volume two boxes share."""
    return math.prod(max(0.0, min(a[1][i], b[1][i]) - max(a[0][i], b[0][i])) for i in range(3))


@pytest.fixture(scope="module")
def kiln():  # type: ignore[no-untyped-def]
    return load_design(EXAMPLES / "electric-front-loader.yaml")


def test_lining_parts_fill_the_shell_without_overlap(kiln) -> None:  # type: ignore[no-untyped-def]
    parts = lining_parts(kiln)
    lo = [min(p.lo[i] for p in parts) for i in range(3)]
    hi = [max(p.hi[i] for p in parts) for i in range(3)]
    outside = (hi[0] - lo[0]) * (hi[1] - lo[1]) * (hi[2] - lo[2])
    inside = (22.5 * IN) * (22.5 * IN) * (24 * IN)
    # Boxes that tile the shell exactly: their volumes add up to outside minus inside.
    assert sum(p.volume for p in parts) == pytest.approx(outside - inside, rel=1e-9)
    # 22.5 in + 2 × 5.5 in walls
    assert hi[0] - lo[0] == pytest.approx(33.5 * IN)
    # 24 in + 7 in floor + 5.5 in roof
    assert hi[2] - lo[2] == pytest.approx(36.5 * IN)


def test_parts_are_named_by_face_and_layer(kiln) -> None:  # type: ignore[no-untyped-def]
    names = [p.name for p in lining_parts(kiln)]
    assert "door/1-ifb-jm26" in names
    assert "floor/2-ifb-k23" in names
    assert len(names) == len(set(names)) == 12


def _tiles(parts: list[Part], inside: float) -> None:
    """The parts fill the box round them, less the chamber, and no two overlap."""
    lo = [min(p.lo[i] for p in parts) for i in range(3)]
    hi = [max(p.hi[i] for p in parts) for i in range(3)]
    outside = math.prod(h - lo_ for lo_, h in zip(lo, hi, strict=True))
    assert sum(p.volume for p in parts) == pytest.approx(outside - inside, rel=1e-9)
    for a, b in itertools.combinations(parts, 2):
        assert _overlap((a.lo, a.hi), (b.lo, b.hi)) == pytest.approx(0, abs=1e-3), (a.name, b.name)


FRONT_LOADER_INSIDE = (22.5 * IN) * (22.5 * IN) * (24 * IN)


def test_a_door_thicker_than_the_walls_wraps_the_side_walls() -> None:
    """An 8 in door of three layers on the front loader's 5½ in walls: its third layer runs the
    whole width of the kiln, across the ends of the side walls."""
    door = [
        {"material": "ifb-jm26", "thickness": "4.5 in"},
        {"material": "ifb-k23", "thickness": "2.5 in"},
        {"material": "kaowool-blanket-8pcf", "thickness": "1 in"},
    ]
    parts = lining_parts(_changed("electric-front-loader.yaml", lining__door=door))
    _tiles(parts, FRONT_LOADER_INSIDE)
    by_name = {p.name: p for p in parts}
    outer = by_name["door/3-kaowool-blanket-8pcf"]
    assert outer.lo[0] == pytest.approx(-(22.5 / 2 + 5.5) * IN)
    assert outer.hi[0] == pytest.approx((22.5 / 2 + 5.5) * IN)
    assert outer.lo[1] == pytest.approx(-(22.5 / 2 + 8) * IN)
    # The side walls' outer layer stops at the door's second layer
    assert by_name["left/2-kaowool-blanket-8pcf"].lo[1] == pytest.approx(-(22.5 / 2 + 7) * IN)
    assert by_name["back/2-kaowool-blanket-8pcf"].hi[1] == pytest.approx((22.5 / 2 + 5.5) * IN)


def test_a_door_thinner_than_the_walls_fits_between_them() -> None:
    """A 4½ in door of one layer: the side walls' blanket runs out to the door's outside."""
    door = [{"material": "ifb-jm26", "thickness": "4.5 in"}]
    parts = lining_parts(_changed("electric-front-loader.yaml", lining__door=door))
    _tiles(parts, FRONT_LOADER_INSIDE)
    assert [p.name for p in parts if p.name.startswith("door/")] == ["door/1-ifb-jm26"]
    left = next(p for p in parts if p.name == "left/2-kaowool-blanket-8pcf")
    assert left.lo[1] == pytest.approx(-(22.5 / 2 + 4.5) * IN)


def test_element_runs_follow_the_element_walls(kiln) -> None:  # type: ignore[no-untyped-def]
    runs = element_runs(kiln, 3, 10.0)
    assert len(runs) == 3
    # left, back, right: four corners, three straight runs
    assert len(runs[0].path) == 4
    assert runs[0].path[0][2] == pytest.approx(24 * IN / 6)


def test_no_element_runs_without_elements_or_rows(kiln: Kiln) -> None:
    assert element_runs(load_design(EXAMPLES / "gas-crossdraft.yaml"), 3, 10.0) == []
    assert element_runs(kiln, 0, 10.0) == []


def _arched():  # type: ignore[no-untyped-def]
    text = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    return parse_design(text.replace("type: flat", "type: sprung_arch\n  rise: 3 in"))


def test_arched_roof_parts() -> None:
    parts = lining_parts(_arched())
    roof = [p for p in parts if p.name.startswith("roof/")]
    caps = [p for p in parts if p.cap]
    assert len(roof) == 2
    assert len(caps) == 4  # two layers at each end
    inner = roof[0]
    assert inner.arch is not None
    # The arch's hot face meets the walls' inside faces at the springline.
    a = inner.arch
    half_span = a.radius * math.sin(a.half_angle)
    assert half_span == pytest.approx(22.5 * IN / 2)
    assert a.centre_z + a.radius * math.cos(a.half_angle) == pytest.approx(24 * IN)
    assert a.centre_z + a.radius == pytest.approx(27 * IN)  # 3 in rise


def test_the_arch_springs_from_skewbacks_across_the_whole_wall() -> None:
    skewbacks = {p.wall: p for p in lining_parts(_arched()) if p.profile is not None}
    assert set(skewbacks) == {"left", "right"}
    right, left = skewbacks["right"], skewbacks["left"]
    assert right.profile is not None
    assert right.profile[0] == pytest.approx((22.5 * IN / 2, 24 * IN))  # at the springline
    assert right.hi[0] == pytest.approx((22.5 / 2 + 5.5) * IN)  # out to the wall's outer face
    assert right.material == "ifb-jm26"  # the wall's brick, not its blanket
    assert left.lo[0] == pytest.approx(-right.hi[0])


def test_a_skewback_under_an_arch_wider_than_its_wall_ends_on_the_arch_radius() -> None:
    """2½ in walls under 6 in of roof: the arch's outer corner, 6 in × sin 30° = 3 in out past
    the springline, is past the wall's outer face, so the skewback is a triangle cut along the
    arch's radius."""
    kiln = _changed(
        "gas-crossdraft.yaml",
        lining__walls=[{"material": "ifb-jm26", "thickness": "2.5 in"}],
        lining__roof=[
            {"material": "kast-o-lite-30-li-plus", "thickness": "3 in"},
            {"material": "kaowool-blanket-8pcf", "thickness": "3 in"},
        ],
    )
    skewbacks = {p.wall: p for p in lining_parts(kiln) if p.profile is not None}
    assert set(skewbacks) == {"left", "right"}
    right = skewbacks["right"]
    assert right.profile is not None
    springline, cut, foot = right.profile
    assert springline == pytest.approx((14 * IN, 40 * IN))
    assert cut[0] == pytest.approx(16.5 * IN)  # out to the wall's outer face
    assert foot == pytest.approx((16.5 * IN, 40 * IN))
    # The cut lies on the radius through the springline: R = (14² + 3.75²) / (2 × 3.75) in,
    # centred R − 3¾ in below the crown
    radius = (14**2 + 3.75**2) / (2 * 3.75)
    centre = (40 + 3.75 - radius) * IN
    assert (cut[1] - centre) / cut[0] == pytest.approx((40 * IN - centre) / (14 * IN))
    left = skewbacks["left"].profile
    assert left is not None
    assert [c for point in left for c in point] == pytest.approx(
        [c for x, z in right.profile for c in (-x, z)]
    )


def test_walls_of_fibre_alone_give_an_arch_nothing_to_spring_from() -> None:
    kiln = _changed(
        "gas-crossdraft.yaml",
        lining__walls=[{"material": "kaowool-blanket-8pcf", "thickness": "4 in"}],
    )
    parts = lining_parts(kiln)
    assert not [p for p in parts if p.profile is not None]
    assert [p.name for p in parts if p.arch is not None and not p.cap] == [
        "roof/1-kast-o-lite-30-li-plus",
        "roof/2-kaowool-blanket-8pcf",
    ]


def test_the_part_index_says_what_every_part_and_piece_is(kiln: Kiln) -> None:
    report = design_report(kiln)
    hw = build_hardware(kiln, report.frame, report.gas)
    index = part_index(kiln, report, hw)
    assert report.electric is not None
    elements = report.electric.elements
    assert elements is not None
    assert set(index) == (
        {p.name for p in lining_parts(kiln)}
        | {f"element/{i + 1}" for i in range(elements.count)}
        | {p.name for p in hw.pieces}
    )
    # JM 26 is drawn in (0.93, 0.89, 0.78): #ede3c7
    assert index["door/1-ifb-jm26"] == {
        "title": "Door, layer 1 from the inside",
        "detail": f"{JM26}, 4½ in thick",
        "kind": "Insulating firebrick",
        "colour": "#ede3c7",
    }
    assert index[f"element/{elements.count}"] == {
        "title": f"Element {elements.count} of {elements.count}",
        "detail": (
            f"{elements.gauge} {report.electric.alloy}, {elements.length_each} of wire, "
            f"{elements.power_each}"
        ),
        "kind": "Elements",
        "colour": "#8c8c94",
    }
    case = next(p for p in hw.pieces if p.name == "case/left")
    assert index["case/left"] == {
        "title": "Case, left",
        "detail": case.detail,
        "kind": "Steel",
        "colour": "#4c525c",
    }


def test_skewbacks_and_arch_caps_are_indexed_without_a_thickness() -> None:
    """They're cut to the arch, so no one thickness says what they are."""
    kiln = load_design(EXAMPLES / "gas-crossdraft.yaml")
    index = part_index(kiln, design_report(kiln))
    assert set(index) == {p.name for p in lining_parts(kiln)}  # no hardware given, no elements
    assert index["left/skewback-ifb-jm26"]["title"] == "Left wall, the skewback and fill on top"
    assert index["left/skewback-ifb-jm26"]["detail"] == JM26
    assert index["back/1-ifb-jm26-arch"]["title"] == (
        "Back wall, layer 1 from the inside, above the springline"
    )
    assert index["back/1-ifb-jm26-arch"]["detail"] == JM26
    assert index["door/1-ifb-jm26"]["detail"] == f"{JM26}, 4½ in thick"


@pytest.mark.geometry
def test_arch_solids_match_their_parts() -> None:
    kiln = _arched()
    parts = lining_parts(kiln)
    model = build_model(kiln)
    for part, solid in zip(parts, model.children, strict=True):
        assert solid.volume == pytest.approx(part.volume, rel=2e-3), part.name
        box = solid.bounding_box()
        assert pytest.approx(part.lo[1], abs=0.5) == box.min.Y, part.name
        assert pytest.approx(part.hi[1], abs=0.5) == box.max.Y, part.name


@pytest.mark.geometry
def test_model_builds_and_exports(kiln, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    model = build_model(kiln, element_runs(kiln, 2, 10.0))
    labels = [c.label for c in model.children]
    assert "element/2" in labels
    lining_volume = sum(p.volume for p in lining_parts(kiln))
    lining = [c for c in model.children if not c.label.startswith("element")]
    assert sum(c.volume for c in lining) == pytest.approx(lining_volume, rel=1e-6)
    files = export_model(model, tmp_path)
    assert files["step"].stat().st_size > 1000
    assert files["gltf"].read_bytes()[:4] == b"glTF"


@pytest.mark.geometry
def test_a_build_writes_the_model_what_each_part_is_and_the_ports(
    kiln: Kiln, tmp_path: Path
) -> None:
    report = design_report(kiln)
    files = write_model(kiln, report, tmp_path)
    assert set(files) == {"step", "gltf", "parts", "layout"}
    assert files["step"].stat().st_size > 1000
    assert files["gltf"].read_bytes()[:4] == b"glTF"
    hw = build_hardware(kiln, report.frame, report.gas)
    assert json.loads(files["parts"].read_text("utf-8")) == part_index(kiln, report, hw)
    assert files["layout"] == tmp_path / LAYOUT
    shown = json.loads(json.dumps(layout(kiln, hw)))
    assert json.loads(files["layout"].read_text("utf-8")) == shown


@pytest.mark.geometry
def test_ports_cut_the_lining_and_chimney_but_not_the_burners() -> None:
    """The gas cross-draft under a flat roof, so every lining part is a box: each solid is its
    part less what the openings take out of it. Its Ransome B4 ports are round, 4¾ in, and lie
    wholly inside the front wall, the door; the flue, spy holes, chimney inlet and damper are
    rectangles."""
    kiln = _changed(
        "gas-crossdraft.yaml",
        roof={"type": "flat"},
        heat__gas__burners={"model": "Ransome B4", "count": 2},
    )
    report = design_report(kiln)
    hw = build_hardware(kiln, report.frame, report.gas)
    solids = {c.label: c for c in build_model(kiln, hardware=hw).children}
    parts = lining_parts(kiln)
    assert list(solids) == [p.name for p in parts] + [p.name for p in hw.pieces]

    def removed(lo: tuple[float, float, float], hi: tuple[float, float, float]) -> float:
        total = 0.0
        for o in hw.openings:
            if o.round_axis is None:
                total += _overlap((lo, hi), o.box)
            elif _overlap((lo, hi), o.box) > 0:
                ax = o.round_axis
                depth = min(hi[ax], o.box[1][ax]) - max(lo[ax], o.box[0][ax])
                across = min(o.box[1][i] - o.box[0][i] for i in range(3) if i != ax)
                total += math.pi * (across / 2) ** 2 * depth
        return total

    for p in parts:
        assert solids[p.name].volume == pytest.approx(p.volume - removed(p.lo, p.hi), rel=1e-6)
    # The ports went through the door (the burners and the spy holes) and the back (the flue)
    for name in ("door/1-ifb-jm26", "back/1-ifb-jm26"):
        part = next(p for p in parts if p.name == name)
        assert removed(part.lo, part.hi) > 0, name

    stack = next(p for p in hw.pieces if p.name == "chimney/stack")
    cut = sum(removed(lo, hi) for lo, hi in stack.boxes)
    assert cut > 0  # by the inlet and the damper slot
    assert solids["chimney/stack"].volume == pytest.approx(stack.volume - cut, rel=1e-6)
    # A burner reaches back into its port, but isn't cut by it
    ports = [o for o in hw.openings if o.name.startswith("port/burner-")]
    assert len(ports) == 2
    for port in ports:
        burner = next(p for p in hw.pieces if p.name == f"burner/{port.name.rsplit('-', 1)[1]}")
        [c] = burner.cylinders
        reach = c.centre[1] + c.length / 2  # it fires along y, out of the front wall
        assert reach > port.box[0][1]
        assert solids[burner.name].volume == pytest.approx(math.pi * c.radius**2 * c.length)
