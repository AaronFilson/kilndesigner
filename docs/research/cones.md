# Orton cone temperature equivalents: cones 15 to 42, and a re-check of 022 to 14

Research for extending `core/src/kilndesigner/data/cones.yaml` past cone 14. It also re-checks
the rows flagged in `electric-and-thermal.md` §8.

Status words:

- **Verified**: read first-hand from the source document. For PDFs, the text was extracted
  from the file and the numbers were read directly.
- **Excerpt**: read through a page summary or a search snippet, not from the full document.
- **Derived**: worked out here, for example °F → °C as (°F − 32) × 5/9.
- **Not found**: no source was found.

Values are in °C unless marked. "Independent" means the source does not copy another one.
Wikipedia, Ceramic Materials Workshop and Glazy all reproduce Orton's 2016 chart. JR Refractory
reproduces ASTM C24. They are listed, but they are not counted as independent.

**Main finding:** no web source gives three *independent* values for cones 15 to 42. Every
public table found goes back to one data set. That is the NBS/NIST calibration (Beerman 1956
for cones 12–37, and Fairchild & Peters 1926 for cones 38–42), as tabulated in ASTM C24 Table
X1.1. Orton's own PCE chart for 12–42 is "available by request" only [C5]. It was not obtained.
**Get it from Orton before shipping cones 15+.** Olsen's *The Kiln Book* (the user has a copy) is
also worth checking.

---

## 1. Which cones exist above 14

- Orton: "For high temperature applications, Orton makes self-supporting cones up to cone 28,
  Large and PCE cones up to cone 42." [C5] (Excerpt). **Self-supporting cones do go above 14.**
  But no published chart for self-supporting cones above 14 was found. Orton's public charts stop
  at 14 [C1].
- Orton's current PCE product list [C6] (Verified, from the product links): 12, 13, 14, 15, 16,
  17, 18, 19, 20, **21**, 23, 26, 27, 28, 29, 30, 31, 31½, 32, 32½, 33, 34, 35, 36, 37, 38, 39,
  40. Page 3 of the list shows no further products. Orton states the PCE range is "cone 12 to
  42", 1337 °C to 2015 °C [C6].
- **Cones 22, 24 and 25 do not exist.** They are absent from Orton's list [C6], ASTM C24 [C2],
  JR Refractory [C4] and Wikipedia [C3]. Confirmed.
- **Cone 21 does exist.** Orton sells #21 PCE [C6]. But ASTM C24 Table X1.1 gives **no
  temperature for 21** [C2]. No Orton temperature for cone 21 was found. The only value is
  Wikipedia's "Nimra Glass" 1570, which is another maker's cone, not Orton's [C3]. Not found.
- Cone 33½ exists only in the Börkey Keratech series [C3]. It is not an Orton cone.
- ASTM C24 X1.3: cones 28 and 30 "are manufactured but are not used in the PCE test" [C2].

## 2. Heating rates for the cone 15+ data

From ASTM C24-09 X1.2 [C2] (Verified):

| Cones | Heating rate |
|---|---|
| 12 to 37 | 150 °C/h (270 °F/h) |
| 38 | 100 °C/h (180 °F/h) |
| 39 to 42 | 600 °C/h (1080 °F/h) |

So there is **no 600 °C/h column alongside a 150 °C/h column**. Each cone has one rate, and
cones 38 to 42 are not at 150 °C/h. ASTM also says these temperatures "do not apply to the
conditions of commercial firing of kilns and use of refractory materials" [C2]. ASTM C24 Tables
1 and 2 (test schedules up to and above cone 26) both run at 150 °C/h (Note 6) [C2].

The values come from: cones 12–37 from NIST (Beerman, *J. Am. Ceram. Soc.* 39 (2) 1956,
pp. 47–53), and cones 38–42 from Fairchild & Peters, "Characteristics of Pyrometric Cones",
*J. Am. Ceram. Soc.* 9 (11), p. 700. ASTM C24-09 prints "November 1976" for that paper; the
paper is 1926 (vol. 9, pp. 701–743) [C2][C4]. Values were measured in °C, and the °F values
were calculated [C2]. JR Refractory says the cone 12–37 revision was adopted by ASTM in June 1955
[C4] (Excerpt).

