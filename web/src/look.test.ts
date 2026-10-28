import { afterEach, describe, expect, it } from "vitest";

import { colourOf, DEFAULT_LOOK, loadLook, saveLook } from "./palettes";
import { applyAppearance, loadAppearance, saveAppearance } from "./theme";

afterEach(() => localStorage.clear());

describe("appearance", () => {
  it("is the system theme in terracotta until one is chosen, and is remembered", () => {
    expect(loadAppearance()).toEqual({ theme: "system", accent: "terracotta" });
    saveAppearance({ theme: "dark", accent: "celadon" });
    expect(loadAppearance()).toEqual({ theme: "dark", accent: "celadon" });
  });

  it("ignores a stored choice it doesn't know", () => {
    localStorage.setItem("kilndesigner.appearance", '{"theme": "neon", "accent": "cobalt"}');
    expect(loadAppearance()).toEqual({ theme: "system", accent: "cobalt" });
    localStorage.setItem("kilndesigner.appearance", "not json");
    expect(loadAppearance()).toEqual({ theme: "system", accent: "terracotta" });
  });

  it("marks the root element for the stylesheet, and unmarks it for the defaults", () => {
    const root = document.createElement("html");
    applyAppearance({ theme: "light", accent: "tenmoku" }, root);
    expect(root.dataset).toMatchObject({ theme: "light", accent: "tenmoku" });
    applyAppearance({ theme: "system", accent: "terracotta" }, root);
    expect(root.dataset.theme).toBeUndefined();
    expect(root.dataset.accent).toBeUndefined();
  });
});

describe("the model's colours", () => {
  it("are as built, then the palette's, and a colour picked for a material beats both", () => {
    expect(colourOf(DEFAULT_LOOK, "Steel")).toBeUndefined();
    const grey = { ...DEFAULT_LOOK, palette: "grey" as const };
    expect(colourOf(grey, "Steel")).toBe("#404040");
    expect(colourOf(grey, "Something new")).toBeUndefined();
    expect(colourOf({ ...grey, custom: { Steel: "#ff00ff" } }, "Steel")).toBe("#ff00ff");
    expect(colourOf(grey, undefined)).toBeUndefined();
  });

  it("are remembered, keeping only real colours", () => {
    saveLook({ palette: "blueprint", edges: true, custom: { Steel: "#123456" } });
    expect(loadLook()).toEqual({ palette: "blueprint", edges: true, custom: { Steel: "#123456" } });
    localStorage.setItem(
      "kilndesigner.viewer",
      '{"palette": "plaid", "custom": {"Steel": "red", "Burners": "#00ff00"}}',
    );
    expect(loadLook()).toEqual({ palette: "built", edges: false, custom: { Burners: "#00ff00" } });
  });
});
