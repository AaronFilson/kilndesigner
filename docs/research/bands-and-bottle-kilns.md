# Bands round hot domes and round walls; bottle-oven sizes (third research round, 2026-10-31)

Third pass at `blocked-items.md` §1, §2 and §11 (bottle-kiln sizes, the allowable stress for a hot
band, iron against steel). Earlier rounds found only practice (FAO), a Snippet of EN 1993-1-2 and
secondary bottle-oven figures. This round read full texts: EN 1993-1-2 and EN 1992-1-2 (PDF copies
of the BSI printings), Kent's *Mechanical Engineers' Pocket-Book* (1916, Internet Archive), Norton's
*Refractories* (3rd ed. 1949, and 2nd ed. 1942, Digital Library of India scans on the Internet
Archive) and the Bureau of Standards' Technologic Paper 7 (1911).

Status marks as in `refractory-bearing.md`: **Verified** = read in the full text (here mostly OCR
of a scan; the OCR is quoted as read, obvious OCR slips corrected in square brackets);
**Snippet** = search extract or summary only; **Partial**; **NOT FOUND**. Primary = a standard,
handbook, maker's sheet, book or official report; secondary = a web page that does not cite a
source for its number.

## Short answer

| Question | Status | Usable number |
|---|---|---|
| Band steel's strength when hot (EN 1993-1-2 Table 3.1) | **Verified**, primary | k_y,θ = 1.000 to 400 °C, 0.780 at 500, 0.470 at 600, 0.230 at 700 °C; linear between rows |
| Wrought iron and steel tensile strength when hot (historic) | **Verified**, primary (handbook quoting tests) | Kollmann and Franklin Institute tables in Kent (below) |
| A factor of safety for a dome's tension band | **Verified**, primary | "at least 5" (Norton, *Refractories*, 1949, p. 732) |
| General factors of safety, iron and steel, dead load | **Verified**, primary | 3 on ultimate (Rankine; Unwin), Kent's lowest "3" |
| Furnace binding stress limit | Verified (already in `kiln-hardware.md` [S20]; re-read in the 2008 HW guide) | 12,000 psi |
| ASME II-D Table 1A for SA-36 | NOT FOUND (no free copy) | none |
| Creep of band steel in long service | NOT FOUND (EN 1993-1-2 covers fire heating only) | none |
| Band's temperature on a kiln's outside | Partial: one measured electric-kiln shell, no brick-kiln band | 538 °F (281 °C), K25 electric kiln at cone 6 (student report) |
| How bottle-oven bonts were sized or tightened | NOT FOUND (spacing only, secondary) | about 12 in apart |
| Iron or steel | Verified sources on strength and corrosion; no kiln source compares them | see §4 |
| Bottle-oven sizes | Partial, secondary | several ovens (§6) |

---

## 1. Steel strength at temperature: EN 1993-1-2:2005 Table 3.1 (Verified)

Read in BS EN 1993-1-2:2005 (incorporating corrigendum December 2005), §3.2.1, Table 3.1, p. 22
[N1]. The PDF is a scan; values below read from its text layer and checked row by row.

> "(1) For heating rates between 2 and 50 K/min, the strength and deformation properties of steel at
> elevated temperatures should be obtained from the stress-strain relationship given in figure 3.1.
> NOTE: For the rules of this standard it is assumed that the heating rates fall within the specified
> limits." (§3.2.1)

> "Table 3.1: Reduction factors for stress-strain relationship of carbon steel at elevated
> temperatures" ... "NOTE: For intermediate values of the steel temperature, linear interpolation may
> be used."

| Steel temperature θa | k_y,θ = f_y,θ / f_y (effective yield) | k_p,θ = f_p,θ / f_y (proportional limit) | k_E,θ = E_a,θ / E_a (elastic slope) |
|---|---|---|---|
| 20 °C | 1.000 | 1.000 | 1.000 |
| 100 °C | 1.000 | 1.000 | 1.000 |
| 200 °C | 1.000 | 0.807 | 0.900 |
| 300 °C | 1.000 | 0.613 | 0.800 |
| 400 °C | 1.000 | 0.420 | 0.700 |
| 500 °C | 0.780 | 0.360 | 0.600 |
| 600 °C | 0.470 | 0.180 | 0.310 |
| 700 °C | 0.230 | 0.075 | 0.130 |
| 800 °C | 0.110 | 0.050 | 0.090 |
| 900 °C | 0.060 | 0.0375 | 0.0675 |
| 1000 °C | 0.040 | 0.0250 | 0.0450 |
| 1100 °C | 0.020 | 0.0125 | 0.0225 |
| 1200 °C | 0.000 | 0.0000 | 0.0000 |

