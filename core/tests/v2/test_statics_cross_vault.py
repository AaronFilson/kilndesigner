"""v2 statics: crossing vaults (roof.crossing), sliced both ways through the groin solid and coupled
where the slices cross (cross_vault.py). Each family's compressive stress field adds to the
other's, so an admissible state of the grid is one of the vault: the safe theorem (Heyman 1966)."""

import math
from pathlib import Path
from typing import Any

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.groin import GroinLayer, tubes
from kilndesigner.model import Kiln, SprungArch
from kilndesigner.units import Q_, si
from kilndesigner.v2.statics import sources
from kilndesigner.v2.statics.blocks import G
from kilndesigner.v2.statics.cross_vault import CREASE, analyse, not_modelled, slices
from kilndesigner.v2.statics.kiln import statics
from kilndesigner.v2.statics.section import NotModelledError

ROOT = Path(__file__).resolve().parents[3]
LBFT = 4.4482216152605 / 0.3048  # N/m in a lbf/ft


def olsen(name: str) -> Kiln:
    return load_design(ROOT / "examples" / "olsen" / f"{name}.yaml")


def with_roof(kiln: Kiln, **update: Any) -> Kiln:
    roof = kiln.roof
    assert isinstance(roof, SprungArch)
    return kiln.model_copy(update={"roof": roof.model_copy(update=update)})


def with_crossing(kiln: Kiln, **update: Any) -> Kiln:
    roof = kiln.roof
    assert isinstance(roof, SprungArch)
    assert roof.crossing is not None
    return with_roof(kiln, crossing=roof.crossing.model_copy(update=update))


def with_shell(kiln: Kiln, *layers: tuple[str, float]) -> Kiln:
    shell = kiln.lining.for_face("roof")[0]
    roof = [shell.model_copy(update={"material": m, "thickness": Q_(t, "inch")}) for m, t in layers]
    return kiln.model_copy(update={"lining": kiln.lining.model_copy(update={"roof": roof})})


def solid(kiln: Kiln, inner: float, outer: float) -> float:
    """m³ of the groin solid between ``inner`` and ``outer`` out, over the inside plan."""
    main, cross = tubes(kiln, "m")
    lo, hi = (-main.span / 2, -cross.span / 2), (main.span / 2, cross.span / 2)
    return GroinLayer((main, cross), inner, outer).volume(lo, hi, 400)


def test_the_slices_weigh_what_the_vault_does() -> None:
    """The Church kiln's 6 in cast shell: each family carries half of every strip, so the two
    together weigh what the groin solid over the chamber does (its volume summed column by column,
    `GroinLayer`), to 0.2 %."""
    kiln = olsen("church-skaelskor")
    cut = slices(kiln)
    assert len(cut) == 18
    rho = sources.density("kast-o-lite-26-li-plus")
    weight = sum(w for s in cut for w, _ in s.loads)
    assert weight == pytest.approx(rho * G * solid(kiln, 0.0, 0.1524), rel=2e-3)


def test_the_joints_are_radial_on_their_own_vault_and_plumb_on_the_other() -> None:
    """The slice across the width nearest the front wall: under the chamber's own vault in the
    middle, its joints radial to that vault's circle; out by the walls it runs along the crossing
    vault's generators, its joints plumb; none within 1.2 shell thicknesses of the groins, and its
    ends plumb at the walls' inside faces."""
    kiln = olsen("church-skaelskor")
    main, cross = tubes(kiln, "m")
    edge = slices(kiln)[0]
    assert edge.family == 0
    t = 0.1524
    z_cross = cross.centre_z + math.sqrt(cross.radius**2 - (edge.at - cross.centre) ** 2)
    groin = math.sqrt(main.radius**2 - (z_cross - main.centre_z) ** 2)  # where the two meet
    assert 0 < groin < main.span / 2
    radial = plumb = 0
    for lo, up in edge.joints:
        if abs(lo[0]) < groin:  # under the chamber's own vault
            cross_product = (up[0] - lo[0]) * (lo[1] - main.centre_z) - (up[1] - lo[1]) * lo[0]
            assert cross_product == pytest.approx(0.0, abs=1e-9)
            radial += 1
        else:
            assert up[0] == lo[0]
            plumb += 1
    assert radial > 10
    assert plumb >= 2
    for lo, _ in edge.joints[1:-1]:
        assert abs(abs(lo[0]) - groin) > CREASE * t
    (first, top), (last, _) = edge.joints[0], edge.joints[-1]
    assert first[0] == pytest.approx(-main.span / 2)
    assert last[0] == pytest.approx(main.span / 2)
    assert top[0] == first[0]


