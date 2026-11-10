# Thermal tools in pairs, threes and bridges: what each takes off engine v2's hands

Surveyed 2026-11-10, after `thermal-software.md` (single tools), on the pattern of
`statics-combinations.md` and `tool-triples.md`. No engine changes were made. It ends with the
proposed build order for v2's heat model and the questions for the user.

**Status: complete.** Still *pending*: Idelchik's rectangular fittings (no open copy reached) and
the primary papers behind the theses quoted for the zone method and its smoothing.

## The yardstick

- **What a combination takes off v2's hands (the user, 2026-11-09).** Judged by the part of the
  problem it takes, and what v2 would still write and own. Matching a rule or past result counts
  for nothing.
- **The reference kilns stand (the user, 2026-11-10).** "The kilns in the reference material all
  worked for the people that built them for the purpose they were built for. Those are the
  starting point, and the model has to let them stand as working examples. Formulas then go to
  get the right info for the engine, and existing modules are used in the right places in combo
  with the right bridges." A chain is judged by whether it lets a reference kiln's documented
  firing be reached with the kiln's own burners or fuel and its own draft (Olsen's fast-fire: cone
  10 in 3½ h, p.139). Where a chain says a working kiln can't reach its firing, the chain is
  missing physics; the sourced formula or tool that would supply it is named. Nothing is fitted
  to the kiln.
- **A bridge module is cheaper than a whole science module** (the user, 2026-11-10). Bridges are
  ranked by the science taken off v2's hands over the bridge's size.
- **Anything useful is allowed if accurate and it runs on a desktop; like for like, faster is
  better** (the user, 2026-11-10).
- Probes: `scratch/thermal-survey/` (git-ignored). Marks as in `thermal-software.md`: **Run**,
  **Read**, **Snippet**, **Derived**, "from memory".

## 0. Short answer

| Combination (X + Y (+ Z) → result) | Takes off v2's hands | v2 would still write | Verdict |
|---|---|---|---|
| **trimesh + embreex + a WSGG set + IDA (scikit-sundae)** → the zone model: radiation between faces through a radiating gas, with the setting in the way, integrated through a firing | ray tracing and shadowing, the grey-gas exchange areas (from the same rays), the stiff DAE integration and its events | sampling and tallies (~100 lines), the WSGG function and radiosity solve (~80), the zone DAE (~300) | **adopt** as v2's heat core (§2.1); ran end to end on two reference kilns, on IDA and on the step pattern, agreeing to 0.1–2 % (§4) |
| **Cantera + fluids + ht** → the gas path and the draft-limited air (as `tool-triples.md` §2), now feeding the zone model each step through a table of air against gas temperature | gas properties and composition, friction, fittings, grates, convection | the table and its range (~40 lines) | **adopt** (§1.3, §4) |
| **scikit-fem + the floor's zone** → the ground under the kiln | the 2-D transient field | mesh, boundaries, the coupling (~150) | **adopt** (§1.5) |
| **v1's `TransientWall` + any zone solver**, through its affine heat-in | the whole wall physics (k(T), c_p(T), harmonic interfaces) | nothing new (Run) | **keep** as the fallback integrator's wall (§1.4) |
| **Cantera's reactors + our radiation** | kinetics in a zone | – | **not needed**: within 0.22 % of equilibrium in energy (§1.6) |
| **radis or HAPI + HITEMP** → a WSGG fit of our own | line-by-line spectra | the fit; a HITRANonline login and 9.2 GB compressed (Read) | **not needed**: Bordbar 2014 already is a HITEMP fit; Alberti's free tables are the test reference |
| **SciPy `brentq` + IDA's events** → target times | the root and the stopping time | the outer loop (~60) | **adopt** (§1.7) |

**Ranked verdicts** (by the science taken off v2's hands over the bridge's size):