Also read: "(2) The mechanical properties of steel at 20 °C should be taken as those given in EN
1993-1-1" (§3.1); unit mass "ρa = 7850 kg/m3" (§3.2.2); and, §4.3 (p. 43), "Provided that the
stress-strain relationships given in section 3 are used, the effects of transient thermal creep need
not be given explicit consideration."

Scope, important for a kiln band: the table is for **fire** (heating at 2 to 50 K/min, a few
hours); "effective yield" is the stress at 2 % strain. A band sits warm for the whole of every
firing, for years. Transient creep is built into the table; long-term creep is not. So the table is
an authoritative upper bound on strength for the band's temperature, not a long-service allowable.
The earlier Snippet ([K21] in `blocked-items.md`) is confirmed for 400 and 500 °C; its 0.93 at
450 °C is the linear interpolation (1.000 + 0.780)/2 = 0.89, **not** 0.93: the Snippet's 450 and 550
values do not match the standard and should not be used.

**Engine (`frame` band check, dome hoop tension):** allowable = f_y(20 °C) × k_y,θ(T_band) / FoS,
interpolated linearly, refusing above the band temperature the designer can justify (ADR 0009). At
or below 400 °C, k_y,θ = 1.0. Because the band must not stretch (it holds the dome by staying tight),
the proportional limit k_p,θ (0.42 at 400 °C) is the more cautious factor for "no permanent set";
which to use is a design decision no source makes for kiln bands.

## 2. Historic hot-strength tests of wrought iron and steel (Verified, primary handbook)

Kent, *The Mechanical Engineer's Pocket-Book*, 9th ed. (1916), "Tenacity of Metals at Various
Temperatures", pp. 463–464 [N2]. Kent quotes three test series.

**Huston (Jour. Franklin Inst., 1877), boiler plate, average of three tests each:**

| Material | 68 °F | 575 °F | 925 °F |
|---|---|---|---|
| Charcoal iron plate, tensile strength, lb/in² | 55,366 | 63,080 | 65,343 |
| Soft open-hearth steel | 54,600 | 66,083 | 64,350 |
| Crucible steel | 64,000 | 69,266 | 68,600 |

**Howard (Watertown Arsenal; Iron Age, 10 Apr 1890), as summarised by Kent:** steel's tensile
strength falls to a minimum between 200 and 300 °F, then rises "up to a temperature of 400° to
650° F.", then "decreases steadily at a rate approximating 10,000 lbs. decrease per 100° increase of
temperature. A strength of 20,000 lbs. per square inch is still shown by 0.10 C. steel at about
1000° F." "The strength of wrought iron increases with temperature from 0° up to a maximum at from
400 to 600° F., the increase being from 8000 to 10,000 lbs. per square inch, and then decreases
steadily till a strength of only 6000 lbs. per square inch is shown at 1500° F."

**Kollmann (Oberhausen; Jour. F. I., cxii, 1881, p. 241), with the Franklin Institute committee's
1832–36 results for comparison.** Materials: "fibrous iron of 52,464 lbs. T. S., 38,280 lbs. E. L.,
and 17.5% elong.; fine-grained iron of 56,892 lbs. T. S., 39,113 lbs. E. L., and 20% elong.; and
Bessemer steel of 84,826 lbs. T. S., 55,029 lbs. E. L." Mean ultimate tensile strength as a percentage
of that at ordinary temperature:

