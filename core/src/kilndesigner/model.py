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
    Angle,
    Current,
    Density,
    Duration,
    EnergyPrice,
    Flow,
    Length,
    Mass,
    MassPrice,
    Money,
    Power,
    Pressure,
    Rate,
    Share,
    SpecificHeat,
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
    specific_heat: SpecificHeat | None = Field(
        default=None,
        description=(
            "The material's specific heat, from its maker's sheet, for the firing simulation of a "
            "material the library has no sourced value for (castables, for one)"
        ),
    )


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

    shape: Literal["box", "round"] = Field(
        default="box",
        description=(
            "A box, or round: a cylinder, as bottle and many folk kilns are, whose width and "
            "depth are its diameter"
        ),
    )
    width: Length = Field(description="Inside, side to side (a round chamber's diameter)")
    depth: Length = Field(
        description="Inside, front to back (a round chamber's diameter); of one chamber in a row"
    )
    height: Length = Field(
        description=(
            "Inside, floor to the roof: to the springline of a sprung arch or a dome, to the crown "
            "of a catenary arch"
        )
    )
    chambers: int = Field(
        default=1,
        ge=1,
        description=(
            "Chambers of this size in a row, front to back, the gases passing from each into the "
            "next: a climbing or tandem kiln"
        ),
    )
    slope: Angle | None = Field(
        default=None,
        description=(
            "How steeply the floor climbs from the firing end to the flue end: a climbing kiln, "
            "an anagama or a tunnel kiln, as an angle (a 20 % slope is atan 0.2 = 11.3 degree)"
        ),
    )
    bend: Angle | None = Field(
        default=None,
        description=(
            "How far the run turns in plan, from the firing end to the flue end, for a kiln built "
            "round a hillside or a corner: a box chamber's centreline on a circular arc, turning "
            "left as you look from the firing end. Only its drawing changes: a section swept "
            "along an arc has the same inside area and volume as along a straight line of the "
            "same length (Pappus's theorems), so the heat loss is worked out as for a straight run"
        ),
    )
    on_ground: bool = Field(
        default=False,
        description=(
            "The floor is built on the ground or a foundation, as most wood kilns are, not raised "
            "on a stand with air under it. Its loss goes into dry soil, worked out at steady state"
        ),
    )
    rings: Literal["mortar", "cut", "featheredge", "arch"] | None = Field(
        default=None,
        description=(
            "How a round wall's 4½ in brick rings are turned: 'mortar', straights with their "
            "inside faces on the curve and the wedge-shaped joints behind filled with mortar "
            "(Olsen, The Kiln Book, 4th ed., Fig. 2-13, p.45); 'cut', straights cut to the angle, "
            "the norm in electric kilns; 'featheredge', straights with featheredges among them; "
            "'arch', arch bricks, possible but not recommended (p.45). Left out: 'cut' for an "
            "electric kiln, 'mortar' otherwise"
        ),
    )

    @model_validator(mode="after")
    def _a_shape_it_can_be(self) -> Chamber:
        if self.shape == "round" and abs(si(self.width, "in") - si(self.depth, "in")) > 1e-6:
            raise ValueError("a round chamber's width and depth are both its diameter")
        if self.shape == "round" and self.chambers > 1:
            raise ValueError("chambers in a row are boxes; a round kiln is one chamber")
        if self.slope is not None:
            if f"{self.slope.units}" not in ("degree", "radian"):
                raise ValueError(
                    "give the slope as an angle, for example '11.3 degree': a slope in percent is "
                    "the rise over the run, and 20 % is atan(0.2) = 11.3 degree"
                )
            if not 0 <= si(self.slope, "degree") < 60:
                raise ValueError("a floor's slope must be from 0 to under 60 degrees")
        if self.bend is not None:
            if f"{self.bend.units}" not in ("degree", "radian"):
                raise ValueError("give the bend as an angle, for example '45 degree'")
            if not 0 <= si(self.bend, "degree") <= 180:
                raise ValueError("a run's bend must be from 0 to 180 degrees")
            if self.shape == "round" and si(self.bend, "degree") > 0:
                raise ValueError("a round chamber has no run to bend")
        return self

    @property
    def length(self) -> Length:
        """The whole run, front to back, of the chambers in a row (their walls between left out)."""
        return self.depth * self.chambers


