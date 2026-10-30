# Door headers: what carries the wall and roof over a kiln door

Checked: 2026-10-28. Scope: a door, or a car opening, that stops below the roof of a studio kiln
of about 10 to 60 ft³. Walls are 4½ to 9 in of IFB or hard firebrick, sometimes with castable. The
roofs covered are a sprung arch springing from the side walls, a sail dome on four walls, a flat
IFB roof in a steel band or frame, and a catenary arch. Source tags are [H1], [H2] and so on, listed
at the end. Where a source is already in `kiln-hardware.md`, its S tag is given as well.

How values are marked (as in `kiln-hardware.md`):
- **Verified** means I read it on the page or in the PDF text.
- **Verified (scan)** means I read it from a rendered page image of a scanned PDF. Such a page
  either has no text layer or has a bad OCR layer.
- **Verified (OCR)** means I read it in the Internet Archive's OCR text of a scanned book. Obvious
  OCR slips are corrected silently.
- **Excerpt** means I saw it only in a search snippet. That includes Internet Archive full-text-search
  snippets of borrow-only books, stitched together from overlapping hits.
- **Derived** means I calculated it from sourced inputs. The working is shown.
- **(secondary)** means a forum post or similar, passing on practice rather than a design rule.
- **NOT FOUND** means I found no source. Do not fill these gaps with guesses.

Notes on the sources:
- The Brick Industry Association (BIA) notes and the masonry codes are written for building brick
  laid cold in portland-cement-lime mortar. A kiln wall is refractory brick that is dry-laid or set
  in thin refractory mortar, and one face of it is hot. **No source found tests the BIA rules on
  such a wall.** They are the best-sourced method available, not a validated kiln rule.
- BIA Technical Note (TN) 31B p. 3 and TN 31A pp. 2–8 are scans. They were rendered to images
  and read. The OCR text layer on TN 31A p. 1 misreads the load-triangle sentence ("¼ of the span");
  the scan reads "½".
- Rhodes, Olsen and Harbison-Walker's 1950 *Modern Refractory Practice* are borrow-only. Their quotes
  are stitched from Internet Archive full-text-search snippets, as `kiln-hardware.md` does for Rhodes.
- AISC 360-16 could not be read from aisc.org, which returned 403 as before. It was read from a copy
  on a University of Maryland faculty site [H7]. That closes the single-angle bending rules (F10) and
  the bending safety factor listed as gaps in `kiln-hardware.md` §4.6 and §4.7.4. The tension and
  threaded-part provisions that §4.7.4 also lists were not looked up here.

---

## D1. Steel lintels in masonry (BIA TN 31B, 1987)

### D1.1 When the masonry above may be assumed to arch

| Item | Value | Mark | Source |
|---|---|---|---|
| Load triangle | "The triangular wall area (ABC) in Fig. 2b above the opening has sides at 45-deg angles to the base." Fig. 2b marks its height L/2 | Verified (scan) | [H1] p. 3 |
| What arching carries | "Arching action of a masonry wall will carry the dead weight of the wall and the superimposed loads outside this triangle, provided that the wall above Point B (the top of the triangle) is sufficient to provide resistance to arching thrusts." | Verified (scan) | [H1] |
| Height above the apex | "For most lintels of ordinary wall thickness, loads and spans, a depth of 8 to 16 in. (200 mm to 400 mm) above the apex is sufficient." | Verified (scan) | [H1] |
| Bond | "If stack bonded masonry is used, horizontal joint reinforcement must be provided to ensure the arching action." | Verified (scan) | [H1] |
| Lintel load when it arches | "the weight of masonry enclosed within the triangular area (ABC)". "To the dead load of the wall must be added the uniform live and dead loads of the floor bearing on the wall above the opening and below the apex of the 45-deg triangle." Loads above the apex "may be neglected" | Verified (scan) | [H1] |
| Shoring | When arching is assumed, "the lintel must be shored until the masonry has attained sufficient strength to carry its own weight. This shoring period should not be less than 24 hr", or three days with imposed loads | Verified (scan) | [H1] |
| No arching | "If arching action is not assumed and temporary shoring is not to be used, the steel lintel must be designed for the full weight of the masonry and other superimposed live and dead loads above the opening." | Verified (scan) | [H1] |
| Conditions (CMHA TEK 17-01D, 2011 MSJC) | Running bond. A wall tall enough for a symmetrical triangle with 45° base angles. "at least 8 in. (203 mm) of wall height above the apex of the 45° triangle". "minimum end bearing (4 in. (102 mm) typ.)". "control joints are not located adjacent to the lintel". "sufficient masonry on each side of the opening to resist lateral thrust from the arching action". The triangle's base is the effective span and its height is half the effective span | Verified | [H5] |
| Dry masonry | "even with dry masonry a part of the wall will be self-supporting" (BIA, on arch loading) | Verified (scan) | [H3] p. 6 |

- How much masonry beside the opening counts as "sufficient": no source quantifies it for a
  lintel. **NOT FOUND.** BIA's abutment check for arches (§D3.5) is the nearest method.
- How much a dry-laid or hot refractory wall arches: **NOT FOUND.**

### D1.2 Loads inside the triangle, and concentrated loads

| Item | Value | Mark | Source |
|---|---|---|---|
| Concentrated load (BIA) | "may be distributed over a wall length equal to the base of the trapezoid and whose summit is at the point of load application and whose sides make an angle of 60 deg with the horizontal", taken as a partially distributed uniform load. "Arching action of the masonry is not assumed when designing for concentrated loads." Stack bond needs joint reinforcement for this spread | Verified | [H1] p. 4 |
| Concentrated load (MSJC) | "The 2005 MSJC (ref. 2c) provides for the concentrated load to be distributed at a 45° angle rather than at a 1:2 slope as required by the 2008 and 2011 MSJC". Its Figure 3 draws the slope as 1 horizontal to 2 vertical. "For running bond, the concentrated load dispersion terminates at: half the wall height; a movement joint; the end of the wall; or an opening—whichever provides the smallest length." The load becomes w = P/a over the spread length a | Verified | [H5] |
| Uniform load inside the triangle | "The MSJC (ref. 2) does not address how to apply uniform loads that are applied within the 45° triangle." There are two schools: apply the full uniform load directly to the lintel, or disperse the part inside the triangle onto the lintel at 45° | Verified | [H5] |
| Loads outside the triangle | "Any superimposed roof and floor live and dead loads outside this triangle are neglected, since they are assumed to be distributed to the masonry on either side of the lintel. Loads applied within the triangle need to be considered, however." | Verified | [H5] |

- A 1:2 slope lies at atan 2 = 63.4° to horizontal, close to BIA's 60°. A load applied over a width
  b at a height h above the lintel spreads over b + 2h/tan 60° = b + 1.155h under BIA's rule, and
  over b + h under MSJC's **(derived)**.
- No source treats a roof's edge (a skewback or a dome's edge) as a load on a wall over an opening.
  BIA's "floor bearing on the wall" is the nearest case.

### D1.3 Bending, shear and bearing

The formulas are BIA's [H1] p. 4–5, Verified.
- Triangle load: Mmax = WL/6. W is the total load on the lintel (lb) and L the "span of lintel,
  center to center of end bearing" (ft); M comes out in ft·lb.
- Alternative: "calculate an equivalent uniform load by taking 2/3 of the maximum height of the
  triangle times the unit weight of the masonry as the uniform load across the entire lintel",
  then Mmax = wL²/8. Concentrated and partially distributed loads are added using the AISC Manual's
  formulas.
- Section: S = 12 Mmax/Fb. "The allowable stress, Fb, for ASTM A 36 structural steel is 22,000 psi
  (150 MPa) for members laterally supported. Solid brick masonry walls under most conditions provide
  sufficient lateral stiffness to permit the use of the full 22,000 psi (150 MPa). This is
  especially true when floors or roofs frame into the wall immediately above the lintel." A lintel
  that is not laterally supported is designed to the AISC Specification (see §D2).
- Torsion arises when the load is not applied through the shear centre (cavity and veneer walls). If
  the lintel carries only the triangle, torsion "can be safely ignored". "If, on the other hand, there
  are imposed uniform loads within the triangle or imposed concentrated loads above the lintel, then
  a detailed, combined stress analysis will be necessary."
