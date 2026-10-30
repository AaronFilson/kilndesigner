# Electric and thermal reference data

Compiled 2026-10-21 for kilndesigner (see `docs/planning/02-plan.md`).
Every value has a source, given as [S#] in the Sources list at the end.

How to read this file:

- **Verified**: read from the source page itself (HTML page or data sheet text).
- **Excerpt**: taken from a search-engine text extract of a PDF. The PDF could not be opened with
  the tools available here (no shell, no PDF renderer). Check the column alignment before you rely
  on it.
- **Derived**: worked out here from sourced inputs. The formula is shown.
- **Not found**: no source located. No number is given.

Unit conversions used:

- 1 Btu·in/(h·ft²·°F) = 0.144228 W/(m·K)
- 1 W/in² = 0.155 W/cm², and 1 W/cm² = 6.4516 W/in²
- 1 Btu/(lb·°F) = 4.1868 kJ/(kg·K)
- °F = °C × 9/5 + 32

---

## 1. Resistance wire for kiln elements

### 1.1 Basic properties (Kanthal data sheets, verified)

| Alloy | ρ at 20 °C (Ω·mm²/m) | ρ at 20 °C (Ω·cmil/ft) | Density (g/cm³) | Max continuous temp in air (°C) | Melting point (°C) | Emissivity, fully oxidized | Source |
|---|---|---|---|---|---|---|---|
| Kanthal A-1 | 1.45 | 872 | 7.10 | 1400 | 1500 | 0.70 | [S1] |
| Kanthal APM | 1.45 | not stated | 7.10 | 1425 | 1500 | 0.70 | [S2] |
| Kanthal AF | 1.39 | 836 | 7.15 | 1300 | 1500 | 0.70 | [S3] |
| Kanthal D | 1.35 | 812 | 7.25 | 1300 | 1500 | 0.70 | [S4] |
| Nikrothal 80 (NiCr 80/20) | 1.09 | not stated | 8.30 (other makers: 8.40–8.41 [S81, S82, S83]) | 1200 | 1400 | 0.88 | [S5]; ρ also [S81], 1.08 [S82]; max temp [S81, S82], Omega 1150 [S83] |

Cross-checks (2026-10-24): A-1-class FeCrAl, Aperam Resistohm 145 gives ρ 1.45, density 7.10,
melting 1500 °C, but max 1300 °C [S79]. JLC FeCrAl 135 gives 7.25 g/cm³ and max 1200 °C [S80].
See the Corroboration section.

Nominal composition of A-1 and APM: 22% Cr, 5.8% Al, balance Fe [S6].

Other A-1 data from [S1] (verified):

- Curie point about 600 °C. Poisson's ratio 0.30.
- Thermal expansion (×10⁻⁶/K): 11 (20–250 °C), 12 (20–500 °C), 14 (20–750 °C), 15 (20–1000 °C).
- Thermal conductivity (W/(m·K)): 11 at 50 °C, 20 at 600 °C, 22 at 800 °C, 26 at 1000 °C,
  27 at 1200 °C, 35 at 1400 °C.
- Specific heat (kJ/(kg·K)): 0.46 at 20 °C, 0.56 at 200 °C, 0.63 at 400 °C, 0.75 at 600 °C,
  0.71 at 800 °C, 0.72 at 1000 °C, 0.74 at 1200 °C, 0.80 at 1400 °C.
- Tensile strength (MPa): 34 at 900 °C, 18 at 1000 °C, 10 at 1100 °C, 6 at 1200 °C, 4 at 1300 °C.
- Creep strength, 1% in 1000 h (MPa): 1.2 at 800 °C, 0.5 at 1000 °C.

### 1.2 Temperature factor Ct (R_T = Ct · R20)

Verified from the Kanthal data sheets [S1–S5]. The sheets start at 100 °C. At 20 °C, Ct = 1.00 by
definition, because R20 is the reference.

| T (°C) | T (°F) | A-1 | APM | AF | D | Nikrothal 80 |
|---|---|---|---|---|---|---|
| 20 | 68 | 1.00 (definition) | 1.00 (definition) | 1.00 (definition) | 1.00 (definition) | 1.00 (definition) |
| 100 | 212 | 1.00 | 1.00 | 1.00 | 1.00 | 1.01 |
| 200 | 392 | 1.00 | 1.00 | 1.01 | 1.01 | 1.02 |
| 300 | 572 | 1.00 | 1.00 | 1.01 | 1.01 | 1.03 |
| 400 | 752 | 1.00 | 1.00 | 1.02 | 1.02 | 1.04 |
| 500 | 932 | 1.01 | 1.01 | 1.03 | 1.03 | 1.05 |
| 600 | 1112 | 1.02 | 1.02 | 1.04 | 1.04 | 1.04 |
| 700 | 1292 | 1.02 | 1.02 | 1.04 | 1.05 | 1.04 |
| 800 | 1472 | 1.03 | 1.03 | 1.05 | 1.06 | 1.04 |
| 900 | 1652 | 1.03 | 1.03 | 1.05 | 1.07 | 1.04 |
| 1000 | 1832 | 1.04 | 1.04 | 1.06 | 1.07 | 1.05 |
| 1100 | 2012 | 1.04 | 1.04 | 1.06 | 1.07 | 1.06 |
| 1200 | 2192 | 1.04 | 1.04 | 1.06 | 1.08 | 1.07 |
| 1300 | 2372 | 1.04 | 1.04 | 1.06 | 1.08 | not listed (above max) |
| 1400 | 2552 | 1.05 | 1.05 | not listed | not listed | not listed |

Notes:

- Nikrothal 80's Ct is not monotonic. It peaks at 500 °C (1.05) and dips to 1.04 from 600 to 900 °C.
  Interpolate it piecewise. Do not fit a smooth curve.
- Ct is tabulated to two decimals only. Linear interpolation between rows is the practical choice.
- Independent cross-check (derived from mean temperature coefficients): Aperam Resistohm 145,
  33×10⁻⁶/K over 20–1000 °C, gives Ct(1000) = 1 + 33e-6 × 980 = 1.032 vs Kanthal A-1 1.04 [S79].
  JLC NiCr 80:20, 60×10⁻⁶/K, gives Ct(1000) = 1.059 vs Nikrothal 80 1.05 [S82].

### 1.3 Generic FeCrAl equivalents (Chinese GB/T 1234 grades)

The GB/T 1234 standard itself sits behind a paywall [S7]. The figures below come from supplier
listings only [S8]. Treat them as unverified.

| Grade | Rough Kanthal analogue | ρ20 (μΩ·m = Ω·mm²/m) | Density (g/cm³) | Max service temp (°C) |
|---|---|---|---|---|
| 0Cr25Al5 | Kanthal D class | 1.42 | 7.1 | 1250 (one supplier) |
| 0Cr21Al6Nb | Kanthal A-1/AF class | 1.45 | 7.1 | sources conflict (not found reliably) |
| 0Cr27Al7Mo2 | above A-1 | 1.53 | 7.1 | 1400 (one supplier) |

The "analogue" column is a judgment from the resistivity figures. It is not from a source.

### 1.4 Maximum element temperature by atmosphere (Kanthal, verified)

All values in °C, from [S9].

| Atmosphere | A-1 / APM | AF | D | Nikrothal 80 |
|---|---|---|---|---|
| Air, dry | 1400 (APM 1425) | 1300 | 1300 | 1200 |
| Air, moist (3% H₂O) | 1200 | 1200 | 1200 | 1150 |
| Nitrogen (second value: pre-oxidized) | 1200 / 1050 | 1250 / 1100 | 1150 / 1000 | 1250 |
| Argon | 1400 | 1400 | 1300 | 1250 |
| Exothermic gas (10% CO, 15% H₂, 5% CO₂, 70% N₂) | 1150 | 1150 | 1100 | 1100 |
| Endothermic gas (20% CO, 40% H₂, 40% N₂) | 1050 | 1050 | 1000 | 1100 |
| Hydrogen | 1400 | 1400 | 1300 | 1250 |
| 75% H₂ / 25% N₂ | 1200 | 1200 | 1100 | 1100 |
| Vacuum, 10⁻³ torr | 1150 | 1200 | 1100 | 1100 |

### 1.5 Behaviour in reducing atmospheres

From Kanthal (verified, [S6] and [S9]):

- FeCrAl alloys form an Al₂O₃ (alumina) layer. Kanthal says it adheres better than the Cr₂O₃ layer
  on NiCr alloys. It is also a better diffusion barrier and electrical insulator [S6].
- Kanthal says its alloys resist carburizing atmospheres better than Nikrothal (NiCr). They also
  resist sulphur compounds far better. Kanthal says NiCr is "highly susceptible" to sulphur [S6].
- The atmosphere table (§1.4) shows the trade-off. In strongly reducing, CO and H₂ rich
  endothermic gas, Nikrothal 80 is allowed 1100 °C. Kanthal A-1/APM/AF are allowed only 1050 °C,
  and D only 1000 °C [S9].
- Pre-oxidation is recommended before use in protective atmospheres: 7–10 h in air at 1050 °C [S9].
- NiCr alloys suffer "green rot". Kanthal gives the range as 800–950 °C in one place and
  500–950 °C in another, so the page is inconsistent [S9].
- Ceramic supports should have Al₂O₃ ≥ 45%, iron oxide < 1% and alkali oxides < 0.1% [S9].
- Boron compounds attack both alloy families above 900 °C [S9].

Kiln practice (secondary sources):

- Reducing atmospheres and some fumes corrode the oxide crust. Venting early in the firing is
  advised [S10].
- Forum guidance says to run a re-oxidizing firing after reduction firings in an electric kiln.
  It says this is not needed if use stays below 1050 °C, or for fibre-lined kilns [S11]. This is
  anecdotal.
- **Guidance from Kanthal or kiln makers on elements in gas/electric hybrid kilns: not found.**
  A patent describes switching element heating off during high-temperature reduction. It also
  notes that SiC elements are not harmed by reduction [S12].
- **Which alloy tolerates kiln reduction better:** no source addresses CO-rich kiln reduction
  directly. From the Kanthal table, NiCr is allowed a higher temperature in endothermic
  (reducing) gas, but NiCr tops out at 1200 °C in air. FeCrAl resists carburization and sulphur
  better [S6, S9]. This is an inference from the sources, not a sourced recommendation.

### 1.6 Surface load and element geometry (Kanthal)

**Olsen disagrees with the 17.5 W/in² below** (4th ed., Verified):
normal electric kilns 5–9 W/in² (p.254); for cone 10, 6.4–9 W/in² (p.257); his worked 26 kW
example comes out at 7.4 W/in² (p.259). That is about half of Krueger's figure. Lower loads give
a cooler wire and longer element life. Power density 1.0–1.2 W/in³ (1.5–2.07 kW/ft³, p.256)
agrees with §7. Coil OD 5–6 × the wire, pitch 2 × the wire, groove 1.25 × the coil OD (p.247,
p.259–260) agree with the rules below.

General rules (verified, [S13]):

- Surface load p = P / A, where A is the wire surface area. Units are W/cm² or W/in².
- The maximum surface load falls as furnace temperature rises. Kanthal publishes this as diagrams
  for A-1/AF/APM and Nikrothal. **The diagram values are image-only and were not readable here:
  not found as numbers.**
- The diagrams assume thyristor control. For on/off control, use surface loads about 20% lower.
- Coil diameter ratio D/d (outer coil diameter to wire diameter) should ideally be 5 to 12.
- Coil pitch is normally 2 to 4 times the wire diameter.
- Element types A and B: minimum wire diameter 5 mm. Type C (wire on ceramic tube) and type D
  (wire in grooves): minimum wire diameter 3 mm [S13].
- Recommended maximum loop length: 300 mm below 900 °C, 250 mm at 1000 °C, 200 mm at 1100 °C,
  150 mm at 1200 °C, 100 mm at 1300 °C [S13].
- Kanthal recommends at least 3 mm wire and 2 mm strip to maximize furnace element life [S9].

Element type data (Kanthal "Key data for Kanthal elements", verified [S14]. The page's column
alignment was reconstructed by order, so check it against the page):

| Element type | Support | Max furnace temp (°C) | Max wall loading at 1000 °C (kW/m²) | Max surface load at 1000 °C (W/cm²) | Wire d (mm) | Outer coil D | Min pitch at max loop length |
|---|---|---|---|---|---|---|---|
| Spiral on ceramic tubes | sillimanite | 1300 | 40 | 3–4 | 2.0–6.5 | 12–14 d | 3d |
| Spiral in grooves | chamotte grade 28 | 1250 | 35 | 3–4 | 2.0–5.0 | 5–6 d | 2d |
| Porcupine (ceramic tubes) | sillimanite | 800 | – | – | 1.0–6.5 | – | 3d |
| Rod over bend | Kanthal APM rods | 1300 | 50 | 5–6 | ≥ 5.0 | – | 40 mm |
| Corrugated | U-shaped Kanthal staples | 1300 | 50 | 3–6 | 2.0–5.0 | – | 40 mm |
| Looped | ceramic tubes | 1300 | 60 | 5–6 | ≥ 5.0 | – | 40 mm |

Kiln-maker figure (verified [S15]): Krueger Pottery gives about **17.5 W/in²** maximum wire loading
for Kanthal A-1 coils in brick grooves in ceramic kilns rated about 2300 °F (1260 °C). That is
**2.71 W/cm²** (derived). Krueger also notes that lower loading gives longer element life.

Example kiln element (Krueger 240 V 24 A replacement element, verified [S15]): coil OD 0.4570 in,
60 in unstretched, 120 in minimum stretched, 240 in maximum stretched. The page gives no wire gauge
for this element. It recommends 15 ga Kanthal A-1 for element pins.

### 1.7 Kanthal worked example: wire element design (validation test)

Source: Kanthal "Design calculations and standard tolerances / Calculations of wire: examples" PDF
[S16]. The PDF could not be opened here. The inputs and Kanthal's stated results below are
**excerpts** from search-engine extracts of that PDF. The intermediate values are **derived**.
Ct comes from the verified AF data sheet [S3]. The derived values reproduce every Kanthal-stated
result, which is a good check on the reading.

**Inputs (excerpt):**

| Quantity | Value |
|---|---|
| Power P | 20 kW (20 000 W) |
| Voltage U | 220 V |
| Target surface load p | 4.0 W/cm² |
| Wire temperature | 1200 °C |
| Alloy | Kanthal AF |
| ρ20 | 1.39 Ω·mm²/m (verified [S3]) |
| Ct at 1200 °C | 1.06 (verified [S3]) |

**Steps:**

| Step | Formula | Result | Status |
|---|---|---|---|
| 1. Current | I = P/U | 90.909 A (Kanthal: 90.9 A) | excerpt + derived |
| 2. Hot resistance | R_T = U²/P | 2.420 Ω | derived |
| 3. Cold resistance | R20 = R_T/Ct | 2.283 Ω | derived |
| 4. Wire diameter | d³ = 4·ρ20·Ct·P² / (10·π²·U²·p), with d in mm, ρ in Ω·mm²/m, p in W/cm² | d³ = 123.38 mm³, so d = 4.978 mm (Kanthal: about 4.98 mm) | excerpt + derived |
| 5. Choose standard size | nearest standard | 5.0 mm (Kanthal: 5.0 mm) | excerpt |
| 6. Cross-section | q = π·d²/4 | 19.635 mm² | derived |
| 7. Wire length | L = R_T·q / (ρ20·Ct) | 32.25 m | derived |
| 8. Surface area | A = 10·π·d·L (cm², d in mm, L in m) | 5066 cm² | derived |
| 9. Actual surface load | p = P/A | 3.948 W/cm² (Kanthal: 3.95 W/cm², 25.5 W/in²) | excerpt + derived |
| 10. Wire mass | m = q·L·γ, with γ = 7.15 g/cm³ | 633.2 cm³, so 4.53 kg | derived |

The factor 10 in steps 4 and 8 comes from the mixed units: A [cm²] = π · d[mm] · 0.1 · L[m] · 100.

Kanthal also describes a "table lookup" method that uses the ratio of surface area to cold
resistance (η) [S16]. **The η table values: not found.**

Other Kanthal examples exist: a 1000 W, 220 V flat-iron tubular element and a 2000 W, 230 V
broiler element, in "appliance calculations" [S17]. **Their full inputs and outputs: not found.**

---

## 2. Wire gauges (AWG = B&S)

AWG is defined by ASTM B258 [S18]: d_n = 0.005 in × 92^((36 − n)/39) = 0.127 mm × 92^((36 − n)/39).
Each gauge step changes the diameter by 92^(1/39) ≈ 1.1229. Dimensions are taken at 20 °C [S18].
AWG and Brown & Sharpe (B&S) are the same series [S19].

Table from [S19] (verified). It matches the B258 formula.

| AWG / B&S | Diameter (in) | Diameter (mm) |
|---|---|---|
| 8 | 0.1285 | 3.264 |
| 9 | 0.1144 | 2.906 |
| 10 | 0.1019 | 2.588 |
| 11 | 0.0907 | 2.305 |
| 12 | 0.0808 | 2.053 |
| 13 | 0.0720 | 1.828 |
| 14 | 0.0641 | 1.628 |
| 15 | 0.0571 | 1.450 |
| 16 | 0.0508 | 1.291 |
| 17 | 0.0453 | 1.150 |
| 18 | 0.0403 | 1.024 |
| 19 | 0.0359 | 0.912 |
| 20 | 0.0320 | 0.812 |

ASTM B258-18 Table 1 itself (paywalled): not read. Compute the values from the formula and round to
4 significant figures, as B258 does.

---

## 3. US electrical rules for kilns

The NFPA 70 (NEC) text was not read directly, because it needs an NFPA login. The section numbers
below come from secondary sources [S20, S21, S22]. Verify them against the edition the
jurisdiction has adopted.

| Rule | NEC reference | Content (as reported by secondary sources) |
|---|---|---|
| Continuous load | Article 100, definitions | Maximum current expected to continue for 3 hours or more [S20, S21] |
| Branch-circuit conductors | 210.19(A)(1) | Ampacity ≥ noncontinuous load + 125% of continuous load [S22] |
| Branch-circuit overcurrent device | 210.20(A) | Rating ≥ noncontinuous load + 125% of continuous load. There is an exception for assemblies listed for 100% operation [S20] |
| Appliance branch circuit | 422.10(A) | The 125% minimum, as forums cite it [S23] |
| Single non-motor appliance OCPD maximum | 422.11(E) | Not above the marked rating. If unmarked: 20 A for ≤ 13.3 A, or 150% of rating for > 13.3 A, with the next standard size up permitted [S23] |
| Conductor protection | 240.4 | Still applies to the conductors [S23] |
| Standard ampere ratings | 240.6(A) | Fuses and inverse-time breakers: 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 125, 150, 175, 200, 225, 250, 300, 350, 400, 450, 500, 600, 700, 800, 1000, 1200, 1600, 2000, 2500, 3000, 4000, 5000 and 6000 A; fuses also 1, 3, 6, 10 and 601 A. Manufacturers make other ratings, "and the use of these non-standard ampere ratings is permitted". From the 2005 NEC [S100] Verified |
| Receptacle rating | 210.21(B)(1) | A single receptacle on an individual branch circuit must be rated ≥ the branch circuit. This bears on a 50 A cord on a 60 A circuit [S24] |
| Industrial process heating | Article 425 | One forum opinion classes kilns here, which would make them continuous loads [S24]. Unverified |

Kiln-maker guidance (verified):

- **L&L** [S25]: Multiply the kiln's full-load amps by 1.25. Round up to the next standard
  breaker size. L&L calls this the NEC-based rule for resistive heaters that run more than 3 hours,
  citing the NEC Handbook (Jan 2001).
  - **48 A kiln: 48 × 1.25 = 60 A, so a 60 A breaker with 6 AWG copper.**
  - 60 A kiln: 75 A, so an 80 A breaker.
  - L&L says a 50 A breaker on a 48 A kiln tends to nuisance-trip.
  - Kilns up to 48 A use a 50 A cord (NEMA 6-50P) built to carry at least 60 A. Above 48 A, hardwire
    the kiln. L&L says hardwiring a 48 A kiln to a 60 A breaker does not affect the warranty.
- **L&L breaker-to-copper-wire table** (75 °C copper, short runs) [S25]:

  | Breaker (A) | 20 | 30 | 40 | 50 | 60 | 70 | 80 | 90 | 100 | 125 | 150 | 175 | 200 | 225 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | Copper wire | 12 AWG | 10 | 8 | 6 | 6 | 4 | 3 | 2 | 1 | 1/0 | 2/0 | 4/0 | 250 kcmil | 350 kcmil |

- L&L wire-size page [S26]: copper rated 75 °C (THW, THWN, SE, USE, XHHW). Minimums apply to runs
  up to about 25 ft. Upsize for voltage drop on longer runs. About 5 V drop is "probably
  acceptable". Copper only.
- **L&L nameplate** [S25]: model, serial number, voltage, phase, amperage, wattage and recommended
  maximum temperature. Nameplate voltages: 120, 208, 220, 220/110, 240, 380/220 and 480 V.
  - A 240 V kiln on 208 V gets roughly 25% less power. Derived check: (208/240)² = 0.751.
  - A 208 V kiln on 240 V burns out its elements quickly.
- **Skutt** [S27]: The listed wire size is based on the recommended breaker, not the kiln's amps.
  - Conductors are rated 75 °C, with no more than 3 current-carrying conductors and 30 °C ambient.
  - Use heavier gauge for each extra 50 ft (15 m) of run. Do not use aluminium. Local codes
    supersede Skutt.
  - Skutt's page shows no breaker sizes. Example nameplates: KM-1227 3-phase 240 V, 29.3 A,
    11 520 W, NEMA 15-50. KM-818-3 208 V, 24 A, 4990 W, NEMA 6-30.
- **Paragon** [S28]: Older A-82B3 model: 30 A, 7200 W, 40 A breaker, 8 AWG. PMT-10: 20 A, 20 A
  breaker, 12 AWG. Paragon advises against a GFCI on the kiln circuit.

---

## 4. Refractory and insulation thermal properties

k is the thermal conductivity at the stated **mean** temperature. Test methods: ASTM C182
(insulating firebrick), C201 (fibre), C417/C201 (castables). Values are typical, not specification
values.

### 4.1 Insulating firebrick (IFB)

**Morgan Thermal Ceramics JM series, metric (excerpt, from the 06:2011 JM data sheet [S29])**

| Grade | Classification temp (°C) | Density (kg/m³) | k at 400 °C | k at 600 °C | k at 800 °C | k at 1000 °C |
|---|---|---|---|---|---|---|
| JM 23 | 1260 | 480 | 0.12 | 0.14 | 0.17 | 0.19 |
| JM 26 | 1430 | 800 | 0.25 | 0.27 | 0.30 | 0.33 |
| JM 28 | 1540 | 890 | 0.30 | 0.32 | 0.34 | 0.36 |

k is in W/(m·K). Classification temperatures and densities are also in the 2025 JM data sheet
[S30], which adds JM 26HD at 920 kg/m³. Excerpt: check the column mapping, since the sheet also has
JM 30/32/33 columns.

**Morgan US K and TC grades (excerpt)**

| Grade | Use limit / class temp | Density | k at 500 °F (260 °C) | k at 1000 °F (538 °C) | k at 1500 °F (816 °C) | k at 2000 °F (1093 °C) | Source |
|---|---|---|---|---|---|---|---|
| K-23 | 1315 °C (2400 °F) class temp in the 2025 sheet. An older sheet says 2300 °F | 513 kg/m³ (32.0 pcf) | 0.90 | 1.18 (at 1004 °F) | 1.39 (at 1499 °F) | 1.67 (at 2012 °F) | [S31] |
| K-25 | 1370 °C (2500 °F) | 617 kg/m³ | not found | not found | not found | not found | [S31] |
| K-26 | 1430 °C (2600 °F) | 657 kg/m³ | not found | not found | not found | not found | [S31] |
| TC-26 | 2600 °F | not found | 1.6 | 1.9 | 2.2 | 2.6 | [S32] |
| JM-28 | 2800 °F | not found | 2.3 | 2.4 | 2.5 | 2.6 | [S32] |

k is in Btu·in/(h·ft²·°F). For JM-28, the metric JM sheet gives 0.30 W/(m·K) at 400 °C, which is
2.08 Btu·in/(h·ft²·°F). The two Morgan sheets differ slightly, so both are listed.

**BNZ Materials (Allied Mineral), via lookpolymers / MatWeb copies (excerpt, ASTM C182, [S33])**

| Grade | Density | k at 500 °F | k at 1000 °F | k at 1500 °F | k at 1999 °F |
|---|---|---|---|---|---|
| BNZ 23 (as "PA 23") | 0.705 g/cm³ (44 pcf). Armil lists BNZ 23HS at 42 pcf | 1.60 | 2.01 | 2.43 | 2.57 |
| BNZ 26 | 0.769 g/cm³ (48 pcf) | 1.60 | 1.87 | 2.22 | 2.57 |
| BNZ 26 HS | 0.913 g/cm³ | 1.87 | not found | not found | 2.78 |
| BNZ 28 | 0.881 g/cm³ (55 pcf) | 2.29 | 2.43 | 2.57 | 2.71 |

k is in Btu·in/(h·ft²·°F). The BNZ "PA 23" k values look high for a 23 grade, about twice Morgan
K-23. Do not use them for K-23 without checking.

**Allied / Harbison-Walker IFB:** HWI IFB data sheets not found.

**IFB specific heat:**

- Not found from Morgan or BNZ.
- One vendor's 26-class IFB (500 kg/m³, 1400 °C) gives 1.21 kJ/(kg·K) at 1000 °C [S34]. Unverified.

### 4.2 Dense firebrick

| Product | Class | Max service | Bulk density | k at 400 °F (205 °C) | k at 800 °F (425 °C) | k at 1200 °F (650 °C) | k at 1600 °F (870 °C) | k at 2000 °F (1095 °C) | Source |
|---|---|---|---|---|---|---|---|---|---|
| HWI KX-99 | super-duty fireclay, 42% Al₂O₃ | 3200 °F (Foundry Service) | 142 lb/ft³ (2.27 g/cm³). Foundry Service says 143 | 9.7 (1.40) | 9.8 | 10.0 | 10.3 | 10.7 (1.54) | [S35] excerpt |
| Allied super-duty | super-duty | – | 2.21–2.27 g/cm³ (138–142 lb/ft³) | not found | not found | not found | not found | not found | [S36] |
| Allied medium-duty | medium-duty, 32.9% Al₂O₃ | – | 2.07–2.13 g/cm³ (129–133 lb/ft³) | not found | not found | not found | not found | not found | [S36] |

k is in Btu·in/(h·ft²·°F), with W/(m·K) in brackets.

- Medium-duty k vs temperature: **not found** from a maker.
- Dense firebrick specific heat: **not found** from a maker.
- Generic reference value: fire-clay brick k = 1.4 W/(m·K) at 500 °C [S37]. That source gives
  no grade.

### 4.3 Ceramic fibre blanket

**Kaowool blanket, Morgan data sheet 5-14-205 (excerpt, ASTM C201, [S38])**

8 pcf: k = 0.44 at 500 °F, 0.87 at 1000 °F, 1.45 at 1500 °F and 2.09 at 2000 °F, in
Btu·in/(h·ft²·°F).

**Kaowool blanket, Foundry Service page (verified, [S39])**

Temperature rating 2300 °F (1260 °C). Continuous use limit 2000 °F (1093 °C). k in
Btu·in/(h·ft²·°F):

| Mean temp | 8 pcf (128 kg/m³) | 6 pcf (96 kg/m³) | 4 pcf (64 kg/m³) |
|---|---|---|---|
| 500 °F (260 °C) | 0.44 | 0.47 | 0.54 |
| 1000 °F (538 °C) | 0.87 | 1.01 | 1.29 |
| 1500 °F (816 °C) | 1.45 | 1.73 | 2.30 |
| 1800 °F (982 °C)* | 1.83 | 2.19 | 2.96 |

*The page prints "1800 ºF (837 ºC)". 837 °C is a typo for 982 °C.

Disagreements:

- MatWeb (Thermal Ceramics, "not recently verified") gives 8 pcf 0.416/0.833/1.46/1.80 and 6 pcf
  0.486/1.04/1.74 at 500/1000/1500/1800 °F [S40].
- Foundry Service's Cerablanket page gives 2.05 (8 pcf) and 2.45 (6 pcf) at 1800 °F, and
  1.06 (6 pcf) at 1000 °F [S39].

**Cerachem blanket, Morgan data sheet BL.03, 1 January 2025 (verified, read in the PDF, [S101])**

Alumina-silica-zirconia (ZrO₂ 13–17 %). Classification temperature 1430 °C (2600 °F); continuous
use temperature 1315 °C (2400 °F). Densities 64, 96, 128 and 160 kg/m³ (4, 6, 8, 10 pcf). k by
ASTM C201, W/(m·K):

| Mean temp | 6 pcf (96 kg/m³) | 8 pcf (128 kg/m³) |
|---|---|---|
| 200 °C | 0.07 | 0.05 |
| 400 °C | 0.10 | 0.08 |
| 600 °C | 0.16 | 0.14 |
| 800 °C | 0.24 | 0.19 |
| 1000 °C | 0.36 | 0.27 |
| 1200 °C | 0.51 | 0.36 |

The same sheet gives Cerablanket (alumina-silica): classification 1260 °C (2300 °F), continuous use
1180 °C (2150 °F); 8 pcf 0.05/0.08/0.13/0.19/0.27 W/(m·K) at 200–1000 °C. Olsen's hot face for
fibre above 2200 °F is 2600 °F, 8 lb blanket (4th ed. p.64–65), which is a Cerachem-class blanket.

**Cerawool blanket, Morgan (excerpt, ASTM C201, [S41])**

| Density | k at 400 °C | k at 600 °C | k at 800 °C | k at 1000 °C |
|---|---|---|---|---|
| 96 kg/m³ | 0.08 | 0.12 | 0.18 | 0.26 |
| 128 kg/m³ | 0.07 | 0.11 | 0.17 | 0.25 |

k is in W/(m·K).

**Fibre specific heat (distributor listings, unverified)**

- Kaowool: 0.27 Btu/(lb·°F), which is 1.13 kJ/(kg·K) [S42].
- Cerablanket: a listing gives "1.13 Btu/lb-F". This is almost certainly 1.13 kJ/(kg·K) mislabelled
  [S42].

### 4.4 Ceramic fibre board

- Morgan Kaowool board data sheets exist [S43]. The excerpt shows a 260 kg/m³ (16 pcf) board with
  k about 0.16–0.23 W/(m·K) at 1000 °C, but the product column was not legible. **Full k vs
  temperature: not found.**
- Kaowool 1401 millboard: 35–40 pcf, k 0.61–1.33 Btu·in/(h·ft²·°F) over its range (distributor
  figure) [S43].

### 4.5 Castables

| Product | Max service | Density | k at 400 °F | k at 800 °F | k at 1200 °F | k at 1600 °F | k at 2000 °F | Source |
|---|---|---|---|---|---|---|---|---|
| Kast-O-Lite 26 LI Plus (HWI, sheet 1/09) | 2600 °F (1427 °C) | 90–100 lb/ft³ dried at 220 °F. 86–96 lb/ft³ fired at 1500 °F. 86 lb/ft³ needed to place | 3.6 (0.52) | 3.4 (0.49) | 3.5 (0.50) | 3.7 (0.53) | 4.0 (0.58) | [S44] excerpt |
| Kast-O-Lite 30 LI (HWI, sheet 3/06) | 3000 °F (1649 °C) | 95 lb/ft³ dried | 6.1 (0.88) | not found | not found | not found | not found | [S45] excerpt |
| Kast-O-Lite 30 LI Plus (HWI, sheet 10/19) | 3000 °F | 98 lb/ft³ dried. 92 lb/ft³ needed | 5.6 (0.81) | not found | not found | not found | not found | [S45] excerpt. A reseller gives 4.54 at 2000 °F (unverified) |
| Mizzou Castable Plus (HWI, sheet 1/05) | 3000 °F | 145 lb/ft³ dried. 141 lb/ft³ at 1500 °F. The 12/12 sheet says 142 and 140 | 7.8 (1.12) | not found | not found | not found | 7.4 (1.07) at 2400 °F | [S46] excerpt |

k is in Btu·in/(h·ft²·°F), with W/(m·K) in brackets.

- Foundry Service gives 78–88 lb/ft³ at 1500 °F for the Kast-O-Lite 26 line [S47].
- **Greenlite-30:** no product by this exact name found. HWI makes Greenlite 45-L (2500 °F,
  77 lb/ft³, k 4.6 Btu·in/(h·ft²·°F) at 400 °F) [S48].

### 4.6 Back-up insulation

**Calcium silicate, Promat PROMASIL-1100 (excerpt, [S49])**

- 285 kg/m³. Specific heat 1.05 kJ/(kg·K).
- k = 0.085 at 200 °C, 0.105 at 400 °C, 0.145 at 600 °C and 0.185 at 800 °C, in W/(m·K).
- Classification temperature: 1100 °C in one copy and 1050 °C in the US copy. Check this.

**Calcium silicate, BNZ ZelieBlok 2000S (excerpt, [S50])**

- Max 1100 °C. About 245 kg/m³.
- k = 0.08 at 200 °C, 0.10 at 400 °C and 0.12 at 600 °C, in W/(m·K).

**Mineral wool, ROCKWOOL ProRox (excerpt, [S51])**

All rated 1200 °F hot face. k in Btu·in/(h·ft²·°F).

| Product | Actual density | k at 75 °F | k at 100 °F | k at 200 °F | k at 300 °F | k at 400 °F | k at 600 °F |
|---|---|---|---|---|---|---|---|
| SL 560 | 8.6 lb/ft³ | – | 0.27 | 0.29 | – | 0.40 | 0.52 |
| SL 460 | 6.5 lb/ft³ | – | – | 0.30 | – | 0.38 | 0.55 |
| SL 760 | 3.0 lb/ft³ | 0.24 | – | 0.31 | 0.35 | – | – |

### 4.7 Steel shell emissivity

CIBSE Guide Table C3.7, via IES-VE (verified [S52]). These are normal emissivities, with no
temperature given.

| Surface | ε |
|---|---|
| Steel, oxidised | 0.79 |
| Steel, rough plate | 0.9 |
| Steel, rolled sheet | 0.6 |
| Steel, polished | 0.08 |
| Paint (unspecified) | 0.95 |
| Brick | 0.93 |

- Engineering ToolBox gives black enamel paint 0.80 and aluminium paint 0.27–0.67 [S53].
- Painted mild steel as one combined figure: not found. Use the paint value, since the coating
  governs.

---

## 5. Standard US brick sizes (9-inch series)

**Straights and splits (Larkin Refractory, verified [S54])**

- Straight: 9 × 4½ × 2½ in. This is one "brick equivalent". The 3 in series is 9 × 4½ × 3 in.
- Soap: 9 × 2¼ × 2½ in (or × 3 in).
- Splits: 9 × 4½ × 1, 1¼, 1½ or 2 in.

**Arches** taper across the 2½ in thickness, along the 4½ in face (sprung roofs) [S54]. The
2½ in figures are confirmed by SSFBS [S55] and Armadillo Clay [S56].

| Shape | Size (in) |
|---|---|
| No. 1 arch | 9 × 4½ × 2½ → 2⅛ |
| No. 2 arch | 9 × 4½ × 2½ → 1¾ |
| No. 3 arch | 9 × 4½ × 2½ → 1 |
| No. 1 arch, 3 in series | 9 × 4½ × 3 → 2¾ |
| No. 2 arch, 3 in series | 9 × 4½ × 3 → 2½ |
| No. 3 arch, 3 in series | 9 × 4½ × 3 → 2 |
| No. 4 arch, 3 in series | 9 × 4½ × 3 → 1 |

**Wedges** taper along the 9 in length, for 9 in thick arches [S54].

| Shape | Size (in) |
|---|---|
| No. 1-X wedge | 9 × 4½ × 2½ → 2¼ |
| No. 1 wedge | 9 × 4½ × 2½ → 1⅞ |
| No. 2 wedge | 9 × 4½ × 2½ → 1½ |
| No. 1 wedge, 3 in series | 9 × 4½ × 3 → 2¾ |
| No. 2 wedge, 3 in series | 9 × 4½ × 3 → 2½ |
| No. 3 wedge, 3 in series | 9 × 4½ × 3 → 2 |

Bailey sells a "#1 arch" in the 3 in series as 9 × 4.5 × 3 → 2.73 in [S57]. Larkin gives 2¾.

**Not found:**

- Key and skew dimensions. Larkin names keys and side/end skews but gives no sizes [S54].
- Inside ring diameters per shape. Compute them from the geometry.
- ASTM C909 (modular series) and ASTM C861 (metric dimensions of the standard series) are the
  standards for these shapes [S58]. Their tables were not read (paywalled or garbled).

---

## 6. Heat-loss method

### 6.1 ASTM C680

From the ASTM and ANSI abstracts [S59]:

- C680 gives algorithms for heat loss or gain and surface temperatures of insulation systems.
- It covers one-dimensional, steady or quasi-steady heat transfer, in rectangular, cylindrical or
  spherical geometry.
- Layers are homogeneous and uniformly dimensioned. k may vary with temperature, and C680 handles
  k(T).
- The surface coefficient combines convection and radiation, and the method iterates on the
  surface temperature.
- **Which convection correlations the current C680 edition uses: not verified (paywalled).** The
  standard correlations below are the usual choice.

### 6.2 Natural-convection correlations

Vertical plate, Churchill and Chu (1975). Verified from a course note [S60], and the same in
EngineersEdge [S61]:

- All Ra, 10⁻¹ < Ra_L ≤ 10¹²:
  Nu_L = { 0.825 + 0.387·Ra_L^(1/6) / [1 + (0.492/Pr)^(9/16)]^(8/27) }²
- Laminar only, 10⁻¹ < Ra_L ≤ 10⁹:
  Nu_L = 0.68 + 0.670·Ra_L^(1/4) / [1 + (0.492/Pr)^(9/16)]^(4/9)

Horizontal plate, characteristic length L = A/P (area / perimeter), after Lloyd and Moran
(excerpt [S62]):

| Case | Ra range | Correlation |
|---|---|---|
| Hot surface facing up (or cold facing down) | 10⁴ – 10⁷ | Nu = 0.54·Ra^(1/4) |
| Hot surface facing up (or cold facing down) | 10⁷ – 10¹¹ | Nu = 0.15·Ra^(1/3) |
| Hot surface facing down (or cold facing up) | 10⁵ – 10¹¹ (as given) | Nu = 0.27·Ra^(1/4) |

The laminar/turbulent switch point varies by source: 10⁷, 8×10⁶ or 10⁶ [S62]. Some texts use
Nu = 0.52·Ra^(1/5) for the hot-facing-down case. **No source was found for it here.**

Definitions:

- Ra_L = g·β·(T_s − T_∞)·L³ / (ν·α), with β = 1/T_film (ideal gas, T in K).
- Evaluate the air properties at the film temperature T_film = (T_s + T_∞)/2.
- h = Nu·k/L.
- Radiation: h_r = ε·σ·(T_s² + T_∞²)(T_s + T_∞), with σ = 5.670374×10⁻⁸ W/(m²·K⁴).

### 6.3 Air properties at 1 atm

Neutrium tabulation (verified [S63]). Neutrium does not name its underlying data source.

| T (K) | ρ (kg/m³) | c_p (J/(kg·K)) | k (W/(m·K)) | μ (kg/(m·s)) |
|---|---|---|---|---|
| 250 | 1.413 | 1003 | 0.0223 | 1.610e-5 |
| 300 | 1.177 | 1005 | 0.0261 | 1.850e-5 |
| 400 | 0.883 | 1013 | 0.0331 | 2.290e-5 |
| 500 | 0.706 | 1029 | 0.0395 | 2.680e-5 |
| 600 | 0.589 | 1051 | 0.0456 | 3.030e-5 |
| 700 | 0.504 | 1075 | 0.0513 | 3.350e-5 |
| 800 | 0.441 | 1099 | 0.0569 | 3.640e-5 |
| 900 | 0.392 | 1120 | 0.0625 | 3.920e-5 |
| 1000 | 0.353 | 1141 | 0.0672 | 4.180e-5 |

Derived quantities:

- ν = μ/ρ. For example, ν = 1.572e-5 m²/s at 300 K.
- Pr = c_p·μ/k. For example, Pr = 0.712 at 300 K.
- These are Holman's values (*Heat Transfer*, Table A-5), not Incropera's (Table A.4), as the
  science review of 2026-10-28 found: Neutrium's 1.177 kg/m³ at 300 K is Holman's 1.1774, where
  Incropera gives 1.1614. The review puts the difference at under 2 % in h_c. Neither book was
  read here. (This corrects an earlier note that they matched Incropera.)
- Cross-checked 2026-10-24 against Çengel Table A-9 [S84]: k and μ agree within about 1–2 % at every row, and Çengel's density (1.176 kg/m³ at 27 °C) matches the ideal-gas value p/(R·T) = 1.1766.

### 6.4 Worked multi-layer wall examples (validation tests)

**Test A: furnace wall with film coefficients**

Source: FOSSEE textbook companion, *Basic Mechanical Engineering*, Example 6.11, p. 232
(verified [S64]).

Inputs:

- Fire brick: 0.2 m thick, k = 4.0 W/(m·°C).
- Common brick: 0.2 m thick, k = 0.65 W/(m·°C).
- Hot gas at 1400 °C. Inside h = 16.5 (convection) + 17.5 (radiation) = 34 W/(m²·°C).
- Outside air at 50 °C. Outside h = 12.5 + 6.5 = 19 W/(m²·°C).

Published results:

- Heat loss: **3.07 kW/m²**
- Fire brick inner face: **1309.705 °C**
- Fire brick / common brick interface: **1156.204 °C**

Derived check:

- ΣR = 1/34 + 0.2/4 + 0.2/0.65 + 1/19 = 0.43974 m²·K/W
- q = 1350/0.43974 = 3070 W/m² ✓

**Test B: same source, Example 6.5, p. 226 (verified [S64])**

Inputs:

- Brick: 0.225 m, k = 4.984 kJ/(h·m·°C).
- Insulating brick: 0.125 m, k = 0.623 kJ/(h·m·°C).
- Gas at 1650 °C, with h_i = 245.28 kJ/(h·m²·°C).
- Ambient at 27 °C, with h_o = 40.88 kJ/(h·m²·°C).

Published results:

- Heat loss: **5916.3 kJ/(h·m²)**, which is 1643.4 W/m² (derived)
- Inner surface: **1625.88 °C**
- Outer surface: **171.72 °C**

**Test C: three layers, fixed surface temperatures**

Source: CSJM University lecture notes, CHE S204 ch. 2 (excerpt [S65]).

Inputs:

- Fire brick: 22 cm, k = 1.0 W/(m·°C).
- Insulating brick: 7.5 cm, k = 0.12 W/(m·°C).
- Red brick: 11 cm, k = 0.75 W/(m·°C).
- Inner face 870 °C. Outer face 40 °C.

The source gives R = 0.22, 0.625 and 0.147 m²·°C/W per layer, a total of about 0.992. It cuts off
before the final answer.

Derived results:

- q = 830/0.99167 = **837.0 W/m²**
- Interface temperatures: **685.9 °C** and **162.8 °C**

A **kiln-specific** published multi-layer example (IFB plus fibre plus steel, with numbers): **not
found**. 3E Plus (NAIMA) runs C680, but its outputs are not published as worked examples.

### 6.5 Transient conduction solutions (for validating the finite-volume solver)

**Semi-infinite solid, step change in surface temperature**

At t = 0 the surface steps from T_i to T_s. Source: LearnChemE [S66] and a Holman-based note
[S67] (verified).

- Temperature: (T(x,t) − T_s) / (T_i − T_s) = erf( x / (2·√(α·t)) )
- Surface heat flux: q″_s(t) = k·(T_s − T_i) / √(π·α·t)
- Reference values (mathematical constants): erf(0.5) = 0.520500, erf(1.0) = 0.842701,
  erf(1.5) = 0.966105, erf(2.0) = 0.995322.

**Slab, step change in surface temperature on both faces**

Thickness 2L, initial temperature T_i, both faces stepped to T_s. This is the standard Fourier
series result (Carslaw and Jaeger, *Conduction of Heat in Solids*, §3.3). It was **not
re-verified online here**.

- θ* = (T − T_s)/(T_i − T_s) = Σ_{n=0}^{∞} [4·(−1)ⁿ / ((2n+1)·π)] · cos((2n+1)·π·x/(2L)) · exp(−(2n+1)²·π²·Fo/4)
- Fo = α·t/L². x is measured from the mid-plane.

**Slab with convection, one-term form**

θ* ≈ C₁·exp(−ζ₁²·Fo)·cos(ζ₁·x/L), where:

- ζ₁·tan ζ₁ = Bi
- C₁ = 4·sin ζ₁ / (2ζ₁ + sin 2ζ₁)

This is from a secondary source [S68]. The form is standard (Incropera ch. 5).

---

## 7. Energy rules of thumb for studio electric kilns

**L&L method (verified [S69])**

- Split the firing into equal time blocks: 3 blocks for low fire, 4 for high fire.
- The blocks draw 25%, 50%, 75% (and 100% for high fire) of rated kW.
- Example: E23T, 11.52 kW, 12 h cone 6 firing = **86.4 kWh**. That is 11.52 × 3 × 2.5. At
  $0.09/kWh it costs about $7.78.

**Skutt method (verified [S70])**

- Cost = kW × hours × $/kWh × adjustment factor. Skutt says 0.5 is a good estimate across its
  ConeFire programs.
- Example: KM1231PK (208 V, 1 phase, 16.64 kW), medium-speed cone 6, 100 lb load:
  16.64 × 8.47 × 0.12 × 0.5 = $8.45. That is **70.5 kWh** (derived).
- A KM-818 fired to cone 06 cost $2.83. The inputs were not stated.

**Lakeside Pottery duty cycles (secondary [S71])**

- About 50% for cone 04/06 bisque, about 65% for cone 6 glaze and about 15% for preheating.
- Example: 11.52 kW kiln at $0.18/kWh. Candling $2.18, bisque $12.35, glaze $13.48.

**Wattage per cubic foot**

- No kiln-maker figure found. Forum claims (unverified) say a "true cone 10" needs at least
  1800–2000 W/ft³ [S72].
- One poster suggests about 3.5 W per in² of external shell area for cone 10, about 3 for cone 8 and
  2.5–3 for cone 6 [S72].

Derived from retailer specs (Easy-Fire 240 V 1-phase, Skutt KM-series):

| Kiln | Rating | Volume | W/ft³ | Source |
|---|---|---|---|---|
| L&L E23T-3 | 11 520 W, 48 A, cone 10 | 6.7 ft³ | ≈ 1720 | [S73] |
| Skutt KM-1027 | 11 520 W, 48 A, cone 10 | about 7 ft³ | ≈ 1650 | [S74] |
| Skutt KM-818 | 6660 W, 27.8 A, cone 10 | about 2.6 ft³ | ≈ 2560 | [S74] |

Small kilns need more W/ft³, because the wall area per unit volume is larger.

---

## 8. Orton cone temperature equivalents

See also `cones.md` (2026-10-24): PCE cones 15 to 42 from ASTM C24 Table X1.1, and a re-check
of this table against Orton's own °F chart.

Values are in °C. "SSB" means self-supporting regular cones and "LRB" means large regular cones.
The rates are the heating rate over the last 100 °C or so of the firing.

Source: the Wikipedia table [S75], which reproduces Orton's 2016 chart. It was read from the page
wikitext, so the column order is SSB 15/60/150, SSK 15/60/150, LRB 60/150.

Spot checks against Orton itself:

- Orton's Cone 10 self-supporting product page: 1251/1285/1305 °C ✓ [S76].
- Orton FAQ: SS cone 06 fast = 1855 °F (1013 °C ✓). Large cone 06 fast = 1852 °F (1011 °C ✓) [S77].

The °F values are derived as °C × 9/5 + 32. Orton's own °F chart [S78] (PDF, not opened) may differ
by ±1 °F from rounding.

| Cone | SSB 60 °C/h (108 °F/h) | SSB 150 °C/h (270 °F/h) | LRB 60 °C/h | LRB 150 °C/h | SSB 15 °C/h (27 °F/h) |
|---|---|---|---|---|---|
| 022 | 586 | 590 | – | – | – |
| 021 | 600 | 617 | – | – | – |
| 020 | 626 | 638 | – | – | – |
| 019 | 678 | 695 | 676 | 693 | 656 |
| 018 | 715 | 734 | 712 | 732 | 686 |
| 017 | 738 | 763 | 736 | 761 | 705 |
| 016 | 772 | 796 | 769 | 794 | 742 |
| 015 | 791 | 818 | 788 | 816 | 750 |
| 014 | 807 | 838 | 807 | 836 | 757 |
| 013 | 837 | 861 | 837 | 859 | 807 |
| 012 | 861 | 882 | 858 | 880 | 843 |
| 011 | 875 | 894 | 873 | 892 | 857 |
| 010 | 903 | 915 | 898 | 913 | 891 |
| 09 | 920 | 930 | 917 | 928 | 907 |
| 08 | 942 | 956 | 942 | 954 | 922 |
| 07 | 976 | 987 | 973 | 985 | 962 |
| 06 | 998 | 1013 | 995 | 1011 | 981 |
| 05½ | 1015 | 1025 | 1012 | 1023 | 1004 |
| 05 | 1031 | 1044 | 1030 | 1046 | 1021 |
| 04 | 1063 | 1077 | 1060 | 1070 | 1046 |
| 03 | 1086 | 1104 | 1086 | 1101 | 1071 |
| 02 | 1102 | 1122 | 1101 | 1120 | 1078 |
| 01 | 1119 | 1138 | 1117 | 1137 | 1093 |
| 1 | 1137 | 1154 | 1136 | 1154 | 1109 |
| 2 | 1142 | 1164 | 1142 | 1162 | 1112 |
| 3 | 1152 | 1170 | 1152 | 1168 | 1115 |
| 4 | 1162 | 1183 | 1160 | 1181 | 1141 |
| 5 | 1186 | 1207 | 1184 | 1205 | 1159 |
| 5½ | 1203 | 1225 | – | – | 1167 |
| 6 | 1222 | 1243 | 1220 | 1241 | 1185 |
| 7 | 1239 | 1257 | 1237 | 1255 | 1201 |
| 8 | 1249 | 1271 | 1247 | 1269 | 1211 |
| 9 | 1260 | 1280 | 1257 | 1278 | 1224 |
| 10 | 1285 | 1305 | 1282 | 1303 | 1251 |
| 11 | 1294 | 1315 | 1293 | 1312 | 1272 |
| 12 | 1306 | 1326 | 1304 | 1324 | 1285 |
| 13 | 1331 | 1348 | 1321 | 1346 | 1310 |
| 14 | 1365 | 1384 | 1388 ⚠ | 1366 ⚠ | 1351 |

Rows to check against Orton's own chart:

- **Cone 14 LRB:** the source has 1388 at 60 °C/h and 1366 at 150 °C/h, which is reversed. The
  value at 60 °C/h should be the lower one. The values are probably swapped.
- **Cone 05 LRB 150 (1046) and cone 04 LRB 150 (1070):** these break the usual pattern
  (LRB 150 is about SSB 150 − 2). Check them against the Orton chart.

Other notes:

- Orton defines heating rate as the temperature rise per hour [S77]. The "last 100 °C" convention
  is how the chart is usually read [S75]. It was not confirmed on the Orton page itself.
- **Orton terms:** the Orton site carries "© 2021-2023 The Edward Orton Jr. Ceramic Foundation.
  All rights reserved." [S77]. **No specific licence or terms for reproducing the chart were
  found.** The plan already flags this (02-plan.md, open question 2). Ask Orton before shipping the
  table in code. Temperature equivalents are factual data, but the chart layout is copyrighted.

---

## Corroboration (2026-10-24)

The goal is at least three independent sources per item. Resellers and distributors that copy a
maker's sheet (Foundry Service, SSFBS, Clay-Planet, Distribution International, lookpolymers,
MatWeb, Krueger listings) are **not** independent of that maker. Kanthal pages [S1–S6, S9, S13,
S14, S16] count as one source (one maker). Morgan JM, K, TJM and Kaowool/Cerawool sheets count as
one maker. §8 (cones) is out of scope here.

