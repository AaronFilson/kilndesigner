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
| Exit flues | 7½ (faint) × 4½ in; eight drawn (Fig 4-105) | one 4½ × 7½ in | count not expressible (one flue) |
| Chimney | 8 ft, "9" INSIDE" | 60 × 9 in, 8 ft | matches (width read as the kiln's) |
| Door | dashed in the front arch, left of centre, no size | engine door in the front | position and size not set |
| Spy holes | not drawn | engine default | — |

## Key results

58.9 ft³; heat loss 13.3 kW; chimney 8 ft against the engine's 5–10.2 ft; draft 0.073 in. w.c.

## Open questions for the user

1. Fig 4-105: are there eight exit flues, and how many inlet flues through the bag wall?
2. The door's width and height, and the openings along the foot of the front arch: air holes?
</content>
