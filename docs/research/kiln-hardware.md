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
- PDFs were read as text with `pdftotext`. In the first pass drawings inside them (dimension
  call-outs on shape sketches) could not be seen. In the second pass the HarbisonWalker shape
  pages were rendered as images and the call-outs read off them (§5.4); values read that way
  are marked "Verified (drawing)".
- Most kiln-scale numbers come from single documented builds, chiefly Vince Pitelka's
  handouts (Tennessee Tech, Appalachian Center for Craft) [S4] [S5] [S11] [S13]. A single
  build shows what worked once. It is not a design rule. The tables say which kiln each
  number comes from.
- The arch method and skewback shapes come from HarbisonWalker's *Brick Installation Guide*
  (2008) [S20]. That is an industrial furnace manual. Its method is general, but its worked
  example is a 12 ft basic-brick roof, far larger than a studio kiln.
- Olsen's *The Kiln Book* and Rhodes' *Kilns* are on the Internet Archive, but only as
  borrow-only scans. Olsen is cited only where a forum quotes him. Rhodes can be searched
  through the Archive's full-text search, which returns short snippets (about a line each)
  around the search term. Rhodes quotes in this file are stitched from overlapping snippets
  and are marked Excerpt [S34]. The OCR garbles some fractions; where it does, that is said.
- Steel section properties come from the AISC Shapes Database v16.0 spreadsheet [S28], read
  row by row. Thread areas come from Fastenal's printed table and formula [S29].

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
| Burner set-back, floor port (Rohde, a kiln maker) | burners "placed exactly below the openings"; "Burner head and kiln bottom have to be approximately 2 cm apart" (0.79 in **derived**) | Rohde gas top-loading kilns, venturi burner unit under the floor, manual dated 05/2004. Port size not given | Verified | [S38] |
| Forum rule of thumb | "if your burner is 2.5" in diameter make the port 4.5"", that is 1 in all round | (secondary) | Excerpt | [S12] |
| Forum builds | ports about 4 × 4 in | (secondary) | Excerpt | [S12] |
| Exit flue against ports | exit flue area = total of all burner port areas (Ward) | already in `combustion-and-masonry.md` §4.1 | Verified there | |

**Derived checks:**
- Pitelka's kiln meets Ward's flue rule exactly. Ports: 3 × (4.5 × 5) = 67.5 in². Exit flue:
  9 × 7.5 = 67.5 in² [S4] [S5] **(derived)**.
- The two Ward rules (port = head + 1 in; tip ≥ ½ in back) and Pitelka's ½ in tip distance
  agree. Robinson's ½–¾ in is the same rule for a floor port. Rohde's maker figure of about
  2 cm (0.79 in) is the same order **(derived)**.
- Ward's "head + 1 in" applied to the MR-750's 2.5 in outside diameter (§1.2) gives 3.5 in,
  which is exactly Robinson's 3½ in floor hole for MR-750s [S1] [S30] [S6] **(derived)**.

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

GACO cast-iron venturis (one-piece, with flame retention):

| Model | Size | Inlet | Rating | Mark | Source |
|---|---|---|---|---|---|
| MR-750 | "overall length of this burner is 8""; "Outside diameter measures 2.5" and interior diameter measures 1.7"" | "1/2" IPT thread" | 77,400 BTU/h propane at 11 in w.c. (Axner); 72,000 (Ward) | Verified (retailer) | [S30] [S8] |
| MR-100 | "larger than the MR750" (Clay Planet); "slightly larger" (Ward). Length and head diameter: **NOT FOUND** | "1/2" male brass fitting" | 94,000 BTU/h propane at 11 in w.c. | Verified (retailer) | [S31] [S8] |

- Pitelka mounts the MR-100 with a 1½ in muffler clamp round its throat and gives its gas spud
  as ½ in male NPT [S5]. With Clay Planet's ½ in fitting, that is still the only size clue for
  the MR-100.
- The MR-750 figures are a retailer's (Axner names the maker only as "Other"), not GACO's own
  sheet. No GACO data sheet was found.
- **Conflict (ratings and orifices):** Axner rates the MR-750 at 77,400 BTU/h with a #50
  propane orifice; Ward gives 72,000 BTU/h. Clay Planet lists the MR-100 with #38 for
  low-pressure propane and #50 for high-pressure propane [S30] [S8] [S31]. Orifices belong to
  `combustion-and-masonry.md` §3; they are noted here only because they disagree.
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
| Updraft | flue port(s) in the arch, each with its own kiln-shelf damper on deep kilns (Pitelka) | Verified | [S11] |
| Updraft (Rhodes) | the flame passes under a "horizontal baffle, or floor, and passes upwards along the walls and out a flue hole at the top. By positioning the burners mostly toward the outside, an excessively hot bottom may ..." (snippet ends). No distances given | Excerpt | [S34] |

Bag walls (Pitelka): "always necessary in gas kilns with side-mounted burners" so the flames do
not hit the ware. Salt kiln: hard brick laid flat (4½ in). Soda: hard brick on edge (2½ in).
First course solid in front of the burners [S4].

### 1.4 Power-burner ports

- Port size for power burners: **NOT FOUND**. Ward's MB instructions give only the ½ to 1 in
  offset label and say that wrong port size or placement makes pilots "dance" and burns out
  thermocouples [S2]. Ward's power-burner page gives ratings (MB200 270,000 to MB700
  795,000 BTU/h) but no tube, nozzle or port sizes [S40].
- Bailey (a maker of forced-draft downdraft kilns): "the Bailey has only two burner ports",
  mounted "up off the floor", and every Bailey kiln has "built in burner port covers": at the
  end of the firing "the refractory covers track over the port area to prevent re-oxidation"
  [S36] Verified. No port size is given.

---

## 2. Spy holes

### 2.1 Size

| Source | Size | Notes | Mark |
|---|---|---|---|
| Pitelka, hinged IFB door [S13] | round, 1½ to 2 in across at the outer face, widening to about 2½ in square at the inside face | wider inside gives a broader view. 2 in hole cut in a sheet-metal door skin | Verified |
| Pitelka, soda kiln walls [S4] | 2½ in high × 2¼ in wide (a quarter brick) | all spy holes in the kiln | Verified |
| Berggren [S7] | about 2½ × 2 × 4½ in, cut in the IFB inner wall; the 2½ in side tapers to 2 in | the taper makes the plug loosen on the slightest pull and wedge tight when pushed in | Verified |
| Pitelka, salt or soda [S13] | one extra, larger port about midway up the door | for pulling draw rings | Verified |
| Bailey (maker) [S36] | size not given | "SPY PORTS LINED WITH DENSE REFRACTORY": spy ports "can get worn away and enlarge" from pulling plugs, so Bailey lines them with hard refractory. The ports sit in IFB walls 4½ in (Deluxe) or 6 in (Production) thick | Verified |
| Rhodes [S34] | not given ("a small spy hole") | the snippets found speak of a spy hole in the door and cone plaques "visible through a small spy hole" | Excerpt |

