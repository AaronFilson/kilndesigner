# 13. Every warning and error is a sheet of formulas you can edit

- **Status:** proposed
- **Date:** 2026-10-28

## Context

A warning that says "see arch-thrust-theory.md" asks the builder to take the engine's word for it.
Builders and inspectors trust a limit when they can see the formula, every input, where each
number comes from, and how far the design is from passing, and when they can try a change and
watch the result move. A table of allowed values doesn't show why, and a sentence can't be
checked.

## Decision

- Every warning and error carries a **check** (`kilndesigner.sheet`). A check is a list of cells:
  inputs, each with its value, unit and source, and formulas over the cells above it, then the
  requirements (`σ <= σ_allow`) with the level a failure raises.
- The formulas are written in one small expression language: numbers, names, `+ - * / ^`,
  brackets and a fixed set of functions. Both the engine (Python) and the web page (TypeScript)
  evaluate it, in SI units. A shared set of cases (`core/tests/expressions.json`) holds the two
  evaluators to the same answers.
- **The sheet is the calculation, not a description of it.** The engine raises the finding
  because the sheet's requirement fails, and each check states the engine's own result for the
  cell it describes; a mismatch fails the tests.
- Each formula is also evaluated with Pint quantities, so a formula whose dimensions don't match
  its cell's unit is a bug the tests catch.
- A check may name a **lever**: the input the builder controls. The engine and the page solve for
  the value of the lever at which the check changes state ("passes when d ≥ 0.52 in").
- Where a limit comes from a table, the sheet uses the table's formula wherever one has been
  derived and sourced; the table stays as a test of the formula.
- The web report links each warning and error to its sheet; inputs can be edited in the page
  and everything below them recomputes. The build writes `checks.xlsx`, one worksheet per check
  with live spreadsheet formulas. The PDF plans label each finding (E1, W2) and print its sheet in
  an appendix.
- A result the engine reaches by iteration (a wall's surface temperature, the line of thrust)
  enters a sheet as an input that names the working step it came from. Editing it in the page
  recomputes what follows from it, not the iteration.

## Consequences

- Adding a warning means writing its formula as a sheet, which is more work than a sentence and
  is the point.
- The expression language must stay small, because two evaluators and a spreadsheet translation
  have to agree on it.
- A finding with no formula behind it (a material that can't carry a dome) carries a check with
  a stated rule and the facts it was applied to, and no lever.
