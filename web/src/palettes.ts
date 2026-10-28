// Colour schemes for the 3D model, by what each part is made of. The names are the engine's (the
// "kind" in a build's parts.json, from geometry.KIND_NAMES). "As built" keeps the colours the
// engine gave the model; the others recolour it in the viewer, with no rebuild. A part whose
// kind a palette doesn't name keeps its built colour.

export type PaletteId = "built" | "contrast" | "grey" | "blueprint";

export interface Palette {
  id: PaletteId;
  label: string;
  colours: Record<string, string>;
  /** The viewer's background, when the palette needs its own. */
  background?: string;
  /** The colour of the parts' outlines, when they're shown. */
  edges: string;
}

export const PALETTES: Palette[] = [
  { id: "built", label: "As built", colours: {}, edges: "#2b2622" },
  {
    // Okabe and Ito's colour-blind safe set, one hue a material
    id: "contrast",
    label: "Colour-blind safe",
    colours: {
      "Insulating firebrick": "#f0e442",
      "Hard firebrick": "#d55e00",
      "Ceramic fibre blanket": "#56b4e9",
      "Ceramic fibre board": "#0072b2",
      "Insulating castable": "#e69f00",
      "Dense castable": "#cc79a7",
      "Backup insulation": "#009e73",
      Elements: "#b0b0b0",
      Steel: "#5a5a5a",
      Burners: "#000000",
    },
    edges: "#1f1b16",
  },
  {
    id: "grey",
    label: "Greyscale",
    colours: {
      "Insulating firebrick": "#e6e6e6",
      "Hard firebrick": "#8c8c8c",
      "Ceramic fibre blanket": "#ffffff",
      "Ceramic fibre board": "#f2f2f2",
      "Insulating castable": "#cfcfcf",
      "Dense castable": "#a6a6a6",
      "Backup insulation": "#d9d9d9",
      Elements: "#707070",
      Steel: "#404040",
      Burners: "#595959",
    },
    edges: "#262626",
  },
  {
    id: "blueprint",
    label: "Blueprint",
    colours: {
      "Insulating firebrick": "#d6e6f5",
      "Hard firebrick": "#8fb3d9",
      "Ceramic fibre blanket": "#f0f7ff",
      "Ceramic fibre board": "#e0eefc",
      "Insulating castable": "#b8d0ea",
      "Dense castable": "#7aa0cc",
      "Backup insulation": "#c9dcf0",
      Elements: "#5b84b8",
      Steel: "#2c4f7c",
      Burners: "#f2c14e",
    },
    background: "#12355b",
    edges: "#e8f1ff",
  },
];

export function palette(id: PaletteId): Palette {
  return PALETTES.find((p) => p.id === id) ?? PALETTES[0]!;
}

/** The viewer's look: a palette, outlines or not, and colours the user picked for materials. */
export interface ViewerLook {
  palette: PaletteId;
  edges: boolean;
  custom: Record<string, string>;
}

const KEY = "kilndesigner.viewer";
const HEX = /^#[0-9a-f]{6}$/i;
export const DEFAULT_LOOK: ViewerLook = { palette: "built", edges: false, custom: {} };

export function loadLook(): ViewerLook {
  try {
    const saved = JSON.parse(localStorage.getItem(KEY) ?? "{}") as Record<string, unknown>;
    const custom: Record<string, string> = {};
    if (saved.custom && typeof saved.custom === "object") {
      for (const [kind, colour] of Object.entries(saved.custom)) {
        if (typeof colour === "string" && HEX.test(colour)) custom[kind] = colour;
      }
    }
    return {
      palette: PALETTES.some((p) => p.id === saved.palette) ? (saved.palette as PaletteId) : "built",
      edges: saved.edges === true,
      custom,
    };
  } catch {
    return DEFAULT_LOOK;
  }
}

export function saveLook(look: ViewerLook): void {
  try {
    localStorage.setItem(KEY, JSON.stringify(look));
  } catch {
    // Storage is blocked: the look lasts until the page is closed
  }
}

/** The colour a material is shown in: the user's pick, the palette's, or undefined for as built. */
export function colourOf(look: ViewerLook, kind: string | undefined): string | undefined {
  if (kind === undefined) return undefined;
  return look.custom[kind] ?? palette(look.palette).colours[kind];
}
