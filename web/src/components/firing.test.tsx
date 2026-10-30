import type { FiringPoint, FiringResult, Simulation, SwitchOverChart } from "@kilndesigner/api-client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { FiringPanel, firingCharts } from "./FiringPanel";
import { map } from "./heatmap.fixture";

const server = vi.hoisted(() => {
  class PageRequest extends Request {
    constructor(input: RequestInfo | URL, init?: RequestInit) {
      super(typeof input === "string" ? new URL(input, location.href) : input, init);
    }
  }
  const routes = new Map<string, (request: Request) => Response | Promise<Response>>();
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const request = new PageRequest(input, init);
    const answer = routes.get(`${request.method} ${new URL(request.url).pathname}`);
    return answer ? answer(request) : new Response(null, { status: 404, statusText: "Not Found" });
  });
  vi.stubGlobal("Request", PageRequest);
  vi.stubGlobal("fetch", fetch);
  return { routes };
});

// The heatmap's canvas needs WebGL: this stands in for it and shows what it was given
vi.mock("./WallHeatmap", () => ({
  WallHeatmap: (props: { time: number; show: string[] }) => (
    <p>
      Heatmap at row {props.time}, showing {props.show.join(" ")}
    </p>
  ),
}));

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } });

afterEach(() => {
  cleanup();
  server.routes.clear();
});

const sim = (over: Partial<Simulation> = {}): Simulation => ({
  key: "k",
  status: "done",
  summary: null,
  error: null,
  created_at: "2026-10-29T12:00:00Z",
  finished_at: "2026-10-29T12:01:00Z",
  ...over,
});

const point = (t: number, over: Partial<FiringPoint> = {}): FiringPoint => ({
  time_h: t,
  chamber_c: 20 + 200 * t,
  setpoint_c: 20 + 200 * t,
  heat_kw: 10,
  available_kw: 11.5,
  electric_kw: 10,
  fuel_kw: 0,
  walls_kw: 10,
  ware_kw: 0,
  shell_kw: 0.5,
  energy_kwh: 10 * t,
  electricity_kwh: 10 * t,
  fuel_kwh: 0,
  cost_usd: 1.2 * t,
  hottest_shell_c: 20 + 10 * t,
  ...over,
});

const result: FiringResult = {
  name: "Test kiln",
  heat: "electric",
  switch_over_c: null,
  reached_c: 1285,
  target_c: 1285,
  duration_h: 5.4,
  duration: "5 h 24 min",
  held: true,
  completed: true,
  electricity_kwh: 60.5,
  fuel_kwh: 0,
  propane_gallons: null,
  energy_kwh: 60.5,
  walls_kwh: 60.5,
  ware_kwh: 0,
  shell_kwh: 2.5,
  cost_usd: 7.27,
  cost: "$7.27",
  points: [],
  faces: map.walls.map((face) => ({
    face,
    depths_m: [0.025, 0.075],
    layers: ["a", "b"],
    inside_area_m2: 1,
    outside_area_m2: 1.4,
  })),
  working: [{ name: "Firing time", value: "5.40 h", reference: "thermal/transient.py", inputs: {} }],
  findings: [{ level: "info", message: "No ware is given." }],
};

const chart: SwitchOverChart = {
  points: [
    { switch_over_c: 204, switch_over_f: 400, duration_h: 4.7, cost_usd: 60, electricity_kwh: 14,
      propane_gallons: 16.7, held: true, completed: true, handed_over_c: 204, elements_stalled: false },
    { switch_over_c: 649, switch_over_f: 1200, duration_h: 14.4, cost_usd: 54, electricity_kwh: 137,
      propane_gallons: 10.8, held: true, completed: true, handed_over_c: 649, elements_stalled: false },
    { switch_over_c: 1093, switch_over_f: 2000, duration_h: 70.5, cost_usd: 110, electricity_kwh: 793,
      propane_gallons: 4.3, held: true, completed: true, handed_over_c: 1089, elements_stalled: true },
    { switch_over_c: 1204, switch_over_f: 2200, duration_h: 66, cost_usd: 91, electricity_kwh: 759,
      propane_gallons: 0.1, held: true, completed: false, handed_over_c: null, elements_stalled: false },
  ],
  cheapest_c: 649,
  fastest_c: 204,
  working: [],
  findings: [{ level: "info", message: "The elements stall at about 1993 °F." }],
}; // prettier-ignore

function show() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={client}>
      <FiringPanel simKey="k" />
    </QueryClientProvider>,
  );
}

function finished(over: { switchover?: SwitchOverChart; result?: Partial<FiringResult>; points?: FiringPoint[] } = {}) {
  server.routes.set("GET /api/simulations/k", () => json(sim()));
  server.routes.set("GET /api/simulations/k/result", () => json({ ...result, ...over.result }));
  server.routes.set("GET /api/simulations/k/series", () => json(over.points ?? [point(0), point(5.4)]));
  server.routes.set("GET /api/simulations/k/heatmap", () => json(map));
  if (over.switchover) server.routes.set("GET /api/simulations/k/switchover", () => json(over.switchover));
}

