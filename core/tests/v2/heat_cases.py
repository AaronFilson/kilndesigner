"""The reference kilns' firings as heat-model runs, for the reference-firing tests.

Each case is a kiln's design file plus what the book doesn't print and the model needs, each a
stated test input (not engineering data) with its question in `docs/planning/11-09-26.md` §I: the
setting's load and envelope above all (ADR 0017 decision 11: no heat result without a load).
Nothing here is fitted: each input is the survey's test input or the book's printed figure.
"""

from __future__ import annotations

from collections.abc import Hashable, Mapping
from dataclasses import replace
from functools import cache
from pathlib import Path
from typing import Any, Protocol

import fuel as own
import yaml

from kilndesigner.designfile import load_design
from kilndesigner.model import Kiln
from kilndesigner.v2.heat import bands
from kilndesigner.v2.heat import draft as dr
from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import gas
from kilndesigner.v2.heat import kiln as hk

ROOT = Path(__file__).resolve().parents[3]
OLSEN = ROOT / "examples" / "olsen"
IN = 0.0254
HOUR = 3600.0
CONE_10 = 1285 + 273.15
CONE_10_FAST = 1305 + 273.15
# The rays: 10⁵ a zone moves cone 10 by under 0.1 % against 10⁶ (thermal-combinations.md §4.1)
RAYS = 100_000


class Outcome(Protocol):
    """What a reference-firing test reads from a run."""

    @property
    def completed(self) -> bool: ...

    @property
    def worst_air_share(self) -> float: ...

    @property
    def fuel_kg(self) -> float: ...

    def reached(self, target: float) -> float | None: ...


# Olsen's fast-fire (p.139–143). TEST INPUTS: the setting's envelope from p.142's layout (4½ in
# clear each side and in front, 1 in at the back; on the bag walls' two rowlock rows, 9 in; to
# 33 in, under the 36 in springline) and its 55 kg (three 12 × 24 × 1 in shelves, posts and
# about 25 kg of ware: the survey's); ε 0.8 (the survey's); its own wood (below; until B4 a test
# input, 12 % moisture at 19 MJ/kg); λ 1 (the stoker's, the survey's); the grate's ¾ in round bars
# (printed, p.204).
FAST_FIRE_LOAD = hk.Load(
    55.0,
    (-9 * IN, -9 * IN, 9 * IN),
    (9 * IN, 12.5 * IN, 33 * IN),
    0.8,
    "TEST INPUT: envelope from Olsen p.142's layout, 55 kg and ε 0.8 the survey's "
    "(thermal-combinations.md §4.1); the book prints no load",
)
WOOD = hk.Wood(0.12, 19e6, "TEST INPUT: FAO's air-dried 12 %, Forest Research's 19 MJ/kg")
# The fast-fire's own fuel (ADR 0017 decision 12): "wood of any kind" (printed, p.139), the
# dataset's band for a wood no source names (kiln-fuels.md §5: coniferous or deciduous, net
# 17.60–19.31 MJ/kg dry, 12–25 % moisture, the analysis at its quartiles' middles)


def fast_fire_fuel(end: own.End = "mid") -> gas.Fuel:
    return own.own_fuels("fast-fire", end)[0]


def own_intake(kid: str) -> dr.Intakes | None:
    """A kiln's air intakes as the draft takes them, from the dataset (firebox-air-intakes.md
    §3): below the grate and above it, each its band; None where the dataset has a gap."""
    got = own.own_intakes(kid)
    if got is None:
        return None
    return dr.Intakes(*got, reference=f"{kid}'s, the dataset's (firebox-air-intakes.md §3)")


# Olsen p.309's log, minutes from 4:55 and °C, the start at the room's 21.1 °C (70 °F)
LOG = (
    (0, 21.1), (5, 190), (20, 315), (35, 455), (50, 580), (65, 720), (80, 790), (95, 900),
    (110, 955), (125, 1016), (140, 1050), (155, 1095), (170, 1105), (185, 1180), (200, 1205),
    (215, 1235), (230, 1260), (245, 1285), (260, 1285), (275, 1285), (290, 1285),
)  # fmt: skip
LOG_POINTS = tuple((m * 60.0, c + 273.15) for m, c in LOG)


