# HarbisonWalker, *Handbook of Refractory Practice* (2005): the drawn and boxed content of the product sections

[HW05] Harbison-Walker Refractories Company, *Handbook of Refractory Practice*, © 2005 (331 PDF pages;
owner's copy `docs/research/da86e4bd09a66be00c11a67957ff8e5a.pdf`, git-ignored and copyrighted). Second
reading, by the "lit" agent, 2026-11-17. Scope: Section 9's bound-in bulletins (PDF 232–330) and Sections 5–6
(MP-1 to MP-24, BP-1 to BP-9; PDF 91–123). It adds to `hwi-handbook.md` (the first pass) and does not
repeat it.

How it was read. Every page in scope was scanned for vector paths, embedded images and keywords
(`scan.py`). Pages with graphs, diagrams or photos were rendered, most of them as 75 dpi contact sheets
(three pages per sheet) for triage, and the graphs and tick matrices again at 130–300 dpi. The Emisshield
curves were digitised from the page's vector paths with PyMuPDF and checked on a 300 dpi render. Marks:
**Verified** (read on the page image, or on the vector path with the method and ± stated), **Read** (text
layer only), **Derived** (arithmetic here). Quotes are short. No page image or crop is committed.

Section 9 pages carry no printed label, so each item cites the bulletin's catalogue number and date, and
the PDF page once.

Result in one paragraph: the only curves in the bound-in bulletins are the Emisshield emissivity plot (PDF
241), the KAST-O-LITE k plots (PDF 280, done in the first pass) and two bar charts (PDF 234 and 237, PDF
244). There is no hot-MOR, creep, expansion or temperature-profile curve in Section 9, and no k curve for
any brick, IFB, dense castable or blanket besides the tables the first pass already transcribed. Sections
5–6 have no drawing at all beyond a header rule, and no box, caution or footnote beyond one (PDF 115).

---

## 0. Triage

"Kiln" = bears on a pottery kiln. Dates are the bulletins' (periphery.md key; checked on the pages where
printed).

| PDF | Bulletin (cat. no., date) | Graph, diagram, photo, sidebar | Kiln? |
|---|---|---|---|
| 91–123 | Sections 5–6 (MP, BP) | No graph, diagram or photo; no box. One footnote, PDF 115 (data sheets are on a website) | Text only; first pass §5.1 covers it |
| 232–233 | Alumina-chrome brick | Product table | No (chrome) |
| 234, 237 | HW 192 (12/03) VERSAFLOW C and 2-TOUGH | Bar chart "Thermal Shock Resistance & 2000°F Hot MOR vs Wire Content" (PDF 234); impact-test sidebar (PDF 235); photos of cup tests | Yes, castable thermal shock (§2.1) |
| 235–236 | same | Photos, 2-TOUGH density table | Partly (castable) |
| 238–241 | HW 150 (5/04) Emisshield | Zone sketches (PDF 240), emissivity graph (PDF 241), photos with captions | Yes: coating, kiln-car skirts, tunnel-kiln preheat (§1) |
| 242–243 | HW 95 (1/04) EXCELERATE ABR PLUS | Photo; features list | Partly (phosphate monolithic) |
| 244–245 | HW 87R (5/04) extra-high alumina brick | Bar chart "Prism Spalling Test 2,200 °F With Water Quench" (PDF 244) | Partly: thermal shock of high-alumina brick (§2.2). KORUNDAL XD named for "ceramic kilns" |
| 246–247 | HW 91R (11/02) high-alumina brick 50–70 % | Photo; text only | Brick, table in periphery.md §3 |
| 248–249 | HW 99R (01/04) INSWOOL blanket | Photo; application list; k table (PDF 249, done) | Yes, fibre |
| 250–251 | HW 96 (05/04) INSWOOL modules | Photos of CSW and FQW modules; layout drawings | Yes, fibre |
| 252–253 | HW 102 (09/03) INSBOARD | Application tick matrix (PDF 252) | Yes (§3.1) |
| 254–257 | HW 97 (09/03), HW 98 (05/03) papers | Text and k tables (transcribed) | Yes, fibre paper (kiln-car deck covering) |
| 258–259 | HW 100 (9/02) ropes and braids | Photos | Yes, fibre seals |
| 260–261 | HW106 (8/02) INSWOOL PUMPABLE | Photo; property box | Yes, fibre |
| 262–263, 284–285, 318–319 | MAGSHOT | Photos; table with a conductivity word | No (magnesite) |
| 264–265 | HW 89R (4/04) superduty fireclay brick | Application tick matrix (PDF 264) | Yes (§3.2) |
| 266–267 | HW 105 (3/03) VIB-TECH shapes | Photos; list | Partly (fired shapes) |
| 268–273 | HW190 (6/03), HW 192 (07/03) aluminium furnaces and troughs | Photos; service-conditions text | No (aluminium contact), except castable numbers in periphery.md §5 |
| 274–275 | Long brick for rotary kilns | Drawings | No (rotary cement kiln) |
| 276–279 | HW132 R (7/03) bricks for rotary kilns | Kiln-system drawing (PDF 276), brick list | One line (§3.3) |
| 280–283 | HW139 (3/03) lightweight castables | k plots (PDF 280) | Yes; done in first pass (hwi-handbook.md §5.2) |
| 286–289 | HW135 (9/02) lime industry | Photos; precast lifter drawing (PDF 289) | No (lime kiln) |
| 290–297 | THOR AZS, TZ 352, VERSAFLOW 70 | Nose-ring joint drawings (PDF 292, 296) | No; anchors reference only |
| 298–299 | Mag-chrome brick | Table | No |
| 300–307 | HW115R (1/03), HW 122R (2/03) cupola, channel induction | Cutaway drawing (PDF 300), tables | No (iron melting); one line each |
| 308–313 | EAF, ladle, NARGON porous plugs | Photos, tables, PDF 312 has 113 images | No |
| 314–315 | HW 117R (2/03) cupola upper stack to melt zone | Zone drawing with callouts | One line (§3.3) |
| 316–317 | HW 104R (11/02) lime recovery kiln | Kiln-sections drawing, issues and solutions table | Partly: preheating zone "Alkali & Insulation" (§3.3) |
| 320–321 | HW94R (11/02) fluid catalytic cracking unit | Vessel drawing; service text | Partly: "Reducing environment" (§3.3) |
| 322–323 | HW170 (11/02) sulfur recovery unit thermal reactor | Cutaway drawing; brick and monolithic table; notes | Yes, layering (§3.3) |
| 324–325 | HW75R (12/03) ash hopper | Photo; severity table | No (power boiler) |
| 326–327 | Product / Application Update, boiler | Boiler section drawing (PDF 326), tick matrix of KAST-O-LITE, GREENLITE, INSWOOL and other products against boiler locations (PDF 327) | No (boiler); tick columns not resolved |
| 328 | CFB combustor | Loop drawing; text | No |
| 329–330 | RUBY SR/C slag dam | Photos | No (chrome-alumina) |

