# Concrete for a kiln's platform: strength, bearing and heat

Research round 2026-10-31, after the user's answer that "any concrete foundation that holds up to
frost and the elements will do for a kiln; 1800 psi is low grade and would hold most any kiln in
Olsen's book". What freely readable standards ask of concrete exposed to frost and weather, what
they allow it to bear, and where the engine uses them (`foundation.py`, `chamber.foundation`).
Concrete at temperature (EN 1992-1-2) and ACI 349's long-term limits are in `blocked-items.md`
§20 [K31] [K32].

## C1. Minimum strength: the International Residential Code, Table R402.2 (Verified)

Read in the 2025 California Residential Code (Title 24 Part 2.5), which prints the IRC's §R402.2
and Table R402.2 unchanged [C1]. §R402.2: "Concrete shall have a minimum specified compressive
strength of f′c, as shown in Table R402.2. Concrete subject to moderate or severe weathering as
indicated in Table R301.2 shall be air entrained as specified in Table R402.2."

TABLE R402.2 — MINIMUM SPECIFIED COMPRESSIVE STRENGTH OF CONCRETE (psi at 28 days, footnote a),
by weathering potential (footnote b: "See Table R301.2 for weathering potential"):

| Type or location of concrete construction | Negligible | Moderate | Severe |
|---|---|---|---|
| Basement walls, foundations and other concrete not exposed to the weather | 2,500 | 2,500 | 2,500 c |
| Basement slabs and interior slabs on grade, except garage floor slabs | 2,500 | 2,500 | 2,500 c |
| Basement walls, foundation walls, exterior walls and other vertical concrete work exposed to the weather | 2,500 | 3,000 d | 3,000 d |
| Porches, carport slabs and steps exposed to the weather, and garage floor slabs | 2,500 | 3,000 d,e,f | 3,500 d,e,f |

Footnote d: "Concrete shall be air-entrained. Total air content (percent by volume of concrete)
shall be not less than 5 percent or more than 7 percent." Footnote c: concrete "subject to
freezing and thawing during construction shall be air-entrained concrete in accordance with
Note d."

**Engine:** a kiln's platform is a slab exposed to the weather, the last row. The design's
`chamber.foundation.compressive_strength` defaults to **3,500 psi**, that row's severe column, the
most the table asks of any slab, since the site's weathering potential isn't a design input (the
default is the strength to specify, not one assumed of an existing slab). The user's 1800 psi for
Bowen Mountain is below every cell of the table; it stays as Bowen's value with its own source.

Secondary, not used: city handouts citing earlier IRC editions (2012, 2018) give 3,000 psi for
foundation walls, and Minnesota's amendment 5,000 psi for footings [C4]; editions and local
amendments differ, so a builder checks the code their jurisdiction adopted.

## C2. Eurocode 2: exposure classes and indicative strength classes (Verified)

EN 1992-1-1:2004 Table 4.1 [C2] (read in a third-party copy of the BSI printing): freeze/thaw
attack, "XF1 Moderate water saturation, without de-icing agent" (informative example: "Vertical
concrete surfaces exposed to rain and freezing"); "XF3 High water saturation, without de-icing
agents" ("Horizontal concrete surfaces exposed to rain and freezing"). Annex E, Table E.1N,
"Indicative minimum strength class" (recommended values; a country's National Annex may set
others): XC1 C20/25; XC2, XC3 C25/30; XC4 C30/37; XF1 C30/37; XF2 C25/30; XF3 C30/37; X0 C12/15.

A platform's top, horizontal and exposed to rain and freezing, is XF3: **C30/37**, f_ck 30 MPa on
cylinders (about 4,350 psi). Not used as the engine's default: the design files are in US units
and the IRC is the code a US builder works to; recorded so a European builder can set
`compressive_strength: 30 MPa` with this as its source.

## C3. Allowable bearing on concrete: AISC 360-16 §J8, as ACI 318 (Verified)

AISC 360-16 [C3] (the copy already read for door-headers.md [H7]), §J8, p.16.1-140–141: "In the
absence of code regulations, the design bearing strength, φcPp, and the allowable bearing
strength, Pp/Ωc, for the limit state of concrete crushing are permitted to be taken as follows:
φc = 0.65 (LRFD) Ωc = 2.31 (ASD)". "(a) On the full area of a concrete support Pp = 0.85f′c A1
(J8-1)"; "(b) On less than the full area … Pp = 0.85f′c A1 √(A2/A1) ≤ 1.7f′c A1 (J8-2)".
Commentary J8 (p.16.1-447): "The provisions of this section are identical to equivalent
provisions in ACI 318 and ACI 318M (ACI, 2014)." ACI 318 itself was not read (not freely
readable).

