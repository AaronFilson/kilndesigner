# Holding a sprung arch with springs or an expansion allowance

Status: first pass, 2026-10-25. Builds on `arch-thrust-theory.md` (min/max thrust, [A1–A6]),
`thermal-properties.md` §2 (expansion) and `frame.py` (`cold_thrust_factor`,
`heated_thrust_factor`). Labels: **Verified** (read in the source), **Excerpt** (search-result
or snippet text, source not opened in full), **Derived** (worked here from sourced inputs),
**Not found**. Fewer than three independent sources is said each time.

## 1. Mechanics: thrust against an elastic restraint

| # | Fact | Status | Sources |
|---|---|---|---|
| 1.1 | A masonry arch on spreading supports goes to its minimum-thrust state; on closing (or a heated arch pressed against rigid supports) to its maximum-thrust state. Both are three-hinge mechanisms. | Verified/Excerpt | [A1] in arch-thrust-theory.md; [P1]; [P2] (2 independent beyond Heyman) |
| 1.2 | Hinge positions follow the extreme thrust lines; with growing support movement hinges can migrate (Ochsendorf's tests). | Excerpt | [P2], [P3] |
| 1.3 | Analytic formulas exist for the maximum allowable spreading displacement and its thrust for circular arches (kinematic approach). | Excerpt (paper not read) | [P1] |
| 1.4 | No source found gives a closed-form thrust vs. support-displacement curve between the two states for a kiln arch. | **Not found** | — |

**Derived model (engine proposal, from 1.1 and elementary elasticity).** Between the two
limit states the arch is a mechanism: it carries any thrust between H_min (≈ the cold,
free thrust the engine already computes) and H_max (Heyman maximum, `heated_thrust_factor`).
Thrust is therefore set by the restraint, not the arch:

- Free hot growth of span: ΔS_free = ε_eff · S (§2).
- Restraint in series (springs, rods, angle bending): 1/k = 1/k_spring + 1/k_rod + 1/k_angle;
  k_rod = A_t·E/L.
- H = clamp(H_preload + k·ΔS_free, H_min, H_max).
- If k·ΔS_free + preload > H_max, the arch cannot push harder; it **rises** at the crown
  (hinges open at the faces) and the excess growth becomes rise, not thrust. This is the
  rigid-steel case the engine already designs for.
- If preload < H_min the arch spreads (minimum thrust); the preload must be ≥ H_min cold.

This is a linear-spring idealisation; it ignores creep of hot refractory, friction at the
skewbacks and hinge migration [P2]. Fewer than 3 sources support it as a whole: it is Derived.

## 2. How much the span grows

| # | Fact | Status | Sources |
|---|---|---|---|
| 2.1 | IFB reversible expansion 0.5–0.7 % to ~1000 °C | Verified/Excerpt | thermal-properties.md §2 (3 sources) |
| 2.2 | Fireclay/dense castable ≈ 0.55–0.6 % at 1000 °C | Excerpt, weak | thermal-properties.md §2 (2 sources) |
| 2.3 | Kast-O-Lite / Mizzou reversible expansion; any curve to 1300 °C | **Not found** | — |
| 2.4 | Olsen: allow 1/16–3/32 in per foot of arch | Excerpt (book p.51, via user) | Olsen; 1 source |
| 2.5 | Fraction of hot-face expansion that reaches the skewbacks through the gradient | **Not found** | — |

Derived: a uniformly expanded arch scales geometrically, so ΔS = ε·S. Because the cold
face is cooler, the mean ε through the thickness is below the hot-face ε; the hot-face
value is an upper bound. For S = 28 in:
- ε = 0.6 % (2.2): ΔS ≤ 0.168 in.
- Olsen 1/16–3/32 in/ft × 2.33 ft: 0.146–0.219 in.
The two agree; the engine can use ΔS ≈ 0.15–0.22 in for 28 in at cone 10 and must say the
castable figure is weak.

## 3. Springs

| # | Fact | Status | Sources |
|---|---|---|---|
| 3.1 | Helical compression spring rate k = G·d⁴/(8·D³·n), n active coils, D mean diameter | Excerpt | [P4], [P5], [P6] (3) |
| 3.2 | Max service temperature: music wire ASTM A228 120 °C / 250 °F; chrome-vanadium 425 °F; chrome-silicon A401 475 °F; Inconel X-750 1100 °F (spring) to 1300 °F (strength) | Excerpt | [P7], [P8], [P9], [P10]; Cr-Si on 1 source only |
| 3.3 | Automotive valve springs, Summit listings: rates 283–746 lb/in; seat loads 120–350 lb; open loads 285–895 lb; e.g. Howards 98442 283 lb/in, 145 lb @1.750 in, 315 lb @1.150 in | Excerpt | [P11] (1 vendor, several makers) |
| 3.4 | Allowable shear stress, solid-height rules, relaxation derating curves (Shigley/Machinery's Handbook) | **Not found** (books not read) | — |
| 3.5 | Keeping springs outside the insulation (US 4,512,738) | Not re-checked here | olsen-questions.md [O3] context |

Derived: one 283 lb/in valve spring per rod end, taking ΔS/2 = 0.08–0.11 in per side,
adds only ~25–30 lb, well inside the spring's 145→315 lb working range. Springs must stay
below 250 °F (music wire) or 475 °F (Cr-Si); bolt them on the outside of the steel.

## 4. Fiber paper/board as the allowance

Olsen's 4th edition has no springs (the user, who has read it). It allows for expansion in the
walls instead: 1/16 in per foot of wall in a steel frame, a ¼ in fiber pad at the brick ends,
no joints under 4 ft in a flexible frame (p.52–53). Its growth figure,
1/16–3/32 in per foot (p.51), is what the engine uses for a sprung arch's span with springs.

| # | Fact | Status | Sources |
|---|---|---|---|
| 4.1 | Bio-soluble fiber paper: recovery ≥ 60 % after compression to 50 % thickness, 500 °C, 3 h | Excerpt (patent claim) | [P12] |
| 4.2 | Unifrax Duraboard HD (26 pcf): 59 psi @5 %, 70 psi @10 %, 81 psi @15 % deformation | Excerpt | [P13] |
| 4.3 | Fiberfrax paper "resiliency", no numbers | Excerpt | [P14] |
| 4.4 | Compression vs. pressure curve for 1/8 in paper | **Not found** | — |

Derived: if paper compresses to ~50 % usable, 0.15–0.22 in of growth needs ≈ 0.3–0.45 in of
paper across the arch (e.g. 3 joints of 1/8 in). Fiber gives a near-constant, low thrust but
does not recover fully (4.1), so repeated firings loosen the arch. One source each: weak.

## 5. Worked example (Derived)

28 in span, 5 in rise, 4.5 in castable (`frame.py`): H_cold/W = 0.671; heated factor 4.33,
H_max = 2.91 W (W = arch weight per unit depth; castable density not sourced here).
Rigid: ½-13 rod, A_t = 0.1419 in², E = 29×10⁶ psi, L = 40 in → k_rod ≈ 1.0×10⁵ lb/in;
k·ΔS ≈ 17,000 lb ≫ H_max, so thrust = H_max and the arch rises. With springs
(k ≈ 283 lb/in per end, rod in series barely matters): H ≈ preload (≥ 0.671 W) + ~30 lb,
i.e. close to the cold thrust.

## 6. Prices (Excerpt, dated by fetch 2026-10)

| Item | Price | Source |
|---|---|---|
| ½-13 × 6 ft zinc rod | $14.93 Home Depot; $12.64 Bolt Depot; $18.12 SupplyHouse; $4.21 All Fasteners (bulk) | [P15] |
| 2×2×¼ A36 angle | $10.02 / 12 in cut, $35.83 / 72 in (≈ $6/ft) | [P16] Speedy Metals only |
| 1 in square tube | **Not found** (nearest 1¼ in × .120: $0.88/in base) | [P16] |
| Valve springs, set of 16 | $124.99–$229.99 Howards; $200.99 Edelbrock (≈ $8–14 each) | [P11] Summit only |
| Ceramic fiber paper 1/8 in | ≈ $1.40/ft² + shipping (Kaowool, eBay, 24 in × 50 ft $140) | [P17] one source |

Not found: McMaster, Grainger, Lee Spring, Online Metals, Sheffield, Axner prices.

## Gaps
Castable reversible expansion; gradient fraction (2.5); spring stress/relaxation data;
fiber compression curves; second suppliers for angle, tube, springs, fiber.

## Sources
- [P1] Coccia, Di Carlo, Rinaldi 2015, Int J Adv Struct Eng, https://link.springer.com/10.1007/s40091-015-0101-x
- [P2] Zampieri et al. 2018, https://research.unipd.it/retrieve/e14fb26b-0ad1-3de1-e053-1705fe0ac030/19_Zampieri%20et%20al%20%282018%29CS.pdf
- [P3] Le Quy Don Tech. Univ. paper, https://jst.lqdtu.edu.vn/index.php/sce/article/download/952/626/6452
- [P4] Univ. Idaho springs poster, https://www.webpages.uidaho.edu/mindworks/machine_design/posters/pdf/springs.pdf
- [P5] https://customthermoelectric.com/tech-info/more-useful-info/equations-formulas/mechanical
- [P6] https://compressionspring.com/spring-rate-calculator.html
- [P7] AmesWeb spring steels, https://amesweb.info/MechanicalSprings/Tables/Spring-Steels.aspx
- [P8] Acxess Spring, https://acxesspring.com/properties-of-common-spring-materials-spring-wires.html
- [P9] Spring material table (Scribd), https://www.scribd.com/document/511881462/Spring-Material-Data
- [P10] Gibbs Inconel X-750 sheet, https://www.gibbswire.com/wp-content/uploads/2025/08/Gibbs-Datasheet-Wire-13-Inconel-X750.pdf
- [P11] Summit Racing, e.g. https://www.summitracing.com/parts/HRS-98442, /EDL-5745, /hrs-98441, /HRS-98611, /man-221447p-16
- [P12] US 8,940,134, https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8940134
- [P13] Distribution International, Duraboard HD, https://shop.distributioninternational.com/refractories/ceramic-fiber/ceramic-fiber-board/cfbdhd1024u
- [P14] Alkegen Fiberfrax paper A-5264, https://alkegen.com/wp-content/uploads/product_Info_north%20america/Fiberfrax/Fiberfrax%20Ceramic%20Fiber%20Paper_A-5264_1223.pdf
- [P15] https://www.homedepot.com/p/Everbilt-1-2-in-x-6-ft-Zinc-Plated-Steel-Coarse-Threaded-Rod-23041/332733421 ; https://boltdepot.com/Threaded_rod_Zinc_plated_steel_1_2-13 ; https://www.supplyhouse.com/Cooper-B-Line-ATR1-2X72ZN-1-2-x-6-ft-All-Threaded-Rod ; https://allfasteners.com/1-2-13-x-6ft-threaded-rod-zinc.html
- [P16] https://speedymetals.com/p-3947-2-x-2-x-14-angle-a-36-1020-hot-rolled-steel.aspx ; https://speedymetals.com/p-4767-1-14-x-76864-x-1-14-wall-square-steel-tubing.aspx
- [P17] https://www.ebay.de/itm/257061144578
