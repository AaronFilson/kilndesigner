# Structure and draft: follow-up research

Follow-up to `kiln-hardware.md` §3–4 and `combustion-and-masonry.md` §3–4 (2026-10-24).
Marks as in those files: **Verified** (read on the source page), **Excerpt** (search summary
or snippet only, not read in full), **Derived** (my arithmetic), **NOT FOUND**. The target was
three independent sources per fact; the count is given for each, and most fall short.

Several primary sources could not be read: aisc.org PDFs return 403 (as in `kiln-hardware.md`
§4.7.4), EN 1993-1-2 and NFPA 211 are paywalled, and no refractory handbook (AP Green, Kaiser,
Norton, Trinks, Chesters) has an online copy that turned up.

## 1. Heated arch thrust for thick arches (T/S > 10 %)

| Finding | Mark | Sources (count) |
|---|---|---|
| No source found that extends HarbisonWalker's heated-arch table [HW, `kiln-hardware.md` S20] past T/S = 10 %. Trinks, Chesters and the AP Green/Kaiser/Norton handbooks have no online copy. | **NOT FOUND** | 0 |
| Conditions for a stable sprung arch (McDowell, quoted in an open-hearth roof paper): the line of thrust stays in the middle third; the thrust stays within the friction angle at each joint; peak pressure stays below the brick's hot strength. Agrees with HW's middle-third rule. | Excerpt | [A1], HW (2) |
| Skewbacks are pushed outward, and restraining them is what keeps the arch in compression. Patent designs pivot the buckstays so they don't take bending moments. | Excerpt | [A2] (1) |
| Binding steel for buckstay bands designed to "a maximum stress of 15,000 psi to allow for erection stresses and other design uncertainties", with net-section reductions at bolted joints | Excerpt | [A3] (1) |

**Extrapolation.** The HW table rises steeply toward its "stress excessive" cells as T/S rises at
low rise (1 in/ft: 1.88 at 4 %, 5.0 at 7 %, then **). Some columns change direction near the
limit. No source gives a law to fit, so extrapolating past 10 % is **not supported**. Keep the
ADR 0009 refusal (`kiln-hardware.md` §4.6).

- A cautious option, **not sourced**: at T/S > 10 %, report the cold thrust and the 10 % factor,
  labelled as outside the checked range, and don't pass the result as a design value.
- Skewback channel and buttress sizing rules from a refractory handbook: **NOT FOUND**.

## 2. Allowable stress for hot binding steel

| Item | Value | Mark | Sources |
|---|---|---|---|
| HW hot-binding tensile limit | 12,000 psi | Verified | HW (1) |
| Buckstay bands, "good engineering practice" | 15,000 psi max | Excerpt | [A3] |
| EN 1993-1-2 ky,θ (yield) at 500 °C | 0.78 (kE,θ 0.60) | Excerpt (Dlubal worked example) | [A4] |
| EN 1993-1-2 at 560 °C (S355) | ky 0.594, kE 0.426, kp 0.252 | Verified | [A5] |
| ky,θ at 600 °C | 0.47, which fits a straight line from 0.78 at 500 °C to 0.594 at 560 °C | Derived from [A4] [A5]; not read in the standard | |
| ky,θ at 400 °C | 1.00 for carbon steel ("Eurocode and AISC") | Excerpt (search summary) | [A6] (1) |
| AISC 360 Appendix 4, 1,000 °F (538 °C) | ky ≈ 0.66 | Excerpt | [A7] |
| Basis of those yield factors | **2 % strain offset**, fit for fire, where large deformation is acceptable. For sustained load at temperature, 0.2 % offset values "will be more appropriate" | Excerpt (AISC quiz, 2013) | [A8] |

- **Caution.** The Eurocode and AISC factors are fire-limit-state values (2 % strain) for
  short exposure. They aren't allowables for steel that runs warm on every firing, so neither
  confirms nor replaces HW's 12,000 psi. Creep allowables for carbon steel (ASME Section II
  Part D, for example) weren't searched for here.
- The 12,000 psi (HW) and 15,000 psi [A3] figures are 1/3 and 0.42 of A36's 36 ksi yield
  **(derived)**. These are the only two refractory-side figures found.
- Full Table 3.1 / Table A-4.2.1 by temperature: **NOT FOUND** (paywalled or blocked).

## 3. Angle section properties and AISC F10

