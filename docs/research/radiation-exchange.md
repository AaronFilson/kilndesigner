# Radiation between the chamber's faces

For proposed item 1 of `energyplus-review.md` §7 and item 6 of
`docs/reviews/2026-11-physics-review-heat.md`: grey-body exchange among the chamber's inside
faces, with exact view factors. Engine: `kilndesigner.thermal.radiation`
(`core/tests/thermal/test_radiation.py`). Read 2026-11-09.

## 1. View factors

### 1.1 The formulas

All three were read in two independent sources, which agree term for term.

| Configuration | Formula | Sources |
|---|---|---|
| Identical parallel rectangles a × b, directly opposed, c apart | X = a/c, Y = b/c; F = 2/(πXY)·{ln[(1+X²)(1+Y²)/(1+X²+Y²)]^½ + X√(1+Y²)·tan⁻¹(X/√(1+Y²)) + Y√(1+X²)·tan⁻¹(Y/√(1+X²)) − X tan⁻¹X − Y tan⁻¹Y} | Howell C-11 [R1]; Lienhard Table 10.3 case 1 [R2] |
| Two rectangles with a common edge ℓ at 90°, widths w (A₁) and h (A₂) | H = h/ℓ, W = w/ℓ; F₁₋₂ = 1/(πW)·{W tan⁻¹(1/W) + H tan⁻¹(1/H) − √(H²+W²) tan⁻¹(H²+W²)^−½ + ¼ ln([(1+W²)(1+H²)/(1+W²+H²)]·[W²(1+W²+H²)/((1+W²)(W²+H²))]^W²·[H²(1+H²+W²)/((1+H²)(H²+W²))]^H²)} | Howell C-14 [R1]; Lienhard Table 10.3 case 2 [R2] |
| Coaxial parallel discs r₁, r₂, h apart | R₁ = r₁/h, R₂ = r₂/h, X = 1 + (1+R₂²)/R₁²; F₁₋₂ = ½[X − √(X² − 4(R₂/R₁)²)] | Lienhard Table 10.3 case 3 [R2] |

Howell's catalogue gives each formula as an image. The page sources reference
`../images/C-11eq.gif` and `C-14eq.gif`; the images were downloaded and read on 2026-11-09. Howell
cites Hottel (1931), Hamilton and Morgan (no year given on the page) and Camaraza-Medina,
Hernandez-Guerrero and Luviano-Ortiz (2022) for both.

### 1.2 Checks against published numbers

- Adjoining unit squares: 0.20 (Lienhard Ex. 10.2, read off Fig. 10.9). The formula gives 0.20004.
- Squares along a shared edge twice their side: Fig. 10.9 reads 0.245, and Ex. 10.2 gets 0.045
  for the offset squares. The formula gives 0.2406 and 0.0406, which agree to the chart's reading.
- Coaxial discs R₁ = 0.25, R₂ = 0.5: 0.192 (Lienhard Ex. 10.3). The formula gives
  X = 21, F = ½(21 − √425) = 0.1922.
- A cube: each face sees the opposite one with 0.19982 and each neighbour with 0.20004. The row
  sums to 1.0000, so the two formula families close together.
- Parallel rectangles against direct integration of Lienhard eq. 10.17a (midpoint rule): within
  0.2 %.

### 1.3 View-factor algebra

- **Summation:** Σⱼ Fᵢⱼ = 1 over an enclosure (Lienhard eq. 10.12).
- **Reciprocity:** AᵢFᵢⱼ = AⱼFⱼᵢ (eq. 10.15).
  The engine refuses any enclosure that breaks either rule by more than 10⁻⁹ (ADR 0009).
- **A concave face over an opening** (an arch or dome over the springline) sees what the opening
  sees. Treat the opening as a plane surface (Lienhard Ex. 10.1, the slit; Ex. 10.3, the shield's
  open top). Then:
  - F_cover→j = (A_open/A_cover)·F_open→j
  - F_cover→cover = 1 − A_open/A_cover

  This follows from summation and reciprocity, with F_open→cover = 1. It is exact when the
  radiosity is uniform over the cover; the method assumes that for every face anyway.

## 2. Grey-body exchange (net radiation method)

Lienhard §10.4 [R2], after Oppenheim (1956). The method assumes:

- every face is diffuse, grey and opaque (ε = α, ρ = 1 − ε);
- each face has one temperature and one radiosity;
- the view factors are known;
- the medium is transparent and doesn't radiate.

The equations:

