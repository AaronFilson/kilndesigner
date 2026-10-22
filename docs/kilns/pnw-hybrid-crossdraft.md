# The PNW hybrid cross-draft: first results

_Generated 2026-10-21 from `examples/pnw-hybrid-crossdraft*.yaml` with Kilndesigner 0.1.0. Rebuild
with `uv run kilndesigner build examples/pnw-hybrid-crossdraft.yaml --out out/pnw` for the full
plans (PDF, DXF, 3D model). Every number below has its working and source in the plans._

## The design as entered

- Cross-draft, cone 10, burners firing through the front wall, flue at the back.
- Chamber 28 in wide × 60 in long × 44 in to the springline, under a 60° arch with a 3¾ in
  rise: **45 ft³ inside** by Ward's method. Stacking space will be less than this.
- Walls 8 in: 4½ in JM 26 IFB, 2½ in K-23 IFB, 1 in fibre blanket. The outside width is
  **44 in**, the site limit, before any steel frame.
- The arch is cast: 3 in Kast-O-Lite 30 LI Plus under 2 in of blanket.
- 240 V, 60 A breaker (48 A continuous, **11.5 kW**) on Kanthal APM elements in the left wall,
  off above 1650 °F; propane from four 100 lb cylinders; coldest firing day 20 °F.

## What the engine found

| | Bricked door | Car | Budget lining, slow firing, 500 gal tank |
|---|---|---|---|
| Heat loss held at cone 10 | 14.3 kW | 14.3 kW | 14.4 kW |
| Hottest outside face | 279 °F (the arch) | 279 °F | 279 °F |
| Burner input | 723,000 BTU/hr (6–7 h firing) | same | 452,000 BTU/hr (14–18 h) |
| Propane supply keeps up at 20 °F | **no**, even with full cylinders | **no** | yes |
| Priced materials | **$9,476** | $9,476 + the car's hardware | **$7,392** |
| Errors / warnings | 1 / 5 | 1 / 5 | 0 / 5 |

1. **Four 100 lb cylinders can't fire this kiln at 20 °F.** A fast firing needs 723,000 BTU/hr;
   full cylinders give about 668,000, half-full 376,000, and the conservative case (¼ full,
   keeping 10 psi) 173,000. Even a slow firing (452,000) only works while they're nearly full.
   A 500 gal tank keeps up with a slow firing at 20 °F; a fast firing at 20 °F needs about
   1000 gal. Ward's own guidance for a kiln this size is a 500 gal tank.
2. **Electricity is the cheaper heat at every temperature.** At $0.12/kWh and $3.50/gal, a kWh
   from propane that stays in the kiln costs $0.15 at 300 °F and $0.38 at cone 10, because the
   flue carries more heat away as the kiln gets hotter (Cantera, checked against published
   flame temperature and heating values). So the elements should run as long as they can keep
   the schedule, with the burners added alongside rather than instead of them.
3. **The switch-over at 1650 °F is set by reduction, not cost.** Reduction starts about 900 °C
   (1652 °F) and attacks the elements' protective oxide. The elements could hold the kiln up to
   about 2050 °F against steady loss, but at 1650 °F only about 3.3 kW is left for heating ware.
4. **The budget is the hard constraint.** About 1,000 insulating bricks are most of the cost.
   Swapping the K-23 backup and 1 in blanket for 3½ in of 6 pcf blanket saves about $2,100 with
   almost no change in heat loss (14.35 kW against 14.26 kW), but it's still over $5,000. The
   remaining levers are a smaller chamber, used or seconds brick, or a cheaper hot-face brick.
5. **Elements:** 8 elements of 10 AWG (2.59 mm) APM in the left wall, in two strings of four,
   28⅜ ft each, at 13.2 W/in². That's the fewest elements that work, each with the thickest wire
   whose coil fits its groove. Kanthal recommends wire of 3 mm or more for the longest life in
   grooves; 12 elements would take 8 AWG (3.26 mm), at the cost of four more grooves and about
   2½ times the wire (14 lb against 6).
6. **Chimney:** about 14 ft above the chamber floor (3 × 47¾ in + ⅓ × 77 in), an exit flue of
   about 113 in², and 0.15–0.19 in. w.c. of draft at 20 °F.

## Not done yet

- The skewbacks and fill are drawn and counted (about 22 bricks a side, by volume), but the
  steel frame and the arch's thrust are not designed or priced.
- Fuel and electricity per firing need the firing simulation (milestone M6).
- The car's hardware has no sourced prices; set `loading.car_hardware_cost` to compare it.
- Kanthal APM wire has no sourced price.

## Decisions for you

1. Is a 500 gal tank possible on the site? If not, how many cylinders, or is firing only above
   about 40 °F acceptable?
2. Which way on the budget: a smaller chamber, cheaper brick, or a higher budget?
3. Elements: 8 of 10 AWG, or 12 of 8 AWG for longer element life?
4. Fast (6–7 h) or slow (14–18 h) firings? This sets the burners and the propane supply.
