"""Natural convection, checked against an independent implementation (the ``ht`` library)."""

import pytest
from ht.conv_free_immersed import (  # pyright: ignore[reportMissingTypeStubs]
    Nu_horizontal_plate_McAdams,
    Nu_vertical_plate_Churchill,
)
from ht.radiation import q_rad  # pyright: ignore[reportMissingTypeStubs]

from kilndesigner.thermal.air import air
from kilndesigner.thermal.surface import (
    GRAVITY,
    RA_RANGE,
    STEFAN_BOLTZMANN,
    FixedSurface,
    StillAirSurface,
    convection_coefficient,
    nusselt,
    radiation_coefficient,
    rayleigh,
)


def film_rayleigh_350_300(length: float) -> tuple[float, float]:
    """Ra and Pr for a 350 K face in 300 K air, worked by hand from the Neutrium rows at 300 and
    400 K (electric-and-thermal.md §6.3): the film at 325 K is a quarter of the way between."""
    rho = 1.177 + 0.25 * (0.883 - 1.177)
    cp = 1005 + 0.25 * (1013 - 1005)
    k = 0.0261 + 0.25 * (0.0331 - 0.0261)
    mu = 1.850e-5 + 0.25 * (2.290e-5 - 1.850e-5)
    nu, alpha = mu / rho, k / (rho * cp)
    ra = GRAVITY * (1 / 325) * 50 * length**3 / (nu * alpha)  # β = 1/T_film, ideal gas
    return ra, cp * mu / k


@pytest.mark.parametrize("ra", [1e3, 1e6, 1e8, 1e10])
@pytest.mark.parametrize("pr", [0.69, 0.71, 0.72])
def test_churchill_chu_matches_ht(ra: float, pr: float) -> None:
    gr = ra / pr
    assert nusselt("vertical", ra, pr) == pytest.approx(Nu_vertical_plate_Churchill(pr, gr))


@pytest.mark.parametrize("ra", [1e5, 1e6, 1e8, 1e10])
def test_hot_plate_facing_up_matches_mcadams(ra: float) -> None:
    pr = 0.71
    expected = Nu_horizontal_plate_McAdams(pr, ra / pr, buoyancy=True)
    assert nusselt("facing_up", ra, pr) == pytest.approx(expected, rel=1e-2)


def test_air_at_300_k() -> None:
    a = air(300.0)
    assert a.kinematic_viscosity == pytest.approx(1.572e-5, rel=1e-3)
    assert a.prandtl == pytest.approx(0.712, rel=1e-3)


def test_rayleigh_for_a_warm_wall() -> None:
    ra, pr = rayleigh(350.0, 300.0, 1.0)
    assert 1e8 < ra < 1e10
    assert 0.69 < pr < 0.72
    assert (ra, pr) == pytest.approx(film_rayleigh_350_300(1.0))


def test_lloyd_moran_hot_face_up_changes_form_at_ra_1e7() -> None:
    """Nu = 0.54 Ra^¼ for 10⁴–10⁷ and 0.15 Ra^⅓ for 10⁷–10¹¹ (electric-and-thermal.md §6.2)."""
    assert nusselt("facing_up", 1e6, 0.71) == pytest.approx(0.54 * 10**1.5)
    assert nusselt("facing_up", 1e9, 0.71) == pytest.approx(0.15 * 1e3)


def test_hot_face_down_is_027_ra_to_the_quarter() -> None:
    """Nu = 0.27 Ra^¼ (§6.2): at Ra 10⁸ that is 27."""
    assert nusselt("facing_down", 1e8, 0.71) == pytest.approx(27.0)


def test_convection_coefficient_is_nusselt_times_k_over_length() -> None:
    """h = Nu·k/L with k at the film temperature, Nu from Churchill–Chu (via ``ht``)."""
    ra, pr = film_rayleigh_350_300(1.0)
    k_film = 0.0261 + 0.25 * (0.0331 - 0.0261)
    expected = Nu_vertical_plate_Churchill(pr, ra / pr) * k_film / 1.0
    assert convection_coefficient("vertical", 1.0, 350.0, 300.0) == pytest.approx(expected)


def test_no_temperature_difference_means_no_convection() -> None:
    assert convection_coefficient("vertical", 1.0, 300.0, 300.0) == 0.0
    assert convection_coefficient("facing_down", 0.3, 450.0, 450.0) == 0.0


def test_a_still_air_surface_adds_convection_and_radiation() -> None:
    shell = StillAirSurface("vertical", 1.0, 0.79)  # oxidised steel, CIBSE Guide C [S52]
    radiation = 0.79 * STEFAN_BOLTZMANN * (350.0**2 + 300.0**2) * (350.0 + 300.0)
    convection = convection_coefficient("vertical", 1.0, 350.0, 300.0)
    assert shell.coefficient(350.0, 300.0) == pytest.approx(convection + radiation)


def test_a_fixed_surface_ignores_the_temperatures() -> None:
    surface = FixedSurface(19.0)
    assert surface.coefficient(350.0, 300.0) == 19.0
    assert surface.coefficient(1000.0, 250.0) == 19.0


def test_each_face_knows_whether_its_correlation_covers_it() -> None:
    """Checked ranges (thermal-properties.md §5): vertical 0.1–10¹², hot face up 10⁴–10¹¹, hot
    face down 10⁵–10¹⁰. Ra grows with L³, so a small plate falls below and a big one above."""
    assert RA_RANGE == {
        "vertical": (0.1, 1e12),
        "facing_up": (1e4, 1e11),
        "facing_down": (1e5, 1e10),
    }
    ra_per_m3, _ = film_rayleigh_350_300(1.0)  # about 3.4e9
    ra, covered = StillAirSurface("vertical", 1.0, 0.9).rayleigh_in_range(350.0, 300.0)
    assert ra == pytest.approx(ra_per_m3)
    assert covered
    ra, covered = StillAirSurface("facing_down", 0.01, 0.9).rayleigh_in_range(350.0, 300.0)
    assert ra == pytest.approx(ra_per_m3 * 1e-6)
    assert not covered
    ra, covered = StillAirSurface("facing_up", 5.0, 0.9).rayleigh_in_range(350.0, 300.0)
    assert ra == pytest.approx(ra_per_m3 * 125)
    assert not covered


@pytest.mark.parametrize(
    ("emissivity", "t_surface", "t_air"), [(1.0, 400.0, 300.0), (0.79, 350.0, 300.0)]
)
def test_radiation_coefficient_matches_hts_grey_body_flux(
    emissivity: float, t_surface: float, t_air: float
) -> None:
    """h_r against an independent implementation: ``ht``'s net grey-body flux ÷ ΔT. No published
    worked example with numbers for h_r is in docs/research (notebooks/validation/surface.py)."""
    flux: float = q_rad(emissivity, t_surface, t_air)  # pyright: ignore[reportArgumentType]
    expected = flux / (t_surface - t_air)
    assert radiation_coefficient(emissivity, t_surface, t_air) == pytest.approx(expected, rel=1e-5)


@pytest.mark.parametrize("ra", [1e5, 1e7, 1e10])
def test_hot_face_down_matches_mcadams(ra: float) -> None:
    """Hot face down, 0.27 Ra^¼ (electric-and-thermal.md §6.2), against ``ht``'s McAdams."""
    expected = Nu_horizontal_plate_McAdams(0.71, ra / 0.71, buoyancy=False)
    assert nusselt("facing_down", ra, 0.71) == pytest.approx(expected, rel=1e-9)
