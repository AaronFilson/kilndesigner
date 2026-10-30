"""Castables the builder mixes, from a batch recipe to what goes in the wall and how to fire it.

A mix is a list of ingredients by mass, water and, optionally, foam. From it:

- **Volumes and densities**, by conserving mass and volume: each ingredient fills its mass over
  its true density, water fills its own volume, and foam is air, a share of the cast volume. The
  dried and fired densities follow from what leaves: the water, the clay's water of
  crystallisation (its LOI) and the organics, which burn out.
- **Conductivity**, from the fired density, by a law fitted to nine published insulating
  firebricks (castables.md §6.3): k = a·(ρ/1000)ⁿ·(1 + s·(T − 400 °C)/1000 K). A power law in
  density is how foams and porous solids scale; the fit's error, and the density and temperature
  range it was fitted over, come with every result, and a mix outside that range is refused
  (ADR 0009). Maxwell–Eucken and Landauer effective-medium models were tried and fit worse.
- **What happens in the wall**, from the steady temperatures through each layer: where kyanite
  can turn to mullite, where quartz passes its inversion, where the organic binder is gone.
- **The first firing**: the water to boil off and the organics to burn, with the oxygen, air and
  heat that takes, against the kiln's own heat; and a dry-out schedule from a maker's.
- **Batches**: how many, and how much of each ingredient, for the layers that use the mix.

Measured values from fired test pieces (``measured``) replace the estimates.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from functools import cache
from importlib import resources
from typing import TYPE_CHECKING, Any, Literal

import numpy as np
import yaml
from pydantic import BaseModel, ConfigDict

from kilndesigner.castable_checks import (
    burnout_heat,
    cast_in_layers,
    dryout_reach,
    no_service_limit,
)
from kilndesigner.library import ConductivityData, Material, material
from kilndesigner.model import CastableMix, Kiln
from kilndesigner.units import Q_, parse_quantity, si
from kilndesigner.working import Finding, Step, length_text, show

if TYPE_CHECKING:
    from kilndesigner.heatloss import HeatLoss

SOURCE = "castables.md"
WATER_DENSITY = 1000.0  # kg/m³ at room temperature
O2_IN_AIR = 0.2095  # by volume (combustion-and-masonry.md §1.1 [S1])
GAS_CONSTANT = 8.314462618  # J/(mol·K)
GLUCAN_MOLAR_MASS = 0.16214  # kg/mol, the (C6H10O5) unit of starch, dextrin and cellulose
# Heats of combustion (castables.md §7 [S51], verified): starch 4.16, cellulose 4.15 kcal/g
HHV = {"dextrin": 4.16 * 4184e3, "cornstarch": 4.16 * 4184e3}
HHV_CELLULOSE = 4.15 * 4184e3  # J/kg
LATENT_HEAT = 2256.4e3  # J/kg at 100 °C (castables.md §8.1, NIST [S15])
STEAM_DENSITY = 0.598  # kg/m³, saturated vapour at 100 °C (same)
# Organics in air: mass loss from about 240 °C, all gone above about 550 °C (castables.md §7
# [S54], an excerpt for a starch-based filler)
BURNOUT = (240.0, 550.0)  # °C
BURNOUT_SOURCE = "castables.md §7 [S54] (excerpt)"
KYANITE_START, KYANITE_FULL = 1200.0, 1400.0  # °C (castables.md §2.2 [S19] [S2])
QUARTZ_INVERSION = 573.0  # °C, 0.45 % linear (castables.md §3 [S23], secondary)
# Mizzou's dry-out, as High Temp Tools gives it (castables.md §8.2 [S41], secondary)
DRYOUT_RAMP_F = 75.0  # °F/h
DRYOUT_HOLDS_F = (250.0, 500.0, 1000.0)
DRYOUT_HOLD_PER_IN = 0.5  # h per inch of thickness
DRYOUT_MAX_IN = 9.0  # "for one layer ≤ 9 in thick"
DRYOUT_SOURCE = "Mizzou dry-out via High Temp Tools; castables.md §8.2 [S41] (secondary)"
CURE_SOURCE = "Mizzou: 16–24 h above 60 °F, kept damp; castables.md §8.2 [S41] (secondary)"
STATUS_WORDS = {"verified": "source", "secondary": "secondary source", "excerpt": "search excerpt"}
WASTE = 0.10  # extra mixed for spills and what sticks to the tools: an assumption, not sourced
US_QUART = 0.946353e-3  # m³


def amount(value: Any, unit: str) -> str:
    """A quantity as a builder reads it: '1,066 lb', '27,600 ft³', '0.25 lb'."""
    q = value.to(unit)
    v = float(q.magnitude)
    text = f"{v:,.0f}" if abs(v) >= 100 else f"{v:.3g}"
    return f"{text} {q.units:~P}"


class CastableError(ValueError):
    """A mix the engine can't work out: an unknown ingredient, a missing density, a density
    outside the range its conductivity was checked over."""


class Ingredient(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    id: str
    name: str
    role: Literal["aggregate", "clay", "cement", "organic", "kyanite", "quartz", "lightweight"]
    density: str | None = None
    fired_density: str | None = None
    loi: float
    quartz: str | None = None  # free quartz in an ingredient that isn't itself quartz, e.g. a clay
    limit: str | None = None
    limit_note: str | None = None
    note: str | None = None
    source: str
    status: Literal["verified", "secondary", "excerpt"]


@cache
def ingredients() -> dict[str, Ingredient]:
    text = resources.files("kilndesigner.data").joinpath("ingredients.yaml").read_text("utf-8")
    data: list[Any] = yaml.safe_load(text)
    return {i.id: i for i in (Ingredient.model_validate(e) for e in data)}


# The conductivity law


@dataclass(frozen=True)
class ConductivityLaw:
    """k = a·(ρ/1000)ⁿ·(1 + s·(T − 673.15)/1000), W/(m·K), with ρ in kg/m³ and T in K."""

    a: float
    n: float
    s: float
    rms: float  # of the fit, as a fraction
    worst: float  # the worst error predicting a brick left out of the fit, as a fraction
    densities: tuple[float, float]  # kg/m³, the bricks' range
    temperatures: tuple[float, float]  # °C, the data's range
    bricks: int
    source: str

    def k(self, density: float, t_kelvin: float) -> float:
        return self.a * (density / 1000) ** self.n * (1 + self.s * (t_kelvin - 673.15) / 1000)


def _fit(data: list[tuple[float, float, float]]) -> tuple[float, float, float]:
    """Least squares on log k: log k = log a + n log ρ' + log(1 + s τ), linear but for s."""
    from scipy.optimize import least_squares

    rho = np.array([d[0] / 1000 for d in data])
    tau = np.array([(d[1] + 273.15 - 673.15) / 1000 for d in data])
    logk = np.log(np.array([d[2] for d in data]))

    def residuals(p: np.ndarray) -> np.ndarray:
        return np.log(p[0]) + p[1] * np.log(rho) + np.log1p(p[2] * tau) - logk

    fit = least_squares(residuals, [1.0, 1.0, 0.3], bounds=([1e-3, 0.1, -0.9], [100, 5, 5]))
    a, n, s = (float(v) for v in fit.x)
    return a, n, s