**PCE cones and large cones are not the same series.** At cones 13 to 15 the ASTM PCE values
differ from Orton's large-cone values (see §4).

## 3. Cones 12 to 42: PCE end points

C2 = ASTM C24-09 Table X1.1 (Verified). C4 = JR Refractory, a copy of ASTM (Excerpt). C6 =
Orton PCE page, range end points only (Verified). C7 = the older Orton/NBS large-cone chart,
150 °C/h (Verified). Independent sources = C2, C6 and C7. C4 is a copy.

| Cone | Rate °C/h | C2 ASTM °C (°F) | C4 JR Refr. °C (°F) | C6 Orton | C7 Orton/NBS large | Agree? |
|---|---|---|---|---|---|---|
| 12 | 150 | 1337 (2439) | 1306 (2383) ⚠ | 1337 (2439 °F) | 1326 | C2 = C6. JR gives the SSB 60 value. C7 is a large cone. **2 independent** |
| 13 | 150 | 1349 (2460) | 1349 (2460) | – | 1346 | C7 is a large cone, 3 °C lower. **1 PCE source** |
| 14 | 150 | 1398 (2548) | 1398 (2548) | – | 1366 | PCE ≠ large (32 °C). **1 PCE source** |
| 15 | 150 | 1430 (2606) | 1430 (2606) | – | 1431 (2608 °F) | within 1 °C. **2 independent-ish** |
| 16 | 150 | 1491 (2716) | 1491 (2716) | – | – | **1 source** |
| 17 | 150 | 1512 (2754) | 1512 (2754) | – | – | **1 source** |
| 18 | 150 | 1522 (2772) | 1522 (2772) | – | – | **1 source** |
| 19 | 150 | 1541 (2806) | 1541 (2806) | – | – | **1 source** |
| 20 | 150 | 1564 (2847) | 1564 (2847) | – | – | **1 source** |
| 21 | – | not listed | not listed | sold, no temp. | – | **Not found** |
| 23 | 150 | 1605 (2921) | 1605 (2921) | – | – | **1 source** |
| 26 | 150 | 1621 (2950) | 1621 (2950) | – | – | **1 source** |
| 27 | 150 | 1640 (2984) | 1640 (2984) | – | – | **1 source** |
| 28 | 150 | 1646 (2995) | not listed | – | – | **1 source** |
| 29 | 150 | 1659 (3018) | 1659 (3018) | – | – | **1 source** |
| 30 | 150 | 1665 (3029) | not listed | – | – | **1 source** |
| 31 | 150 | 1683 (3061) | 1683 (3061) | – | – | **1 source** |
| 31½ | 150 | 1699 (3090) | 1699 (3090) | – | – | **1 source** |
| 32 | 150 | 1717 (3123) | 1717 (3123) | – | – | **1 source** |
| 32½ | 150 | 1724 (3135) | 1724 (3135) | – | – | **1 source** |
| 33 | 150 | 1743 (3169) | 1743 (3169) | – | – | **1 source** |
| 34 | 150 | 1763 (3205) | 1763 (3205) | – | – | **1 source** |
| 35 | 150 | 1785 (3245) | 1785 (3245) | – | – | **1 source** |
| 36 | 150 | 1804 (3279) | 1804 (3279) | – | – | **1 source** |
| 37 | 150 | 1820 (3308) | 1820 (3308) | – | – | **1 source** |
| 38 | **100** | 1835 (3335) | 1820 (3362) ⚠ | – | – | JR is self-inconsistent. 3362 °F = 1850 °C (Derived). **1 source** |
| 39 | **600** | 1865 (3389) | 1865 (3389) | – | – | **1 source** |
| 40 | **600** | 1885 (3425) | 1885 (3425) | – | – | **1 source** |
| 41 | **600** | 1970 (3578) | 1970 (3525) ⚠ | – | – | JR's °F is a typo (3525 °F = 1941 °C). **1 source** |
| 42 | **600** | 2015 (3659) | 2015 (3659) | 2015 (3659 °F) | – | C2 = C6. **2 independent** |

