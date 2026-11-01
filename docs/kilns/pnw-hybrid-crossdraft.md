# The PNW hybrid cross-draft: results

_Rebuilt 2026-10-30 with the author's answers in (below: "With the answers in"). The section after
it, "What the engine found before the answers", is the earlier 2026-10-30 build, kept for
comparison. Rebuild with `uv run kilndesigner build examples/pnw-hybrid-crossdraft.yaml --out out/pnw`
and `uv run kilndesigner simulate examples/pnw-hybrid-crossdraft.yaml --chart`. Every number
below has its working and source in the report and plans._

## Review on the engine of 2026-10-31

All four designs rebuilt (`build`), simulated as designed (`simulate`), solved for 8 h and 12 h
(`simulate --target`), and the bricked door and castable versions fired slowly (`slow 12h`,
`slow 24h`), on branch `m7-5` at 7a2b1e6. **No design file was changed**: nothing in them is a
mistake, and every value is the author's or already noted as an assumption.

### Numbers then (2026-10-30) and now

| | Bricked door | Car | Budget lining | Castable |
|---|---|---|---|---|
| Errors / warnings | 0 / 1, same | 0 / 1, same | 0 / 1, same | 0 / 3, same (cylinders ¼ full, dome T/S 10.7 %, budget) |
| Chamber | 45.2 ft³, same | same | same | 55.2 ft³, same |
| Heat loss at cone 10 | 14.31 kW, same | same | 14.33 kW, same | 20.29 kW, same |
| Burners | 8 × B3 at 1.0 psi, 452,083 BTU/hr, same | same | same | 8 × B3 at 1.6 psi, 552,249, same |
| Priced materials | $11,606, same (JM 26 now 651, K-23 378: the cut count moved, the total didn't) | $11,566 + the car | $9,859 | $10,088, same |
| Firing as designed (elements to 1650 °F) | 65 h 12 min, $150.03, same | same | 59 h 13 min, $140.95, same | **was** 999 °C at 96 h, $143.57; **now** 1174 °C at 97 h 40 min, $178.77, still not finished |
| 8 h target | 406,332 BTU/hr, $131.44 (was $131.49) | same | 402,965, $130.67 | 536,263, $170.17 (was 535,000, $170.14) |
| 12 h target | 266,418 BTU/hr, $138.60 (was $138.61) | same | 262,661, $135.77 (was 260,000, $135.94) | 350,849, $176.02 (was 349,000, $176.18) |
| Steel | arch frame as before (L4×4×5/16 36 ft, flat bar 35 ft, rod 11 ft) | same | same | dome frame as before (L4×4×5/16 43 ft, flat bar 25 ft, rod 11 ft, 741 lb on the busiest rod) |

Why the castable's plain firing moved: the simulation's 96 h stop now counts only time at full
heat, so a firing that is still climbing runs on (the slow-firing work, 10-30-26.md); it gets
further, burns more, and still doesn't reach cone 10. The target-run differences (under 0.5 %) are
solver tolerance. Nothing else moved.

### What the new checks say about it

- **Domes laid course by course, membrane forces, bands:** for round domes and round kilns. None of
  the four is round; the castable's sail dome is still checked as arches across the side walls.
- **Mortar:** the wedge-joint mortar is for brick rings. These walls are dry-laid IFB and the
  roofs cast; the door's arched ring (3 in, or 4½ in in the castable) passes Heyman's statics as
  before.
- **Foundations:** the designs give none, so none is checked. The floor's loss is taken as a hot
  plate facing down in open air, as on a stand (the report says a slab would lose less).
- **Steel tables, corbels, smoke fireboxes:** the frames are the same sizes; no corbels; gas, no
  firebox.
- **Ware rate:** at 8 h the ware heats at up to 351 °C/h (368 in the castable). The engine reports
  it as information only; the firing speed is the author's.

Numbers that may move with work in progress elsewhere: the **heat loss, firing times and costs**
with the floor's loss into the ground (if a foundation is entered); the **castable's dome** steel
and T/S warning with the cracked-dome and groin work; nothing here depends on bands.

### Firing time against the 8–12 h target

As designed (elements alone to 1650 °F, then the burners) the bricked door kiln takes 65 h; a slow
firing can't be quicker than that either (`slow 12h` comes out at 65 h 21 min, $149.15; `slow 24h`
at 68 h 30 min, $162.72, because 11.5 kW of elements alone is what sets the pace below the hand-over).
The 8–12 h target needs **the burners lit from the start, alongside the elements**:

