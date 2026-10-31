// A version's build: start it, follow it, then show the model, the drawings, the materials and
// the report, each on its own tab, with the files to download underneath.
import type { Build, Report } from "@kilndesigner/api-client";
import { useState } from "react";

import { fileUrl, hasReport, useBuild, useLayout, useReport, useStartBuild } from "../api";
import type { KilnDocument } from "../design";
import { Castables } from "./Castables";
import { Drawings } from "./Drawings";
import { FiringPanel } from "./FiringPanel";
import { KilnViewer } from "./KilnViewer";
import { Materials } from "./Materials";
import { ReportView } from "./ReportView";
import { SlowFiringPanel } from "./SlowFiringPanel";

const DOWNLOADS: [string, string][] = [
  ["plans.pdf", "Plans (PDF)"],
  ["sections.dxf", "Sections (DXF)"],
  ["kiln.step", "3D model (STEP)"],
  ["kiln.glb", "3D model (glTF)"],
  ["checks.xlsx", "Warnings' working (spreadsheet)"],
  ["report.json", "Report (JSON)"],
];

type Tab = "model" | "drawings" | "materials" | "castables" | "firing" | "report";

/** "Report", or "Report (1 error, 5 warnings)". */
export function reportTabLabel(report: Report | undefined): string {
  if (!report) return "Report";
  const count = (level: string) => report.findings.filter((f) => f.level === level).length;
  const parts = [
    [count("error"), "error"],
    [count("warning"), "warning"],
  ] as const;
  const shown = parts.filter(([n]) => n > 0).map(([n, what]) => `${n} ${what}${n === 1 ? "" : "s"}`);
  return shown.length ? `Report (${shown.join(", ")})` : "Report";
}

const needsReport = (tab: Tab) => tab !== "model" && tab !== "drawings" && tab !== "firing";

/** The design being edited, and a way to change it from the model (a port moved). */
interface Editing {
  draft?: KilnDocument | null;
  onEdit?: (apply: (document: KilnDocument) => KilnDocument) => void;
}

function Built({ build, draft, onEdit }: { build: Build } & Editing) {
  const report = useReport(build);
  const layout = useLayout(build);
  const [tab, setTab] = useState<Tab>("model");
  const tabs: [Tab, string][] = [
    ["model", "3D model"],
    ["drawings", "Drawings"],
    ["materials", "Materials"],
    ...(report.data?.castables.length ? [["castables", "Castables"] as [Tab, string]] : []),
    ["firing", "Firing"],
    ["report", reportTabLabel(report.data)],
  ];
  const downloads = DOWNLOADS.filter(([file]) => build.files.includes(file));
  return (
    <>
      <div role="tablist" aria-label="The build" className="tabs">
        {tabs.map(([id, label]) => (
          <button
            key={id}
            type="button"
            role="tab"
            aria-selected={tab === id}
            className={tab === id ? "tab active" : "tab"}
            onClick={() => setTab(id)}
          >
            {label}
          </button>
        ))}
      </div>
      <div role="tabpanel" aria-label={tabs.find(([id]) => id === tab)?.[1]}>
        {tab === "model" &&
          (build.files.includes("kiln.glb") ? (
            <KilnViewer
              url={fileUrl(build.key, "kiln.glb")}
              partsUrl={fileUrl(build.key, "parts.json")}
              layout={layout.data}
              draft={draft}
              onEdit={onEdit}
            />
          ) : (
            <p className="muted">This build has no 3D model.</p>
          ))}
        {tab === "drawings" && <Drawings build={build} />}
        {tab === "firing" && (
          <>
            <FiringPanel simKey={build.key} />
            <SlowFiringPanel simKey={build.key} />
          </>
        )}
        {/* A query that isn't run counts as pending, so a build without a report says so */}
        {needsReport(tab) && !hasReport(build) && <p className="muted">This build has no report.</p>}
        {needsReport(tab) && hasReport(build) && report.isPending && (
          <p className="muted">Loading the report…</p>
        )}
        {tab === "materials" && report.data && <Materials report={report.data} />}
        {tab === "castables" && report.data && <Castables report={report.data} />}
        {tab === "report" && report.data && <ReportView report={report.data} />}
        {report.error && <p className="error">The report could not be loaded: {report.error.message}</p>}
      </div>
      {build.notes.map((note) => (
        <p key={note} className="note">
          {note}
        </p>
      ))}
      {downloads.length > 0 && (
        <p className="downloads">
          <span className="muted">Download:</span>
          {downloads.map(([file, label]) => (
            <a key={file} href={fileUrl(build.key, file)} download>
              {label}
            </a>
          ))}
        </p>
      )}
    </>
  );
}

export function BuildPanel({ buildKey, draft, onEdit }: { buildKey: string } & Editing) {
  const build = useBuild(buildKey);
  const start = useStartBuild();

  if (build.isPending) return <p className="muted">Checking the build…</p>;
  if (build.isError) return <p className="error">{build.error.message}</p>;
  const b = build.data;
  if (b === null || b.status === "failed") {
    return (
      <div className="build-start">
        {b?.error && <p className="error">The build failed: {b.error}</p>}
        <button type="button" onClick={() => start.mutate(buildKey)} disabled={start.isPending}>
          {b ? "Build again" : "Build"}
        </button>
      </div>
    );
  }
  if (b.status !== "done") {
    return (
      <p className="muted" aria-live="polite">
        {b.status === "queued" ? "Waiting for the worker…" : "Building the model and the plans…"}
      </p>
    );
  }
  return <Built build={b} draft={draft} onEdit={onEdit} />;
}
