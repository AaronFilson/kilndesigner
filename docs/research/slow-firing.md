# Slow firings: what the sources say

For plan item 7 of [10-30-26.md](../planning/10-30-26.md): kilns designed for very slow firings,
for ware that needs them. The author's rule (30 October 2026): firing speed is the user's choice;
no ware-rate warnings; report the numbers per source as options and warn only on physical faults.
Olsen page numbers are the book's (*The Kiln Book*, 4th ed.); the rows marked "Checked on the page
image" were read on the scan on 2026-10-31, the rest come from `olsen-kilns.md` and
`kiln-reference.md`, where each was read before.

## 1. Slow firings reported

| Kiln | Fuel | Time | Fuel used | Notes | Source |
|---|---|---|---|---|---|
| Kei Fujiwara's Bizen kiln, climbing cross-draft | wood | Seven days: 2½ days stoking the fire-mouth air duct (preheating), 4 days the fire mouth, 12 h the chambers; the top at 6½ days, then a soaking fire | not given | Cooled with every spy hole and damper closed, very slowly, over about three days (p.105) | Olsen pp.99, 103–105; checked on the page image (p.99) |
| Bizen design aims | — | "maximum efficiency of wood consumption over a seven-day firing period with minimum stoking and draft"; "minimum loss of heat during gradual temperature increase" | — | Bizen clays "bloat, blister, crack and sag if fired too rapidly"; losses about 50 % with the artist's clay, 20 % with commercial clay | Olsen p.99; checked on the page image |
| Bizen walls | — | — | — | 10–13 in, tightly built, no vapour holes, no expansion joints: the long, slow firing and cooling take the movement | Olsen p.100 |
| La Borne tunnel kilns, 1766–2825 ft³ | wood | 2½–3 days' preheating, up to four days of *petit feu*, about one day of *grand feu*: about 7–8 days (derived) | not given | Light salting near the end | Olsen pp.110–111 |
| Tamba tube kilns, 120–150 ft | wood | Firebox about 36 h, to about 1000 °C at the first stoke holes; side stoking 14 (?) to 18 h | about 200 bundles (15 × 15 × 30 in) | | Olsen pp.86–87 |
| Suzuki cooperative climbing kiln, Kyoto | wood bundles | About 56 h to cone 8–9; the firebox 15 h to 1000 °C | about 75 bundles a side, chambers 1–3 | | Olsen p.93 |
| Olsen's Hollyweird tube | wood | A "normal" firing 60 h; at cone 11-plus 35–40 h (front), 10–15 h (back) | not given | | Olsen p.117 |
| Mr Kato's coal downdraft, about 250 ft³ | coal | Over 50 h to 2372 °F; cooled three days or more | not given | Slow because of "the very thick walls and only two fireboxes" | Olsen p.131 |
| Jun Kaneko's car kiln, 8 × 9 × 8 ft | gas, 32 atmospheric burners | "fired extremely slowly, allowing for a long soaking rise in temperature over several days, depending upon the size of the pieces being fired" | not given | Large updrafts with floor burners use "long protracted soaking periods" for even temperature (p.171) | Olsen pp.171–172; checked on the page image |
| Tobe climbing kiln, largest chamber 25 × 10 × 10 ft | wood | not given | "40 tons of wood to fire" (the chamber or the kiln: unclear) | | Olsen p.90 |
| Anagamas | wood | 4–5 days where given | 14 cords a firing (Montevallo); 10 cords over 4 days (Buck Creek); about 6 cords over 5 days (forum) | 1 cord about 128 ft³, 2,000–3,000 lb | `combustion-and-masonry.md` §5.3 [S49] |
| A small conventional wood kiln | wood | 24–48 h | "a cord or more" | A patent's background | `combustion-and-masonry.md` §5.3 [S48] |

None of these gives a heating rate in °C/h, a soak temperature, or wood per hour, so the engine
takes no schedule from them. They are listed beside a slow firing as options to compare
(`slow.SOURCED`).

## 2. What the engine does with them

- **The longest firing it will simulate** is the longest sourced: Bizen's seven days and about
  three days' cooling, 240 h (`simulation.LONGEST_FIRING_H`). A schedule whose ramps and holds
  take longer is refused with that reason; so is a target firing time past it.
- **A long schedule runs to its end.** The simulation used to stop every firing at 96 h; it now
  allows the schedule's own paced time (ramps at their rates, and holds) plus 96 h of full heat.
- **A slow firing** (`slow.slow_firing`, `kilndesigner slow DESIGN 5day --soak 12h`): the design's
  own elements and burners fire a constant rise from the room to the top in the chosen time less
  the soak, then hold the soak. Reported: the heat put in and where it goes (walls, ware, the
  shell's loss), fuel or electricity, cost, beside the design's quickest firing. The constant rise
  is the engine's simplest schedule, not a source's; give `firing.schedule` for a shaped one.
- **Mass and insulation.** The simulation shows the trade-off rather than a rule: in a long firing
  the shell's loss grows with the time while the walls' store does not (for example the gas
  cross-draft example: 4 kWh lost from the shell in its 4 h firing, 847 kWh in 168 h). Olsen's
  Bizen aim, "minimum loss of heat during gradual temperature increase", is quoted with it.
- **Warnings**: only a physical fault, the kiln's heat not reaching the top at all. Falling behind
  the asked pace is reported as information (the firing takes longer).
- **Wood, coal and oil kilns** aren't simulated (milestone M7, no wood combustion source), so for
  them the slow firing gives the sources' firings only. Wood per firing therefore stays as reported
  above, per source; no engine figure.

## 3. Not found

- A heating or soaking rate for any of these firings, or a temperature for Bizen's preheat.
- Wood per hour or per firing for the Bizen and La Borne kilns.
- Whether Kaneko's "several days" includes cooling.
