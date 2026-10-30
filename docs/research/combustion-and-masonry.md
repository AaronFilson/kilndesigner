# Combustion and masonry reference data

Checked: 2026-10-21. Every number has a source tag like [S3], and the tags are listed under "Sources" at the end.

How values are marked:
- **(derived)** means I calculated it from sourced inputs. The working is shown.
- **(secondary)** means a forum, blog or retailer passing on a primary source I could not open.
- **NOT FOUND** means I found no source. Do not fill these gaps with guesses.

Many primary PDFs (the PERC pocket guide, the RegO L-545 and Emerson LP-10 handbooks, the HWI and Allied data sheets, the CAD "Gas Kilns" PDF) could not be read with the tools available. Their text is compressed. Where a number from one of them came only through a search-engine snippet, it is marked.

---

## 1. Propane properties

### 1.1 Heating value, density, combustion

| Property | Value | Conditions | Source |
|---|---|---|---|
| HHV per gallon (liquid) | 91,502 BTU/gal | 60 °F | [S1] [S2] |
| HHV per gallon | 91,690 BTU/gal | "vaporized" | [S3] |
| HHV per gallon | 91,420 BTU/gal | AFDC/NREL | [S4] |
| HHV per gallon | 91,410 BTU/gal | GREET table | [S5] |
| HHV per gallon | "roughly 92,000" BTU/gal | Ward Burner | [S20] |
| LHV per gallon | 84,250 BTU/gal | AFDC/NREL | [S4] |
| LHV per gallon | 84,950 BTU/gal | GREET table | [S5] |
| HHV per pound | 21,548 BTU/lb | | [S1] [S2] |
| HHV per pound | 21,591 BTU/lb | | [S3] |
| LHV per pound | ≈ 20,060 BTU/lb | 84,250 ÷ 4.20 **(derived)** | [S4] [S1] |
| HHV per cubic foot of vapor | 2,488 BTU/ft³ | 60 °F | [S1] [S2] |
| HHV per cubic foot (rounded) | 2,500 BTU/ft³ | Ward; Ceramics Monthly | [S21] [S30] |
| LHV per cubic foot | ≈ 2,291 BTU/ft³ | 2,488 × 84,250/91,502 **(derived)** | |
| HHV, mass basis | 50.152 MJ/kg | GREET | [S5] |
| LHV, mass basis | 46.607 MJ/kg | GREET | [S5] |
| LHV, mass basis | 46.66 MJ/kg | CARB LCFS (84,250 BTU/gal, 4.2 lb/gal) | [S5b] |
| Liquid density | 4.20 lb/gal | 60 °F | [S1] [S2] |
| Liquid density | 4.23 lb/gal | | [S3] |
| Liquid density | 31.63 lb/ft³ = 4.228 lb/gal | NIST, saturated liquid near 60 °F; ÷ 7.4805 gal/ft³ **(derived)** | [S6] |
| Liquid density | "about 4.5 lb per gallon" | Ward. **Disagrees** with the other sources. Do not use. | [S20] |
| Liquid specific gravity | 0.504 (water = 1) | | [S1] |
| Liquid specific gravity | 0.51 | | [S3] |
| Vapor specific gravity | 1.50 (air = 1) | | [S1] |
| Vapor specific gravity | 1.53 | | [S3] |
| Vapor specific gravity | 1.522 | Ward power-burner rating basis | [S22] |
| Vapor per gallon of liquid | 36.38 ft³/gal | 60 °F | [S1] |
| Vapor per pound | 8.66 ft³/lb | 60 °F | [S1] |
| Liquid-to-vapor expansion | 272 : 1 | | [S3] |
| Boiling point | −44 °F | 1 atm | [S1] [S3] |
| Latent heat of vaporization | 773 BTU/gal | at boiling point | [S1] |
| Air needed, by volume | 23.86 ft³ air per ft³ gas | stoichiometric | [S1] |
| Air needed, by volume | ≈ 23.87 | C₃H₈ + 5 O₂ → 3 CO₂ + 4 H₂O; 5 ÷ 0.2095 O₂ in air **(derived)** | |
| Air needed (rounded) | "approximately 25" ft³ air per ft³ | Ceramics Monthly | [S30] |
| Air/fuel ratio, by mass | ≈ 15.67 : 1 | 23.87 × 28.96 ÷ 44.10 (molar masses) **(derived)** | |
| Flammability limits | 2.15 % to 9.6 % gas in air | | [S1] |
| Ignition temperature in air | 920 to 1,120 °F | | [S1] |
| Max flame temperature in air | 3,595 °F | | [S1] |
| CO₂ per gallon | 12.68 lb/gal (5.75 kg/gal) | EIA, released 2024-09-18 | [S7] |
| CO₂ per gallon | ≈ 12.57 lb/gal | 4.20 lb × (3 × 44.01 ÷ 44.10) **(derived)**. The small gap from EIA is probably the density basis. | |

### 1.1a Natural gas

| Property | Value | Conditions | Source |
|---|---|---|---|
| Heating value, the orifice tables' basis | 1000 BTU/ft³, specific gravity 0.64 | Ward's tables as Olsen prints them | Olsen, 4th ed. p.230 |
| Methane, enthalpy of combustion | −890.7 ± 0.4 kJ/mol (Pittam and Pilcher, 1972) | gas, 25 °C | [S87] |
| Methane, molar mass | 16.0425 g/mol | | [S87] |
| Methane HHV, mass basis | 55.52 MJ/kg | 890.7 ÷ 16.0425 **(derived)** | [S87] |

- For available heat the engine takes natural gas as methane, its main part (Cantera has no
  "natural gas"). Ethane and heavier gases in a real supply raise its heating value a little.

### 1.2 Vapor pressure against temperature (psig)

NIST gives values for pure propane. I converted them from psia by subtracting 14.696, interpolating linearly between NIST rows **(derived)** [S6].

| °F | NIST pure propane (psig, derived) | Flame Engineering [S3] | Propane Warehouse / Pro Tank Supply [S1] [S2] | Emerson LP-10 (snippet only) [S8] |
|---|---|---|---|---|
| −20 | 10.7 | 11.5 | 13.5 | 13.5 |
| −10 | 16.7 | 17.5 | 23.3 | 20 |
| 0 | 23.7 | 24.5 | 28 | — |
| 10 | 31.8 | 34 | 37 | — |
| 20 | 41.1 | 42 | 47 | 47 (PERC snippet [S9]) |
| 30 | 51.8 | 53 | 58 | — |
| 40 | 63.9 | 65 | 72 | — |
| 50 | 77.6 | not listed | 86 | — |
| 60 | 93.0 | 93 | 102 | — |
| 70 | 110.2 | 110 | 127 | — |
| 80 | 129.3 | 128 | 140 | — |
| 90 | 150.5 | 150 | 165 | — |
| 100 | 173.9 | 177 | 196 | — |

- Flame Engineering's column agrees with NIST pure propane to within about 3 psi.
- The Propane Warehouse and Pro Tank Supply table runs 4 to 22 psi higher. It may assume a commercial mix with some ethane, but that sheet does not say so. **The two sources disagree. Use NIST for code.**
- Ward gives rough examples: "about 77 psi at 50 °F, about 23 psi at 0 °F, about 5 psi at −30 °F" [S23]. These match NIST.

---

## 2. Cylinder and tank vaporization

### 2.1 100 lb cylinder, maximum continuous draw (BTU/hr), by pounds left in the cylinder

Source: Flame Engineering [S3], reproduced the same by Propane Warehouse [S1] and Pro Tank Supply [S2]. The basis (lowest allowed cylinder pressure, orientation) is **not stated**.

| lb in cylinder | 0 °F | 20 °F | 40 °F | 60 °F | 70 °F |
|---|---|---|---|---|---|
| 100 | 113,000 | 167,000 | 214,000 | 277,000 | 300,000 |
| 90 | 104,000 | 152,000 | 200,000 | 247,000 | 277,000 |
| 80 | 94,000 | 137,000 | 180,000 | 214,000 | 236,000 |
| 70 | 83,000 | 122,000 | 160,000 | 199,000 | 214,000 |
| 60 | 75,000 | 109,000 | 140,000 | 176,000 | 192,000 |
| 50 | 64,000 | 94,000 | 125,000 | 154,000 | 167,000 |
| 40 | 55,000 | 79,000 | 105,000 | 131,000 | 141,000 |
| 30 | 45,000 | 66,000 | 85,000 | 107,000 | 118,000 |
| 20 | 36,000 | 51,000 | 68,000 | 83,000 | 92,000 |
| 10 | 28,000 | 38,000 | 49,000 | 60,000 | 66,000 |

Note: a "100 lb" cylinder holds 100 lb of propane when full.

### 2.2 Conservative cylinder table: vertical cylinder, 25 % full, cylinder pressure kept at or above 10 psi (BTU/hr)

Sources: Motorsnorkel and US Carburetion (same table) [S10], and Monnick Supply's PDF [S11]. I could only read these through search snippets, so many cells are missing.

| Cylinder | +60 °F | +40 °F | +20 °F | 0 °F | −20 °F |
|---|---|---|---|---|---|
| 20 lb | 24,000 | NOT FOUND | NOT FOUND | 7,500 | NOT FOUND |
| 30 lb | 32,000 | NOT FOUND | NOT FOUND | 10,000 | NOT FOUND |
| 40 lb | 40,100 | NOT FOUND | NOT FOUND | 12,600 | NOT FOUND |
| 100 lb | 79,700 | 61,500 [S11] | 43,300 [S11] | 25,000 | NOT FOUND |
| 200 lb | 125,900 | NOT FOUND | NOT FOUND | NOT FOUND | NOT FOUND |
| 420 lb | 185,500 | 143,100 | 100,700 | 58,300 | NOT FOUND |

