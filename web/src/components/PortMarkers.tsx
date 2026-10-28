// Ports on the model that can be picked up and moved: each burner port, spy hole and flue is a
// marker on its wall's outside face, dragged across that wall or onto another. Where it's dropped
// becomes a place in the design, to save and build; the engine checks it fits (ADR 0005: the
// model is the engine's, so a moved port is only a marker until it's built).
import { type ThreeEvent, useFrame, useThree } from "@react-three/fiber";
import { useEffect, useRef, useState } from "react";
import { type Group, Matrix4, Mesh, type Ray, Raycaster, Vector2, Vector3 } from "three";

import {
  fromMm,
  type KilnDocument,
  type Layout,
  type Place,
  type PortKind,
  setIn,
  toMm,
  WALLS,
  type WallFace,
} from "../design";

/** A port as a marker: where it is now (the design's place, if it has one, or the build's). */
export interface Marker {
  key: string;
  kind: PortKind;
  index: number;
  title: string;
  wall: WallFace;
  across: number; // mm
  up: number; // mm
  width: number;
  height: number;
  round: boolean;
  cut: boolean;
}

type Moving = { key: string; wall: WallFace; across: number; up: number };

/** What a spy hole is called in this kiln ("Spy hole", or "Peephole" in an electric one). */
export function spyWord(ports: Pick<Marker, "kind" | "title">[]): string {
  return ports.find((p) => p.kind === "spy")?.title.replace(/\s*\d+$/, "") ?? "Spy hole";
}

const KIND_COLOURS: Record<PortKind, string> = {
  burner: "#e8833a",
  spy: "#3a8be8",
  flue: "#8c8c8c",
};

/** The places the design gives ports of one kind, if it places them one by one. */
function placesOf(doc: KilnDocument | null | undefined, kind: PortKind): Place[] | undefined {
  if (kind === "burner") return doc?.heat.gas?.burners?.places;
  if (kind === "spy") return doc?.spy_holes?.places;
  return undefined;
}

/** Each port, where the design (as edited, not yet built) or else the build puts it. */
export function markers(layout: Layout, doc: KilnDocument | null | undefined): Marker[] {
  const found: Marker[] = [];
  for (const kind of ["burner", "spy", "flue"] as const) {
    const spots = layout.ports.filter((p) => p.kind === kind);
    const first = spots[0];
    if (!first) continue;
    const places = placesOf(doc, kind);
    if (places) {
      places.forEach((place, i) => {
        const size = spots[i] ?? first;
        found.push({
          ...size,
          key: `${kind}-${i}`,
          kind,
          index: i,
          title: size === spots[i] ? size.title : `${first.title.replace(/\d+$/, "")}${i + 1}`,
          wall: place.wall,
          across: toMm(place.across ?? "0 in") ?? 0,
          up: toMm(place.up) ?? size.up,
        });
      });
      continue;
    }
    spots.forEach((spot, i) => {
      let { wall, across } = spot;
      if (kind === "flue" && doc?.draft) {
        wall = doc.draft.flue_wall ?? wall;
        across = doc.draft.flue_across === undefined ? 0 : (toMm(doc.draft.flue_across) ?? across);
      }
      found.push({ ...spot, key: `${kind}-${i}`, kind, index: i, wall, across });
    });
  }
  return found;
}

type Spot = { wall: WallFace; across: number; up: number };

function placeAt(at: Spot, units: Layout["units"]): Place {
  return { wall: at.wall, across: fromMm(at.across, units), up: fromMm(at.up, units) };
}

/** The design with the burners or the spy holes placed one by one, at ``places``. */
function placing(doc: KilnDocument, kind: "burner" | "spy", places: Place[]): KilnDocument {
  if (kind === "burner") {
    const burners = { ...doc.heat.gas?.burners, places, count: undefined };
    return setIn(doc, ["heat", "gas", "burners"], burners);
  }
  return setIn(doc, ["spy_holes"], { ...doc.spy_holes, places, count: undefined });
}

