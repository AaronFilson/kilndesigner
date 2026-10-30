// The design as choices: every part of a design file as a form, so a kiln can be designed
// without writing YAML. The form edits the JSON document; the API checks it (ADR 0006).
import type { Library } from "@kilndesigner/api-client";
import { type ReactNode, useId, useState } from "react";

import {
  type Burners,
  type Castable,
  type Electric,
  type Fire,
  type Firebox,
  type FireboxPosition,
  fromMm,
  type Gas,
  joinQuantity,
  type KilnDocument,
  type Layer,
  type Layout,
  type Place,
  type Port,
  type PortKind,
  placesFrom,
  portFrom,
  setIn,
  splitQuantity,
  toMm,
  WALLS,
  type WallFace,
} from "../design";

const LENGTH = ["in", "mm", "ft", "cm"];
const TEMPERATURE = ["degF", "degC"];
const SPRING_RATE = ["lbf/in", "N/mm"];
const UNIT_LABELS: Record<string, string> = {
  degF: "°F",
  degC: "°C",
  "USD/kWh": "$/kWh",
  "USD/gallon": "$/gal",
  USD: "$",
};

type Path = (string | number)[];
type Change = (path: Path, value: unknown) => void;

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="field">
      <span>{label}</span>
      {children}
    </label>
  );
}

function Quantity({
  label,
  value,
  units,
  onChange,
}: {
  label: string;
  value: string | undefined;
  units: string[];
  onChange: (value: string | undefined) => void;
}) {
  const [number, unit] = splitQuantity(value);
  // A unit the field doesn't list, as a file written by hand may have, is shown and kept: picked
  // as the first listed, an edit would rewrite "1 m" as "1.2 in"
  const shown = unit !== "" && !units.includes(unit) ? [...units, unit] : units;
  const chosen = shown.includes(unit) ? unit : (shown[0] ?? "");
  const id = useId();
  return (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <span className="quantity">
        <input
          id={id}
          type="number"
          step="any"
          value={number}
          onChange={(e) =>
            onChange(e.target.value === "" ? undefined : joinQuantity(e.target.value, chosen))
          }
        />
        {shown.length > 1 ? (
          <select
            aria-label={`${label}, unit`}
            value={chosen}
            onChange={(e) => number !== "" && onChange(joinQuantity(number, e.target.value))}
          >
            {shown.map((u) => (
              <option key={u} value={u}>
                {UNIT_LABELS[u] ?? u}
              </option>
            ))}
          </select>
        ) : (
          <span className="unit">{UNIT_LABELS[chosen] ?? chosen}</span>
        )}
      </span>
    </div>
  );
}

function Choice<T extends string | number>({
  label,
  value,
  options,
  disabled = [],
  onChange,
}: {
  label: string;
  value: T | undefined;
  options: [T, string][];
  /** Options shown but not open to choose, for now. */
  disabled?: T[];
  onChange: (value: T) => void;
}) {
  return (
    <Field label={label}>
      <select
        value={value ?? ""}
        onChange={(e) => {
          const found = options.find(([v]) => String(v) === e.target.value);
          if (found) onChange(found[0]);
        }}
      >
        {value === undefined && <option value="">Choose…</option>}
        {options.map(([v, text]) => (
          <option key={String(v)} value={String(v)} disabled={disabled.includes(v)}>
            {text}
          </option>
        ))}
      </select>
    </Field>
  );
}

const FACE_WORDS: Record<WallFace, string> = {
  front: "Front",
  back: "Back",
  left: "Left",
  right: "Right",
};
const faceOptions = WALLS.map((w): [WallFace, string] => [w, FACE_WORDS[w]]);

const KIND_WORDS: Record<string, string> = {
  insulating_firebrick: "Insulating firebrick",
  dense_firebrick: "Hard firebrick",
  fibre_blanket: "Ceramic fibre",
  fibre_board: "Ceramic fibre board",
  insulating_castable: "Insulating castable",
  dense_castable: "Dense castable",
  backup_insulation: "Backup insulation",
  building_brick: "Building brick",
  stone: "Stone",
  diy_castable: "Your castables",
};

function Layers({
  title,
  layers,
  library,
  mixes,
  onChange,
}: {
  title: string;
  layers: Layer[];
  library: Library;
  mixes: { id: string; name: string }[];
  onChange: (layers: Layer[]) => void;
}) {
  const groups = new Map<string, { id: string; name: string }[]>();
  for (const m of library.materials) {
    const list = groups.get(m.kind) ?? [];
    list.push({ id: m.id, name: `${m.name} (to ${m.max_service})` });
    groups.set(m.kind, list);
  }
  if (mixes.length) groups.set("diy_castable", mixes);
  const set = (i: number, layer: Layer) => onChange(layers.map((l, j) => (j === i ? layer : l)));
  const move = (i: number, by: number) => {
    const next = [...layers];
    const [taken] = next.splice(i, 1);
    if (taken) next.splice(i + by, 0, taken);
    onChange(next);
  };
  return (
    <div className="layers" role="group" aria-label={title}>
      <ol>
        {layers.map((layer, i) => (
          <li key={i}>
            <Field label={`${title}, layer ${i + 1} material`}>
              <select
                value={layer.material}
                onChange={(e) => set(i, { ...layer, material: e.target.value })}
              >
                {[...groups].map(([kind, items]) => (
                  <optgroup key={kind} label={KIND_WORDS[kind] ?? kind}>
                    {items.map((m) => (
                      <option key={m.id} value={m.id}>
                        {m.name}
                      </option>
                    ))}
                  </optgroup>
                ))}
              </select>
            </Field>
            <Quantity
              label={`${title}, layer ${i + 1} thickness`}
              value={layer.thickness}
              units={LENGTH}
              onChange={(v) => set(i, { ...layer, thickness: v ?? "" })}
            />
            <span className="layer-tools">
              <button
                type="button"
                className="secondary"
                aria-label={`Move ${title.toLowerCase()} layer ${i + 1} in`}
                disabled={i === 0}
                onClick={() => move(i, -1)}
              >
                ↑
              </button>
              <button
                type="button"
                className="secondary"
                aria-label={`Move ${title.toLowerCase()} layer ${i + 1} out`}
                disabled={i === layers.length - 1}
                onClick={() => move(i, 1)}
              >
                ↓
              </button>
              <button
                type="button"
                className="secondary"
                aria-label={`Remove ${title.toLowerCase()} layer ${i + 1}`}
                disabled={layers.length === 1}
                onClick={() => onChange(layers.filter((_, j) => j !== i))}
              >
                Remove
              </button>
            </span>
          </li>
        ))}
      </ol>
      <button
        type="button"
        className="secondary"
        onClick={() =>
          onChange([...layers, { material: layers.at(-1)?.material ?? "ifb-k23", thickness: "1 in" }])
        }
      >
        Add a layer to the {title.toLowerCase()}
      </button>
    </div>
  );
}

