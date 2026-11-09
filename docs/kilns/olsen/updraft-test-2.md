# Updraft test kiln 2, 2 × 3 × 4 ft stacking (`updraft-test-2`)

Example: [`examples/olsen/updraft-test-2.yaml`](../../../examples/olsen/updraft-test-2.yaml).
Research notes: `docs/research/olsen-kilns.md`, `updraft-test-1` to `updraft-test-4`.

Test kiln 1 cut 1 ft shorter: 2 × 3 × 4 ft of stacking, "perfectly even" with floor burners.

## Book pages

Olsen, *The Kiln Book*, 4th ed., p.74: text only. No figure.

## What's modelled

As `updraft-test-1` but 48 in to the springline: 33 × 45 in, twelve MR-750 floor burners in 2½ in
ports on natural gas at 8 in w.c., 7 in IFB walls, a No. 1 arch, a hinged door, cone 10.

## Feature by feature

| Feature | Book (p.74) | Model | |
|---|---|---|---|
| Stacking | 2 × 3 × 4 ft | plus 4½ in each side, 48 in high | matches |
| Burners | in the floor | 12 MR-750, floor | place matches; count and model assumed |
| Draft | updraft | up | matches |
| Exit flue, damper, door, spy holes, walls, roof | not given | engine defaults and Olsen's kit practice | assumed |

## Results from the build

43.6 ft³ inside; 2345 °F; 15.2 kW lost at top temperature.

## Open questions for the user

None the book can answer (p.74 is the only source).
