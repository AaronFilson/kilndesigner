# Tobe Village climbing kiln, Shikoku (`tobe`)

Example: [`examples/olsen/tobe.yaml`](../../../examples/olsen/tobe.yaml).
Research notes: `docs/research/olsen-kilns.md`, `tobe`.

The largest chamber kiln Olsen describes: seven wood-fired chambers, 15,000 ft³ in all, destroyed
in July 1963.

## Book pages

Olsen, *The Kiln Book*, 4th ed., p.90 and p.92: text only. There is no figure of this kiln.

## What's modelled

Seven chambers each the size of the largest, 25 ft across, 10 ft along the draft and 10 ft to the
crown (a semicircular arch on 10 ft), climbing at 18.4°; a 9 in himae trough per chamber; 9½ in
walls and a 9 in arch of medium-duty firebrick; cross-draft to an engine-sized chimney; cone 10
(assumed).

## Scaling (step A, 2026-11-09)

Nothing to scale: there is no figure of this kiln.

## Feature by feature

| Feature | Book | Scaled | Model | |
|---|---|---|---|---|
| Chambers | seven (p.90) | — | seven | matches |
| Total volume | 15,000 ft³ (p.90) | — | about 15,600 ft³ | close |
| Largest chamber | 25 × 10 × 10 ft (p.90) | — | every chamber that size | assumed for the others |
| Width ≈ height | p.92 | — | 10 ft along, 10 ft tall | matches |
| Firebox, flues, chimney, doors, spy holes, damper | not given | — | himae; engine defaults | assumed / engine default |

No figure exists to compare burners, ports, flues, doors or chimney against.

## Results from the build

About 15,600 ft³; 2345 °F; 2,549 kW lost at top temperature (every chamber hot at once). The roof's
outside Rayleigh number, 1.9 × 10¹¹, is past the convection correlation's checked range (warning
W1).

## v2 statics (2026-11-10)

The walls between the chambers are now 18 in (Olsen's common wall, 4½ in thicker than the others
and never narrower than the two 9 in arches' feet on it, p.46; the engine's default), so the run
is 8½ in longer a wall and each floor steps 45.9 in. Along the row each chamber's arch stands cold,
the ends' supports (the firebox, the earth, the chimney) giving 210 lbf/ft; hot, with dense brick's
25 psi crushing stand-in carried over from IFB by analogy its 10 ft arches have no admissible state,
without it one, so that verdict isn't given (`docs/planning/11-09-26.md` §H item 9). With 9½ in
walls between the chambers, a 103 in tall wall between 10 ft arches had a mechanism even without
sliding.

## Open questions for the user

1. Does "required 40 tons of wood to fire" (p.90) mean the largest chamber or the whole kiln?
2. How thick were the walls between the chambers, and the arches? (Assumed: 18 in by Olsen's
   p.46, and 9 in as Bidai's.)
