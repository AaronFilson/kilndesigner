"""Plans: a PDF to build from (Typst), and a DXF of the sections for CAD.

The PDF is made from data and drawings only; its template is ``data/plans.typ``. Output is
deterministic: no dates are embedded, so the same design gives the same plans.
"""

from __future__ import annotations

import json
import tempfile
from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, cast

import typst

from kilndesigner.bom import Bom, bill_of_materials
from kilndesigner.charts import Marker, Series, line_chart
from kilndesigner.drawings import (
    course_plan_svg,
    ring_plan_svg,
    section_views,
    view_svg,
    write_dxf,
)
from kilndesigner.hybrid import CostPoint, HybridAnalysis
from kilndesigner.masonry import MasonryPlan, plan_masonry
from kilndesigner.model import Kiln
from kilndesigner.report import Report
from kilndesigner.round_masonry import RingPlan
from kilndesigner.sheet import Check, cell_text, requirement_text
from kilndesigner.working import Finding, Step

LAYING_WORDS = {
    "stretcher": "bricks laid flat along the wall, 2½ in courses",
    "on_edge": "bricks on edge",
    "header": "bricks laid through the wall, 4½ in along it",
    "flat": "bricks laid flat",
    "soldier": "bricks standing on end",
}


def hybrid_charts(h: HybridAnalysis, us: bool) -> dict[str, str]:
    def t(p: CostPoint) -> float:
        return p.temperature_f if us else p.temperature_c

    unit = "°F" if us else "°C"
    switch = h.switch_over_c * 9 / 5 + 32 if us else h.switch_over_c
    marker = [Marker(switch, f"switch-over, {h.switch_over}")]
    cost = [
        Series("Electricity", [(t(p), p.electric_per_kwh) for p in h.points]),
        Series("Propane, oxidising (3% O₂)", [(t(p), p.propane_per_kwh) for p in h.points]),
    ]
    reducing = [(t(p), p.propane_reducing_per_kwh) for p in h.points if p.propane_reducing_per_kwh]
    if reducing:
        cost.append(Series("Propane, reducing (λ 0.9)", reducing, dashed=True))  # type: ignore[arg-type]
    surplus = [Series("Element power left over", [(t(p), p.element_surplus_kw) for p in h.points])]
    return {
        "cost.svg": line_chart(
            cost,
            x_label=f"Kiln temperature ({unit})",
            y_label="$ per kWh kept in the kiln",
            markers=marker,
            y_format="${:.2f}",
        ),
        "surplus.svg": line_chart(
            surplus,
            x_label=f"Kiln temperature ({unit})",
            y_label="kW for heating ware and walls",
            markers=marker,
        ),
    }


@dataclass(frozen=True)
class Drawing:
    """A drawing in the plans, kept for the app too: a section, a course plan or a chart."""

    file: str
    kind: str  # "section", "course plan" or "chart"
    title: str
    description: str
    svg: str


@dataclass(frozen=True)
class Plans:
    pdf: bytes
    masonry: MasonryPlan
    bom: Bom
    drawings: tuple[Drawing, ...] = ()
    pages_png: tuple[bytes, ...] = ()


def _steps(steps: list[Step]) -> list[dict[str, Any]]:
    return [s.model_dump(mode="json") for s in steps]


def _finding(f: Finding) -> dict[str, Any]:
    """A finding as the plans list it, with its sheet's mark (E1, W2) in place of the sheet."""
    return f.model_dump(mode="json", exclude={"check"}) | {
        "label": f.check.label if f.check else None
    }


def _check(c: Check) -> dict[str, Any]:
    """A finding's sheet as the plans print it: every row, each requirement, what would pass."""
    return {
        "label": c.label,
        "title": c.title,
        "status": c.status,
        "rule": c.rule,
        "rule_met": c.rule_holds,
        "rows": [
            [
                x.symbol,
                x.meaning,
                f"{x.symbol} = {x.formula}" if x.formula else "",
                cell_text(x),
                x.source or "",
            ]
            for x in c.cells
        ],
        "requirements": [
            [requirement_text(r), "holds" if r.holds else f"fails ({r.level})", r.margin]
            for r in c.requirements
        ],
        "solve": c.solve,
        "reference": c.reference,
    }


