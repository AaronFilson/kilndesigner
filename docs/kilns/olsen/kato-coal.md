# Mr Kato's coal downdraft, Tajimi (`kato-coal`)

A Tajimi-style coal downdraft with two side fireboxes, fired in over 50 hours to 2372 °F in heavy
reduction. Design file: `examples/olsen/kato-coal.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.131 (text; Fig 5-4 section and plan), p.132, p.207 (Fig 8-18).

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 6'6" wide, 6'6" to the crown, 7' long; about 250 cu ft | 78 × 84 in, semicircular arch from 39 in | matches (264 ft³) |
| Walls | very thick; 10" at the door end and by the chimney (Fig 5-4) | sides 18 in assumed, door 10 in, back 10 in (`lining.back`) | matches the printed ends |
| Fireboxes | two, one each side, 2'6" mouths, grates 30 × 22 in, 1 in iron rods (Figs 5-4, 8-18) | two 30 × 22 in with grates | matches; bar gap not printed |
| Bag walls | 36" high, 4'8" apart (Fig 5-4) | — | not expressible |
| Exit flues | twelve 6 × 6 in floor flues, 432 in² (p.131) into flue channels | twelve 6 × 6 in in an even grid in the floor, 432 in² (`draft.exits`) | matches (places not printed); the channels aren't modelled |
| Chimney | round, 3 ft inside, 20 ft, tapering to 15½ in; 20" connection, damper (Fig 5-4) | 36 in → 15½ in, 20 ft | matches; the 20" connection is expressible (`draft.connection`) but not whether it is round or square, and the damper isn't sized |
| Vapour holes | in the arch (Fig 5-4) | — | not expressible |
| Door | in the end wall, bricked | front, bricked, 10 in | matches |
| Spy holes | not drawn | engine default | — |

2026-11-09 (B3): the back wall takes its printed 10 in (`lining.back`), so the heat loss rises
from 117 to 124.4 kW.

## Key results

264 ft³; heat loss 124.4 kW; grates 1320 in²; chimney 20 ft against the engine's 13–23.6 ft range;
draft 0.18 in. w.c. at 1000 °F flue gas.

## Open questions for the user

1. Is there a damper size on Fig 5-4 (the 20" connection's height)?
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| Exit flue places | twelve 6 × 6 in (p.131) | three rows of four | rows 16 in left, 1 in left, 13 in right of centre; columns 32, 13 in in front of and 6, 23 in behind the middle (Fig 5-4 plan, from 7' and 6'6", ±1 in) | `draft.exits.places` |
| Firebox height over grate | — | — | 26 in (section, from 6'6" and 36", ±1 in) | `height: 26 in` |
| Grate below chamber floor | — | — | 9 in (±1 in) | `step: 9 in` |
| Ash pit | — | — | 27 in (from 6'6" and 36", ±1 in); 15 in from the 18" channel | `ash_pit: 27 in` |
| Damper | drawn in the plan, no size | shelf 28 in long | plan only: no height | left at default |
| Checks | mouth 2'6", connection 20", grate 22 in | — | 25, 23.6, 24.5 in | printed kept |

Questions: (a) the section's 18" flue channel scales against its 6'6" and 36" by nearly 2×; which is the ash pit's depth, 27 in or about 15 in? (b) the plan draws the 2'6" mouth at 25 in and the 20" connection at 23½ in: is the plan loose there, or are the printed sizes something else?
