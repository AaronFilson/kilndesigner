"""The hardware's checks as sheets (ADR 0013): a port on its wall, a burner in its port, the flue's
area, and what a hinged door is lined with.

Each sheet starts from the design's own numbers; :mod:`kilndesigner.hardware` decides its findings
from them.
"""

from __future__ import annotations

from dataclasses import dataclass

from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_

DESIGN = "the design"


@dataclass(frozen=True)
class Spot:
    """A port on a wall's inside face (in): across from the middle, up from the floor to its
    centre."""

    title: str
    across: float
    up: float
    width: float
    height: float


def port_fits(
    spot: Spot,
    wall: str,
    inside_width: float,
    inside_top: float,
    clash: Spot | None,
    lever: str,
) -> Sheet:
    """The port within its wall's inside face, and clear of ``clash``, the port it would overlap."""
    s = Sheet("hardware.port", f"{spot.title} on the {wall} wall")
    s.given("w", "the port's width", Q_(spot.width, "in"), source=f"{DESIGN}: its size")
    s.given("h", "the port's height", Q_(spot.height, "in"), source=f"{DESIGN}: its size")
    s.given(
        "a",
        "across, from the middle of the wall to its centre",
        Q_(spot.across, "in"),
        source=f"{DESIGN}: where it is",
    )
    s.given(
        "z", "up, from the floor to its centre", Q_(spot.up, "in"), source=f"{DESIGN}: where it is"
    )
    s.given(
        "W", f"the {wall} wall's width, inside", Q_(inside_width, "in"), source="the chamber's size"
    )
    s.given(
        "z_top",
        "the inside top of the wall over the port",
        Q_(inside_top, "in"),
        source="the chamber's shape: the roof's lowest over the port's sides and middle",
    )
    s.let("x_side", "the port's far side, out from the middle of the wall", "abs(a) + w/2", "in")
    s.let("x_wall", "the wall's inside edge, out from its middle", "W/2", "in")
    s.let("z_min", "the lowest centre that keeps the port above the floor", "h/2", "in")
    s.let("z_high", "the port's top", "z + h/2", "in")
    s.require("x_side", "<=", "x_wall")
    s.require("z", ">=", "z_min")
    s.require("z_high", "<=", "z_top")
    if clash is not None:
        name = clash.title.lower()
        s.given("a_2", f"{name}: across", Q_(clash.across, "in"), source=DESIGN)
        s.given("z_2", f"{name}: up", Q_(clash.up, "in"), source=DESIGN)
        s.given("w_2", f"{name}: width", Q_(clash.width, "in"), source=DESIGN)
        s.given("h_2", f"{name}: height", Q_(clash.height, "in"), source=DESIGN)
        s.let(
            "q",
            "the larger of the two spacings, as a share of the spacing at which they'd "
            "touch: 1 or more and the ports miss",
            "max(abs(a - a_2)/((w + w_2)/2), abs(z - z_2)/((h + h_2)/2))",
        )
        s.given("q_min", "spacing at which they touch", 1.0)
        s.require("q", ">=", "q_min")
    if lever == "z":
        s.lever("z", Q_(spot.height / 2, "in"), Q_(inside_top - spot.height / 2, "in"))
    else:
        edge = (inside_width - spot.width) / 2
        s.lever("a", Q_(-edge, "in"), Q_(edge, "in"))
    return s


OLSEN_PORT = (
    "Olsen, The Kiln Book, 4th ed., p.173 and Fig. 6-67: ports 2½–2¾ in for a 2½ in tip, the tip "
    "at least ¼ in below the floor; Fig. 5-82: burner ports = burner tip size"
)


def burner_in_port(model: str, head: float, across: float, head_source: str) -> Sheet:
    """The port at least as wide as the burner's head: Olsen sizes ports to the tip, set back
    from the port so secondary air comes in round it; Ward's inch of room round a head set within
    the port is a note, not a requirement."""
    s = Sheet("hardware.burner-port", f"A {model} in its port", reference=OLSEN_PORT)
    s.given("d", f"the {model}'s head", Q_(head, "in"), source=head_source)
    s.given(
        "w",
        "the port, across its narrower side",
        Q_(across, "in"),
        source=f"{DESIGN}: the burners' port",
    )
    s.require("w", ">=", "d", level="error")
    s.lever("w", Q_(0.5, "in"), Q_(24, "in"))
    return s