| °F | Fibrous iron | Fine-grained iron | Bessemer steel | Franklin Institute (1832–36) |
|---|---|---|---|---|
| 0 | 100.0 | 100.0 | 100.0 | 96.0 |
| 100 | 100.0 | 100.0 | 100.0 | 102.0 |
| 200 | 100.0 | 100.0 | 100.0 | 105.0 |
| 300 | 97.0 | 100.0 | 100.0 | 106.0 |
| 400 | 95.5 | 100.0 | 100.0 | 106.0 |
| 500 | 92.5 | 98.5 | 98.5 | 104.0 |
| 600 | 88.5 | 95.5 | 92.0 | 99.5 |
| 700 | 81.5 | 90.0 | 68.0 | 92.5 |
| 800 | 67.5 | 77.5 | 44.0 | 75.5 |
| 900 | 44.5 | 51.5 | 36.5 | 53.5 |
| 1000 | 26.0 | 36.0 | 31.0 | 36.0 |
| 1100 | 20.0 | 30.5 | 26.5 | — |
| 1200 | 18.0 | 28.0 | 22.0 | — |
| 1400 | 13.5 | 19.0 | 15.0 | — |
| 1600 | 7.0 | 12.5 | 10.0 | — |
| 1800 | 4.5 | 8.5 | 7.5 | — |
| 2000 | 3.5 | 5.0 | 5.0 | — |

(OCR read "30 5", "18 0" etc. for 30.5, 18.0; the Franklin column stops at 1000 °F in the scan.)

These are **short-time ultimate tensile** tests, not yield and not creep. They agree with EN
1993-1-2 in shape: little loss to about 600 °F (315 °C), then a steep fall past 700 °F (370 °C).
The Franklin Institute's own 1837 report was not read (the 1830s originals were not found as a free
full text this round; Kent's column is the secondary route to them).

## 3. Factor of safety for a band

| Source | Text | Status |
|---|---|---|
| Norton, *Refractories*, 3rd ed. (1949), ch. "Brickwork construction", §6 Domes, "Steelwork", p. 732 [N3] | "The dome is particularly easy to brace because a simple tension band around the base will take care of the stresses completely. The section of this band can be easily computed from the formulas previously given, allowing a factor of safety of at least 5 to take care of the elevated temperatures, corrosion, and scaling." Same words in the 2nd ed. (1942) [N4] | **Verified**, primary |
| Norton, same, on arch buckstays (p. 704) | "The strength of these sections can be readily computed from the thrust of the arch, but a considerable factor of safety ..." (the sentence runs on past a figure; its end was not found in the OCR; no number) | Verified (no number) |
| HarbisonWalker, *Brick Installation Guide* (2008), p. 20 [N5] | "The safety factor used in furnace binding design is ordinarily higher than that used in conventional steel structural design because the furnace binding may become overheated. For ordinary structural steel bindings, many furnace designers limit tensile stress to 12,000 pounds per square inch." | Verified (same text as `kiln-hardware.md` [S20]) |
| Kent (1916), "Factors of Safety", pp. 374–376 [N2] | Rankine: iron and steel, dead load 3, live load 6; masonry dead load 4. Unwin: "Wrought iron and steel" 3 (dead load), 5 (varying, one kind), 8 (alternating), 12 (shocks); "Brickwork and Masonry" 20 (dead load). Kent: "When the ultimate strength of the material is known within narrow limits ... when the load is entirely a steady one of a known amount, and there is no reason to fear the deterioration of the metal by corrosion, the lowest factor that should be adopted is 3." Rule 6: "When the piece is subject to deterioration from corrosion the section should be sufficiently increased to allow for a definite amount of corrosion" | **Verified**, primary (factors on **ultimate** strength) |

