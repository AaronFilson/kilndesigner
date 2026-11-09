# Cheever Meaders's groundhog (`meaders-cheever`)

A shallow-firebox wood groundhog of rubble brick, Mossy Creek, Georgia. Design file:
`examples/olsen/meaders-cheever.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: pp.112–113 (text; Figs 4-86 to 4-89).

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 48 in to the crown, 5 ft wide (faint), 12 ft long | 5 ft half-circle on 18 in walls, 8 ft chamber + 4 ft firebox | matches |
| Exit flues | six, 5 × 9 in, in the back wall (Fig 4-89) | six 5 × 9 in, spread evenly along the back wall (`draft.exits`) | matches (places not printed) |
| Chimney | 9 in × 5 ft (p.112); height not printed | 60 × 9 in, 8 ft | section matches; height assumed |
| Firebox | shallow, full width | 5 × 4 ft, no grate | matches |
| Central post | 30 in (faint) | — | not expressible |
| Door, spy holes | front (loading); spy holes not drawn | front, engine default | — |

No change in this pass.

## Key results

139 ft³; heat loss 55.6 kW; draft 0.073 in. w.c.; chimney 8 ft against the engine's 8–15.4 ft.

## Open questions for the user

None new.
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| Exit flue places | six 5 × 9 in | four drawn | 23½ and 15 in each side of the middle (Fig 4-89, from 48", 30", 5', ±1 in); two hidden by the post | `places`, the hidden two at ±5 in |
| Central post | 30" high | — | 7 in wide (±½ in) | not expressible |

Question: are the two flues not drawn behind the post, about 5 in each side of the middle?
