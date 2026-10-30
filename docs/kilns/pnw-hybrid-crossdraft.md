# The PNW hybrid cross-draft: results

_Rebuilt 2026-10-30 from `examples/pnw-hybrid-crossdraft*.yaml` on the current engine (this
replaces the 2026-10-21 first estimate, whose burner, element, chimney and supply figures are
stale). Rebuild with `uv run kilndesigner build examples/pnw-hybrid-crossdraft.yaml --out out/pnw`
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

## What the engine finds now

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

## The door

The door variant's door is the **whole front wall**, bricked up dry for each firing. No document
from the author gives a door size, so no `loading.opening` is set and none is invented. To lay
out a door in part of the wall the engine needs its width, height and sill (and an arched head
or a lintel, which it then checks: `frame.door-arch`, `frame.door-jamb`). Note the burners also
fire through the front wall in this variant, so their ports sit in the bricked door; the car
variant moves them to the right wall.

## Open, needs the author

1. **The door's size**, if not the whole front wall, and whether the burners stay in the door
   wall.
2. **Propane:** a 500 gal tank, or more cylinders, or firing only on warmer days. Four cylinders
   meet the burners only full and above about 20 °F.
3. **Budget:** $8,500–$10,178 priced against $5,000, before steel, wire, car hardware, fittings
   and shipping. JM 26 (655 bricks, $4,696) is most of it.
4. **Burner count** (two B5s chosen; Olsen's builds use more).
5. **Ware and shelves** (`firing.ware`) for a realistic firing time and cost.
6. **Switch-over:** 1650 °F as set, or about 1200 °F for the cheapest firing.

## Not sourced, left out

Kanthal APM wire price; steel prices; the car's wheels, rails and seal (no source sizes them);
an allowable bearing stress for the refractory (shown, not checked); HWI's own c_p.
