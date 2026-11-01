# Mortar and brick strength, hot and cold; two rings as one (fifth research round)

Fifth round (2026-10-31) on the "Follow-up research: mortar, bricks and statics" section of
`docs/planning/02-plan.md`. Builds on `refractory-bearing.md` ([B…]), `blocked-items.md` ([K…]),
`masonry-statics.md` ([M…]) and `bands-and-bottle-kilns.md`; nothing recorded there is repeated
except where this round corrects or completes it. Web search and fetch; PDFs downloaded to a
scratch folder outside the repo and their text extracted with pypdf.

Marks: **Verified** = read in the source's text (page given is the printed page, or "PDF p." when
the file has no printed numbers); **Snippet** = search extract only; **Partial**; **NOT FOUND**.
Primary = paper, report, standard or maker's sheet; secondary = a page that does not cite its
source.

Not used: two ASTM full texts (C583, C832) offered by an unlicensed mirror were not downloaded this
round; only the ASTM store's own free scope pages were read.

## Short answer

| # | Question | Status | Usable result |
|---|---|---|---|
| S1 | Friction at a dry refractory joint, by temperature | **Verified** (closes `refractory-bearing.md` §B4.1's Snippet) | 30.9° (μ ≈ 0.60) cold; 26.5°, 27.0°, 27.9° at 300, 600, 900 °C (alumina-spinel brick) |
| S2 | Bond (flexural) strength of mortared joints, cold and after heating | **Verified** (NBS 1939, 1942, 1943; HWI, BNZ sheets) | joints 5–540 psi; many air-setting joints lose all bond after 1000 °C; heat-setting joints weak until fired at 1500 °C |
| S3 | Shear (cohesion, friction) of mortared refractory joints when hot | Partial: trend Verified only in abstracts | "friction angle weakly dependent on temperature; cohesion and tensile strength decrease sharply over 900 °C"; no numbers read |
| S4 | Joint thickness | Partial (NBS test joints 1/16 and 1/8 in; HW 2008 "thin") | no sourced maximum |
| S5 | Air-setting vs heat-setting at heat | **Verified** (HWI brochure; NBS) | definitions and the strength dip at 750–1000 °C |
| S6 | Two rings, one on another | **Verified** for building brick arches (review of tests) | ring separation cut strength 33 % to 71 %; failure loads 1.5–3 × lower |
| B1 | Hot modulus of rupture (C583) | **Verified** for dense alumina brick (Bureau of Mines); C583 scope Verified | 42 % Al₂O₃ brick 530 ± 70 psi at 1350 °C vs 700–1000 cold; IFB not covered by C583 |
| B2 | Hot crushing strength | **Verified** for one dense alumina-spinel brick | 29.2 MPa cold; 24.2, 34.4, 27.0 MPa at 600, 800, 1000 °C |
| B3 | Hot load (C16) for IFB grades | **Verified** (Morgan 2011, Thermal Ceramics 2016, BNZ 2000 sheets) | closes `refractory-bearing.md` gap 5 for JM26–JM32, TC-26, BNZ grades |
| B4 | Creep (C832) | scope Verified; product values only KX-99 (already) | "useful in characterizing the load-bearing capacity of a refractory that is uniformly heated" |
| B5 | Allowable bearing / design rule | Partial: one maker's design rule | BNZ: limit IFB by a **maximum mean temperature** per grade with the hot-load figure; still no allowable stress |
| T1 | Heyman's assumptions, primary wording | Verified (Angelillo & Huerta 2018 preface) | "high compressive strength, no tensile strength and a construction which precludes sliding" |
| T2 | Rampant arch thrust, catenary at a step, hot corbels, Trinks Vol. I | NOT FOUND (again) | none new |

---

## S1. Friction at dry refractory joints, by temperature (Verified)

Source: R. L. G. Oliveira, J. P. C. Rodrigues, J. M. Pereira, P. B. Lourenço, H. U. Marschall,
"Normal and tangential behaviour of dry joints in refractory masonry", *Engineering Structures*
(2021); author's accepted manuscript, CC BY 4.0, Zenodo record 6622027 [R1]. Primary. Read in full
(34 PDF pages).

| Item | Text (verbatim) | Where | Status |
|---|---|---|---|
| Brick | alumina-spinel: "Al2O3 94.0% Fe2O3 0.1% SiO2 0.3% MgO 5.0%" (Table 1) | PDF p. 5 | Verified |
| Mortared joints | "The behaviour of joints in mortarless masonry is ruled by the Coulomb friction law [3, 4]. For masonries with mortar the Mohr-Coulomb failure criterion with tensile cut-off may be used [18]. EN 1052-3:2002 [19] is widely used to determine the initial shear strength at ambient temperature" | §2, PDF p. 5 | Verified |
| Gap it fills | "the friction coefficient between bricks is usually taken as a temperature independent parameter ... This is because there is a lack of data in the literature related to the evaluation of the friction coefficient at high temperatures." | §2, PDF p. 5 | Verified |
| Test | tilting beam in a furnace, two stacked bricks; heat at 10 °C/min, dwell 1.5 h; "The friction angle was calculated based on the displacement of the hydraulic jack" (Eq. 3, arctangent) | §6, PDF pp. 25–26 | Verified |
| Result | "The average friction angle at ambient temperature is 30.9º. The friction angle was 26.5º at 300ºC that is below the value at ambient temperature. However, a small increasing observed when comparing with the value at 300ºC, being 27.0º for 600ºC and 27.9º for 900ºC (Figure 24). The reduction of the friction coefficients when compared to the ambient temperature results were 14.2%, 12.6% and 9.7% for the temperatures of 300ºC, 600ºC and 900ºC" | §6.3, PDF p. 29 | Verified |

Derived (tan of the angles, ours): μ = 0.60 at 20 °C, 0.50 at 300 °C, 0.51 at 600 °C, 0.53 at
900 °C. These are the four values `refractory-bearing.md` [B20] had only as a Snippet, now
matched to their temperatures. Gajjar et al. 2023 [B20] (read in full this round) adopt
"a friction coefficient value of 0.598 ... based on the experiments performed by Oliveira et al."
for their numerical model (PDF p. 13), i.e. the cold value.

**Engine.** `frame_checks.py` `door_slide` and `flat_friction` (via `frame.FRICTION`) use BIA
TN 31A's 0.60 for clay brick, and `door.py` says none is sourced for refractory joints. Replace that
note with: for dense refractory on dry joints, the cold value (0.60) is confirmed and the hot value
falls to 0.50 at 300 °C (the lowest found, 0.53 at 900 °C). A hot check should use 0.50, not 0.60,
for a dry-laid dense springing. Range: one brick (94 % alumina-spinel), 20–900 °C; IFB and fireclay
not tested: refuse to claim the hot value for them (ADR 0009) or flag it.

## S2. Bond strength of mortared joints, cold and after heating (Verified)

### S2.1 National Bureau of Standards, 1939–1943 (primary, public domain)

Heindl and Pendergast tested every commercial refractory mortar type: wet air-setting (RP1219,
1939, 23 mortars) [R2], dry air-setting (RP1461, 1942, 17 mortars) [R3], heat-setting (RP1534,
1943, 12 mortars) [R4]. Bond was measured as the modulus of rupture of two half-bricks joined end
to end with mortar, broken in cross-bending, **cold after heating** (not hot).

| Item | Text (verbatim) | Where | Status |
|---|---|---|---|
| Wet air-set, joint | "The bonding strength of the mortars in assemblages of two half-brick and mortar was obtained ... The lowest strength was 5 lb/in.² and the highest 540 lb/in.² In general, a high air-setting strength of the neat mortar presages a satisfactory strength of a brick-and-mortar assembly in cross bending. Failure of the assembly occurred either in the brick, in the mortar, in the joint, or in some combination of these." | [R2] p. 37 | Verified |
| Wet air-set, heat | most mortars had "high air-setting strength, which was lowered by heating at intermediate temperatures but raised again, probably because of vitrification, when heated at the highest temperatures" or "lowered ... and not further changed"; lowest strengths "in general, close to the lowest obtained after they were heated" at 750 °C | [R2] p. 37 | Verified |
| Wet air-set, piers | piers with 1/8- and 1/16-in joints: "after they were heated at 750° C, four were found to have cracked badly. During the heating at 1,425° C many of the cracks ... healed, but numerous cases of thermal cracking occurred. Heating at 1,500° C caused slippage of the brick in the case of three mortars. The appearance of five mortars was much better in units made with the 1/16-in. joint than with the 1/8-in. one." (fractions OCR-garbled as "Ys" and "X6"; read from context) | [R2] pp. 37–38 | Verified (fractions inferred) |
| Dry air-set, joint | "The strengths of the assemblages after drying at 105° C ranged from 35 to 480 lb/in.², eight of the values being not less than 200 lb/in.²" (OCR "180"; Table 2's highest dry value is 480, mortar M-1) ... "after the 1,000° C heat treatment, seven mortars had no apparent bonding strength—that is, the specimens failed during handling" | [R3] p. 412 | Verified |
| Dry air-set, 1500 °C | "The strengths of assemblages bonded with six different mortars were obtained after heating at 1,500° C for 1 hour. The values showed great increases in strength in comparison with those obtained after heating at 1,350° C" | [R3] p. 412 | Verified |
| Dry air-set, scatter | coefficients of variation of joint strength "(1) 105° C, 8.3 to 73 percent; (2) 750° C, 18 to 79 percent; (3) 1,000° C, 35 to 65 percent, and (4) 1,350° C, 8.3 to 64 percent" | [R3] p. 412 | Verified |
| Dry air-set, reducing fire | "heating at 1,350° C in a reducing atmosphere had no significant effect on the strength of the mortars containing large percentages of chromite; but the fire-clay mortars, with one exception ... showed decreases in strength up to 50 percent" | [R3] p. 414 | Verified |
| Heat-set, neat bars | "The average modulus of rupture of the neat mortars dried at 105° C ranged from 0 to 290 lb/in.²; of those heated at 1,350° C, from 350 to 4,720 lb/in.²; and of those heated at 1,500° C, from 1,705 to 5,550 lb/in.²" | [R4] p. 310 | Verified |
| Heat-set, joint | "the bonding strength of the mortars in assemblies of two half-brick and mortar, heated at 1,350° C and cooled, was poor, as indicated by the lack of any significant strength of 8 of the 12 mortars. Satisfactory bonding strength was shown, however, by 8 of the 12 mortars after the heat treatment at 1,500° C"; assemblies up to 665 lb/in.²; "In all cases the lack of strength in the assembly was due to failure of bonding of the mortar and brick and not due to weakness of the mortar." | [R4] pp. 307–310 | Verified |
| Heat-set, lift test | lifting the top brick of a three-brick pier: "only two mortars were observed to fail when heated at 1,350° C, and but one when heated at 1,500° C and cooled" | [R4] p. 310 | Verified |

### S2.2 Current makers' sheets (primary)

| Product | Text | Status | Source |
|---|---|---|---|
| HWI SAIRSET (wet air-set, 2/2021) | "Modulus of Rupture at Joints After 220°F (105°C) lb/in.² (MPa) 530 (3.7)"; "Material Required per 1,000 9-inch Equivalent 350 to 400 lb"; "Maximum Service Temperature 3000°F (1650°C)"; "The test data shown are based on average results on production samples ... cannot be taken as minimum or maximum values for specification purposes." No fired or hot value | Verified | [R5] |
| BNZ Super Blak, No. 2986, Blakbond, Zelie No. 20 | "Modulus of Rupture (psi) Mortar 4200 4000 6100 4700"; "Modulus of Rupture (psi) Dipped Joint, ASTM C 198 375 525 575" (three values for four products; which product lacks one is not clear in the text layer) | Verified (values); column alignment NOT FOUND | [K13] in `blocked-items.md` |

ASTM C198 (free ASTM scope, via search extract): "covers the determination of the bonding
strength of air-setting refractory mortar by determining the flexural strength (modulus of rupture)
at room temperature of oven-dried brick-mortar joints." Snippet. So C198 is a **cold, unfired**
joint test only.

**Engine.** Today a mortared wall gets no credit for its mortar, and no check relies on tension
across a joint. These sources support keeping it that way (no tensile credit) and give the reason
with numbers: joint bond is 5–665 psi cold, scatter up to 79 %, and for air-setting mortars it can
fall to nothing after 1000 °C; heat-setting mortars have almost no bond below about 1350 °C. The
Bowen Mountain arch "held by mortared masonry" is therefore *not* supported as a tension or
bending capacity; its arch check should stay a no-tension (thrust line) check, with mortar treated
as bedding. Where the engine notes mortar, cite [R2]–[R4] instead of "the author's word".

## S3. Hot shear of mortared refractory joints (Partial)

| Item | Text | Status | Source |
|---|---|---|---|
| Brulin et al. (Orléans, PRISME/LaMé), slant-shear and a new tensile test, room temperature to 1450 °C, two brick/mortar couples | "Internal friction angle shows a weak dependence on temperature, while cohesion and tensile strength decrease sharply over 900°C." Table 2 (cohesion, friction angle, tensile strength by temperature) not read: HAL returned a bot wall | Snippet (abstract) | [R6] |
| "Methodology for brick/mortar interface strength characterization at high temperature", *Construction and Building Materials* (2021), S0950061820325708 | same group, to about 1500 °C; full text paywalled | Snippet | [R6] |
| "Fireclay mortar joint shear behavior at high temperatures: Slant shear testing and microscopic analysis", *J. Eur. Ceram. Soc.* (2026), S0955221926006552 | fireclay joints 25–1200 °C, Mohr–Coulomb and Drucker–Prager fits; values not reached (403) | Snippet | [R7] |
| Building brick and mortar (not refractory), elevated temperature | "the shear strength of masonry triplets declines to about 40% of its initial value at 600 °C"; mortar flexural and compressive strength lose "nearly 80% around 700 °C" | Snippet | search extract, S0379711224002479 |

**Engine.** Nothing to code: no numbers. The trend (friction steady, cohesion lost above 900 °C)
supports using friction alone at a hot mortared joint, i.e. the same Coulomb check as a dry joint
with no cohesion, which is what `door_slide` already does. Next: the two Orléans papers' tables.

## S4. Joint thickness (Partial)

| Source | Text | Status |
|---|---|---|
| NBS RP1219 [R2] | test piers "made up with 1/8-in. and 1/16-in. joints"; five mortars "much better" at 1/16 in | Verified (fractions inferred from OCR) |
| NBS RP1534 [R4] p. 304 | bond specimens made with drill-rod spacers "to obtain uniform thickness of mortar joints"; the troweling test reduces a layer to 1/16 in | Verified |
| HW *Brick Installation Guide* (2008) p. 11 | heat-setting: "thin joints, either dipped or poured"; air-setting "somewhat thicker, but such joints should be completely filled" | Verified (repo, `blocked-items.md` §19) |
| Morgan JM sheet (06:2011) | "The accurate dimensions enable the bricks to be laid more quickly, with thin, uniform joints, allowing the construction of strong and stable structures." | Verified [R9] |
| A largest joint for refractory masonry | none in any primary source; forum and retail figures (1/16–1/8 in, up to 1/2 in for one retail mortar) not used | NOT FOUND |

**Engine.** The wedge-joint mortar in `conical.py` and `rings.py` has no sourced upper limit.
Report the joint's thickness; cite NBS's 1/16 and 1/8 in as tested joints and HW's "thin" as the
rule, and do not pass/fail a thickness.

## S5. Air-setting and heat-setting at heat (Verified)

HWI, *Mortar for any installation* brochure [R8], p. 1:

- "Air-Setting - takes a rigid set when dried over 230°F. Air-setting mortars help maintain the
  strength of the bond up to the temperature at which the ceramic bond takes effect."
- "Heat-Setting - develops a ceramic set with a strong bond only at high furnace temperatures.
  These mortars offer expansion flexibility during initial heating."
- "Phosphate - often grouped with heat-setting mortars, but these mortars see a chemical reaction
  occur at lower temperatures (500°-600°F) between the phosphoric acid and ceramic oxides."
- Bond type by product (alumina-silica): SAIRSET, SAIRBOND, MORTAR MIX 413, HARWACO BOND
  air-set; SATANITE, MEXI-KOMO heat-set; PHOXBOND, GREENSET-85 P phosphate.

Combined with S2.1: air-setting joints keep a cold-set bond but weaken at 750–1000 °C (some to
zero) before a ceramic bond forms near 1350–1500 °C; heat-setting joints have almost no bond until
about 1350–1500 °C. A stoneware kiln (cone 10, about 1300 °C) may never fully develop a
heat-setting bond in its cooler courses. That last sentence is our reading of [R2]–[R4], not a
quote.

## S6. Two rings laid one on another (Verified, building brick)

Source: V. Sarhosis, S. De Santis, G. de Felice, "A review of experimental investigations and
assessment methods for masonry arch bridges", *Structure and Infrastructure Engineering* 12(11)
(2016) 1439–1464, doi 10.1080/15732479.2015.1136655; accepted version, White Rose eprints 146294
[R10]. Secondary review of primary tests. Read §3.4.

| Item | Text (verbatim) | Where | Status |
|---|---|---|---|
| Construction | "built up in one ring of large cut stones or in several concentric rings or layers of bricks, crossed by headers to promote interlocking. In few cases, multi-ring arches, consisting of several concentric rings of bricks without headers, were built especially in the UK." | §2, PDF p. 4 | Verified |
| First tests | Melbourne et al. (1989): "The models with artificial ring separation showed a 50% reduction in strength compared to the normal models." | §3.4, PDF p. 13 | Verified |
| Bolton, 3 m | "the introduction of ring separation reduced the arch strength by 33%" (two 3 m spans, two brick rings, sand in place of the mortar between rings) | §3.4, PDF p. 14 | Verified |
| Bolton, 5 m | four rings: "the strength of the arch reduced by 71%" | §3.4, PDF p. 14 | Verified |
| Melbourne & Gilbert (1995) | "The failure load of the bridges with the built-in defect of ring separation were 1.5-3 times lower than those of the bridges without the defect." | §3.4, PDF p. 14 | Verified |
| Cause | "ring separation was reliant on the shear capacity of the brick-mortar interface" | §3.4, PDF p. 14 | Verified |

Also, Snippet only: Melbourne, Tomor and Wang (ARCH'04) found cyclic capacity of multi-ring arches
"37 and 57% of the static" capacity, by ring separation [R11].

**Engine.** When a roof is two rings (e.g. a 4½ in ring on a 4½ in ring, or IFB over dense), the
engine must not take the two as one thickness unless they are bonded through with headers or
shapes. Sourced rule: unbonded rings (sand or no bond) act separately, with strength losses of 33 to
71 % in tests; mortar alone between rings depends on the interface's shear capacity, which at heat
loses its cohesion above about 900 °C (S3). So: check each ring as its own arch carrying its own
weight (the outer ring's weight resting on the inner if it cannot span alone), and give the
combined thickness only for header-bonded rings. That is a lower-bound choice; the numbers are
building brick under traffic load, so quote them as the reason, not as factors.

---

## B1. Hot modulus of rupture (Verified for dense alumina brick)

ASTM C583 scope (ASTM store page, free) [R12]: "covers determination of the high-temperature
modulus of rupture of refractory brick or monolithic refractories in an oxidizing atmosphere and
under action of a force or stress that is increased at a constant rate"; §3.1 "a widely accepted
means to evaluate materials at service temperatures"; §3.3 "refractory materials will reach a
semiplastic state at elevated temperatures where Hooke's law does not apply"; §3.4 "applies to
fired dense refractory brick and shapes, chemically bonded brick and shapes, shapes formed from
castables, plastics, or ramming materials". Insulating firebrick is not named. Verified.

US Bureau of Mines, RI 8845 (A. V. Petty Jr., 1984) [R13], public domain:

| Brick (maker's sheet, Table 1) | Cold crushing, psi | Cold MOR, psi | Hot load, C16 Sch. 3, 25 psi to 1450 °C | Hot MOR (C583), psi, as received |
|---|---|---|---|---|
| A, 41.9 % Al₂O₃, 144–148 pcf | 1,800–3,000 | 700–1,000 | 1.0–3.0 % | **530 ± 70 at 1350 °C** |
| B, 58.0 % Al₂O₃ | 7,000–10,000 | 2,300–3,300 | 0.1–0.5 % | 590 ± 110 at 1400 °C |
| C, 69.2 % Al₂O₃ | 6,000–9,000 | 1,700–2,400 | 0.4–1.0 % | 370 ± 50 at 1400 °C |

Measured cold crushing of the same as-received cores: 8,400 / 14,400 / 10,900 psi (Table 5).
Verified, p. 3 (Table 1), p. 7 (Table 5), p. 8 (Table 6).

Quotes (Verified): "Cold compressive strength data, although traditionally reported for refractory
products, must be carefully evaluated since they may have little bearing on the high-temperature or
service properties of refractories. High room temperature compressive strengths often indicate the
formation of excessive glassy phase at grain boundaries, which results in very poor high-temperature
properties." (p. 7). For brick A: strengths "similar at 1,250°, 1,300°, and 1,350° C but dropped
significantly at 1,400° C. Softening and deformation under load prior to breaking were also noted
at 1,400° C" (p. 7).

**Engine.** Hot MOR is not used today (no check relies on tension). It gives a sourced ratio for
the material library's notes: a 42 % alumina brick keeps roughly 530 / 850 ≈ 0.6 of its mid-range
cold MOR at 1350 °C (ratio ours, from the sheet's range midpoint), and loses it fast above that.
No IFB hot MOR found (C583 does not cover IFB): NOT FOUND.

## B2. Hot crushing strength (Verified, one dense brick)

Oliveira et al. 2021 [R1], §3, Table 3 (PDF pp. 8–9), alumina-spinel cores ø50 mm, heated at
5 °C/min, held 1 h: "The average compressive strength (fc avg) of brick A tested in the pressing
direction (series S01) was 29.2 MPa ... Series S04 was tested for different temperatures: 600ºC,
800ºC and 1.000ºC. The average compressive strength (fc avg) for these temperatures are 24.2MPa,
34.4 MPa and 27.0 MPa, respectively." Verified. No hot crushing value for fireclay or IFB was found;
`refractory-bearing.md`'s note that there is no hot crushing test standard stands.

## B3. Hot load (ASTM C16) for insulating firebrick (Verified; closes a gap)

All "% deformation", 10 psi (0.069 MPa) for 1½ h unless stated. Makers' typical values.

| Grade | Load and temperature | Deformation | Source |
|---|---|---|---|
| JM 23 | 5 psi (0.034 MPa), 1100 °C | 0.1 % | Morgan JM sheet 06:2011 [R9] p. 2 |
| JM 26 | 1260 °C | 0.2 % | [R9] |
| JM 28 | 1260 °C / 1320 °C | 0.1 / 0.2 % | [R9] |
| JM 30 | 1320 °C / 1370 °C | 0.1 / 0.5 % | [R9] |
| JM 32 | 1370 °C | 0.2 % | [R9] |
| TC-26 | 2200 °F (1204 °C) | 0.2 % | Thermal Ceramics US 1-14-2, 02/2016 [R14] p. 2 |
| JM-28 (US) | 2200 °F / 2400 °F (1315 °C) | 0.1 / 0.2 % | [R14] |
| JM-30 (US) | 2400 °F | 0.3 % | [R14] |
| BNZ-20, 23, 23 HS | 2000 °F (1093 °C) | 0 % | BNZ R-3033 7/00 [R15] p. 3 |
| BNZ-26, 26-60, 28 | 2200 °F | 0.2, 0.1, 0.1 % | [R15] |
| BNZ-3000, 32 | 2400 °F (1316 °C) | 0.3, 0.2 % | [R15] |
| C-22 Z, BNZ-24 | 2000 °F | 0.1, 0 % | [R15] p. 4 |
| BNZ-25, BNZ-26 HS | 2200 °F | 0.3, 0.1 % | [R15] p. 4 |

The Morgan 2011 JM sheet also prints cold strengths that differ from the 2025 sheet in
`refractory-bearing.md` §B2 (JM 23/26/28/30 MOR 1.0/1.5/1.8/2.0 MPa, CCS 1.2/1.6/2.1/2.1 MPa,
"ASTM C-93-84"); the US 2016 sheet gives TC-26/JM-28/JM-30 CCS 250/275/375 psi and MOR 175/220/275
psi. BNZ 2000: CCS 105 (BNZ-20) to 450 psi (BNZ-32); BNZ-23 125 psi, BNZ-26 270 psi. All Verified.
So JM 28's CCS reads 2.1 MPa in 2011 and 2025, 275 psi (1.9 MPa) on the US sheet.

## B4. Creep (ASTM C832)

ASTM C832 scope, via search extract of the ASTM store and GlobalSpec [R16]: "the linear change of
refractory specimens that are subjected to compressive stress while being heated and while being
held at elevated temperatures"; §5.1 "The thermal expansion under load and the 20 to 50 h creep
properties of a refractory are useful in characterizing the load-bearing capacity of a refractory
that is uniformly heated. Directly applicable examples are blast furnace stoves and glass furnace
checkers." Snippet (two extracts agree). The only product creep value found is still KX-99's
(`refractory-bearing.md` §B3). Norton's creep-based allowable (`blocked-items.md` §21) remains the
design method; no creep curve for any IFB or the dense grades in the library was found.

## B5. A maker's design rule for IFB under load (Partial)

BNZ, *Insulating Fire Brick* R-3033 (7/00) [R15] p. 5, "Design": "Temperature use limits should be
considered along with other properties of the IFB in determining the proper grade to use for your
application. The hot load deformation along with the mean temperature (i.e. the temperature at the
midpoint of the brick) should be considered as well, to assure a successful application. Guidelines
for the mean temperature of each type brick are: Maximum Mean Temperature 1800°F (982 °C) BNZ-20;
2100°F (1149 °C) BNZ-23, BNZ-23HS, C-22Z; 2200°F (1204 °C) BNZ-25, BNZ-26, BNZ-26-60, BNZ 26-HS,
BNZ-28; 2400°F (1316 °C) BNZ-3000; 2600°F (1427 °C) BNZ-32." Also: "C-22Z is a higher strength IFB
... normally specified in load bearing applications"; "The high compressive strength of IFB allows
for self-supporting structures at elevated temperatures. IFB are compatible with dense fire brick,
and add strength to the whole construction." (p. 2). Verified.

**Engine.** This is the first maker's rule found that ties load to temperature for IFB. It fits
Norton's "relatively cool portion" argument (`blocked-items.md` §21). `frame_checks.py` and
`door.py` (bearing shown, not checked) could add: for an IFB grade carrying load, compute the
brick's mean temperature from the wall's steady profile (already computed in `heatloss.py`) and
compare it with the maker's maximum mean temperature, quoting BNZ; refuse for grades with no
published guideline (Morgan K and JM sheets print none). The bearing *stress* still has no
allowable: the hot-load tests are at 10 psi, so report the stress against 10 psi as "the load the
hot-load figure was measured at", not as an allowable.

---

## T1. Statics: Heyman's assumptions from a primary hand

M. Angelillo, S. Huerta Fernández, Preface, *J. Mech. Mater. Struct.* 13(5) (2018) 607–608, doi
10.2140/jomms.2018.13.607 [R17]: Heyman "realised that the whole field of masonry structures could
be included within the wider field of limit analysis if the material met certain conditions: high
compressive strength, no tensile strength and a construction which precludes sliding. Precisely
these conditions were the hypotheses used in the calculation of masonry arches throughout the
nineteenth century. In his paper 'The stone skeleton', published in 1966, Professor Heyman took
this crucial step" (p. 607). Verified. Heyman (1966), *Int. J. Solids Struct.* 2, 249–279, not
reached; Boothby and Coronelli, "The Stone Skeleton: a reappraisal", *Heritage* 7(5) (2024) 107
(open access) returned 403.

The "precludes sliding" condition is what S1 and S3 now quantify for refractory joints.

## T2. Still not found

| Item | Searched this round | Status |
|---|---|---|
| Rampant arch thrust (hot or cold) | ArchLab, thrust-line papers; Velilla et al., "Rampant arch and its optimum geometrical generation", *Symmetry* 11(5) 627 (2019), is geometry only (common tangent parallel to the slope), no thrust | NOT FOUND (thrust); geometry Snippet |
| Load share onto an opening in a vault; groin ribs | left to the parallel round on domes and groins (`masonry-statics.md` M1, M4) | not repeated |
| Catenary meeting the next at a step | | NOT FOUND |
| Corbels at heat | | NOT FOUND |
| Trinks, *Industrial Furnaces* Vol. I (1923) pp. 196, 238 | Internet Archive holds only Vol. II (1925, 1926); HathiTrust search returned 403 to the fetcher; no full view found | NOT FOUND |
| Huerta (2001), "Mechanics of masonry vaults: the equilibrium approach", *Historical Constructions 2001*, pp. 47–69 | copy at architettura.unige.it timed out (504) twice | NOT READ |

---

## What the engine can use now

| Need | Value | Source | Module, current assumption |
|---|---|---|---|
| Friction, dry dense refractory joint, hot | μ 0.60 (20 °C), 0.50 (300 °C), 0.51 (600 °C), 0.53 (900 °C) | [R1] §6.3 | `frame_checks.door_slide`, `flat_friction` (`frame.FRICTION` = BIA 0.60, "none sourced for refractory") |
| Tension across a mortar joint | none: bond 5–665 psi, scatter to 79 %, lost after 1000 °C in some | [R2]–[R4] | all masonry checks: keep no tension; replace "author's word" for Bowen Mountain with these |
| Mortared joint when hot | friction only (cohesion lost above 900 °C) | [R6] Snippet | `door_slide` already friction-only |
| Two rings | separate unless header-bonded; 33–71 % loss in tests | [R10] | roof arches with several rings (`vault.py`, `frame.py`) |
| IFB hot load | per grade, B3 table | [R9], [R14], [R15] | material library; `refractory-bearing.md` gap 5 |
| IFB load rule | maximum mean temperature per BNZ grade | [R15] p. 5 | bearing notes in `frame_checks.py`, `door.py` |
| Dense brick hot MOR | 530 psi at 1350 °C (42 % alumina) | [R13] | notes only |
| Allowable bearing stress | **none** | | stays shown, not checked |

## Gaps

1. Hot cohesion and friction of mortared refractory joints (Brulin et al., the 2026 JECS paper).
2. Hot MOR or hot crushing of IFB; creep curves for IFB and fireclay.
3. A largest joint thickness from a primary source.
4. Trinks Vol. I; Heyman (1966); Huerta (2001); rampant-arch thrust; catenary at a step; hot corbels.
5. Column alignment of BNZ's dipped-joint C198 values.

---

## Sources

- [R1] R. L. G. Oliveira, J. P. C. Rodrigues, J. M. Pereira, P. B. Lourenço, H. U. Marschall, "Normal and tangential behaviour of dry joints in refractory masonry", *Engineering Structures* (2021). Accepted manuscript, CC BY 4.0: https://zenodo.org/records/6622027 ; publisher: https://www.sciencedirect.com/science/article/abs/pii/S0141029621007501 . Read in full.
- [R2] R. A. Heindl, W. L. Pendergast, "Properties of air-setting refractory-bonding mortars of the wet type", *J. Res. NBS* 23 (1939) 7–38, RP1219. https://nvlpubs.nist.gov/nistpubs/jres/23/jresv23n1p7_A1b.pdf . Read: pp. 36–38 and the assemblage results.
- [R3] R. A. Heindl, W. L. Pendergast, "Some properties of dry air-setting type of refractory bonding mortar", *J. Res. NBS* 28 (1942) 401–416, RP1461. https://nvlpubs.nist.gov/nistpubs/jres/28/jresv28n4p401_A1b.pdf . Read: pp. 405–414.
- [R4] R. A. Heindl, W. L. Pendergast, "Some properties of heat-setting refractory mortars", *J. Res. NBS* 30 (1943) 303–310, RP1534. https://nvlpubs.nist.gov/nistpubs/jres/30/jresv30n4p303_A1b.pdf . Read in full.
- [R5] HarbisonWalker International, *'SAIRSET* Product Data 2/2021: 5006. https://ssfbs.com/wp-content/uploads/2021/06/SAIRSET.pdf . Read.
- [R6] J. Brulin et al., "Experimental set-up for mortar / brick interface strength characterization at high temperature", HAL hal-00651606 (https://hal.science/hal-00651606 , bot wall); "Methodology for brick/mortar interface strength characterization at high temperature", *Constr. Build. Mater.* (2021), https://www.sciencedirect.com/science/article/abs/pii/S0950061820325708 . Abstracts by search extract only.
- [R7] "Fireclay mortar joint shear behavior at high temperatures: Slant shear testing and microscopic analysis", *J. Eur. Ceram. Soc.* (2026). https://www.sciencedirect.com/science/article/pii/S0955221926006552 . Search extract only (403).
- [R8] HarbisonWalker International, *Mortar for any installation* (brochure, 2021). https://thinkhwi.com/wp-content/uploads/2021/04/Mortar-Brochure.pdf . Read.
- [R9] Morgan Thermal Ceramics, *Insulating Firebricks JM*, datasheet 1-11-10 E, 06:2011. http://www.aldero.com/files_prodotti/612/files/2253_TDS%20insulating%20firebricks%20jm%20ENG.pdf . Read.
- [R10] V. Sarhosis, S. De Santis, G. de Felice, "A review of experimental investigations and assessment methods for masonry arch bridges", *Structure and Infrastructure Engineering* 12(11) (2016) 1439–1464, doi 10.1080/15732479.2015.1136655. Accepted version: https://eprints.whiterose.ac.uk/id/eprint/146294/ . Read §2, §3.4.
- [R11] C. Melbourne, A. K. Tomor, J. Wang, "Cyclic load capacity and endurance limit of multi-ring masonry arches", ARCH'04. https://caminstech.upc.edu/sites/default/files/Cyclic%20Load%20Capacity%20and%20Endurance%20Limit%20of%20Multi-Ring%20Masonry%20Arches.pdf . Downloaded; figure quoted from a search extract only.
- [R12] ASTM C583-15(2021), *Modulus of Rupture of Refractory Materials at Elevated Temperatures*, scope page. https://store.astm.org/c0583-15r21.html . Read.
- [R13] A. V. Petty Jr., *High-Temperature Properties of Alumina Refractory Brick Impregnated With Oxide and Salt Solutions*, US Bureau of Mines RI 8845 (1984). https://stacks.cdc.gov/view/cdc/10518/cdc_10518_DS1.pdf . Read pp. 1–10.
- [R14] Thermal Ceramics (Morgan), *IFB above 2600°F (1427°C) - TC-26, JM-28, JM-30 IFB*, US datasheet 1-14-2, 02/2016. https://www.lynnmfg.com/wp-content/uploads/2015/11/199482_DATA-TC-114-2.pdf . Read.
- [R15] BNZ Materials, *Insulating Fire Brick*, R-3033 7/00. https://ssfbs.com/wp-content/uploads/2021/06/BNZ_Summary_Data_for_IFB.pdf . Read.
- [R16] ASTM C832, *Measuring Thermal Expansion and Creep of Refractories Under Load*, scope (search extracts of https://store.astm.org/c0832-21.html and GlobalSpec). Snippet.
- [R17] M. Angelillo, S. Huerta Fernández, Preface, *J. Mech. Mater. Struct.* 13(5) (2018) 607–608. https://msp.org/jomms/2018/13-5/jomms-v13-n5-p01-s.pdf . Read.
- [B20], [K13]: see `refractory-bearing.md` and `blocked-items.md`. Gajjar et al. (2023) was read in full this round from https://zenodo.org/records/7965714 .
