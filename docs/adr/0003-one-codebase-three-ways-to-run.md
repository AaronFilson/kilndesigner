# 3. One codebase, three ways to run: CLI, self-hosted, hosted

- **Status:** proposed
- **Date:** 2026-10-21

## Context

The project needs a hosted app with accounts (the production story) and a self-deployed tool
(for studios, offline use and easy testing). Two products would double the work; one product
with modes needs the modes kept honest.

## Decision

- **CLI:** `kilndesigner build kiln.yaml --out plans/`. Designs are YAML files that diff well in
  git. Jobs run in process. No database, no network.
- **Self-hosted:** `docker compose up` runs the *same images* as hosted: API, worker, web,
  Postgres and Valkey. Auth defaults to a single local user bound to localhost; setting
  `OIDC_ISSUER` turns on real sign-in for a shared studio server.
- **Hosted:** the same images on AWS, with multi-tenant data separated by Postgres row-level
  security, and sign-in with Google and GitHub (OIDC, PKCE).
- Differences live in configuration and in a few adapters (`JobRunner`, `BlobStore`,
  `Authenticator`), each with an in-process or local implementation and a hosted one. Both run in
  CI.
- A design exported from the app is the same YAML the CLI reads, and the reverse.

## Consequences

- Any result in the app can be reproduced, and tested, from the command line.
- Self-hosting is a supported product, not an afterthought: it needs release notes, migrations
  that run on start, and a backup note.
- Every adapter is a second code path to test.

## In an interview

"Hosted and self-hosted are the same containers with different settings, and the CLI runs the
same engine on plain files. That made the hosted app easy to test: every bug report could be
turned into a YAML file and a golden test."
