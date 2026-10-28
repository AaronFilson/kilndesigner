// The viewer's toolbar, legend and messages. jsdom can't draw WebGL, so the Canvas is a stand-in
// that draws none of the 3D scene: it shows only stand-ins for the port markers and the orbit
// controls, whose callbacks and settings the toolbar drives. The model's loader is mocked too.
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { Children, isValidElement, type ReactNode, useEffect } from "react";
import { BoxGeometry, Color, Group, Mesh, MeshBasicMaterial, MeshStandardMaterial } from "three";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { KilnDocument, Layout, WallFrame } from "../design";
import { KilnViewer } from "./KilnViewer";
import type { Marker } from "./PortMarkers";

const IN = 25.4;

const stage = vi.hoisted(() => ({
  /** The Canvas throws, as React Three Fiber does where there's no WebGL. */
  fails: false,
  gl: { localClippingEnabled: false },
  load: vi.fn<(url: string) => Promise<{ scene: unknown }>>(),
}));

/** Rendered by the stand-in Canvas, as page elements; everything else in it is left out. */
const { inPage } = vi.hoisted(() => ({
  inPage: <P,>(component: (props: P) => ReactNode) => Object.assign(component, { inPage: true }),
}));

vi.mock("@react-three/fiber", async (importOriginal) => ({
  ...(await importOriginal<object>()),
  Canvas: ({
    children,
    onCreated,
    onPointerMissed,
  }: {
    children?: ReactNode;
    onCreated?: (state: { gl: typeof stage.gl }) => void;
    onPointerMissed?: () => void;
  }) => {
    if (stage.fails) throw new Error("Error creating WebGL context.");
    useEffect(() => onCreated?.({ gl: stage.gl }), [onCreated]);
    const shown = Children.toArray(children).filter(
      (child) => isValidElement(child) && (child.type as { inPage?: boolean }).inPage,
    );
    return (
      <div>
        <button type="button" onClick={() => onPointerMissed?.()}>
          Click off the model
        </button>
        {shown}
      </div>
    );
  },
}));

vi.mock("@react-three/drei", () => ({
  Bounds: () => null,
  useBounds: () => null,
  OrbitControls: inPage(({ enableRotate }: { enableRotate?: boolean }) => (
    <p>Turning {enableRotate ? "on" : "off"}</p>
  )),
}));

vi.mock("three/addons/loaders/GLTFLoader.js", () => ({
  GLTFLoader: class {
    loadAsync(url: string) {
      return stage.load(url);
    }
  },
}));

type Spot = { wall: Marker["wall"]; across: number; up: number };

vi.mock("./PortMarkers", async (importOriginal) => ({
  ...(await importOriginal<object>()),
  PortMarkers: inPage(
    (props: {
      all: Marker[];
      picked: string | null;
      adding: boolean;
      onDrop: (marker: Marker, all: Marker[], to: Spot) => void;
      onPick: (key: string) => void;
      onAdd: (to: Spot) => void;
      onHover: (text: string | null) => void;
    }) => (
      <div aria-label="Markers" role="group">
        <p>
          adding: {String(props.adding)}, picked: {props.picked ?? "none"}
        </p>
        {props.all.map((m) => (
          <p key={m.key}>
            {m.title} on the {m.wall} wall
            <button type="button" onClick={() => props.onPick(m.key)}>
              Pick {m.title}
            </button>
            <button type="button" onClick={() => props.onHover(`${m.title}, here`)}>
              Hover {m.title}
            </button>
            <button
              type="button"
              onClick={() => props.onDrop(m, props.all, { wall: "left", across: 6 * IN, up: 12 * IN })}
            >
              Drop {m.title} on the left wall
            </button>
          </p>
        ))}
        <button type="button" onClick={() => props.onAdd({ wall: "back", across: 2 * IN, up: 20 * IN })}>
          Click the back wall
        </button>
      </div>
    ),
  ),
}));

