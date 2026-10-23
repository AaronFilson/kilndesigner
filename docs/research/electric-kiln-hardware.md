# Electric kiln hardware reference data

Checked: 2026-10-22. Scope: US studio electric kilns to cone 10, front-loaders first, with
top-loaders where they show the same hardware. The aim is the hardware outside the lining that
the engine must draw for a buildable kiln: case or frame, stand, door, element ends and their
boxes, spy holes, vent holes, control box, and the clearances around it all.
Every number has a source tag like [S3]. The tags are listed under "Sources" at the end.

How values are marked:
- **Verified** means I read it on the page or in the PDF text itself.
- **Excerpt** means I saw it only in a search-engine snippet or summary.
- **Derived** means I calculated it from sourced inputs. The working is shown.
- **(secondary)** means a retailer page or similar, passing on a maker's claim second-hand.
- **NOT FOUND** means I found no source. Do not fill these gaps with guesses.

Notes on the sources:
- PDFs were read as text with `pdftotext`. No PDF renderer was available, so drawings could
  not be seen. On the L&L general-dimension drawings, a dimension is given here only when its
  label follows it directly in the text (for example "50.0in ... FLOOR TO CONTROL"). That
  pairing is by text order, so it is marked "drawing, paired by text order".
- Every downloaded file was matched to its URL by byte size, except the three noted in the
  Sources list.
- Almost every number is one maker's design for named models. One maker's design is not a rule.
  The tables say which maker and which kiln each number comes from.
- Kiln makers' installation guides quote building codes (the Uniform Mechanical Code, NFPA 86,
  the NEC). Those codes were not read first-hand. Where a guide quotes one, the row says so.

Cross-references: this file adds to `electric-and-thermal.md`. It does not repeat that file's
element and wire data (§1, including Kanthal coil geometry and Krueger's 15 ga element pins in
§1.6), gauges (§2), US electrical rules and kiln-maker breaker and wire tables (§3), refractory
properties (§4), shell emissivity (§4.7) or brick sizes (§5). Gas-kiln spy holes are in
`kiln-hardware.md` §2.

---

## 1. Case, frame and stand

### 1.1 Top-loaders: stainless jacket held by bands

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Jacket material | stainless steel | Skutt KM series | Verified | [S9] |
| Jacket material | "Full stainless jackets", on most of Evenheat's shallow designs, "as opposed to a sectional design" | Evenheat ceramic kilns | Verified | [S16] |
| What holds the wall | "the bricks are held together by compression of the stainless steel jacket. The wall bricks are not cemented together" | Olympic studio line | Verified | [S17] |
| Band fastener | worm-drive screws on the back of the kiln. To change a brick, loosen them 3–4 turns at a time; tighten evenly top to bottom | Skutt (KilnParts repair guide) | Verified | [S13] |
| Band fastener | "worm-type jacket fasteners". Loosen them equally, 0.5 to 0.75 in, to slip a brick out. To make bands extra tight, heat the metal band (not the brick) with a propane torch and retighten | Skutt KM manual | Verified | [S9] |
| Band fastener | "adjustable clamps" / hose clamps on the stainless band, two or three per wrap. Tighten ¼ turn at a time on each, alternating, "so that you don't cock the stainless casing". Bands also go round the lid and the floor slab | L&L | Verified | [S8] [S1] |
| Band fastener | hose clamps; set the kiln on the stand with the clamps to the back | Olympic | Verified | [S17] |
| Lid | L&L lids use stainless steel clips to keep hairline cracks from spreading | L&L | Verified | [S8] |
| Sections | draw-pull catches between sections | Skutt KM | Verified | [S9] |
| Sections | deep Evenheat models have a "Maintenance Line": a split in the jacket held by stainless steel plates and screws | Evenheat | Verified | [S16] |
| Holes in the jacket | L&L punches the holes for peepholes and element connections in the stainless; the brick behind is drilled in the field through them | L&L | Verified | [S8] |
| Holes in the jacket | Skutt stamps a thermocouple hole in the band; Olympic punches one in the jacket | Skutt, Olympic | Verified | [S9] [S17] |
| Jacket thickness or gauge | **NOT FOUND** for any maker | | | |

### 1.2 Front-loaders: welded case or frame

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Case | "Solid welded heavy gauge (1/8") thick steel case with integrated welded stand. Feet include leveling bolts." Powder coated "hammertone blue" | L&L Easy-Load EL2436–EL3048 (bulletin EL-3-15) | Verified | [S6] |
| Case | "Stand, case, door and hinge are powder-coated hammertone blue". "Support tubing adds rigidity to welded door and hinge". "Adjustable leveling feet" | L&L EL2424, EL3048 drawings | Verified (drawing labels) | [S4] [S5] |
| Lifting | the case "is designed to be picked up by a forklift or pallet jack from the front, back or sides". Stand is wide enough for pallet jacks up to 30.5 in (EL2424) and 36.5 in (EL3048) | L&L Easy-Load | Verified | [S6] [S4] [S5] |
| Case | "Stainless steel case". Back brick "covered with galvannealed plate". "Steel is powder-coated hammertone blue". "Welded door frame". "Adjustable tension brackets" | L&L eFL1626 drawing | Verified (drawing labels) | [S2] |
| Legs | "Heavy-duty 11 ga legs and brackets come disassembled but install quickly". Legs and leg cross-supports bolt on; the base metal has slots for a forklift | L&L eFL | Verified | [S2] [S1] |
| Floor fixing | without casters, the caster-mount brackets "become floor-mount brackets and have holes for anchoring to the floor" | L&L eFL | Verified | [S1] |
| Frame | the door hinge is fastened to a 2 in tubular steel frame running from the floor to the top of the kiln | Paragon Super Dragon (retailer listing) | Excerpt (secondary) | [S19] |
| Angle or tube sizes for a site-built front-loader frame | **NOT FOUND** | | | |

The gauge-to-thickness table for sheet steel is not in the repo, so "11 ga" is not converted
here. (`electric-and-thermal.md` §2 is the AWG wire gauge, which is a different scale.)

### 1.3 Stand

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Stand height | "L&L stands typically raise the floor of the kiln by 8" (20 cm)". A rolling stand keeps 8 in only with its casters on | L&L | Verified | [S1] |
| Stand height | "Nearly every Skutt kiln uses a 8" high stand". The EnviroVent 2 is designed to fit under it | Skutt | Verified | [S11] |
| Stand height for a vent | "Ensure that kiln stand is a minimum of eight (8) inches high" | Skutt CSI specification | Verified | [S10] |
| Why a stand | "Never set a kiln on a floor without significant air space circulating under the kiln"; the air space stops heat being conducted to the floor | L&L; Olympic (same reason) | Verified | [S1] [S17] |
| Hearth height | "Approximately 30" for EL2436 and 18" for all other models" | L&L Easy-Load | Verified | [S6] |
| Floor to control | 50.0 in | L&L eFL1626 | Verified (drawing, paired by text order) | [S2] |
| Floor to control | 45.5 in | L&L EL2424 | Verified (drawing, paired by text order) | [S4] |
| Rolling stand | 14 ga galvannealed steel; 22.5 × 22.8 in (8-sided kiln), 28.8 × 30 in (10-sided), 34.3 × 34 in (12-sided); same height as the normal stands | L&L top-loaders | Verified | [S3] |
| Levelling | thin metal shims under the legs, never wood | L&L; Evenheat; Olympic ("sheet metal") | Verified | [S1] [S16] [S17] |
| Levelling | do not shim between the stand and the slab | Skutt | Verified | [S9] |
| Tip-over | UL 499 9.2: the appliance must not overturn on a 10° incline. Exception 2: an appliance "intended to be mounted to a supporting surface such as the floor" need not be tested | UL 499 | Verified | [S21] |

