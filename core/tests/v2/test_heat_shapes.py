"""Every chamber shape in v2's heat model (part C2): a round chamber's and a crossing's walls grow
to their outsides as the engine's own shape grows them, checked against geometry worked by hand;
Hollyweird's domes traced as built; the class values a wall takes where its material has none;
and `heat_model` builds for every reference kiln at λ 1 with its own load, fuel or elements."""

from __future__ import annotations

import math
from pathlib import Path

import fuel
import loads
import numpy as np
import pytest
import reference as ref

from kilndesigner.designfile import load_design
from kilndesigner.library import material
from kilndesigner.shape import SailDome
from kilndesigner.units import si
from kilndesigner.v2.heat import chamber as ch
from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat import sources as src

ROOT = Path(__file__).resolve().parents[3]
IN = 0.0254
KILNS = sorted(ref.load()["kilns"])
pytestmark = pytest.mark.geometry


def _face(m: object, name: str) -> object:
    return next(f for f in m.faces if f.name == name)  # pyright: ignore[reportAttributeAccessIssue]


def _thickness(kiln: object, face: str) -> float:
    return sum(si(x.thickness, "m") for x in kiln.lining.for_face(face))  # pyright: ignore[reportAttributeAccessIssue]


def test_a_round_chamber_grows_as_a_cylinder_and_a_dome() -> None:
    """Singh's round downdraft under its dome: the wall's outside is the cylinder moved out by its
    thickness, π(D + 2t)(h + 2t) over πDh; the floor's the disc, ((D + 2t)/D)²; the dome's the
    sphere moved out over the wall's outside circle, 2π(R + t)·cap (Derived by hand)."""
    k = loads.design("singh-coal")
    m = hk.heat_model(k, loads.loads("singh-coal"), 1.0, fuel.own_fuels("singh-coal")[0],
                      n_rays=2_000)  # fmt: skip
    d, h = si(k.chamber.width, "m"), si(k.chamber.height, "m")
    t = _thickness(k, "walls")
    wall = _face(m, "wall").wall  # pyright: ignore[reportAttributeAccessIssue]
    assert wall.area_out / wall.area_in == pytest.approx((d + 2 * t) * (h + 2 * t) / (d * h),
                                                         rel=1e-9)  # fmt: skip
    rise, tr = si(k.roof.rise, "m"), _thickness(k, "roof")  # pyright: ignore[reportAttributeAccessIssue]
    a = d / 2
    big = (a * a + rise * rise) / (2 * rise)
    inside = math.pi * (a * a + rise * rise)
    out_r, base = big + tr, a + tr
    outside = 2 * math.pi * out_r * (out_r - math.sqrt(out_r**2 - base**2))
    dome = _face(m, "roof").wall  # pyright: ignore[reportAttributeAccessIssue]
    assert dome.area_out / dome.area_in == pytest.approx(outside / inside, rel=1e-9)
    said = next(s for s in m.steps if s.name == "Said about the model").value
    assert "the engine's own chamber shape" in said
    assert "round wall" in said  # its wall openings are left out, said


def test_a_flat_floored_round_chamber_and_its_disc() -> None:
    """A round electric kiln under a flat roof (`round-electric`, 12 facets of cut brick): its floor
    and its lid grow as the 12-sided plan moved out by their thickness, ((a + t)/a)², a the
    polygon's apothem when its flats and corners average the width, D/(1 + 1/cos 15°) (Derived by
    hand); the plan's convection a disc's (πD²/4, D_h = D)."""
    k = load_design(ROOT / "examples" / "round-electric.yaml")
    c = ch.cavity(k)
    r = c.width / 2
    load = hk.Load(20.0, (-0.6 * r, -0.6 * r, 0.06), (0.6 * r, 0.6 * r, c.height - 0.1), 0.75,
                   "test input")  # fmt: skip
    m = hk.heat_model(k, load, 1.0, n_rays=2_000)
    d = c.width
    a = d / (1 + 1 / math.cos(math.pi / 12))
    for name in ("floor", "roof"):
        f = _face(m, name).wall  # pyright: ignore[reportAttributeAccessIssue]
        t = _thickness(k, name)
        assert f.area_out / f.area_in == pytest.approx(((a + t) / a) ** 2, rel=1e-9)
    assert m.gas[0].flow.area == pytest.approx(math.pi * d * d / 4)
    assert m.gas[0].flow.duct == pytest.approx(d)
    assert m.elements is not None  # electric: its elements as face sources


def test_a_crossing_grows_as_its_plan_and_vaults() -> None:
    """The Fireworks kiln: its floor is the 9 × 9 ft plan moved out by its thickness, an outline's
    A + P·t + 4t², here (108 in + 2t)²; its convection over that plan, D_h = 4A/P."""
    k = loads.design("fireworks-edmonton")
    m = hk.heat_model(k, loads.loads("fireworks-edmonton"), 1.0,
                      fuel.own_fuels("fireworks-edmonton")[0], n_rays=2_000)  # fmt: skip
    t = _thickness(k, "floor")
    side = 108 * IN
    floor = _face(m, "floor").wall  # pyright: ignore[reportAttributeAccessIssue]
    assert floor.area_out / floor.area_in == pytest.approx((side + 2 * t) ** 2 / side**2,
                                                           rel=1e-6)  # fmt: skip
    assert m.gas[0].flow.area == pytest.approx(side * side, rel=1e-6)
    assert m.gas[0].flow.duct == pytest.approx(side, rel=1e-6)
    assert {f.name for f in m.faces} >= {"left", "right", "front", "back", "floor", "roof"}


