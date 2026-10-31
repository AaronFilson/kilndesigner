# A.P. Green, *Firebrick Shapes, Standard and Special*: transcription

**Source:** A. P. Green Refractories Co. (also printed "A. P. Green Services, Inc."), *Firebrick
Shapes, Standard and Special*, with *Firebrick Combinations for circular linings and arches* and
*Estimating Data and General Information*: catalogue pp.95–229. No edition or year is printed on
any scanned page. Scanned by the author, 30 October 2026: `brick-shapes/b1.jpg`–`b10.jpg` and
`brick-shapes/Image (11).jpg`–`Image (61).jpg`, each a two-page spread turned 90°. Cite the
catalogue page, not the file.

**How it was read:** each page transcribed as printed, every count table summed against its
printed total. `[?read: …]` marks a doubtful reading, `[illegible]` one that couldn't be read,
`(sic)` a value kept as printed though it looks wrong. Handwriting is the owner's, not data
(`(handwritten: …)`): "½ brick" at the Soap on p.95, "12 X 36" on p.168 and p.170.

## What is here, and what isn't

- **Shapes** (p.95–107): the 9 in series (2½ and 3 in), 9 × 6, large 9 in, 9 × 9, 12 × 6, 13½ in,
  square-edge, shiplap; circle brick (p.102); door jambs (p.105); skews (p.106: from standard
  brick, and Brands 4160-A to -F); blast-furnace keys (p.107).
- **Tolerances** (p.104): ±2 % on dimensions of 4 in or more, 3 % under 4 in; overs shipped up to
  10 % on special shapes.
- **Complete circles** (p.111–163): 4½ in to 18 in linings, arch, wedge, key and circle brick,
  rotary-kiln blocks. "No joint allowance was used in computing these tables. Generally it will
  be necessary to cut one or two brick to complete each course" (p.109).
- **Sprung arches** (p.164–199): bricks per course by span, with rise and inside radius, at
  1½ in, 1.608 in (radius = span, 60°), 2 in and 2.302 in of rise per foot of span (central angles
  56°, 60°, 74°, 84°), 4½ in to 18 in thick.
- **Formulas** (p.205): radius = span² ÷ (8 × rise) + rise ÷ 2; rise = radius − √(radius² −
  (span ÷ 2)²); rise = radius − cos(½ central angle) × radius; arch constants for 11 rises per foot
  with a worked 10 ft span (p.206).
- **Estimating** (p.202–205): firebrick per ft³ and per ft² of wall, mortar per 1,000 brick, pounds
  per ft² of castables, plastics and ramming mixes; cones 12–42 (p.207, ASTM C24).
- **Not in the scans:** dome brick and any dome or bottle-kiln table, so conical-brick domes
  (complex curves step 4) have no source here.

## Totals that don't add up as printed

p.115 4'-9" (69, printed 70); p.116 29'-0" (Straight 267 reads, total wants 261); p.128 3'-9"
(No. 1 wedge 62, total wants 60); p.145 6'-6" (KL-3-W 33, total and p.125 want 38); p.151 8'-6"
(No. 2 key taken from the total); p.170 1'-6" and 1'-10", p.172 3'-10" (each one more than
printed: misprints, re-read on crops); p.188 4'-11" (32, printed 31); p.196 15'-6" (69, printed
70). These rows are left out of the tests.

## The engine against these tables

`core/tests/test_apg_tables.py`, with the tables as data (`apg_circles.json`, `apg_arches.json`):

- Every thin end the engine uses (`rings.py`) is printed on p.95–98, including the 3 in series'
  ones it had derived from Olsen's tables.
- **Complete circles**, 681 rows of the 2½ and 3 in arch, wedge and key tables: the engine's ring
  method is within one brick of every total and two of every shape, once A.P. Green's three extra
  shapes are given it (No. 1-X wedge 2½ → 2¼, 3 in No. 4 arch 3 → 1, 3 in No. 1 wedge 3 → 2¾;
  p.96, p.98). They are an option (`rings.ring(..., apg=True)`, `APG_EXTRA`); Olsen's shapes stay
  the default, as studio potters mostly keep to the simpler shapes (the author, 2026-10-30).
- **Sprung arches**, 551 rows (4½ and 9 in, 2½ in series, all four rises): the engine's bricks per
  course (`masonry.arch_ring`, one taper and straights) are within one of every total.


---


Scans are rotated 90°; each image is a two-page spread. No edition or year is printed on these pages. Publisher named: A. P. Green Refractories Co.

## b1.jpg — catalogue p.95 (left half: section title page, unnumbered)

**Section title page (left):** A. P. GREEN / FIREBRICK SHAPES / STANDARD AND SPECIAL

**Page 95 — Firebrick Shapes**

### 9"x4½"x2½" SERIES—IN STOCK . . .

Illustrated here are the standard shapes of 9-inch firebrick — shapes which are specifically designed to be used in connection with the Standard 9-inch firebrick, size 9 x 4½ x 2½ inches. Sometimes the Standard 9-inch firebrick is called "Square" or "Straight". We recommend the use of these 9-inch Shapes where needed, rather than cutting a Standard 9-inch Straight. Cutting is expensive.

| Shape | Dimensions |
|---|---|
| 9" STRAIGHT | 9"x4½"x2½" |
| SMALL 9" BRICK | 9"x3½"x2½" |
| JAMB BRICK | 9"x4½"x2½" |
| SOAP | 9"x2½"x2¼" |
| No. 1 SPLIT | 9"x4½"x1¼" |
| No. 2 SPLIT | 9"x4½"x2" |
| No. 1 ARCH | 9"x4½"x(2½"–2⅛") |
| No. 2 ARCH | 9"x4½"x(2½"–1¾") |
| No. 3 ARCH | 9"x4½"x(2½"–1") |

(handwritten: "½ brick" with an arrow pointing at the SOAP)

## b2.jpg — catalogue p.96–97

### p.96 — 9"x4½"x2½" SERIES . . .

| Shape | Dimensions |
|---|---|
| No. 1-X WEDGE | 9"x4½"x(2½"–2¼") |
| No. 1 WEDGE | 9"x4½"x(2½"–1⅞") |
| No. 2 WEDGE | 9"x4½"x(2½"–1½") |
| 9" NECK | 9"x4½"x(2½"–⅝") |
| No. 1 KEY | 9"x(4½"–4")x2½" |
| No. 2 KEY | 9"x(4½"–3½")x2½" |
| No. 3 KEY | 9"x(4½"–3")x2½" |
| No. 4 KEY | 9"x(4½"–2¼")x2½" |
| FEATHER EDGE | 9"x4½"x(2½"–⅛") |
| EDGE SKEW | 9"x(4½"–1½")x2½" |
| SIDE SKEW | 9"x(4½"–2¼")x2½"; Also 60° SIDE SKEW 9"x(4½"–3⁵⁄₁₆")x2½" [?read: 3⁵⁄₁₆] |
| END SKEW | (9"–6¾")x4½"x2½"; Also 60° END SKEW (9"–7⁷⁄₁₆")x4½"x2½" [?read: 7⁷⁄₁₆] |

### p.97 — 9"x4½"x2½" SERIES—MODIFIED . . .

| Shape | Dimensions |
|---|---|
| ANGLE "A" SKEW | (9"–4½")x4½"x2½" |
| ANGLE "B" SKEW | (9"–)x4½"x2½" |
| ANGLE "C" SKEW | (9"–4½")x4½"x2½" |
| 770 ANCHOR | 8⅞"x4½"x2½" |
| THIN SPLIT | 9"x4½"x½"; 9"x4½"x¾"; 9"x4½"x⅞"; 9"x4½"x1" |
| CIRCLE SPLIT | 9"x4½"x1¼" — "Available in all diameters shown in CIRCLE BRICK table on Page 117." |
| No. 1 NECK | (9"–3½")x4½"x(2½"–⅝") |
| No. 2 NECK | (9"–1½")x4½"x(2½"–⅝") |
| SINGLE TONGUE AND GROVE [sic] | 9"x4½"x2½" |
| DOUBLE TONGUE AND GROOVE | 9"x4½"x2½" |

## b3.jpg — catalogue p.98–99

### p.98 — 9"x4½"x3" SERIES . . .

Listed below are the standard shapes of the 9" x 4½" x 3" series which are available on order. (See section on 9" x 4½" x 2½" series for illustrations of the various shapes.)

| Shape | Dimensions |
|---|---|
| 9" Straight — 3" Series | 9" x 4½" x 3" |
| Small 9" Brick — 3" Series | 9" x 3½" x 3" |
| 9" Soap — 3" Series | 9" x 2¼" x 3" |
| 9" Split Brick — 3" Series | 9" x 4½" x 1½" |
| 9" No. 1 Key — 3" Series | 9" x (4½"-4") x 3" |
| 9" No. 2 Key — 3" Series | 9" x (4½"-3½") x 3" |
| 9" No. 3 Key — 3" Series | 9" x (4½"-3") x 3" |
| 9" No. 4 Key — 3" Series | 9" x (4½"-2¼") x 3" |
| 9" No. 1 Arch — 3" Series | 9" x 4½" x (3"-2¾") |
| 9" No. 2 Arch — 3" Series | 9" x 4½" x (3"-2½") |
| 9" No. 3 Arch — 3" Series | 9" x 4½" x (3"-2") |
| 9" No. 4 Arch — 3" Series | 9" x 4½" x (3"-1") |
| 9" No. 1 Wedge — 3" Series | 9" x 4½" x (3"-2¾") |
| 9" No. 2 Wedge — 3" Series | 9" x 4½" x (3"-2½") |
| 9" No. 3 Wedge — 3" Series | 9" x 4½" x (3"-2") |
| 9" Featheredge — 3" Series | 9" x 4½" x (3"-⅛") |
| 9" Neck Brick — 3" Series | 9" x 4½" x (3"-⅝") |
| 9" Edge Skew — 3" Series | 9" x (4½"-1½") x 3" |
| 9" Jamb — 3" Series | 9" x 4½" x 3" |
| 9"— 60° End Skew — 3" Series | (9"-7¼") x 4½" x 3" |
| 9"— 48° End Skew — 3" Series | (9"-6⁵⁄₁₆") x 4½" x 3" [?read: 6⁵⁄₁₆] |
| 9"— 60° Side Skew — 3" Series | 9" x (4½"-2¾") x 3" |
| 9"— 48° Side Skew — 3" Series | 9" x (4½"-1¹³⁄₁₆") x 3" [?read: 1¹³⁄₁₆] |
| Large 9" Straight — 3" Series | 9" x 6¾" x 3" |
| Large 9" No. 1 Wedge — 3" Series | 9" x 6¾" x (3"-2¾") |
| Large 9" No. 2 Wedge — 3" Series | 9" x 6¾" x (3"-2½") |
| Large 9" No. 3 Wedge — 3" Series | 9" x 6¾" x (3"-2") |

Note: the 3" series No. 1–3 Arch and No. 1–3 Wedge print identical tapers (arch tapers across 4½" width, wedge across 9" length per p.95–96 convention).

### p.99 — 9"x6" SHAPES—

| Shape | Dimensions |
|---|---|
| STRAIGHT | 9"x6"x2½"; Also 9"x6"x3"; 9"x6"x2" |
| SPLIT | 9"x6"x1¼" |
| No. 1 ARCH | 9"x6"x(3½"–2½") |
| No. 2 ARCH | 9"x6"x(3½"–2") |
| No. 1 KEY | 9"x(6"–5⅜")x2½"; Also 9"x(6"–5⅜")x3" |
| No. 2 KEY | 9"x(6"–4¹³⁄₁₆")x2½"; Also 9"x(6"–4¹³⁄₁₆")x3" |

Also Available In:
- 9"x6" No. 1 ARCH 9"x6"x(3"–2¾")
- 9"x6" No. 2 ARCH 9"x6"x(3"–2½")
- 9"x6" No. 3 ARCH 9"x6"x(3"–2")

See tables on 9"x6"x3½" Arch Brick Pages 124 and 125.
See tables on 9"x6" Keys on Pages 138, 139, 140.

## b4.jpg — catalogue p.100–101

### p.100 — LARGE 9" SERIES (9"x6¾")—

From the standpoint of good firebrick construction, this series (9" x 6¾") is especially valuable. As is readily seen, this series is designed to work in connection with the 9" Straight Brick. For example, the large 9" Straight is the same as a full-size 9" brick and a Soap combined. The Wedges have the same taper as the corresponding Wedges in the 9" Shapes. This makes these brick very desirable for breaking joints.

| Shape | Dimensions |
|---|---|
| LARGE 9" STRAIGHT | 9"x6¾"x2½"; ALSO 9"x6¾"x3"; 9"x6¾"x2"; 9"x6¾"x1¼" |
| LARGE 9" No. 1 WEDGE | 9"x6¾"x(2½"-1⅞") |
| LARGE 9" No. 1-X WEDGE | 9"x6¾"x(2½"-2¼") |
| LARGE 9" No. 2 WEDGE | 9"x6¾"x(2½"-1½") |
| LARGE 9" No. 3 WEDGE | 9"x6¾"x(3"-2") |

### p.101

#### 9"x9" SHAPES

| Size | Shape | Dimensions |
|---|---|---|
| 9"x9" | STRAIGHT | 9"x9"x2" |
| 9"x9" | STRAIGHT | 9"x9"x2½" |
| 9"x9" | STRAIGHT | 9"x9"x3" |
| 9"x9" | SPLIT | 9"x9"x1¼" |
| 9"x9" | ARCH OR WEDGE | 9"x9"x(2½"-1½") |
| 9"x9" | ARCH OR WEDGE | 9"x9"x(2½"-1⅞") |
| 9"x9" | ARCH OR WEDGE | 9"x9"x(2½"-2") |
| 9"x9" | ARCH OR WEDGE | 9"x9"x(3"-2½") |

#### 12"x6" SHAPES

| Size | Shape | Dimensions |
|---|---|---|
| 12"x6" | STRAIGHT | 12"x6"x2" |
| 12"x6" | STRAIGHT | 12"x6"x2½" |
| 12"x6" | STRAIGHT | 12"x6"x3" |
| 12"x6" | No. 1 ARCH | 12"x6"x(3"-2¾") |
| 12"x6" | No. 2 ARCH | 12"x6"x(3"-2½") |
| 12"x6" | No. 3 ARCH | 12"x6"x(3"-2") [?read: printed "(3"-2")" with stray mark] |
| 12"x6" | No. 1 WEDGE | 12"x6"x(3"-2¾") |
| 12"x6" | No. 2 WEDGE | 12"x6"x(3"-2½") |
| 12"x6" | No. 3 WEDGE | 12"x6"x(3"-2") |
| 12"x6" | No. 1 KEY | 12"x(6"-5½")x3" |
| 12"x6" | No. 2 KEY | 12"x(6"-5")x3" |
| 12"x6" | 2X KEY | 12"x(6"-4")x3" |
| 12"x6" | No. 3 KEY | 12"x(6"-3")x3" |

#### 13½" SERIES

| Size | Shape | Dimensions |
|---|---|---|
| 13½" | STRAIGHT | 13½"x6"x2½" |
| 13½" | STRAIGHT | 13½"x6"x3" |
| 13½" | No. 1 WEDGE | 13½"x6"x(3"-2¾") |
| 13½" | No. 2 WEDGE | 13½"x6"x(3"-2½") |
| 13½" | No. 3 WEDGE | 13½"x6"x(3"-2") |
| 13½" | No. 1 KEY | 13½"x(6"-5")x2½" |
| 13½" | No. 1 KEY | 13½"x(6"-5")x3" |
| 13½" | No. 2 KEY | 13½"x(6"-4⅜")x2½" |
| 13½" | No. 2 KEY | 13½"x(6"-4⅜")x3" |

NOTE — Also in stock 13½"x4½"x2½"; 13½"x4½"x3"; 13½"x9"x2½" and 13½"x9"x3". In ordering 13½" series brick, always give complete dimensions.
See tables on Pages 153, 154, 157 and 158.

#### SQUARE EDGE SHAPES (Size)

Column 1: 1"x12"x12"; 1¼"x9"x9"; 1½"x6"x12"; 1½"x12"x12"; 1½"x12"x18"; 2"x6"x12"; 2"x9"x9"; 2"x12"x12"; 2"x12"x15"; 2"x12"x18"; 2"x12"x24"; 2"x12"x30"; 2"x15"x18"; 2"x15"x24"; 2"x18"x24"; 2¼"x4½"x12"; 2¼"x4½"x12½"; 2½"x6"x12"; 2½"x6"x13"; 2½"x6"x13½"

Column 2: 2½"x6"x18"; 2½"x9"x9"; 2½"x9"x13½"; 2½"x9"x18"; 2½"x12"x12"; 2½"x12"x15"; 2½"x12"x18"; 2½"x12"x20"; 2½"x12"x24"; 2½"x12"x30"; 2½"x12"x36"; 2½"x15"x18"; 2½"x15"x24"; 2½"x18"x24"; 3"x4½"x13½"; 3"x4½"x18"; 3"x6"x9"; 3"x6"x12"; 3"x6"x13½"; 3"x6"x18"

Column 3: 3"x6"x24"; 3"x9"x9"; 3"x9"x13½"; 3"x9"x18"; 3"x9"x24"; 3"x12"x12"; 3"x12"x15"; 3"x12"x18"; 3"x12"x20"; 3"x12"x24"; 3"x12"x30"; 3"x12"x36"; 3"x15"x15"; 3"x18"x18"; 3"x18"x24"; 3"x18"x30"; 4"x6"x24"; 4"x9"x18"; 4"x9"x20"; 4"x9"x24"

Column 4: 4"x12"x12"; 4"x12"x15"; 4"x12"x18"; 4"x12"x24"; 4"x12"x30"; 4"x12"x36"; 4"x15"x36"; 4"x18"x18"; 4"x18"x20"; 4"x18"x24"; 4"x18"x30"; 4½"x4½"x10½"; 4½"x9"x13½"; 4½"x9"x18"; 5"x6"x18"; 5"x9"x18"; 5"x9"x24"; 5"x9"x30"; 5"x12"x30"; 5"x13½"x24"

#### SHIPLAP SHAPES

| Size | Lapping |
|---|---|
| 2" x6" x12" | (lapped 12" sides) |
| 2" x12"x12" | (lapped 2 sides) |
| 2" x12"x18" | (lapped 18" sides) |
| 2½"x12"x12" | (lapped 2 sides) |
| 2½"x12"x15" | (lapped 15" sides) |
| 2½"x12"x18" | (lapped 18" sides) |
| 2" x6"x12" | (lapped 4 sides) |
| 2" x12"x12" | (lapped 4 sides) |
| 2" x12"x18" | (lapped 4 sides) |
| 2½"x12"x12" | (lapped 4 sides) |
| 2½"x12"x15" | (lapped 4 sides) |
| 2½"x12"x18" | (lapped 4 sides) |

Other shiplap tile, and tongue and groove tile, made to order. When ordering give the number of sides to be lapped. When two sides only are lapped, specify which sides.

## b5.jpg — catalogue p.102–103

### p.102 — CUPOLA BLOCKS 6" LINING (9"—) x 6"x4" — STANDARD BLOCKS

| No. of Block | Dimensions | Diameter Inside | Diameter Outside | No. Blocks to Circle |
|---|---|---|---|---|
| 6-30 | (9"–)x6"x4" | 30" | 42" | 15 |
| 6-36 | (9"–)x6"x4" | 36" | 48" | 17 |
| 6-42 | (9"–)x6"x4" | 42" | 54" | 19 |
| 6-48 | (9"–)x6"x4" | 48" | 60" | 21 |
| 6-54 | (9"–)x6"x4" | 54" | 66" | 23 |
| 6-60 | (9"–)x6"x4" | 60" | 72" | 26 |
| 6-66 | (9"–)x6"x4" | 66" | 78" | 28 |
| 6-72 | (9"–)x6"x4" | 72" | 84" | 30 |
| 6-78 | (9"–)x6"x4" | 78" | 90" | 32 |
| 6-84 | (9"–)x6"x4" | 84" | 96" | 34 |

9"x9"x4" blocks also available. See tables on Page 124 (9"x6"x4" blocks) and Page 141 and 142 (9"x9"x4" blocks).

### p.102 — STANDARD CIRCLE BRICK 4½" LINING (9"—) x 4½" x 2½"

| Name of Brick | Dimensions | Diameter Inside | Diameter Outside | No. Brick to Circle |
|---|---|---|---|---|
| 24" Circle | (9"–)x4½"x2½" | 24" | 33" | 12 |
| 36" Circle | (9"–)x4½"x2½" | 36" | 45" | 16 |
| 48" Circle | (9"–)x4½"x2½" | 48" | 57" | 20 |
| 60" Circle | (9"–)x4½"x2½" | 60" | 69" | 24 |
| 72" Circle | (9"–)x4½"x2½" | 72" | 81" | 29 |
| 84" Circle | (9"–)x4½"x2½" | 84" | 93" | 33 |
| 96" Circle | (9"–)x4½"x2½" | 96" | 105" | 37 |
| 108" Circle | (9"–)x4½"x2½" | 108" | 117" | 41 |
| 120" Circle | (9"–)x4½"x2½" | 120" | 129" | 45 |

See Page 117 for table of 9" Circle Brick.
Circle Splits 9"x4½"x1¼" also available in Circle Brick sizes.

### p.103 — CUPOLA (OR CALLIAU) BLOCKS 4½" LINING (9"—) x 4½" x 9"

| No. of Block | Dimensions | Diameter of Lining Inside | Outside | No. Blocks to Circle |
|---|---|---|---|---|
| A | (9"–)x4½"x9" | 16" | 25" | 9 |
| 1A | (9"–)x4½"x9" | 18" | 27" | 10 |
| B | (9"–)x4½"x9" | 21" | 30" | 11 |
| 2B | (9"–)x4½"x9" | 24" | 33" | 12 |
| C | (9"–)x4½"x9" | 27" | 36" | 13 |
| D | (9"–)x4½"x9" | 30" | 39" | 14 |
| 2D | (9"–)x4½"x9" | 33" | 42" | 15 |
| 3D | (9"–)x4½"x9" | 36" | 45" | 16 |
| E | (9"–)x4½"x9" | 40" | 49" | 18 |
| AE | (9"–)x4½"x9" | 42" | 51" | 18 |
| CE | (9"–)x4½"x9" | 47" | 56" | 20 |
| 2E | (9"–)x4½"x9" | 48" | 57" | 20 |
| F | (9"–)x4½"x9" | 51" | 60" | 21 |
| 2F | (9"–)x4½"x9" | 56" | 65" | 23 |
| G | (9"–)x4½"x9" | 60" | 69" | 24 |
| H | (9"–)x4½"x9" | 73" | 82" | 29 |

### p.103 — ROTARY KILN BLOCKS

6" LINING (9"—) x 6" x 4" *
9" LINING (9"—) x 9" x 4" **
4½", 7½", and other lining thicknesses also available

Much of the success of refractory liners in cement and lime kilns is dependent upon the application of the proper refractory to meet varying operating conditions. To meet these conditions A. P. Green Rotary Kiln Liners are made in high heat duty, super duty and 50%, 60% and 70% high alumina qualities. Each is manufactured with the right physical structure and chemical properties necessary to fill a specific need as required in the various zones of rotary kilns.

A. P. Green KRUZITE D (70% Al₂O₃) are ideal for use in conjunction with Green B 80 and Green B 70 Kiln Liners and are especially recommended where operating conditions are severe. High temperature resistant and carefully controlled and tested during manufacture, their chemical composition cause attraction and retention of a protective coating that means long trouble-free service.

The Engineering Department of the A. P. Green Refractories Co. offers its facilities, without obligation to you, in determining the proper refractories to meet your specific operating conditions.

*See table on page 124.  **See table on page 141 and 142.

## b6.jpg — catalogue p.104–105

### p.104 — SPECIAL REFRACTORY SHAPES

We are able to supply special refractory shapes made to blueprint specifications. Many of the more generally used shapes are carried in stock.

Quality and workmanship are of the highest. Production facilities are unsurpassed. The accuracy and uniformity of A. P. Green special shapes are the result of craftsmanship, scientific control and perfected processes and equipment.

The Green Company keeps molds on hand to manufacture thousands of other special refractory shapes. New molds can be made as required.

(Photo caption:) View of unloading docks at the A. P. Green Refractories Co. Finished ware ready to be unloaded from kiln cars.

#### DEVIATIONS IN DIMENSIONS

Variations (plus or minus) of 2% allowed from specifications on dimensions of 4 inches or over. On dimensions under 4 inches the allowed variations will be 3%.

#### OVER-SHIPMENTS ON SPECIAL SHAPES

It is generally necessary to make a few 'overs' in the production of special material. This is done so that the special shapes, necessary to fill your order, may be carefully selected. If the kiln run has been unusually good, there will frequently be some 'overs' of first quality. These will be shipped in quantities, not to exceed 10%, unless specified to the contrary.

### p.105 — Special Shapes: GREENCLAD DOOR JAMB BRICK*

| Brand | A | B | C | D |
|---|---|---|---|---|
| DJ-1-2½ | 9" | 4½" | 1½" | 2½" |
| DJ-1-3 | 9" | 4½" | 1½" | 3" |
| DJ-2-2½ | 9" | 6¾" | 3¾" | 2½" |
| DJ-2-3 | 9" | 6¾" | 3¾" | 3" |
| DJ-3-2½ | 9" | 9" | 6" | 2½" |
| DJ-3-3 | 9" | 9" | 6" | 3" |
| BS-115-2½ | 13½" | 6¾" | 2¾" | 2½" |
| BS-115-3 | 13½" | 6¾" | 2¾" | 3" |
| BS-116-2½ | 13½" | 9" | 5" | 2½" |
| BS-116-3 | 13½" | 9" | 5" | 3" |
| DJ-18-1-2½ | 18" | 6¾" | 2¾" | 2½" |
| DJ-18-1-3 | 18" | 6¾" | 2¾" | 3" |
| DJ-18-2-2½ | 18" | 9" | 5" | 2½" |
| DJ-18-2-3 | 18" | 9" | 5" | 3" |

(Diagram: A = length, B = width, C = inset dimension, D = thickness.)
*Not internally plated—can also be externally plated on one, two or three sides.

## b7.jpg — catalogue p.106–107

### p.106 — Skews: SKEWS BUILT FROM STANDARD 9" BRICK

1. For 4½" Arch; Rise = 1½" per Foot of Span. One Skew Requires — One Featheredge; 9" x 4½" x (2½"–⅛"), One 2" Brick—9"x4½"x2". See Tables, Pages 164, 165.
2. For 4½" Arch; Rise = 2.302" per Foot of Span. One Skew Requires — Two Side Skews 9" x (4½"-2¼") x 2½"; One Straight Brick — 9" x 4½" x 2½"; One Soap Brick—9"x2½"x2¼". See Tables, Pages 170, 171.
3. For 9" Arch; Rise = 2.302" per Foot of Span. One Skew Requires — Three Side Skews 9" x (4½"-2¼") x 2½"; One Straight Brick — 9" x 4½" x 2½"; One Soap Brick—9"x2½"x2¼". See Tables, Pages 188-191.

(Drawings show overall skew outlines: 4½"x2⅝"[?read]x9"; 4½"/5"x9"; 7¼"x2½"[?read]x9"/9" — dimension labels too small to read with confidence.)

### p.106 — SPECIAL SKEWS

| Skew | Text |
|---|---|
| 4160-A | For 4½" Arch; Rise = 1.608" per Foot of Span. Central Angle = 60°, and Radius = Span. See Tables, Pages 166, 167 |
| 4160-B | For 9" Arch; Rise = 1.608" per Foot of Span. Central Angle = 60°; and Radius = Span. See Tables, Pages 180-183. |
| 4160-C | For 4½" Arch; Rise = 2" per Foot of Span. See Tables, Pages 168, 169. |
| 4160-D | For 9" Arch; Rise = 2" per Foot of Span. See Tables, Pages 184-187. |
| 4160-E | For 6" Arch; Rise = 1½" per Foot of Span. See Table, Page 172. |
| 4160-F | For 6" Arch; Rise = 2" per Foot of Span. See Table, Page 174. |

Drawing dimension labels (small, doubtful): 4160-A 2¼"[?], 4½", 9", 4½"; 4160-B 4½", 9", 9"; 4160-C 1⅝"[?read], 4½", 9", 4½"; 4160-D 3⅝"[?read], 8"[?read], 9"; 4160-E 1/16"[?read: 1⁄16 top], 6", 9", 4½", ⅝"[?]; 4160-F 29/32"[?read], 5"[?read], 9", 4½". [illegible: fine dimension marks on skew drawings]

Note: 4160-A/B central angle 60° with radius = span — consistent with rise 1.608" per foot (12 x (1 − cos30°)/(2 sin30°) = 1.608"). (My check, not printed.)

### p.107 — Special Blast Furnace Key Brick

Drawings: each key 6" (or 5²³⁄₃₂"/5²⁹⁄₃₂"/5³¹⁄₃₂" top) wide tapering to 5¹¹⁄₁₆" or 5⅝" at the other face, length 13½", 9" or 12", thickness "A".

| Brand | Length | Width (large – small) | Dimen. "A" |
|---|---|---|---|
| A-1K | 13½" | 6" – 5¹¹⁄₁₆" | 3" |
| A-1K-2½ | 13½" | 6" – 5¹¹⁄₁₆" | 2½" |
| A-1K-S | 13½" | 6" – 5¹¹⁄₁₆" | 1½" |
| A-2K | 13½" | 6" – 5⅝" | 3" |
| A-2K-2½ | 13½" | 6" – 5⅝" | 2½" |
| A-2K-S | 13½" | 6" – 5⅝" | 1½" |
| B-1K | 9" | 5²⁹⁄₃₂" – 5¹¹⁄₁₆" | 3" |
| B-1K-2½" | 9" | 5²⁹⁄₃₂" – 5¹¹⁄₁₆" | 2½" |
| B-1K-S | 9" | 5²⁹⁄₃₂" – 5¹¹⁄₁₆" | 1½" |
| B-2K | 9" | 5²³⁄₃₂" – 5⅝" [?read] | 3" |
| B-2K-2½ | 9" | 5²³⁄₃₂" – 5⅝" [?read] | 2½" |
| B-2K-S | 9" | 5²³⁄₃₂" – 5⅝" [?read] | 1½" |
| C-1K | 12" | 5³¹⁄₃₂" – 5¹¹⁄₁₆" [?read] | 3" |
| C-1K-2½ | 12" | 5³¹⁄₃₂" – 5¹¹⁄₁₆" [?read] | 2½" |
| C-1K-S | 12" | 5³¹⁄₃₂" – 5¹¹⁄₁₆" [?read] | 1½" |
| C-2K | 12" | 5²⁹⁄₃₂" – 5⅝" [?read] | 3" |
| C-2K-2½ | 12" | 5²⁹⁄₃₂" – 5⅝" [?read] | 2½" |
| C-2K-S | 12" | 5²⁹⁄₃₂" – 5⅝" [?read] | 1½" |

(Small upper-face fractions on the B and C drawings are doubtful; lengths and "A" values are clear.) Each box: "See Table, Page 148." Also available in 15" and 18" lengths.

## b8.jpg — catalogue p.109 (left half: section title page, unnumbered)

**Section title page (left):** A. P. GREEN / FIREBRICK COMBINATIONS / For circular linings and arches

### p.109 — Tables of Brick Combinations for Circles and Arches

The following tables are offered for use in estimating the quantities of brick required for circular linings of various diameters and for the construction of arches. No joint allowance was used in computing these tables. Generally it will be necessary to cut one or two brick to complete each course of the circular lining or arch.

An index for the tables is given below. They are arranged according to the thickness of the lining or arch, starting with 4½ inches and progressively increasing to 18 inches.

The majority of the shapes listed in the tables are stock items in many qualities. Contact your Green representative for definite shipping promises on specific bills of material.

#### INDEX OF TABLES

| Section | Table | Page |
|---|---|---|
| 4½-Inch Circle Lining | 9" x 4½" x 2½" or 13½" x 4½" x 2½" Arch Brick | 111 |
| | 9" x 4½" x 3" or 13½" x 4½" x 3" Arch Brick | 114 |
| | 9" x 4½" x 2½" or 9" x 4½" x 3" Circle Brick | 117 |
| 4½-Inch Arch — 1½" Rise per Foot of Span | 9" x 4½" x 2½" or 13½" x 4½" x 2½" Arch Brick | 164 |
| | 9" x 4½" x 3" or 13½" x 4½" x 3" Arch Brick | 165 |
| 4½-Inch Arch — 1.608" Rise per Foot of Span | 9" x 4½" x 2½" or 13½" x 4½" x 2½" Arch Brick | 166 |
| | 9" x 4½" x 3" or 13½" x 4½" x 3" Arch Brick | 167 |
| 4½-Inch Arch — 2" Rise per Foot of Span | 9" x 4½" x 2½" or 13½" x 4½" x 2½" Arch Brick | 168 |
| | 9" x 4½" x 3" or 13½" x 4½" x 3" Arch Brick | 169 |
| 4½-Inch Arch — 2.302" Rise per Foot of Span | 9" x 4½" x 2½" or 13½" x 4½" x 2½" Arch Brick | 170 |
| | 9" x 4½" x 3" or 13½" x 4½" x 3" Arch Brick | 171 |
| 6-Inch Circle Lining | 9" x 6" x 3", 12" x 6" x 3" or 13½" x 6" x 3" Arch Brick | 118 |
| | 9" x 6" x 3½" Arch Brick with 9" x 6" x 2½" Straights | 120 |
| | 9" x 6" x 3½" Arch Brick with 9" x 6" x 3" Straights | 121 |
| | 9" x 6" x 3" Arch Type Rotary Kiln Liners | 122 |
| | 9" x 6" x 3½" Arch Type Rotary Kiln Liners | 123 |
| | 9" x 6" x 4" Rotary Kiln Blocks | 124 |
| | 9" x 6" x 4" Arch Type Rotary Kiln Blocks | 125 |
| | 9" x 6" x 3" Rotary Kiln Blocks (Basic Brick only) | 126 |
| | 9" x 6" x 3½" Rotary Kiln Blocks (Basic Brick only) | 127 |
| 6-Inch Arch — 1½" Rise per Foot of Span | 9" x 6" x 3", 12" x 6" x 3" or 13½" x 6" x 3" Arch Brick | 172 |
| 6-Inch Arch — 1.608" Rise per Foot of Span | 9" x 6" x 3", 12" x 6" x 3" or 13½" x 6" x 3" Arch Brick | 173 |
| 6-Inch Arch — 2" Rise per Foot of Span | 9" x 6" x 3", 12" x 6" x 3" or 13½" x 6" x 3" Arch Brick | 174 |
| 6-Inch Arch — 2.302" Rise per Foot of Span | 9" x 6" x 3", 12" x 6" x 3" or 13½" x 6" x 3" Arch Brick | 175 |

Continued Next Page

## b9.jpg — catalogue p.110–111

### p.110 — Tables of Brick Combinations for Circles and Arches—Continued: INDEX OF TABLES (cont.)

(The heading of the 9-Inch Circle Lining section is on p.109's continuation, not repeated; the first rows below belong to it.)

| Section | Table | Page |
|---|---|---|
| 9-Inch Circle Lining (cont.) | 9" x 4½" x 2½", 9" x 6¾" x 2½" or 9" x 9" x 2½" Wedge Brick | 130 |
|  | 9" x 4½" x 3", 9" x 6¾" x 3" or 9" x 9" x 3" Wedge Brick | 133 |
|  | 9" x 4½" x 2½" or 9" x 4½" x 3" Key Brick | 136 |
|  | 9" x 6" x 2½" or 9" x 6" x 3" Key Brick | 138 |
|  | 9" x 6" x 3" Wedge Type Rotary Kiln Liners | 139 |
|  | 9" x 6" x 3½" Wedge Type Rotary Kiln Liners | 140 |
|  | 9" x 9" x 4" Rotary Kiln Blocks | 141 |
|  | 12" x 9" x 4" Rotary Kiln Blocks | 143 |
|  | 9" x 6" x 4" Wedge Type Rotary Kiln Blocks | 145 |
|  | 9" x 6" x 3" Wedge Type Rotary Kiln Blocks (Basic Brick Only) | 146 |
|  | 9" x 6" x 3½" Wedge Type Rotary Kiln Blocks (Basic Brick Only) | 147 |
| 9-Inch, 12-Inch and 13½-Inch Circle Lining | Special Blast Furnace Key Brick | 148 |
| 9-Inch Arch — 1½" Rise per Foot of Span | 9" x 4½" x 2½", 9" x 6¾" x 2½" or 9" x 9" x 2½" Wedge Brick | 176 |
|  | 9" x 4½" x 3", 9" x 6¾" x 3" or 9" x 9" x 3" Wedge Brick | 178 |
| 9-Inch Arch — 1.608" Rise per Foot of Span | 9" x 4½" x 2½", 9" x 6¾" x 2½" or 9" x 9" x 2½" Wedge Brick | 180 |
|  | 9" x 4½" x 3", 9" x 6¾" x 3" or 9" x 9" x 3" Wedge Brick | 182 |
|  | 9" x 6" x 3" Rotary Kiln Block Wedges (Basic Brick only) | 146 |
|  | 9" x 6" x 3½" Rotary Kiln Block Wedges (Basic Brick only) | 147 |
| 9-Inch Arch — 2" Rise per Foot of Span | 9" x 4½" x 2½", 9" x 6¾" x 2½" or 9" x 9" x 2½" Wedge Brick | 184 |
|  | 9" x 4½" x 3", 9" x 6¾" x 3" or 9" x 9" x 3" Wedge Brick | 186 |
| 9-Inch Arch — 2.302" Rise per Foot of Span | 9" x 4½" x 2½", 9" x 6¾" x 2½" or 9" x 9" x 2½ Wedge Brick | 188 |
|  | 9" x 4½" x 3", 9" x 6¾" x 3" or 9" x 9" x 3" Wedge Brick | 190 |
| 12-Inch Circle Lining | 12" x 4½" x 3", 12" x 6" x 3" or 12" x 9" x 3" Wedge Brick | 149 |
|  | 12" x 6" x 2½" or 12" x 6" x 3" Key Brick | 151 |
| 12-Inch Arch — 1.608" Rise per Foot of Span | 12" x 4½" x 3", 12" x 6" x 3" or 12" x 9" x 3" Wedge Brick | 192 |
| 13½-Inch Circle Lining | 13½" x 4½" x 3", 13½" x 6" x 3" or 13½" x 9" x 3" Wedge Brick | 153 |
|  | 13½" x 4½" x 3" Key Brick (Basic Brick only) | 155 |
|  | 13½" x 6" x 2½" or 13½" x 6" x 3" Key Brick | 157 |
| 13½-Inch Arch — 1.608" Rise per Foot of Span | 13½" x 4½" x 3", 13½" x 6" x 3" or 13½" x 9" x 3" Wedge Brick | 194 |
| 15-Inch Circle Lining | 15" x 6" x 3" or 15" x 9" x 3" Wedge Brick | 159 |
| 15-Inch Arch — 1.608" Rise per Foot of Span | 15" x 6" x 3" or 15" x 9" x 3" Wedge Brick | 196 |
| 18-Inch Circle Lining | 18" x 6" x 3" or 18" x 9" x 3" Wedge Brick | 161 |
| 18-Inch Arch — 1.608" Rise per Foot of Span | 18" x 6" x 3" or 18" x 9" x 3" Wedge Brick | 198 |
| 18-Inch Blast Furnace Bottom Blocks |  | 163 |

### p.111 — COMPLETE CIRCLES 9"x4½"x2½" or 13½"x4½"x2½" ARCH BRICK — 4½-INCH LINING

SHAPES REQUIRED TO TURN CIRCLE. Columns: No. 3 ARCH 9x4½x(2½-1); No. 2 ARCH 9x4½x(2½-1¾); No. 1 ARCH 9x4½x(2½-2⅛); STRAIGHT 9x4½x2½. "…" = none printed (dotted leader).

| Inside Diameter | No. 3 Arch | No. 2 Arch | No. 1 Arch | Straight | Total |
|---|---|---|---|---|---|
| 0'-6" | 19 | … | … | … | 19 |
| 0'-7" | 17 | 4 | … | … | 21 |
| 0'-8" | 16 | 6 | … | … | 22 |
| 0'-9" | 15 | 8 | … | … | 23 |
| 0'-10" | 14 | 10 | … | … | 24 |
| 0'-11" | 12 | 14 | … | … | 26 |
| 1'-0" | 11 | 16 | … | … | 27 |
| 1'-1" | 10 | 18 | … | … | 28 |
| 1'-2" | 9 | 20 | … | … | 29 |
| 1'-3" | 7 | 24 | … | … | 31 |
| 1'-4" | 6 | 26 | … | … | 32 |
| 1'-5" | 5 | 28 | … | … | 33 |
| 1'-6" | 4 | 30 | … | … | 34 |
| 1'-7" | 2 | 34 | … | … | 36 |
| 1'-8" | 1 | 36 | … | … | 37 |
| 1'-9" | … | 38 | … | … | 38 |
| 1'-10" | … | 36 | 3 | … | 39 |
| 1'-11" | … | 35 | 6 | … | 41 |
| 2'-0" | … | 34 | 8 | … | 42 |
| 2'-1" | … | 33 | 10 | … | 43 |
| 2'-2" | … | 31 | 13 | … | 44 |
| 2'-3" | … | 30 | 16 | … | 46 |
| 2'-4" | … | 29 | 18 | … | 47 |
| 2'-5" | … | 28 | 20 | … | 48 |
| 2'-6" | … | 26 | 23 | … | 49 |
| 2'-7" | … | 25 | 26 | … | 51 |
| 2'-8" | … | 24 | 28 | … | 52 |
| 2'-9" | … | 23 | 30 | … | 53 |
| 2'-10" | … | 21 | 33 | … | 54 |
| 2'-11" | … | 20 | 36 | … | 56 |
| 3'-0" | … | 19 | 38 | … | 57 |
| 3'-1" | … | 18 | 40 | … | 58 |
| 3'-2" | … | 16 | 43 | … | 59 |
| 3'-3" | … | 15 [?read] | 46 | … | 61 |
| 3'-4" | … | 14 [?read] | 48 | … | 62 |
| 3'-5" | … | 13 [?read] | 50 | … | 63 |
| 3'-6" | … | 11 [?read] | 53 | … | 64 |
| 3'-7" | … | 10 [?read] | 56 | … | 66 |
| 3'-8" | … | 9 [?read] | 58 | … | 67 |
| 3'-9" | … | 8 [?read] | 60 | … | 68 |
| 3'-10" | … | 6 | 64 | … | 70 |
| 3'-11" | … | 5 | 66 | … | 71 |
| 4'-0" | … | 4 | 68 | … | 72 |
| 4'-1" | … | 3 | 70 | … | 73 |
| 4'-2" | … | 1 | 74 | … | 75 |
| 4'-3" | … | … | 76 | … | 76 |
| 4'-4" | … | … | 76 | 1 | 77 |
| 4'-5" | … | … | 76 | 2 | 78 |
| 4'-6" | … | … | 76 | 4 | 80 |
| 4'-8" | … | … | 76 | 6 | 82 |
| 4'-10" | … | … | 76 | 9 | 85 |

Totals check: all rows sum to the printed total. The No. 2 Arch digits for 3'-3" to 3'-9" are crowded in the scan; the values given are the ones consistent with the clearly printed No. 1 Arch and Total. Continued Next Page.

## b10.jpg — catalogue p.112–113

COMPLETE CIRCLES 9"x4½"x2½" or 13½"x4½"x2½" ARCH BRICK — 4½-INCH LINING (continued). Same columns; No. 3 Arch and No. 2 Arch are dotted (none) on every row of both pages, so only No. 1 Arch, Straight and Total are shown.

### p.112

| Inside Diameter | No. 1 Arch | Straight | Total |
|---|---|---|---|
| 5'-0" | 76 | 11 | 87 |
| 5'-2" | 76 | 14 | 90 |
| 5'-4" | 76 | 16 | 92 |
| 5'-6" | 76 | 19 | 95 |
| 5'-8" | 76 | 21 | 97 |
| 5'-10" | 76 | 24 | 100 |
| 6'-0" | 76 | 26 | 102 |
| 6'-2" | 76 | 29 | 105 |
| 6'-4" | 76 | 31 | 107 |
| 6'-6" | 76 | 34 | 110 |
| 6'-8" | 76 | 36 | 112 |
| 6'-10" | 76 | 39 | 115 |
| 7'-0" | 76 | 41 | 117 |
| 7'-2" | 76 | 44 | 120 |
| 7'-4" | 76 | 46 | 122 |
| 7'-6" | 76 | 49 | 125 |
| 7'-8" | 76 | 51 | 127 |
| 7'-10" | 76 | 54 | 130 |
| 8'-0" | 76 | 56 | 132 |
| 8'-2" | 76 | 59 | 135 |
| 8'-4" | 76 | 61 | 137 |
| 8'-6" | 76 | 64 | 140 |
| 8'-8" | 76 | 66 | 142 |
| 8'-10" | 76 | 69 | 145 |
| 9'-0" | 76 | 71 | 147 |
| 9'-2" | 76 | 74 | 150 |
| 9'-4" | 76 | 76 | 152 |
| 9'-6" | 76 | 79 | 155 |
| 9'-8" | 76 | 81 | 157 |
| 9'-10" | 76 | 84 | 160 |
| 10'-0" | 76 | 87 | 163 |
| 10'-2" | 76 | 89 | 165 |
| 10'-4" | 76 | 92 | 168 |
| 10'-6" | 76 | 94 | 170 |
| 10'-8" | 76 | 97 | 173 |
| 10'-10" | 76 | 99 | 175 |
| 11'-0" | 76 | 102 | 178 |
| 11'-2" | 76 | 104 | 180 |
| 11'-4" | 76 | 107 | 183 |
| 11'-6" | 76 | 109 | 185 |
| 11'-8" | 76 | 112 | 188 |
| 11'-10" | 76 | 114 | 190 |
| 12'-0" | 76 | 117 | 193 |
| 12'-2" | 76 | 119 | 195 |
| 12'-4" | 76 | 122 | 198 |
| 12'-6" | 76 | 124 | 200 |
| 12'-8" | 76 | 127 | 203 |
| 12'-10" | 76 | 129 | 205 |
| 13'-0" | 76 | 132 | 208 |
| 13'-2" | 76 | 134 | 210 |

### p.113

| Inside Diameter | No. 1 Arch | Straight | Total |
|---|---|---|---|
| 13'-4" | 76 | 137 | 213 |
| 13'-6" | 76 | 139 | 215 |
| 13'-8" | 76 | 142 | 218 |
| 13'-10" | 76 | 144 | 220 |
| 14'-0" | 76 | 147 | 223 |
| 14'-2" | 76 | 149 | 225 |
| 14'-4" | 76 | 152 | 228 |
| 14'-6" | 76 | 154 | 230 |
| 14'-8" | 76 | 157 | 233 |
| 14'-10" | 76 | 159 | 235 |
| 15'-0" | 76 | 162 | 238 |
| 15'-6" | 76 | 169 | 245 |
| 16'-0" | 76 | 177 | 253 |
| 16'-6" | 76 | 185 | 261 |
| 17'-0" | 76 | 192 | 268 |
| 17'-6" | 76 | 200 | 276 |
| 18'-0" | 76 | 207 | 283 |
| 18'-6" | 76 | 215 | 291 |
| 19'-0" | 76 | 222 | 298 |
| 19'-6" | 76 | 230 | 306 |
| 20'-0" | 76 | 237 | 313 |
| 20'-6" | 76 | 245 | 321 |
| 21'-0" | 76 | 252 | 328 |
| 21'-6" | 76 | 260 | 336 |
| 22'-0" | 76 | 267 | 343 |
| 22'-6" | 76 | 275 | 351 |
| 23'-0" | 76 | 283 | 359 |
| 23'-6" | 76 | 290 | 366 |
| 24'-0" | 76 | 298 | 374 |
| 24'-6" | 76 | 305 | 381 |
| 25'-0" | 76 | 313 | 389 |
| 25'-6" | 76 | 320 | 396 |
| 26'-0" | 76 | 328 | 404 |
| 26'-6" | 76 | 335 | 411 |
| 27'-0" | 76 | 343 | 419 |
| 27'-6" | 76 | 350 | 426 |
| 28'-0" | 76 | 358 | 434 |
| 28'-6" | 76 | 365 | 441 |
| 29'-0" | 76 | 373 | 449 |
| 29'-6" | 76 | 381 | 457 |
| 30'-0" | 76 | 388 | 464 |
| 30'-6" | 76 | 396 | 472 |
| 31'-0" | 76 | 403 | 479 |
| 31'-6" | 76 | 411 | 487 |
| 32'-0" | 76 | 418 | 494 |
| 32'-6" | 76 | 426 | 502 |
| 33'-0" | 76 | 433 | 509 |
| 33'-6" | 76 | 441 | 517 |
| 34'-0" | 76 | 448 | 524 |

Totals check (p.112–113): every printed total equals 76 + Straight; no mismatches.

## Image (11).jpg — catalogue p.114–115

### p.114 — COMPLETE CIRCLES 9"x4½"x3" or 13½"x4½"x3" ARCH BRICK — 4½-INCH LINING

SHAPES REQUIRED TO TURN CIRCLE. Columns: No. 4 ARCH 9x4½x(3-1); No. 3 ARCH 9x4½x(3-2); No. 2 ARCH 9x4½x(3-2½); No. 1 ARCH 9x4½x(3-2¾); STRAIGHT 9x4½x3.

| Inside Diameter | No. 4 Arch | No. 3 Arch | No. 2 Arch | No. 1 Arch | Straight | Total |
|---|---|---|---|---|---|---|
| 0'-4½" | 15 | … | … | … | … | 15 |
| 0'-5" | 14 | 1 | … | … | … | 15 |
| 0'-6" | 13 | 3 | … | … | … | 16 |
| 0'-7" | 12 | 5 | … | … | … | 17 |
| 0'-8" | 11 | 7 | … | … | … | 18 |
| 0'-9" | 10 | 9 | … | … | … | 19 |
| 0'-10" | 8 | 12 | … | … | … | 20 |
| 0'-11" | 7 | 14 | … | … | … | 21 |
| 1'-0" | 6 | 16 | … | … | … | 22 |
| 1'-1" | 5 | 18 | … | … | … | 23 |
| 1'-2" | 4 | 20 | … | … | … | 24 |
| 1'-3" | 2 | 24 | … | … | … | 26 |
| 1'-4" | 1 | 26 | … | … | … | 27 |
| 1'-5" | … | 28 | … | … | … | 28 |
| 1'-6" | … | 28 | 1 | … | … | 29 |
| 1'-7" | … | 27 | 3 | … | … | 30 |
| 1'-8" | … | 26 | 5 | … | … | 31 |
| 1'-9" | … | 25 | 7 | … | … | 32 |
| 1'-10" | … | 24 | 9 | … | … | 33 |
| 1'-11" | … | 23 | 11 | … | … | 34 |
| 2'-0" | … | 22 | 13 | … | … | 35 |
| 2'-1" | … | 21 | 15 | … | … | 36 |
| 2'-2" | … | 20 | 17 | … | … | 37 |
| 2'-3" | … | 19 | 19 | … | … | 38 |
| 2'-4" | … | 18 | 21 | … | … | 39 |
| 2'-5" | … | 17 | 23 | … | … | 40 |
| 2'-6" | … | 16 | 25 | … | … | 41 |
| 2'-7" | … | 15 | 27 | … | … | 42 |
| 2'-8" | … | 14 | 29 | … | … | 43 |
| 2'-9" | … | 13 | 31 | … | … | 44 |
| 2'-10" | … | 12 | 33 | … | … | 45 |
| 2'-11" | … | 10 | 36 | … | … | 46 |
| 3'-0" | … | 9 | 39 | … | … | 48 |
| 3'-1" | … | 8 | 41 | … | … | 49 |
| 3'-2" | … | 7 | 43 | … | … | 50 |
| 3'-3" | … | 6 | 45 | … | … | 51 |
| 3'-4" | … | 5 | 47 | … | … | 52 |
| 3'-5" | … | 4 | 49 | … | … | 53 |
| 3'-6" | … | 3 | 51 | … | … | 54 |
| 3'-7" | … | 2 | 53 | … | … | 55 |
| 3'-8" | … | 1 | 55 | … | … | 56 |
| 3'-9" | … | … | 57 | … | … | 57 |
| 3'-10" | … | … | 56 | 2 | … | 58 |
| 3'-11" | … | … | 55 | 4 | … | 59 |
| 4'-0" | … | … | 54 | 6 | … | 60 |
| 4'-1" | … | … | 52 | 9 | … | 61 |
| 4'-2" | … | … | 51 | 11 | … | 62 |
| 4'-3" | … | … | 50 | 13 | … | 63 |
| 4'-4" | … | … | 49 | 15 | … | 64 |
| 4'-5" | … | … | 48 | 17 | … | 65 |
| 4'-6" | … | … | 47 | 19 | … | 66 |

Totals check (p.114): every row sums to its printed total (totals run 15, 15, 16 … 66, read from the page and matching). Continued Next Page.

### p.115 — continued (No. 4 Arch and No. 3 Arch dotted/none on every row)

| Inside Diameter | No. 2 Arch | No. 1 Arch | Straight | Total |
|---|---|---|---|---|
| 4'-7" | 46 | 21 | … | 67 |
| 4'-8" | 45 | 23 | … | 68 |
| 4'-9" | 44 | 25 | … | 70 |
| 4'-10" | 42 | 29 | … | 71 |
| 4'-11" | 41 | 31 | … | 72 |
| 5'-0" | 41 | 32 | … | 73 |
| 5'-1" | 39 | 35 | … | 74 |
| 5'-2" | 38 | 37 | … | 75 |
| 5'-3" | 38 | 38 | … | 76 |
| 5'-4" | 36 | 41 | … | 77 |
| 5'-5" | 35 | 43 | … | 78 |
| 5'-6" | 34 | 45 | … | 79 |
| 5'-7" | 33 | 47 | … | 80 |
| 5'-8" | 32 | 49 | … | 81 |
| 5'-9" | 32 | 50 | … | 82 |
| 5'-10" | 30 | 53 | … | 83 |
| 5'-11" | 29 | 55 | … | 84 |
| 6'-0" | 28 | 57 | … | 85 |
| 6'-1" | 27 | 59 | … | 86 |
| 6'-2" | 26 | 61 | … | 87 |
| 6'-3" | 25 | 63 | … | 88 |
| 6'-4" | 24 | 65 | … | 89 |
| 6'-5" | 23 | 67 | … | 90 |
| 6'-6" | 21 | 71 | … | 92 |
| 6'-7" | 20 | 73 | … | 93 |
| 6'-8" | 19 | 75 | … | 94 |
| 6'-9" | 18 | 77 | … | 95 |
| 6'-10" | 17 | 79 | … | 96 |
| 6'-11" | 16 | 81 | … | 97 |
| 7'-0" | 15 | 83 | … | 98 |
| 7'-1" | 14 | 85 | … | 99 |
| 7'-2" | 13 | 87 | … | 100 |
| 7'-3" | 12 | 89 | … | 101 |
| 7'-4" | 11 | 91 | … | 102 |
| 7'-5" | 10 | 93 | … | 103 |
| 7'-6" | 9 | 95 | … | 104 |
| 7'-7" | 8 | 97 | … | 105 |
| 7'-8" | 7 | 99 | … | 106 |
| 7'-9" | 6 | 101 | … | 107 |
| 7'-10" | 5 | 103 | … | 108 |
| 7'-11" | 4 | 105 | … | 109 |
| 8'-0" | 3 | 107 | … | 110 |
| 8'-1" | 2 | 109 | … | 111 |
| 8'-2" | 1 | 111 | … | 112 |
| 8'-3" | … | 113 | … | 113 |
| 8'-6" | … | 113 | 4 | 117 |
| 9'-0" | … | 113 | 10 | 123 |
| 9'-6" | … | 113 | 16 | 129 |
| 10'-0" | … | 113 | 22 | 135 |
| 10'-6" | … | 113 | 29 | 142 |

Totals check (p.115): **mismatch at 4'-9"** — printed No. 2 Arch 44 + No. 1 Arch 25 = 69, but printed Total is 70 (the sequence 67, 68, 70, 71, 72 skips 69). Either a misprint or one cell is misread [?read: No. 1 Arch may be 26]. All other rows sum correctly. Continued Next Page.

## Image (12).jpg — catalogue p.116–117

### p.116 — COMPLETE CIRCLES 9"x4½"x3" or 13½"x4½"x3" ARCH BRICK — 4½-INCH LINING (continued)

No. 4, No. 3 and No. 2 Arch dotted (none) on every row.

| Inside Diameter | No. 1 Arch | Straight | Total |
|---|---|---|---|
| 11'-0" | 113 | 35 | 148 |
| 11'-6" | 113 | 41 | 154 |
| 12'-0" | 113 | 48 | 161 |
| 12'-6" | 113 | 54 | 167 |
| 13'-0" | 113 | 60 | 173 |
| 13'-6" | 113 | 66 | 179 |
| 14'-0" | 113 | 73 | 186 |
| 14'-6" | 113 | 79 | 192 |
| 15'-0" | 113 | 85 | 198 |
| 15'-6" | 113 | 92 | 205 |
| 16'-0" | 113 | 98 | 211 |
| 16'-6" | 113 | 104 | 217 |
| 17'-0" | 113 | 110 | 223 |
| 17'-6" | 113 | 117 | 230 |
| 18'-0" | 113 | 123 | 236 |
| 18'-6" | 113 | 129 | 242 |
| 19'-0" | 113 | 136 | 249 |
| 19'-6" | 113 | 142 | 255 |
| 20'-0" | 113 | 148 | 261 |
| 20'-6" | 113 | 154 | 267 |
| 21'-0" | 113 | 161 | 274 |
| 21'-6" | 113 | 167 | 280 |
| 22'-0" | 113 | 173 | 286 |
| 22'-6" | 113 | 180 | 293 |
| 23'-0" | 113 | 186 | 299 |
| 23'-6" | 113 | 192 | 305 |
| 24'-0" | 113 | 198 | 311 |
| 24'-6" | 113 | 205 | 318 |
| 25'-0" | 113 | 211 | 324 |
| 25'-6" | 113 | 217 | 330 |
| 26'-0" | 113 | 224 | 337 |
| 26'-6" | 113 | 230 | 343 |
| 27'-0" | 113 | 236 | 349 |
| 27'-6" | 113 | 242 | 355 |
| 28'-0" | 113 | 249 | 362 |
| 28'-6" | 113 | 255 | 368 |
| 29'-0" | 113 | 261 [?read: looks like 267] | 374 |
| 29'-6" | 113 | 268 | 381 |
| 30'-0" | 113 | 274 | 387 |
| 30'-6" | 113 | 280 | 393 |
| 31'-0" | 113 | 286 | 399 |
| 31'-6" | 113 | 293 | 406 |
| 32'-0" | 113 | 299 | 412 |
| 32'-6" | 113 | 305 | 418 |
| 33'-0" | 113 | 312 | 425 |
| 33'-6" | 113 | 318 | 431 |
| 34'-0" | 113 | 324 | 437 |

Totals check (p.116): every total = 113 + Straight. At 29'-0" the Straight digit reads like 267, which would give 380, but the printed Total is 374 (→ 261); 29'-6" is 268/381. Either the scan misleads or there is a misprint; 261 fits the series (+6/+7 per 6").

### p.117 — COMPLETE CIRCLES 9"x4½"x2½" or 9"x4½"x3" CIRCLE BRICK — 4½-INCH LINING

Column headings are circle brick named by the inside–outside diameter range in inches, e.g. "9x4½x2½ (24-33)". Three tables on the page.

| Inside Diameter | (24-33) | (36-45) | (48-57) | (60-69) | (72-81) | Total |
|---|---|---|---|---|---|---|
| 2'-0" | 12 | … | … | … | … | 12 |
| 2'-6" | 7 | 7 | … | … | … | 14 |
| 3'-0" | … | 16 | … | … | … | 16 |
| 3'-6" | … | 9 | 9 | … | … | 18 |
| 4'-0" | … | … | 20 | … | … | 20 |
| 4'-6" | … | … | 11 | 11 | … | 22 |
| 5'-0" | … | … | … | 24 | … | 24 |
| 5'-6" | … | … | … | 13 | 14 | 27 |
| 6'-0" | … | … | … | … | 29 | 29 |

| Inside Diameter | (72-81) | (84-93) | (96-105) | (108-117) | (120-129) | Total |
|---|---|---|---|---|---|---|
| 6'-6" | 15 | 16 | … | … | … | 31 |
| 7'-0" | … | 33 | … | … | … | 33 |
| 7'-6" | … | 17 | 18 | … | … | 35 |
| 8'-0" | … | … | 37 | … | … | 37 |
| 8'-6" | … | … | 19 | 20 | … | 39 |
| 9'-0" | … | … | … | 41 | … | 41 |
| 9'-6" | … | … | … | 21 | 22 | 43 |
| 10'-0" | … | … | … | … | 45 | 45 |

| Inside Diameter | (120-129) | (132-141) | (144-153) | (156-165) | (168-177) | Total |
|---|---|---|---|---|---|---|
| 10'-6" | 23 | 24 | … | … | … | 47 |
| 11'-0" | … | 50 | … | … | … | 50 |
| 11'-6" | … | 26 | 26 | … | … | 52 |
| 12'-0" | … | … | 54 | … | … | 54 |
| 12'-6" | … | … | 28 | 28 | … | 56 |
| 13'-0" | … | … | … | 58 | … | 58 |
| 13'-6" | … | … | … | 30 | 30 | 60 |
| 14'-0" | … | … | … | … | 62 | 62 |

Totals check (p.117): all rows sum correctly. Note the 24" circle brick lays exactly 12 to the 2'-0" circle, consistent with p.102 (24" Circle, 12 brick).

## Image (13).jpg — catalogue p.118–119

### p.118 — COMPLETE CIRCLES 9"x6"x3", 12"x6"x3" or 13½"x6"x3" ARCH BRICK — 6-INCH LINING

Columns: No. 3 ARCH 9x6x(3-2); No. 2 ARCH 9x6x(3-2½); No. 1 ARCH 9x6x(3-2¾); STRAIGHT 9x6x3.

| Inside Diameter | No. 3 Arch | No. 2 Arch | No. 1 Arch | Straight | Total |
|---|---|---|---|---|---|
| 2'-0" | 38 | … | … | … | 38 |
| 2'-1" | 37 | 2 | … | … | 39 |
| 2'-2" | 36 | 4 | … | … | 40 |
| 2'-3" | 35 | 6 | … | … | 41 |
| 2'-4" | 34 | 8 | … | … | 42 |
| 2'-5" | 33 | 10 | … | … | 43 |
| 2'-6" | 32 | 12 | … | … | 44 |
| 2'-7" | 31 | 14 | … | … | 45 |
| 2'-8" | 30 | 16 | … | … | 46 |
| 2'-9" | 28 | 20 | … | … | 48 |
| 2'-10" | 27 | 22 | … | … | 49 |
| 2'-11" | 26 | 24 | … | … | 50 |
| 3'-0" | 25 | 26 | … | … | 51 |
| 3'-1" | 24 | 28 | … | … | 52 |
| 3'-2" | 23 | 30 | … | … | 53 |
| 3'-3" | 22 | 32 | … | … | 54 |
| 3'-4" | 21 | 34 | … | … | 55 |
| 3'-5" | 20 | 36 | … | … | 56 |
| 3'-6" | 19 | 38 | … | … | 57 |
| 3'-7" | 18 | 40 | … | … | 58 |
| 3'-8" | 17 | 42 | … | … | 59 |
| 3'-9" | 16 | 44 | … | … | 60 |
| 3'-10" | 15 | 46 | … | … | 61 |
| 3'-11" | 14 | 48 | … | … | 62 |
| 4'-0" | 13 | 50 | … | … | 63 |
| 4'-1" | 12 | 52 | … | … | 64 |
| 4'-2" | 11 | 54 | … | … | 65 |
| 4'-3" | 10 | 56 | … | … | 66 |
| 4'-4" | 9 | 58 | … | … | 67 |
| 4'-5" | 8 | 60 | … | … | 68 |
| 4'-6" | 6 | 64 | … | … | 70 |
| 4'-7" | 5 | 66 | … | … | 71 |
| 4'-8" | 4 | 68 | … | … | 72 |
| 4'-9" | 3 | 70 | … | … | 73 |
| 4'-10" | 2 | 72 | … | … | 74 |
| 4'-11" | 1 | 74 | … | … | 75 |
| 5'-0" | … | 76 | … | … | 76 |
| 5'-1" | … | 75 | 2 | … | 77 |
| 5'-2" | … | 74 | 4 | … | 78 |
| 5'-3" | … | 72 | 7 | … | 79 |
| 5'-4" | … | 71 | 9 | … | 80 |
| 5'-5" | … | 70 | 11 | … | 81 |
| 5'-6" | … | 69 | 13 | … | 82 |
| 5'-7" | … | 68 | 15 | … | 83 |
| 5'-8" | … | 67 | 17 | … | 84 |
| 5'-9" | … | 66 | 19 | … | 85 |
| 5'-10" | … | 65 | 21 | … | 86 |
| 5'-11" | … | 64 | 23 | … | 87 |
| 6'-0" | … | 63 | 25 | … | 88 |
| 6'-1" | … | 62 | 27 | … | 89 |

Totals check (p.118): all rows sum to the printed total. Continued Next Page.

### p.119 — continued (No. 3 Arch dotted/none on every row)

| Inside Diameter | No. 3 Arch | No. 2 Arch | No. 1 Arch | Straight | Total |
|---|---|---|---|---|---|
| 6'-2" | … | 61 | 29 | … | 90 |
| 6'-3" | … | 60 | 31 | … | 91 |
| 6'-4" | … | 58 | 35 | … | 93 |
| 6'-5" | … | 57 | 37 | … | 94 |
| 6'-6" | … | 56 | 39 | … | 95 |
| 6'-7" | … | 55 | 41 | … | 96 |
| 6'-8" | … | 54 | 43 | … | 97 |
| 6'-9" | … | 53 | 45 | … | 98 |
| 6'-10" | … | 52 | 47 | … | 99 |
| 6'-11" | … | 51 | 49 | … | 100 |
| 7'-0" | … | 50 | 51 | … | 101 |
| 7'-1" | … | 49 | 53 | … | 102 |
| 7'-2" | … | 48 | 55 | … | 103 |
| 7'-3" | … | 47 | 57 | … | 104 |
| 7'-4" | … | 46 | 59 | … | 105 |
| 7'-5" | … | 45 | 61 | … | 106 |
| 7'-6" | … | 44 | 63 | … | 107 |
| 7'-7" | … | 43 | 65 | … | 108 |
| 7'-8" | … | 42 | 67 | … | 109 |
| 7'-9" | … | 41 | 69 | … | 110 |
| 7'-10" | … | 40 | 71 | … | 111 |
| 7'-11" | … | 39 | 73 | … | 112 |
| 8'-0" | … | 38 | 75 | … | 113 |
| 8'-1" | … | 37 | 78 | … | 115 |
| 8'-2" | … | 36 | 80 | … | 116 |
| 8'-3" | … | 35 | 82 | … | 117 |
| 8'-4" | … | 34 | 84 | … | 118 |
| 8'-5" | … | 33 | 86 | … | 119 |
| 8'-6" | … | 32 | 88 | … | 120 |
| 8'-7" | … | 31 | 90 | … | 121 |
| 8'-8" | … | 30 | 92 | … | 122 |
| 8'-9" | … | 29 | 94 | … | 123 |
| 8'-10" | … | 27 | 97 | … | 124 |
| 8'-11" | … | 26 | 99 | … | 125 |
| 9'-0" | … | 25 | 101 | … | 126 |
| 9'-3" | … | 22 | 107 | … | 129 |
| 9'-6" | … | 19 | 113 | … | 132 |
| 9'-9" | … | 16 | 119 | … | 135 |
| 10'-0" | … | 13 | 126 | … | 139 |
| 10'-3" | … | 10 | 132 | … | 142 |
| 10'-6" | … | 6 | 139 | … | 145 |
| 10'-9" | … | 3 | 145 | … | 148 |
| 11'-0" | … | … | 151 | … | 151 |
| 11'-3" | … | … | 151 | 3 | 154 |
| 11'-6" | … | … | 151 | 6 | 157 |
| 11'-9" | … | … | 151 | 10 | 161 |
| 12'-0" | … | … | 151 | 13 | 164 |
| 12'-3" | … | … | 151 | 16 | 167 |
| 12'-6" | … | … | 151 | 19 | 170 |
| 12'-9" | … | … | 151 | 22 | 173 |

Totals check (p.119): all rows sum to the printed total.

## Image (14).jpg — catalogue p.120–121

### p.120 — COMPLETE CIRCLES 9"x6"x3½" ARCHES WITH 9"x6"x2½" STRAIGHTS — 6-INCH LINING

Columns: No. 3 ARCH 9x6x(3½-1½); No. 2 ARCH 9x6x(3½-2); No. 1 ARCH 9x6x(3½-2½); STRAIGHT 9x6x2½.

| Inside Diameter | No. 3 Arch | No. 2 Arch | No. 1 Arch | Straight | Total |
|---|---|---|---|---|---|
| 0'-9" | 19 | … | … | … | 19 |
| 0'-10" | 16 | 4 | … | … | 20 |
| 0'-11" | 13 | 8 | … | … | 21 |
| 1'-0" | 10 | 12 | … | … | 22 |
| 1'-1" | 7 | 16 | … | … | 23 |
| 1'-2" | 4 | 20 | … | … | 24 |
| 1'-3" | 1 | 24 | … | … | 25 |
| 1'-4" | … | 26 | … | … | 26 |
| 1'-5" | … | 24 | 2 | … | 26 |
| 1'-6" | … | 22 | 5 | … | 27 |
| 1'-7" | … | 20 | 8 | … | 28 |
| 1'-8" | … | 18 | 11 | … | 29 |
| 1'-9" | … | 16 | 14 | … | 30 |
| 1'-10" | … | 14 | 17 | … | 31 |
| 1'-11" | … | 12 | 20 | … | 32 |
| 2'-0" | … | 10 | 23 | … | 33 |
| 2'-1" | … | 8 | 26 | … | 34 |
| 2'-2" | … | 8 | 26 | … | 34 |
| 2'-3" | … | 6 | 29 | … | 35 |
| 2'-4" | … | 4 | 32 | … | 36 |
| 2'-5" | … | 2 | 35 | … | 37 |
| 2'-6" | … | … | 38 | … | 38 |
| 2'-7" | … | … | 38 | 1 | 39 |
| 2'-8" | … | … | 38 | 3 | 41 |
| 2'-9" | … | … | 38 | 4 | 42 |
| 2'-10" | … | … | 38 | 5 | 43 |
| 2'-11" | … | … | 38 | 6 | 44 |
| 3'-0" | … | … | 38 | 8 | 46 |
| 3'-1" | … | … | 38 | 9 | 47 |
| 3'-2" | … | … | 38 | 10 | 48 |
| 3'-3" | … | … | 38 | 11 | 49 |
| 3'-4" | … | … | 38 | 13 | 51 |
| 3'-5" | … | … | 38 | 14 | 52 |
| 3'-6" | … | … | 38 | 15 | 53 |
| 3'-8" | … | … | 38 | 18 | 56 |
| 3'-10" | … | … | 38 | 20 | 58 |
| 4'-0" | … | … | 38 | 23 | 61 |
| 4'-2" | … | … | 38 | 25 | 63 |
| 4'-4" | … | … | 38 | 28 | 66 |
| 4'-6" | … | … | 38 | 30 | 68 |
| 4'-8" | … | … | 38 | 33 | 71 |
| 4'-10" | … | … | 38 | 35 | 73 |
| 5'-0" | … | … | 38 | 38 | 76 |
| 5'-2" | … | … | 38 | 40 | 78 |
| 5'-4" | … | … | 38 | 43 | 81 |
| 5'-6" | … | … | 38 | 45 | 83 |
| 5'-8" | … | … | 38 | 48 | 86 |
| 5'-10" | … | … | 38 | 50 | 88 |
| 6'-0" | … | … | 38 | 53 | 91 |

Totals check (p.120): every printed total (19 … 91) agrees with the row sum; note 2'-1" and 2'-2" are both printed 8 / 26 / total 34. 2'-8" jumps by 2 straights (1→3), total 39→41, as printed.

### p.121 — COMPLETE CIRCLES 9"x6"x3½" ARCHES WITH 9"x6"x3" STRAIGHTS — 6-INCH LINING

Columns: No. 3 ARCH 9x6x(3½-1½); No. 2 ARCH 9x6x(3½-2); No. 1 ARCH 9x6x(3½-2½); STRAIGHT 9x6x3.

| Inside Diameter | No. 3 Arch | No. 2 Arch | No. 1 Arch | Straight | Total |
|---|---|---|---|---|---|
| 0'-9" | 19 | … | … | … | 19 |
| 0'-10" | 16 | 4 | … | … | 20 |
| 0'-11" | 13 | 8 | … | … | 21 |
| 1'-0" | 10 | 12 | … | … | 22 |
| 1'-1" | 7 | 16 | … | … | 23 |
| 1'-2" | 4 | 20 | … | … | 24 |
| 1'-3" | 1 | 24 | … | … | 25 |
| 1'-4" | … | 26 | … | … | 26 |
| 1'-5" | … | 24 | 2 | … | 26 |
| 1'-6" | … | 22 | 5 | … | 27 |
| 1'-7" | … | 20 | 8 | … | 28 |
| 1'-8" | … | 18 | 11 | … | 29 |
| 1'-9" | … | 16 | 14 | … | 30 |
| 1'-10" | … | 14 | 17 | … | 31 |
| 1'-11" | … | 12 | 20 | … | 32 |
| 2'-0" | … | 10 | 23 | … | 33 |
| 2'-1" | … | 8 | 26 | … | 34 |
| 2'-2" | … | 8 | 26 | … | 34 |
| 2'-3" | … | 6 | 29 | … | 35 |
| 2'-4" | … | 4 | 32 | … | 36 |
| 2'-5" | … | 2 | 35 | … | 37 |
| 2'-6" | … | … | 38 | … | 38 |
| 2'-7" | … | … | 38 | 1 | 39 |
| 2'-8" | … | … | 38 | 2 | 40 |
| 2'-9" | … | … | 38 | 3 | 41 |
| 2'-10" | … | … | 38 | 4 | 42 |
| 2'-11" | … | … | 38 | 5 | 43 |
| 3'-0" | … | … | 38 | 6 | 44 |
| 3'-1" | … | … | 38 | 7 | 45 |
| 3'-2" | … | … | 38 | 8 | 46 |
| 3'-3" | … | … | 38 | 9 | 47 |
| 3'-4" | … | … | 38 | 11 | 49 |
| 3'-5" | … | … | 38 | 12 | 50 |
| 3'-6" | … | … | 38 | 13 | 51 |
| 3'-8" | … | … | 38 | 15 | 53 |
| 3'-10" | … | … | 38 | 17 | 55 |
| 4'-0" | … | … | 38 | 19 | 57 |
| 4'-2" | … | … | 38 | 21 | 59 |
| 4'-4" | … | … | 38 | 23 | 61 |
| 4'-6" | … | … | 38 | 25 | 63 |
| 4'-8" | … | … | 38 | 27 | 65 |
| 4'-10" | … | … | 38 | 29 | 67 |
| 5'-0" | … | … | 38 | 31 | 69 |
| 5'-2" | … | … | 38 | 34 | 72 |
| 5'-4" | … | … | 38 | 36 | 74 |
| 5'-6" | … | … | 38 | 38 | 76 |
| 5'-8" | … | … | 38 | 40 | 78 |
| 5'-10" | … | … | 38 | 42 | 80 |
| 6'-0" | … | … | 38 | 44 | 82 |

Totals check (p.121): every printed total (19 … 82) agrees with the row sum. Rows down to 2'-6" are identical to p.120.

## Image (15).jpg — catalogue p.122–123

Small fractions in these two tables are printed very small; values are read as best possible and doubtful ones are marked. "Kiln size" = inside diameter. Block designations like (72-A-84) give inside–outside diameter in inches. The ⅔ and ¾ Split columns give the reduced-thickness splits (thick end – thin end) that go with each size.

### p.122 — COMPLETE CIRCLES 9"x6"x3" ARCH TYPE ROTARY KILN LINERS — 6-INCH LINING

| Kiln Size | Brick | Per Circle | ⅔ Split | ¾ Split |
|---|---|---|---|---|
| 7'-0" | 9x6x(3-2⁹⁄₁₆) (72-A-84) | 88 | (2-1²³⁄₃₂) | (2¼-1¹⁵⁄₁₆) |
| 7'-3" | 9x6x(3-2¹⁹⁄₃₂) (75-A-87) | 92 | (2-1²³⁄₃₂) | (2¼-1¹⁵⁄₁₆) |
| 7'-6" | 9x6x(3-2¹⁹⁄₃₂) (78-A-90) | 95 | (2-1²³⁄₃₂) | (2¼-1¹⁵⁄₁₆) |
| 7'-9" | 9x6x(3-2⅝) (81-A-93 [sic, no closing parenthesis] | 98 | (2-1¾) | (2¼-1³¹⁄₃₂) |
| 8'-0" | 9x6x(3-2⅝) (84-A-96) | 101 | (2-1¾) | (2¼-1³¹⁄₃₂) |
| 8'-3" | 9x6x(3-2⅝) (87-A-99) | 104 | (2-1¾) | (2¼-1³¹⁄₃₂) |
| 8'-6" | 9x6x(3-2²¹⁄₃₂) (90-A-102) | 107 | (2-1¾) | (2¼-2) |
| 8'-9" | 9x6x(3-2²¹⁄₃₂) (93-A-105) | 110 | (2-1²⁵⁄₃₂) | (2¼-2) |
| 9'-0" | 9x6x(3-2²¹⁄₃₂) (96-A-108) | 113 | (2-1²⁵⁄₃₂) | (2¼-2) |
| 9'-3" | 9x6x(3-2¹¹⁄₁₆) (99-A-111) | 117 | (2-1²⁵⁄₃₂) | (2¼-2) |
| 9'-6" | 9x6x(3-2¹¹⁄₁₆) (102-A-114) | 120 | (2-1²⁵⁄₃₂) | (2¼-2) |
| 9'-9" | 9x6x(3-2¹¹⁄₁₆) (105-A-117) | 123 | (2-1²⁵⁄₃₂) | (2¼-2¹⁄₃₂) |
| 10'-0" | 9x6x(3-2¹¹⁄₁₆) (108-A-120) | 126 | (2-1¹³⁄₁₆) | (2¼-2¹⁄₃₂) |
| 10'-3" | 9x6x(3-2²³⁄₃₂) (111-A-123) | 129 | (2-1¹³⁄₁₆) | (2¼-2¹⁄₃₂) |
| 10'-6" | 9x6x(3-2²³⁄₃₂) (114-A-126) | 132 | (2-1¹³⁄₁₆) | (2¼-2¹⁄₃₂) |
| 10'-9" | 9x6x(3-2²³⁄₃₂) (117-A-129) | 135 | (2-1¹³⁄₁₆) | (2¼-2¹⁄₃₂) |
| 11'-0" | 9x6x(3-2²³⁄₃₂) (120-A-132) | 139 | (2-1¹³⁄₁₆) | (2¼-2¹⁄₃₂) |
| 11'-3" | 9x6x(3-2²³⁄₃₂) (123-A-135) | 142 | (2-1¹³⁄₁₆) | (2¼-2¹⁄₁₆) |
| 11'-6" | 9x6x(3-2¾) (126-A-138) | 145 | (2-1¹³⁄₁₆) | (2¼-2¹⁄₁₆) |
| 11'-9" | 9x6x(3-2¾) (129-A-141) | 148 | (2-1²⁷⁄₃₂) | (2¼-2¹⁄₁₆) |
| 12'-0" | 9x6x(3-2¾) (132-A-144) | 151 | (2-1²⁷⁄₃₂) | (2¼-2¹⁄₁₆) |
| 12'-3" | 9x6x(3-2¾) (135-A-147) | 154 | (2-1²⁷⁄₃₂) | (2¼-2¹⁄₁₆) |
| 12'-6" | 9x6x(3-2¾) (138-A-150) | 157 | (2-1²⁷⁄₃₂) | (2¼-2¹⁄₁₆) |
| 12'-9" | 9x6x(3-2¾) (141-A-153) | 161 | (2-1²⁷⁄₃₂) | (2¼-2¹⁄₁₆) |
| 13'-0" | 9x6x(3-2²⁵⁄₃₂) (144-A-156) | 164 | (2-1²⁷⁄₃₂) | (2¼-2¹⁄₁₆) |
| 13'-3" | 9x6x(3-2²⁵⁄₃₂) (147-A-159) | 167 | (2-1²⁷⁄₃₂) | (2¼-2³⁄₃₂) |
| 13'-6" | 9x6x(3-2²⁵⁄₃₂) (150-A-162) | 170 | (2-1²⁷⁄₃₂) | (2¼-2³⁄₃₂) |
| 13'-9" | 9x6x(3-2²⁵⁄₃₂) (153-A-165) | 173 | (2-1²⁷⁄₃₂) | (2¼-2³⁄₃₂) |
| 14'-0" | 9x6x(3-2²⁵⁄₃₂) (156-A-168) | 176 | (2-1²⁷⁄₃₂) | (2¼-2³⁄₃₂) |

No totals printed. Fractions with 32nds are doubtful throughout [?read: small type]; the 7'-0" taper may read 2⁹⁄₁₆ or 2¹⁹⁄₃₂.

### p.123 — COMPLETE CIRCLES 9"x6"x3½" ARCH TYPE ROTARY KILN LINERS — 6-INCH LINING

| Kiln Size | Brick | Per Circle | ⅔ Split | ¾ Split |
|---|---|---|---|---|
| 7'-0" | 9x6x(3½-3) (72-A-84) | 76 | (2¹¹⁄₃₂-2) | (2⅝-2¼) |
| 7'-3" | 9x6x(3½-3¹⁄₃₂) (75-A-87) | 78 | (2¹¹⁄₃₂-2¹⁄₃₂) | (2⅝-2¼) |
| 7'-6" | 9x6x(3½-3¹⁄₃₂) (78-A-90) | 81 | (2¹¹⁄₃₂-2¹⁄₃₂) | (2⅝-2²⁹⁄₃₂) [sic? likely 2⅝-2⁹⁄₃₂] |
| 7'-9" | 9x6x(3½-3¹⁄₁₆) (81-A-93) | 84 | (2¹¹⁄₃₂-2¹⁄₃₂) | (2⅝-2²⁹⁄₃₂) [sic? likely 2⅝-2⁹⁄₃₂] |
| 8'-0" | 9x6x(3½-3¹⁄₁₆) (84-A-96) | 87 | (2¹¹⁄₃₂-2¹⁄₃₂) | (2⅝-2²⁹⁄₃₂) [sic? likely 2⅝-2⁹⁄₃₂] |
| 8'-3" | 9x6x(3½-3¹⁄₁₆) (87-A-99) | 89 | (2¹¹⁄₃₂-2¹⁄₁₆) | (2⅝-2⁵⁄₁₆) |
| 8'-6" | 9x6x(3½-3³⁄₃₂) (90-A-102) | 92 | (2¹¹⁄₃₂-2¹⁄₁₆) | (2⅝-2⁵⁄₁₆) |
| 8'-9" | 9x6x(3½-3³⁄₃₂) (93-A-105) | 95 | (2¹¹⁄₃₂-2¹⁄₁₆) | (2⅝-2⁵⁄₁₆) |
| 9'-0" | 9x6x(3½-3⅛) (96-A-108) | 97 | (2¹¹⁄₃₂-2¹⁄₁₆) | (2⅝-2¹¹⁄₃₂) |
| 9'-3" | 9x6x(3½-3⅛) (99-A-111) | 100 | (2¹¹⁄₃₂-2³⁄₃₂) | (2⅝-2¹¹⁄₃₂) |
| 9'-6" | 9x6x(3½-3⅛) (102-A-114) | 103 | (2¹¹⁄₃₂-2³⁄₃₂) | (2⅝-2¹¹⁄₃₂) |
| 9'-9" | 9x6x(3½-3⁵⁄₃₂) (105-A-117) | 105 | (2¹¹⁄₃₂-2³⁄₃₂) | (2⅝-2¹¹⁄₃₂) |
| 10'-0" | 9x6x(3½-3⁵⁄₃₂) (108-A-120) | 108 | (2¹¹⁄₃₂-2³⁄₃₂) | (2⅝-2⅜) |
| 10'-3" | 9x6x(3½-3⁵⁄₃₂) (111-A-123) | 111 | (2¹¹⁄₃₂-2³⁄₃₂) | (2⅝-2⅜) |
| 10'-6" | 9x6x(3½-3⁵⁄₃₂) (114-A-126) | 113 | (2¹¹⁄₃₂-2⅛) | (2⅝-2⅜) |
| 10'-9" | 9x6x(3½-3³⁄₁₆) (117-A-129) | 116 | (2¹¹⁄₃₂-2⅛) | (2⅝-2⅜) |
| 11'-0" | 9x6x(3½-3³⁄₁₆) (120-A-132) | 119 | (2¹¹⁄₃₂-2⅛) | (2⅝-2⅜) |
| 11'-3" | 9x6x(3½-3³⁄₁₆) (123-A-135) | 122 | (2¹¹⁄₃₂-2⅛) | (2⅝-2¹³⁄₃₂) |
| 11'-6" | 9x6x(3½-3³⁄₁₆) (126-A-138) | 124 | (2¹¹⁄₃₂-2⅛) | (2⅜-2¹³⁄₃₂) [sic? printed 2⅜, others 2⅝] |
| 11'-9" | 9x6x(3½-3³⁄₁₆) (129-A-141) | 127 | (2¹¹⁄₃₂-2⅛) | (2⅝-2¹³⁄₃₂) |
| 12'-0" | 9x6x(3½-3⁷⁄₃₂) (132-A-144) | 130 | (2¹¹⁄₃₂-2⅛) | (2⅝-2¹³⁄₃₂) |
| 12'-3" | 9x6x(3½-3⁷⁄₃₂) (135-A-147) | 132 | (2¹¹⁄₃₂-2⁵⁄₃₂) | (2⅝-2¹³⁄₃₂) |
| 12'-6" | 9x6x(3½-3⁷⁄₃₂) (138-A-150) | 135 | (2¹¹⁄₃₂-2⁵⁄₃₂) | (2⅝-2¹³⁄₃₂) |
| 12'-9" | 9x6x(3½-3⁷⁄₃₂) (141-A-153) | 138 | (2¹¹⁄₃₂-2⁵⁄₃₂) | (2⅝-2¹³⁄₃₂) |
| 13'-0" | 9x6x(3½-3⁷⁄₃₂) (144-A-156) | 140 | (2¹¹⁄₃₂-2⁵⁄₃₂) | (2⅝-2⁷⁄₁₆) |
| 13'-3" | 9x6x(3½-3¼) (147-A-159) | 143 | (2¹¹⁄₃₂-2⁵⁄₃₂) | (2⅝-2⁷⁄₁₆) |
| 13'-6" | 9x6x(3½-3¼) (150-A-162) | 146 | (2¹¹⁄₃₂-2⁵⁄₃₂) | (2⅝-2⁷⁄₁₆) |
| 13'-9" | 9x6x(3½-3¼) (153-A-165) | 149 | (2¹¹⁄₃₂-2⁵⁄₃₂) | (2⅝-2⁷⁄₁₆) |
| 14'-0" | 9x6x(3½-3¼) (156-A-168) | 151 | (2¹¹⁄₃₂-2⁵⁄₃₂) | (2⅝-2⁷⁄₁₆) |

No totals printed. The ¾ Split for 7'-6" to 8'-0" reads "2²⁹⁄₃₂", which is larger than the 2⅝ thick end and so can't be right; probably 2⁹⁄₃₂ [?read]. All 32nds on this page are doubtful.

## Summary

- **Edition, year, publisher:** no edition or year printed on any of these pages. Publisher: A. P. Green Refractories Co. Section title pages: "A. P. GREEN FIREBRICK SHAPES STANDARD AND SPECIAL" (b1) and "A. P. GREEN FIREBRICK COMBINATIONS For circular linings and arches" (b8).
- **Ring/circle brick counts:** p.102 (cupola blocks 6" lining; standard circle brick 4½" lining, 24"–120"); p.103 (cupola/Calliau blocks 4½" x 9", 16"–73" ID); p.111–113 (4½" lining, 9x4½x2½ arch brick, 0'-6" to 34'-0"); p.114–116 (4½" lining, 9x4½x3 arch brick, 0'-4½" to 34'-0"); p.117 (circle brick 9x4½x2½/3, 2'-0" to 14'-0"); p.118–119 (6" lining, 9x6x3 arch brick, 2'-0" to 12'-9"); p.120–121 (6" lining, 9x6x3½ arches with 2½" or 3" straights, 0'-9" to 6'-0"); p.122–123 (6" rotary kiln liners, 7'-0" to 14'-0").
- **Arch/key/wedge counts by span and rise:** none of the count tables are in these pages. p.109–110 index them: 4½" arches at 1½", 1.608", 2", 2.302" rise per foot of span (pp.164–171), 6" (pp.172–175), 9" (pp.176–191), 12"/13½"/15"/18" at 1.608" (pp.192–198).
- **Shape dimensions:** p.95–101 (9" straight, arch, wedge, key, skew, neck, split; 3" series; 9x6; large 9"; 9x9; 12x6; 13½"; square edge; shiplap); p.105 Greenclad door jamb; p.107 blast furnace keys.
- **Dome brick:** none in these pages.
- **Skewbacks:** p.106 (skews built from standard 9" brick for 4½" arch at 1½" and 2.302" rise and 9" arch at 2.302"; special skews 4160-A to F for 1.608", 2", 1½" rises, 4½"/6"/9" arches; table page refs). Also 60°/48° end and side skews on p.96, 98.
- **Formulas/rules:** no printed formulas. Stated rules: rise 1.608" per foot = central angle 60°, radius = span (p.106); tolerance ±2% on dimensions ≥ 4", 3% under 4" (p.104); overs up to 10% (p.104); no joint allowance in the tables, usually cut 1–2 brick per course (p.109).
- **Totals mismatches:** p.115, 4'-9" (44 + 25 = 69, printed 70); p.116, 29'-0" (Straight reads 267, total 374 implies 261). p.123 has an impossible ¾-split value printed as "2²⁹⁄₃₂". p.111 3'-3"–3'-9" No. 2 Arch cells were reconstructed from the totals.

---


Conventions: `…` = dotted leader (no brick of that shape) as printed. No edition/year/publisher line is printed on these pages unless noted. Each scan is a two-page spread, rotated 90° (read with the spine horizontal).

## Image (16).jpg — catalogue p.124–125

### p.124 — COMPLETE CIRCLES 9"x6"x4" ROTARY KILN BLOCKS — 6-INCH LINING

"SHAPES REQUIRED TO TURN CIRCLE". Column headings are shape sizes "9x6x4" with a range (e.g. 30-42); the ranges change in bands printed across the table. Here each band's six columns are given as C1–C6.

Band 1: C1 = 9x6x4 30-42, C2 = 36-48, C3 = 42-54, C4 = 48-60, C5 = 54-66, C6 = 60-72

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 3'-6" | 15 | … | … | … | … | … | 15 |
| 3'-9" | 8 | 8 | … | … | … | … | 16 |
| 4'-0" | … | 17 | … | … | … | … | 17 |
| 4'-3" | … | 9 | 9 | … | … | … | 18 |
| 4'-6" | … | … | 19 | … | … | … | 19 |
| 4'-9" | … | … | 10 | 10 | … | … | 20 |
| 5'-0" | … | … | … | 21 | … | … | 21 |
| 5'-3" | … | … | … | 11 | 11 | … | 22 |
| 5'-6" | … | … | … | … | 23 | … | 23 |
| 5'-9" | … | … | … | … | 12 | 12 | 24 |

Band 2: C1 = 60-72, C2 = 66-78, C3 = 72-84, C4 = 78-90, C5 = 84-96, C6 = 90-102

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 6'-0" | 26 | … | … | … | … | … | 26 |
| 6'-3" | 13 | 14 | … | … | … | … | 27 |
| 6'-6" | … | 28 | … | … | … | … | 28 |
| 6'-9" | … | 14 | 15 | … | … | … | 29 |
| 7'-0" | … | … | 30 | … | … | … | 30 |
| 7'-3" | … | … | 15 | 16 | … | … | 31 |
| 7'-6" | … | … | … | 32 | … | … | 32 |
| 7'-9" | … | … | … | 16 | 17 | … | 33 |
| 8'-0" | … | … | … | … | 34 | … | 34 |
| 8'-3" | … | … | … | … | 17 | 18 | 35 |

Band 3: C1 = 90-102, C2 = 96-108, C3 = 102-114, C4 = 108-120, C5 = 114-126, C6 = 120-132

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 8'-6" | 36 | … | … | … | … | … | 36 |
| 8'-9" | 18 | 19 | … | … | … | … | 37 |
| 9'-0" | … | 38 | … | … | … | … | 38 |
| 9'-3" | … | 19 | 20 | … | … | … | 39 |
| 9'-6" | … | … | 40 | … | … | … | 40 |
| 9'-9" | … | … | 20 | 21 | … | … | 41 |
| 10'-0" | … | … | … | 42 | … | … | 42 |
| 10'-3" | … | … | … | 21 | 22 | … | 43 |
| 10'-6" | … | … | … | … | 44 | … | 44 |
| 10'-9" | … | … | … | … | 22 | 23 | 45 |

Band 4: C1 = 120-132, C2 = 126-138, C3 = 132-144, C4 = 138-150, C5 = 144-156, C6 = (none printed)

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 11'-0" | 46 | … | … | … | … | … | 46 |
| 11'-3" | 24 | 24 | … | … | … | … | 48 |
| 11'-6" | … | 49 | … | … | … | … | 49 |
| 11'-9" | … | 25 | 25 | … | … | … | 50 |
| 12'-0" | … | … | 51 | … | … | … | 51 |
| 12'-3" | … | … | 26 | 26 | … | … | 52 |
| 12'-6" | … | … | … | 53 | … | … | 53 |
| 12'-9" | … | … | … | 27 | 27 | … | 54 |
| 13'-0" | … | … | … | … | 55 | … | 55 |

Totals checked: all rows sum to the printed total.

### p.125 — COMPLETE CIRCLES 9"x6"x4" ARCH TYPE ROTARY KILN BLOCKS — 6-INCH LINING

| Kiln size | KL-3-A 9x6x(4-3⅝) [?read: 3 5/16 per brand table below] | KL-2-A 9x6x(4-3½) | KL-1-A 9x6x(4-3 11/16) | Total |
|---|---|---|---|---|
| 5'-9" | 54 | … | … | 54 |
| 6'-0" | 50 | 7 | … | 57 |
| 6'-3" | 44 | 15 | … | 59 |
| 6'-6" | 38 | 24 | … | 62 |
| 6'-9" | 32 | 32 | … | 64 |
| 7'-0" | 25 | 41 | … | 66 |
| 7'-3" | 19 | 50 | … | 69 |
| 7'-6" | 13 | 58 | … | 71 |
| 7'-9" | 6 | 67 | … | 73 |
| 8'-0" | … | 76 | … | 76 |
| 8'-3" | … | 72 | 6 | 78 |
| 8'-6" | … | 68 | 13 | 81 |
| 8'-9" | … | 64 | 19 | 83 |
| 9'-0" | … | 60 | 25 | 85 |
| 9'-3" | … | 56 | 32 | 88 |
| 9'-6" | … | 52 | 38 | 90 |
| 9'-9" | … | 48 | 44 | 92 |
| 10'-0" | … | 44 | 51 | 95 |
| 10'-3" | … | 40 | 57 | 97 |
| 10'-6" | … | 36 | 63 | 99 |
| 10'-9" | … | 33 | 69 | 102 |
| 11'-0" | … | 28 | 76 | 104 |
| 11'-3" | … | 24 | 82 | 106 |
| 11'-6" | … | 21 | 88 | 109 |
| 11'-9" | … | 17 | 94 | 111 |
| 12'-0" | … | 13 | 100 | 113 |
| 12'-3" | … | 9 | 107 | 116 |
| 12'-6" | … | 5 | 113 | 118 |
| 12'-9" | … | 1 | 119 | 120 |

(Column header for KL-3-A printed as "9x6x(4-3⁵⁄₁₆)" [?read: 3 5/16].) Totals checked: all rows sum correctly.

Note (verbatim): "KL-4-A, 9x6x(3-2⅝), and KL-5-A, 9x6x(2²¹⁄₃₂-2¹¹⁄₃₂), may be used for keying each ring to avoid cutting last brick. Two of each should be ordered for each ring of full size liners."

Drawing: block 9" long, 6" wide, thickness "T" tapering to "A"; detail "METHOD OF MARKING THICK EDGE OF LINER" showing a ⅛" R notch and ¼" ø hole [?read], ½" [?read] dimension.

| Brand | "T" | "A" | Description |
|---|---|---|---|
| KL-1-A | 4" | 3 11/16" | FULL SIZE LINER |
| KL-2-A | 4" | 3½" | FULL SIZE LINER |
| KL-3-A | 4" | 3 5/16" | FULL SIZE LINER |

## Image (17).jpg — catalogue p.126–127

### p.126 — COMPLETE CIRCLES—BASIC BRICK ONLY, ROTARY KILN 9"x6"x3" ARCHES — 6-INCH LINING

Printed as one shape per row: shape designation "9x6x(3-x)A-(range)" and No. pieces per circle.

| Kiln size | Shape | No. pieces per circle |
|---|---|---|
| 7'-0" | 9x6x(3-2 9/16)A-(72-84) | 86 |
| 7'-3" | 9x6x(3-2 9/16)A-(75-87) | 89 |
| 7'-6" | 9x6x(3-2 19/32)A-(78-90) | 92 |
| 7'-9" | 9x6x(3-2 19/32)A-(81-93) | 95 |
| 8'-0" | 9x6x(3-2⅝)A-(84-96) | 98 |
| 8'-3" | 9x6x(3-2⅝)A-(87-99) | 102 |
| 8'-6" | 9x6x(3-2⅝)A-(90-102) | 105 |
| 8'-9" | 9x6x(3-2 21/32)A-(93-105) | 108 |
| 9'-0" | 9x6x(3-2 21/32)A-(96-108) | 111 |
| 9'-3" | 9x6x(3-2 21/32)A-(99-111) | 114 |
| 9'-6" | 9x6x(3-2 11/16)A-(102-114) | 117 |
| 9'-9" | 9x6x(3-2 11/16)A-(105-117) | 120 |
| 10'-0" | 9x6x(3-2 11/16)A-(108-120) | 123 |
| 10'-3" | 9x6x(3-2 11/16)A-(111-123) | 126 |
| 10'-6" | 9x6x(3-2 23/32)A-(114-126) | 129 |
| 10'-9" | 9x6x(3-2 23/32)A-(117-129) | 132 |
| 11'-0" | 9x6x(3-2 23/32)A-(120-132) | 135 |
| 11'-3" | 9x6x(3-2 23/32)A-(123-135) | 138 |
| 11'-6" | 9x6x(3-2 23/32)A-(126-138) | 142 |
| 11'-9" | 9x6x(3-2¾)A-(129-141) | 145 |
| 12'-0" | 9x6x(3-2¾)A-(132-144) | 148 |
| 12'-3" | 9x6x(3-2¾)A-(135-147) | 151 |
| 12'-6" | 9x6x(3-2¾)A-(138-150) | 154 |
| 12'-9" | 9x6x(3-2¾)A-(141-153) | 157 |
| 13'-0" | 9x6x(3-2¾)A-(144-156) | 160 |
| 13'-3" | 9x6x(3-2 25/32)A-(147-159) | 163 |
| 13'-6" | 9x6x(3-2 25/32)A-(150-162) | 166 |
| 13'-9" | 9x6x(3-2 25/32)A-(153-165) | 169 |
| 14'-0" | 9x6x(3-2 25/32)A-(156-168) | 172 |
| 14'-3" | 9x6x(3-2 25/32)A-(159-171) | 175 |
| 14'-6" | 9x6x(3-2 25/32)A-(162-174) | 178 |
| 14'-9" | 9x6x(3-2 25/32)A-(165-177) | 182 |
| 15'-0" | 9x6x(3-2 25/32)A-(168-180) | 185 |
| 15'-3" | 9x6x(3-2 13/16)A-(171-183) | 188 |
| 15'-6" | 9x6x(3-2 13/16)A-(174-186) | 191 |
| 15'-9" | 9x6x(3-2 13/16)A-(177-189) | 194 |
| 16'-0" | 9x6x(3-2 13/16)A-(180-192) | 197 |
| 16'-3" | 9x6x(3-2 13/16)A-(183-195) | 200 |
| 16'-6" | 9x6x(3-2 13/16)A-(186-198) | 203 |
| 16'-9" | 9x6x(3-2 13/16)A-(189-201) | 206 |
| 17'-0" | 9x6x(3-2 13/16)A-(192-204) | 209 |
| 17'-3" | 9x6x(3-2 13/16)A-(195-207) | 212 |
| 17'-6" | 9x6x(3-2 13/16)A-(198-210) | 215 |
| 17'-9" | 9x6x(3-2 13/16)A-(201-213) | 218 |
| 18'-0" | 9x6x(3-2 27/32)A-(204-216) | 222 |
| 18'-3" | 9x6x(3-2 27/32)A-(207-219) | 225 |
| 18'-6" | 9x6x(3-2 27/32)A-(210-222) | 228 |
| 18'-9" | 9x6x(3-2 27/32)A-(213-225) | 231 |
| 19'-0" | 9x6x(3-2 27/32)A-(216-228) | 234 |
| 19'-3" | 9x6x(3-2 27/32)A-(219-231) | 237 |
| 19'-6" | 9x6x(3-2 27/32)A-(222-234) | 240 |
| 19'-9" | 9x6x(3-2 27/32)A-(225-237) | 243 |
| 20'-0" | 9x6x(3-2 27/32)A-(228-240) | 246 |

(Small fractions on this page are tiny in the scan; the 32nds are [?read] where they fall between 2⅝ and 2 27/32, but they increase monotonically as transcribed.)

RING CLOSURE BRICK (p.126)

| Kiln diameter | Shape | No. per ring |
|---|---|---|
| 7'-0" To 13'-6" | RCA-1 9x6x(3½-3 5/32) [?read] | 1 |
| | RCA-2 9x6x(2¼-2 1/32) [?read] | 1 |
| Over 13'-6" | RCA-3 9x6x(3½-3 9/32) [?read] | 1 |
| | RCA-4 9x6x(2¼-2 3/32) [?read] | 1 |

(Which two RCA shapes belong to which diameter range is not explicit beyond the printed layout: the diameter labels sit beside the four-line list.)

### p.127 — COMPLETE CIRCLES—BASIC BRICK ONLY, ROTARY KILN 9"x6"x3½" ARCHES — 6-INCH LINING

| Kiln size | Shape | No. pieces per circle |
|---|---|---|
| 7'-0" | 9x6x(3½-3)A-(72-84) | 74 |
| 7'-3" | 9x6x(3½-3)A-(75-87) | 77 |
| 7'-6" | 9x6x(3½-3 1/32)A-(78-90) | 79 |
| 7'-9" | 9x6x(3½-3 1/32)A-(81-93) | 82 |
| 8'-0" | 9x6x(3½-3 1/16)A-(84-96) | 85 |
| 8'-3" | 9x6x(3½-3 1/16)A-(87-99) | 87 |
| 8'-6" | 9x6x(3½-3 3/32)A-(90-102) | 90 |
| 8'-9" | 9x6x(3½-3 3/32)A-(93-105) | 93 |
| 9'-0" | 9x6x(3½-3 3/32)A-(96-108) | 95 |
| 9'-3" | 9x6x(3½-3⅛)A-(99-111) | 98 |
| 9'-6" | 9x6x(3½-3⅛)A-(102-114) | 101 |
| 9'-9" | 9x6x(3½-3⅛)A-(105-117) | 103 |
| 10'-0" | 9x6x(3½-3 5/32)A-(108-120) | 106 |
| 10'-3" | 9x6x(3½-3 5/32)A-(111-123) | 109 |
| 10'-6" | 9x6x(3½-3 5/32)A-(114-126) | 111 |
| 10'-9" | 9x6x(3½-3 5/32)A-(117-129) | 114 |
| 11'-0" | 9x6x(3½-3 3/16)A-(120-132) | 116 |
| 11'-3" | 9x6x(3½-3 3/16)A-(123-135) | 119 |
| 11'-6" | 9x6x(3½-3 3/16)A-(126-138) | 122 |
| 11'-9" | 9x6x(3½-3 3/16)A-(129-141) | 124 |
| 12'-0" | 9x6x(3½-3 3/16)A-(132-144) | 127 |
| 12'-3" | 9x6x(3½-3 7/32)A-(135-147) | 130 |
| 12'-6" | 9x6x(3½-3 7/32)A-(138-150) | 132 |
| 12'-9" | 9x6x(3½-3 7/32)A-(141-153) | 135 |
| 13'-0" | 9x6x(3½-3 7/32)A-(144-156) | 138 |
| 13'-3" | 9x6x(3½-3 7/32)A-(147-159) | 140 |
| 13'-6" | 9x6x(3½-3¼)A-(150-162) | 143 |
| 13'-9" | 9x6x(3½-3¼)A-(153-165) | 146 |
| 14'-0" | 9x6x(3½-3¼)A-(156-168) | 148 |
| 14'-3" | 9x6x(3½-3¼)A-(159-171) | 151 |
| 14'-6" | 9x6x(3½-3¼)A-(162-174) | 154 |
| 14'-9" | 9x6x(3½-3¼)A-(165-177) | 156 |
| 15'-0" | 9x6x(3½-3¼)A-(168-180) | 159 |
| 15'-3" | 9x6x(3½-3 9/32)A-(171-183) | 161 |
| 15'-6" | 9x6x(3½-3 9/32)A-(174-186) | 164 |
| 15'-9" | 9x6x(3½-3 9/32)A-(177-189) | 167 |
| 16'-0" | 9x6x(3½-3 9/32)A-(180-192) | 169 |
| 16'-3" | 9x6x(3½-3 9/32)A-(183-195) | 172 |
| 16'-6" | 9x6x(3½-3 9/32)A-(186-198) | 175 |
| 16'-9" | 9x6x(3½-3 9/32)A-(189-201) | 177 |
| 17'-0" | 9x6x(3½-3 9/32)A-(192-204) | 180 |
| 17'-3" | 9x6x(3½-3 9/32)A-(195-207) | 183 |
| 17'-6" | 9x6x(3½-3 9/32)A-(198-210) | 185 |
| 17'-9" | 9x6x(3½-3 5/16)A-(201-213) | 188 |
| 18'-0" | 9x6x(3½-3 5/16)A-(204-216) | 191 |
| 18'-3" | 9x6x(3½-3 5/16)A-(207-219) | 193 |
| 18'-6" | 9x6x(3½-3 5/16)A-(210-222) | 196 |
| 18'-9" | 9x6x(3½-3 5/16)A-(213-225) | 199 |
| 19'-0" | 9x6x(3½-3 5/16)A-(216-228) | 201 |
| 19'-3" | 9x6x(3½-3 5/16)A-(219-231) | 204 |
| 19'-6" | 9x6x(3½-3 5/16)A-(222-234) | 206 |
| 19'-9" | 9x6x(3½-3 5/16)A-(225-237) | 209 |
| 20'-0" | 9x6x(3½-3 5/16)A-(228-240) | 212 |

(32nds [?read] as for p.126.)

RING CLOSURE BRICK (p.127)

| Kiln diameter | Shape | No. per ring |
|---|---|---|
| 7'-0" To 13'-6" | RCA-5 9x6x(3-2 11/16) [?read] | 1 |
| | RCA-2 9x6x(2¼-2 1/32) [?read] | 1 |
| Over 13'-6" | RCA-6 9x6x(3-2 13/16) [?read] | 1 |
| | RCA-4 9x6x(2¼-2 3/32) [?read] | 1 |

## Image (18).jpg — catalogue p.128–129

### COMPLETE CIRCLES 9"x4½"x2½", 9"x6¾"x2½" or 9"x9"x2½" WEDGE BRICK — 9-INCH LINING

Columns (SHAPES REQUIRED TO TURN CIRCLE): No. 2 Wedge 9x4½x(2½-1½); No. 1 Wedge 9x4½x(2½-1⅞); No. 1-X Wedge 9x4½x(2½-2¼); Straight 9x4½x2½; Total. Continues to p.130 ("Continued Next Page").

| Inside diameter | No. 2 | No. 1 | No. 1-X | Straight | Total |
|---|---|---|---|---|---|
| 2'-3" | 57 | … | … | … | 57 |
| 2'-4" | 55 | 3 | … | … | 58 |
| 2'-5" | 52 | 7 | … | … | 59 |
| 2'-6" | 51 | 10 | … | … | 61 |
| 2'-7" | 48 | 14 | … | … | 62 |
| 2'-8" | 46 | 17 | … | … | 63 |
| 2'-9" | 44 | 20 | … | … | 64 |
| 2'-10" | 42 | 24 | … | … | 66 |
| 2'-11" | 40 | 27 | … | … | 67 |
| 3'-0" | 38 | 30 | … | … | 68 |
| 3'-1" | 36 | 33 | … | … | 69 |
| 3'-2" | 34 | 37 | … | … | 71 |
| 3'-3" | 32 | 40 | … | … | 72 |
| 3'-4" | 29 | 44 | … | … | 73 |
| 3'-5" | 27 | 47 | … | … | 74 |
| 3'-6" | 25 | 51 | … | … | 76 |
| 3'-7" | 23 | 54 | … | … | 77 |
| 3'-8" | 21 | 57 | … | … | 78 |
| 3'-9" | 19 | [?read: 60] | … | … | 79 |
| 3'-10" | 17 | 64 | … | … | 81 |
| 3'-11" | 15 | 67 | … | … | 82 |
| 4'-0" | 13 | 70 | … | … | 83 |
| 4'-1" | 11 | 74 | … | … | 85 |
| 4'-2" | 9 | 77 | … | … | 86 |
| 4'-3" | 6 | 81 | … | … | 87 |
| 4'-4" | 4 | 84 | … | … | 88 |
| 4'-5" | 2 | 88 | … | … | 90 |
| 4'-6" | … | 91 | … | … | 91 |
| 4'-7" | … | 90 | 2 | … | 92 |
| 4'-8" | … | 89 | 4 | … | 93 |
| 4'-9" | … | 88 | 7 | … | 95 |
| 4'-10" | … | 87 | 9 | … | 96 |
| 4'-11" | … | 86 | 11 | … | 97 |
| 5'-0" | … | 85 | 13 | … | 98 |
| 5'-1" | … | 85 | 15 | … | 100 |
| 5'-2" | … | 84 | 17 | … | 101 |
| 5'-3" | … | 83 | 19 | … | 102 |
| 5'-4" | … | 82 | 21 | … | 103 |
| 5'-5" | … | 82 | 23 | … | 105 |
| 5'-6" | … | 81 | 25 | … | 106 |
| 5'-7" | … | 80 | 27 | … | 107 |
| 5'-8" | … | 79 | 29 | … | 108 |
| 5'-9" | … | 78 | 32 | … | 110 |
| 5'-10" | … | 77 | 34 | … | 111 |
| 5'-11" | … | 76 | 36 | … | 112 |
| 6'-0" | … | 75 | 38 | … | 113 |
| 6'-1" | … | 75 | 40 | … | 115 |
| 6'-2" | … | 74 | 42 | … | 116 |
| 6'-3" | … | 73 | 44 | … | 117 |
| 6'-4" | … | 72 | 46 | … | 118 |
| 6'-5" | … | 72 | 48 | … | 120 |
| 6'-6" | … | 71 | 50 | … | 121 |
| 6'-7" | … | 70 | 52 | … | 122 |
| 6'-8" | … | 69 | 54 | … | 123 |
| 6'-9" | … | 68 | 57 | … | 125 |
| 6'-10" | … | 67 | 59 | … | 126 |
| 6'-11" | … | 66 | 61 | … | 127 |
| 7'-0" | … | 65 | 63 | … | 128 |
| 7'-1" | … | 65 | 65 | … | 130 |
| 7'-2" | … | 64 | 67 | … | 131 |
| 7'-3" | … | 63 | 69 | … | 132 |
| 7'-4" | … | 62 | 72 | … | 134 |
| 7'-5" | … | 61 | 74 | … | 135 |
| 7'-6" | … | 60 | 76 | … | 136 |
| 7'-7" | … | 59 | 78 | … | 137 |
| 7'-8" | … | 59 | 80 | … | 139 |
| 7'-9" | … | 58 | 82 | … | 140 |
| 7'-10" | … | 57 | 84 | … | 141 |
| 7'-11" | … | 56 | 86 | … | 142 |
| 8'-0" | … | 56 | 88 | … | 144 |
| 8'-1" | … | 55 | 90 | … | 145 |
| 8'-2" | … | 54 | 92 | … | 146 |
| 8'-3" | … | 53 | 94 | … | 147 |
| 8'-4" | … | 52 | 97 | … | 149 |
| 8'-5" | … | 51 | 99 | … | 150 |
| 8'-6" | … | 50 | 101 | … | 151 |
| 8'-7" | … | 49 | 103 | … | 152 |
| 8'-8" | … | 49 | 105 | … | 154 |
| 8'-9" | … | 48 | 107 | … | 155 |
| 8'-10" | … | 47 | 109 | … | 156 |
| 8'-11" | … | 46 | 111 | … | 157 |
| 9'-0" | … | 46 | 113 | … | 159 |
| 9'-1" | … | 45 | 115 | … | 160 |
| 9'-2" | … | 44 | 117 | … | 161 |
| 9'-3" | … | 43 | 119 | … | 162 |
| 9'-4" | … | 42 | 122 | … | 164 |
| 9'-5" | … | 41 | 124 | … | 165 |
| 9'-6" | … | 40 | 126 | … | 166 |
| 9'-7" | … | 39 | 128 | … | 167 |
| 9'-8" | … | 39 | 130 | … | 169 |
| 9'-9" | … | 38 | 132 | … | 170 |
| 9'-10" | … | 37 | 134 | … | 171 |
| 9'-11" | … | 36 | 136 | … | 172 |
| 10'-0" | … | 35 | 139 | … | 174 |
| 10'-1" | … | 35 | 140 | … | 175 |
| 10'-2" | … | 34 | 142 | … | 176 |
| 10'-3" | … | 33 | 144 | … | 177 |
| 10'-4" | … | 32 | 147 | … | 179 |
| 10'-5" | … | 31 | 149 | … | 180 |
| 10'-6" | … | 30 | 151 | … | 181 |
| 10'-7" | … | 30 | 153 | … | 183 |
| 10'-8" | … | 29 | 155 | … | 184 |

(p.128 ends at 6'-5"; p.129 runs 6'-6" to 10'-8".) Totals check: all rows sum to the printed total, except 3'-9", where the No. 1 figure looks like "62" in the scan (19 + 62 = 81 ≠ 79); the sequence and the total both point to 60, so it is marked doubtful.

## Image (19).jpg — catalogue p.130–131

### p.130 — continuation of the 9"x4½"x2½", 9"x6¾"x2½" or 9"x9"x2½" WEDGE BRICK table — 9-INCH LINING

| Inside diameter | No. 2 | No. 1 | No. 1-X | Straight 9x4½x2½ | Total |
|---|---|---|---|---|---|
| 10'-9" | … | 28 | 157 | … | 185 |
| 10'-10" | … | 27 | 159 | … | 186 |
| 10'-11" | … | 26 | 162 | … | 188 |
| 11'-0" | … | 25 | 164 | … | 189 |
| 11'-1" | … | 24 | 166 | … | 190 |
| 11'-2" | … | 23 | 168 | … | 191 |
| 11'-3" | … | 23 | 170 | … | 193 |
| 11'-4" | … | 22 | 172 | … | 194 |
| 11'-5" | … | 21 | 174 | … | 195 |
| 11'-6" | … | 20 | 176 | … | 196 |
| 11'-7" | … | 20 | 178 | … | 198 |
| 11'-8" | … | 19 | 180 | … | 199 |
| 11'-9" | … | 18 | 182 | … | 200 |
| 11'-10" | … | 17 | 184 | … | 201 |
| 11'-11" | … | 16 | 187 | … | 203 |
| 12'-0" | … | 15 | 189 | … | 204 |
| 12'-1" | … | 14 | 191 | … | 205 |
| 12'-2" | … | 13 | 193 | … | 206 |
| 12'-3" | … | 13 | 195 | … | 208 |
| 12'-4" | … | 12 | 197 | … | 209 |
| 12'-5" | … | 11 | 199 | … | 210 |
| 12'-6" | … | 10 | 201 | … | 211 |
| 12'-7" | … | 10 | 203 | … | 213 |
| 12'-8" | … | 9 | 205 | … | 214 |
| 12'-9" | … | 8 | 207 | … | 215 |
| 12'-10" | … | 7 | 209 | … | 216 |
| 12'-11" | … | 6 | 212 | … | 218 |
| 13'-0" | … | 5 | 214 | … | 219 |
| 13'-1" | … | 4 | 216 | … | 220 |
| 13'-2" | … | 3 | 218 | … | 221 |
| 13'-3" | … | 3 | 220 | … | 223 |
| 13'-4" | … | 2 | 222 | … | 224 |
| 13'-5" | … | 1 | 224 | … | 225 |
| 13'-6" | … | … | 227 | … | 227 |
| 14'-0" | … | … | 227 | 7 | 234 |
| 14'-6" | … | … | 227 | 15 | 242 |
| 15'-0" | … | … | 227 | 22 | 249 |
| 15'-6" | … | … | 227 | 30 | 257 |
| 16'-0" | … | … | 227 | 37 | 264 |
| 16'-6" | … | … | 227 | 45 | 272 |
| 17'-0" | … | … | 227 | 52 | 279 |
| 17'-6" | … | … | 227 | 60 | 287 |
| 18'-0" | … | … | 227 | 67 | 294 |
| 18'-6" | … | … | 227 | 75 | 302 |
| 19'-0" | … | … | 227 | 82 | 309 |
| 19'-6" | … | … | 227 | 90 | 317 |
| 20'-0" | … | … | 227 | 98 | 325 |
| 20'-6" | … | … | 227 | 105 | 332 |
| 21'-0" | … | … | 227 | 113 | 340 |

Totals checked: all rows sum correctly.

### p.131 — COMPLETE CIRCLES 9"x4½"x3", 9"x6"x3", 9"x6¾"x3", or 9"x9"x3" WEDGE BRICK — 9-INCH LINING

Columns: No. 3 Wedge 9x4½x(3-2); No. 2 Wedge 9x4½x(3-2½); No. 1 Wedge 9x4½x(3-2¾); Straight 9x4½x3; Total. Continues to p.132.

| Inside diameter | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|
| 3'-0" | 57 | … | … | … | 57 |
| 3'-1" | 56 | 2 | … | … | 58 |
| 3'-2" | 55 | 4 | … | … | 59 |
| 3'-3" | 54 | 6 | … | … | 60 |
| 3'-4" | 52 | 9 | … | … | 61 |
| 3'-5" | 51 | 11 | … | … | 62 |
| 3'-6" | 50 | 13 | … | … | 63 |
| 3'-7" | 49 | 15 | … | … | 64 |
| 3'-8" | 48 | 17 | … | … | 65 |
| 3'-9" | 47 | 19 | … | … | 66 |
| 3'-10" | 46 | 21 | … | … | 67 |
| 3'-11" | 45 | 23 | … | … | 68 |
| 4'-0" | 44 | 25 | … | … | 69 |
| 4'-1" | 43 | 27 | … | … | 70 |
| 4'-2" | 42 | 30 | … | … | 72 |
| 4'-3" | 41 | 32 | … | … | 73 |
| 4'-4" | 40 | 34 | … | … | 74 |
| 4'-5" | 39 | 36 | … | … | 75 |
| 4'-6" | 38 | 38 | … | … | 76 |
| 4'-7" | 37 | 40 | … | … | 77 |
| 4'-8" | 36 | 42 | … | … | 78 |
| 4'-9" | 35 | 44 | … | … | 79 |
| 4'-10" | 34 | 46 | … | … | 80 |
| 4'-11" | 33 | 48 | … | … | 81 |
| 5'-0" | 32 | 50 | … | … | 82 |
| 5'-1" | 31 | 52 | … | … | 83 |
| 5'-2" | 29 | 55 | … | … | 84 |
| 5'-3" | 28 | 57 | … | … | 85 |
| 5'-4" | 27 | 59 | … | … | 86 |
| 5'-5" | 26 | 61 | … | … | 87 |
| 5'-6" | 25 | 63 | … | … | 88 |
| 5'-7" | 24 | 65 | … | … | 89 |
| 5'-8" | 23 | 67 | … | … | 90 |
| 5'-9" | 22 | 69 | … | … | 91 |
| 5'-10" | 21 | 71 | … | … | 92 |
| 5'-11" | 20 | 74 | … | … | 94 |
| 6'-0" | 19 | 76 | … | … | 95 |
| 6'-1" | 18 | 78 | … | … | 96 |
| 6'-2" | 17 | 80 | … | … | 97 |
| 6'-3" | 16 | 82 | … | … | 98 |
| 6'-4" | 15 | 84 | … | … | 99 |
| 6'-5" | 14 | 86 | … | … | 100 |
| 6'-6" | 13 | 88 | … | … | 101 |
| 6'-7" | 12 | 90 | … | … | 102 |
| 6'-8" | 11 | 92 | … | … | 103 |
| 6'-9" | 10 | 94 | … | … | 104 |
| 6'-10" | 9 | 96 | … | … | 105 |
| 6'-11" | 7 | 99 | … | … | 106 |
| 7'-0" | 6 | 101 | … | … | 107 |
| 7'-1" | 5 | 103 | … | … | 108 |

Totals checked: all rows sum correctly.

## Image (20).jpg — catalogue p.132–133

### continuation of the 9"x4½"x3", 9"x6"x3", 9"x6¾"x3", or 9"x9"x3" WEDGE BRICK table — 9-INCH LINING

| Inside diameter | No. 3 | No. 2 | No. 1 | Straight 9x4½x3 | Total |
|---|---|---|---|---|---|
| 7'-2" | 4 | 105 | … | … | 109 |
| 7'-3" | 3 | 107 | … | … | 110 |
| 7'-4" | 2 | 109 | … | … | 111 |
| 7'-5" | 1 | 111 | … | … | 112 |
| 7'-6" | … | 113 | … | … | 113 |
| 7'-7" | … | 112 | 2 | … | 114 |
| 7'-8" | … | 111 | 5 | … | 116 |
| 7'-9" | … | 110 | 7 | … | 117 |
| 7'-10" | … | 109 | 9 | … | 118 |
| 7'-11" | … | 108 | 11 | … | 119 |
| 8'-0" | … | 107 | 13 | … | 120 |
| 8'-1" | … | 106 | 15 | … | 121 |
| 8'-2" | … | 105 | 17 | … | 122 |
| 8'-3" | … | 104 | 19 | … | 123 |
| 8'-4" | … | 103 | 21 | … | 124 |
| 8'-5" | … | 102 | 23 | … | 125 |
| 8'-6" | … | 101 | 25 | … | 126 |
| 8'-7" | … | 100 | 27 | … | 127 |
| 8'-8" | … | 99 | 29 | … | 128 |
| 8'-9" | … | 97 | 32 | … | 129 |
| 8'-10" | … | 96 | 34 | … | 130 |
| 8'-11" | … | 95 | 36 | … | 131 |
| 9'-0" | … | 94 | 38 | … | 132 |
| 9'-1" | … | 93 | 40 | … | 133 |
| 9'-2" | … | 92 | 42 | … | 134 |
| 9'-3" | … | 91 | 44 | … | 135 |
| 9'-4" | … | 90 | 46 | … | 136 |
| 9'-5" | … | 89 | 49 | … | 138 |
| 9'-6" | … | 88 | 51 | … | 139 |
| 9'-7" | … | 87 | 53 | … | 140 |
| 9'-8" | … | 86 | 55 | … | 141 |
| 9'-9" | … | 85 | 57 | … | 142 |
| 9'-10" | … | 84 | 59 | … | 143 |
| 9'-11" | … | 83 | 61 | … | 144 |
| 10'-0" | … | 82 | 63 | … | 145 |
| 10'-1" | … | 81 | 65 | … | 146 |
| 10'-2" | … | 80 | 67 | … | 147 |
| 10'-3" | … | 79 | 69 | … | 148 |
| 10'-4" | … | 78 | 71 | … | 149 |
| 10'-5" | … | 77 | 73 | … | 150 |
| 10'-6" | … | 76 | 75 | … | 151 |
| 10'-7" | … | 74 | 78 | … | 152 |
| 10'-8" | … | 73 | 80 | … | 153 |
| 10'-9" | … | 72 | 82 | … | 154 |
| 10'-10" | … | 71 | 84 | … | 155 |
| 10'-11" | … | 70 | 86 | … | 156 |
| 11'-0" | … | 69 | 88 | … | 157 |
| 11'-1" | … | 69 | 89 | … | 158 |
| 11'-2" | … | 67 | 93 | … | 160 |
| 11'-3" | … | 66 | 95 | … | 161 |
| 11'-4" | … | 65 | 97 | … | 162 |
| 11'-5" | … | 64 | 99 | … | 163 |
| 11'-6" | … | 63 | 101 | … | 164 |
| 11'-8" | … | 61 | 105 | … | 166 |
| 11'-10" | … | 59 | 109 | … | 168 |
| 12'-0" | … | 57 | 113 | … | 170 |
| 12'-2" | … | 55 | 117 | … | 172 |
| 12'-4" | … | 52 | 122 | … | 174 |
| 12'-6" | … | 50 | 126 | … | 176 |
| 12'-8" | … | 48 | 130 | … | 178 |
| 12'-10" | … | 47 | 133 | … | 180 |
| 13'-0" | … | 44 | 139 | … | 183 |
| 13'-2" | … | 42 | 143 | … | 185 |
| 13'-4" | … | 40 | 147 | … | 187 |
| 13'-6" | … | 38 | 151 | … | 189 |
| 13'-8" | … | 36 | 155 | … | 191 |
| 13'-10" | … | 34 | 159 | … | 193 |
| 14'-0" | … | 32 | 163 | … | 195 |
| 14'-2" | … | 29 | 168 | … | 197 |
| 14'-4" | … | 27 | 172 | … | 199 |
| 14'-6" | … | 25 | 176 | … | 201 |
| 14'-8" | … | 23 | 180 | … | 203 |
| 14'-10" | … | 21 | 185 | … | 206 |
| 15'-0" | … | 19 | 189 | … | 208 |
| 15'-2" | … | 17 | 193 | … | 210 |
| 15'-4" | … | 15 | 197 | … | 212 |
| 15'-6" | … | 13 | 201 | … | 214 |
| 15'-8" | … | 11 | 205 | … | 216 |
| 15'-10" | … | 8 | 210 | … | 218 |
| 16'-0" | … | 6 | 214 | … | 220 |
| 16'-2" | … | 4 | 218 | … | 222 |
| 16'-4" | … | 2 | 222 | … | 224 |
| 16'-6" | … | … | 226 | … | 226 |
| 17'-0" | … | … | 226 | 7 | 233 |
| 17'-6" | … | … | 226 | 13 | 239 |
| 18'-0" | … | … | 226 | 19 | 245 |
| 18'-6" | … | … | 226 | 26 | 252 |
| 19'-0" | … | … | 226 | 32 | 258 |
| 19'-6" | … | … | 226 | 38 | 264 |
| 20'-0" | … | … | 226 | 44 | 270 |
| 20'-6" | … | … | 226 | 51 | 277 |
| 21'-0" | … | … | 226 | 57 | 283 |

(p.132 ends at 11'-3"; p.133 from 11'-4", in 2" steps, then 6" steps from 16'-6".) Totals checked: all rows sum correctly. (At 11'-1" No. 2 is printed 69, the same as 11'-0"; 69 + 89 = 158 matches the total.)

## Image (21).jpg — catalogue p.134–135

### COMPLETE CIRCLES 9"x4½"x2½" or 9"x4½"x3" KEY BRICK — 9-INCH LINING

Columns: No. 4 Key 9x(4½-2¼)x2½; No. 3 Key 9x(4½-3)x2½; No. 2 Key 9x(4½-3½)x2½; No. 1 Key 9x(4½-4)x2½; Straight 9x4½x2½; Total.

| Inside diameter | No. 4 | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|
| 1'-6" | 25 | … | … | … | … | 25 |
| 1'-8" | 23 | 4 | … | … | … | 27 |
| 1'-10" | 20 | 8 | … | … | … | 28 |
| 2'-0" | 17 | 13 | … | … | … | 30 |
| 2'-2" | 14 | 17 | … | … | … | 31 |
| 2'-4" | 11 | 21 | … | … | … | 32 |
| 2'-6" | 9 | 25 | … | … | … | 34 |
| 2'-8" | 6 | 29 | … | … | … | 35 |
| 2'-10" | 3 | 34 | … | … | … | 37 |
| 3'-0" | … | 38 | … | … | … | 38 |
| 3'-2" | … | 35 | 4 | … | … | 39 |
| 3'-4" | … | 32 | 9 | … | … | 41 |
| 3'-6" | … | 29 | 13 | … | … | 42 |
| 3'-8" | … | 27 | 17 | … | … | 44 |
| 3'-10" | … | 24 | 21 | … | … | 45 |
| 4'-0" | … | 21 | 25 | … | … | 46 |
| 4'-2" | … | 18 | 30 | … | … | 48 |
| 4'-4" | … | 15 | 34 | … | … | 49 |
| 4'-6" | … | 13 | 38 | … | … | 51 |
| 4'-8" | … | 10 | 42 | … | … | 52 |
| 4'-10" | … | 7 | 46 | … | … | 53 |
| 5'-0" | … | 4 | 51 | … | … | 55 |
| 5'-2" | … | 1 | 55 | … | … | 56 |
| 5'-3" | … | … | 57 | … | … | 57 |
| 5'-4" | … | … | 56 | 2 | … | 58 |
| 5'-6" | … | … | 55 | 4 | … | 59 |
| 5'-8" | … | … | 53 | 7 | … | 60 |
| 5'-10" | … | … | 52 | 10 | … | 62 |
| 6'-0" | … | … | 50 | 13 | … | 63 |
| 6'-2" | … | … | 49 | 16 | … | 65 |
| 6'-4" | … | … | 48 | 18 | … | 66 |
| 6'-6" | … | … | 46 | 21 | … | 67 |
| 6'-8" | … | … | 45 | 24 | … | 69 |
| 6'-10" | … | … | 43 | 27 | … | 70 |
| 7'-0" | … | … | 42 | 30 | … | 72 |
| 7'-2" | … | … | 41 | 32 | … | 73 |
| 7'-4" | … | … | 39 | 35 | … | 74 |
| 7'-6" | … | … | 38 | 38 | … | 76 |
| 7'-8" | … | … | 36 | 41 | … | 77 |
| 7'-10" | … | … | 35 | 44 | … | 79 |
| 8'-0" | … | … | 34 | 46 | … | 80 |
| 8'-2" | … | … | 32 | 49 | … | 81 |
| 8'-4" | … | … | 31 | 52 | … | 83 |
| 8'-6" | … | … | 29 | 55 | … | 84 |
| 8'-8" | … | … | 28 | 57 | … | 85 |
| 8'-10" | … | … | 27 | 60 | … | 87 |
| 9'-0" | … | … | 25 | 63 | … | 88 |
| 9'-2" | … | … | 24 | 66 | … | 90 |
| 9'-4" | … | … | 22 | 69 | … | 91 |
| 9'-6" | … | … | 21 | 71 | … | 92 |
| 9'-8" | … | … | 20 | 74 | … | 94 |
| 9'-10" | … | … | 18 | 77 | … | 95 |
| 10'-0" | … | … | 17 | 80 | … | 97 |
| 10'-2" | … | … | 15 | 83 | … | 98 |
| 10'-4" | … | … | 14 | 86 | … | 100 |
| 10'-6" | … | … | 13 | 88 | … | 101 |
| 10'-8" | … | … | 11 | 91 | … | 102 |
| 10'-10" | … | … | 10 | 94 | … | 104 |
| 11'-0" | … | … | 9 | 96 | … | 105 |
| 11'-2" | … | … | 7 | 100 | … | 107 |
| 11'-4" | … | … | 6 | 102 | … | 108 |
| 11'-6" | … | … | 4 | 105 | … | 109 |
| 11'-8" | … | … | 3 | 108 | … | 111 |
| 11'-10" | … | … | 2 | 110 | … | 112 |
| 12'-0" | … | … | … | 113 | … | 113 |
| 12'-6" | … | … | … | 113 | 5 | 118 |
| 13'-0" | … | … | … | 113 | 9 | 122 |
| 13'-6" | … | … | … | 113 | 13 | 126 |
| 14'-0" | … | … | … | 113 | 17 | 130 |
| 14'-6" | … | … | … | 113 | 21 | 134 |
| 15'-0" | … | … | … | 113 | 26 | 139 |
| 15'-6" | … | … | … | 113 | 30 | 143 |
| 16'-0" | … | … | … | 113 | 34 | 147 |
| 16'-6" | … | … | … | 113 | 38 | 151 |
| 17'-0" | … | … | … | 113 | 42 | 155 |
| 17'-6" | … | … | … | 113 | 46 | 159 |
| 18'-0" | … | … | … | 113 | 51 | 164 |
| 18'-6" | … | … | … | 113 | 55 | 168 |
| 19'-0" | … | … | … | 113 | 59 | 172 |
| 19'-6" | … | … | … | 113 | 63 | 176 |
| 20'-0" | … | … | … | 113 | 67 | 180 |
| 20'-6" | … | … | … | 113 | 72 | 185 |
| 21'-0" | … | … | … | 113 | 76 | 189 |
| 21'-6" | … | … | … | 113 | 80 | 193 |
| 22'-0" | … | … | … | 113 | 84 | 197 |
| 22'-6" | … | … | … | 113 | 88 | 201 |
| 23'-0" | … | … | … | 113 | 93 | 206 |
| 23'-6" | … | … | … | 113 | 97 | 210 |
| 24'-0" | … | … | … | 113 | 101 | 214 |
| 24'-6" | … | … | … | 113 | 105 | 218 |
| 25'-0" | … | … | … | 113 | 109 | 222 |
| 25'-6" | … | … | … | 113 | 114 | 227 |
| 26'-0" | … | … | … | 113 | 118 | 231 |
| 26'-6" | … | … | … | 113 | 122 | 235 |
| 27'-0" | … | … | … | 113 | 126 | 239 |
| 27'-6" | … | … | … | 113 | 130 | 243 |
| 28'-0" | … | … | … | 113 | 134 | 247 |
| 28'-6" | … | … | … | 113 | 139 | 252 |
| 29'-0" | … | … | … | 113 | 143 | 256 |
| 29'-6" | … | … | … | 113 | 147 | 260 |
| 30'-0" | … | … | … | 113 | 151 | 264 |

(p.134 runs 1'-6" to 9'-8"; p.135 from 9'-10".) Totals checked: all rows sum correctly.

## Image (22).jpg — catalogue p.136–137

### COMPLETE CIRCLES 9"x6"x2½" or 9"x6"x3" KEY BRICK — 9-INCH LINING

Columns: No. 3 Key 9x(6-3)x2½; No. 2-X Key 9x(6-4)x2½; No. 2 Key 9x(6-4 13/16)x2½; No. 1 Key 9x(6-5⅜)x2½; Straight 9x6x2½; Total. Continues to p.138.

| Inside diameter | No. 3 | No. 2-X | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|
| 1'-6" | 19 | … | … | … | … | 19 |
| 1'-7" | 18 | 2 | … | … | … | 20 |
| 1'-8" | 17 | 3 | … | … | … | 20 |
| 1'-9" | 16 | 5 | … | … | … | 21 |
| 1'-10" | 15 | 6 | … | … | … | 21 |
| 1'-11" | 14 | 8 | … | … | … | 22 |
| 2'-0" | 13 | 9 | … | … | … | 22 |
| 2'-1" | 12 | 11 | … | … | … | 23 |
| 2'-2" | 11 | 12 | … | … | … | 23 |
| 2'-3" | 10 | 14 | … | … | … | 24 |
| 2'-4" | 9 | 15 | … | … | … | 24 |
| 2'-5" | 8 | 17 | … | … | … | 25 |
| 2'-6" | 7 | 18 | … | … | … | 25 |
| 2'-7" | 5 | 21 | … | … | … | 26 |
| 2'-8" | 5 | 22 | … | … | … | 27 |
| 2'-9" | 3 | 24 | … | … | … | 27 |
| 2'-10" | 2 | 26 | … | … | … | 28 |
| 2'-11" | 1 | 27 | … | … | … | 28 |
| 3'-0" | … | 29 | … | … | … | 29 |
| 3'-1" | … | 28 | 1 | … | … | 29 |
| 3'-2" | … | 27 | 3 | … | … | 30 |
| 3'-3" | … | 26 | 4 | … | … | 30 |
| 3'-4" | … | 26 | 5 | … | … | 31 |
| 3'-5" | … | 25 | 6 | … | … | 31 |
| 3'-6" | … | 24 | 8 | … | … | 32 |
| 3'-7" | … | 23 | 9 | … | … | 32 |
| 3'-8" | … | 22 | 11 | … | … | 33 |
| 3'-9" | … | 21 | 12 | … | … | 33 |
| 3'-10" | … | 21 | 13 | … | … | 34 |
| 3'-11" | … | 20 | 14 | … | … | 34 |
| 4'-0" | … | 19 | 16 | … | … | 35 |
| 4'-1" | … | 18 | 17 | … | … | 35 |
| 4'-2" | … | 18 | 18 | … | … | 36 |
| 4'-3" | … | 17 | 19 | … | … | 36 |
| 4'-4" | … | 16 | 21 | … | … | 37 |
| 4'-5" | … | 16 | 22 | … | … | 38 |
| 4'-6" | … | 15 | 23 | … | … | 38 |
| 4'-7" | … | 14 | 25 | … | … | 39 |
| 4'-8" | … | 13 | 26 | … | … | 39 |
| 4'-9" | … | 13 | 27 | … | … | 40 |
| 4'-10" | … | 12 | 28 | … | … | 40 |
| 4'-11" | … | 11 | 30 | … | … | 41 |
| 5'-0" | … | 10 | 31 | … | … | 41 |
| 5'-1" | … | 9 | 33 | … | … | 42 |
| 5'-2" | … | 8 | 34 | … | … | 42 |
| 5'-3" | … | 8 | 35 | … | … | 43 |
| 5'-4" | … | 7 | 36 | … | … | 43 |
| 5'-5" | … | 6 | 38 | … | … | 44 |
| 5'-6" | … | 5 | 39 | … | … | 44 |
| 5'-7" | … | 5 | 40 | … | … | 45 |
| 5'-8" | … | 4 | 41 | … | … | 45 |
| 5'-9" | … | 3 | 43 | … | … | 46 |
| 5'-10" | … | 2 | 44 | … | … | 46 |
| 5'-11" | … | 1 | 46 | … | … | 47 |
| 6'-0" | … | … | 47 | … | … | 47 |
| 6'-2" | … | … | 47 | 2 | … | 49 |
| 6'-4" | … | … | 46 | 4 | … | 50 |
| 6'-6" | … | … | 45 | 6 | … | 51 |
| 6'-8" | … | … | 44 | 8 | … | 52 |
| 6'-10" | … | … | 43 | 10 | … | 53 |
| 7'-0" | … | … | 41 | 13 | … | 54 |
| 7'-2" | … | … | 40 | 15 | … | 55 |
| 7'-4" | … | … | 39 | 17 | … | 56 |
| 7'-6" | … | … | 38 | 19 | … | 57 |
| 7'-8" | … | … | 37 | 21 | … | 58 |
| 7'-10" | … | … | 36 | 23 | … | 59 |
| 8'-0" | … | … | 34 | 26 | … | 60 |
| 8'-2" | … | … | 33 | 28 | … | 61 |
| 8'-4" | … | … | 32 | 30 | … | 62 |
| 8'-6" | … | … | 31 | 32 | … | 63 |
| 8'-8" | … | … | 30 | 34 | … | 64 |
| 8'-10" | … | … | 28 | 37 | … | 65 |
| 9'-0" | … | … | 27 | 39 | … | 66 |
| 9'-2" | … | … | 26 | 41 | … | 67 |
| 9'-4" | … | … | 25 | 43 | … | 68 |
| 9'-6" | … | … | 24 | 45 | … | 69 |
| 9'-8" | … | … | 23 | 47 | … | 70 |
| 9'-10" | … | … | 22 | 50 | … | 72 |
| 10'-0" | … | … | 21 | 52 | … | 73 |
| 10'-2" | … | … | 19 | 55 | … | 74 |
| 10'-4" | … | … | 18 | 57 | … | 75 |
| 10'-6" | … | … | 17 | 59 | … | 76 |
| 10'-8" | … | … | 16 | 61 | … | 77 |
| 10'-10" | … | … | 15 | 63 | … | 78 |
| 11'-0" | … | … | 13 | 66 | … | 79 |
| 11'-2" | … | … | 12 | 68 | … | 80 |
| 11'-4" | … | … | 11 | 70 | … | 81 |
| 11'-6" | … | … | 10 | 72 | … | 82 |
| 11'-8" | … | … | 9 | 74 | … | 83 |
| 11'-10" | … | … | 8 | 76 | … | 84 |
| 12'-0" | … | … | 6 | 79 | … | 85 |
| 12'-2" | … | … | 5 | 81 | … | 86 |
| 12'-4" | … | … | 4 | 83 | … | 87 |
| 12'-6" | … | … | 3 | 85 | … | 88 |
| 12'-8" | … | … | 2 | 87 | … | 89 |
| 12'-10" | … | … | 1 | 89 | … | 90 |
| 13'-0" | … | … | … | 91 | … | 91 |
| 13'-6" | … | … | … | 91 | 4 | 95 |
| 14'-0" | … | … | … | 91 | 7 | 98 |
| 14'-6" | … | … | … | 91 | 10 | 101 |
| 15'-0" | … | … | … | 91 | 13 | 104 |
| 15'-6" | … | … | … | 91 | 16 | 107 |

(p.136 runs 1'-6" to 5'-9"; p.137 from 5'-10".) Totals checked: all rows sum correctly.

## Image (23).jpg — catalogue p.138–139

### p.138 — continuation of the 9"x6"x2½" or 9"x6"x3" KEY BRICK table — 9-INCH LINING

No. 3, No. 2-X and No. 2 are blank (…) in every row; No. 1 = 91 in every row.

| Inside diameter | No. 1 | Straight 9x6x2½ | Total |
|---|---|---|---|
| 16'-0" | 91 | 19 | 110 |
| 16'-6" | 91 | 22 | 113 |
| 17'-0" | 91 | 26 | 117 |
| 17'-6" | 91 | 29 | 120 |
| 18'-0" | 91 | 32 | 123 |
| 18'-6" | 91 | 35 | 126 |
| 19'-0" | 91 | 38 | 129 |
| 19'-6" | 91 | 41 | 132 |
| 20'-0" | 91 | 44 | 135 |
| 20'-6" | 91 | 48 | 139 |
| 21'-0" | 91 | 51 | 142 |
| 21'-6" | 91 | 54 | 145 |
| 22'-0" | 91 | 57 | 148 |
| 22'-6" | 91 | 60 | 151 |
| 23'-0" | 91 | 63 | 154 |
| 23'-6" | 91 | 66 | 157 |
| 24'-0" | 91 | 70 | 161 |
| 24'-6" | 91 | 73 | 164 |
| 25'-0" | 91 | 76 | 167 |
| 25'-6" | 91 | 79 | 170 |
| 26'-0" | 91 | 82 | 173 |
| 26'-6" | 91 | 85 | 176 |
| 27'-0" | 91 | 88 | 179 |
| 27'-6" | 91 | 92 | 183 |
| 28'-0" | 91 | 95 | 186 |
| 28'-6" | 91 | 98 | 189 |
| 29'-0" | 91 | 101 | 192 |
| 29'-6" | 91 | 104 | 195 |
| 30'-0" | 91 | 107 | 198 |
| 30'-6" | 91 | 110 | 201 |
| 31'-0" | 91 | 114 | 205 |
| 31'-6" | 91 | 117 | 208 |
| 32'-0" | 91 | 120 | 211 |
| 32'-6" | 91 | 123 | 214 |
| 33'-0" | 91 | 126 | 217 |
| 33'-6" | 91 | 129 | 220 |
| 34'-0" | 91 | 132 | 223 |
| 34'-6" | 91 | 135 | 226 |
| 35'-0" | 91 | 139 | 230 |
| 35'-6" | 91 | 142 | 233 |
| 36'-0" | 91 | 145 | 236 |
| 36'-6" | 91 | 148 | 239 |
| 37'-0" | 91 | 151 | 242 |
| 37'-6" | 91 | 154 | 245 |
| 38'-0" | 91 | 157 | 248 |
| 38'-6" | 91 | 161 | 252 |
| 39'-0" | 91 | 164 | 255 |
| 39'-6" | 91 | 167 | 258 |
| 40'-0" | 91 | 170 | 261 |

Totals checked: all rows sum correctly.

### p.139 — COMPLETE CIRCLES 9"x6"x3" WEDGE TYPE ROTARY KILN LINERS — 9-INCH LINING

Columns: Kiln size; shape (size and designation); Per circle; ⅔ Split; ¾ Split. The 32nds/16ths are small in the scan: values are as read, and any single fraction may be off by one step [?read].

| Kiln size | Shape | Per circle | ⅔ split | ¾ split |
|---|---|---|---|---|
| 10'-0" | 9x6x(3-2 9/16) (102-W-120) | 126 | (2-1 11/16) | (2¼-1 29/32) |
| 10'-3" | 9x6x(3-2 9/16) (105-W-123) | 129 | (2-1 23/32) | (2¼-1 29/32) |
| 10'-6" | 9x6x(3-2 9/16) (108-W-126) | 132 | (2-1 23/32) | (2¼-1 29/32) |
| 10'-9" | 9x6x(3-2 19/32) (111-W-129) | 135 | (2-1 23/32) | (2¼-1 15/16) |
| 11'-0" | 9x6x(3-2 19/32) (114-W-132) | 139 | (2-1 23/32) | (2¼-1 15/16) |
| 11'-3" | 9x6x(3-2 19/32) (117-W-135) | 142 | (2-1 23/32) | (2¼-1 15/16) |
| 11'-6" | 9x6x(3-2 19/32) (120-W-138) | 145 | (2-1¾) | (2¼-1 31/32) |
| 11'-9" | 9x6x(3-2⅝) (123-W-141) | 148 | (2-1¾) | (2¼-1 31/32) |
| 12'-0" | 9x6x(3-2⅝) (126-W-144) | 151 | (2-1¾) | (2¼-1 31/32) |
| 12'-3" | 9x6x(3-2⅝) (129-W-147) | 154 | (2-1¾) | (2¼-1 31/32) |
| 12'-6" | 9x6x(3-2⅝) (132-W-150) | 157 | (2-1¾) | (2¼-1 31/32) |
| 12'-9" | 9x6x(3-2 21/32) (135-W-153) | 161 | (2-1¾) | (2¼-2) |
| 13'-0" | 9x6x(3-2 21/32) (138-W-156) | 164 | (2-1 25/32) | (2¼-2) |
| 13'-3" | 9x6x(3-2 21/32) (141-W-159) | 167 | (2-1 25/32) | (2¼-2) |
| 13'-6" | 9x6x(3-2 21/32) (144-W-162) | 170 | (2-1 25/32) | (2¼-2) |
| 13'-9" | 9x6x(3-2 11/16) (147-W-165) | 173 | (2-1 25/32) | (2¼-2) |
| 14'-0" | 9x6x(3-2 11/16) (150-W-168) | 176 | (2-1 25/32) | (2¼-2) |
| 14'-3" | 9x6x(3-2 11/16) (153-W-171) | 179 | (2-1 25/32) | (2¼-2) |
| 14'-6" | 9x6x(3-2 11/16) (156-W-174) | 183 | (2-1 25/32) | (2¼-2 1/32) |
| 14'-9" | 9x6x(3-2 11/16) (159-W-177) | 186 | (2-1 25/32) | (2¼-2 1/32) |
| 15'-0" | 9x6x(3-2 11/16) (162-W-180) | 189 | (2-1 13/16) | (2¼-2 1/32) |
| 15'-3" | 9x6x(3-2 23/32) (165-W-183) | 192 | (2-1 13/16) | (2¼-2 1/32) |
| 15'-6" | 9x6x(3-2 23/32) (168-W-186) | 195 | (2-1 13/16) | (2¼-2 1/32) |
| 15'-9" | 9x6x(3-2 23/32) (171-W-189) | 198 | (2-1 13/16) | (2¼-2 1/32) |
| 16'-0" | 9x6x(3-2 23/32) (174-W-192) | 201 | (2-1 13/16) | (2¼-2 1/32) |
| 16'-3" | 9x6x(3-2 23/32) (177-W-195) | 204 | (2-1 13/16) | (2¼-2 1/32) |
| 16'-6" | 9x6x(3-2 23/32) (180-W-198) | 208 | (2-1 13/16) | (2¼-2 1/32) |
| 16'-9" | 9x6x(3-2 23/32) (183-W-201) | 211 | (2-1 13/16) | (2¼-2 1/16) |
| 17'-0" | 9x6x(3-2¾) (186-W-204) | 214 | (2-1 13/16) | (2¼-2 1/16) |
| 17'-3" | 9x6x(3-2¾) (189-W-207) | 217 | (2-1 13/16) | (2¼-2 1/16) |
| 17'-6" | 9x6x(3-2¾) (192-W-210) | 220 | (2-1 27/32) | (2¼-2 1/16) |
| 17'-9" | 9x6x(3-2¾) (195-W-213) | 223 | (2-1 27/32) | (2¼-2 1/16) |
| 18'-0" | 9x6x(3-2¾) (198-W-216) | 227 | (2-1 27/32) | (2¼-2 1/16) |
| 18'-3" | 9x6x(3-2¾) (201-W-219) | 230 | (2-1 27/32) | (2¼-2 1/16) |
| 18'-6" | 9x6x(3-2¾) (204-W-222) | 233 | (2-1 27/32) | (2¼-2 1/16) |
| 18'-9" | 9x6x(3-2¾) (207-W-225) | 236 | (2-1 27/32) | (2¼-2 1/16) |
| 19'-0" | 9x6x(3-2¾) (210-W-228) | 239 | (2-1 27/32) | (2¼-2 1/16) |
| 19'-3" | 9x6x(3-2 25/32) (213-W-231) | 242 | (2-1 27/32) | (2¼-2 1/16) |
| 19'-6" | 9x6x(3-2 25/32) (216-W-234) | 245 | (2-1 27/32) | (2¼-2 1/16) |
| 19'-9" | 9x6x(3-2 25/32) (219-W-237) | 249 | (2-1 27/32) | (2¼-2 3/32) |
| 20'-0" | 9x6x(3-2 25/32) (222-W-240) | 252 | (2-1 27/32) | (2¼-2 3/32) |

## Image (24).jpg — catalogue p.140–141

### p.140 — COMPLETE CIRCLES 9"x6"x3½" WEDGE TYPE ROTARY KILN LINERS — 9-INCH LINING

(Same columns as p.139; small fractions [?read] as there.)

| Kiln size | Shape | Per circle | ⅔ split | ¾ split |
|---|---|---|---|---|
| 10'-0" | 9x6x(3½-2 31/32) (102-W-120) | 108 | (2 11/32-1 31/32) | (2⅝-2 7/32) |
| 10'-3" | 9x6x(3½-3) (105-W-123) | 111 | (2 11/32-2) | (2⅝-2¼) |
| 10'-6" | 9x6x(3½-3) (108-W-126) | 113 | (2 11/32-2) | (2⅝-2¼) |
| 10'-9" | 9x6x(3½-3) (111-W-129) | 116 | (2 11/32-2) | (2⅝-2¼) |
| 11'-0" | 9x6x(3½-3 1/32) (114-W-132) | 119 | (2 11/32-2) | (2⅝-2 9/32) |
| 11'-3" | 9x6x(3½-3 1/32) (117-W-135) | 122 | (2 11/32-2 1/32) | (2⅝-2 9/32) |
| 11'-6" | 9x6x(3½-3 1/32) (120-W-138) | 124 | (2 11/32-2 1/32) | (2⅝-2 9/32) |
| 11'-9" | 9x6x(3½-3 1/16) (123-W-141) | 127 | (2 11/32-2 1/32) | (2⅝-2 9/32) |
| 12'-0" | 9x6x(3½-3 1/16) (126-W-144) | 130 | (2 11/32-2 1/32) | (2⅝-2 9/32) |
| 12'-3" | 9x6x(3½-3 1/16) (129-W-147) | 132 | (2 11/32-2 1/16) | (2⅝-2 5/16) |
| 12'-6" | 9x6x(3½-3 1/16) (132-W-150) | 135 | (2 11/32-2 1/16) | (2⅝-2 5/16) |
| 12'-9" | 9x6x(3½-3 3/32) (135-W-153) | 138 | (2 11/32-2 1/16) | (2⅝-2 5/16) |
| 13'-0" | 9x6x(3½-3 3/32) (138-W-156) | 140 | (2 11/32-2 1/16) | (2⅝-2 5/16) |
| 13'-3" | 9x6x(3½-3 3/32) (141-W-159) | 143 | (2 11/32-2 1/16) | (2⅝-2 5/16) |
| 13'-6" | 9x6x(3½-3⅛) (144-W-162) | 146 | (2 11/32-2 1/16) | (2⅝-2 11/32) |
| 13'-9" | 9x6x(3½-3⅛) (147-W-165) | 149 | (2 11/32-2 3/32) | (2⅝-2 11/32) |
| 14'-0" | 9x6x(3½-3⅛) (150-W-168) | 151 | (2 11/32-2 3/32) | (2⅝-2 11/32) |
| 14'-3" | 9x6x(3½-3⅛) (153-W-171) | 154 | (2 11/32-2 3/32) | (2⅝-2 11/32) |
| 14'-6" | 9x6x(3½-3⅛) (156-W-174) | 157 | (2 11/32-2 3/32) | (2⅝-2 11/32) |
| 14'-9" | 9x6x(3½-3 5/32) (159-W-177) | 159 | (2 11/32-2 3/32) | (2⅝-2 11/32) |
| 15'-0" | 9x6x(3½-3 5/32) (162-W-180) | 162 | (2 11/32-2 3/32) | (2⅝-2⅜) |
| 15'-3" | 9x6x(3½-3 5/32) (165-W-183) | 165 | (2 11/32-2 3/32) | (2⅝-2⅜) |
| 15'-6" | 9x6x(3½-3 5/32) (168-W-186) | 167 | (2 11/32-2 3/32) | (2⅝-2⅜) |
| 15'-9" | 9x6x(3½-3 5/32) (171-W-189) | 170 | (2 11/32-2⅛) | (2⅝-2⅜) |
| 16'-0" | 9x6x(3½-3 5/32) (174-W-192) | 173 | (2 11/32-2⅛) | (2⅝-2⅜) |
| 16'-3" | 9x6x(3½-3 3/16) (177-W-195) | 175 | (2 11/32-2⅛) | (2⅝-2⅜) |
| 16'-6" | 9x6x(3½-3 3/16) (180-W-198) | 178 | (2 11/32-2⅛) | (2⅝-2⅜) |
| 16'-9" | 9x6x(3½-3 3/16) (183-W-201) | 180 | (2 11/32-2⅛) | (2⅝-2⅜) |
| 17'-0" | 9x6x(3½-3 3/16) (186-W-204) | 184 | (2 11/32-2⅛) | (2⅝-2⅜) |
| 17'-3" | 9x6x(3½-3 3/16) (189-W-207) | 186 | (2 11/32-2⅛) | (2⅝-2 13/32) |
| 17'-6" | 9x6x(3½-3 3/16) (192-W-210) | 189 | (2 11/32-2⅛) | (2⅝-2 13/32) |
| 17'-9" | 9x6x(3½-3 3/16) (195-W-213) | 192 | (2 11/32-2⅛) | (2⅝-2 13/32) |
| 18'-0" | 9x6x(3½-3 7/32) (198-W-216) | 194 | (2 11/32-2⅛) | (2⅝-2 13/32) |
| 18'-3" | 9x6x(3½-3 7/32) (201-W-219) | 197 | (2 11/32-2 5/32) | (2⅝-2 13/32) |
| 18'-6" | 9x6x(3½-3 7/32) (204-W-222) | 200 | (2 11/32-2 5/32) | (2⅝-2 13/32) |
| 18'-9" | 9x6x(3½-3 7/32) (207-W-225) | 202 | (2 11/32-2 5/32) | (2⅝-2 13/32) |
| 19'-0" | 9x6x(3½-3 7/32) (210-W-228) | 205 | (2 11/32-2 5/32) | (2⅝-2 13/32) |
| 19'-3" | 9x6x(3½-3 7/32) (213-W-231) | 208 | (2 11/32-2 5/32) | (2⅝-2 13/32) |
| 19'-6" | 9x6x(3½-3 7/32) (216-W-234) | 210 | (2 11/32-2 5/32) | (2⅝-2 7/16) |
| 19'-9" | 9x6x(3½-3 7/32) (219-W-237) | 213 | (2 11/32-2 5/32) | (2⅝-2 7/16) |
| 20'-0" | 9x6x(3½-3¼) (222-W-240) | 216 | (2 11/32-2 5/32) | (2⅝-2 7/16) |

### p.141 — COMPLETE CIRCLES 9"x9"x4" ROTARY KILN BLOCKS — 9-INCH LINING

Three sub-tables, each headed "SHAPES REQUIRED TO TURN CIRCLE" with six "9x9x4 <range>" columns (C1–C6). "Continued Next Page".

Band 1: C1 = 48-66, C2 = 54-72, C3 = 60-78, C4 = 66-84, C5 = 72-90, C6 = 78-96

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 5'-6" | 23 | … | … | … | … | … | 23 |
| 5'-9" | 12 | 12 | … | … | … | … | 24 |
| 6'-0" | … | 26 | … | … | … | … | 26 |
| 6'-3" | … | 13 | 14 | … | … | … | 27 |
| 6'-6" | … | … | 28 | … | … | … | 28 |
| 6'-9" | … | … | 14 | 15 | … | … | 29 |
| 7'-0" | … | … | … | 30 | … | … | 30 |
| 7'-3" | … | … | … | 15 | 16 | … | 31 |
| 7'-6" | … | … | … | … | 32 | … | 32 |
| 7'-9" | … | … | … | … | 16 | 17 | 33 |

Band 2: C1 = 78-96, C2 = 84-102, C3 = 90-108, C4 = 96-114, C5 = 102-120, C6 = 108-126

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 8'-0" | 34 | … | … | … | … | … | 34 |
| 8'-3" | 17 | 18 | … | … | … | … | 35 |
| 8'-6" | … | 36 | … | … | … | … | 36 |
| 8'-9" | … | 18 | 19 | … | … | … | 37 |
| 9'-0" | … | … | 38 | … | … | … | 38 |
| 9'-3" | … | … | 19 | 20 | … | … | 39 |
| 9'-6" | … | … | … | 40 | … | … | 40 |
| 9'-9" | … | … | … | 20 | 21 | … | 41 |
| 10'-0" | … | … | … | … | 42 | … | 42 |
| 10'-3" | … | … | … | … | 21 | 22 | 43 |

Band 3: C1 = 108-126, C2 = 114-132, C3 = 120-138, C4 = 126-144, C5 = 132-150, C6 = 138-156

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 10'-6" | 44 | … | … | … | … | … | 44 |
| 10'-9" | 22 | 23 | … | … | … | … | 45 |
| 11'-0" | … | 46 | … | … | … | … | 46 |
| 11'-3" | … | 24 | 24 | … | … | … | 48 |
| 11'-6" | … | … | 49 | … | … | … | 49 |
| 11'-9" | … | … | 25 | 25 | … | … | 50 |
| 12'-0" | … | … | … | 51 | … | … | 51 |
| 12'-3" | … | … | … | 26 | 26 | … | 52 |
| 12'-6" | … | … | … | … | 53 | … | 53 |
| 12'-9" | … | … | … | … | 27 | 27 | 54 |

Totals checked: all rows sum correctly.

## Image (25).jpg — catalogue p.142–143

### p.142 — 9"x9"x4" ROTARY KILN BLOCKS (continued) — 9-INCH LINING

Band A: C1 = 9x9x4 138-156, C2 = 144-162, C3 = 150-168, C4 = 156-174, C5 = 162-180, C6 = 168-186

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 13'-0" | 55 | … | … | … | … | … | 55 |
| 13'-3" | 28 | 28 | … | … | … | … | 56 |
| 13'-6" | … | 57 | … | … | … | … | 57 |
| 13'-9" | … | 29 | 29 | … | … | … | 58 |
| 14'-0" | … | … | 59 | … | … | … | 59 |
| 14'-3" | … | … | 30 | 30 | … | … | 60 |
| 14'-6" | … | … | … | 61 | … | … | 61 |
| 14'-9" | … | … | … | 31 | 31 | … | 62 |
| 15'-0" | … | … | … | … | 63 | … | 63 |
| 15'-3" | … | … | … | … | 32 | 32 | 64 |

Band B: C1 = 168-186, C2 = 174-192, C3 = 180-198, C4 = 186-204, C5 = 192-210, C6 = 198-216

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 15'-6" | 65 | … | … | … | … | … | 65 |
| 15'-9" | 33 | 33 | … | … | … | … | 66 |
| 16'-0" | … | 67 | … | … | … | … | 67 |
| 16'-3" | … | 34 | 34 | … | … | … | 68 |
| 16'-6" | … | … | 69 | … | … | … | 69 |
| 16'-9" | … | … | 35 | 36 | … | … | 71 |
| 17'-0" | … | … | … | 72 | … | … | 72 |
| 17'-3" | … | … | … | 36 | 37 | … | 73 |
| 17'-6" | … | … | … | … | 74 | … | 74 |
| 17'-9" | … | … | … | … | 37 | 38 | 75 |
| 18'-0" | … | … | … | … | … | 76 | 76 |

Totals checked: all rows sum correctly.

### p.143 — COMPLETE CIRCLES 12"x9"x4" ROTARY KILN BLOCKS — 9-INCH LINING

Band 1: C1 = 12x9x4 108-126, C2 = 114-132, C3 = 120-138, C4 = 126-144, C5 = 132-150, C6 = 138-156

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 10'-6" | 33 | … | … | … | … | … | 33 |
| 10'-9" | 17 | 17 | … | … | … | … | 34 |
| 11'-0" | … | 35 | … | … | … | … | 35 |
| 11'-3" | … | 18 | 18 | … | … | … | 36 |
| 11'-6" | … | … | 37 | … | … | … | 37 |
| 11'-9" | … | … | 18 | 19 | … | … | 37 |
| 12'-0" | … | … | … | 38 | … | … | 38 |
| 12'-3" | … | … | … | 19 | 20 | … | 39 |
| 12'-6" | … | … | … | … | 40 | … | 40 |
| 12'-9" | … | … | … | … | 20 | 20 | 40 |

Band 2: C1 = 138-156, C2 = 144-162, C3 = 150-168, C4 = 156-174, C5 = 162-180, C6 = 168-186

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 13'-0" | 41 | … | … | … | … | … | 41 |
| 13'-3" | 21 | 21 | … | … | … | … | 42 |
| 13'-6" | … | 43 | … | … | … | … | 43 |
| 13'-9" | … | 22 | 22 | … | … | … | 44 |
| 14'-0" | … | … | 44 | … | … | … | 44 |
| 14'-3" | … | … | 22 | 23 | … | … | 45 |
| 14'-6" | … | … | … | 46 | … | … | 46 |
| 14'-9" | … | … | … | 23 | 24 | … | 47 |
| 15'-0" | … | … | … | … | 48 | … | 48 |
| 15'-3" | … | … | … | … | 24 | 24 | 48 |

Band 3: C1 = 168-186, C2 = 174-192, C3 = 180-198, C4 = 186-204, C5 = 192-210, C6 = 198-216

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 15'-6" | 49 | … | … | … | … | … | 49 |
| 15'-9" | 25 | 25 | … | … | … | … | 50 |
| 16'-0" | … | 51 | … | … | … | … | 51 |
| 16'-3" | … | 25 | 26 | … | … | … | 51 |
| 16'-6" | … | … | 52 | … | … | … | 52 |
| 16'-9" | … | … | 26 | 27 | … | … | 53 |
| 17'-0" | … | … | … | 54 | … | … | 54 |
| 17'-3" | … | … | … | 27 | 28 | … | 55 |
| 17'-6" | … | … | … | … | 55 | … | 55 |
| 17'-9" | … | … | … | … | 28 | 28 | 56 |

Totals checked: all rows sum correctly.

## Image (26).jpg — catalogue p.144–145

### p.144 — 12"x9"x4" ROTARY KILN BLOCKS (continued) — 9-INCH LINING

Band 1: C1 = 12x9x4 198-216, C2 = 204-222, C3 = 210-228, C4 = 216-234, C5 = 222-240, C6 = 228-246

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 18'-0" | 57 | … | … | … | … | … | 57 |
| 18'-3" | 29 | 29 | … | … | … | … | 58 |
| 18'-6" | … | 58 | … | … | … | … | 58 |
| 18'-9" | … | 29 | 30 | … | … | … | 59 |
| 19'-0" | … | … | 60 | … | … | … | 60 |
| 19'-3" | … | … | 30 | 31 | … | … | 61 |
| 19'-6" | … | … | … | 62 | … | … | 62 |
| 19'-9" | … | … | … | 31 | 31 | … | 62 |
| 20'-0" | … | … | … | … | 63 | … | 63 |
| 20'-3" | … | … | … | … | 32 | 32 | 64 |

Band 2: C1 = 228-246, C2 = 234-252, C3 = 240-258, C4 = 246-264, C5 = 252-270, C6 = 258-276

| Kiln size | C1 | C2 | C3 | C4 | C5 | C6 | Total |
|---|---|---|---|---|---|---|---|
| 20'-6" | 65 | … | … | … | … | … | 65 |
| 20'-9" | 33 | 33 | … | … | … | … | 66 |
| 21'-0" | … | 66 | … | … | … | … | 66 |
| 21'-3" | … | 33 | 34 | … | … | … | 67 |
| 21'-6" | … | … | 68 | … | … | … | 68 |
| 21'-9" | … | … | 34 | 35 | … | … | 69 |
| 22'-0" | … | … | … | 69 | … | … | 69 |
| 22'-3" | … | … | … | 35 | 35 | … | 70 |
| 22'-6" | … | … | … | … | 71 | … | 71 |
| 22'-9" | … | … | … | … | 36 | 36 | 72 |

Band 3: C1 = 258-276, C2 = 264-282, C3 = 270-288

| Kiln size | C1 | C2 | C3 | Total |
|---|---|---|---|---|
| 23'-0" | 73 | … | … | 73 |
| 23'-3" | 36 | 37 | … | 73 |
| 23'-6" | … | 74 | … | 74 |
| 23'-9" | … | 37 | 38 | 75 |
| 24'-0" | … | … | 76 | 76 |

Totals checked: all rows sum correctly.

### p.145 — COMPLETE CIRCLES 9"x6"x4" WEDGE TYPE ROTARY KILN BLOCKS — 9-INCH LINING

| Kiln size | 9x6x(4-2 31/32) KL-3-W | 9x6x(4-3¼) KL-2-W | 9x6x(4-3 11/32) KL-1-W | Total |
|---|---|---|---|---|
| 5'-9" | 54 | … | … | 54 |
| 6'-0" | 50 | 7 | … | 57 |
| 6'-3" | 44 | 15 | … | 59 |
| 6'-6" | [?read: 38; looks like 33] | 24 | … | 62 |
| 6'-9" | 32 | 32 | … | 64 |
| 7'-0" | 25 | 41 | … | 66 |
| 7'-3" | 19 | 50 | … | 69 |
| 7'-6" | 13 | 58 | … | 71 |
| 7'-9" | 6 | 67 | … | 73 |
| 8'-0" | … | 76 | … | 76 |
| 8'-3" | … | 72 | 6 | 78 |
| 8'-6" | … | 68 | 13 | 81 |
| 8'-9" | … | 64 | 19 | 83 |
| 9'-0" | … | 60 | 25 | 85 |
| 9'-3" | … | 56 | 32 | 88 |
| 9'-6" | … | 52 | 38 | 90 |
| 9'-9" | … | 48 | 44 | 92 |
| 10'-0" | … | 44 | 51 | 95 |
| 10'-3" | … | 40 | 57 | 97 |
| 10'-6" | … | 36 | 63 | 99 |
| 10'-9" | … | 33 | 69 | 102 |
| 11'-0" | … | 28 | 76 | 104 |
| 11'-3" | … | 24 | 82 | 106 |
| 11'-6" | … | 21 | 88 | 109 |
| 11'-9" | … | 17 | 94 | 111 |
| 12'-0" | … | 13 | 100 | 113 |
| 12'-3" | … | 9 | 107 | 116 |
| 12'-6" | … | 5 | 113 | 118 |
| 12'-9" | … | 1 | 119 | 120 |

Totals check: all rows sum correctly, except 6'-6": the KL-3-W figure looks like "33" (33 + 24 = 57 ≠ 62). The printed total, and the same row on p.125 (38), point to 38.

Note (verbatim): "KL-4-W, 9x6x(3-2 7/16), and KL-5-W, 9x6x(2 21/32-2 3/16), may be used for keying each ring to avoid cutting last brick. Two of each should be ordered for each ring of full size liners." (fractions [?read])

Drawing: block 9" x 6", end thickness "T" tapering to "W"; detail "METHOD OF MARKING THICK END OF LINER" (⅛" R, ¼" ø [?read]).

| Brand | "T" | "W" | Description |
|---|---|---|---|
| KL-1-W | 4" | 3 11/32" [?read] | FULL SIZE LINER |
| KL-2-W | 4" | 3¼" | FULL SIZE LINER |
| KL-3-W | 4" | 2 31/32" | FULL SIZE LINER |

## Image (27).jpg — catalogue p.146–147

### p.146 — COMPLETE CIRCLES—BASIC BRICK ONLY, ROTARY KILN 9"x6"x3" WEDGES — 9-INCH LINING

(Small fractions [?read], as on p.126.)

| Kiln size | Shape | No. pieces per circle |
|---|---|---|
| 7'-0" | 9x6x(3-2 11/32)W-(66-84) | 86 |
| 7'-3" | 9x6x(3-2⅜)W-(69-87) | 89 |
| 7'-6" | 9x6x(3-2⅜)W-(72-90) | 92 |
| 7'-9" | 9x6x(3-2 13/32)W-(75-93) | 95 |
| 8'-0" | 9x6x(3-2 7/16)W-(78-96) | 98 |
| 8'-3" | 9x6x(3-2 7/16)W-(81-99) | 102 |
| 8'-6" | 9x6x(3-2 15/32)W-(84-102) | 105 |
| 8'-9" | 9x6x(3-2 15/32)W-(87-105) | 108 |
| 9'-0" | 9x6x(3-2½)W-(90-108) | 111 |
| 9'-3" | 9x6x(3-2½)W-(93-111) | 114 |
| 9'-6" | 9x6x(3-2 17/32)W-(96-114) | 117 |
| 9'-9" | 9x6x(3-2 17/32)W-(99-117) | 120 |
| 10'-0" | 9x6x(3-2 17/32)W-(102-120) | 123 |
| 10'-3" | 9x6x(3-2 9/16)W-(105-123) | 126 |
| 10'-6" | 9x6x(3-2 9/16)W-(108-126) | 129 |
| 10'-9" | 9x6x(3-2 9/16)W-(111-129) | 132 |
| 11'-0" | 9x6x(3-2 19/32)W-(114-132) | 135 |
| 11'-3" | 9x6x(3-2 19/32)W-(117-135) | 138 |
| 11'-6" | 9x6x(3-2 19/32)W-(120-138) | 142 |
| 11'-9" | 9x6x(3-2 19/32)W-(123-141) | 145 |
| 12'-0" | 9x6x(3-2⅝)W-(126-144) | 148 |
| 12'-3" | 9x6x(3-2⅝)W-(129-147) | 151 |
| 12'-6" | 9x6x(3-2⅝)W-(132-150) | 154 |
| 12'-9" | 9x6x(3-2⅝)W-(135-153) | 157 |
| 13'-0" | 9x6x(3-2 21/32)W-(138-156) | 160 |
| 13'-3" | 9x6x(3-2 21/32)W-(141-159) | 163 |
| 13'-6" | 9x6x(3-2 21/32)W-(144-162) | 166 |
| 13'-9" | 9x6x(3-2 21/32)W-(147-165) | 169 |
| 14'-0" | 9x6x(3-2 21/32)W-(150-168) | 172 |
| 14'-3" | 9x6x(3-2 11/16)W-(153-171) | 175 |
| 14'-6" | 9x6x(3-2 11/16)W-(156-174) | 178 |
| 14'-9" | 9x6x(3-2 11/16)W-(159-177) | 182 |
| 15'-0" | 9x6x(3-2 11/16)W-(162-180) | 185 |
| 15'-3" | 9x6x(3-2 11/16)W-(165-183) | 188 |
| 15'-6" | 9x6x(3-2 11/16)W-(168-186) | 191 |
| 15'-9" | 9x6x(3-2 23/32)W-(171-189) | 194 |
| 16'-0" | 9x6x(3-2 23/32)W-(174-192) | 197 |
| 16'-3" | 9x6x(3-2 23/32)W-(177-195) | 200 |
| 16'-6" | 9x6x(3-2 23/32)W-(180-198) | 203 |
| 16'-9" | 9x6x(3-2 23/32)W-(183-201) | 206 |
| 17'-0" | 9x6x(3-2 23/32)W-(186-204) | 209 |
| 17'-3" | 9x6x(3-2 23/32)W-(189-207) | 212 |
| 17'-6" | 9x6x(3-2¾)W-(192-210) | 215 |
| 17'-9" | 9x6x(3-2¾)W-(195-213) | 218 |
| 18'-0" | 9x6x(3-2¾)W-(198-216) | 222 |
| 18'-3" | 9x6x(3-2¾)W-(201-219) | 225 |
| 18'-6" | 9x6x(3-2¾)W-(204-222) | 228 |
| 18'-9" | 9x6x(3-2¾)W-(207-225) | 231 |
| 19'-0" | 9x6x(3-2¾)W-(210-228) | 234 |
| 19'-3" | 9x6x(3-2¾)W-(213-231) | 237 |
| 19'-6" | 9x6x(3-2¾)W-(216-234) | 240 |
| 19'-9" | 9x6x(3-2 25/32)W-(219-237) | 243 |
| 20'-0" | 9x6x(3-2 25/32)W-(222-240) | 246 |

RING CLOSURE BRICK (p.146)

| Kiln diameter | Shape | No. per ring |
|---|---|---|
| 7'-0" To 13'-6" | RCW-1 9x6x(3½-3) | 1 |
| | RCW-2 9x6x(2¼-1 29/32) [?read] | 1 |
| Over 13'-6" | RCW-3 9x6x(3½-3 3/16) [?read] | 1 |
| | RCW-4 9x6x(2¼-2 1/32) [?read] | 1 |

### p.147 — COMPLETE CIRCLES—BASIC BRICK ONLY, ROTARY KILN 9"x6"x3½" WEDGES — 9-INCH LINING

| Kiln size | Shape | No. pieces per circle |
|---|---|---|
| 7'-0" | 9x6x(3½-2¾)W-(66-84) | 74 |
| 7'-3" | 9x6x(3½-2¾)W-(69-87) | 77 |
| 7'-6" | 9x6x(3½-2 25/32)W-(72-90) | 79 |
| 7'-9" | 9x6x(3½-2 13/16)W-(75-93) | 82 |
| 8'-0" | 9x6x(3½-2 27/32)W-(78-96) | 85 |
| 8'-3" | 9x6x(3½-2 27/32)W-(81-99) | 87 |
| 8'-6" | 9x6x(3½-2⅞)W-(84-102) | 90 |
| 8'-9" | 9x6x(3½-2⅞)W-(87-105) | 93 |
| 9'-0" | 9x6x(3½-2 29/32)W-(90-108) | 95 |
| 9'-3" | 9x6x(3½-2 15/16)W-(93-111) | 98 |
| 9'-6" | 9x6x(3½-2 15/16)W-(96-114) | 101 |
| 9'-9" | 9x6x(3½-2 15/16)W-(99-117) | 103 |
| 10'-0" | 9x6x(3½-2 31/32)W-(102-120) | 106 |
| 10'-3" | 9x6x(3½-2 31/32)W-(105-123) | 109 |
| 10'-6" | 9x6x(3½-3)W-(108-126) | 111 |
| 10'-9" | 9x6x(3½-3)W-(111-129) | 114 |
| 11'-0" | 9x6x(3½-3)W-(114-132) | 116 |
| 11'-3" | 9x6x(3½-3 1/32)W-(117-135) | 119 |
| 11'-6" | 9x6x(3½-3 1/32)W-(120-138) | 122 |
| 11'-9" | 9x6x(3½-3 1/32)W-(123-141) | 124 |
| 12'-0" | 9x6x(3½-3 1/16)W-(126-144) | 127 |
| 12'-3" | 9x6x(3½-3 1/16)W-(129-147) | 130 |
| 12'-6" | 9x6x(3½-3 1/16)W-(132-150) | 132 |
| 12'-9" | 9x6x(3½-3 3/32)W-(135-153) | 135 |
| 13'-0" | 9x6x(3½-3 3/32)W-(138-156) | 138 |
| 13'-3" | 9x6x(3½-3 3/32)W-(141-159) | 140 |
| 13'-6" | 9x6x(3½-3 3/32)W-(144-162) | 143 |
| 13'-9" | 9x6x(3½-3⅛)W-(147-165) | 146 |
| 14'-0" | 9x6x(3½-3⅛)W-(150-168) | 148 |
| 14'-3" | 9x6x(3½-3⅛)W-(153-171) | 151 |
| 14'-6" | 9x6x(3½-3⅛)W-(156-174) | 153 |
| 14'-9" | 9x6x(3½-3⅛)W-(159-177) | 156 |
| 15'-0" | 9x6x(3½-3 5/32)W-(162-180) | 159 |
| 15'-3" | 9x6x(3½-3 5/32)W-(165-183) | 161 |
| 15'-6" | 9x6x(3½-3 5/32)W-(168-186) | 164 |
| 15'-9" | 9x6x(3½-3 5/32)W-(171-189) | 167 |
| 16'-0" | 9x6x(3½-3 5/32)W-(174-192) | 169 |
| 16'-3" | 9x6x(3½-3 5/32)W-(177-195) | 172 |
| 16'-6" | 9x6x(3½-3 3/16)W-(180-198) | 175 |
| 16'-9" | 9x6x(3½-3 3/16)W-(183-201) | 177 |
| 17'-0" | 9x6x(3½-3 3/16)W-(186-204) | 180 |
| 17'-3" | 9x6x(3½-3 3/16)W-(189-207) | 183 |
| 17'-6" | 9x6x(3½-3 3/16)W-(192-210) | 185 |
| 17'-9" | 9x6x(3½-3 3/16)W-(195-213) | 188 |
| 18'-0" | 9x6x(3½-3 3/16)W-(198-216) | 190 |
| 18'-3" | 9x6x(3½-3 7/32)W-(201-219) | 193 |
| 18'-6" | 9x6x(3½-3 7/32)W-(204-222) | 196 |
| 18'-9" | 9x6x(3½-3 7/32)W-(207-225) | 198 |
| 19'-0" | 9x6x(3½-3 7/32)W-(210-228) | 201 |
| 19'-3" | 9x6x(3½-3 7/32)W-(213-231) | 204 |
| 19'-6" | 9x6x(3½-3 7/32)W-(216-234) | 206 |
| 19'-9" | 9x6x(3½-3 7/32)W-(219-237) | 209 |
| 20'-0" | 9x6x(3½-3 7/32)W-(222-240) | 212 |

RING CLOSURE BRICK (p.147)

| Kiln diameter | Shape | No. per ring |
|---|---|---|
| 7'-0" To 13'-6" | RCW-5 9x6x(3-2 9/16) [?read] | 1 |
| | RCW-2 9x6x(2¼-1 29/32) [?read] | 1 |
| Over 13'-6" | RCW-6 9x6x(3-2 23/32) [?read] | 1 |
| | RCW-4 9x6x(2¼-2 1/32) [?read] | 1 |

## Image (28).jpg — catalogue p.148–149

### p.148 — COMPLETE CIRCLES, Special blast furnace key brick — 9", 12" and 13½"-INCH LINING

Subheading (verbatim): "Brands 1K and 2K—See Page 107 for sizes". Printed in two side-by-side column groups; merged here.

| Inside diameter | 2K | 1K | Total |
|---|---|---|---|
| 13'-3" | 98 | … | 98 |
| 13'-6" | 96 | 3 | 99 |
| 14'-0" | 94 | 8 | 102 |
| 14'-6" | 93 | 13 | 106 |
| 15'-0" | 91 | 18 | 109 |
| 15'-6" | 89 | 23 | 112 |
| 16'-0" | 87 | 28 | 115 |
| 16'-6" | 85 | 33 | 118 |
| 17'-0" | 84 | 37 | 121 |
| 17'-6" | 82 | 42 | 124 |
| 18'-0" | 80 | 48 | 128 |
| 18'-6" | 79 | 52 | 131 |
| 18'-9" | 78 | 54 | 132 |
| 19'-0" | 77 | 57 | 134 |
| 19'-3" | 76 | 59 | 135 |
| 19'-6" | 75 | 62 | 137 |
| 19'-9" | 74 | 65 | 139 |
| 20'-0" | 73 | 67 | 140 |
| 20'-3" | 72 | 70 | 142 |
| 20'-6" | 71 | 72 | 143 |
| 20'-9" | 71 | 74 | 145 |
| 21'-0" | 70 | 76 | 146 |
| 21'-3" | 69 | 79 | 148 |
| 21'-6" | 68 | 82 | 150 |
| 21'-9" | 67 | 84 | 151 |
| 22'-0" | 66 | 87 | 153 |
| 22'-3" | 65 | 89 | 154 |
| 22'-6" | 65 | 91 | 156 |
| 22'-9" | 64 | 93 | 157 |
| 23'-0" | 63 | 96 | 159 |
| 23'-3" | 62 | 99 | 161 |
| 23'-6" | 61 | 101 | 162 |
| 23'-9" | 60 | 104 | 164 |
| 24'-0" | 59 | 106 | 165 |
| 24'-3" | 58 | 109 | 167 |
| 24'-6" | 57 | 111 | 168 |
| 24'-9" | 57 | 113 | 170 |
| 25'-0" | 56 | 116 | 172 |
| 25'-3" | 55 | 118 | 173 |
| 25'-6" | 54 | 121 | 175 |
| 25'-9" | 53 | 123 | 176 |
| 26'-0" | 52 | 126 | 178 |
| 26'-3" | 51 | 128 | 179 |
| 26'-6" | 51 | 130 | 181 |
| 26'-9" | 50 | 133 | 183 |
| 27'-0" | 49 | 135 | 184 |
| 27'-3" | 48 | 138 | 186 |
| 27'-6" | 47 | 140 | 187 |
| 27'-9" | 46 | 143 | 189 |
| 28'-0" | 45 | 145 | 190 |
| 28'-3" | 45 | 147 | 192 |
| 28'-6" | 44 | 150 | 194 |
| 28'-9" | 43 | 152 | 195 |
| 29'-0" | 42 | 155 | 197 |
| 29'-3" | 41 | 157 | 198 |
| 29'-6" | 40 | 160 | 200 |
| 29'-9" | 39 | 162 | 201 |
| 30'-0" | 38 | 165 | 203 |
| 30'-3" | 37 | 167 | 204 |
| 30'-6" | 37 | 169 | 206 |
| 30'-9" | 36 | 172 | 208 |
| 31'-0" | 35 | 174 | 209 |
| 31'-3" | 34 | 177 | 211 |
| 31'-6" | 33 | 179 | 212 |
| 31'-9" | 32 | 182 | 214 |
| 32'-0" | 31 | 184 | 215 |
| 32'-3" | 31 | 186 | 217 |
| 32'-6" | 30 | 189 | 219 |
| 32'-9" | 29 | 191 | 220 |
| 33'-0" | 28 | 194 | 222 |
| 33'-3" | 27 | 196 | 223 |
| 33'-6" | 26 | 199 | 225 |
| 33'-9" | 25 | 201 | 226 |
| 34'-0" | 24 | 204 | 228 |
| 34'-3" | 24 | 206 | 230 |
| 34'-6" | 23 | 208 | 231 |
| 34'-9" | 22 | 211 | 233 |
| 35'-0" | 21 | 213 | 234 |
| 35'-3" | 20 | 216 | 236 |
| 35'-6" | 19 | 218 | 237 |
| 35'-9" | 18 | 221 | 239 |
| 36'-0" | 18 | 223 | 241 |
| 36'-3" | 16 | 226 | 242 |
| 36'-6" | 16 | 228 | 244 |
| 36'-9" | 15 | 230 | 245 |
| 37'-0" | 14 | 233 | 247 |
| 37'-3" | 13 | 235 | 248 |
| 37'-6" | 12 | 238 | 250 |
| 37'-9" | 11 | 241 | 252 |
| 38'-0" | 10 | 243 | 253 |
| 38'-3" | 10 | 245 | 255 |
| 38'-6" | 9 | 247 | 256 |
| 38'-9" | 8 | 250 | 258 |
| 39'-0" | 7 | 252 | 259 |
| 39'-3" | 6 | 255 | 261 |
| 39'-6" | 5 | 258 | 263 |
| 39'-9" | 4 | 260 | 264 |
| 40'-0" | 4 | 262 | 266 |
| 40'-3" | 2 | 265 | 267 |
| 40'-6" | 2 | 267 | 269 |
| 40'-9" | 1 | 269 | 270 |
| 41'-0" | … | 272 | 272 |

Totals checked: all rows sum correctly.

### p.149 — COMPLETE CIRCLES 12"x4½"x3", 12"x6"x3" or 12"x9"x3" WEDGE BRICK — 12-INCH LINING

Columns: No. 3 Wedge 12x6x(3-2); No. 2 Wedge 12x6x(3-2½); No. 1 Wedge 12x6x(3-2¾); No. 1-X Wedge 12x6x(3-2⅞); Straights 12x6x3; Total. Continues to p.150.

| Inside diameter | No. 3 | No. 2 | No. 1 | No. 1-X | Straights | Total |
|---|---|---|---|---|---|---|
| 4'-0" | 76 | … | … | … | … | 76 |
| 4'-3" | 72 | 7 | … | … | … | 79 |
| 4'-6" | 69 | 13 | … | … | … | 82 |
| 4'-9" | 66 | 19 | … | … | … | 85 |
| 5'-0" | 63 | 25 | … | … | … | 88 |
| 5'-3" | 60 | 31 | … | … | … | 91 |
| 5'-6" | 57 | 37 | … | … | … | 94 |
| 5'-9" | 54 | 44 | … | … | … | 98 |
| 6'-0" | 51 | 50 | … | … | … | 101 |
| 6'-3" | 47 | 57 | … | … | … | 104 |
| 6'-6" | 44 | 63 | … | … | … | 107 |
| 6'-9" | 41 | 69 | … | … | … | 110 |
| 7'-0" | 38 | 75 | … | … | … | 113 |
| 7'-3" | 35 | 81 | … | … | … | 116 |
| 7'-6" | 32 | 88 | … | … | … | 120 |
| 7'-9" | 29 | 94 | … | … | … | 123 |
| 8'-0" | 25 | 101 | … | … | … | 126 |
| 8'-3" | 22 | 107 | … | … | … | 129 |
| 8'-6" | 19 | 113 | … | … | … | 132 |
| 8'-9" | 16 | 119 | … | … | … | 135 |
| 9'-0" | 13 | 125 | … | … | … | 138 |
| 9'-3" | 10 | 132 | … | … | … | 142 |
| 9'-6" | 7 | 138 | … | … | … | 145 |
| 9'-9" | 3 | 145 | … | … | … | 148 |
| 10'-0" | … | 151 | … | … | … | 151 |
| 10'-3" | … | 148 | 6 | … | … | 154 |
| 10'-6" | … | 145 | 12 | … | … | 157 |
| 11'-0" | … | 139 | 25 | … | … | 164 |
| 11'-6" | … | 132 | 38 | … | … | 170 |
| 12'-0" | … | 126 | 50 | … | … | 176 |
| 12'-6" | … | 119 | 63 | … | … | 182 |
| 13'-0" | … | 113 | 76 | … | … | 189 |
| 13'-6" | … | 107 | 88 | … | … | 195 |
| 14'-0" | … | 101 | 100 | … | … | 201 |
| 14'-6" | … | 95 | 113 | … | … | 208 |
| 15'-0" | … | 88 | 126 | … | … | 214 |
| 15'-6" | … | 82 | 138 | … | … | 220 |
| 16'-0" | … | 75 | 151 | … | … | 226 |
| 16'-6" | … | 69 | 164 | … | … | 233 |
| 17'-0" | … | 63 | 176 | … | … | 239 |
| 17'-6" | … | 57 | 188 | … | … | 245 |
| 18'-0" | … | 51 | 201 | … | … | 252 |
| 18'-6" | … | 44 | 214 | … | … | 258 |
| 19'-0" | … | 38 | 226 | … | … | 264 |
| 19'-6" | … | 31 | 239 | … | … | 270 |
| 20'-0" | … | 25 | 252 | … | … | 277 |
| 20'-6" | … | 19 | 264 | … | … | 283 |
| 21'-0" | … | 13 | 276 | … | … | 289 |
| 21'-6" | … | 7 | 289 | … | … | 296 |
| 22'-0" | … | … | 302 | … | … | 302 |

Totals checked: all rows sum correctly.

## Image (29).jpg — catalogue p.150–151

### p.150 — continuation of the 12"x4½"x3", 12"x6"x3" or 12"x9"x3" WEDGE BRICK table — 12-INCH LINING

No. 3 and No. 2 are blank (…) in every row.

| Inside diameter | No. 1 | No. 1-X | Straights 12x6x3 | Total |
|---|---|---|---|---|
| 22'-6" | 295 | 13 | … | 308 |
| 23'-0" | 289 | 25 | … | 314 |
| 23'-6" | 283 | 38 | … | 321 |
| 24'-0" | 277 | 50 | … | 327 |
| 24'-6" | 270 | 63 | … | 333 |
| 25'-0" | 264 | 75 | … | 339 |
| 25'-6" | 258 | 88 | … | 346 |
| 26'-0" | 251 | 101 | … | 352 |
| 26'-6" | 245 | 113 | … | 358 |
| 27'-0" | 239 | 126 | … | 365 |
| 27'-6" | 233 | 138 | … | 371 |
| 28'-0" | 226 | 151 | … | 377 |
| 28'-6" | 220 | 163 | … | 383 |
| 29'-0" | 214 | 176 | … | 390 |
| 29'-6" | 207 | 189 | … | 396 |
| 30'-0" | 202 | 200 | … | 402 |
| 30'-6" | 195 | 214 | … | 409 |
| 31'-0" | 189 | 226 | … | 415 |
| 31'-6" | 182 | 239 | … | 421 |
| 32'-0" | 176 | 251 | … | 427 |
| 32'-6" | 170 | 264 | … | 434 |
| 33'-0" | 163 | 277 | … | 440 |
| 33'-6" | 158 | 288 | … | 446 |
| 34'-0" | 151 | 301 | … | 452 |
| 34'-6" | 145 | 314 | … | 459 |
| 35'-0" | 138 | 327 | … | 465 |
| 35'-6" | 132 | 339 | … | 471 |
| 36'-0" | 126 | 352 | … | 478 |
| 36'-6" | 119 | 365 | … | 484 |
| 37'-0" | 113 | 377 | … | 490 |
| 37'-6" | 107 | 389 | … | 496 |
| 38'-0" | 101 | 402 | … | 503 |
| 38'-6" | 94 | 415 | … | 509 |
| 39'-0" | 88 | 427 | … | 515 |
| 39'-6" | 82 | 440 | … | 522 |
| 40'-0" | 76 | 452 | … | 528 |
| 40'-6" | 69 | 465 | … | 534 |
| 41'-0" | 63 | 477 | … | 540 |
| 41'-6" | 57 | 490 | … | 547 |
| 42'-0" | 50 | 503 | … | 553 |
| 42'-6" | 44 | 515 | … | 559 |
| 43'-0" | 38 | 527 | … | 565 |
| 43'-6" | 32 | 540 | … | 572 |
| 44'-0" | 25 | 553 | … | 578 |
| 44'-6" | 19 | 565 | … | 584 |
| 45'-0" | 13 | 578 | … | 591 |
| 45'-6" | 6 | 591 | … | 597 |
| 46'-0" | … | 603 | … | 603 |
| 46'-6" | … | 604 | 5 | 609 |
| 47'-0" | … | 604 | 12 | 616 |

Totals checked: all rows sum correctly. (The 1-X count goes 603 at 46'-0" and then 604 plus straights.)

### p.151 — COMPLETE CIRCLES 12"x6"x2½" or 12"x6"x3" KEY BRICK — 12-INCH LINING

Columns: No. 3 Key 12x(6-3)x3; No. 2-X Key 12x(6-4)x3; No. 2 Key 12x(6-5)x3; No. 1 Key 12x(6-5½)x3; Straight 12x6x3; Total. Continues to p.152.

| Inside diameter | No. 3 | No. 2-X | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|
| 2'-0" | 26 | … | … | … | … | 26 |
| 2'-2" | 23 | 4 | … | … | … | 27 |
| 2'-4" | 21 | 7 | … | … | … | 28 |
| 2'-6" | 19 | 10 | … | … | … | 29 |
| 2'-8" | 17 | 13 | … | … | … | 30 |
| 2'-10" | 15 | 16 | … | … | … | 31 |
| 3'-0" | 13 | 19 | … | … | … | 32 |
| 3'-2" | 11 | 22 | … | … | … | 33 |
| 3'-4" | 9 | 25 | … | … | … | 34 |
| 3'-6" | 6 | 29 | … | … | … | 35 |
| 3'-8" | 4 | 32 | … | … | … | 36 |
| 3'-10" | 2 | 35 | … | … | … | 37 |
| 4'-0" | … | 38 | … | … | … | 38 |
| 4'-2" | … | 37 | 2 | … | … | 39 |
| 4'-4" | … | 36 | 4 | … | … | 40 |
| 4'-6" | … | 35 | 6 | … | … | 41 |
| 4'-8" | … | 34 | 8 | … | … | 42 |
| 4'-10" | … | 32 | 11 | … | … | 43 |
| 5'-0" | … | 31 | 13 | … | … | 44 |
| 5'-2" | … | 30 | 15 | … | … | 45 |
| 5'-4" | … | 29 | 17 | … | … | 46 |
| 5'-6" | … | 28 | 19 | … | … | 47 |
| 5'-8" | … | 28 | 21 | … | … | 49 |
| 5'-10" | … | 27 | 23 | … | … | 50 |
| 6'-0" | … | 25 | 26 | … | … | 51 |
| 6'-2" | … | 24 | 28 | … | … | 52 |
| 6'-4" | … | 23 | 30 | … | … | 53 |
| 6'-6" | … | 22 | 32 | … | … | 54 |
| 6'-8" | … | 21 | 34 | … | … | 55 |
| 6'-10" | … | 20 | 36 | … | … | 56 |
| 7'-0" | … | 19 | 38 | … | … | 57 |
| 7'-2" | … | 18 | 40 | … | … | 58 |
| 7'-4" | … | 17 | 42 | … | … | 59 |
| 7'-6" | … | 16 | 44 | … | … | 60 |
| 7'-8" | … | 15 | 46 | … | … | 61 |
| 7'-10" | … | 14 | 48 | … | … | 62 |
| 8'-0" | … | 13 | 50 | … | … | 63 |
| 8'-2" | … | 12 | 52 | … | … | 64 |
| 8'-4" | … | 11 | 54 | … | … | 65 |
| 8'-6" | … | 9 | [?read: 57, poorly printed] | … | … | 66 |
| 8'-8" | … | 8 | 59 | … | … | 67 |
| 8'-10" | … | 7 | 61 | … | … | 68 |
| 9'-0" | … | 6 | 63 | … | … | 69 |
| 9'-2" | … | 5 | 65 | … | … | 70 |
| 9'-4" | … | 5 | 67 | … | … | 72 |
| 9'-6" | … | 4 | 69 | … | … | 73 |
| 9'-8" | … | 2 | 72 | … | … | 74 |
| 9'-10" | … | 1 | 74 | … | … | 75 |
| 10'-0" | … | … | 76 | … | … | 76 |
| 10'-3" | … | … | 74 | 3 | … | 77 |
| 10'-6" | … | … | 72 | 7 | … | 79 |

Totals checked: all rows sum correctly (8'-6" taken as 57).

## Image (30).jpg — catalogue p.152–153

### p.152 — continuation of the 12"x6"x2½" or 12"x6"x3" KEY BRICK table — 12-INCH LINING

No. 3 and No. 2-X are blank (…) in every row.

| Inside diameter | No. 2 | No. 1 | Straight 12x6x3 | Total |
|---|---|---|---|---|
| 10'-9" | 71 | 9 | … | 80 |
| 11'-0" | 69 | 13 | … | 82 |
| 11'-3" | 68 | 16 | … | 84 |
| 11'-6" | 66 | 19 | … | 85 |
| 11'-9" | 65 | 22 | … | 87 |
| 12'-0" | 63 | 25 | … | 88 |
| 12'-3" | 61 | 29 | … | 90 |
| 12'-6" | 60 | 31 | … | 91 |
| 12'-9" | 58 | 35 | … | 93 |
| 13'-0" | 57 | 38 | … | 95 |
| 13'-3" | 55 | 41 | … | 96 |
| 13'-6" | 54 | 44 | … | 98 |
| 13'-9" | 52 | 47 | … | 99 |
| 14'-0" | 51 | 50 | … | 101 |
| 14'-3" | 49 | 53 | … | 102 |
| 14'-6" | 47 | 57 | … | 104 |
| 14'-9" | 46 | 60 | … | 106 |
| 15'-0" | 44 | 63 | … | 107 |
| 15'-3" | 43 | 66 | … | 109 |
| 15'-6" | 41 | 69 | … | 110 |
| 15'-9" | 40 | 72 | … | 112 |
| 16'-0" | 38 | 75 | … | 113 |
| 16'-3" | 36 | 79 | … | 115 |
| 16'-6" | 34 | 82 | … | 116 |
| 16'-9" | 33 | 85 | … | 118 |
| 17'-0" | 32 | 88 | … | 120 |
| 17'-3" | 30 | 91 | … | 121 |
| 17'-6" | 29 | 94 | … | 123 |
| 17'-9" | 27 | 97 | … | 124 |
| 18'-0" | 25 | 101 | … | 126 |
| 18'-3" | 23 | 104 | … | 127 |
| 18'-6" | 22 | 107 | … | 129 |
| 18'-9" | 21 | 110 | … | 131 |
| 19'-0" | 19 | 113 | … | 132 |
| 19'-3" | 18 | 116 | … | 134 |
| 19'-6" | 16 | 119 | … | 135 |
| 19'-9" | 14 | 123 | … | 137 |
| 20'-0" | 13 | 125 | … | 138 |
| 20'-3" | 11 | 129 | … | 140 |
| 20'-6" | 10 | 132 | … | 142 |
| 20'-9" | 8 | 135 | … | 143 |
| 21'-0" | 7 | 138 | … | 145 |
| 21'-3" | 5 | 141 | … | 146 |
| 21'-6" | 3 | 145 | … | 148 |
| 21'-9" | 1 | 148 | … | 149 |
| 22'-0" | … | 151 | … | 151 |
| 22'-6" | … | 151 | 3 | 154 |
| 23'-0" | … | 151 | 6 | 157 |
| 23'-6" | … | 151 | 9 | 160 |
| 24'-0" | … | 151 | 13 | 164 |
| 24'-6" | … | 151 | 16 | 167 |

Totals checked: all rows sum correctly.

### p.153 — COMPLETE CIRCLES 13½"x4½"x3", 13½"x6"x3" or 13½"x9"x3" WEDGE BRICK — 13½-INCH LINING

Columns: No. 3 Wedge 13½x6x(3-2); No. 2 Wedge 13½x6x(3-2½); No. 1 Wedge 13½x6x(3-2¾); No. 1-X Wedge 13½x6x(3-2⅞); Straights 13½x6x3; Total. "Continued Next Page".

| Inside diameter | No. 3 | No. 2 | No. 1 | No. 1-X | Straights | Total |
|---|---|---|---|---|---|---|
| 4'-6" | 85 | … | … | … | … | 85 |
| 5'-0" | 79 | 12 | … | … | … | 91 |
| 5'-6" | 73 | 25 | … | … | … | 98 |
| 6'-0" | 66 | 38 | … | … | … | 104 |
| 6'-6" | 60 | 50 | … | … | … | 110 |
| 7'-0" | 54 | 63 | … | … | … | 117 |
| 7'-6" | 47 | 76 | … | … | … | 123 |
| 8'-0" | 41 | 88 | … | … | … | 129 |
| 8'-6" | 35 | 100 | … | … | … | 135 |
| 9'-0" | 29 | 113 | … | … | … | 142 |
| 9'-6" | 22 | 126 | … | … | … | 148 |
| 10'-0" | 16 | 138 | … | … | … | 154 |
| 10'-6" | 9 | 151 | … | … | … | 160 |
| 11'-0" | 3 | 164 | … | … | … | 167 |
| 11'-3" | … | 170 | … | … | … | 170 |
| 11'-6" | … | 167 | 6 | … | … | 173 |
| 12'-0" | … | 160 | 19 | … | … | 179 |
| 12'-6" | … | 154 | 32 | … | … | 186 |
| 13'-0" | … | 148 | 44 | … | … | 192 |
| 13'-6" | … | 141 | 57 | … | … | 198 |
| 14'-0" | … | 135 | 69 | … | … | 204 |
| 14'-6" | … | 129 | 82 | … | … | 211 |
| 15'-0" | … | 123 | 94 | … | … | 217 |
| 15'-6" | … | 116 | 107 | … | … | 223 |
| 16'-0" | … | 110 | 119 | … | … | 229 |
| 16'-6" | … | 104 | 132 | … | … | 236 |
| 17'-0" | … | 97 | 145 | … | … | 242 |
| 17'-6" | … | 92 | 157 | … | … | 249 |
| 18'-0" | … | 85 | 170 | … | … | 255 |
| 18'-6" | … | 79 | 182 | … | … | 261 |
| 19'-0" | … | 72 | 195 | … | … | 267 |
| 19'-6" | … | 66 | 207 | … | … | 273 |
| 20'-0" | … | 60 | 220 | … | … | 280 |
| 20'-6" | … | 53 | 233 | … | … | 286 |
| 21'-0" | … | 48 | 244 | … | … | 292 |
| 21'-6" | … | 41 | 258 | … | … | 299 |
| 22'-0" | … | 35 | 270 | … | … | 305 |
| 22'-6" | … | 28 | 283 | … | … | 311 |
| 23'-0" | … | 22 | 295 | … | … | 317 |
| 23'-6" | … | 16 | 308 | … | … | 324 |
| 24'-0" | … | 9 | 321 | … | … | 330 |
| 24'-6" | … | 4 | 332 | … | … | 336 |
| 24'-9" | … | … | 339 | … | … | 339 |
| 25'-0" | … | … | 336 | 7 | … | 343 |
| 25'-6" | … | … | 330 | 19 | … | 349 |
| 26'-0" | … | … | 324 | 31 | … | 355 |
| 26'-6" | … | … | 317 | 44 | … | 361 |
| 27'-0" | … | … | 311 | 57 | … | 368 |
| 27'-6" | … | … | 305 | 69 | … | 374 |
| 28'-0" | … | … | 298 | 82 | … | 380 |

Totals checked: all rows sum correctly. (There is a small pen or ink mark on the "22'-0"" label; it may be handwritten, and it is not data.)

---

## Summary

- No edition, year or publisher imprint is printed on pp.124–153. Only the page numbers and the running heads (6-, 9-, 12-, 13½-INCH LINING) appear. No handwritten annotations, apart from a possible ink mark on p.153.
- **Ring/circle brick counts (complete circles, by inside diameter):** every page from p.124 to p.153.
  - Rotary kiln blocks: 9x6x4 (p.124), 9x9x4 (pp.141–142), 12x9x4 (pp.143–144).
  - Arch/wedge-type rotary liners KL-1/2/3-A (p.125) and KL-1/2/3-W (p.145).
  - Basic-brick rotary arches/wedges 9x6x3 and 9x6x3½, with ring closure brick RCA/RCW: pp.126–127, 146–147.
  - Wedge-type liners with ⅔ and ¾ splits: pp.139–140.
  - 9" wedge circles: 9x4½x2½ (pp.128–130) and 9x4½x3 (pp.131–133).
  - 9" key circles: 9x4½ (pp.134–135) and 9x6 (pp.136–138).
  - Blast-furnace 1K/2K keys: p.148.
  - 12" wedges (pp.149–150), 12" keys (pp.151–152), 13½" wedges (p.153, continues past my range).
- **Arch/key/wedge counts by span and rise:** none in this range. All tables are complete circles by diameter.
- **Dome brick:** none. **Skewbacks:** none.
- **Formulas:** none printed.
- **Notes/limits:**
  - p.125 and p.145: KL-4/KL-5 closure shapes for keying each ring; "two of each should be ordered for each ring", with T/A and T/W dimension tables.
  - Ring closure diameter split at 13'-6" (pp.126, 127, 146, 147).
  - p.148: 1K/2K sizes are on p.107.
- **Doubtful cells:**
  - p.128, 3'-9" No. 1: reads 62, total implies 60.
  - p.145, 6'-6" KL-3-W: reads 33, total implies 38.
  - p.151, 8'-6" No. 2: poorly printed, taken as 57.
  - The small 32nd-inch fractions on pp.125–127, 139–140, 145–147 are [?read].


---


Conventions: `…` = the dotted leader printed in an empty cell (no brick of that shape). All scans are two-page spreads rotated 90°; left page = even number. Columns with every cell blank are kept so the table matches the print. Totals were checked against row sums; all checked rows agree unless a mismatch line follows the table.

## Image (31).jpg — catalogue p.154–155

### p.154 — COMPLETE CIRCLES — 13½"x4½"x3", 13½"x6"x3" or 13½"x9"x3" WEDGE BRICK — 13½-INCH LINING

(continued from previous page.) Header: SHAPES REQUIRED TO TURN CIRCLE. Columns: No. 3 Wedge 13½x6x(3-2); No. 2 Wedge 13½x6x(3-2½); No. 1 Wedge 13½x6x(3-2¾); No. 1-X Wedge 13½x6x(3-2⅞); Straights 13½x6x3.

| Inside diameter | No. 3 | No. 2 | No. 1 | No. 1-X | Straights | Total |
|---|---|---|---|---|---|---|
| 28'-6" | … | … | 292 | 94 | … | 386 |
| 29'-0" | … | … | 286 | 107 | … | 393 |
| 29'-6" | … | … | 280 | 119 | … | 399 |
| 30'-0" | … | … | 273 | 132 | … | 405 |
| 30'-6" | … | … | 267 | 145 | … | 412 |
| 31'-0" | … | … | 261 | 157 | … | 418 |
| 31'-6" | … | … | 254 | 170 | … | 424 |
| 32'-0" | … | … | 248 | 182 | … | 430 |
| 32'-6" | … | … | 242 | 195 | … | 437 |
| 33'-0" | … | … | 236 | 207 | … | 443 |
| 33'-6" | … | … | 229 | 220 | … | 449 |
| 34'-0" | … | … | 223 | 233 | … | 456 |
| 34'-6" | … | … | 217 | 245 | … | 462 |
| 35'-0" | … | … | 210 | 258 | … | 468 |
| 35'-6" | … | … | 204 | 270 | … | 474 |
| 36'-0" | … | … | 198 | 283 | … | 481 |
| 36'-6" | … | … | 192 | 295 | … | 487 |
| 37'-0" | … | … | 185 | 308 | … | 493 |
| 37'-6" | … | … | 179 | 321 | … | 500 |
| 38'-0" | … | … | 173 | 333 | … | 506 |
| 38'-6" | … | … | 167 | 345 | … | 512 |
| 39'-0" | … | … | 160 | 358 | … | 518 |
| 39'-6" | … | … | 154 | 371 | … | 525 |
| 40'-0" | … | … | 148 | 383 | … | 531 |
| 40'-6" | … | … | 141 | 396 | … | 537 |
| 41'-0" | … | … | 135 | 408 | … | 543 |
| 41'-6" | … | … | 129 | 421 | … | 550 |
| 42'-0" | … | … | 122 | 434 | … | 556 |
| 42'-6" | … | … | 116 | 446 | … | 562 |
| 43'-0" | … | … | 110 | 459 | … | 569 |
| 43'-6" | … | … | 104 | 471 | … | 575 |
| 44'-0" | … | … | 97 | 484 | … | 581 |
| 44'-6" | … | … | 91 | 496 | … | 587 |
| 45'-0" | … | … | 85 | 509 | … | 594 |
| 45'-6" | … | … | 79 | 521 | … | 600 |
| 46'-0" | … | … | 72 | 534 | … | 606 |
| 46'-6" | … | … | 66 | 547 | … | 613 |
| 47'-0" | … | … | 60 | 559 | … | 619 |
| 47'-6" | … | … | 54 | 571 | … | 625 |
| 48'-0" | … | … | 47 | 584 | … | 631 |
| 48'-6" | … | … | 41 | 597 | … | 638 |
| 49'-0" | … | … | 35 | 609 | … | 644 |
| 49'-6" | … | … | 28 | 622 | … | 650 |
| 50'-0" | … | … | 22 | 635 | … | 657 |
| 50'-6" | … | … | 16 | 647 | … | 663 |
| 51'-0" | … | … | 9 | 660 | … | 669 |
| 51'-6" | … | … | 3 | 672 | … | 675 |
| 51'-9" | … | … | … | 679 | … | 679 |
| 52'-0" | … | … | … | 679 | 3 | 682 |
| 52'-6" | … | … | … | 679 | 9 | 688 |

All totals check.

### p.155 — COMPLETE CIRCLES—BASIC BRICK ONLY — 13½"x4½"x3" KEY BRICK — 13½-INCH LINING

Columns: No. 4 Key 13½x(4½-2¼)x3; No. 3 Key 13½x(4½-3)x3; No. 2 Key 13½x(4½-3½)x3; No. 1 Key 13½x(4½-4)x3; Straights 13½x4½x3.

| Inside diameter | No. 4 | No. 3 | No. 2 | No. 1 | Straights | Total |
|---|---|---|---|---|---|---|
| 2'-3" | 38 | … | … | … | … | 38 |
| 2'-4" | 37 | 2 | … | … | … | 39 |
| 2'-6" | 34 | 6 | … | … | … | 40 |
| 2'-8" | 31 | 11 | … | … | … | 42 |
| 2'-10" | 28 | 15 | … | … | … | 43 |
| 3'-0" | 25 | 19 | … | … | … | 44 |
| 3'-2" | 23 | 23 | … | … | … | 46 |
| 3'-4" | 20 | 27 | … | … | … | 47 |
| 3'-6" | 17 | 32 | … | … | … | 49 |
| 3'-8" | 14 | 36 | … | … | … | 50 |
| 3'-10" | 11 | 40 | … | … | … | 51 |
| 4'-0" | 9 | 44 | … | … | … | 53 |
| 4'-2" | 6 | 48 | … | … | … | 54 |
| 4'-4" | 3 | 53 | … | … | … | 56 |
| 4'-6" | … | 57 | … | … | … | 57 |
| 4'-8" | … | 54 | 4 | … | … | 58 |
| 4'-10" | … | 51 | 9 | … | … | 60 |
| 5'-0" | … | 48 | 13 | … | … | 61 |
| 5'-2" | … | 46 | 17 | … | … | 63 |
| 5'-4" | … | 43 | 21 | … | … | 64 |
| 5'-6" | … | 40 | 25 | … | … | 65 |
| 5'-8" | … | 37 | 30 | … | … | 67 |
| 5'-10" | … | 34 | 34 | … | … | 68 |
| 6'-0" | … | 32 | 38 | … | … | 70 |
| 6'-2" | … | 29 | 42 | … | … | 71 |
| 6'-4" | … | 26 | 46 | … | … | 72 |
| 6'-6" | … | 23 | 51 | … | … | 74 |
| 6'-8" | … | 20 | 55 | … | … | 75 |
| 6'-10" | … | 18 | 59 | … | … | 77 |
| 7'-0" | … | 15 | 63 | … | … | 78 |
| 7'-2" | … | 12 | 67 | … | … | 79 |
| 7'-4" | … | 9 | 72 | … | … | 81 |
| 7'-6" | … | 6 | 76 | … | … | 82 |
| 7'-8" | … | 4 | 80 | … | … | 84 |
| 7'-10" | … | 1 | 84 | … | … | 85 |
| 8'-0" | … | … | 84 | 2 | … | 86 |
| 8'-2" | … | … | 83 | 5 | … | 88 |
| 8'-4" | … | … | 81 | 8 | … | 89 |
| 8'-6" | … | … | 80 | 11 | … | 91 |
| 8'-8" | … | … | 78 | 14 | … | 92 |
| 8'-10" | … | … | 77 | 16 | … | 93 |
| 9'-0" | … | … | 76 | 19 | … | 95 |
| 9'-2" | … | … | 74 | 22 | … | 96 |
| 9'-4" | … | … | 73 | 24 | … | 97 |
| 9'-6" | … | … | 71 | 28 | … | 99 |
| 9'-8" | … | … | 70 | 30 | … | 100 |
| 9'-10" | … | … | 69 | 33 | … | 102 |

"Continued Next Page". All totals check.

## Image (32).jpg — catalogue p.156–157

### p.156 — COMPLETE CIRCLES—BASIC BRICK ONLY — 13½"x4½"x3" KEY BRICK — 13½-INCH LINING (continued)

Same columns as p.155.

| Inside diameter | No. 4 | No. 3 | No. 2 | No. 1 | Straights | Total |
|---|---|---|---|---|---|---|
| 10'-0" | … | … | 67 | 36 | … | 103 |
| 10'-2" | … | … | 66 | 38 | … | 104 |
| 10'-4" | … | … | 65 | 41 | … | 106 |
| 10'-6" | … | … | 63 | 44 | … | 107 |
| 10'-8" | … | … | 62 | 47 | … | 109 |
| 10'-10" | … | … | 60 | 50 | … | 110 |
| 11'-0" | … | … | 59 | 52 | … | 111 |
| 11'-2" | … | … | 58 | 55 | … | 113 |
| 11'-4" | … | … | 56 | 58 | … | 114 |
| 11'-6" | … | … | 55 | 61 | … | 116 |
| 11'-8" | … | … | 53 | 64 | … | 117 |
| 11'-10" | … | … | 52 | 66 | … | 118 |
| 12'-0" | … | … | 51 | 69 | … | 120 |
| 12'-2" | … | … | 49 | 72 | … | 121 |
| 12'-4" | … | … | 48 | 75 | … | 123 |
| 12'-6" | … | … | 46 | 78 | … | 124 |
| 12'-8" | … | … | 45 | 80 | … | 125 |
| 12'-10" | … | … | 44 | 83 | … | 127 |
| 13'-0" | … | … | 42 | 86 | … | 128 |
| 13'-2" | … | … | 41 | 89 | … | 130 |
| 13'-4" | … | … | 39 | 92 | … | 131 |
| 13'-6" | … | … | 38 | 94 | … | 132 |
| 13'-8" | … | … | 37 | 97 | … | 134 |
| 13'-10" | … | … | 35 | 100 | … | 135 |
| 14'-0" | … | … | 34 | 103 | … | 137 |
| 14'-2" | … | … | 32 | 106 | … | 138 |
| 14'-4" | … | … | 31 | 108 | … | 139 |
| 14'-6" | … | … | 30 | 111 | … | 141 |
| 14'-8" | … | … | 28 | 114 | … | 142 |
| 14'-10" | … | … | 27 | 117 | … | 144 |
| 15'-0" | … | … | 25 | 120 | … | 145 |
| 15'-2" | … | … | 24 | 122 | … | 146 |
| 15'-4" | … | … | 23 | 125 | … | 148 |
| 15'-6" | … | … | 21 | 128 | … | 149 |
| 15'-8" | … | … | 20 | 131 | … | 151 |
| 15'-10" | … | … | 18 | 134 | … | 152 |
| 16'-0" | … | … | 17 | 136 | … | 153 |
| 16'-6" | … | … | 13 | 145 | … | 158 |
| 17'-0" | … | … | 9 | 153 | … | 162 |
| 17'-6" | … | … | 4 | 162 | … | 166 |
| 18'-0" | … | … | … | 170 | … | 170 |
| 18'-6" | … | … | … | 170 | 4 | 174 |
| 19'-0" | … | … | … | 170 | 8 | 178 |
| 19'-6" | … | … | … | 170 | 13 | 183 |
| 20'-0" | … | … | … | 170 | 17 | 187 |

All totals check.

### p.157 — COMPLETE CIRCLES — 13½"x6"x2½" or 13½"x6"x3" KEY BRICK — 13½-INCH LINING

Columns: No. 3 Key 13½x(6-3)x3; No. 2-X Key 13½x(6-3¾)x3; No. 2 Key 13½x(6-4⅜)x3; No. 1 Key 13½x(6-5)x3; Straights 13½x6x3.

| Inside diameter | No. 3 | No. 2-X | No. 2 | No. 1 | Straights | Total |
|---|---|---|---|---|---|---|
| 2'-3" | 29 | … | … | … | … | 29 |
| 2'-4" | 27 | 2 | … | … | … | 29 |
| 2'-6" | 24 | 6 | … | … | … | 30 |
| 2'-8" | 20 | 11 | … | … | … | 31 |
| 2'-10" | 17 | 15 | … | … | … | 32 |
| 3'-0" | 14 | 19 | … | … | … | 33 |
| 3'-2" | 11 | 23 | … | … | … | 34 |
| 3'-4" | 8 | 27 | … | … | … | 35 |
| 3'-6" | 5 | 32 | … | … | … | 37 |
| 3'-8" | 2 | 36 | … | … | … | 38 |
| 3'-9" | … | 38 | … | … | … | 38 |
| 3'-10" | … | 37 | 2 | … | … | 39 |
| 4'-0" | … | 34 | 6 | … | … | 40 |
| 4'-2" | … | 31 | 10 | … | … | 41 |
| 4'-4" | … | 28 | 14 | … | … | 42 |
| 4'-6" | … | 26 | 17 | … | … | 43 |
| 4'-8" | … | 23 | 21 | … | … | 44 |
| 4'-10" | … | 20 | 25 | … | … | 45 |
| 5'-0" | … | 18 | 28 | … | … | 46 |
| 5'-2" | … | 15 | 32 | … | … | 47 |
| 5'-4" | … | 12 | 36 | … | … | 48 |
| 5'-6" | … | 9 | 40 | … | … | 49 |
| 5'-8" | … | 7 | 43 | … | … | 50 |
| 5'-10" | … | 4 | 47 | … | … | 51 |
| 6'-0" | … | 1 | 51 | … | … | 52 |
| 6'-1" | … | … | 52 | 1 | … | 53 |
| 6'-2" | … | … | 51 | 2 | … | 53 |
| 6'-4" | … | … | 49 | 5 | … | 54 |
| 6'-6" | … | … | 48 | 7 | … | 55 |
| 6'-8" | … | … | 46 | 10 | … | 56 |
| 6'-10" | … | … | 44 | 13 | … | 57 |
| 7'-0" | … | … | 43 | 15 | … | 58 |
| 7'-2" | … | … | 41 | 19 | … | 60 |
| 7'-4" | … | … | 40 | 21 | … | 61 |
| 7'-6" | … | … | 38 | 24 | … | 62 |
| 7'-8" | … | … | 36 | 27 | … | 63 |
| 7'-10" | … | … | 35 | 29 | … | 64 |
| 8'-0" | … | … | 33 | 32 | … | 65 |
| 8'-2" | … | … | 31 | 35 | … | 66 |
| 8'-4" | … | … | 30 | 37 | … | 67 |
| 8'-6" | … | … | 28 | 40 | … | 68 |
| 8'-8" | … | … | 26 | 43 | … | 69 |
| 8'-10" | … | … | 24 | 46 | … | 70 |
| 9'-0" | … | … | 23 | 48 | … | 71 |
| 9'-2" | … | … | 21 | 51 | … | 72 |
| 9'-4" | … | … | 19 | 54 | … | 73 |
| 9'-6" | … | … | 18 | 56 | … | 74 |
| 9'-8" | … | … | 16 | 59 | … | 75 |
| 9'-10" | … | … | 14 | 62 | … | 76 |
| 10'-0" | … | … | 13 | 64 | … | 77 |
| 10'-2" | … | … | 11 | 67 | … | 78 |

"Continued Next Page". All totals check. (The 6'-1" row prints between 6'-0" and 6'-2".)

## Image (33).jpg — catalogue p.158–159

### p.158 — COMPLETE CIRCLES — 13½"x6"x2½" or 13½"x6"x3" KEY BRICK — 13½-INCH LINING (continued)

Same columns as p.157.

| Inside diameter | No. 3 | No. 2-X | No. 2 | No. 1 | Straights | Total |
|---|---|---|---|---|---|---|
| 10'-4" | … | … | 9 | 70 | … | 79 |
| 10'-6" | … | … | 7 | 73 | … | 80 |
| 10'-8" | … | … | 6 | 75 | … | 81 |
| 10'-10" | … | … | 4 | 78 | … | 82 |
| 11'-0" | … | … | 3 | 81 | … | 84 |
| 11'-2" | … | … | 1 | 84 | … | 85 |
| 11'-3" | … | … | … | 85 | … | 85 |
| 11'-6" | … | … | … | 85 | 2 | 87 |
| 12'-0" | … | … | … | 85 | 5 | 90 |
| 12'-6" | … | … | … | 85 | 8 | 93 |
| 13'-0" | … | … | … | 85 | 11 | 96 |
| 13'-6" | … | … | … | 85 | 14 | 99 |
| 14'-0" | … | … | … | 85 | 17 | 102 |
| 14'-6" | … | … | … | 85 | 20 | 105 |
| 15'-0" | … | … | … | 85 | 24 | 109 |
| 15'-6" | … | … | … | 85 | 27 | 112 |
| 16'-0" | … | … | … | 85 | 30 | 115 |
| 16'-6" | … | … | … | 85 | 33 | 118 |
| 17'-0" | … | … | … | 85 | 36 | 121 |
| 17'-6" | … | … | … | 85 | 39 | 124 |
| 18'-0" | … | … | … | 85 | 42 | 127 |
| 18'-6" | … | … | … | 85 | 46 | 131 |
| 19'-0" | … | … | … | 85 | 49 | 134 |
| 19'-6" | … | … | … | 85 | 52 | 137 |
| 20'-0" | … | … | … | 85 | 55 | 140 |
| 20'-6" | … | … | … | 85 | 58 | 143 |
| 21'-0" | … | … | … | 85 | 61 | 146 |
| 21'-6" | … | … | … | 85 | 64 | 149 |
| 22'-0" | … | … | … | 85 | 68 | 153 |
| 22'-6" | … | … | … | 85 | 71 | 156 |
| 23'-0" | … | … | … | 85 | 74 | 159 |
| 23'-6" | … | … | … | 85 | 77 | 162 |
| 24'-0" | … | … | … | 85 | 80 | 165 |
| 24'-6" | … | … | … | 85 | 83 | 168 |
| 25'-0" | … | … | … | 85 | 86 | 171 |
| 25'-6" | … | … | … | 85 | 89 | 174 |
| 26'-0" | … | … | … | 85 | 93 | 178 |
| 26'-6" | … | … | … | 85 | 96 | 181 |
| 27'-0" | … | … | … | 85 | 99 | 184 |
| 27'-6" | … | … | … | 85 | 102 | 187 |
| 28'-0" | … | … | … | 85 | 105 | 190 |
| 28'-6" | … | … | … | 85 | 108 | 193 |
| 29'-0" | … | … | … | 85 | 111 | 196 |
| 29'-6" | … | … | … | 85 | 115 | 200 |
| 30'-0" | … | … | … | 85 | 118 | 203 |
| 30'-6" | … | … | … | 85 | 121 | 206 |
| 31'-0" | … | … | … | 85 | 124 | 209 |
| 31'-6" | … | … | … | 85 | 127 | 212 |
| 32'-0" | … | … | … | 85 | 130 | 215 |
| 32'-6" | … | … | … | 85 | 133 | 218 |
| 33'-0" | … | … | … | 85 | 137 | 222 |

All totals check.

### p.159 — COMPLETE CIRCLES — 15"x6"x3" or 15"x9"x3" WEDGE BRICK — 15-INCH LINING

Columns: No. 3 Wedge 15x6x(3-2); No. 2 Wedge 15x6x(3-2½); No. 1 Wedge 15x6x(3-2¾); No. 1-X Wedge 15x6x(3-2⅞); Straights 15x6x3.

| Inside diameter | No. 3 | No. 2 | No. 1 | No. 1-X | Straights | Total |
|---|---|---|---|---|---|---|
| 5'-0" | 95 | … | … | … | … | 95 |
| 5'-6" | 88 | 13 | … | … | … | 101 |
| 6'-0" | 82 | 25 | … | … | … | 107 |
| 6'-6" | 75 | 38 | … | … | … | 113 |
| 7'-0" | 69 | 51 | … | … | … | 120 |
| 7'-6" | 63 | 63 | … | … | … | 126 |
| 8'-0" | 57 | 75 | … | … | … | 132 |
| 8'-6" | 50 | 88 | … | … | … | 138 |
| 9'-0" | 44 | 101 | … | … | … | 145 |
| 9'-6" | 38 | 113 | … | … | … | 151 |
| 10'-0" | 31 | 126 | … | … | … | 157 |
| 10'-6" | 25 | 138 | … | … | … | 163 |
| 11'-0" | 19 | 151 | … | … | … | 170 |
| 11'-6" | 13 | 163 | … | … | … | 176 |
| 12'-0" | 6 | 176 | … | … | … | 182 |
| 12'-6" | … | 189 | … | … | … | 189 |
| 13'-0" | … | 182 | 13 | … | … | 195 |
| 13'-6" | … | 176 | 25 | … | … | 201 |
| 14'-0" | … | 170 | 37 | … | … | 207 |
| 14'-6" | … | 164 | 50 | … | … | 214 |
| 15'-0" | … | 157 | 63 | … | … | 220 |
| 15'-6" | … | 151 | 75 | … | … | 226 |
| 16'-0" | … | 145 | 88 | … | … | 233 |
| 16'-6" | … | 138 | 101 | … | … | 239 |
| 17'-0" | … | 132 | 113 | … | … | 245 |
| 17'-6" | … | 126 | 125 | … | … | 251 |
| 18'-0" | … | 120 | 138 | … | … | 258 |
| 18'-6" | … | 113 | 151 | … | … | 264 |
| 19'-0" | … | 107 | 163 | … | … | 270 |
| 19'-6" | … | 100 | 176 | … | … | 276 |
| 20'-0" | … | 94 | 189 | … | … | 283 |
| 20'-6" | … | 88 | 201 | … | … | 289 |
| 21'-0" | … | 82 | 213 | … | … | 295 |
| 21'-6" | … | 76 | 226 | … | … | 302 |
| 22'-0" | … | 69 | 239 | … | … | 308 |
| 22'-6" | … | 63 | 251 | … | … | 314 |
| 23'-0" | … | 56 | 264 | … | … | 320 |
| 23'-6" | … | 50 | 277 | … | … | 327 |
| 24'-0" | … | 44 | 289 | … | … | 333 |
| 24'-6" | … | 38 | 301 | … | … | 339 |
| 25'-0" | … | 32 | 314 | … | … | 346 |
| 25'-6" | … | 25 | 327 | … | … | 352 |
| 26'-0" | … | 19 | 339 | … | … | 358 |
| 26'-6" | … | 12 | 352 | … | … | 364 |
| 27'-0" | … | 6 | 365 | … | … | 371 |
| 27'-6" | … | … | 377 | … | … | 377 |
| 28'-0" | … | … | 371 | 12 | … | 383 |
| 28'-6" | … | … | 365 | 25 | … | 390 |
| 29'-0" | … | … | 358 | 38 | … | 396 |
| 29'-6" | … | … | 352 | 50 | … | 402 |

"Continued Next Page". All totals check.

## Image (34).jpg — catalogue p.160–161

### p.160 — COMPLETE CIRCLES — 15"x6"x3" or 15"x9"x3" WEDGE BRICK — 15-INCH LINING (continued)

Same columns as p.159.

| Inside diameter | No. 3 | No. 2 | No. 1 | No. 1-X | Straights | Total |
|---|---|---|---|---|---|---|
| 30'-0" | … | … | 345 | 63 | … | 408 |
| 30'-6" | … | … | 339 | 76 | … | 415 |
| 31'-0" | … | … | 333 | 88 | … | 421 |
| 31'-6" | … | … | 327 | 100 | … | 427 |
| 32'-0" | … | … | 321 | 113 | … | 434 |
| 32'-6" | … | … | 314 | 126 | … | 440 |
| 33'-0" | … | … | 308 | 138 | … | 446 |
| 33'-6" | … | … | 302 | 150 | … | 452 |
| 34'-0" | … | … | 295 | 164 | … | 459 |
| 34'-6" | … | … | 289 | 176 | … | 465 |
| 35'-0" | … | … | 283 | 188 | … | 471 |
| 35'-6" | … | … | 277 | 201 | … | 478 |
| 36'-0" | … | … | 270 | 214 | … | 484 |
| 36'-6" | … | … | 264 | 226 | … | 490 |
| 37'-0" | … | … | 258 | 238 | … | 496 |
| 37'-6" | … | … | 251 | 252 | … | 503 |
| 38'-0" | … | … | 245 | 264 | … | 509 |
| 38'-6" | … | … | 239 | 276 | … | 515 |
| 39'-0" | … | … | 232 | 289 | … | 521 |
| 39'-6" | … | … | 226 | 302 | … | 528 |
| 40'-0" | … | … | 220 | 314 | … | 534 |
| 40'-6" | … | … | 214 | 326 | … | 540 |
| 41'-0" | … | … | 208 | 339 | … | 547 |
| 41'-6" | … | … | 201 | 352 | … | 553 |
| 42'-0" | … | … | 195 | 364 | … | 559 |
| 42'-6" | … | … | 188 | 377 | … | 565 |
| 43'-0" | … | … | 182 | 390 | … | 572 |
| 43'-6" | … | … | 176 | 402 | … | 578 |
| 44'-0" | … | … | 170 | 414 | … | 584 |
| 44'-6" | … | … | 164 | 427 | … | 591 |
| 45'-0" | … | … | 157 | 440 | … | 597 |
| 45'-6" | … | … | 151 | 452 | … | 603 |
| 46'-0" | … | … | 144 | 465 | … | 609 |
| 46'-6" | … | … | 138 | 478 | … | 616 |
| 47'-0" | … | … | 132 | 490 | … | 622 |
| 47'-6" | … | … | 126 | 502 | … | 628 |
| 48'-0" | … | … | 120 | 515 | … | 635 |
| 48'-6" | … | … | 113 | 528 | … | 641 |
| 49'-0" | … | … | 107 | 540 | … | 647 |
| 49'-6" | … | … | 100 | 553 | … | 653 |
| 50'-0" | … | … | 94 | 566 | … | 660 |
| 51'-0" | … | … | 82 | 590 | … | 672 |
| 52'-0" | … | … | 69 | 616 | … | 685 |
| 53'-0" | … | … | 56 | 641 | … | 697 |
| 54'-0" | … | … | 44 | 666 | … | 710 |
| 55'-0" | … | … | 31 | 691 | … | 722 |
| 56'-0" | … | … | 19 | 716 | … | 735 |
| 57'-0" | … | … | 6 | 742 | … | 748 |
| 58'-0" | … | … | … | 754 | 6 | 760 |
| 59'-0" | … | … | … | 754 | 19 | 773 |
| 60'-0" | … | … | … | 754 | 31 | 785 |

All totals check.

### p.161 — COMPLETE CIRCLES — 18"x6"x3" or 18"x9"x3" WEDGE BRICK — 18-INCH LINING

Columns: No. 3 Wedge 18x6x(3-2); No. 2 Wedge 18x6x(3-2½); No. 1 Wedge 18x6x(3-2¾); No. 1-X Wedge 18x6x(3-2⅞); Straights 18x6x3.

| Inside diameter | No. 3 | No. 2 | No. 1 | No. 1-X | Straights | Total |
|---|---|---|---|---|---|---|
| 6'-0" | 113 | … | … | … | … | 113 |
| 6'-6" | 107 | 13 | … | … | … | 120 |
| 7'-0" | 101 | 25 | … | … | … | 126 |
| 7'-6" | 94 | 38 | … | … | … | 132 |
| 8'-0" | 88 | 50 | … | … | … | 138 |
| 8'-6" | 82 | 63 | … | … | … | 145 |
| 9'-0" | 76 | 75 | … | … | … | 151 |
| 9'-6" | 69 | 88 | … | … | … | 157 |
| 10'-0" | 63 | 101 | … | … | … | 164 |
| 10'-6" | 57 | 113 | … | … | … | 170 |
| 11'-0" | 50 | 126 | … | … | … | 176 |
| 11'-6" | 44 | 138 | … | … | … | 182 |
| 12'-0" | 38 | 151 | … | … | … | 189 |
| 12'-6" | 32 | 163 | … | … | … | 195 |
| 13'-0" | 25 | 176 | … | … | … | 201 |
| 13'-6" | 19 | 188 | … | … | … | 207 |
| 14'-0" | 13 | 201 | … | … | … | 214 |
| 14'-6" | 6 | 214 | … | … | … | 220 |
| 15'-0" | … | 226 | … | … | … | 226 |
| 15'-6" | … | 220 | 13 | … | … | 233 |
| 16'-0" | … | 214 | 25 | … | … | 239 |
| 16'-6" | … | 207 | 38 | … | … | 245 |
| 17'-0" | … | 201 | 50 | … | … | 251 |
| 17'-6" | … | 195 | 63 | … | … | 258 |
| 18'-0" | … | 189 | 75 | … | … | 264 |
| 18'-6" | … | 182 | 88 | … | … | 270 |
| 19'-0" | … | 176 | 100 | … | … | 276 |
| 19'-6" | … | 170 | 113 | … | … | 283 |
| 20'-0" | … | 163 | 126 | … | … | 289 |
| 20'-6" | … | 157 | 138 | … | … | 295 |
| 21'-0" | … | 151 | 151 | … | … | 302 |
| 21'-6" | … | 145 | 163 | … | … | 308 |
| 22'-0" | … | 138 | 176 | … | … | 314 |
| 22'-6" | … | 132 | 188 | … | … | 320 |
| 23'-0" | … | 126 | 201 | … | … | 327 |
| 23'-6" | … | 119 | 214 | … | … | 333 |
| 24'-0" | … | 113 | 226 | … | … | 339 |
| 24'-6" | … | 107 | 239 | … | … | 346 |
| 25'-0" | … | 101 | 251 | … | … | 352 |
| 25'-6" | … | 94 | 264 | … | … | 358 |
| 26'-0" | … | 88 | 276 | … | … | 364 |
| 26'-6" | … | 82 | 289 | … | … | 371 |
| 27'-0" | … | 75 | 302 | … | … | 377 |
| 27'-6" | … | 69 | 314 | … | … | 383 |
| 28'-0" | … | 63 | 327 | … | … | 390 |
| 28'-6" | … | 57 | 339 | … | … | 396 |
| 29'-0" | … | 50 | 352 | … | … | 402 |
| 29'-6" | … | 44 | 364 | … | … | 408 |
| 30'-0" | … | 38 | 377 | … | … | 415 |
| 30'-6" | … | 31 | 390 | … | … | 421 |
| 31'-0" | … | 25 | 402 | … | … | 427 |

"Continued Next Page". All totals check.

## Image (35).jpg — catalogue p.162–163

### p.162 — COMPLETE CIRCLES — 18"x6"x3" or 18"x9"x3" WEDGE BRICK — 18-INCH LINING (continued)

Same columns as p.161: No. 3 Wedge 18x6x(3-2); No. 2 Wedge 18x6x(3-2½); No. 1 Wedge 18x6x(3-2¾); No. 1-X Wedge 18x6x(3-2⅞); Straights 18x6x3.

| Inside diameter | No. 3 | No. 2 | No. 1 | No. 1-X | Straights | Total |
|---|---|---|---|---|---|---|
| 31'-6" | … | 19 | 415 | … | … | 434 |
| 32'-0" | … | 13 | 427 | … | … | 440 |
| 32'-6" | … | 6 | 440 | … | … | 446 |
| 33'-0" | … | … | 452 | … | … | 452 |
| 33'-6" | … | … | 446 | 13 | … | 459 |
| 34'-0" | … | … | 440 | 25 | … | 465 |
| 34'-6" | … | … | 433 | 38 | … | 471 |
| 35'-0" | … | … | 427 | 51 | … | 478 |
| 35'-6" | … | … | 421 | 63 | … | 484 |
| 36'-0" | … | … | 415 | 75 | … | 490 |
| 36'-6" | … | … | 408 | 88 | … | 496 |
| 37'-0" | … | … | 402 | 101 | … | 503 |
| 37'-6" | … | … | 396 | 113 | … | 509 |
| 38'-0" | … | … | 390 | 125 | … | 515 |
| 38'-6" | … | … | 384 | 138 | … | 522 |
| 39'-0" | … | … | 377 | 151 | … | 528 |
| 39'-6" | … | … | 371 | 163 | … | 534 |
| 40'-0" | … | … | 364 | 176 | … | 540 |
| 40'-6" | … | … | 358 | 189 | … | 547 |
| 41'-0" | … | … | 352 | 201 | … | 553 |
| 41'-6" | … | … | 345 | 214 | … | 559 |
| 42'-0" | … | … | 339 | 226 | … | 565 |
| 42'-6" | … | … | 333 | 239 | … | 572 |
| 43'-0" | … | … | 327 | 251 | … | 578 |
| 44'-0" | … | … | 314 | 277 | … | 591 |
| 45'-0" | … | … | 301 | 302 | … | 603 |
| 46'-0" | … | … | 289 | 327 | … | 616 |
| 47'-0" | … | … | 276 | 352 | … | 628 |
| 48'-0" | … | … | 264 | 377 | … | 641 |
| 49'-0" | … | … | 251 | 402 | … | 653 |
| 50'-0" | … | … | 239 | 427 | … | 666 |
| 51'-0" | … | … | 226 | 453 | … | 679 |
| 52'-0" | … | … | 213 | 478 | … | 691 |
| 53'-0" | … | … | 201 | 503 | … | 704 |
| 54'-0" | … | … | 188 | 528 | … | 716 |
| 55'-0" | … | … | 176 | 553 | … | 729 |
| 56'-0" | … | … | 163 | 578 | … | 741 |
| 57'-0" | … | … | 151 | 603 | … | 754 |
| 58'-0" | … | … | 138 | 629 | … | 767 |
| 59'-0" | … | … | 126 | 653 | … | 779 |
| 60'-0" | … | … | 113 | 679 | … | 792 |
| 61'-0" | … | … | 100 | 704 | … | 804 |
| 62'-0" | … | … | 88 | 729 | … | 817 |
| 63'-0" | … | … | 75 | 754 | … | 829 |
| 64'-0" | … | … | 63 | 779 | … | 842 |
| 65'-0" | … | … | 51 | 804 | … | 855 |
| 66'-0" | … | … | 38 | 829 | … | 867 |
| 67'-0" | … | … | 25 | 855 | … | 880 |
| 68'-0" | … | … | 12 | 880 | … | 892 |
| 69'-0" | … | … | … | 905 | … | 905 |
| 70'-0" | … | … | … | 905 | 12 | 917 |

All totals check. (No "Continued" line; this ends the complete-circle tables.)

### p.163 — BLAST FURNACE BOTTOM BLOCKS — 18"x9"x4½"

"Number per course; Blocks laid on end"

| Diameter of Hearth | No. of Blocks | | Diameter of Hearth | No. of Blocks |
|---|---|---|---|---|
| 10'-0" | 303 | | 24'-0" | 1665 |
| 10'-6" | 333 | | 24'-6" | 1734 |
| 11'-0" | 364 | | 25'-0" | 1804 |
| 11'-6" | 397 | | 25'-6" | 1876 |
| 12'-0" | 431 | | 26'-0" | 1949 |
| 12'-6" | 466 | | 26'-6" | 2023 |
| 13'-0" | 503 | | 27'-0" | 2099 |
| 13'-6" | 541 | | 27'-6" | 2176 |
| 14'-0" | 581 | | 28'-0" | 2255 |
| 14'-6" | 621 | | 28'-6" | 2335 |
| 15'-0" | 664 | | 29'-0" | 2417 |
| 15'-6" | 708 | | 29'-6" | 2500 |
| 16'-0" | 753 | | 30'-0" | 2584 |
| 16'-6" | 799 | | 30'-6" | 2669 |
| 17'-0" | 847 | | 31'-0" | 2756 |
| 17'-6" | 897 | | 31'-6" | 2845 |
| 18'-0" | 947 | | 32'-0" | 2935 |
| 18'-6" | 999 | | 32'-6" | 3026 |
| 19'-0" | 1053 | | 33'-0" | 3119 |
| 19'-6" | 1108 | | 33'-6" | 3213 |
| 20'-0" | 1164 | | 34'-0" | 3308 |
| 20'-6" | 1222 | | 34'-6" | 3405 |
| 21'-0" | 1281 | | 35'-0" | 3503 |
| 21'-6" | 1342 | | 35'-6" | 3603 |
| 22'-0" | 1403 | | 36'-0" | 3704 |
| 22'-6" | 1467 | | 36'-6" | 3806 |
| 23'-0" | 1531 | | 37'-0" | 3909 |
| 23'-6" | 1598 | | 37'-6" | 4013 |

No totals printed.

## Image (36).jpg — catalogue p.164–165

### p.164 — SPRUNG ARCHES — 1½" rise per foot of span — 4½-INCH ARCH THICKNESS — Central Angle=56°

9"x4½"x2½" or 13½"x4½"x2½". "Standard 9-inch Featheredge to be used for Skew". Header: BRICK REQUIRED PER COURSE. Columns: No. 3 Arch 9x4½x(2½-1); No. 2 Arch 9x4½x(2½-1¾); No. 1 Arch 9x4½x(2½-2⅛); Straight 9x4½x2½.

| Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|
| 0'-6" | ¾" | 6¾" | 1 | 4 | … | … | 5 |
| 0'-7" | ⅞" | 7 7/16" | 1 | 4 | … | … | 5 |
| 0'-8" | 1" | 8½" | 1 | 4 | … | … | 5 |
| 0'-9" | 1⅛" | 9 9/16" | … | 6 | … | … | 6 |
| 0'-10" | 1¼" | 10⅝" | … | 6 | … | … | 6 |
| 0'-11" | 1⅜" | 11 11/16" | … | 5 | 2 | … | 7 |
| 1'-0" | 1½" | 1'-0¾" | … | 5 | 2 | … | 7 |
| 1'-1" | 1⅝" | 1'-1 13/16" | … | 4 | 4 | … | 8 |
| 1'-2" | 1¾" | 1'-2⅞" | … | 4 | 4 | … | 8 |
| 1'-3" | 1⅞" | 1'-3 15/16" | … | 4 | 4 | … | 8 |
| 1'-4" | 2" | 1'-5" | … | 3 | 6 | … | 9 |
| 1'-5" | 2⅛" | 1'-6 1/16" | … | 3 | 6 | … | 9 |
| 1'-6" | 2¼" | 1'-7⅛" | … | 2 | 8 | … | 10 |
| 1'-7" | 2⅜" | 1'-8 3/16" | … | 2 | 8 | … | 10 |
| 1'-8" | 2½" | 1'-9¼" | … | 2 | 8 | … | 10 |
| 1'-9" | 2⅝" | 1'-10 5/16" | … | 1 | 10 | … | 11 |
| 1'-10" | 2¾" | 1'-11⅜" | … | 1 | 10 | … | 11 |
| 1'-11" | 2⅞" | 2'-0 7/16" | … | … | 12 | … | 12 |
| 2'-0" | 3" | 2'-1½" | … | … | 12 | … | 12 |
| 2'-1" | 3⅛" | 2'-2 9/16" | … | … | 12 | … | 12 |
| 2'-2" | 3¼" | 2'-3⅝" | … | … | 12 | 1 | 13 |
| 2'-3" | 3⅜" | 2'-4 11/16" | … | … | 12 | 1 | 13 |
| 2'-4" | 3½" | 2'-5¾" | … | … | 12 | 2 | 14 |
| 2'-5" | 3⅝" | 2'-6 13/16" | … | … | 12 | 2 | 14 |
| 2'-6" | 3¾" | 2'-7⅞" | … | … | 12 | 3 | 15 |
| 2'-7" | 3⅞" | 2'-8 15/16" | … | … | 12 | 3 | 15 |
| 2'-8" | 4" | 2'-10" | … | … | 12 | 3 | 15 |
| 2'-9" | 4⅛" | 2'-11 1/16" | … | … | 12 | 4 | 16 |
| 2'-10" | 4¼" | 3'-0⅛" | … | … | 12 | 4 | 16 |
| 2'-11" | 4⅜" | 3'-1 3/16" | … | … | 12 | 5 | 17 |
| 3'-0" | 4½" | 3'-2¼" | … | … | 12 | 5 | 17 |
| 3'-1" | 4⅝" | 3'-3 5/16" | … | … | 12 | 6 | 18 |
| 3'-2" | 4¾" | 3'-4⅜" | … | … | 12 | 6 | 18 |
| 3'-3" | 4⅞" | 3'-5 7/16" | … | … | 12 | 6 | 18 |
| 3'-4" | 5" | 3'-6½" | … | … | 12 | 7 | 19 |
| 3'-5" | 5⅛" | 3'-7 9/16" | … | … | 12 | 7 | 19 |
| 3'-6" | 5¼" | 3'-8⅝" | … | … | 12 | 8 | 20 |
| 3'-9" | 5⅝" | 3'-11 13/16" | … | … | 12 | 9 | 21 |
| 4'-0" | 6" | 4'-3" | … | … | 12 | 10 | 22 |
| 4'-3" | 6⅜" | 4'-6 3/16" | … | … | 12 | 11 | 23 |
| 4'-6" | 6¾" | 4'-9⅜" | … | … | 12 | 13 | 25 |
| 4'-9" | 7⅛" | 5'-0 9/16" | … | … | 12 | 14 | 26 |
| 5'-0" | 7½" | 5'-3¾" | … | … | 12 | 15 | 27 |
| 5'-3" | 7⅞" | 5'-6 15/16" | … | … | 12 | 16 | 28 |
| 5'-6" | 8¼" | 5'-10⅛" | … | … | 12 | 18 | 30 |
| 5'-9" | 8⅝" | 6'-1 5/16" | … | … | 12 | 19 | 31 |
| 6'-0" | 9" | 6'-4½" | … | … | 12 | 20 | 32 |
| 6'-3" | 9⅜" | 6'-7 11/16" | … | … | 12 | 21 | 33 |
| 6'-6" | 9¾" | 6'-10⅞" | … | … | 12 | 23 | 35 |

Footer: "See Page 106 For Skews". All totals check. (Rows jump 3'-6" to 3'-9", as printed.)

### p.165 — SPRUNG ARCHES — 1½" rise per foot of span — 4½-INCH ARCH THICKNESS — Central Angle=56°

9"x4½"x3" or 13½"x4½"x3". "Standard 9-inch Featheredge to be used for Skew". Columns: No. 3 Arch 9x4½x(3-2); No. 2 Arch 9x4½x(3-2½); No. 1 Arch 9x4½x(3-2¾); Straight 9x4½x3.

| Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|
| 1'-0" | 1½" | 1'-0¾" | 3 | 3 | … | … | 6 |
| 1'-1" | 1⅝" | 1'-1 13/16" | 3 | 3 | … | … | 6 |
| 1'-2" | 1¾" | 1'-2⅞" | 3 | 4 | … | … | 7 |
| 1'-3" | 1⅞" | 1'-3 15/16" | 2 | 5 | … | … | 7 |
| 1'-4" | 2" | 1'-5" | 2 | 5 | … | … | 7 |
| 1'-5" | 2⅛" | 1'-6 1/16" | 2 | 6 | … | … | 8 |
| 1'-6" | 2¼" | 1'-7⅛" | 1 | 7 | … | … | 8 |
| 1'-7" | 2⅜" | 1'-8 3/16" | 1 | 8 | … | … | 9 |
| 1'-8" | 2½" | 1'-9¼" | 1 | 8 | … | … | 9 |
| 1'-9" | 2⅝" | 1'-10 5/16" | … | 9 | … | … | 9 |
| 1'-10" | 2¾" | 1'-11⅜" | … | 9 | 1 | … | 10 |
| 1'-11" | 2⅞" | 2'-0 7/16" | … | 8 | 2 | … | 10 |
| 2'-0" | 3" | 2'-1½" | … | 8 | 2 | … | 10 |
| 2'-1" | 3⅛" | 2'-2 9/16" | … | 8 | 3 | … | 11 |
| 2'-2" | 3¼" | 2'-3⅝" | … | 7 | 4 | … | 11 |
| 2'-3" | 3⅜" | 2'-4 11/16" | … | 7 | 4 | … | 11 |
| 2'-4" | 3½" | 2'-5¾" | … | 7 | 5 | … | 12 |
| 2'-5" | 3⅝" | 2'-6 13/16" | … | 6 | 6 | … | 12 |
| 2'-6" | 3¾" | 2'-7⅞" | … | 6 | 6 | … | 12 |
| 2'-7" | 3⅞" | 2'-8 15/16" | … | 6 | 7 | … | 13 |
| 2'-8" | 4" | 2'-10" | … | 6 | 7 | … | 13 |
| 2'-9" | 4⅛" | 2'-11 1/16" | … | 5 | 8 | … | 13 |
| 2'-10" | 4¼" | 3'-0⅛" | … | 5 | 9 | … | 14 |
| 2'-11" | 4⅜" | 3'-1 3/16" | … | 4 | 10 | … | 14 |
| 3'-0" | 4½" | 3'-2¼" | … | 4 | 10 | … | 14 |
| 3'-1" | 4⅝" | 3'-3 5/16" | … | 4 | 11 | … | 15 |
| 3'-2" | 4¾" | 3'-4⅜" | … | 3 | 12 | … | 15 |
| 3'-3" | 4⅞" | 3'-5 7/16" | … | 3 | 12 | … | 15 |
| 3'-4" | 5" | 3'-6½" | … | 3 | 13 | … | 16 |
| 3'-5" | 5⅛" | 3'-7 9/16" | … | 2 | 14 | … | 16 |
| 3'-6" | 5¼" | 3'-8⅝" | … | 2 | 14 | … | 16 |
| 3'-7" | 5⅜" | 3'-9 11/16" | … | 2 | 15 | … | 17 |
| 3'-8" | 5½" | 3'-10¾" | … | 1 | 16 | … | 17 |
| 3'-9" | 5⅝" | 3'-11 13/16" | … | … | 17 | … | 17 |
| 4'-0" | 6" | 4'-3" | … | … | 18 | 1 | 19 |
| 4'-3" | 6⅜" | 4'-6 3/16" | … | … | 18 | 2 | 20 |
| 4'-6" | 6¾" | 4'-9⅜" | … | … | 18 | 3 | 21 |
| 4'-9" | 7⅛" | 5'-0 9/16" | … | … | 18 | 4 | 22 |
| 5'-0" | 7½" | 5'-3¾" | … | … | 18 | 5 | 23 |
| 5'-3" | 7⅞" | 5'-6 15/16" | … | … | 18 | 6 | 24 |
| 5'-6" | 8¼" | 5'-10⅛" | … | … | 18 | 7 | 25 |
| 5'-9" | 8⅝" | 6'-1 5/16" | … | … | 18 | 8 | 26 |
| 6'-0" | 9" | 6'-4½" | … | … | 18 | 9 | 27 |
| 6'-3" | 9⅜" | 6'-7 11/16" | … | … | 18 | 10 | 28 |
| 6'-6" | 9¾" | 6'-10⅞" | … | … | 18 | 11 | 29 |

Footer: "See Page 106 For Skews". All totals check.


## Image (37).jpg — catalogue p.166–167

### p.166 — SPRUNG ARCHES — 1.608" rise per foot of span — 4½-INCH ARCH THICKNESS — Radius=Span: Central Angle=60°

9"x4½"x2½" or 13½"x4½"x2½". "Brand 4160-A to be used for Skew". Columns: No. 3 Arch 9x4½x(2½-1); No. 2 Arch 9x4½x(2½-1¾); No. 1 Arch 9x4½x(2½-2⅛); Straight 9x4½x2½.

| Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|
| 0'-6" | 13/16" | 6" | 2 | 3 | … | … | 5 |
| 0'-7" | 15/16" | 7" | 2 | 3 | … | … | 5 |
| 0'-8" | 1 1/16" | 8" | 1 | 5 | … | … | 6 |
| 0'-9" | 1 7/32" | 9" | 1 | 5 | … | … | 6 |
| 0'-10" | 1 11/32" | 10" | … | 6 | … | … | 6 |
| 0'-11" | 1 15/32" | 11" | … | 6 | 1 | … | 7 |
| 1'-0" | 1 19/32" | 1'-0" | … | 6 | 1 | … | 7 |
| 1'-1" | 1¾" | 1'-1" | … | 6 | 2 | … | 8 |
| 1'-2" | 1⅞" | 1'-2" | … | 5 | 3 | … | 8 |
| 1'-3" | 2" | 1'-3" | … | 5 | 4 | … | 9 |
| 1'-4" | 2 5/32" | 1'-4" | … | 4 | 5 | … | 9 |
| 1'-5" | 2 9/32" | 1'-5" | … | 4 | 5 | … | 9 |
| 1'-6" | 2 13/32" | 1'-6" | … | 3 | 7 | … | 10 |
| 1'-7" | 2 17/32" | 1'-7" | … | 3 | 7 | … | 10 |
| 1'-8" | 2 11/16" | 1'-8" | … | 3 | 8 | … | 11 |
| 1'-9" | 2 13/16" | 1'-9" | … | 2 | 9 | … | 11 |
| 1'-10" | 2 15/16" | 1'-10" | … | 2 | 10 | … | 12 |
| 1'-11" | 3 3/32" | 1'-11" | … | 1 | 11 | … | 12 |
| 2'-0" | 3 7/32" | 2'-0" | … | 1 | 11 | … | 12 |
| 2'-1" | 3 11/32" | 2'-1" | … | … | 13 | … | 13 |
| 2'-2" | 3 15/32" | 2'-2" | … | … | 13 | … | 13 |
| 2'-3" | 3⅝" | 2'-3" | … | … | 13 | 1 | 14 |
| 2'-6" | 4 1/32" | 2'-6" | … | … | 13 | 2 | 15 |
| 2'-9" | 4 7/16" | 2'-9" | … | … | 13 | 3 | 16 |
| 3'-0" | 4 13/16" | 3'-0" | … | … | 13 | 4 | 17 |
| 3'-3" | 5 7/32" | 3'-3" | … | … | 13 | 6 | 19 |
| 3'-6" | 5⅝" | 3'-6" | … | … | 13 | 7 | 20 |
| 3'-9" | 6 1/32" | 3'-9" | … | … | 13 | 8 | 21 |
| 4'-0" | 6 7/16" | 4'-0" | … | … | 13 | 9 | 22 |
| 4'-3" | 6 27/32" | 4'-3" | … | … | 13 | 11 | 24 |
| 4'-6" | 7¼" | 4'-6" | … | … | 13 | 12 | 25 |
| 4'-9" | 7⅝" | 4'-9" | … | … | 13 | 13 | 26 |
| 5'-0" | 8 1/32" | 5'-0" | … | … | 13 | 14 | 27 |
| 5'-3" | 8 7/16" | 5'-3" | … | … | 13 | 16 | 29 |
| 5'-6" | 8 27/32" | 5'-6" | … | … | 13 | 17 | 30 |
| 5'-9" | 9¼" | 5'-9" | … | … | 13 | 18 | 31 |
| 6'-0" | 9 21/32" | 6'-0" | … | … | 13 | 19 | 32 |
| 6'-3" | 10 1/16" | 6'-3" | … | … | 13 | 21 | 34 |
| 6'-6" | 10 7/16" | 6'-6" | … | … | 13 | 22 | 35 |

Footer: "See Page 106 For Skews". All totals check. (Total column partly in the binding gutter; digits legible.)

### p.167 — SPRUNG ARCHES — 1.608" rise per foot of span — 4½-INCH ARCH THICKNESS — Radius=Span: Central Angle=60°

9"x4½"x3" or 13½"x4½"x3". "Brand 4160-A to be used for Skew". Columns: No. 3 Arch 9x4½x(3-2); No. 2 Arch 9x4½x(3-2½); No. 1 Arch 9x4½x(3-2¾); Straight 9x4½x3.

| Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|
| 1'-0" | 1 19/32" | 1'-0" | 4 | 2 | … | … | 6 |
| 1'-1" | 1¾" | 1'-1" | 3 | 3 | … | … | 6 |
| 1'-2" | 1⅞" | 1'-2" | 3 | 4 | … | … | 7 |
| 1'-3" | 2" | 1'-3" | 3 | 4 | … | … | 7 |
| 1'-4" | 2 5/32" | 1'-4" | 2 | 5 | … | … | 7 |
| 1'-5" | 2 9/32" | 1'-5" | 2 | 6 | … | … | 8 |
| 1'-6" | 2 13/32" | 1'-6" | 2 | 6 | … | … | 8 |
| 1'-7" | 2 17/32" | 1'-7" | 2 | 7 | … | … | 9 |
| 1'-8" | 2 11/16" | 1'-8" | 1 | 8 | … | … | 9 |
| 1'-9" | 2 13/16" | 1'-9" | 1 | 8 | … | … | 9 |
| 1'-10" | 2 15/16" | 1'-10" | … | 9 | … | … | 9 |
| 1'-11" | 3 3/32" | 1'-11" | … | 9 | 1 | … | 10 |
| 2'-0" | 3 7/32" | 2'-0" | … | 9 | 1 | … | 10 |
| 2'-1" | 3 11/32" | 2'-1" | … | 9 | 2 | … | 11 |
| 2'-2" | 3 15/32" | 2'-2" | … | 8 | 3 | … | 11 |
| 2'-3" | 3⅝" | 2'-3" | … | 8 | 3 | … | 11 |
| 2'-4" | 3¾" | 2'-4" | … | 8 | 4 | … | 12 |
| 2'-5" | 3⅞" | 2'-5" | … | 7 | 5 | … | 12 |
| 2'-6" | 4 1/32" | 2'-6" | … | 7 | 5 | … | 12 |
| 2'-7" | 4 5/32" | 2'-7" | … | 7 | 6 | … | 13 |
| 2'-8" | 4 9/32" | 2'-8" | … | 6 | 7 | … | 13 |
| 2'-9" | 4 7/16" | 2'-9" | … | 6 | 7 | … | 13 |
| 2'-10" | 4 9/16" | 2'-10" | … | 6 | 8 | … | 14 |
| 2'-11" | 4 11/16" | 2'-11" | … | 5 | 9 | … | 14 |
| 3'-0" | 4 13/16" | 3'-0" | … | 5 | 9 | … | 14 |
| 3'-1" | 4 31/32" | 3'-1" | … | 5 | 10 | … | 15 |
| 3'-2" | 5 3/32" | 3'-2" | … | 4 | 11 | … | 15 |
| 3'-3" | 5 7/32" | 3'-3" | … | 4 | 12 | … | 16 |
| 3'-4" | 5 11/32" | 3'-4" | … | 3 | 13 | … | 16 |
| 3'-5" | 5½" | 3'-5" | … | 3 | 13 | … | 16 |
| 3'-6" | 5⅝" | 3'-6" | … | 3 | 14 | … | 17 |
| 3'-7" | 5¾" | 3'-7" | … | 2 | 15 | … | 17 |
| 3'-8" | 5 29/32" | 3'-8" | … | 2 | 15 | … | 17 |
| 3'-9" | 6 1/32" | 3'-9" | … | 2 | 16 | … | 18 |
| 3'-10" | 6 5/32" | 3'-10" | … | 1 | 17 | … | 18 |
| 3'-11" | 6 9/32" | 3'-11" | … | 1 | 17 | … | 18 |
| 4'-0" | 6 7/16" | 4'-0" | … | 1 | 18 | … | 19 |
| 4'-1" | 6 9/16" | 4'-1" | … | … | 19 | … | 19 |
| 4'-2" | 6 11/16" | 4'-2" | … | … | 19 | … | 19 |
| 4'-3" | 6 27/32" | 4'-3" | … | … | 19 | 1 | 20 |
| 4'-6" | 7¼" | 4'-6" | … | … | 19 | 2 | 21 |
| 4'-9" | 7⅝" | 4'-9" | … | … | 19 | 3 | 22 |
| 5'-0" | 8 1/32" | 5'-0" | … | … | 19 | 4 | 23 |
| 5'-3" | 8 7/16" | 5'-3" | … | … | 19 | 5 | 24 |
| 5'-6" | 8 27/32" | 5'-6" | … | … | 19 | 6 | 25 |
| 5'-9" | 9¼" | 5'-9" | … | … | 19 | 7 | 26 |
| 6'-0" | 9 21/32" | 6'-0" | … | … | 19 | 8 | 27 |
| 6'-3" | 10 1/16" | 6'-3" | … | … | 19 | 9 | 28 |
| 6'-6" | 10 7/16" | 6'-6" | … | … | 19 | 10 | 29 |

Footer: "See Page 106 For Skews". All totals check.

## Image (38).jpg — catalogue p.168–169

### p.168 — SPRUNG ARCHES — 2" rise per foot of span — 4½-INCH ARCH THICKNESS — Central Angle=74°

(handwritten at top of page: "12 X 36" followed by an unclear mark, possibly "T")

9"x4½"x2½" or 13½"x4½"x2½". "Brand 4160-C to be used for Skew". Columns: No. 3 Arch 9x4½x(2½-1); No. 2 Arch 9x4½x(2½-1¾); No. 1 Arch 9x4½x(2½-2⅛); Straight 9x4½x2½.

| Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|
| 0'-6" | 1" | 5" | 3 | 2 | … | … | 5 |
| 0'-7" | 1 5/32" | 5 27/32" | 3 | 3 | … | … | 6 |
| 0'-8" | 1 11/32" | 6 21/32" | 2 | 4 | … | … | 6 |
| 0'-9" | 1½" | 7½" | 2 | 5 | … | … | 7 |
| 0'-10" | 1 21/32" | 8 11/32" | 1 | 6 | … | … | 7 |
| 0'-11" | 1 27/32" | 9 5/32" | 1 | 6 | … | … | 7 |
| 1'-0" | 2" | 10" | … | 8 | … | … | 8 |
| 1'-1" | 2 5/32" | 10 27/32" | … | 7 | 1 | … | 8 |
| 1'-2" | 2 11/32" | 11 21/32" | … | 7 | 2 | … | 9 |
| 1'-3" | 2½" | 1'-0½" | … | 7 | 2 | … | 9 |
| 1'-4" | 2 21/32" | 1'-1 11/32" | … | 7 | 3 | … | 10 |
| 1'-5" | 2 27/32" | 1'-2 5/32" | … | 6 | 4 | … | 10 |
| 1'-6" | 3" | 1'-3" | … | 5 | 5 | … | 10 |
| 1'-7" | 3 5/32" | 1'-3 27/32" | … | 5 | 6 | … | 11 |
| 1'-8" | 3 11/32" | 1'-4 21/32" | … | 5 | 6 | … | 11 |
| 1'-9" | 3½" | 1'-5½" | … | 4 | 8 | … | 12 |
| 1'-10" | 3 21/32" | 1'-6 11/32" | … | 4 | 8 | … | 12 |
| 1'-11" | 3 27/32" | 1'-7 5/32" | … | 4 | 9 | … | 13 |
| 2'-0" | 4" | 1'-8" | … | 3 | 10 | … | 13 |
| 2'-1" | 4 5/32" | 1'-8 27/32" | … | 2 | 11 | … | 13 |
| 2'-2" | 4 11/32" | 1'-9 21/32" | … | 2 | 12 | … | 14 |
| 2'-3" | 4½" | 1'-10½" | … | 2 | 12 | … | 14 |
| 2'-4" | 4 21/32" | 1'-11 11/32" | … | 1 | 14 | … | 15 |
| 2'-5" | 4 27/32" | 2'-0 5/32" | … | 1 | 14 | … | 15 |
| 2'-6" | 5" | 2'-1" | … | 1 | 15 | … | 16 |
| 2'-7" | 5 5/32" | 2'-1 27/32" | … | … | 16 | … | 16 |
| 2'-8" | 5 11/32" | 2'-2 21/32" | … | … | 16 | 1 | 17 |
| 2'-9" | 5½" | 2'-3½" | … | … | 16 | 1 | 17 |
| 3'-0" | 6" | 2'-6" | … | … | 16 | 2 | 18 |
| 3'-3" | 6½" | 2'-8½" | … | … | 16 | 3 | 19 |
| 3'-6" | 7" | 2'-11" | … | … | 16 | 5 | 21 |
| 3'-9" | 7½" | 3'-1½" | … | … | 16 | 6 | 22 |
| 4'-0" | 8" | 3'-4" | … | … | 16 | 7 | 23 |
| 4'-3" | 8½" | 3'-6½" | … | … | 16 | 9 | 25 |
| 4'-6" | 9" | 3'-9" | … | … | 16 | 10 | 26 |
| 4'-9" | 9½" | 3'-11½" | … | … | 16 | 11 | 27 |
| 5'-0" | 10" | 4'-2" | … | … | 16 | 12 | 28 |
| 5'-3" | 10½" | 4'-4½" | … | … | 16 | 14 | 30 |
| 5'-6" | 11" | 4'-7" | … | … | 16 | 15 | 31 |
| 5'-9" | 11½" | 4'-9½" | … | … | 16 | 16 | 32 |
| 6'-0" | 1'-0" | 5'-0" | … | … | 16 | 18 | 34 |
| 6'-3" | 1'-0½" | 5'-2½" | … | … | 16 | 19 | 35 |
| 6'-6" | 1'-1" | 5'-5" | … | … | 16 | 20 | 36 |

Footer: "See Page 106 For Skews". All totals check.

### p.169 — SPRUNG ARCHES — 2" rise per foot of span — 4½-INCH ARCH THICKNESS — Central Angle=74°

9"x4½"x3" or 13½"x4½"x3". "Brand 4160-C to be used for Skews". Columns: No. 3 Arch 9x4½x(3-2); No. 2 Arch 9x4½x(3-2½); No. 1 Arch 9x4½x(3-2¾); Straight 9x4½x3.

| Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|
| 1'-0" | 2" | 10" | 6 | 1 | … | … | 7 |
| 1'-1" | 2 5/32" | 10 27/32" | 5 | 2 | … | … | 7 |
| 1'-2" | 2 11/32" | 11 21/32" | 5 | 2 | … | … | 7 |
| 1'-3" | 2½" | 1'-0½" | 5 | 3 | … | … | 8 |
| 1'-4" | 2 21/32" | 1'-1 11/32" | 4 | 4 | … | … | 8 |
| 1'-5" | 2 27/32" | 1'-2 5/32" | 4 | 4 | … | … | 8 |
| 1'-6" | 3" | 1'-3" | 4 | 5 | … | … | 9 |
| 1'-7" | 3 5/32" | 1'-3 27/32" | 3 | 6 | … | … | 9 |
| 1'-8" | 3 11/32" | 1'-4 21/32" | 3 | 6 | … | … | 9 |
| 1'-9" | 3½" | 1'-5½" | 2 | 8 | … | … | 10 |
| 1'-10" | 3 21/32" | 1'-6 11/32" | 2 | 8 | … | … | 10 |
| 1'-11" | 3 27/32" | 1'-7 5/32" | 2 | 9 | … | … | 11 |
| 2'-0" | 4" | 1'-8" | 1 | 10 | … | … | 11 |
| 2'-1" | 4 5/32" | 1'-8 27/32" | 1 | 10 | … | … | 11 |
| 2'-2" | 4 11/32" | 1'-9 21/32" | 1 | 11 | … | … | 12 |
| 2'-3" | 4½" | 1'-10½" | … | 12 | … | … | 12 |
| 2'-4" | 4 21/32" | 1'-11 11/32" | … | 11 | 1 | … | 12 |
| 2'-5" | 4 27/32" | 2'-0 5/32" | … | 11 | 2 | … | 13 |
| 2'-6" | 5" | 2'-1" | … | 11 | 2 | … | 13 |
| 2'-7" | 5 5/32" | 2'-1 27/32" | … | 10 | 3 | … | 13 |
| 2'-8" | 5 11/32" | 2'-2 21/32" | … | 10 | 4 | … | 14 |
| 2'-9" | 5½" | 2'-3½" | … | 10 | 4 | … | 14 |
| 2'-10" | 5 21/32" | 2'-4 11/32" | … | 9 | 5 | … | 14 |
| 2'-11" | 5 27/32" | 2'-5 5/32" | … | 9 | 6 | … | 15 |
| 3'-0" | 6" | 2'-6" | … | 8 | 7 | … | 15 |
| 3'-2" | 6 11/32" | 2'-7 21/32" | … | 8 | 8 | … | 16 |
| 3'-4" | 6 21/32" | 2'-9 11/32" | … | 7 | 10 | … | 17 |
| 3'-6" | 7" | 2'-11" | … | 6 | 11 | … | 17 |
| 3'-8" | 7 11/32" | 3'-0 21/32" | … | 6 | 12 | … | 18 |
| 3'-10" | 7 21/32" | 3'-2 11/32" | … | 5 | 14 | … | 19 |
| 4'-0" | 8" | 3'-4" | … | 4 | 15 | … | 19 |
| 4'-2" | 8 11/32" | 3'-5 11/16" | … | 3 | 17 | … | 20 |
| 4'-4" | 8 21/32" | 3'-7 11/32" | … | 3 | 18 | … | 21 |
| 4'-6" | 9" | 3'-9" | … | 2 | 20 | … | 22 |
| 4'-8" | 9 11/32" | 3'-10 21/32" | … | 1 | 21 | … | 22 |
| 4'-10" | 9 21/32" | 4'-0 11/32" | … | 1 | 22 | … | 23 |
| 4'-11" | 9 27/32" | 4'-1 5/32" | … | … | 23 | … | 23 |
| 5'-0" | 10" | 4'-2" | … | … | 23 | 1 | 24 |
| 5'-3" | 10½" | 4'-4½" | … | … | 23 | 2 | 25 |
| 5'-6" | 11" | 4'-7" | … | … | 23 | 3 | 26 |
| 5'-9" | 11½" | 4'-9½" | … | … | 23 | 4 | 27 |
| 6'-0" | 1'-0" | 5'-0" | … | … | 23 | 5 | 28 |
| 6'-3" | 1'-0½" | 5'-2½" | … | … | 23 | 6 | 29 |
| 6'-6" | 1'-1" | 5'-5" | … | … | 23 | 7 | 30 |

Footer: "See Page 106 For Skews". All totals check. (4'-2" radius prints as 3'-5 11/16" while its neighbours are in 32nds; transcribed as printed.)

## Image (39).jpg — catalogue p.170–171

### p.170 — SPRUNG ARCHES — 2.302" rise per foot of span — 4½-INCH ARCH THICKNESS — Central Angle=84°

(handwritten at top of page, faint: looks like "12 X 36" again [?read])

9"x4½"x2½" or 13½"x4½"x2½". "Standard sideskews to be used for Skew". Columns: No. 3 Arch 9x4½x(2½-1); No. 2 Arch 9x4½x(2½-1¾); No. 1 Arch 9x4½x(2½-2⅛); Straight 9x4½x2½.

| Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|
| 0'-6" | 1 5/32" | 4½" | 4 | 2 | … | … | 6 |
| 0'-7" | 1 11/32" | 5 7/32" | 3 | 3 | … | … | 6 |
| 0'-8" | 1 17/32" | 5 31/32" | 3 | 4 | … | … | 7 |
| 0'-9" | 1 23/32" | 6 23/32" | 2 | 5 | … | … | 7 |
| 0'-10" | 1 29/32" | 7 15/32" | 2 | 5 | … | … | 7 |
| 0'-11" | 2⅛" | 8 7/32" | 2 | 6 | … | … | 8 |
| 1'-0" | 2 5/16" | 8 31/32" | 1 | 7 | … | … | 8 |
| 1'-1" | 2½" | 9 23/32" | 1 | 8 | … | … | 9 |
| 1'-2" | 2 11/16" | 10 15/32" | … | 9 | … | … | 9 |
| 1'-3" | 2⅞" | 11 7/32" | … | 9 | 1 | … | 10 |
| 1'-4" | 3 1/16" | 11 31/32" | … | 8 | 2 | … | 10 |
| 1'-5" | 3¼" | 1'-0 23/32" | … | 7 | 3 | … | 10 |
| 1'-6" | 3 15/32" | 1'-1 15/32" | … | 7 | 4 | … | 10 |
| 1'-7" | 3 21/32" | 1'-2 3/16" | … | 7 | 4 | … | 11 |
| 1'-8" | 3 27/32" | 1'-2 15/16" | … | 6 | 6 | … | 12 |
| 1'-9" | 4 1/32" | 1'-3 11/16" | … | 6 | 6 | … | 12 |
| 1'-10" | 4 7/32" | 1'-4 7/16" | … | 6 | 7 | … | 12 |
| 1'-11" | 4 13/32" | 1'-5 3/16" | … | 5 | 8 | … | 13 |
| 2'-0" | 4 19/32" | 1'-5 15/16" | … | 5 | 9 | … | 14 |
| 2'-1" | 4 25/32" | 1'-6 11/16" | … | 4 | 10 | … | 14 |
| 2'-2" | 5" | 1'-7 7/16" | … | 4 | 10 | … | 14 |
| 2'-3" | 5 3/16" | 1'-8 3/16" | … | 3 | 12 | … | 15 |
| 2'-4" | 5⅜" | 1'-8 15/16" | … | 3 | 12 | … | 15 |
| 2'-5" | 5 9/16" | 1'-9 11/16" | … | 3 | 13 | … | 16 |
| 2'-6" | 5¾" | 1'-10 7/16" | … | 2 | 14 | … | 16 |
| 2'-7" | 5 15/16" | 1'-11 5/32" | … | 2 | 15 | … | 17 |
| 2'-8" | 6⅛" | 1'-11 29/32" | … | 1 | 16 | … | 17 |
| 2'-9" | 6 11/32" | 2'-0 21/32" | … | … | 17 | … | 17 |
| 2'-10" | 6 17/32" | 2'-1 13/32" | … | … | 18 | … | 18 |
| 2'-11" | 6 23/32" | 2'-2 5/32" | … | … | 18 | … | 18 |
| 3'-0" | 6 29/32" | 2'-2 29/32" | … | … | 18 | 1 | 19 |
| 3'-3" | 7 15/32" | 2'-5 5/32" | … | … | 18 | 2 | 20 |
| 3'-6" | 8 1/16" | 2'-7 13/32" | … | … | 18 | 3 | 21 |
| 3'-9" | 8⅝" | 2'-9⅝" | … | … | 18 | 5 | 23 |
| 4'-0" | 9 7/32" | 2'-11⅞" | … | … | 18 | 6 | 24 |
| 4'-3" | 9 25/32" | 3'-2⅛" | … | … | 18 | 7 | 25 |
| 4'-6" | 10⅜" | 3'-4⅜" | … | … | 18 | 9 | 27 |
| 4'-9" | 10 15/16" | 3'-6 19/32" | … | … | 18 | 10 | 28 |
| 5'-0" | 11½" | 3'-8 27/32" | … | … | 18 | 11 | 29 |
| 5'-3" | 12 3/32" | 3'-11 3/32" | … | … | 18 | 13 | 31 |
| 5'-6" | 1'-0 21/32" | 4'-1 11/32" | … | … | 18 | 14 | 32 |
| 5'-9" | 1'-1¼" | 4'-3 9/16" | … | … | 18 | 15 | 33 |
| 6'-0" | 1'-1 13/16" | 4'-5 13/16" | … | … | 18 | 17 | 35 |
| 6'-3" | 1'-2⅜" | 4'-8 1/16" | … | … | 18 | 18 | 36 |
| 6'-6" | 1'-2 31/32" | 4'-10 5/16" | … | … | 18 | 19 | 37 |

Footer: "See Page 106 For Skews".
Total check: MISMATCH at 1'-6" (7 + 4 = 11, printed 10) and at 1'-10" (6 + 7 = 13, printed 12). Both re-read on a zoomed crop; the printed figures are as transcribed. All other rows check.

### p.171 — SPRUNG ARCHES — 2.302" rise per foot of span — 4½-INCH ARCH THICKNESS — Central Angle=84°

9"x4½"x3" or 13½"x4½"x3". "Standard sideskews to be used for Skew". Columns: No. 3 Arch 9x4½x(3-2); No. 2 Arch 9x4½x(3-2½); No. 1 Arch 9x4½x(3-2¾); Straight 9x4½x3.

| Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|
| 1'-0" | 2 5/16" | 8 31/32" | 7 | … | … | … | 7 |
| 1'-1" | 2½" | 9 23/32" | 6 | 1 | … | … | 7 |
| 1'-2" | 2 11/16" | 10 15/32" | 6 | 2 | … | … | 8 |
| 1'-3" | 2⅞" | 11 7/32" | 6 | 2 | … | … | 8 |
| 1'-4" | 3 1/16" | 11 31/32" | 5 | 3 | … | … | 8 |
| 1'-5" | 3¼" | 1'-0 23/32" | 5 | 4 | … | … | 9 |
| 1'-6" | 3 15/32" | 1'-1 15/32" | 5 | 4 | … | … | 9 |
| 1'-7" | 3 21/32" | 1'-2 3/16" | 4 | 6 | … | … | 10 |
| 1'-8" | 3 27/32" | 1'-2 15/16" | 4 | 6 | … | … | 10 |
| 1'-9" | 4 1/32" | 1'-3 11/16" | 3 | 7 | … | … | 10 |
| 1'-10" | 4 7/32" | 1'-4 7/16" | 3 | 8 | … | … | 11 |
| 1'-11" | 4 13/32" | 1'-5 3/16" | 3 | 8 | … | … | 11 |
| 2'-0" | 4 19/32" | 1'-5 15/16" | 2 | 9 | … | … | 11 |
| 2'-1" | 4 25/32" | 1'-6 11/16" | 2 | 10 | … | … | 12 |
| 2'-2" | 5" | 1'-7 7/16" | 2 | 10 | … | … | 12 |
| 2'-3" | 5 3/16" | 1'-8 3/16" | 1 | 11 | … | … | 12 |
| 2'-4" | 5⅜" | 1'-8 15/16" | 1 | 12 | … | … | 13 |
| 2'-5" | 5 9/16" | 1'-9 11/16" | 1 | 12 | … | … | 13 |
| 2'-6" | 5¾" | 1'-10 7/16" | … | 14 | … | … | 14 |
| 2'-7" | 5 15/16" | 1'-11 5/32" | … | 13 | 1 | … | 14 |
| 2'-8" | 6⅛" | 1'-11 29/32" | … | 13 | 1 | … | 14 |
| 2'-9" | 6 11/32" | 2'-0 21/32" | … | 12 | 2 | … | 14 |
| 2'-10" | 6 17/32" | 2'-1 13/32" | … | 12 | 3 | … | 15 |
| 2'-11" | 6 23/32" | 2'-2 5/32" | … | 11 | 4 | … | 15 |
| 3'-0" | 6 29/32" | 2'-2 29/32" | … | 11 | 5 | … | 16 |
| 3'-2" | 7 9/32" | 2'-4 13/32" | … | 10 | 6 | … | 16 |
| 3'-4" | 7 11/16" | 2'-5 29/32" | … | 10 | 7 | … | 17 |
| 3'-6" | 8 1/16" | 2'-7 13/32" | … | 9 | 9 | … | 18 |
| 3'-8" | 8 7/16" | 2'-8⅞" | … | 8 | 11 | … | 19 |
| 3'-10" | 8 13/16" | 2'-10⅜" | … | 7 | 12 | … | 19 |
| 4'-0" | 9 7/32" | 2'-11⅞" | … | 7 | 13 | … | 20 |
| 4'-2" | 9 19/32" | 3'-1⅜" | … | 6 | 15 | … | 21 |
| 4'-4" | 9 31/32" | 3'-2⅞" | … | 5 | 17 | … | 22 |
| 4'-6" | 10⅜" | 3'-4⅜" | … | 4 | 18 | … | 22 |
| 4'-8" | 10¾" | 3'-5 27/32" | … | 4 | 19 | … | 23 |
| 4'-10" | 11⅛" | 3'-7 11/32" | … | 3 | 21 | … | 24 |
| 5'-0" | 11½" | 3'-8 27/32" | … | 3 | 22 | … | 25 |
| 5'-2" | 11 29/32" | 3'-10 11/32" | … | 2 | 23 | … | 25 |
| 5'-4" | 1'-0 9/32" | 3'-11 27/32" | … | 1 | 25 | … | 26 |
| 5'-6" | 1'-0 21/32" | 4'-1 11/32" | … | … | 27 | … | 27 |
| 5'-8" | 1'-1 1/16" | 4'-2 13/16" | … | … | 27 | … | 27 |
| 5'-10" | 1'-1 7/16" | 4'-4 5/16" | … | … | 27 | 1 | 28 |
| 6'-0" | 1'-1 13/16" | 4'-5 13/16" | … | … | 27 | 2 | 29 |
| 6'-2" | 1'-2 3/16" | 4'-7 5/16" | … | … | 27 | 3 | 30 |
| 6'-4" | 1'-2 19/32" | 4'-8 13/16" | … | … | 27 | 3 | 30 |
| 6'-6" | 1'-2 31/32" | 4'-10 5/16" | … | … | 27 | 4 | 31 |

Footer: "See Page 106 For Skews". All totals check.

## Image (40).jpg — catalogue p.172–173

### p.172 — SPRUNG ARCHES — 1½" rise per foot of span — 6-INCH ARCH THICKNESS — Central Angle=56°

9"x6"x3", 12"x6"x3" or 13½"x6"x3". "Brand 4160-E to be used for Skew". Columns: No. 3 Arch 9x6x(3-2); No. 2 Arch 9x6x(3-2½); No. 1 Arch 9x6x(3-2¾); Straight 9x6x3.

| Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|
| 1'-0" | 1½" | 1'-0¾" | 6 | 1 | … | … | 7 |
| 1'-2" | 1¾" | 1'-2⅞" | 5 | 2 | … | … | 7 |
| 1'-4" | 2" | 1'-5" | 4 | 4 | … | … | 8 |
| 1'-6" | 2¼" | 1'-7⅛" | 4 | 5 | … | … | 9 |
| 1'-8" | 2½" | 1'-9¼" | 3 | 6 | … | … | 9 |
| 1'-10" | 2¾" | 1'-11⅜" | 2 | 8 | … | … | 10 |
| 2'-0" | 3" | 2'-1½" | 2 | 9 | … | … | 11 |
| 2'-2" | 3¼" | 2'-3⅝" | 1 | 10 | … | … | 11 |
| 2'-4" | 3½" | 2'-5¾" | … | 12 | … | … | 12 |
| 2'-6" | 3¾" | 2'-7⅞" | … | 11 | 2 | … | 13 |
| 2'-8" | 4" | 2'-10" | … | 10 | 3 | … | 13 |
| 2'-10" | 4¼" | 3'-0⅛" | … | 10 | 4 | … | 14 |
| 3'-0" | 4½" | 3'-2¼" | … | 9 | 6 | … | 15 |
| 3'-2" | 4¾" | 3'-4⅜" | … | 9 | 7 | … | 16 |
| 3'-4" | 5" | 3'-6½" | … | 8 | 8 | … | 16 |
| 3'-6" | 5¼" | 3'-8⅝" | … | 7 | 10 | … | 17 |
| 3'-8" | 5½" | 3'-10¾" | … | 7 | 11 | … | 18 |
| 3'-10" | 5¾" | 4'-0⅞" | … | 6 | 13 | … | 18 |
| 4'-0" | 6" | 4'-3" | … | 5 | 14 | … | 19 |
| 4'-2" | 6¼" | 4'-5⅛" | … | 5 | 15 | … | 20 |
| 4'-4" | 6½" | 4'-7¼" | … | 4 | 16 | … | 20 |
| 4'-6" | 6¾" | 4'-9⅜" | … | 3 | 18 | … | 21 |
| 4'-8" | 7" | 4'-11½" | … | 2 | 20 | … | 22 |
| 4'-10" | 7¼" | 5'-1⅝" | … | 1 | 21 | … | 22 |
| 5'-0" | 7½" | 5'-3¾" | … | 1 | 22 | … | 23 |
| 5'-2" | 7¾" | 5'-5⅞" | … | … | 24 | … | 24 |
| 5'-4" | 8" | 5'-8" | … | … | 24 | 1 | 25 |
| 5'-6" | 8¼" | 5'-10⅛" | … | … | 24 | 1 | 25 |
| 5'-8" | 8½" | 6'-0¼" | … | … | 24 | 2 | 26 |
| 5'-10" | 8¾" | 6'-2⅜" | … | … | 24 | 3 | 27 |
| 6'-0" | 9" | 6'-4½" | … | … | 24 | 3 | 27 |
| 6'-2" | 9¼" | 6'-6⅝" | … | … | 24 | 4 | 28 |
| 6'-4" | 9½" | 6'-8¾" | … | … | 24 | 5 | 29 |
| 6'-6" | 9¾" | 6'-10⅞" | … | … | 24 | 5 | 29 |
| 6'-8" | 10" | 7'-1" | … | … | 24 | 6 | 30 |
| 6'-10" | 10¼" | 7'-3⅛" | … | … | 24 | 7 | 31 |
| 7'-0" | 10½" | 7'-5¼" | … | … | 24 | 8 | 32 |
| 7'-2" | 10¾" | 7'-7⅜" | … | … | 24 | 8 | 32 |
| 7'-4" | 11" | 7'-9½" | … | … | 24 | 9 | 33 |
| 7'-6" | 11¼" | 7'-11⅝" | … | … | 24 | 10 | 34 |
| 7'-8" | 11½" | 8'-1¾" | … | … | 24 | 10 | 34 |
| 7'-10" | 11¾" | 8'-3⅞" | … | … | 24 | 11 | 35 |
| 8'-0" | 1'-0" | 8'-6" | … | … | 24 | 12 | 36 |

Footer: "See Page 106 For Skews".
Total check: MISMATCH at 3'-10" (6 + 13 = 19, printed 18); re-read on a zoomed crop. All other rows check. (Total column partly in the gutter; read from the overlapping crop.)

### p.173 — SPRUNG ARCHES — 1.608" rise per foot of span — 6-INCH ARCH THICKNESS — Central Angle=60°

9"x6"x3", 12"x6"x3" or 13½"x6"x3". "3 inch 60° sideskews to be used for Skew". Columns: No. 3 Arch 9x6x(3-2); No. 2 Arch 9x6x(3-2½); No. 1 Arch 9x6x(3-2¾); Straight 9x6x3.

| Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|
| 1'-0" | 1 19/32" | 1'-0" | 7 | … | … | … | 7 |
| 1'-2" | 1⅞" | 1'-2" | 6 | 1 | … | … | 7 |
| 1'-4" | 2 5/32" | 1'-4" | 5 | 3 | … | … | 8 |
| 1'-6" | 2 13/32" | 1'-6" | 4 | 5 | … | … | 9 |
| 1'-8" | 2 11/16" | 1'-8" | 3 | 6 | … | … | 9 |
| 1'-10" | 2 15/16" | 1'-10" | 3 | 7 | … | … | 10 |
| 2'-0" | 3 7/32" | 2'-0" | 2 | 9 | … | … | 11 |
| 2'-2" | 3½" | 2'-2" | 2 | 10 | … | … | 12 |
| 2'-4" | 3¾" | 2'-4" | 1 | 11 | … | … | 12 |
| 2'-6" | 4 1/32" | 2'-6" | … | 13 | … | … | 13 |
| 2'-8" | 4 9/32" | 2'-8" | … | 12 | 2 | … | 14 |
| 2'-10" | 4 9/16" | 2'-10" | … | 11 | 3 | … | 14 |
| 3'-0" | 4 13/16" | 3'-0" | … | 11 | 4 | … | 15 |
| 3'-2" | 5 3/32" | 3'-2" | … | 10 | 6 | … | 16 |
| 3'-4" | 5⅜" | 3'-4" | … | 9 | 7 | … | 16 |
| 3'-6" | 5⅝" | 3'-6" | … | 8 | 9 | … | 17 |
| 3'-8" | 5 29/32" | 3'-8" | … | 8 | 10 | … | 18 |
| 3'-10" | 6 5/32" | 3'-10" | … | 7 | 11 | … | 18 |
| 4'-0" | 6 7/16" | 4'-0" | … | 6 | 13 | … | 19 |
| 4'-2" | 6 23/32" | 4'-2" | … | 6 | 14 | … | 20 |
| 4'-4" | 6 31/32" | 4'-4" | … | 5 | 16 | … | 21 |
| 4'-6" | 7¼" | 4'-6" | … | 4 | 17 | … | 21 |
| 4'-8" | 7½" | 4'-8" | … | 4 | 18 | … | 22 |
| 4'-10" | 7 25/32" | 4'-10" | … | 3 | 20 | … | 23 |
| 5'-0" | 8 1/32" | 5'-0" | … | 2 | 21 | … | 23 |
| 5'-2" | 8 5/16" | 5'-2" | … | 2 | 22 | … | 24 |
| 5'-4" | 8 9/16" | 5'-4" | … | 1 | 24 | … | 25 |
| 5'-6" | 8 27/32" | 5'-6" | … | … | 25 | … | 25 |
| 5'-8" | 9⅛" | 5'-8" | … | … | 25 | 1 | 26 |
| 5'-10" | 9⅜" | 5'-10" | … | … | 25 | 2 | 27 |
| 6'-0" | 9 21/32" | 6'-0" | … | … | 25 | 3 | 28 |
| 6'-2" | 9 29/32" | 6'-2" | … | … | 25 | 3 | 28 |
| 6'-4" | 10 3/16" | 6'-4" | … | … | 25 | 4 | 29 |
| 6'-6" | 10 15/32" | 6'-6" | … | … | 25 | 5 | 30 |
| 6'-8" | 10 23/32" | 6'-8" | … | … | 25 | 5 | 30 |
| 6'-10" | 11" | 6'-10" | … | … | 25 | 6 | 31 |
| 7'-0" | 11¼" | 7'-0" | … | … | 25 | 7 | 32 |
| 7'-2" | 11 17/32" | 7'-2" | … | … | 25 | 7 | 32 |
| 7'-4" | 11 25/32" | 7'-4" | … | … | 25 | 8 | 33 |
| 7'-6" | 1'-0 1/16" | 7'-6" | … | … | 25 | 9 | 34 |
| 7'-8" | 1'-0 5/16" | 7'-8" | … | … | 25 | 10 | 35 |
| 7'-10" | 1'-0 19/32" | 7'-10" | … | … | 25 | 10 | 35 |
| 8'-0" | 1'-0⅞" | 8'-0" | … | … | 25 | 11 | 36 |

Footer: "See Page 106 For Skews". All totals check.

## Image (41).jpg — catalogue p.174–175

### p.174 — SPRUNG ARCHES — 2" rise per foot of span — 6-INCH ARCH THICKNESS — Central Angle=74°

9"x6"x3", 12"x6"x3" or 13½"x6"x3". "Brand 4160-F to be used for Skew". Columns: No. 3 Arch 9x6x(3-2); No. 2 Arch 9x6x(3-2½); No. 1 Arch 9x6x(3-2¾); Straight 9x6x3.

| Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|
| 1'-4" | 2 21/32" | 1'-1 5/16" | 8 | 1 | … | … | 9 |
| 1'-6" | 3" | 1'-3" | 6 | 3 | … | … | 9 |
| 1'-8" | 3 11/32" | 1'-4 21/32" | 6 | 4 | … | … | 10 |
| 1'-10" | 3 21/32" | 1'-6 11/32" | 5 | 6 | … | … | 11 |
| 2'-0" | 4" | 1'-8" | 4 | 7 | … | … | 11 |
| 2'-2" | 4 11/32" | 1'-9 21/32" | 4 | 8 | … | … | 12 |
| 2'-4" | 4 21/32" | 1'-11 11/32" | 3 | 10 | … | … | 13 |
| 2'-6" | 5" | 2'-1" | 2 | 12 | … | … | 14 |
| 2'-8" | 5 11/32" | 2'-2 21/32" | 1 | 13 | … | … | 14 |
| 2'-10" | 5 21/32" | 2'-4 11/32" | 1 | 14 | … | … | 15 |
| 3'-0" | 6" | 2'-6" | … | 16 | … | … | 16 |
| 3'-2" | 6 11/32" | 2'-7 21/32" | … | 15 | 1 | … | 16 |
| 3'-4" | 6 21/32" | 2'-9 11/32" | … | 14 | 3 | … | 17 |
| 3'-6" | 7" | 2'-11" | … | 13 | 5 | … | 18 |
| 3'-8" | 7 11/32" | 3'-0 21/32" | … | 13 | 6 | … | 19 |
| 3'-10" | 7 21/32" | 3'-2 11/32" | … | 12 | 7 | … | 19 |
| 4'-0" | 8" | 3'-4" | … | 11 | 9 | … | 20 |
| 4'-2" | 8 11/32" | 3'-5 21/32" | … | 11 | 10 | … | 21 |
| 4'-4" | 8 21/32" | 3'-7 11/32" | … | 10 | 11 | … | 21 |
| 4'-6" | 9" | 3'-9" | … | 9 | 13 | … | 22 |
| 4'-8" | 9 11/32" | 3'-10 21/32" | … | 8 | 15 | … | 23 |
| 4'-10" | 9 21/32" | 4'-0 11/32" | … | 8 | 16 | … | 24 |
| 5'-0" | 10" | 4'-2" | … | 7 | 17 | … | 24 |
| 5'-2" | 10 11/32" | 4'-3 21/32" | … | 6 | 19 | … | 25 |
| 5'-4" | 10 21/32" | 4'-5 11/32" | … | 6 | 20 | … | 26 |
| 5'-6" | 11" | 4'-7" | … | 5 | 21 | … | 26 |
| 5'-8" | 11 11/32" | 4'-8 21/32" | … | 4 | 23 | … | 27 |
| 5'-10" | 11 21/32" | 4'-10 11/32" | … | 3 | 25 | … | 28 |
| 6'-0" | 1'-0" | 5'-0" | … | 3 | 26 | … | 29 |
| 6'-2" | 1'-0 11/32" | 5'-1 21/32" | … | 2 | 27 | … | 29 |
| 6'-4" | 1'-0 21/32" | 5'-3 11/32" | … | 1 | 29 | … | 30 |
| 6'-6" | 1'-1" | 5'-5" | … | 1 | 30 | … | 31 |
| 6'-9" | 1'-1½" | 5'-7½" | … | … | 31 | 1 | 32 |
| 7'-0" | 1'-2" | 5'-10" | … | … | 31 | 2 | 33 |
| 7'-3" | 1'-2½" | 6'-0½" | … | … | 31 | 3 | 34 |
| 7'-6" | 1'-3" | 6'-3" | … | … | 31 | 4 | 35 |
| 7'-9" | 1'-3½" | 6'-5½" | … | … | 31 | 5 | 36 |
| 8'-0" | 1'-4" | 6'-8" | … | … | 31 | 6 | 37 |

Footer: "See Page 106 For Skews". All totals check (total column partly in the gutter, read from the overlapping crop).

### p.175 — SPRUNG ARCHES — 2.302" rise per foot of span — 6-INCH ARCH THICKNESS — Central Angle=84°

9"x6"x3", 12"x6"x3" or 13½"x6"x3". "3 inch 48° sideskews to be used for Skew". Columns: No. 3 Arch 9x6x(3-2); No. 2 Arch 9x6x(3-2½); No. 1 Arch 9x6x(3-2¾); Straight 9x6x3.

| Span | Rise | Inside radius | No. 3 | No. 2 | No. 1 | Straight | Total |
|---|---|---|---|---|---|---|---|
| 1'-4" | 3 1/16" | 11 31/32" | 9 | … | … | … | 9 |
| 1'-6" | 3 15/32" | 1'-1 15/32" | 8 | 2 | … | … | 10 |
| 1'-8" | 3 27/32" | 1'-2 15/16" | 8 | 3 | … | … | 11 |
| 1'-10" | 4 7/32" | 1'-4 7/16" | 7 | 4 | … | … | 11 |
| 2'-0" | 4 19/32" | 1'-5 15/16" | 6 | 6 | … | … | 12 |
| 2'-2" | 5" | 1'-7 7/16" | 5 | 8 | … | … | 13 |
| 2'-4" | 5⅜" | 1'-8 15/16" | 4 | 9 | … | … | 13 |
| 2'-6" | 5¾" | 1'-10 7/16" | 4 | 10 | … | … | 14 |
| 2'-8" | 6⅛" | 1'-11 29/32" | 3 | 12 | … | … | 15 |
| 2'-10" | 6 17/32" | 2'-1 13/32" | 2 | 14 | … | … | 16 |
| 3'-0" | 6 29/32" | 2'-2 29/32" | 2 | 14 | … | … | 16 |
| 3'-2" | 7 9/32" | 2'-4 13/32" | 1 | 16 | … | … | 17 |
| 3'-4" | 7 11/16" | 2'-5 29/32" | … | 18 | … | … | 18 |
| 3'-6" | 8 1/16" | 2'-7 13/32" | … | 17 | 2 | … | 19 |
| 3'-8" | 8 7/16" | 2'-8⅞" | … | 16 | 3 | … | 19 |
| 3'-10" | 8 13/16" | 2'-10⅜" | … | 15 | 5 | … | 20 |
| 4'-0" | 9 7/32" | 2'-11⅞" | … | 15 | 6 | … | 21 |
| 4'-2" | 9 19/32" | 3'-1⅜" | … | 14 | 8 | … | 22 |
| 4'-4" | 9 31/32" | 3'-2⅞" | … | 13 | 9 | … | 22 |
| 4'-6" | 10 11/32" | 3'-4⅜" | … | 13 | 10 | … | 23 |
| 4'-8" | 10¾" | 3'-5 27/32" | … | 12 | 12 | … | 24 |
| 4'-10" | 11⅛" | 3'-7 11/32" | … | 11 | 13 | … | 24 |
| 5'-0" | 11½" | 3'-8 27/32" | … | 10 | 15 | … | 25 |
| 5'-2" | 11 29/32" | 3'-10 11/32" | … | 10 | 16 | … | 26 |
| 5'-4" | 1'-0 9/32" | 3'-11 27/32" | … | 9 | 18 | … | 27 |
| 5'-6" | 1'-0 21/32" | 4'-1 11/32" | … | 8 | 19 | … | 27 |
| 5'-8" | 1'-1 1/32" | 4'-2 13/16" | … | 7 | 21 | … | 28 |
| 5 -10" (sic) | 1'-1 7/16" | 4'-4 5/16" | … | 7 | 22 | … | 29 |
| 6'-0" | 1'-1 13/16" | 4'-5 13/16" | … | 6 | 24 | … | 30 |
| 6'-2" | 1'-2 3/16" | 4'-7 5/16" | … | 5 | 25 | … | 30 |
| 6'-4" | 1'-2 19/32" | 4'-8 13/16" | … | 5 | 26 | … | 31 |
| 6'-6" | 1'-2 31/32" | 4'-10 5/16" | … | 4 | 28 | … | 32 |
| 6'-8" | 1'-3 11/32" | 4'-11 25/32" | … | 3 | 29 | … | 32 |
| 6'-10" | 1'-3 23/32" | 5'-1 9/32" | … | 2 | 31 | … | 33 |
| 7'-0" | 1'-4⅛" | 5'-2 25/32" | … | 2 | 32 | … | 34 |
| 7'-2" | 1'-4½" | 5'-4 9/32" | … | … | 35 | … | 35 |
| 7'-4" | 1'-4⅞" | 5'-5 25/32" | … | … | 35 | … | 35 |
| 7'-6" | 1'-5¼" | 5'-7¼" | … | … | 35 | 1 | 36 |
| 7'-8" | 1'-5 21/32" | 5'-8¾" | … | … | 35 | 2 | 37 |
| 7'-10" | 1'-6 1/32" | 5'-10¼" | … | … | 35 | 3 | 38 |
| 8'-0" | 1'-6 13/32" | 5'-11¾" | … | … | 35 | 3 | 38 |

Footer: "See Page 106 For Skews". All totals check. (5'-8" rise prints 1'-1 1/32" where the 2.302" series elsewhere has 1'-1 1/16"; transcribed as printed. 7'-2" jumps from 32 to 35 No. 1 arch as printed.)

## Image (42).jpg — catalogue p.176–177

### p.176 — SPRUNG ARCHES — 1½" rise per foot of span — 9-INCH ARCH THICKNESS — Central Angle=56°

9"x4½"x2½", 9"x6¾"x2½" or 9"x9"x2½". "Standard 9 inch Featheredge to be used for Skew". Columns: No. 2 Wedge 9x4½x(2½-1½); No. 1 Wedge 9x4½x(2½-1⅞); No. 1-X Wedge 9x4½x(2½-2¼); Straights 9x4½x2½.

| Span | Rise | Inside radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 1'-6" | 2¼" | 1'-7⅛" | 5 | 6 | … | … | 11 |
| 1'-7" | 2⅜" | 1'-8 3/16" | 5 | 7 | … | … | 12 |
| 1'-8" | 2½" | 1'-9¼" | 4 | 8 | … | … | 12 |
| 1'-9" | 2⅝" | 1'-10 5/16" | 3 | 10 | … | … | 13 |
| 1'-10" | 2¾" | 1'-11⅜" | 2 | 11 | … | … | 13 |
| 1'-11" | 2⅞" | 2'-0 7/16" | 2 | 12 | … | … | 14 |
| 2'-0" | 3" | 2'-1½" | 1 | 13 | … | … | 14 |
| 2'-1" | 3⅛" | 2'-2 9/16" | … | 14 | … | … | 14 |
| 2'-2" | 3¼" | 2'-3⅝" | … | 14 | 1 | … | 15 |
| 2'-3" | 3⅜" | 2'-4 11/16" | … | 14 | 1 | … | 15 |
| 2'-4" | 3½" | 2'-5¾" | … | 14 | 2 | … | 16 |
| 2'-5" | 3⅝" | 2'-6 13/16" | … | 13 | 3 | … | 16 |
| 2'-6" | 3¾" | 2'-7⅞" | … | 13 | 3 | … | 16 |
| 2'-7" | 3⅞" | 2'-8 15/16" | … | 13 | 4 | … | 17 |
| 2'-8" | 4" | 2'-10" | … | 12 | 5 | … | 17 |
| 2'-9" | 4⅛" | 2'-11 1/16" | … | 12 | 6 | … | 18 |
| 2'-10" | 4¼" | 3'-0⅛" | … | 12 | 6 | … | 18 |
| 2'-11" | 4⅜" | 3'-1 3/16" | … | 12 | 7 | … | 19 |
| 3'-0" | 4½" | 3'-2¼" | … | 11 | 8 | … | 19 |
| 3'-1" | 4⅝" | 3'-3 5/16" | … | 11 | 8 | … | 19 |
| 3'-2" | 4¾" | 3'-4⅜" | … | 11 | 9 | … | 20 |
| 3'-3" | 4⅞" | 3'-5 7/16" | … | 10 | 10 | … | 20 |
| 3'-4" | 5" | 3'-6½" | … | 10 | 11 | … | 21 |
| 3'-5" | 5⅛" | 3'-7 9/16" | … | 10 | 11 | … | 21 |
| 3'-6" | 5¼" | 3'-8⅝" | … | 10 | 11 | … | 21 |
| 3'-7" | 5⅜" | 3'-9 11/16" | … | 10 | 12 | … | 22 |
| 3'-8" | 5½" | 3'-10¾" | … | 9 | 13 | … | 22 |
| 3'-9" | 5⅝" | 3'-11 13/16" | … | 9 | 14 | … | 23 |
| 3'-10" | 5¾" | 4'-0⅞" | … | 9 | 14 | … | 23 |
| 3'-11" | 5⅞" | 4'-1 15/16" | … | 9 | 15 | … | 24 |
| 4'-0" | 6" | 4'-3" | … | 8 | 16 | … | 24 |
| 4'-1" | 6⅛" | 4'-4 1/16" | … | 8 | 16 | … | 24 |
| 4'-2" | 6¼" | 4'-5⅛" | … | 8 | 17 | … | 25 |
| 4'-3" | 6⅜" | 4'-6 3/16" | … | 7 | 18 | … | 25 |
| 4'-4" | 6½" | 4'-7¼" | … | 7 | 19 | … | 26 |
| 4'-5" | 6⅝" | 4'-8 5/16" | … | 7 | 19 | … | 26 |
| 4'-6" | 6¾" | 4'-9⅜" | … | 6 | 20 | … | 26 |
| 4'-7" | 6⅞" | 4'-10 7/16" | … | 6 | 21 | … | 27 |
| 4'-8" | 7" | 4'-11½" | … | 6 | 21 | … | 27 |
| 4'-9" | 7⅛" | 5'-0 9/16" | … | 6 | 22 | … | 28 |
| 4'-10" | 7¼" | 5'-1⅝" | … | 5 | 23 | … | 28 |
| 4'-11" | 7⅜" | 5'-2 11/16" | … | 5 | 23 | … | 28 |
| 5'-0" | 7½" | 5'-3¾" | … | 5 | 24 | … | 29 |
| 5'-1" | 7⅝" | 5'-4 13/16" | … | 4 | 25 | … | 29 |
| 5'-2" | 7¾" | 5'-5⅞" | … | 4 | 26 | … | 30 |

Footer: "See Page 106 For Skews"; "Continued Next Page". All totals check.

### p.177 — SPRUNG ARCHES — 1½" rise per foot of span — 9-INCH ARCH THICKNESS — Central Angle=56° (continued)

Same title lines and columns as p.176.

| Span | Rise | Inside radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 5'-3" | 7⅞" | 5'-6 15/16" | … | 4 | 26 | … | 30 |
| 5'-4" | 8" | 5'-8" | … | 4 | 27 | … | 31 |
| 5'-5" | 8⅛" | 5'-9 1/16" | … | 3 | 28 | … | 31 |
| 5'-6" | 8¼" | 5'-10⅛" | … | 3 | 28 | … | 31 |
| 5'-7" | 8⅜" | 5'-11 3/16" | … | 3 | 29 | … | 32 |
| 5'-8" | 8½" | 6'-0¼" | … | 2 | 30 | … | 32 |
| 5'-9" | 8⅝" | 6'-1 5/16" | … | 2 | 31 | … | 33 |
| 5'-10" | 8¾" | 6'-2⅜" | … | 2 | 31 | … | 33 |
| 5'-11" | 8⅞" | 6'-3 7/16" | … | 1 | 32 | … | 33 |
| 6'-0" | 9" | 6'-4½" | … | 1 | 33 | … | 34 |
| 6'-1" | 9⅛" | 6'-5 9/16" | … | 1 | 33 | … | 34 |
| 6'-2" | 9¼" | 6'-6⅝" | … | 1 | 34 | … | 35 |
| 6'-3" | 9⅜" | 6'-7 11/16" | … | … | 35 | … | 35 |
| 6'-4" | 9½" | 6'-8¾" | … | … | 36 | … | 36 |
| 6'-5" | 9⅝" | 6'-9 13/16" | … | … | 36 | … | 36 |
| 6'-6" | 9¾" | 6'-10⅞" | … | … | 36 | … | 36 |
| 6'-9" | 10⅛" | 7'-2 1/16" | … | … | 36 | 2 | 38 |
| 7'-0" | 10½" | 7'-5¼" | … | … | 36 | 3 | 39 |
| 7'-3" | 10⅞" | 7'-8 7/16" | … | … | 36 | 4 | 40 |
| 7'-6" | 11¼" | 7'-11⅝" | … | … | 36 | 5 | 41 |
| 7'-9" | 11⅝" | 8'-2 13/16" | … | … | 36 | 7 | 43 |
| 8'-0" | 1'-0" | 8'-6" | … | … | 36 | 8 | 44 |
| 8'-3" | 1'-0⅜" | 8'-9 3/16" | … | … | 36 | 9 | 45 |
| 8'-6" | 1'-0¾" | 9'-0⅜" | … | … | 36 | 10 | 46 |
| 8'-9" | 1'-1⅛" | 9'-3 9/16" | … | … | 36 | 12 | 48 |
| 9'-0" | 1'-1½" | 9'-6¾" | … | … | 36 | 13 | 49 |
| 9'-3" | 1'-1⅞" | 9'-9 15/16" | … | … | 36 | 14 | 50 |
| 9'-6" | 1'-2¼" | 10'-1⅛" | … | … | 36 | 15 | 51 |
| 9'-9" | 1'-2⅝" | 10'-4 5/16" | … | … | 36 | 17 | 53 |
| 10'-0" | 1'-3" | 10'-7½" | … | … | 36 | 18 | 54 |
| 10'-3" | 1'-3⅜" | 10'-10 11/16" | … | … | 36 | 19 | 55 |
| 10'-6" | 1'-3¾" | 11'-1⅞" | … | … | 36 | 20 | 56 |
| 10'-9" | 1'-4⅛" | 11'-5 1/16" | … | … | 36 | 22 | 58 |
| 11'-0" | 1'-4½" | 11'-8¼" | … | … | 36 | 23 | 59 |
| 11'-3" | 1'-4⅞" | 11'-11 7/16" | … | … | 36 | 24 | 60 |
| 11'-6" | 1'-5¼" | 12'-2⅝" | … | … | 36 | 25 | 61 |
| 11'-9" | 1'-5⅝" | 12'-5 13/16" | … | … | 36 | 27 | 63 |
| 12'-0" | 1'-6" | 12'-9" | … | … | 36 | 28 | 64 |
| 12'-3" | 1'-6⅜" | 13'-0 3/16" | … | … | 36 | 29 | 65 |
| 12'-6" | 1'-6¾" | 13'-3⅜" | … | … | 36 | 30 | 66 |
| 12'-9" | 1'-7⅛" | 13'-6 9/16" | … | … | 36 | 32 | 68 |
| 13'-0" | 1'-7½" | 13'-9¾" | … | … | 36 | 33 | 69 |
| 13'-3" | 1'-7⅞" | 14'-0 15/16" | … | … | 36 | 34 | 70 |
| 13'-6" | 1'-8¼" | 14'-4⅛" | … | … | 36 | 35 | 71 |
| 13'-9" | 1'-8⅝" | 14'-7 5/16" | … | … | 36 | 37 | 73 |
| 14'-0" | 1'-9" | 14'-11½" | … | … | 36 | 38 | 74 |

Footer: "See Page 106 For Skews". All totals check.

## Image (43).jpg — catalogue p.178–179

### p.178 — SPRUNG ARCHES — 1½" rise per foot of span — 9-INCH ARCH THICKNESS — Central Angle=56°

9"x4½"x3", 9"x6¾"x3" or 9"x9"x3". "Standard 9 inch Featheredge to be used for Skew". Columns: No. 3 Wedge 9x4½x(3-2); No. 2 Wedge 9x4½x(3-2½); No. 1 Wedge 9x4½x(3-2¾); Straights 9x4½x3.

| Span | Rise | Inside radius | No. 3 Wedge | No. 2 Wedge | No. 1 Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 1'-6" | 2¼" | 1'-7⅛" | 9 | 1 | … | … | 10 |
| 1'-7" | 2⅜" | 1'-8 3/16" | 8 | 2 | … | … | 10 |
| 1'-8" | 2½" | 1'-9¼" | 8 | 2 | … | … | 10 |
| 1'-9" | 2⅝" | 1'-10 5/16" | 8 | 3 | … | … | 11 |
| 1'-10" | 2¾" | 1'-11⅜" | 7 | 4 | … | … | 11 |
| 1'-11" | 2⅞" | 2'-0 7/16" | 7 | 4 | … | … | 11 |
| 2'-0" | 3" | 2'-1½" | 7 | 5 | … | … | 12 |
| 2'-1" | 3⅛" | 2'-2 9/16" | 6 | 6 | … | … | 12 |
| 2'-2" | 3¼" | 2'-3⅝" | 6 | 6 | … | … | 12 |
| 2'-3" | 3⅜" | 2'-4 11/16" | 6 | 7 | … | … | 13 |
| 2'-4" | 3½" | 2'-5¾" | 5 | 8 | … | … | 13 |
| 2'-5" | 3⅝" | 2'-6 13/16" | 5 | 8 | … | … | 13 |
| 2'-6" | 3¾" | 2'-7⅞" | 5 | 9 | … | … | 14 |
| 2'-7" | 3⅞" | 2'-8 15/16" | 4 | 10 | … | … | 14 |
| 2'-8" | 4" | 2'-10" | 4 | 10 | … | … | 14 |
| 2'-9" | 4⅛" | 2'-11 1/16" | 4 | 11 | … | … | 15 |
| 2'-10" | 4¼" | 3'-0⅛" | 3 | 12 | … | … | 15 |
| 2'-11" | 4⅜" | 3'-1 3/16" | 3 | 12 | … | … | 15 |
| 3'-0" | 4½" | 3'-2¼" | 2 | 14 | … | … | 16 |
| 3'-1" | 4⅝" | 3'-3 5/16" | 2 | 14 | … | … | 16 |
| 3'-2" | 4¾" | 3'-4⅜" | 2 | 15 | … | … | 17 |
| 3'-3" | 4⅞" | 3'-5 7/16" | 1 | 16 | … | … | 17 |
| 3'-4" | 5" | 3'-6½" | 1 | 16 | … | … | 17 |
| 3'-5" | 5⅛" | 3'-7 9/16" | 1 | 17 | … | … | 18 |
| 3'-6" | 5¼" | 3'-8⅝" | … | 18 | … | … | 18 |
| 3'-7" | 5⅜" | 3'-9 11/16" | … | 18 | … | … | 18 |
| 3'-8" | 5½" | 3'-10¾" | … | 17 | 2 | … | 19 |
| 3'-9" | 5⅝" | 3'-11 13/16" | … | 17 | 2 | … | 19 |
| 3'-10" | 5¾" | 4'-0⅞" | … | 16 | 3 | … | 19 |
| 3'-11" | 5⅞" | 4'-1 15/16" | … | 16 | 4 | … | 20 |
| 4'-0" | 6" | 4'-3" | … | 16 | 4 | … | 20 |
| 4'-1" | 6⅛" | 4'-4 1/16" | … | 15 | 5 | … | 20 |
| 4'-2" | 6¼" | 4'-5⅛" | … | 15 | 6 | … | 21 |
| 4'-3" | 6⅜" | 4'-6 3/16" | … | 15 | 6 | … | 21 |
| 4'-4" | 6½" | 4'-7¼" | … | 14 | 7 | … | 21 |
| 4'-5" | 6⅝" | 4'-8 5/16" | … | 14 | 8 | … | 22 |
| 4'-6" | 6¾" | 4'-9⅜" | … | 14 | 8 | … | 22 |
| 4'-7" | 6⅞" | 4'-10 7/16" | … | 13 | 9 | … | 22 |
| 4'-8" | 7" | 4'-11½" | … | 13 | 10 | … | 23 |
| 4'-9" | 7⅛" | 5'-0 9/16" | … | 13 | 10 | … | 23 |
| 4'-10" | 7¼" | 5'-1⅝" | … | 12 | 11 | … | 23 |
| 4'-11" | 7⅜" | 5'-2 11/16" | … | 12 | 12 | … | 24 |
| 5'-0" | 7½" | 5'-3¾" | … | 12 | 12 | … | 24 |
| 5'-1" | 7⅝" | 5'-4 13/16" | … | 11 | 13 | … | 24 |
| 5'-2" | 7¾" | 5'-5⅞" | … | 11 | 14 | … | 25 |

Footer: "See Page 106 For Skews"; "Continued Next Page". All totals check (total column in the gutter; read from the facing-page crop).

### p.179 — SPRUNG ARCHES — 1½" rise per foot of span — 9-INCH ARCH THICKNESS — Central Angle=56° (continued)

9"x4½"x3", 9"x6¾"x3" or 9"x9"x3"; same columns as p.178.

| Span | Rise | Inside radius | No. 3 Wedge | No. 2 Wedge | No. 1 Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 5'-3" | 7⅞" | 5'-6 15/16" | … | 11 | 14 | … | 25 |
| 5'-4" | 8" | 5'-8" | … | 10 | 15 | … | 25 |
| 5'-5" | 8⅛" | 5'-9 1/16" | … | 10 | 16 | … | 26 |
| 5'-6" | 8¼" | 5'-10⅛" | … | 10 | 16 | … | 26 |
| 5'-7" | 8⅜" | 5'-11 3/16" | … | 10 | 17 | … | 27 |
| 5'-8" | 8½" | 6'-0¼" | … | 9 | 18 | … | 27 |
| 5'-9" | 8⅝" | 6'-1 5/16" | … | 8 | 19 | … | 27 |
| 5'-10" | 8¾" | 6'-2⅜" | … | 8 | 20 | … | 28 |
| 5'-11" | 8⅞" | 6'-3 7/16" | … | 8 | 20 | … | 28 |
| 6'-0" | 9" | 6'-4½" | … | 7 | 21 | … | 28 |
| 6'-1" | 9⅛" | 6'-5 9/16" | … | 7 | 22 | … | 29 |
| 6'-2" | 9¼" | 6'-6⅝" | … | 7 | 22 | … | 29 |
| 6'-3" | 9⅜" | 6'-7 11/16" | … | 6 | 23 | … | 29 |
| 6'-4" | 9½" | 6'-8¾" | … | 6 | 24 | … | 30 |
| 6'-5" | 9⅝" | 6'-9 13/16" | … | 6 | 24 | … | 30 |
| 6'-6" | 9¾" | 6'-10⅞" | … | 5 | 25 | … | 30 |
| 6'-7" | 9⅞" | 6'-11 15/16" | … | 5 | 26 | … | 31 |
| 6'-8" | 10" | 7'-1" | … | 5 | 26 | … | 31 |
| 6'-9" | 10⅛" | 7'-2 1/16" | … | 4 | 27 | … | 31 |
| 6'-10" | 10¼" | 7'-3⅛" | … | 4 | 28 | … | 32 |
| 6'-11" | 10⅜" | 7'-4 3/16" | … | 4 | 28 | … | 32 |
| 7'-0" | 10½" | 7'-5¼ (sic, no inch mark) | … | 3 | 29 | … | 32 |
| 7'-1" | 10⅝" | 7'-6 5/16" | … | 3 | 30 | … | 33 |
| 7'-2" | 10¾" | 7'-7⅜" | … | 3 | 30 | … | 33 |
| 7'-3" | 10⅞" | 7'-8 7/16" | … | 2 | 31 | … | 33 |
| 7'-4" | 11" | 7'-9½" | … | 2 | 32 | … | 34 |
| 7'-5" | 11⅛" | 7'-10 9/16" | … | 2 | 32 | … | 34 |
| 7'-6" | 11¼" | 7'-11⅝" | … | 1 | 33 | … | 34 |
| 7'-7" | 11⅜" | 8'-0 11/16" | … | 1 | 34 | … | 35 |
| 7'-8" | 11½" | 8' -1¾" | … | 1 | 34 | … | 35 |
| 7'-9" | 11⅝" | 8'-2 13/16" | … | … | 35 | … | 35 |
| 7'-10" | 11¾" | 8'-3⅞" | … | … | 36 | … | 36 |
| 7'-11" | 11⅞" | 8'-4 15/16" | … | … | 36 | … | 36 |
| 8'-0" | 1'-0" | 8'-6" | … | … | 36 | 1 | 37 |
| 8'-6" | 1'-0¾" | 9'-0⅜" | … | … | 36 | 3 | 39 |
| 9'-0" | 1'-1½" | 9' -6¾" | … | … | 36 | 5 | 41 |
| 9'-6" | 1'-2¼" | 10'-1⅛" | … | … | 36 | 7 | 43 |
| 10'-0" | 1'-3" | 10'-7½" | … | … | 36 | 9 | 45 |
| 10'-6" | 1'-3¾" | 11'-1⅞" | … | … | 36 | 11 | 47 |
| 11'-0" | 1'-4½" | 11'-8¼" | … | … | 36 | 13 | 49 |
| 11'-6" | 1'-5¼" | 12'-2⅝" | … | … | 36 | 15 | 51 |
| 12'-0" | 1'-6" | 12'-9" | … | … | 36 | 17 | 53 |
| 12'-6" | 1'-6¾" | 13'-3⅜" | … | … | 36 | 19 | 55 |
| 13'-0" | 1'-7½" | 13'-9¾" | … | … | 36 | 21 | 57 |
| 13'-6" | 1'-8¼" | 14'-4⅛" | … | … | 36 | 24 | 60 |
| 14'-0" | 1'-9" | 14'-11½" | … | … | 36 | 26 | 62 |

Footer: "See Page 106 For Skews". All totals check.

## Image (44).jpg — catalogue p.180–181

### p.180 — SPRUNG ARCHES — 1.608" rise per foot of span — 9-INCH ARCH THICKNESS — Central Angle=60°

9"x4½"x2½", 9"x6¾"x2½" or 9"x9"x2½". "Brand 4160-B to be used for Skew". Columns: No. 2 Wedge 9x4½x(2½-1½); No. 1 Wedge 9x4½x(2½-1⅞); No. 1-X Wedge 9x4½x(2½-2¼); Straights 9x4½x2½. (Inside radius = span.)

| Span | Rise | Inside radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 1'-6" | 2 13/32" | 1'-6" | 7 | 5 | … | … | 12 |
| 1'-7" | 2 17/32" | 1'-7" | 6 | 6 | … | … | 12 |
| 1'-8" | 2 11/16" | 1'-8" | 5 | 8 | … | … | 13 |
| 1'-9" | 2 13/16" | 1'-9" | 4 | 9 | … | … | 13 |
| 1'-10" | 2 15/16" | 1'-10" | 3 | 10 | … | … | 13 |
| 1'-11" | 3 3/32" | 1'-11" | 3 | 11 | … | … | 14 |
| 2'-0" | 3 7/32" | 2'-0" | 2 | 12 | … | … | 14 |
| 2'-1" | 3 11/32" | 2'-1" | 2 | 13 | … | … | 15 |
| 2'-2" | 3 15/32" | 2'-2" | 1 | 14 | … | … | 15 |
| 2'-3" | 3⅝" | 2'-3" | … | 15 | … | … | 15 |
| 2'-4" | 3¾" | 2'-4" | … | 15 | 1 | … | 16 |
| 2'-5" | 3⅞" | 2'-5" | … | 15 | 1 | … | 16 |
| 2'-6" | 4 1/32" | 2'-6" | … | 15 | 2 | … | 17 |
| 2'-7" | 4 5/32" | 2'-7" | … | 14 | 3 | … | 17 |
| 2'-8" | 4 9/32" | 2'-8" | … | 14 | 4 | … | 18 |
| 2'-9" | 4 7/16" | 2'-9" | … | 14 | 4 | … | 18 |
| 2'-10" | 4 9/16" | 2'-10" | … | 13 | 5 | … | 18 |
| 2'-11" | 4 11/16" | 2'-11" | … | 13 | 6 | … | 19 |
| 3'-0" | 4 13/16" | 3'-0" | … | 13 | 6 | … | 19 |
| 3'-1" | 4 31/32" | 3'-1" | … | 13 | 7 | … | 20 |
| 3'-2" | 5 3/32" | 3'-2" | … | 12 | 8 | … | 20 |
| 3'-3" | 5 7/32" | 3'-3" | … | 12 | 8 | … | 20 |
| 3'-4" | 5 11/32" | 3'-4" | … | 12 | 9 | … | 21 |
| 3'-5" | 5½" | 3'-5" | … | 11 | 10 | … | 21 |
| 3'-6" | 5⅝" | 3'-6" | … | 11 | 11 | … | 22 |
| 3'-7" | 5¾" | 3'-7" | … | 11 | 11 | … | 22 |
| 3'-8" | 5 29/32 (sic, no inch mark) | 3'-8" | … | 11 | 12 | … | 23 |
| 3'-9" | 6 1/32" | 3'-9" | … | 10 | 13 | … | 23 |
| 3'-10" | 6 5/32" | 3'-10" | … | 10 | 13 | … | 23 |
| 3'-11" | 6 9/32" | 3'-11" | … | 10 | 14 | … | 24 |
| 4'-0" | 6 7/16" | 4'-0" | … | 9 | 15 | … | 24 |
| 4'-1" | 6 9/16" | 4'-1" | … | 9 | 16 | … | 25 |
| 4'-2" | 6 11/16" | 4'-2" | … | 9 | 16 | … | 25 |
| 4'-3" | 6 27/32" | 4'-3" | … | 9 | 17 | … | 26 |
| 4'-4" | 6 31/32" | 4'-4" | … | 8 | 18 | … | 26 |
| 4'-5" | 7 3/32" | 4'-5" | … | 8 | 18 | … | 26 |
| 4'-6" | 7¼" | 4'-6" | … | 8 | 19 | … | 27 |
| 4'-7" | 7⅜" | 4'-7" | … | 7 | 20 | … | 27 |
| 4'-8" | 7½" | 4'-8" | … | 7 | 21 | … | 28 |
| 4'-9" | 7⅝" | 4'-9" | … | 7 | 21 | … | 28 |
| 4'-10" | 7 25/32" | 4'-10" | … | 6 | 22 | … | 28 |
| 4'-11" | 7 29/32" | 4'-11" | … | 6 | 23 | … | 29 |
| 5'-0" | 8 1/32" | 5'-0" | … | 6 | 23 | … | 29 |
| 5'-1" | 8 3/16" | 5'-1" | … | 6 | 24 | … | 30 |
| 5'-2" | 8 5/16" | 5'-2" | … | 5 | 25 | … | 30 |
| 5'-3" | 8 7/16" | 5'-3" | … | 5 | 26 | … | 31 |

Footer: "See Page 106 For Skews"; "Continued Next Page". All totals check (total column in the gutter; read from the facing-page crop).

### p.181 — SPRUNG ARCHES — 1.608" rise per foot of span — 9-INCH ARCH THICKNESS — Central Angle=60° (continued)

Same title lines and columns as p.180.

| Span | Rise | Inside radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 5'-4" | 8 9/16" | 5'-4" | … | 5 | 26 | … | 31 |
| 5'-5" | 8 23/32" | 5'-5" | … | 4 | 27 | … | 31 |
| 5'-6" | 8 27/32" | 5'-6" | … | 4 | 28 | … | 32 |
| 5'-7" | 8 31/32" | 5'-7" | … | 4 | 28 | … | 32 |
| 5'-8" | 9⅛" | 5'-8" | … | 4 | 29 | … | 33 |
| 5'-9" | 9¼" | 5'-9" | … | 3 | 30 | … | 33 |
| 5'-10" | 9⅜" | 5'-10" | … | 3 | 30 | … | 33 |
| 5'-11" | 9½" | 5'-11" | … | 3 | 31 | … | 34 |
| 6'-0" | 9 21/32" | 6'-0" | … | 3 | 31 | … | 34 |
| 6'-1" | 9 25/32" | 6'-1" | … | 3 | 32 | … | 35 |
| 6'-2" | 9 29/32" | 6'-2" | … | 2 | 33 | … | 35 |
| 6'-3" | 10 1/16" | 6'-3" | … | 2 | 34 | … | 36 |
| 6'-4" | 10 3/16" | 6'-4" | … | 2 | 34 | … | 36 |
| 6'-5" | 10 5/16" | 6'-5" | … | 1 | 35 | … | 36 |
| 6'-6" | 10 7/16" | 6'-6" | … | 1 | 36 | … | 37 |
| 6'-7" | 10 19/32" | 6'-7" | … | 1 | 36 | … | 37 |
| 6'-8" | 10 23/32" | 6'-8" | … | 1 | 37 | … | 38 |
| 6'-9" | 10 27/32" | 6'-9" | … | … | 38 | … | 38 |
| 7'-0" | 11¼" | 7'-0" | … | … | 38 | 1 | 39 |
| 7'-3" | 11 21/32" | 7'-3" | … | … | 38 | 3 | 41 |
| 7'-6" | 1'-0 1/16" | 7'-6" | … | … | 38 | 4 | 42 |
| 7'-9" | 1'-0 15/32" | 7'-9" | … | … | 38 | 5 | 43 |
| 8'-0" | 1'-0⅞" | 8'-0" | … | … | 38 | 6 | 44 |
| 8'-3" | 1'-1¼" | 8'-3" | … | … | 38 | 8 | 46 |
| 8'-6" | 1'-1 21/32" | 8'-6" | … | … | 38 | 9 | 47 |
| 8'-9" | 1'-2 1/16" | 8'-9" | … | … | 38 | 10 | 48 |
| 9'-0" | 1'-2 15/32" | 9'-0" | … | … | 38 | 11 | 49 |
| 9'-3" | 1'-2⅞" | 9'-3" | … | … | 38 | 13 | 51 |
| 9'-6" | 1'-3 9/32" | 9'-6" | … | … | 38 | 14 | 52 |
| 9'-9" | 1'-3 11/16" | 9'-9" | … | … | 38 | 15 | 53 |
| 10'-0" | 1'-4 3/32" | 10'-0" | … | … | 38 | 16 | 54 |
| 10'-3" | 1'-4 15/32" | 10'-3" | … | … | 38 | 18 | 56 |
| 10'-6" | 1'-4⅞" | 10'-6" | … | … | 38 | 19 | 57 |
| 10'-9" | 1'-5 9/32" | 10'-9" | … | … | 38 | 20 | 58 |
| 11'-0" | 1'-5 11/16" | 11'-0" | … | … | 38 | 21 | 59 |
| 11'-3" | 1'-6 3/32" | 11'-3" | … | … | 38 | 23 | 61 |
| 11'-6" | 1'-6½" | 11'-6" | … | … | 38 | 24 | 62 |
| 11'-9" | 1'-6⅞" | 11'-9" | … | … | 38 | 25 | 63 |
| 12'-0" | 1'-7 9/32" | 12'-0" | … | … | 38 | 26 | 64 |
| 12'-3" | 1'-7 11/16" | 12'-3" | … | … | 38 | 28 | 66 |
| 12'-6" | 1'-8 3/32" | 12'-6" | … | … | 38 | 29 | 67 |
| 12'-9" | 1'-8½" | 12'-9" | … | … | 38 | 30 | 68 |
| 13'-0" | 1'-8 29/32" | 13'-0" | … | … | 38 | 31 | 69 |
| 13'-3" | 1'-9 5/16" | 13'-3" | … | … | 38 | 33 | 71 |
| 13'-6" | 1'-9 23/32" | 13'-6" | … | … | 38 | 34 | 72 |
| 13'-9" | 1'-10⅛" | 13'-9" | … | … | 38 | 35 | 73 |
| 14'-0" | 1'-10½" | 14'-0" | … | … | 38 | 36 | 74 |

Footer: "See Page 106 For Skews". All totals check.

## Image (45).jpg — catalogue p.182–183

### p.182 — SPRUNG ARCHES — 1.608" rise per foot of span — 9-INCH ARCH THICKNESS — Central Angle=60°

9"x4½"x3", 9"x6¾"x3" or 9"x9"x3". "Brand 4160-B to be used for Skew". Columns: No. 3 Wedge 9x4½x(3-2); No. 2 Wedge 9x4½x(3-2½); No. 1 Wedge 9x4½x(3-2¾); Straights 9x4½x3.

| Span | Rise | Inside radius | No. 3 Wedge | No. 2 Wedge | No. 1 Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 1'-6" | 2 13/32" | 1'-6" | 10 | … | … | … | 10 |
| 1'-7" | 2 17/32" | 1'-7" | 9 | 1 | … | … | 10 |
| 1'-8" | 2 11/16" | 1'-8" | 9 | 2 | … | … | 11 |
| 1'-9" | 2 13/16" | 1'-9" | 9 | 2 | … | … | 11 |
| 1'-10" | 2 15/16" | 1'-10" | 8 | 3 | … | … | 11 |
| 1'-11" | 3 3/32" | 1'-11" | 8 | 4 | … | … | 12 |
| 2'-0" | 3 7/32" | 2'-0" | 8 | 4 | … | … | 12 |
| 2'-1" | 3 11/32" | 2'-1" | 7 | 5 | … | … | 12 |
| 2'-2" | 3 15/32" | 2'-2" | 7 | 6 | … | … | 13 |
| 2'-3" | 3⅝" | 2'-3" | 7 | 6 | … | … | 13 |
| 2'-4" | 3¾" | 2'-4" | 6 | 7 | … | … | 13 |
| 2'-5" | 3⅞" | 2'-5" | 6 | 8 | … | … | 14 |
| 2'-6" | 4 1/32" | 2'-6" | 5 | 9 | … | … | 14 |
| 2'-7" | 4 5/32" | 2'-7" | 5 | 9 | … | … | 14 |
| 2'-8" | 4 9/32" | 2'-8" | 5 | 10 | … | … | 15 |
| 2'-9" | 4 7/16" | 2'-9" | 4 | 11 | … | … | 15 |
| 2'-10" | 4 9/16" | 2'-10" | 4 | 11 | … | … | 15 |
| 2'-11" | 4 11/16" | 2'-11" | 4 | 12 | … | … | 16 |
| 3'-0" | 4 13/16" | 3'-0" | 3 | 13 | … | … | 16 |
| 3'-1" | 4 31/32" | 3'-1" | 3 | 13 | … | … | 16 |
| 3'-2" | 5 3/32" | 3'-2" | 3 | 14 | … | … | 17 |
| 3'-3" | 5 7/32" | 3'-3" | 2 | 15 | … | … | 17 |
| 3'-4" | 5 11/32" | 3'-4" | 2 | 15 | … | … | 17 |
| 3'-5" | 5½" | 3'-5" | 2 | 16 | … | … | 18 |
| 3'-6" | 5⅝" | 3'-6" | 1 | 17 | … | … | 18 |
| 3'-7" | 5¾" | 3'-7" | 1 | 18 | … | … | 19 |
| 3'-8" | 5 29/32" | 3'-8" | 1 | 18 | … | … | 19 |
| 3'-9" | 6 1/32" | 3'-9" | … | 19 | … | … | 19 |
| 3'-10" | 6 5/32" | 3'-10" | … | 19 | 1 | … | 20 |
| 3'-11" | 6 9/32" | 3'-11" | … | 18 | 2 | … | 20 |
| 4'-0" | 6 7/16" | 4'-0" | … | 18 | 2 | … | 20 |
| 4'-1" | 6 9/16" | 4'-1" | … | 18 | 3 | … | 21 |
| 4'-2" | 6 11/16" | 4'-2" | … | 17 | 4 | … | 21 |
| 4'-3" | 6 27/32" | 4'-3" | … | 17 | 4 | … | 21 |
| 4'-4" | 6 31/32" | 4'-4" | … | 17 | 5 | … | 22 |
| 4'-5" | 7 3/32" | 4'-5" | … | 16 | 6 | … | 22 |
| 4'-6" | 7¼" | 4'-6" | … | 16 | 6 | … | 22 |
| 4'-7" | 7⅜" | 4'-7" | … | 16 | 7 | … | 23 |
| 4'-8" | 7½" | 4'-8" | … | 15 | 8 | … | 23 |
| 4'-9" | 7⅝" | 4'-9" | … | 15 | 8 | … | 23 |
| 4'-10" | 7 25/32" | 4'-10" | … | 15 | 9 | … | 24 |
| 4'-11" | 7 29/32" | 4'-11" | … | 14 | 10 | … | 24 |
| 5'-0" | 8 1/32" | 5'-0" | … | 14 | 10 | … | 24 |
| 5'-1" | 8 3/16" | 5'-1" | … | 14 | 11 | … | 25 |
| 5'-2" | 8 5/16" | 5'-2" | … | 13 | 12 | … | 25 |
| 5'-3" | 8 7/16" | 5'-3" | … | 13 | 12 | … | 25 |
| 5'-4" | 8 9/16" | 5'-4" | … | 12 | 14 | … | 26 |

Footer: "See Page 106 For Skews"; "Continued Next Page". All totals check (total column in the gutter; read from the facing-page crop).

### p.183 — SPRUNG ARCHES — 1.608" rise per foot of span — 9-INCH ARCH THICKNESS — Central Angle=60° (continued)

Same title lines and columns as p.182.

| Span | Rise | Inside radius | No. 3 Wedge | No. 2 Wedge | No. 1 Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 5'-5" | 8 23/32" | 5'-5" | … | 12 | 14 | … | 26 |
| 5'-6" | 8 27/32" | 5'-6" | … | 12 | 15 | … | 27 |
| 5'-7" | 8 31/32" | 5'-7" | … | 11 | 16 | … | 27 |
| 5'-8" | 9⅛" | 5'-8" | … | 11 | 16 | … | 27 |
| 5'-9" | 9¼" | 5'-9" | … | 11 | 17 | … | 28 |
| 5'-10" | 9⅜" | 5'-10" | … | 10 | 18 | … | 28 |
| 5'-11" | 9½" | 5'-11" | … | 10 | 18 | … | 28 |
| 6'-0" | 9 21/32" | 6'-0" | … | 10 | 19 | … | 29 |
| 6'-1" | 9 25/32" | 6'-1" | … | 9 | 20 | … | 29 |
| 6'-2" | 9 29/32" | 6'-2" | … | 9 | 20 | … | 29 |
| 6'-3" | 10 1/16" | 6'-3" | … | 9 | 21 | … | 30 |
| 6'-4" | 10 3/16" | 6'-4" | … | 8 | 22 | … | 30 |
| 6'-5" | 10 5/16" | 6'-5" | … | 8 | 22 | … | 30 |
| 6'-6" | 10 7/16" | 6'-6" | … | 8 | 23 | … | 31 |
| 6'-7" | 10 19/32" | 6'-7" | … | 7 | 24 | … | 31 |
| 6'-8" | 10 23/32" | 6'-8" | … | 7 | 24 | … | 31 |
| 6'-9" | 10 27/32" | 6'-9" | … | 7 | 25 | … | 32 |
| 6'-10" | 11" | 6'-10" | … | 6 | 26 | … | 32 |
| 6'-11" | 11⅛" | 6'-11" | … | 6 | 26 | … | 32 |
| 7'-0" | 11¼" | 7'-0" | … | 6 | 27 | … | 33 |
| 7'-1" | 11⅜" | 7'-1" | … | 5 | 28 | … | 33 |
| 7'-2" | 11 17/32" | 7'-2" | … | 5 | 29 | … | 34 |
| 7'-3" | 11 21/32" | 7'-3" | … | 4 | 30 | … | 34 |
| 7'-4" | 11 25/32" | 7'-4" | … | 4 | 30 | … | 34 |
| 7'-5" | 11 15/16" | 7'-5" | … | 4 | 31 | … | 35 |
| 7'-6" | 1'-0 1/16" | 7'-6" | … | 3 | 32 | … | 35 |
| 7'-7" | 1'-0 3/16" | 7'-7" | … | 3 | 32 | … | 35 |
| 7'-8" | 1'-0 5/16" | 7'-8" | … | 3 | 33 | … | 36 |
| 7'-9" | 1'-0 15/32" | 7'-9" | … | 2 | 34 | … | 36 |
| 7'-10" | 1'-0 19/32" | 7'-10" | … | 2 | 34 | … | 36 |
| 7'-11" | 1'-0 23/32" | 7'-11" | … | 2 | 35 | … | 37 |
| 8'-0" | 1'-0⅞" | 8'-0" | … | 1 | 36 | … | 37 |
| 8'-1" | 1'-1" | 8'-1" | … | 1 | 36 | … | 37 |
| 8'-2" | 1'-1⅛" | 8'-2" | … | 1 | 37 | … | 38 |
| 8'-3" | 1'-1¼" | 8'-3" | … | … | 38 | … | 38 |
| 8'-6" | 1'-1 21/32" | 8'-6" | … | … | 38 | 1 | 39 |
| 9'-0" | 1'-2 15/32" | 9'-0" | … | … | 38 | 3 | 41 |
| 9'-6" | 1'-3 9/32" | 9'-6" | … | … | 38 | 5 | 43 |
| 10'-0" | 1'-4 3/32" | 10'-0" | … | … | 38 | 7 | 45 |
| 10'-6" | 1'-4⅞" | 10'-6" | … | … | 38 | 9 | 47 |
| 11'-0" | 1'-5 11/16" | 11'-0" | … | … | 38 | 12 | 50 |
| 11'-6" | 1'-6½" | 11'-6" | … | … | 38 | 14 | 52 |
| 12'-0" | 1'-7 9/32" | 12'-0" | … | … | 38 | 16 | 54 |
| 12'-6" | 1'-8 3/32" | 12'-6" | … | … | 38 | 18 | 56 |
| 13'-0" | 1'-8 29/32" | 13'-0" | … | … | 38 | 20 | 58 |
| 13'-6" | 1'-9 23/32" | 13'-6" | … | … | 38 | 22 | 60 |
| 14'-0" | 1'-10½" | 14'-0" | … | … | 38 | 24 | 62 |

Footer: "See Page 106 For Skews". All totals check.

---

## Notes common to these pages

- No edition, year, or publisher imprint is printed on p.154–183; only "Page NNN" folios. (Publisher per the catalogue title: A.P. Green.)
- Skew references: every sprung-arch page says "See Page 106 For Skews". Skew brick named per table: Standard 9-inch Featheredge (1½" rise/ft, 4½" and 9" thick); Brand 4160-A (1.608", 4½"); 4160-C (2", 4½"); Standard sideskews (2.302", 4½"); 4160-E (1½", 6"); 3 inch 60° sideskews (1.608", 6"); 4160-F (2", 6"); 3 inch 48° sideskews (2.302", 6"); 4160-B (1.608", 9").
- Rise-per-foot to central angle as printed: 1½" = 56°; 1.608" = 60° ("Radius=Span"); 2" = 74°; 2.302" = 84°. No formulas are printed on these pages.
- Total mismatches found (as printed): p.170 rows 1'-6" and 1'-10"; p.172 row 3'-10". All other totals on p.154–183 equal the row sums.

## Summary

- Ring/circle brick counts (complete circles): p.154 (13½" lining, wedge, end), p.155–156 (13½"x4½"x3" key, 13½" lining), p.157–158 (13½"x6" key, 13½" lining), p.159–160 (15" lining wedge), p.161–162 (18" lining wedge). Blast-furnace bottom blocks per course by hearth diameter: p.163.
- Arch counts by span and rise (sprung arches, per course): 4½" thick: p.164–165 (1½"/ft), p.166–167 (1.608"/ft), p.168–169 (2"/ft), p.170–171 (2.302"/ft); 6" thick: p.172 (1½"), p.173 (1.608"), p.174 (2"), p.175 (2.302"); 9" thick: p.176–179 (1½"), p.180–183 (1.608"). Each lists span, rise, inside radius, arch/wedge counts by number, straights, total.
- Dome brick: none on these pages.
- Skewbacks: no skew tables here; each page names the skew brand and points to p.106.
- Formulas: none printed; only the rise/ft to central-angle pairs above.

---


## Image (46).jpg — catalogue p.184–185

(Scan rotated 90°; two facing pages. p.184 on the left of the spread, p.185 on the right.)

### p.184

**SPRUNG ARCHES — 2" rise per foot of span**
**9-INCH ARCH THICKNESS — Central Angle=74°**
9"x4½"x2½", 9"x6¾"x2½" or 9"x9"x2½"
Brand 4160-D to be used for Skew

Brick required per course. Column brick: No. 2 Wedge 9x4½x(2½-1½); No. 1 Wedge 9x4½x(2½-1⅞); No. 1-X Wedge 9x4½x(2½-2¼); Straights 9x4½x2½. ("…" = dotted, none.)

| Span | Rise | Inside Radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 1'-6" | 3" | 1'-3" | 11 | 2 | … | … | 13 |
| 1'-7" | 3 5/32" | 1'-3 27/32" | 10 | 3 | … | … | 13 |
| 1'-8" | 3 11/32" | 1'-4 21/32" | 9 | 5 | … | … | 14 |
| 1'-9" | 3½" | 1'-5½" | 8 | 6 | … | … | 14 |
| 1'-10" | 3 21/32" | 1'-6 11/32" | 7 | 7 | … | … | 14 |
| 1'-11" | 3 27/32" | 1'-7 5/32" | 7 | 8 | … | … | 15 |
| 2'-0" | 4" | 1'-8" | 6 | 9 | … | … | 15 |
| 2'-1" | 4 5/32" | 1'-8 27/32" | 6 | 10 | … | … | 16 |
| 2'-2" | 4 11/32" | 1'-9 21/32" | 5 | 11 | … | … | 16 |
| 2'-3" | 4½" | 1'-10½" | 4 | 13 | … | … | 17 |
| 2'-4" | 4 21/32" | 1'-11 11/32" | 3 | 14 | … | … | 17 |
| 2'-5" | 4 27/32" | 2'-0 5/32" | 2 | 15 | … | … | 17 |
| 2'-6" | 5" | 2'-1" | 2 | 16 | … | … | 18 |
| 2'-7" | 5 5/32" | 2'-1 27/32" | 1 | 17 | … | … | 18 |
| 2'-8" | 5 11/32" | 2'-2 21/32" | 1 | 18 | … | … | 19 |
| 2'-9" | 5½" | 2'-3½" | … | 18 | 1 | … | 19 |
| 2'-10" | 5 21/32" | 2'-4 11/32" | … | 18 | 2 | … | 20 |
| 2'-11" | 5 27/32" | 2'-5 5/32" | … | 18 | 2 | … | 20 |
| 3'-0" | 6" | 2'-6" | … | 17 | 3 | … | 20 |
| 3'-1" | 6 5/32" | 2'-6 27/32" | … | 17 | 4 | … | 21 |
| 3'-2" | 6 11/32" | 2'-7 21/32" | … | 17 | 4 | … | 21 |
| 3'-3" | 6½" | 2'-8½" | … | 17 | 5 | … | 22 |
| 3'-4" | 6 21/32" | 2'-9 11/32" | … | 16 | 6 | … | 22 |
| 3'-5" | 6 27/32" | 2'-10 5/32" | … | 16 | 7 | … | 23 |
| 3'-6" | 7" | 2'-11" | … | 16 | 7 | … | 23 |
| 3'-7" | 7 5/32" | 2'-11 27/32" | … | 15 | 8 | … | 23 |
| 3'-8" | 7 11/32" | 3'-0 21/32" | … | 15 | 9 | … | 24 |
| 3'-9" | 7½" | 3'-1½" | … | 15 | 9 | … | 24 |
| 3'-10" | 7 21/32" | 3'-2 11/32" | … | 15 | 10 | … | 25 |
| 3'-11" | 7 27/32" | 3'-3 5/32" | … | 14 | 11 | … | 25 |
| 4'-0" | 8" | 3'-4" | … | 14 | 12 | … | 26 |
| 4'-1" | 8 5/32" | 3'-4 27/32" | … | 14 | 12 | … | 26 |
| 4'-2" | 8 11/32" | 3'-5 21/32" | … | 13 | 13 | … | 26 |
| 4'-3" | 8½" | 3'-6½" | … | 13 | 14 | … | 27 |
| 4'-4" | 8 21/32" | 3'-7 11/32" | … | 13 | 14 | … | 27 |
| 4'-5" | 8 27/32" | 3'-8 5/32" | … | 13 | 15 | … | 28 |
| 4'-6" | 9" | 3'-9" | … | 12 | 16 | … | 28 |
| 4'-7" | 9 5/32" | 3'-9 27/32" | … | 12 | 17 | … | 29 |
| 4'-8" | 9 11/32" | 3'-10 21/32" | … | 12 | 17 | … | 29 |
| 4'-9" | 9½" | 3'-11½" | … | 11 | 18 | … | 29 |
| 4'-10" | 9 21/32" | 4'-0 11/32" | … | 11 | 19 | … | 30 |
| 4'-11" | 9 27/32" | 4'-1 5/32" | … | 11 | 19 | … | 30 |
| 5'-0" | 10" | 4'-2" | … | 11 | 20 | … | 31 |
| 5'-1" | 10 5/32" | 4'-2 27/32" | … | 10 | 21 | … | 31 |
| 5'-2" | 10 11/32" | 4'-3 21/32" | … | 10 | 22 | … | 32 |
| 5'-3" | 10½" | 4'-4½" | … | 10 | 22 | … | 32 |
| 5'-4" | 10 21/32" | 4'-5 11/32" | … | 9 | 23 | … | 32 |
| 5'-5" | 10 27/32" | 4'-6 5/32" | … | 9 | 24 | … | 33 |
| 5'-6" | 11" | 4'-7" | … | 9 | 24 | … | 33 |
| 5'-7" | 11 5/32" | 4'-7 27/32" | … | 9 | 25 | … | 34 |
| 5'-8" | 11 11/32" | 4'-8 21/32" | … | 8 | 26 | … | 34 |

Totals checked against row sums: all match.

Footer: "See Page 106 For Skews" — "Continued Next Page" — "Page 184"

### p.185

**SPRUNG ARCHES — 2" rise per foot of span** (continued)
**9-INCH ARCH THICKNESS — Central Angle=74°**
9"x4½"x2½", 9"x6¾"x2½" or 9"x9"x2½"
Brand 4160-D to be used for Skew

| Span | Rise | Inside Radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 5'-9" | 11½" | 4'-9½" | … | 8 | 27 | … | 35 |
| 5'-10" | 11 21/32" | 4'-10 11/32" | … | 8 | 27 | … | 35 |
| 5'-11" | 11 27/32" | 4'-11 5/32" | … | 7 | 28 | … | 35 |
| 6'-0" | 1'-0" | 5'-0" | … | 7 | 29 | … | 36 |
| 6'-1" | 1'-0 5/32" | 5'-0 27/32" | … | 7 | 29 | … | 36 |
| 6'-2" | 1'-0 11/32" | 5'-1 21/32" | … | 7 | 30 | … | 37 |
| 6'-3" | 1'-0½" | 5'-2½" | … | 6 | 31 | … | 37 |
| 6'-4" | 1'-0 21/32" | 5'-3 11/32" | … | 6 | 32 | … | 38 |
| 6'-5" | 1'-0 27/32" | 5'-4 5/32" | … | 6 | 32 | … | 38 |
| 6'-6" | 1'-1" | 5'-5" | … | 5 | 33 | … | 38 |
| 6'-7" | 1'-1 5/32" | 5'-5 27/32" | … | 5 | 34 | … | 39 |
| 6'-8" | 1'-1 11/32" | 5'-6 21/32" | … | 5 | 34 | … | 39 |
| 6'-9" | 1'-1½" | 5'-7½" | … | 5 | 35 | … | 40 |
| 6'-10" | 1'-1 21/32" | 5'-8 11/32" | … | 4 | 36 | … | 40 |
| 6'-11" | 1'-1 27/32" | 5'-9 5/32" | … | 4 | 37 | … | 41 |
| 7'-0" | 1'-2" | 5'-10" | … | 4 | 37 | … | 41 |
| 7'-1" | 1'-2 5/32" | 5'-10 27/32" | … | 3 | 38 | … | 41 |
| 7'-2" | 1'-2 11/32" | 5'-11 21/32" | … | 3 | 39 | … | 42 |
| 7'-3" | 1'-2½" | 6'-0½" | … | 3 | 39 | … | 42 |
| 7'-4" | 1'-2 21/32" | 6'-1 11/32" | … | 3 | 40 | … | 43 |
| 7'-5" | 1'-2 27/32" | 6'-2 5/32" | … | 2 | 41 | … | 43 |
| 7'-6" | 1'-3" | 6'-3" | … | 2 | 42 | … | 44 |
| 7'-7" | 1'-3 5/32" | 6'-3 27/32" | … | 2 | 42 | … | 44 |
| 7'-8" | 1'-3 11/32" | 6'-4 21/32" | … | 1 | 43 | … | 44 |
| 7'-9" | 1'-3½" | 6'-5½" | … | 1 | 44 | … | 45 |
| 7'-10" | 1'-3 21/32" | 6'-6 11/32" | … | 1 | 44 | … | 45 |
| 7'-11" | 1'-3 27/32" | 6'-7 5/32" | … | 1 | 45 | … | 46 |
| 8'-0" | 1'-4" | 6'-8" | … | … | 46 | … | 46 |
| 8'-3" | 1'-4½" | 6'-10½" | … | … | 47 | … | 47 |
| 8'-6" | 1'-5" | 7'-1" | … | … | 47 | 2 | 49 |
| 8'-9" | 1'-5½" | 7'-3½" | … | … | 47 | 3 | 50 |
| 9'-0" | 1'-6" | 7'-6" | … | … | 47 | 4 | 51 |
| 9'-3" | 1'-6½" | 7'-8½" | … | … | 47 | 6 | 53 |
| 9'-6" | 1'-7" | 7'-11" | … | … | 47 | 7 | 54 |
| 9'-9" | 1'-7½" | 8'-1½" | … | … | 47 | 8 | 55 |
| 10'-0" | 1'-8" | 8'-4" | … | … | 47 | 9 | 56 |
| 10'-3" | 1'-8½" | 8'-6½" | … | … | 47 | 11 | 58 |
| 10'-6" | 1'-9" | 8'-9" | … | … | 47 | 12 | 59 |
| 10'-9" | 1'-9½" | 8'-11½" | … | … | 47 | 13 | 60 |
| 11'-0" | 1'-10" | 9'-2" | … | … | 47 | 15 | 62 |
| 11'-3" | 1'-10½" | 9'-4½" | … | … | 47 | 16 | 63 |
| 11'-6" | 1'-11" | 9'-7" | … | … | 47 | 17 | 64 |
| 11'-9" | 1'-11½" | 9'-9½" | … | … | 47 | 18 | 65 |
| 12'-0" | 2'-0" | 10'-0" | … | … | 47 | 20 | 67 |
| 12'-3" | 2'-0½" | 10'-2½" | … | … | 47 | 21 | 68 |
| 12'-6" | 2'-1" | 10'-5" | … | … | 47 | 22 | 69 |
| 12'-9" | 2'-1½" | 10'-7½" | … | … | 47 | 24 | 71 |
| 13'-0" | 2'-2" | 10'-10" | … | … | 47 | 25 | 72 |
| 13'-3" | 2'-2½" | 11'-0½" | … | … | 47 | 26 | 73 |
| 13'-6" | 2'-3" | 11'-3" | … | … | 47 | 27 | 74 |
| 14'-0" | 2'-4" | 11'-8" | … | … | 47 | 30 | 77 |

Totals checked against row sums: all match.

Footer: "See Page 106 For Skews" — "Page 185"


## Image (47).jpg — catalogue p.186–187

(Scan rotated 90°; two facing pages.)

### p.186

**SPRUNG ARCHES — 2" rise per foot of span**
**9-INCH ARCH THICKNESS — Central Angle=74°**
9"x4½"x3", 9"x6¾"x3" or 9"x9"x3"
Brand 4160-D to be used for Skew

Brick required per course: No. 3 Wedge 9x4½x(3-2); No. 2 Wedge 9x4½x(3-2½); No. 1 Wedge 9x4½x(3-2¾); Straights 9x4½x3.

| Span | Rise | Inside Radius | No. 3 Wedge | No. 2 Wedge | No. 1 Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 1'-10" | 3 21/32" | 1'-6 11/32" | 12 | … | … | … | 12 |
| 1'-11" | 3 27/32" | 1'-7 5/32" | 11 | 1 | … | … | 12 |
| 2'-0" | 4" | 1'-8" | 11 | 2 | … | … | 13 |
| 2'-1" | 4 5/32" | 1'-8 27/32" | 10 | 3 | … | … | 13 |
| 2'-2" | 4 11/32" | 1'-9 21/32" | 10 | 4 | … | … | 14 |
| 2'-3" | 4½" | 1'-10½" | 10 | 4 | … | … | 14 |
| 2'-4" | 4 21/32" | 1'-11 11/32" | 9 | 5 | … | … | 14 |
| 2'-5" | 4 27/32" | 2'-0 5/32" | 9 | 6 | … | … | 15 |
| 2'-6" | 5" | 2'-1" | 9 | 6 | … | … | 15 |
| 2'-7" | 5 5/32" | 2'-1 27/32" | 8 | 7 | … | … | 15 |
| 2'-8" | 5 11/32" | 2'-2 21/32" | 8 | 8 | … | … | 16 |
| 2'-9" | 5½" | 2'-3½" | 8 | 8 | … | … | 16 |
| 2'-10" | 5 21/32" | 2'-4 11/32" | 7 | 9 | … | … | 16 |
| 2'-11" | 5 27/32" | 2'-5 5/32" | 7 | 10 | … | … | 17 |
| 3'-0" | 6" | 2'-6" | 7 | 10 | … | … | 17 |
| 3'-1" | 6 5/32" | 2'-6 27/32" | 6 | 11 | … | … | 17 |
| 3'-2" | 6 11/32" | 2'-7 21/32" | 6 | 12 | … | … | 18 |
| 3'-3" | 6½" | 2'-8½" | 5 | 13 | … | … | 18 |
| 3'-4" | 6 21/32" | 2'-9 11/32" | 5 | 14 | … | … | 19 |
| 3'-5" | 6 27/32" | 2'-10 5/32" | 5 | 14 | … | … | 19 |
| 3'-6" | 7" | 2'-11" | 4 | 15 | … | … | 19 |
| 3'-7" | 7 5/32" | 2'-11 27/32" | 4 | 16 | … | … | 20 |
| 3'-8" | 7 11/32" | 3'-0 21/32" | 4 | 16 | … | … | 20 |
| 3'-9" | 7½" | 3'-1½" | 3 | 17 | … | … | 20 |
| 3'-10" | 7 21/32" | 3'-2 11/32" | 3 | 18 | … | … | 21 |
| 3'-11" | 7 27/32" | 3'-3 5/32" | 3 | 18 | … | … | 21 |
| 4'-0" | 8" | 3'-4" | 2 | 19 | … | … | 21 |
| 4'-1" | 8 5/32" | 3'-4 27/32" | 2 | 20 | … | … | 22 |
| 4'-2" | 8 11/32" | 3'-5 21/32" | 2 | 20 | … | … | 22 |
| 4'-3" | 8½" | 3'-6½" | 1 | 21 | … | … | 22 |
| 4'-4" | 8 21/32" | 3'-7 11/32" | 1 | 22 | … | … | 23 |
| 4'-5" | 8 27/32" | 3'-8 5/32" | … | 23 | … | … | 23 |
| 4'-6" | 9" | 3'-9" | … | 24 | … | … | 24 |
| 4'-7" | 9 5/32" | 3'-9 27/32" | … | 23 | 1 | … | 24 |
| 4'-8" | 9 11/32" | 3'-10 21/32" | … | 23 | 1 | … | 24 |
| 4'-9" | 9½" | 3'-11½" | … | 22 | 3 | … | 25 |
| 4'-10" | 9 21/32" | 4'-0 11/32" | … | 22 | 3 | … | 25 |
| 4'-11" | 9 27/32" | 4'-1 5/32" | … | 21 | 4 | … | 25 |
| 5'-0" | 10" | 4'-2" | … | 21 | 5 | … | 26 |
| 5'-1" | 10 5/32" | 4'-2 27/32" | … | 21 | 5 | … | 26 |
| 5'-2" | 10 11/32" | 4'-3 21/32" | … | 20 | 6 | … | 26 |
| 5'-3" | 10½" | 4'-4½" | … | 20 | 7 | … | 27 |
| 5'-4" | 10 21/32" | 4'-5 11/32" | … | 20 | 7 | … | 27 |
| 5'-5" | 10 27/32" | 4'-6 5/32" | … | 19 | 8 | … | 27 |
| 5'-6" | 11" | 4'-7" | … | 19 | 9 | … | 28 |
| 5'-7" | 11 5/32" | 4'-7 27/32" | … | 19 | 9 | … | 28 |

Totals checked against row sums: all match.

Footer: "See Page 106 For Skews" — "Continued Next Page" — "Page 186"

### p.187

**SPRUNG ARCHES — 2" rise per foot of span** (continued)
**9-INCH ARCH THICKNESS — Central Angle=74°**
9"x4½"x3", 9"x6¾"x3" or 9"x9"x3"
Brand 4160-D to be used for Skew

| Span | Rise | Inside Radius | No. 3 Wedge | No. 2 Wedge | No. 1 Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 5'-8" | 11 11/32" | 4'-8 21/32" | … | 18 | 10 | … | 28 |
| 5'-9" | 11½" | 4'-9½" | … | 18 | 11 | … | 29 |
| 5'-10" | 11 21/32" | 4'-10 11/32" | … | 18 | 11 | … | 29 |
| 5'-11" | 11 27/32" | 4'-11 5/32" | … | 17 | 13 | … | 30 |
| 6'-0" | 1'-0" | 5'-0" | … | 17 | 13 | … | 30 |
| 6'-1" | 1'-0 5/32" | 5'-0 27/32" | … | 16 | 14 | … | 30 |
| 6'-2" | 1'-0 11/32" | 5'-1 21/32" | … | 16 | 15 | … | 31 |
| 6'-3" | 1'-0½" | 5'-2½" | … | 16 | 15 | … | 31 |
| 6'-4" | 1'-0 21/32" | 5'-3 11/32" | … | 15 | 16 | … | 31 |
| 6'-5" | 1'-0 27/32" | 5'-4 5/32" | … | 15 | 17 | … | 32 |
| 6'-6" | 1'-1" | 5'-5" | … | 15 | 17 | … | 32 |
| 6'-7" | 1'-1 5/32" | 5'-5 27/32" | … | 14 | 18 | … | 32 |
| 6'-8" | 1'-1 11/32" | 5'-6 21/32" | … | 14 | 19 | … | 33 |
| 6'-9" | 1'-1½" | 5'-7½" | … | 14 | 19 | … | 33 |
| 6'-10" | 1'-1 21/32" | 5'-8 11/32" | … | 13 | 20 | … | 33 |
| 6'-11" | 1'-1 27/32" | 5'-9 5/32" | … | 13 | 21 | … | 34 |
| 7'-0" | 1'-2" | 5'-10" | … | 13 | 21 | … | 34 |
| 7'-1" | 1'-2 5/32" | 5'-10 27/32" | … | 12 | 23 | … | 35 |
| 7'-2" | 1'-2 11/32" | 5'-11 21/32" | … | 12 | 23 | … | 35 |
| 7'-3" | 1'-2½" | 6'-0½" | … | 11 | 24 | … | 35 |
| 7'-4" | 1'-2 21/32" | 6'-1 11/32" | … | 11 | 25 | … | 36 |
| 7'-5" | 1'-2 27/32" | 6'-2 5/32" | … | 11 | 25 | … | 36 |
| 7'-6" | 1'-3" | 6'-3" | … | 10 | 26 | … | 36 |
| 7'-7" | 1'-3 5/32" | 6'-3 27/32" | … | 10 | 27 | … | 37 |
| 7'-8" | 1'-3 11/32" | 6'-4 21/32" | … | 10 | 27 | … | 37 |
| 7'-9" | 1'-3½" | 6'-5½" | … | 9 | 28 | … | 37 |
| 7'-10" | 1'-3 21/32" | 6'-6 11/32" | … | 9 | 29 | … | 38 |
| 7'-11" | 1'-3 27/32" | 6'-7 5/32" | … | 9 | 29 | … | 38 |
| 8'-0" | 1'-4" | 6'-8" | … | 8 | 30 | … | 38 |
| 8'-1" | 1'-4 5/32" | 6'-8 27/32" | … | 8 | 31 | … | 39 |
| 8'-2" | 1'-4 11/32" | 6'-9 21/32" | … | 7 | 32 | … | 39 |
| 8'-3" | 1'-4½" | 6'-10½" | … | 7 | 33 | … | 40 |
| 8'-6" | 1'-5" | 7'-1" | … | 6 | 35 | … | 41 |
| 8'-9" | 1'-5½" | 7'-3½" | … | 5 | 37 | … | 42 |
| 9'-0" | 1'-6" | 7'-6" | … | 4 | 39 | … | 43 |
| 9'-3" | 1'-6½" | 7'-8½" | … | 3 | 41 | … | 44 |
| 9'-6" | 1'-7" | 7'-11" | … | 2 | 43 | … | 45 |
| 9'-9" | 1'-7½" | 8'-1½" | … | 1 | 45 | … | 46 |
| 10'-0" | 1'-8" | 8'-4" | … | … | 47 | … | 47 |
| 10'-6" | 1'-9" | 8'-9" | … | … | 47 | 2 | 49 |
| 11'-0" | 1'-10" | 9'-2" | … | … | 47 | 4 | 51 |
| 11'-6" | 1'-11" | 9'-7" | … | … | 47 | 7 | 54 |
| 12'-0" | 2'-0" | 10'-0" | … | … | 47 | 9 | 56 |
| 12'-6" | 2'-1" | 10'-5" | … | … | 47 | 11 | 58 |
| 13'-0" | 2'-2" | 10'-10" | … | … | 47 | 13 | 60 |
| 13'-6" | 2'-3" | 11'-3" | … | … | 47 | 15 | 62 |
| 14'-0" | 2'-4" | 11'-8" | … | … | 47 | 17 | 64 |

Totals checked against row sums: all match.

Footer: "See Page 106 For Skews" — "Page 187"


## Image (48).jpg — catalogue p.188–189

(Scan rotated 90°; two facing pages. Fractions in the Rise and Inside Radius columns are small print; read at 0.78x scale.)

### p.188

**SPRUNG ARCHES — 2.302" rise per foot of span**
**9-INCH ARCH THICKNESS — Central Angle=84°**
9"x4½"x2½", 9"x6¾"x2½" or 9"x9"x2½"
Standard sideskews to be used for Skew

Brick required per course: No. 2 Wedge 9x4½x(2½-1½); No. 1 Wedge 9x4½x(2½-1⅞); No. 1-X Wedge 9x4½x(2½-2¼); Straights 9x4½x2½.

| Span | Rise | Inside Radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 1'-6" | 3 15/32" | 1'-1 15/32" | 14 | … | … | … | 14 |
| 1'-7" | 3 21/32" | 1'-2 3/16" | 13 | 1 | … | … | 14 |
| 1'-8" | 3 27/32" | 1'-2 15/16" | 12 | 2 | … | … | 14 |
| 1'-9" | 4 1/32" | 1'-3 11/16" | 11 | 4 | … | … | 15 |
| 1'-10" | 4 7/32" | 1'-4 7/16" | 10 | 5 | … | … | 15 |
| 1'-11" | 4 13/32" | 1'-5 3/16" | 10 | 6 | … | … | 16 |
| 2'-0" | 4 19/32" | 1'-5 15/16" | 9 | 7 | … | … | 16 |
| 2'-1" | 4 25/32" | 1'-6 11/16" | 9 | 8 | … | … | 17 |
| 2'-2" | 5" | 1'-7 7/16" | 8 | 9 | … | … | 17 |
| 2'-3" | 5 3/16" | 1'-8 3/16" | 7 | 10 | … | … | 17 |
| 2'-4" | 5 3/8" | 1'-8 15/16" | 6 | 12 | … | … | 18 |
| 2'-5" | 5 9/16" | 1'-9 11/16" | 5 | 13 | … | … | 18 |
| 2'-6" | 5 3/4" | 1'-10 7/16" | 5 | 14 | … | … | 19 |
| 2'-7" | 5 15/16" | 1'-11 5/32" | 4 | 15 | … | … | 19 |
| 2'-8" | 6 1/8" | 1'-11 29/32" | 3 | 17 | … | … | 20 |
| 2'-9" | 6 11/32" | 2'-0 21/32" | 2 | 18 | … | … | 20 |
| 2'-10" | 6 17/32" | 2'-1 13/32" | 2 | 19 | … | … | 21 |
| 2'-11" | 6 23/32" | 2'-2 5/32" | 1 | 20 | … | … | 21 |
| 3'-0" | 6 29/32" | 2'-2 29/32" | … | 21 | … | … | 21 |
| 3'-1" | 7 3/32" | 2'-3 21/32" | … | 21 | 1 | … | 22 |
| 3'-2" | 7 9/32" | 2'-4 13/32" | … | 21 | 1 | … | 22 |
| 3'-3" | 7 15/32" | 2'-5 5/32" | … | 21 | 2 | … | 23 |
| 3'-4" | 7 11/16" | 2'-5 29/32" | … | 20 | 3 | … | 23 |
| 3'-5" | 7 7/8" | 2'-6 21/32" | … | 20 | 4 | … | 24 |
| 3'-6" | 8 1/16" | 2'-7 13/32" | … | 20 | 4 | … | 24 |
| 3'-7" | 8 1/4" | 2'-8 1/8" | … | 19 | 5 | … | 24 |
| 3'-8" | 8 7/16" | 2'-8 7/8" | … | 19 | 6 | … | 25 |
| 3'-9" | 8 5/8" | 2'-9 5/8" | … | 19 | 6 | … | 25 |
| 3'-10" | 8 13/16" | 2'-10 3/8" | … | 18 | 8 | … | 26 |
| 3'-11" | 9 1/32" | 2'-11 1/8" | … | 18 | 8 | … | 26 |
| 4'-0" | 9 7/32" | 2'-11 7/8" | … | 18 | 9 | … | 27 |
| 4'-1" | 9 13/32" | 3'-0 5/8" | … | 17 | 10 | … | 27 |
| 4'-2" | 9 19/32" | 3'-1 3/8" | … | 17 | 11 | … | 28 |
| 4'-3" | 9 25/32" | 3'-2 1/8" | … | 17 | 11 | … | 28 |
| 4'-4" | 9 31/32" | 3'-2 7/8" | … | 16 | 12 | … | 28 |
| 4'-5" | 10 5/32" | 3'-3 5/8" | … | 16 | 13 | … | 29 |
| 4'-6" | 10 3/8" | 3'-4 3/8" | … | 16 | 13 | … | 29 |
| 4'-7" | 10 9/16" | 3'-5 5/32" | … | 16 | 14 | … | 30 |
| 4'-8" | 10 3/4" | 3'-5 27/32" | … | 15 | 15 | … | 30 |
| 4'-9" | 10 15/16" | 3'-6 19/32" | … | 15 | 16 | … | 31 |
| 4'-10" | 11 1/8" | 3'-7 11/32" | … | 15 | 16 | … | 31 |
| 4'-11" | 11 5/16" | 3'-8 3/32" | … | 15 [?read: 15] | 17 | … | 31 |
| 5'-0" | 11½" | 3'-8 27/32" | … | 14 | 18 | … | 32 |
| 5'-1" | 11 23/32" | 3'-9 19/32" | … | 14 | 18 | … | 32 |
| 5'-2" | 11 29/32" | 3'-10 11/32" | … | 14 | 19 | … | 33 |
| 5'-3" | 1'-0 3/32" | 3'-11 3/32" | … | 13 | 20 | … | 33 |

Totals check: every row matches except 4'-11": No. 1 15 + No. 1-X 17 = 32, printed total 31 (either a misprint in the catalogue or my read of the No. 1 cell; four 15s are visible in the No. 1 column for 4'-8" to 4'-11").

Footer: "See Page 106 For Skews" — "Continued Next Page" — "Page 188"

### p.189

**SPRUNG ARCHES — 2.302" rise per foot of span** (continued)
**9-INCH ARCH THICKNESS — Central Angle=84°**
9"x4½"x2½", 9"x6¾"x2½" or 9"x9"x2½"
Standard sideskews to be used for Skew

| Span | Rise | Inside Radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 5'-4" | 1'-0 9/32" | 3'-11 27/32" | … | 13 | 21 | … | 34 |
| 5'-5" | 1'-0 15/32" | 4'-0 19/32" | … | 13 | 21 | … | 34 |
| 5'-6" | 1'-0 21/32" | 4'-1 11/32" | … | 13 | 22 | … | 35 |
| 5'-7" | 1'-0 27/32" | 4'-2 1/16" | … | 12 | 23 | … | 35 |
| 5'-8" | 1'-1 1/16" | 4'-2 13/16" | … | 12 | 23 | … | 35 |
| 5'-9" | 1'-1 1/4" | 4'-3 9/16" | … | 12 | 24 | … | 36 |
| 5'-10" | 1'-1 7/16" | 4'-4 5/16" | … | 11 | 25 | … | 36 |
| 5'-11" | 1'-1 5/8" | 4'-5 1/16" | … | 11 | 26 | … | 37 |
| 6'-0" | 1'-1 13/16" | 4'-5 13/16" | … | 11 | 26 | … | 37 |
| 6'-1" | 1'-2" | 4'-6 9/16" | … | 11 | 27 | … | 38 |
| 6'-2" | 1'-2 3/16" | 4'-7 5/16" | … | 10 | 28 | … | 38 |
| 6'-3" | 1'-2 3/8" | 4'-8 1/16" | … | 10 | 28 | … | 38 |
| 6'-4" | 1'-2 19/32" | 4'-8 13/16" | … | 10 | 29 | … | 39 |
| 6'-5" | 1'-2 25/32" | 4'-9 9/16" | … | 9 | 30 | … | 39 |
| 6'-6" | 1'-2 31/32" | 4'-10 5/16" | … | 9 | 31 | … | 40 |
| 6'-7" | 1'-3 5/32" | 4'-11 1/32" | … | 9 | 31 | … | 40 |
| 6'-8" | 1'-3 11/32" | 4'-11 25/32" | … | 9 | 32 | … | 41 |
| 6'-9" | 1'-3 17/32" | 5'-0 17/32" | … | 8 | 33 | … | 41 |
| 6'-10" | 1'-3 23/32" | 5'-1 9/32" | … | 8 | 34 | … | 42 |
| 6'-11" | 1'-3 15/16" | 5'-2 1/32" | … | 8 | 34 | … | 42 |
| 7'-0" | 1'-4 1/8" | 5'-2 25/32" | … | 7 | 35 | … | 42 |
| 7'-1" | 1'-4 5/16" | 5'-3 17/32" | … | 7 | 36 | … | 43 |
| 7'-2" | 1'-4 1/2" | 5'-4 9/32" | … | 7 | 36 | … | 43 |
| 7'-3" | 1'-4 11/16" | 5'-5 1/32" | … | 7 | 37 | … | 44 |
| 7'-4" | 1'-4 7/8" | 5'-5 25/32" | … | 6 | 38 | … | 44 |
| 7'-5" | 1'-5 1/16" | 5'-6 17/32" | … | 6 | 39 | … | 45 |
| 7'-6" | 1'-5 9/32" | 5'-7 9/32" | … | 5 | 40 | … | 45 |
| 7'-7" | 1'-5 15/32" | 5'-8 1/32" | … | 5 | 40 | … | 45 |
| 7'-8" | 1'-5 21/32" | 5'-8 3/4" | … | 5 | 41 | … | 46 |
| 7'-9" | 1'-5 27/32" | 5'-9 1/2" | … | 4 | 42 | … | 46 |
| 7'-10" | 1'-6 1/32" | 5'-10 1/4" | … | 4 | 43 | … | 47 |
| 7'-11" | 1'-6 7/32" | 5'-11" | … | 4 | 43 | … | 47 |
| 8'-0" | 1'-6 13/32" | 5'-11 3/4" | … | 4 | 44 | … | 48 |
| 8'-3" | 1'-7" | 6'-2" | … | 3 | 46 | … | 49 |
| 8'-6" | 1'-7 9/16" | 6'-4 1/4" | … | 2 | 48 | … | 50 |
| 8'-9" | 1'-8 5/32" | 6'-6 15/32" | … | 1 | 51 | … | 52 |
| 9'-0" | 1'-8 23/32" | 6'-8 23/32" | … | … | 53 | … | 53 |
| 9'-6" | 1'-9 7/8" | 7'-1 7/32" | … | … | 53 | 3 | 56 |
| 10'-0" | 1'-11 11/32" | 7'-5 11/16" | … | … | 53 | 5 | 58 |
| 10'-6" | 2'-0 3/16" | 7'-10 3/16" | … | … | 53 | 8 | 61 |
| 11'-0" | 2'-1 5/16" | 8'-2 21/32" | … | … | 53 | 10 | 63 |
| 11'-6" | 2'-2 15/32" | 8'-7 5/32" | … | … | 53 | 13 | 66 |
| 12'-0" | 2'-3 5/8" | 8'-11 5/8" | … | … | 53 | 16 | 69 |
| 12'-6" | 2'-4 25/32" | 9'-4 1/8" | … | … | 53 | 18 | 71 |
| 13'-0" | 2'-5 15/16" | 9'-8 19/32" | … | … | 53 | 21 | 74 |
| 13'-6" | 2'-7 1/16" | 10'-1 3/32" | … | … | 53 | 24 | 77 |
| 14'-0" | 2'-8 7/32" | 10'-5 9/16" | … | … | 53 | 26 | 79 |

Totals checked against row sums: all match.

Footer: "See Page 106 For Skews" — "Page 189"


## Image (49).jpg — catalogue p.190–191

(Scan rotated 90°; two facing pages.)

### p.190

**SPRUNG ARCHES — 2.302" rise per foot of span**
**9-INCH ARCH THICKNESS — Central Angle=84°**
9"x4½"x3", 9"x6¾"x3" or 9"x9"x3"
Standard sideskews to be used for Skew

Brick required per course: No. 3 Wedge 9x4½x(3-2); No. 2 Wedge 9x4½x(3-2½); No. 1 Wedge 9x4½x(3-2¾); Straights 9x4½x3.

| Span | Rise | Inside Radius | No. 3 Wedge | No. 2 Wedge | No. 1 Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 2'-0" | 4 19/32" | 1'-5 15/16" | 14 | … | … | … | 14 |
| 2'-1" | 4 25/32" | 1'-6 11/16" | 13 | 1 | … | … | 14 |
| 2'-2" | 5" | 1'-7 7/16" | 13 | 1 | … | … | 14 |
| 2'-3" | 5 3/16" | 1'-8 3/16" | 12 | 3 | … | … | 15 |
| 2'-4" | 5 3/8" | 1'-8 15/16" | 12 | 3 | … | … | 15 |
| 2'-5" | 5 9/16" | 1'-9 11/16" | 11 | 4 | … | … | 15 |
| 2'-6" | 5 3/4" | 1'-10 7/16" | 11 | 5 | … | … | 16 |
| 2'-7" | 5 15/16" | 1'-11 5/32" | 11 | 5 | … | … | 16 |
| 2'-8" | 6 1/8" | 1'-11 29/32" | 10 | 6 | … | … | 16 |
| 2'-9" | 6 11/32" | 2'-0 21/32" | 10 | 7 | … | … | 17 |
| 2'-10" | 6 17/32" | 2'-1 13/32" | 10 | 7 | … | … | 17 |
| 2'-11" | 6 23/32" | 2'-2 5/32" | 10 | 8 | … | … | 18 |
| 3'-0" | 6 29/32" | 2'-2 29/32" | 9 | 9 | … | … | 18 |
| 3'-1" | 7 3/32" | 2'-3 21/32" | 9 | 9 | … | … | 18 |
| 3'-2" | 7 9/32" | 2'-4 13/32" | 8 | 11 | … | … | 19 |
| 3'-3" | 7 15/32" | 2'-5 5/32" | 8 | 11 | … | … | 19 |
| 3'-4" | 7 11/16" | 2'-5 29/32" | 7 | 12 | … | … | 19 |
| 3'-5" | 7 7/8" | 2'-6 21/32" | 7 | 13 | … | … | 20 |
| 3'-6" | 8 1/16" | 2'-7 13/32" | 7 | 13 | … | … | 20 |
| 3'-7" | 8 1/4" | 2'-8 1/8" | 6 | 14 | … | … | 20 |
| 3'-8" | 8 7/16" | 2'-8 7/8" | 6 | 15 | … | … | 21 |
| 3'-9" | 8 5/8" | 2'-9 5/8" | 6 | 15 | … | … | 21 |
| 3'-10" | 8 13/16" | 2'-10 3/8" | 6 | 16 | … | … | 22 |
| 3'-11" | 9 1/32" | 2'-11 1/8" | 5 | 17 | … | … | 22 |
| 4'-0" | 9 7/32" | 2'-11 7/8" | 4 | 18 | … | … | 22 |
| 4'-1" | 9 13/32" | 3'-0 5/8" | 4 | 19 | … | … | 23 |
| 4'-2" | 9 19/32" | 3'-1 3/8" | 4 | 19 | … | … | 23 |
| 4'-3" | 9 25/32" | 3'-2 1/8" | 3 | 20 | … | … | 23 |
| 4'-4" | 9 31/32" | 3'-2 7/8" | 3 | 21 | … | … | 24 |
| 4'-5" | 10 5/32" | 3'-3 5/8" | 3 | 21 | … | … | 24 |
| 4'-6" | 10 3/8" | 3'-4 3/8" | 2 | 22 | … | … | 24 |
| 4'-7" | 10 9/16" | 3'-5 5/32" | 2 | 23 | … | … | 25 |
| 4'-8" | 10 3/4" | 3'-5 27/32" | 2 | 23 | … | … | 25 |
| 4'-9" | 10 15/16" | 3'-6 19/32" | 2 | 24 | … | … | 26 |
| 4'-10" | 11 1/8" | 3'-7 11/32" | 1 | 25 | … | … | 26 |
| 4'-11" | 11 15/16" [?read: 11 5/16"] | 3'-8 3/32" | … | 26 | … | … | 26 |
| 5'-0" | 11½" | 3'-8 27/32" | … | 27 | … | … | 27 |
| 5'-1" | 11 23/32" | 3'-9 19/32" | … | 26 | 1 | … | 27 |
| 5'-2" | 11 29/32" | 3'-10 11/32" | … | 26 | 1 | … | 27 |
| 5'-3" | 1'-0 3/32" | 3'-11 3/32" | … | 26 | 2 | … | 28 |
| 5'-4" | 1'-0 9/32" | 3'-11 27/32" | … | 25 | 3 | … | 28 |
| 5'-5" | 1'-0 15/32" | 4'-0 19/32" | … | 25 | 3 | … | 28 |
| 5'-6" | 1'-0 21/32" | 4'-1 11/32" | … | 25 | 4 | … | 29 |
| 5'-7" | 1'-0 27/32" | 4'-2 1/16" | … | 24 | 5 | … | 29 |
| 5'-8" | 1'-1 1/16" | 4'-2 13/16" | … | 24 | 6 | … | 30 |

Totals checked against row sums: all match.
Note: the 4'-11" rise looks like "11 15/16"" on this page, which breaks the sequence (p.188 prints 11 5/16" for the same span); treat as doubtful.

Footer: "See Page 106 For Skews" — "Continued Next Page" — "Page 190"

### p.191

**SPRUNG ARCHES — 2.302" rise per foot of span** (continued)
**9-INCH ARCH THICKNESS — Central Angle=84°**
9"x4½"x3", 9"x6¾"x3" or 9"x9"x3"
Standard sideskews to be used for Skew

| Span | Rise | Inside Radius | No. 3 Wedge | No. 2 Wedge | No. 1 Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 5'-9" | 1'-1 1/4" | 4'-3 9/16" | … | 23 | 7 | … | 30 |
| 5'-10" | 1'-1 7/16" | 4'-4 5/16" | … | 23 | 7 | … | 30 |
| 5'-11" | 1'-1 5/8" | 4'-5 1/16" | … | 23 | 8 | … | 31 |
| 6'-0" | 1'-1 13/16" | 4'-5 13/16" | … | 22 | 9 | … | 31 |
| 6'-1" | 1'-2" | 4'-6 9/16" | … | 22 | 9 | … | 31 |
| 6'-2" | 1'-2 3/16" | 4'-7 5/16" | … | 22 | 10 | … | 32 |
| 6'-3" | 1'-2 3/8" | 4'-8 1/16" | … | 21 | 11 | … | 32 |
| 6'-4" | 1'-2 19/32" | 4'-8 13/16" | … | 21 | 11 | … | 32 |
| 6'-5" | 1'-2 25/32" | 4'-9 9/16" | … | 20 | 13 | … | 33 |
| 6'-6" | 1'-2 31/32" | 4'-10 5/16" | … | 20 | 13 | … | 33 |
| 6'-7" | 1'-3 5/32" | 4'-11 1/32" | … | 20 | 14 | … | 34 |
| 6'-8" | 1'-3 11/32" | 4'-11 25/32" | … | 19 | 15 | … | 34 |
| 6'-9" | 1'-3 17/32" | 5'-0 17/32" | … | 19 | 15 | … | 34 |
| 6'-10" | 1'-3 23/32" | 5'-1 9/32" | … | 19 | 16 | … | 35 |
| 6'-11" | 1'-3 15/16" | 5'-2 1/32" | … | 18 | 17 | … | 35 |
| 7'-0" | 1'-4 1/8" | 5'-2 25/32" | … | 18 | 17 | … | 35 |
| 7'-1" | 1'-4 5/16" | 5'-3 17/32" | … | 18 | 18 | … | 36 |
| 7'-2" | 1'-4 1/2" | 5'-4 9/32" | … | 17 | 19 | … | 36 |
| 7'-3" | 1'-4 11/16" | 5'-5 1/32" | … | 17 | 19 | … | 36 |
| 7'-4" | 1'-4 7/8" | 5'-5 25/32" | … | 16 | 21 | … | 37 |
| 7'-5" | 1'-5 1/16" | 5'-6 17/32" | … | 16 | 21 | … | 37 |
| 7'-6" | 1'-5 9/32" | 5'-7 9/32" | … | 16 | 22 | … | 38 |
| 7'-7" | 1'-5 15/32" | 5'-8 1/32" | … | 15 | 23 | … | 38 |
| 7'-8" | 1'-5 21/32" | 5'-8 3/4" | … | 15 | 23 | … | 38 |
| 7'-9" | 1'-5 27/32" | 5'-9 1/2" | … | 15 | 24 | … | 39 |
| 7'-10" | 1'-6 1/32" | 5'-10 1/4" | … | 14 | 25 | … | 39 |
| 7'-11" | 1'-6 7/32" | 5'-11" | … | 14 | 25 | … | 39 |
| 8'-0" | 1'-6 13/32" | 5'-11 3/4" | … | 14 | 26 | … | 40 |
| 8'-3" | 1'-7" | 6'-2" | … | 12 | 29 | … | 41 |
| 8'-6" | 1'-7 9/16" | 6'-4 1/4" | … | 11 | 31 | … | 42 |
| 8'-9" | 1'-8 5/32" | 6'-6 15/32" | … | 10 | 33 | … | 43 |
| 9'-0" | 1'-8 23/32" | 6'-8 23/32" | … | 9 | 35 | … | 44 |
| 9'-3" | 1'-9 9/32" | 6'-10 31/32" | … | 8 | 37 | … | 45 |
| 9'-6" | 1'-9 7/8" | 7'-1 7/32" | … | 7 | 39 | … | 46 |
| 9'-9" | 1'-10 7/16" | 7'-3 7/16" | … | 6 | 41 | … | 47 |
| 10'-0" | 1'-11 11/32" | 7'-5 11/16" | … | 5 | 44 | … | 49 |
| 10'-3" | 1'-11 19/32" | 7'-7 15/16" | … | 4 | 46 | … | 50 |
| 10'-6" | 2'-0 3/16" | 7'-10 3/16" | … | 3 | 48 | … | 51 |
| 10'-9" | 2'-0 3/4" | 8'-0 13/32" | … | 2 | 50 | … | 52 |
| 11'-0" | 2'-1 5/16" | 8'-2 21/32" | … | … | 53 | … | 53 |
| 11'-6" | 2'-2 15/32" | 8'-7 5/32" | … | … | 53 | 2 | 55 |
| 12'-0" | 2'-3 5/8" | 8'-11 5/8" | … | … | 53 | 4 | 57 |
| 12'-6" | 2'-4 25/32" | 9'-4 1/8" | … | … | 53 | 6 | 59 |
| 13'-0" | 2'-5 15/16" | 9'-8 19/32" | … | … | 53 | 9 | 62 |
| 13'-6" | 2'-7 1/16" | 10'-1 3/32" | … | … | 53 | 11 | 64 |
| 14'-0" | 2'-8 7/32" | 10'-5 9/16" | … | … | 53 | 13 | 66 |

Totals checked against row sums: all match. (Rise 10'-0" printed "1'-11 11/32"" and 10'-3" "1'-11 19/32"" as read; the step between them is irregular, so treat both as [?read].)

Footer: "See Page 106 For Skews" — "Page 191"


## Image (50).jpg — catalogue p.192–193

(Scan rotated 90°; two facing pages.)

### p.192

**SPRUNG ARCHES — 1.608" rise per foot of span**
**12-INCH ARCH THICKNESS — Central Angle=60°**
12"x4½"x3", 12"x6"x3" or 12"x9"x3"
Brand 3878-B to be used for Skew

Brick required per course: No. 2 Wedge 12x6x(3-2½); No. 1 Wedge 12x6x(3-2¾); No. 1-X Wedge 12x6x(3-2⅞); Straights 12x6x3.

| Span | Rise | Inside Radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 6'-0" | 9 21/32" | 6'-0" | 21 | 9 | … | … | 30 |
| 6'-3" | 10 1/16" | 6'-3" | 20 | 11 | … | … | 31 |
| 6'-6" | 10 7/16" | 6'-6" | 19 | 13 | … | … | 32 |
| 6'-9" | 10 27/32" | 6'-9" | 18 | 15 | … | … | 33 |
| 7'-0" | 11¼" | 7'-0" | 17 | 17 | … | … | 34 |
| 7'-3" | 11 21/32" | 7'-3" | 16 | 19 | … | … | 35 |
| 7'-6" | 1'-0 1/16" | 7'-6" | 15 | 21 | … | … | 36 |
| 7'-9" | 1'-0 15/32" | 7'-9" | 14 | 23 | … | … | 37 |
| 8'-0" | 1'-0 7/8" | 8'-0" | 13 | 25 | … | … | 38 |
| 8'-3" | 1'-1¼" | 8'-3" | 12 | 27 | … | … | 39 |
| 8'-6" | 1'-1 21/32" | 8'-6" | 11 | 29 | … | … | 40 |
| 8'-9" | 1'-2 1/16" | 8'-9" | 10 | 31 | … | … | 41 |
| 9'-0" | 1'-2 15/32" | 9'-0" | 8 | 34 | … | … | 42 |
| 9'-3" | 1'-2 7/8" | 9'-3" | 7 | 36 | … | … | 43 |
| 9'-6" | 1'-3 9/32" | 9'-6" | 6 | 38 | … | … | 44 |
| 9'-9" | 1'-3 11/16" | 9'-9" | 5 | 40 | … | … | 45 |
| 10'-0" | 1'-4 1/16" | 10'-0" | 4 | 42 | … | … | 46 |
| 10'-3" | 1'-4 15/32" | 10'-3" | 3 | 44 | … | … | 47 |
| 10'-6" | 1'-4 7/8" | 10'-6" | 2 | 46 | … | … | 48 |
| 10'-9" | 1'-5 9/32" | 10'-9" | 1 | 49 | … | … | 50 |
| 11'-0" | 1'-5 11/16" | 11'-0" | … | 51 | … | … | 51 |
| 11'-3" | 1'-6 3/32" | 11'-3" | … | 50 | 2 | … | 52 |
| 11'-6" | 1'-6½" | 11'-6" | … | 48 | 5 | … | 53 |
| 11'-9" | 1'-6 7/8" | 11'-9" | … | 47 | 7 | … | 54 |
| 12'-0" | 1'-7 9/32" | 12'-0" | … | 46 | 9 | … | 55 |
| 12'-3" | 1'-7 11/16" | 12'-3" | … | 45 | 11 | … | 56 |
| 12'-6" | 1'-8 3/32" | 12'-6" | … | 44 | 13 | … | 57 |
| 12'-9" | 1'-8½" | 12'-9" | … | 43 | 15 | … | 58 |
| 13'-0" | 1'-8 29/32" | 13'-0" | … | 42 | 17 | … | 59 |
| 13'-3" | 1'-9 5/16" | 13'-3" | … | 41 | 19 | … | 60 |
| 13'-6" | 1'-9 23/32" | 13'-6" | … | 40 | 21 | … | 61 |
| 13'-9" | 1'-10 3/32" | 13'-9" | … | 39 | 23 | … | 62 |
| 14'-0" | 1'-10½" | 14'-0" | … | 38 | 25 | … | 63 |
| 14'-3" | 1'-10 29/32" | 14'-3" | … | 37 | 27 | … | 64 |
| 14'-6" | 1'-11 5/16" | 14'-6" | … | 36 | 29 | … | 65 |
| 14'-9" | 1'-11 23/32" | 14'-9" | … | 35 | 31 | … | 66 |
| 15'-0" | 2'-0 1/8" | 15'-0" | … | 34 | 33 | … | 67 |
| 15'-3" | 2'-0 17/32" | 15'-3" | … | 32 | 36 | … | 68 |
| 15'-6" | 2'-0 29/32" [?read: 2'-0 15/16", as printed on p.194 for the same span] | 15'-6" | … | 31 | 38 | … | 69 |
| 15'-9" | 2'-1 5/16" | 15'-9" | … | 30 | 40 | … | 70 |
| 16'-0" | 2'-1 23/32" | 16'-0" | … | 29 | 42 | … | 71 |
| 16'-3" | 2'-2 1/8" | 16'-3" | … | 28 | 44 | … | 72 |
| 16'-6" | 2'-2 17/32" | 16'-6" | … | 27 | 46 | … | 73 |
| 16'-9" | 2'-2 15/16" | 16'-9" | … | 26 | 48 | … | 74 |
| 17'-0" | 2'-3 11/32" | 17'-0" | … | 25 | 51 | … | 76 |
| 17'-3" | 2'-3¾" | 17'-3" | … | 24 | 53 | … | 77 |
| 17'-6" | 2'-4 1/8" | 17'-6" | … | 23 | 55 | … | 78 |
| 17'-9" | 2'-4 17/32" | 17'-9" | … | 22 | 57 | … | 79 |

Totals checked against row sums: all match. (At 60° the inside radius equals the span.)

Footer: "Continued Next Page" — "Page 192"

### p.193

**SPRUNG ARCHES — 1.608" rise per foot of span** (continued)
**12-INCH ARCH THICKNESS — Central Angle=60°**
12"x4½"x3", 12"x6"x3" or 12"x9"x3"
Brand 3878-B to be used for Skew

| Span | Rise | Inside Radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 18'-0" | 2'-4 15/16" | 18'-0" | … | 21 | 59 | … | 80 |
| 18'-3" | 2'-5 11/32" | 18'-3" | … | 20 | 61 | … | 81 |
| 18'-6" | 2'-5¾" | 18'-6" | … | 19 | 63 | … | 82 |
| 18'-9" | 2'-6 5/32" | 18'-9" | … | 18 | 65 | … | 83 |
| 19'-0" | 2'-6 17/32" | 19'-0" | … | 17 | 67 | … | 84 |
| 19'-3" | 2'-6 15/16" | 19'-3" | … | 16 | 69 | … | 85 |
| 19'-6" | 2'-7 11/32" | 19'-6" | … | 15 | 71 | … | 86 |
| 19'-9" | 2'-7¾" | 19'-9" | … | 14 | 73 | … | 87 |
| 20'-0" | 2'-8 5/32" | 20'-0" | … | 13 | 75 | … | 88 |
| 20'-3" | 2'-8 9/16" | 20'-3" | … | 12 | 77 | … | 89 |
| 20'-6" | 2'-8 31/32" | 20'-6" | … | 11 | 79 | … | 90 |
| 20'-9" | 2'-9 11/32" | 20'-9" | … | 10 | 81 | … | 91 |
| 21'-0" | 2'-9¾" | 21'-0" | … | 9 | 83 | … | 92 |
| 21'-3" | 2'-10 5/32" | 21'-3" | … | 8 | 85 | … | 93 |
| 21'-6" | 2'-10 9/16" | 21'-6" | … | 7 | 87 | … | 94 |
| 21'-9" | 2'-10 31/32" | 21'-9" | … | 6 | 89 | … | 95 |
| 22'-0" | 2'-11 3/8" | 22'-0" | … | 5 | 91 | … | 96 |
| 22'-3" | 2'-11 25/32" | 22'-3" | … | 3 | 94 | … | 97 |
| 22'-6" | 3'-0 3/16" | 22'-6" | … | 2 | 97 | … | 99 |
| 22'-9" | 3'-0 19/32" | 22'-9" | … | 1 | 99 | … | 100 |
| 23'-0" | 3'-0 31/32" | 23'-0" | … | … | 101 | … | 101 |
| 23'-3" | 3'-1 3/8" | 23'-3" | … | … | 101 | 1 | 102 |
| 23'-6" | 3'-1 25/32" | 23'-6" | … | … | 101 | 2 | 103 |
| 23'-9" | 3'-2 3/16" | 23'-9" | … | … | 101 | 3 | 104 |
| 24'-0" | 3'-2 19/32" | 24'-0" | … | … | 101 | 4 | 105 |
| 24'-3" | 3'-3" | 24'-3" | … | … | 101 | 5 | 106 |
| 24'-6" | 3'-3 3/8" | 24'-6" | … | … | 101 | 6 | 107 |
| 24'-9" | 3'-3 25/32" | 24'-9" | … | … | 101 | 7 | 108 |
| 25'-0" | 3'-4 3/16" | 25'-0" | … | … | 101 | 8 | 109 |
| 25'-3" | 3'-4 19/32" | 25'-3" | … | … | 101 | 9 | 110 |
| 25'-6" | 3'-5" | 25'-6" | … | … | 101 | 10 | 111 |
| 25'-9" | 3'-5 13/32" | 25'-9" | … | … | 101 | 11 | 112 |
| 26'-0" | 3'-5 13/16" | 26'-0" | … | … | 101 | 12 | 113 |
| 26'-3" | 3'-6 7/32" | 26'-3" | … | … | 101 | 13 | 114 |
| 26'-6" | 3'-6 5/8" | 26'-6" | … | … | 101 | 14 | 115 |
| 26'-9" | 3'-7" | 26'-9" | … | … | 101 | 15 | 116 |
| 27'-0" | 3'-7 13/32" | 27'-0" | … | … | 101 | 16 | 117 |
| 27'-3" | 3'-7 13/16" | 27'-3" | … | … | 101 | 17 | 118 |
| 27'-6" | 3'-8 7/32" | 27'-6" | … | … | 101 | 19 | 120 |
| 27'-9" | 3'-8 5/8" | 27'-9" | … | … | 101 | 20 | 121 |
| 28'-0" | 3'-9 1/32" | 28'-0" | … | … | 101 | 21 | 122 |
| 28'-3" | 3'-9 7/16" | 28'-3" | … | … | 101 | 22 | 123 |
| 28'-6" | 3'-9 13/16" | 28'-6" | … | … | 101 | 23 | 124 |
| 28'-9" | 3'-10 7/32" | 28'-9" | … | … | 101 | 24 | 125 |
| 29'-0" | 3'-10 5/8" | 29'-0" | … | … | 101 | 25 | 126 |
| 29'-3" | 3'-11 1/32" | 29'-3" | … | … | 101 | 26 | 127 |
| 29'-6" | 3'-11 7/16" | 29'-6" | … | … | 101 | 27 | 128 |
| 29'-9" | 3'-11 27/32" | 29'-9" | … | … | 101 | 28 | 129 |
| 30'-0" | 4'-0¼" | 30'-0" | … | … | 101 | 29 | 130 |

Totals checked against row sums: all match.

Footer: "Page 193"


## Image (51).jpg — catalogue p.194–195

(Scan rotated 90°; two facing pages.)

### p.194

**SPRUNG ARCHES — 1.608" rise per foot of span**
**13½-INCH ARCH THICKNESS — Central Angle=60°**
13½"x4½"x3", 13½"x6"x3" or 13½"x9"x3"
Brand 3878-C to be used for Skew

Brick required per course: No. 2 Wedge 13½x6x(3-2½); No. 1 Wedge 13½x6x(3-2¾); No. 1-X Wedge 13½x6x(3-2⅞); Straights 13½x6x3.

| Span | Rise | Inside Radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 6'-0" | 9 21/32" | 6'-0" | 27 | 3 | … | … | 30 |
| 6'-3" | 10 1/16" | 6'-3" | 26 | 5 | … | … | 31 |
| 6'-6" | 10 7/16" | 6'-6" | 25 | 7 | … | … | 32 |
| 6'-9" | 10 27/32" | 6'-9" | 24 | 9 | … | … | 33 |
| 7'-0" | 11¼" | 7'-0" | 22 | 12 | … | … | 34 |
| 7'-3" | 11 21/32" | 7'-3" | 21 | 14 | … | … | 35 |
| 7'-6" | 1'-0 1/16" | 7'-6" | 20 | 16 | … | … | 36 |
| 7'-9" | 1'-0 15/32" | 7'-9" | 20 | 18 | … | … | 38 |
| 8'-0" | 1'-0 7/8" | 8'-0" | 19 | 20 | … | … | 39 |
| 8'-3" | 1'-1¼" | 8'-3" | 18 | 22 | … | … | 40 |
| 8'-6" | 1'-1 21/32" | 8'-6" | 17 | 24 | … | … | 41 |
| 8'-9" | 1'-2 1/16" | 8'-9" | 16 | 26 | … | … | 42 |
| 9'-0" | 1'-2 15/32" | 9'-0" | 14 | 29 | … | … | 43 |
| 9'-3" | 1'-2 7/8" | 9'-3" | 13 | 31 | … | … | 44 |
| 9'-6" | 1'-3 9/32" | 9'-6" | 12 | 33 | … | … | 45 |
| 9'-9" | 1'-3 11/16" | 9'-9" | 11 | 35 | … | … | 46 |
| 10'-0" | 1'-4 3/32" [?read: 1'-4 1/16" on p.192] | 10'-0" | 10 | 37 | … | … | 47 |
| 10'-3" | 1'-4 15/32" | 10'-3" | 9 | 39 | … | … | 48 |
| 10'-6" | 1'-4 7/8" | 10'-6" | 8 | 41 | … | … | 49 |
| 10'-9" | 1'-5 9/32" | 10'-9" | 7 | 43 | … | … | 50 |
| 11'-0" | 1'-5 11/16" | 11'-0" | 6 | 45 | … | … | 51 |
| 11'-3" | 1'-6 3/32" | 11'-3" | 5 | 47 | … | … | 52 |
| 11'-6" | 1'-6½" | 11'-6" | 4 | 49 | … | … | 53 |
| 11'-9" | 1'-6 29/32" | 11'-9" | 3 | 51 | … | … | 54 |
| 12'-0" | 1'-7 9/32" | 12'-0" | 2 | 53 | … | … | 55 |
| 12'-3" | 1'-7 11/16" | 12'-3" | 1 | 55 | … | … | 56 |
| 12'-4½" | 1'-7 29/32" | 12'-4½" | … | 57 | … | … | 57 |
| 12'-6" | 1'-8 3/32" | 12'-6" | … | 56 | 1 | … | 57 |
| 12'-9" | 1'-8½" | 12'-9" | … | 55 | 3 | … | 58 |
| 13'-0" | 1'-8 29/32" | 13'-0" | … | 54 | 5 | … | 59 |
| 13'-3" | 1'-9 5/16" | 13'-3" | … | 53 | 7 | … | 60 |
| 13'-6" | 1'-9 23/32" | 13'-6" | … | 52 | 10 | … | 62 |
| 13'-9" | 1'-10 1/8" | 13'-9" | … | 51 | 12 | … | 63 |
| 14'-0" | 1'-10½" | 14'-0" | … | 50 | 14 | … | 64 |
| 14'-3" | 1'-10 29/32" | 14'-3" | … | 49 | 16 | … | 65 |
| 14'-6" | 1'-11 5/16" | 14'-6" | … | 48 | 18 | … | 66 |
| 14'-9" | 1'-11 23/32" | 14'-9" | … | 47 | 20 | … | 67 |
| 15'-0" | 2'-0 1/8" | 15'-0" | … | 46 | 22 | … | 68 |
| 15'-3" | 2'-0 17/32" | 15'-3" | … | 45 | 24 | … | 69 |
| 15'-6" | 2'-0 15/16" | 15'-6" | … | 44 | 26 | … | 70 |
| 15'-9" | 2'-1 5/16" | 15'-9" | … | 43 | 28 | … | 71 |
| 16'-0" | 2'-1 23/32" | 16'-0" | … | 41 | 31 | … | 72 |
| 16'-3" | 2'-2 1/8" | 16'-3" | … | 40 | 33 | … | 73 |
| 16'-6" | 2'-2 17/32" | 16'-6" | … | 39 | 35 | … | 74 |
| 16'-9" | 2'-2 15/16" | 16'-9" | … | 38 | 37 | … | 75 |
| 17'-0" | 2'-3 11/32" | 17'-0" | … | 37 | 39 | … | 76 |
| 17'-3" | 2'-3¾" | 17'-3" | … | 36 | 41 | … | 77 |
| 17'-6" | 2'-4 1/8" | 17'-6" | … | 35 | 43 | … | 78 |
| 17'-9" | 2'-4 17/32" | 17'-9" | … | 34 | 45 | … | 79 |

Totals checked against row sums: all match.
Rise fractions on this page were read at reduced scale; where a value differs by 1/32" from the same span on p.192 (10'-0", 11'-9", 13'-9"), one of my two reads is wrong; treat those three as [?read].

Footer: "Continued Next Page" — "Page 194"

### p.195

**SPRUNG ARCHES — 1.608" rise per foot of span** (continued)
**13½-INCH ARCH THICKNESS — Central Angle=60°**
13½"x4½"x3", 13½"x6"x3" or 13½"x9"x3"
Brand 3878-C to be used for Skew

| Span | Rise | Inside Radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 18'-0" | 2'-4 15/16" | 18'-0" | … | 33 | 47 | … | 80 |
| 18'-3" | 2'-5 11/32" | 18'-3" | … | 32 | 49 | … | 81 |
| 18'-6" | 2'-5¾" | 18'-6" | … | 31 | 51 | … | 82 |
| 18'-9" | 2'-6 5/32" | 18'-9" | … | 30 | 54 | … | 84 |
| 19'-0" | 2'-6 9/16" | 19'-0" | … | 29 | 56 | … | 85 |
| 19'-3" | 2'-6 15/16" | 19'-3" | … | 28 | 58 | … | 86 |
| 19'-6" | 2'-7 11/32" | 19'-6" | … | 27 | 60 | … | 87 |
| 19'-9" | 2'-7¾" | 19'-9" | … | 26 | 62 | … | 88 |
| 20'-0" | 2'-8 5/32" | 20'-0" | … | 25 | 64 | … | 89 |
| 20'-3" | 2'-8 9/16" | 20'-3" | … | 24 | 66 | … | 90 |
| 20'-6" | 2'-8 31/32" | 20'-6" | … | 23 | 68 | … | 91 |
| 20'-9" | 2'-9 3/8" | 20'-9" | … | 22 | 70 | … | 92 |
| 21'-0" | 2'-9¾" | 21'-0" | … | 21 | 72 | … | 93 |
| 21'-3" | 2'-10 5/32" | 21'-3" | … | 19 | 75 | … | 94 |
| 21'-6" | 2'-10 9/16" | 21'-6" | … | 18 | 77 | … | 95 |
| 21'-9" | 2'-10 31/32" | 21'-9" | … | 17 | 79 | … | 96 |
| 22'-0" | 2'-11 3/8" | 22'-0" | … | 16 | 81 | … | 97 |
| 22'-3" | 2'-11 25/32" | 22'-3" | … | 15 | 83 | … | 98 |
| 22'-6" | 3'-0 3/16" | 22'-6" | … | 14 | 85 | … | 99 |
| 22'-9" | 3'-0 19/32" | 22'-9" | … | 13 | 87 | … | 100 |
| 23'-0" | 3'-0 31/32" | 23'-0" | … | 12 | 89 | … | 101 |
| 23'-3" | 3'-1 3/8" | 23'-3" | … | 11 | 91 | … | 102 |
| 23'-6" | 3'-1 25/32" | 23'-6" | … | 10 | 93 | … | 103 |
| 23'-9" | 3'-2 3/16" | 23'-9" | … | 9 | 95 | … | 104 |
| 24'-0" | 3'-2 19/32" | 24'-0" | … | 8 | 97 | … | 105 |
| 24'-3" | 3'-3" | 24'-3" | … | 7 | 99 | … | 106 |
| 24'-6" | 3'-3 13/32" | 24'-6" | … | 6 | 101 | … | 107 |
| 24'-9" | 3'-3 13/16" | 24'-9" | … | 5 | 104 | … | 109 |
| 25'-0" | 3'-4 3/16" | 25'-0" | … | 4 | 106 | … | 110 |
| 25'-3" | 3'-4 19/32" | 25'-3" | … | 3 | 108 | … | 111 |
| 25'-6" | 3'-5" | 25'-6" | … | 2 | 110 | … | 112 |
| 25'-9" | 3'-5 13/32" | 25'-9" | … | 1 | 112 | … | 113 |
| 25'-10½" | 3'-5 19/32" | 25'-10½" | … | … | 113 | … | 113 |
| 26'-0" | 3'-5 13/16" | 26'-0" | … | … | 113 | 1 | 114 |
| 26'-3" | 3'-6 7/32" | 26'-3" | … | … | 113 | 2 | 115 |
| 26'-6" | 3'-6 5/8" | 26'-6" | … | … | 113 | 3 | 116 |
| 26'-9" | 3'-7" | 26'-9" | … | … | 113 | 4 | 117 |
| 27'-0" | 3'-7 13/32" | 27'-0" | … | … | 113 | 5 | 118 |
| 27'-3" | 3'-7 13/16" | 27'-3" | … | … | 113 | 6 | 119 |
| 27'-6" | 3'-8 7/32" | 27'-6" | … | … | 113 | 7 | 120 |
| 27'-9" | 3'-8 5/8" | 27'-9" | … | … | 113 | 8 | 121 |
| 28'-0" | 3'-9 1/32" | 28'-0" | … | … | 113 | 9 | 122 |
| 28'-3" | 3'-9 7/16" | 28'-3" | … | … | 113 | 10 | 123 |
| 28'-6" | 3'-9 13/16" | 28'-6" | … | … | 113 | 11 | 124 |
| 28'-9" | 3'-10 7/32" | 28'-9" | … | … | 113 | 12 | 125 |
| 29'-0" | 3'-10 5/8" | 29'-0" | … | … | 113 | 13 | 126 |
| 29'-3" | 3'-11 1/32" | 29'-3" | … | … | 113 | 14 | 127 |
| 29'-6" | 3'-11 7/16" | 29'-6" | … | … | 113 | 15 | 128 |
| 29'-9" | 3'-11 27/32" | 29'-9" | … | … | 113 | 16 | 129 |
| 30'-0" | 4'-0¼" | 30'-0" | … | … | 113 | 17 | 130 |

Totals checked against row sums: all match.
(Rises 19'-0", 20'-9", 24'-6", 24'-9" read here as 2'-6 9/16", 2'-9 3/8", 3'-3 13/32", 3'-3 13/16"; p.193 read as 2'-6 17/32", 2'-9 11/32", 3'-3 3/8", 3'-3 25/32" — 1/32" disagreements at small print; treat as [?read].)

Footer: "Page 195"


## Image (52).jpg — catalogue p.196–197

(Scan rotated 90°; two facing pages. Rise values follow the same 1.608"/ft series printed on pp.192–195.)

### p.196

**SPRUNG ARCHES — 1.608" rise per foot of span**
**15-INCH ARCH THICKNESS — Central Angle=60°**
15"x6"x3" or 15"x9"x3"

(No skew brand line is printed on this pair of pages.)

Brick required per course: No. 2 Wedge 15x6x(3-2½); No. 1 Wedge 15x6x(3-2¾); No. 1-X Wedge 15x6x(3-2⅞); Straights 15x6x3.

| Span | Rise | Inside Radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 6'-3" | 10 1/16" | 6'-3" | 32 | … | … | … | 32 |
| 6'-6" | 10 7/16" | 6'-6" | 31 | 2 | … | … | 33 |
| 6'-9" | 10 27/32" | 6'-9" | 30 | 4 | … | … | 34 |
| 7'-0" | 11¼" | 7'-0" | 28 | 7 | … | … | 35 |
| 7'-3" | 11 21/32" | 7'-3" | 27 | 9 | … | … | 36 |
| 7'-6" | 1'-0 1/16" | 7'-6" | 26 | 11 | … | … | 37 |
| 7'-9" | 1'-0 15/32" | 7'-9" | 25 | 13 | … | … | 38 |
| 8'-0" | 1'-0 7/8" | 8'-0" | 24 | 15 | … | … | 39 |
| 8'-3" | 1'-1¼" | 8'-3" | 23 | 17 | … | … | 40 |
| 8'-6" | 1'-1 21/32" | 8'-6" | 22 | 19 | … | … | 41 |
| 8'-9" | 1'-2 1/16" | 8'-9" | 21 | 21 | … | … | 42 |
| 9'-0" | 1'-2 15/32" | 9'-0" | 20 | 23 | … | … | 43 |
| 9'-3" | 1'-2 7/8" | 9'-3" | 19 | 25 | … | … | 44 |
| 9'-6" | 1'-3 9/32" | 9'-6" | 18 | 27 | … | … | 45 |
| 9'-9" | 1'-3 11/16" | 9'-9" | 17 | 29 | … | … | 46 |
| 10'-0" | 1'-4 3/32" | 10'-0" | 16 | 31 | … | … | 47 |
| 10'-3" | 1'-4 15/32" | 10'-3" | 15 | 34 | … | … | 49 |
| 10'-6" | 1'-4 7/8" | 10'-6" | 14 | 36 | … | … | 50 |
| 10'-9" | 1'-5 9/32" | 10'-9" | 13 | 38 | … | … | 51 |
| 11'-0" | 1'-5 11/16" | 11'-0" | 12 | 40 | … | … | 52 |
| 11'-3" | 1'-6 3/32" | 11'-3" | 11 | 42 | … | … | 53 |
| 11'-6" | 1'-6½" | 11'-6" | 10 | 44 | … | … | 54 |
| 11'-9" | 1'-6 29/32" | 11'-9" | 9 | 46 | … | … | 55 |
| 12'-0" | 1'-7 9/32" | 12'-0" | 8 | 48 | … | … | 56 |
| 12'-3" | 1'-7 11/16" | 12'-3" | 7 | 50 | … | … | 57 |
| 12'-6" | 1'-8 3/32" | 12'-6" | 5 | 53 | … | … | 58 |
| 12'-9" | 1'-8½" | 12'-9" | 4 | 55 | … | … | 59 |
| 13'-0" | 1'-8 29/32" | 13'-0" | 3 | 57 | … | … | 60 |
| 13'-3" | 1'-9 5/16" | 13'-3" | 2 | 59 | … | … | 61 |
| 13'-6" | 1'-9 23/32" | 13'-6" | 1 | 61 | … | … | 62 |
| 13'-9" | 1'-10 1/8" | 13'-9" | … | 63 | … | … | 63 |
| 14'-0" | 1'-10½" | 14'-0" | … | 62 | 2 | … | 64 |
| 14'-3" | 1'-10 29/32" | 14'-3" | … | 61 | 4 | … | 65 |
| 14'-6" | 1'-11 5/16" | 14'-6" | … | 60 | 6 | … | 66 |
| 14'-9" | 1'-11 23/32" | 14'-9" | … | 59 | 8 | … | 67 |
| 15'-0" | 2'-0 1/8" | 15'-0" | … | 58 | 10 | … | 68 |
| 15'-3" | 2'-0 17/32" | 15'-3" | … | 57 | 12 | … | 69 |
| 15'-6" | 2'-0 15/16" | 15'-6" | … | 56 | 13 | … | 70 |
| 15'-9" | 2'-1 5/16" | 15'-9" | … | 55 | 17 | … | 72 |
| 16'-0" | 2'-1 23/32" | 16'-0" | … | 54 | 19 | … | 73 |
| 16'-3" | 2'-2 1/8" | 16'-3" | … | 53 | 21 | … | 74 |
| 16'-6" | 2'-2 17/32" | 16'-6" | … | 52 | 23 | … | 75 |
| 16'-9" | 2'-2 15/16" | 16'-9" | … | 51 | 25 | … | 76 |
| 17'-0" | 2'-3 11/32" | 17'-0" | … | 49 | 28 | … | 77 |
| 17'-3" | 2'-3¾" | 17'-3" | … | 48 | 30 | … | 78 |
| 17'-6" | 2'-4 1/8" | 17'-6" | … | 47 | 32 | … | 79 |
| 17'-9" | 2'-4 17/32" | 17'-9" | … | 46 | 34 | … | 80 |
| 18'-0" | 2'-4 15/16" | 18'-0" | … | 45 | 36 | … | 81 |

Totals check: MISMATCH — 15'-6: row sum 69, printed total 70
(The 15'-6" No. 1-X cell reads 13; 14 would fit both the column's step pattern and the printed total of 70. [?read: 13 or 14])

Footer: "Continued Next Page" — "Page 196"

### p.197

**SPRUNG ARCHES — 1.608" rise per foot of span** (continued)
**15-INCH ARCH THICKNESS — Central Angle=60°**
15"x6"x3" or 15"x9"x3"

| Span | Rise | Inside Radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 18'-3" | 2'-5 11/32" | 18'-3" | … | 44 | 38 | … | 82 |
| 18'-6" | 2'-5¾" | 18'-6" | … | 43 | 40 | … | 83 |
| 18'-9" | 2'-6 5/32" | 18'-9" | … | 42 | 42 | … | 84 |
| 19'-0" | 2'-6 9/16" | 19'-0" | … | 41 | 44 | … | 85 |
| 19'-3" | 2'-6 15/16" | 19'-3" | … | 40 | 46 | … | 86 |
| 19'-6" | 2'-7 11/32" | 19'-6" | … | 39 | 48 | … | 87 |
| 19'-9" | 2'-7¾" | 19'-9" | … | 38 | 50 | … | 88 |
| 20'-0" | 2'-8 5/32" | 20'-0" | … | 37 | 52 | … | 89 |
| 20'-3" | 2'-8 9/16" | 20'-3" | … | 36 | 54 | … | 90 |
| 20'-6" | 2'-8 31/32" | 20'-6" | … | 35 | 56 | … | 91 |
| 20'-9" | 2'-9 3/8" | 20'-9" | … | 34 | 58 | … | 92 |
| 21'-0" | 2'-9¾" | 21'-0" | … | 33 | 61 | … | 94 |
| 21'-3" | 2'-10 5/32" | 21'-3" | … | 32 | 63 | … | 95 |
| 21'-6" | 2'-10 9/16" | 21'-6" | … | 31 | 65 | … | 96 |
| 21'-9" | 2'-10 31/32" | 21'-9" | … | 30 | 67 | … | 97 |
| 22'-0" | 2'-11 3/8" | 22'-0" | … | 29 | 69 | … | 98 |
| 22'-3" | 2'-11 25/32" | 22'-3" | … | 28 | 71 | … | 99 |
| 22'-6" | 3'-0 3/16" | 22'-6" | … | 26 | 74 | … | 100 |
| 22'-9" | 3'-0 19/32" | 22'-9" | … | 25 | 76 | … | 101 |
| 23'-0" | 3'-0 31/32" | 23'-0" | … | 24 | 78 | … | 102 |
| 23'-3" | 3'-1 3/8" | 23'-3" | … | 23 | 80 | … | 103 |
| 23'-6" | 3'-1 25/32" | 23'-6" | … | 22 | 82 | … | 104 |
| 23'-9" | 3'-2 3/16" | 23'-9" | … | 21 | 84 | … | 105 |
| 24'-0" | 3'-2 19/32" | 24'-0" | … | 20 | 86 | … | 106 |
| 24'-3" | 3'-3" | 24'-3" | … | 19 | 88 | … | 107 |
| 24'-6" | 3'-3 13/32" | 24'-6" | … | 18 | 90 | … | 108 |
| 24'-9" | 3'-3 13/16" | 24'-9" | … | 17 | 92 | … | 109 |
| 25'-0" | 3'-4 3/16" | 25'-0" | … | 16 | 94 | … | 110 |
| 25'-3" | 3'-4 19/32" | 25'-3" | … | 15 | 96 | … | 111 |
| 25'-6" | 3'-5" | 25'-6" | … | 14 | 98 | … | 112 |
| 25'-9" | 3'-5 13/32" | 25'-9" | … | 13 | 100 | … | 113 |
| 26'-0" | 3'-5 13/16" | 26'-0" | … | 12 | 102 | … | 114 |
| 26'-3" | 3'-6 7/32" | 26'-3" | … | 10 | 105 | … | 115 |
| 26'-6" | 3'-6 5/8" | 26'-6" | … | 9 | 107 | … | 116 |
| 26'-9" | 3'-7" | 26'-9" | … | 9 | 109 | … | 118 |
| 27'-0" | 3'-7 13/32" | 27'-0" | … | 8 | 111 | … | 119 |
| 27'-3" | 3'-7 13/16" | 27'-3" | … | 7 | 113 | … | 120 |
| 27'-6" | 3'-8 7/32" | 27'-6" | … | 6 | 115 | … | 121 |
| 27'-9" | 3'-8 5/8" | 27'-9" | … | 4 | 118 | … | 122 |
| 28'-0" | 3'-9 1/32" | 28'-0" | … | 3 | 120 | … | 123 |
| 28'-3" | 3'-9 7/16" | 28'-3" | … | 2 | 122 | … | 124 |
| 28'-6" | 3'-9 13/16" | 28'-6" | … | 1 | 124 | … | 125 |
| 28'-9" | 3'-10 7/32" | 28'-9" | … | … | 126 | … | 126 |
| 29'-0" | 3'-10 5/8" | 29'-0" | … | … | 126 | 1 | 127 |
| 29'-3" | 3'-11 1/32" | 29'-3" | … | … | 126 | 2 | 128 |
| 29'-6" | 3'-11 7/16" | 29'-6" | … | … | 126 | 3 | 129 |
| 29'-9" | 3'-11 27/32" | 29'-9" | … | … | 126 | 4 | 130 |
| 30'-0" | 4'-0¼" | 30'-0" | … | … | 126 | 5 | 131 |

Totals check: all rows match.
Footer: "Page 197"

## Image (53).jpg — catalogue p.198–199

(Scan rotated 90°; two facing pages.)

### p.198

**SPRUNG ARCHES — 1.608" rise per foot of span**
**18-INCH ARCH THICKNESS — Central Angle=60°**
18"x6"x3" or 18"x9"x3"

(No skew brand line printed.)

Brick required per course: No. 2 Wedge 18x6x(3-2½); No. 1 Wedge 18x6x(3-2¾); No. 1-X Wedge 18x6x(3-2⅞); Straights 18x6x3.

| Span | Rise | Inside Radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 8'-0" | 1'-0 7/8" | 8'-0" | 36 | 4 | … | … | 40 |
| 8'-3" | 1'-1¼" | 8'-3" | 35 | 6 | … | … | 41 |
| 8'-6" | 1'-1 21/32" | 8'-6" | 34 | 8 | … | … | 42 |
| 8'-9" | 1'-2 1/16" | 8'-9" | 32 | 11 | … | … | 43 |
| 9'-0" | 1'-2 15/32" | 9'-0" | 31 | 13 | … | … | 44 |
| 9'-3" | 1'-2 7/8" | 9'-3" | 30 | 15 | … | … | 45 |
| 9'-6" | 1'-3 9/32" | 9'-6" | 29 | 17 | … | … | 46 |
| 9'-9" | 1'-3 11/16" | 9'-9" | 28 | 19 | … | … | 47 |
| 10'-0" | 1'-4 3/32" | 10'-0" | 28 | 21 | … | … | 49 |
| 10'-3" | 1'-4 15/32" | 10'-3" | 27 | 23 | … | … | 50 |
| 10'-6" | 1'-4 7/8" | 10'-6" | 25 | 26 | … | … | 51 |
| 10'-9" | 1'-5 9/32" | 10'-9" | 24 | 28 | … | … | 52 |
| 11'-0" | 1'-5 11/16" | 11'-0" | 23 | 30 | … | … | 53 |
| 11'-3" | 1'-6 3/32" | 11'-3" | 22 | 32 | … | … | 54 |
| 11'-6" | 1'-6½" | 11'-6" | 21 | 34 | … | … | 55 |
| 11'-9" | 1'-6 29/32" | 11'-9" | 20 | 36 | … | … | 56 |
| 12'-0" | 1'-7 9/32" | 12'-0" | 19 | 38 | … | … | 57 |
| 12'-3" | 1'-7 11/16" | 12'-3" | 18 | 40 | … | … | 58 |
| 12'-6" | 1'-8 3/32" | 12'-6" | 17 | 42 | … | … | 59 |
| 12'-9" | 1'-8½" | 12'-9" | 16 | 44 | … | … | 60 |
| 13'-0" | 1'-8 29/32" | 13'-0" | 15 | 46 | … | … | 61 |
| 13'-3" | 1'-9 5/16" | 13'-3" | 14 | 48 | … | … | 62 |
| 13'-6" | 1'-9 23/32" | 13'-6" | 13 | 50 | … | … | 63 |
| 13'-9" | 1'-10 1/8" | 13'-9" | 12 | 52 | … | … | 64 |
| 14'-0" | 1'-10½" | 14'-0" | 11 | 54 | … | … | 65 |
| 14'-3" | 1'-10 29/32" | 14'-3" | 9 | 57 | … | … | 66 |
| 14'-6" | 1'-11 5/16" | 14'-6" | 8 | 59 | … | … | 67 |
| 14'-9" | 1'-11 23/32" | 14'-9" | 7 | 61 | … | … | 68 |
| 15'-0" | 2'-0 1/8" | 15'-0" | 6 | 63 | … | … | 69 |
| 15'-3" | 2'-0 17/32" | 15'-3" | 5 | 65 | … | … | 70 |
| 15'-6" | 2'-0 15/16" | 15'-6" | 5 | 67 | … | … | 72 |
| 15'-9" | 2'-1 5/16" | 15'-9" | 4 | 69 | … | … | 73 |
| 16'-0" | 2'-1 23/32" | 16'-0" | 2 | 72 | … | … | 74 |
| 16'-3" | 2'-2 1/8" | 16'-3" | 1 | 74 | … | … | 75 |
| 16'-6" | 2'-2 17/32" | 16'-6" | … | 76 | … | … | 76 |
| 16'-9" | 2'-2 15/16" | 16'-9" | … | 75 | 2 | … | 77 |
| 17'-0" | 2'-3 11/32" | 17'-0" | … | 74 | 4 | … | 78 |
| 17'-3" | 2'-3¾" | 17'-3" | … | 72 | 7 | … | 79 |
| 17'-6" | 2'-4 1/8" | 17'-6" | … | 71 | 9 | … | 80 |
| 17'-9" | 2'-4 17/32" | 17'-9" | … | 70 | 11 | … | 81 |
| 18'-0" | 2'-4 15/16" | 18'-0" | … | 69 | 13 | … | 82 |
| 18'-3" | 2'-5 11/32" | 18'-3" | … | 68 | 15 | … | 83 |
| 18'-6" | 2'-5¾" | 18'-6" | … | 67 | 17 | … | 84 |
| 18'-9" | 2'-6 5/32" | 18'-9" | … | 66 | 19 | … | 85 |
| 19'-0" | 2'-6 9/16" | 19'-0" | … | 65 | 21 | … | 86 |
| 19'-3" | 2'-6 15/16" | 19'-3" | … | 64 | 23 | … | 87 |
| 19'-6" | 2'-7 11/32" | 19'-6" | … | 63 | 25 | … | 88 |
| 19'-9" | 2'-7¾" | 19'-9" | … | 62 | 27 | … | 89 |
| 20'-0" | 2'-8 5/32" | 20'-0" | … | 61 | 29 | … | 90 |
| 20'-3" | 2'-8 9/16" | 20'-3" | … | 60 | 31 | … | 91 |

Totals check: all rows match.
Footer: "Continued Next Page" — "Page 198"

### p.199

**SPRUNG ARCHES — 1.608" rise per foot of span** (continued)
**18-INCH ARCH THICKNESS — Central Angle=60°**
18"x6"x3" or 18"x9"x3"

| Span | Rise | Inside Radius | No. 2 Wedge | No. 1 Wedge | No. 1-X Wedge | Straights | Total |
|---|---|---|---|---|---|---|---|
| 20'-6" | 2'-8 31/32" | 20'-6" | … | 58 | 34 | … | 92 |
| 20'-9" | 2'-9 3/8" | 20'-9" | … | 57 | 36 | … | 93 |
| 21'-0" | 2'-9¾" | 21'-0" | … | 56 | 38 | … | 94 |
| 21'-3" | 2'-10 5/32" | 21'-3" | … | 56 | 40 | … | 96 |
| 21'-6" | 2'-10 9/16" | 21'-6" | … | 55 | 42 | … | 97 |
| 21'-9" | 2'-10 31/32" | 21'-9" | … | 54 | 44 | … | 98 |
| 22'-0" | 2'-11 3/8" | 22'-0" | … | 53 | 46 | … | 99 |
| 22'-3" | 2'-11 25/32" | 22'-3" | … | 52 | 48 | … | 100 |
| 22'-6" | 3'-0 3/16" | 22'-6" | … | 50 | 51 | … | 101 |
| 22'-9" | 3'-0 19/32" | 22'-9" | … | 49 | 53 | … | 102 |
| 23'-0" | 3'-0 31/32" | 23'-0" | … | 48 | 55 | … | 103 |
| 23'-3" | 3'-1 3/8" | 23'-3" | … | 47 | 57 | … | 104 |
| 23'-6" | 3'-1 25/32" | 23'-6" | … | 46 | 59 | … | 105 |
| 23'-9" | 3'-2 3/16" | 23'-9" | … | 45 | 61 | … | 106 |
| 24'-0" | 3'-2 19/32" | 24'-0" | … | 44 | 63 | … | 107 |
| 24'-3" | 3'-3" | 24'-3" | … | 43 | 65 | … | 108 |
| 24'-6" | 3'-3 13/32" | 24'-6" | … | 42 | 67 | … | 109 |
| 24'-9" | 3'-3 13/16" | 24'-9" | … | 41 | 69 | … | 110 |
| 25'-0" | 3'-4 3/16" | 25'-0" | … | 40 | 71 | … | 111 |
| 25'-3" | 3'-4 19/32" | 25'-3" | … | 39 | 73 | … | 112 |
| 25'-6" | 3'-5" | 25'-6" | … | 38 | 75 | … | 113 |
| 25'-9" | 3'-5 13/32" | 25'-9" | … | 37 | 77 | … | 114 |
| 26'-0" | 3'-5 13/16" | 26'-0" | … | 36 | 79 | … | 115 |
| 26'-3" | 3'-6 7/32" | 26'-3" | … | 34 | 82 | … | 116 |
| 26'-6" | 3'-6 5/8" | 26'-6" | … | 33 | 84 | … | 117 |
| 26'-9" | 3'-7" | 26'-9" | … | 33 | 86 | … | 119 |
| 27'-0" | 3'-7 13/32" | 27'-0" | … | 32 | 88 | … | 120 |
| 27'-3" | 3'-7 13/16" | 27'-3" | … | 31 | 90 | … | 121 |
| 27'-6" | 3'-8 7/32" | 27'-6" | … | 30 | 92 | … | 122 |
| 27'-9" | 3'-8 5/8" | 27'-9" | … | 29 | 94 | … | 123 |
| 28'-0" | 3'-9 1/32" | 28'-0" | … | 27 | 97 | … | 124 |
| 28'-3" | 3'-9 7/16" | 28'-3" | … | 26 | 99 | … | 125 |
| 28'-6" | 3'-9 13/16" | 28'-6" | … | 25 | 101 | … | 126 |
| 28'-9" | 3'-10 7/32" | 28'-9" | … | 24 | 103 | … | 127 |
| 29'-0" | 3'-10 5/8" | 29'-0" | … | 23 | 105 | … | 128 |
| 29'-3" | 3'-11 1/32" | 29'-3" | … | 22 | 107 | … | 129 |
| 29'-6" | 3'-11 7/16" | 29'-6" | … | 21 | 109 | … | 130 |
| 29'-9" | 3'-11 27/32" | 29'-9" | … | 20 | 111 | … | 131 |
| 30'-0" | 4'-0¼" | 30'-0" | … | 19 | 113 | … | 132 |
| 30'-3" | 4'-0 21/32" | 30'-3" | … | 18 | 115 | … | 133 |
| 30'-6" | 4'-1 1/32" | 30'-6" | … | 17 | 117 | … | 134 |
| 31'-0" | 4'-1 27/32" | 31'-0" | … | 15 | 121 | … | 136 |
| 31'-6" | 4'-2 21/32" | 31'-6" | … | 12 | 126 | … | 138 |
| 32'-0" | 4'-3 15/32" | 32'-0" | … | 10 | 130 | … | 140 |
| 32'-6" | 4'-4¼" | 32'-6" | … | 9 | 134 | … | 143 |
| 33'-0" | 4'-5 1/16" | 33'-0" | … | 7 | 138 | … | 145 |
| 33'-6" | 4'-5 7/8" | 33'-6" | … | 4 | 143 | … | 147 |
| 34'-0" | 4'-6 11/16" | 34'-0" | … | 2 | 147 | … | 149 |
| 34'-6" | 4'-7 15/32" | 34'-6" | … | … | 151 | … | 151 |
| 35'-0" | 4'-8 9/32" | 35'-0" | … | … | 151 | 2 | 153 |

Totals check: all rows match.
Beyond 30'-0" the span steps are 30'-3", 30'-6", then every 6" to 35'-0".

Footer: "Page 199"

## Image (54).jpg — section divider (no printed page number)

Section title page (upper half of scan): **A. P. GREEN — ESTIMATING DATA and GENERAL INFORMATION**. Decorative artwork only (pencil, drawing pins, paper clips, compass, A.P. Green logo). Lower half: decorative artwork on the reverse/facing page, no text. No tables, no data.

## Image (55).jpg — catalogue p.202–203

(Scan rotated 90°; two facing pages.)

### p.202 — Estimating Data

**STANDARD FIREBRICK**

| | 9" x 4½" x 2½" | 9" x 4½" x 3" |
|---|---|---|
| Approximate weight per brick | 7.6-8.4 lb. | |
| Approximate weight per cubic foot | 130-140 lb. | 130-140 lb. |
| One cubic foot requires | 17.0 brick | 14.2 brick |

(The weight-per-brick cell for 9" x 4½" x 3" is blank as printed.)

One square foot of wall or floor requires the following number of brick:

| Thickness | 9" x 4½" x 2½" | 9" x 4½" x 3" |
|---|---|---|
| 2½" thick | 3.6 | — |
| 3" thick | — | 3.6 |
| 4½" thick | 6.4 | 5.3 |
| 5" thick | 7.2 | — |
| 6" thick | — | 7.2 |
| 7½" thick | 10.8 | 8.9 |
| 9" thick | 12.8 | 10.7 |
| 13½" thick | 19.2 | 16.0 |
| 18" thick | 25.6 | 21.4 |
| 22½" thick | 32.0 | 26.7 |
| 27" thick | 38.4 | 32.1 |

**FOUR BRICK ARRANGEMENTS OFTEN USED** — sketches labelled STRETCHER COURSE, ROWLOCK COURSE, HEADER COURSE, SOLDIER COURSE.

**MORTAR REQUIRED TO LAY 1,000 PIECES**

| Size | @ 250 Lb. per M 9" Straights | @ 300 Lb. per M 9" Straights | @ 350 Lb. per M 9" Straights | @ 400 Lb. per M 9" Straights |
|---|---|---|---|---|
| 9 x 4½x2½ | 250 | 300 | 350 | 400 |
| 9 x 4½x3 | 270 | 325 | 380 | 435 |
| 9 x 6 x 2½ | 305 | 370 | 430 | 490 |
| 9 x 6 x 3 | 335 | 400 | 465 | 535 |
| 9 x 6 x 3½ Arches | 355 | 425 | 500 | 570 |
| 9 x 6¾x2½ | 335 | 405 | 475 | 540 |
| 9 x 6¾x3 | 365 | 435 | 510 | 580 |
| 9 x 9 x 2½ | 425 | 510 | 595 | 680 |
| 12 x 6 x 2½ | 395 | 470 | 550 | 630 |
| 12 x 6 x 3 | 425 | 510 | 595 | 680 |
| 13½x4½x2½ | 355 | 425 | 500 | 570 |
| 13½x6 x 2½ | 435 | 520 | 610 | 695 |
| 13½x6 x 3 | 470 | 560 | 660 | 750 |
| 9 x 6 x 4 Liners | 385 | 460 | 535 | 615 |
| 9 x 9 x 4 Liners | 515 | 615 | 720 | 825 |
| 9 x 4½x9 Calliaus | 545 | 655 | 765 | 875 |

"For estimating data on specific A. P. Green mortars; see page 41."

Footer: "Page 202"

### p.203 — Estimating Data

"Sectional views illustrating various types of firebrick walls with quantity figures to indicate the approximate number of brick required for each type of wall. The walls shown are of 9 x 4½ x 2½-inch brick."

Six section sketches with captions:

1. 4½" wall (dimension 4½"): "7.7 Firebrick per square foot of wall area". Caption: "4½" Firebrick wall. Headers every 5th course."
2. 9" wall (dimension 9"): "14.1 Firebrick per square foot of wall area". Caption: "9" Firebrick wall. Headers every 5th course."
3. 13½" wall (dimension 13½"), two qualities: "5.1 Firebrick per square foot of wall area" (hot-face layer) and "14.1 Firebrick per square foot of wall area" (backup). Caption: "13½" Firebrick wall. Two qualities of firebrick. 19.2 Firebrick per square foot of wall."
4. 13½" wall (dimension 13½"): "19.2 Firebrick per square foot of wall area". Caption: "13½" Firebrick wall. One quality of firebrick, fully bonded."
5. 18" wall (dimension 18"), two qualities: "11.5 Fire-brick per square foot of wall area" and "14.1 Fire-brick per square foot of wall area". Caption: "18" Firebrick wall. Two qualities of firebrick, bonded every 5th course. 25.6 Firebrick per square foot of wall."
6. 18" wall (dimension 18"), two qualities: "9.6 Fire-brick per square foot of wall area" and "16.0 Fire-brick per square foot of wall area". Caption: "18" Firebrick wall. Two qualities of firebrick, fully bonded. 25.6 Firebrick per square foot of wall."

Totals check: 5.1 + 14.1 = 19.2 ✓; 11.5 + 14.1 = 25.6 ✓; 9.6 + 16.0 = 25.6 ✓.

Footer: "Page 203"


## Image (56).jpg — catalogue p.204–205

(Scan rotated 90°; two facing pages. Both pages headed "Estimating Data".)

### p.204

**CASTABLES** (See pages 60 to 81 for specific product information.)

POUNDS OF MATERIAL REQUIRED PER SQUARE FOOT OF WALL THICKNESS — NET

| Product | Lbs. Reqd. Per Cubic Foot - Net | 1" Wall | 2" Wall | 3" Wall | 4" Wall | 4½" Wall | 5" Wall | 6" Wall | 7" Wall | 8" Wall | 9" Wall |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Castable Block Mix | 21 | 1.7 | 3.5 | 5.2 | 7.0 | 7.9 | 8.7 | 10.5 | 12.2 | 14.0 | 15.8 |
| Castable Insulation No. 20 | 55 | 4.6 | 9.2 | 13.8 | 18.3 | 20.6 | 22.9 | 27.5 | 32.1 | 36.7 | 41.3 |
| Castable No. 22 | 50 | 4.2 | 8.3 | 12.5 | 16.7 | 18.8 | 20.8 | 25.0 | 29.2 | 33.3 | 37.5 |
| Castite | 115 | 9.6 | 19.2 | 28.8 | 38.3 | 43.1 | 47.9 | 57.5 | 67.1 | 76.7 | 86.3 |
| Castex 24 C | 115 | 9.6 | 19.2 | 28.8 | 38.3 | 43.1 | 47.9 | 57.5 | 67.1 | 76.7 | 86.3 |
| Castex 25 C | 120 | 10.0 | 20.0 | 30.0 | 40.0 | 45.0 | 50.0 | 60.0 | 70.0 | 80.0 | 90.0 |
| Castex 25 C (Gunned) | 122 | 10.2 | 20.3 | 30.5 | 40.7 | 45.8 | 50.8 | 61.0 | 71.2 | 81.3 | 91.5 |
| Greencast-12 | 122 | 10.2 | 20.3 | 30.5 | 40.7 | 45.8 | 50.8 | 61.0 | 71.2 | 81.3 | 91.5 |
| Greencast-12 GR (Gunned) | 122 | 10.2 | 20.3 | 30.5 | 40.7 | 45.8 | 50.8 | 61.0 | 71.2 | 81.3 | 91.5 |
| Greencast-12 GR (Troweled) | 118 | 9.8 | 19.7 | 29.5 | 39.3 | 44.3 | 49.2 | 59.0 | 68.8 | 78.7 | 88.5 |
| Greencast-94 | 163 | 13.6 | 27.2 | 40.8 | 54.3 | 61.1 | 67.9 | 81.5 | 95.1 | 108.7 | 122.3 |
| Greencast-94 GR | 160 | 13.3 | 26.7 | 40.0 | 53.3 | 60.0 | 66.7 | 80.0 | 93.3 | 106.7 | 120.0 |
| Greencast-97 | 153 | 12.8 | 25.5 | 38.3 | 51.0 | 57.4 | 63.8 | 76.5 | 89.3 | 102.0 | 114.8 |
| Greencast-97 GR | 160 | 13.3 | 26.7 | 40.0 | 53.3 | 60.0 | 66.7 | 80.0 | 93.3 | 106.7 | 120.0 |
| Greencast-97L | 85 | 7.1 | 14.2 | 21.3 | 28.3 | 31.9 | 35.4 | 42.5 | 49.6 | 56.7 | 63.8 |
| Greencast-97L GR | 105 | 8.8 | 17.5 | 26.3 | 35.0 | 39.4 | 43.8 | 52.5 | 61.3 | 70.0 | 78.8 |
| Greencast-28 GR | 123 | 10.3 | 20.5 | 30.8 | 41.0 | 46.1 | 51.3 | 61.5 | 71.8 | 82.0 | 92.3 |
| Greencast-22-L GR | 80 | 6.7 | 13.3 | 20.0 | 26.7 | 30.0 | 33.3 | 40.0 | 46.7 | 53.3 | 60.0 |
| Greencrete ARC | 172 | 14.3 | 28.7 | 43.0 | 57.3 | 64.5 | 71.7 | 86.0 | 100.3 | 114.7 | 129.0 |
| Green Crete C Standard | 167 | 13.9 | 27.8 | 41.8 | 55.7 | 62.6 | 69.6 | 83.5 | 97.4 | 111.3 | 125.3 |
| Green Crete C Super | 175 | 14.6 | 29.2 | 43.8 | 58.3 | 65.6 | 72.9 | 87.5 | 102.1 | 116.7 | 131.3 |
| Gunweld-90 | 165 | 13.7 | 27.5 | 41.3 | 55.0 | 61.9 | 68.8 | 82.5 | 96.2 | 110.0 | 123.8 |
| Gunweld-70 | 155 | 12.9 | 25.8 | 38.8 | 51.7 | 58.1 | 64.6 | 77.5 | 90.4 | 103.3 | 116.3 |
| Gunweld-50 | 140 | 11.7 | 23.3 | 35.0 | 46.7 | 52.5 | 58.3 | 70.0 | 81.7 | 93.3 | 105.0 |
| Hydrocrete | 120 | 10.0 | 20.0 | 30.0 | 40.0 | 45.0 | 50.0 | 60.0 | 70.0 | 80.0 | 90.0 |
| Hydroset | 125 | 10.4 | 20.8 | 31.3 | 41.7 | 46.9 | 52.1 | 62.5 | 72.9 | 83.3 | 93.8 |
| Kast-O-Lite 30 | 90 | 7.5 | 15.0 | 22.5 | 30.0 | 33.8 | 37.5 | 45.0 | 52.5 | 60.0 | 67.5 |
| Kast-O-Lite 30 GR | 97 | 8.1 | 16.2 | 24.3 | 32.3 | 36.4 | 40.4 | 48.5 | 56.6 | 64.7 | 72.8 |
| Kast-O-Lite 25 | 82 | 6.8 | 13.7 | 20.5 | 27.3 | 30.8 | 34.2 | 41.0 | 47.8 | 54.7 | 61.5 |
| Kast-O-Lite 25 GR (Gunned) | 92 | 7.7 | 15.3 | 23.0 | 30.7 | 34.5 | 38.3 | 46.0 | 53.7 | 61.3 | 69.0 |
| Kast-Set | 115 | 9.6 | 19.2 | 28.8 | 38.3 | 43.1 | 47.9 | 57.5 | 67.1 | 76.7 | 86.3 |
| Kruzite Castable | 150 | 12.5 | 25.0 | 37.5 | 50.0 | 56.3 | 62.5 | 75.0 | 87.5 | 100.0 | 112.5 |
| KS-4 (Gunned) | 121 | 10.1 | 20.2 | 30.3 | 40.3 | 45.4 | 50.4 | 60.5 | 70.6 | 80.7 | 90.8 |
| KS-4 | 118 | 9.8 | 19.7 | 29.5 | 39.3 | 44.3 | 49.2 | 59.0 | 68.8 | 78.7 | 88.5 |
| KS-4V (Gunned) | 125 | 10.4 | 20.8 | 31.3 | 41.7 | 46.9 | 52.1 | 62.5 | 72.9 | 83.3 | 93.8 |
| KS-4V | 122 | 10.2 | 20.3 | 30.5 | 40.7 | 45.8 | 50.8 | 61.0 | 71.2 | 81.3 | 91.5 |
| Lo-Abrade | 132 | 11.0 | 22.0 | 33.0 | 44.0 | 49.5 | 55.0 | 66.0 | 77.0 | 88.0 | 99.0 |
| Lo-Abrade GR | 130 | 10.8 | 21.7 | 32.5 | 43.3 | 48.8 | 54.2 | 65.0 | 75.8 | 86.7 | 97.5 |
| MC-22 | 128 | 10.7 | 21.3 | 32.0 | 42.7 | 48.0 | 53.3 | 64.0 | 74.7 | 85.3 | 96.0 |
| MC-25 | 125 | 10.4 | 20.8 | 31.3 | 41.7 | 46.9 | 52.1 | 62.5 | 72.9 | 83.3 | 93.8 |
| MC-30 | 145 | 12.1 | 24.2 | 36.3 | 48.3 | 54.4 | 60.4 | 72.5 | 84.6 | 96.7 | 108.8 |
| Mizzou Castable | 140 | 11.7 | 23.3 | 35.0 | 46.7 | 52.5 | 58.3 | 70.0 | 81.7 | 93.3 | 105.0 |
| Mizzou GR | 140 | 11.7 | 23.3 | 35.0 | 46.7 | 52.5 | 58.3 | 70.0 | 81.7 | 93.3 | 105.0 |
| Petrocrete-ER | 130 | 10.8 | 21.7 | 32.5 | 43.3 | 48.8 | 54.2 | 65.0 | 75.8 | 86.7 | 97.5 |
| SK-7 | 44 | 3.7 | 7.4 | 11.0 | 14.7 | 16.5 | 18.4 | 22.0 | 25.7 | 29.4 | 33.0 |
| SK-7 (Gunned) | 55 | 4.6 | 9.2 | 13.8 | 18.3 | 20.6 | 22.9 | 27.5 | 32.1 | 36.7 | 41.3 |
| Steelkon | 133 | 11.1 | 22.2 | 33.3 | 44.3 | 49.9 | 55.4 | 66.5 | 77.6 | 88.7 | 99.8 |
| Steelkon BF (Gunned) | 133 | 11.1 | 22.2 | 33.3 | 44.3 | 49.9 | 55.4 | 66.5 | 77.6 | 88.7 | 99.8 |
| Steelkon GR | 130 | 10.8 | 21.7 | 32.5 | 43.3 | 48.8 | 54.2 | 65.0 | 75.8 | 86.7 | 97.5 |
| Steel Plant Castable A | 144 | 12.0 | 24.0 | 36.0 | 48.0 | 54.0 | 60.0 | 72.0 | 84.0 | 96.0 | 108.0 |
| Steel Plant Castable B | 122 | 10.2 | 20.3 | 30.5 | 40.7 | 45.8 | 50.8 | 61.0 | 71.2 | 81.3 | 91.5 |
| Super Kast-Set | 122 | 10.2 | 20.3 | 30.5 | 40.7 | 45.8 | 50.8 | 61.0 | 71.2 | 81.3 | 91.5 |
| VSL-50 | 50 | 4.2 | 8.3 | 12.5 | 16.7 | 18.8 | 20.8 | 25.0 | 29.2 | 33.3 | 37.5 |
| VSL-50 (Gunned) | 57 | 4.8 | 9.5 | 14.3 | 19.0 | 21.4 | 23.8 | 28.5 | 33.3 | 38.0 | 42.8 |

Check: each cell should equal lbs/ft³ × thickness ÷ 12. All cells agree to rounding except: SK-7 2" 7.4, 5" 18.4, 8" 29.4 (44×t/12 gives 7.33, 18.33, 29.33) — printed as read.

Footer: "Page 204"

### p.205

**PLASTICS** (See pages 48 to 58 for specific product information.)

POUNDS OF MATERIAL REQUIRED PER SQUARE FOOT OF WALL THICKNESS — NET

| Product | Lbs. Reqd. Per Cubic Foot - Net | 1" Wall | 2" Wall | 3" Wall | 4" Wall | 4½" Wall | 5" Wall | 6" Wall | 7" Wall | 8" Wall | 9" Wall |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Graphpak | 165 | 13.7 | 27.5 | 41.3 | 55.0 | 61.9 | 68.8 | 82.5 | 96.2 | 110.0 | 123.8 |
| Greenpak-85-P | 185 | 15.4 | 30.8 | 46.3 | 61.7 | 69.4 | 77.1 | 92.5 | 107.9 | 123.3 | 138.8 |
| Greenpak-85-PF | 185 | 15.4 | 30.8 | 46.3 | 61.7 | 69.4 | 77.1 | 92.5 | 107.9 | 123.3 | 138.8 |
| Greenpak-90-P | 195 | 16.3 | 32.5 | 48.8 | 65.0 | 73.1 | 81.3 | 97.5 | 113.8 | 130.0 | 146.3 |
| Greenpak-90-PF | 185 | 15.4 | 30.8 | 46.3 | 61.7 | 69.4 | 77.1 | 92.5 | 107.9 | 123.3 | 138.8 |
| Greenpak-80 | 175 | 14.6 | 29.2 | 43.8 | 58.3 | 65.6 | 72.9 | 87.5 | 102.1 | 116.7 | 131.3 |
| Green P.C. | 210 | 17.5 | 35.0 | 52.5 | 70.0 | 78.8 | 87.5 | 105.0 | 122.5 | 140.0 | 157.5 |
| Green-X | 140 | 11.7 | 23.3 | 35.0 | 46.7 | 52.5 | 58.3 | 70.0 | 81.7 | 93.3 | 105.0 |
| High Alumina Plastic | 165 | 13.7 | 27.5 | 41.2 | 55.0 | 61.9 | 68.7 | 82.5 | 96.2 | 110.0 | 123.8 |
| Jade Pak-88-P | 200 | 16.7 | 33.3 | 50.0 | 66.7 | 75.0 | 83.3 | 100.0 | 116.7 | 133.3 | 150.0 |
| Metalkleen | 150 | 12.5 | 25.0 | 37.5 | 50.0 | 56.3 | 62.5 | 75.0 | 87.5 | 100.0 | 112.5 |
| Quik-Pak | 140 | 11.7 | 23.3 | 35.0 | 46.7 | 52.5 | 58.3 | 70.0 | 81.7 | 93.3 | 105.0 |
| Red-X | 138 | 11.5 | 23.0 | 34.5 | 46.0 | 51.8 | 57.5 | 69.0 | 80.5 | 92.0 | 103.5 |
| Super Fire Wall | 142 | 11.8 | 23.7 | 35.5 | 47.3 | 53.3 | 59.2 | 71.0 | 82.8 | 94.7 | 106.5 |
| Super G | 148 | 12.3 | 24.7 | 37.0 | 49.3 | 55.5 | 61.7 | 74.0 | 86.3 | 98.7 | 111.8 |
| Super H | 145 | 12.1 | 24.2 | 36.3 | 48.3 | 54.4 | 60.4 | 72.5 | 84.6 | 96.7 | 108.8 |
| Super Hybond | 145 | 12.1 | 24.2 | 36.3 | 48.3 | 54.4 | 60.4 | 72.5 | 84.6 | 96.7 | 108.8 |
| Super Plastic | 145 | 12.1 | 24.2 | 36.3 | 48.3 | 54.4 | 60.4 | 72.5 | 84.6 | 96.7 | 108.8 |
| Val-Pak | 135 | 11.3 | 22.5 | 33.8 | 45.0 | 50.6 | 56.3 | 67.5 | 78.8 | 90.0 | 101.3 |

Check: all cells agree with lbs/ft³ × t ÷ 12 except Super G 9" printed 111.8 (148×9/12 = 111.0) — printed as read [?read: 111.0 or 111.8].

**RAMMING MIXES** (See page 83 for specific product information.)

| Product | Lbs. Reqd. Per Cubic Foot - Net | 1" Wall | 2" Wall | 3" Wall | 4" Wall | 4½" Wall | 5" Wall | 6" Wall | 7" Wall | 8" Wall | 9" Wall |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Daubpax-wet | 140 | 11.7 | 23.3 | 35.0 | 46.7 | 52.5 | 58.3 | 70.0 | 81.7 | 93.3 | 105.0 |
| Graphram | 175 | 14.6 | 29.2 | 43.8 | 58.3 | 65.6 | 72.9 | 87.5 | 102.1 | 116.7 | 131.3 |
| Greenram-80 | 172 | 14.3 | 28.7 | 43.0 | 57.3 | 64.5 | 71.7 | 86.0 | 100.3 | 114.7 | 129.0 |
| Greenram-87 W | 205 | 17.1 | 34.2 | 51.3 | 68.3 | 76.9 | 85.4 | 102.5 | 119.6 | 136.7 | 153.8 |
| Greenram-90-W | 193 | 16.1 | 32.2 | 48.3 | 64.3 | 72.4 | 80.4 | 96.5 | 112.6 | 128.7 | 144.8 |
| Greenram-SC | 155 | 12.9 | 25.8 | 38.8 | 51.7 | 58.1 | 64.6 | 77.5 | 90.4 | 103.3 | 116.5 |
| Greenram-Z-P | 220 | 18.3 | 36.7 | 55.0 | 73.3 | 82.5 | 91.7 | 110.0 | 128.4 | 146.7 | 165.0 |
| Greenram-MA | 170 | 14.2 | 28.3 | 42.5 | 56.7 | 63.8 | 70.8 | 85.0 | 99.2 | 113.3 | 127.5 |
| Green Ram Super | 172 | 14.3 | 28.7 | 43.0 | 57.3 | 64.5 | 71.7 | 86.0 | 100.3 | 114.7 | 129.0 |

Check: all cells agree except Greenram-SC 9" printed 116.5 (155×9/12 = 116.25) and Greenram-Z-P 7" printed 128.4 (220×7/12 = 128.33) — small rounding differences, printed as read.

**FORMULAS**

- CIRCLE: Circumference = Diameter × 3.1416
  - Area = Radius² × 3.1416
  - or = Diameter² × .7854
- TRIANGLE: Area = ½ base × perpendicular height.
- CYLINDER: Volume = area of section × length.
- CONE OR PYRAMID: Volume = area of base × ⅓ perpendicular height.
- FRUSTUM OF A CONE: Volume = .2618 × perpendicular height × [large diameter² + small diameter² + product of large and small diameters.]
- ARCHES:
  - Radius = Span² / (8 × Rise) + Rise / 2
  - Rise = Radius − √( Radius² − (Span / 2)² )
  - Rise = Radius − (Cosine ½ central angle × radius).

Footer: "Page 205"

## Image (57).jpg — catalogue p.206–207

(Scan rotated 90°; two facing pages.)

### p.206 — Arch Constants

Diagram of a sprung arch labelled THICKNESS, RISE, SPAN, INSIDE RADIUS (radius lines drawn to the centre of the circle).

| Rise In Inches Per Foot of Span | Inside Radius | Part of Circle |
|---|---|---|
| 1" | Span × 1.5417 | 0.1051 |
| 1¼" | Span × 1.2521 | 0.1308 |
| 1½" | Span × 1.0625 | 0.1560 |
| 1.608" | Span × 1.0000 | 0.1667 |
| 1¾" | Span × 0.9301 | 0.1807 |
| 2" | Span × 0.8333 | 0.2048 |
| 2¼" | Span × 0.7604 | 0.2284 |
| 2.302" | Span × 0.7474 | 0.2333 |
| 2½" | Span × 0.7042 | 0.2513 |
| 2¾" | Span × 0.6600 | 0.2736 |
| 3" | Span × 0.6250 | 0.2952 |

**HOW TO USE ARCH CONSTANT TABLE**

Example: Given an arch, 9" in thickness, with 10'-0" span, and 17½" rise.

Then, the rise in inches per foot of span = 17.5 / 10 = 1.75" per foot.

To find radius:

    Radius   = Span × 0.9301 (from table)
             = 120" × 0.9301
             = 111.6" = 9'-3½"
    Diameter = 223.2" = 18'-7"

To find number of brick for each course in arch:

"Use the wedge brick table showing the number of brick for a complete circle, using the inside *diameter* as figured above, and multiply by the factor shown under "Part of Circle" in the arch constant table. (In this example, 0.1807)"

"From the brick table showing 9" No. 1-X Wedges and 9" Straights (Page 132), we find it requires to turn an 18'-7" inside diameter circle, approximately 227 — 9" No. 1-X Wedges and 76 — 9" Straights."

Then, each course in the arch requires:

    227 × 0.1807 = 41 — 9" No. 1-X Wedges
     76 × 0.1807 = 14 — 9" Straights

"The same principle will apply in figuring arches of 4½" thickness using 9x4½x2½" arch brick tables, or in figuring arches of 13½" thickness using the 13½x6" wedge brick tables."

Arithmetic check: 120 × 0.9301 = 111.6 ✓; 227 × 0.1807 = 41.0 ✓; 76 × 0.1807 = 13.7 → 14 ✓. (Part of Circle = central angle ÷ 360°: 0.1667 = 60°, 0.2048 ≈ 73.7° (the "74°" tables), 0.2333 = 84°.)

Footer: "Page 206"

### p.207 — Temperature Equivalent of Pyrometric Cones

"The test for Pyrometric Cone Equivalent (P.C.E.) is the oldest and most widely used test for fire-clay refractories. By means of this test, the comparative fusion point of a refractory material is determined by comparison with Standard Pyrometric Cones having known fusion properties. Standard Pyrometric Cones are available in a wide range of temperature equivalents. They are made according to a definite formula and, when heated in a furnace operated under proper conditions at the correct rate, will bend at a definite temperature."

"Shown below are the approximate temperature equivalents corresponding to the end points of those Standard Pyrometric Cones (P.C.E.) that are used in connection with refractory testing in accordance with A.S.T.M. Method C24."

| Cone Number | End Point Degree F. | End Point Degree C. |
|---|---|---|
| 12 | 2439 | 1337 |
| 13 | 2460 | 1349 |
| 14 | 2548 | 1398 |
| 15 | 2606 | 1430 |
| 16 | 2716 | 1491 |
| 17 | 2754 | 1512 |
| 18 | 2772 | 1522 |
| 19 | 2806 | 1541 |
| 20 | 2847 | 1564 |
| 23 | 2921 | 1605 |
| 26 | 2950 | 1621 |
| 27 | 2984 | 1640 |
| 28 | 2995 | 1646 |
| 29 | 3018 | 1659 |
| 30 | 3029 | 1665 |
| 31 | 3061 | 1683 |
| 31½ | 3090 | 1699 |
| 32 | 3123 | 1717 |
| 32½ | 3135 | 1724 |
| 33 | 3169 | 1743 |
| 34 | 3205 | 1763 |
| 35 | 3245 | 1785 |
| 36 | 3279 | 1804 |
| 37 | 3308 | 1820 |
| 38 | 3335 | 1835 |
| 39 | 3389 | 1865 |
| 40 | 3425 | 1885 |
| 41 | 3578 | 1970 |
| 42 | 3659 | 2015 |

"Cones 28 and 30 are shown above as information only. They are manufactured and used in special applications in industry but are not used in the P.C.E. test as specified by A.S.T.M. Method C24."

"Heating Rate: Cones 12 to 37, incl.: 150° C. per hr.; Cone 38: 100° C. per hr.; Cones 39 to 42, incl.: 600° C. per hr."

Footer: "Page 207"


## Image (58).jpg — catalogue p.222–223 (INDEX)

(Scan rotated 90°. This index belongs to the full A.P. Green catalogue/handbook, not only the brick-shapes section; it is useful for locating pages. Indented entries are sub-entries of the line above. Page references as printed.)

### p.222 — INDEX

- 68-B . . . 38
- 80 ALUMINA . . . 15, 18
- 90-B . . . 19, 23
- 99-AD . . . 19, 23

**a**

- A-1 . . . 26
- Acid Resistant Brick . . . 35
- ACTO . . . 9
- Advantages of Castables . . . 60
- Advantages of Plastics . . . 49
- Allied Products . . . 92
- Alloy Anchors . . . 85
- Alumina Mortars . . . 41, 44, 45
- Alumina Ramming Mixes . . . 82
- Anchorage Systems . . . 85, 86
- **A. P. Green Refractories Co.** . . . 4
  - Manufacturing Facilities . . . 7
  - Product Development . . . 5
  - Quality Control . . . 5
  - Research . . . 5
- **A. P. Green Services, Inc.** . . . 6
- ARC-HARD D . . . 36
- Arch Constants . . . 206
- ATLANTIC FIRST . . . 11
- ATMOSET . . . 41

**b**

- Baffle Brick, Oil Burner . . . 93
- Basic Brick . . . 29-32
- Basic Castables . . . 74
- Basic Mortars . . . 41, 46
- Basic Ramming Mixes . . . 83
- Basic Refractories . . . 28-32
- BIG CHIEF . . . 15, 16
- Blast Furnace Bottom Blocks . . . 163
- Blast Furnace Keys . . . 107
- Block Insulation . . . 88
- Blocks, Car . . . 39
  - CTX . . . 39
  - SKC . . . 39
- Blocks, Cupola . . . 102, 103
- Blocks, Nose . . . 38
- Blocks, Rear Arch . . . 93
- Blocks, Rotary Kiln . . . 103
- Blow-Off Protector Tile . . . 93
- **Brick**
  - Acid . . . 35
    - C-ACID . . . 35
    - G-ACID . . . 35
  - Basic . . . 28-32
    - DELTA 1 . . . 30
    - DELTA 50 . . . 30
    - GREEN B 80 . . . 31
    - GREEN B 70 . . . 31
    - GREEN-OX . . . 32
  - Checker Brick . . . 37
  - Extra High Alumina (85-99%) . . . 19-23
    - 85%—DV . . . 19, 20
    - 85%—DV-38 . . . 19, 21
    - 85%—DV-38-P . . . 19, 20
    - 90% GREENAL-90 . . . 19, 22
    - 94% GREENAL-94 . . . 19, 22
    - 99%—99-AD . . . 19, 23
  - High Alumina (50-80%) . . . 15-18
    - 50%—BIG CHIEF . . . 15, 16
    - 60%—MIZZOU . . . 15, 16
    - 70%—KRUZITE D . . . 15, 17
    - 70%—KRUZITE R . . . 15, 17
    - 75%—DV-75-P . . . 15, 18
    - 80%—80 ALUMINA . . . 15, 18
  - High Duty . . . 10, 11
    - ATLANTIC FIRST . . . 11
    - CHAMPION . . . 11
    - CLIMAX . . . 11
    - EMPIRE . . . 11
    - EMPIRE BF . . . 11
    - EMPIRE STOVE . . . 11
    - EMPIRE S . . . 11

Footer: "Page 222"

### p.223 (index continued)

  - (High Duty, continued)
    - EMPIRE W . . . 11
    - HOT ZONE . . . 11
    - IDAHO . . . 11
    - MONARC . . . 11
    - PCP . . . 11
    - PYRO STEEL . . . 11
    - S-1 . . . 11
  - Insulating . . . 33, 34
    - GREENLITE . . . 33, 34
    - XSILITE . . . 35
  - Ladle Brick . . . 37
  - Low Duty . . . 9
    - ACTO . . . 9
    - KIMBERLY . . . 9
  - Medium Duty . . . 9
    - DIXIE . . . 9
    - D-SAVAGE . . . 9
    - LONE STAR . . . 9
    - MORRIS . . . 9
    - PAR . . . 9
  - Mullite . . . 25
    - CRYSTALITE . . . 25
    - CRYSTALITE A . . . 25
    - MUL-8 . . . 25
  - Pitch Bonded . . . 32
  - Semi-Mullite . . . 24
    - GREENMUL-60 . . . 24
  - Semi-Silica . . . 27
    - VALENTINE XX . . . 27
  - Silica . . . 27
    - XSIL . . . 27
    - XSIL-E . . . 27
  - Silicon Carbide . . . 26
    - A-1 . . . 26
  - Super Duty . . . 12-14
    - CLIPPER . . . 12, 13
    - KX-99 . . . 12, 14
    - KX-99-BF . . . 12, 14
    - MEX-KO . . . 12, 13
    - SDS . . . 12
    - YUKON . . . 12, 13
  - Zircon . . . 26
- Brick Combinations, Circles and Arches, Index . . . 109, 110
- BTG Marine Burner Tile . . . 37

**c**

- C-ACID . . . 35
- Car Blocks . . . 39
- Cartons, Plastic . . . 51
- CASTABLE BLOCK MIX . . . 77
- CASTABLE INSULATION NO. 20 . . . 77
- CASTABLE NO. 22 . . . 76
- CASTEX 24 C . . . 72
- CASTEX 25 C . . . 72
- CASTITE . . . 73
- **Castable Refractories** . . . 60-79
  - Advantages of Castables . . . 60
  - Anchors for Castables . . . 84, 85
  - Basic Castables . . . 74
    - GREEN CRETE ARC . . . 74
    - GREEN CRETE C STANDARD . . . 74
    - GREEN CRETE C SUPER . . . 74
  - Extra Strength Castables . . . 66, 67
    - GREENCAST-12 . . . 67
    - LO-ABRADE . . . 67
    - MC-22 . . . 66
    - MC-25 . . . 66
    - MC-30 . . . 66
    - STEELKON . . . 67
  - Extreme Temperature Castables . . . 64, 65
    - GREENCAST-94 . . . 64
    - GREENCAST-97 . . . 64
    - KRUZITE CASTABLE . . . 65
    - MIZZOU CASTABLE . . . 65
    - STEEL PLANT CASTABLE A . . . 65
  - General Purpose Castables . . . 72, 73
    - CASTEX 25 C . . . 72
    - CASTEX 24 C . . . 72
    - CASTITE . . . 73
    - HYDROCRETE . . . 73
    - HYDROSET . . . 73
    - KAST-SET . . . 73
    - STEEL PLANT CASTABLE B . . . 72
    - SUPER KAST-SET . . . 72
  - Gun Applied Castables . . . 68-71
    - GREENCAST-12 GR . . . 71
    - GREENCAST-28 GR . . . 69
    - GREENCAST-94 GR . . . 68

Footer: "Page 223"


## Image (59).jpg — catalogue p.224–225 (INDEX, continued)

(Scan rotated 90°. Indented entries are sub-entries; page references as printed.)

### p.224

- (Gun Applied Castables, continued)
  - GREENCAST-97 GR . . . 68
  - KS-4 . . . 71
  - KS-4V . . . 70
  - LO-ABRADE GR . . . 70
  - MIZZOU GR . . . 68
  - STEELKON GR . . . 69
  - STEELKON BF . . . 69
- INSULATING CASTABLES-General Purpose . . . 75-77
  - CASTABLE BLOCK MIX . . . 77
  - CASTABLE NO. 20 . . . 77
  - CASTABLE NO. 22 . . . 76
  - GREENCAST-97-L . . . 75
  - KAST-O-LITE-25 . . . 76
  - KAST-O-LITE-30 . . . 75
- INSULATING CASTABLES-Gun Applied . . . 78, 79
  - GREENCAST-22-L GR . . . 79
  - GREENCAST-97-L GR . . . 78
  - KAST-O-LITE 30 GR . . . 78
  - SK-7 . . . 79
  - VSL-50 . . . 79
- Selection Chart . . . 61-63
- Castables, Estimating Data . . . 204
- **Cement**
  - High Temparature [sic] . . . 41, 46
  - INSULATING CEMENT . . . 89
- CHAMPION . . . 11
- Checker Brick-Blast Furnace Stove . . . 37
- Chrome Brick . . . 28-32
- Chrome Castables . . . 74
- Chrome Mortars . . . 41, 46
- Chrome Plastic . . . 58
- Circle Brick . . . 102
- Circumferences & Areas of Circles . . . 210-213
- CLIMAX . . . 11
- CLIPPER . . . 12, 13
- **Coatings**
  - GREENCOTE . . . 82
- Combinations for Circles and Arches, Index . . . 109, 110
- Combustion Chambers . . . 90-92
  - Allied Products . . . 93
  - PERFECTO . . . 91
  - STANDARD I.F.B. . . . 92
  - STREAMLINED . . . 90
- Conversion Factors . . . 214, 215
  - Area, Length, Volume, Velocity . . . 214
  - Heat, Energy, Power-Pressure-Thermal Conductivity-Weight, Bulk Density . . . 215
- Conversion Tables, Temperature . . . 208, 209
- CRYSTALITE . . . 25
- CRYSTALITE A . . . 25
- CTX . . . 39
- Cupola Blocks . . . 102, 103

**d**

- DAUBPAX . . . 82
- Decimal Equivalent of Fractions . . . 216
- Decimals of a Foot . . . 217
- DELTA 1 . . . 30
- DELTA 50 . . . 30
- DIXIE . . . 9
- D-SAVAGE . . . 9
- Door Jamb Brick . . . 105
- DV . . . 19, 20
- DV-38-P . . . 19, 20
- DV-38 . . . 19, 21
- DV-75-P . . . 15, 18

**e**

- EMPIRE . . . 11
- EMPIRE BF . . . 11
- EMPIRE STOVE . . . 11
- EMPIRE S . . . 11
- EMPIRE W . . . 11
- Engineering Tables, Index . . . 109, 110
- **Estimating Data** . . . **204, 205**
  - Castables . . . 204
  - Firebrick . . . 202, 203
  - Mortars . . . 41, 202
  - Plastics . . . 205
  - Ramming Mixes . . . 205
- Extra High Alumina Brick . . . 19-23
- Extra Strength Castables . . . 66, 67
- Extreme Temperature Castables . . . 64, 65
- Extruded Plastic Block . . . 49, 58

Footer: "Page 224"

### p.225

**f**

- Firebrick
  - Estimating Data . . . 202, 203
- Firebrick Shapes . . . 95-103
- Fireclay Brick (see Brick)
- Formulas . . . 205
- Furnace Accessories . . . 85-93

**g**

- G-20, G-23, G-26 . . . 33
- G-ACID Brick . . . 35
- General Purpose Castables . . . 72, 73
- Graphite Plastics . . . 56, 57
- GRAPHPAK . . . 57
- GRAPHRAM . . . 83
- GREENAL-90 . . . 19, 22
- GREENAL-94 . . . 19, 22
- GREEN B-80 . . . 31
- GREEN B 70 . . . 31
- GREENCAST-12 . . . 67
- GREENCAST-12 GR . . . 71
- GREENCAST-22-L GR . . . 79
- GREENCAST-28 GR . . . 69
- GREENCAST-94 . . . 64
- GREENCAST-94 GR . . . 68
- GREENCAST-97 . . . 64
- GREENCAST-97 GR . . . 68
- GREENCAST-97-L . . . 75
- GREENCAST-97-L GR . . . 78
- GREEN CHROME MORTAR . . . 41, 46
- GREENCLAD DOOR JAMB BRICK . . . 105
- GREENCOTE . . . 82
- GREEN CRETE ARC . . . 74
- GREEN CRETE C STANDARD . . . 74
- GREEN CRETE C SUPER . . . 74
- GREENLITE-28,-33,-KL . . . 33, 34
- GREEN MAGNESITE MORTAR . . . 41, 46
- GREENMUL-60 . . . 24
- GREEN-OX . . . 32
- GREENPAK-80 . . . 49, 53
- GREENPAK-85-P . . . 49, 53
- GREENPAK-85-PF . . . 49, 54
- GREENPAK-90-P . . . 49, 54
- GREENPAK-90-PF . . . 49, 55
- GREENRAM-80 . . . 83
- GREENRAM-87-W . . . 83
- GREENRAM-90-W . . . 83
- GREENRAM-MA . . . 83
- GREENRAM-SC . . . 83
- GREENRAM-Z-P . . . 83
- GREENRAM SUPER . . . 83
- GREENSET-78 . . . 41
- GREENSET-85-P . . . 41
- GREENSET-90 . . . 41
- GREEN TARAM-60 . . . 83
- GREEN-X . . . 49, 56
- Gun Applied Castables . . . 68-71
- Gun Mixes . . . 80-82
  - GUNPATCH . . . 82
  - GUNWELD . . . 80
  - PETROCRETE-ER . . . 81
- Gun, PERFECTO Spray . . . 83

**h**

- HEATITE . . . 41-43
- High Alumina Brick . . . 15-18
- HIGH ALUMINA PLASTIC . . . 49, 52
- High Duty Brick . . . 10, 11
- HOT ZONE . . . 11
- HYDROCRETE . . . 73
- HYDROSET . . . 73

**i**

- IDAHO . . . 11
- Index to Engineering Tables . . . 109, 110
- **Industrial Insulations** . . . 87-89
  - INSBLANKET . . . 87
  - INSBLOK-19 . . . 88
  - INSBLOK-12 . . . 88
  - INSFELT . . . 87
  - INSPAPER . . . 87
  - INSROPE . . . 87
  - INSULATING CEMENT . . . 89

Footer: "Page 225"


## Image (60).jpg — catalogue p.226–227 (INDEX, continued)

(Scan rotated 90°. Indented entries are sub-entries; page references as printed.)

### p.226

- (Industrial Insulations, continued)
  - INSWOOL . . . 87
  - LOOSE WOOL INSULATION . . . 89
- Inert Supports . . . 38
- INSBLOK-19 . . . 88
- INSBLOK-12 . . . 88
- Installation Service . . . 6
- INSFIBER . . . 87
- **Insulating Castables** . . . 66-79 [as printed]
  - General Purpose . . . 66, 77 [as printed]
  - Gun Applied . . . 78, 79
- INSULATING CEMENT . . . 89
- Insulating Firebrick . . . 33, 34
- INSWOOL . . . 87
- Isostatically Pressed . . . 36

**j**

- JADE PAK-88-P . . . 49, 55

**k**

- KAST-O-LITE 25 . . . 76
- KAST-O-LITE-30 . . . 75
- KAST-O-LITE 30 GR . . . 78
- KAST-SET . . . 73
- KD-2 . . . 41, 44
- Kiln Furniture . . . 38
- Kiln Blocks, Rotary . . . 103
- KIMBERLY . . . 9
- KRUZITE CASTABLE . . . 65
- KRUZITE D . . . 15, 17
- KRUZITE R . . . 15, 17
- KS-4 . . . 71
- KS-4V . . . 70
- KX-99 . . . 12, 14
- KX-99-BF . . . 12, 14

**l**

- Ladle Brick . . . 37
- LO-ABRADE . . . 67
- LO-ABRADE GR . . . 70
- LONE STAR . . . 9
- Loose Wool Insulation . . . 89
- Low Brick Duty [as printed] . . . 9
- LOXOL-65 . . . 41, 43

**m**

- Manufacturing Plants . . . 229
- Magnesia Ramming Mixes . . . 82
- Magnesite Brick . . . 28, 32
- Magnesite Mortars . . . 41, 46
- Manufacturing Facilities . . . 7
- Marine Burner Tile . . . 36
- MC-22 . . . 66
- MC-25 . . . 66
- MC-30 . . . 66
- Medium Duty Brick . . . 9
- Metal-Encased Brick . . . 30, 31
- METALKLEEN . . . 49, 57
- MEX-KO . . . 12, 13
- MEXI-KOMO . . . 41, 45
- Milled Fireclay . . . 45
- Millimeters to Inches—Table . . . 218-221
- MIZZOU . . . 15, 16
- MIZZOU CASTABLE . . . 65
- MIZZOU GR . . . 68
- **Mortars** . . . 41-46
  - Alumina
    - GREENSET-78 . . . 41
    - GREENSET-85-P . . . 41
    - GREENSET-90 . . . 41
    - LOXOL-65 . . . 41, 43
    - No. 36 REFRACTORY CEMENT . . . 41, 44
    - No. T-36 REFRACTORY CEMENT . . . 41, 44
    - SATANITE . . . 41, 45
  - Chrome
    - GREEN CHROME MORTAR . . . 41, 46
  - Fireclay
    - HEATITE . . . 41, 43
    - KD-2 . . . 41, 44
    - MEXI-KOMO . . . 41, 45
    - Milled Fire Clay . . . 45
    - 'SAIRBOND . . . 41, 43
    - 'SAIRMIX-7 . . . 41, 42
    - 'SAIRSET . . . 41, 42

Footer: "Page 226"

### p.227

- (Mortars, continued)
  - Magnesite
    - GREEN MAGNESITE MORTAR . . . 41, 46
  - Silica-Fireclay
    - ATMOSET . . . 41
- MONARC . . . 11
- MORRIS . . . 9
- Mortars, Estimating Data . . . 41, 202
- MUL-8 . . . 25
- Mullite Brick . . . 25
- Mullite Mortars . . . 41

**n**

- No. 36 REFRACTORY CEMENT . . . 41, 44
- No. T-36 REFRACTORY CEMENT . . . 41, 44
- Nose Blocks . . . 38

**o**

- Observation Port . . . 93
- Oil Burner Baffle Brick . . . 93
- Oil Burner Combustion Chambers . . . 89, 91

**p**

- PAR . . . 9
- PCP . . . 11
- PERFECTO Blow-Off Tile . . . 93
- PERFECTO Combustion Chamber . . . 91
- PERFECTO Observation Port . . . 93
- PERFECTO Rear Arch Block . . . 93
- PERFECTO Spray Gun . . . 93
- PETROCRETE-ER . . . 81
- PLANT LOCATIONS . . . 229
- **Plastic Refractories** . . . 48-58
  - Anchors for Plastics . . . 85
  - Extruded Plastic Block . . . 49, 58
  - GRAPHPAK . . . 49, 57
  - GREENPAK-80 . . . 49, 53
  - GREENPAK-85-P . . . 49, 53
  - GREENPAK-85-PF . . . 49, 54
  - GREENPAK-90-P . . . 49, 54
  - GREENPAK-90-PF . . . 49, 55
  - GREEN-X . . . 49, 56
  - HIGH ALUMINA PLASTIC . . . 49, 52
  - JADE PAK-88-P . . . 49, 55
  - METALKLEEN . . . 49, 57
  - QUIK-PAK . . . 49, 50
  - RED-X . . . 49, 56
  - SUPER FIRE WALL . . . 49
  - SUPER G . . . 49, 52
  - SUPER H . . . 49, 51
  - SUPER HYBOND . . . 49, 51
  - SUPER PLASTIC . . . 49, 50
  - VAL-PAK . . . 49, 58
- Plastics, Estimating Data . . . 205
- Plastics, Packaging . . . 48
- Product Development . . . 5
- Pyrometric Cones . . . 207
- PYRO STEEL . . . 11

**q**

- Quality Control . . . 5
- QUIK-PAK . . . 49, 50

**r**

- Ramming Mixes . . . 83
- Ramming Mixes, Estimating Data . . . 205
- Rear Arch Blocks . . . 93
- RED-X . . . 49, 56
- Refractory Anchors . . . 85, 86
- Research . . . 5
- Rotary Kiln Blocks . . . 103

**s**

- S-1 . . . 11
- 'SAIRBOND . . . 41, 43
- 'SAIRMIX-7 . . . 41, 42

Footer: "Page 227"


## Image (61).jpg — catalogue p.228–229 (INDEX end; Warehouse Stocks; Plant Locations)

(Scan rotated 90°.)

### p.228 (index, continued)

- 'SAIRSET . . . 41, 42
- SATANITE . . . 41, 45
- SDS . . . 12
- Selection Chart-Castables . . . 61-63
- Selection Chart-Mortars . . . 41
- Selection Chart-Ramming Mixes . . . 83
- Semi-Mullite . . . 24
- Semi-Silica Brick . . . 27
- Shiplap Tile . . . 101
- Silica Brick . . . 27
- Silica Brick-Insulating . . . 35
- Siliceous Gunning Mix . . . 82
- Siliceous Ramming Mix . . . 83
- Silicon Carbide Brick . . . 26
- Silicon Carbide Mortars . . . 41
- Silicon Carbide Ramming Mix . . . 83
- SK-7 . . . 79
- SKC . . . 39
- Skews . . . 106
- **Special Blocks** . . . 93
  - Oil Burner Baffle Brick . . . 93
  - PERFECTO Blow Off Tile . . . 93
  - PERFECTO Rear Arch Blocks . . . 93
- Special Insulating Firebrick . . . 35
- **Special Refractory Products** . . . 36-39
  - Acid Brick . . . 35
  - Ceramic Wear Liners . . . 36
  - BTG Marine Burner Tile . . . 37
  - Car Blocks . . . 39
  - Checker Brick . . . 37
  - Inert Supports . . . 38
  - Kiln Furniture . . . 38
  - Ladle Brick . . . 37
  - Nose Blocks . . . 38
- Special Shapes . . . 104-107
- Spray Gun . . . 93
- Square Edge Tile . . . 101
- STANDARD I.F.B. Combustion Chambers . . . 92
- Standard Shapes . . . 95-103
- STEELKON . . . 67
- STEELKON BF . . . 69
- STEELKON GR . . . 69
- STEEL PLANT CASTABLE A . . . 65
- STEEL PLANT CASTABLE B . . . 72
- STREAMLINED Combustion Chambers . . . 90
- Super Duty Brick . . . 12-14
- SUPER FIRE WALL . . . 49
- SUPER G . . . 49, 52
- SUPER H . . . 49, 51
- SUPER HYBOND . . . 49, 51
- SUPER KAST-SET . . . 72
- SUPER PLASTIC . . . 49, 50

**t**

- Tables, Engineering . . . 109-199
  - Index . . . 109, 110
- Tables of Useful Information . . . 204-221
- Pitch Bonded Brick . . . 32
- Temperature Conversion Table . . . 208, 209

**v**

- VALENTINE XX . . . 27
- VAL-PAK . . . 49, 58
- VSL-50 . . . 79
- VS & SS Rod Type Alloy Anchors . . . 86

**w**

- Warehouse Locations . . . 229

**x**

- XSIL . . . 27
- XSIL-E . . . 27
- XSILITE . . . 35

**y**

- YUKON . . . 12, 13

**z**

- Zircon Brick . . . 26
- Zircon Mortars . . . 41
- Zircon Ramming Mixes . . . 83

Footer: "Page 228"

### p.229 — WAREHOUSE STOCKS AND SERVICE AT . . .

- ALABAMA: Birmingham
- ALASKA: Anchorage
- ARIZONA: Tempe
- CALIFORNIA: Los Angeles, San Francisco
- COLORADO: Denver, Pueblo
- CONNECTICUT: Orange
- DISTRICT OF COLUMBIA: Washington (the word appears underlined; possibly a pen mark — [?read: printed or handwritten])
- FLORIDA: Bartow, Jacksonville
- GEORGIA: Atlanta, Macon
- ILLINOIS: Chicago, East Moline, Lansing, Peoria, Rockford
- INDIANA: Evansville, Fort Wayne
- IOWA: Des Moines
- KENTUCKY: Owensboro
- LOUISIANA: Baton Rouge, New Orleans, Shreveport
- MAINE: Bangor, Portland
- MARYLAND: Baltimore
- MASSACHUSETTS: Waltham
- MICHIGAN: Grand Rapids, Kalamazoo, Lansing, Muskegon Heights, Saginaw, Taylor
- MINNESOTA: Minneapolis
- MISSISSIPPI: Jackson
- MISSOURI: Kansas City, St. Louis
- MONTANA: Billings
- NEBRASKA: Omaha
- NEW JERSEY: Kearny, Woodbridge
- NEW YORK: Albany, Buffalo, Syracuse
- NORTH CAROLINA: Asheville, Charlotte
- OHIO: Canton, Cincinnati, Cleveland, Columbus, Massillon, Oak Hill, Toledo
- OKLAHOMA: Tulsa
- OREGON: Eugene, Medford, Portland
- PENNSYLVANIA: Erie, Harrisburg, Leetsdale, Philadelphia
- SOUTH CAROLINA: Columbia
- TENNESSEE: Knoxville, Memphis, Nashville
- TEXAS: Dallas, El Paso, Fort Worth, Houston, San Antonio, Sulphur Springs
- UTAH: Salt Lake City
- VIRGINIA: Norfolk, Richmond, Roanoke
- WASHINGTON: Pasco, Renton, Spokane
- WISCONSIN: Little Chute, Madison, Milwaukee

**PLANT LOCATIONS . . .**

Bessemer, Alabama; Eufaula, Alabama; Kimberly, Alabama; Little Rock, Arkansas; Pueblo, Colorado; Macon, Georgia; Troy, Idaho; Morris, Illinois; Taylor, Michigan; Fulton, Missouri; Mexico, Missouri; Woodbridge, New Jersey; Jackson, Ohio; Massillon, Ohio; Oak Hill, Ohio; Climax, Pennsylvania; Philadelphia, Pennsylvania; Tarentum, Pennsylvania; Freeport, Texas; Sulphur Springs, Texas.

CANADA: Weston, Ontario; Acton, Ontario; Claybank, Saskatchewan.

Footer: "Page 229"

(No edition, year or printing code is printed on any page in this batch (Images 46–61). Publisher name appears as "A. P. Green" (section title, Image 54) and "A. P. Green Refractories Co." / "A. P. Green Services, Inc." (index, p.222).)


## Summary (Images 46–61)

- **Ring/circle brick counts:** none in this batch. p.206 points to the circle table for 9" No. 1-X Wedges + 9" Straights on p.132, and the index lists "Brick Combinations, Circles and Arches, Index" at pp.109–110.
- **Sprung-arch brick per course, by span and rise (No. 3/2/1/1-X wedges + straights):**
  - pp.184–185: 9" arch, 2"/ft rise, 74°, 2½" brick. Spans 1'-6" to 14'-0". Skew brand 4160-D.
  - pp.186–187: 9" arch, 2"/ft, 74°, 3" brick. Spans 1'-10" to 14'-0". Skew 4160-D.
  - pp.188–189: 9" arch, 2.302"/ft, 84°, 2½" brick. Spans 1'-6" to 14'-0". Standard sideskews.
  - pp.190–191: 9" arch, 2.302"/ft, 84°, 3" brick. Spans 2'-0" to 14'-0". Standard sideskews.
  - pp.192–193: 12" arch, 1.608"/ft, 60°. Spans 6'-0" to 30'-0". Skew 3878-B.
  - pp.194–195: 13½" arch, 1.608"/ft, 60°. Spans 6'-0" to 30'-0". Skew 3878-C.
  - pp.196–197: 15" arch, 1.608"/ft, 60°. Spans 6'-3" to 30'-0".
  - pp.198–199: 18" arch, 1.608"/ft, 60°. Spans 8'-0" to 35'-0".
- **Arch constants (method + formulas):** p.206. A table of rise per foot against inside radius (as span × factor) and part of circle, plus a worked example.
- **Formulas:** p.205 covers the circle, triangle, cylinder, cone/pyramid and frustum. For arches it gives Radius = Span²/(8×Rise) + Rise/2, Rise = R − √(R² − (Span/2)²) and Rise = R − cos(½ central angle)×R.
- **Skewbacks:** no skew tables here. Every arch page says "See Page 106 For Skews", and the index gives Skews at p.106. Skew brands are printed on the arch pages.
- **Dome brick:** none in this batch.
- **Other data:**
  - p.202: firebrick per ft³ and per ft² of wall, and mortar per 1,000 brick.
  - p.203: firebrick per ft² for each wall type.
  - pp.204–205: lb/ft² of wall for castables, plastics and ramming mixes.
  - p.207: pyrometric cone temperatures, cones 12–42 (ASTM C24).
  - pp.222–228: index. p.229: warehouse and plant locations.
- **Edition/year:** not printed in this batch.
- **Totals mismatches:**
  - p.188, span 4'-11": 15 + 17 = 32 against a printed 31.
  - p.196, span 15'-6": 56 + 13 = 69 against a printed 70. The 1-X cell may be 14.
  - Every other arch row adds up.

