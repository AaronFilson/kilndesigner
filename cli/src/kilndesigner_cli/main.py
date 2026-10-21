"""The ``kilndesigner`` command."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated

import typer
from pydantic import ValidationError

from kilndesigner import Kiln, load_design
from kilndesigner.units import UnitError

app = typer.Typer(no_args_is_help=True, help="Design kilns from YAML design files.")

DesignPath = Annotated[
    Path, typer.Argument(exists=True, dir_okay=False, readable=True, help="A design file (YAML)")
]


def _load(path: Path) -> Kiln:
    try:
        return load_design(path)
    except (ValidationError, UnitError) as e:
        typer.echo(f"{path}: the design is not valid\n{e}", err=True)
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
