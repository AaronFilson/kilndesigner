import type { Library } from "@kilndesigner/api-client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { EditorView } from "@uiw/react-codemirror";
import { afterEach, describe, expect, it, vi } from "vitest";

import { ApiError, type DesignInput } from "../api";
import type { KilnDocument, Layout } from "../design";
import { DesignEditor, type Draft, type Edit, type Mode } from "./DesignEditor";
import { YamlEditor } from "./YamlEditor";

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
});

/** The YAML editor on the page, as CodeMirror holds it. */
function yaml(): EditorView {
  const view = EditorView.findFromDOM(document.querySelector<HTMLElement>(".cm-editor")!);
  if (!view) throw new Error("no YAML editor");
  return view;
}

function typeYaml(text: string) {
  const view = yaml();
  act(() => view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: text } }));
}

describe("YamlEditor", () => {
  it("shows the design file and reports each edit", () => {
    const onChange = vi.fn<(value: string) => void>();
    render(<YamlEditor value={"name: Test\n"} onChange={onChange} />);
    const shown = screen.getByLabelText("Design file (YAML)").querySelector(".cm-content");
    expect(shown?.textContent).toBe("name: Test");
    typeYaml("name: Other\n");
    expect(onChange).toHaveBeenLastCalledWith("name: Other\n", expect.anything());
  });
});

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
  name: "Test",
  firing: { cone: "10" },
  chamber: { width: "22.5 in", depth: "22.5 in", height: "24 in" },
  lining: { walls: [{ material: "ifb-k23", thickness: "4.5 in" }] },
  heat: { electric: { supply: { voltage: "240 V", phase: 1, breaker: "60 A" } } },
};
const saved: Draft = { document: doc, source: "name: Test\n" };

interface Options {
  initial?: Draft;
  baseline?: Draft | null;
  mode?: Mode;
  saving?: boolean;
  saveError?: unknown;
  layout?: Layout;
  edit?: Edit | null;
}

function editor(options: Options = {}) {
  if (!server.routes.has("GET /api/library")) server.routes.set("GET /api/library", () => json(library));
  const onSave = vi.fn<(input: DesignInput) => void>();
  const onModeChange = vi.fn<(mode: Mode) => void>();
  const onDocument = vi.fn<(document: KilnDocument) => void>();
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  const ui = (o: Options) => (
    <QueryClientProvider client={client}>
      <DesignEditor
        initial={o.initial ?? saved}
        baseline={o.baseline === undefined ? saved : o.baseline}
        mode={o.mode}
        onModeChange={onModeChange}
        toolbar={(changed) => <span>{changed ? "Unsaved changes" : "Saved"}</span>}
        saving={o.saving ?? false}
        saveError={o.saveError ?? null}
        onSave={onSave}
        layout={o.layout}
        edit={o.edit}
        onDocument={onDocument}
      />
    </QueryClientProvider>
  );
  const { rerender } = render(ui(options));
  return { onSave, onModeChange, onDocument, rerender: (o: Options) => rerender(ui({ ...options, ...o })) };
}

const save = () => screen.getByRole("button", { name: "Save and build" }) as HTMLButtonElement;
const tab = (name: "Choices" | "YAML") => screen.getByRole("tab", { name }) as HTMLButtonElement;
const nameField = () => screen.findByLabelText("Name") as Promise<HTMLInputElement>;

/** Answers the check the editor asks for on switching, and keeps what it was sent. */
function checks(answer: (sent: DesignInput) => Response | Promise<Response>) {
  const sent: DesignInput[] = [];
  server.routes.set("POST /api/designs/check", async (request) => {
    const input = (await request.json()) as DesignInput;
    sent.push(input);
    return answer(input);
  });
  return sent;
}

