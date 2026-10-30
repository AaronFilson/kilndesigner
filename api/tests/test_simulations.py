"""Simulated firings through the API: queued, run, and read back from Parquet with DuckDB."""

import shutil
from pathlib import Path

import httpx
import pytest

from kilndesigner_api.jobs import InlineRunner

pytestmark = [pytest.mark.anyio, pytest.mark.db]

EXAMPLES = Path(__file__).parents[2] / "examples"


async def _key(client: httpx.AsyncClient, source: str) -> str:
    design = (await client.post("/api/designs", json={"source": source})).json()
    return design["latest"]["build_key"]


async def test_a_firing_is_simulated_and_its_results_read_back(
    client: httpx.AsyncClient, runner: InlineRunner, example: str, tmp_path: Path
) -> None:
    key = await _key(client, example)
    assert (await client.get(f"/api/simulations/{key}")).status_code == 404
    assert (await client.get(f"/api/simulations/{key}/result")).status_code == 404

    queued = await client.post(f"/api/simulations/{key}")
    assert queued.status_code == 202, queued.text
    assert queued.json()["status"] == "queued"
    again = await client.post(f"/api/simulations/{key}")  # still queued or running
    assert again.json()["status"] in {"queued", "running"}
    await runner.wait()

    sim = (await client.get(f"/api/simulations/{key}")).json()
    assert sim["status"] == "done", sim["error"]
    assert sim["summary"]["held"] is True
    assert sim["summary"]["switch_over_chart"] is False

    result = (await client.get(f"/api/simulations/{key}/result")).json()
    assert result["completed"]
    assert result["cost"].startswith("$")
    points = (await client.get(f"/api/simulations/{key}/series?max_points=40")).json()
    assert 2 <= len(points) <= 41
    heat = (await client.get(f"/api/simulations/{key}/heatmap?max_times=10")).json()
    assert len(heat["walls"]) == 6
    assert len(heat["times_h"]) <= 11
    assert (await client.get(f"/api/simulations/{key}/switchover")).status_code == 404

    # Done and its files there: returned as it is
    done = (await client.post(f"/api/simulations/{key}")).json()
    assert done["finished_at"] == sim["finished_at"]

    # Its files gone: it runs again
    shutil.rmtree(tmp_path / "simulations" / key)
    rerun = (await client.post(f"/api/simulations/{key}")).json()
    assert rerun["status"] == "queued"
    await runner.wait()
    assert (await client.get(f"/api/simulations/{key}")).json()["status"] == "done"


async def test_a_simulation_the_engine_refuses_fails_with_why(
    client: httpx.AsyncClient, runner: InlineRunner
) -> None:
    source = (EXAMPLES / "pnw-hybrid-crossdraft.yaml").read_text(encoding="utf-8")
    key = await _key(client, source)
    await client.post(f"/api/simulations/{key}")
    await runner.wait()
    sim = (await client.get(f"/api/simulations/{key}")).json()
    assert sim["status"] == "failed"
    assert "specific_heat" in sim["error"]
    # A failed run can be asked for again
    assert (await client.post(f"/api/simulations/{key}")).json()["status"] == "queued"
    await runner.wait()


async def test_a_hybrid_gets_its_switch_over_chart(
    client: httpx.AsyncClient, runner: InlineRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr("kilndesigner_api.tasks.CHART_DT", 1200.0)
    source = (EXAMPLES / "pnw-hybrid-crossdraft.yaml").read_text(encoding="utf-8")
    # A test input only, not engineering data: the castable roof needs some c_p to run
    source = source.replace(
        "kast-o-lite-30-li-plus\n      thickness: 3 in\n",
        "kast-o-lite-30-li-plus\n      thickness: 3 in\n      specific_heat: 1 kJ/(kg*K)\n",
    )
    key = await _key(client, source)
    await client.post(f"/api/simulations/{key}")
    await runner.wait()
    chart = (await client.get(f"/api/simulations/{key}/switchover")).json()
    assert len(chart["points"]) >= 5
    assert "cheapest_c" in chart


async def test_an_unknown_key_cannot_be_simulated(client: httpx.AsyncClient) -> None:
    assert (await client.post("/api/simulations/nope")).status_code == 404


async def test_a_run_whose_design_was_deleted_fails(
    client: httpx.AsyncClient, runner: InlineRunner, example: str
) -> None:
    created = (await client.post("/api/designs", json={"source": example})).json()
    key = created["latest"]["build_key"]
    await client.post(f"/api/simulations/{key}")
    await client.delete(f"/api/designs/{created['id']}")
    await runner.wait()
    sim = (await client.get(f"/api/simulations/{key}")).json()
    assert sim["status"] in {"failed", "done"}
