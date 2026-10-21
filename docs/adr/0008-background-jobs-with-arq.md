# 8. Slow work runs as jobs on Valkey and arq, or in process for the CLI

- **Status:** proposed
- **Date:** 2026-10-21

## Context

Building geometry takes seconds, rendering plans takes seconds, and a transient simulation can
take minutes. None of that should block a web request.

## Decision

- A `JobRunner` interface in the API: `submit(task, args) -> job_id`, `status(job_id)`.
- Hosted and self-hosted: arq workers on Valkey. Tasks are idempotent and keyed by the design's
  content hash, so a repeated request returns the cached result.
- The CLI uses an in-process runner with the same tasks.
- Progress is pushed to the browser over server-sent events.

## Consequences

- Valkey also serves as the session store and the cache.
- Workers scale apart from the API; a slow simulation can't starve requests.
- A Postgres-backed queue would mean one fewer service; Valkey was chosen for its speed and
  progress events.

## In an interview

"Long-running numerical work goes to async workers, keyed by a content hash so repeats are free,
with live progress over SSE. Locally the same tasks run in process."
