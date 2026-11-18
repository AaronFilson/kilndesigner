# Module review: engine v2 and the surfaces (2026-11-17)

Branch `plan-review` at `6bcadb7`. Scope: `core/src/kilndesigner/v2`, its tests, and what the
CLI, API, worker, web and MCP server would need to switch to it. No code was changed.

## Summary

v2 is a strong set of solvers with no front door. Each part works on a `model.Kiln`, but a full
heat run needs inputs that today live only in `core/tests/v2/`. v2 also leans on v1's layout and
heat modules well past ADR 0017's leaf list, so "remove v1's heat and statics" can't happen as
written. Heat and statics share the design model but no hot state. No surface can switch until
v2 has one entry point per design and one result shape.

Findings are ranked by impact on the switch.

## 1. Engine knowledge lives in the tests (high)

A heat result needs a `Load` (`v2/heat/kiln.py:58`, required by decision 11) and, for a fired
kiln, draft-path inputs (`paths.Inputs`, `v2/heat/paths.py:143`). Both are built only in tests:

- `core/tests/v2/loads.py:50-77` holds the sourced rules that turn a design into a setting band:
  ware density 60–260 kg/m³, shelf weights, combustion space, under-shelf gap, the setting's
  emissivity. These are general engine rules with citations, not test data.
- `core/tests/v2/path_inputs.py:101` builds `Inputs` from the reference dataset; the one-firebox-
  per-chamber rule and the Rule 6 set (`:36`, `:40`) are kiln-specific overrides.
- `core/tests/v2/fuel.py:22-41` holds wood heating values, cord weights and diesel's heat, while
  the engine's own fuels are in `v2/heat/gas.py:97-131`. Two homes for fuel data.
- `heat_cases.py`, `single_cases.py`, `row_cases.py`, `gas_cases.py` hold the call recipes
  (λ, mode, schedule, bands' corners) that a caller would need to repeat.

`heat_model` also takes `air_ratio` as an argument (`v2/heat/kiln.py:275`), though decision 9
says λ comes from the intakes and the draft; `firing.FixedInput(air="draft")` does this, but the
default path is a given λ. `path_inputs` is typed `object` (`:288`).

**Recommend:** move `loads.py`'s rules into `v2/heat/setting.py` (a `load_of(kiln, end)` that
reads `model.Setting`/`Shelves`/`Loading` and falls back to the sourced band), and fuel data into
`v2/heat/gas.py` or `library`. Add optional design-file fields for what `Inputs` carries
(intakes, grate bar, chimney band, flue sizes) so a design can say them; keep the dataset
reader in tests. Type `path_inputs` as `paths.Inputs | None`.

## 2. No single entry point or result shape (high)

- Heat has `heat_model` (`v2/heat/kiln.py:272`) returning a `ZoneModel`, then `firing.fire`
  (`v2/heat/firing.py:279`) with a `Mode`, or `series.fire_stages` (`series.py:167`) for rows, or
  `target.input_for` (`target.py:41`). The caller must pick segments, `path`, stages and λ.
- Statics has one: `statics(kiln) -> KilnStatics` (`v2/statics/kiln.py:61`). Good.
- `Firing` (`firing.py:114`) is a frozen dataclass of numpy arrays in SI floats, `KilnStatics`
  (`statics/kiln.py:43`) a dataclass with `dict[str, float]` in N/m. Neither is pydantic, neither
  carries units or `Finding`s.

The surfaces consume v1's pydantic `Report` (`report.py:28`): `heat_loss`, `gas`, `fire`,
`electric`, `target`, `frame`, `findings`, serialised to JSON for the API, the worker's Parquet
results (`results.py`) and the web (`web/src/components/ReportView.tsx`, `FiringPanel.tsx`).

**Recommend:** add `kilndesigner.v2.design(kiln) -> V2Report` (pydantic): it builds the load and
inputs (finding 1), picks single chamber vs row, runs one firing at the nominal band end plus the
band's corners on request, runs `statics`, and returns quantities shown with units (`working.show`)
and `Step`s. Make the band explicit (`least/nominal/most`) as v2's answer instead of one number.
v2 raises no flags (decision 3), so the report's `findings` would carry only `info` and the
`missing`/`NotModelledError` reasons; the web's error badges need a no-flags mode.

## 3. v2 depends on v1 heat and layout modules ADR 0017 would remove (high)

ADR 0017 allows units, working, sheet, model, shape, library, cones, combustion, `thermal.*`
(`docs/adr/0017-engine-v2.md:137`), and says v1's heat and statics modules go (`:139`). v2 imports
well beyond that:

