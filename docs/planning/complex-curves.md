# Plan: complex curves, cast and conical-brick kilns

Started 30 October 2026 at the user's request: support Calimpong's teardrop and the other kilns
that are cast, or built of conical (tapered) bricks, whose shapes the engine can't yet describe.

## Why

The engine describes a chamber as a box or a cylinder, under a sprung arch, a catenary, a dome
over a rectangle or circle, or a flat roof, and a run of chambers along a line or an arc. Olsen's
built kilns include shapes outside that set, so today they are simplified, and every
simplification is written into the example's notes:

| Kiln (`examples/olsen/`) | Shape as built | How the engine has it now |
|---|---|---|
| `conrad-teardrop` | Teardrop plan, cast dome; door head flatter than a semicircle (Fig 4-140, p.124) | A box under a sail dome; the door's head as a semicircle |
| `bae-gilgama` | Teardrop tube on a slope (p.107–108) | A sloping box |
| `gulgong-racer`, `hohr-2003` | Cast domes over the chamber (p.118–123) | Dome over a rectangle |
| `fireworks-edmonton`, `kanayama-multi` | Cast dome over two crossing axes (p.178–189) | Not described |
| `breda-bottle`, `bottle-two-storey`, `sevres` | Round, domed, cone-frustum bottle chimney (p.166–169) | Round chamber; chimney as a straight stack |
| `bowen-mountain` | Crown curving down along the length (Fig 4-153) | Arch across the width |
| `tamba` | Tube with doors turned through the vault's springing (Figs 4-11, 4-15) | Door refused |
| corbel-arched kilns (p.134) | Corbelled vaults | Not described |

## What "complex curves" needs, in layers

1. **Describing the shape.** A chamber as a cross-section swept along a path, and a plan outline,
   instead of named types only:
   - plan outlines from arcs and lines (a teardrop is two tangent arcs and a point; an oval, four
     arcs), and a revolved profile for round kilns, bottles and cones;
   - a vault's section that may change along its length (Bowen Mountain, Tamba's taper), as
     sections at stations, lofted between them;
   - a dome over any convex outline (Calimpong, crossing-axis kilns), as a surface through the
     wall's top edge with a rise, or given as contour sections;
   - door heads of other shapes: segmental, three-centred, flat with rounded corners (Calimpong).
   The design file gets these as data (points, arcs, stations), validated, with the existing named
   types kept as shorthands that produce the same geometry, so every current example builds the
   same.
2. **Geometry and drawings.** build123d already builds lofts, sweeps and revolves; the model, the
   plans' sections and the plan view come from the same description. Areas and volumes for heat
   loss come from the solid (area at depth for the layered wall, as now).
3. **Building it: casting.** A cast shell is the simplest route for any shape: volume of each layer
   from the solid, batches and dry-out as for castables now (single-layer schedule only, as
   sourced). Forms: the inside surface as a form to build (sand or lath former), its area and
   outline in the plans. Sources needed: forming practice for cast domes (Olsen p.118–125, the
   Gulgong racer and Höhr kilns; castable makers' installation guides).
4. **Building it: conical and tapered bricks.** A course of a dome or a cone is a ring whose
   radius changes course by course: each course a ring turned by the methods already in
   `rings.py` (cut to the angle, featheredges, tapered shapes), its bricks also tilted to the
   dome's slope (each joint on a radius of the dome). Sources needed: dome-brick layouts (Olsen's
   dome kilns, HarbisonWalker's dome and circle-brick tables, beehive-kiln practice), the
   conical-brick shapes makers sell, and how far a course may lean before it needs a form.
   Corbelled vaults: each course stepped in, with the limit on overhang per course (source
   needed).
5. **Statics.** For a revolved shell (bottle domes, round domes): membrane theory or a thrust
   network, the hoop tension at the base carried by a band or the wall (the existing sliced-dome
   and band logic generalised). For a vault of changing section: Heyman's thrust-line method at
   each station (as door arches now), with the springing and buttress checks. Cast domes over odd
   outlines: the sliced-arch method along the worst slices. Olsen's built kilns are the check:
   each must pass.
6. **The form.** Shapes edited in the web form by choices first (teardrop, oval, bottle, crossing
   axes), with point editing later (the "drag to stretch" milestone).

## Order

1. Research pass: Olsen's pages for each kiln in the table above (figures checked on the page
   images, metric values where the imperial is unclear), dome and cone brick layouts, cast-dome
   forming, corbel limits; recorded in `docs/research/curved-kilns.md`.
2. The shape description (layer 1) behind the existing types, with no output change; tests that
   every example builds the same.
3. Calimpong first: teardrop plan, cast dome over it, flattened door head; its numbers against
   the book (inside length 9'9", the door 33 × 37 in).
4. Revolved profiles: bottle kilns and round domes of conical-brick courses.
5. Vaults of changing section: Bowen Mountain, Tamba's doors through the springing.
6. Crossing-axis domes (Fireworks, Kanayama) and corbelled vaults, as sources allow.

## Open questions

- Editing: shapes by choice first, point editing later (the user, 2026-10-30).
- Which of these kilns the first users need: the author plans a castable version of the PNW
  kiln to meet the $5,000 budget, so cast domes come first.
