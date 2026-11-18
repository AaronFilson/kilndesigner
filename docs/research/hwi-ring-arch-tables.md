# HarbisonWalker ring and arch combination tables (IR-25 to IR-62), checked against Olsen and the engine

Source: [HW05] HarbisonWalker, *Handbook of Refractory Practice* (2005), "Brick Combinations Required for
Rings" (IR-25 to IR-50, PDF 149–174) and "Brick Combinations Required for Arches" (IR-52 to IR-62,
PDF 175–185). The data are in `hwi-ring-arch-tables.yaml`; this note holds the reading and the
comparisons. Second reading, 2026-11-17, the first pass being `hwi-handbook.md` §3.6 and §4.4.

How it was read. The pages have a native text layer, but its order is scrambled. Every table was rebuilt
from word positions (PyMuPDF), then checked three ways. (1) On every row the counts sum to the printed
total. (2) Diameters and spans run in order. (3) On every arch row the rise and inside radius were
recomputed from the circle geometry (UR-28). Each table page was then rendered (half-page crops, 125–200
dpi) and looked at. The rows that failed a check, and the rows where the engine differs, were read cell by
cell on the image. **Verified** below means that: the image agrees with the extraction on the layout, on
every flagged row and on the rows listed here. I did not re-key every cell by eye. **Read** is the text
layer only, **Derived** is our arithmetic. The book and its images are not in the repo.

**Checked by the coordinator (2026-11-18).**
- Own script (`scratch/hwi-deep/coord/ringcheck.py`) on this YAML and `rings.ring`. Every row's counts
  sum to its total. The totals are equal in all 485 rows and the splits as in §3.2, row for row.
- The IR-30 total model fits 97 of 97 rows.
- On fresh renders:
  - IR-29 at 5'10" (31 + 52 = 83, against Olsen's transcribed 30 + 53);
  - IR-56's 1'11" radius (printed 2'11") and its 2'6" and 2'7" rises (printed 3 1/32 and 3 5/32);
  - IR-26 at 2'11" (20 + 36) and 7'8" (76 + 51 straights);
  - IR-30 at 2'6" (6 + 8) and 3'11" (2 + 18).

  All as recorded here. The coordinator's additions are marked "coordinator" in §3.2.

Rounding, quoted (IR-25, PDF 149; repeated at IR-52, PDF 175): "In calculating the tables, no allowance
was made for mortar or expansion joints or for size deviations of the brick. Fractional parts equal to or
greater than one tenth of a brick were counted as an entire brick." The tables "may lay up to diameters
which differ slightly from the theoretical diameters", and the count "may be slightly in excess of the
number actually required". Verified.

## What matters for the engine

1. **Every total in every ring table equals `rings.ring`'s total** at every printed diameter up to 12 ft:
   485 rows in five tables, 0 differences (Derived). The 0.1-brick rule in `rings.py` is HW's own rule and
   reproduces the totals everywhere. The split between shapes differs by one brick in 12–29 rows per table
   (below). No rounding rule I tried reproduces all of HW's splits.
2. **A circle-brick table exists** (IR-30, PDF 154: 4½ in lining, 3 in circle brick, 2'0" to 10'0" in 1 in
   steps, 97 rows). `rings.py` has no such method. A simple one fits: total = ⌈π(D+9)/9 − 0.1⌉ in all 97
   rows, and the split between the two neighbouring sizes follows the same mixing algebra as the arch bricks
   (§3.3 below). The split is equal in 75 or 82 of 97 rows (by rule), always within one brick.
3. **Three of HW's tables use shapes that `rings.py` holds only as the A.P. Green extras** (`apg=True`): the
   No. 1-X wedge (2½ in wedge table), the No. 4 arch (3 in arch table, below 18 in) and the No. 1 wedge
   (3 in wedge table). Without them the engine refuses 14 of IR-29's 101 rows (below 18 in) and its splits
   differ in most rows of the two wedge tables. With them, totals match and splits are within one brick.
4. **Olsen's A-4 is HW's IR-26 in all 52 rows. A-5 is IR-29 in 65 of 66 rows.** The one exception is 5'10":
   Olsen 30 No.2 + 53 No.1, HW 31 + 52, both 83. `rings.ring("arch3")` agrees with HW there, so Olsen's row
   is the odd one out (Derived, kiln-reference.md as transcribed). A-6 equals IR-27 except where HW uses the
   No. 1-X wedge. A-7 equals the 3 in wedge table in all 49 rows.