- Shear: vmax = Rmax/As, allowed 14,500 psi for A36.
- Bearing: Ab = Rmax/fm. The bearing length is Ab divided by the width of the section and "should
  not be less than 3 in. (75 mm)". Rotation adds bearing stress. Piers between close openings must
  be checked.
- BIA 31A [H3] Verified (scan) puts the triangle's equivalent uniform load at "1⅓ times the
  triangular load".

Derived:
- With unit weight ρ (lb/ft³) and wall thickness t (ft), the triangle weighs W = ρtL²/4, so
  M = WL/6 = ρtL³/24. The uniform alternative, w = ρtL/3, gives wL²/8 = ρtL³/24, the same moment.
  The 1⅓ factor agrees: (4/3)W × L/8 = WL/6.

Refractory bearing:
- BIA's Table 2 allowable compressive stresses are for building brick, from ANSI A41.1-1953: 75 to
  400 psi depending on unit strength and mortar type [H1] Verified.
- An allowable bearing stress for IFB or hard firebrick, cold or hot, is **NOT FOUND**. Strength
  and hot-load data are in §D5.1.

### D1.4 Serviceability

| Item | Value | Mark | Source |
|---|---|---|---|
| Deflection (BIA) | "Lintels supporting masonry should be designed so that their deflection does not exceed 1/600 of the clear span nor more than 0.3 in (8 mm) under the combined superimposed live and dead loads." Δt = 5wL⁴(1728)/384EI, with w in lb/ft, L in ft, E in psi and I in in⁴ | Verified | [H1] |
| Rotation (BIA) | where torsion is present, "limited to 1/16 in. (1.5 mm) maximum" | Verified | [H1] |
| Deflection (TMS 402-16 §5.2.1.4.1) | beams or lintels supporting unreinforced masonry: L/600 | Verified (TMS slides; TMS 402 itself not read) | [H6] |
| Deflection (2011 MSJC) | "limited to the clear lintel span divided by 600" | Verified | [H5] |
| Unrestrained angle (AISC Commentary F10) | "The deflection calculated using the geometric axis moment of inertia has to be increased 82% to approximate the total deflection. Deflection has two components: a vertical component (in the direction of applied load) of 1.56 times the calculated value and a horizontal component of 0.94 times the calculated value." Holding the angle to purely vertical deflection takes a lateral restraining force of 60% of the applied load | Verified | [H7] |

### D1.5 Materials, sizes and code geometry

| Item | Value | Mark | Source |
|---|---|---|---|
| Steel | "as a minimum, should comply with ASTM A 36" | Verified | [H1] |
| Angle size | "at least 1/4 in. (6 mm) thick with a horizontal leg of at least 3 1/2 in. (90 mm) for use with nominal 4 in. (100 mm) thick brick, and 3 in. (75 mm) for use with nominal 3 in. (75 mm) thick brick" | Verified | [H1] |
| Span | "Most building codes permit steel angle lintels to be used for openings up to 8 ft 0 in. (2.4 m)." | Verified | [H1] |
| Solid walls | "single loose angle lintels are usually not capable of doing the job"; use angles back to back, or a beam with plates | Verified | [H1] |
| Loose angle | a loose angle lintel in a veneer or cavity wall "has no lateral support" | Verified | [H1] |
| Arch carried on an angle | "the angle is designed to support the entire weight of brick masonry loading the arch, and the structural resistance of the arch is neglected" | Verified | [H2] |
| Span length (TMS 402-16 §5.2.1.1.1) | the smaller of the clear span plus the beam depth and the distance between support centres | Verified (slides) | [H6] |
| Bearing (TMS 402-16 §5.2.1.3) | at least 4 in. in the direction of the span | Verified (slides) | [H6] |
| Lateral support of masonry beams (TMS 402-16 §5.2.1.2) | compression face braced at no more than the smaller of 32b and 120b²/d | Verified (slides) | [H6] |
| Steel expansion | above 150 °F, "the coefficient of thermal expansion shall be 7.8 × 10⁻⁶/°F" | Verified | [H7] App. 4 |
| IFB expansion | reversible linear thermal expansion, max: K23 0.7 %, K25 0.8 %, K26 0.8 % | Verified | [H20] |

For a kiln, a 4½ in IFB wythe is roughly BIA's nominal 4 in brick, so its rule asks for a ¼ in
angle with a horizontal leg of at least 3½ in: an L3½×3½×¼ or L4×4×¼ **(derived reading, not a
sourced kiln rule)**.

### D1.6 BIA Table 1 as test cases (derived)

BIA's Table 1 gives the "Allowable Uniform Superimposed Load (lb per ft) for ASTM A 36 Structural
Steel Angle Lintels": Fb = 22,000 psi, maximum deflection L/600, "Lateral support is assumed in all
cases", and "For angles laterally unsupported, allowable load must be reduced" [H1] Verified. The
extracted table text is jumbled. The rows below were matched by recomputing each value.

The method is **derived**: w = min(8M/L², w at Δ = L/600) − the angle's own weight, with
M = Fb·S/12 and E = 29×10⁶ psi.

| Angle (vertical × horizontal × t, in) | Weight (lb/ft) | S (in³) | I (in⁴) | Span | Table (lb/ft) | Recomputed | Governs |
|---|---|---|---|---|---|---|---|
| 2 × 2½ × ¼ | 3.6 | 0.25 | 0.372 | 3 ft | 352 | 351.6 | deflection |
| 2½ × 3½ × ¼ | 4.9 | 0.41 | 0.777 | 3 ft | 664 | 663.5 | moment |
| 2½ × 3½ × ¼ | 4.9 | 0.41 | 0.777 | 4 ft | 308 | 308.1 | deflection |
| 3½ × 3½ × ¼ | 5.8 | 0.79 | 2.01 | 3 ft | 1,281 | 1,281.6 | moment |
| 3½ × 3½ × ¼ | 5.8 | 0.79 | 2.01 | 4 ft | 718 | 718.4 | moment |
| 6 × 3½ × ⅜ | 11.7 | 3.24 | 12.90 | 4 ft | 2,958 | 2,958.3 | moment |

---

## D2. Bending and lateral-torsional buckling of single angles (AISC 360-16)

All of this section is [H7] Verified, from the Specification's Table B4.1b (p. 16.1-18), §F1 and
§F10 (pp. 16.1-46 to 16.1-65) and §H2, and Commentary pp. 16.1-341 to 16.1-344. The equations were
read from rendered pages, because the text layer garbles them.

- **F1:** φb = 0.90 (LRFD), Ωb = 1.67 (ASD). The allowable moment is Mn/Ωb.
- **Restraint:** "Single angles with continuous lateral-torsional restraint along the length are
  permitted to be designed on the basis of geometric axis (x, y) bending. Single angles without
  continuous lateral-torsional restraint along the length shall be designed using the provisions for
  principal axis bending except where the provision for bending about a geometric axis is permitted."
- **Yielding:** Mn = 1.5My (F10-1).
- **Lateral-torsional buckling:**
  - When My/Mcr ≤ 1.0: Mn = (1.92 − 1.17√(My/Mcr))My ≤ 1.5My (F10-2).
  - When My/Mcr > 1.0: Mn = (0.92 − 0.17Mcr/My)Mcr (F10-3).
- **Major principal axis:** Mcr = (9EArztCb/8Lb)[√(1 + (4.4βw rz/Lb t)²) + 4.4βw rz/(Lb t)]
  (F10-4). Cb comes from F1-1 with a maximum of 1.5, and βw = 0 for equal-leg angles.
- **Equal-leg angle bent about a geometric axis, with no axial compression and no lateral-torsional
  restraint:**
  - Maximum compression at the toe: Mcr = (0.58Eb⁴tCb/Lb²)[√(1 + 0.88(Lb t/b²)²) − 1] (F10-5a).
  - Maximum tension at the toe: the same with "+ 1" (F10-5b).
  - "My shall be taken as 0.80 times the yield moment calculated using the geometric section
    modulus."
- **Restraint at the point of maximum moment only:** Mcr is 1.25 times F10-5a or F10-5b, and My is
  the full geometric yield moment.
- **User note:** "Mn may be taken as My for single angles with their vertical leg toe in
  compression, and having a span-to-depth ratio less than or equal to (1.64E/Fy)√((t/b)² − 1.4Fy/E)"
  (transcribed from the rendered page).
