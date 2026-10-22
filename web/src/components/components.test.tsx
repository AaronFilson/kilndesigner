import type { Report } from "@kilndesigner/api-client";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

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
  masonry: null,
  bom: null,
  findings: [{ level: "warning", message: "Surface load is high" }],
};

describe("ReportView", () => {
  it("shows the headline numbers, the findings and the working", () => {
    render(<ReportView report={report} />);
    expect(screen.getByText("5.1 kW", { selector: "dd" })).toBeTruthy();
    expect(screen.getByText(/Surface load is high/)).toBeTruthy();
    expect(screen.getByText("Working (1 step)")).toBeTruthy();
    expect(screen.queryByText("Elements")).toBeNull();
  });
});
