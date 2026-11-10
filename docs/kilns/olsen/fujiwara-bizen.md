# Kei Fujiwara's Bizen kiln, Imbe (`fujiwara-bizen`)

_Design file: `examples/olsen/fujiwara-bizen.yaml`. Rebuild with `uv run kilndesigner build
examples/olsen/fujiwara-bizen.yaml --out out/fujiwara`._

## The kiln

A Bizen wood climbing kiln, fired for exactly seven days. The parts, in order: the fire mouth
(dogi), which is the first chamber; the small "secret" chamber (himitsu) in a 24 in flue; the
first chamber (ichi no ma); the lower second chamber (kedo); then a 25 ft round chimney with a
flue damper at its entrance.

Sources: Olsen, *The Kiln Book*, 4th ed., pp.98–105: Fig 4-51 (sections), Fig 4-52 (himitsu),
Fig 4-53 (floor plan), Fig 4-55 (front and side elevations) and the text on pp.100–102.

## What's modelled

Two ware chambers, each its own size (`chamber.sizes`, 2026-11-09): the first 54 in deep and 60 in
to the crown, the kedo 34 in deep and 48 in to the crown, both 10 ft wide, each arch a semicircle
(6 in per foot of its span), so the springlines are 33 and 31 in.
They stand on a 22.6° slope (5 in in 12). Each has its own arch along the draft, held by the
walls between the chambers. Walls are 11½ in of medium-duty firebrick, the arch 9 in. The dogi
is the firebox: 10 × 8 ft, with a 3½ × 2 ft fire-mouth hole. The flue stack runs 3½ ft to a
25 ft chimney.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Dogi | 8 ft × 10 ft (Fig 4-53); fire-mouth hole 3½ × 2 ft (p.102); stepped shelves for ware | firebox 10 × 8 ft, stoke hole 42 × 24 in | matches; the ware in the dogi isn't modelled |
| Himitsu | 24 in flue with a 2 ft chamber; flues 3 × 6 in in and 6 × 9 in out (p.100, Fig 4-52) | the himitsu itself none; its wall is chamber 1's front wall, carrying the first arch, with seven 6 × 9 in flues from the dogi (2026-11-10; before, the dogi's whole mouth was cut through it) | size printed; the count assumed, as the wall between the chambers (7, scaled off Fig 4-53) |
| Wall between chambers | walls 10–13 in (p.100) | 18 in: Olsen's common wall, 4½ in thicker than the others and never narrower than the two 9 in arches' feet on it (p.46), the engine's default | assumed: is the printed 10–13 in for these walls too? |
| Chambers | first 4 ft 6 in, 5 ft tall; kedo 2 ft 10 in, 4 ft tall (Figs 4-53, 4-55) | `chamber.sizes`: 54 × 60 in and 34 × 48 in to the crowns | matches |
| Arches | each chamber's own, along the draft | `chambers: 2`, arches along | matches |
| Slope | 5 in rise per 12 in (Fig 4-55) | 22.6° | matches |
| Exit flues | first chamber 6 × 9 in; kedo 6 × 10 in, count not given (p.101) | engine's flue holes and exit flue | differs (count unknown) |
| Chimney | 25 ft; a 10 in round entry (p.101) | 25 ft, section sized by the engine | matches the height |
| Damper | a flue damper at the chimney entrance (Fig 4-55, p.102) | the engine's shelf-damper note | not expressible as a design feature |
| Doors | the dogi door in the front; a "door to chamber" in the side of each chamber (Figs 4-54, 4-55) | bricked door in the front wall | differs: the side doors aren't sized in the book |
| Side fire holes (takiguchi) | in the first chamber (p.100, Fig 4-55) | none | expressible now (`stoke_holes`); not given, as their size and place aren't printed |
| Spy holes | drawn on the dogi, the himitsu and the chambers (Fig 4-55: "ANA", "SPY HOLE") | engine default, three in the door | differs: not sized or placed in the book |

## Build results

The build finishes with no errors. Chamber 308 ft³ (301 ft³ with one mean size); heat loss
159.1 kW; priced materials $20,002; the masonry holds 239 and 201 lb per foot of arch, hot. Each floor steps 23.1 in above the last. **Information:** the 25 ft chimney is taller
than the 14.7 ft that Olsen's 3 × rise rule gives, counting the two modelled chambers only. Olsen
counts the dogi's run as well (p.101), so this is expected.

## Open questions

1. Fig 4-55 p.101: how wide and how tall are the side "door to chamber" openings? That would let
   the doors move to the side wall (`opening.each_chamber`).
2. Fig 4-53 p.100: how many 6 × 10 in exit flues leave the kedo?
3. Fig 4-55: at what heights are the spy holes ("ANA", "SPY HOLE") in the chamber walls?

## Scaled off the figures (step A, 2026-11-09)

Fig 4-55 (p.101, side elevation) scaled from the 5' and 4' crown heights (4.33 and 4.48 px/in);
horizontally its chambers are drawn at 5.5 and 7.0 px/in against Fig 4-53's depths, so the places
along the wall carry ±3 in. Fig 4-53 (p.100, plan) from its 10', 4'6" and 2'10"; the flue holes
counted with a pixel profile down each wall (`scratch/scale-a/profile.py`). Readings in
`scratch/scale-a/measure.py`.

| Feature | printed | drawing | scaled | In the model |
|---|---|---|---|---|
| Flues, first chamber to kedo | 6 × 9 in (p.101), count not given | piers in the wall | 7 gaps, 4–9 in (mean 6–7 in) | `draft.between`: 7, 6 × 9 in (new) |
| Kedo exit flues | 6 × 10 in (p.101), count not given | piers in the back wall | 5 gaps, 6–10 in (mean 8–9 in), read as the 10 in across (?) | `draft.exits`: 5 in the back, 10 × 6 in (new) |
| Chimney entry | "10in.-diameter opening" (p.101) | — | — | `draft.connection`: 10 in round (new) |
| Spy hole, first chamber ("MEMPO ANA") | — | a rectangle high in the side | 11½ × 7½ in, centre 28 in up, 15–19 in behind the middle | `spy_holes.holes`: left wall (?), chamber 1 |
| Spy hole, kedo | — | a square in the side | 6 × 6 in, centre 22 in up, 9–15 in behind the middle | chamber 2 |
| Takiguchi (side fire holes) | — | round, low beside each door | 5 in round; 13½ in up (chamber 1), 9½ in (kedo) | `stoke_holes`: left wall, chambers 1 and 2 |
| Doors to the chambers | — | arched, in the side | chamber 1: 23–29 × 37–38 in; kedo: 12–20 × 26–27 in | not entered: `opening.each_chamber` takes one size, and these differ |

Questions from step A:

4. Fig 4-55: the side elevation's far wall: is that the left (entered) or the right?
5. Fig 4-53: seven flues between the chambers and five out of the kedo (counted on the plan):
   right? Does the kedo's 10 in run across?
6. Fig 4-55: the doors scale about 26 × 37 in (first chamber) and 16 × 26 in (kedo). Right?