**Engine:** the mean pressure under each wall is checked against 0.85 f′c / 2.31 (ASD, J8-1, the
full area: a wall on a wider platform could take J8-2's √(A2/A1), up to twice, which is left out,
the safe side). With the platform's thickness, f′c is first reduced by EN 1992-1-2 Table 3.1
(siliceous, the lower row) at the top face's temperature, shown, not certified (the table is for
fire, 2–50 K/min).

## C4. Anchors: not sized

AISC 360-16 §J9 says anchor rods "should be designed as threaded parts per Table J3.2", and its
commentary that shear at a column base is usually carried by friction or a shear key; the
concrete's own anchorage strength is ACI 318 Chapter 17, not read. So the engine reports each
post's foot reaction (shear outward; no uplift from a level thrust) and leaves the anchors to the
builder.

## C5. The floor's loss through the platform and its top face

From blocked-items.md §20: EN 1992-1-2 §3.3.3's lower limit λc = 1.36 − 0.136(θ/100) +
0.0057(θ/100)² W/(m·K), the one it says "gives more realistic temperatures", is the platform's
conductivity, the platform taken as wide as the floor on dry soil (heatloss.py's disk on a
semi-infinite medium). Its top face, the floor's outside, is checked against ACI 349-97 §A.4's
long-term 150 °F (200 °F in local areas), a warning, as quoted by the NRC [K32].

## Block foundations (research round 2026-10-31, later)

Asked because Olsen's Bowen Mountain salt kiln is "built upon a concrete-block foundation covered
with common red bricks, followed by a layer of medium-duty firebricks" (*The Kiln Book*, p.126),
and the engine puts a trial 6 in platform's top face at about 1,731 °F under 7½ in of brick. In
short: **no published temperature limit for concrete block or cinder block was found**. What was
found is below; nothing here gives the engine a new number to check against.

### C6. Concrete block (CMU) at sustained temperature (Partial)

- Pope and Zalok, "Fire Impact on the Compressive Strength of Concrete Masonry Materials — A
  Review", *TMS Journal* 39(1), 2025, DOI 10.70803/001c.137880 [C5], abstract only (full text
  paywalled): "The residual compressive strength of concrete is usually unchanged below 400°C.
  Above 400°C the strength starts to decrease due to a combination of moisture loss, micro cracks,
  chemical decomposition, and thermal stresses. The strength loss can be mitigated by using thermal
  stable aggregate such as lightweight aggregates or certain recycled aggregates." Residual (after
  cooling), from fire tests, not sustained heating; no table read.
- UFSCar thesis, "Alvenaria estrutural com blocos de concreto" [C6], abstract only (search
  summary, not read in the original): prisms of two concrete blocks, mortars and grouts held one
  hour at 200, 400, 600 and 800 °C and tested cold; the grouts followed the residual curves for
  ordinary concrete in ACI/TMS 216 and Eurocode 2. No numbers read.
- University of Moratuwa thesis [C7], abstract only: solid cement–sand blocks met load-bearing
  strength requirements "up to 800 °C" (residual, short exposure). Not read further.
- TMS 216 / ACI 216.1: not read (paywalled). EN 1996-1-2 (Eurocode 6, masonry in fire) Annex D:
  not read; a national annex [C8] says thermal conductivity, specific heat and elongation are
  nationally determined, with Annex D giving their variation for some materials. NCMA's TEK notes on
  temperature: none found beyond TEK 3-7A (section C8 below).

**Status:** Not found as a sustained-temperature limit; Partial for residual strength (abstracts).
**Engine:** nothing to change. `foundation.py` checks the platform's top face against ACI 349's
150 °F / 200 °F (K32) and reduces f′c by EN 1992-1-2 Table 3.1; for a block platform the same cast-
concrete figures are the assumption (block is concrete; the hollow cores and mortar joints are not
modelled). Pope and Zalok's 400 °C is a residual-strength observation from fire tests and must not
be used as a long-term limit.

