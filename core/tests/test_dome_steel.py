"""Steel for a sail dome over a whole-wall door: AISC 360-16 F10 for the buttress angle, hot
(Appendix 4), the rods, and the steel's temperature range (steel-design.md)."""

from __future__ import annotations

from pathlib import Path

import pytest

from kilndesigner import frame as frame_module
from kilndesigner import load_design
from kilndesigner.frame import (
    Angle,
    angle,
    angle_allowable,
    design_frame,
    hot_steel,
    steel_data,
)
from kilndesigner.frame_checks import HotSteel
from kilndesigner.model import Kiln

EXAMPLES = Path(__file__).parents[2] / "examples"


def _cold(t: float = 70.0) -> HotSteel:
    d = steel_data()["hot_steel"]
    return HotSteel(t, 1.0, 1.0, d["fy_psi"], d["e_psi"], d["omega_b"], d["source"], "test")


def _dome(**roof: str) -> Kiln:
    document = load_design(EXAMPLES / "dome-castable-kiln.yaml").model_dump(
        mode="json", by_alias=True
    )
    document["roof"].update(roof)
    return Kiln.model_validate(document)


def test_f10_reproduces_the_worked_check() -> None:
    """door-headers.md §D2: L4×4×¼ over Lb = 28 in, Cb = 1, cold: Mn(LTB) = 39.0 kip·in, leg
    buckling 43.3, so Ma = 39.0/1.67 = 23.4 kip·in."""
    assert angle_allowable(angle("L4×4×1/4"), 28, _cold()) == pytest.approx(23_350, rel=0.005)


def test_f10_branches() -> None:
    """A compact leg is limited by yielding or LTB; a long bay goes past My/Mcr = 1 (F10-3); a thin
    leg is slender (F10-7)."""
    compact = angle("L2×2×1/4")  # b/t = 8
    short = angle_allowable(compact, 1, _cold())
    assert short == pytest.approx(1.5 * 0.8 * 36_000 * compact.sx / 1.67, rel=1e-6)
    assert angle_allowable(compact, 2000, _cold()) < short / 5  # F10-3
    slender = Angle("thin", 4, 0.1, 1, 0.5, 0.4, 1.0)  # b/t = 40 > λr = 25.8
    lam = 40
    e = 29e6
    assert angle_allowable(slender, 1, _cold()) == pytest.approx(
        0.71 * e / lam**2 * 0.8 * 0.5 / 1.67, rel=1e-6
    )


def test_hot_steel_is_weaker_by_aiscs_table() -> None:
    d = steel_data()["hot_steel"]
    hot = HotSteel(1000, 0.66, 0.49, d["fy_psi"], d["e_psi"], d["omega_b"], d["source"], "t")
    a = angle("L3×3×1/4")
    cold = angle_allowable(a, 1, _cold())
    assert 0.49 * cold < angle_allowable(a, 1, hot) <= 0.66 * cold


def test_the_steels_temperature_comes_from_the_wall_solve() -> None:
    hot = hot_steel(_dome(), ("left", "right"))
    assert 68 < hot.temperature < 600
    assert hot.ky == 1.0
    assert 0.78 <= hot.ke <= 1.0


def _with_heat(monkeypatch: pytest.MonkeyPatch, t: float) -> None:
    d = steel_data()["hot_steel"]
    import numpy as np

    def fake(kiln: Kiln, faces: tuple[str, ...]) -> HotSteel:
        return HotSteel(
            t, float(np.interp(t, d["ky_deg_f"], d["ky"])),
            float(np.interp(t, d["ke_deg_f"], d["ke"])), d["fy_psi"], d["e_psi"],
            d["omega_b"], d["source"], "test",
        )  # fmt: skip

    monkeypatch.setattr(frame_module, "hot_steel", fake)


def test_steel_past_aiscs_table_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    _with_heat(monkeypatch, 1500)
    frame = design_frame(_dome())
    assert frame.members == []
    [err] = [f for f in frame.findings if f.check and f.check.id == "frame.steel-heat"]
    assert err.level == "error"
    assert "1400 °F" in err.message


def test_steel_past_giles_service_limit_warns(monkeypatch: pytest.MonkeyPatch) -> None:
    _with_heat(monkeypatch, 700)
    frame = design_frame(_dome())
    [warn] = [f for f in frame.findings if f.check and f.check.id == "frame.steel-heat"]
    assert warn.level == "warning"
    assert frame.kind == "dome frame"


def test_too_hot_steel_finds_no_angle(monkeypatch: pytest.MonkeyPatch) -> None:
    """At 1,390 °F the steel keeps 17 % of its yield and 11 % of its stiffness: no listed angle
    carries the dome, and the rods are still checked. The table is cut at L4×4×3/8, as it stood
    before the larger angles came in: an L8×8 still carries it."""
    _with_heat(monkeypatch, 1390)
    upto = [a for a in frame_module.angles() if a.leg <= 4 and a.t <= 0.375]
    monkeypatch.setattr(frame_module, "angles", lambda: upto)
    frame = design_frame(_dome())
    ids = {f.check.id: f for f in frame.findings if f.check}
    assert ids["frame.dome-buttress"].level == "error"
    assert "No listed angle" in ids["frame.dome-buttress"].message


def test_a_door_in_a_side_wall_bears_on_the_front_and_back() -> None:
    document = load_design(EXAMPLES / "dome-castable-kiln.yaml").model_dump(
        mode="json", by_alias=True
    )
    document["loading"]["face"] = "left"
    frame = design_frame(Kiln.model_validate(document))
    assert frame.thrust is not None
    assert "front and back walls" in frame.thrust
    assert frame.posts == 2


def test_a_rod_too_small_is_reported(monkeypatch: pytest.MonkeyPatch) -> None:
    data = dict(steel_data())
    data["rods"] = {**data["rods"], "sizes": data["rods"]["sizes"][:2]}  # ½ in the biggest
    data["binding_stress_psi"] = 100
    monkeypatch.setattr(frame_module, "steel_data", lambda: data)
    frame = design_frame(_dome())
    ids = {f.check.id: f.level for f in frame.findings if f.check}
    assert ids["frame.dome-rod"] == "error"
