# HarbisonWalker, *Handbook of Refractory Practice* (2005): the drawn parts of Section 3 and the Appendix

[HW05] Harbison-Walker Refractories Company, *Handbook of Refractory Practice*, © 2005, 331 PDF pages.
The owner's copy is `docs/research/da86e4bd09a66be00c11a67957ff8e5a.pdf` (git-ignored, copyrighted;
no page image or crop is committed). This is the second reading of `hwi-handbook.md` (the first
pass), for what a text layer drops: the graphs, drawings, photographs and the Appendix's formulas.

Read on 2026-11-17 (second pass): Section 3 (PR-1 to PR-27, PDF 33–59) and the Appendix (A-1 to
A-12, PDF 207–218). Every figure was rendered (110–400 dpi) and looked at. The graphs on PDF 39
(Figs 3.3, 3.4), 40 (Figs 3.5, 3.6), 42 (Fig 3.7), 47 (Fig 1), 50 (Fig 2) and 51 (Fig 3) are vector
paths, so their curves were read from the path coordinates with PyMuPDF (`get_drawings()`), not by
eye. The axes were calibrated on the printed ticks, and which curve is which was confirmed on a
render from the label arrows. The text layer was used for the prose. Cited by the printed page
label (PR-7, A-3) with the PDF page once per item.

Marks as in `hwi-handbook.md`: **Verified** (read on the page image; "graph, vector path" with a ±
where a curve was digitised), **Read** (text layer only, unambiguous), **Derived** (arithmetic
here, shown), **Not found**.

Where the page number differs from the first pass: Figs 3.5 and 3.6 are on **PR-8** (PDF 40). Their
text is on PR-7 (PDF 39), which is where `hwi-handbook.md` §1 row 9 cites them.

---

## 1. How the graphs were read

| Figure | Page | Axis calibration | Residual | What limits the reading |
|---|---|---|---|---|
| 3.3, 3.4 | PR-7, PDF 39 | x: the 13 printed vertical gridlines at 200 °F steps (0 and 2800 °F at the frame). y: the 10 tick marks of the right-hand % scale (0.2 steps), fitted by least squares | y fit 0.008 %; curves start 0.011 % under the fitted zero, so 0.011 % is added to every reading | gridlines are spaced in 0.65 pt steps (±8 °F); line width 0.65 pt (±0.01 %). Net **±0.02 %**, up to ±0.05 % on the steep first 800 °F of the silica curves |
| 3.5 | PR-8, PDF 40 | x: ticks every 400 °F, 0.08 pt/°F. y: 25 ticks, 0.1 % apart | 0.002 % | ±0.02 % and ±10 °F; the curves have no arrowheads |
| 3.6 | PR-8, PDF 40 | as 3.5; 17 ticks | 0.001 % | ±0.02 % and ±10 °F |
| 3.7 | PR-10, PDF 42 | x: 0 and 100 h at the frame (2.70 pt/h). y: frame 5 to −10 % | 0.5 pt | ±0.05 % and ±0.5 h |
| 1 | PR-15, PDF 47 | x: gridlines every 10 % Al₂O₃. y: the right-hand °C labels (23.5 pt per 100 °C, regular to 0.5 pt) | the liquidus starts at 1723.1 °C and ends at 2055.6 °C against the printed 1723 and 2050 | **±8 °C (±15 °F)** |
| 3 | PR-19, PDF 51 | gridlines every 1 % impurity and 25 °F | | ±5 °F, ±0.2 % |

Fig 1's left-hand °F gridlines do not agree with its °C labels: they drift up to 2.7 pt (about 20 °F)
at the top. The °C labels fit the curve's printed end points, so they were used (Verified).
Every Fig 1 reading differs by 7–15 °F from the number HWI prints for the same feature (§6.2); the
printed numbers are the ones to use.

---

## 2. Figs 3.1 and 3.2 (PR-4, PDF 36)

Two half-tone photographs, each with a caption. No scale, no dimension and no leader is printed on
them. Verified.

| Fig | Caption | Shows |
|---|---|---|
| 3.1 | "Cold Crushing Strength Test" | A specimen standing between the platens of a hydraulic press, a control cabinet behind |
| 3.2 | "Modulus of Rupture Test" | A test frame with a dial gauge. A brick, broken, lies on its two supports |

The only dimensions are in the text beside them (Read, and in `hwi-handbook.md` §2.1): the 9 in
straight on two bearing cylinders and the (9 in × 4½ in) faces horizontal; MOR = 3PL/2bd².

---

## 3. Figs 3.3 and 3.4: reversible thermal expansion of brick (PR-7, PDF 39)

Titles: "FIGURE 3.3 Approximate Reversible Thermal Expansion of Brick" and the same for 3.4. Axes: x,
temperature 0–2800 °F (°C scale 0–1500 on top); y, linear expansion, % (right) and in/ft (left,
0–¼), 0–2.0 % shown. Mean values of the brands in each class (PR-7, Read). Digitised every 200 °F.
All values % linear, Verified, graph, vector path, **±0.02 %** (see §1).

### 3.1 Fig 3.3

| Curve (as labelled) | 200 | 400 | 600 | 800 | 1000 | 1200 | 1400 | 1600 | 1800 | 2000 | 2200 | 2400 | 2600 | Ends at °F: % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Conventional silica | 0.15 | 0.58 | 0.99 | 1.12 | 1.17 | 1.20 | 1.21 | 1.21 | 1.21 | 1.21 | 1.21 | 1.21 | 1.21 | 2686: 1.21 |
| Magnesite (92 % MgO) | 0.08 | 0.21 | 0.36 | 0.51 | 0.67 | 0.84 | 1.01 | 1.20 | 1.37 | 1.54 | 1.71 | 1.88 | 2.05 | 2692: 2.12 |
| Forsterite | 0.07 | 0.17 | 0.28 | 0.40 | 0.52 | 0.65 | 0.78 | 0.92 | 1.06 | 1.19 | 1.32 | 1.45 | 1.58 | 2686: 1.64 |
| 99 % alumina | 0.05 | 0.13 | 0.22 | 0.31 | 0.41 | 0.50 | 0.61 | 0.72 | 0.86 | 0.99 | 1.11 | 1.22 | 1.33 | 2674: 1.37 |
| 80 % to 90 % alumina | 0.05 | 0.12 | 0.20 | 0.29 | 0.37 | 0.46 | 0.55 | 0.64 | 0.74 | 0.84 | 0.93 | 1.03 | 1.12 | 2693: 1.17 |
| 60 % to 70 % alumina | 0.04 | 0.10 | 0.17 | 0.24 | 0.32 | 0.40 | 0.47 | 0.55 | 0.64 | 0.72 | 0.80 | 0.88 | 0.97 | 2686: 1.02 |
| Silicon carbide | 0.03 | 0.10 | 0.17 | 0.23 | 0.30 | 0.36 | 0.42 | 0.49 | 0.55 | 0.61 | 0.67 | 0.73 | 0.79 | 2668: 0.81 |

Every curve starts near 40–180 °F and stops at 2670–2700 °F, short of the frame's 2800 °F (the end
x is ±8 °F). In in/ft multiply by 0.12.

### 3.2 Fig 3.4

| Curve (as labelled) | 200 | 400 | 600 | 800 | 1000 | 1200 | 1400 | 1600 | 1800 | 2000 | 2200 | 2400 | 2600 | Ends at °F: % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Superduty silica | 0.17 | 0.77 | 1.07 | 1.20 | 1.27 | 1.31 | 1.34 | 1.35 | 1.36 | 1.35 | 1.34 | 1.33 | 1.32 | 2697: 1.33 |
| Superduty silica (not patch) | 0.14 | 0.53 | 0.89 | 1.03 | 1.12 | 1.16 | 1.19 | 1.21 | 1.23 | 1.24 | 1.26 | 1.27 | 1.28 | 2697: 1.28 |
| Semi-silica fireclay | 0.09 | 0.23 | 0.34 | 0.40 | 0.48 | 0.60 | 0.66 | 0.69 | 0.72 | 0.74 | 0.77 | 0.80 | – | **2477: 0.82** |
| Chrome | 0.04 | 0.12 | 0.22 | 0.32 | 0.43 | 0.53 | 0.63 | 0.74 | 0.85 | 0.96 | 1.08 | 1.20 | 1.32 | 2691: 1.39 |
| **High-duty and superduty fireclay** | 0.05 | 0.13 | 0.20 | 0.27 | 0.33 | 0.40 | 0.46 | 0.52 | 0.59 | 0.65 | 0.71 | – | – | **2382: 0.77** |
| Zircon | 0.02 | 0.07 | 0.13 | 0.18 | 0.24 | 0.29 | 0.34 | 0.40 | 0.45 | 0.51 | 0.56 | 0.62 | – | 2577: 0.68 |

