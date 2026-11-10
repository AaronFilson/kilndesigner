"""The wall between two chambers in a row: how thick it is built, and of what.

Olsen, The Kiln Book, 4th ed., p.46: "A common wall between two chambers carries two arches'
thrust: build it 4½ in thicker than the others, never narrower than its two skewbacks"
(`docs/research/kiln-reference.md` §1, Read). So, unless the design gives the wall's own layers
(``lining.between``, where a book prints its thickness):

- chambers whose arches spring from the walls between them (sprung arches along the draft) or whose
  domes stand on them: the walls' layers, the hot face 4½ in thicker, and then, for arches, as much
  thicker again as the two arches' feet on one wall need (each foot the roof's thickness times the
  sine of its arch's half-angle, up to a semicircle's whole thickness), in whole bricks;
- a tube's vault, a flat roof, a catenary or an open top throws nothing on them: the walls' layers.
"""

from __future__ import annotations

import itertools
import math

from kilndesigner.model import Dome, Kiln, SprungArch
from kilndesigner.shape import Arch
from kilndesigner.units import Q_, si

COMMON_WALL_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.46: a common wall between two chambers carries two arches' "
    "thrust: build it 4½ in thicker than the others, never narrower than its two skewbacks"
)
THICKER = Q_(4.5, "inch")


def carries_arches(kiln: Kiln) -> bool:
    """Whether the chambers' arches or domes spring from the walls between them."""
    roof = kiln.roof
    return (isinstance(roof, SprungArch) and not roof.tube) or isinstance(roof, Dome)


def between_layers(kiln: Kiln, unit: str = "mm") -> list[tuple[str, float]]:
    """The layers of each wall between chambers, front to back: (material, thickness in
    ``unit``). Thickened by the rule, a hot face laid in whole bricks stays whole bricks: its
    thickness rounded up to the next that 9, 4½ and 2½ in bricks make (masonry.py)."""
    lining = kiln.lining
    if lining.between is not None:
        return [(x.material, si(x.thickness, unit)) for x in lining.between]
    walls = [(x.material, si(x.thickness, unit)) for x in lining.walls]
    if kiln.chamber.chambers < 2 or not carries_arches(kiln):
        return walls
    from kilndesigner.masonry import brick_sizes, buildable_near

    mm = [si(x.thickness, "mm") for x in lining.walls]
    total = sum(mm)
    wanted = max(total + si(THICKER, "mm"), feet(kiln, "mm"))
    first = mm[0] + wanted - total
    if brick_sizes(mm[0]) is not None and brick_sizes(first) is None:
        first = buildable_near(first)[1]
    mat = walls[0][0]
    return [(mat, si(Q_(first, "mm"), unit)), *walls[1:]]


def feet(kiln: Kiln, unit: str = "mm") -> float:
    """The most the feet of two neighbouring chambers' arches along the draft take of the wall
    between them (``unit``): each the roof's whole thickness times sin of its half-angle (a
    skewback's bed; a semicircle's foot is the ring's thickness). 0 for a dome."""
    roof = kiln.roof
    if not isinstance(roof, SprungArch):
        return 0.0
    thick = sum(si(x.thickness, unit) for x in kiln.lining.for_face("roof"))
    c = kiln.chamber
    rise = si(roof.rise, unit)
    if c.sizes is None:
        spans = [(si(c.depth, unit), rise)] * c.chambers
    else:
        spans = [(si(s.depth, unit), si(s.rise, unit) if s.rise is not None else rise)
                 for s in c.sizes]  # fmt: skip
    each = [thick * math.sin(min(Arch(d, r).half_angle, math.pi / 2)) for d, r in spans]
    return max(a + b for a, b in itertools.pairwise(each))
