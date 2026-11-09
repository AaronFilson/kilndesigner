# Physics review, part 2: structure and materials (step E, 2026-11-09)

Scope: the engine's structural and materials results, read in the code, against the sources
already in `docs/research/` (masonry-statics, arch-thrust-theory, arch-springs,
mortar-and-brick-strength, refractory-movement-and-mortar, refractory-bearing, steel-design,
castables, castables-minerals, curved-kilns) and the current limit-analysis literature. No engine
changes in this pass. The comparison script is `scratch/physics-e2/compare.py` (git-ignored; run
with `uv run python scratch/physics-e2/compare.py`, PYTHONIOENCODING=utf-8 on Windows). Its
numbers are quoted below.

Status marks: **fix now** (sourced, small, clear), **proposed** (needs a source, a design choice
or more than a small change), **keep** (sound as it is).

Literature this review measures against. "Read" means read for this or an earlier round (see
the research files); "cited" means known from the literature but not re-read this round, so it
backs a direction rather than a number.

- Heyman, *The Stone Skeleton* (CUP 1995) and "The stone skeleton", Int. J. Solids Struct. 2
  (1966): the three assumptions (no tension, unlimited compression, **no sliding**), the safe
  theorem, the geometric factor of safety. Read (arch-thrust-theory.md).
- Block, DeJong & Ochsendorf, "As hangs the flexible line", Nexus Netw. J. 8(2) 2006, and Block
  & Ochsendorf, "Thrust Network Analysis", J. IASS 48(3) 2007: thrust lines and networks as
  linear programs, minimum and maximum thrust found by optimisation, not by fixed hinges. Cited.
- Ochsendorf, "The masonry arch on spreading supports", The Structural Engineer 84(2) 2006:
  an arch on supports that move apart settles at its minimum thrust. Cited.
- Huerta, "Mechanics of masonry vaults: the equilibrium approach", Historical Constructions,
  Guimarães 2001: the equilibrium approach, sliding as a separate check. Cited.
- Gilbert & Melbourne 1994 (Struct. Eng. 72) and Gilbert, Casapulla & Ahmed 2006 (Comput.
  Struct. 84): rigid-block limit analysis with frictional (non-associative) joints; sliding can
  govern where the normal force is small. Cited.
- Lau, *Equilibrium Analysis of Masonry Domes*, MIT S.M. 2006: lunes past 51.8°. Read
  (masonry-statics.md §M3).
- Rizzi, Rusconi & Cocchetti (2010 onward): Couplet–Heyman least thickness. Read
  (domes-over-doors.md §D3).
- ArchLab (MATLAB thrust-line tool, typeset.io copy) and Nikolić et al., FME Transactions 2017
  (closed-form thrust lines for triangular arches and plate-bandes): found this round. Neither
  gives a rampant or two-radius arch case with numbers.

## Ranked findings

Ranked by what a user's result could suffer: safety first, then size of the change.

