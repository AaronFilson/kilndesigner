from pathlib import Path

import pytest
from arq.connections import RedisSettings
from arq.worker import Worker
from sqlalchemy import text

from kilndesigner import load_design
from kilndesigner.build import build_key, design_document
from kilndesigner_api import db
from kilndesigner_api.jobs import ArqRunner
from kilndesigner_api.settings import Settings
from kilndesigner_worker.main import WorkerSettings, build, shutdown, startup

pytestmark = [pytest.mark.anyio, pytest.mark.db, pytest.mark.geometry]

EXAMPLES = Path(__file__).parents[2] / "examples"


async def test_a_build_sent_through_valkey_is_built_by_the_worker(
    database_url: str, redis_url: str, tmp_path: Path
) -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    key = build_key(kiln)
    engine = db.make_engine(database_url)
    sessions = db.make_sessions(engine)
    async with sessions() as s:
        await s.execute(text("TRUNCATE design, design_version, build CASCADE"))
        design = db.Design(name=kiln.name)
        s.add(
            db.DesignVersion(
                design=design,
                number=1,
                schema_version=kiln.schema_version,
                document=design_document(kiln),
                source="",
                build_key=key,
            )
        )
        s.add(db.Build(key=key, files=[], notes=[]))
        await s.commit()

    runner = await ArqRunner.connect(redis_url)
    await runner._pool.flushdb()  # pyright: ignore[reportPrivateUsage]
    settings = Settings(database_url=database_url, redis_url=redis_url, data_dir=tmp_path)

    async def work() -> Worker:
        worker = Worker(
            functions=[build],
            on_startup=startup,
            on_shutdown=shutdown,
            redis_settings=RedisSettings.from_dsn(redis_url),
            ctx={"settings": settings},
            burst=True,
            poll_delay=0.1,
            keep_result=WorkerSettings.keep_result,
        )
        try:
            await worker.main()
        finally:
            await worker.close()
        return worker

    await runner.submit_build(key)
    await runner.submit_build(key)  # a repeat while queued is the same job
    worker = await work()
    assert (worker.jobs_complete, worker.jobs_failed) == (1, 0)

    async with sessions() as s:
        done = await s.get_one(db.Build, key)
    assert done.status == db.BuildStatus.done, done.error
    assert {"report.json", "kiln.glb", "plans.pdf"} <= set(done.files)
    assert (tmp_path / "builds" / key / "kiln.glb").stat().st_size > 0

    # A retry (after a failed build, say) must reach the worker again.
    await runner.submit_build(key)
    await runner.close()
    assert (await work()).jobs_complete == 1
    await engine.dispose()