Wikipedia [C3] has **no Orton values above 14**. Its 15–42 rows are Börkey Keratech and Nimra
Glass cones only, which are different products. They are not usable as Orton equivalents. For
example, Börkey 31 is 1680/1700 and Nimra 15 is 1430.

**None of cones 13 to 41 has three independent sources.** Cones 12 and 42 have two (ASTM and
Orton's stated range). Cone 15 has two if the old large-cone chart counts. Under ADR 0009 and
CLAUDE.md, the engine should not ship cones 15+ as "checked" until Orton's own PCE and large-cone
chart (by request) or another primary source confirms them.

## 4. Re-check of the §8 flags (022 to 14)

Sources:

- **C1**, Orton's own °F chart "Temperature Equivalent Chart for Orton Pyrometric Cones (°F),
  Cone Numbers 022-14". Text extracted from the Trinity Ceramic copy of the Orton PDF, which
  carries Orton's footer. This is the same chart as [S78] (Verified).
- **C3**, Wikipedia, a copy of C1 (Verified).
- **C8**, Ceramic Materials Workshop, a copy of C1 (Excerpt). Cones 04, 05, 13 and 14 SSB match.
- **C7**, the older "Temperature Equivalents for Orton Standard Pyrometric Cones (As Determined
  at the National Bureau of Standards)", large cones at 60/150 and small cones at 300 °C/h. Two
  printings: W P Dawson © 2000 [C7a] and FireRight © 1994 [C7b] (both Verified, and identical to
  each other). This is an **earlier edition**, so it is not a check on the 2016 numbers. Most of
  its large-cone values differ from C1 by 2–10 °C.

### Cone 14 LRB (flagged ⚠)

- C1 has the large cones 13 and 14 starred: "These Large Cones have different compositions and
  different temperature equivalents."
- Orton's own values: large 13 = 2410 °F at 108 °F/h and 2455 °F at 270 °F/h. Large 14 =
  **2530 °F at 108 and 2491 °F at 270** (Verified).
- Derived: 13 = 1321/1346 °C and 14 = **1388/1366 °C**.
- **So the reversal is in Orton's own chart, not a Wikipedia transcription error.**
- C7 gives large 14 = 1366 °C at 150 only, which agrees with C1's 150 value. The 60 value is
  blank in C7.
- The ASTM PCE cone 14 = 1398 °C [C2] is a different series.
- **Verdict:** LRB 14 @150 = 1366 is confirmed by C1 and C7 (2 independent). LRB 14 @60 = 1388
  appears only in C1 and its copies. It is physically implausible, because it is above the 150
  value. **Leave LRB 14 @60 out, or ask Orton.** Don't swap the values: swapping would put 1366 at
  60 °C/h, which no source supports.

### Cones 05 and 04 LRB 150 (flagged)

- C1: LRB 270 °F/h for 05 = 1915 °F (1046 °C) and for 04 = 1958 °F (1070 °C) (Verified, Derived °C).
- **These are Orton's printed values.** The §8 numbers are transcribed correctly.
- C7 (older edition): 05 = 1046 (agrees), 04 = 1060 (differs by 10 °C).
- C1's iron-free large cone (IFB) 150 values are 1044 and 1067 [C3]. They follow the usual
  pattern, which suggests the LRB 04 1070 may be a chart error. Unresolved.
- **Verdict:** 05 LRB 150 = 1046 is confirmed by C1 and C7. 04 LRB 150 has C1 = 1070 and C7 =
  1060, so it is **disputed**. Ask Orton.

### 022 to 14 SSB 60 and 150

- Every SSB 60 and SSB 150 value in §8, from 022 to 14, was checked against C1's °F columns,
  converted to °C. **All 72 match to ±0.5 °C** (Derived). Examples: 022 1087 °F → 586,
  05½ 1859 → 1015, 6 2232 → 1222, 12 2383 → 1306, 14 2489/2523 → 1365/1384.
- The LRB 60 and 150 columns, 019 to 12, also all match C1.
- **But C1, C3, C8 and Glazy are all the same Orton 2016 data.** C7 is a different edition, and
  for large cones only. No independent third measurement of the self-supporting values was found.
  Orton is the only primary source for self-supporting cones. By the "three independent"
  standard, the SSB rows are **one source** (Orton), faithfully copied.