def plan_data(kiln: Kiln, report: Report, masonry: MasonryPlan, bom: Bom) -> dict[str, Any]:
    us = kiln.units == "us"
    summary = [
        ["Chamber volume", report.chamber_volume],
        ["Top temperature", report.heat_loss.top_temperature],
        ["Air around the kiln", report.heat_loss.ambient],
        ["Heat loss at top temperature", report.heat_loss.total],
    ]
    elements: list[list[str]] | None = None
    if report.electric is not None:
        e = report.electric
        summary += [
            ["Supply", e.supply],
            ["Installed power", f"{e.installed_power} ({e.power_per_volume})"],
            ["Line current", e.line_current],
        ]
        if e.elements is not None:
            el = e.elements
            elements = [
                ["Alloy", e.alloy],
                ["Elements", f"{el.count}, wired as {el.wiring}"],
                ["Wire", f"{el.gauge} ({el.wire_diameter})"],
                ["Wire length, each", el.length_each],
                ["Resistance, each", f"{el.cold_resistance_each} cold, "
                 f"{el.hot_resistance_each} hot"],
                ["Power and current, each", f"{el.power_each}, {el.current_each}"],
                ["Surface load", el.surface_load],
                ["Coil", f"{el.turns_each} turns, {el.coil_outside_diameter} outside diameter"],
                ["Coil length", f"{el.close_wound_length_each} close-wound, "
                 f"stretched to {el.stretched_length_each}"],
                ["Pitch", el.pitch],
                ["Grooves", f"{el.groove_rows} rows, evenly spaced up the walls"],
                ["Wire, total", el.wire_mass_total],
            ]  # fmt: skip
    summary.append(["Materials (priced items)", f"${bom.total:,.0f}"])
    findings: list[Finding] = report.findings
    working = [{"title": "Heat loss", "steps": _steps(report.heat_loss.working)}]
    if report.electric is not None:
        working.append({"title": "Elements and circuit", "steps": _steps(report.electric.working)})
    gas: dict[str, Any] | None = None
    if report.gas is not None:
        g = report.gas
        working.append({"title": "Burners, propane and chimney", "steps": _steps(g.working)})
        rows = [
            ["Construction (Ward's classes)", g.construction],
            ["Chamber volume, Ward's way", g.ward_volume],
            ["Burner input, Ward's range", g.demand_range],
            ["Design burner input", g.design_input],
            [f"{g.fuel.capitalize()} at full fire", g.propane_at_full_fire],
        ]
        if g.burners is not None:
            b = g.burners
            rows.append(["Burners", f"{b.count} × {b.model} at {b.pressure} ({b.each} each)"])
        rows += [["Exit flue area", g.flue_area]]
        if g.chimney_height is not None:
            rows.append(["Chimney height", g.chimney_height])
        rows += [["Draft", line] for line in g.draft]
        if g.tank_suggestion is not None:
            rows.append(["A tank that would keep up", g.tank_suggestion])
        gas = {
            "rows": rows,
            "supply_temperature": g.supply_temperature,
            "supply": [s.model_dump(mode="json") for s in g.supply],
            "options": [o.model_dump(mode="json") for o in g.burner_options],
        }
        summary.append(["Burner input", g.design_input])
    hybrid: dict[str, Any] | None = None
    if report.hybrid is not None:
        h = report.hybrid
        working.append({"title": "Elements and burners together", "steps": _steps(h.working)})
        hybrid = {
            "rows": [
                ["Element power", h.element_power],
                ["Electric ceiling (upper bound)", h.electric_ceiling],
                ["Switch to the burners at", f"{h.switch_over}: {h.switch_over_reason}"],
                ["Same cost per useful kWh at", h.cost_crossover or "never in this firing"],
            ],
        }
        summary.append(["Switch from elements to burners", h.switch_over])
    f = report.frame
    frame: dict[str, Any] = {
        "title": "Case" if f.kind == "welded case" else "Steel frame",
        "rows": [[m.part, m.steel, str(m.count), f"{m.length_in:.1f} in"] for m in f.members],
        "thrust": f.thrust,
    }
    working.append({"title": frame["title"], "steps": _steps(f.working)})
    castables = [
        {
            "name": c.mix.name,
            "batch": [[b.name, b.mass, b.share] for b in c.mix.batch]
            + [["Water", c.mix.water, c.mix.water_share]],
            "rows": [
                [label, value]
                for label, value in (
                    ("Foam", c.mix.foam),
                    ("One batch casts", c.mix.cast_volume),
                    ("A level US quart weighs", c.mix.quart_weighs),
                    ("Dried / fired density", f"{c.mix.dried_density} / {c.mix.fired_density}"),
                    ("Conductivity (estimated)", "; ".join(c.mix.conductivity)),
                    ("Service limit", c.mix.service_limit or "not sourced: test it"),
                    ("Placed / batches", f"{c.placed} / {c.batches}"),
                )
                if value
            ],
            "steps": c.steps,
            "schedule": [[s.to, s.rate, s.hold or "—", s.why] for s in c.schedule],
            "layers": [f"{x.face}, {x.thickness}: {' '.join(x.notes)}" for x in c.layers],
        }
        for c in report.castables
    ]
    for c in report.castables:
        working.append(
            {"title": f"Castable: {c.mix.name}", "steps": _steps([*c.mix.working, *c.first_firing])}
        )
    return {
        "name": kiln.name,
        "engine_version": report.engine_version,
        "frame": frame,
        "castables": castables,
        "paper": "us-letter" if us else "a4",
        "summary": summary,
        "findings": [_finding(f) for f in findings],
        "checks": [_check(f.check) for f in findings if f.check is not None],
        "faces": [f.model_dump(mode="json") for f in report.heat_loss.faces],
        "elements": elements,
        "gas": gas,
        "hybrid": hybrid,
        "cut_list": [c.model_dump(mode="json") for c in masonry.result.cut_list],
        "bom": {
            "lines": [
                {
                    **line.model_dump(mode="json"),
                    "cost_text": f"${line.cost:,.2f}" if line.cost else None,
                }
                for line in bom.lines
            ],
            "total_text": f"${bom.total:,.2f}",
        },
        "working": working,
    }  # fmt: skip


