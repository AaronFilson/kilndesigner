"""C1: every reference kiln's own draft path (`v2/heat/paths.py`, the pieces in `draft.py`).

The new elements and path forms against closed forms and Idelchik's own figures; each kiln
family's built path against one written out by hand from its design file; each family's draft
against a Bernoulli estimate through its narrowest flue; and every one of the 53 reference kilns
built on its dataset inputs (`path_inputs.py`), or refused naming what is missing.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import path_inputs as pi
import pytest
import yaml

from kilndesigner.designfile import load_design
from kilndesigner.model import Kiln
from kilndesigner.numeric import find_root
from kilndesigner.v2.heat import draft as dr
from kilndesigner.v2.heat import gas
from kilndesigner.v2.heat import paths as pa

ROOT = Path(__file__).resolve().parents[3]
OLSEN = ROOT / "examples" / "olsen"
IN, FT = 0.0254, 0.3048
ROOM = (70 - 32) / 1.8 + 273.15
WOOD = gas.products(gas.wood(0.12, 19e6), 1.0, ROOM)
HOT = 1300 + 273.15


def _kiln(name: str, change: dict[str, Any] | None = None) -> Kiln:
    data = yaml.safe_load((OLSEN / f"{name}.yaml").read_text(encoding="utf-8"))
    for key, value in (change or {}).items():
        node = data
        *parents, last = key.split(".")
        for p in parents:
            node = node.setdefault(p, {})
        node[last] = value
    return Kiln.model_validate(data)


def _hot(path: dr.Path, t: float = HOT) -> dict[str, float]:
    return dict.fromkeys(("firebox", "chamber", "chimney", *path.zones), t)


# --- the new elements ----------------------------------------------------------------------------


def test_a_contraction_and_an_expansion_are_idelchiks() -> None:
    """3-9's 0.5(1 − F₀/F₁) on the narrow passage, 3-1's 0.50 from a large space; 4-1's sudden
    expansion (1 − F₀/F₂)², Idelchik's own stack example F₀/F₁ 0.27 → 0.53 (Table 1-11)."""
    assert dr.contraction("c", "chamber", 0.25, 1.0).k == pytest.approx(0.375)
    assert dr.contraction("c", "chamber", 0.25, 1e9).k == pytest.approx(0.5)
    assert dr.contraction("c", "chamber", 2.0, 1.0).k == 0.0
    assert dr.expansion("e", "chimney", 0.27, 1.0).k == pytest.approx(0.533, abs=1e-3)
    assert dr.expansion("e", "chimney", 1.0, 0.0).k == pytest.approx(1.0)
    assert "4-1" in dr.expansion("e", "chimney", 0.5, 1.0).note


def test_a_wall_with_through_gaps_meets_the_files_check() -> None:
    """8-4 at l/d_h 1.0 and f 0.5, τ 0.24: [(0.5 + 0.24·0.707)(0.5) + 0.25 + 0.02]/0.25 = 2.42 on
    the approach velocity (fittings-and-kiln-convection.md, the file's Derived check at its λ
    0.02). The jet's part comes on the holes' velocity (× f²), its friction a duct beside it."""
    w = 0.1
    jet, rub = dr.gaps("g", "chamber 1", 1, w, w, w, 2 * w * w)
    assert jet.k / 0.25 + 0.02 * 1.0 / 0.25 == pytest.approx(2.42, abs=5e-3)
    assert jet.area == pytest.approx(w * w)
    assert rub.kind == "duct"
    assert rub.length == pytest.approx(w)
    assert rub.dh == pytest.approx(w)
    many, _ = dr.gaps("g", "chamber 1", 5, 0.1, 0.2, 0.5, 2.0)
    assert many.branches == 5
    assert "8-4" in many.note


def test_several_flues_into_one_chimney_expand_together() -> None:
    """Flues side by side turning up into a much deeper chimney: the expansion's band end on the
    chimney's share each flue takes, (1 − n·F₀/F₁)²."""
    e = dr.turn_up("t", "chimney", 0.1, 0.1, 0.5, 0.01, 0.25, 4)
    assert e.branches == 4
    assert e.k_lo == pytest.approx((1 - 0.04 / 0.25) ** 2)


# --- parallel branches ---------------------------------------------------------------------------


def _intake(name: str, area: float, k: float) -> dr.Element:
    return dr.Element(f"{dr.INTAKE}, {name}", "inlet", "room", area, k=k)


def _group(*branches: list[dr.Element]) -> dr.Element:
    return dr.Element("group", "parallel", "", parts=tuple(tuple(b) for b in branches))


def test_openings_in_parallel_pass_the_sum_of_a_over_root_k() -> None:
    """Two openings at one pressure drop, the stack's buoyancy: m_i = A_i·√(2ρ_a·Δp/K_i), so the
    air is √(2ρ_a·Δp)·Σ A_i/√K_i, split as each A_i/√K_i (the closed form `Intakes` uses)."""
    h, t = 3.0, 1200.0
    path = dr.Path((_group([_intake("a", 0.02, 0.5)], [_intake("b", 0.05, 2.0)]),
                    dr.column("stack", "chimney", h)), ROOM)  # fmt: skip
    rho_g = WOOD.props(t)[0]
    lift = (path.room_density - rho_g) * dr.G * h
    each = [a / math.sqrt(k) * math.sqrt(2 * path.room_density * lift)
            for a, k in ((0.02, 0.5), (0.05, 2.0))]  # fmt: skip
    d = dr.draw(path, {"chimney": t}, WOOD)
    assert d.air == pytest.approx(sum(each), rel=1e-7)
    assert d.shares[0][1] == pytest.approx(tuple(each), rel=1e-6)


