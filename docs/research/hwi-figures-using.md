# HarbisonWalker, *Handbook of Refractory Practice* (2005): the drawings of Using Refractories and the brick shapes

[HW05] Harbison-Walker Refractories Company, *Handbook of Refractory Practice*, © 2005 (the owner's
git-ignored copy, `docs/research/da86e4bd09a66be00c11a67957ff8e5a.pdf`, 331 pages). This is the
second reading of the drawn parts of Section 4 (UR-1 to UR-29, PDF pp.61–89) and of the shape pages
of Section 7 (IR-1 to IR-10, PDF pp.125–134). The first pass is `hwi-handbook.md`; it read the text
layer and the main tables. This note adds what the text layer drops: drawings, photographs, boxes.

Read on 2026-11-17. Each page below was rendered with PyMuPDF at 110–150 dpi and looked at, and each
drawing was zoomed at 300–500 dpi. PDF pp.65, 80, 83, 84 (drawings) and 88, 89 (formulas) were read
on the image; pp.69, 70, 75, 76, 78 (photographs) and pp.72, 73, 74, 77 (figures and boxes) at 110
dpi. A page scan for boxes and images (`page.get_drawings()`, `get_image_info()`) covered PDF
pp.61–89 and 125–136. The book is copyrighted: nothing here is a copy of a figure. Short quotes only.

Marks as in `hwi-handbook.md`: **Verified** (read on the image), **Read** (text layer only),
**Derived** (arithmetic here, shown), and "estimated from the drawing" where a position or a
proportion is judged by eye. Citations are by printed label with the PDF page once per item.

**Limit of this reading.** The UR-20 wall drawings (PDF 80) are one raster picture, about 513 × 635
pt on the page. At 300 dpi the individual bricks are visible but the courses cannot be followed
brick by brick. UR-20 is therefore recorded by its captions and by what the drawings visibly show,
not course by course. §2 says so again where it matters.

---

## 1. Joint construction for castables (UR-5, PDF 65)

The box "Typical Joint Construction" has four isometric drawings of a cut slab of castable (stippled
aggregate), the back face against a shell shown as a zigzag edge. No dimension is printed on any of
them. What is printed (Verified):

| Drawing (caption as printed) | What it shows | Anchor |
|---|---|---|
| "Thin Single Component Lining – 5" or Less" | One slab with one **straight, slanted joint** cut through the thickness at an angle (the cut runs from the hot face at an angle toward the cold face). Two blocks. | One wire anchor, drawn as a bent rod with a loop at the top, standing in the middle of the right-hand block, its tines spread, well clear of the joint |
| "Thick Single Component Lining – 5" or More" | The joint is **stepped** (a Z or key shape across the thickness: the cut runs in, steps sideways, then runs out). Three blocks are drawn. | One anchor in the middle of the right block, tines either side of its centre, clear of the joint |
| "Double Lining Hot Face or Backup – 5" or Less" | A hot-face layer and a thin backup slab on top of it (the cold side). The hot layer has the same **slanted** joint as the thin single lining. The backup has its own joint, at a **different place** (the drawing shows a short vertical joint in the backup that does not line up with the slanted one). | No anchor drawn |
| "Double Lining Hot Face or Backup – 5" or More" | The hot layer has the **stepped** joint. The backup layer on top of it is cut into pieces whose joints sit **between and offset from** the hot-layer joints. | No anchor drawn |

Printed note under the box (Verified): "When construction joints are required, anchors should remain
halfway between them. Anchor tines should be 2 to 3 inches from the joint. If joint position is not
fixed in the drawing, always cut or form the joint midway between anchors. No anchors should be
located at any joint. Expansion joint construction is the same, except that the joint is thicker to
permit insertion of the required expansion material."

- What the joints are filled with: **Not shown.** The drawings show a bare cut line. The text beside
  them says "some types of compressible material should be incorporated in the expansion joint",
  and that a construction joint is for shrinkage and cracks on drying (Verified).
