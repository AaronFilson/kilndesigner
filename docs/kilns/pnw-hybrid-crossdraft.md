# The PNW hybrid cross-draft: results

_Rebuilt 2026-10-30 with the author's answers in (below: "With the answers in"). The section after
it, "What the engine found before the answers", is the earlier 2026-10-30 build, kept for
comparison. Rebuild with `uv run kilndesigner build examples/pnw-hybrid-crossdraft.yaml --out out/pnw`
and `uv run kilndesigner simulate examples/pnw-hybrid-crossdraft.yaml --chart`. Every number
below has its working and source in the report and plans._

## The design as entered

- Cross-draft, cone 10 (1285 °C / 2345 °F at 60 °C/h, Orton), burners through the front wall
  (the right wall in the car variant), flue and chimney at the back.
- Chamber 28 in wide × 60 in long × 44 in to the springline, under a 60° sprung arch with a
  3¾ in rise: **45.2 ft³** by Ward's method. Stacking space will be less.
- Walls 8 in: 4½ in JM 26, 2½ in K-23, 1 in 8 pcf blanket (budget: 4½ in JM 26 and 3½ in 6 pcf
  blanket). Floor 4½ in JM 26 on 2½ in K-23. Roof: 3 in cast Kast-O-Lite 30 LI Plus under 2 in
  of blanket.
- 240 V, 60 A breaker (48 A continuous, 11.5 kW) of Kanthal APM in the left wall, off above
  1650 °F; propane from four 100 lb cylinders (budget: a 500 gal tank); coldest day 20 °F.

## With the answers in

| | Bricked door | Car | Budget lining |
|---|---|---|---|
| Door | 24 × 40 in, sill at the floor, **arched brick head** (semicircular, springing at 28 in) | the car's end | as the bricked door |
| Burners | 8 × Ransome B3 at 1.0 psi, 56,510 BTU/hr each, 452,083 in all, through the door, two columns of four up its sides | same, through the right wall | as the bricked door |
| Burner ports / exit flue | 8 × 4¼ in round, 113 in² / 113 in² (1:1) | same | same |
| Propane | 11 × 100 lb cylinders: meets 452,083 at 20 °F full (1,243,000), half (704,000), ¼ keeping 10 psi (476,300) | same | same (the tank is gone) |
| Priced materials | **$11,606** | $11,566 + the car's hardware | **$9,859** |
| Errors / warnings | 0 / 1 (the budget) | 0 / 1 | 0 / 1 |
| Simulated firing, setting and ware 2,624 lb (ware 7 × the setting), hand-over 1650 °F | 65 h 12 min, $150.03 | same | 59 h 13 min, $140.95 |
| Electricity / propane per firing | 705.4 kWh / 18.7 gal | same | 636.9 kWh / 18.4 gal |

