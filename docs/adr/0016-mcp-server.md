# 16. AI assistants reach the engine through an MCP server that returns the working

- **Status:** proposed
- **Date:** 2026-11-06

## Context

M8: a potter asks an assistant to "design a cone 10 gas kiln for 12 cubic feet, under $3,000".
Left to itself the assistant guesses the engineering. The engine already works it out, with the
formula, inputs and source of every number (ADR 0002). The Model Context Protocol (MCP) is how
Claude, Copilot, Cursor and Gemini call tools.

The author has done this before in Glazecalc (its ADR 17,
[`docs/adr/0017-mcp-server.md`](https://github.com/AaronFilson/glazecalc/blob/main/docs/adr/0017-mcp-server.md)):
`POST /mcp` mounted on the app itself (not under `/api`), on the official TypeScript SDK pinned
by hand, **stateless** (a fresh server per request, no sessions, the 2026-07-28 revision and
2025-era clients both served); public tools that need no account and run the app's own library
code; snake_case verb-first tool names (`analyze_recipe`, `check_limits`, `solve_target`); every
answer as structured data and the same as JSON text, all public tools marked read-only; refusals
in words; the server's instructions telling the assistant what the numbers do not prove; personal
access tokens and then OAuth for a person's own records; per-address and per-account limits; the
official conformance suite and the MCP Inspector run in CI; a listing in the MCP Registry. In
compose it is not a service of its own: the app serves it, and nginx passes `/mcp` through.

## Decision

- **The official Python SDK, `mcp` 2.3.0, pinned** and moved by hand, as Glazecalc pins its SDK.
  Its `MCPServer` (FastMCP's name in v2) builds tool schemas from type hints. A uv workspace
  member, `kilndesigner-mcp` (package `kilndesigner_mcp`), over the engine like the CLI. The folder
  is `mcp-server/`, not the plan's `mcp/`: a top-level `mcp` folder shadows the SDK's `mcp` package
  under pytest's importlib mode.
- **The engine never imports it.** The import-linter contract forbids `kilndesigner` from importing
  `kilndesigner_mcp` or `mcp` (ADR 0002).
- **Stateless and read-only.** Every tool answers from its arguments and the packaged library;
  nothing is stored. A design is passed as its YAML text, the same file the CLI reads (ADR 0003),
  so the assistant can show it, diff it and hand it back. All tools are marked `readOnlyHint`.
- **Tools, named as Glazecalc names them:** `list_templates`, `get_template`, `list_examples`,
  `get_example`, `validate_design`, `build_design` (the design report, nothing written),
  `simulate_firing` (the summary without the temperatures through time) and `start_design` (fuel,
  cone, stacking volume, optional kind and budget: the template of that fuel nearest in chamber
  volume, set to the cone).
- **Results are the engine's own models**, dumped to JSON with their `working` steps and
  `findings`, as structured content and the same JSON in text. A tool that decides something
  itself (`start_design` choosing a template) writes its own `Step`s. Nothing is summarised away
  but the firing's time series.
- **Refuse, don't guess (ADR 0009).** A design the engine refuses comes back as a tool error with
  the engine's reason. `start_design` never resizes a template ("never resize to fit a table"): it
  reports the chamber against the volume asked for and leaves the dimensions to be changed, then
  built. It compares the chamber's volume, not a stacking volume, and says so: what the setting
  takes is not in `docs/research/`. The budget is compared with the priced bill only, and the
  unpriced lines are named.
- **Two transports from one server:** stdio (`kilndesigner-mcp`) for local clients such as Claude
  Code, and `kilndesigner-mcp --http`, stateless Streamable HTTP with JSON responses on 127.0.0.1,
  as Glazecalc's endpoint is stateless.
- **Tested through an in-memory MCP client** (`mcp.Client(server)`): the tool list, the schemas'
  annotations, each tool, its refusals, and that the text is the structured result.

### Differences from Glazecalc, and why

- **Python, not TypeScript**: the engine is Python.
- **Not yet mounted on the API, so no compose service.** Glazecalc serves `/mcp` from its app;
  here the same will be done by mounting the server's Streamable HTTP app on the FastAPI service
  at `/mcp` with its Host and Origin checks, when the hosted app has sign-in (M5). Until then it
  runs locally only, and the compose file is unchanged.
- **No accounts, tokens, OAuth or write tools yet.** Saved designs belong to accounts that do not
  exist yet; reading and saving them waits for M5's sign-in, then follows Glazecalc's tokens and
  OAuth, and its confirm-before-changes.
- **No rate limits yet**: local only. A firing simulation takes seconds of CPU, so the hosted
  endpoint will need Glazecalc's per-caller limits and a stricter one on `simulate_firing`, or the
  worker queue (ADR 0008).
- **Not yet**: resources (the materials library, the formula sheets), prompts, the conformance
  suite and Inspector in CI, and a registry listing.

## Consequences

- An assistant can start, check, calculate and fire a design exactly as the CLI does, and quote
  the working and sources rather than inventing numbers.
- Designs travel as YAML in the conversation, so a long design costs tokens, and a report is
  large; trimming it is a later choice, not a loss of working.
- The SDK is pinned; a new protocol revision is a version bump, with no stored state to migrate.
- What a design file contains is the person's text and goes back to the assistant only as a tool
  result (the prompt-injection surface Glazecalc's ADR describes); with no write tools, the most
  it can do is change what the assistant reads.

## In an interview

"The MCP server is a fourth thin shell around the same engine. Every answer carries the formula,
the inputs and the source, so the assistant quotes the engineering rather than guessing it, and
when the engine hasn't been checked for something, the assistant gets the refusal and its reason."
