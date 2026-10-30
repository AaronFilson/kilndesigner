# Top-down gas firing: design notes

Status: work in progress, last updated 2026-10-27. These notes come from one design conversation. Nothing here is in the engine. Under ADR 0009 the engine should refuse a top-fired layout until there is test data.

How values are marked:
- **(sourced)**: from `docs/research/`, the research report, or a cited patent or data sheet.
- **(derived)**: calculated from sourced inputs. The model in `models/` shows the working.
- **(model)**: from a model whose loss or heat-transfer figures are assumed, not measured. Treat it as a trend.
- **(inference)**: reasoning with no test behind it.

---

## 1. The kiln and the idea

- **The kiln:** a converted electric kiln.
  - 10-sided, about 23 in across, three 9 in rings (27 in tall), 2.5 in walls, about 7 ft³.
  - Brick grade unconfirmed; K-23 assumed.
  - A 3–4.5 in castable (Mizzou) ring could go on top.
- **Flue:** a 9 × 9 in flue/chimney is available. Its height, and where it enters the kiln, are **not known yet**.
- **Last firing:** as a downdraft with high-pressure burners it reached cone 13–14 at the top and cone 8 at the bottom.
  - That is 1,331–1,365 °C against 1,249 °C at 60 °C/h, a spread of 82–116 °C (sourced: `core/src/kilndesigner/data/cones.yaml`).
  - Even heating matters more to the owner than speed. The kiln fires in reduction.
- **Burners on hand:** two Ward/GACO MR-100 venturi burners.
- **How the idea changed over the conversation:**
  1. Propane burners with a cast manifold in the lid, spreading the flame in two half-moon arcs around the perimeter.
  2. Low-pressure (3–11 in w.c.) burners entering at the top of the side wall, so the lid stays unmodified. A Mizzou manifold ring with nozzles around the inside.
  3. The same, with no blower and no secondary air.
  4. Two MR-100s sealed straight down into the lid at 11 in w.c., with a hot chimney or a fan for draft. Deliberately rich for reduction, with no manifold.

## 2. What the research found

The full report is in `research-report.md`, and the four sets of notes behind it are in `research-notes/`. In short:

- **No studio pottery kiln was found with burners in its lid.** Every gas top-loader, raku kiln and electric conversion surveyed fires from the floor and uses the lid as the flue.
- **Top-down firing exists elsewhere:**
  - Knife forges.
  - Glory holes: Canned Heat Glory Hole 12 (tangential top burner) and Trimble's 1893 patent US509146.
  - Ladle covers: Holley's US4014532, with rim burners firing tangentially and fed by steel flexible hose. This is the closest precedent.
  - A lid-fired melting furnace: Aisin's US10598437.
  - A shuttle kiln: Hendryx's US3854865, with burners above the ware and the exhaust through the floor.
  - Roof-fired tunnel kilns (US5667378, US4240788, US4368036A), glass tanks, reheat furnaces and reformers.
- **Every precedent that fires down into a stacked load exhausts at or near the floor.** Even then, the top heats faster than the bottom (Fives US7637739).
- **Forge builders say a straight-down burner splits into two counter-rotating swirls** and leaves a hot stripe, and they avoid it.
- **Material limits at a cone 6–10 hot face (sourced):**
  - Gray iron is good to about 760 °C (ASTM A319).
  - 310 stainless to 1,035 °C when heated and cooled every firing.
  - Inconel 601 to about 1,205–1,250 °C.
  - Propane ignites in air at 920–1,120 °F (`combustion-and-masonry.md` §1.1). No gas-air mix can sit in hot castable.
- **Codes:** UL 21 LP-gas hose is rated to 60 °C. NFPA 86 covers unlisted kilns of any size. No code was found for burners on a lid that moves.

## 3. Pressure, push and draft

- **The buoyancy is small.** From the top ports to the floor flue (0.72–0.75 m at 1,250–1,285 °C), the kiln's own buoyancy is only about 7 Pa (0.03 in w.c.) (derived).
- **Mixer energy bound.** At 100% air premixed, a mixer can deliver at most supply pressure ÷ 24.86 to the manifold, because 23.86 volumes of air ride along with each volume of gas (derived). That's 110 Pa at 11 in w.c. and 30 Pa at 3 in w.c.
- **A realistic mixer gets about a ninth of that.** With ordinary inlet, mixing and diffuser losses, the best geometry delivers 12 Pa at 11 in w.c. and 3.4 Pa at 3 in w.c., giving ports at 3.6 and 1.9 m/s with nothing pushing back (model).
- **Full premix at 3–11 in w.c. can't both pull in its air and leave useful port velocity.** 10 m/s ports need about 3.5 psi of gas and 15 m/s ports about 9 psi (model).
- **Expansion adds volume, not pressure.** Combustion at constant pressure creates no push.
  - With the 9 × 9 in flue, the full-fire hot gas (about 44 L/s) leaves at 0.8 m/s and needs only 0.08 Pa (derived).
  - So the gas will flow top to bottom easily. Getting it to flow isn't the problem.