- A spy-hole size stated by a gas-kiln maker (Geil, Bailey, Olympic): still **NOT FOUND**.
  Olympic's gas-kiln manuals (2018 and 2024 PDFs on olympickilns.com) could not be fetched
  (HTTP 403). Geil's site did not resolve.

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
| Flue size (Rhodes) | "provide a flue large enough to accommodate any foreseeable need. A small gas kiln of 10 cubic feet will need a flue hole of about 40 square inches. This dimension is dependent on the number of burners and the height and pull of the stack" | Excerpt | [S34] |
| Same, per cubic foot | 40 ÷ 10 = **4.0 in²/ft³**, against Olsen's 2.5 and Norsker's 2.63 | Derived | |
| Chimney against flue (Rhodes) | "The cross section of the chimney should be at least equal to that of the flue" | Excerpt | [S34] |
| Horizontal pull (Rhodes) | "each foot of horizontal flue must be compensated for by 2 additional feet of chimney" | Excerpt | [S34] |
| Chimney size (Rhodes) | "dimension the chimney in multiples of bricks. Thus the outside might be 13½ x 13½ inches or 18 x 18 inches" (the OCR prints "13^ x 13|"). With a 4½ in wall that is 4½ × 4½ or 9 × 9 in inside; the snippet does not give the wall | Excerpt; inside size Derived | [S34] |

**Conflict (chimney against flue):** Norsker makes the flues slightly bigger than the
chimney. Olsen (as quoted) makes the chimney bigger than the restricted flue entry, and Rhodes
makes it "at least equal" to the flue. Of the measured kilns below, Pitelka's has the chimney
1.2 × the flue (fits Olsen and Rhodes) and Berggren's 0.90 × (fits Norsker). So two rules and
one kiln put the chimney at or above the flue area, one rule and one kiln below it. None gives
a ratio, so this is not settled.

**Conflict (horizontal pull):** Rhodes adds 2 ft of chimney per foot of horizontal flue. Olsen
and Ward add ⅓ ft (`combustion-and-masonry.md` §4.1) and Norsker 1/3.5. Rhodes' figure is six
times Olsen's. For a cross-draft, where the horizontal run is long, the rules give very
different chimneys.

**Conflict (flue area per ft³):** Rhodes' 4.0 in²/ft³ is about 1.5 × Olsen's 2.5 and
Norsker's 2.63. Rhodes ties it to burner count and stack, so it is not a fixed ratio.

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
| Olsen, updraft 5 × 5 × 6 ft outside (4th ed. p.174) | sprung arch | corners 3 × 3 × ¼ in angle; floor perimeter 4 × 4 × ¼; door frame 3 × 3 × ¼; skewback brace 2 × 2 × ¼. "Can be larger (stronger), but not smaller"; 3/16 in angle for smaller kilns | top and bottom ties 2 × 2 × ¼; floor joists 2 × 2 × ¼ | Verified | Olsen 4th ed. p.174 |
| Olsen, fast-fire wood kiln (4th ed. p.139, Fig. 5-36) | 4½ in IFB, featheredge skews | 2 × 2 × 3/16 in angle, bolted | | Verified | Olsen 4th ed. p.139 |
| Forum | | angle at each corner; angle or channel round the bottom; bracing halfway up; angle behind the skews | all-thread across the top, front and back, so it can be tightened | (secondary) Excerpt | [S21] |
| Rhodes, general guidance | sprung arch | "A steel angle iron is inserted just behind the skewback to hold it securely in place". "For small kilns, 2x2 inch angle iron is sufficient". "In large kilns, channel iron braces called buckstays are placed upright at the sides" | "Metal tie rods are used to hold the corner braces in place"; "... inch tie rods are suitable". The rod size is a fraction the OCR cannot read (one scan prints "^", the other "4"), so it is **not read** | Excerpt | [S34] |

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

Expansion allowance (Olsen, 4th ed. p.51–53, Verified): walls grow
1/16–3/32 in per foot; in a steel frame leave 1/16 in per foot of wall, a ¼ in fiber pad at the
brick ends, offset rather than straight through; an IFB kiln in a flexible frame needs no joints
under 4 ft. The 4th edition does not mention springs on the tie rods.

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

HarbisonWalker brick counts per course for studio spans [S20] Verified (read from the rendered
"Arch Combinations" tables, guide pp. 71–72). These are for a 4½ in arch of **3 in series**
arch brick (9 × 4½ × 3 in). The guide's arch tables are all 3 in series; none covers 2½ in
series brick (`electric-and-thermal.md` §5 has both). Pitelka's counts above do not match these;
which series he used is not stated in the parts read.

| Rise (in/ft) | Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|---|
| 2.302 | 3 ft 0 in | 6 29/32 in | 2 ft 2 29/32 in | – | 11 | 5 | – | 16 |
| 2.302 | 3 ft 6 in | 8 1/16 in | 2 ft 7 13/32 in | – | 9 | 9 | – | 18 |
| 2.302 | 4 ft 0 in | 9 7/32 in | 2 ft 11 7/8 in | – | 7 | 13 | – | 20 |
| 2.302 | 4 ft 6 in | 10 3/8 in | 3 ft 4 3/8 in | – | 5 | 17 | – | 22 |
| 1.608 | 3 ft 0 in | 4 13/16 in | 3 ft 0 in | – | 5 | 10 | – | 15 |
| 1.608 | 3 ft 6 in | 5 5/8 in | 3 ft 6 in | – | 3 | 14 | – | 17 |
| 1.608 | 4 ft 0 in | 6 7/16 in | 4 ft 0 in | – | 1 | 18 | – | 19 |
| 1.608 | 4 ft 6 in | 7 1/4 in | 4 ft 6 in | – | – | 19 | 2 | 21 |

- Check: at 3 ft and 2.302 in/ft the HarbisonWalker formulas give r = 0.74742 × 36 = 26.91 in
  (2 ft 2.91 in) and h = 3 × 2.302 = 6.906 in, matching the table **(derived)**.
