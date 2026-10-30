"""Every validation notebook runs, and every engine figure in it is within its tolerance of the
published one (ADR 0009). The notebooks are in ``notebooks/validation/``; open one with
``uv run marimo edit notebooks/validation/<name>.py`` to read the cases and their sources."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

NOTEBOOKS = Path(__file__).parents[2] / "notebooks" / "validation"
PATHS = sorted(p for p in NOTEBOOKS.glob("*.py") if p.stem != "published")


def _run(path: Path) -> dict[str, Any]:
    if str(NOTEBOOKS) not in sys.path:
        sys.path.insert(0, str(NOTEBOOKS))
    spec = importlib.util.spec_from_file_location(f"validation_{path.stem}", path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    _, defs = module.app.run()
    return dict(defs)


def test_there_is_a_notebook_per_solver() -> None:
    assert {p.stem for p in PATHS} == {
        "wall_heat_loss",
        "surface",
        "elements",
        "transient_wall",
        "combustion",
        "chimney_draft",
        "arch_thrust",
        "castable_conductivity",
        "propane_supply",
    }


@pytest.mark.parametrize("path", PATHS, ids=[p.stem for p in PATHS])
def test_the_engine_matches_the_published_cases(path: Path) -> None:
    results: list[dict[str, Any]] = _run(path)["results"]
    assert results
    failed = [
        f"{r['case']}: engine {r['engine']:.6g}, published {r['published']:.6g} ({r['source']})"
        for r in results
        if not r["ok"]
    ]
    assert not failed, "\n".join(failed)
