// The kiln's 3D model: the glTF the engine built (ADR 0005), framed to fit. Views from the front,
// the side and the top, a cut through the middle to show the lining, the name of any part that's
// clicked, and the model's colours: as built, a palette, or picked per material.
import { Bounds, OrbitControls, useBounds } from "@react-three/drei";
import { Canvas, type ThreeEvent } from "@react-three/fiber";
import { useQuery } from "@tanstack/react-query";
import { Component, type ReactNode, useEffect, useMemo, useState } from "react";
import {
  BufferGeometry,
  Color,
  EdgesGeometry,
  type Group,
  LineBasicMaterial,
  LineSegments,
  Mesh,
  MeshStandardMaterial,
  type Object3D,
  Plane,
  Vector3,
} from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";
import { mergeGeometries, mergeVertices } from "three/addons/utils/BufferGeometryUtils.js";

import type { KilnDocument, Layout } from "../design";
import { colourOf, loadLook, palette, PALETTES, type PaletteId, saveLook, type ViewerLook } from "../palettes";
import { added, markers, moved, PortMarkers, removed, spyWord } from "./PortMarkers";

/** What a part of the model is: from the build's parts.json, by the part's name. */
export interface PartInfo {
  title: string;
  detail: string;
  /** What it's made of ("Insulating firebrick", "Steel") and its colour in the model. */
  kind?: string;
  colour?: string;
}

/** Each material in the model once, with its colour, in the order the parts list them. */
export function legend(parts: Record<string, PartInfo>): [string, string][] {
  const seen = new Map<string, string>();
  for (const part of Object.values(parts)) {
    if (part.kind && part.colour && !seen.has(part.kind)) seen.set(part.kind, part.colour);
  }
  return [...seen];
}

type View = "3d" | "front" | "side" | "top";

// The engine's model is z-up; glTF turns it y-up, so the kiln's front faces +z and its right
// side +x. Each view puts the camera along a direction from the kiln's centre.
const VIEWS: [View, string, [number, number, number]][] = [
  ["3d", "3D", [1, 0.7, 1.2]],
  ["front", "Front", [0, 0, 1]],
  ["side", "Side", [1, 0, 0]],
  ["top", "Top", [0, 1, 0.01]], // just off straight down, where the orbit controls can't turn
];

// Keeps the back half: the kiln cut across its middle, seen from the front, shows every layer.
const CUT = new Plane(new Vector3(0, 0, -1), 0);

/**
 * A part's name as the engine wrote it ("left/1-ifb-jm26"). three.js tidies `name` and keeps the
 * original in `userData.name`, on the part's node: a part with several primitives is a group of
 * meshes, so look up from the mesh that was hit.
 */
function partName(object: Object3D): string {
  for (let o: Object3D | null = object; o; o = o.parent) {
    if (typeof o.userData.name === "string") return o.userData.name;
  }
  return object.name;
}

/**
 * The model is loaded here, outside the canvas, so a model that can't be loaded is a message and
 * not an error thrown inside React Three Fiber, which reports every error it sees as uncaught.
 */
function useModel(url: string) {
  return useQuery({
    queryKey: ["models", url],
    queryFn: async () => {
      const { scene } = await new GLTFLoader().loadAsync(url);
      scene.traverse((object) => {
        if (!(object instanceof Mesh) || !(object.material instanceof MeshStandardMaterial)) return;
        // Each part gets its own material so it can be picked out. glTF's default
        // metallicFactor is 1, so the CAD export arrives as metal, which renders black wherever
        // it has nothing to reflect: brick, fibre and castable are matte.
        const material = object.material.clone();
        material.metalness = 0;
        material.roughness = 0.9;
        object.material = material;
        object.userData.builtColour = material.color.clone(); // for going back to "As built"
      });
      return scene;
    },
    staleTime: Infinity, // a build never changes
    retry: 1,
  });
}

/** What each part is, if the build says; older builds have no parts.json. */
function useParts(url: string) {
  return useQuery({
    queryKey: ["parts", url],
    queryFn: async () => {
      const response = await fetch(url);
      return response.ok ? ((await response.json()) as Record<string, PartInfo>) : {};
    },
    staleTime: Infinity,
  });
}

function NotShown() {
  return (
    <p className="error viewer-message" role="alert">
      The 3D model could not be shown. The files below can still be downloaded.
    </p>
  );
}

/** Keeps a browser that can't draw in 3D (no WebGL) from taking the page down. */
class CanvasBoundary extends Component<{ children: ReactNode }, { failed: boolean }> {
  override state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  override render() {
    return this.state.failed ? <NotShown /> : this.props.children;
  }
}

