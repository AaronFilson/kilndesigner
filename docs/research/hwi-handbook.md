# HarbisonWalker, *Handbook of Refractory Practice* (2005): a full reading

[HW05] Harbison-Walker Refractories Company, *Handbook of Refractory Practice*, © 2005, 331 PDF
pages (PDF metadata: PageMaker 7.0, made 2004-03-10, revised 2005-01-06). The owner's copy is
`docs/research/da86e4bd09a66be00c11a67957ff8e5a.pdf` (git-ignored), from
https://dl.icdst.org/pdfs/files/da86e4bd09a66be00c11a67957ff8e5a.pdf. Read in full on 2026-11-17:
the text layer of every page extracted with PyMuPDF, and every table and figure cited here checked
on the page image (rendered at 110–300 dpi) where the extracted columns could be out of order. A
second pass (2026-11-17/18, §9) read what a text layer loses: the graphs, drawings, photographs,
sidebars and the ring and arch tables, into four notes of their own.

The book is "© 2005 … All Rights Reserved", and its disclaimer says it "is for general
educational use only. It does not contain recommendations for any particular refractory for any
particular use." So the PDF stays out of git, as Olsen's scan does, and this note quotes short
passages and transcribes data only.

Cited by the handbook's printed page labels (PR-9, UR-24, IR-3 …), with the PDF page once where
it helps the next reader. Marks as in the other research files: **Verified** (read on the page
image), **Read** (text layer, unambiguous), **Derived** (arithmetic here), **Not found** (searched
across the whole text and absent).

What the handbook is: a maker's reference in nine sections. Section 1 is company history.
Section 2 (CR) covers the classes of refractory, Section 3 (PR) their properties and tests, and
Section 4 (UR) how to use them: expansion, heat flow, castables, walls and arches. Sections 5–6
(MP, BP) are the product lines, Section 7 (IR) the brick shapes, ring and arch tables and
anchors, and Section 8 (A) the appendix. Section 9 (L) is product and application bulletins of
2002–2004, the only pages with brand data sheets.

## How it relates to what the repo already holds

- **Same maker, same text: the *Brick Installation Guide*.** HWI's 2008 guide (`kiln-hardware.md`
  [S20]) reprints the handbook's Arch Construction (UR-22–UR-29), Brick Sizes and Shapes
  (IR-1–IR-5), Skewback Shapes (IR-11–IR-12) and Arch Combinations (IR-52 ff.). Every arch number
  the engine carries was compared cell by cell with UR-25–UR-27 and all are equal:
  `steel.yaml` `arch_constants` and `heated_factor`, and `kiln-hardware.md` §4.3's formulas,
  constants, W/H/F table and the 12 ft example. So the handbook confirms the transcription. It is
  not an independent second source: `kiln-hardware.md`'s "only 1 source" for the W, H, F and Hmax
  tables stands.
- **Later sheets of the same products.** The repo reads HWI's later product sheets: KX-99 6/12
  [B7], Kast-O-Lite 30 LI Plus 10/19, Mizzou Castable Plus 12/12, SAIRSET 8/10, M-2 12/17/13 and
  Schedule 4 12/17/13. The handbook's product data are the 2001–2004 versions. Where they differ,
  the library keeps the later sheet and the difference is recorded here (§4.1, §5).
- **It was the missing book.** `refractory-bearing.md` gap 8, `refractory-movement-and-mortar.md`
  §3 and `02-plan.md`'s fifth and sixth rounds list "HWI's 2005 Handbook" as not reached. It is
  now reached. On the questions those files asked of it (allowable bearing, hot strength) it is
  silent: §6.

---

## 1. What it settles

