# Kiln hardware reference data

Checked: 2026-10-22. Scope: US studio gas kilns, stoneware to cone 10, about 10 to 60 ft³.
Every number has a source tag like [S3]. The tags are listed under "Sources" at the end.

How values are marked:
- **Verified** means I read it on the page or in the PDF text itself.
- **Excerpt** means I saw it only in a search-engine snippet or summary.
- **Derived** means I calculated it from sourced inputs. The working is shown.
- **(secondary)** means a forum post or similar, passing on practice rather than a design rule.
- **NOT FOUND** means I found no source. Do not fill these gaps with guesses.

Notes on the sources:
- PDFs were read as text with `pdftotext`. Drawings inside them (dimension call-outs on
  shape sketches) could not be seen, so drawing-only values are marked as such.
- Most kiln-scale numbers come from single documented builds, chiefly Vince Pitelka's
  handouts (Tennessee Tech, Appalachian Center for Craft) [S4] [S5] [S11] [S13]. A single
  build shows what worked once. It is not a design rule. The tables say which kiln each
  number comes from.
- The arch method and skewback shapes come from HarbisonWalker's *Brick Installation Guide*
  (2008) [S20]. That is an industrial furnace manual. Its method is general, but its worked
  example is a 12 ft basic-brick roof, far larger than a studio kiln.
- Olsen's *The Kiln Book* and Rhodes' *Kilns* are on the Internet Archive, but only as
  borrow-only scans. Their text could not be read. Olsen is cited only where a forum quotes him.

Cross-references: this file adds to `combustion-and-masonry.md` (§3 burners, §4 flue and
chimney, §6.5 arches, §7 car against door) and `electric-and-thermal.md` (§4.1 IFB density,
§5 brick sizes). It does not repeat what those files already source.

---

## 1. Burner ports

### 1.1 Port size and burner set-back

| Rule or measurement | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Port size (Ward) | port hole "an inch wider than the head of your burner" | electric-to-gas conversion article (Marc Ward, *Clay Times*, May 2003) | Verified | [S1] |
| Burner set-back (Ward) | burner "at least a half of an inch back from the outside of the burner port"; further back is fine, closer is not | same | Verified | [S1] |
| Burner set-back, power burners (Ward MB series) | placement diagram labelled "offset burner 1/2" to 1"" | MB power-burner operating instructions. The diagram itself could not be seen, so the direction of the offset is inferred, not read | Verified (label text) | [S2] |
| Port design (Ward) | open port: secondary air flows around the burner. Burner and pilot must sit "within the perimeter of the port and set back from the outside wall". Too far in shortens nozzle life and makes pilots unstable. Too small a port does the same | general | Verified | [S3] |
| Port taper (Ward) | 15° taper "preferred but not at all necessary" | general; already in `combustion-and-masonry.md` §4.1 | Verified | [S3] |
| Port size, GACO MR-100 (Pitelka) | 4.5 in wide × 5 in high (half a brick wide, two courses high), through a 9 in wall, lined with hard brick | 20 ft³ cross-draft soda kiln, 3 × MR-100 on LPG | Verified | [S4] [S5] |
| Port spacing (Pitelka) | 3 ports, 7 in pillars between them, burners on 11.5 in centres | same | Verified | [S5] |
| Port height (Pitelka) | ports one course (2½ in) above the floor, so pooled soda cannot run into them | same (salt/soda reason) | Verified | [S4] |
| Burner tip to port face (Pitelka) | ½ in for a reduction kiln that is not salt or soda; 3 in for salt or soda (to protect the cast-iron burners) | MR-100 venturis | Verified | [S5] |
| Port size, GACO MR-750 (Robinson) | 3½ in diameter hole in the kiln floor; top of the MR-750 ½ to ¾ in below the floor | 28 × 32 in downdraft conversion of an electric kiln, 2 × MR-750 | Verified | [S6] |
| Port size, 3 in burners (Berggren) | 3½ × 4½ in openings, 9 in deep, in the base of the doorway. "More than ample" secondary air; foil was used to cut it down | small downdraft, chamber floor 20 × 27 in (likely below the 10 ft³ range) | Verified | [S7] |
| Forum rule of thumb | "if your burner is 2.5" in diameter make the port 4.5"", that is 1 in all round | (secondary) | Excerpt | [S12] |
| Forum builds | ports about 4 × 4 in | (secondary) | Excerpt | [S12] |
| Exit flue against ports | exit flue area = total of all burner port areas (Ward) | already in `combustion-and-masonry.md` §4.1 | Verified there | |

**Derived checks:**
- Pitelka's kiln meets Ward's flue rule exactly. Ports: 3 × (4.5 × 5) = 67.5 in². Exit flue:
  9 × 7.5 = 67.5 in² [S4] [S5] **(derived)**.
- The two Ward rules (port = head + 1 in; tip ≥ ½ in back) and Pitelka's ½ in tip distance
  agree. Robinson's ½–¾ in is the same rule for a floor port.

### 1.2 Burner dimensions (for drawing the burner in front of its port)

Ransome torch-type straight-flame burners. "A" is the overall length. "B" and "C" are the two
end diameters; the catalogue drawing that says which end is which could not be seen [S9].
Ward's web page gives the same figures, except C for the B4 (3.5 in) [S8].

| Model | A, length (in) | B (in) | C (in) | Venturi | Source |
|---|---|---|---|---|---|
| B1 | 8½ | 1⅜ | 1⅞ | V050 | [S9] Verified |
| B2 | 10½ | 2¼ | 2¾ | V100 | [S9] Verified |
| B3 | 12 | 3¼ | 2¾ | V125 | [S9] Verified |
| B4 | 17 | 3¾ | 3⅜ (Ward: 3.5) | V150 | [S9] [S8] Verified |
| B5 | 21 | 5 | 4⅛ | V200 | [S9] Verified |

- Ward: the 90° angled head "will double the 'B' measurement" [S8].
- GACO MR-750 and MR-100 dimensions: **NOT FOUND**. Pitelka mounts the MR-100 with a 1½ in
  muffler clamp round its throat and gives its gas spud as ½ in male NPT [S5]. That is the only
  size clue.
- **Derived (use with care):** Ward's "head + 1 in" applied to the larger Ransome end diameter
  gives ports of about 4¼ in (B3), 4¾ in (B4) and 6 in (B5). This assumes the larger end is the
  head, which the text does not confirm.

### 1.3 Where the ports go

