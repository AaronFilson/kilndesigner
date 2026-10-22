// The kiln's 3D model: the glTF the engine built (ADR 0005), framed to fit. Views from the front,
// the side and the top, a cut through the middle to show the lining, and the name of any part
// that's clicked.
import { Bounds, OrbitControls, useBounds } from "@react-three/drei";
import { Canvas, type ThreeEvent } from "@react-three/fiber";
import { useQuery } from "@tanstack/react-query";
import { Component, type ReactNode, useEffect, useState } from "react";
import { type Group, Mesh, MeshStandardMaterial, type Object3D, Plane, Vector3 } from "three";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

/** What a part of the model is: from the build's parts.json, by the part's name. */
export interface PartInfo {
  title: string;
  detail: string;
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

function Model({
  scene,
  cut,
  selected,
  onSelect,
}: {
  scene: Group;
  cut: boolean;
  selected: string | null;
  onSelect: (name: string) => void;
}) {
  useEffect(() => {
    scene.traverse((object) => {
      if (!(object instanceof Mesh) || !(object.material instanceof MeshStandardMaterial)) return;
      object.material.clippingPlanes = cut ? [CUT] : [];
      object.material.emissive.set(partName(object) === selected ? "#8a3a10" : "#000000");
    });
  }, [scene, cut, selected]);

  const pick = (event: ThreeEvent<MouseEvent>) => {
    event.stopPropagation();
    // A cut hides the front half but doesn't stop it being hit: take the first part showing.
    const hit = event.intersections.find((i) => !cut || CUT.distanceToPoint(i.point) >= 0);
    if (hit) onSelect(partName(hit.object));
  };
  return <primitive object={scene} onClick={pick} />;
}

export function KilnViewer({ url, partsUrl }: { url: string; partsUrl: string }) {
  const model = useModel(url);
  const parts = useParts(partsUrl);
  const [view, setView] = useState<View>("3d");
  const [cut, setCut] = useState(false);
  const [selected, setSelected] = useState<string | null>(null);
  const info = selected ? parts.data?.[selected] : undefined;

  if (model.isError) {
    return (
      <div className="viewer" aria-label="3D model of the kiln">
        <NotShown />
      </div>
    );
  }
  return (
    <div className="viewer" aria-label="3D model of the kiln">
      <CanvasBoundary>
        <Canvas
          camera={{ position: [3, 2, 3], fov: 35, near: 1, far: 1e7 }}
          onCreated={({ gl }) => {
            gl.localClippingEnabled = true;
          }}
          onPointerMissed={() => setSelected(null)}
        >
          <hemisphereLight args={["#ffffff", "#8a8070", 1.4]} />
          <directionalLight position={[5, 10, 7]} intensity={1.6} />
          <directionalLight position={[-6, 3, -4]} intensity={0.5} />
          {model.data && (
            <Bounds fit clip margin={1.35}>
              <Model scene={model.data} cut={cut} selected={selected} onSelect={setSelected} />
              <Aim view={view} />
            </Bounds>
          )}
          <OrbitControls makeDefault />
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
      </div>
      <p className="viewer-info" role="status">
        {selected ? (
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
