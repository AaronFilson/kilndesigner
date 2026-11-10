"""v2 statics: the section along a row of chambers (row.py), cut from the engine's own solids.

The reference kilns stood for their builders (the user, 2026-11-10): each piece that let them
stand here is sourced construction the engine's layout lacked, not a parameter fitted to a kiln:
the first chamber's front wall over the firebox (Bidai p.94–95, Kawaii p.97, Fujiwara p.100–101),
the ring's foot coursed into the taller wall behind it (a tas-de-charge), the common wall 4½ in
thicker than the others (Olsen p.46), and a 9 in wall's layers tied by header courses (p.41–42,
p.295)."""

from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.geometry import Part
from kilndesigner.model import Kiln, SprungArch
from kilndesigner.units import Q_
from kilndesigner.v2.statics.kiln import statics
from kilndesigner.v2.statics.rigid import Status, solve
from kilndesigner.v2.statics.row import (
    analyse,
    carved_from,
    clear_slice,
    conditions,
    not_modelled,
    row_section,
)
from kilndesigner.v2.statics.section import NotModelledError

ROOT = Path(__file__).resolve().parents[3]
LBFT = 4.4482216152605 / 0.3048  # N/m in a lbf/ft


def olsen(name: str) -> Kiln:
    return load_design(ROOT / "examples" / "olsen" / f"{name}.yaml")


def cut_to(kiln: Kiln, n: int) -> Kiln:
    """The first n chambers of a row."""
    c = kiln.chamber
    sizes = c.sizes[:n] if c.sizes is not None else None
    return kiln.model_copy(update={"chamber": c.model_copy(update={"chambers": n, "sizes": sizes})})


def with_roof(kiln: Kiln, **changes: object) -> Kiln:
    roof = kiln.roof
    assert isinstance(roof, SprungArch)
    return kiln.model_copy(update={"roof": roof.model_copy(update=changes)})


def test_the_parts_a_carved_wall_was_cut_from() -> None:
    """Carved pieces are named after their box with one more character, on past 'z' (Tobe's
    25 ft walls between chambers carry more flues than letters)."""
    assert carved_from("division/1-ifb-k26-chamber-1-d") == "division/1-ifb-k26-chamber-1"
    assert carved_from("division/1-ifb-k26-chamber-1-{") == "division/1-ifb-k26-chamber-1"
    assert carved_from("division/1-ifb-k26-chamber-1") == "division/1-ifb-k26-chamber-1"
    assert carved_from("front/1-ifb-k26") == "front/1-ifb-k26"


def test_a_slice_must_pass_between_the_openings() -> None:
    """A wall cut by a hole is whole in a slice only where the slice misses the hole; a piece
    over a hole or under a notch at the top won't do."""

    def box(name: str, lo: tuple[float, float, float], hi: tuple[float, float, float]) -> Part:
        return Part(name, "ifb-k26", "insulating_firebrick", lo, hi, face="front")

    pier = [box("front/1-ifb-k26-a", (-500, 0, 0), (-100, 100, 1000)),
            box("front/1-ifb-k26-b", (-100, 0, 300), (500, 100, 1000)),
            box("front/1-ifb-k26-c", (100, 0, 0), (500, 100, 300))]  # fmt: skip
    _, x1 = clear_slice(pier, 100.0, 1000.0)
    assert x1 <= -100.0 + 1e-6
    notched = [box("back/1-ifb-k26-a", (-500, 0, 0), (500, 100, 900)),
               box("back/1-ifb-k26-b", (-500, 0, 950), (500, 100, 1000))]  # fmt: skip
    sliver = box("back/1-ifb-k26-c", (-500, 0, 0), (-499, 100, 1000))
    with pytest.raises(NotModelledError, match="no slice"):
        clear_slice([notched[0], sliver], 100.0, 1000.0)
    with pytest.raises(NotModelledError, match="no slice"):
        clear_slice(notched, 100.0, 1000.0)


