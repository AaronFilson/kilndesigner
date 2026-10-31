import type { FiringResult, SlowFiring } from "@kilndesigner/api-client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { SlowFiringPanel } from "./SlowFiringPanel";

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

const json = (data: unknown, status = 200) =>
  new Response(JSON.stringify(data), { status, headers: { "Content-Type": "application/json" } });

afterEach(() => {
  cleanup();
  server.routes.clear();
});

const firing = (over: Partial<FiringResult> = {}): FiringResult => ({
  name: "Test kiln",
  heat: "electric",
  switch_over_c: null,
  reached_c: 1285,
  target_c: 1285,
  duration_h: 48,
  duration: "48 h 0 min",
  held: true,
  completed: true,
  electricity_kwh: 400,
  fuel_kwh: 0,
  propane_gallons: null,
  energy_kwh: 400,
  walls_kwh: 380,
  ware_kwh: 20,
  shell_kwh: 300,
  cost_usd: 48,
  cost: "$48.00",
  points: [],
  faces: [],
  working: [],
  findings: [],
  ...over,
});

const slow = (over: Partial<SlowFiring> = {}): SlowFiring => ({
  hours: 48,
  soak_h: 6,
  top_c: 1285,
  rate_c_per_h: 30.1,
  firing: firing(),
  quickest: firing({ duration: "5 h 24 min", energy_kwh: 60, shell_kwh: 25, cost: "$7.27" }),
  walls_share: 0.95,
  ware_share: 0.05,
  shell_share: 0.75,
  sources: [
    { kiln: "Bizen", fuel: "wood", time: "7 days", used: null, notes: null, reference: "Olsen p.99" },
  ],
  working: [{ name: "Slow firing schedule", value: "30 °C/h", reference: "the author", inputs: {} }],
  findings: [{ level: "info", message: "Over 48 h the shell loses 75% of the heat put in." }],
  ...over,
});

function show() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={client}>
      <SlowFiringPanel simKey="k" />
    </QueryClientProvider>,
  );
}

describe("SlowFiringPanel", () => {
  it("sends the time and soak, and shows where the heat goes against the quickest firing", async () => {
    let asked: unknown;
    let answer = () => {};
    const answered = new Promise<void>((resolve) => (answer = resolve));
    server.routes.set("POST /api/simulations/k/slow", async (request) => {
      asked = await request.json();
      await answered;
      return json(slow());
    });
    show();
    fireEvent.change(screen.getByLabelText("Firing time"), { target: { value: "2 day" } });
    fireEvent.change(screen.getByLabelText("Soak at the top, within it"), { target: { value: "6 h" } });
    fireEvent.click(screen.getByRole("button", { name: "Work out the slow firing" }));
    expect(await screen.findByText(/Firing the kiln slowly/)).toBeTruthy();
    answer();
    expect(await screen.findByText("300 kWh (75%)")).toBeTruthy();
    expect(asked).toEqual({ time: "2 day", soak: "6 h" });
    expect(screen.getByText("30.1 °C/h to 1285 °C, then 6 h at the top")).toBeTruthy();
    expect(screen.getByText("5 h 24 min, 60 kWh (shell lost 25)")).toBeTruthy();
    expect(screen.getByText("$48.00 (quickest $7.27)")).toBeTruthy();
    expect(screen.getByText("Bizen")).toBeTruthy();
    expect(screen.getByText(/the shell loses 75%/)).toBeTruthy();
    expect(screen.getByText(/Slow firing schedule: 30 °C\/h/)).toBeTruthy();
  });

  it("gives a wood kiln the sources only, and an unfinished firing says so", async () => {
    server.routes.set("POST /api/simulations/k/slow", () =>
      json(slow({ firing: null, quickest: null, soak_h: 0, walls_share: null })),
    );
    show();
    fireEvent.click(screen.getByRole("button", { name: "Work out the slow firing" }));
    expect(await screen.findByText("30.1 °C/h to 1285 °C")).toBeTruthy();
    expect(screen.queryByText("Heat put in")).toBeNull();
    cleanup();
    server.routes.set("POST /api/simulations/k/slow", () =>
      json(
        slow({
          firing: firing({ completed: false, cost: null }),
          walls_share: null,
          sources: [{ kiln: "A kiln", fuel: "wood", time: "2 days", used: "a cord", notes: null, reference: "S48" }],
        }),
      ),
    );
    show();
    fireEvent.click(screen.getByRole("button", { name: "Work out the slow firing" }));
    expect(await screen.findByText("48 h 0 min (doesn't reach the top)")).toBeTruthy();
    expect(screen.getByText("380 kWh")).toBeTruthy();
    expect(screen.getByText("a cord")).toBeTruthy();
    expect(screen.queryByText("Cost")).toBeNull();
  });

  it("says why a slow firing is refused", async () => {
    server.routes.set("POST /api/simulations/k/slow", () =>
      json({ detail: "the soak must be at least zero and shorter than the firing" }, 400),
    );
    show();
    fireEvent.click(screen.getByRole("button", { name: "Work out the slow firing" }));
    expect(await screen.findByText(/can't be worked out: the soak must be/)).toBeTruthy();
  });
});