- **Leg local buckling** (toe in compression):
  - Compact legs: does not apply.
  - Noncompact legs: Mn = FySc[2.43 − 1.72(b/t)√(Fy/E)] (F10-6).
  - Slender legs: Mn = FcrSc with Fcr = 0.71E/(b/t)² (F10-7, F10-8).
  - "For bending about one of the geometric axes of an equal-leg angle with no lateral-torsional
    restraint, Sc shall be 0.80 of the geometric axis section modulus."
- **Leg slenderness**, Table B4.1b case 12, legs of single angles in flexure: λp = 0.54√(E/Fy) and
  λr = 0.91√(E/Fy). E = 29,000 ksi.
- **Combined bending** about both principal axes, such as a skewback angle carrying vertical and
  horizontal load: |fra/Fca + frbw/Fcbw + frbz/Fcbz| ≤ 1.0 (H2-1).
- **Commentary:** for unrestrained bending of an equal-leg angle, "the resulting maximum normal
  stress at the angle tip ... will be approximately 25% greater than the calculated stress using the
  geometric axis section modulus". For longer members "deflections are likely to control rather than
  lateral-torsional buckling or leg local buckling strength."

Derived for A36 (Fy = 36 ksi):
- √(E/Fy) = 28.38, so λp = 15.3 and λr = 25.8.
- b/t: L2×2×¼ is 8 and L3×3×¼ is 12 (compact). L3×3×3/16 and L4×4×¼ are 16 (noncompact).
  L4×4×5/16 is 12.8 (compact).
- A gravity-loaded lintel angle with its horizontal leg at the bottom has the toe of its vertical leg
  in compression. The user-note span-to-depth limit is (1.64 × 805.6)√(0.0039 − 0.00174) = 61 for
  L4×4×¼ and 95 for L3×3×¼. Kiln doors are well inside it: spans under 4 ft over 3 to 4 in angles
  give span/depth of about 6 to 16.
- So an unbraced equal-leg lintel angle with a compact leg can be checked at
  Ma = 0.8FySx/1.67 = 17.2 ksi × Sx, against BIA's 22 ksi for a braced one. A noncompact leg also
  needs the F10-6 check.
- Worked check, L4×4×¼ over Lb = 28 in, Cb = 1:
  - My = 0.8 × 36 × 1.03 = 29.7 kip·in.
  - Mcr (F10-5a) = 111 kip·in, so My/Mcr = 0.27 and Mn(LTB) = 39.0 kip·in.
  - Leg buckling (F10-6) gives 43.3 kip·in. Mn = 39.0 and Ma = 23.4 kip·in.
  - Section properties are from `kiln-hardware.md` §4.7.1.

---

## D3. Masonry arches over openings (BIA TN 31, 31A, 31C)

### D3.1 Practice and terms (TN 31, 1995) [H2] Verified

| Item | Value |
|---|---|
| Relieving arch | "An arch built over a lintel, jack arch or smaller arch to divert loads, thus relieving the lower arch or lintel from excessive loading. Also known as a Discharging or Safety arch." |
| Abutment | "The masonry or combination of masonry and other structural members which support one end of the arch at the skewback." |
| Thrust | "Thrust develops in all arches and the thrust force is greater for flatter arches. The thrust should be resisted so that lateral movement of the abutment does not cause failure in the arch." Abutments fail by "excessive lateral movement of the abutment or exceeding the flexural, compressive or shear strength of the abutment" |
| Minimum depth (a rule of thumb for appearance, not for strength) | "Because aesthetics of an arch are subjective, there are no hard rules for this." Segmental and semicircular arches: "1 in. (25 mm) for every foot (300 mm) of arch span or 4 in. (100 mm), whichever is greater". Jack arches: "4 in. (100 mm) plus 1 in. (25 mm) for every foot (300 mm) of arch span or 8 in. (200 mm), whichever is greater". "For structural arches, a minimum arch depth is determined from the structural requirements. If the arch is supported by a lintel, any arch depth may be used." |
| Keystone | "the likely location of the first crack when the arch fails is at the mortar joint nearest to the midspan of the arch" |
| Joints | mortar joints in arches 1/8 in. minimum, 3/4 in. maximum |
| Expansion joints | "Vertical expansion joints should not be placed in the masonry directly above a structural arch" or "in close proximity to the springing", because they reduce "the effective width of the abutment and its ability to resist horizontal thrust" |
| Centering | "Centering should remain in place for at least seven days after construction of the arch." |
| Unreinforced | "Very long span arches and arches with a small rise may require steel reinforcement to resist tensile stresses." |

### D3.2 Minor arches: scope and loading (TN 31A) [H3]

All Verified (scan) unless marked.

- "Minor arches are those whose spans do not exceed 6 ft and with maximum rise-to-span ratios of
  0.15." Major arches exceed either limit. The p. 1 text layer is Verified, checked on the scan.
- Load: "The dead load of a wall above an arch may be assumed to be the weight of wall contained
  within a triangle immediately above the opening. The sides of this triangle are at 45-deg angles to
  the base. Therefore, its height is ½ of the span. Such triangular loading may be assumed to be
  equivalent to a uniformly distributed load of 1⅓ times the triangular load."
- "Superimposed uniform loads above this triangle may be carried by arching action of the masonry
  wall itself. Uniform live and dead loads occurring below the apex of the triangle are applied
  directly upon the arch for design purposes."
- "Heavy concentrated loads should not be allowed to bear directly on minor arches. This is
  especially true of jack arches. Minor concentrated loads bearing on, or nearly directly on, the
  arch may safely be assumed to be equivalent to a uniformly distributed load equal to twice the
  concentrated load."
- Assumptions, from the "hypothesis of least crown thrust": "1. The thrust at the crown is horizontal
  and passes through the upper ⅓ point of the arch. 2. The reaction passes through the lower ⅓ point
  of the arch at the skewback. 3. The equilibrium polygon lies completely within the middle ⅓ of the
  arch."

### D3.3 Failure checks and formulas (TN 31A) [H3] Verified (scan)

- Three failure modes: "(a) by rotation of one section of the arch about the edge of a joint; (b) by
  the sliding of one section of the arch on another or on the skewback; (c) by crushing of the
  masonry." Rotation is excluded by keeping the line of thrust in the middle third.
- **Sliding:** "The coefficient of friction between the units composing a brick or tile masonry arch
  is at least 0.60, without considering the additional resistance to sliding resulting from bond
  between mortar and the masonry units. This corresponds to an angle of friction of approximately 31
  deg."
  - Printed as β = tan⁻¹(W/2H − γ) (1). β is the angle between the line of resistance and the
    normal to the joint, W the total equivalent uniform load, H the crown thrust and γ the angle of
    the joint with the vertical.
  - Read geometrically it is β = tan⁻¹(W/2H) − γ **(derived; the printed brackets put γ inside)**.
  - For segmental arches the angle is greatest at the skewback.
- **Skewback angle:**
  - Segmental arch with radial joints: γ = tan⁻¹[4rS/(S² − 4r²)] (2), or γ = sin⁻¹(S/2R) (3).
  - Jack arch with the standard skewback: γ = tan⁻¹(S/8) (4).
  - S is the span, r the rise and R the radius. In (4) S is in feet, because the skewback is ½ in. per
    foot of span for each 4 in. of depth, so tan γ = K/d = S/8 **(derived)**.
- **Segmental arch, crushing:**
  - Fig. 3 plots thrust coefficients H/W against S/d (2 to 7) for S/r = 7, 8, 9, 10, 11 and 12, for a
    uniform load over the whole span.
  - S/r and S/d use the clear span, the rise of the soffit and the depth of the arch, all in the same
    units.
  - "If the applied load is triangular or concentrated, the above method may still be used, but the
    horizontal thrust coefficient must be increased by ⅓ for triangular loading and doubled for
    concentrated loads."
  - fm = 2H/bd (5), with fm in psi, H in lb, and b (breadth) and d (depth) in inches. "This value is
    twice an axial compressive stress on the arch, due to a load H, because the horizontal thrust is
    located at the third point of the arch depth."
- **Jack arch:**
  - "The common rule for jack arches is to provide a skewback (K, measured horizontally) of ½ in. per
    ft of span for each 4 in. of arch depth. Jack arches are commonly constructed in depths of 8 and
    12 in. with a camber of ⅛ in. per ft of span."
  - Uniform load over the full span: H = 3WS/8d (6). Triangular load over the full span: H = WS/2d
    (7).
  - fm = 2H/bd (8), or directly fm = 3WS/4bd² (9, uniform) and fm = WS/bd² (10, triangular). Here W
    is the total load in lb, and S, d and b are in inches.
  - "Formulae 8, 9 and 10 include a factor which allows for non-axial loading."
