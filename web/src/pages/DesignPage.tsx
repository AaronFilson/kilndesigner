import type { Design } from "@kilndesigner/api-client";
import { useParams } from "@tanstack/react-router";
import { useState } from "react";

import { api, useDesign, useSaveVersion, useStartBuild } from "../api";
import { BuildPanel } from "../components/BuildPanel";
import { DesignEditor, type Draft, type Mode } from "../components/DesignEditor";
import type { KilnDocument } from "../design";

function Editor({
  design,
  mode,
  onModeChange,
}: {
  design: Design;
  mode: Mode;
  onModeChange: (mode: Mode) => void;
}) {
  const save = useSaveVersion(design.id);
  const build = useStartBuild();
  const latest: Draft = {
    document: design.latest.document as unknown as KilnDocument,
    source: design.latest.source,
  };
  // Loading an earlier version starts the editor again from it
  const [loaded, setLoaded] = useState<{ draft: Draft; key: string }>({
    draft: latest,
    key: `v${design.latest.number}`,
  });

  const restore = async (number: number) => {
    const { data } = await api.GET("/api/designs/{design_id}/versions/{number}", {
      params: { path: { design_id: design.id, number } },
    });
    if (data) {
      setLoaded({
        draft: { document: data.document as unknown as KilnDocument, source: data.source },
        key: `v${number}-${Date.now()}`,
      });
    }
  };

  return (
    <DesignEditor
      key={loaded.key}
      initial={loaded.draft}
      baseline={latest}
      mode={mode}
      onModeChange={onModeChange}
      saving={save.isPending}
      saveError={save.error}
      onSave={(input) =>
        save.mutate(input, { onSuccess: (saved) => build.mutate(saved.latest.build_key) })
      }
      toolbar={(changed) => (
        <>
          <span className="muted">
            Version {design.latest.number}
            {changed && " · unsaved changes"}
          </span>
          <select
            aria-label="Load an earlier version into the editor"
            value=""
            onChange={(e) => void restore(Number(e.target.value))}
          >
            <option value="">History…</option>
            {[...design.versions].reverse().map((v) => (
              <option key={v.number} value={v.number}>
                Version {v.number}, {new Date(v.created_at).toLocaleString()}
              </option>
            ))}
          </select>
        </>
      )}
    />
  );
}

export function DesignPage() {
  const { designId } = useParams({ from: "/designs/$designId" });
  const design = useDesign(designId);
  // Kept here, so saving (which starts the editor again on the new version) keeps the tab
  const [mode, setMode] = useState<Mode>("form");

  if (design.isPending) return <main className="page muted">Loading…</main>;
  if (design.isError) return <main className="page error">{design.error.message}</main>;
  const d = design.data;
  return (
    <main className="page design">
      <header className="page-header">
        <h1>{d.name}</h1>
      </header>
      <div className="split">
        <Editor
          key={`${d.id}-${d.latest.number}`}
          design={d}
          mode={mode}
          onModeChange={setMode}
        />
        <section className="result-pane">
          <BuildPanel key={d.latest.build_key} buildKey={d.latest.build_key} />
        </section>
      </div>
    </main>
  );
}
