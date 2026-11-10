# Statics tools in pairs: what each takes off engine v2's hands

Surveyed 2026-11-09, after `statics-software.md`, on the user's question: is there a pair, tool X
with tool Y giving Z, that helps where neither would alone? No engine changes were made.

**The yardstick (the user, 2026-11-09):** "The ability of a tool or package to match any
particular rule or result is not important, since many of those are not valid conclusions. The
important evaluation is that there is a way to use the tool so this project does not need to
solve that part too. The engine rewrite is going to need to start over anyways, with the
reference kilns and published formulas as the basis." So each pair is judged by the part of the
problem it takes off v2's hands, and by what v2 would still write and own. The checks below
only show that a tool was driven correctly.

- Probes: `scratch/statics-combos/` (git-ignored, as the other surveys' probes are), in three
  folders: `arch-frame/`, `friction/` and `fela/`. Each folder has a `RESULTS.md`, and each
  script's docstring says how to run it.
- Extra packages came through `uv run --with` overlays (PyNiteFEA, scikit-fem, clarabel), or a
  CPython 3.13 side environment (`uv run --no-project --python 3.13 --with compas_cra`). The
  repo's environment wasn't touched.
- Machine as in `statics-software.md`. Times are wall-clock and single runs.
- Marks: **Run** (computed here), **Read** (read in the source), **Snippet** (a search extract
  only), **Derived** (worked here), "from memory".

## 0. Short answer

Two pairs help where the tools alone wouldn't. One pair that looked promising doesn't.

| Pair (X + Y → Z) | Takes off v2's hands | v2 would still write | Verdict |
|---|---|---|---|
| **PyNite + the arch's LP** (HiGHS), coupled by SciPy's bounded least squares → the hot thrust along a real frame, and the steel's stress | the frame's whole analysis (stiffness, member forces, deflections, tension-only rods), and every solve | the arch's LP, the frame built from the design, and the coupling (§2) | **proposed**: neither alone gives the thrust's spread or the frame's share of the growth |
| **HiGHS LP + HiGHS MILP** (`scipy.optimize.milp`) → collapse with non-associative (no-dilatancy) friction | the search over every joint's contact mode, with a proven least value for small models | about 150 lines of formulation beyond the LP model, written and checked here (§3) | **adopt as the fallback** for course-level models; the LP alone only bounds it from above |
| scikit-fem + Clarabel → finite-element limit analysis of a no-tension continuum | simple meshes and the cone solve | the whole formulation (280 lines), and a masonry element that doesn't lock, which is research (§4) | **not worth proposing** |
| build123d + HiGHS → 3-D rigid blocks from the engine's own solids | each brick's solid and the contact faces between bricks | the 3-D block formulation (§5.1) | **next probe**, not run |
| HiGHS + Thrust Network Analysis's linear vertical step → domes and groin vaults in the engine's environment | the solve; the method is published | form and force diagrams, the LP (§5.2) | **probe before dome and vault statics**, not run |
| COMPAS TNO or compas_cra, each in its own environment, fed the engine's geometry | TNO: all of 3-D thrust networks; compas_cra: 3-D contact detection | an export and a runner, and checks of the answers (§5.3) | **cross-checks** outside the engine, not dependencies |
| PyNite + v2's steel temperatures + AISC 360-16 Table A-4.2.1 | the steel's modulus and strength at temperature | the hand-off of temperatures (§5.4) | **with the arch–frame pair** |
| 3-D FE limit analysis (NGSolve or netgen.occ + Clarabel), FEniCSx + dolfinx_optim, and any partner for fedoo, gmsh or OpenSeesPy | – | – | **not useful** (§5.5–5.7) |

What the probes showed about the physics v2's statics must carry (Run, Derived; details in §2–4):
1. **Studio frames hold the span.** Where an arch has a maximum-thrust state, a light angle
   frame gives only 4–27 % of the heated growth, so every slice hinges at H_max. The heated
   thrust then applies uniformly along the arch.
2. **Where an arch has no maximum-thrust state** (Olsen's fast-fire, a flat, thick ring), rigid
   brick gives no finite thrust. The thrust goes to the posts, and the brick's hot crushing and
   creep decide it. Neither has data. v1's 5.34 × rule would need the brick to absorb 53–79 % of
   the growth.
3. **A no-tension wall under a point thrust can crack on a wedge.** From the thrust to the toe,
   it holds 24 % less than one block (the survey's case A1: 1.110 against 1.459 kN/m). So a
   model with only bed joints over-reads a wall unless the bond's head joints, or an inclined cut,
   are in it.
4. **A dry-laid buttress has a range of collapse loads, not one.** Case C: every thrust from
   2.245 to 2.939 kN/m. The LP reports the top; the least is the one to report.

## 1. The parts of the problem, and what could take each

| Part of v2's statics | Taken by | v2 writes |
|---|---|---|
| LP and MILP solves | SciPy (HiGHS), already a dependency | – |
| Cone solves (3-D friction cones, if written as cones) | Clarabel 0.11.1: Apache-2.0, `abi3` wheels for Linux, macOS and Windows (Run) | the cone formulation |
| Frame analysis: stiffness, member forces, deflections, tension-only rods | PyNite (MIT, pure Python; `statics-software.md` §12) | the frame model, from the design |
| Steel at temperature | AISC 360-16 Table A-4.2.1, already in `steel-design.md` §S3 (Verified there) | the temperature hand-off |
| Blocks' solids and the faces where they touch | build123d/OCP, already a dependency; compas_cra's detection (CPython ≤ 3.13 only) | the block formulation |
| 2-D rigid-block limit analysis: arches, walls, buttresses | no package, in process, on CPython 3.14 | the formulation: about 50 lines for an arch, 100 for walls of blocks (`statics-software.md` §11) |
| Non-associative friction | no package (§3) | the MILP: about 150 lines more, written here |
| 3-D thrust networks: domes, groin vaults | COMPAS TNO, outside the engine (`statics-software.md` §10.1) | an export and a runner; or the LP of §5.2 |
| Continuum limit analysis | none open without MOSEK (§4) | – |
| Meshing the engine's STEP solids | netgen.occ, with NGSolve (`statics-software.md` §7) | – |
| Elastic and thermal fields | scikit-fem, NGSolve | the weak forms, and data no source gives |

## 2. PyNite + the arch's LP: the hot thrust along a real frame (Run)

**Why a pair.** The LP alone gives each arch slice's least and most thrust (H_min and H_max) for
a span held fixed. Where an arch has no maximum-thrust state, it gives nothing at all
(`arch-thrust-theory.md` §8). PyNite alone gives the steel's response to a load someone has to
assume. Together they decide, slice by slice, whether the frame takes the arch's growth, the
arch hinges (H_max) or the arch spreads (H_min). The thrust's spread along the kiln and the
steel's stress follow from that.

**What each part takes, and what v2 writes.**
- **PyNite 3.2.1:**
  - the frame's stiffness: the flexibility matrix at the slices came from unit loads;
  - its member forces, rod forces and deflections.

  It matched 5wL⁴/384EI, PL³/48EI, wL²/8 and PL/EA to every printed digit, and the whole frame
  to 1.8 × 10⁻⁴ (Run). That shows it was driven correctly.
- **HiGHS:** each slice's H_min and H_max for its geometry.
- **SciPy's `lsq_linear`:** the compatibility problem as a bounded QP, solved in milliseconds:
  minimise ½PᵀCP − gᵀP over b·H_min ≤ P ≤ b·H_max, with C the frame's flexibility and g each
  side's share of the growth. Its KKT conditions held to 10⁻¹³, and for 4 slices an
  enumeration of the active sets confirmed the solution.
- **v2 would write:**
  - the arch's LP (the probe's `archlp.py`: 160 lines of code, checks included);
  - the frame built from the design (`frameflex.py`: 250);
  - the coupling (`compat.py`: 300, with the checks and sweeps).

**The model** (Heyman's assumptions, and where the probe departs from them):
- The arch is cut into independent rings along the kiln. The engine builds the fast-fire arch as
  4 rings of 9 in.
- The whole ring grows uniformly by ε, at sourced full-temperature values:
  - IFB 0.5–0.7 % (`thermal-properties.md` §2.1);
  - fireclay 3/32 in/ft (`refractory-movement-and-mortar.md` §1.1.1).
- Each ring starts at H_min, settled as the form comes out on a frame that gives (Derived from
  `arch-thrust-theory.md` [A1]).
- Displacements are small.
- The steel is elastic, with no yield.

**What it showed** (Run; `scratch/statics-combos/arch-frame/RESULTS.md`; re-run for this note):

| Case | Result |
|---|---|
| Four arches that have an H_max, in light frames (L2×2×3/16 or ¼, 36 in bays) | Every slice hinges at H_max. The frame gives 4–27 % of the growth at H_max, so the heated thrust applies uniformly |
| The fast-fire arch (27 in span, 1½ in/ft, 4½ in K-23; Olsen pp.139–140) | The LP is unbounded: no H_max, since R = 28.69 ≤ (R + T)·cos φ = 29.29 in. H_min = 11.66 lb/ft; the cold thrust is 29.64 |
| Fast-fire, rigid brick, IFB 0.5 %, 4 rings | The end rings carry 2,239 lb/ft and the middle rings spread at H_min. The angle sits at 41 ksi (past A36 yield), the rods at 11.9 ksi |
| The same, with finer slices | The thrust goes to the slice at each post: 28,126 lb/ft on 3 in strips, 149,716 on 1 in strips. In the limit the rods stretch by the whole growth: 13,900 lb per post (Derived) |
| v1's rule (5.34 × cold = 158 lb/ft) as a load | The frame gives 0.038 in at mid-bay and 0.001 in at a post, so the brick must absorb 53–79 % of IFB's 0.5 % growth |
| The frame's elastic range | ε up to 0.14 % keeps the angle at 12 ksi, and up to 0.44 % at yield. Sourced ε is 0.5–0.78 %. A stiffer angle doesn't help: L3×3×¼ carries 7,118 lb/ft at about the same stress, since the load is set by displacement |
| The steel's own heating (264 °F from the engine's wall solve) | The rods' own growth gives back 37 % of the arch's (end rings 1,406 lb/ft, 25.9 ksi) |
| Test only: the cold crushing strength, 145 psi, as a plastic cap | 1,165 lb/ft per slice at the ends, the steel at 22–23 ksi. The answer no longer depends on the slicing |

**Verdict: proposed.** PyNite takes the frame analysis off v2's hands entirely, and the pair
answers what neither part can alone. For arches without a maximum-thrust state, the answer
still waits on the brick's hot crushing strength and creep, which no source gives: the pair
narrows that gap to a single property.

## 3. HiGHS LP + HiGHS MILP: non-associative friction (Run)

**Why a pair.** Every LP formulation of rigid blocks takes friction as associative: a joint that
slides also opens. Real masonry joints slide without opening. The LP is then only an upper
bound where sliding governs an indeterminate assembly, such as the dry-laid buttress
(`statics-software.md` §11, case C; §16).
- The non-associative collapse load is the least load factor over the states that satisfy
  equilibrium, Coulomb friction, no tension and a mechanism with no dilatancy, with each
  joint's forces and velocities complementary.
- Ferris & Tin-Loi pose it as a mathematical program with complementarity constraints, and take
  the least load factor (1999 report = *Int. J. Mech. Sci.* 43 (2001) 209–224, p.7, Eq. 10;
  Read). Their solver is local and "does not guarantee a global minimum" (p.9; Read).
- HiGHS's branch and cut, through `scipy.optimize.milp`, gives the global least value for small
  models.

**What each tool takes, and what v2 writes.**

| Tool | Takes off v2's hands | v2 writes | Verdict |
|---|---|---|---|
| **SciPy `milp`** (HiGHS 1.12.0 in SciPy 1.18.1) | the search over every joint's contact mode (open, sticking, sliding either way), with a proven least value; the LP solves | the block model (about 100 lines, from the survey's probe) and the big-M mode formulation (about 150 more, `nonassoc_milp.py`) | **adopt as the fallback** for course-level models |
| compas_cra 0.8.0 | 3-D contact detection for polyhedral blocks; an in-process IPOPT solve | an external-load adapter (a 20-line monkeypatch), the load search, and the verdict itself: IPOPT's verdicts are local | **not the solver**; its contact detection could be reused |
| Siconos | per-load frictional contact for nonsmooth dynamics (from memory) | the least-load search, and bindings | **not useful now**: Apache-2.0 and active, but not on PyPI, and it answers "what happens under this load", not "the least collapse load" |
| Pyomo `mpec` with IPOPT; PATH | complementarity for an NLP solver (from memory) | the same formulation | **not useful**: local answers only; PATH is closed source with a size-limited free licence |
| LMGC90 | contact dynamics | the load search, by simulation | **not useful** (`statics-software.md` §10.3) |
| Gilbert, Casapulla & Ahmed's iterative LP, on `linprog` | nothing new | about 50 lines | the option for brick-level walls; no guarantee of the least value (Ahmed 2005, pp.133–134; Read) |

**Results** (kN/m; the survey's test inputs, not engineering data):

| Case | LP (associative) | MILP: least non-associative | Binaries | Time |
|---|---|---|---|---|
| A1, A2, A3, B (statically determinate) | 1.45877, 1.45877, 3.15430, 5.07309 | the same | 6–96 | < 0.25 s |
| C, buttress dry-laid against the wall | 2.93941 | **2.24546 (−23.6 %)** | 18 | 0.02 s |
| C2, both coursed | 2.82639 | ≤ 2.26154 (≥ 20 % lower); not proven least | 288 | found within 300 s; stopped at 1,163 s |
| Ferris & Tin-Loi's 33-block wall | – | no feasible point in 600 s | 498 | – |
| Ahmed's two-block benchmark (2005, ch.5) | 0.25 | 0.15 | – | reproduced, which shows the formulation is driven correctly |

- **Case C** was confirmed by brute force: all 4,096 contact-mode assignments, an LP pair each,
  agree to 10⁻¹⁵, as does a closed form derived by hand (Run, re-run for this note).
- **What governs:** wall and buttress both rock about their toes, while the joint between them
  stays closed and slides, pushed at its top corner.
- **The range:** collapse states exist for every thrust from 2.2455 to 2.9394 kN/m, depending on
  how hard the blocks press on each other, which a rigid model leaves undetermined.
- **compas_cra on case C** fails from H = 1.456 with its defaults, and holds to 2.30–2.60 with
  other settings. A state that stands exists up to at least 2.1555 (Derived), so its first verdict
  is IPOPT's local one. Its penalty solver never converged (Run).

**Verdict: adopt the MILP as the fallback.** No package takes non-associative rigid-block
limit analysis off v2's hands today in a usable form: on CPython 3.14, in process, giving the
least collapse load. The MILP is exact for course-level models (tens of blocks). For brick-level
models, its first feasible answer is still a collapse state, so an upper bound on the least
load; a tighter formulation or the iterative LP is the next step.

## 4. scikit-fem + Clarabel: finite-element limit analysis (Run)

**Why a pair.** `statics-software.md` judged scikit-fem "proposed, waits on data", because an
elastic or thermal field needs a hot modulus no source gives. Limit analysis needs only geometry,
weight and the no-tension assumption. The only open FE limit-analysis route that survey found,
Bleyer's dolfinx_optim, needs the commercial MOSEK. The question: would scikit-fem with an open
cone solver give v2 a limit-analysis tool that needs no new data?

**What each takes, and what v2 writes.**
- **scikit-fem 12.0.2:**
  - takes the mesh container, the edge topology and simple structured meshes;
  - its weak-form assembly doesn't apply, because limit analysis's constraints are pointwise;
  - meshing real kiln shapes is left to v2.
- **Clarabel 0.11.1:** takes the second-order-cone solve. It also has PSD, exponential and power
  cones (Run; Goulart & Chen 2024, Snippet).
  - Apache-2.0, `abi3` wheels on Linux, macOS and Windows, needs `cffi`;
  - no release since 2025-06-11.
  - Solve times grew about as n^1.7: 0.34 s at 552 elements, 88 s at 13,312. Every solve ended
    "AlmostSolved".
- **v2 would write** the whole formulation:
  - linear stress triangles; element equilibrium with self-weight;
  - traction continuity on shared edges;
  - the no-tension cone at every node.

  That is `fela.py`, 280 lines of code. It also needs an element that works for masonry, below.
- **dolfinx_optim / fenics_optim** would take the formulation. But it "relies on the Mosek
  mathematical programming library" (README, Read through a page summary), needs FEniCSx 0.8,
  and is licensed CC BY-SA 4.0. No other open FE limit-analysis library was found (search).

**Why the plain formulation fails for masonry** (Derived; confirmed by Run):
- **A free face locks its triangles.** A triangle with an edge on a traction-free face is forced
  to be uniaxial along that face, and the lock spreads at corners. On the survey's pier (case A1)
  the lower bound reached only 0.598 kN/m at 13,312 elements (88 s), and was stalling.
  - With the cone linearised for HiGHS, H was 0 on every mesh.
  - Linearising has a trap of its own: a uniaxial state survives only at the polygon's vertices.
- **A face that overhangs needs tension.** On an arch's intrados or a lintel's soffit, a face
  triangle can carry its own weight only in tension. So the arch is infeasible at every
  thickness, on every mesh.
- **What would fix it:** line-stress fields (an Airy-function, Normal Rigid No-Tension model, as
  Iannuzzo et al. use; Snippet). That is research, not coding.

**What the probe found that v2 can use with tools it already has.** A no-tension pier under a
point thrust cracks from the thrust to the toe, leaving the wedge behind:
- 0.9 H = V·b/2 + γb²(h/2 − a/3), so H ≤ 1.110 kN/m, against 1.459 for one block (Derived;
  checked by hand for this note);
- the existing HiGHS LP with one cut gives 1.11039 in 4 ms (Run);
- Ochsendorf, Hernando & Huerta (2004) make the same point for buttresses: "the monolithic
  approach is clearly unsafe" (Snippet).

**Verdict: not worth proposing.** The pair takes only the parts that were cheap anyway. The
formulation, and an element that works for masonry, would stay v2's.

## 5. Pairs judged on paper

### 5.1 build123d + HiGHS: 3-D rigid blocks from the engine's own solids

- **What it would take:** build123d (on OpenCascade, already a dependency) makes each brick's
  solid. Its Booleans give the faces where two bricks touch, which become the interfaces.
- **What v2 would write:** the 3-D formulation:
  - six equilibrium equations a block;
  - each interface's no-tension condition, at its corners;
  - friction, as a linearised cone (a pyramid) or as cones for Clarabel;
  - torsion at the interface.
- **Sources** (all Snippet): Orduña & Lourenço's two-part paper (*Int. J. Solids Struct.* 42,
  2005) treats 3-D blocks with torsion at frictional interfaces, non-associated flow and
  limited compression. Portioli et al. (2013) treat associative friction with torsion;
  Casapulla et al.'s 3DiLiA code does 3-D limit analysis.
- **What it answers:** bonded walls, corners tied in and groin vaults as courses.
- **Cost:** 3-D blocks need more equations and contacts per block, and `statics-software.md` §11
  found 2-D time growing as the square of the blocks. So brick-by-brick whole kilns need a
  sparser formulation; course-by-course models don't.
- **Verdict: the next probe** after the 2-D work. Not run.

### 5.2 HiGHS + Thrust Network Analysis's vertical step: domes and groin vaults

- **The method:** in Thrust Network Analysis, the horizontal equilibrium is a reciprocal pair of
  form and force diagrams. With the inverse of the force diagram's scale taken as a variable,
  the vertical equilibrium is linear, and is solved by linear optimisation (Block & Ochsendorf,
  SAHC 2008 slides; Snippet). HiGHS solves that LP in the engine's own environment, without
  COMPAS TNO's NumPy < 2.4.
- **What v2 would write:** the form and force diagrams (for a dome, a radial or ring pattern;
  for a groin vault, a cross or fan), and the LP.
- **Limitation:** a fixed force diagram gives a lower bound for that pattern only. "No admissible
  state" then means none with that pattern, as with the published values themselves (cross
  0.061, fan 0.084; `engine-v2-negative-cases.md` §1).
