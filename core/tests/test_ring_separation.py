"""The fifth research round in the statics: unbonded rings act separately (Sarhosis et al. 2016)
and hot joints slide at dense refractory's hot friction (Oliveira et al. 2021);
mortar-and-brick-strength.md S1, S6."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from kilndesigner.designfile import parse_design
from kilndesigner.frame import HOT_FRICTION, JointFriction
from kilndesigner.frame_checks import rings_apart
from kilndesigner.model import Kiln, SprungArch
from kilndesigner.vault import along_statics

BOWEN = Path(__file__).parents[2] / "examples" / "olsen" / "bowen-mountain.yaml"


def _bowen(**roof: Any) -> Kiln:
    data = yaml.safe_load(BOWEN.read_text(encoding="utf-8"))
    data["roof"].update(roof)
    return parse_design(yaml.safe_dump(data, allow_unicode=True))


def _heyman(kiln: Kiln) -> str:
    working, _ = along_statics(kiln)
    return next(s for s in working if "Heyman" in s.name).value


def test_bowens_two_rings_stand_as_the_inside_ring_alone() -> None:
    # Two 4½ in rings, unbonded: the inside one is checked, 3.7 times the thinnest (was 7.0)
    apart = _bowen()
    assert isinstance(apart.roof, SprungArch)
    assert apart.roof.ring == 2
    assert not apart.roof.rings_bonded
    assert "a 4.495 in ring" in _heyman(apart)
    assert "3.7 times the thinnest" in _heyman(apart)
    working, findings = along_statics(apart)
    note = next(s for s in working if "Heyman" in s.name).note or ""
    assert "Sarhosis" in note
    assert not [f for f in findings if f.level == "error"]
    # Bonded through with headers, the two act as one 9 in ring
    bonded = _bowen(rings_bonded=True)
    assert "7.0 times the thinnest" in _heyman(bonded)
    working, _ = along_statics(bonded)
    assert "Sarhosis" not in (next(s for s in working if "Heyman" in s.name).note or "")


def test_rings_apart_is_said_only_for_unbonded_rings_of_several_layers() -> None:
    assert rings_apart(1, False) is None
    assert rings_apart(2, True) is None
    said = rings_apart(3, False)
    assert said is not None
    assert "the 2 over it its load" in said


def test_hot_friction_names_the_materials_it_was_not_measured_on() -> None:
    assert HOT_FRICTION == 0.50
    tested = JointFriction(HOT_FRICTION, "", ())
    assert "0.50" in tested.note
    assert "unconfirmed" not in tested.note
    ifb = JointFriction(HOT_FRICTION, "", ("JM 26",))
    assert "none is measured hot for JM 26" in ifb.note
