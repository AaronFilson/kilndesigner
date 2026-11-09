# Jun Kaneko's car kiln (`kaneko-car`)

A 500 cu ft gas updraft car kiln, a cube, fired extremely slowly on 32 atmospheric burners round the
floor. Design file: `examples/olsen/kaneko-car.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.170 (text, Fig 6-60 photo), p.171 (text), p.172 (text; Fig 6-63
burner placement for updrafts; Fig 6-64 trolley and suspended door).

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 8 ft wide, 9 ft deep, 8 ft tall; 500 cu ft (p.170–171) | 8 × 9 × 8 ft to the springline, arch on top | matches (height reading assumed) |
| Car | cart 7 ft wide (p.171) | car loading, front | matches; cart width not expressible |
| Burners | 32 atmospheric, ten each side, six front and back, 9 in combustion width (p.172) | 32 MR-100 floor burners, `per_side: 10`, `per_end: 6` | matches; the 9 in channel not expressible (the engine's combustion space) |
| Burner spacing | Fig 6-63: 9–12 in from the corners, 12–24 in apart | engine spacing (about 10 in on the long sides) | close; not set |
| Door | hung from an overhead I-beam on two half-ton trolleys, spring latches (Fig 6-64) | the front wall hung on its own frame, two trolleys of 1000 lb (`loading.hung`); its masonry, 1,757 lb, checked against their 2,000 lb | matches; the beam, frame and latches aren't sized (not printed) |
| Exit flue, chimney, damper | not printed | engine default | — |
| Spy holes | not printed | engine default, three in the door | assumed |

2026-11-09 (B3): the door hangs on its own frame (`loading.hung`), from Fig 6-64's two half-ton
trolleys, half a ton taken as 1000 lb. The photo is "a similar suspended kiln door", so the
trolleys may be that door's.

## Key results

633 ft³ (Ward's way) against the printed 500 cu ft of stacking; heat loss 70.5 kW; Ward's input
6.32 million BTU/hr, twice the 3.2 million the 32 MR-100s give at 8 in. w.c. (the book's slow,
several-day firing fits that); exit flue 864 in²; arch frame L8×8×½.

## Open questions for the user

1. Which burner did Kaneko use, and at what rating and pressure? The model takes the MR-100.
2. Is the 8 ft height to the springline or to the crown, and is the roof an arch or flat?
</content>
