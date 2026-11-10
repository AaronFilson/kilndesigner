# Olsen's kits: the chamber round the stacking space

Research A6 of the round of 2026-11-10 (`docs/planning/11-10-26.md`), for ADR 0017 decision 14:
"Olsen's kits are sized as stacking space (pp.169–170, p.173). Their design files are to be
resized from it; today they take that volume as the whole chamber." What chamber each kit needs
round its printed stacking volume, and how the book relates stacking space to chamber.

Olsen is *The Kiln Book*, 4th ed., cited by its printed page. The book's facts are taken from
`kiln-reference.md` (§6, §7 "Burner ports and combustion space", §11; read from the scan, marked
**Read** there) and `olsen-kilns.md` (§2, §3); the burner's size from `kiln-hardware.md` §1.2.
Marks as in the other research files: **Read** (on the page), **Derived** (arithmetic, shown),
"from memory". Worked 2026-11-10; the arithmetic is `scratch/research-a/kits.py` (git-ignored).

## Short answer

| Kit (stacking, printed) | Stacking cube (Derived) | Chamber it needs, 4½ in all round (Derived) | to the springline | with the arch | Chamber ÷ stacking |
|---|---|---|---|---|---|
| Olsen 16 (16 ft³, p.173) | 25.9 × 25.9 × 41.2 in, in a chamber 25 % taller than wide (p.170) | 34.9 in square, springline 43.7 in | 30.8 ft³ | 32.9 ft³ | 1.9–2.1 |
| Olsen 24 (24 ft³, p.174) | 34.6 in cube | 43.6 in square, springline 37.1 in | 40.9 ft³ | 44.9 ft³ | 1.7–1.9 |
| Olsen 36 (model name only, p.170, p.182) | 39.6 in cube | 48.6 in square, springline 42.1 in | 57.6 ft³ | 63.2 ft³ | 1.6–1.8 |
| Olsen 50 car kiln (50 ft³, p.174) | 44.2 in cube | 53.2 in square, springline 46.7 in | 76.5 ft³ | 83.9 ft³ | 1.5–1.7 |
| Olsen 100 (100 ft³, p.174) | 55.7 in cube | 64.7 in square, springline 58.2 in | 141 ft³ | 154 ft³ | 1.4–1.5 |

With 6 in of combustion space (the book's figure for a 4 in tip, p.171; the band's other end, since
the kits' MR-100 head size isn't found) each chamber is 3 in wider and deeper: 16 → 36.9 ft³ to the
springline, 24 → 46.7, 36 → 65.0, 50 → 85.4, 100 → 154 ft³ (Derived).

**How the book relates them** (Read, the pages below): it sizes a kiln by its stacking space, the
volume the shelves and ware fill, and builds the chamber round it: a combustion space of at least
4½ in between setting and wall for 2½–3 in burner tips (6 in for a 4 in tip, up to 9 in for
tempered-air blocks), at least 2½ in under the setter shelf, a circulation space behind, and, in an
updraft, the arch on top of the cube. The four kilns that print both figures run 1.15–1.9 times
their stacking space (§3).

**For the design files** (B6, the engine's): the kits' chambers today are cubes (or the 16's
1.25 × box) of the printed volume, to the springline, with no combustion space round the setting
(the dataset's notes say so). By the book's own clearances they are 1.4–2.3 times bigger. The
lining, door and frame of each kit aren't printed, so the resize is of the chamber only.

## 1. What the book says (Read; `kiln-reference.md` §6, §7, §11)

- **The kits are sized in stacking space.** "Olsen Kiln Kits, started 1973 … patented designs of 12
  to 120 cu ft (0.34 to 3.4 m³) of stacking space" (pp.169–170). The exit-flue starting sizes are
  given per ft³ of stacking: 16 → 40½ in², 24 → 45 in², 50 → 90 in², 100 → 120–140 in² (p.173–174).
  The small cube kiln of Fig 6-63 is "a 2, 3 or 4cu. … cube (in terms of the amount of stacking
  space)" (p.171; read as a 2, 3 or 4 ft cube, `kiln-reference.md` §11, Flagged there).
- **The shape: a cube.** "A cube is the best all-round chamber shape for a kiln (i.e. height equals
  width) ... the height of the kiln can be up to 25% greater than the width without incurring
  significant risk that it will fire unevenly. An Olsen 16 kiln kit has a 25% height increase over
  the width deviation and, as the picture illustrates, fires quite evenly (Fig. 6-59)" (p.170, read
  on the page image, 2026-11-10): the 25 % is the kiln's, so the 16's chamber is taken 1.25 times
  as tall to the springline as it is wide. "For an updraft put the arch on top of the cube (the
  most stacking space; the arch volume collects the flue gas)" (p.74).
