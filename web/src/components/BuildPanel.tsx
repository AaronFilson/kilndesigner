// A version's build: start it, follow it, then show the model, the files and the report.
import type { Build } from "@kilndesigner/api-client";

import { fileUrl, useBuild, useReport, useStartBuild } from "../api";
import { KilnViewer } from "./KilnViewer";
import { ReportView } from "./ReportView";

const DOWNLOADS: Record<string, string> = {
  "plans.pdf": "Plans (PDF)",
  "sections.dxf": "Sections (DXF)",
  "kiln.step": "3D model (STEP)",
  "kiln.glb": "3D model (glTF)",
  "report.json": "Report (JSON)",
};

function Built({ build }: { build: Build }) {
  const report = useReport(build);
  return (
    <>
      {build.files.includes("kiln.glb") && <KilnViewer url={fileUrl(build.key, "kiln.glb")} />}
      {build.notes.map((note) => (
        <p key={note} className="note">
          {note}
        </p>
      ))}
      <ul className="downloads">
        {build.files.map((name) => (
          <li key={name}>
            <a href={fileUrl(build.key, name)} download>
              {DOWNLOADS[name] ?? name}
            </a>
          </li>
        ))}
      </ul>
      {report.data && <ReportView report={report.data} />}
      {report.error && <p className="error">The report could not be loaded: {report.error.message}</p>}
    </>
  );
}

export function BuildPanel({ buildKey }: { buildKey: string }) {
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
  return <Built build={b} />;
}
