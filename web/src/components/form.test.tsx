import type { Library } from "@kilndesigner/api-client";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { type KilnDocument, setIn, splitQuantity } from "../design";
import { DesignForm } from "./DesignForm";
import { legend } from "./KilnViewer";

afterEach(cleanup);

describe("splitQuantity", () => {
  it("reads the API's quantities back into a number and a unit to choose", () => {
    expect(splitQuantity("22.5 in")).toEqual(["22.5", "in"]);
    expect(splitQuantity("70 °F")).toEqual(["70", "degF"]);
    expect(splitQuantity("0.12 $ / kWh")).toEqual(["0.12", "USD/kWh"]);
    expect(splitQuantity(undefined)).toEqual(["", ""]);
  });
});

describe("setIn", () => {
  it("changes one value and leaves the rest, and the original, alone", () => {
    const doc = { a: { b: 1, c: [1, 2] }, d: 2 };
    expect(setIn(doc, ["a", "c", 1], 5)).toEqual({ a: { b: 1, c: [1, 5] }, d: 2 });
    expect(setIn(doc, ["a", "b"], undefined)).toEqual({ a: { c: [1, 2] }, d: 2 });
    expect(doc).toEqual({ a: { b: 1, c: [1, 2] }, d: 2 });
  });
});

describe("legend", () => {
  it("lists each material once with its colour", () => {
    expect(
      legend({
        a: { title: "", detail: "", kind: "Steel", colour: "#4c525c" },
        b: { title: "", detail: "", kind: "Hard firebrick", colour: "#b8734c" },
        c: { title: "", detail: "", kind: "Steel", colour: "#4c525c" },
        d: { title: "", detail: "" },
      }),
    ).toEqual([
      ["Steel", "#4c525c"],
      ["Hard firebrick", "#b8734c"],
    ]);
  });
});

const library: Library = {
  materials: [
    { id: "ifb-k23", name: "K-23", kind: "insulating_firebrick", max_service: "2300 degF", density: "" },
    { id: "kaowool", name: "Blanket", kind: "fibre_blanket", max_service: "2000 degF", density: "" },
  ],
  ingredients: [
    { id: "mulcoa-70", name: "Mulcoa 70", role: "aggregate", needs_density: false },
    { id: "secar-71", name: "Secar 71", role: "cement", needs_density: true },
  ],
  alloys: [{ id: "kanthal-a1", name: "Kanthal A1" }],
  cones: ["06", "6", "10"],
  cone_rates: { "06": [60, 150], "6": [60, 150], "10": [60, 150] },
  burners: [{ id: "GACO MR750", name: "GACO MR750 (venturi)" }],
};

const electric: KilnDocument = {
  name: "Test",
  firing: { cone: "10" },
  chamber: { width: "22.5 in", depth: "22.5 in", height: "24 in" },
  lining: { walls: [{ material: "ifb-k23", thickness: "4.5 in" }] },
  heat: { electric: { supply: { voltage: "240 V", phase: 1, breaker: "60 A" } } },
};

function form(doc: KilnDocument) {
  const onChange = vi.fn<(d: KilnDocument) => void>();
  render(<DesignForm document={doc} library={library} onChange={onChange} />);
  return () => onChange.mock.lastCall?.[0];
}

describe("DesignForm", () => {
  it("changes a size, keeping its unit", () => {
    const last = form(electric);
    fireEvent.change(screen.getByLabelText("Width"), { target: { value: "30" } });
    expect(last()?.chamber.width).toBe("30 in");
    fireEvent.change(screen.getByLabelText("Height, unit"), { target: { value: "mm" } });
    expect(last()?.chamber.height).toBe("24 mm");
  });

  it("adds, moves and removes lining layers", () => {
    const last = form(electric);
    fireEvent.click(screen.getByRole("button", { name: "Add a layer to the walls" }));
    expect(last()?.lining.walls).toHaveLength(2);
    const two: KilnDocument = setIn(electric, ["lining", "walls", 1], {
      material: "kaowool",
      thickness: "1 in",
    });
    cleanup();
    const after = form(two);
    fireEvent.click(screen.getByRole("button", { name: "Move walls layer 2 in" }));
    expect(after()?.lining.walls.map((l) => l.material)).toEqual(["kaowool", "ifb-k23"]);
    fireEvent.click(screen.getByRole("button", { name: "Remove walls layer 1" }));
    expect(after()?.lining.walls.map((l) => l.material)).toEqual(["kaowool"]);
  });

  it("gives the floor its own layers when it isn't the same as the walls", () => {
    const last = form(electric);
    fireEvent.click(screen.getByLabelText("Floor: the same layers as the walls"));
    expect(last()?.lining.floor).toEqual(electric.lining.walls);
  });

  it("adds propane with a draft, and won't take away the only heat", () => {
    const last = form(electric);
    expect(screen.getByLabelText("Heat with electric elements")).toHaveProperty("disabled", true);
    fireEvent.click(screen.getByLabelText("Fire with propane"));
    expect(last()?.heat.gas?.supply).toEqual({ type: "cylinders", count: 4 });
    expect(last()?.draft).toEqual({ type: "cross", flue_wall: "back" });
  });

  it("turns a flat roof into an arch with a rise", () => {
    const last = form(electric);
    fireEvent.change(screen.getByLabelText("Roof"), { target: { value: "sprung_arch" } });
    expect(last()?.roof).toEqual({ type: "sprung_arch", rise: "3.75 in" });
  });
});

describe("DesignForm, castables", () => {
  it("adds a castable that the lining can then use", () => {
    const last = form(electric);
    fireEvent.click(screen.getByRole("button", { name: "Add a castable" }));
    const mix = last()?.castables?.[0];
    expect(mix).toMatchObject({ id: "my-castable-1", water: "10 lb", foam: 50 });
    cleanup();
    form(last() as KilnDocument);
    const select = screen.getByLabelText("Walls, layer 1 material") as HTMLSelectElement;
    expect([...select.options].map((o) => o.value)).toContain("my-castable-1");
  });

  it("asks for a density where the library has none", () => {
    const withCement: KilnDocument = {
      ...electric,
      castables: [
        {
          id: "mix",
          name: "Mix",
          ingredients: [{ ingredient: "secar-71", mass: "5 lb" }],
          water: "2 lb",
        },
      ],
    };
    const last = form(withCement);
    const density = screen.getByLabelText("Mix, ingredient 1 true density (from its sheet)");
    fireEvent.change(density, { target: { value: "2.9" } });
    expect(last()?.castables?.[0]?.ingredients[0]?.density).toBe("2.9 g/cm**3");
  });
});