| # | Finding | Mark | Effect on a user |
|---|---|---|---|
| 1 | A round dome's band is sized on the membrane ring tension even past 51.8°, where the membrane force falls to nothing at a hemisphere and Lau's cracked dome still pushes | **fix now**, done 2026-11-09 | Band under-sized near a hemisphere (membrane 0 against Lau 20 lb/ft at α = 90° in the example) |
| 2 | `PeakArch.mid_line` puts the back half's points measured from the back run, not from the peak: `line_gap` is wrong for any off-centre peak | **fix now**, done 2026-11-09 | False "leaves the ring" warnings (gap 11 to 458 against a true 0.66 to 1.41); no example uses `peak_at` yet |
| 3 | No sliding check at the springing or the bed joints under it for arches whose walls stand alone (along-vault end walls, masonry-held arches) | **fix now** (as a warning), done 2026-11-09 | A 48 in arch at 1.5 in/ft on a 13½ in end wall: friction alone can't hold the top 41 in of wall |
| 4 | The middle-half check uses one fixed three-hinged line, not the best line | proposed | Over-strict: a level 4.5 in ring over 48 in at 12 in rise "strays 34 %" though it is 10 times the thinnest that stands |
| 5 | A catenary's feet are given the cold thrust only | proposed | Hot, feet held: 1.4× (4½ in ring) to 1.8× (9 in) the reported 13 lb/ft |
| 6 | Along-vault end walls held only by mortar in service ("building" frame) are checked cold only | proposed | Hot thrust 1.3–5.3× cold is not checked against the wall |
| 7 | Expansion growth 3/32 in per ft is applied to every brick, IFB and high-alumina too | proposed | Allowance ±30 % by material; not unsafe as stated |
| 8 | Heated factor past HarbisonWalker's table (T/S over 10 %) | keep | gas-crossdraft: 3.79× at T/S 10.7 %, said so in an info finding |
| 9 | Two-radius arch hot thrust = 5.34 × cold | keep | Cautious side (factor 1.2–3.9 likely) |
| 10 | B3 two-radius cold thrust `PeakArch.thrust` | keep | Matches an independent funicular to 4 digits |
| 11 | Sail dome as slices; level cold thrust; Heyman max thrust hot; Couplet–Heyman η | keep | Safe-theorem methods, checked against HW to 4 % |
| 12 | Lau Eq. 3.6 "least" push | keep | Up to 20 % over the true minimum below 40°; only used past 51.8° |
| 13 | AISC 360-16 §F10 angle chain, Appendix 4 retention, Giles's 600 °F | keep | Correct as coded; frame steel at 176 °F in the examples |
| 14 | Tie rods at 12,000 psi (HarbisonWalker) | keep | About 55 % of AISC's ASD tension on threaded rod; conservative |
| 15 | Jack-arch flat roof, H = 3qS²/(8t₁), μ_need = 4t₁/(3S) | keep | Middle-third derivation checks |
| 16 | Castable conductivity power law | keep | −9 % to +22 % on held-out castables, already quoted |
| 17 | Dry-out reach; burnout heat | keep | Conservative (stored heat left out) |
| 18 | Brick, shaped and castable allowance 5 %; wedge mortar with nothing added | keep, one note | Mortar under-bought by 15–25 % if the user misses the note |
| 19 | Round-6 open items: allowable bearing on refractory, hot cohesion, arch rise on heating, rampant-arch thrust, catenary at a step | not found | Stay out of the engine (ADR 0009) |

## 1. Round dome band past 51.8° (fix now)

**Code.** `frame.round_dome_ring` works out the membrane forces (Timoshenko §106) and, past
α₀ = 51.8°, Lau's cracked-lune least thrust (`lune_thrust`). The band is then sized by
`dome_band(kiln, ring.ring)` (frame.py:1686), where `ring.ring` is the **membrane** ring force,
a₀·N_α·cos α₀. The reported thrust (`DomeRing.thrust`) switches to Lau's, but the band does not.

**Why it is unsafe.** The membrane push N_α cos α₀ goes to zero as α₀ → 90°. A masonry dome past
51.8° can't carry the hoop tension the membrane state needs, cracks into lunes (Heyman; Lau §3;
the engine's own finding says so), and then pushes at least Lau's H. Script, a = 2 ft,
T = 4.5 in, 140 lb/ft³:

| α₀ | membrane push | Lau least push |
|---|---|---|
| 55° | 38 lb/ft | 25 lb/ft |
| 70° | 27 lb/ft | 25 lb/ft |
| 90° | 0 lb/ft | 20 lb/ft |

Near a hemisphere the band is sized for close to nothing, and Norton's factor of 5 multiplies
that nothing.

