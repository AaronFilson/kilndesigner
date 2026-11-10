# Conrad Calimpong's teardrop kiln (Olsen): the book against the model

_Built 2026-11-08 from `examples/olsen/conrad-teardrop.yaml`. Rebuild with
`uv run kilndesigner build examples/olsen/conrad-teardrop.yaml --out out/conrad-teardrop`._

## The kiln

A small wood-fired cross-draft kiln with a teardrop plan under a cast dome. It has a grate and ash
pit at the front, a side door, and a 9 × 9 in chimney at the back. Conrad Calimpong (printed
"Colimpong" on p.124) learnt wood firing on Olsen's Hollyweird tube in 1985.

## Sources

Olsen, *The Kiln Book*, 4th ed.:
- p.116: caption.
- p.124: text and Fig 4-140, the plan and side elevation ("ALL DIMENSIONS ARE INTERIOR
  MEASUREMENTS"), plus photos Figs 4-141 and 4-142.
- p.125: photos Figs 4-143 to 4-147.

Notes: `docs/research/olsen-kilns.md`, `conrad-teardrop`; `docs/research/curved-kilns.md`.

## What's modelled

- Plan: a teardrop outline, 117 in long and 51½ in at the widest, with a 39 in front and a 12 in
  neck 19 in long.
- Dome: cast in Kast-O-Lite, its rise (10 in) and thickness (5½ in) estimated by scale. It springs
  at 35 in.
- Walls: 9 in of K-26.
- Door: 33 × 37 in, flat-headed with rounded corners, in the right wall.
- Firebox: at the front, 39 × 24 in, with a 15 × 24 in grate and a 12 in ash pit.
- Chimney: the engine sizes it, and it comes out 9 × 9 in.

No YAML values changed in this pass. Only the notes were added.

## Feature by feature

| Feature | Book (Fig 4-140) | Model | Status |
|---|---|---|---|
| Plan | 39" front, 51½" widest, 48", 16", 12" neck, 19" to the end, 9'9" | fitted teardrop, about 6 % under the printed widths | matches closely |
| Height | 35½" front (?), 35" near the back | 35 in springline | matches |
| Dome | cast, thickened (Fig 4-146); crown and thickness not printed | estimated by scale | estimated |
| Grate | 15" wide, inside the chamber's front, over the ash pit | 15 × 24 in grate in a front firebox | differs: the model's firebox stands outside the front wall; the book's grate is inside the teardrop |
| Ash pit | 12" deep, 24" long | 12 in, 24 in | matches |
| Stoke hole | 9" high, sill 14" above the floor; width not printed | none | differs: the width isn't printed, so no stoke hole is given; with one, `sill` would set its foot |
| Door | 33" × 37", far jamb 48" from the chimney wall | same, right wall (side not printed) | matches |
| Exit flue | 12" high under a 13" block; width not printed | engine-sized flue | differs: the width isn't printed |
| Chimney | "only 9 x 9in." (p.124); height cut off | engine-sized, comes out 9 × 9 in | matches the section |
| Passive damper | 2½ × 4 at the chimney's foot | a 2½ × 4 in hole through the chimney's foot (`draft.passive_air`; which way each runs (?)) | modelled |
| Damper slot | in the chimney about 73" up (16 + 24 + 33, faint (?)) | the engine's shelf slot at 73 in (`draft.damper.up`) | modelled (the slot's size not printed) |
| Spy holes | none drawn | the engine's three | differs |
| Walls | double side walls, buttressed with stones and concrete (Figs 4-144, 4-145) | 9 in, buttressed | matches |

## Results from the build

- Chamber 97.4 ft³; heat loss at the top 30.33 kW; priced materials $7,140.
- Door: 33 × 37 in in the right wall, flat head, laid out but not checked (no source gives its
  statics).
- Damper: a shelf in a 12 in slot.
- v2 statics (2026-11-10): the cast dome over the teardrop, sliced into arches across its width
  (Heyman's slicing), stands cold and hot on its buttressed walls; being flat (10 in rise over
  51½ in), its strips push hard: the most any needs of the buttress is 164.9 lbf/ft hot
  (`docs/planning/11-09-26.md` §H item 10).

## Open questions for the user

1. Fig 4-140 p.124: how wide is the 9 in high stoke hole? Fig 4-147, p.125, shows the front.
2. Fig 4-140: how wide is the 12 in high exit opening under the 13 in block? The neck's last width
   is unreadable.
3. Fig 4-140: how tall is the chimney? Its top dimension is cut off. Is the damper slot about
   73 in up?
4. Which side is the door on, looking from the firebox to the chimney?

## Scaled off the figures (step A, 2026-11-09)

Fig 4-140 (p.124): the plan's neck scaled from its 16", 12", 19" and 12" (7.9–9.4 px/in); the
elevation's chimney foot from its 35", 12", 13", 24", 8" and 19" (6.9–9.6 px/in). Readings in
`scratch/scale-a/measure.py`.

| Feature | printed | drawing | scaled | In the model |
|---|---|---|---|---|
| Exit opening | 12" high, under a 13" block | the neck's end | 9.6–11.4 in across | `draft.flue_port`: 10½ × 12 in (new; it was engine-sized) |
| Passive damper | "2½ X 4" | a small upright rectangle | 3–3¼ in along the kiln, 4–5½ in high | 2½ across, 4 high, as entered: the drawing bears it out |
| Chimney height | top dimension cut off | — | 55–77 in on the left-hand scales, 119 in on the right-hand stack (16 + 24 + 33 = 73 in drawn at 4.45 px/in): a 2× spread | not entered; engine-sized |
| Stoke hole width | 9" high, sill 14" | — | can't be scaled: neither view draws its width | not given |

Questions from step A:

5. Fig 4-140: the exit opening scales 10½ in wide (9.6–11.4). Is it 9 in, the chimney's inside,
   or wider?
6. Fig 4-140: the elevation's right-hand dimensions are drawn at half the scale of the left. Is the
   chimney about 10 ft (the right-hand stack's reading) or about 5½ ft (the left's)?
