# Science review, 28 October 2026

A review of the engine's physics, data and rules of thumb. It checks them against the sources in
`docs/research/`, the makers' data sheets, and the project's own rules: every number traces to a
source (CLAUDE.md), every result carries its working, and outside the checked range the engine
refuses (ADR 0009).

**Scope.** Four domains were reviewed at commit `b150dce`:
- heat and electric;
- gas and combustion, including `docs/top-down/`;
- structure and masonry;
- materials, castables and costs.

Each reviewer read the code, the data files and the research notes. They recalculated the numbers
that matter and fetched primary sources where the notes cite them. Nothing in the engine was
changed.

**How sure.** Findings marked ✔ were checked again independently while writing this up:
- the missing files;
- the breaker check;
- the door in a springing wall;
- the 5 psi burner rating.

The rest rest on one reviewer's evidence, which is given with each finding.

**Severity.**
- **Critical:** can give an unsafe kiln without a word.
- **Major:** gives a materially wrong number, or passes a design that would fail.
- **Minor:** a small error, a missing reference or an unclear message.

## Fix these first

> **Status, end of 28 October:** fixes 1, 3 and 5 are done (fix 1 with the owner's rules for
> domes and flat roofs), and most of the structure, bug and coverage items. Fixes 2 and 4 wait on
> the missing research files. See `docs/planning/10-28-26.md`, "Status at the end of 28 October".

1. ✔ **A door or car in a wall the roof stands on** (critical, structure 1). A sprung arch springs
   from the left and right walls, and a sail dome bears on all four. The engine lets the door or
   car go in any of them, and nothing carries the roof across the opening.
   - All five sprung-arch examples put the door or car in the right wall. In gas-crossdraft, the
     skewback sits on the dry-stacked door. With a hinged door it sits on the door. On the car
     kiln, the springing wall rolls out with the car.
   - The PNW hybrid design (a dome, with its door in the front wall) has the same problem.
   - The catenary already refuses side-wall doors (`model.py:477-493`).
2. **The check for organics burning off during dry-out misses the shipped example** (critical,
   materials 1).
   - It takes each mix alone and compares it with the burners' installed power. It should add up
     every mix and compare with what the schedule needs.
   - In `diy-castable-test-kiln`, the dextrin and paper give off about 122 kW together. The kiln
     needs 3–25 kW at that stage, and the report says nothing.
3. ✔ **Nothing stops a breaker far too big for the kiln** (major, safety; electric 1).
   - A 4 kW kiln on its 60 A breaker draws 16.7 A. NEC 422.11(E), which `electric-and-thermal.md`
     §3 already records, allows at most 25 A.
   - The leads, terminal block and cord go unprotected.
4. **Gas supply and pressure are optimistic exactly where the stall check matters** (gas 1, 2, 5
   and 6).
   - The "⅓ full" tank table is the 50%-full rule, about 23% high at 0 °F.
   - The 100 lb cylinder table is read by air temperature, but its source gives it by liquid
     temperature. At 20 °F air that is 32% high.
   - The tank pressure ceiling ignores the liquid cooling by 20 °F under draw.
   - The 10 psi cylinder limit leaves no room for the regulator.
   - Together these can pass a supply that stalls on a cold day.
5. ✔ **Burners are listed "at 5.0 psi" when the load is below their 5 psi rating** (gas 4).
   - At 5 psi a burner gives its full rating, not the load. So the kiln draws 1.7–2.2 times the
     input the supply check assumed.
6. **Burner input ignores wall thickness** (gas 3). Ward's table assumes 9 in insulating brick or
   6 in fibre.
   - A 2.5 in wall loses about three times as much heat, so the burners come out undersized with
     no warning.
   - This is the user's own test kiln: 2.5 in walls.
7. **Arch rules the source states are not enforced** (structure 2, 4, 5 and 6). Specifically:
   - HarbisonWalker's 1–3 in of rise per foot of span (2–3 in for IFB);
   - its thickness limit T ≤ (h − S/48) ÷ cos(θ/2);
   - insulation laid over the arch is counted as arch ring;
   - nothing checks that the thrust line meets the buttress steel;
   - an arch wider than its walls is cut short without a finding.
8. **Large kilns crash, or lose their burners** (gas 7).
   - Above about 130 ft³, `design_report` raises `ValueError` because the chimney table runs out.
   - Above 8 burners, the design silently gets none.

