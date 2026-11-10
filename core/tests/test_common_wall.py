"""The wall between two chambers in a row (common_wall.py): Olsen's common wall, "4½ in thicker
than the others, never narrower than its two skewbacks" (The Kiln Book, 4th ed., p.46), in whole
bricks, unless the design gives its own (lining.between)."""

from pathlib import Path

import pytest

from kilndesigner.common_wall import between_layers, carries_arches, feet
from kilndesigner.designfile import load_design
from kilndesigner.model import Kiln

OLSEN = Path(__file__).parents[2] / "examples" / "olsen"


def olsen(name: str) -> Kiln:
    return load_design(OLSEN / f"{name}.yaml")


def total(kiln: Kiln) -> float:
    return sum(t for _, t in between_layers(kiln, "in"))


def test_the_common_wall_carries_two_arches_feet() -> None:
    """Kawaii's 9½ in walls and 9 in semicircular arches: 4½ in thicker would be 14 in, but the two
    arches' feet need 18 in."""
    kawaii = olsen("kawaii")
    assert feet(kawaii, "in") == pytest.approx(18.0)
    assert between_layers(kawaii, "in") == [
        ("firebrick-medium-duty-smithfield", pytest.approx(18.0))
    ]


def test_thickened_in_whole_bricks() -> None:
    """Olsen's three-chamber kiln: 4½ in K-26 and 4½ in K-23, its segmental arches' feet 16.6 in on
    one wall; the hot face thickened to 12½ in, whole bricks (2½ in × 5), for 17 in in all."""
    three = olsen("olsen-three-chamber")
    assert feet(three, "in") == pytest.approx(16.6, abs=0.05)
    layers = between_layers(three, "in")
    assert [m for m, _ in layers] == ["ifb-k26", "ifb-k23"]
    assert total(three) == pytest.approx(17.0)


def test_a_printed_wall_and_walls_that_carry_no_arch() -> None:
    """The design's own wall where the book prints it (Olsen's two-chamber kiln, 9 in, Fig 8-17);
    a dome row without one gets 4½ in more; a tube's walls between chambers carry no arch, nor a
    single chamber's."""
    assert total(olsen("olsen-two-chamber")) == pytest.approx(9.0)
    holly = olsen("hollyweird")
    assert total(holly) == pytest.approx(13.0)
    plain = holly.model_copy(update={"lining": holly.lining.model_copy(update={"between": None})})
    assert carries_arches(plain)
    assert feet(plain, "in") == 0.0
    assert total(plain) == pytest.approx(13.5)
    tamba = olsen("tamba")  # a tube
    assert not carries_arches(tamba)
    assert total(tamba) == pytest.approx(9.0)
    assert total(olsen("fast-fire")) == pytest.approx(4.5)
