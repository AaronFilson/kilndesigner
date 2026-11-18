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

From its own pages, rescanned on 2026-11-18. The owner: "It has two chambers, they are not the
same, and they are described". The heights are scaled against a brick's 9 in face, as the owner
asked (`docs/planning/11-17-26-inputs.md` §8a; `docs/research/olsen-figure-scaling.md` §7, §8).
The width and crown once borrowed from the unbuilt two-chamber design (Fig 8-17) are gone.
- **Width:** 53 in in both chambers, on the bricks of the wall between them (Fig 4-113,
  48–57½ in). Fig 4-108's "55"" falls in that range. The plan isn't drawn to one scale (59–63½ in
  at its shelves, 72½–76½ in at its lengths).
- **Lengths:** Fig 4-108's 8 ft spans the 36 in firebox, the 55 in first platform and the 13 in
  wall (104 in), and its 12 ft the 145 in behind. So the front chamber is entered 55 in deep, with
  the firebox laid in front, and the back chamber 145 in.
- **Front chamber:** springline 42½ in, where the castable meets the wall between the chambers
  (Fig 4-113, 41–44½ in). The dome rises 12 in (2¾ in/ft, p.51) to 54½ in. The photos put the
  crown about 36–51 in over the stoke hole's sill (Figs 4-109, 4-112).
- **Back chamber:** lower. Its springline is 35 in (Fig 4-114, 34–36 in, if that photo shows its
  face of the wall), under the same rise. Its floor is 5–11 in higher there. It falls and tapers
  into the chimney (Figs 4-110, 4-111); neither the fall nor the taper is expressible in a row yet.
- **Walls:** 18 in of medium-duty firebrick, in the plan's drawn 14–19 in (the owner). The printed
  13 in wall between the chambers is kept.
- **Fireboxes:**
  - **The front:** 53 × 36 in, open into the chamber through its whole mouth. Its grate is as the
    plan draws it, 33 × 18 in, bars ¾ in apart. In the door's bricking:
    - the 13½ × 9 in stoke hole (Fig 4-109), covered after each stoking;
    - the 15 × 18 in air inlet (the owner), low in the door, under the grate (Fig 4-112);
    - air holes at grate level, unsized.
  - **The second:** a trough at the back chamber's front, 15 × 53 in, with the 9 × 13½ in stoke
    hole in its side door. Its air comes through the 5 in clay tube under its grate (p.116); the
    door's air holes aren't sized.
- **Flues between the chambers:** three, 12 × 11 in (Figs 4-110, 4-113, 4-114).

Cone 11.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Front firebox | 36 in, dug-out ash pit as the walkway (Fig 4-110, p.117) | 53 × 36 in, grate 33 × 18 in as drawn, on the ground, open into the chamber | matches; the plan draws it curving in to a 44–53 in mouth (not entered) |
| Door's openings | one large 15 × 18 in "inlet flue", one 9 × 13½ in stoke hole, air holes at grate level (p.117) | the 15 × 18 in as the firebox's air below the grate (the owner: an air inlet); the stoke hole 13½ across × 9 in (Fig 4-109), not an intake | matches; the grate-level air holes aren't sized |
| Second firebox | 15 in grate between the chambers, side door (Fig 4-110 "DOOR", about 36 in long, scaled) with a 9 × 13½ in stoke hole (p.117, the owner, 2026-11-17) | 15 × 53 in, the engine's trough at the back chamber's front, its stoke hole 9 × 13½ in, not an intake | matches |
| Between the chambers | a 13 in wall; three large exit flues across the second grate (p.116), about 12 in wide and 10–12 in tall (Figs 4-110, 4-113, 4-114) | the 13 in wall as printed; three 12 × 11 in flues | matches; their sills are 15½–18 in up, the engine cuts them at the floor |
| Secondary air | a 5 in clay tube with a shutter, under the second grate (p.116) | the second firebox's air, 5 in round, below its grate | matches (its shape isn't printed) |
| Steps | 12, 18 and 6 in (Fig 4-110) | the engine's chamber step | differs |
| Domes | two cast K-26 domes (p.116) | dome, 6 in Kaolite 2600-LI | matches (thickness assumed) |
| Chimney | inside 15 × 24 in (Fig 4-110); height not printed | sized by the engine | not expressible: `chimney.inside` needs a height |
| Spy holes | round holes in the domes' sides (Fig 4-108 sketch) | engine default | differs: not sized |
| Damper | not shown | the engine's note | n/a |

## Build results

The build finishes with no errors (2026-11-18, rescanned). Chamber 277 ft³; top temperature
2361 °F (cone 11); heat loss 168.8 kW before the rescan, 103.2 kW now; priced materials $5,630.
The 18 in walls take more of the loss than the old 9 in did. On the borrowed 55 in width it was
335 ft³ and 159.3 kW.

v1 still draws the front firebox with a roof of its own, the walls' layers laid flat. In the kiln
it sits open under the front dome, which v1 can't draw yet.

v2 statics (2026-11-10; rerun 2026-11-18 on the interim 61 in): each chamber's cast dome, sliced
into arches across the width (Heyman's slicing), stood cold and hot on its buttressed walls. The
most any strip needed of the buttress was 182.0 lbf/ft hot (143.6 on the borrowed 55 in). Not yet
rerun on the rescanned 53 in, 42½ and 35 in springlines and 18 in walls. Tests come second for now
(the owner, 2026-11-18).

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