const url = "/api/builds/k/files/kiln.glb";
const partsUrl = "/api/builds/k/files/parts.json";
const firebrick = { kind: "Insulating firebrick", colour: "#d9c9a8" };
const steel = { kind: "Steel", colour: "#4c525c" };
const parts = {
  "left/1-ifb-k23": { title: "Left wall, course 1", detail: "K-23", ...firebrick },
  "frame/1": { title: "Angle", detail: "2 × 2 in", ...steel },
  "frame/2": { title: "Angle", detail: "2 × 2 in", ...steel },
};

const fetchParts = vi.fn(async (_url: string) => Response.json(parts));

beforeEach(() => {
  stage.fails = false;
  stage.gl.localClippingEnabled = false;
  stage.load.mockResolvedValue({ scene: new Group() });
  vi.stubGlobal("fetch", fetchParts);
  // jsdom has no media queries; the viewer follows the system's dark mode for its outlines
  vi.stubGlobal("matchMedia", () => ({ matches: false, addEventListener() {}, removeEventListener() {} }));
});

afterEach(() => {
  cleanup();
  localStorage.clear();
  fetchParts.mockClear();
  vi.restoreAllMocks();
});

type Xyz = [number, number, number];

function wall(origin: Xyz, normal: Xyz, right: Xyz, half: number): WallFrame {
  const top: [number, number][] = [
    [-half, 40 * IN],
    [half, 40 * IN],
  ];
  return { origin, normal, right, half_width: half, thickness: 8 * IN, top };
}

const walls = {
  front: wall([0, -32 * IN, 0], [0, -1, 0], [1, 0, 0], 14 * IN),
  back: wall([0, 32 * IN, 0], [0, 1, 0], [-1, 0, 0], 14 * IN),
  left: wall([-22 * IN, 0, 0], [-1, 0, 0], [0, -1, 0], 24 * IN),
  right: wall([22 * IN, 0, 0], [1, 0, 0], [0, 1, 0], 24 * IN),
};

const burnersAndFlue: Layout["ports"] = [
  { name: "port/burner-1", title: "Burner port 1", kind: "burner", wall: "front", across: -7 * IN, up: 5 * IN,
    width: 4 * IN, height: 4 * IN, round: true, cut: true },
  { name: "port/burner-2", title: "Burner port 2", kind: "burner", wall: "front", across: 7 * IN, up: 5 * IN,
    width: 4 * IN, height: 4 * IN, round: true, cut: true },
  { name: "port/flue", title: "Flue port", kind: "flue", wall: "back", across: 0, up: 3.75 * IN,
    width: 11 * IN, height: 7.5 * IN, round: false, cut: true },
]; // prettier-ignore

const spyHoles: Layout["ports"] = [
  { name: "port/spy-1", title: "Spy hole 1", kind: "spy", wall: "right", across: -3 * IN, up: 8 * IN,
    width: 2.25 * IN, height: 2.5 * IN, round: false, cut: true },
  { name: "port/spy-2", title: "Spy hole 2", kind: "spy", wall: "right", across: 3 * IN, up: 30 * IN,
    width: 2.25 * IN, height: 2.5 * IN, round: false, cut: true },
]; // prettier-ignore

const layout: Layout = { units: "us", walls, ports: [...burnersAndFlue, ...spyHoles] };

const doc: KilnDocument = {
  name: "Test",
  firing: { cone: "10" },
  chamber: { width: "28 in", depth: "48 in", height: "40 in" },
  lining: { walls: [{ material: "ifb-k23", thickness: "8 in" }] },
  heat: { gas: { burners: { wall: "front" }, supply: { type: "cylinders", count: 4 } } },
  draft: { type: "cross", flue_wall: "back" },
};

interface Props {
  layout?: Layout;
  draft?: KilnDocument | null;
  onEdit?: (apply: (document: KilnDocument) => KilnDocument) => void;
}

