# Grates and fuel beds: burning rates, air openings and the bed's resistance

Part A3 of the round (`docs/planning/11-10-26.md`), with the grate side of A2: open sources for how
fast a hand-fired grate burns wood and coal, how hand-fired furnaces size their air openings, how
hard the fuel bed resists the air, and fire research's ventilation-controlled burning as an analogue
of a firebox fed through its stoke hole or ash-pit mouth. Olsen's own firebox, grate, air and coal
rules are in `kiln-reference.md` §14–16, Norsker's flue and chimney rules in `kiln-hardware.md` §3
([S14]), the draft equation in `combustion-and-masonry.md` §4.2: not repeated here.

Read 2026-11-10. The texts were read as archive.org OCR and Project Gutenberg plain text through a
fetch tool that quotes at most 125 characters at a time, so long sentences are quoted in pieces and
joined here; OCR slips are kept, marked [sic] or bracketed. The tool can't read PDFs (page scans or
compressed text), so every PDF-only source is under "Not found / not read", its search snippets
marked as such. Marks: **Read** (on the fetched text), **Snippet** (a search snippet or the tool's
paraphrase or reading of garbled OCR, not checked), **Derived** (working shown).

Conversions (Derived): 1 lb/(ft²·h) = 0.45359 kg ÷ 0.092903 m² = 4.882 kg/(m²·h); 1 in. w.c. =
249.09 Pa (as `combustion-and-masonry.md` §4.2); 4 in² per ft² = 25.81 cm² ÷ 929.0 cm² = 2.78 % of
the grate; 1 Btu/lb = 2.326 kJ/kg; 1 Btu/h = 0.29307 W; 1 ft = 0.3048 m. Where a source gives a
wood's moisture but no heating value, the net value as fired is FAO eq. 3 with 19 MJ/kg oven-dry
(`wood-fuel.md` §2), taking the moisture as wet basis (an assumption: the old sources don't say).

## Short answers

| Quantity | Source's value | SI (Derived) | Basis | Source | Mark |
|---|---|---|---|---|---|
| Coal, potters' kiln firebox, "most efficient" rate | 95–145 kg/(m²·h) | 95–145 kg/(m²·h) (19.5–29.7 lb/(ft²·h)) | hand-stoked; coal and draft not stated | [G1] §2.3.4 | Read |
| Coal, Khurja downdraft kiln, average | 85 kg/(m²·h) | 85 kg/(m²·h) | same | [G1] §2.3.4 | Read |
| Rice husk, inclined grate 40 × 100 cm | 650 kg in 8 h, 1 m³ kiln to 1100 °C | 203 kg/(m²·h) as fired | hand-fed, grate at 50° | [G1] §2.3.3 | Read; rate Derived |
| Coal against the draft between ash pit and furnace | 0.10–0.50 in.: bituminous 10–36 lb (Ky., Pa., Tenn.), 11–41 lb (Ill., Ind., Kan.); anthracite No. 3 3.5–12 lb | 25–125 Pa: 49–176, 54–200, 17–59 kg/(m²·h) | hand-fired, natural draft, "maximum economical" | [G5] Table 29 | Read |
| Coal against the draft over the fire | 28 lb at ½ in.; 20 lb at ¼ in. | 137 kg/(m²·h) at 125 Pa; 98 at 62 Pa | worked example, bed resistance fixed, rate ∝ √draft | [G3] p.28 | Read |
| Draft over the fire, power plants | ⅛–½ in. (breeching ¾–1 in.) | 31–125 Pa | stacks 100–150 ft | [G3] p.26 | Read |
| Design rates, chimney draft | anthracite 10 lb, bituminous 15 lb | 49, 73 kg/(m²·h) | "as liberal as possible" a grate | [G4] p.888 | Read |
| Thurston's rule, anthracite | rate = 2√h − 1 lb/(ft²·h), h stack height ft: 13.1 at 50 ft, 19 at 100, 27.3 at 200 | 64, 93, 133 kg/(m²·h) at 15, 30, 61 m | natural draft | [G4] p.947 | Read |
| Draft for No. 1 buckwheat anthracite (Ennis) | 0.3, 0.45, 0.7, 1.0 in. for 10, 15, 20, 25 lb | 75–249 Pa for 49–122 kg/(m²·h) | | [G4] p.947 | Read |
| Sawmill refuse (hogged wood, sawdust, slabs) | 150 lb/(ft²·h) at 30–40 % moisture | 732 kg/(m²·h); 2.1–2.6 MW/m² at 10.4–12.6 MJ/kg net | extension furnace, fuel piled 3–4 ft, "proper draft", strong natural draft preferred | [G2] Wood | Read; MW Derived |
| Cord wood and slabs | "higher" than refuse; no figure | — | open fire, less air friction; grates ~5 ft deep | [G2] Wood | Read |
| Bagasse, ~50 % moisture | 250–300 lb at 0.3 in. natural draft; 450 lb at 0.5 in. blast | 1,220–1,460 kg/(m²·h) at 75 Pa; 2,200 at 125 Pa; 2.6–3.1 MW/m² natural | not wood: high-moisture biomass | [G2], [G4] p.840 | Read; Derived |
| Forced draft, coal | tests 20–185 lb; 120 lb on 6 in. beds; locomotives 50–225 lb | 98–903; 586; 244–1,099 kg/(m²·h) | blower or exhaust | [G6], [G7], [G5] | Read |
| Modern moving or forced biomass grates | 1–2 MW/m² fuel fired | — | not hand-fired | [G15] | Read (uncited) |
| Free air space through the grate | 30–50 % of grate area, "the larger the better" | — | coal (clinker) | [G4] p.889 | Read |
| Grate gaps | soft coal ≥ ½ to ¾ in.; buckwheat 3/16–5/16 in.; Norsker: wood 15–20 cm, coal 2.5–4 cm | 13–19 mm; 5–8 mm; 150–200 mm; 25–40 mm | | [G3] p.37; [G2]; [G1] | Read |
| Free air space of a wood grate, % | not found | | Gebhardt's Table 38 lists wood; values unreadable | [G5] | — |
| Over-fire air through the fire doors | 4 in² per ft² of grate | 2.78 % of grate area (278 cm²/m²) | Chicago settings, hand-fired, smokeless | [G5] p.198 | Read; % Derived |
| Air through the bed against over it | about ½ and ½: the bed passes about 7 lb air per lb coal gasified of about 15 needed | | coal, 3–185 lb/(ft²·h), independent of rate | [G3] p.17; [G6] pp.8–9; [G8] pp.7–10 | Read |
| Excess air, wood firebox | 50–100 % on primary air only; 30–50 % with secondary | | | [G1] §2.3.2 | Read |
| Bed resistance | Wⁿ = C·P, n ≈ 1.7; P doubles with the bed (6 → 12 in.) | P ∝ W^1.7 | coal, coke, 1 in. pieces | [G6] pp.55–59 | Read |
| Rate ∝ draftᵏ | k = 0.5 [G3]; 0.59 [G6]; 0.76–0.82 [G5], [G4] | | coal | §3 | Derived |
| Kawagoe, ventilation-controlled wood | R = 5.5 A√H kg/min; air 0.5 A√H kg/s | 0.0917 kg/s per m^5/2 | A m², H m; wood cribs in a room | [G16] via [G14] | Snippet; SI Derived |
| Same regime in COMPF2 | m_p ≈ 0.12 A√h kg/s; discharge coefficient 0.68 | 7.2 kg/min per m^5/2 | crib data of Nilsson, Yamashika | [G11] Eq. 20 | Read (OCR rough) |
| Ventilation-limited heat release | about 1500 A√H kW | 0.5 × 0.23 × 13.1 MJ/kg = 1.51 MW | 13.1 MJ per kg O₂ | [G14] | Snippet; check Derived |
| Free-burning crib | R·b^1.6 ≈ 0.62 (R % per s, b cm) | b = 2.54 cm: 8.4 % of the pile per min | sticks 0.16–9.15 cm, open air | [G12] | Read; example Derived |

## 1. Burning rates on hand-fired grates

### Coal, natural draft

**[G1] Norsker, H., *The Self-Reliant Potter: Refractories and Kilns***, GATE / F. Vieweg,
Braunschweig, 1987 (= [S14] in `kiln-hardware.md`). OCR text at
<https://archive.org/details/the-self-reliant-potter-refactories-and-kilns> (file "The Self Reliant
Potter; Refactories and Kilns_djvu.txt"); §2.1.13, §2.3.2–2.3.4 and §2.4.5 read. The OCR prints m²
as "m?". §2.3.4, coal fireboxes (Read): "The most efficient combustion takes place when the burning
rate is about 95—145 kg per m² grate area per hour"; "The Khura [sic: the Khurja kiln, p.51]
down-draught kiln burns on average 85 kg/m² per hour." The coal and the draft aren't given. Stoking
(second technique, burnt coal pushed back and fresh coal fired in front): "... then every 45 minutes
to 1 hour up to 1200 °C and finally every 30 minutes." Derived: 95–145 kg = 19.5–29.7 lb/(ft²·h).

**[G3] Kreisinger, H., *Hand Firing Soft Coal under Power-Plant Boilers***, US Bureau of Mines
Technical Paper 80, GPO, 1915 (title page: first edition October 1914).
<https://archive.org/details/pub_usgov-bmines-technical-paper_0080>. Read: p.28, "If the resistance of
the fuel bed could be kept constant, the air supply through the fuel bed, and therefore the rate of
combustion, would vary approximately as the square root of the draft over the fire. Thus, if with a
draft over the fuel bed of one-half inch of water the rate of combustion is 28 pounds of coal per
square foot of grate per hour, then with the draft one-fourth of an inch and with the same resistance
as before the rate of combustion would be 20 pounds. In a hand-fired furnace it is difficult if not
impossible to keep the resistance of the fuel bed constant." p.26: "The average draft in the breeching
in plants having stacks 100 to 150 feet high is three-fourths to 1 inch of water. The draft over the
fire varies from one-eighth to one-half of an inch of water." p.29: "No more coal can be burned than
there is air for, no matter how much is shoveled into the furnace." p.7: "The best thickness of the
fires is 4 to 10 inches, depending on the character of the coal and the strength of draft." p.16, per
firing, not per hour: with "about 1 inch of water" available, "2 to 24 [2½?] pounds of coal fired per
square foot of grate is a fair average" (OCR). Derived: 137 kg/(m²·h) at 124.5 Pa; 98 at 62.3 Pa.

**[G4] Kent, W. and Kent, R. T., *The Mechanical Engineers' Pocket-Book***, Wiley, 1916.
<https://archive.org/details/mechengpockbook00kentrich> (US public domain per the record). Read:
pp.886–888, "Grate-surface": the grate needed is "extremely variable, depending chiefly upon the
character of the coal and upon the rate of draught"; "the grate-surface should be made as liberal as
possible, say sufficient for a rate of combustion of 10 lbs. per square foot of grate for anthracite,
and 15 lbs. per square foot for bituminous coal"; "With coals high in ash, especially if the ash is
easily fusible, tending to choke the grates, large grate-surface and a slow rate of combustion are
required". p.947: "Thurston's rule for rate of combustion effected by a given height of chimney ... is:
Subtract 1 from twice the square root of the height, and the result is the rate of combustion in
pounds per square foot of grate per hour, for anthracite", tabled from 13.14 lb at h = 50 ft to 27.28
lb at 200 ft; "W. D. Ennis (Eng. Mag., Nov., 1907), gives the following as the force of draught
required for burning No. 1 buckwheat coal": 0.3, 0.45, 0.7, 1.0 in. of water for 10, 15, 20, 25 lb.

**[G5] Gebhardt, G. F., *Steam Power Plant Engineering***, Wiley, 1917.
<https://archive.org/details/steampowerplante01gebh>. Read, §76, pp.152–153: "A liberal allowance of
grate surface is desirable for hand-fired furnaces with natural draft"; "For a general set of
conditions the rate of combustion is primarily a function of the pressure difference between the ash
pit and furnace, and is approximately as shown in Table 29." Table 29, "MAXIMUM ECONOMICAL RATE OF
COMBUSTION" (no source credited), lb of coal per sq. ft. of grate per hour against "Force of Draft
between Furnace and Ash Pit, Inches of Water":

| Coal | 0.10 | 0.15 | 0.20 | 0.25 | 0.30 | 0.35 | 0.40 | 0.45 | 0.50 |
|---|---|---|---|---|---|---|---|---|---|
| Anthracite, No. 3 | 3.5 | 5.0 | 6.2 | 7.2 | 8.2 | 9.0 | 10.0 | 11.0 | 12.0 |
| Anthracite, No. 2 | 5.5 | 7.2 | 9.0 | 10.5 | 11.8 | 13.0 | 14.2 | 15.5 | 16.5 |
| Anthracite, pea | 8.0 | 9.2 | 11.5 | 13.5 | 15.0 | 17.0 | 18.5 | 20.0 | 21.5 |
| Semi-bituminous | 9.5 | 13.0 | 16.0 | 19.0 | 23.0 | 25.0 | 27.0 | 30.0 | 32.0 |
| Ky., Pa. and Tenn. bituminous | 10.0 | 14.0 | 18.0 | 21.0 | 24.0 | 27.0 | 30.0 | 33.0 | 36.0 |
| Ill., Ind. and Kan. bituminous | 11.0 | 15.0 | 20.0 | 24.0 | 28.0 | 32.0 | 35.0 | 38.0 | 41.0 |

"With forced draft these rates of combustion may be greatly increased." Christie's tests: "13 pounds
of anthracite per square foot of grate per hour for maximum efficiency and 24 pounds of bituminous."
Derived: 0.10–0.50 in. = 24.9–124.5 Pa; × 4.882 for kg/(m²·h).

**[G2] Babcock & Wilcox Co., *Steam: Its Generation and Use***, 35th ed., 4th issue, © 1919;
Project Gutenberg eBook 22657, <https://www.gutenberg.org/ebooks/22657> (the text has no page
numbers; sections named). Read, "Chimneys and Draft", Rate of Combustion: "The amount of coal which
can be burned per hour per square foot of grate surface is governed by the character of the coal and
the draft available." The draft against rate is a figure, "Draft Required at Different Combustion
Rates for Various Kinds of Coal" (Fig. 34, values not read); its worked problem, bituminous coal on
stokers at "1.60 × 22 = 35 pounds per square foot of grate surface per hour": "The furnace draft
required for the combustion rate, from the curve, Fig. 34, is 0.6 inch." "Combustion of Coal":
bituminous "fresh coal should be fired at intervals of 10 to 20 minutes"; "Kentucky, Tennessee, Ohio
and Illinois coals require a thickness from 4 to 6 inches"; anthracite beds reach "12 or 14 inches
just before a cleaning period". Derived: 35 lb at 0.6 in. = 171 kg/(m²·h) at 149 Pa.

