"""The design file: what a kiln is, before anything is calculated.

A design is the user's intent: the chamber, the lining, the roof, the heat source and the site.
Everything derived from it (areas, heat loss, elements, geometry, plans) lives elsewhere and is
recalculated, never stored in the design. The YAML file, the API's JSON and the database's JSONB
document are all this model (ADR 0003, ADR 0006).
"""

from __future__ import annotations

import math
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from kilndesigner import cones
from kilndesigner.units import (
    Q_,
    Current,
    Density,
    EnergyPrice,
    Length,
    Mass,
    MassPrice,
    Money,
    Power,
    SpringRate,
    Temperature,
    Voltage,
    VolumePrice,
    si,
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
    height: Length = Field(
        description=(
            "Inside, floor to the roof: to the springline of a sprung arch or a dome, to the crown "
            "of a catenary arch"
        )
    )


class FlatRoof(Spec):
    type: Literal["flat"] = "flat"


class SprungArch(Spec):
    """A circular arch springing from the side walls, spanning the chamber's width."""

    type: Literal["sprung_arch"] = "sprung_arch"
    rise: Length = Field(description="Height of the arch's inside above the springline")
    ring: int = Field(
        default=1,
        ge=1,
        description=(
            "How many of the roof's layers, from the inside, make the arch's ring. Layers laid "
            "over the ring, such as insulation, are only its load"
        ),
    )
    ties: Literal["rigid", "springs"] = Field(
        default="rigid",
        description=(
            "How the tie rods hold the arch: nutted tight to the frame (rigid), or through a "
            "compression spring at each end, so the frame gives as the arch grows hot"
        ),
    )
    spring_rate: SpringRate | None = Field(
        default=None,
        description="Each spring's rate, from its maker's listing, for example 283 lbf/in",
    )

    @model_validator(mode="after")
    def _springs_have_a_rate(self) -> SprungArch:
        if self.ties == "springs" and self.spring_rate is None:
            raise ValueError("springs on the tie rods need their spring_rate, from the listing")
        return self


class CatenaryArch(Spec):
    """A catenary arch springing from the floor, so that it is the side walls and the roof in one
    (combustion-and-masonry.md §6.6). The chamber's width is its span at the floor and its height
    is to the crown; the front and back walls close its ends."""

    type: Literal["catenary_arch"] = "catenary_arch"


class Dome(Spec):
    """A dome on all four walls: a sphere through the chamber's top corners, rising above the
    springline at the centre (a sail dome, combustion-and-masonry.md §6.7)."""

    type: Literal["dome"] = "dome"
    rise: Length = Field(description="Height of the dome's inside above the springline, mid-dome")
    ring: int = Field(
        default=1,
        ge=1,
        description=(
            "How many of the roof's layers, from the inside, make the dome's shell. Layers laid "
            "over it, such as insulation, are only its load"
        ),
    )


type Roof = Annotated[FlatRoof | SprungArch | CatenaryArch | Dome, Field(discriminator="type")]


type WallFace = Literal["left", "right", "back", "front"]


class Loading(Spec):
    """How ware goes in: through a door in one wall, or on a car that rolls out through it.

    On a car kiln the floor is the car's deck and the wall at ``face`` rides on the car.
    """

    type: Literal["door", "car"] = "door"
    face: WallFace = Field(default="front", description="The wall with the door, or the car's end")
    door: Literal["bricked", "hinged"] | None = Field(
        default=None,
        description=(
            "A door bricked up for each firing, or one hung on hinges. Left out: hinged on an "
            "electric kiln, bricked on a gas one"
        ),
    )
    car_hardware_cost: Money | None = Field(
        default=None,
        description="Wheels, rails, frame and seal for a car; no sourced prices exist for these",
    )


class Firing(Spec):
    """The hottest the kiln must reach: a cone, a temperature, or both (the temperature wins)."""

    cone: str | None = Field(default=None, description="An Orton cone, for example '10' or '06'")
    final_rate: Literal[60, 100, 150, 600] = Field(
        default=60,
        description=(
            "Heating rate at the end of the firing, °C per hour, for the cone. Cones 15 to 42 are "
            "tabulated at one rate each: 150, or 100 for cone 38 and 600 for cones 39 to 42"
        ),
    )
    top_temperature: Temperature | None = None

    @model_validator(mode="after")
    def _one_target(self) -> Firing:
        if self.cone is None and self.top_temperature is None:
            raise ValueError("give the firing a cone or a top_temperature")
        if self.cone is not None:
            cones.cone_rates(self.cone)  # refuses a cone that isn't in the table
            if self.top_temperature is None:
                cones.cone_temperature(self.cone, self.final_rate)  # refuses an untabulated pair
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
    off_above: Temperature | None = Field(
        default=None,
        description="In a hybrid kiln, the temperature where the elements hand over to gas",
    )


class Port(Spec):
    """The size of a hole through a wall: round, by its diameter, or a rectangle, by its width
    (across the wall) and height."""

    diameter: Length | None = None
    width: Length | None = None
    height: Length | None = None

    @model_validator(mode="after")
    def _one_shape(self) -> Port:
        sizes = [s for s in (self.diameter, self.width, self.height) if s is not None]
        if self.diameter is not None and (self.width is not None or self.height is not None):
            raise ValueError("give a port a diameter, or a width and a height, not both")
        if self.diameter is None and (self.width is None or self.height is None):
            raise ValueError("give a port a diameter, or both a width and a height")
        if any(si(s, "in") <= 0 for s in sizes):
            raise ValueError("a port's sizes must be more than zero")
        return self

    @property
    def round(self) -> bool:
        return self.diameter is not None

    def size_in(self) -> tuple[float, float]:
        """Width and height, inches (a round port's are its diameter)."""
        if self.diameter is not None:
            d = si(self.diameter, "in")
            return d, d
        assert self.width is not None
        assert self.height is not None
        return si(self.width, "in"), si(self.height, "in")


class Place(Spec):
    """Where a port goes on a wall."""

    wall: WallFace
    across: Length = Field(
        default_factory=lambda: Q_(0, "in"),
        description=(
            "From the middle of the wall to the port's centre: to your right, standing outside "
            "and facing the wall, or to your left when negative"
        ),
    )
    up: Length = Field(description="From the chamber floor up to the port's centre")


class Burners(Spec):
    type: Literal["venturi", "power"] = Field(
        default="venturi", description="Venturi (natural draft, no power) or power (blower)"
    )
    count: int | None = Field(default=None, ge=1, description="Chosen for you when left out")
    model: str | None = Field(default=None, description="For example 'GACO MR100'")
    wall: WallFace = Field(default="front", description="The wall the burners fire through")
    port: Port | None = Field(
        default=None,
        description="The burner ports' size. Left out: the size the burner's sources give",
    )
    up: Length | None = Field(
        default=None,
        description=(
            "From the floor up to the ports' centres. Left out: the ports' bottoms are one 2½ in "
            "course above the floor"
        ),
    )
    places: list[Place] | None = Field(
        default=None,
        min_length=1,
        description="Where each burner's port goes. Left out: spread evenly along the wall",
    )

    @model_validator(mode="after")
    def _a_place_each(self) -> Burners:
        if self.places is not None and self.count is not None and len(self.places) != self.count:
            raise ValueError(
                f"give a place for each of the {self.count} burners, not {len(self.places)}"
            )
        return self

    @property
    def wanted(self) -> int | None:
        """How many burners the design asks for: its count, or one for each place."""
        if self.count is not None:
            return self.count
        return len(self.places) if self.places is not None else None


class SpyHoles(Spec):
    """The spy holes, for watching the cones. Left out: three in the door."""

    count: int | None = Field(default=None, ge=0, le=12, description="Three when left out")
    port: Port | None = Field(
        default=None,
        description=(
            "Their size. Left out: 2¼ × 2½ in, a quarter brick, in a gas kiln; 1 in round in an "
            "electric one"
        ),
    )
    places: list[Place] | None = Field(
        default=None,
        description="Where each one goes. Left out: up the door, a little off centre",
    )

    @model_validator(mode="after")
    def _a_place_each(self) -> SpyHoles:
        if self.places is not None and self.count is not None and len(self.places) != self.count:
            raise ValueError(
                f"give a place for each of the {self.count} spy holes, not {len(self.places)}"
            )
        return self

    @property
    def wanted(self) -> int:
        if self.count is not None:
            return self.count
        return len(self.places) if self.places is not None else 3


class Cylinders(Spec):
    type: Literal["cylinders"] = "cylinders"
    count: int = Field(ge=1)
    size: Literal["100 lb"] = "100 lb"


class Tank(Spec):
    type: Literal["tank"] = "tank"
    gallons: Literal[120, 150, 250, 325, 500, 1000]


type PropaneSupply = Annotated[Cylinders | Tank, Field(discriminator="type")]


class Gas(Spec):
    fuel: Literal["propane"] = "propane"
    burners: Burners = Field(default_factory=Burners)
    supply: PropaneSupply
    reduction: bool = Field(default=True, description="Whether the kiln is fired in reduction")
    firing_speed: Literal["fast", "slow"] = Field(
        default="fast",
        description=(
            "Burners sized for a fast firing (about 6–7 hours, the high end of Ward's range) or "
            "a slow one (about 14–18 hours, the low end)"
        ),
    )


class Heat(Spec):
    electric: Electric | None = None
    gas: Gas | None = None

    @model_validator(mode="after")
    def _some_heat(self) -> Heat:
        if self.electric is None and self.gas is None:
            raise ValueError("give the kiln a heat source: electric, gas, or both")
        return self


class Draft(Spec):
    """How the flame travels through the kiln to the chimney."""

    type: Literal["cross", "down", "up"]
    flue_wall: WallFace = Field(default="back", description="Where the gases leave (cross-draft)")
    run_to_chimney: Length = Field(
        default_factory=lambda: Q_(9, "in"),
        description="From the outside of the flue wall to the chimney's base",
    )
    flue_port: Port | None = Field(
        default=None,
        description=(
            "The exit flue's size. Left out: Ward's area, a whole number of courses high, at the "
            "foot of the flue wall (or square, in the roof of an up-draft)"
        ),
    )
    flue_across: Length | None = Field(
        default=None,
        description=(
            "From the middle of the flue wall to the flue's centre, to your right facing the wall "
            "from outside; the chimney moves with it. Left out: in the middle"
        ),
    )

    @model_validator(mode="after")
    def _flue_in_a_wall(self) -> Draft:
        if self.type == "up" and self.flue_across is not None:
            raise ValueError("an up-draft's flue is in the roof, so it has no flue_across")
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


class MixPart(Spec):
    """One ingredient of a castable, by its mass in one batch."""

    ingredient: str = Field(description="An ingredient id from the library, for example 'kyanite'")
    mass: Mass = Field(description="How much goes into one batch")
    density: Density | None = Field(
        default=None,
        description=(
            "The ingredient's true (particle) density, for an ingredient whose density the "
            "library doesn't have"
        ),
    )
    price: MassPrice | None = Field(
        default=None, description="What it costs, for the materials list"
    )


class Measured(Spec):
    """What test pieces of the mix measured, after firing. These replace the estimates."""

    fired_density: Density | None = None
    linear_shrinkage: float | None = Field(
        default=None, ge=-5, le=20, description="Linear shrinkage after firing, % (negative grows)"
    )
    fired_to: Temperature | None = Field(default=None, description="The test pieces' firing")


class CastableMix(Spec):
    """A castable mixed by the builder: its recipe for one batch. A lining layer uses it by id."""

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]*$", description="How lining layers name it")
    name: str = Field(min_length=1)
    ingredients: list[MixPart] = Field(min_length=1)
    water: Mass = Field(description="Water added to one batch")
    foam: float | None = Field(
        default=None,
        ge=0,
        le=85,
        description="Air folded in as foam, % of the cast volume",
    )
    measured: Measured | None = None


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
    draft: Draft | None = None
    spy_holes: SpyHoles | None = None
    site: Site = Field(default_factory=Site)
    castables: list[CastableMix] | None = Field(
        default=None, min_length=1, description="Castables you mix yourself"
    )

    @model_validator(mode="after")
    def _mixes_named_once(self) -> Kiln:
        ids = [m.id for m in self.castables or []]
        if len(ids) != len(set(ids)):
            raise ValueError("each castable needs its own id")
        return self

    @model_validator(mode="after")
    def _a_roof_it_can_build(self) -> Kiln:
        if isinstance(self.roof, SprungArch):
            rise, span = si(self.roof.rise, "in"), si(self.chamber.width, "in")
            if not 0 < rise <= span / 2:
                raise ValueError(
                    "a sprung arch's rise must be more than 0 and at most half the chamber's "
                    f"width, {span / 2:g} in: past that it isn't a segment of a circle"
                )
            layers = len(self.lining.for_face("roof"))
            if self.roof.ring > layers:
                raise ValueError(
                    f"the arch's ring can't be {self.roof.ring} layers: the roof has {layers}"
                )
            # The arch's skewbacks stand on the side walls, and a door or car is a whole wall
            if self.loading.face in ("left", "right"):
                what = "the car" if self.loading.type == "car" else "the door"
                raise ValueError(
                    f"a sprung arch springs from the left and right walls, so {what} can't be "
                    f"the {self.loading.face} wall: nothing would carry the arch over it. Put it "
                    "in the front or back wall, under the arch's end"
                )
        if isinstance(self.roof, Dome):
            layers = len(self.lining.for_face("roof"))
            if self.roof.ring > layers:
                raise ValueError(
                    f"the dome's ring can't be {self.roof.ring} layers: the roof has {layers}"
                )
            rise = si(self.roof.rise, "in")
            corner = math.hypot(si(self.chamber.width, "in"), si(self.chamber.depth, "in")) / 2
            if not 0 < rise < corner:
                raise ValueError(
                    "a dome's rise must be more than 0 and less than half the chamber's diagonal, "
                    f"{corner:.1f} in, or it would bulge out past the walls"
                )
        if isinstance(self.roof, CatenaryArch):
            if self.heat.electric is not None:
                raise ValueError(
                    "elements in a catenary kiln aren't designed here, because its walls curve: "
                    "fire it with gas"
                )
            walls: list[tuple[str, WallFace]] = [("the door or car", self.loading.face)]
            gas = self.heat.gas
            if gas is not None:
                if gas.burners.places is None:
                    walls.append(("the burners", gas.burners.wall))
                for p in gas.burners.places or []:
                    walls.append(("a burner", p.wall))
            for p in (self.spy_holes.places if self.spy_holes else None) or []:
                walls.append(("a spy hole", p.wall))
            if self.draft is not None and self.draft.type != "up":
                walls.append(("the flue", self.draft.flue_wall))
            for what, wall in walls:
                if wall in ("left", "right"):
                    raise ValueError(
                        f"a catenary arch is its own side walls, so {what} can't go in the {wall} "
                        "wall: use the front or back wall"
                    )
        return self

    def castable(self, mix_id: str) -> CastableMix | None:
        return next((m for m in self.castables or [] if m.id == mix_id), None)

    @property
    def door_face(self) -> Face:
        return self.loading.face

    @property
    def door_kind(self) -> Literal["bricked", "hinged"] | None:
        """How the door is built, or None for a car kiln."""
        if self.loading.type == "car":
            return None
        if self.loading.door is not None:
            return self.loading.door
        return "hinged" if self.heat.gas is None else "bricked"
