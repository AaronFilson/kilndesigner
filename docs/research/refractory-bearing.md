# Refractory bearing stress: cold crushing strength, hot load, and what is NOT found

Research for two engine checks: (a) the end bearing of a steel lintel on refractory brick, and
(b) the bearing at an arch's skewback or jamb base. Researched 2026-10-30.

Status marks: **Verified** = read on the page or in the PDF text; **Snippet** = search-engine extract
only; **NOT FOUND** = searched and absent. "Verified (repo)" = read earlier and recorded in another
`docs/research` file, repeated here with that file's source tag.

Short answer: makers publish a **cold** crushing strength (ASTM C133) for every product, and for some
a hot-load subsidence at a fixed test load (ASTM C16, 25 psi). **No source found gives an allowable
bearing stress, a factor of safety on CCS, or a rule that the hot limit is the C16 test load** for
refractory masonry. The engine can show the numbers below as published data, but any allowable is
unsourced and must refuse or be flagged (ADR 0009).

Not for refractory: building-masonry allowables (TMS 402, BIA Technical Notes, ACI 530, ANSI A41.1
compressive stresses of 75 to 400 psi) are written for building brick and mortar at ambient
temperature. No source read says they apply to refractory brick or castable. They are not used here
(see `door-headers.md` §D1.3, [H1]).

---

## B1. What the standards say

### B1.1 ASTM C133 (cold crushing strength and modulus of rupture), C133-97 (2008)

| Item | Text | Status | Source |
|---|---|---|---|
| Scope | "These test methods cover the determination of the cold crushing strength and the modulus of rupture (MOR) of dried or fired refractory shapes of all types." | Verified | [B1] |
| Not a hot measure | "The cold strength of a refractory material is an indication of its suitability for use in refractory construction. (It is not a measure of performance at elevated temperatures.)" | Verified | [B1] |
| Comparability | "Considerable care must be used to compare the results of different determinations": specimen size and shape, face condition, orientation, loading geometry and rate of load "may all significantly affect the numerical results". | Verified | [B1] |
| Design use | "This test method is useful for research and development, engineering application and design, manufacturing process control, and for developing purchasing specifications." (no allowable or factor given) | Verified | [B1] |
| Insulating brick | Insulating brick and shapes (typical bulk density 100 lb/ft3 and below): the load is applied directly to the 4½ by 4½ in. face | Verified (text read, clause numbers not recorded) | [B1] |

### B1.2 ASTM C16 (load testing refractory shapes at high temperatures), C16-03 (2008)

| Item | Text | Status | Source |
|---|---|---|---|
| Scope | "resistance to deformation or shear of refractory shapes when subjected to a specified compressive load at a specified temperature for a specified time." | Verified | [B2] |
| Significance | "The ability of a refractory shapes to withstand prescribed loads at elevated temperatures is a measure of the high-temperature service potential of the material." Normally run hot enough "to allow some liquids to form within the test brick or to cause weakening of the bonding system". Result "usually a decrease in sample dimension parallel to the applied load". | Verified | [B2] |
| Test load | "Apply a load of 25 psi (172 kPa), before heating is started." This is the only load in the standard. **There is no 10 psi load in C16.** | Verified | [B2] §7.1 |
| Specimen | Two 9 by 4½ by 2½ or 3 in. brick (or cut from shapes), set on end; load on the vertical axis | Verified | [B2] §5, §6 |
| Report | Average percent deformation of original length; if the specimen shears, the temperature of shear | Verified | [B2] §7.4 |
| Schedules (Table 1) | Hold 90 min at: S1 2370 °F (1300 °C); S2 2460 °F (1350 °C); S3 2640 °F (1450 °C); S6 2900 °F; S7 3000 °F. S4 and S5 run to failure | Verified | [B2] Table 1 |
| Precision | Round robin (6 labs, super-duty fireclay and 70 % alumina, Schedule 3): grand mean 3.19 % subsidence; within-lab standard deviation 0.915 %, between-lab 0.629 %. Super-duty mean 5.43 %, 70 % alumina 0.939 %. Critical difference for one test: 79.6 % of the mean within a lab, 96.5 % between labs | Verified | [B2] §8 |
| Bias | "No justifiable statement on bias is possible since the true value of hot compressive load deformation cannot be established." | Verified | [B2] §8.3 |
| Design limit | The standard states no design load, no allowable stress and no link to service load | Verified (absence) | [B2] |