- The guide also tables 1½ and 2 in/ft for this thickness, and 9 in to 18 in arches of 3 in
  wedge brick. Those were not transcribed.

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
- A ⅜-16 rod has a tensile stress area of 0.0775 in², a ½-13 rod 0.1419 in² (§4.7.3). At
  12,000 psi on the stress area, they carry 930 lb and 1,703 lb.
- Case C on ⅜ in rods: 676 ÷ 0.0775 = 8,720 psi. On ½ in rods: 4,760 psi. Case B on ⅜ in rods:
  1,960 psi.
- So for studio spans, arch thrust alone does not size the rods. The ½ in rods builders use
  [S7] [S17] are well above it. Stiffness, door loads and heat probably govern, but no source
  quantifies that.
- HarbisonWalker does not say whether its 12,000 psi applies to the gross or the threaded
  area. Using the thread stress area, as here, is the cautious reading.

Buttress bending check (derived). The buttress angle or channel runs along the top of each side
wall behind the skewbacks and is held at its ends by the corner posts and tie rods. Treated as a
simple beam of length L under a uniform load w = Hmax, the bending moment is M = wL²/8 and the
section modulus needed is S = M ÷ 12,000 psi. M = wL²/8 at the centre of a simple beam under a
uniformly distributed load is AWC's Figure 1 [S41] Verified (drawing). Section moduli from §4.7.1. L = 54 in (the 54 in deep
arch of cases B to D, posts at its ends).

| Case | Hmax | w | M | S needed | Shapes in §4.7.1 that pass |
|---|---|---|---|---|---|
| B: IFB, 54 in span, 2.302 | 67.8 lb/ft | 5.65 lb/in | 2,060 lb·in | 0.172 in³ | all, from L2×2×3/16 (0.188) up |
| C: dense, 54 in span, 2.302 | 300.6 lb/ft | 25.05 lb/in | 9,130 lb·in | 0.761 in³ | L3×3×⅜ (0.825), L4×4×¼ (1.03), C6×8.2 only if bent about its strong axis (4.35). Not L3×3×¼ (0.569), not C6×8.2 web-vertical (Sy 0.488) |
| D: IFB, 54 in span, 1.608 | 132.7 lb/ft | 11.06 lb/in | 4,030 lb·in | 0.336 in³ | from L3×3×3/16 (0.433) up. Not L2×2×¼ (0.244) |

