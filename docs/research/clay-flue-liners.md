# Clay flue liners: what a chimney "made from chimney flues" is, for the heat model

For step 8 of B4 (`docs/planning/11-10-26.md` §B): Olsen's fast-fire chimney is "made from chimney
flues" (Fig 5-37, as `11-09-26.md` §I and the round doc read it), clay flue liners, where the engine
builds every chimney of 4½ in of hard firebrick (`hardware.CHIMNEY_BRICK`), which took 27 % of the
fast-fire's heat in p.309's log. What open sources give for a clay flue liner's wall, and what the
heat model takes. Read 2026-11-10. Marks as the other research files: **Read**, **Snippet**,
**Derived** (working shown).

## Short answer

| Quantity | Value | Source | Mark |
|---|---|---|---|
| How liners are named | "Clay flue liners are designated by their nominal exterior dimensions" | [L1] | Read |
| Standard 8½ × 8½ in, 2 ft | 36 lb; effective net area 49 in² | [L1] | Read |
| Standard 8½ × 13 in, 2 ft | 50 lb; 76 in² | [L1] | Read |
| Standard 13 × 13 in, 2 ft | 66 lb; 127 in² | [L1] | Read |
| Modular 8 × 8 in, 2 ft | 30 lb; 42 in² | [L1] | Read |
| Wall thickness | ASTM C315's tables not read (the standard is sold; the free previews fetched held no tables); search snippets of its round-liner table give ⅝–¾ in nominal walls, ⅛ in tolerance | [L2] | Snippet |
| The body | fire clay or shale, fired (ASTM C315's scope, as snippets give it); no liner's own k or c_p found | [L2] | Snippet |
| The wall the heat model takes | a fireclay body (the library's Smithfield fireclay brick: its k(T), c_p(T), 2,086 kg/m³) 0.63 in thick | Derived below | Derived |

## Sources

- [L1] Rumford Fireplaces, "Flues" (store page), <https://rumford.com/store/flues.html>, Read
  2026-11-10 through the fetch tool: the modular and standard two-foot flues' nominal sizes,
  effective net areas, weights, pallet counts and prices (8½ × 8½ in standard: 36 lb, $20.40).
  The page gives no wall thickness, inside dimension, material or standard.
- [L2] ASTM C315, *Standard Specification for Clay Flue Liners and Chimney Pots* (C315-07, reapproved
  2021), <https://store.astm.org/c0315-07r21.html>: not read (sold). Search snippets of its tables
  (Snippet only) give a round 8 in liner a ¾ in nominal wall and the wall's tolerance ⅛ in.

## The wall, Derived

The weight per length of Rumford's standard 8½ × 8½ in flue is 36 lb ÷ 2 ft = 18 lb/ft = 26.8 kg/m.
A fireclay body at the library's Smithfield density, 2,086 kg/m³ (`masonry-materials.md` §2.2, the
maker's bulk density), has a wall section of 26.8 ÷ 2,086 = 0.01284 m² = 19.9 in². A square tube
8½ in outside with a wall t: 8.5² − (8.5 − 2t)² = 19.9, so t = (8.5 − √52.35) ÷ 2 = 0.63 in, within
the ⅝–¾ in the snippets give. The 13 × 13 in check: 66 lb ÷ 2 ft = 49.1 kg/m, 0.02355 m² = 36.5 in²
at the same density, t = (13 − √(169 − 36.5)) ÷ 2 = 0.74 in: the larger liner the thicker, as the
snippets' tables run.

The body's k and c_p: no liner's own were found; a fired fireclay body's (`masonry-materials.md`
§4a.3: fireclay 1.0–1.7 W/(m·K) from 200 to 1300 °C, Norton's three rows; Smithfield's own sheet
in the library) is the nearest sourced, so the library's Smithfield brick stands for it, said in the
working. Its mass per area, 2,086 × 0.016 m = 33 kg/m², is an eighth of the engine's 4½ in of
KX-99 (about 262 kg/m²).

## What stays open

- Whether Olsen's fast-fire chimney stands free or is cased in brick, and whether its 9 × 9 in
  inside (the design file's) is a liner's: a 13 × 13 in standard liner is about 11½ in inside, an
  8½ × 8½ in one about 7¼ in (Derived from the 0.63–0.74 in walls). The heat model keeps the design
  file's 9 × 9 in inside and takes the liner standing in the room's still air.
- ASTM C315's own tables (the wall thickness by size) and a liner's measured k: not read.