## Across all domains

- ✔ **Six cited research files don't exist**, and never have in git history:
  - `thermal-properties.md`
  - `electrical-supply.md`
  - `cones.md`
  - `castables.md`
  - `castables-minerals.md`
  - `arch-thrust-theory.md`

  They are cited as the source for:
  - every ingredient in `ingredients.yaml`;
  - six firebricks in `ifb_conductivity.yaml`;
  - PCE cones 15–42;
  - the hot-arch thrust theory;
  - the wire-over-kiln margin;
  - the Rayleigh-range warnings;
  - most constants in `castable.py`.

  Where reviewers could check the numbers against makers' sheets, they were right: the K and JM
  bricks, the steam constants and Mizzou's dry-out. The ingredient densities, LOIs, kyanite
  temperatures, quartz figures and burnout window could not be traced at all.
- **Out of range is a note, not a refusal.** These are all `info` where ADR 0009 asks for a
  refusal or at least a warning:
  - k(T) extrapolated below a data sheet's first point;
  - Rayleigh numbers outside a correlation's range;
  - arch T/S above 10%;
  - wire thinner than Kanthal's groove range;
  - the 17.5 W/in² surface load beyond its alloy and temperature.

  Extrapolating k(T) linearly downward gives fibre less conductive than still air.
- **JM 23 conductivity is 14–17% low at 400–600 °C.** Both the electric and materials reviewers
  found this independently. It comes from a 2011 excerpt the research doc itself doubts; Morgan's
  2025 sheet gives 0.14/0.16 against the library's 0.12/0.14 W/(m·K). That error is in the unsafe
  direction.
- **There is no `notebooks/validation/`**, which ADR 0009 calls for. Several tests re-derive the
  code's own formula, so they can't fail:
  - `test_radiation_coefficient`;
  - the catenary thrust test;
  - `test_chimney_follows_the_rule`;
  - the conductivity-law test, which checks one of its own fitting points.

## Heat and electric

No formula, constant or unit errors. These are correct:
- the element formulas;
- NEC 80%;
- the Churchill–Chu and Lloyd–Moran correlations;
- radiation in kelvin;
- the Kirchhoff k(T) wall solver;
- the Kanthal A-1 and Nikrothal tables;
- the Orton cone tables (all 78 values checked by script).

| # | Severity | Where | Finding | Fix |
|---|---|---|---|---|
| E1 | Major (safety) ✔ | `electric.py:269-281` | No check that the breaker isn't too big for the kiln (see Fix first 3). | Error when the breaker is above the next standard size over 1.5 × line current [S23]. |
| E2 | Major | `electric.py`, `thermal/surface.py`, `cones.py`, `ifb_conductivity.yaml` | Four of the missing research files are cited here. The data checked so far is right; its source is missing. `electric-and-thermal.md:326` says K-25 and K-26 k is "not found", which contradicts the data. | Commit the notes, or re-cite. |
| E3 | Major | `materials.yaml:19`, `ifb_conductivity.yaml:7` | JM 23 k is low (see above). Heat loss for a 4½ in JM 23 wall is 6.5–9% low. | Use Morgan's 2025 JM sheet; add JM 26's 1100 °C point. |
| E4 | Minor | `electric.py:50` | Wire down to 0.81 mm is allowed; Kanthal gives 2.0–5.0 mm for coils in grooves. Thinner wire gets only an info note. | Warn or refuse below 2.0 mm [S14]. |
| E5 | Minor | `electric.py:36` | The 17.5 W/in² limit is used for every alloy and temperature, though its source covers A-1 at about 2300 °F. Wall loading (35 kW/m²) isn't checked. | Note when outside the source; check wall loading. |
| E6 | Minor | `conductivity.py:42-52` | k(T) extrapolates linearly: Kaowool 8 pcf gives 0.014 W/(m·K) at 40 °C, below still air. Effect today is under about 1%. | Floor at the first point or at air. |
| E7 | Minor | `electric.py:333-349` | With power left blank, the elements draw exactly 0.8 × breaker when hot, so 1.5–4.8% more while cold. It's disclosed, but its source is the missing file. | Size against the cold Ct, or cite the makers' practice. |
| E8 | Minor | `hybrid.py:223-235` | The reduction warning fires without reduction, and always quotes A-1's 1050 °C. | Check `gas.reduction`; use the alloy's own limit (already loaded, unused). |
| E9 | Minor | `thermal/air.py:3-4` | The air table is Holman's, not Incropera's as claimed (under 2% on h_c). | Fix the citation. |
| E10 | Minor | `electric.py:39` | The coil pitch window is Kanthal's general 2–4 d, not the rule for grooves (minimum 2 d, or 2–3 d). | Use the groove rule. |
| E11 | Minor | heat-loss and element steps | Working is incomplete. Face steps omit the correlation, Ra, Nu, h_c and h_r. The ρ_T and R20 steps and two element formulas aren't shown. The hybrid's ceiling has no reference. | Add the steps. |
| E12 | Minor | `heatloss.py`, `shape.py:231` | Heat loss is conduction only: no door gap, spy holes or flue air. The floor is always a hot plate facing down, even on a slab. Neither caveat is stated. | State them. |