| Kiln type | Port position | Mark | Source |
|---|---|---|---|
| Downdraft (Geil patent) | burners vertical, in circular openings in the floor "immediately adjacent" the side walls, stopping short of the floor's inner surface. Flue opening at floor level, centred in the rear wall | Verified | [S10] |
| Downdraft conversion (Robinson) | burners fire up through floor holes. Spy hole on the side, "not in the area above the burners" | Verified | [S6] |
| Small downdraft (Berggren) | two ports at floor level in the base of the front (door) wall; flue channel along the floor to the back wall | Verified | [S7] |
| Cross-draft (Pitelka) | ports in the firebox end wall, one course above the floor, behind a bag wall; flue at floor level at the far end, into the chimney | Verified | [S4] |
| Converted electric / raku (Ward) | from the bottom shooting up, or from the side at floor level shooting across. Ward says placement matters little for raku | Verified | [S1] |
| Updraft | flue port(s) in the arch, each with its own kiln-shelf damper on deep kilns (Pitelka). Burner positions for a built updraft: **NOT FOUND** beyond Ward's conversion note | Verified (flue) | [S11] |

Bag walls (Pitelka): "always necessary in gas kilns with side-mounted burners" so the flames do
not hit the ware. Salt kiln: hard brick laid flat (4½ in). Soda: hard brick on edge (2½ in).
First course solid in front of the burners [S4].

### 1.4 Power-burner ports

- Port size for power burners: **NOT FOUND**. Ward's MB instructions give only the ½ to 1 in
  offset label and say that wrong port size or placement makes pilots "dance" and burns out
  thermocouples [S2].

---

## 2. Spy holes

### 2.1 Size

| Source | Size | Notes | Mark |
|---|---|---|---|
| Pitelka, hinged IFB door [S13] | round, 1½ to 2 in across at the outer face, widening to about 2½ in square at the inside face | wider inside gives a broader view. 2 in hole cut in a sheet-metal door skin | Verified |
| Pitelka, soda kiln walls [S4] | 2½ in high × 2¼ in wide (a quarter brick) | all spy holes in the kiln | Verified |
| Berggren [S7] | about 2½ × 2 × 4½ in, cut in the IFB inner wall; the 2½ in side tapers to 2 in | the taper makes the plug loosen on the slightest pull and wedge tight when pushed in | Verified |
| Pitelka, salt or soda [S13] | one extra, larger port about midway up the door | for pulling draw rings | Verified |

### 2.2 How many, and where

| Source | Count and position | Mark |
|---|---|---|
| Ward MB instructions [S2] | top, middle and bottom spy holes. Aim for positive pressure at the top and middle and neutral at the bottom. Short flames from the top and middle holes mean normal reduction; long flames mean over-reduction | Verified |
| Pitelka, 40 ft³ sprung-arch kiln, hinged door [S13] | bottom hole about 8 in above the inside floor, a few inches left of centre. Top hole about 1 ft below the inside peak of the arch, a few inches right of centre. Offset the two in opposite directions so they miss the centre shelf posts. "For a smaller kiln, these measurements should be reduced slightly" | Verified |
| Pitelka, 20 ft³ soda kiln [S4] | back wall: bottom hole just above the bottom shelf, a second about midway, a third about level with the bottom of the arch. Same pattern in the door. Keep holes off the centre shelf posts. Cone packs in the top and bottom holes, draw rings in the middle | Verified |
| Berggren [S7] | 8 holes: 5 on one side, 2 on the other, 1 looking at the flue | Verified |
| Norsker, *Self-Reliant Potter* [S14] | bricked door: spy holes at the top and bottom, "with neatly fitting bricks provided for closing the holes" | Verified |
| Robinson [S6] | on the side, not above the burners | Verified |

### 2.3 Plugs

- Pitelka: plugs cut from scrap IFB (they stay cooler and are easy to shape), or a hard-brick
  quarter brick ground to a taper [S4].
- Berggren: tapered rectangular plug. A ¼ in gap in one corner lets the plug stand ¼ to ½ in
  proud for grasping. One plug has a ½ in hole drilled through it for pyrometer readings [S7].
- Norsker: if loose-fill insulation is used, line the spy holes so the fill cannot run in [S14].
- Electric-kiln plugs (L&L, about ⅞ in diameter) are not gas-kiln parts [S27] (secondary).

---

## 3. Exit flue, chimney and damper

### 3.1 Flue and chimney cross-section

Rules:

