from pathlib import Path

from kilndesigner_api.openapi import document

CHECKED_IN = Path(__file__).parents[2] / "packages" / "api-client" / "openapi.json"


def test_the_web_clients_openapi_document_is_up_to_date() -> None:
    """The web client is generated from this file; regenerate it when the API changes:
    ``uv run kilndesigner-openapi packages/api-client/openapi.json``, then ``npm run generate``.
    """
    assert CHECKED_IN.read_text(encoding="utf-8") == document()
