# Olsen's figures scaled for engine v2 (2026-11-17)

Read on the page images of the user's scan of Olsen, *The Kiln Book*, 4th ed. (`kiln-reference.pdf`,
git-ignored), for the handoff `docs/planning/11-17-26-page-images.md` (items §1, §3 and §9 of
`11-17-26-inputs.md`). Pages are the book's printed pages; the PDF index of each page is given once,
in the page map below, for the next reader.

Method: pages rendered with pymupdf at zoom 2.4–8 (the scan's images are about 2,200 × 3,000 px a
page, so zoom 3 is about native). Positions come from pixel profiles along rows and columns (dark
runs under a grey threshold); angles from least-squares line fits, corrected by the tilt of printed
level lines (captions, text, photo edges) near the figure. Pixel figures below are at the zoom
stated. Every number is an **estimate**, scaled from a dimension printed on the same figure unless
the row says otherwise; none is a printed value.

Status words: **scaled** (against a printed dimension on the figure); **drawing** (read off the
figure, no scale); **not shown**; **not scalable** (drawn, but nothing printed to scale it against);
**not yet measured** (work left; the session stopped at its turn limit, and each such row says what
is left).

## Page map: book page → PDF index (0-based) of `kiln-reference.pdf`

| Book pages | PDF index | Note |
|---|---|---|
| 54 | 41 | |
| 55 | 42 and 43 | scanned twice |
| 56 | 44 | p.57 is then 45 (not viewed) |
| 83–97 | 68–82 | index = page − 15 (pp.84, 85, 86, 87, 91, 92, 93, 94, 97 checked) |
| 109–111 | 94–96 | page − 15 |
| 116–117 | 101–102 | page − 15 |
| 160–161 | 147–148 | page − 13 |
| 162 | 149 or 150 | one of the two is a narrow partial scan; not checked |
| 163–164 | 151–152 | page − 12 |
| 178–183 | 166–171 | page − 12 (pp.178, 181 checked) |
| 199–206 | 182–189 | page − 17 (pp.190–193 and 195 are not in the scan); all eight checked |

The scan's first 41 indexes run backwards from p.53 (kiln-reference.md).

## 1. Principle 6: each kiln's chimney and exit flues

