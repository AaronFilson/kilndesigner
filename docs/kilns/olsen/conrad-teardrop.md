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
| Passive damper | 2½ × 4 at the chimney's foot | none | not expressible |
| Damper slot | in the chimney about 73" up (16 + 24 + 33, faint (?)) | the engine's shelf-slot damper | partly |
| Spy holes | none drawn | the engine's three | differs |
| Walls | double side walls, buttressed with stones and concrete (Figs 4-144, 4-145) | 9 in, buttressed | matches |

## Results from the build

- Chamber 97.4 ft³; heat loss at the top 30.33 kW; priced materials $7,140.
- Door: 33 × 37 in in the right wall, flat head, laid out but not checked (no source gives its
  statics).
- Damper: a shelf in a 12 in slot.

## Open questions for the user

1. Fig 4-140 p.124: how wide is the 9 in high stoke hole? Fig 4-147, p.125, shows the front.
2. Fig 4-140: how wide is the 12 in high exit opening under the 13 in block? The neck's last width
   is unreadable.
3. Fig 4-140: how tall is the chimney? Its top dimension is cut off. Is the damper slot about
   73 in up?
4. Which side is the door on, looking from the firebox to the chimney?
