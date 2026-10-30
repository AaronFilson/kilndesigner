# Masonry, stone, earth and castable reference data

Checked 2026-10-29 for kilndesigner. Olsen's *The Kiln Book* (4th ed.) has kilns built of materials
the library lacks: common red brick, fireclay brick by duty class, granite, unfired clay, and two
named castables. This file collects sourced thermal data for them. It adds to
`electric-and-thermal.md` §4 and `castables.md` §6, and does not repeat them. Every value has a
source tag [M#], listed at the end. In-repo sources are named by file and section.

How to read this file:

- **Verified**: read on the source page or in the PDF text itself.
- **Verified (secondary)**: read in full, but in a compilation that copies another source (a
  textbook table, or the `ht` library's transcription of a handbook). The original was not read.
- **Excerpt**: seen only in a search-engine extract. Check it before relying on it.
- **Derived**: my arithmetic on sourced inputs. The working is shown.
- **NOT FOUND**: searched for and not found. No number is given.

k is thermal conductivity. For refractories it is at the stated **mean** temperature. Building
material values are at room temperature unless a temperature is given.

Unit conversions used (the same as `electric-and-thermal.md`):

- 1 Btu·in/(h·ft²·°F) = 0.144228 W/(m·K)
- 1 lb/ft³ = 16.018 kg/m³
- °C = (°F − 32) × 5/9; K = °C + 273.15

Olsen kilns that need these materials (`olsen-kilns.md`):

| Material | Kilns |
|---|---|
| Common red brick | `meaders-cheever` ("RUBBLE BRICK" walls), `ninodaguia` (floor dome of common bricks), `chappell-domura` (common red brick over the foundation) |
| Low-, intermediate- and medium-duty firebrick | `fast-fire` ("LOW DUTY FIREBRICK 90 required"), `chappell-domura` (intermediate-duty and medium-duty) |
| Granite | `moveros-umbrella` (granite rocks mortared together, 18–24 in) |
| Unfired clay | `hotchkiss-raw-clay` (raw blocks of 50 % fireclay, 50 % coarse sand), `anagama-hole`, `pit-kiln-improved`, earth overcoats, the adobe skin of `gulgong-racer` |
| Kaolite 2600-LI ("K-26 IFB castable") | `hollyweird`, `hohr-2003` ("a 2600 IFB (low iron) castable") |
| Coolcast 140 | `gulgong-racer` |

---

## 1. Common (red) clay building brick

### 1.1 Conductivity and density

| Source | Material as named | Density | Temperature | k | c_p | Status | Tag |
|---|---|---|---|---|---|---|---|
| Lienhard, Table A.2 | Brick, common | not given | 0–1000 °C (range) | 0.7 W/(m·K) | not given | Verified (secondary) | [M1] |
| Lienhard, Table A.2 | Brick, fired clay | 1920 kg/m³ | 24 °C | 0.81–0.98 W/(m·K) | 800 J/(kg·K) | Verified (secondary) | [M1] |
| Lienhard, Table A.2 | Brick, facing | not given | 20 °C | 1.3 W/(m·K) | not given | Verified (secondary) | [M1] |
| BIA Technical Note 4, Table 1 | Face brick | 130 lb/ft³ (2082 kg/m³) | room | 6.4–7.8 Btu·in/(h·ft²·°F) = 0.92–1.12 W/(m·K) (derived) | – | Verified | [M3] |
| BIA Technical Note 4, Table 1 | Face brick | 120 lb/ft³ (1922 kg/m³) | room | 5.6–6.8 Btu·in/(h·ft²·°F) = 0.81–0.98 W/(m·K) (derived) | – | Verified | [M3] |
| BIA Technical Note 4, note b | Fired clay brick, density unknown | "most fired clay brick" 120–130 lb/ft³ | room | R = 0.15 per inch, so k = 1/0.15 = 6.7 Btu·in/(h·ft²·°F) = 0.96 W/(m·K) (derived) | – | Verified | [M3] |
| `ht` library (ASHRAE 2013) | Brick, fired clay | 2400 / 2240 / 2080 / 1920 / 1760 / 1600 / 1440 / 1280 / 1120 kg/m³ | room | 1.34 / 1.185 / 1.02 / 0.895 / 0.78 / 0.675 / 0.57 / 0.48 / 0.405 W/(m·K) | 800 J/(kg·K) | Verified (secondary) | [M2] |
| Engineering ToolBox | Brickwork, common (building brick) | not given | not stated | 0.6–1.0 W/(m·K) | – | Verified | [M4] |
| Olsen p.295 | Common brick | 100 lb/ft³ (1602 kg/m³) | – | – | – | Read (`kiln-reference.md`, Appendix weights) | Olsen |

- Lienhard says Table A.2 was built mainly from Touloukian's *Thermophysical Properties of Matter*
  (Purdue, vols 2 and 5), and that some building-material data come from the 2017 ASHRAE Handbook,
  chapter 26 [M1]. The "fired clay" row has the same numbers as BIA's ASHRAE row for 120 lb/ft³
  (1922 kg/m³, 0.81–0.98), so it is probably the ASHRAE one.
- BIA's Table 1 is "From 2013 ASHRAE Handbook – Fundamentals". Its note b says ASHRAE lists k for
  brick densities from 70 to 150 lb/ft³, and that most fired clay brick is 120–130 lb/ft³ [M3].
- `ht` gives one number per density. For 1920 and 2080 kg/m³ these are the midpoints of the BIA
  ranges: (0.81 + 0.98)/2 = 0.895, and (0.92 + 1.12)/2 = 1.02 (derived). So `ht` lists ASHRAE
  midpoints.

### 1.2 Maximum temperature

- **No rating found** for building brick (ASTM C62 or C216 brick) from a standard or a maker.
  NOT FOUND.
- Context, not a rating:
  - EPA AP-42 §11.3: in a tunnel kiln "the firing zone typically is maintained at a maximum
    temperature of about 2000°F (1090°C)" [M5]. Building brick is fired at about this temperature.
  - Whitacre Greer's red firebox brick ("WG Low-duty Firebrick Red", ASTM C1261 only, P.C.E. 13
    min, fired at 2000 °F) has a "Recommended maximum operating Temperature = 1750°F" (954 °C) [M6].
    That is a firebox brick, not a building brick.
  - A 2020 review of clay brick masonry [M7]: after exposure to 600 °C or less, residual compressive
    strength falls linearly with temperature, to about 56.2 % at 600 °C. China's CECS 252-2009 (as
    quoted there) holds that residual strength does not fall for exposures up to 700 °C. The
    strength reduction factor *at* 1000 °C is 0.53. Verified.

### 1.3 Notes and disagreements

- Only one source gives building-brick k at high temperature: Lienhard's single value of 0.7 W/(m·K)
  over 0–1000 °C. It is a rounded compilation value, with no density. **One source only.**
- That 0.7 agrees with ASHRAE at 1600 kg/m³ (0.675 via `ht`) and with Olsen's 100 lb/ft³. Dense
  modern face brick (1920–2080 kg/m³) is 0.81–1.12 W/(m·K) at room temperature, 15–60 % higher.
- EN 1996-1-2 (Eurocode 6, fire) Annex D has curves of k against temperature for clay masonry. The
  numbers were not read. A 2009 Eurocode training talk by the German clay unit producers' association
  says Annex D "contains results from a very limited number of tests", that "the diagrams show some
  strange effects", and that the values "should only be used for a very rough assessment" [M8].
  Its slide of Diagram D.1(b) gives λ(20 °C) = 1.0 W/(m·K), c(20 °C) = 1020 J/(kg·K) and
  ρ(20 °C) = 1600–2000 kg/m³ for one material, but does not name it [M8].
- Moisture raises k. All values above are for dry or conditioned brick.

---

## 2. Fireclay firebrick by ASTM C27 class

### 2.1 Class names

- ASTM C27 fireclay classes: super-duty, high-duty, medium-duty, low-duty and semi-silica. Olsen's
  Table 1-2 calls the medium class "Intermediate-duty", PCE 29 (`kiln-reference.md`, Dense brick).
- Mt. Savage's medium-duty sheet is headed "Medium Duty" and says the brick is "Designed to satisfy
  requirements for intermediate (moderate) duty service", PCE 29 [M11]. So Olsen's
  "intermediate-duty" is ASTM medium-duty.

### 2.2 Maker data sheets

k in Btu·in/(h·ft²·°F), with W/(m·°C) as printed in brackets. The sheets print the °C mean
temperatures as 205, 425, 650, 870, 1095 and 1315 °C.

