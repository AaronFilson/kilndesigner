// The wall heatmap's scene, drawn by React Three Fiber's test renderer (no WebGL): the slabs, their
// textures and the shader's time uniform, which the scrubber moves.
import ReactThreeTestRenderer from "@react-three/test-renderer";
import type { DataTexture, Mesh, ShaderMaterial } from "three";
import { Euler, Vector3 } from "three";
import { afterEach, describe, expect, it } from "vitest";

import { FACES, map } from "./heatmap.fixture";
import { FRAGMENT, faceTexture, HeatmapScene, SAMPLES, slabs, timeCoordinate, VERTEX } from "./WallHeatmap";

const inside = FACES.map(() => 1);

let renderer: Awaited<ReturnType<typeof ReactThreeTestRenderer.create>> | null = null;

afterEach(async () => {
  await renderer?.unmount();
  renderer = null;
});

describe("the heatmap's textures", () => {
  it("are the temperatures resampled through the thickness, as fractions of the range", () => {
    const data = faceTexture(map, 0);
    expect(data).toHaveLength(SAMPLES * 2);
    expect(data[0]).toBe(0); // cold at the start
    expect(data[SAMPLES]).toBeCloseTo(1); // the hot face at the end
    expect(data[2 * SAMPLES - 1]).toBeCloseTo((100 - 20) / 980);
    expect(faceTexture({ ...map, max_c: 20 }, 0)[0]).toBe(0); // a flat range doesn't divide by zero
  });

  it("put the scrubber's time at a row's centre", () => {
    expect(timeCoordinate(0, 2)).toBe(0.25);
    expect(timeCoordinate(1, 2)).toBe(0.75);
    expect(timeCoordinate(0, 1)).toBe(0.5);
  });

  it("are read by a shader that colours by depth and time", () => {
    expect(VERTEX).toContain("vDepth = position.z + 0.5");
    expect(FRAGMENT).toContain("texture2D(uTemps, vec2(clamp(vDepth, 0.0, 1.0), uTime))");
    expect(FRAGMENT).toContain("vec3 stops[5]");
  });
});

describe("the slabs", () => {
  it("sit outside a chamber of the faces' mean area, each turned to face outwards", () => {
    const built = slabs(map, FACES.map(() => 1), FACES);
    expect(built.map((s) => s.face)).toEqual(FACES);
    for (const s of built) {
      expect(s.size).toBe(1);
      expect(s.thickness).toBeCloseTo(0.1);
      // The slab's local +z (hot face to shell) points the way it was placed from the centre
      const position = new Vector3(...s.position);
      expect(position.length()).toBeCloseTo(0.55);
      const out = new Vector3(0, 0, 1).applyEuler(new Euler(...s.rotation));
      expect(out.distanceTo(position.clone().normalize())).toBeLessThan(1e-9);
    }
    expect(slabs(map, [1], ["left"]).map((s) => s.face)).toEqual(["left"]);
    expect(slabs({ ...map, walls: ["oven", ...FACES.slice(1)] }, [1], FACES)).toHaveLength(5);
  });
});

describe("HeatmapScene, in the scene", () => {
  it("draws a slab a face, and moves the shader's time with the scrubber", async () => {
    renderer = await ReactThreeTestRenderer.create(
      <HeatmapScene map={map} inside={inside} time={0} show={FACES} />,
    );
    const meshes = renderer.scene.findAll((n) => n.type === "Mesh");
    expect(meshes.map((m) => (m.instance as Mesh).name)).toEqual(FACES);
    const material = (meshes[0]!.instance as Mesh).material as ShaderMaterial;
    expect(material.uniforms.uTime!.value).toBe(0.25);
    const texture = material.uniforms.uTemps!.value as DataTexture;
    expect([texture.image.width, texture.image.height]).toEqual([SAMPLES, 2]);
    // Scrubbing moves the uniform on the same material: the textures aren't rebuilt
    await renderer.update(<HeatmapScene map={map} inside={inside} time={1} show={FACES} />);
    expect(material.uniforms.uTime!.value).toBe(0.75);
    expect((renderer.scene.findAll((n) => n.type === "Mesh")[0]!.instance as Mesh).material).toBe(material);
    // Fewer faces shown: rebuilt, and the old textures let go
    await renderer.update(<HeatmapScene map={map} inside={inside} time={1} show={["left"]} />);
    expect(renderer.scene.findAll((n) => n.type === "Mesh")).toHaveLength(1);
  });
});
