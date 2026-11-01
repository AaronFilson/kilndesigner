"""The bearing under a kiln's walls on its platform (chamber.foundation, foundation.py)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from pydantic import ValidationError

from kilndesigner.designfile import load_design, parse_design
from kilndesigner.foundation import platform_bearing
from kilndesigner.frame import design_frame
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


def test_bowen_mountains_walls_bear_on_its_platform() -> None:
    kiln = load_design(EXAMPLES / "olsen" / "bowen-mountain.yaml")
    steps, findings = platform_bearing(kiln)
    (step,) = steps
    assert step.value.startswith("2.2 psi under the front wall")
    assert "front wall" in step.inputs
    assert "the user's starting value" in (step.note or "")
    (finding,) = findings
    assert finding.level == "info"
    assert "Shown, not checked" in finding.message
    assert "no thermal conductivity" in finding.message
    assert any(s.name.startswith("Bearing under the walls") for s in design_frame(kiln).working)


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
