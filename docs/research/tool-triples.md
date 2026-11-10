# Tools in threes: what each combination takes off engine v2's hands

Surveyed 2026-11-09 to 11-10, after `statics-software.md` (single tools) and
`statics-combinations.md` (pairs). No engine changes were made.

**The yardstick (the user, 2026-11-09):** a tool is judged by whether there is a way to use it so
the project doesn't have to solve that part itself. Matching a rule or a past result counts for
nothing. The checks below only show that a tool was driven correctly.

- Probes: `scratch/toolsets/` (git-ignored, as the other surveys' probes are), one folder per
  combination: `whole-kiln/`, `thrust-networks/`, `view-factors/`, `gas-path/`. Each has a
  `RESULTS.md` with the steps, the scripts and a summary table.
- Extra packages came through `uv run --with` overlays. The repo's environment wasn't touched.
- Marks: **Run** (computed here), **Read** (read in the source), **Derived** (worked here),
  "from memory". Temperatures, loads and fuels marked as test inputs are not engineering data.

## 0. Short answer

| Combination (X + Y + Z → result) | Takes off v2's hands | v2 would still write | Verdict |
|---|---|---|---|
| **build123d + HiGHS + PyNite** → statics of a whole kiln section, frame included | the blocks' solids and contacts, every LP solve, the frame analysis | about 250–300 lines of glue, the pair's coupling (~100), working steps, all of 3-D | **adopt** as v2's statics path (§1) |
| **Cantera + fluids + ht** → the gas path, burner to chimney top | gas composition and properties, friction, fitting losses, convection | about 150–250 lines: segments, the draft sum, the flow solve, range guards, working | **adopt** (§2) |
| **build123d + pyViewFactor's kernel + `radiation.py`** → view factors for any chamber shape | geometry, meshing, the view-factor integral (unobstructed) | face naming, mesh/group/closure glue (~120), a partial-shadowing test (100–200) | **adopt the kernel, copied as NumPy**, not the package (§3) |
| **compas_tna + HiGHS + build123d** → thrust networks for domes and groin vaults | diagram bookkeeping, the vertical LP solve, intrados/extrados heights | the search over force distributions (300–600), moving springings, loading (~150) | **partial**: keep HiGHS and build123d's ray queries; compas_tna's diagram generators at most (§4) |

## 1. build123d + HiGHS + PyNite: whole-kiln statics (Run)

`scratch/toolsets/whole-kiln/` (`blocks_occ.py`, `section2d.py`).

- **Contacts (build123d 0.13.0 on OCCT 8.0):** a pairwise face-against-face method finds every
  contact and its area to the printed digits, forgives gaps and overlaps up to a tolerance, and
  runs at about 5 ms a contact (6.6 s for a 449-brick wall). OCCT's General Fuse is about 3×
  faster and alone finds curved contacts, but needs a fuzzy value for gaps, and an overlap of
  1e-4 in loses the contact to a sliver.
- **The section:** a 12 in slice across Olsen's fast-fire kiln (`examples/olsen/fast-fire.yaml`),
  46 blocks: 14 courses a wall, skewbacks, 13 arch bricks, ground and frame. K-23 at 32.03
  lb/ft³, friction 0.6 cold and 0.50 hot, from `docs/research`.
  - The arch alone reproduces the pair's least thrust, 11.6705 lb/ft (−0.58 % at 13 bricks,
    exact at 52 and 320).
  - Blocks from the layout numbers and blocks cut from the engine's own solids agree within 0.1 %.
  - With the walls, the least frame force is 7.08 lb/ft a side: the walls buttress.
  - No frame: HiGHS proves the section infeasible. Cold, the thrust has no upper bound; hot, the
    arch sliding on its skewbacks caps it at 580 lb/ft.
  - Contacts 0.13–0.31 s; the two LPs 11–15 ms.
