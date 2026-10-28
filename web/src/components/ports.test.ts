import { Ray, Vector3 } from "three";
import { describe, expect, it } from "vitest";

import type { KilnDocument, Layout, WallFrame } from "../design";
import { fit, markers, moved, topAt, wallHit } from "./PortMarkers";

const IN = 25.4;
const inches = (mm: number) => Math.round((mm / IN) * 1000) / 1000;
const inchesOf = (at: Record<string, number>) =>
  Object.fromEntries(Object.entries(at).map(([k, v]) => [k, inches(v)]));

function wall(
  origin: [number, number, number],
  normal: [number, number, number],
  right: [number, number, number],
  half: number,
  arch: number,
): WallFrame {
  return {
    origin,
    normal,
    right,
    half_width: half,
    thickness: 8 * IN,
    top: [
      [-half, 40 * IN],
      [0, (40 + arch) * IN], // an end wall rises under the arch in the middle
      [half, 40 * IN],
    ],
  };
}

// A 28 × 48 in chamber with 8 in walls, as the gas example's layout.json has it
const layout: Layout = {
  units: "us",
  walls: {
    front: wall([0, -32 * IN, 0], [0, -1, 0], [1, 0, 0], 14 * IN, 4),
    back: wall([0, 32 * IN, 0], [0, 1, 0], [-1, 0, 0], 14 * IN, 4),
    left: wall([-22 * IN, 0, 0], [-1, 0, 0], [0, -1, 0], 24 * IN, 0),
    right: wall([22 * IN, 0, 0], [1, 0, 0], [0, 1, 0], 24 * IN, 0),
  },
  ports: [
    { name: "port/burner-1", title: "Burner port 1", kind: "burner", wall: "front", across: -7 * IN,
      up: 5 * IN, width: 4 * IN, height: 4 * IN, round: true, cut: true },
    { name: "port/burner-2", title: "Burner port 2", kind: "burner", wall: "front", across: 7 * IN,
      up: 5 * IN, width: 4 * IN, height: 4 * IN, round: true, cut: true },
    { name: "port/flue", title: "Flue port", kind: "flue", wall: "back", across: 0, up: 3.75 * IN,
      width: 11 * IN, height: 7.5 * IN, round: false, cut: true },
  ], // prettier-ignore
};

const doc: KilnDocument = {
  name: "Test",
  firing: { cone: "10" },
  chamber: { width: "28 in", depth: "48 in", height: "40 in" },
  lining: { walls: [{ material: "ifb-k23", thickness: "8 in" }] },
  heat: { gas: { burners: { wall: "front" }, supply: { type: "cylinders", count: 4 } } },
  draft: { type: "cross", flue_wall: "back" },
};

describe("markers", () => {
  it("are where the build put the ports, until the design places them", () => {
    expect(markers(layout, doc).map((m) => [m.key, m.wall, inches(m.across)])).toEqual([
      ["burner-0", "front", -7],
      ["burner-1", "front", 7],
      ["flue-0", "back", 0],
    ]);
    const placed: KilnDocument = {
      ...doc,
      heat: {
        gas: {
          ...doc.heat.gas!,
          burners: { places: [{ wall: "left", across: "3 in", up: "10 in" }] },
        },
      },
      draft: { type: "cross", flue_wall: "back", flue_across: "-5 in" },
    };
    const shown = markers(layout, placed);
    expect(shown.map((m) => [m.key, m.wall, inches(m.across), inches(m.up)])).toEqual([
      ["burner-0", "left", 3, 10],
      ["flue-0", "back", -5, 3.75],
    ]);
    expect(shown[0]?.width).toBe(4 * IN); // its size is the built one's
  });
});

describe("moved", () => {
  it("places every port of the kind, the moved one where it was dropped", () => {
    const all = markers(layout, doc);
    const next = moved(doc, all, all[1]!, { wall: "left", across: 6 * IN, up: 12 * IN }, "us");
    expect(next.heat.gas?.burners).toEqual({
      wall: "front",
      places: [
        { wall: "front", across: "-7 in", up: "5 in" },
        { wall: "left", across: "6 in", up: "12 in" },
      ],
    });
  });

  it("moves the flue, and its chimney with it, along a wall or onto another", () => {
    const all = markers(layout, doc);
    const next = moved(doc, all, all[2]!, { wall: "right", across: 100, up: 0 }, "metric");
    expect(next.draft).toEqual({ type: "cross", flue_wall: "right", flue_across: "100 mm" });
  });
});

describe("fit", () => {
  const burner = { kind: "burner" as const, width: 4 * IN, height: 4 * IN };

  it("keeps a port on its wall's inside face, snapped to a quarter inch", () => {
    expect(inchesOf(fit(layout, "front", 20 * IN, 1 * IN, burner))).toEqual({ across: 12, up: 2 });
    expect(inchesOf(fit(layout, "front", 1.1 * IN, 10.1 * IN, burner))).toEqual({
      across: 1,
      up: 10,
    });
    // Under the arch in the middle of the front wall, higher than at its sides
    expect(fit(layout, "front", 0, 100 * IN, burner).up).toBeGreaterThan(40 * IN);
    expect(inches(fit(layout, "left", 0, 100 * IN, burner).up)).toBe(38);
  });

  it("keeps the flue on the floor", () => {
    const flue = { kind: "flue" as const, width: 11 * IN, height: 7.5 * IN };
    expect(inches(fit(layout, "back", 0, 20 * IN, flue).up)).toBe(3.75);
  });

  it("reads the wall's height between its samples", () => {
    expect(topAt(layout, "front", 7 * IN)).toBeCloseTo(42 * IN);
    expect(topAt(layout, "front", 99 * IN)).toBe(40 * IN);
  });
});

describe("wallHit", () => {
  it("finds the wall a ray from the camera meets, from outside", () => {
    const burner = { kind: "burner" as const, width: 4 * IN, height: 4 * IN };
    const fromFront = new Ray(new Vector3(5 * IN, -100 * IN, 20 * IN), new Vector3(0, 1, 0));
    const hit = (ray: Ray) => {
      const found = wallHit(layout, ray, burner);
      return found && { wall: found.wall, ...inchesOf({ across: found.across, up: found.up }) };
    };
    expect(hit(fromFront)).toEqual({ wall: "front", across: 5, up: 20 });
    const fromLeft = new Ray(new Vector3(-100 * IN, -10 * IN, 6 * IN), new Vector3(1, 0, 0));
    // On the left wall, to the right facing it from outside is towards the front (-y)
    expect(hit(fromLeft)).toEqual({ wall: "left", across: 10, up: 6 });
    const away = new Ray(new Vector3(0, -100 * IN, 20 * IN), new Vector3(0, -1, 0));
    expect(wallHit(layout, away, burner)).toBeNull();
  });
});
