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
| `conrad-teardrop` | Teardrop plan, cast dome; door head flatter than a semicircle (Fig 4-140, p.124) | Done (step 3): a teardrop plan (`chamber.outline`) under a sphere through it (`roof.crown_at`), crown and thickness estimated from the figures; the door's head still a semicircle |
| `bae-gilgama` | Teardrop tube on a slope (p.107–108) | A sloping box |
| `gulgong-racer`, `hohr-2003` | Cast domes over the chamber (p.118–123) | Dome over a rectangle |
| `fireworks-edmonton`, `kanayama-multi` | Cast dome over two crossing axes (p.178–189) | Two crossing vaults (`roof.crossing`) for Fireworks and Church since 2026-10-31; Kanayama unmodelled |
| `breda-bottle`, `bottle-two-storey`, `sevres` | Round, domed, cone-frustum bottle chimney (p.166–169) | Round chamber; chimney as a straight stack |
| `bowen-mountain` | Crown curving down along the length (Fig 4-153) | One arch along the length (`roof.along`), since 2026-10-31 |
| `tamba` | Tube with doors turned through the vault's springing (Figs 4-11, 4-15) | Door laid out and checked since 2026-10-31; the example has none, its size unreadable |
| corbel-arched kilns (p.49, Fig 2-23; p.134 is Singh's round downdraft, curved-kilns.md) | Corbelled vaults | Not described |

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
   needed). Research 2026-10-31 (`docs/research/blocked-items.md`): dome and circle brick tables
   not found (HarbisonWalker's *Modern Refractory Practice* is borrow-only on the Archive, not
   read); mortar density found (BNZ: 116–131 lb/ft³, 200–400 lb per 1000 brick), so wedge-joint
   mortar can go on the bill by weight; no largest joint for tatami bricks ("keep the joints
   thin", FAO, no number). Fourth round (`blocked-items.md` §18–19): dome bricks now sourced from
   Norton, *Refractories* (1949) pp. 730–732: Table 155 radial dome brick for 9 in domes (inside
   radius 4 to 40 ft) and a ring-by-ring count of straights, No. 1 wedges and No. 1 keys (worked
   example: 10 ft radius, 60°, 1,230 nine-inch equivalents); mortar per 1000 9 in brick from
   HarbisonWalker (2008): 250–300 lb dipped, 350–450 lb trowelled, 55 lb sacks; heat-setting wants
   thin dipped joints, air-setting "somewhat thicker". HW's *Modern Refractory Practice* still unread.
5. **Statics.** For a revolved shell (bottle domes, round domes): membrane theory or a thrust
   network, the hoop tension at the base carried by a band or the wall (the existing sliced-dome
   and band logic generalised). For a vault of changing section: Heyman's thrust-line method at
   each station (as door arches now), with the springing and buttress checks. Cast domes over odd
   outlines: the sliced-arch method along the worst slices. Olsen's built kilns are the check:
   each must pass. Sources (2026-10-31, `blocked-items.md`): the lune method for a dome past
   51.8° is Eddy's (1877) as described by MIT's masonry group, partial until Heyman (1977, 1995)
   is read; still no allowable stress for a hot band (ASME II-D Table 1A identified, not read),
   no allowable bearing for refractory, no bottle-kiln top diameter (a secondary 60 ft hovel
   minimum and ~12 in oven wall only), and nothing on a catenary meeting the next at a step.
   Second round (`blocked-items.md` §9–12): no hot factor for rampant arches; a vault-with-lunette
   no-tension paper (Monaco et al. 2018) to read for door heads in vaults; steel keeps full yield
   to 400 °C per EN 1993-1-2 (Snippet only), no hot wrought-iron data, no band temperature.
   Third round (`masonry-statics.md`): the dome past 51.8° now has sourced lune formulas (Lau
   2006 read in full: base thrust per length, H/W ≈ −0.583α + 1.123 for α ≥ 60°, a statics
   estimate, all minimum thrusts) to replace "the least it can be" in `frame.py`; groin vaults
   have a check method (Heyman's slicing onto the diagonals, lower bound) and one worked TNA
   example to test against (Maia Avelino et al. 2020); Monaco et al. read in full gives no load
   share for a door in a vault, only that the load gathers along the intersection curve (the
   door ring's assumption stays unconfirmed). Still not found: rampant hot factor, a catenary at
   a step, hot corbel limits, refractory bearing allowable (Trinks Vol. I not online).

   Fourth round (`bands-and-bottle-kilns.md`, `blocked-items.md` §20–21): the band check is
   unblocked: EN 1993-1-2 Table 3.1 now Verified (k_y,θ 1.0 to 400 °C, 0.78 at 500, 0.47 at 600),
   Norton's "factor of safety of at least 5" for a dome's tension band, HW's 12,000 psi; historic
   hot tests of wrought iron and steel (Kent 1916) give iron no advantage. Still open: the band's
   measured temperature on a brick kiln, long-term creep, a hovel's top diameter (secondary chamber
   sizes 11–20 ft and one 60 ft × 33 ft 3 in hovel found), and a general hot bearing allowable
   (Norton gives a creep-based method only). Concrete under the kiln: EN 1992-1-2 strength and
   conductivity tables and ACI 349's 150/200 °F limits (as quoted by the NRC).
6. **The form.** Shapes edited in the web form by choices first (teardrop, oval, bottle, crossing
   axes), with point editing later (the "drag to stretch" milestone).

## Order

1. Research pass: Olsen's pages for each kiln in the table above (figures checked on the page
   images, metric values where the imperial is unclear), dome and cone brick layouts, cast-dome
   forming, corbel limits; recorded in `docs/research/curved-kilns.md`.
2. The shape description (layer 1) behind the existing types, with no output change; tests that
   every example builds the same.
3. Calimpong first: teardrop plan, cast dome over it, flattened door head; its numbers against
   the book (inside length 9'9", the door 33 × 37 in). **Done 2026-10-30.** `chamber.outline`
   chooses a teardrop (flat front, arc sides) or an oval filling the chamber's width and depth,
   for one level chamber under a dome or a flat roof, fired with fuel or gas (other cases
   refused with reasons). The dome is the sphere over `roof.crown_at` through the plan's
   farthest point. Areas, volume and heat loss come from the form (Steiner growth with depth);
   the lining is laid out as rings on the plan moved out layer by layer (`outline.offset`), its
   volumes (castables, brick by volume) and solids (build123d: the plan extruded, cut to the
   sphere) from the same outline; the sections draw it. Calimpong's crown (45 ± 2 in, 53 ± 4 in
   back) and dome thickness (5½ ± 1½ in) are estimates scaled from the figures
   (`curved-kilns.md`). Left: the door's flat head with rounded corners (the door statics cover
   a semicircular ring or a steel lintel only), the book's concave neck, the frame's dome slices
   (still over the chamber's rectangle), brick course plans round the curve, and the web form's
   point editing. **Leftovers done 2026-10-31** (but point editing): the neck
   (`necked_teardrop`: sides, reverse curves, a straight neck and a flat back; the crown must see
   the whole plan); the dome's slices over the curved plan, each the symmetric arch on its
   farther springing, their thrust shown for the masonry that holds it, and no steel sized round
   a curve (refused with a reason); courses round the curve (4½ in stretcher rings: mortar wedge
   joints on convex arcs, cut to the angle on the reverse curves, lapped corners); and a flat door
   head with rounded corners, laid out, its statics flagged as unsourced. The new fit is 6 %
   under the printed widths' area (the widest point sits further forward than the book draws).
4. Revolved profiles: bottle kilns and round domes of conical-brick courses.
5. Vaults of changing section: Bowen Mountain, Tamba's doors through the springing. Done
   2026-10-31 (vault.py): Bowen's vault, re-read, is one arch along the 5 ft length springing at
   18 in from both end walls (`roof.along`), laid out, drawn and counted as a row of one, with
   its section at stations and Heyman's statics (ring factor, hot line, the end wall as a
   buttress); a door through a buttressed tube's springing is laid out and checked (the door's
   ring under half the vault's weight; the vault's thrust over the door reported, not sized).
   Open: Tamba's door size (Fig 4-15 unreadable); Bowen's door height (not printed, 27 in
   assumed); a tube whose section itself changes (Tamba's segments stepping up the slope,
   Fig 4-16) waits for printed sizes.