---

## 2. Door (front-loaders)

### 2.1 Hinge

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Side | "Heavy-duty door hinges to the left (special option allows it to be hinged on the right). Door opens all the way so that the door opening is completely unobstructed." | L&L Easy-Load | Verified | [S6] |
| Bearings | "The door has thrust bearings to make it easy to open. It is adjustable so that you can maintain a proper seal" | L&L Easy-Load | Verified | [S3] |
| Hinge | "Adjustable hinge"; "welded door frame" | L&L eFL1626 | Verified (drawing labels) | [S2] |
| Hinge rod | the door "swings open a full 160 degrees on a robust ¾" steel rod with sealed bearings" | Paragon Dragon 24 (24 × 24 × 27 in inside) | Verified (secondary) | [S18] |
| Swing | "Max range of door: 180 deg" | L&L EL2424, EL3048 | Verified (drawing labels) | [S4] [S5] |
| Swing | 147°: the only angle on sheet 1, which also carries the label "max range of door". The two are not next to each other in the text, so the pairing is a reading | L&L eFL1626 | Verified (drawing; pairing uncertain) | [S2] |
| Fitting | L&L ships eFL doors separately, with mount brackets pre-installed "to help align the door with the hinge precisely" | L&L eFL | Verified | [S1] |
| Hinge side on the eFL, the Dragon | **NOT FOUND** (drawing only) | | | |

### 2.2 Latch

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Latch | "Adjustable DE-STA-CO clamps" | L&L eFL1626, EL2424, EL3048 | Verified (drawing labels) | [S2] [S4] [S5] |
| Latch | "Spring-loaded latches apply even pressure for a tight thermal seal" | Paragon Dragon 24 | Verified (secondary) | [S18] |
| Number of latches | two on the Dragon, four on the Super Dragon | Paragon (retailer listings) | Excerpt (secondary) | [S19] |
| Clamp count and size on L&L doors | **NOT FOUND** (drawing only) | | | |

### 2.3 Door plug, step and gasket

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Plug and gasket | "Brick door has an inset stepped brick plug and fiberglass tadpole gasket around door for tightness of seal." | L&L Easy-Load | Verified | [S6] |
| Gasket retainer | "Stainless steel gasket retainers" | L&L EL2424, EL3048 | Verified (drawing labels) | [S4] [S5] |
| Step | label "1/2" brick offset improves heat seal". The drawing could not be seen, so which two faces the ½ in is measured between is not confirmed | L&L eFL1626, EL2424, EL3048 | Verified (label only) | [S2] [S4] [S5] |
| Plug | "adjustable door with plug seal" | L&L eFL | Verified | [S1] |
| Plug | "the recessed inner door face minimizes heat leakage" | Paragon Dragon 24 | Verified (secondary) | [S18] |
| Door lining | eFL: 3 in K23 brick with microporous backup in the door; the drawing's cutaway says "1" microporous back-up insulation" | L&L eFL1626 | Verified | [S1] [S2] |
| Door lining | "3" firebrick + 1" ceramic fiber block in walls, top, and door" | Paragon Dragon 24 | Verified (secondary) | [S18] |
| Door elements | elements on the sides, back and door. To remove the door, first take the element connection wires off the door's element terminals | L&L Easy-Load | Verified | [S3] [S6] |
| Door elements | door elements with infinite switches; on the car kiln, power to door and floor runs through a plug that must be unplugged before opening | Olympic large-capacity kilns | Verified | [S17] |

### 2.4 Door switch

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Door switch | "Door Shut Off Switch: Shuts power off when door is opened." | L&L Easy-Load | Verified | [S6] |
| Door switch | "door switch" | L&L eFL, EL drawings | Verified | [S1] [S2] [S4] |
| Controller input | the Genesis 2.0 controller "has connections for a lid switch" | L&L | Verified | [S1] |
| Expansion | a door switch out of adjustment can cut the elements part-way through a firing as the door expands at high temperature | Paragon lid/door safety switch | Excerpt | [S20] |
| Opening temperature | "Do not open the kiln door until the kiln has cooled down to 250°F (120°C)" | L&L | Verified | [S1] |
| UL 499 requirement for a kiln door interlock | **NOT FOUND** in the text read. See §8.2 for the clauses on open-wire elements | | | [S21] |

### 2.5 Kiln and door weights

| Kiln | Kiln (lb) | Kiln without door (lb) | Door (lb) | Door share (derived) | Mark | Source |
|---|---|---|---|---|---|---|
| L&L eFL1626 | 570 | 465 | 105 | 105 / 570 = 18.4 % | Verified | [S2] |
| L&L EL2424 | 1135 | 915 | 220 | 220 / 1135 = 19.4 % | Verified | [S4] |
| L&L EL3048 | 1880 | 1540 | 340 | 340 / 1880 = 18.1 % | Verified | [S5] |
| Paragon Dragon 24 | "900+" | – | – | – | Verified (secondary) | [S18] |

---

## 3. Elements in the wall

### 3.1 Hard holders or grooves in the brick

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Hard holders | "Hard ceramic channels that hold and protect the elements" set in the firebrick. "No pins are required." Holders "have a top and a bottom" | L&L (patented holders) | Verified | [S1] |
| Holder sizes | L&L kilns made after January 1996 have larger holders that take heavier-gauge elements. Quad-element kilns need more holders and are not interchangeable | L&L | Verified | [S1] |
| Replacement brick | ordered pre-routed with holders; a brick "where the element connections come through" has different holders | L&L | Verified | [S8] |
| Grooves in IFB | Skutt bricks "have an up and a down. Orient the bricks with the deeper channel down to hold the element." Elements are pre-bent to fit the brick angles | Skutt (KilnParts repair guides) | Verified | [S13] [S14] |
| Grooves in IFB | sidewall and lid "are specially routed to retain the heating elements without the use of metal pins" | Evenheat | Verified | [S16] |
| Grooves in IFB | elements are pinned at each corner with Kanthal pins: "The pins should hold the element down while the lip of the element groove holds the element in." | Olympic | Verified | [S17] |
| Grooves in IFB | "industrial-gauge heating elements protected in dropped, recessed wall grooves" | Paragon Dragon 24 | Verified (secondary) | [S18] |
| Broken groove lip | "almost impossible to cement a broken groove lip back into place without contaminating the heating element"; hang the element on pins instead | Skutt KM | Verified | [S9] |
| Loading gap | "at least a 1-1/2" gap between pieces and elements, further if large flat surfaces are parallel to the kiln wall" | L&L | Verified | [S1] |

### 3.2 Coil and groove geometry

| Rule | Value | Mark | Source |
|---|---|---|---|
| Coil in a groove (Kanthal 2001 handbook, figure labels) | outer coil diameter D = (5–8) d; coil pitch s = (2–3) d, where d is the wire diameter. Spirals on ceramic tubes: D = (10–14) d, s = (3–6) d | Verified (figure labels, paired by text order) | [S22] |
| Same, Kanthal "Key data" web page | grooves: D = 5–6 d, minimum pitch 2 d | in `electric-and-thermal.md` §1.6 | |
| Groove width, depth, lip height and the spacing between grooves | **NOT FOUND** for any maker | | |
| Rows per section | L&L sections have two or three element rows (this sets the peephole drilling angle, §4.1) | Verified | [S8] |