def test_what_the_row_section_refuses() -> None:
    """Each refusal says what isn't cut yet (ADR 0009); none is a verdict on the kiln."""
    kawaii = olsen("kawaii")
    assert not_modelled(kawaii) is None
    assert "sprung arches" in str(not_modelled(olsen("hollyweird")))
    assert "not a row" in str(not_modelled(olsen("fast-fire")))
    assert "not a row" in str(not_modelled(with_roof(kawaii, tube=True)))
    crossing = olsen("church-skaelskor").roof
    assert isinstance(crossing, SprungArch)
    assert "groin" in str(not_modelled(with_roof(kawaii, crossing=crossing.crossing)))
    turned = kawaii.chamber.model_copy(update={"shape": "round"})
    assert "straight box plan" in str(not_modelled(kawaii.model_copy(update={"chamber": turned})))
    assert "offset-peak" in str(not_modelled(with_roof(kawaii, peak_at=Q_(60, "percent"))))
    roof = kawaii.lining.for_face("roof")
    mixed = kawaii.model_copy(update={"lining": kawaii.lining.model_copy(update={"roof": [
        roof[0], roof[0].model_copy(update={"material": "ifb-k26"})]})})  # fmt: skip
    assert "different materials" in str(not_modelled(with_roof(mixed, ring=2, rings_bonded=True)))
    fuji = olsen("fujiwara-bizen")
    sizes = fuji.chamber.sizes
    assert sizes is not None
    lower = [sizes[0], sizes[1].model_copy(update={"height": Q_(20, "inch")})]
    level = fuji.model_copy(update={"chamber": fuji.chamber.model_copy(
        update={"slope": None, "sizes": lower})})  # fmt: skip
    assert "springing lower" in str(not_modelled(level))
    with pytest.raises(NotModelledError, match="not a row"):
        row_section(olsen("fast-fire"))
    refused = statics(with_roof(kawaii, peak_at=Q_(60, "percent")))
    assert refused.all_stand is None
    assert refused.steps[0].name == "Not modelled"
    assert "offset-peak" in str(refused.missing)


def test_a_plane_that_misses_the_ring_makes_no_voussoir() -> None:
    """Cutting by planes through an axis: a plane before the ring leaves nothing on its near side,
    one past it nothing beyond, and neither makes an empty voussoir."""
    from kilndesigner.v2.statics.solids import box as cube
    from kilndesigner.v2.statics.solids import voussoirs

    # a block standing between 0.25 and 0.79 rad about the x axis through the origin (y–z plane)
    block = cube((0.0, 300.0, 100.0), (50.0, 400.0, 300.0))
    pieces = voussoirs(block, 1, (0.0, 0.0), [0.0, 0.1, 0.5, 1.0, 1.2])
    assert len(pieces) == 2
    assert sum(float(p.volume) for p in pieces) == pytest.approx(float(block.volume), rel=1e-9)


@pytest.mark.geometry
def test_a_slice_wider_than_the_piers_finds_none() -> None:
    """Kawaii's walls between chambers carry five 7 in flues across 84 in (8 in piers): a 12 in
    slice can't pass between them."""
    with pytest.raises(NotModelledError, match="no slice along the run"):
        row_section(olsen("kawaii"), depth=0.3048)


@pytest.mark.geometry
def test_a_level_row_on_its_frame() -> None:
    """Olsen's two-chamber kiln, level, its printed 9 in wall between the chambers (Fig 8-17):
    each arch along the draft springs from the end wall and the common wall, held by the frame at
    the ends; symmetric, the two ends take the same."""
    rs = row_section(olsen("olsen-two-chamber"))
    assert rs.support == "frame"
    assert rs.seated == ()
    assert rs.voussoirs == (50, 50)
    cold = analyse(rs, "cold")
    assert cold.stands
    assert cold.least["front"] / LBFT == pytest.approx(27.7, abs=0.5)
    assert cold.least["back"] == pytest.approx(cold.least["front"], rel=1e-3)
    hot = analyse(rs, "hot")
    assert hot.stands
    assert not hot.analogy
    assert hot.most["front"] > hot.least["front"] > cold.least["front"]
    gripped = analyse(rs, "cold", support_friction=True)
    assert gripped.least["front"] <= cold.least["front"] + 1e-6
    assert any(s.name.startswith("Most force") for s in hot.steps)


@pytest.mark.geometry
def test_a_ring_against_a_taller_wall_sits_on_a_springer() -> None:
    """Fujiwara's first chamber's ring ends against the taller wall behind it. The engine's
    layout trims it at the wall's face, where friction alone can't carry its foot; as built it
    sits on the wall: its foot, below the joint that meets the wall's face, laid in the wall's
    level courses and bonded to them. Its dogi meets chamber 1 through the himitsu's wall and its
    6 × 9 in flues (p.100–101), which carries the first arch's front."""
    kiln = olsen("fujiwara-bizen")
    rs = row_section(kiln)
    assert rs.seated == (1,)
    from kilndesigner.run_parts import run_layout

    face = run_layout(kiln).back(0)
    bonded = [b for b in rs.blocks if b.tag == "wall" and b.lo[1] < face - 1 < face + 1 < b.hi[1]]
    assert bonded, "the springer's courses are bonded into the wall's"
    for state in ("cold", "hot"):
        assert analyse(rs, state).stands


