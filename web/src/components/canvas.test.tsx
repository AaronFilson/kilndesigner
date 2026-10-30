// The 3D scene itself, drawn by React Three Fiber's test renderer: a scene graph without WebGL, so
// it runs in jsdom. The model is a small glTF made here and loaded as a build's is, so the parts'
// names come back as the loader leaves them.
import { Bounds } from "@react-three/drei";
import { _roots, type RootState, useThree } from "@react-three/fiber";
import ReactThreeTestRenderer from "@react-three/test-renderer";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import type { ComponentProps, ReactNode } from "react";
import {
  type Group,
  type LineBasicMaterial,
  LineSegments,
  Mesh,
  type MeshStandardMaterial,
  type Object3D,
  Ray,
  Vector3,
} from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import type { KilnDocument, Layout, WallFrame } from "../design";
import { DEFAULT_LOOK } from "../palettes";
import { Aim, faceLook, KilnViewer, Model, outlineColour, prepare } from "./KilnViewer";
import { isClick, markers, PortMarkers, toDevice } from "./PortMarkers";

const IN = 25.4;
const { act } = ReactThreeTestRenderer;
const WIDTH = 1280;
const HEIGHT = 800;

let renderer: Awaited<ReturnType<typeof ReactThreeTestRenderer.create>> | null = null;
let root: RootState | null = null;

/** Keeps the scene's state, so a test can reach its camera, renderer and controls. */
function Probe() {
  root = useThree();
  return null;
}

/** Draws ``scene`` with a canvas that has a size on the page, as a browser's has. */
async function draw(scene: ReactNode) {
  renderer = await ReactThreeTestRenderer.create(
    <>
      {scene}
      <Probe />
    </>,
    {
      width: WIDTH,
      height: HEIGHT,
      beforeReturn: (canvas) => {
        canvas.getBoundingClientRect = () => DOMRect.fromRect({ x: 0, y: 0, width: WIDTH, height: HEIGHT });
      },
    },
  );
  return renderer;
}

afterEach(async () => {
  await renderer?.unmount();
  renderer = null;
  root = null;
});

// A model: a unit cube for each primitive of each part, its buffer inline

const CORNERS = [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1];
const FACES = [
  0, 2, 1, 0, 3, 2, 4, 5, 6, 4, 6, 7, 0, 1, 5, 0, 5, 4, 2, 3, 7, 2, 7, 6, 1, 2, 6, 1, 6, 5, 0, 4, 7, 0, 7, 3,
];

function gltf(parts: { name: string; primitives?: number }[]): string {
  const positions = new Float32Array(CORNERS);
  const indices = new Uint16Array(FACES);
  const bytes = new Uint8Array(positions.byteLength + indices.byteLength);
  bytes.set(new Uint8Array(positions.buffer));
  bytes.set(new Uint8Array(indices.buffer), positions.byteLength);
  return JSON.stringify({
    asset: { version: "2.0" },
    scene: 0,
    scenes: [{ nodes: parts.map((_, i) => i) }],
    nodes: parts.map((p, i) => ({ name: p.name, mesh: i, translation: [i * 2, 0, 0] })),
    meshes: parts.map((p) => ({
      primitives: Array.from({ length: p.primitives ?? 1 }, () => ({
        attributes: { POSITION: 0 },
        indices: 1,
        material: 0,
      })),
    })),
    // glTF's default metallicFactor is 1, as the engine's CAD export leaves it
    materials: [{ pbrMetallicRoughness: { baseColorFactor: [0.8, 0.5, 0.2, 1] } }],
    accessors: [
      { bufferView: 0, componentType: 5126, count: 8, type: "VEC3", min: [0, 0, 0], max: [1, 1, 1] },
      { bufferView: 1, componentType: 5123, count: 36, type: "SCALAR" },
    ],
    bufferViews: [
      { buffer: 0, byteOffset: 0, byteLength: positions.byteLength },
      { buffer: 0, byteOffset: positions.byteLength, byteLength: indices.byteLength },
    ],
    buffers: [
      {
        byteLength: bytes.byteLength,
        uri: `data:application/octet-stream;base64,${btoa(String.fromCharCode(...bytes))}`,
      },
    ],
  });
}