- A kiln door of 18 to 36 in is inside the 6 ft span limit. Whether it is inside the 0.15
  rise-to-span limit depends on its rise. Heat is outside every BIA assumption (§D3.7)
  **(derived reading)**.

### D3.4 Segmental thrust coefficient in closed form (derived)

From the three assumptions in §D3.2, take the crown thrust at the upper third point of the crown
section and the reaction at the lower third point of a radial skewback. Moments about the reaction
point for half the arch under a uniform load W then give:

- R = (S²/4 + r²)/2r, sin ½θ = S/2R
- x = S/4 + (d/3) sin ½θ (lever arm of the half load W/2)
- z = r + 2d/3 − (d/3) cos ½θ (lever arm of H)
- **H/W = x/(2z)**

Checked against Fig. 3, read off the rendered chart to about ±0.01:

| S/r | S/d = 2: formula | S/d = 2: chart | S/d = 7: formula | S/d = 7: chart |
|---|---|---|---|---|
| 7 | 0.505 | ≈0.505 | 0.696 | ≈0.695 |
| 8 | 0.528 | ≈0.53 | 0.764 | ≈0.765 |
| 10 | 0.562 | ≈0.565 | 0.887 | ≈0.885 |
| 12 | 0.587 | ≈0.59 | 0.994 | ≈1.00 |

At S/r = 10 and S/d = 5 the formula gives 0.802 and the chart about 0.80. The engine can use the
formula with this working, and refuse outside the chart's range (S/r 7–12, S/d 2–7).

### D3.5 What resists the thrust (TN 31A) [H3] Verified (scan)

- "Resistance to horizontal thrust, developed by the arch, is provided by the adjacent mass of
  masonry. In areas where limited masonry is available, i.e. corners, openings, etc., it may be
  necessary to check the resistance of the wall to the horizontal thrusts."
- Fig. 4: the thrust "attempts to move a volume of masonry enclosed by the boundary lines ABCD. For
  calculating purposes the area CDEF is equivalent in resistance." The thrust acts against two shear
  planes.
  - Resisting thrust Hr = vm·n·x·t (11).
  - Minimum distance from a corner or opening: x = H/(vm·n·t) (11a).
  - vm is the allowable shear stress, n the number of shear planes, x the distance from the centre of
    the skewback to the end of the wall, and t the wall thickness (in, lb, psi).
- Allowable shear for unreinforced building brick walls (Table 2): 50 psi with type M or S mortar and
  40 psi with type N. The source is SCPI's *Recommended Building Code Requirements for Engineered
  Brick Masonry* (1966).
- Overturning: "The tendency for arch thrust to overturn a section of masonry, rather than slide it
  or rack it, must also be investigated. In general, such overturning forces are found to govern only
  at arches near the top of a wall, since that portion of masonry which tends to overturn must first
  become separated from the body of the wall." This is the kiln case: a door arch a few courses below
  the roof.
- Steel or other non-masonry abutments: "rigidity of the non-masonry structural member and rigidity
  of the ties are very important" [H2] Verified.
- Tie rods across a door arch: no BIA note mentions them. **NOT FOUND.**
- vm for refractory masonry, whether dry-laid or in refractory mortar: **NOT FOUND.**
- Using BIA's friction coefficient of 0.60 for a dry-laid jamb (resistance = 0.60 × the weight above
  the sliding plane) would be an extrapolation. BIA states it for brick or tile arch joints,
  excluding bond.

### D3.6 Major and semicircular arches (TN 31A, 31C)

- Loads on major arches [H3] Verified (scan):
  - "It is often assumed that the entire weight of masonry, above the soffit, presses vertically upon
    the arch. This certainly is not accurate, since even with dry masonry a part of the wall will be
    self-supporting. However, this assumption is certainly on the safe side."
  - "For low rise arches, f/L = 0.2 or less, a uniform load may be assumed. This load will be the
    weight of wall above the crown of the arch up to a maximum height of L/4."
  - Higher-rise arches take uniform plus complementary parabolic loading. The parabolic part's maximum
    ordinate is the weight of a wall as high as the rise, and its minimum is zero. The uniform part is
    the wall above the crown "up to a maximum height of L²/100". The worked example shows L in ft:
    (80)(20²/100) = 320 lb per ft.
  - "Small concentrated loads may be treated as uniform loads of twice the magnitude."
- The major-arch method uses Leontovich, *Frames and Arches* (1959). Its constants are tabled only for
  f/L 0.2–0.6 (Tables 3–6). Leontovich was not read. "No tensile stresses should be permitted in
  unreinforced masonry arches under static loading conditions." [H3] Verified (scan).
- Semicircular arches (TN 31C) [H4] Verified:
  - The spring line is assumed "one fourth the span length above the horizontal axis", and the arch
    is fully restrained there.
  - The uniform-load tables (1-in. thick ring) cover loads between 0.90L and 0.70L above the
    horizontal axis. Loads above 0.90L "may be ignored ... provided arching action occurs".
  - There must be "a minimum height of masonry (line 3) equal to 0.70 L above the horizontal axis. No
    superimposed loads are permitted below this line." "The maximum design height of masonry is 0.25
    L above the crown".
  - Thrust is checked by TN 31A Fig. 4, with vm = 40 psi.
  - "Any segmental arch with f/L' > 0.29 but < 0.50 can be considered as an equivalent semicircular
    arch". The tables themselves (images) were not transcribed.

### D3.7 Limits for the engine (ADR 0009)

- The minor-arch method is limited to spans of 6 ft or less and a rise of at most 0.15 of the span.
  Fig. 3 covers only S/r 7–12 and S/d 2–7 [H3].
- A kiln door arch with a 2 in/ft rise has r/S = 0.167 (S/r = 6) **(derived)**. That is a major arch
  in BIA's terms and is outside Fig. 3.
- Every BIA number is for cold building masonry. The thrust of a heated door arch is **NOT FOUND**.
  HarbisonWalker's Hmax factors (`kiln-hardware.md` §4.3) cover roof arches with T/S of 4–10 %. A
  4½ in door arch over 24 in has T/S = 19 % **(derived)**, outside them.

---

## D4. Kiln and furnace practice at the head of a door

