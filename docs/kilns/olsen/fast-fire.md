# Olsen fast-fire wood kiln

Design file: `examples/olsen/fast-fire.yaml`. A small wood downdraft of 4½ in insulating brick
with two fireboxes under the floor in an "S", firing to cone 10 in 3½ hours.

## Sources

Olsen, *The Kiln Book*, 4th ed.: p.139 (text, Fig 5-35 cut-away, Fig 5-36 frame and chimney),
p.140 (text, Figs 5-37 to 5-39 firebox and grate), p.141 (Figs 5-40 to 5-45, door and bag wall
text), p.142–143, p.199, p.204–205 (Figs 8-13, 8-14), p.309 (firing log). Notes:
`docs/research/olsen-kilns.md` (`fast-fire`).

## Feature by feature

| Feature | Book | Model | |
|---|---|---|---|
| Chamber | 27" wide, 36"–40" to the springline (Fig 5-35) | 27 × 27 × 36 in | depth not printed (assumed) |
| Arch | 4½" IFB, featheredge skewbacks, No. 1 arch (Fig 5-35, p.140) | sprung arch, rise 3⅜ in | matches; rise from the 1½ in/ft rule |
| Door | whole front, laid in rowlock (Fig 5-35, p.140) | whole front wall, bricked | matches |
| Spy holes | pull-out cone-hole plugs; a 2½ × 2½ in hole open at top centre (p.141) | three 2¼ × 2½ in in the door (engine default), and a 2½ × 2½ in hole at the door's top centre (`spy_holes.holes`), its top at the arch's inside (derived) | the top hole matches; the plugs' number and places not given |
| Fireboxes | two, 13½ × 40½ in, under the floor "along the front and back wall" (p.204) in an S: side by side with one wall between, the front one open at the right, the back one at the left (Fig 5-37); "LOW DUTY FIREBRICK 90 required" (Fig 5-39) | 2 under, `runs: across`, `mouth: [right, left]`, 13½ × 40½ in, each far end under the far side wall (Fig 5-44); `lining`: 4½ in Alsey Smithfield, certified to low duty (masonry-materials.md §2.2) | matches (2026-11-10; before, they ran front to back side by side across the width, their inlets 114 mm under the side walls) |
| Grate | 12–13 × 24–27 in, ¾ in gaps, 6–7 in up (Fig 5-39, Fig 8-13, p.199) | 12 × 24 in, ¾ in, 6½ in ash pit | matches; the engine lays the grate from the mouth, where p.204 puts it "as far back in the firebox as possible, so that part of it is directly under the inlet flue" |
| Inlet flues | 4½ × 13½ in, one at each firebox's closed end (Fig 5-39, p.141), against the side wall (Fig 5-44) | 4½ in at the far end, against the side wall; on the floor 11¼ in of the 13½ | the two 13½ in channels and the 4½ in wall between them take 31½ in, so on the assumed 27 in depth each channel reaches 2¼ in under the front or back wall (question below) |
| Bag wall | rowlock rows along the inlet flues (Fig 5-44) | — | not expressible |
| Exit flue | 9 × 7½ in at the back at floor level (Fig 5-35, Fig 5-40) | 9 × 7½ in, back | matches |
| Chimney | 9 × 9 in × 14 ft, tied to the back wall (Figs 5-36, 5-37) | 9 × 9 in, 14 ft, run 0 | matches |
| Damper | slide damper drawn in the chimney (Fig 5-36); passive air hole in its back (p.141) | engine's shelf-in-a-slot damper | size not given; air hole not expressible |
| Frame | 2 × 2 × 3/16 in angle, bolted (Fig 5-36) | engine sizes the steel | — |

## Results (build of 2026-11-08)

16.1 ft³; 2345 °F at cone 10; 7.56 kW lost at the top; $6,334 priced items. Warning W1: K-23 IFB
runs at 2345 °F, past its 2300 °F rating (Olsen specifies 2300 °F IFB). Arch: 4 rings of 12 No. 1
arch bricks and 2 straights. Wood use not worked out (no sourced heating value).

## Open questions

- Chamber depth: not printed. Fig 5-37's foundation is 45" × 40½": is the chamber 27" deep, or
  deeper? Its two 13½ in firebox channels and the wall between them take 31½ in, which with the
  front and back walls on the foundation's outer rows is a 31½ in deep chamber (40½ in outside),
  inside the 30 ± 3 in scaled off Fig 5-35; on 27 in each inlet flue opens 11¼ in of its 13½ in.
- p.141: how many cone holes are in the door, and how high?
- Fig 5-36: the damper's size and height above the kiln.

## Scaled off the figures (step A, 2026-11-09)

Fig 5-35 (p.139) is isometric. Along its depth axis it is scaled from the printed 12 × 24 in
shelves, a pair read as 24 in. Readings in `scratch/scale-a/measure.py`.

| Feature | printed | drawing | scaled | In the model |
|---|---|---|---|---|
| Chamber depth | — | — | about 30 in (one scale only; ±3 in for the iso reading) | 27 in, unchanged: within the reading |
| Damper (Fig 5-36) | — | in the chimney, which is drawn with a break | can't be scaled: the 14 ft chimney is broken in the drawing | engine |
| Cone holes in the door | — | photos (Figs 5-40 to 5-45) | can't be scaled: photos | engine default |