@cache
def conductivity_law() -> ConductivityLaw:
    text = resources.files("kilndesigner.data").joinpath("ifb_conductivity.yaml").read_text("utf-8")
    raw: dict[str, Any] = yaml.safe_load(text)
    bricks: dict[str, tuple[float, list[tuple[float, float]]]] = {
        name: (float(b["density"]), [(float(t), float(k)) for t, k in b["points"]])
        for name, b in raw["bricks"].items()
    }

    def rows(names: list[str]) -> list[tuple[float, float, float]]:
        return [(bricks[n][0], t, k) for n in names for t, k in bricks[n][1]]

    a, n, s = _fit(rows(list(bricks)))
    law = ConductivityLaw(a, n, s, 0, 0, (0, 0), (0, 0), len(bricks), raw["source"])
    errors = [math.log(law.k(rho, t + 273.15) / k) for rho, t, k in rows(list(bricks))]
    worst = 0.0
    for left in bricks:
        a2, n2, s2 = _fit(rows([b for b in bricks if b != left]))
        loo = ConductivityLaw(a2, n2, s2, 0, 0, (0, 0), (0, 0), 0, "")
        for rho, t, k in rows([left]):
            worst = max(worst, abs(math.expm1(math.log(loo.k(rho, t + 273.15) / k))))
    densities = [b[0] for b in bricks.values()]
    temps = [t for b in bricks.values() for t, _ in b[1]]
    return ConductivityLaw(
        a,
        n,
        s,
        rms=math.expm1(math.sqrt(sum(e * e for e in errors) / len(errors))),
        worst=worst,
        densities=(min(densities), max(densities)),
        temperatures=(min(temps), max(temps)),
        bricks=len(bricks),
        source=raw["source"],
    )


# The mix


class BatchLine(BaseModel):
    model_config = ConfigDict(frozen=True)

    ingredient: str
    name: str
    mass: str
    share: str  # of the dry mix
    volume: str
    source: str