- eq. 10.42: Bᵢ = (1 − εᵢ) Σⱼ Fᵢⱼ Bⱼ + εᵢσTᵢ⁴, for a face of known temperature;
- eqs. 10.39 and 10.41: qᵢ = Bᵢ − Σⱼ Fᵢⱼ Bⱼ. For a face of known flux this is the equation that
  holds. q = 0 is Lienhard's insulated "refractory surface", which re-radiates everything it
  absorbs;
- a face's temperature back from B and q: σT⁴ = B + q(1 − ε)/ε (eq. 10.39).

The same algebra is EnergyPlus's ScriptF method (Hottel & Sarofim ch. 3, via
`energyplus-review.md` §4). Writing it in radiosities, as Lienhard does, needs no matrix
inverse beyond one linear solve.

Checks against Lienhard's own worked examples (tests):

- **Ex. 10.9(a)**, two strips 1 m wide and 2.4 m apart (ε 0.3 and 0.5, 400 K and 300 K) with black
  surroundings at 250 K. Book: B = 612.1 and 379.5 W/m², Q₁₋₂ = 46.53 W/m.
- **Ex. 10.9(b)**, the same strips with an insulated reflector. Book: B = 987.7, 657.4 and
  822.6 W/m², Q = 198 W/m, reflector at 347 K.
- The engine agrees to within 0.1 %. Lienhard rounds his coefficients to two places and takes
  σ = 5.67 × 10⁻⁸, so the book itself is only that precise.
- **Eq. 10.27**, an enclosed convex body: Q = A₁σ(T₁⁴ − T₂⁴)/[1/ε₁ + (A₁/A₂)(1/ε₂ − 1)]. The
  engine matches it exactly.

## 3. What the engine has, and what's still to build

**Built:** `parallel_rectangles`, `perpendicular_rectangles`, `coaxial_discs`, `box` (six faces,
all from C-11 and C-14), `covered` (a concave roof over its opening), `exchange` (temperatures
or fluxes given per face) and `surface_temperature`.

**Not built yet: coupling into the firing simulation.** `simulation.py` holds every hot face at
one chamber temperature, and between equal temperatures radiation exchanges nothing. For the
exchange to matter, each face's hot face needs its own temperature. That means deciding where
the heat enters:

- **Electric:** the elements sit in grooves in particular walls, and their watts go into those
  faces.
- **Gas:** the heat goes into the combustion gas, which gives it to the faces by convection and,
  in reality, by gas radiation (§6).

That decision is recorded as a question in `docs/planning/11-09-26.md`.

**Shapes.** `box` covers a rectangular chamber, and `covered` covers one under a sprung arch or
sail dome (the arch over the opening at the springline). Not covered yet:

- **The end walls' segments above the springline under an arch.** Those segments are counted
  in the back and front faces' areas. Their view factors would have to be split from the
  cover's.
- **Round chambers.** The disc formula above gives floor ↔ roof; the wall follows by summation.
  The four quarter walls among themselves need the cylinder's own factors, from Howell's
  catalogue (not read).
- **Catenary, crossing-vault, curved-plan and row chambers.** These need their own factors. An
  engine that meets one should refuse rather than fall back on EnergyPlus's area-proportional
  approximation (`energyplus-review.md` §4 calls that approximation crude for a box with a ware
  stack).

**The ware stack.** A stack is an obstruction inside the enclosure, and closed-form factors don't
exist for it. Options: the stack as a box inside the box, its faces seeing the walls through the
gaps by the crossed-strings rule in plan; or a ware node with an enclosing-body approximation
(eq. 10.27). Not yet chosen or sourced.

## 4. Gaps

