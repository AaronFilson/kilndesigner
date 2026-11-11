"""Part C3b's rows as heat-model runs (`docs/planning/11-10-26.md`, "C3b as built"): the climbing
and multi-chamber reference kilns fired in stages, each stage on its own draft (`series.py`).

**The stages.** The book's where it prints them (Suzuki p.93; Tamba pp.86–87; Fujiwara
pp.103–104; Hollyweird p.117); else the front firebox (or the first chamber's own trough) to
1000 °C, the Kyoto kilns' practice before side stoking (p.93, p.86), then each chamber stoked from
its sides to its cone. The front's stage burns in the firebox's zone on the front's own path; each
chamber's in its own zone on its side holes beside the front's path, or alone with the fire mouth
shut (`paths.Inputs.stage`, ``front_open``; C1's question 3: the band's two ends). Fireboxes one
to a chamber (Suzuki, Tobe, Hotchkiss: the owner's question 3) are read into the path by
`path_inputs.ONE_PER_CHAMBER`, and the heat model takes the chambers alone (no firebox zone from
v1's side-by-side layout), so each stage's fuel burns in its chamber's zone.

**The bands** (`bands.py`'s corner runs; ADR 0017 decision 17): the setting (C2's band,
`loads.py`), the wood (its band, `fuel.py`: heat value and moisture; the grey gases traced at its
middle, so the rays are traced once), the draft (its least-air and most-air ends) and the fire
mouth while side stoking (open, shut), one at a time on the smaller rows. On Suzuki and Tamba the
four move together, all at their slow ends or all at their fast ends (`TOGETHER`): each run takes
a minute or more there, and each input lengthens the firing the same way (heavier, wetter, less
air, the mouth shut), so its band's ends are the same corners. The rows with T1 alone, and Tobe
and Kyoto (minutes a run), run their nominal in the suite; their bands, and Suzuki's inputs one by
one, come from the same code run outside it (the plan doc). Held to the book's stage times, the
stoker's λ 1 alone (`HELD_INPUTS`).

**Stoked times are inequalities** (problem set §2.2, §6): max fire is the fastest the kiln's
draft lets a stage go, so a printed stage time stands if v2's max fire is no slower somewhere in
its band. Nothing here is fitted: each input is the book's, the dataset's (with its source) or a
stated band's end.
"""

from __future__ import annotations

import math
from collections.abc import Hashable, Mapping
from dataclasses import dataclass, field, replace
from functools import cache
from typing import Any

import fuel as own
import loads
import path_inputs as pi
import reference as ref
import yaml

from kilndesigner.cones import cone_temperature
from kilndesigner.model import Kiln
from kilndesigner.units import Q_, si
from kilndesigner.v2.heat import bands, gas
from kilndesigner.v2.heat import draft as dr
from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat import series as se
from kilndesigner.v2.heat.paths import Inputs
from kilndesigner.v2.heat.zone import ZoneModel

HOUR, IN = 3600.0, 0.0254
ROW_RAYS = 20_000  # 2·10⁴ a zone, as B4's and C2's bands (the nominal within 0.1 % of 10⁵)
RTOL = 1e-4  # IDA's: Bidai's four stage times within 0.05 % of 1e-5's, in half the time
SAMPLE = 3600.0
# Side stoking begins at about 1000 °C: Olsen p.93 (Suzuki: the firebox to 1832 °F before side
# stoking), p.86 (Tamba: the first stoke holes to about 1832 °F)
RED = 1000 + 273.15
# A stage's longest at max fire, past which it isn't reached (+∞ in the band): above the longest
# stage the book prints, Tamba's 36 h preheat, by two thirds again
LIMIT = 60 * HOUR


# --- the stages --------------------------------------------------------------------------------


@dataclass(frozen=True)
class Phase:
    """A stage as the book describes it: its name, the chamber whose setting ends it (from 0),
    its target (K; None: the chamber's cone), whether it is side-stoked (else the front's), the
    book's time for it (h), the time a held run takes it to (h, or "side": Tamba's side stoking's
    share; None: not held), and how long it may run at most (h; None: `LIMIT`): a stage the book
    gives a time and no temperature for (Fujiwara's dogi) runs that long or to the cone."""

    name: str
    chamber: int
    target: float | None = None
    side: bool = True
    book: float | None = None
    held: float | str | None = None
    limit: float | None = None


