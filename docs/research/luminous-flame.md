# The luminous flame: soot in wood and oil flames

v2's heat model radiates CO₂ and H₂O only (Bordbar 2014's WSGG, `11-09-26.md` step 4). Soot is not
counted, and the owner's heat question 4 asks whether to carry it as a stated band or leave it out and
say so (`thermal-combinations.md` question 3; `thermal-software.md` §6.4; `radiation-exchange.md` §6).
This file collects what open sources give for the soot of wood (biomass) and oil flames, the models
that turn soot into an absorption coefficient or an emissivity, and the options.

Read 2026-11-10. Marks: **Read** (on the fetched page or PDF, from its extracted text or a rendered page;
values taken off a figure say so and carry about one minor division), **Snippet** (a search-result
snippet only), **Derived** (arithmetic here, working shown; the script is
`scratch/luminous-flame/tools/calc.py`, git-ignored). Quotes are as the page gave them. Could not be
read: HAL (a bot wall), RECERCAT and CORE (HTTP 403), CSIRO Publishing (404 after its redirect), Springer
and ACS (sign-in redirects), the Utah AFRC archive (HTTP 418), and one Lund thesis (over 60 MB). See the
last section.

## Short answer

| Flame | Quantity | Value or band | Conditions | Source | Mark |
|---|---|---|---|---|---|
| Pine-wood pellet, volatiles flame | f_v | peak 1.21 ppm; peak path-average 0.61 ppm | one pellet in CH₄ post-flame gas at 1300 K; flame ≤ 1874 K; emission spectrometry + camera | [W1] | Read |
| Stem wood, entrained-flow gasifier | f_v | 1.0 ppm at φ 0.5 (peat 0.6); falls as φ rises over 0.35–1.2 | 0.1 MW reactor core, TDLAS | [W2] as cited in [W1] | Read (as cited) |
| Biomass powder near stoichiometric | "soot volume fraction" | about 0.17 (jet) and 0.09 (swirl) at λ ≈ 0.8, about 0 at λ 1.0; **no unit printed** | 0.1 MW reactor, air | [W3] | Read (off a slide) |
| Pine-needle fire | f_v | peak 6.8 ppm, persistent flame | 50–170 kW, flames 1–2 m | [W4] | Read (abstract) |
| Wood pellets, 400 kW grate furnace | particle radiation | "doubles the wall irradiation in the hot flame zone" against gas alone | measured and modelled | [W5] | Read |
| Heavy oil C, 800 kW, 3 × 3 × 6 m furnace | f_v | 4×10⁻⁸ to 3×10⁻⁷ in the flame; 9×10⁻⁹ to 1×10⁻⁸ near the flue; KL 0.25–0.8 | λ 1.2, laser extinction | [O2] | Read |
| Light and heavy oils, 0.5 m furnace | soot, mg/Nm³ | ≈ 7000 at λ 0.64 to 200–1450 at λ 1.0; heavy oil B 150–500 to λ 1.75 | as Rayleigh soot at 1500 K: 0.71 → 0.02–0.15 ppm (Derived) | [O1] Fig. 7 | Read (off the figure) |
| Oils and city gas, 0.5 m furnace and IJmuiden | ε_soot/ε_gas | heavy oil 2.0–2.9 at λ 0.66–0.98, 0.1–1.75 at λ 1.0–1.05, 0.4–0.6 to λ 1.7; light oil 1.35–1.6 at λ 0.76 → 0.15–0.3 at 0.9; city gas 1.0 at 0.8 → 0.03 at 1.47 | furnace scale "can be neglected" (the authors) | [O1] Fig. 14 | Read (off the figure) |
| Propane swirl flame, 80 kW | f_v | about 65 ppb with the primary air closed; "very few soot particles" with it open | SMPS sampling | [W6] | Read |
| Vegetation fires, 0.2–4.2 m deep | grey extinction K | 0.7 m⁻¹ (another study 0.72) | IR bands | [E1], [E2] | Snippet |
| Wood cribs | ε | 0.1–0.6 at 0.25–1.9 m thick, 650–1300 °C | burnout tests | [E3] | Snippet |
| Pulverised wood, 130 kW | effective ε | particles 0.17, gas 0.12 in the luminous zone | line-of-sight emission | [E4] | Snippet |
| Any soot, Rayleigh, grey | κ/(f_v T), m⁻¹K⁻¹ | 1817 [L2]; 1800 [L3]; 1285–1336 over 800–1500 K [L1]; 985–1996 for C 3.7–7.5 | Planck mean | [L1]–[L4] | Read; Derived |
| A kiln flame, any fuel; reduction firing | f_v, KL or ε | **not found** | | | |