| Product | ASTM C27 class | PCE | Bulk density | Max service | k 400 °F | 800 °F | 1200 °F | 1600 °F | 2000 °F | 2400 °F | Status | Tag |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Alsey Smithfield Unbranded, dry press (rev. 13 Aug 2012) | Medium duty; also certified to low duty | 29 | 130.2 lb/ft³ (2086 kg/m³), porosity 21.3 % | 2700 °F (1482 °C) | 8.2 (1.18) | 8.5 (1.23) | 9.0 (1.30) | 9.2 (1.33) | 9.5 (1.37) | 9.8 (1.41) | Verified | [M9] |
| Alsey Jet D.P., dry press (rev. 12 Apr 2013) | High duty | 32–32½ | 133.7 lb/ft³ (2142 kg/m³), porosity 19.9 % | 2850 °F (1566 °C) | 8.2 (1.18) | 8.5 (1.23) | 9.0 (1.30) | 9.2 (1.33) | 9.5 (1.37) | 9.8 (1.41) | Verified | [M10] |
| Mt. Savage Medium Duty, dry press | C27, "intermediate (moderate) duty" | 29 | 129–133 lb/ft³ (2066–2130 kg/m³), porosity 16–18.5 % | not stated | not given | | | | | | Verified | [M11] |
| Mt. Savage Hi-Heat, dry press | C27 Regular High-Heat Duty | 31½–32 | 132 lb/ft³ (2114 kg/m³), porosity 17.5–19 % | not stated | not given | | | | | | Verified | [M12] |
| WG Low-duty Firebrick Buff, vacuum dry press (16 Feb 2026) | Low duty (C27 and C1261) | 15 min | not given; apparent porosity 13–17 % | 2000 °F (1093 °C) | not given | | | | | | Verified | [M6] |
| WG Low-duty Firebrick Red (16 Feb 2026) | C1261 only | 13 min | not given; apparent porosity 13–17 % | 1750 °F (954 °C) | not given | | | | | | Verified | [M6] |
| HWI KX-99 (already in the library) | Super duty | – | 142 lb/ft³ | 3200 °F | 9.7 | 9.8 | 10.0 | 10.3 | 10.7 | – | Excerpt | `electric-and-thermal.md` §4.2 [S35] |

- Alumina: Smithfield 30.78 %, Jet D.P. 37.63 %, Mt. Savage medium 32.90 %, Mt. Savage Hi-Heat
  35.7 %, WG Buff 27.6 %, WG Red 26.1 %.
- Neither Alsey sheet names the test method for k.
- The WG Red sheet prints SiO₂ as "6.2%". The listed oxides then add to only 43.7 %, so 62 % is
  probably meant (flagged).

### 2.3 Generic fireclay k(T): VDI Heat Atlas

From the VDI Heat Atlas, 2nd ed. (Springer 2010), as transcribed in the `ht` library's
`refractories` table [M2]. The table has five temperatures, 673.15–1473.15 K.

| Material | Density | k at 400 °C | 600 °C | 800 °C | 1000 °C | 1200 °C | c_p at the same temperatures, J/(kg·K) | Status |
|---|---|---|---|---|---|---|---|---|
| Fireclay | 2150 kg/m³ | 1.05 | 1.10 | 1.15 | 1.18 | 1.22 | 956 / 997 / 1021 / 1037 / 1054 | Verified (secondary) |
| High-duty fireclay | 2320 kg/m³ | 1.20 | 1.27 | 1.33 | 1.38 | 1.42 | 958 / 999 / 1024 / 1040 / 1058 | Verified (secondary) |
| Silica (silica brick, not semi-silica) | 1820 kg/m³ | 1.20 | 1.36 | 1.51 | 1.64 | 1.76 | 915 / 944 / 961 / 969 / 979 | Verified (secondary) |

k in W/(m·K). Other single values: Lienhard, "Clay, Fireclay", 500–750 °C, 1.0 W/(m·K) [M1];
Engineering ToolBox, "Fire-clay brick 500 oC 1.4" and "Chamotte, fireclay 1.4" [M4].

### 2.4 Notes and disagreements

- **Alsey prints the same k table on the medium-duty and the high-duty sheet.** So it is a typical
  fireclay curve, not a separate measurement of each brick.
- Agreement is fair. At 1000 °C: Alsey about 1.35 W/(m·K) (derived, linear between 871 °C, 1.327,
  and 1093 °C, 1.370); VDI fireclay 1.18; VDI high-duty 1.38; HWI KX-99 super-duty about 1.5
  (derived the same way from its 10.3 and 10.7 Btu·in/(h·ft²·°F) at 1600 and 2000 °F).
  Alsey sits about 15 % above VDI "Fireclay" and on VDI "High-duty fireclay".
- **Correction to [S92].** `electric-and-thermal.md` §4.2 cites "a Plibrico fireclay brick sheet"
  for 8.2 Btu·in at 400 °F to 9.5 at 2000 °F [S92]. Those figures are on the Alsey sheets [M9] [M10].
  The file now served at the [S92] address is a Plibrico "Super Demon Air Set Mortar" sheet
  (8/23/2006) whose conductivity cells are blank [M13]. Re-tag the figures to [M9] / [M10].
- Allied's medium-duty brick [S36] (32.9 % Al₂O₃, 129–133 lb/ft³) has the same numbers as the
  Mt. Savage medium-duty sheet [M11]. Treat them as one product, not two sources.
- Low duty: the only low-duty k found is Alsey's shared table, through Smithfield's dual
  certification. Low-duty ratings differ a lot: 2700 °F (Smithfield), 2000 °F (WG Buff), 1750 °F
  (WG Red, C1261 only).
- Semi-silica: no maker sheet with k or density found. NOT FOUND. Olsen's Table 1-2 has the class
  limits only (`kiln-reference.md`).

---

## 3. Granite and fieldstone

### 3.1 k against temperature

Seipold (GFZ Potsdam, 2001) measured many crystalline rocks to 1000 °C [M14]. The high-temperature
runs were made at normal (atmospheric) pressure, always with temperature rising, by a transient
pulse method: a heater wire and a thermocouple inside the sample, in a tube furnace ([M14],
pp.22–24). His mean curve for granites, fitted for 250–1000 K, is ([M14], p.92):

  λ = 1/(0.156 + 5.45·10⁻⁴·T) + 0.763·10⁻⁹·T³, with T in K and λ in W/(m·K).

The second term is radiation. Values from the curve (derived):

| °C | K | k, W/(m·K) |
|---|---|---|
| 0 | 273.15 | 3.30 |
| 20 | 293.15 | 3.19 |
| 100 | 373.15 | 2.82 |
| 200 | 473.15 | 2.50 |
| 300 | 573.15 | 2.28 |
| 400 | 673.15 | 2.15 |
| 500 | 773.15 | 2.08 |
| 600 | 873.15 | 2.09 |
| 700 | 973.15 | 2.16 |
| 726.85 | 1000 (end of fit) | 2.19 |

- One granite (Z1.3) was measured from 850 K to almost 1300 K at fine steps. Seipold saw no notable
  rise in k from partial melting, at test temperatures "partly over 1000 °C", where granitoid rocks
  are well into partial melting ([M14], p.53). The fit to that sample is not used here.
- On cooling from a high temperature, k is a little lower than on first heating; reheating gives
  the first-heating values again. Cracking starts progressively above 300–400 °C. Above that, the
  further fall is a few tenths of a W/(m·K) ([M14], p.23).

### 3.2 Room-temperature values and density

| Source | Material | Density | Temperature | k, W/(m·K) | c_p, J/(kg·K) | Status | Tag |
|---|---|---|---|---|---|---|---|
| Lienhard, Table A.2 | Granite (NTS) | ≈2640 kg/m³ | 20 °C | 1.6 | ≈820 | Verified (secondary) | [M1] |
| `ht` (DIN EN 12524:2000) | Stone, granite | 2600 kg/m³ | room | 2.8 | 1000 | Verified (secondary) | [M2] |
| `ht` (DIN EN 12524:2000) | Natural crystalline rock | 2800 kg/m³ | room | 3.5 | 1000 | Verified (secondary) | [M2] |
| `ht` (ASHRAE 2013) | Calcitic, dolomitic, limestone, marble and granite | 2880 / 2560 / 2240 / 1920 / 1600 kg/m³ | room | 4.33 / 3.17 / 2.31 / 1.59 / 1.15 | 880 (1920 kg/m³ row only) | Verified (secondary) | [M2] |
| Engineering ToolBox | Granite | not given | not stated | 1.7–4.0 | – | Verified | [M4] |
| Olsen p.295 | Granite or limestone | 165 lb/ft³ (2643 kg/m³) | – | – | – | Read (`kiln-reference.md`) | Olsen |
| Seipold mean curve | Granites | not given | 20 °C | 3.19 (derived, §3.1) | – | Derived | [M14] |

### 3.3 Notes

- Granite k at room temperature spans about 1.6 to 4 W/(m·K). Seipold's mean (3.19 at 20 °C) is at
  the high end, and Lienhard's NTS granite (1.6) at the low end. Quartz content drives this.
- Density agrees: about 2600–2650 kg/m³ from Lienhard, EN 12524 and Olsen.
- Quartz inverts at 573 °C (`castables.md` §3). In Seipold's thermal-cracking runs on granite,
  cracks formed mainly at grain boundaries. Cracks inside grains, mostly feldspar, became common
  only at 500 °C and especially at 600 °C. The 600 °C run was already above the quartz α–β
  inversion ([M14], p.85).