Not kiln, one line each: basic, magnesite and chrome brick (PDF 232–233, 262–263, 278, 284–285, 287, 298–299,
318–319); AOD, EAF and ladle steel service (298–299, 308–311); aluminium contact (268–273); the basic
zones of cement and lime kilns (278, 286–289, 316–317); porous plugs (312–313); FCCU erosion service
(320–321); cupola and channel-induction iron melting (300–307, 314–315); boiler, ash hopper and CFB
(324–328); slag dam block (329–330).

---

## 1. Emisshield (bulletin HW 150, 5/04, PDF 238–241)

All of it is the maker's of the coating (Wessex Incorporated) and carries no test method, substrate
description or source. Reported, not adopted.

### 1.1 The emissivity graph (PDF 241, "Metal", figure at lower left)

- Title: none; the y-axis is printed "Emissivty" (sic), 0 to 1.0; the x-axis "Temperature °F", 0 to 2500.
  Four curves, labelled on the plot. The page's text layer gives the tick labels; the curves are four
  Bézier paths 5 pt wide.
- Method: **Verified, graph, vector path.** The page is stored rotated by 270°, so coordinates were turned
  with `page.rotation_matrix` first. Axes were fitted to the tick labels' box centres (x: 0 to 2500 at 38.4 pt
  per 500 °F, checked at five labels; y: 0 to 1.0 at 25.5 pt per 0.2, checked at six labels). Each path was
  sampled at 60 points per segment and read at the temperatures below. The result was checked against a
  300 dpi render for colour and shape. The band is 5 pt wide, so the centre line is good to about ±0.01 on
  the axis fit and the label-centre position adds a possible x offset of about 2.6 pt (±35 °F), which matters
  only where a curve is steep (cold-rolled steel, 700–1700 °F, slope about 0.0003 per °F, so ±0.01).
  Total: **±0.02**.
- Every curve starts at the frame's left edge, which is about −35 °F on the label fit, so the "0 °F" values
  are read at the label position. Three curves end on the bottom frame line, which lies 0.04 below the "0"
  label. They are clipped there, so "reaches zero" means "leaves the plotted area".

