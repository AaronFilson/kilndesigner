"""v2 statics: the must-fail cases N1–N6 against the reference kilns (engine-v2-negative-cases.md
§8; the owner's rule of 2026-11-10: "if the n1-n6 are in conflict with the reference kilns, those
need to change"). Each case's criterion is checked on every reference kiln as built, with v2's own
geometry; a criterion that would condemn one is restated, never the kiln; then the case, as stated
or restated, fails in v2's numbers. N4 is in test_statics_section.py, N5 in test_statics_spread.py.
"""

import math
from functools import cache
from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.model import Dome, Kiln, SprungArch
from kilndesigner.units import Q_, si
from kilndesigner.v2.statics import sail, sources
from kilndesigner.v2.statics.arch import ArchRing, least_thickness, on_walls, thrust
from kilndesigner.v2.statics.blocks import G
from kilndesigner.v2.statics.dome import least_thickness as dome_least
from kilndesigner.v2.statics.kiln import statics
from kilndesigner.v2.statics.rigid import Problem, Status, solve
from kilndesigner.v2.statics.spread import kiln_rings

ROOT = Path(__file__).resolve().parents[3]
OLSEN = ROOT / "examples" / "olsen"
IN = 0.0254


def olsen(name: str) -> Kiln:
    return load_design(OLSEN / f"{name}.yaml")


@cache
def least_arch(phi: float) -> float:
    """v2's least t/R of a circular arch of half angle φ (on the centre line's radius), on fixed
    supports under its own weight: Heyman's table by half angle, 0.1075 for a semicircle."""
    return least_thickness(1.0, phi, 2000.0, 0.6, voussoirs=40, tol=1e-4)


# ------------------------------------------------------------------------------------------ N1


@pytest.mark.slow
def test_n1_no_reference_arch_is_below_its_least_thickness() -> None:
    """N1's criterion, a circular arch's least t/R at its half angle, on every arch the reference
    kilns spring across or along (one ring of each size): none is below it. The nearest is Tobe's
    10 ft semicircle of 13½ in (not printed, p.90; the owner, 2026-11-17: not 9 in), t/R 0.2022,
    1.88 times its 0.1075; Kato's 1.93; the flat IFB arches 60–130 times."""
    ratios: dict[str, float] = {}
    for path in sorted(OLSEN.glob("*.yaml")):
        try:
            rings = kiln_rings(load_design(path))
        except ValueError:
            continue  # not a symmetrical sprung arch: domes, crossings (N2, N6), uneven springings
        for label, ring in rings:
            rc = ring.radius + ring.thickness / 2
            ratios[f"{path.stem} {label}"] = ring.thickness / rc / least_arch(ring.half_angle)
    worst = min(ratios, key=lambda k: ratios[k])
    assert worst == "tobe chamber 1"
    assert ratios[worst] == pytest.approx(1.88, abs=0.01)
    assert ratios["kato-coal across"] == pytest.approx(1.93, abs=0.02)
    assert all(r > 1.0 for r in ratios.values())
    assert len(ratios) == 42  # 39 kilns' rings, one of each size


def test_n1_the_semicircles_least() -> None:
    """The criterion itself: a semicircle needs 0.1075 of its centre line's radius (v2 at 40
    voussoirs within 0.3 %), a flat arch far less (the kits' 28°: 0.0012)."""
    assert least_arch(math.pi / 2) == pytest.approx(0.1075, rel=3e-3)
    assert least_arch(math.radians(28.07)) == pytest.approx(0.0012, abs=2e-4)


# ------------------------------------------------------------------------------------------ N2


def hemisphere(kiln: Kiln, thickness: float) -> Kiln:
    """singh-coal's dome raised to a hemisphere on its 84 in, ``thickness`` in thick (N2's)."""
    roof = kiln.roof
    assert isinstance(roof, Dome)
    shell = kiln.lining.for_face("roof")[0].model_copy(update={"thickness": Q_(thickness, "inch")})
    return kiln.model_copy(update={
        "roof": roof.model_copy(update={"rise": kiln.chamber.width / 2}),
        "lining": kiln.lining.model_copy(update={"roof": [shell]}),
    })  # fmt: skip