## 1. Soot volume fractions measured

### Wood and biomass

**[W1] Yan, W., Li, K., Yu, T., Huang, X., Yu, L., Panahi, A. and Levendis, Y. A., "Determination of
Flame Temperatures and Soot Volume Fractions during Combustion of Biomass Pellets"**, Energy & Fuels
35 (2021) 2313–2325, doi:10.1021/acs.energyfuels.0c03921; the publisher's PDF on NSF's public-access
repository, <https://par.nsf.gov/servlets/purl/10251502>. Pine-wood, rice-straw and corn-stalk pellets
"were ignited and burned in the post-combustion zone of methane gas at 1300 K" (p.2313); flame spectra
(500–800 nm) and a camera with a 615/517 nm filter give T and f_v. "The peak soot volume fractions of
pine wood, rice straw, and corn stalk are 1.21 (at 6.84 s), 1.19 (at 6.16 s), and 1.16 ppm" (p.2319);
"The peak average soot volume fractions ... were 0.61, 0.57, and 0.49 ppm" (p.2321); maximum flame
temperatures 1874, 1878 and 1878 K (p.2319). It cites (p.2314) the same group's 2020 paper: "the average
emissivity of biomass volatile flames was determined to be 0.16 at an equivalence ratio of φ = 0.91,
whereas it was 0.10 at an equivalence ratio of φ = 0.71" (400–700 nm, a visible-band value).

**[W2] Sepman, A., Ögren, Y., Qu, Z., Wiinikka, H. and Schmidt, F. M.**, Proc. Combust. Inst. 36 (2017)
4541–4548 (TDLAS in the core of an entrained-flow biomass gasifier), as [W1] cites it (p.2314): "the
soot volume fraction decreases with the increasing equivalence ratio (in the range of φ = 0.35−1.2)
during the combustion of stem wood and peat. Under the equivalence ratio of φ = 0.5, the soot volume
fraction generated by the combustion of stem (mixed by pine and spruce) wood (fv = 1.0 ppm) was higher
than that of peat (f v = 0.6 ppm)." φ here rises with air, as λ does: an inference, since soot falls
as φ rises and [W3] names the group's ratio "O2-to-fuel equivalence ratio (lambda)". The paper itself
was not read.

**[W3] Schmidt, F., Qu, Z., Valiev, D., Thorin, E., Sepman, A. and Wiinikka, H., "TDLAS-based in situ
measurements of potassium in entrained flow gasifiers"**, IEA Bioenergy Task 33 workshop slides, 2019,
<https://task33.ieabioenergy.com/wp-content/uploads/sites/33/2022/07/Schmidt-SFC-Umea.pdf>. Slide 10: the
reactor is 4 m long, "Operated at 0.1 MWth". Slide 18, "Soot vs. lambda", reactor port, air: soot volume
fraction about 0.17 (jet burner, λ 0.83) and 0.09 (swirl, λ 0.79), falling to about 0 at λ 1.0 (off the
figures); lower with 30 and 40 % O₂; "Less soot for swirl burner". **The axis has no unit.** The paper
behind it, Sepman et al., Energy & Fuels 33 (2019) 11795 ([W1] ref. 29), was not read.

**[W4] Dupuy, J.-L., Vachet, P., Maréchal, J., Meléndez, J. and de Castro, A. J., "Thermal infrared
emission-transmission measurements in flames from a cylindrical forest fuel burner"**, Int. J.
Wildland Fire 16(3) (2007) 324–340; abstract at <https://www.frames.gov/catalog/45982>. Pinus pinaster
needles in wire baskets 20–40 cm across, "between 50 and 170 kW", flames 1–2 m; camera 7.5–13 µm;
"radiation was dominated by soot in the spectral range of the camera, but that radiation from gaseous
products of the combustion was not negligible"; soot volume fractions "peaked at 6.8 x 10-6 in the
persistent region of the flame".

