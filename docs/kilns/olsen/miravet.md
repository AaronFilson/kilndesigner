# Miravet medieval kiln (`miravet`)

A medieval wood updraft of three equal cubes: a domed chamber, a sub-chamber under it holding the
inlet flues, and a firebox in front. Design file: `examples/olsen/miravet.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: pp.157–160 (text; Fig 6-19 diagram with inset section, p.158;
Figs 6-20 to 6-23 photos).

## Changes in this pass

- Firebox inside height **78 in**, the "6'6"" inside the 8 ft firebox cube (Fig 6-19) (drawing)(?).
- Comments: the door is an arched doorway on the firebox side by a "TARGET POT"; the firebox
  mouth's "3'" sill.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 8 × 8 ft, 6 ft to the dome's start, 9 ft to the crown | 96 × 96 × 72 in, 36 in dome | matches |
| Walls, floor | 3–4 ft, partly buried; floor 13–15 in | 36 in; 13½ in | matches |
| Floor flues | 35, 6 × 6 in | 35 firebox inlets 6 × 6 in | matches (through the sub-chamber: not expressible) |
| Dome flues | 15 in main flue; four 5 in corner flues | 15 in round flue | corner flues not expressible |
| Firebox | an 8 ft cube, no grate; mouth 27 × 18 in, 3' up | 96 × 96 in, height 78 in, stoke hole 18 × 27 in, `sill: 36 in` | matches |
| Sub-chamber | a cube under the chamber, holding pots | — | not expressible |
| Door | arched, on the firebox side, unsized | whole front wall | position matches; size not printed |
| Spy holes | a target pot by the door | engine default | — |

## Key results

521 ft³; heat loss 85.2 kW; inlet area 1260 in².

## Open questions for the user

1. Fig 6-19: is "6'6"" the firebox's inside height, and is "3'" the mouth's sill above the
   firebox floor?
2. The chamber door's width and height.
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| Door | arched, on the firebox side, unsized | — | 33 in wide (from the 8' along that wall, ±2½ in), 51 in to its crown (from 6' and 9', ±9 in) | `loading.opening` 31½ × 50 in, arched |
| Corner flues | four, 5 in | at the corners | drawn 12 in (perspective of the tube) | `draft.exits`, 5 in round, centres 2½ in in from both walls |
| Mouth sill | "3'" | — | the 3' arrow runs from the firebox's foot to the mouth's sill (34½ ±2½ in) | `sill: 36 in` confirmed |

The chamber's 6' and 9' disagree by 40 % on the drawing, hence the door height's spread. Question: is the doorway about 2¾ ft wide and 4 ft high?
