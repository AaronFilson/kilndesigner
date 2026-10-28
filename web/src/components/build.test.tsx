import type { Build, Report } from "@kilndesigner/api-client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import type { ReactElement } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { KilnDocument, Layout } from "../design";
import { BuildPanel } from "./BuildPanel";
import { Drawings } from "./Drawings";

// openapi-fetch takes fetch and Request as the client is made, when api.ts is imported, so they
// are stubbed first. The app asks for /api/... relative to the page: a browser resolves that, and
// Node's Request doesn't, so this one does it the browser's way.
const server = vi.hoisted(() => {
  class PageRequest extends Request {
    constructor(input: RequestInfo | URL, init?: RequestInit) {
      super(typeof input === "string" ? new URL(input, location.href) : input, init);
    }
  }
  const routes = new Map<string, (request: Request) => Response | Promise<Response>>();
  const log: string[] = [];
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const request = new PageRequest(input, init);
    const route = `${request.method} ${new URL(request.url).pathname}`;
    log.push(route);
    const answer = routes.get(route);
    return answer ? answer(request) : new Response(null, { status: 404, statusText: "Not Found" });
  });
  vi.stubGlobal("Request", PageRequest);
  vi.stubGlobal("fetch", fetch);
  return { routes, log };
});

// The model needs WebGL, which jsdom hasn't got: this stands in for it and shows what it was given
vi.mock("./KilnViewer", () => ({
  KilnViewer: (props: { url: string; partsUrl: string; layout?: Layout; draft?: KilnDocument | null }) => (
    <p>
      Model {props.url}, parts {props.partsUrl}, {props.layout ? props.layout.ports.length : "no"} ports,
      draft {props.draft?.name ?? "none"}
    </p>
  ),
}));

const json = (data: unknown, status = 200, statusText = "OK") =>
  new Response(JSON.stringify(data), {
    status,
    statusText,
    headers: { "Content-Type": "application/json" },
  });

afterEach(() => {
  cleanup();
  server.routes.clear();
  server.log.length = 0;
});

const build = (over: Partial<Build> = {}): Build => ({
  key: "k",
  status: "done",
  files: [],
  notes: [],
  error: null,
  created_at: "2026-10-01T12:00:00Z",
  finished_at: "2026-10-01T12:05:00Z",
  ...over,
});

const report = {
  name: "Test kiln",
  engine_version: "0.1.0",
  chamber_volume: "7.0 ft³",
  heat_loss: {
    top_temperature: "2345 °F",
    ambient: "70 °F",
    total: "5.1 kW",
    total_watts: 5100,
    faces: [],
    working: [],
    findings: [],
  },
  electric: null,
  gas: null,
  hybrid: null,
  frame: { kind: "welded case", angle: null, rod: null, thrust: null, working: [], findings: [] },
  castables: [],
  masonry: null,
  bom: null,
  findings: [{ level: "warning", message: "Surface load is high" }],
} as unknown as Report;

const layout = { units: "us", walls: {}, ports: [{ kind: "spy" }] } as unknown as Layout;

function show(ui: ReactElement) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(<QueryClientProvider client={client}>{ui}</QueryClientProvider>);
}

