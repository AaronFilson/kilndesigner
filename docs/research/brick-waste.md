# Waste allowances: brick, cut and shaped brick, castable, blanket

Research pass 2026-10-29. The engine had added an unsourced 10 % to every brick count, sheet
area and castable mass (`masonry.py`, `castable.py`), and 5 % to the chimney's brick
(`hardware.py`). This note records what the sources say, case by case, and what the engine now
uses (`kilndesigner.allowance`). A design can set its own (`allowances:` in the design file).

Status words as elsewhere: **Verified** (read on the source page), **Excerpt** (search snippet
only), **NOT FOUND**.

## 1. Whole straights and cut brick in coursed walls

| Source | Statement | Status | Ref |
|---|---|---|---|
| Brick Industry Association, *Technical Notes on Brick Construction 10*, "Dimensioning and Estimating Brick Masonry", Feb 2009, p.11, "Brick Breakage and Waste" | "determine the net quantities of all brick, including all correction factors above, before adding any allowances for waste. Allowances for waste and breakage vary, but as a general rule, at least 5 percent is added to the net brick quantities delivered to the jobsite. Particular job conditions or experience may warrant using a higher percentage for waste." | Verified (PDF text) | [W1] |
| BIA TN 10, p.11, "Mortar Waste" | "as a general rule, add 15 to 25 percent to the net mortar quantities." (The engine counts dry-laid joints and buys no mortar, so this is not used.) | Verified | [W1] |
| BIA TN 10, p.1 summary | "Include partial brick in estimates to maintain bond at corners" and "Modify brick estimates for bond pattern, breakage and waste". | Verified | [W1] |
| Brick-calculator and vendor web pages (codingace, toolcroze, brickcal, firepitsurplus) | 3–5 % for careful handling, 5–10 % typical, 10–15 % for curved fireplace work. | Excerpt; not makers or handbooks, not used | [W5] |

**Reading.** BIA's "at least 5 percent" is over a *net* count that already includes every partial
brick. The engine's count is net in that sense: `bricks_for_cuts` takes a whole brick for each cut
piece that can't come from an earlier offcut, after a ⅛ in saw kerf. So the cutting loss of the
cut pieces is already in the count, and the allowance covers breakage, chipped bricks and
mistakes. BIA writes for building brick laid in mortar; no refractory maker's figure was found
(§5), so the same 5 % is used for insulating and dense firebrick.

**Insulating vs dense brick.** No source found gives a different breakage allowance for IFB.
IFB is softer and chips more in handling; dense brick is harder to cut. Neither difference has a
sourced number. **NOT FOUND**: one value is used for both, and the design can raise it.

## 2. Cut brick for arches, round walls, skewbacks

| Item | Finding | Status |
|---|---|---|
| A refractory maker's or handbook's waste figure for arch, wedge or key brick | **NOT FOUND**. HWI's arch-brick tables (kiln-hardware.md [S20]) count the shapes per ring exactly and add nothing. | — |
| A figure for brick cut to a curve (round walls, dome courses, skewbacks counted by volume) | **NOT FOUND**. Vendor calculators say "arches, domes and burner openings need more", without a number. | Excerpt [W5] |
| Olsen, *The Kiln Book* 4th ed. (kiln-reference.md notes) | No waste or spare-brick allowance recorded in the notes taken so far. **To ask the user** whether a page gives one. | — |
| Rhodes, *Kilns*; Minogue & Sanderson, *Wood-fired Ceramics* | Not available to read in this pass: **NOT FOUND**. | — |