| # | Question, and where it was open | What the handbook gives | Now |
|---|---|---|---|
| 1 | Allowable bearing stress or factor of safety for refractory (`refractory-bearing.md` gaps 1–3; `02-plan.md`) | Nothing. The only stress limit in the book is for the steel binding (12,000 psi, UR-27). The only "safety factors" are on temperature: 100 °F under a castable's rating (UR-7) and 150–200 °F under an IFB's (BP-7) | **Not found**, now with the maker's handbook searched |
| 2 | Hot crushing strength or hot MOR of fireclay brick (Tobe hot; `refractory-bearing.md` gaps 6, 11) | Named as properties (PR-2) but given for no fireclay brick. Hot MOR appears only for high-alumina and castable products in Section 9 | **Not found.** Tobe no longer needs it: the owner (2026-11-17) has its hot strength inferred from the kiln standing (ADR 0017, decision 17 as amended) |
| 3 | C16's load and hold (`refractory-bearing.md` §B1.2, gap 9) | 25 lb/in² on two 9 in straights on end. For fireclay and high-alumina brick the top temperature is held 1½ h, then the furnace cools to 1830 °F or lower before the load comes off. Normal holds: high-duty 2460 °F, superduty 2640 °F (PR-7, PR-8) | 25 psi confirmed for dense brick. **Nothing on a 10 psi IFB load**, so gap 9 stays open |
| 4 | How hot dense fireclay is reported carrying 25 psi (Tobe hot, `11-17-26-inputs.md` §11) | Table 3.4 (PR-9): superduty 1.0–3.0 % subsidence after 2640 °F; high-duty and low-duty "Withstands load to <2640°F". HWI's own superduty brands (2004): 0.6–1.7 % at 2640 °F (§4.1) | Recorded (§2.2); the lower-bound rule's 25 psi now has the maker's handbook behind it |
| 5 | Whether a wall's cooler part may carry the load (Tobe hot's "heat-to-statics bridge") | "The wall should be bonded so that loads will be transferred to the cooler part of the wall when the inner, hotter portion loses its ability to carry them. Walls must be designed to carry structural loads at high temperatures." (UR-19) | A maker's statement of the principle the bridge rests on; no numbers. The owner (2026-11-17): the hot statics' uniform temperature through the brick "is just bad modeling" |
| 6 | The rise of a fireclay arch (`11-17-26-inputs.md` §11 says "the passage gives no fireclay figure") | "Typically, stable fireclay arches rise from 1½ to three inches per foot of span. High temperatures and soaking heat call for higher values." (UR-24, Verified on the image) | **Correction:** the passage does give one. The engine already has it (`steel.yaml` `rise_per_foot.dense_firebrick`, from the guide) |
| 7 | A silica brick's expansion allowance from a maker (`refractory-movement-and-mortar.md` §1.1, Not found) | 5/32 in per ft (1.30 cm/m) in high-temperature service. Silica walls take vertical expansion joints bottom to top, 10–16 ft apart (UR-4) | **Closed** |
| 8 | Expansion curves to 1300 °C+ by class (same §1.1) | Figs 3.3, 3.4 (PR-7), "approximate", to 2800 °F: fireclay, semi-silica, silica, 60–99 % alumina, SiC, zircon, chrome, magnesite, forsterite. Digitised every 200 °F in the second pass (§9.1) | **Closed** as curves (§2.4, §9.1). Not for IFB |
| 9 | Castable drying and first-heat shrinkage (same §1.1; `02-plan.md` sixth round) | Cement-bonded castables shrink at 400–600 °F (the cement decomposes) and above 1800–2000 °F (sintering). The permanent shrinkage after a first heat to 2600 °F is "commonly … on the order of 0.2 % to 1.5 %" (PR-7). Fig 3.5 (PR-8), digitised: −0.40 % fireclay, −0.60 % low-cement fireclay, −1.10 % 90 % alumina castable; Fig 3.6's plastics −0.15 to −0.33 % against the text's 0.2–0.6 % (§9.1). "Fireclay castables do not normally require an expansion allowance" (UR-5) | **Closed** as a band and three class curves (not per product) |
| 10 | The engine's 3/32 in/ft fireclay growth | 3/32 in per ft for superduty, high-duty and low-duty fireclay (UR-4). Fig 3.4's fireclay line ends at about 2380 °F at 0.76 % and reads 0.75 % at cone 10 (second pass, vector path, ±0.01 %; first read here as "about 0.7 % at 2400 °F"). 3/32 in/ft is 0.78 % | A fourth source, beside Olsen p.51, the IFB sheets and Brosnan; 3–5 % above the curve at cone 10 (§9.1) |
| 11 | A primary dry-out schedule from HWI (`castables.md` §8.2 and §13: "No HWI, Allied or Plibrico primary schedule found") | About 50 °F/h (30 °F/h for high-purity cement binders), holds at 250, 500 and 1000 °F, "one hour per inch of thickness for dense linings". Temperatures are of the gas, ½ in off the face; hold while it steams (UR-14) | **Found.** Slower than the engine's (§3.3) |
| 12 | How near its rating an IFB may run (`movement.py` `ifb_notes`: "no source says how near") | "Typically a 150 to 200 °F safety factor is used in selecting the appropriate brick" (BP-7) | **Found**, as a selection margin |
| 13 | A furnace-builder's temperature for concrete foundations (`concrete-foundations.md` C8: no kiln guide gives one) | Portland cement concrete "safely used for furnace foundations up to 700 °F"; at 900 °F "the concrete retains little mechanical strength"; above 700 °F a castable, or calcined fireclay aggregate. Ventilate under the furnace (UR-19) | **Found** (§3.5) |
| 14 | Wall height for a thickness (Olsen p.41, Giles c.1940; `kiln-reference.md`, `door-headers.md`) | 4½ in to 3 ft; 9 in 3–8 ft; 13½ in 8–12 ft; 18 in higher. Thicker when the unsupported length exceeds 1½ × the height; cylindrical walls with backing may be thinner (UR-21) | A third source, with two qualifiers the others lack |
| 15 | The quartz inversion's size (`castables.md` §13: "Disagree … No primary handbook read") | An abrupt volume increase of about 0.9 % at 1063 °F (573 °C), and about 3.2 % in all between 600 and 1100 °F. Cristobalite: 2.8 % in volume at 428–513 °F heating, 480–392 °F cooling (PR-18) | A primary source (§2.8) |
| 16 | Specific heat of any refractory (`materials.yaml` IFB entries are "excerpt") | Only the glossary's definition (A-20) | **Not found** |
| 17 | IFB emissivity above 1077 °C (`11-17-26-inputs.md` §13) | Only Emisshield's sales claim that at high temperature "refractories will only have an emissivity value of 0.2 to 0.5" (L, PDF p.240): unmeasured, from a coating seller. The bulletin's only graph (PDF 241) is of metals, with no refractory curve (§9.4) | **Not adopted**; the extrapolation stands |
| 18 | How Olsen's ring tables round a count (`rings.py`: "derived from the tables, not stated by them") | Olsen's Tables A-4 and A-5 are HW's ring tables (IR-26, IR-29). HW: "Fractional parts equal to or greater than one tenth of a brick were counted as an entire brick" (IR-25). `rings.ring` gives HW's total in all 485 rows of five ring tables to 12 ft (second pass, §9.3) | **Stated** by the tables' maker; the engine's rule is the same (§4.4, §9.3) |
| 19 | Anchors for castable linings (`combustion-and-masonry.md` §6.3: a vendor's post only; ceramic anchor spacing Not found) | Metal anchors where service doesn't exceed 2000 °F, length 0.8 × the lining, spacing by place and thickness. Metal limits: carbon steel 1000 °F, 304 1600, 309 1650, 310 1700. Ceramic anchors above 2000 °F, at 12 in in roofs and arches (IR-64, IR-65, IR-69) | **Found, as reference only.** The owner: most kiln castables need no anchors, and it depends on the material, so no requirement (§4.5) |
| 20 | Kast-O-Lite 26 LI: k ("excerpt" in the library) and strength (`refractory-bearing.md` §B2: Not found) | The 2003 version's k graph agrees with the library within 0.11 Btu·in/(ft²·h·°F); CCS 3,000 psi at 220 °F (bulletin HW139, 3/03) | **Corroborated** and found, for the earlier version (§5.2) |
| 21 | Fibre blanket k between makers (`electric-and-thermal.md` §4.3: Morgan and CNBM disagree at high temperature) | INSWOOL 8 lb runs about 10 % under Kaowool above 1000 °F (bulletin HW 99R, 01/04) | A third maker, nearer Morgan (§5.4) |
| 22 | A circle-brick table for a 4½ in round wall (`rings.py` and `kiln-reference.md`: Olsen's appendix has none; `blocked-items.md` §4) | IR-6 lists nine high-alumina circle brick, 24-33-3 to 120-129-3, 12 to 45 a ring. IR-30 tables the rings from 2'0" to 10'0" by the inch, 3 in brick only (second pass) | **Found** (§9.2, §9.3), beside HW's 1906 table (`blocked-items.md` §18) and A.P. Green's (`brick-shapes.md` p.117). Dome-brick tables stay not found |
| 23 | Fireclay growth below 2400 °F (`movement.py`: "No source read gives the curve below 2400 °F") | Fig 3.4's line: 0.33 % at 1000 °F, 0.59 % at 1800 °F, 0.71 % at 2200 °F, 0.75 % at cone 10 (second pass) | **Found** (§9.1) |

---

## 2. Properties of refractories (Section 3, PR-1–PR-27; PDF pp.33–59)

### 2.1 Cold strength (PR-2–PR-5)

- Cold crushing strength (ASTM C133): a 4½ × 4½ × 2½ or 3 in sample loaded on the 4½ × 4½ face;
  S = W/A. MOR: a 9 in straight on two supports, MOR = 3PL/2bd² (PR-3, PR-4). Read.
- "Room temperature (cold) strength measurements cannot be used directly to predict service
  performance" (PR-3). A fireclay or 50 % alumina brick strong when cold "will typically exhibit
  significantly reduced strength at elevated temperatures where the glassy phase may become quite
  soft or even fluid" (PR-2). Read.
- **Table 3.2, Physical Properties of Refractory Brick** (PR-5, PDF p.37). Verified on the image:

| Brick | Density, lb/ft³ | Apparent porosity | CCS, psi | MOR, psi |
|---|---|---|---|---|
| Superduty fireclay | 144–148 | 11–14 % | 1,800–3,000 | 700–1,000 |
| High-duty fireclay | 132–136 | 15–19 | 4,000–6,000 | 1,500–2,200 |
| Low-duty fireclay | 130–136 | 10–25 | 2,000–6,000 | 1,800–2,500 |
| 60 % alumina | 156–160 | 12–16 | 7,000–10,000 | 2,300–3,300 |
| 70 % alumina | 157–161 | 15–19 | 6,000–9,000 | 1,700–2,400 |
| Silica (superduty) | 111–115 | 20–24 | 4,000–6,000 | 600–1,000 |
| Silicon carbide | 160–166 | 13–17 | 9,000–12,000 | 3,000–5,000 |
| Zircon | 225–232 | 19.5–23.5 | 7,000–11,000 | 2,300–3,300 |

  Use with care. The table has an evident misprint: fused-cast magnesite-chrome prints CCS
  900–1,400 and MOR 6,000–8,000, swapped. And its superduty row doesn't match HWI's own superduty
  brands of 2004 (§4.1: 141–143 lb/ft³, CCS 4,000–8,500 psi, MOR 1,000–2,050 psi). The row looks
  older than the brands. Not for the library; class context only.

### 2.2 Load, creep and strength at temperature (PR-7–PR-9)

- "In service, refractory materials must support a load which, at its minimum, is equal to the
  weight of the lining above the reference point" (PR-7). Read.
- **ASTM C16** (PR-7, PR-8): "two 9-inch straight brick are set on end … and a vertical load of
  25 lb/in² is applied". "For fireclay and high-alumina brick, the maximum temperature is held for
  1½ hours, after which the furnace is allowed to cool by radiation to 1830 °F (1000 °C) or lower
  before the load is removed." Normal hold: high-duty 2460 °F (1350 °C), superduty 2640 °F
  (1450 °C). Improved high-duty checker brick are now tested at 2640 °F. High-alumina: 2640 °F
  for most classes, 2900 °F and 3200 °F for 90 %, mullite and corundum. Silica, basic and SiC brick
  hold until a temperature and then fail abruptly, so they are reported as "withstands load to"
  (PR-8). Read. No IFB load is mentioned anywhere in the book (searched for "10 psi", "10 lb",
  "insulating" near "load").
- **Table 3.4, Typical Results of Load Test … 25 lb/in²** (PR-9, PDF p.41), Read:

| Brick | Result |
|---|---|
| Superduty fireclay | 1.0–3.0 % subsidence after heating at 2640 °F |
| High-duty fireclay | Withstands load to <2640 °F |
| Low-duty fireclay | Withstands load to <2640 °F |
| 60 % alumina | 0.1–0.5 % subsidence at 2640 °F |
| 70 % alumina | 0.4–1.0 % at 2640 °F |
| 85 % alumina | 0.2–0.8 % at 2640 °F |
| 90 % alumina | 0.0–0.4 % at 3200 °F |
| Corundum | 0.1–1.0 % at 2900 °F |
| Silica (superduty) | Withstands load to 3060 °F |
| Silicon carbide | Withstands load to 2800 °F |
| Zircon | 0.1–0.8 % at 2900 °F |

- **Creep, ASTM C832** (PR-8, PR-9): "a constant vertical load, usually 25 psi, is applied to the
  1½" × 1½" faces of a specimen measuring 1½" × 1½" × 4½"". The peak expansion while heating is
  the thermal expansion under load (TEUL). The hold is "50 hours or longer", and creep is the
  subsidence between the 20th and 50th hours. Fig 3.7 gives 50–85 % alumina brick at 2600 °F,
  0–100 h; no fireclay creep curve. Read.
- What decides creep: "Formation of low viscosity glassy phases results in poor creep behavior,
  whereas well-formed crystalline bond phases give good creep behavior. … larger aggregate and
  lower porosity giving better creep resistance." (PR-9). Read.

### 2.3 Permanent changes on reheating (PR-5, PR-6)

- ASTM C113: heated to the test temperature and held 5 h; measured cold (PR-6). Read.
- High-duty fireclay at 2550 °F (1400 °C): "a slight (up to 1.5 %) linear contraction".
  Superduty at 2910 °F (1600 °C): "usually shrink 0.0 % to 1.0 % in length". "Some fireclay brick
  expand slightly in the reheat test, however, the expansion does not occur if the brick are in
  compression." 50–80 % alumina at 2910 °F: −2.0 to −2.5 % for some, +3.5 % or more for others
  (PR-6). Read.
- "The results of a short term reheat test may not be a sufficient basis for predicting the long
  term volume changes which a refractory may undergo in service" (PR-6). Read.

### 2.4 Reversible thermal expansion (PR-6, PR-7; Figs 3.3–3.6)

- Figs 3.3 and 3.4 (PDF p.39), "Approximate Reversible Thermal Expansion of Brick", in per cent and
  inches per foot, 0–2800 °F. They are "mean values" of the brands in each class (PR-7). Read
  off the 300 dpi image, about ±0.03 %:
  - **High-duty and superduty fireclay**: nearly straight, about **0.7 % at 2400 °F**, where the
    line ends. 3/32 in/ft is 0.78 % (Derived). *Second pass (§9.1): this reading was low. On the
    vector path the line ends at about 2380 °F at 0.76 % and reads 0.75 % at cone 10, ±0.01 %.*
  - Semi-silica fireclay: about 0.6 % by 1200 °F, then about 0.8 % at 2500 °F.
  - Zircon: about 0.65 % at 2600 °F. Chrome: about 1.4 % at 2700 °F.
  - Superduty silica: most of its 1.3 % comes below about 800 °F, then flat. Silica brick
    "undergo the greater part of their expansion below 800 °F (about 425 °C)" (PR-7).
- Unfired, cement-bonded refractories (Fig 3.5): shrinkage at 400–600 °F (205–315 °C) as the
  cement decomposes; more above 1800–2000 °F from sintering; "The shrinkages which take place
  during initial heat-up to 2600 °F (1430 °C) are permanent in nature and commonly are on the
  order of 0.2 % to 1.5 %." Plastics (Fig 3.6): linear to about 1900 °F, then contract;
  "Permanent shrinkages of 0.2 % to 0.6 % are common after initial heating to 2600 °F" (PR-7).
  Read; the figures' curves (fireclay, low-cement fireclay and 90 % alumina castables) were not
  digitised. *Second pass (§9.1): Figs 3.5 and 3.6 are on PR-8 (PDF 40), and are now digitised.*

### 2.5 Thermal conductivity (PR-9–PR-11)

- K-values are "reported at the mean temperature of the test brick" (PR-9). Porosity is
  "questionably the most important factor" for materials of like mineralogy; conductivity "may be
  altered in service by mineral changes … by vitrification … or by absorption of slags" (PR-9,
  PR-10). Read.
- **Table 3.5, K-Values for Refractory Brick at Various Mean Temperatures**, Btu·in/(ft²·h·°F)
  (PR-10, PDF p.42; the heading misprints ft³). Verified on the image:

| Brick | 600 °F | 1200 °F | 1500 °F | 1800 °F | 2200 °F | 2600 °F |
|---|---|---|---|---|---|---|
| Superduty fireclay | 9.8 | 9.9 | 10.2 | 10.5 | 11.4 | 12.8 |
| High-duty fireclay | 8.1 | 8.3 | 8.5 | 8.7 | 9.2 | 10.0 |
| 60 % alumina | 13.0 | 12.9 | 13.1 | 13.3 | 14.1 | 15.7 |
| 70 % alumina | 15.6 | 14.4 | 14.4 | 14.3 | 14.6 | 14.9 |
| 85 % alumina | 18.4 | 16.2 | 16.9 | 17.5 | 19.6 | 22.9 |
| 90 % alumina | 21.9 | 18.5 | 17.6 | 17.6 | 17.9 | 18.8 |
| Silica (superduty) | 9.0 | 10.1 | 11.0 | 11.8 | 13.5 | 16.1 |
| Silicon carbide | 121.2 | 112.0 | 107.5 | 103.0 | 97.0 | 94.6 |
| Zircon | 22.4 | 16.5 | 16.6 | 16.6 | 16.8 | 17.9 |

  Against the library (Derived): the superduty class agrees with `hard-firebrick-kx99`'s values
  (an "excerpt" of HWI's KX-99 sheet). At 1200 °F 9.9 against 10.0; at 1600 °F 10.3 by linear
  interpolation against 10.3; at 2000 °F 10.95 against 10.7 (+2.3 %). The high-duty class runs
  3–8 % under the library's Alsey Jet D.P. (8.1 against 8.35 at 600 °F; 8.3 against 9.0 at
  1200 °F; 9.2 against 9.65 at 2200 °F; the Jet D.P. values interpolated). Same maker, a
  different document: it corroborates KX-99's curve and extends a superduty curve to 2600 °F
  (12.8). But it is a class mean, not KX-99's own test.
- **Gases in the pores** (PR-10, PR-11): hydrogen's conductivity is about seven times air's. In
  100 % hydrogen "the heat flow through an insulating firebrick … would be two to two and
  one-half times as great as in an atmosphere of air", almost in proportion at lower
  concentrations. Relative to air: nitrogen 100 %, CO 97 %, CO₂ about 59 %. Read. For a kiln
  (Derived, proportional): at x % H₂ in the pores an IFB wall's loss rises by about 1–1.5 × x %.
  The H₂ in a reducing kiln's atmosphere isn't sourced here, and the engine models none of it.

### 2.6 Spalling (PR-11, PR-12)

- Thermal spalling is least in brick with "the lowest average rate of thermal expansion, high
  tensile strength", and least destructive in brick with high conductivity. "Relatively porous,
  light-duty fireclay brick are usually more resistant to spalling than denser, hard-burned
  brick" (PR-11). Read.
- **Pinch spalling** "is often observed in sprung brick arches because the hot ends of the brick
  expand more than the cold ends. This condition is aggravated by rapid heating … Insulation
  decreases the temperature gradient through a roof arch and tends to somewhat reduce pinch
  spalling." Mechanical spalling also follows "rapid drying of wet brickwork, inadequate provision
  for thermal expansion, or pinching of hot ends of brick, especially in furnace arches" (PR-11).
  Read.
- Silica brick can be "heated or cooled quite rapidly as long as they remain above the inversion
  temperature of about 1200 °F (650 °C)" (PR-11). Monolithics resist thermal spalling better than
  fired brick and mechanical spalling worse (PR-12). Read.

### 2.7 Pyrometric cone equivalents (PR-5, PR-6; Table 3.3)

| Brick | Minimum PCE (C24) | Typical PCE |
|---|---|---|
| Superduty fireclay | 33 | 33 to 34 |
| High-duty | 31½ | 31½ to 33 |
| Medium-duty | 29 | 29 to 31 |
| Low-duty | 15 | 15 to 27 |
| Semi-silica | – | 27 to 31 |
| 50 % alumina | 34 | 35 |
| 60 % alumina | 35 | 36 to 37 |
| 70 % alumina | 36 | 37 to 38 |

Verified on the image. "The PCE does not indicate a definite melting point" (PR-5). The minima
match ASTM C27 (`refractory-bearing.md` §B1.3).

### 2.8 Mineralogy (PR-13–PR-27), the parts a kiln touches

- Fireclay on heating (PR-17), Read. Kaolinite dehydrates at about 750–980 °F (400–525 °C),
  endothermic. Metakaolin turns to a spinel-type phase at about 1700 °F (925 °C), exothermic.
  Mullite and cristobalite form from 1920–2010 °F (1050–1100 °C). "A very small amount of potash
  is sufficient to lower the temperature of initial liquid formation to 1805 °F (985 °C)", a
  liquid "so viscous that it behaves essentially as if it were a solid" over a wide range above
  that. Fired fireclay brick are mullite, cristobalite (some quartz) and glass. "Super duty
  fireclay brick usually contain less glass than do brick of the high-duty class."
- Silica minerals (PR-18), Read:
  - Low to high quartz at about 1063 °F (573 °C): "an abrupt volume increase of approximately
    0.9 percent on heating, and a corresponding shrinkage on cooling. However, the total
    reversible expansion which occurs between 600 °F (316 °C) and 1100 °F (593 °C) is about 3.2
    percent." 0.9 % by volume is about 0.3 % linear (Derived, ÷ 3).
  - Cristobalite's inversion: about 428–513 °F (220–267 °C) heating, 480–392 °F (249–200 °C)
    cooling, "a volume change of about 2.8 percent"; bodies rich in it "tend to crack or spall if
    heated or cooled rapidly through the inversion range".
  - Quartz begins to turn to cristobalite at about 2280 °F (1250 °C), complete in about an hour
    at 2900 °F. Quartz to cristobalite is +14.3 % in volume, quartz to tridymite +17.2 %.
    Specific gravities: quartz 2.65, cristobalite 2.32, tridymite 2.26.
- What it means for the engine (Derived). `castable.py` uses 573 °C only as a temperature; its
  comment's "0.45 % linear" comes from Wikipedia. HWI is a primary source for both the
  temperature and the size: 0.9 % by volume abrupt, 3.2 % over 316–593 °C. The other values in
  `castables.md` §3 sit around these: [S25]'s 0.4 % by volume is under HWI's step, and [S75]'s
  4 % by volume over 200–575 °C is near HWI's total.

---

## 3. Using refractories (Section 4, UR-1–UR-29; PDF pp.61–89)

### 3.1 Expansion and its allowance (UR-4, UR-5)

- "Walls must be allowed to expand freely upward, and joints must permit the horizontal expansion
  required by the refractories. … Too little will cause pinch spalling; too much may weaken the
  wall or roof unnecessarily." (UR-4). Read.
- **Thermal Expansion of Refractory Brick in High Temperature Service**, approximate expansion
  (UR-4, PDF p.64). Verified on the image; the braces group the rows:

| Brick | Per foot | Per metre |
|---|---|---|
| Fireclay: superduty, high-duty, low-duty | 3/32 in | 0.76 cm |
| High-alumina: 60, 70 and 85 % classes | 3/32 in | 0.76 cm |
| 90 % alumina | 1/8 in | 1.04 cm |
| Corundum | 5/32 in | 1.30 cm |
| Silica | 5/32 in | 1.30 cm |
| Silicon carbide; zircon | 3/32 in | 0.76 cm |
| Magnesite, fired; magnesite-chrome, fired | 1/4 in | 2.08 cm |

  3/32 in/ft is 0.78 cm/m, not the printed 0.76 (Derived). The engine's 3/32 in/ft fireclay growth
  now has four sources: Olsen p.51, the IFB sheets, Brosnan and HWI.
- **Where the joints go** (UR-4), Read:
  - Heat-setting mortar: vertical expansion joints "can be staggered". Air-setting mortar:
    "expansion joints must be lined up vertically from course to course. Brick required to move
    with respect to each other as the refractory expands should not be laid with air-setting
    mortar."
  - Fireclay boiler settings with walls of 15 ft or more: joints staggered 4–6 ft apart. Low walls
    may space them "somewhat farther apart". Tunnel kilns: 10–15 ft in the hot section, 15–20 ft
    in the cool.
  - Silica walls: joints bottom to top, 10–16 ft apart. Basic brick: laid dry with gaps, or with
    paper or card in the joints.
- **Castables** (UR-5), Read: "Fireclay castables do not normally require an expansion allowance".
  "Certain dense, highly refractory castables have substantial reversible thermal expansion up to
  2000 °F (993 °C) or more" and may need one "in massive installations". Construction joints
  control drying shrinkage, and expansion joints are built the same way with compressible
  material in them. "When construction joints are required, anchors should remain halfway between
  them. Anchor tines should be 2 to 3 inches from the joint. … No anchors should be located at
  any joint." Four joint drawings: single linings of 5 in or less and of 5 in or more, and double
  linings each way.

### 3.2 Heat flow through a wall (UR-6–UR-8)

- Method (UR-6): one-dimensional steady flow, after "A.S.T.M. Proposal P142, Proposed Procedure
  for Calculating Heat Losses Through Furnace Walls". Q_L = (T_i − T_o)/R_T with R_T = Σ L_j/K_j.
  The surface balance is Q_L = Q_r + Q_nc (or Q_fc). K is re-evaluated at each component's
  temperature on every iteration, and a component whose k(T) isn't near straight is subdivided
  (UR-7). The hot face is taken as the gas temperature: "the difference is typically too small to
  warrant the complex calculation" (UR-6). Read. The engine's `thermal/wall.py` does this, with
  k(T) integrated exactly.
- Surface equations (UR-6, UR-7), Read:
  - Radiation: Q_r = F·ε·(T_o⁴ − T_a⁴), F = 1.74 × 10⁻⁹ Btu/(ft²·h·°R⁴) (5.67 × 10⁻⁸ W/(m²·K⁴)).
    **Misprint:** σ is 1.712 × 10⁻⁹ in those units (Derived from 5.670374 × 10⁻⁸), so HWI's
    English constant is 1.6 % high. The metric one is right.
  - Natural convection: Q_nc = 0.53·C·(1/T_avg)^0.18·(T_o − T_a)^1.27, with C = 1.39 for a vertical
    wall and 1.79 for a crown; T_avg is the mean of surface and air, °R. Its form and constants
    look like Heilman's (1929) flat-surface correlation, with (1/24)^0.2 = 0.53 (Derived). That
    identification wasn't checked against Heilman's paper here, and HWI names no source.
  - Forced convection: Q_fc = (1 + 0.225V)(T_o − T_a), V in ft/s.
- Worked examples (UR-7, UR-8), Read:
  - **Example 1:** 6 in of 60 % alumina brick (UFALA), 2½ in of 2300 °F IFB and a ¼ in steel
    shell. Hot face 2700 °F, air 70 °F, still air, ε 0.9. Result: shell 402 °F, 1099 Btu/(ft²·h)
    (3465 W/m²). The iteration table prints Q_r 741 and Q_nc 361 at 402 °F.
  - Example 3, the shell painted with aluminium (ε 0.30): 1055 Btu/(ft²·h), shell 547 °F.
  - Example 4, forced air at 10 ft/s: 1128 Btu/(ft²·h), shell 297 °F.
  - Example 2: 6 in of tabular alumina castable and 2–5 in of 2200 °F lightweight castable, hot
    face 2500 °F, air 100 °F, ε 0.85. The insulation's thickness sets its interface temperature,
    1980–2250 °F: "it is common practice to allow a 100 °F (38 °C) safety factor", so 2½–3 in is
    chosen.
  - Example 5: a cylinder of 6 in fused silica castable and a ¼ in shell at 2000 °F. Inside
    diameter 0.5, 1, 2, 4, 8 and 16 ft gives shell 435–538 °F and flux 1240–1900 against a flat
    wall's 545 °F and 1950. The table's unit is misprinted "BTU/hr-°F".
  - Two more misprints on UR-8 (Verified on the image), for anyone copying the page into a test:
    - The iteration table's 401 °F row prints Q_nc **660**. HWI's own equation gives 359.6 there,
      between 358 at 400 °F and 361 at 402 °F (Derived).
    - The cylinder's formula prints Q_L = (T_i − T_o)/r_o Σ(L_j/K_j)(ln(r_jo/r_ji)). The radial
      form has no L_j: Q_L = (T_i − T_o)/[r_o Σ ln(r_jo/r_ji)/K_j] (standard conduction; with
      the L_j the units don't balance).
- **Checked against the engine** (2026-11-17, `scratch/hwi/surface_check.py` and
  `example1_wall.py`), Derived:
  - At Example 1's surface state (402 °F, 70 °F, ε 0.9), HWI's equations give Q_r 740 and Q_nc
    361. The engine's radiation gives 728: the 1.6 % is HWI's σ.
  - The engine's Churchill–Chu gives 395 on a vertical face 1 m tall and 382 at 2 m: 6–9 % more
    convection than Heilman for kiln-sized walls (+15 % at 0.5 m). Lloyd–Moran gives 501 against
    Heilman's crown 465 (+8 %). The total surface loss on a 1 m wall is within 2 %.
  - The whole of Example 1 through `solve_wall` uses Table 3.5's 60 % alumina class for UFALA
    and the library's K-23 for HWI's unprinted "2300 °F IFB". It gives 1020 Btu/(ft²·h) and a
    shell of 382–386 °F, 7 % under HWI. HWI's own surface equations on the same wall give the same
    1020 and 387 °F. So the gap is the IFB's k, not the surface model. HWI's R_T of 2.09 implies
    an IFB roughly 10–15 % more conductive than K-23 (Derived, by mean temperatures). Example 1
    can't be a whole-wall test without that k, but it is a sourced check of the surface model.

### 3.3 Castables: mixing, curing, dry-out (UR-9–UR-14)

- Mixing (UR-9, UR-10), Read. Use a paddle mixer and drinking water. Dense castables are mixed
  "never … less than 2 to 3 minutes"; lightweight 2–3 minutes and not over-mixed. Cast within
  30 min of mixing (15 min for high-purity calcium-aluminate cements). The mix should be 60–80 °F,
  and never over 100 °F. The "ball-in-hand" test: tossed 6–12 in, a ball holds the hand's shape.
  "Decreased castable strength results from excess moisture." Forms are oiled; "Extended
  vibration will segregate the components". Use alternate bays.
- Curing (UR-10, UR-11), Read. Mix and cast at 60–80 °F. In cold weather (under 50 °F) mix and
  install at 50–80 °F. "Seventy to eighty percent of the cement's strength should be developed
  after the 24-hour cure". After the 24 h cure, under ideal conditions, the lining "may be air
  dried indefinitely before heat is applied". A lining left idle in long cold spells is held at
  250–300 °F. Curing compound keeps the surface from drying early. Shelf life is about one year
  for conventional castables.
- **Dry-out** (UR-14, PDF p.74), Read:
  - Free water leaves "as steam at around 212 °F", water of hydration "between 400 °F (204 °C)
    and 1200 °F (649 °C)", and sintering comes at 1600–2500 °F.
  - "Initial firing rates typically raise the temperature at about 50 °F (28 °C) per hour. For
    high strength, high purity cement binders, the rate is 30 °F (17 °C) per hour. Normally, holds
    are incorporated at 250 °F (121 °C), 500 °F (260 °C) and 1000 °F (538 °C). … As a rule of
    thumb to determine the time period, use one hour per inch of thickness for dense linings."
  - Temperatures "are the temperatures of the hot gases in contact with the castable … not the
    lining itself", with thermocouples ½ in from the surface. Hold while it steams, avoid flame
    impingement, and "no one dry-out schedule can be advised to fit all uses".
- **Against the engine** (Derived). `castable.py` uses Mizzou's schedule via High Temp Tools
  (`castables.md` §8.2 [S41], secondary): 75 °F/h, holds of ½ h per inch at the same three
  temperatures, layers up to 9 in. HWI's handbook is the maker's own, and slower: 50 °F/h and
  1 h per inch, with no thickness cap stated. For a 4 in dense layer, ambient (70 °F) to 1000 °F:
  the engine's schedule takes 930/75 + 3 × 2 = 18.4 h, HWI's 930/50 + 3 × 4 = 30.6 h. HWI's own
  later Schedule 4 for PLUS-rated lightweight castables (`castables.md` §14.2) is 100 °F/h to
  1200 °F with one hold of 1 h per inch: the maker's schedules differ by product.

### 3.4 Plastics and ramming mixes (UR-15–UR-18)

In case a design ever rams a plastic or ram-mix skin wall (Olsen's 4½ in ram-mix skin, p.42,
`kiln-reference.md`). Read:
- Plastics: anchors are ceramic. Construction joints are scored "approximately 2 inches deep on
  36-inch centers". Steam vents of ⅛–3/16 in rod go "on 8 or 12-inch centers" to two-thirds of the
  lining (UR-15).
- Schedule I, heat- and air-setting plastics (UR-17): ≤ 50 °F/h to 500 °F at the hot face, hold 1 h
  per inch; 50–75 °F/h to 1000 °F, hold 1 h per inch; then ≤ 100 °F/h. Schedule II, phosphate-bonded
  plastics: the same with a first hold at 250 °F.
- Ramming mixes (UR-18): ≤ 75 °F/h, hold at 500 °F at least 1 h per inch, then ≤ 100 °F/h.

### 3.5 Foundations, walls, joints (UR-19–UR-21)

- **Foundations** (UR-19, PDF p.79), Read:
  - "Under normal conditions, Portland cement concrete has been safely used for furnace
    foundations up to 700 °F (371 °C). When the temperature reaches 900 °F (483 °C), dehydration
    of the cement reaches a point where the concrete retains little mechanical strength."
  - Silica aggregate "will expand sufficiently at temperatures up to 1000 °F (538 °C) to set up
    stresses". Limestone or dolomite aggregate calcines a little hotter. "For temperatures above
    700 °F (371 °C), good practice points to the choice of a castable refractory for the
    foundation. Calcined fireclay, in sizes up to 1 inch, can be substituted for conventional
    aggregate."
  - "High temperature furnace operation also calls for ventilation in the lower courses of
    brickwork or the upper part of the foundation", with the furnace "on plates, girders or low
    brick piers, so that air circulates under the vessel. Sometimes, cross flues are formed in the
    top of the concrete foundation. At others, pipes, 3 inches in diameter or larger, are embedded
    in the foundation."
  - Against the engine: `foundation.py` warns when the platform's top face passes ACI 349's
    long-term 150 °F (200 °F local), a nuclear-structure code's limit (`concrete-foundations.md`
    C5). HWI's 700 °F is furnace practice, much looser. The two answer different questions: the
    concrete's long-term properties against the furnace builder's "safely used". HWI also sources
    the vented-platform option `02-plan.md` lists as "needing a source", but as a practice only:
    it gives no way to compute the heat the air carries off.
- **Walls** (UR-19–UR-21), Read:
  - "The wall should be bonded so that loads will be transferred to the cooler part of the wall
    when the inner, hotter portion loses its ability to carry them. Walls must be designed to carry
    structural loads at high temperatures." (UR-19)
  - Stretcher walls one brick thick "usually have the least structural stability". Header courses
    spall less at the hot face, and stretchers expose fewer joints. Three or four stretcher courses
    to a header let a 4½ in skin wall be tied on for repairs, but not "where stretcher courses may
    fall into the furnace". With "marked differences in rates of thermal expansion, the backup
    courses should not be tied to the inner courses". Bonding drawings (UR-20): 9–22½ in walls.
  - **Height**: "In unsupported straight walls, a 4½-inch thickness will carry heights up to 3
    feet; 9 inches will carry heights of 3 to 8 feet; 13½ inches, 8 to 12 feet; and 18 inches,
    walls higher than 12 feet. Walls with unsupported length more than one and one half times their
    heights should be somewhat thicker, and thermal spalling conditions may indicate additional
    thickness. Walls of cylindrical furnaces and stacks, with adequate backing, may be somewhat
    thinner for a given height than straight walls." (UR-21)
- **Joints** (UR-21), Read: "When there is no need for an especially strong bond, the brick are
  laid without mortar. In some cases, the fusion that takes place on the hot face will provide the
  bond required." "Brickwork laid with heat-setting mortars should have thin joints, either dipped
  or poured. The brick should be rubbed or tapped into place to produce as much brick-to-brick
  contact as possible. Joints made with an air-setting mortar generally can be somewhat thicker,
  but such joints should be completely filled." "Usually, vertical expansion allowances permit
  walls to move freely upward".
- **Counts** (UR-3, UR-21), Verified on the image (UR-21's copy; UR-3's text layer drops a row):

| Wall or floor thickness, in | 3 | 4½ | 6 | 7½ | 9 | 12 | 13½ | 18 | 27 |
|---|---|---|---|---|---|---|---|---|---|
| 9 × 4½ × 3 in straights per ft² | 3.6 | 5.3 | 7.2 | 8.9 | 10.7 | 14.2 | 16.0 | 21.4 | 32.1 |

  "Number of brick per cubic foot 14.2", which is 1728/121.5 (Derived). Every cell is
  thickness × 144/121.5, rounded (Derived), so the table can test a count without adding a number.
- **Mortar** (UR-3), Read. Pounds per 1000 9 × 4½ × 2½ in brick: dipped or thin joints 250–300;
  troweled 350–450, for SATANITE, HARWACO BOND, SAIRSET and SAIRBOND. PERIBOND 300–400 and
  500–600. "Minimum figures are used ordinarily for estimating". Larger brick take less "in
  proportion to the decrease in surface area". Ordering overage: 10 % for 1–100 shapes down to 1 %
  over 10,000. This brackets the engine's Olsen 300–400 and BNZ 200–400 (`round_masonry.py`).

### 3.6 Arches (UR-22–UR-29)

All of it is in `kiln-hardware.md` §4 from the 2008 guide, and the tables are equal (above). The
statements below are Read, and checked against what §4 records:
- Kinds (UR-22). Ring arches "require support at the end of the furnace to forestall outward
  displacement". Bonded arches are better for hot repairs. Ribbed arches put a longer brick in
  every third or fourth ring. Suspended arches carry less load, "and therefore, suffer less
  deformation at high temperatures". Monolithic arches: "Skews may be eliminated in monolithic
  arches, but design considerations remain the same as those for brick arches."
- Heating (UR-24): "Operation and thermal expansion tend to push the brick upward, opening joints
  at the top and pinching brick at the bottom. Brick that soften at operating temperatures may
  become permanently deformed, shortening the radius of the arc and increasing the rise. As the
  arch rises on heat-up, the line of thrust … shifts downward. As the line of thrust approaches a
  horizontal position in the arch, the horizontal force approaches its maximum value." Allowances:
  steel casings, paperboard that burns out, "In some cases, horizontal tie rods arc [are] spring
  loaded or manually adjusted". This is the same text as the guide's, not a new source for
  springs (`arch-springs.md`).
- Skewbacks (UR-24, UR-26). The note under the drawings: "A stretcher course should never be used
  immediately below the skewback." A built-up skew with the thrust line outside its support is "a
  construction to be avoided". Built-up skews suit "narrow spans, four feet or less". On a channel
  or angle "the line of thrust should pass through, or slightly above, the corner of the
  supporting steel."
- The 1¾ in/ft row of the heated table runs about 3 % above the engine's statics at T/S 7 % and
  8 % (printed 1.93 and 2.17, statics 1.87 and 2.11). Every printed cell is within 4 %, the largest
  at 1 in/ft, 7 % (+4.0 %) (`scratch/hwi/hmax_check.py`; `frame.heated_thrust_factor`'s own claim).
  No misprint found.
- Rings (UR-29): Formulas 1-a to 4-c for two-brick rings (straight and radial, or two radials).
  Formula 3-a reads "N_e c_e + N_f C_f = πD_g", with a lower-case c on brick E where the outside
  chord C_e is meant (Verified on the image). *Second pass (§9.2): formula 2-b is misprinted too,
  and the engine's ring is formula set 2.*
- Arch combination tables (IR-52): "no allowance was made for mortar or expansion joints or for
  size deviations", and "Fractional parts equal to or greater than one tenth of a brick were
  counted as an entire brick", so the counts "may be slightly in excess". Read.

### 3.7 First heat of a new brick furnace (UR-27)

"In most cases, a new furnace should be heated slowly with enough air circulating over the walls
to remove moisture. … Good practice permits a furnace to dry out thoroughly at a temperature not
over 250 °F (121 °C) for 24 hours or longer". "Temperatures above 400 °F to 600 °F (205 °C to
316 °C) should be avoided until all steaming ceases." Flame impingement during heat-up causes
spalling. "In low temperature furnaces, it is often good practice to heat the refractories to a
higher temperature than that required for operation for a short period of time. This preliminary
heat-up develops the ceramic bond in mortared joints." Read. Beside HWI M-2's "typically 100 °F
per hour" for brick and mortar (`refractory-movement-and-mortar.md` 2.5).

---

## 4. Brick products and installation references (Sections 6, 7)

### 4.1 Fireclay brick (BP-6) and HWI's superduty brands (L, Cat# HW 89R (4/04), PDF p.265)

- Five classes: super-duty, high-duty, semi-silica, medium-duty and low-duty, "about 18 % to 44 %
  alumina, and from 50 % to 80 % silica" (BP-6). Brands: EMPIRE S (high-duty); ALAMO, CLIPPER DP,
  KX-99, KX-99-BF (super-duty). Read.
- Superduty data, 2004 (Read: a single table whose text layer keeps its columns):

| | KX-99-BF | KX-99 | CLIPPER DP | ALAMO |
|---|---|---|---|---|
| Firing | high, coarse aggregate | high | regular | regular |
| Bulk density, lb/ft³ | 142 | 143 | 142 | 141 |
| Apparent porosity, % | 12.2 | 12.7 | 15.3 | 16.1 |
| MOR, psi | 1,950 | 2,050 | 1,350 | 1,000 |
| CCS, psi | 8,000 | 8,500 | 6,300 | 4,000 |
| PCE | 33–34 | 33–34 | 33–34 | 33–34 |
| PLC after 2910 °F, % | −0.3 | −0.4 | −0.3 | +0.5 |
| Hot load at 2640 °F, % subsidence | 0.7 | 0.6 | 1.3 | 1.7 |
| Al₂O₃ / SiO₂ / Fe₂O₃, % | 42.2 / 52.6 / 1.4 | 42.2 / 52.6 / 1.4 | 42.2 / 52.6 / 1.4 | 42.6 / 52.3 / 1.4 |

  "These results cannot be taken as minima or maxima for specification purposes."
- Against the library's `hard-firebrick-kx99`, from the 6/12 sheet [B7]: 142 lb/ft³, CCS
  5,000 psi, MOR 1,700 psi, hot load 0.6 % at 2640 °F. The 2004 sheet has 143, 8,500, 2,050 and
  0.6. Same product, eight years apart. Hot load and density agree; the cold strengths fell by
  41 % and 17 % (Derived). The library rightly keeps the newer sheet. The 2004 figures show how
  far a "typical" cold strength moves between printings, more reason not to treat CCS as an
  allowable.

### 4.2 Insulating brick (BP-7, PDF p.122)

Read:
- "ASTM classifies insulating fireclay brick (IFB) into groups 16, 20, 23, 26, and 28. The group
  number, multiplied by 100 represents the nominal maximum temperature to which the refractory can
  be exposed in service at the hot face. IFB's with temperature rating of 3000 °F are also
  available. **Typically a 150 to 200 °F safety factor is used in selecting the appropriate
  brick.** Special insulating refractories offering significantly higher strength than standard
  IFB's are also available. These can be used in applications requiring load bearing ability."
- Two cautions:
  - ASTM C155 says the group number "is not meant to specifically designate the maximum service
    temperature" (`refractory-bearing.md` §B1.4). The maker's handbook reads it as the nominal
    maximum anyway.
  - The last sentences imply, without saying it, that standard IFB are not chosen for load
    bearing. `refractory-bearing.md` §B4 found no maker saying IFB isn't load-bearing; this is
    the nearest yet, and still indirect.
- HWI's lines: G-Series IFB (low iron, five ratings from 2000 to 3000 °F), GREENLITE 27 (2700 °F,
  high strength), GREENLITE HS (2600 °F), LOTHERM RK, TUFLINE LW (99 % alumina), RUBY LW. Their
  data sheets are not in the handbook.

### 4.3 Brick sizes and shapes (IR-1–IR-5) and skewbacks (IR-11, IR-12)

- "The most widely used standard size for all types of refractory brick is 9 x 4½ by 3 inches"
  (IR-1). Read. Size tolerance (Standard Terms of Sale, A-22): "plus 2 % to minus 2 % on
  dimensions over 4'' and plus 3 % to minus 3 % on dimensions of 4'' or less", A.P. Green's rule
  in `brick-shapes.md` (p.104). A second maker agrees.
- IR-4's table (2½ in and 3 in series, with 9 in equivalents) matches `kiln-hardware.md` §5.1
  shape by shape. It repeats the guide's misprint of the 2½ in series' 2 in split as
  "9 × 4½ × 2½" (its 0.80 equivalent fits 2 in). It also fills four of §5.1's "not read" cells
  for the 3 in series: edge skew **0.80**, featheredge **0.63**, neck **0.73**, jamb **1.07**
  (Verified on the image, IR-4, PDF p.128). Every arch and wedge taper matches.
- IR-11 and IR-12 (PDF pp.135–136, Verified on the image) are the guide's pp.31–32, cut-out tables
  included. They print the same three dimensions `kiln-hardware.md` §5.4 found don't fit the arch
  formulas (60-9's 17/32 in toe, 74-9's 13/16 in toe, 56-9's 4¾ in height) and the same
  "1 13/18" on the 60-13½. The 2005 printing doesn't settle them: §5.4's rule stands (compute the
  profile from T and θ, and ask the maker before buying those three).
- **Dome brick** (IR-8, IR-9, PDF pp.132–133), Read. The only dome shapes in the book are
  electric-arc-furnace roof brick: a "two-shape, triple taper" arch-key-wedge pair for 9 in roofs,
  sold for spherical radii of 6 ft 6 in–7 ft 9 in up to 16 ft–22 ft 4 in (shapes HW-2721 to
  HW-2704, A and B), and also in 13½ in. Their dimensions aren't printed: the maker does the ring
  count from the roof's drawing. UR-21: "Combinations of these shapes taper in two dimensions to
  turn domes." A kiln dome's radius is mostly smaller than 6½ ft, and there is no table, so
  `blocked-items.md` §4 (dome and circle brick tables) stays **Not found**. `conical.py`'s
  builder-sized bricks remain the sourced route. *Second pass (§9.2, §9.3): that holds for dome
  brick only. Circle brick is in the handbook (IR-6's nine sizes, IR-30's ring table).*

### 4.4 Ring and arch tables (IR-25–IR-62)

- **Olsen's Tables A-4 and A-5 are HarbisonWalker's.** IR-26's "4½ in lining, 2½ in arch brick"
  table (PDF p.150) matches Olsen's Table A-4 (p.303, `kiln-reference.md`) row for row from 0'6"
  to 2'3": 19; 18 + 3; 17 + 5; … 31 + 15. IR-29's 3 in table (PDF p.153) holds Olsen's A-5
  (p.304). Its No.3 column runs 29, 28, 26, 25, 24, 23, 22, 21, 20, 19 … from 1'6", and starts
  lower, with No.4 arch brick. This confirms the five A-5 cells (1'11"–2'3") that are faint in the
  scan of Olsen. Read; the columns were traced through the text layer's order. *Second pass
  (§9.3), on the images: A-4 equals IR-26 in all 52 rows, and A-5 equals IR-29 in 65 of 66 (not at
  5'10").*
- **The rounding rule is printed.** "Fractional parts equal to or greater than one tenth of a brick
  were counted as an entire brick. … The number of brick required for a ring, as given in the
  tables, may be slightly in excess of the number actually required." Also: "no allowance was made
  for mortar or expansion joints or for size deviations of the brick" (IR-25 for rings, IR-52 for
  arches). `rings.py` rounds a ring's count down within 0.1 of a brick and up otherwise, which it
  calls "derived from the tables, not stated by them". It is stated, by the tables' maker, and the
  engine's rule is the same.
- The arch tables (IR-52–IR-62: 4½–18 in arches at 1.608 and 2.302 in/ft and others) are the
  guide's, which `kiln-hardware.md` §4.4 read for studio spans. Not re-transcribed. *Second pass
  (§9.3): IR-53 to IR-58 transcribed to 12 ft.*

### 4.5 Anchors (IR-63–IR-82; PDF pp.186–205)

Verified on the images of IR-64, IR-65 and IR-69 (PDF pp.187, 188, 192); the rest Read.
- **Metal (wire) anchors** (IR-64): "used for most anchor applications where the service
  temperatures do need exceed 2000°F(1904°C)". That is a misprint for "do not exceed 2000 °F
  (1093 °C)", as IR-69's ceramic rule shows.
  - "Length of wire anchors should be 0.8 times the thickness of the lining. This figure is
    generally rounded up to the nearest half-inch. For example, a 6-inch lining times 0.8 equals
    4.8 or 5 inches of anchor length."
  - Welded "in a square pattern, rotating the anchor tines 90° from neighboring anchors", with at
    least ½ in of fillet weld each side ("Tack welding is not enough").
  - More anchors at "Edges, roofs, nose, and areas where vibration, mechanical movement or gravity
    impose loads".
- **Wire and rod anchor spacing** (IR-64):

| Location | Lining, in | Centres, in |
|---|---|---|
| Walls, cylinders, slopes | 2–4 / 4–6 / 6–13½ | 6 / 9 / 12 |
| Overhead, roofs, bullnoses | 2–4 / 4–7 / 7–9 | 6 / 9 / 12 |
| Floors | 2–5 / 5–9 / 9+ | 9 / 15 / 24 |

  Anchors per ft² by spacing: 6 × 6 in, 4; 9 × 9, 1.8; 12 × 12, 1; 12 × 18, 0.67.
- **Metal limits** (IR-65, "Maximum Temp of Metallic Components °F"): carbon steel 1000, 304 SS
  1600, 309 SS 1650, 310 SS 1700. Hangers above ceramic anchors (IR-69): 330 alloy 1800 °F.
- **Ceramic anchors** (IR-69):
  - "Harbison-Walker ceramic anchors should be used in all installations where temperatures in the
    furnace will routinely exceed 2000°F (1094°C)." "The length of refractory anchors usually equals
    the lining thickness."
  - The metal hanger stays in the air: "Insulation placed over the cold face of the roof should not
    cover the anchor clip."
  - Spacing: vertical and circular walls 15, 18 and 24 in for linings of 9–12, 12–15 and 15+ in;
    "Roofs, noses and arches", 6 in or more, at 12 in.
- **Joints and seats.** UR-5: anchors "halfway between" construction joints, tines 2–3 in from a
  joint, none at a joint. IR-80: "Consider wall seats when using a dense monolith over 6 inches
  thick and /or 4 feet or more in height."
- **Against the repo.** `combustion-and-masonry.md` §6.3 had only a vendor's post: anchors about ⅔
  of the lining, tips 20–25 mm short of the hot face, tip limits of about 800 °C for 304 and
  1100 °C for 310. It listed ceramic anchor spacing as **Not found**.
  - HWI is the maker's own rule: 0.8 × the lining for wire anchors, and the ceramic spacing above.
  - Its metal limits are for the metal parts: 304 at 1600 °F (871 °C, Derived), 310 at 1700 °F
    (927 °C). They don't match the post's "tip" figures, which carry no source.
- **The owner (2026-11-17): reference only.** "Most castable used in kiln lining does not need
  anchors", and whether a lining does "will depend on the specific material". So the engine adds
  no anchor requirement, and none of the above is proposed for it. These are HWI's rules for
  industrial furnace linings, kept as reference: what a maker says when its own sheet for a
  castable calls for anchors.

---

## 5. Monolithics, fibre and the product bulletins (Sections 2, 5, 9)

Section 9 is bound-in bulletins of 2002–2004, each with its own catalogue number and date. The
2005 text of Section 5 already names the later "PLUS" versions, while most bulletin tables are for
the earlier versions. So every number below carries its bulletin's date, and the library's
2009–2019 sheets are later versions of the same names. Below is what bears on the engine. A
fuller catalogue of every product, with each row's page, is in `scratch/hwi/periphery.md`: working
notes, git-ignored, on the Windows clone only. Promote a product's rows from it, checked on the
image, if the product ever enters the library.

### 5.1 Classes and rules (CR, MP), Read

- **Fireclay brick** (CR-10, CR-11): five classes, about 18–44 % alumina. Superduty 40–44 %, its
  PCE "may not be less than 33"; high-duty not under 31½; medium-duty 29–31; low-duty 15 to 27–29;
  semi-silica 18–25 % alumina and 72–80 % silica. High-fired superduty is "practically inert to
  disintegration by carbon deposition in atmospheres containing carbon monoxide gas".
- **Insulating refractories** (CR-16):
  - Groups 16, 20, 23, 26, 28, 30 and 33: "These numbers multiplied by 100 represent the nominal
    service temperature in degrees Fahrenheit". 16–26 are on a fireclay base and 28–33 on a
    high-alumina base. HWI's own G-28 LI is 45 % Al₂O₃ (bulletin HW170, 11/02, PDF p.323).
  - "Typically, insulating refractories are used as backup materials, but they can also be used as
    working linings of furnaces where abrasion and wear by aggressive slag and molten metal are not a
    concern."
  - High-strength insulating brick on fireclay aggregate: "maximum service limit in the range of
    2100 °F to 2300 °F".
- **Mortars** (CR-17, MP-1, MP-2):
  - Heat-setting mortars "provide flexibility in expansion and contraction". Air-setting ones bond
    the wall "throughout, from the hot to the cold surface".
  - "The thermal expansion of the mortar should be approximately the same as that of the brick".
  - "Mortars which do not develop a strong bond are often desirable for use in laying brick walls
    which are alternately subjected to soaking heat and cooling cycles."
  - Air-setting fireclay mortars "are recommended for use in laying high-alumina brick in the 50 %
    to 70 % range, as well as insulating brick". Olsen's kits lay IFB in SAIRSET
    (`kiln-reference.md`, p.32).
  - Phosphate bonds need "Temperatures in excess of 700 °F" to resist rehydration. PHOXBOND needs
    500 °F at least for full strength. SAIRBOND (dry air-setting) is rated to 3000 °F.
- **Monolithics** (CR-19–CR-22):
  - Heat-setting monolithics bond fully only "with the use of a suitable insulating material as
    backup".
  - Ramming mixes are placed "in 1-1½ inch layers".
  - Fireclay castables serve "up to 2800 °F". 60–70 % alumina low-cement castables serve "up to
    3100 °F (1705 °C), such as kiln floors, doors, cartops".

### 5.2 Insulating castables: KAST-O-LITE (bulletin HW139, 3/03; PDF pp.280–282)

Verified on the images. The table (PDF p.282) and k graph (PDF p.280, read to ±0.05):

| | KAST-O-LITE 26 LI | KAST-O-LITE 30 LI |
|---|---|---|
| Maximum service | 2600 °F | 3000 °F |
| Bulk density, lb/ft³ | 92 | 95 |
| CCS / MOR at 220 °F, psi | 3,000 / 700 | 2,850 / 550 |
| PLC after 1500 °F | −0.2 % | −0.3 % |
| Al₂O₃ / SiO₂ / Fe₂O₃ / CaO, % | 46.5 / 38.2 / 1.3 / 10.5 | 57.5 / 35.5 / 0.7 / 4.2 |
| k at mean 0 / 500 / 1000 / 1500 / 2000 / 2500 °F, Btu·in/(ft²·h·°F) | 3.91 / 3.59 / 3.49 / 3.63 / 3.99 / 4.57 (ends about 4.74 at 2580 °F) | 3.64 / 3.58 / 3.70 / 3.99 / 4.43 / 4.99 (5.71 at 3000 °F) |

- 26 LI: "Low iron content minimizes destructive CO disintegration attack by reducing furnace
  atmospheres. … Lower water content for placement reduces internal steam pressure during initial
  heat up." The graph's axis title misprints the k units onto the temperature axis.
- **Against the library** (Derived):
  - `kast-o-lite-26-li-plus` (an "excerpt" of the 1/09 Plus sheet) gives 3.6, 3.4, 3.5, 3.7 and
    4.0 at 400–2000 °F. The 2003 curve gives about 3.65, 3.51, 3.52, 3.69 and 3.99 at the same
    points (interpolated on a 250 °F grid read off the graph), within 0.11, and its 92 lb/ft³ sits
    in the library's 90–100. The excerpt now has an
    HWI document beside it, though an earlier version of the product.
  - The 2003 CCS, 3,000 psi at 220 °F, is the first HWI strength for this product the repo has
    (`refractory-bearing.md` §B2: "NOT FOUND").
  - `kast-o-lite-30-li-plus` (the 10/19 sheet, verified) prints higher k than the 2003 30 LI:
    5.6 against about 3.58 at 400 °F, and 4.9 against 4.43 at 2000 °F. Density is 98 against 95.
    A different version: the library rightly keeps the 10/19 sheet.
- Not printed for any KAST-O-LITE or GREENLITE: the water to mix or the weight to place a ft³.

### 5.3 Dense castables (bulletin HW123R, 01/03; PDF p.311)

MIZZOU CASTABLE (the pre-Plus version): 3000 °F, "Quantity Required - Net" 139 lb/ft³. MOR
1,080 / 700 psi and CCS 5,000 / 3,000 psi after 230 / 1500 °F. 60.0 % Al₂O₃. Read. The library's
Mizzou Castable Plus (12/12) has 140 lb/ft³ required and CCS 5,500 / 3,500: close. Fireclay and
45 % alumina castables with densities and strengths (VERSAFLOW 45 C, ULTRA-GREEN 45, EXPRESS-30
PLUS and others) are in the catalogue; none is in the library.

### 5.4 Ceramic fibre (INSWOOL, INSBOARD)

- **INSWOOL blanket** (bulletin HW 99R, 01/04; PDF p.249, Verified on the image). Use limits,
  intermittent / continuous: HP 2300 / 2150 °F, HTZ 2600 / 2450 °F, CG 2000 / 1800 °F. k for HP and
  HTZ blanket, Btu·in/(ft²·h·°F); the sheet doesn't say whether the temperature is the mean or the
  hot face:

| Density | 600 °F | 800 °F | 1000 °F | 1200 °F | 1400 °F | 1600 °F |
|---|---|---|---|---|---|---|
| 4 lb/ft³ | 0.63 | 0.85 | 1.16 | 1.4 | 1.8 | 2.2 |
| 6 lb/ft³ | 0.56 | 0.73 | 0.97 | 1.2 | 1.55 | 1.85 |
| 8 lb/ft³ | 0.43 | 0.7 | 0.78 | 1.0 | 1.2 | 1.43 |

  Against the library (Derived): INSWOOL 8 lb runs about 10 % under Morgan's Kaowool 8 pcf above
  1000 °F (0.78 against 0.87 at 1000 °F; 1.43 against 1.58 at 1600 °F, Kaowool interpolated). It
  sits between Morgan and the CNBM blanket that `electric-and-thermal.md` §4.3 found 35–45 % lower,
  and nearer Morgan. That supports the engine's choice of Morgan's figures as the upper ones. The
  6 lb blankets agree within 8 %.
- **INSBOARD** (bulletin HW 102, 09/03; PDF p.253): each grade's "Recommended Use Limit" is
  200–300 °F under its continuous limit (2300 → 2100, 2600 → 2400, 3000 → 2700 °F). k is 0.6 at
  800 °F and 1.2 at 2000 °F for the 2300 and 2600 grades.
- **Rules**, Read:
  - "there is no curing or dry out time when using INSWOOL ceramic fiber blankets" (PDF p.248).
  - INSWOOL is unaffected by most chemicals; "The exceptions are phosphoric acid, hydrofluoric
    acid and strong alkalies" (MP-22). *Second pass (§9.4): the blanket bulletin of 01/04 names
    only the two acids (PDF 248).*
  - Modules: "DO NOT use for linings in contact with molten metal, abrasive, alkali laden, and high
    positive pressure conditions" (MP-23).
  - Module layout: parquet "For applications of 2000 °F and less"; soldier course "2000 °F to
    2150 °F use one batten strip - over 2150 °F use a double batten strip" (PDF p.251).
- The handbook contradicts itself on these products' limits. MP-23 says INSWOOL HP blanket "to
  2400 °F" against the bulletin's 2300 / 2150 °F, and HTZ "2700 °F" against 2600 / 2450 °F. Use the
  bulletin's table.

### 5.5 Other bulletin data

- **50–70 % alumina brick under C16's 25 psi at 2640 °F** (bulletin HW 91R, 11/02; PDF p.247): KALA
  0.3 %, UFALA 0.6 %, ARCO 60 1.2 %, KRUZITE-70 1.0 %, KALA SR 2.9 % subsidence. None is in the
  library.
- **Emisshield** (bulletin HW 150, 5/04; PDF pp.238–241): besides the claim in §1 row 17, a graph
  puts cold-rolled steel at about 0.83 at 0 °F and 0.71 at 500 °F. The engine's rolled steel sheet
  is 0.6. A coating seller's graph with no method: not adopted.

---

## 6. Not in the handbook (searched across all 331 pages)

- An allowable or working compressive or bearing stress for any refractory, cold or hot, or a
  factor of safety on CCS or on the C16 load.
- Hot crushing strength or hot MOR of any fireclay brick or IFB; creep (C832) of any fireclay
  brick or IFB; any IFB load test (10 psi or otherwise).
- Specific heat (or mean specific heat) of any refractory; emissivity data for any refractory
  (only the Emisshield claim, §1 row 17; Emisshield's graph is of metals only, §9.4).
- A measured rise or movement of a heated arch; any cone temperature table (only PCE by class).
- Thermal conductivity of any brick product, dense or insulating (only Table 3.5's class means), of
  HWI's IFB (G-series, GREENLITE) including Example 1's "2300 °F IFB", of GREENLITE castables or
  of Mizzou.
- The water to mix, or the weight to place a ft³, of any KAST-O-LITE or GREENLITE; reversible
  expansion of any castable product (Fig 3.5's three curves are unnamed class mixes, §9.1).
- In Section 9, any k, hot-MOR, expansion, creep or temperature-profile curve for fireclay brick,
  IFB, dense castable or fibre besides PDF 280's KAST-O-LITE k (second pass, §9.4).
- A dome-brick table for a kiln-size dome (only the electric-furnace roof shapes, IR-8, IR-9). Any
  arch table for 2½ in series brick, and any 2½ in key or circle-brick ring table (§9.3).
- A glass fraction or viscosity of fireclay brick at temperature, and any brick-life figure under
  alkali, lime or iron attack (§9.1).

---

## 7. What the engine can use

| Need | From the handbook | Status | Where it goes |
|---|---|---|---|
| A check on the surface model | Example 1's state: 402 °F, 70 °F, ε 0.9 gives Q_r 741, Q_nc 361 Btu/(ft²·h) | Read; the engine is within 2 % in total | A test of `thermal/surface.py` (proposal 4) |
| A check on brick counts | Straights per ft² by thickness (UR-21) | Verified | A test (proposal 4) |
| Fireclay growth to cone 10 | 3/32 in/ft (UR-4). Fig 3.4: 0.75 % at cone 10, 0.76 % at the line's end (about 2380 °F), and the curve below it (§9.1) | Verified (vector path) | A fourth source for `frame.py`'s and `movement.py`'s 3/32; proposal 16 |
| KX-99 k(T) | The superduty class, Table 3.5: within 2.5 % of the library's excerpt to 2000 °F; 11.4 at 2200 °F, 12.8 at 2600 °F | Verified (class mean) | Corroboration; extending KX-99's points with class data is proposal 5 |
| Expansion allowance by class | UR-4's table; joint spacing; air-set joints aligned | Verified / Read | `refractory-movement-and-mortar.md` |
| Castable first-heat shrinkage | 0.2–1.5 % to 2600 °F; Fig 3.5: −0.40 % fireclay, −0.60 % low-cement fireclay, −1.10 % 90 % alumina (§9.1); fireclay castables no allowance | Read; Verified (vector path) | `castables.md`; proposal 16 |
| Castable dry-out | 50 °F/h, holds at 250/500/1000 °F, 1 h per inch for dense linings | Read | Proposal 1 |
| IFB rating margin | 150–200 °F | Read | Proposal 2 |
| Concrete foundation | 700 °F safe, 900 °F little strength; vented foundations | Read | Proposal 3 |
| Wall height by thickness | 4½ in to 3 ft … 18 in above 12 ft, with the length and cylinder qualifiers | Read | A third source; proposal 6 |
| Steel binding | 12,000 psi (already used) | Read | No change |
| Quartz inversion | 0.9 % by volume at 573 °C; 3.2 % over 316–593 °C | Read | Proposal 7 |
| Anchors for a castable lining | Length, spacing, metal limits, the 2000 °F line for ceramic anchors | Verified | Reference only; no requirement (the owner, 2026-11-17) |
| Kast-O-Lite 26 LI k and CCS | The 2003 version: within 0.11 of the library's k; CCS 3,000 psi | Verified | Proposal 12 |
| Fibre and alkali | Modules not for "alkali laden" linings; strong alkalies excepted from INSWOOL's resistance (MP-22); the 01/04 blanket bulletin names only the two acids (§9.4) | Read | Proposal 11 |
| Ring counts as tests | `rings.ring`'s totals equal HW's in all 485 ring rows; splits within one brick; the straight region by UR-29's formula 1-a | Derived (§9.3) | Proposals 13, 15 |
| Arch course counts | IR-53 to IR-58, 538 rows to 12 ft; 20 misprinted rise or radius cells, no count | Verified (§9.3) | Proposal 13 |
| A 4½ in circle-brick ring | IR-30, 97 rows; N = π(D + 9)/9 by the 0.1 rule; IR-6's thin end 9 × ID/OD | Verified, Derived (§9.2, §9.3) | Proposal 14 |
| Growth of a 60–90 % alumina hot face | 0.84–1.00 % at cone 10 (Fig 3.3), above UR-4's 3/32 | Verified (vector path) | Proposal 16 |
| Geometry tests | A-2's circular segment and A-3's spherical cap; misprints in A-3 and A-6 | Derived (§9.1) | Proposal 17 |
| Skewback notes | UR-24's six drawings: the line of thrust through the steel's corner; one built-up construction "to be avoided"; headers under the skew | Verified (§9.2) | Proposal 19 |
| Board for a kiln's hot face | Only INSBOARD 2600 and 3000 are ticked for "Hot Face Linings for Ceramic Kilns" (HW 102, 09/03) | Verified (§9.4) | Information |

## 8. Proposals for the owner (nothing here is built)

1. **Dry-out.** Take HWI's handbook schedule for dense castables (50 °F/h; holds at 250, 500 and
   1000 °F of 1 h per inch), and Schedule 4 for PLUS lightweight castables, in place of the
   retailer's Mizzou schedule. Or show both and let the design choose. HWI states no 9 in cap; the
   engine's refusal past 9 in rests on the retailer's wording.
2. **IFB margin.** In `ifb_notes`, show HWI's "typically a 150 to 200 °F safety factor" beside the
   margin it already shows, as information, not a warning. The note's "no source says how near"
   becomes "HWI's handbook: 150–200 °F when selecting".
3. **Foundation.** Show HWI's 700 °F ("safely used") and 900 °F ("little mechanical strength")
   beside ACI 349's 150 °F in the platform's working. Cite UR-19 for the vented option (piers,
   cross flues, pipes of 3 in or more); it still needs a way to compute the air's heat.
4. **Tests.**
   - Example 1's surface point (radiation 741, convection 361, against `StillAirSurface`, about 2 %
     in total).
   - The straights-per-ft² row against the BOM's count.
   - Table 3.5's superduty row as a cross-check of `hard-firebrick-kx99` (within 2.5 % to 2000 °F).
5. **KX-99 above 2000 °F.** The library's points stop at 2000 °F. Adding the superduty class's
   11.4 (2200 °F) and 12.8 (2600 °F) would mix a class mean with a product's points. Keep it as
   it is, or add them flagged as class values: the owner's call.
6. **Walls.** A free-standing wall taller than UR-21's height for its thickness could get an
   information note, with the length qualifier. Three sources now give the rule (Olsen p.41,
   Giles, HWI), though Olsen's and HWI's wordings are near enough that one may come from the other.
7. **Quartz inversion.** Cite HWI PR-18 in `castable.py`'s comment in place of Wikipedia, and
   record its size as 0.9 % by volume, abrupt.
8. **Ring rounding.** `rings.py`'s docstring: its 0.1-brick rule is stated by HW (IR-25), whose
   tables Olsen's A-4 and A-5 reprint. A comment change; no number moves. (Second pass: the rule
   gives HW's total in all 485 rows; proposals 13, 15 and 18.)
9. **A brick kiln's first firing.** The engine advises a first firing only for castables
   (`castable.py`, `masonry.py`). A mortared brick kiln could get an information note from UR-27:
   dry out at no more than 250 °F for 24 h or longer, and stay under 400–600 °F until the steaming
   stops. HWI M-2's "typically 100 °F per hour" after that (`refractory-movement-and-mortar.md` 2.5).
10. **Anchors: not proposed.** The owner (2026-11-17): most castable used in kiln linings needs no
    anchors, and whether a lining does depends on the specific material. The engine adds no anchor
    requirement; HWI's rules stay in §4.5 as reference.
11. **Fibre in salt and soda kilns.** A design with `salt_ports` and fibre on a hot face could get an
    information note citing MP-22 and MP-23 (strong alkalies excepted; modules not for "alkali laden"
    linings). It flags a material fault, not a firing choice. The 01/04 blanket bulletin names only
    hydrofluoric and phosphoric acid (§9.4), so the note cites the 2005 text, not the bulletin.
12. **Kast-O-Lite 26 LI Plus.** Keep its k "excerpt" (the graph is the 2003 version's), but name the
    agreeing HWI graph in its source line.
13. **Ring and arch tests from HW's tables** (`hwi-ring-arch-tables.yaml`; eleven tests are listed in
    `hwi-ring-arch-tables.md` §4). The main ones:
    - `rings.ring`'s total against every HW ring row: 485 rows, all equal today.
    - The splits within one brick.
    - IR-30's totals by π(D + 9)/9.
    - Every arch row's rise and radius against the circle geometry, with the 20 misprinted cells
      marked.

    They sit beside the Olsen tests, which use HW's own tables reprinted.
14. **A circle-brick ring for 4½ in round walls.**
    - The brick named d-(d+9)-3: 9 in on the outside face, a thin end of 9d/(d+9).
    - Its count π(D + 9)/9 by the 0.1 rule, and neighbouring sizes mixed by the ring algebra.
    - Tested on IR-30 (and on A.P. Green p.117's totals).
    - HW lists the shape in high alumina only, and whether a fireclay circle brick is sold is not
      stated. A fourth choice beside the builder's mortar, cut and featheredge rings: the owner's call.
15. **`rings.py`'s straight region.**
    - Hold the tapered count at UR-29's formula 1-a, 2πL/(T − t), by the 0.1 rule, and let the
      straights make up the total. That is HW's rule (76, 113 and 227 tapered brick).
    - It reproduces every straight-region row of IR-26 and IR-29, where the engine is one brick off
      today.
    - A one-brick change; no total moves.
16. **Growth below cone 10, and other classes.**
    - Fig 3.4's fireclay curve could scale `movement.py`'s and `frame.py`'s 3/32 in/ft for a cooler
      firing (cone 6 reads 0.71–0.72 %, 8 % under), or 3/32 stays as the cautious figure.
    - If a 60–70 % alumina hot face is ever modelled, Fig 3.3 gives 0.84–0.86 % at cone 10.
    - Where a cast part has no measured shrinkage, Fig 3.5's permanent change (0.4, 0.6 and 1.1 %
      for the three classes) could be shown as context, labelled as one unnamed mix per class.
17. **Geometry tests from the Appendix.** A-2's circular segment for `geometry.segment_area`,
    `shape.segment_area` and `conical.segment_radius`; A-3's spherical cap for
    `round_masonry.cap_volume`. Copy neither A-3's stray cylinder line nor A-6's third frustum
    volume: both lack a ⅓.
18. **`rings.py`'s docstring.** Cite UR-29: the engine is formula set 2 (two tapers sharing the
    outside chord), whose printed 2-b is wrong twice; and set 1 in the straight region if proposal
    15 is taken.
19. **Skewback notes.** UR-24's drawings give `frame.py`'s skew notes a picture:
    - the line of thrust through, or slightly above, the corner of the supporting steel;
    - headers, not stretchers, under the skew;
    - the one built-up construction "to be avoided", whose thrust passes below its angle.

    Words only; no number.

---

## 9. Second pass: graphs, drawings and sidebars (2026-11-17/18)

Four readers took what a text layer loses, each into its own note. The coordinator then checked the
numbers that matter most to the engine on fresh renders (110–400 dpi). The key graphs it re-read with
its own script from the PDF's vector paths (§9.5). Section 3's graphs, the Appendix's figures and most
bulletin graphs are vector drawings, so their curves were read from the drawn coordinates, not by eye.

| Note | What it covers |
|---|---|
| `hwi-figures-properties.md` | Figs 3.1–3.7, the phase diagrams (PR-13–PR-27), Table 3.1, the Appendix (A-1–A-12) |
| `hwi-figures-using.md` | The drawings, photographs and boxes of UR-1–UR-29; the shapes of IR-1–IR-10 |
| `hwi-ring-arch-tables.md` and `.yaml` | IR-25–IR-62: 646 ring rows and 538 arch rows to 12 ft, against Olsen, `rings.py` and A.P. Green |
| `hwi-figures-literature.md` | Section 9's bulletins and Sections 5–6: graphs, zone diagrams, tick matrices, sidebars |

### 9.1 Properties and the Appendix (`hwi-figures-properties.md`)

- **Fireclay growth** (Fig 3.4, PR-7, PDF 39; Verified, vector path).
  - The high-duty and superduty line ends at about 2380 °F at 0.76 ± 0.01 %. It reads 0.75 % at
    cone 10, 0.71 % at 2200 °F, 0.59 % at 1800 °F and 0.33 % at 1000 °F.
  - 3/32 in/ft (0.78 %) is the line's end within about 0.02 % and 3–5 % above it at cone 10. The
    mean coefficient over 70–2345 °F is about 6.0 × 10⁻⁶ /K, Brosnan's figure (Derived).
  - The first pass's "about 0.7 % at 2400 °F" was low (§1 row 10, §2.4).
  - This answers `movement.py`'s "No source read gives the curve below 2400 °F" (§1 row 23).
- **Other classes** (Fig 3.3).
  - 60–70 % alumina grows 0.84–0.86 % at cone 10 and about 1.0 % at its end (about 2690 °F); 80–90 %
    alumina 0.99–1.00 % at cone 10.
  - UR-4's table gives 3/32 in/ft for the 60, 70 and 85 % classes (1/8 for 90 %). At cone 10 HWI's
    own 60–70 % curve runs 8–10 % above 3/32, and its 80–90 % curve about 27 % above, near 1/8
    (1.04 %) (Derived).
  - Silica, SiC, magnesite and corundum agree with UR-4.
- **First heat of castables** (Fig 3.5, PR-8, PDF 40). Heat-and-cool loops.
  - The permanent change after cooling is −0.40 % for the fireclay castable, −0.60 % for the
    low-cement fireclay and −1.10 % for the 90 % alumina (Verified, vector path, ±0.02 %).
  - The fireclay castable grows to +0.50 % near 2000 °F and gives some back while still heating.
  - No dip is drawn at 400–600 °F, only a slower rise.
  - Plastics (Fig 3.6) end −0.15 to −0.33 %, under the text's "0.2 % to 0.6 %".
- **Creep** (Fig 3.7, PR-10), 25 psi at 2600 °F, subsidence over hours 20–50: 60 % low-alkali 0.46 %,
  70 % 0.84 %, 85 % 1.69 %, 50 % 1.91 %. No fireclay curve, and nothing at 10 psi.
- **Alumina–silica** (Fig 1, PR-15).
  - The printed eutectic is 5.5 % Al₂O₃ at 2903 °F (1595 °C). The liquidus is 1788–1801 °C at
    40–44 % Al₂O₃ and 1818–1843 °C at 50–70 % (graph, ±8 °C).
  - At cones 9–11 a pure 42 % or 60 % mix is solid, 300–335 °C under the first liquid. A commercial
    brick's first liquid is 985 °C with a little potash (PR-17), so at cone 10 it holds a viscous
    glass. The book gives no glass fraction.
  - Fig 3 (PR-19): each 1 % of K₂O or Na₂O cuts silica's melting point by about 52 or 75 °F, with
    eutectics at 1358 and 1460 °F. It is the one figure bearing on wood-ash, salt and soda kilns,
    and it gives no brick-life figure.
  - Table 3.1 (PR-3): superduty fireclay is 41.9 % Al₂O₃ with 1.2 % alkalies.
- **The Appendix.**
  - A-2's circular segment and A-3's spherical cap equal `geometry.segment_area`,
    `shape.segment_area`, `conical.segment_radius` and `round_masonry.cap_volume` (Derived):
    hand-checkable tests (proposal 17).
  - Misprints:
    - A-3's cylinder carries a stray sphere-segment volume without its ⅓, and A-6's third
      frustum volume lacks its ⅓ (Verified).
    - A-1's trapezium and two polygon rows (Verified, agent).
    - A-7's 7/64, A-11's short ton (0.9078), and A-12's 1550 °C printed as 2922 °F (Read).
  - Use 5/9 for °F to °C, not the printed .556.

### 9.2 Drawings of Using Refractories and the shapes (`hwi-figures-using.md`)

- **Ring formulas** (UR-29, PDF 89).
  - The page assigns the sets: 1 is a straight with a radial brick; 2 is two radials with equal
    outside chords, `rings.py`'s case; 3–4 are two radials whose chords both differ.
  - Besides 3-a's lower-case c_e, formula 2-b is misprinted twice. It prints
    (πD_g − N_f c_f)/(c_e − c_f); it is (πd_g − N_t c_f)/(c_e − c_f) (Verified at 400 dpi; Derived).
  - `rings.py` has the right form.
- **Arch constants** (UR-25, PDF 85). The ninth column is headed "F" but holds P = Q tan ½θ, as
  `kiln-hardware.md` §4.3 already has it. The note under the table gives column 5 the formula of
  column 2; column 5 is (πθ/360°)·cosec ½θ (Verified).
- **Skewbacks** (UR-24, PDF 84). Six drawings; no span or dimension is printed (Verified; the line
  positions estimated by eye).
  - The two constructions captioned "recommened" (sic) draw the line of thrust through the steel's
    corner: a special skew on a steel angle, and built-up standard skews held by an angle.
  - The one "to be avoided" draws it through the brickwork below the angle: built-up skews standing
    on the wall, the angle high on the stack.
  - The "occasionaly used" special skew on special shapes sends the line into the wall's top
    courses.
  - Headers are labelled under the skew.
- **Wall bonds** (UR-20). Eight walls, by caption (Verified). The engine models no bond.
  - 9 in: alternate header and stretcher courses.
  - 13½ in, four ways: alternate; three headers to one stretcher; three stretchers to one header;
    five headers to one stretcher with the backup untied.
  - 18 in twice, and 22½ in.
  - No IFB is drawn.
- **Castable joints** (UR-5). A joint is slanted through a lining of 5 in or less and stepped through
  a thicker one. A double lining's backup joints are offset from the hot layer's. No filler and no
  dimension is drawn.
- **Circle brick** (IR-6, PDF 130). Nine high-alumina sizes, 24-33-3 to 120-129-3, 12 to 45 a ring,
  for a 4½ in lining of 3 in brick. In all nine rows the count is π·OD/9 by IR-25's 0.1 rule, and the
  printed "chord" is the thin end, 9 × ID/OD (Derived, coordinator).
- UR-23: a castable sprung arch has a cast skew shoulder in the same buckstay and tie-rod frame as a
  brick arch.

### 9.3 Ring and arch tables (`hwi-ring-arch-tables.md`, `.yaml`)

- **Totals.** `rings.ring` gives HW's total in all 485 rows of IR-26, IR-27/28, IR-29, IR-34–36 and
  the 9 × 4½ × 3 keys, to 12 ft (Derived; re-run by the coordinator).
  - The 2½ in wedge, the 3 in arch below 18 in and the 3 in wedge need `rings.py`'s A.P. Green
    extras (`apg=True`: the No. 1-X wedge, No. 4 arch and 3 in No. 1 wedge). These shapes are HW's
    own too.
  - The splits differ by one brick in 12–29 rows per table.
- **The straight region is UR-29's formula 1-a.** HW holds the tapered count at 2πL/(T − t), counted
  by the 0.1 rule, and the straights make up the total. That gives 76 No. 1 arch in IR-26 (75.40),
  113 in IR-29 (113.10) and 227 No. 1-X wedges in IR-27/28 (226.19).
  - It reproduces every straight-region row. `rings.py` is one brick off there (Derived,
    coordinator).
  - No simple rule reproduces every two-taper split.
- **Circle brick** (IR-30, PDF 154). 97 rows, 2'0"–10'0" by the inch, 3 in brick only.
  - N = π(D + 9)/9 by the 0.1 rule gives every total (97 of 97). The split between neighbouring sizes
    follows the ring algebra within one brick.
  - A.P. Green's p.117 has the same total at all 17 shared diameters and a different split at the 8
    half-foot rows.
- **Olsen.**
  - A-4 equals IR-26 in all 52 rows.
  - A-5 equals IR-29 in 65 of 66 rows. At 5'10", HW and `rings.py` have 31 + 52 and Olsen, as
    transcribed, 30 + 53: a row to check on Olsen's page.
  - A-6 equals IR-27 except where HW finishes the ring with No. 1-X wedges. HW confirms the three A-6
    cells at 2'3"–2'5" that are misplaced in Olsen.
  - A-7 equals HW in all 49 rows.
- **Arches.** Tables exist for 4½ and 9 in arches of 3 in brick at 1½, 1.608, 2 and 2.302 in/ft
  (IR-53–IR-58), for 12–18 in arches at 1.608 only, and for no arch of 2½ in brick.
  - `kiln-hardware.md` §4.4's eight rows equal them.
  - 20 rise or radius cells are misprinted, 19 of them in IR-56 (Verified); no count is.
  - An arch-course model with the ring algebra gives every total it can handle (535 of 538).
- A.P. Green rounds up only from a larger fraction. Its total is one lower than HW's in 21 ring rows
  (fractions 0.11–0.19) and in 23 arch rows.

### 9.4 Product literature (`hwi-figures-literature.md`)

- **No curves.** Section 9 has no k, hot-MOR, expansion, creep or temperature-profile curve for
  fireclay brick, IFB, dense castable or fibre beyond PDF 280's and the tables the first pass read.
  Sections 5–6 have no figure, box or caution (Not found).
- **Emisshield** (HW 150, 5/04, PDF 241). Its only graph is of metals.
  - Cold-rolled steel: 0.82 at 0 °F, 0.77 at 250 °F, 0.72 at 500 °F, 0.48 at 1000 °F and 0.18 at
    1500 °F. M-1-coated steel: 0.81–0.91 (Verified, vector path, ±0.02; the coordinator's re-reading
    agrees within 0.01).
  - There is no refractory curve: the "0.2–0.5" is a seller's text for above 3000 °F. Not adopted.
  - The engine's 0.6 for rolled steel sheet (`heatloss.py`, from `electric-and-thermal.md`) is under
    this vendor curve at shell temperatures. Recorded, not adopted.
- **INSBOARD** (HW 102, 09/03, PDF 252). "Hot Face Linings for Ceramic Kilns" is ticked for the 2600
  and 3000 grades only. Boards are 36 × 48 in, ¼–2 in thick (Verified).
- **A layered lining** (HW170, 11/02, PDF 322). A sulfur-recovery reactor's combustion chamber pairs
  a dense hot face with a back-up of IFB (G-28 LI, G-3000 LI) or of insulating castable: KAST-O-LITE
  26 LI G for 2000–2400 °F service, 30 LI G above. The two back-ups are alternatives; no thickness is
  printed (Verified, coordinator).
- **Alkali and CO** (HW 89R, 4/04, Verified).
  - KX-99 and KX-99-BF have "excellent resistance to attack by alkalies and carbon monoxide", and
    CLIPPER DP "very good resistance to thermal shock and alkali attack".
  - KAST-O-LITE 23 LI and 26 LI are low in iron against reducing conditions (HW139).
  - The INSWOOL blanket bulletin (HW 99R, 01/04) names only hydrofluoric and phosphoric acid among its
    exceptions; MP-22 adds strong alkalies.
- A coarse-aggregate low-cement castable (HW 192, 12/03) gives 24 prism-spall cycles and 3,180 psi
  hot MOR at 2000 °F with no wire fibre. Both fall as wire is added. Not a pottery castable.

### 9.5 What the coordinator checked

On fresh renders, or the vector paths read with its own scripts (`scratch/hwi-deep/coord/`,
git-ignored), against each reader's note:

| Note | Checked |
|---|---|
| Properties | Figs 3.3 and 3.4 re-digitised (agree within 0.02 %); Fig 3.5's three permanent changes; the printed eutectic and the 985 °C sentence; the cone temperatures in `cones.yaml`; A-6's frustum and A-12's 1550 °C row |
| Drawings | UR-29's 2-b and 3-a at 400 dpi; UR-25's ninth column and note; UR-24's six drawings at 300 dpi; UR-20's eight captions; IR-6's nine rows |
| Ring and arch tables | `rings.ring` re-run on all 485 rows; the IR-30 model; IR-29 at 5'10", IR-56's misprinted cells, IR-26 at 2'11" and 7'8", and IR-30 at 2'6" and 3'11" on the images |
| Literature | The Emisshield curves re-digitised (within 0.01); the wire-fibre bar chart; the INSBOARD and superduty tick matrices; the SRU table |

What the check changed in the readers' notes, each marked "coordinator" where it was made:
- **Properties.** A note of the calibration spread on Figs 3.3–3.4.
- **Drawings.**
  - Which case each UR-29 formula set is for.
  - Drawing 6's channel.
  - The UR-19 comparison, which is not a conflict.
  - IR-6's chord and counts, derived.
- **Ring and arch tables.** The straight-region rule.
- **Literature.**
  - The SRU table, whose cells were misplaced and read as three layers.
  - The full INSBOARD matrix.
  - The source of the engine's 0.6 shell emissivity.
  - The alkali exception the 2004 blanket bulletin drops.

In this note, the second pass changed §1 rows 8–10, 17 and 18, and added rows 22–23. It also added
the italic pointers in §2.4, §3.6, §4.3, §4.4 and §5.4, extended §6 and §7, amended proposals 8 and
11, and added proposals 13–19.

## Sources

- [HW05] Harbison-Walker Refractories Company, *Handbook of Refractory Practice*, © 2005.
  https://dl.icdst.org/pdfs/files/da86e4bd09a66be00c11a67957ff8e5a.pdf (the owner's copy,
  git-ignored: `docs/research/da86e4bd09a66be00c11a67957ff8e5a.pdf`). Section 9's bulletins carry
  their own dates and catalogue numbers (for example "Cat# HW 89R (4/04)").
- [S20] HarbisonWalker, *Brick Installation Guide*, © 2008 (`kiln-hardware.md`).
- [B7] HWI, *KX-99* Product Data 6/12 (`refractory-bearing.md`).
- Working scripts (git-ignored, not sources): `scratch/hwi/extract.py`, `render.py`,
  `surface_check.py`, `example1_wall.py`, `hmax_check.py`.
- The second pass's notes (§9): `hwi-figures-properties.md`, `hwi-figures-using.md`,
  `hwi-ring-arch-tables.md` with `hwi-ring-arch-tables.yaml`, and `hwi-figures-literature.md`. The
  coordinator's check scripts (git-ignored): `scratch/hwi-deep/coord/vec.py`, `rot241.py`,
  `ringcheck.py`, `splitrules.py`.