const firebrick = { kind: "Insulating firebrick", colour: "#d9c9a8" };
const parts = {
  "left/1-ifb-k23": { title: "Left wall, layer 1", detail: "K-23", ...firebrick },
  "burner/1": { title: "Burner 1 of 1", detail: "Ransome B4", kind: "Burner", colour: "#4c525c" },
  "frame/1": { title: "Angle", detail: "2 × 2 in", kind: "Steel", colour: "#4c525c" },
};

/** The model as the viewer gets it: three parts, the frame's in two primitives. */
async function loaded(): Promise<Group> {
  const text = gltf([{ name: "left/1-ifb-k23" }, { name: "burner/1" }, { name: "frame/1", primitives: 2 }]);
  return prepare((await new GLTFLoader().parseAsync(text, "")).scene);
}

/** The part a mesh or line belongs to: the name the engine gave it, which the loader keeps. */
function partOf(object: Object3D): string | undefined {
  for (let o: Object3D | null = object; o; o = o.parent) {
    if (typeof o.userData.name === "string") return o.userData.name;
  }
  return undefined;
}

function meshesOf(scene: Group, part: string): Mesh[] {
  const found: Mesh[] = [];
  scene.traverse((o) => {
    if (o instanceof Mesh && partOf(o) === part) found.push(o);
  });
  return found;
}

const materialOf = (scene: Group, part: string) => meshesOf(scene, part)[0]!.material as MeshStandardMaterial;

/** An outline's colour, as hex. */
const lineHex = (line: LineSegments) => (line.material as LineBasicMaterial).color.getHexString();

function outlinesOf(scene: Group): Map<string, LineSegments> {
  const found = new Map<string, LineSegments>();
  scene.traverse((o) => {
    if (o instanceof LineSegments) found.set(partOf(o)!, o);
  });
  return found;
}

type ModelProps = ComponentProps<typeof Model>;

async function model(props: Partial<ModelProps> = {}) {
  const scene = await loaded();
  const onSelect = vi.fn<(name: string) => void>();
  const at: ModelProps = {
    scene, parts, look: DEFAULT_LOOK, cut: false, wire: false, ink: "#101010", faintBurners: false,
    selected: null, onSelect, ...props,
  }; // prettier-ignore
  const drawn = await draw(<Model {...at} />);
  const update = (more: Partial<ModelProps>) => drawn.update(<Model {...at} {...more} />);
  return { scene, onSelect, update, primitive: drawn.scene.children[0]! };
}

describe("a part's look", () => {
  const showing = { look: DEFAULT_LOOK, wire: false, ink: "#101010", faintBurners: false, selected: null };

  it("glows when it's the part picked, and its faces hide in a wireframe", () => {
    expect(faceLook("left/1", undefined, showing)).toEqual({
      colour: undefined, emissive: "#000000", faint: false, visible: true,
    }); // prettier-ignore
    const picked = faceLook("left/1", undefined, { ...showing, wire: true, selected: "left/1" });
    expect(picked).toMatchObject({ emissive: "#8a3a10", visible: false });
  });

  it("is faint only for a burner, and only while ports are moved", () => {
    expect(faceLook("burner/1", undefined, { ...showing, faintBurners: true }).faint).toBe(true);
    expect(faceLook("burner/1", undefined, showing).faint).toBe(false);
    expect(faceLook("left/1", undefined, { ...showing, faintBurners: true }).faint).toBe(false);
  });

  it("takes the palette's colour, or a colour picked for its material", () => {
    const grey = { ...DEFAULT_LOOK, palette: "grey" as const };
    expect(faceLook("frame/1", "Steel", { ...showing, look: grey }).colour).toBe("#404040");
    const custom = { ...grey, custom: { Steel: "#ff00ff" } };
    expect(faceLook("frame/1", "Steel", { ...showing, look: custom }).colour).toBe("#ff00ff");
  });

  it("is outlined in the palette's edge colour, in ink in a wireframe, in orange if picked", () => {
    expect(outlineColour("left/1", showing)).toBe("#2b2622");
    expect(outlineColour("left/1", { ...showing, wire: true })).toBe("#101010");
    expect(outlineColour("left/1", { ...showing, wire: true, selected: "left/1" })).toBe("#e8833a");
    // Picked but faces showing: the face glows instead
    expect(outlineColour("left/1", { ...showing, selected: "left/1" })).toBe("#2b2622");
    // A palette with its own background keeps its own edges, even in a wireframe
    const blueprint = { ...DEFAULT_LOOK, palette: "blueprint" as const };
    const edges = outlineColour("left/1", { ...showing, look: blueprint });
    expect(outlineColour("left/1", { ...showing, look: blueprint, wire: true })).toBe(edges);
  });
});