The fireclay line is the one the arrowed label "HIGH-DUTY AND SUPERDUTY FIRECLAY" points at (its
leader ends on the curve at about 2380 °F). The line labelled "ZIRCON" is the lowest straight one.
The superduty silica curve has the label above it and the "(not patch)" curve is the lower of the
two silica curves (Verified on the 400 dpi render).

### 3.3 The fireclay curves at cone 10, and the mean coefficient (Derived)

Cone 10 is 2345 °F (1285 °C at 60 °C/h, `cones.yaml`; cone 9 is 1260 °C = 2300 °F and cone 11 is
1294 °C = 2361 °F, same source). The mean coefficient is ε(2345 °F) − ε(70 °F), over the 2275 °F
between them.

| Curve | ε at 2345 °F, % | in/ft | Mean α, 70–2345 °F | In SI | Against 3/32 in/ft (0.781 %) |
|---|---|---|---|---|---|
| High-duty and superduty fireclay | 0.76 | 0.091 | 3.33 × 10⁻⁶ /°F | 6.0 × 10⁻⁶ /K | −3 % |
| Semi-silica fireclay | 0.79 | 0.095 | 3.46 × 10⁻⁶ /°F | 6.2 × 10⁻⁶ /K | +2 % |

The fireclay figure of 6.0 × 10⁻⁶ /K is the same number Brosnan [M1] gives (3/32 in/ft, "6.0exp(-6)/°C",
`refractory-movement-and-mortar.md` §1.1.1). The curve is a little convex (it runs above the straight
line from 70 °F to its end: 0.27 % at 800 °F against 0.24 % for a straight line, Derived). So the
curve, not the mean, is the better scale for a cooler firing:

| Fireclay, from Fig 3.4 | 1000 °F | 1400 | 1800 | 2000 | 2200 | 2345 (cone 10) |
|---|---|---|---|---|---|---|
| % | 0.33 | 0.46 | 0.59 | 0.65 | 0.71 | 0.76 |
| in/ft (× 0.12) | 0.040 | 0.055 | 0.070 | 0.078 | 0.085 | 0.091 |

At 1832 °F (1000 °C) it reads 0.60 % (1800: 0.59; 2000: 0.65, interpolated), the "0.6 % linear at
1000 °C" of `thermal-properties.md` §2 (the Mathios fireclay excerpt, T14), which this corroborates.

### 3.4 Against the other sources

- **The engine's 3/32 in/ft** (`movement.py` `GROWTH_IN_PER_FT`, `frame.py` `GROWTH_IN_PER_FT`;
  stated "to 2400 °F"): the HWI fireclay line reaches 0.77 % at 2382 °F and about 0.78 % at 2400 °F
  (extrapolating its last 0.0003 %/°F, Derived). So 3/32 in/ft is the line's end value to within
  0.01 %, and 3 % above it at cone 10. **The first pass read "about 0.7 % at 2400 °F" (±0.03).
  That was 0.06–0.07 % low and the line ends at 2380 °F, not 2400.**
- **`movement.py` says "No source read gives the curve below 2400 °F".** Fig 3.4 gives it for
  fireclay (above), so the growth could be scaled to a cooler firing. At cone 6 (1222 °C = 2232 °F)
  the curve reads 0.72 %, 8 % under 3/32.
- **UR-4's class table** (first pass §3.1: 60–85 % alumina 3/32, 90 % 1/8, silica 5/32, SiC and
  zircon 3/32, magnesite ¼) against these curves at the curves' ends (about 2690 °F): silica 1.33 %
  (5/32 = 1.30 %), SiC 0.81 % (3/32 = 0.78 %), magnesite 2.12 % (¼ in/ft = 2.08 %), 99 % alumina
  1.37 % (corundum 5/32 = 1.30 %), all consistent. Two are not: **60–70 % alumina 1.02 % against
  UR-4's 3/32 (0.78 %), +30 %; 80–90 % alumina 1.17 %** against 3/32 for the 85 % class, +50 %
  (and 1/8 for 90 %, which fits). At cone 10 the 60–70 % curve is 0.86 % (+10 % over 3/32) and the
  80–90 % curve 1.00 %. Zircon is 0.68 % against 3/32. So UR-4's "3/32 for the 60, 70 and 85 %
  classes" is low against HWI's own Fig 3.3 (Derived; both are "approximate").
- **Kiln relevance:** a 60 % alumina hot face (a rebuilt hot face, a car top) grows about 0.86 % at
  cone 10, 10 % more than the 3/32 the engine uses for all brick. The engine has no growth for any
  other class (`movement.py` is fireclay only).

First-pass spot readings, checked: semi-silica "about 0.6 % by 1200 °F, 0.8 % at 2500 °F": 0.60 and
0.82 (at its end, 2477 °F), agrees. Zircon "0.65 % at 2600 °F": 0.68 at 2577, agrees. Chrome "1.4 %
at 2700 °F": 1.39 at 2691, agrees. Silica "most of its 1.3 % below about 800 °F": 1.20 of 1.33 by
800 °F, agrees.

---

## 4. Figs 3.5 and 3.6: first heat of castables and plastics (PR-8, PDF 40)

Titles: "FIGURE 3.5 Thermal Expansion of Various Refractory Castables", "FIGURE 3.6 Thermal Expansion
of Various Refractory Plastics". Axes: temperature °F, 0–3200; linear expansion in % (left, −1.40
to 1.00 in 3.5; −0.60 to 1.00 in 3.6) and in/ft on the right. Every curve is a **loop**: a heating
leg and a cooling leg, drawn as one line. The caption and the text (PR-7) say "initial heat-up", so
these are first heats. Neither figure says how the bond was fired, the heating rate or the hold at
the top. Text (PR-7, Read): the castables are "cement-bonded"; the plastics are "phosphate-bonded
and clay-bonded" with no curve named as one or the other.

### 4.1 Fig 3.5, castables

The three curves are told apart by the leader arrows (Verified): FIRECLAY CASTABLE is the solid
line, LOW CEMENT FIRECLAY CASTABLE the dash-dot line (the arrow ends on its cooling leg near
1700 °F), 90% ALUMINA CASTABLE the dashed line. Fig 3.5 has no direction arrows; the heating leg is
the one that starts at 0 and the cooling leg ends at the lowest value, as the text's "permanent
shrinkages" say. % linear, Verified, graph, vector path, ±0.02 % and ±10 °F.

| T, °F | Fireclay castable, heat | cool | Low-cement fireclay, heat | cool | 90 % alumina, heat | cool |
|---|---|---|---|---|---|---|
| 200 | 0.03 | – | 0.00 | −0.59 | 0.03 | −1.07 |
| 400 | 0.10 | −0.40 (end, 411 °F) | 0.05 | −0.53 | 0.08 | −1.01 |
| 600 | 0.13 | −0.37 | 0.10 | −0.49 | 0.08 | −0.93 |
| 800 | 0.17 | −0.31 | 0.12 | −0.45 | 0.15 | −0.86 |
| 1000 | 0.25 | −0.25 | 0.18 | −0.42 | 0.25 | −0.77 |
| 1200 | 0.41 | −0.19 | 0.23 | −0.38 | 0.33 | −0.67 |
| 1400 | 0.46 | −0.12 | 0.28 | −0.34 | 0.43 | −0.58 |
| 1600 | 0.48 | −0.06 | 0.28 | −0.29 | 0.52 | −0.48 |
| 1800 | 0.46 | 0.02 | 0.21 | −0.24 | 0.61 | −0.37 |
| 2000 | 0.50 | 0.08 | 0.22 | −0.19 | 0.81 | −0.27 |
| 2200 | 0.47 | 0.10 | 0.29 | −0.10 | 0.98 | −0.15 |
| 2400 | 0.28 | 0.17 | 0.20 | 0.03 | 0.83 | −0.03 |
| 2600 | – | – | – | – | 0.36 | 0.15 |

The fireclay castable's cooling leg ends at 411 °F, so it has no 200 °F value: that cell is "–"
(**not drawn**), not a reading.

