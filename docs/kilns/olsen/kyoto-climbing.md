# Kyoto-style climbing kiln, the type (`kyoto-climbing`)

The wood-fired chamber kilns of south-east Kyoto, drawn from the book's ranges. Design file:
`examples/olsen/kyoto-climbing.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: pp.89–94 (text; Figs 4-21 to 4-34, notably Fig 4-28 dimensions,
4-31 chamber shapes, 4-32 arches, 4-33 and 4-34 stoking), p.96, p.205 (Fig 8-16).

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 6–7' tall, 4.5–6' wide (Fig 4-28) | 63 in wide, 78 in to the crown | middle of the ranges |
| Depth, count, slope | not given for the type | Bidai's depth, ten chambers (Kyomizu), Bidai's slope | assumed |
| Arch | double-radius, peak toward the back (reduction chambers) | semicircular sprung arch across the width | `roof.peak_at` (2026-11-09) can say it, but where the peak stands isn't printed |
| Chamber firebox (himae) | 9 in trough by the front wall, saggar bag wall | ten 9 × 63 in fireboxes | matches |
| Flues | outlet about 9 × 5 in, inlet 9 × 4½–6 in, 9 in apart, count not given | five 5 × 9 in a wall (`draft.between`); exit flue the engine's | count derived (step A, below) |
| Doors | in a side wall | front wall | differs (the engine's door can't sit under the arch's springing here) |
| Main firebox, chimney | not printed | engine | — |

Step A (2026-11-09) added the flues between chambers.

## Key results

1110 ft³; heat loss 512 kW (all ten chambers at top at once); engine chimney 18.5 ft.

## v2 statics (2026-11-10)

The walls between the chambers are now 18 in (Olsen's common wall, never narrower than the two 9 in
arches' feet on it, p.46; the engine's default), so the run is longer and each floor steps 19.7 in.
Along the row every chamber stands cold and hot, the ends' supports giving 0 cold and 7.6 lbf/ft
hot. The arch, its 20.7 in rise a hair past a semicircle on the 41⅓ in span, is laid level on its
walls; each ring's foot against the taller wall behind it is a springer coursed into that wall.

## Open questions for the user

1. Figs 4-31, 4-32: how far along the span does a reduction chamber's peak stand, and the two
   radii (for `roof.peak_at`)?
2. Fig 4-27 (p.91): the vertical dimension at the wall between chambers 2 and 3, and the label at
   the figure's left end, are too faded in the scan to read. What do they say in your copy?

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-KK/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

Fig 4-28 (p.91) prints one length, the 15" from the back wall's floor to the outlet flue's foot,
and the chamber's ranges (6–7' tall, 4½–6' wide). The two don't agree: by the 15" the chamber is
drawn 35 in wide and 49 in tall; by the ranges the 15" reads 22–30 in. The 15" agrees with the
printed flue sizes, so it was used for the flues only. Fig 4-32 (p.92) prints no dimension: only
ratios were taken off it. Fig 4-31's arches (4' and 6' printed) are the type's cross-section
against other kilns', symmetric, and Figs 4-29, 4-30 are photos with nothing printed.

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| Flues out | "approx. 9 × 5", 9 in apart (Fig 4-28) | in the back wall, foot 15" up | 11 ±1 in tall, 5½ ±½ in wide (from the 15") | 5 wide × 9 in high |
| Flues in | 9 × 6 to 9 × 4½ (Fig 4-28) | at the front wall's foot | 9½ ±1 in tall | (one size per wall in the engine: the outlet's) |
| Flue count | not printed | — | as many 5 in flues as fit across 63 in, 9 in apart: 5 (derived, Olsen p.96's rule) | `draft.between`: 5 |
| Reduction chamber's peak | toward the back (p.91–92) | Fig 4-32 | 58 % (56–60 %) of the span from the front wall; rise 0.68 of the span; radii 0.59 and 0.47 of the span (ratios, ±2 %) | not entered: see below |
| Doors, stoke holes, spy holes, main firebox, chimney | not printed | Figs 4-33, 4-34 unsized | nothing to scale from | engine |

`roof.peak_at` isn't entered. On Fig 4-32 the back half runs 0.42 of the span against a rise of
0.68, past a quarter circle, which the engine refuses; and this file's semicircular arch (rise half
the span, from Olsen's 6 in per foot) allows no offset peak at all. Entering 58 % would need the rise
lowered to 0.42 × 41⅓ = 17.4 in or less, which the book doesn't say.

## Checked against the book (2026-11-18)

Read again on the page images: pp.89–94, p.96 and p.205, with Figs 4-27 and 4-28 at zoom 4–14.
The measurements are in the dataset. The design is unchanged, and its gaps are below and in
`docs/planning/02-plan.md`.

**Measured and read:**
- **Fig 4-28's "6–7' tall, 4.5–6' wide" reads along the draft**, front wall to back wall:
  - the figure is drawn along the draft, the inlet flues in one wall and the outlets in the other;
  - Fig 4-31 draws the Kyoto chamber "narrower" than other climbing kilns' (p.91), 4 ft against
    6 ft, its arch's span;
  - Fig 4-27 marks the Kyomizu kiln's third chamber "4' INSIDE";
  - every Kyoto chamber the book sizes is 3–4½ ft along the draft and 6–14 ft across: Bidai
    36–46 × 73 in (Fig 4-36), Kawaii 4 × 7 ft (p.97), Suzuki 4½ × 14 ft (p.93).
  The word alone doesn't decide it. Tobe's "25ft long by 10ft tall by 10ft wide" (p.90) uses
  "wide" along the draft, Kawaii's "7ft wide, 4ft deep" (p.97) across.
- **The type's length across** isn't printed.
- **Fig 4-28's mark** beside the outlet flue reads 15 in at zoom 14. Its second digit is open at
  the top like the figure's other 5s; it had also been read 18.
- **Fig 4-27** numbers its chambers to 10 and draws a chimney past the last one, unsized. Its
  vertical dimension at the wall between chambers 2 and 3, and a label at its left end, are too
  faded in the scan to read.
- **Each chamber's three stoke holes** (Fig 4-34), unsized: the takaguchi low in the himae, the
  aizashiguchi at the floor between the saggar settings, and the mempo ana high at the back. They
  are covered after each stoking.
- **The main firebox (dogi)** is photographed at the kiln's foot (Fig 4-22), unsized. Suzuki's is
  stoked 15 h to 1832 °F before the side stoking (p.93).

**Gaps** (for the plan):
1. **The design's axes.** It takes Fig 4-28's 4½–6 ft across the kiln (63 in) and the Bidai
   kiln's 41⅓ in along the draft. The book's range reads along the draft, and its length across
   isn't printed.
2. **The main firebox.** Neither the book nor the design sizes it, so v2's draft path has no way
   in for chamber 1's air and refuses (stoke holes are covered after each stoking).
3. **The arch.** The book draws it pointed and springing near the floor, with the reduction
   chambers' peak set back. The design's semicircle on side walls is the engine's.
4. **The doors** are in a side wall (Figs 4-27, 4-33); the design's is in the front wall.
5. **Fig 4-27's faded dimension and label**, for the owner's copy (question 2 below).

v2 on the unchanged design: the draft path is refused for gap 2, and the arches stand cold and hot.

Questions: is Fig 4-32's arch drawn to its shape (peak about 58 % back, rise about two thirds of
the span)? If so, the engine's two-radius arch would have to turn past a quarter circle at the
back. How many flues in each wall (5 assumed), and are the inlets the outlets' other ends?