def build_plans(
    kiln: Kiln, report: Report, dxf_path: Path | None = None, preview_ppi: int | None = None
) -> Plans:
    """The PDF plans, the DXF if a path is given, and PNG pages if ``preview_ppi`` is set."""
    us = kiln.units == "us"
    from kilndesigner.geometry import not_drawn
    from kilndesigner.hardware import build_hardware, floor_and_roof_holes

    holes = (
        floor_and_roof_holes(build_hardware(kiln, report.frame, report.gas, report.fire))
        if not_drawn(kiln) is None
        else []
    )
    masonry = plan_masonry(kiln, holes)
    bom = report.bom or bill_of_materials(kiln, masonry.result, report.electric)
    data = plan_data(kiln, report, masonry, bom)
    rows, coil = 0, 0.0
    if report.electric is not None and report.electric.elements is not None:
        rows = report.electric.elements.groove_rows
        coil = report.electric.elements.coil_outside_diameter_mm
    views = section_views(kiln, rows, coil)
    drawings: list[Drawing] = []
    with tempfile.TemporaryDirectory(prefix="kilndesigner-") as tmp:
        root = Path(tmp)
        data["views"] = []
        for i, view in enumerate(views):
            name = f"view-{i + 1}.svg"
            svg = view_svg(view)
            (root / name).write_text(svg, encoding="utf-8")
            data["views"].append({"title": view.title, "file": name})
            drawings.append(Drawing(name, "section", view.title, "", svg))
        data["course_plans"] = []
        data["round"] = bool(masonry.rings)
        for i, layer in enumerate(masonry.course_plans()):
            name = f"course-{i + 1}.svg"
            if isinstance(layer, RingPlan):
                svg = ring_plan_svg(layer, us)
                description = layer.description(us)
            else:
                svg = course_plan_svg(layer, us)
                pieces = layer.pieces
                cut = sum(1 for p in pieces if not p.is_whole)
                rows = "rows" if layer.circle is not None else "courses"
                description = (
                    f"{len(layer.courses)} {rows} of {LAYING_WORDS[layer.laying]}: "
                    f"{len(pieces) - cut} whole bricks and {cut} cut pieces."
                )
            (root / name).write_text(svg, encoding="utf-8")
            plan = {"title": layer.title(), "description": description, "file": name}
            data["course_plans"].append(plan)
            drawings.append(Drawing(name, "course plan", plan["title"], plan["description"], svg))
        if report.hybrid is not None:
            titles = {
                "cost.svg": "What a kWh kept in the kiln costs, from the elements and from propane",
                "surplus.svg": "Element power left for heating the ware and walls",
            }
            for name, svg in hybrid_charts(report.hybrid, us).items():
                (root / name).write_text(svg, encoding="utf-8")
                data["hybrid"]["charts"] = [*data["hybrid"].get("charts", []), name]
                drawings.append(Drawing(name, "chart", titles.get(name, name), "", svg))
        (root / "data.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        template = resources.files("kilndesigner.data").joinpath("plans.typ").read_text("utf-8")
        (root / "plans.typ").write_text(template, encoding="utf-8")
        pdf = typst.compile(str(root / "plans.typ"), root=str(root), format="pdf")
        pages: list[bytes] = []
        if preview_ppi is not None:
            png = typst.compile(
                str(root / "plans.typ"), root=str(root), format="png", ppi=preview_ppi
            )
            pages = list(cast("list[bytes]", png)) if isinstance(png, list) else [png]
    if dxf_path is not None:
        write_dxf(views, str(dxf_path), us)
    return Plans(
        pdf=pdf, masonry=masonry, bom=bom, drawings=tuple(drawings), pages_png=tuple(pages)
    )
