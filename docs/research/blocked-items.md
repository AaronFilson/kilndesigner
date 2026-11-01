# Sources for the blocked curve and masonry items (research round, 2026-10-31)

Research for the items marked **Blocked** in `docs/planning/10-30-26.md` and
`docs/planning/complex-curves.md`. Web search and fetch only; no book in hand. Researched
2026-10-31.

Status marks as in `refractory-bearing.md`: **Verified** = read in the page or PDF text;
**Snippet** = search-engine extract or a summary only, not read in the source; **Partial** = some of
what is needed is Verified, the rest not; **NOT FOUND** = searched and absent. Primary = a standard,
a maker's data sheet, a book or paper, or an official record; secondary = a web page that does not
cite its source for the number.

Short answer: only item 6 (mortar density) yields a number the engine can use. Items 1, 2, 3 and 8
give practice and method, not design numbers; items 4, 5 and 7 are not found.

| # | Item | Status | Usable number |
|---|---|---|---|
| 1 | Bottle-kiln chimney (hovel) sizes | Partial (secondary) | hovel "not less than 60 feet high" (1877 Hanley byelaw, quoted); no top diameter |
| 2 | Allowable stress for a hot band | NOT FOUND (allowable); practice Verified | none |
| 3 | Cracked dome's thrust (lunes) | Partial (method named and described; Heyman not read) | none |
| 4 | Dome and circle brick tables | NOT FOUND | none |
| 5 | Catenary meeting the next at a step | NOT FOUND | none |
| 6 | Mortar weight per volume, per 1000 brick | Verified (BNZ) | 116 to 131 lb/ft³; 200 to 400 lb per 1000 9 in brick |
| 7 | Allowable bearing / FoS for refractory | NOT FOUND (only the Snippet already in `refractory-bearing.md` [B18]) | none |
| 8 | Largest fireclay joint for tatami bricks | NOT FOUND (number); "keep joints thin" Verified (FAO) | none |

---

## 1. Bottle kilns: chimney (hovel) sizes

| Item | Text | Status | Source |
|---|---|---|---|
| Hovel height, byelaw | Borough of Hanley Works Committee minutes, 14 Feb 1877, quoted: hovels "not less than 60 feet high" | Verified on the page; secondary (the minutes are quoted, not seen) | [K1] |
| Hovel height, range | "Some could be up to 70 feet (21m) high." No source given | Verified on the page; secondary | [K1] |
| Oven (firing chamber) wall | "Its walls are about 12" (30cm) thick." No source given | Verified on the page; secondary | [K1] |
| Bands ("bonts") | iron bands round the oven "at about 12" (30cm) intervals"; no section size | Verified on the page; secondary | [K1] |
| Crown opening | "a central hole about 9 inches across" (Cardew, *A Pioneer Potter*, as quoted) | Verified on the page; quoted primary | [K1] |
| Hovel base and top diameters, Gladstone or any Stoke oven | Not given by Historic England list entries read (1220876), the Gladstone pages, thepotteries.org listed-building pages, or the Minkstone 3D model page. The Stoke Ceramic HAZ laser surveys (Staffordshire, LJMU, Keele) exist but no published dimensions were found | NOT FOUND | [K2], [K3], [K4] |
| Breda, Sèvres top diameter | not found online; Olsen Figs 6-50 to 6-58 remain the only source | NOT FOUND | |

So the cone's height has one secondary bound (60 ft, byelaw minimum for Hanley), and the oven
wall one secondary figure (about 12 in). The top diameter is still unsourced: the chimney stays a
straight stack. Next: Historic England's full list-entry texts for each of the 47 Stoke ovens, the
HAZ survey reports when published, or Hind, *Pottery Ovens, Fuels and Firing* (1937) and Sandeman
(1901), both cited by [K1] and not read.

## 2. A hot band round a dome or round wall

| Item | Text | Status | Source |
|---|---|---|---|
| Practice, Brazilian beehive kiln (5 m inside) | "four segments of steel band loosely bolted together should be laid" against the last wall course; "After the dome is completed the steel band should be tightened."; "The steel band of the dome should be tightened regularly and any corroded parts replaced." "Corrosion of the band will, in any case, take place after a few years." The kiln takes "8,500 burnt clay bricks with only one steel band for dome." No band size | Verified | [K5] |
| Argentine half-orange kiln (about 6 m, hemispherical) | built "usually with no iron or steel support at any place" | Verified | [K5] |
| Medalta beehive kilns | "wide adjustable bands of corroding steel which held the kiln together as it expanded and contracted"; no size | Snippet | [K6] |
| Allowable stress for band steel at temperature | ASME BPVC II-D Table 1A gives maximum allowable stress against temperature for SA-36 and others; the values were not read (paywalled); an Engineers Edge extract shows 12,700 and 16,900 psi for SA-36 with the column headings cut off | NOT FOUND (number); table identified | [K7] |
| A rule for sizing kiln bands | none | NOT FOUND | search |

So the band's force (the engine's hoop tension) has no sourced allowable to divide by. ASME II-D
Table 1A is the primary source to buy or borrow; it is written for pressure parts, and whether it
suits an unpressurised band is a judgement no source read makes. The band's temperature is also
unknown (it sits on the outside of the wall). Still blocked.