**The two tables disagree a lot.** At 20 °F a 100 lb cylinder with 25 lb left gives about 58,000 BTU/hr in table 2.1 (interpolated) but 43,300 in table 2.2. Table 2.2 also keeps at least 10 psi in the cylinder, which a high-pressure venturi burner needs. The engine should use table 2.2 as the conservative case and show table 2.1 as the optimistic case.

### 2.3 ASME tanks: D × L × K rule of thumb

Sources: Propane Warehouse [S1], Pro Tank Supply [S2], and a search summary of distributor handouts [S12].

- Capacity at 0 °F (BTU/hr) = D × L × K.
- D is the outside diameter in inches. L is the overall length in inches.
- The formula assumes the liquid cools to −20 °F (a 20 °F difference). Vapor space is ignored [S1].

| % full | K |
|---|---|
| 60 | 100 |
| 50 | 90 |
| 40 | 80 |
| 30 | 70 |
| 20 | 60 |
| 10 | 45 |

Air-temperature correction factors (secondary, from snippets only) [S12]:

| Air temp | Factor |
|---|---|
| −15 °F | 0.25 |
| −10 °F | 0.50 (used in a worked example) |
| 0 °F | 1.00 |
| +5 °F | 1.25 |
| +20 °F | 2.00 |

Worked example from the source: a 1,000 gal tank with D = 41 in., L = 192 in., K = 60, at −10 °F (CF 0.50). 41 × 192 × 60 × 0.50 = 236,160 BTU/hr [S12].

### 2.4 ASME tanks, 1/3 full, "maximum continuous BTU/hr" (secondary)

Source: Engineering Radio blog [S13]. The original source is not named. The blog calls the table "a conservative generalization".

| Tank (gal) | 0 °F | 20 °F | 40 °F | 60 °F | 70 °F |
|---|---|---|---|---|---|
| 120 | 129,600 | 188,640 | 247,680 | 308,160 | 338,400 |
| 150 | 146,880 | 213,790 | 280,700 | 349,200 | 383,520 |
| 250 | 253,800 | 369,400 | 485,000 | 603,480 | 662,700 |
| 325 | 321,300 | 467,670 | 614,000 | 763,900 | 838,900 |
| 500 | 396,270 | 567,700 | 757,300 | 942,240 | 1,034,700 |
| 1000 | 708,480 | 1,031,230 | 1,353,980 | 1,684,600 | 1,849,900 |

Other figures for ASME tanks:
- Ward: a 500 gal tank 60 % full gives about 425,000 BTU/hr at 0 °F and about 850,000 at 20 °F [S23].
- Nova Scotia permit limits are regulatory caps, not measured capacities [S14]:
  - 100 lb cylinder: 52,875 BTU/hr (heating) or 92,531 (water heating and cooking).
  - 420 lb cylinder: 103,500 or 181,125.
  - 500 gal tank: 582,750 (heating) or 333,000 (cooking).
  - 1000 gal tank: 1,033,200 or 590,400.

### 2.5 Ward Burner rules of thumb for temperature and tank size

- A tank gives "about twice as much" vapor at 20 °F as at 0 °F, and "almost four times" as much at 40 °F [S20].
- Keep at least 4 times the liquid you expect to use at 60 °F. That multiple rises as it gets colder [S20].
- A 20 lb cylinder holds about 4.5 gal. A 100 lb cylinder holds about 22 gal [S20]. **Conflict:** 100 lb ÷ 4.2 lb/gal is about 23.8 gal **(derived)**.

Ward's tank guidance for soft-brick stoneware kilns [S20]:

| Kiln | Northern amateur | Northern pro |
|---|---|---|
| 20 ft³ | 250 gal; don't fire below 20 °F | — |
| 40 ft³ | 250 gal (summer only) or 500 gal | 500 gal |
| 70 ft³ | "too large" | 1000 gal (500 gal with caution) |

### 2.6 Manifolding cylinders, frosting and pressure drop

- **Frosting and pressure drop.** Boiling the liquid cools it. The tank cools, its pressure falls, and less gas comes off. Ward calls tank freeze-up a symptom: the tank cannot keep up with what the burner draws. Ward's fix is "a bigger tank for the prevailing circumstances" [S23].
- **Never heat a tank.** Ward warns never to heat a tank with anything that could ignite gas, such as exhaust, hair dryers, heat guns or fires (BLEVE risk). Ward also does not recommend a water bath [S23].
- **Ganging.** Ward sells 2-tank and 3-tank connectors that feed from all tanks at once. Ward says this "can help prevent tank freeze up" [S24]. For raku below 20 °F, Ward suggests two 40 lb cylinders "ganged together" [S20].
- **Adding up capacity.** No source I found says that cylinders in parallel add their capacities. It is a reasonable assumption when the cylinders are at the same temperature and fill, but it is an **inference, not a sourced value**. NFPA 58 manifolding rules: **NOT FOUND** (the handbook is paywalled).
- **Regulators.** A regulator can only lower pressure. Burners run straight from tank pressure change output with temperature and fill [S23] [S25].

### 2.7 Supply pressures, regulators and lines

| Item | Value | Source |
|---|---|---|
| 1 psi | 27.7 in. w.c. | [S21] |
| "Low pressure" | below 1 psi | [S21] |
| Household propane delivery | 11 in. w.c. (≈ 0.4 psi) | [S21] [S25] |
| Household natural gas delivery | 7 in. w.c. (≈ 0.25 psi) | [S21] |
| Full propane tank in summer sun | up to about 250 psi | [S21] |
| Ward power (blower) burners | 14 in. w.c. or less; rated at 11 in. w.c. propane | [S22] [S26] |
| Ward / Ransome venturi burners | rated from 11 in. w.c. up to 20 psi (table in 3.2) | [S27] |
| Example used kiln | 4 venturi burners on propane at 10 psi | [S21] |
| Ceramics Monthly kiln | 0–30 psi regulator and 0–15 psi gauge on MR-750 venturis | [S30] |
| Regulator service life | 15 years (industry standard) | [S25] |

### 2.8 Regulator droop and the liquid's cooling under draw (added 29 October 2026)

RegO, *High Pressure Industrial / Commercial Pounds-to-Pounds Regulators, 597F Series*, catalogue
page A32 (data sheet) [S89]. Verified (read from the PDF):

| Part | Delivery range (psig) | Capacity at set pressure (psig) | Capacity, propane (BTU/hr) |
|---|---|---|---|
| 597FA | 1–15 | 10 | 1,750,000 |
| 597FB | 10–30 | 20 | 3,000,000 |
| 597FC | 20–45 | 30 | 3,500,000 |
| 597FD | 40–100 | 40 | 4,500,000 |

- "Set pressure established at 100 PSIG inlet and a flow of 250,000 BTU/hr."
- "Capacity determined at actual delivery pressure 20% less than set pressure with inlet pressure
  20 PSIG higher than the set pressure."
- The sheet's curves show delivery falling with flow and falling further as the inlet drops
  (597FB: set 20 psig, about 16 psig at 3,000,000 BTU/hr on a 50 psig inlet).

The engine reads this as: the regulator needs the container **20 psig above** the set pressure, and
at full flow the burners may see **20 % less** than the set pressure. Both are this one regulator
family's rating basis, used as the margin for any adjustable pounds-to-pounds regulator; a
regulator with its own published curve may do better. Neither Emerson/Fisher's droop for an
equivalent nor the RegO LP-Gas Serviceman's Manual was read.

**The liquid's cooling under draw.** The D × L × K rule (§2.3) assumes the liquid cools 20 °F
below the air under continuous draw [S1]. The engine takes the same 20 °F for cylinders and tanks
when it reads propane's vapour pressure (§1.2), and reads the 100 lb cylinder table (§2.1), which
Propane Warehouse gives by liquid temperature [S1], at the air temperature less 20 °F.

**The ⅓-full tank table (§2.4).** Its 0 °F column is D × L × 90 (e.g. 120 gal, 24 × 60 × 90 =
129,600), the 50 %-full K (§2.3). At ⅓ full K is 70 + (33.3 − 30) × (80 − 70)/10 = 73.3 (linear
between the 30 % and 40 % rows, **derived**), so the engine scales the table by 73.3 ÷ 90 = 0.815.

- [S89] RegO, 597F Series data sheet, catalogue p. A32 (read 2026-10-29).
  https://cdn.shopify.com/s/files/1/0029/6461/9313/files/252-RE597F.pdf

- Pipe and hose sizing tables: **NOT FOUND** in a readable source. The NFPA 54 / IFGC propane sizing tables are the standard reference; use those.

---

## 3. Gas burner sizing

### 3.1 Ward Burner BTU per cubic foot of kiln per hour

Olsen, 4th ed. p.226 (read from the book): an IFB kiln needs about
10,000 BTU per ft³ per hour at peak; dense firebrick 16,000–19,000. He calls most gas kilns
overpowered. That agrees with the low end of Ward's table below.

Ward Data Guide [S28]. The page calls these "a guide, not a guarantee".

| Wall construction | Cone 06 | Cone 6 | Cone 10 |
|---|---|---|---|
| 9 in. hard brick | 12,000–17,000 | 14,000–18,500 | 16,000–20,000 |
| 9 in. insulating brick | 6,000–10,000 | 8,000–13,000 | 10,000–16,000 |
| 6 in. ceramic fiber | 4,000–6,000 | 6,000–8,000 | 7,000–10,000 |

