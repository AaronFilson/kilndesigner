# 2. The engine is a pure Python package; every surface sits on top of it

- **Status:** proposed
- **Date:** 2026-10-21

## Context

The same calculations are needed by a CLI, a web API, background workers, notebooks and an MCP
server. If the physics leaks into request handlers or database models, each surface drifts and
the physics can only be tested through HTTP.

## Decision

- `core/` is published as the `kilndesigner` package. It depends on Pydantic, Pint, NumPy, SciPy
  and build123d, and **never** on FastAPI, SQLAlchemy, Valkey or any I/O beyond reading and
  writing files it is handed.
- Its public API is functions from a validated `Kiln` model to results: `build_geometry(kiln)`,
  `heat_loss(kiln, at=...)`, `design_elements(kiln, supply)`, `simulate(kiln, schedule)`,
  `render_plans(kiln)`.
- Every result carries its *working*: inputs, intermediate values, formulas and references.
- An import-linter contract in CI fails the build if `core` imports from `api`, `worker` or `cli`.

## Consequences

- The engine is tested in milliseconds, with no services running.
- Other people can use the library on its own, which also makes it a standalone portfolio piece.
- The API layer has a little mapping code between Pydantic models and database rows.

## In an interview

"The physics is a library with no idea it's in a web app. The API, the CLI, the worker and the
MCP server are all thin shells around the same functions, and a lint rule stops anyone from
breaking that."
