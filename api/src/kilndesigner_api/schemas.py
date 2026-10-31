"""What the API accepts and returns. The OpenAPI document and the web client come from here."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, model_validator

from kilndesigner_api.db import BuildStatus


class DesignInput(BaseModel):
    """A design to save: as YAML (the file, or the YAML tab) or as a JSON document (the forms)."""

    source: str | None = None
    document: dict[str, Any] | None = None

    @model_validator(mode="after")
    def _exactly_one(self) -> Self:
        if (self.source is None) == (self.document is None):
            raise ValueError("send either `source` (YAML) or `document` (JSON), not both")
        return self


class Problem(BaseModel):
    """One reason a design is not valid, with where it is in the document."""

    loc: list[str | int]
    msg: str


class InvalidDesign(BaseModel):
    detail: list[Problem]


class VersionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    number: int
    build_key: str
    created_at: datetime


class Version(VersionSummary):
    schema_version: int
    document: dict[str, Any]
    source: str


class DesignSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    created_at: datetime
    updated_at: datetime


class Design(DesignSummary):
    versions: list[VersionSummary]
    latest: Version


class Build(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    key: str
    status: BuildStatus
    files: list[str]
    notes: list[str]
    error: str | None
    created_at: datetime
    finished_at: datetime | None


class Simulation(BaseModel):
    """A simulated firing's status. When done, its results are under /simulations/{key}/…"""

    model_config = ConfigDict(from_attributes=True)

    key: str
    status: BuildStatus
    summary: dict[str, Any] | None
    error: str | None
    created_at: datetime
    finished_at: datetime | None


class SlowFiringRequest(BaseModel):
    """A slow firing to work out: its time and the soak at the top within it, each a quantity
    with its unit ("72 h", "5 day")."""

    time: str
    soak: str = "0 h"


class CheckedDesign(BaseModel):
    """A valid design, both ways: the JSON document the forms edit and the YAML the tab shows."""

    document: dict[str, Any]
    source: str


class Template(BaseModel):
    """A kind of kiln to start a design from."""

    id: str
    title: str
    description: str
    document: dict[str, Any]
    source: str


class LibraryMaterial(BaseModel):
    id: str
    name: str
    kind: str
    max_service: str | None
    density: str


class LibraryEntry(BaseModel):
    id: str
    name: str


class LibraryIngredient(BaseModel):
    id: str
    name: str
    role: str
    needs_density: bool  # no sourced density: the mix must give one


class Library(BaseModel):
    """What a design can choose from: materials, element alloys, cones, burners and what a
    castable can be mixed from."""

    materials: list[LibraryMaterial]
    ingredients: list[LibraryIngredient]
    alloys: list[LibraryEntry]
    cones: list[str]
    cone_rates: dict[str, list[int]]
    burners: list[LibraryEntry]