@cache
def fast_fire_model(
    heavier: float = 1.0, path: bool = True, end: own.End = "mid", intakes: bool = True
) -> Any:
    """The fast-fire's whole gas path (B2: the fireboxes and the chimney as zones of their own,
    with their own brick), or (``path`` False) its chamber alone as the one zone the fire burns
    in, as first built; its own wood at its bands' ``end``; its draft through its own intakes,
    below and above the grates (B4), or (``intakes`` False) the design's ash-pit mouths alone."""
    k = load_design(OLSEN / "fast-fire.yaml")
    load = replace(FAST_FIRE_LOAD, mass=FAST_FIRE_LOAD.mass * heavier)
    intake = own_intake("fast-fire") if intakes else None
    return hk.heat_model(k, load, 1.0, fast_fire_fuel(end), n_rays=RAYS, grate_bar=0.75 * IN,
                         path=path, intake=intake)  # fmt: skip


def fast_fire_max(heavier: float = 1.0) -> fi.Firing:
    model = fast_fire_model(heavier)
    return fi.fire(model, fi.MaxFire(), 6 * HOUR, (CONE_10,), CONE_10_FAST)


@cache
def fast_fire_log(air: str = "stoker", opened: float = 1.0) -> fi.Firing:
    """p.309's log held by the setting: the stoker's air at λ 1 (the least wood), or the draft's
    own through the intakes ``opened`` a share open (λ from the draft)."""
    mode = fi.Schedule("setting", LOG_POINTS, air=air, opened=opened)  # pyright: ignore[reportArgumentType]
    return fi.fire(fast_fire_model(), mode, LOG[-1][0] * 60.0, (CONE_10,))


# --- the fast-fire's bands (ADR 0017 decision 17; `bands.py`) ------------------------------------

# 2·10⁴ rays a zone for the band's runs: each run's own noise well inside the bands it draws
BAND_RAYS = 20_000
MAX_TIME, LOG_WOOD, LOG_AIR = (
    "max fire to cone 10 (h)", "the log's wood (kg, dry)", "the log's air over the draft's most"
)  # fmt: skip
FAST_FIRE_INPUTS = (
    bands.Input("emissivity class", ("low", "high"), "nominal",
                "radiation-exchange.md §5: each brick's lines, the lower and the higher, × 0.95–1.0"),
    bands.Input("grey gases", ("bordbar2014", "dorigon2013"), "bordbar2014",
                "thermal-software.md §6.1: the two HITEMP-2010 WSGG sets"),
    bands.Input("the draft", ("least", "most"), "least",
                "draft.py: brick's roughness (no source), the fittings' two-valued coefficients, "
                "the intakes' areas (the dataset's)"),
    bands.Input("the wood", ("least", "most"), "mid",
                "kiln-fuels.md §5: 'wood of any kind', 12–25 % moisture, 17.60–19.31 MJ/kg dry"),
    bands.Input("the load", (27.5, 220.0), 55.0,
                "TEST INPUT: half to four times the survey's 55 kg (the book prints none)"),
    bands.Input("the setting's passages", (0.025, 0.100), 0.100,
                "sources.SETTING_GAP: gaps of 25–100 mm, a stated band"),
    bands.Input("λ", ("stoker", "draft"), "stoker",
                "decision 9: the stoker's air at λ 1, to all the draft's air (the intakes open)"),
)  # fmt: skip


@cache
def _band_model(wsgg: str, wood: own.End, emissivity: str) -> Any:
    """The fast-fire traced once for each grey-gas set, wood and emissivity class."""
    k = load_design(OLSEN / "fast-fire.yaml")
    return hk.heat_model(
        k, FAST_FIRE_LOAD, 1.0, fast_fire_fuel(wood), wsgg=wsgg, n_rays=BAND_RAYS,  # pyright: ignore[reportArgumentType]
        grate_bar=0.75 * IN, path=True, intake=own_intake("fast-fire"),
        emissivity=emissivity,  # pyright: ignore[reportArgumentType]
    )  # fmt: skip


def _band_variant(s: Mapping[str, Hashable]) -> Any:
    """A band run's model: the traced one with its load, passages and draft's end set."""
    m = _band_model(str(s["grey gases"]), s["the wood"], str(s["emissivity class"]))  # pyright: ignore[reportArgumentType]
    mass, gap = float(s["the load"]), float(s["the setting's passages"])  # pyright: ignore[reportArgumentType]
    settings = tuple(replace(x, mass=mass, gap=gap) for x in m.settings)
    path = m.path.most() if s["the draft"] == "most" else m.path
    return replace(m, settings=settings, path=path)


