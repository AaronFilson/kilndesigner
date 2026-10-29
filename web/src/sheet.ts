// The checks' formula language (ADR 0013): the twin of kilndesigner.sheet in the engine. The two
// are held to the same answers by core/tests/expressions.json, so a sheet edited in the page gives
// the numbers the engine would.
import type { Cell, Check, Requirement } from "@kilndesigner/api-client";

export class ExpressionError extends Error {}

const ARITY: Record<string, number> = {
  sqrt: 1, exp: 1, ln: 1, log10: 1, abs: 1, sin: 1, cos: 1, tan: 1, asin: 1, acos: 1, atan: 1,
  atan2: 2, min: -2, max: -2,
}; // prettier-ignore
const CONSTANTS: Record<string, number> = { pi: Math.PI, π: Math.PI };

type Node =
  | { k: "num"; v: number }
  | { k: "name"; id: string }
  | { k: "neg"; arg: Node }
  | { k: "bin"; op: string; l: Node; r: Node }
  | { k: "call"; fn: string; args: Node[] };

type Token = { kind: "num" | "name" | "op"; text: string };

const TOKEN =
  /\s*(?:(?<num>(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)|(?<name>[\p{L}_][\p{L}\p{N}_]*)|(?<op>[-+*/^(),]))/uy;

function tokens(text: string): Token[] {
  const out: Token[] = [];
  const end = text.trimEnd().length;
  TOKEN.lastIndex = 0;
  while (TOKEN.lastIndex < end) {
    const at = TOKEN.lastIndex;
    const m = TOKEN.exec(text);
    const g = m?.groups;
    if (!m || !g) throw new ExpressionError(`can't read ${text.slice(at).trim()} in ${text}`);
    const kind = g.num !== undefined ? "num" : g.name !== undefined ? "name" : "op";
    out.push({ kind, text: (g.num ?? g.name ?? g.op) as string });
  }
  return out;
}

class Parser {
  private i = 0;
  private readonly toks: Token[];
  constructor(private readonly text: string) {
    this.toks = tokens(text);
  }
  private peek(): string | undefined {
    return this.toks[this.i]?.text;
  }
  private take(): Token {
    const t = this.toks[this.i++];
    if (!t) throw new ExpressionError(`${this.text} ends too soon`);
    return t;
  }
  private expect(tok: string) {
    const t = this.take();
    if (t.kind !== "op" || t.text !== tok)
      throw new ExpressionError(`expected ${tok} but found ${t.text} in ${this.text}`);
  }
  parse(): Node {
    const node = this.sum();
    if (this.i < this.toks.length)
      throw new ExpressionError(`unexpected ${this.toks[this.i]?.text} in ${this.text}`);
    return node;
  }
  private sum(): Node {
    let node = this.term();
    for (let op = this.peek(); op === "+" || op === "-"; op = this.peek()) {
      this.take();
      node = { k: "bin", op, l: node, r: this.term() };
    }
    return node;
  }
  private term(): Node {
    let node = this.unary();
    for (let op = this.peek(); op === "*" || op === "/"; op = this.peek()) {
      this.take();
      node = { k: "bin", op, l: node, r: this.unary() };
    }
    return node;
  }
  private unary(): Node {
    if (this.peek() === "-") {
      this.take();
      return { k: "neg", arg: this.unary() };
    }
    return this.power();
  }
  private power(): Node {
    const base = this.atom();
    if (this.peek() === "^") {
      this.take();
      return { k: "bin", op: "^", l: base, r: this.unary() };
    }
    return base;
  }
  private atom(): Node {
    const t = this.take();
    if (t.kind === "num") return { k: "num", v: Number(t.text) };
    if (t.kind === "name") {
      const n = ARITY[t.text];
      if (this.peek() !== "(") {
        if (n !== undefined) throw new ExpressionError(`${t.text} needs brackets`);
        return { k: "name", id: t.text };
      }
      if (n === undefined) throw new ExpressionError(`${t.text} is not a function the sheets know`);
      this.take();
      const args = [this.sum()];
      while (this.peek() === ",") {
        this.take();
        args.push(this.sum());
      }
      this.expect(")");
      if ((n > 0 && args.length !== n) || (n < 0 && args.length < -n))
        throw new ExpressionError(`${t.text} takes ${n > 0 ? n : "two or more"} arguments`);
      return { k: "call", fn: t.text, args };
    }
    if (t.text === "(") {
      const node = this.sum();
      this.expect(")");
      return node;
    }
    throw new ExpressionError(`unexpected ${t.text} in ${this.text}`);
  }
}

const parsed = new Map<string, Node>();

export function parse(text: string): Node {
  let node = parsed.get(text);
  if (!node) {
    node = new Parser(text).parse();
    parsed.set(text, node);
  }
  return node;
}

const FUNCS: Record<string, (...xs: number[]) => number> = {
  sqrt: Math.sqrt, exp: Math.exp, ln: Math.log, log10: Math.log10, abs: Math.abs, sin: Math.sin,
  cos: Math.cos, tan: Math.tan, asin: Math.asin, acos: Math.acos, atan: Math.atan,
  atan2: Math.atan2, min: Math.min, max: Math.max,
}; // prettier-ignore

/** A formula's value, in SI, from the cells' SI values. */
export function evaluate(node: Node, env: Record<string, number>): number {
  switch (node.k) {
    case "num":
      return node.v;
    case "name": {
      const c = CONSTANTS[node.id];
      if (c !== undefined) return c;
      const v = env[node.id];
      if (v === undefined) throw new ExpressionError(`${node.id} is not a cell above this one`);
      return v;
    }
    case "neg":
      return -evaluate(node.arg, env);
    case "bin": {
      const x = evaluate(node.l, env);
      const y = evaluate(node.r, env);
      if (node.op === "+") return x + y;
      if (node.op === "-") return x - y;
      if (node.op === "*") return x * y;
      return node.op === "/" ? x / y : Math.pow(x, y);
    }
    case "call":
      return (FUNCS[node.fn] as (...xs: number[]) => number)(
        ...node.args.map((a) => evaluate(a, env)),
      );
  }
}

// ---- Numbers as the sheets print them: the same text as kilndesigner.sheet.number ----

const SUPER: Record<string, string> = {
  "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸",
  "9": "⁹", "-": "⁻",
}; // prettier-ignore

function round(x: number, places: number): number {
  const f = 10 ** places;
  return (Math.sign(x) * Math.floor(Math.abs(x) * f + 0.5)) / f;
}

function scaled(x: number, e: number): number {
  return e >= 0 ? x / 10 ** e : x * 10 ** -e;
}

function trim(text: string): string {
  return text.includes(".") ? text.replace(/0+$/, "").replace(/\.$/, "") : text;
}

export function number(x: number): string {
  if (Number.isNaN(x)) return "—";
  if (!Number.isFinite(x)) return x > 0 ? "∞" : "−∞";
  const a = Math.abs(x);
  if (a === 0) return "0";
  let e = Math.floor(Math.log10(a));
  if (Math.abs(scaled(a, e)) >= 10) e += 1;
  else if (Math.abs(scaled(a, e)) < 1) e -= 1;
  if (a >= 1e6 || a < 1e-3) {
    let m = round(scaled(x, e), 3);
    if (Math.abs(m) >= 10) {
      m /= 10;
      e += 1;
    }
    const power = [...String(e)].map((ch) => SUPER[ch]).join("");
    return `${trim(m.toFixed(3)).replace("-", "−")} × 10${power}`;
  }
  const places = Math.max(0, 3 - e);
  const [whole, frac] = round(x, places).toFixed(places).split(".") as [string, string?];
  const grouped = whole.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  return trim(frac === undefined ? grouped : `${grouped}.${frac}`).replace("-", "−");
}

// ---- The sheet ----

const RANK = { pass: 0, warning: 1, error: 2 } as const;
/** ≤ and ≥ allow a part in a billion, as kilndesigner.sheet does. */
function slack(a: number, b: number): number {
  return Number.isFinite(a) && Number.isFinite(b) ? 1e-9 * Math.max(Math.abs(a), Math.abs(b)) : 0;
}

const OPS: Record<Requirement["op"], (a: number, b: number) => boolean> = {
  "<=": (a, b) => a <= b + slack(a, b),
  "<": (a, b) => a < b,
  ">=": (a, b) => a >= b - slack(a, b),
  ">": (a, b) => a > b,
};
export const SHOWN_OP: Record<Requirement["op"], string> = { "<=": "≤", "<": "<", ">=": "≥", ">": ">" };

/** A value as the sheet shows it, in the cell's own unit. */
export function show(c: Cell, si: number): string {
  const text = number(si * (c.scale ?? 1) + (c.offset ?? 0));
  return c.label === "$" ? `$${text}` : `${text} ${c.label ?? ""}`.trimEnd();
}

/** Every numeric cell's SI value, with `given` replacing inputs. */
export function values(cells: Cell[], given: Record<string, number> = {}): Record<string, number> {
  const env: Record<string, number> = {};
  for (const c of cells) {
    if (c.expr) env[c.symbol] = evaluate(parse(c.expr), env);
    else if (c.value != null) env[c.symbol] = given[c.symbol] ?? c.value;
  }
  return env;
}

export function margin(left: Cell, right: Cell, a: number, b: number): string {
  const lt = `${left.symbol} = ${show(left, a)}`;
  const rt = `${right.symbol} = ${show(right, b)}`;
  if (left.offset || right.offset) {
    const d = (a - b) * (left.scale ?? 1);
    return `${lt}, ${number(Math.abs(d))} ${left.label ?? ""} ${d > 0 ? "over" : "under"} ${rt}`;
  }
  if (b !== 0 && Number.isFinite(a) && Number.isFinite(b) && a / b > 0)
    return `${lt}, ${number((100 * a) / b)} % of ${rt}`;
  return `${lt} against ${rt}`;
}

export function status(check: Check, env: Record<string, number>): Check["status"] {
  let worst: Check["status"] = check.rule_holds === false ? check.rule_level ?? "error" : "pass";
  for (const r of check.requirements) {
    if (!OPS[r.op](env[r.left] as number, env[r.right] as number) && RANK[r.level] > RANK[worst])
      worst = r.level;
  }
  return worst;
}

const STEPS = 64;

/** Where the lever nearest changes the result: as kilndesigner.sheet.solve finds it. */
export function solve(check: Check, given: Record<string, number> = {}): string | null {
  const lv = check.lever;
  if (!lv) return null;
  const cell = check.cells.find((c) => c.symbol === lv.symbol) as Cell;
  const passes = (x: number) =>
    status(check, values(check.cells, { ...given, [lv.symbol]: x })) === "pass";
  const x0 = given[lv.symbol] ?? (cell.value as number);
  const p0 = passes(x0);
  const found: number[] = [];
  // Walk out towards each end in STEPS steps, then bisect at the first that differs
  for (const end of [lv.lo, lv.hi]) {
    let prev = x0;
    for (let k = 1; end !== x0 && k <= STEPS; k++) {
      const x = x0 + ((end - x0) * k) / STEPS;
      if (passes(x) !== p0) {
        let [a, b] = [prev, x];
        for (let i = 0; i < 60; i++) {
          const m = (a + b) / 2;
          if (passes(m) === p0) a = m;
          else b = m;
        }
        found.push(p0 ? a : b);
        break;
      }
      prev = x;
    }
  }
  const sym = lv.symbol;
  if (found.length === 0) {
    const span = `${sym} from ${show(cell, lv.lo)} to ${show(cell, lv.hi)}`;
    return p0 ? `Passes for any ${span}` : `Doesn't pass for any ${span}`;
  }
  let x = found.reduce((best, v) => (Math.abs(v - x0) < Math.abs(best - x0) ? v : best));
  const up = x > x0 !== p0;
  const scale = cell.scale ?? 1;
  const offset = cell.offset ?? 0;
  if (Math.abs(x * scale + offset) < 1e-6 * Math.abs(lv.hi - lv.lo) * scale) x = -offset / scale;
  if (lv.step) {
    // 5 cylinders, not 4.331: the next whole step on the side that passes
    const n = x / lv.step;
    const whole = lv.step * (up ? Math.ceil(n - 1e-9) : Math.floor(n + 1e-9));
    if (!passes(whole))
      return `No whole ${sym} passes (it would at ${sym} ${up ? "≥" : "≤"} ${show(cell, x)})`;
    x = whole;
  }
  return `${p0 ? "Passes while" : "Passes when"} ${sym} ${up ? "≥" : "≤"} ${show(cell, x)}`;
}

/** The sheet with some inputs changed: every value, each requirement's state, and the result. */
export function recompute(check: Check, given: Record<string, number>) {
  const env = values(check.cells, given);
  const by = Object.fromEntries(check.cells.map((c) => [c.symbol, c]));
  const requirements = check.requirements.map((r) => ({
    ...r,
    holds: OPS[r.op](env[r.left] as number, env[r.right] as number),
    margin: margin(by[r.left] as Cell, by[r.right] as Cell, env[r.left] as number, env[r.right] as number),
  }));
  return { env, requirements, status: status(check, env), solve: solve(check, given) };
}
