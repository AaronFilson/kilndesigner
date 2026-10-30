# 15. The firing simulation: implicit finite volumes per face, the chamber as one node

- **Status:** proposed
- **Date:** 2026-10-29

## Context

M6 simulates a firing along a schedule: how long it takes, whether the heat can keep the schedule,
the energy, fuel and electricity used, the cost, and the walls' temperatures through time for a
heatmap. It has to run in seconds on a small machine (ADR 0011), many times over for a hybrid's
switch-over chart, and its numbers have to be checkable (ADR 0009).

## Decision

- **Each face is a 1D wall of finite volumes** (`thermal/transient.py`): its layers cut into cells
  of at most 5 mm, the area growing with depth as in the steady model, k(T) and c_p(T) from the
  library, and the outside losing heat through the same still-air (or ground) surface as the
  steady heat loss.
- **Backward Euler with k, c_p and h lagged a step.** Each step is then one tridiagonal solve, and
  the wall's end temperatures are affine in the chamber's temperature T_c. So the heat a step
  needs is a straight line in T_c, and the kiln picks T_c in closed form: the schedule's, the one
  its heat can reach (it falls behind), or the one it cools to with the heat off. No inner
  iteration, and an energy balance that holds exactly per step (a Hypothesis test checks it).
- **The chamber and its ware are one node**, and every face's hot face is held at it, as the
  steady heat loss does. Burners count only their available heat at the kiln's temperature
  (Cantera, ADR 0012); elements all of theirs.
- **Specific heat is sourced or asked for.** The library gives c_p only where `docs/research/`
  does. A layer without one (the castables, Cerachem) refuses the simulation with the reason, and
  the design may give the layer's `specific_heat` from its maker's sheet.
- **A run is keyed by the design's build key** and stored as ADR 0007 says: `firing.json` (the
  summary, its working and findings), `series.parquet` (every step) and `walls.parquet` (every
  face's cells every 5 steps, long form). A `simulation` table in Postgres holds the status and
  headline figures. The arq worker runs it as its own job, beside the build (ADR 0008).
- **The heatmap is drawn on the GPU.** Each face's temperatures through time are one float
  texture (depth across, time down); a fragment shader reads it at the fragment's depth and the
  scrubber's time. Scrubbing changes one uniform, with no new geometry or textures.

## Consequences

- Validated against the erf solution for a semi-infinite solid and the integral of its surface
  flux (Holman eqs. 4-8 and 4-12), against the steady C680-style solver at long times, and by the
  energy-balance invariant.
- No radiation between faces, no gas temperature apart from the walls', no inside film, and no
  air leaks or door seal. The hot face follows the chamber exactly, which overstates how fast the
  walls take heat early on.
- Lagging the properties makes the step first-order in time: a 60 s step is used, and the
  switch-over chart, which runs a firing per point, takes 300 s steps.
- The heatmap is a schematic box of the faces' mean area, not the built model's parts; colouring
  the glTF's lining parts is a later step.
- Wood, coal and oil firings wait for M7.

## In an interview

"Each wall is an implicit finite-volume model with lagged properties, so a step is one tridiagonal
solve and the heat needed is linear in the chamber temperature: the controller logic is closed
form and energy is conserved to round-off, which a property test checks. Results go to Parquet,
DuckDB downsamples them for the charts, and the heatmap is a texture lookup in a shader."