- **Chimney suction at the ports** (derived; chimney gas averaging 500–900 °C, 0.5 Pa friction):

| Chimney height above floor flue | Top ports | Floor ports |
|---|---|---|
| 4 ft | −1.5 to −3.4 Pa | −8 to −10 Pa |
| 6 ft | −6.0 to −8.8 Pa | −12.5 to −15 Pa |
| 8 ft | −10.5 to −14.2 Pa | −17 to −21 Pa |
| 10 ft | −14.9 to −19.6 Pa | −21.5 to −26 Pa |

- **The chimney is what makes low-pressure top firing possible.** It pulls air in around each burner at the top. A venturi then only has to premix 50–70% of its air.
- **Partial premix is the safe kind (inference, textbook flame speeds).** Full premix is what burns back at low velocity, because propane flame speed peaks near full air. These flame speeds aren't in `docs/research/` yet.

## 4. Where the heat lands (evenness)

- **The gas drops its heat in the first space it reaches (model).** The coupling between hot gas and surfaces in one shelf space is about 50–100 W/K, mostly gas radiation. The burner flow carries about 13 W/K. So the gas gives up about 98% of its excess heat in the first space it enters.
- **Heat moves down mostly by radiation through the shelves.** That's estimated at about 85 W/K per shelf for SiC and about 50 W/K for cordierite (model, estimated, not measured). Pushing the gas down carries only about an eighth of the heat that moves downward.
- **Results from `models/evenness.py`**, for the kiln at cone 10 soak:

| Where the heat goes in | Spread, SiC shelves | Spread, cordierite shelves |
|---|---|---|
| All at the top | 130 °C | 200 °C |
| All at the top, kiln gas stirred 5× (needs a fan or high-velocity burners) | 78 °C | 100 °C |
| 70% top, 30% bottom | 52 °C | 83 °C |
| 54% top, 46% bottom (balanced) | 23 °C, middle coolest | 36 °C, middle coolest |

- **The model probably underrates radiation through the shelves.** It makes top-only firing worse than the measured 82–116 °C of the last downdraft firing. Use the rows as a comparison.
- **Heated from above, the gas settles into layers and doesn't mix.** Heated from below, it turns over (inference). That favours putting some heat in low.
- **A straight-down jet behaves differently from a ring of soft flames (model, fountain scaling).**
  - The scaling: penetration ≈ 1.85–2.46 × M^¾ / B^½. The coefficients are textbook (Turner) and **not yet in `docs/research/`**.
  - The plain 11 in w.c. gas jet at 50,000 BTU/hr has about 15 mN of momentum and should reach 0.9–1.2 m down. A blower-fed jet at 20 m/s (about 100 mN) reaches 3.8–5 m. The kiln is about 0.69 m deep.
  - So a focused jet with a clear path can carry heat to the floor. It likely sets up a loop: down the jet, across the floor, up through the ware, back into the jet (inference). That puts heat in at the bottom from a burner at the top.

## 5. Candidate designs

### A. Full-premix ring at about 7 psi (superseded: the owner wants 3–11 in w.c.)

Two inspirators of 50,000 BTU/hr each, each feeding a half-ring manifold of 10 ports. Sized by `models/inspirator.py`:

| Part | Size |
|---|---|
| Gas supply | 6.9 psi at full fire |
| Orifice | #60 drill (0.040 in) |
| Mixing tube | ½ in Sch 40 pipe (0.622 in ID), 5–6 in long. Within 2% of the best throat size |
| Air inlet | Bell mouth with a shutter. A sharp edge costs about 28% of the air |
| Diffuser | Cone from ½ in to 1¼ in, 7° included angle, about 6 in long |
| Manifold | 1¼ in Sch 40 half-ring, fed at its middle. Port-to-port spread about 1% (end-fed 1 in: about 9%) |
| Ports | 5/16 in OD × 0.035 in 310 stainless tube, 13.3 m/s at full fire, into ½ in flame pockets in the castable |
| Floor flue | About 16 in² for 3 Pa |
| Stack | Top at least a foot above the burners |

