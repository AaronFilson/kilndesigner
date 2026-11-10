"""v2 statics: blocks and contacts from build123d solids (blocks.py), and a section made from
them (rigid.section_from_blocks). Test geometry: a 9 × 4½ × 2½ in brick (Olsen pp.19–20)."""

import math
from typing import Any

import build123d as bd
import numpy as np
import pytest

from kilndesigner.v2.statics.arch import ArchRing, thrust
from kilndesigner.v2.statics.blocks import Block, Load, contacts_fuse, contacts_pairwise
from kilndesigner.v2.statics.rigid import (
    Problem,
    assemble,
    force_on,
    section_from_blocks,
    solve,
)

pytestmark = pytest.mark.geometry

IN = 0.0254
SQIN = IN**2


def box(lo: tuple[float, float, float], hi: tuple[float, float, float]) -> Any:
    sx, sy, sz = (b - a for a, b in zip(lo, hi, strict=True))
    cx, cy, cz = ((a + b) / 2 for a, b in zip(lo, hi, strict=True))
    return (bd.Pos(cx, cy, cz) * bd.Box(sx, sy, sz)).solid()


def half_lap(gap: float = 0.0, turn: float = 0.0) -> list[Block]:
    a = box((0, 0, 0), (9, 4.5, 2.5))
    b = box((4.5, 0, 2.5 + gap), (13.5, 4.5, 5 + gap))  # 4½ × 4½ in in contact
    if turn:
        axis = bd.Axis((1, 2, 3), (1, 2, 3))
        a, b = a.rotate(axis, turn), b.rotate(axis, turn)
    return [Block("a", a, 1.0, unit=IN), Block("b", b, 1.0, unit=IN)]


def areas(blocks: list[Block]) -> list[float]:
    return [round(c.area / SQIN, 6) for c in contacts_pairwise(blocks)]


def test_a_block_reports_si() -> None:
    b = Block("brick", box((0, 0, 0), (9, 4.5, 2.5)), 513.0, unit=IN)
    assert b.volume == pytest.approx(9 * 4.5 * 2.5 * IN**3)
    assert b.centroid == pytest.approx(np.array([4.5, 2.25, 1.25]) * IN)
    assert b.weight == pytest.approx(513.0 * 9.80665 * b.volume)
    assert len(b.planes) == 6
    assert b.curved == 0


def test_pairwise_contacts_forgive_a_small_gap_or_overlap() -> None:
    assert areas(half_lap()) == [20.25]
    assert areas(half_lap(1e-4)) == [20.25]  # 0.0025 mm gap, within 0.025 mm
    assert areas(half_lap(-1e-4)) == [20.25]
    assert areas(half_lap(0.01)) == []  # a 0.25 mm gap is a gap
    assert areas(half_lap(turn=17.0)) == [20.25]
    (c,) = contacts_pairwise(half_lap())
    assert c.planar
    assert c.normals[0] == pytest.approx([0.0, 0.0, 1.0])  # from a (below) into b


def test_a_brick_bridging_a_head_joint_has_three_contacts() -> None:
    bricks = [
        Block("l", box((0, 0, 0), (9, 4.5, 2.5)), 1.0, unit=IN),
        Block("r", box((9, 0, 0), (18, 4.5, 2.5)), 1.0, unit=IN),
        Block("top", box((4.5, 0, 2.5), (13.5, 4.5, 5)), 1.0, unit=IN),
    ]
    assert sorted(areas(bricks)) == [11.25, 20.25, 20.25]
    fixed = [Block(b.name, b.solid, 1.0, unit=IN, fixed=True) for b in bricks[:2]]
    assert sorted(areas([*fixed, bricks[2]])) == [20.25, 20.25]  # two fixed blocks aren't paired


