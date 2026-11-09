# Refractory movement and mortar (sixth round)

Status: 2026-11-08. Builds on `mortar-and-brick-strength.md` (fifth round), `thermal-properties.md`
§2, `arch-springs.md` and `kiln-hardware.md` §4. Labels as before: **Verified** (read in the
source), **Excerpt** (search snippet, source not opened), **Derived** (worked here from sourced
inputs), **Not found**. Closed items from earlier rounds are not repeated.

## 1. Size changes

### 1.1 Reversible expansion and the expansion allowance

| # | Fact | Status | Source |
|---|---|---|---|
| 1.1.1 | "A typical fireclay refractory brick will exhibit reversible thermal expansion of 3/32" (2.38mm) per foot (305 mm) of length on heating from room temperature to 2400oF (1315oC). This is equivalent to a thermal expansion coefficient of 6.0exp(-6)/oC" | Verified | [M1] |
| 1.1.2 | "Most brick manufacturers recommend an "expansion allowance" (expansion joint allowance) equivalent to 3/32" for fireclay brick linings for each foot of lining length (horizontal traverse). This prevents undue loading and damage to the fireclay bricks in the wall due to superimposed stress if the lining is constrained from movement when heated." | Verified | [M1] |
| 1.1.3 | "Care should be taken to check the expansion allowance - in practice just one half of the theoretical expansion is sufficient. The remaining one half will be absorbed by the mortal [sic] joints, or even dry joints between the bricks." | Verified | [M2] p.29 |
| 1.1.4 | IFB (Brosnan's Table 8, K-20 … JM-30): a thermal expansion coefficient of 5.4×10⁻⁶/°C is printed for two of the grades; the extracted table is scrambled, so which grades is not certain | Verified (value), grade uncertain | [M1] Table 8 |
| 1.1.5 | "For long-term exposures near the rated service temperature, shrinkage may occur sufficiently to allow joint opening. For this reason, it can be important to use IFB's with a higher duty rating than seems required by the process temperature alone." (PLC is a 24 h test) | Verified | [M1] |
| 1.1.6 | Calcined bauxite brick used above its firing temperature: "the permanent linear expansion on exposing these products to temperatures reaching 1600oC is in the range 2-4%" | Verified | [M1] |
| 1.1.7 | Sillimanite-family minerals expand permanently on turning to mullite: sillimanite 5.6 %, andalusite 4.9 %, kyanite 18.8 % by volume (1530–1625, 1350–1500, 1325–1410 °C). Fired below and used above this, "the expansion will be realized in service" | Verified | [M1] Table 3 |
| 1.1.8 | Fireclay brick PLC, 5 h at 1400 °C, super duty: −0.2 to +0.2 % (Table 4; the extracted table is garbled, read with care) | Verified, layout uncertain | [M1] Table 4 |

This is the **third independent source** for the engine's 3/32 in per foot (Olsen p.51, the IFB
sheets in `thermal-properties.md` §2, and now Brosnan [M1]), and the first that says it is the
makers' recommended allowance rather than a builder's figure. Two sources now agree that a wall or
arch grows about 3/32 in/ft (0.78 %) to cone 10; Bhatia [M2] says an allowance of half that is
enough because the joints take the rest. Olsen's 1/16 in/ft in a steel frame (p.52) is that half
(Derived: 1/16 ÷ 3/32 = 0.67, close to ½).

**Where joints go** (already in the repo, not re-found): not above a structural arch nor near its
springing (`door-headers.md`, [H] BIA); Olsen ¼ in fibre at brick ends, offset, joints when a wall
passes 48 in (`olsen-kilns.md` W29, p.52); Norsker ½ cm per m laid dry (`kiln-hardware.md` §4.2).

**Not found:** a published expansion curve to 1300 °C for high-alumina, silica or IFB beyond the
single coefficients above; any Kast-O-Lite / Mizzou reversible expansion (still only PLC,
`flat-roofs.md`); castable drying shrinkage; a silica brick's allowance from a maker (only a kiln
brick vendor's 10–12 mm/m, Excerpt, not recorded as data).

### 1.2 How an arch moves as it heats

| # | Fact | Status | Source |
|---|---|---|---|
| 1.2.1 | With tie rods rather than a fixed binding, the skewback "can shift horizontally" but not rotate; "tie-rods are rarely adjusted", so heating the roof puts "enormous stress" on the skewback courses (patent background) | Excerpt | [M6] |
| 1.2.2 | Glass-furnace sprung roofs: elastic give in buckstays and rods plus bedding-in lets the crown settle; bricks can loosen and drop during heat-up (patent background) | Excerpt | [M7] |
| 1.2.3 | "fire-clay brick are not well adapted for use in wide sprung arches in furnaces operating continuously at high temperatures" (they creep under load); silica brick are used in wide sprung arches | Verified | [M2] |
| 1.2.4 | A measured rise of a kiln or furnace arch on heating, or a published method for it | **Not found** | — |

