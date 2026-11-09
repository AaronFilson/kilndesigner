# Takichi Kawaii's climbing kiln, 1984 (`kawaii`)

A four-chamber Kyoto-style wood climbing kiln, its plan "almost exactly" the Bidai kiln's. Design
file: `examples/olsen/kawaii.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: pp.96–97 (text; Figs 4-44 to 4-48, photos), p.200.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chambers | four, 7 ft wide × 4 ft deep × 5'8" tall | four, 84 × 48 in, 24 in arch rise | matches |
| Step | 12–15 in between chambers | 13.2° slope | matches |
| Firebox (dogi) | 5 ft tall, bars 18–24 in, two extra side stoke holes | Bidai's firebox, 21 in bars | assumed from Bidai; side stoke holes expressible now (`stoke_holes`), not given: their size isn't printed |
| Flues | inlet and exit 7 × 10 in, last exit 9 × 10 in, count not printed (Figs 4-47, 4-48) | engine flue 9 × 7½ in | count not printed; not set |
| Doors | one per chamber in a side wall, a stoke hole bricked into each (Fig 4-46) | 20 × 44 in arched, each chamber, right wall | size from Bidai; a door stoke hole expressible now (`stoke_holes` at the door's place), not given: its size isn't printed |
| Bracing | on the dogi and front chamber | buttressed, no steel | partly |
| Spy holes | not visible | engine default | — |

No change in this pass. Fig 4-46's doorway looks square-headed in the photo; the model keeps the
arched head of Olsen's other built kilns (see question 2).

## Key results

587 ft³; heat loss 274 kW; grate 294 in²; engine chimney 9.8 ft.

## Open questions for the user

1. How many 7 × 10 in flues are there in each chamber wall (Fig 4-48)?
2. Fig 4-46: is the second chamber's doorway square-headed (a lintel) or arched?
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

Figs 4-44 to 4-48 were not opened in this pass (time): left for a later pass.