def test_curved_contacts_come_from_the_general_fuse() -> None:
    def shell(r_out: float, r_in: float) -> Any:
        ring = bd.Cylinder(r_out, 9, rotation=(90, 0, 0)) - bd.Cylinder(
            r_in, 9, rotation=(90, 0, 0)
        )
        return (ring - bd.Pos(0, 0, -50) * bd.Box(100, 100, 100)).solid()

    blocks = [
        Block("outer", shell(20, 15), 1.0, unit=IN),
        Block("inner", shell(15, 10), 1.0, unit=IN),
    ]
    assert blocks[0].curved == 2
    assert contacts_pairwise(blocks) == []
    (c,) = contacts_fuse(blocks, samples=5)
    assert not c.planar
    assert c.area / SQIN == pytest.approx(math.pi * 15 * 9)
    radial = c.points[:, [0, 2]] / np.linalg.norm(c.points[:, [0, 2]], axis=1)[:, None]
    assert np.einsum("ij,ij->i", c.normals[:, [0, 2]], radial) == pytest.approx(-1.0)
    planar = contacts_fuse(half_lap())
    assert [round(x.area / SQIN, 6) for x in planar] == [20.25]
    assert planar[0].normals[0] == pytest.approx([0.0, 0.0, 1.0])
    assert contacts_fuse([]) == []
    assert contacts_pairwise([]) == []


def test_the_filters_between_blocks_and_faces() -> None:
    """Coplanar faces apart, faces meeting at an edge, a contact under the least area, a fuzzy
    fuse, a block the fuse leaves alone and two fixed blocks: none is a contact."""
    a = Block("a", box((0, 0, 0), (9, 4.5, 2.5)), 1.0, unit=IN)
    # an L: its face on x = 9 starts 0.5 in above a's top, its foot reaches past a
    ell = (box((9, 0, 3), (18, 4.5, 5)) + box((14, 0, 0), (18, 4.5, 3))).solid()
    assert contacts_pairwise([a, Block("L", ell, 1.0, unit=IN)]) == []
    corner = Block("corner", box((9, 0, 2.5), (18, 4.5, 5)), 1.0, unit=IN)
    assert contacts_pairwise([a, corner]) == []  # an edge is no area
    notched = (box((0, 0, 0), (9, 9, 2.5)) - box((4.5, 4.5, 0), (9, 9, 2.5))).solid()
    over = Block("over the notch", box((5, 5, 2.5), (9, 9, 5)), 1.0, unit=IN)
    assert contacts_pairwise([Block("notched", notched, 1.0, unit=IN), over]) == []
    assert contacts_pairwise(half_lap(), min_area=0.1) == []
    gap = half_lap(1e-4)
    assert [round(c.area / SQIN, 6) for c in contacts_fuse(gap, fuzzy=1e-5)] == [20.25]
    far = Block("far", box((100, 0, 0), (109, 4.5, 2.5)), 1.0, unit=IN)
    assert len(contacts_fuse([*half_lap(), far])) == 1
    assert contacts_fuse(half_lap(), min_area=0.1) == []
    held = [Block(b.name, b.solid, 1.0, unit=IN, fixed=True) for b in half_lap()]
    assert contacts_fuse(held) == []


def test_a_face_across_the_slice_is_no_joint_and_the_depth_can_be_given() -> None:
    a = Block("a", box((0, 0, 0), (9, 4.5, 2.5)), 1.0, unit=IN, fixed=True)
    b = Block("b", box((0, 4.5, 0), (9, 9, 2.5)), 1.0, unit=IN)
    sec = section_from_blocks([a, b], contacts_pairwise([a, b]), depth=0.5)
    assert sec.joints == ()
    assert sec.depth == 0.5


def test_blocks_of_one_model_share_a_unit() -> None:
    a, b = half_lap()
    with pytest.raises(ValueError, match="model unit"):
        contacts_pairwise([a, Block("mm", b.solid, 1.0, unit=1e-3)])


