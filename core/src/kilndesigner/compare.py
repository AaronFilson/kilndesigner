"""Designs side by side: the headline numbers of each design's report, in one order.

The numbers are the report's own, as it shows them; nothing here calculates. The command line's
``compare`` and the MCP server's ``compare_designs`` both set designs out with these rows.
"""

from __future__ import annotations

from kilndesigner.report import Report

COMPARED = (
    "Chamber volume",
    "Heat loss at top",
    "Hottest outside face",
    "Installed power",
    "Burner input",
    "Propane supply keeps up",
    "Switch to burners at",
    "Materials (priced)",
    "Errors / warnings",
)
"""The rows of a comparison, in the order they're shown."""


def comparison_rows(report: Report) -> dict[str, str]:
    """The headline numbers of a design, for comparing designs side by side."""
    hottest = max(
        report.heat_loss.faces, key=lambda f: float(f.surface_temperature.split()[0])
    ).surface_temperature
    rows = {
        "Chamber volume": report.chamber_volume,
        "Heat loss at top": report.heat_loss.total,
        "Hottest outside face": hottest,
    }
    if report.electric is not None:
        rows["Installed power"] = report.electric.installed_power
    if report.gas is not None:
        g = report.gas
        rows["Burner input"] = g.design_input
        if g.supply:  # a line (natural gas) has no cylinders or tank to check
            meets = sum(s.meets_demand for s in g.supply)
            rows["Propane supply keeps up"] = f"in {meets} of {len(g.supply)} cases"
    if report.hybrid is not None:
        rows["Switch to burners at"] = report.hybrid.switch_over
    if report.bom is not None:
        unpriced = any(line.cost is None for line in report.bom.lines)
        rows["Materials (priced)"] = f"${report.bom.total:,.0f}" + (
            " + unpriced items" if unpriced else ""
        )
    levels = [f.level for f in report.findings]
    rows["Errors / warnings"] = f"{levels.count('error')} / {levels.count('warning')}"
    return rows
