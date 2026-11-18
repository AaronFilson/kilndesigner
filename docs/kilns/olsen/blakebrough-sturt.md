# Les Blakebrough's chamber kiln, Sturt Pottery

_Design file: `examples/olsen/blakebrough-sturt.yaml`. Built 2026-11-08 with
`uv run kilndesigner build examples/olsen/blakebrough-sturt.yaml --out out/blakebrough-sturt`._

## The kiln

The first chamber of Les Blakebrough's wood-fired chamber kiln at Sturt Pottery, Mittagong,
Australia. It has its own firebox: a low channel 9 in wide, stoked through a hole in the side,
with grate bars wedged along the wall and floor on 9 in centres. An oil-drip system with six drip
channels also fires the kiln.

## Sources

- Olsen, *The Kiln Book*, 4th ed., p.205 (text, Fig 8-15 drawing) and p.208 (text, Fig 8-21).
- Notes: `docs/research/olsen-kilns.md` (`blakebrough-sturt`).

## What changed on 2026-11-08

I re-read Fig 8-15 on the page image. The 45" arrow runs across the arched front and the 6' along
the top from front to back. So the chamber is now 45 in wide and 6 ft deep; before, it was 6 ft
wide and 45 in deep. The chamber is 6 ft to the crown.

- The arch is drawn pointed, with its curve running nearly to the floor. It is now a catenary
  6 ft tall over the 45 in span (uncertain).
- The firebox is now a channel along the side wall (the right wall, from the drawing; uncertain):
  9 in wide, 6 ft long, 12 in tall.
- The firebox now has six 9 × 4½ in inlet flues. The count is read off the drawing and uncertain.
- One spy hole is added; the drawing shows a round hole high in the front.

## Book vs model

| Feature | Book (Fig 8-15, p.205) | Model | |
|---|---|---|---|
| Chamber | 6' tall, 45" wide, 6' deep | 45 in × 6 ft, 6 ft to crown | matches |
| Arch | pointed, springing near the floor | catenary | matches the shape (?) |
| Firebox | 12" tall, 9" wide, 6' deep, along the side | right side, 9 in × 6 ft, 12 in tall | matches (side assumed) |
| Grate | bars or soaps on 9 in centres, wedged on wall and floor | 9 in × 6 ft grate, spacing not entered | partly |
| Inlet flues | 9" × 4½", about six drawn | six, 9 × 4½ in | matches (count read off the drawing) |
| Stoke hole | "STOKE HOLE SIDE" | engine default size, in the firebox's mouth | partly: size not printed |
| Spy hole | one round hole high in the front, left of the crown | one, placed in the door by the engine | partly: position not entered |
| Door | the arched front | bricked front door, engine size | matches |
| Other chambers, oil drip (p.208) | not drawn / six drip channels | not modelled | not expressible (one fuel) |
| Exit flue, chimney | not given | engine-sized | engine default |

## Results from the build

- Chamber volume 101 ft³; top temperature 2345 °F (cone 10, assumed).
- Heat loss at top: 19.42 kW. Priced materials: $4,420.
- **W1 warning:** each foot of the catenary pushes out about 20 lb per foot of kiln, and no source
  sizes what holds it. This is new with the catenary arch. `WARNED` in
  `core/tests/test_olsen_kilns.py` needs `frame.catenary` for `blakebrough-sturt`.

## Open questions

1. Fig 8-15 p.205: is the firebox channel along a side wall (running the 6 ft depth), or across
   the front? The text says "the entire width of the 6ft chamber".
2. Fig 8-15 p.205: which side is the firebox on, and how many inlet flues are there? About six
   slots show.
3. Fig 8-15 p.205: is the arch a catenary springing from the floor, or a sprung arch on walls?
   If a sprung arch, where is the springline?
4. Fig 8-15 p.205: the left-hand labels are cut off in the scan ("…FLUES 4½", "…GRATE BARS").
   Are there flues on the left side too?
5. Fig 8-15 p.205: how high up the front is the spy hole, and how big is it?

## Checked against the book (2026-11-18)

Read again on the page image of p.205: the text at zoom 3.2–7 and Fig 8-15 at zoom 4. Nothing in
the design changes. The measurements and readings are in the dataset.

**What p.205 says** (the gutter clips the bracketed words):

> The firebox channel runs the entire width of the 6ft chamber. Grate bars or long soaps are
> wedged along the kiln wall [and] floor, on 9in. (23cm) centers. The grate holds the wood above
> the air [suppl]y at the inlet flues. As the wood burns, the ashes drop to the bottom [of the]
> channel. ... a long iron poker with a hooked end must be [inser]ted through the stoke hole to
> rake down the coals; otherwise, they can [block] the stoke hole and retard the firing. In
> stoking the chamber, a few [pieces] always drop inside the door. Then the long stoking –
> working back [to the] door – is done.

**What Fig 8-15 draws:**
- an arch 6 ft tall over a 45 in span, running 6 ft back;
- the channel, "FIREBOX: 12" tall, 9" wide, 6' deep", at the bottom along the right side, its
  slots, the "INLET FLUES 9" × 4½"", on its outer face;
- "STOKE HOLE SIDE" on the right wall's inner face above the channel;
- a 12 × 19 in kiln shelf;
- a round hole near the crown;
- "…FLUES 4½"" and "…GRATE BARS" cut off at the left;
- no outlet flues and no chimney.

**Gaps, for the plan** (02-plan.md, item 1):
1. **The inlet flues' role.** By p.205 the inlet flues bring the channel's air under the wood.
   The design takes them as the channel's flues into the chamber. Its air then comes through an
   ash-pit mouth the book doesn't show.
2. **The channel's height.** Fig 8-15 draws the printed 12 in as the whole channel. The design
   takes 12 in above the grate, and the engine adds a 12 in ash pit under it.
3. **The outlet flues.** The book shows none, so where the gas leaves isn't measured. The
   design's back wall is its own choice. (The engine takes no flue through a catenary's legs.
   That is a limit of the engine, not of the kiln.)

## Scaled off the figures (step A, 2026-11-09)

Fig 8-15 (p.205) is a perspective sketch. Its printed arrows don't reach what they name: the 6'
arrow is drawn at 4.0 px/in, the 45" at 4.7, and the chamber's inside from floor to crown at 6.3.
That 55 % spread is too wide to enter. Readings in `scratch/scale-a/measure.py`.

| Feature | printed | drawing | scaled | In the model |
|---|---|---|---|---|
| Spy hole | — | an oval high in the front, left of the crown | 3–5 × 7–11 in, centre 64–99 in up (above the 72 in crown on two of the three scales) | not entered |
| Side stoke hole | "STOKE HOLE SIDE" | a small upright opening in the side | 10–15 in high; its width is foreshortened | not entered |

Question from step A:

6. Fig 8-15: the side stoke hole reads 10–15 in high. How big is it?