/**
 * Moves the camera, smoothly, to frame the kiln from the view's direction. The orbit controls
 * keep the camera within a few fits of the kiln, so the camera is sent straight to the framing
 * distance rather than placed far out and pulled in.
 */
function Aim({ view }: { view: View }) {
  const bounds = useBounds();
  useEffect(() => {
    const [x, y, z] = VIEWS.find(([id]) => id === view)?.[2] ?? [1, 1, 1];
    const { center, distance } = bounds.refresh().getSize();
    const position = new Vector3(x, y, z).normalize().multiplyScalar(distance).add(center);
    bounds.moveTo(position).lookAt({ target: center, up: [0, 1, 0] });
  }, [view, bounds]);
  return null;
}

function meshes(scene: Group): Mesh[] {
  const found: Mesh[] = [];
  scene.traverse((o) => {
    if (o instanceof Mesh && o.material instanceof MeshStandardMaterial) found.push(o);
  });
  return found;
}

type Outline = LineSegments<EdgesGeometry, LineBasicMaterial>;

const PICKED_LINE = "#e8833a";

/**
 * The page's text colour, which stands out against the viewer's background in either theme: a
 * wireframe's lines have no faces behind them. Read again when the theme changes.
 */
function useInk(): string {
  const read = () => getComputedStyle(document.documentElement).getPropertyValue("--text").trim();
  const [ink, setInk] = useState(read);
  useEffect(() => {
    const update = () => setInk(read());
    const themed = new MutationObserver(update);
    themed.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    const dark = matchMedia("(prefers-color-scheme: dark)");
    dark.addEventListener("change", update);
    return () => {
      themed.disconnect();
      dark.removeEventListener("change", update);
    };
  }, []);
  return ink;
}

/** The node that carries a part's name: the mesh, or the group of its primitives. */
function partNode(object: Object3D): Object3D {
  for (let o: Object3D | null = object; o; o = o.parent) {
    if (typeof o.userData.name === "string") return o;
  }
  return object;
}

/**
 * Every part's outline, made the first time outlines are shown and kept on the scene. A part's
 * primitives are merged first, so the outline follows the part's edges, not the seams between its
 * primitives (a curved face arrives as many).
 */
function outlines(scene: Group): Outline[] {
  const kept = scene.userData.outlines as Outline[] | undefined;
  if (kept) return kept;
  scene.updateMatrixWorld(true);
  const byPart = new Map<Object3D, BufferGeometry[]>();
  for (const mesh of meshes(scene)) {
    const node = partNode(mesh);
    const toNode = node.matrixWorld.clone().invert().multiply(mesh.matrixWorld);
    const shape = new BufferGeometry();
    shape.setAttribute("position", mesh.geometry.getAttribute("position").clone());
    shape.setIndex(mesh.geometry.getIndex()?.clone() ?? null);
    byPart.set(node, [...(byPart.get(node) ?? []), shape.applyMatrix4(toNode)]);
  }
  const made: Outline[] = [];
  for (const [node, shapes] of byPart) {
    const merged = mergeVertices(mergeGeometries(shapes.map((g) => g.toNonIndexed())));
    const lines = new LineSegments(new EdgesGeometry(merged, 25), new LineBasicMaterial());
    lines.raycast = () => {}; // clicks go to the part, not its outline
    node.add(lines);
    made.push(lines);
  }
  scene.userData.outlines = made;
  return made;
}