- Maximum service temperature: no rating found. NOT FOUND.
- A folk-kiln wall is rubble in clay or lime mortar, with voids. No source gives k for such a wall.
- Lead not followed up: Vosteen and Schellschmidt (2003) give a k(T) law for crystalline rocks,
  checked from 0 to 500 °C, with constants a = 0.0030 ± 0.0015 and b = 0.0042 ± 0.0006 (Excerpt
  [M15]). The equation itself was not read.

---

## 4. Unfired clay: adobe, raw clay blocks, cob, rammed earth

### 4.1 Values

| Source | Material | Density | Temperature or state | k, W/(m·K) | c_p, J/(kg·K) | Status | Tag |
|---|---|---|---|---|---|---|---|
| Lienhard, Table A.2 | Clay, sandy clay | 1780 kg/m³ | 20 °C | 0.9 | – | Verified (secondary) | [M1] |
| Lienhard, Table A.2 | Soil (mineral), dry | 1500 kg/m³ | 15 °C | 1 (one significant figure) | 1840 | Verified (secondary) | [M1] |
| Lienhard, Table A.2 | Soil (mineral), wet | 1930 kg/m³ | 15 °C | 2 (one significant figure) | – | Verified (secondary) | [M1] |
| Lienhard, Table A.2 | Soil, clays, dry to wet | – | – | 1.1–1.6 | – | Verified (secondary) | [M1] |
| Mosquera et al. 2014 | Adobe, dry | not in abstract | 19 °C, 41 % RH | 0.80 ± 10 % | – | Verified (abstract) | [M16] |
| Mosquera et al. 2014 | Adobe, 1.67 % natural moisture | not in abstract | 19 °C | 0.90 ± 10 % | – | Verified (abstract) | [M16] |
| Molina et al. 2021 | Adobe (Peru) | 1570 ± 62 kg/m³ | – | not measured | 1209 ± 93 | Verified (abstract) | [M17] |
| Solà and Ros 2014, quoted by Petcu et al. 2023 | Rammed earth | 1400 / 1600 / 1800 / 1900 kg/m³ | not stated | 0.60 / 0.80 / 1.00 / 1.20 | – | Verified (secondary) | [M18] |
| Petcu et al. 2023 | Compacted clays, 12 samples (§4.2) | 1490–2150 kg/m³ | see §4.2 | 0.523–1.209 | 701–999 | Verified | [M18] |
| `ht` (DIN EN 12524:2000) | Clay or silt (ground) | 1500 kg/m³ | room | 1.5 | 2085 | Verified (secondary) | [M2] |
| Engineering ToolBox | Clay, dry to moist / Earth, dry | – | – | 0.15–1.8 / 1.5 | – | Verified | [M4] |
| Goodhew, Grindley and Probert 1995 | Cob, "normally-moist state" | – | – | about 0.6 | – | Excerpt | [M19] |
| Olsen p.295 | Fire clay / loam dry packed / dense mud | 85 / 95 / 125 lb/ft³ | – | – | – | Read (`kiln-reference.md`) | Olsen |

- Mosquera et al. measured with a thermal needle probe over 10 min [M16].
- Olsen's weights are bulk weights of loose or wet material, not block densities.

### 4.2 Petcu et al. 2023, Table 5 (twelve compacted clays)

Measured with an ISOMET 2114 (transient method) on samples after an oedometer test [M18]. The
moisture state at test is not stated. The clays' natural water content was 18–22 % (their Table 3),
so the samples were probably moist.

| Sample | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 | S10 | S11 | S12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Density, kg/m³ | 2073 | 1917 | 1994 | 1729 | 1490 | 1913 | 1923 | 1827 | 2150 | 1886 | 1739 | 1641 |
| k, W/(m·K) | 1.146 | 0.882 | 0.930 | 0.679 | 0.523 | 0.931 | 0.988 | 0.552 | 1.209 | 1.040 | 0.716 | 0.839 |
| c_p, J/(kg·K) | 701 | 776 | 765 | 803 | 999 | 764 | 816 | 815 | 736 | 830 | 794 | 917 |

### 4.3 Notes