describe("Model, in the scene", () => {
  it("loads each part matte, with its own material, keeping its colour as built", async () => {
    const scene = await loaded();
    const frame = meshesOf(scene, "frame/1");
    expect(frame).toHaveLength(2); // a part in two primitives: a group of two meshes
    expect(frame[0]!.material).not.toBe(frame[1]!.material);
    for (const part of Object.keys(parts)) {
      const material = materialOf(scene, part);
      expect([material.metalness, material.roughness]).toEqual([0, 0.9]);
      expect(meshesOf(scene, part)[0]!.userData.builtColour.equals(material.color)).toBe(true);
    }
  });

  it("draws a burner faint while ports are moved, and solid again after", async () => {
    const { scene, update } = await model({ faintBurners: true });
    const burner = materialOf(scene, "burner/1");
    expect([burner.transparent, burner.depthWrite, burner.opacity]).toEqual([true, false, 0.25]);
    expect(materialOf(scene, "left/1-ifb-k23").transparent).toBe(false);
    await update({ faintBurners: false });
    expect([burner.transparent, burner.depthWrite, burner.opacity]).toEqual([false, true, 1]);
  });

  it("has no outlines until they're wanted; a wireframe hides the faces and shows them in ink", async () => {
    const { scene, update } = await model();
    expect(outlinesOf(scene).size).toBe(0);
    await update({ wire: true });
    const lines = outlinesOf(scene);
    // One outline a part, the frame's two primitives merged into one
    expect([...lines.keys()].sort()).toEqual(["burner/1", "frame/1", "left/1-ifb-k23"]);
    expect(materialOf(scene, "left/1-ifb-k23").visible).toBe(false);
    for (const line of lines.values()) {
      expect(line.visible).toBe(true);
      expect(lineHex(line)).toBe("101010");
    }
    // Back to faces, without outlines: they're kept, hidden
    await update({ wire: false });
    expect(materialOf(scene, "left/1-ifb-k23").visible).toBe(true);
    expect([...outlinesOf(scene).values()].every((l) => !l.visible)).toBe(true);
  });

  it("outlines the part picked in orange in a wireframe, and its outline can't be clicked", async () => {
    const { scene } = await model({ wire: true, selected: "frame/1" });
    const lines = outlinesOf(scene);
    expect(lineHex(lines.get("frame/1")!)).toBe("e8833a");
    expect(lineHex(lines.get("burner/1")!)).toBe("101010");
    const hits: unknown[] = [];
    lines.get("frame/1")!.raycast(undefined as never, hits as never);
    expect(hits).toEqual([]);
  });

  it("colours the parts from the palette, and goes back to the colours as built", async () => {
    const grey = { ...DEFAULT_LOOK, palette: "grey" as const };
    const { scene, update } = await model({ look: grey });
    expect(materialOf(scene, "frame/1").color.getHexString()).toBe("404040");
    await update({ look: DEFAULT_LOOK });
    const built = meshesOf(scene, "frame/1")[0]!.userData.builtColour;
    expect(materialOf(scene, "frame/1").color.equals(built)).toBe(true);
  });

  it("cuts the kiln in half, faces and outlines", async () => {
    const { scene } = await model({ cut: true, look: { ...DEFAULT_LOOK, edges: true } });
    expect(materialOf(scene, "left/1-ifb-k23").clippingPlanes).toHaveLength(1);
    const outline = outlinesOf(scene).get("left/1-ifb-k23")!;
    expect((outline.material as LineBasicMaterial).clippingPlanes).toHaveLength(1);
  });

  it("names the part clicked, from the mesh hit up to its part", async () => {
    const { scene, onSelect, primitive } = await model();
    const [frame] = meshesOf(scene, "frame/1");
    await renderer!.fireEvent(primitive, "onClick", {
      intersections: [{ object: frame, point: new Vector3(0, 0, 1) }],
    });
    expect(onSelect).toHaveBeenCalledWith("frame/1");
  });

  it("leaves a click that also hits a port's marker to the marker", async () => {
    const { scene, onSelect, primitive } = await model();
    const marker = new Mesh();
    marker.userData.port = true;
    await renderer!.fireEvent(primitive, "onClick", {
      intersections: [
        { object: meshesOf(scene, "burner/1")[0], point: new Vector3() },
        { object: marker, point: new Vector3() },
      ],
    });
    expect(onSelect).not.toHaveBeenCalled();
  });

  it("cut in half, picks the first part behind the cut, and nothing if there's none", async () => {
    const { scene, onSelect, primitive } = await model({ cut: true });
    const front = { object: meshesOf(scene, "burner/1")[0], point: new Vector3(0, 0, 0.5) };
    const back = { object: meshesOf(scene, "left/1-ifb-k23")[0], point: new Vector3(0, 0, -0.5) };
    await renderer!.fireEvent(primitive, "onClick", { intersections: [front, back] });
    expect(onSelect).toHaveBeenLastCalledWith("left/1-ifb-k23");
    await renderer!.fireEvent(primitive, "onClick", { intersections: [front] });
    expect(onSelect).toHaveBeenCalledTimes(1);
  });
});

