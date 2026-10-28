// The pages, through the app's own router at a URL, with the API stubbed at fetch.
import type { Build, Design, Library, Template } from "@kilndesigner/api-client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createMemoryHistory, RouterProvider } from "@tanstack/react-router";
import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { EditorView } from "@uiw/react-codemirror";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { KilnDocument, Layout } from "../design";

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
  const sent: Record<string, unknown> = {};
  const fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const request = new PageRequest(input, init);
    const route = `${request.method} ${new URL(request.url).pathname}`;
    log.push(route);
    if (request.method === "POST") sent[route] = await request.clone().json();
    const answer = routes.get(route);
    return answer ? answer(request) : new Response(null, { status: 404, statusText: "Not Found" });
  });
  vi.stubGlobal("Request", PageRequest);
  vi.stubGlobal("fetch", fetch);
  return { routes, log, sent };
});

// The model needs WebGL, which jsdom hasn't got: this stands in for it, showing the design it's
// given and handing the page a port moved on it
vi.mock("../components/KilnViewer", () => ({
  KilnViewer: (props: {
    layout?: Layout;
    draft?: KilnDocument | null;
    onEdit?: (apply: (document: KilnDocument) => KilnDocument) => void;
  }) => (
    <div>
      <p>
        The model of {props.draft?.name ?? "nothing"}, with {props.layout?.ports.length ?? "no"} ports
      </p>
      <button type="button" onClick={() => props.onEdit?.((d) => ({ ...d, name: `${d.name}, port moved` }))}>
        Move a port on the model
      </button>
    </div>
  ),
}));

// The router scrolls to the top on each navigation; jsdom has nothing to scroll and says so
window.scrollTo = () => {};

// CodeMirror runs in jsdom, but measures text with these, which jsdom hasn't got (it lays nothing out)
const noRect = { x: 0, y: 0, width: 0, height: 0, top: 0, right: 0, bottom: 0, left: 0, toJSON: () => ({}) };
Range.prototype.getClientRects = () => [] as unknown as DOMRectList;
Range.prototype.getBoundingClientRect = () => noRect as DOMRect;

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
  for (const key of Object.keys(server.sent)) delete server.sent[key];
  vi.restoreAllMocks();
});

/** The app at ``path``, as main.tsx starts it, with a router and a cache of its own. */
async function app(path: string) {
  vi.resetModules();
  const { router } = await import("../router");
  router.update({ ...router.options, history: createMemoryHistory({ initialEntries: [path] }) });
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  render(
    <QueryClientProvider client={client}>
      <RouterProvider router={router} />
    </QueryClientProvider>,
  );
  await screen.findByRole("main"); // the router shows the page once it has matched the URL
}

const library: Library = {
  materials: [
    { id: "ifb-k23", name: "K-23", kind: "insulating_firebrick", max_service: "2300 degF", density: "" },
  ],
  ingredients: [],
  alloys: [{ id: "kanthal-a1", name: "Kanthal A1" }],
  cones: ["6", "10"],
  cone_rates: { "6": [60, 150], "10": [60, 150] },
  burners: [],
};

const doc: KilnDocument = {
  name: "Test kiln",
  firing: { cone: "10" },
  chamber: { width: "22.5 in", depth: "22.5 in", height: "24 in" },
  lining: { walls: [{ material: "ifb-k23", thickness: "4.5 in" }] },
  heat: { electric: { supply: { voltage: "240 V", phase: 1, breaker: "60 A" } } },
};

const when = (day: number) => `2026-10-0${day}T12:00:00Z`;
const shownAt = (day: number) => new Date(when(day)).toLocaleString();

function designAt(number: number, over: Partial<KilnDocument> = {}): Design {
  const document = { ...doc, ...over };
  return {
    id: "d1",
    name: document.name,
    created_at: when(1),
    updated_at: when(number),
    versions: Array.from({ length: number }, (_, i) => ({
      number: i + 1,
      build_key: `b${i + 1}`,
      created_at: when(i + 1),
    })),
    latest: {
      number,
      build_key: `b${number}`,
      created_at: when(number),
      schema_version: 1,
      document: document as unknown as Record<string, unknown>,
      source: `name: ${document.name}\n`,
    },
  };
}

const build = (key: string, over: Partial<Build> = {}): Build => ({
  key,
  status: "done",
  files: [],
  notes: [],
  error: null,
  created_at: when(2),
  finished_at: when(2),
  ...over,
});

const layout = { units: "us", walls: {}, ports: [{ kind: "spy" }, { kind: "flue" }] } as unknown as Layout;