@dataclass(frozen=True)
class Plan:
    """A row's staged firing: the stages, whether its fireboxes are zones of their own (False:
    one to a chamber, the fire in each chamber's zone), path inputs over the dataset's, and the
    stages whose max-fire fuel rate the book prints a rate against."""

    kid: str
    phases: tuple[Phase, ...]
    zoned: bool = True
    inputs: dict[str, Any] = field(default_factory=dict)
    rate: tuple[int, ...] = ()


def _climbing(n: int, front: str = "the front, to 1000 °C") -> tuple[Phase, ...]:
    """The Kyoto kilns' practice: the front to 1000 °C (p.93), then each chamber to its cone."""
    return (Phase(front, 0, RED, side=False),
            *(Phase(f"chamber {k + 1}", k) for k in range(n)))  # fmt: skip


# Kitade's chimney, which nothing in the book sizes (C1's refusal): Olsen's Rule 6, the chimney ¼ to
# ⅕ of the chamber's width and seldom under 9 × 9 in at its base (pp.79–80; kiln-reference.md
# "Chimney size"), its 48 in chamber 9.6–12 in square; p.78 carries the exits from it, and its
# height is the climbing kiln's band (p.81, p.101): `paths.Inputs.rule6`, C3a's band for the six
# kilns with nothing sized (C1's question 8), the path's working saying so

PLANS: dict[str, Plan] = {
    # p.93: the firebox stoked 15 h to 1000 °C (the main firebox isn't in the design: the first
    # chamber's own trough takes it), then each chamber's sides: 7 h each for 1–3 (reduction), 5 h
    # each for 4–7 (oxidation); the cones 10, 10, 8–9 (9 taken, the hotter, as the design), 8–9, …,
    # 1 (Fig 4-35)
    "suzuki-kyoto": Plan("suzuki-kyoto", (
        Phase("the firebox, to 1000 °C", 0, RED, side=False, book=15.0, held=15.0),
        *(Phase(f"chamber {k + 1}", k, book=7.0, held=7.0) for k in range(3)),
        *(Phase(f"chamber {k + 1}", k, book=5.0) for k in range(3, 7)),
    ), zoned=False, rate=(1, 2, 3)),
    # pp.86–87: the dogi alone about 36 h, bringing the first three or four stoke holes (chamber 1
    # of seven, its holes 1½ ft apart, Fig 4-7) to about 1000 °C, then 14–18 h of side stoking;
    # cone 10 (assumed)
    "tamba": Plan("tamba", (
        Phase("the dogi, to 1000 °C", 0, RED, side=False, book=36.0, held=36.0),
        *(Phase(f"chamber {k + 1}", k, held="side") for k in range(7)),
    )),
    # pp.103–104: 2½ days stoking the fire mouth's air duct and 4 days the fire mouth, 6½ days "to
    # temperature" (the dogi's ware, which the design leaves out), then 12 h stoking the chambers;
    # 7 days in all. The first chamber's temperature when side stoking begins isn't printed: the
    # dogi's stage is 6½ days at max fire (or until the first chamber reaches its cone), the
    # hottest it can leave the first chamber, so the chambers' stages are the shortest they can be
    "fujiwara-bizen": Plan("fujiwara-bizen", (
        Phase("the dogi, 6½ days", 0, side=False, book=6.5 * 24, limit=6.5 * 24),
        Phase("chamber 1", 0), Phase("the kedo", 1),
    )),
    # p.117: a normal 60 h firing, the front chamber held at cone 11-plus 35–40 h and the back one
    # 10–15 h: the front's firebox to the first chamber's cone, then the second chamber's own
    # firebox (its trough) to its cone. The dataset's intake is the front firebox's own stoke hole
    # (its condition, research A2), so the front's path takes all of it, not a half shared with
    # the second firebox by count (`paths._Build.feeds`' sharing is for intakes of all of them)
    "hollyweird": Plan("hollyweird", (
        Phase("the front chamber", 0, side=False), Phase("the back chamber", 1),
    ), inputs={"intake": (pi.intakes("hollyweird"), None)}),
    "tobe": Plan("tobe", _climbing(7, "chamber 1's trough, to 1000 °C"), zoned=False),
    "kyoto-climbing": Plan("kyoto-climbing", _climbing(10, "chamber 1's trough, to 1000 °C"),
                           zoned=False),
    # The dataset's intake is the second firebox's stoke hole (its condition, research A2), which
    # the second chamber's stage doesn't reach (its side holes, not sized, are its air); the front
    # firebox takes its own, the design's ash-pit mouth, not half the second's shared by count
    "olsen-two-chamber": Plan("olsen-two-chamber", (
        Phase("chamber 1", 0, side=False), Phase("chamber 2", 1),
    ), inputs={"intake": (None, None)}),
    "bidai": Plan("bidai", _climbing(3)),
    "kawaii": Plan("kawaii", _climbing(4)),
    "hotchkiss-raw-clay": Plan("hotchkiss-raw-clay", _climbing(6, "chamber 1's trough, to 1000 °C"),
                               zoned=False),
    "kitade-tojilo": Plan("kitade-tojilo", (Phase("the chamber", 0, side=False),),
                          inputs={"rule6": True}),
    "bae-gilgama": Plan("bae-gilgama", (Phase("the chamber", 0, side=False),)),
}  # fmt: skip
ROWS = tuple(PLANS)


