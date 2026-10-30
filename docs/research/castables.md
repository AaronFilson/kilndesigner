# Castable refractory reference data

Checked: 2026-10-22. Every number has a source tag like [S3], and the tags are listed under "Sources" at the end.

How values are marked:
- **Verified** means I read the number on the source page or in the data sheet text myself.
- **Excerpt** means I saw it only in a search-engine snippet or summary. Check it before the engine relies on it.
- **(derived)** means I calculated it from sourced inputs. The working is shown.
- **(secondary)** means a retailer, distributor, blog or reference site passing on a primary source I could not open.
- **NOT FOUND** means I looked and found no source. Do not fill these gaps with guesses.

The user's notes in `castables/*.txt` are AI chat transcripts. No number in this file comes from them.
Section 11 lists which of their claims the sources here confirm, contradict or can't settle.

Several manufacturer PDFs were blocked (403) or had no text layer: the Imerys SECAR page, the HWI
Mizzou data sheet, mindat.org, the DTIC vitreous-silica review and the Calucem MG4 sheet. Where a
value depends on one of these, it is marked.

---

## 1. True (particle) densities

These are the solid densities to use when turning a mass recipe into solid volume. They are not bulk densities.

| Material | Value, g/cm³ | Notes | Status | Source |
|---|---|---|---|---|
| Kyanite, Al₂SiO₅ | 3.61 (measured range 3.56–3.67); 3.67 calculated from cell | | Verified | [S1] |
| Kyanite | 3.65 "theoretical" | Kyanite Mining Corp paper | Verified | [S2] |
| Sillimanite | 3.23 "theoretical" | | Verified | [S2] |
| Andalusite | 3.16 "theoretical" | | Verified | [S2] |
| Mullite | 3.05 measured (range 3.0–3.1); 3.16 calculated from cell | Formula Al(4+2x)Si(2−2x)O(10−x), x = 0.17–0.59 | Verified | [S3] |
| Mullite | 3.15 | value KMC uses in its expansion sum | Verified | [S2] |
| Mullite + amorphous silica (fired kyanite) | ≈ 3.03 | KMC, using 2.2 for amorphous silica | Verified | [S2] |
| Amorphous (fused) silica | 2.2 | KMC | Verified | [S2] |
| Fused silica | 2.18 | Goodfellow | Verified | [S4] |
| Fused silica | 2.203 | Crystran (snippet; PDF 404) | Excerpt | [S5] |
| Quartz | 2.62 measured (2.6–2.65); 2.65 calculated | | Verified | [S6] |
| Kaolinite, Al₂Si₂O₅(OH)₄ | 2.6 | | Verified | [S7] |
| Metakaolin | 2.5; 2.6; 2.64; 2.5–2.7 | concrete-mix papers and supplier sheets (Grace GMK S 5 = 2.6) | Excerpt | [S8] |
| Alpha alumina (corundum) | 4.05 measured (4.0–4.1); 4.01 calculated | | Verified | [S9] |
| Monocalcium aluminate CA (CaAl₂O₄) | 2.945 (Wikipedia, crystal); 2.98 / 2.981 (chemical listings, Thermo Scientific powder) | | Excerpt | [S10] |
| Ciment Fondu (≈ 38 % Al₂O₃ grade) | "approx. 3.24" specific gravity | Kerneos sheet via Pudlo | Verified | [S11] |
| Ciment Fondu, loose bulk | 1.16–1.37 g/cm³ (72.4–85.5 lb/ft³) | | Verified | [S11] |
| Secar 71 (≈ 70 % Al₂O₃ grade) | NOT FOUND | Imerys page blocked. I would expect about 2.9–3.0; do not use without a sheet. | NOT FOUND | |
| Lumnite MG / ~40 % grade | NOT FOUND | Calucem gives no SG on its pages. Ciment Fondu is the nearest grade with a sheet. | NOT FOUND | |
| Cellulose, crystallites | ≈ 1.60 | "irrespective of the biological origins" | Excerpt | [S12] |
| Cellulose, amorphous | 1.50 | review table | Excerpt | [S12] |
| Starch, wheat granules | 1.6 dry; 1.5 air-equilibrated; 1.3 hydrated; 1.35 ± 0.02 hydrated at 20 °C | Dengate et al. 1978 via BioNumbers | Verified | [S13] |
| Starch, helium pycnometry | 1.503 (maize) to 1.518 (potato) | | Excerpt | [S13b] |
| Dextrin | 1.45 at 20 °C (Thermo/VWR spec); 1.495–1.598 depending on type (DocCheck) | | Excerpt | [S14] |
| Water | 0.95835 at 100 °C (958.35 kg/m³) | NIST saturated liquid | Verified | [S15] |
| Perlite (unexpanded glass) | 2.2–2.4 specific gravity | Perlite Institute figures via Engineering Toolbox | Verified (secondary) | [S16] |

### 1.1 Loose bulk densities

| Material | Value | Status | Source |
|---|---|---|---|
| Expanded perlite, loose | "usually in the 2–25 lb/ft³ range" (32–400 kg/m³) | Verified (secondary) | [S16] |
| Silicone-treated perlite loose fill | recommended 2–11 lb/ft³ (32–176 kg/m³), ASTM C520 | Verified | [S17] |
| Dry softwood sawdust | 100–250 kg/m³ (6.2–15.6 lb/ft³) | Excerpt (secondary, a UK bedding supplier) | [S18] |
| Green sawdust, 45–65 % moisture | 250–350 kg/m³ | Excerpt (secondary) | [S18] |
| Dry sawdust per cubic yard | 76–191 kg = 169–421 lb, from 100–250 kg/m³ × 0.7646 m³ **(derived)** | | [S18] |

---

## 2. Kyanite → mullite + silica

### 2.1 Reaction

KMC says kyanite "decomposes into mullite, (3Al₂O₃·2SiO₂)" and that the product carries "an excess of amorphous silica" [S2] [S19]. Balanced on the 3:2 mullite composition:

3 Al₂SiO₅ → 3Al₂O₃·2SiO₂ + SiO₂ **(derived)**

Molar masses: Al₂SiO₅ 162.05, mullite 426.05, SiO₂ 60.08 g/mol. So fired kyanite is 87.6 % mullite and 12.4 % silica by mass **(derived)**. Real mullite is not exactly 3:2 (x = 0.17–0.59 in [S3]), so treat this as the ideal case.

### 2.2 Temperatures

| Value | Notes | Status | Source |
|---|---|---|---|
| 1200–1450 °C (2192–2642 °F), "depending on the hold time" | Virginia Kyanite spec sheet, 06/2021 | Verified | [S19] |
| "about 1250–1430 °C" (2282–2606 °F) | KMC kyanite web page | Verified | [S20] |
| Conversion does not start until 1300 °C (prior work); full conversion at 1400 °C for two kyanite samples | KMC comparison paper | Verified | [S2] |
| Andalusite: full conversion at 1600 °C | | Verified | [S2] |
| Sillimanite: starts 1550 °C, full at 1700 °C | | Verified | [S2] |

### 2.3 Volume expansion

| Value | Notes | Status | Source |
|---|---|---|---|
| 13.7 % (kyanite), 2.5 % (sillimanite), 0.3 % (andalusite) | theoretical, if the product is fully dense mullite | Verified | [S2] |
| 17 % (kyanite), 6.2 % (sillimanite), 4.1 % (andalusite) | theoretical, counting amorphous silica at 2.2 g/cm³ | Verified | [S2] |
| 17–19 % volumetric | KMC web page | Verified | [S20] |
| "over 25 % for 35 mesh material to about 3 % for 325 mesh" | "Volume expansion is particle size dependent". KMC spec sheet | Verified | [S19] |
| Andalusite 5 %, kyanite 18 %, sillimanite 7 % irreversible volume expansion | BC Geological Survey paper (PDF text not readable; snippet) | Excerpt | [S21] |
| Typically about 4–8 % | Digitalfire (snippet) | Excerpt (secondary) | [S22] |

KMC spec sheet table, "Total % Volume Expansion at Approximately 7 % Addition" [S19] (Verified). The sheet does not say what the kyanite was added to or at what temperature.

