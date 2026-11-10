# Takichi Kawaii's climbing kiln, 1984 (`kawaii`)

A four-chamber Kyoto-style wood climbing kiln, its plan "almost exactly" the Bidai kiln's. Design
file: `examples/olsen/kawaii.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: pp.96–97 (text; Figs 4-44 to 4-48, photos), p.200.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chambers | four, 7 ft wide × 4 ft deep × 5'8" tall | four, 84 × 48 in, 24 in arch rise | matches |
| Step | 12–15 in between chambers | 11.6° slope: a 13½ in step over a chamber and the 18 in wall between (re-derived 2026-11-10, when the wall between chambers became Olsen's common wall) | matches |
| Wall between chambers | not printed | 18 in: Olsen's common wall, 4½ in thicker than the others and never narrower than the two 9 in arches' feet on it (p.46), the engine's default | assumed |
| Firebox (dogi) | 5 ft tall, bars 18–24 in, two extra side stoke holes | Bidai's firebox, 21 in bars | assumed from Bidai; side stoke holes expressible now (`stoke_holes`), not given: their size isn't printed |
| Flues | inlet and exit 7 × 10 in, last exit 9 × 10 in, count not printed (Figs 4-47, 4-48) | five 7 × 10 in a wall, five 9 × 10 in out of chamber 4; since 2026-11-10 five 7 × 10 in inlets from the firebox through chamber 1's front wall, which carries its arch (before, the firebox's whole mouth was cut through that wall) | sizes printed; counts scaled (step A, below) |
| Doors | one per chamber in a side wall, a stoke hole bricked into each (Fig 4-46) | 20 × 44 in flat-headed, each chamber, right wall | size from Bidai; head from Fig 4-46 (step A); a door stoke hole expressible now (`stoke_holes` at the door's place), not given: its size isn't printed |
| Bracing | on the dogi and front chamber | buttressed, no steel | partly |
| Spy holes | not visible | engine default | — |

Fig 4-46's doorway is square-headed in the photo; since step A the model gives it a flat head.

## Key results

587 ft³; heat loss 274 kW; grate 294 in²; engine chimney 9.8 ft.

## Open questions for the user

1. How many 7 × 10 in flues are there in each chamber wall (Fig 4-48)? Scaled 5 (or 6), below.
2. Fig 4-46: is the second chamber's doorway square-headed (a lintel) or arched? A closer look
   (step A) reads a slab lintel; entered flat.
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-KK/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

Figs 4-44 to 4-48 (p.97) are all photos, none with a dimension printed on it. Only Fig 4-48 shows
something whose size is printed in the text (the 7 × 10 in flues), so only it was scaled, each
pier from the flues on either side of it (they are foreshortened, so each flue is its own scale).

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| Flues between chambers | 7 × 10 in, count not printed (p.97) | three seen in Fig 4-48, taller than wide | piers 6–8½ in (Fig 4-48, from the 7 in flues, ±1½ in); across 84 in, 5 flues leave equal 8 in piers, 6 leave 6 in: **5** (or 6) | `draft.between`: 5, 7 wide × 10 in high |
| Exit flues of chamber 4 | 9 × 10 in (p.97); "the same in each chamber" (Fig 4-48 caption) | — | count as between, 5 | `draft.exits`: 5, 9 × 10 in, back wall |
| Check | flue 10 in high | — | flue 2 reads 10½ ±1½ in high by its own 7 in width | method holds |
| Doorway head | not printed | Fig 4-46: square-headed under a slab lintel (photo) | — | `head: flat` (was arched) |
| Doorway size | not printed | — | not scalable (no printed size in the photo) | Bidai's 20 × 44 in kept |
| Side stoke hole on the dogi | not printed | Fig 4-45: one small square hole on its side, low; the mouth a small arch | not scalable: the dogi's printed 5 ft has no clear top edge in the photo | left out |
| Spy hole | not printed | Fig 4-46: one round hole in the arch's end, near the chamber's far end | not scalable | engine default |
| Chimney | not printed | Fig 4-47: the top of the exit flues (photo) | not scalable | engine |

Questions: are there 5 or 6 flues in each chamber wall? Does chamber 4 have as many 9 × 10 in exit
flues? How big is the dogi's side stoke hole, and the doorway (square-headed, Fig 4-46)?