BUTTRESSED = (
    "The roof's thrust is carried by masonry, not steel: thick or battered walls, buttresses, or "
    "the earth of a hillside or a mound (Olsen, 4th ed. p.53, Fig. 2-35B; p.186). No steel is "
    "sized"
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
    buttressed: bool = Field(default=False, description=BUTTRESSED)
    tube: bool = Field(
        default=False,
        description=(
            "Chambers in a row under one vault: the arch spans the width and runs the whole "
            "length, as a tube kiln's, 'an anagama extended' (Olsen, 4th ed. p.85), the walls "
            "between the chambers standing under it. Left out, each chamber in a row has its own "
            "arch spanning along the draft, as Olsen's climbing kilns' do (p.94–95)"
        ),
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
    buttressed: bool = Field(default=False, description=BUTTRESSED)


class Dome(Spec):
    """A dome on all four walls: a sphere through the chamber's top corners, rising above the
    springline at the centre (a sail dome, combustion-and-masonry.md §6.7)."""

    type: Literal["dome"] = "dome"
    rise: Length = Field(description="Height of the dome's inside above the springline, mid-dome")
    buttressed: bool = Field(default=False, description=BUTTRESSED)
    ring: int = Field(
        default=1,
        ge=1,
        description=(
            "How many of the roof's layers, from the inside, make the dome's shell. Layers laid "
            "over it, such as insulation, are only its load"
        ),
    )


class OpenTop(Spec):
    """No built roof: the setting is covered with shards or broken ware for each firing, as in
    folk updraft kilns (Olsen, 4th ed. p.152–157). Its heat loss isn't worked out."""

    type: Literal["open"] = "open"


type Roof = Annotated[
    FlatRoof | SprungArch | CatenaryArch | Dome | OpenTop, Field(discriminator="type")
]


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


class Ramp(Spec):
    """One segment of a firing schedule: heat (or cool) at a rate to a temperature, then hold."""

    to: Temperature
    rate: Rate | None = Field(
        default=None,
        description="Per hour, for example '200 delta_degF/hour'. Left out: as fast as it can",
    )
    hold: Duration | None = Field(default=None, description="How long to hold at ``to``")

    @model_validator(mode="after")
    def _a_rate(self) -> Ramp:
        if self.rate is not None and si(self.rate, "K/hour") <= 0:
            raise ValueError("a ramp's rate must be more than zero; its `to` sets the direction")
        if self.hold is not None and si(self.hold, "s") < 0:
            raise ValueError("a hold can't be negative")
        return self


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
    schedule: list[Ramp] | None = Field(
        default=None,
        min_length=1,
        description=(
            "The firing schedule, for the firing simulation. Left out: as fast as the heat allows "
            "to 100 °C below the top, then the final rate to the top"
        ),
    )
    ware: Mass | None = Field(
        default=None, description="Ware and kiln furniture set in the kiln, for the simulation"
    )

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
    rating: Power | None = Field(
        default=None,
        description=(
            "Each burner's input at the supply's pressure, from its maker or the plans, for a "
            "burner the library doesn't list: for example '36000 BTU/hr'. Give the count with it"
        ),
    )
    wall: WallFace | Literal["floor"] = Field(
        default="front",
        description=(
            "The wall the burners fire through, or the floor: an updraft's burners fire up through "
            "ports round the edge of the floor"
        ),
    )
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
        if self.wall == "floor" and self.places is not None:
            raise ValueError(
                "floor burners are spaced round the edge of the floor for you: give their count, "
                "not their places"
            )
        if self.rating is not None and self.wanted is None:
            raise ValueError("give the count of burners with their rating")
        if self.rating is not None and self.model is not None:
            raise ValueError(
                "give a burner model from the library, or a rating for one it doesn't list, not "
                "both"
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


class Line(Spec):
    """Gas piped to the kiln: natural gas from the meter, or propane from a large tank through
    its regulators. Nothing is vaporized at the kiln, so only the pressure matters."""

    type: Literal["line"] = "line"
    pressure: Pressure = Field(
        description="At the burners: for example '8 inch_H2O' for natural gas, or '2 psi'"
    )


type GasSupply = Annotated[Cylinders | Tank | Line, Field(discriminator="type")]


class Gas(Spec):
    fuel: Literal["propane", "natural_gas"] = "propane"
    burners: Burners = Field(default_factory=Burners)
    supply: GasSupply
    reduction: bool = Field(default=True, description="Whether the kiln is fired in reduction")
    firing_speed: Literal["fast", "slow"] = Field(
        default="slow",
        description=(
            "Burners sized for a slow firing (Olsen's 10,000 BTU per ft³ per hour for insulating "
            "brick, 16,000 for dense: the low end of Ward's range, about 8 hours in Olsen's IFB "
            "updraft) or a fast one (the high end of Ward's, about 6–7 hours)"
        ),
    )

    @model_validator(mode="after")
    def _a_supply_for_the_gas(self) -> Gas:
        if self.fuel == "natural_gas" and not isinstance(self.supply, Line):
            raise ValueError(
                "natural gas comes from a line: give the supply as a line, with its pressure"
            )
        return self


class Grate(Spec):
    """The grate the fuel burns on."""

    width: Length = Field(description="Across the firebox")
    length: Length = Field(description="Along the firebox, from its mouth")
    gap: Length | None = Field(default=None, description="The clear space between its bars")


class Firebox(Spec):
    """A firebox, where wood, coal or oil burns before the flame enters the chamber."""

    count: int = Field(default=1, ge=1, description="How many fireboxes of this size")
    position: Literal["front", "back", "left", "right", "under"] = Field(
        default="front",
        description="Against which wall, or under the chamber's floor",
    )
    width: Length = Field(description="Inside, across its mouth")
    length: Length = Field(description="Inside, from its mouth back")
    height: Length | None = Field(
        default=None, description="Inside, from the grate (or its floor) up to its roof"
    )
    grate: Grate | None = Field(
        default=None, description="Left out: the fuel burns on the firebox's floor"
    )
    ash_pit: Length | None = Field(
        default=None,
        description="From the grate down; left out with a grate, as deep as the firebox is tall "
        "above it, Olsen's grate at the vertical midpoint (The Kiln Book, 4th ed., p.199–200)",
    )
    step: Length | None = Field(
        default=None,
        description="From the grate up to the chamber floor beside it. Left out, 0 in: the grate "
        "level with the floor, the firebox part of the first chamber, as kilns fired for ash and "
        "flashing are; Olsen's 9–12 in drops smouldering coals into the front stacking (p.188)",
    )
    inlet: Port | None = Field(
        default=None, description="Each inlet flue from the firebox into the chamber"
    )
    inlets: int = Field(default=1, ge=1, description="How many inlet flues each firebox has")
    stoke_hole: Port | None = None


class Fire(Spec):
    """Wood, coal or oil, burned in fireboxes. The chimney draws the kiln (natural draft), unless
    a blower drives the burners (forced draft)."""

    fuel: Literal["wood", "coal", "oil"] = "wood"
    fireboxes: list[Firebox] = Field(min_length=1)
    forced: bool = Field(
        default=False, description="A blower drives the air, as forced-oil burners do"
    )
    oil_burners: int | None = Field(default=None, ge=1, description="Oil burners or drip units")
    oil_rate: Flow | None = Field(
        default=None, description="Each oil burner's flow at full fire, for example '2 gallon/hour'"
    )

    @model_validator(mode="after")
    def _oil_with_oil(self) -> Fire:
        if self.fuel != "oil" and (self.oil_burners is not None or self.oil_rate is not None):
            raise ValueError("oil burners and their rate are for oil firing")
        return self


class Heat(Spec):
    electric: Electric | None = None
    gas: Gas | None = None
    fire: Fire | None = Field(default=None, description="Wood, coal or oil in fireboxes")

    @model_validator(mode="after")
    def _some_heat(self) -> Heat:
        if self.electric is None and self.gas is None and self.fire is None:
            raise ValueError("give the kiln a heat source: electric, gas, a fire, or more than one")
        return self


class Section(Spec):
    """A flue's or a chimney's inside cross-section: round, by its diameter, or a rectangle, by its
    two sides."""

    diameter: Length | None = None
    width: Length | None = None
    depth: Length | None = None

    @model_validator(mode="after")
    def _one_shape(self) -> Section:
        sides = (self.width, self.depth)
        if self.diameter is not None and any(s is not None for s in sides):
            raise ValueError("give a section a diameter, or a width and a depth, not both")
        if self.diameter is None and any(s is None for s in sides):
            raise ValueError("give a section a diameter, or both a width and a depth")
        if any(si(s, "in") <= 0 for s in (self.diameter, *sides) if s is not None):
            raise ValueError("a section's sizes must be more than zero")
        return self

    def area_in2(self) -> float:
        """The inside area, in²."""
        if self.diameter is not None:
            return math.pi / 4 * si(self.diameter, "in") ** 2
        assert self.width is not None
        assert self.depth is not None
        return si(self.width, "in") * si(self.depth, "in")


class Chimney(Spec):
    """A chimney as built: how tall, and its inside section."""

    height: Length = Field(description="From the chamber floor to the chimney's top")
    inside: Section | None = Field(
        default=None, description="Inside, at the base. Left out: the size the engine works out"
    )
    top: Section | None = Field(
        default=None,
        description="Inside, at the top, for a chimney that tapers. Left out: as at the base",
    )


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
    chimney: Chimney | None = Field(
        default=None,
        description=(
            "The chimney as built, to check against Olsen's rules. Left out: the engine sizes it"
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
    elevation: Length | None = Field(
        default=None,
        description=(
            "The site's height above sea level. Thinner air weakens burners and draft (Olsen "
            "p.81, p.230). Left out: sea level"
        ),
    )
    electricity_price: EnergyPrice | None = None
    propane_price: VolumePrice | None = None
    materials_budget: Money | None = None


class Allowances(Spec):
    """What is bought over the count in the kiln, for breakage, spills and mistakes. Left out, each
    takes its sourced default (docs/research/brick-waste.md); give your own from experience."""

    brick: Share | None = Field(
        default=None,
        description="Over the bricks counted, whole and cut. Left out: 5 % (BIA Technical Note 10)",
    )
    shaped: Share | None = Field(
        default=None,
        description="Over the arch and wedge bricks counted. Left out: 5 %, as for straights",
    )
    castable: Share | None = Field(
        default=None,
        description=(
            "Over the castable a lining needs, bought or mixed. Left out: 5 % (PCO Refractories "
            "application instructions, 10 % or more in hard conditions)"
        ),
    )
    sheet: Share | None = Field(
        default=None,
        description="Over the blanket and board area. Left out: none, as no source gives one",
    )

    @model_validator(mode="after")
    def _between_none_and_all(self) -> Allowances:
        for name in ("brick", "shaped", "castable", "sheet"):
            value = getattr(self, name)
            if value is not None and not 0 <= si(value, "") < 1:
                raise ValueError(f"the {name} allowance must be at least 0 % and under 100 %")
        return self


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
    allowances: Allowances = Field(
        default_factory=Allowances, description="What to buy over the count, for waste"
    )

    @model_validator(mode="after")
    def _mixes_named_once(self) -> Kiln:
        ids = [m.id for m in self.castables or []]
        if len(ids) != len(set(ids)):
            raise ValueError("each castable needs its own id")
        return self

    @model_validator(mode="after")
    def _a_roof_it_can_build(self) -> Kiln:
        powered = self.heat.gas is not None or self.heat.electric is not None
        if isinstance(self.roof, OpenTop) and powered:
            raise ValueError(
                "an open top's heat loss isn't worked out, so burners or elements can't be sized "
                "for it: fire it with wood, coal or oil, or give it a roof"
            )
        if self.chamber.shape == "round":
            if isinstance(self.roof, SprungArch | CatenaryArch):
                raise ValueError("a round chamber takes a dome or a flat roof, not an arch")
            if self.heat.electric is not None and self.chamber.rings not in (None, "cut"):
                raise ValueError(
                    "elements in a round kiln are designed only in a faceted wall, straights cut "
                    "to the angle (chamber.rings: cut), as electric kilns are built; not in a "
                    "curved one"
                )
            if isinstance(self.roof, Dome):
                rise, radius = si(self.roof.rise, "in"), si(self.chamber.width, "in") / 2
                if not 0 < rise <= radius:
                    raise ValueError(
                        "a round chamber's dome must rise more than 0 and at most its radius, "
                        f"{radius:g} in (a hemisphere)"
                    )
            return self
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
            walls: list[tuple[str, str]] = [("the door or car", self.loading.face)]
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
        return "hinged" if self.heat.gas is None and self.heat.fire is None else "bricked"
