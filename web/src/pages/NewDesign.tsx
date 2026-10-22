import { useNavigate } from "@tanstack/react-router";
import { useState } from "react";

import { ApiError, useCreateDesign, useStartBuild } from "../api";
import { Problems } from "../components/Problems";
import { YamlEditor } from "../components/YamlEditor";

export function NewDesign() {
  const [source, setSource] = useState("");
  const create = useCreateDesign();
  const build = useStartBuild();
  const navigate = useNavigate();

  const save = () =>
    create.mutate(source, {
      onSuccess: (design) => {
        build.mutate(design.latest.build_key);
        void navigate({ to: "/designs/$designId", params: { designId: design.id } });
      },
    });

  const open = async (files: FileList | null) => {
    const file = files?.[0];
    if (file) setSource(await file.text());
  };

  const error = create.error;
  return (
    <main className="page">
      <header className="page-header">
        <h1>New design</h1>
        <label className="button secondary">
          Open a design file…
          <input type="file" accept=".yaml,.yml" hidden onChange={(e) => void open(e.target.files)} />
        </label>
        <button type="button" onClick={save} disabled={!source.trim() || create.isPending}>
          Save and build
        </button>
      </header>
      <p className="muted">
        Paste or open a design file. The files in the repository's <code>examples/</code> folder are a
        good start.
      </p>
      {error && !(error instanceof ApiError && error.problems.length) && (
        <p className="error">{error.message}</p>
      )}
      {error instanceof ApiError && <Problems problems={error.problems} />}
      <YamlEditor value={source} onChange={setSource} />
    </main>
  );
}
