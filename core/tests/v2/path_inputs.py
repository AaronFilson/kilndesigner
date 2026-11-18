"""Each reference kiln's draft-path inputs from the dataset (C1, `v2/heat/paths.py`): what the
design file can't say, read from the kiln's facts by the precedence of `11-09-26.md` §A (printed
> scaled > drawing; derived as printed), each with its page.

- the air intakes (research A2: ``primary_air``, ``secondary_air``);
- the grate's bars (``grate_bar``);
- the chimney: a printed or scaled height band (``chimney_height``, its least to its most), its
  inside sides (``chimney_width``, ``chimney_depth``), round where the book prints it round with
  no size (p.78 then gives its area), none where it prints no stack (``chimney_count`` 0);
- flues the design gives none of, or gives otherwise (``exit_flue_*``, ``inlet_flue_*``,
  ``between_flue_*``): a count or a size left out is p.78's, in the engine;
- the connection into the chimney (``connection_width``, ``connection_height``);
- the oil drip's draft where the design has none (the dataset's ``draft``);
- the fireboxes one to a chamber, as the book draws them (the owner's question 3: Suzuki, Tobe
  and Hotchkiss, whose design files lay them side by side at the front).
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import fuel as own
import reference as ref

from kilndesigner.v2.heat import draft as dr
from kilndesigner.v2.heat.paths import Band, Flues, Inputs, Stack

GIVEN = ("printed", "derived", "scaled", "drawing")
# C1's own words take the dataset's assumptions too (each with its reason); a chimney's height
# doesn't: an assumed one is the design file's, which holds it
WITH_ASSUMED = (*GIVEN, "assumed")
# The book draws each chamber's own firebox (a himae or a stoking channel along its front wall);
# their design files lay as many fireboxes side by side at the first chamber's front (the owner's
# question 3, `11-10-26.md` §B, B4–B6): the path takes the book's. The Kyoto type's himae, one in
# each chamber (p.92, Fig 4-34), joined them on 2026-11-18, when its chambers became 14 ft across
# and ten 9 in fireboxes would otherwise fit side by side at its front
ONE_PER_CHAMBER = frozenset({"suzuki-kyoto", "tobe", "hotchkiss-raw-clay", "kyoto-climbing"})
# The six kilns with nothing on their gas path sized (C1's refused six): their paths are built only
# on Olsen's Rule 6 seeding p.78 (`paths.Inputs.rule6`), asked for by the tests that run them,
# `inputs(kid, rule6=True)`, and every result on it says so. The owner answered on 2026-11-17
# (11-17-26-inputs.md §1), applied 2026-11-18: the drawing's scale where the part is drawn, else
# ¼ of the width (`paths.rule6`). The anagama in the hole left the set then: its flue is drawn,
# 4–8 in, its depth not, so ¼ of the width (the dataset's chimney_width and chimney_depth)
RULE_6 = frozenset({"falcone-pompeii", "fireworks-edmonton", "kannofen", "kitade-tojilo",
                    "la-borne"})  # fmt: skip


def _kiln(kid: str) -> dict[str, Any]:
    return own._kilns()[kid]  # pyright: ignore[reportPrivateUsage]


def _band(kiln: dict[str, Any], what: str, unit: str = "m") -> Band | None:
    """The union of a kiln's numeric facts of one kind (a chimney's height only as the book gives
    it), as a band with its pages."""
    statuses = GIVEN if what == "chimney_height" else WITH_ASSUMED
    fs = [f for f in ref.facts(kiln, "flow", what, *statuses) if ref.numeric(f)]
    if not fs:
        return None
    spans = [ref.span(f, unit) for f in fs]
    pages = "; ".join(f"{f['status']}, {f.get('page', '')}" for f in fs)
    lo, hi = min(s[0] for s in spans), max(s[1] for s in spans)
    return Band(lo, hi, f"the dataset's {what}: {pages}")


def _count(kiln: dict[str, Any], what: str) -> int | None:
    fs = [f for f in ref.facts(kiln, "flow", what, *WITH_ASSUMED) if ref.numeric(f)]
    return int(ref.raw(fs[0])[0]) if fs else None


def _flues(kiln: dict[str, Any], kind: str) -> Flues | None:
    width = _band(kiln, f"{kind}_width")
    height = _band(kiln, f"{kind}_height")
    count = _count(kiln, f"{kind}_count")
    if width is None and height is None:
        area = _band(kiln, f"{kind}_area", "m**2")  # their whole area only (the exits')
        return None if area is None else Flues(count=count, area=area, source=area.source)
    source = ", ".join(b.source for b in (width, height) if b is not None)
    return Flues(width, count, height, source=source)


def intakes(kid: str) -> dr.Intakes | None:
    """A kiln's air intakes from the dataset (firebox-air-intakes.md §3), all its fireboxes'."""
    got = own.own_intakes(kid)
    if got is None:
        return None
    return dr.Intakes(*got, reference=f"{kid}'s, the dataset's (firebox-air-intakes.md §3)")


def stack(kiln: dict[str, Any]) -> Stack | None:
    """The chimney as the dataset gives it: a height band, its sides, round with no size."""
    height = _band(kiln, "chimney_height")
    if height is not None and height.lo == height.hi:
        height = None  # one printed height: the design file's (it holds it)
    width, depth = _band(kiln, "chimney_width"), _band(kiln, "chimney_depth")
    words = [str(f["value"]) for f in ref.facts(kiln, "flow", "chimney_section", *GIVEN)]
    rnd = width is None and any(w.startswith("round") for w in words)
    if height is None and width is None and not rnd:
        return None
    source = "; ".join(b.source for b in (height, width, depth) if b is not None)
    if rnd:
        source = "the dataset's chimney section: round, its size not printed"
    return Stack(height=height, width=width, depth=depth, round=rnd, source=source)


def inputs(kid: str, **change: Any) -> Inputs:
    """A reference kiln's path inputs from the dataset; ``change`` sets any field over them."""
    kiln = _kiln(kid)
    bar = _band(kiln, "grate_bar")
    conn_w, conn_h = _band(kiln, "connection_width"), _band(kiln, "connection_height")
    got = Inputs(
        grate_bar=bar.lo if bar is not None else None,
        intake=intakes(kid),
        stack=stack(kiln),
        exits=_flues(kiln, "exit_flue"),
        inlets=_flues(kiln, "inlet_flue"),
        between=_flues(kiln, "between_flue"),
        connection=(conn_w, conn_h) if conn_w is not None and conn_h is not None else None,
        one_per_chamber=kid in ONE_PER_CHAMBER,
        updraft=kiln.get("draft") == "up",
        stackless=_count(kiln, "chimney_count") == 0,
    )
    return replace(got, **change)
