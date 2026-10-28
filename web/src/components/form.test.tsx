import type { Library } from "@kilndesigner/api-client";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { type KilnDocument, type Layout, setIn, splitQuantity, type WallFrame } from "../design";
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