- **Verdict: probe before v2's dome and vault statics.** Not run.

### 5.3 Side environments: COMPAS TNO, compas_cra and compas_lmgc90 on the engine's geometry

- **What each takes:**
  - TNO takes all of 3-D thrust networks (form diagrams, envelopes, optimisation; it ran on
    NumPy 2.3.5, `statics-software.md` §10.1);
  - compas_cra takes 3-D contact detection (§3);
  - compas_lmgc90 takes contact dynamics.
- **How they'd run:** each in its own environment, `uv run --no-project --python 3.13 --with …`,
  reading a JSON or OBJ export of the engine's geometry.
- **What v2 would write:** the export, a runner, and checks of the answers. TNO failed on two of
  six 3-D runs; compas_cra's verdicts are IPOPT's local ones.
- **Not at run time:** a subprocess breaks ADR 0002.
- **Verdict: cross-checks** for N2 and N6 on a developer's machine or in CI. Not dependencies.

### 5.4 PyNite + v2's steel temperatures + AISC 360-16 Table A-4.2.1

- **What it takes:** the table (already sourced in `steel-design.md` §S3) gives Fy(T)/Fy and
  E(T)/E. PyNite takes the analysis at those values.
- **The pair's main effect** is the rods' own growth. At the engine's 264 °F steel temperature
  for the fast-fire kiln, it gave back 37 % of the arch's growth (§2).