def test_identical_branches_are_one_branch_of_their_count() -> None:
    rest = (dr.column("stack", "chimney", 3.0), dr.outlet("top", "chimney", 0.03))
    one = dr.Path((dr.Element("in", "inlet", "room", 0.02, 2, k=0.5), *rest), ROOM)
    two = dr.Path((_group([dr.inlet("a", 0.02)], [dr.inlet("b", 0.02)]), *rest), ROOM)
    t = {"chimney": 1300.0}
    assert dr.draw(two, t, WOOD).air == pytest.approx(dr.draw(one, t, WOOD).air, rel=1e-8)


def test_branches_of_different_buoyancy_share_one_junction() -> None:
    """Two stacks of different heights after one inlet: each m_i = ρ_g·A·√(2(B_i − D)/(K·ρ_g)),
    the junction's draft D the inlet's loss at their sum (solved here by hand, by bisection);
    a stack whose buoyancy is under D carries nothing."""
    a0, a, t = 0.02, 0.01, 1300.0

    def solve(h1: float, h2: float) -> tuple[float, list[float]]:
        path = dr.Path((dr.inlet("in", a0), _group(
            [dr.column("c1", "chimney", h1), dr.outlet("o1", "chimney", a)],
            [dr.column("c2", "chimney", h2), dr.outlet("o2", "chimney", a)])), ROOM)  # fmt: skip
        rho_a, rho_g = path.room_density, WOOD.props(t)[0]
        g_per_a = WOOD.mass / WOOD.air
        lifts = [(rho_a - rho_g) * dr.G * h for h in (h1, h2)]

        def flows(d: float) -> list[float]:  # each stack's gas, then as air
            return [rho_g * a * math.sqrt(max(b - d, 0.0) * 2 / (1.06 * rho_g)) / g_per_a
                    for b in lifts]  # fmt: skip

        def gap(d: float) -> float:
            m = sum(flows(d))
            return 0.5 * rho_a * (m / (rho_a * a0)) ** 2 / 2 - d

        d = find_root(gap, 0.0, max(lifts), xtol=1e-12)
        got = dr.draw(path, {"chimney": t}, WOOD)
        assert got.air == pytest.approx(sum(flows(d)), rel=1e-6)
        assert got.shares[0][1] == pytest.approx(tuple(flows(d)), rel=1e-5, abs=1e-12)
        return got.air, list(got.shares[0][1])

    _, both = solve(4.0, 2.0)
    assert both[0] > both[1] > 0
    _, one = solve(4.0, 0.01)
    assert one[1] == 0.0


def test_a_branch_with_no_loss_holds_the_junction() -> None:
    """An opening left out for want of its size (an empty branch) holds the junction at its own
    buoyancy and takes what the others don't: here the room's, so the sized opening beside it
    carries nothing and the chimney draws as it would alone."""
    alone = dr.Path((dr.column("stack", "chimney", 3.0), dr.outlet("top", "chimney", 0.02)), ROOM)
    beside = dr.Path((_group([], [_intake("a", 0.02, 0.5)]), *alone.elements), ROOM)
    t = {"chimney": 1300.0}
    got = dr.draw(beside, t, WOOD)
    assert got.air == pytest.approx(dr.draw(alone, t, WOOD).air, rel=1e-9)
    assert got.shares[0][1][1] == 0.0
    empty = dr.balance(beside, 0.0, t, WOOD, lambda m: m)
    assert empty.shares[0][1] == (0.0, 0.0)


def test_a_free_branch_under_the_junction_carries_nothing() -> None:
    """A free branch whose buoyancy is under the draft the others need: it carries nothing and
    the others take it all."""
    path = dr.Path((dr.inlet("in", 0.005), _group(
        [dr.column("low", "chimney", 0.1)],
        [dr.column("c", "chimney", 4.0), dr.outlet("o", "chimney", 0.01)])), ROOM)  # fmt: skip
    got = dr.draw(path, {"chimney": 1300.0}, WOOD)
    low, high = got.shares[0][1]
    assert low == 0.0
    assert high == pytest.approx(got.air)


def test_zones_take_their_alias_then_their_kind() -> None:
    path = dr.Path((dr.column("s", "stack", 1.0),), ROOM, alias=(("stack", "chamber 3"),))
    assert dr.zone_temperature(path, "stack", {"chamber 3": 1000.0}) == 1000.0
    assert dr.zone_temperature(path, "stack", {"chamber": 900.0}) == 900.0
    assert dr.zone_temperature(path, "firebox left", {"firebox": 800.0}) == 800.0
    with pytest.raises(KeyError, match="stack"):
        dr.zone_temperature(path, "stack", {"firebox": 800.0})
    assert path.zones == ("stack",)


