"""The bearing under a kiln's walls on its platform (chamber.foundation, foundation.py)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from kilndesigner.designfile import load_design, parse_design
from kilndesigner.foundation import platform_bearing, platform_top
from kilndesigner.frame import design_frame
from kilndesigner.heatloss import heat_loss
from kilndesigner.model import Kiln

EXAMPLES = Path(__file__).parents[2] / "examples"
PLATFORM = {
    "material": "concrete",
    "compressive_strength": "1800 psi",
    "strength_source": "a test value",
}


def _on_platform(name: str) -> Kiln:
    data = yaml.safe_load((EXAMPLES / name).read_text(encoding="utf-8"))
    data["chamber"]["foundation"] = PLATFORM
    return parse_design(yaml.safe_dump(data, allow_unicode=True))


BOWEN = EXAMPLES / "olsen" / "bowen-mountain.yaml"


def _bowen_on(thickness: str) -> Kiln:
    data = yaml.safe_load(BOWEN.read_text(encoding="utf-8"))
    data["chamber"]["foundation"]["thickness"] = thickness
    return parse_design(yaml.safe_dump(data, allow_unicode=True))


def test_bowen_mountains_walls_bear_on_its_platform() -> None:
    kiln = load_design(BOWEN)
    steps, findings = platform_bearing(kiln)
    (step,) = steps
    # AISC 360-16 J8-1, ASD: 0.85 × 1800 / 2.31 = 662 psi
    assert step.value.startswith("2.2 psi under the front wall against 662 psi allowed")
    assert "front wall" in step.inputs
    assert "the user's starting value" in (step.note or "")
    assert "taken unreduced" in (step.note or "")
    (finding,) = findings
    assert finding.level == "info"
    assert finding.check is not None
    assert finding.check.id == "foundation.bearing"
    assert "Give the platform's thickness" in finding.message
    assert any(s.name.startswith("Bearing under the walls") for s in design_frame(kiln).working)


def test_a_platforms_heat_and_top_face_are_worked_out_with_its_thickness() -> None:
    kiln = _bowen_on("6 in")
    loss = heat_loss(kiln)
    assert any(s.name == "Platform under the floor" for s in loss.working)
    assert "through its platform" in (loss.working[-1].note or "")
    steps, findings = platform_bearing(kiln)
    top = next(s for s in steps if s.name.endswith("platform's top face"))
    assert "°F" in top.value
    # 9 in of IFB on the slab: its top runs far past ACI 349's 150 °F, and f'c is reduced
    warned = [f for f in findings if f.check and f.check.id == "foundation.top-temperature"]
    assert warned[0].level == "warning"
    bearing = next(s for s in steps if s.name.startswith("Bearing under"))
    assert "662 psi" not in bearing.value
    assert platform_top(load_design(BOWEN)) is None


def test_a_cool_platform_top_passes() -> None:
    data = yaml.safe_load(BOWEN.read_text(encoding="utf-8"))
    data["chamber"]["foundation"]["thickness"] = "6 in"
    # Into dry soil at steady state even a thick floor's slab runs hot; a low firing keeps it cool
    data["firing"] = {"top_temperature": "250 degF"}
    kiln = parse_design(yaml.safe_dump(data, allow_unicode=True))
    _, findings = platform_bearing(kiln)
    top = [f for f in findings if f.check and f.check.id == "foundation.top-temperature"]
    assert top[0].level == "info", top[0].message


def test_a_weak_platform_fails_its_bearing() -> None:
    data = yaml.safe_load(BOWEN.read_text(encoding="utf-8"))
    data["chamber"]["foundation"]["compressive_strength"] = "5 psi"
    kiln = parse_design(yaml.safe_dump(data, allow_unicode=True))
    _, findings = platform_bearing(kiln)
    assert findings[0].level == "error"
    assert "stronger mix" in findings[0].message


def test_a_platforms_strength_defaults_to_the_irc() -> None:
    data = yaml.safe_load(BOWEN.read_text(encoding="utf-8"))
    data["chamber"]["foundation"] = {"material": "concrete"}
    kiln = parse_design(yaml.safe_dump(data, allow_unicode=True))
    found = kiln.chamber.foundation
    assert found is not None
    assert found.compressive_strength.to("psi").magnitude == 3500
    assert "IRC Table R402.2" in found.strength_source
    data["chamber"]["foundation"] = {"thickness": "0 in"}
    text = yaml.safe_dump(data, allow_unicode=True)
    with pytest.raises(ValidationError, match="more than zero"):
        parse_design(text)


def test_a_cross_arch_bears_on_its_side_walls() -> None:
    steps, _ = platform_bearing(_on_platform("gas-crossdraft.yaml"))
    (step,) = steps
    assert "the roof's" in step.inputs["left wall"]
    assert "the roof's" not in step.inputs["front wall"]


def test_other_roofs_are_refused_with_a_reason() -> None:
    steps, findings = platform_bearing(_on_platform("electric-front-loader.yaml"))
    assert steps == []
    assert "sprung arch only" in findings[0].message
    assert platform_bearing(load_design(EXAMPLES / "gas-crossdraft.yaml")) == ([], [])


def test_a_platform_needs_its_strength_and_its_source() -> None:
    with pytest.raises(ValidationError):
        parse_design(
            yaml.safe_dump(
                {
                    **yaml.safe_load((EXAMPLES / "gas-crossdraft.yaml").read_text("utf-8")),
                    "chamber": {"width": "3 ft", "depth": "3 ft", "height": "3 ft",
                                "foundation": {"compressive_strength": "1800 psi"}},
                }
            )
        )  # fmt: skip