| Source | Practice | Mark |
|---|---|---|
| Rhodes, *Kilns* (1968) [H10] (= [S34]) | "The sides and jambs of kiln doors should be built with hard firebrick. It is best to arch over the door. This is done in the same way as the main arch is built. A wooden form is constructed to hold up the arch during construction, and skewbacks are prepared. The thrust of the door arch is slight compared to the main arch over the kiln, and the mass of the walls furnishes sufficient buttress." | Excerpt |
| Rhodes [H10] | "The door should not be on the side of the kiln supporting the arch, and it should be high enough so no dead pocket is formed just above the door where no ware can be set. Often, the whole front of the kiln is considered a door, or the door is without an arch or lintel buttress and is bricked up each time past the main arch. For convenience, doors are often built in steel frames hinged to the steel braces of the [kiln]" | Excerpt |
| Rhodes [H10] | "arches over flue holes, doors, and crowns are more of a problem. To bridge over small openings such as burner ports, a brick is used as a lintel. This will serve to bridge over holes up to six inches across. For larger openings, the corbel arch may be used ... Corbel arches are not practical for openings more than about 18 inches across. Sometimes special shapes longer than nine inches are used to form a lintel over openings." | Excerpt |
| Berggren (1968) [H14] (= [S7]) | When the 27 in ceiling arch was turned 90° ("Ceiling Design B"), "the arch weight was transferred from the interior wall to the exterior wall of fire brick", and "A side of the kiln was used to serve as a door for this change in direction of the arch, since the previously discussed front supported one side of the ceiling arch." The door moved out of the springing wall | Verified (OCR) |
| Pitelka [H12] (= [S11], [S4]) | The doors are in the end walls; the arch springs from the side walls. With a stacked door and an arch the inside depth only, "the stacked door simply overlaps the front of the arch at the top". During construction the rear wall and door jambs are left "one brick shorter" to carry the arch form, then built up. On the soda kiln, "The vertical angle-iron member to the right of the kiln door is very important. This is a high stress area, and without that vertical, the stub-wall will often warp or lean outwards with time." A 9 in wide flue opening is roofed by a corbel (the third course projects 2 in each side to carry straights), or "Another option is to cast a slab with Mizzou castable to span the opening" | Verified |
| Olsen, *The Kiln Book* (2001) [H11] | Climbing kiln: "The door arch frame support is made to span the door jamb, and the door ring arch is laid in exactly the same way as ..."; "Another ring arch, resting on top of the door arch, is then laid." "When the skewback, wall, and arch form an acute angle, steel supports must be used to hold the stress of the ...". "Special care must also be taken in sizing the door and door frame angle iron. If the angle iron is undersized and the door extremely heavy, the weight will torque the arch and cause it to break its bond." A leaking seal goes on "until the seal is completely destroyed, and oxidation and warping of the door frame begin." A steel list (which kiln it belongs to is not in the snippet): "door frame 3" x 3" x 1/4" — skewback brace 2" x 2" x 1/4"" | Excerpt |
| HarbisonWalker guide (2008) [H8] (= [S20]) | "In some application, arches span wall openings, and sometimes they carry the weight of walls or checkerwork." "The vertical force may be carried by steel beams or by the furnace walls or a combination of walls and steel buttresses." "When the skewback is carried on a channel or angle, the line of thrust should pass through, or slightly above, the corner of the supporting steel." It lists skewbacks with cut-outs for a steel angle or channel (`kiln-hardware.md` §5.2) | Verified |
| Harbison-Walker, *Modern Refractory Practice* (1950) [H9] | "WALL ARCHES The term 'wall arches' may be used to designate relieving arches, and arches over firing door and charging door openings, ports and the like. The rise of wall arches can safely be made higher than that of roof arches, because the tendency to buckle is resisted by the weight of the overlying brickwork. Consequently wall arches are frequently made semi-circular." "In arches spanning wall openings, the stresses are supported by resistances within the wall." | Excerpt |
| Harbison-Walker 1950 [H9] | "In spanning wall openings or narrow flues, a sprung arch is generally better than a flat tile, for the arch brick are under compression, while the lower face of the tile is under tension. Moreover, a tile spanning an opening between two parallel walls may shear or spall, if the walls are heated and cooled at different [rates]". "A wall opening spanned by a flat arch has a rectangular cross-section ... A jack arch such as illustrated is structurally weak and should be used only for narrow spans. For best construction, a large number of special shapes is required." The jack arch's shapes are laid out "by first laying out a radial sprung arch of proper rise and thickness for the given span" | Excerpt |
| Norsker (1987) [H13] (= [S14]) | "Arches are used to bridge doors, flues and fireboxes". "A relieving arch is used to remove the load from the main arch. Normally it is rarely used. However, the firebox shown in fig. 2-92 benefits from having a relieving arch above, which would carry the load of the kiln wall. ... The important feature is the gap between the relieving and the main arch which ensures that no weight is being carried by the main arch. A loose filler ... can be used to fill the gap." | Verified (OCR) |
| Norsker [H13] | Round kilns: "The inner lining should preferably not support the dome which instead is made to rest on the outer wall ... the wall, only carrying its own weight, can be made from light insulating bricks. The outer, dome-supporting wall should have twice the thickness of the inner lining". Inner linings are 10 cm for diameters up to 2 m, 15 cm for 2–3 m and 23 cm above 3 m | Verified (OCR) |
| Searle, *Modern Brickmaking* (1911) [H15] | Industrial brick kilns: "Flattened arches are, therefore, to be avoided, as are also those with a very pronounced point. In almost every case the true semi-circle is the best form of arch." The wicket (door) arch is "of a semi-circular or Roman type. The distance r should never be less than 20 in. so as to allow ample room for the men to enter the kiln". The crowns of round kilns are part of a true circle, "though not a complete semi-circle" | Verified (OCR) |
| US 4,977,838, M. H. Detrick Co. (1990) [H16] | An industrial furnace door: "vertical steel beams 18 along the sides of the access opening, and a upper horizontal steel I-beam 20 along the top of the access opening". The lintel is "an assembly including a cross support member, such as an external steel beam, and a top wall of refractory brick hanging from the cross support member", with "interlocking refractory bricks shaped such that a lower layer of bricks hangs from an upper layer" | Verified |
| Giles (c. 1940) [H23] | Reinforcing refractory concrete with angle iron: "one flange of the angle is exposed to the air for rapid dissipation of the heat to maintain a low temperature in the steel." "It is commonly accepted that brick walls of 4½" thickness are not suitable for heights greater than about 3 feet, while 9" brick walls should be limited to a height of 8 feet; 13½" brick walls to a height of 12 feet" | Verified (OCR; 4½ checked on scan) |

What this settles, and what it does not:
- **A door in a sprung arch's springing wall:** Rhodes says not to put it there, and Berggren moved
  his door when he turned his arch. Industrial practice carries a skewback over a wall that cannot
  take it on steel (HarbisonWalker 2008, and the -A and -C skewbacks with cut-outs for steel).
  No studio source sizes a skewback beam spanning a door. **NOT FOUND.**
- **A door in an end wall under a sprung arch:** the end wall carries no roof (Pitelka, Rhodes'
  "bricked up each time past the main arch").
- **Dome kilns:** door arches are usually semicircular (Searle; Harbison-Walker 1950). Norsker puts
  the dome on an outer wall, not on the IFB lining.
- **Car kilns:** header details for a studio car kiln are **NOT FOUND**. The industrial analogue is an
  exterior steel beam over the opening, with the refractory hung from it [H16].

---

## D5. Refractory lintels: practice and strength

### D5.1 Strength data (all from the makers' sheets)

MOR and CCS are "after" heating to the stated temperature. That is the usual ASTM C133 cold test
after firing; the sheets do not state it. No sheet read gives a hot MOR (ASTM C583) at temperature.
HWI: "The test data shown are based on average results on production samples and are subject to
normal variation on individual tests. The test data cannot be taken as minimum or maximum values for
specification purposes." [H17] [H18] [H19] Verified.

| Product | Density (lb/ft³) | MOR (psi) | CCS (psi) | Under load when hot | Mark | Source |
|---|---|---|---|---|---|---|
| Kast-O-Lite 30 LI Plus (HWI 10/19, 5874) | 98 after 220 °F; 92 after 1,500 °F | 600 after 220 °F; 300 after 1,500; 300 after 2,000; 900 after 2,500; 800 after 2,910 | 2,700; 2,300; 1,300; 2,000; 1,800 (same temperatures) | not given | Verified | [H17] |
| Mizzou Castable Plus (HWI 12/12, 5976) | 142 after 220 °F; 140 after 1,500 °F | 1,100 after 220 °F; 800 after 1,500; 600 after 2,000; 1,100 after 2,500 | 5,500; 3,500; 3,000; 4,000 | not given | Verified | [H18] |
| KX-99 super-duty fireclay brick (HWI 6/12, 5912) | 142 | 1,700 | 5,000 | "Hot Load Test Deformation at 2640°F (1450°C)" 0.6 % (load not printed). Creep at 28.4 psi: 0.2 % subsidence between 20 and 50 h at 2,192 °F | Verified | [H19] |
| K23 IFB (Morgan, 2025) | 32.0 | 114.5 (0.79 MPa) | 145 (1 MPa) | — | Verified | [H20] |
| K25 / K26 IFB (Morgan, 2025) | 38.5 / 41 | 137.7 / 130.5 | 188.5 / 188.5 | — | Verified | [H20] |
| K-23 (Morgan, 01:2013) | 31–35 | 115 | 145 | ASTM C16 at 10 psi: 0 % after 1½ h at 2,000 °F; 0.3 % after 1½ h at 2,200 °F (K-25: 0 and 0.1 %) | Verified | [H22] |
| JM23 / JM26 / JM28 / JM30 IFB (Morgan, 2025) | 30.0 / 49.9 / 55.5 / 63.6 | 145 / 217.5 / 261 / 290 | 145 / 232 / 304.5 / 333.5 | — | Verified | [H21] |

