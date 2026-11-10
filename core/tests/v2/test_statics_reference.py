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
    # a row of chambers: the section along the kiln isn't cut yet
    "bidai": "along the draft",
    "bowen-mountain": "along the draft",
    "fujiwara-bizen": "along the draft",
    "hotchkiss-raw-clay": "along the draft",
    "kawaii": "along the draft",
    "kyoto-climbing": "along the draft",
    "olsen-three-chamber": "along the draft",
    "olsen-two-chamber": "along the draft",
    "suzuki-kyoto": "along the draft",
    "tobe": "along the draft",
    # vaults crossing in a groin: a 3-D force pattern or 3-D blocks
    "church-skaelskor": "groin",
    "fireworks-edmonton": "groin",
    # domes over square or curved plans
    "conrad-teardrop": "sail dome",
    "hollyweird": "sail dome",
    "miravet": "sail dome",
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
        assert r.steps[0].name == "Not modelled"


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
