"""Wood, coal and oil firing (:mod:`kilndesigner.fire`): Olsen's chimney and firebox rules, checked
against his worked examples (*The Kiln Book*, 4th ed.)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pytest

from kilndesigner import load_design
from kilndesigner.fire import design_fire, pull
from kilndesigner.model import Fire, Kiln


def _kiln(**changes: Any) -> Kiln:
    """Olsen's chimney example (p.79–80, Fig. 3-14): a cross-draft chamber 5 ft along the draft and
    6 ft to the top inside; 1 ft from it to the chimney (a 9 in flue wall and a 3 in run); a
    chimney 1 ft across. Its grate is 10 × the chimney's 144 in², the most Olsen gives (p.76).
    ``changes`` replace parts: ``draft__chimney={...}`` replaces draft.chimney, and so on."""
    document: dict[str, Any] = {
        "name": "Olsen's chimney example",
        "firing": {"cone": "10"},
        "chamber": {"width": "48 in", "depth": "60 in", "height": "72 in"},
        "lining": {"walls": [{"material": "hard-firebrick-kx99", "thickness": "9 in"}]},
        "heat": {
            "fire": {
                "fuel": "wood",
                "fireboxes": [
                    {
                        "width": "48 in",
                        "length": "36 in",
                        "grate": {"width": "48 in", "length": "30 in"},
                    }
                ],
            }
        },
        "draft": {
            "type": "cross",
            "run_to_chimney": "3 in",
            "chimney": {"height": "244 in", "inside": {"width": "12 in", "depth": "12 in"}},
        },
    }
    for path, value in changes.items():
        *parents, last = path.split("__")
        target = document
        for key in parents:
            target = target.setdefault(key, {})
        if value is None:
            target.pop(last, None)
        else:
            target[last] = value
    return Kiln.model_validate(document)


def _checks(kiln: Kiln) -> dict[str, str]:
    """Each warning's check id and message."""
    fire = design_fire(kiln)
    return {f.check.id: f.message for f in fire.findings if f.check is not None}


def test_rule_5_reproduces_olsens_chimney_example() -> None:
    """3 × 6 ft of downward pull is 18 ft, and the horizontal pull, 5 + 1 + 1 ft, adds a third of
    itself, 2 ft 4 in: 20 ft 4 in, the most (p.80). The least is the early proportions: a chimney
    twice the chamber's height (p.130, Fig. 5-2: 4 m on a 2 m cube), 12 ft."""
    kiln = _kiln()
    assert kiln.heat.fire is not None
    p = pull(kiln, kiln.heat.fire.fireboxes, forced=False, chimney=12)
    assert (p.down, p.across, p.rise) == pytest.approx((72, 84, 0))
    fire = design_fire(kiln)
    assert fire.chimney_range == "12.0–20.3 ft"
    assert fire.chimney_height_in == pytest.approx(244)
    assert _checks(kiln) == {}  # 20 ft 4 in, and the grate 10 × the chimney
    assert fire.flue_area_in2 == pytest.approx(0.75 * 144)  # 3 bricks into 4 (p.78)
    assert not any("taller than" in f.message for f in fire.findings)


def test_olsens_groundhogs_sit_between_the_least_and_the_most() -> None:
    """p.112: groundhog chimneys of 5–10 ft on chambers 29–48 in high. Twice the chamber's height
    is 4.8–8 ft, so the book's 5 ft on a 29 in groundhog and 10 ft on a 48 in one both pass."""
    for crown, chimney in (("29 in", "5 ft"), ("48 in", "10 ft")):
        kiln = _kiln(
            chamber={"width": "96 in", "depth": "180 in", "height": crown},
            draft__chimney={"height": chimney, "inside": {"width": "96 in", "depth": "9 in"}},
            heat__fire__fireboxes=[{"width": "96 in", "length": "48 in"}],
        )
        assert "fire.chimney" not in _checks(kiln)


def test_with_no_chimney_given_the_engine_builds_rule_5s() -> None:
    """The section is the grate ÷ 7 in half-brick sizes: 1440 ÷ 7 = 206 in² → 13½ × 18 in, which
    adds 13½ in to the horizontal pull."""
    fire = design_fire(_kiln(draft__chimney=None))
    assert fire.chimney_area_in2 == pytest.approx(13.5 * 18)
    # Olsen's 20 ft 4 in, plus a third of the 1½ in the wider chimney adds to the pull
    assert fire.chimney_height_in == pytest.approx(244 + 1.5 / 3)


