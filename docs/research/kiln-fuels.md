# Each reference kiln's fuel: wood, oil and coal as sourced bands

Research A1 of the round of 2026-11-10 (`docs/planning/11-10-26.md`), for ADR 0017 decision 12
("each kiln's own fuel ... with that fuel's composition and heating value looked up from a source").
Which wood, oil or coal each of the 38 fuel-burning reference kilns burned, and that fuel's
composition (C, H, O, N, ash), moisture and net heating value, each as a band with its source.

Read 2026-11-10. Marks: **Read** (read on the fetched page, or in the text extracted from the
downloaded PDF, `scratch/research-a/dl/`, git-ignored), **Snippet** (a search result or a
summarising tool's paraphrase, not checked on the page), **Derived** (arithmetic shown; the
scripts are `scratch/research-a/oil.py`, `summary.py`), "from memory". Olsen is *The Kiln Book*,
4th ed., by printed page; the book's facts are as `core/tests/v2/reference_kilns.yaml` and
`kiln-reference.md` record them. Which wood each region burns, and each place's equilibrium
moisture, are in `kiln-fuelwood-by-region.md` (the same round); this file holds the fuels'
properties and the per-kiln bands.

Not read: Pettersen 1984 (the FPL copy returned HTTP 502, a course mirror failed its certificate;
the 50/6/44 C/H/O the engine uses is now corroborated by [F1] instead, §2.3); Phyllis2's records
for akamatsu and chestnut, which hold no ultimate analysis (Read: #2280 has ash and lignin only,
#190 a net calorific value only); India's BEE fuels guide (only Scribd copies found).

## Short answer

**Wood**, per kg of oven-dry wood (each band the interquartile range of [F1]'s review unless said;
the genus rows are [F1]'s min–max with the median):

| Wood | C % | H % | O % | N % | Ash % | Net heating value, MJ/kg dry | Source |
|---|---|---|---|---|---|---|---|
| any wood (stem wood) | 47.2–50.0 | 5.98–6.30 | 42.6–45.8 | 0.10–0.35 | 0.30–0.74 | 17.9–19.0 (HHV 19.1–20.1) | [F1] Table 1 |
| coniferous wood | 47.8–50.7 | 6.06–6.46 | 42.1–45.3 | 0.10–0.30 | 0.25–0.50 | 18.4–19.3 (HHV 19.5–20.3) | [F1] Table 2 |
| deciduous (broad-leaf) wood | 47.2–49.1 | 5.86–6.20 | 43.0–46.0 | 0.16–0.40 | 0.40–0.81 | 17.6–18.7 (HHV 19.1–19.9) | [F1] Table 3 |
| coniferous branches and twigs | 48.6–50.3 | 5.86–6.58 | 40.2–43.3 | 0.40–0.76 | 0.83–2.27 | 19.1–19.6 | [F1] Table 5 |
| deciduous branches and twigs (brushwood) | 47.0–49.0 | 6.10–6.52 | 41.4–45.1 | 0.27–1.17 | 0.96–3.28 | HHV 19.2–19.9 (one LHV) | [F1] Table 6 |
| *Pinus* (pine), wood | 45.8–53.2 (48.9) | 5.91–6.91 (6.18) | 41.2–46.4 (44.2) | 0.03–0.85 (0.12) | 0.17–1.14 (0.18) | 17.5–19.9 (19.1) | [F1] Tables A1, A2 |
| *Quercus* (oak), wood | 46.1–50.3 (48.0) | 5.40–6.07 (5.90) | 42.7–46.8 (45.1) | 0.11–0.50 (0.30) | 0.20–2.40 (0.51) | 17.0–18.3 (17.5); HHV 18.7–20.1 | [F1] |
| *Betula* (birch), wood | 42.8–50.9 (48.0) | 5.22–6.60 (6.10) | 43.0–48.1 (46.1) | 0.07–0.48 (0.16) | 0.18–0.70 (0.38) | 18.1–19.1 (18.6) | [F1] |
| *Fagus* (beech), wood | 45.9–51.6 (48.4) | 5.89–6.4 (6.20) | 38.7–47.3 (43.4) | 0.06–0.60 (0.35) | 0.17–0.79 (0.59) | 17.0–18.6 (17.7) | [F1] |
| *Castanea* (chestnut), wood | 47.1 (one study) | 4.90 (one) | 47.7 (one) | 0.20 (one) | 0.10 (one) | HHV 18.70 (one) | [F1] |
| *Pseudotsuga* (Douglas-fir), wood | 46.3–52.3 (49.9) | 5.90–8.25 (6.21) | 40.5–46.0 (43.0) | 0.06–0.20 (0.10) | 0.10–2.70 (0.30) | HHV 19.7–21.8 (20.4) | [F1] |
| CEN/TS 14961 typical, coniferous / broad-leaf | – | – | – | – | 0.2–0.5 / 0.2–0.5 | 18.8–19.8 / 18.5–19.2 (daf) | [F2] Table 10 |
| firewood (Finland) | 48–52 | 6.0–6.5 | – | 0.3–0.5 | 0.5–1.2 | 18.5–19.0 | [F3] Annex 10 |

- **Moisture**: none is printed for any kiln. Firewood stored several years holds 15–25 %, one
  summer 25–35 %, fresh 50–60 % (wet basis, [F2] Table 12); air-dried wood 12–20 % (FAO UBET,
  `wood-fuel.md` [W3]); the floor for wood seasoned under cover is the site's outdoor equilibrium
  moisture (`kiln-fuelwood-by-region.md`). The per-kiln band (§5) runs from that floor (the driest
  month's) to 25 %, or to the region's own seasoning where a source gives it (23–35 %).
- **Net heat as fired**: q_net,ar = q_net,d·(100 − M)/100 − 0.02443·M MJ/kg, M the moisture in
  % wet basis ([F4] eq. 2.5; [F3] Annex 5; FAO UBET's eq. 3 with 2.443 for 2.44).
- **Gross to net, dry**: q_net,d = q_gr,d − 212.2·H − 0.8·(O + N) J/g, H, O, N in % dry (EN 14918 /
  EN ISO 18125, [F4] eq. 2.4): 1.29–1.35 MJ/kg for wood (Derived, §2.2).
- **The engine's wood surrogate** (50/6/44 C/H/O, from Pettersen, never read) sits at [F1]'s
  upper quartile for C and inside its quartiles for H and O (§2.3): open data now supports it.

**Oil** (`olsen-oil-drip`; the oil drip of `blakebrough-sturt`):

| Oil | C % | H % | S % | Net heating value | Gross | Source |
|---|---|---|---|---|---|---|
| #2 diesel, Olsen's own | 86 (fuel oils in general) | 13 | 0–2; #2 diesel 0.3 | 18,610 BTU/lb = 43.29 MJ/kg, 132,000–140,000 BTU/gal, sg 0.85; basis not stated | – | Olsen p.196, p.209 |
| light fuel oil (Finland) | 86.2 | 13.7 | 0.1 | 42.4 MJ/kg (36.7 MJ/L, 870 kg/m³) | – | [F3] |
| heating oil | 85–86 | 11–13 | – (O 1–4) | – | – | [F2] Table 19 |
| low-sulphur diesel | – | – | – | 128,488 BTU/gal = 42.1 MJ/kg at sg 0.85 | 138,490 BTU/gal = 45.4 MJ/kg | [F6] |

Band for the engine: **net 42.1–43.3 MJ/kg, C 85–86.2 %, H 13.0–13.7 %** (#2 diesel; [F2]'s lower
H is for heating oils in general). Olsen's 132,000 BTU/gal is exactly his 18,610 BTU/lb at
sg 0.85, between the net (128,488) and gross (138,490) per gallon of [F6]; his 140,000 is above
any net value, a gross figure (Derived, §3). `core/tests/v2/fuel.py` takes 132,000–140,000 as heat:
its top end is gross.

**Coal**:

| Kiln | Coal | Heating value | Composition | Source |
|---|---|---|---|---|
| `singh-coal` (New Delhi) | "Steam coal, Grade B" (p.133, Table 5-1) | Grade B: useful heat value 5,600–6,200 kcal/kg = 23.4–26.0 MJ/kg; on the 2011 GCV grades G4–G6, 5,501–6,400 kcal/kg = 23.0–26.8 MJ/kg gross | UHV = 8900 − 138·(ash + moisture) puts its ash + moisture at 19.6–23.9 % (Derived); the C, H, O of a Grade B coal not found open: the generic coal below carried as the band | [F7]; [F3], [F2] |
| `kato-coal` (Tajimi) | "coal", kind not printed (p.131) | generic coal: net 27.9 MJ/kg dry, 24.8 as received at 10 % moisture, ash 14 % dry | C 68–78 % (71.5), H 3.5–5.0 % (4.5), N 0.8–1.5 %, S < 0.5 % dry [F3]; C 72.5, H 5.6, O 11.0, N 1.3, S 0.94 % [F2] | [F3], [F2] |

So coal **needn't stay refused**: each coal kiln has a sourced band, Singh's from its printed grade,
Kato's a generic one (said so in the working). The shovelful has one open figure, Taylor's 21 lb
(9.5 kg), a shoveler's best load, not a kiln's shovel [F8]; its band is a question for the owner.

## 1. Sources

**[F1] Stolarski, M. J., Dudziec, P., Olba-Zięty, E., Stachowicz, P. and Krzyżaniak, M. (2022),
"Forest Dendromass as Energy Feedstock: Diversity of Properties and Composition Depending on
Systematic Genus and Organ"**, *Energies* 15(4), 1442, doi:10.3390/en15041442, open access, CC BY 4.0
(Read on the PDF's p.1). PDF:
<https://mdpi-res.com/d_attachment/energies/energies-15-01442/article_deploy/energies-15-01442.pdf>
(the article page returned HTTP 403 to the fetch tool; the PDF was downloaded and its text read).
A review of published analyses of 21 temperate genera (5 coniferous, 16 deciduous) by organ. Tables
1–9 give N, mean, median, min, max, quartiles; Tables A1–A2 give each genus and organ as min–max
(median; mean absolute deviation of the median); Tables A10–A24 the genus means. "The mean wood HHV
was 19.66 MJ kg−1 dry matter (d.m.)"; coniferous 19.90, deciduous 19.42 (p.8). Read rows:

| Table (page) | Wood | HHV, MJ/kg d.m., Q1–Q3 (mean) | LHV, Q1–Q3 (mean) | Ash % d.m., Q1–Q3 | C, Q1–Q3 | H, Q1–Q3 | O, Q1–Q3 | N, Q1–Q3 |
|---|---|---|---|---|---|---|---|---|
| 1 (p.8) | all wood | 19.12–20.05 (19.66) | 17.93–19.04 (18.44) | 0.30–0.74 | 47.20–49.99 | 5.98–6.30 | 42.60–45.79 | 0.10–0.35 |
| 2 (pp.8–9) | coniferous | 19.47–20.32 (19.90) | 18.44–19.31 (18.85) | 0.25–0.50 | 47.75–50.72 | 6.06–6.46 | 42.10–45.33 | 0.10–0.30 |
| 3 (p.9) | deciduous | 19.06–19.94 (19.42) | 17.60–18.67 (18.13) | 0.40–0.81 | 47.15–49.10 | 5.86–6.20 | 42.99–46.03 | 0.16–0.40 |
| 5 (p.10) | coniferous branches | 20.57–21.37 (20.87) | 19.11–19.64 (19.40) | 0.83–2.27 | 48.60–50.26 | 5.86–6.58 | 40.20–43.30 | 0.40–0.76 |
| 6 (p.11) | deciduous branches | 19.17–19.94 (19.54) | one value, 13.84 | 0.96–3.28 | 47.00–49.00 | 6.10–6.52 | 41.38–45.08 | 0.27–1.17 |

Genus rows, wood (Tables A1, A2, pp.30–36), min–max (median): *Pinus* ash 0.17–1.14 (0.18), HHV
18.89–21.60 (20.06), LHV 17.50–19.88 (19.13), C 45.80–53.17 (48.94), H 5.91–6.91 (6.18), O
41.19–46.40 (44.22), N 0.03–0.85 (0.12); *Pinus* foliage (needles) ash 1.40–4.72 (2.35), HHV
20.00–23.00 (21.40), C 47.80–54.20, H 6.20–6.90, O 37.90–43.70; *Quercus* ash 0.20–2.40 (0.51), HHV
18.70–20.05 (19.63), LHV 17.00–18.30 (17.51), C 46.10–50.30 (48.00), H 5.40–6.07 (5.90), O
42.70–46.80 (45.10), N 0.11–0.50 (0.30); *Quercus* branches ash 0.75–4.20 (2.26), HHV 17.72–20.87,
C 44.70–48.62, H 6.08–6.81, O 41.01–47.06; *Betula* ash 0.18–0.70 (0.38), HHV 18.02–19.94 (19.64),
LHV 18.10–19.06 (18.61), C 42.76–50.91 (48.00), H 5.22–6.60 (6.10), O 42.98–48.10 (46.13), N
0.07–0.48 (0.16); *Fagus* ash 0.17–0.79 (0.59), HHV 18.30–20.01 (19.23), LHV 17.00–18.60 (17.67), C
45.90–51.60 (48.40), H 5.89–6.4 (6.20), O 38.70–47.30 (43.40); *Castanea* (sweet chestnut only)
wood: ash 0.10, HHV 18.70, C 47.10, H 4.90, O 47.70, N 0.20, each a single value; its branches ash
3.31, C 48.62, H 5.89, O 45.07; *Pseudotsuga* ash 0.10–2.70 (0.30), HHV 19.70–21.77 (20.37), C
46.34–52.30 (49.90), H 5.90–8.25 (6.21), O 40.50–46.02 (43.00); *Picea* ash 0.16–0.92 (0.37), HHV
18.78–21.10 (20.03), LHV 18.40–19.79 (19.11), C 48.30–52.43 (50.45), H 5.80–6.60 (6.20), O
40.63–44.66 (42.75). No *Eucalyptus*, *Acacia*, *Calluna* or *Erica* (temperate European genera
only).

**[F2] Krajnc, N. (2015), *Wood Fuels Handbook***, FAO, Pristina, ISBN 978-92-5-108728-2; "FAO
encourages the use, reproduction and dissemination of material in this information product"
(p.iv). <https://www.bioenergy.org.nz/documents/resource/Reports/wood-fuels-handbook-fao.pdf> (Read,
the PDF's text). p.11: "The net calorific value (NCV0) of oven-dry wood of different species varies
within a very narrow interval, from 18.5 to 19 MJ per Kg. In conifers it is 2 percent higher than in
broad-leaved trees." "Water evaporation involves the 'consumption' of 2.44 MJ per kilo of water."
Table 10 (p.11, after CEN/TS 14961:2010): coniferous wood, ash 0.3 (0.2–0.5) w-%, gross 20.5
(20.2–20.8), net 19.2 (18.8–19.8) MJ/kg daf; broad-leaf wood, ash 0.3 (0.2–0.5), gross 20.2
(19.5–20.4), net 19.0 (18.5–19.2); coniferous forest residues ash 2 (1–4) % d, net 20 (19.5–20.0);
broad-leaf forest residues ash 1.5 (0.8–3), net 19 (18.4–19.1). Table 12 (p.12): "Fresh timber
50–60% 2.0kWh per kg; Timber stored for a summer 25–35% 3.4kWh per kg; Timber stored several years
15–25% 4.0kWh per kg". Table 4 (p.6): basic density, air-dry, typical (variation), kg/m³: Scots pine
510 (330–890), beech 720 (540–910), oak 690 (430–960), chestnut 620 (590–660). Table 19 (p.18), wt %
d.b.: spruce with bark C 49.8, H 6.3, O 43.2, N 0.13; beech with bark C 47.9, H 6.2, O 43.3, N
0.22; coal C 72.5, H 5.6, O 11.0, N 1.30, S 0.940; heating oil C 85–86, H 11–13, O 1–4.

**[F3] Alakangas, E. and Impola, R. (2015), *Quality guidelines for wood fuels in Finland***, VTT
Technical Research Centre of Finland, VTT-M-04712-15 (a translation of their 2014 guideline).
<https://sarjaweb.vtt.fi/julkaisut/muut/2015/VTT-M-04712-15.pdf> (Read, the PDF's text). Annex 5
(p.49): q_p,net,ar = q_p,net,d × (100 − M_ar)/100 − 0.02443 × M_ar. Annex 10, Table 1 (pp.55–57):
firewood net 18.5–19.0 MJ/kg dry, moisture 20–25 %, 13.4–14.5 MJ/kg as received, ash 0.5–1.2 %; coal
27.9 MJ/kg dry, 10 % moisture, 24.8 MJ/kg as received, ash 14 %; light fuel oil 36.7 MJ/L, moisture
0.01–0.02 %, 42.4 MJ/kg as received, 870 kg/m³, ash 0.01 %. Table 2 (pp.58–59), w-% dry: firewood C
48–52, H 6.0–6.5, S < 0.05, N 0.3–0.5; coal C 68–78 (average 71.5), H 3.5–5.0 (4.5), S < 0.5, N
0.8–1.5 (1.3); light fuel oil C 86.2, H 13.7, S 0.1, N 0.01–0.03; heavy fuel oil C 88.4, H 10.1,
S 0.8–0.95. (36.7 MJ/L ÷ 870 kg/m³ is 42.2 MJ/kg, Derived, against the printed 42.4.)

**[F4] Alakangas, E., Hurskainen, M., Laatikainen-Luntama, J. and Korhonen, J. (2016), *Properties
of indigenous fuels in Finland***, VTT Technology 272. <https://publications.vtt.fi/pdf/technology/2016/T272.pdf>
(Read, the PDF's text). Eq. 2.4 (p.27): q_p,net,d = q_V,gr,d − 212.2 × w(H)_d − 0.8 × [w(O)_d +
w(N)_d] (J/g); "The default values for hydrogen, w(H)_d, are 6.1–6.3% for wood-based fuels ... The
value for w(O)_d + w(N)_d is 40.4–44.5% for wood-based fuels" (EN ISO 18125:2016 Appendix H, p.28);
eq. 2.5 (p.28) the as-received formula of [F3]. "The net calorific value of wood on a dry basis is
18.3–20.0 MJ/kg" (p.61). Table 4.3 (p.54): wood in general C 48–50, H 6.0–6.5, O 38–42 % dry.
Table 4.21 (p.77), stem wood net MJ/kg dry: pine 19.33, spruce 19.02, downy birch 19.19, silver
birch 19.15, aspen 18.65. "The ash content of debarked stem wood is usually 0.3–0.7 w-%" (p.57).

**[F5] Olsen, *The Kiln Book*, 4th ed.** p.196: fuel oils' composition "about carbon 86 %, hydrogen
13 %, sulphur 0–2 %"; p.209: #2 diesel 132,000–140,000 BTU/gal, specific gravity 0.85, 18,610
BTU/lb, 0.3 % sulphur; p.196: bituminous ("gas") coal gives about 75 % coke and 25 % coal gas;
p.133: Singh's "Steam coal, Grade B" (as `kiln-reference.md` §15–16 and the dataset record them).

**[F6] US DOE Alternative Fuels Data Center, "Fuel Properties Comparison"**,
<https://afdc.energy.gov/fuels/properties> (Read through the fetch tool): low-sulphur diesel "C8 to
C25", lower heating value 128,488 Btu/gal, higher heating value 138,490 Btu/gal (its footnote "c",
not shown to the tool). No density printed.

**[F7] Singh, A. K., "Indian coal", a presentation at an IEA event** (no date on the slides read;
resources "as on 1.4.2017").
<https://iea.blob.core.windows.net/assets/imports/events/243/16_India_A.KumarSingh.pdf> (Read, the
PDF's text). p.14, non-coking coal, "Useful Heat Value (k.cal/kg)": A > 6200; **B 5600–6200**; C
4940–5600; D 4200–4940; E 3360–4200; F 2400–3360; G 1300–2400; "Useful Heat Value = 8900 – 138
(Ash + Moisture) (At 60% R.H & 40°C Temperature)", "(Department of Coal, Ministry of Energy,
1979)". p.15: "Old UHV based grading / New GCV based grading", B → G4 6101–6400, G5 5801–6100, G6
5501–5800 kcal/kg, "(Gazette Notification, Ministry of Coal, 30th December 2011)". p.9: Barakar
coal "Carbon - 85 to 90% (on dmmf basis)", "Ash - 15 to 30%", moisture < 2 to 6 %. A Lok Sabha
answer giving the same A and B bands was seen only as a search snippet (Snippet; its host didn't
resolve).

**[F8] Taylor, F. W. (1911), *The Principles of Scientific Management*** (public domain), Project
Gutenberg #6435, <https://www.gutenberg.org/cache/epub/6435/pg6435.txt> (Read through the fetch
tool): "it was found that a first-class man would do his biggest day's work with a shovel load of
about 21 pounds"; shovels were issued to "hold a load of 21 pounds of whatever class of material
they were to handle", "a small shovel for ore, say, or a large one for ashes".

## 2. Wood

### 2.1 Composition and heating value

The bands in the short answer. What they say:
- C, H and O vary little between genera; the spread inside a genus (between studies) is as wide as
  between genera. Pine and Douglas-fir run higher in heating value (more lignin and resin), oak and
  beech lower: [F1]'s genus LHV medians are oak 17.5, beech 17.7, birch 18.6, pine and spruce
  19.1 MJ/kg dry (Table A1).
- Bark, branches, twigs and needles carry more ash (1–3 %, needles 2.4 % median) and slightly more
  heating value than stem wood ([F1] Tables 4–9, A1).
- [F1]'s HHV and LHV come from different sets of studies (N 163 against 108), so their difference
  isn't the gross-to-net step for one sample: for oak the medians differ by 2.1 MJ/kg, where eq. 2.4
  of [F4] gives 1.3 (Derived, §2.2). The engine wants net: where a genus's own LHV range exists it is
  the band; else the class's LHV quartiles.

### 2.2 Gross to net, and the moisture

- Dry basis ([F4] eq. 2.4): with [F4]'s wood defaults, H 6.1–6.3 % and O + N 40.4–44.5 %, the step
  from gross to net is 212.2 × 6.1–6.3 + 0.8 × 40.4–44.5 = 1.33–1.37 MJ/kg (Derived); 1.29–1.35 over
  [F1]'s quartiles.
- As fired ([F3], [F4] eq. 2.5): q_net,ar = q_net,d·(1 − M/100) − 0.02443·M. Per kg of oven-dry wood
  burned at moisture w (wet fraction): q_net,d − 2.443·w/(1 − w): at 19 MJ/kg dry, 18.73 at 10 %,
  18.39 at 20 %, 18.19 at 25 %, 17.68 at 35 % (Derived). This is `fuel.py`'s formula with 2.443 for
  2.44.

### 2.3 The engine's surrogate against the data

v2's gas model burns wood as 50/6/44 C/H/O (`heat/gas.py`, after `firebox-efficiency.md` §4,
which quoted Pettersen 1984 through search results). Against [F1] Table 1 (all wood): C 50 at the
upper quartile (49.99), H 6 inside 5.98–6.30, O 44 inside 42.60–45.79 (Derived). The surrogate is a
fair centre for coniferous wood (Table 2: C 47.75–50.72, H 6.06–6.46) and a little carbon-rich for
oak and birch (medians 48.0). Pettersen stays unread; [F1] is now the source for the band.

## 3. Oil

- Olsen fires his drip-oil kiln on #2 diesel by choice ("kerosene and #1 also burn clean"; once on
  free crankcase oil, p.209), and the printed 60–75 gal to cone 10 is #2 diesel (p.208). The
  Blakebrough kiln's drip oil isn't named (p.208, Fig 8-21); the book's drip practice is #2 diesel
  (p.207–209), so that is the assumed oil.
- His figures hang together: 18,610 BTU/lb × 0.85 × 8.3454 lb/gal = 132,000 BTU/gal (Derived).
  18,610 BTU/lb is 43.29 MJ/kg. [F6]'s net 128,488 BTU/gal is 42.13 MJ/kg at sg 0.85 (42.79 at the
  0.837 of a lighter diesel), its gross 138,490 is 45.41 MJ/kg; [F3]'s light fuel oil is 42.4 MJ/kg
  net. So Olsen's 43.3 MJ/kg lies 2–3 % above the net values and 5 % below gross: his basis isn't
  printed; the band for the engine's net heat is **42.1–43.3 MJ/kg**. His 140,000 BTU/gal top is a
  gross figure (above [F6]'s gross), so the dataset's 132,000–140,000 mixes bases.
- Composition: C 86 %, H 13 % (Olsen p.196, fuel oils generally); 86.2/13.7 (light fuel oil, [F3]);
  85–86/11–13 with O 1–4 (heating oil, [F2]). For #2 diesel: C 85–86.2 %, H 13.0–13.7 %, S 0.1–0.3 %
  (Olsen's 0.3 % for his #2, p.209).
- Not found: a used crankcase oil's composition or heating value in an open source read here.

## 4. Coal

- **Singh's Grade B steam coal** (p.133). India's non-coking grades (1979) are set by "useful heat
  value", 8900 − 138 × (ash + moisture) kcal/kg at 60 % RH and 40 °C ([F7] p.14): Grade B is UHV
  5,600–6,200 kcal/kg, so its ash plus moisture is 19.6–23.9 % (Derived). The 2011 GCV grades map B
  onto G4–G6, 5,501–6,400 kcal/kg gross, 23.0–26.8 MJ/kg ([F7] p.15). UHV isn't a calorimetric value
  (it is a formula on the proximate analysis), so the engine's band is the GCV one, gross, on the
  equilibrated basis; the net, dry value needs the coal's H and moisture, which aren't printed for
  Grade B: with [F3]'s H 3.5–5.0 % dry and [F2]'s O + N about 12 %, the gross-to-net step is about
  0.75–1.07 MJ/kg plus the moisture's (Derived from [F4] eq. 2.4, an assumption for this coal). The Barakar coals are
  C 85–90 % dmmf ([F7] p.9). Kiln-specific: the book prints no shovel's weight (the dataset's gap).
- **Kato's coal** (p.131): the kind isn't printed. Olsen's p.196 speaks of bituminous coal for
  kilns, generally. Carried as the generic coal of [F3] and [F2]: net 27.9 MJ/kg dry, ash 14 % dry,
  C 68–78 %, H 3.5–5.6 %, O 11 %, N 0.8–1.5 %, S < 0.5–0.94 %. Said in the working as generic.
- **The shovelful**: [F8]'s 21 lb (9.5 kg) is a shoveler's best sustained load, with shovels sized
  to hold it whatever the material; neither kiln's shovel is described. A single sourced point:
  its band is the owner's question (§6).

## 5. Each kiln's fuel

The dataset (`core/tests/v2/reference_kilns.yaml`) carries each kiln's fuel as heat facts:
`fuel_species` (printed where the book names it, else assumed with its source), `fuel_moisture`
(% wet basis, as fired), `fuel_heating_value` (net, MJ per kg of oven-dry wood), `fuel_carbon`,
`fuel_hydrogen`, `fuel_oxygen`, `fuel_ash` (% dry), and for coal `fuel_nitrogen`, `fuel_sulphur`
and `fuel_unit_mass` (the shovel). The rules, so every band traces:

- **The wood's class**: a wood the book names, or one a source names for the kiln's place
  (`kiln-fuelwood-by-region.md`), takes its class: coniferous or deciduous wood ([F1] Tables 2–3),
  deciduous branches for brushwood (Table 6). A wood no source names takes "either": the two
  classes' interquartile ranges joined. A tradition's wood elsewhere ("pine by analogy") is said in
  the fact's reason and doesn't narrow the band.
- **The heating value**: the genus's own LHV range where [F1] has one (pine 17.50–19.88; beech
  17.00–18.60; oak and birch together 17.00–19.06), else the class's LHV interquartile range.
