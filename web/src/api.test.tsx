import type { Build, Design, Report } from "@kilndesigner/api-client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { act, cleanup, renderHook, waitFor } from "@testing-library/react";
import type { ReactNode } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  ApiError,
  checkDesign,
  fileUrl,
  useBuild,
  useCreateDesign,
  useDeleteDesign,
  useDesign,
  useDesigns,
  useLayout,
  useLibrary,
  useReport,
  useSaveVersion,
  useStartBuild,
  useTemplates,
} from "./api";
import type { KilnDocument, Layout } from "./design";

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
  vi.useRealTimers();
});

function setup() {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  const wrapper = ({ children }: { children: ReactNode }) => (
    <QueryClientProvider client={client}>{children}</QueryClientProvider>
  );
  return { client, wrapper };
}

const doc: KilnDocument = {
  name: "Test",
  firing: { cone: "10" },
  chamber: { width: "22.5 in", depth: "22.5 in", height: "24 in" },
  lining: { walls: [{ material: "ifb-k23", thickness: "4.5 in" }] },
  heat: { electric: { supply: { voltage: "240 V", phase: 1, breaker: "60 A" } } },
};

const design: Design = {
  id: "d1",
  name: "Test",
  created_at: "2026-10-01T12:00:00Z",
  updated_at: "2026-10-02T12:00:00Z",
  versions: [{ number: 1, build_key: "b1", created_at: "2026-10-01T12:00:00Z" }],
  latest: {
    number: 1,
    build_key: "b1",
    created_at: "2026-10-01T12:00:00Z",
    schema_version: 1,
    document: doc as unknown as Record<string, unknown>,
    source: "name: Test\n",
  },
};

const build = (over: Partial<Build> = {}): Build => ({
  key: "k",
  status: "done",
  files: [],
  notes: [],
  error: null,
  created_at: "2026-10-01T12:00:00Z",
  finished_at: null,
  ...over,
});

describe("fileUrl", () => {
  it("points at a build's file, escaping each part of its path but not the slashes", () => {
    expect(fileUrl("abc", "plans.pdf")).toBe("/api/builds/abc/files/plans.pdf");
    expect(fileUrl("abc", "drawings/course 1#.svg")).toBe("/api/builds/abc/files/drawings/course%201%23.svg");
  });
});

describe("checkDesign", () => {
  it("sends the YAML or the document, and gives the design back both ways", async () => {
    const sent: unknown[] = [];
    server.routes.set("POST /api/designs/check", async (request) => {
      sent.push(await request.json());
      return json({ document: doc, source: "name: Test\n" });
    });
    expect(await checkDesign({ source: "name: Test" })).toEqual({ document: doc, source: "name: Test\n" });
    await checkDesign({ document: doc });
    expect(sent).toEqual([{ source: "name: Test" }, { document: doc }]);
  });

  it("refuses a design that isn't valid with the problems, and where each is", async () => {
    const problems = [{ loc: ["chamber", "width"], msg: "Field required" }];
    server.routes.set("POST /api/designs/check", () =>
      json({ detail: problems }, 422, "Unprocessable Content"),
    );
    const error = await checkDesign({ source: "name: Test" }).catch((e: unknown) => e);
    expect(error).toBeInstanceOf(ApiError);
    expect(error).toMatchObject({ status: 422, message: "The design is not valid", problems });
  });

  it("says what the API said went wrong, or else the status", async () => {
    server.routes.set("POST /api/designs/check", () =>
      json({ detail: "Schema 9 is newer than this API" }, 400),
    );
    await expect(checkDesign({ source: "" })).rejects.toMatchObject({
      status: 400,
      message: "Schema 9 is newer than this API",
      problems: [],
    });
    server.routes.set("POST /api/designs/check", () =>
      new Response("<html>upstream down</html>", { status: 502, statusText: "Bad Gateway" }),
    );
    await expect(checkDesign({ source: "" })).rejects.toMatchObject({ status: 502, message: "Bad Gateway" });
  });
});

/** Every query that reads: the templates, the library, the designs and one design. */
const useReading = (id: string) => ({
  templates: useTemplates(),
  library: useLibrary(),
  designs: useDesigns(),
  design: useDesign(id),
});

