"""The MCP server, through an in-memory MCP client: what an assistant sees."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import anyio
import pytest
from mcp import Client
from mcp.types import TextContent

from kilndesigner_mcp import server
from kilndesigner_mcp.server import mcp

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"


def call(name: str, arguments: dict[str, Any] | None = None) -> tuple[bool, Any]:
    """Call a tool; (is_error, the structured result or the error's text)."""

    async def run() -> tuple[bool, Any]:
        async with Client(mcp) as client:
            result = await client.call_tool(name, arguments or {})
        if result.is_error:
            text = result.content[0]
            assert isinstance(text, TextContent)
            return True, text.text
        # The same result as JSON text, for clients that read only text
        text = result.content[0]
        assert isinstance(text, TextContent)
        assert json.loads(text.text) == result.structured_content
        return False, result.structured_content

    return anyio.run(run)


def ok(name: str, arguments: dict[str, Any] | None = None) -> Any:
    is_error, value = call(name, arguments)
    assert not is_error, value
    return value


def test_lists_the_tools_all_read_only() -> None:
    async def run() -> list[Any]:
        async with Client(mcp) as client:
            return (await client.list_tools()).tools

    tools = anyio.run(run)
    assert {t.name for t in tools} == {
        "list_templates",
        "get_template",
        "list_examples",
        "get_example",
        "validate_design",
        "build_design",
        "simulate_firing",
        "start_design",
    }
    assert all(t.annotations and t.annotations.read_only_hint for t in tools)


def test_templates_and_one_template() -> None:
    listed = ok("list_templates")["templates"]
    crossdraft = next(t for t in listed if t["id"] == "gas-crossdraft")
    assert crossdraft["fuel"] == "gas"
    assert crossdraft["cone"] == "10"
    assert {t["fuel"] for t in listed} >= {"electric", "gas", "hybrid", "wood", "coal", "oil"}
    design = ok("get_template", {"id": "gas-crossdraft"})["design"]
    assert ok("validate_design", {"design": design})["valid"]
    is_error, text = call("get_template", {"id": "nope"})
    assert is_error
    assert "gas-crossdraft" in text


def test_examples(monkeypatch: pytest.MonkeyPatch) -> None:
    names = [e["name"] for e in ok("list_examples")["examples"]]
    assert "electric-front-loader" in names
    design = ok("get_example", {"name": "electric-front-loader"})["design"]
    assert design == (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    assert call("get_example", {"name": "../pyproject"})[0]
    monkeypatch.setenv("KILNDESIGNER_EXAMPLES", str(EXAMPLES / "missing"))
    assert ok("list_examples")["examples"] == []
    assert call("get_example", {"name": "electric-front-loader"})[0]


def test_validate_refuses_with_the_reason() -> None:
    assert ok("validate_design", {"design": "name: [unclosed"})["valid"] is False
    result = ok("validate_design", {"design": "schema: 1\nname: x\n"})
    assert result["valid"] is False
    assert any(e.startswith("chamber") for e in result["errors"])


def test_build_carries_the_working() -> None:
    design = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    report = ok("build_design", {"design": design})
    steps = report["heat_loss"]["working"]
    assert steps
    assert {"name", "value"} <= steps[0].keys()
    assert report["electric"]["installed_power"]
    is_error, text = call("build_design", {"design": "name: [unclosed"})
    assert is_error
    assert "YAML" in text
    assert call("build_design", {"design": "schema: 1\n"})[0]


def test_build_refuses_what_the_engine_refuses(monkeypatch: pytest.MonkeyPatch) -> None:
    def refuse(_: object) -> None:
        raise ValueError("outside the checked range")

    monkeypatch.setattr(server, "design_report", refuse)
    design = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    is_error, text = call("build_design", {"design": design})
    assert is_error
    assert "outside the checked range" in text
    start = {"fuel": "gas", "cone": "10", "stacking_volume": "12 ft**3", "budget_usd": 3000}
    assert call("start_design", start)[0]


@pytest.mark.slow
def test_simulate_a_firing() -> None:
    design = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    result = ok("simulate_firing", {"design": design})
    assert result["working"]
    assert "points" not in result
    assert result["duration_h"] > 0
    is_error, text = call("simulate_firing", {"design": design, "switch_over": "12 in"})
    assert is_error
    assert "temperature" in text


def test_start_a_cone_10_gas_kiln_for_12_cubic_feet_under_3000() -> None:
    result = ok(
        "start_design",
        {
            "fuel": "gas",
            "cone": "10",
            "stacking_volume": "12 ft**3",
            "kind": "cross-draft",
            "budget_usd": 3000,
        },
    )
    assert result["template"] == "gas-crossdraft"
    assert isinstance(result["within_budget"], bool)
    names = [s["name"] for s in result["working"]]
    assert names[:3] == [
        "Kind",
        "Nearest template by chamber volume",
        "Chamber volume against the volume asked for",
    ]
    assert "Priced materials against the budget" in names
    assert ok("validate_design", {"design": result["design"]})["cone"] == "10"


def test_start_design_sets_the_cone_and_falls_back_on_kind() -> None:
    result = ok(
        "start_design",
        {"fuel": "electric", "cone": "6", "stacking_volume": "7 ft**3", "kind": "zzz"},
    )
    assert result["cone"] == "6"
    assert result["working"][0]["value"] == "none matched"
    assert any(s["name"] == "Cone" for s in result["working"])
    assert "within_budget" not in result


def test_start_design_refusals() -> None:
    base = {"fuel": "gas", "cone": "10", "stacking_volume": "12 ft**3"}
    assert "volume" in call("start_design", {**base, "stacking_volume": "12 in"})[1]
    assert call("start_design", {**base, "stacking_volume": "0 ft**3"})[0]
    assert call("start_design", {**base, "cone": "99"})[0]
    assert call("start_design", {**base, "fuel": "steam"})[0]


def test_start_design_with_no_template_of_the_fuel(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(server, "_template_facts", tuple)
    assert (
        "No template"
        in call("start_design", {"fuel": "gas", "cone": "10", "stacking_volume": "12 ft**3"})[1]
    )


def test_main_picks_the_transport(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[tuple[Any, ...]] = []

    def run(*a: Any, **k: Any) -> None:
        seen.append((a, k))

    monkeypatch.setattr(mcp, "run", run)
    monkeypatch.setattr("sys.argv", ["kilndesigner-mcp"])
    server.main()
    monkeypatch.setattr("sys.argv", ["kilndesigner-mcp", "--http"])
    server.main()
    assert seen[0] == ((), {})
    assert seen[1][0] == ("streamable-http",)
    assert seen[1][1]["stateless_http"] is True