- Earth k depends mainly on density and moisture. The sources span about 0.5–1.6 W/(m·K) for
  dry-to-damp earth, and about 2 when wet (Lienhard's wet soil).
- No source gives k of unfired clay above room temperature. NOT FOUND. In a kiln the hot side of a
  raw-clay wall dries, then fires in place. Hotchkiss's raw blocks blew out if the first firing was
  fast (`olsen-kilns.md`, `hotchkiss-raw-clay`). For the fired state, see §4a.
- Maximum service temperature: none found. NOT FOUND.

---

## 4a. Raw clay fired in place

Checked 2026-10-29. Two Olsen kilns have walls of raw clay that fire where they stand:
`hotchkiss-raw-clay` (raw blocks of 50 % Lincoln 60 fireclay and 50 % coarse sand, laid in the
same mix, p.33, pp.54–57) and `anagama-hole` (a tube dug into a clay hill, walls "ground clay
bisque", pp.83–84) (`olsen-kilns.md`). The hypothesis tested here is the user's: **fired raw clay
is likely between low-duty and medium-duty hard firebrick.** The answer is in §4a.7.

### 4a.1 The clay: Lincoln 60 is not "Lincoln Fireclay"

Olsen names "Lincoln 60 fireclay" from Lincoln, California (p.54). Digitalfire lists two different
clays under similar names.

| Property | Lincoln 60 (Gladding McBean, Lincoln, CA) | Lincoln Fireclay (North American Refractories) |
|---|---|---|
| Description | "Dark buff-firing plastic stoneware"; used since the late 1800s, first for sewer pipe; "Is Lincoln #60 a really fireclay? Absolutely not!" | "a distinct clay from Lincoln 60 Clay"; closer to Greenstripe |
| SiO₂ / Al₂O₃ / Fe₂O₃ / TiO₂, % | 52.00 / 32.50 / 2.20 / – | 58.20 / 26.60 / 1.85 / 1.65 |
| K₂O / Na₂O / MgO / CaO, % | 0.75 / 0.30 / 0.60 / 0.20 | – |
| LOI, % | 11.20 | 10.25 |
| PCE | 31 ("claimed") | 31 |
| Drying shrinkage | 5.5–6.0 % at 27 % water | 6.0 % |
| Firing shrinkage | cone 6: 7.5 %; cone 7: 8.0 %; cone 8: 8.5 %; cone 10: 8.0 % | – |
| Water absorption | cone 6: 3.0 %; cone 7: 2.5 %; cone 8: 1.5 %; cone 10: 0.2 % | – |
| Firing behaviour | "completely vitrifies by cone 10 (where it is near zero porosity)"; bloating begins at cone 11; shrinkage peaks at cone 8, then the clay expands (over-firing) | – |
| Status, tag | Verified (secondary) [M29] | Verified (secondary), `castables.md` [S29] |

- `castables.md` §4.1 and `castables-minerals.md` §7 quote the Lincoln Fireclay figures. They are
  not the clay Hotchkiss used (§6).
- A Lincoln-pit technical sheet dated 07/09/02 was posted on the Ceramic Arts forum (SiO₂ 54.31,
  Al₂O₃ 24.49, Fe₂O₃ 1.92, K₂O 2.02, TiO₂ 2.23, LOI 9.50 %, per a search extract). The page
  refused the fetch. Excerpt only; it disagrees with Digitalfire's analysis.

### 4a.2 What the 50/50 body is, by chemistry

Olsen does not say whether 50/50 is by weight or by volume, or what the sand is. Taking it by
weight, with the sand as pure quartz (both assumptions), and Lincoln 60 as in §4a.1 (Derived):

- 100 g of dry mix = 50 g clay + 50 g sand. The clay keeps its oxides, 88.55 % of its weight
  (the LOI of 11.2 % burns off): 44.3 g. Fired mass 44.3 + 50 = 94.3 g.
- SiO₂ = (0.5 × 52.0 + 50)/94.3 = 80.6 %; Al₂O₃ = 0.5 × 32.5/94.3 = 17.2 %; Fe₂O₃ 1.2 %;
  K₂O + Na₂O 0.56 %; MgO + CaO 0.4 %.
- If the sand is not pure quartz, silica is lower and the fluxes higher.

| Class or body | SiO₂, % | Al₂O₃, % | PCE | Other | Status | Source |
|---|---|---|---|---|---|---|
| 50/50 Lincoln 60 and quartz sand, fired | 80.6 | 17.2 | NOT FOUND | – | Derived | above |
| Lincoln 60 alone, fired basis | 58.7 | 36.7 | 31 (claimed) | vitrified by cone 10 | Derived from [M29] | §4a.1 |
| WG Low-duty Firebrick Buff | 63.5 | 27.6 | 15 min | apparent porosity 13–17 %; fired at 2000 °F (1093 °C); maximum operating 2000 °F | Verified | [M6] |
| Alsey Smithfield (medium, also low duty) | – | 30.78 | 29 | porosity 21.3 % | Verified | [M9] |
| ASTM C27 semi-silica (Olsen's Table 1-2) | 72 min | – | 31½ | hot-load subsidence 1.5 % max at 2460 °F (1349 °C); MOR 300 psi min | Read | `kiln-reference.md` |
| Institution of Gas Engineers (UK), "siliceous" brick, as Searle quotes it | 80–92 | – | cone 29 | – | Verified | [M28] p.32 |

Searle on bricks of clay and silica [M28] (pp.39–40, Verified):

- Bricks made of a mixture of silica and clay are "semi-silica" or "ganister" bricks. Those with
  more clay, "though not necessarily as much as 50 per cent", are usually called semi-silica.
- Semi-silica bricks "are intermediate between fireclay and silica bricks, and have the advantage
  of being almost constant in volume when reheated. This is due to the effect of the shrinkage of
  the clay being neutralized by the expansion of the silica."
- "The addition of silica to a refractory clay often reduces its refractoriness considerably,
  though if the clay is of low refractoriness the addition of silica may raise its softening
  point."
- Semi-silica bricks carry more load at high temperature than fireclay bricks, but less than silica
  bricks, and they are used "where constancy of volume is the first consideration".

### 4a.3 Conductivity of fired clay bodies against temperature

Norton, *Refractories* (1942), Table 76, "Heavy Refractories", read on the page image [M27]. k in
Btu·in/(h·ft²·°F) at the mean temperature; W/(m·K) below each row (Derived, × 0.144228). The mean
temperatures are 204, 427, 649, 871, 1093 and 1316 °C. No densities are printed.

| Brick | Porosity, % | 400 °F | 800 °F | 1200 °F | 1600 °F | 2000 °F | 2400 °F | Authority (Norton's) | Status |
|---|---|---|---|---|---|---|---|---|---|
| Fireclay | 15.2 | 8.1 | 8.4 | 10.1 | 10.8 | 11.4 | 12.0 | Wilkes 1934 | Verified (secondary) |
| | | 1.17 | 1.21 | 1.46 | 1.56 | 1.64 | 1.73 | | Derived |
| Fireclay | 18.4 | 7.3 | 8.7 | 9.8 | 10.6 | 11.6 | 11.8 | Norton 1927 | Verified (secondary) |
| | | 1.05 | 1.25 | 1.41 | 1.53 | 1.67 | 1.70 | | Derived |
| Fireclay | 26.7 | 7.0 | 7.8 | 8.7 | 9.3 | 10.2 | 10.5 | Norton 1927 | Verified (secondary) |
| | | 1.01 | 1.12 | 1.25 | 1.34 | 1.47 | 1.51 | | Derived |
| Silica | 28.0 | 6.5 | 8.5 | 10.5 | 12.4 | 14.0 | 15.7 | Austin and Pierce | Verified (secondary) |
| Silica | 30.4 | 8.1 | 10.0 | 11.8 | 13.0 | 14.2 | 15.3 | Norton 1927 | Verified (secondary) |

Other fired fireclay bodies with k at temperature:

| Source | Material | Density | Porosity | k, W/(m·K) | Status | Tag |
|---|---|---|---|---|---|---|
| Mathios, "Firebrick Lava" (fireplace brick) | Al₂O₃ 32–33, SiO₂ 61–62, Fe₂O₃ 1.4–1.5 %; refractoriness 1650 °C; refractoriness under load 1250 °C | printed "2.15 kg/ m3" (2.15 g/cm³ meant, flagged) | ≤ 16 % | 0.95 at 105 °C; 1.10 at 650 °C; 1.30 at 1100 °C | Verified | [M30] |
| Aliprandi 1987, as quoted by Allegretta et al. | fireclay refractories | – | – | 1.2–1.5 at 1300–1500 °C | Verified (secondary) | [M26] |
| VDI Heat Atlas | Fireclay; Silica | 2150; 1820 kg/m³ | – | §2.3 | Verified (secondary) | [M2] |

- Norton warns: "Owing to experimental difficulties, the values for heavy refractories cannot be
  depended on closely" [M27]. His 1931 first edition prints the same three fireclay rows (OCR text
  read), so the transcription holds; it is the same author, not a second source.
- Porosity matters less than expected. From 18.4 to 26.7 % porosity, Norton's k falls by only
  4–12 % (Derived: ratios 0.96, 0.90, 0.89, 0.88, 0.88, 0.89 at the six temperatures).
- Sources disagree more than porosity does. At 1000 °C (Derived, linear between table points):
  Norton 26.7 % 1.42, Norton 18.4 % 1.61, Alsey 1.35 (§2.4), VDI fireclay 1.18 W/(m·K).
- Density of Norton's 26.7 % brick (Derived): the makers' sheets in §2.2 give an apparent solid
  density of bulk ÷ (1 − porosity) = 2086/0.787 = 2651 (Smithfield), 2142/0.801 = 2674 (Jet D.P.)
  and about 2535 kg/m³ (Mt. Savage). At 26.7 % porosity that is 1860–1960 kg/m³; about 1900. Norton
  does not say whether his porosity is apparent or true.

### 4a.4 Conductivity against firing temperature and quartz content

Allegretta, Eramo, Pinto and Hein (2017) fired four natural clays at 950–1350 °C and measured k
with a modified Lee's disk, its heater set at 120, 220 and 370 °C [M26]. Disks 30 mm × 7 mm,
pressed at 25 MPa with 5 % water, fired at 150 °C/h with a 1 h soak; open porosity by EN 993-1; k
not corrected for porosity. Only values printed in the text are given; the tables did not survive
in the accepted manuscript that was read.

| Clay | Make-up | Fired at | k, W/(m·K), heater at 120–370 °C | Porosity | Status |
|---|---|---|---|---|---|
| BAR1 (Swiss "clayey sand", glass-furnace refractory earth) | quartz up to ~75 wt %, kaolinite 19 wt %, 65 % sand-sized | 950 °C | comparable to the 1150 °C value | – | Verified |
| | | 1150 °C | 0.64 | no densification up to 1150 °C | Verified |
| | | 1250–1350 °C | 0.99–1.20 | open porosity about 10 % at 1350 °C | Verified |
| BAR2 | quartz up to ~75 wt %, kaolinite 21 wt %, 55 % sand-sized | 1150 °C | 0.73 | – | Verified |
| | | 1250–1350 °C | 1.09–1.37 | about 10 % at 1350 °C | Verified |
| BAR1 and BAR2 | | 1350 °C | 0.99–1.13 | about 10 % | Verified |
| ARG (fine kaolinitic, ~55 % kaolinite) | | 950 → 1150 °C | 0.63–0.67 → 1.17–1.22; constant above 1150 °C | 0.32 → 0.08, or → 0.01 (the text gives both; fraction) | Verified |
| SIF (glaucophane-rich, Fe₂O₃ 11.45 %) | | 950 °C | 1.03–1.07 | – | Verified |
| | | 1150 °C | 1.56 at 120 °C, 1.45 at 370 °C; melted above 1150 °C | 0.04 | Verified |

What the paper finds [M26]:

- Porosity is the main control. Mullite (ARG) and cristobalite (BAR) add to k as they form.
- "In samples in which quartz exceeds 50 wt%, the ceramics' thermal conductivity decreases because
  of fissures and detachment zones formed after the α-β quartz phase transition." The BAR bodies
  (50–80 % quartz) also lose k as the test temperature rises, except those fired at 1150 °C.
- Earlier work it cites: quartz or granite temper raises k up to about 10–15 %, then lowers it, from
  expansion mismatch and the α–β transition around the grains.
- In BAR1 and BAR2, cristobalite grew from 2.8 to 13.4 wt % and from 3.5 to 17.8 wt % between
  1150 and 1350 °C firing (1 h soaks).
- Clayey sands like BAR served in 17th–18th-century forest glass furnaces at 1300–1500 °C. Purer
  clayey sands are up to 99 % SiO₂ + Al₂O₃, "with an eutectic of about 1600 °C" (Aramaki and Roy
  1962, as cited).

The BAR clays hold less clay and more quartz than a 50/50 fireclay–sand mix, and were pressed at
25 MPa, so a hand-moulded block is likely more porous. They bracket the quartz-rich end.

### 4a.5 Low-duty brick: what is known

- k of a low-duty-only brick: NOT FOUND. The only low-duty k is Alsey's shared table, through
  Smithfield's dual certification (§2.4).
- WG's low-duty bricks [M6] (Verified) are vacuum dry pressed, fired at only 2000 °F (1093 °C), with
  apparent porosity 13–17 %. Buff: PCE 15 min, MOR 600 psi min, maximum operating 2000 °F. Red
  (C1261 only): PCE 13 min, MOR 500 psi min, maximum 1750 °F. Bulk density is not given.
- Olsen (p.17–18, Read, `kiln-reference.md`): low- and intermediate-duty bricks suit potters'
  kilns except fireboxes; intermediate is well suited to about cone 10; a low-duty brick of PCE 28
  stands cone 10 in a kiln but not in a firebox.

### 4a.6 Walls fired in place

Measured temperatures through a clay kiln wall. Campus Galli open-air museum, Germany: an updraft
kiln built in 2016 of local calcareous and non-calcareous clays mixed with dung and sand. Four
thermocouples sat in a large block built into the wall, 5 cm apart, starting from the inner side.
One firing of about 16½ h, with about 1100 °C reached just above the floor [M31] (Verified):

| Block thermocouple | Depth from the inner side (5 cm spacing) | Peak, °C | Clay state afterwards |
|---|---|---|---|
| TC1 | innermost | 878.4 | kaolinite gone (XRD and FTIR); calcite starting to decompose; organics burnt |
| TC2 | 5 cm further out | 542.3 | kaolinite bands gone in FTIR, still seen in XRD; organics charred |
| TC3 | 10 cm | 268.1 | kaolinite present; no significant change in FTIR; organics starting to burn, vegetal fibres still visible |
| TC4 | 15 cm | 124.7 | as TC3 |

- The paper: wall temperatures "were drastically lower than inside the kiln", 124–542 °C away from
  the flames and 878 °C only on the side touching the firing chamber. Cracks opened during firing
  and were patched with ash, water and cob. The kiln "is still in use today".
- These are peaks in one transient firing, not a steady state. They show how thin the fired skin
  is after one firing: kaolinite survived beyond the first 5 cm.
- The Hotchkiss kiln was fired for many years. Olsen: still firing after 30 years (p.33). A page
  dated 15 April 2023 says the multi-chambered wood-fired kiln "he built 51 years ago with students
  ... is still being fired today" [M32] (Verified). A listing for a "136th" firing of "a historic
  six-chambered, wood-fired climbing kiln built in 1971" at Woolman, Nevada City, California,
  designed by Dik Hotchkiss, asks for "high-fire work" [M32] (Excerpt). It is very likely the same
  kiln, but the listing does not mention raw clay.
- Dug anagama: a New Zealand page says the originals were dug into a clay hillside and that "on the
  first firing the clay vitrified to form a strong long lasting kiln" [M33] (Excerpt; the page
  refused the fetch). Olsen's `anagama-hole` fired "for weeks" to bisque the walls (pp.83–84).
- k of a wall fired in place, and steady temperatures through one in long service: NOT FOUND.

### 4a.7 The hypothesis: between low-duty and medium-duty firebrick?

**Partly. It holds for the fired face's conductivity, it needs refining for refractoriness, and it
does not hold for the wall as a whole.**

- **Conductivity of the fired face: yes, as dense fireclay brick, but "between low and medium"
  can't be tested.** Fireclay brick of 15–27 % porosity runs about 1.0–1.7 W/(m·K) over 200–1300 °C
  [M27], and 27 % porosity costs only 4–12 % against 18 %. Quartz-rich clayey sands fired at
  1250–1350 °C measure 0.99–1.37 W/(m·K), heater at 120–370 °C [M26], inside the same band. No
  source gives low-duty brick a k of its own: Alsey prints one table for its low-, medium- and
  high-duty bricks (§2.4). So the defensible statement is "about a porous dense fireclay brick".
- **Underfired zones conduct less.** The same clayey sands fired at 950–1150 °C measure 0.64–0.73
  W/(m·K), 28–46 % below dense fireclay brick at a similar temperature (Derived: 0.73/1.01 and
  0.64/1.18, against Norton's 26.7 % brick and Smithfield at 400 °F). Beyond the fired skin the
  wall is raw clay: 0.5–1.2 W/(m·K) at room temperature, nothing above (§4). So the whole wall
  likely conducts less than a firebrick wall of the same thickness, not more (inference).
- **Refractoriness: refine.** By chemistry the body is off the fireclay scale. A 50/50 mix (by
  weight, quartz sand) fires to about 81 % SiO₂ and 17 % Al₂O₃ (§4a.2), the range of ASTM C27
  semi-silica (SiO₂ ≥ 72 %) and of the old IGE "siliceous" class. Low- and medium-duty bricks are
  26–33 % Al₂O₃. Searle puts semi-silica "intermediate between fireclay and silica bricks" and warns
  that silica "often reduces [a refractory clay's] refractoriness considerably" [M28]. No PCE or
  use limit for such a mix has been published: NOT FOUND.
- **The practical ceiling is the clay's.** By Digitalfire's account Lincoln 60 is a stoneware clay:
  near-zero porosity at cone 10 and bloating from cone 11, despite a claimed PCE 31 [M29]. The hot
  face is therefore likely limited near cone 10–11 (inference; the sand may move this, and no test
  shows by how much). That is where Olsen puts low- and intermediate-duty brick: cone 10 in a
  chamber, not a firebox. Olsen has the kiln still firing after 30 years, and a kiln Hotchkiss
  built with students about 51 years before 2023, very likely this one, was still fired in 2023
  [M32]. That is field evidence that the body survives decades of firing in the chambers. The
  cone isn't given; a firing listing asks for "high-fire work" (Excerpt).
- **The wall is graded, not a brick.** One firing fired only about the inner 5 cm of a clay wall
  (Campus Galli [M31]). Builders bisque the walls with long first firings (Olsen). A layered model,
  with a fired skin over raw clay, fits the evidence better than one material.

For the engine (suggestion only): take the fired zone as `fireclay-brick-porous-norton` (§7) with
no service limit, take the raw zone from §4 (room temperature only), and refuse above cone 10 or
in a firebox until a PCE or test firing of the body is found (ADR 0009). Using the dense-brick
curve for the whole wall would likely overstate the heat lost through it (inference).

---

## 5. Castables Olsen names

### 5.1 Morgan Thermal Ceramics Kaolite 2600-LI

k in W/(m·K), Btu·in/(h·ft²·°F) in brackets.

| Sheet | Placement | Max service | Density | k at 260 °C (500 °F) | 538 °C (1000 °F) | 816 °C (1500 °F) | 1093 °C (2000 °F) | Method | Status | Tag |
|---|---|---|---|---|---|---|---|---|---|---|
| Kaolite 2600LI Pump, code CA.89, 1 Jan 2025 (Americas) | cast by vibration, or pumped | 1427 °C (2600 °F) | dried 24 h at 105 °C: 1330–1570 kg/m³ (83–98 pcf); fired 5 h at 816 °C: 1201–1442 (75–90); net to place 1330 (83) | 0.39 (2.7) | 0.42 (2.9) | 0.43 (3.0) | 0.46 (3.2) | ASTM C417 | Verified | [M20] |
| Kaolite 2600LI Gun, code CA.120, 1 Jan 2025 (Americas) | gunned | 1427 °C (2600 °F) | dried: 1362–1538 (85–96 pcf); fired at 816 °C: 1250–1410 (79–89); net 1346 (84) | 0.42 (2.9) | 0.42 (2.9) | 0.43 (3.0) | 0.46 (3.2) | ASTM C417 | Verified | [M21] |
| Thermal Ceramics Kaolite range sheet (undated, before 2025) | cast or gunned | 1427 °C | fired at use limit: 1282–1410 kg/m³; at 816 °C: 1250–1410; 37 kg to place one cubic foot | 0.39 | 0.42 | 0.43 | 0.46 | label garbled | Verified (metric values only) | [M22] |
| Kaolite 2600LI D, rev. 2, 10 Jan 2011 (Dalian Morgan plant) | vibrocast | 1427 °C | fired to 815 °C: 1250–1410; material 1314 kg/m³ | – | 0.42 | – | – | ASTM where applicable | Verified | [M23] |

- The older range sheet's text layer garbles its Btu figures and most labels. Its metric figures in
  brackets read cleanly, and match the 2025 Pump sheet exactly.
- 37 kg = 81.6 lb (derived). Olsen's Table 1-5 gives 81 lb to cast 1 ft³ of Kaolite 2600-LI
  (`kiln-reference.md` §4). So Olsen's Kaolite 2600-LI is this product.
- The Dalian "Kaolite 2600LI Gun D" page prints its conductivity as "2.9" in W/mK. That is the Btu
  figure under a metric label (flagged). The Dalian sheets give k at 538 °C only.
- Chemistry (Pump sheet): Al₂O₃ 49, SiO₂ 34, Fe₂O₃ 1, TiO₂ 1.5, CaO 14.5 (11 reactive) %. The sheet
  says the rest of the CaO "is Calcia from the anorthite aggregate" [M20].
- Permanent linear change after 5 h at the maximum service temperature: −0.5 to −1.5 % (Pump, Gun,
  and Dalian sheets). Olsen prints "−.05 to +1.5" after 5 h at 2500 °F (flagged in
  `kiln-reference.md`). Morgan's figures suggest the "+1.5" is also a misprint for −1.5. The test
  temperatures differ (1427 °C against 1370 °C).

### 5.2 Morgan Firelite 2600LI (Europe)

Olsen writes that "Morgan Ceramics 2600 LI (Europe)" is similar to Kast-O-Lite 26 LI
(`kiln-reference.md`). Morgan's European 2600 LI castable is Firelite 2600LI [M24]:

| Sheet | Max service | Density | k at 200 °C | 400 °C | 600 °C | 800 °C | 1000 °C | Method | Status | Tag |
|---|---|---|---|---|---|---|---|---|---|---|
| Firelite 2600LI, code CA.25, 1 Jan 2025, made in Europe, cast | 1430 °C (2600 °F) | oven dried 110 °C: 1230 kg/m³ (76.8 pcf); after 5 h at 815 °C: 1140 (71.1) | 0.38 (2.64) | 0.38 (2.64) | 0.38 (2.64) | 0.39 (2.71) | 0.39 (2.71) | ASTM C201/417 | Verified | [M24] |

- It "Conforms to class Q and R of ASTM classification C-401-91". Al₂O₃ 61.6 %, Fe₂O₃ 0.7 %.
- That Olsen's "Morgan Ceramics 2600 LI (Europe)" is Firelite 2600LI is likely, not confirmed.

### 5.3 Is Olsen's "K-26 IFB castable" Kaolite 2600-LI?

Probably, but no source confirms it.

- For: Olsen uses Kaolite 2600-LI by name in Table 1-5 (`kiln-reference.md` §4), and his 3rd
  edition's cast-dome text says "a castable like Kaolite 2,500 or 2,600 LI" (`domes-over-doors.md`
  [D15], Excerpt). Kaolite 2600-LI is a Thermal Ceramics product rated 2600 °F, the K-26 rating.
  Its aggregate is anorthite [M20], as in Morgan's slurry-cast K-series IFB (`castables.md` §6.3).
  It is sold as "low iron" [M20] [M21], which fits the "2600 IFB (low iron) castable" of
  `hohr-2003`.
- Against or unknown: no source uses the names "K-26 LI" or "K-26 castable". Morgan also sells
  Firelite 2600LI (§5.2), another low-iron 2600 °F castable.

### 5.4 Coolcast 140

- **"Coolcast 140": NOT FOUND.** No data sheet, listing or mention found.
- The line is real. Thermal Ceramics Australia sold "Moral Coolcast" castables, for example
  "Moral Coolcast 100 LW-K" [M25]: 1100 °C rating; bulk density 510–590 kg/m³ at 110 °C, 438–512 at
  800 °C, 447–523 at 1000 °C; approximate k 0.14 at 250 °C, 0.16 at 500 °C, 0.17 at 750 °C (W/m·K);
  AS 1774 test methods "where applicable". Verified.
- A 2011 Thermal Ceramics product-information set names Coolcast grades by dried bulk density [M23].
  (The same file holds Kaolite "D" sheets made at Morgan's Dalian plant; the Coolcast sheets do not
  name a plant or region.) The numbered grades are all rated 1200 °C maximum service, and the sheets
  say densities of 750–1500 kg/m³ can be made:

  | Grade | Dried bulk density, kg/m³ | k at 600 °C, W/(m·K) |
  |---|---|---|
  | Coolcast 75 | 750 | 0.21 |
  | Coolcast 85 | 850 | 0.24 |
  | Coolcast 90 | 900 | 0.25 |
  | Coolcast 100 | 1000 | 0.28 |
  | Coolcast 110 | 1100 | 0.30 |
  | Coolcast 125 | 1250 | 0.33 |

  Plain Coolcast and Coolcast G are 750 kg/m³, 1100 °C, 0.22 at 600 °C. Tests are to "British
  Standard 1902 (where applicable)". Verified.
- Under that scheme "140" would mean about 1400 kg/m³ at a 1200 °C rating. But the Australian
  "Coolcast 100 LW-K" is 510–590 kg/m³ and 1100 °C, so the scheme does not carry across regions.
  Olsen calls "Coolcaste 140" similar to a 2600 °F castable (`kiln-reference.md` §4). None of this
  fixes the product. Do not infer its data.
- **The product's name** (2026-10-29): Morgan's safety data sheet IC2 (Abu Dhabi; first issued
  14 May 2015, revised 26 February 2025) lists "Moral Coolcast 110LW, 120LW, 120MW & 140MW" among
  its insulating castables, so Olsen's Coolcast 140 is **Moral Coolcast 140MW**, a medium-weight
  insulating castable [M34] (Verified, read in the PDF). The sheet gives the whole family's
  composition (alumino-silicate 30–65 %, cement over 20 %, clay 2–20 %, wollastonite under 15 % by
  weight) and one relative density for all of its products, "0.3 – 1.5 T/m³"; no conductivity, no
  service temperature and no density for 140MW alone. A search for a 140MW technical data sheet
  found none (LC 140 is a different, dense castable).
- **Not used:** an AI summary (Gemini, passed on by the user) gave 140MW 1300–1500 kg/m³, a
  1400 °C rating and k "estimations" of 0.40–0.62 W/(m·K), citing [M34]. None of those values is in
  [M34]; they stay out of the library until a data sheet gives them.

---

## 6. Findings that touch other research files

- `electric-and-thermal.md` §4.2 and its Corroboration row for KX-99: the "Plibrico" 8.2–9.5 figures
  are Alsey's (§2.4 above). The [S92] file is a mortar sheet with no conductivity values [M13].
- `electric-and-thermal.md` Gaps lists "Medium-duty dense brick k(T)". Now found: Alsey Smithfield
  [M9], with VDI fireclay [M2] as a second, generic source.
- `thermal-properties.md` §1 says c_p(T) for dense fireclay was not found. VDI gives it, 400–1200 °C
  (§2.3 above), through `ht` [M2].
- `thermal-properties.md` §1, row from [T2]: Lienhard's Table A.2 (v6.00) does print "Firebrick,
  insulating: 300 °C, 2000 kg/m³, 960 J/(kg·K), 0.1 W/(m·K), α 5.4 × 10⁻⁸ m²/s; 0.2 at 1000 °C"
  [M1]. So the scan was read correctly. The density is the book's, and it is implausible for IFB.
  The book's α agrees with that density: 0.1/(2000 × 960) = 5.2 × 10⁻⁸ m²/s (derived).
- `kiln-reference.md` §4: Morgan's −0.5 to −1.5 % for Kaolite 2600-LI supports reading Olsen's
  "+1.5" as −1.5 (§5.1).
- `castables.md` §4.1 and §11, and `castables-minerals.md` §3 and §7: the "Lincoln Fireclay" figures
  there (North American Refractories; PCE 31, drying 6.0 %) [S29] are not for the clay Hotchkiss
  used. Olsen names Lincoln 60 from Lincoln, California (p.54). Digitalfire says Lincoln Fireclay
  "was a distinct clay from Lincoln 60 Clay" [S29], and describes Lincoln 60 as a Gladding McBean
  stoneware clay that vitrifies by cone 10 and bloats at cone 11 (§4a.1) [M29]. The Lincoln 60
  quartz content is still NOT FOUND.

---

## 7. What the library can take

Suggestions only. Each row has k at two or more temperatures, a density and a source.

| Suggested id | Kind | Density | Max service | k points | Status | From |
|---|---|---|---|---|---|---|
| `building-brick-common` | new kind `building_brick` | 1600 kg/m³ (Olsen p.295) | null | W/(m·K), °C: [0, 0.7], [1000, 0.7] | verified | §1 [M1] |
| `firebrick-medium-duty-smithfield` | `dense_firebrick` | 130.2 lb/ft³ | 2700 °F | Btu·in/(h·ft²·°F), °F: [400, 8.2], [800, 8.5], [1200, 9.0], [1600, 9.2], [2000, 9.5], [2400, 9.8] | verified | §2.2 [M9] |
| `firebrick-high-duty-jet-dp` | `dense_firebrick` | 133.7 lb/ft³ | 2850 °F | same points as Smithfield | verified | §2.2 [M10] |
| `fireclay-brick-vdi` (generic) | `dense_firebrick` | 2150 kg/m³ | null | W/(m·K), °C: [400, 1.05], [600, 1.10], [800, 1.15], [1000, 1.18], [1200, 1.22] | verified (secondary) | §2.3 [M2] |
| `granite` | new kind `stone` | 2640 kg/m³ (Lienhard; Olsen 2643) | null | W/(m·K), °C: [0, 3.30], [100, 2.82], [200, 2.50], [300, 2.28], [400, 2.15], [500, 2.08], [600, 2.09], [700, 2.16] | derived | §3.1 [M14] |
| `kaolite-2600-li` | `insulating_castable` | 1450 kg/m³ (middle of 1330–1570 dried) | 1427 °C | W/(m·K), °C: [260, 0.39], [538, 0.42], [816, 0.43], [1093, 0.46] | verified | §5.1 [M20] |
| `firelite-2600li` | `insulating_castable` | 1230 kg/m³ (oven dried) | 1430 °C | W/(m·K), °C: [200, 0.38], [400, 0.38], [600, 0.38], [800, 0.39], [1000, 0.39] | verified | §5.2 [M24] |
| `fireclay-brick-porous-norton` | `dense_firebrick` | 1900 kg/m³ (derived from 26.7 % porosity; 1860–1960) | null | Btu·in/(h·ft²·°F), °F: [400, 7.0], [800, 7.8], [1200, 8.7], [1600, 9.3], [2000, 10.2], [2400, 10.5] | verified (secondary) for k; density derived | §4a.3 [M27] |

`fireclay-brick-porous-norton` is a measured fireclay brick, the most porous in Norton's table. It is
the best stand-in found for the fired zone of a raw-clay wall (`hotchkiss-raw-clay`,
`anagama-hole`), but it was not measured on that body (§4a.7). Name the wall's material as a proxy
if it is used.

Not enough data for an entry with k(T): unfired clay (room-temperature values only; Lienhard's
sandy clay, 1780 kg/m³ and 0.9 W/(m·K) at 20 °C, is the best single row), raw clay fired in place
as a body of its own (k above 370 °C, density and service limit all NOT FOUND; §4a), low-duty
firebrick on its own, semi-silica brick, and Coolcast 140.

---

## Corroboration

Resellers and forum copies of a maker's sheet are not independent of the maker. `ht`, BIA and
Lienhard's "fired clay" row all copy ASHRAE, so they count as one.

| Item | Independent sources | Agreement | Note |
|---|---|---|---|
| Building brick k at room temperature | 3: ASHRAE ([M1] [M2] [M3]), Lienhard "common" (Touloukian-based) [M1], Engineering ToolBox [M4] | 0.6–1.1 W/(m·K), by density | Fair |
| Building brick k up to 1000 °C | **1**: Lienhard [M1] | – | Single compiled value |
| Building brick max temperature | 0 | – | NOT FOUND; context only |
| Medium/high-duty fireclay k(T) | 2: Alsey [M9] [M10] (one maker, one shared table), VDI [M2]. Plus single values from Lienhard and ToolBox | within about 15 % | Alsey's two sheets are not independent of each other |
| Fireclay brick density by class | 2 makers: Alsey, Mt. Savage | medium 129–133 lb/ft³; high 132–134 | Good |
| Granite k(T) | **1**: Seipold [M14] | – | Room-temperature values from 4 sources spread 1.6–4 W/(m·K) |
| Granite density | 3: Lienhard, EN 12524 (via `ht`), Olsen | 2600–2650 kg/m³ | Good |
| Earth / adobe k at room temperature | 4+: Lienhard, Mosquera, Petcu, Solà and Ros, EN 12524 | 0.5–1.6 W/(m·K), by density and moisture | Wide but consistent |
| Kaolite 2600-LI k(T) | **1 maker**, 4 sheets [M20]–[M23] | identical | Proprietary; cannot reach three |
| Firelite 2600LI k(T) | **1 maker** [M24] | – | Proprietary |
| Fired fireclay body k(T), 15–27 % porosity | 4: Norton's table (Norton and Wilkes, two labs) [M27], VDI [M2], Alsey [M9], Mathios [M30] | 1.0–1.7 W/(m·K) over 200–1300 °C; at 1000 °C 1.18–1.61 | Fair; the sources differ more than 18 % and 27 % porosity do |
| Clay–sand body k against firing temperature | **1**: Allegretta et al. [M26] | – | Heater at 120–370 °C only |
| Low-duty brick k on its own | 0 (Alsey's shared table only) | – | NOT FOUND |
| Service limit of a fireclay–sand body | 0 | – | NOT FOUND; semi-silica class and Lincoln 60's cone 10–11 behaviour are context |
| Temperatures through a clay wall fired in place | **1**: Amicone et al. [M31], one firing | – | Transient peaks only |

---

## Gaps

- Building brick k measured at temperature, as a table of points. Only Lienhard's single value was
  found. Not reached: Harmathy, *Properties of Building Materials at Elevated Temperatures*, NRC
  Canada DBR Paper 1080 (1983); Al Nahhas et al., *Applied Thermal Engineering* 27 (2007) 258–267,
  on HAL (blocked by a bot check); the EN 1996-1-2 Annex D numbers.
- A maximum service temperature for building brick from a standard or maker.
- Low-duty firebrick: k(T) for a low-duty-only product, and the density of the WG bricks.
- Semi-silica firebrick: k, density, service limit.
- The k test method on the Alsey sheets.
- Maker sheets with k from HarbisonWalker (other than KX-99), Allied, Resco, Plibrico, Christy and
  Calderys fireclay brick: not found online.
- Granite: a service limit; the Vosteen and Schellschmidt equation (only its constants were seen);
  k of a mortared rubble wall; k after many firing cycles.
- Unfired clay: any k above room temperature; a single study giving both density and k for adobe;
  a verified cob value.
- Raw clay fired in place (§4a): k above 370 °C of a clay–sand body, with its density and porosity;
  the density of Hotchkiss's blocks; a PCE or use limit for a 50/50 Lincoln 60–sand body; whether
  Olsen's 50/50 is by weight or volume, and what the sand is; the fired depth and steady
  temperatures in a raw-clay or dug kiln after long service.
- Lincoln 60: a Gladding McBean data sheet and its free-quartz content. A 2002 Lincoln-pit sheet
  posted on the Ceramic Arts forum could not be opened.
- Papers not reached: Allegretta et al. 2017 Table 5 (only values in the text were read; the
  accepted manuscript lacks its tables); García-Ten et al. 2010, Parts I and II (k against bulk
  density and firing temperature); Michot et al. 2008 (kaolinite k after heat treatment; HAL bot
  check); Hein et al. 2008 and 2013 (archaeological and furnace ceramics; the hosting site serves a
  mismatched TLS certificate, so the PDFs were not downloaded); the TPRC data series vol. 2
  (lending-only on archive.org, 403 at DTIC).
- Kaolite 2600-LI: k above 1093 °C (rated to 1427 °C).
- "Coolcast 140" (Olsen's "Moral Coolcast 140", "Coolcaste 140"): any data. Ask Morgan Thermal
  Ceramics Australia.
- Whether Olsen's "K-26 IFB castable" / "K-26 LI castable" is Kaolite 2600-LI.

---

## Sources

- [M1] J. H. Lienhard V and J. H. Lienhard IV, *A Heat Transfer Textbook*, 6th ed., Phlogiston
  Press, 2024, version 6.00 dated 19 April 2024. Appendix A, Table A.2 "Properties of nonmetallic
  solids", pp.741–744; sources on pp.732–735 (Touloukian [A.2]; 2017 ASHRAE Handbook ch. 26
  [A.14]). PDF read. https://ahtt.mit.edu/wp-content/uploads/2024/04/AHTTv600.pdf
- [M2] C. Bell, `ht` library, `ht/insulation.py` (master branch, read 2026-10-29). Tables
  transcribed from the VDI Heat Atlas, 2nd ed. (Springer 2010), the ASHRAE Handbook: Fundamentals
  (2013) and DIN EN 12524:2000. https://raw.githubusercontent.com/CalebBell/ht/master/ht/insulation.py ;
  docs: https://ht.readthedocs.io/en/latest/ht.insulation.html
- [M3] Brick Industry Association, Technical Note 4, *Introduction to Energy Performance of Brick
  Masonry*, January 2016, Table 1 and notes a–c. PDF read.
  https://gobrick.com/media/file/4-introduction-to-energy-performance-of-brick-masonry.pdf
- [M4] Engineering ToolBox, Thermal conductivity of common materials (same page as [S37]).
  https://www.engineeringtoolbox.com/thermal-conductivity-d_429.html
- [M5] US EPA, AP-42 §11.3, Brick and Structural Clay Product Manufacturing (8/97), §11.3.2. PDF
  read. https://www.epa.gov/sites/default/files/2020-10/documents/c11s03.pdf
- [M6] Whitacre Greer, Product Data Sheets: WG Low-duty Firebrick Buff, and WG Low-duty Firebrick
  Red, both dated 16 February 2026. PDFs read.
  https://wgpaver.com/wp-content/uploads/Fire-Brick-Data-Sheet-Buff.pdf ;
  https://wgpaver.com/wp-content/uploads/Fire-Brick-Data-Sheet-Red.pdf
- [M7] Zheng W., Huang W., Wang Y., Jiao Z., "Influence of high temperature on compressive strength
  of clay brick masonry: a literature review" (in Chinese), *Journal of Harbin Institute of
  Technology* 52(11) (2020) 192–200, doi:10.11918/201907084. Page read.
  https://hit.ijournals.cn/html/hitxb_cn/2020/11/20201124.html
- [M8] U. Meyer (Arbeitsgemeinschaft Mauerziegel, Bonn), "Eurocode 6-1-2, Design of masonry
  structures, Structural fire design", Eurocodes training, Brussels, 2–3 April 2009, slides 6–8.
  PDF read. https://eurocodes.jrc.ec.europa.eu/sites/default/files/2022-06/3_am_Meyer.pdf
- [M9] Alsey Refractories, Product Data, Smithfield Unbranded Medium Duty Firebrick, revised
  13 August 2012. Forum copy, PDF read. https://community.fornobravo.com/filedata/fetch?id=308784
- [M10] Alsey Refractories, Product Data, Jet D.P. High Duty Firebrick, revised 12 April 2013.
  Reseller copy, PDF read. https://ssfbs.com/wp-content/uploads/2021/06/Jet_D.P._High_Duty_Firebrick_.pdf ;
  listing ("temperature use limit of 2850 F"): https://ssfbs.com/product/high-duty-1-arch-9-x-4-5-x-2-5/
- [M11] Mt. Savage Firebrick, Product Data, Medium Duty (code M959/01/06). Forum copy, PDF read.
  https://community.fornobravo.com/filedata/fetch?id=317702
- [M12] Mt. Savage Specialty Refractories, Hi-Heat High Duty Fireclay Brick, technical data (code
  3901). Forum copy, PDF read. https://community.fornobravo.com/filedata/fetch?id=317352
- [M13] Plibrico, Refractory Product Data Sheet, Super Demon Air Set Mortar - Dry (product 17003),
  data date 8/23/2006. The file now at the [S92] address. PDF read.
  https://community.fornobravo.com/filedata/fetch?id=284408
- [M14] U. Seipold, *Der Wärmetransport in kristallinen Gesteinen unter den Bedingungen der
  kontinentalen Kruste* (Heat transfer in crystalline rocks under the conditions of the continental
  crust), GFZ Potsdam Scientific Technical Report STR01/13, November 2001. Printed pages 22–24
  (high-temperature method), 53 (partial melting), 85 (thermal cracking of granite) and 91–92
  (mean curves). The report's section numbers differ between its contents list and its text, so
  pages are cited. PDF read.
  https://gfzpublic.gfz-potsdam.de/pubman/item/item_8538_2/component/file_10491/0113.pdf
- [M15] Vosteen and Schellschmidt, "Influence of temperature on thermal conductivity, thermal
  capacity and thermal diffusivity for different types of rock", *Physics and Chemistry of the
  Earth* 28 (2003) 499–509. Search extract only. Record:
  https://repository.geologyscience.ru/handle/123456789/35157 ; follow-up by Mottaghy et al. (2008):
  https://link.springer.com/article/10.1007/s00531-007-0238-3
- [M16] P. Mosquera, I. Cañas, J. Cid-Falceto, F. Marcos, "Determination of the Thermal Conductivity
  in Adobe With Several Models", *Journal of Heat Transfer* 136(3) (2014) 031303 (online
  28 November 2013), doi:10.1115/1.4025560. Abstract read through Crossref.
  https://api.crossref.org/works/10.1115/1.4025560
- [M17] J. O. Molina, H. F. Ríos, M. M. Gómez, M. J. Horn, "Thermophysical characterization of
  vernacular wall materials: measurements of specific heat and density", *Journal of Physics:
  Conference Series* 1841 (2021) 012011, doi:10.1088/1742-6596/1841/1/012011. Abstract read through
  Crossref. https://api.crossref.org/works/10.1088/1742-6596/1841/1/012011
- [M18] C. Petcu et al., "Thermophysical Characteristics of Clay for Efficient Rammed Earth Wall
  Construction", *Materials* 16(17) (2023) 6015, doi:10.3390/ma16176015. Full text read through
  Europe PMC (Tables 3 and 5; introduction quoting G. B. Solà and F. M. Ros, "Thermal improvement of
  rammed earth buildings by the inclusion of natural cork", ECPPM 2014, CRC Press, p.37).
  https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10488609/fullTextXML ;
  https://pmc.ncbi.nlm.nih.gov/articles/PMC10488609
- [M19] S. Goodhew, P. C. Grindley, S. D. Probert, cob thermal-probe study, WIT Transactions on the
  Built Environment vol. 16 (1995). Search extract only; the paper could not be opened.
  https://witpress.com/elibrary/wit-transactions-on-the-built-environment/16/10643
- [M20] Morgan Advanced Materials – Thermal Ceramics, Kaolite 2600LI Pump, Product Data Sheet, code
  CA.89, publication date 1 January 2025. PDF read.
  https://morganthermalceramics.com/media/cxtj5iyt/kaolite-2600li-pump_eng.pdf
- [M21] Morgan Advanced Materials – Thermal Ceramics, Kaolite 2600LI Gun, Product Data Sheet, code
  CA.120, publication date 1 January 2025. PDF read.
  https://www.morganthermalceramics.com/media/11772/kaolite-2600li-_eng.pdf
- [M22] Thermal Ceramics, *Kaolite Insulating Castables*, Product Information (range sheet, undated;
  footer names The Morgan Crucible Company plc). Distributor copy, PDF read; metric values only.
  https://jjmoroney.com/pdf/tc_kaolite2.pdf
- [M23] Thermal Ceramics, *Product Information: Insulating Castables* (Coolcast range, revision 5)
  and Kaolite D range (revision 2, made at the Dalian Morgan Refractory Plant under agreement with
  Thermal Ceramics Inc.), both dated 10 January 2011. Distributor copy, PDF read.
  https://www.taybac.com.vn/Upload/Images/Be%20tong%20chiu%20nhiet/Products%20datasheet.pdf
- [M24] Morgan Advanced Materials – Thermal Ceramics, Firelite 2600LI, Product Data Sheet, code
  CA.25, publication date 1 January 2025. PDF read.
  https://morganthermalceramics.com/media/d3plff0a/firelite-2600li_eng.pdf
- [M25] Thermal Ceramics Australia (Morgan), Product Information Sheet, Moral Coolcast 100 LW-K,
  revision 2. Forum copy, PDF read. https://community.fornobravo.com/filedata/fetch?id=273664
- [M26] I. Allegretta, G. Eramo, D. Pinto, A. Hein, "The effect of mineralogy, microstructure and
  firing temperature on the effective thermal conductivity of traditional hot processing ceramics",
  *Applied Clay Science* 135 (2017) 260–270, doi:10.1016/j.clay.2016.10.001. Accepted manuscript
  read (text; its tables are missing). Quotes Aliprandi, *I refrattari* (Faenza Editrice, 1987).
  https://ricerca.uniba.it/bitstream/11586/178579/7/Pinto_2017_11586_178579.pdf
- [M27] F. H. Norton, *Refractories*, McGraw-Hill, New York, 1942, Table 76 "Heavy Refractories",
  p.553. Read on the page image (archive.org leaf 549). Norton's authorities: F. H. Norton, "The
  Thermal Conductivity of Some Refractories", *J. Am. Ceram. Soc.* 10(1) (1927) 30–52; G. B. Wilkes,
  "The Thermal Conductivity of Refractories", *J. Am. Ceram. Soc.* 17(6) (1934) 173. Same fireclay
  rows in the 1st edition (1931), OCR text read.
  https://archive.org/details/in.ernet.dli.2015.205928 ;
  https://archive.org/details/in.ernet.dli.2015.462020
- [M28] A. B. Searle, *Refractories for Furnaces, Crucibles, etc.*, Sir Isaac Pitman and Sons,
  London, 1923, p.32 (Institution of Gas Engineers silica classes) and pp.39–40 (semi-silica
  bricks). OCR text of the scan read. https://archive.org/details/in.ernet.dli.2015.46590
- [M29] Digitalfire, "Lincoln 60 Fireclay" (material 971). Page read 2026-10-29.
  https://digitalfire.com/material/lincoln+60+fireclay ; https://digitalfire.com/material/971
- [M30] Mathios (mathios.com), product page "Firebrick Lava" 22 × 11 × 6 cm, product no. 100207
  (posted 7 February 2023). Page read. https://mathios.com/?p=12246
- [M31] S. Amicone et al., "An interdisciplinary approach to the study of kiln firing: a case study
  from the Campus Galli open-air museum (southern Germany)", *Archaeological and Anthropological
  Sciences* 15 (2023) 111, doi:10.1007/s12520-023-01798-1. Open-access PDF read (pp.3, 7–10, 15–16).
  https://iris.unipa.it/retrieve/43ac55fe-61f9-45c8-8aa9-ddb71df0c003/s12520-023-01798-1.pdf
- [M32] Hotchkiss kiln, later notices: fundraiser page "Mr. Hotchkiss studio rebuild", dated
  15 April 2023, kiln sentences read, https://gofundme.com/f/mr-hotchkiss-studio-rebuild ; listing
  "136th Noborigama Kiln Firing", Woolman, Nevada City, search extract only (404 when fetched),
  https://site.corsizio.com/c/6331f4b34ab8bc6e82bcfa64
- [M33] Knowledge Bank (New Zealand), "Anagama History". Search extract only (403 when fetched).
  https://knowledgebank.org.nz/text/anagama-history
- [M34] Morgan Advanced Materials – Thermal Ceramics, Abu Dhabi, Safety Data Sheet IC2, insulating
  castables (revised 26 February 2025; read in the PDF, 2026-10-29).
  https://www.morganthermalceramics.com/media/zlbgzz1z/ic2-ghs-uae.pdf
