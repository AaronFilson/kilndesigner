"""v2 statics: a kiln's cross-section cut from the engine's own solids (section.py), and the
parametric arch on walls (arch.on_walls) with negative cases N3 and N4
(engine-v2-negative-cases.md §6)."""

import math
from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.model import Kiln
from kilndesigner.units import Q_
from kilndesigner.v2.statics import sources
from kilndesigner.v2.statics.arch import ArchRing, on_walls
from kilndesigner.v2.statics.rigid import Problem, Section, Status, assemble, force_on, solve
from kilndesigner.v2.statics.section import (
    NotModelledError,
    analyse,
    cross_section,
    not_modelled,
    stations,
)

ROOT = Path(__file__).resolve().parents[3]
IN = 0.0254
LBFT = 4.4482216152605 / 0.3048  # N/m in a lbf/ft
PCF = 16.018463373960138


def olsen(name: str) -> Kiln:
    return load_design(ROOT / "examples" / "olsen" / f"{name}.yaml")


def least(held: str, sec: Section, mu: float = 0.6) -> tuple[Status, float]:
    """Whether the section stands with friction μ at the masonry's joints (none at the support's),
    and the least force a side on what holds it (N/m)."""
    tags = [(sec.bodies[j.a].tag, sec.bodies[j.b].tag) for j in sec.joints]
    p = Problem(sec, tuple(0.0 if held in t else mu for t in tags))
    if held == "none":
        return solve(p).status, 0.0
    sol = solve(p, force_on(assemble(p), sec, held, 0, outward=True), 1)
    return sol.status, sol.value / 2 / sec.depth


# ---------------------------------------------------------------- the parametric arch on walls


FAST_FIRE = ArchRing.from_span_rise(27 * IN, 3.375 * IN, 4.5 * IN, 513.0, 0.3048, voussoirs=13)


def test_n3_the_fast_fire_arch_on_free_walls_falls() -> None:
    """N3: the fast-fire arch (27 in, 1½ in/ft, 4½ in K-23; Olsen pp.139–140) on its 4½ in IFB
    walls, 36 in high, with no frame: no admissible state. With the frame Olsen bolts on, the
    least it must give is 7.08 lbf/ft a side, the walls leaning on their outer toes."""
    free = on_walls(FAST_FIRE, 4.5 * IN, 36 * IN, 513.0, 14, "none")
    assert least("none", free)[0] is Status.INFEASIBLE
    status, frame = least("frame", on_walls(FAST_FIRE, 4.5 * IN, 36 * IN, 513.0, 14, "frame"))
    assert status is Status.OPTIMAL
    assert frame / LBFT == pytest.approx(7.0785, abs=1e-3)
    backed = on_walls(FAST_FIRE, 4.5 * IN, 36 * IN, 513.0, 14, "buttress")
    status, buttress = least("buttress", backed)
    assert buttress == pytest.approx(frame, rel=1e-6)


def test_n4_the_reviews_end_wall_restated() -> None:
    """N4 (structure review #3): a 48 in arch at 1½ in/ft, 9 in ring at 140 lb/ft³ on a 13½ in
    end wall, μ 0.6. The review's μ needed of 1.96 at the springing took HarbisonWalker's
    mid-thickness thrust, 465 lbf/ft. v2 lets the arch settle to its least thrust, 168.8 lbf/ft:
    then the springing bed, with the skewback's own weight on it, needs μ 0.518. So it stands
    cold (0.60) and slides hot (0.50, Oliveira et al. 2021); a 60 in wall overturns either way."""
    ring = ArchRing.from_span_rise(48 * IN, 6 * IN, 9 * IN, 140 * PCF, 0.3048, voussoirs=40)
    from kilndesigner.v2.statics.arch import thrust

    assert thrust(ring, 0.6, 1).value / LBFT == pytest.approx(168.84, abs=0.01)
    wall = on_walls(ring, 13.5 * IN, 41 * IN, 140 * PCF, 16, "none")
    assert least("none", wall, 0.60)[0] is Status.OPTIMAL
    assert least("none", wall, 0.50)[0] is Status.INFEASIBLE
    assert least("none", wall, 0.519)[0] is Status.OPTIMAL
    assert least("none", wall, 0.517)[0] is Status.INFEASIBLE
    tall = on_walls(ring, 13.5 * IN, 60 * IN, 140 * PCF, 24, "none")
    assert least("none", tall, 0.60)[0] is Status.INFEASIBLE
    status, need = least("buttress", on_walls(ring, 13.5 * IN, 60 * IN, 140 * PCF, 24, "buttress"))
    assert status is Status.OPTIMAL
    assert need / LBFT == pytest.approx(16.15, abs=0.01)


