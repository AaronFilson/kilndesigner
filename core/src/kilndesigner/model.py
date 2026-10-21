"""The design file: what a kiln is, before anything is calculated.

A design is the user's intent: the chamber, the lining, the roof, the heat source and the site.
Everything derived from it (areas, heat loss, elements, geometry, plans) lives elsewhere and is
recalculated, never stored in the design. The YAML file, the API's JSON and the database's JSONB
document are all this model (ADR 0003, ADR 0006).
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from kilndesigner.units import (
    Q_,
    Current,
    EnergyPrice,
    Length,
    Money,
    Power,
    Temperature,
    Voltage,
    VolumePrice,
)

SCHEMA_VERSION = 1

type Face = Literal["left", "right", "back", "front", "floor", "roof"]
type ElementWall = Literal["left", "right", "back", "front"]


class Spec(BaseModel):
    model_config = ConfigDict(
        extra="forbid", frozen=True, validate_default=True, populate_by_name=True
    )


class Layer(Spec):
    """One layer of a lining, from the hot face outwards."""

    material: str = Field(description="A material id from the library, for example 'ifb-k26'")
    thickness: Length


class Lining(Spec):
    """The layers of each face, hot face first. Unset faces use the walls' layers."""

    walls: list[Layer] = Field(min_length=1)
    floor: list[Layer] | None = Field(default=None, min_length=1)
    roof: list[Layer] | None = Field(default=None, min_length=1)
    door: list[Layer] | None = Field(default=None, min_length=1)

    def for_face(self, face: Face, *, door_face: Face | None = None) -> list[Layer]:
        if face == door_face and self.door is not None:
            return self.door
        if face == "floor" and self.floor is not None:
            return self.floor
        if face == "roof" and self.roof is not None:
            return self.roof
        return self.walls


class Chamber(Spec):
    """The inside of the kiln: the space the lining encloses."""

    width: Length = Field(description="Inside, side to side")
    depth: Length = Field(description="Inside, front to back")
    height: Length = Field(description="Inside, floor to the roof (to the springline of an arch)")


class FlatRoof(Spec):
    type: Literal["flat"] = "flat"


class SprungArch(Spec):
    """A circular arch springing from the side walls, spanning the chamber's width."""

    type: Literal["sprung_arch"] = "sprung_arch"
    rise: Length = Field(description="Height of the arch's inside above the springline")


type Roof = Annotated[FlatRoof | SprungArch, Field(discriminator="type")]


class Loading(Spec):
    type: Literal["front_door", "car"] = "front_door"


class Firing(Spec):
    """The hottest the kiln must reach: a cone, a temperature, or both (the temperature wins)."""

    cone: str | None = Field(default=None, description="An Orton cone, for example '10' or '06'")
    final_rate: Literal[60, 150] = Field(
        default=60, description="Heating rate at the end of the firing, °C per hour, for the cone"
    )
    top_temperature: Temperature | None = None

    @model_validator(mode="after")
    def _one_target(self) -> Firing:
        if self.cone is None and self.top_temperature is None:
            raise ValueError("give the firing a cone or a top_temperature")
        return self


class ElectricSupply(Spec):
    voltage: Voltage
    phase: Literal[1, 3] = 1
    breaker: Current = Field(description="The circuit breaker's rating")


class Electric(Spec):
    """Electric elements in grooves in the walls."""

    supply: ElectricSupply
    alloy: str = Field(default="kanthal-a1", description="An alloy id from the library")
    walls: list[ElementWall] = Field(default=["left", "right", "back"], min_length=1)
    elements: int | None = Field(
        default=None, ge=1, description="How many elements; chosen for you when left out"
    )
    power: Power | None = Field(
        default=None, description="The power to install; the circuit's continuous limit if unset"
    )


class Heat(Spec):
    electric: Electric | None = None

    @model_validator(mode="after")
    def _some_heat(self) -> Heat:
        if self.electric is None:
            raise ValueError("give the kiln a heat source")
        return self


class Shell(Spec):
    """The kiln's outside skin. Its finish sets how much heat it radiates."""

    finish: Literal["painted", "oxidised_steel", "rolled_steel_sheet"] = "oxidised_steel"


class Site(Spec):
    ambient: Temperature = Field(
        default_factory=lambda: Q_(70, "degF"), description="The air around the kiln"
    )
    coldest_ambient: Temperature | None = Field(
        default=None, description="The coldest air the kiln will be fired in"
    )
    electricity_price: EnergyPrice | None = None
    propane_price: VolumePrice | None = None
    materials_budget: Money | None = None


class Kiln(Spec):
    """A kiln design: everything the user decides, and nothing that is calculated."""

    schema_version: Literal[1] = Field(default=SCHEMA_VERSION, alias="schema")
    name: str = Field(min_length=1)
    units: Literal["us", "metric"] = Field(default="us", description="How results are shown")
    firing: Firing
    chamber: Chamber
    roof: Roof = Field(default_factory=FlatRoof)
    loading: Loading = Field(default_factory=Loading)
    lining: Lining
    shell: Shell = Field(default_factory=Shell)
    heat: Heat
    site: Site = Field(default_factory=Site)

    @property
    def door_face(self) -> Face | None:
        return "front" if self.loading.type == "front_door" else None