- **Conflict:** Ward's 1996 *Clay Times* article gives fiber as 6,000–9,000 at cone 6 and 7,000–11,000 at cone 10. The brick rows match [S29].
- The high end of each range gives about a 6 to 7 hour firing (the article says 6 to 8 hours). The low end gives about 14 to 18 hours (the article says 14 or more) [S28] [S29].
- Method: total BTU/hr = (BTU/ft³/hr) × interior ft³. Then divide by the number of burners [S28].

Ward's kiln volume formulas [S28]:
- Flat top: H × W × L.
- Sprung arch: W × L × (wall height + ⅔ of the arch rise).
- Catenary: L × (4/3 × H × ½ base).
- Divide cubic inches by 1,728 to get cubic feet.

Raku (fast firing) [S28]:

| Construction | Total BTU/hr |
|---|---|
| 4.5 in. hard brick | 70,000 |
| 2.5 in. insulating brick | 40,000 |
| 4.5 in. insulating brick | 30,000 |
| 1 in. fiber | 25,000 |
| 2 in. fiber | 20,000 |

### 3.2 Venturi burner ratings against pressure (BTU/hr, propane unless noted)

Ward venturi page [S27]. Prices were checked 2026-10-21.

| Model | 11 in. w.c. | 1 psi | 2 psi | 5 psi | 10 psi | 15 psi | 20 psi | Price |
|---|---|---|---|---|---|---|---|---|
| Ransome B1 | 5,900 | 9,700 | 13,900 | 21,600 | 30,700 | — | 43,000 | $165.00 |
| Ransome B2 | 9,000 | 14,800 | 20,900 | 33,200 | 46,700 | — | 66,400 | $219.00 |
| Ransome B3 | 34,200 | 55,300 | 77,500 | 123,000 | 175,900 | — | 246,000 | $245.00 |
| Ransome B4 | 55,300 | 89,800 | 126,700 | 200,500 | 286,600 | — | 403,400 | $295.00 |
| Ransome B5 | 89,800 | 145,200 | 205,400 | 324,700 | 462,400 | — | 649,400 | $395.00 |
| GACO MR750 | 72,000 | — | 76,840 | 121,570 | 172,000 | 210,500 | 243,150 | $99.95 |
| GACO MR100 | 94,000 | — | 96,600 | 152,830 | 216,300 | 264,650 | 305,660 | $159.95 |

- **Derived check:** from 5 to 20 psi, the MR100 figures grow with the square root of gauge pressure. 216,300 ÷ 152,830 = 1.415 and 305,660 ÷ 216,300 = 1.413, against √2 = 1.414. So BTU/hr ≈ 68,400 × √(psig) for the MR100 and ≈ 54,400 × √(psig) for the MR750 in that range **(derived)**.
- **Every model against that curve** (checked 2026-10-28, **derived**): each rating ÷ (its 5 psi rating × √(p ÷ 5)) − 1.

  | Model | 11 in. w.c. | 1 psi | 2 psi | 10 psi | 15 psi | 20 psi |
  |---|---|---|---|---|---|---|
  | Ransome B1 | −3.1 % | +0.4 % | +1.7 % | +0.5 % | — | −0.5 % |
  | Ransome B2 | −3.8 % | −0.3 % | −0.5 % | −0.5 % | — | 0.0 % |
  | Ransome B3 | −1.3 % | +0.5 % | −0.4 % | +1.1 % | — | 0.0 % |
  | Ransome B4 | −2.1 % | +0.1 % | −0.1 % | +1.1 % | — | +0.6 % |
  | Ransome B5 | −1.9 % | 0.0 % | 0.0 % | +0.7 % | — | 0.0 % |
  | GACO MR750 | +110 % | — | −0.1 % | 0.0 % | 0.0 % | 0.0 % |
  | GACO MR100 | +118 % | — | −0.1 % | +0.1 % | 0.0 % | 0.0 % |

  - Every 2 psi rating, and every Ransome rating down to 11 in. w.c., lies within 4 % of the curve: the same orifice. Only GACO's two 11 in. w.c. ratings sit about twice above it, so they probably use a different (low-pressure) orifice. This corrects an earlier note here that the 2 psi entries were off the curve too.
  - Between published pressures on one orifice, a burner's pressure for a given output can be read by interpolating √pressure. Below the lowest of them (11 in. w.c. for the Ransomes, 2 psi for the GACOs) the high-pressure orifice's output is not published.
- Ward only sells the printed orifice charts ($9.50 each, $14.95 for both). They cover 4 in. w.c. to 25 psi and drill sizes #80 to ½ in., for natural gas and propane. The page does not reproduce the tables, so they are **NOT FOUND** [S31].

### 3.3 Venturi (atmospheric) against power (blower) burners

From Ward's comparison and draft articles [S26] [S32] [S22].

| Topic | Power (blower) | Venturi (natural draft) |
|---|---|---|
| Supply pressure | 14 in. w.c. or less, for natural gas and propane | wide range, 11 in. w.c. to 20 psi (3.2) |
| Electricity | needed; a power cut stops the firing | none (**the off-grid choice**) |
| Weather | not affected | affected |
| Primary air | all from the blower | 30–50 % drawn in at the mixer; the rest is secondary air pulled in by draft |
| Chimney | only tall enough to vent the building | height matters (see 4.1) |
| Burners per kiln | 2 power burners can replace 4 to 6 venturis | more needed |
| Efficiency | generally higher | lower; higher pressure lowers it further |

Ward power burners [S22]:

| Model | Blower | Up to (BTU/hr) | Price |
|---|---|---|---|
| MB200 | 50 CFM | 270,000 | $1,229 |
| MB300 | 75 CFM | 395,000 | $1,229 |
| MB400 | 75 CFM | 475,000 | $1,229 |
| MB500 | 130 CFM | 595,000 | $1,389 |
| MB600 | 130 CFM | 695,000 | $1,389 |
| MB700 | 130 CFM | 795,000 | $1,389 |

Ratings are at 7 in. w.c. natural gas (SG 0.65) and 11 in. w.c. propane (SG 1.522). A 220 V conversion is $129. A solenoid valve is $209 [S22].

### 3.4 Orifice flow equation (low pressure)

The standard form is:

Q = 1658.5 × A × C_d × √(h / SG)

- Q = gas flow in ft³/hr.
- A = orifice area in in².
- C_d = discharge coefficient.
- h = pressure in inches of water column.
- SG = specific gravity of the gas (air = 1).
- Then BTU/hr = Q × HHV (BTU/ft³).

Sources:
- Eng-Tips gives the 1658.5 constant [S33] (secondary; units were not stated, so they are inferred).
- ORNL MEASUR uses the same form with 1655: CFH = 1655 · C_d · f_corr · (A_ft² · 144) · √(P_inwc / SG). It credits the *Eclipse Combustion Engineering Guide* (1986) [S34].
- C_d = 0.9 is the basis of the Fisher and NFPA 54 orifice tables at 11 in. w.c. [S35] (snippet only).

Check against the NFPA 54-2006 Table F.1 values given in the Fisher reamer manual. I saw these only as OCR'd snippets, so they are unverified [S35]:

| Drill | Dia (in.) | Formula at 11 in. w.c., C_d 0.9, SG 1.52, 2,516 BTU/ft³ **(derived)** | NFPA 54 table (snippet) |
|---|---|---|---|
| #55 | 0.052 | 8.53 ft³/hr → 21,460 BTU/hr | 21,939 |
| #50 | 0.070 | 15.45 ft³/hr → 38,880 BTU/hr | 39,842 |

- The formula comes out about 2 % below the table. That is good enough for a calculator, but tune the constant before relying on it.
- Forum reports for #55 at 11 in. w.c. propane give 18,888 BTU/hr, which shows the spread between charts [S35].
- **Limit.** This form assumes the gas does not compress. It is fine in inches of water column but not at psi pressures. Real orifice flow reaches its maximum (chokes) when downstream absolute pressure falls below about 0.58 × upstream. The 0.58 comes from (2/(k+1))^(k/(k−1)) with k ≈ 1.13 for propane **(derived)**. That point is near 10 psig when the gas discharges to the atmosphere.
- For psi-level venturi burners, use the manufacturer's tables (3.2) or the √(psig) fit.
- **Do not use** the Industrial Monitor Direct example. Its result (≈ 0.5 SCFH for a 1/16 in. orifice at 20 psig) is wrong by orders of magnitude [S36].

---

## 4. Flue, chimney and draft

### 4.1 Rules of thumb

