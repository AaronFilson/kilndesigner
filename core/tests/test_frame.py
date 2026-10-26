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
