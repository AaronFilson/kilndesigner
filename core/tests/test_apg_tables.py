"""Bricks to turn a circle, against A.P. Green's tables (*Firebrick Shapes, Standard and Special*,
brick-shapes.md): the shapes' sizes (p.95–98), the complete circles (p.111–116, p.128–135)
and the sprung arches (p.164–189).

Olsen's tables A-4 to A-7 (test_rings.py) set the method; A.P. Green's are a second, longer set
of the same arithmetic. A.P. Green carries three shapes Olsen's tables don't use, a No. 1-X wedge
and the 3 in series' No. 4 arch and No. 1 wedge (p.96, p.98), an option (``ring(..., apg=True)``);
Olsen's families stay the default."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pytest

from kilndesigner.geometry import ArchShape, Part
from kilndesigner.masonry import arch_ring
from kilndesigner.rings import FAMILIES, IN, Series, apg_family, ring

DATA: dict[str, Any] = json.loads(
    (Path(__file__).parent / "apg_circles.json").read_text(encoding="utf-8")
)


def _name(series: Series, shape: str) -> str:
    """The engine's name for a shape in A.P. Green's table."""
    family = apg_family(series)
    if shape == "straight":
        return family.straight
    return next(t.name for t in family.tapers if t.name.startswith(shape))


def test_the_engines_shapes_are_a_p_greens() -> None:
    """Every thin end the engine uses is printed on p.95–98, including the 3 in series' ones the
    engine derived from Olsen's tables because his shape page is faint (rings.py)."""
    printed = {
        "arch": {"No. 3 arch": 1.0, "No. 2 arch": 1.75, "No. 1 arch": 2.125},  # p.95
        "wedge": {"No. 2 wedge": 1.5, "No. 1 wedge": 1.875},  # p.96
        "key": {"No. 4 key": 2.25, "No. 3 key": 3.0, "No. 2 key": 3.5, "No. 1 key": 4.0},  # p.96
        "arch3": {"No. 3 arch": 2.0, "No. 2 arch": 2.5, "No. 1 arch": 2.75},  # p.98
        "wedge3": {"No. 3 wedge": 2.0, "No. 2 wedge": 2.5},  # p.98
    }
    for series, shapes in printed.items():
        for taper in FAMILIES[series].tapers:  # type: ignore[index]
            key = taper.name.split(",")[0]
            assert taper.thin == shapes[key], (series, taper.name)


ROWS = [
    pytest.param(series, d, counts, total, id=f"{series}-{d}in")
    for series, table in DATA["tables"].items()
    for d, counts, total in table["rows"]
]


@pytest.mark.parametrize(("series", "d", "counts", "total"), ROWS)
def test_circles_match_a_p_greens_tables(
    series: Series, d: int, counts: dict[str, int], total: int
) -> None:
    """Within a brick of A.P. Green's total and two of each shape: the tables round by their own
    rule, which the catalogue doesn't print (p.109: 'No joint allowance was used')."""
    r = ring(d * IN, series, apg=True)
    assert abs(r.total - total) <= 1
    got = dict(r.counts)
    for shape, n in counts.items():
        assert abs(got.get(_name(series, shape), 0) - n) <= 2, shape


def test_every_table_is_read() -> None:
    """The rows left out are those read with doubt or whose printed total isn't their sum."""
    assert {s: len(t["rows"]) for s, t in DATA["tables"].items()} == {
        "arch": 143,
        "arch3": 145,
        "wedge": 150,
        "wedge3": 142,
        "key": 101,
    }


ARCHES: dict[str, Any] = json.loads(
    (Path(__file__).parent / "apg_arches.json").read_text(encoding="utf-8")
)
ARCH_ROWS = [
    pytest.param(float(depth), span, radius, angle, total, id=f"{depth}in-{angle}deg-{span:g}in")
    for depth, table in ARCHES["tables"].items()
    for span, radius, angle, total in table["rows"]
]


@pytest.mark.parametrize(("depth", "span", "radius", "angle", "total"), ARCH_ROWS)
def test_arch_courses_match_a_p_greens_sprung_arches(
    depth: float, span: float, radius: float, angle: int, total: int
) -> None:
    """Bricks per course of a sprung arch, 4½ in (p.164–170) and 9 in (p.176–189) thick, at the
    four rises A.P. Green tabulates (56°, 60°, 74°, 84°). The engine turns each course with one
    taper and straights where A.P. Green mixes two tapers, so only the count is compared: within
    a brick of the table."""
    half = math.radians(angle) / 2
    rise = radius * (1 - math.cos(half))
    along = 9.0 if depth == 4.5 else 4.5  # one brick along the kiln
    part = Part(
        "roof/1",
        "hard-firebrick-kx99",
        "firebrick",
        (0.0, 0.0, 0.0),
        (span * IN, along * IN, rise * IN),
        arch=ArchShape(radius * IN, depth * IN, 0.0, half),
        face="roof",
    )
    course = arch_ring(part)
    assert course is not None
    assert course.rings == 1
    assert abs(course.shaped + course.straights - total) <= 1


def test_every_arch_table_is_read() -> None:
    assert {d: len(t["rows"]) for d, t in ARCHES["tables"].items()} == {"4.5": 174, "9": 377}


def test_a_p_greens_shapes_are_an_option_and_olsens_the_default() -> None:
    """A 10 ft ring of 9 in wedges: straights with Olsen's shapes, No. 1-X wedges with A.P.
    Green's (p.130); a series with no extra shape is the same either way."""
    olsen = dict(ring(120 * IN, "wedge").counts)
    apg = dict(ring(120 * IN, "wedge", apg=True).counts)
    assert "No. 1-X wedge" not in olsen
    assert olsen["straight"] > 0
    assert apg["No. 1-X wedge"] > 0
    assert apg_family("key") is FAMILIES["key"]
