# Curved, cast and conical-brick kilns: shape data and building practice

Research pass for `docs/planning/complex-curves.md` (step 1 of its Order), 30 October 2026.
Part A reads the shapes of Olsen's kilns off the figures; Part B collects outside sources on
dome and cone brickwork, cast-dome forming and corbel limits.

Olsen, *The Kiln Book*, 4th ed.: cited by **printed page and figure number**. The other facts
for these kilns (fireboxes, flues, chimneys, firing) are in `olsen-kilns.md`, and general dome
and castable practice in `kiln-reference.md` §1 and §4; they aren't repeated here.

Status words:

- **Checked on the page image**: read again from a rendered page image during this pass.
- **Unreadable**: on the page but too faint or cut off to read; left out.
- **Not given**: not printed anywhere on the pages read.
- **(?)**: an uncertain reading. **derived**: arithmetic on printed numbers.
- Web sources: **sourced** (quote read on the page), **partial** (quote seen only in a search
  snippet, or the source covers part of the question), **not found**.

None of Olsen's drawings is to scale, and no drawing gives a radius. Every curve below is a
shape read off a sketch; only the printed dimensions are numbers.

---

## Part A. Olsen's kilns

### `conrad-teardrop`: Calimpong's teardrop kiln (p.124, Fig 4-140; p.125, Figs 4-143 to 4-147)

Fig 4-140, "ALL DIMENSIONS ARE INTERIOR MEASUREMENTS". Checked on the page image.

- **Plan outline**: a straight front wall 39" wide (the firebox end), the side walls bulging out
  in smooth curves to the widest point, 51½" (the ½ faint), then curving in to 48" at a station
  33" further back, then narrowing in a reverse (concave) curve to a neck 16" (?) wide, 12" wide
  12" further on, then a straight 19" run to the chimney. So: a teardrop of convex arcs, with a
  concave transition into a parallel-sided flue neck; the plan is symmetric about the long axis.
  The station spacing from the front wall to the 51½" point is not printed. Grate 15" wide, on
  the axis at the front.
- **Long section**: inside length 9'9" (front wall to chimney wall). Front wall 35½" (?) high;
  the crown rises from the front wall in a convex curve, peaks about a third of the way back
  (height at the peak not printed), and falls steadily to 35" at 24" in front of the chimney
  wall, then down to the exit opening (12" high under a 13" block). The roof is one surface
  over the whole plan, not an arch across the width.
- **Door**: side door 33" wide × 37" high, its far jamb 48" from the chimney wall. Drawn with
  vertical jambs and a flat head with rounded corners (not a semicircle).
- **Stoke hole** 9" high, sill 14" above the floor; ash pit 12" deep × 24" long.
- **How built** (captions p.124, photos p.125): IFB walls in stretcher courses, double side
  walls (4-144); top courses stepped and slanted inward as the skewback for the casting (4-143,
  4-144 photos); dome shaped in dirt on the plan outline, plastic over it (4-144 photo); a cast
  dome, "too thin and had to be thickened by adding more castable over the top" (4-146);
  buttressed with stones and concrete (4-145).
- **Not given**: dome thickness (only that the first casting was too thin), crown height,
  wall thickness, castable used.

#### Estimates scaled from the figures (2026-10-30, at the user's request)

These are **estimates**, not printed values: each was measured on the page images and scaled
against a dimension printed on the same figure. Book p.124 is PDF page 111 of
`kiln-reference.pdf` (index 110; book page − 13 holds here), p.125 is index 111. Rendered at
300 dpi; pixel positions found by tracing the drawn lines (the darkest pixels in each column).

| Quantity | Estimate | Photo or figure | Scaled against | Uncertainty |
|---|---|---|---|---|
| Crown height, floor to the inside of the crown | **45 in** | Fig 4-140, long section (p.124) | The door's printed 37 in (416 px → 11.24 px/in); checked against the printed 35 in at 24 in from the back (397 px → 11.34 px/in) and the 35½ in front wall (10.8 px/in) | ±2 in: the crown line is 503 px above the floor; the three printed heights give 44.4–46.6 in, as the sketch isn't drawn exactly to scale |
| Rise above the 35 in springline | **10 in** | as above | as above | ±2 in |
| Where the crown peaks | **53 in behind the front wall** | as above | The printed 9'9" (1260 px → 10.77 px/in horizontally; the 33 in door gives 10.67) | ±4 in: the crown is flat within a line's width from 50 to 58 in |
| Dome thickness at its edge, finished | **5½ in** | Fig 4-147 (p.125), the front of the finished kiln | The stoke hole's printed 9 in height (120 px → 13.3 px/in): the cast shell's front edge shows 70–80 px thick over the front wall | ±1½ in: the edge is rough, partly blackened and seen a little from above; the photo shows the thickened shell (4-146: the first casting was too thin and more castable was added over the top), and its thickness over the crown can't be seen |

