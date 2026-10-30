"""The frame: arch thrust checked against HarbisonWalker's tables, and the steel it picks."""

from __future__ import annotations

import math
from pathlib import Path

import pytest
from pydantic import ValidationError

from kilndesigner import load_design, parse_design
from kilndesigner.frame import (
    MAX_PRINTED_HEATED,
    NO_FRAME,
    cold_thrust_factor,
    design_frame,
    heated_thrust_factor,
    steel_data,
)
from kilndesigner.model import Kiln
from kilndesigner.sheet import Check

EXAMPLES = Path(__file__).parents[2] / "examples"


def _dense_arch() -> Kiln:
    """kiln-hardware.md §4.5 case C: a 4½ in dense arch (142 lb/ft³) over 54 in at 2.302 in/ft,
    54 in long outside."""
    hard = [{"material": "hard-firebrick-kx99", "thickness": "4.5 in"}]
    return Kiln.model_validate(
        {
            "name": "case C",
            "firing": {"cone": "10"},
            "chamber": {"width": "54 in", "depth": "45 in", "height": "40 in"},
            "roof": {"type": "sprung_arch", "rise": f"{2.302 * 54 / 12} in"},
            "lining": {"walls": hard, "floor": hard, "roof": hard},
            "heat": {"gas": {"supply": {"type": "cylinders", "count": 4}}},
        }
    )


def _value(design: object, name: str) -> str:
    return next(s.value for s in design.working if s.name == name)  # type: ignore[attr-defined]


def test_arch_weight_and_thrust_agree_with_harbisonwalker() -> None:
    frame = design_frame(_dense_arch())
    # HarbisonWalker's constant W = 1.17 DST gives 280.4 lb/ft and H = 0.62 W = 173.8 lb/ft; the
    # engine weighs the arch exactly (density × thickness × mean arc), so it differs slightly.
    weight = float(_value(frame, "Arch weight per foot of length").split()[0])
    cold = float(_value(frame, "Cold horizontal thrust").split()[0])
    assert weight == pytest.approx(280.4, rel=0.02)
    assert cold == pytest.approx(173.8, rel=0.02)
    # T/S = 4.5 / 54 = 8.3 %: the heated factor interpolates to about 1.73, Hmax about 300.6
    hot = float(_value(frame, "Thrust of the heated arch, free to rise").split()[0])
    assert hot == pytest.approx(300.6, rel=0.03)


def test_the_buttress_is_sized_by_the_thrust() -> None:
    # §4.5: case C over 54 in needs Sx ≥ 0.761 in³; L3×3×⅜ and L4×4×¼ pass, L3×3×¼ doesn't.
    frame = design_frame(_dense_arch())
    assert "0.7" in _value(frame, "Buttress angle, bending")
    assert frame.angle == "L4×4×1/4"  # the lighter of the two that pass
    assert frame.rod == "1/2-13"


def test_a_flat_thick_arch_takes_the_most_harbisonwalker_tabulates() -> None:
    """2 in of rise under a 4½ in dense arch over 54 in: HarbisonWalker's heated-arch method has
    no finite hot thrust (its thrust line can't hinge in the ring). Olsen builds such arches in
    light frames that give, so the steel takes 5.34 × the cold thrust, with a note, not an error
    (the user's rule: the book's kilns are built and fired)."""
    document = _dense_arch().model_dump(mode="json", by_alias=True)
    kiln = Kiln.model_validate({**document, "roof": {"type": "sprung_arch", "rise": "2 in"}})
    frame = design_frame(kiln)
    assert not [f for f in frame.findings if f.level == "error" and "thrust line" in f.message]
    [note] = [f for f in frame.findings if "stress excessive" in f.message]
    assert note.level == "info"
    cold = float(_value(frame, "Cold horizontal thrust").split()[0])
    hot = float(_value(frame, "Thrust of the heated arch").split()[0])
    assert hot == pytest.approx(MAX_PRINTED_HEATED * cold, rel=1e-3)
    # Under Olsen's 1½ in/ft: a warning
    [low] = [f for f in frame.findings if f.check and f.check.id == "frame.rise"]
    assert low.level == "warning"


