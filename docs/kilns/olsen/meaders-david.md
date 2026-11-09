# David Meaders's groundhog (`meaders-david`)

A small wood groundhog adapted from his grandfather Cheever's design: a half-cylinder chamber, a
full-width firebox at the front, the chimney at the back. Design file:
`examples/olsen/meaders-david.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.115 (Fig 4-105 diagram, Figs 4-106, 4-107 photos).

## Changes in this pass

- Comments: eight exit flues drawn along the foot of the back wall; the door drawn dashed in the
  front arch, left of centre, unsized; a row of unlabelled openings at the front arch's foot.
- Engine: this file failed to build in the CLI (the plan section crashed on an arch springing from
  the floor). Fixed in `drawings.py`; see the report.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 5 ft wide, 6 ft long, 30 in to the crown | half-circle from the floor, 60 × 72 in | matches |
| Firebox | 4 ft long, front arch to bag wall | 60 × 48 in, no grate | matches |
| Bag wall | 18 in (faint) | — | not expressible |
| Inlet flue | 9 × 4½ in, count not printed | one 4½ × 9 in inlet | count not printed |
| Exit flues | 7½ (faint) × 4½ in; eight drawn (Fig 4-105) | eight 4½ × 7½ in, spread evenly along the back wall (`draft.exits`) | matches (count and places from the drawing) |
| Chimney | 8 ft, "9" INSIDE" | 60 × 9 in, 8 ft | matches (width read as the kiln's) |
| Door | dashed in the front arch, left of centre, no size | engine door in the front | position and size not set |
| Spy holes | not drawn | engine default | — |

## Key results

58.9 ft³; heat loss 13.3 kW; chimney 8 ft against the engine's 5–10.2 ft; draft 0.073 in. w.c.

## Open questions for the user

1. Fig 4-105: are there eight exit flues, and how many inlet flues through the bag wall?
2. The door's width and height, and the openings along the foot of the front arch: air holes?
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| Exit flue places | 4½ × 7½ in | eight drawn | 26½, 19½, 13½, 7 in left, 0, 6½, 13½, 21½ in right (Fig 4-105, from the 5' span and arrow, ±1 in) | `places` |
| Door | dashed, in the front arch | — | 19½ in wide, 5½ in left of centre, 25 in tall (±1½ in) | not entered: `loading.opening` needs a wall, and this arch springs from the floor |

The figure is a perspective drawn about twice as tall as wide (the 30" gives 13.3 px/in up, the 5' 6.8–7.0 across), so each axis is scaled alone. Question: is the door about 1½ ft wide and 2 ft high?