1. **The path-length bridge** (keep each zone pair's ray lengths as quantiles): gas radiation for
   any grey gas from rays already cast, ~20 lines. **Adopt.**
2. **build123d + trimesh + embreex**: rays on the engine's own chamber solids, obstruction
   included, a few lines of hand-over (§2.3). **Adopt.**
3. **trimesh + embreex + WSGG + IDA**: the zone model as a whole (§2.1, §4). **Adopt** as v2's heat
   core.
4. **Cantera + fluids (+ ht)**: the draft-limited air, tabulated for the zone model (§1.3).
   **Adopt.**
5. **scikit-fem + the floor's zone**: the ground (§1.5). **Adopt.**
6. **SciPy `brentq` + IDA's events**: target times (§1.7). **Adopt.**
7. **`TransientWall` through its affine heat-in**: the fallback integrator (§1.4). **Keep.**
8. **Cantera's well-stirred reactor as a test of equilibrium** (§1.6). **Adopt as a test.**
9. **A 1-D hemisphere for the ground** (§3 #5). **Fallback.**

Not adopted: Cantera's reactors as the zones; a WSGG fit from radis or HAPI and HITEMP; the
contour kernel joined to Monte Carlo; fluids' packed-bed laws for a fuel bed (data first); fluids'
jet pump for a venturi burner.

**End to end on two reference kilns** (§4; Run):
- **Olsen's fast-fire (wood, p.139, p.309): it stands.** With a transparent gas the chain could
  not follow the logged firing (the setting 219–229 K short); the missing physics was gas
  radiation. With Bordbar's WSGG set, holding the setting to the log takes a gas of at most
  1329 °C and at most 28 % of the air its own chimney draws, matching the printed, mostly closed
  damper. Its wood (33–39 kg) is under Olsen's ¼ cord, but the efficiency it implies (44–52 %) is
  above the 12–22 % measured on wood kilns: losses the chain lacks (fireboxes, excess air and
  smoke through stoking, leaks) are named, not fitted.
- **Olsen's 36 ft³ dense cross-draft (gas, p.226): it doesn't stand on the design file's
  inputs.** On its six 36,000 BTU/h burners the setting reaches 940 °C at 15 h; cone 10 in 15 h
  needs 2.07 × that input with the file's assumed backing, 3.99 × with bare dense brick, and no
  gas-to-load transfer closes the gap (the plug-flow bound). The same chain on an IFB lining
  brings Olsen's W15 IFB updraft to cone 10 in 3.9 h on its ten burners (he says about 8 h), and in
  9–10 h on six, near the cross-draft's 12–15 h (§4.3). So the question is the cross-draft's
  lining, and it goes to the user (§Questions 4), as the rule says: name what's missing, fit
  nothing.
- The chain was built twice, on v1's step pattern and as one DAE on IDA, and the two agree within
  the step pattern's own error (0.1 % at 5 s steps, 2 % at 30 s), after the IDA version exposed a
  fault in the other (§4).

## 1. Pairs

### 1.1 trimesh + embreex with `radiation.py` → an obstructed grey enclosure (Run)

`mc_exchange.py` (`thermal-software.md` §5.1): the Monte Carlo factors, closed by a symmetric
least-change correction, are what `radiation.Enclosure` takes (rows and reciprocity to 1e-15).
With the setting and the bag walls as part of the mesh, the factors carry their shadows; the
closure moves them by the noise only (the obstructed chamber: 9e-4 at 10⁶ rays a face, falling as
1/√N; §2.3), not by a modelling error as the centroid ray did (8.4e-3, `tool-triples.md` §3), and
the variance-weighted form is the most accurate of those tried (`thermal-software.md` §5.2).
Verdict: **adopt**. Bridge: ~100 lines. Both halves are now sourced: why the closure must be
exact (Clarksean & Solbrig 1993, OSTI 10188074, Read: broken summation or reciprocity put a
wall's heat flux off by over 2×, where ±20 % in the independent factors moved temperatures by
±4 °C), and how (Larsen & Howell 1986's least-squares smoothing with Lagrange multipliers, as
Monnaemang's 2015 thesis restates it, Read: the probes' correction is exactly it, with the
variance as its weights, which is Loehrke et al. 1995's idea for Monte Carlo factors as Frangi's
2025 thesis restates it; `thermal-software.md` §5.2).

### 1.2 trimesh + embreex with a WSGG set → Hottel's zone method for a radiating gas (Run)

The zone method needs, for each grey gas of absorption coefficient k_m, the direct exchange areas
s_i s_j(k_m) and g s_i(k_m) (Hottel's notation; the method's balances are restated openly by
Monnaemang 2015, eqs. 3.11–3.14, after Hottel & Sarofim 1967 and Modest 2013, and the
one-gas-zone furnace with its enthalpy balance by Latham 2008, eqs. 24–26, after Rhine & Tucker
1991; Read). The
rays that give the view factors give them too: each ray's length s is known at its hit, so
s_i s_j(k) = A_i·mean[exp(−k s)·hit_ij] and g s_i(k) = A_i − Σ_j s_i s_j(k) for one gas zone
(Derived). Checked against a sphere's closed form to 1e-5 (Run). A bridge found here: keep each
pair's path lengths as 200 quantiles, and the exchange areas for any k are a sum, with no new ray
cast (Run, `chain_fastfire.py`). With the WSGG weights a_m(T), each grey gas's radiosity solve is
`radiation.exchange`'s with the gas's emission added (~60 lines). The coefficients: Bordbar 2014,
read in FDS's source, and Dorigon 2013, read in the ENCIT paper (`thermal-software.md` §6; both
checked, Run). In the chains (§4) this pair is what lets the fast-fire follow its log. Verdict:
**adopt**.

### 1.3 Cantera + fluids → the air a stoked kiln's own draft draws (Run)

`tool-triples.md` §2's gas path, reused unchanged as a module: the air drawn at λ 1 with the damper
open, tabulated against the chamber gas's temperature (18 solves, about 1 s), and the zone model
reads the air from the table each step. Fast-fire (test inputs as `gas_path.py`; bed and setting
resistance zero, no source; `draft_print.py`, Run): the air rises from 0.076 kg/s with the gas at
77 °C to 0.106 kg/s at 330 °C, then falls as the gas thins, to 0.082 kg/s at 1327 °C; at λ 1 that
burns 44–65 kg/h of dry wood (227–336 kW at 18.67 MJ/kg as fired). Verdict: **adopt**; the bed's and
setting's resistance stay unsourced, so the table is an upper bound on the air.

### 1.4 v1's `TransientWall` with any zone solver (Run)

`TransientWall.heat_in_line` gives a wall's heat-in over a step as a + b·T_face. The zone solver
needs nothing else from the wall. The chain ran six walls this way with no change to v1's code
(Run). For IDA the same physics is re-expressed as cell rates (`thermal-software.md` §3.2).
Verdict: **keep**: it is the fallback integrator's wall and the test oracle for the IDA walls.

### 1.5 scikit-fem with the floor's zone → the ground (Run standalone)

`soil_probe.py` (`thermal-software.md` §4.2): a 2-D axisymmetric transient under the floor,
0.8 s for 30 days. The coupling (not run): the floor's underside temperature is the field's
boundary each step and the field's reaction is the floor's heat-out; with IDA the FE mass and
stiffness matrices can enter the DAE as they are (M·dT/dt + K·T = f), its Jacobian sparse.
Verdict: **adopt**; 1-D hemisphere in `TransientWall` as the fallback (−16 % to −1.4 %, Run).

The fallback was also run coupled to a firing (`ground_coupled.py`, Run): W15's IFB kiln (§4.3)
with its floor carried on into dry soil, 1.6 s a firing. For a 4 h firing over 9 in of IFB the
soil changes almost nothing, as it should: the heat front hasn't reached it (√(αt) ≈ 7 cm in IFB
in 4 h, Derived). The 3 % shorter firing it printed (3.75 against 3.87 h) is the probe's own
construction (the floor's area held constant through the lining on the ground, growing on the
stand), not the soil. The ground matters for days-long firings and thin dense floors (anagamas,
groundhogs dug in): the coupling is ready for them; no such run was made.

