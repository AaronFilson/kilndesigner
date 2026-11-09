# Chappell's Domura salt kiln (Olsen): the book against the model

_Built 2026-11-08 from `examples/olsen/chappell-domura.yaml`. Rebuild with
`uv run kilndesigner build examples/olsen/chappell-domura.yaml --out out/chappell-domura`._

## The kiln

John Chappell's tandem kiln at Domura, Japan (1962): a two-chamber kiln of 2 × 40 ft³ and a salt
kiln of 50 ft³. They share a common wall and one chimney. The model is the salt chamber only.

## Sources

Olsen, *The Kiln Book*, 4th ed.:
- p.33: brick and mortar.
- p.126: text, Fig 4-148 (foundation), Fig 4-149 (plan), Fig 4-150 (sketch of the two chambers),
  Fig 4-151 (photo).
- p.243: the shed fire.

Notes: `docs/research/olsen-kilns.md`, `chappell-domura`.

## What's modelled

- Chamber: 3 × 5 ft, 3 ft to the springline, with a sprung arch across the 3 ft rising 6 in (the
  rise is assumed), 50.1 ft³.
- Walls: 9 in of medium-duty firebrick.
- Floor: on the ground.
- Firebox: a wood firebox across the front, 9 in wide, on its floor. That floor is 30 in below the
  chamber floor (`step`, new).
- Chimney: 25 ft, 12 in square tapering to 9 in.

## Feature by feature

| Feature | Book (Fig 4-149 unless noted) | Model | Status |
|---|---|---|---|
| Chamber | 3' × 5', "3' TALL", 50 ft³ (p.126) | 3 × 5 × 3 ft plus a 6 in rise = 50.1 ft³ | matches (the rise is assumed) |
| Walls | "(9" WALLS)", intermediate-duty brick (p.33) | 9 in medium-duty | matches |
| Floor/foundation | concrete block, red brick, medium-duty firebrick (p.126, Fig 4-148) | medium-duty on red brick, on the ground | matches |
| Firebox | front, "30" below floor"; its width isn't printed | 9 in wide (taken from the chamber kiln's firebox), step 30 in | matches the depth; the width is assumed |
| Inlet flues | three openings in the front wall (drawing), not sized | none | differs: they can't be sized |
| Exit flues | three openings into the collection box (drawing), box 9" | one flue sized by the engine | not expressible (one exit flue) |
| Chimney | "12 X 12" tapering to 9 X 9" 25' TALL" | same | matches |
| Damper | "DRAFT HOLE" at the chimney | the engine's shelf damper | partly |
| Door | a gap of about 3 ft in the left side wall, mid-length (drawing (?)) | front wall | differs: the engine refuses a door under a sprung arch's springing wall |
| Spy holes | none drawn | the engine's three | differs |
| Arch | Fig 4-150 sketches arched roofs; direction and rise not printed | across the 3 ft, 6 in rise | assumed |
| Two-chamber kiln | 4' wide, 31" chambers, firebox 12" below floor, 18" side opening | not modelled | not expressible (no kilns side by side sharing a wall) |
| Salt ports | p.243 | none | not expressible |

## Results from the build

- Chamber 50.1 ft³; 2345 °F; heat loss 54.31 kW; priced materials $5,521.
- Warning: the firebox floor is 2.2 times the chimney's section, outside the 4–10 times of Olsen's
  wood kilns. The 9 in firebox width is an assumption, so this warning comes from that assumption.
- The 25 ft chimney is taller than the 13 ft that Rule 5 gives as the most for this chamber. The
  printed chimney draws both kilns.

## Open questions for the user

1. Fig 4-149 p.126: is the open stretch of the salt chamber's left wall, about 3 ft, the door? If
   it is, does the arch run along the 5 ft length (springing from the front and back walls, as at
   Bowen Mountain)? That would let the door sit in the side wall.
2. Fig 4-149: how wide is the salt kiln's firebox, front to back, and how big are its three inlet
   flues?
3. Fig 4-149: how big are the three exit flues into the collection box?
4. Spy holes: does any photo or page show where they were?

## Scaled off the figures (step A, 2026-11-09)

Fig 4-149 (p.126) scaled from the salt chamber's 3' and 5' and the "9" WALLS" (7.9, 9.9 and 7.2
px/in). The plan isn't to scale across the sheet: the chamber kiln beside it draws its 4' at 6.4
px/in and its 31" at 13 px/in. Fig 4-150 is a sketch with no dimension. Readings in
`scratch/scale-a/measure.py`.

| Feature | printed | drawing | scaled | In the model |
|---|---|---|---|---|
| Inlet flues | — | three openings in the front wall | each 3–4 in wide (a half-brick, 4½ in, read loosely); height not in a plan | not entered (`inlet` needs a height) |
| Exit flues | — | three openings into the collection box | each 2½–3½ in wide; height not in a plan | not entered (a hole needs a height) |
| Open stretch of the left wall | "3'" beside it (?) | a gap mid-length | 34–42 in | not entered (question 1 stands) |
| Firebox width, front to back | — | — | can't be read: the plan doesn't draw the firebox apart from the inlet wall | 9 in, assumed |

Questions from step A:

5. Fig 4-149: is the "3'" on the left wall the open stretch, the door? It scales 34–42 in.
6. How tall are the three inlet and three exit flues? They scale 3–4 and 2½–3½ in wide.