def test_a_band_of_lengths_and_the_intakes_through_branches() -> None:
    """A length band carries its most-air end's elements (`alt`) to `most`; the stoker's bricks
    reach intakes inside parallel branches and the band's other end too."""
    short = (_group([_intake("a", 0.02, 0.5)], [dr.inlet("b", 0.02)]),
             dr.column("stack", "chimney", 3.0), dr.outlet("top", "chimney", 0.02))  # fmt: skip
    tall = (short[0], dr.column("stack", "chimney", 4.0), short[2])
    path = dr.Path(short, ROOM, alt=tall)
    assert path.most().elements == tall
    assert path.most().alt is None
    t = {"chimney": 1300.0}
    assert dr.draw(path.most(), t, WOOD).air > dr.draw(path, t, WOOD).air
    half = path.opened(0.5)
    a = half.elements[0].parts[0][0]
    assert a.k == pytest.approx(2.0)
    assert half.elements[0].parts[1][0].k == pytest.approx(0.5)  # not an intake
    assert half.alt is not None
    assert half.alt[0].parts[0][0].k == pytest.approx(2.0)
    tab = dr.table(dr.Path(short, ROOM, alias=(("chimney", "chamber"),)), WOOD)
    assert tab.at(1573.15) > 0


# --- the forms, against paths written out by hand ------------------------------------------------


def _same(built: dr.Path, hand: dr.Path, t: float = HOT) -> None:
    """The built path draws what the hand-written one does, at both ends of its band."""
    temps = _hot(built, t)
    assert dr.draw(built, temps, WOOD).air == pytest.approx(dr.draw(hand, temps, WOOD).air,
                                                            rel=1e-9)  # fmt: skip
    assert dr.draw(built.most(), temps, WOOD).air == pytest.approx(
        dr.draw(hand.most(), temps, WOOD).air, rel=1e-9
    )


def _bernoulli(rise: float, flues: list[tuple[float, float, bool]], t: float = HOT) -> float:
    """An independent estimate of the air (kg/s): the buoyancy of a column ``rise`` tall at the
    gas's ``t`` against each flue's velocity heads alone, (area m², K, the room's air or the gas),
    no friction: Δp = m²·Σ K/(2ρ·A²), with the gas the air × products ÷ air."""
    rho_a = ROOM_RHO
    rho_g = WOOD.props(t)[0]
    r = WOOD.mass / WOOD.air
    lift = (rho_a - rho_g) * dr.G * rise
    per = sum(k / (2 * rho_a * a * a) if cold else k * r * r / (2 * rho_g * a * a)
              for a, k, cold in flues)  # fmt: skip
    return math.sqrt(lift / per)


ROOM_RHO = dr.Path((), ROOM).room_density


def test_an_updraft_kit_whose_chamber_is_its_stack() -> None:
    """The Olsen 16 kit (p.173): eight 2½ in ports up through its 4½ in floor, the chamber's
    column to the 9 × 4½ in flue in its crown (43.7 + 4.37 in), up through the 4½ in arch and out
    to the room: no chimney (p.80). Written out by hand from its design file."""
    k = load_design(OLSEN / "olsen-kit-16.yaml")
    built = dr.kiln_path(k)
    pa_ = math.pi * (1.25 * IN) ** 2
    hand = dr.Path((
        dr.inlet("ports", pa_, 8),
        dr.duct("ports", "room", 2.5 * IN, 2.5 * IN, 4.5 * IN, 8, rnd=True),
        dr.outlet("ports", "room", pa_, 8),
        dr.column("chamber", "chamber", (43.7 + 4.37) * IN),
        dr.entrance("exit", "chamber", 40.5 * IN**2),
        dr.duct("exit", "chamber", 9 * IN, 4.5 * IN, 4.5 * IN),
        dr.column("roof", "chamber", 4.5 * IN),
        dr.outlet("exit", "chamber", 40.5 * IN**2),
    ), ROOM)  # fmt: skip
    _same(built, hand)
    assert built.zones == ("chamber",)
    assert "updraft kilns have no chimneys" in (built.steps[0].note or "")
    # Bernoulli through the ports (cold) and the flue (hot), K 1.5 each: friction and 11-1's
    # 1.06 take a little off
    est = _bernoulli((43.7 + 4.37 + 4.5) * IN, [(8 * pa_, 1.5, True), (40.5 * IN**2, 1.5, False)])
    got = dr.draw(built, _hot(built), WOOD).air
    assert 0.85 * est < got < est


def _family(kid: str) -> float:
    k = load_design(ROOT / DATA[kid]["design"])
    path = dr.kiln_path(k, inputs=pi.inputs(kid))
    return dr.draw(path, _hot(path), WOOD).air


