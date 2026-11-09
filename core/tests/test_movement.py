"""The expansion allowance in walls and over a sprung arch, the IFB rating notes and the ¼ in
mortar joint (refractory-movement-and-mortar.md, the sixth round)."""

from __future__ import annotations

from pathlib import Path

import pytest

from kilndesigner.designfile import load_design, parse_design
from kilndesigner.frame import design_frame
from kilndesigner.masonry import plan_masonry
from kilndesigner.model import Kiln
from kilndesigner.movement import expansion, ifb_notes
from kilndesigner.round_masonry import joint_sheet
from kilndesigner.units import Q_

EXAMPLES = Path(__file__).parents[2] / "examples"


def _gas() -> Kiln:
    return load_design(EXAMPLES / "gas-crossdraft.yaml")


def _allowances(kiln: Kiln) -> list[str]:
    return [f.message for f in design_frame(kiln).findings if f.check and "movement." in f.check.id]


def test_each_wall_run_gets_its_growth_and_allowance() -> None:
    kiln = _gas()
    steps, findings = expansion(kiln, "arch frame")
    assert {f.check.id for f in findings if f.check} == {"movement.across", "movement.along"}
    assert all(f.level == "info" and f.check and f.check.status == "pass" for f in findings)
    run = next(f for f in findings if f.check and f.check.id == "movement.along")
    assert run.check is not None
    cells = {c.symbol: c for c in run.check.cells}
    length = cells["L"].value or 0.0
    grown = cells["ΔL"].value or 0.0
    assert grown == pytest.approx(length / 0.3048 * 3 / 32 * 0.0254)
    assert cells["a"].value == pytest.approx(grown / 2)
    names = [s.name for s in steps]
    assert "Expansion allowance, the arch's span" in names
    assert "No joint in the masonry over an arch" in run.message


def test_a_free_standing_kiln_has_no_joints() -> None:
    _, findings = expansion(_gas(), "no frame")
    assert all("Olsen's chamber kilns have no expansion joints" in f.message for f in findings)


def test_past_2400_f_the_growth_is_not_worked_out() -> None:
    kiln = _gas()
    firing = kiln.firing.model_copy(update={"cone": None, "top_temperature": Q_(2450, "degF")})
    kiln = kiln.model_copy(update={"firing": firing})
    steps, findings = expansion(kiln, "arch frame")
    assert findings
    assert all("isn't worked out" in f.message for f in findings)
    assert all(f.check and f.check.status == "warning" for f in findings)
    assert not steps


def test_round_and_catenary_kilns_are_not_covered() -> None:
    assert expansion(load_design(EXAMPLES / "round-electric.yaml"), "x") == ([], [])
    assert expansion(load_design(EXAMPLES / "catenary-gas-kiln.yaml"), "x") == ([], [])


def test_short_ifb_walls_in_a_frame_need_no_joint() -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    messages = _allowances(kiln)
    assert messages
    assert any("needs no joint" in m or "fibre pads" in m for m in messages)


def test_long_ifb_walls_take_olsens_fibre_pads() -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    chamber = kiln.chamber.model_copy(update={"depth": Q_(72, "in")})
    _, findings = expansion(kiln.model_copy(update={"chamber": chamber}), "welded case")
    assert any("past 48 in he joints IFB walls too" in f.message for f in findings)


def test_ifb_on_a_hot_face_shows_its_rating() -> None:
    steps = ifb_notes(load_design(EXAMPLES / "electric-front-loader.yaml"))
    assert steps
    assert all(s.name.startswith("IFB near its rating") for s in steps)
    assert all("below" in s.value for s in steps)


def test_a_joint_past_a_quarter_inch_is_warned() -> None:
    assert joint_sheet("j", 0.5).check().status == "warning"
    assert joint_sheet("j", 0.2).check().status == "pass"


ROUND = """
schema: 1
name: Round test kiln
units: us
firing: {cone: "6"}
chamber: {shape: round, width: 60 in, depth: 60 in, height: 36 in%s}
roof: {type: flat}
lining:
  walls: [{material: firebrick-medium-duty-smithfield, thickness: 4.5 in}]
heat:
  fire:
    fuel: wood
    fireboxes: [{position: under, width: 24 in, length: 48 in, height: 24 in}]
draft: {type: up}
"""


def test_mortar_rings_the_design_states_are_held_to_a_quarter_inch() -> None:
    stated = plan_masonry(parse_design(ROUND % ", rings: mortar")).result.findings
    [warned] = [f for f in stated if f.level == "warning"]
    assert warned.check is not None
    assert warned.check.id == "masonry.joint"
    assert "Beall" in warned.message
    default = plan_masonry(parse_design(ROUND % "")).result.findings
    assert not [f for f in default if f.level == "warning"]
    assert any("Beall gives ¼ in" in f.message for f in default)