| Grade | Expansion |
|---|---|
| 35 mesh | 8–9 % |
| 48 mesh | 4–5 % |
| 100 mesh | 2–3 % |
| 200 mesh | 1–2 % |
| 325 mesh | 1–2 % |

The two KMC statements on the same sheet differ by a factor of about 3 for 35 mesh. The ">25 %" figure is for the kyanite grain itself; the 8–9 % figure seems to be for a mix with about 7 % kyanite. The engine should not use either until the basis is clear.

### 2.4 Virginia Kyanite chemistry [S19] (Verified)

Al₂O₃ 57.5 % (55.0 min), SiO₂ 40.3, TiO₂ 1.2, Fe₂O₃ 0.6 (0.85 max), CaO < 0.04, MgO < 0.03, Na₂O < 0.04, K₂O < 0.07, P₂O₅ < 0.15. Mineralogy: kyanite 92–98 %, quartz 2–8 %. Grades from 35 mesh (425 µm) to 325 mesh (45 µm).

---

## 3. Silica inversions

| Transition | Temperature | Size of change | Status | Source |
|---|---|---|---|---|
| α ↔ β quartz | 573 °C (1063 °F) | "linear expansion of 0.45 %" | Verified (secondary, Wikipedia) | [S23] |
| α ↔ β quartz | 573 °C theoretical; working range 540–600 °C (1004–1112 °F) | expansion curve "much steeper" over about 50 degrees; no number | Verified (secondary) | [S24] |
| α ↔ β quartz | | "around 0.4 %" volume increase | Excerpt (NTNU silicon text) | [S25] |
| α ↔ β quartz | | "1–2 % expansion" (pottery article; not stated if linear or volume) | Excerpt (secondary) | [S26] |
| α ↔ β cristobalite | 220 °C (Wikipedia); 210–280 °C (410–536 °F) (Digitalfire) | | Verified (secondary) | [S23] [S24] |
| α ↔ β cristobalite | | shrinks "3 %" on cooling (pottery article) | Excerpt (secondary) | [S26] |
| α ↔ β cristobalite | 220 °C | sudden 0.7 % expansion measured in one rice-husk silica refractory | Excerpt | [S27] |
| β-quartz → β-cristobalite (reconstructive, not an inversion) | | "around 17 %" volume increase | Excerpt | [S25] |
| Quartz no longer stable above | 870 °C | | Verified (secondary) | [S23] |

No primary handbook value for the volume change of pure quartz or cristobalite was read. NOT FOUND at primary level.

---

## 4. Fireclay, grog and calcined kaolin

### 4.1 Greenstripe fireclay

| Property | Value | Status | Source |
|---|---|---|---|
| Supplier | US Mine Corp (Digitalfire links to its page). Not Resco or Christy as far as found. | Verified (secondary) | [S28] |
| Al₂O₃ / SiO₂ / Fe₂O₃ / Na₂O / LOI | 27.70 / 57.20 / 2.00 / 1.30 / 10.30 % | Verified (secondary) | [S28] |
| Grind | "200 mesh" (manufacturer 2023 claim quoted by Digitalfire) | Verified (secondary) | [S28] |
| "Frit softening point" | 2970 °F (a Digitalfire data field, not a PCE) | Verified (secondary) | [S28] |
| PCE | NOT FOUND | | |
| Drying shrinkage, firing shrinkage | NOT FOUND | | |

Related clay, not Greenstripe: Lincoln Fireclay (North American Refractories), mined near the same pit, "had more in common with Greenstripe" [S29]. Lincoln: SiO₂ 58.20, Al₂O₃ 26.60, Fe₂O₃ 1.85, TiO₂ 1.65, LOI 10.25 %; PCE 31; drying shrinkage 6.0 % (Verified, secondary).

### 4.2 CE70 grog

NOT FOUND. No page names a product "CE70" or "CE 70". The likeliest meaning is a C-E Minerals grade: Mulcoa (Andersonville, Georgia) was "a subsidiary of C-E Minerals" and is now Imerys [S30] (Excerpt). If it is Mulcoa 70, Digitalfire gives [S31] (Verified, secondary):

| Property | Mulcoa 70 |
|---|---|
| Al₂O₃ / SiO₂ / TiO₂ / Fe₂O₃ | 68.80 / 26.80 / 2.80 / 1.20 % |
| Mullite | 87 % |
| PCE | 39 |
| Apparent porosity | 3.5 % |
| Bulk density (packed) | 2.88 g/cm³ |
| Reheat change | 0 % at 2800 °F and 2910 °F |
| Sizes | 10x18, 14x28, 16x30, 22S, 35S, 50S, 60S, 20x50, 35x80, 50x100, 60x200, 300S, 200 IC-C, 325 IC-C |
| Other grades | Mulcoa 60 is PCE 37; Mulcoa 47 is PCE 35 and "65 % mullite and 20 % glass and 15 % cristobalite" |

**Settled (2026-10-23):** Clay Art Center sells "GROGS – CE70 35 MESH" (RM407), described as
"produced from calcined mullite… a low expansion grog for bodies" [S57]. The SDS it links is
Imerys Refractory Minerals' *MULCOA® 70 / MULGRAIN® 70* (version 3.1, 19/07/2019): calcined kaolin,
CAS 92704-41-1, under 1 % quartz and under 1 % cristobalite in the fine fraction, density
"2 – 3 g/cm³" [S58] (Verified). So CE70 is Mulcoa 70, and the Digitalfire figures above apply
(secondary). Price: $50.00 per 50 lb, 5 % off for 2 or more, checked 2026-10-23 [S57] (Verified,
retail).

### 4.3 Molochite

From the Valentine Clays data sheet (UK distributor, "mean values ... do not represent a specification") [S32] (Verified, secondary):

| Property | Value |
|---|---|
| Specific gravity | 2.70 |
| Porosity | 10 vol % |
| Mullite / amorphous | 55 / 45 mass % |
| Initial deformation; squatting | 1750–1770; > 1770 (units not printed, presumably °C) |
| Expansion 20–1000 °C | 4.4 × 10⁻⁶ /K (sheet prints "4.4 x 10") |
| Al₂O₃ / SiO₂ / K₂O / Fe₂O₃ / MgO / TiO₂ / CaO | 42.0 / 54.0 / 2.0 / 1.30 / 0.30 / 0.07 / 0.07 % |
| Grades | −200s, −120s, −80s, 50/80s, 30/80s, −30s |

Digitalfire says conversion to mullite is "usually 95 %+" [S22b] (Excerpt). That conflicts with 55 % above. An Imerys sheet was NOT FOUND.

---

## 5. Calcium aluminate cements

### 5.1 Grades

| Cement | Al₂O₃ | Fe₂O₃ | Refractoriness / service | Status | Source |
|---|---|---|---|---|---|
| Ciment Fondu (Kerneos, North American spec) | ≥ 37.0 % (CaO ≤ 39.8, SiO₂ ≤ 6.0) | ≤ 18.5 % | PCE 8–9 on neat paste, "≈ 2320 °F or 1271 °C". Not for reducing atmospheres. | Verified | [S11] |
| Ciment Fondu | | | Blaine 3600–4400 cm²/g; heat of hydration 340 kJ/kg (6 h), 445 kJ/kg (24 h, 5 d); main phase CA; minor C12A7, C2S, ferrites, C4AF | Verified | [S11] |
| Lumnite MG (Calucem) / ISTRA 40 | "approximately 40 %" | NOT FOUND | "refractory castable up to 1270 °C" (2318 °F) | Verified | [S33] |
| Lumnite MG | ~40 % | | "Refractoriness up to 1250 °C" (2282 °F) | Excerpt | [S33] |
| Lumnite (standard) | ~45 % | | up to 1350 °C | Excerpt | [S33] |
| ISTRA 40 (Calucem, sister of MG) | 38–42 % | 13–17 % | CaO 36–40, SiO₂ ≤ 6; main phase CA | Excerpt | [S34] |
| Aluminite (Calucem) | ≈ 40 % | ≈ 18 % (snippet) | "insulating castable up to 1295 °C" | Verified (temp); Excerpt (Fe) | [S33] |
| Secar 71 | "approximately 70 %" | "approximately 0.1 %" | "for use above 1400 °C" | Excerpt (secondary, Tiranti, UK retailer) | [S35] |
| Secar 71 | | | CA "approx. 58 % by weight" (phase content) | Excerpt (US patent 9,193,626) | [S36] |
| Secar range | 40–80 % across grades | | | Excerpt (Imerys page blocked) | [S37] |
| Secar 51 | NOT FOUND | NOT FOUND | NOT FOUND | | |
| Lumnite MG4 | NOT FOUND (Calucem gives a description only) | | | | [S34] |

