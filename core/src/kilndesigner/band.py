"""The tension band round a round kiln's dome, sized hot (bands-and-bottle-kilns.md §1, §3, §5).

The band holds the dome's ring tension H (membrane theory, ``frame.round_dome_ring``). Its
allowable stress is the lesser of:

- f_y · k_y,θ / 5: A36's yield, reduced to the band's temperature by EN 1993-1-2:2005 Table 3.1
  (linear between rows, as its note allows), over Norton's factor of safety for a dome's band,
  "at least 5" (*Refractories*, 1949, p.732). Norton doesn't say whether his 5 is on yield or on
  ultimate strength. It is taken on yield here: on A36's 58 ksi ultimate it would allow 11.6 ksi
  cold against 7.2 ksi on its 36 ksi yield, so on yield is the safe side.
- HarbisonWalker's 12,000 psi, the limit "many furnace designers" put on bindings that may run
  hot (Brick Installation Guide, 2008, p.20).

The band's temperature: no measured temperature of a band on a brick kiln was found
(bands-and-bottle-kilns.md §5). The engine's own outside-surface temperature stands in for it:
the hottest of the walls' and roof's outside faces in the steady state at the top temperature
(heatloss.py), the band sitting on the wall's top where the dome springs. Above Table 3.1's last
row, 1200 °C, the band isn't checked (ADR 0009).
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from kilndesigner.sheet import Sheet
from kilndesigner.units import Q_
from kilndesigner.working import Finding, Step

if TYPE_CHECKING:
    from kilndesigner.model import Kiln

FLAT_BAR = ("¼ × 2 in flat bar", 0.25 * 2.0)
"""The flat bar the engine's frames use elsewhere (Pitelka), checked as the band."""
PITELKA = "Pitelka, sprung-arch frames (¼ × 2 in flat bar); kiln-hardware.md §4.2 [S11]"
TEMPERATURE_SOURCE = (
    "heatloss.py: the outside surface, steady state at the top temperature; no measured band "
    "temperature on a brick kiln found (bands-and-bottle-kilns.md §5)"
)
FOS_NOTE = (
    "Norton doesn't say whether his 5 is on yield or ultimate; taken on yield, the safe side "
    "(on A36's 58 ksi ultimate it would allow 11.6 ksi cold, on its 36 ksi yield 7.2 ksi)"
)


def ky(data: dict[str, Any], t_c: float) -> float:
    """EN 1993-1-2 Table 3.1's k_y,θ at ``t_c`` °C, linear between rows; 1 below 20 °C. Raises
    ValueError above the table's last row."""
    temps: list[float] = data["ky_deg_c"]
    if t_c >= temps[-1]:
        raise ValueError(f"at or past EN 1993-1-2 Table 3.1's last row, {temps[-1]:.0f} °C")
    return float(np.interp(t_c, temps, data["ky"]))


def band_temperature(kiln: Kiln) -> float:
    """The band's temperature, °C: the hottest outside face of the walls and roof (heatloss.py)."""
    from kilndesigner.heatloss import heat_loss

    faces = [f for f in heat_loss(kiln).faces if f.face != "floor"]
    return max(f.layers[-1].cold_side_k for f in faces) - 273.15


