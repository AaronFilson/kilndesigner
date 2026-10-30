import type { Report } from "@kilndesigner/api-client";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { AppearanceMenu } from "./AppearanceMenu";
import { reportTabLabel } from "./BuildPanel";
import { Castables } from "./Castables";
import { Materials } from "./Materials";
import { Problems, where } from "./Problems";
import { ReportView } from "./ReportView";

afterEach(cleanup);

/** The value shown beside a label in a list of rows. */
const row = (label: string, scope: HTMLElement = document.body) =>
  [...scope.querySelectorAll("dt")].find((dt) => dt.textContent === label)?.nextElementSibling?.textContent;

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
    posts: 2,
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

  it("doesn't count notes", () => {
    const noted = { ...report, findings: [{ level: "info", message: "k is extrapolated" }] } as Report;
    expect(reportTabLabel(noted)).toBe("Report");
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

  it("marks what isn't priced, and names a brick by its id when the masonry doesn't", () => {
    const unpriced = {
      ...report,
      bom: {
        lines: [
          {
            item: "Kiln shelf",
            needed: "4",
            buy: "4",
            unit_price: null,
            cost: null,
            priced_as: null,
            source: null,
          },
        ],
        total: 0,
        prices_checked: "2026-10-21",
        findings: [{ level: "warning", message: "Shelves aren't priced" }],
      },
      masonry: {
        quantities: [],
        cut_list: [{ material: "hfb-super", cut: "split", count: 4 }],
        findings: [],
      },
    } as unknown as Report;
    render(<Materials report={unpriced} />);
    const bom = screen.getByRole("table", { name: "Bill of materials" });
    const shelf = within(bom).getByRole("row", { name: /Kiln shelf/ });
    expect(shelf.textContent).toBe("Kiln shelf44—not priced");
    expect(screen.getByText(/Shelves aren't priced/)).toBeTruthy();
    expect(screen.getByRole("table", { name: "Cut list" }).textContent).toContain("hfb-supersplit4");
  });

  it("has no cut list when nothing is cut", () => {
    const bom = { lines: [], total: 0, prices_checked: "", findings: [] };
    const uncut = { ...report, bom } as unknown as Report;
    render(<Materials report={uncut} />);
    expect(screen.getByRole("table", { name: "Bill of materials" }).textContent).toContain("$0");
    expect(screen.queryByRole("table", { name: "Cut list" })).toBeNull();
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

  it("cites where an error or a note comes from", () => {
    const cited = {
      ...report,
      findings: [
        { level: "error", message: "The hot face is past its limit", reference: "JM 26 data sheet" },
        { level: "info", message: "Conductivity is extrapolated", reference: "ASTM C201" },
      ],
    } as Report;
    render(<ReportView report={cited} />);
    const error = screen.getByText(/past its limit/).closest("li");
    expect(error?.className).toBe("error");
    expect(within(error!).getByText("JM 26 data sheet").tagName).toBe("CITE");
    const note = screen.getByText(/extrapolated/).closest("li");
    expect(within(note!).getByText("ASTM C201").tagName).toBe("CITE");
  });

  it("shows an electric kiln's elements, with the working's formulas and sources", () => {
    const electric = {
      ...report,
      electric: {
        alloy: "Kanthal A1",
        installed_power: "11.5 kW",
        power_per_volume: "1.6 kW/ft³",
        line_current: "48 A",
        elements: {
          count: 6,
          gauge: "14 AWG",
          wiring: "in parallel",
          length_each: "60 ft",
          surface_load: "2.1 W/cm²",
          pitch: "0.5 in",
        },
        working: [
          { name: "P", value: "11.5 kW", formula: "P = V²/R", reference: "Kanthal handbook" },
          { name: "I", value: "48 A" },
        ],
        findings: [],
      },
    } as unknown as Report;
    render(<ReportView report={electric} />);
    const section = screen.getByRole("heading", { name: "Elements" }).closest("section")!;
    expect(row("Installed power", section)).toBe("11.5 kW (1.6 kW/ft³)");
    expect(row("Elements", section)).toBe("6 × 14 AWG Kanthal A1, in parallel");
    expect(row("Coil pitch", section)).toBe("0.5 in");
    expect(within(section).getByText("Working (2 steps)")).toBeTruthy();
    expect(within(section).getByText("P = V²/R").tagName).toBe("CODE");
    expect(within(section).getByText("Kanthal handbook").tagName).toBe("CITE");
  });

  it("leaves out the elements' rows when none were designed", () => {
    const supplyOnly = {
      ...report,
      electric: {
        alloy: "Kanthal A1",
        installed_power: "0 kW",
        power_per_volume: "0 kW/ft³",
        line_current: "0 A",
        elements: null,
        working: [],
        findings: [],
      },
    } as unknown as Report;
    render(<ReportView report={supplyOnly} />);
    const section = screen.getByRole("heading", { name: "Elements" }).closest("section")!;
    expect(row("Line current", section)).toBe("0 A");
    expect(row("Elements", section)).toBeUndefined();
    expect(row("Surface load", section)).toBeUndefined();
    expect(within(section).queryByText(/^Working/)).toBeNull();
  });

  it("shows a gas kiln's burners and propane, and when a hybrid hands over to gas", () => {
    const hybrid = {
      ...report,
      gas: {
        design_input: "300,000 BTU/h",
        propane_at_full_fire: "3.3 gal/h",
        tank_suggestion: null,
        chimney_height: "12 ft",
        flue_area: "40 in²",
        working: [],
      },
      hybrid: { switch_over: "1800 °F", switch_over_reason: "The elements can't keep up", working: [] },
    } as unknown as Report;
    render(<ReportView report={hybrid} />);
    const gas = screen.getByRole("heading", { name: "Burners and propane" }).closest("section")!;
    expect(row("Burner input", gas)).toBe("300,000 BTU/h");
    expect(row("Chimney height", gas)).toBe("12 ft");
    expect(row("Tank", gas)).toBeUndefined();
    const handover = screen.getByRole("heading", { name: "Electric to gas" }).closest("section")!;
    expect(row("Switch to burners at", handover)).toBe("1800 °F");
    expect(row("Why", handover)).toBe("The elements can't keep up");
  });

  it("calls a frame of angle and rods a steel frame, and totals the priced materials", () => {
    const framed = {
      ...report,
      frame: {
        ...report.frame,
        kind: "angle frame",
        angle: "2 × 2 × 3/16 in",
        rod: "1/2 in",
        thrust: "350 lbf",
      },
      bom: { lines: [], total: 1234.4, prices_checked: "2026-10-21", findings: [] },
    } as Report;
    render(<ReportView report={framed} />);
    const frame = screen.getByRole("heading", { name: "Steel frame" }).closest("section")!;
    expect(row("Angle", frame)).toBe("2 × 2 × 3/16 in");
    expect(row("Tie rods", frame)).toBe("1/2 in");
    expect(row("Arch thrust", frame)).toBe("350 lbf");
    expect(row("Priced items")).toBe("$1,234");
    expect(screen.queryByRole("heading", { name: "Case" })).toBeNull();
  });
});

type CastableReport = Report["castables"][number];

const castable = {
  mix: {
    id: "foamed",
    name: "Foamed mix",
    batch: [
      { ingredient: "mulcoa-70", name: "Mulcoa 70", mass: "30 lb", share: "60 %", volume: "", source: "" },
      { ingredient: "secar-71", name: "Secar 71", mass: "20 lb", share: "40 %", volume: "", source: "" },
    ],
    dry_mass: "50 lb",
    water: "10 lb",
    water_share: "20 %",
    foam: "50 %",
    cast_volume: "1.2 ft³",
    wet_density: "62 lb/ft³",
    quart_weighs: "2.1 lb",
    dried_density: "55 lb/ft³",
    fired_density: "50 lb/ft³",
    porosity: "78 %",
    conductivity: ["0.25 W/m·K at 500 °C", "0.31 W/m·K at 1000 °C"],
    service_limit: null,
    sets: "",
    working: [
      { name: "Dry mass", value: "50 lb" },
      { name: "Cast volume", value: "1.2 ft³", formula: "V = m / ρ", reference: "Castable notes" },
    ],
    findings: [],
  },
  placed: "the walls' hot face",
  batches: 3,
  allowance: "5 %",
  totals: [],
  layers: [
    {
      face: "walls",
      thickness: "2 in",
      hot_side: "2345 °F",
      cold_side: "1500 °F",
      notes: ["Above its service limit.", "Fire it slowly."],
    },
  ],
  first_firing: [
    { name: "Water", value: "4 lb", inputs: { batches: "3", "per batch": "1.3 lb" } },
    { name: "Bound water", value: "1 lb" },
  ],
  schedule: [
    { to: "250 °F", rate: "50 °F/h", hold: "4 h", why: "Dry it" },
    { to: "1000 °F", rate: "100 °F/h", hold: null, why: "Burn out the foam" },
  ],
  schedule_hours: 12.6,
  steps: ["Weigh the dry ingredients.", "Mix in the water, then the foam."],
  findings: [
    { level: "warning", message: "Its strength isn't known" },
    { level: "info", message: "Conductivity is estimated from porosity" },
  ],
} as unknown as CastableReport;

describe("Castables", () => {
  it("says so when the design mixes none", () => {
    render(<Castables report={report} />);
    expect(screen.getByText("This design has no castables of its own.")).toBeTruthy();
  });

  it("gives the batch to weigh, what it becomes, and how many batches to mix", () => {
    render(<Castables report={{ ...report, castables: [castable] }} />);
    const mix = screen.getByRole("region", { name: "Foamed mix" });
    const batch = within(mix).getByRole("table", { name: "One batch of Foamed mix" });
    expect(within(batch).getAllByRole("row").map((r) => r.textContent)).toEqual([
      "IngredientWeightShare",
      "Mulcoa 7030 lb60 %",
      "Secar 7120 lb40 %",
      "Water10 lb20 %",
    ]);
    expect(row("Foam", mix)).toBe("50 %");
    expect(row("Conductivity (estimated)", mix)).toBe("0.25 W/m·K at 500 °C; 0.31 W/m·K at 1000 °C");
    expect(row("Service limit", mix)).toBe("not sourced: test it");
    expect(row("Batches to mix", mix)).toBe("3, with 5 % to spare");
    expect(within(mix).getAllByRole("listitem").map((li) => li.textContent)).toContain(
      "Mix in the water, then the foam.",
    );
    expect(within(mix).getByText("Working (2 steps)")).toBeTruthy();
    expect(within(mix).getByText("V = m / ρ").tagName).toBe("CODE");
  });

  it("plans the first firing, says what it drives off and what the wall's heat means for it", () => {
    render(<Castables report={{ ...report, castables: [castable] }} />);
    const schedule = screen.getByRole("table", { name: "First firing of Foamed mix" });
    expect(within(schedule).getByText("First firing, about 13 h")).toBeTruthy();
    expect(within(schedule).getAllByRole("row").map((r) => r.textContent)).toEqual([
      "ToRateHoldWhy",
      "250 °F50 °F/h4 hDry it",
      "1000 °F100 °F/h—Burn out the foam",
    ]);
    expect(row("Water")).toBe("4 lb (batches: 3; per batch: 1.3 lb)");
    expect(row("Bound water")).toBe("1 lb");
    expect(screen.getByText(/^walls, 2 in/).closest("li")?.textContent).toBe(
      "walls, 2 in (2345 °F to 1500 °F): Above its service limit. Fire it slowly.",
    );
    expect(screen.getByText(/strength isn't known/).closest("li")?.className).toBe("warning");
    expect(screen.getByText(/estimated from porosity/).closest("section")?.className).toBe("notes");
  });

  it("leaves out what wasn't worked out", () => {
    const plain = {
      ...castable,
      mix: { ...castable.mix, foam: null, service_limit: "2000 °F" },
      batches: 0,
      schedule: [],
      layers: [],
      first_firing: [],
      findings: [],
    };
    render(<Castables report={{ ...report, castables: [plain] }} />);
    expect(row("Foam")).toBeUndefined();
    expect(row("Batches to mix")).toBeUndefined();
    expect(row("Service limit")).toBe("2000 °F");
    expect(screen.queryByRole("table", { name: "First firing of Foamed mix" })).toBeNull();
    expect(screen.queryByRole("heading", { name: "In the wall" })).toBeNull();
    expect(screen.queryByRole("heading", { name: "The first firing drives off" })).toBeNull();
  });

  it("gives a first firing without its length when it isn't known", () => {
    render(<Castables report={{ ...report, castables: [{ ...castable, schedule_hours: null }] }} />);
    const schedule = screen.getByRole("table", { name: "First firing of Foamed mix" });
    expect(schedule.querySelector("caption")?.textContent).toBe("First firing");
  });
});

describe("AppearanceMenu", () => {
  afterEach(() => {
    localStorage.clear();
    delete document.documentElement.dataset.theme;
    delete document.documentElement.dataset.accent;
  });

  it("starts from this browser's choice, then applies and remembers a new one", () => {
    localStorage.setItem("kilndesigner.appearance", JSON.stringify({ theme: "dark", accent: "celadon" }));
    render(<AppearanceMenu />);
    const theme = screen.getByLabelText("Theme") as HTMLSelectElement;
    const accent = screen.getByLabelText("Accent colour") as HTMLSelectElement;
    expect([theme.value, accent.value]).toEqual(["dark", "celadon"]);
    fireEvent.change(theme, { target: { value: "light" } });
    expect(document.documentElement.dataset).toMatchObject({ theme: "light", accent: "celadon" });
    fireEvent.change(accent, { target: { value: "cobalt" } });
    expect(document.documentElement.dataset.accent).toBe("cobalt");
    expect(theme.value).toBe("light");
    expect(JSON.parse(localStorage.getItem("kilndesigner.appearance") ?? "")).toEqual({
      theme: "light",
      accent: "cobalt",
    });
  });

  it("offers every theme and accent", () => {
    render(<AppearanceMenu />);
    const options = (label: string) =>
      [...(screen.getByLabelText(label) as HTMLSelectElement).options].map((o) => o.textContent);
    expect(options("Theme")).toEqual(["As the system", "Light", "Dark"]);
    expect(options("Accent colour")).toEqual([
      "Terracotta",
      "Shino",
      "Celadon",
      "Cobalt",
      "Tenmoku",
      "Copper red",
    ]);
  });
});