def test_rule_5_reproduces_wards_worked_example() -> None:
    """Ward [S32] (combustion-and-masonry.md §4.1): 36 in inside, 54 in of linear draw (36 in deep,
    a 9 in back wall, 9 in to the chimney's base): 3 × 36 + 54/3 = 126 in. Ward stops at the
    chimney's base, Olsen counts its width too, so a 9 in chimney adds 3 in: 129 in."""
    kiln = _kiln(
        chamber={"width": "48 in", "depth": "36 in", "height": "36 in"},
        draft__run_to_chimney="9 in",
        draft__chimney={"height": "11 ft", "inside": {"width": "9 in", "depth": "9 in"}},
    )
    span = design_fire(kiln).chimney_range
    assert span is not None
    most = float(span.split("–")[1].split()[0]) * 12
    assert most == pytest.approx(126 + 9 / 3, abs=0.61)  # printed to 0.1 ft: 10.75 shows as 10.8
    assert most / 126 - 1 == pytest.approx(0.024, abs=0.005)


def test_a_chimney_under_the_least_is_a_warning_and_over_the_most_a_note() -> None:
    low = {"height": "10 ft", "inside": {"width": "12 in", "depth": "12 in"}}
    [message] = _checks(_kiln(draft__chimney=low)).values()
    assert message.startswith("The chimney is 10.0 ft, under the 12.0 ft")
    tall = {"height": "30 ft", "inside": {"width": "12 in", "depth": "12 in"}}
    fire = design_fire(_kiln(draft__chimney=tall))
    assert _checks(_kiln(draft__chimney=tall)) == {}
    assert any("taller than the 20.3 ft" in f.message and "(Rule 5)" in f.message
               for f in fire.findings)  # fmt: skip


def test_forced_draft_needs_less_chimney_and_altitude_more() -> None:
    """A quarter less with a blower (p.79, p.130); 30 % more above about 4000 ft (p.81)."""
    forced = design_fire(_kiln(heat__fire__forced=True))
    assert forced.chimney_range == "9.0–15.2 ft"
    high = design_fire(_kiln(site={"elevation": "5000 ft"}))
    assert high.chimney_range == "15.6–26.4 ft"
    # The same chimney draws less in thinner air: the draft at its base, in. w.c.
    sea = design_fire(_kiln())
    assert float(high.draft[0].split()[0]) < float(sea.draft[0].split()[0])


def test_fireboxes_under_the_floor_add_to_the_downward_pull() -> None:
    """Olsen's fast-fire kiln pulls down through its fireboxes too (p.140): 36 in to the
    springline, a 3⅜ in arch, and the five-course firebox, 6 in above the grate and 6½ in below it
    (Fig 5-39, p.199)."""
    kiln = load_design(Path(__file__).parents[2] / "examples" / "olsen" / "fast-fire.yaml")
    assert kiln.heat.fire is not None
    p = pull(kiln, kiln.heat.fire.fireboxes, forced=False)
    assert p.down == pytest.approx(36 + 3.375 + 6 + 6.5)


def test_a_climbing_kilns_chimney_reaches_the_line_of_its_chamber_tops() -> None:
    """p.81: at least the line through the chamber tops, and Rule 5 doesn't cover a climbing
    kiln; p.101: the Bizen kiln's chimney is about 3 × its rise. With none given, the engine
    proposes the least: the slope draws."""
    kiln = _kiln(chamber={"width": "48 in", "depth": "60 in", "height": "72 in", "chambers": 3,
                          "slope": "18.43 degree"})  # fmt: skip
    assert kiln.heat.fire is not None
    p = pull(kiln, kiln.heat.fire.fireboxes, forced=False, chimney=12)
    rise = math.tan(math.radians(18.43)) * (180 + 9 + 3)
    assert p.rise == pytest.approx(rise)
    assert p.down == pytest.approx(72)
    fire = design_fire(kiln)
    least, most = rise + 72, 3 * rise
    assert fire.chimney_range == f"{least / 12:.1f}–{most / 12:.1f} ft"
    assert _checks(kiln) == {}  # 244 in is over the chamber tops' line
    assert any("(3 × the kiln's rise)" in f.message for f in fire.findings)  # and over 3 × rise
    low = {"height": "10 ft", "inside": {"width": "12 in", "depth": "12 in"}}
    [message] = _checks(kiln.model_copy(update={"draft": _kiln(draft__chimney=low).draft})).values()
    assert message.startswith(f"The chimney is 10.0 ft, under the {least / 12:.1f} ft")
    proposed = kiln.model_copy(update={"draft": _kiln(draft__chimney=None).draft})
    assert design_fire(proposed).chimney_height_in == pytest.approx(least)
    # A shallow slope: 3 × the rise is under the chamber-top line, which is then the most too
    gentle = _kiln(chamber={"width": "48 in", "depth": "60 in", "height": "72 in", "chambers": 3,
                            "slope": "2 degree"})  # fmt: skip
    low_rise = math.tan(math.radians(2)) * 192
    assert design_fire(gentle).chimney_range == (
        f"{(low_rise + 72) / 12:.1f}–{(low_rise + 72) / 12:.1f} ft"
    )


