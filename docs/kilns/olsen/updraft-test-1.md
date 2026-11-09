# Updraft test kiln 1, 2 × 3 × 5 ft stacking (`updraft-test-1`)

Example: [`examples/olsen/updraft-test-1.yaml`](../../../examples/olsen/updraft-test-1.yaml).
Research notes: `docs/research/olsen-kilns.md`, `updraft-test-1` to `updraft-test-4`.

One of four gas updraft test kilns with burners in the floor behind Olsen's Design Principle 1. A
2 × 3 ft base stacked "5ft (152cm)-plus-high" fired ½ to 1 cone apart top to bottom, whatever the
schedule; cut 1 ft shorter (`updraft-test-2`) it fired evenly.

## Book pages

Olsen, *The Kiln Book*, 4th ed., p.74: text only (second scan). There is no figure of these kilns.

## What's modelled

Stacking 2 × 3 × 5 ft plus 4½ in combustion space round it: 33 × 45 in, 60 in to the springline, a
No. 1 arch (4.13 in rise); twelve GACO MR-750 venturi burners in 2½ in floor ports, natural gas at
8 in w.c.; 4½ in K-26 backed by 2½ in K-23 walls; a hinged front door; cone 10; the exit flue the
engine's. Everything but the stacking size and floor burners is assumed (see the YAML).

## Scaling (step A, 2026-11-09)

Nothing to scale: p.74 is text only, with no figure of these kilns.

## Feature by feature

| Feature | Book (p.74) | Scaled | Model | |
|---|---|---|---|---|
| Stacking | 2 × 3 ft, 5 ft-plus high | — | 2 × 3 × 5 ft, plus 4½ in each side | matches ("plus" not sized) |
| Burners | "in the floor" | — | 12 MR-750, floor | matches in place; count and model assumed |
| Draft | updraft | — | up | matches |
| Exit flue, damper, door, spy holes, walls, roof | not given | — | engine defaults and Olsen's kit practice | assumed |
| Evenness top to bottom | ½ to 1 cone | — | not worked out | not expressible |

## Results from the build

54 ft³ inside; 2345 °F; 17.2 kW lost at top temperature.

## Open questions for the user

1. None the book can answer: p.74 is the only source. If you know who built these kilns or where
   they are written up, that would size the burners, flues and walls.
