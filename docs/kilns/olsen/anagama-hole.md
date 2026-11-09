# Anagama dug into a clay hill

_Design file: `examples/olsen/anagama-hole.yaml`. Built 2026-11-08 with
`uv run kilndesigner build examples/olsen/anagama-hole.yaml --out out/anagama-hole`. Every number
below has its working and source in the report._

## The kiln

This is the original anagama: a cavity dug into a clay bank, then widened and tapered back into a
chimney flue that comes out at the surface. The firebox, floor and walls were shaped in the clay,
and a fire kept up for weeks bisqued the walls into one piece. It is a type of kiln, not a
particular built one. It is wood-fired, with a cross-draft through one sloping chamber.

## Sources

- Olsen, *The Kiln Book*, 4th ed., p.83 (text) and p.84 (text, Figs 4-3, 4-4A, 4-4B photos, and
  the Fig 4-5 drawing).
- Notes: `docs/research/olsen-kilns.md` (`anagama-hole`).

## What is modelled

A box 63 × 126 in (5¼ × 10½ ft) under a half-circle arch. The arch springs at 10½ in and crowns at
3½ ft. The box sits on the ground on a 25° slope, and the hill buttresses it. The walls are 9 in of
fired clay, entered as Norton's porous fireclay brick. A 2 × 2 × 2 ft firebox sits at the front,
and its mouth is the 2 × 2 ft entrance. It fires to cone 10. The engine places the door, chimney,
exit flue and spy holes.

## Book vs model

| Feature | Book (Fig 4-5, p.84) | Model | |
|---|---|---|---|
| Chamber | 5¼ ft wide, 3½ ft tall, 9–12 ft long | 5¼ × 10½ ft, crown 3½ ft | matches (length the middle) |
| Slope | "SLOPE ANGLE 25" | 25° | matches |
| Section | a rounded teardrop, dashed | half-circle arch | differs (no teardrop section) |
| Entrance and firebox | "2' × 2'" | firebox 2 × 2 ft, 2 ft tall, 2 × 2 ft stoke hole | matches (one reading for all three) |
| Walls | "ground clay bisque", the hill around them | 9 in of fired clay, losing heat to air | differs (the earth isn't modelled) |
| Chimney | a vertical flue up the back to the hill's surface, not sized | engine-sized chimney | differs: no size printed |
| Taper into the chimney | drawn | not modelled | not expressible |
| Door, spy holes, damper, exit flues | not drawn | engine defaults (three spy holes in the door) | added by the engine |

## Results from the build

- Chamber volume 162 ft³; top temperature 2345 °F (cone 10).
- Heat loss at top: 105.1 kW. That is high because the walls are counted as losing heat through
  9 in of fired clay to the air, not into the hill.
- Priced materials: $2,180.
- No errors or warnings.

## Open questions

1. Fig 4-5 p.84: the chamber's height prints as "3½'" but the fraction is faint. Is it 3½?
2. Fig 4-5 p.84: is the "2' × 2'" entrance the size of the firebox, its mouth, or both? The model
   uses it for both.
3. Fig 4-5 p.84: the chimney flue at the back has a width arrow but no number. Is a size given
   anywhere?