| Rule | Value | Source |
|---|---|---|
| Chimney height, natural draft (Olsen) | 3 × the downward pull + ⅓ × the horizontal pull | Olsen, *The Kiln Book*, cited on the CAD forum (secondary) [S37] |
| Same rule (Ward) | "Three times the interior height plus 1/3 the linear draw or chamber length" | [S32] |
| Ward worked example | 36 in. interior height and 54 in. linear draw (36 depth + 9 back wall + 9 to the chimney base): 3 × 36 + 54/3 = 126 in. (10.5 ft) | [S32] |
| Same rule (Olsen, Baker, Cardew, via archaeology review) | Olsen: 3 ft per ft of downward pull + 1 ft per 3 ft horizontal. Baker: 3 ft per ft down + 1 ft per 3.5 ft horizontal. Cardew measures downward pull from the springer, Olsen from the crown. | Peacey, *Internet Archaeology* 1 [S82] |
| Starting height (other books) | "approximately three times the inside kiln height" | Robinson, *Ceramics Monthly*, Apr 2020 [S30] |
| Forced-draft reduction | chimney "can be reduced by as much as 25 percent" with forced-draft burners | Kiln Book excerpt (secondary) [S38] |
| Power burners | chimney only needs to clear the building | [S26] [S32] |
| Exit flue area (Ward) | same area as the total of all burner (entrance) ports | [S32] |
| Exit flue area (Olsen) | "2.5 square inches of opening for each cubic foot" of chamber | Olsen via Iain Shields via D. Palmer (secondary) [S39] [S38] |
| Exit flue against ports (builder) | "a bit bigger than the burner ports combined" | [S39] |
| Exit flue against chimney (Olsen) | restrict the exit flues where they enter the chimney, so the chimney cross-section is larger than the flue area | *Kiln Book* 4th ed. p. 78, quoted on the CAD forum (secondary) [S37] |
| "Tuned flue" | smaller than the total burner port area. Works with venturis but can cause trouble with power burners. | [S32] |
| Too small a flue | back-pressure, safety-valve shutdowns, burned thermocouples, stalling | [S32] |
| Burner port taper | 15° preferred but not necessary | [S40] |
| Grate area against chimney (wood, Olsen) | grate about 10 × the chimney cross-section | (secondary) [S38] [S41] |
| **Olsen, read from the book** | Chimney height: p.80 (Principle 5) and p.130, measured inside the kiln. Exit flue: three methods, p.236 (total inlet area; 2½ in² per ft³; 1 in² per 7000 BTU/hr), he uses the first and third. Natural draft: inlet = exit = chimney section, p.78. Chimney ¼–⅕ of the chamber's diameter, p.80. Forced draft about 25 % shorter, p.79 and p.130–131. Grate 10 × the chimney, p.76 (he now uses about 7:1, p.77) | Olsen 4th ed. (Verified) |
| Consistent ratios? | A builder comparing Nils Lou and other books found "no consistent ratios" | [S37] |

Not found:
- Damper sizing rule: **NOT FOUND** (Ward's draft article gives none).
- Joe Finch's *Kiln Construction*: **NOT FOUND** (no online text).
- Rhodes' *Kilns: Design, Construction and Operation*: **NOT FOUND** online.

Example measured data: Robinson's 28 × 32 in. downdraft-converted kiln [S30]:
- Flue 35 in². In oxidation it was dampered to about 23–28 in².
- About 150,000 BTU/hr total near cone 10, from two MR-750s with #50 (0.070 in.) orifices.
- About 140 CFM of flue flow at about 10 ft/s.
- Burner floor hole 3.5 in. diameter.

### 4.2 Stack-effect draft equation

SI form [S42]:

ΔP = C · a · h · (1/T_o − 1/T_i)

- C = 0.0342 K/m.
- a = atmospheric pressure in Pa.
- h = stack height in m.
- T_o and T_i = absolute temperatures of the outside air and the average flue gas.

This is the same physics as ΔP = g·h·(ρ_o − ρ_i), with ρ ≈ 353/(273 + t °C) kg/m³ for air [S43].

US form **(derived)** from the SI form, at sea level (a = 101,325 Pa, 1 in. w.c. = 249.09 Pa):

ΔP (in. w.c.) ≈ 7.63 × H_ft × (1/T_o,°R − 1/T_i,°R)

Woodheat.org gives 1 Pa ≈ 0.004 in. w.c. [S44].

Wikipedia "Stack effect" gives the US form ΔP (psi) = 0.0188 · a (psia) · h (ft) · (1/T_o − 1/T_i) in °R [S80]. At a = 14.696 psia and 27.7 in. w.c./psi this is 7.65 in. w.c. per ft·(1/°R), within 0.3 % of the 7.63 derived above. Rumford.com states draft is proportional to height, flue temperature and atmospheric pressure [S81].

Draft-driven flow (first estimate) [S42]:

Q = C · A · √(2 g H (T_i − T_o)/T_i), with C = 0.65 to 0.70.

Worked example for the PNW kiln **(derived)**: a 12 ft (3.66 m) stack, 20 °F outside (266.5 K), and 1,000 °F average flue gas (810.9 K).
- ΔP = 0.0342 × 101,325 × 3.66 × (1/266.5 − 1/810.9) ≈ 32 Pa ≈ 0.128 in. w.c.
- The US form gives 7.63 × 12 × (1/479.7 − 1/1459.7) = 0.128 in. w.c.
- No source gave a worked kiln example.

### 4.3 Air at altitude (checked 2026-10-29)

The air's pressure and density at the site set the draft (a in §4.2) and how much a burner gives.
NASA Glenn's "Earth Atmosphere Model – Metric Units", troposphere, from the surface to 11,000 m
[S88] (Verified, read on the page):

- T = 15.04 − 0.00649·h, with T in °C and h in m.
- p = 101.29·[(T + 273.1)/288.08]^5.256, with p in kPa.
- ρ = p / [0.2869·(T + 273.1)], with ρ in kg/m³.

At 5000 ft (1524 m) this gives p = 84.4 kPa and ρ/ρ₀ = 0.862; √(ρ/ρ₀) = 0.928, which is Ward's
burner factor of 0.9279 printed in Olsen (4th ed. p.230). At 10,000 ft (3048 m), p = 69.8 kPa and
√(ρ/ρ₀) = 0.860, against Ward's 0.8579 (p.232), within 0.2 % **(derived)**. The engine uses this model for the draft's a and for
burner output at altitude (`gas.py`, altitude_factor).

---

## 5. Cross-draft and wood kilns

### 5.1 Cross-draft proportions
- Specific cross-draft ratios (port area, flue, chimney) from Olsen or others: **NOT FOUND** online.
- The Ward and Olsen chimney rule in 4.1 uses "linear draw" (the horizontal run). That makes it the rule to use for a cross-draft: 3 × chamber height + ⅓ × horizontal run [S32] [S37].

### 5.2 Wood firebox rules

| Rule | Value | Source |
|---|---|---|
| Total grate area | 12–25 % of the chamber floor area. 12–15 % is enough in most cases; 25 % is for fast, high-temperature (≥ 1300 °C) firing. | *The Self-Reliant Potter* (Norsker/GATE), via search snippet (secondary) [S45] |
| Grate against chimney | about 10 : 1 (Olsen). One builder found 10 : 1 gave "not enough pull" with a 9 ft chimney of 81 in². | (secondary) [S41] |
| Olsen Fast Fire, measured | exit flue = 79 % of the firebox entry area (69 % after a support brick was added) | (secondary) [S41] |
| Chamber : firebox volume | one builder: 16.24 ft³ ÷ 3.6 ft³ = 4.51. Claims "< 6.8 is considered overpowered". | [S46] |
| Same kiln | primary air inlet 13.5 in²; firebox-to-chamber port 81 in² (6 × the inlet); chimney outlet up to 81 in²; design chimney 12 ft | [S46] |

Bourry box proportions, based on Janine King and Steve Harrison's *Laid Back Wood Firing* [S47]. Areas are relative to chamber floor area = 100. V is the firebox volume above the hobs, as a % of the kiln volume W.

| Element | Case 1 | Case 2 | Small double Bourry |
|---|---|---|---|
| Exit flues | 8 | 11.1 | 7.6 |
| Chimney | 7 | 8.3 | 7 |
| Bag wall opening | 17 | 16.7 | 14.2 |
| Throat arch | 25 | 26.2 | 56.5 |
| Firebox above hobs (V) | 12 % of W | 17.9 % of W | 11.7 % of W |

### 5.3 Wood used per firing

| Kiln | Reported | Source |
|---|---|---|
| Olsen Fast Fire | "less than half a cord", cone 10 in 6–8 h (another article says 8–12 h) | marketing-style articles, unverified [S48] |
| Small conventional wood kiln | "a cord or more", 24–48 h | US patent 7,357,632 [S48] |
| Anagama (Univ. of Montevallo) | 14 cords per firing (1 cord ≈ 128 ft³, 2,000–3,000 lb) | [S49] |
| Anagama (Buck Creek) | 10 cords over 4 days | [S49] |
| Anagama (forum) | about 6 cords over 5 days | [S49] |
| Train kiln | **NOT FOUND** | |
| Bourry box | **NOT FOUND** | |

Off-grid note: only natural-draft (venturi) burners work without power, and they need real chimney height (3.3, 4.1).

---

## 6. Castables, cast domes and arches

### 6.1 Castable data

| Product | Max service | Material per ft³ | Bulk density | Water | Thermal k (BTU·in/hr·ft²·°F) | Source |
|---|---|---|---|---|---|---|
| Kast-O-Lite 30 LI Plus (HWI, insulating) | 3,000 °F | 92 lb/ft³ | 98 lb/ft³ after 220 °F; 92 after 1,500 °F | 17.0 % of dry weight (≈ 9.4 lb per 55 lb bag) | 5.6 @400 °F, 4.2 @800, 4.1 @1200, 4.5 @1600, 4.9 @2000 | HWI data sheet, via search snippets [S50] |
| Kast-O-Lite 30 LI Plus (retailer figures) | 3,000 °F | — | 90 lb/ft³ | 18 % by weight | — | [S51] [S52] |
| Kast-O-Lite 26 LI Plus (HWI, insulating) | 2,600 °F | 86 lb/ft³ | 90–100 after 220 °F; 86–96 after 1,500 °F | not readable; one snippet showed 20.0 % (**unverified**) | 3.6 @400, 3.4 @800, 3.5 @1200, 3.7 @1600, 4.0 @2000 | data sheet copy on Yumpu [S53] |
| Mizzou Castable Plus (HWI, dense) | 3,000 °F | NOT FOUND | 2.27 g/cc ≈ 142 lb/ft³ (**derived**, from a distributor snippet, unverified) | about 5 pints per 55 lb; never over 11.0 % | NOT FOUND | High Temp Tools FAQ via E. Lippert (secondary) [S54] [S55] |

Other Kast-O-Lite 30 LI Plus data [S50]:
- Modulus of rupture: 600 psi after 220 °F, 300 after 1,500 °F, 300 after 2,000 °F, 900 after 2,500 °F, 800 after 2,910 °F.
- Permanent linear change "None" (the test temperature was not visible in the snippet).

Bags per cubic foot **(derived)**:
- Kast-O-Lite 30 LI Plus: 92 ÷ 55 = 1.67 bags/ft³.
- Kast-O-Lite 26 LI Plus: 86 ÷ 55 = 1.56 bags/ft³.

Note: cone 10 is about 2,345 °F. Kast-O-Lite 26 LI is rated to 2,600 °F, which leaves little margin on the hot face.

### 6.2 Curing and dry-out

- **HWI general guidance** [S56]:
  - Cure at 70–90 °F. Below 70 °F, strength drops and curing takes longer.
  - Water leaves at these temperatures: free water at 212 °F; cement phases at 440, 530 and 1,020 °F.
  - Steam takes up about 1,600 times the volume of the water.
  - HWI's standard schedules apply to single-component linings 9 in. thick or less.
  - The schedule chart itself is an image, so the numbers are **NOT FOUND**.
- **Mizzou cure and dry-out** (High Temp Tools FAQ, secondary) [S54]:
  - Air cure 16–24 h above 60 °F, kept damp or covered. Keep it from freezing.
  - Single layer, 9 in. or less:
    - Ambient to 250 °F at 75 °F/h, then hold ½ h per inch of thickness.
    - 250 to 500 °F at 75 °F/h, then hold ½ h per inch.
    - 500 to 1,000 °F at 75 °F/h, then hold ½ h per inch.
    - 1,000 °F to operating temperature at 75 °F/h.
  - Never enclose castable in a vapor-tight casing (steam explosion risk).
- **Other manufacturers:**
  - BNZ's Blazelite AHP insulating castables can be fired at 100–200 °F/h with no holds (a different product) [S57].
  - AGC (Japan): 30–50 °C/h up to 900 °C for plastics and ramming mixes [S57].
- Kast-O-Lite-specific dry-out schedule: **NOT FOUND** in a readable form.

### 6.3 Anchoring

- Roofs need closer anchor spacing than walls (patent literature) [S58].
- Thicker linings: spacing of 2 to 3 times the anchor height (a single patent, not a standard) [S58].
- Vendor post (secondary) [S58]:
  - Walls 200–300 mm, closer on roofs.
  - Anchor height about ⅔ of the lining thickness, with tips 20–25 mm short of the hot face.
  - Tip temperature limits: SS304 about 800 °C, SS310 1,100 °C, Inconel 601 1,200 °C.
- Thermal Ceramics' "Suggested Anchor Spacing" table: **NOT FOUND** (only the table of contents was visible).
- Ceramic anchor spacing: **NOT FOUND**.
- Stainless needles as reinforcement: John Britt used Rib-Tec 400 1 in. needles at about 4 lb per 100 lb of castable [S59].

### 6.4 Formwork and cast arches

John Britt, Ceramic Arts Network, 2012-05-07 [S59]:
- A catenary arch of Phlocast 30 low-cement castable, 1.5 in. thick. He notes that castable "is usually cast 3 inches or more" thick.
- Backed with 5 in. of 2,000 °F fiber.
- Inner form of EPS foam on 4 in. legs. Outer form of two ¾ in. plywood arch pieces braced with 2×4s.
- Poured in 4 in. lifts, with plastic wrap at each joint as an expansion break. Forms were removed after 24 h.

Pizza-oven builders advise cast domes at least 3 in. thick and warn of slumping over a mold [S60].

Sand-form domes: **NOT FOUND** as a documented method with numbers.

### 6.5 Sprung arch geometry

- A sourced rule of "1.5 in. rise per ft of span": **NOT FOUND**.
- Forum builders use 2 to 4 in./ft. Angle-iron bracing holds the thrust [S61].
- A CAD forum post attributes to Olsen a minimum rise of 1½ in./ft and a maximum of 3 in./ft (secondary; **ask the user for Olsen p.__ to confirm**) [S84].
- A 60° skewback is called "standard" in a masonry supplier's form, and 60–70° is typical in masonry [S62].
- Geometry **(derived)** for a circular arch of span S and radius R:
  - Rise = R − √(R² − S²/4).
  - With R = S (a 60° central angle), rise = S × (1 − √3/2) = 0.134 S = **1.608 in. per ft of span**.
  - The skewback face lies along the radius, so it sits at 60° to horizontal.
  - This is probably where the "about 1.5 in./ft" folk rule comes from, but no source confirms it.
- Catenary arches: build them by hanging a chain and inverting the curve [S63]. A "height = base width" rule: **NOT FOUND**. Ward's volume formula treats the area as 2/3 × base × height (a parabola) [S28].

### 6.6 Catenary arch statics (checked 2026-10-27)

- Wikipedia [S63], verified: "a catenary is the ideal shape for a freestanding arch of constant
  thickness"; in the hanging chain "the forces of tension become forces of compression and
  everything is inverted". For y = a cosh(x/a): "The horizontal traction force at P1 and P2 is
  T0 = wa, where w is the weight per unit length of the chain or cable", and "the vertical
  component of the tension, T sin φ = ws" with the arc length s = a sinh(x/a).
- **Derived** for a catenary arch springing from the floor, with span S and height H inside:
  - a from H = a (cosh(S / 2a) − 1), solved numerically.
  - The inside arc is 2a sinh(S / 2a); the area under it is S(H + a) − 2a² sinh(S / 2a).
  - Each foot pushes out with H = w a and carries V = w a sinh(S / 2a), half the arch's weight,
    where w is the arch's weight per unit of its length (Σ density × thickness of its layers, per
    foot of kiln). Taken along the inside face: the ring's own thickness moves the line of thrust
    out a little.
  - This is the cold arch carrying only itself. How hot expansion changes it: **NOT FOUND**.