- The 5 in split between the two shapes is the only number the drawings carry. A joint through
  5 in or less is a plain slant; through 5 in or more it is stepped (estimated from the drawing,
  that the step is to lengthen the leak path; HWI doesn't say why).
- Where the double lining joints sit: offset between layers (Verified in the drawing), though no
  distance is printed.
- Kiln relevance: a cast door frame, arch, floor or car top. The owner's rule stands: anchors are
  reference only and most kiln castables need none. The one usable rule is the geometry of the
  joint itself: slant a joint in a lining 5 in or less, step it in one thicker than 5 in, and in a
  double lining offset the backup's joints from the hot layer's.

## 2. Wall bonding (UR-20, PDF 80; UR-21, PDF 81)

### 2.1 What UR-20 draws

The page title is "Bonding of Walls Built with Rectangular Brick". It has **eight** isometric
drawings, each an L-shaped corner of wall stepped back course by course. They are not nine, and not
only 9, 13½, 18 and 22½: the thicknesses repeat. All captions below are Verified on the image.

| # | Wall | Caption as printed |
|---|---|---|
| 1 | 9 in | "Alternate header and stretcher courses" |
| 2 | 13½ in | "Alternate header and stretcher courses" |
| 3 | 13½ in | "Three header courses to one stretcher course on exposed or hot face" |
| 4 | 18 in | "Alternate header and stretcher courses" |
| 5 | 13½ in | "Three stretcher courses to one header course on exposed or hot face" |
| 6 | 18 in | "Only header course on hot face" / "Mainly stretcher course on cold face" |
| 7 | 22½ in | "Only header course on hot face" / "Alternate header and stretcher course on cold face" |
| 8 | 13½ in | "Five header courses to one stretcher course on hot face" / "Only stretcher course on cold face" / "Back-up brick not tied to inner courses" |

- **Course by course:** Not readable (limit above). Both the L's corner return and the stepped
  courses show alternate courses with the brick joints breaking, and the corners are bonded round
  (the two wings interlock at the corner in every drawing, estimated from the drawings).
- What follows from the brick size, **Derived** (9 × 4½ × 3 in straight; a header lies with its
  9 in length through the wall, a stretcher with 4½ in through):
  - 9 in wall, alternating: a header course is one 9 in header, a stretcher course is two rows of
    4½ in stretchers (a double-width course). So drawing 1 is the plain English bond.
  - A 13½ in wall is 9 + 4½: a header course is a 9 in header plus a 4½ in stretcher behind it, so
    "alternate" gives a course of header-plus-stretcher, then a course of three stretchers (3 × 4½).
    I could not check this against the drawing.
  - Drawing 8: five hot-face header courses of 9 in with a single 4½ in row of stretchers behind
    them (the "only stretcher course on cold face") makes 13½ in. The backup is "not tied to the
    inner courses": that is the case UR-19's text allows when expansion rates differ markedly
    (first pass §3.5).
  - Drawing 7: 22½ = 9 in of hot-face header + 13½ in of alternating backup. Drawing 6: 18 = 9 +
    9 (two stretcher rows, "mainly" stretchers).
- **IFB or other backup:** the drawings show **no** insulating brick, no mortar, no anchors, no
  steel, no expansion joint. The only "backup" word is drawing 8's caption. Nothing about IFB in
  UR-20 (**Not shown**).
- The first pass's UR-19 text: "Three or four stretcher courses to a header" for a 4½ in skin wall.
  The drawing prints three (drawing 5), not four.

### 2.2 Against Olsen and the engine

- Olsen (`kiln-reference.md` "Walls, bonds and openings", pp.41–44): English bond (alternate
  header and stretcher courses) in 9 or 13½ in walls is "extremely stable"; a mainly-header wall
  has three or four header courses to a stretcher course; a mainly-stretcher wall three stretcher
  courses to one header (his Fig. 2-4 draws four); a 13½ in wall three ways, one being four
  courses of hot-face stretchers backed by headers then a header course backed by stretchers.
- HW's drawings agree on the principle and the bond names (alternate H/S for 9 and 13½ in; 3:1 each
  way for 13½ in). HW adds three things Olsen doesn't draw: the 5:1 header wall with an untied
  backup (drawing 8), 18 in and 22½ in walls with an all-header hot face (6, 7), and a 3:1
  stretcher/header ratio at 13½ in with no 4:1 (Olsen's Fig. 2-4 draws four). No conflict in
  substance; a difference of one course in a ratio the text calls "normally three".
- A kiln builder's 9 in wall: drawing 1 (alternate). A 13½ in wall: drawings 2, 3, 5 or 8. For a
  hot face of IFB, HW's drawing 8 (header-faced, untied backup) is the nearest to a veneer on
  backup, but HW draws no IFB.
- **The engine models no bond.** `masonry.py` and `round_masonry.py` contain no "header",
  "stretcher" or "bond" (Grep, 2026-11-17). `curve_masonry.py` lays all stretchers (Olsen's
  Figs 4-143, 4-144). `conical.py` has header and stretcher dome courses (9 in deep in headers,
  4½ in in stretchers). So nothing in the engine depends on UR-20.

### 2.3 UR-21's figure (PDF 81)

One black-and-white photograph, bottom right: a rammed plastic arch in a frame. Caption (Verified):
"Rammed plastic refractories used for arch construction minimize the number of joints." The rest of
UR-21 is the text and count table the first pass read. No other box.

## 3. Arches (UR-22 to UR-29, PDF 82–89)

### 3.1 Arch types (UR-23, PDF 83)

Four drawn arches, each between two steel buckstays with a tie rod across the top, each with brick
side walls (Verified captions and what is drawn):

| Caption | What distinguishes it in the drawing |
|---|---|
| "Ribbed arch roof" | The crown shows raised bands running across the roof at intervals: rings of a longer brick every third or fourth ring (text, UR-22). The roof sits on channel rails on the wall tops. |
| "Ring arch roof" | Every course is a continuous ring across the roof, with the joints running unbroken round the arch. A sprung brick arch on skews, tie rod above. |
| "Typical castable construction for sprung arch" | A smooth, single-piece cast arch: no brick joints. The skew is a cast shoulder on the wall head. Tie rod above, same frame. |
| "Bonded arch roof" | The brick pattern is staggered along the roof: joints are broken from ring to ring (the bricks form a bond like a wall's, estimated from the drawing). Same frame. |

These agree with UR-22's text, which the first pass read (rings, bonded, ribbed, suspended,
monolithic). No dimension is printed. A suspended arch is not drawn.

### 3.2 The arch geometry and thrust diagram (UR-22, PDF 82, and UR-25, PDF 85)

Two diagrams, Verified at 400 dpi.

**UR-22**: "Hypothetical position of thrust in a simple sprung arch, when the bricks are in full
contact at joints." The left half is drawn solid, the right half as a dashed mirror. Labels, and
what each is in `kiln-hardware.md` §4.3's symbols:

| UR-22 label | Drawn as | §4.3 symbol |
|---|---|---|
| S | Horizontal dimension line under the arch, between the two inside-arc springing points | span S |
| h | Vertical dimension from that chord to the inside arc at midspan | rise h |
| r | A radius line from the centre below to the inside arc | inside radius r |
| T | Vertical dimension across the arch at the crown | thickness T |
| θ over 2, twice | Two arcs below the span, one per half, each marked θ/2 (the glyph is a circle with a bar: θ) | central angle θ (each half ½θ) |
| Line of thrust | A dash-dot line through mid-thickness from the crown to the skewback | the line of thrust (the S20 assumption: mid-thickness at crown and skewbacks) |
| Center of gravity | A small circle on the line of thrust in the left half, with a thin arrow down to "W/2" | where W/2 acts |
| W/2 | A thin arrow down from the centre of gravity; and a thick arrow down at the skewback, marked "−W/2" | W/2 per side; the reaction is −W/2 |
| H | A thick horizontal arrow at the left skewback | horizontal thrust H |
| −H | A thick horizontal arrow at the crown, pointing the other way | −H, the balance of the other half |
| F | A thick arrow along the line of thrust, from the crown down to the left skewback | resultant F |
| −F | An arrow at the skewback, equal and opposite | the reaction −F |
| Center of pressure | A short hatched joint in the right half, near its centre of the line | where the resultant crosses a joint |

So the diagram carries H, F, W/2, S, h, r, T and θ, as §4.3 does. W (the whole-arch weight) is
not drawn, only its half. R (outside radius) is not on this drawing; it is in UR-25 and UR-28's
list.

**UR-25 and UR-28** (the same drawing twice, PDF 85 small, PDF 88 large): a half-circle sector with
its two skewbacks. Labels (Verified): OUTSIDE ARC A, INSIDE ARC a, RISE h, SPAN S, CENTRAL ANGLE θ,
½θ (at the centre), INSIDE RADIUS r, T, and four skew dimensions: **P** (horizontal) and **Q**
(vertical) on the left, "Skewback not flush with arch at top"; **H** (horizontal) and **V**
(vertical) on the right, "Skewback flush with arch at top". UR-28's list: a_a length of inside arc,
A_a length of outside arc, R, r, S, d, h, T, θ, and "H, V, P, Q = Skewback dimensions indicated in
the Arch Constants table".

- The skew's H and V are the horizontal run and vertical rise of the sloped face. P and Q are the
  same pair for a skew whose top is **not** flush with the arch (Q is the skew's height, P the
  corresponding run). `kiln-hardware.md` §4.3 formulas 8, 12, 13 (H = T sin ½θ, V = T cos ½θ,
  P = Q tan ½θ) are these.
- **Misprint in the table, UR-25 (PDF 85).** The ninth column, "Skewback F", holds 0.34286Q …
  1.33333Q. Those are **P** (P = Q tan ½θ; at 1.608 in/ft, tan 30° = 0.57735, which is the printed
  0.57735Q, Derived). The heading F collides with the resultant F of UR-26. `kiln-hardware.md`
  has it right (column "P (skew)").
- **Misprint in the note under the table (UR-25).** The printed note says: "Column 2, ½ cosecant
  ½θ; column 4, Ø divided by 360°; column 5; ½ cosecant ½θ". Column 5 (inside arc, in units of S)
  can't be the same function as column 2. At 60° it is 1.04720: that is (πθ/360°)·cosec ½θ =
  0.5236 × 2 = 1.0472 (Derived). The printed column 5 note repeats column 2's.

### 3.3 Skewback constructions (UR-24, PDF 84)

Six small drawings in a box, each a half-section of the wall head and the springing of the arch, with
a steel buckstay (the vertical member on the left) and brick wall below. Each has a printed caption
and, where drawn, an arrow labelled "Approx. Line of Thrust". The first four of these descriptions
of the line's position are **estimated from the drawing**; the arrows are drawn schematically.

| # | Caption as printed | What is drawn | Line of thrust against the support |
|---|---|---|---|
| 1 | "Special skewback / A recommended construction" | One special skew block, sitting on a horizontal steel flat or angle at the top of the wall, against the buckstay. A header course below; "Ground Brick and Mortar Mixture" at the foot of the skew on the arch side. | The arrow runs from the skew's lower corner **through the corner of the supporting steel** and out through the buckstay |
| 2 | "Built-up skewback / A recommended construction" | Standard skews (two pieces, so a stack) on a header course, held by a small steel angle at the wall head; ground brick and mortar mixture at the toe. | The arrow runs down-left **through, or at, the corner of the angle** and the buckstay |
| 3 | "Built-up skewback / **A construction to be avoided.**" | Standard skews built up on stretcher-looking courses of the wall; the angle sits high on the stack. | The arrow, from the arch's toe, runs down across the wall's upper corner and meets the buckstay **below** the angle: the thrust passes **under and outside the support**, through the brickwork (estimated). This is the case UR-26 words as the line passing "through, or slightly above, the corner of the supporting steel" and the drawing breaks. |
| 4 | "A 60° skewback with buttress block." | Skewback No. 60-9 sitting on a buttress block, which sits on a buttress angle bolted to the buckstay. The wall below is brick with a vertical strip of "Bulk Insulation" between the hot brick and the steel. Labels: Buckstay, Buttress Block, Skewback No. 60-9, Top of Skewback, Buttress Angle, Bulk Insulation. | No arrow drawn |
| 5 | "Special skewback / A construction occasionaly used" (misspelled as printed) | A special skew with "Special Shapes" (three small blocks, marked with dots) built up on top of the wall, against the buckstay; a small I-shaped mark between buckstay and skew at the skew's foot (not readable: possibly a spacer or gap). | The arrow runs from the arch's lower brick across the top courses of the wall to the buckstay **below the skew** (estimated); no steel corner is drawn at the skew's foot |
| 6 | "Arch with skewbacks supported outside of walls" | A skew carried on a channel (C-shaped steel, open side up) clear of the wall, the brick wall standing under it, no buckstay shown. | No arrow drawn |

- Printed note under the box (Verified): "A stretcher course should never be used immediately
  below the skewback." In drawings 1 and 2 the course under the skew is labelled "Header Course".
- "Constructions to be avoided": **one**, drawing 3 (the built-up skewback). No span is named in
  any caption. The only span in the nearby text is UR-26's: "Built-up skews satisfy the requirements
  of narrow spans, four feet or less" (first pass §3.6).
- The two recommended constructions are the ones whose arrows pass through the steel's corner. That
  is the practical reading of UR-26's rule, and the drawings are its only picture (no dimension).
- The drawn skews against `kiln-hardware.md` §5:
  - "Standard Skew" and "Special Skew" are not dimensioned. "Special Shapes" are not defined.
  - "Skewback No. 60-9" is the one-piece shape of §5.4. It is the shape whose printed toe
    (17/32 in) doesn't fit the arch formulas. UR-24 draws it only as a block on a buttress block,
    with no dimension, so it doesn't settle §5.4.
  - The drawn skew faces slope up toward the arch at roughly the angle of the arch springing;
    that is all that can be said (estimated). No feather, 9 in or 13½ in skew is drawn.
  - A **buttress block** (UR-24 drawing 4) is not in `kiln-hardware.md`. It's a block that carries
    the skew and bears on an angle fixed to the buckstay; the printed word is all HW gives.
- UR-26 (PDF 86) has the formula F = √(H² + (W/2)²) set in the text and the table of constants
  of §4.3, no drawing. UR-27 (PDF 87) has the Hmax table and the "Complex refractory design
  problems" text, no drawing and no box.

### 3.4 The arch formulas (UR-28, PDF 88)

The 13 formulas, Verified on the image, match `kiln-hardware.md` §4.3 symbol for symbol:
r = S²/8h + h/2; R = r + T; h = r − √(r² − (S/2)²); sin ½θ = S/2r; tan ¼θ = 2h/S; tan ¼θ = d/6;
part of circle = θ/360°; H = T sin ½θ; d = 6 tan ¼θ; a_a = 6.2832 r (θ/360°); A_a = 6.2832 R (θ/360°);
V = T cos ½θ; P = Q tan ½θ. One print difference: formula 8 is printed with the symbol **H**
(skew run), which is not the horizontal thrust H of UR-26. §4.3 keeps the same letter ("skewback
H") and so carries the same overload. The 12 ft worked example (UR-28): sin ½θ = 12/(2 × 9.125) =
0.6575, arcsine 41.11°, central angle 82.22° = 82° 13′ (Verified).

### 3.5 The ring formulas (UR-29, PDF 89)

The drawing (Verified at 300 dpi): two views of a ring segment, each titled "Ring Calculations".
Left: "Combination of a Straight Brick (E) and a Radial Brick (F) to Form a Ring": the sequence
F F E F F E, the E bricks parallel-sided, the F bricks tapered, with chord marks C_f and C_e above
("Outside Cord Dimensions", sic) and c_f and c_e below ("Inside Chord Dimensions"), and the radial
depth T marked. Right: "Combination of Two Radial Brick (E and F) to Form a Ring. Brick E Turns a
Large Diameter than Brick F" (sic): F E F E, both tapered, the same marks.

Symbols (UR-29, Verified): E, F bricks; T radial dimension common to both; D_e, D_f outside
diameters of the rings E and F would form alone; D_g a given outside diameter (between D_e and D_f
for two radial bricks); d_g a given inside diameter; C_e, C_f outside chords; c_e, c_f inside
chords; N_e, N_f numbers used; N_t total; N_x the number of E to form a complete ring of outside
diameter D_e; N_y the number of F for a complete ring of D_f.

The formulas as printed, and a check (**Derived**):

| No. | As printed | Check |
|---|---|---|
| 1-a | N_f = 2πT / (C_f − c_f) | Correct: a full ring of radial bricks has N·C = πD_o and N·c = πD_i, so N(C − c) = π(D_o − D_i) = 2πT |
| 2-a | N_t = πD_g / C_e = πD_g / C_f | Correct when the straight and the radial brick have the same outside chord (C_e = C_f) |
| 3-a | N_e c_e + N_f C_f = πD_g | **c_e is lower case**, confirmed on the image. With the outside diameter D_g, E's chord must be C_e: N_e C_e + N_f C_f = πD_g |
| 4-a | N_e = N_x/(D_e − D_f) · (D_g − D_f) | Linear interpolation between a ring of all E (N_x) and none; correct |
| 1-b | N_e = (πD_g − N_f C_f) / C_e | Correct, given N_f |
| 2-b | N_e = (πD_g − N_f c_f) / (c_e − c_f) | **Misprint as printed.** Inside chords with the outside diameter D_g, and N_f in the numerator. Solving N_e c_e + (N_t − N_e) c_f = πd_g gives N_e = (πd_g − N_t c_f)/(c_e − c_f): N_t and d_g (the inside diameter) |
| 3-b | N_e c_e + N_f c_f = πd_g | Correct (inside chords, inside diameter) |
| 4-b | N_f = N_y/(D_e − D_f) · (D_e − D_g) | Correct, linear |
| 1-c | N_t = N_e + N_f | |
| 2-c | N_f = N_t − N_e | |
| 3-c | N_t = N_e + N_f | |
| 4-c | N_t = N_e + N_f | |

- Against `rings.py` (docstring lines 6–11): N = π(D + 2L)/T outside, Σ nᵢtᵢ = πD inside,
  n₂ = (πD − N t₁)/(t₂ − t₁), n₁ = N − n₂. These are HW's 2-a/3-a for the outside count, 3-b for
  the inside, and 2-b **as corrected** (N total for N_f, inside diameter d_g for D_g). The engine
  has the right form; the book's printed 2-b is the one that is wrong. No engine change.
- The first pass's note that 3-a has a lower-case c_e is **confirmed** (Verified).

## 4. Castable and plastic installation: photographs and figures

Only what a builder of a castable or ram-mix kiln part would use. The rest is in the first pass
§3.3–3.4.

- **UR-9 (PDF 69)**, four photographs (Verified): "A paddle mixer is used for castables" (looking
  down into the mixer); "This ball shows too much water in the mix" (a slumped, wet ball in a hand);
  "This ball is too dry for casting" (a crumbly ball); "A properly mixed ball shows the impression
  of fingers when tossed 6 to 12 inches in the air and caught" (a hand holding a ball with finger
  marks). Text: mixer of 4–12 ft³; "ball-in-hand" described in first pass. Numbers: none beyond the
  6–12 in toss.
- **UR-10 (PDF 70)**, three photographs of a pail under a vibrator (Verified): "This mix is right
  for vibration casting"; "This contains too much water for vibration" (a smooth, thin, glossy
  surface); "There is not enough water in this batch" (rough, holes). The text: a mix is too stiff if
  the vibrator "leaves holes"; a mixing minimum of 5 min for the low-water VERSAFLOW, ULTRA-GREEN
  and EXPRESS castables; steel forms preferred to wood; wood forms waterproofed; casting against
  existing masonry needs that masonry waterproofed; "construction joints will coincide with the
  expansion joints shown on the drawings"; use an alternate bay system (Read, first pass for the
  rest).
