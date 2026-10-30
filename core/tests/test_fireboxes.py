"""Fireboxes laid out in brick: against a wall, under the floor, and troughs one to a chamber."""

from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.firebox_parts import firebox_boxes, grates, openings
from kilndesigner.geometry import lining_parts, not_drawn, write_model
from kilndesigner.masonry import plan_masonry
from kilndesigner.model import Kiln
from kilndesigner.plans import build_plans
from kilndesigner.report import design_report

ROOT = Path(__file__).parents[2]
EXAMPLES = ROOT / "examples"
TEMPLATES = ROOT / "core" / "src" / "kilndesigner" / "data" / "templates"
IN = 25.4
FIRED = [
    p
    for p in sorted(EXAMPLES.rglob("*.yaml")) + sorted(TEMPLATES.glob("*.yaml"))
    if load_design(p).heat.fire is not None
]


def _template(name: str) -> Kiln:
    return load_design(TEMPLATES / f"{name}.yaml")


def _firebox_parts(kiln: Kiln) -> list[str]:
    return [p.name for p in lining_parts(kiln) if p.name.startswith("firebox-")]


@pytest.mark.parametrize("path", FIRED, ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_every_fired_design_lays_its_fireboxes_in_brick(path: Path) -> None:
    kiln = load_design(path)
    if not_drawn(kiln) is not None:
        pytest.skip("drawn as shells")
    names = _firebox_parts(kiln)
    boxes = firebox_boxes(kiln)
    assert boxes
    # Each firebox but a trough shallow enough to sit in the floor has walls of its own
    walled = {n.split("/")[0] for n in names}
    for b in boxes:
        if not b.trough:
            assert f"firebox-{b.index}" in walled
    masonry = plan_masonry(kiln)
    # Laid in courses, or said why not (a lining that isn't whole bricks, say)
    planned = any(p.part.name.startswith("firebox-") for p in masonry.layers)
    said = any(f.message.startswith("Firebox ") for f in masonry.result.findings)
    bricks = [p for p in lining_parts(kiln) if p.name.startswith("firebox-") and "brick" in p.kind]
    assert planned or said or not bricks
    assert any("Fireboxes are built of the kiln's own layers" in f.message
               for f in masonry.result.findings)  # fmt: skip
    names_all = [p.name for p in lining_parts(kiln)]
    assert len(names_all) == len(set(names_all))


def test_under_floor_fireboxes_have_their_own_walls_and_inlets_through_the_floor() -> None:
    kiln = _template("wood-fast-fire")
    boxes = firebox_boxes(kiln)
    assert len(boxes) == 2
    a, b = boxes
    # Packed so each has its own walls: no overlap
    walls = sum(x.thickness.to("mm").magnitude for x in kiln.lining.walls)
    assert b.lo[0] - a.hi[0] >= 2 * walls - 1e-6
    assert a.hi[2] < 0  # under the floor
    inlets = [o for o in openings(kiln) if o.name.endswith("/inlet")]
    assert len(inlets) == 2
    assert all(o.hi[2] > 0 for o in inlets)  # up through the floor
    parts = lining_parts(kiln)
    # The floor is cut round the inlets
    assert any(p.name.startswith("floor/") and p.name[-2] == "-" for p in parts)
    # No roof of their own: the chamber floor roofs them
    assert not [p for p in parts if p.name.startswith("firebox-") and p.face == "roof"]
    # The grate: ¾ in bars ¾ in apart across a 12 in grate, eight of them
    g1, _ = grates(kiln)
    assert g1.bars == 8
    assert g1.length == pytest.approx(24 * IN)


def test_a_firebox_against_the_front_wall_cuts_its_mouth_through_it() -> None:
    kiln = _template("groundhog")
    (box,) = firebox_boxes(kiln)
    assert box.kiln_side == "+y"
    assert box.hi[1] < -kiln.chamber.depth.to("mm").magnitude / 2
    parts = lining_parts(kiln)
    fb = [p for p in parts if p.name.startswith("firebox-1/")]
    assert {p.face for p in fb} == {"left", "right", "front", "floor", "roof"}
    mouth = [o for o in openings(kiln) if o.name.endswith("/mouth")]
    assert len(mouth) == 1
    front = [
        p
        for p in parts
        if p.face == "front" and not p.name.startswith("firebox") and p.arch is None
    ]
    # The front wall's courses are cut round the mouth, so their brick no longer fills it; its
    # caps under the arch are cut in the model, and counted by volume
    for p in front:
        lo, hi = mouth[0].lo, mouth[0].hi
        inside = all(lo[i] < (p.lo[i] + p.hi[i]) / 2 < hi[i] for i in range(3))
        assert not inside


def test_inlet_flues_and_stoke_holes_are_cut() -> None:
    kiln = load_design(EXAMPLES / "olsen" / "ellington-new-hog.yaml")
    holes = openings(kiln)
    assert len([o for o in holes if o.name.endswith("/inlet")]) == 3
    stoke = [o for o in holes if o.name.endswith("/stoke-hole")]
    assert len(stoke) == 1
    assert stoke[0].hi[0] - stoke[0].lo[0] == pytest.approx(13.5 * IN)


def test_troughs_one_to_a_chamber() -> None:
    kiln = _template("climbing")
    boxes = firebox_boxes(kiln)
    assert len(boxes) == kiln.chamber.chambers
    assert all(b.trough for b in boxes)
    assert [b.chamber for b in boxes] == list(range(1, kiln.chamber.chambers + 1))
    floors = [p for p in lining_parts(kiln) if p.name.startswith("floor/")]
    # Each chamber's floor is cut for its trough
    assert any(p.name.endswith("-a") for p in floors)


def test_a_round_kiln_counts_its_firebox_brick() -> None:
    kiln = _template("bottle")
    assert _firebox_parts(kiln)
    masonry = plan_masonry(kiln)
    assert any(p.part.name.startswith("firebox-") for p in masonry.layers)


def test_side_fireboxes_stand_beside_the_walls() -> None:
    kiln = _template("coal")
    left, right = firebox_boxes(kiln)
    w = kiln.chamber.width.to("mm").magnitude
    assert left.hi[0] < -w / 2
    assert right.lo[0] > w / 2


def test_grate_bars_are_in_the_bill_of_materials() -> None:
    report = design_report(_template("wood-fast-fire"))
    assert report.bom is not None
    assert any(line.item.startswith("Grate bars") for line in report.bom.lines)


def test_fireboxes_are_in_the_plans(tmp_path: Path) -> None:
    kiln = _template("wood-fast-fire")
    plans = build_plans(kiln, design_report(kiln), dxf_path=tmp_path / "s.dxf")
    assert plans.pdf.startswith(b"%PDF")


def test_walls_between_chambers_have_olsens_flue_holes() -> None:
    from kilndesigner.run_parts import FLUE_HEIGHT, flue_holes, flue_rows

    kiln = _template("climbing")
    rows = flue_rows(kiln)
    assert len(rows) == kiln.chamber.chambers - 1
    w = kiln.chamber.width.to("inch").magnitude
    # 4½ in flues with 9 in separators across the chamber (p.96, p.45)
    assert rows[0].count == int((w + 9) // 13.5)
    assert all(r.top - r.bottom <= FLUE_HEIGHT + 1e-6 for r in rows)
    holes = flue_holes(kiln)
    divisions = [p for p in lining_parts(kiln) if p.name.startswith("division/")]
    for p in divisions:  # no wall's brick fills a flue hole
        for h in holes:
            assert not all(h.lo[i] < (p.lo[i] + p.hi[i]) / 2 < h.hi[i] for i in range(3))
    notes = " ".join(f.message for f in plan_masonry(kiln).result.findings)
    assert "flue holes 4½ in wide and 9 in tall" in notes


def test_floor_ports_and_roof_flues_are_noted_in_the_masonry() -> None:
    kiln = _template("bottle")
    notes = " ".join(f.message for f in plan_masonry(kiln).result.findings)
    assert "The flue through the roof is cut in the 3D model" in notes


@pytest.mark.geometry
def test_a_round_updrafts_roof_flue_is_cut_in_the_model() -> None:
    from kilndesigner.geometry import _holes  # pyright: ignore[reportPrivateUsage]
    from kilndesigner.hardware import build_hardware

    kiln = _template("bottle")
    report = design_report(kiln)
    hardware = build_hardware(kiln, report.frame, report.gas, report.fire)
    h = kiln.chamber.height.to("mm").magnitude
    assert any(lo[2] >= h - 30 for lo, _, _ in _holes(kiln, hardware))


@pytest.mark.geometry
@pytest.mark.parametrize("name", ["wood-fast-fire", "groundhog", "bottle", "coal"])
def test_fireboxes_are_in_the_model(name: str, tmp_path: Path) -> None:
    import json

    kiln = _template(name)
    written = write_model(kiln, design_report(kiln), tmp_path)
    index = json.loads(written["parts"].read_text("utf-8"))
    assert any(k.startswith("firebox-") for k in index)
