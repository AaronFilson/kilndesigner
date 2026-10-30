// Each castable the builder mixes: the batch to weigh, what it becomes, how much to mix, what
// the temperatures in the wall mean for it, and how to fire it the first time.
import type { Report } from "@kilndesigner/api-client";

import { Findings, Notes } from "./ReportView";

type CastableReport = Report["castables"][number];

function Mix({ c }: { c: CastableReport }) {
  const m = c.mix;
  return (
    <section className="castable-report" aria-label={m.name}>
      <h3>{m.name}</h3>
      <table className="plain" aria-label={`One batch of ${m.name}`}>
        <caption>One batch</caption>
        <thead>
          <tr>
            <th scope="col">Ingredient</th>
            <th scope="col" className="number">
              Weight
            </th>
            <th scope="col" className="number">
              Share
            </th>
          </tr>
        </thead>
        <tbody>
          {m.batch.map((b) => (
            <tr key={b.ingredient}>
              <th scope="row">{b.name}</th>
              <td className="number">{b.mass}</td>
              <td className="number">{b.share}</td>
            </tr>
          ))}
          <tr>
            <th scope="row">Water</th>
            <td className="number">{m.water}</td>
            <td className="number">{m.water_share}</td>
          </tr>
        </tbody>
      </table>
      <dl className="rows">
        {(
          [
            ["Foam", m.foam],
            ["One batch casts", m.cast_volume],
            ["Wet", m.wet_density],
            ["A level US quart weighs", m.quart_weighs],
            ["Dried", m.dried_density],
            ["Fired", m.fired_density],
            ["Porosity when fired", m.porosity],
            ["Conductivity (estimated)", m.conductivity.join("; ")],
            ["Service limit", m.service_limit ?? "not sourced: test it"],
            ["Placed in the lining", c.placed],
            ["Batches to mix", c.batches > 0 ? `${c.batches}, with 10 % to spare` : null],
          ] as [string, string | null | undefined][]
        )
          .filter((row): row is [string, string] => row[1] != null)
          .map(([label, value]) => (
            <div key={label}>
              <dt>{label}</dt>
              <dd>{value}</dd>
            </div>
          ))}
      </dl>
      <h4>Steps</h4>
      <ol className="steps">
        {c.steps.map((s) => (
          <li key={s}>{s}</li>
        ))}
      </ol>
      {c.schedule.length > 0 && (
        <table className="plain" aria-label={`First firing of ${m.name}`}>
          <caption>
            First firing{c.schedule_hours ? `, about ${Math.round(c.schedule_hours)} h` : ""}
          </caption>
          <thead>
            <tr>
              <th scope="col">To</th>
              <th scope="col">Rate</th>
              <th scope="col">Hold</th>
              <th scope="col">Why</th>
            </tr>
          </thead>
          <tbody>
            {c.schedule.map((s) => (
              <tr key={s.to}>
                <th scope="row">{s.to}</th>
                <td>{s.rate}</td>
                <td>{s.hold ?? "—"}</td>
                <td>{s.why}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {c.layers.length > 0 && (
        <>
          <h4>In the wall</h4>
          <ul className="layer-notes">
            {c.layers.map((l) => (
              <li key={`${l.face}-${l.thickness}`}>
                <strong>
                  {l.face}, {l.thickness}
                </strong>{" "}
                ({l.hot_side} to {l.cold_side}): {l.notes.join(" ")}
              </li>
            ))}
          </ul>
        </>
      )}
      {c.first_firing.length > 0 && (
        <>
          <h4>The first firing drives off</h4>
          <dl className="rows">
            {c.first_firing.map((s) => (
              <div key={s.name}>
                <dt>{s.name}</dt>
                <dd>
                  {s.value}
                  {Object.entries(s.inputs ?? {}).length > 0 && (
                    <span className="muted">
                      {" "}
                      ({Object.entries(s.inputs ?? {})
                        .map(([k, v]) => `${k}: ${v}`)
                        .join("; ")})
                    </span>
                  )}
                </dd>
              </div>
            ))}
          </dl>
        </>
      )}
      <Findings findings={c.findings} />
      <Notes findings={c.findings} />
      <details className="working">
        <summary>
          Working ({m.working.length} step{m.working.length === 1 ? "" : "s"})
        </summary>
        <ol>
          {m.working.map((s) => (
            <li key={s.name}>
              <strong>{s.name}</strong> = {s.value}
              {s.formula && <code>{s.formula}</code>}
              {s.reference && <cite>{s.reference}</cite>}
            </li>
          ))}
        </ol>
      </details>
    </section>
  );
}

export function Castables({ report }: { report: Report }) {
  if (report.castables.length === 0) {
    return <p className="muted">This design has no castables of its own.</p>;
  }
  return (
    <div className="report castables">
      {report.castables.map((c) => (
        <Mix key={c.mix.id} c={c} />
      ))}
    </div>
  );
}
