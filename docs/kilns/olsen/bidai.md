# Kyoto Bidai climbing kiln, 1962

_Design file: `examples/olsen/bidai.yaml`. Built 2026-11-08 with
`uv run kilndesigner build examples/olsen/bidai.yaml --out out/bidai`._

## The kiln

A small Kyoto-style wood climbing kiln, built in 1962 with its foundation dug into a slope. It has
a firebox, three cross-draft chambers up a 3 to 1 slope, and a chimney. It is 19' 5" long overall.

## Sources

- Olsen, *The Kiln Book*, 4th ed., pp.94–97 (text, Figs 4-36 to 4-43; Fig 4-36 is the side view
  and plan, on p.94) and pp.200–201 (Fig 8-7, the firebox).
- Notes: `docs/research/olsen-kilns.md` (`bidai`).

## What changed on 2026-11-08

- Firebox: `step: 24 in`. On Fig 4-36 the grate slab is 18 in above the ground and chamber 1's
  floor is 42 in, read off the drawing.
- Firebox: `inlets: 6`. Fig 8-7 shows six flues into chamber 1, and the Fig 4-36 plan draws five
  piers between them.
- Firebox: a 9 × 14 in stoke hole, from the 9" mouth on Fig 4-36 and the 14" stoking opening on
  Fig 8-7.
- Chimney: `height: 81 in`. Fig 4-36 stacks 73" + 41" + 9" = 123 in above the front ground line;
  the engine measures from chamber 1's floor, 42 in up. This is derived from the drawing and
  uncertain.
- I tried a firebox height of 22 in (the 40" mark less 18"). The engine refused it because the
  firebox would end below the chamber floor, so the height is left to the engine.

## Book vs model

| Feature | Book (Fig 4-36 unless noted) | Model | |
|---|---|---|---|
| Chambers | three, 73 in wide; 42/46/36 deep; 59/65/59 to crown | `chamber.sizes`: 42/46/36 deep, crowns 59/65/59, each arch a semicircle, springlines 38/42/41 in | matches (springlines derived) |
| Arch | 9 in, its peak set back toward the chimney | 6 in tatami brick + 3 in overcoat, circular | partly: `roof.peak_at` can say it, but how far back isn't printed |
| Slope | 3 to 1 | 18.4° | matches |
| Doors | one per chamber, 20 in, one side | 20 × 38 in, each chamber, right wall, 8 in off each chamber's middle (to fit the 36 in chamber 3) | matches (height assumed) |
| Firebox | semicircular front, 46 in long, 18 in ash-pit section, grate slab 18 in up | box 73 × 46 in, grate 14 × 21 in, 14 in ash pit, step 24 in | partly: no round front |
| Flame-diffusing blocks | three pointed blocks | none | not expressible |
| Inlet flues | six (Fig 8-7) | six, engine size | matches the count; size not printed |
| Stoke hole | mouth 9 in; opening 14 in (Fig 8-7) | 9 × 14 in | matches (drawing) |
| Middle-chamber side stoke hole | aizashiguchi 15 in up | none | expressible now (`stoke_holes`, chamber 2's side wall, 15 in up); not given, as its size isn't printed |
| Spy holes | one round hole high in each arch near its back; chamber 2's 56 in up | three in chamber 1's door (default) | expressible now (`spy_holes.holes`, by chamber, in a wall or through the arch); not given, as their size isn't printed and only chamber 2's height is (question 2) |
| Vapour holes | rows in the arches | none | not expressible |
| Flues between chambers | 6"×12" and 7"×12" piers; 12 in flues over a 15 in wall | engine's six 4½ × 9 in holes per wall | differs |
| Exit | 12 in step and 12 in exit flue at chamber 3's back | engine flue | differs: width not printed |
| Chimney | 9 × 9 flue grid across 73 in; top about 123 in above ground | 81 in from chamber 1's floor, engine section | partly |
| Damper | not drawn | engine's shelf-in-slot note | engine default |

## What changed on 2026-11-09 (B3)

- Each chamber its own size (`chamber.sizes`), from Fig 4-36's depths and crowns. Each arch is
  taken as a semicircle on its depth, the springline the crown less half the depth: chamber 1's
  38 in is the printed springline; 42 and 41 in for chambers 2 and 3 are derived. The doors move
  to 8 in off each chamber's middle so the 20 in door fits the 36 in chamber 3.

## Results from the build

- Chamber volume 297 ft³; top temperature 2345 °F (cone 10, assumed).
- Heat loss at top: 164.4 kW (168.1 kW with one mean size). Priced materials: $1,248. The
  masonry holds each arch's thrust: 161, 168 and 150 lb per foot, hot.
- **W1 warning:** the 6.8 ft chimney is under the 8.8 ft that Olsen's rules give as the least for
  this kiln. This follows from the drawing. `core/tests/test_olsen_kilns.py`'s `WARNED` doesn't
  list it yet, so that test fails until the lead adds `fire.chimney` for `bidai`.

## Open questions

1. Fig 4-36 p.94: do the "41"" and "9"" marks above the "73"" stack up to the chimney's top, about
   123 in above the ground at the front?
2. Fig 4-36 p.94: how far above each chamber's floor are the spy holes in chambers 1 and 3?
   Chamber 2's reads 56 in.
3. Fig 4-36 p.94: how tall is the firebox inside, from the grate slab to the crown of its arch?
4. Fig 8-7 p.201: how big are the six inlet flues into chamber 1?
5. Fig 4-36 p.94: how wide is the 12 in exit flue at chamber 3's back, and how many are there?
6. Fig 4-36 p.94: where along each chamber does its arch's peak stand (for `roof.peak_at`), and
   is each chamber's springline 38 in, or does it follow the semicircles' 38, 42 and 41 in?
