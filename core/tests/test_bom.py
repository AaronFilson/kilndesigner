"""The bill of materials, priced from prices.yaml (combustion-and-masonry.md §9)."""

import math
from pathlib import Path

import pytest

from kilndesigner import bom as bom_module
from kilndesigner import load_design, parse_design
from kilndesigner.bom import PriceList, bill_of_materials, price_list
from kilndesigner.castable import analyse_mix, castable_reports
from kilndesigner.electric import design_elements
from kilndesigner.heatloss import heat_loss
from kilndesigner.masonry import Masonry, Quantity
from kilndesigner.model import Kiln
from kilndesigner.units import parse_quantity, si

EXAMPLES = Path(__file__).parents[2] / "examples"
FRONT_LOADER = load_design(EXAMPLES / "electric-front-loader.yaml")
NO_MASONRY = Masonry(quantities=[], cut_list=[], findings=[])


def _quantity(material: str, name: str, unit: str, amount: float) -> Quantity:
    return Quantity(
        material=material, name=name, kind="test", amount=amount, unit=unit, detail="walls",
        priced_amount=amount,
    )  # fmt: skip


def test_masonry_is_bought_in_the_units_it_is_sold_in() -> None:
    """K-23 by the brick at $6.24; blanket by the 50 ft²·in roll at $150; Mizzou by the 55 lb bag
    at $83.05 (prices.yaml, checked 2026-10-21). JM 28 has no price."""
    masonry = Masonry(
        quantities=[
            _quantity("ifb-k23", "K-23 brick", "bricks", 100),
            _quantity("kaowool-blanket-8pcf", "Blanket, 8 pcf", "ft²·in", 121),
            _quantity("mizzou-castable-plus", "Mizzou Castable Plus", "lb", 110),
            _quantity("ifb-jm28", "JM 28 brick", "bricks", 40),
        ],
        cut_list=[],
        findings=[],
    )
    bom = bill_of_materials(FRONT_LOADER, masonry, None)
    lines = {line.item: line for line in bom.lines}
    assert (lines["K-23 brick"].buy, lines["K-23 brick"].unit_price) == ("100 bricks", "$6.24")
    assert lines["K-23 brick"].cost == pytest.approx(624.00)
    assert lines["K-23 brick"].needed == "100 bricks (walls)"
    assert (lines["Blanket, 8 pcf"].buy, lines["Blanket, 8 pcf"].cost) == ("3 rolls", 450.0)
    assert lines["Blanket, 8 pcf"].priced_as is not None
    assert lines["Blanket, 8 pcf"].priced_as.endswith("(a comparable product)")
    assert lines["Mizzou Castable Plus"].buy == "2 bags"
    assert lines["Mizzou Castable Plus"].cost == pytest.approx(2 * 83.05)
    unpriced = lines["JM 28 brick"]
    assert (unpriced.buy, unpriced.unit_price, unpriced.cost, unpriced.source) == (
        "—",
        None,
        None,
        None,
    )
    assert bom.total == pytest.approx(624.00 + 450.00 + 166.10)
    assert bom.prices_checked == "2026-10-21"
    assert "No price found for: JM 28 brick." in [f.message for f in bom.findings]


def test_wire_is_bought_to_the_next_half_pound_with_a_tenth_spare() -> None:
    """Kanthal A-1 at $55.65/lb, derived from TEMCo's 16 AWG price (prices.yaml [S77])."""
    electric = design_elements(FRONT_LOADER)
    assert electric.elements is not None
    bom = bill_of_materials(FRONT_LOADER, NO_MASONRY, electric)
    [wire] = bom.lines
    mass_lb = si(parse_quantity(electric.elements.wire_mass_total), "lb")
    buy_lb = math.ceil(mass_lb * 1.1 * 2) / 2
    assert wire.item == "Kanthal A-1 wire"
    assert wire.buy == f"{buy_lb:g} lb"
    assert wire.unit_price == "$55.65/lb"
    assert wire.cost == pytest.approx(buy_lb * 55.65)
    assert bom.total == pytest.approx(buy_lb * 55.65)


def test_a_car_kiln_is_priced_from_the_designs_own_estimate() -> None:
    """No sourced prices exist for car hardware, so it is priced only when the design gives one."""
    text = (EXAMPLES / "pnw-hybrid-crossdraft-car.yaml").read_text(encoding="utf-8")
    without = bill_of_materials(parse_design(text), NO_MASONRY, None)
    [car] = without.lines
    assert (car.item, car.cost, car.unit_price) == (
        "Kiln car: wheels, rails, frame and sand seal",
        None,
        None,
    )
    assert without.total == 0.0
    assert any("set loading.car_hardware_cost" in f.message for f in without.findings)

    car_end = "face: front # an end wall: the arch springs from the sides"
    assert car_end in text
    priced = parse_design(text.replace(car_end, "face: front\n  car_hardware_cost: 1500 USD"))
    bom = bill_of_materials(priced, NO_MASONRY, None)
    [car] = bom.lines
    assert (car.unit_price, car.cost, car.priced_as) == (
        "$1,500.00",
        1500.0,
        "the design's own estimate",
    )
    assert bom.total == pytest.approx(1500.0)
    assert not [f for f in bom.findings if "No price found" in f.message]