/** The design with one port moved: every port of its kind becomes a place, as they now are. */
export function moved(
  doc: KilnDocument,
  all: Marker[],
  marker: Marker,
  to: Spot,
  units: Layout["units"],
): KilnDocument {
  if (marker.kind === "flue") {
    const next = setIn(doc, ["draft", "flue_wall"], to.wall);
    return setIn(next, ["draft", "flue_across"], fromMm(to.across, units));
  }
  const places = all
    .filter((m) => m.kind === marker.kind)
    .map((m) => placeAt(m.key === marker.key ? to : m, units));
  return placing(doc, marker.kind, places);
}

/** The design with a spy hole added at ``to``: the others become places, as they now are. */
export function added(doc: KilnDocument, all: Marker[], to: Spot, units: Layout["units"]): KilnDocument {
  const places = all.filter((m) => m.kind === "spy").map((m) => placeAt(m, units));
  return placing(doc, "spy", [...places, placeAt(to, units)]);
}

/** The design without one spy hole: the others become places, as they now are. */
export function removed(
  doc: KilnDocument,
  all: Marker[],
  marker: Marker,
  units: Layout["units"],
): KilnDocument {
  const places = all.filter((m) => m.kind === "spy" && m.key !== marker.key).map((m) => placeAt(m, units));
  return placing(doc, "spy", places);
}

/** How high a wall's inside reaches at ``across`` (mm), between the layout's samples. */
export function topAt(layout: Layout, wall: WallFace, across: number): number {
  const top = layout.walls[wall].top;
  for (let i = 1; i < top.length; i++) {
    const [a0, z0] = top[i - 1]!;
    const [a1, z1] = top[i]!;
    if (across <= a1 || i === top.length - 1) {
      const t = a1 === a0 ? 0 : Math.min(1, Math.max(0, (across - a0) / (a1 - a0)));
      return z0 + t * (z1 - z0);
    }
  }
  return top[0]?.[1] ?? 0;
}

/** Where a ray (in the model's mm, z up) meets a wall's outside face, nearest first, if it does. */
export function wallHit(
  layout: Layout,
  ray: Ray,
  marker: Pick<Marker, "kind" | "width" | "height">,
): { wall: WallFace; across: number; up: number } | null {
  let best: { wall: WallFace; across: number; up: number; t: number } | null = null;
  for (const wall of WALLS) {
    const frame = layout.walls[wall];
    const normal = new Vector3(...frame.normal);
    const facing = ray.direction.dot(normal);
    if (facing >= 0) continue; // seen from inside, or edge on
    const origin = new Vector3(...frame.origin);
    const t = origin.clone().sub(ray.origin).dot(normal) / facing;
    if (t <= 0) continue;
    const hit = ray.at(t, new Vector3()).sub(origin);
    const across = hit.dot(new Vector3(...frame.right));
    const reach = frame.half_width + frame.thickness;
    if (Math.abs(across) > reach || hit.z < -frame.thickness || hit.z > topAt(layout, wall, 0) + reach) {
      continue;
    }
    if (best === null || t < best.t) best = { wall, across, up: hit.z, t };
  }
  if (best === null) return null;
  return { wall: best.wall, ...fit(layout, best.wall, best.across, best.up, marker) };
}

/** A position kept on the wall's inside face, snapped to ¼ in (or 5 mm in a metric design). */
export function fit(
  layout: Layout,
  wall: WallFace,
  across: number,
  up: number,
  marker: Pick<Marker, "kind" | "width" | "height">,
): { across: number; up: number } {
  const step = layout.units === "metric" ? 5 : 25.4 / 4;
  const snap = (v: number) => Math.round(v / step) * step;
  const half = layout.walls[wall].half_width - marker.width / 2;
  const a = Math.min(half, Math.max(-half, snap(across)));
  if (marker.kind === "flue") return { across: a, up: marker.height / 2 }; // it sits on the floor
  const edges = [a - marker.width / 2, a + marker.width / 2].map((x) => topAt(layout, wall, x));
  const top = Math.min(...edges) - marker.height / 2;
  return { across: a, up: Math.min(top, Math.max(marker.height / 2, snap(up))) };
}

type Point = { x: number; y: number };

/** A press and a release close enough to be a click: further apart, it's a drag that turns the
 * model. */
