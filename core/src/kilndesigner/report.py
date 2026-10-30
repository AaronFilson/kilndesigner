"""The design report: everything calculated from a design, with its working and findings."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from kilndesigner.bom import Bom, bill_of_materials
from kilndesigner.castable import CastableReport, castable_reports
from kilndesigner.electric import ElectricDesign, design_elements
from kilndesigner.fire import FireDesign, design_fire
from kilndesigner.frame import FrameDesign, design_frame
from kilndesigner.gas import GasDesign, design_gas
from kilndesigner.geometry import GeometryNotSupportedError, lining_parts, not_drawn
from kilndesigner.hardware import build_hardware
from kilndesigner.heatloss import HeatLoss, heat_loss
from kilndesigner.hybrid import HybridAnalysis, analyse_hybrid
from kilndesigner.masonry import Masonry, plan_masonry
from kilndesigner.model import Kiln
from kilndesigner.shape import chamber_shape
from kilndesigner.units import Q_, si
from kilndesigner.working import Finding, show

ENGINE_VERSION = "0.1.0"


class Report(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    engine_version: str
    chamber_volume: str
    heat_loss: HeatLoss
    electric: ElectricDesign | None
    gas: GasDesign | None
    fire: FireDesign | None = None
    hybrid: HybridAnalysis | None
    frame: FrameDesign
    castables: list[CastableReport]
    masonry: Masonry | None
    bom: Bom | None
    findings: list[Finding]

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.level == "error"]


def _unique_checks(findings: list[Finding]) -> list[Finding]:
    """Label each finding's check (E1, E2, W1 in report order) and number a check that fires more
    than once (``frame.slice``, ``frame.slice-2``), so the page, the plans and the workbook can link
    each finding to its own sheet."""
    seen: dict[str, int] = {}
    counts = {"error": 0, "warning": 0}
    out: list[Finding] = []
    for f in findings:
        if f.check is not None and f.level != "info":
            n = seen[f.check.id] = seen.get(f.check.id, 0) + 1
            counts[f.level] += 1
            label = f"{'E' if f.level == 'error' else 'W'}{counts[f.level]}"
            check_id = f.check.id if n == 1 else f"{f.check.id}-{n}"
            check = f.check.model_copy(update={"id": check_id, "label": label})
            f = f.model_copy(update={"check": check})
        out.append(f)
    return out


def design_report(kiln: Kiln) -> Report:
    loss = heat_loss(kiln)
    electric = design_elements(kiln, loss.total_watts) if kiln.heat.electric is not None else None
    gas = design_gas(kiln, loss.total_watts) if kiln.heat.gas is not None else None
    fire = design_fire(kiln) if kiln.heat.fire is not None else None
    findings = [*loss.findings, *(electric.findings if electric else [])]
    findings += gas.findings if gas else []
    findings += fire.findings if fire else []
    hybrid: HybridAnalysis | None = None
    if electric is not None and gas is not None:
        site = kiln.site
        if kiln.heat.gas is not None and kiln.heat.gas.fuel != "propane":
            # The cost comparison is worked out for propane by the gallon only (ADR 0009)
            findings.append(
                Finding(
                    level="info",
                    message=(
                        "When the elements should hand over to the burners is worked out for "
                        "propane only, so it isn't given for this natural-gas kiln."
                    ),
                )
            )
        elif site.electricity_price is not None and site.propane_price is not None:
            hybrid = analyse_hybrid(kiln, electric.installed_watts)
            findings += hybrid.findings
        else:
            findings.append(
                Finding(
                    level="info",
                    message=(
                        "Give the site's electricity_price and propane_price to find when the "
                        "elements should hand over to the burners."
                    ),
                )
            )
    frame = design_frame(kiln)
    drawn = not_drawn(kiln) is None
    hardware = build_hardware(kiln, frame, gas, fire) if drawn else None
    findings += [*frame.findings, *(hardware.findings if hardware is not None else [])]
    # The heat the kiln puts in while its castables burn out: the elements, or else the burners
    heat_watts = (
        electric.installed_watts
        if electric is not None
        else si(Q_(gas.design_input_btu_hr, "BTU/hr"), "W")
        if gas is not None
        else si(Q_(fire.full_fire_btu_hr, "BTU/hr"), "W")
        if fire is not None and fire.full_fire_btu_hr > 0
        else None
    )
    placed: dict[str, float] = {}
    for part in lining_parts(kiln) if drawn else []:
        if kiln.castable(part.material) is not None:
            placed[part.material] = placed.get(part.material, 0.0) + part.volume * 1e-9
    castables = castable_reports(kiln, loss, heat_watts, placed)
    for c in castables:
        findings += c.findings
    masonry: Masonry | None = None
    bom: Bom | None = None
    try:
        masonry = plan_masonry(kiln).result
    except GeometryNotSupportedError as e:
        findings.append(Finding(level="info", message=f"No masonry plan or bill of materials: {e}"))
    if masonry is not None:
        bricks = hardware.chimney_bricks if hardware is not None else 0
        bom = bill_of_materials(kiln, masonry, electric, gas, frame, bricks, castables)
        findings += [*masonry.findings, *bom.findings]
    order = {"error": 0, "warning": 1, "info": 2}
    findings = list({(f.level, f.message): f for f in findings}.values())  # once each
    findings.sort(key=lambda f: order[f.level])
    findings = _unique_checks(findings)
    volume = Q_(chamber_shape(kiln).volume, "m**3")
    return Report(
        name=kiln.name,
        engine_version=ENGINE_VERSION,
        chamber_volume=show(volume, "ft**3" if kiln.units == "us" else "m**3", 3),
        heat_loss=loss,
        electric=electric,
        gas=gas,
        fire=fire,
        hybrid=hybrid,
        frame=frame,
        castables=castables,
        masonry=masonry,
        bom=bom,
        findings=findings,
    )
