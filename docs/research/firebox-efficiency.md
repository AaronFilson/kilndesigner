# Efficiency of a wood kiln's firebox

The engine burns wood as m = Q ÷ (η·H(w)) (`core/src/kilndesigner/wood.py`): Q is the simulated
heat into the kiln's walls and ware, H(w) the wood's net heating value as fired, and η
(`site.wood.firebox_efficiency`) "everything else, chiefly the flue gas". η is the user's own; the
example carried 25 %, a non-airtight stove's figure (`wood-fuel.md` §3). This file looks for kiln
values and for a way to work η out.

Read 2026-11-09. Quotes are as the fetched page gave them. Several PDFs (the Nepal pottery-furnace
paper, a Polish wood flue-loss paper, BEE India's slides) came back as unreadable binary or
unreachable: listed under "Not found" so nobody cites them from here.

## 1. Definitions differ, so read every number with its own

- **Engine's η**: heat into walls **and** ware ÷ net heat of the wood as fired. Flue gas, unburnt
  fuel, ash and the firebox's own outside losses are the rest. Heat the walls store and lose
  outside is *inside* Q, so it is not part of 1 − η.
- **Brick-kiln "energy efficiency"** (Practical Action, [B1]): the table doesn't state it, but
  its figures match theoretical firing energy ÷ actual (derived: 0.85 MJ/kg ÷ 3.0 = 28 %, ÷ 8.0 =
  11 %, against its "10 – 28" for clamps; 0.85 MJ/kg is the theoretical energy to fire brick in
  [B2]). That counts **ware only**: wall storage and wall loss are losses. So a brick kiln's
  efficiency is a **lower bound** on the engine's η for the same kiln.
- **Specific energy consumption (SEC)**, MJ per kg of fired product: no efficiency at all until
  divided into a theoretical figure.
- **Pottery-kiln "thermal efficiency"** ([P1], [P2]): useful heat in the kiln ÷ fuel heat. [P2]'s
  numbers fit useful ÷ (useful + losses) (derived, §2); whether "useful" includes the walls isn't
  stated in what could be read.

## 2. Measured pottery and wood kilns

**[P1] Adubah, D. A., "Sustainability and fuel consumption patterns in traditional firewood
kilns: Implications for the pottery industry in Ghana"**, Journal of African Arts and Culture 8(4)
(2025), published 2026-05-07. <https://journals.uew.edu.gh/index.php/jaac/article/view/703>.
Abstract: "19 firewood kilns at the Mfensi Pottery Centre"; "kiln thermal efficiency ranged
between 12.4% and 21.6%, with mean firewood consumption of 0.82 kg kg⁻¹ of fired clay"; "High heat
losses through uninsulated walls and uncontrolled airflow". Kiln type, temperature and the
efficiency's definition aren't in the abstract (earthenware, by the centre's trade: not stated).

**[P2] Jongpluempiti, J., Naphon, P. and Vengnungnle, P., "Study on the thermal efficiency and
temperature distribution of Dan Kwien kiln in Thailand"**, JP Journal of Heat and Mass Transfer
12(2), 181–195, November 2015, doi:10.17654/JPHMTNov2015_181_195.
<https://www.pphmj.com/abstract/9414.htm>; also
<https://ir.swu.ac.th/entities/publication/020513d3-59d1-4921-880b-8803f25c15be>.
A clay-and-brick kiln 2.5 × 8 m, 262 pots in 108 h on about 2,600 kg of firewood (abstract, as
summarised by the fetch tool). "the main heat loss from the Dan Kwien pottery kiln is the exhaust
heat loss from the chimney"; "the Dan Kwien pottery kiln gives the 18.07% thermal efficiency".
Per the SWU record's abstract: chimney loss about 19.34 GJ of about 33.09 GJ total losses, useful
heat about 7.3 GJ. Derived: 7.3 ÷ (7.3 + 33.09) = 18.07 %; the chimney is 19.34 ÷ 40.39 = **48 %**
of the input. Its firing reaches 900–1000 °C, not stoneware.

**Olsen, *The Kiln Book*, 4th ed., p.143** (kiln-reference.md): a 12–16 ft³ fast-fire downdraft to
cone 10 in 3½–4 h on "less than a quarter of a cord". This bounds η from below only (derived, not a
source): the engine's 32.9 ft³ version takes Q = 719 kWh (11-09-26.md); scaled by stacking volume
(an assumption) 12–16 ft³ is 262–350 kWh. A quarter cord oven-dry is 255 kg (white pine, 2,250
lb/cord) to 391 kg (kiawe, 3,450 lb/cord) (wood-fuel.md), at 19 MJ/kg 1,350–2,060 kWh, a little
less at the wood's moisture. So η ≳ 13–26 %, the spread being the cord's weight and the scaling.

Not found: any measured anagama, noborigama, groundhog, Bourry-box or Minnesota flat-top energy
balance or wood mass with a heat-up model; no Woodfire conference paper or thesis with one could
be read. The Ceramics Monthly figures (1½–5 cords a firing, wood-fuel.md §4) have no kiln size.

## 3. Brick and tile kilns

**[B1] Practical Action, "Sustainable small-scale brick production"** (no date on the page), table
of kiln types; the page says the data is "no more than indicative".
<https://samplecontents.library.ph/en-practical_action/Construction/Clay%20bricks/KnO-100102_Sustainable%20small%20scale%20brick%20production/page3.html>
(rows mapped by position by the fetch tool: check against the page).

| Kiln | Fuel | MJ/kg fired brick | Energy efficiency |
|---|---|---|---|
| Traditional clamp | biomass | 3.0–8.0 | 10–28 % |
| Intermediate clamp | coal, coke | 2.0–4.5 | 19–42 % |
| Scotch kiln | biomass | 1.5–7.0 | 12–59 % |
| Vertical shaft (VSBK) | coal | 0.8–1.4 | 60–100 % |
| Bull's trench | coal | 1.1–4.0 | 21–77 % |
| Hoffmann | coal, gas, oil | 1.5–4.3 | 20–56 % |
| Tunnel | oil, gas | 1.5–2.0 | 45–56 % |

**[B2]** Theoretical energy to fire brick, 0.85 MJ/kg (search-result snippet of a brick-kiln
review; the page wasn't read: treat as unverified).

**[B3] Maithel, S., PhD seminar on the Bull's trench kiln, IIT Bombay, 2003**
(<https://sidhiee.beeindia.gov.in/pdf/bricks/3.pdf>, unreachable on 2026-11-09; figures from a
search summary only, **unverified**): SEC 1.12 ± 0.03 MJ/kg; heat balance water vapour 46.5 %,
irreversible reactions in the brick 17.1 %, kiln surface 14.7 %, ground 12.8 %, sensible heat of
flue gas and fired brick 7.2 %, unaccounted 1.8 %. A continuous kiln: the flue gas leaves cool
because it preheats green brick, which an intermittent studio kiln can't do.

Search summaries (not read) of BEE India's brick-sector mapping give zigzag 1.11, FCBTK 1.34,
tunnel 1.42, clamp 1.79 MJ/kg; Indian intermittent kilns 3.85–5.35 and downdraft 2.37 MJ/kg; a
Thai rectangular downdraft open-top kiln 2.52 MJ/kg. Left out of the table until read.

What it means for a studio kiln: intermittent, biomass-fired kilns (clamp, Scotch) sit at
**10–28 %** and 12–59 % on a ware-only basis. Continuous kilns' higher figures come from heat
recovery a batch kiln doesn't have; they don't transfer.

## 4. The loss terms and a formula

### Flue gas: the dominant term

The sensible heat of the flue gas over the net heating value, q = Σ nᵢ·[h̄ᵢ(T_flue) − h̄ᵢ(25 °C)] ÷
H(w), for complete combustion at an air ratio λ. That is the Siegert form's physics; Siegert's
coefficients (qA = f·(t_flue − t_air)/CO₂, Bosch's table at
<https://www.boiler-planning.com/en/efficiency/basics/combustion-efficiency.html>, read
2026-11-09) are given there only for gases and oils, and are fitted near boiler flue temperatures,
not 1300 °C. Not found: a published Siegert f or A1/B for wood (a Madur table seen in a search
snippet gives dry wood CO₂max 19.4 %, A1 0.65, B 0: unverified).

Inputs (derived values; complete combustion to CO₂ and H₂O, excess O₂ and N₂ at 79/21, enthalpy
from 25 °C to the flue temperature):

- Dry wood ≈ 50 % C, 6 % H, 44 % O by mass: Pettersen, R. C., "The chemical composition of wood",
  in Rowell (ed.), *The Chemistry of Solid Wood*, ACS Advances in Chemistry 207, 1984 (quoted in
  search results as "about 50% carbon, 6% hydrogen, 44% oxygen"; the chapter wasn't read). Gives
  a stoichiometric air of **5.9 kg per kg dry wood** (derived).
- H = 19 MJ/kg net oven-dry ([W2] in wood-fuel.md), moisture by FAO eq. 3.
- Gas enthalpies: Cantera's gri30 thermodynamic data, as the engine's propane model (ADR 0012).

Flue-gas loss, % of the wood's net heat as fired (derived; water stays vapour, so this is the
net-basis loss; moisture 12 % wet, 20 % within 1–3 points higher):

| λ (air ÷ stoichiometric) | 200 °C | 600 °C | 900 °C | 1100 °C | 1300 °C |
|---|---|---|---|---|---|
| 1.0 | 7 | 25 | 40 | 50 | 60 |
| 1.2 | 8 | 29 | 46 | 57 | 69 |
| 1.5 | 10 | 35 | 55 | 69 | 83 |
| 2.0 | 13 | 44 | 70 | 87 | 106 |

Check: [P2]'s chimney took 48 % at 900–1000 °C, between λ 1.0 and 1.2 here.

In a downdraft or cross-draft studio kiln the gas leaves the chamber at about the chamber's
temperature (no heat recovery; reasoning, not a source), so the instantaneous η is at most
1 − q(T_chamber, λ): about 60–75 % at 600 °C, 30–40 % at 1300 °C with λ 1.0–1.2, falling to zero
where q reaches 100 % (λ 2 at about 1250 °C). Fuel spent per degree rises steeply toward peak.
That is the shape of a firing; no source read gives η against time for a wood kiln.

### Other terms

- **Unburnt (CO, smoke, char in the ash)**: not found as a measured share for a kiln. Reduction
  firing deliberately runs λ < 1 for part of the firing, where the combustibles leaving are a loss
  the formula above doesn't count.
- **Ash**: wood ash is around 1 % of dry mass ([W3] Table 10 gives total ash, values not copied
  here); its sensible heat is negligible next to the gas (reasoning).
- **Firebox outside losses**: the engine's Q includes the chamber walls; a firebox outside the
  modelled shell loses through its own walls. Not found as a measured share.
- **Heat stored in the structure**: inside Q in the engine (the transient wall model), so not part
  of 1 − η. [B3]'s surface and ground losses (27.5 %) are the brick kiln's equivalent.

### Firebox types

Not found: any comparison of η between Bourry box, Minnesota flat-top, sutema/through-draft,
groundhog or anagama side stoking. Their differences would act through λ and through unburnt
fuel; the flue formula would carry the first.

## 5. Summary

| Source | Kiln | Basis | Value |
|---|---|---|---|
| [P1] Adubah 2026 | 19 firewood pottery kilns, Ghana | thermal efficiency | 12.4–21.6 %; 0.82 kg wood/kg ware |
| [P2] Jongpluempiti et al. 2015 | Dan Kwien wood pottery kiln, 900–1000 °C | useful ÷ input | 18.07 %; chimney 48 % |
| [B1] Practical Action | traditional biomass clamp | ware-only | 10–28 %; 3.0–8.0 MJ/kg |
| [B1] Practical Action | Scotch kiln, biomass | ware-only | 12–59 %; 1.5–7.0 MJ/kg |
| Olsen p.143 (derived) | 12–16 ft³ fast-fire, cone 10 | engine's η, lower bound | ≳ 13–26 % |
| §4 (derived) | any, gas leaving at chamber temperature | 1 − flue loss | 30–40 % at 1300 °C, λ 1.0–1.2; 60–75 % at 600 °C |
| wood-fuel.md [W1] | non-airtight stove (not a kiln) | appliance | 25 % |

## 6. Recommendation

- **Starting range for `firebox_efficiency`: 15–30 %** for an intermittent, uninsulated-to-
  moderate wood kiln fired to cone 10, with **20–25 %** a reasonable middle. Sourced: wood pottery
  kilns measured at 12.4–21.6 % [P1] and 18.07 % [P2]; biomass clamps 10–28 % on a ware-only
  basis [B1], which understates the engine's η; Olsen's quarter cord gives ≳ 13–26 % (derived);
  the flue formula caps a cone-10 firing's last hours near 30–40 %. The 25 % in the example sits
  in this band, so it stays, re-sourced to kilns rather than a stove.
- **Compute η from the flue loss instead (proposed, not built).** The engine already integrates
  the propane firing step by step with Cantera's available heat. Wood can go the same way: a
  CH₁.₄₃O₀.₆₆ surrogate (50/6/44 C/H/O by mass, derived) at the user's moisture, λ from the user (default none),
  the flue at the chamber's gas temperature, η_step = 1 − q(T, λ) − u, u the user's unburnt
  allowance. The firing's wood is then Σ Q_step ÷ (η_step·H). This replaces one guessed number
  with λ and u, of which λ is measurable (an O₂ probe) and u not yet sourced. It needs: Pettersen
  read at the page, and a check against one weighed firing. Until then, `firebox_efficiency` stays
  the user's.

## Not found / not read

- Measured energy balances for anagama, noborigama, groundhog, Bourry-box, Minnesota flat-top,
  sutema kilns; Woodfire conference proceedings; Japanese, Korean or Australian theses.
- A Siegert f or A1/B for wood from a primary source; measured unburnt and CO losses for a kiln.
- Adhikari et al., Nepal (Thimi) pottery furnaces, Journal of Innovations in Engineering
  Education (nepjol.info, download 39694): PDF unreadable here; a summary gives 0.98–2.4 MJ/kg.
- BEE India Brick Sector Energy Mapping (404) and Maithel's slides (DNS failure).
- Le Brun and Markides, MATEC 2016, FCBTK model (core.ac.uk 77017432): not read.
- ESMAP/World Bank, CCAC, GKSPL and MinErgy brick reports; FAO wood-energy pottery surveys:
  not reached in this round.
