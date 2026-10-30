"""What to buy over the count in the kiln, for breakage, spills and mistakes.

Each case has its own default from docs/research/brick-waste.md, and the design can give its own
(``Kiln.allowances``). A cut brick's cutting loss is already in its count: the cut list takes a
whole brick for each piece that can't come from another's offcut, so the allowance covers breakage.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

from kilndesigner.model import Kiln
from kilndesigner.units import si
from kilndesigner.working import Step

type Case = Literal["brick", "shaped", "castable", "sheet"]

BIA = "brick-waste.md §1, BIA Technical Note 10 (2009), p.11 [W1]"
PCO = "brick-waste.md §3, PCO Refractories, castable application instructions 1/2026, §5.3 [W2]"
NONE_FOUND = "brick-waste.md §4: no source gives one"


@dataclass(frozen=True)
class Default:
    share: float
    what: str
    reference: str


DEFAULTS: dict[Case, Default] = {
    "brick": Default(0.05, "bricks, whole and cut", BIA),
    "shaped": Default(0.05, "arch and wedge bricks", f"{BIA}; brick-waste.md §2"),
    "castable": Default(0.05, "castable", PCO),
    "sheet": Default(0.0, "blanket and board", NONE_FOUND),
}


@dataclass(frozen=True)
class Allowance:
    case: Case
    share: float
    reference: str
    from_design: bool

    def buy(self, count: float) -> int:
        """Whole units to buy: the count plus the allowance, rounded up."""
        return math.ceil(count * (1 + self.share) - 1e-9)

    @property
    def text(self) -> str:
        return f"{self.share * 100:.3g} %"

    def step(self) -> Step:
        return Step(
            name=f"Allowance over the count: {DEFAULTS[self.case].what}",
            formula=(
                "buy = ⌈count × (1 + allowance)⌉"
                if self.case in ("brick", "shaped")
                else "buy = amount × (1 + allowance)"
            ),
            inputs={"allowance": self.text},
            value=self.text,
            reference="the design file" if self.from_design else self.reference,
            note=None
            if self.from_design
            else f"the default; set allowances.{self.case} in the design to change it",
        )


def allowance(kiln: Kiln, case: Case) -> Allowance:
    given = getattr(kiln.allowances, case)
    if given is not None:
        return Allowance(case, si(given, ""), "the design file", from_design=True)
    d = DEFAULTS[case]
    return Allowance(case, d.share, d.reference, from_design=False)