- **With PyNite** (4 and 36 slices over a 36 in bay; 0.2 and 1.3 s): the bay's ends hold the arch
  at the hot bound, 580 lb/ft; mid-bay the angle gives and the thrust drops to 7.1 lb/ft. The
  angle reaches about 21,000 psi and the rods about 600 lb; not judged, as no allowable was set.
- **Not run:** 3-D (corners, returns, the arch along its length), and LP rows for curved
  contacts.

## 2. Cantera + fluids + ht: the gas path (Run)

`scratch/toolsets/gas-path/` (`gas_path.py`, `cantera_probe.py`, `licences.py`).

- **The run:** Olsen's fast-fire wood downdraft, ash-pit mouths → grates → fireboxes → inlet
  flues → chamber → exit flue → 14 ft chimney, on test inputs (temperatures, λ 1.2, roughness,
  fuel). Draft 41.5 Pa (38.1 from the column); the largest loss the turn up the chimney, 14.5 Pa;
  0.087 kg/s of air; the chimney gas cools 1285 → 1167 °C by convection. Solves in 50–65 ms.
- **Cantera** (BSD-3, 62 MB): composition at any λ and temperature (CO below λ 1), density,
  viscosity, conductivity, heat capacity, stream mixing.
- **fluids** (MIT, 2.5 MB): Colebrook friction; entrance, exit, contraction, expansion, bend and
  bar-grate losses; the outside air column.
- **ht** (MIT, 2.4 MB): flue and shelf convection coefficients.
- **Faults (Run):**
  - ht's method selector crosses three laminar-entry names, and at Re 3600 picks a correlation
    stated for Re ≥ 10⁴. v2 calls named correlations only.
  - Cantera evaluates at 150 K and 5000 K without a warning, outside most species' 200–3500 K.
    v2 checks the range itself (ADR 0009).
  - fluids' fittings are for round pipes. On rectangular brick flues they are an assumption until
    rectangular-duct values (Idelchik) are sourced.
  - Neither fluids nor ht has a chimney-draft function; the column sum is v2's.
- **Not covered by any of the three:** gas radiation (H6), fuel-bed and setting resistance, brick
  roughness. Each needs sourced data.

## 3. build123d + pyViewFactor + `radiation.py`: view factors for any chamber (Run)

`scratch/toolsets/view-factors/` (`vfmesh.py`, `numpy_kernel.py`, `dome.py`, and others).

- **The chain:** the engine's cavity solid → faces named by place → OCCT tessellation → refined
  facets → pyViewFactor's contour-integral matrix → grouped by face → a least-change closure →
  `radiation.Enclosure`.
- **Checks (≤ 1800 facets a mesh):**
  - box: 4.1e-9 from `radiation.box` at 640 facets;
  - sprung arch: 9.9e-4 from `covered()`, all of it the mesh's crown area 0.1 % short (7.3e-7 on
    the mesh's own area);
  - dome (test dimensions): 1.9e-3 from `coaxial_discs` + `covered`; OCCT's angular tolerance,
    not the linear one, sets the curved mesh;
  - a catenary with a door and flue, a shape v1 refuses: energy balances to 8e-11 W; 12 → 32
    chords moves factors up to 1e-2, mostly where the wall/crown split lands.
- **Obstruction fails:** with a bag wall and setting, one centroid-to-centroid ray per pair leaves
  rows off by 1.5–4.7e-2 and a symmetric chamber slightly asymmetric. The closure then moves
  factors up to 8.4e-3, hiding the error, not fixing it. Unobstructed, the closure moves them at
  most 4e-6.
- **Cost:** about 5 s at 1250–1500 facets after a 6.7 s first-call compile; time and memory grow
  as the square of the facets.
- **The package's weight:** 1.1.0 (MIT) needs pyvista and numba at import: 220 MB new to the repo
  on Linux, VTK the repo avoids on purpose, and numba caps NumPy below 2.6. A NumPy-only copy of
  its kernel matches it to 2.5e-7 but takes 32.6 s against 4.7 s at 1252 facets.