function Section({ title, children }: { title: string; children: ReactNode }) {
  return (
    <fieldset className="form-section">
      <legend>{title}</legend>
      {children}
    </fieldset>
  );
}

function Castables({
  castables,
  library,
  onChange,
}: {
  castables: Castable[];
  library: Library;
  onChange: (castables: Castable[]) => void;
}) {
  const set = (i: number, c: Castable) => onChange(castables.map((x, j) => (j === i ? c : x)));
  const needsDensity = new Set(library.ingredients.filter((g) => g.needs_density).map((g) => g.id));
  const add = () => {
    let n = castables.length + 1;
    while (castables.some((c) => c.id === `my-castable-${n}`)) n += 1;
    onChange([
      ...castables,
      {
        id: `my-castable-${n}`,
        name: `My castable ${n}`,
        ingredients: [{ ingredient: library.ingredients[0]?.id ?? "", mass: "50 lb" }],
        water: "10 lb",
        foam: 50,
      },
    ]);
  };
  return (
    <Section title="Castables you mix">
      <p className="muted section-note">
        A recipe for one batch. The engine works out its densities, its conductivity, the batches
        the lining needs and how to fire it. Lining layers can then use it.
      </p>
      {castables.map((c, i) => (
        <div key={i} className="castable" role="group" aria-label={`Castable: ${c.name}`}>
          <Field label="Castable name">
            <input value={c.name} onChange={(e) => set(i, { ...c, name: e.target.value })} />
          </Field>
          <Field label="Its id, for the lining">
            <input
              value={c.id}
              pattern="[a-z0-9][a-z0-9-]*"
              onChange={(e) => set(i, { ...c, id: e.target.value })}
            />
          </Field>
          <ol className="ingredients">
            {c.ingredients.map((part, j) => {
              const setPart = (next: typeof part) =>
                set(i, { ...c, ingredients: c.ingredients.map((p, k) => (k === j ? next : p)) });
              return (
                <li key={j}>
                  <Field label={`${c.name}, ingredient ${j + 1}`}>
                    <select
                      value={part.ingredient}
                      onChange={(e) => setPart({ ingredient: e.target.value, mass: part.mass })}
                    >
                      {library.ingredients.map((g) => (
                        <option key={g.id} value={g.id}>
                          {g.name}
                        </option>
                      ))}
                    </select>
                  </Field>
                  <Quantity
                    label={`${c.name}, ingredient ${j + 1} mass`}
                    value={part.mass}
                    units={["lb", "kg"]}
                    onChange={(v) => setPart({ ...part, mass: v ?? "" })}
                  />
                  {needsDensity.has(part.ingredient) && (
                    <Quantity
                      label={`${c.name}, ingredient ${j + 1} true density (from its sheet)`}
                      value={part.density}
                      units={["g/cm**3"]}
                      onChange={(v) => setPart({ ...part, density: v })}
                    />
                  )}
                  <button
                    type="button"
                    className="secondary"
                    aria-label={`Remove ingredient ${j + 1} from ${c.name}`}
                    disabled={c.ingredients.length === 1}
                    onClick={() =>
                      set(i, { ...c, ingredients: c.ingredients.filter((_, k) => k !== j) })
                    }
                  >
                    Remove
                  </button>
                </li>
              );
            })}
          </ol>
          <button
            type="button"
            className="secondary"
            onClick={() =>
              set(i, {
                ...c,
                ingredients: [...c.ingredients, { ingredient: library.ingredients[0]?.id ?? "", mass: "1 lb" }],
              })
            }
          >
            Add an ingredient to {c.name}
          </button>
          <Quantity
            label={`${c.name}, water per batch`}
            value={c.water}
            units={["lb", "kg"]}
            onChange={(v) => set(i, { ...c, water: v ?? "" })}
          />
          <Field label={`${c.name}, air from foam (% of the cast volume)`}>
            <input
              type="number"
              min={0}
              max={85}
              value={c.foam ?? ""}
              onChange={(e) =>
                set(i, { ...c, foam: e.target.value === "" ? undefined : Number(e.target.value) })
              }
            />
          </Field>
          <Quantity
            label={`${c.name}, measured fired density (test pieces)`}
            value={c.measured?.fired_density}
            units={["lb/ft**3", "kg/m**3"]}
            onChange={(v) => set(i, { ...c, measured: { ...c.measured, fired_density: v } })}
          />
          <Field label={`${c.name}, measured linear shrinkage, %`}>
            <input
              type="number"
              step="any"
              value={c.measured?.linear_shrinkage ?? ""}
              onChange={(e) =>
                set(i, {
                  ...c,
                  measured: {
                    ...c.measured,
                    linear_shrinkage: e.target.value === "" ? undefined : Number(e.target.value),
                  },
                })
              }
            />
          </Field>
          <button
            type="button"
            className="secondary"
            onClick={() => onChange(castables.filter((_, k) => k !== i))}
          >
            Remove {c.name}
          </button>
        </div>
      ))}
      <button type="button" className="secondary" onClick={add}>
        Add a castable
      </button>
    </Section>
  );
}

type Shape = "auto" | "round" | "rect";

/** A port's size: as the engine chooses (`auto` says how), round, or a rectangle. Switching shape
 * starts from the size the last build used, when there is one. */
