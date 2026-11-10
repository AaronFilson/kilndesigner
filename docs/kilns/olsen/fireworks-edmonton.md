# Fireworks kiln, Edmonton, 1998 (`fireworks-edmonton`)

_Design file: `examples/olsen/fireworks-edmonton.yaml`. Rebuild with `uv run kilndesigner build
examples/olsen/fireworks-edmonton.yaml --out out/fireworks`._

## The kiln

Olsen's first multi-directional wood kiln, built by 40 workshop participants. An anagama-style
tube and a groundhog cross at right angles over one fire zone. Each firebox faces its own chimney
and also serves as a door.

Sources: Olsen, *The Kiln Book*, 4th ed., p.178 (Figs 7-1 and 7-2), p.179 (text and the firebox
design, Fig 7-3), p.181 (text and Figs 7-5 to 7-7), p.183 (text).

## What's modelled

A 9 × 9 ft fire zone under two crossing vaults. The anagama vault's crown is at 60 in and the
groundhog's at 72 in (the user's heights). Both spring at 36 in. The vaults are 6 in of
Kast-O-Lite 26 LI Plus and the walls 9 in of K-26. There are two fireboxes, one at the front for
the anagama and one at the left for the groundhog. Each has a 14 in grate with bars ¾ in apart,
an 18 in ash pit, and, new in this pass, a 13½ in step up to the ware floor. One flue wall and
one chimney are at the back.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Fire zone | about 9 ft both ways (p.183); diagonal 9 ft (Fig 7-2) | 9 × 9 ft | matches the text |
| Vaults | two crossing tubes meeting in a groin (Fig 7-1) | `roof.crossing` | matches |
| Fireboxes | one per axis, each also a door (p.179) | front and left | matches |
| Grate, ash pit | grate 3–4 ft; ash pit 14 in wide and 18 in deep (Fig 7-3) | 42 in grate, 14 in wide, 18 in pit | matches |
| Step to the ware platform | 12–15 in (Fig 7-3) | 13½ in (drawing) | matches (**new**) |
| Chimneys | a single anagama chimney and a three-flue groundhog chimney, equal height, slightly tapered (p.179, Fig 7-7) | one chimney at the back, sized by the engine | not expressible (one draft path and one chimney) |
| Dampers | a passive air and shelf damper on each chimney flue (p.179) | the engine's shelf-damper note | not expressible |
| Spy holes | a round hole in the dome's side (Fig 7-6, sketch) | engine default | differs: not sized or placed in the book |
| Plan | walls curving in between the arms (Fig 7-2) | two straight tubes | differs |

## Build results

The build finishes with no errors. Chamber 431 ft³; top temperature 2345 °F (cone 10); heat loss
66.94 kW; priced materials $18,287. The damper note gives a 16.5 in shelf slot.

v2 statics (2026-11-10): the groin solid cut both ways into slices, coupled where they cross
(`docs/planning/11-09-26.md` §H item 11), stands cold and hot on its buttressed walls; the least
peak push on the walls is 255.9 lbf/ft cold, 299.2 hot. It stands down to a 2.21 in shell cold,
so the 6 in cast is 2.7 times the thinnest.

## Open questions

1. Fig 7-2 p.178: which wall holds the groundhog's three-flue chimney? It is drawn opposite the
   groundhog firebox. Should the model put that firebox at the right, so that the front-to-back
   path is the anagama's?
2. Fig 7-7 p.181: how tall are the two chimneys, and what are their sections?
3. p.183 gives 3½–4½ ft to the ceiling's vertex. Your starting heights were 5 and 6 ft. Which
   should stand?
4. Fig 7-7: how thick is the cover of stones or shards on the roof? v2's statics would carry it
   as a layer over the shell; it is left out now (`docs/planning/11-09-26.md`, "For the user
   later", v2 question 9).

## Scaled off the figures (step A, 2026-11-09)

Nothing scaled. Figs 7-5 and 7-6 (p.181) are sketches with no printed dimension, Fig 7-7 is a
photo, and Fig 7-2 (p.178) prints only the fire zone's diagonal. The chimneys, their flues, the
dampers and the spy hole can't be scaled.
