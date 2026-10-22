import httpx
import pytest

from kilndesigner_api.jobs import InlineRunner

pytestmark = [pytest.mark.anyio, pytest.mark.db]


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
    assert report["electric"]["elements"]["count"] >= 3
    file = await client.get(f"/api/builds/{key}/files/kiln.glb")
    assert file.content[:4] == b"glTF"

    again = (await client.post(f"/api/builds/{key}")).json()
    assert again["status"] == "done"
    assert again["finished_at"] == build["finished_at"]


async def test_only_built_files_can_be_fetched(client: httpx.AsyncClient, example: str) -> None:
    design = (await client.post("/api/designs", json={"source": example})).json()
    key = design["latest"]["build_key"]
    assert (await client.get(f"/api/builds/{key}/files/report.json")).status_code == 404
    assert (await client.post("/api/builds/not-a-key")).status_code == 404


async def test_deleting_a_design(client: httpx.AsyncClient, example: str) -> None:
    design = (await client.post("/api/designs", json={"source": example})).json()
    assert (await client.delete(f"/api/designs/{design['id']}")).status_code == 204
    assert (await client.get(f"/api/designs/{design['id']}")).status_code == 404