describe("FiringPanel", () => {
  it("offers to simulate a firing not yet run, and starts it", async () => {
    let started = false;
    server.routes.set("GET /api/simulations/k", () => (started ? json(sim({ status: "running" })) : json(null, 404)));
    server.routes.set("POST /api/simulations/k", () => {
      started = true;
      return json(sim({ status: "queued" }), 202);
    });
    show();
    fireEvent.click(await screen.findByRole("button", { name: "Simulate the firing" }));
    expect(await screen.findByText("Waiting for the worker…")).toBeTruthy();
  });

  it("says why a firing couldn't be simulated, and offers to try again", async () => {
    server.routes.set("GET /api/simulations/k", () =>
      json(sim({ status: "failed", error: "no sourced specific heat for Kast-O-Lite" })),
    );
    show();
    expect(await screen.findByText(/can't be simulated: no sourced specific heat/)).toBeTruthy();
    expect(screen.getByRole("button", { name: "Simulate again" })).toBeTruthy();
  });

  it("says while the firing runs", async () => {
    server.routes.set("GET /api/simulations/k", () => json(sim({ status: "running" })));
    show();
    expect(await screen.findByText("Firing the kiln, step by step…")).toBeTruthy();
  });

  it("shows an error from the API", async () => {
    server.routes.set("GET /api/simulations/k", () => json({ detail: "broken" }, 500));
    show();
    expect(await screen.findByText("broken")).toBeTruthy();
  });

  it("shows the firing: summary, charts, heatmap with its scrubber, findings and working", async () => {
    finished();
    show();
    expect(await screen.findByText("5 h 24 min")).toBeTruthy();
    expect(screen.getByText("$7.27")).toBeTruthy();
    for (const title of ["Temperature", "Power", "Energy and cost"]) {
      expect(screen.getByRole("img", { name: title })).toBeTruthy();
    }
    expect(screen.queryByRole("img", { name: /hand-over/ })).toBeNull();
    // The heatmap starts at the end of the firing, without the front and the roof
    expect(await screen.findByText("Heatmap at row 1, showing left right back floor")).toBeTruthy();
    const table = screen.getByRole("table");
    expect(within(table).getAllByText("1000 °C")).toHaveLength(6);
    fireEvent.change(screen.getByRole("slider", { name: "Time through the firing" }), { target: { value: "0" } });
    expect(screen.getByText("Heatmap at row 0, showing left right back floor")).toBeTruthy();
    expect(within(table).getAllByText("20 °C")).toHaveLength(12);
    fireEvent.click(screen.getByRole("checkbox", { name: "roof" }));
    expect(screen.getByText("Heatmap at row 0, showing left right back floor roof")).toBeTruthy();
    fireEvent.click(screen.getByRole("checkbox", { name: "left" }));
    expect(screen.getByText("Heatmap at row 0, showing right back floor roof")).toBeTruthy();
    expect(screen.getByLabelText("Temperature scale").textContent).toContain("1000 °C");
    expect(screen.getByText("No ware is given.")).toBeTruthy();
    expect(screen.getByText(/Firing time: 5.40 h/)).toBeTruthy();
  });

  it("shows a hybrid's fuel and its switch-over charts, marking the cheapest", async () => {
    finished({
      switchover: chart,
      result: { fuel_kwh: 300, propane_gallons: 7, held: false, completed: false, heat: "electric, then gas" },
      points: [point(0, { fuel_kw: 30, fuel_kwh: 0 }), point(10, { fuel_kw: 30, fuel_kwh: 300 })],
    });
    show();
    expect(await screen.findByText("300.0 kWh (7.0 gal propane)")).toBeTruthy();
    expect(screen.getByText("no: the heat falls behind")).toBeTruthy();
    expect(screen.getByText(/stopped before the end/)).toBeTruthy();
    expect(await screen.findByRole("img", { name: "Cost against the hand-over to the burners" })).toBeTruthy();
    expect(screen.getAllByTestId("marker")).toHaveLength(2);
    expect(screen.getByText("The elements stall at about 1993 °F.")).toBeTruthy();
  });

  it("says when the results can't be loaded", async () => {
    server.routes.set("GET /api/simulations/k", () => json(sim()));
    server.routes.set("GET /api/simulations/k/result", () => json({ detail: "gone" }, 500));
    show();
    expect(await screen.findByText("The firing could not be loaded: gone")).toBeTruthy();
  });
});

describe("the firing's charts", () => {
  it("leave out fuel, electricity and cost where the firing had none", () => {
    const charts = firingCharts([point(0, { cost_usd: null, electricity_kwh: 0 })]);
    expect(charts.map((c) => c.title)).toEqual(["Temperature", "Power", "Energy"]);
    expect(charts[2]!.series.map((s) => s.label)).toEqual(["Put into the kiln, kWh"]);
    expect(charts[1]!.series.map((s) => s.label)).not.toContain("Fuel burned");
  });
});