**[W5] Hofgren, H., *Modelling and Experimental Investigations on Thermal Radiation in Combustion
Environments***, PhD thesis, Lund University, 2015, <https://lup.lub.lu.se/search/files/5546431/5384281.pdf>.
A 400 kW grate-fired test furnace on "regular wood pellets", about 100 kg/h (p.42); particles sampled in
the hot flame zone were "assumed to be soot" (p.44); abstract (p.ii): "particle radiation is very
important in the evaluated furnace, it doubles the wall irradiation in the hot flame zone compared with
irradiation only from gases." No f_v: the particles are a mass–size distribution in mg/Nm³ (Fig. 4.2).

**[W6] Gunnarsson, A., *Experimental and numerical studies of thermal radiation in gas, coal and
co-fired pilot test facilities***, Licentiate thesis, Chalmers, 2017,
<https://publications.lib.chalmers.se/records/fulltext/249422/249422.pdf>. A rotary-kiln test furnace (400
then 580 kWth) on coal and on 30 % wood (steam-exploded; ground and pelletised): "it was shown by modeling
that the heat transfer from the flame was dominated by the particles"; "The oil and gas flames were
shorter than any of the solid fuel flames" (p.6). No f_v for the wood flames. The 80 kW air–propane swirl
flame: with the primary-air valve open "very few soot particles were observed" (p.8); closed, "the soot
volume fraction at port M3 was estimated to be about 65 ppb for the sooty flame" (SMPS, p.36).

### Oil

**[O1] Sato, T. and Kunitomo, T., "Experimental Study on Luminous Flame"**, Memoirs of the Faculty of
Engineering, Kyoto University 31(1) (1969) 47–69, open access, <http://hdl.handle.net/2433/280762>. The
oil furnace is 2.7 m long and 0.5 m square, brick floor and roof, water-cooled sides with cold black-body
cavities opposite the windows (p.48); city gas burns in a 0.4 m tube. High- and low-pressure air-atomising
burners; diesel light oil (s.g. 0.805), heavy oils A (0.85) and B (0.92); "about 60 kinds of luminous
flames" (p.51); 4.5–10.3 kg/h at air ratios 0.84–1.46 in Table 2 (p.52); soot by a soot collector, the
flame emissivity by a radiation pyrometer (p.51). Fig. 7 (p.60), soot C_N in mg/Nm³ off the figure: 7000
at λ 0.64 (low-pressure burner, heavy oil A), 2000–4000 at λ 0.7–0.8, 200–1450 at λ 1.0, heavy oil B
150–500 over λ 1.1–1.75. "in the case of the heavy oil, even at the air excess ratio greater than 1.0,
the soot formation is very strong and does not approach to zero"; "in the city gas flame, the soot
concentration becomes zero at the air excess ratio greater than 1.5. However, the soot formation is as
strong as that in the liquid fuel flame at the air excess ratio smaller than 1.0", with a burner chosen
to be "easy to use for the observation of the soot formation" (p.60). Particles span "0.02µ~10µ", with
hollow "bee-hive like" ones from oil (p.61); the scatter in emissivity "is caused mainly by the
differences of the soot particle diameter" (p.65).
Derived: as Rayleigh soot, f_v = C_N·(273.15 K/T)/ρ_s with ρ_s = 1800 kg/m³ [L3]; at 1500 K, 150 mg/Nm³
→ 0.015 ppm, 500 → 0.051, 1000 → 0.10, 1450 → 0.15, 2000 → 0.20, 4000 → 0.41, 7000 → 0.71. Large
particles radiate less than Rayleigh soot of the same mass, so these overstate the radiating soot.