function Model({
  scene,
  parts,
  look,
  cut,
  wire,
  ink,
  faintBurners,
  selected,
  onSelect,
}: {
  scene: Group;
  parts: Record<string, PartInfo>;
  look: ViewerLook;
  cut: boolean;
  /** Only the parts' outlines, seen through: a skeleton of the kiln, drawn in ``ink``. */
  wire: boolean;
  ink: string;
  /** While ports are moved: a burner stands in front of its port, and stays where it was built
   * until the design is built again, so it's drawn faint and the port is what's picked up. */
  faintBurners: boolean;
  selected: string | null;
  onSelect: (name: string) => void;
}) {
  useEffect(() => {
    const { edges: onFaces, background } = palette(look.palette);
    // A palette with its own background has edges to suit it; otherwise the theme's text colour
    const edges = wire && !background ? ink : onFaces;
    for (const mesh of meshes(scene)) {
      const material = mesh.material as MeshStandardMaterial;
      const name = partName(mesh);
      material.clippingPlanes = cut ? [CUT] : [];
      material.emissive.set(name === selected ? "#8a3a10" : "#000000");
      const colour = colourOf(look, parts[name]?.kind);
      if (colour) material.color.set(colour);
      else if (mesh.userData.builtColour instanceof Color) material.color.copy(mesh.userData.builtColour);
      const faint = faintBurners && name.startsWith("burner/");
      if (material.transparent !== faint) {
        material.transparent = faint;
        material.depthWrite = !faint;
        material.needsUpdate = true;
      }
      material.opacity = faint ? 0.25 : 1;
      material.visible = !wire; // hidden faces can still be clicked
    }
    if (look.edges || wire || scene.userData.outlines) {
      for (const lines of outlines(scene)) {
        lines.visible = look.edges || wire;
        // With no faces to light up, the part picked is picked out by its outline
        lines.material.color.set(wire && partName(lines) === selected ? PICKED_LINE : edges);
        lines.material.clippingPlanes = cut ? [CUT] : [];
      }
    }
  }, [scene, parts, look, cut, wire, ink, faintBurners, selected]);

  const pick = (event: ThreeEvent<MouseEvent>) => {
    // A click on a port's marker is the marker's, even where a part (a burner) stands in front
    if (event.intersections.some((i) => i.object.userData.port === true)) return;
    event.stopPropagation();
    // A cut hides the front half but doesn't stop it being hit: take the first part showing.
    const hit = event.intersections.find((i) => !cut || CUT.distanceToPoint(i.point) >= 0);
    if (hit) onSelect(partName(hit.object));
  };
  return <primitive object={scene} onClick={pick} />;
}

const NO_PARTS: Record<string, PartInfo> = {};