| T, °F | Steel coated with Emisshield M-1 | Cold rolled steel | Zirconia on Inconnel (sic) | Aluminum alloy A3003 |
|---|---|---|---|---|
| 0 | 0.90 | 0.82 | 0.57 | 0.37 |
| 250 | 0.84 | 0.77 | 0.52 | 0.37 |
| 500 | 0.81 | 0.72 | 0.51 | 0.36 |
| 750 | 0.81 | 0.60 | 0.50 | 0.32 |
| 1000 | 0.82 | 0.48 | 0.50 | 0.19 |
| 1250 | 0.84 | 0.35 | 0.50 | 0.02 |
| 1500 | 0.90 | 0.18 | 0.49 | – |
| 1750 | 0.90 | 0.03 | – | – |
| 2000 | 0.91 | – | – | – |
| 2250 | 0.90 | – | – | – |

- Curve ends: M-1 at about 2465 °F (0.90); cold rolled steel leaves the plot at about 1860 °F (crosses 0
  at about 1800 °F); zirconia on Inconel ends at about 1660 °F (0.46); aluminium A3003 leaves the plot at
  about 1350 °F (crosses 0 at about 1280 °F).
- M-1's minimum is 0.805 at about 620 °F, and its curve has a visible kink at 1500 °F where it rises to 0.90.
- The first pass's values (periphery.md §10.1) agree within 0.03 at every point (cold rolled steel: first
  pass 0.83 at 0 °F, 0.78 at 250, 0.71 at 500, 0.51 at 1000, 0.16 at 1500; here 0.82, 0.77, 0.72, 0.48,
  0.18). The note's "about 0.83 at 0 °F and 0.71 at 500 °F" is confirmed to within the ±0.02.
- A physical oddity, not a reading error: the cold rolled steel and aluminium curves fall to zero emissivity.
  A real oxidising steel surface would not. The plot gives no atmosphere or surface condition.
- The curves are for **metal** substrates. There is no curve for a refractory, coated or uncoated, anywhere in
  the bulletin. The "refractory" figures are two drawn numbers (§1.2).

### 1.2 Other content, Read (PDF 238–240)

- PDF 240, zone sketches: a refractory without coating, "0.2-0.5" beside a conduction arrow; with a coating,
  "0.8-0.9". Text: "most refractories will steadily lose their ability to reradiate … At these high
  temperatures, refractories will only have an emissivity value of 0.2 to 0.5 depending on their
  composition." The temperature range is "above 3000°F" in the text, and the sketches give no temperature.
- PDF 239 (Read): "At a very low ∆T and in applications such as boilers and power generation units where the
  furnace atmosphere or load is hotter than the coating, Emisshield™ will increase the amount of heat
  conducted through the substrate." So the maker's own claim of "reduced conduction" holds only with a
  colder load. For a kiln wall, where the load is cooler than the hot face, the claim is that more heat
  goes back to the load. No quantity is given.
- Photo captions: PDF 240, "Emisshield™ coated brick (right) in a tunnel kiln preheat zone abut uncoated brick
  in firing zone". PDF 241, "Emisshield™ coated steel kiln car skirts resist oxidation and warping".
  The metal text lists "kiln car skirts" among applications.
- PDF 238: "maintains that value at temperatures up to 3000º F and beyond."

### 1.3 What it means for the engine

The engine radiates with the library's emissivities. This bulletin's only measured-looking data are metal
curves with no method. Three things it does show, as a reported range: bare cold-rolled steel at 0.82 to 0.72
over 0–500 °F (the shell's temperatures; the engine uses 0.6 for rolled sheet and 0.79 for oxidised steel,
`radiation-exchange.md`), a coated steel near 0.81–0.90, and a vendor's 0.2–0.5 for uncoated refractory
above 3000 °F, a temperature no kiln reaches. Not adopted.

---

## 2. Graphs and bar charts other than Emisshield

### 2.1 Castable thermal shock against wire-fibre content (bulletin HW 192, 12/03, PDF 234; the same page is repeated as PDF 237)

Title "Thermal Shock Resistance & 2000°F Hot MOR Vs Wire Content". Bars, two per x position: "Prism Spall
Cycles" (red) and "HMOR (PSI/100)" (blue). x: "% Wire Fiber" 0, 3, 6, 9, 12, 15, 18, 21, 36. y: 0–40, grid every
10. Caption: "Increasing Wire Fiber Content. After Firing to 2910°F". The product is not named; the chart is for
a coarse-aggregate castable family (VERSAFLOW C) with wire added. The test conditions of the prism spall
(quench temperature) are not printed on this chart. **Verified, graph by eye at 250 dpi, ±0.5 on the
chart's scale** (smallest grid division 10, bar edges read to about 5 px of 10.75 px per unit).