### 5.2 Hydration and bound water

| Item | Value | Status | Source |
|---|---|---|---|
| Hydrates by temperature | CAH10 below about 20 °C; C2AH8 + AH3 around 20–35 °C (one source says ~30 °C); C3AH6 + AH3 above about 35–55 °C | Excerpt | [S38] |
| Conversion | CAH10 and C2AH8 are metastable and convert to C3AH6 + AH3, raising porosity and losing strength; the conversion releases free water | Excerpt | [S38] |
| Hydrate densities | CAH10 ≈ 1.72, C2AH8 ≈ 1.95, C3AH6 ≈ 2.52 g/cm³ | Excerpt | [S38] |
| Water to fully hydrate pure CA: CA + 10H → CAH10 | 180.15 / 158.04 = 1.14 g water per g CA **(derived)** | | |
| 2CA + 11H → C2AH8 + AH3 | 198.2 / 316.1 = 0.63 **(derived)** | | |
| 3CA + 12H → C3AH6 + 2AH3 | 216.2 / 474.1 = 0.46 **(derived)** | | |

These ratios are for pure CA reacting to completion. Real cements contain other phases and do not hydrate fully at castable water levels. A measured "fraction of mix water chemically bound" for a castable was NOT FOUND.

### 5.3 Cement and water contents of castables

| Item | Value | Status | Source |
|---|---|---|---|
| ASTM C401 classes, by CaO on a calcined basis | Regular > 2.5 %; low-cement > 1.0 to 2.5 %; ultra-low > 0.2 to 1.0 %; no-cement ≤ 0.2 %. Insulating castables are classed by dried bulk density instead. Normal strength ≥ 300 psi dried MOR; high strength ≥ 600 psi. | Excerpt (standard text via snippet) | [S39] |
| Conventional castables | "8–15 % water addition" | Excerpt | [S40] |
| Low-cement castable cement content | about 4–8 % CAC; ultra-low about 1–2 % | Excerpt | [S40] |
| ULC product sheet | 5.3–5.7 % and 4.0–4.7 % water by weight (two grades) | Excerpt (Scribd upload, unnamed maker) | [S40] |
| Insulating castables, water | NOT FOUND | | |
| Mizzou: "55 lbs. to 5 pints of water"; "Do not exceed 11.0 % water under any circumstances" | High Temp Tools FAQ, quoted on a blog | Verified (secondary) | [S41] |
| Mizzou water, by weight | 5 US pints = 2.366 L ≈ 5.20 lb; 5.20 / 55 = 9.5 % of dry weight **(derived)** | | [S41] |
| Mizzou Castable Plus | 2.27 g/cm³ bulk, 3000 °F rating, 60.6 % Al₂O₃, 32.6 % SiO₂, 2.6 % CaO | Excerpt (distributor; page 403) | [S42] |

---

## 6. Thermal conductivity

### 6.1 Solid phases

| Material | Value | Status | Source |
|---|---|---|---|
| Mullite single crystal at 100 °C | [001] 6.862, [100] 4.563, [010] 4.400 W/m·K. Dense monophase mullite ceramics match the averaged crystal data; measured RT–1200 °C. | Verified (abstract only) | [S43] |
| Mullite, axis average at 100 °C | (6.862 + 4.563 + 4.400) / 3 = 5.28 W/m·K **(derived)** | | [S43] |
| Mullite k at higher temperatures | NOT FOUND in text. The curve is in Hildmann & Schneider 2005 (full text not read). | NOT FOUND | [S43] |
| Fused silica at 20 °C | 1.2–1.4 W/m·K; cp 750 J/kg·K; max continuous use 900–1200 °C | Verified | [S4] |
| Fused silica at room temperature | 1.38 W/m·K | Excerpt | [S5] |
| Fused silica, 300–2500 K | 1.4–3.0 W/m·K (compiled range) | Excerpt | [S44] |
| Fused silica, tabulated 80–6600 K | Carwile & Hoge 1966, DTIC AD0636276. PDF blocked. | NOT FOUND | [S45] |

### 6.2 Porous-solid models

| Item | What was found | Status | Source |
|---|---|---|---|
| Maxwell-type model with pore radiation | k_eff = k · [2Λ + 1 + 2φ(1 − Λ)] / [2Λ + 1 − φ(1 − Λ)], with Λ = k / k_r, φ = porosity. Limits: Λ ≫ 1 gives k_eff = 2(1 − φ)/(2 + φ) · k. | Verified | [S46] |
| Loeb 1954 | "Thermal conductivity: VIII, a theory of thermal conductivity of porous materials", J. Am. Ceram. Soc. 37(2) 96–99. Formula itself not read. | Citation verified; formula NOT FOUND | [S46] |
| Francl & Kingery 1954 | "Thermal conductivity: IX, experimental investigation of effect of porosity...", J. Am. Ceram. Soc. 37(2) 99–107. Pore orientation mattered above 500 °C. | Citation verified; data NOT FOUND | [S46] |
| Radiation term scales with pore size | for spherical and cylindrical pores, radiative conductivity proportional to pore diameter | Excerpt | [S47] |
| Russell 1935, Litovsky | NOT FOUND | | |
| Porous mullite (gel-cast) | 0.26 → 0.54 W/m·K from 25 to 1000 °C | Excerpt | [S48] |

### 6.3 Insulating firebrick data for checking a model

The repo already has K-23, JM 23 and JM 26 (`electric-and-thermal.md` §4.1, [S31] there). The rows below add K-25 and K-26 conductivity, which that file lists as not found, plus the rest of the JM series. From Morgan data sheets dated 01 January 2025, ASTM C-182 [S49] [S50] (Verified).

K series (slurry-cast, anorthite):

| Grade | Class temp | Density | Al₂O₃ / SiO₂ / CaO / Fe₂O₃ % | k at 260 / 540 / 815 / 1100 / 1370 °C, W/m·K |
|---|---|---|---|---|
| K25 | 1370 °C (2500 °F) | 617 kg/m³ (38.5 pcf) | 47 / 38 / 13.5 / 0.2 | 0.15 / 0.18 / 0.20 / 0.22 / – |
| K26 | 1430 °C (2600 °F) | 657 kg/m³ (41 pcf) | 51 / 35 / 11.0 / 0.4 | 0.20 / 0.23 / 0.26 / 0.29 / 0.31 |
| Insalcor | 1790 °C (3250 °F) | 1314 kg/m³ (82 pcf) | 77 / 21 / 0.1 / 0.4 | 0.79 / 0.80 / 0.91 / 1.09 / 1.33 |

K26 in BTU·in/hr·ft²·°F: 1.39 (500 °F), 1.60 (1004 °F), 1.80 (1499 °F), 2.01 (2012 °F), 2.15 (2498 °F). K26 shrinkage −1.00 % after 24 h at 1400 °C.

JM series (clay with burnt-out organic filler, the closest commercial analogue to a burnout castable):

| Grade | Class temp | Density | Al₂O₃ % | k at 400 / 600 / 800 / 1000 / 1100 / 1200 °C, W/m·K |
|---|---|---|---|---|
| JM28 | 1540 °C (2800 °F) | 890 kg/m³ | 67.1 | 0.30 / 0.32 / 0.34 / 0.36 / 0.36 / – |
| JM30 | 1650 °C (3000 °F) | 1020 kg/m³ | 71.5 | 0.36 / 0.37 / 0.37 / 0.38 / 0.39 / 0.39 |
| JM30HA | 1650 °C (3000 °F) | 1250 kg/m³ | 79.7 | 0.47 / 0.48 / 0.49 / 0.50 / 0.51 / – |
| JM26HD | 1400 °C (2600 °F) | 920 kg/m³ | 58 | 0.33 / 0.35 / 0.37 / 0.39 / – / – |

K-16 and K-20: NOT FOUND. They are not on the 2025 K-series sheet. An eBay listing calls K-20 "Rated 2000F" (Excerpt, secondary).