def test_each_familys_draft_against_a_bernoulli_estimate() -> None:
    """At 1300 °C, each family's draft against the buoyancy of its whole hot column over its main
    flues' velocity heads alone (K 1.5 a hole through a wall, 1.0 a turn or a top, 0.5 a mouth in
    the room's air; no friction, no Reynolds factor), from the book's sizes: a groundhog with a
    chimney (Meaders-Cheever, p.112), a climbing row (Kawaii, p.97), a downdraft through its floor
    (Singh, Fig 5-10), an updraft with no chimney (Miravet, Fig 6-19). Friction and Idelchik's
    finer coefficients take 0–20 % off."""
    from kilndesigner.run_parts import run_layout

    hole = 45 * IN**2
    cheever = _bernoulli(8 * FT, [(6 * hole, 1.5, False), (6 * hole, 1.0, False),
                                  (540 * IN**2, 1.0, False)])  # fmt: skip
    run = run_layout(load_design(OLSEN / "kawaii.yaml"))
    top = math.tan(math.radians(11.6)) * (run.length * 1e-3 + 18.5 * IN) + 68 * IN
    kawaii = _bernoulli(top, [(84 * 14 * IN**2, 0.5, True), *[(350 * IN**2, 1.5, False)] * 4,
                              (450 * IN**2, 1.5, False), (450 * IN**2, 1.0, False),
                              (450 * IN**2, 1.0, False)])  # fmt: skip
    singh = _bernoulli(30 * FT + 22.5 * IN, [(4236 * IN**2, 0.5, True), (1440 * IN**2, 1.5, False),
                                             (432 * IN**2, 1.5, False), (384 * IN**2, 1.0, False),
                                             (576 * IN**2, 1.0, False)])  # fmt: skip
    miravet = _bernoulli(126 * IN, [(486 * IN**2, 0.5, True), (1260 * IN**2, 1.5, False),
                                    (255 * IN**2, 1.5, False)])  # fmt: skip
    for kid, est in (("meaders-cheever", cheever), ("kawaii", kawaii), ("singh-coal", singh),
                     ("miravet", miravet)):  # fmt: skip
        assert 0.8 * est < _family(kid) < 1.05 * est, kid


def test_a_gas_updraft_with_no_flue_takes_p78s_to_the_kits_20_percent() -> None:
    """Updraft test kiln 4 (4 × 4 × 5 ft of stacking): no exit flue given, so p.78's inlet =
    exit, the 18 burner ports' area, to the kits' 20 % more (pp.173–174): the band's two ends in
    the crown, the larger at the most-air end."""
    built = dr.kiln_path(load_design(OLSEN / "updraft-test-4.yaml"))
    ports = 18 * math.pi * (1.25 * IN) ** 2
    els = {e.name: e for e in built.elements}
    assert els["exit flue, sharp entrance"].area == pytest.approx(ports)
    assert built.most().elements != built.elements
    most = {e.name: e for e in built.most().elements}
    assert most["exit flue, sharp entrance"].area == pytest.approx(1.2 * ports)
    assert "20 % less inlet than exit" in (built.steps[0].note or "")
    assert els["chamber, inlet to the exit flue's middle"].rise == pytest.approx(
        (60 + 7.13) * IN
    )  # the crown of the arch over the 57 in span


def test_a_wall_firebox_and_two_sets_of_roof_exits() -> None:
    """Miravet (Fig 6-19): its 8 ft cube firebox fired on its floor in front, its 35 floor flues
    of 6 × 6 in (the design's count and size, though the engine cuts them as one slot), the
    chamber's column to each set of exits in the dome (a 15 in main flue at the crown, four 5 in
    flues at the corners, lower on the sail dome), the two sets in parallel to the room."""
    k = load_design(OLSEN / "miravet.yaml")
    built = dr.kiln_path(k, inputs=pi.inputs("miravet"))
    els = {e.name: e for e in built.elements}
    flues = els["firebox's inlet flues, through the front wall"]
    assert flues.branches == 35
    assert flues.area == pytest.approx(36 * IN**2)
    assert els["firebox, the fire to its inlet flues' middle"].rise == pytest.approx(3 * IN)
    group = next(e for e in built.elements if e.kind == "parallel")
    crown, corners = group.parts
    # The sail dome over the 96 in square, 36 in rise: R = (2·48² + 36²)/72 = 82 in, its centre
    # 46 in under the 72 in springline; the corner flues 45.5 in each way from the middle
    assert crown[0].rise == pytest.approx((72 + 36) * IN)
    assert corners[0].rise == pytest.approx((72 - 46 + math.sqrt(82**2 - 2 * 45.5**2)) * IN)
    d = dr.draw(built, _hot(built), WOOD)
    main, side = d.shares[0][1]
    assert main + side == pytest.approx(d.air)
    a_main, a_side = math.pi * (7.5 * IN) ** 2, 4 * math.pi * (2.5 * IN) ** 2
    assert main / a_main > side / a_side  # the taller, wider flue draws more on its area
    assert "the dataset's" in (built.steps[0].note or "")