**[O2] Ishii, K., Tsuboi, T., Okada, K., Ishioka, M. and Suzukawa, Y., "Soot Measurement in a Tubular
Flame Burner for Heavy Oil"** (Japanese), JSME Thermal Engineering Conference 2005, paper B122, pp.55–56,
doi:10.1299/jsmeted.2005.55 (free on J-STAGE). JFE Steel's furnace, 3 m × 3 m × 6 m; C heavy oil, 800 kW,
air ratio 1.2, air at 400 °C, one- or two-stage air (p.55). Table 1 (p.56), f_v by He–Ne laser
extinction, cm³/cm³: one-stage 4×10⁻⁸ at window 2 (path 0.36 m, the flame's width) and 1×10⁻⁸ at window
5 (path 3 m); two-stage 3×10⁻⁷ and 9×10⁻⁹. The window-5 figure agrees with the flue's smoke meter. KL
0.25–0.8 (against 1.0–3.0 in a small furnace on A heavy oil), soot at about 1580 K; even at window 2 the
soot cloud is not optically thick enough to treat as a black body (p.56; translated here).

## 2. Luminous emissivities measured or recommended

- **[O1] Fig. 12 (p.65)**: the soot cloud's emissivity, ε_s = 1 − (1 − ε_t)/(1 − ε_g) (p.51), runs from
  0 to about 0.5 in the 0.5 m furnace; IJmuiden's and Sheffield's results fall in the same scatter.
- **[O1] Fig. 14 (p.67), the ratio rule**, mean ε_s/ε_g against air ratio, off the figure: heavy oil A
  2.0–2.45 at λ 0.66–0.69, 1.1–1.45 at 0.82–0.85, 0.1–0.3 at 1.0–1.07; heavy oil B 2.8–2.9 at λ 0.97,
  0.3–1.75 at 1.0–1.05, 0.4–0.6 flat over 1.15–1.7; light oil 1.35–1.6 at λ 0.76, 0.15–0.3 at 0.9–0.95;
  city gas 1.0–1.1 at λ 0.8, 0.15 at 1.2, 0.03 at 1.47; IJmuiden's heavy oils 0.7–1.5 over λ 1.05–1.4 and
  creosote pitch 2.0 at 1.1. "the ratios depend mainly upon the fuel kinds and the air excess ratio. The
  effect of the burner kinds almost disappears" (p.67); IJmuiden's furnaces are "about five or six times"
  larger, and "the effect of the furnace scale can be neglected if such means of calculation are adopted"
  (p.68). ε_g came from Hottel and Ullich's charts (p.51), not a WSGG set.
- **[O3] IFRF Combustion Handbook, "How do I calculate the emissivity of combustion products from oil
  combustion?"**, posted 29 March 2003, <https://ifrf.net/research/handbook/how-do-i-calculate-the-emissivity-of-combustion-products-from-oil-combustion/>.
  Oil products hold "approximately 13% H2O and 13% CO2 by volume" at stoichiometric, pw/pc ≈ 1 ± 0.1;
  "Soot can increase the total emissivity of flames significantly." Its spreadsheet (Truelove's 3-term
  mixed grey gas model, UKAEA AERE-R 8494, 1976) takes "carbon or soot concentration c in kg/m3", valid as
  printed for "Soot concentration c greater than or equal to 5×10-3 kg/m3" (5 g/m³, 2.8 ppm at 1800
  kg/m³, Derived; the direction of that bound may be a slip). It cites Taylor and Foster 1974, Hottel and
  Sarofim 1967 and Gray and Müller 1974, none open; the spreadsheet was not downloaded.
- **[E1] Johnston, J. M., Wooster, M. J. and Lynham, T. J.** (2014), "Experimental confirmation of the
  MWIR and LWIR grey body assumption for vegetation fire flame emissivity", Int. J. Wildland Fire
  (WF12197): boreal fuel flames 0.2–4.2 m deep, one emissivity–depth relation in both bands, "extinction
  coefficient K = 0.7 m–1". **Snippet.**
- **[E2] Costafreda et al.** (RECERCAT 2072/188984): nine circular Mediterranean fuel beds 0.3–2.5 m;
  "only flames thicker than 3.2 m would exhibit an emissivity close to that of a blackbody (0.9), and the
  associated extinction coefficient would be 0.72". **Snippet.**
- **[E3] Beyreis, J. R., Monsen, H. W. and Abbasi, A. F., "Properties of wood crib flames"**, Fire
  Technology 7 (1971) 145–155, doi:10.1007/BF02588954; as a citing paper puts it: 650–1300 °C, flames
  25–190 cm thick, "flame emissivities were located in a range between 0.1 and 0.6". **Snippet.**
- **[E4] Tree, D. R., Tobiasson, J., Egbert, S. C. and Adams, B. R., "Measurement of radiative gas and
  particle emissions in biomass flames"**, Proc. Combust. Inst. (BYU), a 130 kWth down-fired reactor: in
  the luminous zone of a pulverised-wood flame (500 µm) particles 0.17 against gas 0.12; downstream gas
  0.13–0.19, particles 0.01–0.02; a lean natural-gas flame, soot 0.02 against gas 0.14. **Snippet.**

Derived cross-check: K = 0.7 m⁻¹, if it were all Planck-mean soot at 1817·f_v·T [L2], is f_v ≈ 0.39 ppm
at 1000 K and 0.32 ppm at 1200 K, the order of [W1]'s path averages. K was measured in IR windows and
includes the gas, so this is an order of magnitude only.

## 3. From f_v to an absorption coefficient or an emissivity

**[L1] Sadeghi, H., Hostikka, S., Fraga, G. C. and Bordbar, H., "Weighted-sum-of-gray-gases models for
non-gray thermal radiation of hydrocarbon fuel vapors, CH4, CO and soot"**, Fire Safety Journal 125
(2021) 103420, doi:10.1016/j.firesaf.2021.103420, **CC BY 4.0** (p.1; Aalto's reprint, downloaded by the
earlier survey). Rayleigh soot: κ_sη = C_η f_v η (eq. 2), C_η = 36πn_s k_s/[(n_s² − k_s² + 2)² + 4n_s²k_s²]
(eq. 3), n and k from Chang and Charalampopoulos (eqs. 4–5) (p.4). "Different fuel-dependent values of C
have been reported in the literature, e.g., 4.0 for acetylene, 4.1 for methane flames, 4.9 for propane, 6.3
for oil combustion and 3.7–7.5 for coal combustion [28]" (Cassol et al. 2014; p.4). Soot WSGG: four grey
gases and no clear gas ("due to continuity of absorption spectrum of soot, the transparent gas is not
needed", p.6), a_j = max(Σ b_j,n T_rⁿ, 0), T_r = T/1400 K (eqs. 9–10, pp.4–5), for "300K ≤ T ≤ 3000K"
(p.6); Table B9 (p.14):

| j | κ_j/f_v (m⁻¹) | b_j0 | b_j1 | b_j2 | b_j3 | b_j4 | b_j5 |
|---|---|---|---|---|---|---|---|
| 1 | 1.4530e5 | 1.8613 | −7.7857 | 12.809 | −10.158 | 3.8717 | −0.56880 |
| 2 | 2.0836e6 | 0.25975 | −2.9708 | 9.6830 | −9.7681 | 4.1073 | −0.63057 |
| 3 | 7.5475e5 | −1.1374 | 10.625 | −21.665 | 18.750 | −7.4578 | 1.1219 |
| 4 | 4.2113e6 | −0.038367 | 0.42159 | −1.4101 | 1.7225 | −0.75889 | 0.11454 |

The grey fit (eq. 24, p.8, "at fv = 1"): κ_s = aT³ + bT² + cT + d, a = 2.156×10⁻⁵ K⁻³, b = −0.2889 K⁻²,
c = 1804 K⁻¹, d = −2.012×10⁵ K. Mixtures by superposition: κ's add, weights multiply (eqs. 12–14, p.6).
Table 2 (p.8; f_v = 10⁻⁵, 1000 K, 1 m): the grey Planck mean errs 13.6 % on average in q_r, the four-gas
set 0.13 %. Conclusion (p.12): coupling with a CO₂–H₂O set "and considering soot as a gray medium" is
"recommended ... the average accuracy loss was generally less than 5%". The f_v·L range of the soot fit
is not stated in the pages read.
Derived: B9's weights sum to 1 within 0.6 % over 300–1800 K, 0.98 at 2400 K, 0.95 at 3000 K; eq. 24
gives κ/(f_v T) = 1336, 1310, 1285 m⁻¹K⁻¹ at 1000, 1300, 1500 K, 0.71–0.74 of RadLib's 1817 [L2].

**[L2] RadLib** (BYU, MIT licence), `rad_wsgg.cc` lines 75–89 and 224–229 (the earlier survey's copy):
"k_soot = F_s fv_soot T, where F_s = 3.72 c_soot/C_2, where C_2 = 0.014388 m·K and c_soot = 36πnk/[(n² −
k² + 2)² + 4(nk)²]"; "Using Shaddix's model ... k = 1.03, n = 1.75, giving F_s = 1817 K⁻¹m⁻¹" (Williams,
Shaddix et al., IJHMT 50 (2007) 1616); "The soot absorption coefficient is added to that for each gas
(including the clear gas, since the soot absorption spectrum is "full"). The weights don't need to be
changed ... This soot addition was suggested by H. Bordbar." The code:
`double ksoot= 1817 * fvsoot*T;` then `kabs += ksoot;`. Derived: C₀ = 7.027 for n 1.75, k 1.03, and
3.72 × 7.027/0.014388 = 1817.