class MixAnalysis(BaseModel):
    """A mix worked out: per batch, as cast, dried and fired."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    batch: list[BatchLine]
    dry_mass: str
    water: str
    water_share: str
    foam: str | None
    cast_volume: str  # one batch, as cast
    wet_density: str
    quart_weighs: str  # a level US quart of the wet mix
    dried_density: str
    fired_density: str
    porosity: str
    conductivity: list[str]
    service_limit: str | None
    sets: str  # "cement" or "dries"
    working: list[Step]
    findings: list[Finding]
    # In SI, for the other calculations
    cast_volume_m3: float
    dry_mass_kg: float
    water_kg: float
    fired_density_kg_m3: float
    organic_kg: float  # per batch
    organic_heat_j: float  # per batch
    cement_kg: float  # per batch


def _density(mix: CastableMix, part_index: int) -> tuple[float, float]:
    """True density as mixed and as fired (kg/m³) of one ingredient of the mix."""
    part = mix.ingredients[part_index]
    ing = ingredients()[part.ingredient]
    if part.density is not None:
        d = si(part.density, "kg/m**3")
        return d, d
    if ing.density is None:
        raise CastableError(
            f"{mix.id}: no density is sourced for {ing.name}. Give it in the mix "
            f"(density: …, from the maker's sheet)."
        )
    d = si(parse_quantity(ing.density), "kg/m**3")
    fired = si(parse_quantity(ing.fired_density), "kg/m**3") if ing.fired_density else d
    return d, fired


def analyse_mix(kiln: Kiln, mix: CastableMix) -> MixAnalysis:
    lib = ingredients()
    for p in mix.ingredients:
        if p.ingredient not in lib:
            known = ", ".join(sorted(lib))
            raise CastableError(
                f"{mix.id}: no ingredient {p.ingredient!r}; the library has: {known}"
            )
    masses = [si(p.mass, "kg") for p in mix.ingredients]
    dry = sum(masses)
    water = si(mix.water, "kg")
    densities = [_density(mix, i) for i in range(len(masses))]
    solid_volume = sum(m / d for m, (d, _) in zip(masses, densities, strict=True))
    water_volume = water / WATER_DENSITY
    air = (mix.foam or 0.0) / 100
    cast = (solid_volume + water_volume) / (1 - air)
    roles = [lib[p.ingredient].role for p in mix.ingredients]
    lois = [lib[p.ingredient].loi for p in mix.ingredients]
    fired_mass = sum(m * (1 - loi) for m, loi in zip(masses, lois, strict=True))
    fired_solid = sum(
        m * (1 - loi) / fd for m, loi, (_, fd) in zip(masses, lois, densities, strict=True)
    )
    measured = mix.measured
    shrink = (measured.linear_shrinkage or 0.0) / 100 if measured else 0.0
    fired_volume = cast * (1 - shrink) ** 3
    fired_density = fired_mass / fired_volume
    if measured and measured.fired_density is not None:
        fired_density = si(measured.fired_density, "kg/m**3")
    porosity = 1 - fired_solid / fired_volume
    working: list[Step] = []
    findings: list[Finding] = []
    lb = "lb"

    def mass_text(kg: float) -> str:
        return show(Q_(kg, "kg"), lb, 3)

    batch = [
        BatchLine(
            ingredient=p.ingredient,
            name=lib[p.ingredient].name,
            mass=mass_text(m),
            share=f"{100 * m / dry:.1f} %",
            volume=show(Q_(m / d, "m**3"), "L", 3),
            source=lib[p.ingredient].source
            + ("; density given in the mix" if p.density is not None else ""),
        )
        for p, m, (d, _) in zip(mix.ingredients, masses, densities, strict=True)
    ]
    working.append(
        Step(
            name="Solid volume in one batch",
            value=show(Q_(solid_volume, "m**3"), "L", 4),
            formula="Σ mass ÷ true density",
            inputs={b.name: f"{b.mass} → {b.volume}" for b in batch},
            reference=f"{SOURCE} §1 (densities)",
        )
    )
    working.append(
        Step(
            name="Cast volume of one batch",
            value=f"{show(Q_(cast, 'm**3'), 'ft**3', 3)} ({show(Q_(cast, 'm**3'), 'L', 3)})",
            formula="(solids + water) ÷ (1 − air from foam)",
            inputs={
                "water": show(Q_(water_volume, "m**3"), "L", 3),
                "air from foam": f"{100 * air:.0f} %",
            },
            note="Water taken as 1 kg/L.",
        )
    )
    wet = (dry + water) / cast
    working.append(
        Step(
            name="Wet density",
            value=f"{show(Q_(wet, 'kg/m**3'), 'lb/ft**3', 3)}",
            formula="(dry mix + water) ÷ cast volume",
            note="Weigh a level quart of each batch: this is the check that the foam is right.",
        )
    )
    dried = dry / cast
    working.append(
        Step(
            name="Dried density",
            value=show(Q_(dried, "kg/m**3"), "lb/ft**3", 3),
            formula="dry mix ÷ cast volume",
            note=(
                "No drying shrinkage is assumed. Water the cement binds stays in, so a mix with "
                "cement dries a little heavier."
            ),
        )
    )
    working.append(
        Step(
            name="Fired density",
            value=show(Q_(fired_density, "kg/m**3"), "lb/ft**3", 3),
            formula=(
                "measured on test pieces"
                if measured and measured.fired_density is not None
                else "Σ mass × (1 − LOI) ÷ (cast volume × (1 − shrinkage)³)"
            ),
            inputs={
                "linear shrinkage": f"{100 * shrink:.1f} %" + ("" if measured else " (assumed)")
            },
            reference=f"{SOURCE} §4 (LOI), §7 (organics burn out)",
        )
    )
    if porosity < 0:
        raise CastableError(
            f"{mix.id}: the fired mix would be denser than its solids; check the masses and "
            "densities."
        )
    working.append(
        Step(
            name="Porosity when fired",
            value=f"{100 * porosity:.0f} %",
            formula="1 − fired solids' volume ÷ fired volume",
            note="Solids fired: clay as metakaolin, kyanite as mullite and silica.",
        )
    )

    law = conductivity_law()
    lo, hi = law.densities
    if not lo <= fired_density <= hi:
        raise CastableError(
            f"{mix.id} fires to about {show(Q_(fired_density, 'kg/m**3'), 'lb/ft**3', 3)} "
            f"({fired_density:.0f} kg/m³). Its conductivity can only be estimated from "
            f"{lo:.0f} to {hi:.0f} kg/m³ ({show(Q_(lo, 'kg/m**3'), 'lb/ft**3', 3)} to "
            f"{show(Q_(hi, 'kg/m**3'), 'lb/ft**3', 3)}), the range of the firebricks it was fitted "
            "to. Change the foam or the recipe, or measure the fired density of test pieces."
        )
    btu_in = 0.144228  # W/(m·K) per BTU·in/(hr·ft²·°F)
    k_text = [
        f"{t} °F: {law.k(fired_density, si(Q_(t, 'degF'), 'K')) / btu_in:.2f} BTU·in/(hr·ft²·°F)"
        for t in (500, 1000, 1500, 2000)
    ]
    working.append(
        Step(
            name="Conductivity",
            value="; ".join(k_text),
            formula=f"k = {law.a:.3f}·(ρ/1000)^{law.n:.2f}·(1 + {law.s:.2f}·(T − 400 °C)/1000 K) "
            "W/(m·K)",
            inputs={
                "fired density": f"{fired_density:.0f} kg/m³",
                "fitted to": f"{law.bricks} insulating firebricks, {lo:.0f}–{hi:.0f} kg/m³, "
                f"{law.temperatures[0]:.0f}–{law.temperatures[1]:.0f} °C",
                "fit error": f"{100 * law.rms:.0f} % rms; up to {100 * law.worst:.0f} % for a "
                "brick left out of the fit",
            },
            reference=f"{law.source}",
            note="Fitted law, not measured: test pieces measured for conductivity would replace "
            "it.",
        )
    )
    findings.append(
        Finding(
            level="info",
            message=(
                f"{mix.name}: its conductivity is estimated from its fired density by a law "
                f"fitted to {law.bricks} commercial insulating firebricks. Expect it to be off by "
                f"up to about {100 * law.worst:.0f} %, and more if the mix's pores or solids "
                "differ from a firebrick's."
            ),
            reference=law.source,
        )
    )

    limits = [
        (si(parse_quantity(lib[p.ingredient].limit or ""), "K"), lib[p.ingredient])
        for p in mix.ingredients
        if lib[p.ingredient].limit
    ]
    limit = min(limits, key=lambda x: x[0]) if limits else None
    if limit is not None:
        working.append(
            Step(
                name="Service limit",
                value=show(Q_(limit[0], "K"), "degF"),
                inputs={"set by": limit[1].name, "why": limit[1].limit_note or ""},
                reference=limit[1].source,
            )
        )
    else:
        from kilndesigner.heatloss import top_temperature

        check = no_service_limit(
            mix.name,
            [lib[p.ingredient].name for p in mix.ingredients],
            si(top_temperature(kiln)[0], "degF"),
            f"{SOURCE} §4.1",
        )
        findings.append(
            Finding.failed(
                check.check(),
                message=(
                    f"{mix.name}: no source gives a service limit for this mix (Greenstripe's PCE, "
                    "for one, is not sourced). Fire test pieces past the kiln's top temperature "
                    "before trusting it at the hot face."
                ),
            )
        )
    for p in mix.ingredients:
        ing = lib[p.ingredient]
        if ing.status != "verified" and p.density is None:
            findings.append(
                Finding(
                    level="info",
                    message=(
                        f"{ing.name}: {ing.note} ({ing.status})."
                        if ing.note
                        else f"{ing.name}: its density comes from a {STATUS_WORDS[ing.status]}; "
                        "check it."
                    ),
                    reference=ing.source,
                )
            )
    cement = sum(m for m, r in zip(masses, roles, strict=True) if r == "cement")
    organic = sum(m for m, r in zip(masses, roles, strict=True) if r == "organic")
    heat = sum(
        m * HHV.get(p.ingredient, HHV_CELLULOSE)
        for p, m, r in zip(mix.ingredients, masses, roles, strict=True)
        if r == "organic"
    )
    if cement and water / cement > 0:
        findings.append(
            Finding(
                level="info",
                message=(
                    f"{mix.name}: {100 * water / dry:.0f} % water on the dry mix. Mizzou takes "
                    "about 9.5 % and never more than 11 %; conventional castables 8–15 %. More "
                    "water than the cement needs weakens it."
                ),
                reference=f"{SOURCE} §5.3 [S40] [S41]",
            )
        )
    quart = Q_(wet * US_QUART, "kg")
    return MixAnalysis(
        id=mix.id,
        name=mix.name,
        batch=batch,
        dry_mass=mass_text(dry),
        water=mass_text(water),
        water_share=f"{100 * water / dry:.1f} % of the dry mix",
        foam=f"{100 * air:.0f} % of the cast volume" if mix.foam else None,
        cast_volume=f"{show(Q_(cast, 'm**3'), 'ft**3', 3)} ({show(Q_(cast, 'm**3'), 'L', 3)})",
        wet_density=show(Q_(wet, "kg/m**3"), "lb/ft**3", 3),
        quart_weighs=f"{show(quart, lb, 3)} ({show(quart, 'g', 3)})",
        dried_density=show(Q_(dried, "kg/m**3"), "lb/ft**3", 3),
        fired_density=show(Q_(fired_density, "kg/m**3"), "lb/ft**3", 3),
        porosity=f"{100 * porosity:.0f} %",
        conductivity=k_text,
        service_limit=show(Q_(limit[0], "K"), "degF") if limit else None,
        sets="cement" if cement else "dries",
        working=working,
        findings=findings,
        cast_volume_m3=cast,
        dry_mass_kg=dry,
        water_kg=water,
        fired_density_kg_m3=fired_density,
        organic_kg=organic,
        organic_heat_j=heat,
        cement_kg=cement,
    )


@cache
def _analysis(kiln_json: str, mix_id: str) -> MixAnalysis:
    kiln = Kiln.model_validate_json(kiln_json)
    mix = kiln.castable(mix_id)
    assert mix is not None
    return analyse_mix(kiln, mix)


def mix_analysis(kiln: Kiln, mix: CastableMix) -> MixAnalysis:
    """The analysis of one of the design's mixes (worked out once per design)."""
    return _analysis(kiln.model_dump_json(by_alias=True), mix.id)