The plan widths printed in Fig 4-140 (39, 51½, 48, 16 and 12 in) are fitted in
`examples/olsen/conrad-teardrop.yaml` by a teardrop of tangent arcs with a flat front and the
book's neck (`chamber.outline`, 2026-10-31): the 51½ in round end cut square by the 39 in front,
sides of 145 in radius, each turning in a reverse curve of 32 in radius into a 12 in neck that
runs straight for its last 19 in to the back wall, 117 in from the front (`outline.necked_teardrop`).
The two radii were fitted by a grid search to the 48 in and 16 in widths: the plan is 16.7 in wide
12 in before the neck (the book's 16), but only 43.9 in 33 in behind the widest point (the
book's 48), as the round end, fixed by the 51½ and 39 in, puts the widest point 17 in behind the
front where the drawing puts it about 37 in back (unprinted), and fuller sides would bulge past
the round end. Its area, 3962 in², is 6 % under the 4206 in² of the printed widths joined by
straight lines. (The earlier fit, sides of 200 in meeting in a point, had 4321 in² but no neck.)
The dome is the sphere centred over the estimated crown, through the plan's farthest points (the
neck's back corners), 10 in above the 35 in springline there.

**The door's head**, measured on the page image at 600 dpi (2026-10-31; 20.8 px/in from the
printed 33 in width): the jambs stand about 33 in, the head rises about 4 in to its crown at the
printed 37 in in a shallow curve, and its corners are rounded to about ¾ in, so **1 ± ½ in** (an
estimate). The example lays it out flat at 37 in with 1 in corners (`head: flat`, `corner`).
What spans it isn't printed, and no source gives statics for a flat or near-flat head over a
door in hot refractory: the engine's door statics are Heyman's for a semicircular ring and
AISC's for a steel lintel; BIA's jack and segmental minor arches (door-headers.md §D3.3, §D3.4)
are cold building brick, need an allowable crushing stress no refractory maker gives (§D8), and
a jack arch needs tapered voussoirs on cut skewbacks. So the head is laid out and reported as not
checked. Drawn as a segmental head (rise 4 in on 33 in, S/r ≈ 8) it would fall inside BIA's
Fig. 3 range, so its thrust could be worked out by §D3.4; what blocks the check is the
allowable stress.

### `bae-gilgama`: Mr Bae's gilgama (p.107, Fig 4-67; p.108)

Checked on the page image (p.107 faded).

- Text (p.107): "The kiln was bricked up in a teardrop form using [?] bricklaying technique
  (Fig. 4-74) butting into the back wall". The technique's name is unreadable.
- Fig 4-67 (isometric): a single tube whose plan is an elongated oval/teardrop, 16' long at the
  base; "4'" and "6'" across the plan (which is width and which is a station unclear); "4½'"
  (?) to the tallest point; front mouth "18"" with a "4'" combustion area below; slope marked
  "20°" (text says 20 %, Flagged in `olsen-kilns.md`). The roof is one continuous shell, the
  walls curving straight into it with no visible springing line.
- Door: round-headed (near-semicircular, taller than wide) firebox mouth (Fig 4-69 photo).
- Exit: two 4½ × 9" flues in a flat back wall; chimney 8'.
- **Not given**: radii, shell thickness, any section across the tube, brick type.

### `gulgong-racer` (p.118, Fig 4-117; p.119 text; p.120, Figs 4-118 to 4-124; p.121)

Checked on the page image.

