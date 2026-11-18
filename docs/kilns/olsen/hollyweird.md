# Olsen's Hollyweird Tube, 1985 (`hollyweird`)

_Design file: `examples/olsen/hollyweird.yaml`. Rebuild with `uv run kilndesigner build
examples/olsen/hollyweird.yaml --out out/hollyweird`._

## The kiln

A two-chamber wood kiln of the anagama type, at Olsen's home pottery: a Bizen-style front chamber
joined to a tube-style second chamber, each under a dome cast in K-26 castable. It has a front
firebox, whose ash pit is the walkway into the kiln, and a second firebox between the chambers,
stoked from the side.

Sources: Olsen, *The Kiln Book*, 4th ed., p.116 (text, Fig 4-108 sketch, Fig 4-110 plan),
p.117 (text and photos), p.124.

## What's modelled

From its own pages (2026-11-18). The owner: "It has two chambers, they are not the same, and they
are described." The width and crown once borrowed from the unbuilt two-chamber design (Fig 8-17)
are gone (`docs/planning/11-17-26-inputs.md` §8a):
- **Width:** both chambers 61 in inside, scaled on Fig 4-110 against the drawn shelves' printed 12 in
  across (59–63½ in). At the printed lengths' scale along the kiln they would be 72½–76½ in; the
  plan isn't drawn to one scale (`docs/research/olsen-figure-scaling.md` §7).
- **Lengths:** Fig 4-108's 8 ft spans the 36 in firebox, the 55 in first platform and the 13 in
  wall (104 in), and its 12 ft the 145 in behind. So the front chamber is entered 55 in deep, with
  the firebox laid in front, and the back chamber 145 in. Before, the front was 8 ft deep with the
  firebox in front of it as well.
- **Heights:** no figure scales one. Olsen's Principle 1 (p.74–75), his own rule on his own kiln:
  the height equal to the width, the dome counted in it, so 61 in to the crown. The domes are 6 in
  of Kaolite 2600-LI, rising 2¾ in per foot of the span (14 in, p.51), so the walls stand 47 in.
  Fig 4-108 draws the front dome taller and rounder than the back, by an amount it doesn't scale.
- **What differs between the chambers:** the front's 36 in firebox and one platform; the back's
  side-stoked 15 in second grate (a trough at its front), its two platforms and 9 in grate, and its
  taper into the chimney.

Walls are 9 in of medium-duty firebrick (the plan draws the side walls 14–19½ in, perhaps the
buttressing). The front firebox is 61 × 36 in with a grate whose bars are ¾ in apart. It has a
15 × 18 in inlet flue and a 9 × 13½ in stoke hole. The second firebox is 15 × 61 in. Cone 11.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Front firebox | 36 in, dug-out ash pit as the walkway (Fig 4-110, p.117) | 61 × 36 in, grate, on the ground | matches; the plan draws it curving in to a 44–53 in mouth (scaled, not entered) |
| Inlet flue, stoke hole | one 15 × 18 in, one 9 × 13½ in, in the door bricking, with air holes at grate level (p.117) | as printed | matches; the air holes aren't modelled |
| Second firebox | 15 in grate between the chambers, side door (Fig 4-110 "DOOR", about 36 in long, scaled) with a 9 × 13½ in stoke hole (p.117, the owner, 2026-11-17) | 15 × 61 in, the engine's trough at the back chamber's front, its stoke hole 9 × 13½ in | the engine takes the stoke hole as a fully open intake, against the owner's rule that stoke holes are covered after stoking (to fix, the plan's item 1) |
| Between the chambers | a 13 in wall; three large exit flues across the second grate (p.116), about 12–14 in wide (scaled, Figs 4-110, 4-114) | the 13 in wall as printed (`lining.between`, 2026-11-10; it was 9 in) with 5 flue holes, 4½ × 9 in (the engine's Kyoto rule) | the wall matches; the flue count and size can't be set without the flues' height |
| Secondary air | a 5 in clay tube with a shutter, under the second grate (p.116) | none | not expressible |
| Steps | 12, 18 and 6 in (Fig 4-110) | the engine's chamber step | differs |
| Domes | two cast K-26 domes (p.116) | dome, 6 in Kaolite 2600-LI | matches (thickness assumed) |
| Chimney | inside 15 × 24 in (Fig 4-110); height not printed | sized by the engine | not expressible: `chimney.inside` needs a height |
| Spy holes | round holes in the domes' sides (Fig 4-108 sketch) | engine default | differs: not sized |
| Damper | not shown | the engine's note | n/a |

## Build results

The build finishes with no errors (2026-11-18, on its own figures). Chamber 399 ft³; top
temperature 2361 °F (cone 11); heat loss 168.8 kW; priced materials $8,093. (On the borrowed
55 in width it was 335 ft³ and 159.3 kW.)

v2 statics (2026-11-10; rerun on its own figures 2026-11-18): each chamber's cast dome, sliced
into arches across the 61 in width (Heyman's slicing), stands cold and hot on its buttressed
walls; the most any strip needs of the buttress is 182.0 lbf/ft hot (143.6 on the 55 in borrowed
before; `docs/planning/11-09-26.md` §H item 10).

## Open questions

1. How tall is the chimney? With its height, the printed 15 × 24 in section can go in.
2. Fig 4-110 p.116: how big are the three exit flues from the front chamber? (Their width scales
   about 12–14 in, 2026-11-18; their height isn't drawn.)
3. Fig 4-108: how far above the floor are the round spy holes in the domes, and how big are they?
4. ~~Was Hollyweird built to the two-chamber design?~~ No (the owner, 2026-11-18): its two chambers
   differ and are described on its own pages.

## Scaled off the figures (step A, 2026-11-09)

Fig 4-110 (p.116, plan) scaled from the 55" chamber width and the printed 12 × 24 in shelves
(7.1–7.8 px/in); the flues counted with a pixel profile down the 13" wall
(`scratch/scale-a/profile.py`). Fig 4-108 is a perspective sketch: its domes' spy holes have no
printed dimension in their plane, so they aren't scaled. Readings in `scratch/scale-a/measure.py`.

| Feature | printed | drawing | scaled | In the model |
|---|---|---|---|---|
| Flues between the chambers | "Three large exit flues" (p.116); the wall "13"" | three gaps between two piers | 11–13 in wide each (the piers 10½–11½ in), on the 55 in width; rescaled 2026-11-18 to about 12–14 in (piers about 10–11), and about 12 in on Fig 4-114's brick (`olsen-figure-scaling.md` §7.3) | not entered: their height isn't drawn, and `draft.between` needs it |
| Spy holes in the domes | — | round, in the domes' sides (Fig 4-108) | can't be scaled: a perspective sketch | engine default |
| Chimney | 15 × 24 in inside; height not printed | — | not drawn in elevation | engine |

Question from step A:

4. The three flues between the chambers scale about 12 in wide. How tall are they?