/** The API for design d1 at version 2, built, with a model and where it put the ports. */
function designD1() {
  server.routes.set("GET /api/designs/d1", () => json(designAt(2)));
  server.routes.set("GET /api/library", () => json(library));
  server.routes.set("GET /api/builds/b2", () => json(build("b2", { files: ["kiln.glb", "layout.json"] })));
  server.routes.set("GET /api/builds/b2/files/layout.json", () => json(layout));
}

const nameField = () => screen.findByLabelText("Name") as Promise<HTMLInputElement>;

function yaml(): EditorView {
  const view = EditorView.findFromDOM(document.querySelector<HTMLElement>(".cm-editor")!);
  if (!view) throw new Error("no YAML editor");
  return view;
}

const onTab = (name: "Choices" | "YAML") =>
  waitFor(() => expect(screen.getByRole("tab", { name }).getAttribute("aria-selected")).toBe("true"));

describe("the top bar", () => {
  it("is on every page, with the way home and the appearance menu", async () => {
    server.routes.set("GET /api/templates", () => json([]));
    server.routes.set("GET /api/designs", () => json([]));
    await app("/designs/new");
    expect(await screen.findByRole("heading", { name: "New design" })).toBeTruthy();
    expect(screen.getByRole("group", { name: "Appearance" })).toBeTruthy();
    fireEvent.click(screen.getByRole("link", { name: "Kilndesigner" }));
    expect(await screen.findByRole("heading", { name: "Designs" })).toBeTruthy();
  });

  it("stays above a page that failed, which says what happened and leads back", async () => {
    // React and the router both report the error they caught
    vi.spyOn(console, "error").mockImplementation(() => {});
    vi.spyOn(console, "warn").mockImplementation(() => {});
    server.routes.set("GET /api/designs/broken", () => json({ id: "broken", name: "Broken" }));
    server.routes.set("GET /api/designs", () => json([]));
    await app("/designs/broken");
    expect(await screen.findByRole("heading", { name: "This page could not be shown" })).toBeTruthy();
    expect(screen.getByText(/Cannot read properties of undefined/).className).toBe("error");
    expect(screen.getByRole("link", { name: "Kilndesigner" })).toBeTruthy();
    fireEvent.click(screen.getByRole("link", { name: "Back to the designs" }));
    expect(await screen.findByText("No designs yet. Start one from a design file (YAML).")).toBeTruthy();
  });
});

describe("DesignList", () => {
  it("lists each design with when it was changed, linking to it", async () => {
    designD1();
    server.routes.set("GET /api/designs", () =>
      json([
        { id: "d1", name: "Test kiln", created_at: when(1), updated_at: when(2) },
        { id: "d2", name: "Car kiln", created_at: when(1), updated_at: when(3) },
      ]),
    );
    await app("/");
    expect(screen.getByText("Loading…")).toBeTruthy();
    const list = await screen.findByRole("list");
    expect(within(list).getAllByRole("listitem").map((li) => li.textContent)).toEqual([
      `Test kiln${shownAt(2)}`,
      `Car kiln${shownAt(3)}`,
    ]);
    expect(list.querySelector("time")?.getAttribute("datetime")).toBe(when(2));
    expect(screen.getByRole("link", { name: "Car kiln" }).getAttribute("href")).toBe("/designs/d2");
    fireEvent.click(screen.getByRole("link", { name: "Test kiln" }));
    expect(await screen.findByRole("heading", { name: "Test kiln" })).toBeTruthy();
  });

  it("says when there are no designs yet, and starts a new one", async () => {
    server.routes.set("GET /api/designs", () => json([]));
    server.routes.set("GET /api/templates", () => json([]));
    await app("/");
    expect(await screen.findByText("No designs yet. Start one from a design file (YAML).")).toBeTruthy();
    fireEvent.click(screen.getByRole("link", { name: "New design" }));
    expect(await screen.findByRole("heading", { name: "New design" })).toBeTruthy();
  });

  it("says why the designs couldn't be listed", async () => {
    server.routes.set("GET /api/designs", () => json({ detail: "The database is down" }, 503));
    await app("/");
    expect(await screen.findByText("The database is down")).toBeTruthy();
  });
});

