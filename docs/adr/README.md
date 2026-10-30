# Architecture decision records

Short records of the decisions that shape Kilndesigner: what was decided, why, and what it costs.
Each one is written once; a later change gets a new record that replaces the old one.

| No. | Decision | Status | Date |
|---|---|---|---|
| [0001](0001-record-architecture-decisions.md) | Record architecture decisions | accepted | 2026-10-21 |
| [0002](0002-a-pure-engine-package.md) | The engine is a pure Python package; every surface sits on top of it | proposed | 2026-10-21 |
| [0003](0003-one-codebase-three-ways-to-run.md) | One codebase, three ways to run: CLI, self-hosted, hosted | proposed | 2026-10-21 |
| [0004](0004-units-with-pint.md) | Quantities carry units (Pint); the engine works in SI | proposed | 2026-10-21 |
| [0005](0005-geometry-in-python-served-as-gltf.md) | Geometry is built only in Python (build123d) and served as glTF | proposed | 2026-10-21 |
| [0006](0006-designs-as-versioned-documents-in-postgres.md) | Designs are versioned JSON documents in Postgres | proposed | 2026-10-21 |
| [0007](0007-simulation-results-in-parquet-and-duckdb.md) | Simulation results are Parquet files, queried with DuckDB | proposed | 2026-10-21 |
| [0008](0008-background-jobs-with-arq.md) | Slow work runs as jobs on Valkey and arq, or in process for the CLI | proposed | 2026-10-21 |
| [0009](0009-physics-checked-against-published-references.md) | The physics is checked against published references, in CI | proposed | 2026-10-21 |
| [0010](0010-react-and-react-three-fiber.md) | The web app is React with React Three Fiber | proposed | 2026-10-21 |
| [0011](0011-hosted-on-one-ec2-instance.md) | The hosted app is the self-hosted compose file on one EC2 instance | proposed | 2026-10-21 |
| [0012](0012-combustion-with-cantera.md) | Combustion is modelled with Cantera, not a rule of thumb | proposed | 2026-10-21 |
| [0013](0013-checks-as-evaluable-sheets.md) | Every warning and error is a sheet of formulas you can edit | proposed | 2026-10-28 |
| [0014](0014-built-kilns-are-the-reference.md) | Built kilns are the reference: a rule that fails one is the rule's fault | proposed | 2026-10-29 |
| [0015](0015-firing-simulation.md) | The firing simulation: implicit finite volumes per face, the chamber as one node | proposed | 2026-10-29 |
