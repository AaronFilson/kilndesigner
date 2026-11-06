"""The MCP server: the engine's design, report and firing tools for AI assistants (ADR 0016).

Every tool runs the engine on what it is given and stores nothing. A result is the engine's own
model, dumped to JSON with its working (the steps, formulas, inputs and references) and its
findings, as structured content and as the same JSON in text. A design the engine refuses comes
back as a tool error with the engine's reason, never a guess (ADR 0009).
"""

from __future__ import annotations

import math
import os
import sys
from functools import cache
from pathlib import Path
from typing import Any, Literal

import yaml
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import ValidationError

from kilndesigner import Kiln
from kilndesigner.castable import CastableError
from kilndesigner.designfile import dump_design, parse_design
from kilndesigner.library import UnknownEntryError
from kilndesigner.report import ENGINE_VERSION, design_report
from kilndesigner.shape import chamber_shape
from kilndesigner.simulation import SimulationError
from kilndesigner.simulation import simulate as simulate_firing_run
from kilndesigner.templates import Template, templates
from kilndesigner.units import UnitError, parse_quantity, si
from kilndesigner.working import Step

Fuel = Literal["electric", "gas", "hybrid", "wood", "coal", "oil"]

INSTRUCTIONS = """\
Kilndesigner designs kilns from a design file (YAML) and works out the heat loss, elements or
burners, the frame, the masonry, the bill of materials and a simulated firing. Every number comes
with its working: the formula, the inputs and the published source. Quote the working and the
findings when you answer, and say where a number comes from.

To start a design, call start_design with the fuel, the cone and the stacking volume, or pick one
of list_templates. It returns a design file to change; it never resizes a template for you. Change
the chamber's dimensions in the YAML, then call validate_design and build_design. Errors and
warnings in a report are physical faults to fix; firing time is the potter's choice. The engine
refuses what it has not been checked against, with a reason: pass that reason on rather than
working around it. The bill of materials prices only what has a price in the library; unpriced
lines are not free."""

RESULT_ERRORS = (UnknownEntryError, CastableError, SimulationError, UnitError, ValueError)

mcp = MCPServer(
    "kilndesigner",
    title="Kilndesigner",
    instructions=INSTRUCTIONS,
    version=ENGINE_VERSION,
    website_url="https://github.com/AaronFilson/kilndesigner",
)

READ_ONLY = ToolAnnotations(read_only_hint=True, idempotent_hint=True, open_world_hint=False)


def _examples_folder() -> Path | None:
    """The repository's examples/, or KILNDESIGNER_EXAMPLES; None when neither is there."""
    configured = os.environ.get("KILNDESIGNER_EXAMPLES")
    folder = Path(configured) if configured else Path(__file__).resolve().parents[3] / "examples"
    return folder if folder.is_dir() else None


def _parse(design: str) -> Kiln:
    try:
        return parse_design(design)
    except yaml.YAMLError as e:
        raise ToolError(f"The design is not valid YAML: {e}") from e
    except ValidationError as e:
        raise ToolError(f"The design is not valid:\n{e}") from e


def _fuel(kiln: Kiln) -> Fuel:
    heat = kiln.heat
    if heat.electric is not None and heat.gas is not None:
        return "hybrid"
    if heat.gas is not None:
        return "gas"
    if heat.fire is not None and heat.fire.purpose == "heat":
        return heat.fire.fuel
    return "electric"


def _volume_m3(kiln: Kiln) -> float:
    return chamber_shape(kiln).volume


@cache
def _template_facts() -> tuple[tuple[Template, Kiln, Fuel, float], ...]:
    out: list[tuple[Template, Kiln, Fuel, float]] = []
    for t in templates():
        kiln = t.kiln
        out.append((t, kiln, _fuel(kiln), _volume_m3(kiln)))
    return tuple(out)


def _cone(kiln: Kiln) -> str | None:
    return kiln.firing.cone