def test_a_half_circle_springs_from_its_walls_tops() -> None:
    semi = ArchRing.semicircle(1.0, 0.2, 2000.0, voussoirs=20)
    assert least("none", on_walls(semi, 0.3, 0.5, 2000.0, 4, "none"))[0] is Status.OPTIMAL
    for held in ("frame", "buttress"):
        status, force = least(held, on_walls(semi, 0.3, 0.5, 2000.0, 4, held))
        assert status is Status.OPTIMAL
        assert force == pytest.approx(0.0, abs=1e-6)


def test_the_crushing_stand_ins_by_material() -> None:
    assert sources.crushing("ifb-k26") is sources.C16_IFB
    assert sources.crushing("firebrick-medium-duty-smithfield") is sources.C16_DENSE
    assert sources.crushing("kast-o-lite-26-li-plus") is None
    assert sources.C16_IFB.value == pytest.approx(68947.57, rel=1e-6)  # 10 psi
    assert sources.density("ifb-k23") == 513.0


# ---------------------------------------------------------- the engine's own solids (OCC)


@pytest.mark.geometry
def test_the_fast_fire_kiln_cut_from_the_engines_solids() -> None:
    """46 blocks: 14 courses a wall, two skewbacks, 13 voussoirs, the ground and the frame. The
    least frame force cold is the probe's 7.080 lbf/ft (section2d.py, method B); the walls hinge
    on their outer toes and the skewback beds need the most friction, T/N 0.249. Hot (μ 0.50,
    the C16 stand-in at 10 psi) the frame can be pushed with at most about 176 lbf/ft."""
    xs = cross_section(olsen("fast-fire"))
    assert (xs.courses, xs.voussoirs, len(xs.blocks), xs.support) == (14, 13, 46, "frame")
    assert xs.y_range == pytest.approx((-6 * IN, 6 * IN))
    cold = analyse(xs, "cold")
    assert cold.stands
    assert cold.least / LBFT == pytest.approx(7.080, abs=2e-3)
    assert math.isinf(cold.most)
    assert len(cold.beds) == 30
    base = [b for b in cold.beds if b.height == 0.0]
    assert [b.e for b in base] == pytest.approx([0.5, 0.5])
    assert max(b.t_over_n for b in cold.beds) == pytest.approx(0.249, abs=1e-3)
    gripped = analyse(xs, "cold", support_friction=True)
    assert gripped.least < cold.least
    hot = analyse(xs, "hot")
    assert hot.stands
    assert hot.most / LBFT == pytest.approx(176.0, abs=0.5)
    assert hot.least > cold.least
    names = [s.name for s in hot.steps]
    assert "Hot crushing stand-in, ifb-k23" in names
    stand_in = hot.steps[names.index("Hot crushing stand-in, ifb-k23")]
    assert stand_in.value == "10 psi"
    assert stand_in.note == sources.C16_IFB.note
    assert any(s.name.startswith("Most force on the frame") for s in hot.steps)


@pytest.mark.geometry
def test_without_its_frame_the_fast_fire_kiln_falls() -> None:
    xs = cross_section(olsen("fast-fire"), support="none")
    result = analyse(xs, "cold")
    assert not result.stands
    assert math.isnan(result.least)
    assert result.beds == ()
    assert "can't stand" in result.steps[-1].value


@pytest.mark.geometry
def test_the_slice_clears_the_openings() -> None:
    """Olsen's oil-drip kiln: the firebox enters the left wall at mid-depth, 9 in wide and 9 in
    high; the slice moves along the run until both walls run whole from the floor. Kato's coal
    kiln has an opening at the foot of its side walls at mid-depth, likewise."""
    xs = cross_section(olsen("olsen-oil-drip"))
    y0, y1 = xs.y_range
    assert y0 >= 4.5 * IN - 1e-9 or y1 <= -4.5 * IN + 1e-9
    assert analyse(xs, "cold").stands
    kato = cross_section(olsen("kato-coal"))
    assert kato.y_range != pytest.approx((-6 * IN, 6 * IN))
    assert analyse(kato, "cold").stands
    with pytest.raises(NotModelledError, match="no slice"):
        cross_section(olsen("fast-fire"), depth=1.0)