- **Turndown:** 70% flow at 3.4 psi gives ports at 9.3 m/s; 50% at 1.7 psi, 6.7 m/s; 30% at 17 in w.c., 4.0 m/s.
- **Keep the manifold off the castable.** The outside of a Mizzou ring runs about 290–540 °C (model), near propane's ignition temperature. Stand the manifold off 2–3 in in open air.

### B. Two rings of low-pressure natural-draft burners (proposed; depends on chimney height)

- **Layout:**
  - **Top ring:** five burners at the top of the side wall, on alternate sides, ports about 2 in below the lid and at least 2 in above the ware. Angled about 35° off straight-in, all turning the same way.
  - **Bottom ring:** five burners on the other sides, about 1.5 in above the floor, firing under a bottom shelf raised on 3–4 in posts. No bag wall.
  - **Exhaust:** the floor flue, preferably central, to the chimney, with a damper.
- **Each burner:**
  - Orifice: #59 (0.041 in), centred 1–1.5 in ahead of the tube.
  - Body: ½ in Sch 40, 6–8 in long, with a bell-mouth inlet and shutter.
  - Tip: a flame-retention tip.
  - Port: a 1¼ in hole with a sliding collar over the gap around the burner.
- **Output per burner** (orifice equation in `combustion-and-masonry.md` §3.4): 6,900 BTU/hr at 3 in w.c., 10,500 at 7 in and 13,200 at 11 in. Ten burners give 69,000, 105,000 and 132,000.
- **Demand:** cone 10 needs an estimated 80,000–110,000 BTU/hr at the top of the firing (derived). That covers about 7 kW through the walls plus 1–2 kW to keep climbing, at 10–30% excess air.
- **Primary air:** about 65% with no draft, rising with draft (model). Set it to 50–70% with the shutter.
- **Gas train:**
  - A first-stage regulator.
  - Two adjustable 3–11 in w.c. regulators, one per ring, each with a gauge.
  - A ball valve and a flame-failure valve per burner.
  - A quarter-turn main shutoff.
- **Firing:**
  1. Light the bottom ring first.
  2. Light the top ring only once a top spy hole draws, about −0.01 to −0.02 in w.c.
  3. Near peak, start with the top ring at 11 in and the bottom at about 7.5 in, about 55/45 by heat.
  4. Reduce with the shutters and collars, keeping the top just below zero draft.
- **If you add the castable ring,** use K-26 insulating brick with small cast port blocks, or wrap the Mizzou in fibre. Solid Mizzou would add about 2 kW of heat loss.

### C. Two MR-100s sealed straight down into the lid (latest idea; works only with a fan on the burners)

- **Sealed, the only air is what the venturis pull in.**
  - Ward gives 30–50% for venturis (sourced, §3.3). The model gives 28–37% at Ward's 11 in w.c. rating of 94,000 BTU/hr per burner.
  - Propane's rich limit, 9.6% gas in air, is 40% of full air (derived from §1.1). So the mix is at or past the point where it stops burning as a flame.
- **Most of the heat never gets released.** At most about the air fraction of the fuel's heat is released in the kiln (§8, derived). Two burners at 188,000 BTU/hr of gas would release at most 56,000–94,000. The rest leaves as CO, hydrogen, soot and propane.
- **Reduction needs an oxidizing start.** It's an oxidizing climb to about 900 °C, then slightly short of air: light reduction just under full air, heavy about half (Finkelnburg, *Ceramics Monthly*, in §8, figures for natural gas). Sealed venturis can never oxidize.
- **Draft can't pull enough air through a sealed burner (model):**

| Burner | Air with no draft | Suction for 90% air | Suction for 105% air |
|---|---|---|---|
| Ward's 94,000 BTU/hr orifice, 1 in tube | 37% | 204 Pa | 292 Pa |
| Ward's 94,000 BTU/hr orifice, ¾ in tube | 28% | 619 Pa | 883 Pa |
| Orifice for 50,000 BTU/hr at 11 in (0.080 in), 1 in tube | 53% | 44 Pa | 67 Pa |
| Orifice for 50,000 BTU/hr at 11 in, ¾ in tube | 40% | 144 Pa | 208 Pa |

