# Singh's round coal downdraft, Delhi Blue Pottery (`singh-coal`)

Example: [`examples/olsen/singh-coal.yaml`](../../../examples/olsen/singh-coal.yaml).
Research notes: `docs/research/olsen-kilns.md`, `singh-coal`.

Mansimran Singh's round, domed, natural-draft downdraft, fired with steam coal (Grade B) from four
fireboxes to cone 10 in 19 to 20 hours.

## Book pages

Olsen, *The Kiln Book*, 4th ed.:

- p.133: text, Fig 5-9 (photo), Table 5-1 (the stoking schedule).
- p.134: Fig 5-10 (floor plan), Fig 5-11 (cross-section), text on the notched wall.
- p.135: Figs 5-12 to 5-16, the setting.
- p.207: Fig 8-18, grate area per firebox.

## What's modelled

A 7 ft round chamber, 5 ft to the springline, a 2 ft dome; four coal fireboxes on the diagonals,
each with a 4 × 2 ft coal pit outside, with 24 × 24 in grates, a 15 × 24 in flue into the chamber and a 15 × 13 in stoking hole each; a 24 × 16 in flue
channel to a 24 × 24 in chimney 30 ft tall, about 27½ ft away. Walls 13½ in (scaled), dome and
floor 9 in of medium-duty firebrick (the dome and floor thicknesses and the brick are
assumptions, said in the YAML). Twelve floor flues at their printed places; three dome vents.

## Scaling (step A, 2026-11-09)

Figs 5-10 and 5-11 (p.134, PDF 121) carry printed dimensions, so both were scaled
(`scratch/scale-pz/scale.py` holds every pixel reading). Fig 5-11 from 7' (7.49 px/in at
200 dpi), 5' (7.02) and 40" (7.00); its 2' dome rise is drawn about 15 % tall (8.21) and wasn't
used. Fig 5-10 from 7' (7.20) and the 24" chimney (7.17). The spread between the scales is the
± given, at least ±1 in for reading the lines.

## Feature by feature

| Feature | Book | Scaled | Model | |
|---|---|---|---|---|
| Chamber | 7' diameter, 5' to springline, 2' dome (Figs 5-10, 5-11) | — | the same | matches |
| Volume | "approximately 385 cu. ft" (p.133) | — | 235 ft³ from the drawn sizes | differs (book flagged) |
| Fireboxes, count | four, arched over (Fig 5-10) | — | four | matches |
| Fireboxes, place | on the diagonals, evenly round the wall (Fig 5-10) | — | `front-left`, `front-right`, `back-left`, `back-right`: each against the front or back wall, its middle on the 45° line, square to that wall | matches in place; drawn square, not turned to the diagonal |
| Firebox width | 24" inside, 9" outer wall, 40" overall (Fig 5-11) | — | 24 in | matches |
| Firebox height | 15", 15" and 36" up its side, which is which unclear (Fig 5-11) | grate bars drawn 21–23½ in under the firebox's roof, 32½–36 in above the ground (±1¼ in, both fireboxes, from 7', 5' and 40") | 22½ in above the grate (9 courses), 36 in ash pit | scaled; disagrees with the 15 + 15 = 30 in reading (question 1) |
| Grate | 24 × 24 in, 4 ft² (p.207, Fig 8-18); round bars, four drawn | — | 24 × 24 in, no bar gap | matches (bars not sized) |
| Firebox flue entrance | 15 × 24 in (p.134); drawing 16" high, sill 24" up | — | 24 wide × 15 high | matches the text |
| Stoking hole | 15" × 13" (Fig 5-11) | — | 15 × 13 in | matches |
| Coal pit outside | 4' × 2' at each firebox (Fig 5-10) | the pit's outer side, across the mouth, 22 in (±1 in, from 7' and the 24" chimney): the 2' side | `coal_pit` 24 in across, 48 in out, depth not given; reported, not drawn | matches; the scale answers which way (depth still not drawn) |
| Notched wall | 9" deep, 2' wide, 3' long at each firebox (p.134) | — | none | not expressible |
| Floor exit flues | twelve 6" × 6", evenly spaced; spacings 12", 10" and 18" printed between them (Fig 5-10) | not needed: placed by the printed spacings; the drawn grid is near the plan's scale (6.5–8.2 px/in against 7.2) | twelve 6 × 6 in at their places (`draft.exits.places`): two rows of four at ±12 in across, ±9 and ±27 in along, one more each side at ±28 in across, ±9 in along; the set centred | matches (printed) |
| Flue collection channel | 12" deep under a 9" floor (Fig 5-11) | — | floor on the ground; not drawn | not expressible |
| Flue channel to chimney | 24" × 16" (Fig 5-10) | — | `draft.connection` 24 × 16 in | matches |
| Chimney | 24" × 24" inside, 30' tall, 25–30' away (Fig 5-10) | — | 24 × 24 in, 30 ft, run 27½ ft | matches |
| Damper | in the chimney entrance (Fig 5-10) | plan only: no height to scale | engine's damper note (a shelf in a slot) | engine default |
| Door | arched, between two fireboxes (Fig 5-10) | 21½–22½ in wide (±1 in); its height isn't drawn (plan only) | the front wall is a bricked door | differs |
| Spy holes | not drawn | — | engine's three in the door | engine default |
| Dome vents | "cooling & vapor holes" (Fig 5-11) | three in the section, about 2¾ in across, at the crown and 27–29 in either side (±1 in, from 7', 5' and 40") | `openings.vents`: three 2½ × 2½ in (a course) through the dome, at 0 and ±28 in across | scaled; how many round the dome isn't drawn, and the section's line is taken as side to side |
| Walls, dome thickness | not given | wall 13½–14 in hatched, plus 8½ in solid "extra brick bracing between fire boxes" (±1 in, from 7' and the 24" chimney) | 13½ in walls (1½ bricks), 9 in dome (assumed) | scaled wall; the bracing isn't modelled; the dome's thickness assumed |

## Results from the build

235 ft³; 2345 °F (cone 10); 98.5 kW lost at top temperature (89.4 kW with the 18 in walls
assumed before step A); the dome pushes 146 lb/ft round the
wall's top, a ring tension of 558 lb, held by a ¼ × 2 in band. Coal per firing isn't worked out
(no heating value for coal in `docs/research/`).

## Open questions for the user

1. Fig 5-11, left side of the firebox: the three bands are 15", 15" and 36". Is the grate at the
   line between the two 15" bands, or between the lower 15" and the 36"? And does the 36" run from
   the ground to the grate (the ash pit), or to the chamber floor? Scaled (step A), the grate bars
   are drawn inside the lower 15" band, 21–23½ in under the firebox's roof and 32½–36 in above
   the ground: the model now takes 22½ in above the grate, not 30. Which is right?
2. Fig 5-11, the "AIR SOURCE AND COAL ASH PIT 36" X 24"" label at the right: is 36" its height and
   24" its width?
3. The wall scales 13½–14 in on the plan (Fig 5-10), with 8½ in of solid bracing outside it
   between the fireboxes, but the section (Fig 5-11) draws the firebox's inner wall about 7 in
   (40" − 24" − 9"). Is 13½ in right for the chamber wall?
4. The door in Fig 5-10 scales about 22 in wide; its height isn't drawn. Is it known? With it the
   door could go in as `loading.opening`.
5. Fig 5-10: the pit's 2' side scales across the mouth, so 4' runs out (as modelled). Is its
   depth known?
6. The dome vents: how many are there round the dome (the section shows three), and are they
   round or square?