function viewer(props: Props = {}) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  const ui = (p: Props) => (
    <QueryClientProvider client={client}>
      <KilnViewer url={url} partsUrl={partsUrl} {...p} />
    </QueryClientProvider>
  );
  const { rerender } = render(ui(props));
  return { client, rerender: (p: Props) => rerender(ui(p)) };
}

/** The viewer, ready to move ports: returns what each change the model hands the design does to it. */
function moving(withLayout: Layout = layout) {
  const onEdit = vi.fn<(apply: (document: KilnDocument) => KilnDocument) => void>();
  viewer({ layout: withLayout, draft: doc, onEdit });
  fireEvent.click(screen.getByRole("button", { name: "Move ports" }));
  return () => onEdit.mock.lastCall?.[0](doc);
}

const button = (name: string) => screen.getByRole("button", { name }) as HTMLButtonElement;
const pressed = (name: string) => button(name).getAttribute("aria-pressed");
const status = () => screen.getByRole("status").textContent;

describe("KilnViewer, the model", () => {
  it("loads the build's model with each part matte and its own material, keeping its colour as built", async () => {
    const shared = new MeshStandardMaterial({ color: "#b8734c", metalness: 1, roughness: 0.2 });
    const brick = new Mesh(new BoxGeometry(), shared);
    const angle = new Mesh(new BoxGeometry(), shared);
    const glass = new Mesh(new BoxGeometry(), new MeshBasicMaterial());
    const scene = new Group().add(brick, angle, glass);
    stage.load.mockResolvedValue({ scene });
    viewer();
    await waitFor(() => expect((brick.material as MeshStandardMaterial).metalness).toBe(0));
    expect(stage.load).toHaveBeenCalledWith(url);
    const material = brick.material as MeshStandardMaterial;
    expect(material.roughness).toBe(0.9);
    expect([material === shared, material === angle.material]).toEqual([false, false]);
    expect((brick.userData.builtColour as Color).getHexString()).toBe("b8734c");
    expect(glass.material).toBeInstanceOf(MeshBasicMaterial);
  });

  it("says so when the model can't be loaded, after trying again", async () => {
    stage.load.mockRejectedValue(new Error("not a glTF file"));
    viewer();
    const alert = await screen.findByRole("alert", {}, { timeout: 4000 });
    expect(alert.textContent).toBe(
      "The 3D model could not be shown. The files below can still be downloaded.",
    );
    expect(stage.load).toHaveBeenCalledTimes(2);
    expect(screen.queryByRole("toolbar")).toBeNull();
  });

  it("says so in a browser that can't draw in 3D, and keeps the rest of the viewer", () => {
    vi.spyOn(console, "error").mockImplementation(() => {}); // React reports the error it caught
    stage.fails = true;
    viewer();
    expect(screen.getByRole("alert").textContent).toContain("The 3D model could not be shown.");
    expect(screen.getByRole("toolbar", { name: "View" })).toBeTruthy();
  });

  it("turns on clipping in the renderer, for the cut", () => {
    viewer();
    expect(stage.gl.localClippingEnabled).toBe(true);
  });
});

