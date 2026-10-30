"""Reading and writing design files (YAML)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from kilndesigner.model import Kiln


def parse_design(text: str) -> Kiln:
    data: Any = yaml.safe_load(text)
    return Kiln.model_validate(data)


def load_design(path: str | Path) -> Kiln:
    return parse_design(Path(path).read_text(encoding="utf-8"))


def dump_design(kiln: Kiln) -> str:
    data = kiln.model_dump(mode="json", by_alias=True, exclude_none=True)
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