AISC values for L2×2×3/16 to L4×4×⅜ are already in `kiln-hardware.md` §4.7.1 (AISC Shapes
Database v16.0). The Engineering ToolBox table [A9] Verified gives area and Ix for all
thicknesses. It cites no standard, but where it overlaps it matches AISC to two figures
(L3×3×¼: Ix 1.24 against AISC 1.23):

| Size | t (in) | A (in²) | W (lb/ft) | Ix (in⁴) | rx = √(Ix/A) (in, derived) |
|---|---|---|---|---|---|
| 2×2 | 1/8 | 0.48 | 1.7 | 0.19 | 0.63 |
| 2×2 | 5/16 | 1.15 | 3.9 | 0.42 | 0.60 |
| 2½×2½ | 3/16 | 0.90 | 3.1 | 0.55 | 0.78 |
| 2½×2½ | 5/16 | 1.46 | 5.0 | 0.85 | 0.76 |
| 2½×2½ | 3/8 | 1.73 | 5.9 | 0.98 | 0.75 |
| 2½×2½ | 1/2 | 2.25 | 7.7 | 1.23 | 0.74 |
| 3×3 | 7/16 | 2.43 | 8.3 | 1.99 | 0.90 |
| 3×3 | 1/2 | 2.75 | 9.4 | 2.22 | 0.90 |
| 3½×3½ | 1/4 – 1/2 | 1.7 – 3.3 | 5.8 – 11.1 | 2.01 – 3.64 | |
| 4×4 | 7/16 | 3.3 | 11.3 | 4.97 | 1.23 |
| 4×4 | 1/2 | 3.8 | 12.8 | 5.56 | 1.21 |
| 4×4 | 5/8 | 4.6 | 15.7 | 6.66 | 1.20 |
| 4×4 | 3/4 | 5.4 | 18.5 | 7.67 | 1.19 |

- Sx and x̄ for these sizes: **NOT FOUND** here. Sx = Ix ÷ (b − x̄) needs x̄ from the AISC
  database, which `kiln-hardware.md` [S28] already uses; read the remaining rows from it.

AISC 360 F10 (single angles):
- Geometric-axis (x, y) design is allowed for angles with continuous lateral-torsional
  restraint, and for unrestrained **equal-leg** angles with no axial compression bent about one
  geometric axis only. Otherwise design about the principal axes (w, z). Excerpt [A10] [A11] (2).
- ASD Ωb = 1.67, LRFD φb = 0.90. Verified [A10] (1).
- An unrestrained equal-leg angle bent about a geometric axis has a tip stress about 25 %
  above the value from the geometric S (Commentary, quoted on a forum). Excerpt [A12] (1).
- The F10 equations themselves (yielding at 1.5 My, the Mcr expressions, leg local buckling):
  **NOT FOUND**. The AISC PDFs were blocked; the user or a later session needs the spec.

Deflection limits: IBC Table 1604.3 gives L/360 under live load and L/240 under total load for
floor members. Footnote g takes dead load as zero for steel. Excerpt [A13] [A14] [A15] (3,
all secondary). These are building limits, and no source applies them to kiln frames. **No
kiln-frame deflection limit was found.**

## 4. Chimney draft

| Item | Value | Mark | Sources |
|---|---|---|---|
| Required draft for a natural-draft kiln (in. w.c.) | — | **NOT FOUND** | 0 |
| Draft-regulated appliances (ASHRAE) | 0.10 in. w.c. available draft required | Verified | [A16] |
| Boiler breech / over the fire | about −0.05 / −0.02 to −0.03 in. w.c. | Excerpt | [A17] |
| Wood stove makers | −0.04 to −0.08 in. w.c. | Excerpt | [A18] |
| Design ambient (ASHRAE Ch. 35) | **60 °F (520 °R)**. A high design ambient gives better chimney operation when outdoor temperatures drop | Verified | [A16] |
| Code sizing tables (Canada, IFGC) | 2.5 % January heating design temperature; IFGC masonry chimney table banded by outdoor temperature | Excerpt | [A19] [A20] |
| Theoretical draft (ASHRAE Table 6) | ≈ 0.5 in. w.c. per 100 ft at 300 °F rise; 0.2 per 100 ft at 100 °F rise | Verified | [A16] |
| Cooling up the stack | gases "lose heat continuously from entrance to exit"; the design uses one mean temperature. Connector multiplier example: 16 ft, 7 in single-wall connector 0.61 (300 °F rise becomes 183 °F mean). Little correction for a straight vertical vent | Verified | [A16] |

