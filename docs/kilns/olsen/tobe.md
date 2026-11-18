# Tobe Village climbing kiln, Shikoku (`tobe`)

Example: [`examples/olsen/tobe.yaml`](../../../examples/olsen/tobe.yaml).
Research notes: `docs/research/olsen-kilns.md`, `tobe`.

The largest chamber kiln Olsen describes: seven wood-fired chambers, 15,000 ft³ in all, destroyed
in July 1963.

## Book pages

Olsen, *The Kiln Book*, 4th ed., p.90 and p.92: text only. There is no figure of this kiln.

## What's modelled

Seven chambers each the size of the largest, 25 ft across, 10 ft along the draft and 10 ft to the
crown (a semicircular arch on 10 ft), climbing at 18.4°; a 9 in himae trough per chamber; 13½ in
walls and arch of high-duty firebrick (the owner, 2026-11-17); cross-draft to an engine-sized
chimney; cone 10 (assumed).

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
W1). (v1, on the 9 in medium-duty lining before 2026-11-17.)

## v2 statics (2026-11-10)

The walls between the chambers are now 18 in (Olsen's common wall, 4½ in thicker than the others
and never narrower than the two 9 in arches' feet on it, p.46; the engine's default), so the run
is 8½ in longer a wall and each floor steps 45.9 in. Along the row each chamber's arch stands cold,
the ends' supports (the firebox, the earth, the chimney) giving 210 lbf/ft. Hot, with dense brick's
25 psi crushing stand-in (ASTM C16's load, sourced since 2026-11-10 from the makers' C16 results,
`docs/research/refractory-bearing.md` §B6) at every joint there is no admissible state; it stands
from 29.7 psi, and with compression unlimited. The stand-in is a lower bound on the brick's hot
strength, so that verdict isn't given: the masonry's temperature through its thickness (the
hottest brick at cone 10, 2345 °F, is cooler than C16's 2460–2640 °F) and the brick's real hot
strength are to decide it (`docs/planning/11-10-26.md` §D2). With 9½ in walls between the
chambers, a 103 in tall wall between 10 ft arches had a mechanism even without sliding.

## Worked back from standing (the owner, 2026-11-17)

The section above is the 9 in medium-duty model as it was. The owner's answer:
- **Brick:** high duty. Tobe was built in Japan in the 1800s or before, perhaps of tatami-rolled
  fireclay brick, and nothing specific is known of it.
- **Thickness:** not 9 in. "The brick could have been much thicker given the size and that it was
  pre-industrial."
- **The rule:** "the reference kiln is truth … work backwards to find the properties". This is
  ADR 0017, decision 17 as amended.

The design takes high-duty brick and 13½ in walls and ring, the next standard thickness. Working
back with v2's row statics (seven chambers hot, μ 0.50):
- **13½ in ring (the design):** stands hot on C16's 25 psi; it needs 19.5 psi (none at 19.50, one
  at 19.53).
- **The thinnest that stands on 25 psi:** about 9¾ in on the design's 13½ in walls (9.74 in has
  no admissible state, 9.77 in has one). The first run, 9.70–9.84 in, was on the old 9½ in walls.
- **9 in ring:** it would need 30.5 psi (none at 30.50, one at 30.53). Had its ring been 9 in,
  its brick carried that hot.

The walls barely move it. The dataset records the two strengths as `inferred` facts. The ring
frontier is a geometry, not a property of the brick, so it goes in the assumed ring's reason
(2026-11-18; `scratch/tobe/worked_back.py`). Cold, the ends' supports
(the firebox, the earth, the chimney) now give 131 lbf/ft, against 210 with the 9 in ring.

Heat with the thicker lining: it still reaches cone 10, and 40 tons is still no less than v2's
max fire. The hot statics still takes all the masonry at C16's temperature. The owner calls that a
model fault ("the temp does not go around all sides of the brick"); the fix is the bridge from the
heat model's wall temperatures (`docs/planning/02-plan.md`).

## Checked against the book (2026-11-18)

Read again on the page images, p.90 and p.92. The dataset matches them:
- seven chambers, 15,000 ft³;
- the largest 25 ft long by 10 ft tall by 10 ft wide, with 40 tons of wood (the whole kiln);
- destroyed in July 1963;
- on Shikoku, its width almost its height, so more oxidizing.

The book's order, long × tall × wide, puts the 25 ft across the kiln and the 10 ft along the
draft, as the design has them.

v2:
- **Cavity:** 2,239–2,246 ft³ a chamber, 15,710 ft³ in all, 4.7 % over the printed total. The
  design's header had said 14,800 ft³, wrongly.
- **Draft path: refused.** The book doesn't mention a main firebox, and the himae's stoke holes are
  covered after each stoking, so chamber 1 has no way in for its air. Future work, with Suzuki's
  and the Kyoto type's.

## Open questions for the user

1. Does "required 40 tons of wood to fire" (p.90) mean the largest chamber or the whole kiln?
   (Answered 2026-11-09: the whole kiln; ADR 0017, decision 15.)
2. How thick were the walls between the chambers, and the arches? (Answered 2026-11-17: not 9 in,
   could have been much thicker; 13½ in taken. High-duty brick.)