export function KilnViewer({
  url,
  partsUrl,
  layout,
  draft,
  onEdit,
}: {
  url: string;
  partsUrl: string;
  /** Where the build put the ports: with `onEdit`, they can be moved on the model. */
  layout?: Layout;
  /** The design as it is being edited, so the ports show where it now puts them. */
  draft?: KilnDocument | null;
  onEdit?: (apply: (document: KilnDocument) => KilnDocument) => void;
}) {
  const model = useModel(url);
  const parts = useParts(partsUrl);
  const [view, setView] = useState<View>("3d");
  const [cut, setCut] = useState(false);
  const [wire, setWire] = useState(false);
  const ink = useInk();
  const [selected, setSelected] = useState<string | null>(null);
  const [look, setLook] = useState<ViewerLook>(loadLook);
  const [moving, setMoving] = useState(false);
  // While moving ports: a drag that misses a port doesn't turn the model (it can still zoom)
  const [still, setStill] = useState(false);
  const [hovered, setHovered] = useState<string | null>(null);
  // The marker last pressed, which can be removed if it's a spy hole; and adding a spy hole
  const [picked, setPicked] = useState<string | null>(null);
  const [adding, setAdding] = useState(false);
  const movable = layout !== undefined && onEdit !== undefined && layout.ports.length > 0;
  const all = useMemo(() => (layout ? markers(layout, draft) : []), [layout, draft]);
  const pickedSpy = all.find((m) => m.key === picked && m.kind === "spy");
  const spy = spyWord(layout?.ports ?? []).toLowerCase();
  // A spy hole added is the size of those built
  const canAdd = layout?.ports.some((p) => p.kind === "spy") ?? false;
  const info = selected ? parts.data?.[selected] : undefined;
  const changeLook = (next: ViewerLook) => {
    setLook(next);
    saveLook(next);
  };
  const background = palette(look.palette).background;

  if (model.isError) {
    return (
      <div className="viewer" aria-label="3D model of the kiln">
        <NotShown />
      </div>
    );
  }
  return (
    <div className="viewer" aria-label="3D model of the kiln" style={background ? { background } : undefined}>
      <CanvasBoundary>
        <Canvas
          camera={{ position: [3, 2, 3], fov: 35, near: 1, far: 1e7 }}
          onCreated={({ gl }) => {
            gl.localClippingEnabled = true;
          }}
          onPointerMissed={() => {
            setSelected(null);
            setPicked(null);
          }}
        >
          <hemisphereLight args={["#ffffff", "#8a8070", 1.4]} />
          <directionalLight position={[5, 10, 7]} intensity={1.6} />
          <directionalLight position={[-6, 3, -4]} intensity={0.5} />
          {model.data && (
            <Bounds fit clip margin={1.35}>
              <Model
                scene={model.data}
                parts={parts.data ?? NO_PARTS}
                look={look}
                cut={cut}
                wire={wire}
                ink={ink}
                faintBurners={movable && moving}
                selected={selected}
                // While ports are moved, a click on the model lets go of the marker picked
                onSelect={(name) => (moving ? setPicked(null) : setSelected(name))}
              />
              <Aim view={view} />
            </Bounds>
          )}
          {model.data && movable && moving && (
            <PortMarkers
              layout={layout}
              all={all}
              picked={picked}
              adding={adding}
              onHover={setHovered}
              onPick={setPicked}
              onDrop={(marker, all, to) =>
                onEdit((doc) => moved(doc, all, marker, to, layout.units))
              }
              onAdd={(to) => {
                onEdit((doc) => added(doc, all, to, layout.units));
                setAdding(false);
              }}
            />
          )}
          {/* Zooms toward what's under the pointer, so a port a few pixels across can be zoomed to */}
          <OrbitControls makeDefault zoomToCursor enableRotate={!(movable && moving && still)} />
        </Canvas>
      </CanvasBoundary>
      <div className="viewer-tools" role="toolbar" aria-label="View">
        {VIEWS.map(([id, label]) => (
          <button
            key={id}
            type="button"
            aria-pressed={view === id}
            className={view === id ? "active" : undefined}
            onClick={() => setView(id)}
          >
            {label}
          </button>
        ))}
        <button
          type="button"
          aria-pressed={cut}
          className={cut ? "active" : undefined}
          onClick={() => setCut(!cut)}
        >
          Cut in half
        </button>
        <button
          type="button"
          aria-pressed={look.edges}
          className={look.edges ? "active" : undefined}
          onClick={() => changeLook({ ...look, edges: !look.edges })}
        >
          Outlines
        </button>
        <button
          type="button"
          aria-pressed={wire}
          className={wire ? "active" : undefined}
          onClick={() => setWire(!wire)}
        >
          Wireframe
        </button>
        {movable && (
          <button
            type="button"
            aria-pressed={moving}
            className={moving ? "active" : undefined}
            onClick={() => {
              setMoving(!moving);
              setHovered(null);
              setSelected(null);
              setPicked(null);
              setAdding(false);
            }}
          >
            Move ports
          </button>
        )}
        {movable && moving && (
          <>
            <label className="viewer-check">
              <input type="checkbox" checked={still} onChange={(e) => setStill(e.target.checked)} />
              Stop turning
            </label>
            <button
              type="button"
              aria-pressed={adding}
              className={adding ? "active" : undefined}
              disabled={!canAdd}
              title={canAdd ? undefined : `Build with a ${spy} first: one added is the size of those built`}
              onClick={() => {
                setAdding(!adding);
                setPicked(null);
              }}
            >
              Add a {spy}
            </button>
            {pickedSpy && (
              <button
                type="button"
                onClick={() => {
                  onEdit((doc) => removed(doc, all, pickedSpy, layout.units));
                  setPicked(null);
                }}
              >
                Remove {pickedSpy.title.toLowerCase()}
              </button>
            )}
          </>
        )}
        <select
          aria-label="Model colours"
          value={look.palette}
          onChange={(e) => changeLook({ ...look, palette: e.target.value as PaletteId })}
        >
          {PALETTES.map((p) => (
            <option key={p.id} value={p.id}>
              {p.label}
            </option>
          ))}
        </select>
      </div>
      {parts.data && legend(parts.data).length > 0 && (
        <div className="viewer-legend">
          <ul aria-label="Materials in the model">
            {legend(parts.data).map(([kind, built]) => (
              <li key={kind}>
                <input
                  type="color"
                  className="swatch"
                  aria-label={`Colour for ${kind}`}
                  value={colourOf(look, kind) ?? built}
                  onChange={(e) =>
                    changeLook({ ...look, custom: { ...look.custom, [kind]: e.target.value } })
                  }
                />
                {kind}
              </li>
            ))}
          </ul>
          {Object.keys(look.custom).length > 0 && (
            <button type="button" className="secondary" onClick={() => changeLook({ ...look, custom: {} })}>
              Reset colours
            </button>
          )}
        </div>
      )}
      <p className="viewer-info" role="status">
        {adding ? (
          <span>Click the wall where the new {spy} goes.</span>
        ) : moving && hovered ? (
          <span>{hovered}</span>
        ) : moving ? (
          <span className="muted">
            Drag a port across its wall or onto another, then save and build: orange is a
            burner's (the burner is faint), blue a spy hole, grey the flue, red didn't fit. Scroll
            over a port to zoom to it.
          </span>
        ) : selected ? (
          <>
            <strong>{info?.title ?? selected}</strong>
            {info?.detail && <span> {info.detail}</span>}
          </>
        ) : (
          <span className="muted">Drag to turn, scroll to zoom, click a part to see what it is.</span>
        )}
      </p>
    </div>
  );
}