describe("KilnViewer, the toolbar", () => {
  it("looks from one side at a time, and cuts the kiln in half or shows it as a wireframe", () => {
    viewer();
    expect(pressed("3D")).toBe("true");
    fireEvent.click(button("Front"));
    const views = ["3D", "Front", "Side", "Top"].map(pressed);
    expect(views).toEqual(["false", "true", "false", "false"]);
    fireEvent.click(button("Cut in half"));
    fireEvent.click(button("Wireframe"));
    expect([pressed("Cut in half"), pressed("Wireframe")]).toEqual(["true", "true"]);
    fireEvent.click(button("Cut in half"));
    expect(pressed("Cut in half")).toBe("false");
    expect(status()).toBe("Drag to turn, scroll to zoom, click a part to see what it is.");
  });

  it("remembers outlines and a palette, which can give the viewer its own background", () => {
    viewer();
    fireEvent.click(button("Outlines"));
    fireEvent.change(screen.getByLabelText("Model colours"), { target: { value: "blueprint" } });
    expect(screen.getByLabelText("3D model of the kiln").style.background).toBe("rgb(18, 53, 91)");
    cleanup();
    viewer();
    expect(pressed("Outlines")).toBe("true");
    expect((screen.getByLabelText("Model colours") as HTMLSelectElement).value).toBe("blueprint");
  });

  it("lists each material once, in the palette's colour, and keeps a colour picked until reset", async () => {
    viewer();
    const legend = await screen.findByRole("list", { name: "Materials in the model" });
    expect(within(legend).getAllByRole("listitem").map((li) => li.textContent)).toEqual([
      "Insulating firebrick",
      "Steel",
    ]);
    const steel = () => screen.getByLabelText("Colour for Steel") as HTMLInputElement;
    expect(steel().value).toBe("#4c525c");
    fireEvent.change(screen.getByLabelText("Model colours"), { target: { value: "grey" } });
    expect(steel().value).toBe("#404040");
    expect(screen.queryByRole("button", { name: "Reset colours" })).toBeNull();
    fireEvent.change(steel(), { target: { value: "#ff00ff" } });
    expect(steel().value).toBe("#ff00ff");
    const remembered = JSON.parse(localStorage.getItem("kilndesigner.viewer") ?? "{}");
    expect(remembered.custom).toEqual({ Steel: "#ff00ff" });
    fireEvent.click(button("Reset colours"));
    expect(steel().value).toBe("#404040");
    expect(fetchParts).toHaveBeenCalledWith(partsUrl);
  });

  it("has no legend for a build that doesn't say what its parts are", async () => {
    fetchParts.mockResolvedValueOnce(new Response(null, { status: 404 }));
    const { client } = viewer();
    // An older build has no parts.json: it has no parts, rather than an error
    await waitFor(() => expect(client.getQueryState(["parts", partsUrl])?.data).toEqual({}));
    expect(screen.queryByRole("list", { name: "Materials in the model" })).toBeNull();
    expect(screen.getByRole("toolbar", { name: "View" })).toBeTruthy();
  });
});