| % wire fibre | 0 | 3 | 6 | 9 | 12 | 15 | 18 | 21 | 36 |
|---|---|---|---|---|---|---|---|---|---|
| Prism spall cycles | 24.0 | 16.0 | 12.2 | 8.5 | 5.1 | 5.0 | 3.3 | 3.3 | 4.6 |
| HMOR at 2000 °F, psi (reading × 100) | 3180 | 2500 | 1780 | 1720 | 1240 | 1280 | 1610 | 1520 | 1070 |

The bulletin's point: adding wire fibre lowered both spalling cycles and hot MOR. Sidebar (PDF 235, Read from
the 75 dpi sheet): a ½-in projectile impact test on a sample heated to 2000 °F, VERSAFLOW C "survive close to 40
cycles … compared to traditional low cement castables which typically fail after 15 to 20 cycles".
For a kiln: a dense castable's hot MOR at 2000 °F of about 3000 psi (0 % fibre) is the only hot-strength
figure of a castable in Section 9 outside the tables (periphery.md §5: GREENKLEEN-60 3,800 at 1500 °F,
NARCOTUFF 4,650 at 1500 °F). It is for a low-cement, coarse-aggregate product, not for a pottery castable.

### 2.2 Prism spalling of extra-high alumina brick (bulletin HW 87R, 5/04, PDF 244)

Title "Prism Spalling Test 2,200°F With Water Quench", y "Cycles - To - Failure", 0–40. Bar labels include the
value (Read, text layer; bar heights agree on the image): KORUNDAL XD DM (5), KORUNDAL XD (10), TUFLINE 98 DM
(26), TUFLINE 90 (35), TUFLINE 95 DM (40+), TUFLINE 90 DM (40+). A note on the page: "Test concluded with
maximum of 40 cycles." Corundum and mullite-bonded 90 %+ brick; it bears on kiln furniture-grade
brick only as a measure of how the bond decides spalling. No fireclay or IFB spalling data in any bulletin.

### 2.3 k(T), hot MOR, expansion, creep, temperature profile

- k(T): only PDF 280 (done), and the blanket, board and paper tables (periphery.md §9). No k curve for fireclay
  brick, IFB, dense castable, mortar or plastic in Section 9. **Not found.**
- Hot MOR as a curve, expansion curve, creep curve, temperature-profile curve: **Not found** in PDF 232–330.
  The only expansion and creep figures are in Section 3 (first pass §2.2, §2.4).
- Shrinkage of INSBOARD, PUMPABLE: tables only (periphery.md §9.3, §9.4).

---

## 3. Tick matrices, application drawings, zone diagrams

### 3.1 INSBOARD application matrix (bulletin HW 102, 09/03, PDF 252)

Columns 2300LW, 2300HD, 2600, 3000. Verified on the 130 dpi clip (lower part) and the 75 dpi sheet (upper
part, so the upper rows are Read from the lower-resolution image):

| Application | 2300LW | 2300HD | 2600 | 3000 |
|---|---|---|---|---|
| Hot Face Linings for Ceramic Kilns & Petrochemical Furnaces | | | x | x |
| Hot Gas Duct Linings | x | x | x | x |
| Expansion Joint Material | x | x | | |
| Heat Shields for Personnel Protection | x | x | x | x |
| Pouring Forms for Castable | x | | | |
| Combustion Chambers | x | x | x | x |
| High Temperatures Dryers | x | x | x | x |
| Industrial Heat Shields | x | x | x | x |
| Flue & Chimney Linings / Kilns & Furnaces | x | x | x | x |
| High Temperature Muffles | x | x | x | |
| Heat Treating Furnaces | x | | | |

The upper rows (full-thickness linings, board over blanket, backup insulation, rigid gaskets) were not
re-read at higher resolution. They are in the 75 dpi sheet: full thickness linings under 2300HD, 2600 and
3000; board over blanket and refractory backup insulation under most columns. Treat them as Read-level, not
Verified. The ceramic-kiln hot-face row is the one that matters: only the 2600 and 3000 boards are ticked.
That fits the INSBOARD continuous limits (2600 and 3000 °F, periphery.md §9.3) but is not a test result.

### 3.2 Superduty fireclay application matrix (bulletin HW 89R, 4/04, PDF 264)

**Verified** (130 dpi clip). A dot marks the brand. Rows with a dot for any brand:

| Use | KX-99-BF | KX-99 | CLIPPER DP | ALAMO |
|---|---|---|---|---|
| Stacks | x | x | x | x |
| Boiler linings | x | x | x | x |
| Air heaters | x | x | x | x |
| Charcoal furnaces | x | x | | |
| Hot gas ducts | | | x | x |
| Rotary kilns | | | x | |
| Zinc galvanizing furnaces | x | x | | |
| Low temp incinerators | x | | x | |
| Blast furnace stoves; sidewalls | x | | | |
| Checkers | x | x | | |
| Oil heater division walls | x | x | | |
| Oil heater floors | x | x | x | x |
| Low temp metal ladles | x | | x | x |
| Floors around furnaces | | | x | x |
| Heat exchangers | x | | x | x |
| Cement preheaters | | | x | x |

"Ceramic kiln" is not a row. The matrix lists coarse-grain KX-99-BF and KX-99 (both high fired) for
checkers and charcoal furnaces, and regular-fired CLIPPER DP and ALAMO for floors and ducts. The text beside
it (Read): KX-99 and KX-99-BF "resistance to alkalies and carbon monoxide". A statement of intended use,
not a limit.

### 3.3 Application zone diagrams with lining callouts

Kiln-like content first. No thickness is printed in any callout, and the only temperatures are the zone
service temperatures below.

| PDF, bulletin | Zone or location | Product called for | Temperature or condition printed | Kiln-like? |
|---|---|---|---|---|
| 322, HW170 (11/02), sulfur recovery thermal reactor (Read, table checked on the image) | Burner throat, hot face | brick TUFLINE 98 DM; monolithic NOVACON 95 (most severe) | "Most Severe = Oxygen Enrichment (up to 3,000°F)"; "Severe = Higher Temperatures (2,400-2,700°F)"; "Less Severe = Lower Temperatures (2,000-2,400°F)" | Yes: burner block |
| same | Burner throat, back-up | brick G-3000 LI; monolithic KAST-O-LITE 30 LI G (most severe) | | Yes: IFB back-up |
| same | Combustion chamber, hot face | KORUNDAL XD, KORUNDAL XD DM, GREENAL-90; monolithic GREENPAK-90-P, GREENCAST-94 PLUS (severe); UFALA UCR, KRUZITE-70, NOVACON 95, GREENCAST-94(-GR) PLUS, GREENPAK-90-P (less severe) | | Yes: hot face |
| same | Combustion chamber, back-up | brick G-28 LI, G-3000 LI; monolithic KAST-O-LITE 30 LI G (severe), 26 LI G (less severe) | | Yes: IFB with insulating castable back-up |
| same | Checker wall; tube sheet | KORUNDAL XD, GREENAL-90, UFALA UCR; monolithic NOVACON 95, GREENCAST-94 PLUS | | Partly |
| 322 note 1 | Mortar | "Mortar for laying brick linings with KORUNDAL®, GREENAL and TUFLINE® SERIES BRICK, use KORUNDAL® BOND." | | Yes (mortar) |
| 314, HW 117R (2/03), cupola upper stack to melt zone (Read) | Charge zone | premium TUFLINE 90, UFALA XCR, UFALA; work-horse ALADIN 80, KRUZITE-70, KX-99 | "600 - 2000 °F Temperature"; abrasion from charging, thermal shock | No: cupola; but KX-99 is the dense fireclay named for a 600–2000 °F zone |
| 314 | Preheat zone | premium TUFLINE 90, GREENAL-80, ALADIN 85; work-horse ALADIN 80, KRUZITE-70, KX-99 | "2000 - 2400 °F Temperature"; "Thermal Shock Reduced" | No |
| 314 | Melt zone | premium KORUNDAL XD, TUFLINE 90, DV-38 | "2000 - 3200 °F Temperature"; metal corrosion | No |
| 314 | Upper stack | premium UFALA, KRUZITE-70, CLIPPER DP; work-horse KS-4V GR PLUS (castable "to 2600°F") | | No |
| 316, HW 104R (11/02), lime recovery kiln (Read) | Preheating | GREENLITE HS (IFB, "Alkali & Insulation"), CLIPPER DP | issue "Alkali & Insulation" | Partly: IFB against alkali |
| 316 | Chain; tumbler; burning zone; dam; nose | LO-ABRADE GR, MC-25 PLUS, PNEUCRETE BF ADTECH; VERSAFLOW 45 C ADTECH precast; UFALA, KRUZITE 70, MAGNEL, NOKROME; UFALA, VERSAFLOW 60 PLUS; NARPHOS 85P PLASTIC, VERSAFLOW 60 PLUS | issues: abrasion and impact; strength and stability; temperature and alkali | No |
| 320, HW94R (11/02), FCC (Read) | Regenerator and reactor walls | gun mixes GREENLITE-45L GR, KAST-O-LITE 26 LI G, 23 ES, HPV GUN MIX; spray PNEULITE SPRAY 26 | "Relatively mild", "Reducing environment", "Coking"; "Highest strength to density ratio" | Partly: a reducing-atmosphere insulating castable |
| 320 | Flue gas lines and seal pot | "Low iron, high strength castable providing volume stability with resistance to chemical attack" | "Thermal shock", "Chemical reaction" | Partly |
| 276, HW132 R (7/03), rotary kiln systems | Whole kiln drawing | list: CLIPPER DP (superduty); ARCO 50, KALA, ARCO 60, UFALA, KRUZITE-70, ALTEX 75B, ALADIN 80, CORAL BP; basic brick | no callouts | No (cement/lime) |
| 268, HW190 (6/03) | Aluminium furnace | text only; no zone diagram | "Temperature … leading to corundum formation" | No |
| 300, HW115R (1/03), cupola breast wall and trough | Cutaway with callouts (taphole, breast wall, well, bottom, front slagger and dam, runner) | plastics, rams, precast | "Temperature (2000°F - 3000°F)" | No |
| 324–325, HW75R (12/03), ash hopper | Severity table | VERSAFLOW 45, PNEUCRETE 45, LO-ABRADE GR PLUS, THERMAX products | Less severe / severe / most severe by impact and thermal shock | No |
| 326–327, boiler guide | Boiler drawing and tick matrix of products against locations (furnace walls, penthouse, ash hopper, ducts, burners "Tangential and Front Fired") | KAST-O-LITE 19-L, 22; GREENLITE 22, 45 L GR; INSWOOL PUMPABLE, INSBOARD 2300, HP BLANKET; others | tick-to-column mapping not resolved | No |
| 328, CFB | Loop drawing (cross-over duct, cyclone, combustor, loop seal) | KX-99 BF, KALA, NIKE 60 AR, GREFCON 70GR; phosphate plastics | "thermal cycling", "severe abrasion" | No |

