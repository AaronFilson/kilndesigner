"""The 3D model of kilns whose bricks aren't laid out yet: round, open, chambered, sloped, bent."""

import json
import math
from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest
from pydantic import ValidationError

from kilndesigner.designfile import load_design, parse_design
from kilndesigner.geometry import GeometryNotSupportedError, not_drawn, write_model
from kilndesigner.hardware import PortSpot, build_hardware
from kilndesigner.massing import (
    Cell,
    MassingError,
    Run,
    cells,
    check_bend,
    massing_index,
    massing_layout,
    place,
    port_axis,
    run_of,
    turn_at,
)
from kilndesigner.model import Kiln
from kilndesigner.report import design_report

EXAMPLES = Path(__file__).parents[2] / "examples"
ALL = sorted(EXAMPLES.rglob("*.yaml"))
ANAGAMA = (EXAMPLES / "olsen" / "anagama-hole.yaml").read_text(encoding="utf-8")
KYOTO = (EXAMPLES / "olsen" / "kyoto-climbing.yaml").read_text(encoding="utf-8")
BOTTLE = (EXAMPLES / "olsen" / "breda-bottle.yaml").read_text(encoding="utf-8")


def _bent(text: str, degrees: float) -> str:
    return text.replace("  slope:", f"  bend: {degrees} degree\n  slope:", 1)


def test_a_bend_is_an_angle_up_to_a_half_turn_and_not_on_a_round_kiln() -> None:
    assert parse_design(_bent(ANAGAMA, 90)).chamber.bend is not None
    for bad in ("200 degree", "3 in"):
        with pytest.raises(ValidationError):
            parse_design(ANAGAMA.replace("  slope:", f"  bend: {bad}\n  slope:", 1))
    with pytest.raises(ValidationError, match="no run to bend"):
        parse_design(BOTTLE.replace("  shape: round", "  shape: round\n  bend: 10 degree", 1))


def test_every_shape_the_bricks_cant_be_laid_for_says_it_is_drawn() -> None:
    for text in (ANAGAMA, KYOTO, BOTTLE, _bent(ANAGAMA, 30)):
        assert "drawn, but not yet laid out" in (not_drawn(parse_design(text)) or "")
    level = ANAGAMA.replace("  slope: 25 degree\n", "  bend: 30 degree\n")
    assert "bent run" in (not_drawn(parse_design(level)) or "")


def test_a_straight_level_run_leaves_points_alone() -> None:
    run = run_of(parse_design(KYOTO))
    flat = replace(run, slope=0.0)
    assert place(flat, (1.0, 2.0, 3.0)) == (1.0, 2.0, 3.0)
    assert turn_at(flat, 500.0) == 0.0
    assert flat.radius == math.inf


def test_a_climbing_run_rises_with_its_slope_from_its_front_face() -> None:
    run = run_of(parse_design(KYOTO))
    front = -run.depth / 2
    _, _, z = place(run, (0.0, front + 1000.0, 0.0))
    assert z == pytest.approx(1000.0 * math.sin(run.slope))
    assert run.chamber_centre(2) == pytest.approx(2 * (run.depth + run.between))
    assert run.length == pytest.approx(10 * run.depth + 9 * run.between)


def test_a_bent_run_follows_its_arc_and_carries_on_straight_beyond_it() -> None:
    run = run_of(parse_design(_bent(ANAGAMA, 90)))
    flat = replace(run, slope=0.0)
    front = -run.depth / 2
    rho = run.radius
    end = place(flat, (0.0, front + run.length, 0.0))
    assert end[0] == pytest.approx(-rho)
    assert end[1] == pytest.approx(front + rho)
    beyond = place(flat, (0.0, front + run.length + 100.0, 0.0))
    assert beyond[0] == pytest.approx(-rho - 100.0)
    assert turn_at(flat, front + run.length * 2) == pytest.approx(math.pi / 2)
    assert turn_at(flat, front - 10) == 0.0


def test_too_tight_a_bend_is_refused() -> None:
    run = run_of(parse_design(_bent(ANAGAMA, 180)))
    tight = replace(run, depth=100.0)
    with pytest.raises(MassingError, match="tighter than the kiln is wide"):
        check_bend(tight)


def test_chambers_in_a_row_have_arches_along_the_draft_and_troughs_for_their_fireboxes() -> None:
    kiln = parse_design(KYOTO)
    inside = cells(kiln, run_of(kiln))
    boxes = [c for c in inside if c.kind == "box"]
    pits = [c for c in inside if c.kind == "pit"]
    assert len(boxes) == 10
    assert all(c.along for c in boxes)
    assert len(pits) == 10
    assert all(p.z1 == 0.0 for p in pits)


def _beyond(c: Cell, run: Run, position: str) -> bool:
    return {
        "front": c.y < -run.depth / 2,
        "back": c.y > run.depth / 2,
        "under": c.z1 < 0,
        "left": c.x < -run.width / 2,
        "right": c.x > run.width / 2,
    }[position]