function PortSize({
  label,
  port,
  auto,
  seed,
  onChange,
}: {
  label: string;
  port: Port | undefined;
  auto: string;
  seed: Port | undefined;
  onChange: (port: Port | undefined) => void;
}) {
  const [picked, setPicked] = useState<Shape>("round");
  const shape: Shape =
    port === undefined
      ? "auto"
      : port.width !== undefined || port.height !== undefined
        ? "rect"
        : port.diameter !== undefined
          ? "round"
          : picked;
  const side = port?.diameter ?? port?.width ?? seed?.diameter ?? seed?.width;
  return (
    <>
      <Choice
        label={label}
        value={shape}
        options={[
          ["auto", auto],
          ["round", "Round"],
          ["rect", "Rectangular"],
        ]}
        onChange={(v) => {
          if (v !== "auto") setPicked(v);
          if (v === "auto") onChange(undefined);
          else if (v === "round") onChange({ diameter: side });
          else onChange({ width: side, height: port?.height ?? seed?.height ?? side });
        }}
      />
      {shape === "round" && (
        <Quantity
          label={`${label}: diameter`}
          value={port?.diameter}
          units={LENGTH}
          onChange={(v) => onChange({ diameter: v })}
        />
      )}
      {shape === "rect" && (
        <>
          <Quantity
            label={`${label}: width`}
            value={port?.width}
            units={LENGTH}
            onChange={(v) => onChange({ ...port, width: v })}
          />
          <Quantity
            label={`${label}: height`}
            value={port?.height}
            units={LENGTH}
            onChange={(v) => onChange({ ...port, height: v })}
          />
        </>
      )}
    </>
  );
}

/** Ports placed one by one: each one's wall, across from the middle and up from the floor. */
function Places({
  title,
  places,
  least = 1,
  fresh,
  onChange,
}: {
  title: string;
  places: Place[];
  /** How few there can be: a kiln needs a burner, but can do without spy holes. */
  least?: number;
  /** Where one added to an empty list goes; otherwise it starts where the last one is. */
  fresh?: Place;
  onChange: (places: Place[]) => void;
}) {
  const set = (i: number, place: Place) => onChange(places.map((p, j) => (j === i ? place : p)));
  const last = places.at(-1) ?? fresh;
  return (
    <div className="places" role="group" aria-label={`${title}s, where each goes`}>
      <ol>
        {places.map((p, i) => (
          <li key={i}>
            <Choice
              label={`${title} ${i + 1}, wall`}
              value={p.wall}
              options={faceOptions}
              onChange={(wall) => set(i, { ...p, wall })}
            />
            <Quantity
              label={`${title} ${i + 1}, across`}
              value={p.across}
              units={LENGTH}
              onChange={(v) => set(i, { ...p, across: v })}
            />
            <Quantity
              label={`${title} ${i + 1}, up`}
              value={p.up}
              units={LENGTH}
              onChange={(v) => set(i, { ...p, up: v ?? "" })}
            />
            <button
              type="button"
              className="secondary"
              aria-label={`Remove ${title.toLowerCase()} ${i + 1}`}
              disabled={places.length <= least}
              onClick={() => onChange(places.filter((_, j) => j !== i))}
            >
              Remove
            </button>
          </li>
        ))}
      </ol>
      {last && (
        <button type="button" className="secondary" onClick={() => onChange([...places, { ...last }])}>
          Add a {title.toLowerCase()}
        </button>
      )}
    </div>
  );
}

const SIDES: (WallFace | "floor" | undefined)[] = ["left", "right"];

/** A catenary is its own side walls: the door goes to the front, the burners there too, and the
 * flue to the back. Ports placed one by one are left where they are, for the check to point out. */
function offTheSides(doc: KilnDocument): KilnDocument {
  let next = doc;
  if (SIDES.includes(doc.loading?.face)) next = setIn(next, ["loading", "face"], "front");
  if (doc.heat.gas && SIDES.includes(doc.heat.gas.burners?.wall)) {
    next = setIn(next, ["heat", "gas", "burners", "wall"], "front");
  }
  if (doc.draft && SIDES.includes(doc.draft.flue_wall)) next = setIn(next, ["draft", "flue_wall"], "back");
  return next;
}

/** A part of the document with nothing left in it is left out. */
function tidy<T extends object>(value: T): T | undefined {
  return Object.values(value).some((v) => v !== undefined) ? value : undefined;
}