**Fix.** Size the band on T = max(a₀·N_α cos α₀, h_Lau·a₀) whenever α₀ > 51.8° and Lau's range
(t/R 0.03–0.20) covers the dome. Outside Lau's range past 51.8°, refuse to size the band (ADR
0009) rather than use the membrane force. Formula: h_Lau = (H/W)·W_dome/(2π a sin α₀), H/W from
Lau Eq. 3.6 (p.58), W_dome from Eq. 2.5 (p.36); both are already coded and cited
(masonry-statics.md §M3).

**Tests.**
- A round dome at α₀ = 90°, t/R = 0.1: the band's tension equals `lune_thrust(...).ring`, not 0.
- At α₀ = 55°: the band uses the larger, the membrane (38 > 25 in the script's case).
- At α₀ < 51.8°: unchanged (golden reports for round kilns stay the same).
- Past 51.8° with t/R outside 0.03–0.20: a refusal finding, no band size.

**Done (2026-11-09).** `DomeRing.band_tension` (frame.py) takes the larger and adds a working
step "Dome band: the ring tension it is sized on" with both forces and which governs; outside
Lau's range past 51.8° `band_refusal` gives an info finding and no band (warnings come only
from a failed check, ADR 0013). Tests: `test_revolved_domes.py::test_band_past_51_8_*`.

## 2. Two-radius arch: `mid_line` places the back half wrongly (fix now)

**Code.** `shell.PeakArch.mid_line` (shell.py:975–981) loops over `halves()`, which return each
half's own run `a`. It sets `u = a - du` for the front and `u = a + du` for the back. The back
half's u must be measured from the peak, `front_run + du`. When the arch is level the two runs
are equal, so the error doesn't show. That is why `test_shell.py:330` (monotone in the ring) and
the symmetric checks pass.

**Effect.** `line_gap`, and the `frame.peak_line` warning built on it, are wrong for any
`peak_at` ≠ 0.5:

| S, ρ, peak share, ring | engine gap | corrected gap |
|---|---|---|
| 48, 12, 0.5, 4.5 in | 0.344 | 0.344 |
| 48, 12, 0.35, 4.5 in | 10.95 | 0.656 |
| 48, 12, 0.25, 4.5 in | 457.5 | 1.372 |
| 60, 20, 0.30, 4.5 in | 51.8 | 1.414 |
| 36, 6, 0.40, 4.5 in | 3.04 | 0.427 |
| 48, 18, 0.35, 9 in | 6.31 | 0.735 |

All of these still warn after the fix (finding 4 explains why even the level arch does). The
numbers the user reads ("strays 1095 %") are wrong, though, and the message's "leaves the ring"
branch fires where the true line may not leave it. No example sets `roof.peak_at` yet; bidai and
kyoto are waiting on the user for it, so this should be fixed before either is entered.

**Fix.** In `mid_line`: `u = self.front_run - du if which == 0 else self.front_run + du`.

**Tests.**
- For share 0.35, the points' u run from about 0 to S (min ≈ −T/2·sin φ_f, max ≈ S + T/2·sin φ_b),
  and each half's points lie on its side of `front_run`.
- `line_gap` at share 0.5 is unchanged; at share s and 1 − s it is the same (mirror symmetry).
  The current code fails this.
- The H that `line_gap` solves, scaled to the intrados hinges, equals `thrust()`'s H: the
  corrected mid-line H is 0.354 against `thrust()`'s 0.415 at 48/12/0.35, the expected
  mid-line-vs-intrados difference (0.392 vs 0.461 when level).

**Done (2026-11-09).** Fixed as above. Tests: `test_shell.py::test_the_mid_line_measures_both_halves_from_the_peak`
and `::test_the_line_gap_is_mirror_symmetric` (the table's corrected gaps, and 0.344 level as
before).