def sector(r0: float, r1: float, a0: float, a1: float, depth: float) -> Any:
    """An annular sector in the x–z plane between angles a0 < a1, run along y."""

    def p(r: float, t: float) -> bd.Vector:
        return bd.Vector(r * math.cos(t), 0, r * math.sin(t))

    mid = (a0 + a1) / 2
    wire = bd.Wire(
        [
            bd.Edge.make_line(p(r0, a0), p(r1, a0)),
            bd.Edge.make_three_point_arc(p(r1, a0), p(r1, mid), p(r1, a1)),
            bd.Edge.make_line(p(r1, a1), p(r0, a1)),
            bd.Edge.make_three_point_arc(p(r0, a1), p(r0, mid), p(r0, a0)),
        ]
    )
    solid = bd.Solid.extrude(bd.Face(wire), (0, depth, 0))
    return solid if solid.volume > 0 else bd.Solid.extrude(bd.Face(wire), (0, -depth, 0))


def test_an_arch_of_build123d_voussoirs_matches_the_analytic_ring() -> None:
    """The fast-fire arch (27 in span, 3⅜ in rise, 4½ in K-23 at 32.0 pcf) as 13 voussoirs cut
    as true annular sectors: the least thrust through the contacts and the section equals the
    analytic ring's."""
    ring = ArchRing.from_span_rise(27 * IN, 3.375 * IN, 4.5 * IN, 512.59, 0.3048, voussoirs=13)
    r, ro, d = ring.radius, ring.radius + ring.thickness, ring.depth
    a0 = math.pi / 2 - ring.half_angle
    th = [a0 + 2 * ring.half_angle * i / 13 for i in range(14)]
    blocks = [Block(f"v{i}", sector(r, ro, th[i], th[i + 1], d), ring.density) for i in range(13)]
    blocks.append(Block("R", sector(r, ro, th[0] - 0.2, th[0], d), fixed=True, tag="support"))
    blocks.append(Block("L", sector(r, ro, th[-1], th[-1] + 0.2, d), fixed=True, tag="support"))
    sec = section_from_blocks(blocks, contacts_pairwise(blocks))
    assert len(sec.joints) == 14
    assert sec.depth == pytest.approx(d)
    p = Problem(sec, (0.6,) * 14)
    least = solve(p, force_on(assemble(p), sec, "support", 0, outward=True), 1)
    assert least.value / 2 / d == pytest.approx(thrust(ring, 0.6, 1).value, rel=1e-9)


def test_a_curved_contact_in_a_section_and_loads_on_blocks() -> None:
    """A half shell resting in a fixed one: the curved contact becomes a joint of points in
    order; a load on the shell is carried to the bed."""

    def shell(r_out: float, r_in: float) -> Any:
        ring = bd.Cylinder(r_out, 9, rotation=(90, 0, 0)) - bd.Cylinder(
            r_in, 9, rotation=(90, 0, 0)
        )
        return (ring - bd.Pos(0, 0, 50) * bd.Box(100, 100, 100)).solid()  # the lower half

    load = Load((0.0, 0.0, -12.5 * IN), (0.0, 0.0, -10.0))
    blocks = [
        Block("bed", shell(20, 15), 1.0, unit=IN, fixed=True, tag="bed"),
        Block("shell", shell(15, 10), 2000.0, unit=IN, loads=(load,)),
    ]
    sec = section_from_blocks(blocks, contacts_fuse(blocks, samples=7))
    (joint,) = sec.joints
    assert not joint.planar
    assert joint.length == pytest.approx(math.pi * 15 * IN, rel=0.02)  # the chords of 7 points
    assert sec.bodies[1].loads == ((0.0, -12.5 * IN, 0.0, -10.0),)
    p = Problem(sec, (0.6,))
    up = solve(p, force_on(assemble(p), sec, "bed", 1), -1)
    assert -up.value == pytest.approx(blocks[1].weight + 10.0)  # the bed carries it all
    assert sec.without({"bed"}).joints == ()