- **Hot-face emissivities: partly found (§5).** Dense fire brick, insulating firebrick and fibre
  board have measured emissivities against temperature. Still missing:
  - **The alumina bands of Osborn's three fire-brick classes.** Neither compilation defines
    "low", "medium" and "high" Al₂O₃. A kiln's dense brick (HWI KX-99 at 42 % Al₂O₃, Allied
    medium-duty at 32.9 %, `electric-and-thermal.md` §4.2) could fall in the low class
    (ε₀ 0.75–0.79 at 1073–1473 K) or the medium one (0.55–0.63), a difference that matters.
    Osborn (1985) itself is needed.
  - **IFB above 1350 K (1077 °C): to be searched for.** There are no data, and cone 10 is near
    1285 °C. Until data are found, the engine extrapolates the measured lines (the user's
    decision, 2026-11-09; §5.5). The chemistry of the IFBs kilns use (K-23, K-26, JM 23, JM 26)
    isn't recorded in `docs/research/`, so they can't yet be matched to a measured grade in §5.2.
  - **Castables, kiln wash, glazed ware and element wire** (oxidised Kanthal 0.70 and 0.88,
    `electric-and-thermal.md` §1.1, one source only): no high-temperature data found.
  - **Touloukian and DeWitt vol. 8 (1972) has no brick emissivity.** Its master index (vol. 14,
    DTIC ADA129117, public on archive.org as `DTIC_ADA129117`; index pp. 12, 32–33, 80, 117,
    138, read 2026-11-09) shows this:
    - every brick, firebrick, IFB and "aluminosilicate refractories" entry has conductivity
      (vol. 2) or diffusivity (vol. 10) data only, and none in vol. 8;
    - the nearest material is mullite (aluminium silicate), the main fired phase of
      alumina-silica brick: emissivity on vol. 8 pp. 1685 and 1687, reflectivity on p. 618. A
      dense mineral is only a guide to a porous brick's face.

    Where to get vol. 8: DTIC (ADA951942; the page was down for maintenance on 2026-11-09, and
    DTIC refuses scripted downloads), or a borrow-only scan on archive.org
    (`thermophysicalpr0008purd`).
