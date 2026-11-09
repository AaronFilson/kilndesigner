# Physics review, part 1: heat and fuel (step E)

Date: 2026-11-09. Scope: step E of `docs/planning/11-09-26.md`, the heat-and-fuel half. Arch and dome
statics, castables and the structural checks are part 2. This review builds on
`docs/research/energyplus-review.md` (cited here as EP §n), `docs/research/heat-libraries.md`
(HL) and `docs/research/firebox-efficiency.md` (FE), and does not repeat them. **No engine
changes were made.**

Labels: **fix now** means sourced, small and clear, with the formula, source and tests given.
**Proposed** means it needs more work or data first. **Keep** means our method is fine.

## How the numbers were measured

`scratch/e1/compare.py` loads `examples/gas-crossdraft.yaml` and
`examples/pnw-hybrid-crossdraft.yaml`, runs `heat_loss`, `design_gas` and `simulate`, and swaps
in each alternative by monkeypatching for that run only. Both kilns stand on a stand, so the
floor's underside is a hot plate facing down. The gas cross-draft has no setting or ware. The
hybrid has a 16-shelf setting with ware at 7 × its weight. The baselines:

| Kiln | Firing time | Fuel | Electricity | Into the kiln | Into the ware | Cost |
|---|---|---|---|---|---|---|
| gas-crossdraft | 4.12 h | 387 kWh | – | 165 kWh | 0 | $50.47 |
| pnw-hybrid-crossdraft | 65.2 h | 501 kWh | 705 kWh | 900 kWh | 337 kWh | $150.03 |

## Ranked findings

Ranked by how much a user's number moves.

