# Kannofen, Höhr-Grenzhausen (`kannofen`)

A wood-fired salt-glaze "updraught tunnel kiln": two fireboxes at one end, the flame running along
the tunnel to rows of exit flues in the top and sides. Design file: `examples/olsen/kannofen.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: pp.161–164; Fig 6-37 (p.163, exploded interior view, "NOT TO
SCALE, all measurements metric"), Fig 6-38 (section of kiln and shed), Fig 6-39 (fireboxes), Figs
6-40, 6-41 (photos).

## Changes in this pass

- Firebox length 1.22 m (borrowed from La Borne) → **1.40 m**, the "140cm" drawn along the ash
  pit's edge in Fig 6-37 (drawing)(?).

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Tunnel | 4.5 m long; four arch sections 1.04–1.07 m wide, 1.43–1.82 m to the crown; floor rises 38 cm (Fig 6-37) | `chamber.widths`: 1.05, 1.04, 1.07, 1.05 m at 1.5 m apart, each arch 3 in/ft of its width; mean height, sloped 4.83° | widths match; the level crown over the rising floor isn't modelled |
| Fireboxes | two, side by side, grate bars on both sides, brick wall between the ash pits, 140 cm (Fig 6-37) | two, 0.525 × 1.40 m | length matches; widths assumed; grates not sized |
| Firebox mouths | two arched mouths (photo, Fig 6-39) | — | not sized in the book |
| Flue channels | four, 15 cm wide, under setter tiles (Fig 6-37) | — | not expressible |
| Exit flues | rows along the top and down both sides (Fig 6-37, p.164) | one flue in the roof | not expressible (one flue) |
| Door | "BACK ENTRANCE", far end | bricked door, back wall | matches |
| Spy holes | none drawn | engine default, three in the door | — |
| Salt ports | into the top exit flue | — | not expressible |

2026-11-09 (B3): the four sections' widths (`chamber.widths`). The steel is sized for the widest,
1.07 m. The bricks aren't laid out for a width that changes, so the build gives the report and the
3D model as shells, with no masonry plan or bill of materials; the widths differ by 3 %, so
leaving them out (one 1.05 m box) gets the plans back at little cost to the numbers.

## Key results

7.33 m³; heat loss 53.5 kW; arch frame sized at the widest section, 1.07 m (the book doesn't show
what holds the arch).

## Open questions for the user

1. Fig 6-37: does the "140cm" mark the length of the firebox and ash pit?
2. Fig 6-37: the "25cm" and "40cm" (or "64cm") near the firebox: what do they span?
</content>