- **UR-12 (PDF 72)**, Figure 1 (a graph of material consistency, Dusty / Damp / Sticky / Castable,
  against water addition, with a narrow band for old-style gun mixes and a wide one for HW's). Gun
  mixes only. Predampen dense gun mixes with 4–6 % water by weight, lightweight and medium-weight
  10–15 % or more (Read; not a kiln part).
- **UR-13 (PDF 73)**, Illustration 1 (a nozzle spraying a wall in oval loops): loops 6–9 in high and
  18–24 in wide, starting 3–6 in from the side edge, nozzle 3–4 ft from the face, perpendicular to
  it (Verified). Gunning; not for a studio kiln.
- **UR-14 (PDF 74)**, two boxes (Verified): a red box, "For the proper schedule for specific products,
  use this link to the Mixing and Use section of our web site. www.hwr.com", and a grey **CAUTION**
  box: spalling during heat-up if the procedures aren't followed; the schedule temperatures "are the
  temperatures of the hot gases in contact with the castable or gun mix and not the lining itself";
  thermocouples may be ½ in from the surface; if steaming is seen, hold until it stops; ventilate
  to remove steam; avoid flame impingement. Same as the first pass §3.3, now with the box layout
  and the warning that this is the safety caution box.
- **UR-15 (PDF 75)**, one photograph, "Peening. Plastic adjacent to anchors should be lightly rammed
  up and around the anchors to give a tighter seal." (a worker ramming overhead with an air tool).
  New numbers from the text (Read, the page was also viewed): a pneumatic ramming tool with a
  **minimum 2½–3 in convex aluminium head**; ram the whole mass two or three times; ram parallel to
  the hot face; a lining thickness overage of ⅛–¼ in of plastic so the hot face keeps its full
  thickness after the forms are stripped; ram the 3 in area next to a form one extra time; trim the
  hot face back to the anchors and keep the surface coarse, not smoothed, "a coarse surface is
  necessary for uniform drying"; construction joints scored about 2 in deep on 36 in centres;
  steam vents ⅛ or 3/16 in rod, 8 or 12 in centres, to two-thirds of the thickness.
- **UR-16 (PDF 76)**, one photograph of the BSM gun, caption "Here you can see the BSM Gun, the
  "V" Shaped opening in the bulk carton, and the GREENGUN plastic being raked into the hopper."
  Gunning equipment; rebound 15–20 %. Not a kiln part. Patching: chip back to a sound surface,
  steep-angled sides, a V cut toward the cold face, a thin coat of PHOXBOND under phosphate-bonded
  plastic, the patch bonds at about 500 °F (Read).
- **UR-17 (PDF 77)**, two boxes: Schedules I and II (first pass §3.4; layout checked on the image, the
  text agrees). A paragraph "PLUS designation": plastics with PLUS in the name have non-metallic
  fibre additions for moisture removal and "passed a very severe spalling test", heated more quickly
  (no rate given). Winterized plastic: freezing point lowered to below 15 °F (−9 °C); optimum plastic
  storage 55–60 °F (Read).
- **UR-18 (PDF 78)**, one photograph, "Installing ramming mix in top cap of coreless induction
  furnace." (Verified). Rules not in the first pass (Read, page viewed): ram at "the most acute
  angle possible to the hot face"; an anvil or reciprocating air rammer with a metal head; score
  each layer about ¼ in deep; a good sign that the mix is rammed enough is that the rammer head
  leaves noticeable tracks in the top face; cover an interrupted job with a damp cloth if the break is
  over one hour.
- UR-3 (PDF 63) and UR-4 (PDF 64): tables only, covered in the first pass; no figure.

## 5. Every sidebar, caution box and boxed note, UR-1 to UR-29

Found by scanning every page for boxes and images, then viewing each hit. Verified unless "Read".

| Label (PDF) | Box | What it is |
|---|---|---|
| UR-3 (63) | Three framed tables | Straights per ft² (3.6 … 32.1), mortar per 1000 brick, overage. First pass §3.5 |
| UR-4 (64) | One framed table | Thermal expansion by brick type. First pass §3.1 |
| UR-5 (65) | "Typical Joint Construction" | §1 above |
| UR-14 (74) | Red box and grey CAUTION box | §4 above |
| UR-17 (77) | Schedule I and Schedule II | First pass §3.4 |
| UR-20 (80) | One framed picture | §2 above |
| UR-21 (81) | Count table and a photograph | §2.3 |
| UR-22 (82) | Framed diagram | §3.2. Also a footnote beside the UR-25 text (below) |
| UR-23, UR-24 (83, 84) | Framed drawings | §3.1, §3.3. UR-24's box ends with the stretcher-course note |
| UR-25 (85) | Framed arch-constants table, a diagram, and a footnote | The footnote: "Assuming that the absolute lower limit for the rise of the line of thrust is ¼ inch (1/48) per foot of span, the rise (h) must exceed thickness (T) times the cosine of the central angle (θ) plus 1/48 span (S). This implies that T should not exceed: (h − S/48) / cosine θ/2." It also cites J. Spotts McDowell, "Sprung-Arch Roofs for High Temperature Furnaces", *Blast Furnace and Steel Plant*, September 1939. First pass: the formula is in `kiln-hardware.md` §4.3 (Read; not new) |
| UR-26 (86), UR-27 (87) | Framed tables | W/H/F and Hmax; checked cell by cell in the first pass |
| UR-28 (88), UR-29 (89) | Framed diagrams | §3.4, §3.5 |

Pages UR-1, UR-2, UR-6 to UR-8, UR-11, UR-19 have no box or image (page scan). UR-6 to UR-8 hold
the heat-flow equations and the worked-example tables (first pass §3.2).

## 6. Brick shapes, IR-1 to IR-10 (PDF 125–134)

### 6.1 IR-1, IR-2, IR-3 (PDF 125, 126, 127): the 9 in series drawn

IR-1 is text only (first pass §4.3). **IR-2 (PDF 126)** and **IR-3 (PDF 127)** are the shape
drawings of the "Nine-Inch Sizes (9 × 4½ × 3)": every shape an isometric block with its dimensions
printed on it. Verified on the image. Every printed size is the one in `kiln-hardware.md` §5.1's 3 in
series and in `brick-shapes.md`:

| Shape (page) | Printed size | In §5.1 / brick-shapes |
|---|---|---|
| 9 Inch Straight (IR-2) | 9 × 4½ × 3 | yes |
| Small 9 Inch Straight | 9 × 3½ × 3 | yes |
| 9 Inch Soap | 9 × 2¼ × 3 | yes |
| 9–2 Inch Split | 9 × 4½ × 2 | yes |
| 9 Inch Split | 9 × 4½ × 1½ | yes |
| No. 1-X Wedge | 9 × 4½ × (3 − 2⅞) | not in §5.1 |
| No. 1, 2, 3 Wedge | 9 × 4½ × (3 − 2¾ / 2½ / 2) | brick-shapes yes |
| No. 1, 2, 3 Arch (IR-3) | 9 × 4½ × (3 − 2¾ / 2½ / 2) | yes |
| No. 1, 2, 3, 4 Key | 9 × (4½ − 4 / 3½ / 3 / 2¼) × 3 | yes |
| 48° and 60° Side Skew | 9 × (4½ − 1 13/16) × 3 and 9 × (4½ − 2¾) × 3 | yes |
| 48° and 60° End Skew | (9 − 6 5/16) × 4½ × 3 and (9 − 7¼) × 4½ × 3 | yes |
| Edge Skew | 9 × (4½ − 1½) × 3 | yes |
| Featheredge | 9 × 4½ × (3 − ⅛) | yes |
| Neck | 9 × 4½ × (3 − ⅝) | yes |
| 9 Inch Jamb | 9 × 4½ × 3, drawn with a quarter-round on the 9 × 3 edge (radius spanning the 3 in) | yes (§5.1: "rounded edge") |

Differences from the other notes:
- IR-3 draws **No. 1, 2, 3 Arch only**, no No. 4 Arch; `brick-shapes.md` and IR-4's table list
  a No. 4 Arch (3 − 1) (text layer of IR-4, first pass). Not a conflict: IR-4 has it.
- The drawn "arch" tapers across the 4½ in width and the "wedge" along the 9 in length, as
  `brick-shapes.md` notes ("tapers across 4½ in width, wedge across 9 in length").
- Dimensions printed per drawing (e.g. 48° side skew "1 13/16" at the top, and the skew's 3 in
  rise) are the §5.1 numbers; the 3 in series skew angles check as in §5.1's Derived paragraph.
  Nothing conflicts.

### 6.2 IR-5 (PDF 129): larger sizes

A table (not a drawing): 13½, 15, 18 and 21 in lengths in 4½, 6, 6¾ and 9 in widths, 3 in thick,
with 9 in-straight equivalents. The first pass read IR-4 (PDF 128) only. Verified on the image, for
the sizes a kiln might use:

| Size | Shape | Equivalent |
|---|---|---|
| 13½ × 4½ × 3 | Straight | 1.80 |
| | No. 1 / 2 / 3 Arch (3 − 2¾ / 2½ / 2) | 1.72 / 1.65 / 1.50 |
| | No. 1 / 2 / 3 / 4 Key (4½ − 4 / 3½ / 3 / 2¼) | 1.70 / 1.60 / 1.50 / 1.35 |
| 13½ × 6 × 3 | Straight | 2.40 |
| 13½ × 9 × 3 | Straight | 3.60 |
| 15 × 4½ × 3 | Straight | 2.00 |
| 18 × 4½ × 3 | Straight | 2.40 |

Check (Derived): 13½ × 4½ × 3 over a 9 × 4½ × 2½ is 182.25/101.25 = 1.80, as printed. The sheet also
lists miscellaneous straights (9 × 6 × 2 = 1.07; 9 × 7 × 2 = 1.24; 9 × 7½ × 2 = 1.33; 10½ × 4½ × 3 =
1.39; 10½ × 4½ × 4½ = 2.10; 13½ × 4½ × 4½ = 2.70; 18 × 6¾ × 3 = 3.60; 18 × 9 × 4½ = 7.20). I did not
compare the rest cell by cell with `brick-shapes.md`.

### 6.3 IR-6 (PDF 130): door jambs, blast-furnace bottom blocks, **circle brick**

Three things, Verified at 300 dpi.

**METALKASE door jamb brick.** One photograph of a tapered block (a wedge in side view) with
dimensions A (length), B (tall end), C (short end), D (width). Metal-cased brick for electric-arc
furnace door jambs.

| Name | A | B | C | D (in) |
|---|---|---|---|---|
| DJ-1-3 | 9 | 4½ | 1½ | 3 |
| DJ-2-3 | 9 | 6¾ | 3¾ | 3 |
| DJ-3-3 | 9 | 9 | 6 | 3 |
| BS-115-3 | 13½ | 6¾ | 2¾ | 3 |
| BS-116-3 | 13½ | 9 | 5 | 3 |
| DJ-18-1-3 | 18 | 6¾ | 2¾ | 3 |
| DJ-18-2-3 | 18 | 9 | 5 | 3 |

The slope is B − C = 3 in over A in every 9 in shape (DJ-1: 4½ − 1½ = 3; DJ-2: 6¾ − 3¾ = 3; DJ-3: 9 − 6 = 3)
(Derived). It's a steel-cased door-jamb shape for an arc furnace: no metal case dimension, no
steel gauge. Whether it suits a kiln door jamb I can't say from the page; it is not a kiln
shape and the metal case is not shown.

**Blast-furnace bottom blocks** (18 × 9 × 4½ in, laid on end): a table of blocks per course by
hearth jacket diameter, 17 ft 6 in (897) to 37 ft 0 in (3909). One line; not a kiln shape.

**High-alumina circle brick, nine-inch sizes (9 × 4½ × 3 in), "Circle Brick Number (3 Inch)".** The
drawing is a keystone block, marked 9 in, 4½ in and 3 in. The footnote: "The first two numbers of
the Circle Number indicate the inside and outside diameters, respectively, of the ring produced by
each shape. For example, 24 - 33 - 3 Circle Brick will produce a ring with a 24-inch inside diameter
and 33-inch outside diameter for a 4½ inch lining." Verified:

| Circle brick number | Chord, in | Number per ring |
|---|---|---|
| 24-33-3 | 6 17/32 | 12 |
| 36-45-3 | 7 3/16 | 16 |
| 48-57-3 | 7 19/32 | 20 |
| 60-69-3 | 7 13/16 | 24 |
| 72-81-3 | 8 | 29 |
| 84-93-3 | 8 1/8 | 33 |
| 96-105-3 | 8 7/32 | 37 |
| 108-117-3 | 8 5/16 | 41 |
| 120-129-3 | 8 3/8 | 45 |

- The column is headed only "Chord (Inch)". It does not say inside or outside. **Derived:** it
  tracks the inside arc π·ID/N within 0.25 in: π·24/12 = 6.28 (chord 6.53), π·60/24 = 7.85 (7.81),
  π·120/45 = 8.38 (8.375). The outside arc π·OD/N is 8.64 to 9.01. So the printed chord is about the
  inside face's width (estimated; HWI doesn't say). The count for the 4½ in lining is N ≈ π·OD/9 at
  the larger sizes.