- **Verdict:** part of the arch–frame pair.

### 5.5 3-D FE limit analysis: NGSolve or netgen.occ + Clarabel

- **What it would take:** netgen.occ meshes the engine's STEP solids, and Clarabel has PSD cones
  for a 3-D no-tension condition.
- **Why not:** the formulation problem of §4 stays, and in 3-D it is worse.
- **Verdict: not useful.**

### 5.6 FEniCSx + dolfinx_optim, with an open solver in place of MOSEK

- **What it would take:** the formulation.
- **What v2 would write:** a back-end against its MOSEK Fusion layer, and a fork to maintain,
  still under CC BY-SA 4.0 and on FEniCSx 0.8. FEniCSx's own problems remain (no PyPI release;
  a compiler and MPI at run time; `statics-software.md` §4).
- **Verdict: not useful.**

### 5.7 Licence-blocked tools with any partner

A partner doesn't change a licence:
- fedoo is GPL-3.0;
- gmsh is GPL-2.0-or-later, with a linking exception;
- OpenSeesPy is for non-commercial or internal use only.

None goes into the engine. OpenSees's "internal purposes" would allow a developer's cross-check
of PyNite's frames, but PyNite is already checked against the closed forms. CVXPY is glue only:
Clarabel and SciPy take matrices directly.

