"""The burners the book prints, at their supply pressure (ADR 0017 decision 13; `burners.py`;
`docs/research/burner-inputs.md`): the design's burners from the published charts, and the printed
orifices by Olsen's orifice equation (p.216), checked against the book's own printed figures."""

from __future__ import annotations

from typing import Any

import loads
import pytest
import reference as ref
import yaml

from kilndesigner.model import Kiln
from kilndesigner.v2.heat import burners as bu


def test_the_orifice_equation_gives_the_books_figures() -> None:
    """Olsen's orifice equation at K 0.80 (p.216) on each table's gas: Ward's #38 at 7 in. w.c. on
    natural gas, 35,424 BTU/hr (p.230, his worked example); his propane #38 at 11 in., 71,990
    (p.232); Gas Appliance's #32 on natural gas at 8 in., 54,000 (p.220–221, on Fig 8-39's
    1,100 BTU/ft³); Table 8-7's #18 at 10 in., about 191,000 on propane and 211,700 on butane
    (olsen-kilns.md, the three-chamber kiln's note)."""
    assert bu.orifice(38, 7.0, "natural_gas") == pytest.approx(35_424, rel=0.005)
    assert bu.orifice(38, 11.0, "propane") == pytest.approx(71_990, rel=0.005)
    assert bu.orifice(32, 8.0, "natural_gas_1100") == pytest.approx(54_000, rel=0.005)
    assert bu.orifice(18, 10.0, "propane") == pytest.approx(191_000, rel=0.005)
    assert bu.orifice(18, 10.0, "butane") == pytest.approx(211_700, rel=0.01)
    with pytest.raises(bu.BurnerError, match="no size"):
        bu.orifice(99, 8.0, "propane")
    with pytest.raises(bu.BurnerError, match="low pressure"):
        bu.orifice(32, 2 * bu.IN_WC_PER_PSI, "propane")


def test_the_kit_24s_burners() -> None:
    """Olsen's 24 kit: ten burners (p.174), MR-750 or MR-100 at 75,000 or 100,000 BTU/hr on
    natural gas at 8 in. w.c. (p.222): 750,000 or 1,000,000 BTU/hr; its printed propane firing
    through the #32 natural-gas orifices at most 4 in. w.c. (p.221, the general example of orifice
    sizing, ADR 0017 decision 16): 56,700 BTU/hr each, 567,000 for ten."""
    kit = bu.design_input(loads.design("olsen-kit-24"))
    assert kit.count == 10
    assert kit.total == pytest.approx(750_000, rel=1e-5)  # Pint's in. w.c. against 27.68 a psi
    mr100 = bu.carried(100_000, 8 / bu.IN_WC_PER_PSI, 8 / bu.IN_WC_PER_PSI, "natural_gas")
    assert 10 * mr100 == pytest.approx(1_000_000)
    assert 10 * bu.orifice(32, 4.0, "propane") == pytest.approx(567_000, rel=0.002)


def test_the_printed_burners_of_the_other_gas_kilns() -> None:
    """The three-chamber kiln: six Eclipse TR-80s, 214,200 BTU/hr each at 10 in. w.c. on a #18
    (p.224), 1,285,200 at peak (the design's rating); Bowen Mountain's eight MR-750s on propane at
    11 in. w.c. (assumed: p.215, p.227), GACO's published 72,000 each on its low-pressure orifice,
    576,000; W16's four burners, a #34 at 8 in. w.c. on natural gas (p.228): 45,400 each by the
    orifice equation, 181,500, against the 50,000 each (200,000) printed and Rule 4's 45 ft³/hr a
    burner (p.227–228)."""
    three = bu.design_input(loads.design("olsen-three-chamber"))
    assert three.total == pytest.approx(1_285_200)
    assert bu.orifice(18, 10.0, "propane") < three.each < bu.orifice(18, 10.0, "butane") * 1.01
    bowen = bu.design_input(loads.design("bowen-mountain"))
    assert (bowen.count, bowen.each) == (8, 72_000)
    assert "low-pressure orifice" in bowen.how
    w16 = bu.orifice(34, 8.0, "natural_gas")
    assert w16 == pytest.approx(45_380, rel=0.005)
    assert 4 * w16 < 200_000


def _kit(change: dict[str, Any]) -> Kiln:
    data = yaml.safe_load((ref.ROOT / "examples" / "olsen" / "olsen-kit-24.yaml").read_text(
        encoding="utf-8"))  # fmt: skip
    for key, value in change.items():
        node = data
        *parents, last = key.split(".")
        for p in parents:
            node = node.setdefault(p, {})
        node[last] = value
    return Kiln.model_validate(data)


def test_a_library_burner_on_propane_and_what_isnt_given() -> None:
    """A library burner on propane above 2 psi reads its published curve (the MR-750 at 5 psi,
    121,570 BTU/hr); refused where no source gives the input: no rating and no library burner
    (Kähler's power burners, Blakebrough's compound injectors), no count, no pressure at the
    burners (a tank), a burner with no natural-gas rating on natural gas."""
    line = {"heat.gas.fuel": "propane", "heat.gas.supply": {"type": "line", "pressure": "5 psi"}}
    assert bu.design_input(_kit(line)).each == pytest.approx(121_570, rel=1e-6)
    with pytest.raises(bu.BurnerError, match="isn't sourced"):
        bu.design_input(loads.design("kahler-salt"))
    with pytest.raises(bu.BurnerError, match="isn't sourced"):
        bu.design_input(loads.design("blakebrough-tasmania"))
    with pytest.raises(bu.BurnerError, match="no gas burners"):
        bu.design_input(loads.design("fast-fire"))
    with pytest.raises(bu.BurnerError, match="how many"):
        bu.design_input(_kit({"heat.gas.burners.count": None}))
    tank = {"heat.gas.fuel": "propane", "heat.gas.supply": {"type": "tank", "gallons": 500}}
    with pytest.raises(bu.BurnerError, match="no pressure"):
        bu.design_input(_kit(tank))
    with pytest.raises(bu.BurnerError, match="no natural-gas rating"):
        bu.design_input(_kit({"heat.gas.burners.model": "Ransome B3"}))
