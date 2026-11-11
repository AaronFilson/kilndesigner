"""C3a's engine pieces (`docs/planning/11-10-26.md` §C, "C3a as built"):

- **several fireboxes burning**: where the fireboxes stand on more than one side they are gas zones
  side by side (`chamber._plan`), each with its own faces, and the fuel and its air split among
  them by their grates' areas (`kiln.fire_shares`; `zone.Balance.released`), the chamber taking
  their products together; a staged firing's stream passes through them as air, shared the same;
- **Olsen's Rule 6 seeding p.78** (`paths.Inputs.rule6`; C1's question 8, open): where nothing on
  a gas path is sized, the chimney's side ⅕ to ¼ of the chamber's width and at least 9 in, a band,
  every path on it saying so.
"""

from __future__ import annotations

from dataclasses import replace

import fuel
import loads
import numpy as np
import path_inputs as pi
import pytest

from kilndesigner.v2.heat import chamber as ch
from kilndesigner.v2.heat import draft as dr
from kilndesigner.v2.heat import firing as fi
from kilndesigner.v2.heat import kiln as hk
from kilndesigner.v2.heat import series
from kilndesigner.v2.heat.air import burnt
from kilndesigner.v2.heat.draft import Element
from kilndesigner.v2.heat.zone import Balance, ZoneModel

IN = 0.0254
HOUR = 3600.0


def test_a_firebox_zones_surfaces_name_their_part_and_side() -> None:
    assert ch.fire_part("grate") == ("grate", "")
    assert ch.fire_part("firebox roof left") == ("firebox roof", "left")
    assert ch.fire_part("inlet flues front") == ("inlet flues", "front")
    assert ch.fire_part("floor 2") == ("", "")


@pytest.mark.geometry
def test_fireboxes_on_two_sides_are_two_zones_each_with_its_faces() -> None:
    """Kato's two coal fireboxes against the left and right walls (p.131): two gas zones, each
    its grate (the fire), its walls and roof of the firebox's own brick, and its mouth through
    its wall; the fuel shared half and half by their equal grates (30 × 22 in each)."""
    k = loads.design("kato-coal")
    c = ch.chamber(k, path=True)
    assert [g.name for g in c.gas] == ["firebox left", "firebox right", "chamber"]
    names = {z.name for z in c.zones}
    assert {"grate left", "grate right", "firebox walls left", "firebox walls right",
            "firebox roof left", "firebox roof right", "inlet flues left",
            "inlet flues right"} <= names  # fmt: skip
    assert c.built["grate right"] == ("grate", 1)
    assert c.built["firebox roof left"] == ("firebox", 0)
    assert c.built["inlet flues right"] == ("walls", 1)
    assert hk.fire_shares(k, c) == ((0, 0.5), (1, 0.5))


def test_a_firebox_fired_on_its_floor_shares_by_its_hearth() -> None:
    """No grate (the anagama's 2 × 2 ft firebox, fired on its floor): its hearth's area."""
    fb = loads.design("anagama-hole").heat.fire.fireboxes[0]  # pyright: ignore[reportOptionalMemberAccess]
    assert hk._grate_area(fb) == pytest.approx((24 * IN) ** 2)  # pyright: ignore[reportPrivateUsage]


@pytest.fixture(scope="module")
def kato() -> ZoneModel:
    k = loads.design("kato-coal")
    return hk.heat_model(k, loads.loads("kato-coal"), 1.0, fuel.own_fuels("kato-coal")[0],
                         n_rays=2_000, path=True, path_inputs=pi.inputs("kato-coal"))  # fmt: skip


@pytest.mark.geometry
def test_the_stream_splits_among_the_firebox_zones(kato: ZoneModel) -> None:
    """Each firebox zone takes its share of the air and the fuel; what the chamber takes is their
    products together, so the zones release what one zone would: the room's air and the fuel in,
    the last zone's stream out (`air.burnt` is linear in the fuel and air together)."""
    m = kato
    assert m.fires == ((0, 0.5), (1, 0.5))
    assert m.burns == 0
    zones = next(s for s in m.steps if s.name == "The gas zones")
    assert zones.inputs == {"firebox left": "50% of the fuel and its air",
                            "firebox right": "50% of the fuel and its air"}  # fmt: skip
    assert zones.note == hk.SHARES_NOTE
    # Each firebox zone's section over its share: the whole stream gives each its own velocity
    assert m.gas[0].flow.area == pytest.approx(2 * 30 * 26 * IN**2)
    bal = Balance(m)
    p = m.products
    tg = np.array([1700.0, 1650.0, 1500.0])
    fuel_rate, air = 0.03, 0.03 * p.air * 1.2
    q = bal.released(tg, fuel_rate, air)
    room = air * p.h_air(p.t_air)
    assert q.sum() == pytest.approx(room + fuel_rate * p.fuel_enthalpy
                                    - burnt(p, fuel_rate, air, 1500.0).flow, rel=1e-12)  # fmt: skip
    half = 0.5 * room + 0.5 * fuel_rate * p.fuel_enthalpy
    assert q[0] == pytest.approx(half - burnt(p, fuel_rate / 2, air / 2, 1700.0).flow, rel=1e-12)
    into = burnt(p, fuel_rate / 2, air / 2, 1700.0).flow + burnt(p, fuel_rate / 2, air / 2,
                                                                 1650.0).flow  # fmt: skip
    assert q[2] == pytest.approx(into - burnt(p, fuel_rate, air, 1500.0).flow, rel=1e-12)


