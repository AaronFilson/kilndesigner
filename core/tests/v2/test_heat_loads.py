"""Each reference kiln's setting as a sourced band (`loads.py`; `docs/research/kiln-settings.md`):
the dataset's mass bands are the method's, the envelopes the book's clearances and lie in their
chambers, and the survey's test loads fall inside their kilns' bands."""

from __future__ import annotations

import heat_cases as hc
import loads
import pytest
import reference as ref

IN = 0.0254
KILNS = sorted(ref.load()["kilns"])
# Kilns that take each part of the method: printed plans and ware, a round chamber, a crossing, an
# arch from the floor, domes over chambers in a row, an open top, an arch along the run, the kits
QUICK = (
    "fast-fire", "kahler-salt", "blakebrough-tasmania", "olsen-kit-24", "olsen-kit-16",
    "updraft-test-1", "singh-coal", "kenzan-muffle", "fireworks-edmonton", "groundhog-basic",
    "hollyweird", "falcone-pompeii", "bowen-mountain", "electric-car-45", "olsen-crossdraft-36",
)  # fmt: skip


def test_every_kiln_has_its_setting_band() -> None:
    """Every reference kiln has its setting's mass as a band, one per chamber zone (ADR 0017
    decision 11: no heat result without a load)."""
    for kid in KILNS:
        bands = loads.dataset_bands(kid)
        assert bands, kid
        assert all(0 < lo < hi for lo, hi in bands), kid


def test_the_sources_numbers() -> None:
    """Olsen's 12 × 24 in shelves (pp.33–35) as kg per m²; Skutt's kit's four layers in 27 in."""
    assert loads.kg_per_m2(8.0) == pytest.approx(19.53, abs=0.01)
    assert loads.kg_per_m2(22.0) == pytest.approx(53.71, abs=0.01)
    assert pytest.approx(27 * IN / 4) == loads.LAYER_PITCH
    assert loads.WARE_DENSITY == (60.0, 260.0)
    assert loads.EMISSIVITY[0] < loads.EMISSIVITY_NOMINAL < loads.EMISSIVITY[1]


@pytest.mark.geometry
@pytest.mark.parametrize("kid", QUICK)
def test_the_bands_are_the_methods_and_the_settings_fit(kid: str) -> None:
    """The dataset's bands are the method's to the kilogram; each envelope lies in its chamber's
    gas (`Chamber.holds`) and is a box with height."""
    s = loads.setting(kid)
    assert len(s.masses) == len(s.dataset) == len(s.envelopes)
    for m, (lo, hi) in zip(s.masses, s.dataset, strict=True):
        assert lo == pytest.approx(m.low, abs=0.6)
        assert hi == pytest.approx(m.high, abs=0.6)
    c = loads.traced(kid)
    for e in s.envelopes:
        assert e.height >= loads.MIN_HEIGHT
        assert c.holds(e.lo, e.hi)


@pytest.mark.geometry
def test_the_envelopes_the_book_gives() -> None:
    """The kits' stackings (kit-stacking-space.md §2), the updraft tests' printed 2 × 3 ft (p.74),
    Kähler's printed 24 × 24 in to the arch line (p.136), the fast-fire's printed plan on its bag
    walls (p.142) up to its arch less 4½ in, near the survey's 33 in; a round chamber's square
    12 in inside its wall (Singh's printed clearance, p.135)."""

    def size(kid: str) -> tuple[float, ...]:
        e = loads.setting(kid).envelopes[0]
        return (*((h - lo) / IN for lo, h in zip(e.lo, e.hi, strict=True)), e.lo[2] / IN)

    assert size("olsen-kit-24") == pytest.approx((34.6, 34.6, 34.6, 2.5), abs=0.05)
    assert size("olsen-kit-16") == pytest.approx((25.9, 25.9, 41.2, 2.5), abs=0.05)
    assert size("updraft-test-1") == pytest.approx((24.0, 36.0, 57.5, 2.5), abs=0.05)
    assert size("kahler-salt") == pytest.approx((24.0, 24.0, 45.5, 2.5), abs=0.05)
    ff = size("fast-fire")
    assert ff[:2] == pytest.approx((18.0, 21.5))
    assert ff[3] == pytest.approx(9.0)
    assert 9.0 + ff[2] == pytest.approx(33.0, abs=1.0)
    singh = loads.setting("singh-coal").envelopes[0]
    c = loads.traced("singh-coal")
    half_diagonal = (singh.hi[0] ** 2 + singh.hi[1] ** 2) ** 0.5
    assert half_diagonal <= c.width / 2 - 12 * IN + 1e-3
    assert "open top" in loads.setting("kenzan-muffle").envelopes[0].how


@pytest.mark.geometry
def test_the_survey_loads_lie_in_their_bands() -> None:
    """The fast-fire's survey load, 55 kg (`heat_cases.FAST_FIRE_LOAD`, its tests' input, kept),
    lies inside its band, 40–159 kg, near its light end; the cross-draft's 150 kg inside its."""
    lo, hi = loads.dataset_bands("fast-fire")[0]
    assert lo < hc.FAST_FIRE_LOAD.mass < hi
    assert (hc.FAST_FIRE_LOAD.mass - lo) / (hi - lo) == pytest.approx(0.13, abs=0.01)
    lo, hi = loads.dataset_bands("olsen-crossdraft-36")[0]
    assert lo < hc.CROSSDRAFT_LOAD.mass < hi


@pytest.mark.geometry
def test_loads_at_the_bands_ends() -> None:
    """The heat model's loads at the band's least, middle and most; a tube cut into segments
    shares its band by the segments' volumes; the wider combustion space (6 in, p.171) gives a
    smaller envelope."""
    least, mid, most = (loads.loads("olsen-kit-24", e)[0] for e in ("least", "mid", "most"))
    assert least.mass < mid.mass < most.mass
    assert (least.mass, most.mass) == pytest.approx(loads.dataset_bands("olsen-kit-24")[0])
    assert mid.emissivity == loads.EMISSIVITY_NOMINAL
    assert "kiln-settings.md" in mid.reference
    parts = loads.loads("anagama-hole", "most", segments=4)
    assert len(parts) == 4
    assert sum(x.mass for x in parts) == pytest.approx(loads.dataset_bands("anagama-hole")[0][1])
    narrow = loads.loads("olsen-kit-24", wide=False)[0]
    assert narrow.hi[0] - narrow.lo[0] == pytest.approx(mid.hi[0] - mid.lo[0] - 3 * IN)


@pytest.mark.slow
@pytest.mark.geometry
def test_every_kilns_bands_are_the_methods() -> None:
    """All 53 kilns: each chamber zone's band is the method's, each envelope in its chamber."""
    for kid in KILNS:
        s = loads.setting(kid)
        assert len(s.masses) == len(s.dataset), kid
        for m, (lo, hi) in zip(s.masses, s.dataset, strict=True):
            assert (lo, hi) == pytest.approx((m.low, m.high), abs=0.6), kid
        c = loads.traced(kid)
        assert all(c.holds(e.lo, e.hi) for e in s.envelopes), kid
