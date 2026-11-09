# Groundhog, Olsen's basic dimensions (`groundhog-basic`)

_Design file: `examples/olsen/groundhog-basic.yaml`. Rebuild with `uv run kilndesigner build
examples/olsen/groundhog-basic.yaml --out out/groundhog-basic`._

## The kiln

The groundhog of the American South as a type: a wood-fired cross-draft half-cylinder, with a
full-width firebox at one end and a full-width chimney at the other. Every size is the middle of
Olsen's range.

Sources: Olsen, *The Kiln Book*, 4th ed., p.111 (Fig 4-85, "Basic groundhog dimensions") and
p.112 (text). Notes in `docs/research/olsen-kilns.md`.

## What's modelled

Chamber 8½ ft wide and a 12 ft ware platform. The arch springs from the floor and rises 38½ in.
There is a 6 ft shallow firebox across the full width, 13½ in below the platform. The chimney is
7½ ft tall; its section is left to the engine (see the table). Walls are 9 in of K-26. Cone 10.

## Book against model

| Feature | Book (Fig 4-85 / p.112) | Model | |
|---|---|---|---|
| Chamber | 29–48 in high, 7–10 ft wide, 12–24 ft long | 38½ in, 8½ ft, 12 ft platform + 6 ft firebox | matches (the middle of each range) |
| Arch | a cylinder cut lengthwise, springing from the floor | sprung arch, springline at 0 in | matches |
| Firebox | shallow, 5–10 ft wide, about 4–6 ft long; or dug-out, 42–48 in deep | 102 in wide, 6 ft | matches the shallow type; the dug-out variant isn't modelled |
| Step up to the platform | "12–15" RISE FROM SHALLOW FIREBOX" | `step: 13.5 in` (drawing) | matches (**new**) |
| Exit flues | six drawn at the foot of the chimney wall, not sized | one, sized by the engine | not expressible (one flue only) |
| Chimney | 5–10 ft (text), 5–12 ft (drawing); 9–30 in deep inside, full width | 7½ ft; section by the engine | differs: a 102 in wide section makes the engine's flue port taller than the back wall under an arch springing from the floor, which it refuses |
| Door / loading | from the front, through the firebox (shallow type) | bricked door, front | matches |
| Spy holes | not shown | engine default | none in the book |
| Damper | not shown | engine's shelf damper note | n/a |

## Build results

**The build fails, both before and after this pass.** It stops in `drawings.py:_arch_cut` with
`AssertionError: arches are only cut across and along`. The design file at HEAD fails the same
way, so the cause is in the engine, not in the new fields. The likely trigger is an arch that
springs from the floor (`chamber.height: 0 in`). The engine needs fixing; no results are
available until then.

## Open questions

1. Fig 4-85 p.111: is the shallow firebox's faint length label "4–6'" or "6'"?
2. Fig 4-85: are the six exit flues all one size? A flue size, or their total area, would let
   the flue be checked.

The build now runs (the arch-cut failure above was fixed in the engine since).

## Scaled off the figures (step A, 2026-11-09)

Fig 4-85 (p.111) prints only ranges. The flues are scaled from the 29–48" crown at its middle,
38½ in; the range itself puts ±25 % on the scale. Readings in `scratch/scale-a/measure.py`.

| Feature | printed | drawing | scaled | In the model |
|---|---|---|---|---|
| Exit flues | — | six at the foot of the chimney wall | each 5–8½ in wide, 6–10 in high | `draft.exits`: 6 in the back, 7 × 7½ in (three courses high), spread evenly (new) |
| Chimney section | 9–30" deep, full width | — | — | engine |

Question from step A:

3. The six exit flues scale about 7 × 7½ in. Is there a usual size for a groundhog's flues?
