from pathlib import Path

import pytest

from kilndesigner import load_design, parse_design
from kilndesigner.geometry import (
    GeometryNotSupportedError,
    build_model,
    element_runs,
    export_model,
    lining_parts,
)

EXAMPLES = Path(__file__).parents[2] / "examples"
IN = 25.4


@pytest.fixture(scope="module")
def kiln():  # type: ignore[no-untyped-def]
    return load_design(EXAMPLES / "electric-front-loader.yaml")


def test_lining_parts_fill_the_shell_without_overlap(kiln) -> None:  # type: ignore[no-untyped-def]
    parts = lining_parts(kiln)
    lo = [min(p.lo[i] for p in parts) for i in range(3)]
    hi = [max(p.hi[i] for p in parts) for i in range(3)]
    outside = (hi[0] - lo[0]) * (hi[1] - lo[1]) * (hi[2] - lo[2])
    inside = (22.5 * IN) * (22.5 * IN) * (24 * IN)
    # Boxes that tile the shell exactly: their volumes add up to outside minus inside.
    assert sum(p.volume for p in parts) == pytest.approx(outside - inside, rel=1e-9)
    # 22.5 in + 2 × 5.5 in walls
    assert hi[0] - lo[0] == pytest.approx(33.5 * IN)
    # 24 in + 7 in floor + 5.5 in roof
    assert hi[2] - lo[2] == pytest.approx(36.5 * IN)


def test_parts_are_named_by_face_and_layer(kiln) -> None:  # type: ignore[no-untyped-def]
    names = [p.name for p in lining_parts(kiln)]
    assert "door/1-ifb-jm26" in names
    assert "floor/2-ifb-k23" in names
    assert len(names) == len(set(names)) == 12


def test_element_runs_follow_the_element_walls(kiln) -> None:  # type: ignore[no-untyped-def]
    runs = element_runs(kiln, 3, 10.0)
    assert len(runs) == 3
    # left, back, right: four corners, three straight runs
    assert len(runs[0].path) == 4
    assert runs[0].path[0][2] == pytest.approx(24 * IN / 6)


def test_arched_roofs_are_not_modelled_yet() -> None:
    text = (EXAMPLES / "electric-front-loader.yaml").read_text(encoding="utf-8")
    arched = parse_design(text.replace("type: flat", "type: sprung_arch\n  rise: 3 in"))
    with pytest.raises(GeometryNotSupportedError):
        lining_parts(arched)


@pytest.mark.geometry
def test_model_builds_and_exports(kiln, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    model = build_model(kiln, element_runs(kiln, 2, 10.0))
    labels = [c.label for c in model.children]
    assert "element/2" in labels
    lining_volume = sum(p.volume for p in lining_parts(kiln))
    lining = [c for c in model.children if not c.label.startswith("element")]
    assert sum(c.volume for c in lining) == pytest.approx(lining_volume, rel=1e-6)
    files = export_model(model, tmp_path)
    assert files["step"].stat().st_size > 1000
    assert files["gltf"].read_bytes()[:4] == b"glTF"