| Curve | Heat to | Peak on heating | Local minimum on heating | Value at 2345 °F (heating) | Turning point | End of cooling (permanent change) |
|---|---|---|---|---|---|---|
| Fireclay castable | 2451 °F | 0.50 % at 1985 °F | none (the curve never falls below its start; a shoulder at 400–1000 °F) | 0.34 % | 2451 °F, 0.21 % | **−0.40 % at 411 °F** |
| Low-cement fireclay castable | 2545 °F | 0.29 % at 1530 °F, and 0.29 % again at 2170 °F | 0.20 % at about 1900 °F | 0.22 % | 2545 °F, 0.19 % | **−0.60 % at 122 °F** |
| 90 % alumina castable | 2621 °F | 0.97 % at 2190 °F | none | 0.90 % | 2621 °F, 0.22 % | **−1.10 % at 81 °F** |

- All three are heat-and-cool loops. The 90 % alumina castable is not reversible at all above
  2200 °F: it expands 0.97 % by 2190 °F, then **shrinks 0.75 % between 2190 and 2620 °F while still
  heating** (sintering), and returns 1.1 % short of its start. The fireclay castable also turns
  over (0.50 % at 1985 °F down to 0.21 % at 2451 °F while heating).
- **No visible dip at 400–600 °F.** The text (PR-7) says "shrinkage over the temperature range
  400 °F to 600 °F … associated with thermal decomposition of the cement". The curves show a
  slower rise there, not a fall: the fireclay castable gains 0.03 % from 400 to 600 °F, against
  0.07 % from 200 to 400 °F and 0.04–0.08 % per 200 °F from 600 to 1000 °F.
- **The permanent changes are 0.40, 0.60 and 1.10 %** (measured at 81–411 °F, not at room
  temperature), inside the text's "commonly … 0.2 % to 1.5 %" (PR-7, Read).
- **Kiln relevance** (cast door frames, floors, car tops and arches on their first firing,
  `castable.py`): a fireclay castable fired to cone 10 (2345 °F) grows about 0.5 % (0.06 in/ft) by
  1600–2000 °F, then gives some back, and ends 0.40 % short of its cast length on cooling
  (0.048 in/ft). A 90 % alumina castable ends 1.1 % short (0.13 in/ft), so its joints and its edge
  against brick open by that much (Derived, ×0.12). This is the maker's figure for one unnamed
  mix of each class, not a product's. `castable.py` takes a measured shrinkage from the mix; none
  of the engine's library castables has a reversible curve (`hwi-handbook.md` §6).

### 4.2 Fig 3.6, plastics

Labels and arrows (Verified): SUPERDUTY FIRECLAY PLASTIC is the solid line (its arrow ends on the
curve at about 2500 °F), 90% ALUMINA PLASTIC the dashed line (arrow at about 1100 °F), 70% MULLITE
PLASTIC the dash-dot line (arrow on its cooling leg at about 1600 °F). Fig 3.6 has small direction
arrowheads on the solid curve (the upper leg heats; it starts at 0.00 %, the lower leg ends at
−0.15 %). % linear, Verified, graph, vector path, ±0.02 %, ±10 °F.

| T, °F | Superduty fireclay, heat | cool | 90 % alumina, heat | cool | 70 % mullite, heat | cool |
|---|---|---|---|---|---|---|
| 200 | 0.02 | −0.10 | 0.03 | −0.30 | 0.02 | −0.20 |
| 400 | 0.12 | 0.02 | 0.08 | −0.18 | 0.07 | −0.15 |
| 600 | 0.21 | 0.07 | 0.15 | −0.08 | 0.12 | −0.10 |
| 800 | 0.27 | 0.12 | 0.24 | 0.00 | 0.19 | −0.04 |
| 1000 | 0.33 | 0.19 | 0.37 | 0.11 | 0.24 | 0.03 |
| 1200 | 0.38 | 0.25 | 0.52 | 0.22 | 0.29 | 0.09 |
| 1400 | 0.43 | 0.32 | 0.63 | 0.31 | 0.36 | 0.16 |
| 1600 | 0.48 | 0.38 | 0.73 | 0.41 | 0.42 | 0.24 |
| 1800 | 0.49 | 0.45 | 0.86 | 0.50 | 0.50 | 0.32 |
| 2000 | 0.49 | 0.53 | 0.93 | 0.60 | 0.56 | 0.40 |
| 2200 | 0.54 | 0.60 | 0.91 | 0.71 | 0.59 | 0.48 |
| 2400 | 0.61 | 0.67 | 0.88 | 0.84 | 0.60 | 0.56 |

| Curve | Top | Peak | End of cooling (permanent change) |
|---|---|---|---|
| Superduty fireclay plastic | 2473 °F, 0.68 % | 0.68 % at 2458 °F | **−0.15 % at 121 °F** |
| 90 % alumina plastic | 2417 °F, 0.86 % | 0.93 % at 2010 °F | **−0.33 % at 83 °F** |
| 70 % mullite plastic | 2483 °F, 0.60 % | 0.60 % at 2483 °F | **−0.21 % at 140 °F** |

- All three are heat-and-cool loops, with no minimum on heating. The text (PR-7) says plastics
  "show linear behavior below about 1900 °F" then "the materials contract". The figure shows that
  only for the 90 % alumina plastic (it turns over at about 2010 °F). The fireclay plastic goes
  flat at 1800–2000 °F and then rises again, and the mullite plastic never turns.
- **The permanent changes (0.15–0.33 %) are lower than the text's "0.2 % to 0.6 %"** (PR-7): the
  top of that range is not in the figure. Superduty fireclay's 0.15 % is under the text's floor.
  A text and figure disagreement in HWI itself (Derived).
- Relevance: a ram-mix or plastic skin wall (Olsen p.42), first firing. Reversible growth to
  about 2400 °F is 0.6–0.9 %, so a plastic grows about as a brick does (0.76 % for fireclay),
  then comes back 0.15–0.33 % short.

---

## 5. Fig 3.7: creep (PR-10, PDF 42)

Caption (Read): "Creep measurement of various high-alumina refractories under 25 psi load at
2600 °F for 0-100 hrs. Note the excellent creep resistance of 60% alumina low alkali brick."
Axes: time 0–100 h; linear subsidence %, +5 to −10. Four curves, told apart by their leader arrows
(Verified). Linear subsidence %, Verified, graph, vector path, ±0.05 % and ±0.5 h.

| Brick | 0 h | 5 | 10 | 20 | 30 | 40 | 50 | 75 | 100 h |
|---|---|---|---|---|---|---|---|---|---|
| 60 % alumina, low alkali | −0.17 | −0.32 | −0.46 | −0.71 | −0.87 | −1.00 | −1.17 | −1.57 | −1.84 |
| 70 % alumina | −0.30 | −0.52 | −0.74 | −1.16 | −1.50 | −1.83 | −2.00 | −2.52 | −2.82 |
| 85 % alumina | −0.41 | −0.95 | −1.36 | −2.04 | −2.65 | −3.20 | −3.73 | −4.84 | −5.63 |
| 50 % alumina | −0.57 | −1.90 | −3.15 | −4.83 | −5.71 | −6.31 | −6.75 | −7.48 | −8.00 |

The curves are drawn starting at −0.2 to −0.6 % at 0 h (the heat-up is not shown).

**Creep as C832 defines it (PR-8), the subsidence between the 20th and 50th hour** (Derived from
the table), and the rate after it:

| Brick | 20–50 h, % | rate, %/h | 50–100 h, %/h |
|---|---|---|---|
| 60 % alumina, low alkali | −0.46 | −0.015 | −0.013 |
| 70 % alumina | −0.84 | −0.028 | −0.017 |
| 85 % alumina | −1.69 | −0.056 | −0.038 |
| 50 % alumina | −1.91 | −0.064 | −0.025 |

The rates are still falling at 100 h for all four (primary creep; the 60 % low-alkali brick runs
−0.015, −0.013 and −0.011 %/h over 20–50, 50–100 and 75–100 h). The order is not the order of alumina:
the 85 % brick creeps almost as fast as the 50 %. Against Table 3.4 (first pass §2.2: 60 % alumina,
0.1–0.5 % after C16 at 2640 °F, 25 psi): a different test, 1½ h not 100 h. **No fireclay creep curve
is in the book**, and none for any brick below 2600 °F or below 25 psi. Not for a 10 psi IFB wall.

---

## 6. Phase diagrams (PR-13 to PR-27, PDF 45–59)

### 6.1 What is there

