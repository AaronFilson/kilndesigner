"""The reference library: materials and element alloys, loaded from cited data files."""

from __future__ import annotations

import itertools
from functools import cache
from importlib import resources
from typing import Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field

from kilndesigner.thermal.conductivity import Conductivity
from kilndesigner.units import Q_, Length, Quantity, parse_quantity, si


class _Entry(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)


class ConductivityData(_Entry):
    unit: str
    temperature_unit: str
    points: list[tuple[float, float]] = Field(min_length=1)

    def to_conductivity(self) -> Conductivity:
        """k(T) in SI: kelvin to W/(m·K)."""
        temps = [si(Q_(t, self.temperature_unit), "K") for t, _ in self.points]
        ks = [si(Q_(k, self.unit), "W/(m*K)") for _, k in self.points]
        return Conductivity(tuple(temps), tuple(ks))


class SpecificHeatData(_Entry):
    """c_p at temperatures, held at the end values beyond them; with its own source."""

    unit: str
    temperature_unit: str
    points: list[tuple[float, float]] = Field(min_length=1)
    source: str
    status: Literal["verified", "excerpt", "derived"]

    def to_points(self) -> tuple[tuple[float, ...], tuple[float, ...]]:
        """(kelvin, J/(kg·K)) pairs, as two tuples."""
        temps = tuple(si(Q_(t, self.temperature_unit), "K") for t, _ in self.points)
        values = tuple(si(Q_(c, self.unit), "J/(kg*K)") for _, c in self.points)
        return temps, values


class Material(_Entry):
    id: str
    name: str
    kind: Literal[
        "insulating_firebrick",
        "dense_firebrick",
        "fibre_blanket",
        "fibre_board",
        "insulating_castable",
        "dense_castable",
        "backup_insulation",
        "building_brick",
        "stone",
    ]
    density: str
    max_service: str | None  # None: no source gives one
    conductivity: ConductivityData
    source: str
    status: Literal["verified", "excerpt", "derived"]
    specific_heat: SpecificHeatData | None = None  # None: no source gives one
    # A castable's "material required" to place a unit volume, from its maker's sheet
    material_required: str | None = None

    @property
    def max_service_temperature(self) -> Quantity | None:
        if self.max_service is None:
            return None
        return parse_quantity(self.max_service, "[temperature]")

    @property
    def k(self) -> Conductivity:
        return self.conductivity.to_conductivity()


class Alloy(_Entry):
    id: str
    name: str
    resistivity_20c: str
    density: str
    max_temperature_air: str
    max_temperature_endothermic_gas: str
    ct: list[tuple[float, float]] = Field(min_length=2)
    source: str

    @property
    def resistivity(self) -> Quantity:
        return parse_quantity(self.resistivity_20c).to("ohm*mm**2/m")

    def temperature_factor(self, temperature: Quantity) -> float:
        """Kanthal's Ct at a wire temperature, interpolated linearly between the table's rows."""
        t = si(temperature, "degC")
        rows = self.ct
        if t <= rows[0][0]:
            return rows[0][1]
        for (t0, c0), (t1, c1) in itertools.pairwise(rows):
            if t <= t1:
                return c0 + (c1 - c0) * (t - t0) / (t1 - t0)
        return rows[-1][1]

    @property
    def max_air_temperature(self) -> Quantity:
        return parse_quantity(self.max_temperature_air, "[temperature]")

    @property
    def max_reducing_temperature(self) -> Quantity:
        """The hottest Kanthal allows the wire in CO- and H₂-rich (endothermic) gas."""
        return parse_quantity(self.max_temperature_endothermic_gas, "[temperature]")


class UnknownEntryError(KeyError):
    def __str__(self) -> str:
        return str(self.args[0])


def _load(name: str) -> list[Any]:
    text = resources.files("kilndesigner.data").joinpath(name).read_text(encoding="utf-8")
    data: list[Any] = yaml.safe_load(text)
    return data


@cache
def materials() -> dict[str, Material]:
    return {m.id: m for m in (Material.model_validate(e) for e in _load("materials.yaml"))}


@cache
def alloys() -> dict[str, Alloy]:
    return {a.id: a for a in (Alloy.model_validate(e) for e in _load("alloys.yaml"))}


def material(material_id: str) -> Material:
    try:
        return materials()[material_id]
    except KeyError:
        known = ", ".join(sorted(materials()))
        raise UnknownEntryError(f"no material {material_id!r}; the library has: {known}") from None


def alloy(alloy_id: str) -> Alloy:
    try:
        return alloys()[alloy_id]
    except KeyError:
        known = ", ".join(sorted(alloys()))
        raise UnknownEntryError(f"no alloy {alloy_id!r}; the library has: {known}") from None


def awg_diameter(gauge: int) -> Length:
    """American Wire Gauge diameter, from the ASTM B258 definition, to 4 significant figures.

    d = 0.127 mm × 92^((36 − n)/39) (electric-and-thermal.md §2).
    """
    d_mm = 0.127 * 92 ** ((36 - gauge) / 39)
    return Q_(float(f"{d_mm:.4g}"), "mm")
