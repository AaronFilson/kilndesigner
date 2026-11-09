"""The MCP server: the engine's design, report and firing tools for AI assistants (ADR 0016).

Every tool runs the engine on what it is given and stores nothing. A result is the engine's own
model, dumped to JSON with its working (the steps, formulas, inputs and references) and its
findings, as structured content and as the same JSON in text. A design the engine refuses comes
back as a tool error with the engine's reason, never a guess (ADR 0009).
"""

from __future__ import annotations

import json
import math
import os
import sys
from functools import cache
from pathlib import Path
from typing import Any, Literal

import yaml
from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ResourceError, ToolError
from mcp.types import ToolAnnotations
from pydantic import ValidationError

from kilndesigner import Kiln
from kilndesigner.castable import CastableError
from kilndesigner.compare import COMPARED, comparison_rows
from kilndesigner.designfile import dump_design, parse_design
from kilndesigner.library import UnknownEntryError, alloys, material, materials
from kilndesigner.report import ENGINE_VERSION, Report, design_report
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
working around it. compare_designs sets designs side by side. The resources hold the design
file's JSON Schema, the materials library with its sources, and the formula sheet behind each
warning and error of a template or example. The bill of materials prices only what has a price
in the library; unpriced lines are not free."""

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


def _template(id: str) -> Template:
    for t in templates():
        if t.id == id:
            return t
    ids = ", ".join(t.id for t in templates())
    raise ToolError(f"No template {id!r}. The templates are: {ids}")


@mcp.tool(annotations=READ_ONLY)
def get_template(id: str) -> dict[str, Any]:
    """A template's design file (YAML), to change and build."""
    t = _template(id)
    return {"id": t.id, "title": t.title, "design": t.source}


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


def _example(name: str) -> str:
    folder = _examples_folder()
    if folder is not None:
        path = (folder / f"{name}.yaml").resolve()
        if path.is_relative_to(folder.resolve()) and path.is_file():
            return path.read_text(encoding="utf-8")
    raise ToolError(f"No example {name!r}; list_examples gives the names.")


@mcp.tool(annotations=READ_ONLY)
def get_example(name: str) -> dict[str, Any]:
    """An example's design file (YAML), by the name list_examples gives."""
    return {"name": name, "design": _example(name)}


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


def _design_text(ref: str) -> tuple[str, str]:
    """(a label, the YAML) for 'template:<id>', 'example:<name>' or a design's YAML itself."""
    if ref.startswith("template:"):
        tid = ref.removeprefix("template:").strip()
        return tid, _template(tid).source
    if ref.startswith("example:"):
        name = ref.removeprefix("example:").strip()
        return name, _example(name)
    return "", ref


def _steps(steps: list[Step]) -> list[dict[str, Any]]:
    return [s.model_dump(mode="json", exclude_none=True) for s in steps]


def _compared(report: Report) -> dict[str, Any]:
    """The working behind each headline row: the report's own steps, not new ones."""
    working: dict[str, Any] = {"Heat loss at top": _steps(report.heat_loss.working)}
    if report.electric is not None:
        working["Installed power"] = _steps(report.electric.working)
    if report.gas is not None:
        working["Burner input"] = _steps(report.gas.working)
    if report.hybrid is not None:
        working["Switch to burners at"] = _steps(report.hybrid.working)
    if report.bom is not None:
        working["Materials (priced)"] = report.bom.model_dump(
            mode="json", exclude={"findings"}, exclude_none=True
        )
    return working


FIRING_FIELDS = {
    "heat",
    "duration",
    "duration_h",
    "completed",
    "held",
    "energy_kwh",
    "electricity_kwh",
    "fuel_kwh",
    "propane_gallons",
    "natural_gas_therms",
    "cost",
    "cost_usd",
    "working",
    "findings",
}


@mcp.tool(annotations=READ_ONLY)
def compare_designs(designs: list[str], simulate: bool = False) -> dict[str, Any]:
    """Build two or more designs and set them side by side: chamber volume, heat loss, the hottest
    outside face, installed power or burner input, priced materials and the findings, each row
    with the engine's working. Each design is its YAML, 'template:<id>' or 'example:<name>'. With
    simulate, each design's firing is simulated too: time, energy, fuel and cost per firing. The
    stacking volume is not estimated: the chamber volume is compared."""
    if len(designs) < 2:
        raise ToolError("Give two or more designs to compare.")
    out: list[dict[str, Any]] = []
    for i, ref in enumerate(designs, start=1):
        label, text = _design_text(ref)
        kiln = _parse(text)
        try:
            report = design_report(kiln)
        except RESULT_ERRORS as e:
            raise ToolError(f"Design {i} ({label or kiln.name}): {e}") from e
        entry: dict[str, Any] = {
            "design": label or kiln.name,
            "name": kiln.name,
            "fuel": _fuel(kiln),
            "cone": _cone(kiln),
            "rows": comparison_rows(report),
            "working": _compared(report),
            "findings": [f.model_dump(mode="json", exclude_none=True) for f in report.findings],
        }
        if simulate:
            try:
                run = simulate_firing_run(kiln)
            except RESULT_ERRORS as e:
                entry["firing"] = {"refused": str(e)}
            else:
                entry["firing"] = run.result.model_dump(
                    mode="json", include=FIRING_FIELDS, exclude_none=True
                )
        out.append(entry)
    rows = [label for label in COMPARED if any(label in d["rows"] for d in out)]
    return {
        "rows": rows,
        "table": {label: [d["rows"].get(label) for d in out] for label in rows},
        "designs": out,
        "note": (
            "A missing cell (null) is a number the design has no part for. Priced materials leave "
            "out what the library has no price for; those lines are not free."
        ),
    }