| Rule | Value | Mark | Source |
|---|---|---|---|
| Flue area per chamber (Norsker) | "about 600 cm²" of flue for each 1 m³ of kiln chamber. The scan renders the superscripts as "?", so m³ is a reading, not certain | Verified (unit unclear) | [S14] |
| Same, in US units, reading m³ | 600 ÷ 6.4516 ÷ 35.315 = **2.63 in²/ft³**. Agrees with Olsen's 2.5 in²/ft³ (`combustion-and-masonry.md` §4.1), which supports the m³ reading | Derived | |
| Inlet against exit flue (Norsker) | "of equal but generous size" | Verified | [S14] |
| Flue against chimney (Norsker) | flues "slightly bigger than the cross-section of the chimney" | Verified | [S14] |
| Chimney base area (Norsker) | "approximately 10% of the area of the kiln chamber" (the text does not say floor area, but that is the likely reading) | Verified | [S14] |
| Chimney against flue (Olsen, 4th ed. p. 78) | chimney cross-section larger than the exit flue where it enters; the book's diagram narrows the entry by 25 % (4 bricks to 3) | (secondary) Excerpt | [S15] |
| Altitude (Norsker) | enlarge chimney and flue dimensions about 1 % per 100 m above sea level | Verified | [S14] |
| Gas speed (Olsen via Norsker) | about 1.2–1.5 m/s through the kiln at about 1100 °C; checked with an oily rag | Verified | [S14] |
| Chimney height (Norsker) | 3 m of chimney per 1 m of downward pull plus 1 m per 3.5 m of horizontal pull. (Olsen's rule in `combustion-and-masonry.md` §4.1 uses ⅓, not 1/3.5) | Verified | [S14] |

**Conflict:** Norsker makes the flues slightly bigger than the chimney. Olsen (as quoted) makes
the chimney bigger than the restricted flue entry. Pitelka's measured kiln (below) has the
chimney 1.2 × the flue, which fits Olsen.

Measured kilns:

| Kiln | Exit flue | Chimney inside | Ratio chimney ÷ flue | Source |
|---|---|---|---|---|
| Pitelka, 20 ft³ cross-draft, 3 × MR-100 | 9 × 7½ in = 67.5 in² | 9 × 9 in = 81 in² | 1.20 **(derived)** | [S4] Verified |
| Berggren, small downdraft | 2½ × 9 in = 22.5 in² through the back wall | 4½ × 4½ in = 20.25 in² (within two courses) | 0.90 **(derived)** | [S7] Verified |
| Berggren, same | largest damper opening in a successful firing: 2½ × 4½ in | | | [S7] Verified |
| Merrill flat-top (CM, Apr 2023) | flue opening 8 in wide × 5 in tall | not given | | [S16] Verified |
| Davis, Durango wood kiln (> 50 ft³) | two flue/damper shelves 9 × 18 in | chimney 9 in deep | | [S17] Verified |
| Forum, 15 ft³ sprung-arch downdraft with power burners | flue and chimney 8 × 4½ in inside | | | [S19] (secondary) Excerpt |

### 3.2 Chimney construction

| Item | Value | Mark | Source |
|---|---|---|---|
| Wall (Pitelka) | single thickness of hard brick (4½ in); laid with thin fireclay mortar, no sand; joints staggered. The rest of that kiln is dry-stacked; the chimney is mortared "to minimize air leakage and maximize draft" | Verified | [S4] |
| Height (Pitelka) | interior chimney height about twice the ware chamber height, natural-draft venturis. He no longer advises 8 ft above the arch unless a roof must be cleared | Verified | [S4] |
| Steel pipe (Pitelka) | formerly 10 in inside-diameter corrugated steel culvert above the kiln; on salt or soda kilns any pipe "will corrode through in three to five years" | Verified | [S4] |
| Bracing (Pitelka) | angle-iron verticals on all four corners; flat-bar cross-members at bottom, midpoint and top; tied to the kiln frame. "An unreinforced chimney is a death-trap in an earthquake" | Verified | [S4] |
| Cuzick soda kiln (≈ 25 ft³ stacking) | chimney one brick thick, hard brick, to the top of the kiln; then a 10 ft stainless stack rolled from two 5 ft pieces | Verified | [S18] |
| Berggren | brick to 30 in, then an 8 in, 12-gauge steel cylinder 7 ft tall through the roof, with 3 in clearance inside a 14 in galvanized sleeve at the roof | Verified | [S7] |
| Davis, Durango | 2 in angle corner posts for a 5 ft upper chimney frame; ¼ in mesh spark screen | Verified | [S17] |
| Geil downdraft | vertical flue "only to approximately the height of the exterior surface" of the crown | Verified | [S10] |
| Foundations (Norsker) | chimneys above about 6 m "need a good foundation" | Verified | [S14] |

### 3.3 Damper

| Item | Value | Mark | Source |
|---|---|---|---|
| Slot position (Pitelka) | about 1 ft above the top of the flue, on any face of the chimney | Verified | [S4] |
| Damper plate (Pitelka) | 11 × 26 in, 1 in thick mullite or cordierite kiln shelf | Verified | [S4] |
| Slot (Pitelka) | 12 in wide × 2½ in high (one course), walls of bricks cut to 3 in wide. A loose 2½ in slot lets a slagged damper be worked free. Close the gap above the damper with a soap and a quarter brick | Verified | [S4] |
| Lintel (Pitelka) | cast Mizzou block 18 × 4½ × 5 in spans the slot, replacing two courses | Verified | [S4] |
| Position (Berggren) | damper brick in the top course; position "not found to be critical" if expansion is allowed for | Verified | [S7] |
| Position (Norsker) | dampers go between the kiln's outlet flue and the chimney; an opening at the chimney base that bleeds in cold air also slows the pull | Verified | [S14] |
| Height around the damper (forum) | build the chimney to the top of the arch; "9" below the damper, 4.5" above" (12 ft³ downdraft) | (secondary) Excerpt | [S19] |
| Updraft (Pitelka) | a kiln-shelf damper over each flue port in the arch | Verified | [S11] |
| Durango wood kiln | two damper slots for 9 × 18 in dampers, plus two "passive" slots that admit air | Verified | [S17] |

- A rule linking damper size to flue size: **NOT FOUND**. The measured plates above are larger
  than their flues (Pitelka: 11 in plate across a 9 in chimney).

---

## 4. Steel frame for a sprung arch

### 4.1 What the frame does

- A sprung arch pushes down and out on its skewbacks. Walls (with or without steel) carry the
  vertical part. "The horizontal binding, including buckstays and tie rods, must contain the
  horizontal force" [S20] Verified.
- HarbisonWalker's industrial binding: (1) horizontal buttress beams along the furnace against
  the skewbacks, (2) vertical buckstays, (3) tie rods, I-beams or channels across the top
  joining opposite buckstays [S20] Verified.
- "When the skewback is carried on a channel or angle, the line of thrust should pass through,
  or slightly above, the corner of the supporting steel" [S20] Verified.
- "A stretcher course should never be used immediately below the skewback" [S20] Verified.
- Fit all the steel before the arch form comes out; the angle iron is "the only thing keeping
  the kiln together" (forum) [S21] (secondary) Excerpt. Pitelka gives the same order: walls up
  to the skews, frame welded, then the arch [S11] Verified.

### 4.2 Published member sizes

No source relates steel size to arch span. These are the sizes builders used.

| Kiln | Arch | Corner posts and buttress | Cross-members / rods | Mark | Source |
|---|---|---|---|---|---|
| Pitelka, general guidance | studio sprung arch | 3 × 3 × 3/16 in angle "generally adequate". Buttress: heavy angle on top of the side walls, welded between corner posts, vertical leg outside. Larger hard-brick arch: 2 × 6 in channel, legs outward | 8 cross-members, top and bottom on all four sides. Flat bar is enough with a stacked or roll-away door | Verified | [S11] |
| Pitelka, if a hinged door is fitted | | at least ¼ × 3 × 3 in angle for kilns of 24 ft³ or less; ¼ × 4 × 4 in for larger | top cross-members in angle, not flat bar | Verified | [S11] |
| Pitelka, 20 ft³ cross-draft soda kiln | 36 in span, 4½ in hard brick + 4 in insulating castable | ¼ × 2 × 2 in angle: corner posts, arch buttress members, front upper and lower members, burner-support member, door-side vertical | ¼ × 2 in flat bar for the other members; about 80 ft of angle and 50 ft of flat bar | Verified | [S4] |
| Berggren, small downdraft | 27 in span, 4½ in IFB, 4 in rise | windmill-leg angle iron | one ½ in rod front and back | Verified | [S7] |
| Davis, Durango wood kiln, > 50 ft³ | #1 arch and straights, 3 in series | 3 in angle at the corners; 6 in channel supports the arch | ½ in threaded rod, with springs | Verified | [S17] |
| Merrill flat-top (CM, Apr 2023) | flat roof, not an arch | roof angle 2 × 2 × 3/16 × 72 in | twelve 3/8 in threaded rods, 58 in long ("4 inches longer than the width of the kiln") | Verified | [S16] |
| Forum | | angle at each corner; angle or channel round the bottom; bracing halfway up; angle behind the skews | all-thread across the top, front and back, so it can be tightened | (secondary) Excerpt | [S21] |

Other frame details (Pitelka):
- Weld everything. "The idea of a bolted frame with spring-loaded expansion joints at the
  corners is misdirected" [S11] Verified.
- On the flue side of the soda kiln, the lower cross-member is ¼ × 2 in flat bar slipped
  through a ½ in gap left in the first floor course [S4] Verified.
- The burner-support cross-member sits one to one and a half bricks (about 4 in) below the
  ports to keep it cool [S4] Verified.

**Conflict:** HarbisonWalker says tie rods are "in some cases" spring-loaded or manually
adjusted for expansion [S20]. Pitelka and the forum advise against springs [S11] [S21]. The
Durango kiln used springs [S17].

Expansion allowance (Norsker): firebrick expands 0.5–1 % each time the kiln is fired and
shrinks back on cooling. Expansion joints of
about ½ cm per 1 m of wall, laid dry, are needed only in big square kilns of hard-fired brick
held by steel [S14] Verified (the "½ cm" is unclear in the scan).

### 4.3 Arch geometry and thrust (HarbisonWalker method)

Formulas [S20] Verified. S = span, h = total rise, d = rise in inches per foot of span,
T = thickness, r = inside radius, R = outside radius, θ = central angle.

1. r = S²/8h + h/2
2. R = r + T
3. h = r − √(r² − (S/2)²)
4. sin ½θ = S/2r
5. tan ¼θ = 2h/S
6. tan ¼θ = d/6
7. part of circle = θ/360°
8. skewback H = T sin ½θ
9. d = 6 tan ¼θ
10. inside arc = 6.2832 r (θ/360°)
11. outside arc = 6.2832 R (θ/360°)
12. skewback V = T cos ½θ
13. skewback P = Q tan ½θ

Check: for d = 1.608, θ = 60° and 6 × tan 15° = 1.608 **(derived)**.

Arch constants [S20] Verified:

| d (in/ft) | r | θ | part of circle | inside arc | H (skew) | V (skew) | P (skew) |
|---|---|---|---|---|---|---|---|
| 1 | 1.54167 S | 37° 50.9′ | 0.10514 | 1.01840 S | 0.32432 T | 0.94595 T | 0.34286 Q |
| 1¼ | 1.25208 S | 47° 4.4′ | 0.13076 | 1.02868 S | 0.39933 T | 0.91681 T | 0.43557 Q |
| 1½ | 1.06250 S | 56° 8.7′ | 0.15596 | 1.04117 S | 0.47059 T | 0.88235 T | 0.53333 Q |
| 1.608 | 1.00000 S | 60° 0.0′ | 0.16667 | 1.04720 S | 0.50000 T | 0.86603 T | 0.57735 Q |
| 1¾ | 0.93006 S | 65° 2.5′ | 0.18067 | 1.05579 S | 0.53760 T | 0.84320 T | 0.63757 Q |
| 2 | 0.83333 S | 73° 44.4′ | 0.20483 | 1.07251 S | 0.60000 T | 0.80000 T | 0.75000 Q |
| 2¼ | 0.76042 S | 82° 13.4′ | 0.22840 | 1.09125 S | 0.65753 T | 0.75342 T | 0.87273 Q |
| 2.302 | 0.74742 S | 83° 58.5′ | 0.23326 | 1.09544 S | 0.66896 T | 0.74329 T | 0.90000 Q |
| 2½ | 0.70417 S | 90° 28.8′ | 0.25133 | 1.11200 S | 0.71006 T | 0.70414 T | 1.00840 Q |
| 2¾ | 0.66004 S | 98° 29.7′ | 0.27360 | 1.13464 S | 0.75753 T | 0.65280 T | 1.16044 Q |
| 3 | 0.62500 S | 106° 15.6′ | 0.29517 | 1.15912 S | 0.80000 T | 0.60000 T | 1.33333 Q |

The guide also gives the outside-minus-inside arc length: 0.66059 T at 1 in/ft up to 1.85459 T
at 3 in/ft (1.04720 T at 1.608) [S20].

Forces in a cold arch, per foot of arch length [S20] Verified. D = brick density (lb/ft³),
S and T in feet. W = weight of brick per foot of arch length. The constants assume the line of
thrust runs from mid-thickness at the crown to mid-thickness at the skewbacks.

| d (in/ft) | W | H, horizontal thrust | F, resultant at skewback |
|---|---|---|---|
| 1 | 1.05 DST | 1.49 W | 1.57 W |
| 1¼ | 1.07 DST | 1.18 W | 1.28 W |
| 1½ | 1.09 DST | 0.98 W | 1.10 W |
| 1.608 | 1.10 DST | 0.91 W | 1.04 W |
| 1¾ | 1.11 DST | 0.83 W | 0.97 W |
| 2 | 1.14 DST | 0.72 W | 0.88 W |
| 2¼ | 1.17 DST | 0.64 W | 0.81 W |
| 2.302 | 1.17 DST | 0.62 W | 0.80 W |
| 2½ | 1.19 DST | 0.57 W | 0.76 W |
| 2¾ | 1.22 DST | 0.51 W | 0.71 W |
| 3 | 1.25 DST | 0.46 W | 0.68 W |

- Vertical force on each wall = W/2. F = √(H² + (W/2)²) [S20] Verified. Check at 2¼:
  √(0.64² + 0.5²) = 0.81 **(derived)**.

Maximum horizontal thrust in a heated arch "free to rise", as a multiple of the cold H above,
by arch thickness as a percentage of span [S20] Verified. "**" = "stress excessive".

| T/S | 1 | 1¼ | 1½ | 1.608 | 1¾ | 2 | 2¼ | 2.302 | 2½ | 2¾ | 3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 % | 1.88 | 1.61 | 1.47 | 1.43 | 1.39 | 1.33 | 1.29 | 1.28 | 1.26 | 1.24 | 1.22 |
| 5 % | 2.41 | 1.86 | 1.63 | 1.59 | 1.52 | 1.43 | 1.38 | 1.37 | 1.33 | 1.29 | 1.26 |
| 6 % | 3.29 | 2.29 | 1.94 | 1.79 | 1.67 | 1.56 | 1.47 | 1.46 | 1.42 | 1.37 | 1.33 |
| 7 % | 5.0 | 2.80 | 2.14 | 1.98 | 1.93 | 1.69 | 1.58 | 1.57 | 1.51 | 1.45 | 1.41 |
| 8 % | ** | 3.73 | 2.55 | 2.31 | 2.17 | 1.86 | 1.70 | 1.69 | 1.60 | 1.53 | 1.48 |
| 9 % | ** | 5.34 | 3.06 | 2.75 | 2.41 | 2.04 | 1.84 | 1.81 | 1.72 | 1.63 | 1.57 |
| 10 % | ** | ** | 3.88 | 3.30 | 2.77 | 2.22 | 2.00 | 1.95 | 1.82 | 1.73 | 1.63 |

Other HarbisonWalker statements [S20] Verified:
- Steel stress: "For ordinary structural steel bindings, many furnace designers limit tensile
  stress to 12,000 pounds per square inch", because the binding may run hot.
- Thickness limit: taking ¼ in per foot of span (S/48) as the lowest allowed rise of the line
  of thrust, T should not exceed (h − S/48) ÷ cos ½θ.
- The line of thrust in a cold arch should lie in the middle third of the brick.
- Worked example (industrial): 12 ft span, 13½ in thick, 192 lb/ft³ basic brick, 2¼ in/ft.
  W = 3,032.64 lb/ft, W/2 = 1,516.32, H = 1,940.89, F = 2,546.44, T/S = 9 % so
  Hmax = 1.84 H = 3,571.24 lb per foot of arch length.

### 4.4 Rise per foot of span

| Source | Rise | Mark |
|---|---|---|
| HarbisonWalker [S20] | simple roof arch: not less than 1 nor more than 3 in/ft. Fireclay 1½–3. Insulating firebrick 2–3. High-alumina at least 1.608. Basic 2¼–3. Silica 1–2. "A 1.608 inch rise, about 1⅝-inch, is a logical standard" (60° central angle, span = inside radius) | Verified |
| Norsker [S14] | "a rise of 20 cm for each 100 cm span is reasonable" (2.4 in/ft **derived**); 12.5–25 cm per 100 cm (1.5–3 in/ft **derived**) is normal good practice | Verified |
| Pitelka [S11] | prefers at least 2 in/ft; "very low arches are extremely risky in home-built studio kilns" | Verified |
| Cuzick [S18] | built at 1½ in/ft (about 25 ft³ stacking space) | Verified |

This closes the gap in `combustion-and-masonry.md` §6.5: the 1.608 in/ft (60°) arch is a
manufacturer's stated standard, not only a derivation. Note that HarbisonWalker puts IFB arches
at 2–3 in/ft, above that standard.

Pitelka's worked studio arches (both check against the HarbisonWalker constants):
- 45 in span, 2.3 in/ft: rise 8⅝ in, radius 2 ft 9⅝ in; 18 rows of #1 arch and 5 rows of
  straights [S11] Verified. HarbisonWalker at 2.302: r = 0.74742 × 45 = 33.63 in,
  h = 8.63 in **(derived)**.
- 36 in span, 2.3 in/ft: rise 6 15/16 in; 18 rows of #1 arch plus one straight in theory; in
  practice 16 rows of #1 arch, 2 rows of straights and a cast key row about 1¼ in wide [S4]
  Verified. The narrative prints the radius as "2' 15/16"", but its corrected form-radius
  (2 ft 2 13/16 in after taking off ⅛ in Masonite) shows 2 ft 2 15/16 in was meant.
  HarbisonWalker: r = 0.74742 × 36 = 26.91 in **(derived)**.
- Arch form: width = inside width less ¼ in clearance; wedges about 6 in long tapering 1 in to
  ¼ in; key row of a hard-brick arch cast in Mizzou, wedged apart every 4–5 in first [S4] [S11]
  Verified.

### 4.5 Worked thrust examples for studio arches (all derived)

Inputs: HarbisonWalker constants above; K-23 IFB density 32.0 lb/ft³ and super-duty dense brick
142 lb/ft³ from `electric-and-thermal.md` §4.1–4.2. All arches 4½ in thick (T = 0.375 ft).
Loads are per foot of arch length (front to back).

| Case | Span | Rise | T/S | W | W/2 | H (cold) | Hmax factor | Hmax |
|---|---|---|---|---|---|---|---|---|
| A: K-23 IFB | 45 in | 2.302 | 10.0 % | 1.17 × 32 × 3.75 × 0.375 = 52.6 lb/ft | 26.3 | 32.6 | 1.95 | 63.7 lb/ft |
| B: K-23 IFB | 54 in | 2.302 | 8.3 % | 63.2 | 31.6 | 39.2 | 1.73 (interpolated 8–9 %) | 67.8 |
| C: dense, 142 lb/ft³ | 54 in | 2.302 | 8.3 % | 280.4 | 140.2 | 173.8 | 1.73 | 300.6 |
| D: K-23 IFB | 54 in | 1.608 | 8.3 % | 59.4 | 29.7 | 54.1 | 2.46 (interpolated) | 132.7 |

Tie-rod check (derived): put the whole Hmax on two rods per side, one front and one back.
- Case B, 54 in deep arch: 67.8 × 4.5 = 305 lb per side, 152 lb per rod. At 12,000 psi that
  needs 0.013 in².
- Case C, 54 in deep arch: 1,353 lb per side, 676 lb per rod, 0.056 in².
- A ⅜ in rod has a gross area of 0.110 in², a ½ in rod 0.196 in² (π d²/4). Threads reduce this;
  the thread stress area is not in `docs/research/`.
- So for studio spans, arch thrust alone does not size the rods. The ½ in rods builders use
  [S7] [S17] are well above it. Stiffness, door loads and heat probably govern, but no source
  quantifies that.

Thickness check (derived from the HarbisonWalker limit):
- 36 in span at 2.302 in/ft: T may be up to (6.91 − 0.75) ÷ cos 42.0° = 8.3 in. A 4½ in arch
  passes.
- 36 in span at 1.608 in/ft: T up to (4.82 − 0.75) ÷ cos 30° = 4.7 in. A 4½ in arch only just
  passes; a 9 in arch fails.

### 4.6 Limits of the method (for ADR 0009 refusals)

- The heated-arch table covers T/S from 4 % to 10 % only. A 4½ in arch has T/S above 10 % for
  any span under 45 in (36 in span: 12.5 %). **No sourced Hmax for those arches.**
- The constants cover the arch brick's own weight. Insulation laid on top of the arch (Pitelka
  adds 4 in of castable [S4] [S11]) is extra load the tables do not include. **NOT FOUND.**
