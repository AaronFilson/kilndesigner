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

Not found: eucalyptus's heating value (its density is in §6), and scrap lumber or pallets, in any source read. Kiln-dried lumber's heating
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

## 6. Hawai'i

Read 2026-11-09, for a Hawai'i kiln burning wood seasoned about a year. Starting values only, as
the rest of this file: the user's own wood replaces them.

### Firewoods and their density

**[H1] Little, E. L., Jr. and Skolmen, R. G., *Common Forest Trees of Hawaii (Native and
Introduced)*, USDA Forest Service Agriculture Handbook 679, 1989**; reprinted by UH CTAHR, 2003,
one PDF per species under <https://www3.ctahr.hawaii.edu/gsp/doc/Forestry/Little_Skolmen_CFT/>
(file `CFT_<Genus>_<species>.pdf`). The handbook doesn't state the basis of its specific
gravities (FPL's usual one is oven-dry weight over green or 12 % volume): read them as about ±10 %.

| Species | Hawai'i name | sp. gr. [H1] | Firewood use, as [H1] words it |
|---|---|---|---|
| *Prosopis pallida* | kiawe, algarroba | 0.85 | "very heavy (sp. gr. 0.85), extremely hard … Its most common uses are charcoal, fuelwood, and fence posts"; "the most common tree in the lowland dry zone", about 90,000 acres |
| *Eucalyptus robusta* | robusta, swamp-mahogany | 0.6 | "Moderately heavy (sp. gr. 0.6) but quite variable in density … interior of logs … (sp. gr. 0.35), while that near the log surface may be heavy (sp. gr. 0.8)"; "Hawaii's most plentiful exotic timber species" |
| *Eucalyptus saligna* | saligna, Sydney bluegum | 0.61 | "Moderately heavy (sp. gr. 0,61)"; "Now, this is the main species in biomass fuelwood plantations in Hawaii." |
| *Eucalyptus grandis* | rosegum | 0.57 | "averages moderately heavy (sp. gr. 0.57)"; most Hawai'i trees are hybrids with *E. saligna* |
| *Casuarina equisetifolia* | ironwood, horsetail casuarina | 0.81 | "very hard, heavy (sp. gr. 0.81)"; "In Hawaii, the wood is used only as fuel." |
| *Psidium cattleianum* | strawberry guava, waiawi | not given | "A fine-textured, moderately heavy wood used only for fuelwood in Hawaii." |
| *Grevillea robusta* | silk-oak | 0.57 | "of moderate density (sp. gr. 0.57)"; furniture and paneling, no fuel use stated |
| *Acacia koa* | koa | 0.55 | "moderately heavy wood (sp. gr. 0.55)"; a cabinet wood, "Hawaii's best known wood", no fuel use stated (too valuable to burn, by its uses; not a source) |
| *Schinus terebinthifolius* | Christmas berry | not found | [H1]'s PDF for it returned 404; no density read |

**Oven-dry weight of a cord** (derived): sp. gr. × 62.4 lb/ft³ (water) × 65–90 ft³ of solid wood
in a 128 ft³ cord ([W1], §1). Kiawe's crooked stems ([H1]: "often angled and fluted, twisted, and
crooked") put it at the low end.

| Species | lb/ft³ | 65 ft³ | 80 ft³ | 90 ft³ |
|---|---|---|---|---|
| Kiawe (0.85) | 53.0 | 3,450 | 4,240 | 4,770 |
| Ironwood (0.81) | 50.5 | 3,290 | 4,040 | 4,550 |
| Saligna (0.61) | 38.1 | 2,470 | 3,050 | 3,430 |
| Robusta (0.6) | 37.4 | 2,430 | 2,990 | 3,370 |
| Rosegum, silk-oak (0.57) | 35.6 | 2,310 | 2,850 | 3,200 |
| Koa (0.55) | 34.3 | 2,230 | 2,750 | 3,090 |

**[H2] NFTA 87-05, "Prosopis pallida: pioneer species for dry, saline shores"**, Nitrogen Fixing
Tree Association, October 1987 (now Winrock/FACT Net).
<https://winrock.org/prosopis-pallida-pioneer-species-for-dry-saline-shores/>: "Kiawe's wood is
very dense (old trees to .85 specific gravity) and is challenging to cut but burns slowly almost
smokeless and with little ash (NAS 1980)." So 0.85 is old trees' upper value: young kiawe weighs
less.

### Heating value

**[H3] Oduor, N. M. and Githiomi, J. K., "Fuel-wood energy properties of *Prosopis juliflora* and
*Prosopis pallida* grown in Baringo District, Kenya"**, African Journal of Agricultural Research
8(21), 2476–2481, 6 June 2013, doi:10.5897/AJAR08.221.
<https://www.fornis.net/sites/default/files/documents/Fuel-wood%20energy%20properties%20of%20prosopis%20spp%20in%20baringo%20district%20Oduor%20and%20Githiomi.pdf>
Table 1: *P. pallida* wood, moisture 8.11 %, calorific value "4.862" "(Kcal)"; method: "The gross
calorific value … determined on adiabatic bomb calorimeter", 1 g samples, result in "CV (Cal/g)"
(their eq. 4). Density of *P. pallida* wood 834 kg/m³ (citing Oduor and Githiomi 2004). Kenyan
trees grown partly from Hawai'i seed.

Read as 4.862 kcal/g, it is 20.3 MJ/kg **gross**, at 8 % moisture (derived, × 4.1868). Flagged:
the unit is printed as "Kcal" and the sample basis isn't plain, and the engine needs a **net**,
oven-dry value, which needs the wood's hydrogen (§2, not found). So it isn't used; it is
consistent with [W2]'s generic 19 MJ/kg net. Not found: a heating value for eucalyptus, ironwood,
strawberry guava or Christmas berry in a source read here.

### Moisture after a year's air drying

**[H4] Simpson, W. T., "Equilibrium moisture content of wood in outdoor locations in the United
States and worldwide"**, Res. Note FPL-RN-0268, USDA Forest Service, Forest Products Laboratory,
August 1998. <https://research.fs.usda.gov/download/treesearch/5913.pdf>. Monthly EMC "of wood
exposed to the outdoor atmosphere but protected from direct precipitation or sun", from NOAA
(NCDC) humidity and temperature normals, "at least 30 years of observation", through the FPL
sorption model. EMC is on the **dry basis** (moisture over oven-dry wood). Table 2, Hawai'i, %:

| Station | Jan | Feb | Mar | Apr | May | Jun | Jul | Aug | Sep | Oct | Nov | Dec | Mean (derived) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Hilo | 13.7 | 13.5 | 13.9 | 14.3 | 14.0 | 13.3 | 14.1 | 14.3 | 13.8 | 14.1 | 14.6 | 14.3 | 14.0 |
| Honolulu | 13.3 | 12.8 | 11.9 | 11.3 | 10.8 | 10.6 | 10.6 | 10.7 | 10.8 | 11.3 | 12.1 | 12.9 | 11.6 |
| Kahului | 13.5 | 13.2 | 12.6 | 12.1 | 11.5 | 11.1 | 11.5 | 11.5 | 11.4 | 11.8 | 12.5 | 13.1 | 12.2 |
| Lihue | 14.1 | 13.8 | 13.5 | 13.5 | 13.1 | 12.9 | 13.0 | 13.1 | 13.1 | 13.5 | 14.1 | 14.1 | 13.5 |

On the wet basis (w = u ÷ (1 + u), §2): 10.6–14.6 % dry is **9.6–12.7 % wet**; the annual means,
11.6–14.0 % dry, are **10.4–12.3 % wet**. [H4] warns that high-extractive tropical woods sit lower
at high humidity, and that hysteresis can move EMC by up to 3 %.

**[H5] Boone, R. S., "Moisture content of wood for interior use … Douglas-fir and robusta
eucalyptus samples studied"**, Res. Note PSW-RN-152, Pacific Southwest Forest and Range Experiment
Station, 1967. <https://research.fs.usda.gov/treesearch/37891>. Indoors on Oahu, 19 sites:
"Minimum EMC at nonair-conditioned locations was 10 percent … Maximum EMC at nonairconditioned
locations was 16 percent".

EMC is the floor drying approaches, not a promise of a year: whether split kiawe reaches it in a
year isn't in a source read here (assumed; uncovered or unsplit wood stays wetter). Not found: a
UH CTAHR firewood-seasoning guide.

### Price

Not found: a dated public price per cord of Hawai'i firewood. A directory site (firewood360.com)
quotes kiawe at $250–400 a cord without date or source, and Oahu sellers price by the box or rack;
neither is used.

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