@pytest.mark.geometry
def test_a_springer_of_another_material_is_weighed_as_its_own() -> None:
    """An IFB ring's springer bonded into a dense wall's course: the block's weight is the sum of
    the two materials', at their centroid."""
    kiln = olsen("fujiwara-bizen")
    ifb = [x.model_copy(update={"material": "ifb-k26"}) for x in kiln.lining.for_face("roof")]
    light = kiln.model_copy(update={"lining": kiln.lining.model_copy(update={"roof": ifb})})
    rs = row_section(light)
    assert rs.ring_material == "ifb-k26"
    from kilndesigner.run_parts import run_layout

    face = run_layout(light).back(0)
    bonded = [b for b in rs.blocks if b.tag == "wall" and b.lo[1] < face - 1 < face + 1 < b.hi[1]]
    assert bonded
    assert all(b.material == "ifb-k26" for b in bonded)  # the weaker stand-in, IFB's 10 psi


@pytest.mark.geometry
@pytest.mark.slow
def test_a_walls_layers_are_tied_by_header_courses() -> None:
    """Olsen's three-chamber kiln, its 9 in walls of 4½ in K-26 and 4½ in K-23: a header course
    every fifth course ties the layers (Fig 2-4, p.295). With the common wall 4½ in thicker
    (p.46) it stands cold and hot in its frame."""
    rs = row_section(cut_to(olsen("olsen-three-chamber"), 2))
    headers = [b.name for b in rs.blocks if b.name.endswith("headers")]
    assert headers
    assert all(int(h.split(", course ")[1].split(",")[0]) % 5 == 0 for h in headers)
    assert analyse(rs, "cold").stands


@pytest.mark.geometry
def test_an_arch_a_hair_past_a_semicircle_lies_level_on_its_walls() -> None:
    """Kyoto's 20.7 in rise on a 41⅓ in span turns 0.1° past a semicircle, so its radial feet dip
    0.4 mm into the walls' tops; laid level on them, the feet bear and the row stands."""
    rs = row_section(cut_to(olsen("kyoto-climbing"), 2))
    sec = rs.section
    first = next(i for i, b in enumerate(sec.bodies) if b.name == "chamber 1 voussoir 1")
    joints = [j for j in sec.joints if first in (j.a, j.b)]
    assert "wall" in [sec.bodies[j.a if j.b == first else j.b].tag for j in joints]
    assert analyse(rs, "cold").stands


@pytest.mark.geometry
def test_a_semicircular_row_in_a_frame_bears_on_the_walls_top_course() -> None:
    """Without a skewback the frame bears on the end walls' top courses. A cast ring has no
    crushing stand-in (only IFB and dense brick do): hot, it is unlimited in compression
    (Heyman), and the working names only the walls' stand-in."""
    kiln = with_roof(cut_to(olsen("kawaii"), 2), buttressed=False)
    cast = [x.model_copy(update={"material": "kast-o-lite-26-li-plus"})
            for x in kiln.lining.for_face("roof")]  # fmt: skip
    kiln = kiln.model_copy(update={"lining": kiln.lining.model_copy(update={"roof": cast})})
    rs = row_section(kiln)
    assert rs.support == "frame"
    front = next(b for b in rs.blocks if b.name == "frame front")
    assert front.hi[2] - front.lo[2] < 100.0  # a course or so
    assert analyse(rs, "cold").stands
    hot = analyse(rs, "hot")
    named = [s.name for s in hot.steps if s.name.startswith("Hot crushing")]
    assert named == ["Hot crushing stand-in, firebrick-medium-duty-smithfield"]


@pytest.mark.geometry
def test_one_chamber_under_an_uneven_arch_along_its_depth() -> None:
    """Bowen Mountain: one chamber, its arch along the draft springing 16 in at the front and
    18 in at the back (Fig 4-153), held by masonry and its concrete platform."""
    k = olsen("bowen-mountain")
    rs = row_section(k)
    assert rs.chambers == 1
    assert rs.support == "buttress"
    r = statics(k)
    assert r.kind == "arches along the draft"
    assert r.stands == {"cold": True, "hot": True}


@pytest.mark.geometry
@pytest.mark.slow
def test_a_hot_verdict_resting_on_dense_bricks_stand_in_alone_isnt_given() -> None:
    """Tobe's 10 ft arches, 9 in rings of dense firebrick: hot, with the 25 psi crushing stand-in
    carried over from IFB by analogy, no admissible state, without it one. That verdict rests on
    an unsourced value, so it isn't given (ADR 0009): the missing data is said instead."""
    kiln = cut_to(olsen("tobe"), 2)
    rs = row_section(kiln)
    hot = analyse(rs, "hot")
    assert not hot.stands
    assert hot.analogy
    assert solve(conditions(rs, "hot", analogy=False)).status is Status.OPTIMAL
    assert any("analogy" in s.name for s in hot.steps)
    r = statics(kiln)
    assert r.stands == {"cold": True, "hot": None}
    assert r.all_stand is None
    assert "dense brick's hot crushing" in str(r.missing)
