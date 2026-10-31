"""Bricks to turn a circle, against Olsen's tables (kiln-reference.md, Tables A-4 to A-7)."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from kilndesigner.rings import (
    CLOSER,
    IN,
    RingError,
    cut_bricks,
    cut_count,
    cut_diameter,
    floor_inside_depth,
    nominal_diameter,
    ring,
    ring_method,
    ring_series,
    wall_height,
    wall_rings,
)

# Table A-4, 9 × 4½ × 2½ in arch bricks (p.303): inside diameter in inches, No.3, No.2, No.1,
# straights. Every row of the book.
A4 = [
    (6, 19, 0, 0, 0), (7, 18, 3, 0, 0), (8, 17, 5, 0, 0), (9, 15, 8, 0, 0), (10, 14, 10, 0, 0),
    (11, 13, 13, 0, 0), (12, 12, 15, 0, 0), (13, 10, 18, 0, 0), (14, 9, 20, 0, 0),
    (15, 8, 23, 0, 0), (16, 7, 25, 0, 0), (17, 5, 28, 0, 0), (18, 4, 30, 0, 0), (19, 3, 33, 0, 0),
    (20, 2, 35, 0, 0), (21, 0, 38, 0, 0), (22, 0, 36, 3, 0), (23, 0, 36, 5, 0), (24, 0, 34, 8, 0),
    (25, 0, 33, 10, 0), (26, 0, 31, 13, 0), (27, 0, 31, 15, 0), (28, 0, 29, 18, 0),
    (29, 0, 28, 20, 0), (30, 0, 26, 23, 0), (31, 0, 26, 25, 0), (32, 0, 24, 28, 0),
    (33, 0, 23, 30, 0), (34, 0, 21, 33, 0), (35, 0, 20, 36, 0), (36, 0, 19, 38, 0),
    (37, 0, 18, 40, 0), (38, 0, 16, 43, 0), (39, 0, 15, 46, 0), (40, 0, 14, 48, 0),
    (41, 0, 13, 50, 0), (42, 0, 11, 53, 0), (43, 0, 10, 56, 0), (44, 0, 9, 58, 0),
    (45, 0, 8, 60, 0), (46, 0, 7, 63, 0), (47, 0, 5, 66, 0), (48, 0, 4, 68, 0), (49, 0, 3, 70, 0),
    (50, 0, 2, 73, 0), (51, 0, 0, 76, 0), (54, 0, 0, 76, 4), (60, 0, 0, 76, 11),
    (66, 0, 0, 76, 19), (72, 0, 0, 76, 26), (78, 0, 0, 76, 34), (84, 0, 0, 76, 41),
]  # fmt: skip

# Table A-6, 9 × 4½ × 2½ in wedges (p.304–305): No.2, No.1, straights. The first three rows'
# totals are misprinted in the book; their counts are kept.
A6 = [
    (27, 57, 0, 0), (28, 55, 3, 0), (29, 52, 7, 0), (30, 51, 10, 0), (31, 48, 14, 0),
    (32, 46, 17, 0), (33, 44, 20, 0), (34, 42, 24, 0), (35, 40, 27, 0), (36, 38, 30, 0),
    (37, 36, 34, 0), (38, 34, 37, 0), (39, 32, 40, 0), (40, 29, 44, 0), (41, 28, 47, 0),
    (42, 25, 51, 0), (43, 23, 54, 0), (44, 21, 57, 0), (45, 19, 61, 0), (46, 17, 64, 0),
    (47, 15, 67, 0), (48, 13, 70, 0), (49, 11, 74, 0), (50, 9, 77, 0), (51, 6, 81, 0),
    (52, 4, 84, 0), (53, 2, 88, 0), (54, 0, 91, 0), (60, 0, 91, 7), (66, 0, 91, 15),
    (72, 0, 91, 22), (78, 0, 91, 30), (84, 0, 91, 38),
]  # fmt: skip


def _counts(diameter_in: float, series: str) -> dict[str, int]:
    r = ring(diameter_in * IN, series)  # type: ignore[arg-type]
    return dict(r.counts)


@pytest.mark.parametrize("row", A4, ids=lambda r: f"{r[0]}in")
def test_arch_brick_rings_match_olsens_table_a4(row: tuple[int, ...]) -> None:
    d, n3, n2, n1, s = row
    got = _counts(d, "arch")
    want = {"No. 3 arch": n3, "No. 2 arch": n2, "No. 1 arch": n1, "straight": s}
    assert sum(got.values()) == sum(want.values())
    for name, n in got.items():
        assert abs(n - want[name]) <= 1, (name, got, want)


@pytest.mark.parametrize("row", A6, ids=lambda r: f"{r[0]}in")
def test_wedge_rings_match_olsens_table_a6(row: tuple[int, ...]) -> None:
    d, n2, n1, s = row
    got = _counts(d, "wedge")
    want = {"No. 2 wedge": n2, "No. 1 wedge": n1, "straight": s}
    assert sum(got.values()) == sum(want.values())
    for name, n in got.items():
        assert abs(n - want[name]) <= 1, (name, got, want)


REFERENCE = Path(__file__).parents[2] / "docs" / "research" / "kiln-reference.md"


def _table(heading: str) -> list[list[int]]:
    """A transcribed table's rows: the diameter in inches, then each column's count (– is 0)."""
    text = REFERENCE.read_text(encoding="utf-8").split(heading, 1)[1].split("\n\n**", 1)[0]
    text = text.split("\n### ", 1)[0]
    rows: list[list[int]] = []
    for line in text.splitlines():
        m = re.match(r"\| (\d+)'(\d+)\" \|(.*)\|$", line)
        if m:
            cells = [c.strip().replace("(?)", "").strip() for c in m[3].split("|")]
            rows.append([int(m[1]) * 12 + int(m[2])] + [0 if c == "–" else int(c) for c in cells])
    return rows


A5 = _table("**Table A-5")
A7 = _table("**Table A-7")


@pytest.mark.parametrize("row", A5, ids=lambda r: f"{r[0]}in")
def test_3_inch_arch_rings_match_olsens_table_a5(row: list[int]) -> None:
    d, n3, n2, n1, total = row
    got = _counts(d, "arch3")
    want = {"No. 3 arch, 3 in series": n3, "No. 2 arch, 3 in series": n2,
            "No. 1 arch, 3 in series": n1, "3 in straight": 0}  # fmt: skip
    assert sum(got.values()) == total
    for name, n in got.items():
        assert abs(n - want[name]) <= 1, (name, got, want)


@pytest.mark.parametrize("row", A7, ids=lambda r: f"{r[0]}in")
def test_3_inch_wedge_rings_match_olsens_table_a7(row: list[int]) -> None:
    d, n3, n2, total = row
    got = _counts(d, "wedge3")
    want = {"No. 3 wedge, 3 in series": n3, "No. 2 wedge, 3 in series": n2, "3 in straight": 0}
    assert sum(got.values()) == total
    for name, n in got.items():
        assert abs(n - want[name]) <= 1, (name, got, want)


def test_the_3_inch_tables_are_all_read() -> None:
    assert (len(A5), A5[0][0], A5[-1][0]) == (66, 18, 83)
    assert (len(A7), A7[0][0], A7[-1][0]) == (49, 36, 84)


def test_a_circle_tighter_than_the_tightest_shape_is_refused() -> None:
    with pytest.raises(RingError, match=r"tighter than No\. 3 arch bricks turn on their own"):
        ring(5 * IN, "arch")


def test_key_rings_put_4_and_a_half_inches_round_the_outside() -> None:
    """A 60 in round wall of keys: π × 78 in outside ÷ 4½ in = 54.45, rounded up to 55; round
    the inside, π × 60 = 188.5 in = 3 n₃ + 3½ n₂, so n₂ = (188.5 − 54.45 × 3) ÷ ½ = 50.3."""
    r = ring(60 * IN, "key")
    assert r.total == 55
    assert dict(r.counts) == {"No. 3 key": 5, "No. 2 key": 50}


def test_round_walls_are_rings_of_9_and_4_and_a_half_inches() -> None:
    assert wall_rings(9 * IN) == [9 * IN]
    assert wall_rings(13.5 * IN) == [4.5 * IN, 9 * IN]
    assert wall_rings(18 * IN) == [9 * IN, 9 * IN]
    assert wall_rings(24 * IN) is None
    assert wall_rings(4 * IN) is None
    assert ring_series(9 * IN) == "key"
    assert ring_series(4.5 * IN) == "arch"
    assert ring_series(2.5 * IN) is None


def test_a_mortar_ring_follows_the_curve_with_one_closer() -> None:
    """A 36 in circle: each 9 in inside face turns 2·asin(9/36) = 28.96°, so 12 whole bricks
    (347.5°) and a closer cut to the chord of the 12.54° left, 36·sin(6.27°) = 3.93 in. Two whole
    bricks open a joint 2 × 4½ × sin(14.48°) = 2¼ in wide at the outside (d·L/r)."""
    r = ring(36 * IN, "mortar")
    assert dict(r.counts) == {"straight laid flat": 12, CLOSER: 1}
    assert r.length == pytest.approx(3.932 * IN, abs=0.01 * IN)
    assert r.joint == pytest.approx(2.25 * IN)
    assert r.mortar is not None
    assert r.mortar > 0


def test_a_mortar_ring_narrower_than_a_straight_is_refused() -> None:
    with pytest.raises(RingError, match="narrower than a 9 in straight"):
        ring(8 * IN, "mortar")


def test_a_cut_ring_keeps_full_bricks_and_closes_with_one_short_one() -> None:
    """A 36 in ring 4½ in through, sized as makers quote it (the mean of flats and corners):
    N solves 2(4½/tan(π/N) − 4½)(1 + 1/cos(π/N)) ÷ 2 = 36 at 15.79, so 15 full bricks and a
    closer of 0.79 × 9 = 7.1 in along the outside, the ends 180/15.79 = 11.4° off square."""
    r = ring(36 * IN, "cut")
    assert dict(r.counts) == {"straight cut to the angle": 15, CLOSER: 1}
    assert r.length == pytest.approx(7.125 * IN, abs=0.01 * IN)
    assert r.angle == pytest.approx(11.40, abs=0.01)


def test_whole_brick_cut_rings_need_no_closer() -> None:
    """12 full bricks round, 4½ in through: inside apothem 4½/tan(15°) − 4½ = 12.29 in, so
    12.29 × (1 + 1/cos 15°) = 25.02 in across inside, the mean of flats and corners."""
    assert cut_diameter(12) == pytest.approx(25.02 * IN, abs=0.01 * IN)
    assert cut_bricks(cut_diameter(12)) == pytest.approx(12)
    r = ring(cut_diameter(12), "cut")
    assert dict(r.counts) == {"straight cut to the angle": 12}
    assert r.length is None
    assert r.angle == pytest.approx(15)


# Published round electric kilns: sides, brick (in), inside diameter (in), as electric-kiln-
# survey.md records them. Skutt's own KM-1227 sheet prints 28.00 in for 12 sides of 3 in brick.
ELECTRIC = [
    ("Skutt KM-1227-3", 12, 3.0, 28.00),
    ("L&L e23T-3", 10, 3.0, 22.30),
    ("Skutt KM-1027", 10, 2.5, 23.375),
    ("Skutt KM-818", 8, 2.5, 17.5),
    ("Skutt KM-818-3", 8, 3.0, 16.5),
]


@pytest.mark.parametrize("kiln", ELECTRIC, ids=lambda k: k[0])
def test_cut_rings_match_published_electric_kilns(kiln: tuple[str, int, float, float]) -> None:
    """Full 9 in faces outside, the inside quoted as the mean of flats and corners: within
    0.15 in of each published diameter (derived, electric-kiln-survey.md)."""
    _, sides, brick, published = kiln
    assert nominal_diameter(sides, brick * IN) == pytest.approx(published * IN, abs=0.15 * IN)
    assert round(cut_bricks(published * IN, brick * IN)) == sides


def test_paragon_tnf_27_3_floor_inside_the_walls() -> None:
    """Paragon's TnF-27-3 (electric-kiln-survey.md). Status: a dealer snippet, search summaries
    only, Paragon's own sheet not reached: "12-sided", "3" thick firebrick", "Firing Opening 28"
    Depth - 22-1/4"". Its 27 in of wall holds the floor slab inside the lowest 4½ in course (the
    user, 2026-10-30), so it is 27 − 4½ = 22½ in deep inside, 22¼ printed."""
    assert nominal_diameter(12, 3 * IN) == pytest.approx(28 * IN, abs=0.15 * IN)
    assert round(cut_bricks(28 * IN, 3 * IN)) == 12
    assert floor_inside_depth(27) == pytest.approx(22.5)
    assert floor_inside_depth(27) == pytest.approx(22.25, abs=0.25)
    assert wall_height(22.5, floor_inside=True) == pytest.approx(27)
    assert wall_height(27, floor_inside=False) == pytest.approx(27)  # Skutt's KM-1227-3


def test_electric_walls_are_one_cut_ring_of_2_and_a_half_or_3_inch_brick() -> None:
    assert wall_rings(3 * IN, "cut") == [3 * IN]
    assert wall_rings(2.5 * IN, "cut") == [2.5 * IN]
    assert wall_rings(3 * IN, "mortar") is None
    assert ring_series(3 * IN, "cut") == "cut3"
    assert ring_series(2.5 * IN, "cut") == "cut2.5"
    r = ring(nominal_diameter(12, 3 * IN), "cut3")
    assert dict(r.counts) == {"straight cut to the angle": 12}
    assert r.series == "cut3"


def test_a_featheredge_ring_takes_about_twelve_whatever_its_size() -> None:
    """π × 45 in ÷ 2½ = 56.5, so 57 round the outside; round the inside π × 36 = 113.1 in =
    ⅛ n_f + 2½ n_s, so n_s = (113.1 − 56.5 × ⅛) ÷ 2⅜ = 44.6 → 45 straights and 12 featheredges:
    2π × 4½ ÷ 2⅜ = 11.9 at any diameter."""
    assert dict(ring(36 * IN, "featheredge").counts) == {"featheredge": 12, "straight": 45}
    assert dict(ring(72 * IN, "featheredge").counts)["featheredge"] == 12


def test_the_4_and_a_half_inch_ring_is_the_builders_choice() -> None:
    assert ring_series(4.5 * IN, "mortar") == "mortar"
    assert ring_series(9 * IN, "cut") == "key"
    assert ring_method(None, electric=True) == "cut"
    assert ring_method(None, electric=False) == "mortar"
    assert ring_method("featheredge", electric=True) == "featheredge"


def test_a_cut_ring_within_a_sixteenth_of_whole_bricks_is_laid_whole() -> None:
    """1/16 in round the ring is near enough (the user); 9 in × 0.006 = 0.054 in is, 9 in ×
    0.01 = 0.09 in isn't, so that ring takes the fewest bricks and a closer."""
    assert cut_count(12.006) == (12, True)
    assert cut_count(11.994) == (12, True)
    assert cut_count(12.01) == (12, False)
    assert cut_count(11.99) == (11, False)
