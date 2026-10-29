// @vitest-environment node
// The page's formula evaluator against the cases the engine's evaluator passes.
import { readFileSync } from "node:fs";

import type { Check } from "@kilndesigner/api-client";
import { describe, expect, it } from "vitest";

import { ExpressionError, evaluate, number, parse, recompute, solve } from "./sheet";

type Corpus = {
  expressions: { expr: string; env?: Record<string, number>; value: number | string }[];
  errors: { expr: string; env?: Record<string, number> }[];
  numbers: { x: number | string; text: string }[];
  checks: Check[];
};

const corpus = JSON.parse(
  readFileSync(new URL("../../core/tests/expressions.json", import.meta.url), "utf-8"),
) as Corpus;

describe("the shared formula cases", () => {
  it.each(corpus.expressions)("$expr", ({ expr, env, value }) => {
    const got = evaluate(parse(expr), env ?? {});
    const want = Number(value);
    if (Number.isNaN(want)) expect(got).toBeNaN();
    else if (!Number.isFinite(want)) expect(got).toBe(want);
    else expect(got).toBeCloseTo(want, 12);
  });

  it.each(corpus.errors)("$expr is refused", ({ expr, env }) => {
    expect(() => evaluate(parse(expr), env ?? {})).toThrow(ExpressionError);
  });

  it.each(corpus.numbers)("$x prints as $text", ({ x, text }) => {
    expect(number(Number(x))).toBe(text);
  });
});

describe("the shared checks", () => {
  it.each(corpus.checks.map((c, i) => [i, c] as const))("check %i", (_, check) => {
    const got = recompute(check, {});
    expect(got.status).toBe(check.status);
    expect(got.solve).toBe(check.solve ?? null);
    expect(got.requirements.map((r) => [r.holds, r.margin])).toEqual(
      check.requirements.map((r) => [r.holds, r.margin]),
    );
  });

  it("follows an edited input", () => {
    const rod = corpus.checks[0] as Check;
    const d = rod.cells.find((c) => c.symbol === "d")?.value as number;
    const thin = recompute(rod, { d: d / 3 });
    expect(thin.status).toBe("error");
    expect(thin.solve).toBe("Passes when d ≥ 0.1542 in");
    expect(solve({ ...rod, lever: null }, {})).toBeNull();
  });
});
