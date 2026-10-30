# Flat brick roofs: statics, bands and precedent

Checked: 2026-10-28. Scope: a flat roof of insulating firebrick (IFB) or castable over a studio
kiln, spans of about 1 to 4 ft, held by a steel band, frame or rods; in particular whether the
wall under one edge can be a full-height door. Every number has a source tag like [F3]. The tags
are listed under "Sources" at the end.

How values are marked (as in `kiln-hardware.md`):
- **Verified** means I read it on the page or in the PDF text itself.
- **Excerpt** means I saw it only in a search-engine snippet or summary.
- **Derived** means I calculated it from sourced inputs. The working is shown.
- **(secondary)** means a forum post or retailer page, passing on practice rather than a design rule.
- **NOT FOUND** means I found no source. Do not fill these gaps with guesses.

Notes on the sources:
- BIA Technical Notes 31A [F2] is a 1986 scan. Only page 1 has a text layer. Pages 2–8 were
  rendered to images and read off the images (equations checked by eye); marked "Verified
  (rendered page)". The scan is cropped at the top of some pages, so a few lines are missing
  (noted where it matters).
- The Kast-O-Lite data sheet [F16] is an encrypted PDF; it was rendered and read the same way.
- Rhodes [F6], Olsen [F7] and Nils Lou [F8] are borrow-only scans on the Internet Archive. Their
  quotes are stitched from overlapping full-text-search snippets (about a line each), as in
  `kiln-hardware.md` [S34], and are marked Excerpt.
- Some web pages (Merrill [F9], Finkelnburg [F10], Skutt [F23], the SECEM patent [F30], Heyman's
  chapter summary [F4], Masonry Magazine [F5]) were read through a fetch tool that returns quoted
  extracts rather than the raw page. Quoted text from them is marked Verified; their omissions are
  not evidence that the page is silent.
- Paragon's site returned HTTP 429 and Olympic's 403; Paragon was read from a Wayback copy,
  Olympic only through search summaries.

