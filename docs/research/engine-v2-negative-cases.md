# Negative cases for engine v2's statics

Every reference kiln stood and fired (Olsen, *The Kiln Book*, 4th ed.; ADR 0014), so the 53 can
only show that a check is not too strict. An engine that passed everything would pass them too.
This file collects cases that **fail**, from analysis that has been published and checked, from
experiments, and from the book's own failures, and turns them into tests for v2
(`docs/adr/0017-engine-v2.md`). Gathered 2026-11-09. Marks as elsewhere: **Verified** (read in
the source, here or in the research file named), **Snippet** (a search extract only), **Derived**
(statics on sourced inputs, worked here), **Not read**.

## 1. Analytic limits: thinner than this cannot stand

Each is a least thickness under self-weight on Heyman's assumptions (no tension, unlimited
compression, no sliding). Below it no line or network of thrust fits inside the masonry, so the
structure is a mechanism and falls.

| Case | Least thickness | Status | Source |
|---|---|---|---|
| Semicircular arch (Couplet–Heyman) | t/R = 0.1075 (on the centre line's radius) | Verified | Maia Avelino, Iannuzzo, Van Mele & Block, SAHC 2020, §4.1: TNA limit 0.1079 "against the analytical 0.1075" (masonry-statics.md M3, [M3]) |
| The same, with its hinge | 0.10748, intrados hinge at 54.48° from the crown; Heyman's earlier 0.106 at 58.8° | Snippet | attributed to Ochsendorf in a Vietnamese J. Sci. Tech. paper (search extract, not read; below) |
| Circular arches of any half-angle | Heyman's table by half-angle | Verified | `core/src/kilndesigner/data/steel.yaml` (Rizzi et al. 2010; domes-over-doors.md §D3 [D5]) |
| Hemispherical dome, hoop forces allowed | t/R = 0.042 (Heyman 1977); 0.041 (Lau's modified thrust line; TNA t'/R = 0.041) | Verified | Lau 2006 p.55; SAHC 2020 §4.2 (masonry-statics.md M3) |
| Hemispherical dome, no hoop force (cracked into lunes) | t/R = 0.069 | Verified | Lau 2006 p.54 |
| Rectangular groin vault, corners supported | t'/R = 0.061 (cross diagram), 0.084 (fan) | Verified | SAHC 2020 §4.3 (masonry-statics.md M4) |
| A heated arch in a rigid frame | no maximum-thrust state when T/R ≥ 1/cos φ − 1: HarbisonWalker's "stress excessive" | Derived | arch-thrust-theory.md §3, §8 |

The first and the dome rows are the cleanest negative tests: a published number, a mechanism, and
a margin either side. (2026-11-10, §8: the dome rows are a hemisphere's, a shallower dome needs
less; the groin vault's row is for four corner supports, R half the larger span.)

## 2. Rigid blocks: walls that a thrust pushes over or along

| Case | Fails when | Status | Source |
|---|---|---|---|
| A wall standing alone under a thrust H at height h | H·h > W·b/2 (the resultant leaves the base) | Derived | statics; Heyman's no-tension assumption (arch-thrust-theory.md) |
| A bed joint under a thrust | H > μ·N; μ 0.6–0.7 cold (BIA), 0.50 hot (Oliveira et al. 2021) | Verified (μ); Derived (case) | mortar-and-brick-strength.md; structure review #3 |
| A 48 in arch at 1.5 in/ft, 9 in ring, on a 13½ in end wall | friction alone can't hold the top 41 in of wall (μ_need 1.96 at the springing joint against 0.6) | Derived | `docs/reviews/2026-11-physics-review-structure.md` #3; `test_vault.py` |

The first row leaves out the arch's own weight on the wall's top, and so would condemn six
reference kilns whose walls carry their half circles alone: restated in §8 (N3), the resultant of
everything on the wall. The third is restated in §7 (N4).

## 3. Three Olsen kilns changed past a limit

These were probed against v1 on 2026-11-09 by a script that wasn't kept, and its output wasn't
saved. v1 was reported to pass all three without a statics error or warning. That hasn't been
re-run.

| Probe | Change | Limit crossed | v1 |
|---|---|---|---|
| N1 | meaders-david's 60 in half-circle (p.115) with a 3 in ring | t/r 0.095 < 0.1075 (§1) | thrust reported, "carried by the kiln's masonry"; no ring check on a roof arch across the width |
| N2 | singh-coal's 84 in dome (pp.133–135) raised to a hemisphere, 1 in thick | t/R 0.024 < 0.041 (§1) | an info note: the band isn't sized outside Lau's range |
| N3 | the fast-fire arch (27 in, 1½ in/ft, 4½ in IFB; p.139–140) declared buttressed, no frame | 30 lb/ft cold at 36 in against a 4½ in IFB wall of about 34 lb/ft (§2; Derived) | `buttressed: true` taken on trust |

For each there are two positive controls:
- the kiln as built, which must stand;
- the change made just short of the limit, which must also stand, with its factor of safety
  reported.

## 4. Failures the book records

None is a masonry arch falling; they are the book's own negative evidence, and v2 should not
contradict them.

| Page | What failed | Kind | Use |
|---|---|---|---|
| p.47 | a ring arch "opened almost ½ in" in firing; a steel tie might have helped | arch movement hot | a hot-thrust case without a printed span (olsen-kilns.md `olsen-chamber-p23`) |
| p.134–135 | a free-standing bag wall "has a tendency to collapse": notch the chamber wall instead | wall stability | a qualitative check on free-standing internal walls |
| p.63, Fig 2-62 | fibre blanket and board wired in place: roof and walls collapsed | fibre anchoring | out of masonry statics; a refusal for wired fibre |
| p.62 | on a twice-daily cone 10 fibre kiln the Kao-Lok anchors' packing leaked and the Inconel studs oxidised away | anchor service | an anchor's service temperature |
| p.71 | blanket veneered onto hard brick has failed | fibre over brick | as above |
| p.35 | thin nitride-bonded SiC shelves cracked near the inlet flue | furniture, thermal shock | none (no data) |
| p.243 | a corrugated plastic shed roof melted and caught fire when flame leaked through the arch, door and salt ports of Chappell's salt kiln | clearance, leaks | Q4 (safety), not statics |

## 5. Experiments that found collapse: found, not read

These would give measured collapse thresholds (a support spread, a tilt) for arches whose t/R is
known. None was read in this round; each is listed so nobody cites a number from it without
reading it.

- J. A. Ochsendorf, *Collapse of Masonry Structures*, PhD thesis, Cambridge 2002, ch. 5 "The
  Masonry Arch on Spreading Supports" (§5.5 spread limits at collapse, §5.7 experimental
  results). https://www.repository.cam.ac.uk/bitstream/1810/244820/1/Ochsendorf25710.pdf : over
  the fetch tool's 10 MB limit.
- J. A. Ochsendorf, "The masonry arch on spreading supports", *The Structural Engineer* 84(2),
  2006. https://www.istructe.org/journal/volumes/volume-84-(published-in-2006)/issue-2/the-masonry-arch-on-spreading-supports/
  (abstract only: as the supports spread, the crown descends and the thrust rises).
- A Le Quy Don Technical University paper (J. Science and Technique) on 20-block semicircular
  models, t/R 0.15 and 0.24, under span expansion, reduction and abutment settlement: hinges at
  about 54° spreading and 45° closing (Snippet; the PDF could not be read here).
  https://jst.lqdtu.edu.vn/index.php/sce/article/download/952/626/6452
- S. Galassi, G. Misseri, L. Rovero, G. Tempesta, reduced-scale PVC block arches with a
  horizontal or vertical support settlement, *Engineering Structures* 173 (2018); and Galassi,
  Misseri & Rovero, *Engineering Failure Analysis* (2021), large displacements on spreading
  supports (Snippet).
- S. Coccia, F. Di Carlo, an experimental study of the horizontal support displacement a
  semicircular arch sustains under self-weight before collapse, ECCOMAS 2023; and a kinematic
  approach, *Structures* (2026) (Snippet). https://art.torvergata.it/handle/2108/362106
- Paris et al. (2026): large-scale tests of arches on spreading supports against discrete-element
  analysis (Snippet).
- M. DeJong, J. Ochsendorf (2006 onward): tilting and shaking-table tests of dry-joint arches
  (Snippet; no numbers found).
- **Read (2026-11-10):** S. Coccia, F. Di Carlo, Z. Rinaldi, "Collapse displacements for a
  mechanism of spreading-induced supports in a masonry arch", *Int. J. Adv. Struct. Eng.* 7(3)
  (2015) 307–320, doi 10.1007/s40091-015-0101-x, open access; the article's text on SpringerLink,
  read through the fetch tool (its quotes as extracted). It reports Ochsendorf's test (secondary for
  Ochsendorf): "The arch is characterized by 16 voussoirs cast as individual concrete blocks with a
  50-mm radial thickness"; "The mean radius R is equal to 220 mm, and the thickness–radius ratio
  (t/R) is 0.23"; "The experimental collapse took place for a displacement value of 30 mm (span
  increase equal to 15.4 %)"; their kinematic "ultimate displacement is equal to 32.24 mm, related
  to a span increase of 16.53 %"; "The span increase developed by Ochsendorf with a static
  procedure, is 16.9 %". The span's increase is 2u over the inside span (Derived: 2 × 30 mm over
  2 × 195 mm is 15.4 %). Their Eq. 18, a regression "with the ordinary least squares method" of
  their results, "more effective for a number of voussoirs higher than 25–30": u_coll/t =
  −365.44(t/R)⁶ + 1022.5(t/R)⁵ − 1167.8(t/R)⁴ + 702.36(t/R)³ − 238.84(t/R)² + 44.62(t/R) − 2.766.
  Assumptions: "a no-tension material with infinite compression strength", "infinite shear
  strength", rigid blocks, hinges "always in the joints", large displacements; the intrados hinge
  "moves slightly toward the center" in the deformed state. Used for N5 (§8).
