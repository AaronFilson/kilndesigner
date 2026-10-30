# Electrical supply reference data

Compiled 2026-10-24 for kilndesigner (see `docs/planning/02-plan.md`).
Sources are given as [E#] in the Sources list at the end. The prefix is E, so these do not clash
with the [S#] numbers in `electric-and-thermal.md`. That file's [S#] are cited by their own numbers.

How to read this file (same tiers as `electric-and-thermal.md`):

- **Verified**: read from the source document itself.
- **Excerpt**: taken from a search-engine extract or a secondary reproduction. The primary text
  (NFPA 70, ANSI C84.1) is paywalled and was not read.
- **Derived**: worked out here from sourced inputs. The formula is shown.
- **Not found**: no source located. No number is given.

The target was three independent sources per fact. Each section says how many it has. Where the
count is below three, the shortfall is stated.

---

## 1. Service voltage: ANSI C84.1

### 1.1 Ranges (Verified from [E1]; 120 V service limits also in [E2], [E3])

ANSI C84.1 sets two ranges for each nominal system voltage. **Range A** is the normal design range.
Equipment "shall be designed and rated to give fully satisfactory performance" in it. **Range B**
covers excursions that "shall be limited in extent, frequency, and duration"; corrective action is
expected. Limits apply to sustained voltages, not momentary dips [E1].

Table 1 of [E1] (PG&E, July 2018, quoting C84.1). Service = Range A service, −5 %/+5 %.
Utilization = Range B utilization, −13 %/+6 %.

| Nominal (V) | Range A service (V) | Range B utilization (V) | Equipment nameplate (V) | NEMA ±10 % of nameplate (V) |
|---|---|---|---|---|
| 120 | 114 – 126 | 104.4 – 127.2 | 115 | 103.5 – 126.5 |
| 208 | 197.6 – 218.4 | 181 – 220.5 | 200 | 180 – 220 |
| 240 | 228 – 252 | 208.9 – 254.4 | 230 | 207 – 253 |
| 277 | 263.2 – 290.9 | 241 – 293.6 | not listed | not listed |
| 480 | 456 – 504 | 417.6 – 508.8 | 460 | 414 – 506 |

Figure 1 of [E1], on a 120 V base: Range A service 114–126 V; Range B service 110–127 V;
Range A utilization 110 (108 for non-lighting) – 125 V (126 for systems above 600 V);
Range B utilization 106 (104 non-lighting) – 127 V.

Cross-checks (Excerpt): the USDA RUS bulletin 1724D-113 reproduces C84.1-2016 with 120 V
Range A 114–126, Range B 110–127, Range B utilization minimum 104 [E2]. Con Edison EO-2096 gives the
same 126/114 and 127/110 [E3]. An Iowa State course note gives 107 V as a Range B utilization
minimum [E4]; this disagrees with [E1] and [E2]. **Use [E1]'s table**; the utilization lower bound
has a ±3 V spread between sources.

Not found: the exact "−8.3 %" figure. Range B service on 120 V is 110/120 = −8.3 % (Derived), so the
figure is consistent with Range B service, but it was not seen stated in a source. The Range B
service limits for 208Y/120 V and 480 V were not read from a primary table; scale the 120 V base
(Derived: V_nom × 110/120 and × 127/120). C84.1 itself (2016/2020 edition) was not read.

### 1.2 How 208 V vs 240 V is recognised (3 sources, all practice, not a standard)

- 208 V comes from a 208Y/120 V three-phase service (two legs of a wye); 240 V from 120/240 V
  single-phase. The nominal values are 13 % apart (208/240 = 0.867), wider than Range A's ±5 %
  band, so a measured voltage normally falls clearly in one band: 197.6–218.4 V vs 228–252 V [E1]
  (Derived from the table).
- Skutt: "contact your local power company or an electrician to determine what voltage you have
  (208 or 240 volt supplies)". 208 V kilns "should never be fired on a 240V supply without first
  installing a full set of 240V elements"; 240 V kilns "should not be used on a 208 volt supply ...
  will fail to reach the maximum rated temperatures" [E5] (Verified).
- Skutt's table lists 208 V and 240 V versions of each model; 1-phase models of the same size draw
  the same current at both voltages with lower watts at 208 V (KM1027 1-ph: 48.0 A, 11520 W at
  240 V, 9980 W at 208 V) [E5] (Verified). So makers re-wind the elements for 208 V to keep current
  equal, and accept ~13 % less power (9980/11520 = 0.866, Derived).
- Forum practice (Excerpt, weak): 240 V elements on 208 V give (208/240)² ≈ 0.75 of rated power and
  may not get past bisque; 208 V elements on 240 V draw more current (48 A → ~55 A) [E6], [E7].
- L&L and Paragon: Not found as maker documents in this pass. Only forum relays [E6], [E7].

**Engine:** take supply as nominal 120, 208, 240, 277 or 480 V. Check the design at Range A min and
max (±5 %) and report power at each; refuse a supply value outside Range B (ADR 0009). Never let a
240 V element set be specified for a 208 V supply without stating the power ratio.

---

## 2. Conductors and overcurrent protection: NEC (NFPA 70)

The code text was not read (paywalled). Edition: values below are from 2020 NEC reproductions
unless stated; the 2023 rules are reported unchanged in substance [E9]. Check the edition the
jurisdiction has adopted.

### 2.1 Continuous load, 125 % (3 sources, Excerpt)

- Continuous load: maximum current expected for 3 h or more (NEC Article 100) [E9], [E10].
- 210.19(A)(1): branch-circuit conductors ampacity ≥ 125 % of the continuous load plus 100 % of
  the non-continuous load [E9], [E10], [E11].
- 210.20(A): overcurrent device rating ≥ 125 % of continuous load, unless the device and assembly
  are listed for 100 % operation [E9], [E10].
- Kilns: treated as continuous loads by makers and installers. Skutt's table pairs 48 A with a
  60 A breaker and 6 AWG Cu, 29.3–33 A with 40 A and 8 AWG, 20 A with 30 A and 10 AWG, "based on
  National Electric Code Requirements" [E5] (Verified). 48 × 1.25 = 60 (Derived). A supplier page
  states the same 125 % rule for kilns [E12].
- Article 422 (appliances): 422.10(A) — for a non-motor appliance that is a continuous load, the
  branch-circuit rating is not less than 125 % of the marked rating [E11] (Excerpt, one source).
  [E12] cites 424.3(B) (fixed space heating) instead; which article governs a kiln is not settled
  in the sources found. Both lead to 125 %. 110.3(B) (follow listing instructions) means the
  maker's nameplate breaker size controls when stated [E13] (forum, weak).

### 2.2 Table 310.16, copper, not more than 3 current-carrying conductors, 30 °C ambient

Excerpt from the 2020 NEC reproduction [E14]; 14–10 AWG corroborated by [E15]. One gap: 3 AWG at
60 °C and 90 °C were not in the reproduction.

| AWG | 60 °C (A) | 75 °C (A) | 90 °C (A) |
|---|---|---|---|
| 14* | 15 | 20 | 25 |
| 12* | 20 | 25 | 30 |
| 10* | 30 | 35 | 40 |
| 8 | 40 | 50 | 55 |
| 6 | 55 | 65 | 75 |
| 4 | 70 | 85 | 95 |
| 3 | not found | 100 | not found |
| 2 | 95 | 115 | 130 |

Older editions (1996 and some reproductions) show 20 A for 14 AWG at 60 °C [E15]; the 2020 value
is 15 A. Source count for 8–2 AWG is one; treat as Excerpt, verify before release.

### 2.3 240.4(D) small conductors (2 sources, Excerpt)

Unless 240.4(E)–(G) permit otherwise, overcurrent protection shall not exceed 15 A for 14 AWG,
20 A for 12 AWG, 30 A for 10 AWG copper [E14], [E15].

### 2.4 110.14(C) terminal temperature (2 sources, Excerpt)

Size conductors by the terminal rating, not the insulation. For circuits rated 100 A or less, or
14–1 AWG, use the 60 °C column unless the equipment is marked 75 °C; above that, the 75 °C column.
The 90 °C column is a starting point for derating only [E14], [E15].

**Engine:** I_branch = nameplate A × 1.25 → round up to a standard breaker size; pick the smallest
Cu conductor whose ampacity in the terminal-rated column (60 °C default, 75 °C if the user says the
terminals are marked) is ≥ 1.25 × I and which satisfies 240.4(D). Report the edition used and that
derating (ambient, bundling, voltage drop) is not applied. Refuse above 2 AWG (no checked data).

---

## 3. Power and current versus voltage and temperature

### 3.1 Voltage (physics, Derived)

For a resistive element, P = V²/R and I = V/R. At fixed R:
P(208)/P(240) = (208/240)² = 0.751; at Range A limits, (0.95)² = 0.9025 and (1.05)² = 1.1025.
Two forum sources state the same ~75 % for 240 V elements on 208 V [E6], [E7].

### 3.2 Cold resistance and inrush (Derived from [S1] in `electric-and-thermal.md`)

Kanthal A-1 Ct is 1.00 to 400 °C and 1.04 at 1000–1300 °C [S1]. So R_cold = R_hot / 1.04 and the
cold current is 1.04 × hot current (4 % higher); cold power 4 % higher. For Nikrothal 80
(Ct 1.07 at 1200 °C) the factor is 1.07. This is small; there is no motor-like inrush. One forum
note says the same ("drift is small") [E8]. Use the cold value for breaker sizing.

### 3.3 Ageing (3 sources, all forum/hobbyist; no maker document found)

- Replace when measured cold resistance is more than 10 % over spec; some run to 14–15 % [E8].
- A maintenance guide: if any element is more than 10 % out of spec, replace the set [E16].
- Reported effect: ~10–15 % resistance rise cost ~30 % of output at top temperature [E8]. Note the
  P = V²/R loss alone is 1 − 1/1.10 = 9 % (Derived); the larger observed loss is because net heat
  input at top temperature is power minus wall loss. Do not encode 30 % as data.
- Kanthal, L&L, Skutt, Paragon statements of the 10 % figure: Not found in this pass.

**Engine:** report power at new resistance and at R × 1.10 (end of life), labelled as the
practice rule from [E8], [E16]; check the kiln still reaches the target cone at the aged power.

---

## 4. Three-phase element connections (physics; maker data 1 source)

- Delta: each element across two lines, sees V_line. Wye: each element from line to neutral (star
  point), sees V_line/√3 (480 V → 277 V; 208 V → 120 V) [E17], [E18] (forum, Excerpt).
- Balanced delta: line current = √3 × element current [E19] (forum). In a delta with only one
  element per pair, one shared line carries more current ("about 1.7×") [E19].
- P_total = √3 × V_line × I_line for a balanced load (Derived, standard).
- Skutt 3-phase data (Verified, [E5]): KM1027 3-ph 240 V 29.3 A 11520 W; 208 V 31.7 A 11000 W;
  KM1227-3 PK 3-ph 240 V 40.0 A, 208 V 46.7 A, both 14300 W. Check: 11520 / (√3 × 240) = 27.7 A
  (Derived) against 29.3 listed; makers' figures include controls and rounding, so use the
  nameplate, not the derived value, for breaker sizing.
- 480 V kilns: no maker document found. Wye on 480Y/277 lets 277 V elements be used [E17].

**Engine:** for 3-phase, compute element voltage from connection (delta = V_line, wye =
V_line/√3), require element count to be a multiple of 3 for balance, and report line current.
Refuse unbalanced layouts until a source for unbalanced practice is added.

---

## 5. Wire temperature vs furnace temperature and surface load (Kanthal)

What was found:

- Kanthal's handbook worked example (rod-over-bend, 5.5 mm wire, 1000 °C furnace): Kanthal AF
  element 1106 °C at 3.98 W/cm²; Nikrothal 80 element 1068 °C at 3.09 W/cm² [E20] (Excerpt from
  the handbook text; also relayed in two search summaries of [E21]). So ΔT ≈ 106 K and 68 K at
  those loads. One example only; it is a freely radiating rod-over-bend, not a coil in a groove.
- Kanthal: "Increased surface load results in a higher element temperature compared to its
  surroundings"; "For embedded and supported element types, the wire temperature depends on both the
  wire and the element surface load" [E22] (Verified).
- Kanthal's max surface load at 1000 °C furnace: spirals in grooves or on tubes 3–4 W/cm²;
  rod-over-bend and looped 5–6 [E23] (Verified). On-off control: choose about 20 % lower [E22].
- The diagram of element temperature vs surface load at furnace temperatures exists in Kanthal's
  handbook/design-calculation PDFs [E21], [E24], but those PDFs are image-based and could not be read
  here; no curve values were extracted.

Not found: any digitisable value for a coil in a groove (e.g. 1200 °C furnace at 2 W/cm²). The
"wire runs 100 °C above the kiln" assumption is not supported for grooved coils; the only sourced
point is ~106 K at 3.98 W/cm² for a free rod at 1000 °C. **Engine:** do not compute wire temperature
from a fixed offset. Either leave it out and say so, or ask the user (owner of Kanthal handbook print
copy?) to read the chart values in [E21] into a table.

---

## Gaps

1. Primary texts of ANSI C84.1 and NFPA 70 not read; all code values are from reproductions.
2. Table 310.16 for 8–2 AWG has one source; 3 AWG at 60/90 °C missing.
3. Which NEC article governs kilns (422 vs 424) not settled.
4. No maker (Kanthal, L&L, Skutt, Paragon) statement of the 10 % replacement rule.
5. No L&L or Paragon 208/240 V ordering document; no 480 V kiln maker data.
6. Kanthal wire-temperature chart not digitised.

## Sources

- [E1] PG&E, "Voltage Tolerance Boundary", July 2018. https://PGE.com/assets/pge/docs/contact-us/report-an-issue/Voltage_Tolerance.pdf
- [E2] USDA RUS, UEP Bulletin 1724D-113. https://rd.usda.gov/sites/default/files/UEP_Bulletin_1724D-113.pdf
- [E3] Con Edison, EO-2096. https://www.coned.com/-/media/files/coned/documents/es/specs/electric/eo-2096.pdf
- [E4] Iowa State EE455 notes, voltage regulators. https://wzy.ece.iastate.edu/Courses/EE455/08%20EE455%20Modeling%20Voltage%20Regulators.pdf
- [E5] Skutt, "Installation and Electrical Notes" and Electrical Requirements table. https://skutt.com/contractors/elec_install.pdf
- [E6] Ceramic Arts Daily forum, Paragon voltage conversion 240 V to 208 V. https://community.ceramicartsdaily.org/topic/27527-paragon-kiln-voltage-conversion-240v-to-208v/
- [E7] Ceramic Arts Daily forum, running a 208 V kiln at 240 V. https://community.ceramicartsdaily.org/topic/22372-running-a-208v-single-phase-kiln-at-240v/
- [E8] Ceramic Arts Daily forum, resistance change in elements / do these elements need replacing. https://community.ceramicartsdaily.org/topic/24005-resistance-change-in-elements/ and https://community.ceramicartsdaily.org/topic/19754-do-these-elements-need-replacing/
- [E9] Mike Holt forum, 210.19(A)(1) 2023 cycle. https://forums.mikeholt.com/goto/post?id=2937334
- [E10] VIOX, NEC 125 % rule for continuous loads. https://viox.com/bn/nec-125-percent-rule-continuous-loads/
- [E11] EC&M, Code Q&A water heaters / 422. https://ecmweb.com/national-electrical-code/qa/article/21125391/code-qa-electrical-requirements-for-water-heaters
- [E12] Seattle Pottery Supply, for the installing electrician. https://seattlepotterysupply.com/pages/electrician-kiln-install
- [E13] Mike Holt forum, kiln installation. https://forums.mikeholt.com/threads/kiln-installation.2557190/post-2622105
- [E14] Open Exam Prep, conductor ampacity (Table 310.16, 2020 NEC). https://open-exam-prep.com/study-guides/va-electrician/conductors-and-cables/conductor-ampacity
- [E15] Border States, NEC Table 310-16 reproduction; Elektroda 2023 excerpt. https://solutions.borderstates.com/?p=5303 and https://www.elektroda.com/qa,nec-table-31016-ampacity-wire-sizing.html
- [E16] docum.ents.ca pottery troubleshooting. https://docum.ents.ca/books/pottery/page/troubleshooting/export/markdown
- [E17] Mike Holt forum, 440 V heaters (delta/wye). https://forums.mikeholt.com/threads/440-volt-heaters.34088/post-528907
- [E18] Ceramic Arts Daily forum, kiln conversion 1 ph to 3 ph. https://community.ceramicartsdaily.org/topic/22514-kiln-conversion-from-1ph-to-3ph/
- [E19] Mike Holt forum, delta wired calculations for kiln elements. https://forums.mikeholt.com/goto/post?id=1742521
- [E20] Kanthal handbook copy (ibt.co.il). https://www.ibt.co.il/uploaded_files/documents/file1434025342_U5122.pdf
- [E21] Kanthal, Resistance heating alloys and systems for industrial furnaces. https://prodshop.kanthal.com/globalassets/kanthal-global/downloads/resistance-heating-alloys-and-systems-for-industrial-furnaces_b_eng_lr.pdf
- [E22] Kanthal, Design calculations for heating elements. https://www.kanthal.com/en/knowledge-hub/heating-material-knowledge/design-calculations-for-heating-elements/
- [E23] Kanthal, Key data for Kanthal elements. https://www.kanthal.com/knowledge-hub/heating-material-knowledge/key-data-for-kanthal-elements/
- [E24] Kanthal, Design calculations of wire elements (PDF). https://prodshop.kanthal.com/contentassets/3720091e7e604cf89d4a289536f6b56b/design-calculations-of-wire-elements.pdf