Not shown in any callout: a car top, a door, a flue or stack lining of a kiln, a thickness, a hot-face to
cold-face temperature. The only drawing of a layered lining is the SRU table, which pairs a dense hot face
with IFB (G-28 LI, G-3000 LI) and an insulating gun mix (KAST-O-LITE 26 LI G, 30 LI G) behind it. This is a
sourced example of the dense-face-over-IFB-and-castable layering, in a reducing, 2000–3000 °F service. The
choice of the 26 LI G for the less severe (2000–2400 °F) and 30 LI G for the severe (2400–2700 °F) and most
severe cases follows each material's rating (26 LI G 2600 °F, 30 LI G 3000 °F, PDF 281–282) but is a
selection, not a rule.

---

## 4. Sidebars, features and photo notes of kiln interest

| Where | What | Status |
|---|---|---|
| HW 99R (01/04), PDF 248 | "there is no curing or dry out time when using INSWOOL® ceramic fiber blankets. These linings can be fired to peak operating temperature immediately after installation." Fibre "unaffected by most chemicals. The only exceptions are hydrofluoric and phosphoric acid." | Read (first pass has it) |
| HW 99R, PDF 248 | Typical uses: HP "Furnace Door Linings"; HTZ "Refractory and Ceramic Kilns"; blanket heading "Lower Heat Storage: Faster heat up and cool down … Reduces Fuel Consumption" | Read, from the 75 dpi sheet |
| HW 96 (05/04), PDF 250–251 | Module layouts: parquet for 2000 °F and less; soldier course for 2000–2150 °F with one batten strip, over 2150 °F a double strip; FQW folded module "no blind welds" | Read (first pass §9.2) |
| HW 98 (05/03), HW 97 (09/03), PDF 254–257 | Papers' uses include "Kiln Car Deck Covering" and "Ware Separator"; organic binder; k at mean temperatures | Read (first pass §9.4) |
| HW 106 (8/02), PDF 260 | PUMPABLE "dries to a firm, but compressible board-like consistency … suitable for expansion joints, and for filling contraction cracks"; "can generally be dried or put into heat containment service without preheating" | Read |
| HW 150 (5/04), PDF 240–241 | Tunnel-kiln preheat-zone coated brick; coated kiln-car skirts (§1.2) | Read |
| HW 192 (12/03), PDF 235 | Impact test at 2000 °F, ~40 cycles against 15–20 (§2.1) | Read, 75 dpi sheet |
| HW 87R (5/04), PDF 244 | KORUNDAL XD "is used in a wide range of applications including ferrous foundry, ceramic kilns, chemical processing units, and incinerators" | Read |
| HW 91R (11/02), PDF 246 | The text on the 50–70 % bricks stresses alkali: "Alkalies can be particularly harmful since they ultimately react with silica to form a low melting glass"; adding andalusite and a little phosphoric acid improves alkali resistance and load-bearing | Read, 75 dpi sheet |
| HW 139 (3/03), PDF 281–282 | KAST-O-LITE 23 LI and 26 LI: "low iron … to resist detrimental reducing furnace conditions"; "Low iron content minimizes destructive CO disintegration attack by reducing furnace atmospheres" (first pass periphery §1.6) | Read |
| HW 139 (3/03), PDF 280 | Title "Mean Temperature (Btu/Hr ft² F/in)" on the x-axis (sic; the k unit is in the wrong title) | Verified (first pass) |
| HW 135 (9/02), PDF 289 | Precast "lifters or tumblers" in a lime kiln "reduces the heat consumption and improves fuel efficiency". Cement/lime kiln. | Read |
| Sections 5–6, PDF 115 | Footnote: the data sheets are online ("www.hwr.com") and the book carries none for Section 6 products. | Read |