### B1.3 ASTM C27 (classification of fireclay and high-alumina brick), C27-98 (2008)

Test specimen 9 by 4½ by 2½ or 3 in. Methods named: PCE C24; reheat C113 (Schedule C for super-duty
at 2910 °F); **load test "(2460 °F, 1350 °C) Schedule No. 2 of Method C16"**; MOR C133; density C134
[B3] §6, §7. Table 1 as extracted (columns: PCE min; hot load subsidence max %; reheat shrinkage max %;
MOR min psi). Column alignment comes from PDF text extraction, so the blank cells ("...") were
inferred from the order of the entries. Status: Verified for text, alignment inferred.

| Class / type | PCE min | Hot load subsidence max | Reheat shrinkage max | MOR min | Other |
|---|---|---|---|---|---|
| Super-duty, regular | 33 | none printed | 1.0 % at 2910 °F | 600 psi | |
| Super-duty, spall-resistant | 33 | none printed | 1.0 % at 2910 °F | 600 psi | |
| Super-duty, slag-resistant | 33 | none printed | none | 1000 psi | bulk density min 140 lb/ft3 |
| High-duty, regular and spall-resistant | 31½ | none printed | none | 500 psi | |
| High-duty, slag-resistant | 31½ | none printed | none | 1200 psi | density min 137 lb/ft3 or porosity max 15 % |
| Semi-silica | none | **1.5 % at 2460 °F (1350 °C)** | none | 300 psi | SiO2 min 72 % |
| Medium-duty | 29 | none | none | 500 psi | |
| Low-duty | 15 | none | none | 600 psi | |

So the only fireclay class with a hot-load limit in C27 is **semi-silica: 1.5 % at 2460 °F** (the
C16 Schedule 2 hold, load 25 psi by C16 §7.1). C27 sets no cold crushing strength for any class. A
search-engine summary claimed super-duty has a "1.0 % hot load" limit; the standard text above shows
that 1.0 % is the 2910 °F **reheat** limit, so the summary was wrong (this was caught by reading [B3]).

### B1.4 ASTM C155 (classification of insulating firebrick), C155-97 (2007)

Table 1, "Grouping of Insulating Firebrick": reheat change not more than 2 % when tested (C210, 24 h,
9 in. dimension only) at the temperature below; bulk density not greater than. Verified [B4].

| Group | Reheat test, °F (°C) | Bulk density max, lb/ft3 (g/cm3) |
|---|---|---|
| 16 | 1550 (845) | 34 (0.54) |
| 20 | 1950 (1065) | 40 (0.64) |
| 23 | 2250 (1230) | 48 (0.77) |
| 26 | 2550 (1400) | 54 (0.86) |
| 28 | 2750 (1510) | 60 (0.96) |
| 30 | 2950 (1620) | 68 (1.09) |
| 32 | 3150 (1730) | 95 (1.52) |
| 33 | 3250 (1790) | 95 (1.52) |

- **C155 has no load test and no strength requirement.** Its only referenced methods are C134
  (density) and C210 (reheat). Verified [B4].
- "The group identification number is not meant to specifically designate the maximum service
  temperature ... The bulk density limits the weight per unit volume for any group as sold, but is
  not meant to be used for detailed engineering calculations." Verified [B4] §3.1.
- Therefore the "10 psi, 1½ h" load figure on Morgan and BNZ IFB sheets is each maker's own test
  condition, not a C155 or C16 requirement. The sheets do not state which standard it follows.

---

## B2. Cold crushing strength by material (maker sheets)

CCS is ASTM C133 after drying or firing, as printed. HWI's own caveat: "The test data shown are based
on average results on production samples and are subject to normal variation on individual tests.
The test data cannot be taken as minimum or maximum values for specification purposes." [B7] Morgan:
values "are subject to normal manufacturing variation".