## 3. A round dome past 51.8° from the crown (hoop tension lost)

| Item | Text | Status | Source |
|---|---|---|---|
| Lune method | Eddy's method "provides an equilibrium solution or curve assuming zero hoop forces in the dome; that is, the dome consists of a series of arches butt against each other." "The force polygons for each voussoir in the lune share a common pole ... from which meridional forces and the outward horizontal thrust at the dome's base are calculated." Hoop forces "are maximum compression at the crown of the dome, decrease to near zero, and then become tensile." Cites Eddy, *New Constructions in Graphical Statics* (1877) | Verified (MIT tutorial page) | [K8] |
| Heyman's treatment | thrust-line work treats a hemispherical dome "as a series of lunes", following Poleni and Heyman; Heyman assumes no hoop force between lunes, which reduces the dome to a 2-D arch for minimum thickness | Snippet (review abstracts); Heyman's text not read | [K9], [K10] |
| Cracked dome with a compressed cap | later work keeps hoop compression in the cap above the cracks, the lunes below acting as arches | Snippet | [K10] |
| Lau thesis (MIT 2006), Wolfe's and Eddy's methods worked | identified; the PDF is encrypted and its text was not extracted | NOT READ | [K11] |

Usable as a method, pending a read of the primary: below the angle where hoop stress would turn
tensile, cut the dome into lunes and find each lune's thrust as an arch (the engine already finds
arch thrust lines, Heyman's way, for door arches and vaults). That is Eddy's 1877 method as
described by [K8]; the thrust it gives is one *equilibrium* solution (by Heyman's safe theorem, safe if
the line stays in the masonry; that reading is ours, not quoted). Primary to read next: Heyman, *Equilibrium
of Shell Structures* (Oxford, 1977) and *The Stone Skeleton* (Cambridge, 1995), the dome chapter;
Eddy (1877). Partial: the method is described in a secondary source, the 51.8° itself is the
membrane result already sourced in `domes-over-doors.md` §D1.

## 4. Dome and circle brick tables

| Item | Finding | Status | Source |
|---|---|---|---|
| HarbisonWalker *Modern Refractory Practice* (1950; 4th ed. 1961) | on the Internet Archive (`modernrefractory00harb`, `modernrefractory0000harb`) but "access-restricted" (borrow only); not read. Whether it holds dome tables is unconfirmed | NOT FOUND (not read) | [K12] |
| Full-text search of the Archive for "dome brick" Harbison | 36 hits: hot-blast stove dome brick (steel works), none a kiln dome table | NOT FOUND | [K12] |
| A.P. Green dome brick | the scanned A.P. Green pages in `brick-shapes.md` have none | NOT FOUND | `brick-shapes.md` |

Conical (tatami) bricks sized by the builder remain the only sourced route (`conical.py`).
Next: borrow the 1961 *Modern Refractory Practice* from the Archive and check its index.

## 5. One chamber's catenary meeting the next at a step

