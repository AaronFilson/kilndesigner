"""Wood, coal and oil firing's checks as sheets (ADR 0013): the chimney against Olsen's rules for
natural draft, and the fireboxes against the chimney and the floor.

These are Olsen's rules of thumb, from *The Kiln Book*, 4th ed. His own kilns stray from them (the
fast-fire kiln's chimney is under Rule 5; his groundhogs run 4 : 1 against his 7 : 1 grate), so
each requirement is set at the edge of what he states and builds, and only a design beyond that
raises a warning. :mod:`kilndesigner.fire` computes the same numbers its own way; each sheet must
agree with them (``Sheet.agrees``).
"""

from __future__ import annotations

from dataclasses import dataclass

from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_

DESIGN = "the design"
RULE_5 = (
    "Olsen, The Kiln Book, 4th ed., p.80 (Principle 5): 3 ft of chimney per ft of downward pull "
    "plus 1 ft per 3 ft of horizontal pull, inside the kiln; p.130 (Fig. 5-2): the early Far-East "
    "proportions, a chimney twice the chamber's height (4 m on a 2 m cube), are the least and "
    "Rule 5 the most"
)
CLIMBING = (
    "Olsen, The Kiln Book, 4th ed., p.81 (Principle 8): a climbing kiln's chimney reaches at least "
    "the line through its chamber tops; p.101: the Bizen chimney is about 3 × the kiln's total rise"
)
FORCED = "Olsen, 4th ed. p.79, p.130–131: forced draft, about a quarter shorter"
AUXILIARY_AIR = (
    "Olsen, The Kiln Book, 4th ed., p.79: a chimney for gas under pressure can be at least 25 % "
    "shorter, but 'If a combination of wood is also to be used, then you must provide an "
    "auxillary [sic] air source'"
)
ALTITUDE = "Olsen, 4th ed. p.81–82, p.140: above about 4000 ft, at least 30 % taller"
GRATE = (
    "Olsen, The Kiln Book, 4th ed., p.76: wood grate 10 × the chimney's section at its base; p.77: "
    "he now uses about 7 : 1, and groundhogs run about 4 : 1"
)
COAL = "Olsen, The Kiln Book, 4th ed., p.76, p.206: coal, 1 ft² of grate per 6–8 ft² of floor"
OIL = "Olsen, The Kiln Book, 4th ed., p.213: oil, 1 ft² of combustion area per 5 ft² of floor"


@dataclass(frozen=True)
class Pull:
    """What a natural-draft chimney's height comes from: the pull inside the kiln (in)."""

    down: float  # downward pull: the gases' drop from the top of the chamber to the exit flue
    across: float  # horizontal pull: the chamber, the flue wall, the run and the chimney's width
    rise: float  # a climbing kiln's rise from its firing end to its chimney; 0 if level
    forced: bool
    high: bool  # above about 4000 ft


def chimney_height(pull: Pull, height: float, given: bool, with_gas: bool = False) -> Sheet:
    """The chimney against the least Olsen's rules allow: the p.130 proportions (twice the
    downward pull), or a climbing kiln's chamber-top line; less with forced draft, more at
    altitude. A wood fire in a kiln that burns gas too, with no blower, is its own check: a
    chimney cut down for the gas needs an auxiliary air source for the wood (p.79)."""
    climbing = pull.rise > 0
    reference = CLIMBING if climbing else RULE_5
    if with_gas and not pull.forced:
        s = Sheet(
            "fire.auxiliary-air",
            "The chimney's height, for wood drawn by it alone",
            reference=f"{reference}; {AUXILIARY_AIR}",
        )
    else:
        s = Sheet("fire.chimney", "The chimney's height", reference=reference)
    if climbing:
        s.given(
            "h_d",
            "the chamber's inside height at the chimney end",
            Q_(pull.down, "in"),
            source=f"{DESIGN}: the chamber",
        )
        s.given(
            "R",
            "the kiln's rise from its firing end to the chimney",
            Q_(pull.rise, "in"),
            source=f"{DESIGN}: the chambers' run and the floor's slope",
        )
        s.let("H_0", "the line through the chamber tops, at the chimney", "R + h_d", "ft")
    else:
        s.given(
            "P_d",
            "downward pull: from the top inside down to the exit flue",
            Q_(pull.down, "in"),
            source=f"{DESIGN}: the chamber, the roof and any firebox under the floor",
        )
        s.given("k", "chimney per unit of downward pull, the least", 2.0, source=RULE_5)
        s.let("H_0", "the p.130 proportions", "k*P_d", "ft")
    s.given("f_f", "forced draft", 0.75 if pull.forced else 1.0, source=FORCED)
    s.given("f_a", "at altitude", 1.3 if pull.high else 1.0, source=ALTITUDE)
    s.let("H_min", "the least chimney", "H_0*f_f*f_a", "ft")
    s.given(
        "H",
        "the chimney's top above the chamber floor",
        Q_(height, "in"),
        "ft",
        source=f"{DESIGN}: draft.chimney.height" if given else "the engine",
    )
    s.require("H", ">=", "H_min", level="warning")
    s.lever("H", Q_(1, "ft"), Q_(120, "ft"))
    return s


def grate_ratio(
    grate_in2: float, chimney_in2: float, what: str, ratios: tuple[float, float]
) -> Sheet:
    """A wood kiln's grate (or firebox floor) against its chimney's section at the base."""
    lo, hi = ratios
    s = Sheet("fire.grate", "The grate against the chimney", reference=GRATE)
    s.given("A_g", what, Q_(grate_in2, "in**2"), source=f"{DESIGN}: the fireboxes")
    s.given(
        "A_c",
        "the chimney's section at its base",
        Q_(chimney_in2, "in**2"),
        source=f"{DESIGN}: draft.chimney.inside",
    )
    s.let("r", "grate ÷ chimney", "A_g/A_c")
    s.given("r_min", "the least: Olsen's groundhogs", lo, source=GRATE)
    s.given("r_max", "the most: Olsen's first rule", hi, source=GRATE)
    s.require("r", ">=", "r_min", level="warning")
    s.require("r", "<=", "r_max", level="warning")
    s.lever("A_c", Q_(10, "in**2"), Q_(2000, "in**2"))
    return s


def floor_ratio(
    area_in2: float, floor_in2: float, what: str, per_floor: float, source: str, id: str
) -> Sheet:
    """Coal's grate or oil's combustion area against the chamber's floor."""
    s = Sheet(id, f"The {what} against the floor", reference=source)
    s.given("A_g", f"the {what}", Q_(area_in2, "in**2"), "ft**2", source=f"{DESIGN}: the fireboxes")
    s.given(
        "A_f",
        "the chamber's floor",
        Q_(floor_in2, "in**2"),
        "ft**2",
        source=f"{DESIGN}: the chamber",
    )
    s.given("n", f"floor per unit of {what}, the most", per_floor, source=source)
    s.let("A_min", f"the least {what}", "A_f/n", "ft**2")
    s.require("A_g", ">=", "A_min", level="warning")
    s.lever("A_g", Q_(10, "in**2"), Q_(floor_in2, "in**2"))
    return s


__all__ = ["Pull", "chimney_height", "floor_ratio", "grate_ratio"]