| Repo material id | Product | CCS, psi | Condition | Status | Source |
|---|---|---|---|---|---|
| ifb-k23 | Morgan K23 (2025 sheet) | 145 (1 MPa) | as printed | Verified (repo) | [B10] via `door-headers.md` [H20] |
| ifb-k23 | Morgan K-23 (01:2013 sheet) | 145 | as printed | Verified (repo) | [B11] via [H22] |
| ifb-k25 | Morgan K25 (2025) | 188.5 | as printed | Verified (repo) | [B10] |
| ifb-k26 | Morgan K26 (2025) | 188.5 | as printed | Verified (repo) | [B10] |
| ifb-jm23 | Morgan JM23 (2025) | 145 | as printed | Verified (repo) | [B12] via [H21] |
| ifb-jm26 | Morgan JM26 (2025) | 232 | as printed | Verified (repo) | [B12] |
| ifb-jm28 | Morgan JM28 (2025) | 304.5 (2.1 MPa) | as printed | Verified (repo); also Snippet from this search | [B12] |
| ifb-jm30 | Morgan JM30 (2025) | 333.5 | as printed | Verified (repo) | [B12] |
| (no repo id) | Morgan K-28 | **NOT FOUND**; the K sheet lists K23, K25, K26 only | | NOT FOUND | [B10] |
| (historic JM) | Johns-Manville catalogue, "Cold Crushing Strength, psi 400 300 210 210 155 145" for JM-3000 / JM-28 / JM-26 / JM-23 / JM-20 / JM-1620; undated | OCR read through a fetch summary | Verified (OCR) | [B13] |
| (cross-check) | BNZ PA-20 / PA-23 / PA-26 | 95 / 140 / 240 | | Snippet | [B14] |
| hard-firebrick-kx99 | HWI KX-99 super-duty (6/12) | **5,000** (34.5 MPa); MOR 1,700; 142 lb/ft3 | as printed | Verified | [B7] |
| firebrick-high-duty-jet-dp | Alsey Jet D.P. (rev. 12 Apr 2013) | **3,560**; MOR 1,062; 133.7 lb/ft3; porosity 19.9 % | "Cold Crush", under "ASTM C-133" heading | Verified | [B8] |
| firebrick-medium-duty-smithfield | Alsey Smithfield (rev. 13 Aug 2012) | **NOT FOUND**. The sheet prints MOR 977 psi and no cold crush line | | NOT FOUND | [B9] |
| (reference only) | Mt. Savage medium-duty dry press | 3,000 to 4,000 | | Snippet | search result, not opened |
| kast-o-lite-30 | Kast-O-Lite 30 LI Plus (10/19) | 2,700 (220 °F), 2,300 (1,500 °F), 1,300 (2,000 °F), 2,000 (2,500 °F), 1,800 (2,910 °F) | dried or fired at each temperature | Verified (repo) | [B15] via [H17] |
| mizzou-castable-plus | HWI Mizzou Castable Plus (12/12) | 5,500 (220 °F), 3,500 (1,500 °F), 3,000 (2,000 °F), 4,000 (2,500 °F) | same | Verified (repo) | [B16] via [H18] |
| kast-o-lite-26 | HWI Kast-O-Lite 26 LI | **NOT FOUND** (no HWI sheet surfaced) | | NOT FOUND | search |
| kaolite-2600-li | Morgan Kaolite 2600 LI Gun | 950 to 1,700 psi (6.55 to 11.72 MPa) dried 24 h at 105 °C; fired values 225 to 900 psi "layout ambiguous" | dried | Snippet; do not use until the PDF is read | [B17] |

Notes
- The 2025 Morgan K and JM sheets are image or encoded PDFs; this session could not re-extract them.
  Their values rest on the earlier verified reading in `door-headers.md` §D5.1.
- Castable CCS falls by up to half from dried (220 °F) to fired values, so the engine must use the
  value at or below the service temperature class, not the dried value.
- CCS of IFB is read on the 4½ by 4½ in. face; the same brick bears on a 2½ in. edge in a lintel
  seat. Whether CCS applies to that orientation is **NOT FOUND**.

---

## B3. Hot load behaviour by material

