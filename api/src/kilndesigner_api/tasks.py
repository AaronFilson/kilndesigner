"""The build task, run by the worker (or in the API process when ``jobs`` is ``inline``).

A build is keyed by the design's build key, so it is idempotent: building the same design twice
returns the first build's files (ADR 0008).
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

import anyio.to_thread
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from kilndesigner import Kiln
from kilndesigner.build import build_design, build_key
from kilndesigner_api.db import Build, BuildStatus, DesignVersion, Simulation, now


def build_dir(data_dir: Path, key: str) -> Path:
    return data_dir / "builds" / key


async def refresh_build_keys(sessions: async_sessionmaker[AsyncSession]) -> int:
    """Re-key every saved version for the engine running now, so that after an engine change a
    design is built afresh rather than shown with its old results. Returns how many changed."""
    changed = 0
    async with sessions() as session:
        for version in await session.scalars(select(DesignVersion)):
            try:
                key = build_key(Kiln.model_validate(version.document))
            except ValidationError:
                continue  # saved under an older schema; it keeps the key it had
            if key != version.build_key:
                version.build_key, changed = key, changed + 1
        await session.commit()
    return changed


def _build_files(document: dict[str, object], target: Path) -> tuple[list[str], list[str]]:
    """Build into a temporary folder, then move it into place, so a folder is never half-written."""
    target.parent.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(dir=target.parent, prefix=".tmp-"))
    try:
        result = build_design(Kiln.model_validate(document), scratch)
        if target.exists():
            shutil.rmtree(target)
        scratch.rename(target)
    except BaseException:
        shutil.rmtree(scratch, ignore_errors=True)
        raise
    return [p.relative_to(scratch).as_posix() for p in result.written], result.notes


def simulation_dir(data_dir: Path, key: str) -> Path:
    return data_dir / "simulations" / key


CHART_DT = 300.0  # s: the switch-over chart runs many firings, so it takes a coarser step


def _simulate_files(document: dict[str, object], target: Path) -> dict[str, object]:
    """Simulate into a temporary folder, then move it into place; the run's headline figures."""
    from kilndesigner.results import write_run
    from kilndesigner.simulation import simulate, switch_over_chart

    kiln = Kiln.model_validate(document)
    target.parent.mkdir(parents=True, exist_ok=True)
    scratch = Path(tempfile.mkdtemp(dir=target.parent, prefix=".tmp-"))
    try:
        run = simulate(kiln)
        write_run(run, scratch, run_id=target.name)
        chart = None
        site = kiln.site
        hybrid = kiln.heat.electric is not None and kiln.heat.gas is not None
        if (
            hybrid
            and kiln.heat.gas is not None
            and kiln.heat.gas.fuel == "propane"
            and site.electricity_price is not None
            and site.propane_price is not None
        ):
            chart = switch_over_chart(kiln, dt=CHART_DT)
            (scratch / "switchover.json").write_text(chart.model_dump_json(), encoding="utf-8")
        if target.exists():
            shutil.rmtree(target)
        scratch.rename(target)
    except BaseException:
        shutil.rmtree(scratch, ignore_errors=True)
        raise
    r = run.result
    return {
        "duration_h": r.duration_h,
        "held": r.held,
        "completed": r.completed,
        "energy_kwh": r.energy_kwh,
        "cost_usd": r.cost_usd,
        "switch_over_chart": chart is not None,
    }


async def run_simulation(
    sessions: async_sessionmaker[AsyncSession], data_dir: Path, key: str
) -> None:
    async with sessions() as session:
        sim = await session.get(Simulation, key)
        if sim is None or sim.status == BuildStatus.done:
            return
        document = await session.scalar(
            select(DesignVersion.document).where(DesignVersion.build_key == key).limit(1)
        )
        sim.status = BuildStatus.running
        await session.commit()
    try:
        if document is None:
            raise LookupError(f"no design version has the build key {key}")
        summary = await anyio.to_thread.run_sync(
            _simulate_files, document, simulation_dir(data_dir, key)
        )
    except Exception as e:  # recorded on the run and shown to the user, as a build's is
        async with sessions() as session:
            sim = await session.get_one(Simulation, key)
            sim.status, sim.error, sim.finished_at = BuildStatus.failed, str(e), now()
            await session.commit()
        return
    async with sessions() as session:
        sim = await session.get_one(Simulation, key)
        sim.status, sim.summary, sim.error, sim.finished_at = BuildStatus.done, summary, None, now()
        await session.commit()


async def run_build(sessions: async_sessionmaker[AsyncSession], data_dir: Path, key: str) -> None:
    async with sessions() as session:
        build = await session.get(Build, key)
        if build is None or build.status == BuildStatus.done:
            return
        document = await session.scalar(
            select(DesignVersion.document).where(DesignVersion.build_key == key).limit(1)
        )
        build.status = BuildStatus.running
        await session.commit()

    try:
        if document is None:
            raise LookupError(f"no design version has the build key {key}")
        files, notes = await anyio.to_thread.run_sync(
            _build_files, document, build_dir(data_dir, key)
        )
    except Exception as e:  # any failure is recorded on the build and shown to the user
        async with sessions() as session:
            build = await session.get_one(Build, key)
            build.status, build.error, build.finished_at = BuildStatus.failed, str(e), now()
            await session.commit()
        return

    async with sessions() as session:
        build = await session.get_one(Build, key)
        build.status, build.files, build.notes = BuildStatus.done, files, notes
        build.error, build.finished_at = None, now()
        await session.commit()
