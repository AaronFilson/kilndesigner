"""v2's ground (`heat/ground.py`): scikit-fem's axisymmetric soil under a floor, against the
survey's probe (`scratch/thermal-survey/soil_probe.py`, 1,548 nodes, consistent mass), the steady
disc (Incropera Table 4.1 case 10) and the semi-infinite slab; then coupled to a firing."""

from __future__ import annotations

import math
from typing import Any

import heat_cases as hc
import numpy as np
import pytest

from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import ground as gr
from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat.zone import ZoneModel

DISC = math.pi * 0.6**2  # the survey's D 1.2 m disc
# The survey's 2-D, the ground round the disc adiabatic: Q/(kΔT) in m (thermal-software.md §4.2)
SURVEY = {0.25: 39.12, 1.0: 20.37, 6.0: 9.49, 12.0: 7.27, 48.0: 4.70, 72.0: 4.25, 720.0: 2.98}


@pytest.fixture(scope="module")
def soil() -> gr.Ground:
    return gr.ground(DISC)


def test_the_step_response_is_the_surveys(soil: gr.Ground) -> None:
    """A 1 K step on the disc, dry soil (k 1, so W/K reads as Q/(kΔT) in m): within 1.5 % of the
    survey's finer mesh from 15 min to 30 days (this one is lumped and coarser, 700 nodes)."""
    got = gr.step_response(soil, [h * 3600 for h in SURVEY])
    for (h, want), q in zip(SURVEY.items(), got, strict=True):
        assert q == pytest.approx(want, rel=0.015), h


def test_early_and_late_limits(soil: gr.Ground) -> None:
    """Early the floor's middle is the semi-infinite slab, A k ΔT/√(παt), and the edge adds to it;
    late the steady disc, S = 2D on a half-space (Incropera case 10), a few per cent more in the
    finite 8 m domain (the survey's 2.541 m)."""
    alpha = gr.DRY.k / (gr.DRY.rho * gr.DRY.c)
    t = 900.0
    slab = DISC * gr.DRY.k / math.sqrt(math.pi * alpha * t)
    (q,) = gr.step_response(soil, [t])
    assert slab < q < 1.15 * slab
    s = gr.steady(soil)
    assert s == pytest.approx(2.541, rel=0.015)
    assert 1.0 < s / (2 * 1.2) < 1.08


def test_the_rows_hold_at_steady_state(soil: gr.Ground) -> None:
    """The DAE's rows vanish on the steady field, and the heat into the soil is its conductance."""
    k = soil.stiffness
    u = np.zeros(soil.nodes)
    u[soil.disc] = 1.0
    import scipy.sparse as sp
    import scipy.sparse.linalg as spla

    kff = sp.csc_matrix(k[soil.free][:, soil.free])
    solved: Any = spla.spsolve(kff, -(k[soil.free][:, soil.disc] @ np.ones(len(soil.disc))))
    u[soil.free] = np.asarray(solved)
    free = u[soil.free]
    assert np.abs(soil.rows(free, np.zeros(len(free)), 1.0, 0.0)).max() < 1e-9
    assert soil.into(free, 1.0, 0.0, 0.0) == pytest.approx(gr.steady(soil), rel=1e-9)
    assert soil.disc_capacity > 0
    assert soil.into(free, 1.0, 0.0, 1.0) - soil.into(free, 1.0, 0.0, 0.0) == pytest.approx(
        soil.disc_capacity
    )


def test_a_ground_too_small_is_refused() -> None:
    with pytest.raises(ValueError, match="four of the disc's radii"):
        gr.ground(DISC, extent=1.0)
    assert gr.DAMP.k == 1.5


@pytest.mark.slow
@pytest.mark.geometry
def test_a_thin_floor_on_the_ground_fires() -> None:
    """The 36 ft³ cross-draft with a 2½ in dense floor, on the ground and on a stand (test
    inputs): the coupled soil runs, the balance closes, and the floor on dry soil loses less than
    one hot underneath in still air over 20 h, so the setting ends hotter."""
    thin = {"lining.floor": [{"material": "firebrick-medium-duty-smithfield",
                              "thickness": "2.5 in"}]}  # fmt: skip
    ends = {}
    for on in (False, True):
        k = hc._crossdraft(hc.FLUE | thin | {"chamber.on_ground": on})  # pyright: ignore[reportPrivateUsage]
        m = hk.heat_model(k, hc.CROSSDRAFT_LOAD, 1.0, n_rays=20_000)
        assert (m.ground is not None) == on
        f = fi.fire(m, fi.FixedInput(hc._burners(k, m)), 20 * 3600.0, sample=1800.0)  # pyright: ignore[reportPrivateUsage]
        e = f.energy
        closure = e["fuel heat"] - e["flue"] - e["walls"] - e["setting"] - e["openings"]
        assert abs(closure) < 1e-9 * e["fuel heat"]
        ends[on] = f.t_setting[-1]
    assert ends[True] > ends[False] + 20


@pytest.mark.slow
@pytest.mark.geometry
def test_a_ground_needs_its_wall() -> None:
    m = hc.fast_fire_model()
    with pytest.raises(ValueError, match="a ground needs one wall"):
        ZoneModel(m.products, m.exchange, m.names, m.faces, m.setting, m.openings, m.flow,
                  m.t_room, ground=gr.ground(1.0))  # fmt: skip