### 1.6 Cantera's reactors with our radiation (Run)

A Cantera zone with a `Wall` whose heat flux is our Python function works (5,405 calls for 60 s
of zone time). It would add kinetics, and kinetics change a zone's energy by at most 0.22 % of
the fuel's heat at λ 1.15 (0.5–10 s residence time), and by about 2 % only in reduction below
1000 K (`thermal-software.md` §7.2). Verdict: **not needed**. Keep Cantera's reactors as an offline
check of the equilibrium assumption.

### 1.7 SciPy `brentq` + IDA's events → target times (Derived from Run)

A firing to the cone is one IDA run with a terminal event (0.02–0.04 s on the reduced kiln); the
input for a target time is a root of that (`thermal-software.md` §12). Verdict: **adopt**.

### 1.8 Not adopted

- **The contour kernel + Monte Carlo** (exact factors where a pair is unobstructed, rays where
  it isn't): which pairs are unobstructed isn't known without rays; Monte Carlo at 10⁶ rays a
  face is already within 1e-3. Keep the kernel as a check only.
- **fluids' packed-bed laws + Cantera's gas → a char bed's resistance**: the tools are there
  (Ergun; Idelchik's form for voidage 0.3–0.8), the bed's particle size and voidage aren't
  sourced. Data first.
- **fluids' liquid jet pump → a venturi burner's primary air**: it is a momentum balance for
  liquids with set loss coefficients; nothing ties it to a gas burner. Not proposed.

## 2. Threes

### 2.1 trimesh + embreex + WSGG + IDA → the zone model (Run)

The three pairs above together: the rays give F and the grey-gas exchange areas; the WSGG set
weights the grey gases; IDA integrates the gas, faces, cells and ware with the cone as an event.
On the fast-fire (`chain_ida.py`, 155 unknowns, Bordbar's set) a max-fire firing to cone 10 takes
0.7 s and the 4 h 50 min log 2.9 s, agreeing with the step-pattern chain (SciPy `root` per step)
within its step error (§4). Verdict: **adopt** as v2's heat core. What v2 writes beyond the pairs:
the zone DAE's rows and state (~300 lines), and restarts at schedule breakpoints.

### 2.2 Cantera + fluids + ht → the gas path (`tool-triples.md` §2)

Unchanged; now a module the zone model calls (§1.3).

### 2.3 build123d + trimesh + embreex → rays on the engine's own chambers (Run)

`engine_mesh_mc.py`: the gas volume as the engine draws it (`massing._cavity` for
`examples/gas-crossdraft.yaml`), its faces named and tessellated by `tool-triples.md` §3's
`vfmesh.py`, the triangles handed to trimesh (a few lines), then the rays.

| Chamber | Triangles | Rays a face | Run | Result |
|---|---|---|---|---|
| sprung arch, crown = arch + end caps | 52 | 10⁵ / 10⁶ | 0.3 / 3.3 s | max \|F − `covered()`\| 3.0e-3 / 8.6e-4 raw, 1.6e-3 / 6.0e-4 closed (the exact factors taken with the mesh's own crown area) |
| the same with `obstructed_arch.py`'s bag wall and setting block (test inputs) | 84 | 10⁵ / 10⁶ | 0.4 / 4.7 s | rows exact; reciprocity off 2.8e-3 / 8.5e-4 (the noise); left and right walls to the setting 0.59455 / 0.59444 at 10⁶; the closure moved F by 9.0e-4 |

Against `tool-triples.md` §3's pyViewFactor run on the same chamber (1,492 facets, 5.1 s): its
centroid ray left rows off by 1.5e-2 and a symmetric chamber asymmetric, and the closure moved F
by 8.4e-3, hiding that error. With rays, the closure moves F by the noise only, and the noise
falls as 1/√N. This settles the obstructed case `tool-triples.md` §3 and §5 left open. Verdict:
**adopt** the three together; the engine's meshes need no refining for rays (52–84 triangles
here), only for the faces' own naming.

## 3. Bridges the pairs and threes missed

| # | Bridge | Takes | Size | Verdict |
|---|---|---|---|---|
| 1 | Path-length quantiles per zone pair, kept from the Monte Carlo rays | the grey-gas exchange areas for any k without a new ray cast | ~20 lines (Run) | **adopt** |
| 2 | `TransientWall.heat_in_line` as the wall–zone coupling | the wall's whole physics for the fallback integrator | 0 lines (exists; Run) | **keep** |
| 3 | A draft table, air against gas temperature, from `gas_path.py` | the pressure balance inside every step | ~40 lines (Run) | **adopt** |
| 4 | A Δh(T) table of the products at λ from Cantera | equilibrium enthalpy inside every residual | ~30 lines (Run) | **adopt** |
| 5 | A 1-D hemisphere in `TransientWall` for the ground | a ground model with no new package | ~15 lines (Run) | **fallback** |
| 6 | Cantera's well-stirred reactor as a test of equilibrium | kinetics, offline | the probe (Run) | **adopt as a test** |

## 4. End to end on reference kilns

### 4.1 A stoked kiln: Olsen's fast-fire (Run)

`chain_fastfire.py`. The kiln as `examples/olsen/fast-fire.yaml` draws it: a 27 × 27 in chamber,
36 in to the springline, a 3⅜ in arch; 4½ in K-23 walls, door and arch; a 4½ in KX-99 floor over
the fireboxes; two inlet slots 4½ × 13½ in; the exit flue 9 × 7½ in at the back at floor level;
the 14 ft, 9 × 9 in chimney. The chain:

1. the chamber, the openings and the setting meshed (132 triangles), 2×10⁵ rays a zone, 2.0 s;
2. the gas radiation model, pluggable: a transparent gas, or a published WSGG set (Bordbar 2014;
   Dorigon 2013 for the band);
3. six `TransientWall`s (library k(T) and c_p(T)), outside still air (v1's `StillAirSurface`);
4. the setting as one lumped node, v1's fireclay c_p(T);
5. the gas zone: wood products at equilibrium (Cantera), the air from the draft table (§1.3);
6. 30 s steps, one SciPy `root` per step; the energy balance closes to 1e-9 MJ over a firing.

The rays are not the limit: 2×10⁵ and 10⁶ rays a zone give the same cone times, the same setting
temperature to 0.1 K and the same wood to 0.01 kg (`chain_rays.py`, Run; 1.8 against 7.8 s of
ray casting).

**Test inputs** (not engineering data; the book gives none of them): the setting's envelope
(18 × 21½ in, from 9 to 33 in up) and its 55 kg load (three 12 × 24 × 1 in shelves, posts, about
25 kg of ware); IFB ε 0.6, setting 0.8, shell 0.9 (the floor takes Osborn's low-alumina line,
`radiation-exchange.md` §5.1); wood 50/6/44 C/H/O, 12 % moisture, 19 MJ/kg net oven-dry; zero bed
and setting flow resistance; no firebox zone (the fire's whole heat enters the chamber gas; the
floor's underside adiabatic); the inlet slots black at the gas temperature (the flame seen through
them) and the exit flue black at the back face's temperature; convection from ht's laminar flat
plate at the mean downdraft velocity.

On the exit flue: ADR 0017's H13 puts spy holes and flues at the room's temperature. For a spy
hole open to the room that is right; for the exit flue it would lose about 15 kW at cone 10 (black
at 21 °C, 0.044 m² seeing a 1300 °C chamber: Derived), down a channel that carries the 1300 °C gas.
H13's other half, the chimney's walls as transient faces of their own zone, is the consistent
treatment; the back face's temperature stands in for it here. A question of method for H13, not a
number to fit.

**Two independent formulations, one answer (Run).** The chain was written twice: with v1's step
pattern (`chain_fastfire.py`: `TransientWall`s, a SciPy `root` per step) and as one DAE on IDA
(`chain_ida.py`: the walls as cells, 155 unknowns, a sparse Jacobian pattern). At first they
disagreed (cone 10 at 1.33 h against 0.78 h); the step version had left the floor's
`TransientWall` at its default unit area, 2.55 times too much dense brick. Fixed, they agree:

| Max fire, transparent gas | Cone 10 at 1285 / 1305 °C | Dry wood | Run |
|---|---|---|---|
| step pattern, dt 60 / 30 / 10 / 5 s | 0.800 / 0.783 / 0.783 / 0.781 h; 0.833 / 0.825 / 0.819 / 0.819 h | 39.5 / 39.1 / 38.9 / 38.9 kg | 0.2 / 0.3 / 0.9 / 1.8 s |
| IDA, rtol 1e-5 | 0.780 h; 0.818 h | 38.8 kg | 0.3 s |

IDA in the schedule mode ran the whole 4 h 50 min log in 1.0 s at rtol 1e-5 and agreed with the
step pattern (setting 1056 °C at the end, 25 kg); at rtol 1e-6 it failed at 3.56 h with repeated
corrector failures at h = 1e-17. The log is piecewise linear, so its kinks make the algebraic fuel
rate's slope jump; v2 should stop and restart IDA at each schedule breakpoint (SUNDIALS' tstop),
which a schedule mode needs anyway (Derived).

With gas radiation (Bordbar 2014) the two agree again (Run): max fire, cone 10 at 0.359 / 0.376 h on
19.0 kg (IDA, 0.7 s) against 0.367 / 0.383 h on 19 kg (step pattern at 30 s); held to the log, the
setting at 1247 °C on 32.8 kg (IDA, 2.9 s) against 1247 °C on 33 kg. At rtol 1e-6 the log run
failed on a kink once more, this time after 325 s: the restart at breakpoints is needed, not
optional.

**Transparent gas** (no gas radiation; Run, the step pattern at 30 s; IDA agrees):

| Mode | Setting at the end | Cone 10 (1285 / 1305 °C) | Dry wood | Air needed ÷ the draft's most | Flue share of the fuel's heat |
|---|---|---|---|---|---|
| max: the wood the draft's air burns at λ 1, damper open | – | 0.78 / 0.83 h | 39 kg | 1.00 | 76 % |
| the gas held to the p.309 log, λ 1.0 | 1056 °C at 4 h 50 min | not reached | 25 kg | ≤ 0.18 | 53 % |
| the same, λ 1.2 | 1066 °C | not reached | 31 kg | ≤ 0.28 | 61 % |

Holding the setting itself to the log failed in the first minutes: the log's 190 °C at five
minutes asks for more than any gas temperature delivers, and hybr stalled (the thermocouple read
the gas, not the ware).

What it says, against the yardstick:
- **The kiln can reach its firing on its own draft**: the draft-limited fire reaches cone 10 well
  inside 3½ h (and inside Olsen's 1 h 55 min at 6000 ft). A stoked kiln's time is the stoker's
  choice below that bound (problem set §2.2).
- **But the chain can't follow the documented firing.** With the gas at the log's temperatures, the
  setting ends 219–229 K short of cone 10. The ware is fed only by convection (5–10 W/(m²·K)), the
  inlet slots and the walls' re-radiation. The chain is missing physics: **gas radiation (H6)**,
  and the **luminous flame** of wood (soot), for which no source is yet in `docs/research/`.
- **The wood is far under Olsen's bound**: 25–39 kg against "less than a quarter cord" (about
  255–391 kg oven-dry, `firebox-efficiency.md` §2). Olsen's figure is an upper bound, so this
  doesn't contradict it; but it puts the chain's heat into walls and ware at 24 % (max fire) to
  39–47 % (the log) of the fuel's, against the 12–22 % measured on wood pottery kilns
  (`firebox-efficiency.md` §2). The losses the chain lacks, each needing a source: the fireboxes'
  own brick (90 firebricks, p.140) and their zone, excess air between stokes and smoke (unburnt
  fuel) during them, air leaking in at the stoke holes, and the setting's real load.

**With gas radiation** (Bordbar 2014's WSGG set at the wood products' MR 0.90, p_w + p_c 0.33 atm;
Run, the step pattern at 30 s; Dorigon 2013's MR 1 set gives the same within 5 K and 1 kg):

| Mode | Setting at the end | Cone 10 (1285 / 1305 °C) | Dry wood | Air needed ÷ the draft's most | Flue share |
|---|---|---|---|---|---|
| max: the draft's air at λ 1, damper open | – | 0.37 / 0.38 h | 19 kg | 1.00 | 61 % |
| the gas held to the p.309 log, λ 1.0 | 1247 °C | 38 K short | 33 kg | ≤ 0.19 | 48 % |
| the same, λ 1.2 | 1244 °C | 41 K short | 39 kg | ≤ 0.27 | 56 % |
| the setting held to the log, λ 1.0 | 1285 °C (the log's) | at 4.08 h, the log's 9:00 | 37 kg | ≤ 0.28 | 50 % |

Against the yardstick, now:
- **The fast-fire stands as a working example.** Its documented firing is reachable on its own
  draft: held to the log, the setting needs a gas at most 1329 °C and at most 28 % of the air the
  chimney draws with the damper open. That fits the printed damper schedule, ¾ closed at the
  start, ½ open from 6:15, ¾ open at 8:15, fully open at 9:15 (p.309): the draft was ample, and
  the stoker held the kiln back. The gas-held and setting-held modes bracket the truth (the log's
  thermocouple reads between gas and setting): 38 K short and on time.
- **Gas radiation was the missing physics** the transparent run pointed to: it moved the setting at
  the end of the gas-held log from 1056 to 1247 °C. Which published set is used moves it by less
  than 5 K here (`thermal-software.md` §6.2 for where the sets differ).
- **The wood is still far under Olsen's bound**: 33–39 kg against "less than a quarter cord"
  (255–391 kg). The bound holds. But the chain's heat into walls and ware is 44–52 % of the fuel's,
  against 12–22 % measured on wood pottery kilns: the losses named above (the fireboxes and their
  brick, excess air and smoke through the stoking cycle, air at the stoke holes, the real load)
  are where a weighed firing would point. None has a source yet; none may be fitted.

### 4.2 A fixed-input kiln: Olsen's 36 ft³ cross-draft (Run)

(§4.1's chain, on the step pattern at 60 s, with the kiln's own geometry and fixed fuel; halving
the step moves the setting by 0.1 K at 30 h, `crossdraft_dt.py`, Run.)

`chain_crossdraft.py`, the same chain at a fixed input: six 36,000 BTU/h burners (63.3 kW, HHV),
natural gas as methane at λ 1.15 (v1's `combustion.py`), the gas temperature solved each 60 s step.
Olsen fired it to cone 10 "in about 12–15 hours" on these burners (p.226): his evidence that most
gas kilns are overpowered, so the time is near flat out. The design file's chamber is a 39.6 in
cube (assumed from 36 ft³) and its lining a 4½ in medium-duty hot face backed with 4½ in of K-23,
which the file assumed because v1 couldn't reach cone 10 on bare dense brick; the book says only
"dense brick". Test inputs: a setting envelope 4½ in clear of the walls, 150 kg; medium-duty brick
on Osborn's medium-alumina line; the exit flue 9 × 4½ in; convection from the laminar flat plate
at the mean cross-draft velocity (about 0.1 m/s).

| Lining, transparent gas | Setting at 15 h | at 30 h | Gas | Flue share |
|---|---|---|---|---|
| as designed (dense + K-23) | 476 °C | 648 °C | 1330–1490 °C | 75 % |
| bare 9 in medium-duty (the book's "dense brick") | 371 °C | 414 °C | 1330–1430 °C | 73 % |

Against the yardstick: **the chain says a kiln Olsen fired to cone 10 in 12–15 h can't get its
setting past 650 °C in 30 h.** So the chain is missing physics, and two pieces are named: gas
radiation (H6; a gas flame is non-luminous, so here CO₂ and H₂O carry it), and the convection the
burner jets drive (the mean-velocity flat plate gives 2–3 W/(m²·K); jets and recirculation give
far more, and no correlation for a kiln chamber is in `docs/research/`; impinging-jet correlations
such as Martin's are in the VDI Heat Atlas, not in ht).

**With gas radiation** (Bordbar 2014 at methane's MR 2; Run, 60 s steps; the step pattern):

| Lining, Bordbar's WSGG | Setting at 15 h | at 30 h | Gas at 30 h | Flue share | Into the walls |
|---|---|---|---|---|---|
| as designed (dense + K-23) | 940 °C | 1176 °C | 1222 °C | 48 % | 49 % |
| bare 9 in medium-duty | 733 °C | 799 °C | 890 °C | 39 % | 59 % |

Gas radiation lifts the designed kiln's setting from 476 to 940 °C at 15 h, but it still doesn't
reach cone 10 in 30 h. Is it the gas-to-load transfer the single zone gets wrong? Two bounds
(`crossdraft_bounds.py`, Run), at the printed input:

| Bound | Setting at 15 h | Cone 10 |
|---|---|---|
| as run | 940 °C | not by 30 h |
| the flue gas leaving at the setting's temperature (the plug-flow limit: no zone model can cool the exit below the load it passes; Derived) | 990 °C | not by 30 h |
| inside convection at least 30 W/(m²·K) (a test value for the burners' jets) | 970 °C | not by 30 h |
| both | 992 °C | not by 30 h |

So **the gap isn't in the transfer** that zones in series or jet convection would add. It is in the
energy budget: a rough count (Derived) has about 2 GJ to store in 1,700 kg of dense hot face, its
backing and the setting, against an available heat that falls to about 0.30 of the 63.3 kW input
(19 kW) near cone 10 (`2026-11-physics-review-heat.md` #9), less the lining's steady loss. The
closed form makes it exact at the top (`mustfail.py`, Run: v1's Cantera available heat and v1's
steady `solve_wall`, the six faces as one wall of the cube's area):

| Lining | Kept at 1285 °C (0.304 × 63.3 kW) | Steady loss at 1285 °C | Margin |
|---|---|---|---|
| as designed | 19.3 kW | 17.0 kW (shell 115 °C) | +2.3 kW: can reach, but slowly |
| bare 9 in medium-duty | 19.3 kW | 54.4 kW (shell 228 °C) | −35.2 kW: **can never reach cone 10** |

With 2.3 kW to spare at the top, the designed kiln creeps up on cone 10; bare dense brick can't
get there on any schedule. The margin is thin enough that small terms decide it: an open spy hole
of the engine's default 2¼ × 2½ in, black at room temperature as H13 has it, loses up to 1.2 kW
at cone 10 (Derived; less for the hole's depth, which the rays would count), and the chain has
none.

The energy budget points at the design file's inputs, not at the chain's physics: the chamber
(36 ft³ taken as a cube to the springline; if it was stacking space, as the kits' are, the chamber
is bigger still), the lining (only "dense brick" is printed; the K-23 backing is the file's
assumption) and the burners' real input (rated 36,000 BTU/h; at what pressure?).

**The target-time solve** (`crossdraft_target.py`, Run: SciPy `brentq` on the input around whole
firings, 66 s for the root at 60 s steps):

| Case | Cone 10 (setting at 1285 °C) |
|---|---|
| the printed 216,000 BTU/h (63.3 kW), designed lining | not by 30 h |
| the same with λ 1.0, or half the setting load (75 kg), or Dorigon's set | not by 30 h, each |
| 1.5 × the printed input | 23.1 h |
| 2 × | 15.7 h |
| **cone 10 in 15 h, designed lining** | **131.0 kW = 447,000 BTU/h, 2.07 × printed** |
| **cone 10 in 15 h, bare 9 in dense brick** | **252.5 kW = 862,000 BTU/h, 3.99 × printed** |

For scale only (a rule is not evidence, by the yardstick): Olsen's own Rule 1 for dense brick,
16,000–19,000 BTU/ft³/h (p.226), gives 576,000–684,000 BTU/h for 36 ft³, between the chain's two
answers; the p.226 anecdote of 6,000 BTU/ft³/h is a third of his own dense minimum
(`kiln-reference.md`). **Not fitted**: the kiln's own figures are the question for the user
(§Questions). Until then step 0 can't use this kiln as a positive case.

### 4.3 A sanity check on a light lining: Olsen's W15 IFB updraft (Run)

Olsen's W15 (p.226): a 36 ft³ IFB updraft on at least ten of the same burners "fires easily in
about 8 h". The dataset marks it a general statement, not a built kiln (no design file; the
lining's thickness and the cone not printed), so it is weaker evidence. `w15_ifb.py`: the
cross-draft chain's cube and setting, test lining 4½ in K-26 over 4½ in K-23, IFB ε 0.6, cone 10:

| Burners | Cone 10 at 1285 / 1305 °C | Flue | Walls | Setting |
|---|---|---|---|---|
| 10 (105.5 kW, W15's) | 3.9 / 4.2 h | 57 % | 30 % | 13 % |
| 6 (63.3 kW, the cross-draft's) | 9.2 / 10.1 h | 56 % | 34 % | 9 % |

On its own ten burners the IFB kiln stands easily (inside Olsen's 8 h, which is a potter's pace).
And on the **six** burners Olsen gave the dense cross-draft, an IFB-lined 36 ft³ kiln reaches cone
10 in 9–10 h, near his 12–15 h. The chain behaves on a light lining as the book says; what it
can't reconcile is the six burners with **dense** brick. That points the cross-draft question at
its lining.

## 5. What this does not settle

- **Zones in series** (H1 across chambers, tubes and fireboxes): every chain here is one gas zone.
  Gas-to-gas exchange between zones needs volume emission in the rays (not written); the
  cross-draft's plug-flow bound shows the single zone isn't what limits that kiln.
- **The fireboxes as zones** with their own brick and fuel bed; the bed's and the setting's flow
  resistance; brick roughness; rectangular-section fittings (Idelchik's diagrams, *pending*).
- **The luminous flame** (soot) and the convection the burner jets drive: physics published,
  kiln data absent.
- **λ through a stoked firing**, unburnt fuel and leaks: what the fast-fire's efficiency gap
  points at; no source.
- **The ground in a long firing**: the 2-D field was run alone, the 1-D fallback coupled only to a
  4 h IFB firing where the soil can't matter (§1.5); and elements as face sources.
- **Sources still secondary**: the zone method, the well-stirred model and the smoothing are
  sourced openly, but through theses (Latham 2008 after Rhine & Tucker 1991; Monnaemang 2015 after
  Hottel & Sarofim, Modest, Larsen & Howell; Frangi 2025 after Loehrke et al.), not the primaries;
  Hottel's own (GS₁)_R not found open; Latham's eqs. 24–26 read in a garbled text layer; GRI-Mech
  3.0's optimisation range, still quoted from memory.
- **Olsen's 36 ft³ cross-draft**: the design file's inputs (§4.2, Questions 4).

## Build order

Proposed for `kilndesigner.v2.heat` (ADR 0017, "Where v2 lives"). Each step leaves a usable,
tested piece; the reference-firing checks come first so every later step is judged against
kilns that worked, not against v1 (the user, 2026-11-10). Line counts are the bridge's own,
estimated from the probes (Derived).

| Step | Module | What it does | Tools (new package?) | Size | First check |
|---|---|---|---|---|---|
| 0 | `tests/v2/heat/test_reference_firings.py` | the documented firings as inequalities: the fast-fire reaches cone 10 inside 3½ h on its own draft (p.139), follows the p.309 log within its draft's air, and its wood stays under ¼ cord (p.143); Olsen's 36 ft³ cross-draft reaches cone 10 inside 12–15 h on six 36,000 BTU/h burners (p.226; the chain says it can't with the design file's lining, §4.2: settle the file's inputs first); W15's IFB updraft inside about 8 h on ten (p.226, a general statement; 3.9 h in the chain, §4.3); later the multi-chamber stage times (Suzuki p.93) and the electric W25 (pp.258–260). And must-fail heat cases from physics, since the book prints no heat failure: a kiln whose available heat at the cone is below its lining's steady loss there never reaches the cone (Derived; e.g. the cross-draft on bare 9 in dense brick, −35 kW at the top, §4.2, Run) | pytest only | ~150 | each fails until the chain carries its physics, then must hold; nothing fitted (problem set §6) |
| 1 | `heat/gas.py` | fuels (propane, natural gas, wood and coal surrogates), equilibrium products at λ, Δh(T) and transport tables, the 200–3500 K guard | Cantera (have) | ~150 | v1's `available_heat`; `cantera-tespy-review.md` §2's wood table |
| 2 | `heat/draft.py` | the gas path's pressure balance from the design; air against gas temperature | fluids (**add**; MIT), Cantera | ~250 | `tool-triples.md` §2's fast-fire numbers; Idelchik's rectangular forms once read |
| 3 | `heat/rays.py` | the chamber's faces, openings, bag walls and setting meshed from the engine's solids; Monte Carlo view factors and path-length quantiles; Larsen & Howell's smoothing (variance weights) | trimesh, embreex (**add**; MIT, BSD) | ~150 | `radiation.box`, `covered`; the sphere's closed form; Cauchy's 4V/A |
| 4 | `heat/gasrad.py` | a published WSGG set as data; the grey-gas exchange areas and radiosity solve (the zone method, one gas zone) | NumPy | ~100 | Lienhard Ex. 10.11; the published set's own test cases |
| 5 | `heat/walls.py` | walls as method-of-lines cells (`TransientWall`'s physics, no lag) | NumPy | ~80 | `TransientWall`; erf; Incropera §5.5; de Monte's two-layer slab |
| 6 | `heat/zone.py`, `heat/firing.py` | one well-stirred zone per chamber as a DAE: gas, faces, cells, ware; max-input and schedule modes; the cone as an event; restarts at schedule breakpoints; the working | scikit-sundae (**add**; BSD-3) | ~300 | the step-pattern chain (agreeing within its step error, §4); the energy balance closing; then step 0's fast-fire, W15 and cross-draft checks |
| 7 | `heat/ground.py` | the 2-D transient ground under a grounded floor, coupled each step | scikit-fem (**add**; BSD-3) | ~150 | the slab and disc limits (`thermal-software.md` §4.2) |
| 8 | `heat/target.py` | the time at an input; the input for a time | SciPy (have) | ~60 | v1's `target.py` cases |
| 9 | zones in series | fireboxes, chambers and tube segments as zones; the gas leaving each at its temperature (H1) | as 6 | ~200 | the multi-chamber stage times and spreads (problem set §6, T5) |
| 10 | heat input | burners sized from charts and the gas system (decision 13); elements as face sources; stoking within the draft's air | fluids, Cantera | ~200 | Olsen's W25; the kits' burners (p.222) |

Packages to add to `core/pyproject.toml` (all with CPython 3.14 wheels for Linux, macOS and
Windows, Run): `trimesh>=5.2` (MIT, 0.8 MB), `embreex>=4.4` (a BSD-style wrapper with Embree,
Apache-2.0, inside; 14.6 MB), `scikit-sundae>=1.2` (BSD-3, bundling SUNDIALS, SuperLU_MT, OpenBLAS
and LAPACK, each BSD-3; 20.8 MB),
`scikit-fem>=12` (BSD-3, 0.2 MB), `fluids>=1.3` (MIT, 0.6 MB) and `ht>=1.2` (MIT, 0.8 MB; moved from
the dev group). About 38 MB more on Linux. All ran in overlays with the repo's NumPy 2.5.4 and
SciPy 1.18.1 (Run). The engine stays pure (ADR 0002): none does I/O beyond what it is handed.

## Questions for the user

Also recorded in each section above; none blocks the build order's steps 1–8.

1. **The four new packages** (trimesh, embreex, scikit-sundae, scikit-fem) plus fluids and ht as
   runtime dependencies: agreed? scikit-sundae has one listed maintainer (a national-laboratory
   project, released 2026-10-16); its fallback is SciPy's `solve_ivp` (§1, `thermal-software.md`
   §3.2).
2. **The fast-fire's load.** The book gives no ware or shelf load (a gap in the dataset); the chain
   used 55 kg as a test input. A firing's load, even roughly (shelves and posts, and pots by
   weight), turns step 0's check from a bound into a test. And Fig 5-43's shelf layout (4½ in
   clear each side, 1 in between) leaves 18 in across for 12 × 24 in shelves in a 27 in chamber:
   one shelf across, turned how?
3. **The luminous flame.** Wood (and oil, and gas in reduction) flames radiate mostly from soot
   (Lienhard p.594). The physics is published openly (Sadeghi et al. 2021's soot WSGG, CC BY;
   `thermal-software.md` §6.4); a kiln flame's soot volume fraction is in no source read. Should
   v2 carry soot as a stated band of soot fraction, or leave it out and say so in the working?
4. **Olsen's 36 ft³ dense cross-draft (p.226).** With sourced brick properties, Cantera's flue loss
   and gas radiation, the chain needs 2.07 × the printed 216,000 BTU/h to reach cone 10 in 15 h
   with the design file's K-23-backed lining, and 3.99 × with bare 9 in dense brick, which on the
   printed burners can never reach cone 10 at all (its steady loss at the top exceeds the heat
   the burners leave by 35 kW); no transfer physics closes it (the plug-flow bound gains 50 K at
   15 h; §4.2). The same chain with an IFB
   lining reaches cone 10 in 9–10 h on those six burners (§4.3). Which of the file's inputs is
   wrong: the chamber (a 39.6 in cube taken from "36 cu ft"), the lining ("dense brick"; the
   backing is the file's), the burners' real input (rated at what pressure?), or the time (to
   which cone)? Do you know anything more about this kiln?
5. **A weighed wood firing** (as `11-09-26.md` §F asks): with gas radiation the fast-fire chain
   burns 33–39 kg for the logged firing, putting 44–52 % of the wood's heat into walls and ware,
   against 12–22 % measured on wood pottery kilns. The weight of wood for one firing of any wood
   kiln you know, and an O₂ reading at the flue, would show which of the missing losses
   (fireboxes, excess air between stokes, smoke, leaks) matter.

## Sources

- The probes, `scratch/thermal-survey/`: `chain_fastfire.py`, `chain_ida.py`, `chain_dt.py`,
  `chain_rays.py`, `draft_print.py`, `chain_crossdraft.py`, `crossdraft_bounds.py`,
  `crossdraft_target.py`, `mustfail.py`, `w15_ifb.py`, `ground_coupled.py`, `engine_mesh_mc.py`,
  `closure_probe.py`, `mc_exchange.py`, `mbl_check.py`, `soil_probe.py`, `integrator_probe.py`,
  `cantera_wsr.py`, `wsgg.py`, `wsgg_check.py` (Run); earlier probes reused:
  `scratch/toolsets/gas-path/gas_path.py`,
  `scratch/toolsets/view-factors/vfmesh.py`, `obstructed_arch.py`, `check_engine_shapes.py`.
- The packages and the WSGG sets: `thermal-software.md`, Sources.
- Olsen, *The Kiln Book*, 4th ed.: the fast-fire (pp.139–143, p.204, the p.309 log and damper
  schedule) and the 36 ft³ cross-draft (p.226), as `core/tests/v2/reference_kilns.yaml`,
  `examples/olsen/fast-fire.yaml`, `examples/olsen/olsen-crossdraft-36.yaml` and
  `kiln-reference.md` record them.
- Material properties from the engine's library (`core/src/kilndesigner/data/materials.yaml`:
  Morgan K-23 [S31], Alsey Smithfield medium-duty [M9], HWI KX-99 [S35], VDI c_p(T) [M2]); hot
  emissivities from `radiation-exchange.md` §5 (Osborn 1985, via Jones et al. 2019).
- Wood: `wood-fuel.md` ([W2] 19 MJ/kg net; FAO UBET eq. 3), `firebox-efficiency.md` (§2, measured
  kilns), `cantera-tespy-review.md` §2 (the surrogate).
