# Fittings for brick flues and convection inside a kiln

Part A4 of the round of 2026-11-10 (`docs/planning/11-10-26.md`). Two stand-ins in v2's heat model
are given sourced forms here: the draft's round-pipe fittings on brick flues through
area-equivalent diameters, "Idelchik's rectangular forms still *pending*" (`11-09-26.md` step 2),
and the inside convection taken from ht's laminar flat plate at the mean velocity (step 6).
`thermal-software.md` §8–9 and `thermal-combinations.md` §4.2 and §5 hold the earlier survey.

Read 2026-11-10. Marks: **Read** (read on the fetched page or PDF; for Idelchik, "page image" means
the rendered scan was read, "text layer" the scan's OCR text only), **Snippet** (a search snippet or
a summarising tool's paraphrase, not checked), **Derived** (my arithmetic, working shown), *from
memory* (not to be relied on). Idelchik's 1966 translation was read in full from NTIS's free
download; the NRC's copy (ADAMS ML12209A041) refuses scripts (HTTP 403) and Scribd's needs a login.
Not read: the primaries behind the convection correlations (Martin 1977, Gnielinski 1976,
Abou-Ziyan 2004, Rhine & Tucker 1991, Hottel & Sarofim 1967), a tunnel-kiln thesis behind a
repository's bot check, and the later Idelchik editions (see the end).

Idelchik's coefficient is ζ = ΔH/(γw²/2g), i.e. Δp = ζ·ρw²/2, on the velocity the diagram names
(w₀, the inlet or narrow section, unless said). Pages are the printed ones; the scan's PDF page is
the printed page + 8 on pp.1–3 and + 10 from p.45 on.

## Short answer

| Item | Coefficient or correlation | Range | Source | Mark | Open |
|---|---|---|---|---|---|
| Any fitting without rectangular data | as circular, on D_h = 4F/Π = 2a₀b₀/(a₀ + b₀) | 0.6 ≤ a₀/b₀ ≤ 1.7 | [D1] §1-2 item 12, p.3 | Read (text layer) | yes |
| Friction in a rectangular flue | turbulent: as circular on D_h (Colebrook–White); laminar: λ = k₁·64/Re, k₁ 1.50 (a₀/b₀ → 0) … 0.89 (1.0) | turbulent 0.5 ≤ a₀/b₀ ≤ 2; laminar Re < 2000 | [D1] pp.57–59; diag. 2-1 p.66 | Read | yes |
| Roughness of brick | **none given**; nearest: concrete "coarse" 3–9 mm, "average" 2.5; cement pipe "mortar in the joints not smoothed" 1.9–6.4 mm | — | [D1] Table 2-1 pp.62–64 | Read (text layer) | yes |
| Entrance from a large volume | flush in a wall 0.50; thin edge standing ≥ 0.5D_h clear of the wall 1.00; flush at angle δ: 0.5 + 0.3cos δ + 0.2cos²δ; rounded, flush, r/D_h 0.01–0.20: 0.43 → 0.03 | Re > 10⁴ | [D1] diag. 3-1, 3-2, 3-3 pp.92–93 | Read (3-2, 3-3 page image) | yes |
| Sudden contraction | 0.5(1 − F₀/F₁), blunt edge in the end wall; ζ′(1 − F₀/F₁) rounded or projecting | Re > 10⁴; a table for 10 < Re < 10⁴ | [D1] diag. 3-9, 3-10 pp.98–99 | Read (text layer) | yes |
| Sudden expansion | (1 − F₀/F₂)² on the narrow section's velocity | Re > 3.5·10³ | [D1] diag. 4-1 p.128 | Read (text layer) | yes |
| Exit into a large volume | 1.00 uniform; 1.06 for a power profile with m = 7 | — | [D1] diag. 11-1 p.416 | Read (text layer) | yes |
| Sharp 90° turn, equal sections | C₁·A·ζ₁ = 1.19·C₁; C₁ 1.10 (a₀/b₀ 0.25), 1.00 (1), 0.90 (2), 0.70 (8); × 45λ_Re at 3·10³–4·10⁴; ≈ ×1.2 with a recess | Re ≥ 4·10⁴ (smooth) | [D1] diag. 6-7 pp.215–216 | Read (page image) | yes |
| Sharp turn into a narrower or wider passage | ζ₁ 1.04–1.76 (b₁/b₀ 0.8–0.6) … 0.55–1.06 (b₁/b₀ 2.0), by a₀/b₀ | Re ≥ 2·10⁵; k_Re as 6-7 below | [D1] diag. 6-6 p.214 | Read (page image) | yes |
| Rounded bend | A₁B₁C₁ + ζ_fr | 0.5 < R₀/D_h < 1.5, Re ≥ 2·10⁵ | [D1] diag. 6-1 pp.206–207 | Read (page image) | yes |
| Two turns in a row | ζ₁ by l₀/b₀: Z 0.62 (0.4) → 4.22 (1.8) → 2.30 (∞); two planes 1.15 → 3.44 → 2.30; 180° Π (b_ch/b₀ = 1) 3.6 → 1.2 → 2.3 | Re > 10⁴ (Π: > 4·10⁴) | [D1] diag. 6-19, 6-20, 6-21 pp.228–230 | Read (page image) | yes |
| Flue into a much larger stack; stack exit | sudden expansion alone (0.53 at F₀/F₁ = 0.27); exit 1.0 | Idelchik's worked example | [D1] Table 1-11 pp.46–47 | Read (page image) | yes |
| Two streams meeting head-on | 1 + (F_c/F_1b)² + 3(F_c/F_1b)²[(Q_1b/Q_c)² − Q_1b/Q_c] on the outlet velocity; 1.25 at an equal split | — | [D1] diag. 7-29 p.289 | Read (page image) | yes |
| A side flue joining a main one | A[1 + (Q_bF_c/Q_cF_b)² − 2(1 − Q_b/Q_c)²], A 1.00 → 0.60 | — | [D1] diag. 7-7 p.266 | Read (text layer) | yes |
| Wall with through-gaps (bag wall) | [(0.5 + τ√(1 − f))(1 − f) + (1 − f)² + λl/d_h]/f² on the approach velocity; τ 1.35 → 0 as l/d_h 0 → 3 | Re ≥ 10⁵ (an approximate low-Re form) | [D1] diag. 8-4 pp.324–325 | Read (page image) | yes |
| Grate of bars | β₁k₁ sin θ, k₁ = (S₁/a₀ − 1)^{4/3}; β₁ 2.34 (square-edged) … 1.73 (round) | Re = w₀a₀/ν > 10⁴ | [D1] diag. 8-9 p.330 | Read (page image) | yes |
| Convection: a jet striking a surface | Martin: Nu = G·2Re^{0.5}(1 + 0.005Re^{0.55})^{0.5}·Pr^{0.42} | 2000 ≤ Re ≤ 4·10⁵; 2 ≤ H/D ≤ 12; 0.004 ≤ A_r ≤ 0.04 | [C3] after Martin 1977 | Read (secondary) | page yes; primary no |
| Convection: flues, chimneys, passages | Gnielinski with D_h for D | 2300 ≤ Re ≤ 5·10⁶, 0.6 ≤ Pr ≤ 10⁵; ±20 % on D_h | [C1] eq. 7.41, §7.5 | Read | yes |
| Convection: laminar passages | Nu_Dh by shape (square 2.976, a = 4b 4.439, plates 7.541 at fixed T_w); entry forms | Re < 2300 | [C1] Table 7.4; [C2] | Read | yes |
| Convection: brick-lattice setting | Nu = 0.556Re^{0.90}Pr^{0.333}RR^{0.26}ε^{2.064}(CC/c)^{1.78}(EC/b)^{2.91}(SC/a)^{−0.315} | Re 125–10,200; two lattices | [C4] eq. 29 | Read | yes (CC BY) |
| Convection: tunnel-kiln settings | Abou-Ziyan: Nu = 0.088Re^{0.625}(CC/c)^{−2.30}(εCC/a)^{1.837} | Re 6000–33,000 | [C5] via [C4] | Read (secondary) | primary no |
| Convection in furnace zone models | 0.023Re^{4/5}Pr^{1/3} on the furnace's D_h at the throughflow | Re ≥ 10⁴ ([C1] p.368) | [C6] | Read | yes |
| Natural convection on a wall; mixed | Churchill–Chu; mixed where Gr/Re² is near 1 | all Ra_L (8.13b) | [C1] eqs. 8.13, 8.45 | Read | yes |

## 1. Fittings for brick flues

### [D1] Idelchik 1966

**I. E. Idel'chik, *Handbook of Hydraulic Resistance: Coefficients of Local Resistance and of
Friction*** (*Spravochnik po gidravlicheskim soprotivleniyam*, Gosenergoizdat, 1960), translated by
A. Barouch, Israel Program for Scientific Translations, Jerusalem, 1966; AEC-tr-6630, IPST Cat.
No. 1505, "Published Pursuant to an Agreement with the U.S. Atomic Energy Commission and the
National Science Foundation", © 1966 IPST. Reproduced by NTIS: NTRL product AECTR6630, 528 PDF
pages, free through the record's "Download PDF" form,
<https://ntrl.ntis.gov/NTRL/dashboard/searchResults/titleDetail/AECTR6630.xhtml>. The scan carries
an OCR layer; tables marked "page image" were read on the rendered page.

**General directions (§1-2, pp.2–3; text layer).** Item 7: values are "for conditions of uniform
velocity distribution in the inlet section". Item 8: "The influence on the local resistance of an
element, due to fittings, obstructions, or lengthy straight stretches located downstream, is not
allowed for ... except as noted" (the combined diagrams below are the exceptions). Item 9: "In
practice, Re has an influence on the local resistance in the range Re < 10⁵ – 2×10⁵"; where no Re
is given, for turbulent flow (Re > 10³) "the resistance coefficient is practically independent of
the value of Re", and for laminar flow the data "can be used only for a rough estimate". Item 11:
roughness in local resistances "has not been extensively studied"; for Re > 4×10⁴ "a factor of the
order of 1.1 to 1.2 (higher at large roughness)". Item 12: "where the cross section is not
indicated, or when no additional data on the resistance of elements of noncircular section are
given, the value of the resistance coefficient for a polygonal or rectangular section of side ratio
0.6 ≤ a₀/b₀ ≤ 1.7 is to be considered equal to the value for a circular section."

**Friction (Section Two).** D_h = 4F₀/Π₀, a rectangle 2a₀b₀/(a₀ + b₀) (eq. 2-3, p.53). Laminar,
Re < 2000: λ = 64/Re; a rectangle "λ_r = k₁λ", k₁ at a₀/b₀ 0, 0.1, 0.2, 0.4, 0.6, 0.8, 1.0 =
1.50, 1.34, 1.20, 1.02, 0.94, 0.90, 0.89 (diagram 2-1, p.66, page image). Turbulent: "the friction
coefficient of rectangular pipes with small sides ratio (0.5 ≤ a₀/b₀ ≤ 2.0) can be determined in
the same way as for circular pipes" (item 17, p.59); smooth λ = (1.8 lg Re − 1.64)⁻² (item 13,
pp.57–58); commercial pipes Colebrook–White (eq. 2-16, p.58); the square law (eq. 2-19, p.59).
Text layer.