def test_the_church_kilns_vault_stands_and_pushes_its_walls() -> None:
    """The Church kiln's cast vaults, 31 and 34 in rises over its 7 ft crossing, on buttressed
    walls: an admissible state cold, the least peak push on the walls about 189 lbf/ft."""
    cold = analyse(olsen("church-skaelskor"), "cold")
    assert cold.stands
    assert not cold.analogy
    assert cold.peak / LBFT == pytest.approx(188.9, abs=0.5)
    assert cold.steps[0].value.endswith("an admissible state")
    assert "least peak push" in cold.steps[1].name


@pytest.mark.slow
def test_the_two_crossing_vaults_stand_cold_and_hot() -> None:
    """Olsen's Church and Fireworks kilns: both stand cold and hot; hot, with less friction, their
    walls must give more."""
    want = {"church-skaelskor": (188.9, 208.6), "fireworks-edmonton": (255.9, 299.2)}
    for name, (cold, hot) in want.items():
        r = statics(olsen(name))
        assert r.kind == "crossing vault", name
        assert r.stands == {"cold": True, "hot": True}, name
        assert r.numbers["least peak push on the walls, cold"] / LBFT == pytest.approx(
            cold, abs=0.5
        )
        assert r.numbers["least peak push on the walls, hot"] / LBFT == pytest.approx(hot, abs=0.5)


@pytest.mark.slow
def test_more_slices_change_the_peak_little() -> None:
    """5, 9 and 13 slices each way: the least peak push settles (2877, 2757, 2748 N/m)."""
    kiln = olsen("church-skaelskor")
    p5, p9, p13 = (analyse(kiln, "cold", n).peak for n in (5, 9, 13))
    assert abs(p5 - p9) / p9 < 0.05
    assert abs(p9 - p13) / p9 < 0.005


def test_a_shell_too_thin_for_its_spans_falls() -> None:
    """The Church kiln's vaults cast 1½ in thick: no state of the grid, cold or hot (the model can
    fail a vault; it is never fitted to stand one)."""
    kiln = with_shell(olsen("church-skaelskor"), ("kast-o-lite-26-li-plus", 1.5))
    r = statics(kiln)
    assert r.stands == {"cold": False, "hot": False}
    assert math.isnan(r.numbers["least peak push on the walls, cold"])
    assert r.steps[0].value.endswith("none")


def test_layers_over_the_shell_are_its_load() -> None:
    """2 in of K-23 laid over the Church kiln's shell: the slices carry its weight, the solid
    between 6 and 8 in out, and the walls must give more."""
    kiln = olsen("church-skaelskor")
    covered = with_shell(kiln, ("kast-o-lite-26-li-plus", 6), ("ifb-k23", 2))
    extra = sum(w for s in slices(covered) for w, _ in s.loads) - sum(
        w for s in slices(kiln) for w, _ in s.loads
    )
    want = sources.density("ifb-k23") * G * solid(kiln, 0.1524, 0.2032)
    assert extra == pytest.approx(want, rel=5e-3)
    assert analyse(covered, "cold").peak > analyse(kiln, "cold").peak


def test_what_the_slicing_refuses() -> None:
    kiln = olsen("church-skaelskor")
    assert not_modelled(kiln) is None
    assert "not a crossing" in str(not_modelled(olsen("fast-fire")))
    assert "off the chamber's middle" in str(not_modelled(with_crossing(kiln, at=Q_(30, "inch"))))
    assert not_modelled(with_crossing(kiln, at=Q_(42, "inch"))) is None
    assert "arms" in str(not_modelled(with_crossing(kiln, length=Q_(9, "ft"))))
    assert "narrower or wider" in str(not_modelled(with_crossing(kiln, span=Q_(6, "ft"))))
    assert "frame" in str(not_modelled(with_roof(kiln, buttressed=False)))
    two = with_shell(kiln, ("kast-o-lite-26-li-plus", 4), ("ifb-k26", 2))
    assert not_modelled(two) is None  # the layer over the shell is its load
    bonded = with_roof(two, ring=2, rings_bonded=True)
    assert "different materials" in str(not_modelled(bonded))
    with pytest.raises(NotModelledError, match="not a crossing"):
        analyse(olsen("fast-fire"), "cold")
    r = statics(with_crossing(kiln, length=Q_(9, "ft")))
    assert r.kind == "crossing vault"
    assert r.all_stand is None
    assert r.steps[0].name == "Not modelled"


def test_a_hot_verdict_resting_on_dense_bricks_stand_in_alone_isnt_given() -> None:
    """The Fireworks kiln's vaults in 6 in of dense firebrick: with the 25 psi stand-in carried
    over from IFB by analogy, halved for each family of slices, no state hot; without it one; the
    verdict isn't given, the missing data said."""
    kiln = with_shell(olsen("fireworks-edmonton"), ("firebrick-medium-duty-smithfield", 6))
    r = statics(kiln)
    assert r.stands == {"cold": True, "hot": None}
    assert "dense brick's hot crushing" in str(r.missing)
    assert any("analogy" in s.name for s in r.steps)
    assert si(Q_(r.numbers["least peak push on the walls, cold"], "N/m"), "lbf/ft") > 255.9
