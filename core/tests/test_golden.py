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
    if update_golden or not golden.exists():
        old = json.loads(golden.read_text(encoding="utf-8")) if golden.exists() else None
        text = json.dumps(_keep_close(report, old), indent=2, ensure_ascii=False, sort_keys=True)
        GOLDEN.mkdir(exist_ok=True)
        golden.write_text(text + "\n", encoding="utf-8", newline="\n")
    assert report == _approx(json.loads(golden.read_text(encoding="utf-8")))


def _keep_close(new: object, old: object) -> object:
    """``new``, but with ``old``'s floats where they agree to 1e-9, so that regenerating on
    another platform doesn't rewrite every last-bit difference into the diff."""
    if isinstance(new, float) and isinstance(old, float):
        return old if new == pytest.approx(old, rel=1e-9) else new
    if isinstance(new, dict) and isinstance(old, dict):
        return {k: _keep_close(v, old.get(k)) for k, v in new.items()}  # pyright: ignore[reportUnknownVariableType, reportUnknownMemberType, reportUnknownArgumentType]
    if isinstance(new, list) and isinstance(old, list) and len(new) == len(old):  # pyright: ignore[reportUnknownArgumentType]
        return [_keep_close(n, o) for n, o in zip(new, old, strict=True)]  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType]
    return new


def _approx(value: object) -> object:
    """Floats compared to 1e-9, so a last-bit difference between platforms isn't a failure."""
    if isinstance(value, float):
        return pytest.approx(value, rel=1e-9)
    if isinstance(value, dict):
        return {k: _approx(v) for k, v in value.items()}  # pyright: ignore[reportUnknownVariableType]
    if isinstance(value, list):
        return [_approx(v) for v in value]  # pyright: ignore[reportUnknownVariableType]
    return value