The two Kanthal sources differ: the 2001 handbook allows D up to 8 d and pitch up to 3 d for
grooves; the current web page gives 5–6 d and 2 d. Neither gives the groove itself.

### 3.3 Element pins

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Pin length | "hang it on 1.5 inch element pins inclined toward the back of the groove"; put the pins in a straight row | Skutt KM | Verified | [S9] |
| Pinning method | push in at a steep angle, then lower it to a shallower angle. "The pins job is to hold the element DOWN into the channel" | Skutt (KilnParts guide) | Verified | [S14] |
| Pin shapes | straight pins (stop side-to-side movement; suit heavy gauge), horseshoe pins (keep coils at the bottom of the groove; "most common"), hook pins (less brick damage). Pin as few spots as possible | Euclid's | Verified | [S23] |
| Pin through the wall | "if element pins pass completely through the kiln wall and touch the kiln case they will cause a short" | Euclid's | Verified | [S23] |
| Pin material | V-shaped pins "made from the same material" as the element; nails or other wire damage elements | Rohde (German maker; not a US kiln) | Verified | [S24] |
| Pin wire | 15 ga Kanthal A-1 | Krueger; in `electric-and-thermal.md` §1.6 | | |

**Check for the engine (not a rule):** Euclid's warning [S23] means pin reach must stay inside
the wall. Reach = groove depth + pin length (1.5 in for Skutt [S9]) at its insertion angle.
Groove depth is **NOT FOUND**, so this check cannot yet be computed.

### 3.4 Where the element ends pass through the wall

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Through-hole | "Small hole allowing the element tail to pass through the kiln wall" | L&L | Verified | [S1] |
| Hole too large | lets too much heat escape and overheats the terminal connections; L&L's remedy is to stuff ceramic fibre lightly into the hole | L&L | Verified | [S1] |
| Drilling | for element connections, use a 1/8 to 3/16 in bit from the centre of the hole in the stainless case, "perpendicular to the case" | L&L | Verified | [S8] |
| Insulators | older L&L boards have ceramic insulator bushings and spacers on the outside of the through-holes; the newer ceramic terminal block "is all one integrated piece" | L&L | Verified | [S1] |
| Insulator | Skutt: push a porcelain insulator onto the pigtail, "tightly against the brick. Its job is to keep the element pigtail from coming into contact with the sheet metal." Cut the pigtail so 5/16 in sticks out past the insulator; crimp on a barrel connector | Skutt (KilnParts guide) | Verified | [S14] |
| Insulator | Olympic: reinstall porcelain insulators over the twisted pigtail; clip it "5/16 inch beyond the insulator"; high-temperature crimp connector | Olympic | Verified | [S17] |
| Feeder wire | strip ¾ in of insulation if the barrel connector takes one wire, ⅜ in if it takes two | Skutt (KilnParts guide) | Verified | [S14] |
| Terminal brick | Skutt and Olympic call the brick the element passes through the "terminal brick"; replacing one means cutting the pigtails | Skutt; Olympic | Verified | [S13] [S17] |

### 3.5 Terminal blocks and the element (terminal) box

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Terminal block | "Ceramic block that mounts the terminal hardware"; hardware is "Stainless steel bolts, washers, and nuts connecting the elements and power wires" | L&L | Verified | [S1] |
| Hardware | standard parallel block: two bolts, each stacked washer, nut, washer, element tail, washer, element tail, washer, power wire, nut. Wrap tails halfway round the bolt in a "U". Tool: 3/8 in nut driver | L&L | Verified | [S1] |
| Hardware | Easy-Load blocks have a single bolt, several blocks per section; the new "Universal" block has four bolts, one per element tail | L&L | Verified | [S1] |
| Box | "Stainless steel element box"; "ceramic element terminals (not shown)" | L&L eFL1626 | Verified (drawing labels) | [S2] |
| Box | "Ceramic element terminals (not shown) covered by perforated backing"; thermocouples likewise | L&L EL2424, EL3048 | Verified (drawing labels) | [S4] [S5] |
| Box | on Easy-Fire, eQuad-Pro, School-Master and eFL kilns, "a piggy-backed control panel covers up the element terminal blocks"; on Jupiter and DaVinci the panel is separate and jumper cords run to it | L&L | Verified | [S1] |
| Box | a "heat shield around the elements" (over the terminal area) carries the control box; it "will not come off unless you cut the element pigtails" | Skutt (KilnParts guide) | Verified | [S13] |
| Box | PK kilns: feeder wires go to terminal blocks "located on the fiberglass lined heat baffle" | Skutt KM-PK | Verified | [S9] |
| Box size, standoff from the case, vent openings | **NOT FOUND** as numbers for any maker | | | |

Temperatures that bear on terminals and wires are in UL 499 Table 36.1 (§8.4).

---

## 4. Spy holes (peepholes) and thermocouple ports

### 4.1 Size and plugs

| Kiln / context | Size and plug | Mark | Source |
|---|---|---|---|
| L&L Easy-Load | "one 1" diameter peephole per zone ... full diameter all the way through the firebrick", not tapered; one ceramic plug per hole | Verified | [S3] |
| L&L Easy-Load (EL2436–EL3048) | "Non-fragile solid ceramic with heat-locked head. 1" diameter full-view non-tapered. Three per kiln." | Verified | [S6] |
| L&L eFL | "Solid, Straight-View Peephole Plug" | Verified | [S1] |
| L&L, drilling | "use a 1" diameter drill bit or hole saw" through the pre-punched hole in the stainless. Two-row sections: drill perpendicular to the case. Three-row sections: drill "at a slightly down angle (about 5° to 7°)" to miss the element holders | Verified | [S8] |
| Skutt KM | "white porcelain peep plugs"; "Give them a slight twist to lock them in". Without a downdraft vent, leave the top plug out when firing | Verified | [S9] |
| Olympic | "The tapered shape and mortar coating of the 'peep hole' insure a good fit"; plugs are "hollow ceramic" | Verified | [S17] |
| Evenheat | "a special metal peephole cover that is permanently attached to the kiln"; it swings open on a screw | Verified | [S16] |
| Paragon Dragon 24 | "Two 1" peepholes on left side" | Verified (secondary) | [S18] |
| Gas-kiln file | an L&L peephole plug listed at about ⅞ in diameter (secondary) agrees with L&L's 1 in hole | see `kiln-hardware.md` §2.3 | |

### 4.2 How many, and where

| Kiln / context | Count and position | Mark | Source |
|---|---|---|---|
| L&L Easy-Load | one per zone | Verified | [S3] |
| L&L EL3048 | three zones, three peepholes | Verified | [S6] |
| Paragon Dragon 24 | two, on the left side | Verified (secondary) | [S18] |
| Olympic | a witness cone "should be placed 3 inches behind the observation hole" | Verified | [S17] |
| Heights of the holes on a studio electric kiln | **NOT FOUND** | | |

