"""The setting: shelves and posts weighed from Olsen's shelf weights, and the ware as a multiple."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from kilndesigner import load_design
from kilndesigner.furniture import setting_weight
from kilndesigner.model import Kiln, Setting
from kilndesigner.units import Q_, si

EXAMPLES = Path(__file__).parents[2] / "examples"

SHELVES = {
    "length": "24 in",
    "width": "12 in",
    "thickness": "1 in",
    "material": "mullite",
    "per_layer": 4,
    "layers": 4,
}


def _kiln(setting: dict[str, object], ware: str | None = None) -> Kiln:
    doc = load_design(EXAMPLES / "pnw-hybrid-crossdraft.yaml").model_dump(mode="json")
    firing = {k: v for k, v in doc["firing"].items() if k not in ("ware", "setting")}
    doc["firing"] = {**firing, "setting": setting, **({"ware": ware} if ware else {})}
    return Kiln.model_validate(doc)


def test_olsens_shelf_weighs_what_he_says() -> None:
    furniture, ware, steps = setting_weight(Setting.model_validate({"shelves": SHELVES}))
    assert si(Q_(furniture, "kg"), "lb") == pytest.approx(16 * 20.5)
    assert ware == pytest.approx(7 * furniture)
    assert [s.name for s in steps] == ["Shelves", "Setting", "Ware", "Setting and ware"]
    assert steps[-1].value == f"{8 * 16 * 20.5:.0f} lb"


def test_posts_are_weighed_at_their_materials_density() -> None:
    posts = {
        "width": "2 in",
        "depth": "2 in",
        "height": "6 in",
        "material": "silicon-carbide",
        "per_layer": 3,
    }
    setting = Setting.model_validate({"shelves": SHELVES, "posts": posts, "ware_ratio": 6})
    furniture, ware, steps = setting_weight(setting)
    post = 2 * 2 * 6 * 22 / 288  # lb
    assert si(Q_(furniture, "kg"), "lb") == pytest.approx(16 * 20.5 + 12 * post)
    assert ware == pytest.approx(6 * furniture)
    assert "Posts" in [s.name for s in steps]


@pytest.mark.parametrize("ratio", [0, 2.5, 12])
def test_any_ratio_from_zero_up_is_taken(ratio: float) -> None:
    setting = Setting.model_validate({"shelves": SHELVES, "ware_ratio": ratio})
    furniture, ware, _ = setting_weight(setting)
    assert ware == pytest.approx(ratio * furniture)


def test_a_negative_ratio_is_refused() -> None:
    with pytest.raises(ValidationError, match="greater than or equal to 0"):
        Setting.model_validate({"shelves": SHELVES, "ware_ratio": -1})


def test_a_material_with_no_sourced_density_is_refused() -> None:
    with pytest.raises(ValidationError, match="no sourced density"):
        Setting.model_validate({"shelves": {**SHELVES, "material": "advancer"}})
    with pytest.raises(ValidationError, match="no sourced density"):
        Setting.model_validate(
            {
                "shelves": SHELVES,
                "posts": {
                    "width": "1 in",
                    "depth": "1 in",
                    "height": "1 in",
                    "material": "brick",
                    "per_layer": 1,
                },
            }
        )


def test_layers_that_dont_fit_the_chamber_are_refused() -> None:
    posts = {"width": "2 in", "depth": "2 in", "height": "10 in", "material": "mullite"}
    assert _kiln({"shelves": SHELVES, "posts": {**posts, "per_layer": 3}})
    with pytest.raises(ValidationError, match="more than the chamber's 44 in"):
        _kiln({"shelves": {**SHELVES, "layers": 5}, "posts": {**posts, "per_layer": 3}})
    with pytest.raises(ValidationError, match="more than the chamber's"):
        _kiln({"shelves": {**SHELVES, "layers": 45}})


def test_a_weight_or_a_setting_not_both() -> None:
    with pytest.raises(ValidationError, match="not both"):
        _kiln({"shelves": SHELVES}, ware="300 lb")


def test_the_simulation_heats_the_setting_and_ware() -> None:
    from kilndesigner.simulation import simulate

    kiln = _kiln({"shelves": SHELVES})
    names = [s.name for s in simulate(kiln).result.working]
    assert {"Shelves", "Setting", "Ware", "Setting and ware", "Ware and furniture"} <= set(names)
