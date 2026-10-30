from pathlib import Path

import pytest
from pydantic import ValidationError

from kilndesigner import dump_design, load_design, parse_design
from kilndesigner.model import SprungArch
from kilndesigner.units import si

EXAMPLES = Path(__file__).parents[2] / "examples"


@pytest.mark.parametrize("path", sorted(EXAMPLES.glob("*.yaml")), ids=lambda p: p.stem)
def test_examples_are_valid_and_round_trip(path: Path) -> None:
    kiln = load_design(path)
    assert parse_design(dump_design(kiln)) == kiln


def test_reads_the_front_loader() -> None:
    kiln = load_design(EXAMPLES / "electric-front-loader.yaml")
    assert si(kiln.chamber.width, "in") == 22.5
    assert kiln.door_face == "front"
    assert kiln.heat.electric is not None
    assert si(kiln.heat.electric.supply.breaker, "A") == 60
    assert si(kiln.site.ambient, "degF") == pytest.approx(70)


MINIMAL = """
name: Test kiln
firing: {cone: "6"}
chamber: {width: 18 in, depth: 18 in, height: 18 in}
lining:
  walls: [{material: ifb-k23, thickness: 4.5 in}]
heat:
  electric:
    supply: {voltage: 240 V, breaker: 30 A}
"""


def test_defaults_fill_in() -> None:
    kiln = parse_design(MINIMAL)
    assert kiln.schema_version == 1
    assert kiln.roof.type == "flat"
    assert kiln.lining.for_face("floor") == kiln.lining.walls
    assert si(kiln.site.ambient, "degF") == pytest.approx(70)


def test_a_bare_number_is_rejected_with_an_example() -> None:
    with pytest.raises(ValidationError, match="has no unit"):
        parse_design(MINIMAL.replace("width: 18 in", "width: 18"))


def test_a_wrong_unit_is_rejected() -> None:
    with pytest.raises(ValidationError, match="not a length"):
        parse_design(MINIMAL.replace("width: 18 in", "width: 18 kg"))


def test_unknown_fields_are_rejected() -> None:
    with pytest.raises(ValidationError, match="Extra inputs"):
        parse_design(MINIMAL + "colour: red\n")


def test_firing_needs_a_target() -> None:
    with pytest.raises(ValidationError, match="cone or a top_temperature"):
        parse_design(MINIMAL.replace('firing: {cone: "6"}', "firing: {}"))


def test_a_cone_must_be_in_the_table_even_beside_a_temperature() -> None:
    with pytest.raises(ValidationError, match="not in the Orton table"):
        parse_design(
            MINIMAL.replace('firing: {cone: "6"}', 'firing: {cone: "99", top_temperature: 2300 °F}')
        )


def test_roof_is_chosen_by_type() -> None:
    kiln = parse_design(MINIMAL + "roof: {type: sprung_arch, rise: 4 in}\n")
    assert isinstance(kiln.roof, SprungArch)