- Fig 4-117 (isometric section): a box chamber with the ware platform "5 X 5", firebox "5 X 5"
  at the front, step "1.5'" (?) between; the roof labelled "MORAL COOLCAST 140" is a curved
  shell over the chamber, "4'" high at the front, "3'" at the middle, falling to the chimney
  (5 × 9" (?) brick chimney, 8'). Front door under a brick semicircular ring arch.
- p.119: side walls on the upper platform "only 1ft (30cm) high, sloping down to meet the
  firebox platform and the entry door arch"; dome "shaped using local dirt capped by a thin
  layer of wet sand smoothed to a final finished shape and covered with plastic".
- Fig 4-120 (photo, caption "Finishing door arch and side skews with platform construction for
  forming the dirt mound"): the door arch is a ring of IFB headers; the side skews are bricks
  laid sloping inward; the platform under the mound is corrugated iron on supports.
- Figs 4-121, 4-122: plastic over the mound; Coolcaste 140 placed by hand from the edges.
- Fig 4-124: walls buttressed "with concrete and rocks"; Fig 4-125 adobe of dirt, straw and
  cement over the casting.
- **Not given**: dome thickness, rise in section, radii.

### `hohr-2003` (p.122, Fig 4-129; p.123, Figs 4-132 to 4-139)

Checked on the page image.

- Fig 4-129 (plan): rectangle, firebox one third, stacking two thirds; the front corners cut
  off at an angle (a chamfered front, wider at the stacking area); shelves "40 X 50CM". No
  dimensions in feet or inches.
- Captions: 4-134 "Preparing the wall skewbricks for building the wood platform for the
  shaping dirt"; 4-135 key brick placed in "the entry door arch" (a brick ring arch, near
  semicircular in the photo); 4-136 dirt mound "covering with a thin layer of wet sand for
  final shaping ... covering with plastic for casting with a 2600 IFB (low iron) castable";
  4-137 "two round dowels in the casting for blow holes and coffee can on the back downhill
  slope, for possible side-stoke holes"; 4-138 buttress of "concrete and rocks and rubble".
- **Not given**: any size of the dome.

### `bowen-mountain` (p.127, Fig 4-153)

Checked on the page image.

- Long section: the arch is drawn in the long section, springing from the front wall (with
  "BRACING" on its face) and curving down along the length to the back; "36"" floor to crown
  near the front third, "18"" at the back wall; chamber "5'" long. So the crown height falls
  by half along the length, a vault whose section changes from front to back.
- Plan: "5'" × "3'" chamber, "9" WALLS"; door "24" (+-)" in the side wall.
- Arch thickness drawn about as thick as the 9" walls, but not dimensioned. The cross-section
  (across the 3' width) is not drawn.
- **Not given**: rise across the width, the curve's shape, arch brick.
- Re-read at 300 dpi, 2026-10-31: the front wall stands upright from the floor to about the
  height of the back wall's "18"", where the drawing puts "BRACING" on its face, and the arch
  springs from it there; the crown's "36"" arrow stands near the middle of the 5' (about 0.43 of
  the way back by scale). So the vault is one arch spanning the length, front to back, springing
  from both end walls at about 18", rising 18" (3.6 in/ft of the 60" span): the section across
  the width is a rectangle rising from 18" at the end walls to 36" mid-way. The front springing's
  height is drawn, not printed. The salt hole "built into door" is drawn about 30" up (by scale);
  the door's height isn't printed. Used in `bowen-mountain.yaml` (`roof.along`).

### `tamba` (p.86, Figs 4-11 to 4-13; p.87, Figs 4-14 to 4-16)

Checked on the page image; Fig 4-15 is cut off at the left page edge.

- Fig 4-11 (photo inside the tube): a low vault of rough masonry; the doorways in the side are
  tall round-headed openings rising into the vault, near parabolic.
- Figs 4-12, 4-13 (sections across the tube): the tube is a near-semicircular (slightly
  pointed) arch section resting on the floor, no vertical wall. Chamber flue holes in the
  cross-wall, round-headed, "20 x 12"" and "24 x 12""; firebox flue holes "9 X 18"", four
  round-headed slots.
- Fig 4-14 (photo): a doorway, round-headed and taller than wide, under a projecting hood arch.
- Fig 4-15 (section through a door): "SUPPORTING WALL IN FRONT OF ALL DOORS"; the vault
  continues over the door, the opening cut through the springing; "3½'" (?) tall; "STOKE
  HOLES"; "FLUE MIDDLE CHAMBER". Other sizes unreadable (cut off).
- Fig 4-16 (long section, firebox): firebox "6'" long, "4'" drop; first chamber "3½'" tall
  under a curved vault; the vault steps up in segments along the slope.
- **Not given**: tube width, wall/vault thickness, radii.

### `breda-bottle`, `bottle-two-storey`, `sevres` (pp.166–169, Figs 6-49 to 6-58)

Checked on the page image.

- Fig 6-50 (Breda, exploded): round chamber "15'" diameter, "7'" high; "KILN WALL – 2' thick"
  with "METAL BANDING"; "DOME CEILING" with "CHIMNEY HOLES"; on it a "CHIMNEY BOTTLE" drawn as
  a cone, "12'" across at its base, "25'" high (the 25' faint), its sides slightly convex;
  "KILN DOMED FLOOR" (the grate floor) a shallow segmental dome "3'" above the grate.
- Fig 6-51: the domed floor is a segmental arch section, thinner than the wall, pierced by
  4½" inlet flues; firebox below "SLOPES UP SHARPLY" to the walls; 2' high bag wall.
- Fig 6-52 (photo, inside): the dome ceiling is brick in concentric horizontal rings.
- Fig 6-53: the dome ceiling is shallow; 8 dome exit flues in the centre and "21 – 4½ x 5"
  exit flues" round the perimeter; "9" WALLS IN CHIMNEY CONE"; a door in the cone "for cleaning
  dome and repair".
- Fig 6-54 (two-storey bottle kiln, section): lower chamber with a round-headed (near
  semicircular) vault; upper (bisque) chamber whose walls curve in at the shoulder to a neck,
  the bottle profile; "12. EXTREMELY THICK DOME (2' or more)" between the storeys.
- Figs 6-55 to 6-58 (Sèvres): the model shows a lower chamber under a semicircular-section
  dome and an upper chamber under a taller pointed dome narrowing to the flue; the photos show
  hemispherical outer domes of brick in horizontal courses, iron bands round the walls.
- **Not given**: dome rise, dome thickness at Breda, any Sèvres number.

### `fireworks-edmonton` (p.178, Figs 7-1, 7-2; p.179, Fig 7-3; p.181, Figs 7-5 to 7-7)

Checked on the page image.

- Fig 7-1: two arched tubes at right angles, a groundhog crossing an anagama, their vaults
  meeting in a groin. A concept, not a built kiln: the section shows how the fire and ash travel
  through the two systems, and gives no height for either arch (the user, 2026-10-31). The
  heights are the designer's choice; about 5 ft for the anagama and 6 ft for the groundhog is a
  reasonable start (the user's estimate, not printed).
- Fig 7-2 (plan): a cross: four arms (two fireboxes, the anagama chimney, the groundhog
  chimney) with the walls between the arms curving inward (concave) round an oval "FIRE ZONE";
  "DIAGONAL – 9' (FIREWORKS)".
- Fig 7-3: entry door "size optional", drawn round-headed.
- Figs 7-5, 7-6: freehand sketches, no numbers; Fig 7-7 photo: the dome covered in stones.
- p.183: fire zone about 3½–4½ ft to the ceiling's vertex. **Not given**: dome thickness, form.

### `kanayama-multi` (pp.183–189, Figs 7-12 to 7-33)

Checked on the page image (pp.184, 186, 187).

- Fig 7-12 (isometric plan): the chamber outline drawn round 16 numbered shelves; four arms
  (two fireboxes, two chimney ends) with the walls between them in concave and convex curves,
  so the plan is a wavy cross. No dimensions.
- p.186 text: "The 9in. (23cm) walls, as well as the chimneys, were laid straight up to 1[?]
  rows high. Thereafter the next layer of header bricks was slanted in to begin the transition
  to the castable." "Door arch frames were made for each firebox and the three door ring arches
  were laid ... In one door the ring arches increase in width and height to accommodate the
  form of the casting." "The transition bricks in row 14 were angled even further toward the
  kiln to give the angle for the castable form." Then "a collapsible-frame support system was
  built at the level of the transition brick inside the chamber. Plywood and other flat boards
  were used to make the platform to hold the dirt", dirt shaped, "a thick layer of sand over
  the dirt", "wetted for the final shaping".
- p.187: "covered with plastic to prevent the sand from absorbing the water from the castable,
  which has to be cast on a non-porous surface"; castable placed from the perimeter, "built up
  to 5 to 6in. (12.5 to 15cm) thick"; "make a ledge pointing down into the form to receive the
  next layer".
- Figs 7-25, 7-28: door ring arches are semicircular brick rings; the stepped rings of the
  flared door are visible. The inside (7-27, 7-28) is a smooth pointed-to-round vault.

### Corbel and dome rules (p.49, Fig 2-23; p.51, Figs 2-28, 2-28A; p.134)

Checked on the page image.

- p.49: "Use the corbel arch to span up to 61cm (24in.)". Small 10 to 16 ft³ kilns with
  corbel arches are "not a good practice": structural instability, uneven surface, erosion.
  Fig 2-23 draws each course stepping in by roughly a third to half a brick length, but the
  step is **not dimensioned**. No overhang limit per course is printed.
- p.51: a dome is part of one sphere, a crown two sphere radii; rise 2½–3 in per foot of span;
  "Standard bricks can be laid in header or stretcher courses"; Hendo's dome gauge (Fig 2-28A):
  a swing arm from the dome's centre point, moved up each row, "gives the pitch of each brick
  to make the dome's radius"; the arm measures the outside edge, a block on it the inside edge.
- p.134 (the page the plan cites for corbel kilns) is **Singh's round downdraft** (Figs 5-10,
  5-11), not a corbel kiln: a round chamber 7' across under a brick dome of radial courses,
  "2'" (?) rise above the springing line, "5'" chamber height (which points the 5' spans is
  unclear), 9" walls. Useful as a round-dome example; dome thickness not dimensioned. No corbel
  kiln is drawn in the book's scanned pages.

---

## Part B. Outside sources

### Dome and conical brick layouts

| Source | Quote / content | Status |
|---|---|---|
| HarbisonWalker, *Handbook of Refractory Practice* | Searched for its dome and circle-brick tables; no online copy or excerpt found. | Not found |
| A.P. Green "Pocket Guide", via Masonry Heater Assoc., https://www.mha-net.org/docs/v8n2/wildac15h.htm | "an arch brick circle layout table, from the famous A.P. Green Refractories 'Pocket Guide'" (table in MHA members' area) | Partial (search snippet; table not seen) |
| ASTM C909, *Dimensions of a Modular Series of Refractory Brick and Shapes*, https://store.astm.org/c0909-18r22.html | Covers "straight, split, soap, arch, wedge, and key brick" in common US use. Paywalled; no dome or circle shapes named. | Partial |
| BS 3056-2 (glass-furnace brick sizes), https://knowledge.bsigroup.com/products/sizes-of-refractory-bricks-specification-for-bricks-for-use-in-glass-melting-furnaces | Keywords list tapered and circle shapes; withdrawn (per search summary). | Partial |
| FAO, Brazilian beehive charcoal kiln, https://www.fao.org/4/X5328e/x5328e0g.htm | "The dome is constructed with the thickness of half a brick and it is extremely important that a minimum of mortar is placed between the bricks. The bricks are laid and kept in position more by lateral pressure than by mortar." A peg with a cord guides the dome (a radius gauge, like Hendo's). Dome springs at 1.80 m wall height; no radius or rise. | Sourced |
| Medalta beehive rebuild, https://albertashistoricplaces.com/2015/09/09/rebuilding-the-beehive-kiln/ | Stability from compression in "each concentric ring of tightly fitted brick"; "Each row of fire brick is re-laid and tightly fitted with new keys". | Partial (search snippet) |
| NPS National Register nomination (beehive kiln), https://npgallery.nps.gov/GetAsset/92038d01-dcfe-4323-8e48-42d41cff2843 | Crown "one course of brick laid in a circular pattern ending at the peak of the crown with a specially made keystone brick"; iron bands round the structure. | Partial (search snippet) |
| Conical / dome brick shapes sold by makers | No maker's catalogue of dome (doubly tapered) shapes found. | Not found |

### Cast-dome forming

| Source | Quote / content | Status |
|---|---|---|
| Olsen pp.58–59, 119, 123, 186–187 | Dirt mound on a braced platform, wet sand skin, plastic; cast from the skewback up in one session; 5–6 in; 24 h damp cure; buttress before striking (Part A; `kiln-reference.md` §4). | Checked on the page image |
| Castable instructions (Forno Bravo file), https://community.fornobravo.com/filedata/fetch?id=426785 | "Mould should be watertight and structurally strong and treated with a suitable release oil or grease to facilitate stripping." | Partial (search snippet) |
| AGC Ceramics, monolithic refractories, https://www.agcc.jp/Portals/0/images/en/core/shokyakuro/about/monolithicRefractory.pdf | "To facilitate removing the form from the refractory lining, apply oil, grease, lubricant or wax, etc., beforehand"; vibration casting essential for low-cement castables, forms stronger under vibration; cure at least 24 h. The URL returned 404 on fetch. | Partial (search snippet) |
| BS 7335-1:1991, code of practice for installation of monolithics by casting, https://knowledge.bsigroup.com/products/installation-of-monolithic-refractories-code-of-practice-for-installation-by-casting | Exists; paywalled. | Partial |
| HarbisonWalker, Allied Mineral, Plibrico, Thermal Ceramics installation guides | No guide addressing dome forms (sand or lath) found online. | Not found |

### Corbel overhang per course

| Source | Quote | Status |
|---|---|---|
| Brick Industry Association, *Corbels* bulletin (2025), https://www.gobrick.com/media/file/BB%20Corbels_082025.pdf (p.2, citing TMS 402) | "The maximum projection of a single unit/course must not exceed the smaller of: One-half the nominal height of the unit; One-third the nominal thickness of the unit or wythe" (p.2). p.3: "The maximum projection of the entire corbel beyond the face of the wall must not exceed either: One-half the overall wall thickness for multi-wythe composite solid masonry; One-half the nominal unit thickness for walls with an air space". Nominal = specified size plus one mortar joint. Prescriptive only for **non-loadbearing** corbels (p.2). | Sourced (PDF text read 2026-10-31) |
| Pitelka, in `door-headers.md` [H12] | A 9 in flue roofed by a corbel, "the third course projects 2 in each side". | Verified there |
| Rhodes, in `door-headers.md` [H10] | "Corbel arches are not practical for openings more than about 18 inches across." | Excerpt there |
| Olsen p.49 | Corbel arch up to 24 in; corbel roofs poor practice. | Checked on the page image |

TMS 402 is for structural masonry at ambient temperature, not refractory at heat; using it for a
kiln is an assumption the engine must state.

---

## Gaps

- **No radii anywhere.** Olsen's drawings give stations and heights, not radii or curve
  definitions; a teardrop or crossing-axis outline from these figures is a fitted curve, not a
  sourced one. Station positions of Calimpong's widest point and crown peak are not printed
  (the crown's is estimated from the figure above).
- **Cast-dome thickness** is printed only for Kanayama (5–6 in) and Olsen's general rule (6 in
  for 10–12 ft domes, `kiln-reference.md`); not for Calimpong, Gulgong, Höhr or Fireworks.
- **Crown heights**: Calimpong's peak (estimated above, 45 ± 2 in), Bae's (4½' (?)), Bowen Mountain's cross-section rise,
  Breda's dome rise: not given.
- **Dome/circle brick tables** (HarbisonWalker, A.P. Green): not obtained. A user copy of the
  Handbook of Refractory Practice or the A.P. Green Pocket Guide is needed.
- **Conical/dome brick shapes**: no maker's catalogue found; ASTM C909 (paywalled) covers only
  arch, wedge and key shapes.
- **How far a course may lean before it needs a form** (layer 4 of the plan): no source found.
- **Corbel limit at temperature**: only the ambient masonry rule (TMS 402) is sourced; the engine
  (`corbel.py`) uses it as it stands and says so. With Rhodes's 6 in lintel brick on top, the
  whole-corbel limit (half the wall) caps a corbel at 6 in + the wall's thickness: 15 in in a 9 in
  wall, under Rhodes's 18 and Olsen's 24 in.
- **Crossing-axis plans** (Fireworks, Church, Kanayama): Fig 7-2 dimensions only the fire zone's
  diagonal; no arm widths, curve radii or vault sections for the two crossing tubes (Fig 7-1 is
  undimensioned). Kanayama prints none at all. The sizes are the designer's (the user,
  2026-10-31); the engine takes them as inputs (`roof.crossing`).
- **Groin vault statics**: masonry-statics.md §M4 now records one worked example (Maia Avelino
  et al. 2020: forces along the diagonals, corner thrust 67.5–96.7 % of W) and Heyman's slicing
  (summary only). Not yet applied: the engine checks each vault as a barrel vault on its walls
  and reports the groin as unchecked; a slicing check on the diagonals is the next step.
- **Castable makers' forming guidance**: only general release-agent and watertight-mould
  statements, from snippets; no maker's guide on sand or lath dome forms.
- **Corbel kilns**: the book names them (p.49) but draws none; p.134 is a round dome.
