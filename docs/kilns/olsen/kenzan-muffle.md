# Kenzan enamel kiln, kin-gama (`kenzan-muffle`)

A small round wood updraft whose flame rises round a clay muffle. Only the outer kiln is modelled.
Design file: `examples/olsen/kenzan-muffle.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.165 (text; Fig 6-47).

## Changes in this pass

- Roof: engine default (a flat roof) → **open**: Fig 6-47 draws the top as the wall's 4 in ring
  round the muffle (drawing)(?).

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Kiln | "2½" across the top (feet), wall 4" thick | 22 in inside, 4 in walls, straight cylinder | matches; slight taper not expressible |
| Top | drawn open round the muffle | open | matches (?) |
| Firebox | 2 × 2 ft, iron grate opening 15 × 19 in, drawn apart below the kiln | under, 24 in wide and tall, 15 × 19 in grate | matches; its length not printed |
| Muffle | 2½ ft tall, 16–18 in across, two bands of seven holes, lid, 6 in exit flue | — | not expressible |
| Spy holes, door | not drawn | engine default | — |

## Key results

9.24 ft³; heat loss 19.8 kW (walls only: the open top's loss isn't worked out); grate 285 in².

## Open questions for the user

1. Fig 6-47: is the firebox under the kiln, or a box built against its foot?
2. Is the kiln's top open, or covered round the muffle?
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| Kiln height | not printed | — | 43½ in (Fig 6-47, from the 2½' top, ±3 in) | 42½ in (17 courses) |

The firebox is a separate sketch at another scale (its 2' wide and 2' high give 5.6 and 6.2 px/in, the kiln 10.7), so its place under the kiln can't be scaled.