Derived (for the engine, not yet coded): a circular arch whose span is held while its ring grows
by ε rises. With the arc length L = rθ held to (1+ε)L and the span S fixed, the new rise solves
sin(θ'/2)/θ' = S/(2(1+ε)L). This is geometry only; no source checks it against a kiln.

Searched again 2026-11-09 (search extracts only, not opened, **Not found** as a usable method):
US 4,137,037 (repairing furnace roofs during heat-up: a crown that settles cold is lifted back by
the bricks' expansion); US 2,641,207 (an arch's width growth "calculated in advance"); a
Refractories and Industrial Ceramics paper on glass-furnace roofs, doi 10.1007/s11148-014-9714-z,
whose extract shows a rise formula f = S²/(…) for a 9 m wedge-brick span, garbled; a study of
blast-furnace stoves finding measured expansion below calculated (doi 10.1007/BF01282040). The
Springer paper is the lead to open. Until then the rise formula is not shipped.

## 2. Mortar

| # | Fact | Status | Source |
|---|---|---|---|
| 2.1 | Bond types (HWI): **air-setting** "takes a rigid set when dried over 230°F" and holds the bond "up to the temperature at which the ceramic bond takes effect"; **heat-setting** "develops a ceramic set with a strong bond only at high furnace temperatures. These mortars offer expansion flexibility during initial heating"; **phosphate** reacts "at lower temperatures (500°-600°F)", giving "high strength to the mortar joint" | Verified | [M3] |
| 2.2 | "All mortars can be thinned to a dipping consistency by adding water and mixing. Mortars cannot be thickened." | Verified | [M3] |
| 2.3 | HWI products and bond types, e.g. SAIRSET 34.6 % Al₂O₃ wet air-set; MEXI-KOMO 50.1 dry heat-set; SATANITE 59.4 dry heat-set; GREENSET-85 P 81.6 wet phosphate; PHOXBOND 75.6 wet phosphate | Verified | [M3] |
| 2.4 | SAIRSET (8/10: 5006): max service 3000 °F (1650 °C); MOR at joints 650 psi (4.5 MPa) after 220 °F, **500 psi (3.4 MPa) after 1500 °F (815 °C)**; 350–400 lb per 1,000 9-in equivalents at dipping consistency; max grain 20 mesh (0.83 mm), 0.5 % retained. "As supplied, this is a thick trowel mortar" | Verified | [M4] |
| 2.5 | "Mortar is always the weakest link in refractory brick installation. Mortar joints should be full and as thin as possible with no voids." "Troweled mortar joints always offer improved performance over dipped mortar joints." "For most brick and mortar installations, dryout and heatup are governed by the brick requirements, typically 100°F per hour." | Verified | [M5] HWI M-2, 12/17/13 |
| 2.6 | **Largest joint:** "Mortar joints for refractory mortars should not exceed 1⁄4 in. The fire bricks are often dipped to get a thin mortar coating, with no conventional mortar bed laid." | Verified | [M8] Beall, p.143 |
| 2.7 | Joint 1/16–1/8 in recommended (HeatStop; Isokern, which adds smaller joints "may not leave room for heat expansion"); HeatStop accepts up to ½ in; a boiler spec: average joint ≤ 1/16 in (1.6 mm); Morgan's JM mortar coverage based on a trowelled joint about 2 mm | Excerpt | search snippets [M9] |
| 2.8 | Joint MOR after firing to 1500 °F, 500 psi, is the first hot-side joint strength from a maker on a current sheet (round 5 had 530 psi, dried only). It is after firing and tested cold, **not hot cohesion** | Verified | [M4] |

Findings for the engine:

- The fifth round's rule (no tension across joints) stands. HWI itself calls mortar "the weakest
  link" [M5]; SAIRSET's 500 psi after 815 °C is measured cold.
- **Joint thickness:** ¼ in is the one published maximum read on the page [M8]; 1/16–1/8 in is
  the common recommendation (Excerpt only). A design giving joints thicker than ¼ in can be told
  so, citing [M8].
- **Joints and movement:** Bhatia [M2] says joints take about half the theoretical expansion;
  heat-setting mortar gives "expansion flexibility during initial heating" [M3]. No source
  quantifies how joint thickness changes an arch's settling or thrust: **Not found**.
- **Hot cohesion:** still **Not found** as a number.

## 3. Still-open statics from round 5

| Item | Result |
|---|---|
| Allowable bearing stress / FoS for refractory | **Not found.** The nearest published limits are the load tests: fireclay subsidence 0.5–3.0 % under 172 kPa (25 psi) at 1350–1450 °C [M1] Table 4; IFB 0.2 % at 1200 °C under 0.069 MPa (10 psi) for K26 and JM26 (Lynn sheet, Excerpt [M10]) |
| IFB hot MOR (C583) and creep (C832) | **Not found.** Morgan's sheets give cold MOR (JM26 about 1.5 MPa, K26 0.9 MPa, Excerpt [M10]) |
| Rampant-arch thrust, catenary at a step, hot corbels, door in a vault | **Not found** this round |
| Trinks Vol. I, Gilchrist, Norton, Routschka, HWI *Modern Refractory Practice* / 2005 Handbook | No open full text reached (HWI 2005 Handbook at masonryheaterassociation.org returns 404; Scribd copies not readable). *Modern Refractory Practice* 3rd ed. 1950 is catalogued "Also issued online" at Texas A&M, link not followed |

## 4. Proposed engine work (not done)

1. **Wall expansion allowance:** per wall in a steel frame, growth = length × 3/32 in/ft [M1],
   allowance ≥ half [M2] (Olsen's 1/16 in/ft); an info finding naming Olsen's ¼ in fibre joints
   when a wall passes 48 in, and BIA's "not above the arch's springing".
2. **Arch rise on heating** with the frame held (§1.2, Derived): a working step only, marked
   unchecked against a kiln.
3. **Joint thickness:** if the design ever carries a joint thickness, warn past ¼ in [M8].

Done 2026-11-09 (`movement.py`): items 1 and 3 (the joint warned only where the design states
`chamber.rings: mortar`; the default ring's text cites Beall), and IFB hot faces shown against their
rating in the working. Item 2 stays proposed. No brick in the materials library is identified as
bauxite, kyanite or andalusite, so no permanent-growth note is shown for brick (kyanite in a
castable is already in `castable.py`).

Done in the engine this round: the sprung-arch growth's reference (`frame.py`, `GROWTH_SOURCE`)
now cites Brosnan [M1] beside Olsen. No number moved.

## Sources

- [M1] D. A. Brosnan, "Alumina-Silica Brick", chapter in C. A. Schacht (ed.), *Refractories
  Handbook*, Marcel Dekker (preprint), https://www.jurispro.com/files/documents/doc-1066205184-article-1604.pdf (read in full via pdftotext).
- [M2] A. Bhatia, *Overview of Refractory Materials*, PDHonline Course M158, 2011, p.29 and
  "Fireclay" section, https://www.pdhonline.com/courses/m158/m158content.pdf
- [M3] HarbisonWalker International, *Mortar for Any Installation* brochure,
  https://thinkhwi.com/wp-content/uploads/2021/04/Mortar-Brochure.pdf
- [M4] HWI/ANH, SAIRSET Product Data 8/10: 5006,
  https://cdn.shopify.com/s/files/1/1896/6099/files/Sairset_TechData_Sheet.pdf
- [M5] HWI, Installation Guidelines, Dry Mortars (M-2), 12/17/13,
  https://cdn.shopify.com/s/files/1/0453/9799/9783/files/Installation_M2_Dry_Mortars.pdf
- [M6] US 3,962,528, *Furnace skewback support with buckstay pivot*, background,
  https://patents.justia.com/patent/3962528 (search extract).
- [M7] Glass-furnace roof patent background (search extract of the same search); patent number
  not confirmed.
- [M8] C. Beall, *Masonry Design and Detailing for Architects and Contractors*, 5th ed.,
  McGraw-Hill 2004, §6.4.1 p.143, https://uop.edu.jo/PDF%20File/uop%20[Architecture_Ebook]_Masonry_Design_and_Detailing_For_Architects_and_Contractors-20615_Part72.pdf
- [M9] Search extracts: HeatStop dry mortar sheet; Isokern Magnum manual p.51
  (https://manualshive.com/en/manual/isokern/magnum-82028/2093411?page=51); Morgan JM2600/Blakite
  sheet (link now 404).
- [M10] Search extracts: Morgan JM and K IFB sheets; Lynn K26 spec,
  https://orders.sidharvey.com/documents/Lynn-K26_Spec.pdf
