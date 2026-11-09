# Kitade Tojilo chamber kiln, Kutani (`kitade-tojilo`)

A wood chamber kiln on a 33 % slope with a "modern chamber-kiln firebox", side-stoked, slab wood on a
full-width grate. Design file: `examples/olsen/kitade-tojilo.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.202 (text; Fig 8-11 firebox section, plan and sketch; photos
Figs 8-8, 8-9), p.203.

## Changes in this pass

- Firebox height above the grate **18 in**: 42 in from the ash pit's bottom less the 24 in ash pit
  (Fig 8-11, derived).

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 4' wide, 5' tall, 8' deep, arched; slope 33 % | one chamber, 48 × 96 in, 24 in rise, 18.3° | matches; the other chambers not counted in the book |
| Firebox | 15" wide, the chamber's width long; ash pit 24" | 15 × 48 in, ash pit 24 in, height 18 in | matches |
| Firebox roof | slopes 30° up to the chamber | flat | not given: `roof: sloped` slopes along a firebox's run from its mouth to the chamber, but this side-stoked firebox is modelled running 4 ft out from the front wall, so its 30° over the 15 in toward the chamber runs across the model's width |
| Grate | fireclay bars at 6" | gap 6 in | matches |
| Stoke hole | 9 × 7 in, in the side | 9 × 7 in | matches |
| Flue inlet | 9 × 12 in, 12 in above the grate, count not printed | — | left out: count not given |
| Air holes | two 12 × 18 in in the front, "2½"" from the end (Flagged) | — | not expressible |
| Door, exit flue, chimney | sketch shows an arched end; others not printed | engine default | — |

## Key results

146 ft³; heat loss 100 kW; grate 720 in²; engine chimney 8.2 ft; arch frame L6×6×5⁄16.

## Open questions for the user

1. Fig 8-11: how many 9 × 12 in flue inlets cross into the chamber?
2. Fig 8-11: the "2½"" from the end wall to the first air hole scales to about 20 in: which is it?
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| Stoke hole sill | — | — | 4 in over the grate (Fig 8-11, from 42", 24", 12", 15", ±½ in) | `sill: 5 in` (two courses) |
| Stoke hole | 9 × 7 in | — | drawn 4 × 5½ in | printed kept |
| Flue inlet | 9 × 12 in, 12 in over grate | — | 11 in high, foot 12 in over grate | printed; count can't be scaled |
| Air holes | 12 × 18 in, "2½"" from the end | — | the 2½" arrow scales 20–24 in; hole centres 22 and 71 in from the end | not expressible |

Questions: (a) the plan (Fig 8-11) scales 8 ft long ±9 in from its own 12" and 18": the chamber's depth, not its 4 ft width. Does the firebox run along the 8 ft side? (b) the stoke hole is drawn 4 × 5½ in against its printed 9 × 7 in.
