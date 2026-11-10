"""v2 statics: domes of revolution as rigid rings with hoop compression (dome.py), against
published least thicknesses (domes-over-doors.md §D1; engine-v2-negative-cases.md N2) and the
round reference kilns."""

import math
from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.v2.statics.dome import (
    DomeShell,
    kiln_dome,
    kiln_not_modelled,
    least_thickness,
    problem,
    section,
    springing_thrust,
    stands,
)
from kilndesigner.v2.statics.rigid import Status, assemble, force_on, solve
from kilndesigner.v2.statics.section import NotModelledError

ROOT = Path(__file__).resolve().parents[3]
IN = 0.0254


def olsen(name: str):
    return load_design(ROOT / "examples" / "olsen" / f"{name}.yaml")


def test_a_hemisphere_needs_four_per_cent() -> None:
    """With hoop compression the hemisphere needs t/R 0.0428 of its mid-surface radius: Heyman's
    0.042, Nodargi and Bisegna's refined 0.04284. Cracked into lunes the same: hoop compression is
    never active at the limit (Lau's 0.069 for lunes isn't reproduced: an open question)."""
    hoops = least_thickness(1.0, math.pi / 2, 2000.0, 0.6, True)
    assert hoops == pytest.approx(0.04284, abs=2e-4)
    assert least_thickness(1.0, math.pi / 2, 2000.0, 0.6, False) == pytest.approx(hoops, rel=1e-3)


def test_n2_a_hemisphere_a_inch_thick_falls() -> None:
    """N2: singh-coal's dome as a 1 in hemisphere, t/R 0.024, has no admissible state, with or
    without hoop force; t/R 0.10 stands, its least thrust 19.5 % of its weight (the TNA's 19.8 %,
    Lau's 'about 20 %', masonry-statics.md M2–M3)."""
    thin = DomeShell.hemisphere(1.0, 0.024, 2000.0)
    assert not stands(thin, 0.6, True)
    assert not stands(thin, 0.6, False)
    shell = DomeShell.hemisphere(1.0, 0.10, 2000.0)
    assert stands(shell, 0.6)
    assert springing_thrust(shell, 0.6) / shell.weight == pytest.approx(0.195, abs=0.005)
    assert math.isnan(springing_thrust(thin, 0.6))
    assert math.isnan(least_thickness(1.0, math.pi / 2, 2000.0, 0.05))  # slides at any thickness


def test_a_dome_on_a_wall_with_a_band() -> None:
    """A shallow cap (84 in across, 24 in rise, 9 in) on a 4½ in wall 60 in high doesn't stand;
    a band at the springline holds it, pulling the least it must."""
    shell = DomeShell.from_span_rise(84 * IN, 24 * IN, 9 * IN, 2050.0, rings=30)
    wall = (4.5 * IN, 60 * IN, 2050.0, 24)
    assert solve(problem(section(shell, True, wall), 0.6)).status is Status.INFEASIBLE
    banded = section(shell, True, wall, band=60 * IN)
    p = problem(banded, 0.6)
    pull = solve(p, force_on(assemble(p), banded, "band", 0), 1)
    assert pull.status is Status.OPTIMAL
    assert pull.value > 0  # the wall pushes out on the band: its tension per radian
    low = section(shell, True, wall, band=30 * IN)  # halfway down: the wall above it overturns
    assert solve(problem(low, 0.6)).status is Status.INFEASIBLE
    loaded = section(shell, True, overburden=[(2 * IN, 500.0)])
    assert all(len(b.loads) == 1 for b in loaded.bodies if b.tag == "ring")
    half = DomeShell.hemisphere(1.0, 0.1, 2000.0, rings=20)  # springs level from its wall's top
    level = section(half, True, (0.3, 0.5, 2000.0, 4))
    assert not any(b.tag == "skewback" for b in level.bodies)
    assert solve(problem(level, 0.6)).status is Status.OPTIMAL


def test_shells_need_their_sizes() -> None:
    with pytest.raises(ValueError, match="positive"):
        DomeShell(1.0, 0.0, 1.0, 2000.0)
    with pytest.raises(ValueError, match="equator"):
        DomeShell(1.0, 0.1, 2.0, 2000.0)
    with pytest.raises(ValueError, match="two rings"):
        DomeShell(1.0, 0.1, 1.0, 2000.0, rings=1)
    with pytest.raises(ValueError, match="rise"):
        DomeShell.from_span_rise(1.0, 0.6, 0.1, 2000.0)


def test_the_round_kilns_domes_stand() -> None:
    """singh-coal (84 in across, 24 in rise, 9 in on a 13½ in wall, no band, pp.133–135) and the
    Breda bottle kiln (180 in, 45 in rise assumed, 24 in wall, p.167) stand cold and hot, with
    hoops and as lunes; the box and curved-plan domes are refused with their reason."""
    for name in ("singh-coal", "breda-bottle"):
        for state in ("cold", "hot"):
            r = kiln_dome(olsen(name), state)
            assert r.stands
            assert r.stands_as_lunes
            assert r.thrust > 0
            assert r.steps[0].name == "The dome as rings of revolution"
    assert "sail dome" in str(kiln_not_modelled(olsen("miravet")))
    assert "not a dome" in str(kiln_not_modelled(olsen("fast-fire")))
    assert kiln_not_modelled(olsen("singh-coal")) is None
    with pytest.raises(NotModelledError, match="sail dome"):
        kiln_dome(olsen("conrad-teardrop"))
    sc = olsen("singh-coal")
    mixed = sc.model_copy(update={"lining": sc.lining.model_copy(
        update={"walls": [*sc.lining.walls, *olsen("fast-fire").lining.walls]})})  # fmt: skip
    assert "several materials" in str(kiln_not_modelled(mixed))