- The W factors bake in a typical thickness ratio. The exact weight is D × T × (mean of inside
  and outside arc) per foot, from formulas 10 and 11 **(derived)**.
- Hmax is for an arch "free to rise". Thrust in an arch held rigidly against expansion is not
  given. **NOT FOUND.**
- Bending of a buttress angle or channel spanning between corner posts needs steel section
  properties, which are not in `docs/research/`. **NOT FOUND.**

---

## 5. Skewback bricks

### 5.1 Standard 9-inch series shapes (HarbisonWalker)

Sizes are length × width × thickness in inches. "(a − b)" means the dimension tapers from a to
b. Brick equivalents are against a 9 × 4½ × 2½ straight. From the guide's shape drawings and
size table [S20] Verified.

3 in series:

| Shape | Size (in) | Brick equiv. |
|---|---|---|
| 48° side skew | 9 × (4½ − 1 13/16) × 3 | 0.84 |
| 60° side skew | 9 × (4½ − 2¾) × 3 | 0.97 |
| 48° end skew | (9 − 6 5/16) × 4½ × 3 | 1.02 |
| 60° end skew | (9 − 7¼) × 4½ × 3 | 1.08 |
| Edge skew | 9 × (4½ − 1½) × 3 | not read |
| Featheredge | 9 × 4½ × (3 − ⅛) | not read |
| Neck | 9 × 4½ × (3 − ⅝) | not read |
| Jamb | 9 × 4½ × 3 (rounded edge in the drawing) | not read |
| No. 1 / 2 / 3 / 4 key | 9 × (4½ − 4 / 3½ / 3 / 2¼) × 3 | 1.13 / 1.07 / 1.00 / 0.90 |
| 2 in split | 9 × 4½ × 2 | not read |
| Split | 9 × 4½ × 1½ | 0.60 |
| Soap | 9 × 2¼ × 3 | 0.60 |
| Small 9 in straight | 9 × 3½ × 3 | 0.93 |

