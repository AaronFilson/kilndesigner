"""Part C3a's single-chamber wood, coal and oil kilns as heat-model runs (`11-10-26.md` §C, "C3a
as built"): each kiln's own fuel at its bands' ends (`fuel.py`, research A1), its setting
band (C2's `loads.py`), its own draft path (C1's `path_inputs.py`; the six with nothing on their
path sized on Olsen's Rule 6, the owner's question 8, open), the fireboxes and the chimney as gas
zones of their own (B2; several fireboxes each burning its share, C3a), and v2's band over the
inputs no source fixes (`bands.py`'s corner runs).

**The inputs**, each a stated band where no source gives one:
- the load: the setting's band, least to most (`kiln-settings.md`, the dataset's `setting` facts);
- the fuel: the kiln's own, its moisture and heating value at the least-heat end and the most
  (`kiln-fuels.md` §5);
- λ, for the fuel a printed firing takes: the stoker's at 1 (the least fuel) to all the air the
  draft draws through the open intakes (decision 9, B4 step 4);
- the coal bed, for the coal kilns: 85–200 kg/(m²·h) as fired (`grates-and-fuel-beds.md`: Norsker,
  Gebhardt's Table 29), the most the grates burn;
- for a printed fuel or log (the energy balance), the rest B4 carried for the fast-fire's log: the
  emissivity class, the grey gases and the setting's passages. A time's band leaves them at their
  nominal, as C2's did: on the fast-fire they swung its max fire less than the load and the wood
  (B4 step 5).

The draft is drawn at its band's least-air end (rough brick, each fitting's higher coefficient),
the slow side for a max fire. Each kiln is traced once for each end of its fuel, grey-gas set and
emissivity class it takes (2·10⁴ rays a zone: the fast-fire's nominal agreed with 10⁵ to 0.1 %,
B4) and the corners reuse the traces.

A stoked kiln's printed time is the stoker's choice within what its draft lets it burn (problem
set §2.2): v2's max fire must be sooner. A printed fuel against v2's is the energy balance (T3):
the setting held to a straight rise from the room to the kiln's target over the printed time, the
fuel it takes as fired (dry ÷ (1 − w)). Nothing is fitted.
"""

from __future__ import annotations

import math
from collections.abc import Hashable, Mapping
from dataclasses import dataclass, replace
from functools import cache

import fuel as own
import gas_cases
import heat_cases as hc
import loads
import path_inputs as pi

from kilndesigner.units import Q_, si
from kilndesigner.v2.heat import air as air_mod
from kilndesigner.v2.heat import bands
from kilndesigner.v2.heat import chamber as ch
from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat.zone import ZoneModel

HOUR = 3600.0
BAND_RAYS = 20_000
LB = si(Q_(1, "lb"), "kg")
# A shovelful of coal (kiln-fuels.md [F8], Taylor 1911): shovels issued to "hold a load of 21
# pounds of whatever class of material"; one man's own shovel took "about 30 pounds" of ore and
# "less than 4 pounds" of rice coal: a coal shovelful 4–21 lb, a stated band (the owner's question
# A3: neither kiln's shovel is described)
SHOVEL_LB = (4.0, 21.0)
# #2 diesel's specific gravity, 0.85 (Olsen p.209), a US gallon 3.785 L
DIESEL_KG_PER_GAL = 0.85 * 3.785411784

MAX = "max fire to its target (h)"
FUEL = "the printed firing's fuel (kg as fired)"
AIR = "the printed firing's air over the draft's most"

LOAD = bands.Input(
    "the load",
    ("least", "most"),
    "mid",
    "kiln-settings.md: the kiln's setting band (the dataset's `setting` facts)",
)
FUEL_IN = bands.Input("the fuel", ("least", "most"), "mid",
                      "kiln-fuels.md §5: the kiln's own fuel, its moisture and net heating value "
                      "at the least-heat end and the most")  # fmt: skip