| Item (section) | Independent sources | Agreement | Discrepancy / note |
|---|---|---|---|
| FeCrAl A-1 class ρ20 1.45, density 7.10, melt 1500 (§1.1) | 3: Kanthal [S1], Aperam [S79], GB/T suppliers [S8] (weak) | ρ and density agree exactly | Aperam max temp 1300 °C vs Kanthal A-1 1400 °C. That is a grade difference, not an error |
| FeCrAl max temp 1400 °C (A-1) (§1.1, §1.4) | **only 1** (Kanthal). Others give 1300 [S79], 1200 [S80] for their own grades | — | Engine `alloys.yaml` A-1 1400 °C depends on Kanthal alone. That is right for genuine A-1 wire, but not for generic FeCrAl |
| Kanthal D density 7.25 (§1.1) | 2: Kanthal [S4], JLC FeCrAl 135 7.25 [S80] | agree | short by one |
| NiCr 80/20 ρ20 1.09 (§1.1) | 3: Kanthal [S5], NiWire 1.09 [S81], JLC 1.08 [S82] | agree within 1% | — |
| NiCr 80/20 density 8.30 (§1.1) | 4 | **disagree** | Kanthal 8.30 vs NiWire 8.40, JLC 8.41, Omega 8.41 [S81–S83]. About 1.3%. It affects wire mass only (`alloys.yaml` Nikrothal 80), not resistance |
| NiCr 80/20 max temp 1200 (§1.1) | 4 | mostly | Kanthal, NiWire and JLC give 1200. Omega gives 1150 (2100 °F) [S83] |
| NiCr melting 1400 (§1.1) | 3: Kanthal, NiWire, Omega [S81, S83] | agree | — |
| Emissivity 0.70 / 0.88 of oxidized wire (§1.1) | **only 1** (Kanthal) | — | not found elsewhere |
| Ct tables (§1.2) | 2 makers for derived end points: Aperam [S79], JLC [S82] give mean TCR only | A-1 Ct(1000) 1.032 vs 1.04; NiCr 1.059 vs 1.05 | Full tables are Kanthal only. **Only 1 source for the row-by-row values.** The others are mean coefficients, so the shape (e.g. Nikrothal's 500 °C peak) is not corroborated |
| Atmosphere limits (§1.4, `hybrid.py`) | **only 1** (Kanthal [S9]). Aperam says pre-oxidise below 1000 °C for 7–8 h before reducing use and calls N₂, NH₃ and hydrocarbons harmful [S79] | qualitatively consistent with the Kanthal 7–10 h at 1050 °C | numbers single-source |
| FeCrAl better than NiCr in sulphur (§1.5) | 2: Kanthal [S6], Aperam [S79] | agree | short by one |
| Surface load 17.5 W/in² (2.71 W/cm²) for A-1 in grooves at ~2300 °F (§1.6, `electric.py` SURFACE_LOAD) | 2: Krueger [S15], Kanthal key data 3–4 W/cm² at 1000 °C for grooves [S14]. Forum "Brauer" figure 3.5 W/cm² below 900 °C, 1.5 W/cm² near 1350 °C [S86] (unverified). A patent cites 30.5 W/in² at ~1200 °C [S87] | loosely: Krueger's 2.71 W/cm² at 1260 °C sits below Kanthal's 3–4 at 1000 °C, as expected | **only 2 credible sources.** The patent's 30.5 W/in² (4.7 W/cm²) is far above the others. It is probably a different duty, but record it |
| On/off control −20%, D/d 5–12, pitch 2–4 d (§1.6) | **only 1** (Kanthal [S13], confirmed again [S86]) | — | — |
| Kanthal worked example (§1.7) | 1 (Kanthal), re-derived here | reproduces | a validation test, so a single source is acceptable |
| AWG formula and table (§2) | 3: ASTM B258 abstract [S18], Wikipedia [S19], and the closed-form formula re-computed | agree | — |
| NEC 125% continuous load, 3 h definition (§3, `electric.py`) | ≥4: EC&M [S20], Mike Holt [S21, S89], EC mag [S22], L&L [S25], solar-forum quotation of Art. 100 [S88] | agree | NEC text still not read first-hand |
| 48 A kiln → 60 A breaker, 6 AWG Cu (§3) | 3: L&L [S25], Austin Gallery table [S90], CAD forum installs [S24] | agree | One forum post reports a Paragon page saying 50 A for an older TnF-82 (unverified) |
| JM 23 / JM 26 / JM 28 k(T) (§4.1, `materials.yaml`, `ifb_conductivity.yaml`) | **only 1 maker** (Morgan, several sheets [S29–S32]). BNZ 23 [S91] is a different, denser product (593 kg/m³ vs 480) | — | BNZ 23: 0.14 W/(m·K) at 260 °C, 0.19 at 538, 0.23 at 816, 0.26 at 1093. Morgan K-23: 0.13 / 0.17 / 0.20 / 0.24 at about the same points. JM 23 0.12 at 400 °C vs BNZ 23 about 0.165 interpolated. Not a contradiction (different grade), but no second maker confirms JM 23 |
| BNZ "PA 23" vs K-23 (§4.1) | — | — | Already flagged. BNZ 23 at 0.14 W/(m·K) (0.97 Btu) at 500 °F [S91] contradicts the lookpolymers "PA 23" 1.60 at 500 °F, which supports the suspicion that "PA 23" is mislabelled |
| KX-99 dense brick k (§4.2, `materials.yaml`) | **only 1** (HWI; Foundry Service and SSFBS are resellers) | — | Generic fire-clay 1.4 W/(m·K) at 500 °C [S37] is close to KX-99 1.40–1.54. A Plibrico fireclay sheet gives 8.2 at 400 °F to 9.5 at 2000 °F Btu·in [S92] (a lower-alumina product, about 10% lower) |
| Kaowool 8 pcf k(T) (§4.3, `materials.yaml`) | 3 for "1260 °C blanket, 128 kg/m³": Morgan Kaowool [S38/S39], MatWeb copy (not independent), CNBM [S93], Morgan Cerawool [S41] (same maker) | **disagree at high T** | At ~1000 °C: Kaowool 0.26–0.30, Cerawool 0.25, CNBM 0.17 W/(m·K), and a supplier listing gives 0.20. The CNBM value is 35–45% lower than Morgan's. The engine uses Morgan's (the conservative choice for heat loss) |
| Fibre specific heat 1.13 kJ/(kg·K) (§4.3) | 2: Distribution International Kaowool [S42], Unifrax Durablanket S listing 0.27 Btu/(lb·°F) [S94] | agree | both are distributor listings |
| Kast-O-Lite 26, Mizzou (§4.5) | **only 1** (HWI). All other copies are resellers | — | — |
| PROMASIL calcium silicate (§4.6, `materials.yaml`) | 2: Promat [S49], BNZ ZelieBlok [S50] (a comparable product) | similar: 0.085 vs 0.08 at 200, 0.105 vs 0.10 at 400, 0.145 vs 0.12 at 600 °C | Within 17% at 600 °C. Short by one |
| Mineral wool (§4.6) | 1 (ROCKWOOL) | — | — |
| Oxidized steel ε 0.79 (§4.7, `heatloss.py`) | 2: CIBSE via IES-VE [S52], Engineering ToolBox [S53]. EngineersEdge/Optris tables [S95] list wide ranges | agree on 0.79 | CIBSE values are normal emissivity, and ToolBox values are at 300 K. Hemispherical ε at shell temperature can differ. Brick: CIBSE 0.93 vs ToolBox fire-clay 0.75 |
| Brick sizes 9 × 4½ × 2½ (§5, `masonry.py`) | ≥3: Larkin [S54], SSFBS [S55], Armadillo [S56], Bailey [S57], HWI Greentherm listings [S96] | agree | — |
| Arch/wedge tapers (§5, `masonry.py` ARCH) | 2: Larkin [S54], Bailey [S57] (#1 arch 3 in: 2.73 vs 2¾). Forum confirms #2 arch 2½ → 1¾ [S97] | agree | ASTM C909 table still not read. **Short.** Wedge tapers rest on Larkin alone |
| ASTM C680 scope (§6.1) | 2: ASTM and ANSI abstracts (same document) | — | **only 1 effective source** |
| Churchill–Chu vertical plate (§6.2) | ≥3: ULA notes [S60], EngineersEdge [S61], Caleb Bell `ht` library citing Churchill & Chu 1975 and Incropera 6th ed. [S98], Maya HTT [S99] | agree | — |
| Horizontal plate 0.54/0.15/0.27 (§6.2) | 2: Maya HTT/Lloyd–Moran [S62], COMSOL [S62]. The `ht` library [S98] lists McAdams/VDI/Rohsenow alternatives, which differ | partial | **Short of 3 independent sources quoting the same constants.** `ht` shows McAdams vs VDI vs Rohsenow differ by up to ±15% (hot side) and ±50% (cold side) for one test case |
| Air properties (§6.3, `thermal/air.py`) | 3: Neutrium [S63], Çengel [S84], Incropera [S85] | k, μ, c_p within ~1–2% | Incropera ρ(300 K) 1.1614 vs Neutrium 1.177 (1.3%). Neutrium matches ideal gas, so no change is needed |
| Worked wall examples (§6.4) | single-source validation cases, re-derived | reproduce | acceptable as tests |
| erf, semi-infinite and slab solutions (§6.5) | mathematical. [S66], [S67], Carslaw & Jaeger | agree | — |
| Energy rules of thumb (§7, `electric.py` W/ft³) | L&L [S69], Skutt [S70], Lakeside [S71] are 3 independent methods. W/ft³ derived from 2 makers [S73, S74] | methods differ: L&L about 62.5% of kW×h for high fire, Skutt 50% | W/ft³ is **2 makers plus forum**. No maker publishes a W/ft³ rule |

Summary: at ≥3 independent sources are AWG, NEC 125%/3 h, the 48 A → 60 A example, NiCr ρ and
melting point, FeCrAl A-1-class ρ and density, standard straight brick size, Churchill–Chu, air
properties, the transient solutions and the energy methods. Single-maker items that **cannot reach
three by nature** (proprietary product data): all Kanthal-specific figures (Ct rows, atmosphere
table, element key data, emissivity), Morgan JM/K IFB, HWI KX-99, Kast-O-Lite and Mizzou. For these
the second and third sources can only be the same maker's other sheets, or comparable products,
which are listed above.

## Gaps (not found)

- Kanthal maximum surface load vs furnace temperature diagrams, as numbers. Kanthal gives only the
  1000 °C values, in §1.6.
- Kanthal η (area / cold resistance) tables. Full inputs and outputs of the appliance examples.
- Kanthal or kiln-maker guidance for elements in gas/electric hybrid kilns.
- The NEC text, read first-hand.
- K-25 and K-26 k values. Allied and HWI IFB data sheets. Medium-duty dense brick k(T). Dense and
  IFB specific heat from a maker.
- Ceramic fibre board k(T). Greenlite-30.
- Key and skew brick dimensions.
- The convection correlations inside the current ASTM C680 edition. A kiln-specific published
  multi-layer example.
- A kiln-maker W/ft³ by cone figure.
- Orton reproduction terms.

---

## Sources

- [S1] Kanthal A-1 data sheet. https://www.kanthal.com/en/products/material-datasheets/wire/resistance-heating-wire-and-resistance-wire/kanthal-a-1/
- [S2] Kanthal APM data sheet. https://www.kanthal.com/en/products/material-datasheets/wire/resistance-heating-wire-and-resistance-wire/kanthal-apm/
- [S3] Kanthal AF data sheet. https://www.kanthal.com/en/products/material-datasheets/wire/resistance-heating-wire-and-resistance-wire/kanthal-af/
- [S4] Kanthal D data sheet. https://www.kanthal.com/en/products/material-datasheets/wire/resistance-heating-wire-and-resistance-wire/kanthal-d/
- [S5] Nikrothal 80 data sheet. https://www.kanthal.com/en/products/material-datasheets/wire/resistance-heating-wire-and-resistance-wire/nikrothal-80/
- [S6] Kanthal, Ferritic alloys. https://www.kanthal.com/en/knowledge-hub/heating-material-knowledge/resistance-heating-alloys/ferritic-alloys/
- [S7] Total Materia, GB 0Cr21Al6 (GB/T 1234). https://www.totalmateria.com/en-us/material/1408980
- [S8] Supplier listings (Xi'an Qianfeng and others), unverified. https://www.ec21.com/ec-market/co-qianfengtech/surface-resistivity.html ; https://www.goldsupplier.com/provide/p173197489.html
- [S9] Kanthal, Furnace-specific factors. https://www.kanthal.com/en/knowledge-hub/heating-material-knowledge/design-factors/furnace-specific-factors/
- [S10] Potterycrafts, Kiln and firing advice. https://www.potterycrafts.co.uk/kilnadvice
- [S11] Ceramic Arts Daily forum, Reduction firing in electric kiln. https://community.ceramicartsdaily.org/topic/3728-reduction-firing-in-electric-kiln
- [S12] US Patent 4,215,265, Method and apparatus for producing ceramic ware. https://patents.google.com/patent/US4215265
- [S13] Kanthal, Design calculations for heating elements. https://www.kanthal.com/en/knowledge-hub/heating-material-knowledge/design-calculations-for-heating-elements/
- [S14] Kanthal, Key data for Kanthal elements. https://www.kanthal.com/en/knowledge-hub/heating-material-knowledge/key-data-for-kanthal-elements/
- [S15] Krueger Pottery, 240 V 24 A element. https://kruegerpottery.com/products/element_240v_24amp
- [S16] Kanthal, Calculations of wire: examples (PDF). https://www.kanthal.com/contentassets/3720091e7e604cf89d4a289536f6b56b/design-calculations-of-wire-elements.pdf
- [S17] Kanthal, Appliance calculations: examples (PDF). https://www.kanthal.com/contentassets/70579d218872450dbf638848883078ff/design-calculations_examples.pdf
- [S18] ASTM B258 (abstract). https://store.astm.org/standards/b258
- [S19] Wikipedia, American wire gauge. https://en.wikipedia.org/wiki/American_wire_gauge
- [S20] EC&M, NEC: Branch-circuit overcurrent protection. https://www.ecmweb.com/nec/nec-branch-circuit-overcurrent-protection
- [S21] Mike Holt forum, Continuous load 125% 3-hour rule. https://forums.mikeholt.com/threads/continuous-load-125-3-hour-rule-80.2576877
- [S22] Electrical Contractor, Sizing conductors part XXXIX. https://www.ecmag.com/magazine/articles/article-detail/codes-standards-sizing-conductors-part-xxxix
- [S23] Mike Holt forum, NEC 422.10(A) and 422.11(E)(3). https://forums.mikeholt.com/threads/nec-422-10-a-422-11-e-3.96359/post-1537310
- [S24] Mike Holt forum, Kiln wiring. https://forums.mikeholt.com/goto/post?id=3042968 ; Ceramic Arts Daily, Circuit breaker size for kiln. https://community.ceramicartsdaily.org/topic/38275-circuit-breaker-size-for-kiln
- [S25] L&L Kiln, How to size the circuit breaker, fuses, cord. https://hotkilns.com/support/pottery-kiln-knowledgebase/electrical-how-size-circuit-breaker-fuses-cord
- [S26] L&L Kiln, What wire size is used to connect a kiln? https://hotkilns.com/support/pottery-kiln-knowledgebase/wire-size-used-connect-kiln
- [S27] Skutt, Electrical specifications. https://skutt.com/skutt-resources/resources-just-for-you/architectural-specifications/electrical-specifications/
- [S28] Paragon, PMT-10 and FAQ pages. https://www.paragonweb.com/PMT-10.cfm ; https://corp.paragonweb.com/faqs/should-you-include-a-gfci-on-the-kilns-electric-circuit/
- [S29] Morgan Thermal Ceramics, Insulating Firebricks JM, 06:2011 (PDF). http://www.aldero.com/files_prodotti/612/files/2253_TDS%20insulating%20firebricks%20jm%20ENG.pdf
- [S30] Morgan Thermal Ceramics, JM IFB series (2025, PDF). https://www.morganthermalceramics.com/media/5beap13n/jm-ifb-series_eng.pdf
- [S31] Morgan Thermal Ceramics, K IFB series (2025, PDF). https://www.morganthermalceramics.com/media/0wobjak3/k-ifb-series_eng.pdf ; older K-23 sheet: https://cdn.shopify.com/s/files/1/1023/7667/files/Morgan_Thermal_Ceramics_K-23_IFB.pdf
- [S32] Morgan Thermal Ceramics, IFB above 2600 °F: TC-26, JM-28, JM-30 (PDF). https://www.lynnmfg.com/wp-content/uploads/2015/11/199482_DATA-TC-114-2.pdf
- [S33] BNZ data sheets via lookpolymers and MatWeb. https://www.lookpolymers.com/pdf/BNZ-Materials-BNZ-26-Insulating-Firebrick.pdf ; https://www.lookpolymers.com/pdf/BNZ-Materials-BNZ-28-Insulating-Firebrick.pdf ; https://www.matweb.com/search/datasheet_print.aspx?matguid=df3655b657f34612ae9d7652f1d82c58 ; Armil CFS: https://armilcfs.com/wp-content/uploads/2015/07/ifb-BNZ.pdf
- [S34] Solargil, FB26 insulating firebrick. https://solargil.com/gb/materiels-refractaires/589-briques-legeres-isolantes-haute-qualite-1400c-26fb.html
- [S35] HWI KX-99 product data 6/12 (PDF). https://ssfbs.com/wp-content/uploads/2021/06/KX_99.pdf ; Foundry Service KX-99: https://www.foundryservice.com/product/hard-fire-bricks-high-density-super-duty/kx-99-high-fired-super-duty-fire-brick-3200of-42-alumina-hard-brick/
- [S36] Allied Mineral, Firebrick. https://alliedmineral.com/partnerships/thermal-integrated-materials/firebrick/
- [S37] Engineering ToolBox, Thermal conductivity. https://www.engineeringtoolbox.com/thermal-conductivity-d_429.html
- [S38] Morgan, Kaowool blankets 5-14-205 (PDF). https://www.morganthermalceramics.com/media/llhhadih/5-14-205_kaowoolblankets_072018.pdf
- [S39] Foundry Service, Kaowool blanket. https://www.foundryservice.com/product/kaowool-blanket-products-1800of-2600of-insulation-blankets/kaowool-blanket/ ; Cerablanket: https://www.foundryservice.com/product/kaowool-blanket-products-1800of-2600of-insulation-blankets/cerablanket/
- [S40] MatWeb, Thermal Ceramics Kaowool blanket. https://www.matweb.com/search/datasheet_print.aspx?matguid=cb830e74bc69422aa560a7b57494955a
- [S41] Morgan, Cerawool blanket (PDF). https://morganthermalceramics.com/media/3oipt3dt/cerawool-blanket_eng.pdf
- [S42] Distribution International, Kaowool and Cerablanket listings. https://shop.distributioninternational.com/refractories/ceramic-fiber/ceramic-fiber-blankets/cfbt80504kt ; https://shop.distributioninternational.com/refractories/ceramic-fiber/ceramic-fiber-blankets/cfbt82041cbt
- [S43] Morgan, Kaowool boards (PDF). https://www.morganthermalceramics.com/media/8981/kaowool-boards_americas-region_eng.pdf ; millboard listing: https://www.distributioninternational.com/refractories/ceramic-fiber/ceramic-fiber-board/cfbdm0855i
- [S44] HWI, Kast-O-Lite 26 LI Plus product data 1/09 (PDF). https://ssfbs.com/wp-content/uploads/2021/06/KAST-O-LITE_26_LI_PLUS.pdf
- [S45] HWI, Kast-O-Lite 30 LI 3/06 (PDF). http://shop.clay-planet.com/pdfs/kast-o-lite-30-li-plus-data.pdf ; 30 LI Plus 10/19: https://ssfbs.com/wp-content/uploads/2021/06/KAST-O-LITE_30_LI_PLUS.pdf
- [S46] HWI, Mizzou Castable / Plus (PDF). https://shop.clay-planet.com/pdfs/MIZZOU-CASTABLE.pdf ; https://ssfbs.com/wp-content/uploads/2021/06/MIZZOU_CASTABLE_PLUS.pdf
- [S47] Foundry Service, Kast-O-Lite 26. https://www.foundryservice.com/product/insulating-castables/kast-o-lite-26-insulating-castable-2600of/
- [S48] Greenlite 45-L Plus sheet. https://www.scribd.com/document/584772707/Greenlite-45-l-Plus-3
- [S49] Promat PROMASIL data sheets (PDF). https://www.distriplac.com/media/catalog/product/3/1/31099313375.pdf ; https://media.promat.com/doc_682552_us/original/1850243040/promat-data-sheet--promasil-en-us.pdf?market=us
- [S50] BNZ ZelieBlok. https://www.bnzmaterials.com/zelieblok/
- [S51] ROCKWOOL ProRox SL 560 / 460 / 760 data sheets (PDF). https://rti.rockwool.com/syssiteassets/tools--documentation/products-industrial/product-data-sheets/english/rti-prorox-sl-560_na_en.pdf ; https://rti.rockwool.com/syssiteassets/tools--documentation/products-industrial/product-data-sheets/english/rti-prorox-sl-460_na_en.pdf ; https://rti.rockwool.com/syssiteassets/tools--documentation/products-industrial/product-data-sheets/english/rti-prorox-sl-760_na_en.pdf
- [S52] IES-VE, Table 23 emissivities (CIBSE Guide C3.7). https://help.iesve.com/ve2026/table_23_emissivities_of_various_materials__table_c3_7_cibse_guide_.htm
- [S53] Engineering ToolBox, Emissivity coefficients. https://www.engineeringtoolbox.com/emissivity-coefficients-d_447.html
- [S54] Larkin Refractory, Firebrick 101. https://www.larkinrefractory.com/resources/firebrick-101/
- [S55] SSFBS, High Duty #1 arch. https://ssfbs.com/product/high-duty-1-arch-9-x-4-5-x-2-5/
- [S56] Armadillo Clay, Soft firebricks No. 1 arch. https://www.armadilloclay.com/store/p1422/Soft_Firebricks_-_No._1_Arch.html
- [S57] Bailey Pottery, #1 arch brick. https://www.baileypottery.com/k23-45-30-a4.html
- [S58] ASTM C909 / C861 listings. https://knowledge.bsigroup.com/products/standard-practice-for-dimensions-of-a-modular-series-of-refractory-brick-and-shapes ; https://shop-checkout.bsigroup.com/products/standard-practice-for-determining-metric-dimensions-of-standard-series-refractory-brick-and-shapes-2
- [S59] ASTM C680 abstracts. https://store.astm.org/c0680-23.html ; https://webstore.ansi.org/standards/astm/astmc68019
- [S60] Universidad de Los Andes course notes, Convección (PDF). https://webdelprofesor.ula.ve/ingenieria/franz/index.html/TC/Conveccion.pdf
- [S61] EngineersEdge, Isothermal vertical plate natural convection. https://engineersedge.com/heat_transfer/isothermal_vertical_plate_natural_convection_13964.htm
- [S62] Maya HTT, Horizontal plate, hot side up. https://thermal.mayahtt.com/tmwiz/convect/natural/hup-isot/about.htm ; Lloyd and Moran study: https://experts.umn.edu/en/publications/natural-convection-mass-transfer-adjacent-to-horizontal-plates/ ; COMSOL: https://doc.comsol.com/6.2/doc/com.comsol.help.heat/heat_ug_theory.07.091.html
- [S63] Neutrium, Properties of air. https://neutrium.net/articles/properties/properties-of-air/
- [S64] FOSSEE textbook companion, Basic Mechanical Engineering ch. 6. https://tbc-python.fossee.in/convert-notebook/Basic_Mechanical_Engineering/bme6.ipynb
- [S65] CSJM University, CHE S204 Chapter 2 Conduction (PDF). https://gyansanchay.csjmu.ac.in/wp-content/uploads/2022/01/CHE-S204-Chapter-2-Conduction_G.pdf
- [S66] LearnChemE, Semi-infinite solid. https://learncheme.com/quiz-yourself/interactive-self-study-modules/semi-infinite-solid/semi-infinite-solid-screencasts/
- [S67] Semnan University notes (Holman-based). https://mjahangiri.profile.semnan.ac.ir/downloads/file/8773
- [S68] Physics Forums, Transient solution. https://www.physicsforums.com/threads/transient-solution-for-a-semi-infinate-solid-from-a-pipe.347321/post-2403729
- [S69] L&L Kiln, What does it cost for the electricity to fire the kiln? https://hotkilns.com/support/pottery-kiln-knowledgebase/what-does-it-cost-electricity-fire-kiln
- [S70] Skutt, Studio FAQs. https://skutt.com/skutt-resources/resources-just-for-you/studio/faqs/
- [S71] Lakeside Pottery, Estimating electric kiln firing costs. https://lakesidepottery.com/HTML%20Text/Tips/estimating-electric-kiln-firing-costs.htm
- [S72] Ceramic Arts Daily forum, Paragon DTC 800 / kiln max temperature. https://community.ceramicartsdaily.org/topic/30261-paragon-dtc-800-kiln/ ; https://community.ceramicartsdaily.org/topic/41800-kiln-max-temperature
- [S73] L&L E23T-3 listings. https://kruegerpottery.com/products/ll-easy-fire-e23t-3 ; https://www.dickblick.com/items/l-l-easy-fire-kiln-e23t-3-w11520-240v-p1-48-0-amp/
- [S74] Skutt KM-1027 / KM-818 listings. https://www.theceramicshop.com/product/18271/km-1027-kiln-240v-1p-w-fk/ ; https://www.creative-crafts.com/skutt-km818-electronic-kiln
- [S75] Wikipedia, Pyrometric cone (wikitext). https://en.wikipedia.org/w/index.php?title=Pyrometric_cone&action=raw
- [S76] Orton, Cone 10 self-supporting. https://www.ortonceramic.com/product-page/10-self-supporting-25-box
- [S77] Orton, Pyrometric cones FAQ. https://www.ortonceramic.com/pyrometric-cones-faq
- [S78] Orton, °F cone chart 022–14 (PDF). https://www.ortonceramic.com/files/2676/File/Orton-Cone-Chart-F-022-14.pdf
- [S100] T. Crnko, "Overcurrent protection, part 2", IAEI Magazine, May/June 2007 (2005 NEC). https://iaeimagazine.org/features/overcurrent-protection-part-2
- [S101] Morgan Advanced Materials – Thermal Ceramics, "Cerablanket and Cerachem Blankets" product data sheet, code BL.03, 1 January 2025 (read 2026-10-29). https://www.morganthermalceramics.com/media/3993/cerablanket_cerchem-blankets_eng.pdf
- [S79] Aperam Alloys Rescal, Resistohm 145 data sheet, April 2012 (PDF, read). https://www.aperam.com/sites/default/files/documents/datasheet_RESISTOHM_145.pdf
- [S80] JLC Electromet, FeCrAl data sheet, May 2016 (PDF, read). https://www.jlcelectromet.com/downloads/20.data.sheet.FeCrAl.pdf
- [S81] NiWire, Nichrome 80 data sheet (search extract). https://www.mikrocontroller.net/attachment/659182/Nichrome_80.pdf
- [S82] JLC Electromet, Nickel-Chromium data sheet, Dec 2020 (PDF, read). https://www.jlcelectromet.com/downloads/2.data.sheet.NiCr.pdf
- [S83] Omega (DwyerOmega), NI80 resistance heating wire (search extract). https://www.dwyeromega.com/en-us/2100-f-max-80-nickel-20-chromium-resistance-heating-wire/p/NI80 ; Concept Alloys Chromel A: https://conceptalloys.com/?p=5624
- [S84] Çengel, Heat and Mass Transfer, Table A-9, Properties of air at 1 atm (PDF, read). https://www.me.psu.edu/cimbala/me420/Links/Table_A_9_CC_Properties_of_Air.pdf
- [S85] University of Waterloo ME 353, air properties after Incropera & DeWitt Table A.4 (read). https://www.mhtlab.uwaterloo.ca/courses_old/me353/maple/tp/airprops1.html
- [S86] Kanthal, Element surface load. https://kanthal.com/en/knowledge-hub/heating-material-knowledge/element-surface-load ; Gold Refining Forum, element design (cites "Brauer", unverified). https://www.goldrefiningforum.com/threads/how-to-design-electric-elements-for-kilns.22204/
- [S87] US Patent 5,126,535, Furnace and kiln construction (search extract). https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/5126535
- [S88] Solar-electric forum, "The 125% rules and the NEC" (quotes Art. 100). https://forum.solar-electric.com/discussion/comment/331643
- [S89] Mike Holt forum, NEC 210.20(A) clarification. https://forums.mikeholt.com/threads/nec-210-20-a-clarification.2555041/post-2638656
- [S90] Austin Gallery, Kiln electrical requirements. https://www.austingallery.org/blog/kiln-electrical-requirements
- [S91] BNZ 23 insulating firebrick listing (ASTM C182, search extract). https://ibspot.com/products/bnz-materials-9-x-4-5-x-2-5-2300-f-insulating-firebrick-12ct-box
- [S92] Plibrico fireclay brick sheet via Forno Bravo (search extract). https://community.fornobravo.com/filedata/fetch?id=284408 — **Misattributed** (masonry-materials.md §6, 2026-10-29): the file at this address is a Plibrico mortar sheet with no conductivity; the 8.2–9.5 Btu·in figures are Alsey's fireclay brick sheets, masonry-materials.md [M9] [M10].
- [S93] CNBM, Fibra cerámica data sheet (search extract). https://safe-energy.cl/pdf/CNBM/Fibra_Ceramica.pdf
- [S94] Distribution International, Unifrax Durablanket S 8 pcf. https://shop.distributioninternational.com/refractories/ceramic-fiber/ceramic-fiber-blankets/cfbt8104dsu
- [S95] EngineersEdge emissivity table. https://engineersedge.com/heat_transfer/emissivity.htm ; Optris emissivity table: https://optris.com/us/technology/emissivity-table/
- [S96] Distribution International, HWI Greentherm 23/26 straights 9 × 4½ × 2½. https://shop.distributioninternational.com/refractories/refractories-bricks/rebr23094525sgh
- [S97] Forno Bravo forum, Firebricks in South Florida (#2 arch taper). https://community.fornobravo.com/forum/pizza-oven-design-and-installation/getting-started/6976-firebricks-in-south-florida?p=96376
- [S98] Caleb Bell, `ht` library, Free convection to immersed bodies (read). https://ht.readthedocs.io/en/latest/ht.conv_free_immersed.html
- [S99] Maya HTT, Vertical plate, isothermal. https://thermal.mayahtt.com/tmwiz/convect/natural/vp-isot/about.htm
