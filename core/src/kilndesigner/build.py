"""Building a design: the report, the 3D model and the plans, written to one folder.

The CLI and the app's worker both call :func:`build_design`, so a build from the command line
and a build in the app write the same files.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

from kilndesigner.model import Kiln
from kilndesigner.report import ENGINE_VERSION, Report, design_report


def design_document(kiln: Kiln) -> dict[str, object]:
    """The design as a JSON document: the same shape as the YAML file."""
    return kiln.model_dump(mode="json", by_alias=True, exclude_none=True)


def build_key(kiln: Kiln) -> str:
    """A hash of the design and the engine version: equal keys build identical files."""
    canonical = json.dumps(
        {"engine": ENGINE_VERSION, "design": design_document(kiln)},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )
    return hashlib.sha256(canonical.encode()).hexdigest()


@dataclass
class BuildResult:
    report: Report
    written: list[Path] = field(default_factory=list[Path])
    notes: list[str] = field(default_factory=list[str])
    """Parts that could not be produced, and why (for example a shape with no 3D model yet)."""


def build_design(kiln: Kiln, out: Path, *, model: bool = True, plans: bool = True) -> BuildResult:
    """Calculate a design and write ``report.json``, the model and the plans into ``out``."""
    from kilndesigner.geometry import GeometryNotSupportedError

    result = BuildResult(design_report(kiln))
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(result.report.model_dump_json(indent=2), encoding="utf-8")
    result.written.append(out / "report.json")
    if model:
        from kilndesigner.geometry import write_model

        try:
            result.written.extend(write_model(kiln, result.report, out).values())
        except GeometryNotSupportedError as e:
            result.notes.append(f"No 3D model: {e}")
    if plans:
        from kilndesigner.plans import build_plans

        try:
            drawn = build_plans(kiln, result.report, dxf_path=out / "sections.dxf")
            (out / "plans.pdf").write_bytes(drawn.pdf)
            result.written += [out / "plans.pdf", out / "sections.dxf"]
        except GeometryNotSupportedError as e:
            result.notes.append(f"No plans: {e}")
    return result