- How the outward push at a catenary's feet is held (a curb, ties, buttresses), and its sizes:
  **NOT FOUND**.

### 6.7 Domes over a rectangular chamber (geometry derived)

- A sail dome (domical vault): a sphere through the chamber's four top corners at the
  springline, rising `rise` above it at the centre. With c the half-diagonal of the chamber's
  inside, the radius is R = (c² + rise²) / 2 rise **(derived)**, as for a circular arch of span 2c.
- Where the sphere meets a wall's inside face, its curve is a circle of radius √(R² − (half the
  other side)²): each wall rises in a circular segment above the springline **(derived)**.
- The rise must stay under c, or the sphere bulges out past the walls.
- A dome's thrust on its walls: see `domes-over-doors.md`, which works it out (derived) from
  membrane theory and from Heyman's slicing of a half dome, with the rule the engine applies to a
  dome over a door. The steel that holds a dome: still **NOT FOUND**. Cast domes are noted in §6.4
  [S60].

---

## 7. Kiln car against door

| Topic | Note | Source |
|---|---|---|
| Brick-up door | cheapest to build; seal can be adjusted, good for wood, salt and soda; rebuilt every firing | Ray Brown, Studio Potter [S64] |
| Swing door | opens in seconds; saves handling brick and wear; needs hardware and design work | [S64] |
| Car on rails | wheels run on rails under the deck; the deck carries the ware | kiln-car patents [S65] |
| Car drawbacks | a heavy car top soaks up heat; heat is lost each time the car comes out | US 3,759,661 [S65] |
| Sand seal | apron on the car dips into a sand-filled channel; leaks gas, "far from perfect"; needs coarse sand so it won't blow out | patents [S65] |
| Fiber seals | alumina-silica fabric seal (patent); a forum builder's car door was all fiber | [S65] |
| Cost | car kilns "command even higher prices" (commercial units, a weak source) | [S65] |

- Builder cost or labour figures for car versus door on a site-built kiln: **NOT FOUND**.

---

## 8. Reduction firing

| Item | Value | Source |
|---|---|---|
| Oxidation before reduction | fire to about 1,652 °F (900 °C) to burn off organics and sulfur | Finkelnburg, *CM* Mar 2022 [S66] |
| Body reduction start | about 1,750 °F, for about half an hour (forum) | [S67] |
| Body reduction start | cone 010, for 20–30 min (forum) | [S67] |
| Body reduction start | 930 °C / 1,706 °F | Hawaii Potters Guild [S67] |
| Body reduction start | between cone 09 and 04; reduce about 45 min, clear 5–10 min (forum) | [S67] |
| Reduction hold | 1,652–1,742 °F (900–950 °C) for about 45 min; flue dampered to 2¼ in. | Robinson, *CM* Apr 2020 [S30] |
| Whole firing | normal reduction firing about 8–10 h (forum) | [S67] |
| Continuous (Plainsman C10RPL) | 10 °C/h to 120 °C; 50 °C/h to 550 °C; 100 °C/h to 980 °C; then light reduction while rising at 50 °C/h to 1,300 °C; 30 min oxidation as it drops about 100 °F. Total about 31.7 h. | Digitalfire [S68] |
| Atmosphere (O₂ : CH₄ by mole) | oxidation ≥ 2 : 1; light reduction just below 2 : 1; heavy reduction near 1 : 1 | [S66] |
| Oxidation definition | more than 3 % excess oxygen | Frenzel, CAN [S69] |

