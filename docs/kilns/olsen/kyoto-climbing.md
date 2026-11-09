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

## Open questions for the user

1. Figs 4-31, 4-32: how far along the span does a reduction chamber's peak stand, and the two
   radii (for `roof.peak_at`)?
</content>

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

Questions: is Fig 4-32's arch drawn to its shape (peak about 58 % back, rise about two thirds of
the span)? If so, the engine's two-radius arch would have to turn past a quarter circle at the
back. How many flues in each wall (5 assumed), and are the inlets the outlets' other ends?
