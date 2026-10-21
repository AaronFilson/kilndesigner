# kilndesigner

Design your kiln, get plans, make pots.

Describe the kiln you want in a short design file: what it fires, the size of the chamber, the
lining, the fuel or the power supply. Kilndesigner works out the heat loss, sizes the elements
or burners, builds a 3D model and draws plans you can build from. Every number comes with its
working and its source, so you can check it.

**Status:** early development. See [the plan](docs/planning/02-plan.md), the
[market survey](docs/planning/01-market-survey.md) and the [decision records](docs/adr/README.md).

## Try it

```
uv sync
uv run kilndesigner check examples/electric-front-loader.yaml
uv run kilndesigner build examples/electric-front-loader.yaml --out out/front-loader
uv run kilndesigner compare examples/pnw-hybrid-crossdraft.yaml examples/pnw-hybrid-crossdraft-budget.yaml
```

`build` writes `report.json` (every result with its working and sources), `plans.pdf` (drawings,
brick course plans, cut list, bill of materials, burner and propane checks, the working),
`sections.dxf`, and the 3D model as `kiln.step` and `kiln.glb`.

## What it does today

- **Heat loss** through layered walls with temperature-dependent conductivity, in the manner of
  ASTM C680, checked against published furnace-wall examples.
- **Electric elements** by Kanthal's method: wire, length, coil, surface load, circuits, the NEC
  continuous-load rule.
- **Gas burners and propane**: Ward's sizing, burner choice by pressure, cylinder and tank
  vaporization at your coldest firing day, chimney height and draft.
- **Hybrid kilns**: what a useful kWh costs from the elements and from propane at each
  temperature (combustion by Cantera), and when to switch over.
- **Masonry**: brick-by-brick course plans with staggered joints, arches, castables, a cut list
  and a priced bill of materials.
- **3D model and plans** from one set of parts, so they can't disagree.

## How it's built

- `core/`: the engine, a pure Python package (Pydantic, Pint, NumPy, SciPy, build123d, Typst).
- `cli/`: the `kilndesigner` command.
- Later: a FastAPI service, workers, and a React Three Fiber web app, self-hosted with Docker
  Compose or hosted.

## Safety

Kilndesigner gives engineering guidance. It does not replace a licensed electrician, a gas
fitter, or your local codes, and its electrical and gas results say so.

## License

MIT