def test_a_climbing_row_in_series_through_its_walls() -> None:
    """Kawaii's four chambers (p.97): the dogi's five 7 × 10 in flues into chamber 1, five 7 × 10
    in flues through each 18 in wall between (8-4), each chamber's climb a column of its step
    (run_parts' floors), five 9 × 10 in exits into a chimney no source sizes: p.78's section (the
    exits' 450 in²) and the climbing kiln's band, its chamber-top line (p.81) to 3 × its rise
    (p.101)."""
    from kilndesigner.run_parts import run_layout

    k = load_design(OLSEN / "kawaii.yaml")
    run = run_layout(k)
    built = dr.kiln_path(k)
    cols = {e.zone: e.rise for e in built.elements if e.kind == "column"}
    step = run.floor(1) * 1e-3
    for c in (1, 2, 3):
        assert cols[f"chamber {c}"] == pytest.approx(step, rel=1e-9)  # a flue row to the next
    assert "chamber 4" not in cols  # its inlet and its exits both 5 in over its floor
    walls = [e for e in built.elements if "(Idelchik 8-4)" in e.name and e.kind == "fitting"]
    assert len(walls) == 3
    f = 5 * 7 * 10 / (84 * 44)
    tau = dr.grid_tau(run.between * 1e-3 / dr.hydraulic(7 * IN, 10 * IN))
    assert walls[0].k == pytest.approx((0.5 + tau * math.sqrt(1 - f)) * (1 - f) + (1 - f) ** 2)
    stack = next(e for e in built.elements if e.name == "chimney" and e.kind == "duct")
    assert stack.area == pytest.approx(450 * IN**2)
    rise = math.tan(math.radians(11.6)) * (run.length * 1e-3 + 9.5 * IN + 9 * IN)
    base = run.floor(3) * 1e-3 + 5 * IN
    least = cols["stack"]
    most = next(e.rise for e in built.most().elements if e.kind == "column" and e.zone == "stack")
    assert least + base == pytest.approx(rise + (44 + 24) * IN, rel=1e-9)
    assert most + base == pytest.approx(3 * rise, rel=1e-9)
    assert "Principle 8" in (built.steps[0].note or "")


def test_a_downdraft_through_its_floor_and_a_long_connection() -> None:
    """Singh's coal kiln (Fig 5-10): four fireboxes on the diagonals (two zones, front and back,
    as the heat model names them), twelve 6 × 6 in floor holes into the channels, the 24 × 16 in
    connection 27½ ft to the 24 × 24 in chimney, 30 ft. The connection's run is the holes' mean
    distance to the flue wall, the wall and the run."""
    k = load_design(OLSEN / "singh-coal.yaml")
    built = dr.kiln_path(k, inputs=pi.inputs("singh-coal"))
    els = {e.name: e for e in built.elements}
    assert els["exit flues, through the floor"].branches == 12
    conn = els["the channels and connection to the chimney"]
    wall = sum(x.thickness.to("m").magnitude for x in k.lining.for_face("back"))
    assert conn.length == pytest.approx(42 * IN + wall + 27.5 * FT, rel=1e-9)
    assert conn.area == pytest.approx(24 * 16 * IN**2)
    assert set(built.zones) == {"firebox front", "firebox back", "chamber", "stack"}
    group = next(e for e in built.elements if e.kind == "parallel")
    assert len(group.parts) == 4  # one firebox on each diagonal
    assert all(b[0].branches == 1 for b in group.parts)
    chimney = next(e for e in built.elements if e.name == "chimney" and e.kind == "column")
    assert chimney.rise == pytest.approx(30 * FT + sum(
        x.thickness.to("m").magnitude for x in k.lining.for_face("floor")) + 8 * IN)  # fmt: skip


def test_a_row_fired_in_stages_takes_its_side_holes() -> None:
    """Fujiwara's kedo stoked from its side (the design's 5 in takiguchi, 10 in up): the hole an
    inlet beside the front's path, joined in that chamber. With the 3½ × 2 ft fire mouth wide
    open the chamber is hardly under suction, the 10 in round entry into the chimney (p.101) the
    path's narrowest, so the hole, 10 in up, stands at the neutral plane and draws nothing; the
    front closed, the hole alone draws the chimney's air."""
    k = load_design(OLSEN / "fujiwara-bizen.yaml")
    staged = dr.kiln_path(k, inputs=pi.inputs("fujiwara-bizen", stage=1))
    group = next(e for e in staged.elements if e.kind == "parallel")
    assert group.name == "chamber 2's side stoke holes beside the front's path"
    side = group.parts[1]
    assert side[0].name.startswith(dr.INTAKE)
    assert side[0].area == pytest.approx(math.pi * (2.5 * IN) ** 2)
    d = dr.draw(staged, _hot(staged), WOOD)
    front, hole = d.shares[0][1]
    assert front == pytest.approx(d.air)
    assert hole == 0.0
    alone = dr.kiln_path(k, inputs=pi.inputs("fujiwara-bizen", stage=1, front_open=False))
    assert alone.zones[0] == "chamber 2"
    assert "the front's intakes closed for the stage" in (alone.steps[0].note or "")
    through = dr.draw(alone, _hot(alone), WOOD).air
    assert 0 < through < d.air
    assert dr.draw(alone.opened(0.5), _hot(alone), WOOD).air < through  # the stoker's bricks
    with pytest.raises(dr.NotModelledError, match="no chamber 3"):
        dr.kiln_path(k, inputs=pi.inputs("fujiwara-bizen", stage=2))


def test_a_side_hole_above_the_neutral_plane_draws_nothing() -> None:
    """Tamba as its design lays it (level, p.85's slope unprinted), its exits the end chamber's
    holes and no stack (p.88): its side holes 32 in up stand where the hot column below them
    works against them, so stoking chamber 3 the front's path carries the air and they none (no
    flow backwards counted, said in the draft's docstring)."""
    k = load_design(OLSEN / "tamba.yaml")
    staged = dr.kiln_path(k, inputs=pi.inputs("tamba", stage=2))
    assert "stack" not in staged.zones
    assert "no stack" in (staged.steps[0].note or "")
    d = dr.draw(staged, _hot(staged), WOOD)
    assert d.shares[0][1][1] == 0.0