- This was **not** in the first pass, and it bears on `blocked-items.md` §4 ("dome and circle brick
  tables" Not found). It is **only a nine-size high-alumina table for the 3 in series 4½ in
  lining**, 24 in to 129 in. `brick-shapes.md` (A.P. Green's catalogue, "complete circles", pp.111–163)
  has the fuller set. Whether the shape is made in fireclay is not stated on the page. A kiln's
  circle usually has an ID smaller than 24 in or is built of arch/wedge brick (IR-26–IR-29, first
  pass §4.4), so this table is a cross-check for a larger round kiln, not a new route.

### 6.4 IR-7, IR-8, IR-9, IR-10 (PDF 131–134)

- **IR-7 (PDF 131), blast-furnace keys.** Four key shapes drawn: 13½ in X-1, 9 in X-1, 13½ in X-2,
  9 in X-2 (6 in top, 5 11/16 in bottom or 5 29/32 and 5 11/16 in, 3 in thick), plus the table "Brick
  Combinations for All-Key Linings" (X-2 and X-1 per ring, by inside diameter from 13 ft 3 in to
  41 ft 0 in). The note: X-1 and X-2 are also made in 6, 10½ and 15 in lengths and the table applies
  to all. Not a kiln shape. (The table prints "t84" for 184 at 27 ft 0 in: 49 + 135 = 184, Derived.)
- **IR-8 (PDF 132), IR-9 (PDF 133), electric-furnace roof shapes.** IR-8 is the radius table the first
  pass read. IR-9 is a drawing, not text only: a plan of a circular roof in rings of brick, three
  electrode holes in a triangle at the middle, with a detail enlarged at left of the **A** and **B**
  bricks in a ring, and the two shapes drawn tall (A and B each tapered on two faces, each with a
  small notch or peg at the cold end "notching system at the cold end of the brick shape", per IR-8's
  text). Below, a section across the roof from a steel ring at the left to a larger centre block
  (the electrode delta ring) on a stepped steel ring at the right. No dimension. The shape
  designations and radius ranges are in the first pass. Nothing for a kiln dome.
- **IR-10 (PDF 134), semi-universal ladle brick (SULB).** A drawing of a ladle lining's
  spiral courses (tilt-back course, starter set of 12 or 18 pieces, half-brick to bond the course),
  and the 4 in series dimensions (SU 4-20: A 6.983; SU 4-30: 7.414; SU 4-45: 7.690; SU 4-60: 7.831;
  all 8.250 long, 4 in thick, 3 in). The worked count: pieces per ring = π × average diameter ÷
  8.25 (the brick length), rings = height ÷ 3. Not a kiln shape. The one thing of interest: this
  is the maker's own use of the "π D / brick length" count, as in HW's ring formulas.
- **IR-11, IR-12 (PDF 135–136):** done in the first pass, not redone.

---

## 7. What the engine can use

| Need | Finding | Status | Where it would go |
|---|---|---|---|
| A cast joint rule | Slant the joint in a lining 5 in or less, step it in a thicker one, offset the backup's joints from the hot layer's; no filler drawn | Verified (UR-5, PDF 65) | `castable.py` notes as information |
| A line of thrust check | Thrust through or slightly above the steel's corner is drawn as recommended; a built-up skew with the line below the angle is "a construction to be avoided" | Verified (UR-24, PDF 84; line positions estimated) | `frame.py` skewback note (words only, no number) |
| A stretcher course below the skew | "A stretcher course should never be used immediately below the skewback"; headers drawn under the skew | Verified (UR-24) | A skew detail in `frame.py` or the plans' notes |
| Ring formulas | The book's 1-a, 2-a, 3-b, 4-a, 4-b are right; 2-b and 3-a have misprints; `rings.py` has the correct 2-b | Verified (UR-29, PDF 89) | No change; the docstring may cite UR-29 |
| Wall bonds | 9 in: alternate H/S. 13½ in: alternate, 3 H : 1 S, 3 S : 1 H, or 5 H : 1 S with an untied backup. 18 in and 22½ in: header hot face | Verified (captions, UR-20, PDF 80) | A bond note if the engine ever draws one; today none |
| Circle brick counts, 24–129 in ID | N = 12 at 24 in to 45 at 120 in for the 4½ in lining, 3 in series, high alumina | Verified (IR-6, PDF 130) | A cross-check of `rings.py` for round kilns above 24 in |
| Brick shape sizes | IR-2 and IR-3 print the 3 in series sizes of `kiln-hardware.md` §5.1; larger straights in IR-5 | Verified (PDF 126, 127, 129) | No change; the equivalents are the same |
| A cast arch | Castable sprung arch with a cast skew shoulder, same buckstay and tie-rod frame as a brick arch | Verified (UR-23, PDF 83) | The frame check applies to cast arches |
| Ramming a plastic or ram mix | Aluminium 2½–3 in head, ⅛–¼ in overage, 3 in extra pass beside forms, ¼ in score between layers | Read, page viewed (UR-15, UR-18) | Only if the engine models a ram-mix skin (Olsen p.42) |

## 8. Conflicts

With `kiln-hardware.md`:
- §4.3 table of constants: the ninth column's heading in UR-25 is **F**, §4.3 calls it **P**. §4.3 is
  right (P = Q tan ½θ). Add a line: "HW prints the heading F; the values are P."
- §4.3 formula 8's symbol H (skew run) and the horizontal thrust H (UR-26): HW uses H for both. No
  change; a footnote would help.
- §5.4's three non-fitting shapes: UR-24 draws 60-9 undimensioned, so the print doesn't settle it.
- §5.1: IR-2 and IR-3 agree with it in every cell. No conflict. The 2 in split is correctly printed
  "9 × 4½ × 2" here (the 2½ in series misprint is IR-4's).

With `brick-shapes.md`: no dimension differs on any of IR-2, IR-3. IR-3 has no No. 4 Arch (IR-4 does).

With the engine: none. `rings.py` is right where UR-29's formula 2-b is wrong.

With the first pass (`hwi-handbook.md`):
- §3.5: "Bonding drawings (UR-20): 9–22½ in walls" is right but there are **eight** drawings, with
  13½ in four times and 18 in twice.
- §3.5 and §3.6: "Three or four stretcher courses to a header" is from the text; the drawing shows three.
- §3.6: UR-29's lower-case c_e in 3-a is confirmed; 2-b has a second misprint (N_f for N_t, D_g for
  d_g) that the first pass didn't record.
- §4.3 and `blocked-items.md` §4: the first pass says "no table" of dome or circle brick; there is
  a high-alumina circle brick table in IR-6 (PDF 130), nine sizes, 24 in to 129 in. The dome-brick
  statement for IR-8 and IR-9 stands.
- §4.3: IR-5 (PDF 129) wasn't read; §6.2 above.

## 9. Not shown, not readable, skipped

- UR-20: the courses of each wall, brick by brick, are not readable at this resolution (a raster).
  Which bricks of the 13½ in walls are headers and stretchers is Derived from the brick size and the
  captions. Any IFB, steel or expansion joint: **Not shown**.
- UR-5: the joint filler, any joint width, any anchor dimension: **Not shown**.
- UR-24: the arrow positions in drawings 3 and 5 are judged by eye; the I-shaped mark in drawing 5 is
  not readable; no span, skew dimension or steel size is printed on any of the six drawings.
- UR-22: the arrowheads' sense (which way H and −H point) was read from the drawing but a
  statics reader should recheck it on the page.
- IR-6: what "Chord" means in the circle-brick table is not printed (§6.3). The METALKASE case's
  metal gauge and dimensions: **Not shown**. Whether the table's brick comes in fireclay: **Not found**.
- IR-5: only the shapes in §6.2 were read closely; the rest of the table is skipped.
- IR-7, IR-10: blast-furnace and ladle tables were not transcribed beyond the lines above.
- UR-12, UR-13, UR-16 gunning: described briefly; no kiln use.
- Photographs in UR-9, UR-10, UR-15, UR-16, UR-18 are described from the 110 dpi render only.

## Sources

- [HW05] *Handbook of Refractory Practice*, © 2005 (as above).
- `hwi-handbook.md` (first pass), `kiln-hardware.md` §4–5, `brick-shapes.md`, `kiln-reference.md`,
  `core/src/kilndesigner/rings.py`.
- Working scripts (git-ignored): `scratch/hwi-deep/using/boxes.py` and the page renders in
  `scratch/hwi-deep/using/img/`.