export function isClick(from: Point | null, to: Point): boolean {
  return from !== null && Math.hypot(to.x - from.x, to.y - from.y) <= 4;
}

/** A point on the canvas (client pixels) in normalised device coordinates, -1 to 1, y up. */
export function toDevice(at: Point, box: Pick<DOMRect, "left" | "top" | "width" | "height">): Vector2 {
  return new Vector2(((at.x - box.left) / box.width) * 2 - 1, -((at.y - box.top) / box.height) * 2 + 1);
}

function MarkerMesh({
  layout,
  marker,
  active,
  facing,
  onDown,
  onMove,
  onUp,
  onHover,
}: {
  layout: Layout;
  marker: Marker;
  active: boolean;
  /** Its wall faces the camera. Markers draw over the model (a burner can hide its port), so
   * those on the far walls are faint and can't be picked up through the kiln. */
  facing: boolean;
  onDown: (e: ThreeEvent<PointerEvent>) => void;
  onMove: (e: ThreeEvent<PointerEvent>) => void;
  onUp: (e: ThreeEvent<PointerEvent>) => void;
  onHover: (marker: Marker | null) => void;
}) {
  const frame = layout.walls[marker.wall];
  const depth = 12; // mm out from the face, so it shows over the hole
  const sideways = marker.wall === "left" || marker.wall === "right";
  const centre = new Vector3(...frame.origin)
    .add(new Vector3(...frame.right).multiplyScalar(marker.across))
    .add(new Vector3(0, 0, marker.up))
    .add(new Vector3(...frame.normal).multiplyScalar(depth / 2 + 1));
  const colour = marker.cut ? KIND_COLOURS[marker.kind] : "#d92d20";
  return (
    <mesh
      position={centre}
      rotation={marker.round && sideways ? [0, 0, Math.PI / 2] : [0, 0, 0]}
      renderOrder={10}
      userData={{ port: true }}
      raycast={facing || active ? Mesh.prototype.raycast : () => {}}
      onPointerDown={onDown}
      onPointerMove={onMove}
      onPointerUp={onUp}
      onPointerOver={(e) => {
        e.stopPropagation();
        onHover(marker);
      }}
      onPointerOut={() => onHover(null)}
      onClick={(e) => e.stopPropagation()}
    >
      {marker.round ? (
        <cylinderGeometry args={[marker.width / 2, marker.width / 2, depth, 32]} />
      ) : (
        <boxGeometry
          args={
            sideways
              ? [depth, marker.width, marker.height]
              : [marker.width, depth, marker.height]
          }
        />
      )}
      <meshStandardMaterial
        color={colour}
        emissive={active ? colour : "#000000"}
        emissiveIntensity={0.6}
        transparent
        depthTest={false}
        opacity={facing || active ? 0.95 : 0.2}
      />
    </mesh>
  );
}

/** A ray in the scene, in the markers' group: the model's millimetres, z up. */
function inModel(group: Group, ray: Ray): Ray {
  return ray.clone().applyMatrix4(new Matrix4().copy(group.matrixWorld).invert());
}