## Discrepancies

- Olsen, *The Kiln Book* 4th ed., Table A-11 (p.307–308) prints Orton equivalents with cone 7
  (1251 °C) above cone 8 (1236 °C) and column headings that don't match Orton's. It is not used
  as a source.

1. LRB 14: Orton's chart prints 1388 @60 and 1366 @150, which is reversed. The 150 value is
   confirmed by the older NBS chart.
2. LRB 04 @150: 1070 (2016 chart) vs 1060 (older NBS chart).
3. PCE vs large cones: cone 13 is 1349 vs 1346, 14 is 1398 vs 1366, and 15 is 1430 vs 1431.
   These are different cone series. Don't mix them in one column.
4. Cone 38: ASTM 1835 °C / 3335 °F. JR Refractory has 1820 °C / 3362 °F (= 1850 °C). The likely
   cause is transcription errors at JR. ASTM is preferred.
5. Cone 41: JR's °F (3525) does not match its own °C (1970). ASTM's 3578 °F does.
6. JR's cone 12 (1306) is the self-supporting 60 °C/h value, not PCE (1337).
7. ASTM C24-09 footnote 6 gives the Fairchild & Peters date as 1976. It is 1926.

## Not found

- Orton's PCE / large-cone chart for 12–42. It exists "by request" [C5].
- Any self-supporting cone 15–28 temperatures.
- Any Orton temperature for cone 21.
- An independent (non-ASTM-lineage) table for cones 16–41.
- Large-cone (LRB) values above 15, and whether they equal the PCE values.
- Beerman 1956 and Fairchild & Peters 1926 first-hand (paywalled). Harbison-Walker handbook,
  Hamer & Hamer, Olsen: not checked online. Olsen is in the user's hands.

## Sources

- [C1] Orton, "Temperature Equivalent Chart for Orton Pyrometric Cones (°F), Cone Numbers
  022-14" (copy hosted by Trinity Ceramic). https://trinityceramic.com/wp-content/uploads/2018/05/cone-chart.pdf
  Orton's original: https://www.ortonceramic.com/files/2676/File/Orton-Cone-Chart-F-022-14.pdf
- [C2] ASTM C24-09, Standard Test Method for Pyrometric Cone Equivalent (PCE) of Fireclay and
  High Alumina Refractory Materials, Table X1.1 and X1.2–X1.5. https://dl.azmanco.com/standards/ASTM-C/ASTM-C-Series-Full/C/C24.pdf
- [C3] Wikipedia, Pyrometric cone (wikitext). https://en.wikipedia.org/w/index.php?title=Pyrometric_cone&action=raw
- [C4] JR Refractory, Furnace Temperature (reproduces the ASTM PCE table). https://jrrefractory.com/furnace-temperature/
- [C5] Orton, Pyrometric Cones Resources. https://www.ortonceramic.com/pyrometric-cones-resources
- [C6] Orton, PCE cones product pages. https://www.ortonceramic.com/pce and https://www.ortonceramic.com/pce?page=2
- [C7a] W P Dawson / Orton, "Temperature Equivalents for Orton Standard Pyrometric Cones (As
  Determined at the National Bureau of Standards)", © 2000. https://hotkilns.com/sites/default/files/pdf/dawson-cones.pdf
- [C7b] The same chart, FireRight Controls / Warner Instruments, © 1994. https://www.fireright.com/docs/general/pcomecharts.pdf
- [C8] Ceramic Materials Workshop, Pyrometric Cone Chart (cites Orton 2016). https://my.ceramicmaterialsworkshop.com/anatomy/glaze-anatomy/reference/cones
- Cited by C2, not read: H. P. Beerman, "Calibration of Pyrometric Cones", J. Am. Ceram. Soc.
  39 (2) 1956, 47–53, https://doi.org/10.1111/j.1151-2916.1956.tb15622.x. C. O. Fairchild and
  M. F. Peters, "Characteristics of Pyrometric Cones", J. Am. Ceram. Soc. 9 (11) 1926, 701–743,
  https://doi.org/10.1111/j.1151-2916.1926.tb17132.x