### 4.3 Thermocouple ports

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Protrusion | "at least 1" (2.5 cm) in from the inside surface" | L&L | Verified | [S1] |
| Protrusion | "between 1 1/8" - 1 1/2"" | L&L Easy-Fire (Genesis section) | Verified | [S7] |
| Protrusion | "at least 1"" | Skutt KM | Verified | [S9] |
| Protrusion | 1.25 to 1.5 in for the KM-1 wall-mount controller retrofit | Skutt | Verified | [S9] |
| Protrusion | 1 in | Olympic; Evenheat (pyrometer thermocouple) | Verified | [S17] [S16] |
| Diameter | Type S 1/4 in (6.4 mm); Type K 1/2 in (12.7 mm). Pack fibre round the smaller couple, which "also helps prevent excess heat radiating into the control box" | Skutt KM | Verified | [S12] |
| Diameter | 8 gauge Type K in a mullite protection tube; Pyrocil metallic option 1/4 in diameter, 6-1/2 in long | L&L | Verified | [S3] [S7] |
| Mount | flange tube about 5/8 in diameter, 1.5 in long, on a washer, screwed over the jacket hole; jacket hole 0.5 to 5/8 in. The manual's drill size reads ".5 in. (0.64 cm)", which is inconsistent (0.5 in = 1.27 cm) | Skutt KM-1 retrofit | Verified (source inconsistent) | [S9] |

---

## 5. Downdraft vents

### 5.1 Fan and flow

| Vent | Flow | Electrical | Other limits | Mark | Source |
|---|---|---|---|---|---|
| Skutt EnviroVent 2 | 140 CFM | 115 V, 1.4 A, 50/60 Hz | heat leaving the blower 160 °F max. One plenum cup per kiln up to 12 ft³; up to 24 ft³ per motor with the dual intake kit | Verified | [S11] |
| Orton Vent Master | 73 CFM | 115 V 60 Hz 1.1 A, or 208–240 V 50/60 Hz 0.5 A | "Normal room conditions will replenish air, makeup air system not necessary" | Verified | [S15] |
| L&L Vent-Sure, 120 V motor | 146 / 140 / 126 / 124 / 120 / 110 CFM at 0 / 0.1 / 0.2 / 0.3 / 0.4 / 0.5 in static pressure | 115 V, 0.75 A full load, 3100 RPM | blower 5-3/4 H × 6-5/16 W × 5-3/8 D in; motor rating "Max. Inlet Temp. 104 °F"; exit "less than 150 Deg F" | Verified | [S1] |
| L&L Vent-Sure, 230 V motor | 133 / 128 / 126 / 119 / 112 / 105 CFM at the same pressures | 230 V, 0.33 A, 2880 RPM | | Verified | [S1] |
| L&L Vent-Sure, capacity | "Each vent is capable of handling 20 cubic feet of kiln" | | | Verified | [S3] |

### 5.2 Holes in the floor and lid

| Rule | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Hole rule (Orton) | "one 1/4" hole for every four cubic feet of kiln volume", the same number in the lid and the floor; never more than four ¼ in holes | Vent Master | Verified | [S15] |
| Hole rule (L&L) | the same ¼ in per 4 ft³. Holes "normally placed within a 4 inch circle in the center of the kiln floor". L&L "does not normally recommend drilling holes in the top" | Vent-Sure | Verified | [S1] |
| Floor pattern (Orton) | within a 3½ in diameter circle, so the collector cup covers them | Vent Master | Verified | [S15] |
| Floor pattern (L&L) | Step 2 says "draw a circle in the middle with a radius of 1.5"" (3 in across); the FAQ says a 4 in circle. The two disagree | Vent-Sure | Verified (source inconsistent) | [S1] |
| Floor pattern (Skutt) | "must fit within a 1 1/2" diameter circle at the center of the floor" | EnviroVent 2 | Verified | [S11] |
| Lid pattern (Orton) | "about 2-3" inside the edge of the firebrick"; the holes must open into the chamber, not the wall | Vent Master | Verified | [S15] |
| Lid pattern (Skutt) | no closer to the outside edge than the sidewall brick thickness plus 1 in; evenly spaced, not clustered, not directly above the thermocouple | EnviroVent 2 | Verified | [S11] |
| Single-hole equivalents (Orton) | 2 × ¼ in → one ⅜ in; 3 → 7/16 in; 4 → ½ in | Vent Master | Verified | [S15] |
| Square kilns (Skutt) | for kilns that are square or rectangular, "find out the total cubic feet of the kiln and use the closest value in the chart" | EnviroVent 2 | Verified | [S11] |
| Floor flex | "The floor of a 12 sided kiln will flex up to 1/4"", which is why Skutt's plenum cup is spring-loaded | EnviroVent 2 | Verified | [S11] |
| Bottom shelf | at least 1 in above the floor so the holes stay open | Skutt; Orton | Verified | [S11] [S15] |

Orton's chart (rectangular kilns, length × width × depth in inches, and number of ¼ in holes) [S15]:

| Volume (ft³) | 1–2 | 2–4 | 4–6 | 4–6 | 6–8 | 8–10 | 10–12 |
|---|---|---|---|---|---|---|---|
| Rectangular kiln (in) | 12 × 12 × 18 | 18 × 18 × 18 | 20 × 20 × 20 | 30 × 20 × 24 | 24 × 24 × 24 | 22 × 16 × 44 | 24 × 24 × 36 |
| Holes | 1 | 1 | 2 | 2 | 2 | 3 | 3 |

Skutt's chart, the rows near 7 ft³ (multi-sided kilns) [S11]:

| Kiln | Holes in slab | Holes in lid | Drill | ft³ |
|---|---|---|---|---|
| Ten-sided, 18 in deep | 2 | 3 | 3/16 in | 4.2–4.6 |
| Ten-sided, 27 and 22 in deep | 3 | 3 | 3/16 in | 5.3–7.0 |
| Twelve-sided, 18 in deep | 1 | 2 | 1/4 in | 6.6 |
| Twelve-sided, 27 and 22 in deep | 2 | 3 | 1/4 in | 8.1–9.9 |

L&L's drill chart for its front-loaders (holes in the floor, all ¼ in) [S1]:

| Model | eFL1616 | eFL1626 | eFL2026 | eFL2626 | eFL2635 | EL2424 | EL2427 | EL2436 | EL2448 | EL2848 | EL3048 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ft³ | 4.0 | 6.6 | 8.6 | 10.2 | 13.7 | 8.0 | 9.0 | 12.0 | 16.0 | 20.0 | 25.0 |
| Holes | 2 | 2 | 2 | 3 | 4 | 2 | 3 | 3 | 4 | 7 | 8 |

### 5.3 Ducting and mounting

| Item | Value | Vent | Mark | Source |
|---|---|---|---|---|
| Duct | 3 in flexible aluminium, 8 ft, stretching 6–8 ft. Wall hole 3⅛ in for the 3 in discharge tube (supplied 8 in long). Mounting plate 8 × 12 in | Skutt EnviroVent 2 | Verified | [S11] |
| Long runs | beyond 60 ft or with 4 or more 90° bends, change to 4 in duct no further than 8 ft from the plenum cup | Skutt EnviroVent 2 | Verified | [S11] |
| Central duct | 4, 6, 8, 8, 10, 10 in for 1 to 6 vents | Skutt EnviroVent 2; L&L Vent-Sure (same table) | Verified | [S11] [S1] |
| Duct | 2 in high-temperature hose from cup to blower; then 4 in duct: 100 ft with no bends, 90 ft with 1, 80 with 2, 70 with 3, 60 with 4 | Orton Vent Master | Verified | [S15] |
| Duct | 3 in inlet duct before the motor, 4 in after it; 4 in wall penetration; up to 60 ft with four 90° bends | L&L Vent-Sure | Verified | [S1] |
| Blower position | at least 6 in from the kiln, or on the wall; "Never place the blower housing under the kiln" | Orton Vent Master | Verified | [S15] |
| Blower position | "hook up vent motor within 15 feet of outlet of vent tube" | L&L drawings | Verified | [S2] [S4] |
| Collector | spring-loaded plenum cup between kiln floor and room floor | Skutt EnviroVent 2 | Verified | [S11] |
| Collector | collector cup on an adjustable foot; fit differs if the floor-to-kiln gap is under or over 6 in | Orton Vent Master | Verified | [S15] |
| Collector | bypass collection box bolted to the bottom of the stand, with a sliding flow adjuster | L&L Vent-Sure | Verified | [S1] |
| Outlet | at least 4 ft from any opening (window or door) into the building | Skutt; L&L | Verified | [S11] [S1] |
| Side mount | if the cup cannot go under the kiln, mount it as low as possible on the side (Skutt) or near the bottom at the back (Orton) | Skutt; Orton | Verified | [S11] [S15] |