Sections 5–6 (PDF 91–123): every page has only a header rule, a "Click here for Technical Data Sheets or go
to www.hwr.com" line and the page label. No box, no caution, no photo and no drawing in the range. The first
pass's text covers them. One check: MP-12 and MP-18 give each castable's top temperature in the same words in
the 2005 text; nothing in the text is boxed apart from the headings.

---

## 5. The library against Section 9

The first pass compared KX-99, KAST-O-LITE 26 LI and 30 LI, Mizzou and INSWOOL (hwi-handbook.md §4.1,
§5.2–5.4). The graphs and boxes read here change none of them. What was checked again:

| Library entry (sheet date) | Bulletin | Result |
|---|---|---|
| `hard-firebrick-kx99` (6/12) | HW 89R (4/04), PDF 264–265, 315 | The 4/04 sheet values are in hwi-handbook.md §4.1 (143 lb/ft³, MOR 2,050, CCS 8,500). The cupola bulletin (HW 117R, 2/03) prints 143 lb/ft³, porosity 12.0 %, MOR 2,200 (periphery.md §2). Bulk density 142 vs 143 is **+0.7 %** (Derived, 143/142). The MOR moves 2,200 (2/03) to 2,050 (4/04) to 1,700 (6/12), a 23 % fall over nine years (Derived, 1 − 1700/2200). The matrix (§3.2) adds no number |
| `kast-o-lite-26-li-plus`, `kast-o-lite-30-li-plus` | HW139 (3/03), PDF 280–282 | Nothing new. k and density comparison stands (hwi-handbook.md §5.2). The 30 LI curve starts at 3.64 at 0 °F and is nearly flat to 750 °F (3.58 to 3.62), unlike the library's 5.6 at 400 °F, which is a 2019 value, not the 2003 curve (periphery.md §12) |
| IFB `ifb-jm*`, `ifb-k*` | G-28 LI and G-3000 LI listed in HW170 (11/02), PDF 322 | Only names and densities (periphery.md §4). No k; **Not found** |
| INSWOOL / Kaowool / Cerachem blankets | HW 99R (01/04), PDF 249 | Nothing new here. First pass §5.4 stands |
| PROMASIL-1100, Alsey, Norton, Kaolite | | Not in the handbook |
| Emissivity (`radiation-exchange.md`) | HW 150 (5/04), PDF 241 | §1.3. No library value changes |

---

## 6. Section 9 against Section 5 (2005 text)

Recorded as printed, no ruling. Sources: first pass periphery.md §13 (Read) plus what the images here show.

| Item | Section 5 (2005) | Section 9 bulletin | Note |
|---|---|---|---|
| INSWOOL HP blanket, maximum | MP-23 (PDF 113) "to 2400°F" | HW 99R (01/04), PDF 249: 2300 intermittent, 2150 continuous; PDF 248 "up to 2300 °F" | bulletin is newer in print, 2005 text says 2400 |
| INSWOOL HTZ blanket | MP-23 "2700°F" | PDF 249: 2600 intermittent, 2450 continuous | |
| INSWOOL HP modules, continuous | MP-23 2250 | HW 96 (05/04), PDF 251: "HP - 1500°F - 2150°F" blanket option | |
| INSWOOL line | MP-22 "1500° F to 3000° F" | PDF 248: line "up to 2600 °F" | 3000 °F is the INSBOARD 3000 grade only (HW 102, PDF 253) |
| MC-25 PLUS | MP-12 (PDF 102) "to 2250°F" | HW 104R (11/02), PDF 317: 2550 | |
| GREENKLEEN-60 PLUS MOR after 1500 °F | | HW190 PDF 270, HW104R 321: 2,000; HW 192 PDF 273: 5,000 | |
| INSBOARD grades | MP-22: "2300, 2600, and 3000"; HD in 2300, 2600, 2800, 3000 | HW 102 (09/03), PDF 253: 2300 LW, 2300 HD, 2600, 3000 (no 2800) | |
| MIZZOU, KAST-O-LITE versions | "PLUS" products | 2002–2004 brochures without "PLUS" | different versions, not a contradiction |

