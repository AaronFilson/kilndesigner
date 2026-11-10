"""v2's draft (`heat/draft.py`): the pressure balance round the gas path, against a closed form,
the survey's probe of the fast-fire (`scratch/toolsets/gas-path/gas_path.py`) on its own inputs,
and the paths built from the design files."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pytest
import yaml
from fluids.filters import round_edge_grill  # pyright: ignore[reportMissingTypeStubs]
from fluids.fittings import (  # pyright: ignore[reportMissingTypeStubs]
    bend_miter,
    contraction_sharp,
    diffuser_sharp,
)

from kilndesigner.designfile import load_design
from kilndesigner.model import Kiln
from kilndesigner.v2.heat import draft as dr
from kilndesigner.v2.heat import gas

ROOT = Path(__file__).resolve().parents[3]
OLSEN = ROOT / "examples" / "olsen"
IN, FT = 0.0254, 0.3048
ROOM = (70 - 32) / 1.8 + 273.15
WOOD = gas.products(gas.wood(0.12, 19e6), 1.0, ROOM)


def test_a_chimney_alone_draws_bernoullis_flow() -> None:
    """A hot column H tall that only loses its velocity head at the top:
    (ρ_a − ρ_g)·g·H = K·ρ_g·v²/2, so m_gas = ρ_g·A·√(2(ρ_a − ρ_g)gH/(K·ρ_g)), K 1.0 at the
    band's most-air end (a uniform jet) and 1.06 at its least (Idelchik 11-1)."""
    h, a, t = 4.0, 0.05, 1200.0
    path = dr.Path((dr.column("stack", "chimney", h), dr.outlet("top", "chimney", a)), ROOM)
    rho_g = WOOD.props(t)[0]
    want = rho_g * a * math.sqrt(2 * (path.room_density - rho_g) * dr.G * h / rho_g)
    d = dr.draw(path.most(), {"chimney": t}, WOOD)
    assert d.gas == pytest.approx(want, rel=1e-8)
    assert d.air == pytest.approx(want * WOOD.air / WOOD.mass, rel=1e-8)
    least = dr.draw(path, {"chimney": t}, WOOD)
    assert least.gas == pytest.approx(want / math.sqrt(1.06), rel=1e-8)
    fixed = dr.draw(path.most(), {"chimney": t}, WOOD, fuel=0.001)
    assert fixed.gas == pytest.approx(want, rel=1e-8)
    assert fixed.air == pytest.approx(want - 0.001, rel=1e-8)


def test_no_buoyancy_no_flow() -> None:
    path = dr.Path((dr.column("down", "chimney", -1.0), dr.outlet("top", "chimney", 0.05)), ROOM)
    assert dr.draw(path, {"chimney": 1200.0}, WOOD).air == 0.0


def test_the_pressure_balance_as_a_row() -> None:
    """The DAE's row for the draft's air at max fire: zero at the air the path draws, buoyancy
    above it, and a flow pushed backwards is pushed back."""
    path = dr.Path((dr.column("stack", "chimney", 4.0), dr.outlet("top", "chimney", 0.05)), ROOM)
    temps = {"chimney": 1200.0}
    air = dr.draw(path, temps, WOOD).air
    assert dr.pressure(path, air, temps, WOOD) == pytest.approx(0.0, abs=1e-6)
    assert dr.pressure(path, 0.0, temps, WOOD) > 0
    assert dr.pressure(path, -air, temps, WOOD) > dr.pressure(path, 0.0, temps, WOOD)
    burners = dr.draw(path, temps, WOOD, fuel=0.001).air
    assert dr.pressure(path, burners, temps, WOOD, 0.001) == pytest.approx(0.0, abs=1e-6)


def _eq(area: float) -> float:
    return math.sqrt(4 * area / math.pi)


def _probe_duct(name: str, zone: str, w: float, h: float, length: float, n: int = 1) -> dr.Element:
    """The probe's friction: a round pipe's on D_h (k₁ 1), as fluids gives it."""
    return dr.Element(name, "duct", zone, w * h, n, length=length, dh=dr.hydraulic(w, h))


