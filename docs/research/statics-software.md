# Statics software for engine v2: FEniCSx, fedoo and the alternatives

Surveyed 2026-11-09, before any v2 statics code (ADR 0017, decision 5). No engine changes were
made. This restarts a survey that stopped before writing anything: its probe scripts were reused
after reading them, and every number below was re-run for this note.

**Judged by what each tool takes off v2's hands (the user, 2026-11-09):** "The important
evaluation is that there is a way to use the tool so this project does not need to solve that
part too." Matching a particular rule or result counts for nothing, since many of those aren't
valid conclusions; v2 starts over from the reference kilns and published formulas. The
benchmarks (§2) only show that each tool was driven correctly. Pairs of tools are surveyed in
`statics-combinations.md`.

- Probe scripts: `scratch/statics-software/` (git-ignored; their output is copied into the tables
  below). Each script's docstring says how to run it:
  - B1, the arch: `arch_rigid_block_lp.py`, `arch_compas_tno.py`, `arch_compas_tno2.py`;
  - 3-D vaults: `vault_compas_tno.py`, `vault_minthk_tno.py`;
  - B2, walls: `wall_buttress_lp.py`, `wall_bond_scale.py`;
  - B3, thermal stress: `cyl_PACKAGE.py`, `plate_PACKAGE.py`, `cyl3d_PACKAGE.py`
    (`cyl3d_skfem_tet.py` for P2 tetrahedra);
  - B4, the beam: `frame_probe.py`;
  - STEP meshing: `docker_step.sh` with `step_write.py` and `step_mesh.py`;
  - Docker runs: `docker_slim.sh`, `docker_fenicsx_pip.sh`.
- Throwaway venvs: CPython 3.14.10 under uv 0.13.7, in the session scratchpad, never the repo's
  `.venv`. FEniCSx and NGSolve were also run in Docker: the official `dolfinx/dolfinx:stable`
  image, and the project's own `kilndesigner-server:latest` (python:3.14-slim-trixie).
- Machine: Intel i7-7700 (4 cores, 8 threads, 2017), 15 GB, WSL2 Debian. Times are wall-clock
  and single runs.
