"""Radiation between the chamber's faces: thermal/radiation.py against published values."""

import math

import numpy as np
import pytest

from kilndesigner.thermal.radiation import (
    BOX_FACES,
    Enclosure,
    box,
    coaxial_discs,
    covered,
    exchange,
    parallel_rectangles,
    perpendicular_rectangles,
    surface_temperature,
)
from kilndesigner.thermal.surface import STEFAN_BOLTZMANN


def test_unit_squares_match_lienhard_fig_10_9() -> None:
    # Lienhard Example 10.2 reads 0.20 for adjoining unit squares off Fig. 10.9; opposite unit
    # squares one side apart are 0.1998 (Howell C-11)
    assert perpendicular_rectangles(1, 1, 1) == pytest.approx(0.20004, abs=1e-5)
    assert parallel_rectangles(1, 1, 1) == pytest.approx(0.19982, abs=1e-5)


def test_offset_squares_lienhard_example_10_2() -> None:
    # Squares of side 1 along a shared edge 2 long: F(1+3)–(4+2) at w/ℓ = h/ℓ = ½ reads 0.245
    # off Fig. 10.9, F1–4 0.20, so F1–2 = 0.045. Read off a chart: the formula gives 0.2406
    combined = perpendicular_rectangles(1, 1, 2)
    assert combined == pytest.approx(0.245, abs=0.005)
    assert combined - perpendicular_rectangles(1, 1, 1) == pytest.approx(0.045, abs=0.005)


def test_coaxial_discs_lienhard_example_10_3() -> None:
    # R1 = 5/20, R2 = 10/20: F = 0.192
    assert coaxial_discs(5, 10, 20) == pytest.approx(0.192, abs=5e-4)


def test_far_apart_and_close_limits() -> None:
    # Far apart: F → A2 cos·cos/(πs²); close together, opposite faces see only each other
    assert parallel_rectangles(1, 1, 100) == pytest.approx(1 / (math.pi * 100**2), rel=1e-3)
    assert parallel_rectangles(100, 100, 0.01) == pytest.approx(1, abs=1e-3)
    assert coaxial_discs(100, 100, 0.01) == pytest.approx(1, abs=1e-3)


def _quadrature_parallel(a: float, b: float, c: float, n: int = 60) -> float:
    """Lienhard eq. 10.17a by the midpoint rule: cos β1 = cos β2 = c/s."""
    xs = (np.arange(n) + 0.5) / n
    x1, y1, x2, y2 = np.meshgrid(xs * a, xs * b, xs * a, xs * b, indexing="ij")
    s2 = (x1 - x2) ** 2 + (y1 - y2) ** 2 + c * c
    integrand = c * c / (math.pi * s2 * s2)
    return float(integrand.mean() * (a * b) ** 2 / (a * b))


def test_parallel_formula_against_direct_integration() -> None:
    assert parallel_rectangles(1.2, 0.8, 0.9) == pytest.approx(
        _quadrature_parallel(1.2, 0.8, 0.9), rel=2e-3
    )


@pytest.mark.parametrize(("w", "d", "h"), [(1, 1, 1), (0.71, 0.91, 1.07), (0.6, 2.4, 1.1)])
def test_box_closes(w: float, d: float, h: float) -> None:
    # Two published formulas, combined: each face's row must sum to 1 and every pair must obey
    # reciprocity, or Enclosure refuses them
    e = box(w, d, h)
    assert e.view.sum(axis=1) == pytest.approx(np.ones(6), abs=1e-12)


def test_cube_faces_see_a_fifth_each() -> None:
    e = box(1, 1, 1)
    assert e.factor("floor", "roof") == pytest.approx(0.19982, abs=1e-5)
    assert e.factor("floor", "left") == pytest.approx(0.20004, abs=1e-5)


def test_tall_box_floor_sees_mostly_walls() -> None:
    e = box(0.5, 0.5, 5.0)
    assert e.factor("floor", "roof") < 0.01
    assert e.factor("roof", "floor") == e.factor("floor", "roof")


def test_cover_over_an_opening() -> None:
    flat = box(0.71, 0.91, 0.8)
    arch = covered(flat, "roof", flat.areas[5] * 1.18)
    k = BOX_FACES.index("roof")
    assert arch.view[k, k] == pytest.approx(1 - 1 / 1.18)
    # The rest still see the opening as before
    assert arch.factor("floor", "roof") == flat.factor("floor", "roof")
    with pytest.raises(ValueError, match="smaller than the opening"):
        covered(flat, "roof", flat.areas[5] * 0.9)


