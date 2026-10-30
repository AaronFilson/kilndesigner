"""Kilns other than a single box or round chamber, laid out in brick: open tops on boxes, chambers
in a row (stepped up a slope or level), single chambers on a slope."""

import json
import math
from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.drawings import section_views
from kilndesigner.geometry import Part, lining_parts, not_drawn, write_model
from kilndesigner.masonry import plan_masonry
from kilndesigner.model import Kiln
from kilndesigner.plans import build_plans
from kilndesigner.report import design_report
from kilndesigner.run_parts import run_layout
from kilndesigner.units import si

ROOT = Path(__file__).parents[2]
EXAMPLES = ROOT / "examples"
TEMPLATES = ROOT / "core" / "src" / "kilndesigner" / "data" / "templates"


def _with(path: Path, **chamber: object) -> Kiln:
    kiln = load_design(path)
    document = kiln.model_dump(mode="json", by_alias=True)
    roof = chamber.pop("roof", None)
    if roof is not None:
        document["roof"] = roof
    document["chamber"].update(chamber)
    return Kiln.model_validate(document)


def open_box() -> Kiln:
    """Ninodaguia's open-topped wood kiln, built square, its walls whole bricks thick."""
    kiln = _with(EXAMPLES / "olsen" / "ninodaguia.yaml", shape="box")
    document = kiln.model_dump(mode="json", by_alias=True)
    document["lining"]["walls"][0]["thickness"] = "13.5 inch"
    return Kiln.model_validate(document)


def test_an_open_box_is_laid_out_with_no_roof() -> None:
    kiln = open_box()
    assert not_drawn(kiln) is None
    parts = lining_parts(kiln)
    assert parts
    assert not [p for p in parts if p.wall == "roof"]
    masonry = plan_masonry(kiln)
    assert masonry.layers
    assert not [p for p in masonry.layers if p.part.wall == "roof"]
    report = design_report(kiln)
    assert report.bom is not None
    assert any("bricks" in line.needed for line in report.bom.lines)


def test_an_open_box_has_plans(tmp_path: Path) -> None:
    kiln = open_box()
    plans = build_plans(kiln, design_report(kiln), dxf_path=tmp_path / "s.dxf")
    assert plans.pdf.startswith(b"%PDF")
    assert (tmp_path / "s.dxf").exists()


@pytest.mark.geometry
def test_an_open_box_has_a_model(tmp_path: Path) -> None:
    kiln = open_box()
    written = write_model(kiln, design_report(kiln), tmp_path)
    assert written["gltf"].stat().st_size > 1000


DESIGNS = sorted(EXAMPLES.rglob("*.yaml")) + sorted(TEMPLATES.glob("*.yaml"))
IN_A_ROW = [p for p in DESIGNS if load_design(p).chamber.chambers > 1]


def _name(p: Path) -> str:
    return f"{p.parent.name}/{p.stem}"


def test_there_are_chambers_in_a_row_level_and_stepped() -> None:
    slopes = {load_design(p).chamber.slope is not None for p in IN_A_ROW}
    assert slopes == {True, False}


def _lining(kiln: Kiln) -> list[Part]:
    """The kiln's own lining, its fireboxes left out."""
    return [p for p in lining_parts(kiln) if not p.name.startswith("firebox-")]


def _overlap(a: Part, b: Part) -> float:
    sizes = [min(a.hi[k], b.hi[k]) - max(a.lo[k], b.lo[k]) for k in range(3)]
    return math.prod(sizes) if all(s > 1e-6 for s in sizes) else 0.0


@pytest.mark.parametrize("path", IN_A_ROW, ids=_name)
def test_chambers_in_a_row_are_laid_out_in_brick(path: Path) -> None:
    kiln = load_design(path)
    assert not_drawn(kiln) is None
    parts = lining_parts(kiln)
    assert len({p.name for p in parts}) == len(parts)
    blocks = [p for p in parts if p.profile is None and p.dome is None and p.arch is None]
    for k, a in enumerate(blocks):
        for b in blocks[k + 1 :]:
            assert _overlap(a, b) == 0.0, (a.name, b.name)
    masonry = plan_masonry(kiln)
    assert masonry.result.quantities
    report = design_report(kiln)
    assert report.bom is not None
    assert any("stand in a row" in f.message for f in report.findings)


