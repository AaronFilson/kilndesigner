import json
from pathlib import Path
from xml.etree import ElementTree

import pytest

from kilndesigner import load_design, parse_design
from kilndesigner.build import DRAWINGS, BuildResult, build_design, build_key, design_document
from kilndesigner.geometry import GeometryNotSupportedError, lining_parts

EXAMPLES = Path(__file__).parents[2] / "examples"


def test_the_build_key_ignores_yaml_formatting() -> None:
    path = EXAMPLES / "electric-front-loader.yaml"
    kiln = load_design(path)
    text = path.read_text(encoding="utf-8")
    reformatted = parse_design("# a comment\n" + text.replace("\n\n", "\n"))
    assert build_key(reformatted) == build_key(kiln)


def test_the_build_key_changes_with_the_design() -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    renamed = kiln.model_copy(update={"name": kiln.name + " (copy)"})
    assert build_key(renamed) != build_key(kiln)


def test_the_build_key_changes_with_the_engine(monkeypatch: pytest.MonkeyPatch) -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    before = build_key(kiln)
    monkeypatch.setattr("kilndesigner.build.engine_fingerprint", lambda: "changed code")
    assert build_key(kiln) != before


def test_the_document_round_trips() -> None:
    kiln = load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml")
    assert type(kiln).model_validate(design_document(kiln)) == kiln


def test_a_build_without_model_or_plans_writes_the_report(tmp_path: Path) -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    result = build_design(kiln, tmp_path, model=False, plans=False)
    # The report, and the workbook of its warning's sheet (the case band, W1)
    assert result.written == [tmp_path / "report.json", tmp_path / "checks.xlsx"]
    assert result.notes == []


@pytest.fixture(scope="module")
def plans_build(tmp_path_factory: pytest.TempPathFactory) -> tuple[Path, BuildResult]:
    out = tmp_path_factory.mktemp("plans") / "build"  # not there yet: the build makes it
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    return out, build_design(kiln, out, model=False, plans=True)


def test_a_plans_build_writes_the_pdf_the_dxf_and_the_drawings(
    plans_build: tuple[Path, BuildResult],
) -> None:
    out, result = plans_build
    assert result.notes == []
    drawings = out / DRAWINGS
    svgs = sorted(drawings.glob("*.svg"))
    assert result.written[:5] == [
        out / "report.json",
        out / "checks.xlsx",
        out / "plans.pdf",
        out / "sections.dxf",
        drawings / "index.json",
    ]
    assert sorted(result.written[5:]) == svgs
    assert {p.name for p in svgs} >= {"view-1.svg", "view-2.svg", "view-3.svg", "course-1.svg"}
    assert all(p.is_file() for p in result.written)
    assert (out / "plans.pdf").read_bytes().startswith(b"%PDF")
    assert (out / "sections.dxf").read_text(encoding="utf-8").startswith("  0\nSECTION")


def test_the_report_file_is_the_report(plans_build: tuple[Path, BuildResult]) -> None:
    out, result = plans_build
    written = json.loads((out / "report.json").read_text(encoding="utf-8"))
    assert written == result.report.model_dump(mode="json")
    assert written["name"] == "Electric front-loader, cone 10"


def test_the_drawings_index_describes_each_svg(plans_build: tuple[Path, BuildResult]) -> None:
    out, result = plans_build
    folder = out / DRAWINGS
    index = json.loads((folder / "index.json").read_text(encoding="utf-8"))
    assert [folder / d["file"] for d in index] == result.written[5:]
    assert [d["kind"] for d in index[:3]] == ["section"] * 3
    assert {d["kind"] for d in index[3:]} == {"course plan"}
    assert index[0]["title"] == "Section A–A: across the kiln, looking at the back"
    for d in index:
        assert set(d) == {"file", "kind", "title", "description"}
        root = ElementTree.fromstring((folder / d["file"]).read_text(encoding="utf-8"))
        assert root.tag == "{http://www.w3.org/2000/svg}svg"
    # A course plan says what it's made of: "N courses of … whole bricks and … cut pieces."
    assert all("whole bricks" in d["description"] for d in index[3:])


def test_a_shape_without_a_3d_model_is_noted(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    def no_model(*args: object) -> dict[str, Path]:
        raise GeometryNotSupportedError("this roof has no solid model yet")

    monkeypatch.setattr("kilndesigner.geometry.write_model", no_model)
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    result = build_design(kiln, tmp_path, model=True, plans=False)
    assert result.notes == ["No 3D model: this roof has no solid model yet"]
    assert result.written == [tmp_path / "report.json", tmp_path / "checks.xlsx"]


def test_a_shape_without_plans_is_noted(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    def no_plans(*args: object, **kwargs: object) -> object:
        raise GeometryNotSupportedError("this roof can't be drawn yet")

    monkeypatch.setattr("kilndesigner.plans.build_plans", no_plans)
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    result = build_design(kiln, tmp_path, model=False, plans=True)
    assert result.notes == ["No plans: this roof can't be drawn yet"]
    assert result.written == [tmp_path / "report.json", tmp_path / "checks.xlsx"]
    assert not (tmp_path / "plans.pdf").exists()
    assert not (tmp_path / DRAWINGS).exists()


@pytest.mark.geometry
def test_a_model_build_writes_the_model_and_what_each_part_is(tmp_path: Path) -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    result = build_design(kiln, tmp_path, model=True, plans=False)
    assert result.notes == []
    assert result.written == [
        tmp_path / "report.json",
        tmp_path / "checks.xlsx",
        tmp_path / "kiln.step",
        tmp_path / "kiln.glb",
        tmp_path / "parts.json",
        tmp_path / "layout.json",
    ]
    assert (tmp_path / "kiln.glb").read_bytes()[:4] == b"glTF"
    assert (tmp_path / "kiln.step").read_text(encoding="utf-8").startswith("ISO-10303-21;")
    parts = json.loads((tmp_path / "parts.json").read_text(encoding="utf-8"))
    assert {p.name for p in lining_parts(kiln)} <= set(parts)
    electric = result.report.electric
    assert electric is not None
    assert electric.elements is not None
    count = electric.elements.count
    assert {f"element/{i + 1}" for i in range(count)} <= set(parts)