### Wood and other biomass

[G2] B&W, "Solid Fuels other than Coal", Wood (Read). Sawmill refuse ("In such refuse the moisture
may run as high as 60 per cent"): "With proper draft conditions, 150 pounds of this fuel containing
about 30 to 40 per cent of moisture can be burned per square foot of grate surface per hour, and in a
properly designed furnace one square foot of grate surface can develop from 5 to 6 boiler horse
power. Where the wood contains 50 per cent of moisture or over, it is not usually safe to figure on
obtaining more than 3 to 4 horse power per square foot of grate surface." Its furnace: "Extension
furnaces of the proper size are usually essential", "grates dropped to the floor line with an ashpit
below", "A thick fuel bed is necessary in order to avoid excessive quantities of air passing through
the boiler", fuel piled "to a height of 3 or 4 feet in the form of a cone under each chute", each
chute serving "about 30 or 35 square feet of grate surface"; "A strong natural draft usually is
preferable to a blast with this fuel." Cord wood: "Cord wood and slabs form an open fire through which
the frictional loss of the air is much less than in the case of sawdust or hogged material. The
combustion rate with cord wood is, therefore, higher and the grate surface may be considerably
reduced. Such wood is usually cut in lengths of 4 feet or 4 feet 6 inches, and the depth of the grates
should be kept approximately 5 feet"; "Air is admitted under the grates through an excavated ashpit";
the walls "corbelled out to cover about one-third of the total grate surface". No cord-wood rate is
printed. "When newly cut, wood contains moisture varying from 30 per cent to 50 per cent" (basis not
stated). Bagasse, "as fired containing approximately 50 per cent of moisture": "With a natural draft
in the furnace of, say, three-tenths inch of water, a combustion rate of from 250 to 300 pounds per
square foot of grate surface per hour may be obtained. With a blast of, say, five-tenths inch of water
this rate can be increased to 450 pounds".

Derived: 150 lb = 732 kg/(m²·h) as fired. Net value at 30 % and 40 % moisture: 19 × 0.70 − 2.44 × 0.30
= 12.57 and 19 × 0.60 − 2.44 × 0.40 = 10.42 MJ/kg, so 732 × 10.42–12.57 = 7,630–9,210 MJ/(m²·h) =
**2.1–2.6 MW/m²**. Bagasse: 1,220–1,460 kg/(m²·h) at 74.7 Pa; 2,200 at 124.5 Pa; with Kerr's net 3256
Btu/lb ([G4] below; net also of heating the vapour to 594 °F, so below a plain net value) = 7.57
MJ/kg, 2.6–3.1 MW/m² natural draft and 4.6 MW/m² blast.

[G4] Kent, about p.840 (leaf 900), quoting E. W. Kerr, Louisiana Agr. Exp. Sta. Bull. 117 (Read): a
bagasse of "net calorific value of 3256 B.T.U."; "For the best results the bagasse should be burned at
a high rate of combustion, at least 100 lb. per sq. ft of grate per hour." Kent's "Wood as Fuel"
(pp.820–841) gives no grate rate for wood.

[G1] Norsker gives no burning rate for wood (Read, §2.3.2). Rice husk, §2.3.3: "A grate measuring 40 x
100 cm fired a 1 m³ kiln to 1100 °C with rice husks in eight hours consuming 650 kg husks"; "The grate
is set at an inclination of 50°." Derived: 650 ÷ 8 = 81 kg/h on 0.40 m² = **203 kg/(m²·h)**. The
Champaknagar chamber kiln (§2.1.13, wood): "The first two chambers consume 2200 kg firewood and each
additional chamber about 500 kg"; "Each additional chamber reaches 1100 °C after about two hours'
stoking" (Derived: about 250 kg/h into a side-stoked chamber; no grate area is printed).

**[G9] Bourry, E., *A Treatise on Ceramic Industries***, 2nd English ed. revised (with A. B.
Searle), Scott, Greenwood & Son, London, 1911. <https://archive.org/details/treatiseoncerami00bouriala>.
Read pp.194–209: his wood fireplace and the coal furnace fireplaces are described with no rate, grate
area or opening size. p.195: "The air enters by a lower passage which forms an ashpit"; "A part of the
fuel, falls into this ashpit and is consumed there while heating the air"; "The combustion takes place
by the air passing between the logs"; "The embers which fall to the bottom of the fireplace help the
burning, owing to the air entering through the ashpit door"; "For slow firing, the logs must be
replaced by faggots, or the upper opening may be closed with a damper." p.199 (coal): "There is an
extra supply of air entering on each side and heated by circulating through channels placed in the
side walls of the furnace."

### Forced draft, the largest rates, and what limits a grate

**[G6] Kreisinger, H., Ovitz, F. K. and Augustine, C. E., *Combustion in the Fuel Bed of Hand-Fired
Furnaces***, US Bureau of Mines Technical Paper 137, GPO, September 1916.
<https://archive.org/details/pub_usgov-bmines-technical-paper_0137>. Read: "The rate of combustion was
varied from 20 to 185 pounds of fuel per square foot of grate per hour" (p.8); the air came "under a
pressure of 8 to 20 inches of water by a cupola blower" (p.16); Pittsburgh coal, anthracite and coke,
"sized by passing them over 1-inch square-mesh screen" (p.17), on 6 and 12 in. beds. pp.8–9: "The
larger the quantity of air forced through the fuel bed, the faster the fuel burns or gasifies"; "it is
not necessary with the ordinary rates of combustion to run a fuel bed thicker than 4 to 6 inches"; "A
thick fuel bed, therefore, reduces the rate of combustion and thus reduces the capacity of the
boiler." p.51: "the rate of combustion varies directly with the rate of feeding air through the grate."

**[G7] Kreisinger, H., Augustine, C. E. and Ovitz, F. K., *Combustion of Coal and Design of
Furnaces***, US Bureau of Mines Bulletin 135, GPO, October 1917.
<https://archive.org/details/combustionofcoal00krei>. Read, pp.3–4: "The gases rising from a level fuel
bed contain 15 to 32 per cent of combustible gases, about 8 per cent of carbon dioxide, and practically
no free oxygen. This is true of even 6-inch fuel beds and rates of combustion as high as 120 pounds of
coal per hour per square foot of grate." Its tests burned coal "at five rates—20, 30, 40, 50, and 60
pounds per square foot of grate per hour" (p.6) on "25 square feet of projected grate area", with a fan
that "could maintain a pressure of 1 inch of water in the ash pit" (pp.10–11).

[G5] Gebhardt, locomotives (Read, in the §76 tables; page not recorded): "Maximum rate 225", "Very high
rate 150", "Average high rate 100", "Average rate 80", "Economical rate 60", "Low rate 50", lb of coal
per sq. ft. of grate per hour. Derived: 244–1,099 kg/(m²·h).

Modern grates, moving or forced-air, not hand-fired: **[G15] Wikipedia, "Grate firing"**,
<https://en.wikipedia.org/wiki/Grate_firing> (Read 2026-11-10): "Fuel fired per grate area 1-2 MW/m2,
maximum grate area 100 m2"; "A moving grate which is covered with a fuel layer, 10-30 cm." No citation
on the line; the nearest is EN 12952-16:2022 (not read). Snippets only: a Babcock & Wilcox leaflet
(PS201-113, water-cooled vibrating grate) up to 2.5 MW/m² [G19]; a mirror of a US Unified Facilities
Criteria chapter (`3_430_08`): "in wood burning applications, heat releases have been as high as
1,000,000 Btu/square foot/hr of active grate area" [G18] (Derived: 293 kW ÷ 0.0929 m² = 3.15 MW/m²).

What limits a grate, as the sources put it (Read): the air ([G3] p.29; [G6] p.51); "the character of
the coal and the draft available" ([G2]); the bed's thickness and clinker ([G6] pp.8–9, 55–56; [G3]
p.28: read the rate off the draft gauge only with "the thickness of the fuel bed and particularly the
accumulation of clinker" in mind); fusible ash choking the grate, which wants a larger grate and a
slower rate ([G4] p.887). No source read gives a limiting rate for wood logs on a grate.

## 2. Air openings

### Through the grate

[G4] Kent p.889, "Air-passages through Grate-bars" (Read): "The usual practice is, air-opening = 30%
to 50% of area of the grate; the larger the better, to avoid stoppage of the air-supply by clinker; but
with coal free from clinker much smaller air-space may be used without detriment. See paper by F. A.
Scheffler, Trans. A. S. M. E., vol. xv, p. 503." (Scheffler not read.)

[G3] TP 80 p.37, soft coal (Read): "grates containing large air spaces are not only better but are
necessary for the majority of coals"; "The air spaces should not be less than one-half inch wide, and
for some coals should be as wide as three-quarters of an inch. The percentage of air space should be as
high as possible without weakening the grate. [G]rates with 100 per cent air spaces would be the best,
but of course such grates are impossible."

[G2] B&W, anthracite (Read): "Air openings in the grate bars should be made from 3/16 inch in width for
No. 3 buckwheat to 5/16 inch for No. 1 buckwheat"; "A blast up to 3 inches of water should be available
for the finer sizes".

[G1] Norsker (Read). Firewood, §2.3.2: "For firewood the distance between the grates should be 15-20 cm
so that the wood will fall into the ash pit as soon as it is nearly burned out. Otherwise it will block
the access of primary air." "The grate can be made of iron bars but they will soon wear out"; "grates
made of fire-clay bars (fig. 2-50) are more durable" (caption: "Fireclay bars made as long solid
firebricks"). "The ash pit should be as big as or bigger than the space above the grate because a thick
layer of embers is needed to preheat the primary air." "The grate for firewood should be about 15—25 %
of the floor area of the kiln chamber, the 15% sufficient for firings up to 1100 °C and the 25% for
1300 °C and above." Coal, §2.3.4: "The grates are made of iron bars with 2.5—4 cm space in between."
"The grate area of each firebox is within 0.3 — 0.5 m²." "The length is normally 80—90 cm." "The total
grate area of all fireboxes should fall between 12% and 25% of the floor area of the kiln chamber"; "The
top of the firebox arch should be around 80 cm above the grate." "The lower part of the grate should be
at least 50 cm above the floor of the ash pit."

[G5] Gebhardt §85, pp.175–176: "The width of the air space is determined by the size of the fuel to be
used, the average proportions being given in Table 38" ("AIR SPACES AND THICKNESS OF GRATE BARS"; rows
for screenings, anthracite sizes, "Bituminous, average" and "Wood — Slabs, Sawdust, Shavings"). The
figures are scrambled in both scans read (`steampowerplante01gebh`, `in.ernet.dli.2015.153645`): **not
read**. No source read gives a wood grate's free air space as a percentage.

