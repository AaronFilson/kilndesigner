import shutil
from pathlib import Path

import httpx
import pytest

from kilndesigner_api import db
from kilndesigner_api.jobs import InlineRunner
from kilndesigner_api.tasks import refresh_build_keys

pytestmark = [pytest.mark.anyio, pytest.mark.db]

EXAMPLES = Path(__file__).parents[2] / "examples"


async def test_a_saved_design_comes_back_as_written(
    client: httpx.AsyncClient, example: str
) -> None:
    created = await client.post("/api/designs", json={"source": example})
    assert created.status_code == 201, created.text
    design = created.json()
    assert design["name"] == "Electric front-loader, cone 10"
    assert design["latest"]["number"] == 1
    assert design["latest"]["source"] == example  # comments and all
    assert design["latest"]["document"]["chamber"]["width"] == "22.5 in"

    listed = (await client.get("/api/designs")).json()
    assert [d["id"] for d in listed] == [design["id"]]


async def test_an_invalid_design_is_refused_with_where_and_why(client: httpx.AsyncClient) -> None:
    response = await client.post("/api/designs", json={"source": "name: x\n"})
    assert response.status_code == 422
    problems = response.json()["detail"]
    assert problems
    assert all("loc" in p and "msg" in p for p in problems)


async def test_yaml_that_does_not_parse_is_refused(client: httpx.AsyncClient) -> None:
    response = await client.post("/api/designs", json={"source": "name: [unclosed\n"})
    assert response.status_code == 422
    assert "YAML" in response.json()["detail"][0]["msg"]


async def test_saving_adds_versions_and_skips_unchanged_saves(
    client: httpx.AsyncClient, example: str
) -> None:
    design = (await client.post("/api/designs", json={"source": example})).json()
    url = f"/api/designs/{design['id']}/versions"

    unchanged = (await client.post(url, json={"source": example})).json()
    assert len(unchanged["versions"]) == 1

    renamed = example.replace("cone 10\n", "cone 10, v2\n", 1)
    saved = (await client.post(url, json={"source": renamed})).json()
    assert [v["number"] for v in saved["versions"]] == [1, 2]
    assert saved["name"] == "Electric front-loader, cone 10, v2"
    assert saved["versions"][0]["build_key"] != saved["versions"][1]["build_key"]

    first = (await client.get(f"{url}/1")).json()
    assert first["source"] == example


async def test_a_design_can_be_saved_from_the_forms_as_json(
    client: httpx.AsyncClient, example: str
) -> None:
    from_yaml = (await client.post("/api/designs", json={"source": example})).json()["latest"]
    document = from_yaml["document"]
    from_json = (await client.post("/api/designs", json={"document": document})).json()["latest"]
    assert from_json["document"] == document
    assert from_json["build_key"] == from_yaml["build_key"]
    assert "chamber:" in from_json["source"]


@pytest.mark.geometry
async def test_a_build_writes_the_report_and_is_reused(
    client: httpx.AsyncClient, runner: InlineRunner, example: str
) -> None:
    design = (await client.post("/api/designs", json={"source": example})).json()
    key = design["latest"]["build_key"]

    queued = await client.post(f"/api/builds/{key}")
    assert queued.status_code == 202, queued.text
    assert queued.json()["status"] == "queued"
    await runner.wait()

    build = (await client.get(f"/api/builds/{key}")).json()
    assert build["status"] == "done", build["error"]
    assert "report.json" in build["files"]
    report = (await client.get(f"/api/builds/{key}/report")).json()
    assert report["electric"]["elements"]["groove_rows"] >= 3  # an element may run several
    file = await client.get(f"/api/builds/{key}/files/kiln.glb")
    assert file.content[:4] == b"glTF"

    again = (await client.post(f"/api/builds/{key}")).json()
    assert again["status"] == "done"
    assert again["finished_at"] == build["finished_at"]


@pytest.mark.geometry
async def test_a_build_whose_files_have_gone_can_be_built_again(
    client: httpx.AsyncClient, runner: InlineRunner, example: str, tmp_path: Path
) -> None:
    # The dev loop and `docker compose up` share the database but not the data folder.
    design = (await client.post("/api/designs", json={"source": example})).json()
    key = design["latest"]["build_key"]
    await client.post(f"/api/builds/{key}")
    await runner.wait()
    shutil.rmtree(tmp_path / "builds" / key)

    gone = (await client.get(f"/api/builds/{key}")).json()
    assert gone["status"] == "failed"
    assert "no longer in the data folder" in gone["error"]
    assert (await client.get(f"/api/builds/{key}/report")).status_code == 404
    assert (await client.get(f"/api/builds/{key}/files/kiln.glb")).status_code == 404

    assert (await client.post(f"/api/builds/{key}")).json()["status"] == "queued"
    await runner.wait()
    assert (await client.get(f"/api/builds/{key}")).json()["status"] == "done"
    assert (await client.get(f"/api/builds/{key}/files/kiln.glb")).content[:4] == b"glTF"


