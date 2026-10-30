"""``kilndesigner-migrate``: it brings the database the settings name up to date."""

import asyncio

import pytest
from alembic.script import ScriptDirectory
from sqlalchemy import URL, make_url, text
from sqlalchemy.ext.asyncio import create_async_engine

from kilndesigner_api.migrate import alembic_config, main
from kilndesigner_api.settings import get_settings

pytestmark = pytest.mark.db


async def _as_admin(url: URL, statement: str) -> None:
    engine = create_async_engine(url.set(database="postgres"), isolation_level="AUTOCOMMIT")
    async with engine.connect() as conn:
        await conn.execute(text(statement))
    await engine.dispose()


async def _tables_and_revision(url: URL) -> tuple[set[str], str]:
    engine = create_async_engine(url)
    async with engine.connect() as conn:
        tables = await conn.scalars(
            text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        )
        names = set(tables)
        revision = await conn.scalar(text("SELECT version_num FROM alembic_version"))
    await engine.dispose()
    return names, str(revision)


def test_the_migrate_command_creates_the_tables_in_the_database_the_settings_name(
    database_url: str,
) -> None:
    fresh = make_url(database_url)
    fresh = fresh.set(database=f"{fresh.database}_migrate")
    drop = f'DROP DATABASE IF EXISTS "{fresh.database}" WITH (FORCE)'
    asyncio.run(_as_admin(fresh, drop))
    asyncio.run(_as_admin(fresh, f'CREATE DATABASE "{fresh.database}"'))
    try:
        with pytest.MonkeyPatch.context() as env:
            env.setenv("KILNDESIGNER_DATABASE_URL", fresh.render_as_string(hide_password=False))
            get_settings.cache_clear()
            main()
        tables, revision = asyncio.run(_tables_and_revision(fresh))
    finally:
        get_settings.cache_clear()  # back to the settings without the variable
        asyncio.run(_as_admin(fresh, drop))

    assert {"design", "design_version", "build", "alembic_version"} <= tables
    assert revision == ScriptDirectory.from_config(alembic_config()).get_current_head()


def test_alembic_is_given_a_database_only_when_one_is_named() -> None:
    url = "postgresql+asyncpg://someone@db.example/kilns"
    assert alembic_config(url).get_main_option("sqlalchemy.url") == url
    assert alembic_config().get_main_option("sqlalchemy.url") is None  # env.py reads the settings