def test_n2_through_the_pipeline() -> None:
    """N2: singh-coal's 84 in dome raised to a hemisphere 1 in thick (t/R 0.024) has no admissible
    state on its wall, cold or hot; 2½ in thick (t/R 0.058, between Heyman's 0.042 and Lau's
    0.069) it stands, as N2+ is restated (§7)."""
    sc = olsen("singh-coal")
    thin = statics(hemisphere(sc, 1.0))
    assert thin.kind == "dome of revolution"
    assert thin.stands == {"cold": False, "hot": False}
    mid = statics(hemisphere(sc, 2.5))
    assert mid.stands["cold"] is True


def test_n2_restated_a_domes_least_falls_with_its_springing() -> None:
    """N2's criterion, the hemisphere's least t/R (Heyman 0.042; v2 0.0428; Lau's no-hoop 0.069),
    taken for any dome, would condemn the Calimpong teardrop's cast dome (5½ in on a 212 in sphere,
    t/R 0.026) and Hollyweird's (6 in on 128 in, 0.046, under Lau's 0.069). Restated: the limit is
    the hemisphere's. A spherical dome's least t/R falls with its springing angle (v2: with hoop
    forces 0.0003 at singh-coal's 59.5°, under 0.0002 at Breda's 53.1°; as lunes 0.040 and 0.037),
    and the sail domes' strips stand down to a few hundredths of an inch."""
    assert dome_least(1.0, math.pi / 2, 2000.0, 0.6, True, rings=40) == pytest.approx(
        0.0428, abs=5e-4
    )
    singh = dome_least(1.0, math.radians(59.5), 2000.0, 0.6, False, rings=40)
    breda = dome_least(1.0, math.radians(53.1), 2000.0, 0.6, False, rings=40)
    assert singh == pytest.approx(0.040, abs=1e-3)
    assert breda == pytest.approx(0.037, abs=1e-3)
    assert dome_least(1.0, math.radians(59.5), 2000.0, 0.6, True, rings=40) < 1e-3
    for name, built, lunes in (("singh-coal", 0.169, singh), ("breda-bottle", 0.077, breda)):
        kiln = olsen(name)
        roof = kiln.roof
        assert isinstance(roof, Dome)
        a, h = si(kiln.chamber.width, "m") / 2, si(roof.rise, "m")
        t = si(kiln.lining.for_face("roof")[0].thickness, "m")
        r = (a * a + h * h) / (2 * h)
        assert t / (r + t / 2) == pytest.approx(built, abs=1e-3)
        assert t / (r + t / 2) > 2 * lunes
    for name, ratio in (("conrad-teardrop", 0.026), ("hollyweird", 0.046)):
        kiln = olsen(name)
        shell = sail.shells(kiln)[0]
        t = shell.thickness
        assert t / (shell.radius + t / 2) == pytest.approx(ratio, abs=1e-3)
        assert t / (shell.radius + t / 2) < 0.069
        assert sail.analyse(kiln, "cold").stands
        layer = kiln.lining.for_face("roof")[0].model_copy(update={"thickness": Q_(0.25, "inch")})
        lining = kiln.lining.model_copy(update={"roof": [layer]})
        assert sail.analyse(kiln.model_copy(update={"lining": lining}), "cold").stands  # ¼ in


# ------------------------------------------------------------------------------------------ N3


def walls_alone(name: str) -> tuple[float, bool]:
    """A kiln's ring on its two walls standing alone (arch.on_walls, held by nothing): the bare
    rule's ratio H·h/(W·b/2), the arch's least thrust against the wall's own weight, and whether
    v2's section, every force on the wall counted, stands."""
    kiln = olsen(name)
    roof = kiln.roof
    assert isinstance(roof, SprungArch)
    (_, ring), = kiln_rings(kiln)  # fmt: skip
    h = si(kiln.chamber.height, "m")
    b = sum(si(x.thickness, "m") for x in kiln.lining.walls)
    rho = sum(sources.density(x.material) * si(x.thickness, "m") for x in kiln.lining.walls) / b
    ring40 = ArchRing(ring.radius, ring.thickness, ring.half_angle, ring.density, 1.0, 40,
                      ring.overburden)  # fmt: skip
    bare = thrust(ring40, 0.6, 1).value * h / (rho * G * b * h * b / 2)
    sec = on_walls(ring40, b, h, rho, max(1, round(h / sources.COURSE.value)), "none")
    return bare, solve(Problem(sec, (0.6,) * len(sec.joints))).status is Status.OPTIMAL


