// A small heatmap for the tests: two moments, cold, then 1000 °C at the hot face falling to 100 °C
// at the shell, on all six faces.
import type { WallHeatmap } from "@kilndesigner/api-client";

export const FACES = ["left", "right", "back", "front", "floor", "roof"];

export const map: WallHeatmap = {
  times_h: [0, 5],
  walls: FACES,
  depths_m: FACES.map(() => [0.025, 0.075]),
  layers: FACES.map(() => ["ifb-jm26", "kaowool-blanket-8pcf"]),
  temperatures: [FACES.map(() => [20, 20]), FACES.map(() => [1000, 100])],
  min_c: 20,
  max_c: 1000,
};