def test_one_firebox_to_a_chamber_as_the_book_draws_them() -> None:
    """Suzuki's seven fireboxes (p.93) one to each chamber, the book's himae (the owner's
    question 3), not side by side at the front as the engine lays them: the fire in chamber 1's
    own zone, its side holes not sized (left out, said: the air an upper bound)."""
    k = load_design(OLSEN / "suzuki-kyoto.yaml")
    book = dr.kiln_path(k, inputs=pi.inputs("suzuki-kyoto"))
    assert book.zones[0] == "chamber 1"
    assert "question 3" in (book.steps[0].note or "")
    assert book.left_out == ("chamber 1's side stoke holes (not sized)",)
    engine = dr.kiln_path(k, inputs=pi.inputs("suzuki-kyoto", one_per_chamber=False))
    assert engine.zones[0] == "firebox"
    tab = dr.table(book, WOOD)
    assert "an upper bound, too" in (tab.steps[-1].note or "")


def test_a_chimney_through_the_crown_and_a_tapered_one() -> None:
    """Kähler's (Figs 5-17, 5-18): three floor flues, the chimney through the crown from the
    channels to 10–12 ft (printed, the band); Bowen Mountain's 13½ in chimney tapering to 9 in
    from the kiln's top (p.127, p.80), its friction in slices, its top's exit on the 9 × 9 in."""
    kahler = dr.kiln_path(load_design(OLSEN / "kahler-salt.yaml"), inputs=pi.inputs("kahler-salt"))
    assert "through the crown" in (kahler.steps[0].note or "")
    assert "10.0–12.0 ft" in (kahler.steps[0].note or "")
    tall = next(e.rise for e in kahler.most().elements if e.name == "chimney")
    short = next(e.rise for e in kahler.elements if e.name == "chimney")
    assert tall - short == pytest.approx(2 * FT)
    bowen = dr.kiln_path(load_design(OLSEN / "bowen-mountain.yaml"),
                         inputs=pi.inputs("bowen-mountain"))  # fmt: skip
    slices = [e for e in bowen.elements if e.name.startswith("chimney, tapering")]
    assert len(slices) == pa.TAPER_STEPS
    assert slices[0].area > slices[-1].area > 81 * IN**2
    top = next(e for e in bowen.elements if e.name == "chimney top")
    assert top.area == pytest.approx(81 * IN**2)


def test_p78_carries_the_inlets_to_the_exit_and_the_chimney() -> None:
    """Bidai (Figs 4-36, 8-7): six 4½ × 9 in inlet flues, 243 in²; its exit flue 12 in tall,
    width and count not printed: one, 243 ÷ 12 = 20.25 in wide (p.78); its chimney's section not
    printed either: 243 in², square (p.78)."""
    built = dr.kiln_path(load_design(OLSEN / "bidai.yaml"), inputs=pi.inputs("bidai"))
    els = {e.name: e for e in built.elements}
    exit_ = els["exit flues, through the flue wall"]
    assert exit_.sides == pytest.approx((20.25 * IN, 12 * IN))
    assert els["chimney"].area == pytest.approx(243 * IN**2)
    assert "p.78" in (built.steps[0].note or "")


def test_the_height_band_by_rule_5_and_fig_5_2() -> None:
    """Hollyweird's chimney (15 × 24 in, p.116), its height not printed: twice the downward pull
    (35.4 + 12.6 in, p.130) to Rule 5, 3 × that + ⅓ × the horizontal pull (the two chambers, the
    wall between, the flue wall and the 9 in run, p.80)."""
    from kilndesigner.run_parts import run_layout

    k = load_design(OLSEN / "hollyweird.yaml")
    built = dr.kiln_path(k, inputs=pi.inputs("hollyweird"))
    run = run_layout(k)
    down = (35.4 + 12.6) * IN
    wall = sum(x.thickness.to("m").magnitude for x in k.lining.for_face("back"))
    across = run.length * 1e-3 + wall + 9 * IN
    col = next(e for e in built.elements if e.name == "chimney" and e.kind == "column")
    most = next(e for e in built.most().elements if e.name == "chimney" and e.kind == "column")
    base = 2 * down - col.rise
    assert most.rise + base == pytest.approx(3 * down + across / 3, rel=1e-9)
    stack = next(e for e in built.elements if e.name == "chimney" and e.kind == "duct")
    assert stack.sides == pytest.approx((15 * IN, 24 * IN))
    assert "Rule 5" in (built.steps[0].note or "")