describe("Aim, framing the kiln", () => {
  it.each([
    ["front", [0, 0, 1]],
    ["side", [1, 0, 0]],
    ["top", [0, 1, 0.01]],
  ] as const)("looks at it from the %s", async (view, direction) => {
    await draw(
      <Bounds fit clip margin={1.35}>
        <mesh position={[3, 2, 1]}>
          <boxGeometry args={[1, 1, 1]} />
        </mesh>
        <Aim view={view} />
      </Bounds>,
    );
    await act(async () => renderer!.advanceFrames(90, 1 / 30));
    const seen = root!.camera.position.clone().sub(new Vector3(3, 2, 1)).normalize();
    expect(seen.distanceTo(new Vector3(...direction).normalize())).toBeLessThan(1e-3);
  });
});

// Ports: a 28 × 48 in chamber with 8 in walls, burners in the front, the flue at the back and spy
// holes in the right wall

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

const ports: Layout["ports"] = [
  { name: "port/burner-1", title: "Burner port 1", kind: "burner", wall: "front", across: -7 * IN, up: 5 * IN,
    width: 4 * IN, height: 4 * IN, round: true, cut: true },
  { name: "port/burner-2", title: "Burner port 2", kind: "burner", wall: "front", across: 7 * IN, up: 5 * IN,
    width: 4 * IN, height: 4 * IN, round: true, cut: false },
  { name: "port/flue", title: "Flue port", kind: "flue", wall: "back", across: 0, up: 3.75 * IN,
    width: 11 * IN, height: 7.5 * IN, round: false, cut: true },
  { name: "port/spy-1", title: "Spy hole 1", kind: "spy", wall: "right", across: -3 * IN, up: 8 * IN,
    width: 2.25 * IN, height: 2.5 * IN, round: false, cut: true },
]; // prettier-ignore

const layout: Layout = { units: "us", walls, ports };

const doc: KilnDocument = {
  name: "Test",
  firing: { cone: "10" },
  chamber: { width: "28 in", depth: "48 in", height: "40 in" },
  lining: { walls: [{ material: "ifb-k23", thickness: "8 in" }] },
  heat: { gas: { burners: { wall: "front" }, supply: { type: "cylinders", count: 4 } } },
  draft: { type: "cross", flue_wall: "back" },
};

/** A ray in the model's millimetres, z up, as the scene sees it: metres, y up, the front at +z. */
function sceneRay(origin: Xyz, direction: Xyz): Ray {
  const turn = ([x, y, z]: Xyz) => new Vector3(x, z, -y);
  return new Ray(turn(origin).multiplyScalar(0.001), turn(direction).normalize());
}

