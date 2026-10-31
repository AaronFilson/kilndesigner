"""The chamber's inside as shape data (outline.py): a plan outline, walls standing on it to the
springline, and over them vaults (sections along runs) or domes.

The named types in a design file are shorthands for a form (``form_of``): a box is a rectangle,
a round chamber a circle or a faceted ring's polygon; a sprung arch is one arch section run along
the chamber, or across each chamber in a row; a catenary a crown springing from the floor; a dome
a sphere over the plan. The form gives the same chamber that shape.chamber_shape does (the tests
hold every example to it), so a shape the names can't say (a teardrop plan, a vault changing
along its length) can be given as a form and treated the same way. A curved plan
(chamber.outline: a teardrop or an oval) is one now: shape.chamber_shape takes its faces and
volume from its form.

As shape.py, a chamber on a slope or turned in plan is taken as laid out straight and level.
"""

from __future__ import annotations

from dataclasses import dataclass

from kilndesigner.model import CatenaryArch, Dome, Kiln, OpenTop, SprungArch, arches_along
from kilndesigner.outline import (
    Outline,
    Point,
    Run,
    SphereDome,
    arch_section,
    circle,
    curve_section,
    flat_teardrop,
    necked_teardrop,
    oval,
    prism,
    rectangle,
    regular_polygon,
)
from kilndesigner.units import si


@dataclass(frozen=True)
class Form:
    """A chamber: walls ``height`` high round ``plan`` (from the floor to the springline; none
    under a catenary), then ``vaults`` and ``domes`` above the springline, or nothing at all over
    an ``open_top`` or a flat roof."""

    plan: Outline
    height: float
    vaults: tuple[Run, ...] = ()
    domes: tuple[SphereDome, ...] = ()
    open_top: bool = False

    @property
    def volume(self) -> float:
        """The walls' prism, and the space under each vault and dome above the springline."""
        return (
            self.plan.area * self.height
            + sum(v.volume for v in self.vaults)
            + sum(d.volume for d in self.domes)
        )


CATENARY_STEPS = 256  # chords along a catenary's crown: its area within 1e-5 of the curve's


def plan_of(kiln: Kiln, unit: str = "m") -> Outline:
    """A curved plan (chamber.outline) in ``unit``, centred on the chamber: its front at −y.
    Raises ValueError for sizes that don't make the shape."""
    c, o = kiln.chamber, kiln.chamber.outline
    assert o is not None
    w, d = si(c.width, unit), si(c.depth, unit)
    if o.shape == "oval":
        assert o.end_radius is not None
        # outline.oval runs its length along y, as the chamber's depth
        return oval(w, d, si(o.end_radius, unit))
    front = si(o.front_width, unit) if o.front_width is not None else None
    side = si(o.side_radius, unit) if o.side_radius is not None else None
    if o.neck_width is not None:
        assert front is not None
        assert side is not None
        assert o.neck_length is not None
        assert o.neck_radius is not None
        return necked_teardrop(w, d, front, side, si(o.neck_width, unit),
                               si(o.neck_length, unit), si(o.neck_radius, unit))  # fmt: skip
    return flat_teardrop(w, d, front, side)


def crown_of(kiln: Kiln, unit: str = "m") -> Point:
    """Where a dome over a curved plan has its crown, in plan (``unit``): ``crown_at`` behind
    the front wall, on the long axis, or the middle."""
    roof = kiln.roof
    at = roof.crown_at if isinstance(roof, Dome) else None
    if at is None:
        return (0.0, 0.0)
    return (0.0, si(at, unit) - si(kiln.chamber.depth, unit) / 2)


def form_of(kiln: Kiln) -> Form:
    """The form the design's named chamber and roof types stand for, in metres (as
    shape.chamber_shape, which this follows case by case)."""
    from kilndesigner.shape import CatenaryCurve, facets

    c, roof = kiln.chamber, kiln.roof
    w, d, h = si(c.width, "m"), si(c.length, "m"), si(c.height, "m")
    if c.outline is not None:
        plan = plan_of(kiln)
        if isinstance(roof, Dome):
            crown = crown_of(kiln)
            return Form(plan, h, domes=(SphereDome(plan, si(roof.rise, "m"), crown),))
        return Form(plan, h, open_top=isinstance(roof, OpenTop))
    if c.shape == "round":
        sides = facets(kiln)
        if sides is None:
            plan = circle(w)
        else:
            from kilndesigner.rings import inside_apothem

            plan = regular_polygon(sides, inside_apothem(w, sides))
        # A faceted ring's dome is still the sphere over the round chamber (shape.RoundDome)
        domes = (SphereDome(circle(w), si(roof.rise, "m")),) if isinstance(roof, Dome) else ()
        return Form(plan, h, domes=domes, open_top=isinstance(roof, OpenTop))
    plan = rectangle(w, d)
    if isinstance(roof, OpenTop):
        return Form(plan, h, open_top=True)
    n, one = c.chambers, si(c.depth, "m")
    # Each chamber in a row, centred along y
    centres = [-d / 2 + (i + 0.5) * one for i in range(n)]
    if isinstance(roof, SprungArch) and arches_along(kiln):
        # An arch over each chamber, spanning along the draft and running across the kiln
        section = arch_section(one, si(roof.rise, "m"))
        runs = tuple(prism(section, w, axis=(1.0, 0.0), offset=y) for y in centres)
        return Form(plan, h, vaults=runs)
    if isinstance(roof, Dome) and n > 1:
        rise = si(roof.rise, "m")
        domes = tuple(SphereDome(rectangle(w, one, (0.0, y)), rise, (0.0, y)) for y in centres)
        return Form(plan, h, domes=domes)
    if isinstance(roof, SprungArch):
        return Form(plan, h, vaults=(prism(arch_section(w, si(roof.rise, "m")), d),))
    if isinstance(roof, CatenaryArch):
        # From the right foot over to the left, anticlockwise
        crown = curve_section(CatenaryCurve(w, h).offset(0.0, CATENARY_STEPS)[::-1])
        return Form(plan, 0.0, vaults=(prism(crown, d),))
    if isinstance(roof, Dome):
        return Form(plan, h, domes=(SphereDome(plan, si(roof.rise, "m")),))
    return Form(plan, h)