Searched for noborigama and stepped multi-chamber construction with catenary vaults. Found only
the general description (chambers as "half-tubes ... buttressing each other" with openings between,
Wikipedia, secondary) and a modern multi-chamber kiln's layout without its arch details
(St John's, Johanna kiln). **NOT FOUND.** The refusal stands. Next: Olsen's noborigama chapter,
Rhodes, *Kilns: Design, Construction and Operation*, and Japanese-language builders' manuals.

## 6. Mortar: weight per volume and per 1000 brick

BNZ Materials, refractory mortars data sheet (PDF, created 2013-05-14), text read [K13]:

| Property | Super Blak | No. 2986 | Blakbond | Zelie No. 20 |
|---|---|---|---|---|
| Temp. limit, °F | 3000 | 3000 | 3000 | 2700 |
| "Estimated lbs. to set 1000 9" x 4 1/2" x 2 1/2" brick*" | 200-400 | 200-400 | 200-400 | 200-400 |
| Bulk density as received, pcf | 126 | 129 | 131 | 121 |
| Dipping, pcf | 124 | 126 | 123 | 116 |
| Dipping, percent H2O | 4 | 4 | 7 | 10 |

"* Amount depends on thickness of joint and porosity of the brick." Status: **Verified**, primary
(maker's sheet). Also, Snippet only: a Plibrico air-set mortar, "350-400 lb / 160-180 kg per 1000
standard firebrick"; an ABI Super #3000 Mix 26 sheet, 300 to 350 lb per 1000 9 in equivalents; a
hydraulic "Mortar Mix 413", about 850 lb per 1000 at a ¼ in joint [K14]. Bag size: HWI Green Patch
421 sold as a 55 lb bag (distributor listing, Snippet) [K15]; no yield per bag is printed by any
source read, but yield follows from the bag weight and the density.

Usable: the wedge-joint mortar's volume times a sourced wet density (116 to 126 pcf dipping, BNZ)
gives its weight; divide by the bag weight the builder buys to count bags. The density applies
only to the four BNZ products; another maker's mortar needs its own sheet.

## 7. Allowable bearing stress or factor of safety for refractory brick

Searched again (2026-10-31). Only the Elsevier topic-page extract already recorded as
`refractory-bearing.md` [B18] came back ("a factor of safety of 2 based on the minimum specified
crush strength of the material at temperature", for refractory-lined vessels; book unidentified),
plus, from the same publisher's "Refractory Lining" topic page, "The cold crushing strength of a
fired brick is generally much greater than its crushing strength at higher temperatures" (Snippet).
**NOT FOUND**: no new primary source. The bearing stays shown, not checked.

## 8. Fireclay joints with hand-made (tatami) bricks

| Item | Text | Status | Source |
|---|---|---|---|
| Joint rule, half-orange kiln (FAO) | "Keep the joints thin otherwise the kiln will not be strong and durable."; "Bricks are laid in mud mortar consisting of clay, sand and charcoal fines."; near the top, "put each brick hard up to its neighbour ... keeping joints as thin as possible so that each run of brickwork is tight" | Verified; no number | [K16] |
| Japanese climbing kilns | Arita kilns' walls of "tonbai" fire bricks; Tokoname's last noborigama on a 17° slope (MLIT multilingual heritage texts); no joint size | Snippet | [K17] |
| A largest joint for tatami brick | none | NOT FOUND | search |

---

## Second round (2026-10-31): rampant arches, door heads in vaults, iron vs steel bands

Web search and fetch only, short round. Short answer: no gap closes. One method paper for
openings in vaults (Verified title and summary), one steel-at-temperature table (Snippet), nothing
for rampant-arch thrust, wrought iron when hot, band sizing, chimney diameters or refractory FoS.

### 9. Rampant (unequal-springing) arch thrust

| Item | Finding | Status | Source |
|---|---|---|---|
| Hot thrust factor for unequal springings (HarbisonWalker style) | none found | NOT FOUND | search |
| Three-hinged parabolic arch with supports at different levels | textbook topic (span split into L1, L2 from the two springing heights, H from moment about the crown hinge); seen only as a garbled Scribd extract, no citable text | Snippet; not usable | [K18] |
| Heyman, *The Stone Skeleton*, "The masonry vault" chapter | exists (Cambridge abstract page); not read | NOT READ | [K19] |

Engine: keep using the largest printed HarbisonWalker factor for the rampant vault. A sourced
route is the cold statics itself: for vertical loads H is the same everywhere along the arch, and a
thrust line through the two springings at their own heights gives H by moments (standard statics,
not a hot factor). The hot factor for unequal springings stays unsourced.

### 10. A door head rising into a vault's edge (opening in a barrel vault)

| Item | Text | Status | Source |
|---|---|---|---|
| Barrel vault with lunette, no-tension analysis | M. Monaco, I. Bergamasco, M. Betti, "A no-tension analysis for a brick masonry vault with lunette", *J. Mech. Mater. Struct.* 13(5) (2018) 703–714. Summary read: a rigid no-tension (Heyman) continuum model; the vault as a compression-only membrane between extrados and intrados; admissible stress field from a concave stress function; "particular attention" to singular stresses (line Dirac deltas) along the intersection curves | Verified (title, authors, summary); paper not read; primary | [K20] |
| Load share between vault and door ring | no source gives a split | NOT FOUND | search |

So the engine's assumption (vault spans to its end walls; door ring carries none of the vault) is
consistent with the safe-theorem approach these papers use (any admissible compression field is
safe), but the papers show the load concentrating along the intersection curve, i.e. onto the
lunette's edge. That edge is the door ring here: the assumption is not confirmed and may be
unconservative for the ring. Read [K20] in full before relying on it.

### 11. Iron vs steel bands

| Item | Text | Status | Source |
|---|---|---|---|
| Carbon steel yield at temperature, EN 1993-1-2 Table 3.1 k_y,θ | 1.00 to 400 °C, 0.93 at 450, 0.78 at 500, 0.63 at 550, 0.47 at 600, 0.33 at 650 °C (worked-example extract); 0.78 at 500 °C confirmed in a Dlubal example | Snippet (two secondary extracts agree; the standard not read) | [K21] |
| SA-36 in ASME II-D Table 1A | upper temperature for SA-36 plate stated as 900 °F in a forum post; values not read; an NRC filing notes an edition (1974) printed SA-36 values in error, so the edition matters | Snippet | [K7], [K22] |
| Wrought iron strength when hot | Fairbairn, as told by Pole: tensile resistance "as great at the temperature of zero as it was at 60° or upwards" (cold only). Kirkaldy (1862) tested room-temperature tensile strength; no hot data found | Snippet; no hot numbers | [K23] |
| Creep of either at band temperature | none | NOT FOUND | |
| Band temperature on a kiln's outside | none measured | NOT FOUND | |
| Sizing and tightening | only FAO practice already in §2 (steel band, tighten after building and "regularly", replace corroded parts) | Verified (§2) | [K5] |

Which is better: no source compares them for kilns. The only sourced number for either is the
steel reduction (Snippet): full yield strength up to 400 °C. A band on the outside of a kiln wall
is very likely below that, but no measured band temperature was found, so the engine cannot yet
claim it. Usable once the standard is read: allowable = (yield at 20 °C) × k_y,θ / FoS, refusing above
the tabulated range (ADR 0009); no FoS for a band was found.

### 12. Other sources still unread

HarbisonWalker *Modern Refractory Practice*, Heyman's two books, Hind (1937), ASME II-D: no free
copies found this round. Bottle-oven chimney diameters: Stoke listing texts searched (Dolby Pottery,
Uttoxeter Road, Falcon Works) describe shape only ("square base ... oval and then cylindrical at
the top"), no dimensions [K24]. Refractory FoS: nothing new beyond §7.

---

## Third round (2026-10-31): statics, in `masonry-statics.md`

### 13. What the third round settled

Full findings, quotes and sources in `masonry-statics.md` ([M1]–[M6]). In short:

| Item here | Third round | Status |
|---|---|---|
| §10 lunette (door head in a vault) | [K20] read in full: a compression-only line force gathers along the intersection curve, larger than in a free arch of the lunette's shape; no load share printed | Partial (method Verified; no number) |
| §9 rampant arch | nothing beyond the cold statics | NOT FOUND |
| §3 dome past 51.8° | [K11] read in full: lune base thrust h = H/[aθ(sin α − sin δ)]; H/W ≈ −0.583α + 1.123 (α ≥ π/3, ±20 %); statics estimate Eq. 3.6; no-hoop minimum t/R 0.069 for a hemisphere; TNA hemisphere (T/W)min 19.8 % | Verified (Lau; Heyman via Lau) |
| Groin vaults (new) | TNA worked example, 10 × 7.5 m cross vault, t/R = 0.10: corner thrust 67.5–96.7 % of W, forces "accumulate along the diagonals" | Verified |
| §5 catenary at a step | | NOT FOUND |
| Corbels hot | only a cold 1 in per course chimney rule | NOT FOUND (Snippet) |
| §7 refractory bearing | Trinks Vol. II read, no value; Vol. I not online | NOT FOUND |

## Fourth round (2026-10-31): full texts on the Internet Archive, Eurocodes, NRC

Full texts read this time (scans' text layers, searched and quoted): EN 1993-1-2 and EN 1992-1-2
(BSI printings), Kent's *Pocket-Book* (1916), Norton's *Refractories* (2nd ed. 1942, 3rd ed. 1949),
HarbisonWalker's 1906 catalogue and 2008 *Brick Installation Guide*, the Wellsville Fire Brick
catalogue (1923), Norton Co.'s *Refractory Cements* (1939), Bureau of Standards Technologic Paper 7
(1911), an NRC filing quoting ACI 349-97. Bands, iron against steel and bottle-oven sizes are in
`bands-and-bottle-kilns.md`; the rest below.

| # | Item | Status | Usable number |
|---|---|---|---|
| 2, 11 | Hot band: strength, FoS | **Verified** (`bands-and-bottle-kilns.md`) | EN 1993-1-2 k_y,θ = 1.0 to 400 °C; Norton FoS "at least 5"; HW 12,000 psi |
| 1 | Bottle-oven sizes | Partial, secondary (`bands-and-bottle-kilns.md` §6) | chambers 11–20 ft; one hovel 60 ft × 33 ft 3 in; no top diameter |
| 4 | Dome brick tables | **Verified** (Norton Table 155 and method); HW *Modern Refractory Practice* still not read | radial dome brick small ends; dome count by rings |
| 6 | Mortar per 1000 brick, bag size, air vs heat setting | **Verified** (HW 2008, HW 1906, Wellsville 1923) | 250–300 / 350–450 lb per 1000; 55 lb sacks |
| 13 | Concrete under heat | **Verified** (EN 1992-1-2; ACI 349-97 as quoted by NRC) | f_c,θ/f_ck table; λ 1.33–1.95 W/m K at 20 °C; 150 °F / 200 °F limits |
| 7 | Refractory allowable bearing | Partial: a design method (creep) and a worked example, no general allowable | Norton: 1.7 psi example; BoS 1911 test 50 psi at 1350 °C |

### 18. Dome and circle brick (completes item 4 in part)

| Item | Text | Status | Source |
|---|---|---|---|
| Norton, radial dome brick | "The spherical dome can be best constructed of special shapes having a large end of 4½ by 2½ in. and a taper such that a projection of their corners will pass through the center of curvature of the dome. This allows strictly radial joints and either 2½- or 4½-in. rings. However, as the rings approach the top of the crown, even these blocks will not fit perfectly unless hand cut. In practice, such shapes can be economically made by grinding insulating firebrick, but with heavy bricks this is not generally feasible." Table 155 "Radial Dome Brick", for 9 in thick domes, inner end width × thickness (in) by inside radius of curvature: 4 ft 3.79 × 2.11; 6 ft 4.00 × 2.22; 8 ft 4.12 × 2.29; 10 ft 4.18 × 2.33; 14 ft 4.28 × 2.37; 18 ft 4.33 × 2.40; 24 ft 4.36 × 2.42; 30 ft 4.39 × 2.44; 40 ft 4.42 × 2.45 | **Verified**, primary (OCR; the large-end "4½ by 2½" read as "4} £ by 2" and corrected from the table, whose ends shrink from 4.5 × 2.5) | [K25] pp. 730–731 |
| Norton, standard shapes | "Most domes are built up in 2½-in. rings with combinations of straights and keys alternated with 4½-in. rings of straights and wedges to give the curvature in both directions. A by no means accurate fit can be obtained, and mortar must be used to fill the joints." Method (Fig. 417): outer area A = 2π(r_m + ½t)h_m; 9-in equivalents in the first ring = circumference at a / 4.5; No. 1 keys in the first ring = (circ. a − circ. b)/(4.5 − 4.0); rings = arc aa₁/2.5; No. 1 wedge rings = (aa₁ − bb₁)/(2.50 − 1.88). Worked example: r = 120 in, t = 9 in, θ = 60°: 90 nine-inch equivalents and 58 No. 1 keys in the first ring, 54 rings, 15 No. 1 wedge rings, 1,230 nine-inch equivalents in all (342 No. 1 wedges, 585 No. 1 keys, 303 straights). "As each ring in the dome is self-supporting, a complete form is not needed." | **Verified** (formulas partly garbled in OCR; the worked numbers read cleanly) | [K25] pp. 731–732 |
| Norton, dome shape | "the spherical dome is not the most stable form. Fellows and Goodier have shown that this limiting form approaches the surface of revolution formed by an ellipse. Any dome inside this surface is stable." Cites J. N. Goodier, "Stresses in Domes and Crowns of Circular Kilns", *J. Am. Ceram. Soc.* 16 (5), 1933, p. 220 (not read) | Verified | [K25] p. 730; [K26] |
| HarbisonWalker 1906 catalogue | "Brick tables" (p. 80): "how a circle or arch of any diameter may be laid up with a combination of the standard size fire brick" (wedge-brick rings by inside diameter from 2 ft); "Table for circle brick" (p. 100): number to the circle, sine of half angle, "Diameter for 9" Chord". Rings only; no dome table | Verified | [K27] |
| HW *Brick Installation Guide* (2008) | "Cylindrical walls, arches and domes are built with brick tapered to turn circles ... Combinations of these shapes taper in two dimensions to turn domes." Ring combinations pp. 43–69; dome design by "computer programs" on request; no dome table | Verified | [K28] pp. 11, 20 |
| HW *Modern Refractory Practice* (1950, 1961) | still borrow-only; a third Archive copy (`modernrefractory0000harb_f4j7`) also restricted | NOT READ | [K12] |

**Engine (`conical.py`, `rings.py`, layer 4 of `complex-curves.md`):** Norton's method counts a
dome of standard 9-in straights, No. 1 wedges and No. 1 keys ring by ring; Table 155 gives
radial-dome brick sizes for 9 in domes (or IFB ground to them). Both are usable now.

### 19. Mortar: weight per 1000 brick, bags, air- and heat-setting (completes item 6)

| Source | Text | Status |
|---|---|---|
| HW *Brick Installation Guide* (2008), p. 9, "Approximate Pounds of Mortar per 1000 9-Inch Brick (9 × 4½ × 2½ Inch)" | Brick laid dry and grouted / dipped or thinly trowelled: heat-setting SATANITE 250–300 / 350–450; air-setting HARWACO BOND, SAIRSET, SAIRBOND 250–300 / 350–450; H-W PERIBOND 300–400 / 500–600. "This is for 9-inch straights. Normally, for larger sizes the quantities required are reduced in proportion to the decrease in surface area covered by the mortar per 1000 9-inch equivalent." "NOTE: Minimum figures are used ordinarily for estimating." Packaging: "Standard packaging for monolithic refractories are 55 lb. sacks, pails, and cartons, and 2,000 lb., 3,000 lb., and 4,000 lb. bulk bags." Grossing (overage) for brick: 1–100 10 %, 101–1,000 7 %, 1,001–5,000 3 %, 5,001–10,000 2 %, over 10,000 1 % | **Verified**, primary [K28] |
| HW 2008, p. 11, joints | "Brickwork laid with heat-setting mortars should have thin joints, either dipped or poured. The brick should be rubbed or tapped into place to produce as much brick-to-brick contact as possible. Joints made with an air-setting mortar generally can be somewhat thicker, but such joints should be completely filled." | **Verified** [K28] |
| HW 1906 catalogue, "General information about fire brick", p. 79 | "From 250 to 350 pounds of fire clay or silica cement is enough to lay up one thousand brick ... In first class brick work, less than three hundred and fifty pounds of fire clay per thousand brick should be used." "1 cubic foot fire clay brick work weighs 150 pounds"; "1 cubic foot brick work requires 17 nine-inch straight brick" | **Verified** [K27] |
| Wellsville Fire Brick Co. catalogue (1923) | "From 400 to 600 pounds of fire clay are enough to lay one thousand brick." "1 cubic foot of fire-brickwork weighs 125 to 140 pounds." | **Verified** [K29] |
| Norton Co., *Refractory Cements* (1939) | for RA 162 and RA 1019 (Alundum laying cements): "Thin joints and a surface wash of the water mix is recommended for brick construction. Approximately one half pound of cement should be provided for each 9" standard brick." Sold in 5, 10 lb bags, 25, 50, 300 lb kegs | **Verified** (specialty cements, not fireclay mortar) [K30] |

**Engine (bill of materials):** the wedge-joint mortar can now be counted per 1000 brick from a
current maker's table (HW: 350–450 lb per 1000 9-in straights trowelled, 250–300 dipped; minimum
figures for estimating), or by joint volume × density (BNZ, §6), and bagged at 55 lb (HW's
standard sack). The joint-volume route is the one that follows a wedge joint's real size; the
per-1000 figure is for thin joints only. Air-setting allows "somewhat thicker" joints, no number.

### 20. Concrete as a kiln platform (new)

**EN 1992-1-2:2004, Table 3.1** (p. 20), normal-weight concrete, f_c,θ / f_ck (Verified, primary [K31]):

| θ, °C | 20 | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900 | 1000 | 1100 | 1200 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Siliceous aggregate | 1.00 | 1.00 | 0.95 | 0.85 | 0.75 | 0.60 | 0.45 | 0.30 | 0.15 | 0.08 | 0.04 | 0.01 | 0.00 |
| Calcareous aggregate | 1.00 | 1.00 | 0.97 | 0.91 | 0.85 | 0.74 | 0.60 | 0.43 | 0.27 | 0.15 | 0.06 | 0.02 | 0.00 |

Scope, §3.2.1: "As creep effects are not explicitly considered, the material models in this
Eurocode are applicable for heating rates between 2 and 50 K/min." "(7) Possible strength gain of
concrete in the cooling phase should not be taken into account." Calcareous means "containing at
least 80% calcareous aggregate by weight" (§3.2.2.1(4)).

**Thermal conductivity, §3.3.3** (Verified): upper limit λc = 2 − 0.2451(θ/100) + 0.0107(θ/100)²
W/m K; lower limit λc = 1.36 − 0.136(θ/100) + 0.0057(θ/100)² W/m K, 20 °C ≤ θ ≤ 1200 °C; "The value
of thermal conductivity may be set by the National annex within the range"; the lower limit "gives
more realistic temperatures for concrete structures" (Annex note). At 20 °C: 1.95 and 1.33 W/m K
**(derived)**. Density: the standard's figures use "a density of 2300 kg/m3 for siliceous
concrete" (Fig. 3.6b) and gives ρ(θ) falling to 0.95 ρ(20 °C) by 400 °C (§3.3.2(3)).

**Long-term temperature limits, ACI 349-97 §A.4**, as quoted in an NRC-filed AREVA calculation
(Verified as quoted; ACI text not read; nuclear-safety concrete) [K32]: "Temperatures shall not
exceed 150'F except for local areas, such as around penetrations, which are allowed to reach a
maximum of 200'F for normal operation or any other long term period. For accident or any other short
term period, the temperatures shall not exceed 350 F for the surface. Higher temperatures may be
allowed for concrete if tests are provided to evaluate the reduction in strength and this reduction is
applied to design allowables." The NRC's own criteria for storage casks (same filing): up to 200 °F
"no tests or reduction of concrete strength are required"; 200 to 300 °F none required "if Type II
[OCR: "Type I/"] cement is used and aggregates are selected which are acceptable" (listed minerals or a low
expansion coefficient).

ACI 216.1 not read (paywalled). The user's 1800 psi is not in any source read; Bleininger (1911)
quotes the period's "English specifications" for firebrick crushing ("not less than 1,800 pounds per
square inch"), unrelated to concrete.

**Engine (foundation / floor heat loss):** the floor's conductivity can take EN 1992-1-2's lower
limit (sourced, temperature-dependent) and 2300 kg/m³; the concrete's strength at the slab's top
temperature is f_ck × k(θ) from Table 3.1; and a sourced warning threshold for the slab's top face is
150 °F general / 200 °F local (ACI 349, long-term). Refuse above Table 3.1's use (sustained heating is
outside its 2–50 K/min scope: show, don't certify).

**Used (2026-10-31):** the conductivity, Table 3.1 and ACI 349's 150 °F in `foundation.py` and
`heatloss.py`; minimum strengths (IRC Table R402.2, EN 1992-1-1 Table E.1N) and the allowable
bearing (AISC 360-16 §J8, as ACI 318) in `concrete-foundations.md`.

### 21. Refractory bearing (item 7, partial)

| Source | Text | Status |
|---|---|---|
| Norton (1949), "Application of Load-test Results to Design", pp. 416–417 | "the results of the usual short-time load test are of little value to the designer of furnaces. Only with the long-time test that has come to equilibrium flow are values available for the designer to use in computing allowable stresses in the structure. From the curve in Fig. 243 ... A pier under the hearth of a heat-treating furnace has an allowable deformation of 10 per cent in its estimated working life of 4,000 hr, which amounts to a rate of 2.5 per cent in 1,000 hr. On the curve this corresponds to a loading of 1.7 psi." Fig. 243 is "a firebrick" (p. 409); its temperature not read | **Verified** (method and example; Fig. 243 not read) [K25] |
| Norton, same | "very few load failures occur in actual furnace construction and then only in cases where the refractory part is heated all the way through, such as in piers, partition walls, and highly insulated crowns. Nearly all other parts of furnaces have a considerable temperature gradient ... the load is supported by a relatively cool portion of the refractory"; approximate by "dividing the wall into a number of sections parallel to the face and considering the mean temperature of each section" | **Verified** [K25] |
| Bleininger & Brown, NBS Technologic Paper 7 (1911) | test loads "should be somewhat greater than the maximum furnace loads"; tentative spec No. 1 A: at 1350 °C "under a load of 50 pounds per square inch, a standard fire brick tested on end should show no serious deformation and should not be compressed more than 1 inch" (in 9 in; footnote: "In more recent specifications the maximum deformation allowed is one-half inch"), cold crushing "not less than 1000 pounds per square inch"; No. 1 B, 30 psi. "while a fire brick may show a compressive strength of 2500-3000 pounds per square inch at atmospheric temperature, it will possess but a small part of this strength at a temperature of, say, 1300° C." | **Verified**, primary [K33] |
| Kent (1916), factors of safety | masonry dead load: Rankine 4, Unwin 20; Kent: "If the actual crushing strength of a pier of masonry is known from direct experiment, then a factor of safety of 4 is sufficient ... but if the crushing strength is merely assumed from figures given by the authorities ... a factor of safety of 20 may be none too great" | **Verified** (building masonry, cold) [N2 in `bands-and-bottle-kilns.md`] |
| Trinks, *Industrial Furnaces* (1925–26), Chesters (1944) | Trinks read (two Archive volumes): binding practice, no allowable; Chesters restricted | NOT FOUND / NOT READ |

So: still no general hot allowable bearing stress. Sourced now: (a) Norton's design method (allowable
stress from a long-time creep rate and an allowed deformation over the working life; example 1.7 psi
for a pier heated through), (b) the cool-side argument for walls with a gradient, (c) a cold FoS of 4
(tested strength) to 20 (assumed strength) for masonry (Kent, building masonry). The engine can show
bearing against CCS / 4 and CCS / 20 as cold references, and flag only fully heated piers and
partition walls, with Norton's quote; a hot pass/fail still needs a creep curve for the product.

### 22. Next sources to get

Goodier (1933) *J. Am. Ceram. Soc.* 16:220 (dome and crown stresses of circular kilns; Wiley,
paywalled); Norton Fig. 243 (page image, to read its temperature); HW *Modern Refractory Practice*
(borrow); ASME II-D Table 1A (library); ACI 216.1 and ACI 349 (library); Hind (1937); Historic
England's Ceramic HAZ bottle-oven survey reports.

---

## Sources

- [K1] "The Potteries Bottle Oven: Construction, their different parts, and who built them", bottleoven.blogspot.com (author not named on the page). https://bottleoven.blogspot.com/p/construction.html . Secondary; quotes Hanley Works Committee minutes (14 Feb 1877, extract by Paul Niblett) and Cardew, *A Pioneer Potter*.
- [K2] Historic England, list entry 1220876, Bottle Oven on corner of Warren Street, Longton. https://historicengland.org.uk/listing/the-list/list-entry/1220876 (search extract).
- [K3] Gladstone Pottery Museum: https://en.wikipedia.org/wiki/Gladstone_Pottery_Museum ; https://potteries.org.uk/gladstone-pottery-museum (no dimensions).
- [K4] Historic England, *Minkstone Works bottle oven* 3D model. https://sketchfab.com/3d-models/minkstone-works-bottle-oven-726958d496a94b28a6debbc58ac61e50
- [K5] FAO, *Simple technologies for charcoal making* (FAO Forestry Paper 41), Chapter 7 "Brick kilns". https://www.fao.org/4/x5328e/x5328e08.htm . Primary (FAO publication). The series title is from memory of the X5328E document code; check on the FAO contents page.
- [K6] Alberta's Historic Places, "Rebuilding the Beehive Kiln" (2015). https://albertashistoricplaces.com/2015/09/09/rebuilding-the-beehive-kiln/ (search extract).
- [K7] ASME BPVC Section II Part D, Table 1A (maximum allowable stress values, ferrous). Not read. Extract: https://engineersedge.com/pressure,045vessel/maximum_allowable_stress_values_13906.htm
- [K8] W. W. Lau (MIT Masonry Research Group), "Tutorial for Eddy's Method". https://web.mit.edu/masonry/wwlau/eddyTutorial.htm . Read. Cites H. T. Eddy, *New Constructions in Graphical Statics* (1877).
- [K9] "Finite element thrust line analysis of axisymmetric masonry domes" (ResearchGate record). https://www.researchgate.net/publication/294882612 (abstract extract).
- [K10] "Graphical Modelling of Hoop Force Distribution for Equilibrium Analysis of Masonry Domes" (ResearchGate record). https://www.researchgate.net/publication/352582506 (abstract extract).
- [K11] W. W. Lau, *Equilibrium Analysis of Masonry Domes*, MIT M.Eng. thesis (2006). https://web.mit.edu/masonry/papers/wwLau_SMBT_2006.pdf (encrypted PDF, not extracted).
- [K12] Harbison-Walker Refractories Co., *Modern Refractory Practice* (1950; 4th ed. 1961). https://archive.org/details/modernrefractory00harb ; https://archive.org/details/modernrefractory0000harb (access-restricted).
- [K13] BNZ Materials, refractory mortars data sheet (PDF created 2013-05-14). https://www.bnzmaterials.com/wp-content/uploads/2013/05/mortars_data_sheet.pdf . Text read.
- [K14] Search extracts (Plibrico air-set mortar; ABI Super #3000 Mix 26; Mortar Mix 413); sheets not opened.
- [K15] Distribution International, "GREEN PATCH 421 55#". https://shop.distributioninternational.com/refractories/refractories-castable/recagp42155h (search extract).
- [K16] FAO, as [K5], Appendix 3 "Building and operating the Argentine Half Orange Kiln", 2. Brickwork. https://www.fao.org/4/X5328e/x5328e0i.htm . Read.
- [K17] Japan MLIT multilingual explanation database, "Tonbai Walls" and "Noborigama". https://www.mlit.go.jp/tagengo-db/en/R2-01934.html (search extract).
- [K18] "Structural Analysis" (Scribd upload, unattributed), three-hinged parabolic arch at different levels. https://www.scribd.com/document/318257756/Structural-Analysis (search extract).
- [K19] J. Heyman, *The Stone Skeleton* (Cambridge, 1995), "The masonry vault". https://resolve-he.cambridge.org/core/books/abs/stone-skeleton/masonry-vault/F8FED3C1C0FB0D34DF89CDE03A5E05C1 (abstract only).
- [K20] M. Monaco, I. Bergamasco, M. Betti, "A no-tension analysis for a brick masonry vault with lunette", *Journal of Mechanics of Materials and Structures* 13(5), 2018, 703–714. https://msp.org/jomms/2018/13-5/p09.xhtml ; PDF https://msp.org/jomms/2018/13-5/jomms-v13-n5-p09-s.pdf (not read).
- [K21] EN 1993-1-2:2005 Table 3.1 (not read). Extracts: Scribd "Calculation Examples" https://www.scribd.com/document/266876895/Calculation-Examples ; Dlubal knowledge base 001644 https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001644 .
- [K22] eng-tips, "Upper temp limit SA36" https://eng-tips.com/threads/upper-temp-limit-sa36.376573 (search extract; page 403); NRC ML20069J689 https://www.nrc.gov/docs/ML2006/ML20069J689.pdf (search extract).
- [K23] W. Pole, *Life of Sir William Fairbairn*, ch. XXII, via Grace's Guide. https://www.gracesguide.co.uk/Life_of_Sir_William_Fairbairn_by_William_Pole:_Chapter_XXII (search extract). Kirkaldy (1862): https://en.wikipedia.org/wiki/David_Kirkaldy .
- [K24] British Listed Buildings, Bottle oven at former Dolby Pottery. https://britishlistedbuildings.co.uk/101220666-bottle-oven-at-former-dolby-pottery-penkhull-and-stoke-ward (search extract).
- [K25] F. H. Norton, *Refractories*, 3rd ed. (McGraw-Hill, 1949), Internet Archive `dli.ernet.239470` and `in.ernet.dli.2015.462020`, https://archive.org/details/dli.ernet.239470 . Full text read: pp. 408–417, 704, 729–733. 2nd ed. (1942), `in.ernet.dli.2015.205928`, same dome text.
- [K26] J. N. Goodier, "Stresses in Domes and Crowns of Circular Kilns", *J. Am. Ceram. Soc.* 16 (5), 1933, p. 220. Cited by [K25]; not read.
- [K27] Harbison-Walker Refractories Co., *Catalogue containing useful information in connection with the use of silica, magnesia, chrome and fire clay brick* (Pittsburgh, 1906). https://archive.org/details/cataloguecontain00harbrich . Full text read: pp. 79, 80, 100.
- [K28] Harbison-Walker Refractories Co., *Brick Installation Guide* (2008). https://ssfbs.com/wp-content/uploads/2021/06/HW_Brick_Installation_Guide.pdf . Read: pp. 9, 11, 20.
- [K29] Wellsville Fire Brick Co., catalogue (1923). https://archive.org/details/wellsville-brick-1920s-a . Full text read ("general information" page).
- [K30] Norton Company, *Refractory Cements* (1939). https://archive.org/details/NortonRefractoryCementsCCA23189 . Full text read.
- [K31] BS EN 1992-1-2:2004, *Eurocode 2: Design of concrete structures — Part 1-2: Structural fire design*. PDF read: https://www.phd.eng.br/wp-content/uploads/2015/12/en.1992.1.2.2004.pdf (third-party copy of the BSI printing). §3.2.1, Table 3.1, §3.3.2–3.3.3, Annex A note.
- [K32] AREVA calculation 10955-TLAA01 rev. 0 (2015), filed with the US NRC, ML15075A347, quoting ACI 349-97 §A.4 and the NRC's NUHOMS SER (1994). https://www.nrc.gov/docs/ML1507/ML15075A347.pdf . Read. Public record.
- [K33] A. V. Bleininger and G. H. Brown, *The Testing of Clay Refractories, with Special Reference to their Load Carrying Ability at Furnace Temperatures*, Bureau of Standards Technologic Paper 7 (1911). https://archive.org/details/testingofclayref19117blei . Full text read, pp. 5, 76–77 and the load-test chapter. Public domain (US government).
