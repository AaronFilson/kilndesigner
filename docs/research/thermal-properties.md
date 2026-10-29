# Thermal properties, touch limits and heat-transfer validity ranges

Collected 2026-10-24. This file adds to `electric-and-thermal.md` §4 and §6. It does not repeat
the conductivity tables there.

Labels:

- **Verified**: read in the source text here, quoted or tabulated.
- **Excerpt**: read through a search summary or a partial copy. Check before relying on it.
- **Not found**: searched for and not found. No value is given, and none should be invented.

The aim was three independent sources per fact. Each section says how many were found. Sources
are [T1] to [T24] at the end.

---

## 1. Specific heat c_p(T)

| Material | c_p | Temperature | Sources | Status |
|---|---|---|---|---|
| Fire brick (generic) | 1.05 kJ/(kg·K) (0.25 Btu/(lb·°F)) | not stated | Engineering ToolBox [T1] | Verified, 1 source |
| Insulating firebrick (generic) | 960 J/(kg·K) | 300 °C row | Lienhard & Lienhard appendix, garbled scan [T2] | Excerpt, 1 source. The same row gives ρ ≈ 2000 kg/m³, which is wrong for IFB, so the row may be misread |
| 26-class IFB (one vendor, 500 kg/m³) | 1.21 kJ/(kg·K) | 1000 °C | Solargil listing [T3] (already [S34]) | Excerpt, 1 source |
| Fireclay (Bejan table) | 0.84 kJ/(kg·K) | 100 °C | via search summary [T2] | Excerpt, 1 source |
| Chamotte fireclay | 0.8 (unit column missing, probably kJ/(kg·K)) | not stated | Engineering ToolBox [T1] | Verified, 1 source |
| High-alumina refractory (IEC 60672 C-510) | 800 J/(kg·K) | not stated | MakeItFrom [T4] | Excerpt, 1 source |
| Ceramic fibre blanket (Kaowool, Fiberfrax Durablanket) | 0.27 Btu/(lb·°F) = 1.13 kJ/(kg·K) | not stated | distributor listings for Morgan [S42] and Unifrax [T5] | Excerpt, 2 listings that may share one origin. Not on the makers' own sheets |
| Mineral wool blanket | 0.84 kJ/(kg·K) | not stated | Engineering ToolBox [T1] | Verified, 1 source |
| Calcium silicate (PROMASIL-1100) | 1.05 kJ/(kg·K) | not stated | already [S49] | 1 source |
| Steel (generic) | 0.49 kJ/(kg·K) | room temperature | Engineering ToolBox [T1] | Verified |
| A36 carbon steel | 470 J/(kg·K) | room temperature | MakeItFrom [T6] | Excerpt |
| Carbon steel, c_a(θ) | see the formula below | 20–1200 °C | EN 1993-1-2 §3.4.1.2, via Dlubal [T7] | Verified (secondary copy of the code) |

For steel there are three sources at room temperature (0.465–0.49 kJ/(kg·K)), and EN 1993-1-2 gives
the temperature dependence. The value 486 J/(kg·K) was **not found** in any source.

**EN 1993-1-2 carbon steel specific heat** [T7], with θ in °C and c_a in J/(kg·K):

- 20 ≤ θ < 600: c_a = 425 + 0.773·θ − 1.69×10⁻³·θ² + 2.22×10⁻⁶·θ³
- 600 ≤ θ < 735: c_a = 666 + 13002/(738 − θ)
- 735 ≤ θ < 900: c_a = 545 + 17820/(θ − 731)
- 900 ≤ θ ≤ 1200: c_a = 650

These give c_a ≈ 440 at 20 °C and ≈ 488 at 100 °C, which agrees with [T1] and [T6]. Conductivity in
the same code is λ_a = 54 − 3.33×10⁻²·θ W/(m·K) for 20–800 °C, and 27.3 above that. Dlubal prints
3.3×10⁻². EN 1993-1-2 is generally quoted as 3.33×10⁻². Check against the code itself.

