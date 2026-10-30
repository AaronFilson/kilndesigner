# 9. The physics is checked against published references, in CI

- **Status:** proposed
- **Date:** 2026-10-21

## Context

A kiln design tool is only worth using if its numbers can be trusted, and a wrong number for
elements, burners or shell temperature is a safety problem.

## Decision

- Each engineering module has a marimo notebook in `notebooks/validation/` that reproduces at
  least one published example: a worked example from a standard text, a manufacturer's data sheet
  or calculator, or an analytical solution (for example, transient conduction in a slab).
- The notebooks run as scripts in CI and assert agreement within a stated tolerance, with the
  reason for the tolerance written down.
- Every reference is cited in the result's working and in the notebook.
- Results outside the range that has been checked are refused with a reason rather than drawn.

## Consequences

- The validation notebooks are documentation people can read and run.
- Adding a module means finding a reference first; some modules will wait for one.

## In an interview

"Every formula is checked in CI against a published worked example or an analytical solution,
in notebooks you can open and read. If a design is outside what we've checked, the tool says so
rather than guessing."
