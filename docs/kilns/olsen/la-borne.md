# La Borne tunnel kiln (`la-borne`)

Long wood-fired tunnel kilns on a slope, fired from the firebox at the low end; ware in and gases
out through the back. Design file: `examples/olsen/la-borne.yaml`.

## Sources

Olsen, *The Kiln Book*, 4th ed.: pp.109–111 (text; Fig 4-78 plan and section; Fig 4-79 exit-flue
brick construction; Figs 4-80 to 4-84 photos).

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Size | 1766–2825 cu ft; 10 ft at the bag wall, 12 ft widest, 27 ft long; skewback "7'?" | 11 × 27 ft, 7 ft springline, 33 in rise | mean width; 2650 ft³ |
| Slope | about 1:9 | 6.34° | matches |
| Firebox | 4 ft long, the width at the bag wall | 10 × 4 ft | matches |
| Grate | bonded arch with nine 5×5×5×7 in holes a row, or ring arches 4½ in apart | — | not expressible |
| Bag wall | greenware checkerboard, 2 ft space behind the grate | — | not expressible |
| Exit flue | the bricked-up back entrance, laid as a lattice, with a "draw hole or spy hole" at the top (Fig 4-79) | engine flue 85½ × 7½ in at the back | lattice not expressible |
| Spy holes | one draw/spy hole drawn high in the back wall (Fig 4-79) | engine default, three in the back | not set: height not printed |
| Chimneys | two, each side of the back door, since the "rebirth" | two, spread along the back wall, engine-sized (`draft.chimneys: 2`) | matches the count; no sizes printed |

2026-11-09 (B3): `chamber.widths` can now say the plan's 10 ft at the bag wall and 12 ft at the
widest, but where along the 27 ft the widest stands isn't printed, so the mean-width box stays.

## Key results

2650 ft³; heat loss 136 kW; engine chimney 12.9 ft.

## Open questions for the user

1. Fig 4-78: how far from the bag wall is the plan at its widest, 12 ft (for `chamber.widths`)?
</content>