Test gaps:
- the hot-face-down correlation;
- three-phase delta per element;
- the Ct tables for D, AF and Nikrothal 80;
- an end-to-end element against Krueger's published 240 V, 24 A element;
- the breaker rule.

## Gas and combustion

These match their sources:
- Ward's BTU/ft³ table and all seven venturi burners' ratings;
- the power-burner basis;
- the 100 lb cylinder table;
- the propane properties;
- the NIST vapour pressures;
- Ward's chimney example (126 in);
- Olsen's 2.5 in²/ft³;
- the stack-effect constant;
- the λ algebra;
- Cantera's flame temperature (2,263 K).

| # | Severity | Where | Finding | Fix |
|---|---|---|---|---|
| G1 | Major | `gas.yaml:58-69` | The "⅓ full" tank table is D × L × 90, the 50%-full rule. At ⅓ full K ≈ 73, so 0 °F is 23% high. | Compute D × L × K for the assumed fill, or relabel. |
| G2 | Major | `gas.py:427-429` | The tank pressure ceiling uses VP(air). Under draw the liquid sits 20 °F colder, so below about 15 °F the engine allows pressures the tank can't hold. The −10 psi margin is unsourced. | VP(air − 20 °F) minus a sourced regulator margin; refuse below 5 psi. |
| G3 | Major | `gas.py:64-73, 295` | Burner input ignores wall thickness; the working even prints "9 in insulating brick" for a 2.5 in wall. | Refuse or warn when the wall's R differs materially from Ward's basis; print the real wall. |
| G4 | Major ✔ | `gas.py:110-123, 183` | A burner below its 5 psi rating is listed "at 5.0 psi" with the load as its output. `test_gas.py:89` asserts this. | Say "below 5 psi: orifice drilled for the load", or pick smaller burners. |
| G5 | Major | `gas.py:212, 357`, `gas.yaml:35-36` | The optimistic cylinder table is by liquid temperature (Propane Warehouse, under the table), but it's read by air temperature: 32% high at 20 °F air. | Offset for cooling under draw, or use it for information only. |
| G6 | Major | `gas.py:429, 459-462` | The 10 psi limit on cylinders has no source and no regulator margin. Two examples run at 9.7–9.8 psi. | Limit to the cylinder floor minus a sourced regulator drop, or say no sourced limit exists. |
| G7 | Major | `hardware.py:827-831`, `gas.py:173` | Over about 130 ft³ the build crashes (`min()` of an empty list). Over 8 burners, none are chosen and nothing says so. The research covers about 10–60 ft³. | Refuse outside the sourced range, with the reason. |
| G8 | Minor | `gas.py:500-529` | Ward's chimney rule is "for downdraft kilns only", but it's used for cross-draft. Rhodes adds 2 ft per ft of horizontal run, against Olsen's ⅓. The height datum is an assumption. | State the inference and the conflict; label the datum. |
| G9 | Minor | `gas.py:36, 537` | Altitude is ignored. At 1,600 m draft is about 18% lower; Norsker's 1% per 100 m is sourced but unused. | Add site elevation. |
| G10 | Minor | `gas.py:198` | The default is the fewest, cheapest burners: 1 × B5 for 45 ft³. Every sourced build uses several. | Prefer several burners; cite the precedent. |
| G11 | Minor | `gas.py:33-34`, `combustion.py:20-21` | Propane data disagree by about 1%. GREET's figures are its LPG row, not propane. | Use one consistent propane set. |
| G12 | Minor | `gas.py`, `hardware.py:783, 835` | Some steps lack references and inputs. Results travel as formatted imperial strings that hardware parses back (ADR 0004), even for metric designs. | Return quantities. |
| G13 | Minor | `gas.yaml:21-22` | Ward's prices have moved: B4 $325, B5 $445. | Update with a date. |

