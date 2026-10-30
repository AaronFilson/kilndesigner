import { describe, expect, it } from "vitest";

import { at, css, extent, fraction, hours, linePath, rampColour, STOPS, ticks } from "./firing";

describe("chart helpers", () => {
  it("ticks at 1, 2 or 5 times a power of ten", () => {
    expect(ticks(0, 1300)).toEqual([0, 500, 1000]);
    expect(ticks(0, 10)).toEqual([0, 2, 4, 6, 8, 10]);
    expect(ticks(0.5, 0.9, 4)).toEqual([0.5, 0.6, 0.7, 0.8, 0.9]);
    expect(ticks(3, 3)).toEqual([3]);
  });

  it("spans every series, from zero unless asked not to", () => {
    const s = [{ label: "a", colour: "", points: [[1, 5], [3, 9]] as [number, number][] }];
    expect(extent(s, 1)).toEqual([0, 9]);
    expect(extent(s, 0, false)).toEqual([1, 3]);
    expect(extent([], 1)).toEqual([0, 1]);
    const flat = [{ label: "f", colour: "", points: [[0, -2]] as [number, number][] }];
    expect(extent(flat, 1)).toEqual([-2, -1]);
  });

  it("draws a path scaled into its box, y down", () => {
    expect(linePath([[0, 0], [10, 5]], [0, 10], [0, 5], 100, 50)).toBe("M0.0,50.0L100.0,0.0");
  });
});

describe("the heatmap's scale", () => {
  it("runs from the first stop to the last, clamped", () => {
    expect(rampColour(0)).toEqual(STOPS[0]);
    expect(rampColour(1)).toEqual(STOPS[STOPS.length - 1]);
    expect(rampColour(-3)).toEqual(STOPS[0]);
    expect(rampColour(0.125)[0]).toBeCloseTo((STOPS[0]![0] + STOPS[1]![0]) / 2);
    expect(css([1, 0, 0.5])).toBe("rgb(255, 0, 128)");
    expect(fraction(600, 0, 1200)).toBe(0.5);
    expect(fraction(5, 5, 5)).toBe(0);
  });

  it("reads a face's temperature between its cells, held at the ends", () => {
    const depths = [0.01, 0.03, 0.05];
    const temps = [1000, 800, 400];
    expect(at(depths, temps, 0)).toBe(1000);
    expect(at(depths, temps, 0.02)).toBeCloseTo(900);
    expect(at(depths, temps, 0.04)).toBeCloseTo(600);
    expect(at(depths, temps, 0.2)).toBe(400);
  });

  it("writes hours as hours and minutes", () => {
    expect(hours(5.4)).toBe("5 h 24 min");
    expect(hours(1.9999)).toBe("2 h 00 min");
  });
});