def test_enclosure_refuses_broken_view_factors() -> None:
    with pytest.raises(ValueError, match="sum to 1"):
        Enclosure(("a", "b"), (1.0, 1.0), np.array([[0.0, 0.9], [0.9, 0.0]]))
    with pytest.raises(ValueError, match="reciprocity"):
        Enclosure(("a", "b"), (1.0, 2.0), np.array([[0.0, 1.0], [1.0, 0.0]]))
    with pytest.raises(ValueError, match="outside 0–1"):
        Enclosure(("a", "b"), (1.0, 1.0), np.array([[-0.5, 1.5], [1.5, -0.5]]))
    with pytest.raises(ValueError, match="one area"):
        Enclosure(("a", "b"), (1.0,), np.array([[0.0, 1.0], [1.0, 0.0]]))


def _strips(a3: float) -> Enclosure:
    """Lienhard Example 10.9: two strips 1 m wide, 2.40 m apart (per metre), F1–2 = 0.2, and a
    third surface closing the sides."""
    f13 = 0.8
    view = np.array([[0.0, 0.2, f13], [0.2, 0.0, f13], [f13 / a3, f13 / a3, 1 - 2 * f13 / a3]])
    return Enclosure(("1", "2", "3"), (1.0, 1.0, a3), view)


# Lienhard works Example 10.9 with σ = 5.67e-8 and its coefficients rounded to two places
# (B1 − 0.14 B2 ...), so its radiosities agree to about 0.1 %
BOOK = 2e-3


def test_lienhard_example_10_9_black_surroundings() -> None:
    ex = exchange(_strips(4.8), [0.3, 0.5, 1.0], [400.0, 300.0, 250.0])
    assert ex.radiosity[0] == pytest.approx(612.1, rel=BOOK)
    assert ex.radiosity[1] == pytest.approx(379.5, rel=BOOK)
    q12 = (ex.radiosity[0] - ex.radiosity[1]) * 0.2
    assert q12 == pytest.approx(46.53, abs=0.1)


def test_lienhard_example_10_9_insulated_reflector() -> None:
    ex = exchange(_strips(4.8), [0.3, 0.5, 0.5], [400.0, 300.0, None], [None, None, 0.0])
    assert list(ex.radiosity) == pytest.approx([987.7, 657.4, 822.6], rel=BOOK)
    assert ex.power[0] == pytest.approx(198, abs=0.5)
    assert ex.power[0] == pytest.approx(-ex.power[1])
    assert surface_temperature(ex, 0.5, 2) == pytest.approx(347, abs=0.5)


def test_enclosed_body_lienhard_eq_10_27() -> None:
    # A convex body 1 (sees none of itself) inside body 2
    a1, a2, e1, e2, t1, t2 = 1.0, 4.0, 0.6, 0.8, 1500.0, 1000.0
    view = np.array([[0.0, 1.0], [a1 / a2, 1 - a1 / a2]])
    ex = exchange(Enclosure(("in", "out"), (a1, a2), view), [e1, e2], [t1, t2])
    expected = a1 * STEFAN_BOLTZMANN * (t1**4 - t2**4) / (1 / e1 + a1 / a2 * (1 / e2 - 1))
    assert ex.power[0] == pytest.approx(expected, rel=1e-12)


def test_isothermal_box_exchanges_nothing() -> None:
    ex = exchange(box(0.7, 0.9, 1.0), [0.8] * 6, [1500.0] * 6)
    assert ex.flux == pytest.approx(np.zeros(6), abs=1e-6)
    assert ex.radiosity == pytest.approx(np.full(6, STEFAN_BOLTZMANN * 1500.0**4))


def test_box_energy_balance() -> None:
    temps = [1500.0, 1450.0, 1400.0, 1300.0, 1200.0, 1520.0]
    ex = exchange(box(0.7, 0.9, 1.0), [0.75, 0.75, 0.8, 0.6, 0.85, 0.75], temps)
    assert ex.power.sum() == pytest.approx(0.0, abs=1e-6 * np.abs(ex.power).max())
    assert ex.power[5] > 0 > ex.power[4]  # the hot roof feeds the cold floor


def test_exchange_refuses_what_it_cannot_solve() -> None:
    e = box(1, 1, 1)
    with pytest.raises(ValueError, match="emissivity"):
        exchange(e, [0.0] * 6, [1000.0] * 6)
    with pytest.raises(ValueError, match="temperature or a flux"):
        exchange(e, [0.8] * 6, [1000.0] * 5)
    with pytest.raises(ValueError, match="neither"):
        exchange(e, [0.8] * 6, [None, *[1000.0] * 5])
    with pytest.raises(ValueError, match="at least one"):
        exchange(e, [0.8] * 6, [None] * 6, [0.0] * 6)


@pytest.mark.parametrize(
    "call",
    [
        lambda: parallel_rectangles(0, 1, 1),
        lambda: perpendicular_rectangles(1, 0, 1),
        lambda: coaxial_discs(1, 1, 0),
    ],
)
def test_sizes_must_be_positive(call: object) -> None:
    with pytest.raises(ValueError, match="positive"):
        call()  # pyright: ignore[reportCallIssue]