- A channel set with its web against the skews and its legs pointing outward (Pitelka's "legs
  outward" [S11]) takes the horizontal thrust across its web, which bends it about its weak
  (y) axis **(derived from the section geometry)**.
- The angle values use the geometric-axis S (bending parallel to a leg). An angle free to twist
  bends about its principal axes, and Sz is smaller (L3×3×¼: 0.415 against 0.569). Which applies
  depends on how the brickwork restrains the angle. No source here says.
- The check ignores the wall's own resistance and the load from insulation on the arch (§4.6).
- Pitelka's soda kiln buttresses a 36 in span, 4½ in hard-brick arch at 2.3 in/ft with
  L2×2×¼ [S4]. Its cold thrust is H = 0.62 × (1.17 × 142 × 3 × 0.375) = 116 lb/ft, or
  9.66 lb/in. On this model an L2×2×¼ (S 0.244 in³) reaches 12,000 psi at a span of
  √(8 × 12,000 × 0.244 ÷ 9.66) = 49 in between supports, before any heated factor
  **(derived)**. Its T/S (12.5 %) is outside the Hmax table, so the heated case cannot be
  checked. Treat the model as a cautious first check, not a sourced design rule.

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
- Section properties for the buttress members are now in §4.7. What is still missing is a
  sourced bending rule for single angles (AISC 360 §F10, lateral-torsional and leg buckling)
  and an allowable bending stress for steel that runs hot. **NOT FOUND.** The only sourced
  limit is HarbisonWalker's 12,000 psi tensile stress for hot bindings [S20].

### 4.7 Steel data for checking the frame

#### 4.7.1 Section properties (AISC Shapes Database v16.0)

All values read from the database rows [S28] Verified. US units: W lb/ft, A in², lengths in,
I in⁴, S in³. AISC's angle axes: x and y are the geometric axes parallel to the legs (equal for
an equal-leg angle); z is the minor principal axis, and Sz is its smallest elastic modulus (the
database's SzB). For channels, x is the strong axis (parallel to the flanges) and y the weak
axis. x̄ is the database's x, the distance to the centroid from the member's "designated edge"
(defined in AISC Manual Part 1, which was not read). The values fit the back of the leg (angles)
and the back of the web (channels): by hand, an L2×2×¼ has its centroid 0.59 in from the back
of a leg, against 0.586 listed **(derived)**.

Equal-leg angles:

| Shape | W | A | t | x̄ = ȳ | Ix = Iy | Sx = Sy | rx = ry | Iz | Sz | rz |
|---|---|---|---|---|---|---|---|---|---|---|
| L2×2×3/16 | 2.44 | 0.722 | 0.188 | 0.561 | 0.271 | 0.188 | 0.612 | 0.109 | 0.137 | 0.389 |
| L2×2×¼ | 3.19 | 0.944 | 0.250 | 0.586 | 0.346 | 0.244 | 0.605 | 0.142 | 0.171 | 0.387 |
| L2×2×⅜ | 4.70 | 1.37 | 0.375 | 0.632 | 0.476 | 0.348 | 0.591 | 0.203 | 0.227 | 0.386 |
| L2½×2½×¼ | 4.10 | 1.19 | 0.250 | 0.711 | 0.692 | 0.387 | 0.764 | 0.276 | 0.273 | 0.482 |
| L3×3×3/16 | 3.71 | 1.09 | 0.188 | 0.812 | 0.948 | 0.433 | 0.933 | 0.373 | 0.324 | 0.586 |
| L3×3×¼ | 4.90 | 1.44 | 0.250 | 0.836 | 1.23 | 0.569 | 0.926 | 0.490 | 0.415 | 0.585 |
| L3×3×5/16 | 6.10 | 1.78 | 0.313 | 0.860 | 1.50 | 0.699 | 0.918 | 0.606 | 0.497 | 0.583 |
| L3×3×⅜ | 7.20 | 2.11 | 0.375 | 0.884 | 1.75 | 0.825 | 0.910 | 0.716 | 0.573 | 0.581 |
| L4×4×¼ | 6.60 | 1.93 | 0.250 | 1.08 | 3.00 | 1.03 | 1.25 | 1.19 | 0.778 | 0.783 |
| L4×4×5/16 | 8.20 | 2.40 | 0.313 | 1.11 | 3.67 | 1.27 | 1.24 | 1.46 | 0.930 | 0.781 |
| L4×4×⅜ | 9.80 | 2.86 | 0.375 | 1.13 | 4.32 | 1.50 | 1.23 | 1.73 | 1.08 | 0.779 |

Channels (d = depth, bf = flange width, tw = web, tf = mean flange thickness):

| Shape | W | A | d | bf | tw | tf | x̄ | Ix | Sx | rx | Iy | Sy | ry |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| C3×4.1 | 4.1 | 1.20 | 3 | 1.41 | 0.170 | 0.273 | 0.437 | 1.65 | 1.10 | 1.18 | 0.191 | 0.196 | 0.398 |
| C4×5.4 | 5.4 | 1.58 | 4 | 1.58 | 0.184 | 0.296 | 0.457 | 3.85 | 1.92 | 1.56 | 0.312 | 0.277 | 0.444 |
| C5×6.7 | 6.7 | 1.97 | 5 | 1.75 | 0.190 | 0.320 | 0.484 | 7.48 | 2.99 | 1.95 | 0.470 | 0.372 | 0.489 |
| C6×8.2 | 8.2 | 2.39 | 6 | 1.92 | 0.200 | 0.343 | 0.512 | 13.1 | 4.35 | 2.34 | 0.687 | 0.488 | 0.536 |
| C6×10.5 | 10.5 | 3.07 | 6 | 2.03 | 0.314 | 0.343 | 0.500 | 15.1 | 5.04 | 2.22 | 0.860 | 0.561 | 0.529 |
| C6×13 | 13 | 3.82 | 6 | 2.16 | 0.437 | 0.343 | 0.514 | 17.3 | 5.78 | 2.13 | 1.05 | 0.638 | 0.524 |
| MC6×12 | 12 | 3.53 | 6 | 2.50 | 0.310 | 0.375 | 0.704 | 18.7 | 6.24 | 2.30 | 1.85 | 1.03 | 0.724 |
| C8×11.5 | 11.5 | 3.37 | 8 | 2.26 | 0.220 | 0.390 | 0.572 | 32.5 | 8.14 | 3.11 | 1.31 | 0.775 | 0.623 |

- Pitelka's "2 × 6 in channel" [S11] is not a named AISC size. The lightest 6 in channel,
  C6×8.2, has a 1.92 in flange, which is probably what he means **(derived; not confirmed)**.
- The spreadsheet also holds plastic moduli (Zx, Zy), torsion constants (J, Cw) and the
  angle's principal-axis distances, for a fuller check.

#### 4.7.2 Flat bar (derived)

AISC does not list flat bar. Rectangle formulas: A = bt, I = tb³/12 and S = tb²/6 about the
strong axis (load in the plane of the bar), I = bt³/12 and S = bt²/6 about the weak axis.
Weight from steel at 490 lb/ft³ [S39] (W = A × 490/144). Check of that density against AISC
weights: L3×3×¼ gives 1.44 × 490/144 = 4.90 lb/ft, the same as the database; L2×2×¼ gives
3.21 against 3.19 **(derived)**.

| Bar (t × b) | A (in²) | W (lb/ft) | I strong (in⁴) | S strong (in³) | I weak (in⁴) | S weak (in³) |
|---|---|---|---|---|---|---|
| ¼ × 1 | 0.250 | 0.85 | 0.0208 | 0.0417 | 0.00130 | 0.0104 |
| 3/16 × 2 | 0.375 | 1.28 | 0.125 | 0.125 | 0.00110 | 0.0117 |
| ¼ × 2 | 0.500 | 1.70 | 0.167 | 0.167 | 0.00260 | 0.0208 |
| ¼ × 3 | 0.750 | 2.55 | 0.563 | 0.375 | 0.00391 | 0.0313 |
| ¼ × 4 | 1.000 | 3.40 | 1.33 | 0.667 | 0.00521 | 0.0417 |

#### 4.7.3 Threaded rod (UNC)

Formulas printed by Fastenal [S29] Verified (D = nominal diameter, n = threads per inch):
- Tensile stress area = 0.7854 (D − 0.9743/n)²
- Thread root area = 0.7854 (D − 1.3/n)²

| Size | Threads/in | Tensile stress area (in²) | Root area (in²) | Gross area π D²/4 (in²) | Load at 12,000 psi on the stress area (lb) |
|---|---|---|---|---|---|
| ⅜ | 16 | 0.0775 | 0.0678 | 0.110 | 930 |
| ½ | 13 | 0.1419 (Fastenal 0.142) | 0.1257 (Fastenal 0.126) | 0.196 | 1,703 |
| ⅝ | 11 | 0.226 | 0.202 | 0.307 | 2,712 |
| ¾ | 10 | 0.334 (Fastenal 0.335) | 0.302 | 0.442 | 4,008 |

- Stress and root areas: Portland Bolt's thread chart [S32] Verified and Fastenal's table [S29]
  Verified agree to the third figure. The formulas reproduce both **(derived)**: for ½-13,
  0.7854 × (0.5 − 0.9743/13)² = 0.1419.
- Gross area and the 12,000 psi loads are **derived**.
- The formula is the one in ASME B1.1, but that standard was not read; the sources above print
  it without naming the standard.

#### 4.7.4 Material strengths

| Material | Yield, min | Tensile | Note | Mark | Source |
|---|---|---|---|---|---|
| ASTM A36 (bars) | 36 ksi | 58–80 ksi | elongation 20 % in 2 in, 23 % in 8 in. "Bolts manufactured from A36 steel include ASTM specifications A307 and F1554 Grade 36" | Verified | [S33] |
| ASTM A307 Grade A (bolts, threaded rod) | not specified | 60 ksi min | "Headed bolts, threaded rods and bent bolts intended for general applications"; ¼ to 4 in | Verified | [S33] [S29] |
| ASTM F1554 Grade 36 (anchor bolts, rod) | 36 ksi | 58–80 ksi | | Verified | [S29] |
| Furnace bindings (HarbisonWalker) | | 12,000 psi limit | "many furnace designers limit tensile stress to 12,000 pounds per square inch", because the binding may run hot | Verified | [S20] |

- 12,000 psi is one-third of A36's minimum yield and one-fifth of A307's minimum tensile
  strength **(derived)**.
- Portland Bolt's A36 table is "abridged" to bars. The A36 requirements for shapes (angle,
  channel) were not read here.