async def test_after_an_engine_change_saved_designs_are_built_afresh(
    client: httpx.AsyncClient, database_url: str, example: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    design = (await client.post("/api/designs", json={"source": example})).json()
    old = design["latest"]["build_key"]

    monkeypatch.setattr("kilndesigner.build.engine_fingerprint", lambda: "changed code")
    engine = db.make_engine(database_url)
    assert await refresh_build_keys(db.make_sessions(engine)) == 1
    await engine.dispose()

    new = (await client.get(f"/api/designs/{design['id']}")).json()["latest"]["build_key"]
    assert new != old
    assert (await client.get(f"/api/builds/{new}")).status_code == 404  # not built yet


async def test_only_built_files_can_be_fetched(client: httpx.AsyncClient, example: str) -> None:
    design = (await client.post("/api/designs", json={"source": example})).json()
    key = design["latest"]["build_key"]
    assert (await client.get(f"/api/builds/{key}/files/report.json")).status_code == 404
    assert (await client.post("/api/builds/not-a-key")).status_code == 404


async def test_deleting_a_design(client: httpx.AsyncClient, example: str) -> None:
    design = (await client.post("/api/designs", json={"source": example})).json()
    assert (await client.delete(f"/api/designs/{design['id']}")).status_code == 204
    assert (await client.get(f"/api/designs/{design['id']}")).status_code == 404


async def test_the_kinds_of_kiln_to_start_from(client: httpx.AsyncClient) -> None:
    templates = (await client.get("/api/templates")).json()
    assert [t["id"] for t in templates] == [
        "electric-front-loader",
        "gas-crossdraft",
        "hybrid-crossdraft",
    ]
    for t in templates:
        saved = await client.post("/api/designs", json={"document": t["document"]})
        assert saved.status_code == 201, saved.text


async def test_the_library_offers_what_a_design_can_choose(client: httpx.AsyncClient) -> None:
    library = (await client.get("/api/library")).json()
    assert "ifb-k23" in {m["id"] for m in library["materials"]}
    assert "kanthal-a1" in {a["id"] for a in library["alloys"]}
    assert "10" in library["cones"]
    assert "GACO MR750" in {b["id"] for b in library["burners"]}


async def test_checking_a_design_turns_it_either_way(
    client: httpx.AsyncClient, example: str
) -> None:
    from_yaml = (await client.post("/api/designs/check", json={"source": example})).json()
    assert from_yaml["source"] == example
    document = {**from_yaml["document"], "chamber": {**from_yaml["document"]["chamber"],
                                                     "width": "30 in"}}  # fmt: skip
    from_json = (await client.post("/api/designs/check", json={"document": document})).json()
    assert "width: 30 in" in from_json["source"]
    bad = await client.post("/api/designs/check", json={"document": {"name": "x"}})
    assert bad.status_code == 422
    assert (await client.get("/api/designs")).json() == []  # nothing was saved


async def test_the_api_answers_a_health_check(client: httpx.AsyncClient) -> None:
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_the_design_schema_uses_the_names_the_file_uses(client: httpx.AsyncClient) -> None:
    schema = (await client.get("/api/schema")).json()
    assert schema["title"] == "Kiln"
    assert "schema" in schema["properties"]  # the file's name for schema_version
    assert "schema_version" not in schema["properties"]
    assert {"name", "firing", "chamber", "lining", "heat"} <= set(schema["required"])


async def test_a_design_comes_as_yaml_or_as_json_but_not_both(
    client: httpx.AsyncClient, example: str
) -> None:
    for body in ({}, {"source": example, "document": {"name": "x"}}):
        response = await client.post("/api/designs/check", json=body)
        assert response.status_code == 422
        assert "send either `source` (YAML) or `document` (JSON)" in response.text
    assert (await client.get("/api/designs")).json() == []


async def test_a_lining_material_the_library_lacks_is_refused_with_where_it_is(
    client: httpx.AsyncClient, example: str
) -> None:
    source = example.replace("kaowool-blanket-8pcf", "mystery-wool", 1).replace(
        "ifb-k23", "unobtainium"
    )
    response = await client.post("/api/designs", json={"source": source})
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {
            "loc": ["lining", "walls", 1, "material"],
            "msg": "no material or castable called 'mystery-wool'",
        },
        {
            "loc": ["lining", "floor", 1, "material"],
            "msg": "no material or castable called 'unobtainium'",
        },
    ]
    assert (await client.get("/api/designs")).json() == []


