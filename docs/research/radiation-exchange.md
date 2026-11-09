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
  in reality, by gas radiation (§4).

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

- **Gas radiation.** CO₂ and H₂O emit and absorb strongly at 1000 °C and above; a gas kiln's
  flame and flue gases do. This needs Hottel's zone method or a mean-beam-length gas emissivity
  (Hottel's charts, or Leckner's correlation). None is in `docs/research/` yet. Until one is,
  the engine leaves gas radiation out and says so (`energyplus-review.md` §4).
- **Emissivity of refractory hot faces at firing temperatures: not found.** A search on
  2026-11-09 found only room-temperature tables, with no temperature or method stated:
  - fireclay brick 0.75 and firebrick 0.68 (ThermoWorks);
  - CIBSE brick 0.93 and ToolBox fire-clay 0.75 (`electric-and-thermal.md` §4.7 note);
  - one maker's statement that refractories' emissivity falls as the temperature rises, with
    fireclay 0.70–0.80 at ambient (Highland Refractory, a coatings seller).

  A measured total hemispherical ε for dense firebrick, IFB, castable and ceramic fibre at
  800–1300 °C is needed before the exchange is coupled in. Possible sources: refractory
  handbooks (Schacht; Harbison-Walker's), NIST/NASA reports, and the makers' sheets. In a nearly
  isothermal chamber the result depends only weakly on ε, but it isn't zero.
- **Kiln wash and glaze on the shelves, and element-wire emissivity** (oxidised Kanthal 0.70 and
  0.88, `electric-and-thermal.md` §1.1, one source only): needed with the ware node and the
  electric heat input.

## Sources

- [R1] J. R. Howell, *A Catalog of Radiation Heat Transfer Configuration Factors*, 3rd ed. online,
  cases C-11 and C-14. https://www.thermalradiation.net/sectionc/C-11.html ;
  https://www.thermalradiation.net/sectionc/C-14.html (formula images
  https://www.thermalradiation.net/images/C-11eq.gif, C-14eq.gif). Read 2026-11-09.
- [R2] J. H. Lienhard V and J. H. Lienhard IV, *A Heat Transfer Textbook*, 6th ed., Phlogiston
  Press, 2024, version 6.00 dated 19 April 2024. §10.3 (pp. 555–566: eqs. 10.12, 10.15, 10.17,
  Tables 10.2–10.3, Exs. 10.1–10.4) and §10.4 (pp. 567–578: eqs. 10.18–10.43, Exs. 10.5–10.9).
  Free PDF:
  https://ahtt.mit.edu/wp-content/uploads/2024/04/AHTTv600.pdf (already [M1] in
  `masonry-materials.md`). Read 2026-11-09.
- [R3] H. C. Hottel and A. F. Sarofim, *Radiative Transfer*, McGraw-Hill (1967), ch. 3. Not read;
  cited by EnergyPlus for ScriptF (`energyplus-review.md` §4).
- ThermoWorks emissivity table, https://www.thermoworks.com/emissivity-table/ ; Highland
  Refractory, https://www.highlandrefractory.com/high-emissivity-coating.html . Room temperature
  only; recorded in §4, not used.
