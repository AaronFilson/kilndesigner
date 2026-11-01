# Masonry statics: lunettes, rampant arches, cracked domes, groins, steps, corbels, bearing (third round)

Third research round (2026-10-31) on the statics items left open in `blocked-items.md` §3, §5, §7,
§9, §10 and §12. Web search and fetch, with PDFs downloaded and their text extracted (pypdf). Marks
as in `blocked-items.md`: **Verified** = read in the source's text; **Snippet** = search extract
only; **Partial**; **NOT FOUND**. Primary = paper, thesis, book or standard; secondary = a page
that does not cite its source.

Short answer:

| # | Question | Status | Usable result |
|---|---|---|---|
| M1 | Opening (lunette) cut into a barrel vault: load share to the opening's ring | Verified (paper read in full); **no share given** | Method only: a line force (Dirac delta) concentrates along the intersection curve, larger than in a plain arch of the lunette's shape |
| M2 | Rampant arch, hot or cold thrust | NOT FOUND (beyond the cold statics already noted) | none new |
| M3 | Round dome past 51.8°: lunes, base thrust | Verified (Lau 2006 read in full; Maia Avelino et al. 2020 read) | H/W formulas and figures below; hemisphere minimum thrust ≈ 20 % of a lune's weight (already in `domes-over-doors.md`), plus Lau's Eqs 3.1–3.6 and the TNA dome figures |
| M4 | Groin (cross) vault: how the groins carry load, a check method | Verified (Maia Avelino et al. 2020 read; Block & Ochsendorf 2008 slides read) | One worked example: rectangular cross vault, total thrust 67.5–96.7 % of W at t/R = 0.10; limit t'/R = 0.061 with force carried along the diagonals |
| M5 | Catenary meeting the next chamber's at a step | NOT FOUND | none |
| M6 | Corbel limits for refractory brick hot; corbelled kiln roofs | NOT FOUND (refractory); one more cold building-code rule (Snippet) | none new for refractory |
| M7 | Allowable bearing stress / FoS for refractory brick | NOT FOUND; Trinks Vol. II read (no bearing value), Vol. I not online | none |

---

## M1. An opening cut into a barrel vault (vault with lunette)

Source: M. Monaco, I. Bergamasco, M. Betti, "A no-tension analysis for a brick masonry vault with
lunette", *J. Mech. Mater. Struct.* 13(5) (2018) 703–714 [M1]. Primary. **Read in full** (14 pages,
text extracted from the publisher's PDF).

| Item | Text (verbatim) | Page / section | Status |
|---|---|---|---|
| Model | "The masonry vault is modelled as a membrane (thrust surface) subjected to compressive stresses only, contained within extrados and intrados surfaces, and carrying uniform applied loads." | p. 703, abstract | Verified |
| Equilibrium | Pucher stresses S_αβ = J T_αβ; with an Airy stress function F, "S11 = F,22, S22 = F,11, S12 = S21 = −F,12" (eq. 4) and the transverse equilibrium "L(F) = F,22 f,11 + F,11 f,22 − 2F,12 f,12 = p" (eq. 5), f being the membrane's height | §2, p. 706 | Verified |
| No tension | "F,11 + F,22 ≤ 0, F,11 F,22 − F²,12 ≥ 0 (7). These correspond to the condition on F(x1, x2) to be concave." | §2, p. 706 | Verified |
| The fold | "The only requirement of continuity for F gives as a result the possibility of a folded surface, with discontinuous Pucher stresses defined as a Dirac delta line whose definition domain is the projection Γ0 of the fold." Singular part "Ss = δ(Γ0) [[F,h]] k⊗k", k tangent to the fold (eq. 8) | §2, pp. 706–707 | Verified |
| Case | San Barbaziano, Bologna (1608–1612): nave 11.60 m wide; "thin masonry vaults (thickness 12.5 cm)"; uniform vertical load "p = 1800 N·m−2" | §3, pp. 707–709 | Verified |
| Stress level | "the stress intensity derived from the presented equilibrium solution is very low compared to the possible strength of the masonry, which can be considered ranging between four to six times the calculated values [Faella et al. 2012]" | §3, p. 709 | Verified |
| Where it concentrates | "the maximum stress concentration has been found at the springing of the vaults and at the intersection of the two vaults (Figure 9)" (FE comparison) | §3, p. 710 | Verified |
| Intersection vs arch | "there is an increase in the normal stress along the intersection curve ... compared to the same loading condition in an arch with unitary depth and the same geometry of the lunette, i.e., the directrix curve of the cylindrical vault". The comparison is a plot only (Fig. 11); its values are not in the text | §4, pp. 711–712 | Verified (statement); values NOT FOUND (figure only) |
| Builders' answer | "they realized technological details such as the carved stone ribs that counterbalance the stresses" | §4, p. 712 | Verified |
| Load share between vault and opening ring | not given; the paper gives no fraction, factor or formula for it | — | **NOT FOUND** |