| # | Finding | Mark | Effect on the examples |
|---|---|---|---|
| 1 | Ware and setting c_p held at the room-temperature 800 J/(kg·K) | **fix now** | hybrid: +12 % energy, +13 % cost, +8.3 h; nothing for a kiln with no ware |
| 2 | Flue gas assumed to leave at the chamber's temperature (no gas-to-ware/wall heat transfer) | proposed | gas kiln: +8 / +18 / +35 % fuel for flue gas 50 / 100 / 150 K hotter than the chamber; hybrid +7 / +17 / +30 % on its propane |
| 3 | Excess air fixed at 3 % O₂ through the whole firing (λ 1.15) | proposed | gas kiln +1 % (λ 1.5) to +5 % (λ 2.0) fuel below 800 °C; also moves the hybrid's cost crossover |
| 4 | Chimney draft without friction or entry/exit losses | proposed | net draft 81–87 % (gas) and 92–95 % (hybrid) of the stack figure shown |
| 5 | Ground-contact floor: steady disk, S = 2D, adiabatic ground surface | proposed (EP §5 #2) | not in these examples; engine's own note gives about 2× floor loss at 12 h |
| 6 | Radiation between faces and the ware lag (lumped chamber) | proposed (EP §4 #1) | small on total fuel; larger on floor and ware temperatures |
| 7 | Hot face down: McAdams 0.27 Ra^¼ against Schulenberg/Jaffer | **fix now** | total loss −0.09 %; floor shell temperature +16 °F (234 → 251 °F) |
| 8 | Element power held at its hot value from cold | keep (note) | cold power +4 % (A-1/APM), +6 % (AF); faster only in the first hours |
| 9 | Natural gas as pure methane | keep | available heat at the top 0.304 (NG) vs 0.330 (propane); per-therm pricing exact |
| 10 | No inside film (hot face at the chamber's temperature) | keep | radiative h at 1000 °C ≈ 370 W/(m²·K) against about 1 W/(m²·K) for the lining: < 0.3 % |
| 11 | Steady layered walls, k(T), C680-style iteration; vertical Churchill–Chu; hot face up Lloyd–Moran | keep (EP §3, HL) | – |
| 12 | Available heat from Cantera equilibrium (ADR 0012) | keep | – |
| 13 | Burner sizing (Olsen Rule 1 plus "holds top" check) | keep (note) | – |
| 14 | Propane vaporisation from cylinders and tanks (tables, liquid 20 °F under the air) | keep | – |
| 15 | Kanthal surface loads, resistance at temperature | keep | – |
| 16 | Olsen's chimney height and section rules for wood | keep, with #4 | – |
| 17 | Wood per firing, m = Q ÷ (η·H(w)) | keep; F stays proposed | scales as 1/η (FE) |
| 18 | Hybrid switch-over cost per useful kWh | keep the method; inherits #2, #3 | – |

---

## 1. Ware and setting heat capacity: **fix now**

**Ours.** `simulation.py` lumps the setting and the ware into one capacity, `ware_kg × WARE_CP`.
`WARE_CP` = 800 J/(kg·K), Lienhard Table A.2, fired-clay brick at 24 °C (masonry-materials.md §1.1
[M1]). The capacity is held constant from room temperature to cone 10.

**Standard practice.** Fireclay c_p rises with temperature. The library already carries VDI Heat
Atlas fireclay c_p(T) for the dense firebricks, verified, [M2] via `ht`: 956–958 J/(kg·K) at
400 °C, 1021–1024 at 800 °C, 1037–1040 at 1000 °C, 1054–1058 at 1200 °C (`materials.yaml`,
`firebrick-medium-duty-smithfield`). Every wall layer already uses c_p(T). Only the ware does not.

**Where it goes wrong.** In every firing with a setting or ware, the ware's energy is too low by
the mean-c_p ratio. From 10 °C to 1285 °C, Lienhard's 800 at 24 °C and VDI's points (linear between
them, held at 1058 above 1200) give a mean of about 980 J/(kg·K), 22 % above 800.

**Effect (measured).** pnw-hybrid-crossdraft with WARE_CP = 980: energy 900 → 1018 kWh (+13 %), ware
337 → 413 kWh, electricity 705 → 795 kWh, propane 501 → 572 kWh, time 65.2 → 73.5 h, cost $150.03
→ $170.11 (+13 %). This is the largest sourced change in this review, and wood per firing
(`wood.py`) inherits it.

**The fix.** Give the ware a `HeatCapacity` curve and integrate its enthalpy rather than m·c·ΔT:

- c_p(T) = 800 J/(kg·K) at 24 °C [M1], then the VDI fireclay points [M2] (400 → 956, 600 → 997,
  800 → 1021, 1000 → 1037, 1200 → 1054), linear between them and held at the end values, as
  `HeatCapacity` already does for wall layers;
- step 2 of the simulation: D(T) = Σ faces + m·[H(T) − H(T_c)], with H(T) = ∫c_p dT. This is still
  monotone in T, so the root-find is unchanged. Alternatively, keep the step linear with c_p
  evaluated at the step's start (lagged), as for the walls (METHOD);
- shelves: if the setting gives `material: mullite` and no mullite c_p is sourced in
  `docs/research/`, use the fireclay curve and say so in the working, or ask for one. Don't invent
  one.

**Tests.**
1. Unit: `ware_enthalpy(10 °C → 1285 °C)` per kg equals the trapezoid of the points above to 0.1 %.
2. A lumped-only case (zero-thickness faces or a FixedSurface 0): energy into the ware equals
   m·∫c_p dT to 0.5 %.
3. Regression: pnw-hybrid-crossdraft's `ware_kwh` rises by 20–25 % (337 → about 413 kWh); update the
   golden reports with a note.
4. A kiln with no ware (gas-crossdraft) is unchanged to the kWh.

Not counted, and not found in `docs/research/`: the heat of green ware's dehydroxylation and
residual water. Leave it out and say so in the working ("bisque or glaze firing; raw ware takes
more").

## 2. Flue gas leaves at the chamber's temperature: **proposed**

**Ours.** Available heat (Cantera, ADR 0012) is taken with the products at the chamber's
temperature, T_flue = T_c. The hot face is also at T_c, so gas-to-surface heat transfer is
implicitly infinite.

**Standard practice.** In furnace design the combustion gases leave hotter than the load. Hottel's
well-stirred-furnace model takes the exit gas at the gas temperature, set by the balance of
radiation and convection from gas to sink: Q = σ·A·F·(T_g⁴ − T_s⁴) + h·A·(T_g − T_s), with gas
emissivity from CO₂/H₂O (Hottel & Sarofim 1967, ch. 14). No open copy was found in this pass. A
1977 open abstract (Combust. Sci. Technol., doi 10.1080/00102207708946826) gives the method's chart
form only.

**Where it goes wrong.** At the end of a fast firing, when the gas has little time and little area
to give up its heat, and in short cross-draft paths. The error is always the same way: we
under-state the fuel.

**Effect (measured).** Exit gas 50 / 100 / 150 K above the chamber: gas-crossdraft fuel 387 → 418 /
457 / 521 kWh (+8 / +18 / +35 %), time 4.12 → 4.40 / 4.75 / 5.38 h; hybrid propane 501 → 538 / 586 /
652 kWh. At 1285 °C, λ 1.15, available heat falls from 0.330 to 0.277 for 100 K. That is the
biggest single uncertainty in a gas kiln's fuel figure.

**What's needed.** A gas emissivity method (Hottel charts or Leckner 1972's correlation, which is
open in some university theses) recorded in `docs/research/`, mean beam length 3.6 V/A, and one
measured flue-gas temperature from a kiln of known setting to check it. Until then, show the
sensitivity in the working: "if the gas leaves 100 K hotter than the ware, the fuel is ~18 % more."

## 3. Excess air fixed through the firing: **proposed**

**Ours.** λ for 3 % O₂ (oxidation, λ = 1.15 for propane) or 0.9 (reduction) at every temperature.

**Practice.** Natural-draft venturi kilns at low fire draw far more secondary air than they burn
(the draft is set for full fire). Available heat falls steeply with λ: at 600 °C, 0.674 (λ 1.15),
0.608 (1.5), 0.513 (2.0); at 1000 °C, 0.478 / 0.362 / 0.194.

**Effect (measured).** gas-crossdraft with λ 1.5 / 2.0 below 800 °C: fuel +1 % / +5 %. The
hybrid's propane is lit only above 900 °C, so it is unchanged. The hybrid's cost chart (#18),
however, uses the same λ at every temperature, so its crossover would move to a higher
temperature.

**What's needed.** A measured O₂ at the flue through a firing (FE §6 asks the same). No open
source with low-fire λ for kilns was found. Keep the user's λ as an input later.

## 4. Chimney draft without losses: **proposed**

**Ours.** `gas.py` and `fire.py` report the theoretical stack draft ΔP = 0.0342·a·h·(1/T_o − 1/T_i)
[S42]. Against the density form g·h·(ρ_a − ρ_g) with a flue-gas molar mass of 28.5 g/mol, this
agrees to 1 %.

**Practice (pressure balance).** Available draft = stack draft − friction − local losses: ΔP_net =
g·h·(ρ_a − ρ_g) − [f·h/D_h + ΣK]·½ρ_g·v², with f from Moody (1944) and K for entry (0.5) and exit
(1.0) (Idelchik, *Handbook of Hydraulic Resistance*, AEC-tr-6630, 1966, an open US AEC translation;
fetch it and record the pages before use). EN 13384-1 does the same with its own coefficients,
but it is not open.

**Effect (measured, at full fire, with the exit flue as the section).**

| Kiln | Flue gas | Stack | Friction | Entry + exit | Net |
|---|---|---|---|---|---|
| gas-crossdraft, 57 in², 1.24 m | 538 °C | 9.9 Pa | 0.17 | 1.12 | 8.6 Pa (87 %) |
| | 1285 °C | 12.4 Pa | 0.25 | 2.15 | 10.0 Pa (81 %) |
| pnw-hybrid, 113 in², 1.34 m | 538 °C | 10.7 Pa | 0.06 | 0.52 | 10.1 Pa (95 %) |
| | 1285 °C | 13.4 Pa | 0.09 | 1.00 | 12.3 Pa (92 %) |

Friction is negligible in short gas chimneys. The velocity heads matter, and Re ≈ 3000–4300
(transitional) makes f uncertain. For gas kilns this changes a displayed line, not a decision:
the burners drive the flow (Olsen p.151). For wood kilns the real loss is through the grate, the
setting and the flues. That resistance is not sourced, which is why Olsen's empirical Rule 5 stays
the sizing rule (#16).

**Proposed change.** Add a "net draft at full fire" line beside the stack figure once Idelchik's
pages are in `docs/research/structure-and-draft.md`. Tests: the stack term against the density
form (1 %); friction against a hand Darcy–Weisbach case.

## 5. Ground-contact floors: **proposed** (EP §5 item 2)

**Ours.** h = 8k/(πD), k = 1.0 W/(m·K): Incropera Table 4.1 case 10, an isothermal disk on a
semi-infinite medium whose surface elsewhere is adiabatic, at steady state.

**Where it goes wrong.** (a) Transient: in a 12–60 h firing the soil never reaches steady state.
The semi-infinite transient q = kΔT/√(παt) gives h ≈ 3.8 W/(m²·K) at 12 h (α 5×10⁻⁷ m²/s) against
the steady 1.7 for a 1.5 m disk. That is the "about twice at 12 hours" already in the finding.
(b) Boundary: the real ground surface around the kiln loses heat to the air, which steepens the
edge gradient and raises the loss beyond S = 2D. (c) Wet soil: k 1.5–2.5 and latent heat.
Direction: we under-state the floor loss.

**What's needed.** The Kiva-style 2D transient model (EP §5) and the GC10a reference numbers
(blocked; see the plan's "For the user later"). Neither example is on the ground, so no number
was measured here.

## 6. Radiation exchange and ware lag: **proposed** (EP §4 item 1)

Unchanged from EP §4. The lumped chamber puts the ware at T_c with no lag. That over-counts ware
heat at the end of a fast ramp (it would lag) and gives no floor or door cold spots. The effect on
total fuel is small; the effect on cone evenness can't be shown today. Do #1 first. ScriptF needs
the ware node's c_p(T) from #1.

## 7. Hot face down: **fix now**, settled from open sources

**Ours.** Nu = 0.27 Ra^¼, L = A/P (McAdams), Ra 10⁵–10¹⁰.

**Open primary sources found.** A. Jaffer, "Natural Convection Heat Transfer from an Isothermal
Plate", *Thermo* 3(1) 148–175 (2023), doi 10.3390/thermo3010010, CC BY 4.0. Open preprint:
arXiv:2201.02612v5, read in full for this review. It re-fits four published downward-facing data
sets (Fujii & Imura 1972, water, Pr 5, 10⁷ < Ra < 10¹²; Aihara et al. 1972, air, 25 × 35 cm;
Faw & Dullforce 1982, air, 18.1 cm disk; Goldstein & Lau 1983, Pr 2.5) and corrects Schulenberg's
(1985, IJHMT) strip formula:

- Schulenberg, corrected (Jaffer eq. 4): Nu = 0.544·Ra^⅕ / [1 + (0.477/Pr)^⅗]^⅓, L = half the
  shorter side;
- Jaffer eq. 56: **Nu_R = 0.341 + 0.550·(Ra/Ξ(Pr))^⅕**, Ξ(Pr) = [1 + (0.5/Pr)^p]^(1/p),
  p = √(1/3), with **L_R = half the shorter side** of a rectangle (the harmonic-mean length,
  eq. 57; for a disk use eq. 57's disk form). RMSRE against the four data sets: 2.7 %, 4.2 %, 3.8 %,
  3.7 % (Table 6). Stated span: 10⁶ < Ra < 10¹².

The other papers named in the plan (Fujii & Imura 1972, Hatfield & Edwards 1981, Restrepo &
Glicksman 1974, Kitamura et al.) are paywalled in IJHMT/JFM, with no open copy found. Fujii &
Imura's and Aihara's data reach us through Jaffer's fit. Raithby & Hollands' chapter: no open copy
found (HL used a secondary form).

**Verdict.** There is now an open source with a validity range that covers a kiln floor (L_R ≈
0.53 m, ΔT 60–110 K, Ra ≈ 10⁸–10⁹, Pr 0.7). So McAdams can be retired. The two Schulenberg forms
and the R–H form agree within 0.1 % on the total.

**Effect (measured).** Total loss −0.08 to −0.09 % (gas 11,728 → 11,717 W; hybrid 14,314 →
14,301 W). The floor's outside rises 234 → 251 °F (gas) and 237 → 253 °F (hybrid): convection
falls by about half, and radiation, which dominates this face, takes up the rest. The visible
change is the floor's shell temperature, which is the touch and clearance figure under a kiln on
a stand.

**The fix.** In `thermal/surface.py`:
- `facing_down`: Nu = 0.341 + 0.550·(Ra/Ξ)^⅕, Ξ = (1 + (0.5/Pr)^0.57735)^1.73205, L = half the
  shorter side. `shape.characteristic_length` must give L_R for a floor (the rectangle's short
  side ÷ 2; a round floor uses the disk form of eq. 57), not A/P;
- `RA_RANGE["facing_down"] = (1e6, 1e12)`; RA_SOURCE adds Jaffer 2023 Table 6;
- `docs/research/thermal-properties.md` §5: record the formula, the data sets and the RMSRE.

**Tests.**
1. At Pr = 0.71, Ra = 10⁸: Ξ = 2.81, Nu = 0.341 + 0.550·(3.56×10⁷)^0.2 = 18.15 (± 0.05).
2. Large-Pr limit: Ξ → 1, Nu → 0.341 + 0.550 Ra^⅕ (eq. 46).
3. Jaffer Table 6 reproduction: the Aihara 25 × 35 cm air points within 5 %, where the data can be
   transcribed from the paper's Figure 7. Otherwise check eq. 4 against eq. 56 within 10 % for
   Ra 10⁶–10¹².
4. Regression: gas-crossdraft total within −0.2 % of today's; the floor surface rises 10–25 °F.
5. A floor of L_R outside 10⁶–10¹² raises the existing Ra finding.

## 8. Elements: power held at its hot value: **keep** (note)

`electric.py` designs at R_T = U²/P with Ct at the kiln's temperature plus 100 °C (the wire runs
hotter). The simulation then holds that power from cold. With the library's Ct, cold power is
1.04× (A-1, APM) to 1.06× (AF) the hot design power. That speeds only the first hours of a
firing, and total energy is unchanged. A one-line improvement, P(T) = P_design·Ct(T_design)/Ct(T),
is sourced (Kanthal Ct tables, [S9]) and could be done with #1. It is too small to rank higher.
Surface loads: Olsen 9 W/in² preferred, Krueger 17.5 W/in² the limit. Kanthal's key data gives 3–4
W/cm² (19–26 W/in²) at 1000 °C for spirals in grooves, and asks for ~20 % less under on/off
control. Krueger's figure sits inside that. Kanthal's temperature diagrams remain image-only
(electric-and-thermal.md §2). Keep.

## 9. Natural gas as methane: **keep**

Per-therm prices convert exactly. Per-ft³ prices go through 1000 BTU/ft³ and are already flagged.
Real pipeline gas (a few % ethane, N₂, CO₂) changes available heat by much less than #2 or #3. Not
worth a composition input.

## 10. No inside film: **keep**

At kiln temperatures the inside surface exchange is radiative. 4εσT³ at 1000 °C, ε 0.8, is about
370 W/(m²·K) against a lining conductance of about 1 W/(m²·K), so leaving it out changes the loss by
< 0.3 %. The real missing piece is #2 (the gas's temperature), not a film at the wall.

## 11–12. Steady walls, outside convection, combustion: **keep**

Already reviewed (EP §2–3, HL). Churchill–Chu (vertical) and Lloyd–Moran (hot face up) are within
their ranges. HL's VDI-vs-Lloyd–Moran spread (~35 %) on the roof stays as a quoted uncertainty.
Cantera/GRI-Mech equilibrium available heat is the standard method. Its max is LHV/HHV, as it
should be. The Picard update in `TransientWall` (EP §7 #4) stays proposed.

## 13. Burner sizing: **keep** (note)

Olsen's Rule 1 BTU/ft³ plus the physical check η(T_top)·P ≥ steady loss is sound. Note: the check
uses the steady loss only. The final ramp also stores heat in walls and ware, which the
simulation (not this check) already accounts for. With #1 and #2 the check gets stricter.

## 14. Propane vaporisation: **keep**

Cylinder and tank tables [S3, S10, S11, S13], read at the liquid 20 °F under the air under
continuous draw [S1]. The physics, Q = U·A_wetted·(T_air − T_liquid), is the same rule the tables
encode (D × L × K). No open source gives a better general model for a manifold of 100 lb
cylinders. Frost and wind change it more than any formula would.

## 16. Olsen's chimney rules for wood: **keep**

Rule 5 (3 ft per ft of downward pull + 1 ft per 3 ft horizontal) and the 7 : 1 grate-to-chimney
section are empirical and include the setting's resistance, which no open source quantifies for a
kiln. A pressure balance (#4) can't size a wood chimney without that resistance. Keep the rules,
add the net-draft line, and record a measured draft (in. w.c. at the damper) if the user can take
one.

## 17. Wood per firing: **keep**

m = Q ÷ (η·H(w)), with H(w) from FAO UBET eq. 3. The method is right. The answer is set by the
user's η (FE: measured 12–28 %). Firing-step flue loss (plan step F) stays proposed until Pettersen
(1984) and a weighed firing are in hand. Q inherits #1 (+13 % on a kiln with ware).

## 18. Hybrid switch-over: **keep the method**

Cost per useful kWh = price ÷ (kWh per gallon × available heat at T) is right. Its numbers inherit
#2 and #3, both of which push gas's real cost up at low temperature, so the true economic hand-over
is higher than the chart shows. The pnw example's hand-over is set by the glaze (1650 °F), not the
chart, so its numbers don't change.

## Fix-now summary

| Fix | Formula | Source | Tests |
|---|---|---|---|
| Ware c_p(T) | H(T) = ∫c_p dT: 800 @ 24 °C, then 956/997/1021/1037/1054 @ 400–1200 °C | Lienhard Table A.2 [M1]; VDI Heat Atlas fireclay [M2] (already in `materials.yaml`) | enthalpy integral; lumped energy; hybrid ware_kwh +20–25 %; no-ware kiln unchanged |
| Hot face down | Nu = 0.341 + 0.550(Ra/Ξ)^⅕, Ξ = (1 + (0.5/Pr)^√⅓)^√3, L = ½ short side, Ra 10⁶–10¹² | Jaffer, *Thermo* 3 (2023) 148–175, eq. 56–57, Table 6; data Fujii & Imura 1972, Aihara 1972, Faw & Dullforce 1982 | Nu = 18.15 at Ra 10⁸, Pr 0.71; large-Pr limit; total −0.2 % to 0; floor Ts +10–25 °F |

## Sources found, and not found

- Found, open: Jaffer 2023 / arXiv:2201.02612v5 (read). Idelchik AEC-tr-6630 (an open US government
  translation; pages still to record). Moody 1944 (public).
- Not found as open copies: Raithby & Hollands (Handbook chapter), Fujii & Imura 1972, Hatfield &
  Edwards 1981, Restrepo & Glicksman 1974, Kitamura et al. 2015, Hottel & Sarofim 1967, Schulenberg
  1985, EN 13384-1, ASTM C1340, low-fire λ for venturi kilns, a mullite c_p(T), the heat of
  dehydroxylation for green ware.

Comparison script: `scratch/e1/compare.py` (not committed; scratch is ignored).
