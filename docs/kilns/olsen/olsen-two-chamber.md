# Olsen's two-chamber wood kiln, side-stoked (`olsen-two-chamber`)

Two chambers in a row, each with its own firebox; the first stoked from the side. Design file:
`examples/olsen/olsen-two-chamber.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.202 (text; Figs 8-8 to 8-10 photos), p.203, p.206 (text;
Fig 8-17 second-chamber firebox).

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| First chamber | 55" wide, 48" tall, 8' long | 55 in × 8 ft, 22.9 in rise to 48 in | matches |
| Second chamber | not printed | as the first | assumed |
| Wall between | 9", flue hole 15 × 20 in | 9 in walls; second firebox inlet 15 × 20 in | matches |
| First firebox | side, 18 in below the floor, 9 in metal grate, 15 in ash pit | 14 × 55 in, grate, 15 in ash pit | depth below floor not expressible |
| Second firebox | 14" wide, 15" ash pit, bars ¾" apart, stoke hole 7 × 7 in | as printed | matches |
| Air tube | 5 in perforated square tube under the grate | — | not expressible |
| Exit flue, chimney, roof | not printed | engine default | — |
| Doors, spy holes | not printed | engine default | — |

No change in this pass.

## Key results

251 ft³; heat loss 37.6 kW; grates 1540 in²; engine chimney 18.2 ft.

## Open questions for the user

1. Is this the Hollyweird tube (pp.116–117)? They share the 8 ft chamber, 55 in, ¾ in bars and
   the 5 in air tube.
</content>

## Scaled off the figures (step A, 2026-11-09)

Method: `docs/planning/11-09-26.md` §A; pixel readings in `scratch/scale-K/measure.py`. Uncertainty is the spread between the printed dimensions scaled from (never finer than the ±3 px reading).

| Part | Printed | Drawing | Scaled | Used |
|---|---|---|---|---|
| First firebox below the floor | 18 in (p.202) | — | — | not entered: needs the firebox's height over its grate (not printed) |
| Second ash pit | 15 in deep | — | 20 in under the grate, 15 in under the second chamber's floor (Fig 8-17, from 14" and 9", ±1 in) | printed 15 kept |
| Second grate | at half the flue hole | — | 5 in above the second chamber's floor | not expressible |
| Floors | — | — | second chamber's floor 9 in above the first's | not expressible |
| Flue hole | 15 × 20 in | — | drawn 28 in high | printed kept |

Questions: (a) the first firebox's height above its grate, so its 18 in drop can be entered; (b) is the 15 in ash pit measured from the grate or from the chamber floor?