**Not found:**

- c_p(T) curves for JM 23, JM 26, K-23 or K-26 from Morgan. The 2011 and 2025 JM sheets and the K
  sheet [T8] list no specific heat.
- Georgia Tech's Gen3 CSP K23 page [T9] has measured thermal diffusivity of K23, as a plot and a
  K23.xlsx file. The numbers could not be read here. **This is the best lead for a measured IFB
  property.** If c_p is needed, use it with k and ρ, as c_p = k/(ρ·α).
- c_p(T) for dense fireclay, high-alumina brick, or dense and insulating castables, from a maker,
  Harbison-Walker, Perry's or NIST. The Harbison-Walker 2005 Handbook copy at mha-net.org returns
  404 [T10].
- Incropera Table A.3 (fireclay brick, kaolin insulating brick) was not read directly.

## 2. Thermal expansion

Olsen, 4th ed. p.51: each foot of refractory wall grows 1/16–3/32 in
(0.52–0.78 %) heating and cooling, which agrees with the IFB figures below.

### 2.1 Refractories

| Material | Value | Sources | Status |
|---|---|---|---|
| JM IFB series (JM23 and up) | "Reversible Linear Thermal Expansion, max. %: 0.5". The test temperature is not printed beside it | Morgan JM IFB sheet, PDF text extracted [T11] | Verified, 1 source |
| TJM IFB series | max reversible expansion 0.6% (TJM 23), 0.7% (the others). Temperature not shown | Morgan TJM sheet [T12] | Excerpt |
| Kaolin IFB, class 26 (ISO 26-140 / ASTM C155) | 0.5% reversible, 20–1000 °C | H.S. Walsh TF29 data sheet [T13] | Excerpt |
| Fireclay firebrick, about 32% Al₂O₃ | 0.6% linear expansion at 1000 °C, method not stated | Mathios "Firebrick Lava" listing [T14] | Excerpt |
| Dense castables (Plicast 31R, 34R, Plibrico Super AB, Superal XAB) | 0.55, 0.60, 0.56, 0.60 at 1000 °C (presumably %) | user-made Google Sheet [T15] | Excerpt, unofficial |
| Insulating castables (Blazelite 26 LI, Kaolite 2600LI, Firelite 2600LI) | Only the **permanent** linear change at 1500 °F is given (−0.3%, −0.1 to −0.6%, −0.2%). No reversible expansion | BNZ and Morgan sheets [T16] | Excerpt. This is not reversible expansion |

So IFB is about 0.5–0.7% at 1000 °C (3 sources: Morgan JM, Morgan TJM, H.S. Walsh). Dense fireclay
and dense castables are about 0.55–0.6% at 1000 °C, but only from weak sources.

**Not found:**

- Any refractory's expansion curve up to 1300 °C.
- Reversible expansion of Kast-O-Lite or Mizzou.
- Kast-O-Lite's permanent linear change.

BS 1902-5.3 (reversible expansion) tests only to 1100 °C [T17].

### 2.2 Steel

- A36 and low-carbon steel: α ≈ 11.7×10⁻⁶ /°C at room temperature [T6, T18, T19]. MakeItFrom rounds
  it to 11 µm/(m·K). That is 3 sources. ASTM A36 itself sets no thermal properties.
- EN 1993-1-2 thermal elongation [T7]:
  - 20 ≤ θ < 750 °C: Δl/l = 1.2×10⁻⁵·θ + 0.4×10⁻⁸·θ² − 2.416×10⁻⁴
  - 750–860 °C: Δl/l = 1.1×10⁻²
  - 860–1200 °C: Δl/l = 2×10⁻⁵·θ − 6.2×10⁻³
- Matmatch (EN 10216-2 St 45.8) gives a mean α of 1.22–1.25×10⁻⁵ /K at 100 °C and
  1.46–1.49×10⁻⁵ /K at 600 °C [T20]. Excerpt.