- **Verdict (Derived):** copy the kernel in as plain NumPy (about 70 lines, credited to AREP,
  MIT), keep pyViewFactor as a test reference only. v2 writes the face naming (20–40 lines a
  chamber family), the mesh, group and closure glue (~120), and a partial-shadowing test
  (100–200). The closure follows the smoothing of zonal exchange areas (Larsen & Howell 1986;
  Lawson 1995): **from memory, not sourced**; it needs a source here before v2 uses it.

## 4. compas_tna + HiGHS + build123d: thrust networks (Run, Read)

`scratch/toolsets/thrust-networks/` (`tna_lp.py`, `dome.py`, `dome_fine.py`, `groin.py`,
`groin_q.py`, `b123d_probe.py`).

- **Installs:** compas 2.15.1 and compas_tna 0.9.0 as an overlay on the engine's CPython 3.14.10
  and NumPy 2.5.4. Its envelopes fail on NumPy ≥ 2.4 (`ParametricEnvelope`, `float()` on an
  n × 1 array; Read).
- **The method (Read):** Block & Ochsendorf 2007 (J. IASS 48(3), Eq. 4) and 2008 (SAHC, Eq. 1):
  with a fixed force diagram, the heights and the inverse scale r solve as one LP. Choosing the
  force distribution in an indeterminate pattern is left to the user (2007 (e); 2008 (e)).
- **What each took:** compas_tna builds dome and cross form diagrams and converges its horizontal
  step (0.4–0.5 s), but the distribution it settles on is arbitrary. The vertical LP is about 40
  lines on SciPy, 3–9 ms for about 240 nodes. build123d's intrados and extrados heights match a
  sphere's closed form to 6 digits (0.6 ms a ray; 0.07 ms through OCP directly); weights from
  prism Booleans are slow (13 ms a face, about 90 % of the run time).
- **Dome:** least t/R 0.161 with compas_tna's force diagram, 0.079 with a lune pattern. Its form
  diagram stops at the median radius and misses 14 % of the weight. Fixed supports at the base
  joint's middle give about 0.080; a springing free to move across the joint about 0.043
  (Derived). Allowing hoop compression never changed the answer; why is not settled.
- **Groin vault:** no admissible state at any t/R up to 0.30 with compas_tna's force diagram; with
  supports at z = 0 the range of r is empty (Derived). So reproducing negative case N6 (no state
  at t/R 0.05, `engine-v2-negative-cases.md` §1) here says nothing.
- **Verdict: partial.** The hard part, the search over force distributions with a feasible start
  (300–600 lines), stays v2's, as do springings that move within the base joint and loading over
  the whole solid (~150, OCP ray queries). Keep HiGHS and build123d; compas_tna at most for its
  diagram generators, never its equilibrium solvers.

## 5. What this does not settle

- 3-D whole-kiln statics (§1) and LP rows for curved contacts.
- Partial shadowing in view factors (§3), and a source for the closure correction.
- Rectangular-flue fitting losses, fuel-bed and setting resistance, brick roughness, gas
  radiation (§2).
- Why hoop compression doesn't move the dome's least thickness, and a force-distribution search
  for vaults (§4).

## Sources

- P. Block, J. Ochsendorf, "Thrust Network Analysis: a new methodology for three-dimensional
  equilibrium", *J. IASS* 48(3) (2007). web.mit.edu/masonry/papers/block_ochs_IASS_2007.pdf (Read)
- P. Block, J. Ochsendorf, "Lower-bound analysis of masonry vaults", SAHC 2008.
  web.mit.edu/masonry/papers/block_ochs_SAHC_2008.pdf (Read)
- pyViewFactor (AREP, MIT), gitlab.com/arep-dev/pyViewFactor, 1.1.0 (Read, source)
- Cantera (BSD-3), fluids and ht (MIT, C. Bell): licences and sizes read from the installed
  packages (Run)
- The repo's own: `statics-software.md`, `statics-combinations.md`, `radiation-exchange.md`,
  `heat-libraries.md`, `engine-v2-negative-cases.md`, `core/.../thermal/radiation.py`
