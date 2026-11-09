# Electric car kiln, 45 in wide

Design file: `examples/olsen/electric-car-45.yaml`. The widest electric car kiln Olsen knows,
45 × 106 × 49 in inside.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.244–245 (text only; no figure of this kiln). p.245's top line is
cut by the page curve: "...wide and 49in. (124cm) tall, with elements located in the sides,
[and?] floor." Power by p.256; walls by p.39, p.246, p.248. Notes: `docs/research/olsen-kilns.md`.

## Feature by feature

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 45 × 106 × 49 in (p.244–245) | same | matches |
| Loading | car kiln | car, front | matches |
| Elements | sides and (?) floor | left and right walls | floor elements not expressible |
| Roof | not given | sprung arch, 5⅝ in rise | assumed |
| Power, supply, walls, cone | not given | 51.9 kW, 240 V 3-phase, 175 A; 4½ K-26 + 2½ K-23; cone 10 | assumed (see YAML) |
| Spy holes | not given | engine default | — |

## Results (build of 2026-11-08)

146 ft³ (with the arch); 2345 °F; 27.8 kW lost at the top; 51.9 kW installed (356 W/ft³);
9 × 8 AWG Kanthal A-1 elements, 180 ft each, delta; 6.6 W/in²; $9,189 priced items.

## Open questions

- p.245, first line: is the cut word before "floor" "and"? Does the kiln have floor elements?
