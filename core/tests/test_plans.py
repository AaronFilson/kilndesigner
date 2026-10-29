import re
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

import pytest

from kilndesigner import load_design, parse_design
from kilndesigner.drawings import course_plan_svg, section_views, view_svg
from kilndesigner.hybrid import HybridAnalysis, analyse_hybrid
from kilndesigner.masonry import plan_masonry
from kilndesigner.model import Kiln
from kilndesigner.plans import LAYING_WORDS, Plans, build_plans, hybrid_charts, plan_data
from kilndesigner.report import Report, design_report

EXAMPLES = Path(__file__).parents[2] / "examples"
SVG = "{http://www.w3.org/2000/svg}"


@pytest.fixture(scope="module")
def kiln():  # type: ignore[no-untyped-def]
    return load_design(EXAMPLES / "electric-front-loader.yaml")


def test_sections_cut_the_right_parts(kiln) -> None:  # type: ignore[no-untyped-def]
    front, side, plan = section_views(kiln, element_rows=9, coil_mm=10)
    front_parts = {r.layer.split("/")[0] for r in front.rects}
    assert front_parts == {"floor", "left", "right", "roof"}
    side_parts = {r.layer.split("/")[0] for r in side.rects}
    assert side_parts == {"floor", "back", "door", "roof"}
    assert {r.layer.split("/")[0] for r in plan.rects} == {"left", "right", "back", "door"}
    # elements on the left and right walls show in section A–A; on the back wall in B–B
    assert len(front.circles) == 18
    assert len(side.circles) == 9


def test_svgs_are_well_formed(kiln) -> None:  # type: ignore[no-untyped-def]
    for view in section_views(kiln):
        ElementTree.fromstring(view_svg(view))
    for layer in plan_masonry(kiln).layers:
        root = ElementTree.fromstring(course_plan_svg(layer, us=True))
        rects = root.findall(".//{http://www.w3.org/2000/svg}rect")
        assert len(rects) == len(layer.pieces)


