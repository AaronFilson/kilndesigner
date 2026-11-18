# Hotchkiss six-chamber raw-clay kiln, 1971 (`hotchkiss-raw-clay`)

_Design file: `examples/olsen/hotchkiss-raw-clay.yaml`. Rebuild with `uv run kilndesigner build
examples/olsen/hotchkiss-raw-clay.yaml --out out/hotchkiss`._

## The kiln

A six-chamber climbing kiln, built by Richard Hotchkiss and a workshop group from raw blocks of
Lincoln 60 fireclay and sand that fired in place. The builders worked from chamber 6 downward.

Sources: Olsen, *The Kiln Book*, 4th ed., p.33 and pp.54–57: Figs 2-39 to 2-45 are construction
photos, and Figs 2-46 to 2-49 are on p.57.

## What's modelled

Six chambers, each 5 × 5 ft and 6 ft to the crown, on a 22° slope. Each arch runs along the
draft as a near-semicircle rising 30 in, held by the arch below it. Walls are 10 in of porous
fireclay brick, standing in for the fired raw clay. Each chamber has a 9 in side-stoking channel.
The chimney is 30 ft. Cone 10.

## Book against model

| Feature | Book | Model | |
|---|---|---|---|
| Chambers | six, average 5 × 5 × 6 ft (p.56) | six, 5 × 5 ft, crown at 72 in | matches |
| Arches | spring between the front and back walls, each roped until the arch below buttresses it (p.55–56) | arches along the draft, buttressed | matches |
| Flue holes | in the straight wall, about three drawn (Fig 2-40 photo (?)), not sized | the engine's flue holes | differs (count and size unknown) |
| Door | one side wall (p.56, Fig 2-44) | front wall | differs: not sized |
| Stoke holes, spy holes | in both side walls (p.56) | a stoking channel per chamber; spy holes by default | expressible now (`stoke_holes`, `spy_holes.holes`, by chamber); not given, as their sizes and places aren't printed |
| Main firebox | domed (p.57), not sized | none beyond the channels | not modelled |
| Chimney | firebrick to 12 ft, then 18 ft of pipe (p.56–57) | 30 ft, section sized by the engine | matches the height |
| Damper | not described | the engine's note | n/a |

## Build results

The build finishes with no errors. Chamber 820 ft³; heat loss 381.5 kW, likely overstated
because all the clay is treated as fired; priced materials $10,867. Each floor steps 28.3 in. The
fired raw clay has no service rating, so the report flags it as information.

Since 2026-11-10 the walls between the chambers are 20 in (Olsen's common wall, never narrower than
the two 10 in arches' feet on it, p.46; the engine's default), so each floor steps 32.3 in and the
figures above have grown with the run. In v2's statics every chamber stands cold and hot, each
arch's back foot a springer coursed into the taller wall behind it, as "each arch roped until the
arch below was finished to buttress it" (p.55–56).

## Open questions

1. Fig 2-44 p.56: how wide and how tall is the entrance door? Is there one per chamber? With
   that, the doors can go in the side wall (`opening.each_chamber`).
2. Fig 2-40 p.55: how many flue holes are in each straight wall, and how big are they?
3. p.57: how big is the domed main firebox?

## Checked against the book (2026-11-18)

The blocks' sizes are printed on p.54: 9 × 10 × 18 in, 9 × 10 × 9 in and 9 × 5 × 5 in. Every
figure on pp.54–57 was scaled against them (`docs/research/olsen-figure-scaling.md` §9,
`scratch/hotchkiss-1118/`). The two key readings were spot-checked on the page images. The design
is unchanged; the measurements are in the dataset.

**Measured:**
- **Flue holes (Fig 2-40):** four slots between five 9 in piers, 2¼–5½ in wide and 19–22 in
  tall, their sills at the floor, 300–420 in² in all. The step-A note read about three.
- **Arches (Fig 2-45, the 5th chamber):** a near semicircle, span 49–57 in, rise 24–28 in, ring
  10¾–12½ in at the crown. Springline 49–57 in and crown 73–85 in above the ground outside; the
  floor inside isn't seen.
- **Slope (Fig 2-45):** the crowns fall 15–19 in a chamber, 12–15° (11–16° with the spread).
- **The chamber's width (Fig 2-40):** 55–58 in, the arch form's length.
- **Stoke holes (Figs 2-44, 2-45, 2-49):**
  - the pointed hole is 6¼–7½ in wide and 12½–14½ in tall;
  - the side holes are 5–6 in and 8½–10 × 8–9½ in;
  - the spy holes are 1½–2½ in.
- **The main firebox (Fig 2-48):**
  - its front is commercial firebrick, 60–69 in wide;
  - a steel band at the dome's springing stands 36–47 in up, with a diagonal brace;
  - the dome rises at least 16–23 in on a 48–63 in base;
  - three openings at the top of the front are 6–10 × 9–13 in, read as stoke holes.
  Its lower front, where an ash pit, fire mouth or air inlet would be, is hidden in both photos.
- **Chimney (Fig 2-47):** if the dark upper stack is the 18 ft pipe, it is about 29–30½ in across,
  on a brick stack 34–45 in wide.

**Gaps** (for the plan):
1. The slope: the design's 22° (Olsen's Fig 3-15) against the measured 11–16°.
2. The main firebox: the design's six 9 in channels against the book's one domed firebox. Its air
   path is unmeasured, so v2's draft path stays refused.
3. The flues between chambers: four slots measured. The design has the engine's own.
4. The springline above the chambers' floors is still open.
5. The door's size: Fig 2-43's arch, 34–37 in across, may be the door's.

## Scaled off the figures (step A, 2026-11-09)

Superseded on 2026-11-18 (above). Step A scaled nothing: Fig 2-40 (p.55) shows the straight wall
with flue holes between blocks, but the raw-clay blocks' size was taken as unprinted, so the
courses couldn't stand in for a scale. It is printed, on p.54.
