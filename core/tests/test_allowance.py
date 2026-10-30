"""What is bought over the count: sourced defaults by case, and the design's own.

The sources are in docs/research/brick-waste.md."""

from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from kilndesigner import Kiln, load_design
from kilndesigner.allowance import DEFAULTS, allowance
from kilndesigner.masonry import plan_masonry

EXAMPLES = Path(__file__).parents[2] / "examples"


def _with(kiln: Kiln, **allowances: str) -> Kiln:
    data = kiln.model_dump(mode="json", by_alias=True)
    data["allowances"] = allowances
    return Kiln.model_validate(data)


def test_the_defaults_are_sourced() -> None:
    assert {c: d.share for c, d in DEFAULTS.items()} == {
        "brick": 0.05,  # BIA Technical Note 10: "at least 5 percent"
        "shaped": 0.05,
        "castable": 0.05,  # PCO: "approximately 5%"
        "sheet": 0.0,  # none found
    }
    assert "[W1]" in DEFAULTS["brick"].reference
    assert "[W2]" in DEFAULTS["castable"].reference


def test_a_design_sets_its_own() -> None:
    base = load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml")
    kiln = _with(base, brick="8 percent", sheet="10 %", castable="12 percent")
    brick = allowance(kiln, "brick")
    assert (brick.share, brick.text, brick.from_design) == (pytest.approx(0.08), "8 %", True)
    step = brick.step()
    assert step.reference == "the design file"
    assert step.note is None
    assert allowance(kiln, "shaped").from_design is False

    default = plan_masonry(base).result
    own = plan_masonry(kiln).result
    by = {q.material: q for q in own.quantities}
    was = {q.material: q for q in default.quantities}
    jm26 = by["ifb-jm26"]
    assert jm26.detail.endswith("plus 8 % for breakage")
    assert jm26.amount > was["ifb-jm26"].amount
    blanket = by["kaowool-blanket-8pcf"]
    assert "plus 10 % for trimming" in blanket.detail
    assert blanket.amount == pytest.approx(was["kaowool-blanket-8pcf"].amount * 1.1, abs=0.1)
    assert by["kast-o-lite-30-li-plus"].detail.endswith("plus 12 %")
    note = next(f for f in own.findings if f.message.startswith("Brick counts"))
    assert "The allowance is the design's own." in note.message
    assert note.reference is not None
    assert note.reference.endswith("the design file")


def test_an_allowance_is_a_share_under_all_of_it() -> None:
    base = load_design(EXAMPLES / "electric-front-loader.yaml")
    with pytest.raises(ValidationError, match="under 100 %"):
        _with(base, brick="100 percent")
    with pytest.raises(ValidationError, match="at least 0 %"):
        _with(base, castable="-5 percent")
    with pytest.raises(ValidationError, match="share"):
        _with(base, brick="5 in")
