"""Fixtures shared by the API and worker tests: Postgres and Valkey from the compose file.

Set ``KILNDESIGNER_TEST_DATABASE_URL`` and ``KILNDESIGNER_TEST_REDIS_URL`` to choose them (CI
does). Without them, the tests use the local compose services, and skip if they are not running.
"""

from __future__ import annotations

import asyncio
import os

import pytest

DEFAULT_DATABASE_URL = (
    "postgresql+asyncpg://kilndesigner:kilndesigner@127.0.0.1:5432/kilndesigner_test"
)
DEFAULT_REDIS_URL = "redis://127.0.0.1:6379/15"  # not localhost: see Settings


async def _create_database(url: str) -> None:
    import asyncpg  # pyright: ignore[reportMissingTypeStubs]
    from sqlalchemy.engine import make_url

    u = make_url(url)
    conn = await asyncpg.connect(
        user=u.username, password=u.password, host=u.host, port=u.port, database="postgres"
    )
    try:
        exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", u.database)
        if not exists:
            await conn.execute(f'CREATE DATABASE "{u.database}"')
    finally:
        await conn.close()


@pytest.fixture(scope="session")
def database_url() -> str:
    from kilndesigner_api.migrate import upgrade

    url = os.environ.get("KILNDESIGNER_TEST_DATABASE_URL")
    try:
        asyncio.run(_create_database(url or DEFAULT_DATABASE_URL))
    except OSError as e:
        if url:
            raise
        pytest.skip(f"no Postgres for the tests ({e}); run `docker compose up -d postgres`")
    upgrade(url or DEFAULT_DATABASE_URL)
    return url or DEFAULT_DATABASE_URL


@pytest.fixture(scope="session")
def redis_url() -> str:
    from redis import Redis
    from redis.exceptions import ConnectionError as RedisConnectionError

    url = os.environ.get("KILNDESIGNER_TEST_REDIS_URL")
    try:
        Redis.from_url(url or DEFAULT_REDIS_URL).ping()
    except RedisConnectionError as e:
        if url:
            raise
        pytest.skip(f"no Valkey for the tests ({e}); run `docker compose up -d valkey`")
    return url or DEFAULT_REDIS_URL


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"
