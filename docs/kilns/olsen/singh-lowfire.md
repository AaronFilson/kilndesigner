# Singh's low-fire glaze kiln, New Delhi (`singh-lowfire`)

Example: [`examples/olsen/singh-lowfire.yaml`](../../../examples/olsen/singh-lowfire.yaml).
Research notes: `docs/research/olsen-kilns.md`, `singh-lowfire`.

A round wood updraft, "a Muslim design dating from antiquity", built by Mansimran Singh's father
for Delhi Blue tiles and saggared low-fire pottery. No built roof: shards and saggar pieces are
piled over the setting each firing.

## Book pages

Olsen, *The Kiln Book*, 4th ed.:

- p.155: text (the firing: about five hours warming the firebox, then six to seven).
- p.156: Fig 6-11 (stacking, photo), Fig 6-12 (section and plan), Fig 6-13 (shards over the
  setting, photo).

## What's modelled

A round chamber 5 ft across, set 5 ft high, open-topped; one wood firebox under the floor, 4 ft
long, 30 in from the floor down to the pit floor, six 4 × 4 in inlet flues; 9 in medium-duty
firebrick walls and floor (assumed); top temperature 1760 °F (assumed, Falcone's, p.160).

## Feature by feature

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 5' inside diameter (plan); setting 5' (section) | 60 in round, 60 in tall | matches |
| Roof | shards and saggar pieces over the setting (Figs 6-12, 6-13) | `roof: open` | matches |
| Floor | domed, carried on the inlet flues | flat, 9 in | differs |
| Firebox | 4' long; 2' at its entry below ground; 2'6" floor to pit floor | under the floor, 48 in long, 30 in tall | matches |
| Firebox width | not given ("2'" at its entry is a depth) | 24 in (assumed) | assumed |
| Inlet flues | six rectangular, one 4" × 4", top pair 10" apart; a central round flue | six 4 × 4 in; the engine cuts one opening the firebox's width | differs: not expressible as placed |
| Central round flue | size cut off at the page edge | none | not expressible |
| Side entrance | 12–15" from the firebox (plan) | none | not expressible |
| Pit for coals | "pit line (for coals and embers)" | firebox floor | matches in effect |
| Wall thickness | not given; by scale about 9–10 in (drawing, ?) | 9 in | assumed |
| Door | none drawn; loaded from the top (Fig 6-11) | the engine's front wall door | differs (engine default) |
| Spy holes | none drawn | the engine's three | engine default |
| Chimney | none: updraft through the shards | none sized (updraft) | matches |

## Results from the build

98.2 ft³; 1760 °F; 39.7 kW lost at top temperature (the open top's loss is not counted). Wood per
firing isn't worked out (no heating value for wood in `docs/research/`).

## Open questions for the user

1. Fig 6-12 plan: can the note on the round flues' diameter at the right page edge be read in your
   copy ("ALL FLUES … ROUND … DIAMETER")?
2. Is the firebox's width readable (the plan's 12–15" side entrance, or another figure)?
3. Is the kiln loaded from the top only, or through a door in the wall (Fig 6-11 shows a man
   inside)? If there's no door, the engine's default door should be noted as not being the book's.