def _probe_path() -> dr.Path:
    """gas_path.py's fast-fire path, element for element, on its own fittings (fluids' round-pipe
    forms: Blevins' grill, Rennels' contraction and expansion, a mitre) and inputs (the chimney's
    14 ft from the firebox top, a 12 in firebox run, ¾ in round bars at 1½ in, 1 mm roughness):
    the solver against the survey's probe, not the fittings the engine now takes."""
    a_fb, a_in, a_ex, a_ch = 13.5 * 6 * IN**2, 13.5 * 4.5 * IN**2, 9 * 7.5 * IN**2, 81 * IN**2
    z_exit, z_top = 20.75 * IN, 12.5 * IN + 14 * FT
    into = float(contraction_sharp(_eq(a_fb), _eq(a_in))) + float(bend_miter(90))
    up = float(bend_miter(90)) + float(diffuser_sharp(_eq(a_ex), _eq(a_ch)))
    els = (
        dr.Element("ash pit", "inlet", "room", 13.5 * 6.5 * IN**2, 2, k=0.5),
        dr.Element("grate", "grate", "room", 12 * 24 * IN**2, 2, k=float(round_edge_grill(0.5))),
        dr.column("firebox", "firebox", 10.5 * IN),
        _probe_duct("firebox run", "firebox", 13.5 * IN, 6 * IN, 12 * IN, 2),
        dr.Element("into the inlet", "fitting", "firebox", a_in, 2, k=into),
        _probe_duct("inlet", "firebox", 13.5 * IN, 4.5 * IN, 4.5 * IN, 2),
        dr.Element("inlet out", "fitting", "firebox", a_in, 2, k=1.0),
        dr.column("chamber", "chamber", 3.75 * IN),
        dr.Element("exit in", "fitting", "chamber", a_ex, k=0.5),
        _probe_duct("exit", "chamber", 9 * IN, 7.5 * IN, 4.5 * IN),
        dr.Element("turn up", "fitting", "chimney", a_ex, k=up),
        dr.column("chimney", "chimney", z_top - z_exit),
        _probe_duct("chimney", "chimney", 9 * IN, 9 * IN, z_top - z_exit),
        dr.Element("top", "fitting", "chimney", a_ch, k=1.0),
    )
    return dr.Path(els, 21.1 + 273.15, rough=1e-3)


# gas_path.py at λ 1, adiabatic chimney, firebox at T + 50 K (scratch/v2-heat/probe_draft.py)
PROBE = {350.0: 0.076094, 600.0: 0.105947, 1000.0: 0.096880, 1600.0: 0.082203}
# The fast-fire's own path at 1300 °C, Idelchik's fittings at the band's least-air end (kg/s; was
# 0.0820 on fluids' round-pipe fittings)
DRAWN_1300 = 0.0788


@pytest.mark.parametrize("t", sorted(PROBE))
def test_the_surveys_fast_fire_probe_on_its_own_inputs(t: float) -> None:
    d = dr.draw(_probe_path(), {"firebox": t + 50, "chamber": t, "chimney": t}, WOOD)
    assert d.air == pytest.approx(PROBE[t], rel=2e-3)


# --- Idelchik's fittings (fittings-and-kiln-convection.md [D1], its Derived checks) -------------


def test_the_bar_grating_against_the_files_derived_values() -> None:
    """8-9 for ¾ in round bars at 1½ in: case (a) 1.73 × 1.00 = 1.73; case (b) with 8-4's τ 0.97
    at l/d_h 0.5, ζ′ 3.41, × β₂ 0.74 = 2.5: 3–4 × Blevins' 0.6, as the file says."""
    lo, hi = dr.bar_grate(0.75 * IN, 0.75 * IN)
    assert lo == pytest.approx(1.73)
    assert hi == pytest.approx(0.74 * 3.41, rel=2e-3)
    assert dr.grid_tau(0.5) == pytest.approx(0.97)
    assert dr.grid_tau(1.0) == pytest.approx(0.24)
    g = dr.grate("g", 12 * IN, 24 * IN, 0.75 * IN, 0.75 * IN)
    assert (g.coefficient(False), g.coefficient(True)) == (hi, lo)
    assert g.area == pytest.approx(12 * 24 * IN**2)


@pytest.mark.parametrize(
    ("b1_b0", "a0_b0", "zeta"),
    [(1.0, 1.0, 1.15), (0.8, 0.25, 1.43), (2.0, 1e9, 0.55), (1.2, 4.0, 0.81), (0.6, 1.0, 1.70),
     (0.7, 1.0, (1.70 + 1.36) / 2), (2.5, 1.0, 0.84), (0.4, 0.1, 1.76)],
)  # fmt: skip
def test_the_sharp_elbows_table(b1_b0: float, a0_b0: float, zeta: float) -> None:
    """6-6's grid, bilinear between its points, held at its edges."""
    assert dr.elbow(b1_b0, a0_b0) == pytest.approx(zeta)