async function portMarkers(props: Partial<ComponentProps<typeof PortMarkers>> = {}) {
  const all = markers(layout, doc);
  const calls = {
    onDrop: vi.fn(), onPick: vi.fn<(key: string) => void>(), onAdd: vi.fn(),
    onHover: vi.fn<(text: string | null) => void>(),
  }; // prettier-ignore
  const drawn = await draw(<PortMarkers layout={layout} all={all} picked={null} adding={false} {...calls} {...props} />);
  // The camera, at the scene's default (0, 0, 5) m, faces the front wall: one frame finds that
  await act(async () => drawn.advanceFrames(1, 1 / 60));
  root!.scene.updateMatrixWorld(true);
  const meshes = drawn.scene.findAll((node) => node.type === "Mesh");
  return { all, meshes, ...calls };
}

const material = (node: { instance: unknown }) =>
  (node.instance as Mesh).material as MeshStandardMaterial & { color: { getHexString(): string } };

/** Pointer capture, which the test renderer's event target doesn't have. */
const capture = () => ({ setPointerCapture: vi.fn(), releasePointerCapture: vi.fn() });

describe("PortMarkers, in the scene", () => {
  it("draws each port as a marker that is a port's, coloured by kind, red if it didn't fit", async () => {
    const { all, meshes } = await portMarkers();
    expect(meshes).toHaveLength(all.length);
    expect(meshes.every((m) => (m.instance as Mesh).userData.port === true)).toBe(true);
    // Burners first, then spy holes, then the flue, as ``markers`` lists them
    expect(meshes.map((m) => material(m).color.getHexString())).toEqual([
      "e8833a", // a burner's port
      "d92d20", // the burner port that didn't fit
      "3a8be8", // a spy hole
      "8c8c8c", // the flue
    ]);
  });

  it("makes the markers on walls facing away faint, and lets them be picked up only when seen", async () => {
    const { meshes } = await portMarkers();
    // The front faces the camera; the back and the right walls don't
    expect(meshes.map((m) => material(m).opacity)).toEqual([0.95, 0.95, 0.2, 0.2]);
    const hits: unknown[] = [];
    const ray = sceneRay([0, 1500, 95], [0, -1, 0]); // from behind the kiln at the flue
    (meshes[3]!.instance as Mesh).raycast({ ray } as never, hits as never);
    expect(hits).toEqual([]);
  });

  it("picks a marker that's pressed, and stops the controls turning the model while it's held", async () => {
    const { meshes, onPick } = await portMarkers();
    const controls = { enabled: true };
    await act(async () => root!.set({ controls: controls as never }));
    const target = capture();
    await renderer!.fireEvent(meshes[0]!, "onPointerDown", { pointerId: 7, target });
    expect(onPick).toHaveBeenCalledWith("burner-0");
    expect(target.setPointerCapture).toHaveBeenCalledWith(7);
    expect(controls.enabled).toBe(false);
    // Let go without moving it: nothing is dropped, and the controls work again
    await renderer!.fireEvent(meshes[0]!, "onPointerUp", { pointerId: 7, target });
    expect(target.releasePointerCapture).toHaveBeenCalledWith(7);
    expect(controls.enabled).toBe(true);
  });

  it("drags a marker onto another wall and drops it at a fitted spot", async () => {
    const { all, meshes, onDrop, onHover } = await portMarkers();
    const target = capture();
    await renderer!.fireEvent(meshes[0]!, "onPointerDown", { pointerId: 1, target });
    // Across the left wall, 100 mm along and 300 mm up: snapped to ¼ in
    await renderer!.fireEvent(meshes[0]!, "onPointerMove", { ray: sceneRay([-2000, 100, 300], [1, 0, 0]) });
    expect(onHover).toHaveBeenLastCalledWith(expect.stringMatching(/^Burner port 1: -4 in across and 11.75 in up/));
    await renderer!.fireEvent(meshes[0]!, "onPointerUp", { pointerId: 1, target });
    expect(onDrop).toHaveBeenCalledTimes(1);
    const [marker, given, to] = onDrop.mock.calls[0]!;
    expect([marker, given]).toEqual([all[0], all]);
    expect(to).toMatchObject({ wall: "left" });
    expect(to.across).toBeCloseTo(-16 * (IN / 4));
    expect(to.up).toBeCloseTo(47 * (IN / 4));
    // The marker stays where it was dropped until the design comes back
    const at = (meshes[0]!.instance as Mesh).position;
    expect(at.x).toBeCloseTo(walls.left.origin[0] - 7, 0);
  });

  it("doesn't drop a marker moved off every wall, or another marker's move", async () => {
    const { meshes, onDrop } = await portMarkers();
    const target = capture();
    // A move before any press isn't a drag
    await renderer!.fireEvent(meshes[0]!, "onPointerMove", { ray: sceneRay([-2000, 100, 300], [1, 0, 0]) });
    await renderer!.fireEvent(meshes[0]!, "onPointerUp", { pointerId: 1, target });
    await renderer!.fireEvent(meshes[0]!, "onPointerDown", { pointerId: 1, target });
    // Pointing up past the kiln: no wall, so it stays where it was
    await renderer!.fireEvent(meshes[0]!, "onPointerMove", { ray: sceneRay([0, -2000, 5000], [0, 0, 1]) });
    // The other marker isn't the one held
    await renderer!.fireEvent(meshes[1]!, "onPointerMove", { ray: sceneRay([-2000, 100, 300], [1, 0, 0]) });
    await renderer!.fireEvent(meshes[1]!, "onPointerUp", { pointerId: 1, target });
    await renderer!.fireEvent(meshes[0]!, "onPointerUp", { pointerId: 1, target });
    expect(onDrop).not.toHaveBeenCalled();
  });

  it("says what a marker under the pointer is, and how to move it", async () => {
    const { meshes, onHover } = await portMarkers();
    await renderer!.fireEvent(meshes[2]!, "onPointerOver");
    expect(onHover).toHaveBeenLastCalledWith(
      "Spy hole 1: -3 in across and 8 in up the right wall. Drag it to move it, or click it to remove it.",
    );
    await renderer!.fireEvent(meshes[1]!, "onPointerOver");
    expect(onHover).toHaveBeenLastCalledWith(
      "Burner port 2: 7 in across and 5 in up the front wall (it didn't fit, so it isn't cut). Drag it to move it.",
    );
    await renderer!.fireEvent(meshes[1]!, "onPointerOut");
    expect(onHover).toHaveBeenLastCalledWith(null);
    // A click on a marker is the marker's, not the model's
    const stopPropagation = vi.fn();
    await renderer!.fireEvent(meshes[1]!, "onClick", { stopPropagation });
    expect(stopPropagation).toHaveBeenCalled();
  });
});

