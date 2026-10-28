import json
import sys
from pathlib import Path

import pytest

from kilndesigner_api.openapi import document, main

CHECKED_IN = Path(__file__).parents[2] / "packages" / "api-client" / "openapi.json"


def test_the_web_clients_openapi_document_is_up_to_date() -> None:
    """The web client is generated from this file; regenerate it when the API changes:
    ``uv run kilndesigner-openapi packages/api-client/openapi.json``, then ``npm run generate``.
    """
    assert CHECKED_IN.read_text(encoding="utf-8") == document()


def test_the_openapi_command_writes_the_document_to_the_file_it_is_given(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "openapi.json"
    monkeypatch.setattr(sys, "argv", ["kilndesigner-openapi", str(target)])
    main()
    written = target.read_text(encoding="utf-8")
    assert written == document()
    spec = json.loads(written)
    assert spec["info"]["title"] == "Kilndesigner"
    assert "/api/designs/{design_id}/versions" in spec["paths"]
