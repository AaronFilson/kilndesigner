# 11. The hosted app is the self-hosted compose file on one EC2 instance

- **Status:** proposed
- **Date:** 2026-10-21

## Context

The hosted app needs accounts, backups and approved deploys, at a cost that suits a free
project. Managed services (ECS Fargate, RDS, ElastiCache) cost roughly $60–100 a month before
anyone uses the app. Glazecalc runs on one EC2 instance for about $13 a month (Glazecalc ADR 0001).

## Decision

- The hosted app runs the same `compose.yaml` that self-hosters use, on one EC2 instance: API,
  worker, web, Postgres and Valkey. Only the settings differ (ADR 0003).
- S3 holds the Parquet results, the exported files and nightly Postgres backups.
- The instance, its role, the bucket and the deploy role are defined with AWS CDK in Python.
- Deploys follow Glazecalc ADR 0002: GitHub OIDC, an approval-gated environment, SSM with no
  SSH, and rollback if the health check fails.
- The CDK keeps the compute in its own construct, so moving to Fargate and RDS later is a new
  ADR and a construct swap, not a rewrite.

## Consequences

- Hosted and self-hosted cannot drift: every hosted deploy tests the self-hosted path.
- One instance is a single point of failure. A restore from the S3 backups is a runbook, and it
  is rehearsed.
- A long simulation competes with the API for CPU. The worker's CPU is capped in compose; heavy
  use would be the signal to move workers off the instance.

## In an interview

"The hosted app is literally the self-hosted compose file on one instance, so every production
deploy also tests the path a studio uses. It costs about the same as a lunch a month, and the
CDK is shaped so moving to Fargate later is a construct swap."