LAMBDA = bands.Input("λ", ("stoker", "draft"), "stoker",
                     "decision 9: the stoker's air at λ 1 to all the draft's air (the intakes "
                     "open)")  # fmt: skip
BED = bands.Input("the coal bed", air_mod.COAL_BED, sum(air_mod.COAL_BED) / 2,
                  air_mod.COAL_BED_REFERENCE)  # fmt: skip


@dataclass(frozen=True)
class Case:
    """How a kiln is run: how long its hardest firing may go (h), the segments its chamber is cut
    into (front to back, the front's setting the one that reaches the target), the fast-fire's
    clay flue liners for its chimney (Fig 5-37), the printed firing a fuel figure belongs to
    (hours, the setting held to a straight rise), and the record's sampling (s)."""

    kid: str
    hours: float = 48.0
    segments: int = 1
    liner: bool = False
    firing: float | None = None
    sample: float = 600.0


CASES: dict[str, Case] = {c.kid: c for c in (
    Case("breda-bottle", 24.0, firing=10.0, sample=1800.0),
    Case("falcone-pompeii", 120.0, firing=40.0, sample=1800.0),
    Case("fast-fire-anderson", 12.0, liner=True),
    Case("miravet", 72.0),
    Case("moveros-umbrella", 24.0),
    Case("singh-lowfire", 24.0),
    Case("groundhog-basic", 48.0),
    Case("kannofen", 72.0),
    # its target, about 1300 °C, is the front's, by the firebox (p.111): the tunnel in thirds
    Case("la-borne", 10 * 24.0, segments=3, sample=1800.0),
    Case("kato-coal", 120.0, sample=1800.0),
    Case("singh-coal", 48.0, firing=19.5, sample=1800.0),
    Case("olsen-oil-drip", 24.0),
    Case("fireworks-edmonton", 48.0),
    Case("anagama-hole", 72.0),
    Case("blakebrough-sturt", 48.0),
    Case("chappell-domura", 48.0),
    Case("church-skaelskor", 48.0),
    Case("conrad-teardrop", 48.0),
    Case("ellington-new-hog", 48.0),
    Case("kenzan-muffle", 24.0),
    Case("meaders-cheever", 48.0),
    Case("meaders-david", 48.0),
    Case("ninodaguia", 48.0),
    Case("phoenix-nh", 24.0),
    Case("phoenix-wright", 24.0),
)}  # fmt: skip


def coal(kid: str) -> bool:
    return loads.design(kid).heat.fire.fuel == "coal"  # pyright: ignore[reportOptionalMemberAccess]


def target(kid: str) -> float:
    """The kiln's target (K): its design's cone at its final rate, or its top temperature."""
    return gas_cases.cone(kid)


def grate_area(kid: str) -> float:
    """The grates' whole area (m²), as `kiln._bed` takes it."""
    fire = loads.design(kid).heat.fire
    assert fire is not None
    return sum(si(b.grate.width, "m") * si(b.grate.length, "m") * b.count
               for b in fire.fireboxes if b.grate is not None)  # fmt: skip


@cache
def cavity(kid: str, segments: int = 1) -> ch.Chamber:
    """The kiln's solid with its fireboxes and chimney as zones, built once for all its models."""
    return ch.chamber(loads.design(kid), segments=segments, path=True)


@cache
def model(
    kid: str,
    end: own.End = "mid",
    segments: int = 1,
    wsgg: str = "bordbar2014",
    emissivity: str = "nominal",
) -> ZoneModel:
    """The kiln's whole gas path, its fuel at its bands' ``end``, traced once for each grey-gas
    set and emissivity class (its load at its band's middle: the corners set each mass)."""
    c = CASES[kid]
    k = loads.design(kid)
    inputs = pi.inputs(kid, rule6=kid in pi.RULE_6)
    bed = BED.nominal if coal(kid) else None
    return hk.heat_model(
        k, loads.loads(kid, "mid", segments), 1.0, own.own_fuels(kid, end)[0], n_rays=BAND_RAYS,
        path=True, segments=segments, path_inputs=inputs, bed_rate=bed, wsgg=wsgg,  # pyright: ignore[reportArgumentType]
        emissivity=emissivity, chimney=hk.flue_liner() if c.liner else None,  # pyright: ignore[reportArgumentType]
        cavity=cavity(kid, segments),
    )  # fmt: skip