### Over the fire, and the primary and secondary split

[G5] Gebhardt p.198, the note on the No. 8 furnace of the Chicago settings for hand-fired return-tubular
boilers (Read): "Fire doors must provide for special air admission of an area equal to four square
inches for each square foot of grate surface." Derived: 2.78 % of the grate. **[G17]** A Sydney
University Engineering Society paper on hand firing gives "available area of above grate air opening
should not be less than four square inches per square foot of grate area" (Snippet; the PDF is a scan,
<https://openjournals.library.sydney.edu.au/SUES/article/view/2112/2398>, author and year not read).

[G7] Bulletin 135 (Read): "For the best results the secondary air should be introduced as near to the
fuel bed as practicable, and the air should be supplied in a large number of streams at high
velocities" (p.6); the gases rising from the bed "contain 10 to 28 per cent of combustible and
practically no free oxygen", so "additional air must be supplied over the fuel bed"; "If the pressure in
the furnace is nearly the same as that of the outside atmosphere, the additional air must be supplied
under pressure with a blower or some other device" (p.7); over-bed air "must be introduced either
through the firing door or through the coal magazines" (p.57).

The split (Read):
- [G3] TP 80 p.17: "For the complete combustion of each pound of coal fired, it is necessary to supply
  about 15 pounds of air. At atmospheric temperature 1 pound of air occupies a volume of about 13 cubic
  feet, so that with each pound of coal fired there should be supplied approximately 200 cubic feet of
  air. Of this air about one-half is supplied through the grate and fuel bed and one-half through the
  various openings in and around the fire doors."
