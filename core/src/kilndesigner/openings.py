"""Openings: exit flues of any count and layout, the chimneys and their connection, dampers and
passive air, and the vent holes, salt ports and vapour holes of ``Kiln.openings``.

Each set of holes is cut where the design says, or spread evenly: along a wall with its foot on
the floor, or in an even grid over the floor or under the roof. Holes in a wall are placed as
ports are (``hardware.Faces.place``), so one that doesn't fit is refused with its reason; holes in
the floor and the roof are cut through them and taken out of the brick count, as floor burner
ports are (``hardware.floor_and_roof_holes``).

The stated exit flues' areas add up to the flue area the rules use: Olsen's exit flue as large as
the burner ports (The Kiln Book, 4th ed., p.151) and the exit flues a little smaller than the
chimney where they enter it (p.78).
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

from kilndesigner.model import Holes, Kiln
from kilndesigner.units import si
from kilndesigner.working import Finding, Step

if TYPE_CHECKING:
    from kilndesigner.fire import FireDesign
    from kilndesigner.gas import GasDesign
    from kilndesigner.hardware import Faces, Hardware

EXITS_SOURCE = (
    "Olsen, The Kiln Book, 4th ed., p.78 (the exit flues a little smaller than the chimney where "
    "they enter it), p.151 (the exit flue as large as the burner ports to start)"
)
OPENINGS_SOURCE = "the design: draft.exits and openings, cut where it places them"

SLUGS = {"exit flue": "exit", "vent": "vent", "salt port": "salt", "vapour hole": "vapour"}
FLOOR_AND_ROOF = tuple(f"port/{s}-" for s in SLUGS.values())
"""The names of the openings this module cuts, for the brick count to take out."""


def exit_flues_step(
    sum_text: str,
    total: float,
    against: tuple[float, str] | None = None,
    source: str = EXITS_SOURCE,
) -> Step:
    """The working for the stated exit flues, added up; with ``against``, Olsen's starting size
    and how it was found, beside them."""
    inputs = {"exit flues": sum_text}
    if against is not None:
        start, how = against
        inputs["Olsen's starting size"] = f"{start:.0f} in² ({how})"
        inputs["as built ÷ starting size"] = f"{total / start:.2f}"
    return Step(
        name="Exit flues as built, together",
        value=f"{total:.0f} in²",
        formula="Σ count × each hole's area",
        inputs=inputs,
        reference=source,
    )


def wall_places(h: Holes, inside: float) -> list[tuple[float, float]]:
    """Each hole's (across, up) on a wall ``inside`` in wide (in): as placed, or spread evenly
    with its foot on the floor."""
    _, ht = h.port.size_in()
    if h.places is not None:
        return [
            (si(p.across, "in"), si(p.up, "in") if p.up is not None else ht / 2) for p in h.places
        ]
    n = h.wanted
    return [(-inside / 2 + (k + 0.5) * inside / n, ht / 2) for k in range(n)]


def grid_places(h: Holes, width: float, depth: float) -> list[tuple[float, float]]:
    """Each hole's (across, along) over a ``width`` × ``depth`` floor or roof (in): as placed, or
    in an even grid, row by row from the front."""
    if h.places is not None:
        return [(si(p.across, "in"), si(p.along, "in")) for p in h.places]
    n = h.wanted
    cols = max(1, min(n, round(math.sqrt(n * width / depth))))
    rows = math.ceil(n / cols)
    out: list[tuple[float, float]] = []
    for k in range(n):
        r, c = divmod(k, cols)
        in_row = min(cols, n - r * cols)
        out.append((-width / 2 + (c + 0.5) * width / in_row, -depth / 2 + (r + 0.5) * depth / rows))
    return out


def _sets(kiln: Kiln) -> list[tuple[str, Holes]]:
    sets: list[tuple[str, Holes]] = []
    if kiln.draft is not None and kiln.draft.exits is not None:
        sets += [("exit flue", h) for h in kiln.draft.exits]
    if kiln.openings is not None:
        sets += kiln.openings.all()
    return sets


def cut_openings(kiln: Kiln, f: Faces, hw: Hardware) -> None:
    """Cut every set of holes: the exit flues and the vents, salt ports and vapour holes."""
    from kilndesigner.hardware import MM, Opening, PortSpot

    w, d = si(kiln.chamber.width, "in"), si(kiln.chamber.depth, "in")
    if kiln.chamber.shape == "round":  # the grid inside the square the circle holds
        w = d = w / math.sqrt(2)
    top = si(kiln.chamber.height, "in")
    numbers: dict[str, int] = {}
    for kind, h in _sets(kiln):
        slug = SLUGS[kind]
        numbers[slug] = numbers.get(slug, 0) + 1
        pw, ph = h.port.size_in()
        title = kind[0].upper() + kind[1:]
        if h.through in ("floor", "roof"):
            z = (f.bottom - 1, 1.0) if h.through == "floor" else (top - 1, 1e4)
            for k, (x, y) in enumerate(grid_places(h, w, d), 1):
                box = (
                    ((x - pw / 2) * MM, (y - ph / 2) * MM, z[0] * MM),
                    ((x + pw / 2) * MM, (y + ph / 2) * MM, z[1] * MM),
                )
                hw.openings.append(
                    Opening(
                        f"port/{slug}-{numbers[slug]}-{k}",
                        f"{title} {numbers[slug]}.{k}, in the {h.through}",
                        box,
                        2 if h.port.round else None,
                    )
                )
            continue
        wall = h.through
        for k, (across, up) in enumerate(wall_places(h, f.inside[wall]), 1):
            f.place(
                kiln,
                hw,
                PortSpot(
                    f"port/{slug}-{numbers[slug]}-{k}",
                    f"{title} {numbers[slug]}.{k}",
                    "opening",
                    wall,
                    across,
                    up,
                    pw,
                    ph,
                    h.port.round,
                ),
            )
    if kiln.openings is not None:
        said = ", ".join(
            f"{h.wanted} {kind}{'s' if h.wanted > 1 else ''} in the {h.through}"
            for kind, h in kiln.openings.all()
        )
        hw.findings.append(
            Finding(
                level="info",
                message=(
                    f"Openings cut as the design places them: {said}. Plug each with a brick or a "
                    "bung when it's shut."
                ),
                reference=OPENINGS_SOURCE,
            )
        )


def chimney_centres(kiln: Kiln, inside: float) -> list[float]:
    """Where each chimney stands along the flue wall's face (in from its middle): one at the
    flue, or several spread evenly along the wall."""
    draft = kiln.draft
    assert draft is not None
    n = draft.chimneys
    if n == 1:
        return [si(draft.flue_across, "in") if draft.flue_across is not None else 0.0]
    return [-inside / 2 + (k + 0.5) * inside / n for k in range(n)]


def crown_chimney(
    kiln: Kiln, gas: GasDesign | FireDesign, f: Faces, hw: Hardware, area: float
) -> None:
    """A chimney rising through the roof's crown, in the middle of the chamber, as Kähler's salt
    kiln's (Olsen, The Kiln Book, 4th ed., Figs 5-17, 5-18): the flue is its inside, cut through
    the roof; its walls, one 4½ in layer of hard brick, stand on the roof's outside top."""
    from kilndesigner.allowance import allowance
    from kilndesigner.fire import FireDesign
    from kilndesigner.gas import kiln_top_in
    from kilndesigner.hardware import BRICK, CHIMNEY_BRICK, MM, Opening, Piece

    draft = kiln.draft
    assert draft is not None
    built = draft.chimney.inside if draft.chimney is not None else None
    if built is not None and built.diameter is not None:
        a = b = si(built.diameter, "in")
    elif built is not None:
        assert built.width is not None
        assert built.depth is not None
        a, b = si(built.width, "in"), si(built.depth, "in")
    else:
        need = gas.chimney_area_in2 if isinstance(gas, FireDesign) else area
        side = 4.5 * math.ceil(math.sqrt(need) / 4.5 - 1e-9)
        a = b = side
    h = si(kiln.chamber.height, "in")
    hw.openings.append(
        Opening(
            "port/flue",
            "Flue through the crown",
            ((-a / 2 * MM, -b / 2 * MM, (h - 1) * MM), (a / 2 * MM, b / 2 * MM, 1e4 * MM)),
            2 if built is not None and built.diameter is not None else None,
        )
    )
    if gas.chimney_height_in is None:
        return
    wall = 4.5
    z0, z1 = kiln_top_in(kiln), max(gas.chimney_height_in, kiln_top_in(kiln) + 1)
    outer = ((-a / 2 - wall, -b / 2 - wall), (a / 2 + wall, b / 2 + wall))
    rings = [
        ((outer[0][0], outer[0][1]), (outer[1][0], -b / 2)),  # front
        ((outer[0][0], b / 2), (outer[1][0], outer[1][1])),  # back
        ((outer[0][0], -b / 2), (-a / 2, b / 2)),  # left
        ((a / 2, -b / 2), (outer[1][0], b / 2)),  # right
    ]
    boxes = tuple(
        ((x0 * MM, y0 * MM, z0 * MM), (x1 * MM, y1 * MM, z1 * MM)) for (x0, y0), (x1, y1) in rings
    )
    volume = sum((x1 - x0) * (y1 - y0) * (z1 - z0) for (x0, y0), (x1, y1) in rings)
    hw.pieces.append(
        Piece(
            "chimney/stack",
            "dense_firebrick",
            "Chimney through the crown",
            f"{a:g} × {b:g} in inside, rising through the crown to {z1 / 12:.1f} ft above the "
            "chamber floor, one 4½ in layer of hard brick (kiln-hardware.md §3.2 [S4]). Height: "
            f"{gas.chimney_height}.",
            boxes=boxes,
            material=CHIMNEY_BRICK,
        )
    )
    del f
    hw.chimney_bricks = allowance(kiln, "brick").buy(volume / math.prod(BRICK))


__all__ = [
    "EXITS_SOURCE",
    "FLOOR_AND_ROOF",
    "chimney_centres",
    "crown_chimney",
    "cut_openings",
    "exit_flues_step",
    "grid_places",
    "wall_places",
]