**Fuel effect:**
- No source gives a percentage fuel penalty: **NOT FOUND**.
- Sources agree that too much air wastes fuel heating extra nitrogen (about 3 lb N₂ per lb O₂) [S69] [S66].
- Derived estimate: with air at fraction λ of stoichiometric (λ < 1), at most about λ of the fuel's heating value is released in the chamber. The rest leaves as CO, H₂ and unburned fuel. So λ = 0.9 wastes roughly 10 % of the fuel during reduction. This is **(derived)**, an upper-level estimate that ignores dissociation and afterburning.

---

## 9. Material prices (US)

All prices were checked 2026-10-21. Listing dates are not shown on retailer pages.

| Item | Price | Seller | Source |
|---|---|---|---|
| G-23 IFB straight 9×4.5×2.5 in. (≈ K-23) | $5.60 each | Sheffield Pottery | [S70] |
| G-23 IFB straight, 3 in. | $6.50 each; 10-pack delivered $112.00 | Sheffield | [S70] |
| G-26 IFB straight 2.5 in. (≈ K-26) | $7.17 each (out of stock) | Sheffield | [S70] |
| G-26 IFB straight 3 in. | $8.38 each | Sheffield | [S70] |
| K-23 IFB (Thermal Ceramics), 10-pack | $62.40 (≈ $6.24 each) | High Temp Refractory Store (eBay, Portland) | search snippet [S71] |
| K-23 IFB, case of 24 | $193.57 + $118.58 shipping (listing updated 2025-05-17) | eBay | [S71] |
| Super Duty hard firebrick 9×4.5×2.5 in. | $5.45 each; 4-pack delivered $70.03 | Sheffield | [S70] |
| Kast-O-Lite 30 LI Plus, 55 lb | $115.21 | Refractory West | [S51] |
| Kast-O-Lite 30 LI, 55 lb | $103.24 | The Potters Center | [S72] |
| Kastolite 30 LI Plus, 55 lb | $98.18 | L&M (lmine.com) | [S52] |
| Kastolite 30 Plus, 55 lb | $114.40 | High Temp Refractory Store (eBay) | [S73] |
| Mizzou Plus, 55 lb | $83.05 | High Temp Refractory Store (eBay) | [S73] |
| Kast-O-Lite 26 LI, 55 lb | **NOT FOUND** | | |
| Litewate 23 insulating castable, 30 lb | $58.30 | Sheffield | [S74] |
| 3000 Loucast castable, 50 lb | $68.00 | Sheffield | [S74] |
| Ceramic fiber blanket 2,600 °F, 1 in. × 24 in. × 25 ft, 8 pcf | $150.00 | High Temp Refractory Store (eBay) | [S73] |
| Ceramic fiber blanket 2,300 °F, 1 in. × 24 in. × 25 ft, 6 pcf | $70.00 | same | [S73] |
| Superwool 607 HT, 1 in., 8 pcf, 50 ft² carton | $369.00 | Sheffield | [S75] |
| Kaowool board HT 2,600 °F, 1 in. × 2 × 3 ft | $399.00 (as listed) | Sheffield | [S75] |
| Angle iron 2×2×¼ in. × 20 ft (black) | $1.00/ft | Ferguson | [S76] |
| Kanthal A-1, 16 AWG, 50 ft | $17.50 (out of stock); 159 ft/lb → ≈ $55.65/lb **(derived)** | TEMCo | [S77] |
| Kanthal A-1, 23 AWG, 1 lb | $71.61 | TEMCo | [S77] |
| Kanthal A-1, 12–14 AWG per lb | **NOT FOUND** | | |
| GACO MR100 venturi burner | $159.95 | Ward | [S27] |
| GACO MR750 venturi burner | $99.95 | Ward | [S27] |
| Ransome B3 / B4 / B5 venturi burner | $245 / $295 / $395 | Ward | [S27] |
| Ward MB200 to MB700 power burner | $1,229 to $1,389 | Ward | [S22] |
| Ward 2-tank / 3-tank connector | $92.95 / $123.95 | Ward | [S24] |

Not found:
- Seattle Pottery Supply, Axner and Clay-King: no readable price pages (404, or category pages with no prices).

---

## 10. Quick check for the PNW kiln (all derived)

This uses the plan's inputs: 35 ft³, cone 10, IFB walls, four 100 lb cylinders, 20 °F.

**Demand:**
- 35 ft³ × 10,000–16,000 BTU/ft³/hr (Ward, 9 in. IFB, cone 10) = 350,000–560,000 BTU/hr.
- That is about 3.8–6.1 gal/hr (÷ 91,502 BTU/gal).

**Supply at 20 °F, four cylinders in parallel** (assuming their capacities add, an inference):
- Full: 4 × 167,000 = 668,000 BTU/hr (table 2.1).
- Half full: 4 × 94,000 = 376,000 BTU/hr (table 2.1).
- 25 % full, keeping 10 psi: 4 × 43,300 = 173,200 BTU/hr (table 2.2).

**Elements:** 11.5 kW × 3,412 BTU/kWh ≈ 39,200 BTU/hr.

**Result:** the supply check passes with full cylinders. It is marginal at half full. **It fails under the conservative table.** The engine should report both tables.

---

## Sources