# The inputs B4 carried for the fast-fire's log (`heat_cases.FAST_FIRE_INPUTS`), carried here too
# where a printed fuel or log is the result: on the fast-fire they swung its max fire less than the
# load and the wood, so a time's band leaves them at their nominal (as C2's did)
_B4 = {i.name: i for i in hc.FAST_FIRE_INPUTS}
WSGG, EMISSIVITY, GAP = (_B4[n] for n in ("grey gases", "emissivity class",
                                          "the setting's passages"))  # fmt: skip
# Each corner's model is set by these (λ by the firing's mode)
KEYS = ("the load", "the fuel", "the coal bed", "grey gases", "emissivity class",
        "the setting's passages")  # fmt: skip


def inputs(kid: str, fuel_results: bool = False) -> tuple[bands.Input, ...]:
    """A kiln's uncertain inputs: the load and its fuel (the fuel's ends only where they differ),
    the coal bed for a coal kiln; where a fuel is the result, λ, the grey gases (where Dorigon's
    set takes the products, `two_wsgg`), the emissivity class and the setting's passages too."""
    out = [LOAD]
    least, most = (own.own_fuels(kid, e)[0] for e in ("least", "most"))
    if (least.moisture, least.net_dry) != (most.moisture, most.net_dry):
        out.append(FUEL_IN)
    if coal(kid):
        out.append(BED)
    if fuel_results:
        out += [LAMBDA, *((WSGG,) if two_wsgg(kid) else ()), EMISSIVITY, GAP]
    return tuple(out)


@cache
def two_wsgg(kid: str) -> bool:
    """Whether both grey-gas sets take the kiln's products: Dorigon 2013 is fitted at H₂O/CO₂
    ratios of 1 and 2 only and refuses others (`gasrad.dorigon2013`): a coal's products run near
    0.4, so a coal kiln's band takes Bordbar 2014's alone (fitted over 0.01–4), said."""
    from kilndesigner.v2.heat import gas, gasrad

    p = gas.products(own.own_fuels(kid, "mid")[0], 1.0, si(loads.design(kid).site.ambient, "K"))
    try:
        gasrad.dorigon2013(p.radiating(hk.NOMINAL)[1])
    except gasrad.RangeError:
        return False
    return True


def corner(kid: str, s: Mapping[str, Hashable]) -> tuple[Hashable, ...]:
    """A corner's model key (`KEYS`), each input it doesn't set at its nominal."""
    nominal = {"the load": "mid", "the fuel": "mid", "the coal bed": BED.nominal if coal(kid)
               else None, "grey gases": WSGG.nominal, "emissivity class": EMISSIVITY.nominal,
               "the setting's passages": GAP.nominal}  # fmt: skip
    return tuple(s.get(n, nominal[n]) for n in KEYS)


def variant(kid: str, s: Mapping[str, Hashable], segments: int = 1) -> ZoneModel:
    """A corner's model: the trace for its fuel's end, grey gases and emissivity class, each
    setting's mass at its load's end and its passages', the coal bed's most at its rate."""
    load, end, rate, wsgg, emissivity, gap = corner(kid, s)
    m = model(kid, str(end), segments, str(wsgg), str(emissivity))  # pyright: ignore[reportArgumentType]
    masses = [x.mass for x in loads.loads(kid, load, segments)]  # pyright: ignore[reportArgumentType]
    m = replace(m, settings=tuple(replace(x, mass=w, gap=float(gap)) for x, w in  # pyright: ignore[reportArgumentType]
                                  zip(m.settings, masses, strict=True)))  # fmt: skip
    if rate is not None:
        m = replace(m, bed=air_mod.bed_most(m.products.fuel, grate_area(kid), float(rate)))  # pyright: ignore[reportArgumentType]
    return m