---

## 6. Controller and control box

| Item | Value | Kiln / context | Mark | Source |
|---|---|---|---|---|
| Position | "The control panel is mounted on the right side with standoffs to keep it separate from the heat of the kiln" | L&L Easy-Load | Verified | [S3] |
| Panel | "Separate panel is mounted on the right side. ... The control panel is hinged for easy access." Direct hook-up to a terminal block in the panel | L&L Easy-Load | Verified | [S6] |
| Panel | "Panel folds down 90 deg for easy maintenance" | L&L eFL1626 | Verified (drawing label) | [S2] |
| Access | "Leave 24" free space in front of controller for operation and maintenance" | L&L eFL1626, EL2424, EL3048 | Verified | [S2] [S4] [S5] |
| Standoff | "1" clearance between kiln and switch box to keep components cool"; the switch box is "generously vented", hinged, with a folding support arm | Paragon Dragon 24 | Verified (secondary) | [S18] |
| Standoff | the control panel "is separated from the kiln body by a heatshield" | Evenheat | Verified | [S16] |
| Box | "Skutt kilns have a hinged box which is held closed by 3-6 phillips screws depending on the model" (on its left side); the box lifts off its hinges | Skutt | Verified | [S13] [S9] |
| Heat baffle | a heat baffle is screwed to the back of the control box | Skutt KM | Verified | [S12] |
| Orientation | with more than one kiln, the control boxes must not face other kilns: "Radiant heat from nearby kilns can damage the controller" | Skutt | Verified | [S9] [S10] |
| Pyrometer | "needs to be wall mounted away from the kiln since the heat will damage the instrument" | Olympic manual-control kilns | Verified | [S17] |
| Electronics | DynaTrol and Genesis are specified for 32–125 °F; the electronics "could degrade if operated for long periods above 125°F" | L&L | Verified | [S1] |
| Electronics | Skutt automatic kilns "shutoff if the electronics get too hot" | Skutt | Verified | [S10] |
| L&L standoff distance | **NOT FOUND** (L&L says "standoffs" with no size) | | | |

---

## 7. Clearances and siting

### 7.1 Walls, ceiling and other kilns

| Rule | Value | Maker / context | Mark | Source |
|---|---|---|---|---|
| Walls (Skutt) | "tested to be safe by Underwriters Laboratories when installed a minimum of 18" (46 cm) from any wall or combustible material" | Skutt | Verified | [S10] |
| Between kilns (Skutt) | "as close as 18" (46 cm) apart", controllers not facing each other | Skutt | Verified | [S10] |
| Walls (L&L cautions) | hot surface "no closer than 12" (30 cm) to any wall. 18" (46 cm) is preferable." | L&L | Verified | [S1] |
| UL test (L&L) | "when L&L tested kilns for UL, temperatures were measured 12" from the walls of the kiln and found to be safe from a flammability standpoint" | L&L | Verified | [S1] |
| UMC (as L&L quotes it) | Uniform Mechanical Code 2000: "the sides and tops of kilns shall be located a minimum of eighteen (18) inches (457 mm) from any noncombustible wall surface and three (3) feet (914 mm) from any combustible wall surface" | quoted by L&L | Verified (quotation, code not read) | [S1] |
| Between kilns (L&L cautions) | "a minimum of 36" (91 cm) between the hot surfaces of two adjacent kilns" | L&L cautions | Verified | [S1] |
| Between kilns (L&L drawings) | "Leave at least 18" [45.7cm] between two kilns"; 12 in to walls, 18 in recommended | L&L eFL1626, EL2424, EL3048 | Verified | [S2] [S4] [S5] |
| Service space (L&L) | 24 in in front of the panel and 18 in at the back; "18" to 24" clearance around the outside wall of the kiln is usually sufficient" | L&L | Verified | [S1] |
| Walls (Evenheat) | "A minimum of 12" (31cm) shall be allowed between all surfaces of the kiln and the surrounding walls and ceilings", with lids and doors fully open, fully closed and in between; walls and ceilings non-combustible | Evenheat | Verified | [S16] |
| Ceiling (Evenheat) | "at least 24" between the highest point of the lid, when in the open position and the ceiling" | Evenheat | Verified | [S16] |
| Lid lifter (Evenheat) | "at least 16" from any walls" with the Dyna-Lift | Evenheat | Verified | [S16] |
| Walls (Olympic) | "at least 12 inches of space between the kiln and the wall" | Olympic | Verified | [S17] |

### 7.2 Floor

| Rule | Value | Maker / context | Mark | Source |
|---|---|---|---|---|
| Floor | "a minimum of 2" (5 cm) thick solid masonry extending a minimum of 12" (31 cm) beyond the outer perimeter of the kiln", credited to the Uniform Mechanical Code | Skutt; L&L (quoting UMC 2000); Evenheat | Verified (code quoted, not read) | [S10] [S1] [S16] |
| Floor | bare concrete preferred; no wood, carpet or vinyl | Skutt; L&L | Verified | [S10] [S1] |
| Surface temperature | "Combustible surfaces that stay below 71°C (160°F) are generally considered safe", which L&L ties to NFPA 86 §2-1.5; L&L recommends "under 52°C (125°F)" | L&L | Verified (code quoted, not read) | [S1] |
| Kiln surface | "Kiln surface can be extremely hot: up to 260°C (500°F)." | L&L | Verified | [S1] |

### 7.3 Room temperature, ventilation and sprinklers

| Rule | Value | Maker / context | Mark | Source |
|---|---|---|---|---|
| Room temperature | keep the room below 100 °F (38 °C) | Skutt room guide | Verified | [S10] |
| Room temperature | "maximum operating temperature is 100°F (38°C)" and minimum 33 °F; but also "For small rooms, monitor the firing so room temperatures does not exceed 105°F (41°C)" | Skutt KM manual (inconsistent) | Verified (source inconsistent) | [S9] |
| Room temperature | between 0 °F and 100 °F | L&L | Verified | [S1] |
| Room ventilation | "room ventilation of at least 25-50 times the cubic feet of the kiln per minute", e.g. 250–500 CFM for 10 ft³ | L&L | Verified | [S1] |
| Make-up air | provide make-up air for the 140 CFM the EnviroVent 2 removes, e.g. a vent panel in the door or wall | Skutt | Verified | [S10] |
| Heat to remove | eFL1626, held at temperature (BTU/h): 13 132 at 1800 °F, 15 340 at 2000 °F, 18 098 at 2232 °F, 19 581 at 2350 °F | L&L eFL1626 drawing | Verified | [S2] |
| Same, in kW | 19 581 BTU/h × 0.29307 W per BTU/h = **5.74 kW** at 2350 °F, against a 11.52 kW rating (240 V) | Derived | |
| Sprinklers | "do not place kilns within a 10 ft. (3m) radius below sprinkler heads" | Skutt KM | Verified | [S9] |
| Sprinklers | not directly above the kiln; use the highest rating local code allows | Skutt; L&L | Verified | [S10] [S1] |