- The grade of unmarked threaded rod: no source here says. Check the rod against A307 Grade A
  only if it is sold as A307.
- AISC 360 allowable stresses (ASD safety factors for tension, bending and threaded parts): the
  specification is a free PDF from AISC, but aisc.org returned 403 and the Wayback copy 429, so
  it was not read. **NOT FOUND.**
- Strength of steel at elevated temperature: **NOT FOUND**. HarbisonWalker's 12,000 psi is the
  only sourced allowance for heat.

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
  (60° arches), 74-4½ (4½ in arch) and 74-9 (9 in arch), both 2 in/ft. Dimensions in §5.4.
- Versions with cut-outs for the supporting steel [S20] Verified (table text):

| Skewback | Steel angle: shorter leg, max | Angle thickness, max | Skewback | Channel size, max | Flange width, max | Web thickness, max |
|---|---|---|---|---|---|---|
| 60-9-A | 4 in | ¾ in | 60-9-C | 12 in | 3 13/32 in | ¾ in |
| 60-12-A | 6 in | 1 in | 60-12-C | 12 in | 3 13/32 in | ¾ in |
| 60-13½-A | 8 in | 1⅛ in | 60-13½-C | 15 in | 3 13/16 in | 13/16 in |

The -A and -C drawings (guide p. 32) were not transcribed.

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

### 5.4 One-piece skewback dimensions (HarbisonWalker drawings)

Read from the rendered shape drawings, guide p. 31 [S20] Verified (drawing). Each shape is a
block whose profile (the end view, across the wall) is a rectangle, bed × height, with the corner
on the arch side cut away by the sloped skew face. "Top" is the flat left on top behind the skew
face. "Toe" is the short vertical face left at the bottom of the skew face, on the arch side.
"Length" runs along the arch (into the drawing).

| Shape | For arch | Bed (in) | Height (in) | Top (in) | Toe (in) | Length along arch (in) | Fits the formulas? |
|---|---|---|---|---|---|---|---|
| 60-4½ | 4½ in, 1.608 in/ft (60°) | 4½ | 4½ | 2¼ | 19/32 | 9 | yes |
| 60-9 | 9 in, 60° | 9 | 9 | 4½ | 17/32 (as printed) | 4½ | no, see below |
| 60-12 | 12 in, 60° | 12 | 12 | 6 | 1 19/32 | 4½ | yes |
| 60-13½ | 13½ in, 60° | 13½ | 13½ | 6¾ | "1 13/18" as printed; 1 13/16 fits | 4½ | yes, reading 1 13/16 |
| 74-4½ | 4½ in, 2 in/ft (73° 44.4′) | 4½ | 4½ | 1 13/16 | 29/32 | 9 | yes |
| 74-9 | 9 in, 2 in/ft | 9 | 9 | 3 19/32 | 13/16 (as printed) | 4½ | no, see below |
| 56-9 | 9 in, 1½ in/ft (56° 8.7′) | 9 | 4¾ (as printed) | 4¾ | 11/16 | 4½ | no, see below |

Check against the guide's own formulas **(derived)**. Formulas 8 and 12 in §4.3 give the skew
face's horizontal run H = T sin ½θ and vertical rise V = T cos ½θ. In every drawing the bed
equals the arch thickness T, and so does the height in all but the 56-9. So the top should be
T − H and the toe T − V.
- 60-4½, 60-12, 60-13½ and 74-4½ fit to within 1/64 in. Example, 60-12: H = 12 sin 30° = 6,
  so the top is 6 as printed; V = 10.39, so the toe is 12 − 10.39 = 1.61 against 1 19/32 (1.59)
  printed. Their skew faces come out at 60.0° to 60.1° (60-x) and 53.2° (74-4½) to the bed, as
  the arches need (90° − ½θ = 60° and 53.1°).
- 60-9: the top fits (H = 4.5), but the toe should be 9 − 7.79 = 1.21 in, not 17/32. The
  printed figures give a 62.0° face, not 60°. A dropped "1" (1 7/32 = 1.22) would fit, but
  that is a guess. The 60-9-A drawing on p. 32 prints the same 17/32.
- 74-9: the top fits (H = 5.4, top 3.6), but the toe should be 9 − 7.2 = 1.8 in, not 13/16.
  1 13/16 (1.81) would fit.
- 56-9: the top fits (H = 4.24, top 4.77), but with the printed 11/16 toe the height should be
  7.94 + 0.69 = 8.63 in, not 4¾. The printed 4¾ repeats the top dimension.
- For the engine: compute skew profiles from T and θ with formulas 8 and 12 rather than copy
  these drawings. Use the drawings for the bed, length and the family of shapes, and flag the
  three that do not fit. Ask the maker before buying 60-9, 74-9 or 56-9 shapes.
- Which brick grades these shapes come in was not checked. No one-piece IFB skewback was
  found; Pitelka cuts IFB skews from straights on a saw [S11].

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
| Seal principle (patent) | "All that is required is a barrier against the penetration of radiant heat from the flue to the wheeled metal trolley, in other words to provide a light-tight seal." "It is not necessary to form an air tight seal." The car base is stacked ceramic pillars and bats on a wheeled metal trolley, with projecting bats forming the barrier and fibre, perlite or vermiculite fill. No dimensions | Verified | [S26] |
| Flues (Pitelka) | a deep production car kiln (updraft) usually needs several flue ports, each with its own kiln-shelf damper | Verified | [S11] |
| Sand seal | see `combustion-and-masonry.md` §7: leaky, needs coarse sand | | |

Studio car kilns with stated construction:

| Kiln | Car and deck | Wheels and track | Seal | Mark | Source |
|---|---|---|---|---|---|
| McDowell, Ferndale WA, 2003; designed by Pitelka; gas downdraft, sprung arch | welded steel car frame carrying "the loading bed and door". Bed: "a thin coat of mortar on top of the steel deck", two layers of IFB (soaked, laid in thin fireclay mortar), then a top layer of hard brick "for greater resistance to the heat, abrasion, and uneven weight distribution". The door is one layer of dry-stacked brick in a frame on the car, held by bolts pressing a flat bar; it is bolted, not welded, to the car frame so its position can be adjusted. A latch holds the car closed | "steel wheels and rails"; no sizes | "the brick overlap of the shell of the kiln match up with the layers of brick on the car. A slight wedge shape to the bed allows it to be removed, yet seal tightly when fully pushed in". A small gap was left between bed and door in the top hard-brick layer for expansion. Fit was tuned by sanding where a piece of posterboard would not pass | Verified | [S35] |
| Rhodes, small trackless car kiln | "a layer of asbestos cement board over the metal framework and two layers of insulating firebrick on top of that" | "wheels salvaged from an old saw mill carriage"; "The wheels of the car ride directly on the concrete floor. Two guides of strap iron are fastened to the floor to guide the car into place. Since there is no track, the car can be wheeled about in the studio" | "the opening where the car enters is a true rectangle" | Excerpt | [S34] |
| Rhodes, catenary-arch gas car kiln, Alfred | | | "concrete base in this case is built in a 'U' shape to admit the car. Steel channels are set into the structure to form a sand seal with a skirt on the car" | Excerpt | [S34] |
| Bailey shuttle kilns (maker; 12–31 ft³ Deluxe, 28–120 ft³ Production) | IFB 4½ in in walls, floor and arch (Deluxe); 6 in walls, 6¾ in arch (Production). On the front-loader page, for the same Deluxe and Production construction: "Stainless 'L' anchors (inset into top surface of brick) secure dry stacked brick into steel framework" | track, optionally folding up against the kiln front; or trackless carts with a "docking system", which "does require a uniform cement floor" | "a unique stainless steel spring-loaded channel (filled with refractory) makes a perfect airtight fit between the cart and interior framework" | Verified | [S36] |

Industrial tunnel-kiln car, for scale (JACerS 1922: a direct-fired tunnel kiln about 4 ft 6½ in
wide, the OCR printing "4 ft. 614 in."; the ware on each car occupies 5 ft 9 in of length)
[S37] Verified (OCR):
- Car frame "a single gray iron casting with a gridded top", "two double-flanged wheels and two
  flat-faced wheels—both kinds being 12 inches in diameter", each on its own axle with caged
  roller bearings.
- Skirt: "a depending steel plate, 3/16 inch thick, which runs in the sand-seal trough on each
  side". The fraction is garbled in all three scans ("*/i5", "3/u", "3/ir"); 3/16 is the reading
  that fits.
- Trough: "the outer confining wall of which is a 1/4 in. by 8 in. steel plate, extending the full
  length of the kiln".
- Deck: "a No. 14 gauge steel plate, which supports a 2½ in. layer of Sil-O-Cel (pulverized
  kieselguhr) and Portland cement (4:1 by volume)", then "specially shaped fire-clay slabs, 9 in.
  thick". The "2½" is garbled in all three scans ("21%", "2)/2", "2^2"); 2½ fits all three.
- "Longitudinal slots are provided in the side walls, in which the car platform fits rather
  loosely", to intercept radiant heat before it reaches the car frames and sand seals.
- This is a continuous kiln moving 1.2 in per minute, not a studio car. Its numbers show the
  proportions of a working sand seal; they are not a studio design.

Still **NOT FOUND** for a studio car kiln: wheel diameter, rail size and gauge, deck steel size,
sand-trough width and depth, skirt depth, and fibre-seal dimensions.

---

## 7. Gaps (not found)

Burners and ports:
- GACO's own data sheet for the MR-750 and MR-100. The MR-750's size is a retailer's (§1.2).
  MR-100 length and head diameter: not found anywhere.
- Port size for power burners. Only Ward's "offset ½ to 1 in" label is sourced; Ward's and
  Bailey's pages give no port size.
- Burner positions for a site-built updraft as distances. Rhodes says only "mostly toward the
  outside".

Spy holes:
- A spy-hole size stated by a gas-kiln maker (Geil, Bailey, Olympic). Bailey says only that its
  ports are lined with dense refractory. Olympic's gas manuals returned HTTP 403.

Flue, chimney and damper:
- A chimney-to-flue area ratio. Olsen, Rhodes and Pitelka's kiln put the chimney at or above the
  flue; Norsker and Berggren's kiln put it below. No source gives a ratio.
- Agreement on how much chimney a horizontal run needs: Rhodes 2 ft per ft, Olsen and Ward ⅓,
  Norsker 1/3.5 (§3.1).
- A damper sizing rule.
- Wall thickness for a tall free-standing brick chimney beyond one 4½ in layer; foundation size.

Steel frame:
- A table of frame steel (angle size, tie-rod size and spacing) against arch span. Only single
  builds and Rhodes' "2x2 inch angle iron is sufficient" for small kilns are sourced. Rhodes'
  tie-rod size is an unreadable fraction in the OCR.
- AISC 360 allowable stresses (ASD factors for tension, bending, threaded parts) and the
  single-angle bending rules (§F10). The specification could not be downloaded (403 from
  aisc.org, 429 from the Wayback Machine).
- Allowable stress for steel running hot, other than HarbisonWalker's 12,000 psi practice limit.
  Whether that limit is meant for the gross or the threaded area of a rod.
- ASTM A36 requirements for shapes (only the bar table was read).
- ASME B1.1 itself (its stress-area formula is sourced through Fastenal).

Arch:
- Arch thrust for T/S above 10 %, for arches carrying insulation on top, and for arches held
  against expansion.
- Brick counts per course for 2½ in series arch brick (HarbisonWalker tables 3 in series only).
- Corrected dimensions for the 60-9, 74-9 and 56-9 skewbacks, whose drawings do not fit the
  guide's own formulas (§5.4). ASTM C909 / C861 and ISO 5019-5 tables.

Car kilns:
- For a studio car kiln: wheel diameter, rail size and gauge, deck steel size, sand-trough width
  and depth, skirt depth, fibre-seal dimensions. The deck build-up is sourced only in layers, not
  thicknesses (§6.3). The only numbers are from a 1922 industrial tunnel kiln.

Books:
- Olsen's *The Kiln Book* text (borrow-only; his rules are known only through forum quotes).
  Rhodes' *Kilns* is known only through full-text-search snippets, not page images.

---

## Corroboration (2026-10-24)

Goal: at least three independent sources per fact. Resellers or calculator sites that copy one
table count as one source. Values were not changed; disagreements are listed.

Engine-facing items (`core/src/kilndesigner/frame.py`, `data/steel.yaml`, `hardware.py`):

