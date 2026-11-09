# Tamba tube kiln, Tachikui (`tamba`)

Example: [`examples/olsen/tamba.yaml`](../../../examples/olsen/tamba.yaml).
Research notes: `docs/research/olsen-kilns.md`, `tamba`.

One of the 23 Tamba climbing tube kilns, "an anagama extended to approximately 120 ft", half above
ground, fired from a firebox (dogi) for about 36 hours and then side-stoked chamber by chamber.

## Book pages

Olsen, *The Kiln Book*, 4th ed.:

- p.85: text, Figs 4-6 (tatami bricks), 4-7 (the tube).
- p.86: text, Figs 4-10 (saggar setters, a tube section with a stoke hole), 4-11 (inside, photo),
  4-12 (chamber flues), 4-13 (firebox flues).
- p.87: Figs 4-14 to 4-16 (doors, the firebox section).
- p.88: Figs 4-18 to 4-20A (the end chamber).
- p.210: text (oil burners today).

## What's modelled

A level tube 5 ft wide, 120 ft long in seven door segments, a half-round vault springing 12 in up
and crowning at 3½ ft; 9 in K-26 walls; one firebox at the front 5 ft across and 6 ft deep with
four 9 × 18 in arched flues; cross-draft to an engine-sized chimney; cone 10 (assumed).

## Feature by feature

| Feature | Book | Model | |
|---|---|---|---|
| Length | about 120 ft (p.85); 120–150 (Fig 4-7, flagged) | 7 × 205.7 in = 120 ft | matches |
| Segments | "6–8 door segments" (Fig 4-7) | 7 chambers | matches |
| Tube section | low vault over the setting (Fig 4-10) | half-round on 5 ft, 12 in springline | matches in shape |
| Tube height | first chamber 3½' (Fig 4-16) | 3½ ft to the crown | matches |
| Tube width | not printed | 5 ft (the firebox's) | assumed |
| Firebox | 6' deep, 5' across at the flues (p.86); 4' from ground to first chamber floor (Fig 4-16) | 5 × 6 ft at the front | matches; the 4' drop not expressible |
| Firebox flues | four arched, "9 x 18"" (Fig 4-13) | four 9 × 18 in | matches |
| Chamber flues | arched; "20 x 12"" and "24 x 12"", middle and last chambers (Fig 4-12) | the engine's 4½ × 9 in | not expressible |
| Side stoke holes | 1½' apart (Fig 4-7); one in the vault (Fig 4-10) | none | not expressible |
| Doors | arched, bricked up, one per segment, a supporting wall in front (Fig 4-15) | one front-wall door | differs; `loading.opening` with `each_chamber` could place them, but no size is legible |
| Chimney | the end chamber's open holes, no stack (Figs 4-18, 4-19) | engine-sized stack | differs |
| Slope | not printed | level | assumed |
| Spy holes, damper | not described | engine defaults | engine default |

## Results from the build

About 1,780 ft³; 2345 °F; 200.7 kW lost at top temperature.

## Open questions for the user

1. Fig 4-15 (p.87): can the door's width and height be read in your copy (read 3′ (?) high, 2′ (?)
   wide on the scan)? With them each segment's door can go in its side wall.
2. Fig 4-12: which hatching is the middle chamber's flue holes and which the last's — is 20 × 12
   the middle and 24 × 12 the last?
3. Is the tube's slope given anywhere for the Tamba kilns?
