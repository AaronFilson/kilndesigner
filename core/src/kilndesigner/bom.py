"""The bill of materials: what to buy, in the units it's sold in, and roughly what it costs."""

from __future__ import annotations

import math
from functools import cache
from importlib import resources
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict

from kilndesigner.allowance import allowance
from kilndesigner.castable import CastableReport
from kilndesigner.electric import ElectricDesign
from kilndesigner.frame import FrameDesign
from kilndesigner.gas import GasDesign
from kilndesigner.hardware import CHIMNEY_BRICK
from kilndesigner.masonry import Masonry
from kilndesigner.materials_checks import within_budget
from kilndesigner.model import Kiln
from kilndesigner.units import Q_, parse_quantity, si
from kilndesigner.working import Finding


class PriceItem(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    material: str
    description: str
    unit: str
    per: float  # how many units one purchase covers
    price: str
    seller: str
    source: str
    comparable: bool = False


class PriceList(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    checked: str
    items: list[PriceItem]

    def for_material(self, material_id: str) -> PriceItem | None:
        return next((i for i in self.items if i.material == material_id), None)


@cache
def price_list() -> PriceList:
    text = resources.files("kilndesigner.data").joinpath("prices.yaml").read_text(encoding="utf-8")
    data: Any = yaml.safe_load(text)
    return PriceList.model_validate(data)


class BomLine(BaseModel):
    model_config = ConfigDict(frozen=True)

    item: str
    needed: str
    buy: str
    unit_price: str | None
    cost: float | None
    priced_as: str | None
    source: str | None


class Bom(BaseModel):
    model_config = ConfigDict(frozen=True)

    lines: list[BomLine]
    total: float
    prices_checked: str
    findings: list[Finding]


def _purchase_word(unit: str, count: int) -> str:
    words = {"bricks": "brick", "ft²·in": "roll", "lb": "bag"}
    word = words.get(unit, "unit")
    return f"{count} {word}{'' if count == 1 else 's'}"


def bill_of_materials(
    kiln: Kiln,
    masonry: Masonry,
    electric: ElectricDesign | None,
    gas: GasDesign | None = None,
    frame: FrameDesign | None = None,
    chimney_bricks: int = 0,
    castables: list[CastableReport] | None = None,
) -> Bom:
    prices = price_list()
    lines: list[BomLine] = []
    findings: list[Finding] = []
    total = 0.0
    unpriced: list[str] = []

    for q in masonry.quantities:
        item = prices.for_material(q.material)
        needed = f"{q.amount:g} {q.unit} ({q.detail})"
        if item is None:
            lines.append(
                BomLine(
                    item=q.name, needed=needed, buy="—", unit_price=None, cost=None,
                    priced_as=None, source=None,
                )
            )  # fmt: skip
            unpriced.append(q.name)
            continue
        units = math.ceil(q.priced_amount / item.per - 1e-9)
        unit_price = si(parse_quantity(item.price), "USD")
        cost = units * unit_price
        total += cost
        lines.append(
            BomLine(
                item=q.name,
                needed=needed,
                buy=_purchase_word(item.unit, units)
                if item.unit != "bricks"
                else f"{units} bricks",
                unit_price=f"${unit_price:,.2f}",
                cost=cost,
                priced_as=f"{item.description}, {item.seller}"
                + (" (a comparable product)" if item.comparable else ""),
                source=item.source,
            )
        )

    if electric is not None and electric.elements is not None:
        el = electric.elements
        mass_lb = si(parse_quantity(el.wire_mass_total), "lb")
        alloy_id = kiln.heat.electric.alloy if kiln.heat.electric else ""
        item = prices.for_material(alloy_id)
        buy_lb = math.ceil(mass_lb * 1.1 * 2) / 2  # 10% extra, to the next half pound
        needed = f"{el.count} elements of {el.gauge}, {el.length_each} each ({el.wire_mass_total})"
        if item is None:
            lines.append(
                BomLine(
                    item=f"{electric.alloy} wire", needed=needed, buy=f"{buy_lb:g} lb",
                    unit_price=None, cost=None, priced_as=None, source=None,
                )
            )  # fmt: skip
            unpriced.append(f"{electric.alloy} wire")
        else:
            unit_price = si(parse_quantity(item.price), "USD")
            total += buy_lb * unit_price
            lines.append(
                BomLine(
                    item=f"{electric.alloy} wire",
                    needed=needed,
                    buy=f"{buy_lb:g} lb",
                    unit_price=f"${unit_price:,.2f}/lb",
                    cost=buy_lb * unit_price,
                    priced_as=f"{item.description}, {item.seller}",
                    source=item.source,
                )
            )

    if gas is not None and gas.burners is not None:
        b = gas.burners
        lines.append(
            BomLine(
                item=f"{b.model} burner",
                needed=f"{b.count} burners at {b.pressure}, {b.each} each",
                buy=f"{b.count} burners",
                unit_price=f"${b.total_cost / b.count:,.2f}",
                cost=b.total_cost,
                priced_as=f"{b.model}, Ward Burner Systems",
                source="combustion-and-masonry.md §3.2, §3.3 [S22, S27]",
            )
        )
        total += b.total_cost
    for c in castables or []:
        for t in c.totals:
            if not t.amount_lb:
                continue
            lines.append(
                BomLine(
                    item=f"{t.name}, for {c.mix.name}",
                    needed=f"{t.amount} for {c.batches} batches",
                    buy=f"{math.ceil(t.amount_lb):g} lb",
                    unit_price=None if t.cost is None else f"${t.cost / t.amount_lb:,.2f}/lb",
                    cost=t.cost,
                    priced_as=None if t.cost is None else "your price, in the design",
                    source=None if t.cost is None else "the design file",
                )
            )
            if t.cost is None:
                unpriced.append(t.name)
            else:
                total += t.cost
    if chimney_bricks:
        item = prices.for_material(CHIMNEY_BRICK)
        unit_price = None if item is None else si(parse_quantity(item.price), "USD")
        cost = None if unit_price is None else chimney_bricks * unit_price
        lines.append(
            BomLine(
                item="Chimney and flue duct: hard firebrick",
                needed=(
                    f"{chimney_bricks} straights "
                    f"(with {allowance(kiln, 'brick').text} for cuts and breakage)"
                ),
                buy=f"{chimney_bricks} bricks",
                unit_price=None if unit_price is None else f"${unit_price:,.2f}",
                cost=cost,
                priced_as=None if item is None else f"{item.description}, {item.seller}",
                source=None if item is None else item.source,
            )
        )
        total += cost or 0.0
        if cost is None:
            unpriced.append("chimney brick")
    if frame is not None:
        by_steel: dict[str, float] = {}
        for m in frame.members:
            by_steel[m.steel] = by_steel.get(m.steel, 0.0) + m.total_ft
        for steel, feet in by_steel.items():
            parts = ", ".join(m.part for m in frame.members if m.steel == steel)
            lines.append(
                BomLine(
                    item=steel, needed=f"{feet:.1f} ft ({parts})",
                    buy=f"{math.ceil(feet * 1.1):g} ft", unit_price=None, cost=None,
                    priced_as=None, source=frame.members[0].source,
                )
            )  # fmt: skip
        unpriced.append("steel")
    if kiln.loading.type == "car":
        cost = kiln.loading.car_hardware_cost
        lines.append(
            BomLine(
                item="Kiln car: wheels, rails, frame and sand seal",
                needed="as designed by the builder",
                buy="1 car",
                unit_price=None if cost is None else f"${si(cost, 'USD'):,.2f}",
                cost=None if cost is None else si(cost, "USD"),
                priced_as=None if cost is None else "the design's own estimate",
                source=None if cost is None else "the design file",
            )
        )
        if cost is None:
            unpriced.append("the kiln car's hardware (set loading.car_hardware_cost)")
        else:
            total += si(cost, "USD")

    findings.append(
        Finding(
            level="info",
            message=(
                f"Prices were checked on {prices.checked} and will change. Steel is listed by "
                "length, with 10 % extra, but not priced. Hardware, electrical parts (relays, "
                "controller, wiring), gas fittings and shipping are not included."
            ),
        )
    )
    if unpriced:
        findings.append(
            Finding(
                level="info",
                message="No price found for: " + ", ".join(dict.fromkeys(unpriced)) + ".",
            )
        )
    budget = kiln.site.materials_budget
    if budget is not None:
        priced = [(x.item, x.cost, x.priced_as) for x in lines if x.cost is not None]
        sheet = within_budget(priced, si(budget, "USD"))
        sheet.agrees("C", Q_(total, "USD"))
        if (check := sheet.check()).status != "pass":
            findings.append(
                Finding.failed(
                    check,
                    message=(
                        f"The priced materials come to ${total:,.0f}, over the "
                        f"${si(budget, 'USD'):,.0f} budget, before steel, hardware and shipping."
                    ),
                )
            )
    return Bom(lines=lines, total=total, prices_checked=prices.checked, findings=findings)