| Material | Hot-load datum | Load | Status | Source |
|---|---|---|---|---|
| KX-99 | "Hot Load Test Deformation at 2640 °F (1450 °C)" 0.6 %. Load not printed on the sheet; ASTM C16 would be 25 psi but the sheet does not say so | not printed | Verified | [B7] |
| KX-99 | Creep, DIN furnace: 0.2 % subsidence between 20 and 50 h hold at 2192 °F (1200 °C) | 28.4 psi (2.0 kg/cm2), printed | Verified | [B7] |
| Jet D.P. | "ASTM C-16 Schedule 2, % deformation, Load Test at 2460 °F": **1.3 %** | 25 psi by C16 §7.1, not printed | Verified | [B8], [B2] |
| Smithfield | "ASTM C-16 Schedule 3 % deformation, Load Test at 2640 °F": **-6.8 %** (6.8 % subsidence; the sheet prints a minus sign) | 25 psi by C16 §7.1, not printed | Verified | [B9], [B2] |
| K-23 (Morgan 01:2013) | ASTM C16 at 10 psi: 0 % after 1½ h at 2,000 °F; 0.3 % after 1½ h at 2,200 °F. K-25: 0 and 0.1 % | 10 psi, as printed | Verified (repo) | [B11] via [H22] |
| BNZ PA-20, PA-23 | hot load deformation 10 psi, 1.5 h, about -0.5 % at 2000 °F; other grades and 2200 °F cells unreadable | 10 psi | Snippet | [B14] |
| K26, JM23, JM26, JM28, JM30 | no load test on the sheets read | | NOT FOUND | [B10], [B12] |
| Kast-O-Lite 30 LI Plus, Mizzou | no hot load line | | NOT FOUND (Verified absent) | [B15], [B16] |
| Kast-O-Lite 26, Kaolite 2600 LI | not searched past the CCS | | NOT FOUND | |
| Historic JM IFB | "Load test: none reported" | | Verified (OCR) | [B13] |

Reading the dense-brick numbers: Jet D.P. is 1.3 % at 2460 °F, Smithfield 6.8 % at 2640 °F (a
hotter schedule, so not comparable to Jet D.P.); KX-99 0.6 % at 2640 °F. The only same-schedule pair
is therefore not available. C16 round-robin scatter is large (critical difference 80 to 97 % of the
mean for one test) [B2], so a single sheet number is a typical value, not a limit.

A third-party patent text records, about IFB under load: "a load on the supporting IFB layer of 11.6 psi"
makes "the base IFB layer ... deform a full 1% under those loads in 100 hours" at reformer
temperatures, and "ASTM tests on Super Duty Brick have published results of a 7.86% deflection at
2,600 °F." Verified (repo) as the patentee's analysis only, numbers unchecked: `door-headers.md`
§D5.2, [H24]. Not used as a design value.

---

## B4. Guidance on allowable or design bearing load

| Question | Finding | Status | Source |
|---|---|---|---|
| Allowable bearing stress on refractory brick or castable, cold | Not published in any source read. C133 gives only the test; makers give typical CCS | NOT FOUND | [B1], sheets |
| Allowable hot bearing stress on dense firebrick or IFB | Not found. C16 gives a 25 psi test load and a subsidence result; no source says the hot working limit equals that load | NOT FOUND | [B2] |
| Statement that the hot limit is the C16 load | NOT FOUND in any source read | NOT FOUND | |
| A fraction of CCS (factor of safety) for refractory masonry | NOT FOUND. Giles: "This will represent the ultimate strength, to which a suitable factor of safety should be applied" (about MOR of refractory concrete, no number) | NOT FOUND (number); quote Verified (repo) | `door-headers.md` [H23] |
| Reformer tunnel patent on safety factor | "...sufficient safety factor when compared to the associated static load stresses"; no number | NOT FOUND (number) | [H24] |
| Maker statement that IFB is not load bearing | Not found for Morgan K or JM sheets read. JM catalogue: "All six types offer light weight, low conductivity, high purity and high structural strength"; for Sil-O-Cel: "particularly useful where high load-bearing characteristics are required" | Verified (OCR); not a design value | [B13] |
| Insulating brick next to dense brick | Allied page: IFB may be used with dense firebrick, high compressive strength supports self-standing structures. No stress given | Snippet | Allied search result |
| Handbook of Refractory Practice (HWI), Gilchrist, Chesters, Schacht, Routschka, Caniglia, AISE | Searched; none reachable online, no excerpt on allowable load or arch skewback stress surfaced | NOT FOUND | search |
| Fireclay refractoriness falls as load rises; silica brick far better under load | Old gasworks text via search extract | Snippet | search result, not opened |
| Arch crushing check | `arch-thrust-theory.md` (~line 136): crushing is "then the governing check, not covered"; K23 cold CCS about 1 MPa | Verified (repo) | `arch-thrust-theory.md` |

