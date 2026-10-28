# Working in this repo

## Commands

uv is installed for the user but is not on PATH. Call it by its full path,
`C:/Users/bellows/AppData/Roaming/Python/Python311/Scripts/uv.exe`; below, `uv` means that.

- One command per shell call: no `&&` chains, no shell variables such as `$U`, no `cd`.
- Read, search and edit files with the built-in tools, not the shell.
- Don't read or write outside this repo.

| Task | Command |
|---|---|
| Install or update the environment | `uv sync` |
| Tests | `uv run pytest` (`-m "not geometry"` skips the slower OpenCascade tests) |
| Coverage | `uv run pytest --cov` (branch coverage; fails under 98%). Use `--cov`, not `--cov=kilndesigner.module`: numpy can't be loaded twice in one process. The web: `npm run coverage --workspace @kilndesigner/web` (lines; fails under 98%) |
| Lint and format | `uv run ruff check --fix .` then `uv run ruff format .` |
| Types (strict) | `uv run pyright` |
| The engine stays pure (ADR 0002) | `uv run lint-imports` |
| The CLI | `uv run kilndesigner build examples/electric-front-loader.yaml --out out/` |

Run all five checks before committing; CI runs the same ones.

## Where things are

- `core/`: the `kilndesigner` engine package. No web, database or CLI imports, ever.
- `cli/`: the `kilndesigner` command (Typer).
- `examples/`: design files. Every example is loaded, round-tripped and built by the tests.
- `docs/planning/02-plan.md`: the plan and milestones. `docs/adr/`: decisions.
- `docs/research/`: cited reference data. Every number in the materials library and every
  rule of thumb in the engine must trace to a source there or in a data sheet.

## Rules for the engine

- Every physical value in a design is a Pint quantity, written with its unit (ADR 0004).
  Solvers take plain SI floats through `units.si()`.
- Every calculated result carries its working: a list of steps with the formula, the inputs,
  the value and the reference (`kilndesigner.working`).
- Never invent engineering data. If a value isn't in `docs/research/` or a cited data sheet,
  leave it out and say so.
- Outside the range that has been checked, refuse with a reason rather than guess (ADR 0009).