---

## 7. Organic binders and burnouts

| Item | Value | Status | Source |
|---|---|---|---|
| Formula of starch, dextrin and cellulose repeat unit | (C₆H₁₀O₅)ₙ, 162.14 g/mol per unit | NOT FOUND as a fetched page; standard chemistry. Confirm against a handbook. | |
| Heat of combustion, starch | 4.16 kcal/g representative (4.142 measured; 4.07–4.25 range) | Verified | [S51] |
| Heat of combustion, cellulose | 4.15 kcal/g representative (4.117 measured; 4.05–4.25) | Verified | [S51] |
| Glucose, for comparison | 3.74 kcal/g | Verified | [S51] |
| Starch HHV, SI and US | 4.16 × 4.184 = 17.41 kJ/g = 17.4 MJ/kg ≈ 7,485 BTU/lb **(derived)** | | [S51] |
| Cellulose HHV | 4.15 × 4.184 = 17.36 MJ/kg ≈ 7,465 BTU/lb **(derived)** | | [S51] |
| Cellulose, other measurement | 16.31 kJ/g (adiabatic bomb) | Excerpt | [S52] |
| Pyrolysis, cellulose | weight loss mainly 315–400 °C (599–752 °F); endothermic | Excerpt (Yang et al. 2007 abstract) | [S53] |
| Pyrolysis, hemicellulose | 220–315 °C | Excerpt | [S53] |
| Pyrolysis, lignin | 160–900 °C, ~40 wt % solid residue | Excerpt | [S53] |
| Starch-based filler in air, 20 °C/min | mass loss from about 240 °C, 100 % lost above about 550 °C | Excerpt | [S54] |
| Cellulose in air below 300 °C | oxidation accelerates weight loss | Excerpt | [S54] |
| Dextrin TGA | NOT FOUND | | |
| Newsprint ash | NOT FOUND | | |
| Wood ash, for comparison | about 0.6 % (bark 3 %) | Excerpt | [S55] |

The organics leave as gas and char. Char from cellulose burns out in air, not in a reducing atmosphere. A burnout castable needs oxygen at the pores up to the end of char oxidation.

---

## 8. Steam and dry-out

### 8.1 Water at saturation (NIST Webbook, IAPWS-95 basis) [S15] (Verified)

| T | Pressure | Latent heat h_fg | Vapor density |
|---|---|---|---|
| 100 °C (212 °F) | 1.0142 bar (14.71 psia) | 2256.4 kJ/kg (970.1 BTU/lb) | 0.598 kg/m³ |
| 150 °C (302 °F) | 4.7616 bar (69.06 psia) | 2113.7 kJ/kg (908.7 BTU/lb) | 2.548 kg/m³ |
| 200 °C (392 °F) | 15.549 bar (225.5 psia) | 1939.7 kJ/kg (833.9 BTU/lb) | 7.861 kg/m³ |
| 250 °C (482 °F) | 39.762 bar (576.7 psia) | 1715.1 kJ/kg (737.4 BTU/lb) | 19.967 kg/m³ |
| 300 °C (572 °F) | 85.879 bar (1245.6 psia) | 1404.6 kJ/kg (603.9 BTU/lb) | 46.168 kg/m³ |

psia = bar × 14.5038; BTU/lb = kJ/kg × 0.42992 **(derived)**.

This is why trapped water is dangerous: if a dense castable's pores hold liquid at 200 °C, the steam pressure is about 15 bar.

### 8.2 Dry-out schedules

| Source | Schedule | Status |
|---|---|---|
| Mizzou, via High Temp Tools FAQ [S41] | Air cure 16–24 h above 60 °F, kept damp or covered; best at 90–110 °F. Then, for one layer ≤ 9 in thick: ambient → 250 °F at 75 °F/h, hold 30 min per inch; 250 → 500 °F at 75 °F/h, hold 30 min per inch; 500 → 1000 °F at 75 °F/h, hold 30 min per inch; 1000 °F → use at 75 °F/h. | Verified (secondary) |
| AGC Ceramics (Japan) | 50 °C/h from room temperature to 200 °C, then a hold sized by thickness, "10 mm thickness corresponds to 1 hour" | Excerpt (PDF 404) [S56] |
| General guidance | first hold for cement-bonded refractory between 220 and 400 °F; later holds remove chemically bound water; ramps of 25–50 °F/h with holds at 220 °F and 600–1000 °F | Excerpt (secondary) [S56] |
| HWI, Allied, Plibrico primary sheets | NOT FOUND (PDFs not readable or not found) | |

---

## 9. Perlite

| Property | Value | Status | Source |
|---|---|---|---|
| Softening point | 1600–2000 °F (871–1093 °C) | Verified (secondary; credited to the Perlite Institute) | [S16] |
| Fusion point | 2300–2450 °F (1260–1343 °C) | Verified (secondary) | [S16] |
| Silicone-treated loose fill | "fusion point of approximately 2300 °F (1260 °C)" | Excerpt (Perlite Institute PDF; the text layer I read did not include this line) | [S17] |
| Specific gravity | 2.2–2.4 | Verified (secondary) | [S16] |

---

## 10. Retail prices (secondary)

None tripped over in this pass. No prices recorded.

---

## 11. Claims in the notes checked

| Claim in `castables/*.txt` | Finding |
|---|---|
| Kyanite expands "3–5 % in volume" | **Contradicted** for the grain: KMC gives 17–19 % [S20], ">25 % for 35 mesh to about 3 % for 325 mesh" [S19]. Only the finest grades are near 3 %. The KMC "at approximately 7 % addition" table (35 mesh 8–9 %, 48 mesh 4–5 %) [S19] may be what the notes half-remember. |
| Kyanite converts at 2100–2400 °F | **Partly contradicted.** KMC: 1200–1450 °C (2192–2642 °F) depending on hold [S19]; 1250–1430 °C [S20]; full conversion at 1400 °C (2552 °F) [S2]. 2100 °F (1149 °C) is below every source. |
| Perlite melts ~2300 °F | **Confirmed** as the low end of the fusion range 2300–2450 °F [S16]. It softens much lower, 1600–2000 °F. |
| Quartz inversion at 1063 °F | **Confirmed** (573 °C) [S23] [S24]. |
| … with 1–2 % expansion | **Contradicted** by 0.45 % linear [S23] and ~0.4 % volume [S25]. Only a pottery article says 1–2 % [S26]. |
| Greenstripe drying 4–5 %, firing ~4 % | **Can't settle.** No Greenstripe shrinkage data found. The neighbouring Lincoln fireclay is 6.0 % drying [S29]. |
| CE70 is "mullite grog" vs stoneware grog | **Can't settle.** No "CE70" found. If it is C-E Minerals' Mulcoa 70, that is calcined mullite, 87 % mullite, PCE 39 [S31]. |
| Lumnite MG ~40 % alumina | **Confirmed** [S33]. |
| Lumnite MG rated ~2320 °F | **Can't settle exactly.** Calucem says castable use up to 1270 °C (2318 °F) [S33] and, in a snippet, refractoriness up to 1250 °C [S33]. The 2320 °F figure matches Ciment Fondu's PCE 8–9 "≈ 2320 °F" [S11], a similar ~38–40 % cement. |
| Secar 71 ~70 % alumina | **Confirmed** by a retailer only [S35]. No manufacturer sheet read. |
| Castables normally use 5–8 % water | **Partly contradicted.** That fits low and ultra-low cement castables (4–5.7 % on one sheet) [S40]. Conventional castables are 8–15 % [S40]; Mizzou is about 9.5 %, never over 11 % [S41]. |
| Dextrin pyrolysis 300–900 °F | **Can't settle** for dextrin. Cellulose loses weight mainly at 315–400 °C (599–752 °F) [S53]; a starch-based material in air lost mass from about 240 °C (464 °F) to above 550 °C (1022 °F) [S54]. So 900 °F may be too low for complete char burnout. |
| 1 yd³ dry sawdust weighs 550–600 lb | **Contradicted** (weakly). 100–250 kg/m³ for dry softwood sawdust [S18] gives 169–421 lb per yd³ **(derived)**. 550–600 lb/yd³ would be 326–356 kg/m³, the green-sawdust range [S18]. |