I did not find a contradiction between a Section 9 k, strength or expansion curve and a Section 3 curve, because
there is no such curve in Section 9.

---

## 7. What the engine can use

| Need | Finding | Status | Where it would go |
|---|---|---|---|
| Emissivity of a refractory hot face | Only a coating seller's "0.2–0.5" above 3000 °F; no curve for any refractory. Metal curves: cold rolled steel 0.82 at 0 °F, 0.72 at 500 °F, 0.48 at 1000 °F; M-1 coated steel 0.81 to 0.91 | Verified (graph, ±0.02); not adopted | `radiation-exchange.md` "not adopted" list; no code |
| Shell emissivity at 200–500 °F | Cold rolled steel 0.77 at 250 °F, 0.72 at 500 °F (vendor, no method) against the engine's 0.6 for rolled sheet | Verified (graph, ±0.02); not adopted | `radiation-exchange.md` note |
| Castable thermal-shock and hot strength with added wire | 0 % wire: 24 spall cycles, HMOR 3,180 psi at 2000 °F; both fall as wire rises (§2.1) | Verified (graph by eye, ±0.5 on the chart scale) | `castables.md` context; coarse-aggregate low-cement castable only |
| Layering of a hot face over IFB and insulating castable in a reducing 2000–3000 °F service | SRU thermal reactor: dense hot face, G-28 LI or G-3000 LI back-up, KAST-O-LITE 26 LI G or 30 LI G behind (§3.3) | Read, table checked on the image | Corroborates the layered-wall design; no thickness |
| IFB or castable for a reducing atmosphere | "low iron … to resist detrimental reducing furnace conditions" (23 LI, 26 LI), FCC regenerator walls "Reducing environment" | Read | `castables.md`, `materials.yaml` notes (the library already carries 26 LI and 30 LI) |
| Board for the hot face of a ceramic kiln | INSBOARD 2600 and 3000 only (HW 102, PDF 252) | Verified (clip) | `electric-and-thermal.md` §4 fibre note |
| Fibre needs no dry-out | HW 99R (01/04) | Read | Already in the first pass |
| Any new k(T), hot-MOR, expansion or creep curve for fireclay, IFB, dense castable | None in Section 9 | Not found | None |

---

## 8. Conflicts

- With the first pass (`hwi-handbook.md`, `periphery.md`): none of substance. The Emisshield readings
  differ from periphery.md §10.1 by up to 0.03 (cold rolled steel at 1000 °F 0.48 here against 0.51; at 1500 °F
  0.18 against 0.16; M-1 at 500 °F 0.81 against 0.82). Both are inside the stated ±. periphery.md's "reaches 0
  at ≈1850 °F" for cold rolled steel is the point where the path leaves the plot (≈1860); it crosses 0
  at ≈1800 °F. The M-1 curve has a kink at 1500 °F that periphery.md's 1500 °F value (0.90) sits on.
- With `materials.yaml`: none. No library value changes. The 30 LI discrepancy is already recorded (periphery.md §12).
- With the other research notes: none. `radiation-exchange.md`'s emissivity for rolled steel (0.6) is below the
  vendor's curve (0.72–0.77 at 250–500 °F); recorded in §1.3, not adopted.
- Inside the handbook: §6.

---

## 9. Not shown, not readable, skipped

- Not found: any k, expansion, creep or hot-MOR curve for fireclay brick, IFB, dense castable, mortar, plastic;
  any emissivity curve for a refractory or fibre; any lining thickness or temperature profile in a zone
  diagram; a car top, kiln door or kiln flue callout.
- Ambiguous: the Emisshield axis offset (labels against the frame, ±35 °F on x); the fall of two curves to
  zero emissivity; whether the prism-spall bars (PDF 234) are one test series with the 2000 °F hot MOR; the
  upper rows of the INSBOARD matrix (PDF 252) at 75 dpi only.
- Skipped, with reason: the tick columns of the boiler matrix (PDF 327; boiler service, not kiln); PDF 312
  (113 images, porous plugs); basic, chrome, magnesite pages; PDF 262, 318 MAGSHOT conductivity word
  (magnesite gun mix, no kiln use); the KAST-O-LITE and INSWOOL tables (first pass).
- Not re-checked on an image: the Section 9 INSWOOL, INSBOARD and paper tables (first pass checked them);
  the text of every zone callout except the SRU table (checked on the image) and the cupola and lime
  pages (checked on the 75 dpi sheet).