async def test_an_alloy_or_burner_the_library_lacks_is_refused_when_saved(
    client: httpx.AsyncClient, example: str
) -> None:
    """They were saved, and failed only at build (the review's bugs)."""
    source = example.replace("alloy: kanthal-a1", "alloy: unobtainium")
    response = await client.post("/api/designs", json={"source": source})
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {"loc": ["heat", "electric", "alloy"], "msg": "no alloy called 'unobtainium'"}
    ]
    gas = (EXAMPLES / "gas-crossdraft.yaml").read_text(encoding="utf-8")
    named = gas.replace("wall: front\n    supply", "wall: front\n      model: MR1000\n    supply")
    response = await client.post("/api/designs", json={"source": named})
    assert response.status_code == 422
    [problem] = response.json()["detail"]
    assert problem["loc"] == ["heat", "gas", "burners", "model"]
    assert problem["msg"].startswith("no venturi burner called 'MR1000'; the library has: ")
    # Named the way the engine matches them, by the end of the name
    ok = gas.replace("wall: front\n    supply", "wall: front\n      model: MR100\n    supply")
    assert (await client.post("/api/designs/check", json={"source": ok})).status_code == 200
    power = gas.replace("type: venturi", "type: power").replace(
        "wall: front\n    supply", "wall: front\n      model: MB300\n    supply"
    )
    assert (await client.post("/api/designs/check", json={"source": power})).status_code == 200
    assert (await client.get("/api/designs")).json() == []


async def test_a_lining_can_be_cast_from_the_designs_own_mixes(client: httpx.AsyncClient) -> None:
    source = (EXAMPLES / "diy-castable-test-kiln.yaml").read_text(encoding="utf-8")
    response = await client.post("/api/designs", json={"source": source})
    assert response.status_code == 201, response.text
    document = response.json()["latest"]["document"]
    assert [m["id"] for m in document["castables"]] == ["diy-hot-face", "diy-backup"]
    assert document["lining"]["walls"][0]["material"] == "diy-hot-face"


async def test_a_castable_mix_the_engine_cannot_work_out_is_refused_with_which_one(
    client: httpx.AsyncClient,
) -> None:
    source = (EXAMPLES / "diy-castable-test-kiln.yaml").read_text(encoding="utf-8")
    source = source.replace("ingredient: kyanite", "ingredient: unobtainium", 1)
    response = await client.post("/api/designs", json={"source": source})
    assert response.status_code == 422
    [problem] = response.json()["detail"]
    assert problem["loc"] == ["castables", 0]
    assert problem["msg"].startswith("diy-hot-face: no ingredient 'unobtainium'")


async def test_a_version_that_was_never_saved_is_not_found(
    client: httpx.AsyncClient, example: str
) -> None:
    design = (await client.post("/api/designs", json={"source": example})).json()
    missing = await client.get(f"/api/designs/{design['id']}/versions/2")
    assert missing.status_code == 404
    assert missing.json() == {"detail": "no such version"}


async def test_a_failed_build_says_why_and_can_be_queued_again(
    client: httpx.AsyncClient, runner: InlineRunner, older_schema_key: str, tmp_path: Path
) -> None:
    key = older_schema_key
    queued = await client.post(f"/api/builds/{key}")
    assert queued.status_code == 202, queued.text
    assert queued.json()["status"] == "queued"
    await runner.wait()

    failed = (await client.get(f"/api/builds/{key}")).json()
    assert failed["status"] == "failed"
    assert "validation errors for Kiln" in failed["error"]
    assert failed["finished_at"] is not None
    assert list((tmp_path / "builds").iterdir()) == []  # nothing half-written is left behind
    assert (await client.get(f"/api/builds/{key}/report")).status_code == 404

    again = (await client.post(f"/api/builds/{key}")).json()
    assert (again["status"], again["error"], again["finished_at"]) == ("queued", None, None)
    await runner.wait()
    assert (await client.get(f"/api/builds/{key}")).json()["status"] == "failed"
