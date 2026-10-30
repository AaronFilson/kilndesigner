// Why a warning or an error was raised: its check as a sheet (ADR 0013). Every row is an input,
// with its source, or a formula over the rows above it; the inputs can be changed here, and the
// sheet recomputes with the engine's own formulas (sheet.ts), down to whether it passes and what
// would change that. Changes stay in the page: they don't edit the design.
import type { Cell, Check } from "@kilndesigner/api-client";
import { Fragment, useMemo, useState } from "react";

import { number, recompute, SHOWN_OP, show } from "../sheet";

const NAME_WITH_SUB = /([\p{L}][\p{L}\p{N}]*)_([\p{L}\p{N}]+)/gu;

/** A symbol or a formula, with `σ_allow` written σ<sub>allow</sub>. */
export function Maths({ text }: { text: string }) {
  const parts: (string | [string, string])[] = [];
  let at = 0;
  for (const m of text.matchAll(NAME_WITH_SUB)) {
    parts.push(text.slice(at, m.index), [m[1] as string, m[2] as string]);
    at = (m.index ?? 0) + m[0].length;
  }
  parts.push(text.slice(at));
  return (
    <>
      {parts.map((p, i) =>
        typeof p === "string" ? (
          <Fragment key={i}>{p}</Fragment>
        ) : (
          <Fragment key={i}>
            {p[0]}
            <sub>{p[1]}</sub>
          </Fragment>
        ),
      )}
    </>
  );
}

const STATUS = { pass: "Passes", warning: "Warning", error: "Error" } as const;

function InputCell({
  cell,
  value,
  onChange,
}: {
  cell: Cell;
  value: number;
  onChange: (si: number | undefined) => void;
}) {
  const scale = cell.scale ?? 1;
  const offset = cell.offset ?? 0;
  const shown = value * scale + offset;
  const text = number(shown);
  // Typed back, it must read as a number: "1.23 × 10⁹" doesn't, so it's written out plainly
  const plain = text.includes("×")
    ? String(Number(shown.toPrecision(4)))
    : text.replace(/,/g, "").replace("−", "-");
  const [draft, setDraft] = useState<string | null>(null);
  return (
    <span className="sheet-input">
      <input
        type="text"
        inputMode="decimal"
        aria-label={`${cell.symbol}, ${cell.meaning}`}
        value={draft ?? plain}
        onChange={(e) => {
          setDraft(e.target.value);
          const v = Number(e.target.value);
          if (e.target.value.trim() !== "" && Number.isFinite(v)) onChange((v - offset) / scale);
        }}
        onBlur={() => setDraft(null)}
      />{" "}
      {cell.label}
    </span>
  );
}

export function CheckSheet({ check }: { check: Check }) {
  const [given, setGiven] = useState<Record<string, number>>({});
  const result = useMemo(() => recompute(check, given), [check, given]);
  const edited = Object.keys(given).length > 0;
  return (
    <div className="sheet" id={`check-${check.id}`}>
      <p className="sheet-head">
        <strong>
          {check.label ? `${check.label} · ` : ""}
          {check.title}
        </strong>{" "}
        <span className={`sheet-status ${result.status}`}>{STATUS[result.status]}</span>
        {edited && <span className="muted"> with your values</span>}
      </p>
      {check.rule && (
        <p className="sheet-rule">
          <strong>{check.rule_holds === false ? "Rule, not met:" : "Rule:"}</strong> {check.rule}
        </p>
      )}
      <div className="sheet-scroll">
        <table>
          <thead>
            <tr>
              <th scope="col">Symbol</th>
              <th scope="col">What it is</th>
              <th scope="col">Formula</th>
              <th scope="col">Value</th>
              <th scope="col">From</th>
            </tr>
          </thead>
          <tbody>
            {check.cells.map((c, i) => (
              <tr key={`${c.symbol}-${i}`} className={c.expr ? "formula" : "given"}>
                <th scope="row">
                  <Maths text={c.symbol} />
                </th>
                <td>{c.meaning}</td>
                <td>{c.formula && <Maths text={c.formula} />}</td>
                <td className="value">
                  {c.value == null ? (
                    c.text
                  ) : c.expr ? (
                    show(c, result.env[c.symbol] as number)
                  ) : (
                    <InputCell
                      cell={c}
                      value={result.env[c.symbol] as number}
                      onChange={(si) =>
                        setGiven((g) => (si === undefined ? g : { ...g, [c.symbol]: si }))
                      }
                    />
                  )}
                </td>
                <td className="source">{c.source}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {result.requirements.length > 0 && (
        <ul className="sheet-requirements">
          {result.requirements.map((r) => (
            <li key={`${r.left}${r.op}${r.right}`} className={r.holds ? "holds" : r.level}>
              <Maths text={`${r.left} ${SHOWN_OP[r.op]} ${r.right}`} />:{" "}
              {r.holds ? "holds" : `fails (${r.level})`}. <Maths text={r.margin} />
            </li>
          ))}
        </ul>
      )}
      {result.solve && (
        <p className="sheet-solve">
          <Maths text={result.solve} />
        </p>
      )}
      <p className="muted sheet-help">
        Change a yellow value to see what follows from it. This doesn't change the design.
        {edited && (
          <>
            {" "}
            <button type="button" className="link" onClick={() => setGiven({})}>
              Back to the design's values
            </button>
          </>
        )}
      </p>
      {check.reference && <cite>{check.reference}</cite>}
    </div>
  );
}
