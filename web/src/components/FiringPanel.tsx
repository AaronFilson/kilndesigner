// A simulated firing: start it, then its headline figures, the charts (temperature, power, energy
// and cost through the firing), a hybrid's switch-over chart, and the walls' heatmap with a
// scrubber through time.
import type { FiringPoint, FiringResult, SwitchOverChart, WallHeatmap as Heatmap } from "@kilndesigner/api-client";
import { useMemo, useState } from "react";

import { useFiring, useSimulation, useStartSimulation } from "../api";
import { css, hours, rampColour, type Series } from "../firing";
import { LineChart } from "./LineChart";
import { WallHeatmap } from "./WallHeatmap";

const COLOURS = { a: "#e8833a", b: "#3a8be8", c: "#8c8c8c", d: "#2a9d5c" };

export function firingCharts(points: FiringPoint[]): { title: string; yLabel: string; series: Series[] }[] {
  const line = (label: string, colour: string, y: (p: FiringPoint) => number, dashed = false): Series => ({
    label,
    colour,
    dashed,
    points: points.map((p) => [p.time_h, y(p)]),
  });
  const priced = points.some((p) => p.cost_usd != null);
  return [
    {
      title: "Temperature",
      yLabel: "°C",
      series: [
        line("Chamber", COLOURS.a, (p) => p.chamber_c),
        line("Schedule", COLOURS.c, (p) => p.setpoint_c, true),
        line("Hottest shell", COLOURS.b, (p) => p.hottest_shell_c),
      ],
    },
    {
      title: "Power",
      yLabel: "kW",
      series: [
        line("Put into the kiln", COLOURS.a, (p) => p.heat_kw),
        line("Available", COLOURS.c, (p) => p.available_kw, true),
        line("Lost from the shell", COLOURS.b, (p) => p.shell_kw),
        ...(points.some((p) => p.fuel_kw > 0) ? [line("Fuel burned", COLOURS.d, (p) => p.fuel_kw)] : []),
      ],
    },
    {
      title: priced ? "Energy and cost" : "Energy",
      yLabel: priced ? "kWh, $" : "kWh",
      series: [
        line("Put into the kiln, kWh", COLOURS.a, (p) => p.energy_kwh),
        ...(points.some((p) => p.electricity_kwh > 0)
          ? [line("Electricity, kWh", COLOURS.b, (p) => p.electricity_kwh)]
          : []),
        ...(points.some((p) => p.fuel_kwh > 0) ? [line("Fuel, kWh", COLOURS.d, (p) => p.fuel_kwh)] : []),
        ...(priced ? [line("Cost, $", COLOURS.c, (p) => p.cost_usd ?? 0, true)] : []),
      ],
    },
  ];
}

function Summary({ result }: { result: FiringResult }) {
  const rows: [string, string][] = [
    ["Heat", result.heat],
    ["Firing time", result.duration + (result.completed ? "" : " (stopped before the end)")],
    ["Reached", `${result.reached_c.toFixed(0)} °C of ${result.target_c.toFixed(0)} °C`],
    ["Schedule kept", result.held ? "yes" : "no: the heat falls behind"],
    ["Heat put in", `${result.energy_kwh.toFixed(1)} kWh`],
    ...(result.electricity_kwh > 0 ? [["Electricity", `${result.electricity_kwh.toFixed(1)} kWh`] as [string, string]] : []),
    ...(result.fuel_kwh > 0
      ? [
          [
            "Fuel burned",
            `${result.fuel_kwh.toFixed(1)} kWh` +
              (result.propane_gallons != null ? ` (${result.propane_gallons.toFixed(1)} gal propane)` : ""),
          ] as [string, string],
        ]
      : []),
    ...(result.cost ? [["Cost", result.cost] as [string, string]] : []),
  ];
  return (
    <dl className="firing-summary">
      {rows.map(([k, v]) => (
        <div key={k}>
          <dt>{k}</dt>
          <dd>{v}</dd>
        </div>
      ))}
    </dl>
  );
}

function SwitchOver({ chart }: { chart: SwitchOverChart }) {
  const at = (y: (p: SwitchOverChart["points"][number]) => number): [number, number][] =>
    chart.points.filter((p) => p.completed).map((p) => [p.switch_over_c, y(p)]);
  return (
    <>
      <LineChart
        title="Cost against the hand-over to the burners"
        xLabel="Hand-over, °C"
        yLabel="$"
        series={[{ label: "Cost of the firing", colour: COLOURS.a, points: at((p) => p.cost_usd) }]}
        marker={chart.cheapest_c}
      />
      <LineChart
        title="Time against the hand-over to the burners"
        xLabel="Hand-over, °C"
        yLabel="hours"
        series={[{ label: "Firing time", colour: COLOURS.b, points: at((p) => p.duration_h) }]}
        marker={chart.fastest_c}
      />
    </>
  );
}

