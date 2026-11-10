# 17. Engine v2: heat and statics rebuilt from first principles on the reference kilns

- **Status:** accepted. The software survey reported on 2026-11-09
  (`docs/research/statics-software.md`, with pairs of tools in `statics-combinations.md`); the
  statics design starts from it.
- **Date:** 2026-11-09

## Context

The user asked for the heat and static-forces engine to be rebuilt from Olsen's reference kilns
(*The Kiln Book*, 4th ed.). Every one of them was built and fired, and many print how much energy
and time a firing took.

The first pass is in three places:
- `docs/engine-v2/problem-set.md`;
- `core/tests/v2/reference_kilns.yaml`: what the book prints about each of the 53 kilns, with its
  page and status;
- `docs/research/engine-v2-negative-cases.md`.

It found:

- **v1 simulates only the 15 gas and electric kilns.** It refuses the 38 wood, coal and oil
  kilns, which hold most of the book's fuel figures (problem set §8).
- **v1's statics is too permissive, as well as too strict in places.**
  - It has no ring check on a roof arch across the width.
  - A dome too thin to stand gets only an info note.
  - `buttressed: true` is taken on trust.
  - Three Olsen kilns altered past a published collapse limit were reported to pass it (negative
    cases §3; not re-run).
- **The physics reviews rank v1's other weaknesses**
  (`docs/reviews/2026-11-physics-review-heat.md`, `-structure.md`):
  - heat: one lumped chamber temperature; flue gas taken at the chamber's temperature; fixed
    excess air; draft without losses; a steady ground;
  - statics: a fixed hinge line; cold-only catenary feet and end walls; one expansion rate for
    every material.

The user, on v1's warnings and errors: "these have been so wrong for the whole time".

## Decisions (the user, 2026-11-09)

### The engine

1. **v2 replaces v1 now.** In the user's words: "all tests are invalid until it is rebuilt".
   - v1's tests no longer count as evidence that the engine is right.
   - v1's code stays in the tree only so the CLI, API, web and MCP server keep running until v2
     can stand in.
   - No more work goes into v1's physics. The radiation coupling planned for v1
     (`docs/planning/11-09-26.md` §G part 2) is dropped.
2. **Engine v2 is the focus until it works as a whole.**
3. **No flags until it's done.** v2 computes and reports numbers, each with its working
   (`kilndesigner.working`). It raises no error or warning on any kiln until the engine is
   complete and validated. The levels are then designed afresh.
4. **First principles, nothing fitted.**
   - Every quantity comes from physics and sourced data.
   - Nothing is calibrated to the reference kilns: they only validate.
   - A quantity no source gives is carried as a stated band.

### Order

5. **Statics first**, once the software survey (`docs/research/statics-software.md`) reports. The
   heat model follows.

### Statics

6. **Start over.** The first draft's statics design (thrust lines and wall blocks as linear
   programs, and its error and warning levels) is set aside until the survey reports.
7. **Walls and buttresses are computed, not trusted.**
   - Whatever holds a wall is modelled, and its equilibrium worked out: another wall, the next
     chamber, an earth bank or a frame.
   - That gives the resultant's place in each base and the friction each bed joint needs.
   - In the user's words: "this should not be hard".
   - `buttressed: true` no longer stands in for the check.

### Heat

8. **The gas path, not a flue-loss figure.** The combustion gas gives up much of its heat in the
   chamber before it leaves. How much is worked out along its path; it is not taken as a
   flue-loss fraction at the chamber's temperature.
9. **Excess air from the air intakes and the draft.** λ is worked out from the fireboxes' air
   intakes, sized from the reference material on them, and from the draft. It varies through the
   firing, and many kilns are fired in reduction (λ < 1).