def path_inputs(kid: str, **change: Any) -> Inputs:
    """The kiln's path inputs: the dataset's (`path_inputs.py`), its plan's over them."""
    return pi.inputs(kid, **(PLANS[kid].inputs | change))


def cones(kid: str) -> list[float]:
    """Each chamber's cone (K): the design's `chamber_cones`, else its cone, at its final rate."""
    f = loads.design(kid).firing
    n = loads.design(kid).chamber.chambers
    each = f.chamber_cones or [f.cone] * n
    return [si(cone_temperature(str(c if c is not None else f.cone), f.final_rate), "K")
            for c in each]  # fmt: skip


# --- the model and its variants ------------------------------------------------------------------


@cache
def model(kid: str) -> ZoneModel:
    """The kiln traced once: its own setting and wood at their bands' middles, λ 1 (the stoker's
    and max fire's), its own path."""
    k = loads.design(kid)
    return hk.heat_model(k, loads.loads(kid, "mid"), 1.0, own.own_fuels(kid, "mid")[0],
                         n_rays=ROW_RAYS, path=PLANS[kid].zoned,
                         path_inputs=path_inputs(kid))  # fmt: skip


@cache
def variant(kid: str, load: loads.End, wood: own.End) -> ZoneModel:
    """The traced model with its settings at the load band's end and its wood at its band's end:
    the products' heat, air and gas taken from the wood's end, the rays' grey gases left at its
    middle (traced once; said in the plan doc)."""
    m = model(kid)
    masses = [x.mass for x in loads.loads(kid, load)]
    settings = tuple(replace(s, mass=w) for s, w in zip(m.settings, masses, strict=True))
    prod = m.products
    if wood != "mid":
        prod = gas.products(own.own_fuels(kid, wood)[0], 1.0, m.t_room)
    return replace(m, settings=settings, products=prod)


@cache
def design(kid: str, slope: float | None = None) -> Kiln:
    """The design, or with its run laid at a slope (degrees) the book doesn't print (Tamba's: the
    path's columns change, the rays don't: B1, a slope turns the whole solid)."""
    if slope is None:
        return loads.design(kid)
    data = yaml.safe_load((ref.ROOT / str(own._kilns()[kid]["design"])).read_text("utf-8"))  # pyright: ignore[reportPrivateUsage]
    data["chamber"]["slope"] = f"{slope} degree"
    return Kiln.model_validate(data)


@cache
def stage_path(
    kid: str, stage: int | None, front_open: bool, most: bool, slope: float | None = None
) -> dr.Path:
    """A stage's own draft path at an end of the draft's band: the front's (``stage`` None), or a
    chamber's side holes beside the front's path, or alone with the fire mouth shut."""
    if stage is None and slope is None:
        p = model(kid).path
    else:
        p = dr.kiln_path(design(kid, slope), inputs=path_inputs(kid, stage=stage,
                                                                front_open=front_open))  # fmt: skip
    assert p is not None
    return p.most() if most else p