describe("DesignPage", () => {
  it("shows the design's latest version in the editor, its history, and its build's model", async () => {
    designD1();
    await app("/designs/d1");
    expect(screen.getByText("Loading…")).toBeTruthy();
    expect(await screen.findByRole("heading", { name: "Test kiln" })).toBeTruthy();
    expect((await nameField()).value).toBe("Test kiln");
    expect(screen.getByText("Version 2")).toBeTruthy();
    const history = screen.getByLabelText("Load an earlier version into the editor") as HTMLSelectElement;
    expect([...history.options].map((o) => o.textContent)).toEqual([
      "History…",
      `Version 2, ${shownAt(2)}`,
      `Version 1, ${shownAt(1)}`,
    ]);
    expect(await screen.findByText("The model of Test kiln, with 2 ports")).toBeTruthy();
  });

  it("says why a design can't be shown", async () => {
    server.routes.set("GET /api/designs/gone", () => json({ detail: "No design gone" }, 404));
    await app("/designs/gone");
    expect(await screen.findByText("No design gone")).toBeTruthy();
  });

  it("saves a new version and builds it", async () => {
    designD1();
    server.routes.set("POST /api/designs/d1/versions", () => json(designAt(3, { name: "Renamed" }), 201));
    server.routes.set("POST /api/builds/b3", () => json(build("b3", { status: "queued" }), 202));
    server.routes.set("GET /api/builds/b3", () => json(build("b3", { status: "queued" })));
    await app("/designs/d1");
    fireEvent.change(await nameField(), { target: { value: "Renamed" } });
    expect(screen.getByText("Version 2 · unsaved changes")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Save and build" }));
    expect(await screen.findByText("Version 3")).toBeTruthy();
    expect(await screen.findByText("Waiting for the worker…")).toBeTruthy();
    expect(server.sent["POST /api/designs/d1/versions"]).toEqual({ document: { ...doc, name: "Renamed" } });
    expect(server.log).toContain("POST /api/builds/b3");
    expect((await nameField()).value).toBe("Renamed");
    expect(screen.getByRole("heading", { name: "Renamed" })).toBeTruthy();
  });

  it("stays on the YAML tab through a save", async () => {
    designD1();
    server.routes.set("POST /api/designs/d1/versions", () => json(designAt(3, { name: "From YAML" }), 201));
    server.routes.set("POST /api/builds/b3", () => json(build("b3", { status: "queued" }), 202));
    server.routes.set("GET /api/builds/b3", () => json(build("b3", { status: "queued" })));
    await app("/designs/d1");
    await nameField();
    fireEvent.click(screen.getByRole("tab", { name: "YAML" }));
    const view = yaml();
    const insert = "name: From YAML\n";
    act(() => view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert } }));
    fireEvent.click(screen.getByRole("button", { name: "Save and build" }));
    expect(await screen.findByText("Version 3")).toBeTruthy();
    expect(server.sent["POST /api/designs/d1/versions"]).toEqual({ source: "name: From YAML\n" });
    await onTab("YAML");
    expect(yaml().state.doc.toString()).toBe("name: From YAML\n");
  });

  it("shows why a version was refused", async () => {
    designD1();
    const problems = [{ loc: ["chamber", "width"], msg: "Too narrow" }];
    server.routes.set("POST /api/designs/d1/versions", () => json({ detail: problems }, 422));
    await app("/designs/d1");
    fireEvent.change(await nameField(), { target: { value: "Renamed" } });
    fireEvent.click(screen.getByRole("button", { name: "Save and build" }));
    expect((await screen.findByRole("alert")).textContent).toBe("chamber.width Too narrow");
    expect(screen.getByText("Version 2 · unsaved changes")).toBeTruthy();
  });

  it("loads an earlier version into the editor, to save as the latest", async () => {
    designD1();
    const old = designAt(1, { name: "First try" }).latest;
    server.routes.set("GET /api/designs/d1/versions/1", () => json(old));
    await app("/designs/d1");
    await nameField();
    const history = screen.getByLabelText("Load an earlier version into the editor") as HTMLSelectElement;
    fireEvent.change(history, { target: { value: "1" } });
    await waitFor(async () => expect((await nameField()).value).toBe("First try"));
    expect(screen.getByText("Version 2 · unsaved changes")).toBeTruthy();
    expect(history.value).toBe("");
  });

  it("takes in a port moved on the model, and shows the model the design as edited", async () => {
    designD1();
    await app("/designs/d1");
    await nameField();
    fireEvent.click(await screen.findByRole("button", { name: "Move a port on the model" }));
    expect((await nameField()).value).toBe("Test kiln, port moved");
    expect(screen.getByText("Version 2 · unsaved changes")).toBeTruthy();
    expect(screen.getByText("The model of Test kiln, port moved, with 2 ports")).toBeTruthy();
  });
});