10. **Radiation between faces goes into v2 only.** It uses:
    - `thermal/radiation.py`: view factors and the grey enclosure;
    - the hot-face emissivities in `docs/research/radiation-exchange.md` §5, extrapolated past
      their measured range (the user's decision, recorded there in §5.5);
    - gas radiation (§6), once its correlations are in hand.
11. **The ware load is required.** No heat result without a load in the design.
12. **Each kiln's own fuel.** The fuel is matched to the kiln: the wood species or coal it
    burned, with that fuel's composition and heating value looked up from a source.
13. **Burners are sized, not assumed.** Where the book gives a choice, the engine picks the
    burner that sizes best from the burner charts, the spacing and the gas system. Olsen's kits,
    for example, use the Gas Appliance MR-750 or MR-100 (p.222).

### The reference data

14. **Olsen's kits are sized as stacking space** (pp.169–170, p.173). Their design files are to be
    resized from it; today they take that volume as the whole chamber.
15. **Tobe's "40 tons of wood"** (p.90) is for the whole kiln.
16. **The No. 32 orifice passage** (pp.220–221) is the book's general example of orifice sizing,
    not the kit 24's burner.

### Validation

17. **The bar v2 must meet:**
    - the book's printed figures fall inside v2's bands, carried from the uncertainty of the
      inputs;
    - every must-fail case, N1–N6 (`docs/research/engine-v2-negative-cases.md` §6), fails in the
      numbers;
    - all 53 kilns as built stand.

## The heat model's starting design

Carried from the first draft and amended by the decisions above. Each part is sourced before it
is built.

| Part | Method | Source | Status |
|---|---|---|---|
| H1 Zones in series | a well-stirred zone per chamber or tube segment, from the firebox to the chimney; the gas leaves each zone at that zone's temperature | Hottel's well-stirred furnace (heat review #2; Hottel and Sarofim 1967, not read) | an open source is needed first |
| H2 Combustion | equilibrium products at the local λ, their enthalpy carried along the path | Cantera, GRI-Mech 3.0 thermodynamics (ADR 0012) | NASA polynomials, 200–3500 K |
| H3 Fuels | each kiln's own fuel (decision 12) | to be looked up for each kiln | – |
| H4 Unburnt fuel in reduction | equilibrium CO and H₂ below λ 1; soot not counted | `cantera-tespy-review.md` §2 | equilibrium, as ADR 0012 |
| H5 Radiation between faces | the grey enclosure with exact view factors | `thermal/radiation.py`; `radiation-exchange.md` §1–3 | box, sprung arch and sail dome; other shapes refused |
| H6 Gas radiation | Hottel's framework, mean beam length | `radiation-exchange.md` §6 (Lienhard §10.5; Alberti et al.) | the correlations are still to get |
| H7 Hot emissivities | each face's material, at its own temperature | `radiation-exchange.md` §5 | extrapolated past the measured range (the user's decision), said so in the working |
| H8 Walls | v1's transient wall per face, k(T) and c_p(T); edge and corner shape factors | ADR 0015; Incropera Table 4.1 (to read) | – |
| H9 Ground | two-dimensional transient soil under a grounded floor | Kiva's method (`energyplus-review.md` §5) | – |
| H10 Ware | a node per zone with c_p(T), and its lag; the load is required (decision 11) | heat review #1 | the clay's reaction heats aren't sourced |
| H11 Heat input | burners sized (decision 13); elements' power changing with temperature; fuel stoked at the rate the schedule needs, within the air the draft allows | Olsen ch. 8; Kanthal | – |
| H12 Draft and air | a pressure balance round the gas path: the buoyancy of each hot column less friction and fittings; the air intakes sized from the reference material (decision 9) | Moody 1944; Idelchik (pages to record) | – |
| H13 Openings | spy holes and flues as surfaces at the room's temperature; the firebox and chimney walls as transient faces of their zones | `radiation-exchange.md` §1.3 | – |

## Where v2 lives

**Placement.**
- v2 is built as `kilndesigner.v2` in `core/` (`v2/heat/`, `v2/statics/`), tested in
  `core/tests/v2/`, so the app keeps running meanwhile.
- It may use v1's leaf modules: units, working, sheet, model, shape, library, cones, combustion,
  `thermal.*`.
- When v2 works as a whole, the CLI, API, web and MCP server switch to it, and v1's heat and
  statics modules are removed.

**Engine rules that still hold:**
- the engine stays pure (ADR 0002);
- Pint at the boundary and SI floats in the solvers (ADR 0004);
- every result carries its working;
- outside the range a method was checked to, v2 refuses (ADR 0009), except where the user has
  decided otherwise, as for the emissivities.

## What v2 leaves out for now

- fluid dynamics, flame shape and burner aerodynamics;
- combustion kinetics (equilibrium only);
- soot radiation, until sourced;
- salt and soda chemistry;
- the ware's reaction heats (not sourced);
- fibre anchoring;
- thermal stress, creep, spalling, hot modulus of rupture and hot cohesion, which have no data
  (`refractory-movement-and-mortar.md` §3). The survey kept this: the software is there, the
  data isn't (`statics-software.md` §16).

Each is said in the working where it would matter.

## Consequences

- v1's results aren't to be relied on. The app shows them only until v2 stands in.
- The book's printed figures become tests that v2 can fail.
- v2 needs data v1 never had:
  - each kiln's own fuel;
  - the firebox air-intake sizing;
  - the gas-radiation correlations;
  - the IFB emissivity above 1077 °C;
  - the kits' chambers resized from their stacking space.
- From the stopped first pass, the dataset, the problem set and the negative cases were kept. The
  v1 baseline was dropped with v1.

## In an interview

"The old engine passed every historical kiln I gave it, and also passed kilns I'd made thinner
than the published collapse limit: a test set of kilns that stood can't catch an engine that
lets everything stand. So I rebuilt it from first principles, with nothing fitted to the kilns
it's judged against. They're a check, not a calibration. It flags nothing until it works as a
whole, and the must-fail cases come from the limit-analysis literature."
