# 7. Simulation results are Parquet files, queried with DuckDB

- **Status:** proposed
- **Date:** 2026-10-21

## Context

A transient firing simulation produces temperature by time and by position in each wall: tens of
thousands to millions of values per run. Storing that in Postgres rows is slow and expensive.
Users want charts, comparisons between runs and summaries.

## Decision

- Each run writes one Parquet file (columns: run, wall, node, depth, time, temperature, heat
  flux) to the blob store: a local folder when self-hosted, S3 when hosted.
- Postgres keeps the run's metadata and its summary figures (energy, peak shell temperature, time
  to temperature).
- The API answers chart and comparison queries with DuckDB reading the Parquet files directly,
  downsampled to the chart's resolution.
- The CLI writes the same files, so notebooks read them with DuckDB or Polars.

## Consequences

- Cheap storage and fast analytical queries, with no extra server to run.
- Two places hold run data; the metadata row is written only after the file is complete.

## In an interview

"Postgres for the transactional data and DuckDB over Parquet for the simulation output. It's
the lakehouse pattern at small scale, and the CLI and notebooks read exactly the files the
app does."