def mix_material(kiln: Kiln, mix: CastableMix) -> Material:
    """A mix as a lining material: its fired density's conductivity and its service limit."""
    a = mix_analysis(kiln, mix)
    law = conductivity_law()
    temps = [260.0, 540.0, 815.0, 1100.0, 1370.0]
    points = [(t, law.k(a.fired_density_kg_m3, t + 273.15)) for t in temps]
    return Material(
        id=mix.id,
        name=mix.name,
        kind="insulating_castable",
        density=f"{a.dry_mass_kg / a.cast_volume_m3:.6g} kg/m**3",
        max_service=None
        if a.service_limit is None
        else f"{si(parse_quantity(a.service_limit), 'degF'):.6g} degF",
        conductivity=ConductivityData(unit="W/(m*K)", temperature_unit="degC", points=points),
        source=f"your mix; conductivity from its fired density ({SOURCE} §6.3)",
        status="derived",
    )


def resolve_material(kiln: Kiln, material_id: str) -> Material:
    """A lining material: one of the design's own mixes, or one from the library."""
    mix = kiln.castable(material_id)
    if mix is not None:
        return mix_material(kiln, mix)
    return material(material_id)


# The mix in the kiln


class LayerUse(BaseModel):
    model_config = ConfigDict(frozen=True)

    face: str
    thickness: str
    hot_side: str
    cold_side: str
    notes: list[str]


