# Phoenix workshop kiln, New Hampshire, 1978 (`phoenix-nh`)

Example: [`examples/olsen/phoenix-nh.yaml`](../../../examples/olsen/phoenix-nh.yaml).
Research notes: `docs/research/olsen-kilns.md`, `phoenix-nh`.

"A 40 cubic foot variation" of George Wright's Phoenix kiln, built at the Phoenix workshops in New
Hampshire in 1978 and documented by Gerry Williams in *Studio Potter* (Vol. 7, No. 2). Wood fired.

## Book pages

Olsen, *The Kiln Book*, 4th ed., p.147: text and Fig 5-67 (a diagram with no dimensions). Figs
5-68 and 5-69 on the same page are Salzer's kiln, not this one.

## What's modelled

Only the volume and the layout are the book's. A 41.6 in cube (40 ft³) with a No. 1 arch, one
4½ in K-26 wall, a super-duty floor over one firebox under the floor (27 × 41.6 in, a 24 × 24 in
grate, 15 in above and below it), an inlet flue 27 × 4½ in, a 9 × 7½ in exit flue at the back, and
a 9 × 9 in chimney 18 ft tall sharing the back wall. Every size is assumed by Olsen's rules (see
the YAML).

## Scaling (step A, 2026-11-09)

Can't be scaled: Fig 5-67 (p.147, PDF 134, checked on the page image) is an isometric diagram with
no printed dimension and no countable courses, so the "Scaled" column is empty.

## Feature by feature

| Feature | Book (Fig 5-67, p.147) | Scaled | Model | |
|---|---|---|---|---|
| Volume | 40 ft³ | — | 40 ft³ | matches |
| Chamber shape | box with an arched roof (drawing) | — | box, sprung arch | matches |
| Firebox | one, Roman-arched, under the floor, with grate bars | — | one under the floor, `roof: roman` (crown at its 15 in, haunches filled), grate | matches |
| Firebox mouth | at the chimney end (drawing: entered under the chimney) | — | `mouth: back` | matches the drawing (question 2) |
| Inlet flue | one, rising at the front of the chamber | — | one, at the far end from the mouth: the front | matches |
| Exit flue | at floor level in the back wall | — | 9 × 7½ in at the foot of the back wall | matches (size assumed) |
| Chimney | shares the back wall | — | run 0 in, back wall | matches (size assumed) |
| Door | not shown | — | bricked front wall | assumed |
| Spy holes | not shown | — | engine's three in the door | engine default |
| Damper | not shown | — | engine's damper note | engine default |

## Results from the build

40 ft³; 2345 °F (cone 10, assumed); 15.7 kW lost at top temperature; 15 in above the grate and 15
in below, inside Olsen's 12–18 in for 30–100 ft³ kilns (p.199).

## Open questions for the user

1. Do you have *Studio Potter* Vol. 7, No. 2 (Gerry Williams on the Phoenix kiln)? Its sizes would
   replace every assumed one here: chamber, firebox and grate, inlet and exit flues, chimney.
2. Fig 5-67: is the firebox stoked from the chimney end (under the chimney), as the drawing reads?