- **v1 heat:** `kilndesigner.gas.kiln_top_in` (`v2/heat/paths.py:1314`),
  `kilndesigner.electric.CONTINUOUS_FRACTION` (`v2/heat/kiln.py:423`). Both `gas.py:69` and
  `electric.py:24` import `heatloss`, so v2 transitively needs `heatloss`. `firebox_parts.py:784`
  imports `gas.BURNER_PORTS`, so the layout path does too.
- **v1 layout and geometry:** `massing` (private `_roof_top`, `_axis`: `v2/heat/chamber.py:133,153`),
  `firebox_parts` (private `_layers`: `v2/heat/paths.py:848`), `run_parts`, `crossing`, `groin`,
  `openings`, `hardware` (`kiln.py:250`), `common_wall`, `form`, `outline`, `numeric`, and
  `geometry` (OpenCascade) in statics (`v2/statics/row.py:50`, `section.py:31`).
- No v2 module imports v1's `heatloss`, `simulation`, `target`, `slow`, `frame` or `vault`
  directly. That part is clean.

**Recommend:** amend the ADR's leaf list to name the layout modules v2 relies on (massing,
firebox_parts, run_parts, crossing, groin, openings, geometry, form, outline, common_wall,
numeric), since they are kept anyway for plans and masonry. Move `kiln_top_in`, `BURNER_PORTS`
and `CONTINUOUS_FRACTION` to a leaf (`shape` or a new `fixtures.py`) so `gas.py`/`electric.py`
can go without breaking v2. Make the private helpers public. Add an import-linter contract:
`kilndesigner.v2` may not import `heatloss`, `simulation`, `target`, `slow`, `gas`, `electric`,
`fire`, `hybrid`, `frame`, `vault`, `band` (fails today on `gas` and `electric`).

## 4. Removing v1 heat breaks the modules that stay (high)

v1's heat results feed modules not being rebuilt:
- `report.py:71-123`: `heat_loss` → electric, gas; `gas`/`fire` → `build_hardware`
  (`:107`); `heat_watts` and `loss` → `castable_reports` (`:123`); `electric`, `gas` →
  `bill_of_materials` (`:135`).
- `heatloss` is imported by `band`, `castable`, `foundation`, `frame`, `movement`, `shell`
  (hot-face temperatures for growth and steel); `gas` by `bom`, `hardware`, `openings`,
  `firing_holes`, `frame`.

So "geometry, plans, masonry and electric sizing stay v1" is consistent only if `gas.py` and
`electric.py`'s sizing (burners, ports, wire) also stay, and if castables, frame and movement get
their temperatures and watts from somewhere.

**Recommend:** split each v1 heat module into "sizing and parts" (kept: burner ports, wire,
chimney parts) and "heat physics" (removed: steady loss, flue-loss combustion, simulation,
target, slow). Give the kept modules a small interface (`hot_face_temperature(kiln, face)`,
`input_watts(kiln)`) that v1 fills today and v2 fills later. Record the split in ADR 0017.

## 5. Heat and statics share the model, not a hot state (medium)

Both read `model.Kiln` and v1's shapes, so the geometry is common. But statics' "hot" state uses
growth at the hot face's temperature throughout (`v2/statics/sources.py:76`) and frame steel at
a given °F (`v2/statics/frame.py:134`); nothing takes heat's wall temperatures. Tobe hot waits on
this (`docs/planning/11-10-26.md:1652`, `:1800`). The heat model's walls are `walls.CellWall`
(`v2/heat/walls.py:56`) per face; statics' sections are solids cut by `section.py`/`row.py`.
There is no face-to-section map.

**Recommend:** a bridge module `v2/hot.py`: from a finished `Firing.state` and the `ZoneModel`'s
faces, give each named face's through-thickness temperature at the peak; statics' `conditions(...,
state)` takes an optional per-face profile for growth and the crushing stand-in. Face names are
already shared through `shape.FaceShape`; use them as the key.

## 6. Duplication inside v2 (medium)

- Two `kiln_path`: `v2/heat/draft.py:759` and `v2/heat/paths.py:180`.
- Two `Band` classes: `v2/heat/bands.py:38` and `paths.py:88`. Two `Sourced`:
  `v2/heat/sources.py:13`, `v2/statics/sources.py:16`.