Norton does not say whether his "5" is on ultimate or elastic strength. Read with Kent's convention
of the period (factors on ultimate), 5 on A36's 58 ksi minimum tensile gives 11.6 ksi, close to
HarbisonWalker's 12,000 psi **(derived; the agreement is ours, not a source's)**. Norton's band-force
formula (p. 729–730, "The band stress, however, is approximately given by Total weight of dome /
... cos ½θ") is garbled in both OCR copies and was **not** transcribed; it cites Goodier, "Stresses
in Domes and Crowns of Circular Kilns", *J. Am. Ceram. Soc.* 16 (5), 1933, p. 220, and Fellows,
which were not read. The engine's membrane hoop tension (`domes-over-doors.md` §D1) stays the force.

**Engine:** the band check can now pass/fail: band stress = hoop tension / band area ≤
min(12,000 psi [HW], f_u/5 [Norton]) with the temperature factor of §1 when the band's temperature
is known; corrosion allowance is the designer's (Kent rule 6, no number).

## 4. Iron or steel?

No source read compares them for kilns. What is sourced:

- **Strength when hot:** Kollmann's table (§2) shows Bessemer steel losing strength faster than
  either wrought iron from 700 to 900 °F (68 % against 81.5 to 90 % at 700 °F), but steel starts much
  stronger (84,826 against 52,464 to 56,892 lb/in²). At 700 °F the steel still carries about 57,700
  lb/in² against 42,800 to 51,200 for the irons **(derived from the table)**. Huston's boiler-plate
  tests show soft steel and charcoal iron alike to 925 °F.
- **Corrosion:** H. M. Howe (Proc. ASTM 1906), quoted by Kent p. 466: "there is no very great
  difference between the corrosion of steel and wrought iron. Under certain conditions steel seems to
  rust a little faster than wrought iron, and under others wrought iron seems to rust a little faster
  than steel." "Carelessly made steel, containing blowholes, may rust faster than wrought iron, yet
  carefully made steel ... may rust more slowly."
- **Expansion:** Howard's coefficients (Kent p. 465): wrought iron 0.0000067302 per °F; steels
  0.0000061700 to 0.0000067561 per °F. The same within a few percent.
- **Practice:** bottle-oven bonts were iron (secondary, §6); FAO's Brazilian beehive kiln uses a
  steel band ([K5]); Medalta's beehive kilns "corroding steel" (Snippet, [K6]).

So: today's mild steel (A36 or S235/S275) is the sourced choice: its hot strength is in a current
standard (§1), its room strength in ASTM A36 (`kiln-hardware.md` §4.7.4), and the historic tests
give wrought iron no strength advantage when hot. Wrought iron is no longer made as a commodity
(general knowledge, not sourced here). Corrosion: no clear difference (Howe).

## 5. The band's temperature

| Item | Finding | Status | Source |
|---|---|---|---|
| Electric kiln shell, L&L E23S-JH, 2½ in K25 IFB in stainless jacket, cone 6 fast glaze | "The top exterior section reached a maximum temperature of 538.2 oF, while the bottom exterior section reached a maximum temperature of 517.6 oF"; lid 345.0 °F; "the temperature of the floor did manage to reach 129.1 oF" (slow bisque: floor peak 122.5 °F) | Verified (read); secondary-grade (a student class memo, Auburn CHEN 3600, 2012) | [N6] |
| Brick kiln, bottle oven or beehive: band or outer-wall temperature measured | none | NOT FOUND | search |
| Cement rotary-kiln shells | 200–280 °C quoted in a maintenance blog for a burning zone | Snippet; different plant (steel shell over thin lining), not used | search |

The engine already computes the outer face temperature of each wall from its layers (heat loss);
that computed cold-face temperature is the band's temperature to feed §1's table, with the refusal
above the range the designer accepts. No measured brick-kiln band temperature backs it.

## 6. Bottle ovens: sizes found

All secondary unless marked; none gives a hovel's top diameter except where stated.

| Oven | Figure | Status | Source |
|---|---|---|---|
| Sutherland Works, Longton (Hudson & Middleton), skeleton updraught, last firing 1978 | "Diameter: 14 feet (4.25m)"; "Height to shoulder: 14 feet (4.25m)"; "Rise from shoulder to top of crown: 2.11 feet (0.9m)" [sic: 0.9 m ≈ 2.95 ft]; 8 firemouths; 1174 saggars | Verified on page; secondary | [N7] |
| Middleport Pottery, Burslem, biscuit oven | "11 firemouths in its firing chamber of 18 feet 6 inches internal diameter" | Verified on page; secondary | [N8] |
| Falcon Pottery (Weatherby), Hanley, glost | chamber "about 20ft (6m) in diameter", 10 firemouths | Verified on page; secondary | [N9] |
| Dudson's, Hope Street, Hanley (hovel only) | "The hovel itself is 60' high and has an overall diameter of 33'3"" (base, presumably) | Verified on page; secondary (cites the Grade II listing; the listing text read via thepotteries.org says only "circular hovel, larger scale than most") | [N9], [N10] |
| Falcon Works, Sturgess St, Stoke, No. 1 oven (1976 survey notes) | clamming "approximately 9' high and 20" wide at the bottom", "3'7" wide at the widest point"; 8 firemouths; floor "rose 9" to a central bung 9" diameter"; "a central crown damper 18" diameter"; "The rise in the crown of the kiln was 4'" | Verified on page; quoted primary survey notes (Operation Bottle, 1976) | [N11] |
| King Street, Fenton, calcining kiln stack (not a bottle oven) | stack "rising 37' 6" above the level of the building top", top "with a diameter of 6'" | as above | [N11] |
| Furlong Mills calcining kilns | "stand 42 feet high, well below the minimum 60 feet specified by the regulations of 1877" | as above | [N8] |
| Smallest Potteries chamber | "only 3.35m or 11 feet in diameter" (oven not named in the extract) | Snippet | search |
| Oven wall; bonts | wall "approximately one foot thick"; "Iron bands known as BONTS ... set about twelve inches apart"; hovel "up to seventy feet tall" | Verified on page; secondary | [N12] |
| Bont section, tightening method | none | NOT FOUND | |
| Hind (1937), Sandeman (1901), Historic England HAZ survey reports, Cardew *Pioneer Pottery* | not found as free full text | NOT FOUND | |

So the chamber's diameter (11 to 20 ft) and crown rise (about 3 to 4 ft over 14 to 18 ft) have
secondary figures, and one hovel has a base diameter (33 ft 3 in) and height (60 ft). **No top
diameter of any hovel was found**; the cone frustum's taper stays unsourced and the chimney stays a
straight stack.

---

## Sources

- [N1] BS EN 1993-1-2:2005, *Eurocode 3: Design of steel structures — Part 1-2: General rules —
  Structural fire design* (incorporating corrigendum December 2005). PDF read:
  https://www.phd.eng.br/wp-content/uploads/2015/12/en.1993.1.2.2005.pdf (a third-party copy of
  the BSI printing, the same file Public.Resource.Org circulated; the standard is superseded by EN
  1993-1-2:2024, whose table was not compared). §3.1, §3.2.1–3.2.2, Table 3.1 (p. 22), §4.3.