**Roughness (Table 2-1, pp.62–64; text layer).** "B. Conduits made from concrete, cement or other
materials", Δ in mm: concrete pipes, "Good surface, plaster finish" 0.3–0.8, "Average conditions"
2.5, "Coarse (rough) surface" 3–9; reinforced concrete 2.5; cement pipes, smoothed 0.3–0.8,
non-smoothed 1.0–2.0, "Mortar in the joints not smoothed" 1.9–6.4; cement-mortar plaster channels
0.05–0.22, steel-troweled 0.5; plaster over a metallic grid 10–15; ceramic salt-glazed channels 1.4;
slag-concrete tiles 1.5; slag and alabaster tiles 1.0–1.5. **No brick, firebrick or masonry
entry**: the book's only "Firebrick" is a porous medium for flow *through* the brick (diagram 8-19,
p.345). fluids' "Rough concrete", 3.05 mm, the engine's rough end, sits at the bottom of
Idelchik's "coarse" 3–9 mm (Derived comparison).

**Entrances (Section Three).**
- 3-1 (p.92, text layer), straight entrance, Re > 10⁴; ζ by edge thickness δ₁/D_h and the edge's
  distance b/D_h from the wall it is set in: flush (b/D_h = 0) 0.50 for every edge; a thin edge
  (δ₁/D_h = 0) at b/D_h 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.5, ∞: 0.57, 0.63, 0.68,
  0.73, 0.80, 0.86, 0.92, 0.97, 1.00, 1.00; δ₁/D_h ≥ 0.05: 0.50 throughout.
