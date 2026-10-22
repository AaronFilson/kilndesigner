"""The ``kilndesigner`` command."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError

from kilndesigner import Kiln, load_design
from kilndesigner.build import DRAWINGS, build_design
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


def comparison_rows(report: Report) -> dict[str, str]:
    """The headline numbers of a design, for comparing designs side by side."""
    hottest = max(
        report.heat_loss.faces, key=lambda f: float(f.surface_temperature.split()[0])
    ).surface_temperature
    rows = {
        "Chamber volume": report.chamber_volume,
        "Heat loss at top": report.heat_loss.total,
        "Hottest outside face": hottest,
    }
    if report.electric is not None:
        rows["Installed power"] = report.electric.installed_power
    if report.gas is not None:
        g = report.gas
        rows["Burner input"] = g.design_input
        meets = sum(s.meets_demand for s in g.supply)
        rows["Propane supply keeps up"] = f"in {meets} of {len(g.supply)} cases"
    if report.hybrid is not None:
        rows["Switch to burners at"] = report.hybrid.switch_over
    if report.bom is not None:
        unpriced = any(line.cost is None for line in report.bom.lines)
        rows["Materials (priced)"] = f"${report.bom.total:,.0f}" + (
            " + unpriced items" if unpriced else ""
        )
    levels = [f.level for f in report.findings]
    rows["Errors / warnings"] = f"{levels.count('error')} / {levels.count('warning')}"
    return rows


@app.command()
def compare(
    designs: Annotated[
        list[Path], typer.Argument(exists=True, dir_okay=False, help="Two or more design files")
    ],
) -> None:
    """Compare designs side by side: size, heat loss, fuel, cost and problems."""
    columns = [(d.stem, comparison_rows(_report(_load(d), d))) for d in designs]
    labels = list(dict.fromkeys(label for _, rows in columns for label in rows))
    width = max(len(label) for label in labels) + 2
    col = max(max(len(name) for name, _ in columns), 20) + 2
    typer.echo(" " * width + "".join(name.ljust(col) for name, _ in columns))
    for label in labels:
        cells = "".join(rows.get(label, "—").ljust(col) for _, rows in columns)
        typer.echo(label.ljust(width) + cells)


@app.command()
def build(
    design: DesignPath,
    out: Annotated[Path, typer.Option(help="Folder for everything written")] = Path("out"),
    model: Annotated[bool, typer.Option(help="Build the 3D model (STEP and glTF)")] = True,
    plans: Annotated[bool, typer.Option(help="Draw the plans (PDF and DXF)")] = True,
) -> None:
    """Calculate a design; write the report, the 3D model and the plans."""
    kiln = _load(design)
    try:
        result = build_design(kiln, out, model=model, plans=plans)
    except UnknownEntryError as e:
        typer.echo(f"{design}: {e}", err=True)
        raise typer.Exit(code=2) from e
    for note in result.notes:
        typer.echo(note, err=True)
    typer.echo(summary(result.report))
    top = [p for p in result.written if p.parent == out]
    drawings = sum(1 for p in result.written if p.parent != out and p.suffix == ".svg")
    typer.echo(
        "Wrote "
        + ", ".join(str(p) for p in top)
        + (f", and {drawings} drawings in {out / DRAWINGS}" if drawings else "")
    )
    if result.report.errors:
        raise typer.Exit(code=1)