L&L notes that its BTU charts are steady-state holding values, "rarely the case for a ceramic
kiln", and a safe upper figure for HVAC sizing [S1]. They are also a check for the engine's
heat-loss solver: the eFL1626 (6.6 ft³; 3 in K23 brick, K25 at the back, microporous backup in
the door [S1]) loses about 5.74 kW held at 2350 °F, by L&L's figure.

### 7.4 Where the power connection goes

| Rule | Value | Maker / context | Mark | Source |
|---|---|---|---|---|
| Outlet position | on the right side of the kiln, 18 in (46 cm) to 40 in (102 cm) from the floor; the 6 ft (1.8 m) cords leave the control box at the front | Skutt | Verified | [S10] |
| Outlet position | "Position the kiln to the left of your electrical outlet" | Skutt KM | Verified | [S9] |
| Direct-wired | "need a means of disconnect visible from the kiln or lockable" | Skutt | Verified | [S10] |
| Cord | 6 ft cord, NEMA 6-50 single phase or 15-50 three phase; or hard-wired to a fused disconnect | L&L eFL1626 drawing | Verified | [S2] |
| Cord rating | "All L&L power cords are rated for 105°C (221°F)"; direct-wire connection wires must also be at least 105 °C | L&L | Verified | [S1] |
| Receptacle | mount it so the cord hangs down, not up, and not so low that the cord bends sharply | L&L | Verified | [S1] |
| Disconnect distance | "Distance to Disconnect Box: This should be under 15 feet according to the National Electrical Code" | L&L (its reading of the NEC; not checked) | Verified (quotation) | [S1] |
| Breaker distance | "Try to locate the kiln within 50 feet of your breaker box" | L&L | Verified | [S1] |
| Cord routing | the cord must not touch the hot case | L&L; Skutt; Evenheat; Olympic | Verified | [S1] [S9] [S16] [S17] |

Breaker, wire and plug sizes are in `electric-and-thermal.md` §3.

---

## 8. UL 499 points that set dimensions or materials

Source: ANSI/UL 499, 14th edition (2014) with revisions through 17 November 2025 [S21]. L&L's
eFL and Easy-Load front-loaders are "MET-us listed to UL499" [S1] [S3] [S6]; Skutt says its
kilns were tested by UL [S10]. Only clauses read are quoted.

### 8.1 Enclosure

| Clause | Requirement | Mark |
|---|---|---|
| 1.1 (scope) | heating appliances rated 600 V or less | Verified |
| 7.4 | an enclosure "that shall house all electrical parts", except a supply cord and a recessed open-wire element unit (15.3) | Verified |
| 7.11, Table 7.1 | minimum sheet thickness of the enclosure. Uncoated sheet steel: 0.026 in (0.66 mm) at small or reinforced surfaces and at large unreinforced flat surfaces; 0.032 in (0.81 mm) where field wiring connects. Galvanized: 0.029 / 0.034 / 0.029 in. Nonferrous: 0.036 / 0.045 / 0.036 in. Footnote a: thinner sheet may be used at small or reinforced surfaces if judged acceptable under 7.6. The table does not name stainless steel | Verified |
| 7.18–7.19 | an opening is acceptable if the articulate probe cannot touch an uninsulated live part; or, if it can enter, no live part lies within X of the opening, where X is 5 × the largest rod that fits, "but not less than 4 inches (102 mm)" | Verified |
| 7.25–7.26 | an enclosure door or cover needs a means to hold it closed; if it gives access to fuses it must be hinged, latched, and tight-fitting or overlapping | Verified |
| 7.5 | ventilation openings of a permanently connected product must not vent into concealed building spaces | Verified |
| 10.1–10.2 | iron and steel parts protected against corrosion where corrosion could cause fire or shock; "A sheath employed on a heating element operating in air and terminal parts attached directly to the heating element need not be protected" | Verified |

### 8.2 Elements and insulation

| Clause | Requirement | Mark |
|---|---|---|
| 15.1–15.2 | a heating element "shall be supported in an acceptable manner", protected against damage and contact with outside objects; consider sagging and loosening under continuous heating | Verified |
| 15.3 | "An open-wire element - that is, uninsulated resistance wire - may be used ... provided it is enclosed or protected by barriers or covers that require tools for removal", and meets the live-part accessibility rules 7.18–7.22 | Verified |
| 16.2 | "certain refractory materials are usually acceptable for use as the sole support of live parts" | Verified |
| 16.3 | small fragile insulating parts "should be slightly loose" so expansion does not crack them | Verified |
| 17.2–17.3 | combustible or electrically conductive thermal insulation must not touch uninsulated live parts; some mineral wool contains conductive slag, so it is unacceptable in contact with live parts | Verified |
| 25.6 | on a permanently connected appliance, a switch controlling elements must disconnect all ungrounded supply conductors, unless no live parts are exposed when it is open | Verified |

No clause read says how a front-loader's opening door relates to 15.3. The door switch on
L&L's front-loaders (§2.4) is a maker's feature; that it is how they meet 15.3 is **NOT FOUND**.

### 8.3 Spacings (line voltage)

Table 27.1, at field-wiring terminals [S21] (Verified):

| Parts | 0–250 V, through air | 0–250 V, over surface | 251–600 V, through air | 251–600 V, over surface |
|---|---|---|---|---|
| Live parts of opposite polarity; live part to dead metal other than the enclosure | ¼ in (6.4 mm) | ⅜ in (9.5 mm) | ⅜ in (9.5 mm) | ½ in (12.7 mm) |
| Live part to the enclosure | ½ in (12.7 mm) | ½ in | ½ in | ½ in |

Table 27.2, elsewhere [S21] (Verified): 1/16 in (1.6 mm) at 0–250 V and ¼ in (6.4 mm) at
251–600 V, between uninsulated live parts of opposite polarity and between a rigidly mounted
live part and dead metal. Note c: "A spacing 1/16 inch (1.6 mm) is permissible at the heating
element only, in a heater rated for 300 V or less." Note a: a live part that is not rigidly
supported must keep at least 1/16 in under all operating conditions.

Also: barriers between circuits have openings no larger than ¼ in (6.4 mm) (14.4.4.1); a metal
barrier is at least as thick as the enclosure; an insulating barrier at least 0.028 in
(0.71 mm) (14.4.4.2) [S21] (Verified).

### 8.4 Temperatures and markings

