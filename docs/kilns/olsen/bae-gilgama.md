# Mr Bae's gilgama

_Design file: `examples/olsen/bae-gilgama.yaml`. Built 2026-11-08 with
`uv run kilndesigner build examples/olsen/bae-gilgama.yaml --out out/bae-gilgama`._

## The kiln

Mr Bae, a third-generation Onggi potter, built this Korean climbing tube kiln of the Silla Dynasty
type for an NCECA conference. It is bricked up in a teardrop form that butts into the back wall.
Slab wood 3–5 ft long burns on the floor of a combustion area that has no grate. The kiln is fired
to temperature and then sealed with dirt so the ware comes out black.

## Sources

- Olsen, *The Kiln Book*, 4th ed., p.107 (text, Figs 4-67 to 4-69) and p.108 (text, Figs 4-70 to
  4-74 photos).
- Notes: `docs/research/olsen-kilns.md` (`bae-gilgama`).

## What changed on 2026-11-08

I re-read Fig 4-67 on the page image. The "4'" arrow runs across the chamber floor and the "6'"
arrow runs from the front of the floor to the back wall; the research notes record the same
reading, checked 2026-10-31. Before, the model used an assumed 5¼ ft width and 12 ft depth (16 ft
less 4 ft). It is now 4 ft wide and 6 ft deep, with a half-circle arch that springs at 30 in and
crowns at 4½ ft. The 18 in floor step (p.108) is now entered as the combustion area's step.

## Book vs model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber floor | "4'" across, "6'" deep (Fig 4-67) | 4 × 6 ft box | matches the marks; the plan shape differs |
| Plan | teardrop/oval, butting into the back wall (p.107) | rectangle | not expressible: `outline: teardrop` has the point at the back, not a flat back wall on an oval |
| Overall length | "16'" along the base (Fig 4-67) | 4 + 6 = 10 ft inside | differs: see question 1 |
| Height | "4½'" to the tallest point (faint) | crown 4½ ft | matches |
| Slope | "20% slope" (p.108); "20° SLOPE" (drawing) | 11.3° (20 %) | text followed; the drawing conflicts |
| Combustion area | "4'", "NO GRATES" | firebox 4 × 4 ft, no grate | matches |
| Floor step | 18 in (p.108) | `step: 18 in` | matches |
| Firebox door | arched, bricked up and dirt-sealed (p.108, Fig 4-69) | engine stoke hole and door | differs: no size printed |
| Exit flues | two, 4½ × 9 in, in the back wall (p.108) | one, 4½ × 9 in | not expressible (one flue only) |
| Chimney | two stacks, 8 ft to the ground line (Fig 4-67) | one, 8 ft | partly: one stack; its section is engine-sized |
| Damper | "DAMPER ON TOP" (Fig 4-67) | none | not expressible |
| Spy holes | not drawn | three in the door (engine default) | added by the engine |

## Results from the build

- Chamber volume 97.7 ft³ (was larger under the 5¼ × 12 ft assumption); top temperature 2345 °F
  (cone 10).
- Heat loss at top: 18.53 kW. Priced materials: $2,845.
- No errors or warnings.

## Open questions

1. Fig 4-67 p.107: the chamber reads 4 ft wide and 6 ft deep and the combustion area 4 ft, but the
   base is marked "16'". What makes up the other 6 ft: walls, the chimneys, or a longer chamber
   than the 6' arrow shows?
2. Fig 4-67 p.107 vs p.108: is the slope 20 % (11.3°) or 20° (36 %)?
3. Fig 4-67 p.107: is the "18"" at the front the floor step (p.108) or the mouth's height?
4. Fig 4-67 p.107: are the two dashed stacks two separate chimneys, each with its own damper, or
   one chimney split into two flues?
5. How big is the arched firebox door in Fig 4-69?
