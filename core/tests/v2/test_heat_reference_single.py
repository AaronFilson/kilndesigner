"""Part C3a's tests: the single-chamber wood, coal and oil reference kilns against v2's heat model
(problem set §6; `docs/planning/11-10-26.md` §C, "C3a as built"), each printed figure beside v2's
band (`single_cases.py`: the corner runs over the kiln's setting, its own fuel, the coal bed and λ):

- **T1**, reaches its cone (or its top temperature) at its hardest firing on its own draft, at
  every corner of the band: wood and oil at max fire, coal at its grates' most with the air damped
  to λ 1;
- **T2**, a printed time, not fired flat out: an inequality, v2's hardest firing sooner at every
  corner (problem set §2.2);
- **T3**, a printed fuel against the energy balance: the setting held to a straight rise to the
  target over the printed time, its fuel as fired inside v2's band;
- **T4**, Anderson's printed log (Table 5-2, p.142), as p.309's for the fast-fire: within the
  draft's air;
- **T5**, the evenness's ordering where the zone model can see it: front to back, the chamber cut
  into segments.

The reference kilns all worked as built (the owner, 2026-11-10): where v2 can't fire one to its
documented firing, the test is an open item (`xfail`, strict) traced to the inputs or the missing
physics, with its question in the plan doc. Nothing is fitted. The fast-fire's B4 tests stand as
they were (`test_heat_reference_firings.py`).
"""

from __future__ import annotations

import math

import path_inputs as pi
import pytest
import single_cases as sc

HOUR = 3600.0
pytestmark = [pytest.mark.slow, pytest.mark.geometry]

# --- T1: every single-chamber fuel kiln with a cone or a top temperature, printed or assumed ------

# Printed: the oil drip's cone 10 (p.208), Fireworks' cone 10+ (p.181), Singh's coal kiln's cone 10
# (p.133), Anderson's cone 10 (p.142), Kato's 2372 °F (p.131), Falcone's usual 1760 °F (p.160),
# La Borne's 1300 °C by the firebox (p.111). Assumed, each with its reason in the dataset: the
# rest's cones (10) and the low-fire updrafts' 1760 °F (Falcone's, the only low-fire top printed)
T1 = (
    "anagama-hole", "blakebrough-sturt", "breda-bottle", "chappell-domura", "church-skaelskor",
    "conrad-teardrop", "ellington-new-hog", "falcone-pompeii", "fast-fire-anderson",
    "fireworks-edmonton", "groundhog-basic", "kannofen", "kato-coal", "kenzan-muffle",
    "la-borne", "meaders-cheever", "meaders-david", "miravet", "moveros-umbrella",
    "ninodaguia", "olsen-oil-drip", "phoenix-nh", "phoenix-wright", "singh-coal",
)  # fmt: skip
OPEN_T1 = {
    "singh-lowfire": "open item: the shards and saggar pieces piled over the open top (pp.155–156) "
    "aren't modelled, so the whole top radiates to the room (a third of the heat), and the "
    "1760 °F top is assumed (Falcone's). The owner's answers (2026-11-17, 11-17-26-inputs.md §4), "
    "a top band of 800–1149 °C and the cover a porous shard layer, aren't applied yet",
}


@pytest.mark.parametrize(
    "kid",
    [*T1, *(pytest.param(k, marks=pytest.mark.xfail(strict=True, reason=r))
            for k, r in OPEN_T1.items())],
)  # fmt: skip
def test_t1_reaches_its_target_on_its_own_draft(kid: str) -> None:
    """T1: at every corner of v2's band (the setting's least to most, the fuel's least heat to its
    most, a coal kiln's bed 85–200 kg/(m²·h)) the hardest firing reaches the kiln's target; the
    band's working lists the inputs by their swing. Those with nothing on their path sized run on
    Rule 6's band (the owner's answer of 2026-11-17 not applied yet, `11-17-26-inputs.md` §1),
    said in their path's working; a coal kiln's draft carries its
    grates' most at λ 1."""
    b = sc.max_band(kid)
    print(f"T1 {kid}: {sc.describe(b)}")
    assert math.isfinite(b.high), f"{kid}: not reached at a corner, {sc.describe(b)}"
    assert 0 < b.low <= b.nominal <= b.high
    assert b.steps[0].name.startswith("The band")
    if kid in pi.RULE_6:
        m = sc.model(kid, segments=sc.CASES[kid].segments)
        assert m.path is not None
        assert "Rule 6" in (m.path.steps[0].note or "")
    if sc.coal(kid):  # the draft carries the grates' most at λ 1 (the nominal corner)
        share = sc.max_firing(kid).worst_air_share
        print(f"T1 {kid}: the grates' most at λ 1 needs {share:.2f} of the draft's air")
        assert share <= 1.0