def test_the_grate_against_the_chimney() -> None:
    """Wood: the grate 4 to 10 × the chimney's section (p.76–77)."""
    big = {"height": "244 in", "inside": {"width": "18 in", "depth": "27 in"}}
    assert _checks(_kiln(draft__chimney=big)) == {
        "fire.grate": "The grate is 3.0 times the chimney's section, outside the 4–10 times "
        "Olsen's wood kilns span (about 7 now, 4 in groundhogs). The chimney may pull too hard or "
        "too little for the fire."
    }
    small = {"height": "244 in", "inside": {"diameter": "12 in"}}
    assert set(_checks(_kiln(draft__chimney=small))) == {"fire.grate"}
    # With no grate, its firebox floor
    floor = {"width": "48 in", "length": "36 in"}
    assert (
        "firebox floor is 12.0 times" in _checks(_kiln(heat__fire__fireboxes=[floor]))["fire.grate"]
    )


def test_a_round_chimney_and_a_side_flue_count_their_width_in_the_pull() -> None:
    round_ = _kiln(draft__chimney={"height": "244 in", "inside": {"diameter": "15 in"}})
    assert design_fire(round_).chimney_range == "12.0–20.4 ft"  # (60 + 12 + 15) ÷ 3
    side = _kiln(
        draft={"type": "cross", "flue_wall": "left", "run_to_chimney": "3 in",
               "chimney": {"height": "244 in", "inside": {"width": "15 in", "depth": "9 in"}}},
    )  # fmt: skip
    assert design_fire(side).chimney_range == "12.0–20.1 ft"  # (48 + 12 + 15) ÷ 3 = 25 in


def test_coal_wants_a_grate_of_an_eighth_of_the_floor() -> None:
    """p.206: 1 ft² of coal grate for every 6–8 ft² of floor."""
    coal = _kiln(heat__fire__fuel="coal")
    assert _checks(coal) == {}  # 10 ft² of grate under a 20 ft² floor
    small = [{"width": "12 in", "length": "12 in", "grate": {"width": "12 in", "length": "12 in"}}]
    checks = _checks(_kiln(heat__fire__fuel="coal", heat__fire__fireboxes=small))
    assert checks == {
        "fire.coal-grate": "The coal grates are under 1 ft² per 8 ft² of floor, the least Olsen "
        "gives (1 per 6–8)."
    }


def test_oil_burns_at_132000_btu_a_gallon_and_wants_a_fifth_of_the_floor() -> None:
    """p.214: 132,000 BTU per gallon of #2 diesel; p.213: 1 ft² of combustion area per 5 ft² of
    floor."""
    oil = _kiln(heat__fire__fuel="oil", heat__fire__oil_burners=2,
                heat__fire__oil_rate="1.75 gallon/hour", heat__fire__forced=True)  # fmt: skip
    fire = design_fire(oil)
    assert fire.full_fire_btu_hr == pytest.approx(2 * 1.75 * 132_000)  # Olsen's 462,000 (p.212)
    assert _checks(oil) == {}  # 12 ft² of firebox under a 20 ft² floor
    small = [{"width": "12 in", "length": "24 in"}]  # 2 ft², under the 4
    checks = _checks(_kiln(heat__fire__fuel="oil", heat__fire__fireboxes=small))
    assert set(checks) == {"fire.oil-area"}


def test_wood_beside_gas_needs_an_auxiliary_air_source_or_a_full_chimney() -> None:
    """Olsen p.79: a chimney for gas under pressure can be at least 25 % shorter, but "If a
    combination of wood is also to be used, then you must provide an auxillary air source"."""
    gas = {"supply": {"type": "cylinders", "count": 4}}
    short = {"height": "10 ft", "inside": {"width": "12 in", "depth": "12 in"}}
    hybrid = _kiln(heat__gas=gas, draft__chimney=short)
    [warning] = [f for f in design_fire(hybrid).findings if f.check is not None]
    assert warning.check is not None
    assert warning.check.id == "fire.auxiliary-air"
    assert warning.message.startswith("This kiln burns wood with its gas, and its chimney, 10.0 ft")
    assert "'If a combination of wood is also to be used" in warning.message
    # With a blower for the wood the chimney may be a quarter shorter: 9 ft passes, 8 ft doesn't
    blown = _kiln(heat__gas=gas, heat__fire__forced=True, draft__chimney=short)
    assert _checks(blown) == {}
    lower = _kiln(heat__gas=gas, heat__fire__forced=True,
                  draft__chimney={**short, "height": "8 ft"})  # fmt: skip
    assert set(_checks(lower)) == {"fire.chimney"}
    # A chimney tall enough to draw the wood passes, with a note on the choice
    full = design_fire(_kiln(heat__gas=gas))
    assert not [f for f in full.findings if f.level != "info"]
    assert any("auxiliary air source, a blower (p.79)" in f.message for f in full.findings)