- [G6] TP 137 pp.8–9: "the ratio between weight of air supplied and weight of fuel burned remains
  constant at about 7 to 1"; "about one-half of the 15 pounds of air used to burn 1 pound of coal in a
  boiler furnace is supplied through the fuel bed; the other half must be supplied over the fuel bed";
  "The composition of the gases is practically independent of the rate of air supply"; in a 6 in. bed
  the oxygen "is all used up in combustion in the first 4 inches from the grate"; at the surface "no
  oxygen, only 6 to 8 per cent of carbon dioxide" and "20 to 32 per cent of combustible gases"; tar and
  soot "about one-fourth of the combustible rising from the fuel bed" (p.49).
- **[G8] Kreisinger, H., Augustine, C. E. and Katz, S. H., *Low-Rate Combustion in Fuel Beds of
  Hand-Fired Furnaces***, BoM Technical Paper 139, GPO, June 1918,
  <https://archive.org/details/pub_usgov-bmines-technical-paper_0139>: rates of "10, 6, and 3 pounds of
  fuel per square foot of grate per hour" (p.8; Derived 15–49 kg/(m²·h)) on 6 and 12 in. beds; "The
  ratio of the weight of air that can be supplied through the grate to a pound of coal gasified remains
  constant at about 7 to 1" (p.10); "only about one-half can be supplied through the grate; the other
  half must be supplied above the fuel bed" (p.7); "in no test did free oxygen penetrate to the upper
  surface of the fuel bed" (p.30).