**[L3] Tam, W. C. and Yuen, W. W., *OpenSC – an Open-source Calculation Tool for Combustion Mixture
Emissivity/Absorptivity***, NIST Technical Note 2064 (2019), doi:10.6028/NIST.TN.2064 (US government work).
Eqs. 3–5 (p.4): a_λs = c/λ, c = 36π f_v nk/[(n² + k² + 2)² + 4n²k²] **as printed** (Sadeghi's eq. 3 and
RadLib have n² − k²), with n = 1.6, k = 0.5 "applicable for hydrocarbon fuels such as propane soot"; the
closed form α_s(T_w, f_vL) = 1 − (15/π⁴) ψ⁽³⁾(1 + c T_w L/C₂), ψ⁽³⁾ the pentagamma function, citing Yuen
and Tien 1977 (16th Symp. (Int.) Combust., 1481–1487); with T_w = T_g it is the soot emissivity. The
handbook method (pp.15–16, from the SFPE Handbook): ε_t = (1 − e^(−κ_sL)) + ε_g e^(−κ_sL) (eq. 17), "κ_s is
taken to be k f_v T_g with the optical constant k suggested to be 1800" (citing CFAST, NIST SP 1041). Soot
density "taken to be 1800 kg/m3" (Appendix C, p.28). Derived: C₀ = 4.28 with n² − k², 3.52 as printed.