def hardest(m: ZoneModel) -> fi.Mode:
    """A kiln's hardest firing: wood or oil at max fire, all the air its draft draws burning the
    fuel at λ 1; coal at its grates' most (`air.COAL_BED`) with the air damped to λ 1, as the
    stoker does with the damper and the ash-pit doors (B4–B6 question 2: the damper isn't
    modelled, so the stoker's λ is taken), the draft checked to carry it (the air share)."""
    if m.products.fuel.kind == "coal":
        assert m.bed is not None
        return fi.FixedInput(m.bed)
    return fi.MaxFire()


@cache
def _maxfire(
    kid: str, key: tuple[Hashable, ...], segments: int = 1, to: float | None = None
) -> fi.Firing:
    m = variant(kid, dict(zip(KEYS, key, strict=True)), segments)
    c = CASES[kid]
    top = target(kid) if to is None else to
    return fi.fire(m, hardest(m), c.hours * HOUR, (), (0, top), sample=c.sample)


def max_fire(kid: str, s: Mapping[str, Hashable], to: float | None = None) -> float | None:
    """Hours to the kiln's target (or ``to``, K) at its hardest firing at a corner (None: not in
    the case's hours), its chamber in the case's segments (the front's setting the one that
    reaches it); λ doesn't touch it."""
    f = _maxfire(kid, corner(kid, s), CASES[kid].segments, to)
    hit = f.reached(target(kid) if to is None else to)
    return None if hit is None else hit / HOUR


@cache
def max_band_to(kid: str, to: float) -> bands.Band:
    """v2's band for the hours to another printed temperature (K) at the hardest firing."""
    return bands.corner_runs(lambda s: {MAX: max_fire(kid, s, to)}, inputs(kid))[MAX]


def as_fired(m: ZoneModel, dry: float) -> float:
    return dry / (1.0 - m.products.fuel.moisture)


@cache
def _held(
    kid: str, key: tuple[Hashable, ...], lam: str
) -> tuple[float | None, float | None, float | None]:
    """The printed firing at a corner: its fuel as fired (kg), its air over the draft's most and
    its last fuel rate (kg/h as fired); Nones where the corner can't follow it (no consistent
    state, the gas past its tables, or IDA's budget spent)."""
    m = variant(kid, dict(zip(KEYS, key, strict=True)))
    c = CASES[kid]
    assert c.firing is not None
    points = ((0.0, m.t_room), (c.firing * HOUR, target(kid)))
    mode = fi.Schedule("setting", points, air=lam)  # pyright: ignore[reportArgumentType]
    try:
        f = fi.fire(m, mode, c.firing * HOUR, sample=c.sample, max_steps=5_000)
    except fi.FiringError:
        return None, None, None
    if not f.completed:  # IDA's budget spent: the corner can't follow it
        return None, None, None
    return as_fired(m, f.fuel_kg), f.worst_air_share, as_fired(m, float(f.fuel_rate[-1])) * HOUR


MAX_FUEL = "the hardest firing's fuel (kg as fired)"
RATE = "the printed firing's last fuel rate (kg/h as fired)"
FUEL_AT_MAX = frozenset({"olsen-oil-drip"})  # a printed fuel with no time: against the least


def run(kid: str, s: Mapping[str, Hashable]) -> dict[str, float | None]:
    """One band run: the hardest firing's time (and its fuel, where the book prints a fuel and no
    time), and where a printed firing has a fuel figure, its fuel, its air and its last rate."""
    out: dict[str, float | None] = {MAX: max_fire(kid, s)}
    if kid in FUEL_AT_MAX:
        f = _maxfire(kid, corner(kid, s), CASES[kid].segments)
        out[MAX_FUEL] = as_fired(variant(kid, s), f.fuel_kg)
    if CASES[kid].firing is not None and "λ" in s:
        fuel, air, rate = _held(kid, corner(kid, s), str(s["λ"]))
        out |= {FUEL: fuel, AIR: air} | ({RATE: rate} if coal(kid) else {})
    return out