Round 3 searches (2026-10-30, extended web search):

| Question | Finding | Status | Source |
|---|---|---|---|
| Allowable compressive stress for refractory, any code | Search extract of an Elsevier "Allowable Compressive Stress" topic page (apparently from a pressure-vessel design text on refractory-lined vessels): "no code or standard that dictates the allowable stresses for refractory materials"; "one criteria that has been used is a factor of safety of 2 based on the minimum specified crush strength of the material at temperature"; tensile "40% of the modulus of rupture at 1000 °F". The page returned 403; the book and edition are not identified (Moss, *Pressure Vessel Design Manual*, suspected, not confirmed) | **Snippet** (not adopted: unread, unattributed, written for castable linings of steel vessels, and needs a *minimum* CCS *at temperature*, which no sheet in §B2 gives) | [B18] |
| Skewback load up to crushing | US 4,505,210 (multiple hearth furnace): the load on the skewback "can be anything up to the crushing stress of the bricks, 2500 psi" | **Snippet** (patent PDF is a scanned image; not read). A patentee's figure, not a design allowable | [B19] |
| Masonry arch edge stress | UIC 776-3R (railway masonry arch bridges) limits edge stress to 65 % of characteristic strength, quoted in a Leeds thesis | Snippet; building masonry, not refractory: not used | search |
| HWI Handbook, Schacht, Routschka, Carniglia & Barna, API 936, ASME | Searched again: no text reachable giving an allowable bearing stress or FoS for refractory brick | NOT FOUND | search |

So the bearing stays **shown, not checked**.

### B4.1 Friction at a joint

| Question | Finding | Status | Source |
|---|---|---|---|
| Brick masonry arch joints | BIA TN 31A: "The coefficient of friction between the units composing a brick or tile masonry arch is at least 0.60, without considering the additional resistance to sliding resulting from bond between mortar and the masonry units ... approximately 31 deg." Stable against sliding if the resultant's angle to the joint's normal is under the friction angle | Verified (repo), `door-headers.md` §D3.3, `flat-roofs.md` §2.2 [F2] | [H3] |
| Dry joints in refractory masonry (alumina-spinel, ladle lining), by temperature | Gajjar et al., "Characterisation of mortarless refractory masonry joints under elevated temperatures", *Engineering Structures* (2023), doi 10.1016/j.engstruct.2022.115234, quote a table from Oliveira et al. ("Normal and tangential behaviour of dry joints in refractory masonry", *Eng. Struct.* 2021) of 0.60, 0.50, 0.51, 0.53 at temperatures up to about 1200 °C, and adopt 0.598. The temperature for each value did not come through; the open PDF (Zenodo 7965714, CC BY 4.0) was over the fetch size limit | **Snippet** (values); paper identity Verified (Zenodo record) | [B20] |
| Fireclay brick, IFB, refractory-mortared joints | none | NOT FOUND | search |

The engine uses BIA's 0.60 at the door arch's springing, as it already does for flat roofs
(`frame.flat-friction`). The refractory dry-joint values (0.50 to 0.60, Snippet) bracket it from
below at some temperatures; that is noted, not used, until the table is read.

### B4.2 What the engine checks (2026-10-30)

| Place | Check | Status |
|---|---|---|
| Door arch springing | sliding, H_min/N ≤ 0.60 (BIA), `frame.door-slide` | checked; the jamb's base carries more weight for the same thrust, so the springing governs |
| Lintel ends, door arch springing, jamb toe | bearing stress | shown, not checked: no allowable or FoS (§B4) |
| Roof arch skewbacks, dome feet | bearing | not computed: no rule to check against |

