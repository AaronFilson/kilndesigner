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
channel to a 24 × 24 in chimney 30 ft tall, about 27½ ft away. Walls 18 in, dome and floor 9 in
of medium-duty firebrick (the thicknesses and brick are assumptions, said in the YAML).

## Feature by feature

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 7' diameter, 5' to springline, 2' dome (Figs 5-10, 5-11) | the same | matches |
| Volume | "approximately 385 cu. ft" (p.133) | 235 ft³ from the drawn sizes | differs (book flagged) |
| Fireboxes, count | four, arched over (Fig 5-10) | four | matches |
| Fireboxes, place | on the diagonals, evenly round the wall (Fig 5-10) | `front-left`, `front-right`, `back-left`, `back-right`: each against the front or back wall, its middle on the 45° line, square to that wall | matches in place; drawn square, not turned to the diagonal |
| Firebox width | 24" inside, 9" outer wall, 40" overall (Fig 5-11) | 24 in | matches |
| Firebox height | 15", 15" and 36" up its side, which is which unclear (Fig 5-11) | 30 in above the grate, 36 in ash pit (?) | changed in this pass, (?) |
| Grate | 24 × 24 in, 4 ft² (p.207, Fig 8-18); round bars, four drawn | 24 × 24 in, no bar gap | matches (bars not sized) |
| Firebox flue entrance | 15 × 24 in (p.134); drawing 16" high, sill 24" up | 24 wide × 15 high | matches the text |
| Stoking hole | 15" × 13" (Fig 5-11) | 15 × 13 in | matches |
| Coal pit outside | 4' × 2' at each firebox (Fig 5-10) | `coal_pit` 24 in across, 48 in out, depth not given; reported, not drawn | matches (which way is across the mouth: question 5) |
| Notched wall | 9" deep, 2' wide, 3' long at each firebox (p.134) | none | not expressible |
| Floor exit flues | twelve 6" × 6", evenly spaced (Fig 5-10) | one flue port | not expressible |
| Flue collection channel | 12" deep under a 9" floor (Fig 5-11) | floor on the ground; not drawn | not expressible |
| Flue channel to chimney | 24" × 16" (Fig 5-10) | flue port 24 × 16 in | matches |
| Chimney | 24" × 24" inside, 30' tall, 25–30' away (Fig 5-10) | 24 × 24 in, 30 ft, run 27½ ft | matches |
| Damper | in the chimney entrance (Fig 5-10) | engine's damper note (a shelf in a slot) | engine default |
| Door | arched, between two fireboxes (Fig 5-10) | the front wall is a bricked door | differs |
| Spy holes | not drawn | engine's three in the door | engine default |
| Dome vents | "cooling & vapor holes" (Fig 5-11) | none | not expressible |
| Walls, dome thickness | not given | 18 in walls, 9 in dome (assumed) | assumed |

## Results from the build

235 ft³; 2345 °F (cone 10); 89.4 kW lost at top temperature; the dome pushes 146 lb/ft round the
wall's top, a ring tension of 558 lb, held by a ¼ × 2 in band. Coal per firing isn't worked out
(no heating value for coal in `docs/research/`).

## Open questions for the user

1. Fig 5-11, left side of the firebox: the three bands are 15", 15" and 36". Is the grate at the
   line between the two 15" bands, or between the lower 15" and the 36"? And does the 36" run from
   the ground to the grate (the ash pit), or to the chamber floor?
2. Fig 5-11, the "AIR SOURCE AND COAL ASH PIT 36" X 24"" label at the right: is 36" its height and
   24" its width?
3. Is the chamber wall's thickness readable anywhere? The firebox's 40" overall (24" + 9" + 7"?)
   doesn't say.
4. The door in Fig 5-10: can its width or height be read?
5. Fig 5-10: is the coal pit's 4' across the firebox's mouth or out from it? The model takes 2 ft
   across and 4 ft out. Is its depth readable?