The text (PR-13, PR-14) covers minerals and glasses, the ceramic bond, and equilibrium diagrams
(Bowen and Greig 1924; Aramaki and Roy's revision; the ACerS "Phase Diagrams for Ceramists"). The
book prints **five figures**, and the six Roman-numbered tables. Chrome refractories (PR-24 to
PR-26) have no diagram, only text and Table VI.

| Fig | Title | System | Page | Content |
|---|---|---|---|---|
| 1 | Equilibrium Diagram of the System Alumina-Silica (Al₂O₃·SiO₂) | Al₂O₃–SiO₂ | PR-15, PDF 47 | §6.2 |
| 2 | Partial Equilibrium Diagram of the Binary Systems Lime-Silica and Ferrous Oxide-Silica | CaO–SiO₂, FeO–SiO₂ (silica-rich end) | PR-18, PDF 50 | §6.4 |
| 3 | Effect of Certain Impurities Upon Melting Behavior of Silica | SiO₂ with TiO₂, Al₂O₃, Na₂O, K₂O (0–14 %) | PR-19, PDF 51 | §6.3 |
| 4 | Composition Triangles in the Lime-Magnesia-Silica (CaO·MgO·SiO₂) System | CaO–MgO–SiO₂ | PR-20, PDF 52 | §6.5 |
| 5 | Equilibrium Diagram of the system FeO·MgO | FeO–MgO | PR-22, PDF 54 | §6.5 |

Tables: I, mineral composition of silica brick (PR-19); II, typical dead-burned magnesite (PR-21);
III, minerals coexisting with periclase in CaO–MgO–SiO₂ (PR-21); IV, melting points of compounds in
magnesite refractories (PR-22); V, CaO–MgO–SiO₂ eutectics (PR-23); VI, chrome ores (PR-24). No
caption or sidebar in PR-13 to PR-27 other than these.

### 6.2 Fig 1, alumina-silica (PR-15, PDF 47)

Axes: Al₂O₃ weight % along the bottom (SiO₂ along the top, 100 → 0), temperature °F on the left
(2400–3800) and °C on the right (to 2050). The note at its top: "Melting Point of Silica
(Cristobalite) 1723 °C, 3133 °F; Melting Point of Alumina (Corundum) 2050 °C, 3722 °F". It is
Aramaki and Roy's diagram (PR-14: "The new diagram is in close agreement with the older one up to 55
percent alumina"). Caveats printed on PR-15: it applies only to pure materials and complete
equilibrium; it says nothing on reaction rate or the viscosity of the liquid; with a reducing
atmosphere or about 3270 °F (1800 °C) or above, silica can volatilize, so "caution must be
exercised" above about 55 % alumina. Read.

**Features, printed value and the reading from the drawn lines** (graph, vector path, ±8 °C / ±15 °F;
the printed numbers are Read and cited from PR-14, PR-15, PR-16):

| Feature | Printed | Read from the lines |
|---|---|---|
| Silica–mullite eutectic | 5.5 % Al₂O₃ (94.5 % SiO₂), 2903 °F (1595 °C) | 5.9 % Al₂O₃, 1590 °C (2895 °F) |
| Tridymite ⇄ cristobalite line | 2678 °F (1470 °C), across 0–72.6 % Al₂O₃ | 1474 °C (2685 °F) |
| Mullite, stoichiometric | 3Al₂O₃·2SiO₂ = 71.8 % Al₂O₃, 28.2 % SiO₂ | the left vertical line is at **72.8 %**, not 71.8 |
| Mullite solid solution | up to 74.2 % at equilibrium; to 78 % "easily prepared", metastable above 74.2 % | a band from 72.8 % to 74.5 %, closed above at about 1827 °C (3320 °F). The right line is dashed below about 1770 °C |
| Mullite melting | congruent, 3362 °F (1850 °C), at about 73.0 % Al₂O₃; mullite at 3345 °F (1840 °C) about 72.1 % | the liquidus peaks at 1843 °C (3349 °F) at 69–70 % |
| Mullite–corundum eutectic | 3344 °F (1840 °C), 77.4 % Al₂O₃ | the horizontal at 1831 °C (3329 °F) from 74.1 % to 99.8 %; the liquidus's low point, at 77 %, reads 1836 °C (3337 °F) |
| Corundum liquidus | to 2050 °C (3722 °F) at 100 % | 2055 °C (3732 °F) at 100 % |
| Complete melting, 40 % Al₂O₃ | 3265 °F (1796 °C) (worked example, PR-16) | 1788 °C (3251 °F), 8 °C low |
| Liquid at the eutectic, 40 % | 48.0 % liquid, 52.0 % mullite (PR-16) | – |

Mullite "does not melt incongruently as formerly believed" (PR-14), and silica does not dissolve in
mullite (PR-16). Temperature of complete melting is "almost constant from 60 to about 77 percent
alumina" (PR-15): the lines read 1837–1843 °C (3338–3349 °F) from 60 to 77 %.

**The liquidus read from the drawn line** (Verified, graph, vector path, ±8 °C), with the first liquid
at the eutectic, 1595 °C (2903 °F), for every composition between 5.5 and 71.8 % (PR-15, Read):

| Al₂O₃ % | 10 | 18 | 20 | 22 | 25 | 30 | 40 | 42 | 44 | 50 | 55 | 60 | 65 | 70 | 71.8 | 75 | 77 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Liquidus, °C | 1626 | 1683 | 1695 | 1707 | 1723 | 1748 | 1788 | 1795 | 1801 | 1818 | 1829 | 1837 | 1842 | 1843 | 1842 | 1839 | 1836 |
| Liquidus, °F | 2959 | 3062 | 3083 | 3105 | 3134 | 3178 | 3251 | 3263 | 3275 | 3305 | 3324 | 3338 | 3347 | 3349 | 3348 | 3343 | 3337 |

(80 % 1888 °C = 3430 °F; 90 % 1994 °C = 3621 °F; 100 % 2055 °C.)

**The three classes the engine meets** (Derived from the table; liquid fraction by the lever rule on
the eutectic, as PR-16 does for 40 %: liquid = (71.8 − x)/(71.8 − 5.5)):

| Class | Al₂O₃ | Liquidus | First liquid | Liquid at 1595 °C, pure | Solid at cone 10, pure |
|---|---|---|---|---|---|
| Superduty fireclay | 40–44 % (HWI's brick 42.2 %, Table 3.1a: 41.9 %) | 1788–1801 °C (3251–3275 °F); PR-16's 3265 °F at 40 % | 1595 °C | 45 % at 42 % | mullite 58.5 % + silica phase 41.5 % |
| Semi-silica and low-duty | 18–25 % (CR-11; low-duty 30 %, Table 3.1a) | 1683–1723 °C (3062–3134 °F) | 1595 °C | 71–81 % | mullite 25–35 % + silica phase |
| 60 % class high-alumina | 50–70 % (HWI's 58.0 %, Table 3.1a) | 1818–1843 °C (3305–3349 °F) | 1595 °C | 18 % at 60 %; 0 above 71.8 % | mullite 84 % + silica phase 16 % at 60 % |

**Phases and distance from the solidus at cones 9–11.** Cone temperatures (`cones.yaml`, 60 °C/h;
150 °C/h in brackets): cone 9 1260 °C = 2300 °F (1280 °C = 2336 °F), cone 10 1285 °C = 2345 °F
(1305 °C = 2381 °F), cone 11 1294 °C = 2361 °F (1315 °C = 2399 °F).

| | Cone 9 | Cone 10 | Cone 11 |
|---|---|---|---|
| Below the pure system's first liquid, 1595 °C (2903 °F): 60 °C/h | 335 °C (603 °F) | 310 °C (558 °F) | 301 °C (542 °F) |
| Same at 150 °C/h | 315 °C | 290 °C | 280 °C |
| Below the 42 % liquidus (1795 °C) at 60 °C/h | 535 °C | 510 °C | 501 °C |
| Below the 60 % liquidus (1837 °C) | 577 °C | 552 °C | 543 °C |

In all three, a fireclay brick (42 %) and a 60 % brick sit **below the tridymite–cristobalite line
(1470 °C, 2678 °F)**, so Fig 1 says: **tridymite + mullite, and no liquid.** HWI does not leave it at
that: tridymite "appears always to require the presence of a liquid" and cristobalite forms without
one (PR-18), so a fired fireclay brick holds **mullite, cristobalite (some quartz, rarely
tridymite) and glass** (PR-17), and a high-alumina brick adds corundum (and, with bauxite, may keep
corundum below 71.8 % and free silica above it, PR-18). The real first liquid is far under 1595 °C:
"a very small amount of potash is sufficient to lower the temperature of initial liquid formation
to **1805 °F (985 °C)**" (PR-17, Read; the repeated statement in the first pass §2.8). At cone 10
that is 300 °C (540 °F) **above** the first liquid, so a commercial brick at cone 10 is partly
liquid, "so viscous that it behaves essentially as if it were a solid" (PR-17). The book gives no
glass fraction for fireclay or high-alumina brick, and no figure that locates the 985 °C eutectic
(Not shown). Quartz starts turning to cristobalite at 2280 °F (1250 °C), and a large quartz grain
may keep a core at 2700 °F (PR-17, PR-18; first pass §2.8).

Cross-check with the cone equivalents (Derived; `cones.yaml` 150 °C/h column, Table 3.3 first
pass §2.7): superduty fireclay PCE 33–34 is 1743–1763 °C, 30–50 °C under the pure liquidus at
42 % (1795 °C). The 60 % class, PCE 36–37 (1804–1820 °C), is 15–35 °C under the liquidus at
58–60 % (1834–1837 °C). The commercial brick softens a little below the pure system's liquidus,
which is the right direction for impurities.

### 6.3 Fig 3, silica with Na₂O, K₂O, Al₂O₃, TiO₂ (PR-19, PDF 51)

The one diagram in the book that bears on wood-ash, salt and soda kilns. Axes: percent of impurity
0–14 (bottom), percent of silica 100–86 (top), melting temperature 2750–3200 °F. Four curves
(Verified; the Na₂O and K₂O arrows end on their curves; the K₂O curve is the dashed one). The two
alkali curves run off the bottom of the frame to their eutectics, printed in two boxes under the
graph: **"EUTECTIC MIXTURE 31 % K₂O 69 % SiO₂ MELTING POINT 1358 °F"** and **"26 % Na₂O 74 % SiO₂
MELTING POINT 1460 °F"** (Verified). Temperature of complete melting, °F (graph, vector path, ±5 °F):

| Impurity, % | 0 | 1 | 2 | 3 | 4 | 5 | 5.5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| K₂O (dashed) | 3133 | 3081 | 3033 | 2988 | 2947 | 2909 | 2890 | 2870 | 2828 | 2783 | – | – |
| Na₂O | 3133 | 3058 | 3004 | 2959 | 2923 | 2895 | 2884 | 2876 | 2859 | 2836 | 2806 | 2767 |
| Al₂O₃ | 3133 | 3105 | 3075 | 3039 | 2995 | 2942 | 2907 | 2925 | 2964 | – | – | – |
| TiO₂ | 3133 | 3120 | 3107 | 3092 | 3075 | 3054 | 3043 | 3030 | 2999 | 2959 | 2904 | 2814 |

(The K₂O curve leaves the frame at 8.7 %, 2750 °F; the Na₂O at 10.4 %.) The eutectics in the frame:
Al₂O₃ at 5.4 % (2905 °F, printed "2903"); TiO₂ at 10.0 % (2811 °F, printed "2822"). Silica-rich
side only. Per 1 % of impurity near pure silica the melting point drops by about 52 °F for K₂O, 75 °F
for Na₂O, 28 °F for Al₂O₃ and 13 °F for TiO₂ (Derived, first percent). PR-19, Read: "the temperature
of complete melting drops rapidly with even small additions" of any of the four, and at 2920 °F "a
mixture of 5.5 percent alumina, soda, or potash with silica will be completely melted" (the lines
agree: 2907, 2884, 2890 °F). Fig 3 is binary, silica with one oxide; it is **not** the potash–
alumina–silica system that sets the 985 °C first liquid of a fireclay brick (PR-17), and no
ternary diagram is printed.

What it means for a kiln (Derived, one reading): in a wood, salt or soda kiln the alkali that reaches
a brick face dissolves silica, and from the lines a few per cent of K₂O or Na₂O in silica lowers its
melting point by 100–300 °F; the eutectics are far below cone 10 (K₂O 1358 °F = 737 °C, Na₂O
1460 °F = 793 °C). HWI says nothing about ash or soda kilns; it says only that "the alkalies soda and
potash are especially potent" in fluxing fireclay (PR-17) and that INSWOOL is not resistant to
"strong alkalies" (first pass §5.4). The silica brick data (Table I, below) are for silica brick.

**Table I** (PR-19, Verified, 170 dpi): mineral composition of silica brick, per cent.

| Type | Tridymite | Cristobalite | Quartz | Pseudowollastonite | Apparently noncrystalline |
|---|---|---|---|---|---|
| Superduty | 33–61 | 27–49 | <1.3+ | <2.5+ | 9–17 |
| Superduty, spall resistant | 35–38 | 33–35 | 2.3+ | 1.3+ | 20–30 |
| Conventional | 40–54 | 28–41 | <1 | <1.5+ | 5–24 |

"By difference; believed to consist of 'disordered' silica and 5 to 15 percent glass". The same page:
a silica brick's groundmass (about 25 % of its weight) holds almost all the lime and iron oxide
(8–10 % lime in the groundmass), and in CaO–Al₂O₃–FeO–SiO₂ "liquid can form at a temperature as low
as about 2048 °F (1120 °C)"; alkalies lower it more (PR-19, PR-20, Read). Silica brick are fired at
about 2625 °F (1440 °C), with a permanent linear growth of about 4.2 % (PR-20, Read).

### 6.4 Fig 2, lime-silica and ferrous oxide-silica (PR-18, PDF 50)

Silica-rich end only, 100 → 60 % SiO₂, 2600–3200 °F. Graph, vector path, ±8 °F, ±0.5 %.

- **CaO–SiO₂:** an "immiscibility plateau". Complete melting falls from 3133 to **3106 °F (1708 °C)**
  with the first 1 % lime, then stays at 3106 °F (the drawn line is at 3107) out to the second
  liquid at 27.5 % lime (the line reaches 73.3 % SiO₂; PR-19 says 27.5 % lime = 72.5 % SiO₂). A
  silica–lime mixture of 2.5 % lime is only 9 % liquid just under 3106 °F (PR-19, Derived there as
  2.5/27.5). The liquid boundary falls from 73.3 % SiO₂ at 3108 °F to **65.2 % SiO₂ at 2677 °F**, and
  the eutectic V reaches its bottom at about **62.7 % SiO₂, 2602 °F**; then up on the far side (55.2 %
  SiO₂, 2757 °F).
- **FeO–SiO₂:** a plateau at **3090 °F (1699 °C)** for 1–40 % FeO (the drawn line runs from 99.7 down
  to 60.3 % SiO₂ at 3090 °F), liquid "A" and "B", with a dashed liquid boundary near 60 % SiO₂.
- A horizontal at **2678 °F (2677 read)** across 100 → 65 % SiO₂ (cristobalite to tridymite).
- PR-19 (Read): "a small percentage of alumina or alkalies destroy the immiscibility", and at 2920 °F
  5.5 % lime in silica is 82 % solid and 18 % liquid, where 5.5 % alumina, soda or potash is wholly
  molten.
- Relevance: FeO is what a reducing atmosphere makes of iron oxide (PR-23: "If the furnace
  atmosphere is strongly reducing, iron oxide will be in the form of FeO"), and lime is what
  wood ash brings. The plateaus say lime or FeO in **silica** do not lower the final melting
  point much (3106, 3090 °F); the figure says nothing on how they act in **fireclay**, where HWI
  says (PR-17) their oxides "dissolve wholly or in part" in the alkali-alumina-silica liquid.

### 6.5 Basic systems, invariant points only (PR-20 to PR-27)

- **Fig 4** (PR-20): composition triangles in CaO–MgO–SiO₂ (the periclase-rich part drawn full-line),
  with the lime:silica ratio lines 2.8:1, 1.865:1, 1.4:1 and 0.93:1 by weight, and the point A
  monticellite, CaO·MgO·SiO₂ = 35.9 % CaO, 25.6 % MgO, 38.5 % SiO₂ (PR-21, Read). Table III: below
  0.93 → forsterite + monticellite; 0.93–1.40 → monticellite + merwinite; 1.40–1.86 → merwinite +
  dicalcium silicate; at 1.86 or above, no magnesium silicate (Read).
- **Table V** eutectics (PR-23, Read): MgO + CaO ~4172 °F (~2300 °C); MgO + CaO + 3CaO·SiO₂
  ~3360 °F; MgO + 3CaO·SiO₂ + 2CaO·SiO₂ ~3255 °F; MgO + 2CaO·SiO₂ ~3270 °F; **MgO + 2CaO·SiO₂ +
  3CaO·MgO·2SiO₂ 2867 °F (1575 °C)**; **MgO + 3CaO·MgO·2SiO₂ + CaO·MgO·SiO₂ 2714 °F (1490 °C)**;
  MgO + CaO·MgO·SiO₂ + 2MgO·SiO₂ 2736 °F (1502 °C); MgO + 2MgO·SiO₂ ~3380 °F. PR-22: with lime:silica
  under 1.86, liquid starts at 2867 °F, perhaps as low as 2714 °F; at 1.86 or over, none below 3254 °F.
- **Fig 5** (PR-22): FeO–MgO, a continuous solid solution (magnesiowüstite) with no invariant point.
  Both lines start near 2500 °F at the FeO end and reach **5070 °F** at MgO. By eye at 130 dpi
  (±100 °F), the liquidus is about 4300 °F and the solidus about 3300 °F at 50 % MgO. "Even with more
  than 50 percent FeO, the refractoriness is still high" (PR-23).
- **Table IV** (PR-22, Read): CaO ~4660 °F; MgO ~5070; spinel ~3875; 2CaO·SiO₂ ~3865; forsterite
  ~3450 °F; magnesioferrite begins to melt at 3115 °F; monticellite melts incongruently at 2709 °F
  (complete about 3000 °F); merwinite at 2871 °F; dicalcium ferrite at 2617 °F. 3CaO·SiO₂ "stable only
  from 3452 °F (1900 °C) to 2880 °F (1250 °C)": the text layer's "2880 °F" is a misprint for 2280 °F
  (1250 °C), as the next sentence and PR-23 say.
- Chrome ore (PR-25, Read): the silicate impurities start to melt at 2300 °F (1260 °C) and the spinels
  are not wholly molten until "possibly as high as 3900 °F". Dicalcium silicate dusts at about 1340 °F
  (725 °C) with a 10 % volume increase unless stabilised (PR-23). Fayalite/forsterite: forsterite
  3450 °F; serpentine goes to forsterite + 39.5 % liquid at 2838 °F, talc to 95.6 % liquid at 2811 °F
  (PR-27).
- Not in the book: any diagram with Cr₂O₃, ZrO₂ or SiC.

### 6.6 Table 3.1, the chemistry (PR-3, PDF 35; not in the first pass)

Verified, 170 dpi. Per cent.

| Brick | Al₂O₃ | SiO₂ | Alkalies (Na₂O, K₂O, Li₂O) | Others (TiO₂, Fe₂O₃, CaO, MgO) |
|---|---|---|---|---|
| Fireclay, superduty | 41.9 | 53.2 | 1.2 | 3.7 |
| High-duty | 41.0 | 51.6 | 2.0 | 5.3 |
| Low-duty | 30.0 | 62.0 | 3.7 | 4.3 |
| High-alumina, 60 % class | 58.0 | 38.0 | 0.1 | 3.9 |
| 70 % class | 69.2 | 26.2 | 0.2 | 4.4 |
| 85 % class | 86.5 | 8.9 | 0.1 | 4.5 |
| 90 % class | 88.5 | 11.0 | 0.2 | 0.3 |
| Corundum class | 99.2 | 0.4 | 0.2 | 0.2 |
| Silica, conventional | 0.5 | 95.9 | 0.1 | 3.4 |
| Silica, superduty | 0.2 | 96.5 | 0.04 | 3.4 |

Zircon 32.3 SiO₂, 66.0 ZrO₂, 1.7 others; silicon carbide 5.6 SiO₂, 90.8 SiC, 3.6 others; fired
magnesite 98.2 MgO, 0.2 Al₂O₃, 1.6 others (the rest of 3.1b: first pass §2.1 misprint note). The
alkali and "others" columns are what separate a commercial fireclay brick from Fig 1: 3.2–7.3 %
of fluxes in the three fireclay classes. (Sums are 99.9–100.1 for every row, Derived.)

---

## 7. The Appendix, Area and Volume (A-1 to A-6, PDF 207–212)

Read on the page images (the text layer drops the fractions and the roots). Symbols are the
figure's own. Each formula was derived independently (Derived). Page titles misprint "SECTOF A
CIRCLE" (A-2) and "SEGTOR OR A SPHERE" (A-3), for sector. Engine functions are named where one
exists: `geometry.py:122` (`segment_area` of the circular arch), `shape.py:126` (`segment_area`,
which reads `r²θ − (S/2)(r − rise)`), `conical.py:160` (`segment_radius`), `round_masonry.py:359`
(`cap_volume`), `massing.py:407` (`_parabola`); others were searched for and not found.

| Fig | Formula as printed, with its symbols | Check | Engine function it could test |
|---|---|---|---|
| A-1 rectangle, parallelogram | Area = ab (a the long side, b the height) | right | none (not needed) |
| A-1 triangle | Area = ½cd (c the base, d the height); Area = √[s(s−a)(s−b)(s−c)], s = ½(a+b+c) | right (Heron) | none |
| A-1 trapezium | Area = ½[**s**(e+d) + bd + ce], with b, a, c the three horizontal pieces of the base and d, e the two heights | **misprint**: the figure has no s; the middle piece is a. The area is ½[bd + a(d+e) + ce] (triangle ½bd, trapezoid ½a(d+e), triangle ½ce) | none |
| A-1 regular polygon | Area = ½nsr, n sides, s a side, r the apothem. Table: 2.5981s² = 3.4641r² (printed n = 6); 4.8284s² = 3.3137r² (printed 6); 6.1818s² = 3.2757r² (printed 6); 7.6942s² = 3.2492r² (10); 11.1962s² = 3.2154r² (12) | the numbers are right for **n = 6, 8, 9, 10, 12**: (n/4)cot(180°/n) and n·tan(180°/n). **The second and third rows print "6" for n = 8 and n = 9.** | `polygon_corners`, `polygon_reach` (imported by `drawings.py`): none checks an area; a polygonal kiln's floor area could use 2.5981s² (hex) and 4.8284s² (octagon) |
| A-2 circle | Area = 0.7854D² = πR²; C = chord = 2√[h(D−h)] = 2R sin ½θ; h = R − √[R² − (C÷2)²] = R − ½√[(2R+C)(2R−C)]; L = (θ/360)·2πR = 0.017453Rθ; ½θ = 28.648L÷R; sin ½θ = C÷2R; R = [(C÷2)² + h²]÷2h; circumference = πD = 2πR = 2√(π × Area); D = 2√(Area÷π) | all right (28.648 = 180/π ÷ 2; 0.017453 = π/180) | **`conical.segment_radius(span, rise)`**: R = (span²/4 + rise²)/(2·rise), swept angle 2·asin(span/2R) |
| A-2 segment of a circle | tan ¼θ = 2h÷C; Area = ½[LR − C(R−h)] = πR²·θ/360 − C(R−h)/2 | right: with half-angle a, ½[2aR² − 2R sin a·R cos a] = R²(a − sin a cos a) | **`geometry.py:122` `segment_area`** = r²a − r²sin a cos a; **`shape.py:126`** r²θ − (S/2)(r − rise); both equal this |
| A-2 sector | Area = ½LR = πR²·θ/360 = 0.0087266R²θ | right (π/360 = 0.0087266) | the sector helper in `v2/statics/arch.py:305` (`sector`; not read for its area) |
| A-3 trapezoidal rule | Area ≈ h(½y₀ + y₁ + y₂ + y₃ + ½y₄), h the equal spacing | right (four strips) | none; the engine's dome volume is a midpoint sum (`geometry.py:325`) |
| A-3 segment of a sphere | Spherical surface = 2πrh = 0.7854(c² + 4h²); total surface = 0.7854(c² + 8rh); V = ⅓πh²(3r − h) = 1.0472h²(3r − h); V = (1/24)πh(3c² + 4h²) = 0.1309h(3c² + 4h²) (c the chord, h the height, r the sphere's radius) | right (2πrh + πc²/4 = 0.7854(c² + 8rh); with a = c/2 the cap is πh(3a² + h²)/6) | **`round_masonry.cap_volume(rho, below)`**, h = rho − below: π h²(3ρ − h)/3 |
| A-3 sector of a sphere | Total surface = 1.5708r(4h + c); V = ⅔πr²h = 2.0944r²h | right (cap 2πrh + cone πrc/2 = (π/2)r(4h + c)) | none found (a dome sector) |
| A-3 cylinder | Cylindrical surface = πdh = 2πrh = 6.2832rh; total = 2πr(r + h) = 6.2832r(r + h); V = πr²h = ¼πd²h = 0.7854d²h. **The first line** "Volume = πh²(3r − h) = 1.0472h²(3r − h)" | the three are right. **The first line is a stray copy of the sphere segment's volume with the ⅓ dropped** (π ≠ 1.0472); it is not a cylinder formula | none (a cylinder is trivial) |
| A-4 spandrel | Area = 0.2146R² = 0.1073C² (R the arc's radius, C the chord of the arc) | right (R² − πR²/4; C² = 2R²) | none |
| A-4 circular ring | Area = 0.7854(D² − d²) = 0.7854(D+d)(D−d) | right | a round wall's plan area: not found as a single function |
| A-4 ellipse | Area = πab = 3.1416ab (a, b the semi-axes as drawn) | right | none |
| A-4 parabolic segment | Area = ⅔sh (s the base, h the height) | right | **`massing.py:407` `_parabola`** (a parabolic arch), if it computes an area; no area function found |
| A-4 sphere | Surface = 4πr² = 12.566r² = πd²; V = ⁴⁄₃πr³ = 4.1888r³ = ⅙πd³ = 0.5236d³ | right | `cap_volume` at h = 2ρ |
| A-4 torus | Surface = 4π²Rr = 39.478Rr; V = 2π²Rr² = 19.739Rr² (R the radius of the ring's centre line, r the section's radius, D = 2R, d = 2r) | right | none |
| A-5 pyramid | Lateral area = ½Ps (P the base perimeter, s the slant height); V = ⅓Ah | right (regular pyramid) | none |
| A-5 frustum of a pyramid | Lateral = ½s(P + p); V = ⅓h(a + A + √aA); V = ⅙h(a + A + 4m) (a, A, m the areas of top, base and midsection) | right; the last is the prismoidal formula | none |
| A-5 cone | Conical area = πrs = πr√(r² + h²); V = ⅓πr²h = 1.0472r²h = 0.2618d²h | right (π/12 = 0.2618) | none |
| A-6 frustum of a cone | Conical surface = ½πs(D + d); V = ⅓πh(r² + rR + R²); **V = h(a + √aA + A)**; V = ⅙h(a + 4m + A) | the 1st, 2nd and 4th are right. **The third is missing its ⅓** (it prints no fraction in the image or the text layer; A-5's pyramid version has it) | none found (the conical roof or a stack-cone volume would use it; `conical.py` lays brick courses, not a volume) |

No catenary, no ellipse segment, no parabolic-arch rise, no dome zone and no polygonal-ring formula
is on A-1 to A-6: the catenary arch, the domes' zones and the segment's intersections are not here.

---

## 8. The Appendix, reference tables (A-7 to A-12, PDF 213–218)

Not transcribed. Checked against the engine's needs and by arithmetic (Derived); misprints recorded as
printed.

### 8.1 A-7, decimal fractions of an inch for each 1/64 (PDF 213)

All 64 cells were checked by division. **One misprint: 7/64 is printed ".109325"; it is .109375.**
(Confirmed in the text layer.) The rest are right.

### 8.2 A-8, atomic weights of selected elements (PDF 214)

"International Atomic Weights (1970)". The values a kiln's combustion and oxide arithmetic uses:
H 1.0079, C 12.011, N 14.0067, O 15.9994, Na 22.9898, Mg 24.305, Al 26.9815, Si 28.08, S 32.06,
K 39.098, Ca 40.08, Fe 55.84. They agree with the present standard weights to the printed precision
(from memory of the standard values; nothing in the repo needs this table).

### 8.3 A-9, melting points (PDF 215)

"* In converting temperatures from Centigrade to Fahrenheit, temperatures above 3,300 °F are given
to the nearest five degrees." Verified. The rows a kiln touches (°F / °C):

| Material | °F | °C | Note as printed |
|---|---|---|---|
| Aluminum | 1220 | 660 | |
| Copper | 1981 | 1083 | "(reducing atmosphere)" |
| Cast iron, white | ~2100 | ~1150 | |
| Cast iron, gray | ~2245 | ~1230 | |
| Steel, plain carbon (1 % carbon and less) | ~2680 | ~1470 | |
| Iron, pure | 2795 | 1535 | |
| Nickel | 2647 | 1453 | |
| Chromium | ~3445 | ~1895 | |
| Zinc | 787.1 | 419.5 | |
| Tin | 449.4 | 231.9 | |
| Lead | 621.1 | 327.3 | |
| Magnesium | 1202 | 650 | |
| Silver | 1761.4 | 960.8 | |

**Not found: brass, bronze, nickel-chrome (Nichrome), stainless steel, Kanthal.** The "Metals and
Alloys" table has no alloy but cast iron and steel; no melting range, no strength.

Oxides (second table, same page): chromic oxide ~4080 °F (~2250 °C); corundum ~3720 (~2050); cristobalite
3133 (1723); lime ~4660 (~2570); magnetite 2901 (1594); periclase ~5070 (~2800); rutile 3326 (1830);
zirconia unstabilized 4890 (2700), 5 % calcia 4710 (2599), 7 % calcia 4532 (2500).

°F against °C checks (Derived, 1.8 and 32): every metal row above agrees to the printed digits. **The Kelvin columns
do not all equal °C + 273.15**: copper 1366.6 (should be 1356.2), nickel 1744 (1726.3), chromium 2130
(2168.2), columbium 2743 (2688.2); and in the oxide table chromic oxide 2603 (2523), lime ~3200
(~2843), zirconia 3123 (2973). The Kelvin column is not for use.

### 8.4 A-10 and A-11, conversions (PDF 216, 217)

Every factor on both pages was checked against the exact definitions. All are right except one:
**A-11 "tons (short) → tons (metric)" prints 0.9078; it is 0.9072.** The conversions the engine
needs:

| Engine need | What A-10/A-11 print | Check (Derived) |
|---|---|---|
| Btu → J | Not printed. Btu → foot-pounds 7.7816 × 10²; Btu → gram-calories 2.52 × 10² | 252.0 cal × 4.1868 J = 1055.1 J against 1055.06 J (0.01 %); 778.16 ft·lbf × 1.35582 = 1055.0 J. The calorie-to-joule step is not in the book |
| Btu/(ft²·h) → W/m² | Not printed | 3.1546, from Btu/h → gram-cal/s 7.0 × 10⁻² (0.29308 W) ÷ 0.092903 m². HWI's own Example 1 pairs 1099 Btu/(ft²·h) with 3465 W/m² (first pass §3.2): ratio 3.153 (0.05 % off) |
| Btu·in/(ft²·h·°F) → W/(m·K) | Not printed | 0.14423, from 7.0 × 10⁻² cal/s × 4.1868 × 0.0254 m × 1.8 ÷ 0.092903 m² (A-10: ft² → cm² 9.29 × 10²; in → cm 2.540). Checks to 0.02 % |
| lb/ft³ → kg/m³ | "pounds/ft³ → kgs/meter³ 16.02" | 16.0185, right |
| psi → Pa | "pounds/in² → kgs/cm² 7.03 × 10⁻²" | 0.070307 × 98066.5 = 6894.8 Pa, right; the kgf-to-N step is not in the book |
| °F → °C | "°Fahrenheit .556(F−32) → Centigrade" and "(°C × 1.8) + 32" | .556 is 5/9 rounded up 0.07 %: at 2345 °F it gives 1286.0 °C, 1.0 °C over 1285.0. Use 5/9 |

### 8.5 A-12, temperature scale conversions (PDF 218)

All 105 rows (0 to 580 and 600 to 3600) were checked by script in both directions (Derived). Two
misprints: **1550 °C is printed as 2922 °F (it is 2822 °F)**, and 1000 °F is printed as 537.9 °C
(537.8). Cone 10, 1285 °C = 2345 °F, falls between the table's rows for 2300 °F (1260 °C) and
2350 °F (1288 °C).

---

## 9. Every sidebar, caption and boxed note, PR-1 to PR-27 and A-1 to A-12

None of PR-1 to PR-27 has a sidebar or boxed note beyond the tables and figures listed. A page by
page scan of the drawn boxes found: PR-1 and PR-2, none; PR-3, Table 3.1 (§6.6); PR-4, Figs 3.1 and 3.2
(§2); PR-5, Table 3.2; PR-6, Table 3.3; PR-7, Figs 3.3 and 3.4; PR-8, Figs 3.5 and 3.6; PR-9, Table
3.4; PR-10, Fig 3.7 and Table 3.5; PR-11, PR-12, none; PR-13 to PR-27, the five figures and the six
tables above. The first pass has Tables 3.2 to 3.5. Table 3.5's heading prints "Btu · in/ft³ · hr · °F"
(the first pass has it). The Appendix pages are one framed box each; their titles are the page
headings.

---

## 10. What the engine can use

| Need | Finding | Status | Where it would go |
|---|---|---|---|
| Fireclay growth below 2400 °F | The curve to 2380 °F: 0.33 % at 1000 °F, 0.59 % at 1800, 0.71 % at 2200, 0.76 % at cone 10 (2345 °F) | Verified, graph, vector path, ±0.02 % | `movement.py`, `frame.py`: scale 3/32 in/ft for a cooler firing (cone 6: 0.72 %, 0.086 in/ft); replaces "no source gives the curve below 2400 °F" |
| The 3/32 in/ft check | 0.77 % at 2382 °F, 3 % under 3/32 at cone 10; mean α 6.0 × 10⁻⁶ /K, Brosnan's number | Verified, Derived | a fifth number for the same allowance; the first pass's 0.7 % should read 0.76 |
| Growth for a 60–90 % alumina hot face | 0.86 % (60–70 %) and 1.00 % (80–90 %) at cone 10; UR-4 says 3/32 for 60–85 % | Verified | nothing built; a class table would take these |
| Castable first heat | Permanent −0.40 % (fireclay), −0.60 % (low-cement), −1.10 % (90 % alumina) after 2450–2620 °F; growth to +0.5 % at 2000 °F, then a give-back | Verified, graph, vector path | `castable.py`: a context band for a mix with no measured shrinkage |
| A plastic's first heat | +0.6–0.9 % hot; −0.15 to −0.33 % after | Verified | `castables.md`; a ram-mix skin |
| Creep of high-alumina brick | 60 % low-alkali: 0.46 % in hours 20–50 at 2600 °F, 25 psi; 85 %: 1.69 % | Verified | Reference only; no hot-load rule in the engine |
| Fireclay and high-alumina at cone 9–11 | Pure system: no liquid, 301–335 °C under the first liquid (1595 °C); real first liquid 985 °C with potash | Verified, Derived | a "how far under the solidus" note, if ever shown; the engine holds no phase data |
| Alkali effect on silica | Na₂O and K₂O curves and eutectics (1460 and 1358 °F); about 2900 °F at 5.5 % | Verified, graph, vector path | Reference for the salt/soda/wood-ash cautions; the book gives no brick-life figure |
| The arch segment | A-2's formula equals `geometry.segment_area` and `shape.segment_area`, and `conical.segment_radius` | Derived | tests: independent hand values (A-2, A-3) |
| The dome cap | A-3's ⅓πh²(3r − h) equals `round_masonry.cap_volume` | Derived | a test |
| Conversions | 5/9, not .556; 16.02, 0.0703 kgf/cm² per psi; 252 cal per Btu | Derived | no change; the engine uses Pint |
| Melting points a kiln touches | Table in §8.3 | Verified | reference (cast iron 2245 °F, steel 2680 °F) |

## 11. Conflicts

- **With the first pass (`hwi-handbook.md`):**
  - §2.4 and §1 row 10: "about 0.7 % at 2400 °F, where the line ends (±0.03)". The line ends at
    **2382 °F at 0.77 %** (0.76 at cone 10), so it was read 0.06–0.07 % low.
  - §1 row 9 cites Fig 3.5 as PR-7; it is on PR-8 (its text is on PR-7). Same for Fig 3.6.
  - §2.4 says the plastics are "linear to about 1900 °F, then contract" and "permanent shrinkages
    0.2–0.6 %": that is the text's claim. The figure shows 0.15–0.33 % and only one plastic
    contracting (§4.2).
  - The first pass did not digitise Figs 3.5 to 3.7; they are here (§4, §5). It does not have Table 3.1 (§6.6).
  - §3.1's UR-4 table is consistent with Fig 3.3 for silica, SiC, magnesite and corundum, not for
    the 60–85 % alumina classes (§3.4).
- **With `materials.yaml`:** none; the library has no expansion field.
- **With `refractory-movement-and-mortar.md`:** §1.1 "Not found: a published expansion curve to
  1300 °C for high-alumina, silica or IFB beyond the single coefficients" is closed for high-alumina,
  silica, SiC, zircon, chrome and fireclay (still **not found for IFB** and for castables'
  reversible curve beyond Fig 3.5's three). `movement.py`'s "No source read gives the curve below
  2400 °F" is no longer true.
- **With `thermal-properties.md` §2:** the Mathios fireclay "0.6 % at 1000 °C" is corroborated
  (0.60 % at 1832 °F). The IFB "0.5–0.7 % at 1000 °C" is unchanged, and PR-7 says only that "most
  insulating firebrick have relatively low rates".
- **Inside HWI:** UR-4's 3/32 for the 60–85 % classes against Fig 3.3 (60–70 %: +10 % at cone 10,
  +30 % at 2690 °F; 80–90 %: +28 %, +50 %). Fig 1's drawn lines sit 7–15 °F from their printed
  labels (§6.2), and its mullite line is drawn at 72.8 % though labelled 71.8 %. PR-7's "0.2–0.6 %" plastics
  against Fig 3.6 (§4.2). Table IV's "2880 °F (1250 °C)" for 2280 °F. Appendix misprints (§7, §8).
- **With `castable.py`:** its 573 °C comment ("0.45 % linear", Wikipedia) is the first pass's point,
  not changed here. Nothing in the engine models a castable's first-heat loop.

## 12. Not shown, not readable, skipped

- **Figs 3.1 and 3.2:** no scale or dimension on either photograph.
- **Fig 3.5:** no direction arrows; heating and cooling legs are assigned by the order of the path and
  by the text's permanent shrinkage. The fireclay castable's cooling leg stops at 411 °F, so it has
  no 200 °F value. The bond and mix, the heating rate and the hold are not printed.
- **Fig 3.6:** direction arrowheads were checked on the solid curve; the legs of the other two are
  assigned by the same logic (the leg that ends lower is the cooling leg). Which curves are phosphate-bonded and which clay-bonded is not stated.
- **Fig 3.7:** curves start at −0.2 to −0.6 % at 0 h; the time to reach 2600 °F is not shown.
- **Fig 1:** read to ±8 °C; the left °F gridlines were not used (§1). The `K₂O–Al₂O₃–SiO₂` eutectic
  at 985 °C is text only. No diagram for Cr₂O₃, ZrO₂ or SiC.
- **Fig 2, Fig 3:** only the silica-rich ends are drawn; Fig 3's K₂O and Na₂O curves leave the frame.
- **Fig 4:** not digitised (composition triangles; only the printed ratios and Table III are recorded).
  **Fig 5:** by eye, ±100 °F.
- No glass fraction, no viscosity, and no brick-life figure for any alkali, lime or iron attack.
- Not covered: PR-1 to PR-12 prose beyond the figures; A-8 beyond the elements named; A-7 beyond the
  one misprint (all cells were checked).
- **Re-check on the images, in order:** Fig 3.4 fireclay at 2345 °F (PDF 39, clip 0.10–0.65 × 0.37–0.62
  of the page; the line through the arrowhead near x 312 pt, y 409 pt); Fig 3.5 permanent changes
  (PDF 40, clip 0.05–0.60 × 0.09–0.41); Fig 1 liquidus at 42 % (PDF 47, clip 0.35–0.82 × 0.08–0.23);
  Fig 3.7 at 20 and 50 h (PDF 42, clip 0.05–0.60 × 0.07–0.25).

## 13. Proposals for the owner (nothing here is built)

1. **Scale the growth** in `movement.py` and `frame.py` from Fig 3.4 for a firing under cone 10,
   and drop the "no source gives the curve" sentence. Keep 3/32 in/ft at 2400 °F.
2. **Castable first heat:** show the maker's 0.4–1.1 % permanent change as context where a cast part
   has no measured shrinkage. Add the same for a 60 % alumina hot face's growth if one is ever used.
3. **Tests:** the arch segment, the dome cap and `segment_radius` against A-2 and A-3 (with the
   misprints in §7 recorded, so nobody copies the cylinder line or A-6's third volume).
4. **Conversions:** use 5/9 for °F to °C. Note A-12's 1550 °C row and A-11's 0.9078 are misprints.

## Sources

- [HW05] Harbison-Walker Refractories Company, *Handbook of Refractory Practice*, © 2005 (the owner's
  copy, git-ignored). The first pass: `hwi-handbook.md`.
- `cones.yaml` (Orton temperature equivalents, `electric-and-thermal.md` §8) for cones 9 to 11.
- [M1] Brosnan, quoted in `refractory-movement-and-mortar.md` §1.1.
- Working scripts (git-ignored, not sources): `scratch/hwi-deep/props/fig34.py`, `fig56.py`,
  `fig37.py`, `fig1.py`, `fig3.py`, `a12.py`.
