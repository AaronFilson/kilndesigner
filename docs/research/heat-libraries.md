# Open-source heat-transfer libraries: heatrapy and ht

Reviewed 2026-11-09 for what they could offer kilndesigner's heat calculations. No engine
changes were made. Comparison script: `scratch/heat-libs-review/compare.py` (run with
`uv run python scratch/heat-libs-review/compare.py`; scratch is git-ignored, so its output is
copied into the tables below).

| Library | Version read | Where | Licence |
|---|---|---|---|
| ht (Caleb Bell) | 1.2.0, the version in `uv.lock` (PyPI, 2025-10-26) | https://github.com/CalebBell/ht; read from the installed package, `.venv/Lib/site-packages/ht/` | MIT (header of each module) |
| heatrapy (Daniel Silva) | tag v2.1.1, master as cloned 2026-11-09 | https://github.com/djsilva99/heatrapy; cloned to `scratch/heat-libs/heatrapy` | MIT (`LICENSE`, "Copyright (c) 2017 Daniel Silva") |

Both licences allow use and copying with the notice kept. Neither is a source of engineering
data in itself: under CLAUDE.md, a value or correlation is usable only through the primary
source each docstring cites, which must then be recorded in `docs/research/`.

## 1. What we use of ht today

ht is a dependency (`pyproject.toml` line 29, `ht>=1.2`) but only in tests and the validation
notebook, never in the engine: `core/tests/thermal/test_surface.py` and
`notebooks/validation/surface.py` check our Churchill–Chu, Lloyd–Moran, 0.27 Ra^¼ and h_r
against `ht.conv_free_immersed.Nu_vertical_plate_Churchill`, `Nu_horizontal_plate_McAdams` and
`ht.radiation.q_rad`. The engine's own code is `core/src/kilndesigner/thermal/surface.py`.

## 2. ht: free convection

### 2.1 Horizontal plate, hot face down (energyplus-review.md item 3)

ht 1.2.0 has three hot-face-down forms (`buoyancy=False` for a hot plate facing down), in
`conv_free_immersed.py`:

| Function | Form | Cited source (docstring) | Length scale (docstring) | Range given |
|---|---|---|---|---|
| `Nu_horizontal_plate_McAdams` | 0.27 Ra^¼ to Ra 10¹⁰, then 0.15 Ra^⅓ | McAdams, *Heat Transmission*, 3rd ed., Krieger 1985 | not stated | switch at 10¹⁰ only |
| `Nu_horizontal_plate_VDI` (ht's default) | 0.6 (Ra·f₁)^⅕, f₁ = [1 + (0.492/Pr)^{9/16}]^{−16/9} | VDI Heat Atlas, 2nd ed., Springer 2010; "said to be from" Schlünder, *Heat Exchanger Design Handbook*, Hemisphere 1987 ("the equations there not quite the same") | L = ab/(2(a+b)), which is A/P | "recommended for the laminar flow regime"; no numbers |
| `Nu_horizontal_plate_Rohsenow` | Nu_T = 0.527 Ra^⅕ / [1 + (1.9/Pr)^{0.9}]^{2/9}, Nu = 2.5 / ln(1 + 2.5/Nu_T) | Rohsenow, Hartnett & Cho, *Handbook of Heat Transfer*, 3rd ed., McGraw-Hill 1998 (the Raithby–Hollands chapter's form) | L = ab/(2(a+b)) = A/P | laminar; no numbers |

Comparison, floor underside of a kiln on a stand, still air 20 °C, air properties from our
`thermal/air.py` at the film temperature, h in W/(m²·K). The C1340 column is EnergyPlus's coding
of ASTM C1340 (0.58 Ra^0.2 with L = √A, energyplus-review.md §3).

| Plate | T_s (°C) | Ra (L = A/P) | ours, 0.27 Ra^¼ | McAdams (ht) | VDI 0.6 Ra^⅕ | Raithby–Hollands (Rohsenow) | C1340, L = √A | h_r, ε 0.9 |
|---|---|---|---|---|---|---|---|---|
| 0.9 × 0.9 m | 60 | 3.6e7 | 2.51 | 2.51 | 1.89 | 1.71 | 1.30 | 6.29 |
| 0.9 × 0.9 m | 100 | 5.6e7 | 2.94 | 2.94 | 2.17 | 1.94 | 1.49 | 7.66 |
| 0.9 × 0.9 m | 150 | 6.5e7 | 3.25 | 3.25 | 2.38 | 2.13 | 1.63 | 9.69 |
| 0.9 × 0.9 m | 250 | 6.2e7 | 3.58 | 3.58 | 2.62 | 2.34 | 1.80 | 14.98 |
| 1.2 × 1.8 m | 60 | 1.5e8 | 2.23 | 2.23 | 1.57 | 1.39 | 1.07 | 6.29 |
| 1.2 × 1.8 m | 150 | 2.7e8 | 2.89 | 2.89 | 1.97 | 1.73 | 1.34 | 9.69 |
| 1.2 × 1.8 m | 250 | 2.5e8 | 3.18 | 3.18 | 2.17 | 1.90 | 1.48 | 14.98 |

Findings:

- Ours is exactly ht's McAdams (as the existing test asserts). It is the highest of the five.
- The three Ra^⅕ forms from three separate lineages (VDI/Schlünder, Raithby–Hollands, C1340)
  all fall below it: VDI by 25–30 %, Raithby–Hollands by 32–38 %, C1340 by 48–52 %. Part of
  C1340's gap is its length scale (√A is twice A/P for a square, and Nu/L with Ra^⅕ gives
  h ∝ L^{−0.4}).
- Both handbook forms use the ⅕ exponent, as does C1340; for a hot face down the boundary layer
  flows outward to the edges, and the ⅕ power is the laminar scaling these sources adopt. (The
  primary derivation was not read here; to confirm from the Raithby–Hollands chapter.)
  0.27 Ra^¼ is McAdams's older empirical fit.
- At the face's combined coefficient the effect is modest because radiation dominates: going to
  Raithby–Hollands lowers h_total of the 0.9 m floor at 150 °C from 12.94 to 11.82 W/(m²·K),
  −9 %; at 60 °C from 8.80 to 8.00, −9 %. That face's surface temperature rises a little and its
  loss falls a little. Total kiln loss changes by a few tenths of a percent (one face of six,
  and the floor is usually the coolest in loss).

**Verdict (provisional):** 0.27 Ra^¼ is the outlier, high by about a third against the two
handbook Ra^⅕ correlations at the same L = A/P. The better-founded choice is the
Raithby–Hollands form (Rohsenow et al. 1998) or VDI's 0.6 Ra^⅕, both with L = A/P, which keeps
our length scale. C1340's √A is not needed to explain the difference and should not be mixed
in. Before the engine changes, the Raithby–Hollands chapter (Rohsenow, Hartnett & Cho 1998,
ch. 4) or the VDI Heat Atlas section must be read and its Ra range recorded in
`thermal-properties.md` §5, because ht's docstrings give no numeric range for either. Until
then the current form overstates floor-underside convection and so slightly understates that
face's surface temperature (non-conservative for touch temperature, conservative for fuel).

### 2.2 Horizontal plate, hot face up

`Nu_horizontal_plate_VDI(buoyancy=True)`: 0.766 (Ra·f₂)^⅕ below Ra·f₂ = 7×10⁴, else
0.15 (Ra·f₂)^⅓, f₂ = [1 + (0.322/Pr)^{0.55}]^{20/11} (VDI Heat Atlas, cites Stewartson 1958).
At a roof with L = A/P = 0.225 m it gives **35 % more** than our Lloyd–Moran 0.54 Ra^¼
(8.05 against 5.95 W/(m²·K) at 60 °C; 12.01 against 8.86 at 250 °C) because it switches to the
turbulent Ra^⅓ branch far earlier (7×10⁴ instead of 10⁷) and its f₂ factor is about 1.5 for
air. `Nu_horizontal_plate_Rohsenow(buoyancy=True)` is a blended laminar/turbulent form
(Rohsenow 1998). Not proposed for adoption: Lloyd–Moran is from the textbooks we cite
(Incropera), but the spread between sources (~35 %) should be quoted as the uncertainty of the
roof's convection in the physics review.

### 2.3 Vertical plates and cylinders (walls, chimneys)

- `Nu_vertical_plate_Churchill` (Churchill & Chu 1975, IJHMT 18:1323): ours, identical.
- `Nu_vertical_cylinder_Popiel_Churchill` (Popiel, Wojtkowiak & Bober 2007, Exp. Therm. Fluid
  Sci. 32:607; Popiel 2008 review, Heat Transfer Eng. 29:521): plate × curvature factor,
  0.01 < Pr < 100, **laminar only, Ra < 10⁹** in ht's own table. A 3 m chimney at 100–300 °C has
  Ra_H ≈ 1.3–1.6×10¹¹, outside it. Where computed anyway it adds 3 % to the plate value
  (5.61 against 5.44 W/(m²·K) at 100 °C, D 0.3 m). Other vertical-cylinder fits in ht
  (Griffiths–Davis, Jakob–Linke, Carne, Eigenson, Touloukian, McAdams–Weiss–Saunders,
  Kreith–Eckert, Al-Arabi–Khamis, all "as presented in Morgan") have turbulent branches; none
  changes the answer by more than the curvature correction at D/H = 0.1. Keep the plate for a
  chimney and refuse nothing new; the criterion D/H ≥ 35/Gr^¼ quoted in ht's Churchill–Chu
  docstring (Bergman et al. 2011) is the check to add for slender stacks.
- `Nu_horizontal_cylinder_Churchill_Chu` (Churchill & Chu 1975, IJHMT 18:1049, in ht): for a
  horizontal flue pipe, 5.83 W/(m²·K) at 100 °C, D 0.3 m. We have no horizontal-cylinder face;
  a flue connector exposed in the room would use it. Low priority.

### 2.4 Enclosed spaces

`conv_free_enclosed.py`: `Nu_Nusselt_Rayleigh_Hollands` (Hollands 1984, IJHMT 27:466, as
recommended in VDI 2010) for horizontal layers heated from below with `Rac_Nusselt_Rayleigh`
for finite boxes; `Nu_Nusselt_vertical_Thess` for vertical slots; Probert; Holling–Herwig.
Relevant only to an air gap in a wall (a ventilated double shell or a gap behind sheet steel).
No current design has one; record as available.

## 3. ht: radiation

`radiation.py` has only `blackbody_spectral_radiance`, `q_rad` (grey body to surroundings),
`grey_transmittance` (Beer–Lambert) and `solar_spectrum`. **No view factors and no enclosure
exchange.** It offers nothing for the planned face-to-face ScriptF radiation
(energyplus-review.md item 1); view factors must come from Howell's catalogue or Modest, as that
review says. `grey_transmittance` could later give a flame or flue-gas path transmittance, but
needs a sourced extinction coefficient.

## 4. ht: conduction

`conduction.py`: unit conversions (`R_to_k`, `R_value_to_k`), `R_cylinder`,
`cylindrical_heat_transfer` (multi-layer cylinder with film coefficients, cites Bergman et al.)
and conduction shape factors for **buried pipes and spheres only**
(`S_isothermal_sphere_to_plane`, `S_isothermal_pipe_to_plane`,
`S_isothermal_pipe_normal_to_plane`, pipe to pipe, eccentric pipe, pipe between two planes;
from Kreith, *Principles of Heat Transfer*, and Bergman et al.). There are **no wall edge or
corner shape factors** (the 0.54 L and 0.15 L of Incropera Table 4.1) and **no disk or slab on
a semi-infinite medium**. Nothing here for our corners or grounded floors.

`cylindrical_heat_transfer` is a useful independent check for round kilns
(`round_masonry.py` walls): a test could compare our layered cylinder against it with constant
k. Low effort, test only.

## 5. ht: insulation and refractory data

`insulation.py`:

- `refractories`: 40 refractories, density plus k and c_p at 400, 600, 800, 1000, 1200 °C
  (673.15–1473.15 K), linear interpolation, **clamped** to the end values outside that range
  (`refractory_VDI_k`, `refractory_VDI_Cp`). Cited to VDI Heat Atlas 2nd ed. (2010), no section
  or table number given in the docstring. Includes Fireclay (2150 kg/m³, k 1.05–1.22), High-duty
  fireclay, Silica, Mullite, Sillimanite, Corundum, SiC 40/70/90 %, Zircon, and insulating grades
  L1260, L1400, L1540, L1760, L1870 (classification temperatures, ISO 2245 style).
- `ASHRAE`: building materials at room temperature only (ASHRAE Fundamentals), incl.
  "Brick, fired clay" 1120–2400 kg/m³; and `building_materials` (DIN EN 12524:2000) at room
  temperature.

Against our Morgan data (`core/src/kilndesigner/data/ifb_conductivity.yaml`):

| T (°C) | VDI L1260 (490 kg/m³) | Morgan JM 23 (480) | VDI L1400 (790) | Morgan JM 26 (800) |
|---|---|---|---|---|
| 400 | 0.140 | 0.14 | 0.270 | 0.25 |
| 600 | 0.160 | 0.16 | 0.300 | 0.27 |
| 800 | 0.180 | 0.17 | 0.320 | 0.30 |
| 1000 | 0.200 | 0.19 | 0.340 | 0.33 |

Agreement within 0–11 %. Useful: (a) as an independent cross-check test of the castable/IFB
conductivity law; (b) as the only source we have found so far for **c_p(T) of dense fireclay
and insulating brick at 400–1200 °C** (956→1054 J/(kg·K) for fireclay, 942→1033 for L1260),
which the transient wall needs. Conditions: the VDI Heat Atlas table itself must be checked and
cited by section in `docs/research/thermal-properties.md` (not ht), the clamp must become a
refusal outside 400–1200 °C (ADR 0009) or be bridged by another sourced value at room
temperature, and the generic grades must be labelled as generic, not as any maker's brick.

`Cp_material`, `k_material`, `nearest_material`: fuzzy-name lookup across the three tables.
Not for the engine (silent best match).

## 6. ht: forced convection in ducts (flues, chimneys)

`conv_internal.py`: `turbulent_Gnielinski` (Gnielinski 1976; friction factor from `fluids`;
range to be taken from the primary paper, not checked here), `turbulent_Dittus_Boelter`,
`turbulent_Sieder_Tate`, `laminar_entry_*` (Hausen, Seider–Tate, Baehr–Stephan), `laminar_T_const`
(3.66), `Nu_laminar_rectangular_Shan_London` (Shah & London rectangular ducts), and the
`Nu_conv_internal` selector. Applicable at kiln temperatures if the gas properties are taken at
the bulk temperature (our `cantera` gas properties). Our engine has no convective flue-gas to
chimney-wall model now (draft uses friction and buoyancy only). If a chimney-gas cooling model
is added (the stack's mean gas temperature sets draft), Gnielinski with Shah & London for the
laminar entry of square flues is the standard choice. Not a change to current numbers.

`conv_external.py`: forced convection across a cylinder (Churchill–Bernstein 1977, Zukauskas
1972, Sanitjai–Goldstein 2004) and along a plate (Baehr–Stephan laminar, Schlichting turbulent).
These would let a user give a wind speed for an outdoor kiln or chimney. Wind would raise h_conv
several-fold; it is a scenario option, not a default.

`conv_packed_bed.py` (Wakao–Kagei 1982, Achenbach 1995, Gnielinski 1981) and
`conv_tube_bank.py`: in principle a model of gas through a setting of ware; no geometry in our
design files to drive them. Not proposed.

## 7. ht: temperature-dependent solid properties

Only the VDI refractory table above (k and c_p, 400–1200 °C). No metals or steel at temperature
(our shell steel would need another source).

## 8. heatrapy

heatrapy 2.1.1 (`heatrapy/dimension_1/solvers/`, `dimension_2/solvers/`) is built for
magnetocaloric and caloric-cycle research (its material database is Gd, MnFePSi, Cu, Al, Si,
...). What its schemes are, read from the code:

- `implicit_general.py`: Crank–Nicolson (θ = ½) with β = k_i Δt / (2ρc_pΔx²) built from the
  **cell's own k_i on both sides**, not an interface conductivity. At a layer boundary this is
  not conservative: the flux leaving cell i is not the flux entering cell i+1.
- `implicit_k.py`: Crank–Nicolson with the interface conductivity as the **arithmetic mean**
  (k_i + k_{i±1})/2. Conservative, but wrong in the limit of a strong jump (dense brick against
  fibre, 1.2 vs 0.1 W/(m·K)): the arithmetic mean lets the high-k side dominate, while the
  series (harmonic) resistance, which we use (Patankar 1980, `thermal/transient.py` line 5), is
  exact for steady flow across the face. Its source-term coefficient `2·dt·dt·Q` looks
  dimensionally inconsistent with the rest of the row (Δt² against Δx²); not investigated
  further, as we would not use it.
- `explicit_general.py`, `explicit_k.py`: forward Euler, stable only for Fourier number
  αΔt/Δx² ≤ ½. No adaptive check found.
- Boundaries: fixed temperature, or zero-gradient by copying the neighbour (first-order). No
  convective or radiative boundary; we have both.
- k, c_p evaluated at the old temperature (lagged), as ours. Dense `numpy.linalg.solve` on the
  full N×N matrix every step (O(N³)); we use a tridiagonal solve.
- Uniform Δx and Δt.
- Validation: the tests in `test/integration/` and `test/unit/` are regression values
  ("solution = 245" after 30 steps); **no analytical comparison** in the repository.

Against our wall (`thermal/transient.py`, backward Euler, harmonic interfaces, lagged
properties, ADR 0015):

- Stability: backward Euler is L-stable; Crank–Nicolson is A-stable but not L-stable, so with
  the large Fourier numbers of a firing step (a 1 min step on a 5 mm cell of fibre) it gives
  decaying oscillations after a sudden hot-face change (Patankar 1980, ch. 4, on the
  explicit/Crank–Nicolson/fully implicit family). No gain.
- Accuracy at layer jumps: ours is better (harmonic vs arithmetic or none).
- Accuracy in time: CN is second order, ours first. The EnergyPlus review's item 4 (Picard
  update of k and c_p to the new level) addresses the larger error, the property lag; a
  θ-scheme with θ ≈ 0.5–0.6 would be the second step, only if halved-step tests show time error
  matters. heatrapy offers no code we would take.

Analytical validation cases worth adding (ADR 0009), none of which heatrapy has:

1. Plane wall with a convective face, one-term and full series solution (Incropera et al.,
   *Fundamentals of Heat and Mass Transfer*, §5.5); checks the h boundary, which our erf case
   does not.
2. Two-layer composite slab, step change at one face (de Monte 2000, IJHMT 43:3607, "Transient
   heat conduction in one-dimensional composite slab"): the direct test of the layer interface.
   Citation to be confirmed against the paper before use.
3. Surface temperature rising linearly in time on a semi-infinite solid (Carslaw & Jaeger,
   *Conduction of Heat in Solids*, 2nd ed., 1959, ch. II): a firing ramp, checks the lag error
   that item 4 targets. Section to be confirmed.
4. Steady layered cylinder against `ht.conduction.cylindrical_heat_transfer` (constant k) for
   round kilns.

## 9. Proposed engine changes, ranked

| # | Change | Effect on users' numbers | Source | Effort |
|---|---|---|---|---|
| 1 | Hot face down: replace 0.27 Ra^¼ with Raithby–Hollands' Ra^⅕ form (or VDI 0.6 Ra^⅕), L = A/P, with its stated Ra range | Floor-underside convection −32 to −38 %; that face's combined h −9 %; its surface a few °C warmer; total loss a few tenths of a percent lower | Rohsenow, Hartnett & Cho 1998 (ht `Nu_horizontal_plate_Rohsenow`); VDI Heat Atlas 2010 (`Nu_horizontal_plate_VDI`); must read the primary text for the range first | Low, after reading the source |
| 2 | Add the two-layer composite slab and convective-face plane wall analytical tests to `test_transient.py` | None directly; validates the interface and h boundary (ADR 0009) | de Monte 2000; Incropera §5.5 | Low |
| 3 | c_p(T) of dense fireclay and insulating brick from the VDI Heat Atlas refractory table, refusing outside 400–1200 °C | The table's c_p rises about 10 % from 400 to 1200 °C (fireclay 956→1054); stored heat and heat-up of heavy kilns change by up to that where we now hold c_p lower; not yet computed against our current values | VDI Heat Atlas 2010 table, via `ht.insulation.refractories`; cite the table, not ht | Medium (data entry + a range rule) |
| 4 | Cross-check test: VDI L1260/L1400 k against the Morgan JM 23/26 law | None; an independent check, 0–11 % | as 3 | Very low |
| 5 | Quote the roof's convection spread (Lloyd–Moran vs VDI, ~35 %) as an uncertainty in the working | Working shows the band; numbers unchanged | VDI Heat Atlas; Lloyd & Moran 1974 | Low |
| 6 | Slender-stack check D/H ≥ 35/Gr^¼ for chimney faces | Refusal or note for thin steel stacks; values within 3 % otherwise | Bergman et al. 2011, as cited in ht | Very low |
| 7 | Optional wind speed for outdoor kilns and chimneys (Churchill–Bernstein cylinder, flat plate) | Shell loss several times higher in wind; a scenario, not a default | Churchill & Bernstein 1977; Schlichting & Gersten 1997 | Medium |
| 8 | Flue-gas convection to the chimney wall (Gnielinski, Shah & London) for a cooling stack | Mean stack temperature, so draft, on tall unlined stacks | Gnielinski 1976; Shah & London 1978 | Medium-high; defer |

Not proposed: heatrapy's solvers (no gain over ours); ht's view factors (none exist); ht's
shape factors (no wall corners or floors); ASHRAE/DIN room-temperature tables (out of range).