# --- the runs ------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Corner:
    """One run's inputs: the load's and the wood's ends, the draft's end (most air or least), the
    fire mouth while side stoking, λ for a held run, the side stoking's time (Tamba's band, h) and
    the run's slope (Tamba's band, degrees; None: the design's)."""

    load: loads.End = "mid"
    wood: own.End = "mid"
    most_air: bool = False
    front_open: bool = True
    air: str = "stoker"
    side_time: float = 16.0
    slope: float | None = None


def stages(kid: str, c: Corner, held: bool = False) -> list[se.Stage]:
    """The plan's stages at a corner: max fire on each stage's own draft, or (``held``) each held
    to the book's time on a straight ramp, the stoker's air or the draft's own."""
    m = model(kid)
    out: list[se.Stage] = []
    for ph in PLANS[kid].phases:
        if held and ph.held is None:
            break
        target = cones(kid)[ph.chamber] if ph.target is None else ph.target
        limit = LIMIT if ph.limit is None else ph.limit * HOUR
        mode: se.StageMode = fi.MaxFire()
        if held:
            hours = c.side_time / 7 if ph.held == "side" else float(ph.held)  # type: ignore[arg-type]
            mode = se.Ramp(hours * HOUR, "draft" if c.air == "draft" else "stoker")
        if ph.side:
            path = stage_path(kid, ph.chamber, c.front_open, c.most_air, c.slope)
            out.append(se.Stage(ph.chamber, mode, target, limit, path, None, c.front_open,
                                ph.name))  # fmt: skip
        else:
            path = stage_path(kid, None, True, c.most_air, c.slope)
            out.append(se.Stage(ph.chamber, mode, target, limit, path, m.burns, True, ph.name))
    return out


NOMINAL = Corner()


@cache
def run(kid: str, c: Corner = NOMINAL, held: bool = False) -> se.Staged | None:
    """A staged firing at a corner; None where it can't be fired (no consistent state)."""
    try:
        return se.fire_stages(variant(kid, c.load, c.wood), stages(kid, c, held), SAMPLE, RTOL)
    except fi.FiringError:
        return None


# --- the bands -----------------------------------------------------------------------------------

LOAD = bands.Input(
    "the load",
    ("least", "most"),
    "mid",
    "kiln-settings.md: the kiln's setting band (the dataset's `setting` facts; C2)",
)
WOOD = bands.Input(
    "the wood",
    ("least", "most"),
    "mid",
    "kiln-fuels.md §5: the kiln's own wood, "
    "its moisture and heating value bands (the grey gases at their middles)",
)
DRAFT = bands.Input(
    "the draft",
    ("least", "most"),
    "least",
    "draft.py: brick's roughness (no "
    "source), the fittings' two-valued coefficients, the length bands",
)
MOUTH = bands.Input(
    "the fire mouth",
    ("open", "shut"),
    "open",
    "C1's question 3: whether the "
    "stoker shuts the fire mouth while side stoking isn't printed: its two ends",
)
LAMBDA = bands.Input(
    "λ",
    ("stoker", "draft"),
    "stoker",
    "decision 9: the stoker's air at λ 1, to all the draft's air (the intakes open)",
)
SIDE_TIME = bands.Input(
    "the side stoking's time",
    (14.0, 18.0),
    16.0,
    "printed, pp.86–87: 14–18 h, shared evenly among the seven chambers (an assumption)",
)
TOGETHER = bands.Input(
    "the setting, the wood, the draft and the fire mouth together",
    ("fast", "slow"),
    "nominal",
    "each input's band as above, all at the ends that "
    "shorten the stages or all at those that lengthen them (the largest rows)",
)
# Tamba's slope isn't printed (its doc's question 3; C1's question 5): the design lays the tube
# level (an assumption, the nominal); the book's own tube and climbing kilns print 20 %, "standard
# for most kilns of this style" (p.108, Mr Bae's), to the anagama drawn at 25° (Fig 4-5, p.84)
SLOPE = bands.Input(
    "the tube's slope (°)",
    (11.3, 25.0),
    None,
    "not printed: the design's level nominal; the book's tubes 20 % (p.108) to 25° (Fig 4-5, p.84)",
)
INPUTS: dict[str, tuple[bands.Input, ...]] = {
    "fujiwara-bizen": (LOAD, WOOD, DRAFT, MOUTH),
    "hollyweird": (LOAD, WOOD, DRAFT, MOUTH),
    "olsen-two-chamber": (LOAD, WOOD, DRAFT, MOUTH),
    "kitade-tojilo": (LOAD, WOOD, DRAFT),
    "bae-gilgama": (LOAD, WOOD, DRAFT),
    "suzuki-kyoto": (TOGETHER,),
    # SLOPE waits: the engine steps a row's chambers' floors, and Tamba's tube at 11.3° steps each
    # segment 41 in, past the 12 in springline, so `run_parts.flue_rows` finds no flue between them
    "tamba": (TOGETHER,),
    # The longest runs (Tobe's three minutes each, Kyoto's ten chambers about two) and the rows
    # with T1 alone (no number printed: their nominal runs reach every cone): their nominal runs
    # alone in the suite, Tobe's figure an inequality its nominal already meets; their bands' ends
    # from runs outside it (the plan doc)
    "tobe": (),
    "kyoto-climbing": (),
    "bidai": (),
    "kawaii": (),
    "hotchkiss-raw-clay": (),
}
# Held to the book's times, at the stoker's λ 1 (the least air, so the least fuel at that pace). A
# held run on all the draft's own air (λ from the draft, the band's other end) runs on Suzuki
# (4.38 t for chambers 1–3, against 3.02 t at λ 1) but failed in IDA 1.6 h into Bidai's dogi ramp
# (the corrector's convergence): that air enters every residual through the draft's bisection, so
# any kink in the path's losses (`draft.darcy`'s laminar–turbulent switch, a parallel branch coming
# on) is a jump IDA meets; not traced further, the plan doc's open item. Each held run takes
# minutes, so the suite runs the nominal alone
HELD_INPUTS: dict[str, tuple[bands.Input, ...]] = {"suzuki-kyoto": (), "tamba": ()}
FAST = Corner("least", "most", True, True)
SLOW = Corner("most", "least", False, False)