class Segment(BaseModel):
    model_config = ConfigDict(frozen=True)

    to: str
    rate: str
    hold: str | None
    why: str


class IngredientTotal(BaseModel):
    model_config = ConfigDict(frozen=True)

    ingredient: str
    name: str
    amount: str
    amount_lb: float
    cost: float | None


class CastableReport(BaseModel):
    model_config = ConfigDict(frozen=True)

    mix: MixAnalysis
    placed: str
    batches: int
    totals: list[IngredientTotal]
    layers: list[LayerUse]
    first_firing: list[Step]
    schedule: list[Segment]
    schedule_hours: float | None
    steps: list[str]
    findings: list[Finding]


def _depth_at(m: Material, t_hot: float, t_cold: float, t: float, thickness: float) -> float:
    """How deep below a layer's hot face it is ``t`` (K), from the ∫k dT across a flat layer."""
    if t >= t_hot:
        return 0.0
    if t <= t_cold:
        return thickness
    k = m.k
    total = k.integral(t_cold, t_hot)
    return thickness * k.integral(t, t_hot) / total


def castable_reports(
    kiln: Kiln, loss: HeatLoss, heat_watts: float | None, placed_m3: dict[str, float]
) -> list[CastableReport]:
    """Each mix the lining uses: batches, the temperatures it sees, its first firing."""
    reports: list[CastableReport] = []
    # The kiln dries in one firing, so every mix gets one schedule, set by the thickest castable
    # section anywhere in the lining (HarbisonWalker: castables-minerals.md §5).
    mix_ids = {mix.id for mix in kiln.castables or []}
    lib = ingredients()
    # Only the mixes the lining uses set what the schedule says (a listed, unused mix doesn't)
    all_roles = {
        lib[p.ingredient].role
        for mix in kiln.castables or []
        if placed_m3.get(mix.id, 0.0)
        for p in mix.ingredients
    }
    burning = _burning_shares(kiln, loss)
    burnout: list[tuple[str, float, float, float]] = []  # name, J per batch, m³ burning, batch m³
    kiln_thickest = 0.0
    stacked: list[tuple[str, list[float]]] = []
    for face in loss.faces:
        cast = [
            si(parse_quantity(layer.thickness), "m")
            for layer in face.layers
            if layer.material in mix_ids
        ]
        kiln_thickest = max([kiln_thickest, *cast])
        if len(cast) > 1:
            stacked.append((face.face, cast))
    for mix in kiln.castables or []:
        a = mix_analysis(kiln, mix)
        m = mix_material(kiln, mix)
        lib = ingredients()
        roles = {lib[p.ingredient].role for p in mix.ingredients}
        findings: list[Finding] = list(a.findings)
        volume = placed_m3.get(mix.id, 0.0)
        batches = math.ceil(volume * (1 + WASTE) / a.cast_volume_m3 - 1e-9) if volume else 0
        totals: list[IngredientTotal] = []
        for p in mix.ingredients:
            kg = si(p.mass, "kg") * batches
            cost = None if p.price is None else si(p.price, "USD/kg") * kg
            totals.append(
                IngredientTotal(
                    ingredient=p.ingredient,
                    name=lib[p.ingredient].name,
                    amount=amount(Q_(kg, "kg"), "lb"),
                    amount_lb=si(Q_(kg, "kg"), "lb"),
                    cost=cost,
                )
            )
        if not volume:
            findings.append(Finding(level="info", message=f"{mix.name} is not used in the lining."))
        layers: list[LayerUse] = []
        thickest = 0.0
        for face in loss.faces:
            for layer in face.layers:
                if layer.material != mix.id:
                    continue
                th = si(parse_quantity(layer.thickness), "m")
                thickest = max(thickest, th)
                notes = _zone_notes(m, roles, layer.hot_side_k, layer.cold_side_k, th, mix)
                layers.append(
                    LayerUse(
                        face=face.face,
                        thickness=layer.thickness,
                        hot_side=layer.hot_side,
                        cold_side=layer.cold_side,
                        notes=notes,
                    )
                )
        burns = volume * burning.get(mix.id, 0.0)
        first, more = _first_firing(kiln, a, volume / a.cast_volume_m3, burns / a.cast_volume_m3)
        findings += more
        if a.organic_heat_j and burns:
            burnout.append((a.name, a.organic_heat_j, burns, a.cast_volume_m3))
        # Stacked castables get no schedule, as an over-9 in layer doesn't: HarbisonWalker says
        # multi-component linings need case-by-case evaluation (castables-minerals.md §5)
        schedule, hours, more = _schedule(
            kiln, kiln_thickest if thickest and not stacked else 0.0, all_roles
        )
        findings += more
        if stacked and volume:
            face, cast = max(stacked, key=lambda s: sum(s[1]))
            total = sum(cast)
            sheet = cast_in_layers(
                face, [t / 0.0254 for t in cast], kiln_thickest / 0.0254, "castables-minerals.md §5"
            )
            sheet.agrees("t_all", Q_(total, "m"))
            findings.append(
                Finding.failed(
                    sheet.check(),
                    message=(
                        f"The {face} wall has {total / 0.0254:.1f} in of castable in layers. "
                        "HarbisonWalker evaluates linings of several components case by case, "
                        "and the only sourced schedule covers a single layer, so no dry-out "
                        "schedule is given. Cast and fire each layer on its own, or get the "
                        "maker's schedule for the whole lining."
                    ),
                )
            )
        reports.append(
            CastableReport(
                mix=a,
                placed=f"{show(Q_(volume, 'm**3'), 'ft**3', 3)}" if volume else "none",
                batches=batches,
                totals=totals,
                layers=layers,
                first_firing=first,
                schedule=schedule,
                schedule_hours=hours,
                steps=_steps(a, roles, batches),
                findings=findings,
            )
        )
    if burnout:
        step, finding = _burnout_check(kiln, burnout, heat_watts)
        first_report = next(r for r in reports if r.mix.name == burnout[0][0])
        first_report.first_firing.append(step)
        if finding is not None:
            first_report.findings.append(finding)
    return reports


