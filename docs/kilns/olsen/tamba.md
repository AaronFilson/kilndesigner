# Tamba tube kiln, Tachikui (`tamba`)

Example: [`examples/olsen/tamba.yaml`](../../../examples/olsen/tamba.yaml).
Research notes: `docs/research/olsen-kilns.md`, `tamba`.

One of the 23 Tamba climbing tube kilns, "an anagama extended to approximately 120 ft", half above
ground, fired from a firebox (dogi) for about 36 hours and then side-stoked segment by segment. It
is one tube with no closed chambers: it narrows at the flue wall before each door, whose arched
openings support the vault (p.86, Figs 4-11, 4-12, 4-19; the owner, 2026-11-18).

## Book pages

Olsen, *The Kiln Book*, 4th ed.:

- p.85: text, Figs 4-6 (tatami bricks), 4-7 (the tube).
- p.86: text, Figs 4-10 (saggar setters, a tube section with a stoke hole), 4-11 (inside, photo),
  4-12 (chamber flues), 4-13 (firebox flues).
- p.87: Figs 4-14 to 4-16 (doors, the firebox section).
- p.88: Figs 4-18 to 4-20A (the end chamber).
- p.210: text (oil burners today).

## What's modelled

A level tube 78 in wide (scaled), 120 ft long in seven door segments under one vault, springing
12 in up and crowning at 3½ ft; 9 in K-26 walls; one firebox at the front 5 ft across and 6 ft deep
with four 9 × 18 in arched flues; a flue wall before each segment's door with four 12 × 22 in
holes; a 16 in stoke hole in each side of each segment (the owner's estimate, 2026-11-17);
cross-draft to an engine-sized chimney; cone 10 (assumed). The engine takes each segment as a
chamber and each flue wall as the wall between two. Not modelled: the earth against the walls'
lower half, so they lose to the room (only the floor is on the soil).

## Scaling (step A, 2026-11-09)

Fig 4-12 (p.86, PDF 72) prints only its holes' sizes: scaled from their 12" widths (13.65 px/in
at 300 dpi) and their 20"/24" heights (11.76 px/in); the 16 % between them is the spread. Fig
4-16 (p.87, PDF 73) from 3½' (9.19 px/in) and 6' (9.47); its 4' is drawn short (6.54) and
wasn't used. Fig 4-15 has no clear printed dimension. Readings in `scratch/scale-pz/scale.py`.

## Feature by feature

| Feature | Book | Scaled | Model | |
|---|---|---|---|---|
| Length | about 120 ft (p.85); 120–150 (Fig 4-7, flagged) | — | 7 × 205.7 in = 120 ft | matches |
| Segments | "6–8 door segments" (Fig 4-7) | — | 7 chambers | matches |
| Tube section | low vault over the setting (Figs 4-10, 4-12) | Fig 4-12 draws it rising about half its width | a sprung arch on 78 in, 12 in springline, 30 in rise | matches in shape |
| Tube height | first chamber 3½' (Fig 4-16) | 35–40½ in floor to crown (Fig 4-12, ±3 in) | 3½ ft to the crown | printed kept; the scale is lower by more than its spread (question 4) |
| Tube width | not printed | 73–84½ in inside (Fig 4-12, from the holes' 12" and 20"/24", ±6 in) | 78 in | scaled (was 5 ft assumed) |
| Firebox | 6' deep, 5' across at the flues (p.86); 4' from ground to first chamber floor (Fig 4-16) | — | 5 × 6 ft at the front | matches; the 4' drop not expressible |
| Firebox flues | four arched, "9 x 18"" (Fig 4-13) | drawn 2.6 times as tall as wide (16 and 20.7 px/in); the tube's far side is lost in the gutter, so nothing scaled | four 9 × 18 in | matches |
| Chamber flues | arched; "20 x 12"" on an outer hole, "24 x 12"" on an inner one; a legend for middle and last chambers' hatching (Fig 4-12) | four holes in the wall, all about 12 in wide; the outer two 17–19 in high, the inner two 21–24½ in (±2 in) | `draft.between`: four 12 × 22 in in each wall (the same area as two 12 × 20 and two 12 × 24) | scaled reading of the labels; one size per wall is all the schema takes (question 2) |
| Side stoke holes | 1½' apart (Fig 4-7); one in the vault (Fig 4-10) | round, 7–7¼ in across, centre 31–32 in above the chamber floor (Fig 4-16, from 3½' and 6', ±½ in) | `stoke_holes`: a 16 in round hole in each side of each segment, 32 in up | the owner's estimate for the series (2026-11-17): the scaled 7 in can't pass the bundles; covered after each stoking; how many to a segment isn't drawn (one a side taken) |
| Bundles | about 200 "15 x 30in" of split kindling and small pieces of wood (p.87; the metric "38 x 38 x 76cm") | — | round, 15 in across and 30 in long (the owner, 2026-11-18), 22.5–45.7 kg oven-dry packed as a cord (the dataset) | first read square from the metric, 28.6–58.1 kg (corrected 2026-11-18) |
| Doors | arched, bricked up, one per segment, a supporting wall in front (Fig 4-15) | can't be scaled: Fig 4-15's only dimensions are its own faint 3′ (?) and 2′ (?), and no other figure draws the door | one front-wall door | differs; `loading.opening` with `each_chamber` could place them, but no size is legible |
| Chimney | the end chamber's open holes, no stack (Figs 4-18, 4-19) | — | engine-sized stack | differs |
| Slope | not printed | — | level | assumed |
| Spy holes, damper | not described | — | engine defaults | engine default |

## Results from the build

About 2,220 ft³; 2345 °F; 215.7 kW lost at top temperature (1,780 ft³ and 200.7 kW on the 5 ft
width assumed before step A).

## Open questions for the user

1. Fig 4-15 (p.87): can the door's width and height be read in your copy (read 3′ (?) high, 2′ (?)
   wide on the scan)? With them each segment's door can go in its side wall.
2. Fig 4-12: which hatching is the middle chamber's flue holes and which the last's — is 20 × 12
   the middle and 24 × 12 the last? Scaled, the labels read as the holes' own sizes in one wall:
   the two outer holes 20 in high and the two inner 24 in, all 12 in wide. Modelled as four
   12 × 22 in (the same area). Is that the reading?
3. Is the tube's slope given anywhere for the Tamba kilns? (Answered 2026-11-17: Figs 4-17 and
   4-7 scale 8½–14°, and the owner's estimate for the series is 14°. It waits on a sloped tube in
   the engine.)
4. Fig 4-12 scales the tube 73–84½ in wide (78 in used, up from the 5 ft assumed) and 35–40½ in
   to the crown, below the faint 3½' of Fig 4-16 that is kept. Is the chamber wider than the
   firebox's 5 ft, and is 3½' its height?
5. How many side stoke holes to a segment (one a side is modelled, 32 in up)? (The size is
   answered, 2026-11-17: 16 in, the owner's estimate for the series, in the design since
   2026-11-18. The count is still open.)
6. ~~Is Tamba one tube or a row of chambers?~~ Answered (the owner, 2026-11-18): one half-buried
   tube with no closed chambers, narrowing at its arched supports (`11-17-26-inputs.md` §9).
7. The fire mouth: the book has it open while side stoking (pp.86–87), but the slow test corner
   still shuts it. That is to correct, not a question.
