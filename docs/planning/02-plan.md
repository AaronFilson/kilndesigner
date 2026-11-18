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
    v2/                       engine v2 (ADR 0017): heat/ and statics/; replaces v1's
                              thermal, combustion and statics checks when it stands in
  cli/                        Typer: build, check, simulate, export
  api/                        FastAPI; OpenAPI contract; SQLAlchemy 2 + Alembic
  worker/                     arq tasks: simulate, build geometry, render plans
  mcp-server/                 MCP server over the engine (official SDK's MCPServer, ADR 0016)
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
| [0015](../adr/0015-firing-simulation.md) | The firing is simulated by a 1D finite-volume wall per face (proposed; v1, replaced by 0017's heat model) |
| [0016](../adr/0016-mcp-server.md) | AI assistants reach the engine through an MCP server that returns the working (proposed) |
| [0017](../adr/0017-engine-v2.md) | Engine v2: heat and statics rebuilt from first principles, validated on the reference kilns (accepted) |

ADRs 0002–0016 are still marked proposed, though M0–M8 shipped on them. Accepting the ones
still in force (and marking 0015 superseded by 0017 once v2 stands in) is the owner's call.

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

**2026-11-09: engine v2 replaces v1** (`docs/adr/0017-engine-v2.md`; `11-09-26.md` §H).
- The heat and statics milestones below describe v1. Their results aren't to be relied on until
  v2 is rebuilt.
- Engine v2 is the focus until it works as a whole: statics first, then heat.

### Where things stand (2026-11-18)

- **Merged to `main`:** M0–M4, M6 and M8 (on v1); engine v2's statics and heat (PR #12).
  M7 is on hold; M5 and M9 haven't started.
- **v2 against ADR 0017's bar** ([11-10-26.md](11-10-26.md), "The round's report"; the full
  suite of 2026-11-18, [the review](../reviews/2026-11-18-review.md) §1):
  - 49 of 52 printed figures inside the bands. Suzuki's 60 bundles a side for chambers 4–7 (read
    by the owner, 2026-11-17) is the one added. The other three are the open items: the 36 ft³
    cross-draft, Singh's low-fire kiln and Breda's wood;
  - N1–N6 all fail;
  - **52 reference kilns, not 53 (the owner, 2026-11-17, again 2026-11-18):** Olsen's two-chamber
    kiln (pp.202, 206) is his unbuilt proposal, so it left the set. It stays as a design,
    `examples/olsen-two-chamber.yaml` and the `wood-two-chamber` template, for the model's
    behaviour tests (its facts in `core/tests/v2/design_kilns.yaml`);
  - 51 of the 52 stand hot, every one v2 models (Blakebrough's fibre isn't modelled). Tobe has
    stood hot since 2026-11-17, worked back from standing (high-duty brick, 13½ in;
    `11-17-26-inputs.md` §12). The lower-bound rule's "not given" stays for designs no one has
    built;
  - the suite pins 39 kilns reaching their cone at every corner of their band (14 gas and
    electric, Kähler and Blakebrough on Rule 1's band since 2026-11-18; 25 single chambers), and
    all 11 rows somewhere in theirs. That 7 of the rows reach it at every corner comes from runs
    outside the suite before 2026-11-11, Tobe's on its old lining. 2 kilns are open items.
    (Counted before the full suite was stopped, 2026-11-18: the tests wait until the concepts are
    fixed.)
- **No surface runs v2 yet.** The [module review](../reviews/2026-11-17-module-review.md)
  found what stands in the way:
  1. v2 can't run a design file on its own. The setting, the draft-path inputs and the fuel data
     are built in `core/tests/v2/` (`loads.py`, `path_inputs.py`, `fuel.py`), and λ is passed in
     rather than taken from the draft. These move into the engine and the design model.
  2. There's no front door. v2 returns SI dataclasses; the surfaces read v1's pydantic `Report`.
     The fix is one `v2.design(kiln) -> V2Report` with units and working.
  3. v2 imports two v1 heat modules (`gas`, `electric`), and both pull in `heatloss`. Move the
     constants to leaf modules and add an import-linter contract for v2.
  4. Castables, the bill, hardware, the frame, movement and foundations read v1's heat output.
     Split v1's heat modules into sizing (kept) and physics (removed) before removing v1.
  5. Heat and statics share no hot state. The hot statics takes all the masonry at C16's
     temperature, which the owner calls "just bad modeling" (2026-11-17): the temperature falls
     through the brick. A bridge from the heat model's wall temperatures is the fix. Tobe no longer
     waits on it (worked back, `11-17-26-inputs.md` §12).
  6. Duplication inside v2: two `kiln_path`, `Band`, `Sourced` and `hydraulic`, and four
     `NotModelledError`.
- **The inputs v2 needs** are in [11-17-26-inputs.md](11-17-26-inputs.md), checked against
  sources outside the book first. Concrete's c_p(θ) is now quoted from EN 1992-1-2 §3.3.2. Singh's
  top is a band below 2100 °F, 800–1149 °C (the owner). Dense brick's hot strength and IFB
  emissivity above 1077 °C are still not found; Tobe no longer needs the first, and the owner keeps
  the second's extrapolation. Most of the answers aren't applied yet (next, item 1).

### Next, in order

Reordered 2026-11-18 ([the review](../reviews/2026-11-18-review.md)). The owner's answers of
2026-11-17 overturn rules that the test-side code still carries. So they are applied first, and
v2 is checked against its bar again, before item 2 folds that code into the engine. Otherwise the
engine would take in rules the owner has overturned.

**The priority (the owner, 2026-11-18):** "the only thing that matters right now is getting the
reference kilns measured and the v2 engine on a good start, with the right tools to make the rest
of the system work". Tests come second until then. v1's heat and physics are discarded, and the
rest is reworked around v2 (ADR 0017, "Where v2 lives", amended).

1. **Finish this part: apply the 11-17 answers, then rerun the bar**
   ([11-17-26-inputs.md](11-17-26-inputs.md); the review's §2 lists each one with its files).
   Nothing new needs to be sourced except Singh's cover.
   - **Principle 6 (§1):**
     - ~~where nothing is drawn, the chimney is ¼ of the chamber's width, not a ⅕–¼ band
       (`paths.rule6`, `RULE_6_NOTE`)~~ (done 2026-11-18);
     - ~~a part drawn to scale is sized from the drawing (the anagama in the hole's flue, about
       6 in)~~ (done 2026-11-18: 4–8 in wide, its undrawn depth ¼ of the width);
     - Kitade's chimney is 12 in.
   - **Stoke holes aren't intakes (§3).**
     - A stage's air is the upstream gas, the printed chamber inlets (Hollyweird's tube, the
       two-chamber design's tube), and a side-stoked chamber's own air intake under its stoke hole.
       The owner (2026-11-18): Fig 8-10's side stoke configuration is "a smaller hole, the stoke
       hole, above the air intake and fire pit access". Kitade's second chamber takes its air that
       way on both sides, about the front's 432 in².
     - After the front chamber is done, "some or all of the front air is closed to prevent cooling
       too fast". So the front's intakes for a later stage are a band from closed to open, with
       the book's state where it prints one (Tamba's open, p.87; Kitade's closed, p.202).
     - ~~The design's stoke hole is no longer taken as a fully open intake~~ (done 2026-11-18,
       inputs §3, "Applied in the engine"). A firebox's own `air` and the kiln's `air_inlets`
       carry the air. Only a floor-fired firebox's mouth is still its stoke hole. A stage with the
       front shut and no inlet of its own is refused.
     - ~~The intakes the dataset derives from stoke holes are reworked~~ (done 2026-11-18).
       Ellington's 648 in² and Kitade's 63 in² went. Hollyweird's front is its 15 × 18 in air
       inlet. The two-chamber design's 49 in² went. Singh's coal kiln's stoke holes are a band,
       open in hours 1–3. The book gives the air its own openings (inputs §3):
       - Ellington's three 13½ × 9 in air holes under its stoke holes (Fig 4-97), 364½ in²;
       - Kitade's two 12 × 18 in air-draft and ash-pit holes (Fig 8-11), 432 in².
     - **Left by the change, for the kiln-by-kiln check:**
       - Suzuki, Tobe, the Kyoto climbing kiln and Hotchkiss are refused. Their designs stand a
         trough in for the main firebox, which leaves chamber 1 no way in for its air.
       - No row's design gives a chamber its own air inlets yet. With the front shut, every staged
         chamber except Hollyweird's back is refused. Kitade's second chamber takes two 12 × 18 in
         inlets (`air_inlets`, Fig 8-10) once it is entered.
     - **The draft counts no flow backwards** (`draft.py`). An opening above the neutral plane, the
       height where the kiln's pressure meets the room's (hydrostatics, `fittings-and-kiln-
       convection.md`), is credited no air, and the hot gas it would push out isn't modelled. The
       book prints that outflow: Tamba is stoked until "flame is coming out of two or three stoke
       holes further on" (p.87). It bears on what an open stoke hole does while it is open (the
       owner's inrush, §3), and on reduction's back pressure. Asked about by the owner, 2026-11-18.
   - **The fire mouth (§2):**
     - a design setting per stage: open, an open fraction, or closed;
     - the book's state as a dataset fact where it is printed (Tamba open, Kitade closed), and
       every state reported elsewhere;
     - the open mouth's cooling of the first chamber modelled;
     - Tamba's slow corner stops shutting its mouth.
   - **Kitade (§8):** a second chamber, the first one's size (assumed, the book draws one), its
     stage, the 12 in chimney and the mouth closed; then rerun T1.
   - **Tamba (§9):**
     - ~~16 in side holes in the design, the dataset and the `tunnel` template together~~
       (done 2026-11-18, with the round bundle, 15 × 30 in);
     - the 14° slope waits on a sloped tube, engine work not listed before;
     - the earth against the half-buried tube's walls: v2's heat model takes only a floor to the
       soil (`ground.py`), so the walls lose to the room. New engine work, for Tamba and the
       anagama in the hole.
   - **Singh (§4):** ~~the top as a band from 800 to 1149 °C~~ (in the dataset and the design,
     2026-11-18, carried by `single_cases.TOP`). The cover is the owner's estimate (2026-11-18):
     shards 3 in thick over 80 % of the top, 20 % open as the exhaust. Engine work: an open top
     that takes a partial lid and its port. To source: a loose shard layer's conductivity and
     emissivity.
   - **The 36 ft³ cross-draft (§6):** the band test over its lining and gas, at cone 10 only (the
     owner, 2026-11-18).
   - **The fast-fire's mouths** stay open while firing (the owner, 2026-11-18): its intakes above
     and below the grate stand.
   - ~~**Kähler and Blakebrough (§7):** the Rule 1 burner bands~~ (done 2026-11-18: fibre as IFB
     by pp.39 and 71; both reach cone 10 at the band's most).
   - ~~**The two-chamber design (§8):** read p.202 again~~ (done 2026-11-18: out of the reference
     set, its p.202 facts split from Kitade's).
   - ~~**Breda (§5):** the top as cone 01–2~~ (done 2026-11-18, the owner's estimate). T1 and T2
     pass at both ends; T3 stays open, 1,800 kg 21 % under v2's least (2,290 kg) with the top
     moving it only 3 %. To trace: the setting's light end (it still assumes a shelf layer for
     pots set off the floor), the slats' moisture, the domed floor taken flat.
   - ~~**Hollyweird (§8a):** its two chambers from its own figures~~ (rescanned 2026-11-18,
     `olsen-figure-scaling.md` §7, §8):
     - 53 in wide, on Fig 4-113's bricks;
     - the front's springline 42½ in and the back's 35 in, under 12 in domes;
     - 18 in side walls, the owner's drawn 14–19 in;
     - three 12 × 11 in flues between the chambers;
     - the 15 × 18 in opening the front firebox's air, below the grate, and the 5 in tube the
       second firebox's.
     It stands cold and hot (90.5 lbf/ft on the buttress). Left as engine work:
     - the back chamber's fall and its taper into the chimney: a row whose last chamber narrows
       and falls, new schema work;
     - the floors' steps;
     - the flues' sills, 15½–18 in up;
     - v1 drawing the front firebox with a roof of its own under the dome.
   - **The kiln-by-kiln check** (the owner, 2026-11-18): each reference kiln, one at a time, with
     Hollyweird's care. Read its text and figures on the page images, and compare them with its
     design and its dataset entry. Then check v2 models it as the book describes it. A kiln that
     doesn't match a template or a design is future work, noted here, not a fault to force.
     **Measure, not decide** (the owner, 2026-11-18):
     - Each measurement goes into the dataset with its status and spread.
     - Each gap is listed in the kiln's doc and below: where the design differs from the book,
       where the engine can't express it, and where the book shows nothing.
     - The designs and the engine aren't changed during the check.
     - An engine limit is never a fact about the kiln.
     The design changes made on 2026-11-18 before this was said were taken back. Their
     measurements stay in the dataset.

     The gaps so far, for a later round:
     - ~~Hollyweird~~ (above; the owner's answers set its design).
     - **The Kyoto type:**
       - The design takes Fig 4-28's 4½–6 ft across the kiln and Bidai's 41⅓ in along the draft.
         The book's range reads along the draft, and its length across isn't printed.
       - The main firebox is unsized, so v2's path is refused.
       - The book's arch is pointed and springs near the floor, with the reduction chambers' peak
         set back.
       - The doors are in a side wall.
     - **One firebox in each chamber, in the schema** (the Kyoto type, Suzuki, Tobe, Hotchkiss).
       v1 makes the himae troughs only when they don't fit side by side across the front. Where
       they fit, v1 lays them out in front of the kiln, and v2's path takes them as troughs only
       through the test-side `path_inputs.ONE_PER_CHAMBER`.
     - **Suzuki and Tobe:**
       - No main firebox in the designs: Suzuki's is drawn but unsized, and Tobe's isn't mentioned.
         Both paths are refused.
       - Where a design gives both a main firebox and a himae in each chamber, chamber 1's himae
         should burn the main firebox's gas. Today the path would refuse it, and v1 would lay the
         himae from chamber 2.
     - **Bidai, Kawaii:**
       - The designs have no air opening. The book's (Fig 8-7, 12–14 × 14 in) is in the dataset.
       - Kawaii's dogi has no height in the design, against the printed 5 ft.
     - **Bae's gilgama:** the design gives no firebox mouth. Its scaled size (Fig 4-69, about
       16 × 15 in) is in the dataset.
     - **Blakebrough's Sturt kiln:**
       - By p.205 the inlet flues bring the channel's air supply under the wood; the design takes
         them as the channel's flues into the chamber.
       - The channel's printed 12 in is its whole height; the design takes 12 in above the grate,
         and the engine adds a 12 in ash pit.
       - The outlet flues aren't shown in the book.
     - **Blakebrough's Tasmanian kiln:** the fibre's thickness isn't printed. p.69's "12in. ...
       compressed to 8in." is the stack's height under the press, which the design had taken for
       it. Fig 5-71 scales the walls' ends 7–9 in, which agrees with the design's 8 in. The lower
       15 in of IFB (taken as fibre) and the moving box (taken as a car) were already listed.
     - **Bowen Mountain, Breda:** no new gap.
     - **Chappell's salt kiln:** its firebox's opening isn't drawn or sized, so v2's path leaves
       the intake out and the air is an upper bound.
     - **The Church kiln** (and Fireworks, the same firebox):
       - Fig 7-3 draws each ash pit and walkway 14 in wide and 18 in deep. The design alone takes
         the ash-pit mouth as the firebox's width, 36 and 24 in. The dataset's 504 in² is the
         book's.
       - Fig 7-4's three adjustable air levels (below the grate, at the grate, at the stoke hole)
         aren't sized, and the design has none.
     - **Conrad's teardrop:**
       - Fig 4-147's ash-pit air supply scales about 17 × 13 in, 216 in², against the design's
         468 in² (the firebox's 39 in by the 12 in pit). The measurement is in the dataset.
       - A framed opening high in the front is unidentified.
     - **Ellington's new hog:** Fig 4-99 shows the dug-out firebox's "vertical air channels" in
       its front wall, which the plan draws as the three 13½ × 9 in "inlet flues" (Fig 4-95). So
       they bring the air down into the firebox. The design takes them as flues from the firebox
       into the chamber, closing the firebox's mouth into the chamber, which the book draws open.
     - **The electric car kiln:** no new gap. The floor elements, if p.245's clipped word is
       "and", were already listed.
     - **Falcone's Pompeii updraft:**
       - Fig 6-34's under-air supply scales about 12 × 11 in ([82, 237] in², ±25 %, on the
         bricks' courses). The design gives no opening, so its path alone takes the firebox
         chamber's whole open end, 118 × 71 in.
       - The nine exit holes (Fig 6-32) don't scale to better than a factor of 2 (about 12 or
         25 in square, as the vault's brick faces are ends or beds), so the path stays on Rule 6.
     - **Fujiwara's Bizen kiln:**
       - The dataset's intake was the dogi's loading hole, "3½ × 2ft ... when open" (p.102),
         1,008 in². For the firing that hole is bricked up as the dogi door. Fig 4-55's front
         elevation draws a fire hole in it with an air duct under it, and p.103 fires 2½ days
         "stoking the fire-mouth air duct", then 4 days "from the fire hole".
       - The dataset now takes the air duct as drawn, 75–189 in². That is a drawing scale: the
         widths are firm on the dogi's 10 ft, the heights loose by 2×.
       - The design's stoke hole is still the loading hole (a gap).
       - With the smaller intake, the staged chamber is under suction at its side holes' height.
     - **The basic groundhog:** the type's firebox mouth isn't drawn or sized, so v2's path takes
       the air as an upper bound.
     - **Hotchkiss** (every figure scaled on the printed block sizes, `olsen-figure-scaling.md`
       §9):
       - The slope is 11–16°, where the design takes 22°.
       - The main firebox is one domed box of commercial firebrick, where the design has six 9 in
         channels. Its lower front, and so its air path, is hidden in both photos.
       - There are four flue slots in the measured wall, 300–420 in².
       - The springline above the floors is still open.
     - **Kähler:** no new gap. Fig 5-18's 40½ in, read at zoom 5, is the 36 in depth plus the
       4½ in front wall, which confirms the uncertain 36 in.
     - **Kaneko:** no new gap.
     - **The Kannofen:**
       - Its two fireboxes have grate bars and ash pits, two arched stoking mouths with hinged
         covers (Fig 6-39), and small openings at the ash pits' foot (Fig 6-37).
       - None is sized: the figure is "NOT TO SCALE" and the photo's brick format isn't printed.
       - The design's fireboxes have no grate and no mouth, so its path takes each firebox's whole
         open end.
     - **Kato:** no new gap. Its air is "dampened" (p.132), its openings unsized, so v2's path
       takes the design's ash-pit mouths.
     - **Kenzan:** Fig 6-47's "IRON GRATE OPENING 15" × 19"" may be the firebox's mouth with the
       grate seen through it, not the grate alone, as the design takes it.
     - **Kitade:** no new gap beyond the owner's answers already in this item (inputs §8).
     - **La Borne:** Fig 4-78 draws the firebox front's stoke opening above the grate and an air
       opening into the ash pit, but their numbers are too faded to read. The design gives the
       firebox no grate and no mouth, so its path takes its whole open end.
     - **The Meaders groundhogs:**
       - Neither book figure sizes the firebox mouth, so v2's path takes the air as an upper
         bound.
       - David's Fig 4-105 draws five or six openings at the front arch's foot, about 5–7 in wide,
         their heights loose by the sketch's two scales.
     - **Miravet:** "the two flues at the front of the dome, closest to the firebox, are closed"
       in the initial firing (p.159). A design's flues can't change over a firing, the same need
       as the fire mouth's states (item §2 above).
     - **Moveros:** the firebox mouth is a triangle of two leaning stones, 22 in at the base and
       27 in tall (Fig 6-3), about 297 in². The design takes a 22 × 27 in rectangle, 594 in². The
       dataset now carries the triangle.
     - **Niñodaguia:** its 18 × 27 in mouth is drawn round-headed, 451–486 in² in the dataset.
       The design takes the rectangle.
     - **The oil-drip kiln:** Fig 8-20 draws each port flue's air entering at its foot past
       "DAMPER BRICKS", so the dataset's whole flue face is only the most-air end. The damper
       bricks' least isn't drawn.
     - **The 36 ft³ cross-draft, the four kits, the three-chamber kiln, the Phoenix kilns,
       Singh's two kilns:** no new gap.
     - **Tamba:** Fig 4-16 draws the dogi's mouth, "STOKING" with "AIR" below it, and "the
       firebox becomes the air supply" for the side stoking (p.86). The mouth isn't sized, so v2's
       path takes the dogi's whole open end.
     - **The four updraft tests:** no new gap. p.74, read on the second scan
       (`docs/research/Scanned_20261025-1022.pdf`), matches.

     **The check is done** (2026-11-18): every kiln with a design was read against its pages.
     Across the 52 kilns, the gaps fall into these groups:
     1. **The fire's way in.** The designs often lack the opening the book draws or measures:
        - a firebox's air opening narrower than the firebox (Bidai, Kawaii, the
          multi-directional kilns, Conrad's);
        - a floor-fired mouth (Bae, Moveros' triangle, Niñodaguia's round head, Fujiwara's air
          duct);
        - a main firebox (the Kyoto type, Suzuki, Tobe, Hotchkiss).
        The dataset carries what the book shows. A design schema field for the ash pit's mouth,
        and ports that aren't rectangles, would carry it into the designs.
     2. **Openings that change over a firing:** the fire mouth, flues closed early (Miravet),
        damper bricks (the oil drip).
     3. **Two-way flow at openings:** Breda, the fast-fire, Anderson Ranch and Tamba print gas
        out and air back in.
     4. **Shapes a design can't take:**
        - a row's pointed arch along the draft and its offset peak;
        - a back chamber that falls and tapers (Hollyweird);
        - the doors in a side wall under an arch;
        - flues in a catenary's legs (Sturt's, not shown in the book).
     5. **Readings that move a design's axes or size:**
        - the Kyoto type's chamber along the draft;
        - Hotchkiss's slope, 11–16° against 22°;
        - Sturt's channel and inlet flues.
     - **The design schema:** a port (a stoke hole, an air inlet) is a rectangle or a circle.
       The book draws triangular, round-headed and pointed openings (Moveros, Niñodaguia,
       Hotchkiss, Bae), so their areas can only come in through the dataset.
     - **Engine, for the stoke-hole rule:** v2 takes a grate firebox's ash-pit mouth as the
       firebox's whole width by the pit's depth. Where the book draws a narrower pit (Bidai,
       Kawaii, the multi-directional kilns, Conrad's), the design can't say it except through the
       firebox's `air`.
   - **Then rerun the bar**, once the concepts and the measurements are in (tests come second, the
     owner, 2026-11-18): the full suite, and the rows' band corners outside it (Tobe's on its new
     lining among them). Then restate "Where things stand".
   - **Waiting on the owner:** nothing. Front stoke holes were read in the book instead (the
     review's §5, question 9).
2. **Fold the test-side engine knowledge into the engine** (module review items 1, 3 and 6).
   Nothing new needs to be sourced for it.
   - **Follow-up: two-way flow at openings** (the owner, 2026-11-18, `11-17-26-inputs.md` §3).
     "The fire will suck in as the stoke changes … Mostly the kiln will suck in air when in
     oxidation and vent flame in reduction, but these values change too." v2's draft counts
     inflow only. Each opening needs both directions:
     - air in below the neutral plane, gas out above it, the plane moving with the damper, the
       stoking and the atmosphere;
     - the book's flame from the stoke holes further on (p.87);
     - Breda's flames out of the chimney cone holes, stoked again when they "suck back in"
       (p.168, Fig 6-53);
     - the fast-fire's top spyhole, its flame watched until it "sucks back into the kiln", time to
       stoke (pp.142–143); the Anderson Ranch kiln's "reducing flames coming out of the door blow
       hole" at 1250 °F (Table 5-2).
     Sources to find first: the two-way flow through an opening in a hot enclosure (compartment-
     fire research, `grates-and-fuel-beds.md` [G10]–[G11], the neutral plane's height).
   - Item 3 wasn't scheduled before 2026-11-18: move `kiln_top_in`, `BURNER_PORTS` and
     `CONTINUOUS_FRACTION` to a leaf module, and add the import-linter contract for v2.
   - ~~ADR 0017's list of the v1 modules v2 may use is out of date.~~ Amended 2026-11-18 (the
     owner):
     - v1's heat and physics are discarded;
     - everything else is reworked around v2;
     - the layout modules v2 relies on are listed;
     - v1's sizing may stay, never trusted over v2's measurements.
3. **The v2 front door and the bridge to statics** (items 2 and 5). This puts the masonry's own
   temperature through its thickness into the hot statics: the hot face weak, the cooler brick
   behind it carrying the load (HWI's UR-19 says walls are built for this). It fixes the model
   fault the owner named.
4. **Make the suite faster:** a `bands` marker for the corner runs and an on-disk cache of
   their results. The full `pytest --cov` took 2 h 0 min on 2026-11-18 (about an hour on
   2026-11-11).
5. **Stacked zones up a chamber.** These make every top-to-bottom evenness figure testable.
6. **Reduction (λ < 1) as the fuel band's other end**, and the held runs rerun on all the
   draft's air.
7. **Switch the surfaces to v2**, after the split in module review item 4; then design the levels
   afresh (decision 3).
8. **Small items** (the review's §4):
   - concrete's specific heat into the library;
   - from HWI's second reading (`hwi-handbook.md` §9):
     - Fig 3.4's fireclay growth curve below 2400 °F for `movement.py`;
     - the ring-table tests proposed in `hwi-ring-arch-tables.md`;
     - Olsen's A-5 at 5′10″ checked on his page (HW and `rings.py` give 31 + 52, the
       transcription 30 + 53).
   - Done already:
     - Tobe (§12): worked back from standing (ADR 0017, decision 17 as amended).
     - Scaling the six unsized chimneys from Olsen's drawings: read on 2026-11-17
       (`docs/research/olsen-figure-scaling.md`). Fireworks, La Borne's back door and the Kannofen
       are still to measure.

| # | Milestone | Done when | Resume-worthy engineering |
|---|---|---|---|
| **M0** | **Foundations** | uv workspace, ruff, pyright strict, pytest, CI, ADRs, the design-file schema | A typed Python monorepo with strict CI from the first commit |
| **M1** | **Electric kiln engine** | `kilndesigner build` turns a YAML spec into an electric front-loader box kiln: geometry (STEP, glTF), steady-state heat loss, element design, and a JSON report | Parametric B-rep CAD, unit-safe numerical code, property-based tests (Hypothesis), golden files |
| **M2** | **Plans** | A dimensioned PDF and a DXF, the brick course plan, a cut list and a bill of materials | Typst document generation, 2D projection from 3D, deterministic output |
| **M3** | **Gas and hybrid: the author's kiln** | A cross-draft with a cast dome, as a car kiln and as a door kiln, with costs side by side; burner sizing; the propane supply check; the electric-to-gas switch-over chart; plans to build from | Combustion and fuel-supply models, optimisation (SciPy), cost modelling, comparing designs |
| **M4** | **A kiln you can design in the app** | `docker compose up`, then: (1) the model is a kiln you could build: the arch on skewbacks over the full walls, the steel frame, a door or a car, burner and flue ports, the chimney and spy holes, coloured by material; (2) dimensioned drawings, course plans, the bill of materials and the cut list shown in the page (files still downloadable); (3) a viewer with front, side, top and section views, a cutaway and named parts; (4) a design started from a kiln type and edited with choices, not YAML (YAML stays as a tab); (5) castables you mix yourself: a batch recipe in the design gives its wet, dried and fired densities, a conductivity checked against published firebricks, what the temperatures in the wall do to it (kyanite, quartz, burnout), the batches and ingredients the lining needs, and the first firing (water, organics, heat, a dry-out schedule), refusing mixes outside the checked range. Each point has browser tests | FastAPI + SQLAlchemy 2 + Alembic, a job queue, an OpenAPI-generated client, React Three Fiber, Playwright |
| **M5** | **Hosted app** | Accounts, design sharing by link, deploys with approval to AWS, tracing and metrics | Multi-tenant Postgres (row-level security), OIDC with PKCE, CDK in Python, keyless deploys with rollback, OpenTelemetry |
| **M6** | **Firing simulation** | Transient heat-up along a schedule, results in Parquet, charts and a wall heatmap in the viewer | Finite-volume numerics, DuckDB analytics, GPU shaders for the heatmap |
| **M7** | **Wood and off-grid: the client's kiln** (on hold, 2026-10-31) | A firebox, natural-draft burners, the chimney and draft, fuel per firing, and plans for a site with no mains power | Natural-draft modelling, multi-fuel designs, plans that stand alone |
| **M8** | **AI assistants** | An MCP server: "design a cone 10 gas kiln for 12 cubic feet, under $3,000" | MCP in Python, with tools that return the working |
| **M9** | **Real firings** | Import firing logs from the author's controller, compare them with the simulation, and fit wall properties to them | Parameter estimation (SciPy), data ingestion, model-versus-measurement reports |
| Later | **Glass** | Templates, top-element layouts, annealing schedules | |
| Later | **Drag to stretch, with grid snap** | In the viewer, drag a handle on a wall, the floor, the arch or a port to resize it, as in a CAD tool. Sizes snap to a grid you set (whole bricks by default, or inches or millimetres), the handle shows the size as you drag, and letting go changes the same field the form edits and rebuilds the kiln. A size outside the checked range is refused with the reason (ADR 0009) | Direct manipulation in React Three Fiber, snapping and constraints, a fast rebuild |

### Status (2026-10-21, overnight)

- **M0, M1, M2 and M3 are built**, on the stacked branches `m0` → `m1` → `m2` → `m3`, with 127
  tests passing (published worked examples, Hypothesis invariants, golden reports).
- The first results for the author's kiln are in [docs/kilns](../kilns/pnw-hybrid-crossdraft.md).
- Validation lives in pytest (`core/tests`) rather than marimo notebooks so far; ADR 0009's
  notebooks are still to do, as readable companions to those tests. (Done 2026-10-29: see the
  quality bar below.)
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
  [10-29-26.md](10-29-26.md)). 53 of his kilns are examples in `examples/olsen/` (52 since 2026-11-17: his unbuilt two-chamber design moved to `examples/`) and all build
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

### What's next (2026-10-29; superseded)

_Superseded by ADR 0017 (2026-11-09): no more work goes into v1's physics, so items 1–3 below
stand only as they carry into v2. See "Where things stand" under Milestones._

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

### Status (2026-10-29): M6

- **M6 is built** (ADR 0015): a 1D finite-volume model of each face, fired along the design's
  schedule (or full heat, then the cone's final rate), with the time, whether the heat keeps the
  schedule, energy, electricity, propane and cost per firing (the M3 leftovers), and a hybrid's
  cost and time against its switch-over temperature. Checked against the erf solution, the steady
  solver and an energy-balance invariant. Results are Parquet, read with DuckDB;
  `kilndesigner simulate`, `/api/simulations/{key}` on the worker, and a Firing tab with charts and
  a shader heatmap with a scrubber (Playwright `firing.spec.ts`).
- Gaps: the castables (and Cerachem) have no sourced specific heat, so the author's kiln asks for
  its roof's `specific_heat` before it can be simulated; ware is lumped at fired clay's
  room-temperature c_p; no radiation between faces or inside film; wood and oil wait for M7;
  natural gas has no price field, so its cost isn't given.

### Status (2026-10-30)

On branch `m6`, merged (`a0d89fd` and the fireboxes merge after it), with the rest uncommitted at
the time of writing; 1482 tests, coverage over 98 % in both Python and web. The round's notes and
the next round are in [10-30-26.md](10-30-26.md).

- **Waste allowances** come from sources (BIA 5 %, `brick-waste.md`), not a flat 10 %.
  **Kast-O-Lite** is researched (`castables.md` §14).
- **Steel for domes** is sized (AISC 360-16, hot; `steel-design.md`): an angle along each wall the
  dome bears on, posts, tie rods and a ring, drawn and billed. The lintel for a door in part of a
  wall is a written method only: the design can't yet describe such a door.
- **Every kiln shape is laid in brick:** round kilns (rings, plans, a layer model), open tops,
  chambers in a row (stepped on a slope, an arch over each along the draft), sloping single
  chambers, bent runs, and fireboxes (against a wall, under the floor, troughs), with flues
  between chambers, floor ports and roof flues cut in the model. Tamba and the tunnel are one
  vault over the run, as Olsen draws them. Dimension text is sized to each view.
- **Fireboxes give options, not rules:** a grate step and ash pit set by the design, with
  Olsen's figures for each way of firing reported beside the numbers (heat, even burn, ash and
  flashing); the only error is a firebox that doesn't reach the chamber floor.
- **4½ in round rings** are the builder's choice: straights with mortar-filled wedge joints
  (Olsen Fig. 2-13, the default), straights cut to the angle (the default for electric kilns,
  whole bricks, faces 9 in outside, courses stacked in line, warned when a size needs a closer),
  featheredges, or arch bricks. **Electric walls** of 2½ and 3 in brick are one cut ring in
  4½ in courses, checked against five published kilns to 0.15 in
  (`electric-kiln-survey.md`; a spec log artifact gathers more).

### Status (2026-10-30, round 2)

- **The web form** edits the ring method, firebox step and door openings.
- **Round electric kilns** are N-sided polygons when built of whole cut bricks: elements in
  grooves round the facets, polygon lids and floor slabs in steel bands, a round-electric template.
- **Doors in part of a wall**, from Olsen's figures: steel lintels sized hot, arched heads and
  jambs checked by thrust-line statics, Bidai and Kawaii with their side-wall doors as built.
  Refractory bearing stress is researched but has no published allowable, so it is shown, not
  checked.
- 1531 tests, coverage over 98 % in Python and web, 22 Playwright specs against a rebuilt stack.

### Status (2026-10-30, round 3)

- **Bearing** of refractory still has no published allowable, so it is shown, not checked;
  **sliding** at a door arch's springing is checked (BIA, μ ≥ 0.60).
- **The author's kiln** is rebuilt on today's engine and its write-up is current
  ([pnw-hybrid-crossdraft.md](../kilns/pnw-hybrid-crossdraft.md)); its open items need the author.
- **Round electric kilns** load from a hinged lid, with grooves and polygon slabs in the model.
- **Calimpong's teardrop** has its door as built and passes, after two engine fixes for doors
  under domes.

### Status (2026-10-30, round 4, branch `m7`)

- `m6` is merged to `main` (PR #2); work continues on `m7`.
- **Electric floors** can sit inside the walls (Paragon) or under them (Skutt).
- **Complex curves** have a research file (`curved-kilns.md`) and a shape model behind every
  existing type ([complex-curves.md](complex-curves.md) steps 1–2); Calimpong's teardrop is next,
  in progress. An arch bug (rise over half the span) was found and is being fixed.
- **The author's kiln** has the author's answers in: door, eight burners in the door, 11
  cylinders, the shino hand-over, an editable stacking setting (in progress).
- 1632 tests, coverage over 98 % in Python and web.

### Status (2026-10-30, round 4 done)

- Arches over a semicircle are drawn right (Bidai, Kyoto).
- **The author's kiln** has its arched door head, burners up the door's sides, low spy holes and
  an editable setting (shelves, posts, ware ratio). Loaded it fires in about 65 h, mostly on the
  elements, far from the author's 8–12 h (4–6 h when needed).
- **Calimpong's teardrop** builds as a teardrop plan under a dome (complex curves step 3).
- All checks green on `m7` (1662 tests). The hybrid-firing upgrade is done: elements and burners together, and a target-time
  solver (the author's kiln at 4 h needs about 1,000,000 BTU/hr and 9 full cylinders, $124.65); the author is scanning A.P.
  Green's brick tables for bottle kilns and brick domes.

### What's next (2026-10-30)

See [10-30-26.md](10-30-26.md): the author's castable version to the solver's firing targets, a
faster solver, A.P. Green's tables (being scanned) into the research, bottle kilns and
conical-brick domes, sourced fast-firing limits for ware, then Calimpong's leftovers, the unclear
values and M7. Round 5 is queued there: the A.P. Green scans are in (`docs/research/brick-shapes/`),
and Olsen p.250 turned out to be a smoke firebox for an electric kiln, not a ware limit.

### Status (2026-10-30, round 5)

- **A.P. Green's catalogue** is transcribed (`docs/research/brick-shapes.md`) and its tables are
  tests: 681 complete circles and 551 sprung-arch courses, the engine within a brick of each.
- **Tapered shapes** are a design setting (`lining.shapes`), Olsen's simpler set by default, A.P.
  Green's full set (No. 1-X wedge, 3 in No. 4 arch and No. 1 wedge) as an option, in the form too.
- **A smoke firebox** (`fire.purpose: smoke`, Olsen Fig. 9-25) for reducing an electric or gas
  kiln: no heat rules, Olsen's sizes, the element-life note.
- **Firing time** is the user's choice, not limited by ware (the author).
- Blocked: conical-brick domes (complex curves step 4) have no dome-brick source yet.

### Status (2026-10-31, round 6)

- **Conical (tatami) bricks**, sized by the builder or scaled from Olsen's Fig. 4-6, with the
  author's bore and groove; domes laid course by course with a fit check; the bricks bought as
  raw fireclay. Bidai's arch is 6 in tatami bricks under a 3 in clay, straw and earth overcoat.
- **Complex curves** steps 4–5: revolved domes and their membrane forces, vaults of changing
  section (Bowen Mountain, Tamba's side doors), Calimpong's neck, slices and course plans.
- **Slow firings** (`kilndesigner slow`), ports out of the brick count, wedge mortar on the bill.
- About 60 unclear values settled, 12 of them read by the author; Kato's chamber is 7 ft long
  under the semicircular arch its section draws.
- All checks green on `m7` (2,995 tests, 98.43 %).

### Status (2026-11-06)

- **Natural gas is costed** (M6 gap closed): `site.natural_gas_price`, the user's own rate, per
  therm, kWh or MJ, or per ft³ or m³ through Olsen's 1000 BTU/ft³ (p.230). No default; left out,
  the firing says it needs the rate. It flows into the firing's cost and therms, the switch-over
  chart (now propane or natural gas), the CLI, the API and the form (Playwright step). The Olsen
  24 kit carries the user's $1.5822/therm. `docs/research/natural-gas-prices.md`: EIA's prices,
  informational only. The hybrid cost-per-useful-kWh analysis stays propane only.
- Still unsourced: concrete's specific heat (EN 1992-1-2 §3.3.2(1)'s c_p(θ) isn't quoted in
  `docs/research/`, only its density), so the platform stays out of the simulation; Cerachem and
  castables other than the Kast-O-Lite 30 class value still have no specific heat.

**M7 is on hold (2026-10-31).** The client is dealing with real estate trouble and is
distracted; open question 3 waits until they come back to it. Nothing is built for M7 until
then: the work that would serve it (fireboxes, natural draft, wood) stays general, for any user.

### Status (2026-11-06, M7 started: a general propane-and-wood kiln)

- **A new example**, `examples/olsen-32cuft-propane-wood-fastfire.yaml`: Olsen's fast-fire
  downdraft (p.139–143) enlarged as p.142 allows to 32.9 ft³ of stacking (36 × 54½ × 47½ in
  chamber), two 13½ × 45 in fireboxes under the floor and a 9 × 13½ in chimney (Fig. 3-9, p.77),
  burners four a side (Fig. 5-46). Not the client's kiln, which stays on hold.
- **Propane or wood**: the gas firing of a wood kiln with fireboxes under the floor is simulated
  with them sealed (Olsen p.142), so its target time and slow firing work. At 3½ h (p.139) it needs
  about 1.7 million BTU/hr (8 Ransome B5 at 2.2 psi), 16 full 100 lb cylinders at 20 °F, 49 gal.
- **Wood per firing** isn't worked out: no heating value for wood is in `docs/research`. Olsen's
  fast-fire figure (under ¼ cord, 3½–4 h, 12–16 ft³) is given to compare. Questions for the
  author: a sourced heating value for wood and a firebox efficiency, and whether a firing may
  start on propane and finish on wood.

### Status (2026-11-08, M7: wood per firing)

- **`site.wood`**, all the user's own, no defaults: `heating_value` (net, oven-dry), `moisture`
  (wet basis), `firebox_efficiency`, and optionally `cord_weight` (oven-dry lb/cord) and `price`
  (USD/cord; `cord` = 128 ft³ in the unit registry). Left out, the firing says what it needs.
- **`wood.py`**: the gas firing's heat into the kiln, Q, put in by wood instead: H(w) =
  H(dry)(1 − w) − 2.44w MJ/kg (FAO UBET eq. 3, checked against Forest Research's 14.7 GJ/t at 20 %),
  m = Q ÷ (η·H(w)), cords and cost. In the firing result (`wood_kg`, `wood_oven_dry_kg`,
  `wood_cords`, `wood_cost_usd`), its working and the CLI. Not in the web form yet.
- **`docs/research/wood-fuel.md`**: sourced starting values (MU Extension, Forest Research, FAO,
  USU's cord weights by species), Olsen's and others' wood per firing to compare. Not found: a kiln
  firebox efficiency; eucalyptus and pallet values; FPL's scanned PDFs weren't readable.

M1 to M3 make a usable open-source tool and design the author's kiln. M4 and M5 are the
full-stack story. M7, the client's kiln, is on hold (above); it can move earlier again when the
client is ready, since the CLI can produce the client's plans before the app exists.

### Status (2026-11-06): M8 started

- **ADR 0016**: an MCP server on the official Python SDK (`mcp` 2.3.0, pinned), following
  Glazecalc's: stateless, read-only, snake_case tools, results as structured data and JSON text.
- **`mcp-server/`** (`kilndesigner-mcp`): `list_templates`, `get_template`, `list_examples`,
  `get_example`, `validate_design`, `build_design`, `simulate_firing` and `start_design`, every
  result with the engine's working; stdio, or stateless Streamable HTTP with `--http`. Tested
  through an in-memory MCP client.
- "Cone 10 gas, 12 ft³, under $3,000" now starts from the gas cross-draft (33 ft³ chamber,
  $8,499 priced as it stands): the assistant resizes it and builds again.
- **Left for M8**: a tool that compares designs; resources (materials, formula sheets) and
  prompts; mounting `/mcp` on the API with Glazecalc's Host/Origin checks, limits, tokens and
  OAuth once M5 has sign-in; the conformance suite and Inspector in CI; a registry listing.

### Status (2026-11-08): M8 compares, with resources and prompts

- **`compare_designs`**: two or more designs (YAML, `template:<id>` or `example:<name>`) built and
  set side by side in the CLI's rows (chamber volume, heat loss, hottest face, installed power or
  burner input, propane supply, hand-over, priced materials, errors/warnings), each row with the
  report's own working and every design's findings; with `simulate`, each firing's time, energy,
  fuel and cost with its working, or the engine's reason it isn't simulated. The rows moved from
  the CLI to `kilndesigner.compare`, so both surfaces show the same ones. The stacking volume is
  not estimated (no source in `docs/research/`); the chamber volume is compared.
- **Resources**: `kilndesigner://schema/design` (the design file's JSON Schema),
  `kilndesigner://materials` and `kilndesigner://materials/{id}` (each material's values with its
  source and status), `kilndesigner://alloys`, and the formula sheets (ADR 0013) behind a
  template's or a top-level example's findings: `kilndesigner://templates/{id}/checks`,
  `kilndesigner://examples/{name}/checks`.
- **Prompts**: `design_from_brief` (start_design → resize → validate → build → compare) and
  `explain_finding` (a finding explained from its sheet, margin and lever).
- **Left for M8**: mounting `/mcp` on the API with Host/Origin checks, limits, tokens and OAuth
  once M5 has sign-in; the MCP Inspector and conformance suite in CI (both are fetched with npx at
  run time, so they don't run offline); a registry listing.

## Quality bar

- **Physics:** every module has a validation notebook comparing it with a published example
  ([ADR 0009](../adr/0009-physics-checked-against-published-references.md)). Validation runs in CI
  with stated tolerances. The first references: Kanthal's worked element examples, Ward's BTU per
  cubic foot ranges, an ASTM C680 example, and the analytical solution for a heated slab.
  - **Status (2026-10-29):** done for nine solvers in `notebooks/validation/` (marimo), each
    run by `core/tests/test_validation_notebooks.py`, which fails if any figure leaves its stated
    tolerance: wall (FOSSEE, CSJM), surface (Neutrium air; `ht` for the correlations and h_r),
    elements (Kanthal, Olsen p.258–260, Kanthal's Ct tables, Krueger), transient wall (Holman's
    erf), combustion (flame temperature, LHV, Ward's ranges), chimney draft (Olsen's Rule 5, Ward,
    altitude, stack effect), arch thrust (HarbisonWalker's tables and 12 ft example, Pitelka's
    arches), castable conductivity (three Morgan castables held out) and propane supply (D × L × K,
    Ward's tanks, the cylinder tables, RegO). Not found to check against: an ASTM C680 worked
    example, a published h_r or hot-face-down case with numbers, available heat at kiln flue
    temperatures, a catenary's thrust, a three-phase element design, a BOM waste or curved-brick
    cutting allowance.
  - **Since ADR 0017 (2026-11-09)** these notebooks and v1's tests no longer count as evidence
    for heat and statics. v2's bar is decision 17: the book's printed figures inside v2's bands,
    N1–N6 failing in the numbers, all 52 reference kilns standing (53 until 2026-11-17). Its tests are in
    `core/tests/v2/`. Notebooks for v2's solvers are still to do.
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

## Follow-up research: mortar, bricks and statics (2026-10-31)

These are fundamental to the engine, and several checks are still "shown, not checked" or rest
on a stated assumption for want of them. The information exists in published sources; find it
there (the author would rather not dig through their own textbooks, Hibbeler's *Mechanics of
Materials* and Dowling's *Mechanical Behavior of Materials*, so treat those as a last resort and
ask before relying on them). What's found so far is in `docs/research/blocked-items.md`,
`masonry-statics.md`, `bands-and-bottle-kilns.md`, `concrete-foundations.md` and
`refractory-bearing.md`.

- **Mortar:** how mortared joints behave in masonry (bond and tensile strength, shear and
  friction at a joint, how thick a joint may be, air-setting against heat-setting at heat), and
  whether two rings laid one on another act as one. Today a mortared wall gets no credit for
  its mortar, and Bowen Mountain's arch is taken as held by mortared masonry on the author's
  word, with no number.
- **Bricks:** strength at temperature (hot modulus of rupture, hot crushing, creep under load:
  ASTM C16, C583, C832 and makers' sheets), an allowable bearing stress or factor of safety, and
  how insulating and light-duty brick differ from dense. Bearing is still shown, not checked,
  for refractory.
- **Statics:** masonry arches, vaults and domes from primary texts (Heyman's *The Stone
  Skeleton* and *Equilibrium of Shell Structures*, Huerta's *Arcos, bóvedas y cúpulas*, Block
  and Ochsendorf's papers), with worked examples to test against: the rampant arch's hot
  thrust, a door cut into a vault (how load shares onto its ring), the groin's ribs, a round
  dome past 51.8° (formulas already reconstructed; check them on the page images), a catenary
  at a step, and corbels at heat. Also Trinks's *Industrial Furnaces* Vol. I (pp.196, 238) on
  furnace arches.
- **Foundations:** block and cinder-block platforms (`concrete-foundations.md` C6–C10): no
  sourced temperature limit found, so a block platform is checked as cast concrete; still to get
  TMS 216 / ACI 216.1, EN 1996-1-2 Annex D, NCMA TEK 6-2C and ACI 122R for block conductivity.
- **Option needing a source: a vented block platform** (`concrete-foundations.md` C8 [C12]):
  hollow block laid with its cores horizontal and open so air moves through, a kiln-builders'
  practice known only from a forum thread. Not modelled: it needs a sourced way to work out the
  heat the moving air carries off (a correlation for natural convection through horizontal
  open cores heated from above, or a measured kiln floor on such a course), and the block's
  conductivity above. Until then a platform is solid concrete on dry soil, the side that
  over-states the heat reaching the ground and the platform's top.
- **Concrete's specific heat:** found. EN 1992-1-2 §3.3.2 was quoted on 2026-11-17 in
  `11-17-26-inputs.md` and is in `blocked-items.md` §20 since 2026-11-18. It is still to add to the
  library, so the firing simulation can carry a platform's own layer; today the simulation's
  floor goes into dry soil without it.
- **How to look:** open-access papers and theses (MIT masonry group, SAHC and ICSA
  proceedings), archive.org and HathiTrust full texts, makers' engineering guides, and
  standards' free excerpts. Record quotes, pages and URLs as the research files do; "not found"
  is a valid answer.

**Fifth round (2026-10-31), `docs/research/mortar-and-brick-strength.md`.** What closed:

- *Joint friction, hot (closed):* dry dense refractory joints 30.9° (μ 0.60) cold, 26.5° (0.50)
  at 300 °C, 27.0° and 27.9° at 600 and 900 °C (Oliveira et al. 2021, read in full). A hot
  sliding check should use 0.50, not BIA's 0.60; IFB and fireclay untested.
- *Mortar bond (closed, as "give no credit"):* NBS 1939–43 measured joint bond of 5–665 psi,
  scatter to 79 %, air-setting joints often losing all bond after 1000 °C and heat-setting
  joints having little until 1350–1500 °C; HWI SAIRSET 530 psi at joints, dried only. Keep
  no tension across joints; Bowen Mountain's arch stays a no-tension thrust check, now with a
  sourced reason. Hot shear: friction steady, cohesion lost above 900 °C (abstracts only).
- *Two rings (closed):* unbonded rings act separately; ring separation cut arch strength 33–71 %
  in tests (Sarhosis et al. 2016 review). Combine ring thicknesses only when header-bonded.
- *IFB hot load (closed):* C16 values at 10 psi for JM 23–32, TC-26 and the BNZ grades; BNZ's
  "maximum mean temperature" per grade is the first maker's rule tying load to temperature.
- *Hot strength of dense brick (partial):* hot MOR 530 psi at 1350 °C for a 42 % alumina brick
  (Bureau of Mines 1984); hot crushing 24–34 MPa to 1000 °C for one alumina-spinel brick.
- *In the engine (2026-11-03):* the door arch's springing and a flat roof's ends slide at the
  hot 0.50 (every material named where it isn't Oliveira's tested brick: IFB, fireclay,
  castable); a ring of several layers stands as its inside layer alone unless
  `roof.rings_bonded` (form checkbox too), the thrust still from the whole ring. Bowen Mountain:
  3.7 times the thinnest ring (7.0 as one), still passing. No golden number moved.
- *Burners over several walls (2026-11-03, PR #8):* `heat.gas.burners.walls` names the walls
  that fire together (left and right sides is common in the reference kilns). The count is
  shared between them in the order named, as evenly as it divides, and spread evenly along each;
  a finding says how, and names any wall that got none. The web form edits it too
  ([10-30-26.md](10-30-26.md)).
- *Still open:* an allowable bearing stress or FoS (none found), a largest joint thickness, hot
  cohesion values, IFB hot MOR and creep, rampant-arch thrust, the catenary at a step, hot
  corbels, Trinks Vol. I (not online), Heyman (1966) and Huerta (2001) texts.

**Sixth round (2026-11-08), `docs/research/refractory-movement-and-mortar.md`.** What closed:

- *Growth and allowance (closed):* fireclay brick grows 3/32 in per ft to 2400 °F, and "most
  brick manufacturers recommend" that as the expansion allowance (Brosnan, in Schacht's
  *Refractories Handbook*, read in full): a third source for the engine's 3/32 in/ft beside
  Olsen p.51 and the IFB sheets. Bhatia (PDHonline M158 p.29): half the theoretical expansion is
  enough, the joints take the rest, which matches Olsen's 1/16 in/ft in a steel frame.
- *Mortar types (closed):* HWI's air-setting, heat-setting and phosphate definitions; SAIRSET's
  joint MOR 650 psi dried, 500 psi after 1500 °F (sheet 8/10: 5006); HWI M-2: mortar "is always
  the weakest link", joints "as thin as possible", troweled better than dipped.
- *Largest joint (closed):* "should not exceed 1⁄4 in" (Beall, *Masonry Design and Detailing*,
  5th ed. p.143); 1/16–1/8 in is the usual recommendation (snippets only).
- *In the engine:* the sprung arch's growth reference now cites Brosnan too. No number moved.
- *Proposed:* a wall expansion-allowance finding (3/32 in/ft, half allowed, Olsen's ¼ in joints
  past 48 in); an arch-rise working step (geometry, Derived); a joint-thickness warning past ¼ in.
- *Still open:* hot cohesion, allowable bearing stress or FoS, IFB hot MOR and creep, castable
  reversible expansion and drying shrinkage, a measured arch rise, rampant-arch thrust, the
  catenary at a step, hot corbels, the door in a vault; HWI's 2005 Handbook and *Modern
  Refractory Practice* not reached online.
- *2026-11-17:* HWI's 2005 Handbook reached (the owner's copy) and read in full:
  `docs/research/hwi-handbook.md`.
  - Closed: castable first-heat shrinkage as a band (0.2–1.5 %), expansion allowances by class,
    and a primary dry-out schedule. It also prints the rounding rule of Olsen's ring tables, which
    are HW's own.
  - Anchors: HWI's industrial anchor rules are recorded as reference only. **The owner
    (2026-11-17):** most castable used in kiln linings doesn't need anchors, and it depends on the
    specific material, so the engine adds no anchor requirement.
  - Still open: hot cohesion, an allowable or FoS, IFB hot MOR and creep, a castable's reversible
    expansion by product, and a measured arch rise.
  - Eleven proposals for the engine wait on the owner (`hwi-handbook.md` §8; number 10, anchors,
    is withdrawn).

## Follow-up research: hot emissivities and gas radiation (2026-11-09)

For radiation between the chamber's faces (`11-09-26.md` §G; `docs/research/radiation-exchange.md`
§4–§6). The user's note: firebrick and IFB have changed little in 30–40 years, so older
references serve.

- **IFB emissivity above 1077 °C: search for more.**
  - The measured lines (Morgan's MPK grades, Hampartsoumian 1990) stop at 1350 K. IFB is used
    well past that: K-26 and JM 26 are classified to 1430 °C, and cone 10 is about 1285 °C.
  - Until data are found, the engine extrapolates the measured lines and says so in the
    working (the user's decision, 2026-11-09).
  - Where to look:
    - Touloukian and DeWitt vol. 8. Its master index (ADA129117, public on archive.org) shows
      no brick, firebrick or IFB emissivity in it, so read only its mullite (aluminium silicate)
      pages, 1685 and 1687, as a guide.
      - Vol. 8 is on DTIC (ADA951942): download it in a browser, as DTIC refuses scripts. It
        was down for maintenance on 2026-11-09.
      - It is also a borrow-only scan on archive.org (`thermophysicalpr0008purd`).
      - The DSIAC report DSIAC-BCO-2022-222 (DTIC AD1194128, June 2022) lists the rest of the
        TPRC series on DTIC: vol. 7, metals (ADA951941); vol. 9, coatings (ADA951943, for kiln
        wash and high-emissivity coatings).
      - The electronic version, CINDAS's TPMD, is commercial;
    - Gray et al. (1989) and Hampartsoumian (1990) in full;
    - Jackson and Yen (1994) on ceramic-fibre insulation;
    - the makers' technical bulletins (Morgan/Thermal Ceramics, HWI, Allied);
    - NBS/NIST and NASA reports.
  - Also the chemistry of K-23, K-26, JM 23 and JM 26, so each can be matched to a measured
    grade.
- **Osborn (1985):** what "low", "medium" and "high" alumina mean in his fire-brick classes. A
  kiln's dense brick reads 0.75–0.79 in one class and 0.55–0.63 in the next.
- **Fibre above 1127 °C, castables, kiln wash, glazed ware and element wire** at firing
  temperatures.
- **Gas radiation: closed for CO₂ and H₂O.** v2 uses published WSGG sets (Bordbar 2014 by
  default, Dorigon 2013 as the alternative; `core/src/kilndesigner/v2/heat/gasrad.py`), within
  about ±10 % of Alberti's line-by-line tables. Still open: a soot model for luminous flames
  (wood, reduction), which ADR 0017 leaves out until sourced.

## Open questions

1. **The materials library.** Which manufacturers' data sheets can be used, and how they are
   cited (Glazecalc ADR 0009 is the model).
2. **Cone tables.** Orton publishes temperatures by heating rate; check the terms before
   shipping the table, or store user-entered values only.
3. **The client's kiln** (on hold, 2026-10-31: the client is busy with real estate trouble;
   don't ask again until they return to it): gas, wood or both; its size and cone; the
   timeline; and whether any solar power is planned (for a blower or a controller).
4. **Liability for client work.** Plans given to a paying client need a clear statement of what
   is checked and what is the builder's responsibility, and possibly a review by a gas fitter.