describe("PortMarkers, adding a spy hole", () => {
  /** A press and a release on the canvas, as the browser sends them. */
  function click(from: [number, number], to: [number, number] = from) {
    const canvas = root!.gl.domElement;
    canvas.dispatchEvent(new MouseEvent("pointerdown", { clientX: from[0], clientY: from[1] }));
    canvas.dispatchEvent(new MouseEvent("pointerup", { clientX: to[0], clientY: to[1] }));
  }

  /** Where a marker shows on the canvas, in client pixels. */
  function onCanvas(node: { instance: unknown }): [number, number] {
    const p = (node.instance as Mesh).getWorldPosition(new Vector3()).project(root!.camera);
    return [((p.x + 1) / 2) * WIDTH, ((1 - p.y) / 2) * HEIGHT];
  }

  it("adds one, the size of those built, where a wall is clicked", async () => {
    const { onAdd } = await portMarkers({ adding: true });
    click([WIDTH / 2 - 2, HEIGHT / 2 - 2], [WIDTH / 2, HEIGHT / 2]); // a hand moves a little
    expect(onAdd).toHaveBeenCalledTimes(1);
    const [to] = onAdd.mock.calls[0]!;
    // Straight ahead is the front wall at the floor: kept up off it by half the spy hole
    expect(to).toMatchObject({ wall: "front" });
    expect(to.across).toBeCloseTo(0, 0);
    expect(to.up).toBeCloseTo((2.5 * IN) / 2);
  });

  it("doesn't add one for a drag, which turns the model, or a click on a marker", async () => {
    const { meshes, onAdd } = await portMarkers({ adding: true });
    click([WIDTH / 2, HEIGHT / 2], [WIDTH / 2 + 30, HEIGHT / 2]);
    click(onCanvas(meshes[0]!));
    // A release with no press on the canvas
    root!.gl.domElement.dispatchEvent(new MouseEvent("pointerup", { clientX: 10, clientY: 10 }));
    expect(onAdd).not.toHaveBeenCalled();
  });

  it("doesn't add one for a click that misses the kiln", async () => {
    const { onAdd } = await portMarkers({ adding: true });
    click([5, 5]);
    expect(onAdd).not.toHaveBeenCalled();
  });

  it("listens only while adding, and only with a spy hole built to copy", async () => {
    const { onAdd } = await portMarkers();
    click([WIDTH / 2, HEIGHT / 2]);
    await renderer!.update(
      <PortMarkers
        layout={{ ...layout, ports: ports.filter((p) => p.kind !== "spy") }}
        all={markers(layout, doc)}
        picked={null}
        adding
        onDrop={vi.fn()}
        onPick={vi.fn()}
        onAdd={onAdd}
        onHover={vi.fn()}
      />,
    );
    click([WIDTH / 2, HEIGHT / 2]);
    expect(onAdd).not.toHaveBeenCalled();
  });
});

