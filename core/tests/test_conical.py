import math
from pathlib import Path

import pytest

from kilndesigner.conical import Brick, course, dome, segment_radius, vault
from kilndesigner.designfile import load_design
from kilndesigner.geometry import lining_parts
from kilndesigner.masonry import CONICAL, conical_layer, plan_masonry
from kilndesigner.model import ConicalBrick, Kiln

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"

TATAMI = Brick.of(ConicalBrick())  # 9 in long, 4½ in to 2½ in: the user's starting size


def test_default_brick_and_its_own_radius() -> None:
    assert (TATAMI.length, TATAMI.wide, TATAMI.narrow) == pytest.approx((9, 4.5, 2.5))
    assert TATAMI.own_radius == pytest.approx(11.25)  # 9 × 2.5 / 2
    c = course(11.25, TATAMI)
    assert (c.inside_joint, c.outside_joint) == pytest.approx((0, 0), abs=1e-9)


def test_larger_rings_open_the_hot_face_and_smaller_the_outside() -> None:
    big = course(21, TATAMI)
    assert big.outside_joint == pytest.approx(0, abs=1e-9)
    assert big.inside_joint == pytest.approx(21 * 4.5 / 30 - 2.5)
    small = course(9, TATAMI)
    assert small.inside_joint == pytest.approx(0, abs=1e-9)
    assert small.outside_joint == pytest.approx(18 * 2.5 / 9 - 4.5)


def test_bidai_first_chamber_vault() -> None:
    # Olsen p.94-95, Fig 4-36: 42 in deep, crown 59 in, springing 38 in: a semicircle of 21 in
    v = vault(42, 21, 73, TATAMI)
    assert v.radius == pytest.approx(21)
    assert v.sweep == pytest.approx(math.pi)
    assert (v.per_row, v.rows, v.total) == (21, 17, 357)
    assert 0 < v.hot_face_brick < 1
    assert any(s.name == "The brick's own radius" for s in v.steps)


def test_segment_and_dome() -> None:
    r, a = segment_radius(48, 12)
    assert r == pytest.approx(30)
    assert a == pytest.approx(2 * math.asin(0.8))
    courses = dome(11.25, 11.25, TATAMI)
    assert courses[0][1] == math.ceil(2 * math.pi / course(11.25, TATAMI).angle - 1e-9)
    assert [n for _, n in courses] == sorted((n for _, n in courses), reverse=True)
    assert all(h < 11.25 for h, _ in courses)


@pytest.mark.parametrize(
    ("call", "message"),
    [
        (lambda: Brick(9, 2.5, 4.5), "wide end"),
        (lambda: course(0, TATAMI), "positive"),
        (lambda: segment_radius(10, 6), "half its span"),
        (lambda: dome(10, 11, TATAMI), "its radius"),
    ],
)
def test_refuses(call: object, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        call()  # type: ignore[operator]


def _with_conical(path: str, length: str = "9 in") -> Kiln:
    kiln = load_design(EXAMPLES / path)
    lining = kiln.lining.model_copy(
        update={"conical": ConicalBrick.model_validate({"length": length})}
    )
    return kiln.model_copy(update={"lining": lining})


def _conical_count(kiln: Kiln) -> float:
    return sum(q.amount for q in plan_masonry(kiln).result.quantities if CONICAL in q.name)


@pytest.mark.geometry
def test_bidai_arches_are_laid_in_conical_bricks() -> None:
    kiln = load_design(EXAMPLES / "olsen/bidai.yaml")
    assert kiln.lining.conical is not None
    assert _conical_count(kiln) > 0


@pytest.mark.geometry
def test_a_dome_is_laid_in_conical_bricks_when_as_deep_as_one_is_long() -> None:
    assert _conical_count(_with_conical("olsen/miravet.yaml")) > 0
    # A 9 in dome isn't laid in 6 in conical bricks: it falls back to the usual count
    assert _conical_count(_with_conical("olsen/miravet.yaml", "6 in")) == 0


def test_conical_layer_skips_parts_that_are_neither_arch_nor_dome() -> None:
    kiln = load_design(EXAMPLES / "olsen/bidai.yaml")
    wall = next(p for p in lining_parts(kiln) if p.arch is None and p.dome is None)
    brick = Brick(wall.thickness / 25.4, 4.5, 2.5)
    assert conical_layer(wall, brick) is None
    assert conical_layer(wall, None) is None


def test_model_refuses_a_brick_without_taper() -> None:
    with pytest.raises(ValueError, match="wider than its narrow"):
        ConicalBrick.model_validate({"wide": "2 in", "narrow": "2 in"})
