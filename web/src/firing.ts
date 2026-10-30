// What the firing's charts and the wall heatmap draw, as plain functions the tests can check.

/** A line on a chart: its points, in data units. */
export interface Series {
  label: string;
  colour: string;
  points: [number, number][];
  dashed?: boolean;
}

/** Round, readable tick values covering [lo, hi]: 1, 2 or 5 times a power of ten apart. */
export function ticks(lo: number, hi: number, count = 5): number[] {
  if (!(hi > lo)) return [lo];
  const raw = (hi - lo) / count;
  const power = 10 ** Math.floor(Math.log10(raw));
  const step = [1, 2, 5, 10].map((m) => m * power).find((s) => s >= raw)!;
  const out: number[] = [];
  for (let v = Math.ceil(lo / step) * step; v <= hi + step * 1e-9; v += step) {
    out.push(Number(v.toPrecision(12)));
  }
  return out;
}

/** The range of every point's y (or x), padded to start at zero when all are above it. */
export function extent(series: Series[], axis: 0 | 1, fromZero = true): [number, number] {
  const values = series.flatMap((s) => s.points.map((p) => p[axis]));
  if (!values.length) return [0, 1];
  let lo = Math.min(...values);
  const hi = Math.max(...values);
  if (fromZero && lo > 0) lo = 0;
  return hi > lo ? [lo, hi] : [lo, lo + 1];
}

/** An SVG path through the points, scaled into a box of ``width`` × ``height`` (y down). */
export function linePath(
  points: [number, number][],
  [x0, x1]: [number, number],
  [y0, y1]: [number, number],
  width: number,
  height: number,
): string {
  return points
    .map(([x, y], i) => {
      const px = ((x - x0) / (x1 - x0)) * width;
      const py = height - ((y - y0) / (y1 - y0)) * height;
      return `${i ? "L" : "M"}${px.toFixed(1)},${py.toFixed(1)}`;
    })
    .join("");
}

/** Colour stops of the heatmap scale, cool to hot: a perceptual "inferno"-like ramp. The shader
 * uses the same stops. */
export const STOPS: [number, number, number][] = [
  [0.0, 0.0, 0.016],
  [0.341, 0.063, 0.431],
  [0.733, 0.216, 0.329],
  [0.976, 0.557, 0.035],
  [0.988, 1.0, 0.643],
];

/** The scale's colour at ``f`` (0 cold to 1 hot), as r, g, b in 0–1. */
export function rampColour(f: number): [number, number, number] {
  const t = Math.min(Math.max(f, 0), 1) * (STOPS.length - 1);
  const i = Math.min(Math.floor(t), STOPS.length - 2);
  const u = t - i;
  const a = STOPS[i]!;
  const b = STOPS[i + 1]!;
  return [a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u];
}

export const css = ([r, g, b]: [number, number, number]) =>
  `rgb(${Math.round(r * 255)}, ${Math.round(g * 255)}, ${Math.round(b * 255)})`;

/** A temperature as a fraction of the heatmap's range. */
export const fraction = (t: number, lo: number, hi: number) => (hi > lo ? (t - lo) / (hi - lo) : 0);

/** A face's temperature at a depth (m), linear between its cells' centres, held at the ends. */
export function at(depths: number[], temps: number[], depth: number): number {
  if (depth <= depths[0]!) return temps[0]!;
  for (let i = 1; i < depths.length; i++) {
    if (depth <= depths[i]!) {
      const u = (depth - depths[i - 1]!) / (depths[i]! - depths[i - 1]!);
      return temps[i - 1]! + (temps[i]! - temps[i - 1]!) * u;
    }
  }
  return temps[temps.length - 1]!;
}

/** "5 h 24 min" from hours. */
export function hours(h: number): string {
  const whole = Math.floor(h);
  const minutes = Math.round((h - whole) * 60);
  return minutes === 60 ? `${whole + 1} h 00 min` : `${whole} h ${String(minutes).padStart(2, "0")} min`;
}