- Package facts (versions, dates, licences, wheels) were read from the PyPI JSON API
  (https://pypi.org/pypi/NAME/json; `pypi_info.mjs`), the GitHub REST API (`gh_meta2.mjs`), `uv pip
  compile --python-version 3.14 --only-binary :all:` for Linux and Windows (`wheel_matrix2.mjs`),
  and the documentation pages cited in each section. Anything stated from memory says so.
- Earlier mentions in `docs/`:
  - `planning/02-plan.md` (the `thermal/` package: "later scikit-fem");
  - `planning/01-market-survey.md` (FreeCAD FEM with CalculiX, for heat transfer);
  - the structure review, finding #4 (TNA and LimitState:RING as current practice for the best
    thrust line);
  - `blocked-items.md` [K9] (a paper on finite-element thrust lines in domes, not a package).

  No package had been evaluated before.

## 0. Short answer

| Question | Answer |
|---|---|
| What must v2's statics compute? | Mostly equilibrium, not stress. Every must-fail case (`engine-v2-negative-cases.md` §6, N1–N6) asks whether a thrust line, thrust network or set of joint forces exists inside the masonry, where a resultant falls, or what friction a joint needs. That is limit analysis (Heyman's safe theorem), solved as a linear program |
| Which tool takes the most off v2's hands? | **SciPy's `linprog` (HiGHS)**, already an engine dependency, takes every solve. v2 writes each formulation: about 50 lines for an arch and 100 for walls of blocks (§11). No package takes the 2-D formulations themselves off v2's hands in the engine's environment. Its probes reproduced Couplet–Heyman's least thickness and the wall hand cases, which shows it is driven correctly. **Adopt** |
| FEniCSx? | It would take assembly and solving for continuum problems. But there is no PyPI release, only beta wheels on Test PyPI; it needs a C compiler and an MPI runtime when it runs; and its limit analysis needs the commercial MOSEK. **Not useful now** |
| fedoo? | It would take FE with contact, cohesive joints and rigid bodies. But it is GPL-3.0, so a distributed kilndesigner that includes it is bound by the GPL. Its elastic law has no thermal strain, and it has no limit analysis. **Not useful** |
| Thermal stress? | scikit-fem, FEniCSx, fedoo and NGSolve all take the assembly off v2's hands; v2 would write the weak forms, about 60 lines each. The software is not what's missing: the materials' hot modulus, tensile strength and creep are (ADR 0017, "What v2 leaves out"). The survey does not change that |
| 3-D vaults (N2 domes, N6 groins)? | **COMPAS TNO** would take all of 3-D thrust networks off v2's hands, more than any other package here. But it can't share the engine's environment (it needs NumPy < 2.4), it needs an expert's set-up, it failed on two of six 3-D runs, and its vertical bounds let an arch's thrust line land above the springing (§10.1). **Not useful as a dependency; a cross-check only**, in its own environment |
| Frames, ties and bands? | **PyNite** (MIT, pure Python, tension-only members) takes the whole frame analysis off v2's hands; v2 builds the frame from the design. With the arch's LP it gives the hot thrust along a real frame (`statics-combinations.md` §2). **Proposed** |
| Pairs? | `statics-combinations.md`: PyNite with the arch's LP (proposed); HiGHS's MILP for non-associative friction (adopt as the fallback); FE limit analysis on scikit-fem and Clarabel (not worth proposing) |

---

## 1. What the tools were judged on

The user's decisions (ADR 0017) set what the tools must serve:
- no flags, so a tool is judged on how well, and how simply, it computes the physics, not on
  how it reports;
- walls and buttresses are computed: what holds a wall is modelled, and its equilibrium gives
  the resultant's place in each base and the friction each bed joint needs (decision 7).

| Need | Kind of analysis | Where it comes from |
|---|---|---|
| Arches and vaults (sprung, catenary, two-radius, offset peak) | thrust line inside the ring; least thickness; minimum and maximum thrust | `arch-thrust-theory.md`, `domes-over-doors.md` §D3, N1 |
| Domes, cracked or not | thrust surface with and without hoop force | `masonry-statics.md` §M3, N2 |
| Crossing (groin) vaults | thrust network in 3-D | `masonry-statics.md` §M4, N6 |
| Walls, buttresses, jambs, chimneys | rigid blocks: overturning, sliding at bed joints, resultant in the base | ADR 0017 decision 7, N3, N4 |
| Masonry behaviour | no tension; friction μ 0.6–0.7 cold, 0.50 hot; no hot cohesion | `engine-v2-negative-cases.md` §2 (from `mortar-and-brick-strength.md`); `refractory-movement-and-mortar.md` §2 |
| Frames, rods, bands | elastic frame analysis, tension-only members | `steel-design.md` |
| Heat | thermal stress, expansion against frames, creep | data not found (`arch-thrust-theory.md` §6; `refractory-movement-and-mortar.md` §3) |
| Geometry | v1's OpenCascade solids, exported as STEP | `geometry.py` |

Criteria for each package, after the user's yardstick (which part of the problem it takes off
v2's hands, and what v2 would still write): licence against this repo's MIT `LICENSE`; whether it installs with
uv on CPython 3.14 on Linux, and whether Windows wheels exist; maintenance; documentation and
published verification; features against the table above; dependency weight; whether it runs
headless inside a pure engine (ADR 0002: no I/O beyond files it is handed); runtime.

## 2. The benchmarks and their closed forms

| # | Case | Closed form | Source |
|---|---|---|---|
| B1 | Semicircular arch, own weight, least thickness | η = t/r = 0.107426 (weights on the centre line, "CCR"), 0.107478 (true voussoir centroids, Milankovitch); thrust h = H/(w r) = 0.621 | Rizzi et al., SAHC 2010, Table 1, via `domes-over-doors.md` §D3 [D5] (Verified there). TNA's 0.1079 is in `masonry-statics.md` [M3] |
| B2 | Wall under a thrust H at height h_s, with V on top | overturning: H·h_s = Σ(weight × lever to the toe); sliding at a bed joint: H = μN; resultant x from the toe = (restoring moment − H·h_s)/N | statics, worked in `wall_buttress_lp.py` (Derived) |
| B3a | Plate, temperature linear through the thickness | edges free: no stress; edges clamped against rotation: σ_max = αtE / [2(1 − ν)], t the difference between the faces | Timoshenko & Woinowsky-Krieger, *Theory of Plates and Shells*, 2nd ed., 1959, §14, pp. 49–50, Eq. (51), read on the page this round [T1] |
| B3b | Long thick cylinder, steady radial heat flow (T ∝ ln(b/r)) | σ_θ = αET_a / [2(1 − ν) ln(b/a)] · [1 − ln(b/r) − a²/(b² − a²)(1 + b²/r²) ln(b/a)] | Nowacki, *Thermoelasticity* (1962), as printed on Itasca's FLAC3D verification page [T2]; reduces to the form above (Derived). For a = 1 in, b = 2 in, E = 3×10⁷ psi, ν = 0.3, α = 6×10⁻⁶/°F, 10 °F hotter inside: −1573.7 psi inner, +997.8 outer. Roark & Young, 5th ed., p. 585, case 16 prints −1574 and 998 (quoted by Autodesk's verification page [T3]; Roark not read) |
| B4 | Simply supported beam, uniform load | M = wL²/8; deflection 5wL⁴/(384EI) | standard strength of materials (from memory) |

All loads and material values in the probes are test inputs chosen to exercise the codes, not
engineering data for the engine. The benchmarks show that each tool was driven correctly; no tool
is judged by them.

## 3. The candidates at a glance

| Package | Version read (released) | Licence | CPython 3.14, Linux | Windows wheel | Run here |
|---|---|---|---|---|---|
| SciPy `linprog` (HiGHS) | 1.18.1 (2026-08-21), the version in `uv.lock` | BSD-3-Clause | yes, already locked | yes | B1, B2, scaling |
| FEniCSx (DOLFINx) | 0.11.0.post0 (2026-06-10, Docker stable); 0.12.0.dev202611070209 (Test PyPI, 2026-11-07) | LGPL-3.0-or-later (dolfinx, ffcx, ufl); MIT (basix) | not on PyPI. Test PyPI beta installs, then needs `mpich` and a C compiler to run | beta, abi3 | B3a, B3b, 3-D |
| fedoo | 1.1.0 (2026-10-14), with simcoon 2.2.0 | GPL-3.0 (both) | yes | yes | B3a, B3b, 3-D |
| scikit-fem | 12.0.2 (2026-06-05) | BSD-3-Clause | yes, pure Python | yes | B3a, B3b, 3-D |
| NGSolve | 6.2.2608 (2026-10-01) | LGPL-2.1-only | yes, but needs the system library `libquadmath0` | yes | B3a, B3b, 3-D, STEP |
| SfePy | 2026.3 (2026-09-29) | BSD-3-Clause | no wheels; build failed without a C compiler | no | install only |
| GetFEM | 5.5 (getfem.org) | LGPL | not on PyPI | Python 3.7 installer only | no |
| Kratos | 10.4.4 (2026-09-28) | BSD-4-Clause | yes; imports | yes | import only |
| OpenSeesPy | 3.8.0.0 (2026-03-18) | UC Regents: non-commercial or internal use only | yes; runs | a wheel resolves (classifier 3.12); not run | B4 |
| CalculiX | ccx 2.23 | GPL-2.0 | executable, not on PyPI | third-party builds | no |
| PyMFEM | 4.10.0.1 (2026-10-27) | BSD-3-Clause | yes; imports | no | import only |
| COMPAS TNA / TNO | 0.9.0 (2026-09-02) / 0.4.0 (2026-08-27) | MIT | installs; runs only with NumPy < 2.4 | yes | B1, 3-D vaults |
| compas_cra | 0.8.0 (2026-08-29) | MIT | no cp314 wheel; uv falls back to 0.6.0 | no (3.14) | read only |
| LMGC90 (compas_lmgc90) | compas_lmgc90 0.1.11 (2026-08-28) | CeCILL (LMGC90) | no cp314 wheel | up to cp313 | no |
| YADE | 2025.2.0 (Debian) | GPL-2 | Linux packages only | no | no |
| PyNite | 3.2.1 (2026-10-29) | MIT | yes, pure Python | yes | B4 |
| anaStruct | 1.7.1 (2026-10-31) | LGPL-3.0 in `LICENSE.txt`, GPL-3.0-or-later in `pyproject.toml` | yes | yes | B4 |
| gmsh | 4.15.2 (2026-03-24) | GPL-2.0-or-later, with a linking exception | yes, but needs libGLU, libgomp and X libraries | yes | STEP |
| meshio | 5.3.5 (2024-01-31) | MIT | yes, pure Python | yes | import |
| pygmsh | 7.1.17 (2022-01-28) | GPL-3.0 | pure Python; last push 2023-10-04 | – | no |

---

## 4. FEniCSx (DOLFINx)

**What it gives.** A general finite-element system: weak forms written in UFL, elements from
Basix, MPI-parallel assembly and, optionally, PETSc solvers [F1]. Any 2-D, axisymmetric or 3-D
problem that can be written as a weak form can be posed, including nonlinear ones (from memory:
PETSc SNES or a Newton loop). The official demo list [F2] covers:
- Poisson, elasticity with algebraic multigrid, and static condensation;
- Stokes, Navier–Stokes and Cahn–Hilliard;
- mesh generation with Gmsh;
- the snap-through of a hyperelastic shallow arch.

It has **no demo for thermo-elasticity, plasticity or contact**, and no masonry (no-tension)
material. Limit analysis exists only as Bleyer's `dolfinx_optim`, which needs the commercial
MOSEK solver [F5]; its earlier FEniCS version, `fenics_optim`, had a limit-analysis module [F5].

**Installation (all Run, except where noted).**
- **PyPI:** `fenics-dolfinx` is not on PyPI (HTTP 404). The README [F1] recommends conda or
  "pip (beta)": "Beta binary wheels of main are built twice a week and available from Test PyPI
  for Python 3.12+. They are built without PETSc and with SuperLU_DIST", for Linux (glibc ≥ 2.34),
  macOS 15 and Windows x86_64. "With uv pip install, also pass --index-strategy
  unsafe-best-match." That strategy lets Test PyPI, which anyone can upload to, supply any
  dependency, not only the four FEniCS packages (uv's documentation calls it unsafe for that
  reason; from memory).
- **On CPython 3.14.10,** `fenics-dolfinx==0.12.0.dev202611070209` installed. The first import
  failed: "DOLFINx wheels need an MPICH ABI compatible MPI (libmpi.so.12), e.g. pip install
  mpich". After `uv pip install mpich` it imported in 0.8 s. The first form then failed: the
  JIT compiles generated C through cffi and found no `cc` on the host.
- **In the project's server image,** the wheels plus NumPy, SciPy and mpich took 403 MB, and
  `gcc libc6-dev` added 191 MB to `/usr`. After that the probes ran.
- **The stable route is Docker** (`dolfinx/dolfinx:stable`: DOLFINx 0.11.0.post0, Python 3.12.3,
  PETSc through petsc4py 3.25.1; 4.72 GB on disk), conda-forge, the Ubuntu PPA, Debian or Spack
  [F1]. On Windows, conda has no PETSc [F1].
- **The JIT writes compiled C modules** to `$XDG_CACHE_HOME/fenics`, by default `~/.cache/fenics`
  (`dolfinx/jit.py`, read in the installed package). So the engine would write outside the files
  it is handed unless the cache is redirected (ADR 0002).

**Maintenance.** Releases v0.11.0 (2026-06-09) and v0.11.0.post0 (2026-06-10); pushed
2026-11-09; 1,247 stars [GitHub API]. Cite: Baratta et al., "DOLFINx: the next generation FEniCS
problem solving environment", 2023 preprint, doi 10.5281/zenodo.10447666 [F3].

**Benchmarks (Run).**

| Case | Mesh | Result | Closed form |
|---|---|---|---|
| B3b, plane strain | Q2 quads 16 × 64, 8,514 u-dofs | hoop −1576.7 psi (−0.19 %) inner, 997.6 (−0.02 %) outer | −1573.7, 997.8 |
| B3a free, held, held 0→ΔT | Q2 40 × 4, 1,458 u-dofs | 0.000; −1285.714 / +1285.714; −2571.429 / 0.000 | the same, to the digits printed |

The Docker 0.11.0 and the pip 0.12.0.dev builds gave identical numbers. The first form took about
1.5 s to JIT-compile in Docker and 0.4 s in the server image; later ones came from the cache.

**3-D runtime (Run, Docker 0.11.0, PETSc).** Thick cylinder as a solid, Q2 hexahedra:

| u-dofs | heat (JIT, assemble, solve) | elastic, CG + GAMG | elastic, MUMPS LU | hoop error |
|---|---|---|---|---|
| 56,355 | 1.7 s | 7.2 s (45 iterations) | 7.9 s | −0.67 %, −0.08 % |
| 181,875 | 4.7 s | 24.7 s (43 iterations) | 38.6 s | −0.32 %, −0.03 % |

**Fit for kilns.** It is excellent for continuum problems: thermo-elasticity with
temperature-dependent properties, coupled heat and stress, and contact through add-on packages
(from memory). But v2's
first need is limit analysis, and FEniCSx doesn't do it without MOSEK. As a dependency of a pure,
light engine it costs a compiler and an MPI runtime when it runs, a cache on disk, and an
unreleased (Test PyPI) or 4.7 GB (Docker) install.

**Licence.** LGPL-3.0-or-later for dolfinx, ffcx and ufl; MIT for basix (PyPI metadata). The
MIT repo can import LGPL libraries. A distributed image must let users replace the LGPL parts,
which separately installed Python packages allow (the LGPL's terms, from memory).

**Verdict: not useful now.** It's the strongest general FE code in the survey, and it was not
needed for anything v2's statics must compute first. Revisit if v2 takes on coupled
thermo-mechanical fields in 3-D, and once DOLFINx is on PyPI.

## 5. fedoo

**What it gives.** "A free open source Finite Element library developed in Python" whose "main
application" is "the mechanical response of heterogeneous materials" [D1]. Its README lists an
implicit static and dynamic solver, finite-strain laws from the simcoon library, "Contact in 2D
and 3D, Self contact" and multi-point constraints [D1]. The installed 1.1.0 also has:
- `HeatEquation` and a `ThermalProperties` law;
- beam elements;
- a penalty `Contact`, and an `IPCContact` with Coulomb friction (through the optional `ipctk`);
- cohesive-zone laws, which could model mortar joints;
- rigid bodies.

These are from the package source (`fedoo/constraint/ipc_contact.py`, `constitutivelaw/`). The
documentation index [D2] lists the same areas. No verification or benchmark statement was found
in the README or the docs index, and no journal paper (a CSMA 2024 paper on the 3MAH suite was
found but couldn't be read).

**Thermal strain needs a workaround.** The linear `ElasticIsotrop` law has no thermal expansion.
Following fedoo's own `examples/thermal/thermo_meca_weak_coupling_3D.py`, expansion comes through
simcoon's `ELISO` UMAT (properties E, ν, α) in a `NonLinear` problem. The temperature is written
into the assembly's Gauss-point state. A linear thermo-elastic solve then takes three Newton
iterations.

**Installation (Run).** A pure wheel; simcoon 2.2.0 ships cp314 wheels for Linux and Windows.
`uv pip install fedoo` worked on CPython 3.14.10 (PyPI classifiers stop at 3.13). It took 263 MB
with NumPy, SciPy and h5py. At import it warns that "no fast direct sparse solver has been found.
Consider installing pypardiso (Intel) or python-mumps".
- **pypardiso** brings Intel MKL, under the proprietary Intel Simplified Software License; the
  venv grew to 1.2 GB.
- **python-mumps** has no wheels (sdist only).

**Maintenance.** 12 releases in the last 12 months; pushed 2026-11-09; 34 stars; a small team,
part of the 3MAH suite with simcoon and microgen [GitHub API; D1].

**Benchmarks (Run).**

| Case | Mesh | Result | Closed form |
|---|---|---|---|
| B3b | quad9 33 × 129 nodes, 8,514 u-dofs | −1576.3 (−0.17 %), 997.5 (−0.03 %) | −1573.7, 997.8 |
| B3a free, held, held 0→ΔT | quad9 40 × 4 | 0.000; ∓1285.714; −2571.429 / 0.000 | the same |

3-D cylinder, hex20 (the highest order `box_mesh` offers):

| u-dofs | solver | heat | elastic, 3 Newton iterations | hoop error |
|---|---|---|---|---|
| 30,051 | SciPy (default) | 1.2 s | 14.3 s | −0.60 %, −0.12 % |
| 30,051 | pypardiso | 0.6 s | 3.0 s | the same |
| 95,043 | pypardiso | 1.8 s | 14.0 s | −0.29 %, −0.05 % |

**Fit for kilns.** Its contact, friction, cohesive interfaces and rigid bodies are the right
ingredients for a joint-by-joint masonry model in principle. But that is a nonlinear, incremental
analysis needing joint stiffnesses and hot cohesion that no source gives. And fedoo has no limit
analysis. For thermal stress it works, through a workaround, and it is fast only with MKL.

**Licence.** GPL-3.0 (`LICENSE`; PyPI "GPLv3"), and simcoon is GPL-3.0-or-later. MIT code may be
combined with GPL code, but anything distributed that includes fedoo carries the GPL's terms: the
Docker image, or the engine published as a package that depends on it. The repo's MIT licence
would no longer describe what users receive.

**Verdict: not useful.** The licence alone rules it out as an engine dependency. Beyond that,
nothing it adds is needed for v2's first statics, and what it would be needed for (thermal
stress) waits on data. This agrees with the user's first reading: "I do not think it would suit
me now".

## 6. scikit-fem

**What it gives.** "A pure Python 3.10+ library for performing finite element assembly"; "the
minimal dependencies are numpy and scipy"; it "contains no compiled code" [K1]. You write the
bilinear and linear forms; scikit-fem assembles them, and SciPy (or PyAMG) solves. It reads
meshes through meshio, ships elasticity helpers (`skfem.models.elasticity`), and has an
`autodiff` module for nonlinear forms [K1]. There is no contact, plasticity or thermal-coupling
layer: you write them, as the probes did in about 60 lines each.

**Installation (Run).** A pure wheel; classifiers to 3.14. scikit-fem with PyAMG added 8 MB to
NumPy and SciPy (184 MB venv in all). It imported in 0.75 s. It installs on Windows wherever
NumPy and SciPy do.

**Maintenance and validity.** 12.0.2 (2026-06-05); pushed 2026-11-09; 676 stars. The paper:
Gustafsson & McBain, *JOSS* 5(52) 2369, 2020, doi 10.21105/joss.02369 [K1]. Tests run in GitHub
Actions; no verification against analytical solutions is claimed [K1].

**Benchmarks (Run).**

| Case | Mesh | Result |
|---|---|---|
| B3b | Q2 16 × 64, 8,514 u-dofs | −1576.7 (−0.19 %), 997.6 (−0.02 %): identical to FEniCSx on the same mesh |
| B3a | Q2 40 × 4 | 0.000; ∓1285.714; −2571.429 / 0.000: exact |

3-D cylinder:

| Elements | u-dofs | assemble elastic | PyAMG + CG | SciPy SuperLU | hoop error |
|---|---|---|---|---|---|
| Q2 hexahedra | 56,355 | 39.4 s | 6.7 s (39 iterations) | 16.4 s | −0.67 %, −0.08 % |
| P2 tetrahedra | 56,355 | 5.5 s | 4.4 s (40 iterations) | 46.8 s | +0.61 %, −0.10 % |
| P2 tetrahedra | 181,875 | 20.9 s | 11.6 s (43 iterations) | – | +0.29 %, −0.05 % |

Its vectorised NumPy assembly is the cost, and grows with element order (27-node hexahedra are
slow). For the 2-D sections and axisymmetric shells a kiln needs it takes well under a second.

**Fit for kilns.** The lightest way to add elastic or thermo-elastic fields to the engine. It is
pure Python and does no I/O, so it fits ADR 0002 as it stands. Every step is explicit code,
which suits the "working" the engine must report.

**Licence.** BSD-3-Clause [K1].

**Verdict: proposed** as the FE layer if v2 takes on thermal stress, once the hot modulus, tensile
strength and expansion of the materials are sourced. Not needed for the first statics step.

## 7. NGSolve (with Netgen and netgen.occ)

**What it gives.** High-order FE with symbolic weak forms, built-in BDDC preconditioning, shared-
memory parallel assembly (TaskManager), MPI, and its own OpenCascade kernel (`netgen.occ`) with
curved meshing. The tutorials include "Solving nonlinear Elasticity", "6.2 Contact Problems",
"6.3 Elasto-Plasticity" and "4.4 Open Cascade Technology Geometry" [N1].

**Installation (Run).**
- **Wheels:** NGSolve and Netgen ship cp314 wheels for Linux and Windows, with netgen-occt 7.8.1
  and ngsolve-openblas (310 MB venv).
- **On this host and in python:3.14-slim-trixie, the import failed:** the bundled
  `libgfortran.so.5` needs `libquadmath.so.0`, which the wheel doesn't carry. `apt-get install
  libquadmath0` fixed it. With gmsh's libraries as well (§13), `/usr` grew by 7 MB.
- **On Windows** this was not tested.

**Maintenance.** 23 releases in the last 12 months; pushed 2026-11-09; 591 stars.

**Benchmarks (Run, server image).**

| Case | Mesh | Result |
|---|---|---|
| B3b | P2, maxh 0.0625, curved, 5,564 u-dofs | −1570.7 (+0.19 %), 997.2 (−0.06 %) |
| B3b | P3, maxh 0.25, 758 u-dofs | −1571.5 (+0.14 %), 997.7 (−0.01 %) |
| B3a | P2, maxh 0.25 | 0.000; ∓1285.714; −2571.429 / 0.000: exact |

3-D cylinder, P2 tetrahedra on a curved OpenCascade solid:

| u-dofs | mesh | assemble + BDDC set-up | BDDC + CG | sparse Cholesky | hoop error |
|---|---|---|---|---|---|
| 44,574 | 0.6 s | 1.4 s | 0.05 s (2 iterations) | 1.2 s | −0.19 %, −0.09 % |
| 181,368 | 2.4 s | 20.3 s | 0.48 s (2 iterations) | 21.1 s | −0.11 %, −0.03 % |

**STEP from the engine (Run).** A sprung-arch ring (48 in span, 12 in rise, 4½ in ring) was
written by build123d 0.13.0, as `geometry.py` does. `netgen.occ` read it and meshed 24,298
tetrahedra (116,679 P2 displacement dofs) in 1.9 s. Two OpenCascade builds would sit in one
process (build123d's and netgen-occt), so the hand-over was by file; one process with both was
not tried.

**Fit for kilns.** The fastest 3-D solver here, the only one that meshes the engine's STEP
solids natively with curved elements, and it has contact and plasticity tutorials. It is a
compiled C++ library with its own runtime, not pure Python.

**Licence.** LGPL-2.1-only (Netgen too) [PyPI].

**Verdict: proposed** only if v2 needs 3-D fields (a whole sail dome or a crossing vault as a
continuum). Otherwise scikit-fem covers 2-D and axisymmetric work at a tenth of the weight.

## 8. Other general FE packages

**SfePy** (2026.3, BSD-3-Clause, 849 stars). Its gallery has "Thermo-elasticity with a given
temperature distribution", "Thermo-elasticity with a computed temperature", "Axisymmetric Linear
Elasticity" and penalty contact [S1], but no plasticity or damage. PyPI has only an sdist. `uv
pip install sfepy` on 3.14 failed: "No CMAKE_C_COMPILER could be found" (Run). conda-forge is
the binary route [S2]. **Not useful:** scikit-fem covers the same ground with no compiled code.

**GetFEM** (5.5, LGPL). Strong in contact and friction, but the Python interface isn't on PyPI:
it comes from Debian/Ubuntu packages, a source build (C++14), or a Windows installer for "GetFEM
5.4 interface for 64bits Windows and Python 3.7 of Anaconda 3" [G1]. **Not useful.**

**Kratos Multiphysics** (10.4.4). "Free under BSD-4" [R1]; `kratos/license.txt` carries the
advertising clause ("This product includes Kratos Multi-Physics technology") (Read). Its README
lists applications for structural mechanics, contact structural mechanics, nonlinear
constitutive laws (plasticity, damage) and DEM [R1]; heat conduction is a separate PyPI
application, `KratosConvectionDiffusionApplication`.
- **Install:** cp314 wheels for Linux and Windows. The core, StructuralMechanics and
  ConvectionDiffusion applications imported on 3.14 (Run), printing ASCII banners to stdout.
- **Workflow:** problems are driven by JSON parameter files and `.mdpa` mesh files, a large
  framework for what v2 needs.
- **Verdict: not useful** now.

**OpenSeesPy** (3.8.0.0). It installed and ran on CPython 3.14.10: the B4 beam was exact (Run).
But the OpenSees licence (`COPYRIGHT`, UC Regents) grants use "by educational, research, and
non-profit entities for noncommercial purposes only" and "by other entities for internal
purposes only"; commercial distribution needs a licence from UC Berkeley (Read). That rules it
out for an MIT project with a hosted app (M5). **Not useful.**

**CalculiX** (ccx 2.23, GPL-2.0) [C1]. A thermo-mechanical solver with penalty contact and
Coulomb friction. It runs as an external executable fed input decks: Linux binaries from the
author, Windows builds from third parties [C1]. The Python wrappers are pygccx (GitHub only;
GPL-3 stated as the author's intent in a forum post) and ccx2paraview 3.2.0 (GPL-3.0, last
release 2024-12-19); pycalculix 1.1.4 dates from 2019 [PyPI]. A subprocess writing decks breaks
ADR 0002. **Not useful.**

**PyMFEM / MFEM** (4.10.0.1, BSD-3-Clause). PyPI has cp311–cp314 Linux wheels and no Windows
wheel: uv resolves Windows to an empty `mfem==0.0.3`. The README still says binary installs are
"available only on linux platforms (Py38-312)" [M1]; MPI needs a source build [M1]. `mfem.ser`
imported on 3.14 (Run). It's a C++-style SWIG API with no weak-form language. **Not useful.**

## 9. Notes only: JAX-FEM, torch-fem, Code_Aster

- **JAX-FEM** 0.0.12 (2026-06-13): GPL-3.0 on GitHub, but a BSD classifier on PyPI; its wheel
  declares no dependencies. A differentiable FE for research. Not useful.
- **torch-fem** 0.14.1 (2026-10-28): MIT. On Linux it resolves to 63 packages, including torch
  2.15 and the CUDA 13 libraries (Run, `uv pip compile`). Not useful.
- **Code_Aster:** conda-forge `code-aster` 18.0.12 (2026-04-03), linux-64 only; licence field
  "GPL-3.0-only, CECILL-C, Apache-2.0, LGPL-3.0-only" [A1]. Not on PyPI. Not useful.

---

## 10. Masonry-specific packages

### 10.1 COMPAS TNA and TNO

**What they give.**
- **compas_tna** does "Form finding of funicular networks in compression with vertical loads using
  Thrust Network Analysis" [B1].
- **compas_tno** finds "admissible thrust networks in masonry vaulted structures" [B2]. Given a
  form diagram (the network's plan) and an envelope (intrados and extrados), it optimises the
  force densities and node heights for least or most thrust, or least thickness. Its solvers are
  SLSQP from SciPy and Clarabel through CVXPY; IPOPT and MOSEK come through conda [B2].
- **The README warns** that "As of Summer 2025 COMPAS TNO is being refactored to work with COMPAS
  2.0 … A Legacy version is available at secondary branches" [B2].
- **TNO's own publication list** includes the paper recorded in `masonry-statics.md` as [M3]
  (Maia Avelino et al., 12th SAHC, Barcelona; dated 2020 there and 2021 in TNO's list) [B2]. Its
  numbers are the test values below.

**Installation (Run).** `compas_tno` 0.4.0 installs on 3.14 (28 packages, 450 MB, including
CVXPY, OSQP, SCS, Clarabel, HiGHS and compas_cgal).
- **With the repo's NumPy (2.5.4) every analysis tried failed** (the arch, and the cross vault's
  least and most thrust), and the arch failed with 2.4.6 too. The error is in `compas_tna 0.9.0`,
  `envelope/parametricenvelope.py` line 180: `float(zub[i])` on a one-element array raises "only
  0-dimensional arrays can be converted to Python scalars".
- **With NumPy 2.3.5 it runs.** The repo locks NumPy 2.5.4, and PyNite needs ≥ 2.4, so TNO can't
  share the engine's environment.
- **Its logs:** the analyses print CVXPY logs to stdout even with `printout=False`.
- **The umbrella environment** the README points to, `compas_masonry` 0.4.2, depends on
  compas_lmgc90, which has no cp314 wheel, so on 3.14 uv resolves it to 0.3.0 (Run,
  `uv pip compile`).

**Benchmarks (Run, NumPy 2.3.5, SLSQP).**

| Case | TNO | Published | Time |
|---|---|---|---|
| B1 semicircle, least thickness, TNO's defaults (`create_minthk_analysis`, `BarrelVaultEnvelope`) | t/R = 0.0436 (41 and 81 nodes), 0.0370 (21) | 0.1075 | 0.1–0.5 s |
| the same, support heights fixed at the springing (variables q and t only) | stays at the starting 0.20 and reports success | 0.1075 | < 0.4 s |
| hemisphere t/R 0.10, radial diagram (241 nodes), least thrust | T/W = 21.0 % | 19.8 % [M3]; Lau "about 20 %" | 37 s |
| the same, most thrust | failed: "Inequality constraints incompatible" | 430 % [M3] | 65 s |
| cross vault 10 × 7.5 m, t = 0.5 m, corners supported (225 nodes), least thrust | 66.8 % | 67.5 % [M3] | 21 s |
| the same, most thrust | 92.9 % | 96.7 % [M3] | 10 s |
| the same, least thickness | t'/R = 0.067 | 0.061 [M3] | 12 s |
| hemisphere, least thickness | crashed: `TypeError` in `compas.tolerance.geometric_key` | 0.041 [M3] | – |

Why the arch fails: TNO bounds the thrust line vertically, intrados to extrados at each node's
plan position, and keeps the support heights as variables. At the springing's plan position the
upper bound is the extrados height √((R + t/2)² − R²), about 0.2 R for t/R 0.04
(`compas_tna/envelope/barrelvault.py`). So the line "lands" 0.21 R above the springing, inside the
ring, and the masonry below that point carries nothing. **The 0.044 is unsafe by a factor of 2.5.**
Vertical bounds are sound for shallow vaults and loose where the surfaces turn vertical. The
published 0.1079 for this arch [M3] was evidently obtained with set-ups the current public API
doesn't make simple.

Fixing the case was tried: the example scripts' `form.centroid` had to be patched for a line
diagram (it divides by zero area), and fixing the support heights left the optimiser stuck.

**Fit for kilns.** It is the only package here that does N6 (groin vaults) and 3-D domes. Where it
works its numbers sit within 1–10 % of the published ones, but it needs an expert's set-up, it is
slow (10–65 s per solve), it failed on three of the eight runs above and gave an unsafe answer on
a fourth, and its NumPy pin clashes with the engine's.

**Licence.** MIT (both; `LICENSE`, "Block Research Group - ETH Zurich") [B1, B2].

**Verdict: not useful as an engine dependency.** Keep it as an outside cross-check for vaults, in
its own environment: for N6, and for any 3-D thrust network v2 builds.

### 10.2 Rigid-block equilibrium: compas_cra and compas_rbe

**compas_cra** 0.8.0: "Coupled Rigid-Block Analysis (CRA) implementation using COMPAS framework"
(Kao et al., *Computer-Aided Design* 146, 2022, doi 10.1016/j.cad.2022.103216) [B3].
- **Wheels:** CPython 3.9–3.13, with IPOPT 3.14.19 compiled in [B3]. On 3.14, uv falls back to
  0.6.0, which needs Pyomo and an external IPOPT; a source build of 0.8.0 failed for want of a C++
  compiler (Run).
- **On 3.13** it installed from wheels (Run).
- **Its public solvers** (`rbe_solve`, `cra_solve`, `cra_penalty_solve`) take the blocks' own
  weight as the only load: `external_force_setup` puts −volume × density in z and nothing else.
  They check whether an assembly stands (the examples tilt it); they don't find a load factor
  under an applied thrust. So the wall case B2 can't be posed without changing its code (Read,
  `equilibrium/cra_helper.py`, `cra_nlp.py`).
- **Its method is the right kind:** 3-D blocks with non-associative friction, the case where an
  LP's answer can be too high (Gilbert et al. 2006, cited in the structure review).
- **Verdict: not useful now**; watch for cp314 wheels and an external-load API.

**compas_rbe** 0.1.2rc0 (2021-05-05; classifiers Python 3.4–3.7): stale. **Not useful.**

### 10.3 LMGC90 and YADE

**LMGC90** is non-smooth contact dynamics for "large collections of interacting objects" [L1],
under CeCILL, a GPL-compatible French licence (CSMA 2026 abstract [L2]). It is not on PyPI.
compas_lmgc90 0.1.11 wraps it. PyPI has wheels for CPython 3.10–3.13 on Linux and Windows, none
for 3.14. Its README still says to build from source with gfortran, OpenBLAS and CMake, and that
"Windows is not currently supported" [L3]. **Not useful:** a dynamic DEM is far more than a
statics check needs.

**YADE** (GPL-2 [Y1]). The install page lists Ubuntu/Debian packages, Docker and source, Linux
only, and advises "better avoid installing python packages with pip or conda" [Y2]. The PyPI
name `yade` is an unrelated package. A DEM for granular media. **Not useful.**

---

## 11. The baseline: SciPy `linprog` with HiGHS

`scipy.optimize.linprog(method="highs")` solves "Linear programming: minimize a linear objective
function subject to linear equality and inequality constraints", using HiGHS (Huangfu, Galabova,
Feldmeier & Hall). It returns the dual values ("marginals … shadow prices") with the solution
[H1]. It ships inside SciPy, already an engine dependency, so it adds nothing. Two formulations
were written; their LP cores are about 50 lines (arch) and 100 lines (blocks).

**B1, the arch (`arch_rigid_block_lp.py`).** Livesley's static method (from memory: Livesley,
1978) on voussoirs with radial joints: the crown thrust H and its moment are the unknowns. At
every joint the line of thrust must lie between the intrados and extrados with compression only
(and, optionally, |V| ≤ μN). Least thickness by bisection, one small LP per step.

| Weights | Voussoirs per half | η | Error | H/(w r) | 50 LPs |
|---|---|---|---|---|---|
| on the centre line | 10 / 40 / 160 / 640 | 0.107463 / 0.107411 / 0.107426 / 0.107426 | +0.035 / −0.014 / 0.000 / 0.000 % (vs 0.107426) | 0.6218 | 0.08 / 0.10 / 0.22 / 1.2 s |
| true centroids | 160 / 640 | 0.107477 / 0.107477 | −0.001 % (vs 0.107478) | 0.6209 (printed 0.621) | 0.24 / 1.1 s |

- **Friction at μ 0.5 and 0.4** leaves η unchanged. At μ 0.3 no thickness up to t/R 0.30 stands:
  at the horizontal springing joint the shear H exceeds 0.3 × the half weight (H/(W/2) ≈ 0.40).
- **At t/R 0.20** the least and most thrust, summed over both supports, are 0.308 W and 0.509 W,
  against TNA's 0.316 and 0.512 [M3].
- **N1 follows directly:** t/r 0.095 has no admissible state; 0.11 and 0.22 do. This is implied
  by the bisection (feasibility only grows with t); those three thicknesses were not run
  separately.

**B2, walls and buttresses (`wall_buttress_lp.py`).**
- **The model:** general 2-D rectangular blocks on rigid ground, two contact points per joint,
  N ≥ 0 and |T| ≤ μN at each.
- **The loads:** weights; V at the springing; the thrust H on the wall's inner face. Maximise H.
- **Test inputs:** γ 20 kN/m³, μ 0.6, a 9 in (0.2286 m) wall 1.2 m high, springing at 0.9 m,
  V = 6 kN/m, 75 mm courses.

| Case | LP H (kN/m) | Hand H | What governs |
|---|---|---|---|
| A1 wall as one block | 1.45877 | 1.45877 | base overturns: (V + W)·(b/2)/h_s |
| A2 the same wall in 16 courses | 1.45877 | 1.45877 | the same: the lowest joint |
| A3 thrust on the top course, b 13½ in, h 0.6 m, V 10, μ 0.3 | 3.15430 | 3.15430 | the top joint slides, μ(V + one course); the base would need 4.0333 |
| B 9 in buttress bonded in (18 in courses) | 5.07309 | 5.07309 | base overturns about the buttress's toe |
| C buttress dry-laid against the wall (two blocks) | 2.93941 | 2.93941 | the buttress slides on its base with the wall hanging on it by friction: H = [(b₁/2)(W₁ + V) + W₂b₂/2 + b₂μ²W₂/(1 − μ²)]/h_s (Derived) |
| C2 the same, both coursed (48 joints) | 2.82639 | – | between A2 and B, as it must be |
| Base resultant of A1 at H = 1.0 kN/m | 0.19265 m from the thrust face | 0.19265 m | e/b = 0.343: outside the middle third, inside the base |

Each case solved in 1–8 ms.
- **The hand values are exact for A1–B:** a single column of blocks is statically determinate
  joint by joint. For C the closed form is the LP's own optimum, derived by hand: resultants at
  the toes, the interface friction at its limit, and the buttress's base friction binding.
- **Friction is associative** here, as in every LP formulation. Where sliding governs an
  indeterminate assembly (C, C2) the true collapse load can be lower (Gilbert, Casapulla & Ahmed
  2006, cited in the structure review, not read). An iterative non-associative scheme or CRA's
  method would be the next step.
- **An earth bank** fits the same frame as Coulomb wedges (a soil block on a slip plane), but
  needs the soil's weight and friction angle, which no file in `docs/research/` gives.

**Scaling (`wall_bond_scale.py`, sparse matrices).** A running-bond wall loaded by λ × its weight
horizontally (the tilting test), every brick a block. As a check, a single column of 16 courses
gave λ = 0.190500, the hand value b/H.

| Wall | Blocks | Joints | Variables | λ | HiGHS interior point | HiGHS dual simplex |
|---|---|---|---|---|---|---|
| 16 courses × 8 bricks | 136 | 368 | 1,473 | 0.6000 (base slides) | 0.18 s | 0.45 s |
| 32 × 16 | 528 | 1,504 | 6,017 | 0.5241 | 2.2 s | 6.4 s |
| 48 × 24 | 1,176 | 3,408 | 13,633 | 0.4881 | 11.2 s | – |
| 64 × 32 | 2,080 | 6,080 | 24,321 | 0.4709 | 41.0 s | – |

The time grows about as the square of the brick count. A first attempt that also tried 96 × 48
(4,608 bricks) on the default method was stopped after 11 minutes. So:
- **a course-by-course model** (tens of blocks per wall) solves in milliseconds;
- **a brick-by-brick wall** of a few hundred bricks solves in seconds;
- **a brick-by-brick 3-D kiln** would need a sparser formulation or a stronger solver first.

**Fit for kilns.**
- **Everything the first step needs in 2-D** is in these two formulations: thrust lines in any arch
  shape (the voussoirs are just geometry); minimum and maximum thrust, so hot and cold; walls,
  bonded and dry-laid buttresses, jambs and chimneys as stacks of blocks; sliding at every bed
  joint.
- **Domes as Heyman's lunes** are the arch LP with the lune's weights; hoop forces add one
  variable per ring (not run).
- **Every constraint is a written formula and the duals name the binding joints,** so the result
  carries its working as the engine requires.
- **It is pure** (ADR 0002), fast, and on Windows already.

**Verdict: adopt** as v2's solver for arches, walls and buttresses. It takes every solve; v2
writes the formulations (the probes' LP cores are about 50 and 100 lines). For non-associative
friction the same HiGHS solves a MILP (`statics-combinations.md` §3).

---

## 12. Frames: PyNite and anaStruct

**PyNite** 3.2.1: "An easy to use elastic 3D structural engineering finite element analysis
library for Python" [P1].
- **Features:** 3-D frames, P-Δ, plates, "Tension-only and compression-only elements", springs,
  and load combinations; "its output is tested against a suite of textbook problems with known
  solutions" [P1].
- **No thermal loads:** neither "thermal" nor "temperature" appears in the package (Read). A hot
  rod's growth would have to go in as equivalent end forces.
- **Install:** MIT; pure Python. It needs NumPy ≥ 2.4 and adds matplotlib and prettytable.
- **B4:** M and the deflection exact (Run).
- **Verdict: proposed.** It takes the whole frame analysis off v2's hands: posts, angles and rods
  under the hot thrust, with the rods tension-only. With the arch's LP it gives the thrust along a
  real frame (`statics-combinations.md` §2). v1's hand AISC checks remain the member checks.

**anaStruct** 1.7.1: 2-D frames, with cp314 wheels; B4 exact (Run). Its `LICENSE.txt` is
LGPL-3.0 but its `pyproject.toml` says GPL-3.0-or-later (Read). **Not useful:** PyNite does more,
under MIT.

OpenSeesPy also solved B4 exactly; see §8 for its licence.

## 13. Meshing: gmsh, pygmsh, meshio, netgen.occ

- **gmsh** 4.15.2: "GNU General Public License (GPL) (version 2 or later, with an exception to
  allow for easier linking with external libraries)"; closed-source integration needs a
  commercial licence [E1]. Its wheel is `py2.py3`, so any CPython works.
  - On this host and in the server image the import failed on `libGLU.so.1`, then on
    `libgomp.so.1`. With `libglu1-mesa libxcursor1 libxft2 libxinerama1 libgomp1` (7 MB with
    `libquadmath0`) it meshed the engine's STEP arch ring into 26,327 second-order tetrahedra
    (42,060 nodes) in 0.9 s (Run).
  - **Not useful in the engine:** a GPL library linked in-process makes the distributed whole
    GPL. As a developer's tool outside the engine it is fine.
- **pygmsh** 7.1.17 (GPL-3.0; last release 2022, last push 2023): stale. **Not useful.**
- **meshio** 5.3.5 (MIT): reads and writes Gmsh `.msh`, VTK/VTU, XDMF, Abaqus `.inp` and Exodus
  [E2]; no release since 2024-01, no push since 2024-07. **Not needed** unless meshes are
  exchanged with other tools.
- **netgen.occ** (with NGSolve, LGPL-2.1) read and meshed the same STEP (§7). It is the meshing
  route if 3-D FE is ever needed.

## 14. Commercial reference points

- **LimitState:RING** (version 4): "uses rigid block analysis, underpinned by rigorous Limit
  Analysis theory"; "The line of thrust and pattern of hinges are found using optimization",
  including "combined sliding / hinging modes" and ring separation [X1]. It is the same method as
  the baseline (§11), for masonry arch bridges: confirmation that the LP route is industry
  practice.
- **3DEC / UDEC** (Itasca): "hybrid (DEM + continuum) simulation" for "blocks of discontinuous
  material" such as "jointed rock or masonry bricks", with "Coupled mechanical, hydro, and
  thermal solutions"; subscription or perpetual licences [X2]. A reference for dynamic,
  joint-by-joint masonry with heat, not something v2 needs to reproduce.
- **Abaqus** (Dassault Systèmes SIMULIA): general nonlinear FE with contact, damage and coupled
  thermo-mechanics (from memory; not read this round).

---

## 15. Ranked by what each takes off v2's hands

| # | Tool | Takes off v2's hands | v2 would still write | Licence | Verdict |
|---|---|---|---|---|---|
| 1 | **SciPy `linprog` and `milp` (HiGHS)**, already a dependency | every LP and MILP solve: arches (least thickness, least and most thrust), walls, buttresses, jambs and chimneys as rigid blocks; non-associative friction for course-level models (`statics-combinations.md` §3) | each formulation: about 50 lines for an arch, 100 for blocks, 150 more for non-associative friction | BSD-3-Clause | **adopt** |
| 2 | PyNite | the whole frame analysis: stiffness, member forces, deflections, tension-only rods | the frame from the design; its coupling to the arch (`statics-combinations.md` §2) | MIT | **proposed** |
| 3 | COMPAS TNO | all of 3-D thrust networks: form diagrams, envelopes, optimisation | an export and a runner in its own environment (NumPy < 2.4), and checks of its answers | MIT | not useful as a dependency; **cross-check only** |
| 4 | NGSolve (netgen.occ) | meshing the engine's STEP solids; 3-D FE assembly and fast solves | the weak forms; `libquadmath0` in the image | LGPL-2.1 | **proposed** (only for 3-D) |
| 5 | scikit-fem | FE assembly, 2-D and axisymmetric | the weak forms (about 60 lines each), and the hot data no source gives | BSD-3-Clause | **proposed** (waits on data) |
| 6 | compas_cra | 3-D contact detection | everything else: its IPOPT verdicts are local (`statics-combinations.md` §3); no cp314 wheel | MIT | not useful now |
| 7 | FEniCSx | FE assembly and solving | a compiler and MPI at run time; MOSEK for limit analysis | LGPL-3.0 | not useful now |
| 8 | fedoo | FE with contact, cohesive joints and rigid bodies | – (GPL-3.0 rules it out) | GPL-3.0 | not useful |
| 9 | Kratos | a multiphysics framework | its JSON and mdpa workflow | BSD-4-Clause | not useful |
| 10 | gmsh | meshing STEP | – (GPL in process) | GPL-2.0+ | developer tool only |
| – | SfePy, GetFEM, PyMFEM, CalculiX, OpenSeesPy, anaStruct, LMGC90, YADE, compas_rbe, pygmsh, meshio, JAX-FEM, torch-fem, Code_Aster | – | install, licence or scope (§8–§13) | – | not useful |

How the leading candidates sit with the engine's rules, CI and the server image (Run, except
where noted):

| Tool | Pure engine (ADR 0002) | In the server image | Added weight |
|---|---|---|---|
| SciPy HiGHS | yes: in-process, no I/O | already there | none |
| PyNite | yes | wheels only | matplotlib, prettytable |
| scikit-fem | yes | wheels only | +8 MB with PyAMG |
| NGSolve | yes; compiled C++, parallel only inside a `TaskManager` block | needs `apt-get install libquadmath0` | about 250 MB over NumPy (310 MB venv, NumPy 59 MB) |
| COMPAS TNO | prints solver logs to stdout | can't share the engine's NumPy 2.5.4 | 450 MB venv |
| FEniCSx | JIT writes C modules to `~/.cache/fenics`; MPI at import | needs gcc and libc6-dev (+191 MB) and `mpich` | 403 MB venv |
| fedoo | yes | wheels only; MKL for speed | 263 MB, or 1.2 GB with MKL |

GitHub's Linux CI runners were not tried; they would need the same packages as the image.

## 16. What this does not settle

- **Thermal stress, creep and spalling stay out of v2's statics**, for want of data: hot E and
  tensile strength of IFB, firebrick and castable, joint tensile and hot cohesive strength, creep
  laws (`arch-thrust-theory.md` §6; `refractory-movement-and-mortar.md` §3). B3 shows the software
  side is small: about 60 lines per package.
- **Non-associative friction:** the LP's answer is an upper bound where sliding governs an
  indeterminate assembly (case C). For course-level models a MILP on the same HiGHS settles it:
  case C's least collapse thrust is 23.6 % below the LP's (`statics-combinations.md` §3).
- **3-D thrust networks for groin vaults (N6)** are not covered by the baseline. TNO is the
  reference; a 3-D rigid-block LP built from the engine's own brick courses is the alternative to
  try.
- **Spreading supports (N5)** need the arch's geometry updated as it opens. The LP gives the
  minimum-thrust state at each step; the sources in `engine-v2-negative-cases.md` §5 are still
  unread.
- **Not run:** Kratos, SfePy, GetFEM, CalculiX, LMGC90 and YADE beyond what is stated; NGSolve on
  Windows; FEniCSx's Windows wheels; compas_cra on a thrust; a dome by lunes in the baseline.
- **Not read:** Livesley (1978); Gilbert & Melbourne (1994); Roark & Young (5th ed.) itself; the
  CSMA 2024 paper on 3MAH; Kratos's validation examples.

## Sources

Package metadata: PyPI JSON API (https://pypi.org/pypi/NAME/json), Test PyPI
(https://test.pypi.org/pypi/fenics-dolfinx/json) and the GitHub REST API
(https://api.github.com/repos/OWNER/REPO), all read 2026-11-09.

- [T1] S. Timoshenko, S. Woinowsky-Krieger, *Theory of Plates and Shells*, 2nd ed., McGraw-Hill
  1959, §14 "Thermal Stresses in Plates with Clamped Edges", pp. 49–50, Eq. (51). OCR text of
  https://archive.org/details/TheoryOfPlatesAndShells (the copy `domes-over-doors.md` [D1] cites).
- [T2] Itasca, FLAC3D verification "Conduction in a Hollow Cylinder" (analytical solution after W.
  Nowacki, *Thermoelasticity*, Addison-Wesley 1962).
  https://docs.itascacg.com/pfc700/flac3d/zone/test3d/Thermal/HollowCylinderConduction/hollowcylinderconduction.html
- [T3] Autodesk Fusion, "Thermal stress 01: hollow cylinder with thick walls and temperature
  gradient" (cites Roark & Young, 5th ed., 1975, p. 585, §15.6, case 16).
  https://help.autodesk.com/cloudhelp/ENU/Fusion-Simulate/files/GUID-7F7FDC95-AE83-455F-BDB1-42833851A911.htm
  Its page says the inside is the colder face yet prints the inner face in compression; only its
  magnitudes are used here.
- [F1] DOLFINx README. https://github.com/FEniCS/dolfinx
- [F2] DOLFINx demos. https://docs.fenicsproject.org/dolfinx/main/python/demos.html
- [F3] FEniCS, citing. https://fenicsproject.org/citing/
- [F5] J. Bleyer, `dolfinx_optim` and `fenics_optim` (MOSEK); Bleyer & Hassen, "Automated
  formulation and resolution of limit analysis problems", *Computers & Structures* 2021,
  arXiv 2005.04779. https://fenics-optim.readthedocs.io ; https://bleyerj.github.io/talks/PDESoft-2024
  (search results; the repositories weren't read).
- [D1] fedoo README. https://github.com/3MAH/fedoo
- [D2] fedoo documentation 1.1.0. https://3mah.github.io/fedoo-docs/stable/
- [K1] scikit-fem README. https://github.com/kinnala/scikit-fem
- [N1] NGSolve i-tutorials. https://docu.ngsolve.org/latest/i-tutorials/index.html
- [S1] SfePy gallery. https://sfepy.org/doc-devel/examples/gallery.html
- [S2] SfePy installation. https://sfepy.org/doc-devel/installation.html
- [G1] GetFEM download. https://getfem.org/download.html
- [R1] Kratos README. https://github.com/KratosMultiphysics/Kratos ; licence
  https://raw.githubusercontent.com/KratosMultiphysics/Kratos/master/kratos/license.txt
- OpenSees licence: https://raw.githubusercontent.com/OpenSees/OpenSees/master/COPYRIGHT
- [C1] CalculiX. http://www.dhondt.de/ ; pygccx https://github.com/calculix/pygccx (search
  result); CalculiX forum, "Python framework for CalculiX",
  https://calculix.discourse.group/t/python-framework-for-calculix/1210
- [M1] PyMFEM README. https://github.com/mfem/PyMFEM
- [A1] conda-forge `code-aster`. https://anaconda.org/conda-forge/code-aster (search result)
- [B1] compas_tna README. https://github.com/BlockResearchGroup/compas_tna
- [B2] compas_tno README and docs (installation, solvers, publications).
  https://github.com/BlockResearchGroup/compas_tno ; https://blockresearchgroup.github.io/compas_tno
- [B3] compas_cra README and docs. https://github.com/BlockResearchGroup/compas_cra
- [L1] LMGC90. https://lmgc90.pages-git-xen.lmgc.univ-montp2.fr/lmgc90_dev/
- [L2] CSMA 2026 abstract on LMGC90 (CeCILL). https://csma2026.sciencesconf.org/687100/document
  (search result)
- [L3] compas_lmgc90 README. https://github.com/BlockResearchGroup/compas_lmgc90
- [Y1] Debian copyright for YADE 2025.2.0-1.
  https://sources.debian.org/src/yade/2025.2.0-1/debian/copyright
- [Y2] YADE installation. https://yade-dem.org/doc/installation.html
- [H1] SciPy 1.18 `linprog`.
  https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
- [P1] PyNite README. https://github.com/JWock82/Pynite ; anaStruct
  https://github.com/ritchie46/anaStruct (`LICENSE.txt`, `pyproject.toml`)
- [E1] gmsh. https://gmsh.info/ ; pygmsh https://github.com/nschloe/pygmsh
- [E2] meshio. https://github.com/nschloe/meshio
- [X1] LimitState:RING. https://www.limitstate.com/ring
- [X2] Itasca 3DEC. https://www.itascacg.com/software/3DEC
- [M3] Maia Avelino, Iannuzzo, Van Mele & Block, SAHC 2020, as recorded in `masonry-statics.md`.