- Five `NotModelledError` (`heat/chamber.py:54`, `heat/draft.py:755`, `heat/kiln.py:53`,
  `statics/section.py:67`, plus statics' refusals) and three `RangeError`/`*Error` per module.
  A caller must catch each.
- `hydraulic` twice (`heat/draft.py:110`, `heat/kiln.py:847`).
- `chamber.py` (949 lines) and `paths.py` (1,375) each walk the fireboxes, flues and openings
  of the same design through the same v1 helpers (`firebox_parts.openings`, `run_parts.flue_rows`,
  `openings.grid_places`), imported function-locally 20+ times.

**Recommend:** one `v2/errors.py` with `NotModelled(ValueError)` and `OutOfRange(ValueError)`
for both halves; one `Band`, one `Sourced` in `v2/sources.py`; one `hydraulic`. Build a single
`v2/layout.py` (the chamber's openings, fireboxes and flues once, as data) that `chamber.py`
and `paths.py` both read.

## 7. Test cost (medium)

The time is in the band corners, not in unmarked tests.
- The round's report puts C3b's rows at about 22 min and C3a's single chambers at 15–17 min of
  the hour, "nearly all in the corner runs that make the bands"
  (`docs/planning/11-10-26.md:1803`).
- v2 already marks 39 tests `slow`. The unmarked tests are cheap: `test_statics_row.py` and
  `test_heat_rays.py` without `slow` ran 58 tests in 38 s, the slowest 4.2 s
  (`test_one_chamber_under_an_uneven_arch_along_its_depth`). Six row tests take 2.8–4.2 s each
  on OpenCascade cuts; they are near the 5 s line and could take `slow` too.
- The case modules cache with `functools.cache` (`single_cases.py:146-276`,
  `row_cases.py:184-444`, `heat_cases.py:94-196`), which only helps within one process. Each
  corner is a full IDA integration, rerun on every suite run though the engine hasn't changed.
- The 65 top-level v1 test files still run in full. ADR 0017 says they no longer count as
  evidence (`docs/adr/0017-engine-v2.md:44`); they only guard the surfaces.

**Recommend:**
- Add a `bands` marker for the corner runs (every case but the nominal) and keep the nominal
  under `slow`. CI on a branch runs nominal only; the full bands nightly or before a merge.
- Cache firing results on disk, keyed by a hash of the design file, the inputs and the v2
  source tree (e.g. `pytest`'s `config.cache` or a small `scratch/.v2cache` of `.npz`). An
  unchanged engine then re-checks the asserts in seconds.
- Run the band corners in parallel (`pytest-xdist -n 2`, inside the memory cap).
- On Python 3.14, set coverage's `core = sysmon` in `pyproject.toml`; tracing coverage can
  double an integration-heavy run.
- Once the surfaces switch, delete v1's heat tests with the modules (finding 9).

A small fault seen on the way: `v2/heat/rays.py:123` divides by a zero triangle area and warns
(`RuntimeWarning: invalid value encountered in divide`) in four `test_heat_rays.py` tests.
Guard it, or filter degenerate triangles before.

## 8. What the surfaces need, one by one (medium)

- **CLI** (`cli/src/kilndesigner_cli/main.py:14-25`): `build`, `report`, `simulation`, `slow`,
  `target`, `results`. Switch `report` and `simulate` to `v2.design`; `slow` and `target` map to
  `firing.Schedule` and `target.input_for`. Output text from `Step`s needs a printer for SI
  values shown in the design's units.
- **API** (`api/src/kilndesigner_api/routes.py:21-30`, `tasks.py:18-68`): routes return the
  pydantic `Report` and Parquet results. Needs `V2Report` (pydantic) and a writer from
  `Firing` arrays to the Parquet schema in `results.py`.
- **Worker** (`worker/`): no direct engine import; it runs `api.tasks`. v2 firings take
  minutes for rows (finding 7), so jobs need a timeout and progress.
- **MCP** (`mcp-server/src/kilndesigner_mcp/server.py:25-36`): same as the API; add a
  `statics` tool, which v1 has no counterpart for.
- **Web** (`web/src/components/ReportView.tsx`, `FiringPanel.tsx`, `SlowFiringPanel.tsx`):
  reads `heat_loss`, `findings`, and firing series. Needs bands (least/nominal/most) drawn,
  and a no-flags view.

## 9. What stays v1, confirmed (low)

Geometry (`geometry.py`), plans (`plans.py`, `drawings.py`), masonry (`masonry.py`,
`round_masonry.py`, `curve_masonry.py`), BOM, castables and electric element sizing
(`electric.py`) are not rebuilt. That is consistent with v2's scope as long as finding 4's split
is made: they need watts and hot-face temperatures, which v1's heat gives today. After the switch the v1 removals are: `heatloss`,
`heatloss_checks`, `simulation`, `slow`, `target`, `hybrid`, `wood`, the physics halves of
`gas`, `fire`, `electric`, and v1 statics in `frame_checks`, `vault`, `crossing`'s checks; plus
their tests (65 top-level files, most of the old suite).
