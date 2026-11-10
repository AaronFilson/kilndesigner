"""v2 statics on every reference kiln (ADR 0017, decision 17; the user, 2026-11-10): the kilns in
the book all stood and worked for their builders, so every one v2 models must stand, cold and hot.
Where v2 can't yet model one, what is missing is said, and the set is pinned here so a kiln can't
drop out of the model unnoticed. None is fitted: the kilns only check the model."""

from pathlib import Path

import pytest

from kilndesigner.designfile import load_design
from kilndesigner.v2.statics.kiln import KilnStatics, statics

ROOT = Path(__file__).resolve().parents[3]
OLSEN = ROOT / "examples" / "olsen"

NOT_MODELLED = {
    # stands cold; hot, its verdict rests on dense brick's 25 psi crushing stand-in, carried over
    # from IFB by analogy (a question for the user), so it isn't given
    "tobe": "dense brick's hot crushing",
    # vaults crossing in a groin: a 3-D force pattern or 3-D blocks
    "church-skaelskor": "groin",
    "fireworks-edmonton": "groin",
    # fibre hung in steel
    "blakebrough-tasmania": "fibre",
}


@pytest.fixture(scope="module")
def results() -> dict[str, KilnStatics]:
    return {p.stem: statics(load_design(p)) for p in sorted(OLSEN.glob("*.yaml"))}


@pytest.mark.slow
@pytest.mark.geometry
def test_every_reference_kiln_v2_models_stands(results: dict[str, KilnStatics]) -> None:
    assert len(results) == 53
    falls = {k: r.stands for k, r in results.items() if r.all_stand is False}
    assert falls == {}, f"a reference kiln can't stand in v2: a model fault to find ({falls})"
    standing = {k for k, r in results.items() if r.all_stand}
    assert len(standing) == 53 - len(NOT_MODELLED)
    for kid, words in NOT_MODELLED.items():
        r = results[kid]
        assert r.all_stand is None
        assert r.missing is not None
        assert words in f"{r.kind}: {r.missing}"
        if all(v is None for v in r.stands.values()):
            assert r.steps[0].name == "Not modelled"
    assert results["tobe"].stands == {"cold": True, "hot": None}


@pytest.mark.slow
@pytest.mark.geometry
def test_what_holds_the_reference_kilns(results: dict[str, KilnStatics]) -> None:
    """The fast-fire's frame must give at least 7.08 lbf/ft a side cold (the probe's 7.080), and
    can be pushed with up to 176 hot under the C16 stand-in; La Borne's 7 ft walls need their
    buttress to give 104.8 lbf/ft cold; singh-coal's dome pushes 78 lbf/ft at its springing."""
    lbft = 4.4482216152605 / 0.3048
    ff = results["fast-fire"].numbers
    assert ff["least on the frame, cold"] / lbft == pytest.approx(7.080, abs=0.01)
    assert ff["most on the frame, hot"] / lbft == pytest.approx(176.0, abs=0.5)
    lb = results["la-borne"].numbers
    assert lb["least on the buttress, cold"] / lbft == pytest.approx(104.8, abs=0.5)
    assert results["singh-coal"].numbers["springing push, cold"] / lbft == pytest.approx(
        78.2, abs=0.5
    )
    assert results["meaders-david"].numbers == {}
    assert results["kenzan-muffle"].kind == "no roof"
    assert results["blakebrough-sturt"].kind == "catenary arch"
    assert len([k for k in results["kannofen"].numbers if k.startswith("least")]) == 8  # 4 stations


@pytest.mark.slow
@pytest.mark.geometry
def test_what_holds_the_rows_ends(results: dict[str, KilnStatics]) -> None:
    """The rows of chambers: Olsen's three-chamber kiln's frame must give about 19 lbf/ft at each
    end cold; tobe's 10 ft arches need about 210 lbf/ft at each end from what holds the row (the
    firebox, the earth, the chimney); Bidai's and Fujiwara's end walls carry their arches alone."""
    lbft = 4.4482216152605 / 0.3048
    three = results["olsen-three-chamber"].numbers
    assert three["least on the frame at the front, cold"] / lbft == pytest.approx(18.9, abs=0.5)
    assert three["least on the frame at the back, cold"] / lbft == pytest.approx(18.6, abs=0.5)
    tobe = results["tobe"].numbers
    assert tobe["least on the buttress at the front, cold"] / lbft == pytest.approx(210.4, abs=1.0)
    for kid in ("bidai", "fujiwara-bizen"):
        n = results[kid].numbers
        assert n["least on the buttress at the front, cold"] == pytest.approx(0.0, abs=1e-6)
    rows = {k for k, r in results.items() if r.kind == "arches along the draft"}
    assert len(rows) == 10


@pytest.mark.slow
@pytest.mark.geometry
def test_what_holds_the_sail_domes(results: dict[str, KilnStatics]) -> None:
    """The domes over square, oblong and curved plans, sliced: the most any strip needs of the
    walls' buttress, hot: Miravet's dense-brick dome about 100 lbf/ft, Calimpong's and
    Hollyweird's flat cast domes 165 and 144 lbf/ft."""
    lbft = 4.4482216152605 / 0.3048
    want = {"miravet": 99.5, "conrad-teardrop": 164.9, "hollyweird": 143.6}
    for kid, hot in want.items():
        r = results[kid]
        assert r.kind == "sail dome"
        assert r.numbers["least on the walls' buttress, hot"] / lbft == pytest.approx(hot, abs=1.0)