- [G1] Norsker, wood, §2.3.2: "In case sufficient primary air passes the fuel the combustion will be
  complete, but it would mean an excess of air being 50--100% of the air used for combustion." "This
  excess is reduced to 30— 50% when secondary air completes the combustion." Coal, §2.3.4: "Primary air
  enters under the grate and if the coal bed is thicker than 10 cm, secondary air is needed too for
  complete combustion"; "Channels for secondary air are built into both sides of the firebox so that
  when the secondary air enters above the coal bed it is preheated".
- [G2] B&W, wood refuse: "excess air is as harmful as with coal, and care must be taken that such an
  excess is not admitted through fire doors or fuel chutes".

### Ash pit, stoke hole and doors

No rule sizing an ash-pit door, stoke hole or fire door against the grate or the fuel rate was found.
What the sources give (Read): Norsker, "Stoking is done through a small hole not allowing in excess air"
and "A mousehole letting air into the bottom of the ash pit can regulate the thickness of the embers"
(§2.3.2); his Champaknagar firebox drawing marks "Primary air (7 holes 10 x 10 cm)" and "Stoking hole
(both sides)" (§2.1.13; Derived: 700 cm² of primary air; no grate area printed); B&W's cord-wood furnace
has "large double-deck fire doors" and air "under the grates through an excavated ashpit" [G2]; Bourry's
air comes through the ash pit and its door [G9]. Norsker §2.4.5: "One litre of air at 20 °C will expand
to 4.5 litres when heated to 1250 °C so the cold air entering through the primary and secondary air
inlets needs 4.5 times larger openings after it has been heated in the firebox." Derived check: (1250 +
273) ÷ (20 + 273) = 5.2 at constant pressure, so the printed 4.5 is low (Flagged); as a rule it reads
inlet area ≈ the flues' area ÷ 4.5 to ÷ 5.2 at equal gas speed (a reading, not his words).

## 3. The fuel bed's resistance

[G6] TP 137 gives the one measured relation (Read). p.55: "The two thicknesses of fuel beds used, 6
inches and 12 inches, make two separate groups of points; each lying on a curve having a parabolic
shape, and represented by the following equation: Wⁿ = CP. W = weight of air passing through fuel bed.
C = a constant. P = pressure drop through fuel bed. However, the index of the power [n] is not equal to
2 but only to about 1.7." (The OCR prints the equation "W"= CP" and loses the exponent's symbol.) Fig.
18: "Relation between the pressure in the ash pit (apparent pressure drop through fuel bed) and the
weight of air flowing through fuel bed" (values not read). p.57: "It is usually stated that the
pressure drop through the fuel bed varies as the square of the weight of air passing through it ...
According to figure 18 such rules are only approximate, but can be used safely in figuring the rate of
combustion from pressure drops; that is, the actual rate of combustion is somewhat higher than the
values computed on the basis of squares or square roots." p.59: "when the thickness of fuel bed is
doubled the pressure drop through it is about doubled"; p.60: "with thick fuel beds higher stacks are
necessary". "The presence of clinker and ash in the fuel bed greatly affects its resistance to flow of
air" (pp.55–56); "with the anthracite coal used the pressure drop is higher than with either the
Pittsburgh coal or the coke" (p.57); the ash fused "3 to 4 inches above the grate with 6-inch fuel beds
and even as high as 10 inches with 12-inch fuel beds" (p.60). TP 139's bed pressure drops (Table 3,
item 22) and TP 137's Table 1 are illegible in the OCR.

