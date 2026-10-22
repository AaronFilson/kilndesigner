"""Alembic's environment: runs migrations on the async engine."""

from __future__ import annotations

import asyncio

from alembic import context
from sqlalchemy.engine import Connection

from kilndesigner_api.db import Base, make_engine
from kilndesigner_api.settings import get_settings

config = context.config


def _url() -> str:
    return config.get_main_option("sqlalchemy.url") or get_settings().database_url


def _run(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=Base.metadata)
    with context.begin_transaction():
        context.run_migrations()


async def _online() -> None:
    engine = make_engine(_url())
    async with engine.connect() as connection:
        await connection.run_sync(_run)
    await engine.dispose()


if context.is_offline_mode():
    context.configure(url=_url(), target_metadata=Base.metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    asyncio.run(_online())