- **The combustion space round the setting.** At least 4½ in (11.5 cm) between ware and wall for
  floor burners or 2½–3 in burner tips, usually the length of the wall (p.76, p.171); a 4 in tip
  needs 6 in; tempered-air burner blocks up to 9 in (p.171). Firing from the side or back may need
  7–9 in: 4½ in is enough with low-pressure venturi burners, high-pressure ones may need more
  (p.151). Too small a space can harm the ware (p.171). Fig 6-63's plans mark "4½" Around" (p.172).
- **Under and behind the setting.** "At least 2½ in (6.3 cm) between the setter shelf and the
  floor" (p.172). A back-wall circulation space of 2–4½ in for side-channel burners (p.171,
  Fig 6-63); "leave space behind and in front of the shelves for circulation" (p.171).
- **The arch.** The small cube kiln takes "a 1½in. (4cm)-rise number 1 arch" (p.171), read as 1½ in
  of rise per foot of span, the No. 1 featheredge (`kiln-reference.md` §11).
- **The burners.** The kits use Gas Appliance MR-750 and MR-100 burners (p.222); the 24 has eight
  perimeter burners and two bottom burners (p.174). Perimeter burners at least 6 in and at most
  12 in from the corners, the rest 9–12 in apart (p.171). The MR-750's head is 2.5 in across (a
  retailer's figure, `kiln-hardware.md` §1.2), so the 4½ in rule applies to it; the MR-100's head
  size is not found ("larger", "slightly larger").

## 2. The chamber each kit needs (Derived)

The method, each step a printed rule above:
- stacking: a cube of the printed volume, side s = V^(1/3) (p.170); for the 16, the stacking that
  fills a chamber 1.25 times as tall as wide (p.170), s × s × h with s + 2c the chamber's width and
  h + 2½ in its springline, solved for s·s·h = 16 ft³;
- plan: s + 2 × 4½ in each way (p.171, Fig 6-63), the band's other end s + 2 × 6 in (p.171);
- springline: 2½ in under the setter shelf (p.172) plus the stacking's height, the arch on top
  (p.74);
- the arch: a circular No. 1 arch rising 1½ in a foot of the chamber's width (p.171), its segment's
  volume added above the springline.

