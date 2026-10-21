"""Golden files: every example's full report, so any change in a result is a reviewable diff.

After an intended change, regenerate with ``pytest core/tests/test_golden.py --update-golden``
and review the diff of ``core/tests/golden/``.
"""

import json
from pathlib import Path

import pytest

from kilndesigner import load_design
from kilndesigner.report import design_report

EXAMPLES = Path(__file__).parents[2] / "examples"
GOLDEN = Path(__file__).parent / "golden"


@pytest.mark.parametrize("path", sorted(EXAMPLES.glob("*.yaml")), ids=lambda p: p.stem)
def test_report_matches_golden(path: Path, update_golden: bool) -> None:
    report = design_report(load_design(path)).model_dump(mode="json")
    golden = GOLDEN / f"{path.stem}.report.json"
    text = json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if update_golden or not golden.exists():
        GOLDEN.mkdir(exist_ok=True)
        golden.write_text(text, encoding="utf-8")
    assert report == _approx(json.loads(golden.read_text(encoding="utf-8")))


def _approx(value: object) -> object:
    """Floats compared to 1e-9, so a last-bit difference between platforms isn't a failure."""
    if isinstance(value, float):
        return pytest.approx(value, rel=1e-9)
    if isinstance(value, dict):
        return {k: _approx(v) for k, v in value.items()}  # pyright: ignore[reportUnknownVariableType]
    if isinstance(value, list):
        return [_approx(v) for v in value]  # pyright: ignore[reportUnknownVariableType]
    return value