def test_an_electric_kiln_has_a_case_and_the_hybrid_an_arch_frame() -> None:
    electric = design_frame(load_design(EXAMPLES / "electric-front-loader.yaml"))
    assert electric.kind == "welded case"
    # Its flat roof: Olsen's angle frame and a tie bolt through each row of brick (p.248–249)
    assert {m.part for m in electric.members} >= {"rods across the roof, one every 4½ in"}
    hybrid = design_frame(load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml"))
    assert hybrid.kind == "arch frame"
    # Its 3 in castable arch is 10.7 % of the 28 in span: past the table, worked out by the same
    # statics, a note
    [past] = [f for f in hybrid.findings if "is past it" in f.message]
    assert past.level == "info"
    assert {m.part for m in hybrid.members} >= {"corner posts", "tie rods"}


def test_the_heated_thrust_formula_reproduces_harbisonwalkers_table() -> None:
    """Hinges at the faces: every printed cell to 4 %; every "excessive" cell past the largest
    printed factor or with no lever at all (arch-thrust-theory.md)."""
    table = steel_data()["heated_factor"]
    for pct, row in zip(table["t_over_s"], table["rows"], strict=True):
        for d, printed in zip(steel_data()["arch_constants"]["d"], row, strict=True):
            factor = heated_thrust_factor(12.0, d, pct / 100 * 12.0)
            if printed is None:
                assert factor is None or factor > MAX_PRINTED_HEATED
            else:
                assert factor == pytest.approx(printed, rel=0.045)


def test_a_thick_arch_past_the_table_is_worked_out_not_refused() -> None:
    """The hybrid's 3 in arch over 28 in (T/S 10.7 %) gets a hot thrust, with a note."""
    design = design_frame(load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml"))
    assert not [f for f in design.findings if f.level in ("error", "warning")]
    assert any("is past it" in f.message for f in design.findings)
    assert any(s.name.startswith("Thrust of the heated arch") for s in design.working)


def test_olsens_fast_fire_arch_gets_olsens_angle() -> None:
    """The fast-fire kiln's No. 1 arch, 4½ in of IFB over 27 in at 1½ in/ft: past
    HarbisonWalker's method, so 5.34 × the cold thrust, and the frame comes out as the
    2 × 2 × 3/16 in angle Olsen bolted on it (p.139)."""
    frame = design_frame(load_design(EXAMPLES / "olsen" / "fast-fire.yaml"))
    assert frame.kind == "arch frame"
    assert frame.angle == "L2×2×3/16"
    assert not [f for f in frame.findings if f.level in ("error", "warning")]


def test_the_cold_thrust_formula_reproduces_harbisonwalkers_table() -> None:
    """Statics of a circular arch against every column of HW's H/W table (±0.6 %, its rounding)."""
    consts = steel_data()["arch_constants"]
    for d, factor in zip(consts["d"], consts["h_factor"], strict=True):
        assert cold_thrust_factor(12.0, d) == pytest.approx(factor, rel=0.007)


def _gas_crossdraft(roof: dict[str, str]) -> Kiln:
    """The gas cross-draft (28 × 48 × 40 in inside; 8 in walls, a 7 in floor, a 5 in roof) with
    another roof."""
    document = load_design(EXAMPLES / "gas-crossdraft.yaml").model_dump(mode="json", by_alias=True)
    return Kiln.model_validate({**document, "roof": roof})


def test_a_flat_roofed_gas_kiln_gets_merrills_angle_frame() -> None:
    """Merrill's flat-top: 2 × 2 × 3/16 roof angle and ⅜ in rods "4 inches longer than the width
    of the kiln", one through each 4½ in row of the roof (kiln-hardware.md §4.2 [S16];
    flat-roofs.md §4.3 [F9]). Outside, the kiln is 28 + 2 × 8 = 44 in wide, 48 + 2 × 8 = 64 in
    deep and 7 + 40 + 5 = 52 in tall; the rods cross the 44 in and both 2 in angle legs, plus 4
    in. The roof spans the 28 in between the side walls, the door being the front."""
    frame = design_frame(_gas_crossdraft({"type": "flat"}))
    assert (frame.kind, frame.angle, frame.rod) == ("angle frame", "L2×2×3/16", "3/8-16")
    assert (frame.angle_leg_in, frame.angle_t_in, frame.rod_d_in) == (2, 0.1875, 0.375)
    members = {m.part: m for m in frame.members}
    assert set(members) == {
        "corner posts", "roof angle, front and back", "roof angle, sides",
        "rods across the roof, one every 4½ in",
    }  # fmt: skip
    assert (members["corner posts"].count, members["corner posts"].length_in) == (4, 52)
    # Once round the 44 × 64 in outside, lapping each corner by a leg (the review's structure 8)
    front, sides = members["roof angle, front and back"], members["roof angle, sides"]
    assert (front.count, front.length_in, sides.count, sides.length_in) == (2, 48, 2, 68)
    rods = members["rods across the roof, one every 4½ in"]
    assert (rods.count, rods.length_in) == (math.ceil(64 / 4.5), 44 + 2 * 2 + 4)
    merrill = "Merrill flat-top kiln; kiln-hardware.md §4.2 [S16]"
    assert {m.source for m in frame.members} == {merrill}


def test_a_flat_roof_is_a_jack_arch_squeezed_by_its_frame() -> None:
    """BIA TN 31A: H = 3WS/8d for a uniform load, the thrust line in the middle third
    (flat-roofs.md §2.2 [F2]). The gas example's 3 in of Kast-O-Lite 30 under 2 in of blanket
    over 28 in: W = (98 × 3 + 8 × 2)/1728 lb/in² × 28 in."""
    frame = design_frame(_gas_crossdraft({"type": "flat"}))
    load = (98 * 3 + 8 * 2) / 1728
    thrust = 3 * load * 28**2 / (8 * 3)  # lb per inch of roof
    assert frame.thrust == f"{thrust * 12:.0f} lb per foot of roof, cold"
    step = next(s for s in frame.working if s.name == "Flat roof, as a jack arch")
    assert step.value.startswith("spans 28 in between the left and right walls")
    assert step.inputs["fm"] == f"{2 * thrust / 3:.1f} psi"
    assert not [f for f in frame.findings if f.level == "error"]
    assert any("tighten its band or rods" in f.message for f in frame.findings)


@pytest.mark.parametrize(
    ("width", "roof", "level", "says"),
    [
        ("40 in", "3 in", "warning", "past the longest one-way flat roof in the sources"),
        ("48 in", "3 in", "error", "longer than any flat brick roof in the sources"),
        ("18 in", "9 in", "error", "too deep for its span to hold at its ends by friction"),
    ],
)
def test_a_flat_roof_outside_what_the_sources_cover(
    width: str, roof: str, level: str, says: str
) -> None:
    """Merrill's 36 in is the longest one-way flat roof sourced; about 45 in on four walls
    (§4.1, §4.3). With vertical ends, BIA's friction of 0.60 needs S/d over about 2.2 (§2.4)."""
    document = load_design(EXAMPLES / "gas-crossdraft.yaml").model_dump(mode="json", by_alias=True)
    document["chamber"]["width"] = width
    document["lining"]["roof"][0]["thickness"] = roof
    kiln = Kiln.model_validate({**document, "roof": {"type": "flat"}})
    assert [f.level for f in design_frame(kiln).findings if says in f.message] == [level]


def _flat(width: str, roof: str) -> Kiln:
    document = load_design(EXAMPLES / "gas-crossdraft.yaml").model_dump(mode="json", by_alias=True)
    document["chamber"]["width"] = width
    document["lining"]["roof"][0]["thickness"] = roof
    return Kiln.model_validate({**document, "roof": {"type": "flat"}})


def _check(kiln: Kiln, check_id: str) -> Check:
    found = [f.check for f in design_frame(kiln).findings if f.check and f.check.id == check_id]
    assert len(found) == 1, check_id
    return found[0]


def test_a_flat_roofs_sheets_say_what_would_pass() -> None:
    """18 in under 9 in: the ends need μ = 4d/3S = 0.667 against BIA's 0.60, so d ≤ 8.1 in holds.
    40 in passes Merrill's 36 in but not the 45 in of a roof on four walls."""
    deep = _check(_flat("18 in", "9 in"), "frame.flat-friction")
    assert deep.status == "error"
    assert deep.requirements[0].margin == "μ_need = 0.6667, 111.1 % of μ = 0.6"
    assert deep.solve == "Passes when t_1 ≤ 8.1 in"
    assert next(c for c in deep.cells if c.symbol == "μ_need").formula == "4·t_1/(3·S)"
    wide = _check(_flat("40 in", "3 in"), "frame.flat-span")
    assert wide.status == "warning"
    assert [r.holds for r in wide.requirements] == [True, False]
    assert wide.solve == "Passes when S ≤ 36 in"
    assert _check(_flat("48 in", "3 in"), "frame.flat-span").status == "error"


def test_a_flat_roofs_rods_and_a_cases_band_carry_its_thrust_in_the_sheet() -> None:
    document = load_design(EXAMPLES / "gas-crossdraft.yaml").model_dump(mode="json", by_alias=True)
    document["chamber"]["width"] = "100 in"
    document["lining"]["roof"] = [{"material": "mizzou-castable-plus", "thickness": "9 in"}]
    rods = _check(Kiln.model_validate({**document, "roof": {"type": "flat"}}), "frame.flat-rod")
    assert rods.status == "error"
    assert next(c for c in rods.cells if c.symbol == "H").formula == "3·q·S²/(8·t_1)"
    assert rods.solve is not None
    assert rods.solve.startswith("Passes when A_s ≥ ")


def test_an_electric_kiln_s_flat_roof_takes_olsens_rods() -> None:
    """Olsen's electric flat roof: rows of brick held by tie bolts through them, in an angle-iron
    frame, 'a basic requirement' (p.248–249). The electric example's 4½ in JM 26 over 22½ in: a
    3/8 in rod every 4½ in carries it well inside 12,000 psi."""
    frame = design_frame(load_design(EXAMPLES / "electric-front-loader.yaml"))
    assert not [f for f in frame.findings if f.level in ("warning", "error")]
    rods = next(m for m in frame.members if m.part.startswith("rods across the roof"))
    assert rods.steel == "3/8-16 threaded rod"
    assert rods.source is not None
    assert "Olsen" in rods.source


def test_a_domes_sheets_work_on_the_slice_that_decides_them() -> None:
    """The dome example at 8 in of rise: the middle slice, 3.00 in thick against HarbisonWalker's
    2.645 in, passes from 8.88 in of rise (the engine's own search says 8.9 in); its hot thrust
    passes HarbisonWalker's printed 5.34 times from 9.17 in."""
    document = load_design(EXAMPLES / "dome-castable-kiln.yaml").model_dump(
        mode="json", by_alias=True
    )
    document["roof"]["rise"] = "8 in"
    kiln = Kiln.model_validate(document)
    thick = _check(kiln, "frame.dome-thickness")
    assert thick.status == "error"
    assert thick.requirements[0].margin == "T = 3 in, 113.4 % of T_max = 2.645 in"
    assert thick.solve == "Passes when h ≥ 8.884 in"
    hot = _check(kiln, "frame.dome-heated-factor")
    assert hot.status == "warning"
    assert hot.solve == "Passes when h ≥ 9.168 in"  # not where the hot line leaves the ring
    steel = _check(kiln, "frame.dome-steel")
    assert {"H", "F", "F_tie"} <= {c.symbol for c in steel.cells}
    assert _check(kiln, "frame.dome-checked-range").solve == "Passes when t_1 ≤ 2.673 in"


def test_a_thin_dome_says_how_thick_to_stand() -> None:
    """Near a hemisphere, ¼ in of castable is under Heyman's factor of 2; η comes from his table
    at the slice's half-angle, so only the thickness is solved for."""
    document = load_design(EXAMPLES / "dome-castable-kiln.yaml").model_dump(
        mode="json", by_alias=True
    )
    document["roof"]["rise"] = "23 in"
    document["lining"]["roof"] = [{"material": "kast-o-lite-30-li-plus", "thickness": "0.25 in"}]
    standing = _check(Kiln.model_validate(document), "frame.dome-factor")
    assert standing.status == "error"
    assert standing.lever is not None
    assert standing.lever.symbol == "t_1"
    assert standing.solve is not None
    assert standing.solve.startswith("Passes when t_1 ≥ ")
    eta = next(c for c in standing.cells if c.symbol == "η")
    assert eta.source is not None
    assert "interpolated" in eta.source


def test_a_catenarys_sheet_shows_the_push_its_feet_need_held() -> None:
    feet = _check(load_design(EXAMPLES / "catenary-gas-kiln.yaml"), "frame.catenary-feet")
    by = {c.symbol: c for c in feet.cells}
    assert by["H_a"].value == pytest.approx(by["H_k"].value)  # a solves the crown's height
    assert by["H"].formula == "w·a"
    assert (feet.status, feet.rule_holds) == ("warning", False)


def test_a_fibre_flat_roof_hangs_from_its_frame_unchecked() -> None:
    """Fibre can't span as a flat arch; makers bolt fibre tops to a frame (flat-roofs.md §4.1)."""
    for name, roof_type in (
        ("electric-front-loader.yaml", "flat"),
        ("gas-crossdraft.yaml", "flat"),
    ):
        document = load_design(EXAMPLES / name).model_dump(mode="json", by_alias=True)
        document["lining"]["roof"] = [{"material": "kaowool-blanket-8pcf", "thickness": "4 in"}]
        frame = design_frame(Kiln.model_validate({**document, "roof": {"type": roof_type}}))
        assert frame.thrust is None
        assert any("A fibre roof can't span as a flat arch" in f.message for f in frame.findings)


def test_rods_too_thin_for_a_flat_roofs_thrust_say_so() -> None:
    """9 in of dense castable over 100 in (refused for its span too): each ⅜ in rod would carry
    its 4½ in of the roof's thrust past HarbisonWalker's 12,000 psi."""
    document = load_design(EXAMPLES / "gas-crossdraft.yaml").model_dump(mode="json", by_alias=True)
    document["chamber"]["width"] = "100 in"
    document["lining"]["roof"] = [{"material": "mizzou-castable-plus", "thickness": "9 in"}]
    frame = design_frame(Kiln.model_validate({**document, "roof": {"type": "flat"}}))
    assert any(
        "past HarbisonWalker's 12,000 psi for hot steel" in f.message for f in frame.findings
    )


def test_an_ifb_flat_roof_past_bnzs_2450_f_is_a_warning() -> None:
    """BNZ keeps suspended flat IFB roofs to 2450 °F (flat-roofs.md §4.4 [F15]): the electric
    example (a 4½ in JM 26 roof) fired to 2500 °F."""
    text = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    hot = parse_design(text.replace('  cone: "10"', '  cone: "10"\n  top_temperature: 2500 degF'))
    assert [f.level for f in design_frame(hot).findings if "BNZ keeps flat" in f.message] == [
        "warning"
    ]
    cool = design_frame(load_design(EXAMPLES / "electric-front-loader.yaml"))
    assert not [f for f in cool.findings if "BNZ keeps flat" in f.message]


@pytest.mark.parametrize("rise", ["16 in", "0 in", "-3 in"])
def test_an_arch_that_isnt_a_segment_is_refused(rise: str) -> None:
    """A segmental arch rises more than nothing and at most half its span. A rise of 0 used to
    divide by zero, and one past half the span drew the wrong shape (the review's structure 9)."""
    with pytest.raises(
        ValidationError, match="a sprung arch's rise must be more than 0 and at most"
    ):
        _gas_crossdraft({"type": "sprung_arch", "rise": rise})


def test_a_ring_of_more_layers_than_the_roof_has_is_refused() -> None:
    with pytest.raises(ValidationError, match="the arch's ring can't be 3 layers: the roof has 2"):
        _gas_crossdraft({"type": "sprung_arch", "rise": "3.75 in", "ring": "3"})


def _arch_of(
    roof: list[dict[str, str]],
    span: float,
    per_foot: float,
    walls: str = "4.5 in",
    ring: int = 1,
    depth: str = "45 in",
) -> Kiln:
    """A gas kiln with a sprung arch of ``span`` rising ``per_foot`` in/ft, KX-99 walls."""
    return Kiln.model_validate(
        {
            "name": "arch",
            "firing": {"cone": "10"},
            "chamber": {"width": f"{span} in", "depth": depth, "height": "40 in"},
            "roof": {"type": "sprung_arch", "rise": f"{per_foot * span / 12} in", "ring": ring},
            "lining": {
                "walls": [{"material": "hard-firebrick-kx99", "thickness": walls}],
                "roof": roof,
            },
            "heat": {"gas": {"supply": {"type": "cylinders", "count": 4}}},
        }
    )


def _errors(frame: object) -> list[str]:
    return [f.message for f in frame.findings if f.level == "error"]  # type: ignore[attr-defined]


IFB = {"material": "ifb-jm26", "thickness": "4.5 in"}
HARD = {"material": "hard-firebrick-kx99", "thickness": "4.5 in"}
CASTABLE = {"material": "kast-o-lite-30-li-plus", "thickness": "3 in"}
BLANKET = {"material": "kaowool-blanket-8pcf", "thickness": "2 in"}


@pytest.mark.parametrize(
    ("ring", "per_foot", "warned"),
    [
        (IFB, 1.5, False),  # Olsen's No. 1 featheredge arch, his kits and fast-fire kiln
        (IFB, 6.0, False),  # a semicircle: he has built 6 in/ft (p.51)
        (HARD, 1.25, True),
        (CASTABLE, 0.5, True),
        (CASTABLE, 3.5, False),  # past HarbisonWalker's 3 in/ft: Olsen's chamber kilns run 4–6
    ],
)
def test_olsens_least_rise_is_a_warning_and_there_is_no_most(
    ring: dict[str, str], per_foot: float, warned: bool
) -> None:
    """Olsen p.51: about 1½ in per foot of span at least, what a featheredge gives; less 'can
    result in structural difficulty'; 3 in/ft is 'generally' the most, but he has built 6 and
    there is 'no hard-and-fast rule'. HarbisonWalker's 1–3 in/ft (2–3 for IFB) would refuse his
    own kilns, so it no longer rules."""
    frame = design_frame(_arch_of([ring, BLANKET], 36, per_foot, walls="9 in"))
    rise = [f for f in frame.findings if f.check and f.check.id == "frame.rise"]
    assert [f.level for f in rise] == (["warning"] if warned else [])
    assert not [m for m in _errors(frame) if "per foot of span" in m]


def test_past_harbisonwalkers_thickest_ring_the_steel_takes_5_34_times_the_cold() -> None:
    """T ≤ (h − S/48) ÷ cos ½θ: 8.3 in for a 36 in span at 2.302 in/ft, 4.7 in at 1.608
    (kiln-hardware.md §4.5, derived). Past it HarbisonWalker's method has no hot thrust, and the
    steel takes the most it tabulates, with a note: no longer an error."""
    steep = design_frame(_arch_of([HARD], 36, 2.302))
    assert _value(steep, "Thickest ring for HarbisonWalker's heated-arch method") == "8.28 in"
    low = design_frame(_arch_of([{**HARD, "thickness": "6 in"}], 36, 1.608, walls="9 in"))
    assert _value(low, "Thickest ring for HarbisonWalker's heated-arch method") == "4.70 in"
    assert _errors(low) == [] or all("thicker" not in m for m in _errors(low))
    assert any("stress excessive" in f.message for f in low.findings)


def test_a_steep_factor_inside_harbisonwalkers_rules_takes_the_most_it_prints() -> None:
    """A 4½ in fireclay arch over 36 in at 1.608 in/ft is inside HarbisonWalker's thickness rule
    (4.70 in), but its statics heat it to 6.2 times its cold thrust, past the 5.34 HW prints
    before 'stress excessive'. The steel takes 5.34 × (the frame gives first), with a note. 24 in
    deep, so an angle can carry the thrust between the corner posts."""
    frame = design_frame(_arch_of([HARD], 36, 1.608, depth="24 in"))
    assert _errors(frame) == []
    assert not [f for f in frame.findings if f.level == "warning"]
    assert any("stress excessive" in f.message for f in frame.findings)
    assert frame.kind == "arch frame"


def test_pitelkas_soda_kiln_passes_with_its_brick_as_the_ring() -> None:
    """Pitelka's 20 ft³ soda kiln: a 36 in span at 2.3 in/ft, 4½ in hard brick under 4 in of
    insulating castable (kiln-hardware.md §4.2 [S4]). The castable is load, not ring: a factor
    of 2.44, not the 17.5 it gave counted as ring (the review's structure 4)."""
    soda = [HARD, {"material": "kast-o-lite-30-li-plus", "thickness": "4 in"}]
    frame = design_frame(_arch_of(soda, 36, 2.302))
    assert _errors(frame) == []
    assert _value(frame, "Arch ring") == "4.5 in, T/S 12.5 %"
    hot = next(s for s in frame.working if s.name == "Thrust of the heated arch, free to rise")
    assert hot.inputs["factor"] == "2.44"
    # Its weight still counts the castable
    weight = float(_value(frame, "Arch weight per foot of length").split()[0])
    alone = float(
        _value(design_frame(_arch_of([HARD], 36, 2.302)), "Arch weight per foot of length").split()[
            0
        ]
    )
    assert weight > alone * 1.4


def test_a_ring_of_fibre_is_refused_and_given_no_steel() -> None:
    """Blanket can't carry an arch: a fibre-only roof used to divide by zero (the review's
    structure 9), and a ring marked to include fibre is refused too."""
    only_fibre = design_frame(_arch_of([BLANKET], 36, 2.302))
    [error] = _errors(only_fibre)
    assert error.startswith("The arch's ring includes Morgan Kaowool ceramic fibre blanket")
    assert (only_fibre.kind, only_fibre.members) == (NO_FRAME, [])
    marked = design_frame(_arch_of([CASTABLE, BLANKET], 36, 2.302, ring=2))
    assert any("can't carry an arch's thrust" in m for m in _errors(marked))


def test_a_ring_wider_than_its_walls_is_refused() -> None:
    """A 3 in castable ring over 28 in at 1.608 in/ft reaches 15.5 in out at its skewback; on
    1 in walls (15 in out) the skewback would have no wall under it (the review's structure 6)."""
    frame = design_frame(_arch_of([CASTABLE, BLANKET], 28, 1.608, walls="1 in"))
    assert any(
        m.startswith("The arch's ring reaches 0.50 in past the outside of the side walls")
        for m in _errors(frame)
    )
    assert not [m for m in _errors(design_frame(_arch_of([CASTABLE], 28, 1.608))) if "reaches" in m]


def test_the_arch_frames_bottom_ring_is_counted_once_round_the_kiln() -> None:
    """The bottom cross-members used to be counted as four pieces each half the perimeter long:
    twice the steel (the review's structure 8)."""
    frame = design_frame(_dense_arch())
    members = {m.part: m for m in frame.members}
    front, sides = (
        members["bottom cross-members, front and back"],
        members["bottom cross-members, sides"],
    )
    leg = frame.angle_leg_in
    outside = (54 + 2 * 4.5, 45 + 2 * 4.5)  # inside plus the 4½ in walls
    assert (front.count, front.length_in) == (2, outside[0] + 2 * leg)
    assert (sides.count, sides.length_in) == (2, outside[1] + 2 * leg)


def test_the_buttress_working_says_which_section_modulus_it_uses() -> None:
    """The geometric axis's Sx, with the principal axis's Sz and its stress beside it (the
    review's structure 10)."""
    step = next(
        s for s in design_frame(_dense_arch()).working if s.name == "Buttress angle, bending"
    )
    assert step.note is not None
    assert "Sx is about a geometric axis" in step.note
    assert "where its Sz is 0.778 in³" in step.note  # L4×4×¼ (AISC)


def _big_hard_arch(roof: list[dict[str, str]], ring: int = 1, ties: str = "rigid") -> Kiln:
    """A hard-brick arch over 120 in, 72 in long inside (90 in outside)."""
    hard = [{"material": "hard-firebrick-kx99", "thickness": "9 in"}]
    arch: dict[str, object] = {"type": "sprung_arch", "rise": "16 in", "ring": ring, "ties": ties}
    if ties == "springs":
        arch["spring_rate"] = "283 lbf/in"
    return Kiln.model_validate(
        {
            "name": "big hard arch",
            "firing": {"cone": "10"},
            "chamber": {"width": "120 in", "depth": "72 in", "height": "60 in"},
            "roof": arch,
            "lining": {"walls": hard, "floor": hard, "roof": roof},
            "heat": {"gas": {"supply": {"type": "cylinders", "count": 4}}},
        }
    )


def test_a_heavy_arch_gets_posts_along_its_sides() -> None:
    """A 9 in hard-brick arch over 120 in is past what the largest angle, L4×4×3/8 (Sx 1.50 in³,
    AISC), carries over the 90 in between the corner posts, and what a ¾ in rod's 0.334 in²
    carries at HarbisonWalker's 12,000 psi. Builders brace large kilns with buckstays along the
    sides (kiln-hardware.md §4.1–4.2): the engine adds the fewest posts that let the steel carry
    the thrust between them, each pair tied across by a rod."""
    frame = design_frame(_big_hard_arch([{"material": "hard-firebrick-kx99", "thickness": "9 in"}]))
    assert not [f for f in frame.findings if f.level == "error"]
    assert frame.thrust is not None
    w = float(frame.thrust.split()[0]) / 12  # lb per inch of arch
    assert w * 90**2 / 8 / 12000 > 1.50  # the corner posts alone wouldn't do
    n = frame.posts
    bay = 90 / (n - 1)
    assert _value(frame, "Posts along the side walls") == f"{n} each side, {bay:.1f} in apart"
    assert w * bay**2 / 8 / 12000 <= 1.50  # an angle carries a bay
    assert w * bay / 0.334 <= 12000  # and a ¾ in rod the busiest pair of posts
    fewer = 90 / (n - 2)  # one post fewer each side
    assert w * fewer**2 / 8 / 12000 > 1.50 or w * fewer / 0.334 > 12000
    rods = _value(frame, f"Tie rods, one at each of the {n} pairs of posts")
    assert float(rods.split(": ")[1].split()[0].replace(",", "")) <= 12000
    parts = {m.part: m for m in frame.members}
    assert parts["posts, at the corners and along the sides"].count == 2 * n
    assert parts["tie rods"].count == n


def test_an_arch_too_heavy_for_posts_at_18_in_says_so() -> None:
    """Two 9 in rings: even with posts 18 in apart, two brick lengths, the closest the engine
    sets, no listed angle or rod carries a bay's thrust. Each error's sheet says what would
    pass."""
    hard = {"material": "hard-firebrick-kx99", "thickness": "9 in"}
    frame = design_frame(_big_hard_arch([hard, hard], ring=2))
    errors = [f for f in frame.findings if f.level == "error"]
    assert frame.posts == 6  # 90 in in five bays of 18 in
    angle, rod = errors
    assert angle.message == (
        "No angle up to L4×4×3/8 carries the arch's thrust over 18 in between posts, the shortest "
        "bay the engine sets (18 in or more). Lighten the arch, or hold it with masonry "
        "(buttressed)."
    )
    assert rod.message.startswith("No rod up to 3/4-10 carries the arch's thrust: the busiest of "
                                  "the 6 rods takes")  # fmt: skip
    assert rod.check is not None
    assert rod.check.solve is not None
    assert rod.check.solve.startswith("Passes when A_s ≥ ")
    assert not any("Weld the frame" in f.message for f in frame.findings)
    # With springs on its rods the frame keeps to its corner posts, and says why
    sprung = design_frame(_big_hard_arch([hard, hard], ring=2, ties="springs"))
    assert sprung.posts == 2
    [angle] = [f for f in sprung.findings if f.check and f.check.id == "frame.buttress"]
    assert angle.message.endswith("Tie the rods rigid, so posts can go along the side walls.")
    assert angle.check is not None
    assert angle.check.title == "Buttress angle, L4×4×3/8, in bending"
    # Nothing passed, so the smallest stands: Olsen's for a kiln his 5 × 5 × 6 ft size or bigger
    assert sprung.angle == "L3×3×1/4"


def _with_springs(rate: str) -> str:
    text = (EXAMPLES / "pnw-hybrid-crossdraft.yaml").read_text(encoding="utf-8")
    return text.replace(
        "  rise: 3.75 in", f"  rise: 3.75 in\n  ties: springs\n  spring_rate: {rate}", 1
    )


def test_springs_keep_the_hot_thrust_near_the_cold() -> None:
    """28 in span × 3/32 in/ft (Olsen p.51) = 0.219 in; each 283 lbf/in spring takes half:
    193 lb cold + 283 × 0.109 = 224 lb per rod, against 730 lb with rigid ties."""
    frame = design_frame(parse_design(_with_springs("283 lbf/in")))
    step = next(s for s in frame.working if s.name == "Tie rod load with springs, hot")
    assert step.value.startswith("224 lb per rod (rigid: 730 lb)")
    assert frame.angle == "L3×3×3/16"
    assert not [f for f in frame.findings if f.level == "warning"]


def test_stiff_springs_are_capped_at_the_rigid_frame() -> None:
    """A spring stiffer than the arch can push stays at Heyman's maximum, and the note that the
    statics run past the table comes back."""
    frame = design_frame(parse_design(_with_springs("100000 lbf/in")))
    step = next(s for s in frame.working if s.name == "Tie rod load with springs, hot")
    assert step.value.startswith("730 lb per rod")
    assert frame.angle == "L4×4×5/16"
    assert any("is past it" in f.message for f in frame.findings)


def test_springs_need_their_rate() -> None:
    with pytest.raises(ValidationError, match="spring_rate"):
        parse_design(_with_springs("283 lbf/in").replace("  spring_rate: 283 lbf/in", ""))