describe("KilnViewer, moving ports", () => {
  it("is offered only with ports to move and a design to change", () => {
    const onEdit = vi.fn();
    const { rerender } = viewer();
    expect(screen.queryByRole("button", { name: "Move ports" })).toBeNull();
    rerender({ layout });
    expect(screen.queryByRole("button", { name: "Move ports" })).toBeNull();
    rerender({ layout: { ...layout, ports: [] }, onEdit });
    expect(screen.queryByRole("button", { name: "Move ports" })).toBeNull();
    rerender({ layout, onEdit });
    expect(button("Move ports")).toBeTruthy();
    expect(screen.queryByRole("group", { name: "Markers" })).toBeNull();
  });

  it("shows the markers where the design being edited puts them, and how to move them", async () => {
    const onEdit = vi.fn();
    const places = [{ wall: "right" as const, across: "0 in", up: "10 in" }];
    const placed: KilnDocument = { ...doc, heat: { gas: { ...doc.heat.gas!, burners: { places } } } };
    const { rerender } = viewer({ layout, draft: doc, onEdit });
    fireEvent.click(button("Move ports"));
    const markers = await screen.findByRole("group", { name: "Markers" });
    expect(markers.textContent).toContain("Burner port 2 on the front wall");
    expect(status()).toMatch(/^Drag a port across its wall or onto another, then save and build/);
    rerender({ layout, draft: placed, onEdit });
    expect(markers.textContent).toContain("Burner port 1 on the right wall");
    expect(markers.textContent).not.toContain("Burner port 2");
  });

  it("hands the design a port dropped on another wall", async () => {
    const applied = moving();
    fireEvent.click(await screen.findByRole("button", { name: "Drop Burner port 2 on the left wall" }));
    expect(applied()?.heat.gas?.burners).toEqual({
      wall: "front",
      places: [
        { wall: "front", across: "-7 in", up: "5 in" },
        { wall: "left", across: "6 in", up: "12 in" },
      ],
    });
  });

  it("says what a port under the pointer is", async () => {
    moving();
    fireEvent.click(await screen.findByRole("button", { name: "Hover Flue port" }));
    expect(status()).toBe("Flue port, here");
  });

  it("stops the model turning while ports are moved, when asked", async () => {
    moving();
    expect(screen.getByText(/^Turning/).textContent).toBe("Turning on");
    fireEvent.click(screen.getByLabelText("Stop turning"));
    expect(screen.getByText(/^Turning/).textContent).toBe("Turning off");
    fireEvent.click(button("Move ports")); // done moving: it turns again
    expect(screen.getByText(/^Turning/).textContent).toBe("Turning on");
    expect(screen.queryByLabelText("Stop turning")).toBeNull();
  });

  it("adds a spy hole where the wall is clicked, the size of those built, then stops adding", async () => {
    const applied = moving();
    fireEvent.click(button("Add a spy hole"));
    expect(pressed("Add a spy hole")).toBe("true");
    expect(status()).toBe("Click the wall where the new spy hole goes.");
    await screen.findByRole("group", { name: "Markers" });
    expect(screen.getByText(/^adding:/).textContent).toBe("adding: true, picked: none");
    fireEvent.click(button("Click the back wall"));
    expect(applied()?.spy_holes).toEqual({
      places: [
        { wall: "right", across: "-3 in", up: "8 in" },
        { wall: "right", across: "3 in", up: "30 in" },
        { wall: "back", across: "2 in", up: "20 in" },
      ],
    });
    expect(pressed("Add a spy hole")).toBe("false");
  });

  it("offers to remove a spy hole that's picked, not a burner's port", async () => {
    const applied = moving();
    fireEvent.click(await screen.findByRole("button", { name: "Pick Burner port 1" }));
    expect(screen.getByText(/^adding:/).textContent).toBe("adding: false, picked: burner-0");
    expect(screen.queryByRole("button", { name: /^Remove/ })).toBeNull();
    fireEvent.click(button("Pick Spy hole 1"));
    fireEvent.click(button("Remove spy hole 1"));
    expect(applied()?.spy_holes).toEqual({ places: [{ wall: "right", across: "3 in", up: "30 in" }] });
    expect(screen.queryByRole("button", { name: /^Remove/ })).toBeNull();
  });

  it("lets go of the port picked on a click off the model", async () => {
    moving();
    fireEvent.click(await screen.findByRole("button", { name: "Pick Spy hole 2" }));
    expect(button("Remove spy hole 2")).toBeTruthy();
    fireEvent.click(button("Click off the model"));
    expect(screen.queryByRole("button", { name: "Remove spy hole 2" })).toBeNull();
  });

  it("lets go of everything when moving stops", async () => {
    moving();
    fireEvent.click(button("Add a spy hole"));
    fireEvent.click(await screen.findByRole("button", { name: "Hover Spy hole 1" }));
    fireEvent.click(button("Move ports"));
    expect(screen.queryByRole("group", { name: "Markers" })).toBeNull();
    expect(screen.queryByRole("button", { name: "Add a spy hole" })).toBeNull();
    expect(status()).toBe("Drag to turn, scroll to zoom, click a part to see what it is.");
    fireEvent.click(button("Move ports"));
    expect(pressed("Add a spy hole")).toBe("false");
  });

  it("can't add a spy hole before one has been built to copy, and names it as the build does", () => {
    moving({ ...layout, ports: burnersAndFlue });
    expect(button("Add a spy hole").disabled).toBe(true);
    expect(button("Add a spy hole").title).toBe(
      "Build with a spy hole first: one added is the size of those built",
    );
    cleanup();
    const peepholes = spyHoles.map((p, i) => ({ ...p, title: `Peephole ${i + 1}` }));
    moving({ ...layout, ports: peepholes });
    expect(button("Add a peephole").disabled).toBe(false);
    expect(button("Add a peephole").title).toBe("");
  });
});
