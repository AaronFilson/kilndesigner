# Engine v2: the problem set

What a kiln designer needs the engine to answer, the physics behind each answer, what engine v1
does today, and what Olsen's reference kilns can and can't test. It starts from the brief of
2026-11-09 ("rebuild the heat and static forces engine from the reference kilns") and corrects
it where the code or the sources say otherwise; §8 lists the corrections.

**Decided 2026-11-09 (ADR 0017).** v2 replaces v1 now, and v1's tests prove nothing until v2 is
rebuilt. v2 works from first principles, fits nothing to these kilns, and flags no kiln until it
works as a whole. Statics comes first, after the software survey. Where this file describes v1,
it says what v2 must do better.

Sources: v1's code at a859fde (`core/src/kilndesigner/`); the physics reviews
(`docs/reviews/2026-11-physics-review-heat.md`, `-structure.md`); the research files named in
each section; and the reference dataset (`core/tests/v2/reference_kilns.yaml`). Olsen is *The
Kiln Book*, 4th ed., cited by page.

## 1. The questions

| # | Question | The answer a designer needs, with its working |
|---|---|---|
| Q1 | Will it reach its cone on the heat available? | Yes or no at the top temperature, and the margin: heat kept in the kiln against heat lost |
| Q1a | How long, on a given schedule? | Hours, and where the kiln falls behind the schedule |
| Q1b | What fuel, electricity and cost? | Per firing, in the fuel's own unit (gallons, therms, cords, tons, kWh) |
| Q2 | How evenly will it fire? | Hot and cold places (top and bottom, front and back, chamber by chamber), how far the ware lags the chamber, how the draft carries the flame |
| Q3 | Will it stand, cold and hot? | Arches, vaults and domes under their own weight; hot arches pushing on frames, ties, bands and walls; walls sliding and overturning; door headers, fireboxes, chimneys; the foundation |
| Q4 | Is it safe to stand near, and does the steel stay cool enough? | Shell and steel temperatures, clearances |
| Q5 | Are the parts big enough? | Burners and their gas supply (propane vaporisation), elements, chimney, flues, grates, fireboxes |
| Q6 | Will it last? | Each brick against its service rating, thermal shock and spalling, creep under load |

Q6 is added to the brief's five: v1 already answers part of it (`heatloss.service`), and two
reference kilns print service lives (Hollyweird: about twice a year for 25 years, over 1,500 h at
top temperature, p.117; the Olsen fibre kiln fired twice a day, p.62).

## 2. Heat

### 2.1 The energy balance of a firing

Over a firing, for every kind of heat:

    fuel or electricity in = walls (stored + lost from the shell) + ware and setting
                             + flue gas (sensible heat at its exit temperature)
                             + unburnt fuel (CO, H₂, smoke, char) + openings and leaks
                             + fireboxes, flues and chimney (stored + lost)

| Term | Physics | Source and range | v1 |
|---|---|---|---|
| Fuel in | gas: burner rating × time at each setting; oil: gal/hr; wood and coal: the stoker's rate | Olsen ch. 8; Ward's tables | gas at Ward's or Olsen's rule input, not the printed burners; electric at the designed elements; **wood, coal and oil refused** (M7) |
| Walls | transient conduction in layers, k(T), c_p(T); each face 1D, area growing with depth | ADR 0015; checked against erf and the steady solver | done, every hot face held at one chamber temperature |
| Shell | still-air convection (Churchill–Chu, Lloyd–Moran, Jaffer for a face down) and radiation | thermal-properties.md §5 | done |
| Floor | on the ground: a steady disc into dry soil (Incropera Table 4.1 case 10); over fireboxes: no loss (FixedSurface 0) | heat review #5 | steady; about half the floor's early loss missed |
| Ware and setting | c_p(T) enthalpy, 800 J/(kg·K) at 24 °C, VDI fireclay to 1200 °C | heat review #1 | done, lumped at the chamber's temperature; no reaction heats (not sourced) |
| Flue gas | products of combustion at the exit temperature and λ | Cantera, ADR 0012 | exit taken at the chamber's temperature; λ fixed at 1.15 (3 % O₂), 0.9 in reduction above 900 °C |
| Unburnt | equilibrium CO and H₂ below λ 1 | cantera-tespy-review.md §2, #3 | propane only, through available heat |
| Openings, leaks | radiation out of spy holes and flues; air drawn in round doors and stoke holes | grey enclosure with an open face (radiation-exchange.md §1.3); leaks unsourced | none |
| Fireboxes, flues, chimney | their own walls store and lose heat | as the walls | **none**: an under-floor firebox isn't a face, and its floor face is adiabatic |