@cache
def kiln_bands(kid: str) -> dict[str, bands.Band]:
    """v2's bands for a kiln's results over its inputs (corner runs)."""
    fuel_results = CASES[kid].firing is not None
    return bands.corner_runs(lambda s: run(kid, s), inputs(kid, fuel_results))


def max_band(kid: str) -> bands.Band:
    return kiln_bands(kid)[MAX]


def describe(b: bands.Band) -> str:
    """A band as the results table gives it: low–high (nominal), the input swinging it most."""
    swing = sorted(b.swings, key=lambda x: -abs(x[2] - x[1]) if math.isfinite(x[2] - x[1])
                   else -math.inf)  # fmt: skip
    return f"{b.low:.3g}–{b.high:.3g} ({b.nominal:.3g}); swung most by {swing[0][0]}"


def shovels_kg(count: float) -> tuple[float, float]:
    """A count of coal shovelfuls as kg, over the shovel's band (`SHOVEL_LB`)."""
    return count * SHOVEL_LB[0] * LB, count * SHOVEL_LB[1] * LB


# Kato's coal above 2000 °F (p.131; the dataset's `fuel_rate` facts, printed): 10 to 12 shovels of
# coal every 20 minutes in reduction, 3 to 4 in oxidation, the kiln's two fireboxes together
KATO = "kato-coal"
KATO_SHOVELS_PER_20_MIN = {"reduction": (10.0, 12.0), "oxidation": (3.0, 4.0)}


def kato_rate(atmosphere: str) -> tuple[float, float]:
    """Kato's printed coal rate (kg/h as fired) over the shovel's band: its fewest shovels at the
    lightest shovel to its most at the heaviest."""
    lo, hi = KATO_SHOVELS_PER_20_MIN[atmosphere]
    return shovels_kg(3 * lo)[0], shovels_kg(3 * hi)[1]


def burnt_at_top(kid: str) -> float:
    """The most coal (kg/h as fired) the draft's air burns at λ 1 at the nominal hardest firing's
    end, the kiln at its target."""
    m = variant(kid, nominal(kid))
    return as_fired(m, drawn_at_top(kid) / m.products.air) * HOUR


def grates_most(kid: str) -> float:
    """The most coal (kg/h as fired) the grates burn, at the bed's top rate (`air.COAL_BED`)."""
    return air_mod.COAL_BED[1] * grate_area(kid) * HOUR


def heat_fact(kid: str, what: str, unit: str | None, which: int = 0) -> tuple[float, float]:
    """A kiln's numeric heat fact (`what`) from the dataset, (low, high) in ``unit`` (None: as
    printed, a count's)."""
    import reference as ref

    fs = [f for f in ref.facts(loads._kilns()[kid], "heat", what) if ref.numeric(f)]  # pyright: ignore[reportPrivateUsage]
    return ref.raw(fs[which]) if unit is None else ref.span(fs[which], unit)


# --- Anderson's printed log (T4) ------------------------------------------------------------------

ANDERSON = "fast-fire-anderson"
LOG_AIR, LOG_AIR_MOST, LOG_WOOD = (
    "Table 5-2's air over the draft's most", "the same at the draft's most-air end",
    "Table 5-2's wood (kg as fired)",
)  # fmt: skip
STAGE_AIR = "the front firebox's stage: air over the draft's most, one firebox's intakes"


def anderson_log() -> tuple[tuple[float, float], ...]:
    """Table 5-2's first firing (p.142) as the setting's schedule (s, K): its printed points from
    the fire lit at 2.30 pm to 1820 °F at 9.30 pm, as printed. Its cones aren't joined to it:
    cone 8 was down at the bottom at 10 pm and cone 10 soft at 10.30 pm, 250–300 °C over the
    pyrometer's last reading half an hour to an hour before, so the pyrometer read a cooler place
    than the cones or lagged them (the book doesn't say where it was); the cones' 10 h is T2's."""
    return schedule(ANDERSON)