describe("reading", () => {
  it("fetches the templates, the library, the designs and one design", async () => {
    const template = { id: "electric", title: "Electric", description: "", document: {}, source: "" };
    const library = { materials: [], ingredients: [], alloys: [], cones: ["6"], cone_rates: {}, burners: [] };
    server.routes.set("GET /api/templates", () => json([template]));
    server.routes.set("GET /api/library", () => json(library));
    server.routes.set("GET /api/designs", () => json([{ id: "d1", name: "Test" }]));
    server.routes.set("GET /api/designs/d1", () => json(design));
    const { wrapper } = setup();
    const { result } = renderHook(() => useReading("d1"), { wrapper });
    await waitFor(() => expect(Object.values(result.current).every((q) => q.isSuccess)).toBe(true));
    expect(result.current.templates.data).toEqual([template]);
    expect(result.current.library.data).toEqual(library);
    expect(result.current.designs.data).toEqual([{ id: "d1", name: "Test" }]);
    expect(result.current.design.data).toEqual(design);
  });

  it("is an ApiError, with the status, when the API won't answer", async () => {
    const { wrapper } = setup();
    const { result } = renderHook(() => useReading("gone"), { wrapper });
    await waitFor(() => expect(Object.values(result.current).every((q) => q.isError)).toBe(true));
    for (const query of Object.values(result.current)) {
      expect(query.error).toBeInstanceOf(ApiError);
      expect(query.error).toMatchObject({ status: 404, message: "Not Found" });
    }
    expect(server.log).toContain("GET /api/designs/gone");
  });
});

describe("saving", () => {
  it("creates a design, keeps it, and refreshes the list but no other design", async () => {
    let sent: unknown;
    server.routes.set("POST /api/designs", async (request) => {
      sent = await request.json();
      return json(design, 201, "Created");
    });
    const { client, wrapper } = setup();
    client.setQueryData(["designs"], []);
    client.setQueryData(["designs", "other"], { ...design, id: "other" });
    const { result } = renderHook(() => useCreateDesign(), { wrapper });
    await act(() => result.current.mutateAsync({ source: "name: Test\n" }));
    expect(sent).toEqual({ source: "name: Test\n" });
    expect(client.getQueryData(["designs", "d1"])).toEqual(design);
    expect(client.getQueryState(["designs"])?.isInvalidated).toBe(true);
    expect(client.getQueryState(["designs", "other"])?.isInvalidated).toBe(false);
  });

  it("saves a new version of a design and keeps it as the design", async () => {
    let sent: unknown;
    const saved = { ...design, latest: { ...design.latest, number: 2, build_key: "b2" } };
    server.routes.set("POST /api/designs/d1/versions", async (request) => {
      sent = await request.json();
      return json(saved, 201);
    });
    const { client, wrapper } = setup();
    client.setQueryData(["designs"], []);
    const { result } = renderHook(() => useSaveVersion("d1"), { wrapper });
    await act(() => result.current.mutateAsync({ document: doc }));
    expect(sent).toEqual({ document: doc });
    expect(client.getQueryData(["designs", "d1"])).toEqual(saved);
    expect(client.getQueryState(["designs"])?.isInvalidated).toBe(true);
  });

  it("refuses a design that isn't valid, and keeps what was there", async () => {
    const problems = [{ loc: ["firing"], msg: "Give a cone or a top temperature" }];
    server.routes.set("POST /api/designs", () => json({ detail: problems }, 422));
    server.routes.set("POST /api/designs/d1/versions", () => json({ detail: problems }, 422));
    const { client, wrapper } = setup();
    client.setQueryData(["designs", "d1"], design);
    const { result } = renderHook(() => ({ create: useCreateDesign(), save: useSaveVersion("d1") }), {
      wrapper,
    });
    await act(async () => {
      await result.current.create.mutateAsync({ source: "" }).catch(() => undefined);
      await result.current.save.mutateAsync({ source: "" }).catch(() => undefined);
    });
    await waitFor(() => expect(result.current.create.error).toMatchObject({ status: 422, problems }));
    await waitFor(() => expect(result.current.save.error).toMatchObject({ status: 422, problems }));
    expect(client.getQueryData(["designs", "d1"])).toEqual(design);
  });

  it("deletes a design and refreshes every design query", async () => {
    server.routes.set("DELETE /api/designs/d1", () => new Response(null, { status: 204 }));
    const { client, wrapper } = setup();
    client.setQueryData(["designs"], []);
    client.setQueryData(["designs", "d1"], design);
    const { result } = renderHook(() => useDeleteDesign(), { wrapper });
    await act(() => result.current.mutateAsync("d1"));
    expect(server.log).toEqual(["DELETE /api/designs/d1"]);
    expect(client.getQueryState(["designs"])?.isInvalidated).toBe(true);
    expect(client.getQueryState(["designs", "d1"])?.isInvalidated).toBe(true);
  });

  it("says why a design couldn't be deleted", async () => {
    server.routes.set("DELETE /api/designs/d1", () => json({ detail: "Design d1 not found" }, 404));
    const { wrapper } = setup();
    const { result } = renderHook(() => useDeleteDesign(), { wrapper });
    await act(() => result.current.mutateAsync("d1").catch(() => undefined));
    await waitFor(() =>
      expect(result.current.error).toMatchObject({ status: 404, message: "Design d1 not found" }),
    );
  });
});

