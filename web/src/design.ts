// The design as the forms edit it: the same JSON document the API stores (core/src/kilndesigner/
// model.py), with every physical value a string of a number and its unit ("22.5 in").

export type WallFace = "left" | "right" | "back" | "front";

export interface Layer {
  material: string;
  thickness: string;
}

export interface KilnDocument {
  schema?: number;
  name: string;
  units?: "us" | "metric";
  firing: { cone?: string; final_rate?: 60 | 100 | 150 | 600; top_temperature?: string };
  chamber: { width: string; depth: string; height: string };
  roof?: { type: "flat" } | { type: "sprung_arch"; rise: string };
  loading?: {
    type?: "door" | "car";
    face?: WallFace;
    door?: "bricked" | "hinged";
    car_hardware_cost?: string;
  };
  lining: { walls: Layer[]; floor?: Layer[]; roof?: Layer[]; door?: Layer[] };
  shell?: { finish?: "painted" | "oxidised_steel" | "rolled_steel_sheet" };
  heat: { electric?: Electric; gas?: Gas };
  draft?: { type: "cross" | "down" | "up"; flue_wall?: WallFace; run_to_chimney?: string };
  site?: {
    ambient?: string;
    coldest_ambient?: string;
    electricity_price?: string;
    propane_price?: string;
    materials_budget?: string;
  };
  castables?: Castable[];
}

export interface MixPart {
  ingredient: string;
  mass: string;
  density?: string;
  price?: string;
}

/** A castable the builder mixes: one batch's recipe (castable.py). */
export interface Castable {
  id: string;
  name: string;
  ingredients: MixPart[];
  water: string;
  foam?: number;
  measured?: { fired_density?: string; linear_shrinkage?: number; fired_to?: string };
}

export interface Electric {
  supply: { voltage: string; phase?: 1 | 3; breaker: string };
  alloy?: string;
  walls?: WallFace[];
  elements?: number;
  power?: string;
  off_above?: string;
}

export interface Gas {
  fuel?: "propane";
  burners?: { type?: "venturi" | "power"; count?: number; model?: string; wall?: WallFace };
  supply: { type: "cylinders"; count: number; size?: "100 lb" } | { type: "tank"; gallons: number };
  reduction?: boolean;
  firing_speed?: "fast" | "slow";
}

/** "22.5 in" → [22.5, "in"]; the API writes temperatures as "70 °F". */
export function splitQuantity(text: string | undefined): [string, string] {
  const match = /^\s*([-+]?[\d.]+(?:[eE][-+]?\d+)?)\s*(.*?)\s*$/.exec(text ?? "");
  if (!match) return ["", ""];
  return [match[1] ?? "", normaliseUnit(match[2] ?? "")];
}

const UNIT_ALIASES: Record<string, string> = {
  "°F": "degF",
  "°C": "degC",
  "$ / kWh": "USD/kWh",
  "$ / gal": "USD/gallon",
  $: "USD",
};

export function normaliseUnit(unit: string): string {
  return UNIT_ALIASES[unit] ?? unit;
}

export function joinQuantity(value: string, unit: string): string {
  return `${value} ${unit}`;
}

export const WALLS: WallFace[] = ["front", "back", "left", "right"];

/** A copy of the document with `path` set to `value`; `undefined` removes the key. */
export function setIn<T extends object>(doc: T, path: (string | number)[], value: unknown): T {
  const [head, ...rest] = path;
  if (head === undefined) return value as T;
  const source = doc as unknown as Record<string | number, unknown>;
  const copy = (Array.isArray(doc) ? [...doc] : { ...doc }) as unknown as Record<
    string | number,
    unknown
  >;
  if (rest.length === 0) {
    if (value === undefined) delete copy[head];
    else copy[head] = value;
  } else {
    const child = source[head];
    copy[head] = setIn(
      (child && typeof child === "object" ? child : typeof rest[0] === "number" ? [] : {}) as object,
      rest,
      value,
    );
  }
  return copy as T;
}
