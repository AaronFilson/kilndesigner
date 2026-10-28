"""The build task and re-keying, run straight against the database and a data folder."""

import json
from pathlib import Path

import pytest
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from kilndesigner import load_design
from kilndesigner.build import build_key, design_document
from kilndesigner_api import db
from kilndesigner_api.tasks import build_dir, refresh_build_keys, run_build

pytestmark = [pytest.mark.anyio, pytest.mark.db]

EXAMPLE = Path(__file__).parents[2] / "examples" / "electric-front-loader.yaml"


async def _save(sessions: async_sessionmaker[AsyncSession], *, queue: bool) -> str:
    """Save the example as a design version, optionally with its build queued; its build key."""
    kiln = load_design(EXAMPLE)
    key = build_key(kiln)
    async with sessions() as s:
        s.add(
            db.DesignVersion(
                design=db.Design(name=kiln.name),
                number=1,
                schema_version=kiln.schema_version,
                document=design_document(kiln),
                source=EXAMPLE.read_text(encoding="utf-8"),
                build_key=key,
            )
        )
        if queue:
            s.add(db.Build(key=key, files=[], notes=[]))
        await s.commit()
    return key


async def _keys(sessions: async_sessionmaker[AsyncSession]) -> set[str]:
    async with sessions() as s:
        return set(await s.scalars(select(db.DesignVersion.build_key)))


async def test_rekeying_changes_only_keys_the_engine_would_now_make_differently(
    sessions: async_sessionmaker[AsyncSession],
    older_schema_key: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    current = await _save(sessions, queue=False)
    assert await refresh_build_keys(sessions) == 0
    assert await _keys(sessions) == {current, older_schema_key}

    monkeypatch.setattr("kilndesigner.build.engine_fingerprint", lambda: "changed code")
    assert await refresh_build_keys(sessions) == 1
    keys = await _keys(sessions)
    assert current not in keys
    assert older_schema_key in keys  # it can't be re-keyed, so it keeps the key it had


async def test_a_build_of_a_version_saved_under_an_older_schema_fails_and_writes_nothing(
    sessions: async_sessionmaker[AsyncSession], older_schema_key: str, tmp_path: Path
) -> None:
    async with sessions() as s:
        s.add(db.Build(key=older_schema_key, files=[], notes=[]))
        await s.commit()

    await run_build(sessions, tmp_path, older_schema_key)

    async with sessions() as s:
        build = await s.get_one(db.Build, older_schema_key)
    assert build.status == db.BuildStatus.failed
    assert build.error is not None
    assert "validation errors for Kiln" in build.error
    assert build.finished_at is not None
    assert build.files == []
    assert list((tmp_path / "builds").iterdir()) == []  # the scratch folder was cleared away


async def test_a_build_whose_design_was_deleted_while_it_waited_fails_with_why(
    sessions: async_sessionmaker[AsyncSession], tmp_path: Path
) -> None:
    key = await _save(sessions, queue=True)
    async with sessions() as s:
        await s.execute(delete(db.Design))
        await s.commit()

    await run_build(sessions, tmp_path, key)

    async with sessions() as s:
        build = await s.get_one(db.Build, key)
    assert build.status == db.BuildStatus.failed
    assert build.error == f"no design version has the build key {key}"
    assert build.finished_at is not None
    assert not build_dir(tmp_path, key).exists()


async def test_a_build_not_queued_or_already_done_is_left_as_it_is(
    sessions: async_sessionmaker[AsyncSession], tmp_path: Path
) -> None:
    await run_build(sessions, tmp_path, "never-queued")
    async with sessions() as s:
        assert await s.get(db.Build, "never-queued") is None

    key = await _save(sessions, queue=False)
    async with sessions() as s:
        s.add(db.Build(key=key, status=db.BuildStatus.done, files=["report.json"], notes=[]))
        await s.commit()
    await run_build(sessions, tmp_path, key)
    async with sessions() as s:
        build = await s.get_one(db.Build, key)
    assert (build.status, build.files, build.finished_at) == (
        db.BuildStatus.done,
        ["report.json"],
        None,
    )
    assert not (tmp_path / "builds").exists()


@pytest.mark.geometry
async def test_a_rebuild_replaces_the_old_folder_rather_than_mixing_into_it(
    sessions: async_sessionmaker[AsyncSession], tmp_path: Path
) -> None:
    key = await _save(sessions, queue=True)
    old = build_dir(tmp_path, key)
    old.mkdir(parents=True)
    (old / "stale.txt").write_text("from an earlier build", encoding="utf-8")
    (old / "report.json").write_text("{}", encoding="utf-8")

    await run_build(sessions, tmp_path, key)

    async with sessions() as s:
        build = await s.get_one(db.Build, key)
    assert build.status == db.BuildStatus.done, build.error
    assert {"report.json", "kiln.glb", "plans.pdf"} <= set(build.files)
    assert sorted(p.name for p in (tmp_path / "builds").iterdir()) == [key]  # no scratch left
    assert not (old / "stale.txt").exists()
    report = json.loads((old / "report.json").read_text(encoding="utf-8"))
    assert report["name"] == "Electric front-loader, cone 10"
    assert all((old / name).is_file() for name in build.files)