- [N2] W. Kent, *The Mechanical Engineer's Pocket-Book*, 9th ed. (Wiley, 1916). Internet Archive
  `mechengpockbook00kentrich`, full text:
  https://archive.org/details/mechengpockbook00kentrich . pp. 374–376 (factors of safety), 463–466
  (tenacity at temperature, expansion, corrosion).
- [N3] F. H. Norton, *Refractories*, 3rd ed. (McGraw-Hill, 1949). Internet Archive (Digital Library
  of India) `dli.ernet.239470` and `in.ernet.dli.2015.462020` (both the 3rd ed.):
  https://archive.org/details/dli.ernet.239470 . pp. 408–417 (load tests, design use), 729–733
  (domes, Table 155, dome brick estimate, steelwork).
- [N4] F. H. Norton, *Refractories*, 2nd ed. (McGraw-Hill, 1942). `in.ernet.dli.2015.205928`:
  https://archive.org/details/in.ernet.dli.2015.205928 . "Domes", same text.
- [N5] Harbison-Walker Refractories Co., *Brick Installation Guide* (2008). PDF read:
  https://ssfbs.com/wp-content/uploads/2021/06/HW_Brick_Installation_Guide.pdf . pp. 9, 11, 20.
- [N6] Auburn University CHEN 3600 class memorandum, "Detailed Analysis of Kiln Temperature Data"
  (13 Feb 2012). https://www.eng.auburn.edu/~tplacek/courses/3600/better5.docx (read).
- [N7] "The Last Bottle Oven Firing 1978: Type of Oven", https://lbof1978.blogspot.com/p/what-type-of-oven-was-it.html (read).
- [N8] "The Potteries Bottle Oven: Burslem", https://bottleoven.blogspot.com/p/burslem.html (read, first 100,000 characters).
- [N9] "The Potteries Bottle Oven: Hanley", https://bottleoven.blogspot.com/p/hanley.html (read).
- [N10] thepotteries.org, listed building 51a (Dudson, Hope Street), https://thepotteries.org/listed/51a.html (search extract).
- [N11] "The Potteries Bottle Oven: The Bottle Oven Survey of 1976", https://bottleoven.blogspot.com/p/operation-bottle-survey-of-remaining.html (read; quotes the Operation Bottle survey notes, Frank Galbraith's team).
- [N12] thepotteries.org, "How the Bottle Kiln works", https://www.thepotteries.org/bottle_kiln/bottle_kiln_two.htm (read).
