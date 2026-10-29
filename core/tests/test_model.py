"""The design model's own rules: which layers a face takes, and what a design may not say."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from kilndesigner import parse_design
from kilndesigner.model import Burners, Draft, Firing, Heat, Kiln, Lining, Port, SpyHoles
from kilndesigner.units import si

EXAMPLES = Path(__file__).parents[2] / "examples"
CATENARY = (EXAMPLES / "catenary-gas-kiln.yaml").read_text(encoding="utf-8")
BURNER_PLACES = """places:
        - wall: front
          across: -9 in
          up: 6 in
        - wall: front
          across: 9 in
          up: 6 in"""
ONE_BURNER_RIGHT = BURNER_PLACES.replace(
    "wall: front\n          across: 9", "wall: right\n          across: 9"
)
SPY_HOLE_LEFT = "spy_holes:\n  count: 1\n  places:\n    - wall: left\n      up: 20 in\nsite:"
UP_DRAFT = "type: up"
CROSS_DRAFT = "type: cross\n  flue_wall: back"


def _layer(material: str, thickness: str) -> dict[str, str]:
    return {"material": material, "thickness": thickness}


def test_each_face_takes_its_own_layers_or_the_walls() -> None:
    walls = [_layer("ifb-jm26", "4.5 in"), _layer("kaowool-blanket-8pcf", "1 in")]
    floor = [_layer("ifb-jm26", "4.5 in"), _layer("ifb-k23", "2.5 in")]
    door = [_layer("ifb-jm26", "4.5 in")]
    lining = Lining.model_validate({"walls": walls, "floor": floor, "door": door})
    materials = {
        face: [layer.material for layer in lining.for_face(face, door_face="front")]
        for face in ("front", "left", "floor", "roof")
    }
    assert materials == {
        "front": ["ifb-jm26"],  # the door
        "left": ["ifb-jm26", "kaowool-blanket-8pcf"],
        "floor": ["ifb-jm26", "ifb-k23"],
        "roof": ["ifb-jm26", "kaowool-blanket-8pcf"],  # no roof layers given: the walls'
    }
    # Without door layers the door is built like the walls
    plain = Lining.model_validate({"walls": walls})
    assert plain.for_face("front", door_face="front") == plain.walls


def test_a_firing_may_be_a_temperature_alone() -> None:
    firing = Firing.model_validate({"top_temperature": "2300 degF"})
    assert firing.cone is None
    assert firing.top_temperature is not None
    assert si(firing.top_temperature, "degF") == pytest.approx(2300)


def test_a_temperature_lets_a_cone_stand_at_a_rate_it_is_not_published_at() -> None:
    """Cone 20 is published only at 150 °C/h (ASTM C24); with a temperature, the temperature wins
    and the cone stands as given."""
    with pytest.raises(ValidationError, match="only at 150 °C/h"):
        Firing.model_validate({"cone": "20"})
    firing = Firing.model_validate({"cone": "20", "top_temperature": "1564 degC"})
    assert firing.cone == "20"
    assert firing.final_rate == 60


def test_how_many_burners_a_design_asks_for() -> None:
    place = {"wall": "front", "up": "6 in"}
    assert Burners.model_validate({"count": 2}).wanted == 2
    assert Burners.model_validate({"places": [place, place, place]}).wanted == 3
    assert Burners().wanted is None
    with pytest.raises(ValidationError, match="a place for each of the 2 burners, not 1"):
        Burners.model_validate({"count": 2, "places": [place]})


def test_spy_holes_are_three_unless_the_design_says_otherwise() -> None:
    place = {"wall": "front", "up": "12 in"}
    assert SpyHoles().wanted == 3
    assert SpyHoles.model_validate({"count": 0}).wanted == 0
    assert SpyHoles.model_validate({"places": [place, place]}).wanted == 2
    with pytest.raises(ValidationError, match="a place for each of the 2 spy holes, not 1"):
        SpyHoles.model_validate({"count": 2, "places": [place]})


def test_a_port_is_round_or_rectangular_never_both() -> None:
    round_port = Port.model_validate({"diameter": "2 in"})
    assert round_port.round
    assert round_port.size_in() == pytest.approx((2.0, 2.0))
    quarter_brick = Port.model_validate({"width": "2.25 in", "height": "2.5 in"})
    assert not quarter_brick.round
    assert quarter_brick.size_in() == pytest.approx((2.25, 2.5))
    metric = Port.model_validate({"width": "50.8 mm", "height": "76.2 mm"})
    assert metric.size_in() == pytest.approx((2.0, 3.0))


@pytest.mark.parametrize(
    ("sizes", "message"),
    [
        ({"diameter": "2 in", "width": "2 in"}, "a diameter, or a width and a height, not both"),
        ({"diameter": "2 in", "height": "2 in"}, "a diameter, or a width and a height, not both"),
        ({"width": "2 in"}, "a diameter, or both a width and a height"),
        ({}, "a diameter, or both a width and a height"),
        ({"diameter": "0 in"}, "a port's sizes must be more than zero"),
        ({"width": "2 in", "height": "-1 in"}, "a port's sizes must be more than zero"),
    ],
)
def test_a_port_needs_one_shape_and_real_sizes(sizes: dict[str, str], message: str) -> None:
    with pytest.raises(ValidationError, match=message):
        Port.model_validate(sizes)


def test_a_domes_rise_must_keep_it_inside_the_walls() -> None:
    """A sail dome is a sphere through the chamber's top corners (combustion-and-masonry.md
    §6.7): rising as far as half the 30 × 36 in chamber's diagonal, √(30² + 36²)/2 = 23.4 in, it
    would bulge out past the walls."""
    text = (EXAMPLES / "dome-castable-kiln.yaml").read_text(encoding="utf-8")
    rise = (
        "rise: 9 in # at the centre: the least that carries the dome over the front door is 8.9 in"
    )
    assert rise in text
    assert parse_design(text).roof.type == "dome"
    refusal = r"less than half the chamber's diagonal, 23\.4 in"
    for bad in ("rise: 24 in", "rise: 0 in"):
        with pytest.raises(ValidationError, match=refusal):
            parse_design(text.replace(rise, bad))


def test_elements_arent_designed_for_a_catenary() -> None:
    electric = "heat:\n  electric:\n    supply:\n      voltage: 240 V\n      breaker: 60 A\n  gas:"
    assert "heat:\n  gas:" in CATENARY
    with pytest.raises(ValidationError, match="elements in a catenary kiln aren't designed here"):
        parse_design(CATENARY.replace("heat:\n  gas:", electric))


def test_a_kiln_needs_some_heat() -> None:
    with pytest.raises(ValidationError, match="give the kiln a heat source"):
        Heat.model_validate({})


def test_an_up_draft_flue_is_in_the_roof_so_it_has_no_flue_across() -> None:
    with pytest.raises(ValidationError, match="an up-draft's flue is in the roof"):
        Draft.model_validate({"type": "up", "flue_across": "3 in"})
    cross = Draft.model_validate({"type": "cross", "flue_across": "3 in"})
    assert cross.flue_across is not None
    assert si(cross.flue_across, "in") == pytest.approx(3)


def test_each_castable_needs_its_own_id() -> None:
    text = (EXAMPLES / "diy-castable-test-kiln.yaml").read_text(encoding="utf-8")
    with pytest.raises(ValidationError, match="each castable needs its own id"):
        parse_design(text.replace("id: diy-backup", "id: diy-hot-face"))


@pytest.mark.parametrize(
    ("change", "what", "wall"),
    [
        ((BURNER_PLACES, "wall: left"), "the burners", "left"),
        ((BURNER_PLACES, ONE_BURNER_RIGHT), "a burner", "right"),
        (("face: front", "face: left"), "the door or car", "left"),
        ((CROSS_DRAFT, "type: cross\n  flue_wall: right"), "the flue", "right"),
        (("site:", SPY_HOLE_LEFT), "a spy hole", "left"),
    ],
)
def test_a_catenary_is_its_own_side_walls(change: tuple[str, str], what: str, wall: str) -> None:
    """A catenary arch springs from the floor (combustion-and-masonry.md §6.6): nothing can go in
    its side walls, only the front and back walls that close its ends."""
    old, new = change
    assert old in CATENARY
    with pytest.raises(ValidationError, match=f"so {what} can't go in the {wall} wall"):
        parse_design(CATENARY.replace(old, new))


def _wood(**parts: object) -> dict[str, object]:
    """A wood-fired kiln as a document, with whole parts replaced."""
    hard = [_layer("hard-firebrick-kx99", "9 in")]
    document: dict[str, object] = {
        "name": "wood kiln",
        "firing": {"cone": "10"},
        "chamber": {"width": "48 in", "depth": "48 in", "height": "48 in"},
        "lining": {"walls": hard},
        "heat": {"fire": {"fireboxes": [{"width": "48 in", "length": "36 in"}]}},
    }
    return {**document, **parts}


GAS = {"gas": {"supply": {"type": "cylinders", "count": 4}}}
ELECTRIC = {"electric": {"supply": {"voltage": "240 V", "breaker": "60 A"}}}


@pytest.mark.parametrize(
    ("parts", "message"),
    [
        ({"chamber": {"shape": "round", "width": "84 in", "depth": "80 in", "height": "42 in"}},
         "a round chamber's width and depth are both its diameter"),
        ({"chamber": {"shape": "round", "width": "84 in", "depth": "84 in", "height": "42 in",
                      "chambers": 2}}, "a round kiln is one chamber"),
        ({"chamber": {"width": "48 in", "depth": "48 in", "height": "48 in", "slope": "20 %"}},
         "give the slope as an angle"),
        ({"chamber": {"width": "48 in", "depth": "48 in", "height": "48 in",
                      "slope": "65 degree"}}, "from 0 to under 60 degrees"),
        ({"chamber": {"shape": "round", "width": "84 in", "depth": "84 in", "height": "42 in"},
          "roof": {"type": "sprung_arch", "rise": "10 in"}}, "takes a dome or a flat roof"),
        ({"chamber": {"shape": "round", "width": "84 in", "depth": "84 in", "height": "42 in"},
          "heat": {**ELECTRIC, "fire": None}}, "elements in a round kiln's curved walls"),
        ({"chamber": {"shape": "round", "width": "84 in", "depth": "84 in", "height": "42 in"},
          "roof": {"type": "dome", "rise": "50 in"}}, "at most its radius, 42 in"),
        ({"roof": {"type": "open"}, "heat": GAS}, "an open top's heat loss isn't worked out"),
        ({"chamber": {"width": "48 in", "depth": "48 in", "height": "48 in", "on_ground": True},
          "heat": ELECTRIC}, "a floor on the ground has its loss left out"),
        ({"heat": {"fire": {"fuel": "wood", "oil_burners": 2,
                            "fireboxes": [{"width": "48 in", "length": "36 in"}]}}},
         "oil burners and their rate are for oil firing"),
        ({"heat": {"gas": {"fuel": "natural_gas", "supply": {"type": "cylinders", "count": 4}}}},
         "natural gas comes from a line"),
        ({"heat": {"gas": {"burners": {"wall": "floor",
                                       "places": [{"wall": "front", "up": "4 in"}]},
                           "supply": {"type": "cylinders", "count": 4}}}},
         "floor burners are spaced round the edge of the floor"),
        ({"heat": {"gas": {"burners": {"rating": "36000 BTU/hr"},
                           "supply": {"type": "cylinders", "count": 4}}}},
         "give the count of burners with their rating"),
        ({"heat": {"gas": {"burners": {"rating": "36000 BTU/hr", "count": 6, "model": "GACO MR750"},
                           "supply": {"type": "cylinders", "count": 4}}}},
         "a rating for one it doesn't list, not both"),
        ({"draft": {"type": "cross", "chimney": {"height": "10 ft",
                                                "inside": {"diameter": "9 in", "width": "9 in"}}}},
         "a diameter, or a width and a depth, not both"),
        ({"draft": {"type": "cross", "chimney": {"height": "10 ft", "inside": {"width": "9 in"}}}},
         "or both a width and a depth"),
        ({"draft": {"type": "cross", "chimney": {"height": "10 ft",
                                                "inside": {"diameter": "0 in"}}}},
         "a section's sizes must be more than zero"),
    ],
)  # fmt: skip
def test_what_a_wood_round_or_sloped_kiln_refuses(parts: dict[str, object], message: str) -> None:
    """Olsen's kinds of kiln (round, climbing, open-topped, on the ground, fired with oil or
    natural gas) each refuse what the engine can't work out for them, and say why."""
    document = _wood(**parts)
    heat = document["heat"]
    if isinstance(heat, dict) and heat.get("fire", "") is None:
        document["heat"] = {k: v for k, v in heat.items() if v is not None}
    with pytest.raises(ValidationError, match=message):
        Kiln.model_validate(document)


def test_chambers_in_a_row_are_one_long_chamber() -> None:
    kiln = Kiln.model_validate(
        _wood(chamber={"width": "48 in", "depth": "40 in", "height": "48 in", "chambers": 3,
                       "slope": "18.4 degree"})
    )  # fmt: skip
    assert si(kiln.chamber.length, "in") == pytest.approx(120)
    assert si(kiln.chamber.slope, "degree") == pytest.approx(18.4)  # type: ignore[arg-type]


def test_a_catenary_with_an_up_draft_has_no_flue_wall_to_check() -> None:
    kiln = parse_design(CATENARY.replace(CROSS_DRAFT, UP_DRAFT))
    assert kiln.draft is not None
    assert kiln.draft.type == "up"
    # An up-draft's flue is in the roof, so its flue_wall (a cross-draft setting) isn't checked
    side = parse_design(CATENARY.replace(CROSS_DRAFT, f"{UP_DRAFT}\n  flue_wall: left"))
    assert side.draft is not None
    assert side.draft.flue_wall == "left"