| Kiln | Page, figure | What the figure draws | Scaled against | Estimate | Spread or status |
|---|---|---|---|---|---|
| `anagama-hole` | p.84, Fig 4-5 (perspective sketch) | A vertical chimney flue from the back of the tube up to the hill line: two lines and a short width arrow, no number. The tube tapers into it; no separate exit flues. | The printed 3½' height (arrow 154–163 px at zoom 2.4: 3.7–3.9 px/in) and 5¼' width (194 px: 3.1 px/in). The two disagree by 25 % (perspective). | Flue width **about 6 in** (15–25 px between the lines, widening downward) | 4–8 in. Depth not drawn. The right-hand line lies at the page's gutter. |
| `anagama-hole` | p.84, Fig 4-5 | The flue's height above the tube's back, to the hill line | as above | about 165–175 px, so 3½–4½ ft | drawing only, rough (perspective); not asked for |
| `falcone-pompeii` | p.161, Figs 6-32, 6-34 (photos) | Fig 6-32: the barrel vault's top with square exit holes (p.161: nine, three across at the back, front and middle). Fig 6-34: the stoking port. No chimney: an updraft that exits through the holes in the vault. | Nothing is printed in either photo, and the bricks' size isn't printed. | — | exit holes **not scalable**; chimney **none** |
| `fireworks-edmonton` | p.178, Fig 7-2 (plan, drawn for both kilns: "DIAGONAL – 7' (CHURCH); DIAGONAL – 9' (FIREWORKS)"); p.181, Fig 7-7 (photo) | Fig 7-2: at the groundhog end, a row of openings between piers into a collection box behind. At zoom 6 (crop of the page from x 0.10 to 0.33, y 0.68 to 0.80), the row y = 150 px crosses eight dark runs (76–135, 174–207, 245–276, 317–342, 387–417, 455–493, 523–557, 590–630 px), leaving **seven gaps** of 30–45 px (?). Fig 7-7: a single tall chimney and a three-flue groundhog chimney (p.179: the groundhog chimney split into thirds). | The printed 9 ft diagonal: its pixel length isn't measured yet. | — | **not yet measured**. Left to do: measure the fore-zone diagonal on Fig 7-2, then scale the gaps and the box against 9 ft. It is a type drawing for two kilns, so widen the spread. |
| `kannofen` | pp.162–164, Fig 6-37 (marked NOT TO SCALE); Fig 6-39 (photo of the firebox end) | Exit flues in seven rows, down both sides and along the top, drawn without sizes (p.164: the two nearest the firebox closed, row three dampered, the last four open). No chimney: the flues vent into the shed (p.162). | Fig 6-37 is marked not to scale; Fig 6-39 prints nothing. | — | **not scalable** as drawn. **Not yet measured:** Fig 6-37 against its printed 1.04–1.07 m section widths (a result would carry the not-to-scale spread), and Fig 6-38 (p.163, the kiln in its shed), whose top flues were probed at zoom 8 without a clear result. |
| `la-borne` | p.109, Fig 4-78 (plan and elevation, blurred); p.110, Fig 4-79 (sketch of the back wall's flue lattice), Fig 4-82 (photo of the back) | The exit is the back door, bricked up as a lattice with a draw or spy hole at the top (Fig 4-79; pp.109–110). The two chimneys either side of the back door (p.110) show in Fig 4-82 only. Fig 4-79 prints "18"" beside the lattice, along its receding side; whether that is the wall's depth or a brick's length isn't said. | The plan's printed 27' (662 px at zoom 3.5: 2.04 px/in), 12' (275 px: 1.91), 10' (204 px: 1.70) and 4' (68 px: 1.42). **The plan is not to scale.** | — | Chimney sections **not shown**. The back door's width is **not yet measured**: a vertical arrow beside "BACK DOOR" at the plan's far end, its number illegible. Left to do: measure that arrow at 1.4–2.0 px/in and see whether the elevation gives the exit's height. |
| `kitade-tojilo` | p.202, Fig 8-11 (firebox section; front plan; perspective of one chamber, "CHAMBER: 4' WIDE 5' TALL 8' DEEP", "SLOPE 33%") | No chimney, no exit flues, and only one chamber anywhere in the figure. | — | — | **not shown**, so Principle 6's large side applies (inputs §1, §8) |

## 2. Tamba (§9)

### The floor's slope

| Figure | What was fitted | Raw angle | Level lines near the figure | Estimate | Spread |
|---|---|---|---|---|---|
| Fig 4-7, p.85 (a section of the tube; its only printed dimension is the stoke holes' "1½' apart") | The band's lower edge (the floor), 87 columns at zoom 3.2 clear of the two doorways; rms 5.9 px. Local slopes along it are 0.246–0.256. | 14.1° (0.252) | They rise to the right by 0.3–1.6°: the Fig 4-7 and 4-8 captions below it (0.5°, 0.3°) and the text beside it at the same height (1.2–1.6°). | **about 13°** | 12½–14°; rise over run 0.22–0.25, about 1 in 4 |
| Fig 4-17, p.87 (stacking arrangements; no printed dimension) | The hatched floor under the setters, 12 columns between the setters at zoom 3.2; rms 1.2 px, local 9.0–10.3°. The roof line above the stoke hole fits 8.5°. | 9.4° (0.166) | They fall to the right by 0.5–0.8°: the right half of the Fig 4-14 photo's top edge, and the last text line above it. | **about 8¾°** | 8½–9½°; rise over run 0.15–0.17, about 1 in 6½ |

The two figures disagree, so carry them as the band's two ends: **about 8½° (Fig 4-17) to 14°
(Fig 4-7), rise over run 0.15–0.25.** Neither figure is to scale:
- By its "1½' apart", Fig 4-7 draws the tube about 23 in tall, where Fig 4-16 prints 3½ ft for the
  first chamber.
- It also draws two door segments about 8½ ft apart (325 px along the slope at 3.2 px/in). The
  printed 120–150 ft over 6–8 segments gives 15–25 ft each (derived, p.85).

So both angles are the sketches' drawn angles. Fig 4-7 rises to the right and Fig 4-17 to the left;
that is only how they are drawn.

### Stoke holes on Fig 4-7

At zoom 7 the hole centres are 117 px apart horizontally between the dimension's tick lines, and
124–130 px apart along the slope, for the printed 1½ ft: 6.5–7.2 px/in. The holes are drawn
45–55 px wide and 41–43 px tall, so **about 7 in across (6–8½ in)**, scaled. This agrees with the
dataset's Fig 4-16 reading (7–7¼ in round).

### The supporting arches (the flue walls)

The walls are drawn in Fig 4-12, p.86 ("The Tamba tube kiln chamber flues"), measured again here at
zoom 4. One wall crosses the tube with four arched openings. The printed "20 x 12"" sits in opening
1 and "24 x 12"" in opening 2.

| Opening (left to right) | Width, mid-height | Height, floor to the arch's underside | Scaled against | Estimate |
|---|---|---|---|---|
| 1 (outer; its outer side is the vault) | 122 px (149 px at the floor) | 216 px | its printed 20 in height: 10.8 px/in | 11–14 × 20 in |
| 2 (inner) | 146 px | 271 px | its printed 24 in height: 11.3 px/in | 13 × 24 in |
| 3 (inner) | 163 px | 279 px | 11.3 px/in | 14½ × 24½ in |
| 4 (outer) | 128 px | 226 px | 10.8 px/in | 12 × 21 in |

- **Reading:** the labels give the outer pair as 20 in tall × 12 in wide and the inner pair as 24 ×
  12 in, by position. The inner pair is drawn 1.25 times taller than the outer (24/20 is 1.2).
- **Widths:** they scale 11–14½ in against the printed 12 in, about ±1½ in, which is the drawing's
  own spread.
- **Which wall:** the key's two hatchings ("middle chamber flue holes", "last chamber flue holes")
  split the drawing into left and right halves. So which wall each label belongs to stays open, as
  the dataset already has it.
- **Agreement:** this matches the dataset's step A, which scaled from the widths: 12 in wide, the
  outer pair 17–19 in high, the inner pair 21–24½ in high.

**Spacing:** the spacing isn't drawn to scale anywhere (see above). p.86 says "internal chamber
flues before each door are equally spaced", so there is one wall per door segment: 15–25 ft apart
(derived from p.85's 120–150 ft and Fig 4-7's 6–8 door segments).

### The fire mouth while side stoking (handoff §4 question 4; inputs §2)

The book answers this for Tamba:
- p.86: "…firebox becomes the air supply and stoking is done in the upper stoke [holes] and side
  stoke holes". The word before "firebox" is lost in the gutter.
- p.87: "During the firing of the last segment, the firebox and first segment […] almost cool enough
  for unloading. The air for combustion is coming through the firebox, causing tremendously fast
  cooling in the first segment, and the shattering of quite a few pots. When the firing is
  [finished], the exit or chimney flues are plugged and the firebox sealed."

So Tamba fires with its mouth **open** while side stoking and seals it only at the end.

Kitade closes its front, and so does Olsen's own practice:
- p.202, **Kitade Tojilo's kiln** (the built kiln; corrected 2026-11-17 by the main session on the
  page image). The paragraph describes Kitade's side-stoke firebox, with Olsen's own improvements
  set inside it ("If it was a kiln I had built, I would add more smaller-width air holes …"). It
  ends: "When stoking, the space below the stoke hole is closed, allowing air along the front wall
  to be the primary air source. … Care must be taken, however, that the first chamber does not cool
  too quickly. Closing the front is very important." So the book's word for Kitade's mouth is
  closed. This page was first misread as being about Olsen's two-chamber design: that design is
  Fig 8-17, p.206.
- p.206, Olsen's own practice ("Second-chamber firebox"): "In multi-chamber kilns, the main air
  source is from the front of the kiln. Secondary air can come from cracks, doors, etc." Also:
  "…once construction is completed and there is a need for an even air distribution in the chamber
  after the front chamber has been closed down, I use an extruded air tube the width of the chamber
  placed under the grate." The tube's air "is controlled by a shutter on the tube outside the kiln".

## 3. Side stoke holes and separate air inlets (§3)

| Kiln | Pages, figures | Side stoke hole | Separate air inlet (not a stoke hole) | Status |
|---|---|---|---|---|
| Suzuki | p.93, Fig 4-35 (site plan) | A rounded bay on both sides of every chamber, unlabelled: a stoke porch or a hole | none drawn or named | **not scalable**: the plan isn't to scale. Its chambers are drawn 440 × 85–97 px at zoom 3, about 4.8 : 1, against the printed 14 × 4½ ft, 3.1 : 1. |
| Kyoto | pp.89–94, Figs 4-28, 4-31 to 4-34 | Fig 4-34 (p.92) labels three stoke holes, the takaguchi, the aizashiguchi and the mempo ana, and no other opening | none drawn or named | **not scalable**: Fig 4-34 prints no dimension. If the type's 6–7 ft height (Fig 4-28) is taken as its floor-to-crown (567 px at zoom 3), the takaguchi and aizashiguchi are drawn about 3½ × 6 in and the mempo ana about 5 in across. That is too small to pass a bundle, so the drawing is schematic; not a value to use. |
| Tobe | pp.90, 92 | no figure | — | **not shown** |
| Bidai | pp.94–97, Fig 4-36; pp.200–201, Fig 8-7 | Fig 4-36: "(AIZASHIGUCHI) MIDDLE CHAMBER STOKE HOLE 15" UP FROM FLOOR", the hole itself not drawn. The plan draws the far side wall dashed, not cut, over 20 in opposite each chamber's 20 in door; the positions match within about 15 px at zoom 3. It is unlabelled, perhaps a second opening on that side. | None for the chambers. Fig 8-7's "AIR" and "STOKING" openings belong to the main firebox (air into the ash pit, stoking above it), not to a chamber. | hole size **not printed**; the far-side gaps aren't taken as a size |
| Kawaii | p.97, Figs 4-45 to 4-48 (photos) | Fig 4-45: a small hole low on the dogi's side and a small round-headed opening at its base. Fig 4-46: the doorway; its stoke hole can't be told apart in the scan. | none seen | **not scalable**: photos, nothing printed in them |
| Hotchkiss | pp.54–57, Figs 2-39 to 2-46 | Fig 2-44 (p.56), a photo: the pointed-arch stoke hole, about one block wide and two blocks tall with its pointed head. p.56: "stoke holes and spy holes on both sides". | none seen | **not scalable**: the blocks' faces are 5, 9, 10 or 18 in by orientation (p.54), and the photo is oblique. p.57 (Fig 2-46) not viewed. |
| Hollyweird | pp.116–117, Figs 4-108, 4-110 to 4-112 | The side door is drawn at the second firebox in Fig 4-110 (its stoke hole is the recorded 9 × 13½ in). The door itself is about 36 in long (36–40 in, scaled, §7.3, 2026-11-18). | The second firebox's 5 in tube under the grate (p.116; Fig 4-111's caption: "Notice the secondary air-supply tube at the bottom right on the door"), and the front firebox's "air holes at grate level" (p.117) | **not scalable**: Fig 4-111 prints nothing, and Fig 4-112 is too dark to make out the grate-level holes |
| Fujiwara (reference) | pp.99–105 | — | — | **not yet checked** this session |

Olsen's general pages (pp.199–206) give no typical side-hole size in the text. Sizes printed there:
- Kitade's stoke hole 9 × 7 in (p.202, Fig 8-11); Olsen's second-chamber firebox stoke hole
  7 × 7 in (p.206, Fig 8-17).