/** The markers, drawn in the model's own millimetres with z up, as the engine placed them. */
export function PortMarkers({
  layout,
  all,
  picked,
  adding,
  onDrop,
  onPick,
  onAdd,
  onHover,
}: {
  layout: Layout;
  /** The markers, where the design (as edited) puts them: see ``markers``. */
  all: Marker[];
  /** The marker last pressed, shown lit, for the viewer to offer to remove. */
  picked: string | null;
  /** A click on a wall adds a spy hole there. */
  adding: boolean;
  /** A marker was moved and let go: ``to`` is where, on which wall. */
  onDrop: (marker: Marker, all: Marker[], to: Spot) => void;
  onPick: (key: string) => void;
  onAdd: (to: Spot) => void;
  onHover: (text: string | null) => void;
}) {
  const controls = useThree((s) => s.controls) as { enabled: boolean } | null;
  const gl = useThree((s) => s.gl);
  const camera = useThree((s) => s.camera);
  const group = useRef<Group>(null);
  const add = useRef(onAdd);
  useEffect(() => {
    add.current = onAdd;
  });
  // One added is the size of those built; a build with none gives no size, so none is added
  const spy = layout.ports.find((p) => p.kind === "spy");
  // The canvas's own pointer events, so a click anywhere on a wall counts, whatever part of the
  // model is in front of it. Not a drag (that turns the model) nor a click on a marker (that
  // picks it up).
  useEffect(() => {
    if (!adding || !spy) return;
    const canvas = gl.domElement;
    let from: Point | null = null;
    const press = (e: PointerEvent) => {
      from = { x: e.clientX, y: e.clientY };
    };
    const release = (e: PointerEvent) => {
      const to = { x: e.clientX, y: e.clientY };
      if (!group.current || !isClick(from, to)) return;
      from = null;
      const raycaster = new Raycaster();
      raycaster.setFromCamera(toDevice(to, canvas.getBoundingClientRect()), camera);
      if (raycaster.intersectObject(group.current, true).length > 0) return;
      const hit = wallHit(layout, inModel(group.current, raycaster.ray), spy);
      if (hit) add.current(hit);
    };
    canvas.addEventListener("pointerdown", press);
    canvas.addEventListener("pointerup", release);
    return () => {
      canvas.removeEventListener("pointerdown", press);
      canvas.removeEventListener("pointerup", release);
    };
  }, [adding, spy, gl, camera, layout]);
  // Which walls face the camera, checked each frame and kept only when it changes
  const [facing, setFacing] = useState<string>("");
  useFrame(({ camera }) => {
    if (!group.current) return;
    const eye = group.current.worldToLocal(camera.position.clone());
    const seen = WALLS.filter((wall) => {
      const frame = layout.walls[wall];
      return eye.clone().sub(new Vector3(...frame.origin)).dot(new Vector3(...frame.normal)) > 0;
    }).join(" ");
    if (seen !== facing) setFacing(seen);
  });
  const [drag, setDrag] = useState<Moving | null>(null);
  // A marker dropped stays where it was dropped until the design it was dropped into comes back
  const [dropped, setDropped] = useState<Moving | null>(null);
  useEffect(() => setDropped(null), [all]);
  const held = drag ?? dropped;
  const shown = all.map((m) => (held && m.key === held.key ? { ...m, ...held } : m));

  const describe = (m: Marker) => {
    const at = (mm: number) => fromMm(mm, layout.units);
    const where = `${at(m.across)} across and ${at(m.up)} up the ${m.wall} wall`;
    const how = m.kind === "spy" ? "Drag it to move it, or click it to remove it." : "Drag it to move it.";
    return `${m.title}: ${where}${m.cut ? "" : " (it didn't fit, so it isn't cut)"}. ${how}`;
  };

  return (
    <group ref={group} rotation={[-Math.PI / 2, 0, 0]} scale={0.001}>
      {shown.map((m) => (
        <MarkerMesh
          key={m.key}
          layout={layout}
          marker={m}
          active={drag?.key === m.key || picked === m.key}
          facing={facing.split(" ").includes(m.wall)}
          onHover={(hovered) => onHover(hovered ? describe(hovered) : null)}
          onDown={(e) => {
            e.stopPropagation();
            (e.target as Element).setPointerCapture(e.pointerId);
            if (controls) controls.enabled = false;
            setDrag({ key: m.key, wall: m.wall, across: m.across, up: m.up });
            onPick(m.key);
          }}
          onMove={(e) => {
            if (drag?.key !== m.key || !group.current) return;
            e.stopPropagation();
            const hit = wallHit(layout, inModel(group.current, e.ray), m);
            if (hit) {
              setDrag({ key: m.key, ...hit });
              onHover(describe({ ...m, ...hit }));
            }
          }}
          onUp={(e) => {
            if (drag?.key !== m.key) return;
            e.stopPropagation();
            (e.target as Element).releasePointerCapture(e.pointerId);
            if (controls) controls.enabled = true;
            const original = all.find((x) => x.key === m.key);
            const changed =
              original &&
              (drag.wall !== original.wall || drag.across !== original.across || drag.up !== original.up);
            if (changed) {
              onDrop(original, all, drag);
              setDropped(drag);
            }
            setDrag(null);
          }}
        />
      ))}
    </group>
  );
}
