# kilndesigner

Design your kiln, get plans, make pots.

Describe the kiln you want in a short design file: what it fires, the size of the chamber, the
lining, the fuel or the power supply. Kilndesigner works out the heat loss, sizes the elements
or burners, builds a 3D model and draws plans you can build from. Every number comes with its
working and its source, so you can check it.

**Status:** early development. See [the plan](docs/planning/02-plan.md), the
[market survey](docs/planning/01-market-survey.md) and the [decision records](docs/adr/README.md).

## Try it

```
uv sync
uv run kilndesigner check examples/electric-front-loader.yaml
uv run kilndesigner build examples/electric-front-loader.yaml --out out/
```

## How it's built

- `core/`: the engine, a pure Python package (Pydantic, Pint, NumPy, SciPy, build123d, Typst).
- `cli/`: the `kilndesigner` command.
- Later: a FastAPI service, workers, and a React Three Fiber web app, self-hosted with Docker
  Compose or hosted.

## Safety

Kilndesigner gives engineering guidance. It does not replace a licensed electrician, a gas
fitter, or your local codes, and its electrical and gas results say so.

## License

MIT