def _burning_shares(kiln: Kiln, loss: HeatLoss) -> dict[str, float]:
    """Each castable's share, by volume, that gets above the organics' burnout start: the part of
    each layer hotter than T_lo, weighted by the face's inside area × the layer's thickness."""
    mix_ids = {mix.id for mix in kiln.castables or []}
    hot: dict[str, float] = {}
    whole: dict[str, float] = {}
    for face in loss.faces:
        area = si(parse_quantity(face.inside_area), "m**2")
        for layer in face.layers:
            if layer.material not in mix_ids:
                continue
            th = si(parse_quantity(layer.thickness), "m")
            m = resolve_material(kiln, layer.material)
            depth = _depth_at(m, layer.hot_side_k, layer.cold_side_k, BURNOUT[0] + 273.15, th)
            whole[layer.material] = whole.get(layer.material, 0.0) + area * th
            hot[layer.material] = hot.get(layer.material, 0.0) + area * depth
    return {k: hot[k] / v for k, v in whole.items() if v}


def _burnout_check(
    kiln: Kiln, mixes: list[tuple[str, float, float, float]], installed_w: float | None
) -> tuple[Step, Finding | None]:
    """Every mix's organics together against the heat the kiln needs through the window."""
    from kilndesigner.heatloss import heat_loss

    need = heat_loss(kiln, inside=Q_(BURNOUT[1], "degC")).total_watts
    sheet = burnout_heat(
        mixes,
        BURNOUT,
        DRYOUT_RAMP_F,
        need,
        installed_w,
        (f"{SOURCE} §7 [S51] [S54]", BURNOUT_SOURCE, DRYOUT_SOURCE),
    )
    heat = sum(q * v / vb for _, q, v, vb in mixes)
    window = (BURNOUT[1] - BURNOUT[0]) * 1.8 / DRYOUT_RAMP_F
    rate = heat / (window * 3600)
    sheet.agrees("Q", Q_(heat, "J"))
    sheet.agrees("P_b", Q_(rate, "W"))
    inputs = {
        "mixes": ", ".join(name for name, *_ in mixes),
        "the kiln's loss at 1022 °F": show(Q_(need, "W"), "kW", 3),
    }
    if installed_w is not None:
        inputs["the kiln's installed heat"] = show(Q_(installed_w, "W"), "kW", 3)
    step = Step(
        name="Burnout heat, every mix, against what the schedule needs",
        value=f"{show(Q_(rate, 'W'), 'kW', 3)} against {show(Q_(need, 'W'), 'kW', 3)} "
        f"({rate / need:.1f}×)",
        formula="Σ heat of the organics above 464 °F ÷ the climb from 464 to 1022 °F at 75 °F/h; "
        "against the kiln's steady loss with the inside at 1022 °F",
        inputs=inputs,
        reference=f"{SOURCE} §7 [S51] [S54]; {BURNOUT_SOURCE}; {DRYOUT_SOURCE}",
        note="Only the castable that gets above 464 °F counts. The heat stored in the lining as "
        "it climbs is left out of the need, so this errs towards a warning.",
    )
    if (check := sheet.check()).status == "pass":
        return step, None
    return step, Finding.failed(
        check,
        message=(
            f"Burning out the organics releases about {show(Q_(rate, 'W'), 'kW', 3)} through "
            f"464–1022 °F, {rate / need:.1f} times the "
            f"{show(Q_(need, 'W'), 'kW', 3)} the kiln loses there. The controller can only "
            "switch off, so the kiln can run away. Hold longer through 464–1022 °F, vent hard, "
            "and watch it."
        ),
        reference=f"{SOURCE} §7 [S51] [S54]",
    )


