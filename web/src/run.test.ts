import { Ray, Vector3 } from "three";
import { describe, expect, it } from "vitest";

import type { Layout, RunInfo, WallFrame } from "./design";
import { placePoint, roundHit, wallMatrix, wallPoint } from "./run";
import { fit, wallHit } from "./components/PortMarkers";

const frame = (origin: [number, number, number], normal: [number, number, number], right: [number, number, number]): WallFrame => ({
  origin,
  normal,
  right,
  half_width: 500,
  thickness: 100,
  top: [
    [-500, 1000],
    [500, 1000],
  ],
});

const run: RunInfo = {
  round: false,
  radius: null,
  chambers: 3,
  depth: 1000,
  chamber_pitch: 1200,
  slope: 0,
  bend: 0,
  length: 3400,
};

function layoutOf(r: RunInfo | undefined): Layout {
  return {
    units: "us",
    walls: {
      front: frame([0, -600, 0], [0, -1, 0], [1, 0, 0]),
      back: frame([0, 600, 0], [0, 1, 0], [-1, 0, 0]),
      left: frame([-600, 0, 0], [-1, 0, 0], [0, -1, 0]),
      right: frame([600, 0, 0], [1, 0, 0], [0, 1, 0]),
    },
    ports: [],
    run: r,
  };
}

const near = (a: Vector3, b: [number, number, number]) => {
  expect(a.x).toBeCloseTo(b[0], 6);
  expect(a.y).toBeCloseTo(b[1], 6);
  expect(a.z).toBeCloseTo(b[2], 6);
};

describe("placePoint", () => {
  it("leaves a straight, level run alone", () => {
    near(placePoint(run, new Vector3(1, 2, 3)), [1, 2, 3]);
  });

  it("climbs with the slope from the front face's foot", () => {
    const p = placePoint({ ...run, slope: 30 }, new Vector3(0, -500 + 1000, 0));
    near(p, [0, -500 + 1000 * Math.cos(Math.PI / 6), 500]);
  });

  it("bends round an arc to the left, and carries on straight beyond it", () => {
    const bent = { ...run, bend: 90 };
    const rho = run.length / (Math.PI / 2);
    near(placePoint(bent, new Vector3(0, -500 + run.length, 0)), [-rho, -500 + rho, 0]);
    near(placePoint(bent, new Vector3(0, -500 + run.length + 100, 0)), [-rho - 100, -500 + rho, 0]);
    near(placePoint(bent, new Vector3(0, -600, 0)), [0, -600, 0]);
  });
});

describe("walls on a run of chambers", () => {
  it("puts the flue end's wall at the end of the run, and the others where they were", () => {
    const layout = layoutOf(run);
    near(wallPoint(layout, "back", 0, 0).point, [0, 600 + 2 * 1200, 0]);
    near(wallPoint(layout, "front", 10, 20).point, [10, -600, 20]);
    expect(wallMatrix(layoutOf(undefined), "back").equals(wallMatrix(layoutOf(undefined), "front"))).toBe(true);
  });

  it("tilts the walls with the slope, and finds a port dragged on a tilted wall", () => {
    const layout = layoutOf({ ...run, slope: 20 });
    const { point, normal } = wallPoint(layout, "back", 100, 300, 50);
    expect(normal.z).toBeCloseTo(Math.sin((20 * Math.PI) / 180), 6);
    const ray = new Ray(point.clone().add(normal.clone().multiplyScalar(1000)), normal.clone().negate());
    const hit = wallHit(layout, ray, { kind: "spy", width: 50, height: 50 });
    expect(hit?.wall).toBe("back");
    expect(hit?.across).toBeCloseTo(fit(layout, "back", 100, 300, { kind: "spy", width: 50, height: 50 }).across);
    expect(hit?.up).toBeCloseTo(300, -1);
  });
});

describe("walls on a round chamber", () => {
  const round: RunInfo = { ...run, round: true, radius: 1000, chambers: 1 };
  const layout = layoutOf(round);

  it("puts ports round the curve, across measured along it", () => {
    near(wallPoint(layout, "front", 0, 200).point, [0, -1100, 200]);
    const quarter = wallPoint(layout, "front", (1000 * Math.PI) / 2, 200);
    near(quarter.point, [1100, 0, 200]);
    near(quarter.normal, [1, 0, 0]);
    expect(wallMatrix(layout, "front").equals(wallMatrix(layoutOf(undefined), "front"))).toBe(true);
  });

  it("finds where a ray meets the curve, and which wall's quarter it's in", () => {
    const at = (a: number) => new Ray(new Vector3(5000 * Math.cos(a), 5000 * Math.sin(a), 300), new Vector3(-Math.cos(a), -Math.sin(a), 0));
    const hit = roundHit(layout, at(-Math.PI / 2 + 0.2));
    expect(hit?.wall).toBe("front");
    expect(hit?.across).toBeCloseTo(200, 6);
    expect(hit?.up).toBeCloseTo(300, 6);
    expect(roundHit(layout, at(Math.PI))?.wall).toBe("left");
    expect(wallHit(layout, at(0.1), { kind: "spy", width: 50, height: 50 })?.wall).toBe("right");
  });

  it("misses rays that go straight up, pass by, start inside or point away, or are too high", () => {
    expect(roundHit(layout, new Ray(new Vector3(0, -5000, 0), new Vector3(0, 0, 1)))).toBeNull();
    expect(roundHit(layout, new Ray(new Vector3(5000, -5000, 0), new Vector3(0, 1, 0)))).toBeNull();
    expect(roundHit(layout, new Ray(new Vector3(0, -5000, 0), new Vector3(0, -1, 0)))).toBeNull();
    const high = new Ray(new Vector3(0, -5000, 9000), new Vector3(0, 1, 0));
    expect(wallHit(layout, high, { kind: "spy", width: 50, height: 50 })).toBeNull();
    const low = new Ray(new Vector3(0, -5000, -50), new Vector3(0, 1, 0));
    expect(wallHit(layout, low, { kind: "spy", width: 50, height: 50 })).toBeNull();
    expect(roundHit({ ...layout, run: { ...round, radius: null } }, new Ray(new Vector3(0, -5000, 0), new Vector3(0, 1, 0)))?.across).toBe(0);
  });
});
