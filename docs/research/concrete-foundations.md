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
