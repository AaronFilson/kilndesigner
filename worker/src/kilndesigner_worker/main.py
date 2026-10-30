"""The arq worker. Run it with ``arq kilndesigner_worker.main.WorkerSettings``."""

from __future__ import annotations

from typing import Any, ClassVar

from arq.connections import RedisSettings

from kilndesigner_api import db
from kilndesigner_api.settings import Settings, get_settings
from kilndesigner_api.tasks import run_build, run_simulation


async def startup(ctx: dict[str, Any]) -> None:
    settings: Settings = ctx.setdefault("settings", get_settings())
    ctx["engine"] = db.make_engine(settings.database_url)
    ctx["sessions"] = db.make_sessions(ctx["engine"])


async def shutdown(ctx: dict[str, Any]) -> None:
    await ctx["engine"].dispose()


async def build(ctx: dict[str, Any], key: str) -> None:
    await run_build(ctx["sessions"], ctx["settings"].data_dir, key)


async def simulate(ctx: dict[str, Any], key: str) -> None:
    await run_simulation(ctx["sessions"], ctx["settings"].data_dir, key)


class WorkerSettings:
    functions: ClassVar = [build, simulate]
    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(get_settings().redis_url)
    max_jobs = get_settings().worker_jobs
    job_timeout = 600
    """A build with plans takes seconds; a slow machine gets plenty of room."""
    keep_result = 0
    """Results live in Postgres. A kept result would also block a retry under the same job id."""