def test_n3_the_bare_rule_restated() -> None:
    """N3's rule as §2 wrote it, a wall alone overturns when H·h > W·b/2, leaves out the arch's
    own weight on the wall's top. It would condemn six reference kilns whose walls carry their half
    circles alone in v2 (Kitade's frame and the others' buttresses giving nothing): restated, the
    wall falls when the resultant of everything on it, the arch's vertical load where it bears
    included, leaves its base (v2's LP). The fast-fire's 4½ in IFB walls still fall (N3)."""
    for name, ratio in (
        ("kitade-tojilo", 2.01),
        ("kato-coal", 1.15),
        ("bae-gilgama", 2.24),
        ("meaders-cheever", 3.16),
        ("anagama-hole", 3.39),
        ("tamba", 4.81),
    ):
        bare, stands = walls_alone(name)
        assert bare == pytest.approx(ratio, abs=0.02), name
        assert stands, name
    bare, stands = walls_alone("fast-fire")
    assert bare == pytest.approx(5.18, abs=0.02)
    assert not stands


# ------------------------------------------------------------------------------------------ N6


def test_n6_the_crossings_against_the_corner_supported_vault() -> None:
    """N6's limit (Maia Avelino et al., SAHC 2020 §4.3): a rounded cross vault on its four corners
    needs t'/R 0.061 with the cross diagram (0.084 the fan's), R half the larger span (their t/R
    0.10 is 0.5 m on 10 m). The two crossing kilns' 6 in cast shells: Church 0.143, Fireworks
    0.111 by that R. On the flatter vault's own centre-line radius Fireworks is 0.079, under the
    fan's 0.084: restated, the limit is the corner-supported vault's, R as the source takes it, and
    the fan's 0.084 is a force pattern's, not the vault's (the cross diagram stands it thinner)."""
    for name, by_span, flat in (("church-skaelskor", 0.143, 0.128),
                                ("fireworks-edmonton", 0.111, 0.079)):  # fmt: skip
        kiln = olsen(name)
        roof = kiln.roof
        assert isinstance(roof, SprungArch)
        assert roof.crossing is not None
        t = si(kiln.lining.for_face("roof")[0].thickness, "m")
        spans = [(si(kiln.chamber.width, "m"), si(roof.rise, "m")),
                 (si(roof.crossing.span, "m"), si(roof.crossing.rise, "m"))]  # fmt: skip
        assert t / (max(s for s, _ in spans) / 2) == pytest.approx(by_span, abs=1e-3)
        assert t / (max(s for s, _ in spans) / 2) > 0.084
        radii = [s * s / (8 * h) + h / 2 for s, h in spans]
        assert t / (max(radii) + t / 2) == pytest.approx(flat, abs=1e-3)


@pytest.mark.slow
def test_n6_restated_the_kilns_vaults_thinned_fall() -> None:
    """The kilns' case, vaults on walls all round: the Fireworks kiln's shell cast 2 in thick
    (v2's least 2.21 in, 11-09-26.md §H item 11) has no state of the grid cold; the Church kiln's
    at 1½ in is test_statics_cross_vault.py's."""
    fw = olsen("fireworks-edmonton")
    layer = fw.lining.for_face("roof")[0].model_copy(update={"thickness": Q_(2.0, "inch")})
    thin = fw.model_copy(update={"lining": fw.lining.model_copy(update={"roof": [layer]})})
    from kilndesigner.v2.statics.cross_vault import analyse

    assert not analyse(thin, "cold").stands