function Ports({
  doc,
  layout,
  onChange,
}: {
  doc: KilnDocument;
  layout: Layout | undefined;
  onChange: (document: KilnDocument) => void;
}) {
  const gas = doc.heat.gas;
  const burners = gas?.burners ?? {};
  const spy = doc.spy_holes ?? {};
  const draft = doc.draft;
  const built = (kind: PortKind) => layout?.ports.find((p) => p.kind === kind);
  const seed = (kind: PortKind) => {
    const spot = built(kind);
    return spot && layout ? portFrom(spot, layout.units) : undefined;
  };
  const setBurners = (next: Burners) => onChange(setIn(doc, ["heat", "gas", "burners"], next));
  const setSpy = (next: NonNullable<KilnDocument["spy_holes"]>) =>
    onChange(setIn(doc, ["spy_holes"], tidy(next)));
  const placedLater = "Each where it's placed (build first, or drag it in the 3D model)";
  // A spy hole added to none goes up the middle of the door's wall, halfway up
  const door = doc.loading?.face ?? "front";
  const halfway = fromMm((toMm(doc.chamber.height) ?? 0) / 2, doc.units);
  const freshSpy: Place = { wall: door, across: fromMm(0, doc.units), up: halfway };
  return (
    <Section title="Ports and spy holes">
      <p className="muted section-note">
        Across is from the middle of the wall, to your right as you stand outside facing it; up is
        from the floor to the hole's centre. Ports can also be dragged on the 3D model.
      </p>
      {gas && (
        <div className="subgroup" role="group" aria-label="Burner ports">
          <h3>Burner ports</h3>
          <Choice
            label="Burner ports go"
            value={burners.places ? "placed" : "spread"}
            options={[
              ["spread", "Spread evenly along one wall"],
              ["placed", built("burner") || burners.places ? "Each where it's placed" : placedLater],
            ]}
            disabled={built("burner") || burners.places ? [] : ["placed"]}
            onChange={(v) => {
              if (v === "placed" && layout) {
                setBurners({ ...burners, count: undefined, places: placesFrom(layout, "burner") });
              } else if (v === "spread" && burners.places) {
                setBurners({ ...burners, places: undefined, count: burners.places.length });
              }
            }}
          />
          {!burners.places && (
            <Quantity
              label="Ports' centres above the floor (blank: one course up)"
              value={burners.up}
              units={LENGTH}
              onChange={(v) => setBurners({ ...burners, up: v })}
            />
          )}
          <PortSize
            label="Burner port size"
            port={burners.port}
            auto="Sized for the burner"
            seed={seed("burner")}
            onChange={(port) => setBurners({ ...burners, port })}
          />
          {burners.places && (
            <Places
              title="Burner"
              places={burners.places}
              onChange={(places) => setBurners({ ...burners, places })}
            />
          )}
        </div>
      )}
      {(gas || doc.heat.fire) && draft && (
        <div className="subgroup" role="group" aria-label="Exit flue">
          <h3>Exit flue</h3>
          <PortSize
            label="Flue port size"
            port={draft.flue_port}
            auto="Olsen's 2.5 in² per ft³"
            seed={seed("flue")}
            onChange={(port) => onChange(setIn(doc, ["draft", "flue_port"], port))}
          />
          {draft.type !== "up" && (
            <Quantity
              label="Flue across from the middle (blank: in the middle)"
              value={draft.flue_across}
              units={LENGTH}
              onChange={(v) => onChange(setIn(doc, ["draft", "flue_across"], v))}
            />
          )}
        </div>
      )}
      <div className="subgroup" role="group" aria-label="Spy holes">
        <h3>Spy holes</h3>
        <Choice
          label="Spy holes go"
          value={spy.places ? "placed" : "door"}
          options={[
            ["door", "Up the door"],
            ["placed", layout || spy.places ? "Each where it's placed" : placedLater],
          ]}
          disabled={layout || spy.places ? [] : ["placed"]}
          onChange={(v) => {
            if (v === "placed" && layout) {
              setSpy({ ...spy, count: undefined, places: placesFrom(layout, "spy") });
            } else if (v === "door" && spy.places) {
              setSpy({ ...spy, places: undefined, count: spy.places.length });
            }
          }}
        />
        {!spy.places && (
          <Field label="How many (blank: three)">
            <input
              type="number"
              min={0}
              max={12}
              value={spy.count ?? ""}
              onChange={(e) =>
                setSpy({ ...spy, count: e.target.value === "" ? undefined : Number(e.target.value) })
              }
            />
          </Field>
        )}
        <PortSize
          label="Spy hole size"
          port={spy.port}
          auto={gas ? "A quarter brick, 2¼ × 2½ in" : "1 in round"}
          seed={seed("spy")}
          onChange={(port) => setSpy({ ...spy, port })}
        />
        {spy.places && (
          <Places
            title="Spy hole"
            places={spy.places}
            least={0}
            fresh={freshSpy}
            onChange={(places) => setSpy({ ...spy, places })}
          />
        )}
      </div>
    </Section>
  );
}

const POSITIONS: [FireboxPosition, string][] = [
  ...faceOptions,
  ["under", "Under the floor"],
];

/** A new firebox starts as wide as the chamber and as long as it is deep: no rule of thumb is
 * assumed, so the engine's checks say what to change. */
function freshFirebox(doc: KilnDocument, last: Firebox | undefined): Firebox {
  return last ? { ...last } : { position: "front", width: doc.chamber.width, length: doc.chamber.depth };
}