def test_the_elbows_reynolds_factor() -> None:
    """6-7's k_Re = 45·λ_Re: 1.54 at Re 8,300, 1.21 at 19,900, 1.0 from 4·10⁴ (the file's
    Derived); held at its 3·10³ value, 2.11, below."""
    assert dr.k_re(8_300) == pytest.approx(1.54, abs=0.01)
    assert dr.k_re(19_900) == pytest.approx(1.21, abs=0.01)
    assert dr.k_re(4e4) == 1.0
    assert dr.k_re(500) == dr.k_re(3e3) == pytest.approx(2.11, abs=0.01)


def test_laminar_friction_in_a_rectangle() -> None:
    """Diagram 2-1: λ = k₁·64/Re, k₁ 0.89 for a square, 1.50 for a slot; Colebrook above 2000."""
    assert dr.laminar_k1(1.0, 1.0) == pytest.approx(0.89)
    assert dr.laminar_k1(1.0, 1e-6) == pytest.approx(1.50, abs=1e-4)
    assert dr.darcy(1000, 0.0, 0.89) == pytest.approx(0.89 * 0.064)
    assert dr.darcy(1e5, 0.0) == pytest.approx(0.018, abs=1e-3)
    assert dr.duct("d", "chimney", 0.2, 0.1, 1.0).sides == (0.2, 0.1)


def test_a_flue_into_a_much_deeper_chimney_is_a_band() -> None:
    """Idelchik's own stack example takes the sudden expansion alone; 6-6 stops at b₁/b₀ 2: past
    it the two are the band's ends, the expansion without 6-7's Reynolds factor."""
    flue, stack = 0.1 * 0.1, 0.4 * 0.4
    e = dr.turn_up("t", "chimney", 0.1, 0.1, 0.4, flue, stack)
    assert e.k == pytest.approx(dr.elbow(2.0, 1.0))
    assert e.k_lo == pytest.approx((1 - flue / stack) ** 2)
    assert e.by_re(False)
    assert not e.by_re(True)
    near = dr.turn_up("t", "chimney", 0.1, 0.1, 0.15, flue, 0.1 * 0.15)
    assert near.k_lo is None
    assert near.by_re(True)
    temps = {"chimney": 1200.0}
    path = dr.Path((dr.column("stack", "chimney", 4.0), e, dr.outlet("top", "chimney", stack)),
                   ROOM)  # fmt: skip
    assert dr.draw(path.most(), temps, WOOD).air > dr.draw(path, temps, WOOD).air
    assert path.most().rough == 0.0
    assert dr.outlet("o", "chimney", 1.0).coefficient(True) == 1.0


def _design(name: str, change: dict[str, Any] | None = None) -> Kiln:
    data = yaml.safe_load((OLSEN / f"{name}.yaml").read_text(encoding="utf-8"))
    for key, value in (change or {}).items():
        node = data
        *parents, last = key.split(".")
        for p in parents:
            node = node.setdefault(p, {})
        node[last] = value
    return Kiln.model_validate(data)


def test_the_fast_fires_own_path_and_draft_table() -> None:
    """From the design file: two under-floor fireboxes, the 9 × 7½ in flue, the 14 ft chimney of
    9 × 9 in. The table rises to its most near 600 K and falls as the gas thins, as the probe's
    did (0.076 → 0.106 → 0.082 kg/s), here a little more for a chimney 4½ in taller."""
    path = dr.kiln_path(load_design(OLSEN / "fast-fire.yaml"), grate_bar=0.75 * IN)
    names = [e.name for e in path.elements]
    assert names[0].startswith("ash-pit mouth")
    assert "grate, round bars (Idelchik 8-9)" in names
    assert names[-1] == "chimney top"
    tab = dr.table(path, WOOD)
    peak = tab.temps[int(tab.air.argmax())]
    assert 500 <= peak <= 700
    assert tab.at(1573.15) == pytest.approx(DRAWN_1300, rel=0.01)
    assert all(tab.smooth > tab.air)
    step = tab.steps[-1]
    assert "Rough concrete" in (step.note or "")
    assert "Idel'chik" in (step.reference or "")
    assert "the band's most-air end at 1300 °C" in step.inputs
    assert path.steps[0].name == "The gas path"
    els = {e.name: e for e in path.elements}
    turn = els["into the inlet flue, a sharp turn up"]
    assert turn.k == pytest.approx(dr.elbow(4.5 / 6, 13.5 / 6))  # b₁/b₀ 0.75, a₀/b₀ 2.25
    up = els["turn up into the chimney"]
    assert up.k == pytest.approx(dr.elbow(9 / 7.5, 9 / 7.5))
    assert "past Idelchik's 0.5–2 side ratio" in (path.steps[0].note or "")


