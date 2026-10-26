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
)


@cache
def templates() -> tuple[Template, ...]:
    folder = resources.files("kilndesigner.data").joinpath("templates")
    return tuple(
        Template(id, title, description, folder.joinpath(f"{id}.yaml").read_text(encoding="utf-8"))
        for id, title, description in TEMPLATES
    )