- The hob firebox (p.203, Fig 8-12):
  - "SECONDARY AIR HOLE (size 4½" X 4½" or 2½" X 9")";
  - "Clean out brick to knock down wood and primary air if needed. 4½" X 4½"";
  - "MOUSE HOLE 2½" X 2½"";
  - "Ash pit fills ½ full of coals – entrance bricked up – secondary air holes built in, as is
    clean out hole".
- p.204: the mouse hole is "a covered channel about 2½in. (6.3cm) square running 12 to 15in. (30.5
  to 38cm) into the ash pit".
- The Sturt chamber kiln (p.205, Fig 8-15): its "STOKE HOLE SIDE" is drawn but not sized. Scaled
  against the printed 6' (199 px at zoom 3: 2.76 px/in) and 45" (140 px: 3.11 px/in), it is **about
  12–13 in tall** (10–15½ in, inner to outer line, both scales). Its width is on the receding side
  wall and can't be scaled.

## 4. The owner's open questions (handoff §4)

- **Q2, Kitade's second chamber:** no figure draws it. Fig 8-11 draws one chamber.
- **Q3, separate side air inlets:** on the pages read, the only inlets that feed a later chamber
  are:
  - Hollyweird's 5 in tube under the second grate (p.116);
  - the tube under the grate in Olsen's two-chamber design (p.206).

  The main fireboxes' own air feeds the first stage, not a chamber's (corrected 2026-11-18, which
  makes the list consistent):
  - Bidai's Fig 8-7 air opening;
  - Hollyweird's air holes at the front grate level (p.117);
  - Kitade's two air-draft and ash-pit holes in the front (p.202).

  None is drawn or named for Suzuki, Kyoto, Tobe, Kawaii or Hotchkiss. Fujiwara wasn't checked.
  Olsen's general statement is on p.206 (quoted in §2 above): the main air comes from the front;
  secondary air from cracks, doors and so on.
- **Q4, the fire mouth:**
  - Tamba is open while side stoking and sealed at the end (pp.86–87).
  - Kitade's front is closed so the first chamber doesn't cool too quickly (p.202).
  - In Olsen's own practice the front chamber is "closed down" and the next chamber's air comes
    through a tube under its grate (p.206).
  - The other kilns' pages read here say nothing.

## 5. Against the dataset and the handoff

1. **Tamba's slope:** `reference_kilns.yaml` and the design take the tube as level ("slope not
   printed"). Scaled here: 8½–14°, the two figures' ends. The owner's estimate for modeling is
   14° (2026-11-17; item 3).
2. **Tamba's fire mouth:** pp.86–87 say the air comes through the firebox while side stoking. So
   the mouth-shut corner (inputs §2) isn't the book's practice for Tamba.
3. **Tamba against the bundle rule:** its bundles are "15 x 30in" (p.87), round, 15 in across and
   30 in long (the owner, 2026-11-18; first written here as 15 × 15 × 30 in from the metric "38 x 38
   x 76cm"), but its side holes scale about 7 in on two figures (Figs 4-7 and 4-16). **Answered (the
   owner, 2026-11-17):** Tamba
   is a whole series of kilns without firm numbers on their differences. The owner's estimates for
   modeling are a slope of **14°** and side holes of **16 in**. So the drawings' 7 in isn't used, and
   the bundle rule holds.
4. **Bidai:** the handoff's §4 Q3 lists "Bidai's air and stoke opening (Fig 8-7)" as a separate side
   air inlet. It is the main firebox's ash-pit air under its stoking opening. The dataset's
   `primary_air` entry already reads it that way.
5. **`anagama-hole`:** the flue scales 4–8 in (about 6), which agrees with the dataset's 4½–7 in.
6. **Tamba's flue walls:** the readings agree with the dataset. The printed labels read by position:
   the outer pair 20 × 12 in, the inner pair 24 × 12 in.
7. **`la-borne`:** the plan's four printed dimensions scale 1.4–2.0 px/in. So the dataset's widest
   station, "about 13 ft from the bag wall, ±14 in", is likely tighter than the drawing allows:
   about ±1½–2 ft.
8. **`kitade-tojilo`:** no chimney or exit flue is drawn, which confirms the plan to take Principle
   6's large side, ¼ of the 48 in width (inputs §8).
9. **Kitade's fire mouth:** p.202 closes the front so the first chamber doesn't cool too quickly.
   Where v2 reports Kitade in all three mouth states (inputs §2), the book's own state is "closed".

## 6. Not yet measured: what is left

- **Fireworks, Fig 7-2 (p.178):** the 9 ft diagonal's pixel length, then the seven gaps and the
  collection box (pixel runs in §1).
- **La Borne, Fig 4-78 (p.109):** the back door's width on the plan, and the exit's height on the
  elevation.
- **Kannofen:** Fig 6-37 against its printed section widths, with the not-to-scale spread; Fig 6-38's
  top flues.
- ~~**Hollyweird, Fig 4-110 (p.116):** the side door's width against the printed 55 in
  platforms.~~ Measured, about 36 in long (§7.3).
- **Fujiwara (pp.99–105):** side holes and inlets.
- **Tamba, Fig 4-10 (p.86):** the tube's section against the pots' printed 13–24 in (p.85).
- **Hotchkiss:** p.57 (Fig 2-46).

## 7. Hollyweird's two chambers (2026-11-18)

The owner, 2026-11-18: "It has two chambers, they are not the same, and they are described." The
dataset (`reference_kilns.yaml`, `hollyweird`) takes its 55 in width and 48 in crown from Fig 8-17
(p.206), a design of Olsen's that was never built. This section scales what Hollyweird's own figures
allow (pp.116–117: Figs 4-108 and 4-110 to 4-114) and says plainly what they don't. It sets no
model value.

**Method.** Pages rendered at zoom 3, about native (the scans are 2173 × 2833 px for p.116 and
2257 × 3037 px for p.117); details read at zoom 4–12.

- **The plan.** Positions are pixels of the crop 0.37–1.0 × 0.66–0.97 of p.116 at zoom 3. x runs
  along the kiln from the chimney (left) to the firebox (right); y runs across it.
- **Drawn lines** are 4–6 px wide. They were read at their darkness-weighted centres on the kiln's
  axis (y about 480). They lean about ½°, which changes no length here by more than 0.01 %.
- **The grey wall bands** (grey about 125; the paper 253) were read where they cross 190. A 9 px
  median filter first takes out the drawn lines and the light flecks.
- **Spreads.** A length's spread is ±5 px (a drawn line's inner to outer edge), plus the spread
  between scales.
- **The photos.** Mortar joints are local minima of smoothed grey profiles. Crops of p.117:
  - Fig 4-114: 0.66–1.0 × 0.55–0.745 at zoom 5;
  - Fig 4-111: 0.12–0.28 × 0.075–0.245 at zoom 6;
  - Fig 4-112: 0.58–0.98 × 0.05–0.31 at zoom 4.
- **Fig 4-108**: crops of p.116 at zoom 3, 0.33–0.72 × 0.25–0.47 (the dimension lines) and
  0.37–1.0 × 0.20–0.47 (the domes).

Scripts: `scratch/hollyweird-1118/` (git-ignored). Every number is an estimate unless it is called
printed.

### 7.1 The plan's scales (Fig 4-110, p.116)

Three labels carry arrows:
- "9" GRATE" points into its grate, about 3 in behind the front rail (x 604.3);
- "15" GRATE" points at its grate's middle (x 881.7);
- "13" WALL" points exactly at the wall's front face (x 972.6).

The 36", 55" and 66" labels have no arrows; each sits over its feature. So each length is read
between the boundaries drawn across the kiln:
- the firebox line (x 1195.8);
- the wall's front face (972.6) and its back face (919.5), which is also the 15" grate's front rail;
- the 15" grate's back rail (847.4);
- the 9" grate's rails (615.2 and 584.3).

