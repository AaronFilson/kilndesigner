"""Natural convection, checked against an independent implementation (the ``ht`` library)."""

import pytest
from ht.conv_free_immersed import (  # pyright: ignore[reportMissingTypeStubs]
    Nu_horizontal_plate_McAdams,
    Nu_vertical_plate_Churchill,
)

from kilndesigner.thermal.air import air
from kilndesigner.thermal.surface import nusselt, radiation_coefficient, rayleigh


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


def test_radiation_coefficient() -> None:
    # εσ(Ts² + T∞²)(Ts + T∞) for a black body at 400 K in 300 K surroundings
    assert radiation_coefficient(1.0, 400.0, 300.0) == pytest.approx(
        5.670374e-8 * (400**2 + 300**2) * 700
    )
