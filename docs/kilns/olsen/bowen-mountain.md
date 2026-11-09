# Bowen Mountain salt kiln (Olsen): the book against the model

_Built 2026-11-08 from `examples/olsen/bowen-mountain.yaml`. Rebuild with
`uv run kilndesigner build examples/olsen/bowen-mountain.yaml --out out/bowen-mountain`._

## The kiln

Olsen's cross-draft salt kiln at Col Levy's studio, Australia: a revised version of John Chappell's
design. It has a firebox across the front behind a bag wall, a sprung arch along the 5 ft length,
exit flues into a collection box, and a tapered chimney. The book draws it for gas, oil drip or
wood. The model is the gas version.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.126 (text, foundation and brick); p.127 (Fig 4-152 salting
pattern, Fig 4-153 plan, section and firebox details); p.128 (text, Figs 4-154 and 4-155 photos).
Notes: `docs/research/olsen-kilns.md`, `bowen-mountain`.

## What's modelled

A 3 × 5 ft chamber, 18 in to the back springline, 16 in at the front, 36 in to the crown. One arch
along the length in two 4½ in rings of JM 28. The floor is one course of medium-duty firebrick on
two courses of red brick, on a concrete-block platform. There are eight GACO MR750 venturi burners
in the front wall with 2½ in ports. A 24 × 36 in arched door is in the right wall. The chimney is
13½ in square, tapering to 9 in square, 11 ft tall, behind a 9 in collection box.

## Feature by feature

| Feature | Book (Fig 4-153 unless noted) | Model | Status |
|---|---|---|---|
| Chamber | 5' × 3', 36" to crown, 18" at back | same; front springline 16 in (the user's reading) | matches |
| Arch | along the length, braced at the front; 9" as two 4½" rings (photos p.128) | `along`, `ring: 2` | matches |
| Walls | "9" WALLS" | 9 in JM 28 (the brick isn't named) | matches (size) |
| Floor | concrete block, red brick, medium-duty firebrick (p.126) | same, 7½ in | matches |
| Burners | 2 MR 750 per flue, four flues, in an IFB block with two 2½" holes, firing into the firebox 12" below the floor | 8 MR750, 2½ in ports, spread evenly along the front wall at the engine's height | differs: the burners are placed in the chamber wall, not stacked in pairs in each flue below the floor |
| Firebox and bag wall | across the front, 12" below the floor, "BURNER OR STOKE HOLE" | not modelled | not expressible for gas (a gas kiln's burners can't fire into a `Firebox`) |
| Inlet flues | four, 9" × 4½" (gas) | not modelled | not expressible for gas |
| Exit flues | four, "9" X 4½" FLUE", into the collection box | four 4½ × 9 in, spread evenly along the back wall (`draft.exits`; which way the 9 runs (?)) | matches (places not printed) |
| Collection box | 9" | `run_to_chimney: 9 in` | matches |
| Chimney | 13½" sq "past top of arch", tapering to 9" × 9"; 10–12 ft | 13½ → 9 in, 11 ft | matches |
| Damper | "DAMPER" in the chimney | the engine's damper note (a shelf slot) | matches in kind; its height isn't printed |
| Passive air | "PASSIVE AIR" at the chimney's foot | none | expressible (`draft.passive_air`), but its size isn't printed |
| Door | "24" (+-) DOOR", side wall, mid-length | 24 × 36 in, right wall, centred, arched | matches |
| Spy holes | none labelled; a small unlabelled square low in the far wall, mid-length | the engine's three in the door | differs (?) |
| Salt holes | four: door, top, back (p.128) | none | expressible (`openings.salt_ports`), but their size isn't printed |
| Frame | angle steel at the corners, tie bars over the arch (photos) | building frame, rods 18 in over the crown | matches |

## Results from the build

- Chamber 38.3 ft³; top temperature 2345 °F (cone 10).
- Heat loss at the top: 15.21 kW.
- Priced materials: $3,574.
- The end walls on their own can't hold the cold thrust: the resultant falls 13.0 in (front) and
  14.2 in (back) in from the inside face. The design counts on the mortared masonry and the
  platform, which the report says is a judgment, not a check.
- The door arch's ring is 5.1 times the thinnest that would stand.
- The 2½ in ports leave less than Ward's inch of clearance round the MR750 head. Olsen builds
  them this way (p.173).

## Open questions for the user

1. Fig 4-153 p.127, section: the small white square low in the far wall, mid-length, about 10 in
   up. Is it a spy hole? It isn't labelled.
2. Fig 4-153 detail 1: how high are the two 2½ in burner holes in the 9 in block, measured from
   the firebox floor? The block is drawn upright, 9 in tall.
3. Fig 4-153: how high is the damper slot in the chimney, and how big is the passive-air opening
   at its foot?
4. The four exit flues: should the engine take several exit flues? It takes one at the moment.