**Reading.** Shaped arch brick (`shaped`) are counted exactly ring by ring, as HWI's tables are, so
BIA's breakage allowance is the closest sourced figure: 5 %. Arch caps, skewbacks and the fill
beside an arch are counted *by volume* (`masonry.py`, "about N bricks by volume, cut to the
arch's curve"): that count has no cutting loss in it, and no source gives one. The engine applies
the brick allowance only. A builder who cuts many bricks to a
curve should set `allowances.brick` higher from experience.

## 3. Castable overage

| Source | Statement | Status | Ref |
|---|---|---|---|
| PCO Refractories (Poland), *Product Application Instructions: Castable Refractories*, version 1/2026, 23.02.2026, §5.3 "Material requirement" | "The amount of dry castable required to produce 1 m³ of refractory lining is specified in the Product Technical Data Sheet. When planning material consumption, it is recommended to include an additional allowance of approximately 5% to compensate for losses caused by, among others, accidental bag damage, spillage during handling and residual material left in bags or the mixer. In the case of difficult working conditions or applications carried out at a significant distance from the mixing area, this allowance should be increased to 10% or more." | Verified (PDF text) | [W2] |
| HWI, *Installation Guidelines IC-1, Insulating Castables—Standard*, 8/23/16 | Refers to the data sheet's "Material Required"; gives no overage figure. "Mixer and batch sizes should be as large as possible to minimize the number of batches." | Verified | [W3] |
| Able Refractory, castable installation page | "Estimate the quantity of material required for the job using our published figures"; no overage. | Verified | [W4] |
| HWI *Handbook of Refractory Practice* | Not readable online (academia.edu 403). **NOT FOUND**. | — | — |

**Reading.** The maker's "material required" (HWI: 92 lb/ft³ for Kast-O-Lite 30 LI Plus) is
already the mass that places a cubic foot; PCO's ≈5 % is over that, for spills and what is left in
bags and the mixer. The engine uses 5 % for bought castables (over "material required") and for
the batches of a mix the builder makes (over the lining's volume). PCO's "10 % or more" for hard
conditions is noted in the finding; the design can set it.

## 4. Blanket and board

No maker or handbook trimming allowance for ceramic-fibre blanket or calcium silicate board was
found (Morgan, Unifrax and HWI pages searched; a patent's 118–120 % is a compression allowance for
module linings, not waste). **NOT FOUND**: the engine adds nothing to the sheet area by default and
says so; the design can set `allowances.sheet`.

## 5. Gaps

- A refractory maker's or installer's brick waste figure (HWI, Allied, Morgan/Thermal Ceramics,
  Plibrico, ASTM). Searched; none found online.
- A cutting allowance for brick cut to a curve; arch-brick spares.
- Olsen, Rhodes, Minogue & Sanderson on spare brick: ask the user for pages.
- Blanket and board trimming allowance.

## 6. What the engine uses

| Case (`allowances.` key) | Default | Over what | Source |
|---|---|---|---|
| `brick`: whole and cut straights, IFB and dense; chimney brick | 5 % | the net count, cut pieces included | §1 [W1] |
| `shaped`: arch and wedge brick | 5 % | the exact count per ring | §1–2 [W1] |
| `castable`: bought castable and own-mix batches | 5 % | material required (bought) or the lining's volume (own mix) | §3 [W2] |
| `sheet`: blanket and board | 0 % | the area | §4, none found |

The steel (10 % on length) and element wire (10 % on mass) margins in `bom.py` are outside this
note and still unsourced.

## Sources

- [W1] Brick Industry Association, *Technical Notes on Brick Construction 10: Dimensioning and
  Estimating Brick Masonry*, February 2009, p.1 and p.11. PDF read.
  https://gobrick.com/media/file/10-dimensioning-and-estimating-brick-masonry.pdf
- [W2] PCO Refractories, *Product Application Instructions: Castable Refractories*, version
  1/2026, 23.02.2026, §5.3, p.3. PDF read.
  https://pco-refractories.com/wp-content/uploads/2026/03/Product_Application_Instructions_Castable_Refractories_EN-1.pdf
- [W3] HarbisonWalker International, *Installation Guidelines: Insulating Castables—Standard
  (IC-1)*, 8/23/16, Refractory West copy. PDF read.
  https://www.refwest.com/attachments/Installation%20IC1%20Insulating%20Castables--Standard.pdf
- [W4] Able Refractory, "Castable Installation". http://www.ablerefractory.com/castinfo.html
- [W5] Brick and firebrick calculator pages (search excerpts only; not used for numbers):
  https://codingace.net/construction/brick_cutting_allowance.php ;
  https://toolcroze.com/fire-brick-calculator/ ;
  https://brickcal.com/construction/brick-calculator/fire-brick/ ;
  https://www.firepitsurplus.com/blogs/calculator/firebrick-calculator
