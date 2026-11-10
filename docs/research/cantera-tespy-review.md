# Cantera beyond available heat, and TESPy

Reviewed 2026-11-09 for what they could add to kilndesigner's combustion, flue and firing
calculations. No engine changes were made. Probe scripts (scratch is git-ignored, so their
output is copied into the tables below):

- `scratch/cantera-tespy/cantera_probe.py`, `wood_reduction.py`, `lhv_basis.py`: run with
  `uv run python scratch/cantera-tespy/<name>.py` in the repo's environment;
- `scratch/cantera-tespy/tespy_probe.py`: run in a throwaway virtual environment outside the
  repo (Python 3.14.10, TESPy 0.11.3), not the repo's `.venv`.

| Library | Version read | Where | Licence |
|---|---|---|---|
| Cantera | 3.2.0, the version in `uv.lock`, released 2025-11-18 | https://cantera.org; source read at tag v3.2.0 on GitHub (`src/oneD/Flow1D.cpp`, `include/cantera/oneD/Flow1D.h`, `src/transport/GasTransport.cpp`); installed `.venv/lib/python3.14/site-packages/cantera/` | BSD-3-Clause |
| TESPy (Francesco Witte et al.) | 0.11.3, PyPI 2026-10-15 | https://github.com/oemof/tespy; installed in the throwaway venv; paper: Witte & Tuschy, "TESPy: Thermal Engineering Systems in Python", JOSS 5(49) 2178 (2020) | MIT (`LICENSE`; `SPDX-License-Identifier: MIT` in each module) |
| CoolProp (TESPy's property back end) | 8.0.0 | PyPI | MIT |

Both licences allow use with the notice kept. As with ht (heat-libraries.md), neither library is a
source of engineering data in itself: every coefficient it carries is usable only through the
primary source behind it, recorded in `docs/research/`.

## 1. What we use of Cantera today

`core/src/kilndesigner/combustion.py` (ADR 0012): `ct.Solution("gri30.yaml")`,
`set_equivalence_ratio`, `equilibrate("TP")` and `equilibrate("HP")`, `enthalpy_mass`. That is,
GRI-Mech 3.0's **thermodynamic data only** (NASA 7-coefficient polynomials), never its kinetics or
transport. `simulation.py` caches available heat per whole kelvin. Nothing else in the engine
imports Cantera.

Validity of what we use (printed from the installed mechanism, `species(...).thermo`):

| Species | NASA polynomial range (K) |
|---|---|
| CO₂, H₂O, O₂, CO, H₂, OH, CH₄ | 200–3500 |
| N₂, Ar, C₃H₈ | 300–5000 |
| NO | 200–6000 |

A kiln uses 280–1700 K, inside every range. An ideal-gas phase evaluates the polynomials outside
their range rather than refusing (not tested here), so the engine should keep its own refusal at
the chamber's range (ADR 0009). Source: the
GRI-Mech 3.0 thermo file (Smith, Golden, Frenklach et al., GRI-Mech 3.0, 1999,
http://combustion.berkeley.edu/gri-mech/), as the mechanism header says.

The **kinetics** of GRI-Mech 3.0 were optimised for "roughly 1000 to 2500 K, 10 Torr to 10 atm,
and equivalence ratios from 0.1 to 5 for premixed systems" of natural gas (GRI-Mech 3.0 web page,
from memory of its "Optimization" note: re-read and quote before any kinetic use). Propane is in
the mechanism but not one of its targets. This matters only for §6 (reactor networks); equilibrium
uses none of it.

## 2. Wood flue-gas sensible heat q(T, λ) (plan step F; firebox-efficiency.md §4, §6)

**What it gives.** The enthalpy of the products of a wood surrogate from 25 °C to the flue
temperature, per kg of wood, for any λ, frozen (complete combustion) or at equilibrium. Wood itself
needs no Cantera species: its heat comes from the sourced H(w) (FAO UBET eq. 3, `wood.py`), and
Cantera supplies only the products' enthalpies.

**API.** Products per kg dry wood from the 50/6/44 C/H/O split (Pettersen 1984, as quoted in
FE §4): CO₂ = C, H₂O = H/2 + moisture, O₂ = (λ − 1)s, N₂ = λ·s·3.773, with s = C + H/4 − O/2.
Then `gas.TPX = T, ct.one_atm, products`, optionally `gas.equilibrate("TP")`, and
q = n·[h̄(T) − h̄(298.15 K)] ÷ H(w). The same five calls the engine already makes for propane.

**Result.** Surrogate CH₁.₄₃₀O₀.₆₆₁, stoichiometric O₂ 42.76 mol/kg, air 5.89 kg per kg dry
wood. Flue loss, % of the net heat as fired, moisture 12 % wet basis, frozen | equilibrium:

| λ | 200 °C | 600 °C | 900 °C | 1100 °C | 1300 °C |
|---|---|---|---|---|---|
| 1.0 | 7.2 \| 7.2 | 25.1 \| 25.1 | 39.8 \| 39.8 | 50.0 \| 50.0 | 60.5 \| 60.6 |
| 1.2 | 8.3 \| 8.3 | 29.0 \| 29.0 | 45.8 \| 45.8 | 57.5 \| 57.5 | 69.5 \| 69.6 |
| 1.5 | 10.0 \| 10.0 | 34.7 \| 34.7 | 54.8 \| 54.8 | 68.8 \| 68.9 | 83.1 \| 83.3 |
| 2.0 | 12.8 \| 12.8 | 44.3 \| 44.3 | 69.9 \| 69.9 | 87.6 \| 87.7 | 105.8 \| 106.1 |

This reproduces FE §4's table to the rounding, so that table's method is confirmed. Dissociation
adds at most 0.3 points at 1300 °C: equilibrium is not needed for oxidising wood, but using
`equilibrate("TP")` as for propane keeps one method.

**Below stoichiometric air (reduction), equilibrium.** Loss = [H_eq(T) − H_complete(25 °C)] ÷ H(w),
H_complete being the fully oxidised products the net heating value is referred to
(`wood_reduction.py`):

| λ | 900 °C | 1100 °C | 1300 °C | x_CO at 1300 °C |
|---|---|---|---|---|
| 1.00 | 39.8 | 50.0 | 60.6 | 0 |
| 0.95 | 44.4 | 54.3 | 64.4 | 1.4 % |
| 0.90 | 49.0 | 58.6 | 68.4 | 2.8 % |
| 0.80 | 58.3 | 67.2 | 76.3 | 5.9 % |

This is the part of FE §6's unburnt allowance u that comes from deliberate reduction, computed the
same way ADR 0012 already treats propane at λ 0.9. It does not cover smoke, char in the ash or CO
left by poor mixing at λ > 1; u keeps those, still unsourced.

**Validity and sources.** NASA polynomials 200–3500 K (§1). The composition is the weak link:
Pettersen (1984) has not been read at the page. Equilibrium at λ < 1 assumes the gas reaches
equilibrium at the chamber's temperature and freezes after; no source checks that for a kiln.

**Effect.** Plan step F (review #17): replaces the user's single η with η_step = 1 − q(T, λ) − u.
The wood burnt in the last hours would carry most of the firing's total, since q is 50–70 % above
1100 °C (λ 1.0–1.2).

**Verdict: adopt the method for step F** (no new dependency; same API as `combustion.py`), once
Pettersen is read and one weighed firing checks it, as the plan already says. Reduction losses from
equilibrium: **proposed**, as a second step.

## 3. Excess air through a firing (review #3)

**What it gives.** Nothing new: `available_heat(t_flue, air_ratio, ...)` already takes λ. A λ(T)
schedule is a data problem, not a library one. The only code change is the cache in
`simulation.py`, which would need λ in its key.

**Validity.** As §1. **Effect:** review #3 (+1 to +5 % fuel on the gas kiln). **Verdict: not a
Cantera question.** Blocked on a measured O₂ through a firing, as the review says.

## 4. Flue gas leaving hotter than the chamber (review #2)

**What Cantera gives.** The heat side is already there: `available_heat(t_flue=T_c + ΔT)` is how
the review measured +8 / +18 / +35 %. What is missing is ΔT itself: a gas-to-load heat transfer
model (Hottel's well-stirred furnace), which needs a gas emissivity ε_g(T, p_CO₂·L, p_H₂O·L).
Cantera has no such model (§5). A reactor network with a `Wall` (§6) would only wrap the same
algebra and still need ε_g and a convective h from elsewhere.

**Verdict: not useful beyond what we use.** Review #2 stays proposed on a sourced gas emissivity
(Leckner 1972, or a weighted-sum-of-grey-gases fit; neither read here).

## 5. Gas radiation (CO₂/H₂O) for the radiation-between-faces work (review #6, EP §4)

**What Cantera has.** Only inside the 1D flame solver: `FreeFlame.radiation_enabled`,
`boundary_emissivities`, `Flow1D.radiative_heat_loss`. `Flow1D.h` documents it: "The simple
radiation model used was established by Liu and Rogg [1991]. This model considers the radiation of
CO2 and H2O. This model uses the optically thin limit and the gray-gas approximation to simply
calculate a volume specified heat flux out of the Planck absorption coefficients, the boundary
emissivities and the temperature." The coefficients (`Flow1D.cpp`, `computeRadiation`) are
fifth-order polynomials in 1000/T for H₂O and CO₂, "taken from the RADCAL program" via the TNF
Workshop. No radiation property is exposed on `Solution` or `ThermoPhase`, and there is no
separate radiation class in 3.2.0.

**Validity, from the cited source.** TNF Workshop radiation page (https://tnfworkshop.org/radiation/,
read 2026-11-09): the fits "were generated for temperatures between 300K and 2500K and may be very
inaccurate outside this range"; they are fits to RADCAL (Grosshandler, NIST Technical Note 1402,
1993); the model assumes each point "has an unobstructed, isotropic view of the cold surroundings",
and it "likely over-predicts radiative losses" for CH₄ flames because of CO₂'s 4.3 µm band
absorption. It is meant for small laboratory flames.

**Measured misuse.** Propane products at λ 1.15 (x_CO₂ 0.102, x_H₂O 0.136), Planck-mean k_P from
those polynomials, and 1 − exp(−k_P·L) taken as if it were an emissivity:

| T | k_P (1/m) | L 0.5 m | L 1.0 m |
|---|---|---|---|
| 600 °C | 4.29 | 0.88 | 0.99 |
| 1000 °C | 2.29 | 0.68 | 0.90 |
| 1300 °C | 1.41 | 0.51 | 0.76 |

A kiln chamber is optically thick in the band centres and transparent between bands, which a
Planck-mean grey gas cannot represent; these figures are far above what band-model charts give for
such paths (the Hottel/Leckner values are not recorded in `docs/research/` yet, so no number is
quoted against them here). The model is right for its purpose (emission loss from a thin flame)
and wrong for exchange in a kiln.

**Verdict: not useful.** Keep gas radiation out of the face-to-face work and say so, as EP §4
recommends. The candidates for a sourced method remain Leckner (1972) or a WSGG fit, plus mean
beam length 3.6 V/A.

## 6. Reactor networks

**What it gives.** `ReactorNet` of `IdealGasConstPressureReactor`s, `Reservoir`s,
`MassFlowController`s and `Wall`s (with `heat_transfer_coeff`, `emissivity` and `heat_flux`;
3.2 adds a steady-state solver for networks), integrated by CVODES. A well-stirred chamber fed by a
burner, losing heat through a wall to a reservoir at the ware's temperature, is easy to set up.
`FlowReactor` (plug flow) could follow a gas parcel up a chimney.

**Fit.** The furnace heat balance we need is algebraic per time step (review #2's Hottel form);
a network adds a stiff ODE integrator and the GRI-Mech kinetics without adding any physics we lack.
`Wall.emissivity` is a grey surface-to-surface term between two reactors, not a gas emissivity, so
the missing input (§4, §5) stays missing. The one kinetic question it could answer, whether CO from
reduction burns out in the chimney, falls under GRI-Mech's optimisation range (§1) only partly
(the stack is below 1000 K at its top, and wood volatiles are not methane).

**Verdict: not useful** now. Revisit only if a sourced CO-burnout question arises.

## 7. Transport properties of flue gas (review #4 draft friction; HL #8 stack cooling)

**What it gives.** `gas.transport_model = "mixture-averaged"`; then `viscosity`,
`thermal_conductivity`, `cp_mass`, `density` of the actual flue gas at any temperature.

**Sources and validity.** Pure-species Lennard-Jones parameters from the GRI-Mech 3.0 transport
file; collision integrals from Monchick & Mason's tables (`GasTransport.cpp`: "set up Monchick and
Mason collision integrals"); mixture viscosity by Poling et al. (2001) eq. 9-5.14; method per Kee,
Coltrin & Glarborg, *Chemically Reacting Flow* (2003). The polynomial fits are made over the
phase's thermo range, `minTemp()` to `maxTemp()` (300–3500 K for gri30), at 50 points. No
accuracy is stated by Cantera; it must come from a comparison.

**Checked against our air table** (Holman Table A-5 via `thermal/air.py`), dry air 21/78/1:

| T (K) | μ, Cantera vs Holman | k, Cantera vs Holman |
|---|---|---|
| 300 | +1.0 % | +1.1 % |
| 600 | +1.1 % | 0.0 % |
| 1000 | +2.9 % | +3.1 % |

Propane flue gas, λ 1.15 (M = 28.39 g/mol, against the 28.5 the draft check uses):

| T | ρ (kg/m³) | c_p (J/(kg·K)) | μ (Pa·s) | k (W/(m·K)) | Pr |
|---|---|---|---|---|---|
| 200 °C | 0.731 | 1119 | 2.40e-5 | 0.0377 | 0.711 |
| 600 °C | 0.396 | 1238 | 3.75e-5 | 0.0655 | 0.708 |
| 1000 °C | 0.272 | 1333 | 4.87e-5 | 0.0919 | 0.706 |
| 1300 °C | 0.220 | 1383 | 5.62e-5 | 0.1104 | 0.704 |

**Effect.** Gives Re (review #4's friction term, Re ≈ 3000–4300), the gas density for the stack
term in place of a fixed molar mass, and Pr, k for a Gnielinski flue-convection model (HL #8). It
would not replace `air.py` for outside surfaces: films there stay under 1000 K, and the table is
the cited source.

**Verdict: proposed**, as the flue-gas property source when review #4 or HL #8 is built. Record
the method's sources in `docs/research/structure-and-draft.md` and keep a test against Holman air
(within 3.5 % to 1000 K) as the check ADR 0009 asks for. Above 1000 K there is no independent
check yet; cite that as the limit of what has been verified.

## 8. Wood composition

Cantera has no wood, biomass or solid-fuel data. It cannot supply the 50/6/44 split or the heating
value. **Verdict: not useful**; Pettersen (1984) or an ultimate analysis (e.g. Phyllis2) is still
needed.

## 9. TESPy

**What it is.** A steady-state network solver for power-plant and heat-pump cycles: components
(turbines, compressors, pumps, heat exchangers, pipes, valves, mixers, combustion chambers) joined
by connections, solved for mass, energy and pressure by Newton's method, design then off-design.
Fluid properties from CoolProp.

**Maintenance and packaging.** Active: 0.10.1 to 0.11.3 between June and October 2026, mostly by
the lead developer (fwitte), with a few contributors per release. PyPI `requires_python >= 3.11`,
classifiers 3.11–3.13; it is a pure-Python wheel and **installs and runs on CPython 3.14.10 on
Linux**. `uv pip compile --python-version 3.14 --python-platform x86_64-pc-windows-msvc
--only-binary :all:` resolves all 24 packages to wheels, so **cp314 win_amd64 wheels exist for
CoolProp 8.0.0** and the rest. Dependencies: CoolProp (10 MB), fluprodia, pandas, matplotlib,
jinja2, scipy, numpy, pint, tabulate.

**The components against our problems.**

- *Combustion chamber* (`CombustionChamber`, `DiabaticCombustionChamber`). Complete combustion to
  CO₂ and H₂O, no dissociation; fuels are CoolProp gases with an enthalpy of formation in
  `COMBUSTION_FLUIDS` (methane −74.6, propane −103.8 kJ/mol, no source given in the code);
  `lamb` has `min_val=1`. A cross-check: propane, λ 1.15, outlet held at the kiln temperature,
  heat dissipated ÷ thermal input (LHV basis):

  | Flue | TESPy | Cantera (`combustion.py`) |
  |---|---|---|
  | 600 °C | 0.7296 | 0.7291 |
  | 1000 °C | 0.5192 | 0.5179 |
  | 1285 °C | 0.3614 | 0.3588 |

  Agreement within 0.7 %, the gap being dissociation, which TESPy leaves out. At λ 0.9 it logs
  "Invalid value for lamb ... below minimum value (1)" and returns a result anyway: reduction is
  outside its model, and it warns rather than refuses. It also warns that the mixture is "above the
  upper temperature limit of a mixture component" (CoolProp's propane Tmax is 650 K and methane's
  625 K; CO₂, water, N₂, O₂, Ar have Tmax 2000 K, which for CO₂ (Span & Wagner 1996) and water
  (IAPWS-95) is beyond the range their papers validate: to be confirmed from those papers if ever
  relevant). No solid fuel: wood cannot be a TESPy fuel.
- *Heat exchangers* (simple, counter-current, NTU, sectioned). Driven by a user-given UA or a
  characteristic curve; no convection correlations. A recuperator could be balanced, but none of
  our designs has one, and UA would still need ht-style correlations from a cited source.
- *Chimney and draft.* `Pipe` has Darcy–Weisbach and Hazen–Williams pressure loss, and no
  elevation or buoyancy term (the only gravity in the package is in the Hazen–Williams formula and
  the pump's head). A stack draft cannot be expressed without writing a custom component, at which
  point the component is our own formula.
- *Transient.* None. The firing simulation (ADR 0015) is a time-marching wall model with stored
  heat; TESPy solves stationary operating points only.

**Verdict: not useful. It doesn't fit.** Its combustion gives what Cantera already gives with less
physics (no dissociation, no reduction); its pipes have no buoyancy; it is steady-state only; and
it would add CoolProp, pandas and matplotlib to the engine for nothing we lack. Not proposed as a
dependency or as a test oracle (Cantera and our own hand cases are better checks).

## 10. Ranked

| # | Use | Package | Effect on users' numbers | Source and range | Verdict | Effort |
|---|---|---|---|---|---|---|
| 1 | Wood flue loss q(T, λ) per step, η_step = 1 − q − u (plan F) | Cantera thermo (in use) | Wood per firing set by λ and T instead of one η; flue loss 25–29 % at 600 °C, 60–70 % at 1300 °C (λ 1.0–1.2) | GRI-Mech 3.0 NASA polynomials, 200–3500 K; Pettersen 1984 composition (to read); FAO UBET eq. 3 | **adopt** for step F, after Pettersen and one weighed firing | Low–medium |
| 2 | Flue-gas μ, k, c_p, ρ for draft friction and stack convection | Cantera transport (in package, unused) | Re, net draft (review #4), stack gas temperature (HL #8) | GRI-Mech transport file; Monchick & Mason; Kee et al. 2003; checked vs Holman air to +3.1 % at 1000 K; fitted 300–3500 K | **proposed**, with #4 / HL #8 | Low |
| 3 | Reduction loss for wood from equilibrium CO/H₂ | Cantera thermo | +4 / +8 / +16 points of flue loss at λ 0.95 / 0.9 / 0.8 (1300 °C) | as 1; equilibrium assumed, as ADR 0012 for propane | **proposed**, after #1 | Low |
| 4 | Excess air varying through the firing | none new | +1 to +5 % gas-kiln fuel (review #3) | needs measured O₂ | not a library question | – |
| 5 | Gas temperature above the chamber's | none | +8 to +35 % fuel (review #2) | needs a gas emissivity (Leckner 1972 / WSGG) | Cantera not useful | – |
| 6 | CO₂/H₂O gas radiation | Cantera Flow1D (Liu & Rogg; RADCAL/TNF, 300–2500 K, optically thin) | none: unsuitable for a kiln-sized path | TNF Workshop; Grosshandler NIST TN 1402 | **not useful** | – |
| 7 | Reactor networks | Cantera | none | GRI-Mech kinetics, ~1000–2500 K natural gas | **not useful** | – |
| 8 | Wood composition | Cantera | – | none in Cantera | **not useful** | – |
| 9 | TESPy combustion, heat exchangers, pipes | TESPy 0.11.3 + CoolProp 8.0.0 | – | steady only; λ ≥ 1; no buoyancy | **not useful** | – |

Not proposed: adding any dependency. Everything worth taking is in Cantera, already locked.

## Not found / not read

- Pettersen (1984) at the page; GRI-Mech 3.0's optimisation note (quoted from memory, to re-read).
- Liu & Rogg (1991) itself; Grosshandler (1993) itself (both reached only through Cantera's
  header and the TNF page).
- Leckner (1972) and a WSGG fit for CO₂/H₂O; Hottel & Sarofim (1967).
- Span & Wagner (1996) and IAPWS-95 validity statements (stated from memory, not read here).