| Feature | Figure | What was measured | Scaled against | Estimate | Spread or status |
|---|---|---|---|---|---|
| First ware platform | Fig 4-110 | firebox line to the wall's front face, 223.2 px | the printed 55" | 4.06 px/in | 3.97–4.15 |
| Wall between the chambers | Fig 4-110 | its two faces, 53.1 px | the printed 13" | 4.08 px/in | 3.70–4.47 |
| Second grate | Fig 4-110 | its two rails, 72.1 px | the printed 15" | 4.81 px/in | 4.47–5.14 |
| Second ware platform | Fig 4-110 | the 15" grate's back rail to the 9" grate's front rail, 232.2 px | the printed 55" | 4.22 px/in | 4.13–4.31 |
| Back grate | Fig 4-110 | its two rails, 30.9 px | the printed 9" | 3.43 px/in | 2.88–3.99 |
| **Along the kiln** | Fig 4-110 | the five above together, 611.5 px | the printed 147 in (9 + 55 + 15 + 13 + 55) | **4.16 px/in** | 4.13–4.19; the two 55" platforms 4.06 and 4.22 |
| Front firebox | Fig 4-110 | firebox line to a faint double line across the front (x 1336.5 and 1360; the door bricking?), 140.7–164.2 px | the printed 36" | 4.23 px/in to the double line's middle | 3.91–4.56 (inner or outer line) |
| Back ware platform | Fig 4-110 | the 9" grate's back rail to the last shelf's back line (x 289.5), 294.8 px | the printed 66" | 4.47 px/in | No line marks the platform's end. At 4.16 px/in it ends at x 309.7, 5 in short of that shelf's back edge. |
| Shelves' long sides | Fig 4-110 | the four columns on the two platforms, 87.5–99.5 px | the printed 24 in | 3.65–4.15 px/in | The second platform's 4.14–4.15 agree with the lengths; the first platform's front column is drawn short. |
| **Across the kiln** | Fig 4-110 | the shelves' short sides, 24 readings, 58.5–61.5 px (mean 59.9) | the printed 12 in | **4.99 px/in** | 4.88–5.13 |

**The two scales disagree by 20 %** (4.99 across against 4.16 along). The shelves' 24 in sides agree
with the printed lengths, but their 12 in sides scale a fifth larger. So either the plan is drawn a
fifth larger across than along, or its shelves are drawn a fifth too wide. The plan alone can't say
which.

### 7.2 The chambers' widths (Fig 4-110)

Inside, between the wall bands' inner edges, at both scales:

| Feature | Figure | What was measured | Scaled against | Estimate | Spread or status |
|---|---|---|---|---|---|
| Front chamber | Fig 4-110 | 307.0 px at the wall, 301.5 px at the firebox line | along, 4.16 px/in | 72½–74 in | 71½–75½ |
| | | | across, 4.99 px/in | 60½–61½ in | 59–63 |
| Second chamber, from the 15" grate to the 9" grate | Fig 4-110 | 306–310 px | along | 74 in | 72½–76½ |
| | | | across | 61½–62 in | 59½–63½ |
| Front firebox, at the front | Fig 4-110 | 220–222 px between the walls' curved ends | along / across | 53 in / 44 in | 52–54½ / 43–45½ |
| Throat into the chimney | Fig 4-110 | 129–132 px, straight for about 73 px | along / across | 31 in / 26 in | 30½–32½ / 25–27 |
| Chimney box, inside | Fig 4-110 | 79.5 px along × 206.4 px across, beside the label "15 X 24" | along / across | 19 × 50 in / 16 × 41 in | Not drawn to the printed 15 × 24 in. The label sits in the throat, which scales 15–17½ in long and 26–31 in wide. |

At the shelves' 24 in sides (3.65–4.15 px/in), the chambers would be 73–85 in wide.

What the drawing holds:
- **Across:** four rows of 12 × 24 in shelves, their 12 in sides across. The gaps between rows are
  13–17 px and the clearances at the walls 11–14½ px. At the shelves' own scale the gaps are
  2½–3½ in and the chamber is about 62 in wide. At the along scale the same shelves would be 14–15 in
  wide.
- **Along:** two 24 in shelves and three gaps of 9–17 px (2–4 in) fill each 55" platform. That fits
  the along scale.
- **So:** the content fits 60–63 in only if the shelves are drawn to their printed 12 in across. The
  printed lengths make the same drawn width 73–76 in.
- **Neither reading is 55 in.** That would need 5.6 px/in across, 12 % above the shelves' scale and
  35 % above the lengths' scale.

**Stations: the second chamber and the back platform's taper.** Each station is given in inches behind
the wall's back face (the second chamber's front, 104 in from the kiln's front). Up to the 9" grate's
back rail (79 in) the inches come from the printed lengths; behind it, from 4.16 px/in.
- Widths are ±3 px (about ±¾ in), plus the scales' spreads above.
- Stations are about ±1 in up to the 66" platform's start, and about ±2–3 in behind it (the
  scales 4.06–4.22).

| Behind the wall's back face (in) | Where | Inside (px) | At 4.16 px/in (in) | At 4.99 px/in (in) |
|---|---|---|---|---|
| 0 | the wall's back face; the 15" grate begins | 308 | 74 | 62 |
| 15 | the second platform begins | 308 | 74 | 62 |
| 43 | the platform's middle | 307 | 74 | 61½ |
| 70 | the 9" grate begins | 310 | 74½ | 62 |
| 79 | the 66" platform begins | 309 | 74½ | 62 |
| 92 | the shelf column behind the 9" grate | 310½ (±2½) | 74½ | 62 |
| 104 | | 305 | 73 | 61 |
| 111 | the taper begins | 300½ | 72 | 60 |
| 116 | | 297 | 71½ | 59½ |
| 121 | | 286½ | 69 | 57½ |
| 126 | | 272 | 65½ | 54½ |
| 131 | | 253½ | 61 | 51 |
| 135 | | 234 | 56½ | 47 |
| 140 | | 215½ | 52 | 43 |
| 145 | the 66" platform's end, at 4.16 px/in | 194 | 46½ | 39 |
| 150 | the last shelf's back line | 170 | 41 | 34 |
| 155 | | 151½ | 36½ | 30½ |
| 159 | | 137 | 33 | 27½ |
| 163–179 | the throat | 129–132 | 31–31½ | 26–26½ |
| 180½–199½ | the chimney box, inside | 206½ across | 50 | 41½ |

### 7.3 The exit flues, the piers and the side door

| Feature | Figure | What was measured | Scaled against | Estimate | Spread or status |
|---|---|---|---|---|---|
| The three exit flues | Fig 4-110 | three outlined openings in the wall's column, measured across the kiln: top 65.9 px, middle 67.7, bottom 59.4, clear of the outlines (68.4, 73.0 and 62.6 to the outlines' centres) | settled on the shelves' 12 in sides, 4.99 px/in: the only printed dimension drawn across | **about 12–14 in each**: top 13–14, middle 13–15, bottom 11½–13 | 11½–15 in, scaled. At the along scale they would be 14–18 in. |
| The two piers between them | Fig 4-110 | hatched squares, 46–59 px (inner to outer outline) | 4.99 px/in | about 10–11 in | 9–12 in (11–14½ at the along scale) |
| The flues in a photo | Fig 4-114 (the wall with three openings, shelves set in them) | at zoom 5: the left opening 225 px (beside a 38 px return at the side wall's corner), the middle 236 px, the piers 153 and 148 px; the right opening runs off the photo's edge | standard brick, 18.5–20.7 px/in (§7.5) | flues **about 12 in** (11–13); piers 7–8 in | Scaled. The photo's piers are narrower than the plan draws them: the plan's flue-to-pier ratio is 1.1–1.2, the photo's about 1.6. |
| The wall's inside width at the flues | Fig 4-114 | from the left corner to the photo's edge, at least 1062 px | standard brick, as above | at least 51–57 in | If the right flue and its return mirror the left, about 51–58 in. Not established: the right corner is out of frame. |
| Side door | Fig 4-110 | a gap in the side wall, 161.3 px long (x 754.3–915.6). It starts at the wall's back face, crosses the 15" grate and runs 22 in into the second platform. | the printed lengths | **36 in** (14 over the grate, 22 on the platform); 39 in at the overall 4.16 px/in | 36–40 in, scaled. Answers §6's Hollyweird item. |

### 7.4 The steps (Fig 4-110)

Each "STEP" label's arrow stops below the side wall. A separate dark arrowhead sits inside the wall
band, 15–40 px from it. Each pair falls within 2–7 in of a line drawn across the kiln. The plan
doesn't say which way a step goes.

| Step | Label's arrow | Arrowhead in the wall | Sits at (inches from the kiln's front, by the printed lengths) |
|---|---|---|---|
| 12" | x 1166.4: 43 in | x 1181.0: 40 in | the firebox line (36 in): 4–7 in behind it, at the first platform's front shelves |
| 18" | x 889.4: 110 in | x 929.0: 102 in | the wall's back face, where the 15" grate begins (104 in): from 2 in in front of it to 6 in behind |
| 6" | x 599.0: 179 in | x 624.0: 172 in | the 9" grate's front rail (174 in): from 2 in in front of it to the grate's middle |