### C7. Cinder block and lightweight-aggregate block (Partial, fire ratings only)

The only sourced distinction found is the building code's fire-resistance table (IBC Table
722.3.2, TMS 216), which groups aggregates as "calcareous or siliceous gravel", "limestone, cinders
or slag", "expanded clay, shale or slate" and "expanded slag or pumice", by minimum equivalent
thickness per hourly rating. As printed by an aggregate maker [C9] (secondary, older edition):
expanded clay/shale/slate 2.6, 3.3, 3.6, 4.4, 5.1 in, and limestone/cinders/slag 2.7, 3.4, 4.0,
5.0, 5.9 in, for 1, 1.5, 2, 3 and 4 h. These are fire-test ratings (the unexposed face's rise in
ASTM E119), not temperature limits for the block. Pope and Zalok's abstract [C5] says lightweight
aggregates mitigate the loss. No temperature limit for cinder block was found. **Not found.**
**Engine:** nothing; the engine has no block material and should not invent one.

### C8. Practice for fireplaces, hearths and kilns on block or concrete (Verified, no temperature)

- IRC §R1001 (read in the 2025 California Residential Code [C10]): R1001.2 "Footings for masonry
  fireplaces and their chimneys shall be constructed of concrete or solid masonry"; R1001.9
  "Masonry fireplace hearths and hearth extensions shall be constructed of concrete or masonry,
  reinforced to carry their own weight and all imposed loads. Combustible material shall not remain
  against the underside of hearths and hearth extensions after construction."; R1001.9.1 "The
  minimum thickness of fireplace hearths shall be 4 inches (102 mm)."; R1001.9.2 "The minimum
  thickness of hearth extensions shall be 2 inches (51 mm)."; R1001.5: back and side walls 8 in of
  solid masonry where "a lining of firebrick not less than 2 inches (51 mm) thick" is provided, 10
  in without. No temperature for the hearth or its base.
- NCMA TEK 3-7A, *Concrete Masonry Fireplaces* (2003 review draft) [C11], p.2–3: the base is "a
  concrete footing and concrete masonry foundation walls"; "The concrete slab should be 4 in. (102
  mm) thick, reinforced and capable of resisting thermal stresses resulting from high
  temperatures." Fire brick to ASTM C27 or C1261, at least 2 in, laid in medium-duty refractory
  mortar (ASTM C199), joints no larger than ¼ in. No temperature figure. So in a fireplace the
  block is the foundation and the firebox sits on a 4 in concrete slab plus firebrick: the same
  layering as Bowen Mountain's.
- NFPA 211: not read.
- Kiln practice: a Ceramic Arts Daily forum thread [C12] (anecdotal) advises hollow block with the
  cores laid horizontal and left open "so air can move through", warns that building straight on a
  slab risks the heat "calcining, spalling, or even blowing up the slab", and one poster with a
  cone 11 car kiln on hollow block and about 8 in of clearance says the slab "still gets warm". No
  measured temperature. No published kiln-building guide with a figure was found.

**Engine:** nothing new to check. A possible option (not a warning, not built): a ventilated
hollow-block course as the platform, which the heat-loss model cannot represent today (it takes a
solid disk on dry soil, the safe side for the top face).

### C9. Conductivity and density of block (Partial)

- Conductivity rises with density (Masonry Advisory Council, *Lightweight CMU Advantages* [C13],
  citing NCMA TEK 6-2A); its text and tables did not extract legibly (font encoding), so no number
  is taken from it.
- Resistivity of core-fill concrete at 140 lb/ft³, 0.114 h·ft²·°F/(Btu·in), quoted in a RESNET
  public comment [C14] (secondary; ≈ 8.8 Btu·in/(h·ft²·°F), ≈ 1.26 W/(m·K) **derived**).
- NCMA TEK 6-2C (R-values of single-wythe walls, series-parallel method), ACI/TMS 122R-14 and the
  ASHRAE Handbook tables: not read (paywalled or not found free). EN 1996-1-2 Annex D: not read.

**Engine:** `heatloss.py` takes the platform as solid concrete with EN 1992-1-2's lower-limit
conductivity (1.33 W/(m·K) at 20 °C) and 2300 kg/m³. For a hollow, unfilled block platform this
over-states conduction (the safe side for the floor's loss, the unsafe side for nothing the engine
checks). Keep it until TEK 6-2C or ACI 122R gives sourced figures.