describe("DesignEditor", () => {
  it("loads the choices, then shows the design in the form", async () => {
    editor();
    expect(screen.getByText("Loading the choices…")).toBeTruthy();
    expect((await nameField()).value).toBe("Test");
    expect(tab("Choices").getAttribute("aria-selected")).toBe("true");
  });

  it("says why the choices couldn't be loaded", async () => {
    server.routes.set("GET /api/library", () => json({ detail: "The library is missing" }, 500));
    editor();
    expect(await screen.findByText("The choices could not be loaded: The library is missing")).toBeTruthy();
  });

  it("saves the form's design once it differs from the saved one", async () => {
    const { onSave } = editor();
    fireEvent.change(await nameField(), { target: { value: "Renamed" } });
    expect(save().disabled).toBe(false);
    expect(screen.getByText("Unsaved changes")).toBeTruthy();
    fireEvent.click(save());
    expect(onSave).toHaveBeenCalledWith({ document: { ...doc, name: "Renamed" } });
  });

  it("can't save an unchanged design, or while it's saving", async () => {
    const { rerender } = editor();
    await nameField();
    expect(save().disabled).toBe(true);
    expect(screen.getByText("Saved")).toBeTruthy();
    rerender({ baseline: null, saving: true });
    expect(save().disabled).toBe(true);
  });

  it("can save a new design as it is", async () => {
    const { onSave } = editor({ baseline: null });
    await nameField();
    expect(screen.getByText("Unsaved changes")).toBeTruthy();
    fireEvent.click(save());
    expect(onSave).toHaveBeenCalledWith({ document: doc });
  });

  it("shows the YAML as it was when nothing has changed, without asking the API", async () => {
    const { onModeChange } = editor();
    await nameField();
    fireEvent.click(tab("YAML"));
    expect(yaml().state.doc.toString()).toBe("name: Test\n");
    expect(tab("YAML").getAttribute("aria-selected")).toBe("true");
    expect(onModeChange).toHaveBeenCalledWith("yaml");
    fireEvent.click(tab("YAML")); // already there
    expect(onModeChange).toHaveBeenCalledTimes(1);
    expect(server.log).toEqual(["GET /api/library"]);
  });

  it("has the API check the form's changes, then shows them as YAML", async () => {
    let answer = (_: Response) => {};
    const sent = checks(() => new Promise<Response>((resolve) => (answer = resolve)));
    editor();
    fireEvent.change(await nameField(), { target: { value: "Renamed" } });
    fireEvent.click(tab("YAML"));
    // Nothing can be saved or switched while the API checks it
    expect([tab("Choices").disabled, tab("YAML").disabled, save().disabled]).toEqual([true, true, true]);
    await waitFor(() => expect(sent).toEqual([{ document: { ...doc, name: "Renamed" } }]));
    answer(json({ document: { ...doc, name: "Renamed" }, source: "name: Renamed\n" }));
    await waitFor(() => expect(tab("YAML").getAttribute("aria-selected")).toBe("true"));
    expect(yaml().state.doc.toString()).toBe("name: Renamed\n");
  });

  it("saves the YAML, changed when it differs from the saved file", async () => {
    const { onSave } = editor({ mode: "yaml" });
    expect(save().disabled).toBe(true);
    typeYaml("name: Edited\n");
    expect(save().disabled).toBe(false);
    fireEvent.click(save());
    expect(onSave).toHaveBeenCalledWith({ source: "name: Edited\n" });
  });

  it("won't leave YAML that isn't valid, and says where it's wrong", async () => {
    checks(() => json({ detail: [{ loc: ["chamber", "width"], msg: "Field required" }] }, 422));
    const { onModeChange } = editor({ mode: "yaml" });
    typeYaml("name: Edited\n");
    fireEvent.click(tab("Choices"));
    expect((await screen.findByRole("alert")).textContent).toBe("chamber.width Field required");
    expect(tab("YAML").getAttribute("aria-selected")).toBe("true");
    expect(onModeChange).not.toHaveBeenCalled();
  });

  it("says what went wrong when the check fails for another reason", async () => {
    checks(() => json({ detail: "That isn't YAML" }, 400));
    editor({ mode: "yaml" });
    typeYaml(": : :");
    fireEvent.click(tab("Choices"));
    expect(await screen.findByText("That isn't YAML")).toBeTruthy();
    checks(() => {
      throw new TypeError("Failed to fetch");
    });
    fireEvent.click(tab("Choices"));
    expect(await screen.findByText("Failed to fetch")).toBeTruthy();
    expect(screen.queryByText("That isn't YAML")).toBeNull();
  });

  it("shows the checked YAML's design in the form", async () => {
    const sent = checks(() => json({ document: { ...doc, name: "From YAML" }, source: "name: From YAML\n" }));
    const { onModeChange, onDocument } = editor({ mode: "yaml" });
    typeYaml("name: From YAML\n");
    fireEvent.click(tab("Choices"));
    expect((await nameField()).value).toBe("From YAML");
    expect(sent).toEqual([{ source: "name: From YAML\n" }]);
    expect(onModeChange).toHaveBeenCalledWith("form");
    expect(onDocument).toHaveBeenLastCalledWith({ ...doc, name: "From YAML" });
  });

  it("shows why a save was refused", async () => {
    const problems = [{ loc: ["lining", "walls", 0, "thickness"], msg: "Too thin" }];
    const { rerender } = editor({ saveError: new ApiError(422, "The design is not valid", problems) });
    expect(screen.getByRole("alert").textContent).toBe("lining.walls[0].thickness Too thin");
    expect(screen.queryByText("The design is not valid")).toBeNull();
    rerender({ saveError: new ApiError(500, "Internal Server Error") });
    expect(screen.getByText("Internal Server Error")).toBeTruthy();
    rerender({ saveError: "the network went away" });
    expect(screen.getByText("the network went away")).toBeTruthy();
  });

  it("gives the form where the last build put the ports", async () => {
    const layout = { units: "us", walls: {}, ports: [] } as unknown as Layout;
    editor({ layout });
    await nameField();
    const placed = screen.getByRole("option", { name: "Each where it's placed" }) as HTMLOptionElement;
    expect(placed.disabled).toBe(false);
  });
});