const templates: Template[] = [
  {
    id: "electric",
    title: "Electric",
    description: "A front-loading electric kiln",
    document: doc as unknown as Record<string, unknown>,
    source: "name: Test kiln\n",
  },
  {
    id: "gas",
    title: "Gas",
    description: "A sprung-arch gas kiln",
    document: { ...doc, name: "Gas kiln" } as unknown as Record<string, unknown>,
    source: "name: Gas kiln\n",
  },
];

/** The API taking a new design, d1, and starting its build. */
function created() {
  designD1();
  server.routes.set("GET /api/templates", () => json(templates));
  server.routes.set("POST /api/designs", () => json(designAt(2), 201));
  server.routes.set("POST /api/builds/b2", () => json(build("b2", { status: "queued" }), 202));
  server.routes.set("GET /api/builds/b2", () => json(build("b2", { status: "queued" })));
}

describe("NewDesign", () => {
  it("starts from a kind of kiln, then saves it, builds it and opens it", async () => {
    created();
    await app("/designs/new");
    expect(screen.getByText("Loading…")).toBeTruthy();
    const gas = await screen.findByRole("button", { name: /^Gas/ });
    expect(gas.textContent).toBe("GasA sprung-arch gas kiln");
    fireEvent.click(screen.getByRole("button", { name: /^Electric/ }));
    expect(screen.getByRole("button", { name: /^Electric/ }).getAttribute("aria-pressed")).toBe("true");
    expect(gas.getAttribute("aria-pressed")).toBe("false");
    expect((await nameField()).value).toBe("Test kiln");
    fireEvent.click(screen.getByRole("button", { name: "Save and build" }));
    expect(await screen.findByRole("heading", { name: "Test kiln" })).toBeTruthy();
    expect(await screen.findByText("Waiting for the worker…")).toBeTruthy();
    expect(server.sent["POST /api/designs"]).toEqual({ document: doc });
    expect(server.log).toContain("POST /api/builds/b2");
  });

  it("says why the kinds of kiln couldn't be loaded", async () => {
    server.routes.set("GET /api/templates", () => json({ detail: "No templates" }, 500));
    await app("/designs/new");
    expect(await screen.findByText("No templates")).toBeTruthy();
  });

  it("opens a design file in the YAML tab, as it is, and saves it as it is", async () => {
    created();
    server.routes.set("POST /api/designs/check", () => json({ document: doc, source: "name: Test kiln\n" }));
    await app("/designs/new");
    const file = new File(["name: Test kiln # mine\n"], "kiln.yaml", { type: "application/yaml" });
    fireEvent.change(screen.getByLabelText("Open a design file…"), { target: { files: [file] } });
    await onTab("YAML");
    expect(yaml().state.doc.toString()).toBe("name: Test kiln # mine\n");
    expect(server.sent["POST /api/designs/check"]).toEqual({ source: "name: Test kiln # mine\n" });
    fireEvent.click(screen.getByRole("button", { name: "Save and build" }));
    expect(await screen.findByRole("heading", { name: "Test kiln" })).toBeTruthy();
    expect(server.sent["POST /api/designs"]).toEqual({ source: "name: Test kiln # mine\n" });
  });

  it("opens a design file that isn't valid as it is, and saving it says what's wrong", async () => {
    created();
    const problems = [{ loc: ["chamber"], msg: "Field required" }];
    server.routes.set("POST /api/designs/check", () => json({ detail: problems }, 422));
    server.routes.set("POST /api/designs", () => json({ detail: problems }, 422));
    await app("/designs/new");
    const file = new File(["name: Half done\n"], "half.yml");
    fireEvent.change(screen.getByLabelText("Open a design file…"), { target: { files: [file] } });
    await onTab("YAML");
    expect(yaml().state.doc.toString()).toBe("name: Half done\n");
    expect(screen.queryByRole("alert")).toBeNull();
    fireEvent.click(screen.getByRole("button", { name: "Save and build" }));
    expect((await screen.findByRole("alert")).textContent).toBe("chamber Field required");
    expect(server.sent["POST /api/designs"]).toEqual({ source: "name: Half done\n" });
    expect(screen.getByRole("heading", { name: "New design" })).toBeTruthy();
  });

  it("opens nothing when no file is chosen", async () => {
    server.routes.set("GET /api/templates", () => json(templates));
    await app("/designs/new");
    await screen.findByRole("button", { name: /^Electric/ });
    fireEvent.change(screen.getByLabelText("Open a design file…"), { target: { files: [] } });
    expect(screen.queryByRole("button", { name: "Save and build" })).toBeNull();
    expect(server.log).not.toContain("POST /api/designs/check");
  });
});