- Still not read: the Le Quy Don paper (its PDF came back as compressed streams), Ochsendorf's
  thesis and 2006 paper themselves, Galassi et al., Paris et al.

## 6. The negative tests proposed for v2

v2 flags no kiln until it works as a whole (ADR 0017). So each test checks the computed result:
whether a thrust state exists, where a resultant falls, and the friction a joint needs. It does
not check for an error or a warning.

| Id | Test | Expected result | Source |
|---|---|---|---|
| N1 | semicircle at t/r 0.095 (meaders-david, 3 in ring) | no thrust line fits inside the ring: it can't stand | §1, §3 |
| N1+ | the same at t/r 0.11 and 0.22 | a thrust line fits; factor of safety on thickness about 1.02 and 2.05 (t over the least, 0.1075) | §1 |
| N2 | hemisphere at t/R 0.024 | no admissible state, with or without hoop force (below 0.041) | §1 |
| N2+ | hemisphere at t/R 0.05 (between 0.041 and 0.069) | stands only with hoop force; cracked into lunes, no admissible state | §1 |
| N3 | fast-fire arch on free-standing 4½ in IFB walls | the walls overturn: the resultant leaves the base | §2, §3 |
| N4 | review #3's end wall (48 in, 1.5 in/ft, 9 in ring, 13½ in wall) | friction alone can't hold the top 41 in of wall (μ needed 1.96 at the springing joint against 0.6) | §2 |
| N5 | an arch on spreading supports past its spread limit | it collapses: a mechanism forms | §5 (Coccia et al. 2015, read 2026-11-10); built, §8 |
| N6 | a groin vault at t'/R 0.05 | no admissible state, once crossings are checked | §1; restated, §8 |
| P | all 53 reference kilns as built | each stands: an admissible state exists | ADR 0014, 0017 |