- **The composition**: the class's interquartile ranges (C, H, O, ash).
- **The moisture**: from the driest month's outdoor EMC at the nearest station of [S1] (wet basis;
  `kiln-fuelwood-by-region.md` §2), to 25 %, firewood "stored several years" ([F2] Table 12); where
  the region's own advice is shorter seasoning, to that: Denmark 23 % (one or two summers, [E5]),
  New Hampshire 30 % (6–8 months, "seasoned around 30%", [N1]), Alberta 35 % (one summer, [C1];
  [F2]'s 25–35 % for wood stored a summer). With no place printed, from FAO UBET's 12 % air-dried.

| Kiln | Fuel (status) | Class for the band | Net, MJ/kg dry | Moisture, % wet | Station |
|---|---|---|---|---|---|
| `anagama-hole` | wood, not named (assumed) | either | 17.60–19.31 | 12–25 | none |
| `bae-gilgama` | slab wood, kind not printed (pp.107–108); Korean kilns burn pine dried a year, a tradition | either | 17.60–19.31 | 12–25 | none (built at an NCECA, USA) |
| `bidai`, `kawaii`, `kyoto-climbing`, `suzuki-kyoto` | split pine, Kyoto's kilns ([K1], read) | coniferous, *Pinus* | 17.50–19.88 | 9.7–25 | Kobe |
| `blakebrough-sturt` | sticks, kind not found ([A1]); and #2 diesel for the drip (assumed) | either; oil | 17.60–19.31; oil 42.1–43.3 | 10.2–25 | Sydney |
| `breda-bottle` | chestnut (printed p.166), *Castanea sativa* | deciduous | 17.60–18.67 | 11.7–25 | Barcelona |
| `chappell-domura` | wood, not named | either | 17.60–19.31 | 8.7–25 | Japan's three |
| `church-skaelskor` | wood, not named (Danish firewoods [E5]) | either | 17.60–19.31 | 11.2–23.1 | Copenhagen |
| `conrad-teardrop` | wood, not named | either | 17.60–19.31 | 12–25 | none |
| `ellington-new-hog` | pine slabs ([U2], read) | coniferous, *Pinus* | 17.50–19.88 | 10.2–25 | Charlotte |
| `falcone-pompeii` | long slats, kind not found | either | 17.60–19.31 | 11.5–25 | Naples |
| `fast-fire` | "wood of any kind" (printed p.139) | either | 17.60–19.31 | 12–25 | none |
| `fast-fire-anderson` | wood, not named | either | 17.60–19.31 | 6.1–25 | Grand Junction (Denver 8.6) |
| `fireworks-edmonton` | wood, not named (Alberta's firewoods [C1]) | either | 17.60–19.31 | 9.3–35 | Edmonton |
| `fujiwara-bizen` | red pine ([K2]–[K4], read), with pine needles (pp.103–104) | coniferous, *Pinus* | 17.50–19.88 (needles about 21) | 9.7–25 | Kobe |
| `groundhog-basic` | pine (Catawba Valley [U1], [U2]) | coniferous, *Pinus* | 17.50–19.88 | 10.2–25 | Georgia, North Carolina |
| `hollyweird`, `olsen-two-chamber` | wood, not named (Olsen's own; place not printed: p.170 prints his kit business's address, Mountain Center, California, read on the page image; that his kilns stood there isn't said) | either | 17.60–19.31 | 12–25 | none |
| `hotchkiss-raw-clay` | wood (the fuel isn't named) | either | 17.60–19.31 | 8.8–25 | Sacramento (if near its clay) |
| `kannofen` | beech ([E1], read: a Höhr-Grenzhausen pottery's former fuel) | deciduous, *Fagus* | 17.00–18.60 | 10.6–25 | Luxembourg, Berlin |
| `kenzan-muffle`, `kitade-tojilo` | wood, not named (pine by analogy only) | either | 17.60–19.31 | 8.7–25 | Japan's three |
| `la-borne` | split oak and birch, then branch bundles (printed p.111) | deciduous wood and branches | 17.00–19.06 (bundles 17.8–19.1) | 10.7–25 | Paris |
| `meaders-cheever`, `meaders-david` | wood ("wood-fueled", [U3]); pine slabs by the region's analogy | either | 17.60–19.31 | 10.9–25 | Athens, Georgia |
| `miravet` | long wood, chips, bundles, grass, slash, slats (printed pp.158–160) | all wood | 17.93–19.04 | 11.7–25 | Barcelona |
| `moveros-umbrella` | heather and any brushwood (printed pp.153–154) | deciduous branches | 17.8–19.1 | 7.6–25 | Madrid |
| `ninodaguia` | pine (printed pp.156–157), *Pinus pinaster* ([E3]) | coniferous, *Pinus* | 17.50–19.88 | 7.6–25 | Madrid (Bilbao 11.0) |
| `phoenix-nh` | wood, not named (New Hampshire's firewoods [N1]) | either | 17.60–19.31 | 10.2–30 | Concord |
| `phoenix-wright` | wood, not named | either | 17.60–19.31 | 10.5–25 | Portland |
| `singh-lowfire` | hardwood (printed p.155) | deciduous | 17.60–18.67 | 5.9–25 | New Delhi |
| `tamba`, `tobe` | wood, not named (red pine by analogy only) | either | 17.60–19.31 | 9.7–25 | Kobe |
| `olsen-oil-drip` | #2 diesel (printed pp.208–209) | – | 42.1–43.3 | – | – |
| `singh-coal` | steam coal, Grade B (printed p.133) | generic coal composition | gross 23.0–26.8 (equilibrated) | ash + moisture 19.6–23.9 | – |
| `kato-coal` | coal, kind not printed (p.131) | generic coal | about 27.9 | about 10 | – |

The class bands, % dry ([F1]): coniferous C 47.75–50.72, H 6.06–6.46, O 42.10–45.33, ash 0.25–0.50;
deciduous C 47.15–49.10, H 5.86–6.20, O 42.99–46.03, ash 0.40–0.81; either C 47.15–50.72, H
5.86–6.46, O 42.10–46.03, ash 0.25–0.81; all wood C 47.20–49.99, H 5.98–6.30, O 42.60–45.79, ash
0.30–0.74; deciduous branches C 47.00–49.00, H 6.10–6.52, O 41.38–45.08, ash 0.96–3.28.

Bundles and slabs have no sourced weight (`kiln-fuelwood-by-region.md` §3), so the Suzuki and Tamba
bundles stay unconverted; a Kyoto kiln burned 1,500 bundles of pine in 46 h ([K1], a rough figure).

## 6. Questions for the owner

1. **Moisture**: the band runs from each site's outdoor equilibrium moisture to 25 % ("stored several
   years", [F2]). Kiln wood stored only a summer is 25–35 %: should any kiln take the wetter band?
2. **The coal shovel**: the only open figure is Taylor's 21 lb best load. Carry 21 lb as the point,
   or a band (whose ends would be the owner's)?
3. **Olsen's 140,000 BTU/gal** for #2 diesel is gross: take the net band 42.1–43.3 MJ/kg (128,500–
   132,000 BTU/gal) for the oil kiln's printed 60–75 gal?