- 3-2 (p.93, page image), flush in the wall at angle δ: ζ = 0.5 + 0.3cos δ + 0.2cos²δ (Weisbach);
  δ 20, 30, 45, 60, 70, 80, 90°: 0.96, 0.91, 0.81, 0.70, 0.63, 0.56, 0.50.
- 3-3 (p.93, page image), bellmouth of arc radius r, Re > 10⁴; r/D_h 0, 0.01, 0.02, 0.03, 0.04,
  0.05, 0.06, 0.08, 0.12, 0.16, ≥ 0.20: "c) With end wall" 0.50, 0.43, 0.36, 0.31, 0.26, 0.22, 0.20,
  0.15, 0.09, 0.06, 0.03; "a) Without end wall (not sharpened)" 1.0, 0.87, 0.74, 0.61, 0.51, 0.40,
  0.32, 0.20, 0.10, 0.06, 0.03.
- 3-9 (p.98, text layer), sudden contraction, Re > 10⁴, inlet in the end wall: blunt edge
  ζ = 0.5(1 − F₀/F₁); rounded ζ = ζ′(1 − F₀/F₁) with ζ′ from 3-3 curve c; an edge moved forward
  takes ζ′ from 3-1 (eq. 3-3, p.84: "ζ = ζ′(1 − F₀/F₁)"). 3-10 (p.99): ζ(Re, F₀/F₁) tabulated for
  10 < Re < 10⁴ (not transcribed); ζ = A/Re with A ≈ 27 at the lowest Re (§3-2 item 9, p.84).

**Expansion and exit.** 4-1 (p.128, text layer), sudden expansion, uniform inlet, Re > 3.5·10³:
ζ = (1 − F₀/F₂)² on w₀ (table 1.00, 0.81, 0.64, 0.50, 0.36 at F₀/F₂ 0 … 0.4); 1 < Re < 8: 26/Re;
4-2 to 4-6 after non-uniform profiles. 11-1 (p.416, text layer), free discharge: uniform ζ = 1.0;
a profile w/w_max = (1 − r/R₀)^{1/m} in a circular or square pipe,
ζ = (2m + 1)³(m + 1)³/[4m⁴(2m + 3)(m + 3)]: m 1, 1.35, 2, 3, 4, 7, ∞ → 2.70, 2.00, 1.50, 1.25,
1.15, 1.06, 1.00 (Derived check at m = 7: 15³·8³/(4·7⁴·17·10) = 1.058). m = 7 is the 1/7-power
profile of developed turbulent flow (*from memory*; the diagram says only "exponential").

**Turns (Section Six).** §6-2 (pp.190–195, text layer), item 12: "The resistance of curved conduits
decreases with the increase of the side ratio of the elbow cross section a₀/b₀, and increases with
the decrease of a₀/b₀ in the range below unity"; a₀ is the side normal to the plane of the turn,
b₀ the side in it (the figures of 6-6 and 6-7, page image). Item 13: two sharp elbows forming a Π
with little between them separate "only after the complete turn by an angle δ = 180°", the highest
ζ; at l₀/b₀ of 4–5 and more ζ is "close to twice" one elbow's; near 1.0 it is least. Item 14: a Z
rises with l₀/b₀ to a maximum, then falls to "roughly equal to twice" one elbow's; item 15 likewise
for elbows in perpendicular planes.