The baseline's first finding is how much this balance matters for the fuel-burning kilns. Driven
along the book's own firings with unlimited heat, v1's walls take 45–96 kWh in the fast-fire kiln
(empty, no ware), against 1,160–2,496 kWh in the quarter cord it burns (p.139, p.143): an implied
firebox efficiency of 2–8 %, where measured wood pottery kilns run 12.4–21.6 % and 18 %
(firebox-efficiency.md §2). The missing terms are the ware and setting, the under-floor
fireboxes' brick (90 low-duty firebricks, Fig 5-39, p.140), the chimney, and above all a flue gas
leaving at cone 10 with whatever excess air the stoking gives. A model that ignores them can't
predict a wood kiln's fuel, and an efficiency fitted to cover them would hide which one is wrong.

### 2.2 What decides a firing's time

The brief asks how long a firing takes. That has two different answers.

- **Fixed input** (gas or oil burners at a printed rating, elements at a printed power): the heat
  model predicts the time. A printed time is then a test, but only as an inequality unless the
  book says the kiln was fired flat out: a potter firing slower than the burners allow is
  consistent with any model that is fast enough. Olsen's 36 ft³ cross-draft (p.226) and the 36 ft³
  IFB updraft (p.226, W15) are his own statements of what the burners did.
- **Stoked fuel** (wood, coal, drip oil): the stoker sets the rate. The time is the stoker's
  choice, within two physical limits: the heat the kiln must take along the way (the model), and
  the most fuel the fire can burn, which the air the draft draws and the grate set. A printed time
  and a printed fuel together test the energy balance (§2.1). Neither alone tests the heat model.

