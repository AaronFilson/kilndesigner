// The design as choices: every part of a design file as a form, so a kiln can be designed
// without writing YAML. The form edits the JSON document; the API checks it (ADR 0006).
import type { Library } from "@kilndesigner/api-client";
import { type ReactNode, useId } from "react";

import {
  type Castable,
  type Electric,
  type Gas,
  joinQuantity,
  type KilnDocument,
  type Layer,
  setIn,
  splitQuantity,
  WALLS,
  type WallFace,
} from "../design";

const LENGTH = ["in", "mm", "ft", "cm"];
const TEMPERATURE = ["degF", "degC"];
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
  const chosen = units.includes(unit) ? unit : (units[0] ?? "");
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
        {units.length > 1 ? (
          <select
            aria-label={`${label}, unit`}
            value={chosen}
            onChange={(e) => number !== "" && onChange(joinQuantity(number, e.target.value))}
          >
            {units.map((u) => (
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
  onChange,
}: {
  label: string;
  value: T | undefined;
  options: [T, string][];
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
          <option key={String(v)} value={String(v)}>
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
  onChange,
}: {
  document: KilnDocument;
  library: Library;
  onChange: (document: KilnDocument) => void;
}) {
  const change: Change = (path, value) => onChange(setIn(doc, path, value));
  const roof = doc.roof ?? { type: "flat" };
  const loading = doc.loading ?? {};
  const electric = doc.heat.electric;
  const gas = doc.heat.gas;
  const mixes = (doc.castables ?? []).map((c) => ({ id: c.id, name: c.name }));

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
        {(["width", "depth", "height"] as const).map((k) => (
          <Quantity
            key={k}
            label={{ width: "Width", depth: "Depth", height: "Height" }[k]}
            value={doc.chamber[k]}
            units={LENGTH}
            onChange={(v) => change(["chamber", k], v)}
          />
        ))}
        <Choice
          label="Roof"
          value={roof.type}
          options={[
            ["flat", "Flat"],
            ["sprung_arch", "Sprung arch"],
          ]}
          onChange={(v) =>
            change(["roof"], v === "flat" ? { type: "flat" } : { type: "sprung_arch", rise: "3.75 in" })
          }
        />
        {roof.type === "sprung_arch" && (
          <Quantity
            label="Arch rise"
            value={roof.rise}
            units={LENGTH}
            onChange={(v) => change(["roof", "rise"], v)}
          />
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
            disabled={electric !== undefined && gas === undefined}
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
            disabled={gas !== undefined && electric === undefined}
            onChange={(e) => {
              let next = setIn(doc, ["heat", "gas"], e.target.checked ? DEFAULT_GAS : undefined);
              if (e.target.checked && !doc.draft) {
                next = setIn(next, ["draft"], { type: "cross", flue_wall: "back" });
              }
              onChange(next);
            }}
          />
          Fire with propane
        </label>
        {gas && (
          <>
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
              options={faceOptions}
              onChange={(v) => change(["heat", "gas", "burners", "wall"], v)}
            />
            <Choice
              label="Propane supply"
              value={gas.supply.type}
              options={[
                ["cylinders", "100 lb cylinders"],
                ["tank", "A tank"],
              ]}
              onChange={(v) =>
                change(
                  ["heat", "gas", "supply"],
                  v === "tank" ? { type: "tank", gallons: 250 } : { type: "cylinders", count: 4 },
                )
              }
            />
            {gas.supply.type === "cylinders" ? (
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
            <Choice
              label="Draft"
              value={doc.draft?.type ?? "cross"}
              options={[
                ["cross", "Cross-draft"],
                ["down", "Down-draft"],
                ["up", "Up-draft"],
              ]}
              onChange={(v) => change(["draft", "type"], v)}
            />
            {doc.draft?.type !== "up" && (
              <>
                <Choice
                  label="Flue wall"
                  value={doc.draft?.flue_wall ?? "back"}
                  options={faceOptions}
                  onChange={(v) => change(["draft", "flue_wall"], v)}
                />
                <Quantity
                  label="Flue wall to chimney"
                  value={doc.draft?.run_to_chimney ?? "9 in"}
                  units={LENGTH}
                  onChange={(v) => change(["draft", "run_to_chimney"], v)}
                />
              </>
            )}
          </>
        )}
      </Section>

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