@pytest.mark.slow
@pytest.mark.geometry
def test_both_fireboxes_burn_and_the_energy_closes(kato: ZoneModel) -> None:
    """A fixed rate for an hour: both firebox zones hot and alike (their fireboxes are), the
    chamber cooler; the heat balance closes to round-off."""
    f = fi.fire(kato, fi.FixedInput(0.03), HOUR, sample=600.0)
    left, right, room = f.t_gases[-1]
    assert min(left, right) > room > 700.0
    assert left == pytest.approx(right, rel=0.05)
    e = f.energy
    closure = e["fuel heat"] - e["flue"] - e["walls"] - e["setting"] - e["openings"]
    assert abs(closure) < 1e-9 * e["fuel heat"]
    assert e["walls: firebox left"] > 0
    assert e["walls: firebox right"] > 0


@pytest.mark.slow
@pytest.mark.geometry
def test_a_stage_in_the_chamber_passes_air_through_both_fireboxes(kato: ZoneModel) -> None:
    """The fuel burning in the chamber's zone (a stage, `series.stage_model`): the firebox zones
    side by side carry the room's air, half each, cooler than the chamber; the balance closes."""
    m = series.stage_model(kato, 0)
    assert m.burns == 2
    f = fi.fire(m, fi.FixedInput(0.03), HOUR / 2, sample=600.0)
    left, right, room = f.t_gases[-1]
    assert max(left, right) < room
    e = f.energy
    closure = e["fuel heat"] - e["flue"] - e["walls"] - e["setting"] - e["openings"]
    assert abs(closure) < 1e-9 * e["fuel heat"]


@pytest.mark.geometry
def test_fireboxes_side_by_side_are_the_paths_first_zones(kato: ZoneModel) -> None:
    with pytest.raises(ValueError, match="side by side"):
        replace(kato, fires=((1, 0.5), (2, 0.5)))
    with pytest.raises(ValueError, match="side by side"):
        replace(kato, fires=((0, 0.5), (1, 0.6)))


def test_a_start_is_tried_from_each_guess_in_turn() -> None:
    """A max fire's first consistent state: where the root finders can't converge from the first
    guess (here a residual with a minimum short of zero near it), the next is tried; with none
    converging, the firing is refused (`firing._consistent`)."""

    def resfn(t: float, y: np.ndarray, yp: np.ndarray, res: np.ndarray) -> None:
        x = float(y[0])
        res[0] = x * x + 1.0 if x < 5.0 else x - 6.0

    got = fi._consistent(resfn, np.array([0.0]), [0], 0.0, 1, (np.array([7.0]),))  # pyright: ignore[reportPrivateUsage]
    assert got[0] == pytest.approx(6.0)
    with pytest.raises(fi.FiringError, match="no consistent start"):
        fi._consistent(resfn, np.array([0.0]), [0], 0.0, 1, (np.array([1.0]),))  # pyright: ignore[reportPrivateUsage]


# --- Rule 6 seeding p.78 -------------------------------------------------------------------------


def _named(path: dr.Path, name: str) -> Element:
    def flat(els: tuple[Element, ...]) -> list[Element]:
        out: list[Element] = []
        for e in els:
            out += [x for b in e.parts for x in flat(b)] if e.kind == "parallel" else [e]
        return out

    return next(e for e in flat(path.elements) if e.name == name and e.kind != "column")


@pytest.mark.geometry
def test_rule_6_seeds_p78_where_nothing_on_the_path_is_sized() -> None:
    """La Borne (p.110): two chimneys, nothing sized, so C1 refuses its path. Asked for, Rule 6
    (pp.79–80) sizes the whole chimney section from the 11 ft (132 in) width, its side 26.4 in at
    the band's least-air end and 33 in at its most, the two chimneys sharing it; and every path on
    it says so, with the owner's question it rests on."""
    k = loads.design("la-borne")
    with pytest.raises(dr.NotModelledError, match=r"p\.78"):
        dr.kiln_path(k, inputs=pi.inputs("la-borne"))
    path = dr.kiln_path(k, inputs=pi.inputs("la-borne", rule6=True))
    note = path.steps[0].note or ""
    assert "Rule 6" in note
    assert "question 8" in note
    least = _named(path, "chimney")
    assert least.branches == 2
    assert least.area == pytest.approx((132 / 5 * IN) ** 2 / 2)
    most = _named(path.most(), "chimney")
    assert most.area == pytest.approx((132 / 4 * IN) ** 2 / 2)


@pytest.mark.geometry
def test_rule_6_is_never_under_nine_inches() -> None:
    """The Kannofen's 1.05 m (41.3 in) tunnel: a fifth of it is 8.3 in, under the "seldom under 9 x
    9in" (p.80), so the band runs 9–10.3 in; an updraft, its exit flue p.78's of that section."""
    path = dr.kiln_path(loads.design("kannofen"), inputs=pi.inputs("kannofen", rule6=True))
    assert _named(path, "exit flue, sharp entrance").area == pytest.approx((9 * IN) ** 2)
    assert _named(path.most(), "exit flue, sharp entrance").area == pytest.approx((1.05 / 4) ** 2)
    assert {"la-borne", "kannofen"} <= pi.RULE_6
