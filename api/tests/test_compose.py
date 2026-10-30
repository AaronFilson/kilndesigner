"""The self-hosted app end to end, through nginx: save a design, build it on the worker, fetch it.

Needs a running ``docker compose up``; CI's compose job runs it as::

    docker compose up --detach --wait
    KILNDESIGNER_COMPOSE_URL=http://localhost:8080 uv run pytest -m compose
"""

import os
import time
from collections.abc import Iterator

import httpx
import pytest

pytestmark = pytest.mark.compose


@pytest.fixture
def app() -> Iterator[httpx.Client]:
    url = os.environ.get("KILNDESIGNER_COMPOSE_URL")
    if not url:
        pytest.skip("set KILNDESIGNER_COMPOSE_URL to test a running `docker compose up`")
    with httpx.Client(base_url=url, timeout=30) as client:
        yield client


def test_every_page_of_the_web_app_is_served(app: httpx.Client) -> None:
    page = app.get("/designs/new")
    assert page.status_code == 200
    assert '<div id="root">' in page.text


def test_a_design_is_saved_built_by_the_worker_and_fetched(app: httpx.Client, example: str) -> None:
    design = app.post("/api/designs", json={"source": example}).raise_for_status().json()
    try:
        key = design["latest"]["build_key"]
        app.post(f"/api/builds/{key}").raise_for_status()
        deadline = time.monotonic() + 300
        while (build := app.get(f"/api/builds/{key}").json())["status"] not in {"done", "failed"}:
            assert time.monotonic() < deadline, f"the build is still {build['status']}"
            time.sleep(1)
        assert build["status"] == "done", build["error"]
        assert {"report.json", "kiln.glb", "kiln.step", "plans.pdf"} <= set(build["files"])

        report = app.get(f"/api/builds/{key}/report").raise_for_status().json()
        assert report["electric"]["elements"]["count"] >= 1  # 2 now: an element runs two grooves
        assert app.get(f"/api/builds/{key}/files/kiln.glb").content[:4] == b"glTF"
        assert app.get(f"/api/builds/{key}/files/plans.pdf").content[:5] == b"%PDF-"
    finally:
        app.delete(f"/api/designs/{design['id']}")