So the draft is a heat question: it limits the air, and so the fuel, a natural-draft kiln can
burn, and it sets λ, which sets the flue loss. Olsen's chimney rules (p.80, Rule 5; p.76–77, the
7 : 1 grate) are empirical and include the setting's resistance, which no open source quantifies
(heat review #4, #16).

### 2.3 Inside the chamber

| Mechanism | Matters for | Source | v1 |
|---|---|---|---|
| Convection, gas to surfaces | the gas's temperature over the walls and ware | (forced-flow correlations; none read for a kiln) | infinite: every hot face at the chamber's temperature |
| Gas radiation, CO₂ and H₂O | the dominant transfer above about 1000 °C; flue gas leaving hotter than the ware (+8 to +35 % fuel, heat review #2) | Hottel/Leckner or a weighted-sum-of-grey-gases fit (radiation-exchange.md §4, being researched); Cantera's is unsuitable (cantera-tespy-review.md §5) | none |
| Radiation between faces | floor and door cold, crown hot; the ware's lag | `thermal/radiation.py`: Howell C-11, C-14, Lienhard eq. 10.42, checked | built, not coupled |
| Hot emissivity of refractories | the exchange's size | not found yet (radiation-exchange.md §4) | – |
| The setting | an obstruction to radiation and flow, and a heat sink | no closed-form factors; options in radiation-exchange.md §3 | a heat sink only |
| Flame luminosity (soot) | wood and oil flames radiate far more than clean gas | not sourced | none |

### 2.4 Several gas zones

Twenty-four of the reference kilns aren't one well-stirred chamber:

- **chambers in series** (Bidai, Kawaii, Kyoto, Suzuki, Tobe, Fujiwara, Kitade, Hotchkiss,
  Blakebrough's Sturt kiln, Chappell, Olsen's two- and three-chamber kilns): each chamber's
  exhaust preheats the next, and each is finished by side-stoking in turn. Printed stage times
  describe that sequence: the Suzuki kiln's firebox 15 h to 1000 °C, then 7 h for each of
  chambers 1–3 and 5 h for each of 4–7, 56 h in all to cone 8–9 (p.93);
- **tubes and tunnels** (anagama, Tamba, Bae's gilgama, La Borne, the groundhogs, Hollyweird,
  Kannofen, Conrad's teardrop): the gas cools along the length, the front hotter than the back;
- **multi-directional** (Fireworks, Church): two crossing gas paths.

v1 heats each as one node at one temperature (its `chamber_cones` only shares out the steady loss).
A zone model, gas zones in series along the gas path, each with its faces and its ware, is the
smallest model that can say which chamber reaches which cone, and the book prints several such
spreads (§6).

### 2.5 Through the walls and under the floor

v1's 1D finite volumes per face, with k(T) and c_p(T), are sound (ADR 0015, energyplus-review.md
§2). Missing: the edges and corners (the shape factors of Incropera Table 4.1, to be read), the
ground's transient (energyplus-review.md §5, Kiva's method, GC10a blocked), earth banked against a
wall (the anagama dug into a hill; groundhogs dug in), and the Picard update of lagged properties
in fast ramps (energyplus-review.md §7 #4).

### 2.6 Elements

v1 holds the elements' power at its hot value from cold (heat review #8: cold power 4–6 % more,
first hours only). Only one reference kiln is electric (`electric-car-45`), and the book prints no
firing time for it; electric validation has to come from elsewhere (Olsen's W25 element example,
p.258–260, already reproduced; Table 9-6, p.257, kW against volume for 28 kilns).

## 3. Statics

### 3.1 What holds a kiln up

Masonry on Heyman's assumptions: no tension, compression unlimited, no sliding (Heyman 1966,
*The Stone Skeleton*; arch-thrust-theory.md, masonry-statics.md). The safe theorem: if any line
(or network) of thrust in equilibrium with the loads lies inside the masonry, the structure
stands. Sliding is a separate check (Huerta 2001; Gilbert, Casapulla & Ahmed 2006), and it governs
where the normal force is small, as in the top courses of a wall under a skewback (structure
review #3).

The questions, and the physics each needs:

| Part | Cold | Hot |
|---|---|---|
| Arch or vault (2D) | a thrust line in the ring; the geometric factor of safety; the least thickness (Couplet–Heyman) | the maximum-thrust state when the frame holds the span (HarbisonWalker reproduced by Heyman's hinges, arch-thrust-theory.md §3); past it, the frame's give |
| Dome | membrane to 51.8°, cracked lunes past it (Lau 2006); thrust networks (Maia Avelino et al. 2020) | the band at the springing; no hot method found |
| Crossing (groin) vault | slicing or a thrust network (masonry-statics.md M4); built kilns wait on it | – |
| Walls and buttresses | the resultant inside the base and in its middle third; sliding at each bed joint | the same at the hot thrust |
| Frames, ties, bands | AISC 360-16 §F10, tension on rods, Appendix 4 at temperature | expansion 3/32 in/ft (Olsen p.51; Brosnan), springs, the give of a bolted frame |
| Door headers, fireboxes, chimneys | arches and lintels; a free-standing bag wall "has a tendency to collapse" (p.134–135) | – |
| Foundation | bearing on concrete (AISC J8) and soil | heat into the slab |

Material data for anything past geometry and friction are **not found**: hot elastic modulus,
creep, hot modulus of rupture, hot cohesion of a joint, an allowable bearing stress on refractory
(structure review #19, refractory-movement-and-mortar.md §3). A v2 statics stays with limit
analysis (geometry, weight, friction) and says it can't check thermal stress or creep.

### 3.2 What v1 does, and where it is permissive

v1's methods are listed in the structure review (fixed three-hinged line with middle-third and
middle-half checks, HarbisonWalker's tables and heated factors, 5.34 × past them, catenaries,
sail domes as slices, round domes on the membrane theory with Lau's lunes past 51.8°,
Couplet–Heyman for vaults along the depth, crossings, doors and dome slices, AISC angles, wall
sliding and overturning). Every reference kiln builds without an error, by design (ADR 0014).

That can't show v1 is right: a permissive engine passes every kiln that stood. Three Olsen kilns
changed past a published collapse limit (the baseline's negative probes) all pass v1 without a
statics error or warning:

1. **meaders-david with a 3 in ring** on its 60 in half-circle (t/r 0.095, under the 0.1075 at
   which no line of thrust fits a semicircle; Maia Avelino et al. 2020 give 0.1079 by TNA). v1
   reports an 18 lb/ft thrust "carried by the kiln's masonry". The Couplet–Heyman ring check runs
   for vaults along the depth and for crossings, not for a roof arch across the width.
2. **singh-coal's dome as a 1 in hemisphere** (t/R 0.024, under Heyman's 0.042 and Lau's 0.041 with
   hoop forces): v1 only notes that the band isn't sized outside Lau's range.
3. **the fast-fire arch declared buttressed** (`roof.buttressed: true`, no frame): nothing checks
   that its 4½ in IFB side walls carry the thrust. By hand, 30 lb/ft cold at 36 in against a wall
   of about 34 lb/ft overturns it many times over; Olsen bolts a frame on (p.139).

So v2's statics needs negative cases from the literature as much as the 53 positive ones:
analytic least thicknesses, published collapse tests, and kilns changed past them
(`docs/research/engine-v2-negative-cases.md`).

### 3.3 Inputs the statics can't avoid assuming

Most arch rises in the design files are not printed: about 30 of the sprung arches take Olsen's
1½ in/ft for a featheredge (p.25, p.51) or his 4–6 in/ft for chamber kilns (p.296). Many wall
thicknesses, ring materials and every brick density are the design file's. A built kiln judged
sound is therefore a test of the method and the file's assumptions together; the dataset keeps
them apart (status `assumed`, with the file's reason).

## 4. Safety: the shell and the steel

v1 works out the shell temperature from the steady loss (every face) and the frame steel's (176 °F
in the examples), against Giles's 600 °F continuous limit for steel (structure review #13). The
transient matters here too: a thick wall's shell peaks hours after the chamber does. The reference
kilns print no shell temperature; the one documented failure is a shed roof that melted and caught
fire when flame leaked through the arch, door and salt ports (Chappell's salt kiln, p.243): a
clearance and leak question, not a conduction one. Olsen's Table 1-12 prints two walls' cold faces
(227 °F and 248 °F, p.39).

## 5. Sizing the parts

Burners (Olsen Rule 1, Ward's table, the orifice equation p.216), propane vaporisation (cylinder
and tank tables), elements (Kanthal's equations, Olsen's W25), chimney and flue (Olsen's Rules,
p.76–81), grates (7 : 1, p.76–77; coal ÷ 8, p.206). v1 does these, keeping each rule of thumb as a
starting size and the physics as the refusal (ADR 0014). The reference kilns give printed burner
ratings, orifices and pressures (§6); the gas-supply checks (propane vaporisation) need firing
draws, which only the gas kilns' times give.

## 6. What the reference kilns can test

(Counts from `core/tests/v2/reference_kilns.yaml`; see the dataset's header for the statuses.)

**The dataset.**
- **Kilns:** 53 with a design file: 34 wood, 14 gas, 2 coal, 1 oil, 1 wood and oil, 1 electric.
- **Facts:** 1,546.
  - By status: 852 printed, 73 derived, 60 scaled (each with its spread), 66 read off drawings,
    495 assumed (each with its reason).
  - By group: heat 302, chamber 324, lining 203, flow 353, structure 290, service 74.
- **Gaps and notes:** 277 gaps (what the book doesn't give) and 95 notes (disagreements between
  the notes, the docs and the design files).

**The heat figures the book prints**, as facts, and the kilns that have them:

| Figure | Facts | Kilns |
|---|---|---|
| Firing time | 17 | 12 |
| Fuel per firing | 8 | 7 |
| Fuel rate | 11 | 10 |
| Cone | 15 | 8 |
| Evenness (cone spreads) | 20 | 19 |
| Stage times | 14 | 6 |
| A burner input, as a total | 1 | 1 |

Kinds of test:

| Test | Kilns | What it checks | Limit |
|---|---|---|---|
| T1 reaches its cone | every kiln; numerically only where the input is printed (gas burners, oil nozzles) | available heat at the top ≥ steady loss | an inequality |
| T2 time at a printed input | gas kilns with printed burners and time | the transient model and the flue loss | an inequality unless fired flat out |
| T3 fuel against heat | wood and oil kilns with a printed fuel and time | the whole energy balance (§2.1) | wide: a cord's weight alone spans 2,070–4,200 lb oven-dry (wood-fuel.md [W4]) |
| T4 a printed log | the fast-fire's p.309 log | the shape of the heat-up, the stoker's rate | one firing |
| T5 evenness | printed cone spreads by chamber or top to bottom | the zone model's ordering | qualitative |
| S1 stands | all 53 | no admissible-state failure on a built kiln | positive cases only |
| S2 falls | negative cases (§3.2) | the checks catch a real failure | from the literature, not the book |

**Printed against assumed.** Every comparison names the inputs the design file assumes. A miss on
a kiln whose chamber is assumed (the kits are cubes of their printed volume; the 36 ft³
cross-draft's dense brick is backed with insulation because bare brick couldn't reach cone 10 on
its burners) says as much about the assumption as about the model.

**Calibration.** The free quantities a v2 heat model will have, λ through a firing, the unburnt
share, the ware load and the setting's flow resistance, must not be fitted to the same kilns that
then validate it. If any is calibrated, half the fuel-reporting kilns are held out and both sets
reported. Olsen's own quarter cord already sits inside the sourced firebox-efficiency range
(firebox-efficiency.md §2 derives a lower bound from it), so the fast-fire can't validate that
range.

## 7. What the reference kilns can't test

- Electric kilns: one, with no printed time.
- Coal: two kilns, but no heating value or composition for coal is sourced; Singh's shovels have
  no weight (Table 5-1, p.133).
- Shell temperatures, steel temperatures, and any structural failure: none printed for a modelled
  kiln.
- Ware loads: rarely printed, so the ware's share of the heat is assumed or banded.

## 8. Corrections to the brief's understanding

1. **v1 simulates 15 of the 53 kilns.** It refuses every wood, coal and oil firing (35 wood, 2 coal,
   1 oil; `simulation.heat_supply`, plan milestone M7). Wood use is only given for a wood kiln fired
   on gas, as gas heat ÷ the user's firebox efficiency (`simulation._wood`).
2. **v1 sizes burners by rule, not by the printed ones.** `design_gas` takes Ward's or Olsen's
   BTU/ft³/hr × volume; the burner count and rating in a design don't set the simulated input. The
   baseline passes the printed input explicitly.
3. **A stoked kiln's firing time isn't a heat-model prediction** (§2.2); the printed time and fuel
   together test the energy balance.
4. **The fixed hinge line is not the only statics weakness.** v1 is also permissive: no ring check
   on an across-width roof arch, an info note for a dome too thin to stand, and `buttressed`
   taken on trust (§3.2).
5. **The kits' printed volumes are stacking space** (pp.169–170, p.173), but the design files take
   them as the chamber to the springline; the kit-24's burners are uncertain between ten MR-750s
   (750,000 BTU/hr) and ten simple mixers on its printed #32 orifice (540,000; p.220–222).
6. **The ware's reaction heats** (dehydroxylation, water) remain unsourced; bisque and raw-glaze
   firings take more heat than v1 or v2 can count.
7. **No hot material data for statics** (§3.1): creep, hot E, hot MOR and allowable bearing stay out.

## 9. Open questions

The open decisions were settled on 2026-11-09; see `docs/adr/0017-engine-v2.md`, "Decisions".
The data still missing is listed kiln by kiln in the dataset's `gaps` (277 entries).
