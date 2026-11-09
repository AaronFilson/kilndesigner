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
long and 16½ in wide (scaled), 30 in from the floor down to the pit floor, six 4 × 4 in inlet
flues; 9 in medium-duty firebrick walls and floor (assumed); top temperature 1760 °F (assumed,
Falcone's, p.160).

## Scaling (step A, 2026-11-09)

Fig 6-12 (p.156, PDF 143) prints the 5' diameter on the plan and the 5' setting on the section.
At 300 dpi the plan's circle is 8.25 px/in across and 8.98 px/in up the page (the scan stretches
it), the section 8.28 px/in; the plan's 4" flue is drawn at 10.2 px/in, too large to scale from.
Readings in `scratch/scale-pz/scale.py`.

## Feature by feature

| Feature | Book | Scaled | Model | |
|---|---|---|---|---|
| Chamber | 5' inside diameter (plan); setting 5' (section) | — | 60 in round, 60 in tall | matches |
| Roof | shards and saggar pieces over the setting (Figs 6-12, 6-13) | — | `roof: open` | matches |
| Floor | domed, carried on the inlet flues | — | flat, 9 in | differs |
| Firebox | 4' long; 2' at its entry below ground; 2'6" floor to pit floor | — | under the floor, 48 in long, 30 in tall | matches |
| Firebox width | not given ("2'" at its entry is a depth) | where it passes through the wall (the plan's side entrance): 16–17½ in (±1 in, from the 5' across and up the page) | 16½ in | scaled (was 24 in assumed) |
| Inlet flues | six rectangular, one 4" × 4", top pair 10" apart; a central round flue | the 4" flue is drawn 5 in at the plan's scale (drawn large); not rescaled | six 4 × 4 in; the engine cuts one opening the firebox's width | differs: not expressible as placed |
| Central round flue | size cut off at the page edge | 6½–7½ in across (±½ in) | none | not expressible: an under-floor firebox's inlets can't be placed or sized one by one |
| Side entrance | "1?–15"" beside it, half-legible (plan) | 16–17½ in: it is the firebox's mouth through the wall | the firebox's 16½ in width | scaled; disagrees with a 12–15 in reading (question 2) |
| Pit for coals | "pit line (for coals and embers)" | — | firebox floor | matches in effect |
| Wall thickness | not given | section 9¼–9½ in (from its 5'); plan 10½–14 in (from its 5', ±1½ in round the ring) | 9 in | the section's scale kept; the plan disagrees by more than the spread (question 4) |
| Door | none drawn; loaded from the top (Fig 6-11) | — | no door: `loading.type: top`, set over the walls (2026-11-09) | matches |
| Spy holes | none drawn | — | the engine's three | engine default |
| Chimney | none: updraft through the shards | — | none sized (updraft) | matches |

## Results from the build

98.2 ft³; 1760 °F; 39.7 kW lost at top temperature (the open top's loss is not counted). Wood per
firing isn't worked out (no heating value for wood in `docs/research/`).

## Open questions for the user

1. Fig 6-12 plan: can the note on the round flues' diameter at the right page edge be read in your
   copy ("ALL FLUES … ROUND … DIAMETER")? The central one scales 6½–7½ in across.
2. The firebox's mouth through the wall scales 16–17½ in (now modelled 16½ in). Does the
   half-legible note beside it read 12–15"? If so, which is right?
3. Is the kiln loaded from the top only, or through a door in the wall (Fig 6-11 shows a man
   inside)? The model now has no door (`loading.type: top`), as none is drawn; a door's size
   would put one back.
4. The wall scales 9¼–9½ in on the section but 10½–14 in on the plan. Which is nearer (9 in is
   kept)?