| Kit | s (in) | Combustion space | Width = depth (in) | Springline (in) | Arch rise (in) | Box (ft³) | + arch (ft³) | Total ÷ stacking |
|---|---|---|---|---|---|---|---|---|
| 12 (the family's smallest) | 27.5 | 4½ / 6 in | 36.5 / 39.5 | 30.0 | 4.6 / 4.9 | 23.1 / 27.0 | 25.4 / 30.0 | 2.1 / 2.5 |
| 16, the chamber 25 % taller (p.170) | 25.9 × 41.2 / 25.1 × 43.9 | 4½ / 6 in | 34.9 / 37.1 | 43.7 / 46.4 | 4.4 / 4.6 | 30.8 / 36.9 | 32.9 / 39.4 | 2.1 / 2.5 |
| 16, were it a cube | 30.2 | 4½ / 6 in | 39.2 / 42.2 | 32.7 | 4.9 / 5.3 | 29.2 / 33.8 | 32.1 / 37.5 | 2.0 / 2.3 |
| 24 | 34.6 | 4½ / 6 in | 43.6 / 46.6 | 37.1 | 5.5 / 5.8 | 40.9 / 46.7 | 44.9 / 51.6 | 1.9 / 2.2 |
| 36 | 39.6 | 4½ / 6 in | 48.6 / 51.6 | 42.1 | 6.1 / 6.5 | 57.6 / 65.0 | 63.2 / 71.7 | 1.8 / 2.0 |
| 50 | 44.2 | 4½ / 6 in | 53.2 / 56.2 | 46.7 | 6.7 / 7.0 | 76.5 / 85.4 | 83.9 / 94.1 | 1.7 / 1.9 |
| 100 | 55.7 | 4½ / 6 in | 64.7 / 67.7 | 58.2 | 8.1 / 8.5 | 141.0 / 154.4 | 154.2 / 169.5 | 1.5 / 1.7 |
| 120 (the largest) | 59.2 | 4½ / 6 in | 68.2 / 71.2 | 61.7 | 8.5 / 8.9 | 166.0 / 180.9 | 181.5 / 198.5 | 1.5 / 1.7 |

Laid in brick the plan rounds to the module (p.142, p.81: "keep to brick-module dimensions even if
they look big"): the 24's 43.6 in to 45 in (five stretchers), for example. That rounding, the
door's construction and any space over the top shelf aren't printed; they are the design file's
choices, to be stated as assumed.

## 3. Kilns that print both the stacking and the chamber

| Kiln | Stacking (printed) | Chamber (printed) | Ratio (Derived) | What the clearance is |
|---|---|---|---|---|
| Kähler salt kiln, Næstved (p.136, Figs 5-17, 5-18) | "16cu. ft (0.45cu. m) stacking space" | 30 in wall to wall, 36 in deep, 48 in to the arch line | 30 ft³ ÷ 16 = 1.9 (to the arch line) | 24 in between the dashed stacking lines both ways: 3 in a side across, 6 in at each end; 24 × 24 × 48 in is exactly 16 ft³, so the stacking runs to the arch line (Derived) |
| Blakebrough's envelope kiln, Hobart (p.148) | "A 40 cu. ft (1.13cu. m) stacking" kiln | 42 × 54 × about 52 in, "started from a cube, adjusted for shelves and burner channels" | 68 ÷ 40 = 1.7 | two 24 × 24 in shelves with a 9 in burner channel along each side (42 = 24 + 2 × 9); the shelves' footprint to 52 in is 34.7 ft³, short of the 40 printed (Derived; which height the 40 takes isn't said) |
| Gulgong racer (p.119, p.121) | interior stacking chamber 5 × 5 × 3½ ft (caption 4-126) = 87.5 ft³ | 106 cu ft | 1.21 | a groundhog-style cross-draft; the firebox isn't counted |
| Kaneko's car kiln (p.170–171) | 500 cu ft (the text) | 8 ft tall, 9 ft deep, 8 ft wide = 576 ft³ | 1.15 | `olsen-kilns.md` reads the 500 as probably stacking space; 32 burners, 9 in combustion width (p.172) |

The updraft test kilns behind Design Principle 1 (p.74) give only their stacking (2 × 3 × 5 ft-plus,
2 × 3 × 4, 3 × 3 × 5, 4 × 4 × 5 ft). The salt rule, 1 lb per ft³ of stacking space (p.127), and
the exit-flue rule (p.173–174) also count stacking, not chamber.

So the book's own kilns carry their combustion space outside the stacking volume, and the smaller
the kiln, the larger the ratio: 1.9 for a 16 ft³ salt kiln, 1.7 for a 40 ft³ fibre kiln, 1.15–1.2
for 90–500 ft³. The kits' derived ratios (§2) fall in the same run.

## 4. What stays open

- **The 16's 25 %** (p.170): settled on the page image, the kiln's height; its chamber is taken to
  the springline 1.25 times its width. The cube reading is kept in §2 for comparison (within 2 ft³).
- **The combustion space**: 4½ in fits the MR-750's 2.5 in head (p.171); the MR-100's head size isn't
  found, so 4½–6 in is the band.
- **Above the setting**: whether the stacking runs to the springline (as the Kähler kiln's does to
  its arch line) or stops below it isn't printed for the kits; §2 takes it to the springline,
  with the arch's volume above.
- **The kits' walls, door, arch thickness and frame** aren't printed (`olsen-kilns.md` §2).
- Which burner each kit uses (MR-750 or MR-100) is the engine's to size (ADR 0017 decision 13).
