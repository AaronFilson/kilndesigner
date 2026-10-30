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

## Run the app

```
docker compose up
```

Then open http://localhost:8080. The first start builds the images, which takes a few minutes.
It needs Docker Engine 25 or later.
Designs are kept in Postgres and built files in the `data` volume, so both survive a restart.
The app is reachable from this machine only, because there is no sign-in yet.

To work on the app, run Postgres and Valkey in Docker and the rest on your machine:

```
docker compose up -d postgres valkey
uv run kilndesigner-migrate
uv run kilndesigner-api
uv run arq kilndesigner_worker.main.WorkerSettings
npm install
npm run dev
```

Then open http://localhost:5173.

### On a small machine

On an older laptop the app can take more CPU and memory than the computer can spare. Copy
`small-machine.env` to `.env` and adjust it: the worker then runs one build at a time, with its
CPUs and memory capped. On a Mac with Colima, start Docker's VM with `scripts/colima.sh start`,
which starts it at the size set there and at a low priority, and stop it with
`scripts/colima.sh stop` when you're done: the VM gives its memory back to macOS only when it
stops.

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
- **Roofs**: flat, a sprung arch on skewbacks, a catenary arch from the floor (with the push at
  its feet) or a dome on all four walls.
- **Ports where you want them**: burner ports, spy holes and the flue sized and placed by hand,
  in the form or by dragging them on the 3D model, and checked to fit their walls.
- **3D model and plans** from one set of parts, so they can't disagree. The model can be shown in
  colour-blind safe, greyscale or blueprint colours, or colours you pick per material, and the
  app in a light or dark theme.

## How it's built

- `core/`: the engine, a pure Python package (Pydantic, Pint, NumPy, SciPy, build123d, Typst).
- `cli/`: the `kilndesigner` command.
- `api/`: the FastAPI service: designs, their versions and builds, in Postgres.
- `worker/`: the arq worker, which builds designs with the same code as the CLI.
- `web/`: the React app with a React Three Fiber viewer, and `packages/api-client`, its client
  generated from the API's OpenAPI document.
- `compose.yaml` runs them all; the hosted app (later) is the same compose file on one server.

## Safety

Kilndesigner gives engineering guidance. It does not replace a licensed electrician, a gas
fitter, or your local codes, and its electrical and gas results say so.

## License

MIT