5. **In the straight region HW keeps the gentlest taper's count constant** and adds straights: IR-26 has 76
   No. 1 arch from 4'3" on, IR-29 has 113 No. 1 arch from 8'3" on, IR-27/28 has 227 No. 1-X wedge from
   13'6". `rings.py` mixes straights with the tight shape instead, so it is one brick off in 7 of IR-26's 47
   rows there (75 + 52 against HW's 76 + 51 at 7'8").
6. **Arch tables exist for 4½ in and 9 in arches only (3 in brick), at 1.5, 1.608, 2 and 2.302 in/ft**
   (IR-53 to IR-58). 12, 13½, 15 and 18 in arches are at 1.608 in/ft only (IR-59 to IR-62, not read). No
   2½ in series arch table exists. There is no 2½ in key or circle-brick ring table.
7. **An arch-course method with the ring's own algebra reproduces HW's arch totals in all 535 rows it can
   handle** (3 more sit at the geometric limit of the tightest shape), and its shapes are equal in 430 and
   one brick off in 105 (Derived, §3.7). The arch needs N = θ(r+L)/T and Σnt = θr, θ from span and rise.
8. **Printed misprints, 20 rows**: 19 in IR-56 (9 in arch, 1.608 in/ft) and 1 in IR-54. They are rise or
   inside radius cells, never counts. Details in §3.6. Do not use IR-56's inside radius below 7 ft without
   checking it against r = S.
9. **`kiln-hardware.md` §4.4's eight arch rows equal HW05's** in counts, rise and inside radius (the guide
   and the handbook share these pages).
10. **A.P. Green rounds up from a larger fraction.** In 21 of the compared 3 in wedge, 2½ in wedge and key
    rows, A.P. Green's total is one lower than HW's where the exact count is 0.11–0.19 over a whole brick.
    Its tables are not a second check of HW's rounding (§3.5).

## 1. The tables

All transcribed rows are in the YAML. Rings are cut at 12 ft inside diameter. Status Verified for all.

| Label | PDF | Title | Rows | Range printed | Transcribed |
|---|---|---|---|---|---|
| IR-26 | 150 | 4½ in lining, 2½ in arch brick | 93 | 0'6" to 15'0" | to 12'0" |
| IR-27, IR-28 | 151–152 | 9 in lining, 2½ in wedge brick | 117 | 2'3" to 45'0" | to 12'0" |
| IR-29 | 153 | 4½ in lining, 3 in arch brick | 101 | 0'4½" to 15'0" and beyond | to 12'0" |
| IR-30 | 154 | 4½ in lining, 3 in circle brick | 97 | 2'0" to 10'0" | all |
| IR-34 to IR-36 | 158–160 | 9 in lining, 3 in wedge brick | 109 | 3'0" to 36'6" | to 12'0" |
| IR-36, IR-37 | 160–161 | 9 in lining, 3 in key brick, 9 × 4½ × 3 | 65 | 1'6" to 35'0" | to 12'0" |
| IR-37, IR-38 | 161–162 | 9 in lining, 3 in key brick, 9 × 6 × 3 | 64 | 1'6" to 41'0" | to 12'0" |
| IR-53 | 176 | 4½ in arch, 3 in arch brick, 2 in/ft | 41 | 1'0" to 6'6" | all |
| IR-53 | 176 | same, 1.608 in/ft (60°) | 45 | 1'0" to 6'6" | all |
| IR-54 | 177 | same, 1½ in/ft | 46 | 1'0" to 6'6" | all |
| IR-54 | 177 | same, 2.302 in/ft (2 5/16) | 40 | 1'0" to 6'6" | all |
| IR-55 | 178 | 9 in arch, 3 in wedge brick, 1½ in/ft | 87 | 1'6" to 15'0" | to 12'0" |
| IR-56 | 179 | same, 1.608 in/ft | 90 | 1'6" to 15'0" | to 12'0" |
| IR-57 | 180 | same, 2 in/ft | 96 | 1'10" to 15'0" | to 12'0" |
| IR-58 | 181 | same, 2.302 in/ft | 93 | 2'0" to 15'0" | to 12'0" |

Notes on the layout:
- Each ring page has two blocks side by side. IR-26 has 0'6"–5'10" on the left and 6'0"–15'0" on the
  right. The 9 in tables cross pages: the 2½ in wedge from 2'3" (PDF 151 left) to 6'10", 7'0" to 11'5"
  (PDF 151 right), then PDF 152. The 3 in wedge starts on PDF 158 right (3'0"). The 3 in keys start on
  PDF 160 right (9 × 4½ × 3) and PDF 161 right (9 × 6 × 3), at 1'6", in 2 in steps.
- Step sizes. IR-26: 1 in to 4'4", then 2 in. IR-29: 1 in to 8'3", then 3, 6 and 12 in. IR-30 and the 3 in
  wedge: 1 in. Keys: 2 in. Arch tables: 1 in, then 2, 3 or 6 in at the larger spans.
- IR-30's columns are 24-33-3, 36-45-3, 48-57-3, 60-69-3, 72-81-3 on the left page and 72-81-3, 84-93-3,
  96-105-3, 108-117-3, 120-129-3 on the right. The name is inside diameter, outside diameter, thickness.
- IR-29 has a No. 4 arch column and starts at 0'4½" with 15 No. 4 arch.
- The 9 × 6 × 3 key table (IR-37/38) carries a page note: below 6 ft its No. 3 key "has a very sharp taper";
  a better fit comes from the 9 × 4½ in key combinations (IR-36/37).
- The page numbers run IR-50 (PDF 174) to IR-52 (PDF 175). The PDF has no page labelled IR-51.
- Page footers: PDF 150 = IR-26 … PDF 162 = IR-38; PDF 175 = IR-52; PDF 176 = IR-53 … PDF 185 = IR-62.

Samples (counts as shape × number, total):
- IR-26: 0'6" 19 No.3 = 19. 0'7" 18 No.3 + 3 No.2 = 21. 2'11" 20 No.2 + 36 No.1 = 56. 4'3" 76 No.1 = 76.
  4'4" 76 + 1 straight = 77. 12'0" 76 + 117 = 193.
- IR-30: 2'0" 12 of 24-33 = 12. 2'2" 10 of 24-33 + 3 of 36-45 = 13. 2'6" 6 + 8 = 14. 6'0" 29 of 72-81. 10'0" 45
  of 120-129.
- IR-29: 0'4½" 15 No.4 = 15. 1'6" 29 No.3 = 29. 5'10" 31 No.2 + 52 No.1 = 83. 8'3" 113 No.1 = 113.
- 9 in 2½ in wedge: 2'3" 57 No.2. 4'6" 91 No.1. 4'7" 90 No.1 + 2 No.1-X = 92. 12'0" 15 No.1 + 189 No.1-X = 204.
- IR-53, 1.608 in/ft, 3'0": rise 4 13/16, radius 3'0", 5 No.2 + 10 No.1 = 15.

## 2. Shape sizes

IR-4 (PDF 128), Verified on the image (the first pass also verified it). The ring and arch table
headings print only the brick's bounding size (for example "9 x 4½ x 2½ or 13½ x 4½ x 2½ Inch"); the
tapers come from IR-3 and IR-4. Sizes are length × width × thickness in inches, "(a − b)" a taper.

| Series | Shape | Size | Thin end in `rings.py` |
|---|---|---|---|
| 2½ in | No. 3 / 2 / 1 arch | 9 × 4½ × (2½ − 1 / 1¾ / 2⅛) | 1.0 / 1.75 / 2.125, equal |
| 2½ in | No. 2 / 1 / 1-X wedge | 9 × 4½ × (2½ − 1½ / 1⅞ / 2¼) | 1.5 / 1.875 equal; 1-X = 2.25 is `APG_EXTRA` |
| 2½ in | No. 4 / 3 / 2 / 1 key | 9 × (4½ − 2¼ / 3 / 3½ / 4) × 2½ | 2.25 / 3.0 / 3.5 / 4.0, equal |
| 3 in | No. 4 / 3 / 2 / 1 arch | 9 × 4½ × (3 − 1 / 2 / 2½ / 2¾) | No. 4 = 1.0 is `APG_EXTRA`; 2.0 / 2.5 / 2.75 equal |
| 3 in | No. 3 / 2 / 1 / 1-X wedge | 9 × 4½ × (3 − 2 / 2½ / 2¾ / 2⅞) | 2.0 / 2.5 equal; No. 1 = 2.75 is `APG_EXTRA`; 1-X (2.875) not held |
| 3 in | No. 4 / 3 / 2 / 1 key | 9 × (4½ − 2¼ / 3 / 3½ / 4) × 3 | 4½ in keys: same taper ends as the 2½ in keys |
| 3 in, 6 in wide | No. 3 / 2 / 1 key | 9 × (6 − 3 / 4 13/16 / 5⅜) × 3 | no 6 in key family in `rings.py` |

These agree with `kiln-hardware.md` §5.1 (keys) and with `rings.py`'s `FAMILIES`. The 2½ in series has no
No. 4 arch (and none is in IR-26). The tables' wedge headings also name 9 × 6¾ × 3 and 9 × 9 × 3 wedges:
the same ring counts apply, as the course height is the third dimension.

IR-30's circle brick is 9 × 4½ × 3. The heading prints no taper. The name n-(n+9)-3 is the inside and outside
diameter of the ring it makes, and the totals fit a 9 in outer face (§3.3).

## 3. Comparisons (all Derived)

### 3.1 Olsen's Tables A-4 to A-7 against HW

Olsen as transcribed in `kiln-reference.md` ("Tables A-4 to A-7", p.303–305).

| Olsen | HW table | Rows | Equal | Different | Not in HW |
|---|---|---|---|---|---|
| A-4, 2½ in arch | IR-26 | 52 | 52 | 0 | 0 |
| A-5, 3 in arch (No.3, 2, 1) | IR-29 | 66 | 65 | 1 | 0 |
| A-6, 2½ in wedge | IR-27 | 33 | 25 | 8 | 0 |
| A-7, 3 in wedge | IR-34 to IR-36 | 49 | 49 | 0 | 0 |

The differences:
- **A-5, 5'10"**: Olsen 30 No.2 + 53 No.1 = 83. HW 31 + 52 = 83. HW matches the engine. Worth checking against
  the Olsen page: either a misprint in his table or the transcription.
- **A-6, 2'3", 2'4", 2'5"** (3 rows): Olsen's printed columns are shifted, as the first pass flagged. HW prints
  57 / 55 + 3 / 52 + 7 with totals 57 / 58 / 59 in the right column. So HW settles that Olsen's totals are
  right and his cells are only misplaced.
- **A-6, 5'0", 5'6", 6'0", 6'6", 7'0"** (5 rows): Olsen has 91 No.1 + 7 / 15 / 22 / 30 / 38 straights. HW has
  85 + 13, 81 + 25, 75 + 38, 71 + 50 and 66 + 63 No.1 + No.1-X wedges. The totals are the same (98, 106, 113,
  121, 129). The two differ in which shape finishes the ring, not in size.

The first pass said A-4 equals IR-26 "from 0'6" to 2'3"" and A-5's No.3 column equals IR-29's. Both hold on
all rows now except the one A-5 row above.

### 3.2 `rings.ring` against HW, shape by shape

Run for every diameter transcribed (to 12 ft). "Split" = same total, one brick moved between shapes.

| HW table | Engine series | Rows | Totals equal | Shapes equal | Split off by one |
|---|---|---|---|---|---|
| IR-26 | `arch` | 93 | 93 | 81 | 12 |
| IR-27/28 | `wedge`, apg=True | 117 | 117 | 89 | 28 |
| IR-29 | `arch3`, apg=True | 101 | 101 | 75 | 26 |
| IR-34 to IR-36 | `wedge3`, apg=True | 109 | 109 | 80 | 29 |
| IR-36/37 (9 × 4½ × 3) | `key` | 65 | 65 | 49 | 16 |
| IR-37/38 (9 × 6 × 3) | none | 64 | not comparable | | |

Without the A.P. Green extras: IR-27/28 shapes equal in 21 of 117 (it uses No. 1-X from 4'7"); IR-29
engine refuses 14 rows (the diameters 4½ to 17 in need the No. 4 arch) and is equal in 63; IR-34 to 36
equal in 42 of 109.

The rows that differ (inside diameter, in; HW counts tightest first, then the engine's):
- IR-26: 35 (20/36, 21/35), 39 (15/46, 16/45), 43 (10/56, 11/55), 47 (5/66, 6/65), 51 (0/76, 1/75), and
  92, 96, 100, 104, 108, 112, 116 (HW 76 No.1 + 51, 56, 61, 66, 71, 76, 81 straights; the engine 75 + 52, 57, 62,
  67, 72, 77, 82).
- IR-27/28: 31, 34, 42, 45, 51, 53, 54, 57, 58, 59, 69, 76, 80, 88, 89, 90, 91, 100, 101, 111, 112, 119, 120, 131,
  132, 133, 143, 144.
- IR-29: 17, 18, 20, 21, 22, 23, 34, 42, 43, 44, 49, 50, 57, 58, 59, 60, 71, 78, 79, 80, 81, 82, 92, 102, 108, 144.
- IR-34 to IR-36: 40, 41, 48, 49, 50, 51, 62, 69, 70, 71, 72, 73, 83, 91, 92, 93, 94, 95, 105, 112, 113, 114,
  115, 116, 127, 134, 135, 136, 137.
- Keys (9 × 4½ × 3): 40, 50, 60, 62, 64, 74, 84, 92, 94, 102, 104, 112, 114, 122, 124, 134.

Cause: rounding of the pair, not a different shape size. Take IR-26 at 2'11" (35 in): outside count
N = π(35 + 9)/2.5 = 55.29, so 56 bricks. The inside circle needs 35.19 No.1 arch and 20.11 No.2 arch. HW has
20 No.2 + 36 No.1 (it rounded the tighter shape and let the gentler one make up the total); the engine has 35 + 21
(it rounded the gentler shape). At 4'3" (51 in) the exact counts are 75.40 No.1 and 0.00 No.2: HW 76 + 0, the
engine 75 + 1. I tested nine rules for the split (round the gentler or the tighter count, to nearest,
half-up, down or up; or solve from the whole total); none reproduces every row. Rounding the tighter count fits more rows in the wedge
and key tables (96 of 117, 95 of 109, 56 of 65 against the engine's 89, 80, 49) but fits IR-26 worse (37 of 46
taper rows against 41). The straight region differs systematically (point 5 above).

**The straight region is UR-29's formula 1-a with IR-25's rounding (Derived, coordinator,
`scratch/hwi-deep/coord/splitrules.py`).**
- With a straight and one taper, HW's tapered count is N_f = 2πL/(T − t), counted by the 0.1 rule,
  and the straights make up the total (formulas 1-a to 1-c, `hwi-figures-using.md` §3.5). It is the
  same at every larger diameter:
  - IR-26: 2π × 4½/(2½ − 2⅛) = 75.40 → 76 No. 1 arch;
  - IR-29: 2π × 4½/(3 − 2¾) = 113.10 → 113;
  - IR-27/28: 2π × 9/(2½ − 2¼) = 226.19 → 227 No. 1-X.
- This rule reproduces every straight-region row of IR-26 and IR-29, where the engine's split is one
  brick off.
- In the two-taper rows, the 0.1 rule applied to the gentler count fits more rows than the engine's
  rounding to nearest: IR-27/28 93 of 117 (engine 89), IR-29 83 of 101 (75), IR-34–36 92 of 109
  (80), keys 54 of 65 (49). But in IR-26's taper rows it misses 11 against the engine's 5 (with
  the straight-region rule, IR-26 is 82 of 93 against the engine's 81). So no simple rule gives
  every split; any of them is within one brick.

### 3.3 The circle-brick table (IR-30) and what a method would be

`rings.py` has none, Olsen's appendix has none, and the old planning note that "no 4½ in circle-brick table
exists" is wrong for HW. HW's table fits this model (Derived):
- The circle brick named d-(d+9)-3 has a 9 in outer face and an inner face a = 9·d/(d+9).
- Outside count N = π(D + 9)/9; total = ⌈N − 0.1⌉. This equals HW's total in all 97 rows (2'0" 12,
  3'0" 16, 4'0" 20, 5'0" 24, 6'0" 29, 7'0" 33, 10'0" 45).
- Between sizes d₁ < D < d₂ the two neighbours share the ring: n₂ = (πD − N·a₁)/(a₂ − a₁), n₁ = N − n₂.
- Rounding the gentler count n₂ gives HW's split in 75 of 97 rows; rounding the tighter count n₁ gives it in
  82 of 97. All 22 or 15 misses are one brick.

Example, 2'6" (30 in): N = 13.61 (14 bricks), n₂ = 7.87, n₁ = 5.74, HW 6 of 24-33 + 8 of 36-45.

### 3.4 A.P. Green's circle-brick table (p.117, 6 in steps)

At the 17 diameters both tables print (2'0" to 10'0" in 6 in steps): 9 rows equal (the whole-foot rows, one
size only) and 8 differ, all at the half-foot rows. The totals are equal in all 17. Example: 2'6" A.P. Green 7 + 7,
HW 6 + 8, both 14. The same at 3'6" (9 + 9 against 8 + 10), 4'6" (11 + 11, 10 + 12), 5'6" (13 + 14, 12 + 15),
6'6" (15 + 16, 14 + 17), 7'6" (17 + 18, 16 + 19), 8'6" (19 + 20, 18 + 21) and 9'6" (21 + 22, 20 + 23). A.P.
Green's split is the more even one; HW's follows the exact counts (n₁ = 5.74 at 2'6"), A.P. Green's does not.
A.P. Green also prints 10'6" to 14'0" (sizes to 168-177), beyond HW's table. A.P. Green's table is headed
"9x4½x2½ or 9x4½x3 circle brick"; HW prints 3 in only.

### 3.5 A.P. Green's other ring tables against HW (`brick-shapes.md`)

Compared at the diameters both print (to 12 ft):

| Pair | Rows compared | Equal | Different |
|---|---|---|---|
| IR-26 and p.111 (2½ arch) | 93 | 80 | 13, all splits |
| IR-29 and p.114, p.116 (3 arch) | 100 | 64 | 36, all splits (at 15–19 in a different No. 4 / No. 3 mix) |
| IR-27/28 and the 2½ wedge pages | 117 | 107 | 10, A.P. Green's total one lower |
| 3 in wedge and p.131–132 | 106 | 99 | 7, A.P. Green's total one lower |
| 3 in key 9 × 4½ and A.P. Green's key page | 65 | 61 | 4, A.P. Green's total one lower |

Where the total differs, the exact count has a fraction of 0.11–0.19 (for example the 2½ in wedge at 3'1":
N = 69.12, HW 70, A.P. Green 69; the key at 18 in: N = 25.13, HW 26, A.P. Green 25). So A.P. Green does not round
a tenth up. HW does, and so does the engine. A.P. Green's rule is not derived here (it rounds down at least up
to 0.19).

### 3.6 The arch rows against the geometry (UR-28, `kiln-hardware.md` §4.3)

Rise h = d × (span in ft), with d the printed in/ft; inside radius r = S²/8h + h/2 (r = S at 1.608; r =
0.74742 × S at 2.302). All 538 rows (to 12 ft) were checked. Every row agrees within 0.04 in except the
20 below, which are misprints as printed (**Verified** on the image). No count is among them: every count row
sums to its total.

IR-54, 1½ in/ft (4½ in arch), PDF 177 left:
- 2'5": inside radius printed 2'6 3/16; geometry 2'6 13/16 (the rows either side print 2'5 3/4 and 2'7 7/8).
  A.P. Green prints 2'-6 13/16.

IR-56, 1.608 in/ft (9 in arch), PDF 179. Radius misprints (the foot is one too many):
- Left half: 1'11" prints 2'11" (should be 1'11"); 2'10" prints 3'10"; 2'11" prints 3'11"; 3'10" prints 4'10";
  4'9" prints 5'9"; 4'10" prints 5'10"; 4'11" prints 5'11".
- Right half: 5'8" prints 6'8"; 5'9" 6'9"; 5'10" 6'10"; 5'11" 6'11"; 6'8" prints 7'8"; 6'9" 7'9"; 6'10" 7'10";
  6'11" 7'11".
- A.P. Green's own 1.608 9 in table prints the correct radius in all these rows.

IR-56 rise misprints:
- 2'6" prints 3 1/32, 2'7" prints 3 5/32 (geometry 4 1/32 and 4 5/32; the rows around them step up by 1/8 and
  1/16, so a leading 3 for 4). A.P. Green prints 4 1/32 and 4 5/32.
- 3'9" prints 6 1/8; geometry and A.P. Green 6 1/32.
- 9'6" prints 1'3 9/16; geometry and A.P. Green 1'3 9/32.

No other row differs from the geometry by more than 0.04 in. The largest differences in the other seven
tables are 0.02 in on rise and 0.03 in on radius, the 1/32 in rounding of the printed values.

### 3.7 Arch counts against an arch-course model (Derived, not in the engine)

Model: central angle θ from span and rise; N = θ(r + L)/T outside; Σnt = θr inside; total = ⌈N − 0.1⌉; the
shapes by the engine's pair algebra (gentler count rounded), with the 3 in arch and 3 in wedge tapers (and the No.
1 wedge for the 9 in arch). Against all 538 transcribed rows:

| Table | Totals equal | Shapes equal | Split off by one | At the shape's limit |
|---|---|---|---|---|
| IR-53, 2 in/ft | 41 | 32 | 9 | 0 |
| IR-53, 1.608 | 45 | 38 | 7 | 0 |
| IR-54, 1½ | 46 | 40 | 6 | 0 |
| IR-54, 2.302 | 39 | 29 | 10 | 1 |
| IR-55, 1½ | 87 | 68 | 19 | 0 |
| IR-56, 1.608 | 89 | 75 | 14 | 1 |
| IR-57, 2 | 96 | 72 | 24 | 0 |
| IR-58, 2.302 | 92 | 76 | 16 | 1 |

"At the limit": the tightest shape turns the arch with 0.1 % to spare, so the model refuses by rounding; HW
prints the tightest shape alone (for example 7 No. 3 arch at 1'0", 2.302 in/ft). No total differs.

### 3.8 `kiln-hardware.md` §4.4's eight rows

All eight equal HW05 (counts, rise and inside radius) at 2.302 in/ft (3'0", 3'6", 4'0", 4'6" spans: 11 + 5, 9 + 9,
7 + 13, 5 + 17) and 1.608 in/ft (5 + 10, 3 + 14, 1 + 18, 19 + 2 straights). The note there that "none covers 2½ in
series" holds for the arch tables; the ring table IR-26 does cover the 2½ in arch brick.

### 3.9 A.P. Green's sprung-arch tables against HW's (`brick-shapes.md` p.165–191)

For the 4½ in arch with 3 in brick (HW IR-53, IR-54) and the 9 in arch with 3 in wedge (IR-55 to IR-58),
at 1½, 1.608, 2 and 2.302 in/ft, compared at the spans both print:

| Pair | HW rows | Equal counts | Different |
|---|---|---|---|
| 4½ in arch, 1½ | 46 | 42 | 2 (19": HW 8, APG 9; 32": split) |
| 4½ in arch, 1.608 | 45 | 40 | 5 (13", 16", 22", 36": HW one higher; 40": split) |
| 4½ in arch, 2 | 41 | 40 | 1 (20": 2 + 7 against 3 + 6) |
| 4½ in arch, 2.302 | 40 | 38 | 2 (splits, 52" and 54") |
| 9 in arch, 1½ | 87 | 80 | 7 |
| 9 in arch, 1.608 | 90 | 86 | 4 |
| 9 in arch, 2 | 96 | 79 | 7 (10 HW spans are not in A.P. Green's table) |
| 9 in arch, 2.302 | 93 | 77 | 4 (12 not in A.P. Green's table) |

Totals differ in 23 of the 32 rows, always with A.P. Green one lower, the same rounding difference as §3.5. The
rise and radius cells agree with A.P. Green's except at the HW misprints listed in §3.6 and a 1/32 in rounding at a
few rows (for example 4'2" at 2 in/ft, radius 3'5 21/32 against 3'5 11/16).

## 4. Proposed tests (none written)

Each reads `hwi-ring-arch-tables.yaml`. Source rows are the YAML rows named.

1. **`test_rings_match_hw_totals`**: for every row of IR-26, IR-27/28, IR-29, IR-34 to 36 and IR-36/37 (to 12 ft,
   485 rows), `rings.ring(d, series, apg=…).total == total`. Series: `arch`; `wedge` and `arch3` and `wedge3`
   with `apg=True`; `key`. Source: all rows of those tables.
2. **`test_rings_shapes_within_one_brick_of_hw`**: the same rows, every shape count within 1 of HW's, and the
   number of exact rows at least 81, 89, 75, 80, 49 (the counts in §3.2). A tighter version pins the lists of
   differing diameters in §3.2 so a change to the rounding shows up.
3. **`test_engine_needs_apg_shapes_for_hw_rows`**: IR-29 rows below 18 in raise `RingError` without `apg`; with
   it they equal HW's totals. Source: IR-29 rows 0'4½" to 1'5".
4. **`test_hw_holds_gentlest_taper_in_straight_region`** (documents HW, may be xfail for the engine): IR-26 rows
   from 4'3" have 76 No.1 arch and total − 76 straights; IR-29 rows from 8'3" have 113 No.1 arch. Source: IR-26
   rows 4'3" to 12'0"; IR-29 rows 8'3" to 12'0".
5. **`test_circle_brick_method_matches_ir30_totals`**: a circle-brick method with N = π(D+9)/9 and 0.1 rule returns
   IR-30's total in all 97 rows, and the split within one brick, exact in at least 75. Source: IR-30, all rows.
6. **`test_ir30_single_size_rows`**: at 2'0", 3'0", …, 10'0" the ring is all one size: 12, 16, 20, 24, 29, 33, 37,
   41, 45. Source: IR-30 rows 2'0", 3'0", … 10'0".
7. **`test_olsen_tables_equal_hw`**: Olsen A-4 equals IR-26 in all 52 rows; A-5 equals IR-29's No.3 to No.1
   columns in 65 of 66 rows, the exception being 5'10"; A-6 equals IR-27 with No. 1-X counted as straights where
   HW uses it; A-7 equals the 3 in wedge table. Source: IR-26, IR-29, IR-27, IR-34–36 and Olsen's tables.
8. **`test_arch_geometry_rows`**: for every HW arch row not marked `printed_misprint`, rise is within 1/32 in of
   d × S and inside radius within 1/32 in of S²/8h + h/2; the 20 marked rows fail this and no others do. Source:
   IR-53 to IR-58.
9. **`test_arch_constants_rise_radius`**: r = S at 1.608 and r = 0.74742·S at 2.302, to 1/32 in, on IR-53 and
   IR-56, IR-58 rows. Source: the rows of those tables.
10. **`test_arch_course_totals`**: an arch-course method (θ from span and rise, N = θ(r+L)/T, 0.1 rule) returns
    HW's total in all 538 rows, and shapes within one brick. Source: IR-53 to IR-58.
11. **`test_kiln_hardware_4_4_rows`**: the eight rows of `kiln-hardware.md` §4.4 equal IR-54 right half
    (2.302, 3'0" to 4'6") and IR-53 right half (1.608). Source: those eight YAML rows.

## 5. Not readable, skipped

- **Not readable**: none. Every cell of the transcribed rows was legible.
- **Cut at 12 ft**: IR-26 runs to 15'0", IR-27/28 to 45'0", IR-29 to 15'0", the 3 in wedge to 36'6", the 3 in
  keys to 35'0" (9 × 4½ × 3) and 41'0" (9 × 6 × 3). The 9 in arch tables run to 15'0" (IR-55 to IR-58).
- **Title only, not transcribed** (listed in the YAML under `not_transcribed`):
  - IR-31 (PDF 155), 6 in lining, 3 in arch brick, 12 × 6 × 3 or 13½ × 6 × 3.
  - IR-32, IR-33 (PDF 156–157), 6 in lining, rotary kiln or cupola blocks, 9 × 6 × 4.
  - IR-34 left (PDF 158), 6 in lining, rotary kiln blocks 9 × 6 × 4, arch type, two shape system (KW-3, KW-2,
    KW-1, KW-1X).
  - IR-39, IR-40 (PDF 163–164), 9 in lining, rotary kiln blocks 9 × 9 × 4.
  - IR-41 left (PDF 165), 9 in lining, rotary kiln blocks 9 × 6 × 4, wedge type, two shape system.
  - IR-41 right to IR-43 left (PDF 165–167), 12 in lining, 3 in wedge brick (12 × 4½ × 3, 12 × 6 × 3 or
    12 × 9 × 3); columns No. 3, 2, 1, 1-X wedge and straight.
  - IR-43 right, IR-44 left (PDF 167–168), 12 in lining, 3 in key brick 12 × 6 × 3.
  - IR-44 right to IR-46 left (PDF 168–170), 13½ in lining, 3 in wedge brick.
  - IR-46 right, IR-47 left (PDF 170–171), 13½ in lining, 3 in key brick 13½ × 6 × 3.
  - IR-47 right to IR-49 left (PDF 171–173), 15 in lining, 3 in wedge brick (15 × 6 × 3 or 15 × 9 × 3).
  - IR-49 right, IR-50 (PDF 173–174), 18 in lining, 3 in wedge brick (18 × 6 × 3 or 18 × 9 × 3).
  - IR-59 to IR-62 (PDF 182–185), 12, 13½, 15 and 18 in arch thickness, 3 in wedge brick, 1.608 in/ft on every
    block (read from the headings only).
- **No 2½ in key or circle-brick ring table exists** in IR-25 to IR-50. The key tables are 3 in brick only.
- **Not compared**: A.P. Green's 6 in and 9 × 6 key tables, the 2½ in key table, and the 12 to 18 in sprung
  arches against HW's; `rings.py` has no family for them. Olsen's tables were compared as transcribed in
  `kiln-reference.md`, not against his pages.
