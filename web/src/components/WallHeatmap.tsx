// The walls' temperatures on a 3D kiln, coloured on the GPU. Each face is a slab as thick as its
// lining, around a chamber of its inside area. A face's temperatures through time are one float
// texture (depth across, time down); the fragment shader reads it at the slab's depth and the
// scrubber's time, and colours it on the scale in ../firing.ts. Scrubbing changes one uniform.
import type { WallHeatmap as Heatmap } from "@kilndesigner/api-client";
import { OrbitControls } from "@react-three/drei";
import { Canvas } from "@react-three/fiber";
import { useEffect, useMemo } from "react";
import {
  BoxGeometry,
  DataTexture,
  FloatType,
  LinearFilter,
  RedFormat,
  ShaderMaterial,
  Vector3,
} from "three";

import { at, STOPS } from "../firing";

/** Depth samples per face in its texture: the cells resampled evenly through the thickness. */
export const SAMPLES = 64;

/** The texture of one face: SAMPLES across (hot face to shell), one row per time, each value the
 * temperature as a fraction of the heatmap's range. */
export function faceTexture(map: Heatmap, face: number): Float32Array {
  const depths = map.depths_m[face]!;
  const thickness = depths[depths.length - 1]! + depths[0]!; // centres: the last plus half a cell
  const span = map.max_c - map.min_c || 1;
  const data = new Float32Array(SAMPLES * map.times_h.length);
  map.temperatures.forEach((faces, row) => {
    const temps = faces[face]!;
    for (let i = 0; i < SAMPLES; i++) {
      const depth = ((i + 0.5) / SAMPLES) * thickness;
      data[row * SAMPLES + i] = (at(depths, temps, depth) - map.min_c) / span;
    }
  });
  return data;
}

const glslStops = STOPS.map(([r, g, b]) => `vec3(${r.toFixed(3)}, ${g.toFixed(3)}, ${b.toFixed(3)})`);

export const VERTEX = /* glsl */ `
varying float vDepth;
void main() {
  vDepth = position.z + 0.5; // the slab runs from its hot face (z = -0.5) to its shell (0.5)
  gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}`;

export const FRAGMENT = /* glsl */ `
uniform sampler2D uTemps;
uniform float uTime; // 0 to 1, the scrubber
varying float vDepth;
vec3 ramp(float f) {
  vec3 stops[${STOPS.length}] = vec3[](${glslStops.join(", ")});
  float t = clamp(f, 0.0, 1.0) * ${(STOPS.length - 1).toFixed(1)};
  int i = int(min(floor(t), ${(STOPS.length - 2).toFixed(1)}));
  return mix(stops[i], stops[i + 1], t - float(i));
}
void main() {
  float f = texture2D(uTemps, vec2(clamp(vDepth, 0.0, 1.0), uTime)).r;
  gl_FragColor = vec4(ramp(f), 1.0);
}`;

/** Where each face's slab sits: its outward direction, and which axes its sides run along. */
const PLACES: Record<string, { normal: [number, number, number] }> = {
  left: { normal: [-1, 0, 0] },
  right: { normal: [1, 0, 0] },
  back: { normal: [0, 0, -1] },
  front: { normal: [0, 0, 1] },
  floor: { normal: [0, -1, 0] },
  roof: { normal: [0, 1, 0] },
};

export interface Slab {
  face: string;
  size: number; // m, the side of the square of the face's inside area
  thickness: number; // m
  position: [number, number, number];
  rotation: [number, number, number];
  material: ShaderMaterial;
}

/** The slabs, with their textures and shaders, for a heatmap; the chamber is a cube of the faces'
 * mean inside area (a schematic: the walls' own sizes are in the model tab). */
export function slabs(map: Heatmap, inside: number[], show: string[]): Slab[] {
  const side = Math.sqrt(inside.reduce((a, b) => a + b, 0) / Math.max(inside.length, 1));
  return map.walls.flatMap((face, i) => {
    const place = PLACES[face];
    if (!place || !show.includes(face)) return [];
    const depths = map.depths_m[i]!;
    const thickness = depths[depths.length - 1]! + depths[0]!;
    const texture = new DataTexture(faceTexture(map, i), SAMPLES, map.times_h.length, RedFormat, FloatType);
    texture.magFilter = texture.minFilter = LinearFilter;
    texture.needsUpdate = true;
    const material = new ShaderMaterial({
      uniforms: { uTemps: { value: texture }, uTime: { value: 0 } },
      vertexShader: VERTEX,
      fragmentShader: FRAGMENT,
    });
    const n = new Vector3(...place.normal);
    const centre = n.clone().multiplyScalar(side / 2 + thickness / 2);
    // The slab's local z is its depth: turn +z onto the face's outward normal
    const rotation: [number, number, number] =
      place.normal[0] !== 0
        ? [0, (place.normal[0] * Math.PI) / 2, 0]
        : place.normal[1] !== 0
          ? [(-place.normal[1] * Math.PI) / 2, 0, 0]
          : [0, place.normal[2] > 0 ? 0 : Math.PI, 0];
    return [
      {
        face,
        size: side,
        thickness,
        position: centre.toArray() as [number, number, number],
        rotation,
        material,
      },
    ];
  });
}

/** The row of the scrubber's time in the textures, 0 to 1 (texel centres). */
export function timeCoordinate(index: number, count: number): number {
  return count > 1 ? (index + 0.5) / count : 0.5;
}

export function HeatmapScene({ map, inside, time, show }: { map: Heatmap; inside: number[]; time: number; show: string[] }) {
  const built = useMemo(() => slabs(map, inside, show), [map, inside, show]);
  const geometry = useMemo(() => new BoxGeometry(1, 1, 1), []);
  useEffect(() => {
    for (const s of built) s.material.uniforms.uTime!.value = timeCoordinate(time, map.times_h.length);
  }, [built, time, map.times_h.length]);
  useEffect(
    () => () => {
      for (const s of built) {
        (s.material.uniforms.uTemps!.value as DataTexture).dispose();
        s.material.dispose();
      }
    },
    [built],
  );
  return (
    <group>
      {built.map((s) => (
        <mesh
          key={s.face}
          name={s.face}
          geometry={geometry}
          material={s.material}
          position={s.position}
          rotation={s.rotation}
          scale={[s.size, s.size, s.thickness]}
        />
      ))}
    </group>
  );
}

export function WallHeatmap({ map, inside, time, show }: { map: Heatmap; inside: number[]; time: number; show: string[] }) {
  const side = Math.sqrt(inside.reduce((a, b) => a + b, 0) / Math.max(inside.length, 1));
  return (
    <div className="heatmap-canvas">
      <Canvas camera={{ position: [side * 1.6, side * 1.1, side * 2.2], fov: 40 }}>
        <HeatmapScene map={map} inside={inside} time={time} show={show} />
        <OrbitControls makeDefault />
      </Canvas>
    </div>
  );
}
