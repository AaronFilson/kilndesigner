"""v2 statics: an arch on spreading supports (spread.py), negative case N5
(engine-v2-negative-cases.md §6, §8): the supports moved apart until the moved arch has no
admissible state, against Ochsendorf's test arch and Coccia, Di Carlo & Rinaldi's Eq. 18 (2015,
Int. J. Adv. Struct. Eng. 7:307–320)."""

import math
from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.model import Kiln
from kilndesigner.units import Q_
from kilndesigner.v2.statics.arch import ArchRing
from kilndesigner.v2.statics.spread import (
    collapse,
    first_hinge,
    kiln_rings,
    moved,
    rotation,
    stands,
)

ROOT = Path(__file__).resolve().parents[3]
IN = 0.0254


def olsen(name: str) -> Kiln:
    return load_design(ROOT / "examples" / "olsen" / f"{name}.yaml")


def eq18(x: float) -> float:
    """Coccia et al. 2015 Eq. 18, their regression of the collapse spread a side over the
    thickness against t/R (R the mean radius), for more than 25–30 voussoirs."""
    return (-365.44 * x**6 + 1022.5 * x**5 - 1167.8 * x**4 + 702.36 * x**3 - 238.84 * x**2
            + 44.62 * x - 2.766)  # fmt: skip


OCHSENDORF = ArchRing.semicircle(0.22, 0.05, 2000.0, voussoirs=16)
"""Ochsendorf's test arch as Coccia et al. describe it: 16 voussoirs, 50 mm thick, a 220 mm mean
radius, t/R 0.23."""


def test_ochsendorfs_test_arch() -> None:
    """Measured to collapse at a 15.4 % increase of the span, 16.9 % by Ochsendorf's static method,
    32.24 mm a side and 16.53 % by Coccia et al.'s kinematic one (no sliding, as they assume): v2
    32.22 mm and 16.52 %; with μ 0.6, 32.00 mm. The span's increase is over the inside span, 2u/S
    (Derived: 60 mm over 390 mm is the 15.4 %)."""
    c = collapse(OCHSENDORF, math.inf)
    assert c.u * 1000 == pytest.approx(32.24, abs=0.1)
    assert c.increase == pytest.approx(0.1653, abs=5e-4)
    assert (c.first, c.last) == (3, 3)  # the hinge at the joint 56¼° from the crown
    assert 0.154 < c.increase < 0.169
    assert collapse(OCHSENDORF, 0.6).u * 1000 == pytest.approx(32.0, abs=0.1)


@pytest.mark.parametrize(("x", "within"), [(0.15, 0.04), (0.25, 0.03)])
def test_against_coccia_et_al_eq_18(x: float, within: float) -> None:
    """96 voussoirs, no sliding: the collapse spread a side over the thickness within a few per
    cent of their regression of their own results (0.418 against 0.406; 0.799 against 0.783)."""
    ring = ArchRing.semicircle(1.0, x, 2000.0, voussoirs=96)
    assert collapse(ring, math.inf).u / x == pytest.approx(eq18(x), rel=within)


@pytest.mark.slow
def test_against_coccia_et_al_eq_18_more() -> None:
    for x, within in ((0.2, 0.03), (0.3, 0.02), (0.4, 0.01)):
        ring = ArchRing.semicircle(1.0, x, 2000.0, voussoirs=96)
        assert collapse(ring, math.inf).u / x == pytest.approx(eq18(x), rel=within)


def test_the_hinge_moves_toward_the_crown() -> None:
    """64 voussoirs at t/R 0.15: the unmoved arch's least thrust touches the intrados at joint 11
    and almost at 12; moved about 11 alone it would fall at u/t 0.30, but past that the arch moved
    about joint 12 stands, to 0.39 (32 voussoirs: 0.39; Eq. 18: 0.41)."""
    ring = ArchRing.semicircle(1.0, 0.15, 2000.0, voussoirs=64)
    c = collapse(ring, math.inf)
    assert (c.first, c.last) == (11, 12)
    assert c.u / 0.15 == pytest.approx(0.390, abs=0.005)
    assert not stands(ring, 11, 0.32 * 0.15, math.inf)
    assert stands(ring, 12, 0.32 * 0.15, math.inf)


def test_n5_past_its_spread_the_arch_falls() -> None:
    """N5: moved past its collapse spread no hinge leaves the arch an admissible state; just short
    of it, it stands."""
    c = collapse(OCHSENDORF, 0.6)
    for k in (c.last, c.last + 1):
        assert not stands(OCHSENDORF, k, 1.02 * c.u, 0.6)
    assert stands(OCHSENDORF, c.last, 0.98 * c.u, 0.6)


def test_a_flat_arch_snaps_through_when_its_hinges_line_up() -> None:
    """The fast-fire arch (27 in, 1½ in/ft, 4½ in; Olsen pp.139–140) hinges at the springing's
    intrados and the crown's extrados; a straight line fits in it, so it stands until the three
    hinges line up, 2.13 in a side (|d| − |d_x|)."""
    ring = ArchRing.from_span_rise(27 * IN, 3.375 * IN, 4.5 * IN, 513.0, voussoirs=14)
    c = collapse(ring, 0.6)
    assert c.first == 0
    sec = ring.section()
    h, top = sec.joints[0].points[0], sec.joints[7].points[1]
    reach = math.hypot(top[0] - h[0], top[1] - h[1]) - abs(top[0] - h[0])
    assert c.u == pytest.approx(reach, rel=2e-3)
    assert c.u / IN == pytest.approx(2.13, abs=0.01)
    assert rotation(h, top, reach) is None
    assert moved(ring, 0, reach) is None
    assert not stands(ring, 0, reach)


