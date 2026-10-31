// The design as the forms edit it: the same JSON document the API stores (core/src/kilndesigner/
// model.py), with every physical value a string of a number and its unit ("22.5 in").

export type WallFace = "left" | "right" | "back" | "front";

export interface Layer {
  material: string;
  thickness: string;
}

/** A door in part of a wall (model.DoorOpening); left out, the whole wall is the door. */
export interface DoorOpening {
  width: string;
  height: string;
  across?: string;
  sill?: string;
  head?: "arch" | "lintel" | "flat";
  /** A flat head's rounded corners' radius (model.DoorOpening.corner). */
  corner?: string;
  ring?: string;
  each_chamber?: boolean;
}

export interface KilnDocument {
  schema?: number;
  name: string;
  units?: "us" | "metric";
  firing: {
    cone?: string;
    final_rate?: 60 | 100 | 150 | 600;
    top_temperature?: string;
    ware?: string;
    /** A firing time to solve the burners for (model.py Firing.target_time). */
    target_time?: string;
    setting?: Setting;
  };
  chamber: {
    shape?: "box" | "round";
    width: string;
    depth: string;
    height: string;
    chambers?: number;
    slope?: string;
    bend?: string;
    on_ground?: boolean;
    floor_inside?: boolean;
    rings?: RingMethod;
    outline?: PlanOutline;
  };
  roof?:
    | { type: "flat" }
    | { type: "open" }
    | {
        type: "sprung_arch";
        rise: string;
        ring?: number;
        ties?: "rigid" | "springs";
        spring_rate?: string;
      }
    | { type: "catenary_arch" }
    | { type: "dome"; rise: string; crown_at?: string };
  loading?: {
    /** "lid": a round electric top-loader, its flat roof the lid, hinged on its band. */
    type?: "door" | "car" | "lid";
    face?: WallFace;
    door?: "bricked" | "hinged";
    opening?: DoorOpening;
    car_hardware_cost?: string;
  };
  lining: {
    walls: Layer[];
    floor?: Layer[];
    roof?: Layer[];
    door?: Layer[];
    /** The tapered shapes arches and rings use (model.py Lining.shapes). */
    shapes?: "olsen" | "apg";
    /** Custom conical (tatami) bricks for arches and domes (model.py ConicalBrick). */
    conical?: {
      length?: string;
      wide?: string;
      narrow?: string;
      bore?: string;
      groove?: string;
      proportions?: "given" | "fig-4-6";
    };
  };
  shell?: { finish?: "painted" | "oxidised_steel" | "rolled_steel_sheet" };
  heat: { electric?: Electric; gas?: Gas; fire?: Fire };
  draft?: {
    type: "cross" | "down" | "up";
    flue_wall?: WallFace;
    run_to_chimney?: string;
    flue_port?: Port;
    flue_across?: string;
    chimney?: Chimney;
  };
  spy_holes?: { count?: number; port?: Port; places?: Place[] };
  site?: {
    ambient?: string;
    coldest_ambient?: string;
    electricity_price?: string;
    propane_price?: string;
    materials_budget?: string;
  };
  castables?: Castable[];
}

/** How a round wall's brick rings are turned (model.py Chamber.rings). */
export type RingMethod = "mortar" | "cut" | "featheredge" | "arch";

/** A box chamber's plan as a curve (model.py PlanOutline), filling its width and depth. */
export type PlanOutline =
  | {
      shape: "teardrop";
      front_width?: string;
      side_radius?: string;
      /** A neck at the back, the three given together (model.py PlanOutline). */
      neck_width?: string;
      neck_length?: string;
      neck_radius?: string;
    }
  | { shape: "oval"; end_radius: string };

type Teardrop = Extract<PlanOutline, { shape: "teardrop" }>;

/** A teardrop with its neck added or taken off. Added, it starts at Calimpong's printed neck
 *  (Olsen, Fig. 4-140; examples/olsen/conrad-teardrop.yaml): sizes to edit, not a rule. */
export function withNeck(
  outline: Teardrop,
  neck: boolean,
  units: "us" | "metric" | undefined,
): Teardrop {
  if (!neck) {
    return { ...outline, neck_width: undefined, neck_length: undefined, neck_radius: undefined };
  }
  const size = (inches: number) => fromMm(inches * 25.4, units);
  return { ...outline, neck_width: size(12), neck_length: size(19), neck_radius: size(32) };
}

export type PlanShape = "rectangle" | PlanOutline["shape"];

/** The chamber with its plan chosen: a rectangle drops the outline; an oval starts with round
 *  ends a quarter of the width in radius, a size to edit, not a rule. */
