// How the app looks: light, dark or as the system says, and an accent colour named for a glaze.
// A per-browser choice, kept in localStorage; a browser that won't store it just gets the default.

export type Theme = "system" | "light" | "dark";
export type Accent = "terracotta" | "shino" | "celadon" | "cobalt" | "tenmoku" | "copper";

export const THEMES: [Theme, string][] = [
  ["system", "As the system"],
  ["light", "Light"],
  ["dark", "Dark"],
];

/** Each accent passes WCAG AA (4.5:1) against the page and under button text, in both themes. */
export const ACCENTS: [Accent, string][] = [
  ["terracotta", "Terracotta"],
  ["shino", "Shino"],
  ["celadon", "Celadon"],
  ["cobalt", "Cobalt"],
  ["tenmoku", "Tenmoku"],
  ["copper", "Copper red"],
];

export interface Appearance {
  theme: Theme;
  accent: Accent;
}

const KEY = "kilndesigner.appearance";
export const DEFAULT_APPEARANCE: Appearance = { theme: "system", accent: "terracotta" };

const isTheme = (v: unknown): v is Theme => THEMES.some(([t]) => t === v);
const isAccent = (v: unknown): v is Accent => ACCENTS.some(([a]) => a === v);

export function loadAppearance(): Appearance {
  try {
    const saved = JSON.parse(localStorage.getItem(KEY) ?? "{}") as Record<string, unknown>;
    return {
      theme: isTheme(saved.theme) ? saved.theme : DEFAULT_APPEARANCE.theme,
      accent: isAccent(saved.accent) ? saved.accent : DEFAULT_APPEARANCE.accent,
    };
  } catch {
    return DEFAULT_APPEARANCE;
  }
}

export function saveAppearance(appearance: Appearance): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(appearance));
  } catch {
    // Storage is blocked (a private window): the choice lasts until the page is closed
  }
}

/** Sets the page's theme and accent: styles.css reads them from the root element. */
export function applyAppearance({ theme, accent }: Appearance, root = document.documentElement): void {
  if (theme === "system") delete root.dataset.theme;
  else root.dataset.theme = theme;
  if (accent === DEFAULT_APPEARANCE.accent) delete root.dataset.accent;
  else root.dataset.accent = accent;
}