def unsized_burner_port(model: str) -> Sheet:
    s = Sheet(
        "hardware.burner-port-size", f"The port for a {model}", reference="kiln-hardware.md §1.4"
    )
    s.fact("burner", model, source=f"{DESIGN}: the burners")
    s.fact("its head's size", "not in any source read", source="kiln-hardware.md §1.4")
    s.rule(
        "A burner's port is sized from its head, an inch wider (Ward); without the head's size "
        "no port can be drawn.",
        holds=False,
        level="warning",
    )
    return s


@dataclass(frozen=True)
class FlueNeed:
    """What Olsen's three ways of sizing an exit flue start from (4th ed. p.236): the burner ports
    together (when their size is known), the chamber's volume and the burners' input."""

    inlet_in2: float | None
    volume_ft3: float
    input_btu_hr: float
    source: str


def flue_area(need: FlueNeed, width: float, height: float, round_: bool, under: float) -> Sheet:
    """The exit flue against the smallest of Olsen's three starting sizes, "slightly under"
    allowed: a flue smaller than all of them is outside his practice, and the gases back up."""
    s = Sheet("hardware.flue", "The flue port's area", reference=need.source)
    terms: list[str] = []
    if need.inlet_in2 is not None:
        s.given(
            "A_1",
            "method 1: the burner ports together",
            Q_(need.inlet_in2, "in**2"),
            source="the burners and their ports",
        )
        terms.append("A_1")
    s.given("V", "the chamber's volume", Q_(need.volume_ft3, "ft**3"), source="the chamber's shape")
    s.given("a_v", "method 2: flue per cubic foot", Q_(2.5, "in**2/ft**3"), source=f"{need.source}")
    s.let("A_2", "method 2", "a_v*V", "in**2")
    s.given(
        "P",
        "the burners' input at full fire",
        Q_(need.input_btu_hr, "BTU/hr"),
        source="working: Burners",
    )
    s.given("b", "method 3: input per square inch", Q_(7000, "BTU/hr/in**2"), source=need.source)
    s.let("A_3", "method 3", "P/b", "in**2")
    terms += ["A_2", "A_3"]
    s.let("A_least", "the smallest of Olsen's starting sizes", f"min({', '.join(terms)})", "in**2")
    s.given(
        "k",
        "slightly under, as Olsen builds small updrafts",
        under,
        source="Olsen, 4th ed. p.174: the Olsen 24 kit's 45 in² exit against 50 in² of inlets",
    )
    s.let("A_min", "the smallest exit that passes", "k*A_least", "in**2")
    s.given(
        "w",
        "the port's width" if not round_ else "the port's diameter",
        Q_(width, "in"),
        source=f"{DESIGN}: draft.flue_port",
    )
    if round_:
        s.let("A_p", "the port's area", "pi/4*w^2", "in**2")
    else:
        s.given("h", "the port's height", Q_(height, "in"), source=f"{DESIGN}: draft.flue_port")
        s.let("A_p", "the port's area", "w*h", "in**2")
    s.require("A_p", ">=", "A_min", level="warning")
    s.lever("w", Q_(1, "in"), Q_(60, "in"))
    return s


@dataclass(frozen=True)
class DoorLayer:
    name: str
    density: float  # lb/ft³
    thickness: float  # in


def door_lining(layers: list[DoorLayer], dense: list[str], source: str) -> Sheet:
    s = Sheet("hardware.door-lining", "What the hinged door is lined with", reference=source)
    for i, x in enumerate(layers, 1):
        s.given(f"t_{i}", f"layer {i}, {x.name}", Q_(x.thickness, "in"), source=DESIGN)
        s.given(
            f"ρ_{i}",
            f"{x.name}, weight per cubic foot",
            Q_(x.density, "lbf/ft**3"),
            source="the material's data sheet",
        )
    terms = " + ".join(f"ρ_{i}*t_{i}" for i in range(1, len(layers) + 1))
    s.let("q", "the door's weight per square foot of its face", terms, "lbf/ft**2")
    for name in dense:
        s.fact("dense", name, source="the material's kind")
    s.rule(
        "Pitelka's hinged door, which the frame and hinges follow, holds one 4½ in layer of "
        "insulating brick; a door with dense brick or castable needs them checked for its "
        "weight.",
        holds=False,
        level="warning",
    )
    return s


__all__ = [
    "DoorLayer",
    "FlueNeed",
    "Spot",
    "burner_in_port",
    "door_lining",
    "flue_area",
    "port_fits",
    "unsized_burner_port",
]
