"""The design report: everything calculated from a design, with its working and findings."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from kilndesigner.bom import Bom, bill_of_materials
from kilndesigner.castable import CastableReport, castable_reports
from kilndesigner.electric import ElectricDesign, design_elements
from kilndesigner.frame import FrameDesign, design_frame
from kilndesigner.gas import GasDesign, design_gas
from kilndesigner.geometry import GeometryNotSupportedError, lining_parts
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
    hybrid: HybridAnalysis | None
    frame: FrameDesign
    castables: list[CastableReport]
    masonry: Masonry | None
    bom: Bom | None
    findings: list[Finding]

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.level == "error"]


def design_report(kiln: Kiln) -> Report:
    loss = heat_loss(kiln)
    electric = design_elements(kiln, loss.total_watts) if kiln.heat.electric is not None else None
    gas = design_gas(kiln) if kiln.heat.gas is not None else None
    findings = [*loss.findings, *(electric.findings if electric else [])]
    findings += gas.findings if gas else []
    hybrid: HybridAnalysis | None = None
    if electric is not None and gas is not None:
        site = kiln.site
        if site.electricity_price is not None and site.propane_price is not None:
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
    hardware = build_hardware(kiln, frame, gas)
    findings += [*frame.findings, *hardware.findings]
    # The heat the kiln puts in while its castables burn out: the elements, or else the burners
    heat_watts = (
        electric.installed_watts
        if electric is not None
        else si(Q_(gas.design_input_btu_hr, "BTU/hr"), "W")
        if gas is not None
        else None
    )
    placed: dict[str, float] = {}
    for part in lining_parts(kiln):
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
        bom = bill_of_materials(
            kiln, masonry, electric, gas, frame, hardware.chimney_bricks, castables
        )
        findings += [*masonry.findings, *bom.findings]
    order = {"error": 0, "warning": 1, "info": 2}
    findings = list({(f.level, f.message): f for f in findings}.values())  # once each
    findings.sort(key=lambda f: order[f.level])
    volume = Q_(chamber_shape(kiln).volume, "m**3")
    return Report(
        name=kiln.name,
        engine_version=ENGINE_VERSION,
        chamber_volume=show(volume, "ft**3" if kiln.units == "us" else "m**3", 3),
        heat_loss=loss,
        electric=electric,
        gas=gas,
        hybrid=hybrid,
        frame=frame,
        castables=castables,
        masonry=masonry,
        bom=bom,
        findings=findings,
    )
