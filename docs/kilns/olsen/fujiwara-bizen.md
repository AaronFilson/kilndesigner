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

Two ware chambers of one size, the mean of the two: 44 in deep, 10 ft wide, 54 in to the crown.
They stand on a 22.6° slope (5 in in 12). Each has its own arch along the draft, held by the
walls between the chambers. Walls are 11½ in of medium-duty firebrick, the arch 9 in. The dogi
is the firebox: 10 × 8 ft, with a 3½ × 2 ft fire-mouth hole. The flue stack runs 3½ ft to a
25 ft chimney.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Dogi | 8 ft × 10 ft (Fig 4-53); fire-mouth hole 3½ × 2 ft (p.102); stepped shelves for ware | firebox 10 × 8 ft, stoke hole 42 × 24 in | matches; the ware in the dogi isn't modelled |
| Himitsu | 24 in flue with a 2 ft chamber; flues 3 × 6 in in and 6 × 9 in out (p.100, Fig 4-52) | none | not expressible |
| Chambers | first 4 ft 6 in, 5 ft tall; kedo 2 ft 10 in, 4 ft tall (Figs 4-53, 4-55) | two of the mean size | differs: the engine has one chamber size |
| Arches | each chamber's own, along the draft | `chambers: 2`, arches along | matches |
| Slope | 5 in rise per 12 in (Fig 4-55) | 22.6° | matches |
| Exit flues | first chamber 6 × 9 in; kedo 6 × 10 in, count not given (p.101) | engine's flue holes and exit flue | differs (count unknown) |
| Chimney | 25 ft; a 10 in round entry (p.101) | 25 ft, section sized by the engine | matches the height |
| Damper | a flue damper at the chimney entrance (Fig 4-55, p.102) | the engine's shelf-damper note | not expressible as a design feature |
| Doors | the dogi door in the front; a "door to chamber" in the side of each chamber (Figs 4-54, 4-55) | bricked door in the front wall | differs: the side doors aren't sized in the book |
| Side fire holes (takiguchi) | in the first chamber (p.100, Fig 4-55) | none | expressible now (`stoke_holes`); not given, as their size and place aren't printed |
| Spy holes | drawn on the dogi, the himitsu and the chambers (Fig 4-55: "ANA", "SPY HOLE") | engine default, three in the door | differs: not sized or placed in the book |

## Build results

The build finishes with no errors. Chamber 301 ft³; heat loss 158.5 kW; priced materials
$20,002. Each floor steps 23.1 in above the last. **Information:** the 25 ft chimney is taller
than the 14.7 ft that Olsen's 3 × rise rule gives, counting the two modelled chambers only. Olsen
counts the dogi's run as well (p.101), so this is expected.

## Open questions

1. Fig 4-55 p.101: how wide and how tall are the side "door to chamber" openings? That would let
   the doors move to the side wall (`opening.each_chamber`).
2. Fig 4-53 p.100: how many 6 × 10 in exit flues leave the kedo?
3. Fig 4-55: at what heights are the spy holes ("ANA", "SPY HOLE") in the chamber walls?
