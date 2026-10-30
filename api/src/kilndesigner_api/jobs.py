"""Where builds run: on the arq worker, or in the API process (ADR 0008)."""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Protocol

from arq import ArqRedis, create_pool
from arq.connections import RedisSettings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from kilndesigner_api.tasks import run_build


class JobRunner(Protocol):
    async def submit_build(self, key: str) -> None: ...

    async def close(self) -> None: ...


class ArqRunner:
    """Sends builds to the worker through Valkey."""

    def __init__(self, pool: ArqRedis) -> None:
        self._pool = pool

    @classmethod
    async def connect(cls, redis_url: str) -> ArqRunner:
        return cls(await create_pool(RedisSettings.from_dsn(redis_url)))

    async def submit_build(self, key: str) -> None:
        # The job id makes a repeated request for the same build a no-op while it is queued.
        await self._pool.enqueue_job("build", key, _job_id=f"build:{key}")

    async def close(self) -> None:
        await self._pool.aclose()


class InlineRunner:
    """Runs builds as tasks in the API process: for tests, and a one-process setup."""

    def __init__(self, sessions: async_sessionmaker[AsyncSession], data_dir: Path) -> None:
        self._sessions, self._data_dir = sessions, data_dir
        self._tasks: set[asyncio.Task[None]] = set()

    async def submit_build(self, key: str) -> None:
        task = asyncio.create_task(run_build(self._sessions, self._data_dir, key))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)

    async def wait(self) -> None:
        """Wait for every submitted build to finish."""
        while self._tasks:
            await asyncio.gather(*self._tasks)

    async def close(self) -> None:
        await self.wait()