@cache
def _band_max(key: tuple[Hashable, ...]) -> float | None:
    s = dict(zip([i.name for i in FAST_FIRE_INPUTS], key, strict=True))
    t = fi.fire(_band_variant(s), fi.MaxFire(), 6 * HOUR, (), CONE_10).reached(CONE_10)
    return None if t is None else t / HOUR


def fast_fire_run(s: Mapping[str, Hashable]) -> dict[str, float | None]:
    """One band run: the max fire's time to cone 10 (λ doesn't touch it: run once for the rest)
    and p.309's log's wood and air."""
    key = tuple(s[i.name] if i.name != "λ" else "stoker" for i in FAST_FIRE_INPUTS)
    mode = fi.Schedule("setting", LOG_POINTS, air=s["λ"])  # pyright: ignore[reportArgumentType]
    log = fi.fire(_band_variant(s), mode, LOG[-1][0] * 60.0, sample=300.0)
    return {MAX_TIME: _band_max(key), LOG_WOOD: log.fuel_kg, LOG_AIR: log.worst_air_share}


@cache
def fast_fire_bands() -> dict[str, bands.Band]:
    return bands.corner_runs(fast_fire_run, FAST_FIRE_INPUTS)


def _crossdraft(change: dict[str, Any]) -> Kiln:
    data = yaml.safe_load((OLSEN / "olsen-crossdraft-36.yaml").read_text(encoding="utf-8"))
    for key, value in change.items():
        node = data
        *parents, last = key.split(".")
        for p in parents:
            node = node.setdefault(p, {})
        node[last] = value
    return Kiln.model_validate(data)


# The 36 ft³ cross-draft (p.226) and W15. TEST INPUTS: the exit flue 9 × 4½ in at the back's foot
# (the design leaves it to the engine; the survey's); a setting 4½ in clear of the walls from 4½ in
# to 36 in up, 150 kg, ε 0.8 (the survey's); natural gas (the design's assumption).
FLUE = {"draft.flue_port": {"width": "9 in", "height": "4.5 in"}}
CUBE = 39.6 * IN
CROSSDRAFT_LOAD = hk.Load(
    150.0,
    (-CUBE / 2 + 4.5 * IN, -CUBE / 2 + 4.5 * IN, 4.5 * IN),
    (CUBE / 2 - 4.5 * IN, CUBE / 2 - 4.5 * IN, 36 * IN),
    0.8,
    "TEST INPUT: 4½ in clear of the walls, 150 kg, ε 0.8 (thermal-combinations.md §4.2); the "
    "book prints no load",
)


def _burners(kiln: Kiln, model: Any) -> float:
    rated = hk.rated_fuel(kiln, model.products.fuel)
    assert rated is not None
    return rated


def crossdraft_36() -> fi.Firing:
    """As designed (4½ in medium-duty over 4½ in K-23, assumed), six burners at their printed
    rating, λ 1 (the most heat any air ratio leaves), to 30 h."""
    k = _crossdraft(FLUE)
    m = hk.heat_model(k, CROSSDRAFT_LOAD, 1.0, n_rays=RAYS)
    return fi.fire(m, fi.FixedInput(_burners(k, m)), 30 * HOUR, (CONE_10,), CONE_10)


# W15 (p.226): "an updraught kiln of 36cu. ft using insulation bricks will have a minimum of 10
# such burners". TEST INPUTS: the cross-draft's cube and setting; the lining 4½ in K-26 over 4½ in
# K-23 (the survey's; the book says only "insulation bricks"); λ 1.15 (3 % O₂, v1's oxidising air
# ratio: more flue loss than λ 1).
IFB = {
    "lining.walls": [
        {"material": "ifb-k26", "thickness": "4.5 in"},
        {"material": "ifb-k23", "thickness": "4.5 in"},
    ],
    "heat.gas.burners.count": 10,
}


def w15_ifb() -> fi.Firing:
    k = _crossdraft(FLUE | IFB)
    m = hk.heat_model(k, CROSSDRAFT_LOAD, 1.15, n_rays=RAYS)
    return fi.fire(m, fi.FixedInput(_burners(k, m)), 12 * HOUR, (CONE_10,), CONE_10)