**B3's cold thrust itself is right.** `PeakArch.thrust` (H = (W − W_f c_f/a_f − W_b c_b/a_b) /
(ρ(1/a_f + 1/a_b))) agrees with an independent funicular (4,000 pieces per half, moments of the
whole about the front springing, then of the back half about the peak) to four digits at every
case above, and equals `cold_thrust_factor` when level (0.4608). No published asymmetric
(rampant or two-radius) arch with worked numbers was found: ArchLab and Nikolić et al. 2017 give
methods and other shapes only. The symmetric limit and the independent funicular are the checks
available. Keep those as tests.

## 3. Sliding at the springing of walls that stand alone (fix now, as a warning)

**Code.** `frame_checks.vault_end_wall` and `vault_end_wall_uneven` check the end wall's
overturning only: the resultant inside the base, and in its middle third. The door arch has
`door_slide` (μ_need = H/N), and the flat roof has `flat_friction`. The roof arch's end walls and
`_arches_held` (masonry-held arches) have no sliding check. Heyman's safe theorem assumes sliding
can't happen; Huerta and Gilbert et al. treat it as a separate check, and it governs where the
normal force is small: the top courses of a buttress under a skewback.

**Effect.** Script: a 48 in span, 9 in ring at 140 lb/ft³, a 13½ in end wall at 140 lb/ft³,
μ = 0.6. At a bed joint z below the springing, sliding is held only if H_c ≤ μ(N + γ e z), with
N = W/2:

| rise | W | H_c | the wall would slide down to |
|---|---|---|---|
| 1.5 in/ft | 476 lb/ft | 466 lb/ft | 41 in below the springing |
| 2 in/ft | 501 lb/ft | 362 lb/ft | 27 in |
| 3 in/ft | 560 lb/ft | 258 lb/ft | 11 in |

At the springing joint itself, μ_need = 2H/W: 1.96 at 1.5 in/ft, 0.92 at 3 in/ft, against BIA's
cold 0.6–0.7 and Oliveira et al.'s hot value, both already in the engine (`FRICTION`,
`HOT_FRICTION`). In practice mortar bond, masonry over the skewback or the frame carry this, but
the engine counts none of them for an unframed end wall. The overturning check alone says "holds"
for walls that friction can't hold.

**Fix.** Add to `vault_end_wall` (and `_uneven`) a sheet line μ_need = H_c/(N + G_s), where G_s
is the wall over the joint checked (zero at the springing joint, so μ_need = H_c/N), required
≤ μ (`joint_friction`), level **warning**. Also give the depth z* = max(0, (H_c/μ − N)/(γ̄e)) down
to which friction alone can't hold. Under a frame (`framed=True`) it is info, as the overturning
finding is. Formula: Coulomb friction at a dry joint, BIA (masonry-statics.md; mortar-and-brick-
strength.md), the same as `door_slide`. Cohesion stays out: no hot cohesion was found (below).

**Tests.**
- The script's case: μ_need = 1.96 at the springing joint for 48 in at 1.5 in/ft, z* ≈ 41 in.
- At 3 in/ft: μ_need 0.92 > 0.6, z* ≈ 11 in.
- A framed vault: the same numbers, info level.

