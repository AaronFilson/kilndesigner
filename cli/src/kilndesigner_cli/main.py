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
from kilndesigner.castable import CastableError
from kilndesigner.library import UnknownEntryError
from kilndesigner.report import Report, design_report
from kilndesigner.results import write_run
from kilndesigner.simulation import FiringResult, SimulationError, switch_over_chart
from kilndesigner.simulation import simulate as simulate_firing
from kilndesigner.units import UnitError, parse_quantity, si

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
    except (UnknownEntryError, CastableError) as e:
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
    # A warning or an error is marked as its sheet is in checks.xlsx and the plans: [W1 warning]
    lines.extend(
        f"  [{f.check.label + ' ' if f.check and f.check.label else ''}{f.level}] {f.message}"
        for f in report.findings
    )
    return "\n".join(lines)


COMPARED = (
    "Chamber volume",
    "Heat loss at top",
    "Hottest outside face",
    "Installed power",
    "Burner input",
    "Propane supply keeps up",
    "Switch to burners at",
    "Materials (priced)",
    "Errors / warnings",
)
"""The rows of ``compare``'s table, in the order they're shown."""


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
        if g.supply:  # a line (natural gas) has no cylinders or tank to check
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
    # The same rows in the same order whichever design comes first, and each column as wide as
    # its widest cell, so long cells don't run into the next
    labels = [label for label in COMPARED if any(label in rows for _, rows in columns)]
    width = max(len(label) for label in labels) + 2
    widths = [
        max(len(name), *(len(rows.get(label, "—")) for label in labels)) + 2
        for name, rows in columns
    ]
    typer.echo(" " * width + "".join(n.ljust(w) for (n, _), w in zip(columns, widths, strict=True)))
    for label in labels:
        cells = (r.get(label, "—").ljust(w) for (_, r), w in zip(columns, widths, strict=True))
        typer.echo(label.ljust(width) + "".join(cells))


def firing_summary(result: FiringResult) -> str:
    lines = [
        f"{result.name}: simulated firing",
        f"  Heat:             {result.heat}",
        f"  Firing time:      {result.duration}"
        + ("" if result.completed else " (stopped before the schedule's end)"),
        f"  Reached:          {result.reached_c:.0f} °C of {result.target_c:.0f} °C",
        f"  Schedule kept:    {'yes' if result.held else 'no: the heat falls behind'}",
        f"  Heat put in:      {result.energy_kwh:.1f} kWh "
        f"(walls {result.walls_kwh:.1f}, ware {result.ware_kwh:.1f}; shell lost "
        f"{result.shell_kwh:.1f})",
    ]
    if result.electricity_kwh:
        lines.append(f"  Electricity:      {result.electricity_kwh:.1f} kWh")
    if result.fuel_kwh:
        gallons = f" ({result.propane_gallons:.1f} gal propane)" if result.propane_gallons else ""
        lines.append(f"  Fuel burned:      {result.fuel_kwh:.1f} kWh{gallons}")
    if result.cost is not None:
        lines.append(f"  Cost:             {result.cost}")
    lines.extend(f"  [{f.level}] {f.message}" for f in result.findings)
    return "\n".join(lines)


@app.command()
def simulate(
    design: DesignPath,
    out: Annotated[Path, typer.Option(help="Folder for the results")] = Path("out/firing"),
    switch_over: Annotated[
        str | None,
        typer.Option(help="A hybrid's hand-over to the burners, for example '1650 degF'"),
    ] = None,
    chart: Annotated[
        bool, typer.Option(help="Also chart a hybrid's cost and time against its hand-over")
    ] = False,
) -> None:
    """Simulate a firing along the design's schedule; write Parquet results (ADR 0007)."""
    kiln = _load(design)
    try:
        switch_c = si(parse_quantity(switch_over, "[temperature]"), "degC") if switch_over else None
        run = simulate_firing(kiln, switch_over_c=switch_c)
        written = write_run(run, out, run_id=design.stem)
        if chart:
            c = switch_over_chart(kiln)
            path = out / "switchover.json"
            path.write_text(c.model_dump_json(indent=2), encoding="utf-8")
            written.append(path)
    except (UnknownEntryError, CastableError, SimulationError, UnitError) as e:
        typer.echo(f"{design}: {e}", err=True)
        raise typer.Exit(code=2) from e
    typer.echo(firing_summary(run.result))
    if chart:
        typer.echo("  Hand-over   time     cost")
        for p in c.points:  # pyright: ignore[reportPossiblyUnboundVariable]
            typer.echo(
                f"  {p.switch_over_f:6.0f} °F  {p.duration_h:5.1f} h  ${p.cost_usd:,.2f}"
                + ("" if p.completed else "  (stalls)")
            )
    typer.echo("Wrote " + ", ".join(str(p) for p in written))


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
    except (UnknownEntryError, CastableError) as e:
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