def test_castables_are_bought_by_the_pound_only_for_mixes_the_lining_uses() -> None:
    """The design prices Mulcoa 70 at $1.00/lb (as the DIY example does, from Clay Art Center);
    Secar 71 has no price. A mix listed but not in the lining buys nothing."""
    used: dict[str, object] = {
        "id": "foamed-mulcoa",
        "name": "Foamed Mulcoa and Secar 71",
        "ingredients": [
            {"ingredient": "mulcoa-70", "mass": "40 lb", "price": "1.00 USD/lb"},
            {"ingredient": "secar-71", "mass": "5 lb"},
        ],
        "water": "5 lb",
        "foam": 50,
    }
    unused: dict[str, object] = {
        "id": "starch-mix",
        "name": "Molochite and corn starch",
        "ingredients": [
            {"ingredient": "molochite", "mass": "20 lb"},
            {"ingredient": "cornstarch", "mass": "10 lb"},
        ],
        "water": "10 lb",
    }
    data = FRONT_LOADER.model_dump(mode="json", by_alias=True)
    data["castables"] = [used, unused]
    data["lining"]["walls"] = [
        {"material": "ifb-jm26", "thickness": "4.5 in"},
        {"material": "foamed-mulcoa", "thickness": "2 in"},
    ]
    kiln = Kiln.model_validate(data)
    mix = kiln.castable("foamed-mulcoa")
    assert mix is not None
    placed = 2 * analyse_mix(kiln, mix).cast_volume_m3  # 2 batches, 3 with 10 % for waste
    reports = castable_reports(kiln, heat_loss(kiln), None, {"foamed-mulcoa": placed})
    bom = bill_of_materials(kiln, NO_MASONRY, None, castables=reports)
    assert [(line.item, line.buy, line.cost) for line in bom.lines] == [
        ('Mulcoa 70 calcined mullite grog (Clay Art Center\'s "CE70"), for Foamed Mulcoa and '
         "Secar 71", "120 lb", 120.0),
        ("Secar 71 calcium aluminate cement (about 70 % alumina), for Foamed Mulcoa and Secar 71",
         "15 lb", None),
    ]  # fmt: skip
    assert bom.lines[0].unit_price == "$1.00/lb"
    assert bom.lines[0].priced_as == "your price, in the design"
    assert bom.total == pytest.approx(120.0)
    assert "No price found for: Secar 71 calcium aluminate cement (about 70 % alumina)." in [
        f.message for f in bom.findings
    ]


def test_chimney_brick_is_hard_firebrick_at_its_listed_price() -> None:
    """Super-duty hard firebrick, $5.45 a brick (prices.yaml [S70])."""
    bom = bill_of_materials(FRONT_LOADER, NO_MASONRY, None, chimney_bricks=120)
    [chimney] = bom.lines
    assert chimney.item == "Chimney and flue duct: hard firebrick"
    assert (chimney.buy, chimney.unit_price) == ("120 bricks", "$5.45")
    assert chimney.cost == pytest.approx(120 * 5.45)


def test_chimney_brick_missing_from_the_price_list_is_listed_unpriced(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Prices change and items drop out of the list: then the bricks are still listed, unpriced."""
    full = price_list()
    without = PriceList(
        checked=full.checked,
        items=[i for i in full.items if i.material != "hard-firebrick-kx99"],
    )
    monkeypatch.setattr(bom_module, "price_list", lambda: without)
    bom = bill_of_materials(FRONT_LOADER, NO_MASONRY, None, chimney_bricks=120)
    [chimney] = bom.lines
    assert (chimney.buy, chimney.unit_price, chimney.cost, chimney.source) == (
        "120 bricks",
        None,
        None,
        None,
    )
    assert bom.total == 0.0
    assert "No price found for: chimney brick." in [f.message for f in bom.findings]


def test_going_over_the_budget_is_a_warning() -> None:
    """A $500 budget against 100 K-23 bricks at $6.24."""
    data = FRONT_LOADER.model_dump(mode="json", by_alias=True)
    data["site"]["materials_budget"] = "500 USD"
    kiln = Kiln.model_validate(data)
    masonry = Masonry(
        quantities=[_quantity("ifb-k23", "K-23 brick", "bricks", 100)], cut_list=[], findings=[]
    )
    [warning] = [f for f in bill_of_materials(kiln, masonry, None).findings if f.level == "warning"]
    assert warning.message == (
        "The priced materials come to $624, over the $500 budget, before steel, hardware and "
        "shipping."
    )
    # Its sheet: each priced line, their sum, the budget, and the budget that would do
    check = warning.check
    assert check is not None
    assert check.id == "bom.budget"
    assert [c.symbol for c in check.cells] == ["c_1", "B", "C"]
    assert check.requirements[0].margin == "C = $624, 124.8 % of B = $500"
    assert check.solve == "Passes when B ≥ $624"