@pytest.mark.parametrize("position", ["front", "back", "under", "left", "right"])
def test_fireboxes_go_against_their_wall_or_under_the_floor(position: str) -> None:
    text = ANAGAMA.replace("position: front", f"position: {position}")
    kiln = parse_design(text)
    run = run_of(kiln)
    pits = [c for c in cells(kiln, run) if c.kind == "pit"]
    assert pits
    assert all(_beyond(c, run, position) for c in pits)


def test_a_bent_single_chamber_is_drawn_in_eight_pieces() -> None:
    kiln = parse_design(_bent(ANAGAMA, 45))
    assert sum(c.kind == "box" for c in cells(kiln, run_of(kiln))) == 8


def _spot(wall: str, across: float = 0.0) -> PortSpot:
    return PortSpot("spy-1", "Spy hole 1", "spy", wall, across, 10.0, 2.0, 2.0, True)  # type: ignore[arg-type]


def test_ports_on_a_round_kiln_go_round_its_curve() -> None:
    kiln = parse_design(BOTTLE)
    run = run_of(kiln)
    radius = run.width / 2
    inner, outer = port_axis(kiln, run, _spot("front"))
    assert inner[0] == pytest.approx(0.0, abs=1e-6)
    assert inner[1] == pytest.approx(-radius)
    # A quarter of the way round, to the right facing the front wall: the right side
    inner, _ = port_axis(kiln, run, _spot("front", radius * math.pi / 2 / 25.4))
    assert inner[0] == pytest.approx(radius)
    assert inner[1] == pytest.approx(0.0, abs=1e-6)
    assert math.hypot(outer[0], outer[1]) > radius


@pytest.mark.parametrize("wall", ["front", "back", "left", "right"])
def test_ports_on_a_box_go_through_their_wall(wall: str) -> None:
    kiln = parse_design(KYOTO)
    run = run_of(kiln)
    inner, outer = port_axis(kiln, run, _spot(wall))
    assert inner != outer
    assert inner[2] == outer[2] == pytest.approx(254.0)


def test_the_layout_says_how_the_run_bends_climbs_and_curves() -> None:
    kiln = parse_design(BOTTLE)
    report = design_report(kiln)
    hw = build_hardware(kiln, report.frame, report.gas, report.fire)
    run = cast("dict[str, object]", massing_layout(kiln, hw)["run"])
    assert run["round"] is True
    assert run["radius"] == pytest.approx(si_mm(kiln.chamber.width) / 2)
    index = massing_index(kiln, hw)
    assert next(iter(index.values()))["title"] == "Lining, layer 1"
    assert massing_index(kiln, None).keys() <= index.keys()


def si_mm(q: object) -> float:
    from kilndesigner.units import si

    return si(q, "mm")  # type: ignore[arg-type]


def test_a_cell_is_a_plain_value() -> None:
    assert Cell("box", 0.0, 1.0) == Cell("box", 0.0, 1.0)


@pytest.mark.geometry
@pytest.mark.parametrize("path", ALL, ids=lambda p: f"{p.parent.name}/{p.stem}")
def test_every_example_builds_a_gltf(path: Path, tmp_path: Path) -> None:
    kiln = load_design(path)
    written = write_model(kiln, design_report(kiln), tmp_path)
    assert written["gltf"].stat().st_size > 1000
    layout = json.loads(written["layout"].read_text(encoding="utf-8"))
    assert set(layout["walls"]) == {"front", "back", "left", "right"}
    parts = json.loads(written["parts"].read_text(encoding="utf-8"))
    assert parts


def _roofed(text: str, roof: dict[str, object] | None) -> Kiln:
    kiln = parse_design(text)
    if roof is None:
        return kiln
    document = kiln.model_dump(mode="json", by_alias=True)
    document["roof"] = roof
    return Kiln.model_validate(document)


@pytest.mark.geometry
@pytest.mark.parametrize(
    ("text", "roof"),
    [
        (_bent(ANAGAMA, 60), None),
        (BOTTLE, {"type": "open"}),
        (BOTTLE, {"type": "flat"}),
        (KYOTO, {"type": "dome", "rise": "10 in"}),
        (KYOTO, {"type": "catenary_arch"}),
        (KYOTO, {"type": "flat"}),
    ],
    ids=["bent", "round-open", "round-flat", "chambers-dome", "chambers-catenary", "flat"],
)
def test_every_roof_on_every_run_is_drawn(
    text: str, roof: dict[str, object] | None, tmp_path: Path
) -> None:
    kiln = _roofed(text, roof)
    written = write_model(kiln, design_report(kiln), tmp_path)
    assert written["gltf"].exists()


@pytest.mark.geometry
def test_too_tight_a_bend_builds_no_model(tmp_path: Path) -> None:
    kiln = parse_design(_bent(ANAGAMA.replace("depth: ", "depth: 1 in #"), 180))
    with pytest.raises(GeometryNotSupportedError, match="tighter"):
        write_model(kiln, design_report(kiln), tmp_path)