## 7. What v2's statics gives (2026-11-10)

Run in `core/tests/v2/test_statics_arch.py` and `test_statics_section.py` (Derived: v2's own
limit analysis on the inputs named).

| Id | v2's result | Test |
|---|---|---|
| N1 | least t/R of a semicircle 0.10746 (160 voussoirs), 0.107478 (320); t/r 0.095 has no admissible state; 0.11 and 0.22 stand, factors on thickness 1.02 and 2.05. Through the whole pipeline too: meaders-david's half-circle with a 3 in ring, cut from the engine's solids, can't stand cold or hot; as built (9 in) it stands | `test_n1_a_semicircle_needs_its_least_thickness`, `test_statics_kiln.py::test_n1_through_the_engines_own_solids` |
| N3 | the fast-fire arch on its free 4½ in IFB walls, 36 in high: no admissible state; with the frame, it must give at least 7.08 lbf/ft a side, the walls hinging on their outer toes | `test_n3_…`, `test_without_its_frame_the_fast_fire_kiln_falls` |
| N4 | **restated.** The review's μ needed of 1.96 took HarbisonWalker's mid-thickness thrust, 465 lbf/ft. v2 lets the arch settle to its least thrust, 168.8 lbf/ft, on an end wall that spreads (Heyman); the springing bed then needs μ 0.518 with the skewback's own weight on it (0.71 with none). So the 41 in wall stands cold (μ 0.60) and slides hot (0.50); a 60 in wall overturns either way, and a buttress must give 16.15 lbf/ft | `test_n4_the_reviews_end_wall_restated` |
| P (part) | 37 of the 53 reference kilns are modelled (sprung arches across the width, at each station where the width changes; the catenary; round domes; open tops) and every one stands cold and hot (μ 0.50 and the C16 stand-in); the 16 not modelled are named with what is missing | `test_statics_reference.py` |
| N2 | a hemisphere at t/R 0.024 has no admissible state, with hoop compression or as lunes; v2's least t/R is 0.0428 with hoops (Heyman 0.042; Nodargi & Bisegna's refined 0.04284) | `test_statics_dome.py::test_n2_…`, `test_a_hemisphere_needs_four_per_cent` |
| N2+ | **restated (2026-11-10).** At t/R 0.05 the dome cracked into lunes stands in v2: the lunes' least t/R is the same 0.0428, hoop compression never being active at the limit (the binding zone is low, where hoops would pull). That is Heyman's lune result: his 0.042 negated hoop forces (Lau 2006 p.18, p.55). Lau's 0.069 (p.54) is the edge of his program's search, which tested t/R only at 0.05 and 0.10 between (p.45), found no-hoop solutions at 0.05 only up to α = 86° (p.50), started the thrust line just under the crown's extrados and kept it off both surfaces (p.45), and sought "stable dome geometries" rather than incipient collapse, which Lau gives as the reason his no-hoop minima exceed Heyman's (p.55; `masonry-statics.md` M3). So the case's expectation came from a deliberately conservative search: lunes fall below 0.0428 (N2 at 0.024 falls), and stand at 0.05 | `test_statics_dome.py::test_a_hemisphere_needs_four_per_cent` |

