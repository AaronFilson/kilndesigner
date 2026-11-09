# Suzuki cooperative climbing kiln, Kyoto (`suzuki-kyoto`)

Example: [`examples/olsen/suzuki-kyoto.yaml`](../../../examples/olsen/suzuki-kyoto.yaml).
Research notes: `docs/research/olsen-kilns.md`, `suzuki-kyoto`.

A seven-chamber Kyoto wood climbing kiln on Torincho Street, fired on bundles of wood in about 56
hours to cone 8–9, chambers 1 and 2 to cone 10.

## Book pages

Olsen, *The Kiln Book*, 4th ed., p.93: text and Fig 4-35 (a site plan of the cooperative, not a
construction drawing).

## What's modelled

Seven chambers 4.3 m across, 1.4 m along the draft and 2 m to the crown, climbing at 18.4° (the
Bidai kiln's 3 to 1); a 9 in trough firebox (himae) along each chamber's front; 9½ in walls and a 9
in arch of medium-duty firebrick; cross-draft to a chimney the engine sizes.

## Feature by feature

| Feature | Book | Model | |
|---|---|---|---|
| Chambers | seven in series (p.93, Fig 4-35) | seven | matches |
| Chamber size | "14 x 6 1/2 x 4 1/2 ft (4.3 x 2 x 1.4m)" (p.93) | 4.3 m × 1.4 m, 2 m to the crown | matches (reading of which is which is the note's) |
| Chamber proportion | drawn wide across, short along the draft (Fig 4-35) | the same | matches |
| Main firebox | half-round, below chamber 1 ("KILN", Fig 4-35); stoked 15 h to 1000 °C | none | not expressible alongside the himae |
| Side stoking | each chamber from both sides (p.93) | himae trough per chamber | matches in kind |
| Doors and stoke porches | a bay on both sides of each chamber (Fig 4-35) | one bricked door in the front wall | differs; `loading.opening.each_chamber` exists but no size is printed |
| Chimney | round, at the top of the kiln (Fig 4-35) | engine-sized | not sized in the book |
| Spy holes | not shown | engine's three | engine default |
| Cones by chamber | 10, 10, 8–9 … bisque Δ1 (Fig 4-35) | `firing.chamber_cones`: 10, 10, 9, 9, 9, 9, 1 (8–9 taken as 9, the hotter) | matches; the heat loss takes each chamber at its own cone |
| Slope, walls, arch | not given | 18.4°, 9½ in, 9 in (assumed) | assumed |

## Results from the build

77.9 m³ in all; 1285 °C; 777.4 kW lost with each chamber held at its own cone (803.5 kW with all
seven at cone 10, the steady-state upper bound used before 2026-11-09).

## Open questions for the user

1. Fig 4-35: are the bays drawn on both sides of each chamber doors, stoke porches, or both?
2. Is the round chimney's size given anywhere for this kiln?
3. The chambers 4–7 bundle count lost at the gutter on p.93: can it be read in your copy?