- Cross-check (derived): `combustion-and-masonry.md` §4.2 gives 7.63 × H × (1/To − 1/Ti). At
  To = 520 °R and Ti = 820 °R (300 °F rise), 100 ft gives 0.54 in. w.c., which agrees with
  ASHRAE's 0.5.
- Summer worst case: ASHRAE's 60 °F is a design point, not a summer extreme, and the codes
  use winter temperatures because their concern is starting the draft in the cold. For a
  kiln, a hot day gives the least draft. No source names a summer design temperature for
  kilns: **NOT FOUND**. The engine should let the user enter their own hottest-day figure.
- Mean stack temperature against kiln temperature, for brick kiln chimneys: **NOT FOUND**
  (Olsen lookup below).

## 5. Venturi burner rating against gas pressure

- The √p law holds from 5 to 20 psi on Ward's MR100/MR750 table (`combustion-and-masonry.md`
  §3.2, derived there). This fits incompressible orifice flow, Q ∝ A·√ΔP.
- Choking: the derived critical ratio of 0.58 for propane (k ≈ 1.13) puts the choke near
  10 psig when the gas discharges to atmosphere (§3.3 there). Above the choke, flow rises
  linearly with **absolute** upstream pressure, not with √p, so the √p fit above 10 psig is
  empirical. Only one source (Ward) was found; no independent check.
- Whether Ward's 11 in. w.c. and 2 psi entries use a different orifice: **NOT FOUND**. Ward
  sells the orifice charts but doesn't publish them. GACO and Marc tables weren't found online.
  This needs the vendor or the user.

## 6. Flue-gas velocity and cylinder supply

| Item | Value | Mark | Sources |
|---|---|---|---|
| Vents and chimneys (ASHRAE) | 300–3,000 fpm = **5–50 ft/s** (derived) | Verified | [A16] |
| General chimneys | 1.5–15 m/s (5–49 ft/s) | Excerpt | [A21] |
| Small furnaces | air and flue gas "should not exceed 2 m/s" (6.6 ft/s) | Excerpt | [A22] |
| Residential heating | about 5 ft/s | Excerpt | [A23] |
| Through a kiln at about 1100 °C (Olsen via Norsker) | 1.2–1.5 m/s (3.9–4.9 ft/s) | Verified | `kiln-hardware.md` S14 |

So 3 independent sources (ASHRAE, the general chimney figure, Engineering ToolBox) put chimney
velocity at about 5 ft/s at the low end. A kiln-specific chimney velocity: **NOT FOUND**.

Cylinder vaporisation: Flame Engineering's 100 lb table (already S3 in
`combustion-and-masonry.md` §2.1) gives 113,000 BTU/hr full at 0 °F, 300,000 at 70 °F, and
64,000 at 50 lb and 0 °F. Excerpt here; already Verified there. Corroboration:
- Nova Scotia bulletin [A24]: 100 lb cylinder limits of about 52,875 BTU/hr (heating) and
  92,531 BTU/hr (water heating, cooking). Excerpt.
- A DOT-cylinder guide quoted on a forum [A25]: about 50,000 BTU/hr continuous at 0 °F, with
  ×0.25 for continuous draw. Excerpt, secondary.
- Emerson LP-10 handbook [A26]: 2,488 BTU/ft³ propane vapour. Its vaporisation tables weren't
  read.

These agree with the conservative table in `combustion-and-masonry.md` §2.2 to within a factor
of about 2, but not closely. Manchester Tank and NPGA figures: **NOT FOUND**.

## Ask the user (Olsen, *The Kiln Book*)

- Olsen p.__ (arches chapter): heated thrust or tie-rod sizing for 4½ and 9 in studio arches
  where T/S > 10 %; any buttress or angle-size rule.
- Olsen p.__ (chimney chapter): any draft figure in in. w.c., and the stack exit temperature
  or mean temperature against kiln temperature.
- Olsen p.__ (burners): orifice drill size against pressure for venturi burners (11 in. w.c.
  and psi), and any statement on how burner output varies with pressure.
- Olsen p.__ (flues): flue-gas or chimney velocity, if given beyond Norsker's 1.2–1.5 m/s quote.
- Olsen p.__ (fuels): propane cylinder or tank withdrawal rates, and the manifolding rule.