def test_several_identical_chimneys_and_the_floor_holes_by_p78() -> None:
    """Bae's two exits into two chimneys (Fig 4-67), the flow shared; Breda's floor holes, 4½ in
    square (p.167), as many as p.78 takes on its 29 exits' 652½ in²: 32."""
    bae = dr.kiln_path(load_design(OLSEN / "bae-gilgama.yaml"), inputs=pi.inputs("bae-gilgama"))
    top = next(e for e in bae.elements if e.name == "chimney top")
    assert top.branches == 2
    assert "2 chimneys side by side" in (bae.steps[0].note or "")
    breda = dr.kiln_path(load_design(OLSEN / "breda-bottle.yaml"), inputs=pi.inputs("breda-bottle"))
    holes = next(e for e in breda.elements if e.name == "the floor's holes, through the floor")
    assert holes.branches == 32
    assert "stack" in breda.zones  # the bottle, its gas the chamber's
    assert breda.alias == (("stack", "chamber"),)


def test_a_tube_cut_into_segments() -> None:
    """Bae's sloped tube (11.3°) cut into three zones along its length: the gas taken across each
    cut at the tube's mid-height, each segment its own climb, the columns summing to the
    inlet-to-exit climb; the middle one the slope's rise over its third of the run."""
    k = load_design(OLSEN / "bae-gilgama.yaml")
    whole = dr.kiln_path(k)
    cut = dr.kiln_path(k, segments=3)
    assert cut.zones == ("firebox", "chamber 1", "chamber 2", "chamber 3", "stack")
    rise = sum(e.rise for e in whole.elements if e.kind == "column" and e.zone == "chamber")
    cols = [e for e in cut.elements if e.kind == "column" and e.zone.startswith("cham")]
    assert sum(e.rise for e in cols) == pytest.approx(rise)
    middle = sum(e.rise for e in cols if e.zone == "chamber 2")
    assert middle == pytest.approx(6 * FT / 3 * math.sin(math.radians(11.3)))
    assert "mid-height" in (cut.steps[0].note or "")
    temps = {"firebox": 1500.0, "chamber 1": 1400.0, "chamber 2": 1300.0, "chamber 3": 1200.0,
             "stack": 1000.0}  # fmt: skip
    assert dr.draw(cut, temps, WOOD).air > 0
    level = dr.kiln_path(load_design(OLSEN / "fast-fire.yaml"), segments=3)
    assert "chamber 2" not in level.zones  # a level tube's middle third has no climb


def test_the_design_alone_and_its_variations() -> None:
    """The forms on the design files with nothing from the dataset, and on changed ones: a mouth
    the only intake, a firebox set's own intakes and its grate's bars, fireboxes the engine lays
    past the chamber, a chimney the design leaves out (its band counting the fireboxes under the
    floor, p.140), several of one size, a flat, open or catenary roof over an updraft, exits at
    two heights in one set, a connection with no run."""
    moveros = dr.kiln_path(load_design(OLSEN / "moveros-umbrella.yaml"))
    assert moveros.elements[0].name == "the firebox's mouth (its stoke hole)"
    assert moveros.elements[0].area == pytest.approx(22 * 27 * IN**2)
    church = dr.kiln_path(load_design(OLSEN / "church-skaelskor.yaml"), inputs=pi.inputs(
        "church-skaelskor", intake=(dr.Intakes((0.1, 0.1)),), grate_bar=0.75 * IN))  # fmt: skip
    group = church.elements[0]
    assert group.parts[0][0].name.startswith(dr.INTAKE)
    assert "the design's ash-pit mouth and stoke hole" in (church.steps[0].note or "")
    assert group.parts[0][0].k > dr.intakes(dr.Intakes((0.1, 0.1)), 0.0, None, 1).k  # the bars
    hotch = dr.kiln_path(load_design(OLSEN / "hotchkiss-raw-clay.yaml"),
                         inputs=pi.inputs("hotchkiss-raw-clay", one_per_chamber=False))  # fmt: skip
    assert "stand past the chamber's width" in (hotch.steps[0].note or "")
    bare = dr.kiln_path(_kiln("fast-fire", {"draft.chimney": None}), grate_bar=0.75 * IN)
    col = next(e for e in bare.elements if e.name == "chimney" and e.kind == "column")
    down = (36 + 3.375 + 6 + 6.5) * IN  # the chamber to its crown, the fireboxes and ash pits
    assert col.rise + 3.75 * IN == pytest.approx(2 * down)
    two = dr.kiln_path(load_design(OLSEN / "kawaii.yaml"),
                       inputs=pa.Inputs(stack=pa.Stack(count=2)))  # fmt: skip
    assert "2 chimneys side by side" in (two.steps[0].note or "")
    for roof, top in (({"type": "flat"}, 43.7), ({"type": "catenary_arch"}, 43.7)):
        kit = dr.kiln_path(_kiln("olsen-kit-16", {"roof": roof}))
        els = {e.name: e for e in kit.elements}
        assert els["chamber, inlet to the exit flue's middle"].rise == pytest.approx(top * IN)
    opened = dr.kiln_path(_kiln("miravet", {"roof": {"type": "open"}, "draft.exits": None}))
    assert opened.elements[-1].area == pytest.approx((96 * IN) ** 2)
    kenzan = dr.kiln_path(load_design(OLSEN / "kenzan-muffle.yaml"),
                          inputs=pi.inputs("kenzan-muffle"))  # fmt: skip
    top = kenzan.elements[-1]  # the annulus round the muffle (p.165), π/4·(22² − 18² … 16²) in²
    assert top.area == pytest.approx(math.pi / 4 * (22**2 - 18**2) * IN**2, rel=5e-3)
    assert kenzan.most().elements[-1].area == pytest.approx(
        math.pi / 4 * (22**2 - 16**2) * IN**2, rel=5e-3
    )
    places = [{"across": "0 in", "along": "0 in"}, {"across": "40 in", "along": "40 in"}]
    mixed = _kiln("miravet", {"draft.exits": [{"through": "roof", "port": {"diameter": "6 in"},
                                               "places": places}]})  # fmt: skip
    assert "at their mean height" in (dr.kiln_path(mixed).steps[0].note or "")
    flush = _kiln("fujiwara-bizen", {"draft.run_to_chimney": "0 in"})
    names = [e.name for e in dr.kiln_path(flush).elements]
    assert "exit flues into the connection" in names
    assert "the connection to the chimney" not in names
    kato = dr.kiln_path(load_design(OLSEN / "kato-coal.yaml"), inputs=pi.inputs("kato-coal"))
    conn = next(e for e in kato.elements if e.name == "the channels and connection to the chimney")
    assert conn.sides == pytest.approx((20 * IN, 18 * IN))
    assert kato.left_out == ()
    tab = dr.table(kato, WOOD, zones=("firebox", "chamber", "chimney", *kato.zones))
    assert tab.at(1573.15) > 0


