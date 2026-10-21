"""The design report: everything calculated from a design, with its working and findings."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from kilndesigner.electric import ElectricDesign, design_elements
from kilndesigner.heatloss import HeatLoss, heat_loss
from kilndesigner.model import Kiln
from kilndesigner.shape import chamber_shape
from kilndesigner.units import Q_
from kilndesigner.working import Finding, show

ENGINE_VERSION = "0.1.0"


class Report(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    engine_version: str
    chamber_volume: str
    heat_loss: HeatLoss
    electric: ElectricDesign | None
    findings: list[Finding]

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.level == "error"]


def design_report(kiln: Kiln) -> Report:
    loss = heat_loss(kiln)
    electric = design_elements(kiln, loss.total_watts) if kiln.heat.electric is not None else None
    findings = [*loss.findings, *(electric.findings if electric else [])]
    order = {"error": 0, "warning": 1, "info": 2}
    findings.sort(key=lambda f: order[f.level])
    volume = Q_(chamber_shape(kiln).volume, "m**3")
    return Report(
        name=kiln.name,
        engine_version=ENGINE_VERSION,
        chamber_volume=show(volume, "ft**3" if kiln.units == "us" else "m**3", 3),
        heat_loss=loss,
        electric=electric,
        findings=findings,
    )
