"""Round domes laid course by course, and their membrane forces at the springing."""

import math
from pathlib import Path

import pytest

from kilndesigner.conical import (
    Brick,
    lay_conical_dome,
    lay_dome,
    lay_straights_dome,
    rectangle,
)
from kilndesigner.designfile import load_design
from kilndesigner.frame import NO_TENSION, design_frame, membrane, round_dome_ring
from kilndesigner.masonry import CONICAL, plan_masonry
from kilndesigner.model import ConicalBrick, Kiln
from kilndesigner.units import parse_quantity

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"


def _kiln(name: str, **roof: str) -> Kiln:
    kiln = load_design(EXAMPLES / f"olsen/{name}.yaml")
    if roof:
        update = {k: parse_quantity(v) for k, v in roof.items()}
        kiln = kiln.model_copy(update={"roof": kiln.roof.model_copy(update=update)})
    return kiln


def test_membrane_matches_the_worked_example() -> None:
    # domes-over-doors.md §D1 [D2]: R = 10 m, α₀ = 60°, t = 0.3 m, γ = 25 kN/m³
    meridian, out, ring, hoop = membrane(10, 0.3 * 25, math.radians(60))
    assert meridian == pytest.approx(50)
    assert out == pytest.approx(25)
    assert ring == pytest.approx(216.5, abs=0.05)
    assert hoop == pytest.approx(12.5)
    # Tension starts at 51°50′
    assert membrane(1, 1, math.radians(NO_TENSION))[3] == pytest.approx(0, abs=1e-3)


def test_straights_dome_in_header_and_stretcher_courses() -> None:
    header = lay_straights_dome(112.5, 45, 9)
    stretcher = lay_straights_dome(112.5, 45, 4.5)
    assert header is not None
    assert stretcher is not None
    assert lay_straights_dome(112.5, 45, 6.75) is None
    # Both step 2½ in up the meridian; a header takes half a stretcher's length round
    assert len(header.courses) == len(stretcher.courses)
    assert header.total == pytest.approx(2 * stretcher.total, rel=0.02)
    first = header.courses[0]
    assert first.bricks == math.ceil(math.pi * first.across / 4.5 - 1e-9)
    assert [c.bricks for c in header.courses] == sorted(
        (c.bricks for c in header.courses), reverse=True
    )
    # The courses' hot-face heights stay under the rise; the plug closes what's left
    assert all(0 < c.height < 45 for c in header.courses)
    assert 0 < header.crown < 10
    assert any("Olsen" in (s.reference or "") for s in header.steps)


def test_rectangle_cuts_the_low_courses() -> None:
    part = rectangle(10, 20)
    assert part(5) == 1
    assert part(30) == 0
    assert 0 < part(15) < 1
    whole = lay_dome(30, 10, 0.1, 0.1, what="Dome", reference="test")
    cut = lay_dome(30, 10, 0.1, 0.1, what="Dome", reference="test", fraction=part)
    assert cut.total < whole.total


def test_conical_dome_round_and_over_a_rectangle() -> None:
    brick = Brick(9, 4.5, 2.5)
    laid = lay_conical_dome(30, 20, brick)
    assert laid.total > 0
    assert any("narrow ends" in s.name for s in laid.steps)
    with pytest.raises(ValueError, match="its radius"):
        lay_conical_dome(10, 11, brick)


def test_breda_dome_is_laid_in_header_courses() -> None:
    plan = plan_masonry(_kiln("breda-bottle"))
    text = " ".join(f.message for f in plan.result.findings)
    assert "header courses of straights" in text
    assert any(s.name.startswith("Dome, layer 1") for s in plan.result.working)


def test_round_dome_in_conical_bricks() -> None:
    kiln = _kiln("breda-bottle")
    lining = kiln.lining.model_copy(update={"conical": ConicalBrick()})
    plan = plan_masonry(kiln.model_copy(update={"lining": lining}))
    assert sum(q.amount for q in plan.result.quantities if CONICAL in q.name) > 0


def test_a_dome_past_a_hemisphere_falls_back_to_volume() -> None:
    plan = plan_masonry(_kiln("singh-coal", rise="50 in"))
    assert "by volume" in " ".join(f.message for f in plan.result.findings)
    frame = design_frame(_kiln("singh-coal", rise="50 in"))
    assert any("past a hemisphere" in f.message for f in frame.findings)
    assert round_dome_ring(_kiln("singh-coal", rise="50 in")) is None


def test_a_dome_of_other_depth_falls_back_to_volume() -> None:
    kiln = _kiln("singh-coal")
    assert kiln.lining.roof is not None
    roof = [kiln.lining.roof[0].model_copy(update={"thickness": parse_quantity("6.75 in")})]
    lining = kiln.lining.model_copy(update={"roof": roof})
    plan = plan_masonry(kiln.model_copy(update={"lining": lining}))
    assert "by volume" in " ".join(f.message for f in plan.result.findings)


def test_round_dome_ring_force() -> None:
    shallow = round_dome_ring(_kiln("breda-bottle", rise="37.5 in"))  # 2½ in per foot
    assert shallow is not None
    assert shallow.alpha < NO_TENSION
    assert "least it can be" not in shallow.finding().message
    deep = round_dome_ring(_kiln("breda-bottle"))  # 3 in per foot: 53.1°
    assert deep is not None
    assert deep.alpha == pytest.approx(math.degrees(math.asin(0.8)))
    assert deep.hoop > 0
    assert "least it can be" in deep.finding().message
    frame = design_frame(_kiln("breda-bottle"))
    assert frame.thrust is not None
    assert any(s.name.startswith("Dome: ring tension") for s in frame.working)