def test_t1_falcone_reaches_its_most_printed_temperature() -> None:
    """Falcone's kiln is usually fired to 1760 °F, at most to 1922 °F (p.160): v2's hardest firing
    reaches the most too, at every corner of its band (on Rule 6's flues)."""
    most = sc.heat_fact("falcone-pompeii", "top_temperature", "K", which=1)[0]
    assert most == pytest.approx(1050.0 + 273.15, abs=0.2)
    b = sc.max_band_to("falcone-pompeii", most)
    print(f"T1 falcone-pompeii to 1922 °F: {sc.describe(b)}")
    assert math.isfinite(b.high), sc.describe(b)


# --- T2: printed firing times, not fired flat out ------------------------------------------------

# (kiln, the printed time's least, h): the hardest firing must be sooner at every corner. Breda's
# "about 10 hours" (p.168); Falcone's "Cycle about 40 hours" (p.160); Anderson's cone 10 down
# everywhere about 10 h after lighting (Table 5-2); Miravet's new kiln, 28–32 h (pp.159–160);
# Moveros' 2 h at the mouth and about 6 more (p.154); Singh's Table 5-1, 19–20 h on Grade B
# (p.133); La Borne's 2½–3 days' preheat, up to 4 of petit feu and about 1 of grand feu (p.111)
T2 = (
    ("breda-bottle", 10.0), ("falcone-pompeii", 40.0), ("fast-fire-anderson", 10.0),
    ("miravet", 28.0), ("moveros-umbrella", 8.0), ("singh-coal", 19.0), ("la-borne", 7.5 * 24),
)  # fmt: skip


def _printed(kid: str, what: str, unit: str = "hour", which: int = 0) -> float:
    return sc.heat_fact(kid, what, unit, which)[0]


@pytest.mark.parametrize(("kid", "hours"), T2)
def test_t2_its_printed_time_is_no_faster_than_its_hardest_firing(kid: str, hours: float) -> None:
    """T2: a stoked kiln's time is the stoker's choice within what its draft and grates burn
    (problem set §2.2): v2's hardest firing reaches the target sooner than the printed time at
    every corner of its band."""
    assert hours in {_printed(kid, "firing_time"), _printed(kid, "firing_time", which=-1)}
    b = sc.max_band(kid)
    assert b.high < hours, sc.describe(b)


def test_t2_the_stage_times_stand() -> None:
    """Stage times (problem set §6), each the printed stage's time against v2's hardest firing from
    cold, so the stage stands from any state the stages before it leave: Moveros' about 6 h
    stoked faster (p.154) and La Borne's grand feu, about a day of branches and twigs for intense
    heat (p.111)."""
    assert sc.max_band("moveros-umbrella").high < _printed("moveros-umbrella", "stage_time",
                                                           which=1)  # fmt: skip
    grand_feu = sc.heat_fact("la-borne", "stage_time", "hour", 1)[0]
    assert grand_feu == pytest.approx(24.0)
    print(f"stages: La Borne's front to 1300 °C {sc.describe(sc.max_band('la-borne'))}")
    assert sc.max_band("la-borne").high < grand_feu


# --- T3: printed fuels against the energy balance ------------------------------------------------


