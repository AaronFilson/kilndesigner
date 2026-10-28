// A design, edited two ways: as choices in a form, or as the YAML design file. Switching trades
// the design through the API, which checks it, so each side always holds a valid design.
import type { Problem } from "@kilndesigner/api-client";
import { type ReactNode, useEffect, useRef, useState } from "react";

import { ApiError, checkDesign, type DesignInput, useLibrary } from "../api";
import type { KilnDocument, Layout } from "../design";
import { DesignForm } from "./DesignForm";
import { Problems } from "./Problems";
import { YamlEditor } from "./YamlEditor";

export type Mode = "form" | "yaml";

export interface Draft {
  document: KilnDocument;
  source: string;
}

/** A change made outside the editor (a port dragged on the model), applied once, by its id. */
export interface Edit {
  /** When it was made (Date.now()), so an editor started later passes it by. */
  id: number;
  apply: (document: KilnDocument) => KilnDocument;
}

function problemsOf(error: unknown): { message?: string; problems: Problem[] } {
  if (error instanceof ApiError) {
    return error.problems.length ? { problems: error.problems } : { message: error.message, problems: [] };
  }
  return { message: error instanceof Error ? error.message : String(error), problems: [] };
}

export function DesignEditor({
  initial,
  baseline,
  mode: initialMode = "form",
  onModeChange,
  toolbar,
  saving,
  saveError,
  onSave,
  layout,
  edit,
  onDocument,
}: {
  /** What to start editing. */
  initial: Draft;
  /** What counts as unchanged: the saved version, or null for a new design. */
  baseline: Draft | null;
  mode?: Mode;
  onModeChange?: (mode: Mode) => void;
  /** Shown before the save button: the version, the history. */
  toolbar?: (changed: boolean) => ReactNode;
  saving: boolean;
  saveError: unknown;
  onSave: (input: DesignInput) => void;
  /** Where the last build put the ports. */
  layout?: Layout;
  /** A change from outside the editor; the YAML tab gives way to the form to show it. */
  edit?: Edit | null;
  /** Told the form's document each time it changes. */
  onDocument?: (document: KilnDocument) => void;
}) {
  const library = useLibrary();
  const [mode, setMode] = useState<Mode>(initialMode);
  const [document, setDocument] = useState(initial.document);
  const [source, setSource] = useState(initial.source);
  // The form's document and the YAML agree until one of them is edited
  const [inStep, setInStep] = useState(true);
  const [switching, setSwitching] = useState(false);
  const [switchError, setSwitchError] = useState<unknown>(null);
  const applied = useRef<number | null>(null);
  // An edit made before this editor started (for the version before a save) isn't for it
  const started = useRef(Date.now());

  useEffect(() => onDocument?.(document), [document, onDocument]);

  const changed =
    baseline === null ||
    (mode === "form"
      ? JSON.stringify(document) !== JSON.stringify(baseline.document)
      : source !== baseline.source);

  const switchTo = async (next: Mode) => {
    if (next === mode) return;
    setSwitchError(null);
    if (inStep) {
      setMode(next);
      onModeChange?.(next);
      return;
    }
    setSwitching(true);
    try {
      const checked = await checkDesign(mode === "form" ? { document } : { source });
      if (mode === "form") setSource(checked.source);
      else setDocument(checked.document);
      setInStep(true);
      setMode(next);
      onModeChange?.(next);
    } catch (e) {
      setSwitchError(e);
    } finally {
      setSwitching(false);
    }
  };

  useEffect(() => {
    if (!edit || edit.id < started.current || applied.current === edit.id) return;
    if (mode === "yaml") {
      // Shown in the form: the YAML is checked first, and if it isn't valid the edit waits
      if (!switching && !switchError) void switchTo("form");
      return;
    }
    applied.current = edit.id;
    setDocument((d) => edit.apply(d));
    setInStep(false);
  }, [edit, mode, switching, switchError]); // switchTo is remade each render, so it isn't one

  const error = switchError ?? saveError;
  const shown = error ? problemsOf(error) : null;
  return (
    <section className="editor-pane">
      <div className="toolbar">
        <div role="tablist" aria-label="Edit the design as" className="tabs compact">
          {(
            [
              ["form", "Choices"],
              ["yaml", "YAML"],
            ] as const
          ).map(([id, label]) => (
            <button
              key={id}
              type="button"
              role="tab"
              aria-selected={mode === id}
              className={mode === id ? "tab active" : "tab"}
              disabled={switching}
              onClick={() => void switchTo(id)}
            >
              {label}
            </button>
          ))}
        </div>
        {toolbar?.(changed)}
        <button
          type="button"
          onClick={() => onSave(mode === "form" ? { document } : { source })}
          disabled={!changed || saving || switching}
        >
          Save and build
        </button>
      </div>
      {shown?.message && <p className="error">{shown.message}</p>}
      {shown && <Problems problems={shown.problems} />}
      {mode === "yaml" ? (
        <YamlEditor
          value={source}
          onChange={(v) => {
            setSource(v);
            setInStep(false);
          }}
        />
      ) : library.data ? (
        <DesignForm
          document={document}
          library={library.data}
          layout={layout}
          onChange={(d) => {
            setDocument(d);
            setInStep(false);
          }}
        />
      ) : library.isError ? (
        <p className="error">The choices could not be loaded: {library.error.message}</p>
      ) : (
        <p className="muted">Loading the choices…</p>
      )}
    </section>
  );
}
