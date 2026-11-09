# Wood as kiln fuel: heating values, moisture, efficiency, consumption

Informational starting values. The engine has **no default** for any of them: `site.wood` is the
user's own estimate (`heating_value`, net, of the oven-dry wood; `moisture`, wet basis;
`firebox_efficiency`; optionally `cord_weight` and `price` per cord). Left out, the firing says it
needs them. This mirrors `site.natural_gas_price` and `natural-gas-prices.md`. The engine reads
only the formula in §2 from this file; the figures below are there for the user to choose from.

Read 2026-11-08. Quotes are as the fetched page gave them. Several primary PDFs (Baker, FPL 1983;
White, FPL 1987; the FPL Fuel Value Calculator; Arkansas FSA 1091) are scanned images that could
not be read here: listed under "Not found" so nobody cites them from this file.

## 1. Heating values and the cord

### Per oven-dry pound (net/"available" heat, as the sources word it)

**[W1] University of Missouri Extension, G5450 "Wood Fuel for Heating"**, Hank Stelzer, published
September 2017, reviewed August 2025. <https://extension.missouri.edu/publications/g5450>

- "One pound of oven-dry wood of any hardwood species has an available heat value of about 8,600
  Btu."
- "Resinous softwood species, such as shortleaf pine, tend to average slightly higher at 9,050 Btu
  per oven-dry pound."
- Freshly cut hardwood (75 % moisture, oven-dry basis): 4,900 Btu/lb; air-dried hardwood (20 %):
  7,100 Btu/lb; wood pellets (6 %): about 7,750 Btu/lb.
- "A standard cord is a stack of wood, bark and air spaces 4 feet high, 4 feet wide, and 8 feet
  long for a total volume of 128 cubic feet." Solid wood in it runs from 65 ft³ (small, crooked
  sticks) to about 90 ft³; the Midwest average is about 80 ft³. Seasoned oak weighs about 3,600 lb
  a cord.
- Its fuel table's footnote: 11.4 million available Btu per cord of air-dried hardwood at 50 %
  unit efficiency.

Whether "available heat" is gross or net isn't stated. 8,600 Btu/lb is 20.0 MJ/kg; 9,050 is
21.05 MJ/kg (× 2.326 kJ/kg per Btu/lb, derived).

**[W2] Forest Research (UK), "Typical calorific values of fuels"** (no date on the page).
<https://www.forestresearch.gov.uk/tools-and-resources/fthr/biomass-energy-resources/reference-biomass/facts-figures/typical-calorific-values-of-fuels/>
"Net calorific value (CV) or Lower Heating Value (LHV) given for all fuels."

| Fuel | Net CV, GJ/t | kWh/kg | Bulk density, kg/m³ |
|---|---|---|---|
| Wood (solid, oven dry) | 19 | 5.3 | 400–600 |
| Log wood (stacked, air dry: 20 % MC) | 14.7 | 4.1 | 350–500 |
| Wood chips (30 % MC) | 12.5 | 3.5 | 250 |
| Wood pellets (10 % MC) | 17 | 4.8 | 650 |

**[W3] FAO, Unified Bioenergy Terminology (UBET), 2004, Ch. 5, §5.1.2 "Energy content"**.
<https://www.fao.org/4/j4504e/j4504e08.htm>. Table 10, net calorific value, dry basis, MJ/kg:
spruce wood (with bark) 18.8; beech wood (with bark) 18.4; poplar (short rotation) 18.5; willow
(short rotation) 18.4; softwood bark 19.2. "the net calorific value of wood decreases from
approximately 18.5 MJ/kg with increasing total moisture", reaching zero at about 88 %. "Normally the
total moisture of air-dried wood is between 12 and 20% yielding a calorific value of 13 to 16
MJ/kg."

### Per cord, by species

