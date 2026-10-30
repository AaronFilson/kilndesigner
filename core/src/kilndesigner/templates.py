"""Kiln types to start a design from: each is a complete design that builds as it stands.

The templates are copies of design files in the repository's ``examples/`` folder (a test keeps
them the same), packaged so the app can offer them without the repository.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from importlib import resources

from kilndesigner.designfile import parse_design
from kilndesigner.model import Kiln


@dataclass(frozen=True)
class Template:
    id: str
    title: str
    description: str
    source: str  # the design file, YAML

    @property
    def kiln(self) -> Kiln:
        return parse_design(self.source)


TEMPLATES: tuple[tuple[str, str, str], ...] = (
    (
        "electric-front-loader",
        "Electric front-loader",
        "A brick box with a hinged door and elements in grooves, in a welded steel case.",
    ),
    (
        "gas-crossdraft",
        "Gas cross-draft",
        "Propane venturi burners at one end, the flue and chimney at the other, a sprung arch and "
        "a bricked-up door.",
    ),
    (
        "hybrid-crossdraft",
        "Hybrid cross-draft",
        "The gas cross-draft with elements for the slow early part of the firing, handing over "
        "to propane.",
    ),
    ("catenary-gas", "Catenary arch, gas", "An arch that springs from the floor, fired with gas."),
    ("dome-castable", "Dome down-draft", "A cast dome on four walls, a gas down-draft."),
    ("castable-test", "Castable test kiln", "A small gas kiln lined with a castable you mix."),
    (
        "round-electric",
        "Round electric",
        "A top-loader of 12 facets of 3 in brick cut to the angle, elements in grooves round the "
        "ring (the size of Skutt's KM-1227-3).",
    ),
    ("electric-car", "Electric car kiln", "Elements in a sprung-arch kiln loaded on a car."),
    ("gas-updraft", "Gas updraft", "Burners up through the floor, the flue in the roof."),
    (
        "gas-chambers",
        "Gas climbing kiln",
        "Three chambers up a slope, the gases passing from each into the next (Olsen).",
    ),
    (
        "wood-fast-fire",
        "Wood fast-fire",
        "Two fireboxes with grates either side, wood-fired (Olsen's fast-fire).",
    ),
    (
        "wood-two-chamber",
        "Wood, two chambers",
        "Two chambers in a row, each with its own firebox (Olsen).",
    ),
    ("anagama", "Anagama", "One long sloping tube, fired with wood from its lower end."),
    (
        "climbing",
        "Climbing chamber kiln",
        "Ten chambers up a slope, arches spanning along the draft (Kyoto type).",
    ),
    ("tunnel", "Tube kiln", "A long level tube in seven sections (Tamba)."),
    ("groundhog", "Groundhog", "A low wood kiln on the ground, its arch springing from the floor."),
    ("bottle", "Bottle kiln", "A round chamber under a dome, wood-fired (Breda)."),
    (
        "round-open-top",
        "Round open-top kiln",
        "A round folk updraft covered with shards each firing.",
    ),
    ("coal", "Coal down-draft", "Two coal fireboxes with grates (Kato, Tajimi)."),
    ("oil", "Oil drip", "Oil dripped onto a hot plate in the firebox (Olsen)."),
)


@cache
def templates() -> tuple[Template, ...]:
    folder = resources.files("kilndesigner.data").joinpath("templates")
    return tuple(
        Template(id, title, description, folder.joinpath(f"{id}.yaml").read_text(encoding="utf-8"))
        for id, title, description in TEMPLATES
    )
