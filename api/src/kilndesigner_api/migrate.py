"""Bring the database up to date: ``kilndesigner-migrate``, or :func:`upgrade` from code."""

from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config


def alembic_config(database_url: str | None = None) -> Config:
    config = Config()
    config.set_main_option("script_location", str(Path(__file__).parent / "migrations"))
    if database_url is not None:
        config.set_main_option("sqlalchemy.url", database_url)
    return config


def upgrade(database_url: str | None = None) -> None:
    command.upgrade(alembic_config(database_url), "head")


def main() -> None:
    upgrade()