export function withPlan(
  chamber: KilnDocument["chamber"],
  plan: PlanShape,
  units: "us" | "metric" | undefined,
): KilnDocument["chamber"] {
  if (plan === "rectangle") return { ...chamber, outline: undefined };
  if (plan === "teardrop") return { ...chamber, outline: { shape: "teardrop" } };
  const width = toMm(chamber.width) ?? 0;
  return { ...chamber, outline: { shape: "oval", end_radius: fromMm(width / 4, units) } };
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

/** A hole's size: round, by its diameter, or a rectangle, by its width and height. */
export interface Port {
  diameter?: string;
  width?: string;
  height?: string;
}

/** Where a port goes: across from the middle of the wall (to the right, facing it from outside),
 * and up from the floor to its centre. */
export interface Place {
  wall: WallFace;
  across?: string;
  up: string;
}

export interface Burners {
  type?: "venturi" | "power";
  count?: number;
  model?: string;
  rating?: string;
  wall?: WallFace | "floor";
  port?: Port;
  up?: string;
  places?: Place[];
}

/** A flue's or chimney's inside: round, by its diameter, or a rectangle. */
export interface FlueSection {
  diameter?: string;
  width?: string;
  depth?: string;
}

export interface Chimney {
  /** Needed: the form leaves it blank for the builder to give. */
  height?: string;
  inside?: FlueSection;
  top?: FlueSection;
}

export type FireboxPosition = "front" | "back" | "left" | "right" | "under";

export interface Firebox {
  count?: number;
  position?: FireboxPosition;
  width: string;
  length: string;
  height?: string;
  grate?: { width: string; length: string; gap?: string };
  ash_pit?: string;
  step?: string;
  inlet?: Port;
  inlets?: number;
  stoke_hole?: Port;
  /** "corbel": the side walls' courses stepped in over its top (model.py Firebox.roof). */
  roof?: "flat" | "corbel";
  /** With a corbel roof, each course's step; left out, the most TMS 402 allows. */
  corbel_step?: string;
}

/** Wood, coal or oil burned in fireboxes (model.py Fire). */
export interface Fire {
  fuel?: "wood" | "coal" | "oil";
  /** 'smoke': wood to reduce a kiln the elements or burners heat (model.py Fire.purpose). */
  purpose?: "heat" | "smoke";
  fireboxes: Firebox[];
  forced?: boolean;
  oil_burners?: number;
  oil_rate?: string;
}

export interface Gas {
  fuel?: "propane" | "natural_gas";
  burners?: Burners;
  supply:
    | { type: "cylinders"; count: number; size?: "100 lb" }
    | { type: "tank"; gallons: number }
    | { type: "line"; pressure?: string };
  reduction?: boolean;
  firing_speed?: "fast" | "slow";
  /** A hybrid's burners lit from here with the elements still on (model.py Gas.on_from). */
  on_from?: string;
}

/** Kiln furniture Olsen weighs (p.33–35): the materials a setting can be made of. */
export const FURNITURE = ["mullite", "silicon-carbide", "cordierite"] as const;
export type FurnitureMaterial = (typeof FURNITURE)[number];

/** The shelves and posts in a full setting; the engine weighs them (furniture.py). */
export interface Setting {
  shelves: {
    length?: string;
    width?: string;
    thickness?: string;
    material: FurnitureMaterial;
    per_layer?: number;
    layers?: number;
  };
  posts?: {
    width?: string;
    depth?: string;
    height?: string;
    material: FurnitureMaterial;
    per_layer?: number;
  };
  ware_ratio?: number;
}

/** The setting a form starts from: one 12 × 24 × 1 in mullite shelf, no posts. */
export function freshSetting(): Setting {
  return {
    shelves: {
      length: "24 in",
      width: "12 in",
      thickness: "1 in",
      material: "mullite",
      per_layer: 1,
      layers: 1,
    },
  };
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

const MM_PER: Record<string, number> = { mm: 1, cm: 10, m: 1000, in: 25.4, ft: 304.8 };

/** A length as the design writes it ("6 in"), in millimetres; undefined if it isn't one. */
export function toMm(text: string | undefined): number | undefined {
  const [number, unit] = splitQuantity(text);
  const per = MM_PER[unit];
  return number === "" || per === undefined ? undefined : Number(number) * per;
}

/** Millimetres as the design's units write them: inches to the nearest ⅛, or whole mm. */
export function fromMm(mm: number, units: "us" | "metric" | undefined): string {
  if (units === "metric") return `${Math.round(mm)} mm`;
  return `${Math.round((mm / 25.4) * 8) / 8} in`;
}

/** A build's layout.json: each wall's frame and each port's place, in mm (hardware.layout). */
export interface WallFrame {
  origin: [number, number, number];
  normal: [number, number, number];
  right: [number, number, number];
  half_width: number;
  thickness: number;
  /** How high the wall's inside reaches, at points across it: [across, height]. */
  top: [number, number][];
}

export type PortKind = "burner" | "spy" | "flue";

export interface PortSpot {
  name: string;
  title: string;
  kind: PortKind;
  wall: WallFace;
  across: number;
  up: number;
  width: number;
  height: number;
  round: boolean;
  /** False when it didn't fit, so it wasn't cut (the report says why). */
  cut: boolean;
}

/** How a kiln drawn as shells (massing.py) lies: a round chamber, or a run of chambers that may
 * climb and bend. The walls' frames are the first chamber's; the run moves them. In mm and
 * degrees. */
export interface RunInfo {
  round: boolean;
  radius: number | null;
  chambers: number;
  depth: number;
  chamber_pitch: number;
  slope: number;
  bend: number;
  length: number;
  /** Chambers in a row laid out in brick (core run_parts.py) stand level, each floor this far
   * above the last: the run steps up its slope rather than tilting. Absent for shells. */
  step?: number;
}

export interface Layout {
  units: "us" | "metric";
  walls: Record<WallFace, WallFrame>;
  ports: PortSpot[];
  run?: RunInfo;
}

/** The ports of one kind as places the design can hold, from where the build put them. */
export function placesFrom(layout: Layout, kind: PortKind): Place[] {
  return layout.ports
    .filter((p) => p.kind === kind)
    .map((p) => ({
      wall: p.wall,
      across: fromMm(p.across, layout.units),
      up: fromMm(p.up, layout.units),
    }));
}

/** A port's size as the design writes it, from a size the build used. */
export function portFrom(spot: PortSpot, units: Layout["units"]): Port {
  return spot.round
    ? { diameter: fromMm(spot.width, units) }
    : { width: fromMm(spot.width, units), height: fromMm(spot.height, units) };
}

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