2½ in series:

| Shape | Size (in) | Brick equiv. |
|---|---|---|
| 48° side skew | 9 × (4½ − 2¼) × 2½ | 0.75 |
| 60° side skew | 9 × (4½ − 3 1/16) × 2½ | 0.84 |
| 48° end skew | (9 − 6¾) × 4½ × 2½ | 0.88 |
| 60° end skew | (9 − 7 9/16) × 4½ × 2½ | 0.92 |
| Edge skew | 9 × (4½ − 1½) × 2½ | 0.67 |
| Featheredge | 9 × 4½ × (2½ − ⅛) | 0.53 |
| Neck | 9 × 4½ × (2½ − ⅝) | 0.63 |
| Jamb | 9 × 4½ × 2½ | 0.89 |
| No. 1 / 2 / 3 / 4 key | 9 × (4½ − 4 / 3½ / 3 / 2¼) × 2½ | 0.94 / 0.89 / 0.83 / 0.75 |
| 2 in split | 9 × 4½ × 2 (the table prints 2½; its 0.80 equivalent fits 2 in) | 0.80 |
| Split | 9 × 4½ × 1¼ | 0.50 |
| Soap | 9 × 2¼ × 2½ | 0.50 |

The arch and wedge sizes in the same tables match `electric-and-thermal.md` §5.