describe("KilnViewer, on a canvas of its own", () => {
  // React Three Fiber's own Canvas, sized as a browser would size it, drawing with the test
  // renderer's stand-in for WebGL
  beforeEach(async () => {
    await (await ReactThreeTestRenderer.create(<group />)).unmount(); // puts the stand-in in place
    vi.stubGlobal(
      "ResizeObserver",
      class {
        constructor(private readonly changed: () => void) {}
        observe() {
          setTimeout(() => this.changed());
        }
        unobserve() {}
        disconnect() {}
      },
    );
    vi.spyOn(HTMLElement.prototype, "getBoundingClientRect").mockReturnValue(
      DOMRect.fromRect({ width: WIDTH, height: HEIGHT }),
    );
    vi.stubGlobal("matchMedia", () => ({ matches: false, addEventListener() {}, removeEventListener() {} }));
  });

  afterEach(() => {
    cleanup();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("stops the controls turning the model only while ports are moved and turning is stopped", async () => {
    const model = `data:model/gltf+json;base64,${btoa(gltf([{ name: "left/1-ifb-k23" }]))}`;
    const list = `data:application/json,${encodeURIComponent(JSON.stringify(parts))}`;
    const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
    const { container } = render(
      <QueryClientProvider client={client}>
        <KilnViewer url={model} partsUrl={list} layout={layout} draft={doc} onEdit={vi.fn()} />
      </QueryClientProvider>,
    );
    const store = await waitFor(() => {
      const found = _roots.get(container.querySelector("canvas")!)?.store;
      expect(found?.getState().controls).toBeTruthy();
      return found!;
    });
    const turning = () => (store.getState().controls as unknown as { enableRotate: boolean }).enableRotate;
    expect(turning()).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "Move ports" }));
    const stop = screen.getByRole("checkbox", { name: "Stop turning" });
    expect(turning()).toBe(true); // moving ports, but still turning
    fireEvent.click(stop);
    await waitFor(() => expect(turning()).toBe(false));
    fireEvent.click(stop);
    await waitFor(() => expect(turning()).toBe(true));
    // Stopped, then done moving ports: the model turns again
    fireEvent.click(stop);
    await waitFor(() => expect(turning()).toBe(false));
    fireEvent.click(screen.getByRole("button", { name: "Move ports" }));
    await waitFor(() => expect(turning()).toBe(true));
    // The model loaded and drew, with the renderer clipping for the cut
    expect(store.getState().gl.localClippingEnabled).toBe(true);
    await waitFor(() => {
      const names: string[] = [];
      store.getState().scene.traverse((o) => names.push(String(o.userData.name)));
      expect(names).toContain("left/1-ifb-k23");
    });
  });
});

describe("a click on the canvas", () => {
  it("is a press and a release within 4 px of each other", () => {
    expect(isClick({ x: 10, y: 10 }, { x: 13, y: 12 })).toBe(true);
    expect(isClick({ x: 10, y: 10 }, { x: 15, y: 10 })).toBe(false);
    expect(isClick(null, { x: 10, y: 10 })).toBe(false);
  });

  it("is placed in the canvas's -1 to 1 coordinates, y up", () => {
    const box = { left: 100, top: 50, width: 200, height: 100 };
    expect(toDevice({ x: 200, y: 100 }, box).toArray()).toEqual([0, 0]);
    expect(toDevice({ x: 100, y: 50 }, box).toArray()).toEqual([-1, 1]);
    expect(toDevice({ x: 300, y: 150 }, box).toArray()).toEqual([1, -1]);
  });
});
