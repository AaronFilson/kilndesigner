# Olsen 50 car kiln (`olsen-kit-50`)

A 50 cu ft Olsen gas updraft car kiln. Design file: `examples/olsen/olsen-kit-50.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.170 (caption 6-61), p.171 (photo), p.174 (exit flue); Fig 6-63
(p.172) for floor-burner placement.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Size | 50 ft³ | a 44.2 in cube | assumed shape |
| Exit flue | 90 in² to start | 9½ × 9½ in in the arch | matches |
| Inlet | about 20 % less than the exit (p.174 rule) | fifteen 2½ in ports, 74 in² | matches the rule |
| Car | a car kiln (photo) | see the design file | as modelled there |
| Door, walls, arch | not printed | engine and kit defaults | assumed |
| Spy holes | not printed | engine default | — |

No change in this pass.

## Key results

54.2 ft³; heat loss 17.7 kW; Ward's input 541,000 BTU/hr on fifteen MR-750s.

## Open questions for the user

1. The kiln's inside sizes and burner count, if a kit sheet survives.
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

Only a photo: nothing to scale.