- These sheets confirm several values that `combustion-and-masonry.md` §6.1 and
  `electric-and-thermal.md` §4.5 hold only as snippets:
  - Kast-O-Lite 30 LI Plus: the MOR row; water "Weight 17.0%", 9.4 lb per 55 lb bag; k of 5.6, 4.2,
    4.1, 4.5 and 4.9 Btu·in/hr·ft²·°F at 400, 800, 1,200, 1,600 and 2,000 °F [H17].
  - Mizzou Castable Plus: "Material Required 140 lb/ft3 (2.24 g/cm3)"; bulk density 142 and 140; k of
    7.8, 7.7, 7.6, 7.5, 7.4 and 7.4 at 400, 800, 1,200, 1,600, 2,000 and 2,400 °F; water 8.6 %
    (vibration casting) or 9.0 % (hand casting) [H18].
  - All Verified. They fill the "NOT FOUND" material and k cells for Mizzou in
    `combustion-and-masonry.md` §6.1.
- **Factor of safety on MOR for a refractory beam or lintel: NOT FOUND.** The two sources that touch
  on it give no number:
  - Giles: "This will represent the ultimate strength, to which a suitable factor of safety should be
    applied." [H23] Verified (OCR).
  - A reformer-tunnel patent: "Proper material selection preferably includes confirming that the
    modulus of rupture at the service and excursion temperatures of the furnace has a sufficient
    safety factor when compared to the associated static load stresses." "Knowing the room
    temperature MOR of a refractory material alone is not sufficient for proper design of a tunnel
    system." [H24] Verified.

### D5.2 Heat matters more than load (patent text, patentee's own analysis)

[H24] Verified. The patent's numbers have not been checked.
- A 9 × 9 × 42 in solid lid at a constant 1,900 °F, under its own weight only: "The result is a
  maximum stress of a very modest 10 psi."
- The same lid at 1,910 °F on top and 1,900 °F underneath: "A differential temperature of 10 degrees
  across the lid results in a max stress of 1500 psi, which is above the HMOR of lower end refractory
  materials." The patent concludes "most lid failure is not a result of static load alone".
- "The HMOR of commonly used refractory mortars is roughly 500 psi".
- IFB under load: "a load on the supporting IFB layer of 11.6 psi" (6 in walls 96 in tall under a
  9 in lid) means "the base IFB layer will deform a full 1% under those loads in 100 hours" at
  reformer temperatures.
- "ASTM tests on Super Duty Brick have published results of a 7.86% deflection at 2,600° F."
- Check of the 10 psi (derived): 150 lb/ft³ assumed, simple span 42 in. Then w = 81 × 150/1728 =
  7.0 lb/in, M = 7.0 × 42²/8 = 1,550 lb·in, S = 9 × 9²/6 = 121.5 in³ and σ = 12.8 psi, the same
  order as the patent's figure.

### D5.3 Practice limits

- Rhodes: a brick lintel up to 6 in; a corbel up to about 18 in; special shapes longer than 9 in
  above that (§D4) [H10] Excerpt.
- Harbison-Walker 1950 prefers a sprung arch to a flat tile over wall openings (§D4) [H9] Excerpt.
- Giles: "When refractory concrete is dependent wholly upon its own strength it would appear logical
  to limit the dimension of any slab to not more than 4'-0" in any one direction." [H23] Verified
  (OCR).
- Pitelka: a cast Mizzou block 18 × 4½ × 5 in spans a damper slot, replacing two courses
  (`kiln-hardware.md` §3.3) [S4].

A derived check for a refractory beam would be σ = 6M/bh² against MOR ÷ (a factor not found). Given
§D5.2, a pass on dead load alone says little.

---

## D6. Hot steel

| Item | Value | Mark | Source |
|---|---|---|---|
| AISC 360-16 Table A-4.2.1 (for fire design by analysis): ky = Fy(T)/Fy | 68–600 °F "Use ambient properties"; 750 °F 1.00; 800 °F 0.94; 1,000 °F 0.66; 1,200 °F 0.35; 1,400 °F 0.16; 1,600 °F 0.07; 1,800 °F 0.04; 2,000 °F 0.02; 2,200 °F 0.00 | Verified | [H7] |
| kE = E(T)/E | 200 °F 1.00; 400 °F 0.90; 600 °F 0.78; 750 °F 0.70; 800 °F 0.67; 1,000 °F 0.49; 1,200 °F 0.22; 1,400 °F 0.11 | Verified | [H7] |
| kp = Fp(T)/Fy (proportional limit) | 200 °F 1.00; 400 °F 0.80; 600 °F 0.58; 750 °F 0.42; 800 °F 0.40; 1,000 °F 0.29; 1,200 °F 0.13 | Verified | [H7] |
| Carbon steel in refractory concrete (Giles) | "It is important to remember that the temperature of the steel should not exceed 600 deg. F. in any case." "It has not been definitely proven that a temperature somewhat higher than 600 deg. F. could not be used for ordinary carbon steel. However, it is felt that this temperature is conservative". Above it, "special steels should be used" | Verified (OCR; one page checked on the scan) | [H23] |
| Hot bindings (HarbisonWalker) | "many furnace designers limit tensile stress to 12,000 pounds per square inch" | Verified | [H8] (`kiln-hardware.md` §4.3) |

Derived:
- At 600 °F the proportional limit of A36 is 0.58 × 36 = 20.9 ksi. BIA's 22 ksi allowable would sit
  above it.
- HarbisonWalker's 12 ksi stays under the proportional limit up to about 920 °F (kp = 0.333,
  interpolated between 800 °F and 1,000 °F).
- Deflection grows by 1/kE, which is 1.28 at 600 °F.
- Over a 34 in lintel at 500 °F, steel grows 7.8×10⁻⁶ × 430 × 34 = 0.11 in. The bearing has to let
  it slide.

What is missing:
- AISC's table is for fire, which is a short event. Allowable stress or creep for carbon steel held
  hot through repeated firings is **NOT FOUND**; ASME Section II-D was not read.
- Measured temperatures of steel at a kiln door's jamb or head are **NOT FOUND** (the forum thread
  "How hot do 9 inch walls get" returned 403).
- The engine can estimate the steel temperature as the outer-face temperature from its own
  multi-layer conduction model (`electric-and-thermal.md` §6) **(derived approach)**. A hot gas leak
  at the door seal is outside that model: Olsen [H11] reports seals failing until "oxidation and
  warping of the door frame begin" (Excerpt).

---

## D7. The roof's load on the wall over the door, by roof type

A per-roof map of what the header carries. The rules come from §D1–D6; where a step has no source it
says so.

| Roof | Load on the wall over the door | Mark |
|---|---|---|
| Sprung arch, door in an end wall | No roof load. The arch springs from the side walls, and the end wall is built up under it [H12]. The header carries only end-wall masonry above the door, up to the arch soffit | Verified practice + derived reading |
| Sprung arch, door in a side (springing) wall | Not recommended [H10]. If done, a steel skewback beam must span the opening between frame posts. It carries the vertical V = W/2 per foot (plus any wall above) and the horizontal H, rising toward Hmax when hot (`kiln-hardware.md` §4.3). It bends about two axes, checked with AISC H2-1. Sizing rule: **NOT FOUND** | Derived from [H8] [H7] |
| Sail dome on four walls | Every wall carries the dome's edge. How the line load (vertical and thrust) is shared along each wall of a sail dome: **NOT FOUND** (see the round-dome formula below) | NOT FOUND |
| Round (circular) dome | Membrane theory, self-weight g per unit area of shell: Nα = −gR/(1 + cos α) and Nφ = −gR cos α − Nα. The edge ring force is H = a₀Nα cos α₀, with a₀ = R sin α₀ the base radius | Verified [H25] |
| Flat roof in a steel band (laid as a flat or jack arch between two walls) | BIA's jack-arch thrust per strip: H = 3WS/8d (uniform). The band or rods take H; the two springing walls take W/2 each | Verified formula [H3]; its use for a roof is derived |
| Flat roof bearing on all four walls | How the load is shared among the walls: **NOT FOUND** | NOT FOUND |
| Catenary | Doors only in the end walls. The arch stands on its own, so the end walls carry only themselves. As the wall narrows toward the crown, "sufficient masonry on each side" for arching cannot be shown, so count the full height above the door | Derived |
| Car kiln | The header across the opening is a lintel over the full inside width. Under a sprung arch it carries only itself; under a dome or a four-wall flat roof it also carries the roof's edge. Studio details: **NOT FOUND**; industrial: an exterior I-beam with the refractory hung from it [H16] | NOT FOUND / Verified (industrial) |

