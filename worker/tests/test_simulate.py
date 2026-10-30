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
from kilndesigner_worker.main import WorkerSettings, shutdown, simulate, startup

pytestmark = [pytest.mark.anyio, pytest.mark.db]

EXAMPLES = Path(__file__).parents[2] / "examples"


async def test_a_simulation_sent_through_valkey_is_run_by_the_worker(
    database_url: str, redis_url: str, tmp_path: Path
) -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    key = build_key(kiln)
    engine = db.make_engine(database_url)
    sessions = db.make_sessions(engine)
    async with sessions() as s:
        await s.execute(text("TRUNCATE design, design_version, build, simulation CASCADE"))
        s.add(
            db.DesignVersion(
                design=db.Design(name=kiln.name),
                number=1,
                schema_version=kiln.schema_version,
                document=design_document(kiln),
                source="",
                build_key=key,
            )
        )
        s.add(db.Simulation(key=key))
        await s.commit()

    runner = await ArqRunner.connect(redis_url)
    await runner._pool.flushdb()  # pyright: ignore[reportPrivateUsage]
    await runner.submit_simulation(key)
    await runner.close()
    settings = Settings(database_url=database_url, redis_url=redis_url, data_dir=tmp_path)
    worker = Worker(
        functions=[simulate],
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
    assert (worker.jobs_complete, worker.jobs_failed) == (1, 0)
    async with sessions() as s:
        done = await s.get_one(db.Simulation, key)
    assert done.status == db.BuildStatus.done, done.error
    assert (tmp_path / "simulations" / key / "walls.parquet").stat().st_size > 0
    await engine.dispose()
