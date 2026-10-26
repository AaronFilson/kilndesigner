"""The hardware: frame, door or car, ports, burners, chimney and spy holes, placed on the kiln."""

from __future__ import annotations

import math
from pathlib import Path
from typing import cast

import pytest

from kilndesigner import load_design
from kilndesigner.geometry import lining_parts
from kilndesigner.hardware import MM, Hardware, build_hardware
from kilndesigner.model import Face, Kiln
from kilndesigner.report import Report, design_report

EXAMPLES = Path(__file__).parents[2] / "examples"


def _hardware(name: str) -> tuple[Hardware, tuple[Kiln, Report]]:
    kiln = load_design(EXAMPLES / name)
    report = design_report(kiln)
    return build_hardware(kiln, report.frame, report.gas), (kiln, report)


@pytest.mark.parametrize("name", sorted(p.name for p in EXAMPLES.glob("*.yaml")))
def test_every_piece_and_opening_is_a_real_solid(name: str) -> None:
    hw, _ = _hardware(name)
    for piece in hw.pieces:
        assert piece.boxes or piece.cylinders, piece.name
        for lo, hi in piece.boxes:
            assert all(h > lo_ for lo_, h in zip(lo, hi, strict=True)), piece.name
        for c in piece.cylinders:
            assert c.radius > 0, piece.name
            assert c.length > 0, piece.name
    for opening in hw.openings:
        lo, hi = opening.box
        assert all(h > lo_ for lo_, h in zip(lo, hi, strict=True)), opening.name
    assert len({p.name for p in hw.pieces}) == len(hw.pieces)


def test_the_gas_kiln_has_its_burners_flue_chimney_and_spy_holes() -> None:
    hw, (_, report) = _hardware("pnw-hybrid-crossdraft.yaml")
    gas = report.gas
    assert gas is not None
    assert gas.burners is not None
    assert gas.chimney_height is not None
    names = {o.name for o in hw.openings}
    assert {f"port/burner-{i + 1}" for i in range(gas.burners.count)} <= names
    assert {"port/flue", "port/damper", "port/spy-1", "port/spy-2", "port/spy-3"} <= names
    assert len([p for p in hw.pieces if p.name.startswith("burner/")]) == gas.burners.count
    # The chimney's inside is at least the flue's area (Rhodes) and it reaches the height found
    stack = next(p for p in hw.pieces if p.name == "chimney/stack")
    top = max(hi[2] for _, hi in stack.boxes) / MM
    assert top == pytest.approx(float(gas.chimney_height.split("(")[1].split()[0]))
    xs = sorted({v for lo, hi in stack.boxes for v in (lo[0], hi[0])})
    ys = sorted({v for lo, hi in stack.boxes for v in (lo[1], hi[1])})
    inside = (xs[-2] - xs[1]) * (ys[-2] - ys[1]) / MM**2
    assert inside >= float(gas.flue_area.split()[0])
    assert hw.chimney_bricks > 0


def test_ports_go_through_their_walls() -> None:
    hw, (kiln, _) = _hardware("pnw-hybrid-crossdraft.yaml")
    parts = lining_parts(kiln)
    for opening in hw.openings:
        if opening.name in ("port/chimney-inlet", "port/damper"):
            continue
        lo, hi = opening.box
        hit = [
            p for p in parts
            if all(p.lo[i] < hi[i] and p.hi[i] > lo[i] for i in range(3))
        ]  # fmt: skip
        assert hit, f"{opening.name} cuts nothing"
        # Through every layer of the wall it's in
        faces = {p.face for p in hit}
        assert len(faces) == 1, opening.name
        face = faces.pop()
        assert face is not None
        layers = kiln.lining.for_face(cast("Face", face), door_face=kiln.door_face)
        assert len(hit) >= len(layers), opening.name


def test_the_electric_kiln_has_a_case_a_hinged_door_and_peepholes() -> None:
    hw, _ = _hardware("electric-front-loader.yaml")
    names = {p.name for p in hw.pieces}
    assert {"case/left", "case/right", "case/back", "case/stand", "door/case"} <= names
    assert {"door/hinge-1", "door/hinge-2", "door/latch-1", "door/latch-2"} <= names
    assert not any(n.startswith(("frame/", "burner/", "chimney/")) for n in names)
    holes = [o for o in hw.openings if o.name.startswith("port/spy")]
    assert len(holes) == 3
    for o in holes:  # 1 in round holes
        lo, hi = o.box
        assert o.round_axis is not None
        across = [hi[i] - lo[i] for i in range(3) if i != o.round_axis]
        assert min(across) == pytest.approx(25.4)


def test_a_car_kiln_has_a_car() -> None:
    hw, _ = _hardware("pnw-hybrid-crossdraft-car.yaml")
    names = {p.name for p in hw.pieces}
    assert {"car/frame", "car/wheels", "car/rails"} <= names
    assert any("not sized" in f.message for f in hw.findings)


def test_a_power_burner_with_no_sourced_port_is_not_drawn() -> None:
    kiln = load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml")
    assert kiln.heat.gas is not None
    gas = kiln.heat.gas.model_copy(
        update={"burners": kiln.heat.gas.burners.model_copy(update={"type": "power"})}
    )
    kiln = kiln.model_copy(update={"heat": kiln.heat.model_copy(update={"gas": gas})})
    report = design_report(kiln)
    hw = build_hardware(kiln, report.frame, report.gas)
    assert not any(o.name.startswith("port/burner") for o in hw.openings)
    assert any("port size" in f.message for f in hw.findings)
    assert math.isfinite(hw.chimney_bricks)
