from pathlib import Path

from kilndesigner import load_design, parse_design
from kilndesigner.build import build_design, build_key, design_document

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


def test_the_document_round_trips() -> None:
    kiln = load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml")
    assert type(kiln).model_validate(design_document(kiln)) == kiln


def test_a_build_without_model_or_plans_writes_the_report(tmp_path: Path) -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    result = build_design(kiln, tmp_path, model=False, plans=False)
    assert result.written == [tmp_path / "report.json"]
    assert result.notes == []