**Done (2026-11-09).** `frame_checks.end_wall_slide`, sheet `frame.end-wall-slide` (or
`-front`/`-back`), with μ the hot 0.50 from `joint_friction` (Oliveira 2021) as the door and
flat-roof checks take; wired into `vault.along_statics` and, for the kiln's outer front and back
walls, `shell._arches_held` (walls between chambers have an arch each side and aren't checked).
Warning standing alone; info under a frame or a building frame. Tests:
`test_vault.py::test_end_wall_sliding_*` (the review's 1.96 / 41 in and 0.92 / 11 in at μ 0.6).

## 4. The middle-half check uses one fixed line (proposed)

`PeakArch.line_gap` fixes the hinges at the mid-line's springings and the peak, and asks that
one line to stay in the middle half. Heyman's geometric factor of 2 means *some* line fits in the
half-thickness ring. The fixed three-hinged line is one candidate, so the check is sufficient but
far from necessary. For a level 48 in arch at 12 in rise with a 4½ in ring, the line strays 34 %
(fails ¼), yet `vault_ring`'s own Couplet–Heyman check gives k ≈ 10.

Current practice finds the best line instead: Block & Ochsendorf's TNA (and the 2D case, a small
linear program over the hinge heights and H, as in ArchLab), or Gilbert's rigid-block limit
analysis (LimitState:RING). For the engine, the small version is to minimise the worst stray over
the three hinge heights (crown or peak, and two springings) within the ring, a bounded 3-variable
search. Test: a level arch must give the same verdict as the Couplet–Heyman k ≥ 2 (`vault_ring`),
and the 4½ in/48/12 case must pass. Until then the warning over-calls; it never under-calls.

## 5. Catenary hot thrust (proposed)

`catenary_feet` reports H = w·a cold (13 lb/ft for catenary-gas-kiln), and the script confirms
w·a equals the mid-line three-hinged H (0.135 of the half weight, both ways). Hot, with feet held
(a curb, ties), the same Heyman maximum-thrust statics the engine uses for sprung arches (crown
intrados, feet extrados) gives 1.40× the cold value for a 4½ in ring and 1.82× for 9 in (40 in
span, 48 in high). Free feet (a catenary standing on a floor with nothing at its feet) take no
extra thrust. Proposal: report both, "cold H; if the feet are held, up to f·H hot", with f from
the same `_arch_moment` statics applied to the catenary's ring. Proposed, not fix-now, because
HarbisonWalker's table, the check on the sprung-arch statics, doesn't cover catenaries.

## 6. End walls held by mortar in service, checked cold only (proposed)

With `building_frame`, the frame comes off after building, and the end walls are checked against
the cold thrust only (`_end_finding`, "the design's judgment"). The hot thrust (heated factor
1.3–5.3×) is what such a wall carries every firing. Proposal: add the same overturning and
sliding sheets at H = f·H_c as a warning, saying that mortar and platform restraint are not
counted.

## 7. Expansion allowance (proposed)

`movement.py` applies Brosnan's fireclay 3/32 in per ft (0.78 %) to 2400 °F to every brick run,
IFB and high-alumina too, does not scale it to a cooler firing, and leaves half open (Bhatia).
That is sound and on the safe side for fireclay. For other bricks, makers' data sheets give the
reversible thermal expansion per material (typically 0.5–0.9 % at 1000–1400 °C for fireclay,
high-alumina and IFB). Proposal: a per-material `reversible_expansion` (%, at °F) from the data
sheets in materials.yaml, falling back to Brosnan's figure. **Arch rise on heating**: the Springer
paper (Refract. Ind. Ceram., 2014, doi 10.1007/s11148-014-9714-z) is paywalled. A mirror's
excerpt shows it computes a cold arch's rise from its brick count (corrected span 9063 mm → rise
about 1214 mm) and says such results are checked by computer modelling. Its hot rise was not
seen. The ICG TC11 "Crowns design & material choices" slides were fetched but couldn't be read as
text. The keep-arc-length relation sin(θ'/2)/θ' = S/(2(1+ε)L) stays proposed.

## 8–15. Keep

- **Heated factor** (`heated_thrust_factor`): Heyman's maximum thrust (hinges at the crown
  intrados and the skewback extrados) reproduces all 73 of HarbisonWalker's cells to 4 %. Past
  T/S 10 % it extrapolates and says so (gas-crossdraft: 230.6 / 60.9 = 3.79× at 10.7 %,
  1.61 in/ft). Script values: 1.47 at T/S 4 % and 1.5 in/ft; 3.89 at 10 % (HW prints 3.88).
- **Two radii, hot × 5.34**: no factor is printed for two radii; the largest is the cautious
  side.
- **Sail dome slices** (`dome_factor`, `_dome_steel`): Heyman's slicing technique is a safe lower
  bound; it ignores the hoop action that would lower the push. dome-castable-kiln: 437 lb/ft hot,
  5.7× cold, past HW's 5.34, warned. Rods 946 lb, 6,666 psi.
