# 6. Designs are versioned JSON documents in Postgres

- **Status:** proposed
- **Date:** 2026-10-21

## Context

A design is a deep, changing tree (walls, layers, arch, ports, circuits). Users want to compare
versions and go back. Accounts, sharing and the materials library are plainly relational.

## Decision

- Postgres, through SQLAlchemy 2.0 (typed, async) and Alembic migrations.
- `design` holds the identity, owner and sharing. `design_version` holds an immutable JSONB
  document (the same schema as the YAML file), a schema version and a content hash. Saving
  creates a version; nothing is updated in place.
- The materials library, element alloys and brick catalogues are relational tables, and a design
  version records the library revision it was calculated with.
- Tenancy uses row-level security on the owner, as in Studio Manager ADR 0003.
- Old documents are upgraded by pure functions in `core`, one per schema version, tested
  against stored samples.

## Consequences

- Version history and diffs come almost for free.
- Queries inside the document (for example "all designs over 10 cubic feet") need generated
  columns or GIN indexes; only fields that are actually queried get them.

## In an interview

"Designs are immutable documents with a schema version, around a relational core. It's the
right shape for a CAD-like tool: history is a list of rows, and upgrading an old design is a pure
function you can unit test."
