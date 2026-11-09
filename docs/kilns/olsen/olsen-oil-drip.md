# Olsen gravity-drip oil kiln (`olsen-oil-drip`)

A 45–60 ft³ kiln fired to cone 10 on #2 diesel dripped onto iron plates in three channel ports.
Design file: `examples/olsen/olsen-oil-drip.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: pp.207–209 (text; drip-plate figures).

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Size | 45–60 ft³ | a 45 in cube with a No. 1 arch, 57 ft³ | assumed shape |
| Drip units | three channel ports, three plates each | three oil burners | matches |
| Plates | 9 × 5 in, 3 in apart, overlapping 2 in | — | not expressible |
| Firebox | a channel inside the chamber, at least 9 in to the bag wall, its full length | 9 × 45 in at the left wall | matches |
| Draft, flues, chimney | not printed | engine default (updraft, roof flue) | assumed |
| Door, spy holes | not printed | engine default | — |

No change in this pass.

## Key results

57.2 ft³; heat loss 16.5 kW; arch frame L4×4×¼. Oil at full fire isn't worked out: the drip rate
isn't printed.

## Open questions for the user

1. Which kiln is this (its draft and chimney)?
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| Channel ports | three, 6 in wide, plates 16 in high (Fig 8-20) | — | 15 in apart centre to centre, 6 in jambs (from 16" and 6", ±1 in) | not entered |
| Port flue | — | — | 7½ in wide, 24 in high (side view, from the 9", ±1½ in) | not entered |

Fig 8-20 draws three separate 6 in channel ports against the wall, where the model has one 9 in channel along it. Question: is this kiln's firebox three ports, as Fig 8-20, or one channel (p.208)? Until then the YAML is unchanged.
