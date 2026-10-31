// A slow firing (`kilndesigner slow`): the kiln fired over a time the user chooses, what it
// takes against the quickest schedule, and the sources' slow firings beside it.
import type { SlowFiring } from "@kilndesigner/api-client";
import { useState } from "react";

import { useSlowFiring } from "../api";

const share = (x: number | null | undefined) => (x == null ? "" : ` (${(x * 100).toFixed(0)}%)`);

function Worked({ slow }: { slow: SlowFiring }) {
  const f = slow.firing;
  const q = slow.quickest;
  const rows: [string, string][] = [
    [
      "Pace",
      `${slow.rate_c_per_h.toFixed(1)} °C/h to ${slow.top_c.toFixed(0)} °C` +
        (slow.soak_h ? `, then ${slow.soak_h} h at the top` : ""),
    ],
  ];
  if (f && q) {
    rows.push(
      ["Firing time", f.duration + (f.completed ? "" : " (doesn't reach the top)")],
      ["Heat put in", `${f.energy_kwh.toFixed(0)} kWh`],
      ["Into the walls", `${f.walls_kwh.toFixed(0)} kWh${share(slow.walls_share)}`],
      ["Into the ware", `${f.ware_kwh.toFixed(0)} kWh${share(slow.ware_share)}`],
      ["Lost from the shell", `${f.shell_kwh.toFixed(0)} kWh${share(slow.shell_share)}`],
      ["Quickest firing", `${q.duration}, ${q.energy_kwh.toFixed(0)} kWh (shell lost ${q.shell_kwh.toFixed(0)})`],
    );
    if (f.cost && q.cost) rows.push(["Cost", `${f.cost} (quickest ${q.cost})`]);
  }
  return (
    <div className="firing">
      <dl className="firing-summary">
        {rows.map(([k, v]) => (
          <div key={k}>
            <dt>{k}</dt>
            <dd>{v}</dd>
          </div>
        ))}
      </dl>
      <ul className="findings">
        {slow.findings.map((x) => (
          <li key={x.message}>{x.message}</li>
        ))}
      </ul>
      <table className="profiles">
        <caption>The sources' slow firings</caption>
        <thead>
          <tr>
            <th>Kiln</th>
            <th>Fuel</th>
            <th>Time</th>
            <th>Used</th>
            <th>Reference</th>
          </tr>
        </thead>
        <tbody>
          {slow.sources.map((x) => (
            <tr key={x.kiln + x.time}>
              <td>{x.kiln}</td>
              <td>{x.fuel}</td>
              <td>{x.time}</td>
              <td>{x.used ?? ""}</td>
              <td>{x.reference}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <details>
        <summary>Working</summary>
        <ul>
          {slow.working.map((s) => (
            <li key={s.name}>
              {s.name}: {s.value}
              {s.reference && <span className="muted"> ({s.reference})</span>}
            </li>
          ))}
        </ul>
      </details>
    </div>
  );
}

export function SlowFiringPanel({ simKey }: { simKey: string }) {
  const [time, setTime] = useState("48 h");
  const [soak, setSoak] = useState("0 h");
  const run = useSlowFiring();
  return (
    <section aria-label="Slow firing" className="slow-firing">
      <h3>A slow firing</h3>
      <p className="muted">
        Fire the kiln over a time you choose, a constant rise to the top and then a soak, and see
        what it takes against the quickest schedule and the sources' slow firings.
      </p>
      <form
        onSubmit={(e) => {
          e.preventDefault();
          run.mutate({ key: simKey, time, soak });
        }}
      >
        <label>
          Firing time <input value={time} onChange={(e) => setTime(e.target.value)} />
        </label>
        <label>
          Soak at the top, within it <input value={soak} onChange={(e) => setSoak(e.target.value)} />
        </label>
        <button type="submit" disabled={run.isPending}>
          Work out the slow firing
        </button>
      </form>
      {run.isPending && (
        <p className="muted" aria-live="polite">
          Firing the kiln slowly, and on the quickest schedule to compare…
        </p>
      )}
      {run.isError && <p className="error">The slow firing can't be worked out: {run.error.message}</p>}
      {run.data && <Worked slow={run.data} />}
    </section>
  );
}
