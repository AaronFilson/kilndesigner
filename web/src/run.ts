// Where a port on a wall is in the model, for kilns that aren't one level box: a round chamber's
// curved wall, or a run of chambers that climbs and bends (core massing.py, whose `place` this
// follows). The layout gives each wall's frame on the first chamber; the run moves it.
import { Matrix4, type Ray, Vector3 } from "three";

import type { Layout, RunInfo, WallFace } from "./design";

const DEG = Math.PI / 180;

/** Where a point laid out straight and level (mm) ends up once the run bends and climbs. */
export function placePoint(run: RunInfo, p: Vector3): Vector3 {
  let { x, y, z } = p;
  const front = -run.depth / 2;
  const s = y - front;
  const bend = run.bend * DEG;
  if (bend > 0 && s > 0) {
    const rho = run.length / bend;
    const a = Math.min(s, run.length) / rho;
    const beyond = Math.max(0, s - run.length);
    const nx = -rho + (rho + x) * Math.cos(a) - beyond * Math.sin(a);
    const ny = front + (rho + x) * Math.sin(a) + beyond * Math.cos(a);
    x = nx;
    y = ny;
  }
  const slope = run.slope * DEG;
  if (slope > 0) {
    const dy = y - front;
    const ny = front + dy * Math.cos(slope) - z * Math.sin(slope);
    z = dy * Math.sin(slope) + z * Math.cos(slope);
    y = ny;
  }
  return new Vector3(x, y, z);
}

/** The angle round a round chamber, anticlockwise from +x, at the middle of each wall. */
const BASE: Record<WallFace, number> = { front: -Math.PI / 2, right: 0, back: Math.PI / 2, left: Math.PI };

/** The affine map from a wall's frame in the layout to where the run puts it. Rigid at the frame's
 * origin: exact for the end walls, and for side walls of a run that doesn't bend. */
export function wallMatrix(layout: Layout, wall: WallFace): Matrix4 {
  const run = layout.run;
  if (!run || run.round) return new Matrix4();
  const frame = layout.walls[wall];
  const o = new Vector3(...frame.origin);
  // The flue end's wall is at the far end of the run, not the first chamber's back
  const shift = new Vector3(0, wall === "back" ? (run.chambers - 1) * run.chamber_pitch : 0, 0);
  const at = (d: Vector3) => placePoint(run, o.clone().add(shift).add(d));
  const o2 = at(new Vector3());
  const basis = [new Vector3(1, 0, 0), new Vector3(0, 1, 0), new Vector3(0, 0, 1)].map((d) =>
    at(d.clone().multiplyScalar(100)).sub(o2).divideScalar(100),
  ) as [Vector3, Vector3, Vector3];
  const linear = new Matrix4().makeBasis(...basis);
  return new Matrix4()
    .makeTranslation(o2.x, o2.y, o2.z)
    .multiply(linear)
    .multiply(new Matrix4().makeTranslation(-o.x, -o.y, -o.z));
}

/** A point on a wall's outside face, ``out`` mm proud of it, and its outward normal. */
export function wallPoint(
  layout: Layout,
  wall: WallFace,
  across: number,
  up: number,
  out = 0,
): { point: Vector3; normal: Vector3 } {
  const frame = layout.walls[wall];
  const run = layout.run;
  if (run?.round && run.radius) {
    const a = BASE[wall] + across / run.radius;
    const r = run.radius + frame.thickness + out;
    const normal = new Vector3(Math.cos(a), Math.sin(a), 0);
    return { point: new Vector3(r * normal.x, r * normal.y, up), normal };
  }
  const normal = new Vector3(...frame.normal);
  const flat = new Vector3(...frame.origin)
    .add(new Vector3(...frame.right).multiplyScalar(across))
    .add(new Vector3(0, 0, up))
    .add(normal.clone().multiplyScalar(out));
  const m = wallMatrix(layout, wall);
  return {
    point: flat.applyMatrix4(m),
    normal: normal.transformDirection(m),
  };
}

/** Where a ray (model mm) meets a round chamber's outside, entering it: which wall's quarter,
 * how far across it along the curve, and how far up, with how far along the ray. */
export function roundHit(
  layout: Layout,
  ray: Ray,
): { wall: WallFace; across: number; up: number; t: number } | null {
  const radius = layout.run?.radius ?? 0;
  const r = radius + layout.walls.front.thickness;
  const { origin: o, direction: d } = ray;
  const a = d.x * d.x + d.y * d.y;
  if (a < 1e-12) return null;
  const b = 2 * (o.x * d.x + o.y * d.y);
  const c = o.x * o.x + o.y * o.y - r * r;
  const disc = b * b - 4 * a * c;
  if (disc < 0) return null;
  const t = (-b - Math.sqrt(disc)) / (2 * a);
  if (t <= 0) return null;
  const hit = ray.at(t, new Vector3());
  const angle = Math.atan2(hit.y, hit.x);
  let best: WallFace = "front";
  let off = Infinity;
  for (const wall of Object.keys(BASE) as WallFace[]) {
    const delta = Math.atan2(Math.sin(angle - BASE[wall]), Math.cos(angle - BASE[wall]));
    if (Math.abs(delta) < Math.abs(off)) {
      best = wall;
      off = delta;
    }
  }
  return { wall: best, across: off * radius, up: hit.z, t };
}
