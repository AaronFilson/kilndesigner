# Updraft test kiln 3, 3 × 3 × 5 ft stacking (`updraft-test-3`)

Example: [`examples/olsen/updraft-test-3.yaml`](../../../examples/olsen/updraft-test-3.yaml).
Research notes: `docs/research/olsen-kilns.md`, `updraft-test-1` to `updraft-test-4`.

"A similar kiln", 3 × 3 × 5 ft of stacking, fired with "a constant ½ to 1 cone difference" top to
bottom; widened to 4 × 4 ft (`updraft-test-4`) it evened out.

## Book pages

Olsen, *The Kiln Book*, 4th ed., p.74: text only. No figure.

## What's modelled

45 × 45 in (the stacking plus 4½ in each side), 60 in to the springline, a No. 1 arch; fourteen
MR-750 floor burners in 2½ in ports on natural gas at 8 in w.c.; 7 in IFB walls; a hinged door;
cone 10.

## Feature by feature

| Feature | Book (p.74) | Model | |
|---|---|---|---|
| Stacking | 3 × 3 × 5 ft | plus 4½ in each side | matches |
| Burners | in the floor | 14 MR-750, floor | place matches; count and model assumed |
| Draft | updraft | up | matches |
| Exit flue, damper, door, spy holes, walls, roof | not given | engine defaults and Olsen's kit practice | assumed |
| Evenness | ½ to 1 cone | not worked out | not expressible |

## Results from the build

74.8 ft³ inside; 2345 °F; 20.8 kW lost at top temperature.

## Open questions for the user

None the book can answer (p.74 is the only source).