def test_inputs_that_cant_be_bands_or_flues() -> None:
    with pytest.raises(ValueError, match="least to its most"):
        pa.Band(0.2, 0.1, "")
    with pytest.raises(ValueError, match="its width, its height or its area"):
        pa.Flues()


@pytest.mark.parametrize(
    ("name", "change", "inputs", "words"),
    [
        ("bowen-mountain", {"heat.gas.burners.count": 20}, None, "burner ports aren't laid out"),
        ("kawaii", {"chamber.slope": "59 degree"}, None, "no flues through the wall after"),
        ("moveros-umbrella", {}, pa.Inputs(stack=pa.Stack(
            height=pa.Band(3.0, 3.0, "a test"), width=pa.Band(0.2, 0.2, "a test"),
            depth=pa.Band(0.2, 0.2, "a test"))), "an open top under a chimney"),
    ],
)  # fmt: skip
def test_forms_the_book_doesnt_draw_are_refused(
    name: str, change: dict[str, Any], inputs: pa.Inputs | None, words: str
) -> None:
    with pytest.raises(dr.NotModelledError, match=words):
        dr.kiln_path(_kiln(name, change), inputs=inputs)


@pytest.mark.parametrize(
    ("name", "change", "segments", "words"),
    [
        ("electric-car-45", {}, 1, "electric"),
        ("fast-fire", {}, 0, "one segment or more"),
        ("kawaii", {}, 2, "segments cut a single box chamber"),
        ("olsen-crossdraft-36", {}, 1, "port size"),
        ("anagama-hole", {}, 1, "p.78"),
        ("chappell-domura", {}, 1, "no way into the chamber"),
    ],
)
def test_paths_that_cant_be_bounded_are_refused(
    name: str, change: dict[str, Any], segments: int, words: str
) -> None:
    with pytest.raises(dr.NotModelledError, match=words):
        dr.kiln_path(_kiln(name, change), segments=segments)


# --- every reference kiln ------------------------------------------------------------------------

DATA = yaml.safe_load((ROOT / "core" / "tests" / "v2" / "reference_kilns.yaml").read_text(
    encoding="utf-8"))["kilns"]  # fmt: skip
# What each refused kiln lacks (C1's report, `11-10-26.md`): nothing on its gas path is sized, so
# p.78 has nothing to carry, or its burners' ports aren't given; the electric kiln needs no path
REFUSED = {
    "anagama-hole": "the exit flues: not given",
    "electric-car-45": "electric kiln",
    "falcone-pompeii": "the exit flues: not given",
    "fireworks-edmonton": "the exit flues: not given",
    "kannofen": "the exit flues: not given",
    "kitade-tojilo": "the exit flues: not given",
    "la-borne": "the exit flues: not given",
    "olsen-crossdraft-36": "port size",
    "olsen-three-chamber": "port size",
}


@pytest.mark.parametrize("kid", sorted(DATA))
def test_every_reference_kiln_has_its_path_or_says_what_it_lacks(kid: str) -> None:
    """Each of the 53 on its dataset inputs: a path drawing air at 1300 °C, its band's most-air
    end at least its least, every zone it names given a temperature by the heat model's names;
    or refused, naming the missing input."""
    k = load_design(ROOT / DATA[kid]["design"])
    if kid in REFUSED:
        with pytest.raises(dr.NotModelledError, match=REFUSED[kid]):
            dr.kiln_path(k, inputs=pi.inputs(kid))
        return
    path = dr.kiln_path(k, inputs=pi.inputs(kid))
    temps = _hot(path)
    least = dr.draw(path, temps, WOOD).air
    most = dr.draw(path.most(), temps, WOOD).air
    assert 0.01 < least <= most * (1 + 1e-9) < 10.0
    one_zone = {"firebox": HOT, "chamber": HOT, "chimney": HOT}  # a one-zone model's, zone.py's
    assert all(dr.zone_temperature(path, z, one_zone) == HOT for z in path.zones)
    assert path.steps[0].name == "The gas path"