Test gaps:
- a published end-to-end chimney case run through `design_gas`;
- the tank and cylinder pressure ceilings;
- wall thickness;
- the large-kiln refusal;
- available heat against a published chart.

**Top-down notes** (judged as engineering estimates; most numbers recalculated and confirmed):
- **T1.** Design A's 310 stainless port tubes sit at 1,220–1,300 °C, above the notes' own 1,035 °C
  limit for 310. Its 30% turndown is the burn-back regime warned of elsewhere. It is marked
  superseded.
- **T2.** Relighting a lost flame uses propane's autoignition range (500–600 °C). NFPA 86, as
  reported, uses 760 °C.
- **T3.** `low_pressure.py:71` models a 1.5 in port, but design B specifies 1¼ in, so the
  secondary-air gap is 45% smaller than modelled.
- **T4.** "70,000 Btu/h (12 kW)" should be 20.5 kW. The slip is in Bloom's text; flag it rather
  than repeat it.
- **T5.** The chimney-suction table rests on an assumed friction and gas temperature. Mark it
  "(model)".

## Structure and masonry

These match their sources:
- HarbisonWalker's H/W and heated-factor tables (all 73 cells, to 4%);
- the 12,000 psi rod stress;
- the tie-rod stress areas;
- the angle properties;
- the arch geometry formulas;
- the arch-brick taper counts (they reproduce Pitelka's counts);
- the catenary H = w·a;
- the sail-dome geometry.

| # | Severity | Where | Finding | Fix |
|---|---|---|---|---|
| S1 | Critical ✔ | `model.py:87-91`, `frame.py:443-445` | A door or car in a springing wall (see Fix first 1); the dome too. | Refuse it, as the catenary does, or design a lintel carrying the skewback, checked for vertical load and thrust together. |
| S2 | Major | `frame.py:196, 391, 422-437` | HW's rise and thickness rules aren't enforced; the 5.34 factor cap is inferred. A 0.5 in/ft arch passes; a 1.6 in/ft arch that HW's rule passes is refused. The examples sit below HW's 2–3 in/ft for IFB. | Enforce HW's ranges and the thickness limit as sourced errors; keep 5.34 only as a guard. |
| S3 | Major | `frame.py:184, 214-217` | The hot-thrust theory cites the missing `arch-thrust-theory.md`. Steel is sized past the sourced T/S ≤ 10% with only a note; every sprung example is at 10.7%. The physics is sound. | Write the note (Heyman; McDowell 1939), and record the extrapolation in an ADR or warn. |
| S4 | Major | `frame.py:160-161` | Insulation over the arch counts as arch ring. This refuses Pitelka's documented soda kiln (factor 17.5 against 2.44 for the brick ring), while still sizing steel from cold thrust. | Mark the structural layers; show no steel when the hot check fails. |
| S5 | Major | `frame.py:139`, `geometry.py:318, 460` | HW: the thrust line should pass through the steel's corner. In gas-crossdraft it leaves the wall 2.9 in below it, and that wall is the door. | Put the buttress at the solid ring's outer corner and check the rule. |
| S6 | Major | `geometry.py:464-466` | An arch ring wider than the walls is silently cut to a sliver of skewback, with the steel drawn inside the ring. | Error. |
| S7 | Major | `frame.py:564-601` | The flat-roof frame is attributed to Merrill, but Merrill threaded rods through every roof brick. | Model it as built, or drop the attribution. |
| S8 | Major (bill) | `frame.py:524-529, 575-581` | The bottom cross-members and the roof angle are counted twice: 41.3 ft of flat bar for about 20.7 ft. | Count the perimeter once. |
| S9 | Minor | `shape.py:35, 39`, `frame.py:193` | Rise 0 or a fibre-only roof crashes with ZeroDivisionError. Rise ≥ S/2 isn't refused, and its geometry is wrong. | A validator like the dome's, and require a solid roof layer. |
| S10 | Minor | buttress working | It doesn't say the geometric-axis Sx is used rather than the principal axis. Still safe at about 16.5 ksi. | Say so. |
| S11 | Minor | `masonry.py:555-557` | "A 60° skewback is the usual choice" is printed for every arch, but the skew must match the central angle (48° at 2.3 in/ft). | Print 90° − θ/2. |
| S12 | Minor | `masonry.py:126-129` | HW: never a stretcher course just below the skewback. 4½ in walls are all stretchers. | Surface the rule. |
| S13 | Minor | catenary thrust | Weight is taken per unit of inside arc, so thrust is about 7% low. | Integrate over the ring. |
| S14 | Minor | various | Brick counts carry no working; kerf and waste are unsourced. The flat-roof spy-hole rule adapts S13's "below the arch's peak". The rod error has no reference. | Add the working and references. |

Test gaps:
- `arch_ring` (it does reproduce Pitelka);
- HW's own worked example: 12 ft span, 13½ in, which the engine matches to 2.3%;
- a side-wall door;
- rise 0;
- a fibre-only arch;
- the 1–3 in/ft range.

## Materials, castables and costs

These match their sources:
- the Morgan K and JM 2025 sheets (except JM 23);
- Kaowool;
- Kast-O-Lite 26 and 30 LI Plus;
- Mizzou;
- Mizzou's dry-out for single layers up to 9 in;
- the steam constants;
- the burnout stoichiometry;
- kyanite's volume growth;
- the conversions, batch rounding and dated, sourced prices.

| # | Severity | Where | Finding | Fix |
|---|---|---|---|---|
| M1 | Critical | `castable.py:826-864`, `report.py:72-78` | The burnout check sees each mix alone and compares it with installed power (see Fix first 2). | Sum the mixes; compare with the heat the schedule needs; refuse or warn. |
| M2 | Major | `castable.py:365-409` | The conductivity law is fitted to firebricks but applied to castables. Against Morgan's Kaolite and Firelite castables in its density range it is −21% to +49% out, yet results quote "up to about 21%". | Validate on held-out castables, or fit to them, and quote that error. |
| M3 | Major | `castable.py:269-271, 346` | Firing shrinkage defaults to 0 with no finding, so density and k come out low, the unsafe direction: 5% shrinkage means k +19%. | Refuse without a measured shrinkage, or warn that density and k are lower bounds. |
| M4 | Major | `castable.py:606-621, 894-959` | A dry-out schedule is given for stacked cast linings (2 + 9 in in the example). HWI says multi-component linings need case-by-case evaluation. A 10 in single layer is already refused. | Treat stacked castables like the over-9 in case. |
| M5 | Major | `ingredients.yaml`, `castable.py` | The cited `castables.md` and `castables-minerals.md` are missing (see above). | Commit them, or re-cite. |
| M6 | Major | `ingredients.yaml:14, 140-148`, `castable.py:236-239` | A lightweight aggregate needs its particle (envelope) density. The message says "the maker's sheet" (loose bulk), and the test uses perlite's skeletal 2.3 g/cm³, which shrinks its volume about tenfold. | Ask for particle density by name; fix the test value. |
| M7 | Major | `materials.yaml:11-21` | JM 23 k (see above). | Use the 2025 sheet. |
| M8 | Minor | `masonry.py:596-608` | Bags are counted from dried density, not the maker's "material required": 4–10% over before waste. | Add `material_required`. |
| M9 | Minor | `conductivity.py:47-52` | k(T) below the first point (as E6). | As E6. |
| M10 | Minor | `model.py:415` | `Measured.fired_to` is never read; a test piece fired below the kiln's top temperature passes. | Warn. |
| M11 | Minor | `castable.py:274` | Porosity ignores a measured fired density. | Use 1 − ρ_fired/ρ_skeletal. |
| M12 | Minor | `ingredients.yaml:68-69` | Ciment Fondu's limit is its neat-paste PCE, a softening point, not a use limit. | Find a service limit, or say what it is. |
| M13 | Minor | `castable.py:260-261, 315` | Foam is treated as pure air, so the "quart weighs" target reads light. | Source a foam density, or say so. |
| M14 | Minor | `cli/.../main.py:139-143` | A `CastableError` reaches the CLI user as a traceback. | Catch it like `UnknownEntryError`. |
| M15 | Minor | research docs | Housekeeping. Kast-O-Lite 30 and Mizzou k are "not found" in one note but given in another. Four products can move from "excerpt" to "verified". Mizzou's water is 9.0% hand-cast (HWI 12/12), not 9.5%. | Reconcile. |

Test gaps:
- a held-out castable set for the conductivity law;
- BOM rounding beyond the total;
- a cutting allowance for curved and dome brick.

## Bugs found while raising test coverage

Coverage went from 93% to 99.7% (branch). Writing those tests turned these up. None was fixed,
so the tests pin today's behaviour or skip it.

| Where | Bug |
|---|---|
| `electric.py:291` | The "Wire resistivity when hot" step shows 1.511e-06 Ω·mm²/m, not 1.511. ρ_T is in Ω·m but labelled Ω·mm²/m. It's baked into the golden reports. `test_the_hot_resistivity_step_is_in_ohm_mm2_per_m` is a strict xfail and will start failing when this is fixed; remove the mark then. |
| `hardware.py:388-397`, `frame.py:609-616` | An electric kiln whose door isn't in the front wall gets a case with no front plate. The member list assumes a front door. |
| `castable.py:712-716` against `802-876` | A layer whose organics never reach 240 °C is said never to burn out, but its organics still count in the first-firing burnout steps and can raise the runaway warning. |
| `castable.py:610` | The dry-out schedule mentions organics if any listed mix has them, even one the lining doesn't use. |
| `gas.py:451` | When no named burner fits (e.g. a tank at −20 °F leaving 0.7 psi), the burners are None and no finding says why. |
| `hybrid.py:182, 236` | When propane is cheaper at every temperature, no step or finding says so; the opposite case gets both. |
| `api/.../routes.py:43-77` | The API saves a design with an unknown alloy (and, probably, an unknown burner model); it only fails at build time. |
| `cli/.../main.py:121-123` | `compare` sizes columns from the design names, so long cells run together ("$2,750 + unpriced items$10,386 …"). Row order depends on which design is first. |
| `masonry.py:310-311, 335-340` | "and 1 straights". The ring count rounds shaped and straight bricks up separately, so a ring can come out one straight over what closes it. |
| `web/.../NewDesign.tsx:22-28`, `DesignEditor.tsx:69` | Opening a design file that fails the check leaves an empty placeholder document. The Choices tab then shows a blank form, and "Save and build" from there sends the placeholder, not the file. |
| `web/.../DesignForm.tsx:62` | A value in a unit the field doesn't list (`1 m`) shows with the first unit ("in"), and editing it writes `1.2 in`, silently changing the dimension. |
| `web/.../BuildPanel.tsx:84` | A finished build without `report.json` says "Loading the report…" forever: a disabled query counts as pending in TanStack Query v5. |
| `web/.../Castables.tsx:138` | "Working (1 steps)". |

Dead code:
- `GeometryNotSupportedError` (`geometry.py:214`) is never raised. So `build.py:76, 86`,
  `report.py:90`, `BuildResult.notes` and the CLI's handling of notes and of a missing bill
  never run.
- `routes.py:57-58` and the CLI's `UnitError`: pydantic always wraps it in `ValidationError`.
- `drawings.py:89, 121-122`.
- `masonry.py:249-250, 454->459, 498->437`.
- `surface.py:60->exit`.
- `model.py:479->484`.
- `hardware.py:352->341`.
- `Piece.volume`.

## Not checked

- **Brick crushing at arch hinges, buttress deflection, and hot steel strength:** no source in
  `docs/`.
- **Pages that couldn't be fetched:**
  - Krueger's 17.5 W/in² page;
  - a primary PCE chart for cones 15–42;
  - the JM 23 2011 sheet;
  - the conservative 100 lb cylinder table;
  - Flame Engineering;
  - the RegO and Emerson handbooks;
  - NFPA 54/58/86 text;
  - KX-99 and Promasil-1100;
  - HWI Dryout Schedules 2 and 4;
  - the Ciment Fondu sheet.
- **Ingredient densities and LOIs:** their cited source is missing.
- **ASTM C182 and C201 mean-temperature k:** whether these should be converted to local k(T)
  before integration. C680 is paywalled. Using them directly is conservative for fibre.