- **Gas radiation: a method is sourced (§6), but its correlations are not in hand.** Lienhard
  gives the method and charts; coding it needs the correlations themselves (Alberti et al.,
  with the authors' spreadsheets) or a weighted-sum-of-grey-gases table. Until then the engine
  leaves gas radiation out and says so.
- **Soot.** Luminous flames radiate mainly from soot, not from CO₂ and H₂O (Lienhard p. 594):
  wood firing, and gas in reduction. No soot model is sourced.

## 5. Hot-face emissivities at firing temperatures

Read 2026-11-09. The user's note: firebrick and IFB have changed little in 30–40 years, so the
older measurements below (1978–1994) still apply.

**What is given, and how it converts.**
- Values are total *normal* emissivity ε₀ unless marked. For insulators the hemispherical value
  is 0.95–1.0 of the normal (Jones et al. [R6] Fig. 6, after Hottel and Sarofim [R3]).
  `thermal-properties.md` §7 gives 0.95 for smooth and 0.98 for rough non-metals (CIBSE).
- Refractories emit and reflect diffusely ([R6] §4, citing Hottel and Sarofim and Hampartsoumian),
  as the enclosure model assumes.
- They are not grey. Their spectral emittance is low (under about 0.6) at wavelengths below
  5–6 µm, where a hot surface emits most. So their total emissivity falls as the temperature
  rises: above about 1000 K, light-coloured refractories fall to about 0.3–0.4 ([R6] §3, items
  4–5).
- Treating a face as grey at its own temperature is still reasonable when the surfaces
  exchanging heat are close in temperature. Lienhard (p. 554, citing his [10.2]) gives up to
  about a 30 % difference in absolute temperature for common materials, but only 10 % for
  highly selective ones.

**The correlation** (IFRF CF148 eq. 1 [R5]; Jones et al. eq. 7 [R6]):
ε₀(T) = a + 10⁻⁵·b·T + 10⁻⁸·c·T² + 10⁻¹⁰·d·T³, with T in K, valid only within the stated range.
The ε₀ columns below are computed from these coefficients.

### 5.1 Dense brick

| Material | a | b | c | d | Range (K) | ε₀ at 1073 / 1273 / 1473 K | Source |
|---|---|---|---|---|---|---|---|
| Fire brick (Al/Si/Fe/O), low Al₂O₃ | 0.90 | −10 | | | 673–1673 | 0.79 / 0.77 / 0.75 | Osborn 1985, via [R5], [R6] |
| Fire brick, medium Al₂O₃ | 0.84 | −20 | | | 673–1673 | 0.63 / 0.59 / 0.55 | as above |
| Fire brick, high Al₂O₃ | 0.80 | −20 | | | 673–1673 | 0.59 / 0.55 / 0.51 | as above. The printed range, 0.64–0.39, doesn't match these coefficients (0.665–0.465): unresolved |
| Fired clay, 63.2 % Al₂O₃, 32.1 % SiO₂ | 0.74 | 133 | −268 | 11.8 | 300–1300 | 0.54 / 0.52 / – | Jackson, Romero and Norris 1994, via [R6] |

Single points from Sparrow and Cess (1978), through Lienhard Table 10.1 [R2]:
- fireclay brick 0.75 at 980 °C;
- silica brick 0.80–0.85 at 980 °C;
- "ordinary refractory" 0.59 at 1090 °C;
- "white refractory" 0.29 at 1090 °C;
- magnesite refractory 0.38 at 980 °C.

Lienhard doesn't say whether these are normal or hemispherical.

Check: the low-alumina fire-brick line gives 0.775 at 980 °C (1253 K), against Sparrow and Cess's
0.75 for fireclay brick, 3 % apart.

### 5.2 Insulating firebrick

Morgan's MPK lightweight refractories, ε₀ = a + 10⁻⁵·b·T. Measured by Hampartsoumian (1990), via
[R6] Table A2; IFRF CF148 [R5] cites the same data to Gray et al. (1989) and Hampartsoumian
(1990).

| Grade (chemistry, wt %) | a | b | Range (K) | ε₀ at the range's ends |
|---|---|---|---|---|
| MPK 110 (20 Al₂O₃, 53 SiO₂, 4 Fe₂O₃, 16 MgO) | 0.43 | 14.4 | 1073–1300 | 0.58 → 0.62 |
| MPK 125 (36 Al₂O₃, 46 SiO₂, 15 CaO) | 0.53 | 8 | 1063–1350 | 0.62 → 0.64 (printed 0.54–0.64: the low end disagrees) |
| MPK 140 (41 Al₂O₃, 54 SiO₂) | 0.21 | 25.3 | 1073–1350 | 0.48 → 0.55 |
| MPK 155HA (61 Al₂O₃, 36 SiO₂) | 0.75 | −27.9 | 1063–1350 | 0.45 → 0.37 |
| MPK 130HSR (36 Al₂O₃, 54 SiO₂) | 0.61 | – | 1073–1250 | 0.61 |
| MPK SUPRA (11 Al₂O₃, 75 SiO₂, 6 Fe₂O₃) | −0.16 | 74 | 1073–1300 | 0.63 → 0.80 |

- IFB runs 0.37–0.64 over 790–1077 °C. That is below dense fireclay brick (0.77–0.79 at those
  temperatures, §5.1, low-alumina class). The iron-bearing grades are the highest.
- The data stop at 1350 K (1077 °C).
- The compilations give neither the density nor the classification temperature of these grades.
- IFRF's Fig. 1 band for "light weight refractory" falls from about 0.6 at 750 K to about 0.3 at
  1150 K. That doesn't sit where its own table puts these grades, and the page's reference
  numbers are inconsistent: the figure cites a ref. 14 that isn't listed. The table is used here;
  the figure is not.

### 5.3 Ceramic fibre

| Material | a | b | c | Range (K) | ε₀ at 1073 / 1273 / 1400 K | Source |
|---|---|---|---|---|---|---|
| Fibre board, 45 % Al₂O₃, 55 % SiO₂, fibres normal to the face | 1.27 | −48.5 | 2.84 | 600–1400 | 0.78 / 0.70 / 0.65 | Fletcher and Williams 1984, via [R6] |
| The same board, parallel bonded fibres | 1.47 | −91.1 | 14.4 | 600–1400 | 0.66 / 0.54 / 0.48 | as above |
| Kaowool blanket, 45 % Al₂O₃, 55 % SiO₂ | 2.39 | −165 | – | 923–1173 | 0.62 at 1073 K; 0.45 at 1173 K (printed 0.40) | Hampartsoumian 1990, via [R6] |

Jones et al. report a suggestion: furnaces lined with fibre and run continuously have sometimes
saved less energy than expected, and the fibre's low emissivity has been suggested as the cause
([R6] §1, citing Elliston et al. 1987).

### 5.4 Kiln furniture and oxides

All via [R6] Table A2.

- **Silicon carbide:** ε₀ = 0.8 + 15.4·10⁻⁵T − 9.01·10⁻⁸T², 400–1850 K. That gives 0.85, 0.83 and
  0.82 at 1273, 1473 and 1573 K (Touloukian and DeWitt vol. 8).
- **SiC oxidised for 1 h at 1367 K:** ε₀ = 0.7 − 25·10⁻⁵T, 800–1600 K, giving 0.38 at 1273 K and
  0.31 at 1573 K. The compilation gives no source for this row.
- Which shelf (oxide-bonded, nitride-bonded, recrystallised) follows which line isn't known.
- **Alumina:** ε₀ = 0.98 − 53·10⁻⁵T + 10.2·10⁻⁸T², 300–1800 K, giving 0.47 at 1273 K and 0.40 at
  1573 K (Touloukian and DeWitt vol. 8).
- Grain size matters. At 1200 °C, Al₂O₃ measures 0.35 (2–25 µm grains), 0.43 (15–80 µm) and
  0.53 (90–120 µm) ([R6] Table 2, after Hottel and Sarofim).

### 5.5 For the coupling (not built)

**Each face's emissivity:** its hot-face material's line, at its own temperature, times 0.95–1.0
for the hemispherical value.

**Decided (the user, 2026-11-09): extrapolate.** The IFB data end at 1077 °C, but IFB is used
well past that.
- K-26 and JM 26 are classified to 1430 °C (2600 °F) (`electric-and-thermal.md` [S31]); cone 10
  is 1285–1305 °C (`core/src/kilndesigner/data/cones.yaml`).
- Refusing would stop most IFB kilns' simulations. So the engine evaluates the measured line past
  its range, says in the working that it has, and names the measured range.
- This is the user's exception to ADR 0009's refusal, for this property. More data are to be
  searched for (§4; `docs/planning/02-plan.md`, follow-up research).

**What the lines give at cone 10** (1558 K):
- MPK 110: 0.65; MPK 125: 0.65; MPK 140: 0.60; MPK 130HSR: 0.61.
- MPK 155HA: 0.32.
- MPK SUPRA: 0.99. Its steep line, measured only to 1300 K, runs away when extrapolated; treat it
  with caution.

**The same rule for fibre** (applied here; the user may say otherwise). Fibre board was measured
to 1400 K (1127 °C), but blankets and boards are used higher. Extrapolated to 1558 K: 0.58 for
fibres normal to the face, 0.40 for parallel ones. Kaowool's steep line was measured only to
1173 K; extrapolated, it falls to zero by 1448 K, so it can't be used past its range.

**Proposed: which line stands for a kiln's IFB.** Which MPK grade represents K-23, K-26 or JM 23
waits on those bricks' chemistry (§4). Until then the coupling would show the spread across the
grades.

**Effect.** In a nearly isothermal chamber, ε matters little to the total exchange. It matters
more to how fast a cold face (the floor, the door) catches up.

## 6. Gas radiation (Lienhard §10.5, pp. 586–594)

**The method: Hottel's framework.**
- **Gas emissivity:** ε_g = ε₀(p_aL, T_g)·C(p, p_aL, T_g) (eq. 10.56). ε₀ is charted for CO₂
  (Fig. 10.22) and H₂O (Fig. 10.23). The charts come from Alberti, Weber and Mancini's
  correlations, fitted to the HITEMP-2010 database (CO₂ 2015, H₂O 2016), and the authors provide
  spreadsheets. C is a pressure correction (Figs. 10.24 and 10.25).
- **CO₂–H₂O overlap:** the correction is ≲ 0.01 below about 10 bar-cm and 10 atm (Alberti et
  al. 2018).
- **Absorptance of wall radiation:** α_g = ε_g(p_aL·T_w/T_g, p, T_w)·(T_g/T_w)^½ (eq. 10.57).
  The exponent ½ follows Edwards and Matavosian (1984); Hottel used 0.65 for CO₂ and 0.45 for
  H₂O.
- **Mean beam length:** L₀ = 4V/A (eq. 10.58), or 3.6V/A for a strongly absorbing gas (Howell,
  Mengüç and Siegel). Table 10.4: a cube of side ℓ has L₀ = 2ℓ/3.

**Check case: Example 10.11.**
- **Setup:** CO₂ at 0.2 atm in N₂, in a cylinder 40 cm across (L₀ = 40 cm); gas at 1200 °C;
  black walls at 300 °C.
- **Gas emissivity:** p_aL = 8.11 bar-cm, ε₀ = 0.084 and C ≈ 1, so ε_g = 0.085.
- **Gas absorptance:** α_g = 0.12.
- **Net heat to the walls:** 27 kW per metre.

**Limits.**
- Lienhard calls the mean beam length and the scaling rule "simple but crude"; band models, the
  zonal method and Monte Carlo are more accurate.
- Soot, not gas, carries most of a luminous flame's radiation.

**Next step:** get Alberti et al.'s correlations (or their spreadsheets) in hand and read them
at the page. The charts alone aren't enough to code.

## Sources

- [R1] J. R. Howell, *A Catalog of Radiation Heat Transfer Configuration Factors*, 3rd ed. online,
  cases C-11 and C-14. https://www.thermalradiation.net/sectionc/C-11.html ;
  https://www.thermalradiation.net/sectionc/C-14.html (formula images
  https://www.thermalradiation.net/images/C-11eq.gif, C-14eq.gif). Read 2026-11-09.
- [R2] J. H. Lienhard V and J. H. Lienhard IV, *A Heat Transfer Textbook*, 6th ed., Phlogiston
  Press, 2024, version 6.00 dated 19 April 2024. Table 10.1 (p. 546) and the grey approximation
  (p. 554); §10.3 (pp. 555–566: eqs. 10.12, 10.15, 10.17, Tables 10.2–10.3, Exs. 10.1–10.4);
  §10.4 (pp. 567–578: eqs. 10.18–10.43, Exs. 10.5–10.9); §10.5 (pp. 586–594: eqs. 10.56–10.58,
  Table 10.4, Ex. 10.11). Free PDF:
  https://ahtt.mit.edu/wp-content/uploads/2024/04/AHTTv600.pdf (already [M1] in
  `masonry-materials.md`). Read 2026-11-09.
