"""Fixtures for API tests against a real Postgres (see the root ``conftest.py``)."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

import httpx
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from kilndesigner_api import db
from kilndesigner_api.jobs import InlineRunner
from kilndesigner_api.main import create_app
from kilndesigner_api.settings import Settings

EXAMPLES = Path(__file__).parents[2] / "examples"


@pytest.fixture
async def sessions(database_url: str) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    """Sessions on a test database emptied once per test, before any fixture adds rows."""
    engine = db.make_engine(database_url)
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE design, design_version, build CASCADE"))
    yield db.make_sessions(engine)
    await engine.dispose()


@pytest.fixture
def runner(sessions: async_sessionmaker[AsyncSession], tmp_path: Path) -> InlineRunner:
    return InlineRunner(sessions, tmp_path)


@pytest.fixture
async def client(
    database_url: str, runner: InlineRunner, tmp_path: Path
) -> AsyncIterator[httpx.AsyncClient]:
    settings = Settings(database_url=database_url, data_dir=tmp_path, jobs="inline")
    app = create_app(settings, runner)
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(transport=httpx.ASGITransport(app), base_url="http://test") as c,
    ):
        yield c


@pytest.fixture
def example() -> str:
    return (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")


@pytest.fixture
async def older_schema_key(sessions: async_sessionmaker[AsyncSession]) -> str:
    """The build key of a version saved under an older schema. It no longer validates, so the app
    keeps it as it is, and a build of it fails."""
    key = "saved-under-schema-0"
    name = "A kiln saved under an older schema"
    async with sessions() as s:
        s.add(
            db.DesignVersion(
                design=db.Design(name=name),
                number=1,
                schema_version=0,
                document={"schema": 0, "name": name},
                source="schema: 0\n",
                build_key=key,
            )
        )
        await s.commit()
    return key
