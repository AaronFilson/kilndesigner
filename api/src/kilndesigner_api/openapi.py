"""Write the OpenAPI document, for generating the web client: ``kilndesigner-openapi FILE``."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from kilndesigner_api.main import create_app


def document() -> str:
    return json.dumps(create_app().openapi(), indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    Path(sys.argv[1]).write_text(document(), encoding="utf-8")
