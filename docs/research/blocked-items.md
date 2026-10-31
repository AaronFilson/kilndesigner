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