@pytest.mark.geometry
def test_layers_over_the_ring_are_its_load_and_a_bonded_ring_is_one() -> None:
    """Olsen's 36 ft³ cross-draft: 4½ in K-23 laid over a 4½ in dense ring, as load. The
    fast-fire roof doubled to two 4½ in K-23 layers bonded through acts as one 9 in ring; bonded
    layers of two materials are refused."""
    xd = cross_section(olsen("olsen-crossdraft-36"))
    loaded = [b for b in xd.section.bodies if b.tag == "voussoir"]
    assert all(len(b.loads) == 1 and b.loads[0][3] < 0 for b in loaded)
    assert analyse(xd, "cold").stands
    ff = olsen("fast-fire")
    layer = ff.lining.walls[0]
    two = ff.model_copy(update={
        "lining": ff.lining.model_copy(update={"roof": [layer, layer]}),
        "roof": ff.roof.model_copy(update={"ring": 2, "rings_bonded": True}),
    })  # fmt: skip
    xs = cross_section(two)
    assert all(b.loads == () for b in xs.section.bodies)
    assert analyse(xs, "cold").stands
    dense = olsen("olsen-crossdraft-36")
    mixed = dense.model_copy(
        update={"roof": dense.roof.model_copy(update={"ring": 2, "rings_bonded": True})}
    )
    assert "different materials" in str(not_modelled(mixed))


@pytest.mark.geometry
def test_arches_from_the_floor_and_level_springings() -> None:
    """meaders-david's half circle springs from the ground (nothing holds it but the ground);
    kitade-tojilo's half circle springs level from its walls' tops, so its frame bears on the
    top course; both stand alone, the frame giving nothing."""
    md = cross_section(olsen("meaders-david"))
    assert md.support == "none"
    assert md.courses == 0
    assert analyse(md, "cold").stands
    kt = cross_section(olsen("kitade-tojilo"))
    assert kt.support == "frame"
    r = analyse(kt, "cold")
    assert r.stands
    assert r.least == pytest.approx(0.0, abs=1e-6)


@pytest.mark.geometry
def test_a_kiln_on_a_slope_weighs_cos_slope_in_its_section() -> None:
    xs = cross_section(olsen("bae-gilgama"))
    c = math.cos(math.radians(11.3))
    assert xs.slope == pytest.approx(math.radians(11.3))
    total = sum(b.weight for b in xs.section.bodies)
    assert total == pytest.approx(c * sum(b.weight for b in xs.blocks), rel=1e-9)
    assert any(s.name == "Slope" for s in xs.steps)
    r = analyse(xs, "cold")
    assert r.stands
    assert xs.support == "buttress"
    assert r.least == pytest.approx(0.0, abs=1e-6)


def test_a_chamber_whose_width_changes_is_one_kiln_a_station() -> None:
    """Kannofen's four arch sections 1.5 m apart (Fig 6-37): each station a kiln of its own
    width, the arch's rise scaled with it (it keeps its shape); any other kiln is itself."""
    kf = olsen("kannofen")
    st = stations(kf)
    assert [round(at, 3) for at, _ in st] == [0.0, 1.5, 3.0, 4.5]
    base_w, base_rise = kf.chamber.width, kf.roof.rise  # type: ignore[union-attr]
    for _, k in st:
        assert k.chamber.widths is None
        ratio = (k.chamber.width / base_w).to("").magnitude
        assert (k.roof.rise / base_rise).to("").magnitude == pytest.approx(ratio)  # type: ignore[union-attr]
    ff = olsen("fast-fire")
    assert stations(ff) == [(0.0, ff)]


def test_what_isnt_cut_into_a_cross_section() -> None:
    reasons = {
        name: not_modelled(olsen(name))
        for name in ("singh-coal", "bidai", "church-skaelskor", "kannofen", "blakebrough-sturt")
    }
    assert "dome" in str(reasons["singh-coal"])
    assert "along the draft" in str(reasons["bidai"])
    assert "groin" in str(reasons["church-skaelskor"])
    assert "width changes" in str(reasons["kannofen"])
    assert "catenary_arch" in str(reasons["blakebrough-sturt"])
    ff = olsen("fast-fire")
    assert not_modelled(ff) is None
    with pytest.raises(NotModelledError, match="dome"):
        cross_section(olsen("singh-coal"))
    roof = ff.roof
    round_ = ff.model_copy(update={"chamber": ff.chamber.model_copy(update={"shape": "round"})})
    assert "round or curved" in str(not_modelled(round_))
    peaked = ff.model_copy(update={"roof": roof.model_copy(update={"peak_at": Q_(60, "percent")})})
    assert "offset-peak" in str(not_modelled(peaked))
