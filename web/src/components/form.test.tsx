import type { Library } from "@kilndesigner/api-client";
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { useState } from "react";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  fromMm,
  type KilnDocument,
  type Layout,
  setIn,
  splitQuantity,
  toMm,
  type WallFrame,
} from "../design";
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

  it("makes what's missing on the way, a list where the next step is a number", () => {
    expect(setIn({}, ["spy_holes", "places", 0, "wall"], "back")).toEqual({
      spy_holes: { places: [{ wall: "back" }] },
    });
    expect(setIn({ a: 1 }, [], { b: 2 })).toEqual({ b: 2 });
  });
});

describe("lengths", () => {
  it("are read in millimetres, from any length unit, and nothing else", () => {
    expect([toMm("1 ft"), toMm("2 m"), toMm("3 cm"), toMm("6 in")]).toEqual([304.8, 2000, 30, 6 * 25.4]);
    expect([toMm("70 degF"), toMm("in"), toMm(undefined)]).toEqual([undefined, undefined, undefined]);
  });

  it("are written in the design's units: inches to the nearest eighth, or whole millimetres", () => {
    expect(fromMm(27, "us")).toBe("1.125 in");
    expect(fromMm(304.8, undefined)).toBe("12 in");
    expect(fromMm(12.6, "metric")).toBe("13 mm");
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
  alloys: [
    { id: "kanthal-a1", name: "Kanthal A1" },
    { id: "kanthal-apm", name: "Kanthal APM" },
  ],
  cones: ["06", "04", "6", "10", "15"],
  cone_rates: { "06": [60, 150], "6": [60, 150], "10": [60, 150], "15": [100] },
  burners: [
    { id: "GACO MR750", name: "GACO MR750 (venturi)" },
    { id: "Pine Ridge P1", name: "Pine Ridge P1 (power)" },
  ],
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

/** The form holding the design as it's edited, as the editor does, so edits build on each other. */
function live(doc: KilnDocument, layout?: Layout, lib: Library = library) {
  let latest = doc;
  function Live() {
    const [d, setD] = useState(doc);
    const onChange = (next: KilnDocument) => {
      latest = next;
      setD(next);
    };
    return <DesignForm document={d} library={lib} layout={layout} onChange={onChange} />;
  }
  render(<Live />);
  return () => latest;
}

const field = (label: string) => screen.getByLabelText(label) as HTMLInputElement;
const set = (label: string, value: string) =>
  fireEvent.change(screen.getByLabelText(label), { target: { value } });
const disabled = (button: string) =>
  (screen.getByRole("button", { name: button }) as HTMLButtonElement).disabled;
const options = (label: string) =>
  [...(screen.getByLabelText(label) as HTMLSelectElement).options].map((o) => o.textContent);

describe("DesignForm", () => {
  it("changes a size, keeping its unit", () => {
    const last = form(electric);
    fireEvent.change(screen.getByLabelText("Width"), { target: { value: "30" } });
    expect(last()?.chamber.width).toBe("30 in");
    fireEvent.change(screen.getByLabelText("Height, unit"), { target: { value: "mm" } });
    expect(last()?.chamber.height).toBe("24 mm");
  });

  it("shows a size in a unit it doesn't list as written, and keeps that unit when it's edited", () => {
    const last = form({ ...electric, chamber: { ...electric.chamber, width: "1 m" } });
    expect(field("Width").value).toBe("1");
    expect((screen.getByLabelText("Width, unit") as HTMLSelectElement).value).toBe("m");
    fireEvent.change(screen.getByLabelText("Width"), { target: { value: "1.2" } });
    expect(last()?.chamber.width).toBe("1.2 m");
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
    fireEvent.click(screen.getByLabelText("Fire with gas"));
    expect(last()?.heat.gas?.supply).toEqual({ type: "cylinders", count: 4 });
    expect(last()?.draft).toEqual({ type: "cross", flue_wall: "back" });
  });

  it("turns a flat roof into an arch with a rise", () => {
    const last = form(electric);
    fireEvent.change(screen.getByLabelText("Roof"), { target: { value: "sprung_arch" } });
    expect(last()?.roof).toEqual({ type: "sprung_arch", rise: "3.75 in" });
  });

  it("offers a catenary from the floor and a dome, keeping a rise between arch and dome", () => {
    const arched: KilnDocument = { ...electric, roof: { type: "sprung_arch", rise: "5 in" } };
    const last = form(arched);
    expect(screen.getByLabelText("Height, to the springline")).toBeTruthy();
    fireEvent.change(screen.getByLabelText("Roof"), { target: { value: "dome" } });
    expect(last()?.roof).toEqual({ type: "dome", rise: "5 in" });
    fireEvent.change(screen.getByLabelText("Roof"), { target: { value: "catenary_arch" } });
    expect(last()?.roof).toEqual({ type: "catenary_arch" });
    cleanup();
    // A catenary is its own side walls: the door, burners and flue move off them
    const sided: KilnDocument = {
      ...electric,
      loading: { face: "right" },
      heat: { gas: { burners: { wall: "left" }, supply: { type: "cylinders", count: 4 } } },
      draft: { type: "cross", flue_wall: "right" },
    };
    const moved = form(sided);
    fireEvent.change(screen.getByLabelText("Roof"), { target: { value: "catenary_arch" } });
    expect(moved()?.loading?.face).toBe("front");
    expect(moved()?.heat.gas?.burners?.wall).toBe("front");
    expect(moved()?.draft?.flue_wall).toBe("back");
    cleanup();
    form({ ...electric, roof: { type: "catenary_arch" } });
    expect(screen.getByLabelText("Height, to the crown")).toBeTruthy();
    expect(screen.getByLabelText("Width, at the floor")).toBeTruthy();
    expect(screen.queryByLabelText("Arch rise")).toBeNull();
    expect(screen.getByText(/springs from the floor and is the side walls too/)).toBeTruthy();
  });

  it("puts springs on an arch's tie rods with their rate, and takes them off again", () => {
    const last = live({ ...electric, roof: { type: "sprung_arch", rise: "3.75 in" } });
    expect(screen.queryByLabelText("Each spring's rate, from its listing")).toBeNull();
    set("Tie rods", "springs");
    expect(last().roof).toEqual({
      type: "sprung_arch",
      rise: "3.75 in",
      ties: "springs",
      spring_rate: "283 lbf/in",
    });
    set("Each spring's rate, from its listing", "300");
    expect(last().roof).toMatchObject({ spring_rate: "300 lbf/in" });
    set("Tie rods", "rigid");
    expect(last().roof).toEqual({ type: "sprung_arch", rise: "3.75 in" });
  });

  it("gives a dome a rise at its centre, and a flat roof none", () => {
    const last = live({ ...electric, roof: { type: "dome", rise: "4 in" } });
    expect(screen.getByText(/A dome on all four walls/)).toBeTruthy();
    set("Dome rise, at the centre", "6");
    expect(last().roof).toEqual({ type: "dome", rise: "6 in" });
    set("Roof", "flat");
    expect(last().roof).toEqual({ type: "flat" });
    expect(field("Height")).toBeTruthy();
    expect(screen.queryByLabelText(/rise/)).toBeNull();
  });

  it("stays on the page when Enter submits it", () => {
    form(electric);
    expect(fireEvent.submit(screen.getByRole("form", { name: "Design" }))).toBe(false);
  });
});

describe("DesignForm, the kiln", () => {
  it("names the kiln, shows results in metric, and fires to a cone at a rate it's tabulated for", () => {
    const last = live(electric);
    set("Name", "Big one");
    set("Show results in", "metric");
    set("Final heating rate", "150");
    set("Fire to cone", "6");
    expect(last()).toMatchObject({
      name: "Big one",
      units: "metric",
      firing: { cone: "6", final_rate: 150 },
    });
    // Cone 15 is tabulated at one rate, so the rate moves to it
    set("Fire to cone", "15");
    expect(last().firing).toEqual({ cone: "15", final_rate: 100 });
    expect(options("Final heating rate")).toEqual(["100 °C/h"]);
    // A cone with no rates of its own is fired at 60 °C/h
    set("Fire to cone", "04");
    expect(last().firing).toEqual({ cone: "04", final_rate: 60 });
    expect(options("Final heating rate")).toEqual(["60 °C/h"]);
  });

  it("fires to a top temperature instead, in either scale", () => {
    const last = live({ ...electric, firing: {} });
    expect(options("Fire to cone")[0]).toBe("Choose…");
    expect(screen.queryByLabelText("Final heating rate")).toBeNull();
    // A unit picked before there's a number waits for one
    set("Or a top temperature, unit", "degC");
    expect(last().firing).toEqual({});
    set("Or a top temperature", "1285");
    expect(last().firing.top_temperature).toBe("1285 degF");
    set("Or a top temperature, unit", "degC");
    expect(last().firing.top_temperature).toBe("1285 degC");
    set("Or a top temperature", "");
    expect(last().firing.top_temperature).toBeUndefined();
    // Choosing a cone then fires at 60 °C/h, without writing the rate in
    set("Fire to cone", "10");
    expect(last().firing).toEqual({ cone: "10" });
    expect(field("Final heating rate").value).toBe("60");
  });
});

describe("DesignForm, the setting", () => {
  it("weighs the ware as given, or as shelves and posts the engine weighs", () => {
    const last = live(electric);
    expect(field("Ware for the firing simulation").value).toBe("none");
    set("Ware for the firing simulation", "weight");
    set("Ware and furniture", "300");
    expect(last().firing.ware).toBe("300 lb");
    set("Ware for the firing simulation", "setting");
    expect(last().firing.ware).toBeUndefined();
    expect(last().firing.setting?.shelves.material).toBe("mullite");
    set("Shelf length", "20");
    set("Shelf width", "10");
    set("Shelf thickness", "0.75");
    set("Shelf material", "cordierite");
    set("Shelves a layer", "4");
    set("Layers of shelves", "3");
    set("Layers of shelves", "");
    set("Layers of shelves", "4");
    fireEvent.click(screen.getByLabelText("Posts"));
    set("Post width", "1.5");
    set("Post depth", "1.5");
    set("Post height", "6");
    set("Post material", "silicon-carbide");
    set("Posts a layer", "3");
    set("Ware's weight over the setting's (typically 6–8)", "6");
    expect(last().firing.setting).toEqual({
      shelves: {
        length: "20 in",
        width: "10 in",
        thickness: "0.75 in",
        material: "cordierite",
        per_layer: 4,
        layers: 4,
      },
      posts: { material: "silicon-carbide", width: "1.5 in", depth: "1.5 in", height: "6 in", per_layer: 3 },
      ware_ratio: 6,
    });
    set("Ware's weight over the setting's (typically 6–8)", "");
    expect(last().firing.setting?.ware_ratio).toBeUndefined();
    fireEvent.click(screen.getByLabelText("Posts"));
    expect(last().firing.setting?.posts).toBeUndefined();
    set("Ware for the firing simulation", "none");
    expect(last().firing.setting).toBeUndefined();
  });
});

describe("DesignForm, loading", () => {
  it("loads through a door in a wall, hinged in an electric kiln, or a car with its hardware's cost", () => {
    const last = live(electric);
    expect(field("Door").value).toBe("hinged");
    set("The door's wall", "right");
    set("Door", "bricked");
    expect(last().loading).toEqual({ face: "right", door: "bricked" });
    set("Ware goes in through", "car");
    expect(screen.queryByLabelText("Door")).toBeNull();
    set("The car's end", "back");
    set("Car hardware cost", "1500");
    expect(last().loading).toEqual({
      type: "car",
      face: "back",
      door: "bricked",
      car_hardware_cost: "1500 USD",
    });
  });

  it("loads a round electric kiln from the top, under a hinged lid", () => {
    const options = () =>
      Array.from(field("Ware goes in through").querySelectorAll("option")).map((o) => o.value);
    form(electric);
    expect(options()).toEqual(["door", "car"]);
    cleanup();
    const round: KilnDocument = {
      ...electric,
      chamber: { ...electric.chamber, shape: "round", depth: electric.chamber.width },
    };
    const last = live(round);
    expect(options()).toEqual(["door", "car", "lid"]);
    set("Ware goes in through", "lid");
    expect(last().loading).toEqual({ type: "lid" });
    expect(screen.queryByLabelText("Door")).toBeNull();
    expect(screen.getByText(/The walls have no door/)).toBeTruthy();
    set("The peepholes' wall", "back");
    expect(last().loading).toEqual({ type: "lid", face: "back" });
  });

  it("puts a door in part of a gas kiln's wall, and one into each chamber of a row", () => {
    const gas: KilnDocument = {
      ...electric,
      heat: { gas: { supply: { type: "cylinders", count: 4 } } },
    };
    const last = live(gas);
    expect(screen.queryByLabelText("Door width, inside the jambs")).toBeNull();
    fireEvent.click(screen.getByLabelText(/The door is in part of the wall/));
    expect(last().loading?.opening).toEqual({ width: "20 in", height: "36 in" });
    set("Door width, inside the jambs", "24");
    set("Door height, sill to the top of the opening", "30");
    set("Door's centre off the wall's middle, to the right from outside", "-1");
    set("Sill, above the floor", "2");
    set("Door head", "lintel");
    expect(last().loading?.opening).toEqual({
      width: "24 in",
      height: "30 in",
      across: "-1 in",
      sill: "2 in",
      head: "lintel",
    });
    // A door in each chamber only for chambers in a row, in a side wall
    expect(screen.queryByLabelText(/A door into each chamber/)).toBeNull();
    fireEvent.click(screen.getByLabelText(/The door is in part of the wall/));
    expect(last().loading?.opening).toBeUndefined();
    cleanup();
    const row = live({
      ...gas,
      chamber: { ...gas.chamber, chambers: 3 },
      loading: { face: "right", opening: { width: "20 in", height: "38 in" } },
    });
    fireEvent.click(screen.getByLabelText(/A door into each chamber/));
    expect(row().loading?.opening?.each_chamber).toBe(true);
    fireEvent.click(screen.getByLabelText(/A door into each chamber/));
    expect(row().loading?.opening?.each_chamber).toBeUndefined();
    cleanup();
    // An electric kiln's door is its whole front
    form(electric);
    expect(screen.queryByLabelText(/The door is in part of the wall/)).toBeNull();
  });

  it("bricks up a gas kiln's door unless told otherwise", () => {
    form({ ...electric, heat: { gas: { supply: { type: "cylinders", count: 4 } } } });
    expect(field("Door").value).toBe("bricked");
  });
});

describe("DesignForm, lining", () => {
  it("chooses each layer's material and thickness, and moves a layer out", () => {
    const fibre = { material: "kaowool", thickness: "1 in" };
    const last = live(setIn(electric, ["lining", "walls", 1], fibre));
    expect([disabled("Move walls layer 1 in"), disabled("Move walls layer 2 out")]).toEqual([true, true]);
    set("Walls, layer 1 material", "kaowool");
    set("Walls, layer 2 thickness", "2");
    fireEvent.click(screen.getByRole("button", { name: "Move walls layer 1 out" }));
    expect(last().lining.walls).toEqual([
      { material: "kaowool", thickness: "2 in" },
      { material: "kaowool", thickness: "4.5 in" },
    ]);
    set("Walls, layer 1 thickness", "");
    expect(last().lining.walls[0]).toEqual({ material: "kaowool", thickness: "" });
  });

  it("groups the materials by kind, naming a kind it doesn't know as the library does", () => {
    const mortar = { id: "m1", name: "Mortar", kind: "mortar", max_service: "2800 degF", density: "" };
    const withMortar: Library = { ...library, materials: [...library.materials, mortar] };
    live(electric, undefined, withMortar);
    const groups = [...screen.getByLabelText("Walls, layer 1 material").querySelectorAll("optgroup")];
    expect(groups.map((g) => [g.label, g.textContent])).toEqual([
      ["Insulating firebrick", "K-23 (to 2300 degF)"],
      ["Ceramic fibre", "Blanket (to 2000 degF)"],
      ["mortar", "Mortar (to 2800 degF)"],
    ]);
  });

  it("starts a lining with none with a layer of K-23", () => {
    const last = live({ ...electric, lining: { walls: [] } });
    fireEvent.click(screen.getByRole("button", { name: "Add a layer to the walls" }));
    expect(last().lining.walls).toEqual([{ material: "ifb-k23", thickness: "1 in" }]);
  });

  it("gives the roof its own layers to edit, then the walls' again", () => {
    const last = live(electric);
    fireEvent.click(screen.getByLabelText("Roof: the same layers as the walls"));
    set("Roof, layer 1 thickness", "9");
    expect(last().lining.roof).toEqual([{ material: "ifb-k23", thickness: "9 in" }]);
    expect(last().lining.walls).toEqual(electric.lining.walls);
    expect(disabled("Remove roof layer 1")).toBe(true);
    fireEvent.click(screen.getByLabelText("Roof: the same layers as the walls"));
    expect(last().lining.roof).toBeUndefined();
    expect(screen.queryByLabelText("Roof, layer 1 thickness")).toBeNull();
  });

  it("finishes the outside", () => {
    const last = live(electric);
    expect(field("Outside finish").value).toBe("oxidised_steel");
    set("Outside finish", "painted");
    expect(last().shell).toEqual({ finish: "painted" });
  });
});

describe("DesignForm, castables you mix", () => {
  const withMix: KilnDocument = {
    ...electric,
    castables: [
      {
        id: "mix",
        name: "Mix",
        ingredients: [{ ingredient: "secar-71", mass: "5 lb", density: "2.9 g/cm**3" }],
        water: "2 lb",
      },
    ],
  };

  it("edits a recipe's ingredients, water, foam and what was measured", () => {
    const last = live(withMix);
    set("Mix, ingredient 1 mass", "6");
    fireEvent.click(screen.getByRole("button", { name: "Add an ingredient to Mix" }));
    set("Mix, ingredient 2", "secar-71");
    // Another ingredient has its own density, so the one given goes with the old one
    set("Mix, ingredient 1", "mulcoa-70");
    set("Mix, water per batch", "3");
    set("Mix, air from foam (% of the cast volume)", "40");
    set("Mix, measured fired density (test pieces)", "60");
    set("Mix, measured linear shrinkage, %", "1.5");
    expect(last().castables?.[0]).toEqual({
      id: "mix",
      name: "Mix",
      ingredients: [
        { ingredient: "mulcoa-70", mass: "6 lb" },
        { ingredient: "secar-71", mass: "1 lb" },
      ],
      water: "3 lb",
      foam: 40,
      measured: { fired_density: "60 lb/ft**3", linear_shrinkage: 1.5 },
    });
    set("Mix, air from foam (% of the cast volume)", "");
    set("Mix, measured linear shrinkage, %", "");
    set("Mix, water per batch", "");
    set("Mix, ingredient 2 mass", "");
    expect(last().castables?.[0]).toMatchObject({
      water: "",
      foam: undefined,
      measured: { linear_shrinkage: undefined },
    });
    expect(last().castables?.[0]?.ingredients[1]).toEqual({ ingredient: "secar-71", mass: "" });
  });

  it("renames a castable and its id, removes ingredients down to one, and removes it", () => {
    const last = live(withMix);
    fireEvent.click(screen.getByRole("button", { name: "Add an ingredient to Mix" }));
    set("Castable name", "Light mix");
    set("Its id, for the lining", "light");
    fireEvent.click(screen.getByRole("button", { name: "Remove ingredient 1 from Light mix" }));
    expect(last().castables?.[0]).toMatchObject({
      id: "light",
      name: "Light mix",
      ingredients: [{ ingredient: "mulcoa-70" }],
    });
    expect(disabled("Remove ingredient 1 from Light mix")).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "Remove Light mix" }));
    expect(last().castables).toBeUndefined();
  });

  it("numbers a new castable past the ids already taken", () => {
    const last = live({ ...electric, castables: [{ ...withMix.castables![0]!, id: "my-castable-2" }] });
    fireEvent.click(screen.getByRole("button", { name: "Add a castable" }));
    expect(last().castables?.map((c) => [c.id, c.name])).toEqual([
      ["my-castable-2", "Mix"],
      ["my-castable-3", "My castable 3"],
    ]);
    // Each castable is edited on its own
    set("My castable 3, water per batch", "12");
    expect(last().castables?.map((c) => c.water)).toEqual(["2 lb", "12 lb"]);
  });
});

describe("DesignForm, electric elements", () => {
  it("sets the supply, the alloy and the walls the elements are on", () => {
    const last = live(electric);
    expect(options("Supply voltage")).toEqual(["120 V", "208 V", "240 V", "480 V"]);
    set("Supply voltage", "208");
    set("Phase", "3");
    set("Breaker", "50");
    set("Element alloy", "kanthal-apm");
    const walls = screen.getByRole("group", { name: "Walls with elements" });
    fireEvent.click(within(walls).getByLabelText("Front"));
    fireEvent.click(within(walls).getByLabelText("Left"));
    expect(last().heat.electric).toEqual({
      supply: { voltage: "208 V", phase: 3, breaker: "50 A" },
      alloy: "kanthal-apm",
      walls: ["right", "back", "front"],
    });
    expect(screen.getByText("A", { selector: ".unit" })).toBeTruthy(); // the breaker's only unit
  });

  it("keeps elements on one wall at least", () => {
    form(setIn(electric, ["heat", "electric", "walls"], ["back"]));
    const walls = screen.getByRole("group", { name: "Walls with elements" });
    expect((within(walls).getByLabelText("Back") as HTMLInputElement).disabled).toBe(true);
    expect((within(walls).getByLabelText("Front") as HTMLInputElement).disabled).toBe(false);
  });

  it("hands a hybrid over to gas above a temperature, and can drop either heat but not both", () => {
    const hybrid: KilnDocument = {
      ...electric,
      heat: { electric: electric.heat.electric, gas: { supply: { type: "cylinders", count: 4 } } },
      draft: { type: "down", flue_wall: "left" },
    };
    const last = live(hybrid);
    set("Elements hand over to gas above", "1800");
    expect(last().heat.electric?.off_above).toBe("1800 degF");
    fireEvent.click(screen.getByLabelText("Heat with electric elements"));
    expect(last().heat.electric).toBeUndefined();
    expect(field("Fire with gas").disabled).toBe(true);
    fireEvent.click(screen.getByLabelText("Heat with electric elements"));
    expect(last().heat.electric).toEqual({
      supply: { voltage: "240 V", phase: 1, breaker: "60 A" },
      alloy: "kanthal-a1",
      walls: ["left", "right", "back"],
    });
    fireEvent.click(screen.getByLabelText("Fire with gas"));
    expect(last().heat.gas).toBeUndefined();
    fireEvent.click(screen.getByLabelText("Fire with gas"));
    expect(last().heat.gas).toEqual({
      burners: { type: "venturi", wall: "front" },
      supply: { type: "cylinders", count: 4 },
      reduction: true,
    });
    expect(last().draft).toEqual({ type: "down", flue_wall: "left" }); // the draft it had is kept
  });
});

const gasKiln: KilnDocument = {
  ...electric,
  heat: { gas: { burners: { wall: "front" }, supply: { type: "cylinders", count: 4 } } },
  draft: { type: "cross", flue_wall: "back" },
};

describe("DesignForm, gas burners", () => {
  it("chooses the burners' type, then a model of that type, their number and their wall", () => {
    const last = live(gasKiln);
    expect(options("Burner model")).toEqual(["Chosen for you", "GACO MR750 (venturi)"]);
    set("Burner model", "GACO MR750");
    expect(last().heat.gas?.burners?.model).toBe("GACO MR750");
    set("Burner type", "power");
    expect(last().heat.gas?.burners).toEqual({ wall: "front", type: "power" });
    expect(options("Burner model")).toEqual(["Chosen for you", "Pine Ridge P1 (power)"]);
    set("Burner model", "Pine Ridge P1");
    set("Burner model", "");
    set("Number of burners (blank: chosen for you)", "3");
    set("Burners fire through", "left");
    expect(last().heat.gas?.burners).toEqual({ wall: "left", type: "power", count: 3 });
    set("Number of burners (blank: chosen for you)", "");
    expect(last().heat.gas?.burners?.count).toBeUndefined();
  });

  it("counts placed burners by their ports", () => {
    const places = [
      { wall: "front" as const, across: "-7 in", up: "5 in" },
      { wall: "front" as const, across: "7 in", up: "5 in" },
    ];
    form(setIn(gasKiln, ["heat", "gas", "burners", "places"], places));
    expect(screen.getByText("2 burners, one for each port placed under Ports and spy holes.")).toBeTruthy();
    expect(screen.queryByLabelText("Number of burners (blank: chosen for you)")).toBeNull();
  });

  it("supplies propane from cylinders or a tank", () => {
    const last = live(gasKiln);
    set("Cylinders", "6");
    expect(last().heat.gas?.supply).toEqual({ type: "cylinders", count: 6 });
    set("Cylinders", "");
    expect(last().heat.gas?.supply).toEqual({ type: "cylinders", count: 1 });
    set("Propane supply", "tank");
    expect(last().heat.gas?.supply).toEqual({ type: "tank", gallons: 250 });
    set("Tank size", "500");
    expect(last().heat.gas?.supply).toEqual({ type: "tank", gallons: 500 });
    set("Propane supply", "cylinders");
    expect(last().heat.gas?.supply).toEqual({ type: "cylinders", count: 4 });
  });

  it("fires in reduction or not, fast or slow, with a draft out through a flue wall", () => {
    const last = live(gasKiln);
    expect(field("Flue wall to chimney").value).toBe("9");
    fireEvent.click(screen.getByLabelText("Fired in reduction"));
    set("Burners sized for", "slow");
    set("Flue wall", "left");
    set("Flue wall to chimney", "12");
    expect(last().heat.gas).toMatchObject({ reduction: false, firing_speed: "slow" });
    expect(last().draft).toEqual({ type: "cross", flue_wall: "left", run_to_chimney: "12 in" });
    set("Draft", "up");
    expect(last().draft?.type).toBe("up");
    expect(screen.queryByLabelText("Flue wall")).toBeNull();
    expect(screen.queryByLabelText("Flue across from the middle (blank: in the middle)")).toBeNull();
  });
});

describe("DesignForm, site and costs", () => {
  it("records the air around the kiln and what things cost", () => {
    const last = live(electric);
    expect(field("Air around the kiln").value).toBe("70");
    set("Air around the kiln", "60");
    set("Coldest firing day", "-10");
    set("Coldest firing day, unit", "degC");
    set("Electricity price", "0.15");
    set("Propane price", "3.5");
    set("Materials budget", "5000");
    expect(last().site).toEqual({
      ambient: "60 degF",
      coldest_ambient: "-10 degC",
      electricity_price: "0.15 USD/kWh",
      propane_price: "3.5 USD/gallon",
      materials_budget: "5000 USD",
    });
    expect(screen.getByText("$/kWh")).toBeTruthy();
    expect(screen.getByText("$/gal")).toBeTruthy();
  });
});

describe("DesignForm, ports", () => {
  const gas: KilnDocument = {
    ...electric,
    heat: { gas: { burners: { wall: "front" }, supply: { type: "cylinders", count: 4 } } },
    draft: { type: "cross", flue_wall: "back" },
  };
  const frame = { origin: [0, 0, 0], normal: [0, -1, 0], right: [1, 0, 0], half_width: 300,
    thickness: 200, top: [] } as unknown as WallFrame; // prettier-ignore
  const layout: Layout = {
    units: "us",
    walls: { front: frame, back: frame, left: frame, right: frame },
    ports: [
      { name: "port/burner-1", title: "Burner port 1", kind: "burner", wall: "front",
        across: -177.8, up: 123.825, width: 120.65, height: 120.65, round: true, cut: true },
      { name: "port/spy-1", title: "Spy hole 1", kind: "spy", wall: "right", across: -76.2,
        up: 234.95, width: 57.15, height: 63.5, round: false, cut: true },
    ], // prettier-ignore
  };

  function gasForm(doc: KilnDocument, withLayout?: Layout) {
    const onChange = vi.fn<(d: KilnDocument) => void>();
    render(<DesignForm document={doc} library={library} layout={withLayout} onChange={onChange} />);
    return () => onChange.mock.lastCall?.[0];
  }

  it("places burners one by one, starting where the build put them", () => {
    const last = gasForm({ ...gas, heat: { gas: { ...gas.heat.gas!, burners: { count: 1 } } } }, layout);
    fireEvent.change(screen.getByLabelText("Burner ports go"), { target: { value: "placed" } });
    expect(last()?.heat.gas?.burners).toEqual({
      places: [{ wall: "front", across: "-7 in", up: "4.875 in" }],
    });
    cleanup();
    const placed = gasForm(last() as KilnDocument, layout);
    expect(screen.queryByLabelText("Number of burners (blank: chosen for you)")).toBeNull();
    fireEvent.change(screen.getByLabelText("Burner 1, wall"), { target: { value: "left" } });
    expect(placed()?.heat.gas?.burners?.places?.[0]?.wall).toBe("left");
    fireEvent.click(screen.getByRole("button", { name: "Add a burner" }));
    expect(placed()?.heat.gas?.burners?.places).toHaveLength(2);
  });

  it("places spy holes one by one, down to none, and adds one up the door", () => {
    const door = { ...gas, loading: { type: "door" as const, face: "right" as const } };
    const last = gasForm(door, layout);
    fireEvent.change(screen.getByLabelText("Spy holes go"), { target: { value: "placed" } });
    expect(last()?.spy_holes).toEqual({ places: [{ wall: "right", across: "-3 in", up: "9.25 in" }] });
    cleanup();
    const placed = gasForm(last() as KilnDocument, layout);
    fireEvent.click(screen.getByRole("button", { name: "Remove spy hole 1" }));
    expect(placed()?.spy_holes).toEqual({ places: [] });
    cleanup();
    const none = gasForm(placed() as KilnDocument, layout);
    fireEvent.click(screen.getByRole("button", { name: "Add a spy hole" }));
    // Up the middle of the door's wall, halfway up the 24 in chamber
    expect(none()?.spy_holes?.places).toEqual([{ wall: "right", across: "0 in", up: "12 in" }]);
  });

  it("can't place ports by hand before there's a build to start from", () => {
    gasForm(gas);
    const options = screen.getAllByRole("option", { name: /^Each where it's placed \(build first/ });
    expect(options.map((o) => (o as HTMLOptionElement).disabled)).toEqual([true, true]); // burners, spy holes
  });

  it("sizes a port, starting from the size the build used", () => {
    const last = gasForm(gas, layout);
    fireEvent.change(screen.getByLabelText("Spy hole size"), { target: { value: "rect" } });
    expect(last()?.spy_holes).toEqual({ port: { width: "2.25 in", height: "2.5 in" } });
    fireEvent.change(screen.getByLabelText("Burner port size"), { target: { value: "round" } });
    expect(last()?.heat.gas?.burners?.port).toEqual({ diameter: "4.75 in" });
  });

  it("counts the spy holes, moves the flue, and leaves out what isn't set", () => {
    let last = gasForm(gas, layout);
    fireEvent.change(screen.getByLabelText("How many (blank: three)"), { target: { value: "5" } });
    expect(last()?.spy_holes).toEqual({ count: 5 });
    cleanup();
    last = gasForm(last() as KilnDocument, layout);
    fireEvent.change(screen.getByLabelText("How many (blank: three)"), { target: { value: "" } });
    expect(last()?.spy_holes).toBeUndefined();
    fireEvent.change(screen.getByLabelText("Flue across from the middle (blank: in the middle)"), {
      target: { value: "4" },
    });
    expect(last()?.draft?.flue_across).toBe("4 in");
  });

  it("moves placed burners, and spreads them back along a wall, as many as there were", () => {
    const places = [
      { wall: "front" as const, across: "-7 in", up: "5 in" },
      { wall: "front" as const, across: "7 in", up: "5 in" },
    ];
    // Placed by hand already, so they can stay placed before there's a build
    const last = live(setIn(gas, ["heat", "gas", "burners", "places"], places));
    set("Burner 2, across", "5");
    set("Burner 2, up", "");
    expect(last().heat.gas?.burners?.places?.[1]).toEqual({ wall: "front", across: "5 in", up: "" });
    set("Burner ports go", "spread");
    expect(last().heat.gas?.burners).toEqual({ wall: "front", count: 2 });
    set("Ports' centres above the floor (blank: one course up)", "6");
    expect(last().heat.gas?.burners?.up).toBe("6 in");
  });

  it("sizes a port round, then rectangular from that size, then as the engine chooses", () => {
    const last = live(gas, layout);
    set("Burner port size", "round");
    set("Burner port size: diameter", "5");
    expect(last().heat.gas?.burners?.port).toEqual({ diameter: "5 in" });
    set("Burner port size", "rect");
    expect(last().heat.gas?.burners?.port).toEqual({ width: "5 in", height: "5 in" });
    set("Burner port size: height", "6");
    set("Burner port size: width", "4");
    expect(last().heat.gas?.burners?.port).toEqual({ width: "4 in", height: "6 in" });
    set("Burner port size", "auto");
    expect(last().heat.gas?.burners?.port).toBeUndefined();
    expect(screen.queryByLabelText("Burner port size: width")).toBeNull();
  });

  it("keeps the shape chosen for a port while its size is blank", () => {
    const last = live(gas);
    set("Flue port size", "rect");
    expect(last().draft?.flue_port).toEqual({});
    set("Flue port size: width", "9");
    expect(last().draft?.flue_port).toEqual({ width: "9 in" });
    set("Flue port size", "round");
    expect(last().draft?.flue_port).toEqual({ diameter: "9 in" });
    set("Flue port size: diameter", "");
    expect(field("Flue port size: diameter").value).toBe("");
    expect(screen.queryByLabelText("Flue port size: width")).toBeNull();
  });

  it("moves placed spy holes, adds one where the last is, and puts them back up the door", () => {
    const placed = setIn(gas, ["spy_holes"], { places: [{ wall: "front", across: "0 in", up: "5 in" }] });
    const last = live(placed);
    set("Spy hole 1, wall", "back");
    set("Spy hole 1, across", "-2");
    expect(last().spy_holes?.places).toEqual([{ wall: "back", across: "-2 in", up: "5 in" }]);
    fireEvent.click(screen.getByRole("button", { name: "Add a spy hole" }));
    expect(last().spy_holes?.places).toHaveLength(2);
    expect(last().spy_holes?.places?.[1]).toEqual(last().spy_holes?.places?.[0]);
    set("Spy holes go", "door");
    expect(last().spy_holes).toEqual({ count: 2 });
  });

  it("starts a metric kiln's first spy hole halfway up the door, in millimetres", () => {
    const last = live({ ...electric, units: "metric", spy_holes: { places: [] } });
    fireEvent.click(screen.getByRole("button", { name: "Add a spy hole" }));
    expect(last().spy_holes?.places).toEqual([{ wall: "front", across: "0 mm", up: "305 mm" }]);
  });

  it("offers a gas kiln a quarter-brick spy hole and an electric one a round inch", () => {
    form(gas);
    expect(options("Spy hole size")[0]).toBe("A quarter brick, 2¼ × 2½ in");
    cleanup();
    form(electric);
    expect(options("Spy hole size")[0]).toBe("1 in round");
    expect(screen.queryByRole("group", { name: "Burner ports" })).toBeNull();
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

describe("shapes, fireboxes and chimneys", () => {
  it("keeps every part of a design it doesn't touch: a climbing kiln with two kinds of firebox", () => {
    const climbing: KilnDocument = {
      ...electric,
      chamber: {
        width: "63 in",
        depth: "41.33 in",
        height: "57.3 in",
        chambers: 10,
        slope: "18.4 deg",
        bend: "20 degree",
        on_ground: true,
      },
      roof: { type: "sprung_arch", rise: "20.7 in" },
      heat: {
        fire: {
          fuel: "wood",
          fireboxes: [
            { count: 10, position: "front", width: "9 in", length: "63 in" },
            { position: "under", width: "1 ft", length: "2 ft", grate: { width: "1 ft", length: "2 ft" } },
          ],
        },
        gas: { fuel: "natural_gas", supply: { type: "line", pressure: "8 inch_H2O" } },
      },
      draft: { type: "cross", flue_wall: "back", chimney: { height: "20 ft", inside: { width: "9 in", depth: "13.5 in" } } },
    };
    const last = live(climbing);
    set("Name", "Renamed");
    expect(last()).toEqual({ ...climbing, name: "Renamed" });
  });

  it("makes a round chamber, its depth following its diameter, and back to a box", () => {
    const last = live(electric);
    set("Chamber shape", "round");
    expect(screen.queryByLabelText("Depth")).toBeNull();
    set("Diameter", "30");
    expect(last().chamber).toMatchObject({ shape: "round", width: "30 in", depth: "30 in" });
    expect(screen.queryByRole("group", { name: "Chambers in a row" })).toBeNull();
    set("Chamber shape", "box");
    expect(last().chamber.shape).toBeUndefined();
  });

  it("turns a round chamber's rings a chosen way, only for round chambers", () => {
    const last = live(electric);
    expect(screen.queryByLabelText("Brick rings turned with")).toBeNull();
    set("Chamber shape", "round");
    // Left out, the engine cuts an electric kiln's rings and mortars the rest
    expect(field("Brick rings turned with").value).toBe("");
    set("Brick rings turned with", "featheredge");
    expect(last().chamber.rings).toBe("featheredge");
    set("Brick rings turned with", "");
    expect(last().chamber.rings).toBeUndefined();
    set("Brick rings turned with", "mortar");
    set("Chamber shape", "box");
    expect(last().chamber.rings).toBeUndefined();
  });

  it("chooses a teardrop or an oval plan, its sizes, and a dome's crown over it", () => {
    const last = live(electric);
    expect(screen.queryByLabelText("Sides' radius (left out: straight)")).toBeNull();
    set("Plan", "teardrop");
    expect(last().chamber.outline).toEqual({ shape: "teardrop" });
    set("Flat front wall's width (left out: round)", "15");
    set("Sides' radius (left out: straight)", "200");
    expect(last().chamber.outline).toEqual({ shape: "teardrop", front_width: "15 in", side_radius: "200 in" });
    set("Plan", "oval");
    // Round ends a quarter of the width, to edit
    const quarter = (toMm(last().chamber.width) ?? 0) / 4;
    expect(last().chamber.outline).toEqual({ shape: "oval", end_radius: fromMm(quarter, "us") });
    set("Round ends' radius", "5");
    expect(last().chamber.outline).toEqual({ shape: "oval", end_radius: "5 in" });
    expect(screen.queryByLabelText("Crown, behind the front wall (left out: the middle)")).toBeNull();
    set("Roof", "dome");
    set("Crown, behind the front wall (left out: the middle)", "20");
    expect(last().roof).toMatchObject({ type: "dome", crown_at: "20 in" });
    set("Plan", "rectangle");
    expect(last().chamber.outline).toBeUndefined();
    set("Plan", "teardrop");
    set("Chamber shape", "round");
    expect(last().chamber.outline).toBeUndefined();
    expect(screen.queryByLabelText("Plan")).toBeNull();
  });

  it("puts a round electric kiln's floor inside its walls, only for round electric kilns", () => {
    const label = "The floor slab sits inside the wall's lowest course, the walls running to the bottom (Paragon), not under the walls (Skutt)";
    const last = live(electric);
    expect(screen.queryByLabelText(label)).toBeNull();
    set("Chamber shape", "round");
    fireEvent.click(screen.getByLabelText(label));
    expect(last().chamber.floor_inside).toBe(true);
    fireEvent.click(screen.getByLabelText(label));
    expect(last().chamber.floor_inside).toBeUndefined();
    fireEvent.click(screen.getByLabelText(label));
    set("Chamber shape", "box");
    expect(last().chamber.floor_inside).toBeUndefined();
    expect(screen.queryByLabelText(label)).toBeNull();
  });

  it("adds and removes chambers in a row, with a slope and a floor on the ground", () => {
    const last = live(electric);
    expect(disabled("Remove a chamber")).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "Add a chamber" }));
    fireEvent.click(screen.getByRole("button", { name: "Add a chamber" }));
    expect(last().chamber.chambers).toBe(3);
    expect(screen.getByLabelText("Depth, of each chamber")).toBeTruthy();
    fireEvent.click(screen.getByRole("button", { name: "Remove a chamber" }));
    fireEvent.click(screen.getByRole("button", { name: "Remove a chamber" }));
    expect(last().chamber.chambers).toBeUndefined();
    set("Floor's slope, firing end to flue end (blank: level)", "11.3");
    expect(last().chamber.slope).toBe("11.3 degree");
    set("The run curves to the left by, in plan (blank: straight)", "45");
    expect(last().chamber.bend).toBe("45 degree");
    set("Chamber shape", "round");
    expect(last().chamber.bend).toBeUndefined();
    expect(screen.queryByLabelText("The run curves to the left by, in plan (blank: straight)")).toBeNull();
    set("Chamber shape", "box");
    fireEvent.click(screen.getByLabelText("The floor is on the ground (not raised on a stand)"));
    expect(last().chamber.on_ground).toBe(true);
    fireEvent.click(screen.getByLabelText("The floor is on the ground (not raised on a stand)"));
    expect(last().chamber.on_ground).toBeUndefined();
  });

  it("chooses an open top", () => {
    const last = live(electric);
    set("Roof", "open");
    expect(last().roof).toEqual({ type: "open" });
  });

  it("fires with wood in two fireboxes, with grates, inlets and stoke holes, and gas besides", () => {
    const last = live(electric);
    fireEvent.click(screen.getByLabelText("Fire with wood, coal or oil in fireboxes"));
    expect(last().heat.fire).toEqual({
      fuel: "wood",
      fireboxes: [{ position: "front", width: "22.5 in", length: "22.5 in" }],
    });
    expect(last().draft).toEqual({ type: "cross", flue_wall: "back" });
    expect(disabled("Remove firebox 1")).toBe(true);
    fireEvent.click(screen.getByRole("button", { name: "Add a firebox" }));
    set("Firebox 2, position", "back");
    set("Firebox 2, how many of this size", "2");
    set("Firebox 2, width", "14");
    set("Firebox 2, length", "30");
    set("Firebox 2, height", "20");
    fireEvent.click(screen.getByLabelText("Firebox 2 has a grate"));
    set("Firebox 2, grate width", "12");
    set("Firebox 2, grate length", "24");
    set("Firebox 2, gap between bars", "1");
    set("Firebox 2, ash pit depth", "9");
    set("Firebox 2, step from the grate up to the chamber floor (blank: level)", "10");
    set("Firebox 2, inlet flues into the chamber", "3");
    set("Firebox 2, inlet flue size", "round");
    set("Firebox 2, inlet flue size: diameter", "4");
    set("Firebox 2, stoke hole size", "rect");
    expect(last().heat.fire?.fireboxes[1]).toMatchObject({
      position: "back",
      count: 2,
      width: "14 in",
      length: "30 in",
      height: "20 in",
      grate: { width: "12 in", length: "24 in", gap: "1 in" },
      ash_pit: "9 in",
      step: "10 in",
      inlets: 3,
      inlet: { diameter: "4 in" },
    });
    set("Firebox 2, how many of this size", "1");
    set("Firebox 2, inlet flues into the chamber", "1");
    fireEvent.click(screen.getByLabelText("Firebox 2 has a grate"));
    expect(last().heat.fire?.fireboxes[1]?.count).toBeUndefined();
    expect(last().heat.fire?.fireboxes[1]?.grate).toBeUndefined();
    expect(last().heat.fire?.fireboxes[1]?.step).toBeUndefined();
    fireEvent.click(screen.getByRole("button", { name: "Remove firebox 1" }));
    expect(last().heat.fire?.fireboxes).toHaveLength(1);
    // The electric elements can go now the fire heats it; then the fire can't
    fireEvent.click(screen.getByLabelText("Heat with electric elements"));
    expect(last().heat.electric).toBeUndefined();
    expect(field("Fire with wood, coal or oil in fireboxes").disabled).toBe(true);
    fireEvent.click(screen.getByLabelText("Fire with gas"));
    expect(last().heat.gas).toBeDefined();
    fireEvent.click(screen.getByLabelText("Fire with wood, coal or oil in fireboxes"));
    expect(last().heat.fire).toBeUndefined();
  });

  it("burns oil with its burners and rate, and drops them for wood; a blower forces it", () => {
    const last = live({
      ...electric,
      heat: { fire: { fuel: "wood", fireboxes: [{ width: "1 ft", length: "2 ft" }] } },
      draft: { type: "cross" },
    });
    set("Fuel", "oil");
    set("Oil burners or drip units", "2");
    set("Each oil burner's flow at full fire", "2");
    expect(last().heat.fire).toMatchObject({ fuel: "oil", oil_burners: 2, oil_rate: "2 gallon/hour" });
    set("Oil burners or drip units", "");
    fireEvent.click(screen.getByLabelText("A blower drives the air (forced draft)"));
    expect(last().heat.fire?.forced).toBe(true);
    fireEvent.click(screen.getByLabelText("A blower drives the air (forced draft)"));
    set("Fuel", "coal");
    expect(last().heat.fire).toEqual({ fuel: "coal", fireboxes: [{ width: "1 ft", length: "2 ft" }] });
  });

  it("gives a chimney as built, round or rectangular, and lets the engine size it again", () => {
    const last = live({
      ...electric,
      heat: { fire: { fireboxes: [{ width: "1 ft", length: "2 ft" }] } },
      draft: { type: "down", flue_across: "3 in" },
    });
    fireEvent.click(screen.getByLabelText("Give the chimney as built (otherwise the engine sizes it)"));
    // Nothing is assumed: the height is left for the builder to give
    expect(last().draft?.chimney).toEqual({});
    expect(field("Chimney height, from the chamber floor (needed)").value).toBe("");
    set("Chimney height, from the chamber floor (needed)", "120");
    set("Chimney inside", "round");
    expect(field("Chimney inside diameter").value).toBe("");
    set("Chimney inside diameter", "10");
    expect(last().draft?.chimney).toEqual({ height: "120 in", inside: { diameter: "10 in" } });
    set("Chimney inside", "rect");
    expect(last().draft?.chimney?.inside).toEqual({ width: "10 in", depth: "10 in" });
    set("Chimney inside width", "9");
    set("Chimney inside depth", "13.5");
    expect(last().draft?.chimney?.inside).toEqual({ width: "9 in", depth: "13.5 in" });
    set("Chimney inside", "round");
    expect(last().draft?.chimney?.inside).toEqual({ diameter: "9 in" });
    set("Chimney inside", "auto");
    set("Chimney inside", "rect");
    expect(field("Chimney inside width").value).toBe("");
    set("Chimney inside", "auto");
    expect(last().draft?.chimney?.inside).toBeUndefined();
    set("Draft", "up");
    expect(last().draft?.flue_across).toBeUndefined();
    fireEvent.click(screen.getByLabelText("Give the chimney as built (otherwise the engine sizes it)"));
    expect(last().draft?.chimney).toBeUndefined();
  });

  it("fires natural gas from a line, propane from a line, and burners up through the floor", () => {
    const last = live({
      ...electric,
      heat: { gas: { supply: { type: "cylinders", count: 4 } } },
      draft: { type: "up" },
    });
    set("Gas", "natural_gas");
    // The pressure is the supply's, so it's left for the builder to give
    expect(last().heat.gas).toMatchObject({ fuel: "natural_gas", supply: { type: "line" } });
    expect(screen.queryByLabelText("Propane supply")).toBeNull();
    set("Gas pressure at the burners (needed: from the supply's regulator)", "7");
    expect(last().heat.gas?.supply).toEqual({ type: "line", pressure: "7 inch_H2O" });
    set("Gas", "propane");
    set("Propane supply", "line");
    expect(last().heat.gas?.supply).toEqual({ type: "line" });
    set("Burners fire through", "floor");
    expect(last().heat.gas?.burners?.wall).toBe("floor");
  });
});
