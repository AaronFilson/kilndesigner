# Heated sprung-arch thrust: first-principles theory

Follow-up to `kiln-hardware.md` §4.3 and §4.6, `structure-and-draft.md` §1 and
`thermal-properties.md` §2.3 (2026-10-24). Goal: a formula, not a table, for the "maximum
thrust of a heated arch free to rise" in HarbisonWalker's table [S20 in `kiln-hardware.md`;
`steel.yaml` `heated_factor`], so the engine can go past T/S = 10 %.

Marks: **Verified** (read on the source page or in the PDF text), **Excerpt** (search summary
only), **Derived** (my arithmetic, scripts described below), **NOT FOUND**. Source keys [A1]...
are local to this file (they are not the [A1]... of `structure-and-draft.md`).

## 1. Result in one paragraph

HarbisonWalker's heated-arch factor is reproduced, to within 4 % in all 70 printed cells, by
plain statics of the **maximum-thrust state of a masonry arch** (Heyman's limit analysis): the
line of thrust passes through the **intrados at the crown** and the **extrados at each
skewback**, so the arch acts as a three-hinged arch whose lever arm is the rise *minus most of
the thickness*. The cold constants use the same statics with the thrust line at mid-thickness
at crown and skewback (as HW states). The factor is the ratio of the two lever-arm results.
No elastic modulus or expansion coefficient enters: it is a geometric bound, the highest thrust
that equilibrium allows inside the brick. This is **Derived**: no source was found that says
HW built its table this way, but the fit is too close to be chance (§3).

## 2. Sources for the theory

| # | Statement | Mark | Source |
|---|---|---|---|
| 1 | "The line of thrust in its extreme positions of minimum or maximum thrust provides the possible hinge locations. Anywhere the line touches the boundaries of the structure, a hinge may be created". "An arch on spreading supports will act in a state of minimum thrust and the same arch on closing supports will act in a state of maximum thrust [1]" ([1] = Heyman, *The Stone Skeleton*, CUP 1995). "Masonry structures often deform as a stable three-hinge mechanism." | Verified (PDF text) | [A1] |
| 2 | "The maximum thrust case is thrust line, or zone of thrust, which takes the intrados once near the crown and the extrados near each springing. This pattern is the response the arch makes to abutments which squeeze together." | Verified (PDF text) | [A2] |
| 3 | "The maximum energy thrust, and the highest possible horizontal thrust, occurs when hinges form in the pattern extrados/intrados/extrados." Minimum thrust is "intrados/extrados/intrados"; both limiting cases are three-pinned arches and any thrust between is also valid. | Verified | [A3] |
| 4 | Three-hinged arch is statically determinate: H = M_c / h (simple-beam crown moment over rise); uniform load H = wL²/(8h). | Excerpt; standard statics | [A4], [A5] |
| 5 | Range of thrust lines found by shifting the line until it touches the upper and lower boundary; those are the min and max thrust states (Heyman 1966, *Int J Solids Struct* 2:249–79). | Excerpt | [A6] |
| 6 | Conflict: one paper puts the maximum (active) state's crown contact at the extrados. Sources 1–3 and the HW fit (§3) say intrados. | Excerpt | [A7] |

Count: 3 read sources ([A1] [A2] [A3]) for the hinge pattern of maximum thrust; [A1] traces it
to Heyman. Heyman's books themselves were not read (no online copy).

**Why heating gives maximum thrust (Derived, reasoning from [A1]–[A3]).** A heated arch
expands. If the steel holds the skewbacks, the span the hot arch "wants" is longer than the
span it has, which is the same as the abutments squeezing together, the case [A1] [A2] tie to
maximum thrust. "Free to rise" means the crown can lift, so the arch is not held as an elastic
fixed arch; the thrust stops growing once the thrust line has reached the faces (hinges open,
crown lifts). That ceiling is geometric, which is why HW can tabulate it with no material
data. Hotter intrados than extrados (gradient) is not needed for the result.

## 3. The formula and the check against HW

Symbols (HW convention, `kiln-hardware.md` §4.3): S inside span, h inside rise (h = d·S/12,
d in in/ft), T thickness, R intrados radius = (S²/4 + h²)/(2h), φ half the central angle,
sin φ = S/(2R). D brick density. Per foot of arch length; origin at the arch centre.

Half-arch moment about a contact point P at radius r_P on the skewback joint
(x_P = r_P sin φ, y_P = r_P cos φ):

    M_P = D · [ x_P · φ · T · (R + T/2)  −  ((R+T)³ − R³)(1 − cos φ) / 3 ]

Horizontal thrust, with the crown contact at height y_c:

    H = M_P / (y_c − y_P)

- Cold (HW: mid-thickness at crown and skewback): r_P = R + T/2, y_c = R + T/2.
- Heated maximum (intrados at crown, extrados at skewback): r_P = R + T, y_c = R.
  Lever = R − (R+T) cos φ.
- Factor = H_hot / H_cold. "Stress excessive" (HW "**") matches the lever going to zero:
  T/R → 1/cos φ − 1 (d = 1: T/S ≈ 8.8 %, and HW stars from 8 %) **(Derived)**.

The weight term is the exact annular sector; centroid of a sector strip (2/3)(r³ diff)/(r² diff)
**(Derived)**, geometry as `kiln-hardware.md` formulas 1–13.

Check, all **Derived** (Python, numerical integration and the closed form agree):

| d (in/ft) | T/S | HW factor | Formula | Error |
|---|---|---|---|---|
| 1.608 | 4 % | 1.43 | 1.43 | 0 % |
| 1.608 | 7 % | 1.98 | 2.02 | +2 % |
| 1.608 | 10 % | 3.30 | 3.26 | −1 % |
| 1 | 7 % | 5.0 | 5.20 | +4 % |
| 1.5 | 10 % | 3.88 | 3.89 | 0 % |
| 3 | 10 % | 1.63 | 1.65 | +1 % |

All 70 non-starred cells: max |error| 4.0 %, mean +0.3 %. Letting the contact sit a fraction k
of the half-thickness from mid-depth and fitting k cell by cell gives k = 0.98–1.00, i.e. the
faces. Thrust lines at the middle-third limits (k = 1/3) give 1.11 at 1.608/4 %, far below HW's
1.43, so HW's table is not a middle-third table.

Beyond the table (Derived, same formula, **not checked against any source**):

| d | T/S | Factor |
|---|---|---|
| 2.302 | 12.5 % (Pitelka 4½ in on 36 in) | 2.44 |
| 2.302 | 15 % | 3.13 |
| 2.302 | 20 % | 6.29 |
| 1.608 | 12.5 % | 6.2 |
| 3 | 15 % | 2.16 |

## 4. Why the factor climbs with T/S, and 2¾ vs 3 in

The cold lever is about the full rise; the hot lever is the rise less roughly T·(1 + cos φ)/2
**(Derived)**. Thicker brick on the same rise shortens the hot lever, so the multiplier grows
and blows up as T approaches the rise ("stress excessive"). The factor is a ratio, so the
effect of T is only through T/h.

At 36 in span, d = 2.302 (h ≈ 6.9 in): 2¾ in (T/S 7.6 %) → 1.65, 3 in (8.3 %) → 1.73. Hot
thrust ∝ T × factor, so 3 in pushes about 14 % harder than 2¾ in **(Derived)**: a real but
small change, within the steel's usual margin. That supports the user's view that the
quarter inch is not a practical difference for a flat-ish studio arch, while showing why the
table still moves. At low rise (d = 1) the same quarter inch matters much more.

## 5. Elastic (restrained) theory

The task listed Timoshenko & Young, Roark, Trinks, Norton, Chesters and HW *Modern Refractory
Practice* for an elastic temperature-thrust formula (H_t from E, α, ΔT, I, ∫y² ds).
- No readable copy of any of them was found. The CSUN two-pinned-arch lab [A5] cites
  Timoshenko & Young (1965) but gives only load cases, no temperature case. **NOT FOUND.**
- For a masonry arch the elastic case is bounded anyway: elastic thermal thrust can only
  rise until the thrust line reaches the faces, after which hinges open (§2). So the §3 bound
  is the maximum for an arch free to rise. An arch held so it *cannot* rise (crown restrained)
  is a different case and remains **NOT FOUND**.

## 6. Material data a formula would need

The §3 bound needs only geometry and density. An elastic formula would need hot E and α.

| Property | Material | Result | Mark |
|---|---|---|---|
| Reversible expansion | IFB (JM, TJM, class 26) | 0.5–0.7 % to ~1000 °C | Verified/Excerpt, `thermal-properties.md` §2.1 |
| Reversible expansion | Kast-O-Lite 30 | not on any sheet found | **NOT FOUND** |
| Elastic modulus (cold or hot) | IFB | Morgan JM sheet lists MOR and CCS (~1 MPa) but no E | **NOT FOUND** [A8] |
| Elastic modulus | Kast-O-Lite 30 | distributor lists density, 3000 °F, k only | **NOT FOUND** [A9] |
| E vs temperature, dense firebrick | fireclay, silica, alumina to 800 °C | NBS 1934 paper exists; values not read | Excerpt [A10] |

## 7. Limits (for ADR 0009)

- Validated only where HW is: T/S 4–10 %, d 1–3 in/ft, brick-weight load only. Past 10 % it is
  the same mechanics but unverified by any table.
- Assumes no tension, no sliding, crushing strength not reached at the hinge (Heyman's
  hypotheses, [A1] [A6]). Near the "**" limit the contact force concentrates at an edge; hot
  crushing strength of IFB (~1 MPa cold CCS) is then the governing check, not covered here.
- Insulation load on top (castable layer) changes M_P; the formula can include it as added
  weight, but nothing checks that.

## 8. Past the method: the steel at 5.34 × the cold thrust (2026-10-29)

Olsen's built kilns (*The Kiln Book*, 4th ed.) lie past §7's range, many of them where the method
has no answer at all:

- the fast-fire kiln: a No. 1 arch, 4½ in of IFB over 27 in at 1½ in per foot of span (p.139–140);
- his kits: No. 1 arches of 4½ in IFB on featheredge skewbacks (p.171, p.176);
- his chamber kilns: 4–6 in/ft (p.296).

At 27 in and 1½ in/ft the rise is 3.375 in. The ring's 4½ in is past the thickest the method
takes, (h − S/48) ÷ cos ½θ = 3.19 in. The hot lever, R − (R + T)·cos φ, is negative, so the
maximum-thrust state can't form. HarbisonWalker's table marks such arches "stress excessive".
Yet the kilns stand, in light bolted frames that give (2 × 2 × 3/16 in angle on the fast-fire
kiln, p.139; Fig. 5-36).

Reading (**derived**): a maximum-thrust state needs the abutments to hold their span while the
arch grows. With T past the hot lever, no hinge pattern can lift the crown, so a rigid frame
would see an unbounded thrust. A real studio frame is not rigid: the angle bends, the rods
stretch and the soft brick crushes at the contact, and these limit the thrust. No source gives
the stiffnesses needed to work that out.

**The engine's rule.** Where the method gives no finite factor, or one past 5.34, the hot thrust
is taken as 5.34 × the cold thrust. That is the largest factor HarbisonWalker prints before
"stress excessive". The finding is a note, not a warning. Checks, **derived**:

- **Fast-fire kiln.** The cold thrust is about 30 lb per foot, so 5.34 × gives 160 lb per foot.
  Over the 36 in between the corner posts that needs Sx ≥ 0.18 in³ at 12,000 psi: an
  L2×2×3/16 (0.188 in³), the angle Olsen used (test: `test_frame.py`, Olsen's fast-fire arch).
- **Updraft 5 × 5 × 6 ft outside** (p.174): HarbisonWalker's method applies (lever ≥ S/48), and
  the frame sized from it is at least Olsen's 3 × 3 × ¼ in corner angle.

**Status:** an engineering rule, sourced at both ends (HarbisonWalker's largest printed factor;
Olsen's built frame), not a theory of hot arches in flexible frames. It is recorded in ADR 0014.

## Ask the user (Olsen, *The Kiln Book*)

- Olsen p.__ (arches): does he give a heated-thrust multiplier or describe hinging at the faces
  when the kiln heats; any tie-rod or angle size against span and thickness.
- Olsen p.__ : any expansion figure for IFB or castable arches, or advice on backing off rods.
- Olsen p.__ : his rule for arch thickness against span/rise (to compare with the "**" limit
  T/R = 1/cos φ − 1).

## Sources

- [A1] Block P., Ciblac T., Ochsendorf J., "Real-time limit analysis of vaulted masonry buildings", *Computers and Structures* 84 (2006) 1841–1852. https://www.block.arch.ethz.ch/brg/files/Block-Ciblac-Ochsendorf_CAS_2006.pdf
- [A2] CSJM University lecture notes, "4. Arches". https://gyansanchay.csjmu.ac.in/wp-content/uploads/2022/05/ARCHES.pdf
- [A3] Obvis Archie-M knowledge base, "Multi span viaducts". https://help.obvis.com/article/41-multi-span-viaducts
- [A4] CalcSteel, "The three-hinged arch". https://calcsteel.com/blog/the-three-hinged-arch-why-the-hinge-makes-it-solvable-by-statics-alone (search excerpt)
- [A5] CSUN, "EXP9 Two-Pinned Arch". https://www.csun.edu/sites/default/files/EXP9%20Two-Pinned%20Arch.pdf
- [A6] Boothby T., Coronelli D., "The Stone Skeleton: A Reappraisal", *Heritage* 7 (2024). https://re.public.polimi.it/retrieve/fea942ef-bec3-4919-ab3e-39056d3d797d/heritage-07-00107-v2.pdf (search excerpt; PDF text not extracted)
- [A7] NAUN, *Int J Math Models* 2015. https://www.naun.org/main/NAUN/ijmmas/2015/a802001-369.pdf (search excerpt)
- [A8] Morgan JM IFB series. https://www.murugappamorgan.com/media/9428/jm-ifb-series_eng.pdf (search excerpt)
- [A9] Distribution International, Kast-O-Lite 30 LI Plus. https://shop.distributioninternational.com/refractories/refractories-castable/recakl30lip55h (search excerpt)
- [A10] NBS J. Research 13 (1934). https://nvlpubs.nist.gov/nistpubs/jres/13/jresv13n6p851_A2b.pdf (search excerpt)