function FireSection({
  doc,
  disabled,
  onChange,
}: {
  doc: KilnDocument;
  disabled: boolean;
  onChange: (document: KilnDocument) => void;
}) {
  const fire = doc.heat.fire;
  const set = (next: Fire) => onChange(setIn(doc, ["heat", "fire"], next));
  const setBox = (i: number, box: Firebox) =>
    fire && set({ ...fire, fireboxes: fire.fireboxes.map((b, j) => (j === i ? box : b)) });
  return (
    <Section title="Fireboxes (wood, coal or oil)">
      <label className="check">
        <input
          type="checkbox"
          checked={fire !== undefined}
          disabled={disabled}
          onChange={(e) => {
            let next = setIn(
              doc,
              ["heat", "fire"],
              e.target.checked ? { fuel: "wood", fireboxes: [freshFirebox(doc, undefined)] } : undefined,
            );
            if (e.target.checked && !doc.draft) next = setIn(next, ["draft"], { type: "cross", flue_wall: "back" });
            onChange(next);
          }}
        />
        Fire with wood, coal or oil in fireboxes
      </label>
      {fire && (
        <>
          <Choice
            label="Fuel"
            value={fire.fuel ?? "wood"}
            options={[
              ["wood", "Wood"],
              ["coal", "Coal"],
              ["oil", "Oil"],
            ]}
            onChange={(v) =>
              set(
                v === "oil"
                  ? { ...fire, fuel: v }
                  : { ...fire, fuel: v, oil_burners: undefined, oil_rate: undefined },
              )
            }
          />
          <label className="check">
            <input
              type="checkbox"
              checked={fire.forced ?? false}
              onChange={(e) => set({ ...fire, forced: e.target.checked || undefined })}
            />
            A blower drives the air (forced draft)
          </label>
          {fire.fuel === "oil" && (
            <>
              <Field label="Oil burners or drip units">
                <input
                  type="number"
                  min={1}
                  value={fire.oil_burners ?? ""}
                  onChange={(e) =>
                    set({ ...fire, oil_burners: e.target.value ? Number(e.target.value) : undefined })
                  }
                />
              </Field>
              <Quantity
                label="Each oil burner's flow at full fire"
                value={fire.oil_rate}
                units={["gallon/hour", "L/h"]}
                onChange={(v) => set({ ...fire, oil_rate: v })}
              />
            </>
          )}
          <ol className="fireboxes">
            {fire.fireboxes.map((box, i) => {
              const name = `Firebox ${i + 1}`;
              return (
                <li key={i} role="group" aria-label={name}>
                  <Choice
                    label={`${name}, position`}
                    value={box.position ?? "front"}
                    options={POSITIONS}
                    onChange={(position) => setBox(i, { ...box, position })}
                  />
                  <Field label={`${name}, how many of this size`}>
                    <input
                      type="number"
                      min={1}
                      value={box.count ?? 1}
                      onChange={(e) =>
                        setBox(i, { ...box, count: Number(e.target.value) > 1 ? Number(e.target.value) : undefined })
                      }
                    />
                  </Field>
                  <Quantity
                    label={`${name}, width`}
                    value={box.width}
                    units={LENGTH}
                    onChange={(v) => setBox(i, { ...box, width: v ?? "" })}
                  />
                  <Quantity
                    label={`${name}, length`}
                    value={box.length}
                    units={LENGTH}
                    onChange={(v) => setBox(i, { ...box, length: v ?? "" })}
                  />
                  <Quantity
                    label={`${name}, height`}
                    value={box.height}
                    units={LENGTH}
                    onChange={(v) => setBox(i, { ...box, height: v })}
                  />
                  <label className="check">
                    <input
                      type="checkbox"
                      checked={box.grate !== undefined}
                      onChange={(e) =>
                        setBox(i, {
                          ...box,
                          grate: e.target.checked ? { width: box.width, length: box.length } : undefined,
                          ash_pit: e.target.checked ? box.ash_pit : undefined,
                        })
                      }
                    />
                    {name} has a grate
                  </label>
                  {box.grate && (
                    <>
                      <Quantity
                        label={`${name}, grate width`}
                        value={box.grate.width}
                        units={LENGTH}
                        onChange={(v) => setBox(i, { ...box, grate: { ...box.grate!, width: v ?? "" } })}
                      />
                      <Quantity
                        label={`${name}, grate length`}
                        value={box.grate.length}
                        units={LENGTH}
                        onChange={(v) => setBox(i, { ...box, grate: { ...box.grate!, length: v ?? "" } })}
                      />
                      <Quantity
                        label={`${name}, gap between bars`}
                        value={box.grate.gap}
                        units={LENGTH}
                        onChange={(v) => setBox(i, { ...box, grate: { ...box.grate!, gap: v } })}
                      />
                      <Quantity
                        label={`${name}, ash pit depth`}
                        value={box.ash_pit}
                        units={LENGTH}
                        onChange={(v) => setBox(i, { ...box, ash_pit: v })}
                      />
                    </>
                  )}
                  <Field label={`${name}, inlet flues into the chamber`}>
                    <input
                      type="number"
                      min={1}
                      value={box.inlets ?? 1}
                      onChange={(e) =>
                        setBox(i, { ...box, inlets: Number(e.target.value) > 1 ? Number(e.target.value) : undefined })
                      }
                    />
                  </Field>
                  <PortSize
                    label={`${name}, inlet flue size`}
                    port={box.inlet}
                    auto="Not given"
                    seed={undefined}
                    onChange={(inlet) => setBox(i, { ...box, inlet })}
                  />
                  <PortSize
                    label={`${name}, stoke hole size`}
                    port={box.stoke_hole}
                    auto="Not given"
                    seed={undefined}
                    onChange={(stoke_hole) => setBox(i, { ...box, stoke_hole })}
                  />
                  <button
                    type="button"
                    className="secondary"
                    aria-label={`Remove firebox ${i + 1}`}
                    disabled={fire.fireboxes.length === 1}
                    onClick={() => set({ ...fire, fireboxes: fire.fireboxes.filter((_, j) => j !== i) })}
                  >
                    Remove
                  </button>
                </li>
              );
            })}
          </ol>
          <button
            type="button"
            className="secondary"
            onClick={() =>
              set({ ...fire, fireboxes: [...fire.fireboxes, freshFirebox(doc, fire.fireboxes.at(-1))] })
            }
          >
            Add a firebox
          </button>
        </>
      )}
    </Section>
  );
}

function DraftSection({
  doc,
  onChange,
}: {
  doc: KilnDocument;
  onChange: (document: KilnDocument) => void;
}) {
  const change: Change = (path, value) => onChange(setIn(doc, path, value));
  const draft = doc.draft;
  const chimney = draft?.chimney;
  const inside = chimney?.inside;
  return (
    <Section title="Draft and chimney">
      <Choice
        label="Draft"
        value={draft?.type ?? "cross"}
        options={[
          ["cross", "Cross-draft"],
          ["down", "Down-draft"],
          ["up", "Up-draft"],
        ]}
        onChange={(v) =>
          change(["draft"], v === "up" ? { ...draft, type: v, flue_across: undefined } : { ...draft, type: v })
        }
      />
      {draft?.type !== "up" && (
        <>
          <Choice
            label="Flue wall"
            value={draft?.flue_wall ?? "back"}
            options={faceOptions}
            onChange={(v) => change(["draft", "flue_wall"], v)}
          />
          <Quantity
            label="Flue wall to chimney"
            value={draft?.run_to_chimney ?? "9 in"}
            units={LENGTH}
            onChange={(v) => change(["draft", "run_to_chimney"], v)}
          />
        </>
      )}
      <label className="check">
        <input
          type="checkbox"
          checked={chimney !== undefined}
          onChange={(e) =>
            change(
              ["draft", "chimney"],
              e.target.checked ? { height: doc.chamber.height } : undefined,
            )
          }
        />
        Give the chimney as built (otherwise the engine sizes it)
      </label>
      {chimney && (
        <>
          <Quantity
            label="Chimney height, from the chamber floor"
            value={chimney.height}
            units={LENGTH}
            onChange={(v) => change(["draft", "chimney", "height"], v ?? "")}
          />
          <Choice
            label="Chimney inside"
            value={inside === undefined ? "auto" : inside.diameter !== undefined ? "round" : "rect"}
            options={[
              ["auto", "The size the engine works out"],
              ["round", "Round"],
              ["rect", "Rectangular"],
            ]}
            onChange={(v) =>
              change(
                ["draft", "chimney", "inside"],
                v === "auto"
                  ? undefined
                  : v === "round"
                    ? { diameter: inside?.width ?? inside?.diameter ?? "9 in" }
                    : { width: inside?.diameter ?? "9 in", depth: inside?.diameter ?? "9 in" },
              )
            }
          />
          {inside?.diameter !== undefined && (
            <Quantity
              label="Chimney inside diameter"
              value={inside.diameter}
              units={LENGTH}
              onChange={(v) => change(["draft", "chimney", "inside"], { diameter: v })}
            />
          )}
          {inside && inside.diameter === undefined && (
            <>
              <Quantity
                label="Chimney inside width"
                value={inside.width}
                units={LENGTH}
                onChange={(v) => change(["draft", "chimney", "inside", "width"], v)}
              />
              <Quantity
                label="Chimney inside depth"
                value={inside.depth}
                units={LENGTH}
                onChange={(v) => change(["draft", "chimney", "inside", "depth"], v)}
              />
            </>
          )}
        </>
      )}
    </Section>
  );
}