Cross-references: this adds to `kiln-hardware.md` §4 (sprung-arch frame, HarbisonWalker arch
method, steel data; Merrill's rods and angle are already there as [S16]), §6 (doors), and
`electric-kiln-hardware.md` §1 (bands, welded cases) and §9 (the example's flat 4.5 in roof).

---

## 1. Definitions

| Item | Value | Mark | Source |
|---|---|---|---|
| Jack arch (BIA) | "Jack - A flat arch with zero or little rise." "Camber: The relatively small rise of a jack arch." | Verified | [F1] |
| Depth of a jack arch (BIA) | "the depth of a jack arch is taken to be the vertical dimension of the arch at the springing" | Verified | [F1] |
| Flat arch (HarbisonWalker glossary) | "Arch, Flat: In furnace construction, a flat structure spanning an opening and supported by abutments at its extremities. The arch is formed by a number of special tapered brick, and the brick assembly is held in place by the keying action of the brick. Also called a jack arch." Also: "Flat Arch: An arch in which both outer and inner surfaces are horizontal planes." | Verified | [F3] |
| Suspended arch (HarbisonWalker) | "A furnace roof consisting of brick shapes suspended from overhead supporting members." The guide gives **no design method** for flat or suspended roofs, only for sprung arches (`kiln-hardware.md` §4.3) | Verified | [F3] |
| Heyman, masonry assumptions | "Idealised assumptions are made about masonry: it has zero tensile strength, unlimited compressive strength and zero sliding." | Verified (publisher's chapter summary only) | [F4] |
| Heyman, flat arch | "a 'flat arch', whose abutments can be joined by an internal straight line, does not collapse." "To keep the line of thrust within it, an arch must have at least a minimum thickness." | Verified (chapter summary only) | [F4] |

Heyman's "does not collapse" rests on unlimited compressive strength, zero sliding and abutments
that do not move. For a flat arch those three are exactly what is at stake (§2, §6). His full
chapter text was not read.

---

## 2. Statics of a flat (jack) arch (BIA Technical Notes 31A)

BIA TN 31A, *Structural Design of Brick Masonry Arches*, reissued July 1986 (first published
October 1967) [F2]. Page 1 Verified; pages 2–4 Verified (rendered page).

### 2.1 Scope and assumptions

| Item | Value | Mark |
|---|---|---|
| Minor arches | "Minor arches are those whose spans do not exceed 6 ft and with maximum rise-to-span ratios of 0.15." Jack and segmental arches are both minor arches (Fig. 1) | Verified |
| Basis | "the hypothesis of least crown thrust" (TN 31, older edition) | Verified |
| Assumption 1 | "The thrust at the crown is horizontal and passes through the upper ⅓ point of the arch." | Verified |
| Assumption 2 | "The reaction passes through the lower ⅓ point of the arch at the skewback." | Verified |
| Assumption 3 | "The equilibrium polygon lies completely within the middle ⅓ of the arch." | Verified |
| Failure modes | "(a) by rotation of one section of the arch about the edge of a joint; (b) by the sliding of one section of the arch on another or on the skewback; (c) by crushing of the masonry." The middle-third assumption "precludes the rotation ... or the development of tensile stresses in either the intrados or extrados." | Verified (rendered page) |
| Loads | wall above an opening taken as a 45° triangle (height ½ span), "equivalent to a uniformly distributed load of 1⅓ times the triangular load". "Heavy concentrated loads should not be allowed to bear directly on minor arches. This is especially true of jack arches." Minor concentrated loads: a uniform load of twice the concentrated load | Verified |

Lever arm **(derived)**: the crown thrust acts at 2d/3 above the soffit and the springing reaction
at d/3, so the couple arm is z = d/3. With the simple-span moment WS/8, H = (WS/8)/(d/3) = 3WS/8d,
which is equation (6) below; with WS/6 for a triangular load it gives equation (7). The two
printed equations therefore confirm the d/3 lever arm.

### 2.2 Equations (jack arch)

W = total load (lb), S = clear span (in), d = depth (in), b = breadth (in), per [F2].

| Eq. | Rule | Mark |
|---|---|---|
| (6) | uniform load over the full span: **H = 3WS / 8d** | Verified (rendered page) |
| (7) | triangular load over the full span: **H = WS / 2d** | Verified (rendered page) |
| (8) | maximum compressive stress: **fm = 2H / bd**. "This value is twice an axial compressive stress on the arch, due to a load H, because the horizontal thrust is located at the third point of the arch depth." | Verified (rendered page) |
| Skewback rule | "The common rule for jack arches is to provide a skewback (K, measured horizontally) of ½ in. per ft of span for each 4 in. of arch depth." | Verified (rendered page) |
| (4) | skewback angle from the vertical for that rule: γ = tan⁻¹ (S/8). Dimensionally S is in feet here (K/d = ½ × S/4 per ft) **(derived reading)** | Verified (rendered page) |
| Usual sizes | "Jack arches are commonly constructed in depths of 8 and 12 in. with a camber of ⅛ in. per ft of span." | Verified (rendered page) |
| Sliding | "The coefficient of friction between the units composing a brick or tile masonry arch is at least 0.60 ... This corresponds to an angle of friction of approximately 31 deg." The arch is stable against sliding if the angle the line of resistance makes with the normal to the joint is less than the angle of friction | Verified (rendered page) |
| (1) | printed as "β = tan⁻¹ (W/2H − γ)", W = total equivalent uniform load, H = crown thrust, γ = angle of the joint with the vertical. The bracket mixes a ratio and an angle; the reading that works is β = tan⁻¹(W/2H) − γ **(reading, not printed)** | Verified (rendered page) |
| Abutment | resistance to thrust from the adjacent masonry, H_r = v_m n x t (11), with allowable shear 50 psi (Type M or S mortar) or 40 psi (Type N). The definitions of n, x and t are in lines cropped from the scan | Verified (rendered page), terms **NOT FOUND** |
| Allowable compression | BIA Table 1 is for clay building brick of 2,000–14,000 psi unit strength (200–1,150 psi allowable). It does not cover IFB | Verified (rendered page) |

Segmental arches (TN 31A Fig. 3, thrust coefficients H/W by S/r and S/d) were not transcribed.

### 2.3 Depth rules

| Source | Rule | Mark |
|---|---|---|
| BIA TN 31 (1995) | "For jack arches, the arch depth should equal or exceed 4 in. (100 mm) plus 1 in. (25 mm) for every foot (300 mm) of arch span or 8 in. (200 mm), whichever is greater." This is given "To provide proper visual balance and scale ... Because aesthetics of an arch are subjective, there are no hard rules for this." **It is an appearance rule, not a structural one.** "For structural arches, a minimum arch depth is determined from the structural requirements." | Verified [F1] |
| BIA TN 31A | common depths 8 and 12 in (above) | Verified [F2] |
| HarbisonWalker | for sprung arches: "Assuming that the absolute lower limit for the rise of the line of thrust is 1/4 inch (1/48) per foot of span" (already in `kiln-hardware.md` §4.3) | Verified [F3] |
| Structural minimum depth for a flat kiln roof | **NOT FOUND** | |

The BIA appearance rule would demand 8 in for every span up to 4 ft. Working kiln lids are 3 in
thick over 28–45 in spans (§4.1). The engine must not use it as a structural limit.

Candidate check **(derived; combines two sources, not a sourced rule)**: if the thrust line of a
flat roof must rise at least S/48 (HarbisonWalker's lower limit for sprung arches) and its rise is
the BIA couple arm d/3, then d ≥ S/16. With Heyman's minimum-thrust state (rise = d) it is
d ≥ S/48. Every flat precedent in §4 passes d ≥ S/16 (L&L T3400 long side 45/16 = 2.8 in < 3 in
is the tightest), so it does not separate good roofs from bad ones.

### 2.4 Worked numbers for kiln roofs (all derived)

Self-weight only, per inch of roof breadth. With W = ρ b d S, equation (6) gives
**H/b = (3/8) ρ S²**, independent of depth, and (8) gives **fm = (3/4) ρ S² / d**. The minimum
thrust with the thrust line using the whole depth (rise = d) is one third of that, (1/8) ρ S².
Densities and crushing strengths from §5 (K23 32.0 pcf, CCS 145 psi; BNZ PA-23 44 pcf, CCS
140 psi). ρ in lb/in³ = pcf ÷ 1728.

| Material | Span S | H/b (lb per in of roof) | fm at d = 3 in | fm at d = 4.5 in | fm at d = 9 in | CCS ÷ fm (d = 4.5 in) |
|---|---|---|---|---|---|---|
| K23 | 12 in | 1.0 (12 lb/ft) | 0.67 psi | 0.44 psi | 0.22 psi | 326 |
| K23 | 24 in | 4.0 (48 lb/ft) | 2.7 | 1.8 | 0.9 | 82 |
| K23 | 36 in | 9.0 (108 lb/ft) | 6.0 | 4.0 | 2.0 | 36 |
| K23 | 48 in | 16.0 (192 lb/ft) | 10.7 | 7.1 | 3.6 | 20 |
| PA-23 | 36 in | 12.4 (149 lb/ft) | 8.3 | 5.5 | 2.8 | 25 |
| PA-23 | 48 in | 22.0 (264 lb/ft) | 14.7 | 9.8 | 4.9 | 14 |
| Kast-O-Lite 30 LI Plus (92 pcf fired, CCS 2,300 psi after 1500 °F) | 36 in | 25.9 (311 lb/ft) | 17.3 | 11.5 | 5.8 | 200 |

- Crushing under self-weight is not what limits a 1–4 ft flat roof: the cold stress is one
  fourteenth or less of the published crushing strength. Superimposed load (insulation, a stack
  on the roof) adds to W in proportion.
- The same expression, (3/4) ρ S²/d, is the bending stress of a monolithic slab of that depth
  (M = wS²/8, section modulus bd²/6). A cemented 3 in K23 lid over 28 in reaches 3.6 psi against
  a MOR of 114.5 psi. So cold self-weight bending is not the limit either; joints, heat and loss of
  clamp are (§3, §6).
- Sliding at a vertical end joint (γ = 0, a roof squeezed against a frame rather than bearing on a
  skewback): W/2H = 4d/3S. With BIA's μ = 0.60 the roof is safe if S/d > 2.2. S = 36, d = 9:
  angle 18.4° < 31°. S = 12, d = 9: 45°, fails unless the clamp exceeds the middle-third thrust.
  The friction coefficient of IFB on IFB or on steel is **NOT FOUND**; 0.60 is BIA's figure for
  clay brick masonry.
- BIA skewback rule at kiln sizes: γ = 14.0° at 2 ft, 20.6° at 3 ft, 26.6° at 4 ft; K = 1.1 in
  (2 ft) to 2.25 in (4 ft) for a 4.5 in deep roof, 2.25–4.5 in for 9 in.
- HarbisonWalker's sprung-arch constants (`kiln-hardware.md` §4.3) assume the thrust line runs
  through mid-thickness at crown and skewback. For a flat roof that line has zero rise, so the
  tables cannot be used; use the BIA equations.

### 2.5 Limits of the method (ADR 0009)

- Cold masonry of clay building brick in mortar, uniform or triangular load, one-way span between
  abutments that do not move. No heat, no prestress, no two-way (four-sided) support.
- Minor arches only: span ≤ 6 ft, rise/span ≤ 0.15 [F2]. Kiln spans of 1–4 ft fall inside.
- μ = 0.60 is for brick; IFB **NOT FOUND**. Allowable compressive stress for IFB **NOT FOUND**
  (only crushing strengths, §5).
- Thrust in a flat roof that is heated while held by a rigid frame: **NOT FOUND**. The failure
  record (§4.3, Finkelnburg) shows it can far exceed the cold value.

---

## 3. The band, frame or rods

### 3.1 Clamping force

| Kiln / source | What holds the roof | Force or torque | Mark | Source |
|---|---|---|---|---|
| Nils Lou, Minnesota Flat Top (MFT) | corner braces "made from pairs of 9" long 3" by 3" angles welded edge to edge making a "W" shape. Double tie rods hold it all together." The frame ("cage") "is constructed with 2" angle and 1/2" threaded rod." "The hard-bricks at each corner are designed to absorb the compression of the tie-rods at the corners and distribute it to the IFB's." | "The nuts should be tightened quite tightly. If you have access to a torsion wrench the amount of tightening should equal 40 foot/lbs of torque." "After the first firing the tie-rods may have stretched. Re-tighten all the nuts to 40 foot/lbs. Repeat after several more firings" | Excerpt | [F8] |
| Merrill flat top | 3/8 in threaded rod through every brick of a row, wing nuts and 2 in fender washers; rows drawn together with mechanic's wire round the rod ends; some bricks wired up to the angle (§4.3) | "The wing nuts can be tightened with your pliers." No torque | Verified | [F9] |
| SECEM tunnel-kiln patent | "a resilient lateral compression thrust ... by means of springs or equivalent resilient means", springs outside the steel casing; "This thus achieves a flat roof structure which does away with the need for suspension means" | "the value of this force being predetermined and constant"; set by nuts. No number | Verified | [F30] |
| Electric top-loader lids (L&L, Skutt, Olympic, Paragon) | stainless band with worm-drive or hose clamps (`electric-kiln-hardware.md` §1.1) | **NOT FOUND**. No maker states band tension or torque | | |

MFT clamp **(derived)**. Fastenal: "Torque values calculated from formula T=KDF", with "K = 0.20
for plain and dry conditions", K = 0.17 zinc plated and dry, K = 0.15 lubricated, D = nominal
diameter, F = clamp load [F31] Verified. Fastenal also warns "Torque is only an indirect
indication of tension."
- Assuming ½ in rods (the cage's stated size; the snippets do not tie the size to the roof rods
  explicitly): F = 40 × 12 ÷ (0.20 × 0.5) = **4,800 lb per rod** (6,400 lb at K = 0.15).
- On the ½-13 stress area 0.1419 in² that is 33.8 ksi, close to 36 ksi yield. Fastenal's own A307
  table loads ½-13 to 3,831 lb ("75% of 36,000 PSI"), which is 32 ft·lb at K = 0.20. Nils Lou's
  40 ft·lb is above that, which fits his note that the rods stretch.
- For scale: the BIA middle-third self-weight thrust of a 9 in K23 roof over about 45 in (the
  MFT span, itself derived in §4.3) is 14.1 lb/in × 62.5 in = 879 lb per direction. Two rods per
  side at 4,800 lb (two per side is inferred from "lower front tie-rod" and "top front tie-rod")
  give about 11 times that, a mean prestress of 17 psi over the 9 × 62.5 in edge (K23 CCS 145 psi).
  The clamp is set far above what self-weight needs; no source says why. A likely reason is to
  keep the joints shut after shrinkage, but that is unconfirmed.

### 3.2 Keeping the clamp: re-tightening and springs

| Source | Statement | Mark |
|---|---|---|
| L&L | "The brick will shrink slightly over time. This is more pronounced when using the kiln at higher temperatures like cone 10." "If the bricks shrink too much they will become loose." Bands around the top and bottom can be tightened too: "This will help maintain the integrity of those slabs even if there is a crack." "The stainless steel clips we use in our lids also help keep these natural cracks from normally becoming a problem in the lids." [F18] | Verified |
| L&L | "The geometry of the kiln and the tightness of the stainless steel bands are what holds everything together, whether the brick is in a few pieces or all one piece should not matter a whole lot". Hot brick expanding against the cooler band closes cracks [F19] | Verified |
| Skutt | "Remember to tighten the lid band and lid hardware on a regular basis." [F24] | Verified |
| Olympic | "Expansion and contraction of the kiln during firing will eventually cause the stainless steel jacket/rings to loosen"; clamps "on the jacket, lid and bottom of the kiln should be tightened occasionally with a screwdriver when the kiln is warm." [F25] | Verified |
| MFT | re-torque after the first firing and after several more (§3.1) [F8] | Excerpt |
| NWPG flat top (Finkelnburg) | "Regular tightening of the rods that hold the bricks in place" keeps them in compression; but heating with "no room for the expanding insulating bricks to grow" crushes them a little each firing (§4.3) [F10] | Verified |
| SECEM patent | constant spring force instead of fixed rods [F30] | Verified |
| HarbisonWalker | tie rods "in some cases" spring-loaded or manually adjusted (already in `kiln-hardware.md` §4.2) [F3] | Verified |

### 3.3 Band sizes, cement, and the door edge

| Item | Value | Mark | Source |
|---|---|---|---|
| Stainless band thickness and width on L&L, Skutt, Paragon lids | **NOT FOUND** (replacement-band listings give part numbers only). Same gap as `electric-kiln-hardware.md` §1.1 | | |
| Lid thickness, top-loaders | replacement lids for L&L 8- and 10-sided and Skutt 10-sided kilns come in 2½ or 3 in brick, with band (and, for L&L, angle clips and handle) | (secondary) Excerpt | [F35] |
| L&L, cement | "the cement we normally use for cementing our firebrick" (distinguished from its phosphate repair cement) [F18]; custom polygons: brick "usually cemented in sections and then held together with a stainless-steel band" [F22] | Verified | |
| L&L DaVinci | "LID BRICK IS SECURED WITH CLIPS"; stainless worm-gear case clamps, "Two on the top and bottom" [F19] | Verified | |
| Skutt, lid | "Skutt lids are coated with a refractory cement which helps protect the kiln chamber from falling brick particles." Hairline cracks in the coating are normal; a worn lid can be flipped [F24] | Verified | |
| Olympic | studio line: "the bricks are held together by compression of the stainless steel jacket. The wall bricks are not cemented together"; top and bottom are "slabs" with a thin high-temperature coating. "Olympic Large Capacity electric kiln bricks are mortared together" [F25] | Verified | |
| Forum (top-loaders) | "the lid bricks are cemented and held together with a tension band around the outside edge" | (secondary) Excerpt | [F34] |
| MFT roof | "All bricks not setting on the walls will be dipped in mortar. The mortar is made of an equal mixture of fireclay and common sand plus water." Afterwards "the roof is a slightly domed, monolithic slab. The remaining mortar/slip is then poured over the top" | Excerpt | [F8] |
| NWPG roof | "a thin coat of refractory mortar and the compression of threaded rods" | Verified | [F10] |
| Bailey (against mortar) | "Typical mortared wall construction reduces the utility life of a kiln. Once a kiln is mortared as a continuous brick structure, large cracks will result from the expansion and contraction from each firing." Bailey dry-stacks with stainless "L" anchors instead | Verified | [F28] |
| Front-loader roof at the door edge (frame angle, case lip) | **NOT FOUND** for a flat roof. L&L front-loaders use a 4½ in arch in a welded case ([S6] in `electric-kiln-hardware.md`); L&L: "Arched roofs are the time-proven way to build a long-lasting front-loading kiln" [F21] | Verified (arch) | |

---

## 4. Precedent

Note on support: a top-loader lid sits on walls on all four sides (two-way support). A roof over a
full-height door has one free edge when the door is open, so it must span one way between the
other walls or be carried by steel at the door edge. Top-loader lids are therefore evidence for
banded flat slabs, not directly for flat roofs over doors.

### 4.1 Electric top-loader lids (flat, banded)

| Kiln | Inside | Lid | Mark | Source |
|---|---|---|---|---|
| L&L e28T-3 | "28" Diam x 27" High", 10.2 ft³ | "Brick Thickness: 3" Brick" (walls and lid) | Verified | [F20] |
| L&L DaVinci X2300 | "Approximately 22" wide by 22" deep" | "3" K23 firebrick for all models"; lid brick secured with clips; stainless bands | Verified | [F19] |
| L&L DaVinci X2800 | approx. 27 × 27 in | same | Verified | [F19] |
| L&L DaVinci X3200 | approx. 32 × 32 in | same; optional fibre top (below) | Verified | [F19] |
| L&L DaVinci T2300 | approx. 36 × 28 in | same | Verified | [F19] |
| L&L DaVinci T3400 | approx. 45 × 34 in (hearth 42 × 28), 18–45 in high | standard firebrick lid; "All but the T3400 DaVinci lids can easily be lifted by one person. T3400 models need two persons to lift." [F21] | Verified | [F19] [F21] |
| L&L optional fibre top | "These are ideal for T3400 kilns and X3200 kilns used for tough industrial applications. The lid firebrick is replaced with ceramic fiber modules." 4 in modules bolted to the lid's metal frame; "These lids will never crack or spall" | | Verified | [F19] |
| L&L custom polygons, 38–48 in diameter | "The top is typically made of 4" thick folded and formed ceramic fiber modules." Same for custom DaVinci kilns | | Verified | [F22] |
| Skutt KM-1627 (oval) | "Approximately 46 in. x 31 in. opening and 27 in. high", 18.5 ft³, 3 in brick | fibre lid: "replace the traditional brick lid with an Engineered fiber lid". "Big lids and slabs want to bend like a potato chip during the firing." "This is caused by the surfaces on the inside of the kiln expanding greater than those on the outside." | Verified | [F23] |
| Olympic Large Capacity top-loaders | "The lids of the top loading models are comprised of pyro-brick modules" (what "pyro-brick modules" are is not stated in the text seen) | | Excerpt | [F26] |
| Olsen (1973) | "Arches really have no other function than to span and cover the top in most electric kilns, thus flat roofs are used. (Fig. 13). Flat roofs simplify construction and cut costs." "An angle iron frame is the basic frame used in electric kiln construction." | | Excerpt | [F7] |

Pattern: 3 in K23 lids in steel bands are the standard up to about 32 × 32 and 45 × 34 in (L&L).
At the large end makers offer or switch to fibre: Skutt at 46 × 31 in, L&L for heavy use of the
T3400 and X3200 and for all custom tops of 38 in and up.

### 4.2 Electric and gas front-loaders

| Kiln | Inside W × D × H | Roof | Mark | Source |
|---|---|---|---|---|
| L&L Easy-Load (EL2436–EL3048) | see `electric-kiln-hardware.md` | 4½ in K25 arch; "4-1/2" STRONG FIREBRICK ARCH IS BUILT THE OLD-FASHIONED WAY. Arched roofs are the time-proven way to build a long-lasting front-loading kiln" | Verified | [F21], [S6] there |
| L&L eFL | eFL1626: 17 in wide (bulletin) | "arched sides and top for strength" | Verified | [S1] in `electric-kiln-hardware.md` |
| Paragon Dragon 24 | "24" wide x 24" deep x 27" high"; 900+ lb | "4" of insulation throughout the walls, door, and lid, made from 3" of firebrick backed by 1" of ceramic fiber block". Flat or arched: **NOT FOUND** | Verified | [F27] |
| Olympic FL12E, FL20E | 24 × 24 × 36 in; 28 × 28 × 45 in | "welded heavy angle iron frame"; walls "4 1/2" insulating brick with 1" ceramic fiberboard and 1" air space created by the tube frame"; front-loading doors "backed with 1" x 1" steel tubing". Roof shape: **NOT FOUND** | Excerpt (secondary for the frame) | [F26] |
| Bailey Studio Deluxe gas front-loaders | 27 × 22.5 × 38.5 to 31.5 × 36 × 41.5 in | "4½" of insulating firebrick in the walls, floor and arch"; Production models 6¾ in arch | Verified | [F28] |
| Nabertherm N 100 – N 660 (front-loading chamber kilns) | 400–600 mm wide (400 × 530 × 460 to 600 × 1100 × 1000 mm) | maker page silent on roof; a retailer says "Rugged, self-supporting, vaulted arch construction" | Verified (sizes); (secondary) Excerpt (arch) | [F29] |
| Forum, unnamed region | "all bigger (>100 l) kilns I have seen around here are front loaded box kilns with flat roof" | | (secondary) Excerpt | [F33] |

No maker document read here describes an electric front-loader with a flat brick roof. The two
makers whose front-loader roofs could be read (L&L, Bailey) use arches.

### 4.3 Flat-top gas kilns

| Kiln | Span and depth | Construction | Mark | Source |
|---|---|---|---|---|
| Merrill flat top (CM, Apr 2023) | interior "54 inches wide and 36 inches deep"; outside "8 bricks wide (72 inches) and 6 bricks deep (54 inches)" | "straight K insulating brick" "standing vertically"; 12 rows; 3/8 in rod through each brick, hole "2 1/2 inches from the top edge and 2 1/4 inches from the sides", bit ⅛ in oversize; 2 × 2 × 3/16 × 72 in angle "placed across the top of each row"; 16 ga nichrome wire through grooves from "a brick with wire every three to five bricks and including one in the center" up over the angle; ⅛ in Fiberfrax on the wall tops. Mortar not mentioned. Advantage (search snippet only, Excerpt): "each part of the roof can be handled by two people" | Verified | [F9] |
| Merrill, geometry **(derived)** | rows span the 36 in depth one way; roof about 9 in deep | rods 58 in = the 54 in outside depth + 4 in, so rows run front to back over the 9 in front and back walls. 12 rows × 4½ in = 54 in, the interior width. The 72 in angles equal 54 in + two 9 in side walls, so they rest on the side walls across the rows. Bricks standing on end, so 9 in deep, if standard 9 × 4½ × 2½ in. The roof is part flat arch (rod compression over 36 in) and part suspended (wires to the angles) | Derived | |
| Nils Lou, Minnesota Flat Top (MFT), *The Art of Firing* (1998) | 9 in thick ("Within the nine inch thickness ..."); "fourteen courses of twenty-five soldiered bricks"; 338 IFB + 12 hard bricks "three for each corner" | built on "a flat piece of plywood supported with 2 by 4's. Eliminated is the arch form, the side skews, arch bricks"; spanning bricks dipped in fireclay–sand mortar; before final tightening "jack up the roof about 3/4" so there is a visual doming effect"; W-shaped corner braces and double tie rods; 40 ft·lb, re-torqued (§3.1). "By engineering the proper compression completely around the roof so that there is no possible movement horizontally the roof must remain in place and cannot collapse." "Properly constructed, the flat roof is in reality a flattened dome." Stacking area "for four stacks of 12" by 24" shelves". Olsen: the MFT "became well known" | Excerpt | [F8] [F7] |
| MFT, span **(derived; assumes the roof is flush with 9 in walls on all four sides)** | roof plan 25 × 2½ = 62.5 in by 14 × 4½ = 63 in; clear span about 44.5 × 45 in, two-way | Nils Lou's ¾ in dome over about 45 in is 0.2 in/ft, against BIA's usual camber of ⅛ in/ft | Derived | |
| NWPG flat-top car kiln, Portland (Finkelnburg, CM Oct 2018) | span **NOT FOUND** | "insulating fire bricks placed on end on a flat form", "a thin coat of refractory mortar and the compression of threaded rods". Fired "to cone 10 in reduction at least 25 times a year". Failure: "During each kiln firing, the bricks expand with the heat increase, but there is no room for the expanding insulating bricks to grow." "Instead, they are compressed against each other until some small amount of crushing of the bricks occurs." "Eventually, brick crumbs begin falling from the roof, cracks form, and finally the roof itself begins to fail." "Finally, some whole bricks fell out of the roof onto the top kiln shelf." Replaced with 8 in MZR fibre blocks on 3/8 in stainless studs; no headroom for an arch | Verified | [F10] |
| Same article, arch against flat | "An arched roof can grow upward to relieve most of the effect of thermal expansion." "However, the arch requires more material than a flat top and is more time-consuming to build." "To utilize a sprung arch roof requires lateral support for both side walls of the kiln, support that is unnecessary with a flat-top design." The flat top still needs its own rods; they close on themselves instead of pushing on the walls | Verified | [F10] |
| Rhodes, *Kilns* (1968), p. 114 | no span | "Insulating bricks are so light they can be suspended to form flat roofs. Figure 110 shows a roof made of insulating brick which have been drilled and hung on steel rods. The rods are threaded and bolted to exert inward pressure against angle irons which hold the mass of brick together. This style of roof may be used instead of the harder-to-build arch. It is supported by the walls and can be easily removed for repair. Small flat roofs can be made by clamping together a number of insulating brick with the tightened steel strap used for reinforcing shipping cartons. Brick held together this way, however, have a tendency to become loose. The suspended roof may seem like a simple solution. But in use the suspended bricks tend to break off and drop downward into the kiln. The arch structure is actually much more durable." | Excerpt | [F6] |
| Olsen, *The Kiln Book*, 3rd ed. (2001) | no span | "A special independent frame for the flat roof must be constructed and designed to be either bolted or welded together. In some designs rod holes are drilled through each row of bricks across the span and bolted to the outside perimeter frame. In other designs the corner bolts are cinched down from both directions, putting the spanning bricks in compression. Normal wear and tear of expansion and contraction can grind the bricks down and make them loose. Thus, they require constant surveillance." | Excerpt | [F7] |

### 4.4 Industrial flat roofs

| Source | Statement | Mark |
|---|---|---|
| BNZ, BB-Blok (1998), flat suspended IFB roofs | "A flat suspended arch made of IFB has been an accepted method of kiln roof design in the ceramic industry for many years." "A general rule worth following is to limit the use of the suspended roof design to applications where the temperature will not exceed 1345°C (2450°F). Above this temperature, the better solution is to utilize a sprung arch construction. IFB exposed to higher temperatures is limited in its ability to resist forces of traction. This applies to even the highest IFB grades." Stainless (AISI 321) hangers kept below 750 °C. "Care must be taken to not limit the ability of the brick modules to move slightly during heat-up, as pinch spalling can result." Commonest failure: "a single block spalling and dropping out of the roof" [F15] | Verified |
| SECEM patent (tunnel kilns 40–60 m long) | "the roof (1) is flat and is composed of bricks (4) placed side-by-side", "which may be joined together with mortar", held by springs (§3.1). Narrow notches (about 10 mm) 0.20–0.50 m apart, "at most one third of the height of the bricks", give "an arcuate orientation of prestressing forces". Prior art criticised: arches give "considerable lateral thrust forces which must be supported by the side walls". Span not given [F30] | Verified |

### 4.5 Stated maximum span for a flat IFB roof

**NOT FOUND** in BIA, HarbisonWalker, BNZ, Morgan, Rhodes, Olsen, Nils Lou, Merrill or
Finkelnburg. The only span limits found are BIA's 6 ft scope for minor (building) arches [F2] and
makers' choices (§4.1).

---

## 5. Strength of roof materials

### 5.1 Insulating firebrick

ASTM C133 for MOR and CCS, C134 density. All Verified from the data sheets.

| Grade | Class temp | Density | MOR | CCS | Reversible thermal expansion, max | Linear change, 24 h soak | Source |
|---|---|---|---|---|---|---|---|
| Morgan K23 | 1315 °C (2400 °F) | 513 kg/m³ (32.0 pcf) | 0.79 MPa (114.5 psi) | 1 MPa (145 psi) | 0.7 % | −0.1 % at 1230 °C | [F11] |
| Morgan K25 | 1370 °C (2500 °F) | 617 (38.5 pcf) | 0.95 (137.7) | 1.3 (188.5) | 0.8 % | −0.3 % at 1350 °C | [F11] |
| Morgan K26 | 1430 °C (2600 °F) | 657 (41 pcf) | 0.9 (130.5) | 1.3 (188.5) | 0.8 % | −1.00 % at 1400 °C | [F11] |
| Morgan JM23 | 1260 °C (2300 °F) | 480 (30.0 pcf) | 1 (145) | 1 (145) | 0.5 % | −0.4 % at 1230 °C | [F12] |
| Morgan JM26 | 1430 °C (2600 °F) | 800 (49.9 pcf) | 1.5 (217.5) | 1.6 (232) | 0.5 % | −0.2 % at 1400 °C | [F12] |
| Morgan JM26HD | 1400 °C (2600 °F) | 920 (57.4 pcf) | 2.2 (319) | 3.5 (507.5) | – | −0.3 % at 1400 °C | [F12] |
| Morgan JM28 | 1540 °C (2800 °F) | 890 (55.5 pcf) | 1.8 (261) | 2.1 (304.5) | 0.6 % | −0.4 % at 1510 °C | [F12] |
| Morgan JM30 | 1650 °C (3000 °F) | 1020 (63.6 pcf) | 2 (290) | 2.3 (333.5) | 0.6 % | −0.6 % at 1620 °C | [F12] |
| Morgan TJM 23 | 1260 °C (2300 °F) | 530 (33.1 pcf) | 0.7 (101.5) | 1.0 (145) | 0.6 % | −0.2 % at 1230 °C | [F13] |
| Morgan TJM 26 | 1430 °C (2600 °F) | 800 (49.9 pcf) | 1.5 (217.5) | 2.0 (290) | 0.7 % | −0.5 % at 1400 °C | [F13] |
| Morgan TJM 28 | 1540 °C (2800 °F) | 900 (56.2 pcf) | 1.8 (261) | 2.5 (362.5) | 0.8 % | −0.5 % at 1510 °C | [F13] |
| Morgan TJM 30 | 1650 °C (3000 °F) | 1000 (62.4 pcf) | 2.0 (290) | 3.0 (435) | 0.9 % | −1.0 % at 1570 °C | [F13] |
| BNZ PA-20 | 2000 °F use limit | 39 pcf (625) | 85 psi | 95 psi | see note | −0.0 % at 2250 °F | [F14] |
| BNZ PA-23 | 2300 °F | 44 pcf (705) | 115 | 140 | see note | −0.0 % at 2250 °F | [F14] |
| BNZ PA-26 | 2600 °F | 49 pcf (785) | 180 | 240 | see note | −0.1 % at 2550 °F | [F14] |

- Morgan K-20 and K-28: **NOT FOUND**. The current K sheet (BR.02, 1 Jan 2025) lists only K23,
  K25, K26 and Insalcor. K23's 32.0 pcf matches `electric-and-thermal.md` §4.1.
- TJM columns were matched by position in a ten-column table (TJM 23 is column 1, TJM 26 column 7,
  TJM 28 column 9, TJM 30 column 10); check against the sheet before use.
- BNZ hot load (ASTM C16, "10 psi load for 1½ hours"): PA-20 and PA-23 −0.5 % at 2000 °F; PA-26
  −0.2 % at 2200 °F [F14]. This is the only hot strength figure found. Morgan claims "High hot
  compressive strength" with no number: **NOT FOUND**.
- BNZ reversible thermal expansion "at 2000°F (1093°C)" is printed ".06 .06 0.6" for PA-20/23/26.
  The first two are probably 0.6 % mis-set; not confirmed.
- The temperature at which Morgan's "Reversible Linear Thermal Expansion, max. %" applies is not
  stated. Over 36 in, 0.7 % is 0.25 in **(derived)**; that is the order of movement a rigid frame
  has to absorb, or the brick has to crush.

### 5.2 Castables

Verified from HWI product data sheets. MOR and CCS in psi.

| Product | After 220 °F | After 1500 °F | After 2000 °F | After 2500 °F | After 2900–2910 °F | Other | Source |
|---|---|---|---|---|---|---|---|
| Kast-O-Lite 30 LI Plus (10/19: 5874), MOR | 600 | 300 | 300 | 900 | 800 (2910 °F) | 3000 °F max; 92 lb/ft³ required; bulk density 98 (220 °F), 92 (1500 °F) pcf; permanent linear change none, 0 to −0.3, −0.2, +2.0, +1.0 % | [F16] Verified (rendered page) |
| Kast-O-Lite 30 LI Plus, CCS | 2,700 | 2,300 | 1,300 | 2,000 | 1,800 | water 17.0 % by weight | [F16] |
| Mizzou Castable Plus (12/12: 5976), MOR | 1,100 | 800 | 600 | 1,100 | – | 3000 °F max; 140 lb/ft³ required; bulk density 142 (220 °F), 140 (1500 °F) pcf; permanent linear change −0.1, −0.2, −0.2, +0.9, +2.8 % (2900 °F) | [F17] Verified |
| Mizzou Castable Plus, CCS | 5,500 | 3,500 | 3,000 | 4,000 | – | water 8.6 % (vibration), 9.0 % (hand) | [F17] |

These sharpen `combustion-and-masonry.md` §6.1, which had the Kast-O-Lite MOR only from snippets
and no CCS. Hot (in-service) strength of either castable: **NOT FOUND**.

---

## 6. What an engine could enforce, and how sure each rule is

| # | Rule | Formula | Basis | Confidence |
|---|---|---|---|---|
| R1 | Thrust the band or frame must supply (cold) | H = 3WS/8d (uniform), WS/2d (triangular); self-weight H/b = (3/8)ρS² | BIA TN 31A [F2] | High as cold statics; ignores heat and prestress |
| R2 | Thrust line within the middle third | equilibrium polygon in the middle ⅓ (lever arm d/3) | BIA [F2]; HarbisonWalker "The line of thrust in a cold arch should lie within the middle third of the brick" [F3] | High (two sources agree) |
| R3 | Crushing | fm = 2H/bd ≤ allowable | BIA [F2]; IFB allowable **NOT FOUND**, only CCS (§5) | Formula high; never governs at 1–4 ft (§2.4) |
| R4 | Sliding at the end joints | tan⁻¹(W/2H) − γ < friction angle (31° at μ = 0.60); vertical ends (γ = 0): S/d > 2.2 at the R1 thrust | BIA [F2]; IFB friction **NOT FOUND** | Medium |
| R5 | Binding stress | ≤ 12,000 psi in hot steel | HarbisonWalker, `kiln-hardware.md` §4.7.4 | As there |
| R6 | Minimum depth | no sourced structural rule. Candidate d ≥ S/16 (derived, §2.3); BIA's ≥ 8 in rule is about appearance and contradicts working lids | | Low |
| R7 | Temperature | suspended flat IFB roofs ≤ 2450 °F, else sprung arch | BNZ [F15] | Sourced for suspended roofs only, not for rod-compressed ones |
| R8 | Keep the clamp | re-tighten after the first firing and periodically, or use springs | L&L, Skutt, Olympic, Nils Lou, Finkelnburg, SECEM | High as practice; the only number is MFT 40 ft·lb on ½ in rod (≈ 4,800 lb, derived) |
| R9 | Precedent envelope (pass) | banded 3 in K23 slabs to about 32 × 32 and 45 × 34 in on four-sided support (L&L); rod-compressed 9 in IFB one way over 36 in (Merrill, with hangers); about 45 in two-way, 9 in, mortared, domed, tie-rodded (MFT, span derived) | §4 | Medium: single kilns or one maker each |
| R10 | Refuse or warn | flat brick roof over a full-height door: no maker precedent read; L&L and Bailey arch their front-loaders. Large lids: Skutt replaced brick with fibre at 46 × 31 in; L&L offers fibre for the T3400 and X3200 and uses it on all 38 in+ custom tops | §4.1–4.2 | Medium |

Spreading sensitivity **(derived from statics; the model is mine, no source)**: treat the roof as
two rigid halves hinged at the bottom of each end and the top at midspan, lever arm z = d. If
the abutments spread by δ in total (frame stretch, or brick shortened by crushing and creep), the
arm becomes z' ≈ √(d² − Sδ/2) and the thrust rises as H = WS/8z'. The arm reaches zero at
δ ≈ 2d²/S: 0.64 in for a 3 in roof over 28 in, 1.1 in for 4.5 in over 36 in, 4.5 in for 9 in over
36 in. Compare 0.17–0.38 in of reversible expansion over 24–48 in (§5.1). This shows why thin
flat roofs depend on the clamp being kept up, and why depth helps quickly (δ grows with d²). It
is an explanation, not a sourced rule.

---

## 7. Where the sources agree or disagree with the owner's statement

The owner: for spans of 1 to 3 or 4 ft the standard is a flat roof with a steel band or frame
that keeps the bricks squeezed, in addition to mortar; light IFB matters; and electric
front-loaders (flat roof in a welded case, whole front a hinged door) are normal and successful.

Supports it:
- Banded flat lids are the standard on electric top-loaders: 3 in brick at 28 in diameter
  (L&L e28T-3), and 3 in K23 up to about 45 × 34 in (L&L DaVinci T3400) [F19] [F20]. Olsen: "flat
  roofs are used" in most electric kilns [F7].
- Rod-compressed flat IFB roofs work on gas kilns at about 3 ft (Merrill, 36 in) and probably
  about 3¾ ft (MFT, derived 45 in, 9 in thick, mortared) [F8] [F9]. Finkelnburg: the flat-top
  design "has been around for decades" [F10].
- Mortar plus clamp: L&L cements lid and section brick and bands it; Skutt cement-coats lids; the
  MFT is mortared; Olympic's large kilns are mortared [F18] [F22] [F24] [F25] [F8].
- Light material matters: self-weight thrust and stress scale with density (§2.4); Rhodes:
  "Insulating bricks are so light they can be suspended to form flat roofs" [F6].

Contradicts or qualifies it:
- **Front-loaders**: no maker document read shows a flat-roofed electric front-loader. L&L
  arches both its front-loader lines and says "Arched roofs are the time-proven way to build a
  long-lasting front-loading kiln" [F21]; Bailey's gas front-loaders are arched [F28]. Paragon's
  Dragon (24 in wide) and Olympic's FL (24–28 in wide) roof shapes were not found. Only a
  forum post reports flat-roofed front-loaders as common [F33].
- **Durability**: Rhodes says banded or rod-hung IFB roofs "have a tendency to become loose" and
  "The arch structure is actually much more durable" [F6]; Olsen says flat roofs "require constant
  surveillance" [F7]; a cone 10 rod-compressed flat top failed by progressive crushing [F10].
- **Large lids**: Skutt says "Big lids and slabs want to bend like a potato chip" and replaced the
  brick lid at 46 × 31 in [F23]; L&L offers fibre on its 32 in and 34 in spans for hard use [F19].
  So the 4 ft end of the owner's range is at or past where makers stop using brick.
- **Mortar**: Bailey argues the opposite, that mortared construction cracks and cannot be
  repaired [F28]; Merrill's roof uses no mortar [F9].
- **Temperature**: for suspended flat IFB roofs BNZ advises a sprung arch above 2450 °F [F15];
  cone 10 is under that.

---

## 8. Gaps (not found)

- A structural minimum depth or maximum span for a flat IFB kiln roof, from any source.
- Friction coefficient of IFB on IFB, on mortar, or on steel (BIA's 0.60 is for clay brick).
- Allowable compressive stress or safety factor for IFB; hot compressive strength of any Morgan
  grade; hot strength of Kast-O-Lite 30 LI Plus or Mizzou Castable Plus.
- Thermal stress or thrust in a flat roof heated while held by a rigid frame; how much
  abutment spread a flat roof tolerates (§6 gives an unsourced model only).
- Band tension, torque or clamp force for any electric kiln lid; stainless band thickness and
  width (L&L, Skutt, Paragon, Olympic).
- How a flat roof is held at the door edge of a front-loader (angle, case lip). Whether the
  Paragon Dragon or Olympic FL roofs are flat or arched.
- Morgan K-20 and K-28 data (not on the current K sheet).
- Span of the NWPG flat top; MFT clear span (derived only); number of Merrill's angles; MFT roof
  tie-rod diameter (½ in is the cage's stated size).
- The definitions of n, x and t in BIA's abutment formula (11) (cropped in the scan); the BIA
  TN 31A Fig. 3 thrust coefficients for segmental arches (not transcribed).
- Heyman's full chapter text (only the publisher's summary was read); Ochsendorf, "The masonry
  arch on spreading supports" (paywalled).
- Not relevant despite appearances: Fournier's *Electric Kiln Construction for Potters* (1977)
  rod-diameter-by-span table ("Up to 32/813 mm span rods should be 14 mm diameter ... Up to
  50/1270 mm span rods should be 18 mm diameter") is for silicon-carbide heating rods, not roof
  supports (Excerpt) [F32].

---

## Sources

- [F1] Brick Industry Association, *Technical Notes 31 – Brick Masonry Arches*, January 1995 (PDF, text layer). https://www.gobrick.com/media/file/31-brick-masonry-arches.pdf
- [F2] Brick Institute of America, *Technical Notes 31A – Structural Design of Brick Masonry Arches*, reissued July 1986 (first published October 1967). Scanned PDF; pages 2–8 read from rendered images. https://www.gobrick.com/media/file/31a-structural-design-of-brick-masonry-arches.pdf
- [F3] Harbison-Walker Refractories, *Brick Installation Guide*, © 2008 (same as [S20] in `kiln-hardware.md`; glossary p. 94; arch construction pp. 13–20). https://ssfbs.com/wp-content/uploads/2021/06/HW_Brick_Installation_Guide.pdf
- [F4] J. Heyman, *The Stone Skeleton: Structural Engineering of Masonry Architecture*, ch. 2 "Structural Theory of Masonry", pp. 11–24, Cambridge University Press (publisher's chapter summary only). https://www.cambridge.org/core/books/abs/stone-skeleton/structural-theory-of-masonry/2DF738498EAAF6BEA2B58C9DA6388DFF
- [F5] S. Fechino, "Jack Arches", *Masonry Magazine* (March 2021 by URL). Quotes: "Typically, the skewback is anywhere from 60 to 70 degrees"; the article's arch sits on a lintel, so it gives no structural span rule. https://masonrymagazine.com/blog/2021/03/31/jack-arches/
- [F6] D. Rhodes, *Kilns: Design, Construction, and Operation*, Chilton, 1968, p. 114 (index "Flat roofs, 114"). Archive full-text search snippets. https://archive.org/details/kilnsdesignconst00rhod ; https://archive.org/details/kilnsdesignconst0000rhod
- [F7] F. L. Olsen, *The Kiln Book* (1973; 2nd ed. 1983; 3rd ed. 2001). Archive full-text search snippets. https://archive.org/details/kilnbook0000unse ; https://archive.org/details/kilnbookmaterial00olse ; https://archive.org/details/kilnbook00fred
- [F8] N. Lou, *The Art of Firing*, A & C Black / Gentle Breeze, 1998, "The Minnesota Flat-Top Car Kiln: The Flat Roof" and construction chapters (index: flat roof 67, 68, 89; flattened dome 68; torque 95). Archive full-text search snippets. https://archive.org/details/artoffiring0000nils
- [F9] B. Merrill, "Tips and Tools: Flat-Top Kiln", *Ceramics Monthly*, April 2023 (same as [S16] in `kiln-hardware.md`). https://ceramicartsnetwork.org/ceramics-monthly/ceramics-monthly-article/tips-and-tools-flat-top-kiln
- [F10] D. Finkelnburg, "Techno File: Flat Top Roof Repair", *Ceramics Monthly*, October 2018 (Northwest Potters Guild kiln, report by B. Beattie). https://ceramicartsnetwork.org/ceramics-monthly/ceramics-monthly-article/Techno-File-Flat-Top-Roof-Repair
- [F11] Morgan Advanced Materials – Thermal Ceramics, *K Insulating Firebrick Series* product data sheet, code BR.02, 1 January 2025. https://www.morganthermalceramics.com/media/9429/k-ifb-series_eng.pdf
- [F12] Morgan Advanced Materials – Thermal Ceramics, *JM Insulating Firebrick Series*, code BR.05, 1 January 2025. https://www.murugappamorgan.com/media/9428/jm-ifb-series_eng.pdf
- [F13] Morgan Advanced Materials – Thermal Ceramics, *TJM Insulating Firebrick Series*, code BR.04, 1 January 2025. https://www.morganthermalceramics.com/media/9430/tjm-ifb-series_eng.pdf
- [F14] BNZ Materials, *PA Series IFB Typical Data*, R-3133-W, 3/98. https://www.bnzmaterials.com/wp-content/uploads/2013/03/PA-IFB.pdf
- [F15] BNZ Materials, *BB-Blok* application information, BB-01, 12/98 (flat suspended IFB roofs). https://www.bnzmaterials.com/wp-content/uploads/2013/03/BB-Blok1.pdf
- [F16] HarbisonWalker International, *KAST-O-LITE 30 LI PLUS* Product Data 10/19: 5874 (encrypted PDF; read from rendered pages). https://ssfbs.com/wp-content/uploads/2021/06/KAST-O-LITE_30_LI_PLUS.pdf
- [F17] HarbisonWalker International, *MIZZOU CASTABLE PLUS* Product Data 12/12: 5976. https://ssfbs.com/wp-content/uploads/2021/06/MIZZOU_CASTABLE_PLUS.pdf
- [F18] L&L Kiln Mfg, *Troubleshooting and Fixing Brick Problems*, rev. 9/10/2023 (same as [S8] in `electric-kiln-hardware.md`). https://hotkilns.com/sites/default/files/2023-09/troubleshoot-brick-9-2023_0.pdf
- [F19] L&L Kiln Mfg, *DaVinci Instruction Manual*, rev. 4-1-2022, including bulletin DV-0222 (model series X2300, X2800, X3200, T2300, T3400). https://hotkilns.com/sites/default/files/2022-05/BookDavinci-2022A-web.pdf
- [F20] L&L Kiln Mfg, *Easy-Fire Instruction Manual* (2024 web edition), bulletin BL-e28T-3. https://hotkilns.com/sites/default/files/2024-04/Easy-Fire%20Instructions-2024-web.pdf
- [F21] L&L Kiln Mfg, "All Kiln Features & Benefits" (web page). https://hotkilns.com/all-kiln-features
- [F22] L&L Kiln Mfg, "Custom High-Capacity Kilns for Industry & Large Sculpture" (web page). https://hotkilns.com/high-capacity-kilns
- [F23] Skutt Ceramic Products, KM-1627 product page, "Longer Lasting Lids and Slabs". https://skutt.com/products/km-1627/
- [F24] Skutt Ceramic Products, *KilnMaster Operating Manual*, revised 11/22/11 (same as [S9] in `electric-kiln-hardware.md`), "Lid Maintenance". https://www.theceramicshop.com/downloads/Warranties-Diagrams-Manuals/Skutt/KilnMaster-Manual-2006-2013-(Wiring-Diagrams-on-pages-56-65).pdf
- [F25] Olympic Kilns (Haugen Mfg.), *Electric Kiln Operating Manual* (undated; same as [S17] in `electric-kiln-hardware.md`). https://cdn.shopify.com/s/files/1/0694/7461/5526/files/Olympic_Kilns_Electric_Manual.pdf
- [F26] Olympic Kilns product and catalogue text, via search summaries only (site returned 403): https://www.olympickilns.com/product/fl12e/ ; https://www.olympickilns.com/wp-content/uploads/2023/02/gas.electric.catalog.2023.lowres.pdf ; retailer: https://www.clay-king.com/kilns/dpf_cleaning/olympic_dpf_fl20e.html
- [F27] Paragon Industries, Dragon 24 product page, Wayback Machine copy of 2025-09-16. https://web.archive.org/web/20250916050356/https://paragonkilns.com/products/dragon24-ceramic-and-pottery-front-loading-kiln
- [F28] Bailey Pottery Equipment, "Studio Deluxe and PRO Front Loaders" (same page as [S36] in `kiln-hardware.md`). https://baileypottery.com/studio-deluxe-and-pro-front-loaders
- [F29] Nabertherm, "Chamber Kilns up to 1300 °C heated from five sides" (sizes). https://nabertherm.com/en/products/arts-crafts/chamber-kilns/chamber-kilns-1300-degc-heated-five-sides ; retailer (search summary, "self-supporting, vaulted arch"): https://www.bathpotters.co.uk/nabertherm-chamber-kilns-n-series/p1896
- [F30] M. Hartmann (SECEM), US Patent 4,512,738, "High-temperature kilns", granted 1985-04-23. https://patents.google.com/patent/US4512738A/en
- [F31] Fastenal, *Torque-Tension Relationship for A307A, Grade 5, 8 & 9 Bolts*, Rev 3-6-09. https://crafter.fastenal.com/static-assets/pdfs/Torque-Tension_Chart_for_A307_Gr5_Gr8_Gr9.pdf
- [F32] R. Fournier, *Electric Kiln Construction for Potters*, Van Nostrand Reinhold, 1977. Archive full-text search snippets. https://archive.org/details/electrickilncons0000four
- [F33] Ceramic Arts Daily forum, "Electric kiln design: bucket or box preference" (403 to direct fetch; search summary). https://community.ceramicartsdaily.org/topic/4492-electric-kiln-design-bucket-or-box-preference/
- [F34] Warmglass forum, lid construction of round and oval top-loaders (search summary). https://www.warmglass.com/phpBB3/viewtopic.php?p=6199
- [F35] Replacement lid listings (search summaries): The Ceramic Shop, L&L 10-sided lid, https://www.theceramicshop.com/product/25826/ll-lid-10-sided-25/ ; Chesapeake Ceramics, Skutt 1027 parts, https://chesapeakeceramics.com/collections/1018/model_1027
