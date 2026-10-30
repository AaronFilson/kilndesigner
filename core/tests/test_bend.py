"""A run that bends in plan, laid out in brick: counted along each layer's own path round the
bend, drawn straightened, and swept round the bend in the model."""

import math
from dataclasses import replace
from pathlib import Path

import pytest

from kilndesigner.bend import developed
from kilndesigner.designfile import parse_design
from kilndesigner.drawings import section_views
from kilndesigner.geometry import lining_parts, not_drawn, write_model
from kilndesigner.masonry import plan_masonry
from kilndesigner.massing import place, run_of
from kilndesigner.model import Kiln
from kilndesigner.plans import build_plans
from kilndesigner.report import design_report

EXAMPLES = Path(__file__).parents[2] / "examples"
ANAGAMA = (EXAMPLES / "olsen" / "anagama-hole.yaml").read_text(encoding="utf-8")
KAWAII = (EXAMPLES / "olsen" / "kawaii.yaml").read_text(encoding="utf-8")


def _bent(text: str, degrees: float, level: bool = True) -> Kiln:
    if level:
        return parse_design(text.replace("  slope: 25 degree\n", f"  bend: {degrees} degree\n"))
    return parse_design(text.replace("  slope:", f"  bend: {degrees} degree\n  slope:", 1))


def test_a_bent_run_is_laid_out_in_brick() -> None:
    kiln = _bent(ANAGAMA, 60)
    assert not_drawn(kiln) is None
    masonry = plan_masonry(kiln)
    assert masonry.layers
    assert any("bends 60°" in f.message for f in masonry.result.findings)
    report = design_report(kiln)
    assert report.bom is not None


def test_each_layer_is_counted_at_its_own_length_round_the_bend() -> None:
    kiln = _bent(ANAGAMA, 60)
    run = run_of(kiln)
    straight = {p.name: p for p in lining_parts(kiln)}
    counted = {p.name: p for p in developed(kiln, lining_parts(kiln))}
    left = next(n for n in straight if n.startswith("left/"))
    right = next(n for n in straight if n.startswith("right/"))
    # The left wall is on the inside of the bend: shorter; the right, outside: longer
    assert counted[left].length_y < straight[left].length_y
    assert counted[right].length_y > straight[right].length_y
    x = (straight[right].lo[0] + straight[right].hi[0]) / 2
    grown = counted[right].length_y - straight[right].length_y
    assert grown == pytest.approx(run.length * x / run.radius)
    # The floor's centroid is on the centre line: Pappus, no change
    floor = next(n for n in straight if n.startswith("floor/"))
    assert counted[floor].length_y == pytest.approx(straight[floor].length_y)
    # The end walls are across the run: no change
    back = next(n for n in straight if n.startswith("back/"))
    assert counted[back].hi == straight[back].hi


def test_a_bent_run_has_plans_drawn_straightened(tmp_path: Path) -> None:
    kiln = _bent(ANAGAMA, 45)
    views = section_views(kiln)
    assert all("straightened" in v.title for v in views)
    plans = build_plans(kiln, design_report(kiln), dxf_path=tmp_path / "s.dxf")
    assert plans.pdf.startswith(b"%PDF")


@pytest.mark.geometry
@pytest.mark.parametrize("level", [True, False], ids=["level", "sloping"])
def test_a_bent_runs_model_follows_the_bend(level: bool, tmp_path: Path) -> None:
    import json

    kiln = _bent(ANAGAMA, 90, level)
    written = write_model(kiln, design_report(kiln), tmp_path)
    index = json.loads(written["parts"].read_text("utf-8"))
    assert any(k.startswith("left/") for k in index)  # part by part, not shells
    assert not any(k.startswith("shell/") for k in index)


@pytest.mark.geometry
def test_the_swept_wall_ends_where_the_run_ends() -> None:
    from kilndesigner.bend import bent_solid

    kiln = _bent(ANAGAMA, 90)
    run = run_of(kiln)
    right = next(p for p in lining_parts(kiln) if p.name.startswith("right/"))
    solid = bent_solid(right, run)
    assert solid is not None
    bb = solid.bounding_box()
    # The run turns a quarter to the left: the end of the right wall's inside face, at the run's
    # end, lies where the shells put it
    end = place(replace(run, slope=0.0), (right.lo[0], -run.depth / 2 + run.length, 0.0))
    assert end[0] + 1.0 >= bb.min.X
    assert end[1] - 1.0 <= bb.max.Y
    assert math.isfinite(solid.volume)


def test_chambers_in_a_row_can_bend() -> None:
    kiln = parse_design(KAWAII.replace("  slope:", "  bend: 20 degree\n  slope:", 1))
    assert not_drawn(kiln) is None
    assert plan_masonry(kiln).layers