def _zone_notes(
    m: Material, roles: set[str], hot: float, cold: float, thickness: float, mix: CastableMix
) -> list[str]:
    """What each temperature in the layer means for this mix."""
    notes: list[str] = []

    def depth(t_c: float) -> str:
        d = _depth_at(m, hot, cold, t_c + 273.15, thickness)
        return length_text(d * 1000, True)

    full = length_text(thickness * 1000, True)
    hot_c, cold_c = hot - 273.15, cold - 273.15
    if "organic" in roles:
        lo, hi = BURNOUT
        if hot_c < lo:
            notes.append(
                "The whole layer stays below 464 °F: the organics never burn out, and the binder "
                f"stays as it dried ({BURNOUT_SOURCE})."
            )
        else:
            gone = depth(hi) if hot_c > hi else "0 in"
            kept = thickness * 1000 - _depth_at(m, hot, cold, lo + 273.15, thickness) * 1000
            notes.append(
                f"The organics are gone from the hottest {gone} (above about 1022 °F) and stay in "
                f"the coolest {length_text(max(kept, 0.0), True)} (below about 464 °F). Where "
                "they're gone and the clay hasn't sintered, nothing binds the mix; the clay's "
                "sintering temperature isn't sourced, so test pieces must show it "
                f"({BURNOUT_SOURCE})."
            )
    if "kyanite" in roles:
        if hot_c < KYANITE_START:
            notes.append(
                f"Its hot side reaches {hot_c * 1.8 + 32:.0f} °F, below 2192 °F, where kyanite "
                "starts to turn to mullite. Here the kyanite never expands: it is only a grog "
                "(castables.md §2.2 [S19] [S2])."
            )
        else:
            part = depth(KYANITE_START)
            whole = depth(KYANITE_FULL) if hot_c > KYANITE_FULL else "none of it"
            notes.append(
                f"Kyanite starts to convert in the hottest {part} (above 2192 °F) and converts "
                f"fully in {whole} (above 2552 °F) (castables.md §2.2 [S19] [S2])."
            )
    lib = ingredients()
    carriers = [lib[p.ingredient] for p in mix.ingredients]
    in_clay = [f"{i.name} ({i.quartz} quartz)" for i in carriers if i.quartz and i.role != "quartz"]
    if ("quartz" in roles or in_clay) and cold_c < QUARTZ_INVERSION < hot_c:
        what = "The quartz" if "quartz" in roles else "The free quartz in " + ", ".join(in_clay)
        notes.append(
            f"{what} in the hottest {depth(QUARTZ_INVERSION)} passes its 1063 °F inversion "
            "every firing, growing about 0.45 % in length and shrinking back; sources differ on "
            "the size (castables.md §3 [S23]; castables-minerals.md §2)."
        )
    if not notes:
        notes.append(f"{full}, from {hot_c * 1.8 + 32:.0f} °F to {cold_c * 1.8 + 32:.0f} °F.")
    return notes


def _kyanite_bound(a: MixAnalysis, mix: CastableMix) -> float | None:
    """The most kyanite could grow the mix, linear, if every grain converted and no pore took it
    up: a third of its volume share times its own growth (from its densities)."""
    lib = ingredients()
    share = 0.0
    for p in mix.ingredients:
        ing = lib[p.ingredient]
        if ing.role == "kyanite" and ing.density and ing.fired_density:
            d0 = si(parse_quantity(ing.density), "kg/m**3")
            d1 = si(parse_quantity(ing.fired_density), "kg/m**3")
            share += si(p.mass, "kg") / d0 / a.cast_volume_m3 * (d0 / d1 - 1)
    return share / 3 if share else None


def _first_firing(
    kiln: Kiln, a: MixAnalysis, batches: float, burning: float
) -> tuple[list[Step], list[Finding]]:
    """The water and organics in the cast lining (``batches``' worth, as placed; ``burning``
    batches' worth of it gets above the organics' burnout start)."""
    steps: list[Step] = []
    findings: list[Finding] = []
    if not batches:
        return steps, findings
    water = a.water_kg * batches
    latent = water * LATENT_HEAT
    steps.append(
        Step(
            name="Water to drive off",
            value=f"{amount(Q_(water, 'kg'), 'lb')}; {amount(Q_(latent, 'J'), 'kWh')} to boil it",
            formula="water per batch × batches placed; × latent heat 2256 kJ/kg",
            inputs={"steam at 100 °C": amount(Q_(water / STEAM_DENSITY, "m**3"), "ft**3")},
            reference=f"{SOURCE} §8.1 [S15]",
            note=(
                "Some water stays bound in the cement until it is heated further."
                if a.cement_kg
                else None
            ),
        )
    )
    steps.append(
        Step(
            name="Steam pressure if water is trapped",
            value="15.5 bar (225 psia) at 392 °F; 39.8 bar (577 psia) at 482 °F",
            reference=f"{SOURCE} §8.1 [S15]",
            note="Why the holds must be long enough to dry the layer through before it gets hot.",
        )
    )
    organic = a.organic_kg * burning
    if a.organic_kg and not burning:
        findings.append(
            Finding(
                level="info",
                message=f"{a.name}: none of it gets above 464 °F, so its organics never burn out "
                "and give no heat in the first firing.",
                reference=BURNOUT_SOURCE,
            )
        )
    if organic:
        mol = organic / GLUCAN_MOLAR_MASS
        air_m3 = 6 * mol / O2_IN_AIR * GAS_CONSTANT * 293.15 / 101_325
        heat = a.organic_heat_j * burning
        steps.append(
            Step(
                name="Organics to burn out (the castable above 464 °F)",
                value=(
                    f"{amount(Q_(organic, 'kg'), 'lb')}, releasing {amount(Q_(heat, 'J'), 'kWh')} "
                    f"({amount(Q_(heat, 'J'), 'BTU')})"
                ),
                formula="(C₆H₁₀O₅)ₙ + 6n O₂ → 6n CO₂ + 5n H₂O; heat of combustion 4.15–4.16 kcal/g",
                inputs={
                    "oxygen": amount(Q_(6 * mol * 0.032, "kg"), "lb"),
                    "air, at 68 °F": amount(Q_(air_m3, "m**3"), "ft**3"),
                    "CO₂ made": amount(Q_(6 * mol * 0.04401, "kg"), "lb"),
                    "water made": amount(Q_(5 * mol * 0.018015, "kg"), "lb"),
                },
                reference=f"{SOURCE} §7 [S51]; air 20.95 % oxygen (combustion-and-masonry.md §1.1)",
                note="The (C₆H₁₀O₅)ₙ formula is standard chemistry; castables.md §7 still wants a "
                "cited page.",
            )
        )
        window = (BURNOUT[1] - BURNOUT[0]) * 1.8 / DRYOUT_RAMP_F  # h at the schedule's ramp
        rate = heat / (window * 3600)
        steps.append(
            Step(
                name="Burnout heat, spread over the window",
                value=f"{amount(Q_(rate, 'W'), 'kW')} for about {window:.1f} h",
                formula="heat ÷ (time to climb from 464 to 1022 °F at 75 °F/h)",
                inputs={"air needed": amount(Q_(air_m3 / window, "m**3/hour"), "ft**3/minute")},
                reference=BURNOUT_SOURCE,
                note="The holds stretch the window, which lowers the rate; a wall lagging the kiln "
                "does too.",
            )
        )
        findings.append(
            Finding(
                level="info",
                message=(
                    f"{a.name}: the organics burn out as smoke, CO and CO₂ through the first "
                    "firing. "
                    "Fire it outdoors or with the flue wide open, and keep the elements out of the "
                    "smoke if you can."
                ),
                reference=f"{SOURCE} §7",
            )
        )
    bound = _kyanite_bound(a, kiln.castable(a.id))  # type: ignore[arg-type]
    if bound is not None:
        steps.append(
            Step(
                name="Kyanite's growth, at most",
                value=f"{100 * bound:.2f} % in length",
                formula="⅓ × kyanite's share of the cast volume × (3.61 ÷ 3.03 − 1)",
                reference=f"{SOURCE} §1, §2.3 [S1] [S2]",
                note=(
                    "Only where it gets above 2192 °F, if every grain converts and no pore takes "
                    "the growth up. KMC measures 17–19 % in volume for the grain."
                ),
            )
        )
    return steps, findings