Rate against draft, rate ∝ draftᵏ (Derived from the Read figures):
- TP 80, k = 0.5 by its statement (28 → 20 lb as ½ → ¼ in.) [G3].
- TP 137, k = 1 ÷ 1.7 = 0.59 [G6].
- Gebhardt's Table 29, 0.10 → 0.50 in.: Ky./Pa./Tenn. ln(36/10) ÷ ln 5 = 0.80; Ill./Ind./Kan. 0.82;
  anthracite No. 3 0.77 [G5].
- Ennis, 0.3 → 1.0 in.: ln(25/10) ÷ ln(1/0.3) = 0.76 [G4].
- Thurston's 2√h − 1, with the draft proportional to the stack's height (`combustion-and-masonry.md`
  §4.2): k → 0.5 for tall stacks [G4].

So k = 0.5–0.82; the steeper values are tables "for a general set of conditions" that state no bed.
Read across: Gebhardt's 24 lb (Ky. bituminous) at 0.30 in. between ash pit and furnace; TP 80's 28 lb
at ½ in. over the fire; B&W's 35 lb (stokers) at 0.6 in. furnace draft.

Wood beds: B&W says only that cord wood and slabs "form an open fire through which the frictional loss
of the air is much less than in the case of sawdust or hogged material" [G2] (Read). **Not found**: a
measured pressure drop through a bed of burning wood against air flow or burning rate.

## 4. A firebox fed through its openings: ventilation-controlled burning

**[G16] Kawagoe, K., *Fire Behavior in Rooms*, Building Research Institute Report No. 27, Ministry of
Construction, Tokyo, Japan, Sept. 1958** (the reference as [G10] prints it): not read. R = 5.5 A√H
kg/min (A the opening's area, m²; H its height, m; wood cribs burning in a room) and the inflow 0.5 A√H
kg/s are in search snippets only, of [G14]: the coefficient "C_F = 5.5" "was measured and valid only for
the wood fuel in Kawagoe's original experiments, which changes with the fuel type"; the inflow
coefficient "is not a fixed value", reported "from 0.40 to 0.61"; with 13.1 MJ per kg of oxygen the law
gives a maximum heat release of "1500AH^1/2 (kW)"; one study found inflow 0.41 A√H kg/s and 1131 A√H kW,
20 % under the law (all Snippet). An older review's imperial form of Thomas's constant, 0.678 lb/min per
ft^5/2 (Snippet; IIT digital library PDF, not read). Measured solid-fuel peaks 1.5–2.5 × the 1500 A√H
maximum (Snippet; Yu et al., *Fire* 8(6):215, 2025, MDPI, 403). Derived: 5.5 kg/min = 0.0917 kg/s per
m^5/2 = 0.622 lb/min per ft^5/2 (× 2.2046 ÷ 3.2808^2.5 = ÷ 19.50); Thomas's 0.678 = 6.0 kg/min; air ÷
fuel = 0.5 ÷ 0.0917 = 5.45 kg/kg, near the 5.9 kg/kg stoichiometric for dry wood in
`firebox-efficiency.md` §4; 0.5 kg/s × 0.23 × 13.1 MJ/kg = 1.51 MW per m^5/2.

**[G10] Gross, D., *Preliminary Results of Experimental Fires in Enclosures***, NBS Report 7327, 23
August 1961, <https://archive.org/details/preliminaryresul7327gros>, pp.2–4 (Read): "It is possible to
interpret the results in terms of a simple analysis of wood-burning such as that presented by Kawagoe";
"From the basic chemistry of cellulose burning and consideration of fluid flow through an opening, the
fuel combustion rate W was shown to be a function of the coefficient of discharge C, the opening area A,
the effective height of the opening H, the temperature difference between the enclosure and the
surroundings, and the volume of exhaust gas per unit weight of fuel G" (the equation is lost in the
OCR); "The location of the neutral zone determines the effective height of the opening." The limit: "a
limiting value of A√H [OCR "A /H~"] was reached beyond which the window no longer limited and the rate
of burning had a constant value equal (very nearly) to the rate of burning of the crib in the open. This
point corresponded for the 50 cm box to about 50% of the box width for a central vertical window and 60%
for a central horizontal window."

**[G11] Babrauskas, V., *COMPF2: A Program for Calculating Post-Flashover Fire Temperatures***, NBS
Technical Note 991, June 1979, <https://archive.org/details/compf2programfor991babr> (Read; OCR
rough). §3: the window's air flow "is obtained from the Bernoulli equation at the window"; "The
discharge coefficient has been determined by Prahl and Emmons [14] to be 0.68 for normal-shaped
windows"; Eq. 8, an approximation of about 0.45–0.50 A√h for the air (the tool's reading of garbled OCR:
Snippet), "has not been employed here"; combustion is "fuel-limited" or "ventilation-limited" by
whichever of Eqs. 5 and 6 is smaller, r being the "stoichiometric air/fuel mass ratio". §4.2: "From the
data of Nilsson [19] and Yamashika [20], a set of simplified relationships has been evolved for the
three crib burning regimes" (fuel surface, crib porosity, room ventilation); "each of the three rates
above are determined and the lowest rate taken as governing"; room ventilation, Eq. 20, m_p ≈ 0.12 A_v
h_v^½ kg/s, a pyrolysis rate (OCR "0.12 A^ /h^", read with the nomenclature). Thin pieces regress at
Eq. 17, v_p ≈ 1.7 × 10⁻⁶ D^−0.6 m/s, D the smallest dimension (the tool's reading of garbled OCR:
Snippet). [19] Nilsson, L., Bulletin 18, Lund Institute of Technology, 1971; [20] Yamashika, S. and
Kurimoto, H., Report of the Fire Institute of Japan No. 41, 1976. Its example crib takes 18.80 MJ/kg dry,
15.07 MJ/kg at 12 % water (Appendix A, inputs). Derived: 0.12 kg/s = 7.2 kg/min per m^5/2, 1.31 × 5.5.