def test_each_chambers_floor_steps_up_the_slope() -> None:
    kiln = load_design(EXAMPLES / "olsen" / "kawaii.yaml")
    run = run_layout(kiln)
    assert run.step == pytest.approx(run.pitch * math.tan(math.radians(13.2)))
    floors = {p.chamber: p.hi[2] for p in lining_parts(kiln) if p.name.startswith("floor/1-")}
    assert floors == {i + 1: pytest.approx(i * run.step) for i in range(4)}
    # Each chamber's arch spans along the draft, over its depth
    rings = [p for p in _lining(kiln) if p.wall == "roof"]
    assert len(rings) == 4
    assert all(p.across for p in rings)
    assert all(p.hi[1] - p.lo[1] <= run.depth + 2 * run.between + 1e-6 for p in rings)


def test_a_level_row_runs_its_floor_and_side_walls_the_whole_length() -> None:
    kiln = load_design(TEMPLATES / "tunnel.yaml")
    run = run_layout(kiln)
    parts = lining_parts(kiln)
    floors = [p for p in parts if p.wall == "floor" and not p.name.startswith("firebox-")]
    assert len(floors) == len(kiln.lining.walls)  # the floor takes the walls' layers
    assert floors[0].length_y == pytest.approx(run.length + 2 * run.between)
    assert len({p.chamber for p in parts if p.name.startswith("division/")}) == run.chambers - 1


def test_a_short_flat_arch_along_the_draft_is_counted_in_arch_shapes() -> None:
    kiln = _with(TEMPLATES / "tunnel.yaml", roof={"type": "sprung_arch", "rise": "20 in"})
    document = kiln.model_dump(mode="json", by_alias=True)
    document["lining"]["roof"] = [{"material": "ifb-k26", "thickness": "4.5 inch"}]
    kiln = Kiln.model_validate(document)
    findings = plan_masonry(kiln).result.findings
    assert any("Arch bricks" in f.message and " arch bricks" in f.message for f in findings)


def test_domes_and_flat_roofs_cover_chambers_in_a_row() -> None:
    hollyweird = load_design(EXAMPLES / "olsen" / "hollyweird.yaml")
    domes = [p for p in _lining(hollyweird) if p.wall == "roof"]
    assert {p.chamber for p in domes} == {1, 2}
    flat = _with(EXAMPLES / "olsen" / "kawaii.yaml", roof={"type": "flat"})
    assert len([p for p in _lining(flat) if p.wall == "roof"]) == 4
    assert plan_masonry(flat).layers


def test_a_catenary_over_level_chambers_in_a_row_is_one_vault() -> None:
    kiln = _with(TEMPLATES / "tunnel.yaml", roof={"type": "catenary_arch"})
    assert not_drawn(kiln) is None
    parts = lining_parts(kiln)
    run = run_layout(kiln)
    divisions = [p for p in parts if p.name.startswith("division/")]
    assert {p.chamber for p in divisions} == set(range(1, run.chambers))
    assert all(p.profile is not None for p in divisions)  # closing the catenary
    rings = [p for p in parts if p.name.startswith("arch/")]
    assert rings[0].length_y == pytest.approx(run.length + 2 * run.between)
    assert plan_masonry(kiln).result.quantities


def test_a_catenary_over_chambers_stepped_up_a_slope_isnt_laid_out() -> None:
    kiln = _with(EXAMPLES / "olsen" / "kawaii.yaml", roof={"type": "catenary_arch"})
    assert "no source here says how one chamber's catenary meets" in (not_drawn(kiln) or "")


