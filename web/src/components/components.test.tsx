import type { Report } from "@kilndesigner/api-client";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { reportTabLabel } from "./BuildPanel";
import { Materials } from "./Materials";
import { Problems, where } from "./Problems";
import { ReportView } from "./ReportView";

afterEach(cleanup);

describe("where", () => {
  it("writes a problem's location as a path", () => {
    expect(where(["lining", "walls", 0, "thickness"])).toBe("lining.walls[0].thickness");
    expect(where([])).toBe("");
  });
});

describe("Problems", () => {
  it("lists each problem with where it is", () => {
    render(<Problems problems={[{ loc: ["chamber", "width"], msg: "Field required" }]} />);
    expect(screen.getByRole("alert").textContent).toContain("chamber.width Field required");
  });

  it("shows nothing when there are none", () => {
    const { container } = render(<Problems problems={[]} />);
    expect(container.innerHTML).toBe("");
  });
});

const report: Report = {
  name: "Test kiln",
  engine_version: "0.1.0",
  chamber_volume: "7.0 ft³",
  heat_loss: {
    top_temperature: "2345 °F",
    ambient: "70 °F",
    total: "5.1 kW",
    total_watts: 5100,
    faces: [],
    working: [{ name: "Q", value: "5.1 kW", formula: "Q = ΣUAΔT", inputs: {} }],
    findings: [],
  },
  electric: null,
  gas: null,
  hybrid: null,
  frame: {
    kind: "welded case",
    angle: null,
    angle_leg_in: 0,
    angle_t_in: 0.125,
    rod: null,
    rod_d_in: 0,
    thrust: null,
    members: [],
    working: [],
    findings: [],
  },
  castables: [],
  masonry: null,
  bom: null,
  findings: [{ level: "warning", message: "Surface load is high" }],
};

describe("reportTabLabel", () => {
  it("counts the errors and warnings", () => {
    expect(reportTabLabel(undefined)).toBe("Report");
    expect(reportTabLabel(report)).toBe("Report (1 warning)");
    const worse = {
      ...report,
      findings: [...report.findings, ...report.findings, { level: "error", message: "No" }],
    } as Report;
    expect(reportTabLabel(worse)).toBe("Report (1 error, 2 warnings)");
  });
});

describe("Materials", () => {
  it("lists what to buy with the total, and the cut list", () => {
    const withBom = {
      ...report,
      bom: {
        lines: [
          {
            item: "JM 26 brick",
            needed: "100 bricks",
            buy: "110 bricks",
            unit_price: "$7.17",
            cost: 788.7,
            priced_as: null,
            source: null,
          },
        ],
        total: 788.7,
        prices_checked: "2026-10-21",
        findings: [],
      },
      masonry: {
        quantities: [
          {
            material: "ifb-jm26",
            name: "JM 26 brick",
            kind: "insulating_firebrick",
            amount: 110,
            unit: "bricks",
            detail: "",
            priced_amount: 110,
          },
        ],
        cut_list: [{ material: "ifb-jm26", cut: "cut to 4.5 in long", count: 12 }],
        findings: [],
      },
    } as Report;
    render(<Materials report={withBom} />);
    expect(screen.getByRole("table", { name: "Bill of materials" }).textContent).toContain("$789");
    const cuts = screen.getByRole("table", { name: "Cut list" });
    expect(cuts.textContent).toContain("JM 26 brickcut to 4.5 in long12");
  });

  it("says so when there is no bill of materials", () => {
    render(<Materials report={report} />);
    expect(screen.getByText("This design has no bill of materials.")).toBeTruthy();
  });
});

describe("ReportView", () => {
  it("shows the headline numbers, the findings and the working", () => {
    render(<ReportView report={report} />);
    expect(screen.getByText("5.1 kW", { selector: "dd" })).toBeTruthy();
    expect(screen.getByText(/Surface load is high/)).toBeTruthy();
    expect(screen.getByText("Working (1 step)")).toBeTruthy();
    expect(screen.queryByText("Elements")).toBeNull();
  });

  it("puts notes in their own section, not among the warnings", () => {
    const noted = {
      ...report,
      findings: [...report.findings, { level: "info", message: "k is carried on past the sheet" }],
    } as Report;
    const { container } = render(<ReportView report={noted} />);
    expect(screen.getByText("Notes")).toBeTruthy();
    expect(container.querySelector(".notes")?.textContent).toContain("k is carried on");
    expect(container.querySelector(".report > .findings")?.textContent).not.toContain("carried");
    expect(reportTabLabel(noted)).toBe("Report (1 warning)");
  });
});