def test_a_turn_past_the_diagrams_edge_is_held_and_said() -> None:
    """A firebox 12 in tall turning up into a 4½ in flue: b₁/b₀ 0.375, under 6-6's 0.6."""
    e = dr.turn("t", "firebox", 13.5 * IN, 12 * IN, 4.5 * IN)
    assert e.k == pytest.approx(dr.elbow(0.6, 13.5 / 12))
    assert "held at the diagram's edge" in e.note
    assert e.re_dh == pytest.approx(dr.hydraulic(13.5 * IN, 12 * IN))


def test_an_inlet_narrower_than_its_channel_is_said() -> None:
    narrow = {"heat.fire.fireboxes": [{
        **yaml.safe_load((OLSEN / "fast-fire.yaml").read_text(encoding="utf-8"))["heat"]["fire"][
            "fireboxes"][0],
        "inlet": {"width": "9 in", "height": "4.5 in"},
    }]}  # fmt: skip
    path = dr.kiln_path(_design("fast-fire", narrow), grate_bar=0.75 * IN)
    assert "narrower or wider than its share" in (path.steps[0].note or "")


# The fast-fire's intakes, the dataset's (firebox-air-intakes.md §3): two mouths below the grate,
# 162–216 in², and above it, 121.5–175.5 in²
FAST_FIRE_INTAKES = dr.Intakes(
    (162 * IN**2, 216 * IN**2), (121.5 * IN**2, 175.5 * IN**2), "the dataset's, derived"
)


def test_the_intakes_in_parallel() -> None:
    """Below the grate a mouth (0.5) and the grate's ζ on its own area; above it an orifice,
    1/C²; the two at one pressure drop: K_eq = A_ref²/(Σ A_i/√K_i)² on the most primary area."""
    g = 2 * 12 * 24 * IN**2
    e = dr.intakes(FAST_FIRE_INTAKES, g, (1.73, 2.52), 2)
    a_p, a_s = 162 * IN**2, 121.5 * IN**2
    k_p = 0.5 + 2.52 * (a_p / g) ** 2
    want = (216 * IN**2 / (a_p / math.sqrt(k_p) + a_s * 0.65)) ** 2
    assert e.k == pytest.approx(want)
    assert e.k_lo is not None
    assert e.k_lo < e.k
    assert e.area * e.branches == pytest.approx(216 * IN**2)
    shut = dr.intakes(dr.Intakes((0.0, 0.0), (0.01, 0.01)), 0.0, None, 1)
    assert shut.k == pytest.approx(1 / 0.65**2)
    with pytest.raises(ValueError, match="needs an air intake"):
        dr.Intakes((0.0, 0.0))
    with pytest.raises(ValueError, match="least to its most"):
        dr.Intakes((0.2, 0.1))


def test_the_intakes_open_the_fast_fires_draft() -> None:
    """With the openings above the grate as well, the path draws more than through the ash-pit
    mouths alone; closing the intakes to half draws less; a share outside (0, 1] is refused."""
    k = load_design(OLSEN / "fast-fire.yaml")
    alone = dr.kiln_path(k, grate_bar=0.75 * IN)
    both = dr.kiln_path(k, grate_bar=0.75 * IN, intake=FAST_FIRE_INTAKES)
    assert both.elements[0].name.startswith(dr.INTAKE)
    assert not any(e.kind == "grate" for e in both.elements)
    assert "the dataset's" in (both.steps[0].note or "")
    t = {"firebox": 1500.0, "chamber": 1400.0, "chimney": 1000.0}
    assert dr.draw(both, t, WOOD).air > dr.draw(alone, t, WOOD).air
    half = both.opened(0.5)
    assert dr.draw(half, t, WOOD).air < dr.draw(both, t, WOOD).air
    assert both.opened(1.0) is both
    with pytest.raises(ValueError, match="share"):
        both.opened(0.0)
    bare = dr.kiln_path(k, intake=FAST_FIRE_INTAKES)
    assert bare.elements[0].k == pytest.approx(
        dr.intakes(FAST_FIRE_INTAKES, 2 * 12 * 24 * IN**2, None, 2).k
    )


def test_without_the_bars_size_the_grate_is_left_out_and_said() -> None:
    path = dr.kiln_path(load_design(OLSEN / "fast-fire.yaml"))
    assert not any(e.kind == "grate" for e in path.elements)
    assert "bars' size isn't given" in (path.steps[0].note or "")


