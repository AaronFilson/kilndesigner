# Blakebrough's fibre envelope kiln, Hobart

_Design file: `examples/olsen/blakebrough-tasmania.yaml`. Built 2026-11-08 with
`uv run kilndesigner build examples/olsen/blakebrough-tasmania.yaml --out out/blakebrough-tasmania`._

## The kiln

A 40 cu ft gas downdraft at the Tasmanian School of Art. A fibre box with a suspended flat fibre
roof runs on a track over a fixed brick hearth and seals against the back wall and chimney. Olsen
holds it up as the model true downdraft (p.150).

## Sources

- Olsen, *The Kiln Book*, 4th ed., p.148 (text, Figs 5-70 to 5-73; Fig 5-72 is the hearth
  drawing), p.149 (text, Figs 5-74 to 5-79) and p.150. p.69 describes a folded-fibre kiln at the
  same school, probably this one.
- Notes: `docs/research/olsen-kilns.md` (`blakebrough-tasmania`).

## What changed on 2026-11-08

Only comments. I re-checked the burner channels and ports against Fig 5-72 and they already
matched. The damper and spy-hole gaps are now noted in the file.

## Book vs model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 42 × 54 × about 52 in (p.148) | 42 × 54 × 52 in | matches |
| Roof | suspended flat fibre (p.148) | flat, 8 in Cerachem | matches (thickness assumed) |
| Moving box on a track | box moves; hearth and back wall fixed (p.148) | car loading from the back | differs: the hearth rides on the car instead |
| Bottom 15 in of IFB | p.148, Fig 5-72 "15" OR 5 BRICKS" | fibre | not expressible (no per-height wall layers) |
| Burners | four venturi compound injectors (p.149) | four venturi | matches |
| Burner ports | 4½ × 6 in, back wall and opposing front, firing down 9 in side channels (p.149, Fig 5-72) | 4½ × 6 in at ±16.5 in, back and front, 5½ in up | matches |
| Exit flues | eight floor flues into two 4½ × 6 in channels under the hearth (p.148–149) | one 9 × 6 in flue at the foot of the back wall | not expressible (no floor flues or channels) |
| Chimney flue | 9 × 6 in (p.148) | flue port 9 × 6 in | matches |
| Chimney | 9 × 9 in (Fig 5-72), height not printed | 9 × 9 in, 60 in (assumed) | matches the section |
| Damper | slab on top of the chimney (Fig 5-72) | a slab on the chimney's top (`draft.damper.kind: top`) | modelled |
| Spy hole | one in the box's wall (photo, Fig 5-71) | three engine-placed in the door | differs: size and place not printed |

## Results from the build

- Chamber volume 68.2 ft³; top temperature 2345 °F (cone 10, assumed).
- Heat loss at top: 15.28 kW. Priced materials: $1,452.
- **W1 warning:** the 54 in² flue port is under the smallest of Olsen's three starting sizes
  (68 in²). It is the book's 9 × 6 in chimney flue. The real kiln's eight floor flues feed it, and
  the engine can't model them. This warning was there before.

## Open questions

1. Fig 5-72 p.148: is "15" OR 5 BRICKS" the hearth's height above the concrete block, or the IFB
   at the foot of the chamber walls (text, p.148)?
2. Fig 5-71 p.148: how big is the spy hole in the box's wall, and how high is it?
3. Is the chimney's height given anywhere?
