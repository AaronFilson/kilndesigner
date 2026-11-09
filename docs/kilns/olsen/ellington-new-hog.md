# Kim Ellington's new hog

Design file: `examples/olsen/ellington-new-hog.yaml`. A wood-fired salt groundhog whose ware
chamber tapers to the chimney, stoked from the front and through side stoke holes.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.114 (text; Fig 4-95 plan, Fig 4-96 side view "inside
dimensions", Fig 4-97 front view, Figs 4-98 to 4-100 photos), p.115 (Figs 4-101 to 4-104 photos:
taper, side stoke and salt ports, front with roller conveyor). Notes:
`docs/research/olsen-kilns.md`.

## Feature by feature

| Feature | Book | Model | |
|---|---|---|---|
| Plan | 24' overall; firebox 4' × 10'; ware 10' W × 10' L, then 8' L tapering to 4' W; neck 3' W (?) (Fig 4-95) | `chamber.widths`: 10 ft to 10 ft along, straight to 4 ft at 18 ft | matches; the neck isn't modelled |
| Roof | groundhog arch from the floor; 29" h at the chimney end (Fig 4-96) | sprung arch from the floor, rise 38½ in on 10 ft, keeping its shape as the plan narrows: 15.4 in at the 4 ft end | crown height assumed; the 29 in is more than a circular arch from the floor rises on 4 ft (24 in) |
| Firebox | front, dug 3.5' below the ware floor, 4' wide in section (Fig 4-96) | front, 10 ft × 4 ft | depth below floor not expressible |
| Inlet flues | "(3) INLET FLUE 13.5 X 9"" (Fig 4-95) | 3 × 13½ × 9 in | matches |
| Front stoke holes | 13.5" × 16", air holes 13.5" × 9" under each; Fig 4-97 draws three (left, centre, right, half cut off) | one 13½ × 16 in stoke hole | count and air holes not expressible |
| Side stoke holes | two rows, "spaced every 27"", six a row drawn (Fig 4-96); also salt ports (Fig 4-102) | — | expressible now (`stoke_holes`); not given, as their size and height aren't printed |
| Door | central, in the arched front (Fig 4-97, Fig 4-103) | whole front, bricked | opening size not printed |
| Chimney | 14' (Fig 4-96); label "4'5" 3'" (?) | 14 ft, section by engine | section unreadable |
| Exit flues | not drawn | engine default | — |
| Spy holes | none drawn | engine default | — |

## Results (build of 2026-11-09, with the taper)

327 ft³ (368 ft³ as a box of the mean width); 2345 °F (cone 10); 48.95 kW at the top. The masonry
holds the widest section's thrust, 258 lb per foot of arch hot. The 3D model is drawn as shells
in 16 slices along the taper; the bricks aren't laid out or priced for a plan whose width changes
(no masonry plan or bill of materials), so the build writes the report and model only.

## Open questions

- Fig 4-97: are there three front stoke holes (left, under the door, right) or two (Fig 4-103)?
- Fig 4-97: the door's width and height.
- Fig 4-96: the crown height in the straight section; is "29" h" the inside height at the chimney?
  If so, the arch over the narrow end isn't a circle from the floor (it can rise at most 24 in on
  4 ft), and the model's 15.4 in there, its shape kept from the straight section, is low.
- Fig 4-95: the chimney label "4'5" 3'": the chimney's inside section?
- The side stoke holes' size and their height above the floor in each row.
