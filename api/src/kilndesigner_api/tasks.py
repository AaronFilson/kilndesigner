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
from kilndesigner_api.db import Build, BuildStatus, DesignVersion, now


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
    return [p.name for p in result.written], result.notes


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
