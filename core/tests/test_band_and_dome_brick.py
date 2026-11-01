"""The hot band round a dome (band.py) and Norton's dome counts (dome_brick.py)."""

from __future__ import annotations

import math
from collections.abc import Callable
from pathlib import Path

import pytest

from kilndesigner import band
from kilndesigner.designfile import load_design
from kilndesigner.dome_brick import norton_count, norton_dome, radial_dome, radial_small_end
from kilndesigner.frame import design_frame, steel_data
from kilndesigner.masonry import plan_masonry
from kilndesigner.model import Kiln

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"


def _breda(rise: str | None = None, **chamber: object) -> Kiln:
    k = load_design(EXAMPLES / "olsen" / "breda-bottle.yaml")
    data = k.model_dump(mode="json")
    data["chamber"].update(chamber)
    if rise is not None:
        data["roof"]["rise"] = rise
    return Kiln.model_validate(data)


def _at(t_c: float) -> Callable[[Kiln], float]:
    def temperature(_: Kiln) -> float:
        return t_c

    return temperature


def test_ky_follows_en_1993_1_2_table_3_1() -> None:
    data = steel_data()["band"]
    assert band.ky(data, 0) == 1.0
    assert band.ky(data, 400) == 1.0
    assert band.ky(data, 450) == pytest.approx(0.89)  # (1.000 + 0.780) / 2, not the Snippet's 0.93
    assert band.ky(data, 600) == pytest.approx(0.47)
    with pytest.raises(ValueError, match="1200"):
        band.ky(data, 1200)


def test_breda_band_holds_with_norton_on_yield() -> None:
    frame = design_frame(_breda())
    found = next(f for f in frame.findings if f.message.startswith("The band round"))
    assert found.level == "info"
    assert found.check is not None
    assert "Norton's 5 on the yield, hot governs" in found.message
    assert any(s.name == "Dome band: its temperature" for s in frame.working)


def test_band_fails_when_the_ring_is_too_much(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(band, "band_temperature", _at(550.0))
    steps, found = band.dome_band(_breda(), 10_000)
    assert found.level == "error"
    assert found.check is not None
    # k_y at 550 °C is 0.625: 36,000 × 0.625 / 5 = 4,500 psi, under HarbisonWalker's 12,000
    assert "4,500 psi" in steps[1].value


def test_band_refused_past_the_table(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(band, "band_temperature", _at(1250.0))
    steps, found = band.dome_band(_breda(), 1_000)
    assert steps == []
    assert found.level == "info"
    assert "isn't checked" in found.message


def test_norton_worked_example() -> None:
    """Norton p.731–732: r = 120 in, t = 9 in, 60° spring to spring."""
    c = norton_count(120, 120 * (1 - math.cos(math.radians(30))), 9)
    assert round(c.first_ring) == 90
    assert round(c.rings) == 54
    assert round(c.wedge_rings) == 15
    assert c.first_keys == pytest.approx(58, rel=0.03)
    assert c.total == pytest.approx(1230, rel=0.03)
    # His split of the 1,230 (342 wedges, 585 keys, 303 straights): the step is lost in the scan
    assert c.wedges == pytest.approx(342, rel=0.03)
    assert c.keys == pytest.approx(585, rel=0.08)
    assert c.straights == pytest.approx(303, rel=0.08)
    assert c.wedges + c.keys + c.straights == math.ceil(c.total)


def test_norton_refuses_what_it_doesnt_reach() -> None:
    with pytest.raises(ValueError, match="9 in"):
        norton_count(120, 20, 4.5)
    with pytest.raises(ValueError, match="too tight"):
        norton_count(48, 10, 9)
    with pytest.raises(ValueError, match="rises"):
        norton_count(48, 60, 9)


def test_radial_dome_brick_gives_table_155() -> None:
    table = {4: (3.79, 2.11), 6: (4.00, 2.22), 8: (4.12, 2.29), 10: (4.18, 2.33),
             14: (4.28, 2.37), 18: (4.33, 2.40), 24: (4.36, 2.42), 30: (4.39, 2.44),
             40: (4.42, 2.45)}  # fmt: skip
    for ft, (w, t) in table.items():
        got = radial_small_end(ft * 12)
        assert got[0] == pytest.approx(w, abs=0.011)
        assert got[1] == pytest.approx(t, abs=0.011)
    with pytest.raises(ValueError, match="Table 155"):
        radial_dome(40, 10, 9)
    with pytest.raises(ValueError, match="9 in"):
        radial_dome(120, 10, 4.5)
    hemisphere = radial_dome(120, 120, 9)
    assert hemisphere.counts[0][1] == math.ceil(2 * math.pi * 129**2 / 11.25)
    assert norton_dome(120, 16, 9).counts[0][0] == "straight"


@pytest.mark.parametrize(("how", "said"), [("norton", "Norton's ring count"),
                                            ("radial", "Norton's radial dome brick"),
                                            (None, "straights, course by course")])  # fmt: skip
def test_breda_dome_counted_each_way(how: str | None, said: str) -> None:
    plan = plan_masonry(_breda(dome_bricks=how))
    assert any(s.name.startswith("Dome, layer 1") and s.value.startswith(said)
               for s in plan.result.working)  # fmt: skip


def test_norton_falls_back_where_it_doesnt_reach() -> None:
    plan = plan_masonry(_breda("15 in", width="60 in", depth="60 in", dome_bricks="radial"))
    step = next(
        s for s in plan.result.working if s.name == "Dome, layer 1 from the inside: counted by"
    )
    assert "doesn't reach it" in step.value


def test_dome_bricks_only_for_a_round_kiln() -> None:
    k = load_design(EXAMPLES / "electric-front-loader.yaml")
    data = k.model_dump(mode="json")
    data["chamber"]["dome_bricks"] = "norton"
    with pytest.raises(ValueError, match="dome_bricks"):
        Kiln.model_validate(data)