**[L4] Hofgren [W5]**, eq. 4.12 (p.33), after Modest: κ_P = 3.83 C₀ f_v T/C₂; C₀ "set to be 5.0" in his
paper VI (p.34). Derived: the Planck mean of κ_η = C₀f_vη is exactly Γ(5)ζ(5)/[Γ(4)ζ(4)] = 3.832 times
C₀f_vT/C₂ (RadLib uses 3.72). With [L1]'s C values: 1065 (acetylene), 1091 (methane), 1304 (propane), 1677
(oil), 985–1996 (coal) m⁻¹K⁻¹; [L1]'s eq. 24 is C ≈ 4.8–5.0 in this form.

**[L5] Lienhard and Lienhard, *A Heat Transfer Textbook*, 6th ed. (v6.00, 2024), p.594** (the repo's copy;
the 5th ed. was not opened): a candle's heat and light come from "soot—small solid particles of almost
black-body carbon. The CO2 and H2O in the candle flame actually radiate relatively little heat." No model
or number.

**[L6] Felske, J. D. and Tien, C. L., "Calculation of the Emissivity of Luminous Flames"**, Combust. Sci.
Technol. 7(1) (1973) 25–31, doi:10.1080/00102207308952339; abstract only (Buffalo's research portal): "A
simple analytical basis for determining the total emissivity of luminous flames is developed. The
analysis considers flames whose dominant emitting species are water vapor, carbon dioxide and soot
particles." The closed form above is [L3]'s.

**What the models give**, soot only, uniform path (Derived): grey = 1 − e^(−1817 f_v T L) [L2]; F–T =
[L3]'s closed form with C₀ = 7.027; B9 = Σ a_j(1 − e^(−κ_j f_v L)) [L1]. L = 0.5 m is the fast-fire
chamber's 4V/A (0.69 × 0.69 × 0.91 m, `thermal-software.md` §6.5).

| f_v (ppm) | L 0.5 m, 1500 K: grey / F–T / B9 | L 1.0 m, 1300 K: grey / F–T / B9 |
|---|---|---|
| 0.01 | 0.014 / 0.014 / 0.010 | 0.023 / 0.024 / 0.017 |
| 0.03 | 0.040 / 0.041 / 0.028 | 0.068 / 0.070 / 0.050 |
| 0.1 | 0.127 / 0.129 / 0.091 | 0.210 / 0.210 / 0.154 |
| 0.3 | 0.336 / 0.328 / 0.244 | 0.508 / 0.485 / 0.384 |
| 1 | 0.744 / 0.693 / 0.582 | 0.906 / 0.842 / 0.756 |
| 3 | 0.983 / 0.936 / 0.881 | 0.999 / 0.980 / 0.948 |

Across a row the spread is the soot's optical constants (C₀ 7.0 against about 4.9) and, above about 0.3
ppm, the grey Planck mean's overstatement in a thick path. Down the column, 0.01 to 1 ppm takes soot alone
from about 1 % to 58–74 % emissivity over half a metre: the f_v band, not the model, is what matters.

## 4. Soot in reduction, in kiln flames, in fuel-rich flames

- **Kiln flames: not found.** No source read measures soot, KL or a luminous emissivity in a pottery,
  brick or ceramic kiln, in oxidation or reduction; searches on kiln reduction found CO monitoring and
  potters' notes only.
- **Fuel-rich flames.** Every source that varies the air ratio finds soot rising steeply below λ ≈ 1:
  oils [O1] (7000 mg/Nm³ at λ 0.64 against 200–1450 at 1.0; ε_s/ε_g 2–2.9 below λ 1); city gas [O1] (none
  above λ 1.5, as much as oil below 1.0 with a soot-prone burner); biomass powder [W3] (about 0 at λ 1.0
  to 0.09–0.17 at 0.8, unit not printed); stem wood in a gasifier, 1.0 ppm at φ 0.5 [W2]; an 80 kW
  propane flame made "sooty" by closing its primary air, 65 ppb [W6]. Heavy oil keeps soot with excess air
  ([O1] p.60; [O2] at λ 1.2).
- None of these is a kiln's reduction (its λ, residence time, path, setting): they give the direction and
  the order only.

## The options

**(i) Leave soot out and say so (now).** Model: Bordbar's CO₂–H₂O only, with the working saying "soot not
counted; for wood, oil and any reduction the gas radiation is a lower bound". Band: ε_soot = 0. Why a bound
(Derived): soot adds κ_s ≥ 0 to every grey gas, so every gas emissivity and absorptivity can only rise; at
a given gas temperature the gas–surface exchange is least with soot out. Fits gas burners in oxidation
(city gas: no soot above λ 1.5 [O1]; propane with its primary air open, "very few" particles [W6]; lean
natural gas, soot 0.02 against gas 0.14 [E4], Snippet). Understates wood ([W1]–[W6]), oil ([O1], [O2]) and
any reduction. The fast-fire already reaches cone 10 in 0.40 h against the book's 3½ h (`11-10-26.md`);
soot can only speed that bound further, so it is not the missing piece there.
*To confirm it for a kiln:* a non-luminous flame there, which a KL reading through a spy hole would show.

**(ii) A stated f_v band with a sourced model.** Model: add κ_s = F_s f_v T to each of Bordbar's four grey
gases and the clear gas, weights unchanged ([L2]'s form, Bordbar's suggestion; a few lines in
`gasrad.py`), with F_s from 1285 ([L1] eq. 24 at 1500 K) to 1817 ([L2]) m⁻¹K⁻¹ as the optical-constant
band; or [L1]'s Table B9 by superposition (5 × 4 = 20 grey gases, CC BY). The f_v band by fuel:
- wood: 0 to about 1.2 ppm ([W1] peak 1.21, path average 0.61; [W2] 1.0 at φ 0.5); open fires peak at 6.8
  ppm [W4]. None is a kiln, and none says how much of a firebox's soot reaches the chamber.
- oil: about 0.01–0.3 ppm at λ 1.0–1.2 ([O2]; [O1] mass-equivalent 0.01–0.15), to about 0.7 ppm
  mass-equivalent at λ 0.64 ([O1], Derived; an upper figure).
- gas: 0 to 0.07 ppm [W6]; for reduction no kiln-burner figure.

Effect (§3): at 0.5 m and 1500 K soot alone gives 0.01 at 0.01 ppm, 0.09–0.13 at 0.1 ppm and 0.58–0.74
at 1 ppm. *To narrow it:* the kiln's own soot where its gas exchanges with the setting: laser extinction across the
chamber or the firebox throat (a laser and a photodiode across two spy holes give f_v·L, as [O2]), or a
two-colour KL through one spy hole ([O2], [W1]), with flue O₂ and CO for λ at the same moment, through a
stoking cycle and through reduction. A soot catch in mg/Nm³ ([O1]'s method) needs the particle size too.

**(iii) A luminous-emissivity band.** Model: a grey flame emissivity on top of the gas's.
- Oil: [O1]'s rule, ε_s = r·ε_g with r(fuel, λ) off Fig. 14 (0.03–2.9), ε_t = 1 − (1 − ε_g)(1 − ε_s),
  scale-free by the authors' IJmuiden check. For ε_g 0.10–0.20 (inputs to show the arithmetic, not kiln
  values) and r 0.2–3: ε_t 0.12–0.68 (Derived). Grey, and tied to Hottel's ε_g, not Bordbar's.
- Wood: a grey K ≈ 0.7 m⁻¹ ([E1], [E2], Snippets): ε = 1 − e^(−0.7L), 0.30 at 0.5 m, 0.50 at 1 m
  (Derived); wood cribs 0.1–0.6 at 0.25–1.9 m ([E3], Snippet). Open fires at their own λ and temperature.

*To narrow it:* the kiln's flame emissivity by [O1]'s method, a radiation pyrometer through a spy hole
onto a cold black target across the chamber with the gas temperature taken there, or a wide-angle
radiometer at the wall as in [W5].

**(iv) Soot tied to λ (a refinement of ii).** With λ from B4, the band could open only below λ ≈ 1 for gas
and keep (ii)'s oxidising values for wood and oil (§4). No source gives that curve for a kiln burner or
firebox; [O1]'s or [W3]'s curves would carry their burners into the kiln, and the working would say so.

Not available as an option: a soot yield (kg of soot per kg of wood) from the fire-science handbooks;
none was read.

## Not found / not read

- Any f_v, KL or luminous emissivity in a kiln of any fuel or atmosphere; in-flame soot in a wood stove,
  fireplace, log fire or wood-kiln firebox; f_v in a biomass grate furnace ([W5] has particle mass only).
- Read only as cited, or only as a snippet: Sepman et al. 2016 (Appl. Phys. B), 2017 (PCI 36) and 2019
  (Energy & Fuels 33) (Springer, ACS); Yan et al. 2020 (Energy & Fuels 34:907); Tree et al. [E4];
  Johnston et al. [E1] (CSIRO); Costafreda et al. [E2] (RECERCAT, 403); Beyreis et al. [E3] (Springer).
- Not open or not reached: Taylor and Foster 1974; Truelove 1976 and IFRF's spreadsheet [O3]; Hottel and
  Sarofim 1967; Gray and Müller 1974; Trinks; Modest (cited through [W5]); Yuen and Tien 1977; Felske and
  Tien's full text; Chang and Charalampopoulos; Williams and Shaddix 2007; Cassol et al. 2014's soot
  table; the IJmuiden trial reports (only through [O1]'s figures); Hägglund and Persson's FOA reports;
  Boulet et al. 2011 on HAL (hal-00652744, a bot wall); IFRF's archive report on extinction coefficients
  and flame emissivity; the Utah AFRC archive (HTTP 418); a Lund gasifier-soot thesis
  (lup.lub.lu.se files 42599646, over 60 MB).
- Soot yields of wood (SFPE Handbook, Tewarson): not read.
- Diesel-spray soot data (Sandia's Engine Combustion Network) are for engine pressures: not used.
