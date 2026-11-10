"""v2 statics: domes over square, oblong and curved plans (sail domes), sliced into arches across
their width, each on its walls (sail.py). Heyman's slicing gives a lower bound: if every strip
stands, the dome does (Heyman 1977 p.109, via Lau 2006 p.35)."""

import math
from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.model import Dome, Kiln
from kilndesigner.outline import rectangle
from kilndesigner.units import Q_
from kilndesigner.v2.statics.kiln import statics
from kilndesigner.v2.statics.sail import SphereShell, analyse, not_modelled, shells, strips
from kilndesigner.v2.statics.section import NotModelledError

ROOT = Path(__file__).resolve().parents[3]
LBFT = 4.4482216152605 / 0.3048  # N/m in a lbf/ft


def olsen(name: str) -> Kiln:
    return load_design(ROOT / "examples" / "olsen" / f"{name}.yaml")


def test_a_vertical_plane_cuts_a_spherical_shell_in_a_ring_of_one_thickness() -> None:
    """Miravet's sail dome over its 8 × 8 ft chamber: the sphere through the chamber's corners,
    36 in above them at the middle (Fig 6-19); each strip a ring between √(R² − v²) and
    √((R + T)² − v²), as thick as the shell at the middle and thicker towards the walls."""
    kiln = olsen("miravet")
    (shell,) = shells(kiln)
    assert shell.radius == pytest.approx((2 * 1.2192**2 + 0.9144**2) / (2 * 0.9144), rel=1e-9)
    cut = strips(kiln, shell)
    assert len(cut) == 18
    middle = min(cut, key=lambda s: abs(s.at))
    edge = cut[0]
    assert middle.ring.thickness == pytest.approx(shell.thickness, rel=2e-3)
    assert edge.ring.thickness > middle.ring.thickness
    v = edge.at - shell.centre[1]
    want = math.sqrt((shell.radius + shell.thickness) ** 2 - v * v)
    assert edge.ring.radius + edge.ring.thickness == pytest.approx(want, rel=1e-9)
    assert edge.springing == pytest.approx(shell.springline, abs=1e-3)  # at the corner


@pytest.mark.slow
def test_the_three_sail_domes_stand_on_their_walls() -> None:
    """Miravet's dense-brick sail dome on its 36 in walls, Calimpong's cast dome over a teardrop
    (a curved plan) and Hollyweird's two cast domes in a row: every strip of each stands, cold and
    hot, on its buttressed walls."""
    for name in ("miravet", "conrad-teardrop", "hollyweird"):
        r = statics(olsen(name))
        assert r.kind == "sail dome", name
        assert r.stands == {"cold": True, "hot": True}, name
    hot = analyse(olsen("miravet"), "hot")
    assert hot.least / LBFT == pytest.approx(99.5, abs=1.0)
    assert any("most any strip" in s.name for s in hot.steps)
    assert len(shells(olsen("hollyweird"))) == 2  # a dome over each chamber


def test_layers_over_the_shell_are_its_load() -> None:
    """A layer laid over the shell (not bonded to it) loads each strip, its section's thickness
    growing towards the walls as the shell's does."""
    kiln = olsen("miravet")
    shell_layer = kiln.lining.for_face("roof")[0]
    cover = shell_layer.model_copy(update={"thickness": Q_(3, "inch")})
    covered = kiln.model_copy(update={"lining": kiln.lining.model_copy(
        update={"roof": [shell_layer, cover]})})  # fmt: skip
    (shell,) = shells(covered)
    assert shell.over == (pytest.approx((0.0762, shell.over[0][1])),)
    cut = strips(covered, shell)
    assert all(len(s.ring.overburden) == 1 for s in cut)
    assert cut[0].ring.overburden[0].thickness > 0.0762


def test_a_shell_too_thin_for_its_span_falls() -> None:
    """Miravet's dome at 0.3 in: no strip's thrust line fits, cold or hot; a real fall, not one
    resting on a stand-in, so the hot verdict is given (the model's verdict, never a flag)."""
    kiln = olsen("miravet")
    thin = kiln.lining.for_face("roof")[0].model_copy(update={"thickness": Q_(0.3, "inch")})
    k = kiln.model_copy(update={"lining": kiln.lining.model_copy(update={"roof": [thin]})})
    cold, hot = analyse(k, "cold"), analyse(k, "hot")
    assert not cold.stands
    assert not hot.stands
    assert not hot.analogy
    assert math.isnan(cold.least)
    assert statics(k).stands == {"cold": False, "hot": False}


def test_a_sphere_that_doesnt_reach_over_the_plan_makes_no_strips() -> None:
    """A strip is cut only where the sphere arches over the plan's width."""
    shell = SphereShell(rectangle(2.0, 2.0), (0.0, 0.0, 0.0), 0.5, 0.0, 0.1, ())
    assert strips(olsen("miravet"), shell) == []


def test_what_the_slicing_refuses() -> None:
    kiln = olsen("miravet")
    assert not_modelled(kiln) is None
    assert "is a dome" in str(not_modelled(olsen("fast-fire")))
    assert "revolution" in str(not_modelled(olsen("singh-coal")))
    walls = [kiln.lining.walls[0], kiln.lining.walls[0].model_copy(update={"material": "ifb-k23"})]
    mixed = kiln.model_copy(update={"lining": kiln.lining.model_copy(update={"walls": walls})})
    assert "several materials" in str(not_modelled(mixed))
    roof = kiln.roof
    assert isinstance(roof, Dome)
    shell = kiln.lining.for_face("roof")[0]
    two = kiln.model_copy(update={
        "roof": roof.model_copy(update={"ring": 2, "rings_bonded": True}),
        "lining": kiln.lining.model_copy(update={"roof": [
            shell, shell.model_copy(update={"material": "ifb-k26"})]}),
    })  # fmt: skip
    assert "different materials" in str(not_modelled(two))
    with pytest.raises(NotModelledError, match="revolution"):
        analyse(olsen("singh-coal"), "cold")
    r = statics(mixed)
    assert r.all_stand is None
    assert r.steps[0].name == "Not modelled"


def test_a_hot_verdict_resting_on_dense_bricks_stand_in_alone_isnt_given() -> None:
    """A wide, flat dense-brick sail dome (Miravet widened to 16 ft, rising 12 in): the stress
    block takes about ρgL²/(8fσ) of each joint, whatever its thickness, so with the 25 psi stand-in
    carried over from IFB by analogy no state stands hot, and without it one does; the verdict
    isn't given."""
    kiln = olsen("miravet")
    wide = kiln.chamber.model_copy(update={"width": Q_(16, "ft"), "depth": Q_(16, "ft")})
    roof = kiln.roof
    assert isinstance(roof, Dome)
    k = kiln.model_copy(update={"chamber": wide, "roof": roof.model_copy(
        update={"rise": Q_(12, "inch")})})  # fmt: skip
    hot = analyse(k, "hot")
    assert not hot.stands
    assert hot.analogy
    assert any("analogy" in s.name for s in hot.steps)
    r = statics(k)
    assert r.stands["hot"] is None
    assert "dense brick's hot crushing" in str(r.missing)
