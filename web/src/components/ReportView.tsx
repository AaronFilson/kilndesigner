// The report's headline numbers and its findings. The working stays a click away for each section.
import type { Finding, Report, Step } from "@kilndesigner/api-client";
import { useState } from "react";

import { CheckSheet } from "./CheckSheet";

function Rows({ rows }: { rows: [string, string | null | undefined][] }) {
  return (
    <dl className="rows">
      {rows
        .filter((row): row is [string, string] => row[1] != null)
        .map(([label, value]) => (
          <div key={label}>
            <dt>{label}</dt>
            <dd>{value}</dd>
          </div>
        ))}
    </dl>
  );
}

function Working({ steps }: { steps: Step[] }) {
  if (steps.length === 0) return null;
  return (
    <details className="working">
      <summary>
        Working ({steps.length} {steps.length === 1 ? "step" : "steps"})
      </summary>
      <ol>
        {steps.map((s, i) => (
          <li key={i}>
            <strong>{s.name}</strong> = {s.value}
            {s.formula && <code>{s.formula}</code>}
            {s.reference && <cite>{s.reference}</cite>}
          </li>
        ))}
      </ol>
    </details>
  );
}

function Problem({ finding: f }: { finding: Finding }) {
  const check = f.check;
  const anchor = check ? `#check-${check.id}` : undefined;
  // A link to a sheet opens it, so a shared link lands on the working
  const [open, setOpen] = useState(() => anchor !== undefined && window.location.hash === anchor);
  return (
    <li className={f.level}>
      <span className="level">{check?.label ?? f.level}</span> {f.message}
      {check && (
        <>
          {" "}
          <a
            href={anchor}
            className="why"
            aria-expanded={open}
            onClick={(e) => {
              e.preventDefault();
              setOpen(!open);
              if (!open) window.history.replaceState(null, "", anchor);
            }}
          >
            {open ? "Hide the working" : "Why: the formulas and numbers"}
          </a>
        </>
      )}
      {f.reference && <cite>{f.reference}</cite>}
      {check && open && <CheckSheet check={check} />}
    </li>
  );
}

/** Errors and warnings: things the design should change, each with the sheet that raised it.
 * Notes are shown by `Notes`. */
export function Findings({ findings }: { findings: Finding[] }) {
  const problems = findings.filter((f) => f.level !== "info");
  if (problems.length === 0) return null;
  return (
    <ul className="findings">
      {problems.map((f, i) => (
        <Problem key={f.check?.id ?? i} finding={f} />
      ))}
    </ul>
  );
}

/** What the results rest on and how far to trust them: nothing in the design to change. */
export function Notes({ findings }: { findings: Finding[] }) {
  const notes = findings.filter((f) => f.level === "info");
  if (notes.length === 0) return null;
  return (
    <section className="notes">
      <h3>Notes</h3>
      <ul className="findings">
        {notes.map((f, i) => (
          <li key={i} className="info">
            {f.message}
            {f.reference && <cite>{f.reference}</cite>}
          </li>
        ))}
      </ul>
    </section>
  );
}

export function ReportView({ report }: { report: Report }) {
  const { heat_loss: loss, electric, gas, hybrid, bom, frame } = report;
  const el = electric?.elements;
  return (
    <div className="report">
      <Findings findings={report.findings} />
      <section>
        <h3>Heat loss</h3>
        <Rows
          rows={[
            ["Chamber volume", report.chamber_volume],
            ["Top temperature", loss.top_temperature],
            ["Heat loss at top", loss.total],
          ]}
        />
        <Working steps={loss.working} />
      </section>
      {electric && (
        <section>
          <h3>Elements</h3>
          <Rows
            rows={[
              ["Installed power", `${electric.installed_power} (${electric.power_per_volume})`],
              ["Line current", electric.line_current],
              ["Elements", el && `${el.count} × ${el.gauge} ${electric.alloy}, ${el.wiring}`],
              ["Length each", el?.length_each],
              ["Surface load", el?.surface_load],
              ["Coil pitch", el?.pitch],
            ]}
          />
          <Working steps={electric.working} />
        </section>
      )}
      {gas && (
        <section>
          <h3>Burners and propane</h3>
          <Rows
            rows={[
              ["Burner input", gas.design_input],
              ["Propane at full fire", gas.propane_at_full_fire],
              ["Tank", gas.tank_suggestion],
              ["Chimney height", gas.chimney_height],
              ["Flue area", gas.flue_area],
            ]}
          />
          <Working steps={gas.working} />
        </section>
      )}
      {hybrid && (
        <section>
          <h3>Electric to gas</h3>
          <Rows
            rows={[
              ["Switch to burners at", hybrid.switch_over],
              ["Why", hybrid.switch_over_reason],
            ]}
          />
          <Working steps={hybrid.working} />
        </section>
      )}
      <section>
        <h3>{frame.kind === "welded case" ? "Case" : "Steel frame"}</h3>
        <Rows
          rows={[
            ["Angle", frame.angle],
            ["Tie rods", frame.rod],
            ["Arch thrust", frame.thrust],
          ]}
        />
        <Working steps={frame.working} />
      </section>
      {bom && (
        <section>
          <h3>Materials</h3>
          <Rows rows={[["Priced items", `$${Math.round(bom.total).toLocaleString("en-US")}`]]} />
        </section>
      )}
      <Notes findings={report.findings} />
    </div>
  );
}
