# Falcone Pompeii updraft

Design file: `examples/olsen/falcone-pompeii.yaml`. A wood-fired updraft at Fornace Falcone,
near Montecorvino Rovella, Italy, firing replica tiles and bricks for Pompeii: a ware chamber on
ring arches over a firebox chamber of the same plan, under a barrel vault with nine exit flues.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.160 (text, Figs 6-28 to 6-30, photos), p.161 (text, Figs 6-31A
to 6-35, photos). No measured drawing. Notes: `docs/research/olsen-kilns.md`.

## Feature by feature

| Feature | Book | Model | |
|---|---|---|---|
| Ware chamber | 118 × 157 × 79 in (p.160) | same, 79 in to the springline | matches |
| Vault | barrel vault (Fig 6-32) | sprung arch, 22.6 in rise, 9 in, buttressed | rise and thickness assumed |
| Exit flues | nine square holes in the vault, three across at back, middle, front (p.161, Fig 6-32) | one flue sized by the engine | not expressible (no count/places for up-draft flues) |
| Firebox chamber | same plan, 71 in tall; ring arches 9 in apart carry the floor (p.160, Figs 6-31A/B) | one firebox under, 118 × 157 × 71 in | ring arches not expressible |
| Stoking port | arched mouth with under-air (Fig 6-34) | — | size not printed; a stoke hole on an under-floor firebox not given |
| Grates | none; long slat wood (Fig 6-35) | no grate | matches |
| Walls | modern firebrick inside, tile façade | 36 in medium-duty firebrick | thickness assumed; façade not modelled |
| Door, spy holes | not described (Fig 6-30 shows the setting through an opening) | whole-front bricked door, three spy holes (default) | not given |

## Results (build of 2026-11-08)

About 1,010 ft³ with the vault (848 ft³ as the printed box); 1760 °F; 121 kW lost at the top;
$0 priced (no price for the firebrick).

## Open questions

- Fig 6-32: how big are the nine exit-flue holes?
- Fig 6-34: the stoking port's width and height, and how many there are.
- Where is the ware chamber's door (Fig 6-29 side view)?