@pytest.mark.xfail(
    strict=True,
    reason="open item: the printed 1,800 kg (the user's reading, 2026-11-17) lies 24 % under v2's "
    "band at cone 2 (2,370 kg to never, the load swinging it most); at the old 1760 °F it was "
    "1.1 % under 1,820 kg. The setting's weight isn't printed, and whether cone 2 (earthenware, "
    "rarely above it) is the top or the band's upper end is the owner's; 11-17-26-inputs.md §5",
)
def test_t3_bredas_two_tons_lie_in_its_band() -> None:
    """T3: "some 2 tons" of chestnut slats for about 10 hours (pp.166–168; 1800 kg as fired, the
    metric figure the user read, 2026-11-17): the setting held to a straight rise to its cone 2
    (assumed, the owner's top) over 10 h takes a fuel inside v2's band (the setting, the wood, λ
    from the stoker's 1 to all the draft's air, the grey gases, the emissivity class, the
    setting's passages)."""
    tons = _printed("breda-bottle", "fuel_per_firing", "kg")
    b = sc.kiln_bands("breda-bottle")[sc.FUEL]
    print(f"T3 breda-bottle, {tons:.0f} kg printed: {sc.describe(b)}; {b.swings}")
    assert b.low <= tons <= b.high, sc.describe(b)


def test_t3_falcones_fifteen_tons_lie_in_its_band() -> None:
    """T3: 15 short tons (13.6 t) of long slats a cycle of about 40 hours (p.160), with its printed
    18 t of bricks and tiles: the setting held to a straight rise to 1760 °F over 40 h (whether the
    cycle counts the cooling isn't said: the 40 h the firing's most) on Rule 6's flues."""
    tons = _printed("falcone-pompeii", "fuel_per_firing", "kg")
    b = sc.kiln_bands("falcone-pompeii")[sc.FUEL]
    print(f"T3 falcone-pompeii, {tons:.0f} kg printed: {sc.describe(b)}; {b.swings}")
    assert b.low <= tons <= b.high, sc.describe(b)


def test_t3_singhs_coal_lies_in_its_band() -> None:
    """T3: Table 5-1's 82 shovels a firebox, four fireboxes (p.133, derived), at the shovel's band
    (4–21 lb, Taylor's: `single_cases.SHOVEL_LB`, the owner's question A3) against the coal a
    straight rise to cone 10 in 19½ h takes (the setting, the coal, the bed, λ): the two bands
    meet, and the hour-19 rate (five shovels every 50 min a firebox) meets v2's last rate."""
    count = sc.heat_fact("singh-coal", "fuel_per_firing", None)[0] * 4
    lo, hi = sc.shovels_kg(count)
    b = sc.kiln_bands("singh-coal")[sc.FUEL]
    rate_lo, rate_hi = sc.shovels_kg(4 * 5 * 60 / 50)
    r = sc.kiln_bands("singh-coal")[sc.RATE]
    print(f"T3 singh-coal, {lo:.0f}–{hi:.0f} kg printed: {sc.describe(b)}; {b.swings}")
    print(f"T3 singh-coal hour 19, {rate_lo:.0f}–{rate_hi:.0f} kg/h printed: {sc.describe(r)}")
    print(f"T3 singh-coal: {sc.describe(sc.kiln_bands('singh-coal')[sc.AIR])} of the draft's air")
    assert lo <= b.high
    assert b.low <= hi, sc.describe(b)
    assert rate_lo <= r.high
    assert r.low <= rate_hi, sc.describe(r)


def test_t3_the_oil_drips_gallons_are_no_less_than_its_hardest_firing() -> None:
    """T3: 60–75 gal of #2 diesel to cone 10 (p.208; no time printed): no firing takes less fuel
    than the fastest, so v2's max fire's oil (at its sg 0.85, p.209) is under the printed most at
    every corner."""
    gallons = sc.heat_fact("olsen-oil-drip", "fuel_per_firing", "gallon")
    b = sc.kiln_bands("olsen-oil-drip")[sc.MAX_FUEL]
    print(f"T3 olsen-oil-drip, {gallons[1] * sc.DIESEL_KG_PER_GAL:.0f} kg most: {sc.describe(b)}")
    assert b.high < gallons[1] * sc.DIESEL_KG_PER_GAL, sc.describe(b)