describe("BuildPanel", () => {
  it("checks the build, then offers to start one that hasn't been, and follows it", async () => {
    server.routes.set("POST /api/builds/k", () => json(build({ status: "queued", finished_at: null }), 202));
    show(<BuildPanel buildKey="k" />);
    expect(screen.getByText("Checking the build…")).toBeTruthy();
    fireEvent.click(await screen.findByRole("button", { name: "Build" }));
    expect(await screen.findByText("Waiting for the worker…")).toBeTruthy();
    expect(server.log).toEqual(["GET /api/builds/k", "POST /api/builds/k"]);
  });

  it("says why a build failed, and offers to build it again", async () => {
    server.routes.set("GET /api/builds/k", () => json(build({ status: "failed", error: "Out of memory" })));
    show(<BuildPanel buildKey="k" />);
    expect(await screen.findByText("The build failed: Out of memory")).toBeTruthy();
    expect(screen.getByRole("button", { name: "Build again" })).toBeTruthy();
  });

  it("says when the worker is building it", async () => {
    server.routes.set("GET /api/builds/k", () => json(build({ status: "running" })));
    show(<BuildPanel buildKey="k" />);
    expect(await screen.findByText("Building the model and the plans…")).toBeTruthy();
  });

  it("says why the build couldn't be checked", async () => {
    server.routes.set("GET /api/builds/k", () => json({ detail: "The database is down" }, 503));
    show(<BuildPanel buildKey="k" />);
    expect(await screen.findByText("The database is down")).toBeTruthy();
  });

  it("shows a finished build's model where the build put the ports, its notes and its files", async () => {
    const files = ["kiln.glb", "parts.json", "layout.json", "report.json", "plans.pdf", "sections.dxf"];
    server.routes.set("GET /api/builds/k", () => json(build({ files, notes: ["Fired with engine 0.1.0"] })));
    server.routes.set("GET /api/builds/k/files/layout.json", () => json(layout));
    server.routes.set("GET /api/builds/k/report", () => json(report));
    const draft = { name: "Being edited" } as KilnDocument;
    show(<BuildPanel buildKey="k" draft={draft} />);
    const model = "Model /api/builds/k/files/kiln.glb, parts /api/builds/k/files/parts.json";
    expect(await screen.findByText(`${model}, 1 ports, draft Being edited`)).toBeTruthy();
    expect(screen.getByRole("tab", { name: "3D model" }).getAttribute("aria-selected")).toBe("true");
    expect(screen.getByText("Fired with engine 0.1.0")).toBeTruthy();
    const links = screen.getAllByRole("link").map((a) => [a.textContent, a.getAttribute("href")]);
    expect(links).toEqual([
      ["Plans (PDF)", "/api/builds/k/files/plans.pdf"],
      ["Sections (DXF)", "/api/builds/k/files/sections.dxf"],
      ["3D model (glTF)", "/api/builds/k/files/kiln.glb"],
      ["Report (JSON)", "/api/builds/k/files/report.json"],
    ]);
    expect(screen.getByRole("link", { name: "Plans (PDF)" }).hasAttribute("download")).toBe(true);
    expect(await screen.findByRole("tab", { name: "Report (1 warning)" })).toBeTruthy();
  });

  it("says when a build has no model, and offers nothing to download", async () => {
    server.routes.set("GET /api/builds/k", () => json(build()));
    show(<BuildPanel buildKey="k" />);
    expect(await screen.findByText("This build has no 3D model.")).toBeTruthy();
    expect(screen.queryByText("Download:")).toBeNull();
  });

  it("moves between the drawings, the materials and the report, one tab at a time", async () => {
    let release = () => {};
    const files = ["report.json", "drawings/index.json"];
    server.routes.set("GET /api/builds/k", () => json(build({ files })));
    server.routes.set(
      "GET /api/builds/k/report",
      () => new Promise<Response>((resolve) => (release = () => resolve(json(report)))),
    );
    server.routes.set("GET /api/builds/k/files/drawings/index.json", () =>
      json([{ file: "front.svg", kind: "section", title: "Front section", description: "" }]),
    );
    show(<BuildPanel buildKey="k" />);
    fireEvent.click(await screen.findByRole("tab", { name: "Materials" }));
    expect(screen.getByRole("tabpanel", { name: "Materials" }).textContent).toBe("Loading the report…");
    release();
    expect(await screen.findByText("This design has no bill of materials.")).toBeTruthy();
    fireEvent.click(screen.getByRole("tab", { name: "Drawings" }));
    expect(await screen.findByRole("img", { name: "Front section" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "Drawings" }).getAttribute("aria-selected")).toBe("true");
    fireEvent.click(screen.getByRole("tab", { name: "Report (1 warning)" }));
    const panel = screen.getByRole("tabpanel", { name: "Report (1 warning)" });
    expect(within(panel).getByRole("heading", { name: "Heat loss" })).toBeTruthy();
    expect(screen.queryByRole("tab", { name: "Castables" })).toBeNull();
  });

  it("says a finished build without a report has none, instead of loading it forever", async () => {
    server.routes.set("GET /api/builds/k", () => json(build({ files: ["kiln.glb"] })));
    show(<BuildPanel buildKey="k" />);
    fireEvent.click(await screen.findByRole("tab", { name: "Materials" }));
    expect(screen.getByRole("tabpanel", { name: "Materials" }).textContent).toBe("This build has no report.");
  });

  it("has a tab for the castables when the design mixes its own", async () => {
    const mixed = {
      ...report,
      castables: [
        {
          mix: { id: "m", name: "My mix", batch: [], conductivity: [], working: [] },
          batches: 0,
          steps: [],
          schedule: [],
          layers: [],
          first_firing: [],
          findings: [],
        },
      ],
    };
    server.routes.set("GET /api/builds/k", () => json(build({ files: ["report.json"] })));
    server.routes.set("GET /api/builds/k/report", () => json(mixed));
    show(<BuildPanel buildKey="k" />);
    fireEvent.click(await screen.findByRole("tab", { name: "Castables" }));
    expect(screen.getByRole("region", { name: "My mix" })).toBeTruthy();
  });

  it("says why the report couldn't be loaded", async () => {
    server.routes.set("GET /api/builds/k", () => json(build({ files: ["report.json"] })));
    server.routes.set("GET /api/builds/k/report", () => json({ detail: "report.json is corrupt" }, 500));
    show(<BuildPanel buildKey="k" />);
    expect(await screen.findByText("The report could not be loaded: report.json is corrupt")).toBeTruthy();
  });
});