const DEFAULT_ELECTRIC: Electric = {
  supply: { voltage: "240 V", phase: 1, breaker: "60 A" },
  alloy: "kanthal-a1",
  walls: ["left", "right", "back"],
};
const DEFAULT_GAS: Gas = {
  burners: { type: "venturi", wall: "front" },
  supply: { type: "cylinders", count: 4 },
  reduction: true,
};

export function DesignForm({
  document: doc,
  library,
  layout,
  onChange,
}: {
  document: KilnDocument;
  library: Library;
  /** Where the last build put the ports, to start placing them by hand from. */
  layout?: Layout;
  onChange: (document: KilnDocument) => void;
}) {
  const change: Change = (path, value) => onChange(setIn(doc, path, value));
  const roof = doc.roof ?? { type: "flat" };
  const loading = doc.loading ?? {};
  const electric = doc.heat.electric;
  const gas = doc.heat.gas;
  const fire = doc.heat.fire;
  const mixes = (doc.castables ?? []).map((c) => ({ id: c.id, name: c.name }));
  const round = doc.chamber.shape === "round";
  const chambers = doc.chamber.chambers ?? 1;
  // The last heat source left can't be turned off: a kiln needs one
  const sources = [electric, gas, fire].filter((h) => h !== undefined).length;

  return (
    <form className="design-form" aria-label="Design" onSubmit={(e) => e.preventDefault()}>
      <Section title="The kiln">
        <Field label="Name">
          <input value={doc.name} onChange={(e) => change(["name"], e.target.value)} />
        </Field>
        <Choice
          label="Show results in"
          value={doc.units ?? "us"}
          options={[
            ["us", "US units (in, °F, BTU)"],
            ["metric", "Metric"],
          ]}
          onChange={(v) => change(["units"], v)}
        />
        <Choice
          label="Fire to cone"
          value={doc.firing.cone}
          options={library.cones.map((c): [string, string] => [c, c])}
          onChange={(v) => {
            // Cones 15 and up are tabulated at one rate each, so move the rate to one that exists.
            const rates = library.cone_rates[v] ?? [60];
            const rate = doc.firing.final_rate ?? 60;
            const firing = { ...doc.firing, cone: v };
            onChange(
              setIn(doc, ["firing"], rates.includes(rate) ? firing : { ...firing, final_rate: rates[0] }),
            );
          }}
        />
        {doc.firing.cone !== undefined && (
          <Choice
            label="Final heating rate"
            value={doc.firing.final_rate ?? 60}
            options={(library.cone_rates[doc.firing.cone] ?? [60]).map(
              (r): [number, string] => [r, `${r} °C/h`],
            )}
            onChange={(v) => change(["firing", "final_rate"], v)}
          />
        )}
        <Quantity
          label="Or a top temperature"
          value={doc.firing.top_temperature}
          units={TEMPERATURE}
          onChange={(v) => change(["firing", "top_temperature"], v)}
        />
      </Section>

      <Section title="Chamber (inside)">
        <Choice
          label="Chamber shape"
          value={round ? "round" : "box"}
          options={[
            ["box", "A box"],
            ["round", "Round (a bottle or folk kiln)"],
          ]}
          onChange={(v) =>
            change(
              ["chamber"],
              v === "round"
                ? { ...doc.chamber, shape: v, depth: doc.chamber.width, chambers: undefined }
                : { ...doc.chamber, shape: undefined },
            )
          }
        />
        {(round ? (["width", "height"] as const) : (["width", "depth", "height"] as const)).map((k) => (
          <Quantity
            key={k}
            label={
              {
                width: round
                  ? "Diameter"
                  : roof.type === "catenary_arch"
                    ? "Width, at the floor"
                    : "Width",
                depth: chambers > 1 ? "Depth, of each chamber" : "Depth",
                height:
                  roof.type === "catenary_arch"
                    ? "Height, to the crown"
                    : roof.type === "flat"
                      ? "Height"
                      : "Height, to the springline",
              }[k]
            }
            value={doc.chamber[k]}
            units={LENGTH}
            onChange={(v) =>
              change(["chamber"], {
                ...doc.chamber,
                [k]: v,
                // A round chamber's depth is its diameter too
                ...(round && k === "width" ? { depth: v } : {}),
              })
            }
          />
        ))}
        {!round && (
          <div className="field" role="group" aria-label="Chambers in a row">
            <span>Chambers in a row, front to back (a climbing or tandem kiln)</span>
            <span className="layer-tools">
              <button
                type="button"
                className="secondary"
                aria-label="Remove a chamber"
                disabled={chambers === 1}
                onClick={() => change(["chamber", "chambers"], chambers - 1 > 1 ? chambers - 1 : undefined)}
              >
                −
              </button>
              <output aria-label="Chambers">{chambers}</output>
              <button
                type="button"
                className="secondary"
                aria-label="Add a chamber"
                onClick={() => change(["chamber", "chambers"], chambers + 1)}
              >
                +
              </button>
            </span>
          </div>
        )}
        <Quantity
          label="Floor's slope, firing end to flue end (blank: level)"
          value={doc.chamber.slope}
          units={["degree"]}
          onChange={(v) => change(["chamber", "slope"], v)}
        />
        <label className="check">
          <input
            type="checkbox"
            checked={doc.chamber.on_ground ?? false}
            onChange={(e) => change(["chamber", "on_ground"], e.target.checked || undefined)}
          />
          The floor is on the ground (not raised on a stand)
        </label>
        <Choice
          label="Roof"
          value={roof.type}
          options={[
            ["flat", "Flat"],
            ["sprung_arch", "Sprung arch"],
            ["catenary_arch", "Catenary arch, from the floor"],
            ["dome", "Dome"],
            ["open", "Open top, covered with shards each firing"],
          ]}
          onChange={(v) => {
            // A rise carries over between a sprung arch and a dome
            const rise = "rise" in roof ? roof.rise : "3.75 in";
            let next = setIn(
              doc,
              ["roof"],
              v === "flat" || v === "catenary_arch" || v === "open" ? { type: v } : { type: v, rise },
            );
            if (v === "catenary_arch") next = offTheSides(next);
            onChange(next);
          }}
        />
        {(roof.type === "sprung_arch" || roof.type === "dome") && (
          <Quantity
            label={roof.type === "dome" ? "Dome rise, at the centre" : "Arch rise"}
            value={roof.rise}
            units={LENGTH}
            onChange={(v) => change(["roof", "rise"], v)}
          />
        )}
        {roof.type === "sprung_arch" && (
          <Choice
            label="Tie rods"
            value={roof.ties ?? "rigid"}
            options={[
              ["rigid", "Nutted tight to the frame"],
              ["springs", "Through a spring at each end"],
            ]}
            onChange={(v) =>
              change(
                ["roof"],
                v === "springs"
                  ? { ...roof, ties: v, spring_rate: roof.spring_rate ?? "283 lbf/in" }
                  : // Back to rigid: drop only the springs, keeping the rest (ring, buttressed)
                    setIn(setIn(roof, ["ties"], undefined), ["spring_rate"], undefined),
              )
            }
          />
        )}
        {roof.type === "sprung_arch" && roof.ties === "springs" && (
          <Quantity
            label="Each spring's rate, from its listing"
            value={roof.spring_rate}
            units={SPRING_RATE}
            onChange={(v) => change(["roof", "spring_rate"], v)}
          />
        )}
        {roof.type === "catenary_arch" && (
          <p className="muted section-note">
            The arch springs from the floor and is the side walls too, so the door, the burners and
            the flue go in the front or back wall (choosing it moves them there). It's fired with
            gas: elements in its curved walls aren't designed here.
          </p>
        )}
        {roof.type === "dome" && (
          <p className="muted section-note">
            A dome on all four walls: a sphere through the chamber's top corners, rising to the
            rise at its centre.
          </p>
        )}
      </Section>

      <Section title="Loading">
        <Choice
          label="Ware goes in through"
          value={loading.type ?? "door"}
          options={[
            ["door", "A door"],
            ["car", "A car that rolls out"],
          ]}
          onChange={(v) => change(["loading", "type"], v)}
        />
        <Choice
          label={loading.type === "car" ? "The car's end" : "The door's wall"}
          value={loading.face ?? "front"}
          options={faceOptions}
          onChange={(v) => change(["loading", "face"], v)}
        />
        {loading.type !== "car" && (
          <Choice
            label="Door"
            value={loading.door ?? (gas ? "bricked" : "hinged")}
            options={[
              ["bricked", "Bricked up for each firing"],
              ["hinged", "Hinged"],
            ]}
            onChange={(v) => change(["loading", "door"], v)}
          />
        )}
        {loading.type === "car" && (
          <Quantity
            label="Car hardware cost"
            value={loading.car_hardware_cost}
            units={["USD"]}
            onChange={(v) => change(["loading", "car_hardware_cost"], v)}
          />
        )}
      </Section>

      <Castables
        castables={doc.castables ?? []}
        library={library}
        onChange={(v) => change(["castables"], v.length ? v : undefined)}
      />

      <Section title="Lining, hot face first">
        <Layers
          title="Walls"
          layers={doc.lining.walls}
          library={library}
          mixes={mixes}
          onChange={(v) => change(["lining", "walls"], v)}
        />
        {(["floor", "roof", "door"] as const).map((face) => {
          const own = doc.lining[face];
          const title = { floor: "Floor", roof: "Roof", door: "Door" }[face];
          return (
            <div key={face}>
              <label className="check">
                <input
                  type="checkbox"
                  checked={own === undefined}
                  onChange={(e) =>
                    change(["lining", face], e.target.checked ? undefined : [...doc.lining.walls])
                  }
                />
                {title}: the same layers as the walls
              </label>
              {own && (
                <Layers
                  title={title}
                  layers={own}
                  library={library}
                  mixes={mixes}
                  onChange={(v) => change(["lining", face], v)}
                />
              )}
            </div>
          );
        })}
        <Choice
          label="Outside finish"
          value={doc.shell?.finish ?? "oxidised_steel"}
          options={[
            ["painted", "Painted"],
            ["oxidised_steel", "Oxidised steel"],
            ["rolled_steel_sheet", "Rolled steel sheet"],
          ]}
          onChange={(v) => change(["shell", "finish"], v)}
        />
      </Section>

      <Section title="Electric elements">
        <label className="check">
          <input
            type="checkbox"
            checked={electric !== undefined}
            disabled={electric !== undefined && sources === 1}
            onChange={(e) =>
              change(["heat", "electric"], e.target.checked ? DEFAULT_ELECTRIC : undefined)
            }
          />
          Heat with electric elements
        </label>
        {electric && (
          <>
            <Choice
              label="Supply voltage"
              value={splitQuantity(electric.supply.voltage)[0]}
              options={["120", "208", "240", "480"].map((v): [string, string] => [v, `${v} V`])}
              onChange={(v) => change(["heat", "electric", "supply", "voltage"], `${v} V`)}
            />
            <Choice
              label="Phase"
              value={electric.supply.phase ?? 1}
              options={[
                [1, "Single phase"],
                [3, "Three phase"],
              ]}
              onChange={(v) => change(["heat", "electric", "supply", "phase"], v)}
            />
            <Quantity
              label="Breaker"
              value={electric.supply.breaker}
              units={["A"]}
              onChange={(v) => change(["heat", "electric", "supply", "breaker"], v)}
            />
            <Choice
              label="Element alloy"
              value={electric.alloy ?? "kanthal-a1"}
              options={library.alloys.map((a): [string, string] => [a.id, a.name])}
              onChange={(v) => change(["heat", "electric", "alloy"], v)}
            />
            <div className="field" role="group" aria-label="Walls with elements">
              <span>Walls with elements</span>
              <span className="checks">
                {WALLS.map((w) => {
                  const walls = electric.walls ?? ["left", "right", "back"];
                  return (
                    <label key={w} className="check">
                      <input
                        type="checkbox"
                        checked={walls.includes(w)}
                        disabled={walls.includes(w) && walls.length === 1}
                        onChange={(e) =>
                          change(
                            ["heat", "electric", "walls"],
                            e.target.checked ? [...walls, w] : walls.filter((x) => x !== w),
                          )
                        }
                      />
                      {FACE_WORDS[w]}
                    </label>
                  );
                })}
              </span>
            </div>
            {gas && (
              <Quantity
                label="Elements hand over to gas above"
                value={electric.off_above}
                units={TEMPERATURE}
                onChange={(v) => change(["heat", "electric", "off_above"], v)}
              />
            )}
          </>
        )}
      </Section>

      <Section title="Gas burners">
        <label className="check">
          <input
            type="checkbox"
            checked={gas !== undefined}
            disabled={gas !== undefined && sources === 1}
            onChange={(e) => {
              let next = setIn(doc, ["heat", "gas"], e.target.checked ? DEFAULT_GAS : undefined);
              if (e.target.checked && !doc.draft) {
                next = setIn(next, ["draft"], { type: "cross", flue_wall: "back" });
              }
              onChange(next);
            }}
          />
          Fire with gas
        </label>
        {gas && (
          <>
            <Choice
              label="Gas"
              value={gas.fuel ?? "propane"}
              options={[
                ["propane", "Propane"],
                ["natural_gas", "Natural gas, from a line"],
              ]}
              onChange={(v) =>
                change(
                  ["heat", "gas"],
                  v === "natural_gas"
                    ? { ...gas, fuel: v, supply: { type: "line", pressure: "8 inch_H2O" } }
                    : { ...gas, fuel: undefined, supply: { type: "cylinders", count: 4 } },
                )
              }
            />
            <Choice
              label="Burner type"
              value={gas.burners?.type ?? "venturi"}
              options={[
                ["venturi", "Venturi (natural draft, no power)"],
                ["power", "Power (blower)"],
              ]}
              onChange={(v) =>
                change(["heat", "gas", "burners"], { ...gas.burners, type: v, model: undefined })
              }
            />
            <Choice
              label="Burner model"
              value={gas.burners?.model ?? ""}
              options={[
                ["", "Chosen for you"],
                ...library.burners
                  .filter((b) => b.name.includes(gas.burners?.type === "power" ? "power" : "venturi"))
                  .map((b): [string, string] => [b.id, b.name]),
              ]}
              onChange={(v) => change(["heat", "gas", "burners", "model"], v || undefined)}
            />
            {gas.burners?.places ? (
              <p className="muted section-note">
                {gas.burners.places.length} burners, one for each port placed under Ports and spy
                holes.
              </p>
            ) : (
              <>
                <Field label="Number of burners (blank: chosen for you)">
                  <input
                    type="number"
                    min={1}
                    value={gas.burners?.count ?? ""}
                    onChange={(e) =>
                      change(
                        ["heat", "gas", "burners", "count"],
                        e.target.value ? Number(e.target.value) : undefined,
                      )
                    }
                  />
                </Field>
                <Choice
                  label="Burners fire through"
                  value={gas.burners?.wall ?? "front"}
                  options={[...faceOptions, ["floor", "The floor (an updraft)"]]}
                  onChange={(v) => change(["heat", "gas", "burners", "wall"], v)}
                />
              </>
            )}
            {gas.fuel !== "natural_gas" && (
              <Choice
                label="Propane supply"
                value={gas.supply.type}
                options={[
                  ["cylinders", "100 lb cylinders"],
                  ["tank", "A tank"],
                  ["line", "A line from a large tank"],
                ]}
                onChange={(v) =>
                  change(
                    ["heat", "gas", "supply"],
                    v === "tank"
                      ? { type: "tank", gallons: 250 }
                      : v === "line"
                        ? { type: "line", pressure: "2 psi" }
                        : { type: "cylinders", count: 4 },
                  )
                }
              />
            )}
            {gas.supply.type === "line" ? (
              <Quantity
                label="Gas pressure at the burners"
                value={gas.supply.pressure}
                units={["inch_H2O", "psi"]}
                onChange={(v) => change(["heat", "gas", "supply", "pressure"], v)}
              />
            ) : gas.supply.type === "cylinders" ? (
              <Field label="Cylinders">
                <input
                  type="number"
                  min={1}
                  value={gas.supply.count}
                  onChange={(e) =>
                    change(["heat", "gas", "supply", "count"], Number(e.target.value) || 1)
                  }
                />
              </Field>
            ) : (
              <Choice
                label="Tank size"
                value={gas.supply.gallons}
                options={[120, 150, 250, 325, 500, 1000].map((g): [number, string] => [g, `${g} gal`])}
                onChange={(v) => change(["heat", "gas", "supply", "gallons"], v)}
              />
            )}
            <label className="check">
              <input
                type="checkbox"
                checked={gas.reduction ?? true}
                onChange={(e) => change(["heat", "gas", "reduction"], e.target.checked)}
              />
              Fired in reduction
            </label>
            <Choice
              label="Burners sized for"
              value={gas.firing_speed ?? "fast"}
              options={[
                ["fast", "A fast firing (about 6–7 hours)"],
                ["slow", "A slow firing (about 14–18 hours)"],
              ]}
              onChange={(v) => change(["heat", "gas", "firing_speed"], v)}
            />
          </>
        )}
      </Section>

      <FireSection
        doc={doc}
        disabled={fire !== undefined && sources === 1}
        onChange={onChange}
      />

      {(gas || fire) && <DraftSection doc={doc} onChange={onChange} />}

      <Ports doc={doc} layout={layout} onChange={onChange} />

      <Section title="Site and costs">
        <Quantity
          label="Air around the kiln"
          value={doc.site?.ambient ?? "70 degF"}
          units={TEMPERATURE}
          onChange={(v) => change(["site", "ambient"], v)}
        />
        <Quantity
          label="Coldest firing day"
          value={doc.site?.coldest_ambient}
          units={TEMPERATURE}
          onChange={(v) => change(["site", "coldest_ambient"], v)}
        />
        <Quantity
          label="Electricity price"
          value={doc.site?.electricity_price}
          units={["USD/kWh"]}
          onChange={(v) => change(["site", "electricity_price"], v)}
        />
        <Quantity
          label="Propane price"
          value={doc.site?.propane_price}
          units={["USD/gallon"]}
          onChange={(v) => change(["site", "propane_price"], v)}
        />
        <Quantity
          label="Materials budget"
          value={doc.site?.materials_budget}
          units={["USD"]}
          onChange={(v) => change(["site", "materials_budget"], v)}
        />
      </Section>
    </form>
  );
}
