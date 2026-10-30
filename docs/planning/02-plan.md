# Plan: Product, Architecture, Resume Story

_Drafted 2026-10-21. The [market survey](01-market-survey.md) informs the positioning; the
decisions here are recorded as ADRs in [`docs/adr`](../adr/README.md) with the status
**proposed** until the first milestone ships against them._

## Product positioning

**"Describe the kiln you want; get a kiln you can build."**

A potter or a studio enters a spec: what it fires (stoneware, porcelain, glass, raku, wood
ash), the top temperature or cone, the size of the stacking space, the fuel and the budget. Kilndesigner
returns:

- a parametric 3D model of the kiln, with walls, arch, door, flue and burner or element ports;
- the engineering behind it: heat loss, shell temperature, the energy to fire, heat-up time
  on the chosen elements or burners, and the draft;
- the plans: dimensioned drawings, a brick-by-brick course plan, a cut list and a bill of
  materials, as a PDF and DXF.

Ceramic kilns come first, starting with electric. Gas, wood and glass follow, and they share
one engine.

### What the survey changes

The [survey](01-market-survey.md) found no kiln design software for potters. Builders work from
Olsen's *The Kiln Book*, Kanthal's PDFs, Ward Burner's BTU table, forums and their own
spreadsheets. Refractory makers' heat-flow tools are good but steady-state, tied to their own
products and aimed at industry. So:

- **A "parametric kiln book."** The well-known rules (Olsen's proportions, Ward's BTU ranges,
  Kanthal's surface loads) are encoded as cited defaults the user can resize, with a diff of what
  changed. Every default names its source in the working.
- **Industry-standard methods.** Shell heat loss follows ASTM C680, the method behind Morgan Heat
  Flow, Alkegen, HWI and NAIMA 3E Plus, so results can be compared with theirs.
- **Heat stored in the walls is the headline.** For a kiln fired once a week, the questions are
  "how long to cone 10" and "how much gas or how many kWh per firing." The steady-state tools
  can't answer them. The transient model moves up to sit right after the hosted app.
- **An open, vendor-neutral materials library**, with every value cited and overridable.
- **Brick-level output** (course plans, arch and skewback bricks, cut lists): no tool does it.
- **Firing logs from controllers, later.** Import from jbruce12000/kiln-controller (open source)
  first, then exports from Genesis and KilnLink, to fit the model to real firings.
- **Likely users who pay:** schools, community studios and small makers building gas and wood
  kilns. Hobby electric builders will mostly use the free local tool.
- **Prior art:** RepKiln (OpenSCAD bricks plus a Python 1D transient model) is the closest
  project. It has no license, so it's a reference only, not code to reuse. CalebBell/ht (MIT) is
  a candidate dependency for convection and radiation correlations.

### Decisions
- **2026-10-21 · Hosting:** one EC2 instance running the self-hosted compose file, as Glazecalc
  does. Hosted and self-hosted are the same thing. See
  [ADR 0011](../adr/0011-hosted-on-one-ec2-instance.md).
- **2026-10-21 · Business model:** everything is free and MIT-licensed, including the hosted
  app. No billing in the plan.
- **2026-10-21 · First kiln:** an electric front-loader box: a rectangular brick chamber with a
  door and elements in grooves. Its element circuit is reused for the hybrid kiln in M3.
- **2026-10-21 · Gas and the hybrid move up to M3**, right after plans, because both first users
  need gas (see "The first two users").
- **2026-10-21 · Audience:** US first, metric supported. The defaults are inches, °F, cones, BTU
  and AWG, with US brick sizes and suppliers. Metric is one setting away and works everywhere.
- **2026-10-21 · M4 scope:** designs are edited three ways: forms generated from the design
  file's JSON Schema, a YAML tab, and hand-built forms per kiln type, starting with the electric
  front-loader. Self-hosted has one local user with no sign-in; OIDC waits for M5. The first slice
  is save → build (as an arq job) → view the 3D model and the report. The JavaScript workspace
  uses npm workspaces.
- **2026-10-22 · The bar for M4 is a kiln you can design in the app.** After using the first
  slice, the author's verdict: not a useful product. The model was lining blocks (an arch that
  stops short of the walls' outside, no door, ports or flue), drawings were only downloads, the
  viewer only spun, and designing meant editing YAML. M4 is done when it passes the four points
  under its milestone below, worked in that order; the hosted app (M5) waits for it.
- **2026-10-23 · DIY castables join M4 (point 5).** The author's notes (`castables/*.txt`) are
  chat transcripts, so none of their numbers are used; [castables.md](../research/castables.md)
  sources the data. A mix's conductivity comes from its fired density by a power law fitted to
  nine Morgan K and JM firebricks (8.9 % rms, up to 21 % for a brick left out of the fit).
  Maxwell–Eucken and Landauer models were tried and fit worse. Mixes outside 480–1250 kg/m³
  are refused.

## The first two users

The plan is shaped around two real kilns. Each is a design that must actually get built, and
each is a validation case for the engine.

### 1. The author's kiln (Pacific Northwest)

- **Type:** cross-draft, cone 10, about 30 to 40 cu ft of stacking space.
- **First estimate (2026-10-21):** a chamber about 4 ft tall, 5 to 6 ft long and 28 in. wide
  inside, with 8 in. walls. **The site limits the outside width** (about 44 in. plus the frame at
  8 in. walls), so the inside width follows from the wall build-up the tool picks. The tool
  decides the final sizes.
- **Inputs for costs:** electricity at about $0.12/kWh, propane at about $3.50/gal, firing down to
  about 20°F outside, and **under $5,000 for materials**, which makes a plain door the likely
  choice unless a car fits the budget.
- **Roof:** a cast dome arch of castable refractory, not brick.
- **Loading:** a car or a plain door. **This is open and depends on the budget**, so the tool has
  to price both and compare them.
- **Hybrid firing:** 240 V at 48 A (about 11.5 kW) of elements for the slow, sensitive early
  stages under a digital controller, then propane for the rest. The Pacific Northwest has some of
  the cheapest electricity anywhere, so the elements also cut fuel cost.
- **Propane:** four 100 lb cylinders in parallel.

What it asks of the engine:
- **The switch-over point.** At what temperature should the elements hand over to gas? That
  depends on the cost per kWh against the cost per gallon, and on how much the 11.5 kW can still
  add as heat loss rises. The answer is a chart: cost and time per firing against switch-over
  temperature.
- **The propane supply check.** Cylinders can only vaporise propane so fast, and the rate drops
  as the cylinders get colder and emptier. Four 100 lb cylinders must keep up with the burners'
  peak demand on a cold day, or the kiln stalls near the top. The tool checks this against the
  manufacturer's vaporisation data and says how many cylinders, or what tank, the burners need.
- **Elements in a gas kiln.** Reduction attacks the protective oxide on the wire. The design
  states the element alloy (for example Kanthal APM against A1), how the elements are protected
  or switched off during reduction, and how often they'll need replacing.
- **Castable dome.** Dome geometry, castable volume and weight, anchors, formwork, and the dry-out
  and first-firing schedule. Masonry has to cover castables as well as brick.
- **Car or door.** Both designs, with their bills of materials and costs side by side.

### 2. A client: off-grid, gas and/or wood

- **Type:** gas, wood, or both. **No mains power at the site.**
- What it asks of the engine:
  - **Natural-draft (venturi) burners**, not blowers, unless solar power is planned;
  - **the chimney does all the work**, so the draft calculation must be solid;
  - **wood firebox design** and the switch between wood and propane;
  - **a fuel-logistics estimate:** cords of wood and gallons of propane per firing;
  - **manual control:** cones, pyrometer and damper settings, with no electronic controller to rely on.
- The deliverable is **plans a client can build from**, so the plans must stand up on their own,
  with the working printed.

## Three ways to run it, one codebase

| Mode | For | How it runs | Storage | Jobs | Sign-in |
|---|---|---|---|---|---|
| **CLI and library** | Tinkerers, CI, tests, notebooks | `uvx kilndesigner build kiln.yaml --out plans/` | Design files (YAML) on disk | In process | None |
| **Self-hosted** | A studio, a maker space, anyone offline | `docker compose up`: the same images as hosted | Postgres, DuckDB files, a local folder for exports | Valkey + arq worker | One local user, or OIDC if configured |
| **Hosted** | Everyone else | The same compose file on one EC2 instance | Postgres on the instance (backed up to S3), Parquet and exports on S3 | Valkey + arq workers | Google and GitHub (OIDC with PKCE) |

The CLI is what makes the project easy to test: every result the app shows can be produced from a
YAML file on the command line and compared with a golden file. The hosted app proves the
production side: accounts, multiple tenants, background jobs, observability and deploys. See
[ADR 0003](../adr/0003-one-codebase-three-ways-to-run.md).

## Architecture

```
kilndesigner/                 uv workspace
  core/                       kilndesigner (PyPI): the engine; no web, no database
    model/                    Pydantic: Kiln, WallAssembly, Layer, Material, Arch, Door,
                              ElementCircuit, Burner, Flue, Firebox, FiringSchedule
    units/                    Pint registry; cone tables; °C/°F/K
    geometry/                 build123d: chamber, walls, arches, ports → STEP/STL/glTF/DXF
    thermal/                  steady-state layered walls; 1D transient finite volume; later scikit-fem
    electric/                 element design: wire, length, coil, surface load, circuits
    combustion/               burner sizing, air/fuel, flue and chimney draft (later Cantera)
    masonry/                  brick coursing, arch bricks, cut list, counts
    plans/                    Typst templates → PDF; DXF sheets
    materials/                the materials library, from manufacturers' data sheets
  cli/                        Typer: build, check, simulate, export
  api/                        FastAPI; OpenAPI contract; SQLAlchemy 2 + Alembic
  worker/                     arq tasks: simulate, build geometry, render plans
  mcp/                        FastMCP server over the engine
  web/                        React 19 + Vite + TanStack + React Three Fiber
  packages/api-client/        generated TypeScript client
  notebooks/                  marimo: validation against published references
  infra/                      AWS CDK (Python)
  docs/                       planning, ADRs, runbooks
```

### Key decisions (ADRs)

| ADR | Decision |
|---|---|
| [0001](../adr/0001-record-architecture-decisions.md) | Record architecture decisions |
| [0002](../adr/0002-a-pure-engine-package.md) | The engine is a pure Python package; every surface sits on top of it |
| [0003](../adr/0003-one-codebase-three-ways-to-run.md) | One codebase, three ways to run: CLI, self-hosted, hosted |
| [0004](../adr/0004-units-with-pint.md) | Quantities carry units (Pint); the engine works in SI |
| [0005](../adr/0005-geometry-in-python-served-as-gltf.md) | Geometry is built only in Python (build123d) and served as glTF |
| [0006](../adr/0006-designs-as-versioned-documents-in-postgres.md) | Designs are versioned JSON documents in Postgres |
| [0007](../adr/0007-simulation-results-in-parquet-and-duckdb.md) | Simulation results are Parquet files, queried with DuckDB |
| [0008](../adr/0008-background-jobs-with-arq.md) | Slow work runs as jobs on Valkey and arq, or in process for the CLI |
| [0009](../adr/0009-physics-checked-against-published-references.md) | The physics is checked against published references, in CI |
| [0010](../adr/0010-react-and-react-three-fiber.md) | The web app is React with React Three Fiber |
| [0011](../adr/0011-hosted-on-one-ec2-instance.md) | The hosted app is the self-hosted compose file on one EC2 instance |
| [0012](../adr/0012-combustion-with-cantera.md) | Combustion is modelled with Cantera, not a rule of thumb (proposed) |
| [0013](../adr/0013-checks-as-evaluable-sheets.md) | Every warning and error is a sheet of formulas you can edit (proposed) |
| [0014](../adr/0014-built-kilns-are-the-reference.md) | Built kilns are the reference: a rule that fails one is the rule's fault (proposed) |

## The engineering, by kiln type

Each module returns its result *and* the working: inputs, formulas, intermediate values and the
references used. The plans print the working, so a builder can check it.

- **Walls and heat loss (all kilns).** Layered walls (hard brick, insulating firebrick, fibre
  board, blanket, the shell) as thermal resistances in series, with temperature-dependent
  conductivity from data sheets. The shell loses heat by natural convection and radiation, so the
  shell temperature is solved iteratively. The output is heat loss at temperature, shell
  temperature (a touch-safety check) and a cost-of-materials trade-off by layer thickness.
- **Firing (all kilns).** A 1D transient finite-volume model per wall: the energy stored in the
  walls and the ware plus what is lost, along a firing schedule. This shows why insulating firebrick
  heats faster than dense brick, and how long a schedule takes on the available power.
- **Electric.** From the energy needed, the supply (voltage, phase, breaker) and the alloy
  (Kanthal A1, APM and similar, from data sheets): the wire gauge, length and resistance at temperature,
  the coil diameter and pitch, the surface load against the maker's limits, the circuits and
  the switching. The groove layout is drawn into the walls.
- **Gas.** The burner rating (BTU/hr or kW) from the firing energy, the number of burners and where
  they go, then the flue port, damper and chimney from the rules of thumb in the standard texts,
  checked by a draft calculation. Down-draft, up-draft and cross-draft layouts. Power and
  natural-draft burners. **The fuel supply:** propane vaporisation from cylinders or a tank, at the
  coldest expected temperature, against peak demand.
- **Hybrid.** Elements for the early stages and gas for the rest: the switch-over temperature
  that minimises cost or time, the element alloy and how it survives reduction, and the
  controller hand-off.
- **Cost (all kilns).** Materials from the bill of materials, at user-editable prices, and the
  running cost per firing from local electricity, propane and wood prices. Two designs can be
  compared side by side (for example a car against a door).
- **Wood.** Firebox and grate area, the throat, the chamber and the chimney in proportion; ash pit and
  stoke-hole layout. Anagama, train and Bourry box as templates.
- **Glass.** Fusing, slumping and annealing: top-element layouts, even temperature across the
  shelf, and annealing schedules by glass thickness and COE.
- **Masonry and castables (all kilns).** Brick coursing with staggered joints, sprung and catenary
  arches (rise, skewbacks, arch and wedge bricks), cast domes (castable volume and weight,
  anchors, formwork, dry-out schedule), doors and cars, a cut list and counts with a waste
  allowance.

## Milestones

| # | Milestone | Done when | Resume-worthy engineering |
|---|---|---|---|
| **M0** | **Foundations** | uv workspace, ruff, pyright strict, pytest, CI, ADRs, the design-file schema | A typed Python monorepo with strict CI from the first commit |
| **M1** | **Electric kiln engine** | `kilndesigner build` turns a YAML spec into an electric front-loader box kiln: geometry (STEP, glTF), steady-state heat loss, element design, and a JSON report | Parametric B-rep CAD, unit-safe numerical code, property-based tests (Hypothesis), golden files |
| **M2** | **Plans** | A dimensioned PDF and a DXF, the brick course plan, a cut list and a bill of materials | Typst document generation, 2D projection from 3D, deterministic output |
| **M3** | **Gas and hybrid: the author's kiln** | A cross-draft with a cast dome, as a car kiln and as a door kiln, with costs side by side; burner sizing; the propane supply check; the electric-to-gas switch-over chart; plans to build from | Combustion and fuel-supply models, optimisation (SciPy), cost modelling, comparing designs |
| **M4** | **A kiln you can design in the app** | `docker compose up`, then: (1) the model is a kiln you could build: the arch on skewbacks over the full walls, the steel frame, a door or a car, burner and flue ports, the chimney and spy holes, coloured by material; (2) dimensioned drawings, course plans, the bill of materials and the cut list shown in the page (files still downloadable); (3) a viewer with front, side, top and section views, a cutaway and named parts; (4) a design started from a kiln type and edited with choices, not YAML (YAML stays as a tab); (5) castables you mix yourself: a batch recipe in the design gives its wet, dried and fired densities, a conductivity checked against published firebricks, what the temperatures in the wall do to it (kyanite, quartz, burnout), the batches and ingredients the lining needs, and the first firing (water, organics, heat, a dry-out schedule), refusing mixes outside the checked range. Each point has browser tests | FastAPI + SQLAlchemy 2 + Alembic, a job queue, an OpenAPI-generated client, React Three Fiber, Playwright |
| **M5** | **Hosted app** | Accounts, design sharing by link, deploys with approval to AWS, tracing and metrics | Multi-tenant Postgres (row-level security), OIDC with PKCE, CDK in Python, keyless deploys with rollback, OpenTelemetry |
| **M6** | **Firing simulation** | Transient heat-up along a schedule, results in Parquet, charts and a wall heatmap in the viewer | Finite-volume numerics, DuckDB analytics, GPU shaders for the heatmap |
| **M7** | **Wood and off-grid: the client's kiln** | A firebox, natural-draft burners, the chimney and draft, fuel per firing, and plans for a site with no mains power | Natural-draft modelling, multi-fuel designs, plans that stand alone |
| **M8** | **AI assistants** | An MCP server: "design a cone 10 gas kiln for 12 cubic feet, under $3,000" | MCP in Python, with tools that return the working |
| **M9** | **Real firings** | Import firing logs from the author's controller, compare them with the simulation, and fit wall properties to them | Parameter estimation (SciPy), data ingestion, model-versus-measurement reports |
| Later | **Glass** | Templates, top-element layouts, annealing schedules | |
| Later | **Drag to stretch, with grid snap** | In the viewer, drag a handle on a wall, the floor, the arch or a port to resize it, as in a CAD tool. Sizes snap to a grid you set (whole bricks by default, or inches or millimetres), the handle shows the size as you drag, and letting go changes the same field the form edits and rebuilds the kiln. A size outside the checked range is refused with the reason (ADR 0009) | Direct manipulation in React Three Fiber, snapping and constraints, a fast rebuild |

### Status (2026-10-21, overnight)

- **M0, M1, M2 and M3 are built**, on the stacked branches `m0` → `m1` → `m2` → `m3`, with 127
  tests passing (published worked examples, Hypothesis invariants, golden reports).
- The first results for the author's kiln are in [docs/kilns](../kilns/pnw-hybrid-crossdraft.md).
- Validation lives in pytest (`core/tests`) rather than marimo notebooks so far; ADR 0009's
  notebooks are still to do, as readable companions to those tests.
- Not done in M3: skewbacks and the steel frame, a sourced car-hardware price, and the fuel and
  electricity used per firing (which needs M6).

### Status (2026-10-28)

- M4 is in progress on branch `m4`. A science review (`docs/reviews/2026-10-28-science-review.md`)
  set the work in `10-28-26.md`; its status section says what's done.
- Done: the breaker limit (NEC 422.11(E)), burner pressures read from their curves, HarbisonWalker's
  arch rules enforced, doors refused in a sprung arch's springing walls, domes over doors checked
  as sliced arches, flat roofs checked as jack arches, gas kilns over 60 ft³ refused, and the 3D
  canvas under test (web 99.6 % of lines, Python 99.7 % branch, both enforced in CI).
- New research: `domes-over-doors.md`, `flat-roofs.md`, `door-headers.md`.
- Open: door-header statics (refractory allowables not found), steel for domes, the buttress
  position (S5), validation notebooks, and the fixes waiting on the research files left on the
  Windows machine.
- Performance on small machines: `docs/reviews/2026-10-28-performance-review.md`.

### Status (2026-10-29)

- **M4 is merged to `main`** (PR #1). Each of its five points has a Playwright test in
  `web/e2e/designs.spec.ts`: the buildable model; drawings, course plans, bill and cut list in
  the page; the views, cutaway and named parts; a design started from a kind of kiln and edited
  with choices; and castables you mix, with the refusal outside the checked range.
- Since 28 October: Olsen's *The Kiln Book* is the ground truth (ADR 0014,
  [10-29-26.md](10-29-26.md)). 53 of his kilns are examples in `examples/olsen/` and all build
  with no error. Gas sizing follows his rules (Rule 1, the 1:1 flue, Rule 5 chimneys, natural
  gas, altitude, no 60 ft³ limit), fireboxes for wood, coal and oil are in (`fire.py`), round,
  sloped and chambered kilns compute, and floors on the ground lose heat to the soil. Every check
  is an editable sheet of formulas (ADR 0013).
- The research files once left on the Windows machine are now in the repo (`castables.md`,
  `castables-minerals.md`, `thermal-properties.md`, `electrical-supply.md`,
  `structure-and-draft.md`, `cones.md`), so the review work that waited on them is unblocked.
- Carried over from M4 (the science review's backlog, see [10-28-26.md](10-28-26.md)):
  - Fix 2 (organics burning off in dry-out) and Fix 4 (propane supply in the cold, regulator
    droop);
  - S5 (the buttress at the ring's outer corner), S14, and steel sized for domes;
  - door headers: the method is in `door-headers.md`, refractory allowables aren't found;
  - most of 3a, 3c and 3d, the dead code in 3f, and the validation notebooks (3e);
  - the web form doesn't edit fireboxes, chimneys, round chambers, open tops or floors on the
    ground (YAML does); chamber kilns' arches along the draft aren't drawn;
  - Olsen's Table 1-12 wall: the engine's 445 BTU/ft²·h against his 360, recorded, not tested.

### What's next

The plan put M5 (hosted) after M4, but neither first user needs accounts yet, and what they do
need is still open. In order:

1. **Close the science backlog that's now unblocked:** Fix 4 first (the author's four 100 lb
   cylinders on a 20 °F day is a stall-or-not answer they need), then Fix 2, then 3d. These are
   correctness on numbers that are already shown to users.
2. **The author's kiln, end to end.** Rebuild `pnw-hybrid-crossdraft` (dome, door, car) on the
   Olsen-era engine and read its report against the book; settle the door header or move the
   door, since it's the dome over a door that blocks it.
3. **M6, firing simulation**, pulled ahead of M5: the switch-over chart and fuel and electricity
   per firing (both M3 leftovers) need the transient model, and the 1D finite volume is half of
   the thermal work already planned.
4. **The client's kiln (M7)** is now cheaper than it was: fireboxes, natural draft and Rule 5
   exist. It needs the client's answers (open question 3) before it can start; ask now.
5. **M5, hosted**, once one of the two kilns has plans someone builds from.

M1 to M3 make a usable open-source tool and design the author's kiln. M4 and M5 are the
full-stack story. M7 moves earlier if the client's timeline needs it, since the CLI can produce
the client's plans before the app exists.

## Quality bar

- **Physics:** every module has a validation notebook comparing it with a published example
  ([ADR 0009](../adr/0009-physics-checked-against-published-references.md)). Validation runs in CI
  with stated tolerances. The first references: Kanthal's worked element examples, Ward's BTU per
  cubic foot ranges, an ASTM C680 example, and the analytical solution for a heated slab.
- **Invariants with Hypothesis:** thicker insulation never increases heat loss; energy in = stored
  + lost; a longer element at the same voltage never draws more power; brick counts cover the
  wall volume.
- **Golden files:** the reports, glTF digests and plan PDFs from a fixed set of design files. A
  change shows up as a reviewable diff.
- **API and web:** contract tests from the OpenAPI document, Playwright end to end, axe and
  Lighthouse gates, as in Glazecalc.
- **Safety:** the app gives guidance and is not a substitute for an electrician, a gas fitter or
  local codes. Electrical and gas outputs carry that note, and designs outside the checked range
  are refused with a reason rather than drawn.

## Open questions

1. **The materials library.** Which manufacturers' data sheets can be used, and how they are
   cited (Glazecalc ADR 0009 is the model).
2. **Cone tables.** Orton publishes temperatures by heating rate; check the terms before
   shipping the table, or store user-entered values only.
3. **The client's kiln:** gas, wood or both; its size and cone; the timeline; and whether any
   solar power is planned (for a blower or a controller).
4. **Liability for client work.** Plans given to a paying client need a clear statement of what
   is checked and what is the builder's responsibility, and possibly a review by a gas fitter.