| Target | Burner input | The design's 8 × B3 | Cost/firing | Propane at 20 °F |
|---|---|---|---|---|
| 8 h | 406,332 BTU/hr | yes, at 23 in. w.c. (they give 452,083 at 1.0 psi) | $131.44 | 11 cylinders: full yes, ¼ full from 13 °F of air |
| 12 h | 266,418 BTU/hr | yes, at 11 in. w.c., their lowest published | $138.60 | 11 cylinders: yes |
| 4 h / 6 h (2026-10-30, not rerun) | 1,002,000 / 574,000 | 6 h at 1.7 psi; 4 h needs B4s | $124.65 / $128.37 | see the table further down |

The cost: the elements stay on into reduction, which shortens their life (no source quantifies
by how much). The castable needs 536,263 BTU/hr for 8 h ($170.17), within its burners' 552,249.

### The castable against $5,000

$10,088 priced, $5,088 over. Ranked: Kast-O-Lite $5,530 (48 bags at $115.21); eight B3 burners
$1,960; chimney hard brick $1,406 (258); blanket $630; K-23 $562. Steel, APM wire, cylinders,
the door's ring and plug, the burners' rack, shelves and the dome's form are unpriced, so the true
total is higher. The sourced levers: the same castable from L&M at $98.18 a bag (about $820 off);
the engine's cheapest burners for this input, 6 × GACO MR750 at 2.9 psi ($599.70, $1,360 off,
but not the author's eight). Both together come to about $7,900, still over.

### Decisions for the author

1. **Firing plan.** (a) As designed: 65 h, $150, elements spared reduction. (b) Burners from the
   start: 8 h $131.44, 12 h $138.60, on the burners you have; elements wear faster in reduction.
   (c) An earlier hand-over somewhere between: rerun `simulate --chart` on the full load to see
   the curve. Setting `firing.target_time: 8 h` (as the castable has) puts (b) in the report.
2. **Budget.** Keep $5,000 and give up something big (no sourced lining here reaches it), or raise
   it: brick budget lining $9,859, castable $10,088 (about $9,270 with L&M's price, about $7,910
   with six GACO burners as well).
3. **The castable's plain firing never finishes** (1174 °C at 97.7 h): fire it to a target only, or
   don't build it with element-only early stages.
4. **The door's sill height.** The design has the sill at the chamber floor (0 in), but the height
   of that floor above the ground isn't given: what is it, and what does the kiln stand on (a
   stand, a slab, block)? It sets the loading height, the floor's heat loss and the foundation
   check, none of which can be worked out without it.
5. **Still open from before:** the burners' rack, the shelf layers (four assumed) and posts, the
   top spy hole's place under the arched head, the castable's door ring and plug, and HWI on
   drying a castable laid on blanket.

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

## Firing to a target time (2026-10-30)

On the design as it stands (elements to 1650 °F, then the 452,000 BTU/hr of burners) the
simulation takes 65 h, $150. Most of that time is the 11.5 kW of elements working alone to the
hand-over. `kilndesigner simulate <design> --target 4h` (or `firing.target_time` in the design,
which adds it to the report) works backwards from a target time. It bisects the burner input
with the firing simulation until the schedule finishes in the target time, then sizes everything
else from that input (`core/src/kilndesigner/target.py`). The run follows the author's answers
(2026-10-30):

- **Heat:** elements and burners run together for the whole firing. The burners are lit at the
  start and the elements stay on to the top, through reduction. The cost is a sourced finding:
  reduction above about 900 °C attacks the elements' oxide layer and shortens their life.
- **Load:** the same full load: the design's setting with a ware ratio of 7, about 2,600 lb.
- **Burners:** the design's count of 8, chosen from the library by the existing sizing rules.
- **Ports and flue:** the flue starts at 1 : 1 with the ports.
- **Supply:** checked at the coldest day, 20 °F.
- **Schedule:** the default (full heat to 100 °C under cone 10, then 60 °C/h). With unlimited
  heat it takes **1.68 h**, the floor for any target.

| Target | Burner input, BTU/hr (/ft³) | Burners (8) | Flue | Propane | Elements' share | Cost/firing | Fastest heating |
|---|---|---|---|---|---|---|---|
| 4 h | 1,002,000 (22,200) | Ransome B4 at 2.0 psi | 142 in² | 10.95 gal/h; 34 gal | 9 % (46 kWh) | $124.65 | 725 °C/h |
| 6 h | 574,000 (12,700) | Ransome B3 at 1.7 psi | 113 in² | 6.27 gal/h; 34 gal | 12 % (69 kWh) | $128.37 | 466 °C/h |
| 8 h | 406,000 (9,000) | Ransome B3 at 23 in. w.c. | 113 in² | 4.43 gal/h; 34 gal | 16 % (92 kWh) | $131.49 | 350 °C/h |
| 12 h | 266,000 (5,900) | Ransome B3 at 11 in. w.c., their lowest published (draw 273,600) | 113 in² | 2.99 gal/h; 35 gal | 22 % (138 kWh) | $138.61 | 247 °C/h |