## 6. Ranked by what each takes off v2's hands

| # | Pair | Takes | v2 writes | Verdict |
|---|---|---|---|---|
| 1 | PyNite + the arch's LP | the whole frame analysis | the arch's LP, the frame model, the coupling | **proposed** |
| 2 | HiGHS LP + MILP | the mode search for non-associative friction | about 150 lines beyond the LP model, written | **adopt as the fallback** |
| 3 | COMPAS TNO in its own environment | all of 3-D thrust networks | an export and a runner | **cross-check** |
| 4 | build123d + HiGHS | the blocks' solids and contact faces | the 3-D block formulation | **next probe** |
| 5 | HiGHS + TNA's vertical step | the LP solve | the diagrams and the LP | **probe before vaults and domes** |
| 6 | PyNite + AISC A-4.2.1 | steel at temperature | the hand-off | with #1 |
| 7 | compas_cra | 3-D contact detection | everything else | not the solver |
| 8 | scikit-fem + Clarabel | meshes and the cone solve | the formulation and a new element | **not worth proposing** |
| – | 3-D FELA, FEniCSx + dolfinx_optim, licence-blocked tools, Siconos, LMGC90, Pyomo `mpec`/PATH | – | – | not useful |

## 7. What this does not settle

- **The fast-fire arch's real thrust** waits on IFB's hot crushing strength, creep and joint
  closure, none of them sourced (`arch-thrust-theory.md` §6; `refractory-movement-and-mortar.md`
  §3). The arch–frame pair turns the question into those numbers.