# ---- Resources -------------------------------------------------------------------------------


@mcp.resource(
    "kilndesigner://schema/design",
    title="Design file JSON Schema",
    description="The JSON Schema of a design file: every field, its unit and its limits.",
    mime_type="application/json",
)
def design_schema() -> str:
    return json.dumps(Kiln.model_json_schema(by_alias=True), indent=2)


@mcp.resource(
    "kilndesigner://materials",
    title="Materials library",
    description=(
        "Every refractory and insulation material the engine knows, with its density, service "
        "limit, conductivity and specific heat points and the source each comes from."
    ),
    mime_type="application/json",
)
def materials_resource() -> str:
    return json.dumps(
        {"materials": [m.model_dump(mode="json") for m in materials().values()]}, indent=2
    )


@mcp.resource(
    "kilndesigner://materials/{id}",
    title="One material",
    description="A material from the library by its id, with its cited values.",
    mime_type="application/json",
)
def material_resource(id: str) -> str:
    try:
        return json.dumps(material(id).model_dump(mode="json"), indent=2)
    except UnknownEntryError as e:
        raise ResourceError(str(e)) from e


@mcp.resource(
    "kilndesigner://alloys",
    title="Element alloys",
    description="The element wire alloys, with resistivity, temperature limits and sources.",
    mime_type="application/json",
)
def alloys_resource() -> str:
    return json.dumps({"alloys": [a.model_dump(mode="json") for a in alloys().values()]}, indent=2)


def _checks(text: str) -> str:
    try:
        report = design_report(_parse(text))
    except (*RESULT_ERRORS, ToolError) as e:
        raise ResourceError(str(e)) from e
    sheets = [
        {"level": f.level, "message": f.message, "check": f.check.model_dump(mode="json")}
        for f in report.findings
        if f.check is not None
    ]
    return json.dumps(
        {
            "design": report.name,
            "about": (
                "The formula sheet behind each warning and error, and behind any note that has "
                "one (ADR 0013): its input cells with value, "
                "unit and source, formula cells over them (values in SI), the requirements and "
                "the lever, the input that would change the result."
            ),
            "checks": sheets,
        },
        indent=2,
    )


@mcp.resource(
    "kilndesigner://templates/{id}/checks",
    title="A template's formula sheets",
    description="The formula sheets behind a template's warnings and errors (ADR 0013).",
    mime_type="application/json",
)
def template_checks(id: str) -> str:
    try:
        source = _template(id).source
    except ToolError as e:
        raise ResourceError(str(e)) from e
    return _checks(source)


@mcp.resource(
    "kilndesigner://examples/{name}/checks",
    title="An example's formula sheets",
    description=(
        "The formula sheets behind an example's warnings and errors (ADR 0013). Examples in "
        "examples/ itself; for one in a subfolder, build_design carries the same checks."
    ),
    mime_type="application/json",
)
def example_checks(name: str) -> str:
    try:
        source = _example(name)
    except ToolError as e:
        raise ResourceError(str(e)) from e
    return _checks(source)


# ---- Prompts ---------------------------------------------------------------------------------


@mcp.prompt(title="Design a kiln from a brief")
def design_from_brief(brief: str) -> str:
    """Walk through designing a kiln from a potter's brief: start, resize, build, compare."""
    return f"""\
Design a kiln for this brief, with the kilndesigner tools:

{brief}

1. Read from the brief the fuel, the cone, the stacking volume and any budget or kind of kiln
   (cross-draft, catenary, car, front-loader). Ask for what the brief doesn't say rather than
   guessing; firing time is the potter's choice, not a fault.
2. Call start_design with them. It returns the nearest template's design file, not resized.
3. Change chamber.width, depth and height in the YAML to the size wanted, then call
   validate_design and fix what it reports.
4. Call build_design. Report the heat loss, the elements or burners, the priced materials and
   every error and warning, quoting the working and its references. Fix errors in the design and
   build again; don't work around a refusal, pass its reason on.
5. If there is more than one way to meet the brief (another kind, a thicker wall, another fuel),
   call compare_designs on them (simulate=true for the firing time, energy and cost) and set out
   the trade-offs, number by number, with where each number comes from.
6. Unpriced lines in the bill of materials are not free; say which they are."""


@mcp.prompt(title="Explain a finding")
def explain_finding(design: str, finding: str) -> str:
    """Explain one of a design's warnings or errors from its formula sheet."""
    return f"""\
Explain this finding of a kiln design to the builder: {finding}

The design file:

```yaml
{design}
```

Call build_design on the design and find the finding (by its label, such as E1 or W2, or its
message). Explain it from its check, the formula sheet behind it (ADR 0013): each input with its
value, unit and source, each formula, the requirement that fails and by how much (its margin),
and, if the check names a lever, the value at which it would pass. Say which change to the design
would move that input, and quote the references. Don't add numbers the sheet doesn't give."""


def main() -> None:
    """Run the server: over stdio, or with --http on a local stateless Streamable HTTP endpoint."""
    if "--http" in sys.argv[1:]:
        mcp.run("streamable-http", host="127.0.0.1", stateless_http=True, json_response=True)
    else:
        mcp.run()