def test_katos_printed_rates_against_its_draft_and_grates() -> None:
    """Kato's coal above 2000 °F (p.131): 3–4 shovels every 20 minutes in oxidation, 10–12 in very
    heavy reduction, over the shovel's band (4–21 lb): at its 2372 °F the draft's air burns the
    oxidation rate at λ ≥ 1 for some shovel, the reduction rate overruns the air (λ < 1) for some
    shovel, and the grates' most (200 kg/(m²·h)) takes the reduction rate for some shovel."""
    burns = sc.burnt_at_top(sc.KATO)
    ox, red = sc.kato_rate("oxidation"), sc.kato_rate("reduction")
    print(
        f"kato-coal: the draft burns {burns:.0f} kg/h at λ 1 at 1300 °C; oxidation "
        f"{ox[0]:.0f}–{ox[1]:.0f}, reduction {red[0]:.0f}–{red[1]:.0f}, the grates' most "
        f"{sc.grates_most(sc.KATO):.0f} kg/h as fired"
    )
    assert ox[0] <= burns
    assert red[1] > burns
    assert red[0] <= sc.grates_most(sc.KATO)


# --- T4: Anderson's printed log ------------------------------------------------------------------


def test_t4_andersons_table_5_2_within_its_drafts_air() -> None:
    """T4: Table 5-2's first firing at 8,600 ft (p.142, p.82), its printed points held by the
    setting from 2.30 pm to 1820 °F at 9.30 pm (its cones, 250–300 °C hotter soon after, are T2's):
    within the draft's air (damper open; its printed ¼–¾ openings aren't modelled, B4–B6 question
    2) at some corner of the band (B4's inputs for a log), as it was fired; and the front firebox's
    5 h stage on half the intakes, one firebox's of two."""
    b = sc.log_bands()
    for name, band in b.items():
        print(f"T4 fast-fire-anderson, {name}: {sc.describe(band)}; {band.swings}")
    assert b[sc.LOG_AIR].low <= 1.0, sc.describe(b[sc.LOG_AIR])
    assert b[sc.LOG_AIR_MOST].low <= 1.0
    assert b[sc.STAGE_AIR].low <= 1.0, sc.describe(b[sc.STAGE_AIR])


# --- T5: evenness front to back -------------------------------------------------------------------


def test_t5_la_bornes_tunnel_falls_front_to_back() -> None:
    """T5: the temperature falls along the tunnel, so the ware is graded high-fire, middle-fire and
    earthenware by thirds, about 1300 °C by the firebox, 1200 °C in the middle, about 1100 °C at
    the rear (p.111): the tunnel in three segments, the front's setting at 1300 °C, the middle's and
    the rear's colder in that order (the ordering; the book's own figures beside in the plan)."""
    f = sc.evenness("la-borne", 3)
    front, middle, rear = f.t_settings[-1]
    print(
        f"T5 la-borne at {f.times[-1] / HOUR:.2f} h: settings {front - 273.15:.0f}, "
        f"{middle - 273.15:.0f}, {rear - 273.15:.0f} °C; gas "
        f"{[round(float(x) - 273.15) for x in f.t_gases[-1]]} °C"
    )
    assert f.reached(sc.target("la-borne"), 0) is not None
    assert front > middle > rear


def test_t5_the_groundhogs_back_fires_cooler() -> None:
    """T5: a groundhog runs hot along the crown and cool along the bottom of the back wall (p.75,
    Fig 3-6): its chamber in two segments, the back's setting cooler than the front's when the
    front's reaches cone 10 (top to bottom needs zones stacked up the chamber: not built)."""
    f = sc.evenness("groundhog-basic", 2)
    print(
        f"T5 groundhog-basic at {f.times[-1] / HOUR:.2f} h: settings "
        f"{[round(float(x) - 273.15) for x in f.t_settings[-1]]} °C, gas "
        f"{[round(float(x) - 273.15) for x in f.t_gases[-1]]} °C"
    )
    assert f.reached(sc.target("groundhog-basic"), 0) is not None
    assert f.t_settings[-1, 1] < f.t_settings[-1, 0] - 10.0
