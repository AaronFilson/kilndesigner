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
| Hollyweird | pp.116–117, Figs 4-108, 4-110 to 4-112 | The side door is drawn at the second firebox in Fig 4-110 (its stoke hole is the recorded 9 × 13½ in). The door itself is **not yet measured**: scale it against the printed 55 in platforms. | The second firebox's 5 in tube under the grate (p.116; Fig 4-111's caption: "Notice the secondary air-supply tube at the bottom right on the door"), and the front firebox's "air holes at grate level" (p.117) | **not scalable**: Fig 4-111 prints nothing, and Fig 4-112 is too dark to make out the grate-level holes |
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
- **Q3, separate side air inlets:** on the pages read, the only separate inlets are:
  - Hollyweird's: the 5 in tube under the second grate (p.116) and the air holes at the front
    grate level (p.117);
  - the tube under the grate in Olsen's two-chamber design (p.206);
  - Kitade's two air-draft and ash-pit holes in the front (p.202).

  Bidai's Fig 8-7 air opening belongs to its main firebox, not a chamber. None is drawn or named for
  Suzuki, Kyoto, Tobe, Kawaii or Hotchkiss. Fujiwara wasn't checked. Olsen's general statement is on
  p.206 (quoted in §2 above): the main air comes from the front; secondary air from cracks, doors
  and so on.
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
3. **Tamba against the bundle rule:** its bundles are 15 × 15 × 30 in (p.87), but its side holes
   scale about 7 in on two figures (Figs 4-7 and 4-16). **Answered (the owner, 2026-11-17):** Tamba
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
- **Hollyweird, Fig 4-110 (p.116):** the side door's width against the printed 55 in platforms.
- **Fujiwara (pp.99–105):** side holes and inlets.
- **Tamba, Fig 4-10 (p.86):** the tube's section against the pots' printed 13–24 in (p.85).
- **Hotchkiss:** p.57 (Fig 2-46).