Worked examples (all derived):

1. **A 24 in door in a 4½ in K-23 end wall, 18 in of wall above, 4 in bearings.**
   - L = 28 in.
   - Arching needs 28/2 + 8 = 22 in of wall above (TEK); 18 in is not enough. So the lintel carries
     the full height: w = 32 × 0.375 × 1.5 = 18.0 lb/ft.
   - M = 147 lb·in, and S = 0.0067 in³ at 22 ksi.
   - An L4×4×¼ allows 23.4 kip·in (§D2) and deflects 0.0002 in against L/600 = 0.047 in.
   - With 26 in of wall above, arching applies: the triangle weighs 16.3 lb and M = 76 lb·in.
   - Strength never governs in IFB. Temperature and minimum sizes do.
2. **A 30 in door in a 9 in wall of dense brick (142 lb/ft³), 4 in bearings, L = 34 in.**
   - With 30 in of wall above, the wall arches (it needs 25 in) and M = 1,211 lb·in.
   - With only 12 in above and a roof line load of 140.2 lb/ft on top (W/2 of case C in
     `kiln-hardware.md` §4.5), there is no arching. Then w = 246.7 lb/ft, M = 2,971 lb·in,
     S = 0.135 in³ at 22 ksi, and each end reacts 349 lb.
   - One unbraced L4×4×¼ (BIA's minimum leg) allows 23.3 kip·in over 34 in. Its deflection is
     0.0064 in after the ×1.56 factor, against L/600 = 0.057 in. An L3×3×¼, whose leg is below
     BIA's minimum, would still allow 14.2 kip·in.
   - BIA would put one angle under each wythe of a solid wall (§D1.5). In the hot inner wythe, though,
     the steel would exceed every limit in §D6.
3. **A segmental door arch: 24 in span, 3 in rise, 4½ in deep, K-23.**
   - S/r = 8 and S/d = 5.33, so H/W = 0.717 (§D3.4).
   - Loads: the triangle weighs 12.0 lb, factored ×4/3; the ring weighs 10.2 lb.
   - H = 18.8 lb, fm = 2H/bd = 1.9 psi, γ = 28.1° and β = 2.5°, well under 31°.
   - Cold dead load is trivial. The real unknowns are hot thrust and jamb overturning near the wall
     top (§D3.5).
4. **A flat IFB roof laid as a jack arch: 36 in span, 4½ in thick, per foot of kiln.**
   - W = 36 lb, H = 3WS/8d = 108 lb per foot of roof, and fm = 4.0 psi.
5. **A round dome: 48 in diameter, 12 in rise, 4½ in K-23 (g = 12 lb/ft²).**
   - R = 30 in and α₀ = 53.1°.
   - Nα = 18.75 lb/ft, so the thrust on the wall is 11.25 lb/ft and the vertical load 15.0 lb/ft.
   - Check: 15.0 lb/ft × the 12.57 ft perimeter = 188.5 lb, the weight of the cap.

---

## D8. Gaps (not found)

- **Refractory masonry allowable stresses.** Allowable compressive, bearing and shear stress for IFB
  or hard firebrick, dry-laid or in refractory mortar, cold or hot. BIA's tables are for building
  brick.
- **Refractory beams.** A factor of safety on MOR for a refractory lintel or beam. Hot MOR (ASTM C583)
  for Kast-O-Lite 30 LI Plus, Mizzou Castable Plus, KX-99 and K-23. The load used in KX-99's
  hot-load test.
- **Arching in kiln walls.** Whether BIA/MSJC arching applies to a dry-laid or hot refractory wall,
  and how much masonry beside an opening is "sufficient" to take the arching thrust.
- **Hot door arches.** Thrust in a heated door arch. HarbisonWalker's Hmax covers roof arches with
  T/S 4–10 % only. Tie rods across door arches.
- **Roof edge loads.** How a sail dome's edge load (vertical and thrust) is shared along each wall.
  How a flat roof bearing on four walls shares its load.
- **Steel carrying it all (2026-10-30).** A steel lintel that carries everything above an
  opening needs no refractory allowable stress except at its end bearings, which stay NOT FOUND;
  the hot-steel method, and how Olsen's dome kilns span their doors (ring arches in buttressed
  walls, no steel lintel), are in `steel-design.md`.
- **Skewback over a door.** A sizing rule for a skewback beam spanning a door in a springing wall.
  HarbisonWalker gives only detailing.
- **Car kilns.** Header construction for a studio car kiln: steel size, span, hung or arched.
- **Hot steel.** Measured steel temperatures at kiln door jambs and heads. Allowable stress or creep
  for carbon steel in continuous hot service (AISC Appendix 4 is for fire; ASME II-D was not read).
- **Unread references.**
  - TMS 402-16 itself (its provisions are taken here from TMS's own slides and CMHA's TEK).
  - The BIA 31C load tables and Leontovich's *Frames and Arches*.
  - BIA TN 17H on reinforced brick lintels.
- **Kiln books.** Olsen, Rhodes, Cardew (*Pioneer Pottery*) and Gregory (*Kiln Building*) were
  searched by snippet only. None gives a sizing rule for a door header. Cardew's snippets had nothing
  on door arches.
- **Search of 29 October 2026, still NOT FOUND.** A web search for a refractory lintel's allowable
  stress, a factor of safety on MOR or hot strength for an arch over an opening returned only
  building-masonry guidance (CMHA TEK 17-01D and 17-02A, TMS's ASD course) and ISO 5014:2025, which
  measures MOR at room temperature only. The makers' sheets already read (HWI, Morgan, [H17]–[H22])
  give cold MOR and crushing strength and, for KX-99, a hot-load deformation without its load; none
  gives a hot MOR or a design stress. So the engine keeps refusing a door below a roof with a lintel
  or door arch that would have to carry it: there is nothing to check the design against. What
  would unblock it: hot MOR (ASTM C583) on a maker's sheet for the materials a header is made of,
  and a published factor of safety on it (the HWI *Modern Refractory Practice* [H9] is the likeliest
  place; it is borrow-only and was not read).

---

## D9. The engine's statics for an arched door head and its jambs (2026-10-30, derived)

HarbisonWalker's roof-arch method stays out of reach (§D3.7: a door arch's T/S is 15–45 %, its
table 4–10 %), so the engine uses Heyman's limit analysis, which is geometry and statics alone
and needs no checked range (`arch-thrust-theory.md` §2; `domes-over-doors.md` §D3). Every step
is a formula sheet (`frame_checks.py`, `frame.door-arch`, `frame.door-jamb`,
`frame.door-bearing-*`):

1. **The ring.** A semicircle of inside radius r = S/2, laid as the roof's ring (Olsen, Rhodes,
   §D4: "in the same way as the main arch"; a roof with no ring leaves the door unchecked). Its
   depth d against the thinnest semicircle that holds a line of thrust under its own weight,
   t/r_m = 0.10743 (Couplet–Heyman, `steel.yaml`), with Heyman's factor of about 2.
2. **The load.** The whole wall over the soffit, up to the wall's inside top over the door's
   middle, bears on the arch: BIA's "certainly on the safe side" (§D3.6); the roof's edge load
   (§D7) on top. The ring must fit under the wall's top (Z ≥ R_o).
3. **The thrusts.** Half the arch is cut into a grid; at each radial joint (every ½°) the load is
   the ring nearer the crown and the wall standing on it, cut by a plumb line (a wall's head
   joints are upright). The least thrust is the line from the crown's extrados touching the
   intrados; the most, from the crown's intrados touching the extrados ([A1]–[A3]). A line fits
   in the ring when least ≤ most.
4. **The jamb.** A jamb that gives a little lets the arch settle to its least thrust ("an arch on
   spreading supports will act in a state of minimum thrust", [A1]), so that is what it holds.
   The jamb is its own strip of wall from the door's edge to the next door or the wall's outside
   end. Where that end is the wall's corner, the cross wall bonded into it is part of BIA's
   "adjacent mass of masonry" (§D3.5); the engine counts only a length of it equal to the jamb
   wall's thickness b, the jamb's full height, its weight at the cross wall's middle (G₃ =
   q_c·b·(h_s + Z) at e − b_c/2). That length is a cautious design rule, not a sourced one: a
   corner bond laps the courses about one wall's thickness, and the rest of the return is spare.
   A partition wall bonded in between two doors is not counted. With the springing's load where
   the line crosses the springing, the jamb's weight under the springline and the wall over it
   beside the ring, the resultant at the jamb's base must lie within it (error) and within its
   middle third (warning: no tension, [D7], BIA TN 31A §D3.2).