- **Couplet–Heyman η table**: η(90°) = 0.10743 matches Rizzi et al.'s CCH value; the
  Milankovitch correction is under 0.1 %.
- **Lau Eq. 3.6**: within 5 % of the thrust-line minimum near 90°, up to 20 % over it below 40°
  (Lau p.59); used only past 51.8°. The band question is finding 1.
- **AISC 360-16 §F10** (`angle_allowable`): My = 0.8·Fy·Sx, Mcr with the toe in compression,
  F10-2/3, leg local buckling F10-6 to 8 with Sc = 0.8 Sx, all as the specification. Appendix 4's
  ky and ke are for fires (short events); Giles's 600 °F continuous limit is kept as a warning.
  Creep of carbon steel starts around 700–800 °F, above that limit. The examples' steel runs at
  about 176 °F.
- **Tie rods**: HarbisonWalker's 12,000 psi on the stress area against AISC J3 (0.75 Fu/Ω,
  about 21.8 ksi on the nominal area for A36). Conservative. Springs: P = min(P_c + kΔS/2,
  P_rigid), sound.
- **Flat roof as a jack arch**: H = (qS·S/8)/(d/3) = 3qS²/(8d) with the line at the kern points;
  μ_need = (qS/2)/H = 4d/(3S). Checks.

## 16–18. Materials

- **Castable conductivity** (`castable.ConductivityLaw`): k = a(ρ/1000)ⁿ(1 + s(T − 400 °C)/1000),
  fitted to 9 IFB, 8 % rms, 25 % worst leave-one-out, −9 % to +22 % on two held-out castables.
  The literature's physical models (Maxwell–Eucken with pore radiation, castables.md [S46];
  Loeb, Russell, not found) need porosity and pore size, which a user's mix doesn't give. Keep the
  power law with its quoted error. Revisit if a third castable's sheet lands outside ±25 %.
- **Dry-out and burnout**: the reach check against the sourced schedule's thickest layer, and
  the burnout heat with stored heat left out (errs towards a warning). Keep. Open sources since
  2010 on steam spalling (Innocentini and co-workers) support slow ramps through 100–300 °C. They
  give no schedule by thickness for home mixes, so there is nothing to change.
- **Brick counts and waste**: the cut list takes a whole brick for each piece that can't come from
  an offcut, plus 5 % breakage (BIA TN 10). Wedge-joint mortar is bought "nothing added for
  waste", and the note asks the user to add BIA's 15–25 %. Small proposal: apply it to the
  quantity, with BIA TN 10 p.11 already cited.

## 19. Round-6 open items

- **Allowable bearing stress on refractory brick**: not found. ASTM C16 is a hot-load test for
  specifications, not a design stress (document-center / GlobalSpec abstracts). The engine keeps
  AISC J8 on the concrete platform only.
- **Hot cohesion of a mortared joint**: not found. Sliding (finding 3) stays friction-only.
- **Arch rise on heating**: see finding 7. Not retrieved.
- **Rampant-arch thrust**: no published worked case. B3's H is checked by an independent
  funicular instead (finding 2).
- **Catenary at a step**: no source found this round. Not modelled.

Things only Hibbeler or Dowling could settle: none here. Each check above rests on statics or the
cited masonry and steel sources.

## Sources found this round

- Springer DOI page and a university mirror excerpt, doi 10.1007/s11148-014-9714-z (paywalled).
- ICG TC11, "Crowns design & material choices" (PDF, not readable as text):
  https://icglass.org/pdf/technical-committees/tc11/
- ArchLab, a MATLAB tool for thrust-line analysis (typeset.io copy).
- Nikolić et al., FME Transactions 45(2) 2017: closed-form thrust lines for triangular arches.
- ASTM C16 abstracts (document-center.com, GlobalSpec).