### C10. Concrete past ACI 349 (Partial)

Beyond K31/K32: Pope and Zalok [C5] (above) give "usually unchanged below 400°C" for residual
strength, losses above from "moisture loss, micro cracks, chemical decomposition, and thermal
stresses". No sourced staged dehydration temperatures (paste, portlandite) were read in a primary
source this round. **Engine:** no change; the top face over 150 °F stays a warning, and Table 3.1's
reduction stays shown, not certified.

## Sources

- [C1] 2025 California Residential Code, §R402.2 and Table R402.2 (the IRC's text):
  https://gocodebook.com/library/us/ca/ca-residential-code/chapter-4-foundations/section-r402-materials
  (read 2026-10-31; codes.iccsafe.org returned 403).
- [C2] BS EN 1992-1-1:2004, *Eurocode 2: Design of concrete structures — Part 1-1*, Table 4.1 and
  Annex E Table E.1N: https://www.phd.eng.br/wp-content/uploads/2015/12/en.1992.1.1.2004.pdf
  (third-party copy, read 2026-10-31).
- [C3] AISC, *ANSI/AISC 360-16 Specification for Structural Steel Buildings*, §J8, §J9 and
  Commentary J8: https://user.eng.umd.edu/~ccfu/ref/a360-16-spec-and-commentary.pdf (official:
  https://www.aisc.org/globalassets/aisc/publications/standards/a360-16-spec-and-commentary.pdf).
- [C4] Secondary, not used: Penn State PHRC Concrete 101 handout,
  https://www.phrc.psu.edu/assets/docs/webinars/Concrete101Handouts.pdf ; Minnesota Rules
  1309.0402, https://www.revisor.mn.gov/rules/1309.0402/ .
- [C5] H. Pope and E. Zalok, "Fire Impact on the Compressive Strength of Concrete Masonry
  Materials — A Review", *TMS Journal* 39(1), 2025, abstract page:
  https://journal.masonrysociety.org/article/137880.pdf (read 2026-10-31; full text paywalled).
- [C6] UFSCar repository, "Alvenaria estrutural com blocos de concreto…":
  https://repositorio.ufscar.br/handle/20.500.14289/18898 (abstract, via search summary).
- [C7] University of Moratuwa thesis on masonry units at elevated temperature:
  https://dl.lib.uom.lk/handle/123/25494 (abstract, via search summary).
- [C8] Cyprus National Annex to CYS EN 1996-1-2:2005:
  https://moi.gov.cy/MOI/moiup/moi.nsf/all/05FE06BB537676ACC22585A100430DF8/$file/Cyprus%20National%20Annex%20to%20CYS%20EN%201996_1_2_2005%20INCLUDING%20AC_2010%20-%20CORRECTED%20VERSION%20ON%2023%2008%202019.pdf
  (via search summary, not read in full).
- [C9] Norlite, fire resistance table: https://www.norliteagg.com/sites/default/files/imce_images/fire_resistance.pdf
  (via search summary; secondary, older IBC edition).
- [C10] 2025 California Residential Code §R1001:
  https://gocodebook.com/library/us/ca/ca-residential-code/chapter-10-chimneys-and-fireplaces/section-r1001-masonry-fireplaces
  (read 2026-10-31).
- [C11] NCMA, TEK 3-7A *Concrete Masonry Fireplaces* (2003 review draft), hosted at
  https://www.rumford.com/pdf/TEK3.pdf (read 2026-10-31).
- [C12] Ceramic Arts Daily forum, "Base isolation of wood fired kiln":
  https://community.ceramicartsdaily.org/topic/27607-base-isolation-of-wood-fired-kiln/ (via search
  summary; anecdotal).
- [C13] Masonry Advisory Council, *Lightweight CMU Advantages*:
  https://masonryadvisorycouncil.org/wp-content/uploads/2016/07/Lightweight_CMU_Advantages.pdf
  (downloaded; text illegible).
- [C14] RESNET public comment citing ACI 122 values:
  https://resnet.us/wp-content/uploads/formidable/224/Binder-Comment-Form-ACI-122-Table-PDF.pdf
  (via search summary).
