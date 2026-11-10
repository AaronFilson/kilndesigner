"""v2's draft (`heat/draft.py`): the pressure balance round the gas path, against a closed form,
the survey's probe of the fast-fire (`scratch/toolsets/gas-path/gas_path.py`) on its own inputs,
and the paths built from the design files."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import pytest
import yaml

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
    (ρ_a − ρ_g)·g·H = ρ_g·v²/2, so m_gas = ρ_g·A·√(2(ρ_a − ρ_g)gH/ρ_g)."""
    h, a, t = 4.0, 0.05, 1200.0
    path = dr.Path((dr.column("stack", "chimney", h), dr.outlet("top", "chimney", a)), ROOM)
    d = dr.draw(path, {"chimney": t}, WOOD)
    rho_g = WOOD.props(t)[0]
    want = rho_g * a * math.sqrt(2 * (path.room_density - rho_g) * dr.G * h / rho_g)
    assert d.gas == pytest.approx(want, rel=1e-8)
    assert d.air == pytest.approx(want * WOOD.air / WOOD.mass, rel=1e-8)
    fixed = dr.draw(path, {"chimney": t}, WOOD, fuel=0.001)
    assert fixed.gas == pytest.approx(want, rel=1e-8)
    assert fixed.air == pytest.approx(want - 0.001, rel=1e-8)


def test_no_buoyancy_no_flow() -> None:
    path = dr.Path((dr.column("down", "chimney", -1.0), dr.outlet("top", "chimney", 0.05)), ROOM)
    assert dr.draw(path, {"chimney": 1200.0}, WOOD).air == 0.0


def _probe_path() -> dr.Path:
    """gas_path.py's fast-fire path, element for element (its inputs: the chimney's 14 ft from the
    firebox top, a 12 in firebox run, ¾ in round bars at 1½ in, 1 mm roughness)."""
    a_fb, a_in, a_ex, a_ch = 13.5 * 6 * IN**2, 13.5 * 4.5 * IN**2, 9 * 7.5 * IN**2, 81 * IN**2
    z_exit, z_top = 20.75 * IN, 12.5 * IN + 14 * FT
    els = (
        dr.inlet("ash pit", 13.5 * 6.5 * IN**2, 2),
        dr.grate("grate", 12 * IN, 24 * IN, 0.75 * IN, 0.75 * IN, 2),
        dr.column("firebox", "firebox", 10.5 * IN),
        dr.duct("firebox run", "firebox", 13.5 * IN, 6 * IN, 12 * IN, 2),
        dr.contraction_turn("into the inlet", "firebox", a_fb, a_in, 2),
        dr.duct("inlet", "firebox", 13.5 * IN, 4.5 * IN, 4.5 * IN, 2),
        dr.outlet("inlet out", "firebox", a_in, 2),
        dr.column("chamber", "chamber", 3.75 * IN),
        dr.entrance("exit in", "chamber", a_ex),
        dr.duct("exit", "chamber", 9 * IN, 7.5 * IN, 4.5 * IN),
        dr.turn_expansion("turn up", "chimney", a_ex, a_ch),
        dr.column("chimney", "chimney", z_top - z_exit),
        dr.duct("chimney", "chimney", 9 * IN, 9 * IN, z_top - z_exit),
        dr.outlet("top", "chimney", a_ch),
    )
    return dr.Path(els, 21.1 + 273.15, rough=1e-3)


# gas_path.py at λ 1, adiabatic chimney, firebox at T + 50 K (scratch/v2-heat/probe_draft.py)
PROBE = {350.0: 0.076094, 600.0: 0.105947, 1000.0: 0.096880, 1600.0: 0.082203}


@pytest.mark.parametrize("t", sorted(PROBE))
def test_the_surveys_fast_fire_probe_on_its_own_inputs(t: float) -> None:
    d = dr.draw(_probe_path(), {"firebox": t + 50, "chamber": t, "chimney": t}, WOOD)
    assert d.air == pytest.approx(PROBE[t], rel=2e-3)


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
    assert "grate, round bars (Blevins)" in names
    assert names[-1] == "chimney top"
    tab = dr.table(path, WOOD)
    peak = tab.temps[int(tab.air.argmax())]
    assert 500 <= peak <= 700
    assert tab.at(1573.15) == pytest.approx(0.083, rel=0.05)
    assert all(tab.smooth > tab.air)
    step = tab.steps[-1]
    assert "Rough concrete" in (step.note or "")
    assert "smooth wall at 1300 °C" in step.inputs
    assert path.steps[0].name == "The gas path"


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
