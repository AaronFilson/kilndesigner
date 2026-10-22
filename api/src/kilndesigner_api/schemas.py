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
