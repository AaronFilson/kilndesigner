# Thermal software for engine v2: single tools

Surveyed 2026-11-10, before any v2 heat code (ADR 0017, decision 5: statics first, then heat). No
engine changes were made. This is the heat model's counterpart of `statics-software.md`; pairs,
threes and bridges are in `thermal-combinations.md`, which ends with the proposed build order.

**Status: complete.** Still *pending*: Idelchik's rectangular fittings (no open copy reached),
Daun et al. 2005's algorithm, and the primary papers behind the two theses quoted for the zone
method and its smoothing.

## The yardstick

- **What a tool takes off v2's hands (the user, 2026-11-09).** A tool is judged by whether there
  is a way to use it so the project doesn't have to solve that part itself. Matching a rule or a
  past result counts for nothing; the checks below only show a tool was driven correctly.
- **The reference kilns stand (the user, 2026-11-10).** "The kilns in the reference material all
  worked for the people that built them for the purpose they were built for. Those are the
  starting point, and the model has to let them stand as working examples. Formulas then go to
  get the right info for the engine, and existing modules are used in the right places in combo
  with the right bridges." So a tool or chain is also judged by whether it lets a reference kiln's
  documented firing be reached with that kiln's own burners or fuel and its own draft: Olsen's
  fast-fire, cone 10 in 3½ h (p.139), on two fireboxes and a 14 ft chimney. If a chain says a
  working kiln can't reach its firing, the chain is missing physics, and the sourced formula or
  tool that would supply it is named. Nothing is fitted to the kiln (ADR 0017, decision 4).
- **Anything useful is allowed (the user, 2026-11-10)** "if accurate and can run on a desktop,
  although like for like functionality is better faster". Cantera's kinetics and a WSGG fit made
  from radis are both allowed (`docs/planning/11-09-26.md` §H).
- **A bridge module is cheaper than a whole science module** (the user, 2026-11-10;
  `tool-triples.md` §6).

## How the survey was run

- Read first, and not redone here: `heat-libraries.md` (ht, heatrapy), `energyplus-review.md`
  (CondFD, ScriptF, Kiva), `cantera-tespy-review.md` (Cantera beyond available heat, TESPy),
  `radiation-exchange.md` (view factors, grey enclosure, hot emissivities, gas-radiation method),
  `thermal-properties.md`, `firebox-efficiency.md`, `wood-fuel.md`, `tool-triples.md` §2, §3, §6,
  and the probes in `scratch/toolsets/{gas-path,view-factors}/` and `scratch/missed-combos/`.