| Item | Sources now | Agreement | Notes |
|---|---|---|---|
| AISC angle/channel properties (§4.7.1, `steel.yaml`) | 3: [S28]; beamdimensions.com AISC 360-16 entry [S42] (L3×3×¼: A 1.44, I 1.23, x̄ 0.84); hand calc from geometry (§4.7.1, L2×2×¼ x̄) | agrees | [S42] is a re-host of AISC data, so only partly independent. Engineers Edge angle table [S43] could not be fetched (HTTP 526). Sx 0.569 checks as I/c = 1.23 ÷ 2.164 **(derived)** |
| UNC tensile stress areas (§4.7.3, `steel.yaml`) | ⅜-16, ½-13: 4 ([S29] [S32] [S44] [S45]); ⅝-11, ¾-10: 2 tables + formula | agrees to 4 figures where read | **⅝-11 and ¾-10: only 2 tables found** (Fastenal, Portland Bolt) plus the formula. ASME B1.1 still not read |
| A307 Grade A 60 ksi min tensile (§4.7.4) | 3: [S33] [S29]; ASTM A307 abstract via ANSI/GlobalSpec [S46]; Lawson Products rod listing [S47] (reseller) | agrees | |
| A36 36 ksi yield, 58–80 ksi tensile | 58–80 ksi: 3 ([S33] [S29] [S46], A307 Grade C cites A36 for it). 36 ksi yield: **only 2** ([S33] [S29]) | agrees | ASTM A36 itself not read |
| 12,000 psi hot-binding stress limit (`steel.yaml` `binding_stress`) | **only 1 source** [S20] | — | No second furnace text found by search. Ask the user whether Olsen gives a steel stress (ask the user for Olsen p.__) |
| Arch geometry formulas 1–13 (§4.3, `frame.py`) | 3: [S20]; chord–sagitta geometry (derivation, §4.4 checks); Pitelka's worked arches [S4] [S11] reproduce r and h | agrees within 1/16 in | Geometry is exact; independent of any one book |
| Middle-third rule for line of thrust | 2: [S20]; McDowell via AIME paper [S48] | agrees | **only 2 sources** |
| W, H, F constants and heated Hmax table (§4.3, `frame.py` thrust) | **only 1 source** [S20] (F = √(H²+(W/2)²) is checkable by statics) | — | Engine thrust rests on one manufacturer table. Ask the user for Olsen's arch-thrust treatment (Olsen p.__) |
| M = wL²/8 (§4.5 buttress check) | 3: [S41]; textbook statics (any); AISC Manual Table 3-23 (not read) — count 2 read | agrees | **only 2 read** |
| Steel 490 lb/ft³ | 2: [S39]; AISC weights reproduce it (§4.7.2) | agrees | only 2 |
| Frame members: angle 2×2 to 4×4, ½ in rods (frame.py PITELKA, ½ in minimum) | 4 builds/books: [S4] [S11] [S7] [S17] [S34] (Rhodes 2×2 for small kilns); forum [S21] | broadly agree (2×2 small, 3×3 general, 4×4 hinged door) | No span-based rule anywhere; builds only. Merrill's ⅜ in rods [S16] are below the engine's ½ in minimum (flat top, not arch) |
| Rise 1.608–3 in/ft, Pitelka ≥ 2 in/ft | 4: [S20] [S14] [S11] [S18] | agree in range | Cuzick 1½ in/ft and HW fireclay 1½ sit below Pitelka's 2 |
| Brick-up door 9 in (hardware.py §6.1) | 2: [S4], Berggren 7 in [S7] | **disagree: 9 in vs 7 in** | only 2 |
| Hinged door ¼×4×4 angle, ¾ in pin (hardware.py §6.2) | **only 1** [S13] | — | Electric-kiln ¾ in hinge rod (other file) is a different context |
| Car rails/wheels (hardware.py §6.3) | forum [S24] [S25] secondary; McDowell [S35] no sizes | no numbers | still NOT FOUND |
| Port = burner + 1 in; set-back ½ in (hardware.py §1.1) | 4: [S1] [S5] [S6] [S12]; Rohde 0.79 in [S38] | agree | Ward and the forum may not be independent |
| Chimney inside ≥ flue; 4½ in mortared hard brick (hardware.py §3.2) | chimney/flue: 3 ([S15] Olsen, [S34], [S14]) | **disagree**: Norsker flue > chimney; Olsen/Rhodes chimney ≥ flue; Pitelka 1.20, Berggren 0.90 | unresolved; ask the user for Olsen 4th ed. p. 78 directly |
| Horizontal pull: extra chimney per ft of run | 3 (Rhodes, Olsen/Ward, Norsker) | **disagree**: 2 ft vs ⅓ ft vs 1/3.5 ft (6×) | |
| Flue area per ft³ | 3 (Olsen 2.5, Norsker 2.63, Rhodes 4.0 in²/ft³) | **disagree**: Rhodes 1.5× | |
| Spy hole 1½–2½ in (hardware.py §2) | 3: [S13] [S4] [S7] | agree in range | no maker figure |

