# Olsen 24 kit (`olsen-kit-24`)

Olsen's own 24 cu ft gas updraft kit, fired in eight hours. Design file:
`examples/olsen/olsen-kit-24.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.139, p.173–174 (flues, burners), pp.221–222 (propane, burners),
p.243 (installation); Fig 6-63 (p.172) for floor-burner placement. No drawing of this kiln.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Size | 24 cu ft | a 34.6 in cube | assumed shape |
| Burners | eight perimeter and two bottom (p.174) | ten MR-750: eight round the edge, `centre: 2` down the middle of the floor | matches; where under the setting the two go isn't printed (question 1) |
| Inlet | 50 in² | ten 2½ in ports, 49 in² | matches |
| Exit flue | 45 in² to start | 9 × 5 in | matches |
| Gas | natural gas, #32 orifice | natural gas, 8 in. w.c. line | matches |
| Door, walls, arch | not printed | hinged door, 7 in IFB, No. 1 arch | assumed |
| Spy holes | not printed | engine default | — |

No change in this pass.

## Key results

26 ft³; heat loss 11.5 kW; Ward's input 260,000 BTU/hr against 750,000 from ten MR-750s.

## Open questions for the user

1. Where do the two bottom burners fire: through the floor at its centre, under the setting?
   The model puts them down the floor's centre line, each in the middle of half its depth.
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

No drawing of this kiln: nothing to scale.