- Probes: `scratch/thermal-survey/` (git-ignored, as the other surveys' probes are). Each script's
  docstring says what it models, its test inputs and how to run it:
  - `pypi_facts.py`, `licences.py`, `bundled.py`: versions, licences and CPython 3.14 wheels;
  - `mc_exchange.py`, `engine_mesh_mc.py`, `closure_probe.py`: Monte Carlo view factors and
    grey-gas exchange areas (trimesh + embreex), on test shapes and on the engine's own solids,
    and the closure corrections;
  - `wsgg.py`, `wsgg_check.py`, `mbl_check.py`: the published WSGG sets as data, their checks,
    and the zone method against the mean beam length;
  - `cantera_wsr.py`: Cantera's kinetics against its equilibrium at kiln residence times;
  - `soil_probe.py`: the ground under a hot floor (scikit-fem 2-D; a 1-D stand-in);
  - `integrator_probe.py`: fixed-step implicit stepping, `solve_ivp` and SUNDIALS IDA;
  - the end-to-end chains (`thermal-combinations.md` §4): `chain_fastfire.py`, `chain_ida.py`,
    `chain_dt.py`, `chain_rays.py`, `draft_print.py` (Olsen's fast-fire); `chain_crossdraft.py`,
    `crossdraft_bounds.py`, `crossdraft_target.py`, `mustfail.py` (his 36 ft³ cross-draft);
    `w15_ifb.py`, `ground_coupled.py` (W15);
  - `fluids_rough.py`, `sundae_help.py`, `materials_peek.py`: what a package carries;
  - `lit-gas/`, `lit-zone/`: two literature agents' downloads and extraction scripts.
- Extra packages came through `uv run --with` overlays; the repo's environment wasn't touched.
- Machine: the WSL2 Debian machine of `statics-software.md` (i7-7700, 15 GB), shared overnight
  with another heavy agent, so every probe was kept small. Times are wall-clock, single runs.
- Marks: **Run** (computed here), **Read** (read in the source or the paper), **Snippet** (a
  search extract only), **Derived** (worked here), "from memory". Temperatures, sizes and loads
  marked as test inputs are not engineering data.

## 0. Short answer

| Part of the heat model (ADR 0017) | The tool that takes it | What v2 still writes | Verdict |
|---|---|---|---|
| H1 zones, and the firing in time | SUNDIALS IDA through scikit-sundae: the zone model as a DAE, the cone as an event; on a reduced kiln 0.02–0.04 s and within 0.3 s of the reference, against 0.22 s and 11 s late for 30 s fixed steps (Run, §3.2) | the zone balances, the state, the walls as cells (~60 lines) | **adopt IDA**; v1's step pattern (Run on the fast-fire, §3.1) or `solve_ivp` as the no-new-package fallback |
| H1 by Cantera reactors | Cantera `ReactorNet`: works with a heat flux computed by our own code each call (Run, §3.4) | – | **not needed**: at 0.5–10 s residence time the kinetic zone differs from equilibrium by ≤ 0.22 % of the fuel's heat at λ 1.15 (Run) |
| H2, H4 combustion: equilibrium products, enthalpy, transport | Cantera 3.2 (a dependency already) | wood and coal surrogates, the range guard | **keep** (§7) |
| H5 radiation between faces, with obstruction | trimesh + embreex Monte Carlo (Run, §5.1): checked to 1e-5 on a sphere, Cauchy's 4V/A on a cube, a half shadow within 0.5σ; closed by Larsen & Howell's smoothing (Read, §5.2) | emission sampling, tallies, the smoothing (~100 lines) | **adopt** |
| H5 checks | `radiation.py`'s closed forms; the copied contour kernel (`tool-triples.md` §3) | – | **keep as checks** |
| H6 gas radiation | Bordbar 2014's WSGG set (HITEMP-2010 line by line; MR 0.01–4), read in NIST FDS's source and in RadLib, inside the zone method, its exchange areas from the same Monte Carlo rays (Read, Run, §6) | the set as data, the weights function and the grey-gas radiosity solve (~100 lines) | **adopt**, Dorigon 2013 as the second set for the band (the two within 13 %) |
| H6 line-by-line reference | radis or HAPI with HITEMP: a HITRANonline login and 9.2 GB compressed (H₂O 3.2, CO₂ 6.0 GB; Read) | – | **not needed**; Alberti's free LBL tables (8.5 MB) are the test reference |
| H8 walls | v1's `TransientWall` (k(T), c_p(T), harmonic interfaces), driven by its affine heat-in (Run in the chain) | the Picard update (optional) | **keep** |
| H9 soil | scikit-fem, 2-D axisymmetric (Run, §4.2): 1548 nodes, a 30-day step response in 0.8 s | mesh, boundaries, coupling (~150 lines) | **adopt**; a 1-D hemisphere in `TransientWall` is a fallback (−16 % at 15 min to −1.4 % at 30 days, Run) |
| H12 draft and the gas path | fluids (friction, fittings, grates, packed beds) with Cantera's gas (Run, `tool-triples.md` §2; §8) | the column sum; rectangular-duct coefficients from Idelchik (*pending*, §8) | **adopt** |
| Convection inside and out | ht's named correlations; v1's `surface.py` | the choice per surface and its range | **adopt** ht as a runtime dependency |
| H10 ware and setting | the Monte Carlo obstruction above, a lumped node with v1's fireclay c_p(T) | the setting's envelope from the design | **adopt** (§10) |
| H11 burners, wood beds | no tool; fluids' packed-bed laws for a char bed's resistance | the burner and stoking models; the data | data first (§11) |
| Target-time solves | SciPy `brentq` around a firing; IDA's events | the outer loop | **adopt SciPy** (§12) |

**Ranked verdicts** (by the science each takes off v2's hands):

1. **trimesh + embreex**: ray tracing against any chamber the engine meshes, partial shadowing by
   the setting and bag walls, and the path lengths gas radiation needs. **Adopt.**
2. **SUNDIALS IDA (scikit-sundae)**: the firing as a DAE, events, the fastest of the three
   integrators tried at the same accuracy. **Adopt.**
3. **Bordbar 2014's WSGG set** (data, from FDS and RadLib): the gas's grey gases, HITEMP-based.
   **Adopt**, with **Dorigon 2013** as the second set for the band and **Alberti's tables** as the
   line-by-line test reference.
4. **Cantera**: products, enthalpy, transport. **Keep**; its kinetics only as an offline check.
5. **fluids**: friction, fittings, grates, packed beds for the gas path. **Adopt** at runtime.
6. **scikit-fem**: the ground in 2-D. **Adopt.**
7. **ht**: named convection correlations. **Adopt** at runtime (from the dev group).
8. **v1's `TransientWall`**: the wall physics, now the fallback integrator's wall and the oracle
   for IDA's walls. **Keep.**
9. **SciPy** (`root`, `solve_ivp`, `brentq`): the fallback integrator and the target-time loop.
   **Keep.**

Not adopted: radis or HAPI with HITEMP (a login and ~10 GB to remake a published fit), Cantera's
reactors as zones, CasADi (deferred), pyViewFactor and numba (checks only), Open3D (392 MB),
pyembree, scikits-odes and assimulo (no CPython 3.14 wheels), FiPy, py-pde, pyfvtool and heatrapy
(nothing over scikit-fem), JAX and Pyomo, exo_k (GPL-3.0-only).

What this survey found that changes the plan (Run, Derived):
1. **Gas radiation decides whether a working kiln reaches its firing.** Held to the gas
   temperatures of Olsen's p.309 log, the fast-fire's setting ends at 1056–1066 °C with a
   transparent gas, short of cone 10; with Bordbar's WSGG set it follows the log on 28 % of its
   draft's air (`thermal-combinations.md` §4). The luminous flame (soot) is still missing: no
   source in `docs/research/` gives a kiln flame's soot.
2. **The ground's recommended model under-reads.** `thermal-properties.md` §8.5's
   h_g = max(slab, steady disc) gives 10–46 % less than the 2-D transient between 15 min and 3 days
   (Run, §4.2); the loss is nearer the slab term plus the edge term than the larger of them. And an
   adiabatic ground round the kiln (Incropera's case 10) halves the late loss against ground losing
   to the air (h 10 W/(m²·K), a test value).
3. **Equilibrium is enough for a zone's energy**; kinetics matter only for CO in reduction below
   about 1000 K (2 % of the fuel's heat at 700 K, Run, §7.2).

## 1. What the heat model needs

From ADR 0017's starting design (H1–H13) and the problem set (§2):

| Need | Kind of computation | Where it comes from |
|---|---|---|
| H1 zones in series | well-stirred gas zones, quasi-steady; a firing in time | **open statements found:** D. Latham, MSc thesis, Queen's University, 2008: p. 26 (Read), the well-stirred model after Rhine & Tucker (1991, pp. 244–257: uniform gas, one grey gas, a sink and a refractory, three total exchange areas); pp. 24–25, a gas zone's accumulation = radiation in − out + enthalpy in − out − heat out (after Rhine & Tucker p. 216); eqs. 24–26, a one-gas-zone cube furnace with the gas leaving at the zone's temperature, written as the chains here write it (Read in a garbled text layer: the terms are clear, the indices to be checked on the rendered pages); Monnaemang 2015 (UCT MSc, eqs. 3.11–3.14, after Hottel & Sarofim 1967 and Modest 2013) for the exchange areas. Hottel's own (GS₁)_R and Hottel 1974: no open copy found |
| H2–H4 combustion | equilibrium products at the local λ; enthalpy; CO and H₂ below λ 1 | Cantera, GRI-Mech 3.0 thermo (ADR 0012) |
| H5 radiation between faces | view factors of any chamber, with the setting and bag walls in the way; the grey enclosure | `radiation.py`; `radiation-exchange.md` §1–3 |
| H6 gas radiation | emission and absorption of CO₂ and H₂O between the gas and each face | Hottel's framework (Lienhard §10.5); a WSGG set |
| H7 hot emissivities | each face's material at its temperature | `radiation-exchange.md` §5 |
| H8 walls | 1-D transient, k(T), c_p(T), per face | v1's `TransientWall` (ADR 0015) |
| H9 ground | 2-D transient soil under the floor | Kiva's method (`energyplus-review.md` §5) |
| H10 ware | a node per zone with c_p(T) and its lag | heat review #1 |
| H11 heat input | burners sized; elements; wood stoked within the air the draft allows | Olsen ch. 8; Kanthal |
| H12 draft and air | the pressure balance round the gas path | Moody, Idelchik |
| H13 openings | spy holes and flues as surfaces | `radiation-exchange.md` §1.3 |
| Target time | the input that reaches the cone at a time, or the time at an input | the problem set §2.2 |

## 2. The candidates at a glance

From the PyPI JSON API, 2026-11-10 (Run, `pypi_facts.py`); "3.14 wheels" means CPython 3.14,
abi3 or pure wheels for Linux x86-64 / macOS / Windows amd64.

| Package | Version (released) | Licence | 3.14 wheels L/M/W | Largest wheel | Run here |
|---|---|---|---|---|---|
| SciPy (`solve_ivp`, `root`, `brentq`) | 1.18.1 (2026-08-21) | BSD-3 | yes/yes/yes | 37.5 MB | yes (already locked) |
| Cantera | 3.2.0 (2025-11-18) | BSD-3 | yes/yes/yes | 19.3 MB (62 MB installed) | yes (already locked) |
| scikit-sundae (SUNDIALS IDA, CVODE) | 1.2.0 (2026-10-16) | BSD-3; bundles SUNDIALS, SuperLU_MT, OpenBLAS and LAPACK, each BSD-3 (Run: its `LICENSES_bundled`) | yes/yes/yes | 20.8 MB; needs only NumPy and SciPy | yes |
| scikits-odes | 3.1.1 (2025-01-12) | BSD | no | – | no |
| assimulo | 3.0 (2018-12-15) | LGPL | no | – | no |
| CasADi | 3.8.2 (2026-10-27) | LGPL-3 | yes/yes/yes | 93.2 MB | no |
| Pyomo | 6.10.1 (2026-06-04) | BSD-3 | yes | 4.6 MB (solvers apart) | no |
| diffrax (JAX) | 0.7.2 (2026-02-18) | Apache-2.0 | yes (JAX 0.12) | 0.2 MB + JAX | no |
| numba | 0.68.1 (2026-10-27) | BSD | yes/yes/yes | 3.9 MB + llvmlite; caps NumPy < 2.6 | no |
| scikit-fem | 12.0.2 (2026-06-05) | BSD-3 | pure | 0.2 MB | yes |
| FiPy | 4.0.3 (2026-06-18) | field empty (NIST, from memory) | pure | 0.4 MB; needs matplotlib, typer | no |
| py-pde | 0.60.0 (2026-10-15) | MIT | pure | 0.5 MB; needs numba, sympy, matplotlib | no |
| pyfvtool | 0.6.1 (2026-09-01) | MIT | pure | 0.1 MB; needs matplotlib | no |
| heatrapy | 2.1.1 (2026-02-27) | MIT | pure | pins numpy==2.4.2, matplotlib==3.10.8 | no (`heat-libraries.md` §8) |
| trimesh | 5.2.0 (2026-10-24) | MIT | pure | 0.8 MB; needs only NumPy | yes |
| embreex (Embree 4) | 4.4.0.post1 (2026-10-21) | BSD-style wrapper licence ("Copyright (c) 2015, Anthony Scopatz", Run: its `LICENSE`); Embree itself Apache-2.0 (`tool-triples.md` §6) | yes/yes/yes | 14.6 MB | yes |
| pyViewFactor | 1.1.0 (2026-05-25) | MIT | pure | needs numba, pyvista (VTK) | earlier (`tool-triples.md` §3) |
| Open3D (Embree ray casting) | 0.20.0 (2026-09-16) | MIT | yes/yes/yes | **392 MB** (Linux); needs dash, flask, ipywidgets | no |
| pyembree | 0.2.11 (2022) | BSD | no (Python < 3.9) | – | no |
| View3D, pyview3d, viewfactor, radiosity | – | – | not on PyPI | – | – |
| radis | 0.17.1 (2026-08-12) | LGPL-3 | pure | 6.1 MB + 36 dependencies (astropy, astroquery, h5py, lmfit, matplotlib, …) | earlier (install only) |
| hitran-api (HAPI) | 1.3.0.0 (2026-01-13) | MIT | pure | 1.3 MB | no |
| radcal, pyradcal, wsgg, wsggpy, pywsgg | – | – | not on PyPI | – | – |
| exo_k | 1.3.2 (2026-09-04) | GPL-3.0-only | pure | needs astropy, netCDF4, numba | no |
| fluids | 1.3.1 (2026-06-23) | MIT | pure | 0.6 MB | yes |
| ht | 1.2.0 (2025-10-26) | MIT | pure | 0.8 MB (a dev dependency today) | yes |
| thermo / chemicals | 0.6.1 / 1.5.2 | MIT | pure | 6.4 / 22.3 MB | no (`tool-triples.md` §6) |

## 3. The firing in time, and the zones (H1)

### 3.1 v1's step pattern, extended to zones (Run)

`TransientWall` (`thermal/transient.py`) makes each step linear by lagging k, c_p and h, so the
heat into a wall's hot face over a step is affine in that face's temperature, a + b·T (Read; the
docstring and `heat_in_line`). That turns a zone model into one small nonlinear solve per step:
the unknowns are the gas temperature, each face's hot-face temperature and the ware's
temperature (or, following a schedule, the fuel rate), and each row is a face's balance
(wall uptake = radiation + convection in), the ware's (enthalpy change = heat in) and the gas's
(fuel heat = flue enthalpy + heat to the solids + radiation out of the openings).

In `chain_fastfire.py` (Run): six walls, the setting and three openings, 30 s steps, SciPy
`root` (hybr) each step: 580 steps of the fast-fire's 4 h 50 min log in 1.4–2.5 s, the firing's
energy balance closing to 1e-9 MJ; converged in the step (60 → 5 s moves cone 10 from 0.800 to
0.781 h). It failed once: holding the setting to the log's 190 °C five minutes in asks for more
than any gas temperature gives, and hybr stalled; a schedule mode needs a guard for that. v2
would write the zone rows, the state and the stepping (~150–250 lines). The same chain on IDA
(`chain_ida.py`, 155 unknowns) agrees to 0.1 % and runs a firing in 0.3–1.0 s with a transparent
gas and 0.7–2.9 s with Bordbar's WSGG set (`thermal-combinations.md` §4). Held to a piecewise-linear
schedule at rtol 1e-6, IDA failed on a kink (after 6 and 325 s): it must be stopped and restarted
at each breakpoint.

### 3.2 The three integrators on one reduced kiln (Run)

`integrator_probe.py`, test inputs throughout (it tests integrators, not kilns): one 4½ in K-23
wall in 24 cells (library k(T)), a 55 kg ware node (v1's fireclay c_p(T)), a gas zone on 80 kW
with a grey gas ε 0.2, the wall–ware exchange as an enclosed body, still air outside. The gas, the
hot face and the shell are algebraic; the cells and the ware differential. The event: the ware at
1285 °C. Reference: IDA at rtol 1e-9, 0.7642 h.

| Method | Event error | Run | Function calls |
|---|---|---|---|
| fixed-step backward Euler, a `root` per step (§3.1's pattern), dt 120 / 60 / 30 / 15 s | +45.7 / +22.5 / +11.2 / +5.6 s (first order: 0.4 % at 30 s) | 0.06 / 0.11 / 0.22 / 0.43 s | 880–6,379 residuals |
| SciPy `solve_ivp` BDF, rtol 1e-4 / 1e-6, the algebraic unknowns solved inside the right-hand side | +0.2 / −0.0 s | 0.07 / 0.17 s | 188 / 488 (each a 3-unknown `root`) |
| SciPy `solve_ivp` LSODA, rtol 1e-4 / 1e-6 | −0.1 / 0.0 s | 0.07 / 0.15 s | 243 / 466 |
| SUNDIALS IDA (scikit-sundae), banded, rtol 1e-4 / 1e-6 | −0.3 / −0.0 s | **0.02 / 0.04 s** | 309 / 588 residuals |

- All three are fast enough for a desktop. Like for like, **IDA is the fastest at the same
  accuracy** (it and `solve_ivp` both land within 0.3 s; the fixed step needs 15 s steps to come
  within 6 s), and it takes the model as it stands: no nested solve, events with direction and
  terminal flags, consistent initial values computed for it.
- The step pattern's error is first order in the step, on top of the lagged-property error that
  `energyplus-review.md` §7 #4 wanted a Picard pass for. Inside IDA the properties are iterated
  with everything else, so that pass isn't needed.
- `solve_ivp` needs no new package and is within 0.2 s here, but every right-hand side solves the
  algebraic part afresh; with a zone model's ten or more algebraic unknowns a zone, that grows.

### 3.3 scikit-sundae (SUNDIALS IDA and CVODE)

What it is (Read, the package's docstrings): Python bindings to SUNDIALS IDA (implicit DAEs) and
CVODE; a residual `f(t, y, yp, res)`; `algebraic_idx` for the algebraic unknowns;
`calc_initcond` for consistent starts; dense, banded (`lband`, `uband`), sparse (SuperLU_MT, with a
`sparsity` pattern that also groups the finite-difference Jacobian) and Krylov linear solvers;
events with terminal flags and directions; BSD-3, wheels for CPython 3.14 on all three systems,
needing only NumPy and SciPy (Run). Maintained by researchers at the US national laboratory that
runs NREL's site (Read, PyPI page); one listed maintainer, released 2026-10-16.

Verdict: **adopt IDA as the firing integrator**: a zone model is a DAE as it stands (gas and face
temperatures algebraic, wall cells and ware differential); the cone is an event. The walls then
enter as method-of-lines cells (v1's `TransientWall` physics re-expressed as rates, ~60 lines,
checked against `TransientWall` and its analytical cases). Fallback, with no new package:
`solve_ivp` (BDF) with the algebraic part solved inside the right-hand side, or §3.1's pattern.

### 3.4 Cantera reactor networks as zones (Run)

`cantera_wsr.py`:
- A zone with energy on, fed by a mass-flow controller, losing heat through a `Wall` whose heat
  flux is a Python function of the zone's own temperature: works; 60 s of zone time in 0.13 s,
  with 5,405 calls of the flux function. A firing of 4 h would call the function about 1.3
  million times, each a radiosity solve.
- What it would add is kinetics. §7.2 shows they don't change a zone's energy. Verdict: **not
  needed**; Cantera stays for equilibrium and properties, and its reactors as an offline check of
  the equilibrium assumption (§7.2). This settles `tool-triples.md` §6 #4 ("trial").

### 3.5 Not run

- **CasADi** (LGPL-3, 93 MB): optimal control with gradients. Only worth it if a target-time
  solve needs a whole schedule optimised; §12 shows SciPy's root-finding covers the questions the
  problem set asks. Defer (as `tool-triples.md` §6).
- **diffrax / JAX**: the zone model would have to be written in JAX. Reject.
- **Pyomo**: needs an outside solver for DAEs (from memory). Reject.
- **scikits-odes, assimulo**: no CPython 3.14 wheels (Run). Reject.

## 4. Conduction: walls (H8) and the ground (H9)

### 4.1 v1's `TransientWall` (Read; Run in the chain)

Already sound and validated (ADR 0015; `heat-libraries.md` §8; `energyplus-review.md` §2):
backward Euler, harmonic interfaces, k(T), c_p(T), area growing with depth. What v2 needs that
it lacks is only the hot face as an unknown, and the affine heat-in gives that without changing
it (§3.1). The Picard update of lagged properties (`energyplus-review.md` §7 #4) stays the one
proposed change. No package does this better (`heat-libraries.md` §8): **keep**.

### 4.2 scikit-fem for the ground (Run)

`soil_probe.py`: P1 triangles on a graded r–z mesh, 8 m by 8 m, the r-weighted forms of the
axisymmetric heat equation, backward Euler with cached LU factors; the heat out of the floor from
the reaction at the disc's nodes. Test inputs: a 1.2 m disc stepped by 1 K, dry mineral soil (k
1.0 W/(m·K), ρ 1500, c 1840; Lienhard Table A.2 via `thermal-properties.md` §8.2).

- 1,548 nodes, 1,471 steps to 30 days, 0.82 s.
- Steady, the 8 m domain gives S = 2.541 m against Incropera's 2D = 2.400 m for a half-space
  (+5.9 %, the finite domain).
- Q/(kΔT), metres:

| Time | 2-D, ground adiabatic round it | 2-D, ground losing to air (h 10) | slab A/√(παt) | §8.5's max(slab, 2D) | 1-D hemisphere (`TransientWall`) |
|---|---|---|---|---|---|
| 15 min | 39.12 | 39.36 | 35.34 | 35.34 (−9.7 %) | 32.99 (−15.7 %) |
| 1 h | 20.37 | 20.73 | 17.67 | 17.67 (−13.3 %) | 17.20 (−15.6 %) |
| 6 h | 9.49 | 10.16 | 7.21 | 7.21 (−24.0 %) | 8.39 (−11.6 %) |
| 12 h | 7.27 | 8.10 | 5.10 | 5.10 (−29.8 %) | 6.59 (−9.3 %) |
| 48 h | 4.70 | 5.92 | 2.55 | 2.55 (−45.7 %) | 4.47 (−4.8 %) |
| 72 h | 4.25 | 5.60 | 2.08 | 2.40 (−43.5 %) | 4.09 (−3.7 %) |
| 30 days | 2.98 | 5.00 | 0.66 | 2.40 (−19.3 %) | 2.93 (−1.4 %) |

Findings (Run, Derived):
- §8.5's h_g = max(slab, disc) **under-reads** the 2-D transient by 10–46 %; §8.5 called the max
  "a conservative choice that nothing found checks". The slab term is the floor's middle; the
  edge spreads heat sideways from the start, and the two add.
- The ground round the kiln matters for long firings: losing to the air, the 2-D loss is 11 %
  higher at 12 h and 26 % at 48 h than with Incropera's adiabatic surface, and twice it at steady
  state. An anagama fired for days on the ground sits in that range. Kiva's 2-D method
  (`energyplus-review.md` §5) represents it; a 1-D model can't.
- **A 1-D stand-in with no new package:** v1's `TransientWall` with area 2π(a + x)² and a = D/π,
  so its steady conductance 2πa equals the disc's 2D (Derived), runs in 0.17 s and reads 16 % low
  at 15 min, 9 % at 12 h and 1.4 % at 30 days. Its closed form, Q = 2πa kΔT[1 + a/√(παt)] (the
  sphere's constant-surface-temperature solution, halved; from memory), is within 6 % of the
  1-D wall at 15 min (the wall's 10 mm cells smear the first minutes) and within 1 % from 12 h.

Verdict: **scikit-fem for H9** (pure Python, 0.2 MB, BSD-3): the bridge is the mesh, the boundary
tags (floor, ground surface, far field), the coupling to the floor's zone each step and the
working (~150 lines). The 1-D hemisphere is the fallback if a 2-D solve is refused.

### 4.3 Not run

FiPy (finite volumes; matplotlib and typer as dependencies), py-pde (numba, sympy), pyfvtool
(matplotlib): each would take a 2-D diffusion solve as scikit-fem does, with heavier
dependencies; heatrapy pins NumPy 2.4.2 and has no analytical validation (`heat-libraries.md`
§8). Reject.

## 5. Radiation between faces (H5)

### 5.1 trimesh + embreex: Monte Carlo exchange (Run)

`mc_exchange.py`: emission points uniform by area on each named zone, cosine-weighted directions
into the gas, embree's first hit (trimesh's `ray_pyembree` backend), tallies per zone pair; from
the same rays, for a grey gas of absorption coefficient k, the direct exchange areas
s_i s_j(k) = A_i·mean(exp(−k·s)·[hit j]) and g s_i(k) = A_i − Σ_j s_i s_j(k) (Hottel's zone method
with one gas zone; Derived).

| Check | Result | Expected |
|---|---|---|
| Sphere D = 1 m (icosphere, 20,480 facets), gas absorptance of the wall's diffuse emission, kD = 0.1 / 1 / 3 | 0.06422 / 0.47149 / 0.82202 (±2–5e-4) | 0.06423 / 0.47152 / 0.82203: ε = 1 − 2[1 − (1 + a)e^(−a)]/a², a = kD (Derived: a chord at angle θ is D cos θ) |
| Sphere, mean chord | 0.66659 m | 4V/A of the polyhedron 0.66651 (Cauchy's formula; 2D/3 for a true sphere) |
| Unit cube, Σ A_i·(mean chord from i) | 3.9995 | 4V = 4 (the optically thin limit, Lienhard Table 10.4's L₀ = 2ℓ/3) |
| Unit cube, F against `radiation.box` (exact) | max error 2.7e-3 at 10⁵ rays a face, 7.8e-4 at 10⁶ | 1/√N |
| Half shadow: unit squares 1 m apart, a blocker just in front of half the receiver | 0.10001 ± 0.00021 | 0.09991 (half of 0.19982 by symmetry) |

- Cost: 10⁶ rays a face, six faces, 4.6 s; 10⁶ rays into 20,480 facets, 1.3 s. Memory is the
  rays in flight (chunks of 2×10⁵).
- **A fault in the glue, not the tools:** embree works in float32, so an origin offset of 1e-9 m
  is lost near coordinates of 0.5 m and half the rays hit their own triangle; 1e-6 m fixes it
  (the first run's numbers were off by half; Run).
- On the engine's own solids (`engine_mesh_mc.py`, `thermal-combinations.md` §2.3): the sprung
  arch's 52 OCCT triangles within 8.6e-4 of `radiation.covered` at 10⁶ rays a face (3.3 s); the
  obstructed chamber that pyViewFactor's centroid ray got wrong (rows off 1.5e-2) now with rows
  exact and its left and right walls equal within the noise (0.59455 / 0.59444).
- What it takes off v2's hands: ray–mesh intersection and the BVH, partial shadowing by the
  setting and bag walls, any chamber shape the engine can mesh, and the gas's path lengths for
  H6 at no extra cost. What v2 writes: sampling, tallies, closure, mapping zones to the engine's
  faces (~100 lines).
- Verdict: **adopt** (as `tool-triples.md` §6 #1 proposed; now checked). If embreex ever lacks a
  wheel for a new Python, trimesh falls back to its own NumPy intersector (`ray_triangle`, from
  memory: slower, same answers), so the engine wouldn't stop.

### 5.2 The closure correction (Run; Read)

Monte Carlo factors sum to 1 by row exactly (every ray lands somewhere) but aren't reciprocal.
On the cube (`mc_exchange.py` §D, against the exact factors):

| Correction | max error, 10⁶ rays a face | rms error |
|---|---|---|
| none | 7.8e-4 (reciprocity off by 7.6e-4) | 3.5e-4 |
| symmetric average of A_iF_ij only | 5.0e-4 (rows off by 3.7e-4) | 2.75e-4 |
| least change, weights S² (as `vfmesh.py`) | 5.0e-4 | 2.65e-4 |
| least change, weights ∝ the tally's variance (Derived) | 5.0e-4 | 2.65e-4 |
| symmetric scaling S_ij = x_i x_j S⁰_ij | 5.0e-4 | 2.65e-4 |

All three close summation and reciprocity to round-off and all three cut the rms error by about
a quarter here. Where factors differ widely in size they separate a little: the obstructed
chamber of §2.3 in `thermal-combinations.md` (factors 0.0015–0.594), ten independent runs at 10⁵
rays a face against a reference at 4×10⁶ (`closure_probe.py`, Run):

| Correction | rms error | max error | max relative error (F > 1e-3) |
|---|---|---|---|
| none | 9.2e-4 | 2.7e-3 | 8.2 % |
| symmetric average only | 9.0e-4 | 3.2e-3 | 4.0 % |
| least change, weights S² | 7.2e-4 | 2.5e-3 | 4.0 % |
| **least change, weights ∝ the tally's variance** | **6.7e-4** | **2.2e-3** | 3.9 % |
| symmetric scaling | 7.2e-4 | 2.5e-3 | 3.8 % |

The variance-weighted least change is best, by a little: it trusts each pair's estimate in
proportion to how many rays made it, the idea behind Loehrke et al. 1995's reciprocity weighting
and Daun et al. 2005's maximum likelihood (sources below). Every closure halves the worst
relative error.

**Why the closure must be exact: a source (Read).** R. Clarksean and C. Solbrig, "Minimization
of the Effect of Errors in Approximate Radiation View Factors", Argonne National Laboratory,
6th Int. Topical Meeting on Nuclear Reactor Thermal Hydraulics, Grenoble, 1993 (OSTI 10188074,
an open US-government report; read in the literature agent's download): for N surfaces only
N(N − 1)/2 view factors are independent once summation (their eq. 4) and reciprocity (eq. 5) are
imposed; ±20 % error in the independent ones moved their temperatures by ±4 °C, less than ±20 % in
the emissivities did (±5 °C); but with summation and reciprocity broken, the wall's heat flux was
off by over a factor of 2 (up to 3, their abstract). R. P. Taylor, R. Luck, B. K. Hodge and
W. G. Steele (Mississippi State University), "Uncertainty analysis of diffuse-gray radiation
enclosure problems: a hypersensitive case study" (NASA NTRS 19940019164, open; abstract Read),
found the same: an enclosure hypersensitive to its view factors "could be greatly reduced by
enforcing both closure and reciprocity". So v2 enforces both to round-off, as
`radiation.Enclosure` already demands (1e-9). Their way, estimating the independent factors and
deriving the rest, throws half the Monte Carlo estimates away; a least-change correction uses
them all (Derived), and §5.2's table shows it gains accuracy.

**The least-change correction: Larsen & Howell 1986, as restated in an open thesis (Read).**
W. O. Monnaemang, *A zonal model for radiation heat transfer in coal-fired boiler furnaces*, MSc
thesis, University of Cape Town, 2015, §3.2.3, eqs. 3.33–3.44 (pp. 30–33, read on the rendered
pages), after J. V. Larsen and J. R. Howell, J. Heat Transfer 108 (1986) 239–242 (not read):
- the direct exchange areas x_ij (surface and gas zones together) are adjusted to x′_ij so that
  every row and column sums to c_i (A_i for a surface, 4KV_i for a gas zone), minimising
  H = Σ_i Σ_j (x′_ij − x_ij)²/(2w_ij);
- the solution is x′_ij = x_ij + w_ij(λ_i + λ_j), with [R]λ = δ, r_ij = w_ij (i ≠ j),
  r_ii = w_ii + Σ_j w_ij, δ_i = c_i − Σ_j x_ij;
- w_ij = 1 can drive zero areas negative; w_ij = x_ij² adjusts each in proportion to its size.

That is exactly the probes' "least change, weights S²" (`vfmesh.py`'s `smooth`, written from
memory before this source was found, now checked against it), and the variance weights are a
choice of Larsen & Howell's "arbitrary weighting factors" w_ij. (The thesis prints its eq. 3.36 as
g_i − g*_i, but its expansion and derivative use g_i + g*_i: a misprint.)

**The forms made for Monte Carlo factors** (a second literature agent, its downloads in
`scratch/thermal-survey/lit-zone/`; Read, secondary, in B. Frangi's open thesis, arXiv:2511.04277,
§3.5.3–3.5.5, pp. 50–56):
- Loehrke, Dolaghan & Burns 1995 (J. Heat Transfer 117:524; closed): reciprocity by **variance
  weighting**, η̂_ij = κη_ij + (1 − κ)η_ji with κ = σ²_ji/(σ²_ij + σ²_ji) and
  σ_ij = zΩ_i√((1 − F_ij)/(N_i F_ij)), N_i the rays from surface i; closure after by
  F_ii = 1 − Σ, which can go negative;
- Larsen & Howell with separate row and column multipliers, and weights ω_ij = η_ij, which Vueghs
  (2009, a restricted thesis, via Frangi) found best;
- Daun, Morton & Howell 2005 (J. Heat Transfer 127:1124): the maximum-likelihood factors under
  reciprocity, summation and non-negativity (abstract Read; its algorithm not found);
- Taylor & Luck 1995 (JTHT 9:660): weighted least squares "vastly superior" (abstract Read);
  Murty & Murty 1991: the weights' choice "immaterial" to their zone results (Snippet).

So **adopt Larsen & Howell's smoothing with variance weights**: it is Loehrke's variance idea
inside Larsen & Howell's exact closure, never makes a negative factor, and was the most accurate
of the five tried here; the published alternatives (w = x², w = x) are within 1e-4 of it on these
chambers, as Murty & Murty found. It closes the gas zone's row too (c = 4KV) when the gas radiates.

### 5.3 Monte Carlo against the contour kernel

| | Contour kernel (pyViewFactor's SA-30, or its NumPy copy; `tool-triples.md` §3) | Monte Carlo (trimesh + embreex; §5.1) |
|---|---|---|
| Accuracy | exact for planar polygons to the quadrature: 4.1e-9 on a box; curved faces set by the mesh's chords (9.9e-4 on the arch, all of it the chord-short area) | noise 1/√N: 2.7e-3 at 10⁵ rays a face, 7.8e-4 at 10⁶; no bias found (sphere to 1e-5, Cauchy's 4V/A) |
| Obstruction | none in the NumPy copy; pyViewFactor's one centroid ray: rows off 1.5–4.7e-2 | exact shadowing at every ray; rows exact, the obstructed chamber symmetric to the noise |
| Gas in the way | no (transparent only) | the path lengths come with every hit, so the grey-gas exchange areas cost nothing more |
| Cost | grows as facets²: 4.7 s (numba) or 32.6 s (NumPy) at 1252 facets | grows with rays, hardly with facets: 3.3 s for 52 triangles, 1.3 s for 10⁶ rays into 20,480 |
| Weight | NumPy copy ~70 lines; pyViewFactor brings VTK and numba (220 MB) | trimesh 0.8 MB + embreex 14.6 MB |

Verdict: rays for the engine; the kernel and `radiation.py`'s closed forms as the test oracles.

### 5.4 Not adopted

- **The contour kernel** (pyViewFactor's, copied as NumPy, `tool-triples.md` §3): exact for
  unobstructed planar pairs; keep it as a test oracle beside `radiation.py`'s closed forms.
- **Open3D** (Embree inside): a 392 MB Linux wheel with web-app dependencies. Reject.
- **pyembree**: no wheel since Python 3.8. Reject.
- **numba** to speed the contour kernel: caps the repo's NumPy below 2.6 (Run). Not needed once
  Monte Carlo carries the obstructed cases.
- **View3D** (Walton, NIST): not on PyPI (Run). NISTIR 6925 (Walton 2002, pp. 8–9; Read by the
  literature agent): it handles obstruction by projecting each obstruction's shadow onto the
  receiving surface's plane and running the contour integral round the unshaded edges, with
  adaptive 9/16-point rules (7/13 on triangles), convex polygons only. The NIST original is public
  domain; the maintained versions are a SourceForge port (LGPLv2 / public domain, last updated
  2016) and DeGraw's v4.0 (GPL-3.0; v3.2 was bundled with EnergyPlus); no Python wrapper. A C
  program and GPL forks, for what Monte Carlo already does here: a cross-check at most.

## 6. Gas radiation (H6)

The zone method needs, per grey gas, only the direct exchange areas, which §5.1's rays give for
any k at once (each pair's path-length quantiles are kept, so a new k is a sum, not a new ray
cast; Run). What it needs from outside is a set of grey gases: a published WSGG set. Cantera's
Planck-mean grey gas stays rejected (`cantera-tespy-review.md` §5).

### 6.1 Published WSGG sets, and where their coefficients can be read

Searched 2026-11-10 (a literature agent's report, its downloads in
`scratch/thermal-survey/lit-gas/`; the two sets used below were then read again here).

| Set | Basis | Range | Where the numbers can be read | Mark |
|---|---|---|---|---|
| **Bordbar, Węcel & Hyppänen 2014**, Combust. Flame 161:2435 | HITEMP-2010 line by line; 4 grey gases + a window; one continuous fit in MR = x_H₂O/x_CO₂ | MR 0.01–4; 300 (or 500, sources differ) to 2400 K; pL 0.01–60 atm·m (Ehlmé et al. 2025 Table 1; Selhorst 2020 Table 1.1) | **NIST FDS `Source/radi.f90` lines 3222–3271** (commit f6cc57b; NIST's notice, Read: not subject to US copyright, use and changes allowed if the notice is kept, NIST acknowledged and changes marked; the paper cited at lines 3222–3223) and **BYU RadLib `rad_wsgg.cc`** (MIT): the two agree on all 168 values except three that differ by 1e-7. The paper isn't open (its repository blocks scripted access) | **Read** (FDS's lines and functions, here) |
| Bordbar, Fraga & Hostikka 2020, ICHMT 110:104400 (pure CO₂ and H₂O ends) | HITEMP-2010 LBL | 300–2400 K, 0.01–60 m | accepted manuscript, Aalto (CC BY-NC-ND); FDS and RadLib carry a different pure-species set; the version of record is unread | Read (agent) |
| **Dorigon et al. 2013**, IJHMT 64:863 | HITEMP-2010 LBL; 4 grey gases with fixed k | MR 1 and 2; 400–2500 K; pL 0.001–10 atm·m | ENCIT 2012 paper 118, Tables 1–2 (© ABCM); Dorigon's 2012 MSc (UFRGS, CC BY-NC-SA 2.5 BR) | **Read** (ENCIT tables, here) |
| Cassol et al. 2014, IJHMT 79:796 | HITEMP-2010; H₂O and CO₂ apart, combined by superposition (25 grey gases) | 400–2500 K | Brittes 2015 and Fonseca 2022 theses (UFRGS, CC BY-NC-SA); its soot table not found open | Read (agent) |
| Smith, Shen & Friedman 1982, J. Heat Transfer 104:602 | exponential wide-band model | 600–2400 K; pL 0.001–10 atm·m | Marzouk & Huckaby, arXiv:2411.18467 (CC BY), Table 7 | Read (agent) |
| Sadeghi, Hostikka, Fraga & Bordbar 2021, Fire Safety J. 125:103420 | soot WSGG, and a grey soot fit (eq. 24) | 300–3000 K | the paper (CC BY), Table B9 | Read (agent) |
| Ehlmé et al. 2025, ACS Omega 10:2978 | statistical narrow band, to 5000 K | MR 0.4–4 | CC BY; reads 20–50 % low at L ≤ 0.1 m in the agent's check | Read (agent); avoid |
| Alberti, Weber & Mancini 2015, 2016, 2018 | LBL **look-up tables**, not fits | 300–3000 K; to 6000 bar·cm | supplementary spreadsheets, free from Elsevier's server (1.5, 1.7 and 8.5 MB; no licence stated); the papers are paywalled | Read (agent) |
| Lienhard & Lienhard 2024, §10.5 | Alberti's charts | – | charts only (Figs 10.22–10.25), no coded correlation | Read (agent) |

### 6.2 Checks (Run, `wsgg_check.py`)

- **Lienhard's Example 10.11** (CO₂ 0.2 atm in N₂, L₀ 0.4 m, 1200 °C; ε_g = 0.085 read off Alberti's
  chart): Bordbar's pure-CO₂ set as FDS codes it gives 0.0816 (−4 %).
- **Two independent HITEMP fits against each other**, MR 1 and 2, L 0.1–3 m, 600–1600 K: Bordbar
  2014 reads +0.1 to +13 % above Dorigon 2013, most at 600 K and long paths.
- **Against Alberti's 2018 LBL tables** (the agent's check, L 0.05–0.3 m, 600–1800 K, the overlap
  correction left out): Dorigon −1 to +10 %, Bordbar −1 to +19 % (worst at 600 K), Cassol +2 to
  +13 %, Smith −7 to +34 %.
- The weights stay positive and sum below 1 over 400–2400 K for both sets.

So the published sets carry about ±10 % (up to 19 % at 600 K) against line-by-line: v2 carries it
as a band, running two sets (Bordbar and Dorigon), as ADR 0017 decision 4 asks for a quantity
no source fixes closer.

### 6.3 Line by line: radis or HAPI with HITEMP (Read, agent)

- HITEMP H₂O (2010): 114,241,164 lines, 3.2 GB compressed; CO₂ (2024): 326,260,084 lines,
  6.0 GB compressed; about 18 and 52 GB uncompressed at 160 characters a line (Derived). **A
  HITRANonline login is required**: every HITEMP file URL redirects to the login page.
- radis's `fetch_hitemp` logs in with `HITRAN_EMAIL` and `HITRAN_PASSWORD` (or a prompt) and keeps
  the credentials encrypted in `~/radis.json`; it then downloads into `~/.radisdb/hitemp`.
- Verdict: the owner allows a fit of our own, but it would cost a HITRAN account, about 10 GB of
  downloads and radis's 36 dependencies, to make what Bordbar 2014 already is (a HITEMP-2010 LBL
  fit). **Not needed.** Alberti's spreadsheets (8.5 MB) are the line-by-line reference for tests.

### 6.4 Soot

Sadeghi et al. 2021 (CC BY) give a soot WSGG and a grey soot fit; FDS and RadLib carry grey forms
proportional to the soot volume fraction and T. The physics is there; a kiln flame's soot volume
fraction is not, in any source read. Carried as a question (`thermal-combinations.md`).

### 6.5 The zone method against the mean beam length (Run)

Lienhard's shortcut (eq. 10.58) gives a gas one path length, L = 4V/A or 3.6V/A "for a strongly
absorbing gas", and calls it "simple but crude" (`radiation-exchange.md` §6). The rays give the
exact grey-gas exchange instead (`mbl_check.py`; black walls, 10⁶ rays). Gas emissivity to the
walls, ε = Σ g s_i / A:

| k (1/m) | unit cube, exact | L = 4V/A | L = 3.6V/A | fast-fire box (0.69 × 0.69 × 0.91 m), exact | 4V/A | 3.6V/A |
|---|---|---|---|---|---|---|
| 0.05 | 0.0326 | +0.5 % | −9.4 % | 0.0245 | +0.4 % | −9.5 % |
| 0.5 | 0.2697 | +5.1 % | −3.9 % | 0.2123 | +4.0 % | −5.3 % |
| 2 | 0.6469 | +13.8 % | +8.0 % | 0.5641 | +11.9 % | +5.0 % |
| 5 | 0.8424 | +14.5 % | +12.8 % | 0.7946 | +15.5 % | +12.5 % |

The mean chord, 4V/A, can only overstate the exchange (1 − e^(−kL) is concave in L: Jensen's
inequality on the spread of chords, Derived), by up to 15 % across the k a kiln's grey gases span
(Bordbar's κ_i × 0.33 atm gives k ≈ 0.02–26 m⁻¹); 3.6V/A trades that for −10 % at small k. The rays
remove the error at no extra cost; the mean beam length stays a hand check.

### 6.6 Verdict

**Adopt Bordbar 2014** (cited to the paper; coefficients as FDS and RadLib carry them, the FDS
notice kept) for the zone method, with **Dorigon 2013** as the second set for the band, and
Alberti's tables as the test reference. Bridge: the set as data and the weights function (~40
lines), the grey-gas radiosity solve (~60). In the chains, gas radiation is what lets the
reference kilns reach their firings (`thermal-combinations.md` §4).

## 7. Combustion (H2–H4)

### 7.1 Cantera's equilibrium (in use)

Keep, with the range guard `tool-triples.md` §2 asked for. Wood needs only the products'
enthalpies (`cantera-tespy-review.md` §2); the chain uses the same 50/6/44 C/H/O surrogate
(Pettersen 1984, still not read at the page).

### 7.2 Kinetics against equilibrium at kiln residence times (Run)

`cantera_wsr.py`, GRI-Mech 3.0, premixed at 300 K, test residence times. Derived residence time:
the fast-fire's chamber, about 0.43 m³ at 0.1 kg/s and 0.22 kg/m³, is about 1 s; a 36 ft³ gas kiln
on 63 kW is about 10 s.

- **Flame zone** (adiabatic well-stirred reactor): at τ = 1 s it is at HP equilibrium within 1 K
  (propane λ 1.15: 2139.4 against 2138.4 K); at 0.01 s it is 54–91 K below.
- **Chamber zone** held at T_g and fed with the flame zone's products, the heat still to be
  released on reaching TP equilibrium at T_g, % of the fuel's heat:

| Fuel, λ | 700 K | 1000 K | 1300 K | 1600 K |
|---|---|---|---|---|
| propane 1.15, τ 0.5–10 s | 0.12–0.22 | 0.11–0.17 | 0.08–0.12 | 0.01–0.05 |
| propane 0.9 (reduction) | 1.97–2.08 | 0.18–0.49 | 0.03–0.12 | 0.05–0.17 |
| methane 1.15 | 0.07–0.15 | 0.06–0.11 | 0.05–0.07 | −0.03–0.00 |

- In reduction below about 1000 K the CO freezes: 3.1 % in the zone against 0.29 % at
  equilibrium at 700 K. Kilns are put into reduction near 900–1000 °C (`combustion.py`'s
  `REDUCTION_AIR` note), where the difference is under 0.5 %.

Verdict: equilibrium per zone is enough for the heat model (ADR 0017's "equilibrium only" stands
on evidence now); Cantera's kinetics are an **offline check** of that, as here. GRI-Mech's own
optimisation range (1000–2500 K, natural gas; from memory in `cantera-tespy-review.md` §1) still
needs quoting before any kinetic result is used in the engine.

## 8. The draft and the gas path (H12)

- **fluids** (Run here and in `tool-triples.md` §2): Colebrook friction; entrances, exits,
  contractions, expansions, bends; bar grates (Blevins); and `packed_bed` with 14 laws (Ergun;
  Idelchik's, valid for voidage 0.3–0.8 and 0.001 < Re < 1000; KTA; …) that would take a char bed's
  resistance once its particle size and voidage are sourced (Read, `fluids_rough.py`). Its
  roughness tables are Idelchik's (the "HHR" set) for concrete and cement channels, 0.05–17 mm;
  **no brick, firebrick or masonry entry** (Run). Brick roughness stays a stated band until a
  source gives it.
- **No package has rectangular-section fittings.** fluids' elbows and contractions are for round
  pipes; ht has the rectangular laminar Nusselt number (Shah & London) only. Idelchik's diagrams
  are the source (the 1966 US AEC translation, AEC-tr-6630, an open government document);
  *pending*: no open copy was reached in this run. Leads (Snippet only): a scan of the NTIS
  reproduction on Scribd under the NRC ADAMS number ML12209A041 (the NRC's own URL returned 403),
  and CERN's catalogue record 102966. No OSTI, archive.org or HathiTrust full view was found, so
  no diagram numbers are recorded.
- **ht** has no impinging-jet module (Run: none in its catalog); a burner jet on the ware has no
  correlation here.

## 9. Convection inside and out

- Outside: v1's `surface.py` (Churchill–Chu, Lloyd–Moran, Jaffer) stays; ht's other forms are
  the uncertainty (`heat-libraries.md` §2).
- Inside: radiation dominates above about 1000 °C (`2026-11-physics-review-heat.md` #10), but
  early in a firing convection carries much of the heat to the ware. ht has flat-plate (Baehr–
  Stephan laminar; Schlichting, Kreith turbulent), tube-bank (Zukauskas, ESDU) and packed-bed
  (Wakao–Kagei, Achenbach) forms (Run, catalog). The chain used the laminar flat plate at the mean
  downdraft velocity, 5–10 W/(m²·K) (a test choice). A setting is neither a plate nor a tube bank;
  which form fits a kiln setting is unsourced. Verdict: **ht as a runtime dependency** (it is a
  dev dependency today), named correlations only (`tool-triples.md` §2's selector fault).

## 10. Ware and setting (H10)

- The setting's radiative role is taken by §5.1 (an obstruction with its own faces, Run in the
  chain as one box).
- Its heat capacity: v1's ware curve (800 J/(kg·K) at 24 °C, then VDI's fireclay points), used in
  the chain as a lumped node. A thick shelf or saggar could take a `TransientWall` heated on both
  faces; no package is needed.
- Its flow resistance and the convection through it: no source (problem set §2.2). fluids'
  packed-bed and ht's tube-bank forms are candidates only once a source says a setting behaves as
  one.

## 11. Burners and wood fuel beds (H11)

- Burners: no package takes venturi entrainment or burner sizing. fluids has in-pipe flow-meter
  discharge coefficients (ISO 5167 orifices, nozzles), the critical-flow check and a liquid jet
  pump (Run, its catalog); nothing for a free gas jet or the primary air a venturi draws. v1
  already sizes orifices by Olsen's equation (p.216); decision 13's burner charts (the MR-750 and
  MR-100 sheets) are data, not software.
- Wood: the stoker sets the fuel; the draft sets the most air (problem set §2.2). The chain takes
  the air from fluids' pressure balance and burns the wood at λ (Run, `thermal-combinations.md`
  §4). The bed's own resistance (fluids' packed-bed laws) and the grate's heat-release limit need
  data no source here gives.

## 12. Target-time solves

The questions (problem set §2.2): at a fixed input, how long to the cone; for a target time, what
input. The first is one firing that stops at the cone: IDA's terminal event (§3.2: located within
0.3 s). The second is a root on the input (a burner rating, a stoking rate, a damper setting)
around that firing: SciPy `brentq`, as v1's `target.py` already does for v1's simulation. A
firing of the reduced kiln costs 0.02–0.04 s (Run), so a 20-evaluation root costs about a second;
the fast-fire chain's firing costs 1–3 s with the step pattern. Run on a whole chain: the input
that brings Olsen's 36 ft³ cross-draft to cone 10 in 15 h, a `brentq` over full firings at 60 s
steps, took 66 s (`crossdraft_target.py`; `thermal-combinations.md` §4.2); on IDA each firing
would be a few seconds. Verdict: **SciPy root-finding around IDA**; CasADi only if a whole
schedule is ever to be optimised (§3.5). A stoked kiln's
time is the stoker's choice within the draft's air (problem set §2.2), so its "target time" is
the check that the draft-limited fire reaches the cone sooner than the documented firing
(`thermal-combinations.md` §4).

## 13. Whole-furnace tools

- **DOE's MEASUR / ORNL AMO-Tools-Suite** (github.com/ORNL-AMO/AMO-Tools-Suite; Read by the
  literature agent): C++ with Node and WebAssembly bindings, no Python, archived in favour of
  MEASUR-Tools-Suite; a custom permissive licence (UT-Battelle, 2018). Its opening loss is
  εσ(T_in⁴ − T_amb⁴)·A·F·(% open) with a thick-wall view factor F read off curves defined
  elsewhere, and its leakage loss is an orifice flow through the opening at the furnace's
  pressure (1655·C·A·√(Δp/SG) cfh); **neither cites a source**, and a code comment says one
  doesn't reproduce its own documentation. So not a source (ADR 0009) and not a library. For H13
  the rays already give a thick-walled hole's view exactly (the hole's tunnel in the mesh); a leak
  through an opening is a draft question for the gas path, sized by fluids' orifice forms once a
  source gives the coefficient.
- **View3D**: §5.4.

Not proposed: FDS, OpenFOAM and other CFD (flame shape and burner aerodynamics
are outside v2, ADR 0017; FDS's source is used only as the readable copy of Bordbar's
coefficients), EnergyPlus and Kiva as libraries (`energyplus-review.md`).

## Sources

Packages (Run, Read):
- PyPI JSON API, https://pypi.org/pypi/NAME/json, read 2026-11-10; licence files of the installed
  wheels (`licences.py`, `bundled.py`).
- scikit-sundae 1.2.0 (BSD-3), docstrings of `sksundae.ida.IDA`; SUNDIALS: A. C. Hindmarsh et al.,
  ACM TOMS 31 (2005), doi:10.1145/1089014.1089020; D. J. Gardner et al., ACM TOMS 48 (2022),
  doi:10.1145/3539801.
- trimesh 5.2.0 (MIT, M. Dawson-Haggerty); embreex 4.4.0.post1 (BSD-style, A. Scopatz; Embree,
  Apache-2.0); scikit-fem 12.0.2 (BSD-3); fluids 1.3.1 and ht 1.2.0 (MIT, C. Bell): docstrings read;
  Idelchik, *Flow Resistance*, Hemisphere 1989, as cited in `fluids.packed_bed.Idelchik`.
- Cantera 3.2.0 (BSD-3), GRI-Mech 3.0 (Smith, Golden, Frenklach et al. 1999).

Gas radiation (§6; the literature agent's downloads in `scratch/thermal-survey/lit-gas/`):
- H. Bordbar, G. Węcel, T. Hyppänen, "A line by line based weighted sum of gray gases model for
  inhomogeneous CO2–H2O mixture in oxy-fired combustion", Combust. Flame 161 (2014) 2435–2445 (not
  read; paywalled). Coefficients **Read** in NIST's Fire Dynamics Simulator,
  https://github.com/firemodels/fds/blob/f6cc57b974144e732a8b38125a84ce4a073501f1/Source/radi.f90,
  lines 3222–3271 (arrays) and 5082–5179 (`KAPPA_WSGG`, `A_WSGG`); FDS's NIST notice in
  `LICENSE.md`; and in RadLib (BYU, MIT), https://github.com/BYUignite/radlib,
  `src/c++/rad_wsgg.cc` lines 14–54 (agent).
- M. H. Bordbar, G. C. Fraga, S. Hostikka, "An extended weighted-sum-of-gray-gases model to account
  for all CO2-H2O molar fraction ratios in thermal radiation", Int. Commun. Heat Mass Transf. 110
  (2020) 104400; accepted manuscript (CC BY-NC-ND),
  https://acris.aalto.fi/ws/portalfiles/portal/39751900/ENG_Bordbar_et_al_An_extended_weighted_sum_of_gray_gases_model_ICHMT.pdf
  (agent).
- L. J. Dorigon, M. Galarça, F. H. R. França, ENCIT 2012 paper 118, Tables 1–2 (**Read**),
  https://www.abcm.org.br/anais/encit/2012/links/pdf/ENCIT2012-118.pdf; the journal version
  L. J. Dorigon et al., IJHMT 64 (2013) 863–873 (not read).
- F. Cassol et al., IJHMT 79 (2014) 796–806, via R. Brittes da Silva's 2015 PhD thesis (UFRGS,
  https://lume.ufrgs.br/bitstream/10183/114970/1/000955820.pdf) and Fonseca's 2022 thesis (agent).
- T. F. Smith, Z. F. Shen, J. N. Friedman, J. Heat Transfer 104 (1982) 602–608, via Marzouk &
  Huckaby, arXiv:2411.18467, Table 7 (agent).
- H. Sadeghi, S. Hostikka, G. C. Fraga, H. Bordbar, Fire Safety J. 125 (2021) 103420 (CC BY),
  Table B9 (agent).
- M. Alberti, R. Weber, M. Mancini: Combust. Flame 162 (2015) 597, 169 (2016) 141; JQSRT 205 (2018)
  230, 219 (2018); supplementary spreadsheets, e.g.
  https://ars.els-cdn.com/content/image/1-s2.0-S0022407318304618-mmc1.xlsx (agent).
- HITEMP, https://hitran.org/hitemp/ (**Read**, the saved page: line counts, sizes, login);
  radis 0.17.1, `radis/api/hitempapi.py` (agent).
- J. H. Lienhard IV and V, *A Heat Transfer Textbook*, 6th ed., v6.00, 2024, §10.5 pp. 586–594,
  Example 10.11, Table 10.4; Table A.2 (soil), via `radiation-exchange.md` and
  `thermal-properties.md`.

Radiation between faces and the zone method:
- W. O. Monnaemang, *A zonal model for radiation heat transfer in coal-fired boiler furnaces*, MSc
  thesis, University of Cape Town (supervisors P. G. Rousseau, L. Jestin), August 2015: §3.2,
  eqs. 3.11–3.14 (the zone method's balances, after Modest 2013) and §3.2.3, eqs. 3.33–3.44
  (Larsen & Howell's smoothing, read on the rendered pp. 32–33); open on UCT's repository, the
  copyright the author's (quotation with acknowledgement); the literature agent's download in
  `scratch/thermal-survey/lit-zone/`. Its primary sources not read: J. V. Larsen, J. R. Howell,
  J. Heat Transfer 108 (1986) 239–242; W. A. Lawson, IJHMT 38 (1995) 3109; H. C. Hottel,
  A. F. Sarofim, *Radiative Transfer*, 1967; M. F. Modest, *Radiative Heat Transfer*, 3rd ed., 2013.
- D. Latham, *Mathematical modelling of an industrial steam methane reformer*, MSc thesis,
  Queen's University, Kingston, Ontario, December 2008: pp. 24–26 (the Hottel zone method's
  balances and the well-stirred model, after D. Rhine and R. J. Tucker, *Modelling of Gas-Fired
  Furnaces and Boilers*, 1991, pp. 216, 244–257, not read) and eqs. 24–26 (a one-gas-zone cube
  furnace); Read in the text layer of the literature agent's download (open on Queen's
  repository).
- R. Clarksean, C. Solbrig, "Minimization of the Effect of Errors in Approximate Radiation View
  Factors", Argonne National Laboratory, presented at the 6th International Topical Meeting on
  Nuclear Reactor Thermal Hydraulics, Grenoble, 5–8 October 1993; OSTI 10188074 (Read, the
  literature agent's download in `scratch/thermal-survey/lit-zone/`).
- R. P. Taylor, R. Luck, B. K. Hodge, W. G. Steele, "Uncertainty analysis of diffuse-gray
  radiation enclosure problems: a hypersensitive case study", Mississippi State University; NASA
  NTRS 19940019164 (N94-23637); abstract Read (the same folder).
- B. Frangi, thesis, 2025, arXiv:2511.04277, §3.5.3–3.5.5, pp. 50–56 (open; Read by the
  literature agent): Larsen & Howell with separate multipliers and ω_ij = η_ij (Vueghs 2009),
  Loehrke, Dolaghan & Burns's variance weighting (J. Heat Transfer 117 (1995) 524–526, not read),
  ESARAD's triangulation, open-system variants.
- K. J. Daun, D. P. Morton, J. R. Howell, J. Heat Transfer 127 (2005) 1124–1128, and R. P. Taylor,
  R. Luck, JTHT 9 (1995) 660–666: abstracts only (via Crossref and OpenAlex).
- G. N. Walton, *Calculation of Obstructed View Factors by Adaptive Integration*, NISTIR 6925,
  2002, pp. 8–9, https://nvlpubs.nist.gov/nistpubs/Legacy/IR/nistir6925.pdf (Read by the literature
  agent); View3D's ports: sourceforge.net/projects/view3d, github.com/jasondegraw/View3D.
- ORNL AMO-Tools-Suite, github.com/ORNL-AMO/AMO-Tools-Suite, `OpeningLosses.cpp`,
  `LeakageLosses.cpp` (Read by the literature agent; the formulas to re-check against the files).
- G. T. Tsuyuki, "TRASYS Form Factor Matrix Normalization", Jet Propulsion Laboratory; NASA NTRS
  19930004203 (N93-13391); summary Read (the same folder): row sums within 0.05 of unity
  distributed among the nodes rather than lumped into the factors to space, which biased exterior
  temperatures by up to 7 °C in the hot case (the cold case's figure is unclear in the OCR).

Other:
- Incropera & DeWitt, Table 4.1 case 10, via `thermal-properties.md` §8.1.
- Olsen, *The Kiln Book*, 4th ed., p.139, p.143, p.226, p.309, via
  `core/tests/v2/reference_kilns.yaml` and `kiln-reference.md`.
