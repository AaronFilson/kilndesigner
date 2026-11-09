# Olsen's Hollyweird Tube, 1985 (`hollyweird`)

_Design file: `examples/olsen/hollyweird.yaml`. Rebuild with `uv run kilndesigner build
examples/olsen/hollyweird.yaml --out out/hollyweird`._

## The kiln

A two-chamber wood kiln of the anagama type, at Olsen's home pottery: a Bizen-style front chamber
joined to a tube-style second chamber, each under a dome cast in K-26 castable. It has a front
firebox, whose ash pit is the walkway into the kiln, and a second firebox between the chambers,
stoked from the side.

Sources: Olsen, *The Kiln Book*, 4th ed., p.116 (text, Fig 4-108 sketch, Fig 4-110 plan),
p.117 (text and photos), p.124.

## What's modelled

Two chambers, 55 in wide, 8 ft and 12 ft long (`chamber.sizes`, 2026-11-09), 35.4 in to the
springline. The domes are 6 in of Kaolite 2600-LI and rise 12.6 in. Walls are 9 in of
medium-duty firebrick. The front firebox is 55 × 36 in with a grate whose bars are ¾ in apart.
It has a 15 × 18 in inlet flue and a 9 × 13½ in stoke hole. The second firebox is 15 × 55 in.
Cone 11.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Front firebox | 36 in, dug-out ash pit as the walkway (Fig 4-110, p.117) | 55 × 36 in, grate, on the ground | matches |
| Inlet flue, stoke hole | one 15 × 18 in, one 9 × 13½ in, in the door bricking, with air holes at grate level (p.117) | as printed | matches; the air holes aren't modelled |
| Second firebox | 15 in grate between the chambers, side door (Fig 4-110 "DOOR") | a front firebox 15 × 55 in | differs: no firebox between chambers, and no side stoke door |
| Between the chambers | a 13 in wall; three large exit flues across the second grate (p.116) | a 9 in wall with 4 flue holes, 4½ × 9 in (the engine's Kyoto rule) | differs: the flue count and size can't be set |
| Secondary air | a 5 in clay tube with a shutter, under the second grate (p.116) | none | not expressible |
| Steps | 12, 18 and 6 in (Fig 4-110) | the engine's chamber step | differs |
| Domes | two cast K-26 domes (p.116) | dome, 6 in Kaolite 2600-LI | matches (thickness assumed) |
| Chimney | inside 15 × 24 in (Fig 4-110); height not printed | sized by the engine | not expressible: `chimney.inside` needs a height |
| Spy holes | round holes in the domes' sides (Fig 4-108 sketch) | engine default | differs: not sized |
| Damper | not shown | the engine's note | n/a |

## Build results

The build finishes with no errors. Chamber 335 ft³; top temperature 2361 °F (cone 11); heat loss
159.3 kW; priced materials $6,731.

## Open questions

1. How tall is the chimney? With its height, the printed 15 × 24 in section can go in.
2. Fig 4-110 p.116: how big are the three exit flues from the front chamber?
3. Fig 4-108: how far above the floor are the round spy holes in the domes, and how big are they?

## Scaled off the figures (step A, 2026-11-09)

Fig 4-110 (p.116, plan) scaled from the 55" chamber width and the printed 12 × 24 in shelves
(7.1–7.8 px/in); the flues counted with a pixel profile down the 13" wall
(`scratch/scale-a/profile.py`). Fig 4-108 is a perspective sketch: its domes' spy holes have no
printed dimension in their plane, so they aren't scaled. Readings in `scratch/scale-a/measure.py`.

| Feature | printed | drawing | scaled | In the model |
|---|---|---|---|---|
| Flues between the chambers | "Three large exit flues" (p.116); the wall "13"" | three gaps between two piers | 11–13 in wide each (the piers 10½–11½ in) | not entered: their height isn't drawn, and `draft.between` needs it |
| Spy holes in the domes | — | round, in the domes' sides (Fig 4-108) | can't be scaled: a perspective sketch | engine default |
| Chimney | 15 × 24 in inside; height not printed | — | not drawn in elevation | engine |

Question from step A:

4. The three flues between the chambers scale about 12 in wide. How tall are they?
