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


def test_a_flat_thick_arch_is_refused_hot_and_given_no_steel() -> None:
    """2 in of rise under a 4½ in dense arch over 54 in: the hot thrust line leaves the brick, so
    there's no thrust to size steel by, and none is shown (the review's structure 4)."""
    document = _dense_arch().model_dump(mode="json", by_alias=True)
    kiln = Kiln.model_validate({**document, "roof": {"type": "sprung_arch", "rise": "2 in"}})
    frame = design_frame(kiln)
    errors = [f.message for f in frame.findings if f.level == "error"]
    assert any(m.startswith("Hot, this arch's thrust line would leave the ring") for m in errors)
    assert (frame.kind, frame.angle, frame.thrust, frame.members) == (NO_FRAME, None, None, [])
    assert not any("Weld the frame" in f.message for f in frame.findings)


def test_an_electric_kiln_has_a_case_and_the_hybrid_an_arch_frame() -> None:
    electric = design_frame(load_design(EXAMPLES / "electric-front-loader.yaml"))
    assert electric.kind == "welded case"
    hybrid = design_frame(load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml"))
    assert hybrid.kind == "arch frame"
    # Its 3 in castable arch is 10.7 % of the 28 in span: past the table, worked out by statics,
    # which sizes steel past what's been checked: a warning (the review's structure 3)
    [past] = [f for f in hybrid.findings if "outside it" in f.message]
    assert past.level == "warning"
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
    """The hybrid's 3 in arch over 28 in (T/S 10.7 %) gets a hot thrust, with a warning."""
    design = design_frame(load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml"))
    assert not [f for f in design.findings if f.level == "error" and "arch" in f.message]
    assert any("outside it" in f.message for f in design.findings)
    assert any(s.name.startswith("Thrust of the heated arch") for s in design.working)


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
    assert any(
        "The case, or a band round the roof, must squeeze it" in f.message for f in cool.findings
    )


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
    ("ring", "per_foot", "refused"),
    [
        (IFB, 1.608, "HarbisonWalker gives 2–3 in/ft"),  # insulating firebrick: 2–3
        (IFB, 2.302, None),
        (HARD, 1.25, "HarbisonWalker gives 1.5–3 in/ft"),  # fireclay: 1½–3
        (HARD, 1.608, None),
        (CASTABLE, 0.5, "HarbisonWalker gives 1–3 in/ft"),  # castables aren't named: 1–3
        (CASTABLE, 1.608, None),
        (CASTABLE, 3.5, "HarbisonWalker gives 1–3 in/ft"),
    ],
)
def test_harbisonwalkers_rise_for_the_ring_is_enforced(
    ring: dict[str, str], per_foot: float, refused: str | None
) -> None:
    """kiln-hardware.md §4.4 [S20]: a roof arch rises 1 to 3 in/ft; fireclay brick 1½–3,
    insulating firebrick 2–3 (the review's structure 2). A 0.5 in/ft arch used to pass."""
    frame = design_frame(_arch_of([ring, BLANKET], 36, per_foot, walls="9 in"))
    rise = [m for m in _errors(frame) if "per foot of span" in m]
    if refused is None:
        assert rise == []
    else:
        [message] = rise
        assert refused in message


def test_harbisonwalkers_thickest_ring_is_enforced() -> None:
    """T ≤ (h − S/48) ÷ cos ½θ: 8.3 in for a 36 in span at 2.302 in/ft, 4.7 in at 1.608
    (kiln-hardware.md §4.5, derived)."""
    steep = design_frame(_arch_of([HARD], 36, 2.302))
    assert _value(steep, "Thickest ring for the rise") == "8.28 in"
    low = design_frame(_arch_of([{**HARD, "thickness": "6 in"}], 36, 1.608, walls="9 in"))
    assert _value(low, "Thickest ring for the rise") == "4.70 in"
    assert any(
        "thicker than HarbisonWalker allows for its rise, 4.70 in" in m for m in _errors(low)
    )


def test_a_steep_factor_inside_harbisonwalkers_rules_is_a_warning_not_a_refusal() -> None:
    """A 4½ in fireclay arch over 36 in at 1.608 in/ft is inside HarbisonWalker's rise and
    thickness rules (4.70 in), but heats to 6.2 times its cold thrust, past the 5.34 HW prints.
    It used to be refused; the 5.34 is only a guard (the review's structure 2). 24 in deep, so
    an angle can carry the thrust between the corner posts."""
    frame = design_frame(_arch_of([HARD], 36, 1.608, depth="24 in"))
    assert _errors(frame) == []
    [guard] = [f for f in frame.findings if f"{MAX_PRINTED_HEATED:g} times" in f.message]
    assert guard.level == "warning"
    assert "pushes 6.2 times its cold thrust" in guard.message
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


def test_an_arch_too_heavy_for_any_angle_or_rod_says_so() -> None:
    """A 9 in hard-brick arch over 120 in, 72 in long inside (90 in outside). The thrust passes
    what the largest angle, L4×4×3/8 (Sx 1.50 in³, AISC), carries between the corner posts, and
    what a ¾ in rod's 0.334 in² carries at HarbisonWalker's 12,000 psi."""
    hard = [{"material": "hard-firebrick-kx99", "thickness": "9 in"}]
    kiln = Kiln.model_validate(
        {
            "name": "big hard arch",
            "firing": {"cone": "10"},
            "chamber": {"width": "120 in", "depth": "72 in", "height": "60 in"},
            "roof": {"type": "sprung_arch", "rise": "16 in"},
            "lining": {"walls": hard, "floor": hard, "roof": hard},
            "heat": {"gas": {"supply": {"type": "cylinders", "count": 4}}},
        }
    )
    frame = design_frame(kiln)
    assert [f.message for f in frame.findings if f.level == "error"] == [
        "No angle up to L4×4×3/8 carries the arch's thrust over 90 in between the corner posts. "
        "Add posts along the side walls.",
        "No rod up to ¾ in carries the arch's thrust.",
    ]
    assert frame.thrust is not None
    thrust = float(frame.thrust.split()[0])  # lb per foot of arch
    # Bending: M = wL²/8 over the 90 in, against 12,000 psi
    needed = thrust / 12 * 90**2 / 8 / 12000
    assert needed > 1.50
    bending = _value(frame, "Buttress angle, bending")
    assert float(bending.split("≥ ")[1].split()[0]) == pytest.approx(needed, rel=1e-3)
    # The rods: half the thrust on the 90 in (7.5 ft) each, on 0.334 in²
    rods = _value(frame, "Tie rods, one at the front and one at the back")
    psi = float(rods.split(": ")[1].split()[0].replace(",", ""))
    assert psi == pytest.approx(thrust * 7.5 / 2 / 0.334, rel=1e-3)
    assert psi > 12000
    assert frame.rod == "3/4-10"
    assert frame.angle == "L3×3×3/16"  # nothing passed, so the smallest stands
    assert not any("Weld the frame" in f.message for f in frame.findings)


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
    """A spring stiffer than the arch can push stays at Heyman's maximum, and the table
    warning comes back."""
    frame = design_frame(parse_design(_with_springs("100000 lbf/in")))
    step = next(s for s in frame.working if s.name == "Tie rod load with springs, hot")
    assert step.value.startswith("730 lb per rod")
    assert frame.angle == "L4×4×5/16"
    assert any("outside it" in f.message for f in frame.findings)


def test_springs_need_their_rate() -> None:
    with pytest.raises(ValidationError, match="spring_rate"):
        parse_design(_with_springs("283 lbf/in").replace("  spring_rate: 283 lbf/in", ""))
