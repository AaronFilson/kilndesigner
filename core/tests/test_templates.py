"""The kinds of kiln the app offers to start from."""

from __future__ import annotations

from pathlib import Path

import pytest

from kilndesigner.report import design_report
from kilndesigner.templates import templates

EXAMPLES = Path(__file__).parents[2] / "examples"
FROM_EXAMPLE = {
    "electric-front-loader": "electric-front-loader.yaml",
    "gas-crossdraft": "gas-crossdraft.yaml",
    "hybrid-crossdraft": "pnw-hybrid-crossdraft.yaml",
}


@pytest.mark.parametrize("template", templates(), ids=lambda t: t.id)
def test_each_template_is_its_example(template) -> None:  # type: ignore[no-untyped-def]
    example = (EXAMPLES / FROM_EXAMPLE[template.id]).read_text(encoding="utf-8")
    assert template.source == example


@pytest.mark.parametrize("template", templates(), ids=lambda t: t.id)
def test_each_template_builds_a_report(template) -> None:  # type: ignore[no-untyped-def]
    report = design_report(template.kiln)
    assert report.frame is not None
    # A starting point may carry warnings (a supply short in the cold) but not a refusal
    assert not [f.message for f in report.errors if "propane supply" not in f.message]