def dome_band(kiln: Kiln, ring_lb: float) -> tuple[list[Step], Finding]:
    """The band for a dome's ring tension ``ring_lb`` (lb): the area it needs, and the engine's
    ¼ × 2 in flat bar checked against the allowable stress hot."""
    from kilndesigner.frame import steel_data

    data = steel_data()
    band, hot = data["band"], data["hot_steel"]
    t_c = band_temperature(kiln)
    try:
        k = ky(band, t_c)
    except ValueError as e:
        return [], Finding(
            level="info",
            message=(
                f"The dome's band isn't checked: its temperature, taken from the wall's outside "
                f"face, is {t_c:.0f} °C, {e}, the range steel's hot strength is given over."
            ),
            reference=band["ky_source"],
        )
    name, area = FLAT_BAR
    s = Sheet(
        "frame.dome-band",
        f"Tension band round the dome's springing, {name}, hot",
        reference=f"{band['ky_source']}; {band['safety_source']}; {data['binding_stress_source']}",
    )
    s.given("H", "the dome's ring tension at its springing", Q_(ring_lb, "lbf"),
            source="frame.py: membrane theory (Timoshenko §106)")  # fmt: skip
    s.given("T_b", "the band's temperature", Q_(t_c, "degC"), "degC", source=TEMPERATURE_SOURCE)
    s.given("F_y0", "A36 yield stress, cold", Q_(hot["fy_psi"], "psi"), source=hot["source"])
    s.given("k_y", "f_y,θ / f_y at T_b", k, source=f"{band['ky_source']}, interpolated")
    s.given("n", "factor of safety for a dome's band, on yield", band["safety"],
            source=f"{band['safety_source']}; {FOS_NOTE}")  # fmt: skip
    s.let("σ_N", "Norton's allowable, hot", "k_y*F_y0/n", "psi")
    hw = Q_(data["binding_stress_psi"], "psi")
    s.given("σ_HW", "HarbisonWalker's limit for bindings that may run hot", hw,
            source=data["binding_stress_source"])  # fmt: skip
    s.let("σ_allow", "the lesser of the two", "min(σ_N, σ_HW)", "psi")
    s.let("A_req", "the band's least cross-section", "H/σ_allow", "in**2")
    s.given("A_b", f"{name}'s cross-section", Q_(area, "in**2"), source=PITELKA)
    s.let("σ", "stress in the band", "H/A_b", "psi")
    s.require("σ", "<=", "σ_allow")
    s.lever("A_b", Q_(0.05, "in**2"), Q_(20, "in**2"))
    check = s.check()
    sigma_n = k * hot["fy_psi"] / band["safety"]
    allow = min(sigma_n, data["binding_stress_psi"])
    governs = (
        "Norton's 5 on the yield, hot"
        if sigma_n <= data["binding_stress_psi"]
        else "HarbisonWalker's 12,000 psi"
    )
    need = ring_lb / allow
    steps = [
        Step(
            name="Dome band: its temperature",
            value=f"{t_c:.0f} °C",
            formula="the hottest outside face of the walls and roof, steady at the top temperature",
            reference=TEMPERATURE_SOURCE,
            note="no measured band temperature on a brick kiln is sourced: the engine's own",
        ),
        Step(
            name="Dome band: allowable stress, hot",
            formula="min(f_y·k_y,θ / 5, 12,000 psi)",
            inputs={"f_y": f"{hot['fy_psi']:,.0f} psi", "k_y,θ": f"{k:.3g}"},
            value=f"{allow:,.0f} psi; {governs} governs",
            reference=f"{band['ky_source']}; {band['safety_source']}; "
            f"{data['binding_stress_source']}",
            note=FOS_NOTE,
        ),
        Step(
            name="Dome band: least cross-section",
            formula="A = H / σ_allow",
            inputs={"H": f"{ring_lb:,.0f} lb"},
            value=f"{need:.3g} in²",
            reference="statics",
            note=f"the engine's {name} has {area:g} in²",
        ),
    ]
    text = (
        f"The band round the dome's springing carries {ring_lb:,.0f} lb of ring tension at about "
        f"{t_c:.0f} °C (the wall's outside face, the engine's own figure: no measured band "
        f"temperature is sourced). It needs at least {need:.3g} in² of steel at {allow:,.0f} psi "
        f"({governs} governs); "
    )
    if check.status == "pass":
        finding = Finding(
            level="info",
            message=text + f"a {name} ({area:g} in²) holds it. Allow for scale and rust "
            "besides (Kent's rule 6: no number given).",
            reference=s.reference,
            check=check,
        )
    else:
        finding = Finding.failed(
            check,
            message=text + f"a {name} ({area:g} in²) doesn't: use a band of that section or more.",
        )
    return steps, finding