**[W4] Utah State University Extension, "Wood Heating"**, Michael Kuhns and Tom Schmidt (no date;
partly from a University of Nebraska fact sheet).
<https://extension.usu.edu/forestry/resources/forest-products/wood-heating.php>. Table 1, "Firewood
Facts": "an evenly-stacked pile containing 128 cubic feet of wood and air space"; "Green firewood
may contain 50% or more water by weight." The page gives no Btu per pound or moisture basis for its
heat column. Rows for the kiln woods asked about (blank cells left blank; the table's alignment
for rows with blanks was read by a summarising tool, so check against the page before relying on
a row):

| Species | Green, lb/cord | Dry, lb/cord | Heat, million Btu/cord |
|---|---|---|---|
| Pine, white | | 2250 | 15.9 |
| Pine, ponderosa | 3600 | 2336 | 16.2 |
| Pine, lodgepole | | 2610 | 21.1 |
| Pinyon | | 3000 | 27.1 |
| Douglas-fir | 3319 | 2970 | 20.7 |
| Fir, white | 3585 | 2104 | 14.6 |
| Spruce, Engelmann | | 2070 | 15.0 |
| Larch (tamarack) | | 3330 | 21.8 |
| Oak, red | 4888 | 3528 | 24.6 |
| Oak, white | 5573 | 4200 | 29.1 |
| Oak, Gambel | | | 30.7 |
| Maple, silver | 3904 | 2752 | 19.0 |
| Maple, other | 4685 | 3680 | 25.5 |
| Boxelder | 3589 | 2632 | 18.3 |
| Alder | | 2540 | 17.5 |
| Birch | 4312 | 2992 | 20.8 |
| Beech | | 3760 | 27.5 |

Derived: heat ÷ dry weight is about 6,900–7,000 Btu/lb for most rows (red oak 6,973; ponderosa
6,935; white pine 7,067), well under 8,600 Btu/lb oven-dry: the column is a recoverable or
as-burned figure on an unstated basis, so use the **dry weights** (as `cord_weight`) with a
heating value from [W1]–[W3], not the heat column, in the engine. Pinyon (9,033) and lodgepole
(8,084) don't follow the pattern (Flagged).