**[G12] Gross, D., "Experiments on the burning of cross piles of wood"**, J. Res. NBS 66C(2), 99–105,
1962; OCR at <https://archive.org/details/jresv66Cn2p99> (Read): "For sticks of square cross section
ranging in size from 0.16 to 9.15 centimeters"; "When the rate of burning, expressed in percent per
second, was multiplied by the stick width raised to the 1.6 power, it was found that the maximum values
of Rb^1.6 were all equal to about 0.62" (b in cm); three regions, "Diffusion-limited combustion, in which
the scaled rate of burning is very nearly proportional to the porosity factor", "free combustion, in
which the scaled rate of burning is independent of the porosity factor", and "nonsustained combustion";
the porosity factor sets the shafts' vent area A_v = b²(10 − n)² against the exposed area A_s = 2nb²[N(2l
− n) + n] (OCR garbled: check the scan); the text gives no threshold value. Woods: Douglas fir 0.428, ash
0.660, mahogany 0.375, balsa 0.190 g/cm³. Derived, free-burning maximum R ≈ 0.62 ÷ b^1.6 % of the pile
per second: b = 2.54 cm, 0.14 %/s (8.4 %/min); 5 cm, 0.047 %/s (2.8 %/min); 9.15 cm, 0.018 %/s (1.1
%/min). Per exposed area, on [G11]'s Snippet v_p (check before use): 428 kg/m³ × 1.54 × 10⁻⁵ m/s = 6.6
g/(m²·s) for D = 2.54 cm.

**[G13] Thomas, P. H. and Nilsson, L., *Fully Developed Compartment Fires: New Correlations of
Burning Rates***, Fire Research Note 979, 1973, <https://publications.iafss.org/publications/frn/979/-1>
(abstract as the fetch tool summarised it: Snippet; the PDF link gave 404): three regimes for crib fires
in compartments, two controlled by the crib's porosity and its fuel surface as in the open, and the
ventilation-controlled one; the ratio of burning rate to the ventilation parameter is "not strictly
constant" and can rise at low values of the ventilation parameter against the internal surface area.

**[G14] Wang, Z., Zhang, T. and Huang, X., "Numerical Modeling of Compartment Fires: Ventilation
Characteristics and Limitation of Kawagoe's Law"**, *Fire Technology*, 2022,
doi:10.1007/s10694-022-01218-1; abstract read at
<https://research.polyu.edu.hk/en/publications/numerical-modeling-of-compartment-fires-ventilation-characteristi/>:
"Numerical results show that the inflow rate and indoor heat release rate comply well with Kawagoe's Law
under ordinary openings with a small aspect ratio. However, Kawagoe's Law becomes less valid for openings
with large aspect ratios and small-gap openings." (Read.) The full text is behind a login.

As an analogue (reasoning, not a source): Kawagoe's A√H comes from buoyancy at the opening, the room's
own hot gas driving the flow through a neutral plane ([G10], [G11]). A kiln firebox has a chimney: its
draft sets the pressure across the stoke hole or ash-pit mouth, so the inflow is the orifice flow C·A·
√(2ρΔp) with C ≈ 0.65–0.70 (`combustion-and-masonry.md` §4.2, [S42]; 0.68 in [G11]), not 0.5 A√H, and
the 5.5 doesn't carry over. What does: the air-limited and the bed-limited regimes with the lower rate
governing [G11]; the open-air rate as the ceiling once the openings stop limiting [G10]; air ÷ fuel near
stoichiometric in the air-limited regime (Derived above); and the warning that wide, low or small-gap
openings, which ash-pit mouths and stoke slots are, lie outside the law's checked range [G14].

## For the kilns

What the comparison with Olsen's grates needs, in units (the comparison is the next section):
- **Grate area** in m² (Olsen prints in² and ft²: 1 in² = 6.452 cm², 1 ft² = 0.0929 m²) and **fuel
  per hour** in kg/h (fuel per firing ÷ firing time: `wood-fuel.md` §4, `kiln-reference.md` §12, §15),
  giving kg/(m²·h) against: coal 85–145 [G1]; coal 17–200 at 25–125 Pa [G5]; 98–137 at 62–125 Pa over
  the fire [G3]; sawmill refuse 732 at 30–40 % moisture [G2]; rice husk 203 [G1].
- **Draft at the grate** in Pa from v2's chimney, to enter Table 29 [G5] or rate ∝ draftᵏ, k 0.5–0.82
  (§3).
- **Heating value and moisture as fired** (A1), turning kg/(m²·h) into MW/m² against 2.1–2.6 MW/m²
  (refuse, [G2]) and 1–2 MW/m² (moving grates, [G15]).
- **Grate bars**: bar width and gap give a bar grate's free area, gap ÷ (gap + bar), against 30–50 %
  [G4]; the gap against 15–20 cm (wood) and 2.5–4 cm (coal) [G1]; total grate ÷ floor against 15–25 %
  (wood) and 12–25 % (coal) [G1], beside Olsen's 1 : 6–8 for coal (pp.76, 206).
- **Air openings**: each ash-pit mouth, mouse hole, secondary-air hole and stoke hole as area (m²) and
  height (m): A√H in m^5/2 for [G16] and [G11], and the draft for the orifice flow; over-fire openings
  ÷ grate area against 2.78 % (4 in²/ft²) [G5]; the half-and-half split, a coal figure [G3], [G6], [G8].

## The reference kilns' grates against these (research A3; Derived)

The kilns' printed grates (Olsen, as the dataset records them) and the rates their printed fuel
implies, averaged; each an estimate with its inputs named (`scratch/research-a/grates.py`,
`grates2.py`, git-ignored). Heating values from `kiln-fuels.md` (A1).