**Derived check of the skew angles:** the sloped face rises the full thickness over the taper.
- 3 in series: atan(3 ÷ 2 11/16) = 48.1° and atan(3 ÷ 1¾) = 59.7°.
- 2½ in series: atan(2.5 ÷ 2¼) = 48.0° and atan(2.5 ÷ 1 7/16) = 60.1°.
- So the names give the face angle to the bed.

### 5.2 Which skew suits which arch

- The skew face lies on a radius, so its angle to horizontal is 90° − ½θ. HarbisonWalker: "The
  slope of the skewback must be designed to match the central angle of the arch" [S20]
  Verified.
- 60° skew → 60° central angle → 1.608 in/ft. 48° skew → θ ≈ 84° → 2.302 in/ft **(derived)**.
  That is why the guide lists 2.302 in/ft as a standard rise.
- Built-up skewbacks shown in the guide [S20] Verified:
  - 4½ in arch, 1½ in/ft: one 9 in 2 in split and one 9 in featheredge.
  - 4½ in arch, 2.302 in/ft: two 48° end skews, one 48° side skew and one soap.
  - 9 in arch, 2.302 in/ft: two 48° end skews, two 48° side skews and one soap.
- "Built-up skews satisfy the requirements of narrow spans, four feet or less"; one-piece
  skewbacks are stronger [S20] Verified.
- One-piece shapes named in the guide: 56-9 (9 in arch, 1½ in/ft), 60-4½, 60-9, 60-12, 60-13½
  (60° arches), 74-4½ and 74-9 (2 in/ft). Their dimensions are on drawings that could not be
  read reliably. Versions with cut-outs for steel: 60-9-A takes an angle with a shorter leg up
  to 4 in and up to ¾ in thick; 60-12-A, 6 in and 1 in; 60-13½-A, 8 in and 1⅛ in [S20]
  Verified (table text).
- Pitelka calls the skews he uses for a 2.3 in/ft arch "45-degree skew bricks" [S4] [S11]. By
  the geometry these are the 48° skews **(derived)**. For IFB, he cuts skews from straights on
  a saw jig [S11] Verified.

### 5.3 Other listings

- Sheffield Pottery (retailer), 3 in series: end skew (9 − 6 9/16) × 4½ × 3; No. 1 side skew
  9 × (4½ − 2 11/16) × 3; No. 2 side skew 9 × (4½ − 1 13/16) × 3. Also sells a hard-brick
  "Side Skew 48 Deg" [S22] Verified.
  - **Conflict:** the No. 2 side skew matches the HarbisonWalker 48° side skew. The No. 1 side
    skew (about 58.9° **derived**) and the end skew (about 50.9° **derived**) do not match
    HarbisonWalker's 60° and 48° shapes.
- ISO 5019-5:1984 gives skewback dimensions for 64 mm and 76 mm course heights [S23] Excerpt.
  Its table was not read. ASTM C909 and C861 tables: still not read.

---

