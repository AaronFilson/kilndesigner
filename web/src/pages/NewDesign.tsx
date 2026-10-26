import { useNavigate } from "@tanstack/react-router";
import { useState } from "react";

import { checkDesign, useCreateDesign, useStartBuild, useTemplates } from "../api";
import { DesignEditor, type Draft, type Mode } from "../components/DesignEditor";
import type { KilnDocument } from "../design";

/** Start from a kind of kiln, or from a design file. */
export function NewDesign() {
  const templates = useTemplates();
  const create = useCreateDesign();
  const build = useStartBuild();
  const navigate = useNavigate();
  const [start, setStart] = useState<{ draft: Draft; mode: Mode; key: string } | null>(null);

  const open = async (files: FileList | null) => {
    const file = files?.[0];
    if (!file) return;
    const source = await file.text();
    // A file opens in the YAML tab as it is, even if it isn't valid yet: saving says what's wrong
    let document: KilnDocument;
    try {
      document = (await checkDesign({ source })).document;
    } catch {
      const empty = { width: "", depth: "", height: "" };
      document = { name: "", firing: {}, chamber: empty, lining: { walls: [] }, heat: {} };
    }
    setStart({ draft: { document, source }, mode: "yaml", key: `file-${Date.now()}` });
  };

  return (
    <main className="page">
      <header className="page-header">
        <h1>New design</h1>
        <label className="button secondary">
          Open a design file…
          <input type="file" accept=".yaml,.yml" hidden onChange={(e) => void open(e.target.files)} />
        </label>
      </header>
      <fieldset className="kiln-types">
        <legend>Start from a kind of kiln</legend>
        {templates.isPending && <p className="muted">Loading…</p>}
        {templates.isError && <p className="error">{templates.error.message}</p>}
        <div className="cards">
          {templates.data?.map((t) => (
            <button
              key={t.id}
              type="button"
              className={start?.key === t.id ? "card active" : "card"}
              aria-pressed={start?.key === t.id}
              onClick={() =>
                setStart({
                  draft: {
                    document: t.document as unknown as KilnDocument,
                    source: t.source,
                  },
                  mode: "form",
                  key: t.id,
                })
              }
            >
              <strong>{t.title}</strong>
              <span>{t.description}</span>
            </button>
          ))}
        </div>
      </fieldset>
      {start && (
        <DesignEditor
          key={start.key}
          initial={start.draft}
          baseline={null}
          mode={start.mode}
          saving={create.isPending}
          saveError={create.error}
          onSave={(input) =>
            create.mutate(input, {
              onSuccess: (design) => {
                build.mutate(design.latest.build_key);
                void navigate({ to: "/designs/$designId", params: { designId: design.id } });
              },
            })
          }
        />
      )}
    </main>
  );
}