### 2.3 Thrust from a restrained arch, and adjusting tie rods

**No authoritative refractory reference was found.** Harbison-Walker is 404 [T10], and Norton,
Chesters and Olsen were not available online. Ask the user for Olsen (see the memory note).

What was found:

- Coke-oven patent US3054730A [T21]. The nuts on the tie rods are "gradually loosened, in the course
  of the heating, corresponding to the progressive expansion", so that "a uniform stress is
  maintained in the masonry". Unplanned loosening is "detrimental to the bracing". This is an
  industrial precedent for backing the rods off as the masonry heats.
- Glass-furnace patents US3962528A and US4137037A [T21]. Skews sit on heel plates fixed to
  buckstays. Uneven heating makes bricks expand at different times, and hearth growth turns the
  sidewalls and loads the ends of the arch bricks.
- Ceramic Arts Daily forum thread [T22]. All-thread across the top "so you can tighten it up if
  needed", and advice against springs. Anecdotal.

**Not found:** any formula or number for the thermal thrust of a restrained arch.

## 3. Mean-temperature convention and how C680 uses k(T)

- ASTM C182 (IFB), C201 (refractory insulation, fibre), C1113 (hot wire) and C177 (guarded hot plate)
  report the apparent k at the **mean** temperature of the specimen (see `electric-and-thermal.md`
  §4). The standards' own texts were not read here (paywalled).
- ASTM C1045 is the practice that turns such test data into a k(T) relation. Its abstract [T23]
  says it "describes a method for building apparent thermal conductivity as a function of
  temperature from standard test data taken at small or large temperature differences". The
  resulting relation "can be used ... for use in calculation programs such as Practice C680".
- C680 itself [S59, T24] handles k(T) in each homogeneous layer, and iterates on the surface
  temperature.
- 3E Plus implements C680. An industry note says a single second-order polynomial in temperature
  fits the k curve well for glass fibre, mineral wool, perlite and calcium silicate, but not for
  closed-cell foams [T24].
- **The exact C680 text is not verified (paywalled).** This includes its fitting form, and whether it
  integrates k(T) dT across each layer (the Kirchhoff transform) or applies k at each layer's mean
  temperature.
- The standard physics, stated without a citation here: if k_m(T_m) is a mean-temperature fit from
  tests with a small ΔT, it approximates k(T) directly. Tests with a large ΔT need the C1045
  deconvolution.

## 4. Shell touch-temperature limits

### 4.1 UL 499 (Electric Heating Appliances, 14th ed., 17 Nov 2025)

Full text read [T25]. Kilns are covered as "ceramics-baking kilns and ovens".

Table 36.2, maximum surface temperatures, corrected to a 25 °C room:

| Location | Metal | Nonmetallic |
|---|---|---|
| Handles or knobs grasped for lifting, carrying or holding | 55 °C (131 °F) | 75 °C (167 °F) |
| Handles or knobs contacted but not for lifting, carrying or holding, and other surfaces subject to contact and user maintenance | 60 °C (140 °F) | 85 °C (185 °F) |
| Surfaces other than a heating-function surface that are known to be hot because they are near one | 70 °C (158 °F) | 95 °C (203 °F) |

- 31.3: surfaces likely to be contacted shall not exceed Table 36.2. Exception: accessible
  surfaces other than handles or knobs may exceed it if they are marked under 53.40, with "CAUTION"
  and "Hot Surface. Avoid Contact."
- 36.2.1 (kilns): the kiln is run until its temperatures stabilise. If it carries the 53.22
  marking, it is run instead to the marked internal temperature and the power is then cut.
- So a kiln case may exceed 70 °C when it carries the caution marking, but handles may not exceed
  55 °C or 60 °C.

### 4.2 ASTM C1055 and C1057

From the abstracts [T26]:

- C1055 sets a 5 s contact time for industrial settings and 60 s for consumer products. The longer
  time allows for children, older adults or people with infirmities.
- The recommended maximum injury is a first-degree burn, which is reversible. A second-degree burn
  may be set as a less desirable level. A third-degree burn is never acceptable.
- C1055 does **not** fix one temperature. The limit comes from the contact time, the surface system
  and the injury level.
- A presentation that reproduces C1055-03 [T27] says a metallic surface above 70 °C is a "hazard
  regardless of contact duration".
- **The "60 °C for 5 s" figure is not verified** in any source.
- C1057 estimates skin contact temperature. It has two methods: a mathematical model for design or
  worst-case checks, and a thermesthesiometer for operating systems only. It covers passive heated
  surfaces, and is meant for use with C1055 [T28].

### 4.3 Burn thresholds by contact time

From the same presentation [T27] (verified, PDF text extracted). The values are in °C. The table
sits beside C1055 and Stoll material, and in the search summary it is attributed to BS EN
13202:2000. EN 13202 is the predecessor of ISO 13732-1.

| Surface | 1 s | 4 s | 10 s | 600 s | >1000 s |
|---|---|---|---|---|---|
| Uncoated metal | 65 | 58 | 55 | 48 | 43 |
| Painted metal | 83 | 64 | 55 | 48 | 43 |
| Enamelled metal | 74 | 60 | 56 | 48 | 43 |
| Ceramics, glass, stone | 80 | 70 | 66 | 48 | 43 |
| Plastics | 85 | 74 | 70 | 48 | 43 |
| Wood | 110 | 93 | 89 | 48 | 43 |

**The 1 min value of 51 °C was not found.** The ISO 13732-1 clause 4.2 text was not read. That is
1 source with tables, plus abstracts.

## 5. Natural convection validity ranges

### 5.1 Vertical plate, Churchill and Chu (1975)

Int. J. Heat Mass Transfer 18(11):1323–29.

- All-Ra form: valid for 0.1 < Ra < 10¹². Sources: EES library [T29], course note [S60] and
  EngineersEdge [S61]. That is 3 sources. Volupe says "entire range of Ra" [T30], and `ht` gives
  no range [T31].
- Laminar form: valid for Ra ≤ 10⁹ [S60, T30].
- The 10¹² limit is also quoted for the Churchill–Chu horizontal cylinder (Ra_D ≲ 10¹²) [T30].
- Inclined plates up to 60° from vertical: replace g by g·cos θ [T30].

### 5.2 Horizontal plates, L = A/P

| Case | Correlation | Ra range | Sources |
|---|---|---|---|
| Hot face up, or cold face down | 0.54 Ra^¼ | 10⁴–10⁷ | Volupe, citing McAdams and Incropera [T30]; [S62]; `ht` McAdams switch at 10⁷ [T31] |
| Hot face up, or cold face down | 0.15 Ra^⅓ | 10⁷–10¹¹ | the same 3 |
| Hot face down, or cold face up | 0.27 Ra^¼ | 10⁵–10¹⁰ (Volupe, McAdams via Incropera) [T30]. 10⁵–10¹¹ (Holman 7th ed via MayaHTT and EngineersEdge [T32]; [S62]) | 3 sources, with 2 different upper limits |

- MayaHTT's hot-up page gives 0.54 for 2×10⁴–10⁶ and 0.15 for 10⁶–10¹¹ [T32]. Holman uses this
  variant.
- Lloyd and Moran (1974) put the laminar/turbulent transition for a heated upward-facing plate at
  Ra ≈ 8×10⁶ [T33]. That is the source of the 8×10⁶ switch.
- **Hot face down, Ra^⅕ form:** Incropera 7th ed. "0.52 Ra^⅕, 10⁴–10⁹, Pr ≥ 0.7" was **not
  verified**. Schulenberg (1985), as given by Jaffer [T33], for an isothermal strip of width 2L:
  Nu = 0.544·Ra^⅕ / [1 + (0.477/Pr)^(3/5)]^(1/3). For a disk, using the radius: 0.619·Ra^⅕ /
  [1 + (0.520/Pr)^(3/5)]^(1/3). Jaffer tested his own formula of this kind over 10⁶ < Ra < 10¹².