All four targets are met, and none is limited by the burners: 8 × B5 give up to about 2.0
million BTU/hr. The faster firing is cheaper, because less heat goes into the walls and out of
the shell. The car and budget variants come out within 1 % of the bricked-door kiln: the
budget's 8 h firing needs 403,000 BTU/hr at $130.70, and its 12 h firing 260,000 at $135.94.

**Propane supply options at 20 °F.** The engine lists every option and the user picks one. The
propane burned, and so the cost per firing, is the same whichever option holds it.

| Target | 100 lb cylinders, full / ¼ full | The design's 11 cylinders | Tanks that work (least fill) |
|---|---|---|---|
| 4 h | 9 / 24 | full: yes. ¼ full: no, at any air temperature in the table (to 60 °F) | 1000 gal (47 %) only |
| 6 h | 6 / 14 | full: yes. ¼ full: from 30 °F of air | 500 gal (51 %), 1000 gal (13 %) |
| 8 h | 4 / 10 | full: yes. ¼ full: from 13 °F | 250 (59 %), 325 (38 %), 500 (24 %), 1000 gal (10 %) |
| 12 h | 3 / 7 | yes, both: full from 20 °F, ¼ full from 0 °F | 250 (27 %), 325 (15 %), 500 gal and 1000 gal (10 %) |

A tank's least fill is read between the D × L × K rule's rows. That is derived: K = 45–100 for
10–60 % full (combustion-and-masonry.md §2.3), with the ⅓-full table read as K = 90.

**What limits it:**

- **The schedule.** Its 1.68 h floor is set by the cone's final rate.
- **The ware.** The 4 h firing heats the ware at up to 725 °C/h (1,300 °F/h). The fastest
  sourced schedule is 316 °C/h (Bartlett's Fast Glaze, cone 6; hybrid-firing.md §5). No source
  sets a maximum, so the engine reports the rate and doesn't refuse it. A 4 h cone 10 with a full
  2,600 lb load is beyond any sourced practice. Olsen's fast-fire kiln reaches cone 10 in
  3½–4¾ h, but it is a 12–16 ft³ wood kiln. Even the 8 h firing, at 350 °C/h, is above the
  fastest sourced schedule.
- **The elements.** On through reduction, they give 9–22 % of the heat. Their life in reduction
  isn't quantified by any source (hybrid-firing.md §6).
- **The 12 h firing.** It needs about 33,000 BTU/hr a burner, under the lowest published B3
  rating. Fire the burners turned down below their published range, or light fewer of them.
- **The chimney.** It stays at the kiln's top, 4.4 ft (53 in) above the chamber floor, with a
  hood and stack (Olsen p.151). The flue grows with the burner ports.

## The castable version (2026-10-30)

`examples/pnw-hybrid-crossdraft-castable.yaml`, built on the author's answers: the same chamber
(28 × 60 in, 44 in to the springline), door (24 × 40 in, sill at the floor, arched head), eight
burners up the door's sides, 11 × 100 lb cylinders, setting (ware 7 × the shelves) and site. It
builds with **no errors**. Rebuild with `uv run kilndesigner build
examples/pnw-hybrid-crossdraft-castable.yaml --out out/pnw-castable`.

- **The dome: a sail dome, 2 in of Kast-O-Lite 30 LI Plus under 3 in of 6 pcf blanket, rising
  18 in.** With the door in the 28 in front wall the dome stands as arches spanning the side walls
  (domes-over-doors.md §D4). HarbisonWalker's limit on a ring's thickness for its rise, applied to
  those slices, sets both numbers: a 3 in shell passes at no rise up to the corners' 33.1 in, a
  2½ in shell from 23 in, a 2 in shell from 17 in; the slices stay inside HarbisonWalker's
  1–3 in/ft up to a 24 in rise. 18 in is the least with a margin. It is 3.3 in per foot of the
  66.2 in diagonal, a little over Olsen's 2½–3 in/ft for domes (p.51; 13.8–16.6 in here, where a
  2 in shell fails). **Olsen casts domes 5–6 in thick** ("a 6in. thickness is best", p.59;
  Kanayama 5–6 in, p.187). Over a door in the short wall of this long chamber, that is too thick for
  the slices' rise. A door in a side wall would let the slices span 60 in and take a thicker shell
  (the engine says so), but the door is the author's.
