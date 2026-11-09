# EnergyPlus: what it could offer the heat calculations

Researched 2026-11-09. No engine changes were made; this note proposes them.

**Source read:** EnergyPlus, https://github.com/NatLabRockies/EnergyPlus, branch `develop` at
commit `8470a217859636828887b084d6eba4486625ac7e` (2026-11-09). Paths below are relative to
that commit. The engineering reference is the LaTeX under `doc/engineering-reference/src/`;
section names are its `\section`/`\subsection` titles. Files fetched for line numbers are kept
in `scratch/energyplus/` (git-ignored); nothing was cloned.

**Our side, as of this branch:** `core/src/kilndesigner/thermal/wall.py` (steady layered wall,
k(T) by Kirchhoff transform, ASTM C680-style iteration on the surface temperature),
`thermal/surface.py` (Churchill–Chu vertical; Lloyd–Moran 0.54 Ra^¼ / 0.15 Ra^⅓ hot face up;
0.27 Ra^¼ hot face down, L = A/P; h_r = εσ(Ts²+T∞²)(Ts+T∞) to surroundings at air temperature;
Ra ranges at lines 81–89), `thermal/transient.py` (1D finite volumes, backward Euler, k, c_p and
h lagged one step, ADR 0015), `heatloss.py` (per-face walls; a grounded floor is a disk on a
semi-infinite solid, S = 2D, h = 8k/(πD), lines 242–252, soil k = 1.0 W/(m·K) at line 43) and
`simulation.py` (the same ground h as a fixed surface, line 281). Gaps recorded in
`docs/planning/02-plan.md` lines 319–321 and 485–488: no radiation between faces or inside
film; no ASTM C680 worked example; no published h_r or hot-face-down case with numbers.

## 1. Licence

`LICENSE.txt` (on `develop`) is a modified BSD-3 licence, with:

- the usual BSD conditions (keep the notice and disclaimer in source and binary copies);
- a U.S. Government paid-up licence notice;
- clause 4: anything redistributed must call it "EnergyPlus version X", and the licensee "shall
  not use in a company name, a product name, in advertising, publicity, or other promotional
  activities any name or trade or service mark, or any designation that is confusingly similar
  to … 'EnergyPlus', 'E+' or 'e+'" without DOE's written consent.

Kiva (Big Ladder Software, used by EnergyPlus for foundations) is plain BSD-3-Clause
(GitHub licence API for `bigladder/kiva`, "Copyright (c) 2012-2022 Big Ladder Software LLC").

**For an MIT project:** BSD-3 is compatible with MIT. Re-implementing a published method from the
engineering reference (equations, not code) carries no licence obligation; cite it like any
other source. Porting code (for example `CalcScriptF`) would mean keeping EnergyPlus's notice
with that code, and clause 4 means we may not market a feature as "EnergyPlus" or "E+" (citing it
as a source in `docs/research/` and in working steps is fine). Calling EnergyPlus as a library is
impractical anyway (a C++ building simulator driven by IDF/epJSON, with no kiln-temperature
materials); nothing below recommends it.

## 2. Conduction: CTF versus the finite-difference algorithm

