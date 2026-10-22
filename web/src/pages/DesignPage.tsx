import type { Design } from "@kilndesigner/api-client";
import { useParams } from "@tanstack/react-router";
import { useState } from "react";

import { api, ApiError, useDesign, useSaveVersion, useStartBuild } from "../api";
import { BuildPanel } from "../components/BuildPanel";
import { Problems } from "../components/Problems";
import { YamlEditor } from "../components/YamlEditor";

function Editor({ design }: { design: Design }) {
  const [source, setSource] = useState(design.latest.source);
  const save = useSaveVersion(design.id);
  const build = useStartBuild();
  const changed = source !== design.latest.source;

  const onSave = () =>
    save.mutate(source, { onSuccess: (saved) => build.mutate(saved.latest.build_key) });

  const restore = async (number: number) => {
    const { data } = await api.GET("/api/designs/{design_id}/versions/{number}", {
      params: { path: { design_id: design.id, number } },
    });
    if (data) setSource(data.source);
  };

  const error = save.error;
  return (
    <section className="editor-pane">
      <div className="toolbar">
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
        <button type="button" onClick={onSave} disabled={!changed || save.isPending}>
          Save and build
        </button>
      </div>
      {error && !(error instanceof ApiError && error.problems.length) && (
        <p className="error">{error.message}</p>
      )}
      {error instanceof ApiError && <Problems problems={error.problems} />}
      <YamlEditor value={source} onChange={setSource} />
    </section>
  );
}

export function DesignPage() {
  const { designId } = useParams({ from: "/designs/$designId" });
  const design = useDesign(designId);

  if (design.isPending) return <main className="page muted">Loading…</main>;
  if (design.isError) return <main className="page error">{design.error.message}</main>;
  const d = design.data;
  return (
    <main className="page design">
      <header className="page-header">
        <h1>{d.name}</h1>
      </header>
      <div className="split">
        <Editor key={d.id} design={d} />
        <section className="result-pane">
          <BuildPanel key={d.latest.build_key} buildKey={d.latest.build_key} />
        </section>
      </div>
    </main>
  );
}