## 6. Doors and cars

### 6.1 Brick-up (stacked) door

| Item | Value | Mark | Source |
|---|---|---|---|
| Thickness (Pitelka) | 9 in, loose-stacked, no mortar between the bricks | Verified | [S4] |
| Bond (Pitelka) | lay inner and outer courses together, staggered; a header course about two-thirds of the way up ties the two layers | Verified | [S4] |
| Top of the door (Pitelka) | custom pieces fill the space under the arch, easiest cut from IFB; store them in order on top of the arch. Do not make them tight | Verified | [S4] |
| Gap seal (Pitelka) | seal larger cracks on the outer face with 4 parts slurry or cheap fireclay to 6 parts sand, by volume; some add sawdust to make it crumble off | Verified | [S4] |
| Arch interface (Pitelka) | if the arch spans only the inside depth, the stacked door overlaps the front of the arch at the top | Verified | [S11] |
| Cooling (Pitelka) | below red heat, a few top bricks can come out to speed cooling | Verified | [S4] |
| Mortar (Norsker) | same insulating value as the walls; refractory mortar "which has a high proportion of sand" so the door breaks up easily | Verified | [S14] |
| Small kiln (Berggren) | rebuilt every firing: inner IFB on edge plus outer hard brick laid flat, 7 in total; the layers lap the inner and outer wall faces at the corners | Verified | [S7] |
| Brick type | either; Pitelka uses IFB for the custom pieces | Verified | [S4] |

### 6.2 Hinged (swing) door

All from Pitelka's hinged IFB door handout [S13] unless marked. Verified.

| Part | Value |
|---|---|
| Door frame | ¼ × 4 × 4 in angle, mitred at 45° and welded like a picture frame. Use 4 in angle at any kiln size, because the 4 in leg is needed to hold the IFB |
| Lining | one 4½ in layer of IFB, no mortar. Optional 1 in ceramic fibre board outside it, covered by 18-gauge sheet metal |
| Overlap | the brick lining extends about 4 in beyond the door opening on all sides, including 4 in above the arch peak. The kiln face must be flat |
| Brick clamp | ½ in nuts welded over ½ in holes along the hinge-side angle, starting 4 in from top and bottom, then every 6–8 in. Leave a ⅜ in gap beside the bricks; a ¼ × 3 in flat bar in the gap is pressed against the bricks by 1½ in long ½ in bolts |
| Hinges | pins: two 10 in lengths of ¾ in steel shaft, bevelled at the top, on brackets welded to the kiln frame. Pin centre about 2½ in out from the brick face; pin stands 5 in above its bracket, with a ¾ in washer welded underneath. Door side: 4 in lengths of ¾ in black iron pipe, with ¼ in flat bar (¾ in hole) above and below |
| Latch | two eccentric latches opposite the hinges. 2 × 2 in tabs of ¼ in plate on the door frame. A ¾ in shaft runs in ¾ in black iron pipe on the kiln frame; on its end a 2 in disc (¼ in thick, preferably ½ in) welded ¼ in off-centre; a 10 in lever of ¼ × 1 in flat bar |
| Seal | as the door ages, cement on ceramic fibre webbing; "regular ceramic fiber blanket should not be used" |
| Material | "a hinged door should never be built from hardbrick" |
| Spy holes | bored through the finished IFB door; see §2 |

Kiln frame for a hinged door: ¼ × 3 × 3 in angle (≤ 24 ft³) or ¼ × 4 × 4 in (larger), with
angle across the top [S11] Verified. Pitelka adds an angle vertical beside the door opening
on his soda kiln because "the stub-wall will often warp or lean outwards" without it [S4]
Verified. Geil's downdraft hinges the whole front wall as a "full width door" [S10] Verified.

Brick-up against swing door: see `combustion-and-masonry.md` §7 (Ray Brown). Pitelka prefers
stacked doors on salt and soda kilns because those kilns shift, and because opening a hinged
door pulls cold air in at the bottom [S4] Verified.

### 6.3 Car kilns

| Item | Value | Mark | Source |
|---|---|---|---|
| Track (forum) | two angle irons, apex up; car wheels grooved to run on them | (secondary) Excerpt | [S24] |
| Seal (forum) | car platform stepped to fit inside the bottom course of brick: "a decent seal" | (secondary) Excerpt | [S24] |
| Burners (forum) | "Easiest to do with two power burners coming in from the back"; lots of welding and steel, so a small car kiln may not be worth it | (secondary) Excerpt | [S24] |
| Hobby cart track | V-groove casters on 1½ in angle-iron track; heavy carts can punch through a wood floor | (secondary) Excerpt | [S25] |
| Seal principle (patent) | the car only needs a light-tight barrier against radiant heat reaching the wheeled trolley, not an airtight seal | Excerpt | [S26] |
| Flues (Pitelka) | a deep production car kiln (updraft) usually needs several flue ports, each with its own kiln-shelf damper | Verified | [S11] |
| Sand seal | see `combustion-and-masonry.md` §7: leaky, needs coarse sand | | |

- Car deck build-up (steel, layers, thickness), wheel diameter, rail size and gauge, and
  sand-seal trough or fibre-seal dimensions for a studio car kiln: **NOT FOUND**.

---

## 7. Gaps (not found)

- GACO MR-750 and MR-100 head diameter and length.
- Port size for power burners. Only Ward's "offset ½ to 1 in" label is sourced.
- Burner entry positions for a site-built updraft.
- Olsen's and Rhodes' own text on ports, spy holes, frames and doors (borrow-only scans; not
  readable here). Olsen's chimney/flue rule is known only through a forum quote.
- A rule linking chimney cross-section to exit flue area that the sources agree on (Olsen and
  Norsker conflict). A damper sizing rule.
- Wall thickness for a tall free-standing brick chimney beyond one 4½ in layer; foundation size.
- A table of frame steel (angle size, tie-rod size and spacing) against arch span. Only single
  builds are sourced.
- Arch thrust for T/S above 10 %, for arches carrying insulation on top, and for arches held
  against expansion. Steel section properties for checking the buttress members in bending.
  Thread stress areas for tie rods.
- Dimensions of the one-piece skewback shapes (56-9, 60-x, 74-x): on drawings, not read.
  ASTM C909 / C861 and ISO 5019-5 tables.
- Car kiln deck, wheel, rail and seal dimensions.
- Standard spy-hole size from a kiln maker (Geil, Bailey). Only builders' sizes are sourced.

---

## Sources