- [S1] Propane Warehouse, "LP Gas Properties". https://propanewarehouse.com/helpful-information/lp-gas-properties/
- [S2] Pro Tank Supply, "Propane Facts and Properties". https://protanksupply.com/lpg-info-videos/propane-facts-properties/
- [S3] Flame Engineering, "Propane Information". https://flameengineering.com/pages/propane-information
- [S4] NREL / Alternative Fuels Data Center, fuel properties comparison. https://nrel.gov/docs/fy21osti/78477.pdf (via search summary)
- [S5] Univ. of Illinois NPRE 470, "Lower and Higher Heating Values of Gas, Liquid and Solid Fuels" (GREET). https://courses.grainger.illinois.edu/npre470/sp2018/web/Lower_and_Higher_Heating_Values_of_Gas_Liquid_and_Solid_Fuels.pdf (via search summary)
- [S5b] WPGA comment to CARB LCFS. https://www.arb.ca.gov/lists/com-attach/6-lcfscalculators23-ws-Wm5SegEyBW9QeAQ2.pdf (via search summary)
- [S6] NIST Chemistry WebBook, propane saturation properties. https://webbook.nist.gov/cgi/fluid.cgi?Action=Data&Wide=on&ID=C74986&Type=SatT&TUnit=F&PUnit=psia&DUnit=lbm%2Fft3
- [S7] US EIA, "Carbon Dioxide Emissions Coefficients". https://www.eia.gov/environment/emissions/co2_vol_mass.php
- [S8] Emerson/Fisher, *LP-Gas Serviceman's Handbook* (LP-10). https://d1-auth.emerson.com/documents/automation/lp-10-handbook-pl-pl-9718536.pdf (could not open; snippet only)
- [S9] PERC, *Propane Technical Pocket Guide*. https://cloudinary.propane.com/image/upload/v1664396780/Residential:Commercial/Brochures/4482-BR-21_Technical-Pocket-Guide_v3_HRpg.pdf (compressed PDF; snippet only)
- [S10] Motorsnorkel, "Propane Consumption Rate". https://motorsnorkel.com/propane-consumption-rate/ and US Carburetion. http://www.uscarburetion.com/propane_usage.htm (snippets only)
- [S11] Monnick Supply, propane cylinder chart. https://www.monnicksupply.com/MGR/pdf/Propane_chart.pdf (snippet only)
- [S12] Search summary of distributor handouts (Scribd "VaporizationChart", L.B. White "Propane Tank Sizing"). https://www.scribd.com/document/479321858/VaporizationChart and https://www.lbwhite.com/application/files/3317/0931/0356/Propane-Tank-Sizing.pdf
- [S13] P. Thurst, "Care and feeding of Propane Fueled Generators", Engineering Radio, 2010 (updated 2023). https://www.engineeringradio.us/blog/2010/10/care-and-feeding-of-propane-fueled-generators/
- [S14] Nova Scotia Safety Bulletin 0000034 (June 2024). https://novascotia.ca/lae/healthandsafety/docs/safety-bulletin-0000034-en.pdf (snippet only)
- [S20] Ward Burner Systems, "LP Tank Sizes for Various Kiln Sizes". https://www.wardburner.com/tank-sizes/
- [S21] Ward, "Gas Pressure: The Basics". https://www.wardburner.com/gas-pressure-basics/
- [S22] Ward, Power Burners. https://www.wardburner.com/burners/power-burners/
- [S23] Ward, "Propane Tank Freeze Up" (*Clay Times*, Nov 2003). https://www.wardburner.com/tank-freeze/
- [S24] Ward, LP Tank Gang Connectors. https://www.wardburner.com/burner-components/tank-gang-connectors/
- [S25] Ward, "Regulators and How They Work". https://www.wardburner.com/regulators-work/
- [S26] Ward, "Forced Air vs Venturi Burners". https://www.wardburner.com/technical-info/forced-air-vs-venturi-burners-2/
- [S27] Ward, Venturi Burners. https://www.wardburner.com/burners/venturi-burners/
- [S28] Ward, Data Guide. https://www.wardburner.com/technical-info/data-guide/
- [S29] Ward, "BTU Requirements for Various Kilns" (*Clay Times*, Sep 1996). https://www.wardburner.com/btu-requirements/
- [S30] B. Robinson, "Downdraft Kiln Conversion", *Ceramics Monthly*, Apr 2020. https://ceramicartsnetwork.org/ceramics-monthly/ceramics-monthly-article/Downdraft-Kiln-Conversion
- [S31] Ward, Orifice Charts & Plugs. https://www.wardburner.com/other-products/orifice-charts-plugs/
- [S32] Ward, "Draft and Its Importance". https://www.wardburner.com/draft-important/
- [S33] Eng-Tips, natural gas consumption thread. https://eng-tips.com/threads/natural-gas-consumption.82231
- [S34] ORNL MEASUR Tools Suite, leakage CFH formula. https://industrialresources.ornl.gov/measur/suite/docs/group__leakage__cfh__formula.html
- [S35] Fisher Type P520L reamer manual (NFPA 54-2006 Table F.1). https://d1-live.emerson.com/documents/automation/manuals-type-p520l-reamer-instruction-manual-fisher-en-en-6115260.pdf (snippet only); forum values from https://www.smokingmeatforums.com/threads/increasing-heat-for-a-gas-grill.310210/post-2252921
- [S36] Industrial Monitor Direct, orifice flow for propane (contains errors). https://industrialmonitordirect.com/blogs/knowledgebase/orifice-flow-rate-calculation-for-propane-under-pressure
- [S37] Ceramic Arts Daily forum: "Chimney Entrance Reduction" and "kiln chimney questions". https://community.ceramicartsdaily.org/topic/17145-chimney-entrance-reduction/ and https://community.ceramicartsdaily.org/topic/31906-kiln-chimney-questions/ (via search summary)
- [S38] F. Olsen, *The Kiln Book*, 3rd ed. (Krause, 2001, ISBN 0873419103) and 4th ed. Excerpts seen only in search snippets. Not linked.
- [S39] D. Palmer, "How I Built (and Rebuilt) a Better Gas Kiln", 2024. https://danpalmerceramics.com/2024/05/15/building-and-rebuilding-a-better-gas-kiln/
- [S40] Ward, Burner Placement. https://www.wardburner.com/technical-info/burner-placement/
- [S41] CAD forum, "First Wood Fired Kiln Build, Problem Stalling". https://community.ceramicartsdaily.org/topic/40861-first-wood-fired-kiln-build-problem-stalling/ (via search summary)
- [S42] Wikipedia, "Flue-gas stack". https://en.wikipedia.org/wiki/Flue-gas_stack
- [S43] Engineering ToolBox, natural draught ventilation. https://www.engineeringtoolbox.com/natural-draught-ventilation-d_122.html
- [S44] Woodheat.org, "How chimneys work". https://woodheat.org/how-chimneys-work.html
- [S45] *The Self-Reliant Potter*, "2.3 Combustion and fireboxes" (NZDL). https://www.nzdl.org/cgi-bin/library?cl=CL1.16&d=HASH014964359ef24fc9c7f5c7c4.4.3 (403; snippet only)
- [S46] Dr. Stienecker, "Wood Fired Ceramic Kiln – Kiln Design". https://drstienecker.com/woodkiln/wood-fired-ceramic-kiln-kiln-design/
- [S47] SideStoke, "Bourry box kiln". https://www.sidestoke.com/bourrykiln/bourry.html
- [S48] FARM Infrastructure articles. https://www.farmstandapp.com/?p=351107 ; US 7,357,632. https://patents.google.com/patent/US7357632
- [S49] The Alabamian (Montevallo). https://thealabamian.com/ums-anagama-kiln-roars-to-life-once-again ; Bangor Daily News 2009. https://www.bangordailynews.com/2009/05/29/living/all-fired-up/ ; cactiguide forum. https://cactiguide.com/forum/viewtopic.php?p=399760
- [S50] HWI, KAST-O-LITE 30 LI PLUS Product Data (10/19). https://ssfbs.com/wp-content/uploads/2021/06/KAST-O-LITE_30_LI_PLUS.pdf and Clay-Planet copy. http://shop.clay-planet.com/pdfs/kast-o-lite-30-li-plus-data.pdf (snippets only)
- [S51] Refractory West, KOL30LIP55P. https://www.refwest.com/Details?item=KOL30LIP55P
- [S52] L&M, Kastolite 30LI Plus. https://www.lmine.com/product/kastolite-30li-plus-refractory-3000f/
- [S53] HWI, KAST-O-LITE 26 LI PLUS Product Data (1/09), Yumpu copy. https://www.yumpu.com/en/document/view/47076251/ii-i-kast-o-liter-26-li-plus-jjmedinacomec ; original https://ssfbs.com/wp-content/uploads/2021/06/KAST-O-LITE_26_LI_PLUS.pdf
- [S54] E. Lippert, "Mizzou castable refractory instructions" (quoting the High Temp Tools FAQ), 2012. https://ericlippert.com/2012/08/21/mizzou-castable-refractory-instructions/
- [S55] Distribution International, Mizzou Castable Plus 55#. https://shop.distributioninternational.com/refractories/refractories-castable/recamplus55h (403; snippet only)
- [S56] HWI, "Curing and Dryout of Refractories". https://thinkhwi.com/curing-dryout-refractories/
- [S57] Search summary: BNZ Blazelite AHP; AGC drying method. https://www.agcc.jp/Portals/0/images/en/core/alumi/about/methodDrying.pdf
- [S58] Search summary: anchor patents (e.g. US 4,479,337). https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/4479337 ; vendor post https://cn.linkedin.com/in/zzjsrefractory
- [S59] J. Britt, "How to Build a Solid Arch Ceramic Kiln with Castable Refractory", CAN, 2012-05-07. https://ceramicartsnetwork.org/daily/article/How-to-Build-a-Solid-Arch-Ceramic-Kiln-with-Castable-Refractory
- [S60] Forno Bravo forum, cast dome threads. https://community.fornobravo.com/forum/good-background-information/introductions/469418-hi-thinking-about-building-a-cast-refractory-dome-oven
- [S61] CAD forum, "My kiln build" p. 2 and "metal frame for sprung arch kiln". https://community.ceramicartsdaily.org/topic/14840-my-kiln-build/page/2/ and https://community.ceramicartsdaily.org/topic/15978-metal-frame-for-sprung-arch-kiln/
- [S62] Masonry Magazine, "Jack Arches". https://masonrymagazine.com/blog/2021/03/31/jack-arches/ (via search summary)
- [S63] Wikipedia, "Catenary". https://en.wikipedia.org/wiki/Catenary
- [S64] R. Brown, "Swinging Door Conversion", Studio Potter. https://studiopotter.org/node/1951
- [S65] US 3,759,661 (Kiln cars). https://patents.google.com/patent/US3759661A/en ; US 3,854,865. https://patents.google.com/patent/US3854865A/en ; sand-seal patents via search summary; cost guide https://new.risingsunartscentre.org/news/kiln-cost-guide-price-ranges-for-us-buyers-2026.html
- [S66] D. Finkelnburg, "Techno File: Reduction", *Ceramics Monthly*, Mar 2022. https://ceramicartsnetwork.org/ceramics-monthly/ceramics-monthly-article/reduction
- [S67] CAD forum, "reduction fire ^5/6 gas length of time". https://community.ceramicartsdaily.org/topic/14424-reduction-fire-56-gas-length-of-time/ ; Hawaii Potters Guild. https://www.hawaiipottersguild.org/glazes/oxidation-amp-reduction-firing (via search summary)
- [S68] Digitalfire, C10RPL schedule. https://digitalfire.com/schedule/c10rpl ; glossary https://digitalfire.com/glossary/reduction%20firing
- [S69] H. Frenzel, "How to Fire a Gas Kiln Efficiently", CAN (2013, republished 2026-03-11). https://ceramicartsnetwork.org/daily/article/How-to-Fire-A-Gas-Kiln-Efficiently-Hal-Frenzel-Answers-this-Burning-Question
- [S70] Sheffield Pottery, kiln building bricks (products.json). https://www.sheffield-pottery.com/collections/kiln-building-refractory-bricks
- [S71] eBay High Temp Refractory Store and K23 listing. https://www.ebay.com/str/hightemprefractorystore ; https://ebay.com/itm/202269160961 (via search summary)
- [S72] The Potters Center, Kast-O-Lite. https://thepotterscenter.com/products/kast-o-lite-castable-refractory-harbison-walker
- [S73] eBay High Temp Refractory Store (fetched). https://www.ebay.com/str/hightemprefractorystore
- [S74] Sheffield Pottery, castables and mortars. https://www.sheffield-pottery.com/collections/kiln-cement-and-castable-refractory-mortars
- [S75] Sheffield Pottery, blanket and board. https://www.sheffield-pottery.com/collections/bricks-refractories-and-kaowool
- [S76] Ferguson, 2×2×¼ in. × 20 ft angle. https://www.ferguson.com/product/2-x-2-x-1/4-in.-x-20-ft-iron-angle-in-black-baikkb20ft/2122272.html (via search summary)
- [S77] TEMCo Industrial, Kanthal A-1. https://temcoindustrial.com/electrical/wire/resistance-wire/?page=5 (via search summary)
- [S78] Northern Arizona Univ., "Composition of the Earth's Atmosphere" (O₂ 20.95 %, N₂ 78.08 %, Ar 0.93 % by volume, dry air). https://jan.ucc.nau.edu/jclark/Education%20Mesonet/Composition of the Atmosphere.htm (via search summary)
- [S79] Pearson AFR calculator (propane AFR_st = 5 × (32.00 + 3.76 × 28.0134)/44.10 ≈ 15.6); EngineLabs, "What is the stoichiometric point" (propane ≈ 15.5). https://www.pearson.com/channels/it/calculators/afr-calculator ; https://www.enginelabs.com/?p=5717 (via search summary)
- [S80] Wikipedia, "Stack effect" (US form, C = 0.0188). https://en.wikipedia.org/wiki/Stack_effect (via search summary; mirrors on chemeurope/handwiki are copies, not independent)
- [S81] Rumford.com, "Chimney draft". https://rumford.com/draft.html (via search summary)
- [S82] A. Peacey, "Superstructures" §11.1.5, *Internet Archaeology* 1 (Olsen, Baker and Cardew chimney rules). https://intarch.ac.uk/journal/issue1/peacey/supers.html (via search summary)
- [S83] CAD forum, "inlet height vs chimney height" (Olsen: downdraft inlet area = outlet area, secondary). https://community.ceramicartsdaily.org/topic/4294-inlet-height-vs-chimney-height/
- [S84] CAD forum, "metal frame for sprung arch kiln" (Olsen arch rise 1½–3 in./ft, secondary). https://community.ceramicartsdaily.org/topic/15978-metal-frame-for-sprung-arch-kiln/
- [S85] Laguna LE-2040 gas kiln listing (54.1 ft³, 541,000 BTU/hr max, cone 10 ≈ 10,000 BTU/ft³/hr derived). https://www.theceramicshop.com/product/39374/laguna-model-le-2040-gas-kiln/ ; NM Clay 11.67 ft³ cone 10 kiln, 280,000 BTU/hr (≈ 24,000 BTU/ft³/hr derived). https://nmclay.com/ok2831gas-kiln-28-25-x-31-5-gas (via search summary)
- [S87] NIST Chemistry WebBook, methane, gas-phase thermochemistry: ΔcH°gas −890.7 ± 0.4 kJ/mol (Pittam and Pilcher, 1972), molar mass 16.0425 g/mol. https://webbook.nist.gov/cgi/cbook.cgi?ID=C74828&Mask=1 (read 2026-10-29)
- [S88] NASA Glenn Research Center, "Earth Atmosphere Model – Metric Units" (troposphere: T, p and ρ against altitude; last updated 13 May 2021). https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html (read 2026-10-29)
- [S86] Reach.dog / High Temp Tools, Kast-O-Lite 30 (90 lb/ft³, 3,000 °F, k = 4.54 BTU·in/hr·ft²·°F at 2,000 °F); Distribution International, Kast-O-Lite 30 LI G Plus (1.44–1.6 g/cc). https://acceptance.reach.dog/shop/hightemptools/products/kast-o-lite-30-5 ; https://shop.distributioninternational.com/refractories/refractories-castable/recakl30lip55h (via search summary)

