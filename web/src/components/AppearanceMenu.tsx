// The theme and accent colour, chosen in the top bar and remembered by this browser.
import { useId, useState } from "react";

import {
  ACCENTS,
  type Accent,
  type Appearance,
  applyAppearance,
  loadAppearance,
  saveAppearance,
  THEMES,
  type Theme,
} from "../theme";

export function AppearanceMenu() {
  const [appearance, setAppearance] = useState<Appearance>(loadAppearance);
  const id = useId();
  const change = (next: Appearance) => {
    setAppearance(next);
    applyAppearance(next);
    saveAppearance(next);
  };
  return (
    <div className="appearance" role="group" aria-label="Appearance">
      <label htmlFor={`${id}-theme`}>Theme</label>
      <select
        id={`${id}-theme`}
        value={appearance.theme}
        onChange={(e) => change({ ...appearance, theme: e.target.value as Theme })}
      >
        {THEMES.map(([value, label]) => (
          <option key={value} value={value}>
            {label}
          </option>
        ))}
      </select>
      <label htmlFor={`${id}-accent`}>Accent colour</label>
      <select
        id={`${id}-accent`}
        value={appearance.accent}
        onChange={(e) => change({ ...appearance, accent: e.target.value as Accent })}
      >
        {ACCENTS.map(([value, label]) => (
          <option key={value} value={value}>
            {label}
          </option>
        ))}
      </select>
    </div>
  );
}
