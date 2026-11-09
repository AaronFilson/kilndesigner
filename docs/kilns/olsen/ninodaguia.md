# Niñodaguia kiln (`ninodaguia`)

The round wood updraft of a commercial pottery in north-west Spain, 2000–3000 small pots set on
setter tiles with shards over the top. Design file: `examples/olsen/ninodaguia.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: pp.156–157 (text; Fig 6-14 section).

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 7 ft across, 3½ ft tall | round, 84 × 42 in, open top | matches |
| Walls | 15½ in, "9 rows of bricks up" | 15½ in common brick | matches |
| Floor | shallow dome of common brick in soldier courses, 12 in keystone, 1½ in flue holes | 9 in flat | dome and holes not expressible |
| Firebox | 3 ft high, under the floor | under, 84 × 84 × 36 in | plan assumed |
| Mouth | 27 in high, 18 in wide | stoke hole 18 × 27 in | matches |
| Spy holes, door | not drawn | engine default | — |

No change in this pass.

## Key results

135 ft³; heat loss 16.9 kW (walls only).

## Open questions for the user

1. Fig 6-14: how many 1½ in flue holes through the floor?
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| Floor dome | shallow dome, 12 in keystone | — | rises 11½ in, about 8 in thick (inset, from 3½' and 3', ±1 in) | not expressible |
| The "18"" by the firebox | 18" | — | the hatched wall it marks scales 29 in (vertical scale; the inset has no horizontal dimension) | not used |
| Floor flue holes | 1½ in, count not printed | about twenty dots in a perspective sketch | can't be counted or scaled | left out |

Question: the "18"" beside the firebox marks a wall that scales about 29 in: what does it measure?
