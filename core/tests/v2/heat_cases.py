"""The reference kilns' firings as heat-model runs, for the reference-firing tests.

Each case is a kiln's design file plus what the book doesn't print and the model needs, each a
stated test input (not engineering data) with its question in `docs/planning/11-09-26.md` §I: the
setting's load and envelope above all (ADR 0017 decision 11: no heat result without a load).
Nothing here is fitted: each input is the survey's test input or the book's printed figure.
"""

from __future__ import annotations

from dataclasses import replace
from functools import cache
from pathlib import Path
from typing import Any, Protocol

import yaml

from kilndesigner.designfile import load_design
from kilndesigner.model import Kiln
from kilndesigner.v2.heat import firing as fi
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
# about 25 kg of ware: the survey's); ε 0.8 (the survey's); wood 12 % moisture (FAO's air-dried
# low end) at 19 MJ/kg net oven-dry (Forest Research); λ 1 (the stoker's, the survey's); the
# grate's ¾ in round bars (printed, p.204).
FAST_FIRE_LOAD = hk.Load(
    55.0,
    (-9 * IN, -9 * IN, 9 * IN),
    (9 * IN, 12.5 * IN, 33 * IN),
    0.8,
    "TEST INPUT: envelope from Olsen p.142's layout, 55 kg and ε 0.8 the survey's "
    "(thermal-combinations.md §4.1); the book prints no load",
)
WOOD = hk.Wood(0.12, 19e6, "TEST INPUT: FAO's air-dried 12 %, Forest Research's 19 MJ/kg")
# Olsen p.309's log, minutes from 4:55 and °C, the start at the room's 21.1 °C (70 °F)
LOG = (
    (0, 21.1), (5, 190), (20, 315), (35, 455), (50, 580), (65, 720), (80, 790), (95, 900),
    (110, 955), (125, 1016), (140, 1050), (155, 1095), (170, 1105), (185, 1180), (200, 1205),
    (215, 1235), (230, 1260), (245, 1285), (260, 1285), (275, 1285), (290, 1285),
)  # fmt: skip


@cache
def fast_fire_model(heavier: float = 1.0) -> Any:
    k = load_design(OLSEN / "fast-fire.yaml")
    load = replace(FAST_FIRE_LOAD, mass=FAST_FIRE_LOAD.mass * heavier)
    return hk.heat_model(k, load, 1.0, WOOD, n_rays=RAYS, grate_bar=0.75 * IN)


def fast_fire_max(heavier: float = 1.0) -> fi.Firing:
    model = fast_fire_model(heavier)
    return fi.fire(model, fi.MaxFire(), 6 * HOUR, (CONE_10,), CONE_10_FAST)


@cache
def fast_fire_log() -> fi.Firing:
    pts = tuple((m * 60.0, c + 273.15) for m, c in LOG)
    return fi.fire(fast_fire_model(), fi.Schedule("setting", pts), LOG[-1][0] * 60.0, (CONE_10,))


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