def test_hollyweirds_domes_are_traced() -> None:
    """Hollyweird's two chambers, each under its own sail dome (14 in rise): traced as built,
    not flat at the springline as massing's brick-only domes left them; each dome's area the
    sphere's over its chamber's plan (`shape.SailDome`) within 0.5 %."""
    k = loads.design("hollyweird")
    c = ch.cavity(k)
    rise = si(k.roof.rise, "m")  # pyright: ignore[reportAttributeAccessIssue]
    a = {z.name: float(np.sum(np.linalg.norm(np.cross(
        z.triangles[:, 1] - z.triangles[:, 0], z.triangles[:, 2] - z.triangles[:, 0]), axis=1))) / 2
         for z in c.zones}  # fmt: skip
    for j, r in enumerate(c.rooms, 1):
        w, d = r.hi[0] - r.lo[0], r.hi[1] - r.lo[1]
        assert a[f"roof {j}"] == pytest.approx(SailDome(w, d, rise).area(), rel=5e-3)
    boxes = sum((r.hi[0] - r.lo[0]) * (r.hi[1] - r.lo[1]) * (r.hi[2] - r.lo[2]) for r in c.rooms)
    domes = sum(SailDome(r.hi[0] - r.lo[0], r.hi[1] - r.lo[1], rise).volume for r in c.rooms)
    chambers = sum(g.volume for g in c.gas)
    assert chambers > boxes  # the domes are there
    assert chambers == pytest.approx(boxes + domes, rel=0.03)  # and the flues between


def test_the_class_values_a_wall_takes() -> None:
    """A castable with no maker's specific heat takes the VDI aluminosilicate class value
    (castables.md §14.3); a fibre blanket's hot face Fletcher and Williams' fibre lines (normal
    fibres 0.70 at 1273 K, × 0.95 hemispherical); stone the dense brick's band."""
    cast = hk._layer(loads.design("hollyweird").lining.roof[0])  # pyright: ignore[reportPrivateUsage, reportOptionalSubscript]
    vdi = material(src.CASTABLE_CP_FROM).specific_heat
    assert vdi is not None
    assert cast.heat_capacity.cp(np.array([1273.15]))[0] == pytest.approx(1072.0, rel=1e-3)
    fibre = hk._emissivity("cerachem-blanket-8pcf")  # pyright: ignore[reportPrivateUsage]
    assert fibre(np.array([1273.0]))[0] == pytest.approx(0.95 * 0.70, abs=0.005)
    low = hk._emissivity("cerachem-blanket-8pcf", "low")  # pyright: ignore[reportPrivateUsage]
    assert low(np.array([1273.0]))[0] == pytest.approx(0.95 * 0.54, abs=0.005)
    stone = hk._emissivity("granite", "high")  # pyright: ignore[reportPrivateUsage]
    assert stone.name == "dense-low"
    with pytest.raises(hk.NotModelledError, match="no hot-face emissivity"):
        hk._emissivity("calcium-silicate-promasil-1100")  # pyright: ignore[reportPrivateUsage]


def test_a_setting_is_held_by_the_chambers_gas() -> None:
    """A box in the traced solid (its corners, edges and faces), up into an arch over the
    springline; one poking through a wall isn't; with no solid kept, the rooms' boxes decide."""
    c = loads.traced("olsen-kit-24")
    r = c.rooms[0] if c.rooms else ch.Room((-c.width / 2, -c.depth / 2, 0.0),
                                           (c.width / 2, c.depth / 2, c.height), 0.0)  # fmt: skip
    assert c.holds((-0.2, -0.2, 0.1), (0.2, 0.2, c.height + 0.05))  # into the arch
    assert not c.holds((-0.2, -0.2, 0.1), (0.2, c.depth, 0.5))  # through the back wall
    bare = ch.Chamber((), (), c.width, c.depth, c.height, 0.0, rooms=(r,))
    assert bare.holds((-0.2, -0.2, 0.1), (0.2, 0.2, 0.5))
    assert not bare.holds((-0.2, -0.2, 0.1), (0.2, 0.2, c.height + 0.05))


@pytest.mark.slow
@pytest.mark.parametrize("kid", KILNS)
def test_heat_model_builds_for_every_reference_kiln(kid: str) -> None:
    """Every reference kiln's heat model at λ 1, with its own setting (one per chamber zone, at its
    band's middle), its own fuel, burners or elements; no draft path needed: where none is built,
    the working says the draft isn't worked out."""
    k = loads.design(kid)
    own = fuel.own_fuels(kid) if k.heat.fire is not None else []
    m = hk.heat_model(k, loads.loads(kid), 1.0, own[0] if own else None, n_rays=2_000)
    assert len(m.settings) == len(loads.dataset_bands(kid))
    assert all(f.wall.area_out > 0 for f in m.faces)
    said = next(s for s in m.steps if s.name == "Said about the model").value
    if m.path is None:
        assert "the draft isn't worked out" in said