const FACES = ["left", "right", "back", "front", "floor", "roof"];

export function HeatmapView({ map, result }: { map: Heatmap; result: FiringResult }) {
  const [index, setIndex] = useState(map.times_h.length - 1);
  // The front and the roof are left off at first, to see into the kiln
  const [show, setShow] = useState(() => map.walls.filter((w) => w !== "front" && w !== "roof"));
  // Kept between renders, so scrubbing only moves the shader's time
  const inside = useMemo(() => result.faces.map((f) => f.inside_area_m2), [result.faces]);
  const time = map.times_h[index] ?? 0;
  const ticks = [0, 0.25, 0.5, 0.75, 1];
  return (
    <section aria-label="Wall heatmap" className="heatmap">
      <WallHeatmap map={map} inside={inside} time={index} show={show} />
      <label className="scrubber">
        Time: <output>{hours(time)}</output>
        <input
          type="range"
          min={0}
          max={map.times_h.length - 1}
          value={index}
          onChange={(e) => setIndex(Number(e.target.value))}
          aria-label="Time through the firing"
        />
      </label>
      <fieldset className="faces">
        <legend>Faces</legend>
        {map.walls.filter((w) => FACES.includes(w)).map((w) => (
          <label key={w}>
            <input
              type="checkbox"
              checked={show.includes(w)}
              onChange={() => setShow((s) => (s.includes(w) ? s.filter((x) => x !== w) : [...s, w]))}
            />
            {w}
          </label>
        ))}
      </fieldset>
      <p className="scale" aria-label="Temperature scale">
        {ticks.map((f) => (
          <span key={f} style={{ background: css(rampColour(f)), color: f > 0.5 ? "#111" : "#fff" }}>
            {(map.min_c + f * (map.max_c - map.min_c)).toFixed(0)} °C
          </span>
        ))}
      </p>
      <table className="profiles">
        <caption>Hot face and shell at {hours(time)}</caption>
        <thead>
          <tr>
            <th>Face</th>
            <th>Hot face</th>
            <th>Shell side</th>
          </tr>
        </thead>
        <tbody>
          {map.walls.map((w, i) => {
            const temps = map.temperatures[index]![i]!;
            return (
              <tr key={w}>
                <td>{w}</td>
                <td>{temps[0]!.toFixed(0)} °C</td>
                <td>{temps[temps.length - 1]!.toFixed(0)} °C</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </section>
  );
}

function Fired({ simKey }: { simKey: string }) {
  const { result, series, heatmap, switchover } = useFiring(simKey);
  const error = result.error ?? series.error ?? heatmap.error ?? switchover.error;
  if (error) return <p className="error">The firing could not be loaded: {error.message}</p>;
  if (!result.data || !series.data) return <p className="muted">Loading the firing…</p>;
  const r = result.data;
  return (
    <div className="firing">
      <Summary result={r} />
      {series.data && firingCharts(series.data).map((c) => (
        <LineChart key={c.title} title={c.title} xLabel="hours" yLabel={c.yLabel} series={c.series} />
      ))}
      {switchover.data && <SwitchOver chart={switchover.data} />}
      {heatmap.data && <HeatmapView map={heatmap.data} result={r} />}
      <ul className="findings">
        {r.findings.map((f) => (
          <li key={f.message}>{f.message}</li>
        ))}
      </ul>
      <details>
        <summary>Working</summary>
        <ul>
          {r.working.map((s) => (
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

export function FiringPanel({ simKey }: { simKey: string }) {
  const sim = useSimulation(simKey);
  const start = useStartSimulation();
  if (sim.isPending) return <p className="muted">Checking the firing…</p>;
  if (sim.isError) return <p className="error">{sim.error.message}</p>;
  const s = sim.data;
  if (s === null || s.status === "failed") {
    return (
      <div className="build-start">
        {s?.error && <p className="error">The firing can't be simulated: {s.error}</p>}
        <button type="button" onClick={() => start.mutate(simKey)} disabled={start.isPending}>
          {s ? "Simulate again" : "Simulate the firing"}
        </button>
      </div>
    );
  }
  if (s.status !== "done") {
    return (
      <p className="muted" aria-live="polite">
        {s.status === "queued" ? "Waiting for the worker…" : "Firing the kiln, step by step…"}
      </p>
    );
  }
  return <Fired simKey={simKey} />;
}