def corner(s: Mapping[str, Hashable]) -> Corner:
    """A band run's inputs as a corner."""
    c = Corner()
    if "the setting, the wood, the draft and the fire mouth together" in s:
        c = {"fast": FAST, "slow": SLOW}.get(str(s[TOGETHER.name]), c)
    return replace(
        c,
        load=s.get(LOAD.name, c.load),  # type: ignore[arg-type]
        wood=s.get(WOOD.name, c.wood),  # type: ignore[arg-type]
        most_air=s.get(DRAFT.name, "most" if c.most_air else "least") == "most",
        front_open=s.get(MOUTH.name, "open" if c.front_open else "shut") == "open",
        air=str(s.get(LAMBDA.name, c.air)),
        side_time=float(s.get(SIDE_TIME.name, c.side_time)),  # type: ignore[arg-type]
        slope=s.get(SLOPE.name, c.slope),  # type: ignore[arg-type]
    )


FIRING, FUEL, RATE = "the firing (h)", "the fuel (t, dry)", "the most fuel burnt (kg/h, dry)"
SIDES, WET = "the side stoking (h)", "the fuel as fired (t)"


def results(kid: str, staged: se.Staged | None, moisture: float = 0.0) -> dict[str, float | None]:
    """A max-fire run's results: each stage's time (h), the side stoking's and the firing's (h),
    its fuel (t, dry, and as fired at the run's ``moisture``), and the most fuel the draft burns at
    λ 1 over the stages the book prints a rate for (kg/h). A stage the book gives a time and no
    temperature for counts its time."""
    plan = PLANS[kid]
    names = [f"{ph.name} (h)" for ph in plan.phases]
    keys = [*names, SIDES, FIRING, FUEL, WET, *([RATE] if plan.rate else [])]
    if staged is None:
        return dict.fromkeys(keys)
    # a firing IDA couldn't carry on (SUNDIALS' own failure, kept in its record) ends early
    times = [*staged.times, *[None] * (len(names) - len(staged.times))]
    out: dict[str, float | None] = {n: None if t is None else t / HOUR
                                    for n, t in zip(names, times, strict=True)}  # fmt: skip
    timed = [(ph.limit if t is None and ph.limit is not None else None if t is None else t / HOUR)
             for ph, t in zip(plan.phases, times, strict=True)]  # fmt: skip
    side = [t for ph, t in zip(plan.phases, timed, strict=True) if ph.side]
    out[SIDES] = None if None in side else sum(t or 0.0 for t in side)
    total = None if None in timed else sum(t or 0.0 for t in timed)
    out[FIRING] = total
    out[FUEL] = sum(staged.fuel) / 1e3 if total is not None else None
    out[WET] = None if total is None else sum(staged.fuel) / 1e3 / (1 - moisture)
    if plan.rate:
        hours = [staged.times[i] for i in plan.rate]
        done = all(t is not None and t > 0 for t in hours)
        burnt = sum(staged.fuel[i] for i in plan.rate)
        out[RATE] = burnt / (sum(t or 0.0 for t in hours) / HOUR) if done else None
    return out