- **Bonded walls:** does the head joints' friction win back part of the wedge's 24 %? Rigid
  blocks laid in the real bond can answer that (`scratch/statics-software/wall_bond_scale.py`);
  not run.
- **Non-associative friction at brick level:** needs a tighter MILP or the iterative LP.
- **Nothing in 3-D was run** (§5.1–5.3).
- **Not read:**
  - Gilbert, Casapulla & Ahmed 2006 (abstract only; its basis, Ahmed 2005 ch.5, was read);
  - Ochsendorf, Hernando & Huerta 2004;
  - Orduña & Lourenço 2005;
  - Block & Ochsendorf's TNA papers (a slide extract only);
  - Sloan 1988; Makrodimopoulos & Martin 2006; Iannuzzo et al.

## Sources

- M. C. Ferris, F. Tin-Loi, "Limit analysis of frictional block assemblies as a mathematical
  program with complementarity constraints", UW-Madison Math. Prog. TR 99-01 (1999) = *Int. J.
  Mech. Sci.* 43 (2001) 209–224.
  https://minds.wisc.edu/bitstreams/eb02dd9b-3f1e-429d-b9e5-762c83e628c6/download (Read)
- H. M. Ahmed, PhD thesis, University of Sheffield, 2005, ch.5.
  https://etheses.whiterose.ac.uk/id/eprint/14871/1/419278.pdf (Read)
