# Breda bottle kiln (Olsen): the book against the model

_Built 2026-11-08 from `examples/olsen/breda-bottle.yaml`. Rebuild with
`uv run kilndesigner build examples/olsen/breda-bottle.yaml --out out/breda-bottle`._

## The kiln

A round updraft kiln at Segra Pottery, Breda, near Barcelona, built in 1979 for lead-glazed
earthenware. It has a domed chamber with a bottle-shaped chimney cone over it, and a wood firebox
with a grate and ash pit under a domed floor. A firing takes about 10 hours.

## Sources

Olsen, *The Kiln Book*, 4th ed.:
- p.166: text.
- p.167: Fig 6-49 (photo), Fig 6-50 (exploded drawing), Fig 6-51 (firebox, ash pit and inlet
  flues).
- p.168: Fig 6-52 (photo), Fig 6-53 (dome flues and chimney cone), and the firing text.

Notes: `docs/research/olsen-kilns.md`, `breda-bottle`.

## What's modelled

- Chamber: round, 15 ft across, 7 ft to the springline. The dome rises 45 in (assumed) and is 9 in
  thick.
- Walls: 24 in of medium-duty firebrick.
- Firebox: under the floor, 24 in wide, with the grate 96 in long, bars 1 in apart. It is 36 in
  from the grate to the floor and the ash pit is 42 in deep.
- Chimney: the bottle, 25 ft tall and 12 ft across.

## Feature by feature

| Feature | Book | Model | Status |
|---|---|---|---|
| Chamber | 15' dia × 7' (Fig 6-50) | same | matches |
| Wall | "2' thick", metal banding | 24 in, band checked at the springing | matches |
| Dome | "DOME CEILING" with chimney holes; its rise isn't printed | 45 in rise, 9 in | assumed |
| Floor | "KILN DOMED FLOOR" | flat, 13½ in | differs (the floor can't be domed) |
| Firebox | 3' grate to floor dome; ash pit 2' wide × 3½' deep (Figs 6-50, 6-51) | same | matches |
| Grate | metal, on a 1' ledge, bars 1" apart, run 8', "37 total" | 24 in wide, 8 ft, 1 in gap | partly: 37 bars 1 in apart don't fit 2 ft (flagged) |
| Inlet flues | 4½" × 4½", lines 27" and 18" from the wall, perimeter flues 27" apart, count not printed (Fig 6-51) | none: the floor over the firebox is left solid | expressible now in part (`inlets_at: spread`, one row down the firebox's middle); not given, as their count isn't printed (question 1), and the perimeter flues aren't over the firebox |
| Bag wall | 2' high, inside the perimeter inlets, openings 9" apart | none | not expressible |
| Exit flues | 8 in the centre of the dome, 21 round the edge, 4½ × 5", with damper blocks (Fig 6-53) | one square roof flue | not expressible (one flue) |
| Dampers | damper blocks on the perimeter flues | none | not expressible |
| Chimney | bottle 25' high, 12' at its base, 9" walls, cone holes 7" × 15" 15" apart, a door in the cone | 25 ft, 144 in diameter, no top size | partly: the cone, its holes and door aren't expressible |
| Door | a tall door in the chamber wall (Figs 6-49, 6-50), not sized | the engine's default door | differs (not sized) |
| Spy holes | none drawn; stoking is judged by the flames at the cone holes (p.168) | the engine's three | differs |

## Results from the build

- Chamber 1,600 ft³ (printed by the engine as 1.6e+03); 1760 °F (assumed); heat loss 170 kW.
- Warning W1: a 24 in round wall isn't a whole number of 9 in and 4½ in rings, so its bricks are
  missing from the count and the price ($0 priced). This warning was there before; the engine
  suggests 22½ or 27 in.
- The dome pushes 357 lb per foot of wall top, a ring tension of 2,785 lb. A ¼ × 2 in flat band
  holds it.
- Rule 5 isn't applied to an updraft, so the engine works out no chimney height.

## Open questions for the user

1. Fig 6-51 p.167: how many 4½ in inlet flues are there, and where are they? The figure shows
   lines 27 in and 18 in in from the wall and perimeter flues 27 in apart. What do the two "2"" marks
   mean?
2. Fig 6-51: "37 total grate bars" 1 in apart need more than 6 ft of width, but the ash pit is 2 ft
   wide. Is the grate wider than the pit?
3. Fig 6-50: how wide and how tall is the chamber door?
4. Wall thickness: should it be 22½ or 27 in, so the brick count works?