Search notes: there is no published hot compressive-strength test standard in the results ("no
standards for hot crushing tests of refractory products were found to exist" in one extract), so
hot CCS is not a number makers print. HWI lists only hot load deformation and creep.

---

## B5. Magnitudes in this repo's cases (derived, for context only)

From `flat-roofs.md` §2.4 and `door-headers.md` §D5.3 worked examples: self-weight bearing stresses of
a door lintel or a 1 to 4 ft flat roof are of order 2 to 20 psi (e.g. H = 18.8 lb, fm = 1.9 psi; fm =
4.0 psi; 17 psi mean edge prestress on K23). Against K23 CCS 145 psi those are 1/7 or less, against
Jet D.P. 3,560 psi under 1/180. The unsourced factor of safety matters mainly for IFB under a heavy
superimposed load. These ratios are arithmetic on sheet values, not an allowable.

---

## What the engine can use

| Need | Usable now | Basis |
|---|---|---|
| Cold CCS, KX-99 | 5,000 psi | [B7] Verified, typical value |
| Cold CCS, Jet D.P. | 3,560 psi | [B8] Verified, typical value |
| Cold CCS, Smithfield | none | NOT FOUND (MOR 977 psi only) |
| Cold CCS, K23 / K25 / K26 | 145 / 188.5 / 188.5 psi | Verified (repo), Morgan 2025 |
| Cold CCS, JM23 / 26 / 28 / 30 | 145 / 232 / 304.5 / 333.5 psi | Verified (repo), Morgan 2025 |
| Cold CCS, Kast-O-Lite 30 LI Plus | 2,700 dried; 2,300 fired 1,500 °F; 1,300 fired 2,000 °F | Verified (repo) |
| Cold CCS, Mizzou Castable Plus | 5,500 dried; 3,500 at 1,500 °F; 3,000 at 2,000 °F | Verified (repo) |
| Cold CCS, Kast-O-Lite 26, Kaolite 2600 LI | none | NOT FOUND / Snippet only |
| Hot C16 test load, dense firebrick | 25 psi (C16 §7.1), applied by the standard, so the sheets' subsidence values (Jet D.P. 1.3 % at 2460 °F; Smithfield 6.8 % at 2640 °F; KX-99 0.6 % at 2640 °F) correspond to 25 psi only if the maker ran C16 as written; KX-99's sheet does not print the load | [B2], [B7], [B8], [B9] |
| Hot test load, IFB | 10 psi, 1½ h, K-23 and K-25 only (0 to 0.3 % at 2000 to 2200 °F) | Verified (repo) [B11]. Maker's own condition, not in C16 or C155 |
| Hot load for K26, JM-series, castables | none | NOT FOUND |
| Allowable bearing stress, cold or hot | **none** | NOT FOUND |
| Factor of safety on CCS or on the C16 load | **none** | NOT FOUND |

Suggested engine behaviour (a design decision, not a sourced rule): report the bearing stress with its
working, compare it with the published typical CCS as a ratio (state that CCS is cold and typical),
show the hot-load datum for the material where one exists, and state that no allowable or factor of
safety is published, rather than pass or fail it. Refuse a hot allowable with a reason.

---

## Gaps / NOT FOUND

1. Any allowable (working) compressive or bearing stress for firebrick, IFB or castable, cold or hot.
2. A factor of safety on CCS or on the C16 load for refractory masonry.
3. Any statement that the hot limit equals the C16 test load (25 psi dense, 10 psi IFB).
4. Smithfield cold crushing strength; Kast-O-Lite 26 LI data sheet; Kaolite 2600 LI CCS read from the
   PDF; Morgan K-28.
5. Hot load subsidence for K26, JM23 to JM30, Kast-O-Lite 30 LI Plus, Mizzou; the load (psi) printed
   on KX-99's hot-load line.
6. Hot (elevated-temperature) CCS or hot MOR of any product on these sheets.
7. Bearing on the edge or end of IFB (the lintel case) versus the 4½ by 4½ in. face tested in C133.
8. HWI Handbook of Refractory Practice, Gilchrist, Chesters, Schacht, Routschka, Caniglia, AISE: no
   accessible text on allowable loads or skewback stress.
9. Current-edition ASTM text: C16, C27, C133, C155 above are the 2007/2008 reapproved editions from a
   public mirror; the current editions were not compared.

---

## Sources

- [B1] ASTM C133-97 (Reapproved 2008), *Cold Crushing Strength and Modulus of Rupture of Refractories*. Public copy, text read. https://dl.azmanco.com/standards/ASTM-C/ASTM-C-Series-Full/C/C133.pdf
- [B2] ASTM C16-03 (Reapproved 2008), *Load Testing Refractory Shapes at High Temperatures*. Text read. https://dl.azmanco.com/standards/ASTM-C/ASTM-C-Series-Full/C/C16.pdf
- [B3] ASTM C27-98 (Reapproved 2008), *Classification of Fireclay and High-Alumina Refractory Brick*. Text read. https://dl.azmanco.com/standards/ASTM-C/ASTM-C-Series-Full/C/C27.pdf
- [B4] ASTM C155-97 (Reapproved 2007), *Classification of Insulating Firebrick*. Text read. https://dl.azmanco.com/standards/ASTM-C/ASTM-C-Series-Full/C/C155.pdf
- [B7] HWI, *KX-99* Product Data 6/12: 5912. Text read. https://ssfbs.com/wp-content/uploads/2021/06/KX_99.pdf (= `door-headers.md` [H19])
- [B8] Alsey Refractories, *Jet D.P. High Duty Firebrick*, revised 12 Apr 2013. Text read. https://ssfbs.com/wp-content/uploads/2021/06/Jet_D.P._High_Duty_Firebrick_.pdf (= `masonry-materials.md` [M10])
- [B9] Alsey Refractories, *Smithfield Unbranded Medium Duty Firebrick*, revised 13 Aug 2012. Text read. https://community.fornobravo.com/filedata/fetch?id=308784 (= [M9])
- [B10] Morgan Thermal Ceramics, *K Insulating Firebrick Series*, 1 Jan 2025. https://www.morganthermalceramics.com/media/0wobjak3/k-ifb-series_eng.pdf (values from `door-headers.md` [H20])
- [B11] Morgan Thermal Ceramics, *K-23, TC-23, IFB 23 Tile, K-25*, 01:2013. https://cdn.shopify.com/s/files/1/1023/7667/files/Morgan_Thermal_Ceramics_K-23_IFB.pdf (= [H22])
- [B12] Morgan Thermal Ceramics, *JM Insulating Firebrick Series*, 1 Jan 2025. https://www.morganthermalceramics.com/media/5beap13n/jm-ifb-series_eng.pdf (= [H21])
- [B13] Johns-Manville, insulating fire brick, Sil-O-Cel, Firecrete catalogue, undated. OCR read through a fetch summary. https://www.toxicdocs.org/d/XRMMyjnxdrJk3DJn2ZYmKgb2R
- [B14] BNZ Materials, *PA Grade IFB*. Search extract only; the page body did not load. https://www.bnzmaterials.com/insulating-firebrick/pa/
- [B15] HWI, *Kast-O-Lite 30 LI Plus* Product Data 10/19: 5874. https://ssfbs.com/wp-content/uploads/2021/06/KAST-O-LITE_30_LI_PLUS.pdf (= [H17])
- [B16] HWI, *Mizzou Castable Plus* Product Data 12/12: 5976 (= [H18]; URL in `door-headers.md` sources)
- [B17] Morgan Thermal Ceramics, *Kaolite 2600 LI Gun / Kaolite 2600LI* sheets. Search extract only. https://www.morganthermalceramics.com/media/11772/kaolite-2600li-_eng.pdf
- [B18] Elsevier ScienceDirect Topics, "Allowable Compressive Stress - an overview" (book excerpts). Search extract only; the page returned 403. https://www.sciencedirect.com/topics/engineering/allowable-compressive-stress
- [B19] US Patent 4,505,210, *Multiple hearth furnace chamber*. Search extract only (scanned PDF). https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4505210
- [B20] Gajjar P., Pereira J., Luchini B., Sinnema S., Lourenço P., Put P., "Characterisation of mortarless refractory masonry joints under elevated temperatures", *Engineering Structures* (2023), doi 10.1016/j.engstruct.2022.115234. Record read: https://zenodo.org/records/7965714 ; friction table by search extract only. Cites Oliveira R.L.G., Rodrigues J.P.C., Pereira J.M., Lourenço P.B., Marschall H.U., "Normal and tangential behaviour of dry joints in refractory masonry", *Engineering Structures* (2021), https://www.sciencedirect.com/science/article/abs/pii/S0141029621007501 (not read).
- [H3] BIA Technical Note 31A: see `door-headers.md`.
- [H1], [H23], [H24]: see `door-headers.md` sources (BIA Technical Notes; Giles, *Structural Design of Refractory Concrete*; US 10,155,210 B2).
