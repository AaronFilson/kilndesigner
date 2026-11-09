# Church kiln, Skælskør (Olsen): the book against the model

_Built 2026-11-08 from `examples/olsen/church-skaelskor.yaml`. Rebuild with
`uv run kilndesigner build examples/olsen/church-skaelskor.yaml --out out/church-skaelskor`._

## The kiln

Olsen's second multi-directional wood kiln, built in 1998 at a workshop for Nina Hole at
Guldagergaard. Two cross-draft systems cross at right angles over one fire zone: an anagama-style
system with a 36 in firebox facing a single chimney, and a groundhog system with a 24 in firebox
facing a three-flue chimney.

## Sources

Olsen, *The Kiln Book*, 4th ed.:
- p.178: Fig 7-1, concept.
- p.179: Fig 7-3, firebox.
- p.180: text.
- p.182: text, Fig 7-8 (photo), Fig 7-9 (drawing), Fig 7-10 (sketch).
- p.183: text, fire zone.

Notes: `docs/research/olsen-kilns.md`, `church-skaelskor`.

## What's modelled

- Fire zone: 7 × 7 ft, walls 29 in to the springline.
- Vaults: two crossing vaults of 6 in Kast-O-Lite. The anagama vault rises to 60 in and the
  groundhog vault to 63 in (the user's heights).
- Walls: 9 in of K-26.
- Fireboxes: the anagama firebox (36 in) at the front and the groundhog firebox (24 in) on the
  left. Each has a 14 in grate, bars ¾ in apart, and an 18 in ash pit. **New:** each grate sits
  13½ in below the ware floor.
- Flue: one exit flue, in the back wall.

## Feature by feature

| Feature | Book | Model | Status |
|---|---|---|---|
| Fire zone | 7 ft (p.183), "DIAGONAL – 7'" (Fig 7-2) | 7 × 7 ft square crossing | differs: Fig 7-2's curved walls between the arms aren't modelled |
| Walls | "WALL 9" THICK", "9 BRICKS TALL 28–30"" (Fig 7-9) | 9 in, 29 in | matches |
| Roof | Viking-longboat roof (Fig 7-10); crossing tubes (Fig 7-1) | two crossing vaults | partly; heights are the user's |
| Anagama firebox | 36" wide, faces the single chimney (p.182); grate, ash pit (Fig 7-9) | front, 36 in, grate and ash pit | matches |
| Groundhog firebox | 24" wide, faces the groundhog chimney (p.182) | left, 24 in | matches the size; the side is (?) |
| Step up to ware | "STEP UP TO WARE PLATFORM 12–15"" (Fig 7-3) | 13½ in | matches (middle of the range) |
| Walk-in channels | below ground, "18" STEP DOWN" (Fig 7-9) | floor on the ground | not expressible |
| Anagama chimney | single, 13.5 × 13.5" (Fig 7-9); height not printed | the engine sizes it: 13½ × 13½ in | matches the section |
| Groundhog chimney | three flues, at the groundhog's back wall (Fig 7-9) | none | not expressible (one draft path, one flue wall) |
| Door | none drawn in Fig 7-9 | front wall bricked (the engine's) | differs: the door can't be both the front firebox wall and the real door |
| Spy holes | none drawn | the engine's three in the door | differs |

## Results from the build

- Chamber 236 ft³; 2345 °F; heat loss 44.79 kW; priced materials $14,453 (no price for K-26).
- The groin where the two vaults meet isn't checked (no source covers it). Each vault is checked as
  a barrel.
- Firebox 1: 36 in above the grate, 18 in ash pit (33 % below), grate 13½ in below the floor.
  Firebox 2: 24 in above, 18 in below (43 %).
- The engine puts the door on the front wall, which is the anagama firebox's wall.

## Open questions for the user

1. Fig 7-9 p.182: looking from the anagama firebox toward its chimney, is the groundhog firebox on
   the left or the right?
2. Fig 7-9: what does the "18" STEP DOWN" measure? Is it from the ware floor down into the walk-in
   channel, or down to the grate?
3. Where is the loading door? Fig 7-9 draws none, and Fig 7-8 is a photo of the church. Is it in
   one of the walls between the arms?
4. How tall are the two chimneys, and how big is each of the groundhog chimney's three flues?

## Scaled off the figures (step A, 2026-11-09)

Nothing scaled. Fig 7-9 (p.182) is a perspective sketch; its only dimension near the chimneys is
the single chimney's 13.5 × 13.5 in, on a different face from the three-flue chimney, so the
three flues can't be scaled with a spread. The chimneys' heights aren't drawn. Fig 7-10 is a
sketch with no dimension, Fig 7-8 a photo.