@mcp.tool(annotations=READ_ONLY)
def list_templates() -> dict[str, Any]:
    """The kiln types a design can start from: each a complete design that builds as it stands,
    with its fuel, cone and chamber volume."""
    return {
        "templates": [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "fuel": fuel,
                "cone": _cone(kiln),
                "chamber_volume_ft3": round(volume / 0.3048**3, 2),
                "chamber_volume_m3": round(volume, 3),
            }
            for t, kiln, fuel, volume in _template_facts()
        ]
    }


@mcp.tool(annotations=READ_ONLY)
def get_template(id: str) -> dict[str, Any]:
    """A template's design file (YAML), to change and build."""
    for t in templates():
        if t.id == id:
            return {"id": t.id, "title": t.title, "design": t.source}
    ids = ", ".join(t.id for t in templates())
    raise ToolError(f"No template {id!r}. The templates are: {ids}")


@mcp.tool(annotations=READ_ONLY)
def list_examples() -> dict[str, Any]:
    """The example designs in the repository's examples/ folder: real kilns and the author's."""
    folder = _examples_folder()
    if folder is None:
        return {"examples": [], "note": "No examples folder here (set KILNDESIGNER_EXAMPLES)."}
    out: list[dict[str, str]] = []
    for path in sorted(folder.rglob("*.yaml")):
        name = path.relative_to(folder).with_suffix("").as_posix()
        out.append({"name": name, "kiln": parse_design(path.read_text(encoding="utf-8")).name})
    return {"examples": out}


@mcp.tool(annotations=READ_ONLY)
def get_example(name: str) -> dict[str, Any]:
    """An example's design file (YAML), by the name list_examples gives."""
    folder = _examples_folder()
    if folder is not None:
        path = (folder / f"{name}.yaml").resolve()
        if path.is_relative_to(folder.resolve()) and path.is_file():
            return {"name": name, "design": path.read_text(encoding="utf-8")}
    raise ToolError(f"No example {name!r}; list_examples gives the names.")


@mcp.tool(annotations=READ_ONLY)
def validate_design(design: str) -> dict[str, Any]:
    """Check that a design file (YAML) is valid: every value with its unit, every material in the
    library, and every shape one the engine has been checked against."""
    try:
        kiln = parse_design(design)
    except yaml.YAMLError as e:
        return {"valid": False, "errors": [f"not valid YAML: {e}"]}
    except ValidationError as e:
        errors = [
            f"{'.'.join(str(p) for p in err['loc']) or '(design)'}: {err['msg']}"
            for err in e.errors()
        ]
        return {"valid": False, "errors": errors}
    return {"valid": True, "name": kiln.name, "fuel": _fuel(kiln), "cone": _cone(kiln)}


@mcp.tool(annotations=READ_ONLY)
def build_design(design: str) -> dict[str, Any]:
    """Calculate a design: chamber volume, heat loss, elements or burners, the frame, the masonry,
    the bill of materials and the findings, each with its working. No files are written."""
    kiln = _parse(design)
    try:
        report = design_report(kiln)
    except RESULT_ERRORS as e:
        raise ToolError(str(e)) from e
    return report.model_dump(mode="json", exclude_none=True)


@mcp.tool(annotations=READ_ONLY)
def simulate_firing(design: str, switch_over: str | None = None) -> dict[str, Any]:
    """Simulate a firing along the design's schedule: the time, whether the heat keeps up, the
    energy, fuel and cost, with the working. A hybrid's hand-over to the burners may be given,
    for example '1650 degF'. The temperatures through time are left out."""
    kiln = _parse(design)
    try:
        switch_c = si(parse_quantity(switch_over, "[temperature]"), "degC") if switch_over else None
        run = simulate_firing_run(kiln, switch_over_c=switch_c)
    except RESULT_ERRORS as e:
        raise ToolError(str(e)) from e
    return run.result.model_dump(mode="json", exclude={"points", "faces"}, exclude_none=True)


def _squashed(text: str) -> str:
    """Lower case, letters and digits only: 'Cross-draft' and 'crossdraft' are the same kind."""
    return "".join(c for c in text.lower() if c.isalnum())