describe("builds", () => {
  it("is null for a build that hasn't been started, and doesn't poll it", async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    const { wrapper } = setup();
    const { result } = renderHook(() => useBuild("k"), { wrapper });
    await waitFor(() => expect(result.current.isSuccess).toBe(true));
    expect(result.current.data).toBeNull();
    await act(() => vi.advanceTimersByTimeAsync(5000));
    expect(server.log).toEqual(["GET /api/builds/k"]);
  });

  it("polls a build each second while it runs, and stops when it's done", async () => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
    const states: Build["status"][] = ["queued", "running", "done"];
    server.routes.set("GET /api/builds/k", () => json(build({ status: states.shift() ?? "done" })));
    const { wrapper } = setup();
    const { result } = renderHook(() => useBuild("k"), { wrapper });
    await waitFor(() => expect(result.current.data?.status).toBe("queued"));
    await act(() => vi.advanceTimersByTimeAsync(1000));
    await waitFor(() => expect(result.current.data?.status).toBe("running"));
    await act(() => vi.advanceTimersByTimeAsync(1000));
    await waitFor(() => expect(result.current.data?.status).toBe("done"));
    await act(() => vi.advanceTimersByTimeAsync(5000));
    expect(server.log).toHaveLength(3);
  });

  it("doesn't ask until it's enabled", () => {
    const { wrapper } = setup();
    const { result } = renderHook(() => useBuild("k", false), { wrapper });
    expect(result.current.fetchStatus).toBe("idle");
    expect(server.log).toEqual([]);
  });

  it("is an error when the build can't be read", async () => {
    server.routes.set("GET /api/builds/k", () => json({ detail: "The queue is down" }, 503));
    const { wrapper } = setup();
    const { result } = renderHook(() => useBuild("k"), { wrapper });
    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.error).toMatchObject({ status: 503, message: "The queue is down" });
  });

  it("starts a build and keeps what the API says of it", async () => {
    server.routes.set("POST /api/builds/k", () => json(build({ status: "queued" }), 202));
    const { client, wrapper } = setup();
    const { result } = renderHook(() => useStartBuild(), { wrapper });
    await act(() => result.current.mutateAsync("k"));
    expect(client.getQueryData(["builds", "k"])).toEqual(build({ status: "queued" }));
  });

  it("says why a build couldn't be started", async () => {
    server.routes.set("POST /api/builds/k", () => json({ detail: "Already building" }, 409));
    const { wrapper } = setup();
    const { result } = renderHook(() => useStartBuild(), { wrapper });
    await act(() => result.current.mutateAsync("k").catch(() => undefined));
    await waitFor(() =>
      expect(result.current.error).toMatchObject({ status: 409, message: "Already building" }),
    );
  });
});

const layout: Layout = {
  units: "us",
  walls: {} as Layout["walls"],
  ports: [],
};

describe("useLayout", () => {
  it("waits for a finished build that has a layout", () => {
    const { wrapper } = setup();
    for (const waiting of [
      undefined,
      null,
      build({ status: "running", files: ["layout.json"] }),
      build({ status: "done", files: ["kiln.glb"] }),
    ]) {
      const { result } = renderHook(() => useLayout(waiting), { wrapper });
      expect(result.current.fetchStatus).toBe("idle");
    }
    expect(server.log).toEqual([]);
  });

  it("reads the layout a finished build wrote", async () => {
    server.routes.set("GET /api/builds/k/files/layout.json", () => json(layout));
    const { wrapper } = setup();
    const { result } = renderHook(() => useLayout(build({ files: ["layout.json"] })), { wrapper });
    await waitFor(() => expect(result.current.data).toEqual(layout));
  });

  it("is an ApiError when the layout can't be fetched", async () => {
    const { wrapper } = setup();
    const { result } = renderHook(() => useLayout(build({ files: ["layout.json"] })), { wrapper });
    await waitFor(() => expect(result.current.isError).toBe(true));
    expect(result.current.error).toBeInstanceOf(ApiError);
    expect(result.current.error).toMatchObject({ status: 404, message: "Not Found" });
  });
});

describe("useReport", () => {
  const report = { name: "Test", findings: [] } as unknown as Report;

  it("waits for a finished build that has a report", () => {
    const { wrapper } = setup();
    for (const waiting of [
      build({ status: "running", files: ["report.json"] }),
      build({ status: "done", files: ["kiln.glb"] }),
    ]) {
      const { result } = renderHook(() => useReport(waiting), { wrapper });
      expect(result.current.fetchStatus).toBe("idle");
    }
    expect(server.log).toEqual([]);
  });

  it("reads a finished build's report, or says why it can't", async () => {
    server.routes.set("GET /api/builds/k/report", () => json(report));
    const { wrapper } = setup();
    const { result } = renderHook(() => useReport(build({ files: ["report.json"] })), { wrapper });
    await waitFor(() => expect(result.current.data).toEqual(report));
    const gone = renderHook(() => useReport(build({ key: "gone", files: ["report.json"] })), { wrapper });
    await waitFor(() => expect(gone.result.current.isError).toBe(true));
    expect(gone.result.current.error).toMatchObject({ status: 404, message: "Not Found" });
  });
});
