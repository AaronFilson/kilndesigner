# Moveros umbrella kiln (`moveros-umbrella`)

A round folk updraft of granite rubble at Moveros, Spain, fired with heather and brushwood, the pots
on an "umbrella" floor over the firebox. Design file: `examples/olsen/moveros-umbrella.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: pp.153–154 (text; Fig 6-3 section).

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | about 5 ft across, 4 ft tall | round, 60 × 48 in, open top | matches |
| Walls | granite rubble, 18–24 in, clay plaster | 21 in granite | matches; plaster not expressible |
| Firebox | under the umbrella floor, 3½–4 ft | under, 60 × 60 × 48 in | plan assumed |
| Mouth | 27 in high, 22 in wide (Fig 6-3) | stoke hole 22 × 27 in | matches |
| Umbrella floor | spokes on a central trunk | — | not expressible |
| Spy holes, door | none | engine default | — |

No change in this pass.

## Key results

78.5 ft³; heat loss 35.3 kW (walls; the open top's loss isn't worked out).

## Open questions for the user

None new (the mouth width, 22 or 28 in, was settled as 22).
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| Firebox height | 3½–4 ft | — | 43 in (Fig 6-3, from the 4', ±3 in) | `height: 43 in` |

The elevation is a sketch: its 5' across and 4' up give 6.0 and 3.4 px/in, so nothing across is scaled. The top view and the mouth inset have no dimension to share: wall thickness and the firebox's plan can't be scaled.