## Sources

- [A1] "Development of Bonded Basic Roofs for Open-Hearth Furnaces", OneMine. https://onemine.org/documents/part-i-papers-development-of-bonded-basic-roofs-for-open-hearth-furnaces (search excerpt)
- [A2] US 3962528, "Furnace skewback support with buckstay pivot". https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/3962528 (search excerpt)
- [A3] US 4505210, "Multiple hearth furnace chamber". https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4505210 (search excerpt)
- [A4] Dlubal knowledge base 001644 (EN 1993-1-2 example). https://www.dlubal.com/en/support-and-learning/support/knowledge-base/001644 (search excerpt)
- [A5] IDEA StatiCa, "Fire design". https://www.ideastatica.com/support-center/fire-design
- [A6] Brunel University thesis. https://bura.brunel.ac.uk/bitstream/2438/17713/1/FulltextThesis.pdf (search excerpt)
- [A7] Modern Steel Construction, Feb 2023, "Turning up the Heat". https://lsc-pagepro.mydigitalpublication.com/article/Turning+up+the+Heat/4484630/779506/article.html (search excerpt)
- [A8] AISC Modern Steel quiz, Nov 2013. https://www.aisc.org/globalassets/modern-steel/archives/2013/11/2013v11_quiz.pdf (search excerpt)
- [A9] Engineering ToolBox, "Steel Angles - Equal Legs". https://engineeringtoolbox.com/steel-angles-d_1322.html
- [A10] Tekla Structural Designer, single angles AISC 360. https://support.tekla.com/doc/tekla-structural-designer/2025/ref_designprocedureforsingleanglesanglesandteesaisc360
- [A11] ideCAD, single angles per AISC 360-16. https://help.idecad.com/ideCAD/single-angles-flexural-design-per-aisc-360-16-with (search excerpt)
- [A12] Eng-Tips, "AISC 360-22 single angles". https://www.eng-tips.com/threads/aisc-360-22-single-angles.515226/ (search excerpt)
- [A13] S. K. Ghosh Associates. https://www.skghoshassociates.com/?p=8389 (search excerpt)
- [A14] Missouri S&T course problem 2.15. https://web.mst.edu/jthomas/classes/5260/problem/02/015/index.html (search excerpt)
- [A15] Eng-Tips, deflection design. https://eng-tips.com/threads/deflection-design.149357 (search excerpt)
- [A16] ASHRAE Handbook, Systems and Equipment 2020, Ch. 35 "Chimney, Vent, and Fireplace Systems". https://handbook.ashrae.org/Handbooks/S20/IP/S20_Ch35/S20_ch35_ip.aspx (first 100,000 characters read)
- [A17] InspectApedia, chimney draft measurement. https://inspectapedia.com/heat/Chimney_Draft_Measurement.php (search excerpt)
- [A18] hearth.com thread 11461. https://hearth.com/talk/threads/11461 (search excerpt)
- [A19] Technical Standards and Safety Authority (Ontario), vent and chimney sizing. https://www.safetyauthority.ca/alert/vent-and-chimney-sizing (search excerpt)
- [A20] InspectApedia, IFGC Table 504.2. https://inspectapedia.com/chimneys/Chimney_Flue_Size_Requirements_Table_504.2.php (search excerpt)
- [A21] Engineering Wiki (Fandom), "Chimney". https://engineering.fandom.com/wiki/Chimney (search excerpt)
- [A22] Engineering ToolBox, chimney sizing. https://www.engineeringtoolbox.com/amp/chimney-sizing-d_175.html (search excerpt)
- [A23] Natural Resources Canada, CANMET report IR 75-120. https://download-telecharger.services.geo.ca/pub/nrcan_rncan/publications/STPublications_PublicationsST/301/301766/cmb_erperl_IR_75_120.pdf (search excerpt)
- [A24] Nova Scotia safety bulletin 0000034. https://novascotia.ca/lae/healthandsafety/docs/safety-bulletin-0000034-fr.pdf (search excerpt)
- [A25] TroubleFreePool forum. https://www.troublefreepool.com/goto/post?id=2681118 (search excerpt)
- [A26] Emerson LP-10 handbook. https://d1-auth.emerson.com/documents/automation/lp-10-handbook-pl-pl-9718536.pdf (search excerpt)