- Raithby and Hollands: EES has a combined arbitrary-tilt method from Nellis and Klein §6.2.2 [T34].
  Its coefficients were not read.
- Use L = A/P, which is A/(2W + 2L) for a rectangle [T30, T32, S62]. VDI and Rohsenow use
  ab/(2(a + b)), which is the same thing [T31].

## 6. Shape factors for edges and corners

Incropera & DeWitt Table 4.1 (5th ed. pp. 193–194), via the EES SF_13 and SF_14 functions [T35] and
an NPTEL worked example [T36]:

- **Edge of two adjoining walls** of equal thickness L and inside length D: S = 0.54·D. The EES
  example gives SF_13(D = 1 m, L = 0.1 m) = 0.54 m.
- **Corner of three walls**: S = 0.15·L, added on top of the 1-D wall and edge terms [T35].
- NPTEL (a cubical furnace, L = 0.05 m) uses S_E = 0.54·D for each of 12 edges and S_C = 0.15·L for
  each of 8 corners: q = k·(6·S_W + 12·S_E + 8·S_C)·ΔT. It remarks only "Be sure to note that the
  restriction for S_E and S_C has been met" [T36].
- **The restriction itself (usually written D > L/5, so wall thickness < D/5) was not verified** in
  text. The EES pages show the formula only as an image.
- The attribution to Langmuir, Adams and Meikle (1913) was **not found**. Holman's table was not
  read.

## 7. Hemispherical vs normal emissivity

- CIBSE Guide Table C3.7 (via IES-VE, verified, already [S52]). The tabulated values are normal
  emissivities. Multiply by these to get hemispherical values: **bright metal 1.2, other smooth
  0.95, other rough 0.98** [T37].
  - So paint at ε_n 0.95 gives ε_h ≈ 0.90.
  - Oxidised steel at 0.79 gives about 0.75 to 0.77 (smooth or rough).
- NASA: stably oxidised 347 stainless has a total hemispherical ε of 0.87–0.91 at 600–2000 °F
  [T38]. That is too hot for this question.
- The 316L in-air value of 0.28–0.38 at 429–1096 K is for lightly oxidised stainless, not mild
  steel [T38].
- **Measured hemispherical ε of painted or oxidised mild steel at 50–150 °C was not found.** That
  is 1 source for the conversion factor.

---

## Corroboration summary

| Fact | Sources |
|---|---|
| Steel α ≈ 11.7×10⁻⁶ /K | 3 |
| Steel c_p at room temperature ≈ 0.47–0.49 kJ/(kg·K) | 3 |
| Steel c_p(T) and α(T) | 1 (EN 1993-1-2, via secondary copy) |
| IFB reversible expansion ≈ 0.5–0.7% | 3 |
| Fireclay or dense castable expansion ≈ 0.55–0.6% at 1000 °C | 2, both weak |
| Refractory c_p | 1 per value, generic only |
| UL 499 Table 36.2 | primary text |
| Burn-threshold table | 1 |
| Churchill–Chu 0.1 < Ra < 10¹² | 3 |
| Horizontal plate 0.54/0.15 ranges | 3 |
| Hot-face-down 0.27 Ra^¼ upper limit | 10¹⁰ in 1 source, 10¹¹ in 2 |
| Edge and corner factors 0.54·D and 0.15·L | 2 |
| Hemispherical/normal factor | 1 |

## Gaps

- Maker c_p(T) for JM/K IFB, dense fireclay, high-alumina brick and castables. Try the Georgia Tech
  K23.xlsx, Morgan technical service, or Olsen.