@pytest.mark.parametrize(
    "path", [EXAMPLES / "olsen" / "kawaii.yaml", TEMPLATES / "tunnel.yaml"], ids=_name
)
def test_chambers_in_a_row_have_plans(path: Path, tmp_path: Path) -> None:
    kiln = load_design(path)
    plans = build_plans(kiln, design_report(kiln), dxf_path=tmp_path / "s.dxf")
    assert plans.pdf.startswith(b"%PDF")
    assert [d for d in plans.drawings if d.kind == "course plan"]


SLOPED = [
    p
    for p in DESIGNS
    if (k := load_design(p)).chamber.chambers == 1 and k.chamber.slope is not None
]


def test_there_are_single_chambers_on_a_slope() -> None:
    assert len(SLOPED) >= 5


@pytest.mark.parametrize("path", SLOPED, ids=_name)
def test_a_single_chamber_on_a_slope_is_laid_out_up_it(path: Path) -> None:
    kiln = load_design(path)
    assert not_drawn(kiln) is None
    parts = lining_parts(kiln)
    slope = math.radians(si(kiln.chamber.slope, "degree"))  # type: ignore[arg-type]
    assert all(p.tilt == pytest.approx(slope) for p in parts)
    report = design_report(kiln)
    assert report.bom is not None
    assert any("laid out along its" in f.message for f in report.findings)


def test_a_tilted_part_rises_from_the_front_foot() -> None:
    kiln = load_design(EXAMPLES / "olsen" / "anagama-hole.yaml")
    floor = next(p for p in lining_parts(kiln) if p.wall == "floor")
    assert floor.tilted(floor.pivot, 0.0) == (floor.pivot, 0.0)
    y, z = floor.tilted(floor.pivot + 1000.0, 0.0)
    assert z == pytest.approx(1000.0 * math.sin(floor.tilt))
    assert y == pytest.approx(floor.pivot + 1000.0 * math.cos(floor.tilt))


def test_a_sloped_kiln_is_drawn_up_its_slope(tmp_path: Path) -> None:
    kiln = load_design(EXAMPLES / "olsen" / "anagama-hole.yaml")
    views = section_views(kiln)
    side = views[1]
    assert "slope" in side.title
    assert all(r.points for r in side.rects)
    _, y0, _, y1 = side.bounds()
    level = section_views(_with(EXAMPLES / "olsen" / "anagama-hole.yaml", slope=None))[1]
    assert y1 - y0 > level.bounds()[3] - level.bounds()[1]
    plans = build_plans(kiln, design_report(kiln), dxf_path=tmp_path / "s.dxf")
    assert [d for d in plans.drawings if d.kind == "course plan"]


@pytest.mark.geometry
@pytest.mark.parametrize("path", SLOPED, ids=_name)
def test_a_single_chamber_on_a_slope_has_a_model(path: Path, tmp_path: Path) -> None:
    kiln = load_design(path)
    written = write_model(kiln, design_report(kiln), tmp_path)
    parts = json.loads(written["parts"].read_text(encoding="utf-8"))
    assert {p.name for p in lining_parts(kiln)} <= set(parts)


@pytest.mark.geometry
@pytest.mark.parametrize("path", IN_A_ROW, ids=_name)
def test_chambers_in_a_row_have_a_model(path: Path, tmp_path: Path) -> None:
    kiln = load_design(path)
    written = write_model(kiln, design_report(kiln), tmp_path)
    parts = json.loads(written["parts"].read_text(encoding="utf-8"))
    assert {p.name for p in lining_parts(kiln)} <= set(parts)


def test_the_layout_tells_the_viewer_the_run_steps() -> None:
    from kilndesigner.geometry import brick_layout
    from kilndesigner.hardware import build_hardware

    for path, stepped in (
        (EXAMPLES / "olsen" / "kawaii.yaml", True),
        (TEMPLATES / "tunnel.yaml", False),
    ):
        kiln = load_design(path)
        report = design_report(kiln)
        hardware = build_hardware(kiln, report.frame, report.gas, report.fire)
        run = brick_layout(kiln, hardware)["run"]
        assert isinstance(run, dict)
        assert run["step"] == pytest.approx(run_layout(kiln).step)  # pyright: ignore[reportUnknownArgumentType]
        assert (run["step"] > 0) is stepped
