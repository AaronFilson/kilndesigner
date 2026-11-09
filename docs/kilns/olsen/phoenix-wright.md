# George Wright's Phoenix kiln, Portland (`phoenix-wright`)

Example: [`examples/olsen/phoenix-wright.yaml`](../../../examples/olsen/phoenix-wright.yaml).
Research notes: `docs/research/olsen-kilns.md`, `phoenix-wright`.

The first Phoenix kiln, built in the 1970s by George Wright, a brick and tile kiln fireman: "a
small 8 to 10 cubic foot wood-fired kiln with a Roman arched firebox under the kiln [floor] with a
cross-draft chamber above".

## Book pages

Olsen, *The Kiln Book*, 4th ed., p.147: text only (the "10", lost in the scan's gutter, read by the
user, 2026-10-29). There is no figure of this kiln; Fig 5-67 is its 40 ft³ variation
(`phoenix-nh`).

## What's modelled

A 9 ft³ cube (25.3 in) with a No. 1 arch, built as Olsen's fast-fire kiln: one 4½ in K-26 wall; a
super-duty floor over one fast-fire firebox under it (13½ × 36 in, a 12 × 24 in grate, 6½ in
below and 6 in above it); an inlet flue 13½ × 4½ in; cross-draft to a 9 × 4½ in chimney 9½ ft
tall sharing the back wall. Only the volume and the layout are the book's.

## Feature by feature

| Feature | Book (p.147) | Model | |
|---|---|---|---|
| Volume | 8 to 10 ft³ | 9 ft³ | matches |
| Firebox | Roman-arched, under the floor | under the floor, `roof: roman`; its 6¾ in rise doesn't fit the 6 in assumed above the grate, so the engine draws it flat and says so | given; refused on the assumed height |
| Draft | cross-draft chamber above | cross | matches |
| Inlet flue, exit flue, chimney | not described | by `phoenix-nh`'s layout and Olsen's rules | assumed |
| Door, spy holes, damper | not described | engine defaults | engine default |

## Results from the build

9 ft³; 2345 °F (cone 10, assumed); 6.5 kW lost at top temperature.

## Open questions for the user

1. Any source on Wright's own kiln beyond p.147 (the *Studio Potter* article on the New Hampshire
   kiln may describe it)?