def test_what_the_spreading_refuses() -> None:
    with pytest.raises(ValueError, match="even number"):
        moved(ArchRing.semicircle(1.0, 0.2, 2000.0, voussoirs=15), 3, 0.01)
    with pytest.raises(ValueError, match="between the springing and the crown"):
        moved(OCHSENDORF, 8, 0.01)
    thick = ArchRing.semicircle(1.0, 0.4, 2000.0, voussoirs=16)
    with pytest.raises(ValueError, match="sliding governs"):
        first_hinge(thick, 0.6)  # the crown's steep joints at their friction limit
    with pytest.raises(ValueError, match="no admissible state"):
        first_hinge(ArchRing.semicircle(1.0, 0.09, 2000.0, voussoirs=16))


def test_a_kilns_own_rings() -> None:
    """From the design file: meaders-david's 60 in half circle, 9 in of K-26, 50 voussoirs (one a
    2½ in course of its extrados); Tobe's 10 ft chambers, one ring for its seven equal arches;
    Kannofen's at its widest station; a crossing, a dome or uneven springings refused."""
    (label, ring), = kiln_rings(olsen("meaders-david"))  # fmt: skip
    assert label == "across"
    assert ring.span == pytest.approx(60 * IN)
    assert ring.thickness == pytest.approx(9 * IN)
    assert ring.voussoirs == 50
    (label, tobe), = kiln_rings(olsen("tobe"))  # fmt: skip
    assert label == "chamber 1"
    assert tobe.span == pytest.approx(120 * IN)
    (_, kf), = kiln_rings(olsen("kannofen"))  # fmt: skip
    assert kf.span == pytest.approx(1.07, abs=0.01)
    xd = kiln_rings(olsen("olsen-crossdraft-36"))[0][1]
    assert xd.overburden
    assert xd.overburden[0].thickness == pytest.approx(4.5 * IN)
    for name, words in (("singh-coal", "sprung arches"), ("church-skaelskor", "symmetrical"),
                        ("bowen-mountain", "symmetrical")):  # fmt: skip
        with pytest.raises(ValueError, match=words):
            kiln_rings(olsen(name))


def test_n5_through_a_reference_kilns_design() -> None:
    """N5 through the pipeline: meaders-david's half circle (t/R 0.26) stands with its springings
    6.3 in apart a side, 21 % of its span (Eq. 18 for t/R 0.26: 0.80 of its 9 in, 7.2 in); moved
    farther it falls. Its 3 in ring (N1's) can't stand even unmoved."""
    (_, ring), = kiln_rings(olsen("meaders-david"))  # fmt: skip
    c = collapse(ring, 0.6)
    assert c.u / IN == pytest.approx(6.34, abs=0.05)
    assert c.increase == pytest.approx(0.211, abs=0.002)
    assert not stands(ring, c.last, c.u + 0.1 * IN)
    md = olsen("meaders-david")
    thin = md.model_copy(
        update={
            "lining": md.lining.model_copy(
                update={
                    "roof": [md.lining.walls[0].model_copy(update={"thickness": Q_(3, "inch")})]
                }
            )
        }
    )
    (_, three), = kiln_rings(thin)  # fmt: skip
    with pytest.raises(ValueError, match="no admissible state unmoved"):
        collapse(three)


@pytest.mark.slow
def test_no_reference_arch_is_near_its_spread() -> None:
    """Every reference kiln's arch, cold (μ 0.6): the least collapse spread is the 100 ft³ kit's,
    6.7 % of its span (2.16 in a side), then updraft-test-4's 7.6 % and the 50 ft³ kit's 8.1 %;
    Tobe's 10 ft semicircle of 13½ in (the owner, 2026-11-17) 15.1 % (9.05 in a side). As built
    their supports are held (a frame or masonry); the most an arch moves against them for good is
    its brick's permanent shrinkage, at most 1.0 % (Morgan K-26 at 2552 °F, the 2025 sheet;
    morgan-k-ifb-sheets.md §6): N5's criterion condemns none."""
    least: dict[str, float] = {}
    for path in sorted((ROOT / "examples" / "olsen").glob("*.yaml")):
        try:
            rings = kiln_rings(load_design(path))
        except ValueError:
            continue
        for label, ring in rings:
            try:
                least[f"{path.stem} {label}"] = collapse(ring, 0.6).increase
            except ValueError:
                continue  # sliding governs the unmoved ring: not a three-hinge case
    worst = min(least, key=lambda k: least[k])
    assert worst == "olsen-kit-100 across"
    assert least[worst] == pytest.approx(0.0668, abs=5e-4)
    assert least["tobe chamber 1"] == pytest.approx(0.1509, abs=5e-4)
    assert all(v > 0.01 for v in least.values())
    assert len(least) >= 40
