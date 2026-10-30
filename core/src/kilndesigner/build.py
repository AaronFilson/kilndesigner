"""Building a design: the report, the 3D model and the plans, written to one folder.

The CLI and the app's worker both call :func:`build_design`, so a build from the command line
and a build in the app write the same files.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import TYPE_CHECKING

from kilndesigner.model import Kiln
from kilndesigner.report import ENGINE_VERSION, Report, design_report

if TYPE_CHECKING:
    from kilndesigner.plans import Drawing


def design_document(kiln: Kiln) -> dict[str, object]:
    """The design as a JSON document: the same shape as the YAML file."""
    return kiln.model_dump(mode="json", by_alias=True, exclude_none=True)


@cache
def engine_fingerprint() -> str:
    """A hash of the engine's code and data. The version number only changes at a release, so
    this is what makes a build from changed code a new build rather than a stale one."""
    root = Path(__file__).parent
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.suffix in {".py", ".yaml", ".typ"}):
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(path.read_bytes().replace(b"\r\n", b"\n"))
    return digest.hexdigest()


def build_key(kiln: Kiln) -> str:
    """A hash of the design and the engine: equal keys build identical files."""
    canonical = json.dumps(
        {
            "engine": ENGINE_VERSION,
            "fingerprint": engine_fingerprint(),
            "design": design_document(kiln),
        },
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
    checks = [f.check for f in result.report.findings if f.check is not None]
    if checks:
        from kilndesigner.workbook import checks_workbook

        (out / CHECKS).write_bytes(checks_workbook(checks))
        result.written.append(out / CHECKS)
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
            result.written += _write_drawings(drawn.drawings, out / DRAWINGS)
        except GeometryNotSupportedError as e:
            result.notes.append(f"No plans: {e}")
    return result


CHECKS = "checks.xlsx"
"""The workbook of the report's checks: one worksheet per warning or error, with live formulas."""

DRAWINGS = "drawings"
"""The folder in a build for the plans' drawings as SVG, with ``index.json`` listing them."""


def _write_drawings(drawings: tuple[Drawing, ...], folder: Path) -> list[Path]:
    folder.mkdir(exist_ok=True)
    written: list[Path] = []
    for d in drawings:
        (folder / d.file).write_text(d.svg, encoding="utf-8")
        written.append(folder / d.file)
    index = [
        {"file": d.file, "kind": d.kind, "title": d.title, "description": d.description}
        for d in drawings
    ]
    (folder / "index.json").write_text(json.dumps(index, ensure_ascii=False, indent=2), "utf-8")
    return [folder / "index.json", *written]