def _schedule(
    kiln: Kiln, thickest: float, roles: set[str]
) -> tuple[list[Segment], float | None, list[Finding]]:
    from kilndesigner.heatloss import top_temperature

    findings: list[Finding] = []
    inches = thickest / 0.0254
    if not thickest:
        return [], None, findings
    if (check := dryout_reach(inches, DRYOUT_MAX_IN, DRYOUT_SOURCE).check()).status != "pass":
        findings.append(
            Finding.failed(
                check,
                message=(
                    f"The thickest castable layer is {inches:.1f} in. The only sourced "
                    f"dry-out schedule covers a layer up to {DRYOUT_MAX_IN:g} in, so none is "
                    "given. Cast it thinner, or in layers fired one at a time."
                ),
            )
        )
        return [], None, findings
    hold = DRYOUT_HOLD_PER_IN * inches
    ambient = si(kiln.site.ambient, "degF")
    top = si(top_temperature(kiln)[0], "degF")
    segments: list[Segment] = []
    t, hours = ambient, 0.0
    whys = {
        250.0: "boil off the free water",
        500.0: "drive off bound water"
        + ("; the organics start to burn" if "organic" in roles else ""),
        1000.0: "the last bound water" + ("; burn out the organics" if "organic" in roles else ""),
    }
    for target in DRYOUT_HOLDS_F:
        hours += (target - t) / DRYOUT_RAMP_F + hold
        segments.append(
            Segment(
                to=f"{target:.0f} °F",
                rate=f"{DRYOUT_RAMP_F:.0f} °F/h",
                hold=f"{hold:.1f} h",
                why=whys[target],
            )
        )
        t = target
    hours += (top - t) / DRYOUT_RAMP_F
    segments.append(
        Segment(
            to=f"{top:.0f} °F",
            rate=f"{DRYOUT_RAMP_F:.0f} °F/h",
            hold=None,
            why="on to the top temperature",
        )
    )
    findings.append(
        Finding(
            level="info",
            message=(
                f"First firing: {DRYOUT_RAMP_F:.0f} °F/h with a {hold:.1f} h hold (½ h per inch "
                f"of the {inches:.1f} in layer) at 250, 500 and 1000 °F, about {hours:.0f} h in "
                "all. "
                "This is Mizzou's schedule; no source gives one for a burnout mix."
            ),
            reference=DRYOUT_SOURCE,
        )
    )
    return segments, hours, findings


def _steps(a: MixAnalysis, roles: set[str], batches: int) -> list[str]:
    steps = [
        f"Weigh one batch: {', '.join(f'{b.mass} {b.name}' for b in a.batch)}, and {a.water} of "
        f"water ({a.water_share}). {batches} batches cover the lining with 10 % to spare.",
        "Mix the dry ingredients first, then add the water and mix to an even paste.",
    ]
    if a.foam:
        steps.append(
            f"Fold in foam until the mix is {a.foam} air: a level US quart of it then weighs "
            f"{a.quart_weighs}. Weigh a quart from each batch and add foam or mix to correct it."
        )
    else:
        steps.append(f"Check each batch: a level US quart weighs {a.quart_weighs}.")
    steps.append("Cast it, and from the same batch cast test pieces to fire and measure.")
    if a.sets == "cement":
        steps.append(f"Cure it 16–24 h above 60 °F, covered or kept damp ({CURE_SOURCE}).")
    else:
        steps.append(
            "Nothing in this mix sets with water: it holds only by drying, and stays weak until "
            "it is fired. Keep it dry, and support it until then."
        )
    steps.append("Dry it out and fire it on the schedule below.")
    steps.append(
        "Fire test pieces to the kiln's top temperature, measure their fired density and "
        "shrinkage, and enter them under measured: they replace the estimates here."
    )
    return steps


__all__ = [
    "CastableError",
    "CastableReport",
    "MixAnalysis",
    "analyse_mix",
    "castable_reports",
    "conductivity_law",
    "ingredients",
    "mix_analysis",
    "mix_material",
    "resolve_material",
]
