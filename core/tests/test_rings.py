"""Bricks to turn a circle, against Olsen's tables (kiln-reference.md, Tables A-4 to A-7)."""

from __future__ import annotations

import pytest

from kilndesigner.rings import IN, RingError, ring, ring_series, wall_rings

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
