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
a margin either side.

## 2. Rigid blocks: walls that a thrust pushes over or along

| Case | Fails when | Status | Source |
|---|---|---|---|
| A wall standing alone under a thrust H at height h | H·h > W·b/2 (the resultant leaves the base) | Derived | statics; Heyman's no-tension assumption (arch-thrust-theory.md) |
| A bed joint under a thrust | H > μ·N; μ 0.6–0.7 cold (BIA), 0.50 hot (Oliveira et al. 2021) | Verified (μ); Derived (case) | mortar-and-brick-strength.md; structure review #3 |
| A 48 in arch at 1.5 in/ft, 9 in ring, on a 13½ in end wall | friction alone can't hold the top 41 in of wall (μ_need 1.96 at the springing joint against 0.6) | Derived | `docs/reviews/2026-11-physics-review-structure.md` #3; `test_vault.py` |

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
| N5 | an arch on spreading supports past its spread limit | it collapses: a mechanism forms | §5, once read |
| N6 | a groin vault at t'/R 0.05 | no admissible state, once crossings are checked | §1 |
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
| N2+ | **not reproduced.** At t/R 0.05 the dome cracked into lunes stands in v2: the lunes' least t/R is the same 0.0428, hoop compression never being active at the limit (the binding zone is low, where hoops would pull). Lau's 0.069 for lunes (2006 p.54) comes from his modified thrust line; the thrust-network probe also found lunes and hoops alike (0.043 with a springing free to move, 0.080 fixed at the base joint's middle; `tool-triples.md` §4). Which assumption gives 0.069 is open: read Lau ch. 2–3 for how the lune's springing and sections are taken | — |

N4's expected result in §6 rested on one fixed line of thrust, the thing v2 replaces; the case
is kept, with v2's numbers above as its expectation.

## Sources

As cited above; the research files named hold the full references: masonry-statics.md ([M2] Lau
2006; [M3] Maia Avelino et al., SAHC 2020), domes-over-doors.md ([D3], [D5]), arch-thrust-theory.md,
mortar-and-brick-strength.md, the structure review, and Olsen's pages via olsen-kilns.md and
kiln-reference.md.