- Reversible expansion curves up to 1300 °C, and Kast-O-Lite and Mizzou expansion.
- Arch thrust guidance from Harbison-Walker, Norton, Chesters or Olsen.
- The exact text of ASTM C680 and C1045 on k(T), and of ISO 13732-1 clause 4.2, including the 1 min
  value.
- "60 °C / 5 s" in C1055.
- Incropera 7th ed. 0.52 Ra^⅕.
- The text of the edge-factor validity condition.
- Measured hemispherical ε of painted or oxidised mild steel near 100 °C.

## Sources

- [T1] Engineering ToolBox, Specific heat of solids. https://www.engineeringtoolbox.com/specific-heat-solids-d_154.html
- [T2] Lienhard & Lienhard, A Heat Transfer Textbook, physical properties appendix (EPFL copy). https://wiki.epfl.ch/me341-hmt/documents/Lienhard-Lienhard_2012_Physical%20properties%20ed4.pdf (via search summary; download timed out)
- [T3] Solargil 26FB IFB listing. https://solargil.com/gb/materiels-refractaires/589-briques-legeres-isolantes-haute-qualite-1400c-26fb.html
- [T4] MakeItFrom, High-alumina refractory IEC 60672 C-510. https://makeitfrom.com/material-properties/High-Alumina-Refractory-IEC-60672-Type-C-510
- [T5] Distribution International Fiberfrax / Durablanket listings. https://shop.distributioninternational.com/refractories/ceramic-fiber/ceramic-fiber-blankets/cfbt8102d26u
- [T6] MakeItFrom, ASTM A36 carbon steel. https://www.makeitfrom.com/compare/ASTM-A36-SS400-S275-Structural-Carbon-Steel/Ferrite
- [T7] Dlubal knowledge base 001496, EN 1993-1-2 steel properties. https://www.dlubal.com/en-US/support-and-learning/support/knowledge-base/001496
- [T8] Morgan K IFB series. https://www.morganthermalceramics.com/media/9429/k-ifb-series_eng.pdf
- [T9] Georgia Tech Gen3 CSP, K23 diffusivity. https://gen3csp.gatech.edu/k23
- [T10] Harbison-Walker 2005 Handbook (dead link). https://www.mha-net.org/docs/Harbison%20Walker%202005%20Handbook.pdf
- [T11] Morgan JM IFB series (Murugappa copy). https://www.murugappamorgan.com/media/9428/jm-ifb-series_eng.pdf
- [T12] Morgan TJM IFB series. https://www.morganthermalceramics.com/media/9430/tjm-ifb-series_eng.pdf
- [T13] H.S. Walsh TF29 data sheet. https://www.hswalsh.com/usercontent/doc/27326/tf29%20data%20sheet.doc
- [T14] Mathios Firebrick Lava. https://mathios.com/products/firebrick-lava-22x11x6-cm/
- [T15] Castable specification spreadsheet (Google Sheets). https://docs.google.com/spreadsheets/d/0ApMEk9DBqboTdEZQNHpPWkhMX1FLdm00U21LamtrTEE/edit
- [T16] BNZ Blazelite 26 LI sheet https://www.bnzmaterials.com/wp-content/uploads/2021/09/Blazelite-26-LI-AHP-API-936-Compliance-Data-Sheet.pdf ; Morgan Kaolite 2600LI https://morganthermalceramics.com/media/cxtj5iyt/kaolite-2600li-pump_eng.pdf ; Firelite 2600LI https://morganthermalceramics.com/media/d3plff0a/firelite-2600li_eng.pdf
- [T17] BS 1902-5.3:1990 listing. https://store.sfs.fi/en/bs-1902-53-1990
- [T18] AmesWeb, linear thermal expansion of metals. https://amesweb.info/Materials/Linear-Thermal-Expansion-Coefficient-Metals.aspx
- [T19] DroneBot Workshop wiki, A36 CTE. https://wiki.dronebotworkshop.com/wiki/a36-steel-coefficient-of-thermal-expansion.html
- [T20] Matmatch, EN 10216-2 St 45.8. https://matmatch.com/materials/minfm31523-en-10216-2-grade-st-45-8-normalized-or-normalized-formed-n-
- [T21] Patents US3054730A https://patents.google.com/patent/US3054730A/en ; US3962528A https://patents.google.com/patent/US3962528A/en ; US4137037A https://patents.google.com/patent/US4137037A/en
- [T22] Ceramic Arts Daily forum, metal frame for sprung arch kiln. https://community.ceramicartsdaily.org/topic/15978-metal-frame-for-sprung-arch-kiln/
- [T23] ASTM C1045-19 abstract. https://store.astm.org/c1045-19.html
- [T24] ASTM C680-23 abstract https://store.astm.org/c0680-23.html ; JM blog on 3E Plus https://www.jm.com/en/blog/2020/may/2-_why-don-t-you-recommend-naima-s-3eplus-insulation-thickness-c/ ; Insulation Outlook on 3E Plus https://insulation.org/io/?p=7274
- [T25] UL 499, 14th ed., revised 17 Nov 2025 (law.resource.org). https://law.resource.org/pub/us/cfr/ibr/inc/ul/ul.s499.14.2025.pdf (§31.3, Table 36.2, §36.2.1, §53.22, §53.40)
- [T26] ASTM C1055 abstracts. https://store.astm.org/c1055-03.html ; https://webstore.ansi.org/standards/astm/astmc105520
- [T27] Arora et al. 2010, "Accessible hot surfaces and burn hazards", IEEE Chicago PSTC. https://ewh.ieee.org/r4/chicago/pstc/content/Accessible-hot-surfaces-and-burn-hazards.pdf
- [T28] ASTM C1057 abstracts. https://store.astm.org/c1057-92r98e01.html ; https://eshop.normservis.sk/norma/astm-c1057-22-1.5.2022.html
- [T29] EES heat transfer library, FC_plate_vertical_ND. https://fchartsoftware.com/ees/heat_transfer_library/free_convection/hs3025.htm
- [T30] Volupe, Empirical correlations for convective heat transfer coefficients. https://volupe.com/?p=14363
- [T31] `ht` Python library, conv_free_immersed. https://ht.readthedocs.io/en/latest/ht.conv_free_immersed.html
- [T32] MayaHTT TMWizard, horizontal plate pages https://thermal.mayahtt.com/tmwiz/convect/natural/hdp-isot/about.htm ; EngineersEdge https://engineersedge.com/heat_transfer/horizontal_plate_natural_convection_13968.htm
- [T33] A. G. Jaffer, "Natural Convection Heat Transfer From an Isothermal Plate" (Thermo 3, 2023). https://people.csail.mit.edu/jaffer/convect/thermo.pdf
- [T34] EES, Raithby–Hollands tilted plate. https://fchartsoftware.com/ees/heat_transfer_library/free_convection/hs3016.htm
- [T35] EES SF_13 / SF_14. https://fchartsoftware.com/ees/heat_transfer_library/conduction_shape_factors/hs113.htm ; https://fchartsoftware.com/ees/heat_transfer_library/conduction_shape_factors/hs114.htm
- [T36] NPTEL course 112108149, Module 4 worked problems. https://archive.nptel.ac.in/content/storage2/courses/112108149/pdf/M4/WE_M4.pdf
- [T37] IES-VE, Table 23 / CIBSE Guide Table C3.7. https://help.iesve.com/ve2021/table_23_emissivities_of_various_materials__table_c3_7_cibse_guide_.htm
- [T38] NASA NTRS oxidised-metal hemispherical emissivity https://ntrs.nasa.gov/citations/19980228304 ; Sandia 2018 report https://www.sandia.gov/research/publications/details/total-hemispherical-emissivity-of-metals-applicable-to-radiant-heat-testing-2018-11-01/