| Clause | Requirement | Mark |
|---|---|---|
| 36.1.3 | Table 36.1 limits are rises over an assumed 25 °C (77 °F) room | Verified |
| Table 36.1, item 1 | inside a terminal box or wiring compartment where field wires connect: 35 °C (63 °F) rise, unless marked per 53.7 | Verified |
| Table 36.1, item 2 | any point on a surface adjacent to a permanently connected (or fixed, dedicated-space) appliance, including test surfaces at the designated clearances: 65 °C (117 °F) rise | Verified |
| Table 36.1, items 3, 16, 18, 19 | fuses 65 °C rise; insulated wire or cord "25 °C (45 °F) less than its temperature rating"; bare or insulated copper without nickel coating 125 °C (225 °F) rise; copper terminations in pressure connectors without nickel coating 125 °C rise | Verified |
| 53.7, Table 53.1 | if the terminal box exceeds 60 °C, mark "For supply connections use ___ AWG or larger wires suitable for at least ___°C": 75 °C wire for 61–75 °C, 90 °C wire for 76–90 °C | Verified |
| 36.1.17 | permanently connected or fixed appliances are tested in a corner of two vertical walls of black-painted ⅜ in (9.5 mm) plywood, extending at least 2 ft beyond the heater, on black-painted wood at least ⅜ in thick; spaced away only if marked per 53.9 | Verified |
| 53.9 | if a spacing is needed to keep an adjacent surface at or below 90 °C (194 °F), mark "Do not install closer than ___ inches (or ___ mm) to a (vertical, horizontal, or other) surface" | Verified |
| 31.3, Table 36.2 | user-contact surface limits: handles grasped for lifting, 55 °C metal / 75 °C nonmetallic; handles touched but not lifted and surfaces touched in maintenance, 60 / 85 °C; surfaces hot because they are near the heating surface, 70 / 95 °C | Verified |
| 53.40 | an appliance whose accessible surfaces (not handles or knobs) exceed Table 36.2 is marked "CAUTION ... Hot Surface. Avoid Contact." on or next to the surface | Verified |

**Derived checks:** Table 36.1 item 2 (65 °C rise) on the 25 °C basis is 90 °C, which is
53.9's limit. Item 1 (35 °C rise) is 60 °C, which is 53.7's threshold. L&L's "measured 12" from
the walls" (§7.1) is this corner test.

### 8.5 Supply connection

| Clause | Requirement | Mark |
|---|---|---|
| 11.2.1 | terminals for conductors with ampacity ≥ 125 % of the rating for a continuous load (3 h or more) | Verified |
| 11.2.2 | the test assumes 60 °C wire for continuous loads of 80 A or less; 75 °C above that | Verified |
| 11.2.11 | a lead for field connection has at least 6 in (152 mm) free length in the box | Verified |
| 11.1.3 | the supply terminal box must be placed so its connections can be inspected after installation | Verified |
| 12.1.1, Table 12.1 | appliances not otherwise listed: cord at least 6.0 ft (1.8 m) | Verified |
| 12.1.6 | "The current rating of the attachment plug shall not be less than 125 percent of the current rating of the product when the load will constitute a continuous load (3 hours or more)" | Verified |

### 8.6 Kiln clauses

36.2.1, 42.5.1 and 53.22 cover "ceramics-baking kilns and ovens": a kiln may be tested only up to
a stated internal temperature if it carries a marking that the supply should be cut off when the
interior reaches that value; otherwise it runs until temperatures stabilize [S21] (Verified).

---

## 9. Applied to `examples/electric-front-loader.yaml` (derived)

Inputs from the example: chamber 22.5 × 22.5 × 24 in; 240 V single phase on a 60 A breaker
(48 A continuous); walls 4.5 in IFB + 1 in blanket; flat roof; front door; shell
`oxidised_steel`.

- Chamber volume: 22.5 × 22.5 × 24 = 12 150 in³ ÷ 1728 = **7.03 ft³**.
- Vent holes:
  - Orton: 7.03 ÷ 4 = 1.76 holes; chart row 6–8 ft³ (24 × 24 × 24 in) gives **2 × ¼ in** in the
    floor and 2 in the lid [S15].
  - L&L: nearest front-loaders are eFL1626 (6.6 ft³) and EL2424 (8.0 ft³), both **2 × ¼ in**,
    floor only [S1].
  - Skutt: closest chart value 7.0 ft³ gives **3 × 3/16 in** in the floor and 3 in the lid [S11].
  - Open area: 2 × π/4 × 0.25² = 0.098 in² (Orton, L&L); 3 × π/4 × 0.1875² = 0.083 in² (Skutt).
- Room ventilation by L&L's rule: 25–50 × 7.03 = **176–352 CFM** [S1].
- Nearest catalogue kiln: L&L eFL1626-240 is 6.6 ft³, cone 10, 11 520 W, 48.0 A, 6 ga wire,
  60 A fuse, 6-50 cordset [S1]. Its inside is given as 17 W × 26 H × 26 D in in the bulletin and
  "18.6in inside width" on the drawing [S2]; the sides are arched, so the two numbers probably
  measure different places (not confirmed).
- Roof: the example has a flat 4.5 in IFB roof over a 22.5 in span. Every front-loader read has
  an arched top: L&L Easy-Load "Arched Roof for Strength ... 4-1/2" of extra-strong 2500°F K25
  arch brick" [S6]; L&L eFL "arched sides and top for strength" [S1]. Flat brick tops appear only
  as top-loader lids, held by a band and clips (§1.1). A maker's flat front-loader roof:
  **NOT FOUND**.