### 7.5 Front chamber against back chamber; the heights

**In plan, the chambers are the same.**
- The side walls run straight and parallel through both chambers. Inside they stay 301½–310½ px
  from the back platform's full-width part to the firebox line, within 3 %.
- Neither chamber is drawn wider or rounded. Only the firebox's walls curve in, to its 221 px front,
  and only the back platform tapers.
- The front chamber narrows about 5 px (1 in) toward the firebox line. That is close to the
  drawing's own ±3 px.

**In elevation, the front is drawn taller and rounder.** Fig 4-108 draws the front dome as a high
round dome and the back as a lower vault. It is a perspective sketch, and nothing in it scales a
height.

| Feature | Figure | What was measured | Scaled against | Estimate | Spread or status |
|---|---|---|---|---|---|
| Both domes' crowns and springlines | Fig 4-108 (perspective) | the front dome about 440 px from its base band to its silhouette's top (zoom 3); the back dome 210–265 px | the 12' (395 px: 2.74 px/in) and the 8' (422 px: 4.40 px/in), 60 % apart | — | **not scalable**: on the 12' or the 8' the front dome would stand 100–160 in. Drawing only: the front dome is drawn 1.7–2.1 times the back's height, against the sketch's own perspective enlargement of about 1.6, so it shows the front somewhat taller. |
| The "55"" and a "10" (?) | Fig 4-108 | "55"" is written across the kiln at the 8' line's front end. Beside it a short arrow (about 100 px) runs from the ground to the front dome's base on the near side, with a faint mark that may read "10" (?); at zoom 12 the mark is a loop crossed by the shaft. | — | — | **not scalable**: the arrow doesn't span the front, so the 55" isn't drawn as the front's width |
| The 12' and the 8' | Fig 4-108 | the extension line at their junction runs to the side door's base, near its front end | — | — | **drawing**: the split is at the side door. On the plan the door starts at the wall's back face, 104 in from the front, with 145 in of printed length behind it. |
| Side door's height | Fig 4-111 (photo, side) | a white block in the door's bricking, 100 × 154 px at zoom 6 (proportions 0.65); the bricked width 420–500 px | the 9 × 13½ in stoke hole, if the block is it (the dataset's reading of 2026-11-17 puts that hole in the side door): 11.1–11.4 px/in. The plan's 36–39 in door gives 10.8–13.9. | if so, the bricking stands 50–73 in from its lowest visible course to its top, and the arch's outline 76–89 in above that course | **not scalable**: the block's identity isn't printed, the sill and the bricking's top are only ±40 px, and the domes' crowns aren't in the door's plane. The caption's air tube is a dark hole 47–66 × 76 px, too ragged to scale. |
| Front dome | Fig 4-112 (photo, front) | the one clear opening in the door bricking, 133 × 93 px at zoom 4 (proportions 1.43), in a lighter frame 215 × 170 px (1.26) | as the 13½ × 9 in stoke hole, 9.9–10.3 px/in; as the frame of the 18 × 15 in inlet flue, 11.3–11.9 | the dome's silhouette 34–50 in above the opening | **not scalable**: either printed opening fits; the lower half (the grate-level air holes, the floor) is too dark; the crown isn't in the face's plane |
| First chamber | Fig 4-113 (photo, inside) | the far wall's courses, 31–50 px apart at zoom 5, irregular; its corners not found | — | — | **not scalable** |
| Brick above the flues | Fig 4-114 (photo) | from the middle flue's top (y 445 at zoom 5) to the castable's lower edge (about y 155): five courses at 52.2 px and a thin top row, 285–295 px | standard brick, 9 × 4½ × 2½ in, laid flat in alternate header courses (90.4 px pitch) and stretcher courses (184.5 px), joints ⅛–¼ in (the three pitches agree best there): 18.5–20.7 px/in | **about 15 in** | 14–16 in, scaled. The flues' bottoms and the floor can't be read, so this gives no springline. |

So **no figure scales either chamber's crown or springline**. Fig 4-108 draws the front taller and
rounder than the back, by an amount it doesn't scale.

### 7.6 Against the dataset (`hollyweird`)

1. **Width.** The dataset assumes 55 in (from Fig 8-17). The plan draws both chambers the same
   width, 60–63 in at the shelves' scale or 73–76 in at the printed lengths' scale, not 55. Fig 4-114
   shows at least 51–57 in of the face of the wall between the chambers, and about 51–58 in if its
   hidden right side mirrors the left.
2. **Heights.** The span (55), rise (12.6), springline (35.4) and crown (48 in) all follow from the
   borrowed 55 in and Fig 8-17. No Hollyweird figure scales a height (§7.5).
3. **The 8 ft and the 12 ft.** The notes split the plan at the wall's front face (91 and 158 in).
   Fig 4-108's junction points at the side door instead, whose front end is the wall's back face.
   That puts 104 in in front and 145 in behind. The 12' fits 145 in. The 8' is 8 in short of 104,
   which includes the 36 in firebox and the 13 in wall.
4. **Length 249 in.** The printed lengths end at the 66" platform's end, partway down the taper.
   Behind it the plan draws:
   - 31–36 in more of neck and throat, to the chimney box;
   - the box itself, 16–19 in inside.

   From the front to the chimney's back inside face that is about 25 ft (300–312 in) at the along
   scale.
5. **Exit flues.** The dataset has 11–13 in, from step A with the 55 in width. The plan gives
   11½–15 in (about 12–14) at the shelves' scale and 14–18 in at the along scale. The photo
   (Fig 4-114) gives about 12 in (11–13), against brick.
6. **Chimney 15 × 24 in.** The box isn't drawn to its label: 19 × 50 in or 16 × 41 in at the two
   scales. The label sits in the throat, which scales 15–17½ × 26–31 in. Which of the two the label
   names isn't certain.
7. **Wall thickness.** The dataset assumes 9 in; the book prints none. The plan's side walls are
   drawn 70–81 px thick: 14–16 in at the shelves' scale, 17–19½ in at the along scale. Plan bands
   may be schematic.
8. **Front firebox.** The design has 55 × 36 in. The plan's firebox is 36 in long (printed).
   - At the firebox line it is as wide as the chamber.
   - It curves in to a front opening of 44 in (shelves' scale) or 53 in (along).
   - Its grate box is drawn 138 × 79 px: about 33 in long and 16–19 in wide.
9. **Shelves.** The dataset reads "12 × 24 in, one 12 × 18 in". Five shelves behind the 9" grate
   (three across, two in the neck) are drawn about square, 83–86 × 81–96 px: about 16–21 in a side
   at the two scales. The faint label on one of them reads "12X18" (?), which its drawing doesn't
   show.

## 8. Hollyweird rescanned: the heights (2026-11-18)

The owner, 2026-11-18, after §7:
- "The front dome is taller, so the back chamber should be less and go down. It tapers to the
  chimney as shown."
- "Use the wide part of the brick in figure 4-109 as 9" and scale that to check the height. Rescan
  that whole section to learn about the dimensions. It is not a simple kiln."
- "15" x 18" is an air inlet, also there are air holes at the grate level in addition. The air inlet
  holes are in the doors."
- "Use the drawn side walls of 14-19"."

This section rescans pp.116–117 (the text and Figs 4-108 to 4-115) for heights. Each is scaled
against a standard brick (9 × 4½ × 2½ in, joints ⅛–¼ in) in the plane being measured, or against
a printed size in that plane. It sets no model value, and it leaves the dataset and the design file
alone. Every number is an estimate; the only printed ones are named as printed.

**Method.** Pages rendered with pymupdf. Positions are pixels of these crops (page fractions):
- Fig 4-109: p.116, 0.06–0.37 × 0.60–0.96, zoom 6.
- Fig 4-108: p.116, 0.36–1.0 × 0.23–0.48, zoom 3 (as §7).
- Fig 4-111: p.117, 0–0.48 × 0–0.34, zoom 4.
- Fig 4-112: p.117, 0.46–1.0 × 0–0.31, zoom 4.
- Fig 4-113: p.117, 0.66–1.0 × 0.315–0.53, zoom 5.
- Fig 4-114: p.117, 0.66–1.0 × 0.55–0.745, zoom 5 (as §7).

How the readings were made:
- Joints are local minima of smoothed grey profiles. The photos are posterised, so a joint is
  ±3–5 px. Edges are threshold crossings. Silhouettes are the first light run under a dark
  background.
- Views were made at zoom 6–12 with a light blur and local contrast. Dark areas were brightened
  with a gamma.
- Heights in a plane are read along the vertical. In Figs 4-109, 4-113 and 4-114 the courses,
  lintels and sills are level within about 1°, so no tilt correction changes a height by more than
  1 %.
- A crown or ridge set back behind the plane being scaled appears lower than it is when the camera
  is below it. Each such row says how much the setback allows.

Scripts: `scratch/hollyweird-1118b/` (git-ignored); `compute.py` there holds the arithmetic.

### 8.1 Which way each photo looks

- **Fig 4-109** (p.116, bottom left): the front, nearly square on. The door bricking is on the
  left, with a 9 in high opening by Olsen's hand. The cast dome is above, and a metal hood hangs from
  hooks over the front.
- **Fig 4-111** (side view): taken from the side door's side, with **the front to the right**.
  Three things fix it:
  - The caption's air tube is the dark hole at the door's bottom right.
  - p.116 puts the tube under the second grate, and the plan puts that grate (104–119 in from the
    front) at the door's front end (§7.3).
  - Fig 4-108 is drawn from the same side, with the front dome on the right.

  So the large mass on the left, nearest the camera, is the back chamber. Beyond the door, the
  buttress and the long vault falling to the right are the front dome, which curves down to its
  front end at the photo's edge.
- **Fig 4-112:** the front from the front-left, dark in its lower half.
- **Fig 4-113:** from the firebox, square on to the wall between the chambers, with its three
  flues. The near left frame is the front door's jamb, curving into the door's arch at its top.
- **Fig 4-114:** the same wall from close in, with shelves set in the flues. Which face it shows
  isn't certain (§8.5).
- **Fig 4-115:** an arched opening with a cast crown block bearing two horn-like ornaments, a
  brick ring, two light blocks on a ledge and a dark opening below them, with the stoker kneeling
  in front. Nothing in it is a known size.

### 8.2 The brick scale on the front (Fig 4-109)

| Feature | Figure | What was measured | Scaled against | Estimate | Spread or status |
|---|---|---|---|---|---|
| The brick's long face | Fig 4-109 | the large white brick in the top course left of the opening: light face 199 px long (x 177–376); 205 px from the head joint on its left to its right end (rows 1100–1160) | the owner's 9 in (9⅛–9¼ in joint to joint) | **22.1–22.5 px/in** | 21.4–23.1 for ±3 px at each end. Scaled. |
| The courses | Fig 4-109 | the five bed joints under that brick (y 1172, 1236, 1302, 1365, 1425 ±5): four courses, 63.2–64.3 px each | 2½ in + ⅛–¼ in joint | 23.0–24.5 px/in | 3–10 % above the brick's scale. Scaled (cross-check). |
| That brick's height | Fig 4-109 | its face 75–85 px tall | the two scales | 3–3¾ in | not a 2½ in stretcher course: a 3 in brick (an IFB?) or a piece of another size; the book doesn't say |
| The half-length units below | Fig 4-109 | units 90–125 px long in courses C–D | — | — | headers or bats; too irregular to use |
| **Adopted** | Fig 4-109 | the brick and the courses together | | **22.1–24.5 px/in at zoom 6** | about ±5 % |
| How square the plane is | Fig 4-109 | the courses, lintel and sill are level. The course pitch holds within about 10 % from the steel post on the left to the jamb bricks beside the opening. The steel post leans 2½–3° against the photo's edge. | — | — | Close to square on. The lean fits a camera tipped down about 10° (for a 35–50 mm lens at 8–11 ft), which changes the scale a few per cent between the sill and the dome. |

### 8.3 The front's heights (Figs 4-109 and 4-112)

The ground at the front isn't seen. Below the lowest joint (y 1665) the photo goes uniformly dark
down to Olsen's feet: either the lower front in shadow or the ground. So each height is given above
the opening's sill, a sharp line in the plane (y 1288), and then above two possible bases.

| Feature | Figure | What was measured | Scaled against | Estimate | Spread or status |
|---|---|---|---|---|---|
| The opening | Fig 4-109 | dark from the lintel's underside (y 1075) to the sill's top (y 1266–1289), 190–213 px. 167–180 px of its width shows; the rest is behind Olsen. | brick, 22.1–24.5 px/in | **7¾–9½ in tall**, at least 7–8 in wide | Scaled. It is the 9 in side of the printed 9 × 13½ in stoke hole, laid 13½ in across. The 15 × 18 in inlet would be 332–441 px tall. |
| Its frame | Fig 4-109 | a thin light lintel and sill, about 20 px each; lintel top to sill bottom 254 px | brick | 10½–11½ in overall | Scaled. Each piece is about ¾–1 in: kiln shelf or steel angle, not said. |
| The springing | Fig 4-109 | the castable's lower edge on the left, where the brick courses stop (y 1080–1095) | brick | **8–9½ in above the sill**, level with the opening's top | Scaled, as the castable's edge. That it is the arch's springing is a reading. |
| The door bricking's top | Fig 4-109 | the castable's lower edge rises to the right from the large brick's end, at about 45°; at x 560 it is at y 865 ±15 before Olsen's arm covers it | brick | at least 16½–20 in above the sill | Scaled. The arch's crown (the bricking's top) is hidden. |
| The steel post's top | Fig 4-109 | y 955 | brick | 13½–15 in above the sill | Scaled |
| The hood's bottom | Fig 4-109 | y 455 | brick | 34–37½ in above the sill | Drawing: the hood hangs in front of the plane, so it is a little lower than this. |
| The dome's silhouette | Fig 4-109 | its top at y 390 ±10, left of the hood | brick, at the front's plane | **36–41 in above the sill** | Scaled as apparent. The post's lean puts the horizon near Olsen's eyes (y 565 ±150), so the silhouette is 25–325 px above the eye. A crown set back by 0.1–0.5 of the camera's distance then stands 0–7½ in higher: **36–48 in above the sill**. Had the camera been level, the eye would be at the photo's middle and the setback could add up to about 15 in. |
| The dome's silhouette | Fig 4-112 | the stoke hole 126 × 94 px (ratio 1.34, the 13½ × 9 in seen obliquely); the silhouette 535 px above its sill | the stoke hole's printed 9 in, 10.4 px/in at zoom 4 | about 51 in above the sill | Scaled as apparent, from another viewpoint. The two silhouettes differ by 10–15 in; the method's own spread. |
| The lowest joint seen | Fig 4-109 | y 1665 (bricks show to y 1550, a weak joint at 1663–1667) | brick | 15½–17 in below the sill, about six courses | Scaled. The bricking may go lower in the dark. |
| Olsen | Fig 4-109 | hair to soles about 1645 px; his soles 772 px below the sill | brick | 67–74 in if he stood in the front's plane | Rough check only (no printed height). For a man of 5 ft 4 in–5 ft 8 in he stands within one to two feet of the front. The ground at the front is then near his feet, **22–35 in below the sill**, not at the lowest joint. |
| **Heights above the lowest joint seen** | Fig 4-109 | as above | brick | sill 15½–17; opening's top 24–26½; springing 23½–26; the bricking's edge at x 560 32½–36; **the dome's silhouette 52–58 in** (to about 65 with the setback) | Scaled, above a line that may not be the ground |
| **Heights above a ground at Olsen's feet** | Fig 4-109 | as above, with the ground 22–35 in below the sill | brick and the Olsen check | sill 22–35; **the dome's silhouette 59–76 in** (to about 83 with the setback) | Rough. The ground isn't seen. |

So the front dome's outside top is about **36–48 in above the stoke hole's sill**. Above the ground
it is 52–83 in. The sill's own height above the ground (15–35 in) carries most of that spread.

### 8.4 The openings in the doors

| Feature | Figure | What was measured | Scaled against | Estimate | Spread or status |
|---|---|---|---|---|---|
| Front: the stoke hole | Figs 4-109, 4-112 | §8.3 | brick (4-109) | 9 in tall, more than 7–8 in wide | Scaled. It matches the printed 9 × 13½ in (p.117), with the 13½ across. |
| Front: the 15 × 18 in inlet | Fig 4-109 | no second opening is seen. Below the sill on the right (x 560–800, y 1310–1612) the grey (mean 117–151) is lighter than the stoke hole's interior (78–86) and darker than the bricks (168–235), with no courses seen. | — | — | **Not found** in 4-109. It may be behind Olsen's body, which hides 13–14 in to the opening's right. |
| Front: a framed structure low down | Fig 4-112 | a light frame 140 × 215 px; its top 180–210 px below the stoke hole's sill; light blocks inside with dark gaps 20–40 px high | the stoke hole's 9 in, 10.4 px/in | about 13½ × 20½ in; its top 17–20 in below the stoke hole's sill; the gaps 2–4 in high | Drawing, as the plane isn't known. It could be the 15 × 18 in inlet partly bricked, the grate-level air holes, or loose brick in front of the door; the photo can't tell. |
| Front: the grate-level air holes | Figs 4-109, 4-112 | — | — | — | Not identified, unless they are the gaps above |
| Side door: the air tube | Fig 4-111 | the dark hole at the door's bottom right: 50–62 px across (100–124 px at zoom 8) | the printed 5 in tube (p.116), if the hole is its end | 10–12½ px/in at zoom 4 at the door's base | Scaled, on that condition. The tube's bore would be smaller than 5 in and a hole round it larger, so this scale is ±20 %. |
| Side door: the white block | Fig 4-111 | 68 × 100–108 px (x 1209–1344, y 1059–1275 at zoom 8; a vertical joint divides it), set in a dark recess, high in the door bricking | the tube, 10–12½ px/in | 5½–7 × 8–11 in; its sill 27–33 in and its top 35½–44 in above the door's base | Scaled, on the tube. That is smaller than 9 × 13½ in. The block is the 9 × 13½ in stoke hole only if the dark hole is 6–8½ in across, a hole round the tube. |
| Side door: its height | Fig 4-111 | the brick ring's top (y 345) above the door's base (y 940–1000) | the tube | 48–65 in | Scaled, on the tube |
| Side door: a small bricked recess | Fig 4-111 | in the right jamb, low (x 1390–1520, y 1580–1700 at zoom 8), outlined by joints | — | — | Drawing. Perhaps a plugged opening; not identified. |

The book puts the 15 × 18 in inlet, the stoke hole and the grate-level air holes "into the door
bricking" (p.117), and the 5 in tube through the ash-pit side wall at the side door (p.116). The
photos show the front's stoke hole and the side door's tube; neither shows the 15 × 18 in inlet for
certain.

### 8.5 The wall between the chambers and its three flues (Figs 4-113 and 4-114)

| Feature | Figure | What was measured | Scaled against | Estimate | Spread or status |
|---|---|---|---|---|---|
| The far wall's scale | Fig 4-113 | stretchers above the flues: head joints 101.4 px apart (rows 218 and 250); courses 31.1 px (bed joints 204–328) | 9⅛–9¼ in; 2⅝–2¾ in | 11.0–11.1 and 11.3–11.85 px/in | Scaled. Adopted 11.0–11.85 px/in at zoom 5. |
| The camera's eye and the floor | Fig 4-113 | the ceiling's two side edges converge at y 665–765, at or just below the wall's lowest course (its foot at y 658 ±6). Below that foot a light band begins at once (y 664, no joint between), with a joint at y 728–736. | — | the eye is at about the first chamber's floor | Drawing. The band reads as that floor seen nearly edge-on, then the step's face. So the wall's visible foot is its foot on the floor, within a few inches. |
| Where the castable meets the wall | Fig 4-113 | the top course's top (y 172.5) above the visible base: 486 px, 15½ courses | brick | **41–44½ in** | Scaled, above the visible base (about the floor) |
| The flues' sills | Fig 4-113 | the three openings' bottoms, y 461–473 | brick | **15½–18 in above the visible base** | Scaled |
| The flues' tops | Fig 4-113 | y 343, all three | brick | 26½–29 in | Scaled |
| The flues' height | Fig 4-113 | 118–130 px | brick | **10–12 in** | Scaled |
| Brick above the flues | Fig 4-113 | y 343 to 172.5, 5½ courses | brick | 14½–15½ in | Scaled. It agrees with Fig 4-114's 14–16 in (§7.5). |
| The middle flue's width | Fig 4-113 | 105–142 px (the edge on its left is in shadow) | brick | 9–13 in | Scaled. The side flues show only 68 and 83 px (6–7½ in) through the 13 in wall at an angle. |
| **The chamber's width at the wall** | Fig 4-113 | 600 ±30 px between the corners, where the ceiling's side edges meet the top course (x 460 and 1060) | brick | **about 53 in** | **48–57½ in, scaled.** The flues and piers fill 579 px of it (49–53 in), as Fig 4-114 shows the left flue against the side wall's corner (§7.3). |
| The floor in Fig 4-114 | Fig 4-114 | the wall's base at y 905–912. The courses below the flues are 59–62 px, against 52.2 above (§7.5): the scale grows downward (the camera tipped up). | brick, 21.6–23.5 px/in low, 18.5–20.7 high | — | Scaled |
| The flues in Fig 4-114 | Fig 4-114 | bottoms y 655–745 (the middle one 717, dark under its shelf); tops y 440–480; the middle flue 475–717, 242 px; its shelf at y 607–652 | brick | bottoms 7–11½ in, tops 19–24 in above this floor; the middle flue 11–12 in tall, its shelf 11–14½ in up | Scaled |
| The castable in Fig 4-114 | Fig 4-114 | 725 px above the floor; 13 courses counted (4 above the flues, about 5½ at the flues, 3 below and a part course) | brick | 31–39 in; **34–36 in** by the count | Scaled |
| Which face Fig 4-114 shows | Figs 4-113, 4-114 | the flues stand 5–11 in lower above Fig 4-114's floor than above Fig 4-113's base | — | — | Not settled. Either the back face, whose floor (the second firebox's side) is that much higher, or the front face with fill on its floor. |

### 8.6 The back chamber, its height and its fall (Figs 4-108 and 4-111)

| Feature | Figure | What was measured | Scaled against | Estimate | Spread or status |
|---|---|---|---|---|---|
| The front dome in the sketch | Fig 4-108 | at its crown (x 940): from the base band's bottom (y 572) to the outline's top (y 27), 545 px | — | the reference for the rows below | Drawing |
| Just behind the side door | Fig 4-108 | x 450: top y 94, base 395–425; 301–331 px | the front dome's crown | 0.55–0.61 of the front's height as drawn; **0.69–0.94** allowing the perspective | Drawing. The 12' is drawn at 2.78 px/in along and the 8' at 4.35 (1.56 times). Heights were scaled up by 1.25 (as the square root of that ratio) to 1.55 (as the ratio). |
| Mid-way | Fig 4-108 | x 400: top y 101, base 390–420 (under a glare spot); 289–319 px | as above | 0.53–0.59 as drawn; **0.66–0.91** | Drawing |
| The chimney end | Fig 4-108 | x 340, just in front of the chimney's lines: top y 114, base 385–415; 271–301 px | as above | 0.50–0.55 as drawn; **0.62–0.86** | Drawing |
| In inches | Fig 4-108 | the three rows times the front's outside top | the front: 52–64 in above the lowest joint, or 59–83 in above the Olsen-check ground (§8.3) | the back's top 26–60 in, or 30–78 in | Not scalable to better than this: the sketch's perspective and the front's base both spread it |
| The fall toward the chimney | Fig 4-108 | the chimney end is drawn 0.82–1.00 of the height just behind the door | the sketch's own scale along the 12 ft | 1.16–2.0 once the far end's smaller drawn scale is allowed | Not scalable. The chimney end is drawn at about half the door end's scale if the along-scale changes smoothly from the 12' to the 8'. So the sketch can't show a fall: it fits a level back as well as a falling one. |
| The front against the back | Fig 4-111 | the front dome's top (y 340–365) stands higher than the back's (y 380–390) although it is farther away. Its base-wall courses are 64–73 px, against about 107 px on the back's side face: the back is about 1.5 times nearer. | — | the front is taller, as the owner says | Drawing. How much taller isn't scaled. The camera's eye is at about both tops: the front's base courses converge to a horizon at y 300–440. |
| The back's fall | Fig 4-111 | the back's silhouette falls about 125 px from beside the door (x 450, y 345) to the photo's left edge (x 100, y 470), toward the chimney | — | — | Not scalable. The near vault's own curve and the perspective can't be told from a fall. |
| The front dome's base courses | Fig 4-111 | 64–73 px a course (x 1000–1300), 2 courses showing above the debris | 2⅝–2¾ in | would be 25–27 px/in, making the dome about 1½ ft tall | Not standard 2½ in courses: bricks on edge, soldiers or blocks of a size not printed. No height scales from them. |
| The chimney | Fig 4-108 | two vertical lines rising about 100 px above the back vault's end (x 200 and 330, y 40–150) to the sketch's top edge, where the text begins | — | — | **Not scalable.** No photo shows the chimney, and the sketch's lines run out of the figure. |

The plan's taper (§7.2) narrows the back from 72–74 in (along scale) or 60–62 in (shelves' scale)
at 111 in behind the wall's back face to 26–31 in at the throat. If the back's section kept its
proportions, its height would fall with its width. No figure measures that, so it is not taken here
as a height.

### 8.7 Walls, steps, floors, grates, castable and spy holes

| Feature | Figure | What was measured | Scaled against | Estimate | Spread or status |
|---|---|---|---|---|---|
| Side walls' thickness | Figs 4-111, 4-113 | No wall end shows square on with a scale. Fig 4-113's near left jamb (the front door's) is about one block wide, its blocks 120–170 × 240 px at zoom 6. Fig 4-111's door ring is 40–50 px deep (3¼–5 in on the tube's scale): a 4½ in ring, not the wall. | — | — | **Not scalable.** The plan's 14–19½ in (§7.6 item 7) stands, as the owner asks. |
| The castable's thickness | all | no edge of the castable shows square on | — | — | **Not scalable**; the dataset's 6 in stays assumed |
| The 12 in step | Fig 4-110; p.117; Fig 4-113 | at the firebox line (§7.4). p.117: "Access to the chamber is through the firebox using the ash pit as a walkway". Fig 4-113's eye, taken in the firebox, is at about the first chamber's floor. | — | up from the ash pit to the first chamber | A reading, not printed. The photos fit it. |
| The 18 in and 6 in steps | Fig 4-110 | at the wall's back face and at the 9 in grate (§7.4) | — | — | **Direction not printed or shown** |
| The second grate | p.116; Fig 4-113 | the flues give "air from under and over the grate" (p.116), so the grate lies within the flues' height | the flues in Fig 4-113 | 15½–29 in above the first chamber's floor | Derived from the text and the scaled flues. Fig 4-114's shelves (11–14½ in above its floor) may rest at that level; not shown. |
| The front grate | Figs 4-109, 4-112 | not seen; the stoke hole's sill is 15½–17 in above the lowest joint and 22–35 in above the Olsen-check ground | — | below the sill, height not shown | Not scalable |
| Spy holes | Figs 4-108, 4-111 | Fig 4-108 draws three round holes: one in the back vault, two in the front dome. Fig 4-111 shows a dark round hole about 60 px across in the front dome's side above the buttress by the door. | the tube's scale at the door (the hole is farther) | 5–6 in across or more | Drawing; the size isn't printed |

### 8.8 Against §7 and the dataset (`hollyweird`)

1. **Width.** The dataset has 61 in (59–63½), from the plan's shelves.
   - Fig 4-113 scales the wall between the chambers **48–57½ in wide, about 53 in**, against its
     own stretchers and courses.
   - That agrees with Fig 4-114's at least 51–57 in (§7.3), and with the sketch's "55"" written
     across the front end (§7.5).
   - The plan would then be drawn 5.3–6.4 px/in across, above both of §7.1's scales.
2. **§7.5 found no figure that scales a height.** Fig 4-109 now scales the front against its brick,
   and Fig 4-113 the wall between the chambers against its own:
   - The front's castable meets that wall 41–44½ in above the first chamber's floor.
   - The front dome's outside top is 36–48 in above the front stoke hole's sill.
3. **§7.5, Fig 4-112: "either printed opening fits".**
   - At Fig 4-109's brick scale the front opening is 7¾–9½ in tall: the 9 in side of the 9 × 13½ in
     stoke hole.
   - Its frame is 10½–11½ in, so the "frame of the 15 × 18 in inlet" reading is out.
4. **§7.5, Fig 4-113: "not scalable".** It is scaled now (§8.5).
5. **The assumed heights.** The dataset assumes crown_height 61 in, springline_height 47 in and
   dome_rise 14 in.
   - The castable starts 41–44½ in above the floor at the wall between the chambers, 2½–6 in below
     the assumed springline. That is the front dome's end wall; its side springline isn't seen.
   - The front's top is tied to the front stoke hole's sill (36–48 in above it). The sill's height
     above the chamber's floor isn't known, so no crown above the floor is scaled.
6. **The flues' height** (a gap in the dataset, and "their height isn't drawn"):
   - Fig 4-113: 10–12 in tall, the sills 15½–18 in above the first chamber's floor.
   - Fig 4-114: 11–12 in.
   - The second grate then lies 15½–29 in above that floor.
7. **The side door's white block.** §7.5 took it as the 9 × 13½ in stoke hole (11.1–11.4 px/in at
   zoom 6).
   - The air tube's end gives 10–12½ px/in at zoom 4 (15–18½ at zoom 6) and makes the block
     5½–7 × 8–11 in.
   - The block is the 9 × 13½ in hole only if the dark hole is 6–8½ in across. The dataset's side-door
     stoke hole (the owner's reading, 2026-11-17) is neither confirmed nor ruled out.
8. **The front's height in the gaps list.** The front dome's outside top is 52–58 in above the front's
   lowest visible joint, and about 59–76 in above a ground near Olsen's feet (setback not included).
   The ground isn't seen.
9. **The back's height and fall** stay unscaled.
   - Fig 4-108 draws the back at 0.5–0.6 of the front dome's height, 0.6–0.9 with its perspective
     allowed. It can't show a fall toward the chimney.
   - Fig 4-111 shows the front taller and the back's top falling toward the chimney, without a scale.
10. **Fig 4-111's orientation.** The front is to the right (§8.1). A reading of Fig 4-111 that puts
    the back chamber on the right would swap the two chambers.
