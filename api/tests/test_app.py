"""How the app is put together: where its builds run, and the command that serves it."""

from pathlib import Path

import httpx
import pytest
import uvicorn
from arq import create_pool
from arq.connections import RedisSettings
from fastapi import FastAPI
from uvicorn.importer import import_from_string

from kilndesigner_api.jobs import ArqRunner, InlineRunner
from kilndesigner_api.main import create_app, run
from kilndesigner_api.settings import Settings


def _client(app: FastAPI) -> httpx.AsyncClient:
    return httpx.AsyncClient(transport=httpx.ASGITransport(app), base_url="http://test")


@pytest.mark.anyio
@pytest.mark.db
async def test_with_inline_jobs_the_app_runs_builds_in_its_own_process(
    database_url: str, older_schema_key: str, tmp_path: Path
) -> None:
    app = create_app(Settings(database_url=database_url, data_dir=tmp_path, jobs="inline"))
    async with app.router.lifespan_context(app), _client(app) as client:
        runner = app.state.runner
        assert isinstance(runner, InlineRunner)
        assert (await client.post(f"/api/builds/{older_schema_key}")).status_code == 202
        await runner.wait()
        build = (await client.get(f"/api/builds/{older_schema_key}")).json()
    assert build["status"] == "failed"  # it ran, here, and recorded why it failed
    assert "validation errors for Kiln" in build["error"]
    assert (tmp_path / "builds").is_dir()  # in the data folder the settings name


@pytest.mark.anyio
@pytest.mark.db
@pytest.mark.usefixtures("sessions")  # an empty database
async def test_with_arq_jobs_the_app_sends_builds_to_the_worker_through_valkey(
    database_url: str, redis_url: str, example: str, tmp_path: Path
) -> None:
    valkey = await create_pool(RedisSettings.from_dsn(redis_url))
    await valkey.flushdb()
    settings = Settings(
        database_url=database_url, redis_url=redis_url, data_dir=tmp_path, jobs="arq"
    )
    app = create_app(settings)
    try:
        async with app.router.lifespan_context(app), _client(app) as client:
            assert isinstance(app.state.runner, ArqRunner)
            design = (await client.post("/api/designs", json={"source": example})).json()
            key = design["latest"]["build_key"]
            queued = await client.post(f"/api/builds/{key}")
            assert queued.status_code == 202, queued.text
            assert queued.json()["status"] == "queued"
        jobs = await valkey.queued_jobs()
        assert [(j.function, j.args, j.job_id) for j in jobs] == [("build", (key,), f"build:{key}")]
        assert not (tmp_path / "builds").exists()  # nothing was built in the API process
    finally:
        await valkey.flushdb()
        await valkey.aclose()


def test_the_api_command_serves_the_app_factory_and_reloads_on_change(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[tuple[tuple[object, ...], dict[str, object]]] = []

    def serve(*args: object, **kwargs: object) -> None:
        calls.append((args, kwargs))

    monkeypatch.setattr(uvicorn, "run", serve)
    run()
    [(args, kwargs)] = calls
    assert args == ("kilndesigner_api.main:create_app",)
    assert kwargs == {"factory": True, "port": 8000, "reload": True}
    assert import_from_string(args[0]) is create_app