6. Crossing-axis domes (Fireworks, Kanayama) and corbelled vaults, as sources allow. Done as far
   as they allow, 2026-10-31. Corbels (`corbel.py`): laid out over a span (courses stepped in
   until one brick bridges the rest, Rhodes's 6 in), each step against TMS 402's min(h/2, d/3) and
   the whole against half the wall (BIA's Corbels brief, PDF read), refused past Olsen's 24 in,
   flagged past Rhodes's 18 in; its stepped section and course count given. Not yet a roof type
   of the design file: that touches every roof consumer and no built kiln of Olsen's is corbelled.
   Crossing axes: no longer blocked on the sources, since the sizes are the designer's. Fig 7-1
   (p.178) is a concept, not a built kiln: it shows how the fire and ash travel, with no arch
   heights (the user, 2026-10-31). The engine should take the two tubes' spans and heights as
   design inputs, starting about 5 ft for the anagama and 6 ft for the groundhog (the user's
   estimate), over Fig 7-2's 9 ft fire zone. **Built 2026-10-31** (`roof.crossing`, `groin.py`,
   `crossing.py`): two crossing vaults meeting in a groin, laid out, drawn, modelled, counted and
   each vault checked as a sprung arch; the groin's ribs aren't checked (no source; Heyman's
   vault chapter unread). `fireworks-edmonton` and `church-skaelskor` are now crossing vaults
   (10-30-26.md); `kanayama-multi` prints no fire-zone size and stays unmodelled.

## Open questions

- Editing: shapes by choice first, point editing later (the user, 2026-10-30).
- Which of these kilns the first users need: the author plans a castable version of the PNW
  kiln to meet the $5,000 budget, so cast domes come first.