**EnergyPlus.** The default, conduction transfer functions (`surface-heat-balance-manager-
processes/conduction-through-the-walls.tex`, "Conduction Transfer Function (CTF) Calculation
Method"), are linear with constant coefficients per construction: constant k, ρ, c_p, no interior
temperatures, and the reference itself notes the series become unstable as the time step falls
and for "thermally massive constructions with long characteristic times", with trouble for heavy
slab-on-grade floors even at half-hour steps. A kiln wall is exactly the massive, strongly
non-linear case (k of insulating firebrick roughly doubles from 200 °C to 1200 °C).
**Not applicable.**

The conduction finite-difference algorithm, CondFD (`conduction-finite-difference-
solution.tex`), is the comparable method:

- schemes: Crank–Nicolson (pre-v7) or fully implicit (v7 on, the default), both on half-node /
  full-node grids per layer;
- grid: Δx = √(C·α·Δt), C = 3 by default (grid Fourier number 1/3), rounded to whole nodes per
  layer;
- k(T) as k₀ + k₁(T − 20) or piecewise-linear pairs (`MaterialProperty:VariableThermalConductivity`),
  evaluated at the new time level with interface k as the arithmetic mean of the two nodes;
- c_p from an enthalpy–temperature table (`MaterialProperty:PhaseChange`), c_p = Δh/ΔT per
  iteration;
- Gauss–Seidel inner iterations with under-relaxation, to about 1e-6 °C or 30 iterations; zone
  time step 20–60 per hour recommended.

**Compared with ours.** `thermal/transient.py` is already this method with two different choices:

| | EnergyPlus CondFD | kilndesigner `TransientWall` |
|---|---|---|
| time scheme | fully implicit (or C–N) | backward Euler |
| property time level | new level, iterated (non-linear) | start of step, lagged (linear) |
| interface k | arithmetic mean of node k | harmonic (series half-cells), Patankar |
| storage | enthalpy table possible | c_p(T) points, lagged |
| grid | Δx from Fourier number | ≤ 5 mm, ≥ 4 cells per layer |

What it would change: iterating k and c_p to the new time level removes the lag error, which is
first order in Δt and largest during fast ramps; the arithmetic-mean interface k is less accurate
than our harmonic mean across a dense/insulating boundary (Patankar's argument, already cited in
`transient.py`'s docstring), so don't copy that.
The enthalpy formulation matters if we ever model a material with a latent effect (free water
in a castable at 100 °C; quartz inversion is small). Our closed-form "T_c as an affine function"
trick depends on the step being linear, so iterating properties would need a Picard loop around
it (re-prepare with properties at the provisional new temperatures, two or three passes).

**Recommendation:** keep our solver. Optionally add one Picard correction of k and c_p per step,
cited to the engineering reference §"Conduction Finite Difference Solution Algorithm" and
checked by halving the step. Adopt the enthalpy form only when a sourced latent heat appears.

## 3. Convection at the outside surface

**EnergyPlus correlations.** Exterior natural convection in TARP and DOE-2
(`outside-surface-heat-balance.tex`, "Outdoor/Exterior Convection", "TARP Algorithm") and the
interior ones (`inside-heat-balance.tex`, "Interior Convection", lines 358–450) are dimensional
building fits, ΔT in K, h in W/(m²·K):

- ASHRAE vertical: h = 1.31 |ΔT|^⅓ (ASHRAE HOF 2001 p.3.12 Table 5; `ConvectionCoefficients.hh`
  line 405);
- Walton unstable (hot face up): h = 9.482 |ΔT|^⅓ / (7.238 − |cos Σ|) (Walton 1983, TARP
  NBSSIR 83-2655 pp.79–80; `.hh` line 429);
- Walton stable (hot face down): h = 1.810 |ΔT|^⅓ / (1.382 + |cos Σ|) (`.hh` line 451);
- Alamdari–Hammond: vertical {[1.5(ΔT/H)^¼]⁶ + [1.23 ΔT^⅓]⁶}^⅙, stable horizontal
  0.6 (ΔT/D_h²)^⅕, unstable {[1.4(ΔT/D_h)^¼]⁶ + [1.63 ΔT^⅓]⁶}^⅙, D_h = 4A/P
  (`ConvectionCoefficients.cc` lines 5018–5118);
- Fohanno–Polidori vertical (regime change at Ra*_H = 6.3e9; `.cc` line 5710); Khalifa,
  Fisher–Pedersen (ACH-driven, mechanically ventilated rooms), Beausoleil-Morrison, Awbi–Hatton:
  room-air correlations for heated floors, diffusers and so on.
- ASTM C1340 (`.cc` lines 6438–6560), non-dimensional with its own air-property fits: hot face
  down Nu = 0.58 Ra^0.2, hot face up 0.54 Ra^¼ below Ra = 8e6 and 0.15 Ra^⅓ above, tilted
  0.56 (Ra sin θ)^¼ with a critical Grashof number, L = √A for horizontal faces, height for
  vertical ones; combined with forced convection.

**Note on a typo.** `outside-surface-heat-balance.tex` prints the unstable denominator as 7.283;
the code (`.hh` line 429) and `inside-heat-balance.tex` line 373 have 7.238. Use 7.238.

**Validity at kiln temperatures.** The engineering reference states no ΔT, Ra or temperature
range for TARP/Walton, ASHRAE, Alamdari–Hammond, Khalifa or Awbi–Hatton; they were fitted to
room-scale surfaces with ΔT of a few to a few tens of kelvin. Fisher–Pedersen and the diffuser
models need a room ACH and do not apply to a kiln in still air. None applies inside the kiln
(combustion gases at 1000 °C+). Our Ra-range check (ADR 0009) can't be applied to a dimensional
correlation, so adopting one would lose the refusal we have now.

**What it would change.** At 20 °C air (script `scratch/energyplus-review/compare.py`, run with
the engine's own air table), convection h in W/(m²·K):

| shell | face | ours | Walton/ASHRAE | ASTM C1340 (L = √A = 1 m) |
|---|---|---|---|---|
| 50 °C | vertical, H = 1 m | 4.38 | 4.07 | |
| 50 °C | up, 1 m square (A/P = 0.25 m) | 5.46 | 4.72 | |
| 50 °C | down, 1 m square | 2.29 | 2.36 | 1.18 |
| 80 °C | vertical | 5.31 | 5.13 | |
| 80 °C | up | 6.69 | 5.95 | |
| 80 °C | down | 2.69 | 2.97 | 1.35 |
| 120 °C | vertical | 6.03 | 6.08 | |
| 120 °C | up | 7.64 | 7.06 | |
| 120 °C | down | 3.01 | 3.53 | 1.49 |
| 200 °C | vertical | 6.75 | 7.40 | |
| 200 °C | up | 8.57 | 8.58 | |
| 200 °C | down | 3.35 | 4.29 | 1.66 |

With h_r ≈ 7.3 W/(m²·K) at an 80 °C painted shell (ε = 0.95), the vertical and facing-up
differences are 1–6 % of the combined coefficient; the shell heat loss, which is dominated by the
wall's resistance, moves by much less. Walton agrees with our non-dimensional fits to within
~15 % across 50–200 °C, which is a useful plausibility cross-check but not an independent
published case (both trace to the same laminar/turbulent plate data).

The hot-face-down case is where sources disagree: ASTM C1340's 0.58 Ra^0.2 (with L = √A) gives
about half of our 0.27 Ra^¼ (with L = A/P). The two differ in exponent and in length scale, so
a direct comparison needs the same plate. Where the 0.58 Ra^0.2 form comes from (and whether
other Ra^⅕ fits for heated plates facing down agree with it) is unverified here. Halving the floor's h_conv on a kiln on a stand would cut
that face's combined coefficient by ~13 % (2.7 of ~10 W/(m²·K)) and raise its surface
temperature. This should be checked against the primary sources before anything changes; see
the questions in `docs/planning/11-09-26.md`.

**Recommendation:** keep our correlations (non-dimensional, with Ra ranges). Do not adopt the
building correlations. Add a test that compares ours with Walton/ASHRAE within a stated band at
50–120 °C shells as a sanity check, citing the engineering reference §"TARP Algorithm" and
Walton 1983. Research the hot-face-down choice (0.27 Ra^¼ vs 0.58 Ra^0.2 and their length scales) from ASTM C680 / C1340 and Raithby–Hollands before changing it.

## 4. Radiation between surfaces inside an enclosure

**EnergyPlus.** `inside-heat-balance.tex` §"LW Radiation Exchange Among Zone Surfaces" (lines
38–136) and `HeatBalanceIntRadExchange.cc`: Hottel's ScriptF grey-interchange factors
(Hottel & Sarofim, *Radiative Transfer* ch. 3, 1967; `CalcScriptF` line 1823), with grey, diffuse
surfaces and a non-participating medium. View factors are approximate unless entered
(`CalcApproximateViewFactors` line 1407): a surface sees the others in proportion to their area,
not itself, nor any surface facing within 10° of its own orientation; `FixViewFactors`
(line 1521) then enforces reciprocity and completeness. An alternative, CarrollMRT
(`CalcFMRT` line 2026), exchanges each surface with one mean-radiant node.

**At kiln temperatures.** The ScriptF algebra is exact for grey diffuse surfaces and a
transparent gas at any temperature; nothing in it is fitted to buildings. Two things don't
carry over: EnergyPlus linearises nothing here but treats air as transparent, while kiln gases
(CO₂, H₂O) emit and absorb strongly at 1000 °C+ (Hottel's zone method or a mean-beam-length gas
emissivity would be needed for a gas kiln); and the area-proportional view factors are crude for
a box with a ware stack in it.

**What it would change.** Inside the chamber, faces are already near one temperature at steady
state, so exchange between them changes little in `heatloss.py`. In the firing simulation it
evens out hot spots: the floor (which loses into soil) and the door would be fed by the roof and
walls, and the ware's heating would follow T⁴ rather than our lumped assumption. This is the
"no radiation between faces" gap. The first-order effect is on the ware lag and the floor's
temperature, not total fuel.

**Recommendation:** adopt the method, not code: a small ScriptF enclosure (six faces plus a ware
node), exact box view factors from the published closed forms for parallel and perpendicular
rectangles (Howell's view-factor catalogue; source still to be recorded in `docs/research/`)
rather than EnergyPlus's area approximation, cited to the
engineering reference §"LW Radiation Exchange Among Zone Surfaces" and Hottel & Sarofim ch. 3.
Validate with the standard two-infinite-plates and enclosed-body cases (closed form). Leave gas
radiation out and say so, until a sourced gas emissivity method is in `docs/research/`.

## 5. Ground heat transfer

**EnergyPlus.** Kiva (`ground-heat-transfer-calculations-using-kiva.tex`): 2D finite
differences on a half-domain, ADI time stepping, the 3D footprint reduced to 2D by a half-width
of A/P_exposed (with a Kruis–Krarti correction for concave shapes), deep-ground boundary either
fixed temperature or zero flux, an accelerated warm-up, interior TARP convection; validated
against the IEA BESTEST ground-coupled cases "within 3 % of reference solutions" (Kruis & Krarti
2015). The older Slab and Basement preprocessors (`ground-heat-transfer-calculations-using-
site*.tex`, `…-using-c.tex`) produce monthly ground temperatures for buildings and don't apply.

**At kiln temperatures.** The conduction is the same physics at any temperature, but soil k at
a few hundred degrees (drying, moisture migration) is outside anything Kiva models; it takes k
constant. For us the gain is geometric: our steady disk on a semi-infinite solid (h = 8k/(πD))
ignores the platform's edge losses and the transient. `heatloss.py` line 410 already states
that cold ground takes about twice as much at 12 h.

**What it would change.** A 2D axisymmetric (or A/P half-width) transient soil model under the
floor, run with the firing, would replace the steady h with one that starts high and falls,
raising the early-firing floor loss and the fuel per firing for kilns on the ground; and give
the soil and platform temperatures under the floor over time. Size of the effect: up to ~2× the
floor's loss at 12 h by our own current note; the floor is one face of six.

**Recommendation:** adopt the method (2D implicit FV, A/P reduction, fixed-temperature deep
boundary), citing the engineering reference §"Ground Heat Transfer Calculations using Kiva" and
Kruis & Krarti 2015. Do not call Kiva as a library (C++, tied to EnergyPlus's surface model;
BSD-3 would be fine). Validate against the IEA BESTEST GC10a analytical case (below).

## 6. Validation suites and numbers we could test against

- **ASHRAE Standard 140 / BESTEST.** Building-scale load comparisons. The building cases
  (600, 900 series) compare programs with each other; they are not analytical truths and don't
  test kiln-range physics. Not useful to us as-is. I did not verify the current edition's
  acceptance ranges (ASHRAE 140-2020/2023 added them); no tolerance is quoted here for that
  reason.
- **IEA BESTEST ground-coupled, case GC10a** (Neymark, Judkoff et al., NREL/TP-550-43388, 2008;
  adopted into ASHRAE 140): steady 3D heat loss of an uninsulated slab in grade from Delsante,
  Stokes & Walsh's (1983) analytical solution, the "mathematical truth standard". This is the
  best candidate: an analytical answer, in watts, for a slab on soil, to check a ground model
  (and today's disk formula, scaled) against. The case specification and the reference value
  were not retrieved in this session (the report mirror was unreachable); fetch them before
  writing the test. Kiva's reported agreement is within 3 %.
- **EnergyPlus unit tests** (`tst/EnergyPlus/unit/`): `HeatBalanceIntRadExchange.unit.cc`
  (`FixViewFactorsTest` line 184, `ViewFactorAngleLimitTest` line 884) and
  `ConvectionCoefficients.unit.cc` (`TestASTMC1340` line 2428: 1.977, 2.666, 1.756 W/(m²·K)).
  These are regression values of EnergyPlus's own code at room temperatures with forced flow,
  not published references; under ADR 0009 they could only serve as a cross-check of a port,
  not as validation. I don't recommend copying them.
- **Analytical cases EnergyPlus's documentation points to** that we can use directly: grey
  two-surface exchange q = σ(T₁⁴ − T₂⁴)/(1/ε₁ + 1/ε₂ − 1) for parallel plates, and the enclosed
  body; ScriptF must reduce to these.

Nothing here supplies the missing ASTM C680 worked example or a published hot-face-down case
with numbers at kiln-shell temperatures.

## 7. Proposed engine changes, ranked

| # | Change | Expected effect | Method source | Risk |
|---|---|---|---|---|
| 1 | Radiation exchange inside the chamber (ScriptF over six faces plus a ware node; exact box view factors), in the firing simulation | Closes the "no radiation between faces" gap; feeds the floor and door from the hot faces; ware temperature lags realistically. Small change to total fuel, larger to floor and ware temperatures | Eng. ref. §"LW Radiation Exchange Among Zone Surfaces"; Hottel & Sarofim ch. 3; Howell's view-factor catalogue | Medium: new coupling between faces in `simulation.py` |
| 2 | Transient 2D soil under a grounded floor (A/P half-width, implicit FV, fixed deep temperature) | Floor loss starts higher and falls; more fuel early in firings of kilns on the ground (up to ~2× the floor's loss at 12 h by our own note); soil and platform temperatures over time | Eng. ref. §"Ground Heat Transfer Calculations using Kiva"; Kruis & Krarti 2015; validate with GC10a | Medium; needs GC10a's numbers first |
| 3 | Settle the hot-face-down correlation (0.27 Ra^¼, L = A/P vs 0.58 Ra^0.2, L = √A as in ASTM C1340) from primary sources | Up to ~50 % lower convection on a floor underside or roof overhang facing down; ~13 % on that face's combined h | ASTM C1340 as coded at `ConvectionCoefficients.cc` 6495–6532; needs the standard and Raithby–Hollands | Low effort, but research first |
| 4 | Picard correction of k and c_p to the new time level in `TransientWall` | Removes the first-order lag error in fast ramps; agreement with halved-step runs | Eng. ref. §"Conduction Finite Difference Solution Algorithm" | Low; keeps the affine T_c step if done as re-prepare |
| 5 | Cross-check test of our still-air h against Walton/ASHRAE at 50–120 °C shells | A plausibility band, not validation; catches gross regressions | Eng. ref. §"TARP Algorithm"; Walton 1983 pp.79–80 | Very low |
| 6 | Enthalpy (h–T table) storage option for layers | Only matters with a sourced latent effect (free water in castables) | Eng. ref. CondFD §"Enthalpy" | Defer |

Not recommended: CTF (constant properties, unstable for massive walls); the building
convection correlations as replacements (no stated range, no Ra check, fitted to rooms);
Fisher–Pedersen / Khalifa / Beausoleil-Morrison (need ventilated-room ACH); the Slab/Basement
preprocessors; calling EnergyPlus or Kiva as libraries; using EnergyPlus's area-weighted
approximate view factors for a small box.

## References

- EnergyPlus source and engineering reference, commit `8470a217859636828887b084d6eba4486625ac7e`,
  https://github.com/NatLabRockies/EnergyPlus (files and lines as cited above);
  licence: `LICENSE.txt`.
- Kiva, https://github.com/bigladder/kiva, BSD-3-Clause.
- Walton, G. N. (1983). *Thermal Analysis Research Program Reference Manual*, NBSIR 83-2655,
  pp.79–80 (as cited in `ConvectionCoefficients.hh`).
- Hottel, H. C. and Sarofim, A. F. (1967). *Radiative Transfer*, ch. 3. McGraw-Hill.
- ASTM C1340, *Standard Practice for Estimation of Heat Gain or Loss Through Ceilings Under
  Attics Containing Radiant Barriers by Use of a Computer Program* (as coded in EnergyPlus; not
  read here).
- Kruis, N. and Krarti, M. (2015). Kiva validation against BESTEST ground-coupled cases (as cited
  in the engineering reference).
- Neymark, J., Judkoff, R. et al. (2008). *IEA BESTEST In-Depth Diagnostic Cases for Ground
  Coupled Heat Transfer Related to Slab-on-Grade Construction*, NREL/TP-550-43388; Delsante,
  A. E., Stokes, A. N. and Walsh, P. J. (1983), the GC10a analytical solution.
