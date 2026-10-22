"""Fixtures for API tests against a real Postgres (see the root ``conftest.py``)."""

from __future__ import annotations

from collections.abc import AsyncIterator
from pathlib import Path

import httpx
import pytest
from sqlalchemy import text

from kilndesigner_api import db
from kilndesigner_api.jobs import InlineRunner
from kilndesigner_api.main import create_app
from kilndesigner_api.settings import Settings

EXAMPLES = Path(__file__).parents[2] / "examples"


@pytest.fixture
async def runner(database_url: str, tmp_path: Path) -> AsyncIterator[InlineRunner]:
    engine = db.make_engine(database_url)
    async with engine.begin() as conn:
        await conn.execute(text("TRUNCATE design, design_version, build CASCADE"))
    yield InlineRunner(db.make_sessions(engine), tmp_path)
    await engine.dispose()


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