---

## 11a. What the engine finds for the notes' test kiln (derived)

These come from `examples/diy-castable-test-kiln.yaml`, built with the data above (`castable.py`).
The foam figures are inputs chosen to reach the notes' densities, not measurements.

- **Foam is what makes the mixes light.** With no foam, the "K16 type" backup (15 lb grog, 25 lb
  Greenstripe, 5 lb kyanite, 5 lb dextrin, 0.25 lb paper, 14.5 lb water) fires to about
  77 lb/ft³, not 30–36. Reaching about 31 lb/ft³ takes about 60 % air by volume. Unfoamed, the
  "K26 type" hot face fires to about 87 lb/ft³, outside the range the conductivity can be
  estimated for.
- **Conductivity.** Fitted to the nine bricks in §6.3 and §4.1 of `electric-and-thermal.md`:
  k = 0.326·(ρ/1000)^1.14·(1 + 0.44·(T − 400 °C)/1000 K) W/(m·K), 8.9 % rms and at most 21 %
  for a brick left out. At 31 lb/ft³ and 1500 °F this gives about 1.2 BTU·in/(hr·ft²·°F), close to
  the notes' 1.10–1.45. Those notes values were unsourced, but this puts them in the right range.
- **Shell temperature.** A 2 in hot face with 9 in of that backup gives about 130–150 °F outside at
  cone 10 in 50 °F air. The notes said 9 in would sit above 175 °F and that 150 °F needs 14.5 in.
- **Kyanite does almost nothing here.** Kyanite starts to convert at 2192 °F (§2.2). The
  backup's hot side reaches only about 1950–1990 °F, so its kyanite never converts. In the hot
  face only the hottest ¾–⅞ in converts. Even fully converted, the hot face's 4 lb per batch
  could grow it by at most 0.10 % in length (⅓ × volume share × (3.61 ÷ 3.03 − 1)). The notes'
  "zero shrinkage" does not follow.
- **The first firing is large.** The backup holds about 1,030 lb of water and 373 lb of
  organics. Burning the organics takes about 441 lb of oxygen (25,400 ft³ of air) and releases
  about 820 kWh (2.8 million BTU). Spread over 464–1022 °F at 75 °F/h, that is about 110 kW,
  half the burners' input.
- **No set.** Without cement the mixes hold only by drying, and their service limit is unknown
  until Greenstripe's PCE is sourced or test pieces are fired.

## 12. Gaps

- Secar 71, Secar 51 and Lumnite MG4 manufacturer data sheets: chemistry, specific gravity, PCE.
- Fraction of mix water chemically bound in a CAC castable after curing (measured).
- Water content of insulating castables from a manufacturer sheet.
- HWI, Allied or Plibrico dry-out schedules from a primary sheet; Mizzou data sheet (k, water per bag).
- Greenstripe PCE and shrinkage. ("CE70" is settled: Mulcoa 70, §4.2.)
- Mullite and fused-silica conductivity tabulated against temperature (Hildmann & Schneider 2005 full text; Carwile & Hoge 1966).
- Loeb's radiation formula and constants; Russell's formula; Francl & Kingery data; Litovsky.
- K-16 and K-20 data.
- Dextrin TGA; newsprint ash; a primary sawdust bulk density.
- Primary handbook values for quartz and cristobalite volume change.
- The (C₆H₁₀O₅)ₙ formula needs a cited page.

---

## 13. Second pass: Greenstripe, Secar 71, Lumnite MG, test pieces

Checked 2026-10-23.

### 13.1 Greenstripe fireclay

US Mine Corp's product page says only "200 mesh, fine-grained plastic clay" [S59]. Its linked
technical data sheet (Greenstrip-Tech-Data-Sheet-2018.pdf) returned 404, so no maker fired-properties
table was read. The only maker document read is a 2015 SDS issued by Ione Minerals [S60].

| Property | Value | Source | Status |
|---|---|---|---|
| Particle size | 200 mesh | [S59] | Verified (maker page) |
| Composition | hydrous alumina silicate (kaolin) 80–100 %, crystalline silica (quartz) 10–20 % | [S60] | Verified (SDS) |
| Relative density | 2.65 g/cm³ (as printed) | [S60] | Verified (SDS) |
| pH | 4.5 | [S60] | Verified (SDS) |
| PCE | cone 31–32 (no °F/°C given) | [S61] | secondary (retailer) |
| Chemistry, %: SiO₂ 56.7, Al₂O₃ 28.0, TiO₂ 1.9 (printed "TiO3"), Fe₂O₃ 1.7, K₂O 0.3, MgO 0.4, CaO 0.2, Na₂O 0.3, P₂O₅ 0.05, SO₃ 0.02 | typical analysis | [S61] | secondary (retailer) |
| LOI | 10.4 % | [S61] | secondary |
| Chemistry (Digitalfire): SiO₂ 57.2, Al₂O₃ 27.7, Fe₂O₃ 2.0, Na₂O 1.3, LOI 10.3 | | [S62] | secondary |
| Drying shrinkage | NOT FOUND | | |
| Firing shrinkage, absorption at stated cones | NOT FOUND | | |
| PCE in °F/°C | NOT FOUND (no source converts it) | | |

Note: the SDS gives "Melting Point: Undetermined". The two chemistries disagree on Na₂O
(0.3 vs 1.3 %); neither is from a maker sheet.

### 13.2 Secar 71 (Kerneos, now Imerys)

Kerneos Inc. product data sheet PDS-US-S71-8/06, updated 8/24/2006 [S63], read from a
distributor's copy. Section 2 values are the warranted North American specification; section 3
values are "for guidance only".

| Property | Value | Source | Status |
|---|---|---|---|
| Al₂O₃ | ≥ 68.5 % (XRF) | [S63] | Verified (spec) |
| CaO | ≤ 31.0 % | [S63] | Verified (spec) |
| SiO₂ | ≤ 0.8 % | [S63] | Verified (spec) |
| Fe₂O₃ | ≤ 0.4 % (text: "approximately 0.1%") | [S63] | Verified (spec) |
| Minor: TiO₂ < 0.4, MgO < 0.5, SO₃ < 0.3, K₂O+Na₂O < 0.5 % | | [S63] | Verified (guidance) |
| Blaine | 3700–4500 cm²/g (ASTM C204) | [S63] | Verified (spec) |
| Specific gravity | approx. 2.94 | [S63] | Verified (guidance) |
| Bulk density (powder) | 1.04–1.23 g/cm³ | [S63] | Verified (guidance) |
| Residue at 90 µm | < 5 % | [S63] | Verified (guidance) |
| PCE (ASTM C24, neat paste) | cone 19–20 (≈ 2845 °F / 1563 °C) | [S63] | Verified (guidance) |
| Mineralogy | main CA, secondary CA₂ | [S63] | Verified |
| Set (EN-196 mortar) | Vicat initial ≥ 175 min, final ≤ 290 min | [S63] | Verified (spec) |
| Strength (ASTM C349) | 6 h ≥ 1250 psi (8.6 MPa); 24 h ≥ 4600 psi (31.7 MPa) | [S63] | Verified (spec) |
| Shelf life | ≥ 6 months dry | [S63] | Verified |
| Use | "reference product for ... LCC, ULCC, shotcrete and pumpable refractories"; primary binder in refractory mortars and concretes | [S63] | Verified |
| Maximum service temperature | NOT FOUND on the maker sheet; "in excess of 1400°C" is a retailer claim (search snippet) [S64] | | secondary |
| Current Imerys TDS | NOT FOUND (2006 sheet is the newest read) | | |

The PCE is for neat cement paste, not for a castable made with it; the engine must not use it as
a castable service limit.

### 13.3 Lumnite MG (Calucem)

Calucem Technical Data Sheet LUMNITE MG, dated 09/2014 [S65] (two distributor copies read,
identical numbers).