| Kiln | Grate, printed | Fuel and time, printed | Rate, kg/(m²·h) | As heat, MW/m² | Against the sources |
|---|---|---|---|---|---|
| `fast-fire` (wood) | two pull-out grates 24–27 × 12–13 in, 576–702 in² = 0.37–0.45 m² (p.140, p.204); ¾ in rod at 1½ in centres, 50 % free area | under ¼ cord (2,070–4,200 lb oven-dry a cord, `wood-fuel.md` [W4]) in 3½ h (p.139, p.143) | at most 148–366 dry (an upper bound: "less than" ¼ cord) | at most 0.72–1.96 (net 17.6–19.3 MJ/kg) | no wood-log rate in any source; under sawmill refuse's 2.1–2.6 MW/m² [G2], inside modern grates' 1–2 [G15] |
| the same, v2's draft-limited fire (`11-09-26.md` step 2) | as above | 44–65 kg/h dry at the draft's most air, λ 1 | 97–175 dry | 0.47–0.94 | – |
| `singh-coal` | four 24 × 24 in grates, 4 ft² each, 1.49 m² (p.134, p.207) | Table 5-1: five shovels per 50 min per firebox at hour 19; about 330 shovels in 19–20 h (p.133) | 154 at hour 19; 105–111 over the firing, with Taylor's 21 lb shovel (`kiln-fuels.md` [F8]) | 0.67–1.15 (gross, Grade B) | inside Norsker's "most efficient" 95–145 over the firing, just above it at hour 19 [G1]; inside Gebhardt's natural-draft maxima, 49–200 at 25–125 Pa [G5] |
| `kato-coal` | two grates 30 × 22 in (printed "5 sq ft" each), 0.85–0.93 m² (p.131, p.207) | above 2000 °F: 10–12 shovels every 20 min in reduction, 3–4 in oxidation (p.131) | reduction 308–403, oxidation 92–134, if the count is the kiln's total and each shovel 21 lb | – | oxidation inside [G1] and [G5]; reduction above the highest natural-draft figure (200 at 0.5 in., [G5]) unless a shovel holds about 10 lb or less (counting the shovels as the kiln's total): the shovel's weight decides (a question) |
| `breda-bottle` (wood) | 37 bars 1 in apart, 8 ft into the firebox; the ash pit 2 ft wide (p.167): not reconcilable (the dataset's note) | 2 tons of chestnut in about 10 h (p.166, p.168) | 181 kg/h as fired; no grate area | – | – |
| `falcone-pompeii` (wood) | none; a 3 × 4 m firebox chamber (p.160) | 15 tons (13.6 t) in a 40 h cycle | 28 per m² of firebox floor, as fired | – | no grate |

The grates against the sources' proportions (Derived):
- **Free area**: the fast-fire's ¾ in rods at 1½ in centres leave 50 % open, the top of Kent's
  30–50 % [G4]; Olsen's ¾–1 in gaps (pp.199–206) are far under Norsker's 15–20 cm for firewood
  [G1], on purpose: Olsen keeps the coals small and slows the ash pit's filling (p.204).
- **Grate against floor**: the fast-fire's grates are 71–96 % of its chamber floor, Singh's 42 %,
  Kato's 31–33 %, against Norsker's 15–25 % (wood) and 12–25 % (coal) [G1] and Olsen's own coal rule,
  1 ft² per 6–8 ft² of floor (pp.76, 206). His wood rule ties the grate to the chimney instead
  (about 7 : 1, p.77); the fast-fire's is 7.1–8.7 × its 81 in² chimney.
- **Air openings**: the fast-fire's open mouths are 17–31 % of its grate above the bars and 23–38 %
  below; Singh's stoke holes 34 % and ash pits 150 %; the Chicago settings' over-fire air 2.8 %
  [G5]. The kilns' openings, fully open, don't limit the air (`firebox-air-intakes.md` §3).

What it says, for B4 (reasoning on the Derived figures above, not a fit): the fast-fire's printed
wood is an upper bound and its draft-limited fire sits under the open sources' refuse and moving-
grate heat releases, so its grate needn't be the limit: the draft and the stoker are (problem set
§2.2). Singh's coal rate falls inside the hand-fired range with a 21 lb shovel. Kato's reduction
rate fits the natural-draft tables only with a shovel of about 10 lb or less: the shovel's weight
is the owner's question. No source gives a burning rate for wood logs on a hand-fired grate, or a
burning wood bed's pressure drop: both stay open, the bed's resistance a stated band (ADR 0017
decision 4).

## Not found / not read

- **Wood logs or cordwood**: no burning rate per grate area on a hand-fired natural-draft grate in any
  source read (B&W: "higher" than refuse, no figure; Norsker, Kent, Gebhardt and Bourry: none; Kent's
  text searched for "wood-burning", "cord wood", "of wood per").
- **A wood grate's free air space** as a %: Gebhardt's Table 38 lists slabs, sawdust and shavings but
  its figures are scrambled in two scans; the 1913 edition's text read doesn't hold the table.
- **Sizing rules** for ash-pit doors, stoke holes and fire doors against grate area or fuel rate.
- **Pressure drop through a burning wood bed**; the values of B&W's Fig. 34, TP 137's Fig. 18 and
  Table 1, and TP 139's Table 3 (figures or illegible OCR).
- Kawagoe's BRI Report 27 (1958); Thomas and Heselden's FRN 923 (the CIB programme); FRN 979's PDF
  (404); the full text of [G14] (Springer login).
- PDFs the fetch tool couldn't read: Ray and Kreisinger, *The Significance of Drafts in Steam-Boiler
  Practice*, USGS Bulletin 367, 1909 (pubs.usgs.gov/bul/0367/report.pdf, 403) and its reprint, BoM
  Bulletin 21; the Sydney paper [G17]; *Hand Firing Soft Coal* (publications.iowa.gov/44401, a scan);
  CDC stacks 217769 (a scanned BoM report); the nvlpubs PDFs of NBS 7327 and J. Res. 66C (read through
  archive.org's OCR instead); Bulletin 135's PDF at UNT (over 10 MB; read on archive.org); Yu et al.
  2025 (MDPI 403); Fire Technology doi:10.1007/s10694-023-01466-9 (login); the B&W vibrating-grate
  leaflet [G19]; the Unified Facilities Criteria mirror [G18] (certificate error).
- Not reached (archive.org's search service gave 503 for part of the session): Peabody and Miller,
  *Steam Boilers*; Rankine; Searle, *Kilns and Kiln Building*; Scheffler, Trans. ASME xv, 503; Yin,
  Rosendahl and Kær's review of biomass grate firing (2008); Junge, *Boilers Fired with Wood and Bark
  Residues* (OSU, 1975); EN 12952-16; FAO and ITDG brick-kiln manuals.