- **The door's arch: a 4½ in brick ring of its own** (`loading.opening.ring`, new). A 2 in ring
  from the dome would be 1.4 times the thinnest semicircle that stands (Heyman's 2). Olsen lays the
  door's brick ring arch first and casts the dome over it (Kanayama Figs 7-17, 7-25; Höhr Figs
  4-135, 4-137). The 4½ in ring is 2.9 times the thinnest. The 10 in jamb holds its least thrust,
  22 lb, 6.3 in from the door's edge, inside its middle third (to 6.7 in). It needs friction 0.22 of
  0.6. Bearing is 12.1 psi at the springing and 5.8 psi at the jamb's toe, shown and not checked.
- **Walls: 3¼ in of Kast-O-Lite cast as one layer, on 4¾ in of 6 pcf blanket** (8 in, as before:
  44 in outside). 3¼ in is the least that keeps the blanket under its 2000 °F rating; at 3 in it
  runs at 2008 °F. **Floor: 2½ in of the castable on 2½ in of K-23**, so the 2,600 lb load sits
  on brick, not on blanket.
- **The DIY mixes don't pass** (castables.md §11a): no service limit and no fired shrinkage are
  sourced, and three of their ingredients are unpriced. They stay in the test kiln.

### Side by side

Firing costs are for the full load (2,624 lb), elements on the whole firing in the target runs
(`simulate --target`). Lining weight is the bricks in the kiln at 9 × 4½ × 2½ in, the castable
placed at 98 lb/ft³ (dried, HWI) and the blanket, each at its library density. The chimney isn't
included.

