# Kyoto-style climbing kiln, the type (`kyoto-climbing`)

The wood-fired chamber kilns of south-east Kyoto, drawn from the book's ranges. Design file:
`examples/olsen/kyoto-climbing.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: pp.89–94 (text; Figs 4-21 to 4-34, notably Fig 4-27 the Kyomizu
kiln's section, 4-28 dimensions, 4-31 chamber shapes, 4-32 arches, 4-33 and 4-34 stoking), p.96,
p.205 (Fig 8-16). Checked on the page images, 2026-11-18 (the kiln-by-kiln check).

## The reading (2026-11-18)

Fig 4-28's "6–7' tall, 4.5–6' wide" gives the chamber's span **along the draft**, front wall to back
wall. It is not the width across the kiln:
- The figure is drawn along the draft, with the inlet flues in one wall and the outlets in the other.
- Olsen calls a chamber's length across the kiln its "long": Tobe's largest chamber is "25ft long
  by 10ft tall by 10ft wide" (p.90), its width "almost equal to the height" (p.92); Suzuki's are
  "14 x 6½ x 4½ ft" (p.93).
- Fig 4-31 draws the Kyoto chamber 4 ft along the draft and 6 ft tall, and Fig 4-27 marks the
  Kyomizu kiln's third chamber "4' INSIDE".

Until this check the design read the 4½–6 ft as the width across (63 in), with the Bidai kiln's
41⅓ in along the draft. It now takes:
- 63 in along the draft, the middle of the range;
- 168 in across, the Suzuki kiln's 14 ft (assumed). The type's length across isn't printed. The
  floor's five stoking zones, short, medium and long tosses from both sides at once (p.92,
  Fig 4-33), need a long chamber.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 6–7' tall, 4½–6' along the draft (Fig 4-28); the Kyomizu kiln 4' along, 6' tall (Figs 4-27, 4-31); length across not printed for the type | 63 in along the draft, 78 in to the crown, 168 in across | middle of the ranges; the length across assumed (Suzuki's) |
| Count, slope | not given for the type | ten chambers (Kyomizu, Fig 4-27 numbers them to 10), Bidai's 3 to 1 | assumed |
| Arch | pointed, from near the floor (Figs 4-28, 4-31); reduction chambers double-radius, peak toward the back (Fig 4-32) | a semicircle along the draft, 31½ in rise on 46½ in walls (v2's statics); v1 lays it across the width | differs: a row's pointed arch along the draft and the offset peak aren't expressible |
| Chamber firebox (himae) | a 9 in trough by the front wall, one row of empty saggars as the bag wall (p.92, Fig 4-34) | ten 9 × 168 in, one in each chamber (the path's `ONE_PER_CHAMBER`) | matches |
| Stoke holes | takaguchi (the himae and the upper half), aizashiguchi (at the floor, between the saggar settings), mempo ana (high at the back), stoked from both sides (pp.92–93, Fig 4-34); unsized | none | covered after each stoking, so not intakes |
| Flues | outlet about 9 × 5 in, 9 in apart, its foot 15 in up; inlet 9 × 4½–6 in; count not given (Fig 4-28) | twelve 5 × 9 in a wall (`draft.between`) | count derived (below) |
| Doors | in a side wall (Figs 4-27, 4-33) | front wall | differs (the engine's door can't sit under the arch's springing here) |
| Main firebox | at the foot of the kiln (Fig 4-22, a photo), unsized; Suzuki's stoked 15 h to 1832 °F (p.93) | none | not expressible without its size: v2's path is refused |
| Chimney | at the top end (Fig 4-27), unsized | the engine's | — |

## v2 (2026-11-18)

- **Cavity:** each chamber's gas zone is 439–442 ft³ (12.4–12.5 m³), 4,400 ft³ in all.
- **Draft path: refused.** Chamber 1's trough has no way in for its air: its stoke holes are
  covered after each stoking, and the design has no main firebox. Every stage is refused for the
  same reason, with the front open or shut.
- **Statics:** the arches along the draft stand cold and hot. The least the buttresses at the ends
  must give is 10.7 and 13.3 lbf/ft cold and 53.0 and 56.2 hot; the most they can be asked for hot
  is 709 and 660 lbf/ft.
- **Setting:** regenerated from the method on the new cavity, [835, 4951] kg in chamber 1 and
  [848, 5128] kg in the middle chambers.

Not rerun: the rows' firing tests (tests come second, the owner, 2026-11-18). v1's 1110 ft³ and
512 kW were on the old reading.

## Future work

- **The main firebox (dogi):** the type's isn't sized. With one, chamber 1 takes its air through
  the firebox's mouth and the side stoking's air comes up the kiln, the front's intakes a band
  from closed to open (inputs §3).
- **Arches along the draft in a row:** a pointed or catenary arch springing near the floor (Figs
  4-28, 4-31), and the reduction chambers' offset peak (Fig 4-32, below). v1 lays the arch across.
- **The doors in a side wall.**

## Open questions for the owner

1. Figs 4-31, 4-32: how far along the span does a reduction chamber's peak stand, and the two
   radii (for `roof.peak_at`)?
2. Fig 4-27 (p.91): the vertical dimension at the wall between chambers 2 and 3, and the label at
   the figure's left end, are too faded in the scan to read. What do they say in your copy?

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-KK/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

Fig 4-28 (p.91) prints one length, the 15" from the back wall's floor to the outlet flue's foot
(read again at zoom 14, 2026-11-18: 15, not 18), and the chamber's ranges (6–7' tall, 4½–6' along
the draft). The two don't agree: by the 15" the chamber is drawn 35 in along and 49 in tall; by
the ranges the 15" reads 22–30 in. The 15" agrees with the printed flue sizes, so it was used for
the flues only. Fig 4-32 (p.92) prints no dimension: only ratios were taken off it. Fig 4-31's
arches (4' and 6' printed) are the type's section against other kilns', symmetric, and Figs 4-29,
4-30 are photos with nothing printed.

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| Flues out | "approx. 9 × 5", 9 in apart (Fig 4-28) | in the back wall, foot 15" up | 11 ±1 in tall, 5½ ±½ in wide (from the 15") | 5 wide × 9 in high |
| Flues in | 9 × 6 to 9 × 4½ (Fig 4-28) | at the front wall's foot | 9½ ±1 in tall | (one size per wall in the engine: the outlet's) |
| Flue count | not printed | — | as many 5 in flues as fit across 168 in, 9 in apart: 12 (derived, Olsen p.96's rule; 5 across the old 63 in) | `draft.between`: 12 |
| Reduction chamber's peak | toward the back (p.91–92) | Fig 4-32 | 58 % (56–60 %) of the span from the front wall; rise 0.68 of the span; radii 0.59 and 0.47 of the span (ratios, ±2 %) | not entered: see below |
| Doors, stoke holes, spy holes, main firebox, chimney | not printed | Figs 4-33, 4-34 unsized | nothing to scale from | engine |

`roof.peak_at` isn't entered. On Fig 4-32 the back half runs 0.42 of the span against a rise of
0.68, past a quarter circle, which the engine refuses; and this file's semicircular arch (rise half
the span, from Olsen's 6 in per foot) allows no offset peak at all. Entering 58 % would need the rise
lowered to 0.42 × 63 = 26½ in or less, which the book doesn't say.