@mcp.tool(annotations=READ_ONLY)
def start_design(
    fuel: Fuel,
    cone: str,
    stacking_volume: str,
    kind: str | None = None,
    budget_usd: float | None = None,
) -> dict[str, Any]:
    """Start a design from a spec: the template of that fuel (and kind, such as 'cross-draft',
    'catenary', 'car' or a template id) whose chamber is nearest the volume asked for, set to the
    cone. The volume is a quantity, for example '12 ft**3'. The template is not resized: its
    dimensions are to be changed in the design, then built. With a budget, the template's priced
    bill of materials is compared with it."""
    try:
        wanted = si(parse_quantity(stacking_volume, "[volume]"), "m**3")
    except UnitError as e:
        raise ToolError(str(e)) from e
    if wanted <= 0:
        raise ToolError("The stacking volume must be more than zero.")
    facts = [f for f in _template_facts() if f[2] == fuel]
    if not facts:
        raise ToolError(f"No template is fired with {fuel}.")
    working: list[Step] = []
    if kind:
        asked = _squashed(kind)
        matched = [
            f
            for f in facts
            if asked and asked in _squashed(f"{f[0].id} {f[0].title} {f[0].description}")
        ]
        working.append(
            Step(
                name="Kind",
                value=", ".join(f[0].id for f in matched) if matched else "none matched",
                inputs={"kind": kind, "fuel": fuel},
                note=None if matched else "Every template of the fuel was considered instead.",
            )
        )
        facts = matched or facts
    template, base, _, volume = min(facts, key=lambda f: abs(math.log(f[3] / wanted)))
    ft3 = 0.3048**3
    working.append(
        Step(
            name="Nearest template by chamber volume",
            value=template.id,
            formula="min |ln(V_template / V_asked)|",
            inputs={
                "V_asked": f"{wanted / ft3:.3g} ft³",
                **{f[0].id: f"{f[3] / ft3:.3g} ft³" for f in facts},
            },
            note=(
                "The chamber's volume, compared with the stacking volume asked for: the stacking "
                "volume is less by what the shelves, posts, firebox and bag walls take, which is "
                "not estimated here."
            ),
        )
    )
    working.append(
        Step(
            name="Chamber volume against the volume asked for",
            value=f"{volume / wanted:.2f}",
            formula="V_template / V_asked",
            inputs={"V_template": f"{volume / ft3:.3g} ft³", "V_asked": f"{wanted / ft3:.3g} ft³"},
            note="Change chamber.width, depth and height in the design to size it.",
        )
    )
    data: Any = yaml.safe_load(template.source)
    data["firing"] = {"cone": cone}
    try:
        kiln = Kiln.model_validate(data)
    except ValidationError as e:
        raise ToolError(f"Cone {cone!r} is refused for {template.id}:\n{e}") from e
    if kiln.firing.cone != base.firing.cone:
        working.append(Step(name="Cone", value=cone, inputs={"template's": str(base.firing.cone)}))
    result: dict[str, Any] = {
        "template": template.id,
        "title": template.title,
        "fuel": fuel,
        "cone": cone,
        "chamber_volume_ft3": round(volume / ft3, 2),
        "design": dump_design(kiln),
    }
    if budget_usd is not None:
        try:
            report = design_report(kiln)
        except RESULT_ERRORS as e:
            raise ToolError(str(e)) from e
        if report.bom is not None:
            unpriced = [line.item for line in report.bom.lines if line.cost is None]
            working.append(
                Step(
                    name="Priced materials against the budget",
                    value=f"${report.bom.total:,.0f} of ${budget_usd:,.0f}",
                    inputs={"prices checked": report.bom.prices_checked},
                    note=(
                        "The template as it stands, before it is resized. Not priced: "
                        + ", ".join(unpriced)
                        if unpriced
                        else "The template as it stands, before it is resized."
                    ),
                )
            )
            result["within_budget"] = report.bom.total <= budget_usd
    result["working"] = [s.model_dump(mode="json", exclude_none=True) for s in working]
    return result


def main() -> None:
    """Run the server: over stdio, or with --http on a local stateless Streamable HTTP endpoint."""
    if "--http" in sys.argv[1:]:
        mcp.run("streamable-http", host="127.0.0.1", stateless_http=True, json_response=True)
    else:
        mcp.run()
