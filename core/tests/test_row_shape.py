"""Chambers in a row lose heat through the roof they're built with: an arch over each chamber
along the draft, a dome over each, or one tube's vault over them all."""

import math
from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.geometry import lining_parts
from kilndesigner.model import Kiln
from kilndesigner.shape import Arch, SailDome, chamber_shape
from kilndesigner.units import si

ROOT = Path(__file__).parents[2]
EXAMPLES = ROOT / "examples" / "olsen"
TEMPLATES = ROOT / "core" / "src" / "kilndesigner" / "data" / "templates"


def _faces(kiln: Kiln) -> dict[str, float]:
    return {f.face: f.inside_area for f in chamber_shape(kiln).faces()}


def test_a_climbing_kilns_roof_is_an_arch_over_each_chamber_along_the_draft() -> None:
    kiln = load_design(EXAMPLES / "kawaii.yaml")
    c = kiln.chamber
    w, d, h, n = (si(c.width, "m"), si(c.depth, "m"), si(c.height, "m"), c.chambers)
    arch = Arch(d, si(kiln.roof.rise, "m"))  # type: ignore[union-attr]
    faces = _faces(kiln)
    assert faces["roof"] == pytest.approx(n * arch.arc_length * w)
    # The arches close against the side walls; the end walls stand to the springline
    assert faces["left"] == pytest.approx(n * d * h + n * arch.segment_area)
    assert faces["front"] == pytest.approx(w * h)
    assert chamber_shape(kiln).volume == pytest.approx(w * h * n * d + n * arch.segment_area * w)
    # The roof's area grows with each arch's radius
    shape = next(f for f in chamber_shape(kiln).faces() if f.face == "roof")
    t = 0.1
    assert shape.area_at(t) == pytest.approx(
        n * 2 * (arch.radius + t) * arch.half_angle * (w + 2 * t)
    )


def test_the_drawn_arches_match_the_heat_loss() -> None:
    kiln = load_design(EXAMPLES / "kawaii.yaml")
    rings = [p for p in lining_parts(kiln) if p.name.startswith("roof/1-")]
    arch = Arch(si(kiln.chamber.depth, "mm"), si(kiln.roof.rise, "mm"))  # type: ignore[union-attr]
    for p in rings:
        assert p.across
        assert p.profile is not None
    assert len(rings) == kiln.chamber.chambers
    assert rings[0].hi[2] - rings[0].lo[2] >= arch.rise


def test_domes_in_a_row_are_one_to_a_chamber() -> None:
    kiln = load_design(EXAMPLES / "hollyweird.yaml")
    c = kiln.chamber
    w, d, n = si(c.width, "m"), si(c.depth, "m"), c.chambers
    dome = SailDome(w, d, si(kiln.roof.rise, "m"))  # type: ignore[union-attr]
    assert _faces(kiln)["roof"] == pytest.approx(n * dome.area())


def test_a_tube_is_one_vault_spanning_its_width() -> None:
    kiln = load_design(EXAMPLES / "tamba.yaml")
    c = kiln.chamber
    w, length = si(c.width, "m"), si(c.length, "m")
    arch = Arch(w, si(kiln.roof.rise, "m"))  # type: ignore[union-attr]
    assert _faces(kiln)["roof"] == pytest.approx(arch.arc_length * length)
    rings = [p for p in lining_parts(kiln) if p.name.startswith("roof/1-")]
    assert len(rings) == c.chambers
    assert all(p.arch is not None and not p.across for p in rings)
    # Its span is the width: half a circle on 5 ft, 30 in rise
    assert rings[0].arch is not None
    assert rings[0].arch.radius == pytest.approx(si(c.width, "mm") / 2)
    # The walls between the chambers are filled up to it
    caps = [p for p in lining_parts(kiln) if p.name.startswith("division/") and p.cap]
    assert len(caps) >= c.chambers - 1
    assert math.isfinite(sum(p.volume for p in caps))


def test_arches_along_the_draft_throw_their_thrust_on_the_end_walls() -> None:
    from kilndesigner.frame import NO_FRAME, design_frame
    from kilndesigner.masonry import plan_masonry

    kiln = load_design(TEMPLATES / "wood-two-chamber.yaml")
    assert not kiln.roof.buttressed  # type: ignore[union-attr]
    frame = design_frame(kiln)
    assert frame.kind == NO_FRAME
    assert frame.thrust is not None
    assert "on each end wall" in frame.thrust
    assert any("p.94–95" in f.message for f in frame.findings)
    # The masonry doesn't say there's steel in a frame
    notes = " ".join(f.message for f in plan_masonry(kiln).result.findings)
    assert "is in the frame" not in notes
    assert "The end walls take the arches' thrust" in notes


def test_a_rows_walls_reach_up_to_the_arches_along_the_draft() -> None:
    from kilndesigner.geometry import inside_top

    kiln = load_design(EXAMPLES / "kawaii.yaml")
    h = si(kiln.chamber.height, "mm")
    d = si(kiln.chamber.depth, "mm")
    rise = si(kiln.roof.rise, "mm")  # type: ignore[union-attr]
    assert inside_top(kiln, "front", 0.0) == pytest.approx(h)
    assert inside_top(kiln, "left", 0.0) == pytest.approx(h + rise)
    assert inside_top(kiln, "left", d) == pytest.approx(h)