- **A fan up the chimney doesn't fix it.** At 60 Pa every square inch of gap admits about 3.9 L/s, half the air the kiln needs per 100,000 BTU/hr (derived). The leaks would set the atmosphere. The unburned fuel would also burn, or go off in puffs, where the fan's air meets it in the chimney.
- **What works: put the fan on the burners.**
  - Box the MR-100 inlets and feed them from one blower through a gate, or use power burners. Ward's are rated at 11 in w.c. propane; the MB200 has a 50 CFM blower.
  - Full air is about 16 CFM per 100,000 BTU/hr. A blower of 25–30 CFM at about 1 in w.c. static pressure covers the kiln.
  - Gas: about 50,000 BTU/hr per burner. Drill #46 (0.081 in) orifices for 11 in w.c., or run Ward's 11 in orifices at about 3 in.
- **Firing:** about 105–110% of full air until about 900 °C, then 90–95% for reduction. Keep the top just below zero draft.
- **Burn-back returns with a near-full mix.** Keep the tips set back from the lid's hot face. Run the blower after shutdown, or hot gas rises out through the burner tubes.
- **For the jets to reach the floor (inference):**
  - Leave a clear column under each burner.
  - Put a target tile where each jet lands. Riedhammer uses deflector stones in US4368036A.
  - Keep the floor flue away from the landing spots.

## 6. Safety list (all designs)

- **Flame supervision on every burner.** NFPA 86 reportedly asks for the gas to close within 4 s of flame loss (secondhand). Thermocouple valves take about a minute.
- **Purge before every lighting.** A sealed kiln holds gas.
- **Oxidize below about 900 °C.** Below 500–600 °C a flame that goes out isn't relit by the kiln.
- **Blower-fed designs:** an air-flow switch that shuts off the gas if the blower stops.
- **Burners on the lid:** a switch that shuts the gas off before the lid lifts. Keep hoses and regulators out of the heat rising off the lid (UL 21 hose is rated to 60 °C).
- **CO:** a CO alarm, and a stack exit away from people. Expect flame at the stack during reduction.
- **Top brick:** K-23's class temperature is 1,315 °C on the 2025 Morgan sheet; an older sheet says 2,300 °F. The last firing's top (1,331–1,365 °C) exceeded it, so check the top brick.

## 7. Open questions and next steps

Inputs needed from the owner:
- Chimney height above the floor flue, and where the flue opens in the floor.
- Shelf material (SiC or cordierite) and the target cone.
- Brick grade of the rings and lid.
- The MR-100's tube size and the orifice behind Ward's 11 in w.c. rating.

Data to source into `docs/research/` before any of this goes near the engine:
- Propane laminar flame speed, and how it changes with mix and preheat temperature.
- Fountain penetration coefficients for round buoyant jets.
- NFPA 86 clauses: flame-failure timing, purge, combustion-air proving, lid or door interlocks.
- Turndown for Ward's power burners.
- Measured conductivity for the actual brick.

Tests:
- **Bench-test one burner in open air** before it goes in the kiln. Check the flame shape at 3, 7 and 11 in w.c. with the shutter open and closed.
- **First firings:**
  - Cone packs on the top, middle and bottom shelves.
  - A draft gauge at a top spy hole.
  - An O₂/CO reading at the flue if one is available.
- **Compare the spread** against the table in section 4 to calibrate the model's shelf-radiation figure.

## 8. Models

Run from the repo root. Each script prints its tables:

| Script | What it covers |
|---|---|
| `models/inspirator.py` | The mixer model; delivered pressure and air at 3–11 in w.c.; the energy bound; supply needed for full premix; design A sizing, turndown, throat sensitivity, manifold uniformity; Mizzou ring cold face |
| `models/low_pressure.py` | Partly premixed pipe burners against chimney suction (design B); orifice outputs; port-gap air; chimney suction table; 9 × 9 in flue loss |
| `models/evenness.py` | The five-space lumped model behind the evenness table |
| `models/sealed_lid.py` | Design C: sealed venturi air against suction, leak air, jet penetration |

Assumed coefficients:
- **Mixer losses:** air inlet 0.05, mixing 0.15, diffuser recovery 0.80, orifice discharge 0.90 and velocity 0.96, burner tip exit 1.5 velocity heads.
- **Outside heat-transfer coefficient:** 15–35 W/m²K.
- **Gas coupling and shelf radiation:** as in section 4.

All of these are assumptions and should be replaced by measurements as they come in.