1. **The door** (`loading.opening`: 24 × 40 in, sill 0, `head: arch`): **an arched brick head**,
   the author's choice. It passes: the 3 in ring is 2.1 times the thinnest that holds a line of
   thrust, and the 10 in jamb holds its least thrust (8 lb; 7 lb in the budget lining) 6.1 in
   from the door, inside its middle third (to 6.7 in), needing friction 0.25 of 0.6 (Heyman's
   statics; `frame.door-arch`, `frame.door-jamb`, `frame.door-slide`). Bearing under it, 3.4 psi
   at the springing and 3.8 psi at the jamb's toe, is reported, not checked (no allowable
   bearing stress for refractory brick is published, refractory-bearing.md). The arched head
   adds $46 of brick over the lintel. The car variant keeps no opening: a car's door is its whole
   end.
   - **The roof stays a cast sprung arch** in these brick versions (the author's decision): it
     springs from the side walls and runs front to back, so it puts nothing on the front wall
     (door-headers.md §D7). The dome comes with the castable version later.
2. **Burners: eight.** The same design input (Olsen's Rule 1, 452,083 BTU/hr) split eight ways is
   56,510 BTU/hr each; the library's cheapest burner carrying that within its pressures is the
   Ransome B3 at 1.0 psi ($1,960 for eight). **Up the sides of the door, evenly** (the author's
   layout): two columns of four, 9 in either side of the middle, at 4⅝, 12⅛, 19⅝ and 27⅛ in up:
   one 2½ in course off the floor (Pitelka [S4]) and then every three courses, 7½ in apart. Each
   4¼ in port is 0.9 in in from its jamb, and the top ones end 3¼ in under the arched head at
   their outer edge (the head is 32.5 in up there). All eight are cut, none refused; the
   engine's port checks are the wall's edges and top and the other ports, and it has no
   separate margin to a door's jambs or head, so these clearances are the layout's, not a
   sourced rule. With eight ports the exit flue is sized 1:1 to them: 113 in² (p.151, p.236),
   and `hardware.flue` passes. The car's eight spread along the right wall.
   - Spy holes: the engine now puts them above the burners, in the middle of the door, at 33,
     35⅞ and 38¾ in up. The top one (2¼ × 2½ in, 3 in right of the middle) reaches 40 in, about
     ¾ in past the arched head over it (39.3 in up at its outer edge): move it down or set it
     by hand (`spy_holes.places`).
   The **removable welded-steel rack** they hang on is hardware the engine doesn't size: no
   source gives one, so it is listed here and left unsized and unpriced.
3. **Propane: 11 cylinders.** The least count that meets the burners' draw at 20 °F in every case
   the engine checks, down to ¼ full keeping 10 psi (Flame Engineering's table read at the
   liquid's temperature; combustion-and-masonry.md §2.1–2.3, §2.8). Five clear the error (full,
   565,000), eight are enough half full (512,000), eleven ¼ full (476,300; ten give 433,000).
4. **Budget.** $5,000 stays. The brick kiln is $11,560 priced (the eight burners add $1,170 over
   the two B5s, and the larger flue for their ports 40 more chimney bricks, 229 in all; the
   cylinders aren't on the bill), the budget lining $9,837: both over. The linings
   are unchanged; the castable version the author plans is the one to bring under budget.
5. **The switch-over stays at 1650 °F**: the start of shino reduction, cone 012 to 010 (Orton,
   861–915 °C, about 1580–1680 °F by rate, `cones.yaml`). The glaze sets it, not the cost chart's
   cheapest point. (The cost chart was last run on the shelves-only stack; rerun it with
   `kilndesigner simulate --chart` for the full load.)
6. **The setting and the ware.** `firing.setting` describes the stack and the engine weighs it
   (`furniture.py`): four 12 × 24 × 1 in mullite shelves a layer, 24 in across the 28 in width and
   12 in along (4 in in front, 1 in between and at the back fit four in the 60 in: Olsen p.142,
   p.151, Fig 5-82), weighed from Olsen's 20.5 lb shelf (p.33–35): **328 lb of shelves**. **Four
   layers is an assumption**, not sourced or confirmed. **No posts**: no source gives a post's
   size or weight, so they are left out (the setting is shelves only). The **ware weighs 6 to 8
   times the setting** (the author, 2026-10-30, not a published source); the design uses 7, the
   middle: 2,296 lb of ware, 2,624 lb with the shelves. Across the range, hand-over 1650 °F:

   | Ware ÷ setting | Setting and ware | Bricked door / car | Budget lining |
   |---|---|---|---|
   | 6 | 2,296 lb | 60 h 37 min, 833.9 kWh in, 655.3 kWh + 17.2 gal, $138.96 | 54 h 56 min, 766.5 kWh in, 590.2 kWh + 17.0 gal, $130.33 |
   | 7 | 2,624 lb | 65 h 12 min, 899.7 kWh in, 705.4 kWh + 18.7 gal, $150.03 | 59 h 13 min, 828.6 kWh in, 636.9 kWh + 18.4 gal, $140.95 |
   | 8 | 2,952 lb | 69 h 46 min, 965.3 kWh in, 755.3 kWh + 20.1 gal, $161.10 | 63 h 30 min, 890.8 kWh in, 683.5 kWh + 19.9 gal, $151.58 |

   ("kWh in" is the heat put into the kiln; then electricity and propane bought.) The long
   firing is the 11.5 kW of elements heating over a ton of ware to 1650 °F; an earlier hand-over
   would shorten it.

## What the engine found before the answers

| | Bricked door | Car | Budget lining, 500 gal tank |
|---|---|---|---|
| Heat loss held at cone 10 | 14.31 kW | 14.31 kW | 14.33 kW |
| Hottest outside face | 281 °F (the arch) | 281 °F | 281 °F |
| Burners | 2 × Ransome B5 at 2.4 psi, 452,083 BTU/hr | same | same |
| Supply at 20 °F | **short**: full cylinders 452,000 BTU/hr | **short** | meets it: 462,360 BTU/hr at ⅓ full |
| Priced materials | **$10,178** | $10,178 + the car's hardware | **$8,500** |
| Simulated firing (empty kiln, hand-over 1650 °F) | 28 h 34 min, $61.08 | same | 24 h 58 min, $55.85 |
| Electricity / propane per firing | 307 kWh / 6.9 gal | same | 265 kWh / 6.9 gal |
| Cheapest hand-over (chart, every 200 °F) | 1200 °F: $54.78, 14.9 h | same | 1400 °F: $53.18, 18.1 h |
| Errors / warnings | 1 / 1 | 1 / 1 | 0 / 1 |

1. **Burners.** The design input is now Olsen's Rule 1, the low end of Ward's range
   (10,000 BTU/ft³/hr × 45.2 ft³ = 452,083 BTU/hr; Olsen p.226–228, Ward [S28]), not Ward's
   high end (723,000) as on 21 October. The tool picked the fewest burners that carry it (two
   B5s); Olsen's cross-draft builds use four to six (p.226–228), and no source gives a rule, so
   set `burners.count` to spread the heat.
2. **Four 100 lb cylinders still fall short at 20 °F**, now by a hair when full (452,000 against
   452,083 BTU/hr), and well short half full (256,000) or ¼ full keeping 10 psi (173,200). The
   cylinder table is now read at the liquid's temperature, 20 °F below the air under draw
   (combustion-and-masonry.md §2.3, §2.8). A 500 gal tank kept ⅓ full gives 462,360 BTU/hr.
   95 gal on hand lasts 19 h at full fire.
3. **Electricity is the cheaper heat at every temperature** ($0.12/kWh against $0.149 per useful
   kWh of propane at 300 °F, $0.380 at 2300 °F; Cantera). The elements alone could hold the
   kiln to about 2019 °F against steady loss, and stall in the simulation at about 1993 °F.
4. **The switch-over.** As set, 1650 °F (reduction from about 900 °C, Finkelnburg [S66]). The
   simulation puts the cheapest firing at a hand-over near 1200 °F ($54.78, 14.9 h) against
   $61.08 and 28.6 h at 1650 °F: past about 1200 °F the 11.5 kW of elements climbs so slowly that
   the longer firing's losses cost more than the cheaper heat saves. Fastest is to light the
   burners at once (400 °F: 4.8 h, $59.88). These are an **empty kiln**; ware adds heat and time.
5. **Chimney and flue.** With burners under pressure the chimney need only reach the kiln's top
   (Olsen p.151), a hood and stack taking the gases on: 53 in above the floor, 9 × 9 in inside,
   one 4½ in layer of hard brick (189 straights, $1,030). The exit flue starts at the burner
   ports' 57 in² (p.151, p.236), built big to brick down. The 21 October "14 ft" was the
   natural-draft Rule 5 and no longer applies. Draft 0.043–0.054 in. w.c.
6. **Elements.** Two elements of 8 AWG (3.26 mm) APM, 180.6 ft each, in parallel across 240 V,
   coiled into 480 in of groove each (16 rows in the left wall), at 6.58 W/in² (Olsen's 6.4–9 for cone 10, p.254, p.257) and a
   3.13 d coil pitch. Thicker wire than before, for longer life (Kanthal). APM wire is unpriced.
7. **Steel.** A sprung-arch frame of L4×4×5/16 (four corner posts 53.6 in, two buttresses
   84 in), ¼ × 2 in flat bar cross-members and two ½-13 tie rods. The heated arch's thrust is
   231 lb/ft (Heyman statics, within 4 % of HarbisonWalker's table, which stops at T/S 10 %; this
   arch is 10.7 %). The buttress needs Sx ≥ 1.156 in³ (has 1.270); bent about its principal axis
   it would see 14,919 psi over the 12,000 psi used, which depends on how the brick holds it
   (kiln-hardware.md §4.5). Unpriced: 36 ft angle, 35 ft flat bar, 11 ft rod.
8. **Masonry.** 655 JM 26 (496 whole, 127 cut into 176 pieces) and 367 K-23, with the BIA's 5 %;
   skewbacks and fill about 22 bricks a side, cut to 60°; 394 lb (8 bags) of Kast-O-Lite for the
   4.08 ft³ arch; 90.8 ft² of blanket. Budget: 655 JM 26, 90 K-23 (the floor), 70 ft² of 3½ in
   6 pcf and 17.7 ft² of 2 in 8 pcf blanket. Cure the castable 24 h above 60 °F and dry it out
   per HWI Schedule 4 (100 °F/h to 1200 °F, 1 h hold per inch: castables.md §14.2).
9. **The castable's specific heat** is a class value: VDI Heat Atlas, sillimanite, 978–1093
   J/(kg·K) over 400–1200 °C (castables.md §14.3, status `derived`). HWI gives none. It is held
   at 978 below 400 °C, which overstates the heat stored early (the conservative side). The
   simulation runs without a value in the design.

## Open, needs the author

1. **The burners' rack:** the engine has no source to size it.
2. **The setting:** the number of shelf layers (four, assumed) and the posts' size and material
   (left out, unsourced).
3. **The top spy hole** reaches past the arched head (above): where should it go?

## The author's answers (2026-10-30)

- **Propane: more 100 lb cylinders**, not a tank. The design adds cylinders to the manifold until
  the cold-day check passes (to do: how many).
- **Budget: $5,000 stays.** This brick kiln is over it; the author will make a castable version
  of the kiln once castable linings are worked out, and that version is the one to bring under
  budget.
- **Switch-over: at the start of reduction for shino, about cone 012 to 010.** Orton's large
  cones put 012 at 861–882 °C (1582–1620 °F) and 010 at 903–915 °C (1657–1679 °F), by rate
  (`core/src/kilndesigner/data/cones.yaml`), so the hand-over is about 1580–1680 °F; the
  design's 1650 °F sits in that range. The firing is set by the glaze (shino reduction), not by
  the cheapest point on the cost chart.
- **Door: 24 in wide × 40 in high, the sill at floor level.** The dome is thick enough to support
  itself over the door, with steel bracing. The burners fire through ports in the door, from a
  removable rack of welded steel.
- **Burners: eight**, for slow flame movement at high volume.
- **Ware and shelves:** estimate a full stack from Olsen's stacking guidance, and say so. Later:
  the ware weighs about 6 to 8 times the setting (shelves and posts); every part of the setting
  is the user's to change.
- **Door head: an arched brick head.** The roof stays a cast sprung arch in the brick versions;
  the dome comes with the castable version.
- **Burners: up the sides of the door, spaced evenly.**
- **Curves** (for the castable version): shapes picked by choice first, point editing later.

## Not sourced, left out

Kanthal APM wire price; steel prices; the car's wheels, rails and seal (no source sizes them);
the burners' removable welded-steel rack; the shelf posts' size and mass; propane
cylinder prices;
an allowable bearing stress for the refractory (shown, not checked); HWI's own c_p.