---

## Corroboration (2026-10-24)

Rule: an item needs ≥ 3 **independent** sources. Resellers reprinting one sheet count once: Propane Warehouse [S1] and Pro Tank Supply [S2] are one source; Flame Engineering [S3] is reproduced by both, so table 2.1 is one source; Motorsnorkel and US Carburetion [S10] are one. Ward pages [S20]–[S32] count as one source (one company). Search-summary-only sources are weaker than a read page.

Engine uses (grep of core/src/kilndesigner): combustion.py and gas.py (HHV 91,502 BTU/gal, §1.1), castable.py (O₂ 20.95 %), data/gas.yaml (§2.1, 2.2, 2.4, 1.2, 3.1–3.3), gas.py (chimney §4.1, flue 2.5 in²/ft³, draft §4.2), masonry.py and geometry.py (arch §6.5, cure §6.2), hybrid.py (λ = 0.9, §8), materials.yaml (§6.1), prices.yaml (§9).

| Item | Independent sources | Agreement | Notes / discrepancies |
|---|---|---|---|
| Propane HHV per gallon | 5 ([S1/S2], [S3], [S4], [S5], Ward [S20]) | 91,410–91,690; spread 0.3 % | Engine 91,502 is inside the spread. OK. |
| Propane LHV | 3 ([S4], [S5], [S5b]) | 84,250 vs 84,950 BTU/gal (0.8 %) | Small basis difference. |
| HHV per ft³ vapor | 3 ([S1/S2], Ward [S21], CM [S30]); 2,516 in §3.4 has 1 weak blog | 2,488 vs 2,500 rounded | §3.4 table uses 2,516; 1.1 % above [S1]'s 2,488. Affects only the derived orifice check. |
| Liquid density | 3 ([S1/S2] 4.20, [S3] 4.23, NIST [S6] 4.228) | 0.7 % | Ward's 4.5 rejected (7 % high). Engine 91,502 BTU/gal implies 4.20 basis. |
| Vapor SG | 3 ([S1] 1.50, [S3] 1.53, Ward [S22] 1.522) | 2 % | OK. |
| O₂ in air 20.95 % | 3 ([S1] stoich basis, NAU [S78], textbook AFR calc [S79] uses 3.76 N₂/O₂ = 21.0 %) | agree | castable.py 0.2095 OK. |
| Stoich air 23.86 ft³/ft³ | 3 ([S1], derivation, [S79]) | 23.8–23.87 | CM "≈ 25" [S30] is a rounding (5 % high). |
| Mass AFR 15.67 | 2 published ([S79] 15.6, 15.5) + derivation | **15.67 derived vs 15.6 (0.4 %) and 15.5 (1.1 %)** | Difference is molar-mass/air basis (21 % vs 20.95 %). Not used by engine found in grep. |
| Vapor pressure (NIST) | 3 (NIST [S6], [S3], Ward [S23]) | within 3 psi | [S1/S2] runs 4–22 psi high; disagreement unchanged. |
| 100 lb cylinder table 2.1 | **only 1 source** ([S3]; [S1]/[S2] copy it; a Country Plans forum post (countryplans.com/smf/index.php?msg=149128) cites the same table) | — | gas.yaml relies on it. Still short. |
| Conservative table 2.2 | **only 2** ([S10], [S11]) | agree where read | Emerson LP-10 [S8] likely holds the original; not readable. |
| ASME table 2.4 | **only 1** (secondary [S13]) | — | gas.yaml uses it; original source unnamed. |
| D×L×K rule | 2 ([S1/S2], [S12]) | agree | **only 2 sources found**. |
| Ward BTU/ft³/hr table 3.1 | **only 1 primary** (Ward [S28], [S29] same author) | Laguna LE-2040 ≈ 10,000 and NM Clay ≈ 24,000 BTU/ft³/hr [S85] bracket Ward's ranges; forum 14,000 [S85 search] | Not independent confirmation of the table; data/gas.yaml depends on Ward alone. Ask the user for Olsen's burner-sizing figures (Olsen p.__). |
| Venturi/power burner ratings 3.2, 3.3 | 1 (manufacturer data) | — | Manufacturer ratings; 1 source is appropriate (it is the data sheet). |
| Orifice equation | 3 (Eng-Tips [S33], ORNL/Eclipse [S34], NFPA 54 Table F.1 via Fisher [S35]) | constant 1655 vs 1658.5 (0.2 %); formula 2 % below NFPA table | Unchanged. |
| Chimney rule 3H + L/3 | 4 (Ward [S32], Olsen via CAD [S37], Peacey on Olsen/Baker/Cardew [S82], Robinson [S30] for the 3H part) | agree in form | **Baker uses L/3.5, not L/3** (≈ 4 % lower height for Ward's example: 123.4 vs 126 in.). Olsen measures downward pull from the crown, Cardew from the springer; gas.py uses interior height, which matches Ward. |
| Flue 2.5 in²/ft³ (Olsen) | **only 2, both secondary** ([S38], [S39]) | — | gas.py FLUE_SOURCE uses it. Ward's rule (flue = burner port area) [S32] and Olsen via [S83] (inlet = outlet for downdraft) are a different basis. **Ask the user for Olsen p.__**. |
| Stack-effect ΔP | 4 (Wikipedia flue-gas stack [S42], Wikipedia stack effect [S80], Engineering ToolBox [S43], Rumford [S81]) | US form 7.65 vs 7.63 derived (0.3 %) | Both Wikipedia articles share editors; counted as one would leave 3. OK. |
| Draft flow C = 0.65–0.70 | 2 ([S42], [S80], same wiki family) | — | **only 1–2 sources found**. |
| Arch rise / 60° skewback | 3 for 60° (Masonry Magazine [S62] 60–70°, forum [S61], geometry derivation); rise: Olsen 1½–3 in./ft via [S84], forum 2–4 in./ft [S61] | partly | The doc's earlier "1.5 in./ft NOT FOUND" is now secondarily attributed to Olsen [S84]; derived 60° arch rise 1.608 in./ft sits inside Olsen's 1½–3 range. Ask the user for Olsen p.__. masonry.py §6.5 value unaffected. |
| Kast-O-Lite 30 LI Plus | 3 for density/rating ([S50] HWI 92–98, [S51]/[S52] 90, [S86] 90 and 90–100) | 90 vs 92 lb/ft³ (2 %) | k at 2,000 °F: **HWI 4.9 vs High Temp Tools 4.54 BTU·in/hr·ft²·°F (7 % lower)**; materials.yaml uses HWI. |
| Mizzou cure schedule | **only 1** ([S54] quoting High Temp Tools) + HWI general [S56] | — | masonry.py §6.2 cites it. |
| Reduction λ = 0.9 | derived only; atmosphere ratios 1 source [S66] | — | **only 1 source**; hybrid.py REDUCTION_AIR is an estimate. |
| Wood firebox, Bourry, wood use | 1–2 each, mostly secondary | — | Unchanged; ask the user for Olsen p.__ on grate/chimney ratio. |
| Prices | 1 each (a price is a single listing) | — | Not applicable. |