| | Bricked door | Car | Budget lining | **Castable** |
|---|---|---|---|---|
| Chamber | 45.2 ft³ | 45.2 ft³ | 45.2 ft³ | **55.2 ft³** (the dome's 18 in rise) |
| Roof | 3 in cast sprung arch, 3¾ in rise | same | same | 2 in cast sail dome, 18 in rise |
| Walls | 4½ JM 26, 2½ K-23, 1 in 8 pcf | same | 4½ JM 26, 3½ in 6 pcf | 3¼ Kast-O-Lite, 4¾ in 6 pcf |
| Lining weight | 2,962 lb | 2,950 lb | 2,520 lb | 3,012 lb (2,636 lb of it castable) |
| Heat loss at cone 10 / hottest face | 14.31 kW / 281 °F | same | 14.33 kW / 281 °F | **20.29 kW / 329 °F** |
| Burner input (Olsen Rule 1) | 452,083 BTU/hr, 8 × B3 at 1.0 psi | same | same | 552,249, 8 × B3 at 1.6 psi |
| Cylinders at 20 °F (11) | full, ½, ¼ all pass | same | same | full passes; **¼ full doesn't** (476,300) |
| Priced materials | $11,606 | $11,566 + the car | $9,859 | **$10,088** |
| Errors / warnings | 0 / 1 | 0 / 1 | 0 / 1 | 0 / 3 (cylinders ¼ full, dome T/S, budget) |
| Plain firing, elements to 1650 °F | 65 h 12 min, $150.03 | same | 59 h 13 min, $140.95 | **not finished in the 96 h the simulation runs**: 999 °C at 96 h, $143.57 so far |
| 4 h target | $124.65, 1,002,000 BTU/hr | $124.65 | $124.59 | **not met** on 11 cylinders at 20 °F (needs 1,299,000; 4.1 h on their 1,243,000), $166.83; 12 full cylinders would do |
| 6 h | $128.37, 574,000 | $128.37 | $127.96 | $168.76, 760,000 (8 × B4 at 1.1 psi) |
| 8 h (the castable's `target_time`) | $131.49, 406,000 | $131.49 | $130.70 | $170.14, 535,000 (8 × B3 at 1.5 psi) |
| 12 h | $138.61, 266,000 | $138.61 | $135.94 | $176.18, 349,000 (8 × B3 at 17 in. w.c.) |
| Fastest heating, 4 / 8 / 12 h | 725 / 350 / 247 °C/h | same | 725 / 349 / 243 | 738 / 367 / 254 °C/h |
| Dome or arch steel | arch frame: L4×4×5/16 posts and buttresses, ¼ × 2 in flat bar, two ½-13 rods; 231 lb/ft | same | same | dome frame: L4×4×5/16 along the side walls and round the springline (43 ft), two ½-13 rods across the door's head and the back at 741 lb hot; 234 lb/ft hot (59 cold) on the side walls, the angle at 14,076 of 29,989 lb·in allowed at 216 °F (AISC F10) |

**The budget isn't met.** The castable version comes to **$10,088**. That is $1,500 under the
bricked door and $230 over the budget lining, and still twice the $5,000. What drives it:

- **Kast-O-Lite, $5,530**: 48 bags for 26.9 ft³ placed. At $115.21 a bag (Refractory West
  [S51]) and 92 lb/ft³ to place, a cubic foot costs $193. A cubic foot of JM 26 brick costs $122
  and K-23 $106. **Cast lining costs more than brick per cubic foot**, so casting the walls saves
  nothing. It is cheaper here only because the cast wall is thinner (3¼ in against 4½ + 2½ in of
  brick) and blanket is cheap ($1.40 per ft²·in for 6 pcf). The same castable is $98.18 a bag at
  L&M ([S52], combustion-and-masonry.md §9), which would take about $820 off. The library prices
  the higher listing.
- **Fixed by the author's choices, $3,366**: eight B3 burners ($1,960), and the chimney's 258 hard
  bricks ($1,406, 29 more than the brick kiln's because the dome is taller). These alone are 67 %
  of $5,000.
- The rest: blanket $630, K-23 under the floor $562.
- **Unpriced** (not in the total): Kanthal APM wire (16 lb); the steel (43 ft L4×4×5/16, 25 ft
  ¼ × 2 in flat bar, 11 ft ½-13 rod); the door's 4½ in brick ring (its arch bricks aren't counted:
  the bill counts the wall's own layers); the door plug (the bill counts it as the wall's castable,
  about 1.8 ft³; a plug of IFB, or a cast block, isn't priced); the burners' rack; cylinders;
  shelves; the dome's form (dirt, sand and plastic, Olsen pp.58–59, 186–187).

**The cost per firing is higher**, $167–176 against $125–139. The castable lining stores and
loses more heat: 20.3 kW lost at the top against 14.3, and about 2,600 lb of castable at 98 lb/ft³
to heat against IFB at 32–50. **Elements alone can't bring it to the 1650 °F hand-over in a
working time.** The plain firing is still short of the top at the 96 h the simulation allows. So
the castable version only makes sense fired to a target, with the burners on from the start.

**Dry-out.** HWI Schedule 4 for Kast-O-Lite 30 LI Plus (castables.md §14.2) is for a single
castable layer, one-sided, under 12 in. Cure at least 24 h at 70–100 °F. Heat at 100 °F/h to
1200 °F, measured at the gas ½ in off the face, and hold 1 h per inch: 3¼ h for the walls, the
thickest layer. Then cool, or heat on at 100 °F/h. That is about 14½ h from 70 °F to the end of
the hold. Every castable here is one layer, but each sits on blanket or K-23. HWI says to ask
about "multi-layer linings", and doesn't say whether a castable on blanket counts as one.
**Confirm with HWI.** The engine still prints its generic castable note (Mizzou's 75 °F/h); this
schedule is from the research notes, not the engine. Water leaves through the cold face, so the
blanket should let it out (IC-1). Keep the steel shell's weep holes open.

**Open items for the author (castable version):**

1. **The budget.** It can't be met with this castable at the sourced prices, and the brick-wall
   versions don't meet it either. Choose what gives: the burners (eight B3s, $1,960), a cheaper
   seller of the same castable (L&M, $98.18), or a smaller kiln. The engine won't resize the
   kiln on its own.
2. **A 2 in dome** against Olsen's 5–6 in. It passes the engine's checks only that thin, because
   the door is in the short wall. Accept it, move the door to a side wall (which allows a thicker
   shell), or build a sprung arch, as the brick versions have.
3. **The plain firing doesn't finish.** Fire to a target (8 h is in the design) or hand over
   earlier.
4. **Cylinders:** 11 meet the 552,000 BTU/hr full, but not ¼ full at 20 °F. 13 would, or fire
   them fuller. The 4 h target needs 12 full.
5. **The door's brick ring and plug:** what they're made of and how they're priced (above).
6. **Dry-out of a castable on blanket:** HWI to confirm (above).
7. As for the brick versions: the burners' rack, the setting's layers and posts.

## Not sourced, left out

Kanthal APM wire price; steel prices; the car's wheels, rails and seal (no source sizes them);
the burners' removable welded-steel rack; the shelf posts' size and mass; propane
cylinder prices;
an allowable bearing stress for the refractory (shown, not checked); HWI's own c_p.