def test_with_gas_and_a_fire_the_drawn_chimney_is_the_fires() -> None:
    """The chimney must draw the fire (p.79), so the hardware builds the fire's, not the gas's."""
    from kilndesigner.hardware import build_hardware
    from kilndesigner.report import design_report

    kiln = _kiln(heat__gas={"supply": {"type": "cylinders", "count": 4}})
    report = design_report(kiln)
    assert report.fire is not None
    assert report.gas is not None
    hw = build_hardware(kiln, report.frame, report.gas, report.fire)
    stack = next(p for p in hw.pieces if p.name == "chimney/stack")
    top = max(hi[2] for _, hi in stack.boxes) / 25.4
    assert top == pytest.approx(report.fire.chimney_height_in)
    step = next(s for s in report.gas.working if s.name == "Chimney height")
    assert step.note is not None
    assert "the one drawn is the fire's (Olsen p.79)" in step.note


def test_an_updraft_has_no_chimney_rule() -> None:
    fire = design_fire(_kiln(draft={"type": "up"}))
    assert fire.chimney_height is None
    assert fire.chimney_range is None
    assert any("An updraft's gases rise" in f.message for f in fire.findings)
    assert design_fire(_kiln(draft=None)).chimney_height is None


def test_only_fireboxes_with_inlets_give_the_inlet_area() -> None:
    inlet = {"width": "4.5 in", "height": "13.5 in"}
    two = [{"count": 2, "width": "13.5 in", "length": "40 in", "inlet": inlet, "inlets": 2}]
    assert design_fire(_kiln(heat__fire__fireboxes=two)).inlet_area_in2 == pytest.approx(243)
    mixed = [*two, {"width": "13.5 in", "length": "40 in"}]
    assert design_fire(_kiln(heat__fire__fireboxes=mixed)).inlet_area_in2 is None


def test_a_kiln_with_no_fire_has_no_fire_design() -> None:
    kiln = _kiln()
    gasless = kiln.model_copy(update={"heat": kiln.heat.model_copy(update={"fire": None})})
    with pytest.raises(ValueError, match="no fireboxes"):
        design_fire(gasless)


GAS = {"fuel": "natural_gas", "supply": {"type": "line", "pressure": "7 inch_H2O"}}


def _smoked() -> Kiln:
    """The electric front-loader with Olsen's smoke firebox beside it (p.250, Fig. 9-25): 18 in
    deep with a grate; his drawing gives no width, so the 9 in air inlet's width is used."""
    kiln = load_design(Path(__file__).parents[2] / "examples" / "electric-front-loader.yaml")
    box = {
        "position": "back",
        "width": "9 in",
        "length": "18 in",
        "grate": {"width": "9 in", "length": "18 in"},
    }
    fire = Fire.model_validate({"purpose": "smoke", "fireboxes": [box]})
    return kiln.model_copy(update={"heat": kiln.heat.model_copy(update={"fire": fire})})


def test_a_smoke_firebox_reduces_an_electric_kiln_without_heat_rules() -> None:
    """Olsen p.250: the firebox fills the kiln with smoke, 'not to add heat', so no grate ratio
    or chimney height is checked; his sizes are reported, and the elements' shorter life."""
    fire = design_fire(_smoked())
    assert fire.chimney_height is None
    assert all(f.check is None for f in fire.findings)
    text = " ".join(f.message for f in fire.findings)
    assert "6 × 6 in chimney" in text
    assert "oxide coat" in text
    assert "M7" not in text


def test_a_smoke_firebox_without_elements_says_nothing_of_them() -> None:
    kiln = _kiln(heat__fire__purpose="smoke", heat__gas=GAS)
    assert not any("oxide coat" in f.message for f in design_fire(kiln).findings)


def test_a_smoke_firebox_burns_wood_beside_another_heat() -> None:
    with pytest.raises(ValueError, match="burns wood"):
        _kiln(heat__fire__purpose="smoke", heat__fire__fuel="coal")
    with pytest.raises(ValueError, match="give it elements or burners"):
        _kiln(heat__fire__purpose="smoke")