Cited and identified, not read: Angelillo, Babilio & Fortunato, "Singular stress fields for
masonry-like vaults", *Contin. Mech. Thermodyn.* 25 (2013) 423–441 (the theory behind the fold);
Bergamasco et al., "A no-tension model for the analysis of combined masonry vaults", AIMETA 2017,
pp. 1387–1395 (no free copy found).

**For the engine.** `vault.py` (door through a buttressed tube's springing) and `door.py` assume
the door's ring carries half the vault's weight over it and the vault's thrust over the door is
reported, not sized (`complex-curves.md` step 5). The paper does not supply a split, so that
assumption is neither confirmed nor replaced. What it does establish (Verified): in a
compression-only solution the vault's load gathers as a *line* force along the intersection
curve (the groin round the opening), and the compression there is larger than in a free arch of
the lunette's own shape under the same load. So an arch check of the door ring under its own
share alone is not shown to be safe by this source. A sourced alternative the engine could use is
the method itself: any concave stress function satisfying eqs (5) and (7) inside the vault's
thickness proves safety (safe theorem); the line force on the fold is the jump in F's normal
derivative. That is a solver, not a rule of thumb. Status: **Partial** (method Verified, no
number).

## M2. Rampant arches (springings at different heights)

Searched: Huerta's open papers (UPM archive; "arco rampante"), Heyman, SAHC/ICSA proceedings,
Italian and Spanish terms. **NOT FOUND**: no hot or cold thrust table, factor or worked example for
a rampant arch. Related, not the same case: Zampieri et al. (2018) on arches with a
non-horizontal *settlement* of a springing (already listed as `arch-springs.md` [P2]). Huerta's
*Arcos, bóvedas y cúpulas* (2004) is the likeliest printed source; no free copy.

**For the engine.** `frame.py` (~line 1106, "springing unevenly") already uses the three-hinged
arch with unequal halves and HarbisonWalker's largest printed heated factor
(`frame_checks.py` line 68). Nothing here replaces either. What the safe theorem gives (Verified
as a principle in [M1] p. 704 and [M3] §2: "if any admissible stress field is found for a given
structure, then, the structure is safe") is that the engine's own thrust-line search through the two
springings at their own heights is a valid lower-bound check; it does not give a hot factor.

## M3. A round dome past 51.8° from the crown: lunes and base thrust

Sources: W. W. Lau, *Equilibrium Analysis of Masonry Domes*, MIT S.M. thesis, 2006 [M2] (already
`domes-over-doors.md` [D3]; this round extracted the whole text, 172 pages, and read Ch. 3 in full);
R. Maia Avelino, A. Iannuzzo, T. Van Mele, P. Block, "New strategies to assess the safety of
unreinforced masonry structures using thrust network analysis", SAHC 2020 [M3], read in full.
Heyman, *Equilibrium of Shell Structures* (1977) is quoted here through Lau only (secondary).

| Item | Text (verbatim) | Where | Status |
|---|---|---|---|
| Lune model | Heyman (1977) "derived the minimum thickness-to-radius ratio, t/R, by simplifying the lune analysis to two dimensions and assuming no hoop force transfer between individual lunes" | [M2] p. 18 | Verified (Heyman via Lau) |
| Safe for the whole | "if a thrust surface is found that lies within one lune, then stability is satisfied for the 'original undivided structure' (Heyman 1977, p. 109)" | [M2] p. 35 | Verified (via Lau) |
| Hemisphere thrust | "For a lune of a hemispherical dome of sufficient thickness, the modified thrust line method estimates the minimum thrust to be about 20% of the lune's weight, regardless of θ and t/R." | [M2] p. 51 | Verified (already in `domes-over-doors.md`) |
| Trend | "shallow domes thrust more than deeper domes, relative to self weight ... H/W is inversely related to α"; "an inverse relationship between t/R and H/W with or without the presence of hoop forces" | [M2] pp. 51–52 | Verified |
| Hoop forces barely change H | "While hoop forces were shown to have negligible impact on the magnitude of H/W, their importance is clear [in] a comparison of geometries of lunes with and without hoop forces, for which the modified thrust line method found satisfactory thrust lines"; no-hoop H/W "within a few percent" of the with-hoop values | [M2] pp. 50, 53 | Verified |
| Minimum thickness, no hoop force | "Without hoop forces, the modified thrust line program predicts a minimum t/R ratio of 0.069 for a hemispherical dome, which is more conservative than Heyman's estimate of 0.042" | [M2] p. 54 | Verified |
| Base thrust per length (Eq. 3.1) | "At the base of the dome, h, the horizontal thrust in units of force per length of circumference is given by" h = H / [a θ (sin α − sin δ)] (a the median radius, θ the lune's plan angle in radians, α the embrace angle, δ the truncation angle, 0 for a spherical dome) | [M2] p. 56 | Verified (equation layout garbled in extraction; reading checked against the length "a θ(sin α − sin δ)" printed on p. 62) |
| Linear fit (Eq. 3.2) | "a simple linear equation may be written to approximate H/W within 20% of the value determined by the modified thrust line analysis, as a function of α in radians: H/W = −0.583 α + 1.123 for α ≥ π/3" | [M2] p. 56 | Verified |
| Wider lunes (Eqs 3.3–3.5) | for n lunes of angle θ′: n odd, H_net = H[1 + 2 Σ_{i=1..j} cos(i θ′)], j = (n−1)/2; n even, H_net = 2H Σ_{i=1..j} cos((2i−1)θ′/2), j = n/2; and W_θ = n W_θ′. Example: "a lune with θ = 130° will have a net minimum thrust 110 times the minimum thrust of a lune with θ = 1°" while its weight is 130 times | [M2] pp. 56–57 | Verified (sums reconstructed from garbled extraction; check the page image before coding) |
| By statics (Eq. 3.6) | "Assuming a pin support at the mid-point of the lune's bottom edge, and a vertical roller support at the dome's extrados at the centerline, the minimum horizontal reaction at the crown, H, to prevent inward rotation due to self-weight is" H = W (a sin α − x_cg lune) / ((a + t) cos δ − a cos α), "t is equal to half the dome thickness (Fig. 3.17)"; "W is the weight of the lune (Eq. 2.5), x_cg lune is the center of gravity of the lune (Eq. 2.6)" | [M2] pp. 58–59 | **Verified on the page image (2026-10-31)**: the denominator is (a + t) cos δ − a cos α, *not* the a(cos δ − cos α) + t reconstructed before (the two agree only for δ = 0) |
| Its accuracy | "for domes with α < 40°, the minimum thrust calculated by the modified thrust line analysis will be about 5 to 20% lower than that calculated with static equilibrium equations. As the embrace angle approaches 90 degrees, the thrust values from the two methods are, for the most part, within 5%"; but the equations "reveal nothing about the dome's stability" | [M2] p. 59 | Verified |
| Lune weight (Eq. 2.5) | w_i = θ·ρ·(r³ − r′³)/3 · [cos β − cos γ − (γ − β)·sin δ], "r = a + t, r' = a – t, ρ is the material unit weight" | [M2] p. 36 | **Verified on the page image** (as reconstructed) |
| Centroid (Eq. 2.6) | x_cg = 3(r⁴ − r′⁴)/(8(r³ − r′³)) · sin(θ/2)/θ · [(γ − β)(2 + 4 sin²δ) + (8 sin δ)(cos γ − cos β) − sin 2γ + sin 2β] / [cos β − cos γ + (β − γ) sin γ] | [M2] p. 36 | **Read on the page image.** As printed the denominator's last term is (β − γ) sin γ, which for a hemispherical lune (β = 0, γ = π/2) gives 1 − π/2 < 0, a negative centroid: likely a typo for −(γ − β) sin δ, Eq. 2.5's bracket. With δ = 0 the engine uses the bracket cos β − cos γ, which integrating over the shell confirms (thin hemisphere: x_cg = πa/4) |
| Hoop forces, least thickness | "With hoop forces ... For a hemispherical dome, the modified thrust line method predicts a minimum t/R of 0.041" | [M2] p. 55 | Verified on the page image |
| Eqs 3.3–3.5 | as reconstructed above; condition "provided that nθ′ ≤ 180°", for "a lune with θ ≤ 90°" | [M2] p. 57 | **Verified on the page image** |
| Eq. 3.1 | h = H / [a θ (sin α − sin δ)] | [M2] p. 56 | **Verified on the page image** |
| Eq. 3.7 | y_TL = k·a(cos δ − cos α), "k is given in Table 3.1 for a lune of θ = 1°"; the worked example is the *height* of the thrust line's last point, not a thrust | [M2] p. 62 | Verified on the page image |
| Half dome | "For a half-dome with α = 90°, H/W is between 0.12 and 0.18, which is comparable to Heyman's study of estimated thrust as H = 0.068 W_dome, where W_dome is the weight of a complete hemispherical dome" | [M2] p. 61 | Verified (Heyman via Lau) |
| Into the wall | the thrust line enters the supporting wall with slope (H/W)⁻¹; Eq. 3.7 y_TL = k a (cos δ − cos α), k from Table 3.1; worked: t/R = 0.04, α = 60°, a = 25 ft, median height 12.5 ft, y_TL = 1.005 × 12.5 = 12.56 ft | [M2] pp. 61–62 | Verified |
| TNA, hemisphere, t/R = 0.10 | radial form diagram: "(T/W)min=19.8% and (T/W)max=430%"; limit "t'/R=0.041 where the thrust achieved is (T/W)limit=24.4%", GSF 2.42. The minimum-thrust state "shows a bi-axial compressive cap in the upper portion of the dome and an uni-axial stress state towards the supports, where null hoop forces are observed", compatible with "Heyman's 'orange-slice' mechanism" | [M3] §4.2, pp. 6–7 | Verified |
| TNA, arch check | semicircular arch t/R = 0.20: (T/W)min 31.6 %, max 51.2 %; limit t'/R = 0.1079 against the analytical 0.1075 | [M3] §4.1, p. 5–6 | Verified |

Eddy (1877) itself and Wolfe's graphical method: not read beyond Lau's Ch. 2 summaries (already
recorded as [K8]); no free scan of Eddy found in this round.

**For the engine.** `frame.py` `DomeRing.finding()` (NO_TENSION = 51.83) currently says that past
51.8° the membrane push "is the least it can be, not a design value". Sourced replacements:
(a) a lower-bound number for a cracked (lune) dome's base thrust: H/W ≈ −0.583 α + 1.123
(α in radians, α ≥ 60°, ±20 %), per-length thrust by Eq. 3.1; (b) or the statics estimate Eq. 3.6
(within 5 % near α = 90°). Both are *minimum* thrusts (the dome's least push for its own
weight); the TNA results [M3] show the maximum can be many times larger (430 % for the
hemisphere) if the base ring is pushed inward, so the band or wall must carry at least H, and the
engine should say "at least". Keep the refusal for thin domes: Lau finds no no-hoop solution below
t/R = 0.069 for a hemisphere. Range checked: spherical and pointed domes, t/R 0.001–0.20, α to 90°
(Lau's study range): outside it, refuse (ADR 0009).

**Built (2026-10-31, `frame.py` `lune_thrust`).** Eq. 3.6 with δ = 0, W from Eq. 2.5, x_cg from
the δ = 0 bracket above; per foot of the base by Eq. 3.1; Eq. 3.2 shown as a cross-check for
α ≥ 60°. Refuses outside t/R 0.03–0.20 (Fig. 3.17's range); notes t/R < 0.069. Checks: the
SAHC hemisphere t/R = 0.10 gives H/W = 0.203 against 19.8 %; a thin hemisphere 0.21 against
Lau's "about 20 %"; Lau's worked dome (t/R 0.04, α = 60°, a = 25 ft) gives 0.484 against
Eq. 3.2's 0.512 (median height 12.5 ft as printed).

## M4. Groin vaults (two barrel vaults crossing)

Sources: [M3] §4.3, read; P. Block, J. Ochsendorf, "Lower-bound analysis of vaulted masonry
structures", SAHC 2008 slides [M4], read.

| Item | Text (verbatim) | Where | Status |
|---|---|---|---|
| Case | "a rectangular rounded cross vault with dimensions 10.0x7.5m and a thickness of t=0.50m. The adimensional parameter is taken with regards to the larger span as t/R=0.10. The geometry is defined by the intersection of two cylinders, the smaller becoming an ellipse." "We consider only the four corners of the form diagram to be supported." W = 902 kN at ρ = 20 kN/m³ | [M3] §4.3, p. 9 | Verified |
| Force flow assumed | cross diagram: "an orthogonal path to the diagonals and then via the groins to the supports"; fan diagram: "connects the mid-span to the supports in a straight fashion" | [M3] p. 9 | Verified |
| Thrust, cross diagram | "(T/W)min=67.5% and (T/W)max=96.7% for the initial case t/R=0.10. The minimum thickness calculated in the cross diagram is found to be t'/R=0.061, for a thrust of (T/W)limit=76.9%" | [M3] p. 9 | Verified |
| Thrust, fan diagram | "(T/W)min=75.4% and (T/W)max=90.9%. The limit state is found for t'/R=0.084, corresponding to a thrust of (T/W)limit=80.7%"; GSF 1.64 (cross), 1.20 (fan) | [M3] p. 10 | Verified |
| T defined | the objective sums the horizontal reaction magnitudes over the supports, Σ √(R_x² + R_y²) (eq. 6), so T/W is the total over the four corners, not per corner | [M3] §3.2, p. 4 | Verified |
| Groins carry it | "for the cross diagram, the forces accumulate along the diagonals, while in the fan diagram, the forces are distributed and the compression force accumulate along the ridges"; the cross diagram, the higher GSF, "can be seen as a better approximation of the common crack pattern found on cross vaults, known as Sabouret cracks" | [M3] p. 10 | Verified |
| Heyman's slicing | "webs transmit vertical and horizontal loads to diagonal ribs or to groins that, in turn, convey these loads to piers" (Heyman's sliced model, as summarised) | Springer chapter 978-3-319-54738-1_6 | Snippet |
| Slicing, primary | "Through the slicing technique, the central surface of the webs is divided into a series of independent parallel arches entirely supported from the diagonal cross-ribs modelled as three-hinged arches. In the framework of limit analysis applied to masonry structures, the same approach was successively developed by Heyman [3,4] to clarify the path of the forces in masonry domes and masonry cross vaults and to evaluate the thrust value." Assumptions: webs coursed "in the 'French' way", "divided into a series of parallel arches of variable rise, span and width but with uniform thickness t"; ribs "modelled as parabolic arches with variable thickness and vanishing width (in particular, at the crown the ribs thickness is equal to t)" | [M7] §1, §3, pp. 2, 5 | Verified (text extracted). Heyman's own text still not read |
| Another example | groin vault (pseudo 3-D) "Hthrust (*) ... (*) as percentage of the weight of the vault 23% (min) 32% (max)"; the vault's geometry is shown only in a figure | [M4] slide 26 | Verified (numbers); geometry NOT FOUND |
| Parametric study | Maia Avelino et al., "Parametric Stability Analysis of Groin Vaults", *Appl. Sci.* 11 (2021) 3560, square footprints, three topologies | identified; publisher and repository blocked fetches (403/500) | NOT READ |

**For the engine.** Nothing yet models a groin (`complex-curves.md` step 6: Fireworks and Kanayama
wait for it). A sourced check method now exists: Heyman's slicing (webs as arches spanning onto
the diagonals, the diagonals as arches to the corners) is a lower-bound (safe) state; [M3] gives one
worked TNA result to test against (10 × 7.5 m, t = 0.5 m, four corner supports: total corner
thrust 67.5–96.7 % of W, limit thickness 0.061 × the larger radius). Use it as a test value, not a
rule: [M3] shows the result depends on the force pattern chosen.

**Tried (2026-10-31), not adopted.** The slicing was coded for crowns at one height (webs as
arches across their own vault landing on the groin, the half-diagonals three-hinged at crown and
corner, moments about the corner) and run on [M3]'s vault (semicircle R = 5 m × ellipse to the
same crown, t = 0.5 m, 20 kN/m³; weight 888 kN against the paper's 902). Hinges on the centre
surface: the diagonals need tension at the crown (inadmissible); corner total 57 % of W.
Hinges at the faces (slices from crown extrados to foot intrados, diagonal likewise): total
50 % of W, *below* [M3]'s least (67.5 %), so some thrust line must leave the shell; the
diagonal's crown force reaches zero near t/R ≈ 0.08 (cf. 0.061 cross, 0.084 fan). A sound
check needs the thrust lines shown inside the shell (a thrust-network or slice-by-slice
line-of-thrust search), not built. Also: with crowns at different heights (both Olsen crossing
examples) the groins meet the higher vault's side, not the middle; no source read covers it.
The groin stays unchecked.

## M5. A catenary meeting the next chamber's at a step

Searched again: noborigama construction, stepped multi-chamber vaults, Johanna kiln (St John's),
Japanese-language terms. **NOT FOUND.** The refusal in `geometry.py` (~line 381) stands.

## M6. Corbel limits for refractory brick when hot; corbelled kiln roofs

**NOT FOUND** for refractory or hot conditions. One more cold rule, Snippet only: Wisconsin SPS
321 (fireplaces and chimneys) "The corbeling shall not exceed one-inch projection for each brick
course" [M5]. `corbel.py` already uses TMS 402 and BIA (Verified there); nothing replaces it.

## M7. Allowable bearing stress or factor of safety for refractory masonry

Trinks, *Industrial Furnaces* Vol. II (1925, and the 1926 printing) full texts were read on the
Internet Archive [M6]. Volume II refers the arch thrust back to Vol. I ("the horizontal thrust
(which can be computed from the arch weight and the multiplying factor given in Volume I)",
1925 printing p. 234) and gives no bearing stress for brick. Volume I (1923), which holds "the design of roofs
and arches, pages 196 and 238", is not on the Internet Archive and no HathiTrust full view was
found. ASTM C16's 25 psi test load and makers' subsidence results are already in
`refractory-bearing.md`. **NOT FOUND**: no allowable or factor of safety. The bearing stays
shown, not checked (`frame_checks.py` ~line 733, `door.py` BEARING_NOTE).

Next: Trinks Vol. I (1923) pp. 196, 238 (library or HathiTrust search-only); Huerta (2004);
Heyman (1977) pp. 109–114 directly; Maia Avelino et al. (2021) full text.

---

## Sources

- [M1] M. Monaco, I. Bergamasco, M. Betti, "A no-tension analysis for a brick masonry vault with lunette", *J. Mech. Mater. Struct.* 13(5) (2018) 703–714, doi 10.2140/jomms.2018.13.703. https://msp.org/jomms/2018/13-5/jomms-v13-n5-p09-s.pdf . Read in full. (Same as `blocked-items.md` [K20].)
- [M2] W. W. Lau, *Equilibrium Analysis of Masonry Domes*, S.M. thesis, MIT, 2006. https://web.mit.edu/masonry/papers/wwLau_SMBT_2006.pdf . Full text extracted (172 pp.); Ch. 3 read. (Same as `domes-over-doors.md` [D3], `blocked-items.md` [K11].)
- [M3] R. Maia Avelino, A. Iannuzzo, T. Van Mele, P. Block, "New strategies to assess the safety of unreinforced masonry structures using thrust network analysis", SAHC 2020 (12th Int. Conf. Structural Analysis of Historical Constructions), P. Roca, L. Pelà, C. Molins (eds). https://www.scipedia.com/wd/images/d/d5/Draft_Content_643225908p732.pdf . Read in full.
- [M4] P. Block, J. Ochsendorf, "Lower-bound analysis of vaulted masonry structures", SAHC 2008, Bath (slides). https://web.mit.edu/masonry/thrustNetwork/SAHC08_ppt_block-ochsendorf.pdf . Read.
- [M5] Wisconsin Admin. Code SPS 321.28/321.29 (search extract). https://docs.legis.wisconsin.gov/document/administrativecode/SPS%20321.29(6)(d)
- [M7] C. Intrigila, N. A. Nodargi, P. Bisegna, "The unbuilt Musmeci parabolic cross vault reinvented as a dry-masonry structure", SAHC 2020. https://www.scipedia.com/wd/images/d/df/Draft_Content_303700414p1109.pdf . Text extracted (14 pp.), §1–4 read.
- [M6] W. Trinks, *Industrial Furnaces*, Vol. II (Wiley, 1925; 1926 printing). https://archive.org/details/industrialfurnac0000wtri ; https://archive.org/details/industrialfurnac0002trin . Full text (OCR) searched.