N4's expected result in §6 rested on one fixed line of thrust, the thing v2 replaces; the case
is kept, with v2's numbers above as its expectation.

## 8. N1–N6 against the reference kilns (2026-11-10)

The owner's rule for this round: "if the n1-n6 are in conflict with the reference kilns, those
need to change". Each case's criterion was checked on every reference kiln as built, with v2's own
geometry (the design files' spans, rises, rings and walls as the engine lays them out). Where a
kiln stands but the criterion would condemn it, the case's limit or premise is restated, never the
kiln. Then each case, as stated or restated, is a test that fails in v2's numbers
(`core/tests/v2/test_statics_negative.py`, `test_statics_spread.py`). Run: the scripts in
`scratch/statics-d/` (survey, walls, extras, spread_kilns); the numbers below are Run on v2 unless
marked.

| Case | Criterion | Reference kilns checked | In conflict | Restated | Fails in v2's numbers |
|---|---|---|---|---|---|
| N1 | a circular arch's least t/R at its half angle, under its own weight on fixed supports: 0.1075 of the centre line's radius for a semicircle (Couplet–Heyman; v2 0.10746) | 42 arch rings of 39 kilns (across, at the widest station, or each chamber's along the draft, one of each size): the least margin is Tobe's 10 ft semicircle of 9 in, t/R 0.1395, 1.30 times its least; Kato 1.93; the other semicircles 2.1–3.9; the flat IFB arches 60–130 times | none | no (the premise, self-weight on fixed supports, stated) | yes: meaders-david's half circle with a 3 in ring through the pipeline, cold and hot; a semicircle at 0.095 |
| N2 | a hemisphere's least t/R: 0.0428 (Heyman 0.042; Lau's no-hoop 0.069, restated in §7) | round domes: singh-coal (springing 59.5° from the crown, t/R 0.169), Breda (53.1°, 0.077); sail domes, on the sphere through the plan's farthest point: miravet 0.104, hollyweird 0.046, conrad-teardrop 0.026 | yes, read as any dome's limit: conrad-teardrop's cast dome is under 0.042, Hollyweird's under 0.069 | the limit is the hemisphere's. A dome's least t/R falls with its springing (v2, with hoop forces: 0.0428 at 90°, 0.016 at 80°, 0.004 at 70°, 0.0003 at 60°, under 0.0002 below; cracked into lunes 0.041 down to 60°, 0.037 at 53°, 0.017 at 30°): the shallow cap has no low zone where hoops would pull, the zone that binds a hemisphere (membrane hoop tension starts 51.8° from the crown, `masonry-statics.md` M3). The sail domes' strips stand in v2 down to 0.45 in (miravet), 0.03 in (conrad-teardrop, hollyweird) | yes: singh-coal's dome raised to a hemisphere 1 in thick (t/R 0.024), through the pipeline: no state cold or hot; 2½ in (t/R 0.058, between 0.042 and 0.069) stands |
| N3 | a wall standing alone overturns when H·h > W·b/2 (§2) | the 27 kilns with a sprung arch across on walls (three more spring from the ground): the bare rule's ratio with v2's least thrust, and v2's section of the ring on its two walls standing alone (`arch.on_walls`, held by nothing) | yes: six kilns whose walls carry their half circles alone in v2 (Kitade's frame and the others' buttresses giving nothing): kitade-tojilo (ratio 2.01), kato-coal 1.15, bae-gilgama 2.24, meaders-cheever 3.16, anagama-hole 3.39, tamba 4.81 | the rule left out the arch's own weight on the wall's top: a half circle springs level, its vertical load bearing on the wall and holding it (Derived: kato-coal's half arch, 556 lbf/ft, bearing about 13½ in from the outer toe, adds about 626 lbf·ft/ft against the thrust's 546). Restated: the wall overturns when the resultant of everything on it, the arch's vertical load included, leaves its base, as v2's LP finds it. Every kiln whose walls fall alone in v2 is a segmental arch, where skewback, wall and arch make the acute angle at which Olsen says steel must hold the thrust (p.53, Fig. 2-35A), and its design file gives it a frame or a buttress; the half circles stand alone | yes: the fast-fire's arch on its free 4½ in IFB walls (bare ratio 5.18; v2: no state) |
| N4 | review #3's friction at the springing bed, with HarbisonWalker's mid-thickness thrust | restated in §7 (v2's least thrust) | — | §7 | yes, as restated (`test_statics_section.py`) |
| N5 | an arch on spreading supports collapses past a spread set by its t/R (Ochsendorf 2002, 2006; Coccia et al. 2015 Eq. 18; §5) | every reference arch's collapse spread, cold (μ 0.6), built in v2 (`spread.py`): the least is Tobe's, 4.9 % of its span (2.94 in a side; Eq. 18 for its t/R gives 2.94 in); the IFB arches 7.6 % and more, the flat ones snapping through where their three hinges line up (about 2.1 in a side on a 4½ in ring) | none: as built their supports are held, by a frame or masonry; the most an arch moves against them for good is its brick's permanent shrinkage, at most 1.0 % (Morgan K-26 at 2552 °F, 2025 sheet; −0.2 % at 2450 °F on the 2016 one; `morgan-k-ifb-sheets.md` §6), against 4.9 % | no | yes: built and checked on Ochsendorf's test arch (32.22 mm, 16.52 %, against 32.24 mm and 16.53 %) and Eq. 18 (within 1–3 % at t/R 0.15–0.4, 96 voussoirs); meaders-david's half circle, through its design file, stands to 6.34 in a side and falls past it |
| N6 | a rounded cross vault on its four corners alone: t'/R 0.061 by the cross diagram, 0.084 by the fan, R half the larger span (SAHC 2020 §4.3: their t/R 0.10 is 0.5 m on 10 m) | church-skaelskor 0.143 and fireworks-edmonton 0.111 by that R; on the flatter vault's own centre-line radius 0.128 and 0.079 | only on the fan's 0.084 read against the flatter vault's own radius (fireworks, 0.079) | the limit is the corner-supported semicircular vault's, R as the source takes it; the fan's 0.084 is a force pattern's, not the vault's (the cross diagram stands the same vault at 0.061, so by the safe theorem its least is at most that; and a lower bound below 0.061 isn't excluded either). The kilns' vaults are segmental and rest on walls all round, outside the source's premise; corner supports aren't in v2's grid (a slice can't end at a free edge: it would need the shell's in-plane shear) | the kilns' case: their vaults thinned past v2's own least fall (Church at 1½ in, its least 1.58 in; Fireworks at 2 in, its least 2.21 in) |

**Why the kilns stand where the bare criteria would condemn them** (each Derived from the sources
named): the sail domes are shallow caps, carried by their walls all round (`sail.py`); the half
circles' walls carry their arch's weight on their tops; the crossings rest on walls all round, not
four corners. No kiln's input was changed.

**What N5 adds to v2** (`v2/statics/spread.py`): the supports moved apart step by step; the blocks
below each intrados hinge move with their support, those above turn about it, the crown's hinge kept
on the axis; the opened joints touch at their hinges alone; each moved arch solved by the LP; the
hinge moves toward the crown where the arch moved about the next joint stands and about this one
doesn't. Refused where sliding governs the unmoved ring (a thick semicircle at μ 0.5–0.6: Fujiwara's
second chamber, t/R 0.42), for uneven springings, crossings and offset peaks. Cold only: no crushing
at a hinge (a hinge is a point contact; Coccia et al. assume "infinite compression strength" too),
so a flat arch's spread is its hinges' lining up. Not wired into `statics(kiln)`: the kilns' supports
as built don't spread.

**Olsen p.47** (§4): a ring arch on one of his chamber kilns opened almost ½ in in firing and stood.
If it is olsen-two-chamber's (the book doesn't say), a ½ in gap at a 9 in ring's hinge is a turn of
about 0.056 rad, about 1.8 in of spread a side (Derived: (rise + t)·θ), inside its collapse spread of
6.5 in: no conflict either way.

## Sources

As cited above; the research files named hold the full references: masonry-statics.md ([M2] Lau
2006; [M3] Maia Avelino et al., SAHC 2020), domes-over-doors.md ([D3], [D5]), arch-thrust-theory.md,
mortar-and-brick-strength.md, the structure review, and Olsen's pages via olsen-kilns.md and
kiln-reference.md. N5: S. Coccia, F. Di Carlo, Z. Rinaldi, "Collapse displacements for a mechanism
of spreading-induced supports in a masonry arch", *International Journal of Advanced Structural
Engineering* 7(3) (2015) 307–320, doi 10.1007/s40091-015-0101-x,
https://link.springer.com/article/10.1007/s40091-015-0101-x (read 2026-11-10, §5); through it, J. A.
Ochsendorf, *Collapse of Masonry Structures*, PhD thesis, Cambridge 2002, and "The masonry arch on
spreading supports", *The Structural Engineer* 84(2) (2006) 29–36 (not read themselves).