def test_plans_compile_and_are_deterministic(kiln, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    report = design_report(kiln)
    first = build_plans(kiln, report, dxf_path=tmp_path / "a.dxf")
    second = build_plans(kiln, report)
    assert first.pdf.startswith(b"%PDF")
    assert first.pdf == second.pdf
    assert first.pages_png == ()  # PNG pages only when a preview is asked for
    assert (tmp_path / "a.dxf").read_text(encoding="utf-8").startswith("  0\nSECTION")


def test_dxf_has_a_layer_per_part(kiln, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    from ezdxf.filemanagement import readfile  # pyright: ignore[reportMissingTypeStubs]

    build_plans(kiln, design_report(kiln), dxf_path=tmp_path / "s.dxf")
    doc = readfile(tmp_path / "s.dxf")
    names = {layer.dxf.name for layer in doc.layers}
    assert "left_1-ifb-jm26" in names
    assert "dimensions" in names


def _variant(name: str, *changes: tuple[str, str]) -> Kiln:
    text = (EXAMPLES / f"{name}.yaml").read_text(encoding="utf-8")
    for old, new in changes:
        assert old in text
        text = text.replace(old, new)
    return parse_design(text)


def _data(kiln: Kiln, report: Report) -> dict[str, Any]:
    assert report.bom is not None
    return plan_data(kiln, report, plan_masonry(kiln), report.bom)


def _labels(rows: list[list[Any]]) -> list[str]:
    return [row[0] for row in rows]


def _row(rows: list[list[Any]], label: str) -> Any:
    (value,) = [row[1] for row in rows if row[0] == label]
    return value


def _titles(data: dict[str, Any]) -> list[str]:
    return [w["title"] for w in data["working"]]


@pytest.fixture(scope="module")
def hybrid() -> tuple[Kiln, Report]:
    kiln = load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml")
    return kiln, design_report(kiln)


@pytest.fixture(scope="module")
def hybrid_plans(hybrid: tuple[Kiln, Report]) -> Plans:
    return build_plans(*hybrid, preview_ppi=10)


def test_an_electric_kilns_plans_list_its_elements(kiln) -> None:  # type: ignore[no-untyped-def]
    report = design_report(kiln)
    data = _data(kiln, report)
    e = report.electric
    assert e is not None
    assert e.elements is not None
    summary = data["summary"]
    assert _labels(summary) == [
        "Chamber volume",
        "Top temperature",
        "Air around the kiln",
        "Heat loss at top temperature",
        "Supply",
        "Installed power",
        "Line current",
        "Materials (priced items)",
    ]
    assert _row(summary, "Chamber volume") == "7.03 ft³"  # 22.5 × 22.5 × 24 in
    assert _row(summary, "Installed power") == f"{e.installed_power} ({e.power_per_volume})"
    assert report.bom is not None
    assert _row(summary, "Materials (priced items)") == f"${report.bom.total:,.0f}"
    assert _row(data["elements"], "Elements") == (
        f"{e.elements.count}, wired as {e.elements.wiring}"
    )
    assert data["gas"] is None
    assert data["hybrid"] is None
    assert data["paper"] == "us-letter"
    # A welded case, not a frame
    assert _titles(data) == ["Heat loss", "Elements and circuit", "Case"]


def test_an_electric_kiln_whose_elements_dont_fit_has_no_element_table() -> None:
    # 40 elements is more rows than the 24 in walls hold
    walls = "walls: [left, right, back]"
    kiln = _variant("electric-front-loader", (walls, f"{walls}\n    elements: 40"))
    report = design_report(kiln)
    assert report.electric is not None
    assert report.electric.elements is None
    data = _data(kiln, report)
    assert data["elements"] is None
    assert {"Supply", "Installed power", "Line current"} <= set(_labels(data["summary"]))
    assert "Elements and circuit" in _titles(data)


def test_a_hybrids_plans_have_the_burners_and_the_hand_over(
    hybrid: tuple[Kiln, Report],
) -> None:
    kiln, report = hybrid
    data = _data(kiln, report)
    g, h = report.gas, report.hybrid
    assert g is not None
    assert h is not None
    gas = data["gas"]
    assert isinstance(gas, dict)
    assert _labels(gas["rows"]) == [
        "Construction (Ward's classes)",
        "Chamber volume, Ward's way",
        "Burner input, Ward's range",
        "Design burner input",
        "Propane at full fire",
        "Burners",
        "Exit flue area",
        "Chimney height",
        "Draft",
        "Draft",
        "A tank that would keep up",
    ]
    assert g.burners is not None
    b = g.burners
    assert _row(gas["rows"], "Burners") == f"{b.count} × {b.model} at {b.pressure} ({b.each} each)"
    assert len(gas["options"]) == len(g.burner_options)
    hybrid_rows = data["hybrid"]
    assert isinstance(hybrid_rows, dict)
    # The design hands over at its off_above, 1650 °F
    assert _row(hybrid_rows["rows"], "Switch to the burners at") == (
        f"1650 °F: {h.switch_over_reason}"
    )
    assert h.cost_crossover is None
    assert _row(hybrid_rows["rows"], "Same cost per useful kWh at") == "never in this firing"
    assert _row(data["summary"], "Switch from elements to burners") == "1650 °F"
    assert _row(data["summary"], "Burner input") == g.design_input
    assert _titles(data) == [
        "Heat loss",
        "Elements and circuit",
        "Burners, propane and chimney",
        "Elements and burners together",
        "Steel frame",
    ]


def test_a_gas_kiln_without_burners_chimney_or_tank() -> None:
    # No library burner is rated for natural gas at 2 psi, an up-draft has no chimney sized here,
    # and a line needs no tank
    kiln = _variant(
        "gas-crossdraft",
        ("depth: 48 in", "depth: 60 in"),
        ("height: 40 in", "height: 44 in"),
        ("  gas:\n", "  gas:\n    fuel: natural_gas\n"),
        ("type: cylinders\n      count: 4", "type: line\n      pressure: 2 psi"),
        ("  type: cross\n", "  type: up\n"),
    )
    report = design_report(kiln)
    g = report.gas
    assert g is not None
    assert (g.burners, g.chimney_height, g.tank_suggestion, g.draft) == (None, None, None, [])
    data = _data(kiln, report)
    gas = data["gas"]
    assert isinstance(gas, dict)
    assert _labels(gas["rows"]) == [
        "Construction (Ward's classes)",
        "Chamber volume, Ward's way",
        "Burner input, Ward's range",
        "Design burner input",
        "Natural gas at full fire",
        "Exit flue area",
    ]
    assert data["elements"] is None
    assert data["hybrid"] is None
    assert "Supply" not in _labels(data["summary"])
    assert _titles(data) == ["Heat loss", "Burners, propane and chimney", "Steel frame"]


def test_castables_get_their_batches_schedule_and_working() -> None:
    kiln = load_design(EXAMPLES / "diy-castable-test-kiln.yaml")
    report = design_report(kiln)
    data = _data(kiln, report)
    castables = data["castables"]
    assert isinstance(castables, list)
    assert [c["name"] for c in castables] == [m.name for m in kiln.castables or []]
    for c, r in zip(castables, report.castables, strict=True):  # pyright: ignore[reportUnknownVariableType]
        # The batch: each ingredient, then the water
        assert [row[0] for row in c["batch"]] == [*(b.name for b in r.mix.batch), "Water"]
        assert c["batch"][-1][1] == r.mix.water
        assert _row(c["rows"], "Placed / batches") == f"{r.placed} / {r.batches}"
        assert len(c["schedule"]) == len(r.schedule)
        assert len(c["layers"]) == len(r.layers)
    titles = _titles(data)
    assert [t for t in titles if t.startswith("Castable: ")] == [
        f"Castable: {m.name}" for m in kiln.castables or []
    ]


def _svg(text: str) -> ElementTree.Element:
    return ElementTree.fromstring(text)


def test_the_hybrid_charts_show_each_fuels_cost(hybrid: tuple[Kiln, Report]) -> None:
    h = hybrid[1].hybrid
    assert h is not None
    charts = hybrid_charts(h, us=True)
    assert set(charts) == {"cost.svg", "surplus.svg"}
    cost = _svg(charts["cost.svg"])
    lines = list(cost.iter(f"{SVG}polyline"))
    reducing = [p for p in h.points if p.propane_reducing_per_kwh]
    assert reducing  # the design reduces, so a third, dashed line
    assert [len(x.get("points", "").split()) for x in lines] == [
        len(h.points),
        len(h.points),
        len(reducing),
    ]
    assert [x.get("stroke-dasharray") for x in lines] == [None, None, "6 4"]
    texts = [t.text for t in cost.iter(f"{SVG}text")]
    assert {
        "Electricity",
        "Propane, oxidising (3% O₂)",
        "Propane, reducing (λ 0.9)",
        "switch-over, 1650 °F",
        "Kiln temperature (°F)",
        "$ per kWh kept in the kiln",
    } <= set(texts)
    surplus = _svg(charts["surplus.svg"])
    (line,) = surplus.iter(f"{SVG}polyline")
    assert len(line.get("points", "").split()) == len(h.points)
    assert "kW for heating ware and walls" in [t.text for t in surplus.iter(f"{SVG}text")]


def test_metric_hybrid_charts_are_the_same_picture_in_celsius(
    hybrid: tuple[Kiln, Report],
) -> None:
    h = hybrid[1].hybrid
    assert h is not None
    us, metric = hybrid_charts(h, us=True), hybrid_charts(h, us=False)
    for name in ("cost.svg", "surplus.svg"):
        a, b = _svg(us[name]), _svg(metric[name])
        # °F and °C are a straight-line change of scale, so every line lands in the same place
        assert [x.get("points") for x in a.iter(f"{SVG}polyline")] == [
            x.get("points") for x in b.iter(f"{SVG}polyline")
        ]
        marker = [x for x in b.iter(f"{SVG}line") if x.get("stroke-dasharray") == "4 3"]
        assert [x.get("x1") for x in marker] == [
            x.get("x1") for x in a.iter(f"{SVG}line") if x.get("stroke-dasharray") == "4 3"
        ]
        assert "Kiln temperature (°C)" in [t.text for t in b.iter(f"{SVG}text")]


def test_without_reduction_the_cost_chart_has_two_lines(hybrid: tuple[Kiln, Report]) -> None:
    kiln, report = hybrid
    gas = kiln.heat.gas
    assert gas is not None
    assert report.electric is not None
    # Only the burners change, so the elements stay as the report designed them
    heat = kiln.heat.model_copy(update={"gas": gas.model_copy(update={"reduction": False})})
    oxidising = kiln.model_copy(update={"heat": heat})
    h: HybridAnalysis = analyse_hybrid(oxidising, report.electric.installed_watts)
    assert not [p for p in h.points if p.propane_reducing_per_kwh]
    cost = _svg(hybrid_charts(h, us=True)["cost.svg"])
    assert len(list(cost.iter(f"{SVG}polyline"))) == 2
    assert "Propane, reducing (λ 0.9)" not in [t.text for t in cost.iter(f"{SVG}text")]


def test_a_hybrids_plans_carry_its_drawings_and_charts(
    hybrid: tuple[Kiln, Report], hybrid_plans: Plans
) -> None:
    kiln = hybrid[0]
    kinds = [d.kind for d in hybrid_plans.drawings]
    layers = plan_masonry(kiln).layers
    assert kinds == ["section"] * 3 + ["course plan"] * len(layers) + ["chart"] * 2
    sections = hybrid_plans.drawings[:3]
    assert [d.file for d in sections] == ["view-1.svg", "view-2.svg", "view-3.svg"]
    assert [d.title for d in sections] == [v.title for v in section_views(kiln)]
    for d, layer in zip(hybrid_plans.drawings[3:-2], layers, strict=True):
        cut = sum(1 for p in layer.pieces if not p.is_whole)
        assert d.title == layer.title()
        assert d.description == (
            f"{len(layer.courses)} courses of {LAYING_WORDS[layer.laying]}: "
            f"{len(layer.pieces) - cut} whole bricks and {cut} cut pieces."
        )
        assert d.svg == course_plan_svg(layer, us=True)
    charts = hybrid_plans.drawings[-2:]
    assert [(d.file, d.title) for d in charts] == [
        ("cost.svg", "What a kWh kept in the kiln costs, from the elements and from propane"),
        ("surplus.svg", "Element power left for heating the ware and walls"),
    ]
    h = hybrid[1].hybrid
    assert h is not None
    assert [d.svg for d in charts] == list(hybrid_charts(h, us=True).values())
    for d in hybrid_plans.drawings:
        ElementTree.fromstring(d.svg)


def test_preview_pages_are_one_png_per_pdf_page(hybrid_plans: Plans) -> None:
    pages = len(re.findall(rb"/Type\s*/Page\b(?!s)", hybrid_plans.pdf))
    assert pages > 1
    assert len(hybrid_plans.pages_png) == pages
    assert all(p.startswith(b"\x89PNG\r\n\x1a\n") for p in hybrid_plans.pages_png)


def test_a_gas_kiln_compiles_with_its_castables_and_no_elements(tmp_path: Path) -> None:
    kiln = load_design(EXAMPLES / "diy-castable-test-kiln.yaml")
    plans = build_plans(kiln, design_report(kiln), dxf_path=tmp_path / "s.dxf")
    assert plans.pdf.startswith(b"%PDF")
    sections = [d for d in plans.drawings if d.kind == "section"]
    assert len(sections) == 3
    assert "<circle" not in "".join(d.svg for d in sections)  # no elements to draw
    assert not [d for d in plans.drawings if d.kind == "chart"]
    assert (tmp_path / "s.dxf").exists()