5. **Sliding** at the springing's level joint: H_min/N ≤ 0.60, BIA's friction between brick
   masonry units (§D3.3), `frame.door-slide`; for IFB and refractory joints no friction is
   sourced (refractory dry joints 0.50–0.60, Snippet: `refractory-bearing.md` §B4.1). **Not
   checked:** the hot thrust of a door arch held rigidly (it rises toward the most; not sourced
   as a number).
6. **Bearing.** At the springing and the jamb's toe, the triangle of stress 2N/(3·b·a), a the
   resultant's distance to the nearer edge, against the brick's sourced figure at its
   temperature there (`refractory-bearing.md`).

Olsen's built kilns with arched doors in `examples/olsen` (Bidai, Kawaii: doors per chamber in a
side wall, 20 in wide, Fig 4-36) pass: their 9 in rings are 5.8 times the thinnest, the least
thrust under the wall over them about 8 lb, the resultant 3.7–4.0 in into a 10 in end jamb with
the end wall bonded in (2.8–3.2 in without it), and the springing needs friction 0.02 of BIA's
0.60. Their bearing is 31–32 psi at the springing and 18 psi at the jamb's toe: shown, not
checked (`refractory-bearing.md` §B4).

---

## Sources

- [H1] Brick Industry Association, *Technical Notes on Brick Construction 31B, Structural Steel Lintels*, revised, reissued May 1987 (first published Nov/Dec 1981). p. 3 is a scan, read as an image. https://www.gobrick.com/media/file/31b-structural-steel-lintels.pdf
- [H2] Brick Industry Association, *Technical Notes 31, Brick Masonry Arches*, January 1995. https://www.gobrick.com/media/file/31-brick-masonry-arches.pdf
- [H3] Brick Institute of America, *Technical Notes 31A, Structural Design of Brick Masonry Arches*, reissued July 1986 (first published October 1967; footer "R5M©B.I.A. 7/95"). pp. 2–8 are scans (JBIG2), rendered and read as images. https://www.gobrick.com/media/file/31a-structural-design-of-brick-masonry-arches.pdf
- [H4] Brick Industry Association, *Technical Notes 31C, Structural Design of Semicircular Brick Masonry Arches*, rev. Feb 1971, reissued August 1986. https://www.gobrick.com/media/file/31c-structural-design-of-semicircular-brick-masonry-arches.pdf
- [H5] Concrete Masonry & Hardscapes Association (formerly NCMA), *TEK 17-01D, ASD of Concrete Masonry Lintels Based on the 2012 IBC/2011 MSJC*. Page https://www.cmha.org/resource/tek-17-01d/ ; PDF https://www.cmha.org/?create-tek-pdf=1&post_id=521312&filename=TEK%2017-01D
- [H6] The Masonry Society, *Strength Design of Beams* (webinar slides, 2021-02-08), citing TMS 402-16 §§5.2.1.1–5.2.1.4 and Figure CC-5.2-2. https://masonrysociety.org/wp-content/uploads/2021/02/Strength-Design-of-Beams_2021-02-08.pdf
- [H7] AISC, *ANSI/AISC 360-16 Specification for Structural Steel Buildings* (July 7, 2016) with Commentary: §B4 Table B4.1b, §F1, §F10, §H2, Appendix 4 Table A-4.2.1. The aisc.org copy returned 403; read from https://enme.umd.edu/~ccfu/ref/a360-16-spec-and-commentary.pdf (official: https://www.aisc.org/globalassets/aisc/publications/standards/a360-16-spec-and-commentary.pdf)
- [H8] Harbison-Walker Refractories, *Brick Installation Guide* (2008), Arch Construction pp. 13–17 and skewback shapes p. 32. Same as [S20]. https://ssfbs.com/wp-content/uploads/2021/06/HW_Brick_Installation_Guide.pdf
- [H9] Harbison-Walker Refractories Co. (J. S. McDowell, W. F. Rochow), *Modern Refractory Practice* (1950). Borrow-only; Internet Archive full-text-search snippets. https://archive.org/details/modernrefractory0000harb_f4j7
- [H10] D. Rhodes, *Kilns: Design, Construction, and Operation* (Chilton, 1968), about pp. 101–102 (index: "Lintel, 101, 102"; "Corbel arch, 102"). Same as [S34]. Full-text-search snippets of https://archive.org/details/kilnsdesignconst00rhod
- [H11] F. L. Olsen, *The Kiln Book: Materials, Specifications & Construction* (2001). Borrow-only; full-text-search snippets. https://archive.org/details/kilnbook00fred
- [H12] V. Pitelka, *Building a Sprung Arch* (2016) and *Building a 20-Cubic-Foot Cross-Draft Soda Kiln* (2019). Same as [S11] and [S4]. https://www.vincepitelka.com/wp-content/uploads/2016/03/Building-a-Sprung-Arch.pdf ; http://www.vincepitelka.com/wp-content/uploads/2019/12/Building-a-Crossdraft-Soda-Kiln-1.pdf
- [H13] H. Norsker, *The Self-Reliant Potter: Refractories and Kilns* (GATE/Vieweg, 1987), §2.5.6 Arches and the circular-kiln section. Same as [S14]. Internet Archive OCR text. https://archive.org/details/the-self-reliant-potter-refactories-and-kilns
- [H14] M. W. Berggren, *Experimental Study in the Design of a Small Down-Draft Gas Fired Kiln*, thesis, Kansas State University, 1968, pp. 15–19. Same as [S7]. https://archive.org/download/experimentalstud00berg/experimentalstud00berg_djvu.txt
- [H15] A. B. Searle, *Modern Brickmaking* (1911), pp. 316–318. Internet Archive OCR text. https://archive.org/details/modernbrickmakin00searrich
- [H16] K. L. Farrell et al. (M. H. Detrick Co.), US Patent 4,977,838, "Modular door jamb and lintel system for industrial furnaces", filed 1989-08-07, granted 1990-12-18. https://patents.google.com/patent/US4977838A/en
- [H17] HWI, *Kast-O-Lite 30 LI Plus* Product Data 10/19: 5874 (PDF owner-encrypted; read with PyMuPDF). https://ssfbs.com/wp-content/uploads/2021/06/KAST-O-LITE_30_LI_PLUS.pdf
- [H18] HWI, *Mizzou Castable Plus* Product Data 12/12: 5976. https://ssfbs.com/wp-content/uploads/2021/06/MIZZOU_CASTABLE_PLUS.pdf
- [H19] HWI, *KX-99* Product Data 6/12: 5912. https://ssfbs.com/wp-content/uploads/2021/06/KX_99.pdf
- [H20] Morgan Advanced Materials – Thermal Ceramics, *K Insulating Firebrick Series* data sheet, 01 January 2025, code BR.02. https://www.morganthermalceramics.com/media/0wobjak3/k-ifb-series_eng.pdf
- [H21] Morgan Advanced Materials – Thermal Ceramics, *JM Insulating Firebrick Series* data sheet, 01 January 2025, code BR.05. https://www.morganthermalceramics.com/media/5beap13n/jm-ifb-series_eng.pdf
- [H22] Morgan Thermal Ceramics, *K-23, TC-23, IFB 23 Tile, K-25* data sheet, 01:2013, code US 1-14-3. https://cdn.shopify.com/s/files/1/1023/7667/files/Morgan_Thermal_Ceramics_K-23_IFB.pdf
- [H23] R. T. Giles, *Structural Design of Refractory Concrete* (The Atlas Lumnite Cement Co., c. 1940; reprinted from *Industrial Heating*, 1940), trade catalogue, public domain mark. https://archive.org/details/StructuralDesignOfRefractoryConcrete
- [H24] Blasch Precision Ceramics, US Patent 10,155,210 B2, "Steam reformer furnace, reformer flue gas tunnel therefor and refractory components therefor", granted 2018-12-18. https://patents.google.com/patent/US10155210B2/en
- [H25] BME (Budapest University of Technology and Economics), *Solution Manual, Mechanics of Civil Engineering Structures*, "Problem 11.2. Spherical dome" (Eqs. 11-32, 11-33, 11-35). https://solutionmanual.bme.hu/?p=5397