@cache
def _log(key: tuple[Hashable, ...], lam: str, stage: bool = False) -> fi.Firing | None:
    """Table 5-2 held by the setting at a corner (None where the corner can't follow it); with
    ``stage``, its first part alone (the front firebox's, to the back's start) against the draft
    through half the intakes, one firebox's of the two."""
    m = variant(ANDERSON, dict(zip(KEYS, key, strict=True)))
    log = anderson_log()
    end = log[-1][0]
    if stage:
        assert m.path is not None
        end = heat_fact(ANDERSON, "stage_time", "hour")[0] * HOUR
        m = replace(m, path=m.path.opened(0.5))
    mode = fi.Schedule("setting", log, air=lam)  # pyright: ignore[reportArgumentType]
    try:
        f = fi.fire(m, mode, end, sample=300.0, max_steps=5_000)
    except fi.FiringError:
        return None
    return f if f.completed else None


def log_run(s: Mapping[str, Hashable]) -> dict[str, float | None]:
    """One band run of Table 5-2: its air over the draft's most at both ends of the draft's band,
    its wood as fired, and the front firebox's stage's air."""
    key, lam = corner(ANDERSON, s), str(s["λ"])
    f, st = _log(key, lam), _log(key, lam, stage=True)
    m = variant(ANDERSON, s)
    out: dict[str, float | None] = {LOG_AIR: None, LOG_AIR_MOST: None, LOG_WOOD: None}
    if f is not None:
        out = {LOG_AIR: f.worst_air_share, LOG_AIR_MOST: f.worst_air_share_smooth,
               LOG_WOOD: as_fired(m, f.fuel_kg)}  # fmt: skip
    return out | {STAGE_AIR: st.worst_air_share if st is not None else None}


@cache
def log_bands() -> dict[str, bands.Band]:
    """Table 5-2's bands over B4's inputs for a log (the fast-fire's p.309)."""
    return bands.corner_runs(log_run, inputs(ANDERSON, fuel_results=True))


def nominal(kid: str) -> dict[str, Hashable]:
    """The nominal corner: every input at its middle (`corner`'s defaults)."""
    return dict(zip(KEYS, corner(kid, {}), strict=True))


def evenness(kid: str, segments: int) -> fi.Firing:
    """T5: the kiln cut into ``segments`` gas zones front to back (`chamber.py`), each its share
    of the setting, at its hardest firing at the nominal corner until the front's setting reaches
    the target."""
    return _maxfire(kid, corner(kid, {}), segments)


def max_firing(kid: str) -> fi.Firing:
    """The nominal hardest firing's whole record (its fuel, its air, its state at the target)."""
    return _maxfire(kid, corner(kid, {}), CASES[kid].segments)


def drawn_at_top(kid: str) -> float:
    """The most air (kg/s) the draft draws at the nominal hardest firing's end, at the target:
    the fuel's air over the share of the draft's most it needs (`firing.Firing.air_share`)."""
    f = max_firing(kid)
    p = variant(kid, nominal(kid)).products
    return float(f.fuel_rate[-1] * p.air / f.air_share[-1])


def schedule(kid: str, which: int = 0) -> tuple[tuple[float, float], ...]:
    """A kiln's printed schedule from the dataset (`heat.schedule`: ['H:MM', temperature] from its
    `start`), as (s, K) from the start at the room's temperature."""
    import reference as ref

    f = ref.facts(loads._kilns()[kid], "heat", "schedule")[which]  # pyright: ignore[reportPrivateUsage]

    def hours(clock: str) -> float:
        h, m = clock.split(":")
        return int(h) + int(m) / 60

    t0 = hours(str(f["start"]))
    unit = "degF" if f["unit"] == "degF" else "degC"
    room = si(loads.design(kid).site.ambient, "K")
    pts = [(0.0, room)]
    for clock, temp in f["value"]:
        t = (hours(str(clock)) - t0) % 24
        pts.append((t * HOUR, si(Q_(float(temp), unit), "K")))
    return tuple(pts)
