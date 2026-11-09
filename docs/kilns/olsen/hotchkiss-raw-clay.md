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
| Stoke holes, spy holes | in both side walls (p.56) | a stoking channel per chamber; spy holes by default | not expressible (no side stoke holes); spy holes not placed |
| Main firebox | domed (p.57), not sized | none beyond the channels | not modelled |
| Chimney | firebrick to 12 ft, then 18 ft of pipe (p.56–57) | 30 ft, section sized by the engine | matches the height |
| Damper | not described | the engine's note | n/a |

## Build results

The build finishes with no errors. Chamber 820 ft³; heat loss 381.5 kW, likely overstated
because all the clay is treated as fired; priced materials $10,867. Each floor steps 28.3 in. The
fired raw clay has no service rating, so the report flags it as information.

## Open questions

1. Fig 2-44 p.56: how wide and how tall is the entrance door? Is there one per chamber? With
   that, the doors can go in the side wall (`opening.each_chamber`).
2. Fig 2-40 p.55: how many flue holes are in each straight wall, and how big are they?
3. p.57: how big is the domed main firebox?
