# 4. Quantities carry units (Pint); the engine works in SI

- **Status:** proposed
- **Date:** 2026-10-21

## Context

Kiln building mixes BTU/hr, kW, inches, millimetres, °F, °C, cones, AWG and mm wire, and brick
sizes in inches. A unit mistake in element or burner sizing can be dangerous, not just wrong.

## Decision

- Every physical field in the model is a Pint quantity, validated by Pydantic with an expected
  dimension (`Length`, `Power`, `Temperature`). A bare number is rejected.
- The engine converts to SI on the way in and computes in SI. Results are converted to the
  design's display system on the way out.
- Temperatures use Pint's offset units, so a difference (`delta_degC`) and an absolute value can't
  be confused. Cones are a lookup, not a unit.
- Design files keep the value and unit the user typed (`9 in`), so they round-trip unchanged.

## Consequences

- Unit errors become validation errors at the boundary, with a clear message.
- Pint adds overhead in hot loops, so numerical kernels take plain NumPy arrays in SI, behind a
  typed wrapper.

## In an interview

"Every number in the model has a unit, checked at the boundary. Inside the solvers it's plain
SI NumPy for speed, and the wrapper is the only place that strips units."