def test_thinner_air_up_high_draws_less() -> None:
    """Olsen's 6000 ft firing of the same design (p.309): the US Standard Atmosphere's 81.2 kPa."""
    low = dr.kiln_path(load_design(OLSEN / "fast-fire.yaml"), grate_bar=0.75 * IN)
    high = dr.kiln_path(_design("fast-fire", {"site.elevation": "6000 ft"}), grate_bar=0.75 * IN)
    assert high.pressure == pytest.approx(81_200, rel=2e-3)
    t = {"firebox": 1500.0, "chamber": 1500.0, "chimney": 1500.0}
    assert dr.draw(high, t, WOOD).air < 0.9 * dr.draw(low, t, WOOD).air
    assert "Standard Atmosphere" in (high.steps[0].note or "")


def test_a_burner_kilns_path_draws_through_its_ports() -> None:
    """The 36 ft³ cross-draft given a chimney and flue (test inputs: the design has neither)."""
    k = _design(
        "olsen-crossdraft-36",
        {
            "draft.chimney": {"height": "12 ft", "inside": {"width": "9 in", "depth": "9 in"}},
            "draft.flue_port": {"width": "9 in", "height": "4.5 in"},
            "heat.gas.burners.port": {"diameter": "3 in"},
        },
    )
    path = dr.kiln_path(k)
    assert path.elements[0].branches == 6
    assert "venturi" in (path.steps[0].note or "")
    ng = gas.products(gas.natural_gas(), 1.0, ROOM)
    fuel = 6 * 36_000 * 0.29307107 / gas.natural_gas().hhv
    d = dr.draw(path, dict.fromkeys(("chamber", "chimney"), 1500.0), ng, fuel=fuel)
    assert d.air > 0
    assert d.gas == pytest.approx(d.air + fuel)


def test_round_passages_take_their_circles_area() -> None:
    d = dr.duct("pipe", "chimney", 0.2, 0.2, 3.0, rnd=True)
    assert d.area == pytest.approx(math.pi * 0.01)
    assert d.dh == pytest.approx(0.2)
    k = _design(
        "olsen-crossdraft-36",
        {
            "draft.chimney": {"height": "12 ft", "inside": {"diameter": "10 in"}},
            "draft.flue_port": {"diameter": "6 in"},
            "heat.gas.burners.port": {"diameter": "3 in"},
            "heat.gas.burners.up": "6 in",
        },
    )
    els = {e.name: e for e in dr.kiln_path(k).elements}
    assert els["chimney"].area == pytest.approx(math.pi * (10 * IN) ** 2 / 4)
    assert els["exit flue, through the flue wall"].dh == pytest.approx(6 * IN)
    assert els["chamber, inlet to the exit flue's middle"].rise == pytest.approx(-3 * IN)


NO_PORT = {
    "draft.chimney": {"height": "12 ft"},
    "draft.flue_port": {"width": "9 in", "height": "4.5 in"},
}


@pytest.mark.parametrize(
    ("name", "change", "words"),
    [
        ("olsen-crossdraft-36", {}, "no chimney"),
        ("fast-fire", {"draft.flue_port": None}, "one exit flue"),
        ("fast-fire", {"draft.chimney_through": "crown"}, "crown"),
        ("olsen-crossdraft-36", NO_PORT, "port size"),
        ("fast-fire", {"draft.chimney": {"height": "14 ft"}}, "inside section"),
    ],
)
def test_paths_v2_doesnt_build_are_refused(name: str, change: dict[str, Any], words: str) -> None:
    with pytest.raises(dr.NotModelledError, match=words):
        dr.kiln_path(_design(name, change))


def test_fireboxes_against_a_wall_are_refused() -> None:
    front = {"count": 1, "position": "front", "width": "13.5 in", "length": "24 in",
             "inlet": {"width": "9 in", "height": "4.5 in"}}  # fmt: skip
    with pytest.raises(dr.NotModelledError, match="under the floor"):
        dr.kiln_path(_design("fast-fire", {"heat.fire.fireboxes": [front]}))
    both = {"fuel": "natural_gas", "burners": {"rating": "36000 BTU/hr", "count": 2},
            "supply": {"type": "line", "pressure": "8 inch_H2O"}}  # fmt: skip
    with pytest.raises(dr.NotModelledError, match="one kind of heat"):
        dr.kiln_path(_design("fast-fire", {"heat.gas": both}))