- [S1] M. Ward, "Converting Electric Kilns to Gas", *Clay Times*, May 2003, Ward Burner Systems. https://www.wardburner.com/converting-electric/
- [S2] Ward Burner Systems, *MB Series Power Burner Operating Instructions* (PDF, from Technical Downloads). https://www.dropbox.com/scl/fi/zbgklv5z1k2r9ebqdkvl4/MB_Operating_Instructions.pdf?rlkey=4n7wubvl0m7ncjjfxpao3lj44&st=243fk03r&dl=0 ; list at https://www.wardburner.com/technical-info/technical-downloads/
- [S3] Ward Burner Systems, Burner Placement. https://www.wardburner.com/technical-info/burner-placement/
- [S4] V. Pitelka, *Building a 20-Cubic-Foot Cross-Draft Soda Kiln*, 2019. http://www.vincepitelka.com/wp-content/uploads/2019/12/Building-a-Crossdraft-Soda-Kiln-1.pdf
- [S5] V. Pitelka, *LPG Burner System for a 20- to 30-Cubic Foot Crossdraft Kiln*, 2019. http://www.vincepitelka.com/wp-content/uploads/2019/12/Soda-Kiln-Burner-System.pdf
- [S6] B. Robinson, "Downdraft Kiln Conversion", *Ceramics Monthly*, Apr 2020. https://ceramicartsnetwork.org/ceramics-monthly/ceramics-monthly-article/Downdraft-Kiln-Conversion ; same text in CAN Daily, 2020-04-01: https://ceramicartsnetwork.org/daily/article/DIY-Downdraft-Kiln-How-to-Convert-an-Electric-Kiln-to-Gas
- [S7] M. W. Berggren, *Experimental Study in the Design of a Small Down-Draft Gas Fired Kiln*, thesis, Kansas State University, 1968. https://archive.org/details/experimentalstud00berg (full text: https://archive.org/download/experimentalstud00berg/experimentalstud00berg_djvu.txt)
- [S8] Ward Burner Systems, Venturi Burners. https://www.wardburner.com/burners/venturi-burners/
- [S9] Ransome Manufacturing, Catalog TB-3/99 (copy hosted by V. Pitelka). http://www.vincepitelka.com/wp-content/uploads/2025/07/Ransome-Burner-Catalog.pdf
- [S10] P. H. Geil, US Patent 4,531,910, "Down draft kiln", granted 1985-07-30. https://patents.google.com/patent/US4531910
- [S11] V. Pitelka, *Building a Sprung Arch*, Tennessee Tech University, Appalachian Center for Crafts, 2016. https://www.vincepitelka.com/wp-content/uploads/2016/03/Building-a-Sprung-Arch.pdf
- [S12] Ceramic Arts Daily forum, burner-port threads (search summary only; the thread holding each quote was not identified): https://community.ceramicartsdaily.org/topic/12814-kiln-conversion-updraft-downdraft-chimney/ ; https://community.ceramicartsdaily.org/topic/39130-venturi-burners-backburning/ ; https://community.ceramicartsdaily.org/topic/6282-reduction-s/ ; https://community.ceramicartsdaily.org/topic/14840-my-kiln-build/page/2/
- [S13] V. Pitelka, *Building a Hinged IFB Kiln Door*, Tennessee Tech University, Appalachian Center for Crafts, 2014. http://www.vincepitelka.com/wp-content/uploads/2016/03/Building-a-Hinged-IFB-Kiln-Door.pdf
- [S14] H. Norsker, *The Self-Reliant Potter: Refractories and Kilns*, GATE / F. Vieweg, Braunschweig, 1987 (ISBN 3528020318). Scan from the CD3WD set: https://archive.org/details/the-self-reliant-potter-refactories-and-kilns
- [S15] Ceramic Arts Daily forum, "Chimney Entrance Reduction" (quotes Olsen, *The Kiln Book*, 4th ed., p. 78). https://community.ceramicartsdaily.org/topic/17145-chimney-entrance-reduction/ (search summary; also [S37] in `combustion-and-masonry.md`)
- [S16] B. Merrill, "Tips and Tools: Flat-Top Kiln", *Ceramics Monthly*, Apr 2023. https://ceramicartsnetwork.org/ceramics-monthly/ceramics-monthly-article/tips-and-tools-flat-top-kiln
- [S17] S. Davis, "Durango Firebox Kiln", kazegama.com (undated; comments 2021–2024). https://kazegama.com/durango-woodfire-kiln/
- [S18] D. Cuzick, "How to Build a Soda Kiln", 2015-10-29. https://www.cuzickpottery.com/blog/2015/10/29/how-to-build-a-soda-kiln
- [S19] Ceramic Arts Daily forum, chimney and damper advice (search summary; the "9 in below, 4.5 in above" post is in a 2020 thread on a 12 ft³ downdraft, probably this one): https://community.ceramicartsdaily.org/topic/22724-stupid-questions-about-chimney/ ; 15 ft³ power-burner downdraft with 8 × 4½ in flue: thread not identified.
- [S20] Harbison-Walker Refractories, *Brick Installation Guide*, © 2008 (Arch Construction pp. 13–20; Brick Sizes and Shapes pp. 21–25; Skewback Shapes pp. 31–32). https://ssfbs.com/wp-content/uploads/2021/06/HW_Brick_Installation_Guide.pdf
- [S21] Ceramic Arts Daily forum, "Metal frame for sprung arch kiln" (403 to direct fetch; search summary). https://community.ceramicartsdaily.org/topic/15978-metal-frame-for-sprung-arch-kiln/ (also [S61] in `combustion-and-masonry.md`)
- [S22] Sheffield Pottery, Kiln Building Refractory Bricks. https://www.sheffield-pottery.com/collections/kiln-building-refractory-bricks
- [S23] ISO 5019-5:1984, *Refractory bricks — Dimensions — Part 5: Skewbacks* (abstract only). https://www.iso.org/standard/11041.html
- [S24] Ceramic Arts Daily forum, "Car kiln design" (search summary). https://community.ceramicartsdaily.org/topic/29242-car-kiln-design/
- [S25] WOODWEB, "Tracks for Kiln Loading Cart Wheels" (lumber-kiln carts; search summary). https://woodweb.com/knowledge_base/Tracks_for_Kiln_Loading_Cart_Wheels.html
- [S26] US Patent 4,315,737, "Base for a kiln car" (search summary). https://patents.justia.com/patent/4315737
- [S27] The Ceramic Shop, L&L peep hole plug, small diameter (search summary). https://www.theceramicshop.com/product/41297/peep-hole-plug-ll-small-dia/
