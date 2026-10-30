"""k(T) and its integral (the Kirchhoff transform), against closed forms and the data sheets."""

import pytest

from kilndesigner.library import material
from kilndesigner.thermal.conductivity import Conductivity

C = 273.15


def linear(a: float, b: float) -> Conductivity:
    """k = a + bT, written as two points so the piecewise-linear k is exactly this line."""
    return Conductivity((300.0, 1500.0), (a + b * 300.0, a + b * 1500.0))


def closed_form(a: float, b: float, t0: float, t1: float) -> float:
    """∫ (a + bT) dT from t0 to t1."""
    return a * (t1 - t0) + b / 2 * (t1**2 - t0**2)


def test_k_follows_the_data_sheet_between_its_points_and_carries_on_past_them() -> None:
    """JM 28 (materials.yaml, Morgan JM sheet, 2025): 0.30, 0.32, 0.34, 0.36, 0.36 W/(m·K) at 400,
    600, 800, 1000 and 1100 °C. Between points k is linear; past the last it follows the last
    pair; below the first it is held at the first point's k (science review E6/M9)."""
    k = material("ifb-jm28").k
    assert k.k(400 + C) == pytest.approx(0.30)
    assert k.k(700 + C) == pytest.approx((0.32 + 0.34) / 2)
    assert k.k(1100 + C) == pytest.approx(0.36)
    # 100 °C past the last point, along the 1000–1100 °C slope (flat)
    assert k.k(1200 + C) == pytest.approx(0.36)
    # Below the first point: held at 0.30, not carried down the 400–600 °C slope to 0.29
    assert k.k(300 + C) == pytest.approx(0.30)


def test_fibre_below_its_first_point_is_no_less_conductive_than_there() -> None:
    """Review E6: carried down linearly, Kaowool 8 pcf fell to 0.014 W/(m·K) at 40 °C, below
    still air (about 0.026). Held at its first point it can't."""
    k = material("kaowool-blanket-8pcf").k
    first = k.values[0]
    assert k.k(40 + C) == pytest.approx(first)
    assert k.k(40 + C) > 0.026
    # A k falling with temperature carries on up as it goes down (higher k: the safe side)
    falling = Conductivity((500.0, 600.0), (0.2, 0.1))
    assert falling.k(400.0) == pytest.approx(0.3)


def test_the_integral_across_the_data_points_is_the_sum_of_trapezoids() -> None:
    """∫k dT for JM 26 from 400 to 1000 °C: 200 × (0.25 + 0.27)/2 + 200 × (0.27 + 0.30)/2 +
    200 × (0.30 + 0.33)/2 = 52 + 57 + 63 = 172 W/m, exact for the piecewise-linear k."""
    k = material("ifb-jm26").k
    assert k.integral(400 + C, 1000 + C) == pytest.approx(172.0)
    # 500–700 °C starts and ends between points, with k 0.26, 0.27 (at 600 °C) and 0.285
    expected = 100 * (0.26 + 0.27) / 2 + 100 * (0.27 + 0.285) / 2
    assert k.integral(500 + C, 700 + C) == pytest.approx(expected)


def test_a_constant_k_integrates_to_k_times_the_temperature_difference() -> None:
    k = Conductivity.constant(0.5)
    assert k.k(200.0) == 0.5
    assert k.k(2000.0) == 0.5
    assert k.integral(300.0, 1300.0) == pytest.approx(500.0)


def test_integrating_downwards_gives_the_negative() -> None:
    k = linear(0.05, 2.5e-4)
    assert k.integral(1200.0, 500.0) == pytest.approx(-closed_form(0.05, 2.5e-4, 500.0, 1200.0))
    assert k.integral(800.0, 800.0) == 0.0


def test_extrapolated_k_never_falls_to_zero() -> None:
    """Far past a data sheet's last point, a falling k extrapolates below zero; it is held at a
    small positive floor (1e-3 W/(m·K)) so the solver never divides by zero."""
    k = Conductivity((300.0, 400.0), (0.2, 0.1))  # k = 0.5 − 0.001·T: zero at 500 K
    assert k.k(350.0) == pytest.approx(0.15)
    assert k.k(1000.0) == pytest.approx(1e-3)


def test_upper_temperature_inverts_the_integral() -> None:
    """For k = a + bT the face temperature t1 solves a(t1 − t0) + b/2 (t1² − t0²) = target."""
    a, b = 0.05, 2.5e-4
    k = linear(a, b)
    t0, target = 400.0, 300.0
    # the positive root of (b/2) t1² + a t1 − (a t0 + b/2 t0² + target) = 0
    c = a * t0 + b / 2 * t0**2 + target
    expected = (-a + (a * a + 2 * b * c) ** 0.5) / b
    t1 = k.upper_temperature(t0, target)
    assert t1 == pytest.approx(expected, rel=1e-9)
    assert k.integral(t0, t1) == pytest.approx(target, rel=1e-9)


def test_upper_temperature_works_downwards_too() -> None:
    """A negative target is a face colder than t0; with k rising in T the first guess (from k at
    t0) doesn't reach far enough, so the bracket has to widen downwards."""
    a, b = 0.05, 2.5e-4
    k = linear(a, b)
    t0, target = 1200.0, -150.0
    c = a * t0 + b / 2 * t0**2 + target
    expected = (-a + (a * a + 2 * b * c) ** 0.5) / b
    t1 = k.upper_temperature(t0, target)
    assert t1 < t0
    assert t1 == pytest.approx(expected, rel=1e-9)


def test_upper_temperature_with_k_falling_as_it_heats() -> None:
    """Kast-O-Lite 30's k falls from 400 to 800 °F (materials.yaml, HWI data [S50]); the solver
    still finds the face where ∫k dT reaches the target."""
    k = material("kast-o-lite-30-li-plus").k
    t0 = k.temperatures[0]
    t1 = k.upper_temperature(t0, 150.0)
    assert k.k(t1) < k.k(t0)
    assert k.integral(t0, t1) == pytest.approx(150.0, rel=1e-9)


def test_no_heat_flow_means_no_temperature_change() -> None:
    assert linear(0.05, 2.5e-4).upper_temperature(700.0, 0.0) == 700.0


@pytest.mark.parametrize(
    ("temperatures", "values", "message"),
    [
        ((), (), "matching, non-empty"),
        ((300.0, 400.0), (0.1,), "matching, non-empty"),
        ((400.0, 300.0), (0.1, 0.2), "must increase"),
        ((300.0, 300.0), (0.1, 0.2), "must increase"),
        ((300.0,), (0.0,), "must be positive"),
        ((300.0, 400.0), (0.1, -0.1), "must be positive"),
    ],
)
def test_bad_conductivity_data_is_refused(
    temperatures: tuple[float, ...], values: tuple[float, ...], message: str
) -> None:
    with pytest.raises(ValueError, match=message):
        Conductivity(temperatures, values)