- Shell: the example's `oxidised_steel` finish matches none of the makers read. They use
  stainless steel (top-loader jackets, the eFL case) or powder-coated steel (Easy-Load stand,
  case, door and hinge; the eFL drawing's "steel is powder-coated") [S2] [S4] [S6] [S9].
  Emissivities are in `electric-and-thermal.md` §4.7.
- Wall: the example's 4.5 in IFB + 1 in blanket is thicker than the catalogue front-loaders
  (L&L Easy-Load 3 in K23 + 2 in backup [S6]; Paragon Dragon 3 in + 1 in fibre block [S18]).
  Element tails must cross the blanket layer; UL 499 17.2–17.3 keeps conductive or combustible
  insulation off live parts (§8.2).
- Stand: the example has none. Makers stand top-loaders 8 in off the floor [S1] [S11]; L&L's
  Easy-Load hearth is about 18 in up [S6].

---

## 10. Where the sources disagree

- **Clearance to walls:** Skutt 18 in minimum, "tested ... by Underwriters Laboratories" [S10];
  L&L 12 in minimum, 18 in preferred [S1]; Evenheat and Olympic 12 in [S16] [S17].
- **Between two kilns:** L&L's cautions say 36 in between hot surfaces [S1]; L&L's own drawings
  say at least 18 in [S2] [S4] [S5]; Skutt 18 in [S10].
- **Vent holes near 7 ft³:** Orton and L&L give 2 × ¼ in; Skutt gives 3 × 3/16 in (§9). L&L
  normally drills no lid holes; Orton and Skutt drill the same number in the lid.
- **Vent hole circle in the floor:** L&L 3 in (Step 2) or 4 in (FAQ) [S1]; Skutt 1½ in [S11];
  Orton 3½ in [S15].
- **Room temperature:** Skutt 100 °F in the room guide [S10]; the KM manual gives 100 °F and,
  for small rooms, 105 °F [S9].
- **Coil geometry in grooves:** Kanthal 2001 handbook D = (5–8) d, s = (2–3) d [S22]; Kanthal's
  current web page 5–6 d, 2 d (`electric-and-thermal.md` §1.6).
- **eFL1626 inside width:** 17 in (bulletin) against 18.6 in (drawing) [S1] [S2].
- **Plug rating:** UL 499 12.1.6 asks for a plug rated at least 125 % of the product's current
  for a continuous load [S21]. 48 × 1.25 = 60 A (derived), but the 48 A eFL1626-240 ships with a
  NEMA 6-50 cordset [S1], and `electric-and-thermal.md` §3 records L&L's 50 A cord "built to
  carry at least 60 A". Whether the listing treats a kiln as a continuous load is **NOT FOUND**.

---

## 11. Gaps (not found)

- Stainless jacket thickness or gauge for any top-loader.
- Steel sections (angle or tube sizes) for a front-loader frame. Only L&L's 1/8 in welded case
  (EL bulletin), 11 ga eFL legs, and a retailer's 2 in tube for the Paragon Super Dragon.
- Element groove width, depth, lip height and the spacing between grooves, from any maker or
  from Kanthal. Only coil diameter and pitch relative to wire diameter (§3.2).
- Size of L&L's hard element holders.
- Element (terminal) box size and its standoff from the case; control-panel standoff distance
  for L&L ("standoffs", no size). Only Paragon's 1 in (retailer copy).
- Number and size of L&L's door clamps; hinge side of the eFL and the Dragon; the size and
  position of the door step (only the label "1/2" brick offset").
- Heights of spy holes on a studio electric kiln.
- A UL 499 clause on door interlocks for front-loading kilns.
- The Uniform Mechanical Code, NFPA 86 and NEC text, first-hand (all quoted here through kiln
  makers).
- The dimension drawings themselves (only their text labels were readable).

---

## Sources

- [S1] L&L Kiln Mfg, *eFL Series Instruction Manual* (2024 web edition; contains Cautions rev. 8/1/2022, Installation rev. 6/15/2023, eFL checklist 1/31/2023, Vent-Sure instructions rev. 5/10/2023, Elements troubleshooting rev. 4/19/2024, bulletins BL-eFL1626/2026/2626/2635). https://hotkilns.com/sites/default/files/2024-04/eFL%20Instructions%202024-web.pdf (list: https://hotkilns.com/support/instruction-manuals)
- [S2] L&L Kiln Mfg, drawing 200-000-70 rev. C, *eFL1626 (3" brick) General Dimensions*, 2017–2020. https://hotkilns.com/sites/default/files/2025-04/200-000-70%20eFL1626%20General%20Dimension%20Drawing.pdf (page: https://hotkilns.com/support/kiln-general-dimension-diagrams/efl1626)
- [S3] L&L Kiln Mfg, *Easy-Load Instruction Manual* (2024 web edition; instructions rev. 6/15/2023, accessories rev. 6/20/2023, bulletins BL-EL2424 etc.). https://hotkilns.com/sites/default/files/2024-04/Easy-Load%20Instructions%202024-web.pdf
- [S4] L&L Kiln Mfg, drawing 10000-1 rev. B, *EL2424 (3" brick) General Dimensions*, 2020. https://hotkilns.com/sites/default/files/2020-05/10000-1%20General%20Dimensions%2C%20EL2424.pdf
- [S5] L&L Kiln Mfg, drawing 10000-6 rev. B, *EL3048 (3" brick) General Dimensions*, 2020. https://hotkilns.com/sites/default/files/2023-10/10000-6%20General%20Dimensions%2C%20EL3048.pdf
- [S6] L&L Kiln Mfg, *Easy-Load Large Front-Loading Kilns*, Bulletin EL-3-15 (EL2436, EL2448, EL2848, EL3048). Download URL not recovered; local copy `scratch/research/electric/ll-el-spec/el2015.pdf`.
- [S7] L&L Kiln Mfg, *Easy-Fire Instruction Manual* (2024 web edition, pre-2025 kilns). https://hotkilns.com/sites/default/files/2024-04/Easy-Fire%20Instructions-2024-web.pdf
- [S8] L&L Kiln Mfg, *Troubleshooting and Fixing Brick Problems*, rev. 9/10/2023. https://hotkilns.com/sites/default/files/2023-09/troubleshoot-brick-9-2023_0.pdf (page: https://hotkilns.com/support/pdfs/troubleshooting-and-fixing-brick-problems)
- [S9] Skutt Ceramic Products, *KilnMaster Operating Manual*, revised 11/22/11. https://www.theceramicshop.com/downloads/Warranties-Diagrams-Manuals/Skutt/KilnMaster-Manual-2006-2013-(Wiring-Diagrams-on-pages-56-65).pdf
- [S10] Skutt Ceramic Products, *Kiln Room Design and Product Specifications*, effective 10/25/18 (includes CSI section 11 54 13). https://cdn.shopify.com/s/files/1/0889/3726/7497/files/Designing-A-Kiln-Room-1.pdf
- [S11] Skutt Ceramic Products, *EnviroVent 2 Operating Manual*, revised 12/9/16. https://www.theceramicshop.com/downloads/EnviroVent2.pdf
- [S12] Skutt Ceramic Products, *Service Training Manual 14.17: Type S Thermocouple Upgrade*, rev. 10/8/18. https://skutt.com/images/14.17-Type-S-Thermocouple-Upgrade.pdf (matched by revision date; the server refused a size check)
- [S13] KilnParts.com and Krueger Pottery Supply, *Replacing a brick in a Skutt Kiln*. https://cdn.shopify.com/s/files/1/0272/1968/9606/files/bricks.pdf
- [S14] KilnParts.com and Krueger Pottery Supply, *Replacing a heating element in a Skutt Kiln*. https://cdn.shopify.com/s/files/1/0272/1968/9606/files/elements.pdf
- [S15] Edward Orton Jr. Ceramic Foundation, *Vent Master Installation and Operating Manual*, v05.08.08. https://cdn.shopify.com/s/files/1/1023/7667/files/NEW_VentMasterManual.pdf
- [S16] Evenheat Kiln, *Ceramic Kiln Installation and Operating Manual, North American Models*, March 2018. https://cdn.shopify.com/s/files/1/0675/7541/files/CeramicManual.pdf
- [S17] Olympic Kilns (Haugen Mfg.), *Electric Kiln Operating Manual* (undated). https://cdn.shopify.com/s/files/1/0694/7461/5526/files/Olympic_Kilns_Electric_Manual.pdf
- [S18] The Ceramic Shop, *Paragon Dragon 24* product page (retailer copy of maker's description). https://www.theceramicshop.com/product/41801/paragon-dragon-240v-1p-sc/
- [S19] Retailer listings for the Paragon Dragon and Super Dragon (search summary only). https://abrimagery.com/products/paragon-super-dragon-kiln ; https://abrimagery.com/products/paragon-dragon-kiln
- [S20] Paragon, *Lid/Door Safety Switch* user manual (search summary only). https://www.manualsdir.com/manuals/170667/paragon-lid_door-safety-switch.html
- [S21] UL Standards & Engagement, *ANSI/UL 499 Standard for Electric Heating Appliances*, 14th ed. (7 Nov 2014) with revisions through 17 Nov 2025. https://law.resource.org/pub/us/cfr/ibr/inc/ul/ul.s499.14.2025.pdf
- [S22] Kanthal, *Handbook: Resistance Heating Alloys and Systems for Industrial Furnaces*, cat. 1-A-5B-3, 09.2001 (third-party copy). https://www.ibt.co.il/uploaded_files/documents/file1359965681_U3423.pdf
- [S23] Euclid's Kiln Parts, *Element Pinning* (one-page PDF). Download URL not recovered; local copy `scratch/research/electric/euclid-pinning/pinning.pdf`.
- [S24] Rohde, *How to fit ROHDE heating elements*, 01/2008 (Bath Potters' Supplies copy). https://www.bathpotters.co.uk/userfiles/file/element-installation-instructions.pdf