- [R3] H. C. Hottel and A. F. Sarofim, *Radiative Transfer*, McGraw-Hill (1967), ch. 3. Not read;
  cited by EnergyPlus for ScriptF (`energyplus-review.md` §4).
- [R4] E. M. Sparrow and R. D. Cess, *Radiation Heat Transfer*, Hemisphere, 1978: the source of
  Lienhard's Table 10.1 (his ref. [10.1]). Not read directly.
- [R5] N. Fricker, "What data is available on the emissivity of firebrick and refractories as a
  function of temperature?", IFRF Combustion Handbook, Combustion File 148, posted 3 March 2003.
  The data were first published as E. Hampartsoumian, D. Hainsworth, J. M. Taylor and
  A. Williams, "The radiant emissivity of some materials at high temperatures — review",
  J. Inst. Energy 74(500) (2001) 91–99. https://ifrf.net/?p=8893 (Fig. 1:
  https://ifrf.net/wp-content/uploads/2018/09/148-Fig1.jpg). Read 2026-11-09.
- [R6] J. M. Jones, P. E. Mason and A. Williams, "A compilation of data on the radiant
  emissivity of some materials at high temperatures", J. Energy Inst. 92(3) (2019) 523–534,
  doi:10.1016/j.joei.2018.04.006. The accepted manuscript is open (CC BY-NC-ND 4.0):
  https://eprints.whiterose.ac.uk/133266/ . Read for §1, §3, §4, Fig. 6, Tables 1–2 and
  Table A2, 2026-11-09.

  The primary sources behind §5, not read and cited through [R5] and [R6]:
  - P. D. Osborn, *Handbook of Energy Data and Calculations*, Butterworth, 1985;
  - E. Hampartsoumian, "Spectral emittance measurements of furnace wall materials and
    coatings", Ceramics in Energy Applications Conf., Sheffield, IOP, 1990, 149–157;
  - W. A. Gray, E. Hampartsoumian, J. M. Taylor and A. Williams, Proc. 1989 Int. Gas Res.
    Conf., vol. III, 26–34;
  - J. D. Fletcher and A. Williams, "Emissivities of ceramic fibre linings for high-temperature
    furnaces", J. Inst. Energy (1984) 377;
  - J. D. Jackson, E. Romero and J. J. Norris, Ceramics in Energy Application, Inst. Energy,
    1994, 133–148;
  - Y. S. Touloukian and D. P. DeWitt, *Thermal Radiative Properties: Nonmetallic Solids*, TPRC
    Data Series vol. 8, IFI/Plenum, 1971/1972 (DTIC ADA951942);
  - D. G. Elliston et al., J. Inst. Energy (1987) 155–167.
- [R7] Gas radiation, through Lienhard [R2] §10.5 (his refs. [10.15]–[10.18]); not read:
  - M. Alberti, R. Weber and M. Mancini, Combust. Flame 162(3) (2015) 597–612 (CO₂) and 169
    (2016) 141–153 (H₂O);
  - M. Alberti, R. Weber and M. Mancini, J. Quant. Spectrosc. Radiat. Transf. 205 (2018)
    230–240 (overlap);
  - D. K. Edwards and R. Matavosian, J. Heat Transfer 106(4) (1984) 684–689.
- ThermoWorks emissivity table, https://www.thermoworks.com/emissivity-table/ ; Highland
  Refractory, https://www.highlandrefractory.com/high-emissivity-coating.html . Room temperature
  only; not used.