describe("DesignEditor, a change made on the model", () => {
  const rename = (to: string) => (d: KilnDocument) => ({ ...d, name: `${d.name} ${to}` });

  it("is applied once, and the page is told the new design", async () => {
    const edit: Edit = { id: Date.now() + 1000, apply: rename("moved") };
    const { onDocument, rerender } = editor({ edit });
    expect((await nameField()).value).toBe("Test moved");
    expect(onDocument).toHaveBeenLastCalledWith({ ...doc, name: "Test moved" });
    expect(screen.getByText("Unsaved changes")).toBeTruthy();
    rerender({ edit, saving: true });
    expect((await nameField()).value).toBe("Test moved");
  });

  it("is passed by when it was made before the editor started", async () => {
    editor({ edit: { id: 0, apply: rename("moved") } });
    expect((await nameField()).value).toBe("Test");
  });

  it("takes the YAML tab back to the form to show it", async () => {
    const edit: Edit = { id: Date.now() + 1000, apply: rename("moved") };
    const { onModeChange } = editor({ mode: "yaml", edit });
    expect((await nameField()).value).toBe("Test moved");
    expect(tab("Choices").getAttribute("aria-selected")).toBe("true");
    expect(onModeChange).toHaveBeenCalledWith("form");
    expect(server.log).not.toContain("POST /api/designs/check");
  });

  it("checks YAML that was edited first, and waits if it isn't valid", async () => {
    checks(() => json({ detail: [{ loc: ["name"], msg: "Field required" }] }, 422));
    const { rerender } = editor({ mode: "yaml" });
    typeYaml("nom: Test\n");
    rerender({ edit: { id: Date.now() + 1000, apply: rename("moved") } });
    expect((await screen.findByRole("alert")).textContent).toBe("name Field required");
    expect(tab("YAML").getAttribute("aria-selected")).toBe("true");
    expect(server.log.filter((r) => r === "POST /api/designs/check")).toHaveLength(1);
  });
});