Searches that found nothing new: arch-thrust texts beyond HarbisonWalker; a 12,000 psi or other
hot-steel allowable; frame steel sized by span; studio car-kiln rail and wheel sizes.

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
- [S20] Harbison-Walker Refractories, *Brick Installation Guide*, © 2008 (Arch Construction pp. 13–20; Brick Sizes and Shapes pp. 21–25; Skewback Shapes pp. 31–32; Arch Combinations pp. 71 ff.). https://ssfbs.com/wp-content/uploads/2021/06/HW_Brick_Installation_Guide.pdf . In the second pass, printed pp. 31, 32, 71 and 72 (PDF pages 34, 35, 74, 75) were rendered to images and read. Local copy: `scratch/research/gas/hw-guide/HW_Brick_Installation_Guide.pdf`.
- [S21] Ceramic Arts Daily forum, "Metal frame for sprung arch kiln" (403 to direct fetch; search summary). https://community.ceramicartsdaily.org/topic/15978-metal-frame-for-sprung-arch-kiln/ (also [S61] in `combustion-and-masonry.md`)
- [S22] Sheffield Pottery, Kiln Building Refractory Bricks. https://www.sheffield-pottery.com/collections/kiln-building-refractory-bricks
- [S23] ISO 5019-5:1984, *Refractory bricks — Dimensions — Part 5: Skewbacks* (abstract only). https://www.iso.org/standard/11041.html
- [S24] Ceramic Arts Daily forum, "Car kiln design" (search summary). https://community.ceramicartsdaily.org/topic/29242-car-kiln-design/
- [S25] WOODWEB, "Tracks for Kiln Loading Cart Wheels" (lumber-kiln carts; search summary). https://woodweb.com/knowledge_base/Tracks_for_Kiln_Loading_Cart_Wheels.html
- [S26] J. Elliott, M. G. Bell, W. J. Lovatt (Acme Marls Ltd), US Patent 4,315,737, "Base for a kiln car", granted 1982-02-16. Read on Google Patents in the second pass: https://patents.google.com/patent/US4315737A/en ; also https://patents.justia.com/patent/4315737
- [S27] The Ceramic Shop, L&L peep hole plug, small diameter (search summary). https://www.theceramicshop.com/product/41297/peep-hole-plug-ll-small-dia/
- [S28] American Institute of Steel Construction, *AISC Shapes Database v16.0* (Excel, August 2023; consistent with the *Steel Construction Manual*, 16th ed.). https://cloud.aisc.org/biggie_bin/aisc-shapes-database-v160-2.xlsx (linked from AISC's "AISC Shapes Database v16.0" page). Local copy: `scratch/research/gas/aisc-shapes/aisc-shapes-database-v160-2.xlsx` (the 5 KB `aisc-shapes-database-v16.0.xlsx` beside it is a saved Cloudflare page, not data).
- [S29] Fastenal, *Mechanical Properties of Inch Fasteners* (Rev. 8-25-09; tables of externally threaded fastener strengths and of tensile stress, thread root and stripping areas, with formulas). https://crafter.fastenal.com/static-assets/pdfs/Mechanical_Properties_of_Inch_Fasteners.pdf
- [S30] Axner Pottery Supply, "MR-750 Venturi Burner" (product page). https://www.axner.com/mr-750venturiburner.aspx
- [S31] Clay Planet, "MR-100 Venturi GACO Gas Kiln Burner" (product page; marked sold out). https://shop.clay-planet.com/mr-100-venturi-burner.aspx
- [S32] Portland Bolt & Manufacturing, Thread Pitch Chart (UNC basic pitch diameter, minor-diameter area, tensile stress area). https://www.portlandbolt.com/technical/thread-pitch-chart/
- [S33] Portland Bolt & Manufacturing, ASTM A36 and ASTM A307 specification pages. https://www.portlandbolt.com/technical/specifications/astm-a36/ ; https://www.portlandbolt.com/technical/specifications/astm-a307/
- [S34] D. Rhodes, *Kilns: Design, Construction, and Operation*, Chilton Book Co., Philadelphia, 1968. Borrow-only scans; read through Internet Archive full-text search snippets (`https://archive.org/services/search/beta/page_production/?service_backend=fts&user_query=identifier:<id> AND <term>`). https://archive.org/details/kilnsdesignconst0000rhod ; https://archive.org/details/kilnsdesignconst00rhod
- [S35] M. McDowell, "Building my New Kiln" and "Building my New Kiln, Page 2", McDowell Pottery (build of a Pitelka-designed gas car kiln, 2003). http://www.mcdowellpottery.com/NewKiln.htm ; http://www.mcdowellpottery.com/NewKiln2.htm
- [S36] Bailey Pottery Equipment, "Studio Deluxe and PRO Shuttles", "Studio Deluxe and PRO Front Loaders" and "Burner Design and Safety Systems" pages. https://baileypottery.com/studio-deluxe-and-pro-shuttles ; https://baileypottery.com/studio-deluxe-and-pro-front-loaders ; https://baileypottery.com/burner-design-safety-systems
- [S37] "Preliminary Report of the Committee on Fuel Conservation on the Railroad Tunnel Kiln", *Journal of the American Ceramic Society* 5 (1922), pp. 602 ff.; the car and sand seal on pp. 605–606. Full text: https://archive.org/details/journalofameri05amer1918 (the identifier says 1918; the volume is 5, 1922). Cross-checked in https://archive.org/details/journalofamerica05amer_0 and https://archive.org/details/journala05amer
- [S38] Rohde, *Instruction Manual: Gas – Top loading Kilns* (05/2004), hosted by Bath Potters' Supplies. https://www.bathpotters.co.uk/userfiles/file/top-loading-gas-manual.pdf
- [S39] Iowa Department of Transportation, Materials IM 569, "Computing Structural Steel Weight" (revised 2015-10-20): "Steel: 490 lb./ft.³". https://ia.iowadot.gov/erl/current/IM/content/569.htm
- [S40] Ward Burner Systems, Power Burners. https://www.wardburner.com/burners/power-burners/
- [S41] American Wood Council / AF&PA, *Beam Design Formulas with Shear and Moment Diagrams*, Design Aid No. 6 (2005 NDS edition, © 2007), Figure 1 "Simple Beam – Uniformly Distributed Load" (formulas printed as images; read from the rendered page). https://awc.org/wp-content/uploads/2021/12/AWC-DA6-BeamFormulas-0710.pdf
- [S42] beamdimensions.com, L3x3x1/4 (AISC equal angles; re-host of AISC data, search summary). https://beamdimensions.com/database/American/AISC/Equal_angles/L3x3x1/4
- [S43] Engineers Edge, ASTM A36 steel angle section properties (HTTP 526, not read). https://ns1.engineersedge.com/standard_material/Steel_angle_properties.htm
- [S44] Engineers Edge, ANSI inch thread stress area table (search summary: ⅜-16 0.0775, ½-13 0.1419). https://engineersedge.com/hardware/ansi_inch_size_thread_stress_15800.htm
- [S45] eFunda, UNC thread table (search summary: ⅜-16 0.0775). https://www.efunda.com/designstandards/screws/screw8un.cfm
- [S46] ASTM A307 abstracts (ANSI webstore / GlobalSpec; Grade A 60 ksi min; Grade C to A36, 58–80 ksi). https://webstore.ansi.org/standards/astm/astma30707 ; https://standards.globalspec.com/std/3814645/astm-a307-03
- [S47] Lawson Products, ASTM A307 Grade A threaded rod, 60,000 psi (reseller listing). https://www.lawsonproducts.com/products/threaded-rod-steel-1-4-20-x-36-1344412
- [S48] "Development of Bonded Basic Roofs for Open-Hearth Furnaces", AIME Transactions (OneMine), citing McDowell's arch stability conditions (middle third). https://onemine.org/documents/part-i-papers-development-of-bonded-basic-roofs-for-open-hearth-furnaces
