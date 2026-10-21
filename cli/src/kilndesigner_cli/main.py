"""The ``kilndesigner`` command."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError

from kilndesigner import Kiln, load_design
from kilndesigner.library import UnknownEntryError
from kilndesigner.report import Report, design_report
from kilndesigner.units import UnitError

app = typer.Typer(no_args_is_help=True, help="Design kilns from YAML design files.")

DesignPath = Annotated[
    Path, typer.Argument(exists=True, dir_okay=False, readable=True, help="A design file (YAML)")
]

# Kiln reports use °, Ω and ² everywhere; make sure the console can print them.
for stream in (sys.stdout, sys.stderr):
    reconfigure = getattr(stream, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(encoding="utf-8")


def _load(path: Path) -> Kiln:
    try:
        return load_design(path)
    except (ValidationError, UnitError) as e:
        typer.echo(f"{path}: the design is not valid\n{e}", err=True)
        raise typer.Exit(code=2) from e


def _report(kiln: Kiln, path: Path) -> Report:
    try:
        return design_report(kiln)
    except UnknownEntryError as e:
        typer.echo(f"{path}: {e}", err=True)
        raise typer.Exit(code=2) from e


@app.command()
def check(design: DesignPath) -> None:
    """Check that a design file is valid."""
    kiln = _load(design)
    typer.echo(f"{design}: {kiln.name} is valid")


@app.command()
def schema() -> None:
    """Print the design file's JSON Schema, for editors and validators."""
    typer.echo(json.dumps(Kiln.model_json_schema(by_alias=True), indent=2))


def summary(report: Report) -> str:
    lines = [
        report.name,
        f"  Chamber volume:   {report.chamber_volume}",
        f"  Top temperature:  {report.heat_loss.top_temperature}",
        f"  Heat loss at top: {report.heat_loss.total}",
    ]
    if report.electric is not None:
        e = report.electric
        lines.append(f"  Installed power:  {e.installed_power} ({e.power_per_volume})")
        if e.elements is not None:
            el = e.elements
            lines.append(
                f"  Elements:         {el.count} × {el.gauge} {e.alloy}, "
                f"{el.length_each} each, {el.wiring}"
            )
            lines.append(f"  Surface load:     {el.surface_load}; coil pitch {el.pitch}")
    if report.bom is not None:
        lines.append(f"  Materials:        ${report.bom.total:,.0f} (priced items)")
    lines.extend(f"  [{f.level}] {f.message}" for f in report.findings)
    return "\n".join(lines)


@app.command()
def build(
    design: DesignPath,
    out: Annotated[Path, typer.Option(help="Folder for everything written")] = Path("out"),
    model: Annotated[bool, typer.Option(help="Build the 3D model (STEP and glTF)")] = True,
    plans: Annotated[bool, typer.Option(help="Draw the plans (PDF and DXF)")] = True,
) -> None:
    """Calculate a design; write the report, the 3D model and the plans."""
    from kilndesigner.geometry import GeometryNotSupportedError

    kiln = _load(design)
    report = _report(kiln, design)
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(report.model_dump_json(indent=2), encoding="utf-8")
    written = [out / "report.json"]
    if model:
        from kilndesigner.geometry import write_model

        try:
            written.extend(write_model(kiln, report, out).values())
        except GeometryNotSupportedError as e:
            typer.echo(f"No 3D model: {e}", err=True)
    if plans:
        from kilndesigner.plans import build_plans

        try:
            result = build_plans(kiln, report, dxf_path=out / "sections.dxf")
            (out / "plans.pdf").write_bytes(result.pdf)
            written += [out / "plans.pdf", out / "sections.dxf"]
        except GeometryNotSupportedError as e:
            typer.echo(f"No plans: {e}", err=True)
    typer.echo(summary(report))
    typer.echo("Wrote " + ", ".join(str(p) for p in written))
    if report.errors:
        raise typer.Exit(code=1)