SIDE_FUEL = "the side stoking's fuel (t, dry)"


def held_results(kid: str, staged: se.Staged | None) -> dict[str, float | None]:
    """A held run's results: the side stages' fuel (t, dry); none where it couldn't be fired."""
    if staged is None or not staged.firing.completed:
        return {SIDE_FUEL: None}
    side = [w for ph, w in zip(PLANS[kid].phases, staged.fuel, strict=False) if ph.side]
    return {SIDE_FUEL: sum(side) / 1e3}


def _results(kid: str, s: Mapping[str, Hashable]) -> dict[str, float | None]:
    c = corner(s)
    return results(kid, run(kid, c), variant(kid, c.load, c.wood).products.fuel.moisture)


@cache
def band(kid: str) -> dict[str, bands.Band]:
    """v2's bands over the kiln's max-fire inputs (`INPUTS`)."""
    return bands.corner_runs(lambda s: _results(kid, s), INPUTS[kid])


@cache
def held_band(kid: str) -> dict[str, bands.Band]:
    """v2's bands over the kiln's held runs' inputs (`HELD_INPUTS`)."""
    return bands.corner_runs(lambda s: held_results(kid, run(kid, corner(s), True)),
                             HELD_INPUTS[kid])  # fmt: skip


# --- the book's side -----------------------------------------------------------------------------

# A bundle's weight: no source (kiln-fuelwood-by-region.md §3). A stated band: its gross volume
# packed as a cord is stacked, a cord's oven-dry weight over its 128 ft³ (USU Extension, Wood
# Heating, Table 1; wood-fuel.md [W4]; `fuel.CORD_DRY_LB_*`): pine 2,250–2,610 lb (Suzuki's split
# pine, kiln-fuelwood-by-region.md [K1]), any species 2,070–4,200 lb (Tamba's, not named). That a
# bundle packs as a cord is stacked is the assumption (the owner's question)
CORD_FT3 = 128.0


def bundle_kg(volume_m3: float, pine: bool) -> tuple[float, float]:
    """A bundle's oven-dry weight band (kg) from its gross volume (m³), packed as a cord."""
    lb = own.CORD_DRY_LB_PINE if pine else own.CORD_DRY_LB_ANY
    cord = si(Q_(CORD_FT3, "ft**3"), "m**3")
    lo, hi = (si(Q_(x, "lb"), "kg") * volume_m3 / cord for x in lb)
    return lo, hi


# Suzuki's bundle, "15 in (38 cm) in diameter and 18 in (46 cm) long" (p.93): π/4 × 15² × 18 in³;
# Tamba's, 15 × 15 × 30 in (pp.86–87)
BUNDLES = {
    "suzuki-kyoto": (math.pi / 4 * (15 * IN) ** 2 * 18 * IN, True),
    "tamba": (15 * IN * 15 * IN * 30 * IN, False),
}


def bundle(kid: str) -> tuple[float, float]:
    """A bundle's oven-dry weight band (kg): the dataset's `fuel_unit_mass` (assumed, its reason
    the arithmetic above)."""
    f = ref.facts(own._kilns()[kid], "heat", "fuel_unit_mass")[0]  # pyright: ignore[reportPrivateUsage]
    return ref.span(f, "kg")


SHORT_TON, TONNE = si(Q_(1, "ton"), "kg"), 1000.0  # Tobe's 40 tons: short or metric isn't said