Ceramics Monthly (Gaddie and Coppage, "Techno File: By Weight, Not Volume", December 2021,
<https://ceramicartsnetwork.org/ceramics-monthly/ceramics-monthly-article/techno-file-by-weight-not-volume>)
quotes the same pine (2250 lb, 15.9 million Btu) and oak (4200 lb, 29 million) figures, uncited.

Not found: eucalyptus, and scrap lumber or pallets, in any source read. Kiln-dried lumber's heating
value per oven-dry kg is the wood's own; its moisture is lower (§2).

## 2. Moisture

**Wet basis**: w = water ÷ (wood + water). **Dry basis**: u = water ÷ oven-dry wood; w = u ÷ (1 + u)
(definition). [W1]'s 75 % and 20 % are oven-dry basis (it says so); [W2]'s are wet basis
(FR gives log wood at 20 % MC as 14.7 GJ/t, which only the wet basis reproduces, below).

**The formula the engine uses** ([W3], eq. 3): H(w) = [H(dry)·(100 − w) − 2.44·w] ÷ 100 MJ/kg, w in
%, H the net calorific value. "The constant '2.44' results from the evaporation energy of water."
(The equation is an image on the page; its symbols, H_u(w), H_u(wf) and w, and the constant are in
the text; the form is the standard one and checks against [W2].)

Check (derived): 19 × 0.80 − 2.44 × 0.20 = 14.71 MJ/kg, FR's 14.7 for logs at 20 %; 19 × 0.70 −
2.44 × 0.30 = 12.57, FR's 12.5 for chips at 30 %. H(w) = 0 at w = 19 ÷ 21.44 = 88.6 %, FAO's "about
88 %".

Typical moisture: green, "50% or more water by weight" [W4] (wet basis); freshly cut Missouri
hardwood 75 % oven-dry basis (43 % wet, derived) [W1]; air-dried, 12–20 % [W3], 20 % [W1], [W2].
Not found: a kiln-dried lumber moisture in a source read here.

The engine takes `heating_value` as **net, oven-dry**. A gross (higher) value would need the
water formed from the wood's hydrogen subtracted; no source read here gives wood's hydrogen
content, so the engine doesn't convert, and says net in the field's description.

## 3. Efficiency of a wood kiln firebox

Not found: any source giving a kiln firebox's efficiency (share of the wood's heat into the
kiln's walls and ware). Olsen gives fuel per firing ([§4]) but no efficiency.

A bounded analogue only, **not a kiln**: heating appliances, [W1]: masonry fireplace about 10 %;
fireplace insert up to 40 %; non-airtight stove about 25 %; airtight stove 55 %; advanced
combustion stove 60–72 % advertised; gasification heater up to 80 %; masonry heater 90 %;
"wood-fired units overall: 10% to 90%". A kiln's flue gas leaves at the kiln's temperature (over
1200 °C at cone 10), far hotter than a stove's, so a kiln's share is likely lower than a stove's;
that is reasoning, not a source.

A model check the user can run: the engine's propane firing of the same kiln burns fuel_kwh for
energy_kwh into the kiln, so energy ÷ fuel is the gas firing's own efficiency at that schedule
(Cantera's available heat). That is propane's, not wood's.

## 4. Wood consumption of real kilns, to check a model against

- **Olsen, The Kiln Book, 4th ed., p.139, p.143** (kiln-reference.md §Fast-fire): a 12–16 ft³
  fast-fire downdraft reaches cone 10 in 3½ h on "less than a quarter of a cord of wood for a 3½ to
  4-hour firing" (p.143); a 40 ft³ hard-brick kiln averages 12–14 h (p.143); a logged firing took
  4 h 45 min (p.309).
- **Sullivan and Sullivan, US Patent 7,357,632 B1**, "Automated wood-fired pottery kiln", filed
  2006-01-20, granted 2008-04-15, background: "a minimum-sized wood kiln might require a cord or
  more of wood", "a total attended firing time of 24 to 48 hours"; its embodiment, about 3.75 ft³,
  reaches cone 10 on 100 lb of wood pellets in 9 h. <https://patents.google.com/patent/US7357632>
- **Ceramics Monthly**, December 2021 (above): a large wood kiln "could consume anywhere from 1½ to
  5 cords of wood" a firing; size and duration not given.

Example check (derived, not a test): ¼ cord of white pine at USU's 2250 lb is 562 lb = 255 kg
oven-dry; at 19 MJ/kg that is 4,850 MJ = 1,350 kWh net.

## 5. Air for wood

Olsen, p.197 (kiln-reference.md §Air): "about 10 ft³ of air per 1000 BTU for any fuel". Not found:
a wood-specific stoichiometric air (kg air per kg wood) in a source read here; the Cantera model
(ADR 0012) has no wood mechanism, so the engine doesn't model wood combustion.

## Not found / not read

- FPL Fuel Value Calculator (Techline; "seasoned firewood 15.3 million Btu/cord", seen only in
  search snippets of mirrored copies): the PDF couldn't be read.
- Baker, "Wood fuel properties and fuel products from woods" (FPL, 1983) and White, "Effect of
  lignin content and extractives on the higher heating value of wood" (FPL, 1987): scanned PDFs,
  not read. A search snippet gives White's averages, 8,890 Btu/lb (softwoods) and 8,529 Btu/lb
  (hardwoods), higher heating value, unextracted: unverified, so not tabled.
- USDA Wood Handbook: not consulted for heat of combustion.
- Engineering ToolBox's per-cord table: it cites no primary source, so it is left out.
- Eucalyptus, pallets and scrap lumber values; kiln-dried lumber's moisture; wood's hydrogen
  content; a kiln firebox efficiency.
