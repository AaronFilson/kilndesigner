"""v2 statics: the dispatcher (kiln.py) on edge cases, and rings of any shape (arch.ring_section,
arch.catenary_ring)."""

import math
from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.model import Kiln
from kilndesigner.units import Q_
from kilndesigner.v2.statics.arch import ArchRing, catenary_ring, ring_section, thrust
from kilndesigner.v2.statics.kiln import KilnStatics, statics
from kilndesigner.v2.statics.rigid import Problem, Status, assemble, force_on, solve

ROOT = Path(__file__).resolve().parents[3]


def olsen(name: str) -> Kiln:
    return load_design(ROOT / "examples" / "olsen" / f"{name}.yaml")


def test_a_ring_of_any_shape_meets_the_circular_one() -> None:
    """The circular ring's points through ring_section: its voussoirs' straight chords lose a
    little weight against the exact sectors, so the least thrust agrees to 0.1 %."""
    ring = ArchRing.from_span_rise(1.0, 0.25, 0.15, 2000.0, voussoirs=60)
    r, ro, n = ring.radius, ring.radius + ring.thickness, ring.voussoirs
    a0 = math.pi / 2 - ring.half_angle
    th = [a0 + 2 * ring.half_angle * k / n for k in range(n + 1)]
    zc = 0.0
    sec = ring_section([(r * math.cos(t), zc + r * math.sin(t)) for t in th],
                       [(ro * math.cos(t), zc + ro * math.sin(t)) for t in th], 2000.0)  # fmt: skip
    p = Problem(sec, (0.6,) * len(sec.joints))
    least = solve(p, force_on(assemble(p), sec, "support", 0, outward=True), 1).value / 2
    assert least == pytest.approx(thrust(ring, 0.6, 1).value, rel=1e-3)
    with pytest.raises(ValueError, match="matching"):
        ring_section([(0.0, 0.0), (1.0, 0.0)], [(0.0, 1.0), (1.0, 1.0)], 2000.0)


def test_a_catenary_carries_itself_along_its_centre() -> None:
    """A catenary's line of thrust under its own weight runs near its centre line, so even a
    thin ring stands, and a thicker one has room to spare."""
    for t in (0.05, 0.2):
        sec = catenary_ring(1.2, 1.8, t, 600.0, voussoirs=30)
        p = Problem(sec, (0.6,) * len(sec.joints))
        assert solve(p).status is Status.OPTIMAL
    assert len(sec.bodies) == 32


def test_the_dispatcher_on_its_edge_cases() -> None:
    """A kiln the cross-section refuses (a bonded ring of two materials) is reported not modelled
    with the section's reason; a ring too thin for its span falls, the model's verdict, never a
    flag (ADR 0017); every state is listed."""
    dense = olsen("olsen-crossdraft-36")
    mixed = dense.model_copy(
        update={"roof": dense.roof.model_copy(update={"ring": 2, "rings_bonded": True})}
    )
    r = statics(mixed)
    assert r.kind == "sprung arch"
    assert r.all_stand is None
    assert "different materials" in str(r.missing)
    assert KilnStatics("x", {"cold": True, "hot": False}).all_stand is False
    assert KilnStatics("x", {"cold": True, "hot": True}).all_stand is True


@pytest.mark.geometry
def test_n1_through_the_engines_own_solids() -> None:
    """N1: meaders-david's 60 in half-circle springing from the floor (p.115) with a 3 in ring,
    t/r 0.095 under the semicircle's 0.1075: cut from the engine's solids it can't stand, cold or
    hot; as built (9 in) it stands. (A ¼ in ring on the fast-fire's flat 27 in arch, by contrast,
    stands in its frame: a flat circle is within 0.07 in of its own funicular.)"""
    md = olsen("meaders-david")
    layer = md.lining.walls[0].model_copy(update={"thickness": Q_(3, "inch")})
    thin = md.model_copy(update={"lining": md.lining.model_copy(update={"roof": [layer]})})
    r = statics(thin)
    assert r.all_stand is False
    assert r.stands == {"cold": False, "hot": False}
    assert statics(md).all_stand is True