- M. Gilbert, C. Casapulla, H. M. Ahmed, "Limit analysis of masonry block structures with
  non-associative frictional joints using linear programming", *Computers & Structures* 84
  (2006) 873–887 (Snippet)
- J. Ochsendorf, J. I. Hernando, S. Huerta, "Collapse of masonry buttresses", *J. Archit. Eng.*
  10(3) (2004) 88–97, doi 10.1061/(ASCE)1076-0431(2004)10:3(88) (Snippet)
- J. Bleyer, dolfinx_optim README. https://github.com/bleyerj/dolfinx_optim (Read, page summary)
- P. Goulart, Y. Chen, "Clarabel: an interior-point solver for conic programs with quadratic
  objectives", arXiv 2405.12762 (Snippet). Package facts: https://pypi.org/pypi/clarabel/json,
  https://pypi.org/pypi/scikit-fem/json, https://pypi.org/pypi/cvxpy/json (Run, 2026-11-09)
- S. W. Sloan, *Int. J. Numer. Anal. Meth. Geomech.* 12(1) (1988) 61–77; K. Makrodimopoulos,
  C. M. Martin, *Int. J. Numer. Meth. Eng.* 66(4) (2006) 604–634 (Snippet)
- P. Block, J. Ochsendorf, Thrust Network Analysis, SAHC 2008 slides,
  https://web.mit.edu/masonry/thrustNetwork/SAHC08_ppt_block-ochsendorf.pdf (Snippet: search
  extract; the PDF's text wasn't readable here)
- A. Orduña, P. B. Lourenço, "Three-dimensional limit analysis of rigid blocks assemblages",
  Parts I and II, *Int. J. Solids Struct.* 42 (2005) (Snippet). F. Portioli et al., *Arch.
  Appl. Mech.* 83 (2013) (Snippet)
- AISC 360-16 Table A-4.2.1, as recorded in `steel-design.md` §S3
- The repo's own: `statics-software.md`, `arch-thrust-theory.md`, `refractory-movement-and-mortar.md`,
  `thermal-properties.md`, `steel-design.md`, `engine-v2-negative-cases.md`