| Property | Value | Source | Status |
|---|---|---|---|
| Al₂O₃ | 38.0–42.0 % (ASTM C114) | [S65] | Verified |
| CaO | 36.0–40.0 % | [S65] | Verified |
| Fe₂O₃ | 13.0–17.0 % | [S65] | Verified |
| SiO₂ | 6.0 % max | [S65] | Verified |
| MgO ≤ 1.5 %, SO₃ < 0.4 % | | [S65] | Verified |
| Specific gravity | 3.2–3.3 | [S65] | Verified |
| Bulk density (powder) | approx. 1.15 g/cm³ | [S65] | Verified |
| Blaine | 310–370 m²/kg (ASTM C204) | [S65] | Verified |
| Retained on 325 mesh | < 25 % | [S65] | Verified |
| Approximate melting point | 1270 °C / 2300 °F | [S65] | Verified |
| Service limit | "mild refractory applications ... where temperatures do not exceed 1200° C (2200° F)" | [S65] | Verified |
| Mineralogy | main CA; minor C4AF, C2AS, C12A7 | [S65] | Verified |
| Set (ASTM C403 mortar) | initial 3:00–5:30 h:min; final ≤ 120 min after initial | [S65] | Verified |
| Strength | 6 h > 10 MPa; 1 day > 35 MPa | [S65] | Verified |
| Calucem web page (MG4 / Istra 40 / Lumnite MG) | "refractory castable up to 1270°C"; Aluminite "insulating castable up to 1295°C" | [S66] | Verified (web page) |
| Lumnite MG4 own TDS (chemistry, SG) | NOT FOUND (Calucem: TDS on request from info@calucem.com) | [S66] | |
| PCE | NOT FOUND | | |
| Secar 51 | NOT FOUND (not searched further) | | |

Conflict: the TDS service limit (1200 °C) is lower than the web page's 1270 °C, which matches the
TDS melting point. The engine should use 1200 °C [S65] as the refuse-above limit for Lumnite MG.

### 13.4 Test pieces: ASTM methods

ASTM's store pages forbid AI use of standard text; only scope summaries were read, and only
the scope is recorded. No specimen size, mixing, curing, drying or firing schedule was verifiable
without buying the standards: all NOT FOUND.

| Standard | What it covers (scope only) | Source | Status |
|---|---|---|---|
| ASTM C862 | Practice for mixing, casting and curing monolithic refractory concrete specimens for further testing; not for castables intended primarily for gunning. Specimen size and number are set by the test method that uses them | [S67] | secondary (search snippets of ANSI/normdocs listings) |
| ASTM C865 (current C865-22) | Practice for firing refractory concrete specimens made per C862; also gives heating rates for tests such as C16 and C583 | [S68] | secondary (search snippets) |
| ASTM C113 (C113-14, reapproved 2025) | Permanent linear change of refractory brick after heating under prescribed conditions; refers to C179, C210, C605 for specific materials. Applies to brick, not named for castables | [S69] | Excerpt (ASTM store page, summarised) |
| ASTM C20 | Apparent porosity, water absorption, apparent specific gravity and bulk density of burned refractory brick and shapes by boiling water | [S70] | secondary (search snippet) |
| ASTM C134 (C134-95(2023)) | Size, dimensions, bulk density, warpage, squareness of refractory brick and insulating firebrick; C20 gives the more precise bulk density | [S70] | secondary (search snippet) |
| ASTM C133 (C133-24) | Cold crushing strength and modulus of rupture of dried or fired refractory shapes; not a measure of high-temperature performance | [S70] | secondary (search snippet) |
| Specimen sizes, curing, drying, firing schedules, hold times | NOT FOUND (inside the paid standards) | | |

---

## Corroboration (2026-10-24)

The aim is three independent sources for each value. Resellers or patents that copy one sheet count
as one source. Values the engine uses come first (`castable.py`, `data/ingredients.yaml`).

### At three or more independent sources

| Item | Sources | Agreement |
|---|---|---|
| Kyanite true density ≈ 3.6 | [S1] 3.61, [S2] 3.65, [S3]-style cell calc 3.67 (same site as S1, so the two webmineral figures count once) | Only 2 independent sources (webmineral, KMC). Short, see below. |
| Kyanite → mullite volume expansion ≈ 17 % | [S2] 17 %, [S20] 17–19 %, [S73] 17 vol % at 1400 °C, [S21] 18 % (excerpt) | Agree. [S2] also gives 13.7 % if the mullite is fully dense. |
| Kyanite conversion temperature | [S19] 1200–1450 °C, [S20] 1250–1430 °C, [S2] full at 1400 °C, starts 1300 °C, [S72] about 1400 °C, [S74] total at 1500–1550 °C/2.5 h (sintered body) | **Disagree on the start.** Engine `KYANITE_START = 1200 °C` is the lowest figure in the set (only [S19]); the others start at 1250–1300 °C. `KYANITE_FULL = 1400 °C` matches [S2] [S72], but [S74] needed 1500–1550 °C. |
| α–β quartz inversion at 573 °C | [S23], [S24], [S25], [S75] | Agree on temperature. |
| NIST steam table (latent heat 2256.4 kJ/kg, vapour 0.598 kg/m³ at 100 °C) | [S15] is IAPWS-95 itself, an international formulation | Treated as primary standard data; not chased further. |
| Perlite softening 1600–2000 °F, fusion 2300–2450 °F, SG 2.2–2.4 | [S16], [S17], [S76] | **Only 1–2 independent.** [S76] (patent family) prints the same wording as [S16]; both appear to copy the Perlite Institute. Counts as one source plus [S17]. |
| Ciment Fondu ≈ 38–40 % Al₂O₃ | [S11], [S77], [S78] | Agree. |

### Short of three, after searching

| Item (engine use) | Sources found | Why short |
|---|---|---|
| Kyanite density 3.61 (`ingredients.yaml` kyanite) | 2 (webmineral, KMC) | No handbook read. |
| Fired kyanite 3.03 (`fired_density`) | 1, KMC [S2] (derived) | Only KMC computes it. |
| Quartz inversion size, 0.45 % linear (`QUARTZ_INVERSION`) | [S23] 0.45 % linear, [S25] ~0.4 % volume, [S26] 1–2 %, [S75] **4 % volume** | **Disagree.** 0.45 % linear ≈ 1.35 % volume, which is not the 0.4 % volume in [S25]. [S75] (refractories lecture) says 4 % volume over 200–575 °C. No primary handbook read. The engine's 0.45 % linear is from Wikipedia only. |
| Mulcoa 70 density 2.88 (`ingredients.yaml` mulcoa-70 `density`) | 1, Digitalfire [S31]; [S58] SDS "2–3"; [S79] chemistry only | **Basis mismatch.** 2.88 is a *packed grain bulk density* with 3.5 % apparent porosity, but the yaml uses it as true (particle) density. The skeletal density would be ≈ 2.88/(1 − 0.035) ≈ 2.98 **(derived)**, and mullite itself is 3.05–3.16 [S3] [S2]. No Imerys TDS found. Chemistry agrees: 68.8/26.8 % [S31] vs 68.9/26.7 % [S79]. |
| Molochite SG 2.70, 55 % mullite | 1 sheet [S32]; Digitalfire "95 %+" [S22b] | Conflict unchanged. |
| Greenstripe SG 2.65, LOI 10.3 % | SDS [S60]; LOI 10.3 [S28] vs 10.4 [S61] | 2 sources, agree within 0.1 %. PCE/shrinkage still NOT FOUND. |
| Lumnite MG SG 3.2–3.3, limit 1200 °C | 1 TDS [S65]; web page [S66] says 1270 °C | Ciment Fondu (similar grade) SG 3.24 [S11] supports the SG band. Limit stays at 1200 °C per the TDS. |
| Secar 71 SG 2.94 | 1 sheet [S63] | No Imerys TDS reachable. |
| Dextrin 1.45, starch 1.5, cellulose 1.5 | 1–2 each [S13] [S13b] [S14] [S12] | No third found. |
| Heat of combustion, starch 4.16 / cellulose 4.15 kcal/g (`HHV_*`) | [S51] (a review of ~100 values), [S52] 16.31 kJ/g cellulose, [S80] NBS 1950 bomb calorimetry (values not read), [S81] potato starch calorimetry (values not read) | Effectively 2 read. [S51] 17.4 kJ/g vs [S52] 16.31 kJ/g: **6 % apart**. A teaching page's 14.2 kJ/g [S82] uses glucose's enthalpy for cellulose and is not a measurement; ignore. |
| Mizzou dry-out 75 °F/h, ½ h per inch, ≤ 9 in (`DRYOUT_*`) | [S41] only for Mizzou; AGC [S56] 50 °C/h, 1 h per 10 mm; an unnamed maker sheet [S83] 50 °C/h per 25 mm | **Disagree.** AGC's hold is 1 h per 10 mm ≈ 2.5 h per inch, five times the Mizzou ½ h per inch the engine uses. No HWI, Allied or Plibrico primary schedule found. |
| Mizzou water 9.5 %, ≤ 11 % | 1 [S41] | No HWI sheet found. |
| Mizzou Castable Plus 2.27 g/cm³ | 1 distributor [S42] | |
| CAC hydrate densities, water ratios | excerpts [S38] only | |
| ASTM C401 classes | 1 snippet [S39] | Paid standard. |
| Conventional castable water 8–15 % | 1 [S40] | |
| IFB conductivities (§6.3) | Morgan sheets [S49] [S50] | One maker's own data; primary but single. |
| Burnout window 240–550 °C (`BURNOUT_*`) | [S54] (excerpt), [S53] cellulose 315–400 °C | 2, partly overlapping. |
| `WASTE = 0.10` | none | Marked as an assumption in the code. |
| `GLUCAN_MOLAR_MASS = 0.16214` | none fetched | Standard stoichiometry (6×12.011 + 10×1.008 + 5×15.999 = 162.14) **(derived)**. |

