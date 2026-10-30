"""The database: designs, their immutable versions, and builds (ADR 0006)."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    type_annotation_map = {  # noqa: RUF012 (SQLAlchemy reads this class attribute)
        datetime: DateTime(timezone=True),
        dict[str, Any]: JSONB,
        list[str]: JSONB,
    }


class Design(Base):
    """A design's identity. Its content lives in its versions."""

    __tablename__ = "design"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now())

    versions: Mapped[list[DesignVersion]] = relationship(
        back_populates="design",
        order_by="DesignVersion.number",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class DesignVersion(Base):
    """One saved state of a design. Never updated: saving adds a version."""

    __tablename__ = "design_version"
    __table_args__ = (UniqueConstraint("design_id", "number"),)

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    design_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("design.id", ondelete="CASCADE"))
    number: Mapped[int]
    schema_version: Mapped[int]
    document: Mapped[dict[str, Any]]
    """The design as JSON: the same shape as the YAML file."""
    source: Mapped[str] = mapped_column(Text)
    """The YAML as written, comments and all."""
    build_key: Mapped[str] = mapped_column(String(64), index=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    design: Mapped[Design] = relationship(back_populates="versions")


class BuildStatus(StrEnum):
    queued = "queued"
    running = "running"
    done = "done"
    failed = "failed"


class Build(Base):
    """The files built from a design, shared by every version with the same build key."""

    __tablename__ = "build"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    status: Mapped[BuildStatus] = mapped_column(String(16), default=BuildStatus.queued)
    files: Mapped[list[str]] = mapped_column(default=list)
    notes: Mapped[list[str]] = mapped_column(default=list)
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    finished_at: Mapped[datetime | None]


class Simulation(Base):
    """A simulated firing of a design, by its build key. The results are Parquet files in the
    data folder; this row holds the run's status and its headline figures (ADR 0007)."""

    __tablename__ = "simulation"

    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    status: Mapped[BuildStatus] = mapped_column(String(16), default=BuildStatus.queued)
    summary: Mapped[dict[str, Any] | None] = mapped_column(JSONB)
    """Duration, energy, cost, whether the schedule was kept."""
    error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    finished_at: Mapped[datetime | None]


def make_engine(url: str) -> AsyncEngine:
    return create_async_engine(url, pool_pre_ping=True)


def make_sessions(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False)
