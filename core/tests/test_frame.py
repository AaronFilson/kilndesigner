"""The frame: arch thrust checked against HarbisonWalker's tables, and the steel it picks."""

from __future__ import annotations

from pathlib import Path

import pytest

from kilndesigner import load_design
from kilndesigner.frame import (
    MAX_PRINTED_HEATED,
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


def test_a_flat_thick_arch_is_refused_hot() -> None:
    """2 in of rise under a 9 in dense arch: the hot thrust line leaves the brick."""
    document = _dense_arch().model_dump(mode="json", by_alias=True)
    kiln = Kiln.model_validate({**document, "roof": {"type": "sprung_arch", "rise": "2 in"}})
    frame = design_frame(kiln)
    assert any(f.level == "error" and "Raise the arch" in f.message for f in frame.findings)


def test_an_electric_kiln_has_a_case_and_the_hybrid_an_arch_frame() -> None:
    electric = design_frame(load_design(EXAMPLES / "electric-front-loader.yaml"))
    assert electric.kind == "welded case"
    hybrid = design_frame(load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml"))
    assert hybrid.kind == "arch frame"
    # Its 3 in castable arch is 10.7 % of the 28 in span: past the table, worked out by statics
    assert any("outside it" in f.message for f in hybrid.findings)
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
    of the kiln" (kiln-hardware.md §4.2 [S16]). Outside, the kiln is 28 + 2 × 8 = 44 in wide and
    7 + 40 + 5 = 52 in tall; the rods cross the 44 in and both 2 in angle legs, plus 4 in."""
    frame = design_frame(_gas_crossdraft({"type": "flat"}))
    assert (frame.kind, frame.angle, frame.rod) == ("angle frame", "L2×2×3/16", "3/8-16")
    assert (frame.angle_leg_in, frame.angle_t_in, frame.rod_d_in) == (2, 0.1875, 0.375)
    assert frame.thrust is None  # a flat roof pushes nothing out
    assert frame.findings == []
    members = {m.part: m for m in frame.members}
    assert set(members) == {"corner posts", "roof angle, all four sides", "tie rods"}
    assert (members["corner posts"].count, members["corner posts"].length_in) == (4, 52)
    assert (members["tie rods"].count, members["tie rods"].length_in) == (2, 44 + 2 * 2 + 4)
    merrill = "Merrill flat-top kiln; kiln-hardware.md §4.2 [S16]"
    assert {m.source for m in frame.members} == {merrill}


@pytest.mark.parametrize("rise", ["16 in", "-3 in"])
def test_an_arch_that_isnt_a_segment_is_refused_its_thrust(rise: str) -> None:
    """A segmental arch rises more than nothing and less than half its span; outside that,
    HarbisonWalker's method doesn't apply, so no thrust is given and nothing is sized by it."""
    frame = design_frame(_gas_crossdraft({"type": "sprung_arch", "rise": rise}))
    [error] = [f for f in frame.findings if f.level == "error"]
    assert error.message == (
        f"The arch's rise of {float(rise.split()[0]):.2f} in must be above 0 and below half the "
        "28.0 in span for a segmental arch, so the frame can't be checked."
    )
    assert frame.thrust is None
    names = [s.name for s in frame.working]
    assert names == ["Smallest frame angle", "Arch weight per foot of length"]
    # The bricked door's smallest angle, from Pitelka, and builders' ½ in rods, unchecked
    assert (frame.angle, frame.rod) == ("L3×3×3/16", "1/2-13")
    assert not any("Weld the frame" in f.message for f in frame.findings)
    assert {m.part for m in frame.members} >= {"corner posts", "buttresses behind the skewbacks"}


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