---

## Sources

- [S1] webmineral.com, Kyanite. http://webmineral.com/data/Kyanite.shtml
- [S2] Kyanite Mining Corp, "A Property Comparison of Commercially Available Sillimanite Materials". https://kyanite.com/blog/a-property-comparison-of-commercially-available-sillimanite-materials
- [S3] webmineral.com, Mullite. http://webmineral.com/data/Mullite.shtml
- [S4] Goodfellow, fused silica sheet. https://www.goodfellow.com/usa/fused-silica-sheet-1000002656
- [S5] Crystran, fused silica data sheet (404 when fetched; search snippet). https://www.crystran.co.uk/media/wysiwyg/Materials/fused-silica-sio2-data-sheet.pdf
- [S6] webmineral.com, Quartz. http://webmineral.com/data/Quartz.shtml
- [S7] webmineral.com, Kaolinite. http://webmineral.com/data/Kaolinite.shtml
- [S8] Metakaolin specific gravity, search snippets: https://pmc.ncbi.nlm.nih.gov/articles/PMC6947350/table/materials-12-04091-t002 ; https://www.chempoint.com/products/grace/metakaolin-aluminosilicate-pozzalanic/metakaolin/metakaolin-gmk-s-5
- [S9] webmineral.com, Corundum. http://webmineral.com/data/Corundum.shtml
- [S10] Monocalcium aluminate, search snippets: https://en.wikipedia.org/wiki/Monocalcium_aluminate ; https://b2b-uk.vwr.com/store/product/4761146/null
- [S11] Kerneos Ciment Fondu product data sheet, via Pudlo South Africa. https://cdn.shopify.com/s/files/1/0399/5693/8912/files/Pudlo-Ciment-Fondu.pdf
- [S12] Cellulose density, search snippets: https://link.springer.com/doi/10.1186/1754-6834-3-10 ; https://pmc.ncbi.nlm.nih.gov/articles/PMC9837021/table/Tab1
- [S13] BioNumbers 112354, after Dengate, Baruch & Meredith, Starch/Stärke 30 (1978) 80–84. https://bionumbers.hms.harvard.edu/bionumber.aspx?id=112354
- [S13b] Starch helium pycnometry, search snippet. https://journal.pan.olsztyn.pl/POROSITY-OF-STARCH-GRANULES-OF-DIFFERENT-ORIGIN-,97671,0,2.html
- [S14] Dextrin density, search snippets: https://b2b-ca.vwr.com/store/product/en/7491299/null ; https://flexikon.doccheck.com/de/Dextrin
- [S15] NIST Chemistry WebBook, water, saturation properties 100–300 °C. https://webbook.nist.gov/cgi/fluid.cgi?ID=C7732185&Type=SatP&TUnit=C&TLow=100&THigh=300&TInc=50
- [S16] Engineering Toolbox, perlite insulation (Perlite Institute figures). https://www.engineeringtoolbox.com/perlite-insulation-k-values-d_1173.html
- [S17] Perlite Institute, silicone-treated perlite loose fill. https://www.perlite.org/wp-content/uploads/2018/03/silicone-perlite-loose-fill-insulation.pdf
- [S18] A.W. Jenkinson, dry and green sawdust (search snippet). https://awjenkinson.co.uk/sales/?p=310 ; https://www.awjenkinson.co.uk/sales/?p=313
- [S19] Kyanite Mining Corp, Virginia Kyanite Specification Sheet, 06/2021. https://www.kyanite.com/s/Virginia-Kyanite-Specification-Sheet.pdf
- [S20] Kyanite Mining Corp, kyanite page. https://www.kyanite.com/kyanite
- [S21] Simandl et al., BC Geological Survey Paper 2004-2 (search snippet). https://cmscontent.nrs.gov.bc.ca/geoscience/publicationcatalogue/Paper/BCGS_P2004-02-55_Simandl.pdf
- [S22] Digitalfire, kyanite (search snippet). https://digitalfire.com/material/kyanite
- [S22b] Digitalfire, Molochite (search snippet). https://digitalfire.com/material/molochite
- [S23] Wikipedia, Quartz inversion. https://en.wikipedia.org/wiki/Quartz_inversion
- [S24] Digitalfire, quartz inversion temperature. https://digitalfire.com/temperature/30
- [S25] NTNU, Silicon for the Chemical and Solar Industry XIII, p. 280 (search snippet). https://ntnu.no/trykk/publikasjoner/Silicon%20for%20the%20chemical%20and%20solar%20industry%20XIII/HTML/files/assets/basic-html/page-280.html
- [S26] Ceramic Arts Network, "Quartz Inversion and Other Important Stages of Firing Pottery" (search snippet). https://ceramicartsnetwork.org/daily/article/Quartz-Inversion-and-Other-Important-Stages-of-Firing-Pottery
- [S27] Rice husk silica refractory, J. Adv. Ceram. 2013 (search snippet). https://www.sciopen.com/article/10.1007/s40145-013-0046-0
- [S28] Digitalfire, Greenstripe clay. https://digitalfire.com/material/greenstripe+clay
- [S29] Digitalfire, Lincoln Fireclay. https://digitalfire.com/material/3462
- [S30] Imerys Mulcoa; Georgia mineral industry report 1973 (search snippets). https://www.imerys.com/product-ranges/mulcoa ; https://search.library.wisc.edu/digital/A57PFXIRA6B4IS8Y/text/AIMYGICPD4GVIG83
- [S31] Digitalfire, Mulcoa 70. https://digitalfire.com/material/mulcoa+70+mullite
- [S32] Valentine Clays, Molochite technical data sheet (2024). https://valentineclays.co.uk/cdn/shop/files/Molochite_Technical_Data_Sheet.pdf
- [S33] Calucem, Lumnite MG. https://www.calucem.com/products/lumnite-refcon/lumnite-mg
- [S34] Calucem, Lumnite MG4 page; ISTRA 40 figures from search snippet. https://calucem.com/products/lumnite-refcon/lumnite-mg4
- [S35] Tiranti, Secar 71 (search snippet; 429 when fetched). https://www.tiranti.co.uk/Products/secar-71
- [S36] US Patent 9,193,626, Calcium aluminate cement (search snippet). https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9193626
- [S37] Imerys, SECAR page (403; search snippet). https://imerys.com/node/2056
- [S38] CAC hydration, search snippets: https://hal.mines-ales.fr/hal-02497775 ; https://materconstrucc.revistas.csic.es/index.php/materconstrucc/article/download/124/163/237
- [S39] ASTM C401-91 (R00), Standard Classification of Alumina and Alumina-Silicate Castable Refractories (search snippet).
- [S40] Castable water and cement content, search snippets: https://borregaard.com/biokeram/development-of-monolithic-refractories ; https://www.scribd.com/document/51437739/castable
- [S41] E. Lippert, "Mizzou castable refractory instructions" (2012), quoting hightemptools.com/faq.html. https://ericlippert.com/2012/08/21/mizzou-castable-refractory-instructions/
- [S42] Distribution International, Mizzou Castable Plus 55 lb (search snippet; 403). https://shop.distributioninternational.com/refractories/refractories-castable/recamplus55h
- [S43] Hildmann & Schneider, "Thermal Conductivity of 2/1-Mullite Single Crystals", J. Am. Ceram. Soc. 88 (2005) 2879–2882, abstract. https://elib.dlr.de/49955/
- [S44] RSC supplementary data on fused silica (search snippet; 404 when fetched). https://www.rsc.org/suppdata/c7/cp/c7cp07603g/c7cp07603g1.pdf
- [S45] Carwile & Hoge, "Thermal Conductivity of Vitreous Silica: Selected Values", 1966, DTIC AD0636276 (403). https://apps.dtic.mil/sti/pdfs/AD0636276.pdf
- [S46] "Maxwell-type models for the effective thermal conductivity of a porous material with radiative transfer in the voids", arXiv 1812.11696. https://ar5iv.labs.arxiv.org/html/1812.11696
- [S47] Pore-radiation homogenization (search snippet). https://emerald.com/insight/content/doi/10.1163/157361106777641332/full/html
- [S48] Porous mullite conductivity, J. Mater. Res. Technol. 2023 (search snippet). https://doaj.org/article/7ad1a356115e4c6e89541ffb292477d9
- [S49] Morgan Thermal Ceramics, K IFB series, 01 January 2025. https://www.morganthermalceramics.com/media/9429/k-ifb-series_eng.pdf
- [S50] Morgan Thermal Ceramics, JM IFB series, 01 January 2025. https://www.murugappamorgan.com/media/9428/jm-ifb-series_eng.pdf
- [S51] Martínez-Navarro et al., "Heats of combustion representative of the carbohydrate mass...", Food Sci. Nutr. 7(9) (2019) 3119–3127. https://pmc.ncbi.nlm.nih.gov/articles/PMC6766595/
- [S52] Cellulose heat of combustion (search snippet). https://encyclopedia.pub/entry/history/show/101785
- [S53] Yang et al., "Characteristics of hemicellulose, cellulose and lignin pyrolysis", Fuel 86 (2007) (abstract via search snippet). https://www.scinapse.io/papers/1992469412
- [S54] Rigaku application note (starch-based filler TGA); NIST firedoc on cellulose oxidation (search snippets). https://rigaku.com/hubfs/2024%20Rigaku%20Global%20Site/Resource%20Hub/Applications%20Library/PDF/145539928138.pdf ; https://firedoc.nist.gov/article/C3cxXYQBWEcjUZEY1h1k
- [S55] Baker, Wood Fuel Properties (search snippet). https://inspectapedia.com/chimneys/Wood-Fuel-Properties-Baker-AJ.pdf
- [S56] Dry-out guidance, search snippets: https://www.agcc.jp/Portals/0/images/en/core/alumi/about/methodDrying.pdf ; https://heattreattoday.com/?p=14700 ; https://open-exam-prep.com/study-guides/nccer-boilermaker/towers-exchangers-refractory/refractory-insulation-lagging
- [S57] Clay Art Center, "GROGS – CE70 35 MESH" (RM407), checked 2026-10-23. https://clayartcenter.net/product/rm407-grog-ce70-35-mesh/
- [S58] Imerys Refractory Minerals, MULCOA 70 / MULGRAIN 70 safety data sheet, v3.1, 19/07/2019, as linked by Clay Art Center for CE70. https://clayartcenter.net/sds/rm407-ce70-35-mesh/
- [S59] US Mine Corporation, Greenstripe product page, checked 2026-10-23. https://usminecorp.com/mineral-products/ (linked TDS https://usminecorp.com/wp-content/uploads/2019/03/Greenstrip-Tech-Data-Sheet-2018.pdf returned 404)
- [S60] Ione Minerals, Inc., SDS "GREENSTRIPE CLAY", revised 05/05/2015 (Aardvark Clay copy). https://www.aardvarkclay.com/pdf/raw_clays/SDS-Greenstripe.pdf
- [S61] Axner, "Greenstripe Fireclay" product page (typical analysis, PCE), checked 2026-10-23. https://www.axner.com/fireclay-greenstripe.aspx
- [S62] Digitalfire, "Greenstripe Clay". https://digitalfire.com/material/greenstripe+clay
- [S63] Kerneos Inc., Product data sheet Secar 71, PDS-US-S71-8/06, updated 8/24/2006 (distributor copy). https://baumarket.gr/wp-content/uploads/2018/02/Secar71.pdf
- [S64] Tiranti / Pottery Crafts, Secar 71 product pages (search snippet). https://potterycrafts.co.uk/products/tiranti-secar-71-white-ciment-fondu
- [S65] Calucem, Technical Data Sheet LUMNITE MG, 09/2014 (Ezmix copies). https://www.ezmixinc.com/assets/docs-technical/SD_LUMNITE_Refcon_MG_EN_CAN.pdf ; https://www.ezmixinc.com/assets/docs-technical/LumniteMGTDS.pdf
- [S66] Calucem, Lumnite MG4 product page, checked 2026-10-23. https://calucem.com/products/lumnite-refcon/lumnite-mg4
- [S67] ASTM C862 listings (search snippets). https://webstore.ansi.org/standards/astm/astmc86216 ; https://catalogue.normdocs.ru/catalog/com.normdocs.astm.card.c862-16/Standard-ASTM-C862-16
- [S68] ASTM C865 listings (search snippets). https://webstore.ansi.org/standards/astm/astmc86522 ; https://knowledge.bsigroup.com/products/standard-practice-for-firing-refractory-concrete-specimens-1
- [S69] ASTM C113-14(2025), store page. https://store.astm.org/c0113-14r25.html
- [S70] ASTM C20, C134, C133 listings (search snippets). https://store.astm.org/c0134-95r23.html ; https://store.astm.org/c0133-24.html ; https://www.astm.org/Standards/refractory-standards.html
- [S72] EBSCO Research Starters, "Kyanite and porcelain manufacture" (search snippet). https://www.ebsco.com/research-starters/geology/kyanite-and-porcelain-manufacture
- [S73] Kyanite Mining Corp, "Utilization of Virginia Kyanite and Virginia Mullite in Refractory Applications Worldwide" (search snippet; KMC, so not independent of S2/S19/S20). https://kyanite.com/blog/utilization-of-virginia-kyanite-and-virginia-mullite
- [S74] Int. J. Mater. Sci. Eng. (IUST), article 1-379, kyanite-to-mullite in sintering (search snippet). https://ahc.iust.ac.ir/ijmse/article-1-379-en.pdf
- [S75] University of Technology (Iraq), "Refractories 10" lecture notes (search snippet). https://mae.apps.uotechnology.edu.iq/wp-content/uploads/2024/12/refractories-10.pdf
- [S76] US Patent 7,655,138 and family, perlite properties (search snippet; same figures as S16). https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7655138
- [S77] Wikipedia, Calcium aluminate cements (search snippet). https://en.wikipedia.org/wiki/Calcium_aluminate_cements
- [S78] Materiales de Construcción paper on ciment fondu, CaO ≈ Al₂O₃ 38–40 % (search snippet). https://materconstrucc.revistas.csic.es/index.php/materconstrucc/article/download/695/748/827
- [S79] LKAB Minerals, Mulcoa (search snippet). https://lkabminerals.com/product/mulcoa
- [S80] Jessup & Prosen, NBS J. Res. 44 (1950) 387, heats of combustion of cellulose (search snippet; values not read). https://nvlpubs.nist.gov/nistpubs/jres/44/jresv44n4p387_A1b.pdf
- [S81] J. Chem. Thermodyn. 2013, combustion of potato starch, via NIST TRC (search snippet; values not read). https://trc.nist.gov/ThermoML/10.1016/j.jct.2012.11.031.html
- [S82] Polymer Science Learning Center, heat of combustion of cellulose, teaching calculation (search snippet). https://pslc.ws/fire/cellulos/combans1.htm
- [S83] "Instructions for the use of Castables (Heat Resistant Concretes)", unnamed maker, forum-hosted (search snippet). https://community.fornobravo.com/filedata/fetch?id=426785