- **6-7, sharp (r/D_h = 0) elbows, 0 < δ ≤ 180°** (pp.215–216, page image). Smooth, Re ≥ 4·10⁴:
  ζ = C₁Aζ₁, ζ₁ = 0.95sin²(δ/2) + 2.05sin⁴(δ/2). δ 20, 30, 45, 60, 75, 90, 110, 130, 150, 180°:
  ζ₁ 0.05, 0.07, 0.17, 0.37, 0.63, 0.99, 1.56, 2.16, 2.67, 3.00; A 2.50, 2.22, 1.87, 1.50, 1.28,
  1.20, 1.20, 1.20, 1.20, 1.20. C₁ at a₀/b₀ 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 6, 7, 8: 1.10,
  1.07, 1.04, 1.00, 0.95, 0.90, 0.83, 0.78, 0.75, 0.72, 0.71, 0.70 ("circular or square section
  C₁ = 1.0"). Rough, any Re: ζ = k_Δk_Re C₁Aζ₁ (Table 6-11, tentative): 3·10³ < Re < 4·10⁴,
  k_Re = 45λ_Re, k_Δ 1.0; Re ≥ 4·10⁴, k_Re 1.0, k_Δ 1.0 (Δ̄ = 0), 1 + 0.5·10³Δ̄ (Δ̄ ≤ 0.001),
  ≈ 1.5 (Δ̄ > 0.001); λ_Re the smooth λ at Re. "Elbow with recess: ζ ≈ 1.2ζ_w.r." (a dead-end
  pocket past the turn, as drawn).
  Derived: square, 90°: 1.20 × 0.99 = 1.19. A 4½ × 9 in flue turning in the plane of its 4½ in side
  (a₀/b₀ = 2): 0.90 × 1.19 = 1.07; in the plane of its 9 in side (0.5): 1.27. λ_Re =
  (1.8 lg Re − 1.64)⁻²: Re 8,300 → 0.0341, k_Re 1.54; 19,900 → 0.0269, 1.21; 4·10⁴ → 0.0227, 1.02.
- **6-6, sharp elbows of rectangular section with converging or diverging exit** (p.214, page
  image). Smooth, Re ≥ 2·10⁵: ζ = ζ₁ on the inlet velocity; rough or Re < 2·10⁵: k_Δk_Reζ₁ from 6-7.
  b₁/b₀ (exit width in the plane of the turn) 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 2.0: a₀/b₀ = 0.25:
  1.76, 1.43, 1.24, 1.14, 1.09, 1.06, 1.06; 1.0: 1.70, 1.36, 1.15, 1.02, 0.95, 0.90, 0.84; 4.0:
  1.46, 1.10, 0.90, 0.81, 0.76, 0.72, 0.66; ∞: 1.50, 1.04, 0.79, 0.69, 0.63, 0.60, 0.55.
- **6-1, sharp bends, 0.5 < R₀/D_h < 1.5** (pp.206–207, page image). Smooth, Re ≥ 2·10⁵:
  ζ = A₁B₁C₁ + ζ_fr, ζ_fr = 0.0175λ(R₀/D_h)δ°; A₁ = 0.9sin δ (δ ≤ 70°), 1.0 (90°), 0.7 + 0.35δ/90°
  (δ ≥ 100°); B₁ = 0.21/(R₀/D_h)^{2.5} (0.5–1.0), 0.21/√(R₀/D_h) (above 1.0); C₁ at a₀/b₀ 0.25 … 8:
  1.30, 1.17, 1.09, 1.00, 0.90, 0.85, 0.85, 0.90, 0.95, 0.98, 1.00, 1.00 (not 6-7's). Rough or
  lower Re: Table 6-4 (k_Re = 45λ_Re or 64λ_Re at 3·10³–4·10⁴). 6-9 to 6-11 (rounded or cut-off
  corners) not transcribed.
- **6-19, Z-shaped elbow** (two sharp 90° turns in one plane, l₀ apart), Re > 10⁴ (p.228, page
  image): ζ = C₁ζ₁ + λl₀/b₀, C₁ as 6-7. l₀/b₀ 0, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.4,
  2.8, 3.2, 4, 5, 6, 7, 9, 10, ∞: ζ₁ 0, 0.62, 0.90, 1.61, 2.63, 3.61, 4.01, 4.18, 4.22, 4.18, 3.65,
  3.30, 3.20, 3.08, 2.92, 2.80, 2.70, 2.60, 2.45, 2.30. Rough (tentative) k_Δ = 1.0 at Re < 4·10⁴.
- **6-20, two 90° elbows in perpendicular planes**, Re > 10⁴ (p.229, page image), the same grid:
  1.15, 2.40, 2.90, 3.31, 3.44, 3.40, 3.36, 3.28, 3.20, 3.11, 3.16, 3.18, 3.15, 3.00, 2.89, 2.78,
  2.70, 2.50, 2.41, 2.30.
- **6-21, Π-shaped elbow (180°), equal inlet and exit**, Re > 4·10⁴ (p.230, page image):
  ζ = C₁ζ₁ + λ(1 + l₀/b₀); l₀ the distance between the turns, b_ch the passage between them.
  l₀/b₀ 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.4: b_ch/b₀ = 0.5: 7.9, 6.9, 6.1, 5.4,
  4.7, 4.3, 4.2, 4.3, 4.4, 4.6, 4.8, 5.3; 0.73: 4.5, 3.6, 2.9, 2.5, 2.4, 2.3, 2.3, 2.3, 2.4, 2.6,
  2.7, 3.2; 1.0: 3.6, 2.5, 1.8, 1.4, 1.3, 1.2, 1.2, 1.3, 1.4, 1.5, 1.6, 2.3; 2.0: 3.9, 2.4, 1.5,
  1.0, 0.8, 0.7, 0.7, 0.6, 0.6, 0.6, 0.6, 0.7. 6-22 to 6-28 vary the exit; 6-26 (U-shaped, rounded,
  Re ≥ 2·10⁵, p.235) is lower.

**The worked example (Table 1-11, pp.44–47; pp.46–47 page image).** A gas path ending in a stack:
"Inlet to the stack", a flue of F₀ = 4.2 m² into the side of a round stack of F₁ = 15.8 m²,
F₀/F₁ = 0.27, ζ = 0.53 by "4-1 (sudden expansion)" (Derived check: (1 − 0.27)² = 0.533); "Exit
from the stack" ζ = 1.0 by "11-1"; "Draft in the entire stack" H_L = z(γ_a − γ_g), "Formula (1-38)".

**Junctions (Section Seven).**
- 7-29, symmetrical tee, α = 90° (p.289, page image): two streams joining, no partition,
  ζ_1c.b = ΔH_1b/(γw_c²/2g) = 1 + (F_c/F_1b)² + 3(F_c/F_1b)²[(Q_1b/Q_c)² − (Q_1b/Q_c)]; at
  F_1b/F_c = 1.0 and Q_1b/Q_c 0, 0.1 … 0.5: 2.00, 1.73, 1.52, 1.37, 1.28, 1.25 (symmetric about
  0.5); with a partition, F_1b/F_c = 1: +0.75 at 0.5. Derived check: 1 + 1 + 3(0.25 − 0.5) = 1.25.
- 7-7, converging tee F_b + F_s > F_c, F_s = F_c, α = 90° (p.266, text layer): branch
  ζ_c.b = A[1 + (Q_bF_c/(Q_cF_b))² − 2(1 − Q_b/Q_c)²] on w_c; A (Table 7-4) 1.00 (F_b/F_c 0–0.2),
  0.75 (0.3–0.4), 0.70 (0.6), 0.65 (0.8), 0.60 (1.0); the main passage by a table. Derived check
  against the printed bracket table: F_b/F_c = 0.2, Q_b/Q_c = 0.5: 1 + 6.25 − 0.5 = 6.75, as printed.

**Grids, grates, checkers (Section Eight).**
- 8-4, thickened grid (perforated plate or laths), l/d_h > 0.015 (pp.324–325, page image):
  Re = w₀d_h/ν ≥ 10⁵: ζ = ΔH/(γw₁²/2g) = [(0.5 + τ√(1 − f̄))(1 − f̄) + (1 − f̄)² + λl/d_h]/f̄²,
  f̄ = F₀/F₁, w₁ the approach velocity; τ at l/d_h 0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.4, 2.0, ≥ 3.0:
  1.35, 1.22, 1.10, 0.84, 0.42, 0.24, 0.10, 0.02, 0. Tabulated at λ = 0.02 (l/d_h 1.0, f̄ 0.5: 2.40;
  l/d_h 3.0: 2.24). Re < 10⁵: an approximate form with 8-2's Re terms (not transcribed). Derived
  check: [(0.5 + 0.24·0.707)(0.5) + 0.25 + 0.02]/0.25 = 2.42.
- 8-9, bar grating, approach angle α₀ = 0, Re = w₀a₀/ν > 10⁴ (p.330, page image); a₀ the gap,
  S₁ the pitch, θ the grating's inclination, ζ on w₁ ahead of it. (a) l/d_m = 5 and a₀/S₁ > 0.5:
  ζ = β₁k₁ sin θ, k₁ = (S₁/a₀ − 1)^{4/3} (a₀/S₁ 0.1 … 1.0: 18.7, 6.35, 3.09, 1.72, 1.00, 0.58, 0.32,
  0.16, 0.05, 0); (b) any l/d_m and a₀/S₁: ζ = β₂ζ′ sin θ, ζ′ from 8-4. Table 8-2, bar shapes 1
  (square-edged) to 7 (round): β₁ 2.34, 1.77, 1.77, 1.00, 0.87, 0.71, 1.73; β₂ 1.0, 0.76, 0.76,
  0.43, 0.37, 0.30, 0.74. Clogged: c′ 1.1–1.3 (mechanically cleaned), 1.5–2.0 (by hand).
- 8-22, regenerator checkerwork (p.349, page image): per height l₀ in metres, dimensional;
  "Stal'proekt" design ζ = (1400/Re)l₀ + Δζ_t (Re = w_0m d_h/ν < 700), 2l₀ + Δζ_t (Re > 700);
  Grum-Grzhimailo's ζ = (4400/Re)√d_h·l₀ + Δζ_t (Re < 1000); Siemens types with 0.114 and 1.57 over
  a root of d_h (the root's index and the Re > 1000 exponents not legible in the scan);
  Δζ_t = 2(t_ex − t_in)/(273 + t_m). Drawn for 230 mm checker bricks.

### [D2] fluids 1.3.1: what it takes from Idelchik (secondary)

C. Bell, `fluids` 1.3.1 (MIT), docstrings in the installed package (`fluids/fittings.py`,
`fluids/filters.py`), Read. Nine docstrings in `fittings.py` cite "Idel`chik ... National
technical information Service, 1966", i.e. [D1]:
- `entrance_sharp(method='Idelchik')` = 0.5 (3-1); `entrance_distance(method='Idelchik')`, a table
  on 3-1's grids; `entrance_beveled`, `contraction_round`, `contraction_conical`, `diffuser_conical`
  ('Idelchik' methods): all round.
- `entrance_angled` (only 'Idelchik'): **K = 0.57 + 0.30cos θ + 0.20cos²θ**, where 3-2 prints
  0.5 + 0.3cos δ + 0.2cos²δ (0.50 at 90°, 0.91 at 30°; fluids 0.57 and 0.98).
- `entrance_rounded(method='Idelchik')`: 0.5, 0.44, 0.37, 0.31 … where 3-3 curve c prints 0.50,
  0.43, 0.36, 0.31 ….
- Not in fluids: rectangular elbows or any C₁, combined elbows (Z, two planes, Π), Idelchik's
  junctions (its tees are Crane's), 8-4's thick plates, 8-9's bar gratings.
- `filters.square_edge_grill` (Blevins 1984, not read): K = [0.5(1 − α) + (1 − α²) + fl/D]/α² on
  the approach velocity: **(1 − α²)** where 8-4 has **(1 − f̄)²**, Borda–Carnot on the hole's
  velocity. At α = 0.5, τ = 0, friction aside: fluids 4.0, Idelchik 2.0 (Derived).
- `filters.round_edge_grill` (Blevins; the engine's grate): K 2.0, 1.0, 0.6, 0.4, 0.2 at α 0.3–0.7,
  "a rounded square grill or square bar screen or perforated plate with rounded edges". 8-9 for
  round bars at a₀/S₁ = 0.5: case (a) 1.73 × 1.00 = 1.73; case (b) with l = d_m, d_h = 2a₀,
  l/d_h = 0.5, τ ≈ 0.97 interpolated: ζ′ = [(0.5 + 0.97·0.707)(0.5) + 0.25 + 0.01]/0.25 = 3.41,
  ζ = 0.74 × 3.41 = 2.5 (Derived): 3–4× fluids' 0.6, for geometry described differently.

## 2. Convection inside a kiln

**Where kilns sit** (Derived; air as a stand-in for the gas, [C1] Table A.6 p.755: ν 1.575·10⁻⁵ m²/s
at 300 K and 2.394·10⁻⁴ at 1500 K, the table's top; μ 5.633·10⁻⁵ kg/(m·s) at 1500 K, 3.077·10⁻⁵
at 600 K; k 0.0264 and 0.0918 W/(m·K); Pr 0.707 and 0.743):
- the chamber as one passage, D_h 0.5–3 m at 0.1–2 m/s: Re 3,200–381,000 at 300 K, 210–25,000 at
  1500 K;
- passages in a setting, D_h 0.05–0.2 m (gaps of 25–100 mm, D_h = 2b): Re 320–25,000 at 300 K,
  21–1,700 at 1500 K;
- a 4½ × 9 in flue (D_h 6 in, 0.152 m; A 0.0261 m²) at the fast-fire's 0.08–0.105 kg/s
  (`11-09-26.md` step 2), Re = ṁD_h/(Aμ): 8,300 at 1500 K, 19,900 at 600 K;
- the fast-fire's two 4½ × 13½ in inlet flues (D_h 0.171 m) at 0.08 kg/s and 1500 K: 4.3 m/s,
  Re 3,100.

Hot setting passages are laminar, flues low-turbulent, burner-port and inlet-flue jets near
Re 3,000. Radiation's 4σT³ is 765 W/(m²·K) at 1500 K (Derived), so convection matters early in a
firing and in the flues.

### [C1] Lienhard, *A Heat Transfer Textbook* (open)

J. H. Lienhard V and J. H. Lienhard IV, *A Heat Transfer Textbook*, 6th ed., Version 6.00 (Phlogiston
Press, Cambridge MA, 2024), <https://ahtt.mit.edu/wp-content/uploads/2024/04/AHTTv600.pdf>; the
authors "grant you the right to download and print it for your personal use or for non-profit
instructional use". Read (text layer):
- **Gnielinski**, eq. 7.41 (p.369): Nu_D = (f/8)(Re_D − 1000)Pr/[1 + 12.7√(f/8)(Pr^{2/3} − 1)],
  "for 2300 ≤ Re_D ≤ 5×10⁶ and for 0.6 ≤ Pr ≤ 10⁵", f = (1.82 log₁₀Re_D − 1.64)⁻² (eq. 7.42);
  "reproduces more than 90% of the liquid data examined to within ±20% and is even more accurate for
  gases"; for "either uniform wall temperature or uniform heat flux". Gases (eq. 7.45, p.371):
  Nu = Nu|_Tb·(T_b/T_w)^n, n = 0.47 for T_w > T_b, 0 for T_w < T_b, 0.27 ≤ T_b/T_w ≤ 2.7.
- **Colburn's power law** (eq. 7.39a, p.368): Nu_D = 0.023Re_D^{0.8}Pr^{1/3}, from a friction law
  "for Re_D ≥ 10,000"; "intended for smooth pipes at reasonably low temperature differences";
  "largely superseded".
- **Rough walls** (pp.372–374): Re_ε = Re_D(ε/D)√(f/8), < 5 smooth, 5–70 transitional, > 70 fully
  rough; fully rough (Bhatti & Shah, eq. 7.49): Nu_D = (f/8)Re_D Pr/[1 + √(f/8)(4.5Re_ε^{0.2}
  Pr^{0.5} − 8.48)], "10⁴ ≤ Re_D, 0.5 ≤ Pr ≤ 10, and 0.002 ≤ ε/D ≤ 0.05"; f by Haaland (eq. 7.50).
- **Noncircular ducts** (§7.5, pp.382–387): D_h = 4A_c/P; turbulent, D_h for D in Re, f and Nu,
  "generally accurate to within ±20% and are often within ±10%. Worse results are obtained for duct
  cross-sections having sharp corners"; transition "typically approximated by the circular tube
  value of about 2300". Laminar, fully developed Nu_Dh (Table 7.4), T_w fixed / q_w fixed:
  circular 3.657/4.364, square 2.976/3.608, a = 2b 3.391/4.123, a = 4b 4.439/5.331, a = 8b
  5.597/6.490, parallel plates 7.541/8.235.
- **Natural convection on a vertical wall** (Churchill & Chu, eqs. 8.13a,b, pp.419–420):
  Nu_L = 0.68 + 0.670Ra_L^{1/4}[1 + (0.492/Pr)^{9/16}]^{−4/9} for Ra_L ≲ 10⁹; for all Ra_L,
  {0.825 + 0.387Ra_L^{1/6}/[1 + (0.492/Pr)^{9/16}]^{8/27}}²; properties at the film temperature.
- **Mixed convection** (eq. 8.45, pp.440–441): Gr_L/Re_L² "small compared to one" forced, "much
  larger than one" natural, "on the order of one" mixed; opposing flow "may lead to boundary layer
  separation". No combining formula; enclosures only described (p.440).

### [C2] ht 1.2.0 (docstrings)

C. Bell, `ht` 1.2.0 (MIT), `ht/conv_internal.py`, Read: `turbulent_Gnielinski(Re, Pr, fd)` is
eq. 7.41, "Range according to [Rohsenow et al., *Handbook of Heat Transfer*, 1998] is 0.5 < Pr ≤
2000 and 2300 ≤ Re ≤ 5*10^6"; `turbulent_Bhatti_Shah`; `laminar_entry_Baehr_Stephan(Re, Pr, L,
Di)`, the mean Nu over a tube's simultaneously developing laminar entry (after Baehr & Stephan, via
Incropera), tending to 3.657 as L grows; `Nu_laminar_rectangular_Shan_London(a_r)`. ht is already
the engine's (`thermal-software.md` §9).

### [C3] Martin's impinging-jet correlation (secondary statement)

Altair Engineering, *Flow Simulator 2026, Solver Technical Manual*, "Impingement from a Single
Hole", © 2025,
<https://help.altair.com/flowsim/topics/internal/solver_technical_manual/general_functions_routines/gfr_single_jet_r.htm>,
Read in the page's MathML. "The correlation for a gas jet uses a Nusselt number equation by Martin
(reference 1) that can also be found in Incropera (reference 2)": H. Martin, "Heat and Mass Transfer
between Impinging Gas Jets and Solid Surfaces", *Advances in Heat Transfer* 13 (1977); Incropera &
DeWitt, 6th ed., 2006, eq. 7.75 (neither read).
- Nu = G·[2Re^{0.5}(1 + 0.005Re^{0.55})^{0.5}]·Pr^{0.42}; G = 2√A_r(1 − 2.2√A_r)/[1 + 0.2√A_r(H/D −
  6)]; A_r = D²/(4r²); D the nozzle, r the impinged circle's radius, H the nozzle-to-surface
  distance; Re on D and the nozzle's flow; h = Nu·k/D, "k = fluid conductivity at film
  temperature"; "The HTC is the average over the impinged surface", derived "using the
  pre-impingement air temperature".
- "Reference ranges: 2 ≤ H/D ≤ 12, 2000 ≤ Re ≤ 400,000, 0.004 ≤ A_r ≤ 0.04" (r/D 2.5–7.9, Derived);
  one round jet into stagnant gas; a non-reacting jet.
- Derived example: D = 50 mm, Re 3000 (14.4 m/s at 1500 K), H/D = 6, A_r = 0.01 (r = 0.25 m):
  G = 2(0.1)(0.78) = 0.156; 2·54.77·(1 + 0.005·81.7)^{0.5} = 130.0; Pr^{0.42} = 0.883; Nu = 17.9;
  h = 17.9 × 0.0918/0.05 ≈ 33 W/(m²·K), against the flat plate's 2–3 and the 30 W/(m²·K) test
  value of `thermal-combinations.md` §4.2.

### [C4] Almesri et al. 2023: lattice brick settings (open)

I. F. Almesri, M. A. Alrahmani, J. H. Almutairi, H. Z. Abou-Ziyan, "Correlations of Heat Transfer and
Fluid Flow Data for Lattice Brick Settings in Tunnel Kilns", *Energies* 16 (2023) 3631,
doi:10.3390/en16093631, CC BY 4.0; Read in the LAPSE copy,
<https://psecommunity.org/wp-content/plugins/wpor/includes/file/2305/LAPSE-2023.35568-1v1.pdf>
(MDPI's page refused the fetch). CFD, validated against published experiments, of two lattice
settings: low density, 512 bricks, ε = 0.653; high density, 768 bricks, ε = 0.48.
- Definitions (eqs. 12–22, pp.10–11): Nu = hD_h/k; D_h = 4V_f/A_w (free volume over the wetted
  area of bricks and tunnel); Re = UD_h/ν, U = V/ε the interstitial velocity; RR = e_b/L_c, L_c a
  brick's volume over its surface.
- General correlation (eq. 29, p.14): Nu = 0.556Re^{0.90}Pr^{0.333}RR^{0.26}ε^{2.064}(CC/c)^{1.78}
  (EC/b)^{2.91}(SC/a)^{−0.315} (R² 0.9924); friction eq. 30. "valid for Re between 125 and 10,200,
  Pr from 0.68 to 0.73, relative brick roughness between 0.23 and 0.92, kiln voidage fraction
  between 0.48 and 0.65, column channel group of about 0.51, extension channel group of 0.75, and
  stack channel group between 0.31 and 1.31" — two geometries, so the geometric exponents rest on
  two settings.
- Restated earlier work (pp.2–4): [C5]; Vogt & Beckmann's Nu = Φ·0.018Re^{0.8}, Φ from Dugwell &
  Oakley's measurements, 6100 < Re < 50,700; Refaey et al.'s guide-vane forms, Re 11,867–27,634.

### [C5] Abou-Ziyan 2004 (via [C4])

H. Z. Abou-Ziyan, "Convective heat transfer from different brick arrangements in tunnel kilns",
*Applied Thermal Engineering* 24 (2004) 171–191 (Elsevier; not read). As [C4] gives it (eq. 2,
p.3): Nu = 0.088Re^{0.625}(CC/c)^{−2.30}(εCC/a)^{1.837}, "validated for Re range from 6000 to
33,000, voidage fraction ranges from 0.43 to 0.57, (CC/c) from 0.44 to 1.17, and (CC/a) from 1.62 to
4.25" (CC the column spacing; a, c a brick's thickness and length); six settings at constant heat
flux (Snippet, from an index's abstract).

### [C6] Convection in furnace zone models: Latham 2008

D. Latham, *Mathematical modelling of an industrial steam methane reformer*, MSc thesis, Queen's
University, 2008 (open; `thermal-software.md` Sources), §2.4 pp.29–30, page image: "All of the
furnace models that are used to simulate convective heat transfer from the furnace gas (except the
model by Liu et al. 2006) use the Dittus-Boelter equation (12)": h_f = (λ_fg/D_fur,hydr)(0.023Re^{4/5}
Pr^{1/3}), Re = ṁD_fur,hydr/(A_cross,fur·μ) (eq. 216, p.211, text layer): the throughflow on the
furnace's hydraulic diameter (Colburn's form, [C1] p.368). "Steward and Cannon (1971) used equation
(12) ... to surfaces parallel to the direction of flow and a different correlation for surfaces
perpendicular"; Liu et al. (2001) used Lebedev & Sokolov (1976), h_f = (λ_fg/D_fur,hydr)(A·Re^{3/4}),
"A is an experimentally-determined value that depends on the orientation" (eq. 13; no values).
Its cube-furnace test (Table 8, p.55) fixes h at 1635.3 kJ/(h·m²·K) for methane and oxygen: a test
constant, not a furnace measurement.

### [C7] An intermittent brick kiln (not usable)

G. Guerrero Gómez, L. E. Vera Duarte, C. J. Noriega Sánchez, "Determination of connective [*sic*]
heat transfer coefficients in an intermittent kiln", *J. Phys.: Conf. Ser.* 1587 (2020) 012025,
CC BY 3.0, Read: a coal-fired 2.5 × 2 × 2.88 m brick kiln whose 4.58–6.34 W/(m²·°C) (Table 1) are
*computed* from a natural-convection correlation (eqs. 1–3) at lengths of 0.15–0.56 m, not measured;
its energy balance (51.21 kJ from 1,600 kg of coal) does not hold together.

## For the engine

### Fittings: replacing the round-pipe stand-ins (`v2/heat/draft.py`)

All from [D1], ζ on the velocity named. The tables are for Re ≥ 10⁴–2·10⁵; a kiln's flues run at
Re 3·10³–2·10⁴ (§2). Where a diagram gives k_Re (6-6, 6-7: 45λ_Re, 1.2–1.5 at the fast-fire's
flows, Derived) use it; where none is given, say "below the diagram's Re" in the working.

| draft.py now | Replacement |
|---|---|
| `inlet`, `entrance`: 0.5 (fluids' Idelchik) | keep 3-1's 0.50 for a mouth flush in a wall; an edge standing clear of the wall up to 1.00 (3-1); a rounded mouth 3-3 c; Re < 10⁴: 3-10 |
| `duct`: Colebrook on D_h, roughness smooth to 3.05 mm | keep for 0.5 ≤ a₀/b₀ ≤ 2 (§2-2 item 17); Re < 2000: k₁·64/Re (2-1); roughness stays a band (no brick in Table 2-1) |
| `contraction_turn`: Rennels' contraction + mitre (1.20) | 6-6 at b₁/b₀ < 1: one coefficient on the inlet velocity (1.36–1.76 at b₁/b₀ 0.8–0.6, a₀/b₀ 0.25–1), × k_Re; a straight contraction 3-9 |
| `turn_expansion` (flue into its chimney): mitre + sharp expansion | a chimney up to 2× the flue in the plane of the turn: 6-6 (0.55–1.06 at b₁/b₀ 2) × k_Re; a much larger chimney: the sudden expansion alone (4-1), as Idelchik's own example (Table 1-11); the same section: 6-7, 1.19·C₁ × k_Re; ≈ ×1.2 where the chimney runs on below the flue (6-7's recess) |
| `outlet`: 1.0 | 1.0 (uniform) to 1.06 (an m = 7 profile), 11-1 |
| `grate`: Blevins' round-edged grill, 0.6 at α = 0.5 | 8-9's bar grating, round bars β₁ 1.73: 1.7–2.5 at a₀/S₁ = 0.5 (Derived); 8-9 needs Re = w₀a₀/ν > 10⁴, i.e. over 8.3 m/s in a ¾ in gap at 300 K (Derived: 10⁴ × 1.575·10⁻⁵/0.019) |
| two turns, summed | 6-19 (Z), 6-20 (two planes), 6-21 (180°): a pair is not twice one turn (Z: 0.62 at l₀/b₀ 0.4, 4.22 at 1.8, against 2 × 1.19 = 2.38) |
| several fireboxes or flues meeting (refused now) | 7-29 head-on, 7-7 from the side |
| bag wall, setting (left out) | 8-4 for a wall with through-gaps; no diagram for a setting (8-22's checkers are 230 mm brick lattices) |

### Convection: replacing the flat plate (`heat/zone.py`)

| Surfaces | Correlation | Range | Kiln (Derived, §2) |
|---|---|---|---|
| flues, chimneys | [C1] Gnielinski on D_h, n = 0 when the gas is the hotter (eq. 7.45); Re < 2300: [C2] Baehr–Stephan or [C1] Table 7.4; fully rough: Bhatti–Shah only at Re ≥ 10⁴, ε/D 0.002–0.05 | 2300–5·10⁶; ±20 % on D_h | Re 3,000–20,000: in range |
| surfaces a burner or inlet-flue jet strikes | [C3] Martin, mean over the circle r | Re 2000–4·10⁵, H/D 2–12, A_r 0.004–0.04 | jets near Re 3,000: in range where the geometry fits |
| the setting's passages | [C1] Table 7.4 or [C2] entry below 2300; Gnielinski above; a brick lattice: [C4] eq. 29 | [C4]: Re 125–10,200, its two lattices | hot: Re 20–1,700, laminar |
| walls and slow zones | the forced value, with Churchill–Chu (8.13) as the natural floor; mixed where Gr/Re² is near 1 (8.45) | — | — |

- **(a) A gas kiln's chamber with burner jets.** Best sourced: Martin's single-nozzle correlation
  ([C3]) on the bag wall or ware a port's jet strikes within 2–12 port diameters, the through-flow
  forms elsewhere. Its limits: a secondary statement (the primary not read), non-reacting jets (a
  flame releases heat on the way; the flame-impingement reviews not read), a mean over r ≤ 7.9D.
- **(b) A natural-draft wood kiln's chamber.** No correlation for a setting of shelves and pots was
  found. Best sourced: internal-flow forms on the setting's passages at the interstitial velocity
  ([C1], [C2]), Churchill–Chu as the natural floor; for a brick lattice (a brick kiln's setting),
  [C4] eq. 29 in its range. The setting's passages stay a stated band (ADR 0017 decisions 3–4).
- **(c) Flues and chimneys.** Gnielinski ([C1] eq. 7.41) on D_h, in range at Re 3·10³–2·10⁴. The
  zone models' Colburn form on the furnace's D_h ([C6]) needs Re ≥ 10⁴ ([C1] p.368), which a hot
  chamber mostly doesn't reach (Re 210–25,000 at 1500 K).

## Not found / not read

- **Brick or masonry roughness**: not in Idelchik 1966's Table 2-1 nor in fluids (`thermal-software.md`
  §8); no other source found.
- **Later Idelchik editions** (Hemisphere 1986; CRC/Begell 1994, the 3rd; Begell 2007, the 4th;
  Snippet): not open; a 3rd-edition PDF on typeset.io was not used (rights unclear).
- **Martin 1977** and **Incropera's eq. 7.75**: not read; Martin's formula is [C3]'s statement.
  **Flame impingement** (Baukal & Gebhart, *Combust. Sci. Technol.* 104, 1995; Chander & Ray 2005;
  citations Snippet): paywalled.
- **Gnielinski 1976** and the VDI Heat Atlas (his 2300–10⁴ transition form): not read; [C1], [C2]
  restate the 1976 equation.
- **Tunnel-kiln primaries**: Abou-Ziyan 2004, Dugwell & Oakley (*J. Inst. Energy* 61, 1988), Vogt &
  Beckmann, Refaey et al. 2017 (*Int. J. Therm. Sci.* 122): only through [C4]. H. Refaey's
  dissertation (repo.bibliothek.uni-halle.de, `Main_hassnein_final.pdf`): behind the repository's
  bot check, not bypassed. Mancuhan & Kucukada (*Appl. Therm. Eng.* 26, 2006): closed. (Journal
  details here are Snippet.)
- **Rhine & Tucker 1991, Hottel & Sarofim 1967**: not read; no open statement of the well-stirred
  furnace's convective term found ([C6] is the only open survey read). A University of Utah
  collection's furnace paper (collections.lib.utah.edu, id 13355; HTTP 418) says convection to the
  load is negligible without forced circulation (Snippet).
- **A mixed-convection combining rule** (Churchill 1977): not read; [C1] gives only the criterion.
  Natural convection in enclosures with a through-flow: nothing found.
- **A measured convection coefficient inside a studio or periodic kiln**: none found ([C7] computes,
  doesn't measure).
- Idelchik 1966 not transcribed here: 3-10's low-Re table, 8-4's Re < 10⁵ form, 6-9 to 6-11
  (rounded and cut-off corners), 6-22 to 6-28, exhaust vents and caps (11-14 to 11-17).