describe("Drawings", () => {
  const drawn = build({ files: ["drawings/index.json"] });

  it("says when a build has no drawings, without asking for them", () => {
    show(<Drawings build={build()} />);
    expect(screen.getByText("This build has no drawings.")).toBeTruthy();
    expect(server.log).toEqual([]);
  });

  it("shows the sections, then the charts, then every course plan", async () => {
    server.routes.set("GET /api/builds/k/files/drawings/index.json", () =>
      json([
        { file: "course-1.svg", kind: "course plan", title: "Course 1", description: "" },
        { file: "front.svg", kind: "section", title: "Front section", description: "Through the door" },
        { file: "temps.svg", kind: "chart", title: "Temperatures", description: "" },
        { file: "course 2.svg", kind: "course plan", title: "Course 2", description: "" },
      ]),
    );
    show(<Drawings build={drawn} />);
    expect(screen.getByText("Loading the drawings…")).toBeTruthy();
    const images = await screen.findAllByRole("img");
    expect(images.map((img) => [img.getAttribute("alt"), img.getAttribute("src")])).toEqual([
      ["Front section", "/api/builds/k/files/drawings/front.svg"],
      ["Temperatures", "/api/builds/k/files/drawings/temps.svg"],
      ["Course 1", "/api/builds/k/files/drawings/course-1.svg"],
      ["Course 2", "/api/builds/k/files/drawings/course%202.svg"],
    ]);
    const figure = screen.getByRole("img", { name: "Front section" }).closest("figure");
    expect(figure?.querySelector("figcaption")?.textContent).toBe("Front section Through the door");
    const plans = screen.getByRole("heading", { name: "Course plans" }).closest("section")!;
    const planned = within(plans).getAllByRole("img").map((img) => img.getAttribute("alt"));
    expect(planned).toEqual(["Course 1", "Course 2"]);
  });

  it("has no course plans when the build drew none", async () => {
    server.routes.set("GET /api/builds/k/files/drawings/index.json", () =>
      json([{ file: "front.svg", kind: "section", title: "Front section", description: "" }]),
    );
    show(<Drawings build={drawn} />);
    expect(await screen.findByRole("img", { name: "Front section" })).toBeTruthy();
    expect(screen.queryByRole("heading", { name: "Course plans" })).toBeNull();
  });

  it("says when the drawings couldn't be loaded", async () => {
    server.routes.set("GET /api/builds/k/files/drawings/index.json", () => new Response("", { status: 500 }));
    show(<Drawings build={drawn} />);
    expect(await screen.findByText("the drawings could not be loaded (500)")).toBeTruthy();
  });
});
